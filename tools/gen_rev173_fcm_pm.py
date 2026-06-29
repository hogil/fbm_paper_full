from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "figures" / "full_paper_rev172" / "fig06_fcm_pm.png"
OUT = ROOT / "figures" / "full_paper_rev173" / "fig06_fcm_pm.png"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
        Path("C:/Windows/Fonts/calibrib.ttf" if bold else "C:/Windows/Fonts/calibri.ttf"),
    ]
    for path in candidates:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


F_TITLE = font(36, True)
F_HEAD = font(27, True)
F_BODY = font(21)
F_SMALL = font(18)
F_BOLD = font(22, True)


def crop_chip(src: Image.Image, box: tuple[int, int, int, int], size: int = 135) -> Image.Image:
    chip = src.crop(box).convert("RGB")
    chip = chip.resize((size, size), Image.Resampling.LANCZOS)
    return chip


def card(draw: ImageDraw.ImageDraw, xy: tuple[int, int, int, int], title: str, lines: list[str]) -> None:
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle(xy, radius=12, fill=(250, 250, 250), outline=(120, 120, 120), width=2)
    draw.text((x1 + 14, y1 + 12), title, font=F_HEAD, fill=(30, 30, 30))
    y = y1 + 48
    for line in lines:
        draw.text((x1 + 14, y), line, font=F_BODY, fill=(65, 65, 65))
        y += 25


def arrow(draw: ImageDraw.ImageDraw, p1: tuple[int, int], p2: tuple[int, int], width: int = 4) -> None:
    draw.line([p1, p2], fill=(55, 55, 55), width=width)
    x1, y1 = p1
    x2, y2 = p2
    if abs(x2 - x1) >= abs(y2 - y1):
        direction = 1 if x2 > x1 else -1
        pts = [(x2, y2), (x2 - direction * 18, y2 - 10), (x2 - direction * 18, y2 + 10)]
    else:
        direction = 1 if y2 > y1 else -1
        pts = [(x2, y2), (x2 - 10, y2 - direction * 18), (x2 + 10, y2 - direction * 18)]
    draw.polygon(pts, fill=(55, 55, 55))


def main() -> None:
    src = Image.open(SRC).convert("RGB")
    chips = {
        "a": crop_chip(src, (55, 145, 200, 290)),
        "b": crop_chip(src, (298, 145, 398, 285)),
        "m": crop_chip(src, (730, 145, 865, 290)),
        "ao": crop_chip(src, (95, 720, 242, 838)),
        "bo": crop_chip(src, (675, 720, 785, 815)),
    }

    img = Image.new("RGB", (900, 1040), "white")
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, 900, 70), fill=(238, 238, 238))
    d.text((28, 17), "FCM-PM augmentation", font=F_TITLE, fill=(25, 25, 25))

    card(d, (30, 95, 205, 345), "Single A", ["source chip", "Label = A"])
    img.paste(chips["a"], (50, 200))
    card(d, (245, 95, 420, 345), "Single B", ["source chip", "Label = B"])
    img.paste(chips["b"], (265, 200))
    d.text((216, 207), "+", font=font(44, True), fill=(30, 30, 30))

    card(d, (470, 138, 640, 270), "Full-Cover", ["whole chip", "Label = A+B"])
    arrow(d, (420, 220), (470, 220))
    card(d, (700, 95, 875, 345), "Mixed", ["joint view", "Label = A+B"])
    img.paste(chips["m"], (720, 200))
    arrow(d, (640, 220), (700, 220))

    d.line((45, 415, 855, 415), fill=(190, 190, 190), width=2)
    card(d, (305, 465, 595, 575), "Pair Mask", ["source-specific masked views", "separate masked labels"])
    arrow(d, (785, 345), (545, 465))

    card(d, (70, 670, 300, 900), "A-only view", ["Label = A"])
    img.paste(chips["ao"], (118, 745))
    card(d, (600, 670, 830, 900), "B-only view", ["Label = B"])
    img.paste(chips["bo"], (648, 745))
    arrow(d, (330, 575), (245, 670))
    arrow(d, (570, 575), (655, 670))

    d.rounded_rectangle((55, 942, 845, 1005), radius=12, fill=(248, 248, 248), outline=(130, 130, 130), width=2)
    d.text((82, 955), "Suppress synthetic-background false positives", font=F_BOLD, fill=(25, 25, 25))
    d.text((82, 982), "Train mixed A+B and A-only/B-only views with source-specific labels", font=F_SMALL, fill=(70, 70, 70))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, quality=95)


if __name__ == "__main__":
    main()
