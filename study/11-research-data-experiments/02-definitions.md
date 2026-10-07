<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 11 — Research skill: data experiments (diversity, order, curriculum)](README.md) › Reading 2 / 6
<!-- /nav:top -->

# 02 · Definitions — Experiment design ke shabd

| Term | Matlab | Repo ke experiment me |
|---|---|---|
| **Independent variable** | Jo cheez tum jaan-boojh ke badalte ho | diversity (8 vs 88), order, curriculum |
| **Controls** | Jo cheezein same rakhi jaati hain | model, init, optimizer, LR, batch, updates, eval set |
| **Metric** | Jo number measure hota hai | held-out **target-byte accuracy** |
| **Held-out set** | Data jo training me kabhi nahi aaya | 32 program structures (120 me se) |
| **Seed** | Random number generator ki starting value. Ye init aur data order tay karta hai | 10 seeds: 11, 22, ..., 110 |
| **Paired comparison** | Har seed pe dono conditions chalao aur **same seed** ke results ka fark lo | seed 11 blocked vs seed 11 interleaved |
| **Effect size** | Fark kitna bada hai | +9.7 percentage points |
| **p-value** | "Agar asal me koi fark na ho, to itna bada fark sirf luck se aane ka chance kitna hai?" | 0.00195 |
| **Statistically significant** | p chhota hai (aksar < 0.05), to luck wali explanation kamzor hai | |
| **Matched updates** | Har condition ko same number of optimizer steps | 200 updates |
| **Ablation** | Ek cheez hata ke dekhna ki uska kya role tha | Topic 03 (RMSNorm) |

## Data kaisa hai? (lab Exp 1)

Har example ek chhota program hai jisme 3 operations hain (add, sub, mul, neg, abs):
```
Task: start with x. Increase it by 5. Add 4. Make the result nonnegative.
Python: abs(((x + 5) + 4))
```

- **Structure** = operations ka sequence, jaise `('add', 'add', 'abs')`
- 5³ = 125 combos me se 5 hatao jisme saare ops same hain → **120 structures**
- **Train pool: 88**, aur **held-out: 32**. Held-out structures ka combination model ne kabhi nahi dekha.

Isse "**compositional generalization**" test hota hai: kya model naye combinations samajh sakta hai?

## Paired sign-flip permutation test (simple version)

10 seeds pe fark nikaalo: `diff = B − A`. Agar B aur A me asal me koi fark na hota, to har diff ka **sign** (+/−) random hota.

1. Saare 2¹⁰ = 1,024 sign-combinations try karo
2. Gino ki kitne combinations ka |sum| tumhare asli |sum| jitna ya usse bada hai
3. Wo fraction = **p-value**

**Exact hai, simple hai, koi assumption nahi.** Repo yahi use karta hai, aur lab me tum ise 10 lines me khud likhoge.

### ⚠️ Seeds kam hon to p chhota ho hi nahi sakta

Sabse extreme case: saare seeds ek hi direction me hain. Tab bhi:

| Seeds | Sabse chhota possible p |
|---:|---:|
| 3 | 0.25 |
| 5 | 0.0625 |
| 6 | 0.031 |
| 10 | 0.002 |

3 seeds pe **3/3 jeet** ke bhi p = 0.25 aata hai. Lab Exp 5 me ye khud dekhoge.

> Video (42:36): *"When people are reviewing your papers they will tell you to test on three seeds, and all three seeds should have a clear conclusion."*

Dono baatein sach hain: 3 seeds ek **minimum sanity check** hai, aur formal significance ke liye zyada seeds chahiye.

---
📁 `experiments/pretraining_data_diversity.py` (`all_structures`, `render_example`) · 🎬 Video 28:05–30:27

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [01 · Concept — Accha research sawaal kya hota hai?](01-concept-research-question.md) | 📚 [Topic 11 overview](README.md) | [03 · Practical — Repo ke 3 asli experiments](03-three-experiments.md) ➡️ |
<!-- /nav:bottom -->
