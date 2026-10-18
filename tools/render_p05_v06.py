#!/usr/bin/env python3
"""Render P05 v06 full-page original art and separate Japanese title overlay.

The input SVG is an illustration candidate, not the finished manuscript. The
raster output is deterministic within one CairoSVG/Pango font environment.
"""
from __future__ import annotations
import argparse
import hashlib
import re
from pathlib import Path
import cairosvg
from PIL import Image

SVG_END = "</svg>"
TITLE_MARKER = "<!-- separate typography layer to be split in raster build -->"

def split_layers(svg: str) -> tuple[str, str]:
    if svg.count(TITLE_MARKER) != 1:
        raise ValueError("Title layer marker must occur exactly once")
    art, suffix = svg.split(TITLE_MARKER, 1)
    if not suffix.strip().endswith(SVG_END):
        raise ValueError("Unexpected SVG suffix")
    title = suffix[:suffix.rfind(SVG_END)]
    if title.count("<g ") != 1 or title.count("</g>") != 1:
        raise ValueError("Title layer should contain exactly one group")
    prefix = svg[:svg.find("<defs>")]
    # All gradients are contained in <defs>, and typography does not need them.
    overlay = prefix + title + SVG_END
    return art + SVG_END, overlay

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    art_svg, overlay_svg = split_layers(args.source.read_text(encoding="utf-8"))
    paths = {
        "art": args.out_dir / "p05-art-v06.png",
        "overlay": args.out_dir / "p05-title-overlay-v06.png",
        "composite": args.out_dir / "p05-color-candidate-v06.png",
    }
    cairosvg.svg2png(bytestring=art_svg.encode("utf-8"), write_to=str(paths["art"]))
    cairosvg.svg2png(bytestring=overlay_svg.encode("utf-8"), write_to=str(paths["overlay"]))
    art = Image.open(paths["art"]).convert("RGBA")
    overlay = Image.open(paths["overlay"]).convert("RGBA")
    if art.size != (1400, 2100) or overlay.size != art.size:
        raise RuntimeError("Unexpected raster dimensions")
    Image.alpha_composite(art, overlay).convert("RGB").save(paths["composite"], optimize=True)
    for name, path in paths.items():
        print(name, path, path.stat().st_size, sha(path))

if __name__ == "__main__":
    main()
