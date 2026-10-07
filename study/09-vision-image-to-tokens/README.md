<!-- nav:top -->
[🏠 Course](../README.md) › **Topic 09 / 14** › ▶️ [Pehli reading shuru karo](01-concept-image-as-tokens.md)
<!-- /nav:top -->

# Topic 09 — Vision: image ko tokens me badalna

**Pichle topics se link:** Ab tak model sirf text (bytes) padhta tha. GLM-5.3-Flash **multimodal** hai, yaani wo images bhi dekh sakta hai. Lekin transformer sirf **vectors ki sequence** samajhta hai (Topic 02). To sawaal ye hai: ek photo ko "tokens" kaise banayein, taaki wahi language model use padh sake?

**Time:** ~45 min (padhai) + ~15 min (lab)

## Reading order

| File | Type | Kya milega |
|---|---|---|
| [01-concept-image-as-tokens](01-concept-image-as-tokens.md) | Concept | Image ko puzzle ke tukdon (patches) me todna |
| [02-definitions](02-definitions.md) | Definitions | Patch, ViT, bidirectional attention, spatial merge, projector, placeholder |
| [03-practical-pipeline](03-practical-pipeline.md) | Practical | 32×32 image → 64 patches → 16 tokens, aur sequence me kaise judte hain |
| [04-results-and-real-life](04-results-and-real-life.md) | Practical + Real-life | Faithful vs simple baseline (ek honest negative result), 2D RoPE, Google Lens |
| [05-lab-guide](05-lab-guide.md) | Code | [`lab_vision.py`](lab_vision.py): digit dekho, shapes track karo, digit-reader train karo |
| [06-recap-quiz](06-recap-quiz.md) | Test | 8 sawaal |

## Pipeline (**bold** = is topic ka part)

```
image → **patches → vision transformer → 2×2 merge → projector** → 16 visual tokens ┐
                                                                                     ├→ language model (Topics 02–07) → "7"
text  → tokenizer → embeddings ──────────────────────────────────────────────────────┘
```

## Repo me kahan hai?

- `sources/repo/glm53_flash/vision.py`: poora vision path (`MiniGLMVisionEncoder`, `VisionLanguageModel`)
- `sources/repo/scripts/train_vision.py`: digit images banana + training
- `sources/repo/VISION_REPORT.md` aur `experiments/FULL_25M_VISION_DIGIT_PILOT_REPORT.md`: results

> ⏭️ **Note:** Topic 08 (Hyper-connections) abhi likha nahi gaya hai. Ye topic uske bina bhi samajh aata hai.

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [06 · Recap + Quiz](../07-mixture-of-experts/06-recap-quiz.md) | 📚 [Topic 09 overview](README.md) | [01 · Concept — Image ko puzzle ke tukdon me todo](01-concept-image-as-tokens.md) ➡️ |
<!-- /nav:bottom -->
