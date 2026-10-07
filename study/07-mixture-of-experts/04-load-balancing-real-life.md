<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 07 — Mixture of Experts (MoE)](README.md) › Reading 4 / 6
<!-- /nav:top -->

# 04 · Load balancing, ek repo bug 🐛, aur Real-life

## Problem: Expert collapse ("rich get richer")

1. Shuru me router thoda random hai. Maan lo E1 ko thode zyada tokens mile.
2. E1 zyada train hua → aur accha ho gaya → router use aur zyada chunta hai.
3. E5, E8 ko tokens nahi mile → wo train hi nahi hue → bekaar rahe → router unhe kabhi nahi chunta.
4. **Result:** 8 me se 2–3 experts hi kaam karte hain, aur baaki ke params waste ho jaate hain.

Lab Exp 5 ka TODO (b) (`8 * mu`, strong common direction), bina balance loss ke:
```
usage = [0.02, 0.26, 0.01, 0.01, 0.36, 0.00, 0.35, 0.00]     ← 2 experts dead (0%), 3 almost dead
```
Balance loss ke saath:
```
usage = [0.13, 0.14, 0.13, 0.12, 0.12, 0.11, 0.13, 0.12]     ← sab ~12.5% (= 1/8) ✅
```

## Solution: Balance loss

Repo ka formula (`train_pretrain.py`):
```python
balance = ((usage.mean(dim=0) - 1.0 / config.experts) ** 2).mean() * config.experts
loss = language_loss + 0.01 * balance
```

Matlab: har expert ka usage `1/8 = 0.125` se kitna door hai, uska squared average. Perfect balance → 0.

Lab Exp 4:
- Balanced `[0.125 × 8]` → **0.000**
- Collapsed `[0.5, 0.5, 0, 0, 0, 0, 0, 0]` → **0.375**

## 🐛 Repo me ek chhupa hua bug (maine verify kiya)

```python
usage = torch.zeros(len(self.experts))
usage[expert_id] = positions.numel()        # ← ek integer COUNT
```

Count se gradient nahi banta. Maine repo ka model chala ke check kiya:
```
usage.requires_grad = False   | grad_fn = None
balance.requires_grad = False
```

**Matlab:** Repo ka `0.01 * balance` loss me jud to raha hai aur log bhi ho raha hai, lekin router pe uska **koi asar nahi**. Training me load balancing actually ho hi nahi rahi!

**Fix kaise hota hai?** Real implementations (Switch Transformer, Mixtral) router ki **softmax probabilities** (jo differentiable hain) ko counts ke saath multiply karte hain:
```python
probs = softmax(router_logits).mean(0)        # differentiable
aux_loss = experts * (fraction_counts * probs).sum()
```
Hamare lab Exp 5 me bhi differentiable `probs` use kiye hain, isliye wahan balance loss kaam karta hai.

**Kya isse kuch toota?** Shayad nahi: 8 experts aur chhota model, to collapse shayad naturally nahi hua. Lekin ye ek **real research lesson** hai:

> **Research lesson:** "Loss me jod diya" ≠ "loss kaam kar raha hai". Hamesha check karo ki `requires_grad` hai, aur ablation chala ke dekho ki term hatane se kuch badalta hai ya nahi. Video me Vuk khud bolte hain: *"maybe it's a bug in my code or bug that AI generated"* (39:50). AI-generated code me aise silent bugs common hain.

## Modern alternative: Aux-loss-free balancing

DeepSeek-V3 ne extra loss ki jagah har expert ka ek **bias** rakha. Jo expert overloaded hai uska bias thoda kam karo, aur jo underloaded hai uska badhao. Ye bias sirf **chunne** me use hota hai, output weights me nahi. Isse language loss pe koi "kheench-taan" nahi hoti.

---

## Real-life analogy: Hospital 🏥

- **Experts** = Specialist doctors (cardiologist, dermatologist, ortho, ...)
- **Router** = Reception desk. Tumhare symptoms (token) dekh ke 2 doctors suggest karta hai
- **Gate weights** = "Cardiologist ki raay 60%, general physician ki 40%"
- **Shared expert** = **Nurse/General check-up.** BP, temperature, weight har patient ka hota hai, chahe kisi bhi specialist ke paas jao
- **Total params** = Hospital ke saare doctors. **Active** = jinse tum mile. Bill active ka aata hai, lekin hospital ko saare doctors ki salary deni padti hai (memory)
- **Expert collapse** = Reception sabko ek hi famous doctor ke paas bhejta hai. Uski line 5 ghante lambi hai, baaki doctors khaali baithe hain aur dheere-dheere unki practice chhoot jaati hai
- **Balance loss** = Management ka rule: "har doctor ko roughly barabar patients do"

## Real-life analogy 2: Zomato/Swiggy 🛵

Order (token) aata hai, aur algorithm (router) 2 nearest delivery partners (top-k) me se chunta hai. Agar sirf 2 partners ko saare orders milein, to wo overload ho jaayenge aur baaki ko kaam nahi milega. Isliye load balancing.

---
🎬 **Video:** 20:42–21:30, 39:50 (bug wala comment) · 📁 `scripts/train_pretrain.py` line 94

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [03 · Practical — Repo code aur total vs active params](03-practical-code-and-params.md) | 📚 [Topic 07 overview](README.md) | [05 · Code Lab — `lab_moe.py`](05-lab-guide.md) ➡️ |
<!-- /nav:bottom -->
