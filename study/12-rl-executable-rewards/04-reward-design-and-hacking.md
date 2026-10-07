<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 12 — RL with executable rewards + verifier](README.md) › Reading 4 / 6
<!-- /nav:top -->

# 04 · Reward design, reward hacking + Real-life

## Reward kaise design karein?

> Video (34:44): *"There are many ways in which you can structure rewards. For example, you can say plus one for all tests passed, zero for valid format but wrong number, and maybe minus one for invalid Python syntax."*

Repo do modes deta hai (`reward_for`):

| Jawab | Tests | **binary** (final run) | **case-fraction** |
|---|---:|---:|---:|
| Sahi | 3/3 | +1.0 | +1.0 |
| Aadha sahi | 2/3 | 0.0 | **+0.67** |
| Galat lekin valid | 0/3 | 0.0 | 0.0 |
| Invalid / unsafe | — | −0.1 | −0.1 |

**Binary:** sirf poora sahi hi gina jaata hai. Ye saaf hai, lekin signal kam milta hai.
**Case-fraction (partial credit):** aadhe sahi ko bhi kuch milta hai. Signal zyada hai, lekin model "2/3 pe hi khush" reh sakta hai.

**Invalid penalty (−0.1):** "kam se kam valid Python likho" ka chhota sa dhakka. Ise bahut bada karo (−1) to model darr ke kuch bhi likhna band kar sakta hai.

Repo ke RL variant experiments (Topic 14) me binary, partial, no-penalty aur hard-penalty, **sab ne lagbhag same perform kiya**. Is setup me reward ki shape utni matter nahi ki.

## Sparse reward: jab koi signal hi na mile

Asli final run (lab Exp 5):
- 96 groups me se **23 me saare 16 rewards barabar** the, to **koi update nahi** hua
- Unme se **22 me saare 16 jawab invalid** the (−0.1)

RL tabhi seekhta hai jab ek group me **kuch jawab behtar aur kuch badtar** hon. Agar model kabhi sahi jawab likhta hi nahi, to RL ke paas badhane ke liye kuch hai hi nahi. Isliye:
1. **Pretraining zaroori hai.** RL usi ko badhata hai jo pehle se kabhi-kabhi hota hai.
2. **Checkpoint choice matter karti hai.** Repo ne step 100 chuna, jab dev pe 2/8 sahi tha: kuch sahi, kuch sudhaar ki jagah.

Training ke dauraan sahi rollouts: pehle 24 groups me **23%** → aakhri 24 groups me **46%**.

## 🚨 Reward hacking

**Reward hacking** = model asli kaam seekhne ki jagah reward ka loophole dhoondh leta hai.

> Video (31:48): *"You will not show tests to the model. You will just evaluate its result, because if you show tests it can reward hack."*

> Video (36:24): *"Now you have GPT, Fable, Astra... they are possibly going to hack and see your verifiers. So this is something that's happening right now."*

### Repo me mila ek asli hole 🔍

Har family ke **3 test cases fixed hain** aur saare tasks me same hain. To ye "jawab" verifier pass kar leta hai (lab Exp 3):

```python
def increment_cjaojdr(x):
    return {-3: -2, 0: 1, 7: 8}[x]       # sirf 3 test inputs ka jawab ratta
```
```
repo verifier: passed, reward +1.0  😱
```

`dict` aur `[x]` (subscript) DENIED list me nahi hain. Tests model ko dikhaye nahi jaate, lekin agar model ne RL ke dauraan kabhi galti se aisa kuch likh diya, to wo pattern bhi reward hota aur badhta jaata.

**Kya ye hua?** 25.7M model ke liye ye pattern itna ajeeb hai ki iski sambhavna bahut kam hai, aur repo ke asli outputs (`return x * 2`) sahi hain. Lekin **bade, smart models aise holes dhoondh lete hain.** Repo report bhi maanta hai: *"The same three unit cases are reused within each operation family."*

### Fix: hidden random tests

Lab ka `stronger_verifier` har baar **naye random inputs** se bhi check karta hai:
```
stronger verifier: sahi -> True, hack -> False  ✅
```

Model ratta nahi maar sakta, kyunki agle check ke inputs pehle se pata nahi hote.

---

## Real-life analogy: Driving test 🚗

- **Policy** = learner driver
- **Environment** = RTO ka test track
- **Verifier** = examiner
- **Reward** = pass / fail

**Reward hacking:** Agar test **hamesha same route** pe hota hai (fixed 3 test cases), to log sirf wahi route ratt lete hain, aur asli road pe gaadi nahi chala paate. Achha RTO **route random** rakhta hai (random hidden tests).

**Sandbox:** Examiner learner ko test ke dauraan highway pe nahi le jaata, balki band track pe le jaata hai (restricted builtins, no imports).

**Sparse reward:** Agar learner ko pehle se steering pakadna bhi nahi aata (koi pretraining nahi), to test lene ka fayda nahi. Har baar fail hoga aur kuch nahi seekhega.

## Real-life analogy 2: Leaked exam paper 📝

Agar students ko pata chal jaaye ki exam me exactly kaunse 3 sawaal aayenge, to wo 3 jawab ratt lenge. Marks 100% aayenge, lekin subject zero aayega. **Isliye tests model se chhupaye jaate hain**, aur isliye unhe **badalte rehna** chahiye.

---
🎬 **Video:** 31:40–32:05, 34:44–36:30 · 📊 Slides 63–64 · 📄 `REPORT.md` → Limitations

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [03 · Practical — Verifier: model ka code safely kaise chalayein?](03-verifier-sandbox.md) | 📚 [Topic 12 overview](README.md) | [05 · Code Lab — `lab_rewards.py`](05-lab-guide.md) ➡️ |
<!-- /nav:bottom -->
