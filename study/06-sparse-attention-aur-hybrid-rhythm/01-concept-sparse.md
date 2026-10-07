# 01 · Concept — "Sab mat dekho, sahi cheezein dekho"

## Observation

Softmax attention ke weights dekho to zyadatar tokens ko **lagbhag 0** weight milta hai. Ek token asal me sirf kuch hi tokens ko seriously "sunta" hai:
- paas ke tokens (pichle kuch words)
- kuch khaas door ke tokens (function ka naam, comment me likhi instruction)

To baaki hazaaron tokens ke liye score kyun nikaalna?

## Sparse attention ka idea

> **Har query sirf ek chhoti list of keys ko dekhti hai. Unpe normal softmax attention lagao, baaki ko ignore karo.**

Isme koi compression nahi hai. Jo tokens dekhe, unhe **exact** dekha. Isliye ye linear attention ki "lossy memory" wali problem solve karta hai:

> Video: *"Linear layers carry compressed history cheaply. Sparse layers periodically recover exact distant details."*

## Sawaal: kaunse tokens chunein?

Do approaches hain:

### 1. Fixed pattern (hamara teaching model)

Pehle se tay rule: **local window + regularly spaced anchors.** Slide 36 wala picture (window 5, stride 4, position 14):

```
pos:   0  1  2  3  4  5  6  7  8  9 10 11 12 13 14
       A  ·  ·  ·  A  ·  ·  ·  A  ·  L  L  L  L  L
```
- **L (local):** pichle kuch tokens, taaki detail bachi rahe
- **A (anchor):** har 4th token, taaki door tak "jhaank" sake

> Slide: *"anchors reach far back + local tokens preserve detail"*

### 2. Content-based / Indexer (released GLM-5.3)

Ek **chhota, sasta** attention ("indexer") pehle har token ko jaldi se score karta hai. Fir **top-k sabse relevant** tokens chune jaate hain, aur sirf unpe asli (mehenga) attention lagta hai.

> Video: *"This indexer is going to search for the most relevant tokens for this token to attend to ... a lot lighter, a lot cheaper, a lot faster attention mechanism ... It can be 2,000 most relevant tokens or thousand."*

Ye idea DeepSeek-V3.2 ke **DSA (DeepSeek Sparse Attention)** se aaya hai.

## Fixed vs Indexer, ek line me

| | Fixed pattern | Indexer |
|---|---|---|
| Kaun chunta hai | Ek rule (position se) | Model (content se) |
| Seekhna padta hai? | Nahi | Haan |
| Galat token chun sakta hai? | Haan, agar zaroori token anchor/window me nahi hai | Kam chance |
| Code complexity | Simple | Zyada |

Lab Exp 4 me tum dekhoge ki fixed pattern "needle" miss kar deta hai, aur indexer use pakad leta hai.

---
🎬 **Video:** 16:17–17:48, 20:25–20:45 · 📊 Slide 36 "Sparse attention retrieves selected positions"
