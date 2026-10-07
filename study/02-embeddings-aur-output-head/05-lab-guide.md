# 05 · Code Lab — `lab_embeddings.py`

## Run (~15 sec, CPU pe)

```bash
uv run study/02-embeddings-aur-output-head/lab_embeddings.py
```

## Expected output (aur matlab)

```
Exp 1  ids shape (1, 3) -> vectors shape (1, 3, 192)
```
→ `[B, T]` → `[B, T, D]`. Script ek `assert` se check bhi karta hai ki lookup = `emb.weight[104]` row hai (Reading 02).

```
Exp 2  logits (260,), probs sum = 1.0000
       untrained model ka top guess: 214 (random hi hoga)
```
→ Softmax ka sum 1 hai (Reading 03). Untrained model kuch bhi bolta hai.

```
Exp 3  untied=99,840  tied=49,920  bachat=49,920
```
→ Tying ke baad parameter aadhe ho gaye (Reading 04).

```
Exp 4  tied=False  final loss 0.789  'r' ke baad top-3: [('n', 0.5), ('e', 0.5), ('b', 0.0)]
Exp 4  tied=True   final loss 1.921  'r' ke baad top-3: [('r', 0.3), (' ', 0.14), ('n', 0.13)]
```
→ Ye ek mini **bigram model** hai jo pichla byte dekh ke agla byte predict karta hai, bina kisi transformer ke.
- Untied ne sahi seekha: `return` me `r` ke baad `e` aata hai aur `return` ke doosre `r` ke baad `n`, to dono 50-50 hain. 💯
- Tied atak gaya (Reading 04 ki limitation).

## Tumhara kaam (20 min)

1. **Loss check:** Step 0 ka loss `ln(260) ≈ 5.56` ke paas kyun hai? (Reading 03)
2. **TODO (a):** `DIM = 8` kar do. Kya untied model ab bhi `n`/`e` seekhta hai? 8 numbers 260 tokens ke liye kaafi kyun hain is task me?
3. **TODO (b):** Apne shabdon me 3 lines likho ki tied model `'r'` kyun guess karta hai.
4. **Bonus:** `train_bigram` me ek beech ki layer jodo, jaise `out(torch.tanh(lin(e(x))))` jahan `lin = nn.Linear(DIM, DIM)`. Ab `tied=True` bhi sahi jawab deta hai? Ye Reading 04 ke "to real model me kaam kyun karta hai" ka sabse chhota proof hoga.

## Repo ke asli model pe check

```bash
cd sources/repo && uv run python -c "
from glm53_flash.model import GLM53FlashFromScratch, ModelConfig
m = GLM53FlashFromScratch(ModelConfig())
print(m.parameter_counts())
print('tied:', m.output.weight is m.embedding.weight)"
```
Expected: `{'total': 25730592, 'active_per_token_estimate': 9805344}` aur `tied: True`
