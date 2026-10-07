<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 08 — Hyper-connections: ek highway ki jagah 4 lanes](README.md) › Reading 1 / 6
<!-- /nav:top -->

# 01 · Concept — Residual highway, aur 4 lanes kyun

## Residual connection: yaad karo

Bina residual ke har layer input ko **poora badal** deti hai: `x = f(x)`. 12 layers ke baad original information lagbhag gaayab ho jaati hai.

Residual ke saath har layer sirf ek **badlaav jodti** hai: `x = x + f(x)`. Original information ek "highway" pe aage chalti rehti hai.

Lab Exp 1 (12 random chhoti layers):

| | 12 layers ke baad input se similarity |
|---|---:|
| Bina residual | **−0.05** (kuch nahi bacha) |
| Residual ke saath | **+0.64** (original abhi bhi wahan hai) |

Ye 2015 ka **ResNet** idea hai, aur aaj har transformer isi pe khada hai. Gradients bhi isi highway se seedhe neeche pahunchte hain, isliye 100+ layer models train ho paate hain.

## Problem: ek lane me sab kuch

Ek hi residual stream (192 numbers) pe **har** layer padhti bhi hai aur likhti bhi hai. Attention apni info likhta hai, MoE apni, aur sab ek hi jagah jud jaata hai. Ek lane pe saari traffic.

## Hyper-connections ka idea

> **Residual stream ki n copies (lanes) banao. Har layer seekhti hai: (1) kin lanes ka mix padhna hai, aur (2) apna update kin lanes me kitna likhna hai.**

> Video (11:56): *"Each of them is going to carry different information forward without that information being processed through the attention... It's like some highways where you pass four different types of information."*

```
           lane 1 ─────┬────────────────────(+ 0.23 × update)───── lane 1
           lane 2 ─────┤ read mix           (+ 0.24 × update)───── lane 2
           lane 3 ─────┤ ─→ [block] ─→ update (+ 0.26 × update)── lane 3
           lane 4 ─────┘                    (+ 0.28 × update)───── lane 4
```

End me 4 lanes ka **average** lekar output head ko diya jaata hai.

## Ye kahan se aaya?

- **Hyper-Connections** (ByteDance, 2024): residual ko n streams me badla, aur mixing learnable bana di
- **mHC: Manifold-Constrained Hyper-Connections** (DeepSeek, 2025): mixing matrices pe ek **constraint** lagaya taaki deep models me signal explode na ho (Reading 04)
- **GLM-5.3** mHC use karta hai

> Video: *"These are manifold constrained hyperconnections by DeepSeek and ByteDance."*

## Honest note

Video khud kehta hai: *"I will not go into too much detail here... you can read paper... you need to practice this yourself."* Ye topic architecture ka sabse naya aur sabse kam "settled" hissa hai. Hamara lab bhi dikhata hai ki chhote model pe 4 streams ka koi saaf fayda nahi mila (Reading 04).

---
🎬 **Video:** 11:56–13:27, 21:30–22:28 · 📊 Slide 38 "Four streams continue between attention and MoE"

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [Topic 08 — Hyper-connections: ek highway ki jagah 4 lanes](README.md) | 📚 [Topic 08 overview](README.md) | [02 · Definitions — Streams, mix, route, mHC](02-definitions.md) ➡️ |
<!-- /nav:bottom -->
