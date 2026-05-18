"""Generate FCM-PM demo chips from real selected chip images.

학습 코드 D:/project/known-cnn/chip_multilabel/_train_chip_variant.py:1289-1411 의
grid_complete cutmix + corner-fill paired masking 을 그대로 재현한다.

- FCM: GRID*GRID 격자에서 절반 cell 을 B 의 같은 위치 pixel 로 덮어쓰기
- Pair Mask: A 원본의 같은 영역을 A 상단 8x8 corner mean color 로 fill
"""

from __future__ import annotations
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

FIGURES = Path(r"D:/project/fbm_paper/recommendation/figures")
SEED = 20260518
GRID = 8

CHIP_A = FIGURES / "chip_eval_bank_boundary_selected.png"
CHIP_B = FIGURES / "chip_eval_fork_selected.png"

OUT_A = FIGURES / "fcm_pm_step_a.png"
OUT_B = FIGURES / "fcm_pm_step_b.png"
OUT_MIXED = FIGURES / "fcm_pm_step_mixed.png"
OUT_MASKED = FIGURES / "fcm_pm_step_masked.png"
OUT_PANEL = FIGURES / "fcm_pm_panel.png"


def load_rgb(path: Path) -> np.ndarray:
    return np.asarray(Image.open(path).convert("RGB"), dtype=np.uint8).copy()


def save_rgb(path: Path, arr: np.ndarray) -> None:
    Image.fromarray(arr, "RGB").save(path)


def grid_complete_cutmix(a: np.ndarray, b: np.ndarray, grid: int, rng: np.random.Generator) -> tuple[np.ndarray, list[tuple[int, int, int, int]]]:
    H, W = a.shape[:2]
    n_cells = grid * grid
    half = n_cells // 2
    cell_h = H // grid
    cell_w = W // grid
    out = a.copy()
    rects: list[tuple[int, int, int, int]] = []
    chosen = rng.choice(n_cells, size=half, replace=False)
    for ci in chosen:
        gi = int(ci) // grid
        gj = int(ci) % grid
        y0 = gi * cell_h
        y1 = (gi + 1) * cell_h if gi < grid - 1 else H
        x0 = gj * cell_w
        x1 = (gj + 1) * cell_w if gj < grid - 1 else W
        out[y0:y1, x0:x1] = b[y0:y1, x0:x1]
        rects.append((y0, y1, x0, x1))
    return out, rects


def pair_mask_corner_fill(a: np.ndarray, rects: list[tuple[int, int, int, int]]) -> np.ndarray:
    corner = a[:8, :8].reshape(-1, 3).mean(axis=0).astype(np.uint8)
    out = a.copy()
    for y0, y1, x0, x1 in rects:
        out[y0:y1, x0:x1] = corner
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

    mixed, rects = grid_complete_cutmix(a, b, GRID, rng)
    masked = pair_mask_corner_fill(a, rects)

    save_rgb(OUT_A, a)
    save_rgb(OUT_B, b)
    save_rgb(OUT_MIXED, mixed)
    save_rgb(OUT_MASKED, masked)

    panels = [
        label_panel(a, "A: bank_boundary"),
        label_panel(b, "B: fork"),
        label_panel(mixed, "FCM mixed (A+B)"),
        label_panel(masked, "Pair Mask (A-only)"),
    ]
    H, W = panels[0].shape[:2]
    gap = 8
    composite = np.full((H, W * 4 + gap * 3, 3), 255, dtype=np.uint8)
    for i, p in enumerate(panels):
        x0 = i * (W + gap)
        composite[:, x0:x0 + W] = p
    save_rgb(OUT_PANEL, composite)

    print(f"chosen cells = {len(rects)} of {GRID*GRID}")
    print(f"wrote: {OUT_A.name}, {OUT_B.name}, {OUT_MIXED.name}, {OUT_MASKED.name}, {OUT_PANEL.name}")


if __name__ == "__main__":
    main()
