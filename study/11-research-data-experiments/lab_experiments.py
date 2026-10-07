"""Lab 11 — Research skill: data experiments ko sahi se design, run aur judge karna.

Run:  uv run study/11-research-data-experiments/lab_experiments.py          (~5 sec: saved results ka analysis)
      uv run study/11-research-data-experiments/lab_experiments.py --run    (+ ~90 sec: khud experiment chalao)

Repo ke asli experiment functions aur 10-seed saved results use hote hain.
"""

import itertools
import json
import sys
import warnings
from pathlib import Path

import torch

REPO = Path(__file__).resolve().parents[2] / "sources" / "repo"
sys.path[:0] = [str(REPO)]

from experiments.pretraining_curriculum_order import static_items, train_condition  # noqa: E402
from experiments.pretraining_data_diversity import all_structures, render_example  # noqa: E402

ARTIFACTS = REPO / "artifacts" / "experiments"
warnings.filterwarnings("ignore", message="Converting a tensor with requires_grad")  # repo code ki harmless warning


def paired_sign_flip(a: dict[int, float], b: dict[int, float]) -> tuple[float, float, int]:
    """Exact two-sided paired permutation test (repo jaisa). Return: mean diff, p, kitne seeds me b jeeta."""
    seeds = sorted(a)
    diffs = [b[s] - a[s] for s in seeds]
    observed = abs(sum(diffs))
    flips = list(itertools.product((1, -1), repeat=len(diffs)))
    extreme = sum(abs(sum(d * s for d, s in zip(diffs, signs))) >= observed - 1e-12 for signs in flips)
    return sum(diffs) / len(diffs), extreme / len(flips), sum(d > 0 for d in diffs)


# --- Experiment 1: data kaisa dikhta hai, aur held-out kya hai ----------------
structures = all_structures()
train_pool, eval_pool = structures[:88], structures[88:120]
print(f"Exp 1  kul {len(structures)} program structures -> train {len(train_pool)}, held-out {len(eval_pool)} (kabhi train nahi hue)")
for s in (train_pool[0], eval_pool[0]):
    text, _ = render_example(s, index=0, seed=11)
    tag = "train   " if s in train_pool else "held-out"
    print(f"       [{tag}] {s}: " + text.strip().replace("\n", "  ⏎  "))

# --- Experiment 2: blocked vs interleaved — same data, sirf order alag -------
pool = train_pool[:3]  # sirf 3 structures, taaki pattern dikhe
for mode in ("blocked", "interleaved"):
    order = [pool.index(s) for s, _ in static_items(pool, examples=12, mode=mode)]
    print(f"Exp 2  {mode:11} order: " + " ".join("ABC"[i] for i in order))

# --- Experiment 3: repo ke 10-seed saved results se khud statistics nikalo ---
div = json.loads((ARTIFACTS / "pretraining-data-diversity-200steps-10seed/results.json").read_text())
cur = json.loads((ARTIFACTS / "pretraining-curriculum-order-200steps-10seed/results.json").read_text())


def acc(runs, key, value):
    return {r["seed"]: r["after"]["target_byte_accuracy"] for r in runs if r[key] == value}


repeated8, diverse88 = acc(div["runs"], "diversity", 8), acc(div["runs"], "diversity", 88)
blocked, curriculum = acc(cur["runs"], "condition", "diverse-blocked"), acc(cur["runs"], "condition", "curriculum-8-to-88")
print("Exp 3  sawaal (200 updates, 10 paired seeds)            A -> B mean    diff     p      B jeeta")
for question, a, b in [("Diversity: 8 repeated -> 88 diverse?", repeated8, diverse88),
                       ("Order: blocked -> interleaved?", blocked, diverse88),
                       ("Curriculum: diverse -> 8-to-88 curriculum?", diverse88, curriculum)]:
    diff, p, wins = paired_sign_flip(a, b)
    mean_a, mean_b = (100 * sum(d.values()) / len(d) for d in (a, b))
    print(f"       {question:44} {mean_a:4.1f}% -> {mean_b:4.1f}%  {100 * diff:+5.1f}  {p:.4f}  {wins}/10")

# --- Experiment 4: kitne seeds chahiye? Sabse chhota possible p -------------
print("Exp 4  seeds   sabse chhota possible p (sab seeds ek hi direction me)")
for n in (1, 3, 5, 6, 10):
    print(f"       {n:>5}   {2 / 2 ** n:.4f}" + ("   <- 0.05 ke neeche aa hi nahi sakta!" if 2 / 2**n > 0.05 else ""))

# --- Experiment 5 (optional --run): khud chalao, 3 seeds -------------------
if "--run" in sys.argv:
    print("Exp 5  blocked vs interleaved, 3 seeds x 200 updates (CPU, ~90s)...")
    live = {"diverse-blocked": {}, "diverse-interleaved": {}}
    for seed in (11, 22, 33):
        for cond in live:
            row = train_condition(condition=cond, seed=seed, steps=200, batch_size=24, learning_rate=8e-4,
                                  sequence_length=128, device=torch.device("cpu"),
                                  train_pool=train_pool, eval_pool=eval_pool)
            live[cond][seed] = row["after"]["target_byte_accuracy"]
        print(f"       seed {seed}: blocked {100 * live['diverse-blocked'][seed]:.1f}%  "
              f"interleaved {100 * live['diverse-interleaved'][seed]:.1f}%")
    diff, p, wins = paired_sign_flip(live["diverse-blocked"], live["diverse-interleaved"])
    print(f"       mean diff {100 * diff:+.1f} points, interleaved jeeta {wins}/3, p = {p:.2f}")

# TODO (tumhara kaam):
#  a) Exp 3 ka "Curriculum" result dekho: kya hum keh sakte hain "curriculum bekaar hai"? Ya sirf "fark nahi dikha"?
#  b) Exp 5 (--run) chalao. 3/3 seeds me interleaved jeeta, phir bhi p = 0.25. Ye kaise ho sakta hai? (Exp 4 dekho)
#  c) Report kehta hai "blocked se forgetting hota hai". Is lab me kya measure hua, aur kya NAHI hua?
