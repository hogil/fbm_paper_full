from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "figures" / "full_paper_rev174" / "fig02_pipeline_architecture.png"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
        Path("C:/Windows/Fonts/calibrib.ttf" if bold else "C:/Windows/Fonts/calibri.ttf"),
    ]
    for path in candidates:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


F_TITLE = font(34, True)
F_HEAD = font(27, True)
F_BODY = font(22)
F_SMALL = font(19)


def box(draw: ImageDraw.ImageDraw, xy: tuple[int, int, int, int], title: str, lines: list[str], fill=(250, 250, 250)) -> None:
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle(xy, radius=12, fill=fill, outline=(55, 65, 75), width=3)
    draw.text((x1 + 20, y1 + 16), title, font=F_HEAD, fill=(25, 30, 38))
    y = y1 + 55
    for line in lines:
        draw.text((x1 + 20, y), line, font=F_BODY, fill=(55, 60, 68))
        y += 28


def arrow(draw: ImageDraw.ImageDraw, p1: tuple[int, int], p2: tuple[int, int], width: int = 4) -> None:
    draw.line([p1, p2], fill=(55, 65, 75), width=width)
    x1, y1 = p1
    x2, y2 = p2
    if abs(x2 - x1) >= abs(y2 - y1):
        direction = 1 if x2 > x1 else -1
        pts = [(x2, y2), (x2 - direction * 18, y2 - 10), (x2 - direction * 18, y2 + 10)]
    else:
        direction = 1 if y2 > y1 else -1
        pts = [(x2, y2), (x2 - 10, y2 - direction * 18), (x2 + 10, y2 - direction * 18)]
    draw.polygon(pts, fill=(55, 65, 75))


def main() -> None:
    img = Image.new("RGB", (900, 1220), "white")
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, 900, 76), fill=(238, 238, 238))
    d.text((32, 20), "Coordinate-preserving analysis pipeline", font=F_TITLE, fill=(25, 30, 38))

    box(d, (70, 105, 830, 215), "EDS data", ["raw fail-map + chip-level measures"])
    box(d, (70, 270, 830, 410), "Coordinate-preserving wafer unit", ["FBM image + chip coordinates + measures", "shared coordinate index for model and review"], fill=(247, 247, 247))
    arrow(d, (450, 215), (450, 270))

    box(d, (70, 505, 410, 675), "Known path", ["ConvNeXtV2", "selective ROI-YOLO", "object-id map [development]"])
    box(d, (490, 505, 830, 675), "Unknown path", ["InfoNCE embedding", "HDBSCAN", "candidate groups"])
    arrow(d, (410, 410), (245, 505))
    arrow(d, (490, 410), (655, 505))

    box(d, (120, 815, 780, 960), "Web review + label feedback", ["search / overlay / measure review", "label registration / retraining queue"], fill=(247, 247, 247))
    arrow(d, (245, 675), (300, 815))
    arrow(d, (655, 675), (600, 815))

    # Feedback path back to the shared wafer unit.
    d.line((120, 890, 45, 890, 45, 340, 70, 340), fill=(55, 65, 75), width=4)
    d.polygon([(70, 340), (52, 330), (52, 350)], fill=(55, 65, 75))
    d.text((58, 736), "feedback / retraining", font=F_SMALL, fill=(75, 80, 90))

    d.rounded_rectangle((95, 1025, 805, 1160), radius=12, fill=(252, 252, 252), outline=(125, 125, 125), width=2)
    d.text((125, 1045), "One coordinate system", font=F_HEAD, fill=(25, 30, 38))
    d.text((125, 1082), "Known recognition, Unknown compression,", font=F_BODY, fill=(55, 60, 68))
    d.text((125, 1110), "chip evidence, and web review use the same wafer unit.", font=F_BODY, fill=(55, 60, 68))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, quality=95)


if __name__ == "__main__":
    main()
