"""Lab 12 — RL ka environment: verifier, reward design, aur reward hacking.

Run:  uv run study/12-rl-executable-rewards/lab_rewards.py     (~2 sec)

Repo ka asli verifier (evaluator.py), reward function (train_rl.py) aur final RL run ka
saved data (har rollout + reward) use hota hai.
"""

import json
import random
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[2] / "sources" / "repo"
sys.path[:0] = [str(REPO), str(REPO / "scripts")]

from glm53_flash.evaluator import evaluate_source  # noqa: E402
from glm53_flash.tasks import frozen_tasks  # noqa: E402
from train_rl import reward_for  # noqa: E402

task = next(t for t in frozen_tasks("rl") if t.family == "increment")

# --- Experiment 1: environment — model ko kya milta hai, kya chhupa hai -----
print("Exp 1  model ko sirf ye prompt milta hai:")
print("       " + task.prompt.replace("\n", "\n       "))
print(f"       chhupe hue tests (model ko kabhi nahi dikhte): {list(task.cases)}")

# --- Experiment 2: verifier + reward, alag-alag jawabon pe ---------------------
candidates = {
    "sahi":               "\n    return x + 1\n",
    "galat (valid)":      "\n    return x + 2\n",
    "aadha sahi":         "\n    return x + 1 if x > 0 else 1\n",
    "invalid Python":     "\n    return x * * 0 0\n",
    "import (khatarnak)": "\n    import os\n    return x + 1\n",
    "loop (mana hai)":    "\n    for i in range(1):\n        return x + 1\n",
}
print("Exp 2  jawab                status    tests  binary  case-fraction")
for name, completion in candidates.items():
    ev = evaluate_source(task, task.prompt + completion)
    rb, _ = reward_for(task, completion, "binary", invalid_penalty=-0.1, exact_bonus=0.0)
    rc, _ = reward_for(task, completion, "case-fraction", invalid_penalty=-0.1, exact_bonus=0.0)
    print(f"       {name:20} {ev.status:8}  {ev.tests_passed}/{ev.tests_total}    {rb:+.2f}    {rc:+.2f}"
          + (f"   ({ev.message})" if ev.message else ""))

# --- Experiment 3: reward hacking — tests ratke "jeetna" ---------------------
hack = "\n    return {-3: -2, 0: 1, 7: 8}[x]\n"  # sirf 3 test inputs ka jawab yaad kar liya
ev = evaluate_source(task, task.prompt + hack)
print(f"Exp 3  hack: return {{-3: -2, 0: 1, 7: 8}}[x]  -> repo verifier: {ev.status}, reward "
      f"{reward_for(task, hack, 'binary', invalid_penalty=-0.1, exact_bonus=0.0)[0]:+.1f}  😱")


def stronger_verifier(source: str, n_random: int = 20) -> bool:
    """Fixed tests + har baar naye random inputs (model ko pehle se pata nahi ho sakte)."""
    if not evaluate_source(task, task.prompt + source).passed:
        return False
    namespace: dict = {}
    exec(task.prompt + source, namespace)  # yahan sirf hamare apne trusted candidates hain
    fn = namespace[task.entry_point]
    rng = random.Random()
    for _ in range(n_random):
        x = rng.randint(-1000, 1000)
        try:
            if fn(x) != x + 1:
                return False
        except Exception:
            return False
    return True


print(f"       stronger verifier (random hidden inputs): sahi -> {stronger_verifier(candidates['sahi'])}, "
      f"hack -> {stronger_verifier(hack)}")

# --- Experiment 4: asli RL run — ek group ke 16 attempts aur unke rewards ----
receipt = json.loads((REPO / "artifacts/receipts/runs/glm53-executable-rloo-diverse-001/training-receipt.json").read_text())
groups = receipt["groups_detail"]
g = next(x for x in groups if x["updated"] and x["family"] == "double")
print(f"Exp 4  asli run, group {g['group']} ({g['task_id']}), temperature {receipt['temperature']}:")
counts = Counter((s["completion"].strip(), s["reward"]) for s in g["samples"])
for (text, reward), n in counts.most_common(5):
    print(f"       {n:>2}x  reward {reward:+.1f}  {text[:40]!r}")

# --- Experiment 5: sparse reward — kitne groups se kuch seekha hi nahi? -----
same = [x for x in groups if not x["updated"]]
kinds = Counter(f"sab {x['rewards'][0]:+.1f}" for x in same)
print(f"Exp 5  {len(groups)} groups me se {len(same)} me sab 16 rewards barabar the -> koi update nahi "
      f"({dict(kinds)})")
early = sum(x["exact_rollouts"] for x in groups[:24]) / (24 * 16)
late = sum(x["exact_rollouts"] for x in groups[-24:]) / (24 * 16)
print(f"       training ke dauraan sahi rollouts: pehle 24 groups {early:.0%}  ->  aakhri 24 groups {late:.0%}")

# TODO (tumhara kaam):
#  a) Exp 2 me apna ek "aadha sahi" jawab likho jo 2/3 tests pass kare. Binary aur case-fraction reward kya dete hain?
#  b) Exp 3 jaisa hack 'double' family ke liye likho (tests: -4 -> -8, 0 -> 0, 6 -> 12). Kya repo verifier pass karta hai?
#  c) Exp 5: agar reward sirf "+1 sahi / 0 baaki" ho aur model shuru me 0% sahi ho, to kya RL kabhi shuru hoga? Kyun?
