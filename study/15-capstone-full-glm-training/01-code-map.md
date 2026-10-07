<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 15 — Capstone: poora GLM-5.3-Flash ek file me 🎓](README.md) › Reading 1 / 6
<!-- /nav:top -->

# 01 · Code map — har section kis chapter se

`glm53_full.py` (~690 lines, comments ke saath) self-contained hai: `sources/repo` import **nahi** karti. Har section ke upar ek header hai jo chapter batata hai.

| Section (file me order) | Kya hai | Chapter |
|---|---|---|
| `ByteTokenizer` | 1 byte = 1 token, vocab 263 (256 + 4 special + 3 image) | [01](../01-tokens-aur-tokenizer/) |
| `Config`, `PRESETS` | tiny (~2.2M, CPU) aur full (~25.7M, GPU) | [02](../02-embeddings-aur-output-head/), [10](../10-pretraining-loop/) |
| `RMSNorm` | Size ~1, direction same | [03](../03-rmsnorm/) |
| `apply_rope` | Pairs ko position × frequency se ghumao | [04](../04-rope-position/) |
| `LinearAttention` | φ = elu+1, cumsum running state | [05](../05-attention-aur-linear-attention/) |
| `SparseAttention` | Local window + strided anchors, causal | [06](../06-sparse-attention-aur-hybrid-rhythm/) |
| `Expert`, `SparseMoE` | SwiGLU experts (batched, GPU-friendly), top-2 router, shared expert, **[FIX-07]** balance loss | [07](../07-mixture-of-experts/) |
| `HybridBlock`, `HyperConnection` | 4 streams, read/write, **[FIX-08]** identity once | [08](../08-hyper-connections/) |
| `GLM53Flash` | Tied embeddings, `(i+1) % 4 == 0` → sparse | [02](../02-embeddings-aur-output-head/), [06](../06-sparse-attention-aur-hybrid-rhythm/) |
| `VisionEncoder`, `digit_images` | Patches → ViT → 2×2 merge → projector → 16 tokens | [09](../09-vision-image-to-tokens/) |
| `FAMILIES`, `make_task`, `pretrain_batch` | 8 Python families, splits, padding → −100 | [10](../10-pretraining-loop/), [11](../11-research-data-experiments/) |
| `verify`, `parseable` | AST sandbox + fixed tests + **[FIX-12]** random hidden tests | [12](../12-rl-executable-rewards/) |
| `generate` | Greedy ya sampled group generation | [02](../02-embeddings-aur-output-head/), [12](../12-rl-executable-rewards/) |
| `pretrain` | predict → cross-entropy → backward → clip → AdamW | [10](../10-pretraining-loop/) |
| `reward`, `leave_one_out`, `completion_logprob`, `rl` | Executable reward, RLOO, last block + head | [12](../12-rl-executable-rewards/), [13](../13-rloo-advantage-last-block/) |
| `pass_at_k`, `evaluate`, `mcnemar` | Confirm split ek baar, paired test | [14](../14-evaluation-honest-results/) |
| `vision_stage` | Digit reader, answer-only loss | [09](../09-vision-image-to-tokens/) |
| `main` | Stages + JSON receipt | sab |

## Repo se kya alag hai (jaan-boojh ke)

| Cheez | Repo | Capstone | Kyun |
|---|---|---|---|
| MoE | Python loop: har expert sirf apne tokens pe (`torch.where` + `index_add`) | **Batched**: saare experts ek matmul me + zero gates | Mac GPU pe 2.5× tez (Reading 03). Math same, lekin unchune experts ka compute bhi hota hai |
| Sparse attention | Gather (sirf chuni keys ka compute) | Full T×T scores + **mask** | Code chhota hai aur math same hai. Compute bachat sirf gather me hoti hai |
| Vision transformer | Custom blocks, Q/K norm | `nn.TransformerEncoderLayer` | Chhota code. Idea same (bidirectional) |
| Vision LM | Same LM class, tiny config | Same `GLM53Flash`, tiny config | — |
| Data/tasks | Same families, same seeds | Same (+ har family ka trusted reference function) | Random tests ke liye |
| 3 issues | Present | **Fixed** | Reading 02 |

Agar tumne chapters ke labs kiye hain, to har function pehchaana hua lagega. **Is file ko upar se neeche ek baar padho**, ye pure course ka revision hai.

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [Topic 15 — Capstone: poora GLM-5.3-Flash ek file me 🎓](README.md) | 📚 [Topic 15 overview](README.md) | [02 · Teen fixes — course me jo mila, wo yahan theek hai](02-three-fixes.md) ➡️ |
<!-- /nav:bottom -->
