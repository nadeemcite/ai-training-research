<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 07 — Mixture of Experts (MoE)](README.md) › Reading 3 / 6
<!-- /nav:top -->

# 03 · Practical — Repo code aur total vs active params

## `SparseMoE.forward`, line by line

```python
flat = x.reshape(-1, dim)                              # [B, T, 192] → [B·T, 192]: sab tokens ek list me
logits = self.router(flat)                             # [N, 8]
top_values, top_indices = logits.topk(self.top_k, dim=-1)   # [N, 2], [N, 2]
top_weights = torch.softmax(top_values.float(), dim=-1)     # [N, 2]
output = self.shared(flat)                             # shared expert: har token

for expert_id, expert in enumerate(self.experts):
    positions, slots = torch.where(top_indices == expert_id)   # kin tokens ne mujhe chuna?
    if positions.numel() == 0:
        continue                                               # kisi ne nahi chuna → kaam hi nahi
    contribution = expert(flat[positions])                     # sirf un tokens pe chalo
    contribution = contribution * top_weights[positions, slots, None]
    output.index_add_(0, positions, contribution)              # sahi token ke output me jodo
    usage[expert_id] = positions.numel()

usage = usage / (N * top_k)                            # fraction; sum = 1
```

**Key insight:** Loop **experts** pe hai, tokens pe nahi. Har expert apne saare tokens ek saath (batch me) process karta hai. Yahi MoE ki efficiency hai: jo expert chuna nahi gaya, uska koi compute nahi.

`index_add_`: "position 7 ke output me ye contribution jod do". Ek token 2 experts se aata hai, to dono ke contributions jud jaate hain.

## Total vs Active (lab Exp 3)

| | Params |
|---|---:|
| Ek expert | 221,184 |
| Ek MoE layer, **total** (8 routed + 1 shared) | 1,990,656 |
| Ek MoE layer, **active** per token (2 routed + 1 shared) | 663,552 (**33%**) |
| 12 layers, total | 23,887,872 |
| 12 layers, active | 7,962,624 |

Model ke 25.7M me se ~23.9M (**93%**) sirf experts hain! Baaki attention, embedding, norms, etc.

Repo ka `parameter_counts()`: `{'total': 25,730,592, 'active_per_token_estimate': 9,805,344}`. Ye ~9.8M = 7.96M expert-active + ~1.84M non-expert params (attention, router, embedding, ...).

### Released model me

GLM-5.3: 8 + 1 of 289 ≈ **3.1%** experts active. Total ~320B params hain, lekin har token pe compute bahut kam hai.

## ⚠️ Lekin memory to poori chahiye!

Active params kam hain, lekin **saare** experts GPU memory me hone chahiye, kyunki pata nahi agla token kaunsa expert chunega.
- **Compute (FLOPs):** active ke hisaab se → sasta ✅
- **Memory (VRAM):** total ke hisaab se → mehenga ❌

Isliye bade MoE models ko chalane ke liye bahut saari GPUs chahiye, chahe compute kam ho. Ise **expert parallelism** kehte hain: alag experts alag GPUs pe.

## HybridBlock me MoE

```python
def forward(self, x):
    x = x + self.attention(self.attention_norm(x))   # tokens ke beech info move
    ffn, usage = self.moe(self.ffn_norm(x))          # har token khud ko transform kare
    return x + ffn, usage
```

> Video: *"Attention moves information between token positions. MoE applies specialist transformations to each position."*

---
🎬 **Video:** 20:42–22:30 · 📊 Slides 37–40 · 📁 `model.py` lines 145–188

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [02 · Definitions — Expert, router, top-k, gate](02-definitions.md) | 📚 [Topic 07 overview](README.md) | [04 · Load balancing, ek repo bug 🐛, aur Real-life](04-load-balancing-real-life.md) ➡️ |
<!-- /nav:bottom -->
