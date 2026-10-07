<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 10 — Pretraining loop: random weights se Python tak](README.md) › Reading 4 / 6
<!-- /nav:top -->

# 04 · AdamW, gradient clipping + Real-life

## Optimizer: SGD se AdamW tak

**SGD (simple):** `weight = weight − lr × gradient`. Har weight ke liye same step size.

**Problem:** Kuch weights ke gradients hamesha bade hote hain aur kuch ke chhote. Saare weights ke liye ek hi LR theek nahi hai.

**Adam** har weight ke liye do running averages rakhta hai:
- **m (momentum):** gradient ki average direction. `β₁ = 0.9` ka matlab: purani direction ka 90% yaad rakho. Isse zig-zag kam hota hai.
- **v:** gradient ke size (square) ka average. `β₂ = 0.95`. Jis weight ka gradient bada hai, uska step **chhota** karo, aur jiska chhota hai uska **bada**.

```
update = lr × m / (√v + ε)
```

**AdamW = Adam + weight decay (W):** Har step pe weights ko thoda sa 0 ki taraf khinchte hain (`weight_decay = 0.1`). Isse weights bina wajah bade nahi hote aur model kam overfit karta hai.

Repo: `AdamW(lr=3e-4, betas=(0.9, 0.95), weight_decay=0.1)`. Ye LLM training ka standard setting hai.

### Muon? 🆕

> Video: *"AdamW, most people are using Muon, but I just did it for simplicity."*

**Muon** ek naya (2024) optimizer hai jo 2D weight matrices ke update ko "orthogonalize" karta hai, taaki update har direction me balanced ho. Kimi, GLM jaise naye models me ye popular ho raha hai. Abhi ke liye itna yaad rakho ki AdamW standard hai aur Muon naya challenger hai.

## Gradient clipping

Kabhi-kabhi ek ajeeb batch bahut bada gradient deta hai. Pura step uthaya to model ek jhatke me kharab ho sakta hai (loss spike → NaN).

**Clipping:** Saare gradients ka combined size (norm) nikaalo. Agar wo 1.0 se zyada hai, to sabko **same ratio** se chhota kar do.

Lab Exp 3:
```
gradient [30, 40, 0], norm = 50   →   clip ke baad [0.6, 0.8, 0.0], norm = 1.00
```

**Direction same rehti hai** (30:40 = 0.6:0.8), sirf size kam hota hai. Yaani "sahi taraf jao, lekin dheere."

Repo RL me bhi `clip_grad_norm_(..., 1.0)` use karta hai.

## Learning rate: sabse important knob 🎛️

| LR | Kya hota hai |
|---|---|
| Bahut chhota | Training bahut slow hoti hai, kuch nahi seekhta |
| Theek | Loss smoothly girta hai |
| Bahut bada | Loss upar-neeche koodta hai, ya NaN |

Lab me mini model `lr = 1e-3` use karta hai, jabki repo ka 25.7M model `3e-4`. **Chhote models aksar bada LR jhel lete hain.** Lab TODO (a) me khud try karo.

---

## Real-life analogy: Cricket coach 🏏

Ek naya batsman hai jiske shots bilkul random hain (random weights).

- **Training data** = bowling machine se hazaaron gendein
- **Loss** = "shot kitna galat tha"
- **Gradient** = coach ka feedback: "bat thoda neeche, kohni thodi upar"
- **Learning rate** = feedback pe kitna badlaav karna hai. Bahut zyada badla to next shot ulta ho jaata hai, bahut kam badla to kabhi nahi sudhrega
- **Momentum (Adam ka m)** = pichle 10 feedbacks ka average follow karo, sirf aakhri ek ka nahi
- **Gradient clipping** = ek pagal bounce pe apna poora stance mat badlo
- **Weight decay** = koi bhi ajeeb aadat (bada weight) bina wajah pakki mat hone do
- **Checkpoint** = har hafte video record karo, taaki kharab hafta ho to wapas ja sako

## Real-life analogy 2: Pehle ratta, fir samajh 📚

Pretraining ek student jaisa hai jo hazaaron solved examples **padh ke** pattern pakadta hai, bina khud koi sawaal solve kiye. Wo "solution jaisa dikhne wala" answer likh leta hai, lekin har baar sahi nahi. Asli practice (khud solve karo, galti pe marks kato) RL hai (Topic 12).

---
🎬 **Video:** 27:00–28:05 · 📁 `train_pretrain.py` line 69 (AdamW), line 99 (clipping)

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [03 · Practical — Ek training step, line by line](03-the-training-step.md) | 📚 [Topic 10 overview](README.md) | [05 · Code Lab — `lab_pretrain.py`](05-lab-guide.md) ➡️ |
<!-- /nav:bottom -->
