<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 08 — Hyper-connections: ek highway ki jagah 4 lanes](README.md) › Reading 5 / 6
<!-- /nav:top -->

# 05 · Code Lab — `lab_hyper_connections.py`

## Run

```bash
uv run study/08-hyper-connections/lab_hyper_connections.py          # ~3 sec
uv run study/08-hyper-connections/lab_hyper_connections.py --run    # + ~4 min (1 vs 4 streams training)
```

Repo ka asli `HyperConnection` aur `HybridBlock` import hote hain.

## Expected output (aur matlab)

```
Exp 1  12 layers ke baad input se similarity:  bina residual -0.050   residual ke saath +0.636
```
→ Residual highway information bachata hai (Reading 01).

```
Exp 2  shuruaati weights (seekhe jaate hain):
       read  (kis stream se kitna padhna):   [0.276, 0.258, 0.241, 0.226]  sum = 1.0
       write (update kis stream me kitna):  [0.226, 0.241, 0.258, 0.276]  sum = 1.0
```
→ Read/write weights (Reading 02).

```
Exp 3  embedding (1, 10, 192) -> streams (1, 10, 4, 192)  [batch, tokens, STREAMS, dim]
       shuru me 4 streams bilkul same? True
       6 layers ke baad stream 0 vs 3 ka fark: 18.6%  (write weights alag hain, isliye streams alag ho jaate hain)
       end me: streams.mean(dim=2) -> (1, 10, 192) -> final_norm -> output head
```
→ Shapes (Reading 02).

```
Exp 4  streams=1: output == x + block(x), jahan block(x) = x + attn + MoE  ->  2x + ...?  True
       streams=1: 12 layers ke baad residual stream ka size 7,459.7x (init pe)
       streams=4: 12 layers ke baad residual stream ka size 19.1x (init pe)
```
→ **Repo ka quirk** (Reading 03): identity do baar judti hai.

```
Exp 5  12 layers ke baad stream signal ka size:  free matrix 36.5   doubly-stochastic 2.00  (shuru: 2.00)
```
→ mHC constraint kyun (Reading 04).

`--run` ke saath Exp 6 (~4 min). Maine **do baar** chalaya aur numbers alag aaye:
```
Run 1:  seed 1: 1 stream 0.5177 / 4 streams 0.5196 -> 1 jeeta    Run 2:  seed 1: 0.5294 / 0.5016 -> 4 jeeta
        seed 2: 1 stream 0.6013 / 4 streams 0.5809 -> 4 jeeta            seed 2: 0.6437 / 0.5519 -> 4 jeeta
        seed 3: 1 stream 0.5827 / 4 streams 0.6081 -> 1 jeeta            seed 3: 0.5360 / 0.5583 -> 1 jeeta
```
→ Koi saaf winner nahi (Reading 04). Aur **same seed, alag numbers**: CPU pe multi-threaded floating-point math ka order har run me thoda badal sakta hai (khaas kar jab doosre programs bhi chal rahe hon). Tumhare numbers bhi thode alag aayenge. Isliye ek run ke chhote fark pe kabhi bharosa mat karo.

## Tumhara kaam (10 min)

1. **TODO (a):** Exp 1 me `std=0.02` ko `0.2` karo. Residual wali similarity kya hui? (Hint: bade updates highway ko bhi dhak dete hain.)
2. **TODO (b):** Exp 5 ke baad `ds.sum(dim=0)` aur `ds.sum(dim=1)` print karo. Kya dono me sab ~1 hain?
3. **TODO (c):** Exp 6 ke basis pe ek imaandaar line likho: "Is setup me 4 streams ___".
4. **Bonus:** Reading 03 ka fix (`update = transformed - mixed`) `HyperConnection` ki ek copy me lagao aur Exp 4 dobara chalao. Ab stream kitna badhta hai?

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [04 · mHC ka constraint, asli result + Real-life](04-mhc-and-real-life.md) | 📚 [Topic 08 overview](README.md) | [06 · Recap + Quiz](06-recap-quiz.md) ➡️ |
<!-- /nav:bottom -->
