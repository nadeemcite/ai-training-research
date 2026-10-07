<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 02 — Embeddings, Output Head aur Weight Tying](README.md) › Reading 6 / 6
<!-- /nav:top -->

# 06 · Recap + Quiz

## 5-line recap

1. **Embedding** = token ID se ek seekha hua vector, jo `[260 × 192]` table me sirf ek row lookup hai.
2. Shapes ka flow hai `[B,T] → [B,T,192] → (layers) → [B,T,192] → [B,T,260]`.
3. **Output head** har token ka score (logit) deta hai. **Softmax** use probabilities me badalta hai, aur **cross-entropy** galti naapta hai.
4. **Weight tying** me embedding aur output head ek hi matrix hain. Isse params bachte hain aur geometry same rehti hai.
5. Tying tabhi kaam karta hai jab beech me layers ho. Bina layers ke model "same token repeat" ki taraf jhukta hai.

## Quiz

1. `nn.Embedding(260, 192)` me kitne parameters hain?
2. Input shape `[8, 100]` hai. Embedding ke baad aur output head ke baad shapes kya honge?
3. Lookup aur matrix multiplication me kya fark hai? Lookup kyun sasta hai?
4. Logits `[2.0, 2.0, 2.0]` hain. Softmax probabilities kya hongi?
5. Random 260-vocab model ka shuruaati loss lagbhag kitna hoga, aur kyun?
6. Greedy aur sampling me fark batao. RL me 16 attempts ke liye kaunsa chahiye?
7. Weight tying ke 2 fayde aur 1 limitation batao.
8. **Research soch:** 150k-vocab, `dim=4096` model me tying se kitne params bachenge? Kya ye total (7B) ka bada hissa hai?

---

<details>
<summary>👉 Jawab</summary>

1. 260 × 192 = **49,920**
2. `[8, 100, 192]` aur `[8, 100, 260]`
3. Lookup sirf ek row copy karta hai, koi multiply/add nahi hota. Mathematically ye one-hot vector × matrix ke barabar hai, lekin 260× sasta hai.
4. `[1/3, 1/3, 1/3]`. Sab barabar hain, kyunki softmax sirf *differences* pe depend karta hai.
5. ~`ln(260) ≈ 5.56`. Random model har token ko ~1/260 probability deta hai, aur `-log(1/260) = ln 260`.
6. Greedy hamesha top token chunta hai, isliye har baar same output deta hai. Sampling probability ke hisaab se random chunta hai. RL me **sampling** chahiye, kyunki 16 *alag* attempts chahiye jinhe compare kar sakein.
7. Fayde: parameter bachat aur same reading/predicting geometry. Limitation: bina beech ki layers ke, token apne aap ko predict karne ki taraf jhukta hai (`||e||²` bada hota hai).
8. 150,000 × 4096 ≈ **614M** params. 7B ka ~9% hai, to significant hai! Isliye kuch bade models tying use nahi bhi karte (ye trade-off hai).

</details>

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [05 · Code Lab — `lab_embeddings.py`](05-lab-guide.md) | 📚 [Topic 02 overview](README.md) | [Topic 03 — RMSNorm: numbers ko control me rakhna](../03-rmsnorm/README.md) ➡️ |
<!-- /nav:bottom -->
