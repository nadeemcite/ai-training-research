# 04 · Hybrid rhythm (3:1) + Real-life

## Code: ek expression, poora rhythm

```python
self.layers = nn.ModuleList([
    HyperConnection(config, HybridBlock(config, sparse=((index + 1) % 4 == 0)))
    for index in range(config.layers)
])
```

| index | 0 | 1 | 2 | **3** | 4 | 5 | 6 | **7** | 8 | 9 | 10 | **11** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| (index+1) % 4 | 1 | 2 | 3 | **0** | 1 | 2 | 3 | **0** | 1 | 2 | 3 | **0** |
| Type | L | L | L | **S** | L | L | L | **S** | L | L | L | **S** |

> Video: *"You're just going to take every fourth layer and set it a sparse attention."*

Lab Exp 5 aur TODO (c) me repo model se verify kiya: `['LinearAttention', 'LinearAttention', 'LinearAttention', 'SparseAttention', ...]` ✅

## 3:1 kyun?

| Layer type | Kaam | Cost |
|---|---|---|
| **Linear** (75%) | Recent context ko sasta compress karke aage le jaana | O(T), fixed state |
| **Sparse** (25%) | Har kuch layers baad exact door ki details wapas laana | T × (chuni keys) |

Agar sab sparse hota → mehenga. Agar sab linear hota → lossy, exact recall kharab (Topic 05, Exp 4).

3:1 ek **empirical** choice hai, yaani experiments se nikla, koi theorem nahi. Kimi Linear (Moonshot AI, 2025) bhi 3 linear (KDA) : 1 full attention use karta hai. Ye number aaj research ka active sawaal hai.

> **Research question:** 3:1 ki jagah 2:1 ya 5:1? Ya sparse layers shuru me rakhein vs end me? Ye sab CPU pe testable hai, sirf `(index + 1) % 4` badalna hai!

## Kahan pe lagi hai sparse layer? Last me kyun?

Hamare pattern me layer 12 (aakhri) sparse hai. Intuition: output head se theek pehle model ek baar exact context check kar leta hai. Lekin ye bhi ek design choice hai, isko test kar sakte ho.

---

## Real-life analogy 1: Lambi kitaab padhna 📖

Tum ek 500-page novel padh rahe ho:
- **Linear = dimaag me chalti summary.** "Ab tak hero gaon chhod ke sheher aaya, villain ne dhokha diya..." Ye sasta hai aur hamesha saath hai, lekin details dhundhli hain.
- **Sparse = kabhi-kabhi peeche palatna.** "Ruko, chapter 3 me us letter me exact kya likha tha?" Tum **pichle 2 page** (local window) aur **har chapter ka pehla page** (anchors) jaldi se dekh lete ho.
- **Indexer = index/search.** Kitaab ke end me index dekha, "letter → page 47", aur seedha wahi khola.

**3:1 rhythm** = 3 chapter summary pe chalo, fir ek baar peeche jhaank lo.

## Real-life analogy 2: Google Maps 🗺️

Navigation ke time:
- **Local window** = aas-paas ki galiyan detail me
- **Anchors** = har 10 km pe ek bada landmark/exit
- Poore India ki har gali ek saath load nahi hoti (full attention), wo impossible hai

## Real-life analogy 3: CCTV security guard 📹

Guard 100 cameras ek saath nahi dekhta:
- Apne gate ka camera hamesha (local)
- Baaki cameras round-robin me, har kuch second (anchors)
- **Motion alert** wale camera ko turant (indexer = content-based)

---
🎬 **Video:** 18:38–20:00 · 📊 Slides 32–34 "Our 12 layers: 3 linear + 1 sparse"
