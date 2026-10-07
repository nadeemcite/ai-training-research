<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 04 — RoPE: model ko position kaise pata chalti hai](README.md) › Reading 6 / 6
<!-- /nav:top -->

# 06 · Recap + Quiz

## 5-line recap

1. Attention dot product se chalta hai, jo **order nahi jaanta**. Bina position info ke `x - 1` = `1 - x`.
2. **RoPE** query aur key ko position ke hisaab se **rotate** karta hai. Value ko nahi chhoota, aur 0 params hain.
3. Vector ko **16 pairs** me toda jaata hai, aur har pair ki apni **frequency** hai (tez → dheemi, jaise ghadi ki suiyan).
4. Rotate ke baad score sirf **doori (m − n)** pe depend karta hai, isliye patterns kisi bhi position pe kaam karte hain.
5. Released GLM main attention me **NoPE** aur indexer me RoPE use karta hai. Hamara model simplicity ke liye har jagah RoPE lagata hai.

## Quiz

1. RoPE q, k, v me se kise rotate karta hai, aur kyun?
2. Head dimension 32 hai. RoPE kitne pairs banata hai?
3. Rotation ke baad vector ki length kitni badalti hai?
4. Query pos 10, key pos 7 ka score aur query pos 510, key pos 507 ka score: same ya alag? Kyun?
5. Pair 0 aur pair 15 me se kaun paas ke tokens me fark karne ke liye zyada useful hai?
6. GPT-2 ka learned absolute position embedding lambe context pe kyun fail hota hai?
7. NoPE (koi position encoding nahi) wala model bhi position ka andaaza kaise laga leta hai?
8. **Research soch:** "Hamare teaching model me linear attention se RoPE hata do (sirf sparse me rakho)." Hypothesis kya hai, aur kya measure karoge?

---

<details>
<summary>👉 Jawab</summary>

1. Sirf **q aur k**, kyunki attention score inke dot product se banta hai. v sirf content carry karta hai, to use position ki zaroorat nahi.
2. 32 / 2 = **16** pairs
3. **Bilkul nahi.** Rotation length-preserving hai.
4. **Same.** Dono me doori 3 hai, aur RoPE score sirf doori pe depend karta hai.
5. **Pair 0** (tez). 1 token ke fark pe hi 1 radian ghoom jaata hai. Pair 15 itna dheema hai ki paas ke tokens me lagbhag fark nahi dikhta.
6. Har position ka vector *seekha* jaata hai. Position 5000 training me kabhi aayi hi nahi, to uska vector random/untrained rehta hai.
7. **Causal mask** se. Token t sirf t tokens dekh sakta hai, aur ye count/asymmetry indirectly position batati hai.
8. Hypothesis: "Linear layers recent context ko compress karti hain. Shayad unhe position ki zaroorat nahi, aur sparse layers ka RoPE kaafi hai." Measure karo: pretraining loss, aur dev par order-sensitive tasks (jaise `x - 1` vs `1 - x`) ka pass-rate. Baaki sab same rakho aur 3+ seeds pe chalao.

</details>

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [05 · Code Lab — `lab_rope.py`](05-lab-guide.md) | 📚 [Topic 04 overview](README.md) | [Topic 05 — Attention basics → Linear attention](../05-attention-aur-linear-attention/README.md) ➡️ |
<!-- /nav:bottom -->
