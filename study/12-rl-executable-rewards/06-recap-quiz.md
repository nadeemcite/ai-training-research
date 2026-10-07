<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 12 — RL with executable rewards + verifier](README.md) › Reading 6 / 6
<!-- /nav:top -->

# 06 · Recap + Quiz

## 5-line recap

1. **Pretraining = nakal, RL = koshish + inaam.** RL me model khud jawab likhta hai, aur use code chala ke reward milta hai. Reference answer kabhi nahi dikhaya jaata.
2. RL aksar **naya concept nahi sikhata**, balki pretraining me chhupe sahi jawab ki probability badhata hai (`return x * * 0 0` → `return x * 2`).
3. **Verifier** = AST checks (no imports/loops/attributes) + restricted builtins + strict type-aware tests, aur shak ho to **fail closed**.
4. **Reward design:** binary vs partial credit, invalid penalty. Agar group ke saare rollouts ka reward same ho, to koi signal nahi milta (**sparse reward**).
5. **Reward hacking:** fixed, reused tests ratke pass kiye ja sakte hain (`{-3: -2, 0: 1, 7: 8}[x]`). Fix hai hidden aur **random** tests. Algorithm se zyada **environment design** matter karta hai.

## Quiz

1. Pretraining aur RL me model ko milne wale feedback ka fark batao.
2. Verifier `import` aur `for` loops kyun rokta hai?
3. `type(actual) is type(expected)` check kyun zaroori hai? Ek example do.
4. Ek group ke 16 rollouts sab −0.1 hain. RL is group se kya seekhega?
5. Binary vs case-fraction: ek fayda aur ek nuksaan batao.
6. Repo ke verifier me reward hacking kaise possible hai, aur fix kya hai?
7. Temperature bahut kam ya bahut zyada ho to RL pe kya asar hota hai?
8. **Research soch:** "Kya partial credit (case-fraction) reward se RL jaldi seekhta hai?" Experiment design karo: kya fix rakhoge aur kya measure karoge?

---

<details>
<summary>👉 Jawab</summary>

1. Pretraining me har position pe **sahi agla token** milta hai (dense, detailed). RL me poore jawab ke liye sirf **ek number** milta hai (reward), aur sahi jawab kabhi nahi dikhaya jaata.
2. `import` se `os`, `subprocess` jaise khatarnak modules aa sakte hain, aur loops se infinite loop training atka sakta hai. Model untrusted code likhta hai.
3. Python me `True == 1` aur `2.0 == 2` sach hain. "even" family ko `True` chahiye. Agar model `1` return kare to type check use galat maanta hai, jo sahi hai.
4. **Kuch nahi.** Saare rewards barabar hain, to "kaunsa behtar tha" ka koi signal nahi. Repo ka code update skip kar deta hai (`spread > 1e-8` check).
5. Binary: saaf hai, sirf poora sahi gina jaata hai, lekin signal sparse hai. Case-fraction: zyada signal milta hai (aadhe sahi ko bhi kuch), lekin model partial solutions pe atak sakta hai.
6. Har family ke 3 test cases fixed aur reused hain, to `{-3: -2, 0: 1, 7: 8}[x]` jaisa lookup pass ho jaata hai. Fix: har check pe **random hidden inputs**, aur tests ko model se chhupa ke rakhna.
7. Bahut kam: saare rollouts lagbhag same, to rewards same aur signal nahi. Bahut zyada: zyadatar invalid/kachra, to phir se signal nahi aur training unstable (repo ka pilot 1, temperature 0.8).
8. Fix: same starting checkpoint, tasks, group size, temperature, LR, steps aur seeds. Sirf `--reward-mode binary` vs `case-fraction` badlo. Measure karo: dev pe sahi rollouts ka curve (kitni jaldi badhta hai), aakhir me **binary pass@1** (taaki dono ek hi paimane pe judge hon), aur kitne groups me update hua. 3+ seeds pe chalao. *(Repo ka asli result Topic 14 me: is setup me koi significant fark nahi mila.)*

</details>

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [05 · Code Lab — `lab_rewards.py`](05-lab-guide.md) | 📚 [Topic 12 overview](README.md) | [Course home](../README.md) 🏁 *(agle topics jald aa rahe hain)* |
<!-- /nav:bottom -->
