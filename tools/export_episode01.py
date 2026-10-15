#!/usr/bin/env python3
"""Render 32 SVG manuscript proofs as PNG, contact sheet and vector PDF. Not publication approval."""
from pathlib import Path
from io import BytesIO
import argparse
import json
import xml.etree.ElementTree as ET

SRC = Path(__file__).resolve().parents[1] / "docs/art/episode-01/finish/readproof"

def run(out: Path, width: int) -> None:
    import cairosvg
    from PIL import Image, ImageDraw
    from pypdf import PdfReader, PdfWriter

    out.mkdir(parents=True, exist_ok=True)
    thumbs = []
    writer = PdfWriter()
    for n in range(1, 33):
        source = SRC / f"p{n:02d}.svg"
        if not source.is_file():
            raise ValueError(f"Missing page {source}")
        root = ET.parse(source).getroot()
        if (root.get("viewBox"), root.get("width"), root.get("height")) != ("0 0 1600 2400", "1600", "2400"):
            raise ValueError(f"Incorrect canvas on P{n:02d}")
        output = out / f"p{n:02d}.png"
        cairosvg.svg2png(url=str(source), write_to=str(output), output_width=width)
        with Image.open(output) as im:
            if im.size != (width, round(width * 1.5)):
                raise ValueError(f"Incorrect raster dimensions on P{n:02d}: {im.size}")
            thumbs.append(im.convert("RGB").copy())
        page_pdf = PdfReader(BytesIO(cairosvg.svg2pdf(url=str(source), scale=0.45)))
        if len(page_pdf.pages) != 1:
            raise ValueError(f"P{n:02d} created {len(page_pdf.pages)} PDF pages")
        writer.add_page(page_pdf.pages[0])

    pdf_path = out / "episode01-reading-proof.pdf"
    with pdf_path.open("wb") as fp:
        writer.write(fp)
    if len(PdfReader(str(pdf_path)).pages) != 32:
        raise ValueError("Final PDF is not 32 pages")

    gap, label, cols = 18, 30, 4
    h = thumbs[0].height
    sheet = Image.new("RGB", (cols * (width + gap) + gap, 8 * (h + label + gap) + gap), "white")
    draw = ImageDraw.Draw(sheet)
    for i, tile in enumerate(thumbs):
        row, col = divmod(i, cols)
        x = gap + (cols - 1 - col) * (width + gap)
        y = gap + row * (h + label + gap)
        sheet.paste(tile, (x, y + label))
        draw.text((x, y), f"P{i+1:02d}", fill="black")
    sheet.save(out / "contact-sheet.png", optimize=True)

    manifest = {"page_count": 32, "status": "READING PROOF — NOT APPROVED",
                "pdf": pdf_path.name, "contact_sheet": "contact-sheet.png",
                "pages": [f"p{n:02d}.png" for n in range(1, 33)]}
    (out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Rendered 32 PNGs, a contact sheet, and 32-page vector PDF; visual approval NOT performed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path("build/episode01"))
    parser.add_argument("--width", type=int, default=500)
    args = parser.parse_args()
    if not 200 <= args.width <= 1500:
        parser.error("--width must be 200..1500")
    run(args.out, args.width)
