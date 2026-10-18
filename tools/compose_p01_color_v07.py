#!/usr/bin/env python3
"""Compose the P01 v07 experimental color page from three explicit raster sources.

This is an experimental compositor, not a finished-page renderer. It does not
download images, invoke generative APIs or silently substitute old assets.
All three source images are required; their dimensions are checked to prevent
accidental mixing with another page or crop.
"""
from __future__ import annotations

import argparse
import hashlib
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFont

PAGE_WIDTH, PAGE_HEIGHT = 1400, 2070
SOURCE_SIZES = {
    "rescue": (1024, 612),
    "door": (1448, 1024),
    "shoe": (427, 571),
}
PANELS = ((36, 40, 1364, 600), (36, 622, 1364, 1194), (36, 1216, 1364, 1990))


def load_checked(path: Path, name: str) -> Image.Image:
    if not path.is_file():
        raise FileNotFoundError(f"{name} source is missing: {path}")
    im = Image.open(path).convert("RGB")
    if im.size != SOURCE_SIZES[name]:
        raise ValueError(f"{name} must be {SOURCE_SIZES[name]}, got {im.size}: {path}")
    return im


def japanese_font(size: int) -> ImageFont.FreeTypeFont:
    font_path = subprocess.check_output(
        ["fc-match", "-f", "%{file}", "Noto Sans CJK JP"], text=True
    ).strip()
    if not font_path or not Path(font_path).is_file():
        raise RuntimeError("Noto Sans CJK JP font is required")
    return ImageFont.truetype(font_path, size)


def draw_bubble(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    lines: list[str],
    size: int,
    tip: tuple[int, int] | None = None,
) -> None:
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=24, fill="#fcfbf7", outline="#09151d", width=7)
    if tip:
        draw.polygon([(x0 + 55, y1 - 3), (x0 + 110, y1 - 3), tip], fill="#fcfbf7")
        draw.line([(x0 + 55, y1 - 3), tip, (x0 + 110, y1 - 3)],
                  fill="#09151d", width=5)
    font = japanese_font(size)
    line_height = size + 16
    cy = (y0 + y1 - len(lines) * line_height) // 2 + 5
    for i, line in enumerate(lines):
        bounds = draw.textbbox((0, 0), line, font=font)
        cx = (x0 + x1 - (bounds[2] - bounds[0])) // 2
        draw.text((cx, cy + i * line_height), line, font=font, fill="#0b1319")


def render(rescue: Image.Image, door: Image.Image, shoe: Image.Image) -> Image.Image:
    page = Image.new("RGB", (PAGE_WIDTH, PAGE_HEIGHT), "#f6f4ef")
    page.paste(rescue.resize((1328, 560), Image.Resampling.LANCZOS), (36, 40))

    # The second panel deliberately shows the hand without the boy's face.
    # The source artwork's original text and face are removed by cropping.
    left = door.crop((550, 702, 768, 977)).resize(
        (478, 572), Image.Resampling.LANCZOS
    )
    right = door.crop((776, 702, 1448, 978)).resize(
        (850, 572), Image.Resampling.LANCZOS
    )
    panel = Image.new("RGB", (1328, 572), "#0c1a26")
    panel.paste(left, (0, 0))
    panel.paste(right, (478, 0))
    jamb = door.crop((1188, 702, 1230, 970)).resize(
        (78, 572), Image.Resampling.LANCZOS
    )
    panel.paste(jamb, (439, 0))
    plate = door.crop((1185, 702, 1350, 970)).resize(
        (175, 338), Image.Resampling.LANCZOS
    )
    panel.paste(plate, (850, 0))
    panel_draw = ImageDraw.Draw(panel)
    panel_draw.line([(844, 0), (844, 350)], fill=(16, 23, 29), width=15)
    panel_draw.line([(1030, 0), (1030, 330)], fill=(19, 27, 33), width=10)
    panel = ImageEnhance.Contrast(panel).enhance(1.03)
    page.paste(panel, (36, 622))
    page.paste(shoe.resize((1328, 774), Image.Resampling.LANCZOS), (36, 1216))

    draw = ImageDraw.Draw(page)
    for box in PANELS:
        draw.rectangle(box, outline="#0b1019", width=9)
    draw_bubble(draw, (70, 68, 412, 152), ["2024年　豪雨"], 36)
    draw_bubble(draw, (994, 88, 1320, 295), ["扉が", "開かない！"], 49, (1040, 340))
    draw_bubble(draw, (84, 668, 390, 820), ["だれか……"], 43, (430, 850))
    draw_bubble(draw, (942, 1264, 1324, 1468),
                ["開けりゃ", "いいんだな？"], 46, (923, 1510))
    draw.text((130, 1900), "ザブッ", font=japanese_font(43),
              fill="white", stroke_width=5, stroke_fill="#111c29")
    return page


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rescue-source", required=True, type=Path)
    parser.add_argument("--door-source", required=True, type=Path)
    parser.add_argument("--shoe-source", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    page = render(
        load_checked(args.rescue_source, "rescue"),
        load_checked(args.door_source, "door"),
        load_checked(args.shoe_source, "shoe"),
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    page.save(args.output, optimize=True)
    digest = hashlib.sha256(args.output.read_bytes()).hexdigest()
    print(f"{args.output}: {page.size[0]}x{page.size[1]} sha256={digest}")


if __name__ == "__main__":
    main()
