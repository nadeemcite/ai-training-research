<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 10 — Pretraining loop: random weights se Python tak](README.md) › Reading 2 / 6
<!-- /nav:top -->

# 02 · Definitions — Training ke shabd

| Term | Matlab | Repo me |
|---|---|---|
| **Loss** | Ek number jo bataata hai ki model kitna galat hai. Kam = behtar | cross-entropy |
| **Cross-entropy** | `−log(sahi token ki probability)`, sab positions ka average | `F.cross_entropy` |
| **Gradient** | Har weight ke liye: "loss kam karne ke liye kis taraf aur kitna jaana hai" | `loss.backward()` |
| **Backpropagation** | Chain rule se output se input tak saare gradients nikalna | automatic (PyTorch) |
| **Optimizer** | Gradient dekh ke weights update karne ka rule | AdamW |
| **Learning rate (LR)** | Har step me kitna bada kadam lena | `3e-4` (25.7M model) |
| **Batch** | Ek step me kitne examples ek saath | 32 |
| **Step / update** | Ek baar: batch → loss → gradient → update | 400 steps |
| **Epoch** | Poore dataset ko ek baar dekhna | (synthetic data, har step naya) |
| **Checkpoint** | Training ke beech me weights ka saved snapshot | steps 0, 100, 200, 400 |
| **Padding** | Chhote examples ko barabar length karne ke liye PAD tokens | `pad_id = 0` |
| **`ignore_index = -100`** | Is label wali position ka loss mat gino | padding positions |

## Input aur label: ek position ka shift

```python
values = [BOS, '#', ' ', 'C', 'o', 'm', ...]       # ek example
inputs = values[:-1]     # [BOS, '#', ' ', 'C', 'o', ...]
labels = values[1:]      # ['#', ' ', 'C', 'o', 'm', ...]   ← har input ka "agla" token
```

Position `i` pe model `inputs[:i+1]` dekhta hai aur use `labels[i]` predict karna hai. Lab Exp 1 me ye numbers ke saath dikhega:
```
input  ids[:6] = [1, 39, 36, 71, 115, 113]
labels ids[:6] = [39, 36, 71, 115, 113, 116]
```

## Padding aur -100

Har row ki length 128 honi chahiye, lekin example sirf ~94 tokens ka hai. Baaki jagah `PAD` (0) bhar dete hain, aur un positions ke label `-100` kar dete hain:
```python
labels = labels.masked_fill(labels == tokenizer.pad_id, -100)
```

`F.cross_entropy(..., ignore_index=-100)` un positions ko **skip** karta hai. Warna model "PAD ke baad PAD aata hai" jaisi bekaar cheez seekhta. Lab Exp 1: *"Asli target tokens: 94 / 128"*.

## Loss ke numbers ka matlab

| Loss | Matlab |
|---:|---|
| `ln(260) ≈ 5.56` | Bilkul random guess (260 me se 1) |
| ~2.0 | Kuch patterns pakde (lab step 50) |
| ~0.5 | Zyadatar bytes sahi (step 150) |
| ~0.25 | Kaafi confident (step 300) |
| 0 | Perfect, har byte 100% sure. Ye aksar **overfitting** ka sign hota hai |

Lab Exp 2 me random logits ka loss **6.31** aaya, jo `ln(260)` se bhi zyada hai. Kyun? Random logits **uniform** nahi hote: kuch galat tokens ko zyada probability mil jaati hai, aur ye uniform se bhi bura hai.

## Repo ka asli GPU run (`REPORT.md`)

| Step | Dev tasks solved |
|---:|---:|
| 0 | 0/8 |
| 100 | 2/8 |
| 200 | 7/8 |
| 400 | 8/8 |

1,381,760 tokens, **63 sec**, RTX 3080 Ti GPU. Checkpoint **100** ko RL ke liye chuna gaya, kyunki usme "genuine code learning" tha lekin sudhaar ki jagah (headroom) bhi bachi thi.

---
📁 `train_pretrain.py` lines 22–34 (`batch_for`) · 🎬 Video 26:14–27:30

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [01 · Concept — Pretraining = nakal karke seekhna](01-concept-imitation.md) | 📚 [Topic 10 overview](README.md) | [03 · Practical — Ek training step, line by line](03-the-training-step.md) ➡️ |
<!-- /nav:bottom -->
