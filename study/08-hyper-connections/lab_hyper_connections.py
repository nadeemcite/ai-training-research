"""Lab 8 — Hyper-connections: ek residual highway ki jagah 4 streams.

Run:  uv run study/08-hyper-connections/lab_hyper_connections.py          (~3 sec)
      uv run study/08-hyper-connections/lab_hyper_connections.py --run    (+ ~4 min: 1 vs 4 streams training)

Repo ka asli HyperConnection class import hota hai.
"""

import sys
from pathlib import Path

import torch
import torch.nn as nn
import torch.nn.functional as F

REPO = Path(__file__).resolve().parents[2] / "sources" / "repo"
sys.path[:0] = [str(REPO), str(REPO / "scripts")]

from glm53_flash import ByteTokenizer, GLM53FlashFromScratch, ModelConfig  # noqa: E402
from glm53_flash.model import HybridBlock, HyperConnection  # noqa: E402

torch.manual_seed(0)

# --- Experiment 1: plain residual — "highway" jo kabhi band nahi hota --------
# 12 layers jo apne input ko sirf thoda sa badalte hain. Residual ke bina vs saath.
x0 = torch.randn(1, 192)
W = [nn.Linear(192, 192) for _ in range(12)]
for w in W:
    nn.init.normal_(w.weight, std=0.02)  # repo jaisa chhota init
with torch.no_grad():
    h_plain, h_res = x0.clone(), x0.clone()
    for w in W:
        h_plain = w(h_plain)              # bina residual: x = f(x)
        h_res = h_res + w(h_res)          # residual:      x = x + f(x)
cos = lambda a, b: F.cosine_similarity(a, b).item()  # noqa: E731
print(f"Exp 1  12 layers ke baad input se similarity:  bina residual {cos(h_plain, x0):+.3f}   residual ke saath {cos(h_res, x0):+.3f}")

# --- Experiment 2: repo ka HyperConnection — 4 streams ka mix aur route -----
cfg = ModelConfig()
hc = HyperConnection(cfg, HybridBlock(cfg, sparse=False))
read = torch.softmax(hc.input_logits, 0)
write = torch.softmax(hc.output_logits, 0)
print("Exp 2  shuruaati weights (seekhe jaate hain):")
print("       read  (kis stream se kitna padhna):  ", [round(v, 3) for v in read.tolist()], " sum =", round(read.sum().item(), 3))
print("       write (update kis stream me kitna): ", [round(v, 3) for v in write.tolist()], " sum =", round(write.sum().item(), 3))

# --- Experiment 3: shapes — model ke andar 4 copies chalti hain --------------
model = GLM53FlashFromScratch(cfg)
ids = torch.tensor([ByteTokenizer().encode("def f(x):", bos=True)])
with torch.no_grad():
    embedded = model.embedding(ids)
    streams = embedded.unsqueeze(2).expand(-1, -1, cfg.streams, -1).contiguous()
    print(f"Exp 3  embedding {tuple(embedded.shape)} -> streams {tuple(streams.shape)}  [batch, tokens, STREAMS, dim]")
    print(f"       shuru me 4 streams bilkul same? {torch.equal(streams[:, :, 0], streams[:, :, 3])}")
    for layer in model.layers[:6]:
        streams, _ = layer(streams)
    spread = (streams[:, :, 0] - streams[:, :, 3]).norm() / streams[:, :, 0].norm()
    print(f"       6 layers ke baad stream 0 vs 3 ka fark: {spread:.1%}  (write weights alag hain, isliye streams alag ho jaate hain)")
    print(f"       end me: streams.mean(dim=2) -> {tuple(streams.mean(dim=2).shape)} -> final_norm -> output head")

# --- Experiment 4: repo ka ek quirk — identity do baar judti hai -----------
# HybridBlock khud `x + attention + MoE` return karta hai, aur HyperConnection usme
# stream ko PHIR se jodta hai: streams + block(mixed) * write. Isliye stream har layer badhta hai.
cfg1 = ModelConfig(streams=1)
block = HybridBlock(cfg1, sparse=False)
x = torch.randn(2, 5, 192)
with torch.no_grad():
    via_hc, _ = HyperConnection(cfg1, block)(x.unsqueeze(2))
    inner, _ = block(x)
print(f"Exp 4  streams=1: output == x + block(x), jahan block(x) = x + attn + MoE  ->  2x + ...?  "
      f"{torch.allclose(via_hc.squeeze(2), x + inner, atol=1e-5)}")
for s_count in (1, 4):
    torch.manual_seed(0)
    m = GLM53FlashFromScratch(ModelConfig(streams=s_count))
    with torch.no_grad():
        st = m.embedding(ids).unsqueeze(2).expand(-1, -1, s_count, -1).contiguous()
        start = st.mean(2).norm()
        for layer in m.layers:
            st, _ = layer(st)
    print(f"       streams={s_count}: 12 layers ke baad residual stream ka size {st.mean(2).norm() / start:,.1f}x (init pe)")

# --- Experiment 5: mHC ka "manifold constraint" — kyun zaroori hai -----------
# Released GLM/DeepSeek mHC: streams ke beech ek 4x4 mixing MATRIX hota hai (hamare repo me nahi).
# 12 layers ke matrices multiply hote hain. Free matrix vs doubly-stochastic (har row aur column ka sum = 1).


def sinkhorn(logits: torch.Tensor, iters: int = 20) -> torch.Tensor:
    m = logits.exp()
    for _ in range(iters):
        m = m / m.sum(dim=1, keepdim=True)  # rows sum = 1
        m = m / m.sum(dim=0, keepdim=True)  # columns sum = 1
    return m


torch.manual_seed(1)
free, ds = torch.eye(4), torch.eye(4)
signal = torch.ones(4)
for _ in range(12):
    logits = torch.randn(4, 4)
    free = (torch.eye(4) + 0.5 * logits) @ free   # bina constraint
    ds = sinkhorn(logits) @ ds                    # Sinkhorn se doubly stochastic
print(f"Exp 5  12 layers ke baad stream signal ka size:  free matrix {(free @ signal).norm():.1f}   doubly-stochastic {(ds @ signal).norm():.2f}  (shuru: {signal.norm():.2f})")

# --- Experiment 6 (optional --run): kya 4 streams sach me madad karte hain? --
if "--run" in sys.argv:
    from train_pretrain import batch_for

    tok = ByteTokenizer()

    def heldout_loss(streams: int, seed: int) -> float:
        c = ModelConfig(dim=96, layers=4, heads=4, expert_hidden=192, streams=streams)
        torch.manual_seed(seed)
        m = GLM53FlashFromScratch(c)
        opt = torch.optim.AdamW(m.parameters(), lr=1e-3, betas=(0.9, 0.95), weight_decay=0.1)
        for step in range(150):
            xb, yb, _ = batch_for(tok, step=step, batch_size=16, sequence_length=128, seed=42, device=torch.device("cpu"))
            loss = F.cross_entropy(m(xb)[0].reshape(-1, 260), yb.reshape(-1), ignore_index=-100)
            opt.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(m.parameters(), 1.0)
            opt.step()
        xb, yb, _ = batch_for(tok, step=0, batch_size=64, sequence_length=128, seed=999, device=torch.device("cpu"))
        with torch.no_grad():
            return F.cross_entropy(m(xb)[0].reshape(-1, 260), yb.reshape(-1), ignore_index=-100).item()

    print("Exp 6  2.2M model, 150 steps, held-out loss (kam = behtar):")
    for seed in (1, 2, 3):
        s1, s4 = heldout_loss(1, seed), heldout_loss(4, seed)
        print(f"       seed {seed}:  1 stream {s1:.4f}   4 streams {s4:.4f}   -> {'4 jeeta' if s4 < s1 else '1 jeeta'}")

# TODO (tumhara kaam):
#  a) Exp 1 me std=0.02 ko 0.2 kar do. Ab residual ke saath similarity kya hui? Kyun?
#  b) Exp 5 me sinkhorn ke baad ds.sum(dim=0) aur ds.sum(dim=1) print karo. Kya sab 1 hain?
#  c) Exp 6 (--run) ka result dekh ke ek imaandaar line likho: "4 streams ___".
