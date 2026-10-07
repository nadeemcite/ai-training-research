# 06 · Recap + Quiz

## 5-line recap

1. **Attention:** Har token query (Q) se pichle tokens ke keys (K) match karta hai, softmax weights banata hai, aur values (V) ka mix leta hai. **Causal mask** future chhupata hai.
2. Softmax attention ki `[T×T]` matrix **T²** me badhti hai. 1M context pe ye impossible hai, aur KV cache bhi T ke saath badhta hai.
3. **Linear attention:** φ (elu+1) lagao aur brackets badlo, `Q(KᵀV)`. Ek **fixed `[d×d]` running state S** banti hai, aur har naya token O(1) kaam karta hai.
4. Parallel (cumsum, training) = recurrent (loop, inference). Ye ek hi math hai.
5. Keemat: **lossy memory**, exact recall kharab hota hai. φ ka choice aur decay/delta rules (KDA) isse sudhaarte hain. Repo ke version me decay nahi hai.

## Quiz

1. Library analogy me Q, K, V kya hain?
2. Causal mask na ho to training me kya galat hoga?
3. T = 10,000 pe ek head ki softmax score matrix me kitne numbers hain? Linear state me (d = 32)?
4. `(Q Kᵀ) V = Q (Kᵀ V)` kyun sach hai, aur doosra version sasta kyun hai?
5. φ = elu + 1 kyun lagate hain, φ = identity kyun nahi (repo jaise normalised version me)?
6. Generation ke dauraan linear attention ko KV cache kyun nahi chahiye?
7. Lab Exp 4 vs Exp 6 se kya seekha?
8. **Research soch:** Repo ke `LinearAttention` me decay γ add karna hai. Kya hypothesis hogi aur experiment kaise design karoge?

---

<details>
<summary>👉 Jawab</summary>

1. Q = tumhara sawaal, K = kitaabon ke labels, V = kitaabon ka content.
2. Model agla token *dekh* ke copy kar lega. Training loss bahut kam aayega, lekin generation me (jab future hai hi nahi) model fail hoga.
3. 10,000² = **100,000,000** (10 crore). Linear: 32 × 32 = **1,024**.
4. Matrix multiplication associative hai. `Kᵀ V` sirf `[d × d]` hai, to `[T × T]` matrix kabhi nahi banti. Cost T² ki jagah T·d² hoti hai.
5. Weights positive hone chahiye aur denominator `φ(q)·z` zero/negative nahi hona chahiye. Identity se negative values aati aur division unstable hota.
6. Saari history pehle se **S** (aur z) me compress ho chuki hai. Naye token ko bas S update karke query karna hai.
7. Recall kharab hone ka bada culprit **φ = elu+1** hai (sab keys positive → overlap), sirf memory size nahi. Ek-ek component isolate karke culprit dhoondhna.
8. Hypothesis: "Decay recent context pe focus badhayega aur next-token loss kam karega, kyunki code me aksar paas ke tokens zyada relevant hote hain." Baaki sab same rakho, γ ∈ {1.0, 0.99, 0.95} try karo, aur pretraining loss + dev pass-rate measure karo, 3+ seeds pe. Ye bhi check karo ki lambi-doori dependencies (jaise comment me "one" → code me `1`) pe nuksaan to nahi hua.

</details>
