<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 07 — Mixture of Experts (MoE)](README.md) › Reading 2 / 6
<!-- /nav:top -->

# 02 · Definitions — Expert, router, top-k, gate

## Definitions

| Term | Matlab | Hamare model me |
|---|---|---|
| **Expert** | Ek chhota FFN (SwiGLU) | `Expert(192, 384)` |
| **Routed expert** | Wo experts jinme se router chunta hai | 8 |
| **Shared expert** | Wo expert jisse har token guzarta hai | 1 |
| **Router / gate** | Ek Linear layer jo har expert ka score (logit) deta hai | `Linear(192, 8)` |
| **Top-k** | Sabse zyada score wale k experts | k = 2 |
| **Gate weights** | Chune gaye k scores pe softmax. Ye tay karta hai ki output me kis expert ka kitna hissa hai | sum = 1 |
| **Usage** | Kis expert ko kitne % token-slots mile | sum = 1 (repo test) |
| **Total params** | Model me kul parameters | 25.7M |
| **Active params** | Ek token pe asal me kitne params kaam aaye | ~9.8M (repo estimate) |

## Expert ke andar: SwiGLU

```python
class Expert(nn.Module):
    def __init__(self, dim, hidden):
        self.up   = nn.Linear(dim, hidden * 2, bias=False)   # 192 → 768
        self.down = nn.Linear(hidden, dim, bias=False)       # 384 → 192

    def forward(self, x):
        gate, value = self.up(x).chunk(2, dim=-1)            # 768 → 384 + 384
        return self.down(F.silu(gate) * value)
```

- `up` do cheezein banata hai: **gate** aur **value**
- `silu(gate)` 0 se 1 jaisa "kitna allow karna hai" banata hai (smooth switch)
- `gate × value`: value ka sirf allowed hissa aage jaata hai
- `down` wapas 192 pe le aata hai

SwiGLU Llama, Mistral, DeepSeek, GLM sab me hai. Ye plain ReLU FFN se empirically better nikla (Shazeer, 2020).

**Params per expert:** up `192 × 768` + down `384 × 192` = 147,456 + 73,728 = **221,184** (lab Exp 3 ✅)

## Router step by step (lab Exp 1)

```
1. logits  = router(x)                      # [8] scores, e.g. [0.1, 1.3, 1.0, -0.2, ...]
2. top-2   = topk(logits, 2)                # E2 (1.3), E3 (1.0)
3. weights = softmax([1.3, 1.0])            # [0.57, 0.43]
4. output  = shared(x) + 0.57·E2(x) + 0.43·E3(x)
```

Lab ka asli output:
```
token 0: E2 (0.57), E3 (0.43)  + shared
token 1: E6 (0.55), E3 (0.45)  + shared
token 2: E1 (0.60), E4 (0.40)  + shared
```
Har token ne alag pair chuna. Yahi "routing" hai.

**Notice karo:** Softmax sirf chune hue 2 scores pe lagta hai, saare 8 pe nahi. Kuch models (jaise Mixtral) aise karte hain, aur kuch saare 8 pe softmax karke top-k lete hain. Ye ek chhota sa design choice hai.

---
📁 `model.py` lines 134–174 · 🎬 Video 20:42–21:30

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [01 · Concept — Ek bada dimaag vs bahut saare specialists](01-concept.md) | 📚 [Topic 07 overview](README.md) | [03 · Practical — Repo code aur total vs active params](03-practical-code-and-params.md) ➡️ |
<!-- /nav:bottom -->
