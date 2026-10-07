<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 09 — Vision: image ko tokens me badalna](README.md) › Reading 6 / 6
<!-- /nav:top -->

# 06 · Recap + Quiz

## 5-line recap

1. Image ko **patches** me kaato (4×4 px). Har patch ek token hai (ViT idea).
2. Patches pe **bidirectional** vision transformer chalta hai, kyunki image me "pehle/baad" nahi hota.
3. **2×2 merge** se 64 → 16 tokens bante hain, aur **projector** unhe language model ki dim me badalta hai.
4. Sequence: `<BOS> <img_start> <image>×16 <img_end> text`. Placeholders ki jagah visual vectors **scatter** hote hain, aur baaki sab normal LM hai.
5. Is chhoti setting me simple baseline ne "faithful" path ko har seed pe haraya. Negative results aur multiple seeds dono important hain.

## Quiz

1. 64×64 image, patch size 8. Kitne patches? 2×2 merge ke baad kitne tokens?
2. Vision attention causal kyun nahi hota?
3. Vision model me vocab size 263 kyun hai?
4. `masked_scatter` kya karta hai?
5. Vision training me loss sirf answer digit pe kyun lagta hai?
6. Projector ki zaroorat kyun hai?
7. Faithful path baseline se kyun haara? Do possible reasons batao.
8. **Research soch:** "Kya model digit ki *shape* pehchanta hai, ya sirf *rang*?" Ise test karne ke liye ek experiment design karo.

---

<details>
<summary>👉 Jawab</summary>

1. 64/8 = 8, to 8×8 = **64 patches**. 2×2 merge ke baad 4×4 = **16 tokens**.
2. Image me koi time order nahi hai. Har patch ko poori image dekhni chahiye, upar-neeche, baaye-daaye sab. Causal mask bekaar ki rok hoti.
3. 260 (256 bytes + 4 special) + 3 image IDs (`<img_start>` 260, `<image>` 261, `<img_end>` 262) = **263**
4. Placeholder positions (ID 261) pe embedding vectors ko visual vectors se **replace** karta hai, aur baaki positions ko chhoota nahi.
5. Hum chahte hain ki model image se digit pehchane. "Digit: " predict karna faaltu kaam hai jo gradient ka hissa kha jaata.
6. Vision encoder ki width (24) aur LM ki dim (32) alag hai. Projector dono ko jodne wala "translator" hai, jo shape aur "meaning-space" dono match karta hai.
7. (a) 120 steps me extra layers (transformer + merger + projector) ko train hone ka time nahi mila. (b) Task itna aasaan hai ki seedha 8×8 patch projection kaafi hai, aur zyada structure bas optimization mushkil karta hai. (c) Chhoti width (24) pe vision transformer kamzor hai.
8. Ek **control** test set banao jisme har digit ka rang training se ulta ho (jaise "3" hamesha laal tha, ab neela), ya sab digits ek hi rang ke hon. Agar accuracy same rahe, to model shape pehchanta hai. Agar gir jaaye, to wo rang pe nirbhar tha. *(Repo me rang random hai, to ye risk kam hai. Lekin ye check karna hi research hai.)*

</details>

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [05 · Code Lab — `lab_vision.py`](05-lab-guide.md) | 📚 [Topic 09 overview](README.md) | [Topic 10 — Pretraining loop: random weights se Python tak](../10-pretraining-loop/README.md) ➡️ |
<!-- /nav:bottom -->
