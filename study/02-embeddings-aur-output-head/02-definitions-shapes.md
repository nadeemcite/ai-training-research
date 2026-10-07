<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 02 — Embeddings, Output Head aur Weight Tying](README.md) › Reading 2 / 6
<!-- /nav:top -->

# 02 · Definitions — Embedding table aur tensor shapes

## Definitions

| Term | Matlab | Hamare model me |
|---|---|---|
| **Embedding table / matrix** | Ek badi table jisme har row ek token ka vector hai | shape `[260, 192]` |
| **dim / hidden size (D)** | Har vector me kitne numbers hain | `192` |
| **Lookup** | Token ID = row number, to us row ko utha lo. Koi multiplication nahi hota | `embedding(ids)` |
| **Batch (B)** | Ek saath kitne alag sequences process ho rahe hain | training me kai |
| **Time / sequence length (T)** | Ek sequence me kitne tokens hain | max `192` |
| **Hidden state** | Transformer layers ke andar/baad har token ka vector | shape `[B, T, 192]` |

## Lookup = row uthana

```
Embedding table (260 rows × 192 cols)
row 0   (PAD) → [....192 numbers....]
row 1   (BOS) → [....]
...
row 104 ("d") → [....]   ← ID 104 aaya? Ye row utha lo
...
row 259       → [....]
```

Code me:
```python
self.embedding = nn.Embedding(config.vocab_size, config.dim)   # [260, 192]
vectors = self.embedding(input_ids)
```

## Shapes ki journey 📐 (sabse useful skill!)

Research code padhte waqt **shapes track karna** aadha kaam hai.

```
input_ids            [B, T]           e.g. [1, 4]   → BOS d e f
   ↓ embedding
embedded             [B, T, 192]      [1, 4, 192]
   ↓ 4 streams banao (hyper-connections, Topic 08)
streams              [B, T, 4, 192]
   ↓ 12 layers
   ↓ streams.mean(dim=2) + final_norm
hidden               [B, T, 192]
   ↓ output head
logits               [B, T, 260]      [1, 4, 260]  ← har position pe 260 scores
```

**Maine repo ka model chala ke verify kiya:** input `[1, 4]` → output `torch.Size([1, 4, 260])` ✅

## Notice karo

Output me **har position** ke liye 260 scores aate hain, sirf last ke liye nahi.
- **Training me** saari positions use hoti hain, kyunki har position ek lesson hai (Topic 01, Reading 01)
- **Generation me** sirf last position ka score chahiye, jisse agla token chuna jaata hai

## Parameter count

| Part | Params |
|---|---:|
| Embedding table `260 × 192` | 49,920 |
| Poora model (repo `parameter_counts()`) | 25,730,592 |
| Embedding ka share | **~0.19%** |

Byte vocab ki wajah se embedding ka share bahut chhota hai, isliye lagbhag saare params "dimaag" (layers) me jaate hain.

---
🎬 **Video:** 10:47–11:30 ("first you have embedding and then passing input ID...")
📁 `model.py` → `GLM53FlashFromScratch.__init__` aur `forward_embeddings`

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [01 · Concept — Embedding = token ka "meaning vector"](01-concept-embedding.md) | 📚 [Topic 02 overview](README.md) | [03 · Practical — Output head: vector se "agla token" tak](03-output-head-softmax.md) ➡️ |
<!-- /nav:bottom -->
