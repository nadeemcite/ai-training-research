# 05 · Code Lab — `lab_sparse_attention.py`

## Run (~3 sec)

```bash
uv run study/06-sparse-attention-aur-hybrid-rhythm/lab_sparse_attention.py
```

## Expected output (aur matlab)

```
Exp 1  position 14 dekhta hai: [0, 4, 8, 10, 11, 12, 13, 14]
         0  1  2  3  4  5  6  7  8  9 10 11 12 13 14
         A  ·  ·  ·  A  ·  ·  ·  A  ·  L  L  L  L  L   (A = anchor, L = local window)
```
→ Slide 36 ka picture, repo ke rule se banaya (Reading 02).

```
Exp 2  T=    192  full=        18,528  sparse=       6,128  (33.1%)
Exp 2  T=  4,096  full=     8,390,656  sparse=     390,672  (4.7%)
Exp 2  T=131,072  full= 8,590,000,128  sparse= 272,694,800  (3.2%)
```
→ Bachat, aur anchors ki wajah se abhi bhi quadratic (Reading 03).

```
Exp 3  window=T  : sparse == full? True
       window=3  : sparse == full? False
```
→ Sanity check / unit test (Reading 03).

```
Exp 4  needle position = 37
       fixed pattern  (12 keys): [0, 16, 32, 48, 56, 57, 58, 59, 60, 61, 62, 63]  -> needle mila? False
       indexer top-8  (8 keys): [0, 3, 6, 15, 18, 37, 43, 63]  -> needle mila? True
```
→ Content-based selection ki taakat (Reading 01, 03).

```
Exp 5  12 layers: L L L S L L L S L L L S   -> 9 linear, 3 sparse
```
→ 3:1 rhythm (Reading 04).

## Tumhara kaam (20 min)

1. **TODO (a):** Exp 1 me `stride=4` ko `stride=2` kar do. Ab position 14 kitne tokens dekhta hai? Compute (zyada keys) vs reach (door tak dekhna) ka trade-off apne shabdon me likho.
2. **TODO (b):** Exp 4 me `needle = 48` kar do. Fixed pattern ab needle pakadta hai? Ye "luck" kyun hai, design kyun nahi?
3. **TODO (c):** Repo model ke layer types print karo (command lab file ke end me hai).
4. **Bonus:** Exp 4 me indexer ke dims 4 se 1 kar do (`query[:1]`, `keys[:, :1]`). Needle ab bhi milta hai? Indexer kitna "sasta" ho sakta hai, iski limit kya hai?

## Repo ke asli layer pe check

```bash
cd sources/repo && uv run python -c "
from glm53_flash.model import SparseAttention, ModelConfig
sa = SparseAttention(ModelConfig()); idx, valid = sa._indices(192, 'cpu')
print('position 191 dekhta hai', int(valid[191].sum()), 'keys (full hota to 192)')"
```
Expected: `position 191 dekhta hai 37 keys (full hota to 192)`
