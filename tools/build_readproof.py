#!/usr/bin/env python3
"""Validate and optionally render episode-01 manga reading proofs.

This checks file completeness and SVG XML, not drawing quality or story quality.
Rendering requires CairoSVG and Pillow, installed separately.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

REPO = Path(__file__).resolve().parents[1]
SOURCE = REPO / "docs/art/episode-01/finish/readproof"
PAGES = [SOURCE / f"p{n:02d}.svg" for n in range(1, 33)]


def validate() -> list[Path]:
    missing = [p for p in PAGES if not p.is_file()]
    if missing:
        raise ValueError("Missing pages: " + ", ".join(p.name for p in missing))

    for p in PAGES:
        data = p.read_text(encoding="utf-8")
        if re.search(r"NaN|undefined|Infinity", data):
            raise ValueError(f"{p.name}: suspicious nonnumeric value")
        try:
            root = ET.fromstring(data)
        except ET.ParseError as exc:
            raise ValueError(f"{p.name}: invalid XML: {exc}") from exc

        if not root.tag.endswith("svg"):
            raise ValueError(f"{p.name}: root element is not SVG")
        vb = root.attrib.get("viewBox", "")
        if vb and len(vb.replace(",", " ").split()) != 4:
            raise ValueError(f"{p.name}: invalid viewBox: {vb!r}")
        if not root.attrib.get("width") or not root.attrib.get("height"):
            raise ValueError(f"{p.name}: width or height is missing")

    print(f"XML / completeness checks passed: {len(PAGES)} pages.")
    print("This does NOT certify artwork or lettering.")
    return PAGES


def render(pages: list[Path], out: Path, width: int, columns: int) -> None:
    try:
        import cairosvg
        from PIL import Image, ImageDraw
    except ImportError as exc:
        raise RuntimeError(
            "Rendering requires CairoSVG and Pillow: "
            "python -m pip install cairosvg Pillow"
        ) from exc

    out.mkdir(parents=True, exist_ok=True)
    tiles = []
    for i, page in enumerate(pages, start=1):
        target = out / f"p{i:02d}.png"
        cairosvg.svg2png(url=str(page), write_to=str(target), output_width=width)
        with Image.open(target) as raw:
            tiles.append(raw.convert("RGB").copy())

    gap = 20
    label_space = 32
    max_h = max(image.height for image in tiles)
    rows = (len(tiles) + columns - 1) // columns
    sheet = Image.new(
        "RGB",
        (columns * (width + gap) + gap, rows * (max_h + label_space + gap) + gap),
        "white",
    )
    draw = ImageDraw.Draw(sheet)
    for index, tile in enumerate(tiles):
        row = index // columns
        col = columns - 1 - index % columns  # Japanese page order: right to left
        x = gap + col * (width + gap)
        y = gap + row * (max_h + label_space + gap)
        draw.text((x, y), f"P{index+1:02d}", fill="black")
        sheet.paste(tile, (x, y + label_space))

    sheet_path = out / "contact-sheet.png"
    sheet.save(sheet_path)
    print(f"Rendered {len(tiles)} PNGs and {sheet_path}")
    print("Review the actual images manually before accepting any page as final.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--render", action="store_true", help="Render PNGs and sheet")
    parser.add_argument("--out", type=Path, default=REPO / "build/readproof")
    parser.add_argument("--width", type=int, default=360)
    parser.add_argument("--columns", type=int, default=4)
    args = parser.parse_args()
    if args.width < 100 or not 1 <= args.columns <= 16:
        parser.error("--width must be >=100; --columns must be 1..16")

    try:
        pages = validate()
        if args.render:
            render(pages, args.out, args.width, args.columns)
    except (ValueError, RuntimeError) as exc:
        print(f"Validation/render failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
