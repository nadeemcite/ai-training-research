<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 15 — Capstone: poora GLM-5.3-Flash ek file me 🎓](README.md) › Reading 3 / 6
<!-- /nav:top -->

# 03 · Kaise chalayein

## Tiny (CPU, ~5 min) — default

```bash
uv run study/15-capstone-full-glm-training/glm53_full.py --stages pretrain,rl,eval,vision
```

| Stage | Kya hota hai | Time (Mac CPU) |
|---|---|---:|
| `pretrain` | 2.2M model, 200 steps, batch 16, AdamW lr 1e-3 | ~50 s |
| `rl` | 48 groups × 16 rollouts, families increment/double/even, last block + head, RLOO | ~85 s |
| `eval` | Confirm split (32 tasks): greedy + 8 samples, **before aur after** dono, McNemar | ~115 s |
| `vision` | Alag chhota LM + vision encoder, 120 steps, 200 held-out digits | ~4 s |

## Full (25.7M, GPU)

```bash
uv run study/15-capstone-full-glm-training/glm53_full.py --preset full --device cuda --pretrain-steps 100
```

Repo jaisa model hai: dim 192, 12 layers, 6 heads, 8 experts (top-2), 4 streams. Pretraining lr 3e-4, batch 32, aur RL lr 5e-5. Mac GPU ke liye `--device mps`. CPU pe bhi chalega, lekin pretraining ~4.5 sec/step hai (Topic 10).

*(Full preset maine sirf smoke-test kiya hai: model banta hai aur forward pass chalta hai, 25,731,168 params. Poora full run GPU pe nahi chalaya.)*

## Options

| Flag | Default | Matlab |
|---|---|---|
| `--preset` | `tiny` | `tiny` ya `full` |
| `--stages` | `pretrain,rl,eval` | Comma-separated: `pretrain`, `rl`, `eval`, `vision` |
| `--device` | `cpu` | `cpu`, `cuda`, `mps` |
| `--pretrain-steps` | tiny 200, full 100 | Kitna pretraining. RL ke liye "kuch aata hai, sab nahi" chahiye (Topic 12) |
| `--rl-groups` | 48 | Kitne RL prompts |
| `--group-size` | 16 | Har prompt pe kitne attempts |
| `--rl-families` | `increment,double,even` | RL kin families pe ho |
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
