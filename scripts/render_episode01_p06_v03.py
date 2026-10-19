#!/usr/bin/env python3
"""Recompose episode-01 P06 from existing high-quality GitHub PNG originals.

The input images are original PNGs already tracked in the repository. This script
does not depend on imagegen uploads, temporary Library files or external URLs.
The result is a REVIEW CANDIDATE, not a final/accepted manuscript.
"""
from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs/art/episode-01/finish/color-candidates"
SOURCE_P06 = BASE / "p06.png"
SOURCE_P07 = BASE / "p07.png"
OUTPUT = BASE / "p06_v03.png"
MANIFEST = BASE / "revision-manifest.json"
FONT_PATH = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"

PAGE_SIZE = (1024, 1536)
FRAMES = (
    (28, 28, 996, 467),
    (28, 479, 996, 753),
    (28, 765, 996, 1291),
    (28, 1303, 996, 1508),
)


def bubble(draw: ImageDraw.ImageDraw, box, lines, font, tail=None):
    ink = (23, 29, 34)
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=40, fill=(255, 254, 251), outline=ink, width=5)
    if tail is not None:
        xx, yy = tail
        anchor = x1 - 80
        draw.polygon(
            [(anchor - 15, y1 - 3), (anchor + 22, y1 - 3), (xx, yy)],
            fill=(255, 254, 251),
        )
        draw.line(
            [(anchor - 15, y1 - 4), (xx, yy), (anchor + 22, y1 - 4)],
            fill=ink,
            width=4,
            joint="curve",
        )
    for k, line in enumerate(lines):
        box_text = draw.textbbox((0, 0), line, font=font)
        text_width = box_text[2] - box_text[0]
        line_height = 53 if len(lines) > 1 else 44
        total = (len(lines) - 1) * line_height + max(font.size + 2, 43)
        x = x0 + ((x1 - x0) - text_width) // 2
        y = y0 + ((y1 - y0) - total) // 2 + k * line_height
        draw.text((x, y), line, font=font, fill=ink)


def main() -> None:
    p06 = Image.open(SOURCE_P06).convert("RGB")
    p07 = Image.open(SOURCE_P07).convert("RGB")
    assert p06.size == PAGE_SIZE, ("p06", p06.size)
    assert p07.size == PAGE_SIZE, ("p07", p07.size)

    page = Image.new("RGB", PAGE_SIZE, (251, 249, 245))
    draw = ImageDraw.Draw(page)
    panels = (
        # Silent intact face in coffin; reframe a clean crop without AI-written text.
        (p07, (40, 112, 984, 551)),
        # Aki's hand hesitates; still does not touch him.
        (p06, (88, 414, 720, 592)),
        # Attendant explains repair; Aki asks cause of death.
        (p06, (5, 680, 719, 1070)),
        # Coffin edge and the hand, with answer from offscreen.
        (p06, (102, 237, 716, 343)),
    )
    for frame, (source, crop) in zip(FRAMES, panels):
        x0, y0, x1, y1 = frame
        panel = source.crop(crop).resize((x1 - x0, y1 - y0), Image.Resampling.LANCZOS)
        page.paste(panel, (x0, y0))
        draw.rectangle(frame, outline=(23, 29, 34), width=5)

    font36 = ImageFont.truetype(FONT_PATH, 36, index=0)
    font34 = ImageFont.truetype(FONT_PATH, 34, index=0)
    # Only the three speech items present in the P06 text name.
    bubble(draw, (54, 795, 526, 1006),
           ["能力による損傷は", "修復されている", "そうです"], font36, (528, 1039))
    bubble(draw, (530, 1163, 963, 1260),
           ["……それで、死因は？"], font34, (502, 1285))
    bubble(draw, (436, 1320, 970, 1416),
           ["警察が調べています"], font36)

    page.save(OUTPUT, optimize=True)
    contents = OUTPUT.read_bytes()
    assert contents[:8] == b"\\x89PNG\\r\\n\\x1a\\n"
    assert Image.open(OUTPUT).size == PAGE_SIZE
    manifest = {
        "p06_v03.png": {
            "page": 6,
            "status": "candidate-needs-visual-review",
            "width": PAGE_SIZE[0],
            "height": PAGE_SIZE[1],
            "bytes": len(contents),
            "sha256": sha256(contents).hexdigest(),
            "source": {
                "p06.png": sha256(SOURCE_P06.read_bytes()).hexdigest(),
                "p07.png": sha256(SOURCE_P07.read_bytes()).hexdigest(),
            },
            "notes": "Recomposed art and precise independently typeset Japanese lettering; original files preserved.",
        }
    }
    MANIFEST.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print("Rendered:", OUTPUT.relative_to(ROOT), len(contents), manifest["p06_v03.png"]["sha256"])


if __name__ == "__main__":
    main()
