<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 14 — Evaluation: sahi naapna, imaandaari se bolna](README.md) › Reading 6 / 6
<!-- /nav:top -->

# 06 · Recap + Quiz

## 5-line recap

1. **Train → Dev → Confirm:** dev pe faisle lo, aur confirm sirf **ek baar**, aakhir me kholo. Metrics pehle se tay karo.
2. **pass@1** = reliably karta hai, **pass@k** = kar sakta hai. Unbiased estimator: `1 − C(n−c, k) / C(n, k)`.
3. Main result: greedy **0/24 → 16/24**, 16 gains / 0 losses, McNemar **p = 0.00003**. Lekin ye narrow, within-family claim hai.
4. **Interference:** `square` 52 → 37 aur `list_sum` 61 → 56 gire. `even` bilkul nahi sudhra. Unexpected results ko chhupao mat, unhe agla sawaal banao.
5. **Replication:** screen ka "winner" (group size 4) fresh seeds pe haar gaya. *"A dev win is not a discovery."*

## Quiz

1. Confirmation set baar-baar dekhne me kya galat hai?
2. n = 8 samples me se c = 2 sahi. pass@1 aur pass@8 kya hai?
3. McNemar test me "same rahe" tasks kyun ignore hote hain?
4. 16 gains, 0 losses ka p ≈ 0.00003 kaise aaya?
5. "RL ne model ko coding sikha di" kyun galat claim hai? Do wajah batao.
6. Interference kya hai? Repo me iska ek example do.
7. Group size 4 screen me best tha lekin confirm me haara. Ye kaise possible hai?
8. **Research soch:** Tumhe `even` family ke fail hone ki wajah dhoondhni hai. 3 hypotheses aur har ek ka ek chhota test likho.

---

<details>
<summary>👉 Jawab</summary>

1. Har baar dekh ke faisla lene se tum dheere-dheere confirm set pe hi "tune" ho jaate ho. Wo dev set ban jaata hai, aur final number optimistic (jhootha) ho jaata hai.
2. pass@1 = 2/8 = **25%**. pass@8 = 1 − C(6,8)/C(8,8) = 1 − 0 = **100%** (8 me se 8 chune to sahi wala zaroor aayega).
3. Wo dono conditions me same the, to before/after ke fark ke baare me koi information nahi dete. Sirf discordant pairs (gain ya loss) batate hain ki change kis taraf hua.
4. Null hypothesis (koi asar nahi) me har badla task 50-50 gain/loss hota. 16 me se 16 gains ka chance (1/2)¹⁶, aur two-sided ke liye ×2: 2/65,536 ≈ **0.0000305**.
5. (a) Saari families pretraining me thi, aur confirm me sirf **function naam naye** the, patterns nahi. (b) Sirf 2 families sudhri, 1 flat rahi, 2 giri. Plus 1 training seed aur synthetic benchmark.
6. Ek cheez sikhane se doosri bigadna. Repo: RL increment/double/even pe hua, aur `square` 52/64 → 37/64 gira.
7. Screen **1 seed** aur 20 dev tasks pe tha. 8 vs 6 ka fark noise ho sakta hai. 8 variants me se ek ka luck se top aana kaafi likely hai (multiple comparisons). Fresh seeds pe asli (zero ya negative) effect dikha.
8. Example: (H1) **Type issue:** model `1`/`0` return karta hai `True`/`False` ki jagah. Test: failed `even` outputs padho, aur kya `x % 2 == 0` kabhi generate hota bhi hai? (H2) **Latent solution nahi tha:** before 3/64. Test: zyada pretraining (step 200) se RL shuru karo aur dekho ki `even` sudhra ya nahi. (H3) **Gradient competition:** RL sirf `even` pe chalao (`--families even`) aur dekho ki akele me sudhar hota hai ya nahi.

</details>

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [05 · Code Lab — `lab_evaluation.py`](05-lab-guide.md) | 📚 [Topic 14 overview](README.md) | [Topic 15 — Capstone: poora GLM-5.3-Flash ek file me 🎓](../15-capstone-full-glm-training/README.md) ➡️ |
<!-- /nav:bottom -->
