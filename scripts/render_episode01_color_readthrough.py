#!/usr/bin/env python3
"""Make a four-page P05–P08 color contact sheet for visual continuity review.

Reads originals and verified revised candidates already tracked on GitHub.
Does not change, upscale, or replace any individual manga page.
"""
from __future__ import annotations

from hashlib import sha256
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs/art/episode-01/finish/color-candidates"
OUTPUT = BASE / "review_p05_p08.jpg"
PAGES = [
    ("P05", "p05.png"),
    ("P06 v03", "p06_v03.png"),
    ("P07 v04", "p07_v04.png"),
    ("P08 v04", "p08_v04.png"),
]

def main() -> None:
    width, height = 384, 576
    margin, gap, caption_height = 22, 22, 42
    sheet = Image.new("RGB", (2 * width + 2 * margin + gap, 2 * (height + caption_height) + 2 * margin + gap), "#e9e6de")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 23)
    for i, (label, filename) in enumerate(PAGES):
        src = BASE / filename
        with Image.open(src) as raw:
            assert raw.size == (1024, 1536), (filename, raw.size)
            image = raw.convert("RGB").resize((width, height), Image.Resampling.LANCZOS)
        x = margin + (i % 2) * (width + gap)
        y = margin + (i // 2) * (height + caption_height + gap)
        draw.text((x, y + 5), label, font=font, fill="#28323a")
        sheet.paste(image, (x, y + caption_height))
    sheet.save(OUTPUT, quality=91, subsampling=0, optimize=True)
    data = OUTPUT.read_bytes()
    assert data[:3] == b"\xff\xd8\xff"
    print(f"Readthrough: {OUTPUT.relative_to(ROOT)} size={len(data)} sha256={sha256(data).hexdigest()}")


if __name__ == "__main__":
    main()
