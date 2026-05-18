"""Generate FCM-PM demo chips from real selected chip images (group2: A + B).

학습 코드 D:/project/known-cnn/chip_multilabel/_train_chip_variant.py:1289-1427 의
grid_complete cutmix + do_pair2 (A-side + B-side paired masked forward) 를 재현한다.

같은 chosen cells 위에서 group2 의 4 가지 산출물을 만든다:
- mixed_A : A base + B 의 chosen cells 덮어쓰기  (label = A ∪ B)
- mixed_B : B base + A 의 chosen cells 덮어쓰기  (label = A ∪ B)
- masked_A: A 에서 chosen cells 만 검정 fill     (label = A only)
- masked_B: B 에서 chosen cells 만 검정 fill     (label = B only)

총 6 개 출력 (A, B, mixed_A, mixed_B, masked_A, masked_B) + 2x3 composite panel.
"""

from __future__ import annotations
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

FIGURES = Path(r"D:/project/fbm_paper/recommendation/figures")
SEED = 20260518
GRID = 8

CHIP_A = FIGURES / "chip_eval_scratch_selected.png"
CHIP_B = FIGURES / "chip_eval_scratch_rot_selected.png"

OUT_A = FIGURES / "fcm_pm_step_a.png"
OUT_B = FIGURES / "fcm_pm_step_b.png"
OUT_MIXED_A = FIGURES / "fcm_pm_step_mixed_a.png"
OUT_MIXED_B = FIGURES / "fcm_pm_step_mixed_b.png"
OUT_MASKED_A = FIGURES / "fcm_pm_step_masked_a.png"
OUT_MASKED_B = FIGURES / "fcm_pm_step_masked_b.png"
OUT_PANEL = FIGURES / "fcm_pm_panel.png"


def load_rgb(path: Path) -> np.ndarray:
    return np.asarray(Image.open(path).convert("RGB"), dtype=np.uint8).copy()


def save_rgb(path: Path, arr: np.ndarray) -> None:
    Image.fromarray(arr, "RGB").save(path)


def grid_complete_pair(a: np.ndarray, b: np.ndarray, grid: int, rng: np.random.Generator):
    """Run grid_complete cutmix and return both complementary mixed outputs + chosen rects."""
    H, W = a.shape[:2]
    n_cells = grid * grid
    half = n_cells // 2
    cell_h = H // grid
    cell_w = W // grid
    mixed_a = a.copy()
    mixed_b = b.copy()
    rects: list[tuple[int, int, int, int]] = []
    chosen = rng.choice(n_cells, size=half, replace=False)
    for ci in chosen:
        gi = int(ci) // grid
        gj = int(ci) % grid
        y0 = gi * cell_h
        y1 = (gi + 1) * cell_h if gi < grid - 1 else H
        x0 = gj * cell_w
        x1 = (gj + 1) * cell_w if gj < grid - 1 else W
        mixed_a[y0:y1, x0:x1] = b[y0:y1, x0:x1]
        mixed_b[y0:y1, x0:x1] = a[y0:y1, x0:x1]
        rects.append((y0, y1, x0, x1))
    return mixed_a, mixed_b, rects


def pair_mask_black_fill(base: np.ndarray, rects: list[tuple[int, int, int, int]]) -> np.ndarray:
    out = base.copy()
    for y0, y1, x0, x1 in rects:
        out[y0:y1, x0:x1] = 0
    return out


def label_panel(img: np.ndarray, text: str) -> np.ndarray:
    H, W = img.shape[:2]
    pad = 30
    canvas = np.full((H + pad, W, 3), 255, dtype=np.uint8)
    canvas[pad:, :, :] = img
    pil = Image.fromarray(canvas, "RGB")
    draw = ImageDraw.Draw(pil)
    try:
        font = ImageFont.truetype("arial.ttf", 14)
    except OSError:
        font = ImageFont.load_default()
    draw.text((6, 6), text, fill=(0, 0, 0), font=font)
    return np.asarray(pil, dtype=np.uint8)


def main() -> None:
    rng = np.random.default_rng(SEED)
    a = load_rgb(CHIP_A)
    b = load_rgb(CHIP_B)
    assert a.shape == b.shape, f"shape mismatch: {a.shape} vs {b.shape}"

    mixed_a, mixed_b, rects = grid_complete_pair(a, b, GRID, rng)
    masked_a = pair_mask_black_fill(a, rects)
    masked_b = pair_mask_black_fill(b, rects)

    save_rgb(OUT_A, a)
    save_rgb(OUT_B, b)
    save_rgb(OUT_MIXED_A, mixed_a)
    save_rgb(OUT_MIXED_B, mixed_b)
    save_rgb(OUT_MASKED_A, masked_a)
    save_rgb(OUT_MASKED_B, masked_b)

    row1 = [
        label_panel(a, "A: scratch"),
        label_panel(mixed_a, "FCM mixed (A base)"),
        label_panel(masked_a, "Pair Mask (A-only)"),
    ]
    row2 = [
        label_panel(b, "B: scratch_rot"),
        label_panel(mixed_b, "FCM mixed (B base)"),
        label_panel(masked_b, "Pair Mask (B-only)"),
    ]
    H, W = row1[0].shape[:2]
    gap = 8
    panel_w = W * 3 + gap * 2
    panel_h = H * 2 + gap
    composite = np.full((panel_h, panel_w, 3), 255, dtype=np.uint8)
    for i, p in enumerate(row1):
        x0 = i * (W + gap)
        composite[:H, x0:x0 + W] = p
    for i, p in enumerate(row2):
        x0 = i * (W + gap)
        composite[H + gap:H * 2 + gap, x0:x0 + W] = p
    save_rgb(OUT_PANEL, composite)

    print(f"chosen cells = {len(rects)} of {GRID*GRID}")
    print(f"wrote: a, b, mixed_a, mixed_b, masked_a, masked_b, panel ({OUT_PANEL.name})")


if __name__ == "__main__":
    main()
