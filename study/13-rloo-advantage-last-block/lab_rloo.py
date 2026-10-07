"""Lab 13 — RLOO: advantage se update tak, aur CPU pe ek chhota RL run.

Run:  uv run study/13-rloo-advantage-last-block/lab_rloo.py           (~3 sec: math + asli run ka data)
      uv run study/13-rloo-advantage-last-block/lab_rloo.py --run     (+ ~2.5 min: mini pretrain -> RL, CPU)

Repo ke asli functions: leave_one_out, completion_log_probabilities, reward_for, generate_group.
"""

import json
import sys
import time
from pathlib import Path

import torch
import torch.nn.functional as F

REPO = Path(__file__).resolve().parents[2] / "sources" / "repo"
sys.path[:0] = [str(REPO), str(REPO / "scripts")]

from glm53_flash import ByteTokenizer, GLM53FlashFromScratch, ModelConfig  # noqa: E402
from glm53_flash.evaluator import evaluate_source  # noqa: E402
from glm53_flash.runtime import generate_group  # noqa: E402
from glm53_flash.tasks import frozen_tasks  # noqa: E402
from train_rl import completion_log_probabilities, leave_one_out, reward_for, schedule  # noqa: E402

tok = ByteTokenizer()
cpu = torch.device("cpu")

# --- Experiment 1: leave-one-out advantage, haath se -------------------------
rewards = [1.0, 0.0, -0.1, 1.0]
adv = leave_one_out(rewards)
print("Exp 1  rewards     ", rewards)
for i, (r, a) in enumerate(zip(rewards, adv)):
    others = rewards[:i] + rewards[i + 1:]
    print(f"       attempt {i}: {r:+.1f} - mean{others} = {r:+.1f} - {sum(others) / 3:+.3f} = {a:+.3f}")
print(f"       advantages ka sum = {sum(adv):+.3f}  (hamesha ~0: kuch upar, kuch neeche)")

# --- Experiment 2: sab barabar -> advantage zero -> kuch nahi seekha --------
for case in ([1.0] * 4, [-0.1] * 4):
    print(f"Exp 2  rewards {case} -> advantages {[round(a, 3) for a in leave_one_out(case)]}")

# --- Experiment 3: RLOO vs GRPO normalisation (same group) -------------------
receipt = json.loads((REPO / "artifacts/receipts/runs/glm53-executable-rloo-diverse-001/training-receipt.json").read_text())
group = next(g for g in receipt["groups_detail"] if g["updated"] and g["family"] == "double")
r = torch.tensor(group["rewards"])
rloo = torch.tensor(leave_one_out(group["rewards"]))
grpo = (r - r.mean()) / (r.std() + 1e-6)
print(f"Exp 3  asli group {group['group']} ({group['task_id']}), 16 rewards: {sorted(set(group['rewards']))} values")
for value in sorted(set(group["rewards"]), reverse=True):
    i = group["rewards"].index(value)
    print(f"       reward {value:+.1f}:  RLOO advantage {rloo[i]:+.3f}   GRPO advantage {grpo[i]:+.3f}")
print(f"       (saved receipt ka advantage bhi: {group['advantages'][group['rewards'].index(1.0)]:+.3f} for +1.0)")

# --- Experiment 4: policy-gradient loss ka sign -----------------------------
# loss = -(advantage * log_prob).mean().  Gradient descent loss ghatata hai =>
#   advantage > 0: log_prob BADHAO (attempt zyada likely),  advantage < 0: log_prob GHATAO.
logit = torch.zeros(3, requires_grad=True)  # 3 possible "attempts"
lp = torch.log_softmax(logit, 0)
loss = -(torch.tensor([+0.9, -0.3, -0.6]) * lp).mean()
loss.backward()
print(f"Exp 4  advantages [+0.9, -0.3, -0.6] -> gradient step direction {[round(-g, 3) for g in logit.grad.tolist()]}")
print("       (positive = us attempt ki probability badhegi)")

# --- Experiment 5: kaunse parameters train hote hain? (last-block-head) -----
model = GLM53FlashFromScratch(ModelConfig())
for p in model.parameters():
    p.requires_grad = False
for module in (model.layers[-1], model.final_norm, model.embedding):
    for p in module.parameters():
        p.requires_grad = True
trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
total = sum(p.numel() for p in model.parameters())
print(f"Exp 5  last block + final norm + tied embedding/head: {trainable:,} / {total:,} = {trainable / total:.1%}  "
      f"(repo receipt: {receipt['trainable_parameters']:,})")

# --- Experiment 6 (optional --run): CPU pe asli RLOO --------------------------
if "--run" in sys.argv:
    sys.path.insert(0, str(REPO / "scripts"))
    from train_pretrain import batch_for

    families = {"increment", "double", "even"}
    dev = [t for t in frozen_tasks("dev", per_family=4) if t.family in families]

    def sampled_exact(m) -> int:
        ok = 0
        for i, task in enumerate(dev):
            for g in generate_group(m, tok, task, group_size=8, max_new_tokens=32, temperature=0.35, sample=True, seed=7 + i):
                ok += evaluate_source(task, task.prompt + g["completion"]).passed
        return ok

    cfg = ModelConfig(dim=96, layers=4, heads=4, expert_hidden=192)
    torch.manual_seed(42)
    m = GLM53FlashFromScratch(cfg)
    opt = torch.optim.AdamW(m.parameters(), lr=1e-3, betas=(0.9, 0.95), weight_decay=0.1)
    started = time.perf_counter()
    for step in range(120):  # thoda sa pretraining: "kuch aata hai, sab nahi" (repo ne bhi step 100 chuna tha)
        m.train()
        x, y, _ = batch_for(tok, step=step, batch_size=16, sequence_length=128, seed=42, device=cpu)
        loss = F.cross_entropy(m(x)[0].reshape(-1, 260), y.reshape(-1), ignore_index=-100)
        opt.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(m.parameters(), 1.0)
        opt.step()
    print(f"Exp 6  pretraining 120 steps ({time.perf_counter() - started:.0f}s). Dev sampled exact: {sampled_exact(m)}/96")

    for p in m.parameters():
        p.requires_grad = False
    train_params = [*m.layers[-1].parameters(), *m.final_norm.parameters(), *m.embedding.parameters()]
    for p in train_params:
        p.requires_grad = True
    opt = torch.optim.AdamW(train_params, lr=1e-4, weight_decay=0.0)
    tasks = [t for t in frozen_tasks("rl", per_family=16) if t.family in families]
    started, updates, exact = time.perf_counter(), 0, 0
    for gi, task in enumerate(schedule(tasks, 48, 31415), 1):
        gens = generate_group(m, tok, task, group_size=16, max_new_tokens=32, temperature=0.35, sample=True, seed=31415 + gi * 17)
        rw = [reward_for(task, g["completion"], "binary", invalid_penalty=-0.1, exact_bonus=0.0)[0] for g in gens]
        exact += sum(v == 1.0 for v in rw)
        if max(rw) - min(rw) > 1e-8 and all(g["token_ids"] for g in gens):  # spread nahi to skip
            m.train()
            opt.zero_grad()
            lp = completion_log_probabilities(m, tok.encode(task.prompt, bos=True), [g["token_ids"] for g in gens], cpu)
            loss = -(torch.tensor(leave_one_out(rw)) * lp).mean()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(train_params, 1.0)
            opt.step()
            updates += 1
        if gi % 16 == 0:
            print(f"       RL group {gi:>2}: updates {updates}, sahi rollouts ab tak {exact}/{gi * 16}  ({time.perf_counter() - started:.0f}s)")
    print(f"       RL ke baad dev sampled exact: {sampled_exact(m)}/96")

# TODO (tumhara kaam):
#  a) Exp 1 me rewards [1, 1, 1, 0] karo. Akele 0 wale attempt ka advantage kitna bada negative hai? Kyun?
#  b) Exp 3: RLOO aur GRPO ke advantages ka RATIO har reward ke liye same hai? Kya ye sirf scaling ka fark hai?
#  c) Exp 6 me lr=1e-4 ko 1e-3 aur 1e-5 karke chalao. Repo ka pilot history (REPORT.md) yaad karo.
