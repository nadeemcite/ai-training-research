<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 03 — RMSNorm: numbers ko control me rakhna](README.md) › Reading 3 / 6
<!-- /nav:top -->

# 03 · Practical — Pre-norm, aur LayerNorm se fark

## Repo me RMSNorm kahan lagta hai?

```python
class HybridBlock(nn.Module):
    def forward(self, x):
        x = x + self.attention(self.attention_norm(x))   # norm → attention → jodo
        ffn, usage = self.moe(self.ffn_norm(x))          # norm → MoE
        return x + ffn, usage                            # jodo
```

Har block me **2** RMSNorm hain, plus end me **1** `final_norm`:
- 12 blocks × 2 + 1 = **25 RMSNorms**
- Total params: 25 × 192 = **4,800** (25.7M ka 0.02%). Bahut sasta, lekin bahut zaroori.

## Pre-norm vs Post-norm

| | Post-norm (2017 Transformer) | **Pre-norm (aaj ka standard)** |
|---|---|---|
| Formula | `x = norm(x + f(x))` | `x = x + f(norm(x))` |
| Norm kahan | Jodne ke **baad** | Layer ke input pe, jodne se **pehle** |
| Residual path | Har baar normalize hota hai | **Saaf** rehta hai, koi rok-tok nahi |
| Deep models me training | Mushkil, warmup chahiye | Stable |

**Pre-norm kyun jeeta?** Residual connection (`x + ...`) ek "highway" hai jisse information aur gradient seedha neeche-upar ja sakte hain. Pre-norm is highway ko chhoota nahi, sirf layer ko saaf (normalized) input deta hai.

### Ek honest baat (lab Exp 3 me dikhega)

Pre-norm me residual stream (`x`) khud normalize nahi hota, isliye uska size dheere-dheere badhta hai: lab me 1.67 → 9.94 tak, 48 layers me. Ye **explode nahi hai** (bina norm ke 10¹¹ tha). Aur `final_norm` isi wajah se hai: output head se pehle stream ko ek last baar clean kar deta hai.

## RMSNorm vs LayerNorm

LayerNorm purana (2016) aur thoda zyada kaam karne wala hai:

| | LayerNorm | RMSNorm |
|---|---|---|
| Mean subtract karta hai? | Haan (center karta hai) | **Nahi** |
| Scale karta hai? | Haan (std se) | Haan (RMS se) |
| Learnable params | γ aur β (bias) | sirf γ |
| Speed | Thoda slow | Thoda fast |
| Kaun use karta hai | BERT, GPT-2 | **Llama, Mistral, Qwen, DeepSeek, GLM** |

Lab Exp 4: `[5, 6, 7, 8]` ke saath
- LayerNorm → `[-1.34, -0.45, 0.45, 1.34]` (mean 0 ho gaya)
- RMSNorm → `[0.76, 0.91, 1.06, 1.21]` (sirf scale hua, sab positive rahe)

**Research finding (Zhang & Sennrich, 2019):** Mean hatane wala step zyada zaroori nahi tha. Scale control karna hi asli kaam karta hai. Isliye ~7–64% kam compute me same quality milti hai.

> **Research lesson:** Kisi purane component ka ek-ek hissa hata ke dekho ki kya sach me zaroori hai. Isko **ablation** kehte hain. RMSNorm ek ablation ka hi result hai.

---
🎬 **Video:** 14:27–15:07 · 📁 `model.py` → `HybridBlock`, `GLM53FlashFromScratch.final_norm`

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [02 · Definitions — RMS, epsilon, gamma](02-definitions-formula.md) | 📚 [Topic 03 overview](README.md) | [04 · Real-life — Normalization har jagah hai](04-real-life.md) ➡️ |
<!-- /nav:bottom -->
