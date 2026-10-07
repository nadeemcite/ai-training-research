<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 10 — Pretraining loop: random weights se Python tak](README.md) › Reading 3 / 6
<!-- /nav:top -->

# 03 · Practical — Ek training step, line by line

Slide 46: **Predict → Compare → Backpropagate → Update**

## Repo ka loop (`train_pretrain.py`, simplified)

```python
model = GLM53FlashFromScratch(config)
optimizer = torch.optim.AdamW(model.parameters(), lr=3e-4, betas=(0.9, 0.95), weight_decay=0.1)

for step in range(1, 401):
    inputs, labels, tokens = batch_for(tokenizer, step=step - 1, batch_size=32, ...)

    optimizer.zero_grad(set_to_none=True)                        # 0. purane gradients saaf
    with torch.autocast("cuda", dtype=torch.bfloat16):           #    (GPU pe fast math)
        logits, usage = model(inputs)                            # 1. PREDICT
        language_loss = F.cross_entropy(logits..., labels...,    # 2. COMPARE
                                        ignore_index=-100)
        balance = ...                                            #    MoE balance (Topic 07)
        loss = language_loss + 0.01 * balance

    if not torch.isfinite(loss): raise FloatingPointError        #    NaN aaya to turant ruko
    loss.backward()                                              # 3. BACKPROPAGATE
    clip_grad_norm_(model.parameters(), 1.0)                     #    bade gradients ko kaabu me rakho
    optimizer.step()                                             # 4. UPDATE
```

## Har line kyun hai?

| Line | Kyun |
|---|---|
| `zero_grad()` | PyTorch gradients ko **jodta** rehta hai. Har step pe saaf na karo to purane gradients mil jaate hain |
| `autocast(bfloat16)` | GPU pe 16-bit math 2× tez hai aur kam memory leta hai. CPU pe band rehta hai |
| `cross_entropy(... ignore_index=-100)` | Padding ka loss mat gino (Reading 02) |
| `+ 0.01 * balance` | MoE experts barabar use hon. ⚠️ Topic 07 me dekha tha ki repo me iska gradient zero hai |
| `isfinite` check | Agar loss `NaN`/`inf` ho gaya, to aage training bekaar hai. Fail fast |
| `backward()` | Saare 25.7M weights ke gradients nikaalo |
| `clip_grad_norm_(1.0)` | Ek kharab batch training ko barbaad na kare (Reading 04) |
| `optimizer.step()` | Weights update karo |

## Data: har step naya

```python
text = pretraining_text(step * batch_size + offset, seed=seed)
```

Data koi file nahi hai. Ye har step pe **deterministically generate** hota hai: same seed → same data. 8 families (increment, double, square, absolute, nonnegative, even, reverse, list_sum) hain, aur har example me random function naam aur 2 me se 1 description hoti hai.

Isliye "epoch" ka concept yahan nahi hai: model kabhi exact same function naam dobara nahi dekhta, lekin **same 8 patterns** baar-baar dekhta hai.

## Reproducibility ke liye repo kya karta hai

- `random.seed`, `torch.manual_seed`: sab seeds fix
- Har checkpoint ke weights ka **SHA-256 hash** save hota hai
- `training-receipt.json`: config, har step ka loss, tokens, time, sab record hota hai
- Output folder pehle se ho to **error** aata hai, taaki purana result galti se overwrite na ho

> **Research habit:** Ek run ka "receipt" rakho. 3 hafte baad tumhe yaad nahi rahega ki LR kya tha.

## CPU vs GPU, honest numbers

| Setup | Time per step | 400 steps |
|---|---:|---:|
| 25.7M model, RTX 3080 Ti (repo) | ~0.16 s | 63 s |
| 25.7M model, hamare Mac CPU, batch 32 | ~4.5 s | **~30 min** |
| 2.2M mini model (lab), CPU, batch 16 | ~0.25 s | ~1.5 min (300 steps) |

Video kehta hai *"it can be trained on a CPU"*. Ye sach hai, lekin poora model CPU pe ~30 min leta hai. Isliye lab chhota model use karta hai, **same code aur same data** ke saath.

---
📁 `scripts/train_pretrain.py` lines 69–100 · 🎬 Video 27:00–28:05 · 📊 Slide 46 "One pre-training step"

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [02 · Definitions — Training ke shabd](02-definitions.md) | 📚 [Topic 10 overview](README.md) | [04 · AdamW, gradient clipping + Real-life](04-adamw-clipping-real-life.md) ➡️ |
<!-- /nav:bottom -->
