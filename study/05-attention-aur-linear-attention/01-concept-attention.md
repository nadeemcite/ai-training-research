<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 05 — Attention basics → Linear attention](README.md) › Reading 1 / 6
<!-- /nav:top -->

# 01 · Concept — Attention = "kisse kitna sunna hai"

## Problem

Embedding ke baad har token ka vector **akela** hai. `return x + 1` me `1` ke vector ko nahi pata ki uske pehle `+` hai, ya ki function ka naam `increment` tha.

Agla token sahi predict karne ke liye har token ko **context** chahiye, yaani pichle tokens ki information.

## Attention ka idea

> **Har token pichle saare tokens se poochta hai "tum mere liye kitne relevant ho?", aur relevant tokens ki information zyada leta hai.**

## Analogy: Library me kitaab dhoondhna 📚

Tum library jaate ho:
- **Query (Q):** Tumhara sawaal, "mujhe Python loops pe kuch chahiye"
- **Key (K):** Har kitaab ki spine pe likha title/label
- **Value (V):** Kitaab ke andar ka asli content

Process:
1. Apna sawaal (Q) har kitaab ke label (K) se match karo → **score**
2. Scores ko percentages me badlo (softmax): "loops wali kitaab 70%, Python intro 25%, cooking 5%"
3. Har kitaab ka content (V) utne percent mix karke le jao → **output**

## Model me

Har token apne vector se **teen** cheezein banata hai (teen alag seekhi hui matrices se):
```python
q, k, v = self.qkv(x).chunk(3, dim=-1)     # repo, LinearAttention aur SparseAttention dono me
```

- `q`: "Main kya dhoondh raha hoon?"
- `k`: "Mere paas kis type ki info hai?" (label)
- `v`: "Ye rahi meri asli info" (content)

## Ek example

Prompt: `# Return x plus one.\ndef f(x):\n    return x +`

Last token `+` ka query kuch aisa hai: "mujhe batao kya jodna hai". Attention score:
- `one` (comment me) → **bahut high**
- `x` → medium
- `def`, `(`, `:` → low

To `+` ke output vector me "one" ki info zyada aa jaati hai, aur model `1` predict karne ke kareeb pahunchta hai.

## Causal: sirf peeche dekh sakte ho

Training me poora sentence ek saath diya jaata hai, lekin token 5 ko token 6 dekhne ki **ijaazat nahi**. Warna wo answer "dekh ke" copy kar lega (cheating).

Lab Exp 1 ka weights matrix dekho, upar-right triangle sab **0.00** hai:
```
1.00  0.00  0.00  0.00  0.00     ← token 0 sirf khud ko dekhta hai
0.81  0.19  0.00  0.00  0.00
0.08  0.80  0.12  0.00  0.00     ← token 2 ne token 1 ko 80% suna
0.12  0.30  0.13  0.44  0.00
0.06  0.16  0.25  0.49  0.04
```
Har row ka sum = 1 (softmax).

---
🎬 **Video:** 16:17–17:00 (attention aur indexer ka idea) · 📊 Slide 25

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [Topic 05 — Attention basics → Linear attention](README.md) | 📚 [Topic 05 overview](README.md) | [02 · Definitions — Q, K, V, heads, aur T² problem](02-definitions-and-cost.md) ➡️ |
<!-- /nav:bottom -->
