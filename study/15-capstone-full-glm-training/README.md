<!-- nav:top -->
[🏠 Course](../README.md) › **Topic 15 / 15** › ▶️ [Pehli reading shuru karo](01-code-map.md)
<!-- /nav:top -->

# Topic 15 — Capstone: poora GLM-5.3-Flash ek file me 🎓

**Pichle saare topics se link:** Topic 01–14 me ek-ek tukda seekha: tokenizer, embeddings, RMSNorm, RoPE, linear/sparse attention, MoE, hyper-connections, vision, pretraining, data experiments, RL, RLOO aur evaluation. Ab sab kuch **ek single file** [`glm53_full.py`](glm53_full.py) me jodte hain, jo random weights se shuru karke pretraining, RL, evaluation aur vision tak poora chalti hai.

Aur bonus: course me jo **3 issues** mile the, wo yahan **fixed** hain.

**Time:** ~40 min (padhai) + ~5 min (run, CPU)

## Reading order

| File | Type | Kya milega |
|---|---|---|
| [01-code-map](01-code-map.md) | Concept | File ka har section kis chapter se aaya |
| [02-three-fixes](02-three-fixes.md) | Practical | 3 fixes: balance gradient, identity once, random hidden tests |
| [03-run-it](03-run-it.md) | Practical | Kaise chalayein (tiny CPU / full GPU), stages, receipt |
| [04-results-and-surprises](04-results-and-surprises.md) | Results | Hamara asli run: kya chala, kya bigda, aur kyun |
| [05-research-roadmap](05-research-roadmap.md) | Next steps | Ab kya karein: 10 research sawaal jo tum CPU pe kar sakte ho |
| [06-final-recap](06-final-recap.md) | Recap | Poore course ka summary + final quiz |

## Ek command

```bash
uv run study/15-capstone-full-glm-training/glm53_full.py --stages pretrain,rl,eval,vision
```

~5 min CPU pe, aur `runs/capstone/receipt.json` me poora record milta hai.

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [06 · Recap + Quiz](../14-evaluation-honest-results/06-recap-quiz.md) | 📚 [Topic 15 overview](README.md) | [01 · Code map — har section kis chapter se](01-code-map.md) ➡️ |
<!-- /nav:bottom -->
