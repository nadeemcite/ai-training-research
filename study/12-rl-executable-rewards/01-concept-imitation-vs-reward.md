<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 12 — RL with executable rewards + verifier](README.md) › Reading 1 / 6
<!-- /nav:top -->

# 01 · Concept — Nakal (pretraining) vs Koshish + Inaam (RL)

## Do tarah ka seekhna

| | Pretraining (Topic 10) | Reinforcement Learning (ye topic) |
|---|---|---|
| Model ko kya milta hai | **Sahi jawab** (poora code) | Sirf **sawaal** (prompt) |
| Model kya karta hai | Har byte copy karna seekhta hai | **Khud** jawab likhta hai |
| Feedback | "Agla byte ye tha" | "Tumhara jawab chala? +1 / 0 / −0.1" |
| Kya seekhta hai | Data jaisa dikhna | **Sahi** hona |

> Video (30:38): *"Pre-training is just learning to repeat text and it's learning what each token means. In reinforcement learning it's trying to generate answers and then we reward correct answers."*

> Video: *"In some way, I don't know how, but it's learning to think somehow, and if you can figure out how, you'll be the most famous AI researcher."*

## RL kuch naya nahi sikhata... ya sikhata hai? 🤔

Repo ka report bahut imaandaar hai:
> *"All operation families appeared during pretraining; RL amplified existing latent solutions rather than introducing unseen concepts."*

Matlab pretraining ke baad model ke andar sahi jawab **kahin chhupa tha**, lekin kam probability ke saath. RL ne us sahi raaste ki probability **badha di**.

Repo ka asli example, unseen prompt `# Return two times x.`:

| | 8 samples me se |
|---|---|
| RL se pehle | sab galat, pehla tha `return x * * 0 0` |
| RL ke baad | **8/8:** `return x * 2` ✅ |

> Video (34:37): *"What reinforcement learning did is increase probability that the correct answer will generate."*

## Executable reward kyun itna powerful hai?

Code ke liye "sahi" ka matlab **check kiya ja sakta hai**: code chalao aur tests dekho. Isme koi insaan ya doosra AI judge nahi chahiye.

- ✅ Sasta: lakhon checks per ghanta
- ✅ Objective: kisi ki raay nahi, test pass ya fail
- ✅ Scalable: frontier labs isi tarah coding/math models train karte hain

> Video (31:04): *"Right now reinforcement learning traces, single rollout, single task completion, is taking maybe even days in frontier labs."*

## Asli kaam: environment design

Video ka sabse important RL point:
> *(35:21) "I also think that data is a lot more important than the structure of these algorithms... You will improve the model a lot more if you are thinking about: what am I teaching it? What is the environment? ... This is why DeepSeek is no longer putting substantial effort into GRPO. GRPO, their RL algorithm, is good enough."*

Algorithm (RLOO, GRPO, PPO) ek baar "kaafi accha" ho jaaye, to asli fark is baat se padta hai:
- **Kaunse tasks** do (environment)
- **Kaise check** karo (verifier)
- **Kya reward** do (reward design)

Yahi is topic ka focus hai.

## Result (preview, detail Topic 13–14 me)

| Metric (confirmation set, 3 trained families) | RL se pehle | RL ke baad |
|---|---:|---:|
| Greedy tasks solved | 0/24 | **16/24** |
| Dev pe sahi rollouts | 4.2% | **45.8%** |

> Video (32:06): *"We went from 4% correct answers to 45% correct answers after the training."*

---
🎬 **Video:** 30:27–34:44 · 📊 Slides 57–62 · 📄 `REPORT.md` (Abstract, Exact behavior)

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [Topic 12 — RL with executable rewards + verifier](README.md) | 📚 [Topic 12 overview](README.md) | [02 · Definitions — RL ke shabd](02-definitions.md) ➡️ |
<!-- /nav:bottom -->
