"""Lab 5 — Softmax attention vs Linear attention (running memory).

Run:  uv run study/05-attention-aur-linear-attention/lab_linear_attention.py
"""

import torch
import torch.nn.functional as F

torch.manual_seed(0)


def softmax_attention(q, k, v):
    """Classic causal attention. q, k, v: [T, d]. Har token pichle SAARE tokens ko dekhta hai."""
    T, d = q.shape
    scores = q @ k.T / d**0.5  # [T, T]  <- yahi quadratic matrix hai
    mask = torch.triu(torch.ones(T, T, dtype=torch.bool), diagonal=1)
    weights = torch.softmax(scores.masked_fill(mask, float("-inf")), dim=-1)
    return weights @ v, weights


def phi(x):
    return F.elu(x) + 1.0  # repo ka feature map: hamesha positive


def linear_attention_parallel(q, k, v):
    """Repo jaisa (cumsum) version. Training me yahi chalta hai."""
    q, k = phi(q), phi(k)
    kv = torch.einsum("td,te->tde", k, v).cumsum(dim=0)  # [T, d, d] prefix states
    k_prefix = k.cumsum(dim=0)  # [T, d]
    num = torch.einsum("td,tde->te", q, kv)
    den = torch.einsum("td,td->t", q, k_prefix)[:, None]
    return num / den.clamp_min(1e-6)


def linear_attention_recurrent(q, k, v, decay: float = 1.0):
    """Same cheez, token-by-token. State S ka size [d, d] hamesha fixed rehta hai.

    decay < 1 ho to purani yaadein dheere-dheere fade hoti hain (KDA/Mamba jaisa idea).
    Repo me decay nahi hai (= 1.0).
    """
    q, k = phi(q), phi(k)
    d = q.shape[1]
    S = torch.zeros(d, v.shape[1])  # running key-value memory
    z = torch.zeros(d)  # running key sum (normaliser)
    outs = []
    for t in range(q.shape[0]):
        S = decay * S + torch.outer(k[t], v[t])
        z = decay * z + k[t]
        outs.append((q[t] @ S) / (q[t] @ z).clamp_min(1e-6))
    return torch.stack(outs)


# --- Experiment 1: softmax attention ki weights matrix -----------------------
T, d = 5, 8
q, k, v = torch.randn(T, d), torch.randn(T, d), torch.randn(T, d)
_, w = softmax_attention(q, k, v)
print("Exp 1  causal attention weights (row = query token, col = key token):")
for row in w:
    print("       " + "  ".join(f"{x:.2f}" for x in row.tolist()))

# --- Experiment 2: parallel (cumsum) == recurrent (loop) --------------------
par = linear_attention_parallel(q, k, v)
rec = linear_attention_recurrent(q, k, v)
print("Exp 2  parallel == recurrent?", torch.allclose(par, rec, atol=1e-5))

# --- Experiment 3: memory ka hisaab (per head, per layer) --------------------
d_head = 32  # repo: 192 / 6 heads
print("Exp 3  context T   softmax scores T*T     linear state d*d")
for T_ in [192, 8_000, 128_000, 1_000_000]:
    print(f"       {T_:>9,}   {T_ * T_:>18,}   {d_head * d_head:>15,}")

# --- Experiment 4: recall test — memory compress hone ki keemat --------------
# N (key, value) pairs store karo, fir key_i se query karo: kya value_i wapas milti hai?
d = 32


def recall(n_pairs: int, mode: str, decay: float = 1.0) -> float:
    keys = F.normalize(torch.randn(n_pairs, d), dim=-1) * 4
    vals = torch.randn(n_pairs, d)
    hits = 0
    for i in range(n_pairs):
        q_ = keys[i : i + 1]
        if mode == "softmax":
            w_ = torch.softmax(q_ @ keys.T / d**0.5 * 4, dim=-1)
            out = w_ @ vals
        else:
            out = linear_attention_recurrent(torch.cat([keys, q_]), torch.cat([keys, q_]),
                                             torch.cat([vals, torch.zeros(1, d)]), decay)[-1:]
        hits += int((F.cosine_similarity(out, vals, dim=-1).argmax() == i).item())
    return hits / n_pairs


print("Exp 4  pairs  softmax-recall  linear-recall")
for n in [4, 16, 64]:
    print(f"       {n:>5}  {recall(n, 'softmax'):>13.0%}  {recall(n, 'linear'):>13.0%}")

# --- Experiment 5: decay -> recent yaad, purana bhool ------------------------
n = 32
keys = F.normalize(torch.randn(n, d), dim=-1) * 4
vals = torch.randn(n, d)
print(f"Exp 5  decay=0.8, {n} pairs, kaunse wapas mile? (0 = sabse purana, {n - 1} = sabse naya)")
found = []
for i in range(n):
    out = linear_attention_recurrent(torch.cat([keys, keys[i : i + 1]]), torch.cat([keys, keys[i : i + 1]]),
                                     torch.cat([vals, torch.zeros(1, d)]), decay=0.8)[-1:]
    found.append("✓" if F.cosine_similarity(out, vals, dim=-1).argmax().item() == i else "·")
print("       " + "".join(found))

# --- Experiment 6: asli bottleneck kahan hai? -------------------------------
# Same [d, d] state, lekin phi (elu+1) aur denominator hata do: S = sum(k v^T), out = q S.
# elu+1 saare keys ko positive bana deta hai -> sab keys ek-doosre jaise dikhte hain.
print("Exp 6  pairs  raw outer-product memory recall (no phi)")
for n in [4, 16, 64]:
    keys = F.normalize(torch.randn(n, d), dim=-1)
    vals = torch.randn(n, d)
    out = keys @ (keys.T @ vals)
    acc = (F.cosine_similarity(out[:, None], vals[None], dim=-1).argmax(-1) == torch.arange(n)).float().mean()
    print(f"       {n:>5}  {acc:>13.0%}")

# TODO (tumhara kaam):
#  a) d = 128 kar do. Exp 4 (linear) aur Exp 6 (raw) me se kiska recall sudhra? Kyun?
#  b) Exp 5 me decay = 0.95 aur 0.5 try karo. Kitne recent pairs yaad rehte hain?
