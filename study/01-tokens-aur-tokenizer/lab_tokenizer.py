"""Lab 1 — Byte tokenizer haath se banao aur test karo.

Run:  uv run study/01-tokens-aur-tokenizer/lab_tokenizer.py
"""


class ByteTokenizer:
    """Same logic as sources/repo/glm53_flash/tokenizer.py (copied for study)."""

    pad_id, bos_id, eos_id, sep_id = 0, 1, 2, 3
    byte_offset = 4  # pehle 4 IDs special tokens ke liye reserved
    vocab_size = 260  # 4 special + 256 possible byte values

    def encode(self, text: str, bos: bool = False, eos: bool = False) -> list[int]:
        ids = [self.byte_offset + b for b in text.encode("utf-8")]
        if bos:
            ids.insert(0, self.bos_id)
        if eos:
            ids.append(self.eos_id)
        return ids

    def decode(self, ids: list[int]) -> str:
        out = bytearray()
        for t in ids:
            if t == self.eos_id:
                break
            if t >= self.byte_offset:
                out.append(t - self.byte_offset)
        return out.decode("utf-8", errors="replace")


tok = ByteTokenizer()

# --- Experiment 1: slide wala example --------------------------------------
ids = tok.encode("def x:")
print("Exp 1  'def x:' ->", ids)
assert ids == [104, 105, 106, 36, 124, 62], "slide se match hona chahiye"

# --- Experiment 2: round-trip (encode -> decode = original) ----------------
code = "def double(x):\n    return x * 2\n"
assert tok.decode(tok.encode(code, bos=True, eos=True)) == code
print("Exp 2  round-trip OK")

# --- Experiment 3: English vs Hindi — kitne tokens? -------------------------
for text in ["hello", "namaste", "नमस्ते"]:
    print(f"Exp 3  {text!r:12} chars={len(text):2}  tokens={len(tok.encode(text))}")

# --- Experiment 4: next-token training pairs ek hi line se ------------------
line = "return x + 1"
ids = tok.encode(line)
print("Exp 4  ek line se kitne (input -> target) lessons?", len(ids) - 1)
for i in range(1, 5):
    print(f"       input={tok.decode(ids[:i])!r:10} -> target={tok.decode([ids[i]])!r}")

# --- Experiment 5: vocab size ka parameter cost -----------------------------
dim = 192  # hamare model ki embedding dimension
for name, vocab in [("byte (hamara)", 260), ("BPE 150k", 150_000), ("BPE 250k", 250_000)]:
    params = vocab * dim
    print(f"Exp 5  {name:14} embedding params = {params:>12,}  (~{params / 25.7e6:.1%} of 25.7M)")

# TODO (tumhara kaam):
#  a) Apna naam Hindi + English me encode karo, tokens count compare karo.
#  b) decode([4 + 0xF0, 4 + 0x9F]) try karo — adhoora emoji kya print karta hai? Kyun?
