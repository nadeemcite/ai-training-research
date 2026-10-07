# 02 · Definitions — Q, K, V, heads, aur T² problem

## Definitions

| Term | Matlab | Hamare model me |
|---|---|---|
| **Query / Key / Value** | Har token ke 3 projections: dhoondhna / label / content | `qkv = Linear(192, 576)` |
| **Score** | `q · k / √d`. Dot product, √d se scale kiya taaki softmax saturate na ho | |
| **Attention weights** | Scores pe softmax. Har query ke liye sum = 1 | |
| **Causal mask** | Future positions ka score `−∞`, taaki softmax ke baad weight 0 ho | |
| **Head** | Attention ki ek independent "copy". Har head alag cheez dhoondh sakta hai | 6 heads × 32 dims |
| **Softmax attention** | Classic version jisme har query har key se score nikalta hai | Topic 06 ka sparse isi ka variant hai |

## Formula (classic softmax attention)

```
Attention(Q, K, V) = softmax( Q Kᵀ / √d  +  mask ) · V
                              └── [T × T] ──┘
```

## Multi-head kyun?

Ek head shayad "pichla token kya tha" dekhe, doosra "matching bracket kahan hai", aur teesra "function ka naam kya tha". 192 dims ko 6 heads × 32 me baant ke **6 alag sawaal ek saath** poochte hain, fir results jod dete hain (`self.out`).

## 🚨 T² problem

`Q Kᵀ` ek **T × T** matrix hai, jisme har token ka har token ke saath score hota hai.

Lab Exp 3 (ek head, ek layer):

| Context T | Softmax scores (T²) | Linear state (d²) |
|---:|---:|---:|
| 192 | 36,864 | 1,024 |
| 8,000 | 64,000,000 | 1,024 |
| 128,000 | 16,384,000,000 | 1,024 |
| 1,000,000 | **1,000,000,000,000** | **1,024** |

GLM-5.3 ka context **1 million** tokens hai. T² ka matlab hai ek head, ek layer me 10¹² scores, jo practically impossible hai.

## Generation me bhi problem: KV cache

Generate karte waqt har naya token pichle **saare** tokens ke K aur V dekhta hai. Isliye unhe memory me rakhna padta hai, jise **KV cache** kehte hain.
- Cache T ke saath **badhta** jaata hai
- Har naya token T operations karta hai, to poore generation me T² kaam hota hai

> Video: *"Attention ... compute scales with sequence length"*, aur linear attention ka fayda: *"as context grows, sequence length grows, this state stays fixed."*

## Iska solution?

Do raaste hain (GLM-5.3 dono use karta hai):
1. **Linear attention** → T² matrix banao hi mat (next reading)
2. **Sparse attention** → sirf kuch chune hue tokens dekho (Topic 06)

---
🎬 **Video:** 17:04–17:48 (compute scaling) · 19:55–20:25 (running state)
