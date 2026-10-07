<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 08 — Hyper-connections: ek highway ki jagah 4 lanes](README.md) › Reading 2 / 6
<!-- /nav:top -->

# 02 · Definitions — Streams, mix, route, mHC

| Term | Matlab | Hamare repo me |
|---|---|---|
| **Residual connection** | `x = x + f(x)`: layer ka output input me **joda** jaata hai | har block me |
| **Residual stream** | Wo vector jo layers ke beech aage chalta hai | `[B, T, 192]` |
| **Hyper-connection** | Residual stream ki **n copies**, learnable read/write ke saath | n = `streams = 4` |
| **Read / mix weights** | Block ke input ke liye 4 streams ka weighted average | `softmax(input_logits)` |
| **Write / route weights** | Block ka update har stream me kitna jode | `softmax(output_logits)` |
| **mHC** | Manifold-Constrained HC: streams ke beech mixing **matrix** pe constraint | released GLM me, repo me nahi |
| **Doubly stochastic matrix** | Saare entries ≥ 0, aur har row ka sum = 1 aur har column ka sum = 1 | — |
| **Sinkhorn-Knopp** | Kisi bhi positive matrix ko baar-baar row-normalize aur column-normalize karke doubly stochastic banana | lab Exp 5 |

## Shapes (lab Exp 3)

```
embedding            [1, 10, 192]
→ expand to streams  [1, 10, 4, 192]      ← 4 bilkul same copies se shuru
→ 12 HyperConnections                      ← har layer read-mix → block → write-route
→ streams.mean(dim=2) [1, 10, 192]
→ final_norm → output head
```

6 layers ke baad stream 0 aur stream 3 me **~19% fark** aa jaata hai, kyunki har stream ko update ka alag hissa milta hai.

## Read aur write weights (lab Exp 2)

```
read  = softmax([0.1, 0.033, -0.033, -0.1])  = [0.276, 0.258, 0.241, 0.226]   sum = 1
write = softmax([-0.1, -0.033, 0.033, 0.1])  = [0.226, 0.241, 0.258, 0.276]   sum = 1
```

Shuru me lagbhag barabar hain, lekin ulte tilt ke saath, taaki streams symmetric na rahein aur alag-alag cheezein seekh sakein. Training me ye 8 numbers per layer seekhe jaate hain. Poore model me ye sirf **12 × 8 = 96 parameters** hain!

## Repo vs released GLM-5.3

| | Released GLM-5.3 (mHC) | Hamara repo |
|---|---|---|
| Streams | 4 | 4 |
| Kahan lagta hai | Attention aur FFN **dono ke liye alag** HC (`attn_hc`, `ffn_hc`) | Ek HC poore block (attention + MoE) ko wrap karta hai |
| Streams ke beech mixing | 4×4 **matrix**, Sinkhorn se doubly stochastic | Sirf read vector + write vector (koi stream-to-stream matrix nahi) |
| Constraint | Haan (manifold) | Softmax (sum = 1) |

Slide 38 khud kehti hai: *"The miniature: one simpler hyperconnection wraps attention + MoE together."* Repo ka `REPORT.md` bhi likhta hai ki ye *"not exact implementations of mHC"* hai.

---
📁 `model.py` lines 191–207, 231–243 · 🎬 Video 11:56–13:27

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [01 · Concept — Residual highway, aur 4 lanes kyun](01-concept-residual-highway.md) | 📚 [Topic 08 overview](README.md) | [03 · Practical — Repo ka code, aur ek quirk jo humne pakda](03-practical-repo-code.md) ➡️ |
<!-- /nav:bottom -->
