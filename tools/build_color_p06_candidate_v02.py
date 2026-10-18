#!/usr/bin/env python3
"""P06 color manga page v02: coherent coffin portrait, reaching hand, attendant.

Independent raster illustration and Japanese dialogue layer. This is an art
candidate, not a final accepted page. No P01/P05 source imagery is imported.
"""
from __future__ import annotations
import argparse
import hashlib
from pathlib import Path
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1400, 2100
PAPER = (241, 240, 235)
INK = (22, 30, 38)
BORDER = 14
RECTS = [
    (48, 54, 1352, 838),      # upper half: Sakaki in his coffin
    (730, 864, 1352, 1295),   # right middle: Aki's hand stops
    (48, 864, 700, 1746),     # left vertical: funeral attendant
    (730, 1323, 1352, 2044),  # lower right: coffin edge and unanswered question
]
SEED = 20261018

def font(size, serif=False):
    family = "Noto Serif CJK JP" if serif else "Noto Sans CJK JP"
    name = subprocess.check_output(["fc-match", "-f", "%{file}", family], text=True).strip()
    return ImageFont.truetype(name, size)

def poly(draw, coords, fill, outline=None, width=3):
    draw.polygon(coords, fill=fill)
    if outline:
        draw.line(coords+[coords[0]], fill=outline, width=width, joint="curve")

def glow(canvas, box, rgb):
    x0,y0,x1,y1=box
    hh,ww=y1-y0,x1-x0
    yy,xx=np.mgrid[:hh,:ww]
    cx,cy=ww*.72,hh*.22
    f=np.exp(-(((xx-cx)/(ww*.95))**2+((yy-cy)/(hh*.8))**2))
    rng=np.random.default_rng(SEED+ww+hh)
    noise=rng.normal(0,1.5,(hh,ww))
    data=np.empty((hh,ww,3),dtype=np.uint8)
    for i,v in enumerate(rgb):
        data[:,:,i]=np.uint8(np.clip(v+28*f+noise,0,255))
    canvas.paste(Image.fromarray(data,"RGB"),(x0,y0))

def coffin(draw, x0,y0,x1,y1, pale=True):
    # Broad diagonal casket with four visible planes.
    a=(x0+int(.07*(x1-x0)),y0+int(.68*(y1-y0)))
    b=(x0+int(.70*(x1-x0)),y0+int(.16*(y1-y0)))
    c=(x0+int(.93*(x1-x0)),y0+int(.29*(y1-y0)))
    d=(x0+int(.30*(x1-x0)),y0+int(.84*(y1-y0)))
    poly(draw,[a,b,c,d],(205,214,216) if pale else (126,136,140),(66,78,85),7)
    poly(draw,[a,d,(d[0],d[1]+68),(a[0],a[1]+68)],(138,149,154),(66,78,85),5)
    poly(draw,[d,c,(c[0],c[1]+68),(d[0],d[1]+68)],(167,178,180),(66,78,85),5)
    draw.line([a,b,c,d,a],fill=(243,247,245),width=7)
    draw.line([(a[0]+18,a[1]-12),(b[0]+8,b[1]+13),(c[0]-22,c[1]+12)],fill=(249,251,249),width=6)

def upper(canvas):
    box=RECTS[0];glow(canvas,box,(39,49,61))
    d=ImageDraw.Draw(canvas)
    x0,y0,x1,y1=box
    d.polygon([(x0,y0+580),(x1,y0+430),(x1,y1),(x0,y1)],fill=(55,64,72))
    d.line([(x0,y0+580),(x1,y0+430)],fill=(110,119,125),width=6)
    coffin(d,155,200,1280,760)
    # A pillow and Sakaki's neck, drawn over the open inner casket surface.
    d.ellipse((700,245,1085,563),fill=(232,237,234),outline=(135,145,150),width=7)
    poly(d,[(560,655),(727,455),(906,502),(1135,697),(1100,784),(600,785)],
         (211,216,212),(108,119,125),5)
    poly(d,[(715,504),(805,496),(824,552),(742,589)],(178,159,147),(100,99,101),4)
    # Sakaki: adult 32, black hair, closed eyes, uninjured skin.
    poly(d,[(757,299),(828,263),(911,276),(967,338),(987,412),(955,478),
            (894,524),(813,503),(765,460),(728,383)],(188,168,154),(83,86,93),5)
    poly(d,[(726,374),(750,294),(803,254),(876,253),(941,294),(978,344),
            (940,331),(918,351),(890,314),(850,341),(815,307),(785,359),
            (747,366)],(17,24,34),(10,15,23),7)
    d.line([(788,408),(837,412)],fill=(79,74,77),width=5)
    d.line([(896,418),(945,417)],fill=(79,74,77),width=5)
    d.line([(858,439),(849,464),(864,470)],fill=(115,103,101),width=4)
    d.arc((838,466,916,493),15,166,fill=(119,94,92),width=3)
    d.line([(775,480),(810,505)],fill=(217,197,180),width=5)
    # Plain white clothing. No candy, scars or supernatural glow.
    d.line([(671,596),(635,741)],fill=(247,249,245),width=14)
    d.line([(1008,614),(1051,738)],fill=(244,245,240),width=12)
    d.rectangle((x0,y0,x1,y1),outline=INK,width=BORDER)

def hand_panel(canvas):
    """Continue the *same* Sakaki face from panel 1; Aki stops short of it.

    The crop is taken from the already rendered upper panel, not a separately
    illustrated face. The hand and cheek remain visibly separated.
    """
    box = RECTS[1]
    # Capture before painting this panel, so character features stay identical.
    face = canvas.crop((728, 252, 990, 520))
    glow(canvas, box, (38, 47, 57))
    face = face.resize((380, 420), Image.Resampling.LANCZOS)
    canvas.paste(face, (972, 866))
    d = ImageDraw.Draw(canvas)
    # Sleeve emerges from the bottom-left, without crossing the coffin edge.
    poly(d, [(738, 1279), (762, 1192), (822, 1138), (872, 1140),
             (892, 1196), (835, 1293)], (19, 25, 34), (8, 13, 19), 6)
    d.line([(756, 1223), (828, 1172)], fill=(111, 120, 128), width=4)
    # Aki's palm and four distinct fingers, reaching toward the face.
    # The rightmost fingertip is x=945; the face starts at x=972.
    poly(d, [(848, 1188), (865, 1154), (887, 1124), (899, 1100),
             (911, 1099), (917, 1112), (914, 1126), (907, 1141),
             (927, 1095), (939, 1091), (945, 1105), (938, 1121),
             (920, 1157), (902, 1185), (879, 1210), (855, 1209)],
         (184, 156, 143), (80, 71, 70), 5)
    d.line([(872, 1160), (901, 1112)], fill=(220, 189, 171), width=5)
    d.line([(889, 1183), (920, 1120)], fill=(220, 187, 168), width=4)
    d.line([(855, 1192), (870, 1202)], fill=(119, 91, 85), width=3)
    # Explicit unfilled air gap: do not draw touching fingertips.
    d.rectangle(box, outline=INK, width=BORDER)

def attendant(canvas):
    box=RECTS[2];glow(canvas,box,(43,48,54))
    d=ImageDraw.Draw(canvas)
    x0,y0,x1,y1=box
    # One half of the funeral attendant's face; no excessive acting.
    poly(d,[(70,910),(465,906),(539,1050),(510,1375),(442,1560),
            (278,1655),(88,1630)],(21,28,37),(13,18,26),6)
    poly(d,[(255,1038),(428,1085),(480,1220),(453,1417),(377,1517),
            (275,1482),(221,1347)],(164,151,144),(68,71,78),6)
    poly(d,[(218,1100),(250,1013),(396,993),(470,1097),(448,1137),
            (398,1084),(302,1104)],(24,30,38),(13,17,22),5)
    d.line([(337,1230),(406,1238)],fill=(68,69,74),width=5)
    d.line([(404,1275),(422,1368),(406,1382)],fill=(110,100,99),width=4)
    d.line([(356,1430),(414,1435)],fill=(97,81,82),width=4)
    d.polygon([(58,1630),(247,1537),(480,1604),(665,1746),(48,1746)],fill=(24,31,41))
    d.line([(250,1539),(356,1730)],fill=(138,145,146),width=4)
    d.rectangle(box,outline=INK,width=BORDER)

def strip(canvas):
    box=RECTS[3];glow(canvas,box,(41,49,58))
    d=ImageDraw.Draw(canvas)
    d.polygon([(754,1930),(1140,1420),(1328,1510),(968,2027)],fill=(204,211,212))
    d.line([(754,1907),(1136,1400),(1334,1485)],fill=(246,249,247),width=9)
    d.line([(815,2000),(1220,1520)],fill=(143,155,161),width=7)
    # Aki's fingertips stop above the coffin rim; the body stays outside this panel.
    poly(d,[(1170,2040),(1130,1980),(1104,1922),(1123,1902),
            (1152,1917),(1188,1969),(1212,2040)],(181,155,142),(79,75,79),5)
    d.line([(1105,1924),(1092,1895),(1104,1870)],fill=(198,172,157),width=13)
    d.rectangle(box,outline=INK,width=BORDER)

def balloon(draw, xy, text, size=38):
    x0,y0,x1,y1=xy
    draw.rounded_rectangle(xy,radius=34,fill=(250,249,244,255),outline=INK,width=5)
    f=font(size)
    bbox=draw.multiline_textbbox((0,0),text,font=f,spacing=7,align="center")
    tw,th=bbox[2]-bbox[0],bbox[3]-bbox[1]
    draw.multiline_text((x0+(x1-x0-tw)/2,y0+(y1-y0-th)/2-bbox[1]),text,
                        font=f,fill=INK,spacing=7,align="center")

def title_layer():
    im=Image.new("RGBA",(W,H),(0,0,0,0));d=ImageDraw.Draw(im)
    balloon(d,(70,1010,420,1230),"能力による損傷は\n修復されている\nそうです",36)
    balloon(d,(70,1460,635,1600),"……それで、死因は？",36)
    balloon(d,(765,1510,1320,1660),"警察が調べています",36)
    d.text((1270,2028),"06",font=font(26),fill=(224,226,225,255))
    return im

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--out-dir",type=Path,default=Path("build/episode01-color/p06-v02"))
    a=p.parse_args();a.out_dir.mkdir(parents=True,exist_ok=True)
    art=Image.new("RGB",(W,H),PAPER)
    upper(art);hand_panel(art);attendant(art);strip(art)
    overlay=title_layer()
    composite=Image.alpha_composite(art.convert("RGBA"),overlay).convert("RGB")
    for name,im in [("p06-art-v02.png",art),("p06-text-v02.png",overlay),
                    ("p06-color-candidate-v02.png",composite)]:
        dest=a.out_dir/name;im.save(dest,optimize=True)
        print(name,im.size,hashlib.sha256(dest.read_bytes()).hexdigest())
    preview=a.out_dir/"p06-preview-v02.webp"
    composite.resize((560,840),Image.Resampling.LANCZOS).save(preview,quality=82)
    print(preview.name,hashlib.sha256(preview.read_bytes()).hexdigest())
if __name__=="__main__":
    main()
