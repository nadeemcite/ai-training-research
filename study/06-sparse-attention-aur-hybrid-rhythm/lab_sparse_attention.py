"""Lab 6 — Sparse attention (window + anchors), indexer idea, aur 3:1 rhythm.

Run:  uv run study/06-sparse-attention-aur-hybrid-rhythm/lab_sparse_attention.py
"""

import torch

torch.manual_seed(0)


def sparse_indices(position: int, window: int, stride: int) -> list[int]:
    """Same rule as SparseAttention._indices in sources/repo/glm53_flash/model.py."""
    anchors = list(range(0, position + 1, stride))
    local = list(range(max(0, position - window + 1), position + 1))
    return sorted(set(anchors + local))


def attend(q, k, v, allowed: list[list[int]]):
    """Har query sirf `allowed[t]` positions ko dekhti hai. q, k, v: [T, d]."""
    T, d = q.shape
    mask = torch.full((T, T), float("-inf"))
    for t, cols in enumerate(allowed):
        mask[t, cols] = 0.0
    weights = torch.softmax(q @ k.T / d**0.5 + mask, dim=-1)
    return weights @ v


# --- Experiment 1: slide wala picture (window 5, stride 4, position 14) ------
row = sparse_indices(14, window=5, stride=4)
picture = "".join("A" if p % 4 == 0 and p < 10 else ("L" if p in row else "·") for p in range(15))
print("Exp 1  position 14 dekhta hai:", row)
print("       ", " ".join(f"{p:>2}" for p in range(15)))
print("       ", " ".join(f"{c:>2}" for c in picture), "  (A = anchor, L = local window)")

# --- Experiment 2: repo config (window 32, stride 32) — kitne keys? ----------
W, S = 32, 32
for T in [192, 4_096, 131_072]:
    full_pairs = T * (T + 1) // 2
    sparse_pairs = sum(len(sparse_indices(t, W, S)) for t in range(T)) if T <= 4_096 else None
    if sparse_pairs is None:  # bade T ke liye formula: ~W local + t/S anchors
        sparse_pairs = sum(min(t + 1, W) + t // S + 1 for t in range(T))
    print(f"Exp 2  T={T:>7,}  full={full_pairs:>14,}  sparse={sparse_pairs:>12,}  ({sparse_pairs / full_pairs:.1%})")

# --- Experiment 3: sanity check — window >= T ho to sparse == full -----------
T, d = 12, 16
q, k, v = torch.randn(T, d), torch.randn(T, d), torch.randn(T, d)
full = attend(q, k, v, [list(range(t + 1)) for t in range(T)])
sparse_big = attend(q, k, v, [sparse_indices(t, window=T, stride=4) for t in range(T)])
sparse_small = attend(q, k, v, [sparse_indices(t, window=3, stride=4) for t in range(T)])
print("Exp 3  window=T  : sparse == full?", torch.allclose(full, sparse_big, atol=1e-6))
print("       window=3  : sparse == full?", torch.allclose(full, sparse_small, atol=1e-6))

# --- Experiment 4: fixed pattern vs indexer (content se chunna) --------------
# Ek "needle" position 37 pe chhupi hai. Query usi ko dhoondh rahi hai.
T, d, needle = 64, 16, 37
keys = torch.randn(T, d) * 0.3
query = torch.randn(d)
keys[needle] = query * 2  # needle ka key query se strongly match karta hai
fixed = sparse_indices(T - 1, window=8, stride=16)
small_q, small_k = query[:4], keys[:, :4]  # indexer: sirf 4 dims -> sasta score
indexer_top = (small_k @ small_q).topk(8).indices.sort().values.tolist()
print(f"Exp 4  needle position = {needle}")
print(f"       fixed pattern  ({len(fixed)} keys): {fixed}  -> needle mila? {needle in fixed}")
print(f"       indexer top-8  ({len(indexer_top)} keys): {indexer_top}  -> needle mila? {needle in indexer_top}")

# --- Experiment 5: 3 linear + 1 sparse rhythm --------------------------------
kinds = ["S" if (i + 1) % 4 == 0 else "L" for i in range(12)]
print("Exp 5  12 layers:", " ".join(kinds), f"  -> {kinds.count('L')} linear, {kinds.count('S')} sparse")

# TODO (tumhara kaam):
#  a) Exp 1 me stride=4 ko stride=2 kar do. Ab kitne positions dikhte hain? Compute vs reach ka trade-off kya hai?
#  b) Exp 4 me needle ko position 48 pe le jao (anchor). Fixed pattern ab mila? Ye "luck" kyun hai?
#  c) Repo ke model se verify karo ki layers 4, 8, 12 sparse hain:
#     cd sources/repo && uv run python -c "from glm53_flash.model import *; m=GLM53FlashFromScratch(ModelConfig()); print([type(l.block.attention).__name__ for l in m.layers])"
