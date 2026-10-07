<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 15 — Capstone: poora GLM-5.3-Flash ek file me 🎓](README.md) › Reading 2 / 6
<!-- /nav:top -->

# 02 · Teen fixes — course me jo mila, wo yahan theek hai

Course ke dauraan repo ke code ko **measure** karke 3 chhupe issues mile. Capstone me teeno fixed hain, aur har fix pe `[FIX-xx]` comment hai.

## [FIX-07] MoE balance loss ab sach me gradient deta hai

**Problem (Topic 07):** Repo me `usage` integer counts se banta tha, isliye `requires_grad = False` tha. Balance loss loss me judta tha, log hota tha, lekin router pe **zero asar** karta tha.

**Fix** (Switch Transformer style):
```python
fraction = counts / (N * k)                    # kis expert ko kitne slots mile (no gradient)
probs = logits.softmax(-1).mean(0)             # router ki average probability (HAS gradient)
balance = n_experts * (fraction * probs).sum() # perfect balance = 1.0
```
Router ko gradient milta hai: "jis expert ko zyada slots mil rahe hain, uski probability ghatao." Smoke test: `balance.requires_grad = True` ✅. Hamare run me balance ~1.03 raha, jo perfect balance (1.0) ke bahut paas hai.

## [FIX-08] Hyper-connection me identity sirf ek baar

**Problem (Topic 08):** `HybridBlock` khud `x + attn + MoE` return karta tha, aur `HyperConnection` us poore output ko stream me **phir** jodta tha. Residual stream 12 layers me ~19× badh jaata tha (1 stream pe ~7,000×).

**Fix:** Block sirf **update** return karta hai:
```python
def forward(self, x):
    a = self.attn(self.attn_norm(x))
    m, balance, fraction = self.moe(self.ffn_norm(x + a))
    return a + m, balance, fraction            # identity NAHI — HyperConnection jodega
```
Ab stream = stream + write × (attention + MoE). Identity ek hi baar hai, standard transformer jaisa.

## [FIX-12] Verifier: random hidden tests

**Problem (Topic 12):** Har family ke 3 fixed test cases sab tasks me same the, isliye `return {-3: -2, 0: 1, 7: 8}[x]` jaisa lookup table **pass** ho jaata tha.

**Fix:** Har family ke saath ek **trusted reference function** aur ek random input generator:
```python
Family("increment", ..., reference=lambda x: x + 1, random_input=lambda r: (r.randint(-999, 999),))
```
`verify()` 3 fixed tests ke baad **8 naye random inputs** bhi check karta hai (har call pe naye):
```
sahi    -> passed
hack    -> failed   ✅ (pehle passed tha)
import  -> invalid
galat   -> failed
```
Har family ka reference body bhi verify hota hai (smoke test: 8/8 passed).

**Side effect:** reward ab thoda **random** hai. Ek galat-lekin-kabhi-kabhi-sahi function ka reward call-to-call badal sakta hai. Ye accha hai: model ko luck pe nahi, sahi logic pe reward milta hai.

## Kya in fixes ne cheezein behtar ki?

**Imaandaar jawab: humne ye prove nahi kiya.** Fixes "sahi engineering" hain, lekin "behtar results" ek alag claim hai jiske liye paired, multi-seed experiments chahiye (Topic 11). Ye tumhare liye perfect research projects hain (Reading 05).

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [01 · Code map — har section kis chapter se](01-code-map.md) | 📚 [Topic 15 overview](README.md) | [03 · Kaise chalayein](03-run-it.md) ➡️ |
<!-- /nav:bottom -->
