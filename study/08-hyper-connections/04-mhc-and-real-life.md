<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 08 — Hyper-connections: ek highway ki jagah 4 lanes](README.md) › Reading 4 / 6
<!-- /nav:top -->

# 04 · mHC ka constraint, asli result + Real-life

## "Manifold constraint" kyun chahiye?

Original Hyper-Connections me streams ke beech ek **free 4×4 mixing matrix** hoti thi. Problem ye hai ki 12 (ya 60) layers ke matrices **multiply** hote hain. Har matrix thoda sa bhi signal badhaye, to product explode kar jaata hai. Ye Topic 03 wali problem hai, ek naye roop me.

**DeepSeek ka fix (mHC):** Har mixing matrix ko **doubly stochastic** bana do (rows aur columns dono ka sum = 1), Sinkhorn-Knopp algorithm se:

```python
def sinkhorn(logits, iters=20):
    m = logits.exp()                              # sab positive
    for _ in range(iters):
        m = m / m.sum(dim=1, keepdim=True)        # rows sum = 1
        m = m / m.sum(dim=0, keepdim=True)        # columns sum = 1
    return m
```

**Kyun kaam karta hai?** Doubly stochastic matrices ka product bhi doubly stochastic hota hai. Wo sirf signal ko **mix** (redistribute) karte hain, kabhi badhate nahi. Isliye kitni bhi layers hon, signal ka total same rehta hai.

Lab Exp 5 (12 layers):

| Mixing | Signal size (shuru 2.00) |
|---|---:|
| Free matrix (I + 0.5·random) | **36.5** 💥 |
| Doubly stochastic (Sinkhorn) | **2.00** ✅ |

"Manifold" ka matlab: allowed matrices ek khaas "surface" (Birkhoff polytope) pe hain, aur training unhe usi surface pe rakhti hai.

## Asli sawaal: kya 4 streams madad karte hain? (lab Exp 6, `--run`)

2.2M model, 150 pretraining steps, held-out loss (kam = behtar). Maine experiment **do baar** chalaya:

| Seed | Run 1: 1 stream / 4 streams | Run 2: 1 stream / 4 streams |
|---:|---|---|
| 1 | 0.518 / 0.520 → 1 jeeta | 0.529 / 0.502 → 4 jeeta |
| 2 | 0.601 / 0.581 → 4 jeeta | 0.644 / 0.552 → 4 jeeta |
| 3 | 0.583 / 0.608 → 1 jeeta | 0.536 / 0.558 → 1 jeeta |

Same seeds, alag numbers! CPU pe threads ke beech floating-point math ka order badal sakta hai, aur seed 1 ka "winner" hi palat gaya.

**Imaandaar conclusion:** Is chhote setup me **koi saaf fark nahi** dikha. 3 seeds, direction badalti rahi, aur ek hi seed ka result run-to-run palat gaya. Topic 11 yaad karo: 3 seeds pe p kabhi 0.25 se neeche nahi ja sakta.

Aur Reading 03 ka quirk bhi dhyaan me rakho: repo me "1 stream" ek normal residual nahi hai, to ye comparison waise bhi saaf nahi hai.

**Possible reasons:** sirf 4 layers hain (deep models me fayda zyada hona chahiye), training chhoti hai, aur mHC ka asli matrix mixing yahan hai hi nahi.

---

## Real-life analogy 1: Expressway ki lanes 🛣️

- **Bina residual** = har toll pe gaadi se saara saamaan utaar ke naye truck me bharna. 12 tolls ke baad aadha saamaan gum.
- **Residual** = ek expressway jahan saamaan chalta rehta hai, aur har toll pe bas kuch naya **joda** jaata hai.
- **Hyper-connections (4 lanes)** = 4 lanes, har lane me alag type ka saamaan (jaise ek lane me "syntax", ek me "meaning"). Har exit (layer) decide karti hai ki kin lanes se saamaan uthana hai aur nayi delivery kis lane me daalni hai.
- **mHC constraint** = traffic rule: "lanes ke beech gaadiyan shift ho sakti hain, lekin highway pe gaadiyon ki **kul ginti** na badhe". Isse jam (explosion) nahi lagta.

## Real-life analogy 2: Office ki notebook 📒

Ek team ki ek common notebook hai (residual stream). Har member (layer) usme kuch jodta hai. Agar sab ek hi page pe likhein to bheed ho jaati hai. **4 alag sections** (streams) rakho: har member decide kare ki kaunse sections padhne hain aur kahan likhna hai. End me manager (output head) saare sections ka summary padhta hai.

---
🎬 **Video:** 11:56–13:27 · 📄 Papers: *Hyper-Connections* (ByteDance, 2024), *mHC* (DeepSeek, 2025)

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [03 · Practical — Repo ka code, aur ek quirk jo humne pakda](03-practical-repo-code.md) | 📚 [Topic 08 overview](README.md) | [05 · Code Lab — `lab_hyper_connections.py`](05-lab-guide.md) ➡️ |
<!-- /nav:bottom -->
