# 04 · Weight Tying — ek matrix, do kaam

## Observation

| Layer | Shape | Kaam |
|---|---|---|
| Embedding | `[260, 192]` | Token ID → vector (**padhna**) |
| Output head | `[260, 192]` | Vector → har token ka score (**likhna**) |

Dono ka shape **same** hai! To kya ek hi matrix dono kaam kar sakta hai?

## Haan, aur yahi weight tying hai

Repo me sirf ek line hai:
```python
self.output.weight = self.embedding.weight     # model.py, line 223
```
Ab dono **same memory** point karte hain. Ek update hoga to dono update honge.

Maine verify kiya: `m.output.weight is m.embedding.weight → True` ✅

## Fayde

1. **Parameter bachat:** `260 × 192 = 49,920` params bache. Hamare model me ye chhota hai, lekin 150k-vocab BPE model me ye **lakhon-croron** params hote hain.
2. **Same "geometry":** Video me Vuk bolte hain: *"makes reading and predicting bytes use the same learned geometry"*. Matlab jis vector se `+` padha jaata hai, usi se `+` predict bhi hota hai. Ek token ka ek hi meaning hota hai.
3. **Purana idea hai:** Press & Wolf (2017) aur original Transformer paper me bhi tha. GPT-2 bhi use karta tha.

## ⚠️ Chhupi limitation (lab me khud dekhoge)

Tied model me score aisa banta hai:
```
logit[j] = hidden · embedding[j]
```

Agar beech me koi layer na ho (`hidden = embedding[i]`), to:
```
logit[i → i] = embedding[i] · embedding[i] = ||embedding[i]||²   ← hamesha bada!
```

Har vector apne aap se sabse zyada "match" karta hai. Isliye **sirf embedding + tied head** wala bigram model bolta hai ki "`r` ke baad `r` aayega", jabki training data me `rr` kahin nahi hai!

Lab ka asli output:
```
tied=False  loss 0.789  'r' ke baad: [('n', 0.5), ('e', 0.5), ...]   ✅ sahi
tied=True   loss 1.921  'r' ke baad: [('r', 0.3), (' ', 0.14), ...] ❌ galat
```

### To real model me tying kaam kyun karta hai?

Kyunki embedding aur output head ke beech **12 transformer layers** hain. Wo `hidden` vector ko transform karti hain, taaki wo "abhi wala token" nahi balki "**agla token**" represent kare. Layers ka asli kaam yahi conversion hai.

> **Research lesson:** Ek trick (tying) jo bade model me helpful hai, wo toy setup me nuksaan kar sakti hai. Hamesha check karo ki tumhara toy experiment asli setting ka sahi chhota version hai ya nahi.

## Real-life analogy

Ek hi **dictionary** se tum English → Hindi bhi dekhte ho aur Hindi → English bhi. Do alag dictionary rakhne ki zaroorat nahi, aur dono directions me meaning consistent rehta hai.

## Research question (khud socho)
> *"25M model me tying hata dein to kya pretraining loss better hoga ya worse? Kitne seeds pe check karna padega?"*

---
🎬 **Video:** 13:50–14:27 aur 22:28–23:00 · 📊 Slide 41 "The input and output share one matrix"
