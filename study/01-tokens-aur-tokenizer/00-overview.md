# Topic 01 — Tokens aur Tokenizer

**Goal:** Is topic ke baad tum bata paoge ki LLM text ko "padhta" kaise hai. Tum ye bhi samjha paoge ki hamare chhote GLM model ne BPE ki jagah **bytes** kyun use kiye.

**Time:** ~45 min (padhai) + ~20 min (lab)

## Reading order

| File | Type | Kya milega |
|---|---|---|
| `01-concept-next-token.md` | Concept | LLM asal me kya karta hai, ek line me |
| `02-definitions.md` | Definitions | Token, vocabulary, tokenizer, token ID, special tokens |
| `03-bpe-vs-byte.md` | Practical | Real LLMs vs hamara model, aur vocab size ka cost |
| `04-real-life-hindi-utf8.md` | Real-life | Hindi me zyada tokens kyun lagte hain (₹ ka asar bhi) |
| `05-lab-guide.md` | Code | `lab_tokenizer.py` run karo, output samjho, khud experiment karo |
| `06-recap-quiz.md` | Test | 8 sawaal, jawab neeche chhupe hain |

## Repo me kahan hai?

- `sources/repo/glm53_flash/tokenizer.py` — poora tokenizer sirf ~30 lines ka hai
- `sources/repo/slides/slides.html` — slides 15–16
