<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 14 — Evaluation: sahi naapna, imaandaari se bolna](README.md) › Reading 1 / 6
<!-- /nav:top -->

# 01 · Concept — Train, Dev, Confirm: teen alag kamre

## Problem: apne aap ko dhokha dena

Agar tum ek hi test set pe baar-baar check karo ("lr badla, check kiya, temperature badla, check kiya..."), to aakhir me jo setting "jeetegi" wo **us test set pe overfit** hogi, chahe model asal me behtar na ho. Ise **test set leakage** ya "garden of forking paths" kehte hain.

## Solution: teen splits

```
TRAIN  ──────►  DEV  ──────────────►  CONFIRM 🔒
seekhna         faisle lena            sirf EK baar, aakhir me
                (checkpoint, LR,        "kya ye sach hai?"
                 kab rukna)
```

Slide 69: *"We inspect confirmation only after choosing the checkpoint. Repeatedly checking would turn it into a development set."*

Repo me har split ka **alag seed** hai (Topic 12), isliye function naam alag hain:

| Split | Seed | Kaam |
|---|---:|---|
| `rl` | 3907 | RL training prompts |
| `dev` | 1701 | Checkpoint 96 chuna (curve monotonic tha) |
| `final` | 2909 | Pehle ka held-out, jo pilots ke dauraan use hua |
| `confirm` | 8123 | **Naya**, sirf final claim ke liye |

`final` split pilots me baar-baar dekha gaya tha, isliye repo ne ek **fresh `confirm`** split banaya. Ye ek mature research decision hai.

## "Unseen" ka sahi matlab

Confirm tasks me **function naam naye** hain, lekin:
- Operation families wahi 8 hain
- Descriptions 2 templates me se hain
- **3 test cases har family me same** hain

> Video (33:27): *"In this case we are testing it on similar tasks that it learned during training. It's not same but similar."*

To ye **"within-distribution identity generalization"** hai (REPORT ke shabd): naye naam, purane patterns. Ye "naya algorithm likhna" nahi hai.

## Kya measure karein?

Ek hi number kaafi nahi hota. Repo ne pehle se tay kiya (**prespecified**):
- **Primary:** greedy pass@1 on 3 RL families (24 confirm tasks)
- **Secondary:** sampled exact rate aur pass@8 (temperature 0.35)
- **Sab 8 families** pe bhi, taaki "kya bigda?" dikhe

> **Research habit:** Metric experiment se **pehle** likho. Baad me "jo accha dikhe wo metric chuno" = khud ko dhokha.

---
🎬 **Video:** 32:51–33:50, 38:00–40:00 · 📊 Slide 69 "Open the confirmation set once"

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [Topic 14 — Evaluation: sahi naapna, imaandaari se bolna](README.md) | 📚 [Topic 14 overview](README.md) | [02 · Definitions — Evaluation ke shabd](02-definitions.md) ➡️ |
<!-- /nav:bottom -->
