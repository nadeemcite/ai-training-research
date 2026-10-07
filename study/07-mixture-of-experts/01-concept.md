<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 07 — Mixture of Experts (MoE)](README.md) › Reading 1 / 6
<!-- /nav:top -->

# 01 · Concept — Ek bada dimaag vs bahut saare specialists

## Normal transformer: Dense FFN

Har block me attention ke baad ek FFN hota hai: do badi matrices, beech me ek non-linearity.
```
x → [up: 192 → 768] → activation → [down: 768 → 192] → output
```
**Har token** is poore FFN se guzarta hai, isliye ise **dense** kehte hain. Model bada karna hai to FFN bada karo, aur **har token ka compute bhi badhega**.

## Problem

- Zyada knowledge ke liye zyada parameters chahiye
- Dense model me zyada params = har token pe zyada compute = slow aur mehenga

Kya aisa ho sakta hai ki **params bahut zyada** hon lekin **har token pe compute kam**?

## MoE ka idea

> **Ek bade FFN ki jagah bahut saare chhote FFN ("experts") rakho. Ek chhota "router" har token ke liye decide karta hai ki kaunse 2 experts use karne hain. Baaki experts us token ke liye so jaate hain.**

```
          ┌─ E1
          ├─ E2 ✓ (0.57)
token → router ─┼─ E3 ✓ (0.43)       →  0.57·E2(x) + 0.43·E3(x) + shared(x)
          ├─ ...
          └─ E8
          + shared expert (hamesha)
```

Slide 37: *"Each token chooses experts. Two routed experts + one shared expert."*

## Numbers (video + slides)

| | Released GLM-5.3 | Hamara model |
|---|---|---|
| Routed experts | 288 | 8 |
| Har token kitne chunta hai (top-k) | 8 | 2 |
| Shared expert | 1 | 1 |
| Total params | ~320B | 25.7M |

> Video: *"In GLM you have 288 experts and ... each token will pass through 8 out of 288 and there is one shared expert."*

Released model me har token sirf ~3% experts use karta hai (lab Exp 3). Isliye 320B ka model kuch billion params jitna "sasta" chalta hai.

## Shared expert kyun?

Kuch knowledge **sab tokens** ko chahiye, jaise basic grammar, common patterns, ya "ye Python code hai". Agar har routed expert ye sab khud seekhe, to 8 jagah duplicate ho jaata hai.

> Video: *"Every token passes through the shared expert and that expert will learn some common information for every token. So other experts don't need to waste capacity on that."*

Shared = common knowledge, aur routed = specialization.

## Kya experts sach me "specialist" bante hain?

Naam se lagta hai ki ek expert "maths" ka hoga aur ek "Hindi" ka. Asliyat me specialization aksar **surface-level** hoti hai, jaise punctuation, numbers, ya kisi khaas syntax ke tokens, aur insaan ke liye hamesha samajhne layak nahi hoti. Ye ek open interpretability research question hai.

---
🎬 **Video:** 20:42–21:30 · 📊 Slide 37 "Each token chooses experts"

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [Topic 07 — Mixture of Experts (MoE)](README.md) | 📚 [Topic 07 overview](README.md) | [02 · Definitions — Expert, router, top-k, gate](02-definitions.md) ➡️ |
<!-- /nav:bottom -->
