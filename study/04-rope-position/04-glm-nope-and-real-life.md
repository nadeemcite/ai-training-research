# 04 · Released GLM ka twist (NoPE) + Real-life

## Released GLM-5.3 me position kahan hai?

Video (16:00–18:30) me Vuk batate hain ki **asli** GLM thoda alag karta hai:

| Part | Released GLM-5.3 | Hamara teaching model |
|---|---|---|
| Main attention | **NoPE** (No Positional Encoding, koi RoPE nahi) | RoPE |
| Sparse **indexer** (kaunse tokens dekhne hain, ye chunta hai) | RoPE | (indexer hi nahi hai, fixed pattern hai, Topic 06) |
| Linear attention | — | RoPE |

> Video: *"In GLM they are using NoPE ... in main model and then RoPE in the sparse indexer ... we apply RoPE in attention and indexer just to make it simpler for our model."*

### NoPE kaam kaise karta hai?! 🤔

**Causal mask** ki wajah se. Har token sirf apne se *pehle* wale tokens dekh sakta hai:
- Token 1 sirf 1 cheez dekhta hai
- Token 100 sau cheezein dekhta hai

Ye asymmetry model ko indirectly batati hai ki "main kitna aage hoon". Research (Kazemnejad et al., 2023) me dikha ki NoPE models kabhi-kabhi lambe context pe **better generalize** karte hain, kyunki unhe koi unseen angle nahi milta.

**Design logic:** Indexer ko position chahiye ("paas wale tokens zyada relevant hain"), lekin main attention content pe focus kar sakta hai. Ye ek hybrid design choice hai.

> **Research lesson:** "Sab jagah RoPE" default hai, lekin frontier labs har component pe sawaal karte hain: "kya yahan sach me chahiye?"

---

## Real-life analogy 1: Ghadi ki suiyan 🕐

Ek ghadi me 3 suiyan hain:
- **Second ki sui:** tez ghoomti hai, chhote time gaps batati hai
- **Minute ki sui:** medium
- **Ghante ki sui:** dheemi, bada time batati hai

Sirf second ki sui dekh ke tum nahi bata sakte ki 10:15:30 hai ya 3:45:30. Teeno milke exact time batati hain.

RoPE ke 16 pairs = 16 suiyan, alag-alag speed pe. Tez pairs paas ki position batate hain, dheeme pairs door ki. Sab milke unique position.

**Aur doori wali property:** Do ghadiyon ka time-difference sirf unki suiyon ke angle-difference se pata chal jaata hai, chahe dono subah ki hon ya shaam ki.

## Real-life analogy 2: Car ka odometer 🚗

`0 0 3 4 7` → Sabse right wala digit har km pe badalta hai (tez pair), sabse left wala 10,000 km pe (dheema pair). Alag "speeds" se hi bade numbers unique bante hain.

## Real-life analogy 3: Train me seat number 🚆

"Main seat 47 pe hoon" (absolute) vs "mera dost 2 seat aage hai" (relative). Dost dhoondhne ke liye relative info zyada kaam ki hai, aur wo kisi bhi coach me same tarah kaam karti hai. RoPE relative info deta hai.

---
🎬 **Video:** 16:00–18:30 · 📊 Slide 31 "Where released GLM uses position"
