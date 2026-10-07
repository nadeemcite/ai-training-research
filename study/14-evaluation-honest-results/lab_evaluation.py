"""Lab 14 — Evaluation: pass@k, paired tests, bootstrap, interference, replication.

Run:  uv run study/14-evaluation-honest-results/lab_evaluation.py     (~3 sec)

Repo ke asli confirmation receipts (har task ka before/after output) aur asli
analysis functions (mcnemar_exact, paired_bootstrap) use hote hain.
"""

import json
import math
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2] / "sources" / "repo"
sys.path[:0] = [str(REPO / "scripts")]

from analyze_rl_variants import mcnemar_exact, paired_bootstrap  # noqa: E402

RUNS = REPO / "artifacts" / "receipts" / "runs"
load = lambda name: json.loads((RUNS / f"{name}.json").read_text())  # noqa: E731

# --- Experiment 1: greedy pass@1 — before vs after, same 24 confirm tasks ----
before, after = load("confirm-greedy-pretrain-0100"), load("confirm-greedy-rl-0096")
b = {e["task_id"]: e["evaluation"]["passed"] for e in before["episodes"]}
a = {e["task_id"]: e["evaluation"]["passed"] for e in after["episodes"]}
ids = sorted(b)
print(f"Exp 1  greedy pass@1 (confirm, 3 RL families): before {sum(b.values())}/24  ->  after {sum(a.values())}/24")
for fam in ("increment", "double", "even"):
    fb = sum(b[i] for i in ids if fam in i)
    fa = sum(a[i] for i in ids if fam in i)
    print(f"       {fam:9}  {fb}/8 -> {fa}/8")

# --- Experiment 2: paired test (McNemar exact) ------------------------------
left, right = [b[i] for i in ids], [a[i] for i in ids]
gains, losses, p = mcnemar_exact(left, right)
print(f"Exp 2  paired: {gains} tasks gained, {losses} lost  ->  exact p = {p:.7f}   (= 2 / 2^16 = {2 / 2**16:.7f})")
lo, hi = paired_bootstrap(left, right)
print(f"       paired bootstrap 95% interval for the gain: [{lo:+.1%}, {hi:+.1%}]")

# --- Experiment 3: pass@k — unbiased estimator ------------------------------


def pass_at_k(n: int, c: int, k: int) -> float:
    """n samples me se c sahi. Chance ki k random samples me kam se kam 1 sahi ho (Codex paper)."""
    if n - c < k:
        return 1.0
    return 1.0 - math.comb(n - c, k) / math.comb(n, k)


p8_before, p8_after = load("confirm-pass8-pretrain-0100"), load("confirm-pass8-rl-0096")
print("Exp 3  sampled (temperature 0.35, 8 samples/task), sab 8 families, 64 tasks:")
for name, d in (("before", p8_before), ("after", p8_after)):
    eps = d["episodes"]
    for k in (1, 8):
        est = sum(pass_at_k(8, sum(s["evaluation"]["passed"] for s in e["samples"]), k) for e in eps) / len(eps)
        print(f"       {name:6} pass@{k} = {est:.1%}")
print(f"       (receipt summary: pass@8 before {p8_before['summary']['pass_at_k']:.1%}, after {p8_after['summary']['pass_at_k']:.1%})")

# --- Experiment 4: interference — trained vs untrained families -------------
print("Exp 4  per-family sampled exact rate (8 tasks x 8 samples):")
trained = {"increment", "double", "even"}
for fam in sorted({e["family"] for e in p8_before["episodes"]}, key=lambda f: (f not in trained, f)):
    rate = lambda d: sum(s["evaluation"]["passed"] for e in d["episodes"] if e["family"] == fam for s in e["samples"])  # noqa: E731
    rb, ra = rate(p8_before), rate(p8_after)
    arrow = "↑" if ra > rb else ("↓" if ra < rb else "—")
    print(f"       {'RL ' if fam in trained else '   '}{fam:12} {rb:>2}/64 -> {ra:>2}/64  {arrow}")

# --- Experiment 5: "winner" jo replicate nahi hua (slides 72–74 ka data) -----
screen = {"binary": 5, "partial reward": 5, "no invalid penalty": 5, "hard invalid penalty": 5,
          "temperature 0.20": 7, "temperature 0.80": 6, "group size 4": 8, "group size 16": 6}
print("Exp 5  screen (1 seed, dev tasks solved /20):", ", ".join(f"{k} {v}" for k, v in screen.items()))
confirm = {31415: (12, 13), 27182: (14, 13), 16180: (11, 8)}  # (group 8, group 4) out of 40
print("       confirm (3 fresh seeds, 40 tasks):")
for seed, (g8, g4) in confirm.items():
    print(f"         seed {seed}: group 8 = {g8}/40, group 4 = {g4}/40  ({g4 - g8:+d})")
mean8 = sum(v[0] for v in confirm.values()) / 3
mean4 = sum(v[1] for v in confirm.values()) / 3
print(f"       mean: group 8 = {mean8:.1f}, group 4 = {mean4:.1f}  ->  screen ka 'winner' confirm me haar gaya")

# TODO (tumhara kaam):
#  a) pass_at_k(8, 1, 8) aur pass_at_k(8, 1, 1) nikaalo. Ek hi sahi sample, do alag numbers. Kyun?
#  b) Exp 2: agar 10 gains aur 6 losses hote, to p kya aata? (mcnemar_exact([..], [..]) se check karo)
#  c) Exp 4: kaunsi families "↓" hain? Kya ye RL ka nuksaan hai ya noise? Kaise pata karoge?
