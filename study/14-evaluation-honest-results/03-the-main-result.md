<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 14 — Evaluation: sahi naapna, imaandaari se bolna](README.md) › Reading 3 / 6
<!-- /nav:top -->

# 03 · Practical — Main result: 0/24 → 16/24

## Numbers (lab Exp 1–3, repo receipts se khud nikaale)

**Primary metric:** greedy pass@1, 3 RL families, 24 confirm tasks

| Family | Before RL | After RL |
|---|---:|---:|
| increment | 0/8 | **8/8** |
| double | 0/8 | **8/8** |
| even | 0/8 | 0/8 |
| **Total** | **0/24** | **16/24** |

- Paired: **16 gains, 0 losses** → McNemar exact **p = 0.0000305**
- Greedy hidden tests: 2/72 → 48/72

**Secondary:** sampled (temperature 0.35, 8 samples/task), sab 8 families, 64 tasks

| | Before | After |
|---|---:|---:|
| pass@1 (sampled) | 24.6% | 35.4% |
| pass@8 | 39.1% | **53.1%** |

## Exact behavior (REPORT)

Unseen prompt `# Return two times x.  def double_ywkaoot(x):`
- **Before:** 8/8 samples galat, pehla tha `return x * * 0 0`
- **After:** 8/8 samples `return x * 2` ✅

## Kya claim kar sakte hain?

Slide 61: *"The gain is statistically clear on this frozen synthetic benchmark. It does not prove broad coding improvement."*

| ✅ Claim kar sakte ho | ❌ Claim nahi kar sakte |
|---|---|
| Executable reward RL ne `increment` aur `double` ke **naye function naam** pe greedy accuracy 0 → 100% kar di | "Model ne coding seekh li" |
| Ye luck nahi lagta (p = 0.00003, sab 16 badlaav ek hi direction me) | "RL hamesha kaam karta hai" (1 training seed, 1 confirm seed) |
| RL ne pretraining me chhupe sahi jawab ki probability badhayi | "RL ne naya concept sikhaya" (saari families pretraining me thi) |
| `even` pe koi greedy sudhaar nahi hua | `even` kyun fail hua (ye measure nahi hua) |

REPORT ke shabd: *"The experiment establishes narrow within-family policy improvement — not general coding capability and not a reproduction of GLM-5.3-Flash."*

## `even` ka raaz 🤔

> Video (39:40): *"Interestingly it didn't improve on this one. I don't know why. I need to maybe check it. Maybe it's a bug in my code, or bug that AI generated, or bug in my experiment... or if it's not a bug, then it's even more interesting. But it's probably a bug."*

Ek accha researcher yahi karta hai: unexpected result ko **chhupata nahi**, use agla sawaal banata hai. Kuch hypotheses jo tum test kar sakte ho:
- `x % 2 == 0` ek `bool` return karta hai, aur verifier type strict hai (`True` ≠ `1`)
- Pretraining checkpoint 100 pe `even` ka latent solution tha hi nahi (before: 3/64 sampled)
- 3 families ek saath train hui. Kya increment/double ne gradient "kheench" liya?

---
📄 `REPORT.md` → Confirmation results · 📊 Slides 60–62 · 🎬 Video 38:00–40:00

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [02 · Definitions — Evaluation ke shabd](02-definitions.md) | 📚 [Topic 14 overview](README.md) | [04 · Interference, replication + Real-life](04-interference-replication-real-life.md) ➡️ |
<!-- /nav:bottom -->
