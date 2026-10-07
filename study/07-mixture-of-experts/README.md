<!-- nav:top -->
[🏠 Course](../README.md) › **Topic 07 / 15** › ▶️ [Pehli reading shuru karo](01-concept.md)
<!-- /nav:top -->

# Topic 07 — Mixture of Experts (MoE)

**Pichle topics se link:** Attention (Topic 05–06) tokens ke **beech** information move karta hai. Lekin har token ko information milne ke baad us pe "sochna" bhi padta hai, yaani apne vector ko transform karna. Ye kaam **feed-forward network (FFN)** karta hai. GLM-5.3 me ye FFN ek **Mixture of Experts** hai: bahut saare chhote FFN "specialists", jinme se har token sirf kuch chunta hai.

> Slide: *"Attention reads tokens. MoE transforms them."*

**Time:** ~50 min (padhai) + ~25 min (lab)

## Reading order

| File | Type | Kya milega |
|---|---|---|
| [01-concept](01-concept.md) | Concept | Ek bada dimaag vs bahut saare specialists |
| [02-definitions](02-definitions.md) | Definitions | Expert, router, top-k, gate weights, shared expert, usage |
| [03-practical-code-and-params](03-practical-code-and-params.md) | Practical | Repo code line-by-line, aur total vs active params |
| [04-load-balancing-real-life](04-load-balancing-real-life.md) | Practical + Real-life | Expert collapse, balance loss, **repo me mila ek bug**, hospital analogy |
| [05-lab-guide](05-lab-guide.md) | Code | [`lab_moe.py`](lab_moe.py): router, params, aur collapse khud dekho |
| [06-recap-quiz](06-recap-quiz.md) | Test | 8 sawaal |

## Pipeline me kahan hai?

```
block (× 12):  RMSNorm → attention → +  →  RMSNorm → **MoE** → +
```

## Repo me kahan hai?

- `sources/repo/glm53_flash/model.py`: classes `Expert` (lines 134–142), `SparseMoE` (145–174), `HybridBlock` (177–188)
- `sources/repo/scripts/train_pretrain.py` line 94: balance loss

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [06 · Recap + Quiz](../06-sparse-attention-aur-hybrid-rhythm/06-recap-quiz.md) | 📚 [Topic 07 overview](README.md) | [01 · Concept — Ek bada dimaag vs bahut saare specialists](01-concept.md) ➡️ |
<!-- /nav:bottom -->
