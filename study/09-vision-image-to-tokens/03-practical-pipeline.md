<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 09 — Vision: image ko tokens me badalna](README.md) › Reading 3 / 6
<!-- /nav:top -->

# 03 · Practical — 32×32 image se 16 tokens tak, step by step

## Shapes ki journey (lab Exp 2 ka asli output)

```
image                (1, 3, 32, 32)   [batch, RGB, H, W]
patch embedding      (1, 64, 24)      8×8 patches (har patch 4×4 px)
2 vision blocks      (1, 64, 24)      patches aapas me baat karte hain
2×2 spatial merge    (1, 16, 32)      64 → 16, width 24 → 32 (LM ki dim)
projector            (1, 16, 32)      = 16 "visual tokens"
```

Encoder ka code (`MiniGLMVisionEncoder.forward`):
```python
hidden, grid = self.patch_embedding(images)    # 1. kaato + vector banao (+ position)
for block in self.blocks:
    hidden = block(hidden)                     # 2. bidirectional attention + SwiGLU
hidden = self.post_layernorm(hidden)           # 3. RMSNorm (Topic 03)
hidden = self.spatial_merger(hidden, grid)     # 4. 2×2 → 1
return self.projector(hidden)                  # 5. LM ki bhasha me
```

## Step 4 detail: 2×2 merge kaise hota hai?

8×8 grid ko 2×2 ke blocks me baanto. Har block ke 4 vectors (4 × 24 = 96 numbers) ko **jod ke (concat)** ek Linear layer se 32 numbers banao.

```
8×8 grid (64 tokens)           4×4 grid (16 tokens)
┌─┬─┬─┬─┬ ...                  ┌───┬───┬ ...
│a│b│     concat [a,b,c,d]     │   │   │
├─┼─┤      → Linear(96 → 32)   │ A │   │
│c│d│                          ├───┼───┤
└─┴─┴ ...                      └───┴───┴ ...
```

Repo ka comment: ye exactly ek **stride-2 convolution** ke barabar hai. Bas Conv2d ki jagah reshape + Linear likha gaya, kyunki PyTorch 2.5 ke Mac (MPS) backend pe Conv2d ka backward toota hua tha. Practical engineering ka ek accha example hai.

## Step 6: Language model ke andar kaise jaata hai?

**(a) Sequence banao** (lab Exp 3):
```
<BOS> <img_start> <image> ×16 <img_end> 'Digit: '      → kul 26 positions
```

**(b) Embedding lookup karo**, phir placeholders ki jagah visual vectors **scatter** karo:
```python
embedded = self.language_model.embedding(multimodal_input_ids)   # sab ka normal lookup
placeholder_mask = multimodal_input_ids == 261                   # 16 khaali seats
embedded = embedded.masked_scatter(placeholder_mask..., visual)  # unpe image vectors baithao
return self.language_model.forward_embeddings(embedded)          # baaki sab Topic 02–07 jaisa
```

Yahi `forward_embeddings` function Topic 02 me dekha tha. Language model ko pata hi nahi ki kuch vectors image se aaye hain.

## Step 7: Training — sirf jawab pe loss

Training example: image + `"Digit: 3"`. Loss **sirf "3"** pe lagta hai (`answer_only_labels`). Image positions aur prompt "Digit: " ke labels `-100` hote hain, to wo ignore ho jaate hain (Topic 10 me `-100` detail me aayega).

Kyun? Hum chahte hain ki model image dekh ke digit bataye. "Digit: " predict karna seekhne ka koi fayda nahi.

## Data: seven-segment digits 🔢

Repo koi dataset download nahi karta. Wo digital ghadi jaise **seven-segment** digits khud banata hai, aur har image me badalta hai:
- **Position:** ±2 pixel shift
- **Rang:** random RGB
- **Brightness:** 0.8–1.0
- **Noise:** thoda random noise

Held-out images **alag seed** se bante hain, to model ne wo exact images kabhi nahi dekhi. Lekin digit classes (0–9) wahi hain.

---
📁 `vision.py` (`SpatialMerger2x2`, `VisionLanguageModel`) · `train_vision.py` (`generated_rgb_digit_images`) · 🎬 Video 24:30–25:40

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [02 · Definitions — Vision ke shabd](02-definitions.md) | 📚 [Topic 09 overview](README.md) | [04 · Results — ek honest negative result, aur Real-life](04-results-and-real-life.md) ➡️ |
<!-- /nav:bottom -->
