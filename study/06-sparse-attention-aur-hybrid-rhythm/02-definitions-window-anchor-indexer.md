<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 06 — Sparse attention + 3:1 hybrid rhythm](README.md) › Reading 2 / 6
<!-- /nav:top -->

# 02 · Definitions — Window, anchor, stride, indexer

## Definitions

| Term | Matlab | Hamare model me |
|---|---|---|
| **Sparse attention** | Har query sirf chuni hui keys pe softmax attention karti hai | Layers 4, 8, 12 |
| **Local window (W)** | Pichle W tokens (khud ko milake) | `sparse_window = 32` |
| **Anchors** | Har S-th position (0, S, 2S, ...), jo door tak pahunch dete hain | |
| **Stride (S)** | Anchors ke beech ka gap | `sparse_stride = 32` |
| **Gather** | Chuni hui positions ke K, V nikaal ke ek chhoti list banana | `k[:, :, indices, :]` |
| **Indexer** | Sasta scoring network jo relevant tokens chunta hai | Released GLM me hai, hamare me nahi |
| **Top-k** | Sabse zyada score wale k items | Released: ~1–2 hazaar (video) |

## Repo ka selection rule

```python
def _indices(self, length, device):
    for position in range(length):
        anchors = list(range(0, position + 1, self.stride))                 # 0, 32, 64, ...
        local   = list(range(max(0, position - self.window + 1), position + 1))  # pichle 32
        rows.append(sorted(set(anchors + local)))                            # dono, bina duplicate
```

Lab Exp 1 (window 5, stride 4, position 14):
```
anchors = [0, 4, 8, 12]
local   = [10, 11, 12, 13, 14]
set     = [0, 4, 8, 10, 11, 12, 13, 14]       ← 12 dono me tha, ek baar gina
```

**Causal** bhi hai: `range(..., position + 1)` → future kabhi nahi.

## Forward pass (simplified)

```python
q, k = apply_rope(q, k)                         # Topic 04
gathered_k = k[:, :, indices, :]                # har query ki chuni hui keys
gathered_v = v[:, :, indices, :]
scores  = q · gathered_k / √d                   # sirf chuni hui keys se
scores  = masked_fill(~valid, −∞)               # padding positions band
weights = softmax(scores)
output  = weights · gathered_v
```

Topic 05 wala softmax attention hi hai, bas `[T × T]` ki jagah `[T × chuni hui keys]` pe.

**Padding/`valid` kyun?** Position 3 sirf 4 keys dekhta hai, position 191 ~37 keys. Tensor me sab rows ki length barabar honi chahiye, to chhoti rows ko bhar ke `valid = False` mark karte hain, aur unka score `−∞` ho jaata hai.

## Indexer kaise sasta hai?

Asli attention: 32-dim q·k, 6 heads. Indexer: bahut **chhote** vectors (jaise 4–16 dims), kam heads, aur ho sake to low precision (FP8).

Lab Exp 4 me indexer sirf **4 dims** use karta hai (32 ki jagah), phir bhi needle dhoondh leta hai, kyunki use sirf **ranking** chahiye, exact score nahi.

---
📁 `model.py` lines 89–131 · 🎬 Video 16:17–17:48

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [01 · Concept — "Sab mat dekho, sahi cheezein dekho"](01-concept-sparse.md) | 📚 [Topic 06 overview](README.md) | [03 · Practical — Kitna sasta? Fixed vs Indexer](03-practical-cost-and-indexer.md) ➡️ |
<!-- /nav:bottom -->
