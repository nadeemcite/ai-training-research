# 03 · Practical — BPE vs Byte tokens

## Real LLMs: BPE (Byte-Pair Encoding)

BPE ek tokenizer hai jo data dekh ke **seekhta** hai ki kaunse characters aksar saath aate hain, aur unhe jod ke ek token bana deta hai.

Rough idea:
1. Shuru me har byte alag token hai
2. Sabse common pair dhundo (jaise `t`+`h`), use naya token `th` bana do
3. Fir se repeat karo (`th`+`e` → `the`) ... jab tak vocab ~150k–250k na ho jaaye

Result: `"returning"` shayad sirf 2 tokens ban jaaye (`return` + `ing`).

## Hamara model: Byte tokens

Har byte = 1 token, aur vocab sirf **260** ka hai.

| | BPE (real GLM) | Byte (hamara) |
|---|---|---|
| Vocab size | ~150,000+ | 260 |
| Tokenizer training chahiye? | Haan | Nahi |
| `"return"` kitne tokens | ~1 | 6 |
| Sequence length | Chhoti | Lambi (~3–4× English ke liye) |
| Koi bhi text encode ho sakta hai? | Haan (byte fallback se) | Haan, hamesha |
| Embedding table ka size | Bahut bada | Chhota |

## Asli wajah: **parameters ka budget** 💰

Embedding table ka shape hota hai `[vocab_size × dim]`. Hamare model me `dim = 192` hai.

| Vocab | Embedding params | 25.7M model ka kitna % |
|---|---:|---:|
| 260 (byte) | 49,920 | **0.2%** |
| 150,000 (BPE) | 28,800,000 | **112%** 😱 |
| 250,000 (BPE) | 48,000,000 | **187%** 😱 |

Matlab, agar 25M ke model me BPE lagaate to saare parameters sirf "word → vector" conversion me chale jaate aur asli dimaag (layers) ke liye kuch nahi bachta.

Video me Vuk bolte hain: *"on a very small model... 95% of parameters would just go into the vocabulary conversion"*.

> **Rule of thumb:** Chhota model → chhota vocab. Bada model (billions) → bada vocab theek hai, kyunki tab embedding table total ka chhota hissa hota hai.

## Trade-off jo yaad rakhna hai

Byte tokens ki bhi keemat hai:
- **Lambe sequences:** Same text ke liye 3–4× zyada tokens, to compute zyada lagta hai aur context jaldi bhar jaata hai
- Model ko spelling se word banana bhi khud seekhna padta hai

Hamare tiny Python tasks (`return x + 1`) ke liye ye trade-off bilkul theek hai.

## Research question (khud socho)
> *"Agar vocab 260 se 1000 kar dein (thoda BPE), to kya 25M model jaldi seekhega?"*
Ye ek valid experiment hai jo tum CPU pe kar sakte ho.

---
🎬 **Video:** 05:16–07:00 · 📊 Slides 15–16
