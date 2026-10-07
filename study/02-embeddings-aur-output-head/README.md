<!-- nav:top -->
[🏠 Course](../README.md) › **Topic 02 / 14** › ▶️ [Pehli reading shuru karo](01-concept-embedding.md)
<!-- /nav:top -->

# Topic 02 — Embeddings, Output Head aur Weight Tying

**Pichle topic se link:** Topic 01 me text → token IDs (numbers) bane. Lekin `104` number ka koi "meaning" nahi hai. Is topic me dekhenge:
- ID → **meaning vector** kaise banta hai (embedding)
- Model ke end me vector → **agle token ki probability** kaise banti hai (output head)
- Dono ke liye **ek hi matrix** kaise use hota hai (weight tying)

**Time:** ~50 min (padhai) + ~25 min (lab)

## Reading order

| File | Type | Kya milega |
|---|---|---|
| [01-concept-embedding](01-concept-embedding.md) | Concept | Token ka "meaning vector" kya hai |
| [02-definitions-shapes](02-definitions-shapes.md) | Definitions | Embedding table, dim, tensor shapes `[B, T, D]` |
| [03-output-head-softmax](03-output-head-softmax.md) | Practical | Hidden → logits → softmax → probability |
| [04-weight-tying](04-weight-tying.md) | Practical + Real-life | Ek matrix, do kaam, aur uski ek chhupi limitation |
| [05-lab-guide](05-lab-guide.md) | Code | [`lab_embeddings.py`](lab_embeddings.py): lookup, softmax, tying, aur mini-training |
| [06-recap-quiz](06-recap-quiz.md) | Test | 8 sawaal |

## Poori pipeline (is topic ka part **bold** hai)

```
text → tokenizer → token IDs → **EMBEDDING** → [12 transformer blocks] → final norm → **OUTPUT HEAD** → probabilities
```

Beech ke 12 blocks (attention, MoE, ...) aage ke topics me aayenge. Abhi unhe ek "black box" maan lo.

## Repo me kahan hai?

`sources/repo/glm53_flash/model.py`, class `GLM53FlashFromScratch` (lines ~210–246)

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [06 · Recap + Quiz](../01-tokens-aur-tokenizer/06-recap-quiz.md) | 📚 [Topic 02 overview](README.md) | [01 · Concept — Embedding = token ka "meaning vector"](01-concept-embedding.md) ➡️ |
<!-- /nav:bottom -->
