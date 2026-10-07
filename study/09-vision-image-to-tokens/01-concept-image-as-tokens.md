<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 09 — Vision: image ko tokens me badalna](README.md) › Reading 1 / 6
<!-- /nav:top -->

# 01 · Concept — Image ko puzzle ke tukdon me todo

## Problem

Language model ko input chahiye: **vectors ki ek sequence** `[T, dim]`. Text ke liye ye aasaan tha: har byte ek token, aur har token ka ek vector (Topic 02).

Lekin image kya hai? Ek 32×32 RGB image = 32 × 32 × 3 = **3,072 numbers** ka ek grid. Ye na sequence hai, na tokens.

## Idea: Image ko chhote tukdon (patches) me kaato

> **Image ko chhote square tukdon me kaato. Har tukda ek "token" ban jaata hai, aur use ek vector me badal do.**

> Video: *"For images it's going to get divided to patches, each patch is a token."*

```
32×32 image                         8×8 = 64 patches (har ek 4×4 pixels)
┌────────────────┐                  ┌──┬──┬──┬──┬──┬──┬──┬──┐
│                │                  │  │  │  │  │  │  │  │  │
│      ███       │       →          ├──┼──┼──┼──┼──┼──┼──┼──┤
│        █       │                  │  │  │██│██│  │  │  │  │
│      ███       │                  ├──┼──┼──┼──┼──┼──┼──┼──┤
│        █       │                  │      ...                │
│      ███       │                  └──┴──┴──┴──┴──┴──┴──┴──┘
└────────────────┘
```

Ye idea **ViT (Vision Transformer, 2020)** se aaya: "an image is worth 16×16 words". Ye pura paper ek line ka idea hai: patches ko words ki tarah treat karo.

## Fir patches aapas me baat karte hain

Akela patch sirf ek kona dekhta hai, jaise "yahan ek horizontal line hai". Pata tab chalta hai ki ye "3" hai, jab saare patches ek-doosre ko dekhte hain. Isliye patches pe ek chhota **vision transformer** chalta hai, jisme attention hota hai (Topic 05).

**Ek bada fark:** Text me attention **causal** tha, yaani sirf peeche dekh sakte the. Image me koi "pehle/baad" nahi hota, to har patch **har patch** ko dekh sakta hai. Isse **bidirectional** attention kehte hain.

## Fir tokens kam karo (merge)

64 tokens ek chhoti image ke liye bhi bahut hain, aur har token language model ka compute khaata hai. Isliye **2×2 padosi patches ko jod ke ek token** banate hain: 64 → **16 tokens**.

> Video: *"Four patches are going to become one vector, one token embedding vector. So 2×2 merge, and so we will get 4×4 at the end, which is 16 tokens from this 32×32 image."*

## Fir language model me daal do

16 visual tokens ko text tokens ke saath ek hi sequence me rakh do, aur special markers lagao: "image yahan shuru", "image yahan khatam".

```
<BOS> <img_start> [16 image vectors] <img_end> D i g i t : ␠  →  model predict kare: "3"
```

Language model ke liye ab ye bas ek lambi sequence hai. Use farak nahi padta ki kuch vectors byte se aaye aur kuch image se.

---
🎬 **Video:** 23:06–26:14 · 📊 Slides 18–23 "GLM-5.3-Flash also sees images"

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [Topic 09 — Vision: image ko tokens me badalna](README.md) | 📚 [Topic 09 overview](README.md) | [02 · Definitions — Vision ke shabd](02-definitions.md) ➡️ |
<!-- /nav:bottom -->
