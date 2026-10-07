<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 06 — Sparse attention + 3:1 hybrid rhythm](README.md) › Reading 6 / 6
<!-- /nav:top -->

# 06 · Recap + Quiz

## 5-line recap

1. **Sparse attention** = normal softmax attention, lekin har query sirf **chuni hui keys** pe. Isme compression nahi, exact recall hai.
2. Teaching model ka **fixed pattern** = local window (pichle 32) + anchors (har 32nd position). Simple hai, lekin zaroori token miss ho sakta hai.
3. Released GLM-5.3 ka **indexer** ek sasta scorer hai jo content se top-k chunta hai (DSA idea), aur main attention cost ko T × k pe fix rakhta hai.
4. Hamare pattern me anchors t/32 se badhte hain, to cost ~T²/32 hai. Ye sasta hai, lekin quadratic hi rehta hai.
5. **3:1 rhythm** (`(i+1) % 4 == 0`): 9 linear layers sasta compress karti hain, 3 sparse layers exact details wapas laati hain. Ye ratio empirical hai, research ka sawaal.

## Quiz

1. Window 4, stride 5. Position 12 kaun-kaun si positions dekhega?
2. Sparse attention me "lossy memory" problem kyun nahi hai?
3. Repo config (W=32, S=32) me position 191 kitni keys dekhta hai? (Hint: local 32 + anchors 0..160, overlap hatao)
4. Hamare fixed pattern ki cost T² ki tarah kyun badhti hai, aur indexer isse kaise bachata hai?
5. `valid` mask aur `masked_fill(−∞)` kyun chahiye?
6. `(index + 1) % 4 == 0` 12 layers me kaunse layers (1-based) ko sparse banata hai?
7. Agar saari 12 layers linear hon, to kya nuksaan hoga? Agar saari sparse hon?
8. **Research soch:** "Sparse layers ko end me (10, 11, 12) rakho vs har 4th pe." Hypothesis aur experiment design karo.

---

<details>
<summary>👉 Jawab</summary>

1. Anchors: 0, 5, 10. Local: 9, 10, 11, 12. Set: **[0, 5, 9, 10, 11, 12]**
2. Kyunki jo keys chuni gayi, unke **exact** K, V use hote hain. Kuch bhi compress/mix nahi hota, bas baaki ko ignore kiya jaata hai.
3. Local = 160..191 (32), anchors = 0, 32, 64, 96, 128, 160 (6). 160 dono me hai, to 32 + 6 − 1 = **37**
4. Har position pe anchors ki ginti `t/32` hai, jo T ke saath badhti hai, to total ~T²/32. Indexer hamesha fixed **k** chunta hai, to main attention T × k (linear) hota hai. Indexer khud T² hai, lekin bahut halka.
5. Har query alag number of keys dekhti hai, lekin tensor rectangular hona chahiye. Padding positions ka score −∞ kar do, to softmax ke baad unka weight 0 ho jaata hai.
6. Layers **4, 8, 12**
7. Sab linear: exact recall kharab hoga, door ki specific details kho jaayengi. Sab sparse: mehenga hoga, aur fixed pattern ki wajah se jo tokens pattern me nahi aate unki info kisi raaste se nahi aayegi (linear wala compressed raasta bhi nahi).
8. Hypothesis: "Har 4th pe spread karne se info baar-baar refresh hoti hai, jabki end me cluster karne se shuruaati layers ko kabhi exact context nahi milta." Dono variants same params/steps/data ke saath train karo. Measure karo pretraining loss aur lambi-doori wale tasks (prompt ki instruction 100+ tokens peeche ho) ka dev pass-rate, 3+ seeds pe.

</details>

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [05 · Code Lab — `lab_sparse_attention.py`](05-lab-guide.md) | 📚 [Topic 06 overview](README.md) | [Topic 07 — Mixture of Experts (MoE)](../07-mixture-of-experts/README.md) ➡️ |
<!-- /nav:bottom -->
