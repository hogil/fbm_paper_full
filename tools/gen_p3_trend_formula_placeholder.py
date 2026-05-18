"""Wide placeholder image for the P3 trend-generation formula slot.

사내 자료로 교체 예정. recommendation/figures/p3_trend_generation_formula.png 로 저장.
세 칸 (Region 계측 밀도 / Noise 분포 / Anomaly 수식) 을 가로로 길게 그려둔다.
"""

from __future__ import annotations
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

OUT = Path(r"D:/project/fbm_paper/recommendation/figures/p3_trend_generation_formula.png")
W, H = 1280, 360
PAD = 24


def load_font(size: int):
    for name in ("arial.ttf", "ARIAL.TTF", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def main() -> None:
    img = Image.new("RGB", (W, H), (252, 252, 252))
    draw = ImageDraw.Draw(img)
    title_font = load_font(20)
    sub_font = load_font(15)
    body_font = load_font(13)

    draw.text((PAD, 14), "Trend 합성 원리 (Region x Noise x Anomaly)", font=title_font, fill=(20, 20, 20))
    draw.line([(PAD, 48), (W - PAD, 48)], fill=(180, 180, 180), width=1)

    cell_w = (W - PAD * 4) // 3
    top = 64
    cell_h = H - top - PAD
    headers = [
        ("[1] Region 계측 밀도",
         [
             "dense / sparse / very_sparse / thin / missing",
             "x_obs = x_true at sampled indices",
             "N_obs = N_total * density_ratio(Region)",
         ]),
        ("[2] Noise 분포 모델",
         [
             "Gaussian:    e_t ~ N(0, sigma^2)",
             "Laplacian:   e_t ~ Laplace(0, b)",
             "Correlated:  e_t = rho * e_{t-1} + w_t",
         ]),
        ("[3] Anomaly 수식 (5종)",
         [
             "mean_shift:  y_t = mu + delta",
             "std_change:  y_t = mu + sigma' * z_t",
             "spike:       y_t += A * 1[t = t*]",
             "drift:       y_t += k * (t - t0)",
             "context:     legend-relative outlier",
         ]),
    ]
    for i, (htxt, lines) in enumerate(headers):
        x0 = PAD + i * (cell_w + PAD)
        x1 = x0 + cell_w
        y0 = top
        y1 = top + cell_h
        draw.rectangle([x0, y0, x1, y1], outline=(160, 160, 160), width=1, fill=(255, 255, 255))
        draw.text((x0 + 12, y0 + 10), htxt, font=sub_font, fill=(30, 30, 30))
        cur_y = y0 + 44
        for line in lines:
            draw.text((x0 + 12, cur_y), line, font=body_font, fill=(60, 60, 60))
            cur_y += 22

    footer = "사내 trend 생성 수식 / 도면이 들어갈 자리"
    draw.text((PAD, H - PAD), footer, font=body_font, fill=(140, 140, 140))

    img.save(OUT)
    print(f"wrote: {OUT}")


if __name__ == "__main__":
    main()
