<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 04 — RoPE: model ko position kaise pata chalti hai](README.md) › Reading 1 / 6
<!-- /nav:top -->

# 01 · Concept — Attention "order-blind" hai

## Problem

Attention me har token baaki tokens se **dot product** karke score nikalta hai: "tum mere liye kitne relevant ho?" (Topic 05 me poora detail aayega.)

Lekin dot product sirf **vectors** dekhta hai, unki **position** nahi. To:

```
"x - 1"   aur   "1 - x"
```

dono me same 3 tokens hain (`x`, `-`, `1`). Agar position ki koi info nahi hai, to attention ke liye dono **ek jaise** hain. Lekin Python me inka jawab bilkul alag hai!

> Video: *"In attention mechanism you have tokens multiplied by other tokens but you don't know the order of tokens in the prompt."*

Lab Exp 5 me ye prove hota hai: tokens shuffle karo aur bina RoPE ke output **exactly same** aata hai.

## Purane solutions

| Tarika | Idea | Problem |
|---|---|---|
| **Learned absolute** (GPT-2) | Har position (0, 1, 2...) ka ek seekha hua vector, embedding me jod do | Training se lambe context pe fail, kyunki position 5000 kabhi dekhi hi nahi |
| **Sinusoidal** (2017 Transformer) | Sin/cos waves ka fixed pattern jodo | Kaam karta hai, lekin "doori" ko directly encode nahi karta |
| **RoPE** (2021, aaj ka standard) | Vector ko position ke hisaab se **ghumao (rotate)** | — |

## RoPE ka idea, ek line me

> **Har token ke query aur key vector ko uski position ke hisaab se thoda ghuma do. Position 0 pe 0°, position 1 pe θ, position 2 pe 2θ...**

Jab do ghume hue vectors ka dot product lete hain, to result unke **angle ke fark** pe depend karta hai, yaani unki **doori** pe.

## Kya ghumaya jaata hai, kya nahi?

- ✅ **Query (q)** aur **Key (k)** ghumaye jaate hain, kyunki score inse banta hai
- ❌ **Value (v)** nahi ghumaya jaata, kyunki value "kya information le jaani hai" hai, position ka score nahi
- ❌ Embedding pe kuch **joda nahi** jaata (GPT-2 se fark yahi hai)

Repo me:
```python
q, k = apply_rope(q, k)     # sirf q aur k
```

## Kyun "rotate", kuch aur kyun nahi?

Rotation ki 2 khoobiyan hain:
1. **Length nahi badalti.** Vector ka size same rehta hai, sirf direction ghoomti hai, to RMSNorm wala kaam kharab nahi hota.
2. **Angle ghatana aasaan hai.** `rotate(5θ)` aur `rotate(3θ)` ka "fark" hamesha `2θ` hai, chahe 5 aur 3 ho ya 105 aur 103.

---
🎬 **Video:** 15:10–15:55 · 📊 Slide 30 "RoPE writes position into queries and keys"

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [Topic 04 — RoPE: model ko position kaise pata chalti hai](README.md) | 📚 [Topic 04 overview](README.md) | [02 · Definitions — Rotation, pairs, frequency](02-definitions-rotation.md) ➡️ |
<!-- /nav:bottom -->
