# 05 · Code Lab — `lab_tokenizer.py`

## Run

```bash
uv run study/01-tokens-aur-tokenizer/lab_tokenizer.py
```

## Expected output (aur iska matlab)

```
Exp 1  'def x:' -> [104, 105, 106, 36, 124, 62]
```
→ Slide se exact match. Byte + 4 wala rule kaam kar raha hai.

```
Exp 2  round-trip OK
```
→ `decode(encode(text)) == text`. Ye tokenizer ka **sabse important test** hai. Repo ke `tests/test_lab.py` me bhi "tokenizer round-trip" check hai.

```
Exp 3  'hello'      chars= 5  tokens=5
Exp 3  'namaste'    chars= 7  tokens=7
Exp 3  'नमस्ते'     chars= 6  tokens=18
```
→ Reading 04 wala UTF-8 effect.

```
Exp 4  ek line se kitne (input -> target) lessons? 11
       input='r'        -> target='e'
       input='re'       -> target='t'
       ...
```
→ Ek line = bahut saare next-token lessons (Reading 01).

```
Exp 5  byte (hamara)  embedding params =       49,920  (~0.2% of 25.7M)
Exp 5  BPE 150k       embedding params =   28,800,000  (~112.1% of 25.7M)
```
→ Reading 03 ka parameter budget argument, numbers ke saath.

## Tumhara kaam (15 min)

1. **TODO (a):** Apna naam Hindi aur English dono me encode karo. Ratio kya hai?
2. **TODO (b):** `tok.decode([4 + 0xF0, 4 + 0x9F])` chalao. Ye 😀 emoji ke pehle 2 bytes hain (poora emoji 4 bytes ka hai). Kya print hua aur kyun?
3. **Bonus:** Repo ka asli tokenizer import karke dekho ki tumhare results same hain:
   ```bash
   cd sources/repo && uv run python -c "from glm53_flash.tokenizer import ByteTokenizer as T; print(T().encode('def x:'))"
   ```

## Break karke seekho 🔨

- `byte_offset = 4` ko `0` kar do aur Exp 1 dobara chalao. Assert fail hoga. Socho: agar offset 0 hota to byte value `0x01` aur `BOS=1` me confusion kaise hota?
