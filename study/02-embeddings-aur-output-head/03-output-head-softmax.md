<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 02 — Embeddings, Output Head aur Weight Tying](README.md) › Reading 3 / 6
<!-- /nav:top -->

# 03 · Practical — Output head: vector se "agla token" tak

## Kya chahiye

Transformer ke end me last position ka ek vector `hidden` milta hai (192 numbers). Hume chahiye: **260 tokens me se har ek ki probability**.

## Step 1 · Logits (raw scores)

```python
self.output = nn.Linear(192, 260, bias=False)
logits = self.output(hidden)        # [192] → [260]
```

`logits[i]` = token `i` ka raw score. Ye kuch bhi ho sakta hai, jaise `-3.2`, `0.5`, `7.1`. Ye abhi probability nahi hai.

**Andar kya hota hai?** Har token ki ek "output vector" row hoti hai, aur:
```
logit[i] = hidden · output_row[i]       (dot product = kitna "match" karta hai)
```

## Step 2 · Softmax → probabilities

```
p[i] = exp(logit[i]) / Σ_j exp(logit[j])
```

- Saare `p[i]` 0 aur 1 ke beech aate hain
- Sabka sum = **1**
- Bada logit → bahut zyada probability (exp ki wajah se)

Chhota example:

| Token | logit | exp | probability |
|---|---:|---:|---:|
| `1` | 3.0 | 20.1 | **0.84** |
| `2` | 1.0 | 2.7 | 0.11 |
| `x` | 0.0 | 1.0 | 0.04 |

## Step 3 · Token chuno

| Tarika | Kaise | Kab |
|---|---|---|
| **Greedy** | Sabse badi probability wala token (`argmax`) | Evaluation me ("greedy pass@1", 0/24 → 16/24 wala result) |
| **Sampling** | Probability ke hisaab se random pick | RL me ek prompt pe 16 alag attempts generate karne ke liye |
| **Temperature** | Sampling se pehle logits ko T se divide karo | T kam = confident/boring, T zyada = random/creative |

> Video ke RL experiments me **temperature 0.2** ne zyada random temperature se better perform kiya (40:30+). Ye ek real research knob hai.

## Step 4 · Training me: cross-entropy loss

Agar sahi agla token `1` tha:
```
loss = -log(p["1"])
```
- `p = 0.84` → loss = 0.17 (accha)
- `p = 0.004` → loss = 5.5 (bahut bura; random model aise hi shuru hota hai, `ln(260) ≈ 5.56`)

Lab me tum dekhoge ki training **step 0 pe loss ≈ 5.55** se shuru hota hai, jo exactly random guessing hai! 🎯

## Real-life example

Google search me type karo "how to make" aur suggestions aate hain: *"how to make tea", "how to make money"...*.
Ye top-k sorted probabilities hi hain, aur concept same hai.

---
🎬 **Video:** 07:40–08:30, 13:20–13:50 · 📊 Slide "The pretraining step" (`cross_entropy(logits, labels)`)

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [02 · Definitions — Embedding table aur tensor shapes](02-definitions-shapes.md) | 📚 [Topic 02 overview](README.md) | [04 · Weight Tying — ek matrix, do kaam](04-weight-tying.md) ➡️ |
<!-- /nav:bottom -->
