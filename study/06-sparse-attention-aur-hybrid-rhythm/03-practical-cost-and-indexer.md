# 03 · Practical — Kitna sasta? Fixed vs Indexer

## Lab Exp 2: Kitne (query, key) pairs? (repo config: W=32, S=32)

| Context T | Full causal | Sparse (window + anchors) | % |
|---:|---:|---:|---:|
| 192 | 18,528 | 6,128 | 33.1% |
| 4,096 | 8,390,656 | 390,672 | 4.7% |
| 131,072 | 8,590,000,128 | 272,694,800 | **3.2%** |

Bahut bachat hai! Lekin dhyaan do: 3.2% pe bhi **ruk nahi raha**.

### Kyun? Anchors badhte jaate hain

Position t pe anchors = `t / 32`. Position 100,000 pe ~3,000 anchors hain. To cost abhi bhi **T²/32** hai, matlab quadratic hi hai, bas 32× sasta.

### Indexer ka fayda: fixed k

Indexer har query ke liye hamesha **k** tokens chunta hai (jaise 2,048), chahe T kitna bhi bada ho:
```
Main attention cost:  T × k        ← linear in T!
Indexer cost:         T × T × (bahut chhota)
```

Video: *"The attention size is always fixed, it doesn't scale, but the indexer scales with the sequence length ... a lot less compute because this sparse indexer is a lot lighter."*

Indexer abhi bhi T² hai, lekin itna halka hai ki practically chalta hai.

## Lab Exp 3: Sanity check ✅

```
window = T  : sparse == full?  True
window = 3  : sparse == full?  False
```

Agar window poora context cover kare, to sparse attention **exactly** normal attention ban jaata hai. Ye ek accha **unit test** hai: naya attention likho to pehle check karo ki edge case me wo known-correct cheez se match karta hai.

> **Research habit:** Repo ke `tests/test_lab.py` me bhi "causal outputs", "3:1 rhythm" jaise checks hain (slide 42 "Prove the model is wired correctly"). Experiment se pehle wiring prove karo.

## Lab Exp 4: Needle dhoondho 🪡

64 tokens hain. Position 37 pe ek "needle" hai jiska key query se strongly match karta hai.

```
fixed pattern  (12 keys): [0, 16, 32, 48, 56, ..., 63]  → needle mila? False
indexer top-8  ( 8 keys): [0, 3, 6, 15, 18, 37, 43, 63] → needle mila? True
```

- Fixed pattern ne **zyada** keys dekhi (12), phir bhi miss kiya, kyunki 37 na window me tha, na anchor.
- Indexer ne **kam** keys dekhi (8), lekin sahi wali, kyunki usne content dekha.
- Indexer ne bhi kuch faltu tokens chune (0, 3, 6...), kyunki sirf 4 dims se ranking noisy hoti hai. Koi baat nahi, final attention unhe kam weight dega.

## Code me iska matlab

`return x + 1` ke liye prompt me "plus one" 40 tokens peeche ho sakta hai. Fixed pattern me wo sirf luck se (anchor pe pada to) dikhega. Isliye:
1. Linear layers us info ko compressed form me aage le aati hain
2. Multiple layers milke info ko "hop" karwa sakti hain: layer 4 me anchor tak info pahunchi, aur layer 8 me anchor se current token tak

Hamare chhote 192-token context me ye kaafi hai. 1M tokens pe indexer zaroori ho jaata hai.

---
🎬 **Video:** 17:04–17:48 · 📊 Slides 36, 42
