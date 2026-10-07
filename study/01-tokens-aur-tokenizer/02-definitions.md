<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 01 — Tokens aur Tokenizer](README.md) › Reading 2 / 6
<!-- /nav:top -->

# 02 · Definitions — exact words ka matlab

| Term | Simple Hinglish definition | Hamare model me |
|---|---|---|
| **Token** | Text ka sabse chhota tukda jo model ek baar me dekhta hai. Ye ek word, word ka hissa, ya ek byte ho sakta hai | 1 token = 1 byte |
| **Token ID** | Har token ka ek number. Model text nahi, sirf numbers samajhta hai | `0`–`259` |
| **Vocabulary (vocab)** | Saare possible tokens ki list. Iska size = kitne alag token IDs ho sakte hain | `260` |
| **Tokenizer** | Wo program jo text → token IDs (**encode**) aur token IDs → text (**decode**) karta hai | `ByteTokenizer` |
| **Special tokens** | Aise IDs jo koi text nahi, balki ek "signal" hain | `PAD=0, BOS=1, EOS=2, SEP=3` |
| **Context length** | Model ek baar me max kitne tokens dekh sakta hai | `192` |

## Special tokens detail me

| ID | Naam | Kaam |
|---|---|---|
| 0 | `PAD` (padding) | Batch me chhote sequences ko barabar length karne ke liye khaali jagah bharta hai |
| 1 | `BOS` (beginning of sequence) | "Yahan se naya text shuru hai" |
| 2 | `EOS` (end of sequence) | "Bas, jawab khatam." Isko generate karke model rukta hai |
| 3 | `SEP` (separator) | Do hisson ke beech divider, jaise prompt aur answer |

## Formula: hamare tokenizer ka encode

```
token_id = utf8_byte_value + 4
```

`+4` isliye ki IDs 0–3 special tokens ne le liye hain.

Example (slide "Code becomes tokens"):

| Char | `d` | `e` | `f` | space | `x` | `:` |
|---|---|---|---|---|---|---|
| Byte (ASCII) | 100 | 101 | 102 | 32 | 120 | 58 |
| Token ID (+4) | **104** | **105** | **106** | **36** | **124** | **62** |

## Code (repo se, poora)

```python
class ByteTokenizer:
    pad_id, bos_id, eos_id, sep_id = 0, 1, 2, 3
    byte_offset = 4
    vocab_size = 260                      # 4 special + 256 bytes

    def encode(self, text, bos=False, eos=False):
        ids = [self.byte_offset + v for v in text.encode("utf-8")]
        ...
```

**Notice karo:** Isme koi "training" nahi hai. Ye tokenizer kuch seekhta nahi, sirf ek fixed rule follow karta hai. BPE tokenizers ko data pe *train* karna padta hai (next reading).

---
🎬 **Video:** 05:16–06:10 · 📁 `sources/repo/glm53_flash/tokenizer.py`

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [01 · Concept — LLM bas "agla token" guess karta hai](01-concept-next-token.md) | 📚 [Topic 01 overview](README.md) | [03 · Practical — BPE vs Byte tokens](03-bpe-vs-byte.md) ➡️ |
<!-- /nav:bottom -->
