<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 07 — Mixture of Experts (MoE)](README.md) › Reading 6 / 6
<!-- /nav:top -->

# 06 · Recap + Quiz

## 5-line recap

1. **MoE** = bahut saare chhote FFN experts, aur ek **router** har token ke liye **top-k** chunta hai. Hamara model: 2 of 8 + 1 shared. Released: 8 of 288 + 1 shared.
2. **Shared expert** common knowledge seekhta hai, taaki routed experts specialization pe dhyaan de sakein.
3. **Total params** bahut zyada (memory), lekin **active params** kam (compute). Hamare MoE me 33% active, aur GLM-5.3 me ~3%.
4. **Expert collapse:** router kuch hi experts ko chunne lagta hai. **Balance loss** (ya DeepSeek-V3 ka bias trick) isse rokta hai.
5. **Repo bug:** `usage` integer counts se banta hai, isliye balance loss ka gradient zero hai. "Loss me jodna" ≠ "kaam karna".

## Quiz

1. Dense FFN aur MoE me kya fark hai?
2. Router logits `[0.5, 2.0, -1.0, 1.0]`, top-2. Kaunse experts chune jaayenge aur unke gate weights kya honge? (approx)
3. Shared expert ka kaam kya hai?
4. Ek expert me 221,184 params hain. 8 routed + 1 shared, top-2. Ek layer ke total aur active params?
5. MoE model compute me sasta hai lekin memory me mehenga. Kyun?
6. Expert collapse kya hai aur kyun hota hai?
7. Repo ka balance loss router ko train kyun nahi karta?
8. **Research soch:** "Top-2 vs top-1 vs top-4, same total params." Hypothesis aur experiment design karo. Kya-kya measure karoge?

---

<details>
<summary>👉 Jawab</summary>

1. Dense me **har token poore FFN** se guzarta hai. MoE me bahut saare chhote experts hain aur har token **sirf k** chune hue (plus shared) se guzarta hai.
2. Top-2 = **E2 (2.0)** aur **E4 (1.0)**. softmax([2.0, 1.0]) ≈ **[0.73, 0.27]**
3. Wo knowledge seekhna jo har token ko chahiye (grammar, common patterns), taaki routed experts use duplicate na karein aur specialize kar sakein.
4. Total = 9 × 221,184 = **1,990,656**. Active = 3 × 221,184 = **663,552**
5. Har token sirf kuch experts chalata hai (kam FLOPs), lekin saare experts memory me hone chahiye, kyunki pata nahi agla token kise chunega.
6. Router kuch experts ko zyada chunta hai → wo zyada train hote hain → aur zyada chune jaate hain. Baaki experts ko data nahi milta, wo bekaar rehte hain ("rich get richer").
7. `usage` = `positions.numel()` jaise integer counts se banta hai, jinka koi gradient nahi hota (`requires_grad=False`). Balance term loss me ek constant ki tarah judta hai.
8. Hypothesis: "Top-1 sabse sasta hai lekin quality kam hogi. Top-4 thoda better hoga lekin 2× compute lega." Same experts/params/data/steps rakho, sirf top_k badlo. Measure karo: pretraining loss, dev pass-rate, **training time/FLOPs**, aur expert usage balance. 3+ seeds pe chalao. Quality per compute ka graph banao, sirf quality nahi.

</details>

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [05 · Code Lab — `lab_moe.py`](05-lab-guide.md) | 📚 [Topic 07 overview](README.md) | [Course home](../README.md) 🏁 *(agle topics jald aa rahe hain)* |
<!-- /nav:bottom -->
