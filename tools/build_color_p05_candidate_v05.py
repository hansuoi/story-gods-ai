#!/usr/bin/env python3
"""Compose P05 funeral illustration with a separate Japanese title layer.

The source illustration must be provided explicitly. No previous P05 raster,
P01 art or substitute procedural image is used. This script does not fetch
external assets or call paid APIs.
"""
from __future__ import annotations

import argparse
import hashlib
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1536


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def font(family: str, size: int) -> ImageFont.FreeTypeFont:
    filename = subprocess.check_output(
        ["fc-match", "-f", "%{file}", family], text=True
    ).strip()
    if not filename or not Path(filename).is_file():
        raise RuntimeError("Install fonts-noto-cjk for Japanese typography")
    return ImageFont.truetype(filename, size)


def render_title_overlay() -> Image.Image:
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    tint = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pixels = tint.load()
    # Only the empty upper-right wall is darkened; face and coffin remain visible.
    for y in range(465):
        yf = max(0, 1 - y / 465) ** 0.55
        for x in range(430, W):
            xf = min(1, max(0, (x - 430) / 190))
            pixels[x, y] = (12, 17, 23, int(180 * yf * xf))
    overlay = Image.alpha_composite(overlay, tint)
    draw = ImageDraw.Draw(overlay)
    x = 554
    ivory = (246, 246, 240, 255)
    muted = (216, 224, 225, 240)
    draw.text((x, 70), "2026年10月",
              font=font("Noto Sans CJK JP", 28), fill=muted)
    draw.line([(x, 119), (961, 119)], fill=(210, 218, 219, 135), width=2)
    draw.text((x - 6, 144), "神谷家",
              font=font("Noto Serif CJK JP", 96), fill=ivory,
              stroke_width=1, stroke_fill=(22, 24, 28, 190))
    draw.text((x + 7, 266), "- 原状回復 -",
              font=font("Noto Serif CJK JP", 40), fill=ivory)
    draw.text((x + 7, 354), "第1話  帰ってきた人",
              font=font("Noto Sans CJK JP", 30), fill=muted)
    return overlay


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True,
                        help="P05 source illustration (not included in repo)")
    parser.add_argument("--out-dir", type=Path,
                        default=Path("build/episode01-color/p05-v05"))
    args = parser.parse_args()
    if not args.source.is_file():
        parser.error(f"Source illustration is missing: {args.source}")
    args.out_dir.mkdir(parents=True, exist_ok=True)
    source = Image.open(args.source).convert("RGB")
    if source.size != (W, H):
        source = source.resize((W, H), Image.Resampling.LANCZOS)
    overlay = render_title_overlay()
    composite = Image.alpha_composite(
        source.convert("RGBA"), overlay
    ).convert("RGB")
    files = {
        "p05-funeral-art-v05.webp": (source, {"format": "WEBP", "quality": 92, "method": 6}),
        "p05-title-overlay-v05.png": (overlay, {"optimize": True}),
        "p05-color-candidate-v05.png": (composite, {"optimize": True}),
    }
    for name, (im, options) in files.items():
        dest = args.out_dir / name
        im.save(dest, **options)
        print(name, im.size, sha256(dest))
    preview = args.out_dir / "p05-color-candidate-v05-preview.webp"
    composite.resize((512, 768), Image.Resampling.LANCZOS).save(
        preview, quality=72, method=6
    )
    print(preview.name, (512, 768), sha256(preview))


if __name__ == "__main__":
    main()
