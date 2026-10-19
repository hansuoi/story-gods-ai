#!/usr/bin/env python3
"""Reframe P07's SILENT mouth close-up without altering its three lower panels.

Uses the unchanged, full-resolution P07 and P05 PNGs stored in the repository.
P06 displays Sakaki's entire still face. This version of P07 moves closer to
the mouth (missing candy stick) and adds out-of-focus funeral flowers, giving
the two consecutive pages distinct beats.

This produces a candidate requiring visual review, not an accepted final page.
"""
from __future__ import annotations

from hashlib import sha256
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs/art/episode-01/finish/color-candidates"
SOURCE_P07 = BASE / "p07.png"
SOURCE_P05 = BASE / "p05.png"
OUTPUT = BASE / "p07_v04.png"
MANIFEST = BASE / "revision-manifest.json"
PAGE_SIZE = (1024, 1536)

def render() -> None:
    original = Image.open(SOURCE_P07).convert("RGB")
    flowers_source = Image.open(SOURCE_P05).convert("RGB")
    assert original.size == PAGE_SIZE and flowers_source.size == PAGE_SIZE

    # P07's upper panel is deliberately a detail shot rather than a repeat
    # of the whole face on P06. All panel division and lettering below stay put.
    page = original.copy()
    frame = (40, 40, 984, 564)
    x0, y0, x1, y1 = frame
    crop = (510, 220, 979, 484)
    close_up = original.crop(crop).resize(
        (x1 - x0, y1 - y0), Image.Resampling.LANCZOS
    )
    page.paste(close_up, (x0, y0))

    # Foreground white funeral flowers come from the existing P05 color
    # artwork, not drawn symbols. Feather all edges to avoid a pasted seam.
    bouquet = flowers_source.crop((0, 1210, 475, 1536)).resize(
        (323, 237), Image.Resampling.LANCZOS
    )
    width, height = bouquet.size
    mask = Image.new("L", bouquet.size, 0)
    pixels = mask.load()
    for y in range(height):
        for x in range(width):
            left_fade = math.exp(-(x / (width * .75))**2 * 2.)
            top_fade = min(1., (y / (height * .4))**2)
            bottom_shape = math.exp(-((height - y) / (height * .85))**2 * .45)
            pixels[x, y] = round(255 * .92 * left_fade * top_fade * bottom_shape)
    mask = mask.filter(ImageFilter.GaussianBlur(29))
    page.paste(bouquet, (x0, y1 - height), mask)

    ImageDraw.Draw(page).rectangle(
        (36, 36, 988, 568), outline=(23, 29, 34), width=5
    )

    # No text, speaker, or composition change in the two middle panels and
    # final Aki panel. Pixel identity prevents accidental lettering changes.
    assert page.crop((0, 569, 1024, 1536)).tobytes() == (
        original.crop((0, 569, 1024, 1536)).tobytes()
    )

    page.save(OUTPUT, optimize=True)
    raw = OUTPUT.read_bytes()
    assert raw.startswith(b"\x89PNG\r\n\x1a\n")
    assert Image.open(OUTPUT).size == PAGE_SIZE
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.exists() else {}
    manifest["p07_v04.png"] = {
        "page": 7,
        "status": "candidate-needs-visual-review",
        "width": 1024,
        "height": 1536,
        "bytes": len(raw),
        "sha256": sha256(raw).hexdigest(),
        "source": {
            "p05.png": sha256(SOURCE_P05.read_bytes()).hexdigest(),
            "p07.png": sha256(SOURCE_P07.read_bytes()).hexdigest(),
        },
        "unchanged_area": "pixels with y >= 569 exactly match p07.png",
        "notes": "Mouth-focused silent funeral panel; P05 white flowers feathered in foreground. Other three panels and exact speech unchanged.",
    }
    MANIFEST.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"Rendered {OUTPUT.relative_to(ROOT)} SHA256={sha256(raw).hexdigest()}")

if __name__ == "__main__":
    render()
