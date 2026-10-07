"""Lab 7 — Mixture of Experts: router, top-k, shared expert, load balancing.

Run:  uv run study/07-mixture-of-experts/lab_moe.py
"""

import torch
import torch.nn as nn
import torch.nn.functional as F

torch.manual_seed(0)
DIM, HIDDEN, EXPERTS, TOP_K = 192, 384, 8, 2  # same as repo ModelConfig


class Expert(nn.Module):
    """SwiGLU feed-forward, same as repo."""

    def __init__(self, dim: int, hidden: int):
        super().__init__()
        self.up = nn.Linear(dim, hidden * 2, bias=False)
        self.down = nn.Linear(hidden, dim, bias=False)

    def forward(self, x):
        gate, value = self.up(x).chunk(2, dim=-1)
        return self.down(F.silu(gate) * value)


class SparseMoE(nn.Module):
    """Same logic as sources/repo/glm53_flash/model.py (copied for study)."""

    def __init__(self):
        super().__init__()
        self.router = nn.Linear(DIM, EXPERTS, bias=False)
        self.experts = nn.ModuleList([Expert(DIM, HIDDEN) for _ in range(EXPERTS)])
        self.shared = Expert(DIM, HIDDEN)  # har token isse guzarta hai

    def forward(self, x):
        flat = x.reshape(-1, DIM)
        logits = self.router(flat)
        top_values, top_indices = logits.topk(TOP_K, dim=-1)
        top_weights = torch.softmax(top_values, dim=-1)
        output = self.shared(flat)
        usage = torch.zeros(EXPERTS)
        for expert_id, expert in enumerate(self.experts):
            positions, slots = torch.where(top_indices == expert_id)
            if positions.numel() == 0:
                continue
            output.index_add_(0, positions, expert(flat[positions]) * top_weights[positions, slots, None])
            usage[expert_id] = positions.numel()
        usage = usage / (flat.shape[0] * TOP_K)
        return output.view(x.shape), usage, top_indices, top_weights


moe = SparseMoE()

# --- Experiment 1: router ne kis token ko kahan bheja? ----------------------
tokens = torch.randn(1, 5, DIM)
with torch.no_grad():
    out, usage, idx, wts = moe(tokens)
print("Exp 1  token -> chune gaye experts (weights)")
for t in range(5):
    picks = ", ".join(f"E{e + 1} ({w:.2f})" for e, w in zip(idx[t].tolist(), wts[t].tolist()))
    print(f"       token {t}: {picks}  + shared")
print(f"       output shape {tuple(out.shape)} = input shape  ✓")

# --- Experiment 2: usage ka sum = 1 (repo ka test bhi yahi check karta hai) --
print("Exp 2  usage =", [round(u, 2) for u in usage.tolist()], " sum =", round(usage.sum().item(), 3))

# --- Experiment 3: total vs active parameters --------------------------------
per_expert = sum(p.numel() for p in Expert(DIM, HIDDEN).parameters())
total_ffn = per_expert * (EXPERTS + 1)
active_ffn = per_expert * (TOP_K + 1)
print(f"Exp 3  ek expert = {per_expert:,} params")
print(f"       ek MoE layer: total {total_ffn:,}  |  har token ke liye active {active_ffn:,}  ({active_ffn / total_ffn:.0%})")
print(f"       12 layers:    total {12 * total_ffn:,}  |  active {12 * active_ffn:,}")
glm_ratio = 9 / 289  # GLM-5.3: 8 of 288 routed + 1 shared
print(f"       GLM-5.3 (8 of 288 + shared) me ek token ~{glm_ratio:.1%} experts use karta hai")

# --- Experiment 4: load-balance loss (repo ka formula) -----------------------


def balance_loss(u: torch.Tensor) -> float:
    return (((u - 1.0 / EXPERTS) ** 2).mean() * EXPERTS).item()


balanced = torch.full((EXPERTS,), 1 / EXPERTS)
collapsed = torch.tensor([0.5, 0.5, 0, 0, 0, 0, 0, 0])
print(f"Exp 4  balanced usage  -> balance loss {balance_loss(balanced):.3f}")
print(f"       collapsed (sirf E1, E2) -> balance loss {balance_loss(collapsed):.3f}")

# --- Experiment 5: router training — balance loss ke saath vs bina ----------
# Real hidden states me aksar ek "common direction" hoti hai (mu). Isse router kuch experts
# ki taraf jhuk sakta hai. Task: har token ko ek target vector pe map karna.
mu = F.normalize(torch.randn(DIM), dim=0)
data = torch.randn(512, DIM) + 3 * mu
target = torch.tanh((data - 3 * mu) @ torch.randn(DIM, DIM) / DIM**0.5)


def train(balance_weight: float, seed: int) -> torch.Tensor:
    torch.manual_seed(seed)
    m = SparseMoE()
    opt = torch.optim.AdamW(m.parameters(), lr=3e-3)
    for _ in range(150):
        out, u, _, _ = m(data)
        loss = F.mse_loss(out, target)
        # Repo ka `usage` counts se banta hai (uspe gradient nahi). Yahan router probabilities
        # ka differentiable version use kar rahe hain taaki router seekh sake.
        probs = torch.softmax(m.router(data), dim=-1).mean(0)
        loss = loss + balance_weight * ((probs - 1 / EXPERTS) ** 2).mean() * EXPERTS
        opt.zero_grad()
        loss.backward()
        opt.step()
    return u


for bw in (0.0, 1.0):
    for seed in (1, 2):
        u = train(bw, seed)
        print(f"Exp 5  balance_weight={bw}  seed={seed}  usage={[round(x, 2) for x in u.tolist()]}  "
              f"min={u.min():.2f}  max={u.max():.2f}")

# TODO (tumhara kaam):
#  a) TOP_K = 1 aur TOP_K = 4 karke Exp 3 dekho. Active params kaise badle?
#  b) Exp 5 me `3 * mu` ko `8 * mu` kar do (common direction aur strong). Bina balance loss ke min usage kitna gira?
#  c) Repo ka test chalao: cd sources/repo && uv run python -m pytest tests/test_lab.py -k usage -q
