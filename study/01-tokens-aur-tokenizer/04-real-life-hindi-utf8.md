# 04 · Real-life — Hindi me zyada tokens kyun lagte hain?

## UTF-8 ek minute me

Computer har character ko **bytes** me store karta hai. UTF-8 rule:

| Character type | Example | Bytes |
|---|---|---|
| English / ASCII | `a`, `x`, `+` | 1 |
| Accented Latin | `é` | 2 |
| **Devanagari (Hindi)** | `न`, `म`, `स`, `्`, `त`, `े` | **3** |
| Emoji | `😀` | 4 |

## Experiment (lab me same chalega)

| Text | Characters | Byte tokens |
|---|---:|---:|
| `hello` | 5 | 5 |
| `namaste` | 7 | 7 |
| `नमस्ते` | 6 | **18** |

`नमस्ते` dikhne me 4 letters jaisa hai, lekin Unicode me 6 code points hain (`न म स ् त े`), aur har ek 3 bytes ka hai. **18 tokens** ho gaye.

## Real duniya me iska asar 🌍

1. **API ka bill:** OpenAI/Anthropic/GLM APIs **per token** charge karti hain. Unke BPE tokenizers zyadatar English data pe train hue hote hain, isliye Hindi text aksar same meaning ke English se **zyada tokens** leta hai. Same baat, zyada ₹.
2. **Context jaldi bharta hai:** Agar 8k context hai to Hindi me kam content fit hoga.
3. **Speed:** Zyada tokens = zyada generation steps = slow jawab.
4. **Isliye Indian companies apne tokenizers banati hain**, jo Indic text pe train hote hain, taaki Hindi words bhi 1–2 tokens me aa jaayein.

## Edge case: aadha character

Agar ek 3-byte Hindi letter ke sirf 2 bytes decode karo to valid character nahi banta. Hamara tokenizer `errors="replace"` use karta hai, isliye wahan `�` dikhta hai.

Generation me ye sach me hota hai: byte model kabhi-kabhi adhoora character generate kar deta hai. (Lab TODO (b) me try karo.)

## Takeaway

> Tokenizer **neutral nahi** hota. Wo tay karta hai ki kis language/data ka text "sasta" hai aur kiska "mehenga". Research me tokenizer choice ek real design decision hai.

---
🎬 Video me Hindi example nahi hai. Ye extra real-life context hai, video ke 05:16 wale BPE part se juda hua.
