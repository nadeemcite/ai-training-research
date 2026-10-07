"""Lab 10 — Pretraining loop: random weights se Python likhna (CPU pe ~2 min).

Run:  uv run study/10-pretraining-loop/lab_pretrain.py

Repo ka asli model, data, generation aur verifier import hota hai. Sirf model chhota hai
(2.2M params, taaki CPU pe jaldi chale); training loop repo ke train_pretrain.py jaisa hi hai.
"""

import sys
import time
from pathlib import Path

import torch
import torch.nn.functional as F

REPO = Path(__file__).resolve().parents[2] / "sources" / "repo"
sys.path[:0] = [str(REPO), str(REPO / "scripts")]

from glm53_flash import ByteTokenizer, GLM53FlashFromScratch, ModelConfig  # noqa: E402
from glm53_flash.evaluator import evaluate_source  # noqa: E402
from glm53_flash.runtime import generate_group  # noqa: E402
from glm53_flash.tasks import frozen_tasks, pretraining_text  # noqa: E402
from train_pretrain import batch_for  # noqa: E402

tok = ByteTokenizer()
cpu = torch.device("cpu")

# --- Experiment 1: ek training example — input aur label ek position shifted --
print("Exp 1  ek pretraining example:")
print("       " + pretraining_text(0).replace("\n", "\n       "))
x, y, n = batch_for(tok, step=0, batch_size=1, sequence_length=128, seed=42, device=cpu)
show = 6
print(f"       input  ids[:{show}] = {x[0, :show].tolist()}  -> {tok.decode(x[0, 1:show].tolist())!r} (+BOS)")
print(f"       labels ids[:{show}] = {y[0, :show].tolist()}  (input ka agla token)")
print(f"       padding labels = -100 -> loss me gina nahi jaata. Asli target tokens: {n} / {y.numel()}")

# --- Experiment 2: cross-entropy haath se == F.cross_entropy -----------------
torch.manual_seed(0)
logits = torch.randn(4, 260)
labels = torch.tensor([104, 105, -100, 106])
by_hand = -torch.log_softmax(logits, -1)[[0, 1, 3], [104, 105, 106]].mean()
library = F.cross_entropy(logits, labels, ignore_index=-100)
print(f"Exp 2  haath se {by_hand:.4f}  |  F.cross_entropy {library:.4f}  |  random guess ln(260) = {torch.log(torch.tensor(260.0)):.4f}")

# --- Experiment 3: gradient clipping ----------------------------------------
w = torch.nn.Parameter(torch.ones(3))
(w * torch.tensor([30.0, 40.0, 0.0])).sum().backward()
before = w.grad.norm().item()
torch.nn.utils.clip_grad_norm_([w], max_norm=1.0)
print(f"Exp 3  gradient {[30.0, 40.0, 0.0]} norm={before:.0f}  -> clip ke baad {[round(g, 2) for g in w.grad.tolist()]} "
      f"norm={w.grad.norm():.2f}  (direction same, size 1)")

# --- Experiment 4: asli pretraining — random se Python tak -------------------
dev = frozen_tasks("dev", per_family=1)  # 8 unseen function names, har family se 1


def dev_score(model) -> tuple[int, str]:
    passed, sample = 0, ""
    for task in dev:
        out = generate_group(model, tok, task, group_size=1, max_new_tokens=40,
                             temperature=1.0, sample=False, seed=0)[0]["completion"]
        passed += evaluate_source(task, task.prompt + out).passed
        if task.family == "double":
            sample = out.strip()[:28]
    return passed, sample


config = ModelConfig(dim=96, layers=4, heads=4, expert_hidden=192)  # repo: dim 192, 12 layers
torch.manual_seed(42)
model = GLM53FlashFromScratch(config)
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3, betas=(0.9, 0.95), weight_decay=0.1)
print(f"Exp 4  model {sum(p.numel() for p in model.parameters()):,} params, batch 16, 300 steps")
print("       step   loss   dev(8)  'double' ka greedy jawab")
score, sample = dev_score(model)
print(f"       {0:>4}      -   {score}/8     {sample!r}")
started = time.perf_counter()
for step in range(1, 301):
    model.train()
    x, y, _ = batch_for(tok, step=step - 1, batch_size=16, sequence_length=128, seed=42, device=cpu)
    logits, usage = model(x)                                                       # 1. predict
    loss = F.cross_entropy(logits.reshape(-1, config.vocab_size), y.reshape(-1),   # 2. compare
                           ignore_index=-100)
    optimizer.zero_grad()
    loss.backward()                                                                # 3. backprop
    torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
    optimizer.step()                                                               # 4. update
    if step % 50 == 0:
        score, sample = dev_score(model)
        print(f"       {step:>4}  {loss.item():.3f}   {score}/8     {sample!r}")
print(f"       ({time.perf_counter() - started:.0f}s CPU pe)")

# TODO (tumhara kaam):
#  a) lr=1e-3 ko 1e-2 aur 1e-4 karke chalao. Loss curve aur dev score kaise badle?
#  b) clip_grad_norm_ wali line hata do. Kya training phir bhi stable hai? (lr=1e-2 ke saath try karo)
#  c) Exp 1: pretraining_text(1), (2), (3) print karo. Kitne alag "families" dikhte hain?
