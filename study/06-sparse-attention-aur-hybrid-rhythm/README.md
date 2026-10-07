<!-- nav:top -->
[🏠 Course](../README.md) › **Topic 06 / 14** › ▶️ [Pehli reading shuru karo](01-concept-sparse.md)
<!-- /nav:top -->

# Topic 06 — Sparse attention + 3:1 hybrid rhythm

**Pichle topic se link:** Topic 05 me dekha ki linear attention sasta hai, lekin exact purani cheezein bhool jaata hai (lossy memory). Softmax attention sab yaad rakhta hai, lekin T² mehenga hai. **Sparse attention** beech ka raasta hai: softmax hi lagao, lekin sirf **kuch chune hue tokens** pe. Aur GLM in dono ko ek **rhythm** me mix karta hai.

**Time:** ~45 min (padhai) + ~20 min (lab)

## Reading order

| File | Type | Kya milega |
|---|---|---|
| [01-concept-sparse](01-concept-sparse.md) | Concept | "Sab mat dekho, sahi cheezein dekho" |
| [02-definitions-window-anchor-indexer](02-definitions-window-anchor-indexer.md) | Definitions | Local window, anchors, stride, indexer, top-k |
| [03-practical-cost-and-indexer](03-practical-cost-and-indexer.md) | Practical | Kitna sasta hai? Fixed pattern vs indexer |
| [04-hybrid-rhythm-real-life](04-hybrid-rhythm-real-life.md) | Practical + Real-life | 3 linear + 1 sparse kyun, aur kitaab padhne wali analogy |
| [05-lab-guide](05-lab-guide.md) | Code | [`lab_sparse_attention.py`](lab_sparse_attention.py): needle dhoondho |
| [06-recap-quiz](06-recap-quiz.md) | Test | 8 sawaal |

## Pipeline me kahan hai?

```
Layer:  1  2  3  4  5  6  7  8  9  10 11 12
        L  L  L  S  L  L  L  S  L  L  L  S       (L = linear, S = sparse)
```

## Repo me kahan hai?

- `sources/repo/glm53_flash/model.py`: class `SparseAttention` (lines 89–131)
- Rhythm: `GLM53FlashFromScratch.__init__` → `sparse=((index + 1) % 4 == 0)`
- Config: `sparse_window = 32`, `sparse_stride = 32`

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [06 · Recap + Quiz](../05-attention-aur-linear-attention/06-recap-quiz.md) | 📚 [Topic 06 overview](README.md) | [01 · Concept — "Sab mat dekho, sahi cheezein dekho"](01-concept-sparse.md) ➡️ |
<!-- /nav:bottom -->
