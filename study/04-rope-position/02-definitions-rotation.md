# 02 · Definitions — Rotation, pairs, frequency

## 2D rotation (school wala)

Ek point `(a, b)` ko angle `θ` se ghumao:
```
a' = a·cos θ − b·sin θ
b' = a·sin θ + b·cos θ
```

Lab Exp 1: `[1, 0]` ko position ke hisaab se ghumaya (θ = 1 radian per position):

| Position | Angle | Result | Length |
|---|---|---|---|
| 0 | 0 | `[1.000, 0.000]` | 1 |
| 1 | 1 rad (~57°) | `[0.540, 0.841]` | 1 |
| 2 | 2 rad | `[-0.416, 0.909]` | 1 |
| 3 | 3 rad | `[-0.990, 0.141]` | 1 |

Length hamesha **1** rehti hai ✅

## 32 dimensions ka kya karein? → **Pairs**

Har attention head ka vector 32 numbers ka hai (192 / 6 heads). RoPE ise **16 pairs** me todta hai aur har pair ko apne 2D plane me ghumata hai:

```
[x0, x1 | x2, x3 | x4, x5 | ... | x30, x31]
  pair 0   pair 1   pair 2        pair 15
```

Video: *"If you have some vector, you take pairs of dimensions and rotate each pair."*

## Har pair ki alag speed: **frequency**

```
frequency_i = 1 / 10000^(2i / 32)        i = 0, 1, ..., 15
angle       = position × frequency_i
```

| Term | Matlab | Repo me |
|---|---|---|
| **Base** | Formula ka 10000. Ye tay karta hai ki sabse dheema pair kitna dheema hoga | `10000` |
| **Frequency** | Ek position aage badhne pe pair kitne radian ghoomta hai | pair 0: 1.0, pair 15: 0.000178 |
| **Angle** | Position × frequency | |

Lab Exp 4:
- **Pair 0:** har token pe 1 radian ghoomta hai (tez, "second ki sui")
- **Pair 15:** har token pe 0.000178 radian (bahut dheema, "ghante ki sui"). Ek poora chakkar ~35,000 tokens me.

## Kyun alag speeds?

- **Tez pairs** paas-paas ke tokens me fark batate hain: "ye mere bilkul bagal me hai"
- **Dheeme pairs** door ki position batate hain: "ye ~1000 tokens peeche hai"
- Ek tez pair akela confuse ho jaata hai (6.28 radian baad wapas same jagah aa jaata hai), lekin sab pairs milke ek unique "fingerprint" banate hain

## Repo ka code

```python
frequencies = 1.0 / (10000 ** (torch.arange(0, width, 2).float() / width))
angles = positions[:, None] * frequencies[None, :]       # [T, 16]
cos, sin = angles.cos(), angles.sin()

def rotate(x):
    even, odd = x[..., 0::2], x[..., 1::2]              # pair ka pehla, doosra number
    return torch.stack((even * cos - odd * sin,          # a' = a cos − b sin
                        even * sin + odd * cos),         # b' = a sin + b cos
                       dim=-1).flatten(-2)
```

Upar wala 2D formula hi hai, bas 16 pairs pe ek saath lagaya gaya hai.

---
📁 `model.py` lines 44–59 · 🎬 Video 15:25–15:55
