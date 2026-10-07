# 06 · Recap + Quiz

## 5-line recap

1. Bahut saari layers me multiply hote-hote numbers **explode ya vanish** ho jaate hain.
2. **RMSNorm** vector ko uske RMS se divide karta hai, to size ~1 ho jaata hai aur direction (meaning) wahi rehti hai.
3. **γ** har dimension ka seekhne wala scale hai, aur **ε** divide-by-zero se bachata hai.
4. **Pre-norm** (`x + f(norm(x))`) residual highway ko saaf rakhta hai. Repo me 25 RMSNorms hain (12×2 + final).
5. RMSNorm = LayerNorm minus mean-subtraction. Ye sasta hai, utna hi accha hai, aur aaj ke LLMs ka standard hai.

## Quiz

1. `x = [3, 4]` ka RMS kya hai? RMSNorm(x) kya hoga (γ = 1)?
2. `RMSNorm([6, 8])` aur `RMSNorm([3, 4])` me kya fark hai?
3. ε na ho to kis input pe problem hogi?
4. `x = x + attention(norm(x))`: ye pre-norm hai ya post-norm? Kyun?
5. Repo me kitne RMSNorm layers hain aur kul kitne parameters?
6. LayerNorm aur RMSNorm ka ek fark batao.
7. Pre-norm me residual stream ka size thoda badhta kyun hai, aur `final_norm` kya karta hai?
8. **Research soch:** "RMSNorm ka γ hata do (sab fixed 1)" ye ek ablation hai. Is experiment ko kaise design karoge? Kya measure karoge?

---

<details>
<summary>👉 Jawab</summary>

1. RMS = √((9 + 16) / 2) = √12.5 ≈ **3.54**. RMSNorm = `[0.85, 1.13]`
2. **Koi fark nahi.** `[6, 8]` sirf `[3, 4]` × 2 hai, aur RMSNorm scale-invariant hai.
3. All-zero vector pe: `0 / sqrt(0)` = `0 / 0` = **NaN**
4. **Pre-norm**, kyunki norm attention ke *input* pe laga hai, aur residual `x` bina norm ke jud raha hai.
5. 12 × 2 + 1 = **25** RMSNorms. 25 × 192 = **4,800** params.
6. LayerNorm mean subtract karta hai (aur uske paas β bias hai). RMSNorm sirf RMS se scale karta hai.
7. Har block `x` me kuch jodta hai aur `x` khud kabhi normalize nahi hota, isliye size dheere badhta hai. `final_norm` output head se pehle stream ko normalize karta hai.
8. Do model train karo jo γ ke alawa bilkul same hon: same data, steps aur LR. **Kai seeds** pe chalao. Measure karo: final loss, dev pass-rate, aur training stability (koi loss spike?). Ek seed pe jeet ko discovery mat maano (video 41:19+).

</details>
