"""GLM-5.3-Flash from scratch — poora pipeline, ek file me (Chapters 01–14 ka consolidation).

    uv run study/15-capstone-full-glm-training/glm53_full.py                       # tiny, CPU, ~5 min
    uv run study/15-capstone-full-glm-training/glm53_full.py --preset full --device cuda   # 25.7M, GPU

Stages (default: pretrain,rl,eval):  --stages pretrain,rl,eval,vision

Ye file self-contained hai (sources/repo import nahi karti). Vuk Rosić ke repo
(github.com/vukrosic/glm-5.3-flash-from-scratch, MIT) ke design pe based hai, aur
course me mile teen issues yahan FIXED hain:
  [FIX-07] MoE balance loss differentiable hai (repo me usage counts the, gradient zero).
  [FIX-08] Hyper-connection me identity sirf ek baar judti hai (repo me do baar).
  [FIX-12] Verifier fixed tests ke saath RANDOM hidden tests bhi chalata hai (lookup-table hack band).
"""

from __future__ import annotations

import argparse
import ast
import builtins
import json
import math
import random
import string
import time
from dataclasses import asdict, dataclass, replace
from pathlib import Path

import torch
import torch.nn as nn
import torch.nn.functional as F


# ═════════════════════════════════════════════════════════════════════════════
# Ch 01 · Tokenizer — 1 byte = 1 token, 260 vocab (+3 image IDs for vision)
# ═════════════════════════════════════════════════════════════════════════════
class ByteTokenizer:
    pad_id, bos_id, eos_id, sep_id = 0, 1, 2, 3
    byte_offset = 4
    img_start, img_placeholder, img_end = 260, 261, 262

    def encode(self, text: str, *, bos: bool = False, eos: bool = False) -> list[int]:
        ids = [self.byte_offset + b for b in text.encode("utf-8")]
        return ([self.bos_id] if bos else []) + ids + ([self.eos_id] if eos else [])

    def decode(self, ids: list[int]) -> str:
        out = bytearray()
        for t in ids:
            if t == self.eos_id:
                break
            if self.byte_offset <= t < 260:
                out.append(t - self.byte_offset)
        return out.decode("utf-8", errors="replace")


TOK = ByteTokenizer()


@dataclass(frozen=True)
class Config:
    vocab_size: int = 263          # 256 bytes + 4 special + 3 image
    dim: int = 192
    layers: int = 12
    heads: int = 6
    expert_hidden: int = 384
    experts: int = 8
    top_k: int = 2
    streams: int = 4
    sparse_window: int = 32
    sparse_stride: int = 32
    max_seq: int = 192
    balance_weight: float = 0.01


PRESETS = {
    "tiny": dict(dim=96, layers=4, heads=4, expert_hidden=192),   # ~2.2M, CPU
    "full": dict(),                                                # ~25.7M, repo jaisa
}


# ═════════════════════════════════════════════════════════════════════════════
# Ch 03 · RMSNorm     Ch 04 · RoPE
# ═════════════════════════════════════════════════════════════════════════════
class RMSNorm(nn.Module):
    def __init__(self, dim: int, eps: float = 1e-6):
        super().__init__()
        self.weight = nn.Parameter(torch.ones(dim))
        self.eps = eps

    def forward(self, x):
        scale = torch.rsqrt(x.float().pow(2).mean(-1, keepdim=True) + self.eps)
        return (x.float() * scale).to(x.dtype) * self.weight


def apply_rope(q, k):
    """q, k: [B, T, H, D]. Har pair ko position x frequency se ghumao."""
    T, D = q.shape[1], q.shape[-1]
    freqs = 1.0 / (10000 ** (torch.arange(0, D, 2, device=q.device).float() / D))
    ang = torch.arange(T, device=q.device).float()[:, None] * freqs[None]
    cos, sin = ang.cos()[None, :, None].to(q.dtype), ang.sin()[None, :, None].to(q.dtype)

    def rot(x):
        a, b = x[..., 0::2], x[..., 1::2]
        return torch.stack((a * cos - b * sin, a * sin + b * cos), -1).flatten(-2)

    return rot(q), rot(k)


# ═════════════════════════════════════════════════════════════════════════════
# Ch 05 · Linear attention (running memory)    Ch 06 · Sparse attention
# ═════════════════════════════════════════════════════════════════════════════
class LinearAttention(nn.Module):
    def __init__(self, c: Config):
        super().__init__()
        self.h, self.d = c.heads, c.dim // c.heads
        self.qkv = nn.Linear(c.dim, 3 * c.dim, bias=False)
        self.out = nn.Linear(c.dim, c.dim, bias=False)

    def forward(self, x):
        B, T, D = x.shape
        q, k, v = (t.view(B, T, self.h, self.d) for t in self.qkv(x).chunk(3, -1))
        q, k = apply_rope(q, k)
        q, k = F.elu(q) + 1, F.elu(k) + 1                                 # phi: positive features
        kv = torch.einsum("bthd,bthe->bthde", k, v).cumsum(1)             # S_t (running state)
        num = torch.einsum("bthd,bthde->bthe", q, kv)
        den = torch.einsum("bthd,bthd->bth", q, k.cumsum(1)).unsqueeze(-1)
        return self.out((num / den.clamp_min(1e-6)).reshape(B, T, D))


class SparseAttention(nn.Module):
    def __init__(self, c: Config):
        super().__init__()
        self.h, self.d, self.w, self.s = c.heads, c.dim // c.heads, c.sparse_window, c.sparse_stride
        self.qkv = nn.Linear(c.dim, 3 * c.dim, bias=False)
        self.out = nn.Linear(c.dim, c.dim, bias=False)

    def forward(self, x):
        B, T, D = x.shape
        q, k, v = (t.view(B, T, self.h, self.d) for t in self.qkv(x).chunk(3, -1))
        q, k = apply_rope(q, k)
        pos = torch.arange(T, device=x.device)
        diff = pos[:, None] - pos[None, :]                                  # query - key
        allowed = (diff >= 0) & ((diff < self.w) | (pos[None, :] % self.s == 0))   # local + anchors, causal
        scores = torch.einsum("bthd,bshd->bhts", q, k) * self.d**-0.5
        scores = scores.masked_fill(~allowed, float("-inf"))
        out = torch.einsum("bhts,bshd->bthd", scores.softmax(-1), v)
        return self.out(out.reshape(B, T, D))


# ═════════════════════════════════════════════════════════════════════════════
# Ch 07 · Mixture of Experts — top-k routed + shared expert  [FIX-07]
# ═════════════════════════════════════════════════════════════════════════════
class Expert(nn.Module):
    def __init__(self, dim: int, hidden: int):
        super().__init__()
        self.up = nn.Linear(dim, 2 * hidden, bias=False)
        self.down = nn.Linear(hidden, dim, bias=False)

    def forward(self, x):
        gate, value = self.up(x).chunk(2, -1)
        return self.down(F.silu(gate) * value)                            # SwiGLU


class SparseMoE(nn.Module):
    def __init__(self, c: Config):
        super().__init__()
        self.k, self.n = c.top_k, c.experts
        self.router = nn.Linear(c.dim, c.experts, bias=False)
        self.experts = nn.ModuleList(Expert(c.dim, c.expert_hidden) for _ in range(c.experts))
        self.shared = Expert(c.dim, c.expert_hidden)

    def forward(self, x):
        flat = x.reshape(-1, x.shape[-1])
        logits = self.router(flat)
        top_v, top_i = logits.topk(self.k, -1)
        top_w = top_v.float().softmax(-1).to(flat.dtype)
        out = self.shared(flat)
        counts = torch.zeros(self.n, device=x.device)
        for e, expert in enumerate(self.experts):
            rows, slots = torch.where(top_i == e)
            if rows.numel():
                out = out.index_add(0, rows, expert(flat[rows]) * top_w[rows, slots, None])
                counts[e] = rows.numel()
        # [FIX-07] Switch-Transformer style aux loss: fraction (counts) x mean router PROBABILITY.
        # probs differentiable hai, to router ko sach me balance karne ka gradient milta hai.
        fraction = counts / max(1, flat.shape[0] * self.k)
        probs = logits.float().softmax(-1).mean(0)
        balance = self.n * (fraction * probs).sum()                     # perfect balance pe = 1
        return out.view(x.shape), balance, fraction


# ═════════════════════════════════════════════════════════════════════════════
# Ch 08 · Hyper-connections (4 streams) + hybrid block  [FIX-08]
# ═════════════════════════════════════════════════════════════════════════════
class HybridBlock(nn.Module):
    def __init__(self, c: Config, sparse: bool):
        super().__init__()
        self.attn_norm, self.ffn_norm = RMSNorm(c.dim), RMSNorm(c.dim)
        self.attn = SparseAttention(c) if sparse else LinearAttention(c)
        self.moe = SparseMoE(c)

    def forward(self, x):
        """[FIX-08] Sirf UPDATE return karo (attention + MoE), identity nahi."""
        a = self.attn(self.attn_norm(x))
        m, balance, fraction = self.moe(self.ffn_norm(x + a))
        return a + m, balance, fraction


class HyperConnection(nn.Module):
    def __init__(self, c: Config, sparse: bool):
        super().__init__()
        self.block = HybridBlock(c, sparse)
        self.read = nn.Parameter(torch.linspace(0.1, -0.1, c.streams))
        self.write = nn.Parameter(torch.linspace(-0.1, 0.1, c.streams))

    def forward(self, streams):                                         # [B, T, S, D]
        mixed = torch.einsum("s,btsd->btd", self.read.softmax(0), streams)
        update, balance, fraction = self.block(mixed)
        streams = streams + update.unsqueeze(2) * self.write.softmax(0)[None, None, :, None]
        return streams, balance, fraction


# ═════════════════════════════════════════════════════════════════════════════
# Ch 02 + 06 · Full model — tied embeddings, 3 linear : 1 sparse rhythm
# ═════════════════════════════════════════════════════════════════════════════
class GLM53Flash(nn.Module):
    def __init__(self, c: Config):
        super().__init__()
        self.c = c
        self.embedding = nn.Embedding(c.vocab_size, c.dim)
        self.layers = nn.ModuleList(HyperConnection(c, sparse=(i + 1) % 4 == 0) for i in range(c.layers))
        self.final_norm = RMSNorm(c.dim)
        self.head = nn.Linear(c.dim, c.vocab_size, bias=False)
        self.head.weight = self.embedding.weight                          # weight tying
        for mod in self.modules():
            if isinstance(mod, (nn.Linear, nn.Embedding)):
                nn.init.normal_(mod.weight, std=0.02)

    def forward_embeddings(self, emb):
        streams = emb.unsqueeze(2).expand(-1, -1, self.c.streams, -1).contiguous()
        balance, fractions = 0.0, []
        for layer in self.layers:
            streams, b, f = layer(streams)
            balance = balance + b
            fractions.append(f)
        logits = self.head(self.final_norm(streams.mean(2)))
        return logits, balance / len(self.layers), torch.stack(fractions)

    def forward(self, ids):
        return self.forward_embeddings(self.embedding(ids))

    def param_counts(self) -> dict:
        total = sum(p.numel() for p in self.parameters())
        routed = sum(p.numel() for layer in self.layers for e in layer.block.moe.experts for p in e.parameters())
        return {"total": total, "active_per_token": total - routed + routed * self.c.top_k // self.c.experts}


# ═════════════════════════════════════════════════════════════════════════════
# Ch 09 · Vision — patches -> ViT -> 2x2 merge -> projector -> 16 tokens
# ═════════════════════════════════════════════════════════════════════════════
class VisionEncoder(nn.Module):
    def __init__(self, lm_dim: int, width: int = 24, patch: int = 4, depth: int = 2, heads: int = 4):
        super().__init__()
        self.grid = 32 // patch
        self.patch = nn.Conv2d(3, width, patch, stride=patch)
        self.pos = nn.Parameter(torch.randn(1, self.grid**2, width) * 0.02)
        self.blocks = nn.ModuleList(
            nn.TransformerEncoderLayer(width, heads, 2 * width, dropout=0.0, batch_first=True, norm_first=True)
            for _ in range(depth))                                       # bidirectional attention
        self.norm = RMSNorm(width)
        self.merge = nn.Linear(4 * width, lm_dim)                        # 2x2 neighbours -> 1 token
        self.project = nn.Sequential(nn.Linear(lm_dim, lm_dim), nn.GELU(), nn.Linear(lm_dim, lm_dim))

    def forward(self, images):                                           # [B, 3, 32, 32]
        x = self.patch(images).flatten(2).transpose(1, 2) + self.pos     # [B, 64, w]
        for blk in self.blocks:
            x = blk(x)
        B, N, W = x.shape
        g = self.grid
        x = self.norm(x).view(B, g // 2, 2, g // 2, 2, W).permute(0, 1, 3, 2, 4, 5).reshape(B, (g // 2) ** 2, 4 * W)
        return self.project(self.merge(x))                               # [B, 16, lm_dim]


SEGMENTS = {0: "abcdef", 1: "bc", 2: "abged", 3: "abgcd", 4: "fgbc", 5: "afgcd", 6: "afgecd", 7: "abc", 8: "abcdefg", 9: "abfgcd"}
SEG_BOX = {"a": (4, 7, 8, 24), "g": (14, 17, 8, 24), "d": (25, 28, 8, 24),
           "f": (6, 15, 5, 8), "b": (6, 15, 24, 27), "e": (16, 26, 5, 8), "c": (16, 26, 24, 27)}


def digit_images(labels: torch.Tensor, seed: int) -> torch.Tensor:
    g = torch.Generator().manual_seed(seed)
    imgs = torch.zeros(len(labels), 3, 32, 32)
    for i, lab in enumerate(labels.tolist()):
        dy, dx = (int(torch.randint(-2, 3, (1,), generator=g)) for _ in range(2))
        color = 0.55 + 0.45 * torch.rand(3, 1, 1, generator=g)
        for s in SEGMENTS[lab]:
            y0, y1, x0, x1 = SEG_BOX[s]
            imgs[i, :, max(0, y0 + dy):min(32, y1 + dy), max(0, x0 + dx):min(32, x1 + dx)] = color
    return (imgs + 0.06 * torch.rand(imgs.shape, generator=g)).clamp(0, 1)


# ═════════════════════════════════════════════════════════════════════════════
# Ch 10 · Data — 8 synthetic Python families, deterministic splits
# ═════════════════════════════════════════════════════════════════════════════
@dataclass(frozen=True)
class Family:
    name: str
    arg: str
    descriptions: tuple[str, ...]
    body: str
    cases: tuple
    reference: object          # trusted Python function (random hidden tests ke liye)
    random_input: object


R = random.Random
FAMILIES = (
    Family("increment", "x", ("Return x plus one.", "Increase x by one."), "\n    return x + 1\n",
           (((-3,), -2), ((0,), 1), ((7,), 8)), lambda x: x + 1, lambda r: (r.randint(-999, 999),)),
    Family("double", "x", ("Return two times x.", "Double the input."), "\n    return x * 2\n",
           (((-4,), -8), ((0,), 0), ((6,), 12)), lambda x: x * 2, lambda r: (r.randint(-999, 999),)),
    Family("square", "x", ("Return x squared.", "Multiply x by itself."), "\n    return x * x\n",
           (((-4,), 16), ((0,), 0), ((5,), 25)), lambda x: x * x, lambda r: (r.randint(-99, 99),)),
    Family("absolute", "x", ("Return the absolute value of x.", "Make a negative x positive."), "\n    return -x if x < 0 else x\n",
           (((-7,), 7), ((0,), 0), ((9,), 9)), abs, lambda r: (r.randint(-999, 999),)),
    Family("nonnegative", "x", ("Clamp x to at least zero.", "Return zero when x is negative."), "\n    return x if x > 0 else 0\n",
           (((-5,), 0), ((0,), 0), ((8,), 8)), lambda x: max(x, 0), lambda r: (r.randint(-999, 999),)),
    Family("even", "x", ("Return whether x is even.", "Check divisibility by two."), "\n    return x % 2 == 0\n",
           (((-3,), False), ((0,), True), ((8,), True)), lambda x: x % 2 == 0, lambda r: (r.randint(-999, 999),)),
    Family("reverse", "text", ("Return text in reverse order.", "Reverse the string."), "\n    return text[::-1]\n",
           ((("",), ""), (("abc",), "cba"), (("level",), "level")), lambda t: t[::-1],
           lambda r: ("".join(r.choice(string.ascii_lowercase) for _ in range(r.randint(0, 9))),)),
    Family("list_sum", "values", ("Return the sum of values.", "Add every number in the list."), "\n    return sum(values)\n",
           ((([],), 0), (([1, 2, 3],), 6), (([-2, 5],), 3)), sum,
           lambda r: ([r.randint(-50, 50) for _ in range(r.randint(0, 6))],)),
)
SPLIT_SEEDS = {"pretrain": 42, "dev": 1701, "rl": 3907, "confirm": 8123}


@dataclass(frozen=True)
class Task:
    task_id: str
    family: Family
    entry: str
    prompt: str


def make_task(fam: Family, split: str, index: int, seed: int) -> Task:
    rng = R((seed + 1) * 1_000_003 + index * 9176 + sum(map(ord, fam.name)))
    entry = f"{fam.name}_" + "".join(rng.choice(string.ascii_lowercase) for _ in range(7))
    prompt = f"# Complete this Python function.\n# {rng.choice(fam.descriptions)}\ndef {entry}({fam.arg}):"
    return Task(f"{split}-{fam.name}-{index:03d}", fam, entry, prompt)


def tasks_for(split: str, per_family: int, families: set[str] | None = None) -> list[Task]:
    out = [make_task(f, split, i, SPLIT_SEEDS[split] + fi * 53)
           for fi, f in enumerate(FAMILIES) for i in range(per_family)]
    return [t for t in out if families is None or t.family.name in families]


def pretrain_batch(step: int, batch: int, seq: int, device):
    rows = []
    for j in range(batch):
        rng = R(SPLIT_SEEDS["pretrain"] * 10_000_019 + step * batch + j)
        t = make_task(FAMILIES[rng.randrange(len(FAMILIES))], "pretrain", step * batch + j, SPLIT_SEEDS["pretrain"])
        ids = TOK.encode(t.prompt + t.family.body, bos=True, eos=True)
        rows.append(ids + [TOK.pad_id] * (seq + 1 - len(ids)))
    v = torch.tensor(rows, device=device)
    labels = v[:, 1:].masked_fill(v[:, 1:] == TOK.pad_id, -100)        # padding ka loss nahi
    return v[:, :-1], labels


# ═════════════════════════════════════════════════════════════════════════════
# Ch 12 · Verifier — AST sandbox + fixed tests + RANDOM hidden tests  [FIX-12]
# ═════════════════════════════════════════════════════════════════════════════
DENIED = (ast.Import, ast.ImportFrom, ast.ClassDef, ast.AsyncFunctionDef, ast.With, ast.AsyncWith, ast.Lambda,
          ast.Global, ast.Nonlocal, ast.While, ast.For, ast.AsyncFor, ast.Try, ast.Raise, ast.Delete)
SAFE = {"sum", "len", "abs", "min", "max", "bool", "int", "str"}
SAFE_BUILTINS = {n: getattr(builtins, n) for n in SAFE}


def verify(task: Task, completion: str, n_random: int = 8) -> str:
    """Return 'passed' | 'failed' | 'invalid'. Fail closed."""
    source = task.prompt + completion
    try:
        if len(source.encode()) > 2048:
            raise ValueError("too large")
        tree = ast.parse(source)
        fns = [n for n in tree.body if isinstance(n, ast.FunctionDef)]
        if len(fns) != 1 or fns[0].name != task.entry or len(tree.body) != 1:
            raise ValueError("exactly one requested function")
        for node in ast.walk(tree):
            if isinstance(node, DENIED) or isinstance(node, ast.Attribute) or \
                    (isinstance(node, ast.Name) and node.id.startswith("__")):
                raise ValueError("disallowed")
            if isinstance(node, ast.Call) and (not isinstance(node.func, ast.Name) or node.func.id not in SAFE):
                raise ValueError("unsafe call")
        ns: dict = {"__builtins__": SAFE_BUILTINS}
        exec(compile(tree, "candidate.py", "exec"), ns)
        fn = ns[task.entry]
    except Exception:
        return "invalid"
    rng = R()  # [FIX-12] har call pe naye inputs: ratta nahi chalega
    checks = list(task.family.cases) + [(a, task.family.reference(*a)) for a in
                                         (task.family.random_input(rng) for _ in range(n_random))]
    for args, expected in checks:
        try:
            got = fn(*[list(a) if isinstance(a, list) else a for a in args])
            if type(got) is not type(expected) or got != expected:
                return "failed"
        except Exception:
            return "failed"
    return "passed"


def parseable(task: Task, completion: str) -> bool:
    if not completion.endswith("\n"):
        return False
    try:
        tree = ast.parse(task.prompt + completion)
        return len(tree.body) == 1 and isinstance(tree.body[0], ast.FunctionDef)
    except SyntaxError:
        return False


# ═════════════════════════════════════════════════════════════════════════════
# Generation — greedy ya sampled, batched group
# ═════════════════════════════════════════════════════════════════════════════
@torch.no_grad()
def generate(model: GLM53Flash, task: Task, n: int, *, temperature: float, sample: bool,
             max_new: int, seed: int) -> list[list[int]]:
    model.eval()
    device = next(model.parameters()).device
    prompt = TOK.encode(task.prompt, bos=True)
    rows = torch.tensor([prompt] * n, device=device)
    outs, done = [[] for _ in range(n)], [False] * n
    gen = torch.Generator(device="cpu").manual_seed(seed)
    for _ in range(max_new):
        logits = model(rows)[0][:, -1].float() / temperature
        logits[:, [TOK.pad_id, TOK.bos_id, TOK.sep_id, 260, 261, 262]] = -float("inf")
        probs = logits.softmax(-1).cpu()
        nxt = torch.multinomial(probs, 1, generator=gen).squeeze(1) if sample else probs.argmax(-1)
        for i, t in enumerate(nxt.tolist()):
            if done[i]:
                nxt[i] = TOK.eos_id
                continue
            outs[i].append(t)
            if t == TOK.eos_id or parseable(task, TOK.decode(outs[i])):
                done[i] = True
        rows = torch.cat([rows, nxt[:, None].to(device)], 1)
        if all(done):
            break
    return outs


# ═════════════════════════════════════════════════════════════════════════════
# Ch 10 · Pretraining
# ═════════════════════════════════════════════════════════════════════════════
def pretrain(model: GLM53Flash, steps: int, batch: int, lr: float, device, log) -> None:
    opt = torch.optim.AdamW(model.parameters(), lr=lr, betas=(0.9, 0.95), weight_decay=0.1)
    for step in range(1, steps + 1):
        model.train()
        x, y = pretrain_batch(step - 1, batch, 128, device)
        logits, balance, _ = model(x)                                         # 1. predict
        lm = F.cross_entropy(logits.reshape(-1, model.c.vocab_size), y.reshape(-1), ignore_index=-100)  # 2. compare
        loss = lm + model.c.balance_weight * balance
        if not torch.isfinite(loss):
            raise FloatingPointError("non-finite loss")
        opt.zero_grad(set_to_none=True)
        loss.backward()                                                        # 3. backprop
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()                                                             # 4. update
        if step == 1 or step % max(1, steps // 6) == 0:
            log(f"  pretrain step {step:>4}/{steps}  loss {lm.item():.3f}  balance {balance.item():.3f}")


# ═════════════════════════════════════════════════════════════════════════════
# Ch 12–13 · RL — executable reward, RLOO, last block + head
# ═════════════════════════════════════════════════════════════════════════════
def reward(task: Task, completion: str) -> float:
    return {"passed": 1.0, "failed": 0.0, "invalid": -0.1}[verify(task, completion)]


def leave_one_out(r: list[float]) -> list[float]:
    total = sum(r)
    return [x - (total - x) / (len(r) - 1) for x in r]


def completion_logprob(model: GLM53Flash, task: Task, completions: list[list[int]]) -> torch.Tensor:
    device = next(model.parameters()).device
    prompt = TOK.encode(task.prompt, bos=True)
    L = max(map(len, completions))
    seq = torch.tensor([prompt + c + [0] * (L - len(c)) for c in completions], device=device)
    logits = model(seq[:, :-1])[0][:, len(prompt) - 1:].float()
    lp = logits.log_softmax(-1).gather(-1, seq[:, len(prompt):, None]).squeeze(-1)
    lengths = torch.tensor([len(c) for c in completions], device=device)
    mask = torch.arange(L, device=device)[None] < lengths[:, None]
    return (lp * mask).sum(1) / lengths                                      # per-token average


def rl(model: GLM53Flash, families: set[str], groups: int, group_size: int, temperature: float,
       lr: float, seed: int, log) -> dict:
    for p in model.parameters():
        p.requires_grad = False
    trainable = [*model.layers[-1].parameters(), *model.final_norm.parameters(), *model.embedding.parameters()]
    for p in trainable:
        p.requires_grad = True
    log(f"  RL trainable params: {sum(p.numel() for p in trainable):,} / {sum(p.numel() for p in model.parameters()):,}")
    opt = torch.optim.AdamW(trainable, lr=lr, weight_decay=0.0)
    pool = tasks_for("rl", 16, families)
    order: list[Task] = []
    while len(order) < groups:                                             # shuffled passes over the pool
        block = list(pool)
        R(seed + len(order)).shuffle(block)
        order += block
    order = order[:groups]
    stats = {"updates": 0, "exact": 0, "rollouts": 0}
    for g, task in enumerate(order, 1):
        comps = generate(model, task, group_size, temperature=temperature, sample=True, max_new=32, seed=seed + g * 17)
        rewards = [reward(task, TOK.decode(c)) for c in comps]
        stats["exact"] += sum(r == 1.0 for r in rewards)
        stats["rollouts"] += len(rewards)
        if max(rewards) - min(rewards) > 1e-8 and all(comps):              # spread nahi = signal nahi
            model.train()
            adv = torch.tensor(leave_one_out(rewards), device=next(model.parameters()).device)
            loss = -(adv * completion_logprob(model, task, comps)).mean()
            opt.zero_grad(set_to_none=True)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(trainable, 1.0)
            opt.step()
            stats["updates"] += 1
        if g % max(1, groups // 4) == 0:
            log(f"  RL group {g:>3}/{groups}  updates {stats['updates']}  exact rollouts {stats['exact']}/{stats['rollouts']}")
    for p in model.parameters():
        p.requires_grad = True
    return stats


# ═════════════════════════════════════════════════════════════════════════════
# Ch 14 · Evaluation — greedy pass@1, pass@k, paired McNemar test
# ═════════════════════════════════════════════════════════════════════════════
def pass_at_k(n: int, c: int, k: int) -> float:
    return 1.0 if n - c < k else 1.0 - math.comb(n - c, k) / math.comb(n, k)


def evaluate(model: GLM53Flash, split: str, per_family: int, samples: int, seed: int) -> dict:
    greedy, by_family = {}, {}
    sampled = []
    for i, task in enumerate(tasks_for(split, per_family)):
        g = generate(model, task, 1, temperature=1.0, sample=False, max_new=32, seed=0)[0]
        greedy[task.task_id] = verify(task, TOK.decode(g)) == "passed"
        outs = generate(model, task, samples, temperature=0.35, sample=True, max_new=32, seed=seed + i)
        c = sum(verify(task, TOK.decode(o)) == "passed" for o in outs)
        sampled.append(c)
        fam = by_family.setdefault(task.family.name, {"greedy": 0, "sampled": 0, "tasks": 0})
        fam["greedy"] += greedy[task.task_id]
        fam["sampled"] += c
        fam["tasks"] += 1
    return {"greedy": greedy, "by_family": by_family,
            "pass@1": sum(pass_at_k(samples, c, 1) for c in sampled) / len(sampled),
            f"pass@{samples}": sum(pass_at_k(samples, c, samples) for c in sampled) / len(sampled)}


def mcnemar(before: list[bool], after: list[bool]) -> tuple[int, int, float]:
    gains = sum((not b) and a for b, a in zip(before, after))
    losses = sum(b and (not a) for b, a in zip(before, after))
    n = gains + losses
    if n == 0:
        return 0, 0, 1.0
    return gains, losses, min(1.0, 2 * sum(math.comb(n, k) for k in range(min(gains, losses) + 1)) / 2**n)


# ═════════════════════════════════════════════════════════════════════════════
# Ch 09 · Vision stage — digit reader on top of the same LM
# ═════════════════════════════════════════════════════════════════════════════
def vision_stage(c: Config, steps: int, device, log, seed: int = 42) -> dict:
    torch.manual_seed(seed)
    lm = GLM53Flash(replace(c, dim=32, layers=1, heads=4, expert_hidden=48, experts=4, streams=2,
                            sparse_window=8, sparse_stride=8)).to(device)
    enc = VisionEncoder(lm.c.dim).to(device)
    params = list(lm.parameters()) + list(enc.parameters())
    opt = torch.optim.AdamW(params, lr=2e-3)
    prompt = TOK.encode("Digit: ", bos=True)

    def run(images, labels):
        ids = torch.tensor([[TOK.bos_id, TOK.img_start] + [TOK.img_placeholder] * 16 + [TOK.img_end] + prompt[1:]]
                           * len(labels), device=device)
        emb = lm.embedding(ids)
        emb = emb.masked_scatter((ids == TOK.img_placeholder)[..., None].expand_as(emb), enc(images))
        logits = lm.forward_embeddings(emb)[0][:, -1]
        target = torch.tensor([TOK.byte_offset + ord(str(int(v))) for v in labels], device=device)
        return logits, target

    def accuracy():
        labels = torch.arange(200) % 10
        with torch.no_grad():
            logits, target = run(digit_images(labels, 10_000 + seed).to(device), labels)
        return int((logits.argmax(-1) == target).sum())

    before = accuracy()
    for step in range(steps):
        labels = (torch.arange(40) + step) % 10
        logits, target = run(digit_images(labels, seed + step).to(device), labels)
        loss = F.cross_entropy(logits, target)                               # answer-only loss
        opt.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(params, 1.0)
        opt.step()
    after = accuracy()
    log(f"  vision: held-out digits {before}/200 -> {after}/200  ({sum(p.numel() for p in params):,} params)")
    return {"before": before, "after": after}


# ═════════════════════════════════════════════════════════════════════════════
# Main — receipt ke saath poora pipeline
# ═════════════════════════════════════════════════════════════════════════════
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--preset", choices=PRESETS, default="tiny")
    ap.add_argument("--stages", default="pretrain,rl,eval")
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--pretrain-steps", type=int, default=None, help="default: tiny 200, full 100")
    ap.add_argument("--rl-groups", type=int, default=48)
    ap.add_argument("--group-size", type=int, default=16)
    ap.add_argument("--rl-families", default="increment,double,even")
    ap.add_argument("--out", type=Path, default=Path("runs/capstone"))
    args = ap.parse_args()
    stages = set(args.stages.split(","))
    device = torch.device(args.device)
    tiny = args.preset == "tiny"
    steps = args.pretrain_steps or (200 if tiny else 100)
    receipt: dict = {"args": {k: str(v) for k, v in vars(args).items()}, "fixes": ["FIX-07", "FIX-08", "FIX-12"]}
    started = time.perf_counter()
    log = lambda msg: print(f"[{time.perf_counter() - started:6.1f}s] {msg}", flush=True)  # noqa: E731

    torch.manual_seed(args.seed)
    random.seed(args.seed)
    config = Config(**PRESETS[args.preset])
    model = GLM53Flash(config).to(device)
    receipt["config"], receipt["params"] = asdict(config), model.param_counts()
    log(f"model {args.preset}: {receipt['params']['total']:,} params, ~{receipt['params']['active_per_token']:,} active/token")

    if "pretrain" in stages:
        log(f"STAGE pretrain ({steps} steps)")
        pretrain(model, steps, batch=16 if tiny else 32, lr=1e-3 if tiny else 3e-4, device=device, log=log)
    rl_families = set(args.rl_families.split(","))
    before_state = {k: v.detach().clone() for k, v in model.state_dict().items()}

    if "rl" in stages:
        log(f"STAGE rl ({args.rl_groups} groups x {args.group_size} rollouts, families {sorted(rl_families)})")
        receipt["rl"] = rl(model, rl_families, args.rl_groups, args.group_size, temperature=0.35,
                           lr=1e-4 if tiny else 5e-5, seed=31415, log=log)

    if "eval" in stages:
        log("STAGE eval (confirm split — sirf ek baar, aakhir me)")
        after_eval = evaluate(model, "confirm", per_family=4, samples=8, seed=8675309)
        after_state = {k: v.detach().clone() for k, v in model.state_dict().items()}  # copy! state_dict() sirf references deta hai
        model.load_state_dict(before_state)
        before_eval = evaluate(model, "confirm", per_family=4, samples=8, seed=8675309)
        model.load_state_dict(after_state)
        ids = [t.task_id for t in tasks_for("confirm", 4, rl_families)]
        gains, losses, p = mcnemar([before_eval["greedy"][i] for i in ids], [after_eval["greedy"][i] for i in ids])
        log(f"  RL families greedy pass@1: {sum(before_eval['greedy'][i] for i in ids)}/{len(ids)} -> "
            f"{sum(after_eval['greedy'][i] for i in ids)}/{len(ids)}   (gains {gains}, losses {losses}, McNemar p = {p:.4f})")
        log(f"  all 8 families sampled pass@1 {before_eval['pass@1']:.1%} -> {after_eval['pass@1']:.1%},"
            f"  pass@8 {before_eval['pass@8']:.1%} -> {after_eval['pass@8']:.1%}")
        for fam in before_eval["by_family"]:
            b, a = before_eval["by_family"][fam]["sampled"], after_eval["by_family"][fam]["sampled"]
            log(f"    {'RL ' if fam in rl_families else '   '}{fam:12} sampled exact {b:>2}/32 -> {a:>2}/32 {'↑' if a > b else '↓' if a < b else '—'}")
        receipt["eval"] = {"before": {k: v for k, v in before_eval.items() if k != "greedy"},
                           "after": {k: v for k, v in after_eval.items() if k != "greedy"},
                           "mcnemar": {"gains": gains, "losses": losses, "p": p}}

    if "vision" in stages:
        log("STAGE vision (digit reader, alag chhota LM)")
        receipt["vision"] = vision_stage(config, steps=120, device=device, log=log)

    receipt["elapsed_seconds"] = round(time.perf_counter() - started, 1)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "receipt.json").write_text(json.dumps(receipt, indent=2, default=str) + "\n")
    torch.save(model.state_dict(), args.out / "model.pt")
    log(f"done. receipt -> {args.out / 'receipt.json'}, weights -> {args.out / 'model.pt'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
