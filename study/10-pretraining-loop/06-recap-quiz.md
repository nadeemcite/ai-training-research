<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 10 — Pretraining loop: random weights se Python tak](README.md) › Reading 6 / 6
<!-- /nav:top -->

# 06 · Recap + Quiz

## 5-line recap

1. **Pretraining = imitation.** Har position pe agla byte guess karo, aur galti pe weights thoda sudhaaro. Ye lakhon baar hota hai.
2. Inputs aur labels me **1 position ka shift** hota hai. Padding labels `-100` hote hain, jo loss me nahi gine jaate.
3. Ek step: **zero_grad → predict → cross-entropy → backward → clip → AdamW step.**
4. **AdamW** har weight ka apna step size rakhta hai (m, v) aur weight decay lagata hai. **Clipping** ek kharab batch ko training barbaad karne se rokta hai.
5. Pretraining "Python jaisa dikhna" sikhata hai, "hamesha sahi hona" nahi. Ye gap RL bharta hai.

## Quiz

1. `"abc"` (BOS ke saath) ke liye inputs aur labels kya honge? (Token IDs nahi, characters me batao)
2. `ignore_index = -100` na lagaayein to kya galat hoga?
3. Model ne sahi token ko 0.01 probability di. Uss position ka loss kitna hai? 0.9 di to?
4. `zero_grad()` bhool gaye to kya hoga?
5. Gradient `[3, 4]`, max_norm 1. Clip ke baad kya hoga? `[0.3, 0.4]` ka kya hoga?
6. AdamW ka "W" kya karta hai?
7. Repo ne RL ke liye step 400 ki jagah checkpoint 100 kyun chuna?
8. **Research soch:** "Kya lab ka 2.2M model aur repo ka 25.7M model same tarah seekhte hain?" Ye compare karne ke liye kya fix rakhoge aur kya measure karoge?

---

<details>
<summary>👉 Jawab</summary>

1. Inputs: `[BOS, a, b]`, labels: `[a, b, c]` (EOS ho to: inputs `[BOS, a, b, c]`, labels `[a, b, c, EOS]`)
2. Model PAD positions pe bhi loss lega aur "PAD ke baad PAD" predict karna seekhega. Loss artificially kam dikhega aur asli tokens ka signal patla ho jaayega.
3. `−ln(0.01) ≈ 4.61`. `−ln(0.9) ≈ 0.105`.
4. Har step ke gradients pichle steps ke gradients me **jud jaayenge**, to updates galat aur dheere-dheere bahut bade ho jaayenge.
5. `[3, 4]` ka norm 5 hai, to clip ke baad `[0.6, 0.8]`. `[0.3, 0.4]` ka norm 0.5 hai (1 se kam), to **koi badlaav nahi**.
6. **Weight decay:** har step pe weights ko thoda 0 ki taraf khinchta hai, taaki weights bina wajah bade na hon (regularization).
7. Step 100 pe model ne "genuine code learning" dikhayi thi (dev 2/8), lekin **headroom** bhi thi. Agar 8/8 wala model lete, to RL ka asar measure karne ki jagah hi nahi bachti. Ye choice **dev** pe hui, confirmation pe nahi.
8. Fix rakho: same data/seed, same steps aur batch, ho sake to same tokens seen. Learning rate har size ke liye tune karna pad sakta hai, aur ye ek fair comparison ka hissa hai. Measure karo: dev score vs steps, loss vs tokens, aur time. Ek graph banao: x-axis tokens seen, y-axis dev pass-rate, dono models. Multiple seeds bhi chalao.

</details>

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [05 · Code Lab — `lab_pretrain.py`](05-lab-guide.md) | 📚 [Topic 10 overview](README.md) | [Topic 11 — Research skill: data experiments (diversity, order, curriculum)](../11-research-data-experiments/README.md) ➡️ |
<!-- /nav:bottom -->
