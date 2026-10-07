<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 09 — Vision: image ko tokens me badalna](README.md) › Reading 2 / 6
<!-- /nav:top -->

# 02 · Definitions — Vision ke shabd

| Term | Matlab | Hamare mini model me |
|---|---|---|
| **Multimodal** | Ek model jo ek se zyada type ka input samjhe (text + image) | text bytes + RGB image |
| **RGB** | Har pixel ke 3 numbers: Red, Green, Blue (0 se 1) | `[3, 32, 32]` |
| **Patch** | Image ka ek chhota square tukda | 4×4 pixels |
| **Patch embedding** | Patch ke saare numbers ko ek vector me badalna (ek Linear/Conv layer) | 4×4×3 = 48 numbers → 24-dim vector |
| **Vision Transformer (ViT)** | Patches pe chalne wala transformer | 2 blocks, 4 heads, width 24 |
| **Bidirectional attention** | Har token har token ko dekh sake, koi causal mask nahi | `is_causal=False` |
| **Spatial merge** | Paas-paas ke 2×2 patches ko jod ke 1 token banana | 64 → 16 tokens |
| **Projector** | Vision vectors ko language model ki "bhasha" (dim) me badalna | width → LM dim (32) |
| **Visual tokens** | Projector ke output vectors jo LM me jaate hain | 16 |
| **Placeholder token** | Sequence me ek "khaali seat" jahan baad me image vector baithta hai | ID 261 |
| **Image start / end** | Image ke boundary markers | IDs 260, 262 |

## Vocab size 260 → 263 kyun?

Topic 01 me vocab 260 tha (256 bytes + 4 special). Vision ke liye 3 naye special IDs chahiye:

| ID | Naam | Kaam |
|---|---|---|
| 260 | `<img_start>` | "Image yahan se shuru" |
| 261 | `<image>` (placeholder) | 16 baar aata hai. Har ek ki jagah ek visual vector daala jaata hai |
| 262 | `<img_end>` | "Image khatam" |

Isliye vision model me `vocab_size = 263` hai.

## Patch embedding = ek chalaak Conv

```python
self.proj = nn.Conv2d(3, hidden_size, kernel_size=4, stride=4)
```

`kernel_size = stride = 4` ka matlab hai ki filter 4×4 ke tukde pe lagta hai, fir **4 pixel aage** khisakta hai. Overlap nahi hota, to har patch ek baar dekha jaata hai. Ye ek **Linear layer har patch pe** lagane ke barabar hai.

## Position: patch kahan tha?

Topic 04 jaisi problem yahan bhi hai: attention ko pata nahi ki kaunsa patch upar-left tha aur kaunsa neeche-right.

| | Released GLM-5.3 | Hamara mini model |
|---|---|---|
| Patch position | **2D RoPE**: vector ka aadha hissa row ke hisaab se, aadha column ke hisaab se rotate | **Seekhi hui table** (64 positions × 24) |

> Video: *"It has this 2D positional rotary embeddings, similar to RoPE, it's just 2D."*

2D RoPE ka idea Topic 04 jaisa hi hai, bas ek ki jagah do doori: "kitni row upar" aur "kitne column baaye".

## Q/K norm (vision attention me)

Vision attention me q aur k ko attention se pehle **RMSNorm** kiya jaata hai (`q_norm`, `k_norm`). Ye Topic 03 hai, bas ek nayi jagah pe: isse attention scores bahut bade nahi hote aur training stable rehti hai.

---
📁 `vision.py` lines 18–110 · 🎬 Video 23:06–24:30

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [01 · Concept — Image ko puzzle ke tukdon me todo](01-concept-image-as-tokens.md) | 📚 [Topic 09 overview](README.md) | [03 · Practical — 32×32 image se 16 tokens tak, step by step](03-practical-pipeline.md) ➡️ |
<!-- /nav:bottom -->
