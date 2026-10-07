<!-- nav:top -->
[🏠 Course](../README.md) › **Topic 05 / 07** › ▶️ [Pehli reading shuru karo](01-concept-attention.md)
<!-- /nav:top -->

# Topic 05 — Attention basics → Linear attention

**Pichle topics se link:** Ab har token ka vector hai (Topic 02), normalized hai (Topic 03), aur q/k me position likhi hai (Topic 04). Ab aata hai transformer ka dil: **attention**, yaani tokens ek-doosre se information kaise lete hain. Fir dekhenge GLM-5.3 ka sasta version: **linear attention**, jo 12 me se 9 layers me hai.

**Time:** ~55 min (padhai) + ~25 min (lab). Ye sabse important topics me se ek hai, jaldi mat karna.

## Reading order

| File | Type | Kya milega |
|---|---|---|
| [01-concept-attention](01-concept-attention.md) | Concept | Attention = "kisse kitna sunna hai", Q/K/V library analogy ke saath |
| [02-definitions-and-cost](02-definitions-and-cost.md) | Definitions | Q, K, V, heads, causal mask, aur **T²** problem |
| [03-linear-attention](03-linear-attention.md) | Practical | Brackets badal ke T² ko hatao: running memory **S** |
| [04-tradeoff-real-life](04-tradeoff-real-life.md) | Practical + Real-life | Compressed memory ki keemat, decay/KDA, aur diary analogy |
| [05-lab-guide](05-lab-guide.md) | Code | [`lab_linear_attention.py`](lab_linear_attention.py): recall test, parallel = recurrent |
| [06-recap-quiz](06-recap-quiz.md) | Test | 8 sawaal |

## Pipeline me kahan hai?

```
block (× 12):  RMSNorm → **ATTENTION** (9× linear, 3× sparse) → +  →  RMSNorm → MoE → +
```

Sparse attention aur 3:1 rhythm Topic 06 me aayenge.

## Repo me kahan hai?

`sources/repo/glm53_flash/model.py`: class `LinearAttention` (lines 62–86)

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [06 · Recap + Quiz](../04-rope-position/06-recap-quiz.md) | 📚 [Topic 05 overview](README.md) | [01 · Concept — Attention = "kisse kitna sunna hai"](01-concept-attention.md) ➡️ |
<!-- /nav:bottom -->
