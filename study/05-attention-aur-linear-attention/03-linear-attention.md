# 03 · Practical — Linear attention: brackets badlo, T² hatao

## Trick: matrix multiplication me brackets

Softmax hata do (thodi der ke liye) to attention hai:
```
(Q Kᵀ) V          ← pehle [T×T] banta hai  → T² kaam
Q (Kᵀ V)          ← pehle [d×d] banta hai  → T·d² kaam
```

Matrix multiplication **associative** hai, to dono ka jawab same hai! Lekin doosre me T × T matrix kabhi banti hi nahi.

## Lekin softmax ka kya?

Softmax brackets todne nahi deta, kyunki `exp(q·k)` ko alag-alag nahi tod sakte. Solution: softmax ki jagah ek **feature map φ** lagao jo hamesha positive ho:

```python
q = F.elu(q) + 1.0      # φ(q) > 0
k = F.elu(k) + 1.0      # φ(k) > 0
```

Positive kyun? Kyunki weights negative nahi hone chahiye ("−20% suno" ka koi matlab nahi), aur denominator zero nahi hona chahiye.

## Running memory: S

Causal version me token t sirf 1..t dekh sakta hai:

```
S_t = S_{t-1} + φ(k_t) v_tᵀ        ← [d × d] memory me naya token jodo
z_t = z_{t-1} + φ(k_t)             ← normaliser (kitna total "weight" jud chuka)

output_t = φ(q_t) · S_t  /  φ(q_t) · z_t
```

- **S** ko slides "**running key–value state**" kehti hain
- Iska size hamesha `d × d = 32 × 32 = 1,024` hai, chahe 10 tokens hon ya 10 lakh

> Video: *"You have this state, like a matrix, that's like a memory of all of the tokens ... as they come they get fed into this state ... and it's always same size."*

## Repo ka code: parallel version (training ke liye)

```python
kv = torch.einsum("bthd,bthe->bthde", k, v).cumsum(dim=1)    # har t ka S_t
k_prefix = k.cumsum(dim=1)                                    # har t ka z_t
numerator   = torch.einsum("bthd,bthde->bthe", q, kv)         # φ(q)·S
denominator = torch.einsum("bthd,bthd->bth", q, k_prefix)     # φ(q)·z
output = numerator / denominator.clamp_min(1e-6)
```

`cumsum` = running total. Saare S_t ek saath ban jaate hain, jo GPU pe fast hai.

## Recurrent version (generation ke liye)

Generate karte waqt bas ek loop chalao: naya token aaya, S update karo, output nikalo. **Koi KV cache nahi**, sirf ek fixed S.

Lab Exp 2: parallel (cumsum) == recurrent (loop)? → **True** ✅
Ek hi math hai, bas do tarike se likha gaya hai: training ke liye parallel, inference ke liye recurrent. Isliye linear attention ko RNN/state-space model jaisa bhi kehte hain.

## Cost ki tulna

| | Softmax attention | Linear attention |
|---|---|---|
| Training compute | O(T²·d) | O(T·d²) |
| Generation memory | KV cache, T ke saath badhta hai | **Fixed** S (d²) |
| Har naye token ka kaam | O(T) | **O(1)** |
| Exact recall | ✅ Perfect | ❌ Lossy (next reading) |

Video: *"By my experience this trains a lot faster and inferences a lot faster ... That's why this is optimized for inference."*

---
🎬 **Video:** 18:38–20:25 · 📊 Slide 35 "Linear attention carries a running memory" · 📁 `model.py` lines 62–86
