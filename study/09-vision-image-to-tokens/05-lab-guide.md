<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 09 — Vision: image ko tokens me badalna](README.md) › Reading 5 / 6
<!-- /nav:top -->

# 05 · Code Lab — `lab_vision.py`

## Run (~10 sec, CPU pe)

```bash
uv run study/09-vision-image-to-tokens/lab_vision.py          # seed 42
uv run study/09-vision-image-to-tokens/lab_vision.py 7        # koi aur seed
```

Ye lab **repo ka asli code** import karta hai (`glm53_flash/vision.py`, `scripts/train_vision.py`). Kuch copy nahi kiya gaya hai.

## Expected output (aur matlab)

```
Exp 1  digit '3' (32x32 RGB, har 2 pixel = 1 character):
       ................
       ....########....
       ....##########..
       ............##..
       ....##########..
       ............##..
       ....########....
```
*(16 lines aati hain, yahan kuch chhod di gayi hain.)*
→ Ye repo ka generated seven-segment "3" hai (Reading 03). Asli image rangeen aur thodi noisy hai.

```
Exp 2  image                (1, 3, 32, 32)   [batch, RGB, H, W]
       patch embedding       (1, 64, 24)   8x8 patches (har patch 4x4 px)
       2 vision blocks       (1, 64, 24)   patches aapas me baat karte hain
       2x2 spatial merge     (1, 16, 32)   64 -> 16, width 24 -> 32 (LM ki dim)
       projector             (1, 16, 32)   = 16 'visual tokens'
```
→ Reading 03 ki shape journey, repo ke encoder ke andar se.

```
Exp 3  sequence: <BOS> <img_start> <image> x16 <img_end> 'Digit: '
       kul 26 positions; 16 <image> placeholders ki jagah visual vectors daale jaate hain
```
→ Language model ko yahi sequence milti hai (Reading 01, 03).

```
Exp 4  seed=42, 120 steps training (repo ka VISION_REPORT wala setup), held-out 200 images:
       faithful               params=60,924  accuracy   0/200 -> 139/200  (4.8s)
       direct_patch_baseline  params=42,500  accuracy   0/200 -> 189/200  (2.4s)
```
→ Reading 04 ka negative result. Repo report me faithful 119/200 tha (PyTorch 2.5.1), aur hamare PyTorch 2.14 pe 139/200 aata hai.

## Tumhara kaam (15 min)

1. **TODO (a):** Exp 1 me `seed=7` ko `8`, `9` karo. Digit ki position aur noise kaise badalte hain? Agar har training image bilkul same hoti, to model kya "seekh" leta? (Hint: ratna.)
2. **TODO (b):** `uv run .../lab_vision.py 7` aur `... 123` chalao. Maine chala ke dekha: faithful 120 aur 93, baseline 175 aur 194. Teen seeds pe kya conclusion nikaal sakte ho, aur kya **nahi** nikaal sakte?
3. **TODO (c):** Exp 2 me `v_config` ka `patch_size=8` karo. Ab kitne patches aur kitne final tokens bane? (Hint: 32/8 = 4, fir 2×2 merge.)
4. **Research soch:** Faithful path ko jitane ke liye tum kya badloge? Zyada steps? Bada width? Mushkil data? Ek-ek variable badal ke try karo (Topic 11 isi pe hai).

## Repo ke tests

```bash
cd sources/repo && uv run python -m pytest tests/test_vision.py -q
```
Ye shapes, token order, label alignment, aur "gradients sab components tak pahunchte hain" check karta hai.

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [04 · Results — ek honest negative result, aur Real-life](04-results-and-real-life.md) | 📚 [Topic 09 overview](README.md) | [06 · Recap + Quiz](06-recap-quiz.md) ➡️ |
<!-- /nav:bottom -->
