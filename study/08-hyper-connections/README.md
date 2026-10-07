<!-- nav:top -->
[🏠 Course](../README.md) › **Topic 08 / 15** › ▶️ [Pehli reading shuru karo](01-concept-residual-highway.md)
<!-- /nav:top -->

# Topic 08 — Hyper-connections: ek highway ki jagah 4 lanes

**Pichle topics se link:** Topic 03 me dekha tha ki har block `x = x + f(norm(x))` karta hai, yaani **residual connection**. Ye ek "highway" hai jisse information aur gradients seedhe aage-peeche ja sakte hain. GLM-5.3 (DeepSeek ke **mHC** idea se) is ek highway ko **4 lanes** (streams) me badal deta hai, aur har layer seekhti hai ki kis lane se padhna hai aur kis lane me likhna hai.

**Time:** ~40 min (padhai) + ~10 min (lab, optional 4 min training)

## Reading order

| File | Type | Kya milega |
|---|---|---|
| [01-concept-residual-highway](01-concept-residual-highway.md) | Concept | Residual connection kyun, aur ek lane kaafi kyun nahi |
| [02-definitions](02-definitions.md) | Definitions | Stream, read/mix, write/route, mHC, doubly stochastic, Sinkhorn |
| [03-practical-repo-code](03-practical-repo-code.md) | Practical | Repo ka `HyperConnection` line by line, aur ek quirk jo humne dhoondha |
| [04-mhc-and-real-life](04-mhc-and-real-life.md) | Practical + Real-life | "Manifold constraint" kyun, 1 vs 4 streams ka asli result, aur highway analogy |
| [05-lab-guide](05-lab-guide.md) | Code | [`lab_hyper_connections.py`](lab_hyper_connections.py) |
| [06-recap-quiz](06-recap-quiz.md) | Test | 8 sawaal |

## Pipeline me kahan hai?

```
embedding → [copy ×4 streams] → 12 × HyperConnection( mix → HybridBlock → route ) → mean of 4 → final_norm → output head
```

## Repo me kahan hai?

`sources/repo/glm53_flash/model.py`: class `HyperConnection` (lines 191–207), aur `forward_embeddings` me `expand(... streams ...)` aur `streams.mean(dim=2)`

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [06 · Recap + Quiz](../07-mixture-of-experts/06-recap-quiz.md) | 📚 [Topic 08 overview](README.md) | [01 · Concept — Residual highway, aur 4 lanes kyun](01-concept-residual-highway.md) ➡️ |
<!-- /nav:bottom -->
