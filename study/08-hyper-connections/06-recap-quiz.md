<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 08 — Hyper-connections: ek highway ki jagah 4 lanes](README.md) › Reading 6 / 6
<!-- /nav:top -->

# 06 · Recap + Quiz

## 5-line recap

1. **Residual** (`x + f(x)`) ek highway hai jo information aur gradients ko layers ke paar le jaata hai.
2. **Hyper-connections** is highway ko **n lanes (streams)** me todte hain. Har layer seekhti hai ki kya **padhna** (mix) hai aur kahan **likhna** (route) hai. End me lanes ka average hota hai.
3. **mHC** streams ke beech mixing matrices ko **doubly stochastic** (Sinkhorn) rakhta hai, taaki deep model me signal explode na ho.
4. Repo simplified hai: ek HC poore block pe, aur koi matrix mixing nahi. Plus ek **quirk**: identity do baar judti hai, to stream har layer badhta hai (4 streams: ~19× after 12 layers).
5. 2.2M model pe 1 vs 4 streams me **koi saaf fark nahi** mila (3 seeds, mixed direction).

## Quiz

1. Residual connection bina 12 layers ke baad information ka kya hota hai?
2. 4 streams, read weights `[0.25, 0.25, 0.25, 0.25]`. Block ko kya input milta hai?
3. Repo ke poore model me hyper-connections ke kitne learnable parameters hain?
4. Doubly stochastic matrix kya hai? `[[0.5, 0.5], [0.5, 0.5]]` hai ya nahi?
5. Doubly stochastic matrices ka product signal ko explode kyun nahi karta?
6. Repo me identity "do baar" kaise judti hai?
7. RMSNorm ke hote hue bhi bada residual stream kya nuksaan kar sakta hai?
8. **Research soch:** "Repo ka quirk fix karne se (identity ek baar) training behtar hogi." Experiment design karo.

---

<details>
<summary>👉 Jawab</summary>

1. Har layer input ko poora badal deti hai. 12 layers ke baad original info lagbhag khatam (lab: similarity −0.05).
2. Chaaro streams ka **simple average**.
3. Har layer me 4 read + 4 write logits = 8, aur 12 layers × 8 = **96**.
4. Saare entries ≥ 0, aur har row aur column ka sum = 1. Haan, `[[0.5, 0.5], [0.5, 0.5]]` doubly stochastic hai.
5. Aisi matrix sirf values ko **redistribute** karti hai (weighted averages), aur total "mass" same rehta hai. Product bhi doubly stochastic hota hai, to kitni bhi layers hon, signal ka size bound rehta hai.
6. `HybridBlock` khud `x + attn + MoE` return karta hai, aur `HyperConnection` us poore output ko (jisme `x` already hai) stream me **phir** jodta hai.
7. Baad wali layers ke updates bade stream ke saamne **chhote** pad jaate hain, to unka relative asar kam ho jaata hai. Gradient scale bhi layer ke hisaab se uneven ho sakta hai.
8. Do variants: original vs fixed (`update = transformed − mixed`). Same data, init seed, steps, LR, aur 4 streams. Measure karo held-out loss, dev pass-rate, aur har layer ke update ka relative size (`‖update‖ / ‖stream‖`). 5+ paired seeds chalao. Agar fixed version better hai **aur** baad wali layers ke updates relatively bade hain, to hypothesis ko support milta hai.

</details>

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [05 · Code Lab — `lab_hyper_connections.py`](05-lab-guide.md) | 📚 [Topic 08 overview](README.md) | [Topic 09 — Vision: image ko tokens me badalna](../09-vision-image-to-tokens/README.md) ➡️ |
<!-- /nav:bottom -->
