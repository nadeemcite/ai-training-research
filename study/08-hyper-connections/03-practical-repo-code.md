<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 08 — Hyper-connections: ek highway ki jagah 4 lanes](README.md) › Reading 3 / 6
<!-- /nav:top -->

# 03 · Practical — Repo ka code, aur ek quirk jo humne pakda

## `HyperConnection`, line by line

```python
class HyperConnection(nn.Module):
    def __init__(self, config, block):
        self.block = block
        self.input_logits  = nn.Parameter(torch.linspace(0.1, -0.1, config.streams))   # read
        self.output_logits = nn.Parameter(torch.linspace(-0.1, 0.1, config.streams))   # write

    def forward(self, streams):                                     # [B, T, 4, D]
        mixed = torch.einsum("s,btsd->btd",
                             torch.softmax(self.input_logits, dim=0), streams)   # 1. READ: 4 → 1
        transformed, usage = self.block(mixed)                                   # 2. attention + MoE
        routed = torch.softmax(self.output_logits, dim=0)
        streams = streams + transformed.unsqueeze(2) * routed[None, None, :, None]  # 3. WRITE: 1 → 4
        return streams, usage
```

`einsum("s,btsd->btd")` = "har stream `s` ko uske weight se multiply karo aur jod do". Ye 4 streams ka weighted average hai.

## 🔍 Quirk: identity do baar judti hai

`HybridBlock` khud residual karta hai:
```python
def forward(self, x):
    x = x + self.attention(self.attention_norm(x))
    ffn, usage = self.moe(self.ffn_norm(x))
    return x + ffn, usage            # = x + attention + MoE   ← isme x pehle se hai
```

Fir `HyperConnection` us output ko stream me **phir se jodta** hai:
```
stream_new = stream + write × (mixed + attention + MoE)
                ↑                  ↑
           identity #1        identity #2
```

Isliye residual stream har layer **badhta** jaata hai. Lab Exp 4 (12 layers ke baad, init pe):

| Streams | Residual stream ka size |
|---:|---:|
| 1 | **~7,460×** (har layer lagbhag double) |
| 4 | **~19×** (har layer ~1.25×) |

### Kya isse training toot gayi?

**Nahi.** Har sublayer se pehle RMSNorm hai (Topic 03), aur end me `final_norm`. Norm size ko bhool jaata hai aur sirf direction dekhta hai, isliye model train ho jaata hai (Topic 10 me 8/8 dekha).

**Lekin side-effect hai:** stream jitna bada hota hai, baad wali layers ka update **relatively utna chhota** hota hai. Layer 12 ka update 19× bade stream me judta hai, to uska asar kam ho jaata hai. Standard transformers (aur mHC) isse bachne ke liye identity ko **exactly ek baar** rakhte hain.

**Ek aur nateeja:** `streams=1` set karne se "normal transformer" **nahi** milta. Usme identity har layer double hoti hai. Isliye "1 vs 4 streams" comparison bhi bilkul saaf nahi hai (Reading 04).

> **Research lesson:** Topic 07 (balance loss) aur Topic 12 (reward hack) ki tarah, ye bhi ek chhupi detail hai jo sirf code padhne aur **measure** karne se dikhti hai. Video ka advice yaad karo: *"maybe it's a bug in my code or bug that AI generated."* Har component ko ek chhote test se check karo.

### Fix kaisa dikhega? (idea, repo me nahi)

```python
transformed, usage = self.block(mixed)
update = transformed - mixed                     # block ka sirf "badlaav" lo, identity hata do
streams = streams + update.unsqueeze(2) * routed[None, None, :, None]
```

Ye ek accha **experiment** hai: dono versions train karo aur loss compare karo, kai seeds pe. Chapter 15 ka capstone code yahi fixed version use karta hai.

---
📁 `model.py` lines 177–207

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [02 · Definitions — Streams, mix, route, mHC](02-definitions.md) | 📚 [Topic 08 overview](README.md) | [04 · mHC ka constraint, asli result + Real-life](04-mhc-and-real-life.md) ➡️ |
<!-- /nav:bottom -->
