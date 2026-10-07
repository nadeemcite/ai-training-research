<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 13 — RLOO: advantage se update tak, aur sirf last block train karna](README.md) › Reading 1 / 6
<!-- /nav:top -->

# 01 · Concept — "Apne bhai-behno se behtar tha ya nahi?"

## Naive idea (aur uski problem)

"Jis attempt ko +1 mila, use zyada likely karo. Jise −0.1 mila, use kam likely."

Problem: Agar ek aasaan prompt pe **saare 16 attempts** +1 lein, to model har baar "aur zyada" push hota hai, jabki kuch naya seekhne ko nahi tha. Aur mushkil prompt pe sab 0 hon, to signal kuch nahi bataata. Raw reward se updates bahut **noisy** hote hain.

## Behtar idea: tulna karo (advantage)

> **Ek attempt ko uske group ke baaki attempts se compare karo. Average se behtar tha to badhao, bura tha to ghatao.**

> Video (36:59): *"We want to calculate how much each of the answers is better or worse than other answers, than the average. So they call this advantage. Reward minus mean of other rewards."*

```
advantage_i = reward_i − mean(baaki sab ke rewards)
```

Lab Exp 1 (4 attempts):

| Attempt | Reward | Baaki ka mean | Advantage |
|---:|---:|---:|---:|
| 0 | +1.0 | +0.300 | **+0.700** ⬆️ |
| 1 | 0.0 | +0.633 | **−0.633** ⬇️ |
| 2 | −0.1 | +0.667 | **−0.767** ⬇️ |
| 3 | +1.0 | +0.300 | **+0.700** ⬆️ |

Advantages ka sum **0** hai: kuch upar, kuch neeche. Model ko sirf **relative** signal milta hai.

## Sab barabar? To koi update nahi

Agar saare attempts +1 hain (ya saare −0.1), to har advantage **0** hai, aur kuch nahi badalta. Ye sahi bhi hai: tulna karne ko kuch tha hi nahi. Repo aise groups ko skip hi kar deta hai (Topic 12: 96 me se 23 groups).

## Iska bada fayda: koi "critic" nahi chahiye

Purane RL (PPO) me ek **alag model (critic)** train hota tha jo guess karta tha ki "is prompt pe average reward kitna hona chahiye". Ye mehenga hai aur khud galat ho sakta hai.

Yahan baseline **free** hai: bas group ke baaki attempts ka average.

> Video: *"This is good because you don't need separate critic, like separate model, to review the results and score the results. You don't need humans to do it. You can just let it generate multiple times and compare them to each other."*

## Naam: RLOO, GRPO

- **RLOO** (REINFORCE Leave-One-Out): baseline = **baaki** attempts ka mean (khud ko chhod ke). Repo yahi use karta hai.
- **GRPO** (Group Relative Policy Optimization, DeepSeek): baseline = poore group ka mean, aur fir **std se divide**. Video me mention hai.

Dono ka core idea same hai: group ke andar tulna. Lab Exp 3 me dono asli data pe compare karoge.

---
🎬 **Video:** 36:44–37:37 · 📊 Slides 65–66 "Compare each attempt with the others"

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [Topic 13 — RLOO: advantage se update tak, aur sirf last block train karna](README.md) | 📚 [Topic 13 overview](README.md) | [02 · Definitions — Advantage, log-prob, policy gradient](02-definitions.md) ➡️ |
<!-- /nav:bottom -->
