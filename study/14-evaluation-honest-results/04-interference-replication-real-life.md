<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 14 — Evaluation: sahi naapna, imaandaari se bolna](README.md) › Reading 4 / 6
<!-- /nav:top -->

# 04 · Interference, replication + Real-life

## 1. Jo bigad gaya: interference

Lab Exp 4, sampled exact (8 tasks × 8 samples per family):

| Family | RL me train hua? | Before | After | |
|---|:---:|---:|---:|:---:|
| increment | ✅ | 6/64 | **40/64** | ↑ |
| double | ✅ | 4/64 | **45/64** | ↑ |
| even | ✅ | 3/64 | 3/64 | — |
| **square** | ❌ | **52/64** | 37/64 | ↓ |
| **list_sum** | ❌ | **61/64** | 56/64 | ↓ |
| absolute, nonnegative, reverse | ❌ | 0/64 | 0/64 | — |

Do families jo **pehle se achhi** thi, wo RL ke baad **giri**. Kyun?
- Sirf last block + head train hua aur koi KL penalty nahi thi. Head ki probabilities trained tasks ke hisaab se khisak gayi.
- `square` (`x * x`) aur `double` (`x * 2`) bahut milte-julte hain. "x ke baad `* 2` likho" ka dhakka `* x` ko nuksaan pahuncha sakta hai.

> Video (40:07): *"Two previously strong families regressed because only a narrow parameter surface was optimized for the practice reward distribution."*

Aur imaandaari se: *"Depending on how we calculated the statistical significance, you need to always be careful. Did it actually regress? Do you have enough samples?"* `list_sum` ka 61 → 56 shayad noise bhi ho sakta hai.

> Video (39:33): *"People complain that LLMs only learn what is in training data, and then the other guy says: then we'll put everything into training data."* Isliye bade labs har tarah ke tasks pe RL karte hain.

## 2. Jo replicate nahi hua: "winner" ka bhram

**Screen (1 seed, dev 20 tasks):** 8 RL variants try kiye, aur **ek-ek variable** badla.

| Variant | Dev solved /20 |
|---|---:|
| binary / partial / no penalty / hard penalty | 5 / 5 / 5 / 5 |
| temperature 0.20 / 0.80 | 7 / 6 |
| **group size 4** / 16 | **8** / 6 |

> Video (41:19): *"If I set for example group size four, it performs very well, better than group size 16."*

**Confirm (3 fresh seeds, 40 untouched tasks, group 4 vs default group 8):**

| Seed | Group 8 | Group 4 | Fark |
|---:|---:|---:|---:|
| 31415 | 12/40 | 13/40 | +1 |
| 27182 | 14/40 | 13/40 | −1 |
| 16180 | 11/40 | 8/40 | **−3** |
| **Mean** | **12.3** | **11.3** | group 4 **haara** |

> Video (41:52): *"Check out this horror. You see group size four won over group size eight on this seed, but lost on this seed and lost on this seed."*

> Slide 74: *"A dev win is not a discovery."* · *"None of the four RL changes produced a statistically significant improvement."*

**Lesson:** Ek screen candidates ki ranking de sakta hai, **winner tay nahi kar sakta**. Har "winner" ko fresh seeds pe confirm karo.

> Video (42:36): *"When people are reviewing your papers they will tell you to test on three seeds, and all three seeds should have a clear conclusion."*

---

## Real-life analogy: Cricket team selection 🏏

- **Train** = nets practice
- **Dev** = practice matches. Inke basis pe team chuno (checkpoint selection)
- **Confirm** = World Cup. Ek hi mauka, baar-baar "retry" nahi
- **Screen ka winner** = ek player ne ek practice match me century maari. Kya wo sach me best hai? **3 aur matches** khilao (replication). Shayad agle 3 me 12, 0, 8 bane!
- **Interference** = batsman ko sirf short ball pe train kiya. Short ball pe sudhar gaya, lekin spin pe jo pehle accha tha, wo bigad gaya.
- **pass@k** = "6 gend me ek bhi chhakka?" vs **pass@1** = "pehli gend pe chhakka?" Dono alag skills naapte hain.

---
📊 Slides 70–74 · 🎬 Video 39:35–43:00

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [03 · Practical — Main result: 0/24 → 16/24](03-the-main-result.md) | 📚 [Topic 14 overview](README.md) | [05 · Code Lab — `lab_evaluation.py`](05-lab-guide.md) ➡️ |
<!-- /nav:bottom -->
