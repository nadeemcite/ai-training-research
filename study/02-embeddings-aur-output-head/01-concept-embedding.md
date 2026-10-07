# 01 · Concept — Embedding = token ka "meaning vector"

## Problem

Tokenizer ne `+` ko ID **47** de diya. Lekin:
- 47 aur 48 (`,`) ka numerically paas hona koi meaning nahi rakhta
- Neural network ko aise numbers chahiye jinse wo **math** kar sake, jaise similarity aur combination

## Solution: har token ko ek list of numbers (vector) do

```
"+"  →  [ 0.12, -0.80,  0.33, ..., 0.05]   (192 numbers)
"-"  →  [ 0.10, -0.75, -0.40, ..., 0.07]
"x"  →  [-0.55,  0.20,  0.91, ..., -0.30]
```

Is vector ko **embedding** kehte hain. Video ke shabdon me:
> *"vector embedding is like a sequence of numbers that encodes the meaning of that token... the vector for plus would kind of explain how addition is done."*

## Analogy: Masale ka "taste profile" 🌶️

Har masale ko 5 numbers se describe karo: `[teekha, meetha, khatta, khushboo, rang]`

| Masala | teekha | meetha | khatta | khushboo | rang |
|---|---|---|---|---|---|
| Laal mirch | 0.9 | 0.0 | 0.1 | 0.3 | 0.9 |
| Kashmiri mirch | 0.4 | 0.1 | 0.1 | 0.4 | 1.0 |
| Amchur | 0.0 | 0.2 | 0.9 | 0.3 | 0.2 |

Ab Laal mirch aur Kashmiri mirch ke vectors **paas-paas** hain, aur Amchur door hai. Similarity ab math se nikal sakti hai.

Embeddings bhi aisi hi hain, bas:
- 5 ki jagah **192 dimensions** hain (hamare model me)
- Dimensions ke naam nahi hote, model khud decide karta hai ki har number kya represent kare

## Sabse important baat: ye **seekhe** jaate hain

Shuru me har vector **random** hota hai (repo me `std=0.02` wale chhote random numbers). Training ke dauraan har baar galat prediction pe gradient in vectors ko thoda-thoda adjust karta hai.

Dheere-dheere similar kaam karne wale tokens ke vectors paas aa jaate hain, jaise `+` aur `-`, ya `0`–`9` digits.

> Video: *"These vectors are learned by the LLM... LLM learns how to represent concept of a plus with some numbers."*

## Embedding ke baad kya?

Prompt ke har token ka vector ban gaya. Ab ye **sequence of vectors** transformer layers me jaata hai, jahan tokens ek-doosre se information share karte hain (attention). Wo aage ke topics me aayega.

---
🎬 **Video:** 07:00–08:30 · 📊 Slide 25 "How one byte becomes a prediction"
