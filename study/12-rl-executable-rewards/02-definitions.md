<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 12 — RL with executable rewards + verifier](README.md) › Reading 2 / 6
<!-- /nav:top -->

# 02 · Definitions — RL ke shabd

| Term | Matlab | Repo me |
|---|---|---|
| **Policy** | RL me model ko policy kehte hain: "is situation me kya karna hai" ka rule | pretraining checkpoint 100 se shuru |
| **Environment** | Duniya jisse model interact karta hai: sawaal deti hai aur jawab judge karti hai | coding tasks + verifier |
| **Prompt / task** | Ek sawaal | `# Return x plus one.\ndef increment_cjaojdr(x):` |
| **Rollout / completion** | Model ka ek poora generated jawab | `\n    return x + 1\n` |
| **Verifier** | Program jo jawab ko check karta hai | `evaluate_source` |
| **Reward** | Ek number: kitna accha tha | +1 / 0 / −0.1 |
| **Group** | Ek prompt ke liye kai rollouts ek saath | 16 rollouts |
| **Temperature** | Sampling me randomness. Kam = confident/same, zyada = vividh | 0.35 |
| **Exploration** | Naye/alag jawab try karna | zyada temperature |
| **Exploitation** | Jo pehle se accha lagta hai wahi karna | kam temperature |
| **On-policy** | Model apne **abhi wale** version ke rollouts se seekhta hai | haan (RLOO) |
| **Sparse reward** | Zyadatar rollouts ko same reward (aksar 0), to signal kam milta hai | 23/96 groups me koi signal nahi |
| **Reward hacking** | Model asli kaam kiye bina reward ka loophole dhoondh leta hai | Reading 04 |

## Ek RL step, simple shabdon me

```
1. Ek task chuno:            "# Return two times x.  def double_xyz(x):"
2. Model 16 jawab likhe      (temperature 0.35, max 48 tokens)
3. Har jawab verifier se:    +1, 0, −0.1, +1, 0, ...
4. Update (Topic 13):        +1 wale jawab zyada likely, −0.1 wale kam likely
5. Agla task
```

Repo ka asli final run: **96 tasks × 16 rollouts = 1,536 rollouts**, 155 sec GPU.

## Splits: kaunsa data kahan

Har split ka **alag seed** hai, isliye function naam alag hote hain:

| Split | Kaam |
|---|---|
| `pretrain` | Pretraining data |
| `rl` | RL training ke prompts |
| `dev` | Checkpoint chunne ke liye |
| `final` / `confirm` | **Sirf ek baar**, aakhir me result report karne ke liye |

⚠️ **Lekin:** har family ke **3 test cases same** hain, chahe split koi bhi ho (`increment`: −3→−2, 0→1, 7→8). Ye ek important kamzori hai (Reading 04).

## Temperature: exploration vs exploitation

> Video (04:05): *"Temperature, or randomness of next word generation in reinforcement learning... it's exploration versus exploitation with what it already knows."*

- **Bahut kam temperature:** 16 rollouts lagbhag **same** aate hain, to sab ka reward same hota hai aur kuch seekhne ko nahi milta
- **Bahut zyada:** kachra jawab aate hain, sab invalid, to phir se koi signal nahi
- Repo: 0.8 pe training unstable hui (pilot 1), aur **0.35** pe kaam kiya

Lab Exp 4 me ek asli group dikhega (temperature 0.35, "double" task):
```
 6x  reward +0.0  'return x * x'       ← valid, galat (square kar diya)
 5x  reward -0.1  'return x * * x'     ← invalid
 4x  reward +1.0  'return x * 2'       ← sahi ✅
 1x  reward -0.1  'return x * * 0'
```
Ek hi model, ek hi prompt, aur 4 alag tarah ke jawab. Yahi variety RL ko seekhne deti hai.

---
📁 `train_rl.py` lines 39–54, 150–170 · `tasks.py` · 🎬 Video 30:27–34:44

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [01 · Concept — Nakal (pretraining) vs Koshish + Inaam (RL)](01-concept-imitation-vs-reward.md) | 📚 [Topic 12 overview](README.md) | [03 · Practical — Verifier: model ka code safely kaise chalayein?](03-verifier-sandbox.md) ➡️ |
<!-- /nav:bottom -->
