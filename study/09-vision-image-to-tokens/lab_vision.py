"""Lab 9 — Vision: 32x32 image se 16 tokens, aur ek chhota digit-reader train karo.

Run:  uv run study/09-vision-image-to-tokens/lab_vision.py [seed]     (~10 sec, CPU; default seed 42)

Ye lab repo ka asli vision code import karta hai (sources/repo), copy nahi.
"""

import argparse
import sys
from pathlib import Path

import torch

REPO = Path(__file__).resolve().parents[2] / "sources" / "repo"
sys.path[:0] = [str(REPO), str(REPO / "scripts")]

from glm53_flash import ByteTokenizer, ModelConfig  # noqa: E402
from glm53_flash.vision import MiniVisionConfig, VisionLanguageModel  # noqa: E402
from glm53_flash.model import GLM53FlashFromScratch  # noqa: E402
from train_vision import generated_rgb_digit_images, train_one  # noqa: E402

torch.manual_seed(0)
tok = ByteTokenizer()

# --- Experiment 1: ek generated digit image ko terminal me dekho -------------
image = generated_rgb_digit_images(torch.tensor([3]), seed=7)[0]  # [3, 32, 32] RGB
brightness = image.mean(dim=0)  # [32, 32]
print("Exp 1  digit '3' (32x32 RGB, har 2 pixel = 1 character):")
for row in range(0, 32, 2):
    print("       " + "".join("#" if brightness[row, col] > 0.4 else "." for col in range(0, 32, 2)))

# --- Experiment 2: shapes ki journey — image se 16 tokens --------------------
# Repo ke train_vision.py wala exact config.
lm_config = ModelConfig(vocab_size=263, dim=32, layers=1, heads=4, expert_hidden=48, experts=4,
                        top_k=2, streams=2, sparse_window=8, sparse_stride=8, max_sequence_length=64)
v_config = MiniVisionConfig(image_size=32, patch_size=4, hidden_size=24, depth=2, heads=4,
                            intermediate_size=48, spatial_merge_size=2, projection_intermediate_size=64)
model = VisionLanguageModel(GLM53FlashFromScratch(lm_config), v_config)
enc = model.vision_encoder
x = image[None]
with torch.no_grad():
    patches, grid = enc.patch_embedding(x)
    hidden = patches
    for block in enc.blocks:
        hidden = block(hidden)
    merged = enc.spatial_merger(enc.post_layernorm(hidden), grid)
    tokens = enc.projector(merged)
print("Exp 2  image               ", tuple(x.shape), "  [batch, RGB, H, W]")
print("       patch embedding      ", tuple(patches.shape), f"  {grid[0]}x{grid[1]} patches (har patch 4x4 px)")
print("       2 vision blocks      ", tuple(hidden.shape), "  patches aapas me baat karte hain")
print("       2x2 spatial merge    ", tuple(merged.shape), "  64 -> 16, width 24 -> 32 (LM ki dim)")
print("       projector            ", tuple(tokens.shape), "  = 16 'visual tokens'")

# --- Experiment 3: language model ko kya sequence milta hai? ----------------
text_ids = torch.tensor([tok.encode("Digit: ", bos=True)])
ids = model.prepare_input_ids(text_ids)[0].tolist()
names = {1: "<BOS>", 260: "<img_start>", 261: "<image>", 262: "<img_end>"}
pretty = [names[t] if t in names else tok.decode([t]) for t in ids]
n_img = pretty.count("<image>")
first = pretty.index("<image>")
compact = pretty[:first] + [f"<image> x{n_img}"] + [repr("".join(pretty[first + n_img + 1:]))]
compact.insert(first + 1, "<img_end>")
print("Exp 3  sequence:", " ".join(compact))
print(f"       kul {len(ids)} positions; 16 <image> placeholders ki jagah visual vectors daale jaate hain")

# --- Experiment 4: faithful vision path vs simple baseline — train karo ------
SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 42
args = argparse.Namespace(seed=SEED, steps=120, batch_size=40, eval_examples=200, learning_rate=2e-3)
torch.use_deterministic_algorithms(True)
print(f"Exp 4  seed={SEED}, 120 steps training (repo ka VISION_REPORT wala setup), held-out 200 images:")
for arch in ("faithful", "direct_patch_baseline"):
    r = train_one(arch, args=args, language_config=lm_config, vision_config=v_config,
                  tokenizer=tok, device=torch.device("cpu"))
    print(f"       {arch:22} params={r['parameter_count']:>6,}  "
          f"accuracy {r['before']['correct']:>3}/200 -> {r['after']['correct']:>3}/200  "
          f"({r['wall_time_seconds']:.1f}s)")

# TODO (tumhara kaam):
#  a) Exp 1 me seed badlo (7 -> 8, 9). Digit ka rang, position, noise kaise badalte hain? Ye "held-out" kyun banata hai?
#  b) Doosre seeds chalao: `uv run .../lab_vision.py 7` aur `... 123`. Kya faithful hamesha baseline se haarta hai? (1 seed = 1 anecdote!)
#  c) v_config me patch_size=8 karo (merge 2x2 -> 4 tokens). Exp 2 ke shapes kya hue?
