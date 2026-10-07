# 06 · Recap + Quiz

## 5-line recap

1. LLM har step pe **agle token** ki probability guess karta hai, aur generation bas yahi loop hai.
2. **Tokenizer** text ↔ token IDs convert karta hai. Model sirf numbers dekhta hai.
3. Real LLMs **BPE** use karte hain (~150k+ vocab). Hamara model **bytes** use karta hai (260 vocab = 256 bytes + 4 special).
4. Chhote model me bada vocab rakhne se embedding table hi saare parameters kha jaata. Isliye bytes.
5. Byte tokens ki keemat lambe sequences hain. Hindi = 3 bytes/char, to 3× tokens.

## Quiz (pehle khud jawab do, fir neeche dekho)

1. `"x+1"` ke token IDs kya honge? (Hint: `x`=120, `+`=43, `1`=49)
2. Vocab size 260 hi kyun hai, 256 kyun nahi?
3. Ek 20-character ki ASCII line se kitne next-token training pairs bante hain?
4. `dim=192` aur `vocab=50,000` hai. Embedding table me kitne parameters?
5. BPE tokenizer ko "train" karna padta hai, byte tokenizer ko kyun nahi?
6. Model ko kaise pata chalta hai ki jawab khatam ho gaya?
7. Hindi chatbot banane wali company ke liye English-heavy BPE tokenizer kyun nuksaandayak hai? (2 reasons)
8. **Research soch:** Byte tokenizer ka ek *nuksaan* batao jo 25M model ke liye matter karta hai, aur ek experiment design karo jo use measure kare.

---

<details>
<summary>👉 Jawab dekhne ke liye click karo</summary>

1. `[124, 47, 53]` (har byte + 4)
2. 256 possible byte values + 4 special tokens (PAD, BOS, EOS, SEP)
3. **19** (n − 1)
4. 50,000 × 192 = **9,600,000**
5. Byte tokenizer ek fixed rule hai (byte + 4). Use data se kuch seekhna nahi hota. BPE data se common pairs seekhta hai.
6. Model `EOS` token (ID 2) generate karta hai. `decode()` wahan ruk jaata hai.
7. (a) Zyada tokens = zyada API cost / compute, (b) context window me kam content fit hota hai, aur (c) generation slow hoti hai.
8. Example: Lambe sequences ki wajah se 192-token context me kam code fit hota hai. **Experiment:** Same data pe byte-model vs chhota-BPE (vocab ~1k) model train karo. Same parameter count aur same steps rakho, aur dev pass-rate compare karo. Multiple seeds use karo!

</details>
