<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 10 — Pretraining loop: random weights se Python tak](README.md) › Reading 1 / 6
<!-- /nav:top -->

# 01 · Concept — Pretraining = nakal karke seekhna

## Idea

> **Model ko bahut saara text dikhao. Har position pe use agla token guess karne do. Galat guess hua, to weights thoda sa sudhaar do. Ye lakhon baar repeat karo.**

Ye Topic 01 wala "next token prediction" hi hai, bas ab hum use **training** ke liye use kar rahe hain.

> Video: *"In pre-training it's not thinking of this answer. It's just repeating what the data is... It's similar to imitation learning. It's imitating."*

## Ek example se kitne lessons?

Repo ka ek pretraining example:
```python
# Complete this Python function.
# Double the input.
def double_fofienq(x):
    return x * 2
```

Isme ~94 bytes hain, to ~93 lessons milte hain:
- `#` ke baad → space
- `# Com` ke baad → `p`
- ...
- `return x * ` ke baad → `2`

> Video: *"You have 'r', it predicts 'e'; you have 'return', predicts the space. You have so many training examples just from one prompt."*

## Har galti pe kya hota hai?

1. Model ne `return x * ` ke baad `"2"` ko sirf 5% probability di
2. **Loss** bataata hai: "bahut galat" (`-log(0.05) ≈ 3.0`)
3. **Backpropagation** har weight ke liye nikaalta hai: "agar tum thoda upar/neeche jaate, to `"2"` ki probability kitni badhti?"
4. **Optimizer** har weight ko thoda sa us direction me khiskaata hai

> Video: *"It's going to change millions of weights, so correct byte becomes a bit more likely each time."*

## Lab me jo dikhega (asli output)

| Step | Model `def double_...(x):` ke baad kya likhta hai | Dev tasks (8) |
|---:|---|---:|
| 0 | `'::::::::::::::::::::::::::::'` | 0/8 |
| 50 | `'x x x x x x x x x x x x x x '` | 0/8 |
| 100 | `'return x if x = 0'` | 0/8 |
| 150 | `'return x * 2'` | 3/8 |
| 300 | `'return x * 2'` | **8/8** |

Model ne pehle **characters** seekhe, fir **Python ka shape** (`return x ...`), aur aakhir me **sahi logic**. Ye sab 100 seconds me, CPU pe.

## Pretraining ki limit

Pretraining model ko sikhata hai ki **data me kya common hai**, ye nahi ki **kya sahi hai**. Agar data me galat code hota, to model wo bhi seekhta. Aur ek chhota, kam-trained model "Python jaisa dikhne wala" code bana deta hai jo chalta nahi:

```python
return x * * 0 0        # repo ke checkpoint 100 ka asli output: dikhta Python jaisa, chalta nahi
```

Isi gap ko bharne ke liye **post-training (RL)** hota hai, jahan model ko sahi jawab pe reward milta hai (Topic 12).

---
🎬 **Video:** 26:14–28:05 · 📊 Slides 43–48 "What does pre-training see?"

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [Topic 10 — Pretraining loop: random weights se Python tak](README.md) | 📚 [Topic 10 overview](README.md) | [02 · Definitions — Training ke shabd](02-definitions.md) ➡️ |
<!-- /nav:bottom -->
