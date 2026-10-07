<!-- nav:top -->
[🏠 Course](../README.md) › **Topic 03 / 07** › ▶️ [Pehli reading shuru karo](01-concept.md)
<!-- /nav:top -->

# Topic 03 — RMSNorm: numbers ko control me rakhna

**Pichle topic se link:** Topic 02 me har token ek 192-number ka vector ban gaya. Ab ye vector 12 blocks se guzrega, aur har block isme kuch "jodega". Agar numbers bina control ke bade hote gaye, to training toot jaati hai. RMSNorm yahi control karta hai.

**Time:** ~35 min (padhai) + ~15 min (lab)

## Reading order

| File | Type | Kya milega |
|---|---|---|
| [01-concept](01-concept.md) | Concept | Numbers "explode" kyun hote hain, aur normalize karna kya hai |
| [02-definitions-formula](02-definitions-formula.md) | Definitions | RMS, epsilon, gamma, aur formula step-by-step |
| [03-practical-pre-norm](03-practical-pre-norm.md) | Practical | Repo me RMSNorm kahan-kahan lagta hai (pre-norm), aur LayerNorm se fark |
| [04-real-life](04-real-life.md) | Real-life | Music app ka volume normalization, exam ke marks |
| [05-lab-guide](05-lab-guide.md) | Code | [`lab_rmsnorm.py`](lab_rmsnorm.py): 48 layers me explosion khud dekho |
| [06-recap-quiz](06-recap-quiz.md) | Test | 8 sawaal |

## Pipeline me kahan hai? (**bold** = is topic ka part)

```
embedding → [ block × 12:  **RMSNorm** → attention → +  ,  **RMSNorm** → MoE → + ] → **final RMSNorm** → output head
```

## Repo me kahan hai?

- `sources/repo/glm53_flash/model.py`: class `RMSNorm` (lines 33–41, sirf 9 lines!)
- `HybridBlock`: `attention_norm`, `ffn_norm`
- `GLM53FlashFromScratch`: `final_norm`

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [06 · Recap + Quiz](../02-embeddings-aur-output-head/06-recap-quiz.md) | 📚 [Topic 03 overview](README.md) | [01 · Concept — Numbers ko "explode" hone se bachana](01-concept.md) ➡️ |
<!-- /nav:bottom -->
