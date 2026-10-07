<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 15 — Capstone: poora GLM-5.3-Flash ek file me 🎓](README.md) › Reading 3 / 6
<!-- /nav:top -->

# 03 · Kaise chalayein

## Tiny (~4–5 min) — default

```bash
uv run study/15-capstone-full-glm-training/glm53_full.py --stages pretrain,rl,eval,vision
```

| Stage | Kya hota hai | Time (Mac CPU) |
|---|---|---:|
| `pretrain` | 2.2M model, 200 steps, batch 16, AdamW lr 1e-3 | ~50 s |
| `rl` | 48 groups × 16 rollouts, families increment/double/even, last block + head, RLOO | ~85 s |
| `eval` | Confirm split (32 tasks): greedy + 8 samples, **before aur after** dono, McNemar | ~115 s |
| `vision` | Alag chhota LM + vision encoder, 120 steps, 200 held-out digits | ~4 s |

## Mac GPU (MPS) — unified memory ka fayda 🍎

Apple Silicon Mac pe `--device auto` khud **MPS** (Metal GPU) chunta hai. Unified memory ka matlab hai ki CPU aur GPU ek hi RAM share karte hain, to model "GPU memory me copy" nahi karna padta. 16 GB me 25.7M model aaraam se fit hota hai.

**Pehle GPU dhheema tha!** Pehle version me MoE ek Python loop (`torch.where` + `index_add`) tha. Har expert ke liye token-count badalta tha, aur har baar CPU↔GPU sync hota tha. Backward pass forward se 3–7× slow tha. Fix: **batched MoE** (saare experts ek batched matmul + mostly-zero gate matrix, `SparseMoE` docstring dekho). Math bilkul same hai: outputs, balance loss aur gradients verify kiye gaye.

M1 Pro (14-core GPU), ek training step:

| Model | CPU (pehle) | MPS, loop MoE | **MPS, batched MoE** |
|---|---:|---:|---:|
| tiny, batch 16 | 0.24 s | 0.44–1.38 s | **0.15 s** |
| full 25.7M, batch 32 | 2.9 s | 2.0–2.75 s | **1.14 s** (2.5× tez) |

**Generation (RL aur eval) GPU pe tez nahi hui**, kyunki har naye token pe poora sequence dobara chalta hai (KV cache nahi hai), aur chhote kaam pe GPU ka overhead haavi hai.

> **Research lesson:** "GPU = tez" automatic nahi hai. Pehle **measure** karo, phir dhoondho ki time kahan jaa raha hai (yahan backward me), aur phir code ko hardware ke hisaab se badlo.

## Full (25.7M)

```bash
uv run study/15-capstone-full-glm-training/glm53_full.py --preset full --eval-per-family 8
```

Repo jaisa model hai: dim 192, 12 layers, 6 heads, 8 experts (top-2), 4 streams. Pretraining lr 3e-4, batch 32, 100 steps (repo ne bhi RL ke liye checkpoint 100 chuna tha), aur RL lr 5e-5. `--eval-per-family 8` se 24 confirm tasks milte hain, repo report jitne.

## Options

| Flag | Default | Matlab |
|---|---|---|
| `--preset` | `tiny` | `tiny` ya `full` |
| `--stages` | `pretrain,rl,eval` | Comma-separated: `pretrain`, `rl`, `eval`, `vision` |
| `--device` | `auto` | `auto` = cuda → mps (Mac GPU) → cpu. Ya seedha `cpu`, `cuda`, `mps` |
| `--pretrain-steps` | tiny 200, full 100 | Kitna pretraining. RL ke liye "kuch aata hai, sab nahi" chahiye (Topic 12) |
| `--rl-groups` | 48 | Kitne RL prompts |
| `--group-size` | 16 | Har prompt pe kitne attempts |
| `--rl-families` | `increment,double,even` | RL kin families pe ho |
| `--eval-per-family` | 4 | Confirm tasks per family. 8 = repo report jitna (RL families pe 24 tasks) |
| `--seed` | 42 | Init + pretraining seed |
| `--out` | `runs/capstone` | Receipt aur weights kahan save hon (`runs/` git me ignore hai) |

## Output

```
runs/capstone/receipt.json    ← config, params, RL stats, before/after eval, McNemar, vision, time
runs/capstone/model.pt        ← final weights
```

`receipt.json` hi tumhara **lab notebook** hai (Topic 10 ka "research habit"). Har experiment ke liye alag `--out` do, jaise `runs/exp-lr3e5-seed1`.

## Code me experiment kaise karein

Har idea ek chhota badlaav hai:
- **Ablation:** `Config(streams=1)`, `top_k=1`, ya `experts=4`
- **RL knob:** `rl(..., temperature=0.2)`, ya `lr=3e-5`
- **Reward:** `reward()` me `"invalid": 0.0` karke penalty hata do
- **Fix ko undo karo:** `HybridBlock.forward` me `return x + a + m, ...` likho (repo jaisa), aur compare karo

Fir **kai seeds** pe chalao (`--seed 1`, `2`, `3`...) aur receipts compare karo (Topic 11 ka `paired_sign_flip`).

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [02 · Teen fixes — course me jo mila, wo yahan theek hai](02-three-fixes.md) | 📚 [Topic 15 overview](README.md) | [04 · Results — hamara asli run, aur rasta me mile surprises](04-results-and-surprises.md) ➡️ |
<!-- /nav:bottom -->
