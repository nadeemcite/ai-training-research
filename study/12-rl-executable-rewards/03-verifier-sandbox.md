<!-- nav:top -->
[🏠 Course](../README.md) › [Topic 12 — RL with executable rewards + verifier](README.md) › Reading 3 / 6
<!-- /nav:top -->

# 03 · Practical — Verifier: model ka code safely kaise chalayein?

## Khatra 🚨

RL me hum **model ka likha code** apne computer pe `exec()` karte hain. Model kuch bhi likh sakta hai:
```python
import os
os.system("rm -rf ~")      # 😱
```
Ya `while True: pass`, jo training hamesha ke liye atka de. Isliye verifier ka pehla kaam hai **safety**, aur doosra **correctness**.

> Video (31:53): *"...reward hack, which means maybe reading the results instead of learning how to solve them, learning how to hack into Hugging Face or different systems, what happened."*

## Repo ka verifier: 3 deewarein (`evaluator.py`)

### Deewar 1: Code ko chalane se **pehle** padho (AST)

Python ka `ast` module code ko **bina chalaye** ek tree me badal deta hai. Fir har node check hota hai:

```python
DENIED = (ast.Import, ast.ImportFrom, ast.ClassDef, ast.With, ast.Lambda, ast.Global,
          ast.While, ast.For, ast.Try, ast.Raise, ast.Delete, ...)
SAFE_CALLS = {"sum", "len", "abs", "min", "max", "bool", "int", "str"}
```

| Rule | Kya rokta hai |
|---|---|
| Max 2048 bytes | bahut bada code |
| Top level pe sirf ek function, aur sahi naam | extra functions ya helper code |
| `Import` mana hai | `import os`, `import subprocess` |
| `For`, `While` mana hai | infinite loops |
| Attribute access (`x.y`) mana hai | `().__class__.__bases__...` jaise sandbox-escape tricks |
| Dunder names (`__x`) mana hai | `__import__`, `__builtins__` |
| Sirf `SAFE_CALLS` wale function calls | `open()`, `eval()`, `exec()` |
| Recursion mana hai | infinite recursion |

### Deewar 2: Restricted builtins

```python
namespace = {"__builtins__": SAFE_BUILTINS}   # sirf sum, len, abs, min, max, bool, int, str
exec(compile(tree, "candidate.py", "exec"), namespace)
```
Agar kuch AST check se bach bhi gaya, to bhi `open`, `print`, `__import__` jaise functions exist hi nahi karte.

### Deewar 3: Strict testing

```python
for arguments, expected in task.cases:
    actual = function(*arguments)
    passed += int(type(actual) is type(expected) and actual == expected)
```

`type(actual) is type(expected)` ka matlab: `True` aur `1` alag hain, aur `2.0` aur `2` bhi alag. Python me `True == 1` hota hai, isliye ye check zaroori hai.

## "Fail closed"

Koi bhi error (SyntaxError, ValueError, TypeError) aaye, to jawab = **invalid**, reward −0.1. Shak ho to **reject karo**, accept nahi.

Lab Exp 2 ke asli results:
```
import (khatarnak)   invalid   (disallowed syntax: Import)
loop (mana hai)      invalid   (disallowed syntax: For)
invalid Python       invalid   (invalid syntax)
```

## Honest limitations

Ye ek **teaching** sandbox hai, production security nahi:
- Code usi process me chalta hai, aur koi time ya memory limit nahi hai. Abhi loops, recursion aur `range` jaise calls block hain, isliye ye theek chal jaata hai, lekin ek nayi allowed call se bhi cheez badal sakti hai
- Real labs model ka code **alag container/VM** me chalate hain: no network, CPU/memory/time limits

> **Research habit:** Verifier bhi code hai, aur usme bhi bugs ho sakte hain. Use bhi test karo, bilkul jaise repo ke `tests/test_lab.py` karta hai.

---
📁 `glm53_flash/evaluator.py` (poora file, ~90 lines) · 🎬 Video 31:40–32:05, 36:15 · 📊 Slide 64 "The verifier runs hidden tests"

<!-- nav:bottom -->
---

| ⬅️ Pichla | 📚 Topic | Agla ➡️ |
|:--|:-:|--:|
| ⬅️ [02 · Definitions — RL ke shabd](02-definitions.md) | 📚 [Topic 12 overview](README.md) | [04 · Reward design, reward hacking + Real-life](04-reward-design-and-hacking.md) ➡️ |
<!-- /nav:bottom -->
