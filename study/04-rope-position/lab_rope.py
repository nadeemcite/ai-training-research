"""Lab 4 — RoPE: vector ko ghuma ke position likhna.

Run:  uv run study/04-rope-position/lab_rope.py
"""

import torch

torch.manual_seed(0)


def apply_rope(q: torch.Tensor, k: torch.Tensor, positions: torch.Tensor | None = None):
    """Same math as sources/repo/glm53_flash/model.py. Shape: [batch, time, heads, head_dim].

    Repo me positions hamesha 0..T-1 hain; yahan `positions` optional hai taaki experiment kar sakein.
    """
    length, width = q.shape[1], q.shape[-1]
    if positions is None:
        positions = torch.arange(length, dtype=torch.float32)
    frequencies = 1.0 / (10000 ** (torch.arange(0, width, 2).float() / width))
    angles = positions[:, None] * frequencies[None, :]
    cos = angles.cos()[None, :, None, :]
    sin = angles.sin()[None, :, None, :]

    def rotate(x):
        even, odd = x[..., 0::2], x[..., 1::2]
        return torch.stack((even * cos - odd * sin, even * sin + odd * cos), dim=-1).flatten(-2)

    return rotate(q), rotate(k)


HEAD_DIM = 32  # repo: dim 192 / 6 heads = 32

# --- Experiment 1: 2D me ek vector ghumao -----------------------------------
v = torch.tensor([[[[1.0, 0.0]]]]).repeat(1, 4, 1, 1)  # same vector, 4 positions
rotated, _ = apply_rope(v, v)
for pos in range(4):
    a, b = rotated[0, pos, 0].tolist()
    print(f"Exp 1  pos {pos}: [1, 0] -> [{a:+.3f}, {b:+.3f}]   length = {(a * a + b * b) ** 0.5:.3f}")

# --- Experiment 2: length (norm) kabhi nahi badalti -------------------------
x = torch.randn(1, 50, 1, HEAD_DIM)
rx, _ = apply_rope(x, x)
print("Exp 2  rotation ke baad lengths same?", torch.allclose(x.norm(dim=-1), rx.norm(dim=-1), atol=1e-5))

# --- Experiment 3: score sirf DOORI (m - n) pe depend karta hai --------------
q = torch.randn(1, 1, 1, HEAD_DIM)
k = torch.randn(1, 1, 1, HEAD_DIM)


def score(q_pos: int, k_pos: int) -> float:
    rq, _ = apply_rope(q, q, torch.tensor([float(q_pos)]))
    rk, _ = apply_rope(k, k, torch.tensor([float(k_pos)]))
    return (rq * rk).sum().item()


for qp, kp in [(5, 3), (105, 103), (1005, 1003), (5, 1)]:
    print(f"Exp 3  query pos {qp:>4}, key pos {kp:>4} (doori {qp - kp}) -> score {score(qp, kp):+.4f}")

# --- Experiment 4: har pair alag speed se ghoomta hai (clock ki suiyan) ------
freqs = 1.0 / (10000 ** (torch.arange(0, HEAD_DIM, 2).float() / HEAD_DIM))
print("Exp 4  pair 0  : har token pe", f"{freqs[0]:.4f} rad  (second ki sui, tez)")
print("       pair 8  : har token pe", f"{freqs[8]:.4f} rad")
print("       pair 15 : har token pe", f"{freqs[15]:.6f} rad  (ghante ki sui, dheemi)")
print(f"       pair 15 ko ek chakkar (2pi) lagane me ~{2 * torch.pi / freqs[15]:,.0f} tokens")

# --- Experiment 5: bina position ke attention ko order nahi pata ------------
# Ek chhota attention: last token baaki tokens ko dekhta hai.
T = 6
xs = torch.randn(1, T, 1, HEAD_DIM)
perm = torch.tensor([3, 0, 4, 2, 1, 5])  # pehle 5 tokens shuffle, last same


def last_token_output(seq: torch.Tensor, use_rope: bool) -> torch.Tensor:
    qq, kk = (apply_rope(seq, seq) if use_rope else (seq, seq))
    weights = torch.softmax((qq[0, -1, 0] * kk[0, :, 0]).sum(-1) / HEAD_DIM**0.5, dim=0)
    return (weights[:, None] * seq[0, :, 0]).sum(0)


for use_rope in (False, True):
    same = torch.allclose(last_token_output(xs, use_rope), last_token_output(xs[:, perm], use_rope), atol=1e-5)
    print(f"Exp 5  rope={use_rope!s:5}  shuffle ke baad bhi output same? {same}")

# TODO (tumhara kaam):
#  a) score(50, 0) aur score(250, 200) print karo. Same kyun hain? Fir score(50, 49) se compare karo.
#  b) Exp 4: base 10000 ko 500000 kar do (Llama 3 yahi use karta hai). Pair 15 ka chakkar kitne tokens ka hua? Lambe context ke liye ye kyun accha hai?
