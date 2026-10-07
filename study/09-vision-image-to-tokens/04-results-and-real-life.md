<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 09 — Vision: image ko tokens me badalna](README.md) › Reading 4 / 6
<!-- /nav:top -->

# 04 · Results — ek honest negative result, aur Real-life

## Experiment: "faithful" vs simple baseline

Repo ne do vision paths compare kiye:

| | Faithful (GLM jaisa) | Direct-patch baseline |
|---|---|---|
| Patches | 4×4 → 64 | 8×8 → seedha 16 |
| Vision transformer | 2 blocks | **Koi nahi** |
| Merge + projector | Haan | **Nahi**, bas ek Linear |
| Params | 60,924 | 42,500 |

### Results (120 steps, held-out 200 images)

| Source | Seed | Faithful | Baseline |
|---|---|---:|---:|
| Repo `VISION_REPORT.md` (PyTorch 2.5.1) | 42 | 119/200 | **189/200** |
| Hamara lab (PyTorch 2.14) | 42 | 139/200 | **189/200** |
| Hamara lab | 7 | 120/200 | **175/200** |
| Hamara lab | 123 | 93/200 | **194/200** |

**Simple baseline ne har baar jeeta**, wo bhi kam params ke saath.

### Isse kya seekhein? 🧠

1. **"Asli model jaisa" ≠ "is setting me behtar".** Badi architecture ki taakat badi scale pe dikhti hai: 24 blocks, 1024 width, aur crore-on images. 120 steps aur 60k params pe extra layers ko seekhne ka time hi nahi mila.
2. **Negative results bhi results hain.** Repo ne ise chhupaya nahi: *"This is a useful negative result... One synthetic dataset and one seed cannot establish a general architecture ranking."*
3. **Reproducibility ka sach:** Same seed 42, same code, lekin PyTorch version alag hai, to faithful ka result 119 ki jagah 139 aaya. Floating-point operations ka order versions me badal sakta hai. Isliye **multiple seeds** zaroori hain: ek number pe bharosa mat karo.

## Kya ye poore 25.7M model ke saath bhi chala?

Haan. Repo ka ek pilot (`FULL_25M_VISION_DIGIT_PILOT_REPORT.md`) vision encoder ko **poore 12-layer, 25.7M language model** se joda:
- Language model: pretraining checkpoint 100 se shuru
- Trainable: vision encoder + last LM block + final norm + tied embedding (2.3M params). Blocks 1–11 frozen rahe, lekin unke through gradient flow hua.
- 40 updates (~37 sec, Mac GPU): held-out accuracy **0/100 → 40/100**

Report khud kehta hai ki ye "integration pilot" hai, matlab wiring kaam karti hai. Ye "vision capability" ka proof nahi hai: ek task, ek seed, aur koi baseline nahi.

> Video: *"If you want to do some research, you can make this a lot harder and then try to see at which point it's not able to recognize them."*

---

## Real-life analogy 1: Jigsaw puzzle 🧩

Ek tukda (patch) akela dekh ke nahi bata sakte ki tasveer kya hai. Jab tum saare tukde ek saath dekhte ho aur ek-doosre se jodte ho (attention), tab picture banti hai.
**2×2 merge** = 4 chhote tukdon ko jod ke ek bada tukda bana lena, taaki ginti kam ho jaaye.

## Real-life analogy 2: Google Lens / UPI QR scan 📱

Google Lens photo leta hai, use tukdon me todta hai, features nikalta hai, aur fir language model se jawab banata hai: "Ye ek Peepal ka patta hai". GLM-5.3 jaise multimodal models yahi pipeline bade scale pe chalate hain.

## Real-life analogy 3: Translator 🗣️

Vision encoder aur language model alag "bhasha" bolte hain (width 24 vs 32). **Projector ek translator hai** jo image ki baat ko language model ki bhasha me badal deta hai.

---
🎬 **Video:** 25:00–26:14 · 📄 `VISION_REPORT.md`, `FULL_25M_VISION_DIGIT_PILOT_REPORT.md`

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [03 · Practical — 32×32 image se 16 tokens tak, step by step](03-practical-pipeline.md) | 📚 [Topic 09 overview](README.md) | [05 · Code Lab — `lab_vision.py`](05-lab-guide.md) ➡️ |
<!-- /nav:bottom -->
