#!/usr/bin/env python3
"""P01 v07: replace the two-part hand composition with one continuous door-gap shot.

This is a visual candidate, not an accepted finished manga page. Source images
are local generated artwork from the preceding production run; typography is
added deterministically with Pillow.
"""
from pathlib import Path
import hashlib
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/'docs/art/episode-01/finish/final-candidates/p01'
SOURCE=ART/'assets/p01-panel2-boy-source-v01.webp'
MIDDLE=ART/'assets/middle-source-v01.webp'
BASE=ART/'p01-color-composite-v06.webp'
W,H=1296,474
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'

def hand_panel():
    src=Image.open(SOURCE).convert('RGB')
    # Keep the trapped boy's hand and the wet door in one continuous perspective.
    # Crop the boy's face out of the narrative, rather than masking it with text.
    panel=src.crop((60,0,920,310)).resize((W,H),Image.Resampling.LANCZOS).convert('RGBA')
    # A real photographed metal leaf from the source hides the face. The slit
    # stays closed; the hand alone protrudes on the rescuer's side.
    steel=src.crop((10,0,180,310)).resize((286,H),Image.Resampling.LANCZOS).convert('RGBA')
    panel.alpha_composite(steel,(1010,0))
    d=ImageDraw.Draw(panel,'RGBA')
    d.rectangle((997,0,1014,H),fill=(3,12,22,250))
    d.line((998,0,998,H),fill=(197,219,224,95),width=4)
    d.line((1015,0,1015,H),fill=(2,9,16,180),width=7)
    # Reuse the previously tested rescuer's glove silhouette; replace the
    # flat jacket fill with sampled wet fabric from the rescue artwork.
    prev=Image.open(BASE).convert('RGBA').crop((52,638,1348,1112))
    silhouette=Image.new('L',(W,H),0);mask=ImageDraw.Draw(silhouette)
    mask.polygon([(260,345),(333,358),(402,340),
                  (458,314),(529,306),(566,325),(581,350),(551,382),
                  (490,398),(439,417),(395,450),(335,H),(250,H)],fill=255)
    silhouette=silhouette.filter(ImageFilter.GaussianBlur(1.2))
    layer=Image.new('RGBA',(W,H),(0,0,0,0))
    layer.paste(prev,(0,0),silhouette)
    panel=Image.alpha_composite(panel,layer)
    # Orange rescue jacket: real light-and-shadow texture rather than a flat
    # orange polygon. Preserve a dark waterproof cuff between sleeve and glove.
    real=Image.open(MIDDLE).convert('RGB')
    fabric=real.crop((160,292,340,337)).resize((380,140),Image.Resampling.LANCZOS).convert('RGBA')
    fabric=ImageEnhance.Brightness(fabric).enhance(.80)
    fabric=ImageEnhance.Color(fabric).enhance(.85)
    texmask=Image.new('L',(380,140),0);tm=ImageDraw.Draw(texmask)
    tm.polygon([(0,43),(90,13),(186,0),(290,8),(377,43),(358,93),(267,116),(190,140),(0,140)],fill=230)
    texmask=texmask.filter(ImageFilter.GaussianBlur(2))
    panel.paste(fabric.crop((0,0,380,132)),(0,342),texmask.crop((0,0,380,132)))
    d=ImageDraw.Draw(panel,'RGBA')
    d.line([(262,359),(309,354),(359,365)],fill=(17,31,42,230),width=12)
    d.line([(290,369),(349,379)],fill=(147,163,159,130),width=4)
    # Water spray in the unreachable space between glove and small fingers.
    spray=Image.new('RGBA',(W,H),(0,0,0,0));s=ImageDraw.Draw(spray)
    for x,y,r in [(653,300,2),(694,268,3),(739,322,2),(680,391,3),
                  (760,405,2),(622,354,2),(785,366,2),(708,438,2)]:
        s.ellipse((x-r,y-r,x+r,y+r),fill=(219,244,250,155))
    s.arc((612,289,753,453),start=135,end=244,fill=(219,246,250,120),width=3)
    panel=Image.alpha_composite(panel,spray)
    return panel.convert('RGB')

def main():
    page=Image.open(BASE).convert('RGB')
    row=hand_panel()
    page.paste(row,(52,638))
    draw=ImageDraw.Draw(page)
    # Restore panel border after replacing its full interior.
    draw.rectangle((47,633,1353,1117),outline=(12,24,30),width=8)
    # Speech is an independent typeset layer, never image-generated text.
    bx,by,bw,bh=82,666,348,151
    draw.rounded_rectangle((bx,by,bx+bw,by+bh),radius=35,fill=(252,252,248),outline=(16,31,41),width=6)
    draw.polygon([(bx+242,by+bh-3),(bx+287,by+bh-3),(834,918)],fill=(252,252,248))
    draw.line([(bx+242,by+bh-3),(834,918),(bx+287,by+bh-3)],fill=(16,31,41),width=5)
    draw.line([(bx+251,by+bh-2),(bx+279,by+bh-2)],fill=(252,252,248),width=9)
    font=ImageFont.truetype(FONT,48)
    txt='だれか……';bb=draw.textbbox((0,0),txt,font=font)
    draw.text((bx+(bw-(bb[2]-bb[0]))/2,by+(bh-(bb[3]-bb[1]))/2-bb[1]),txt,font=font,fill=(12,28,39))
    page.save(ART/'p01-color-composite-v07.png',optimize=True)
    page.save(ART/'p01-color-composite-v07.webp',quality=86,method=6)
    row.save(ART/'assets/p01-panel2-hands-v07.webp',quality=90,method=6)
    thumb=page.copy();thumb.thumbnail((560,830));thumb.save(ART/'p01-color-composite-v07-thumb.png')
    for p in [ART/'p01-color-composite-v07.webp',ART/'assets/p01-panel2-hands-v07.webp']:
        print(p.name,p.stat().st_size,hashlib.sha256(p.read_bytes()).hexdigest())
if __name__=='__main__':main()