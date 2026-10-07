"""Lab 2 — Embedding lookup, logits, softmax aur weight tying.

Run:  uv run study/02-embeddings-aur-output-head/lab_embeddings.py
"""

import torch
import torch.nn as nn
import torch.nn.functional as F

torch.manual_seed(0)
VOCAB, DIM = 260, 192  # same as the repo ModelConfig

# --- Experiment 1: embedding = sirf ek lookup table -------------------------
emb = nn.Embedding(VOCAB, DIM)
ids = torch.tensor([[104, 105, 106]])  # "def"
vectors = emb(ids)
print("Exp 1  ids shape", tuple(ids.shape), "-> vectors shape", tuple(vectors.shape))
assert torch.equal(vectors[0, 0], emb.weight[104]), "lookup = row uthana"

# --- Experiment 2: hidden vector -> logits -> probabilities ----------------
head = nn.Linear(DIM, VOCAB, bias=False)
hidden = vectors[0, -1]  # maan lo transformer ne ye last hidden state diya
logits = head(hidden)
probs = F.softmax(logits, dim=-1)
print(f"Exp 2  logits {tuple(logits.shape)}, probs sum = {probs.sum():.4f}")
print("       untrained model ka top guess:", probs.argmax().item(), "(random hi hoga)")

# --- Experiment 3: weight tying — parameter bachat --------------------------
untied = sum(p.numel() for p in [emb.weight, head.weight])
head.weight = emb.weight  # GLM53FlashFromScratch me bhi yahi line hai
tied = sum(p.numel() for p in {id(p): p for p in [emb.weight, head.weight]}.values())
print(f"Exp 3  untied={untied:,}  tied={tied:,}  bachat={untied - tied:,}")
assert head.weight.data_ptr() == emb.weight.data_ptr(), "dono ek hi memory hai"

# --- Experiment 4: chhota bigram model train karo (tied vs untied) ---------
# Ye 'transformer ke bina' next-byte predictor hai: pichla byte dekh ke agla guess.
text = "def inc(x):\n    return x + 1\ndef dbl(x):\n    return x * 2\n" * 20
data = torch.tensor([4 + b for b in text.encode()])
x, y = data[:-1], data[1:]  # input aur target bas 1 position shifted


def train_bigram(tied: bool) -> None:
    torch.manual_seed(0)
    e = nn.Embedding(VOCAB, DIM)
    out = nn.Linear(DIM, VOCAB, bias=False)
    if tied:
        out.weight = e.weight
    for p in (e.weight, out.weight):
        nn.init.normal_(p, std=0.02)  # repo jaisa init
    params = {id(p): p for p in [e.weight, out.weight]}.values()
    opt = torch.optim.AdamW(params, lr=1e-2)
    for step in range(201):
        loss = F.cross_entropy(out(e(x)), y)
        opt.zero_grad()
        loss.backward()
        opt.step()
    with torch.no_grad():  # seekhne ke baad: 'r' ke baad kya aata hai?
        p = F.softmax(out(e(torch.tensor(4 + ord("r")))), dim=-1).topk(3)
        guesses = [(chr(i - 4), round(v, 2)) for v, i in zip(p.values.tolist(), p.indices.tolist())]
    print(f"Exp 4  tied={tied!s:5}  final loss {loss.item():.3f}  'r' ke baad top-3: {guesses}")


train_bigram(tied=False)
train_bigram(tied=True)
# Sahi jawab: "return" me r ke baad 'e' ya 'n' aata hai.
# Tied bigram 'r' -> 'r' kyun bolta hai? Reading 04 dekho.

# TODO (tumhara kaam):
#  a) DIM = 8 kar do — kya untied model ab bhi seekhta hai? Kyun?
#  b) Text me "rr" kahin nahi hai, phir bhi tied model 'r' guess karta hai — apne shabdon me likho kyun.
