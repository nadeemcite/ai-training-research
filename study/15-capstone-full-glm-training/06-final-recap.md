<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 15 — Capstone: poora GLM-5.3-Flash ek file me 🎓](README.md) › Reading 6 / 6
<!-- /nav:top -->

# 06 · Final recap — poora course, ek page me

## Model (Topics 01–09)

| Topic | Ek line |
|---:|---|
| 01 | Text → bytes → token IDs (260 vocab). Chhote model ke liye chhota vocab |
| 02 | ID → embedding vector → … → output head → softmax. Embedding aur head **tied** hain |
| 03 | **RMSNorm** har sublayer se pehle numbers ka size ~1 rakhta hai (pre-norm) |
| 04 | **RoPE**: q/k ko position se ghumao, to score sirf **doori** pe depend karta hai |
| 05 | **Linear attention**: fixed `[d×d]` running memory, O(1) per token, lekin lossy |
| 06 | **Sparse attention**: window + anchors (ya indexer), exact recall. **3 linear : 1 sparse** |
| 07 | **MoE**: router top-2 of 8 + shared expert. Total params zyada, active kam |
| 08 | **Hyper-connections**: 4 residual lanes, learnable read/write. mHC = doubly stochastic mixing |
| 09 | **Vision**: patches → ViT → 2×2 merge → projector → 16 tokens, LM ki sequence me |

## Training & research (Topics 10–14)

| Topic | Ek line |
|---:|---|
| 10 | **Pretraining** = nakal: predict → cross-entropy → backward → clip → AdamW |
| 11 | **Research**: ek variable, held-out, paired seeds, p-value + effect size, imaandaar claims |
| 12 | **RL environment**: sandboxed verifier + executable reward. **Reward hacking** se bacho |
| 13 | **RLOO**: advantage = reward − baaki ka mean. Loss = −adv × logp. Sirf last block + head |
| 14 | **Evaluation**: confirm ek baar, pass@1 vs pass@k, McNemar, interference, **replication** |

## Course me khud dhoondhi gayi cheezein 🔍

Ye sab code padh ke aur **measure** karke mila, sirf video dekh ke nahi:

1. Repo ka **MoE balance loss ka gradient zero** hai (Topic 07)
2. **Hyper-connection me identity do baar** judti hai, aur stream 12 layers me ~19× badhta hai (Topic 08)
3. Verifier ke **fixed tests ratke pass** kiye ja sakte hain (Topic 12)
4. "Faithful" vision path simple baseline se **har seed pe haara** (Topic 09)
5. Same seed pe CPU numbers **run-to-run badal** sakte hain (Topics 08, 13)
6. Capstone me ek `state_dict()` **reference bug** pakda gaya (Topic 15)

Yahi asli research skill hai: **"maybe it's a bug in my code or bug that AI generated"**, isliye har cheez check karo.

## Final quiz (har topic se ek)

1. 25.7M model me 150k BPE vocab kyun nahi?
2. Weight tying ka ek fayda aur ek limitation?
3. Pre-norm ka formula?
4. RoPE ke baad score (5, 3) aur (105, 103) pe same kyun hai?
5. Linear attention ki memory T ke saath kyun nahi badhti?
6. GLM-5.3 ki 12 layers me kaunsi sparse hain?
7. MoE me total vs active params ka fark kya hai?
8. mHC me Sinkhorn kyun lagta hai?
9. Image ke 64 patches 16 tokens kaise bante hain?
10. Padding labels −100 kyun hote hain?
11. 3 seeds pe sabse chhota possible p?
12. `{-3: -2, 0: 1, 7: 8}[x]` kya dikhata hai?
13. Saare rewards barabar hon to RLOO advantage kya hoga?
14. "A dev win is not a discovery" ka matlab?

<details>
<summary>👉 Jawab</summary>

1. 150k × 192 ≈ 28.8M params sirf embedding me jaate, jo poore model se bhi zyada hai.
2. Fayda: parameter bachat + same geometry. Limitation: bina beech ki layers ke model same token repeat karne ki taraf jhukta hai.
3. `x = x + f(norm(x))`
4. Dono me doori 2 hai, aur rotation ke baad dot product sirf angle-difference pe depend karta hai.
5. Saari history ek fixed `[d×d]` state S me jodti jaati hai (compress hoti hai).
6. Layers 4, 8, 12 (`(i + 1) % 4 == 0`).
7. Total = memory me saare experts. Active = ek token pe kaam aaye (2 routed + shared).
8. Mixing matrices doubly stochastic rahein, taaki layers ke product se signal explode na ho.
9. 8×8 grid → 2×2 padosi patches concat → Linear → 4×4 = 16.
10. Padding ka loss na gine, warna model "PAD ke baad PAD" seekhega.
11. 2/2³ = **0.25**
12. **Reward hacking**: fixed tests ratke verifier pass karna, bina asli logic ke.
13. **Zero.** Kuch seekhne ko nahi, update skip.
14. Ek seed / dev pe jeeta hua variant fresh seeds pe haar sakta hai. Replicate karo, tab claim karo.

</details>

---

🎉 **Mubarak ho! Poora course complete.** Ab [Reading 05](05-research-roadmap.md) se ek sawaal chuno aur apna pehla experiment chalao.

🙏 Ye course **Vuk Rosić** ke video aur code pe based hai, jo **freeCodeCamp** ne free me publish kiya. Unka shukriya ada karna mat bhoolna: video like karo, aur agar ho sake to freeCodeCamp ko support karo.

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [05 · Research roadmap — ab kya karein?](05-research-roadmap.md) | 📚 [Topic 15 overview](README.md) | [Course home](../README.md) 🏁 *(course complete 🎉)* |
<!-- /nav:bottom -->
