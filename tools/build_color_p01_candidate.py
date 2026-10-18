#!/usr/bin/env python3
"""Make a reproducible P01 color-layout candidate from committed panel sources.

This is a reading/art candidate, NEVER an automatically accepted final manga page.
The optional --hero-image can replace the provisional vector hero with approved art.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "docs/art/episode-01/finish/final-candidates/p01"
SRC = ART / "assets"
FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
W, H, M = 1400, 1900, 54
PW = W - 2 * M
PANELS = ((58, 502), (586, 455), (1067, 760))
INK = (15, 28, 37)


def fit(image: Image.Image, w: int, h: int) -> Image.Image:
    scale = max(w / image.width, h / image.height)
    image = image.resize(
        (round(image.width * scale) + 2, round(image.height * scale) + 2),
        Image.Resampling.LANCZOS,
    )
    return image.crop(((image.width - w)//2, (image.height - h)//2,
                       (image.width + w)//2, (image.height + h)//2))


def second_panel() -> Image.Image:
    """A slit, a child's hand, an adult glove: hands remain separated."""
    boy = Image.open(SRC / "p01-panel2-boy-source-v01.webp").convert("RGB")
    # Fit original frame without changing the child's hand position.
    child = fit(boy, PW, PANELS[1][1]).convert("RGBA")
    w, h = child.size

    # Mask the child's face using an opaque door leaf copied from its own texture.
    # The reaching hand projects left of the leaf. This is a layout study,
    # not a substitute for independently drawn, fully correct hand anatomy.
    door = boy.crop((60, 4, 398, 301)).convert("RGBA")
    edge = int(w * .65)
    door = door.resize((w - edge, h), Image.Resampling.LANCZOS)
    child.alpha_composite(door, (edge, 0))
    d = ImageDraw.Draw(child, "RGBA")
    d.rectangle((edge-10, 0, edge+19, h), fill=(3, 13, 22, 232))
    d.line((edge+23, 0, edge+23, h), fill=(178, 204, 208, 110), width=5)

    # A single open rescue glove extends from the left, stopping before the
    # child's palm; hand deliberately does not touch, as required by the name.
    glove = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    g = ImageDraw.Draw(glove, "RGBA")
    g.polygon([(0,355),(94,331),(192,346),(280,368),(320,411),(289,h),(0,h)],
              fill=(174,72,49,255))
    g.polygon([(248,352),(328,343),(399,363),(443,389),(398,422),(312,429)],
              fill=(19,35,49,255))
    fingers = [
        [(398,360),(484,317),(532,320),(535,334),(485,348),(425,382)],
        [(412,383),(506,362),(537,373),(527,389),(455,401)],
        [(400,403),(471,408),(495,427),(468,439),(397,430)],
    ]
    for shape in fingers:
        g.polygon(shape, fill=(26,42,56,255))
        g.line(shape+[shape[0]], fill=(93,117,130,180), width=3)
    g.line([(281,374),(350,384),(417,391)], fill=(160,181,181,190), width=6)
    glove = glove.filter(ImageFilter.GaussianBlur(.7))
    child = Image.alpha_composite(child, glove)
    # The gap and gloved fingertip are inspectable at full size.
    return child.convert("RGB")


def bubble(d: ImageDraw.ImageDraw, x, y, w, h, text, font_size, tail=None):
    d.rounded_rectangle((x,y,x+w,y+h),radius=36,fill=(253,253,249),
                        outline=INK,width=6)
    if tail:
        a=(x+w*.28,y+h-3); b=(x+w*.44,y+h-3)
        d.polygon([a,b,tail],fill=(253,253,249))
        d.line([a,tail,b],fill=INK,width=5)
        d.line([(a[0]+6,a[1]-2),(b[0]-6,b[1]-2)],fill=(253,253,249),width=9)
    f=ImageFont.truetype(FONT,font_size)
    bb=d.multiline_textbbox((0,0),text,font=f,spacing=10,align="center")
    d.multiline_text((x+(w-(bb[2]-bb[0]))/2,y+(h-(bb[3]-bb[1]))/2-bb[1]),
                     text,font=f,fill=INK,spacing=10,align="center")


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path,
                        default=ROOT / "build/episode01-color/p01-candidate.png")
    parser.add_argument("--hero-image",type=Path,
                        help="Optional independently verified painting for panel 3")
    a=parser.parse_args()
    if not Path(FONT).exists():
        parser.error("Noto CJK font missing: " + FONT)
    first=fit(Image.open(SRC/"p01-panel1-rescuers-source-v01.webp").convert("RGB"),
              PW,PANELS[0][1])
    middle=second_panel()
    hero_source=a.hero_image or SRC/"p01-panel3-sakaki-pose-reference-v01.webp"
    last=fit(Image.open(hero_source).convert("RGB"),PW,PANELS[2][1])
    out=Image.new("RGB",(W,H),(248,247,243))
    d=ImageDraw.Draw(out)
    for (y,h),tile in zip(PANELS,(first,middle,last)):
        out.paste(tile,(M,y))
        d.rectangle((M-4,y-4,W-M+4,y+h+4),outline=INK,width=7)
    font=ImageFont.truetype(FONT,42)
    d.rounded_rectangle((72,78,430,150),radius=10,
                        fill=(253,252,249),outline=INK,width=4)
    d.text((88,82),"2024年  豪雨",font=font,fill=INK)
    bubble(d,960,94,345,170,"扉が\n開かない！",51,(1070,318))
    bubble(d,85,609,330,152,"だれか……",47,(653,826))
    bubble(d,968,1140,329,190,"開けりゃ\nいいんだな？",48,(753,1382))
    d.text((106,1690),"ザブッ",font=ImageFont.truetype(FONT,50),
           fill=(241,250,251),stroke_width=3,stroke_fill=INK)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    out.save(a.output)
    print(json.dumps({
        "output":str(a.output),"sha256":hashlib.sha256(a.output.read_bytes()).hexdigest(),
        "status":"candidate-not-accepted",
        "source_assets":str(SRC.relative_to(ROOT)),
        "hero_source":str(hero_source),
        "quality_gate":"human visual review is mandatory"
    },ensure_ascii=False))


if __name__=="__main__":
    main()
