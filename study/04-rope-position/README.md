<!-- nav:top -->
[🏠 Course](../README.md) › **Topic 04 / 14** › ▶️ [Pehli reading shuru karo](01-concept-order-problem.md)
<!-- /nav:top -->

# Topic 04 — RoPE: model ko position kaise pata chalti hai

**Pichle topic se link:** Vectors ab normalized hain (Topic 03). Lekin ek badi problem bachi hai: attention ko pata hi nahi ki kaunsa token pehle aaya aur kaunsa baad me. `x - 1` aur `1 - x` uske liye same hain! RoPE ye problem solve karta hai.

**Time:** ~45 min (padhai) + ~20 min (lab)

## Reading order

| File | Type | Kya milega |
|---|---|---|
| [01-concept-order-problem](01-concept-order-problem.md) | Concept | Attention "order-blind" kyun hai |
| [02-definitions-rotation](02-definitions-rotation.md) | Definitions | Rotation, pairs, frequency, angle (2D se shuru) |
| [03-practical-relative-position](03-practical-relative-position.md) | Practical | RoPE ka jaadu: score sirf *doori* pe depend karta hai |
| [04-glm-nope-and-real-life](04-glm-nope-and-real-life.md) | Practical + Real-life | Released GLM me NoPE, aur clock ki suiyon wali analogy |
| [05-lab-guide](05-lab-guide.md) | Code | [`lab_rope.py`](lab_rope.py): rotation, doori, aur shuffle test |
| [06-recap-quiz](06-recap-quiz.md) | Test | 8 sawaal |

## Pre-requisite: dot product (1 minute me)

```
a · b = a₁b₁ + a₂b₂ + ... + a_d·b_d
```
- Dono vectors same direction me hain → **bada positive**
- Perpendicular (90°) → **0**
- Opposite → **negative**

Attention me ye "query aur key kitna match karte hain" ka score hai. (Detail Topic 05 me.)

## Repo me kahan hai?

`sources/repo/glm53_flash/model.py`: function `apply_rope` (lines 44–59). Ise `LinearAttention` aur `SparseAttention` dono call karte hain.

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [06 · Recap + Quiz](../03-rmsnorm/06-recap-quiz.md) | 📚 [Topic 04 overview](README.md) | [01 · Concept — Attention "order-blind" hai](01-concept-order-problem.md) ➡️ |
<!-- /nav:bottom -->
