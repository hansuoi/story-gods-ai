#!/usr/bin/env python3
"""Make inspectable P25-P32 contact sheets using the actual saved color pages.

Image QA aid only. Renders P25–P28, P29–P32 and a combined 8-page overview;
adds base64 text copies for connector-based visual inspection. It does not alter
the manga page PNGs or claim they are finished artwork.
"""
from __future__ import annotations
import base64
from hashlib import sha256
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).resolve().parents[1] / "docs/art/episode-01/finish/color-candidates"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_JP = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"

def sheet(start: int, end: int, filename: str) -> None:
    nums = list(range(start, end + 1))
    cols = 2 if len(nums) <= 4 else 4
    rows = (len(nums) + cols - 1) // cols
    width, height, gap, header = 354, 531, 24, 43
    canvas = Image.new("RGB", (cols * width + (cols + 1) * gap,
                                rows * (height + header) + (rows + 1) * gap), "#eeeae2")
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.truetype(FONT, 27)
    manifest = json.loads((BASE / "revision-manifest.json").read_text(encoding="utf-8"))
    for i, n in enumerate(nums):
        name = f"p{n:02d}_v01.png"
        path = BASE / name
        assert path.exists() and name in manifest, name
        data = path.read_bytes()
        assert sha256(data).hexdigest() == manifest[name]["sha256"], name
        with Image.open(path) as raw:
            assert raw.size == (1024, 1536), (name, raw.size)
            image = raw.convert("RGB").resize((width, height), Image.Resampling.LANCZOS)
        col, row = i % cols, i // cols
        x = gap + col * (width + gap)
        y = gap + row * (height + header + gap)
        draw.text((x, y + 3), f"P{n:02d} color candidate", font=font, fill="#25313b")
        canvas.paste(image, (x, y + header))
    destination = BASE / filename
    canvas.save(destination, "JPEG", quality=88, subsampling=0, optimize=True)
    binary = destination.read_bytes()
    assert Image.open(destination).size == canvas.size
    (BASE / (filename + ".base64")).write_text(base64.b64encode(binary).decode("ascii") + "\n", encoding="ascii")
    print(f"{filename}: {len(binary)} bytes, sha256={sha256(binary).hexdigest()}; {start}-{end}")

def main() -> None:
    sheet(25, 28, "review_p25_p28.jpg")
    sheet(29, 32, "review_p29_p32.jpg")
    sheet(25, 32, "review_p25_p32.jpg")

if __name__ == "__main__":
    main()
