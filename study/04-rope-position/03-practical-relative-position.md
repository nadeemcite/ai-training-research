# 03 · Practical — Score sirf **doori** pe depend karta hai

## RoPE ka sabse important property

Query position `m` pe hai aur key position `n` pe. Rotation ke baad:
```
score = rotate(q, m·θ) · rotate(k, n·θ)
      = q · rotate(k, (n − m)·θ)          ← sirf (m − n) bacha!
```

Intuition: Dono vectors ko ek saath kitna bhi ghumao, unke **beech ka angle** same rehta hai. Aur dot product sirf beech ke angle pe depend karta hai.

## Lab Exp 3 ka proof

Same `q` aur `k` vectors, alag-alag positions pe:

| Query pos | Key pos | Doori | Score |
|---:|---:|---:|---:|
| 5 | 3 | 2 | **+0.1496** |
| 105 | 103 | 2 | **+0.1496** |
| 1005 | 1003 | 2 | **+0.1495** |
| 5 | 1 | 4 | −2.3298 |

Doori 2 hai to score same aata hai, chahe tokens shuru me hon ya 1000 tokens baad. Doori badli to score bhi badal gaya.

(1005 pe chhota sa 0.0001 ka fark float32 rounding ki wajah se hai, math me exact same hai.)

## Iska fayda kya hai?

1. **Patterns kahin bhi kaam karte hain.** `return x + 1` me "`+` ke 2 token baad number aata hai" wala pattern line 1 pe seekha to line 50 pe bhi lagu hoga.
2. **Relative position natural hai.** Language me "pichla word" absolute "word number 347" se zyada important hai.
3. **Koi extra parameter nahi.** RoPE me seekhne ko kuch nahi hai, sirf fixed math hai. 0 params.

## Ek limitation: lambe context

Training me model ne max 192 positions dekhi hain. Agar 10,000 tokens de do, to dheeme pairs aise angles pe pahunch jaate hain jo model ne kabhi dekhe hi nahi, aur quality gir jaati hai.

Real labs ke solutions:
- **Base badhao:** Llama 3 `500,000` use karta hai (10,000 ki jagah), taaki dheeme pairs aur dheeme hon. Lab TODO (b) me try karo.
- **Context extension tricks:** YaRN, NTK-scaling (advanced, abhi skip)

## Repo me RoPE kahan lagta hai?

```python
# LinearAttention.forward
q, k = apply_rope(q, k)
q = F.elu(q) + 1.0      # RoPE ke BAAD feature map
k = F.elu(k) + 1.0

# SparseAttention.forward
q, k = apply_rope(q, k)
```

Dono attention types me lagta hai. Ek subtle baat: linear attention me RoPE ke baad `elu+1` lagta hai, jo upar wali "sirf doori" property ko exactly nahi rakhta. Ye teaching model ka simplification hai. (Ek accha research sawaal: kya isse fark padta hai?)

---
🎬 **Video:** 15:25–15:55 · 📊 Slide 30
