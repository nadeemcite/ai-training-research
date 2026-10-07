<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 13 — RLOO: advantage se update tak, aur sirf last block train karna](README.md) › Reading 4 / 6
<!-- /nav:top -->

# 04 · Sirf last block train karo, pilot history + Real-life

## Train scope: 2.19M of 25.7M

```python
for p in model.parameters():       p.requires_grad = False      # sab freeze
for p in model.layers[-1]...:      p.requires_grad = True       # last hybrid block
for p in model.final_norm...:      p.requires_grad = True       # final RMSNorm
for p in model.embedding...:       p.requires_grad = True       # tied embedding = output head
```

Lab Exp 5: **2,190,152 / 25,730,592 = 8.5%** (repo receipt se exact match).

> Video (37:37): *"I'm just going to update last block, final normalization layer and the output head... This way first of all we are not changing previous layers that have some other knowledge, and they might experience forgetting... And this is also faster, updating less weights."*

### Fayde
1. **Kam forgetting:** pehli 11 layers ka pretraining knowledge safe rehta hai
2. **Tez aur sasta:** kam gradients aur kam optimizer memory
3. **Stable:** chhota "surface" hai, to bade jhatke kam lagte hain

### Ek subtle baat: tied head
Embedding aur output head **ek hi matrix** hain (Topic 02). Head train karne se **input embeddings bhi badal jaate hain**, aur unhe pehli layer bhi use karti hai! To "sirf aakhri hissa" poori tarah sach nahi hai.

### Alternatives
> Video: *"You can also use LoRA, you can use different techniques, you can update the whole model."*

**LoRA:** original weights freeze karo, aur har weight matrix ke saath ek chhota "low-rank" add-on train karo. Ye bade models ka standard hai.

## Pilot history: pehli koshish me kuch nahi chala

REPORT ne saari failed koshishein bhi likhi hain:

| # | Setting | Result |
|---:|---|---|
| 1 | Poora model, temp 0.8, lr 2e-5 | **Unstable**: dev 2/8 → 0/8 |
| 2 | Poora model, temp 0.35, lr 1e-6 | Stable lekin **koi badlaav nahi** (2/8) |
| 3 | Sirf last block, lr 2e-5 | Koi badlaav nahi (2/8) |
| 4 | Focused, lr 5e-5, 24 groups | 2/8 → 3/8 |
| 5 ✅ | Zyada task diversity, group 16, **head bhi trainable**, 96 groups | dev sampled 4.2% → **45.8%** |

> REPORT: *"Reporting only the successful configuration would conceal the amount of method selection."*

Ye honesty bahut zaroori hai. 5 koshishon ke baad ek chali, to "dev" set pe thoda overfit hona possible hai. Isliye final result ek **fresh confirmation split** pe, **sirf ek baar** naapa gaya (Topic 14).

## Hamara CPU run (lab Exp 6, `--run`)

2.2M model, 120 pretraining steps, fir 48 RL groups × 16 (same RLOO code, last block + head, lr 1e-4):

| | Dev sampled exact (3 families, 96) |
|---|---:|
| RL se pehle | 1–3 /96 |
| RL ke baad | **24–25 /96** |

Repo ke GPU run jaisa hi pattern (4/96 → 44/96), bas ~2 min me CPU pe. Do runs me numbers thode alag aaye (CPU threads, Topic 08).

---

## Real-life analogy: Cooking class 🍳

Ek teacher 16 students ko ek hi dish banane ko kehti hai (group). Taste test hota hai (reward).

- **Raw reward:** "Tumhari dish 7/10 thi." Lekin ye aasaan dish thi ya mushkil?
- **Advantage:** "Class ka average 5/10 tha, tumhari 7/10 thi, to tum average se **+2** behtar ho." Ab feedback ka matlab hai.
- **Sab ne same banaya:** kisi ko kuch naya feedback nahi milta (zero advantage).
- **Koi critic nahi:** alag se food critic hire karne ki zaroorat nahi, class khud baseline hai.
- **Last block train karna:** sirf **plating aur final seasoning** sudhaaro, knife skills (pehli layers) mat chhedo, warna wo bigad sakti hain.
- **KL penalty (jo repo me nahi):** "apni pehle wali style se zyada door mat jao."

---
🎬 **Video:** 37:37–38:41 · 📊 Slide 67 "Update only 2.19M parameters" · 📄 `REPORT.md` → Pilot history

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [03 · Practical — Repo ka RLOO update, line by line](03-the-rloo-update.md) | 📚 [Topic 13 overview](README.md) | [05 · Code Lab — `lab_rloo.py`](05-lab-guide.md) ➡️ |
<!-- /nav:bottom -->
