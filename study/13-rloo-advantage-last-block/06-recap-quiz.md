<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 13 — RLOO: advantage se update tak, aur sirf last block train karna](README.md) › Reading 6 / 6
<!-- /nav:top -->

# 06 · Recap + Quiz

## 5-line recap

1. **Advantage** = reward − baseline. Ek attempt ko uske group ke baaki attempts se compare karo. Advantages ka sum ~0 hota hai.
2. **RLOO:** baseline = baaki attempts ka mean. **GRPO:** group mean + std se normalize. Dono me **critic model ki zaroorat nahi**.
3. **Policy gradient loss** = `−(advantage × log_prob).mean()`. Minus isliye ki optimizer minimize karta hai aur hum maximize karna chahte hain.
4. Repo sirf **last block + final norm + tied head** train karta hai (2.19M / 25.7M = 8.5%). Isse forgetting kam hota hai, speed badhti hai, aur stability aati hai.
5. Repo me **KL penalty nahi** hai, isliye non-trained families pe interference dikha. Aur 5 pilot koshishon ke baad ek setting chali, jise imaandaari se report kiya gaya.

## Quiz

1. Rewards `[1, 0, 0, 0]`. Har attempt ka RLOO advantage nikaalo.
2. Saare 16 attempts ko +1 mila. Update kya hoga, aur kyun ye theek hai?
3. Loss me minus sign na lagaayein to kya hoga?
4. Log-prob ko length se divide kyun karte hain?
5. RLOO ko critic model kyun nahi chahiye?
6. Sirf last block train karne ke 2 fayde aur 1 subtle "chhupi" baat batao.
7. KL penalty kya karta hai, aur uske bina kya risk hai?
8. **Research soch:** "RLOO vs GRPO-style normalization, kaunsa behtar hai?" Experiment design karo.

---

<details>
<summary>👉 Jawab</summary>

1. Attempt 0: 1 − mean(0, 0, 0) = **+1.0**. Baaki: 0 − mean(1, 0, 0) = **−0.333** har ek. (Sum = 1 − 1 = 0 ✓)
2. Saare advantages 0 hain, to **koi update nahi**. Theek hai, kyunki tulna karne ko kuch nahi tha. Ye prompt model ke liye already solved hai.
3. Optimizer `adv × logp` ko **minimize** karega, yaani achhe attempts ki probability **ghata** dega aur bure ki badha dega. Model ulta seekhega.
4. Warna lambe attempts ka log-prob (zyada negative numbers ka sum) bahut bada hota, aur update length pe depend karne lagta. Average se har attempt barabar weight paata hai.
5. Baseline group ke baaki attempts ka average hai, jo **free** mil jaata hai. Alag model train karke "expected reward" guess karne ki zaroorat nahi.
6. Fayde: kam forgetting (pehli layers safe), tez/sasta, stable. Chhupi baat: embedding aur head **tied** hain, to head train karne se input embeddings bhi badalte hain, jo pehli layer ka input hain.
7. KL penalty model ko original (pretrained) version se zyada door jaane se rokta hai. Iske bina model reward ke liye trained tasks pe zyada specialize ho sakta hai aur doosri cheezein bhool sakta hai (interference). Repo me `square` 52 → 37/64 gira.
8. Same checkpoint, tasks, seeds, group size, temperature aur steps rakho. Sirf advantage formula badlo: RLOO vs `(r − mean) / std`. LR ko dono ke liye tune karo, kyunki GRPO advantages bade hote hain (scale ka fark). Measure karo: dev sampled exact ka curve, stability (koi collapse?), aur non-trained families ka interference. 3+ seeds, aur winner ko fresh confirm split pe check karo.

</details>

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [05 · Code Lab — `lab_rloo.py`](05-lab-guide.md) | 📚 [Topic 13 overview](README.md) | [Topic 14 — Evaluation: sahi naapna, imaandaari se bolna](../14-evaluation-honest-results/README.md) ➡️ |
<!-- /nav:bottom -->
