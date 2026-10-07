# 04 · Trade-off — Compressed memory ki keemat

## Free lunch nahi hota

1 million tokens ki info **1,024 numbers** me? Kuch na kuch to khoyega.

> Video: *"The trade-off is you lose some information because you are compressing it."*

## Lab Exp 4: Recall test

N (key, value) pairs store karo, fir key_i se poocho: "value_i wapas do".

| Pairs | Softmax recall | Linear recall (repo jaisa, φ = elu+1) |
|---:|---:|---:|
| 4 | 100% | 50% |
| 16 | 100% | 19% |
| 64 | 100% | 2% |

Softmax har cheez exact yaad rakhta hai, kyunki uske paas poori KV list hai. Linear attention jaldi "dhundhla" ho jaata hai.

## Lab Exp 6: Asli bottleneck kahan hai? 🔍

Same `[d × d]` memory, lekin φ (elu+1) aur denominator hata do:

| Pairs | Raw memory recall (d=32) |
|---:|---:|
| 4 | 100% |
| 16 | 100% |
| 64 | 83% |

**Bada fark!** Problem sirf memory ka size nahi hai, balki **φ = elu+1** bhi hai. Wo saare keys ko positive bana deta hai, to sab keys ek-doosre jaise dikhne lagte hain aur memory me "ghul-mil" jaate hain.

Isliye modern linear attentions (DeltaNet, **KDA = Kimi Delta Attention**, jo video me mention hai) smarter update rules use karte hain. Ye 2024–25 ka active research area hai.

> **Research lesson:** Jab koi cheez kaam na kare, to ek-ek component hata ke dekho ki asli culprit kaun hai. Exp 4 vs Exp 6 yahi hai.

## Decay: purana bhoolo, naya yaad rakho

Video kehta hai: *"linears are going to remember recent tokens ... the further away a token is, the more it's been messed up by the newer tokens."*

Real models (KDA, Mamba) me ek **decay/forget gate** hota hai:
```
S_t = γ · S_{t-1} + φ(k_t) v_tᵀ          γ < 1  → purani yaadein dheere fade
```

Lab Exp 5 (γ = 0.8, 32 pairs): `······························✓✓`. Sirf sabse naye 2 yaad rahe.

⚠️ **Honest note:** Repo ka `LinearAttention` me **koi decay nahi** hai (γ = 1, plain `cumsum`). Wo sab tokens ko barabar weight deta hai, lekin "dhundhla" karke. Video ka "recent yaad rehta hai" wala point KDA jaise gated versions pe zyada lagu hota hai.

## Real-life analogy: WhatsApp group vs Diary 📱📓

**Softmax attention = poora WhatsApp chat scroll karna.** Har sawaal pe tum poori history padhte ho. Exact hai, lekin 10 saal ki chat me bahut slow.

**Linear attention = ek diary jisme roz ek paragraph summary likhte ho.** Diary ka size fixed hai (ek page). Har din naye events jodte ho aur purani baatein us page pe "overwrite/ghul" jaati hain.
- Sawaal ka jawab turant mil jaata hai, sirf ek page padhna hai
- Lekin "3 saal pehle Tuesday ko kisne kya bola tha" exact nahi milega

**Decay = "is hafte ki baatein bold me, purani halki pencil me."**

**GLM ka hybrid = diary roz use karo, lekin har kuch din me ek baar asli chat bhi check karo.** Yahi Topic 06 hai: 3 linear + 1 sparse.

---
🎬 **Video:** 18:38–19:40 · 📊 Slide 35
