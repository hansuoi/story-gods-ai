#!/usr/bin/env python3
"""Create four *color review candidates* of the 2024 flooded underpass rescue.

All source artwork is retained losslessly. Rescue photo fragments and Sakaki's
living portrait were generated for this project in previous sessions. The
small technical elements are hand-composited to preserve the exact physical
sequence: blocked latch -> three drops -> retaining-pin break -> human rescue
-> only broken pin repaired. Not accepted as final manga artwork.
"""
from __future__ import annotations

from pathlib import Path
from hashlib import sha256
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter, ImageEnhance
import json, math, random

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/art/episode-01/finish/color-candidates'
RESCUE=BASE/'sources/p01_p04_rescue_source.png'
SAKAKI=BASE/'sources/sakaki_living_smile.png'
W,H=1024,1536
FONT=Path('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc')
PAGE='#f9f8f3'; DARK='#152632'; WHITE='#fffefa'


def font(n):return ImageFont.truetype(str(FONT),n)

def page():return Image.new('RGB',(W,H),PAGE)

def fit(src,crop,sz,center=(.5,.5),tone=0):
    art=ImageOps.fit(src.crop(crop),sz,method=Image.Resampling.LANCZOS,centering=center)
    if tone: art=Image.blend(art,Image.new('RGB',sz,'#0e3046'),tone)
    return art

def frame(im,region,color=DARK,width=7):
    ImageDraw.Draw(im).rectangle(tuple(region),outline=color,width=width)

def scene(im,source,crop,box,center=(.5,.5),tone=0):
    x0,y0,x1,y1=box
    im.paste(fit(source,crop,(x1-x0,y1-y0),center,tone),(x0,y0));frame(im,box)

def bg_gradient(im,box,top,bottom):
    x0,y0,x1,y1=box;h=y1-y0;w=x1-x0
    grad=Image.new('RGB',(w,h));pix=grad.load()
    a=tuple(int(top.lstrip('#')[i:i+2],16) for i in (0,2,4));b=tuple(int(bottom.lstrip('#')[i:i+2],16) for i in (0,2,4))
    for y in range(h):
        t=y/(h-1)
        color=tuple(round((1-t)*a[i]+t*b[i]) for i in range(3))
        for x in range(w):pix[x,y]=color
    im.paste(grad,(x0,y0));frame(im,box)

def paste_face(im,portrait,rect,blur=10):
    x0,y0,x1,y1=rect
    face=fit(portrait,(8,10,235,218),(x1-x0,y1-y0),(.51,.47))
    mask=Image.new('L',face.size,0);d=ImageDraw.Draw(mask)
    d.ellipse((5,0,face.width-5,face.height-1),fill=255)
    mask=mask.filter(ImageFilter.GaussianBlur(blur))
    im.paste(face,(x0,y0),mask)

def draw_text(im,box,lines,size=39,fill=DARK,align='center',panel=None,vertical=False):
    # Use a real Japanese font. Fit without clipping rather than trusting
    # image-generated speech bubbles and their hallucinated kanji.
    d=ImageDraw.Draw(im);x0,y0,x1,y1=box
    pad=20
    if panel is not None:
        d.rounded_rectangle(box,radius=min(44,(y1-y0)//3),fill=panel,outline=DARK,width=5)
    line_spacing=1.32
    chosen=size
    for fsize in range(size,19,-1):
        f=font(fsize);lh=int(fsize*line_spacing)
        if max((d.textbbox((0,0),t,font=f)[2] for t in lines),default=0)<(x1-x0-2*pad) and len(lines)*lh<(y1-y0-12):
            chosen=fsize;break
    f=font(chosen);lh=int(chosen*line_spacing)
    y=y0+((y1-y0)-len(lines)*lh)//2
    for t in lines:
        b=d.textbbox((0,0),t,font=f)
        x=x0+((x1-x0)-(b[2]-b[0]))//2 if align=='center' else x0+pad
        d.text((x,y),t,font=f,fill=fill,stroke_width=0)
        y+=lh
    return chosen

def balloon(im,box,lines,size=38):return draw_text(im,box,lines,size=size,panel=WHITE)

def rain(im,box,seed=14,n=125,alpha=100):
    rand=random.Random(seed);layer=Image.new('RGBA',im.size,(0,0,0,0));d=ImageDraw.Draw(layer)
    x0,y0,x1,y1=box
    for _ in range(n):
        x=rand.randrange(x0,x1);y=rand.randrange(y0,y1);length=rand.randrange(14,51)
        d.line((x,y,x-11,y+length),fill=(221,244,249,alpha),width=2)
    im.paste(Image.alpha_composite(im.convert('RGBA'),layer).convert('RGB'))

def metal(im,box,broken=True,impact=False,repair=False,scale=1):
    """Hand-render one physically continuous door retaining-pin mechanism."""
    x0,y0,x1,y1=box
    # Detailed, low-saturation steel plate over photographic concrete/water.
    d=ImageDraw.Draw(im)
    w=x1-x0;h=y1-y0
    px=lambda v:x0+round(v*w)
    py=lambda v:y0+round(v*h)
    d.rounded_rectangle((px(.17),py(.06),px(.87),py(.94)),radius=11,fill='#5a727e',outline='#b3c5c6',width=12)
    d.rounded_rectangle((px(.23),py(.11),px(.82),py(.89)),radius=9,fill='#2b4759',outline='#7e9faa',width=6)
    d.line((px(.45),py(.12),px(.48),py(.87)),fill='#9bb2b9',width=11)
    d.rounded_rectangle((px(.36),py(.25),px(.61),py(.44)),radius=12,fill='#8a9fa6',outline='#354b5b',width=8)
    d.ellipse((px(.43),py(.30),px(.52),py(.40)),fill='#354f60',outline='#d0d7d1',width=5)
    d.line((px(.48),py(.36),px(.69),py(.30)),fill='#bfcdd0',width=17)
    d.line((px(.48),py(.36),px(.69),py(.30)),fill='#344955',width=6)
    # Only the narrow, already-bent retaining pin changes across pages.
    path=[(px(.43),py(.51)),(px(.53),py(.57)),(px(.48),py(.64)),(px(.59),py(.73))]
    d.line(path,fill='#1b303f',width=23,joint='curve')
    d.line(path,fill='#bbd0d2',width=9,joint='curve')
    if broken and not repair:
        d.ellipse((px(.465),py(.621),px(.505),py(.661)),fill='#122739',outline='#d4ecf0',width=3)
        d.line((px(.46),py(.63),px(.51),py(.65)),fill='#112c3c',width=8)
    if repair:
        d.arc((px(.38),py(.46),px(.65),py(.81)),56,291,fill='#d8eff1',width=7)
        d.arc((px(.35),py(.44),px(.68),py(.84)),40,296,fill='#68b6d3',width=3)
    for xc,yc in ((.31,.20),(.74,.20),(.32,.8),(.75,.78)):
        cx,cy=px(xc),py(yc);rr=9
        d.ellipse((cx-rr,cy-rr,cx+rr,cy+rr),fill='#263b48',outline='#adbec3',width=3)
        d.line((cx-5,cy-4,cx+5,cy+5),fill='#8aa4ab',width=2)
    if impact:
        # Upstream-to-pin axis; no energy beam or a wall of water.
        target=(px(.485),py(.642));start=(x0-160,py(.91))
        d.line((start,target),fill='#d8f7f5',width=6)
        d.line((start[0]-20,start[1]+12,target[0]-4,target[1]+2),fill='#8bdce8',width=2)
        tx,ty=target
        for ax,ay in ((0,-38),(-33,-18),(34,0),(-20,31),(25,28)):
            d.line((tx,ty,tx+ax,ty+ay),fill='#f1ffff',width=4)


def droplets(im,points):
    d=ImageDraw.Draw(im)
    for x,y,rad in points:
        d.ellipse((x-rad,y-rad,x+rad,y+rad),fill='#b9e7f1',outline='#f5ffff',width=4)
        d.arc((x-rad+6,y-rad+6,x+rad-5,y+rad-6),185,310,fill='#31647a',width=3)
        d.ellipse((x-rad//2,y-rad//2-3,x-rad//4,y-rad//4),fill='white')


def shirt_body(im,box):
    x0,y0,x1,y1=box;d=ImageDraw.Draw(im)
    w=x1-x0;h=y1-y0
    X=lambda v:x0+int(w*v);Y=lambda v:y0+int(h*v)
    d.polygon([(X(.02),Y(1)),(X(.10),Y(.28)),(X(.28),Y(.06)),(X(.72),Y(.08)),(X(.91),Y(.30)),(X(.98),Y(1))],fill='#dadfda')
    d.polygon([(X(.15),Y(.19)),(X(.30),Y(.11)),(X(.5),Y(.48)),(X(.37),Y(.36))],fill='#f6f6ea')
    d.polygon([(X(.7),Y(.1)),(X(.84),Y(.23)),(X(.61),Y(.48)),(X(.50),Y(.47))],fill='#f9faf2')
    for i in range(4):
        yy=Y(.56+i*.12);d.line((X(.52),yy,X(.515),yy+8),fill='#9da7a5',width=3)
    d.line((X(.50),Y(.45),X(.52),Y(.98)),fill='#95a5a5',width=4)
    d.line((X(.18),Y(.42),X(.26),Y(.97)),fill='#aab5b3',width=5)
    d.line((X(.84),Y(.42),X(.73),Y(.97)),fill='#aab5b3',width=5)


def sakaki_portrait(im,src,box,smile=True):
    x0,y0,x1,y1=box
    d=ImageDraw.Draw(im)
    # An illustrated long, relaxed white-shirt silhouette; portrait face
    # supplied from another generated project asset (not an SVG placeholder).
    shirt_body(im,(x0,y0+int((y1-y0)*.43),x1,y1))
    face_w=int((x1-x0)*.55);face_h=int((y1-y0)*.53)
    cx=(x0+x1)//2
    paste_face(im,src,(cx-face_w//2,y0+20,cx+face_w//2,y0+20+face_h),6)
    if smile:
        # White candy stick from right corner, clearly distinguishable.
        c_x=cx+int(face_w*.23); c_y=y0+int(face_h*.79)
        d.line((c_x,c_y,c_x+49,c_y+31),fill='#e9efea',width=8)
        d.line((c_x,c_y,c_x+49,c_y+31),fill='#9ba9ac',width=1)


def splash(im,center,r=120):
    d=ImageDraw.Draw(im);cx,cy=center
    for i in range(12):
        ang=math.pi*i/6;dx=math.cos(ang);dy=math.sin(ang)*.45
        r1=r*.44;r2=r*(.65+(i%3)*.13)
        d.line((cx+r1*dx,cy+r1*dy,cx+r2*dx,cy+r2*dy),fill='#c1e8f1',width=6)
        d.ellipse((cx+r2*dx-5,cy+r2*dy-5,cx+r2*dx+5,cy+r2*dy+5),fill='#f6ffff')
    for k in range(3):
        dx=k*27;d.arc((cx-r-dx//2,cy-25-dx//3,cx+r+dx//2,cy+35+dx//4),5,175,fill='#a0d7e5',width=4)


def boot(im,box):
    x0,y0,x1,y1=box;d=ImageDraw.Draw(im)
    w=x1-x0;h=y1-y0;X=lambda x:x0+w*x;Y=lambda y:y0+h*y
    # Wet leather derby boot, one STEP entering floodwater, no person's face.
    outline=[(X(.35),Y(.10)),(X(.63),Y(.06)),(X(.68),Y(.34)),(X(.76),Y(.61)),(X(.96),Y(.74)),(X(.95),Y(.85)),(X(.82),Y(.88)),(X(.45),Y(.87)),(X(.28),Y(.76)),(X(.27),Y(.47))]
    d.polygon(outline,fill='#15212d');d.line(outline+[outline[0]],fill='#9facb3',width=8,joint='curve')
    d.polygon([(X(.36),Y(.2)),(X(.60),Y(.16)),(X(.64),Y(.51)),(X(.37),Y(.62))],fill='#293e50')
    d.line((X(.33),Y(.73),X(.92),Y(.82)),fill='#dbe5e4',width=6)
    for k in range(4):
        y=.39+k*.075
        d.line((X(.43),Y(y),X(.61),Y(y-.026)),fill='#bcc4c5',width=3)
    d.line((X(.39),Y(.23),X(.41),Y(.58)),fill='#5d7989',width=4)
    splash(im,(int(X(.74)),int(Y(.83))),int(w*.40))


def render_p01(src,portrait):
    im=page()
    scene(im,src,(25,0,671,315),(30,30,994,817),center=(.50,.41),tone=.08)
    # A perspective fire door visible in the distance, already warped.
    d=ImageDraw.Draw(im)
    d.polygon([(380,350),(552,333),(561,575),(392,596)],fill='#394e5c',outline='#8ca8b3',width=9)
    d.polygon([(415,376),(539,366),(541,554),(418,574)],fill='#263c4c',outline='#638391',width=6)
    d.line((473,368,483,563),fill='#c7ceca',width=9)
    d.line((509,469,527,465),fill='#dae2d9',width=8)
    d.polygon([(376,550),(561,553),(548,622),(373,640)],fill='#396079')
    rain(im,(40,36,985,807),seed=1,n=100,alpha=78)
    draw_text(im,(75,51,335,135),['2024年'],size=41,panel='#e9e7dd')
    balloon(im,(606,80,953,207),['扉が開かない！'],size=40)
    scene(im,src,(0,690,698,1005),(30,837,994,1171),center=(.48,.53),tone=.17)
    d=ImageDraw.Draw(im)
    # In the second frame only a small wet hand reaches from the door gap,
    # not the boy's face; render a thick, occluding door slab over the photo.
    d.polygon([(37,846),(422,844),(448,1160),(37,1161)],fill='#3b505e',outline='#8097a1',width=12)
    d.polygon([(611,845),(990,841),(990,1161),(593,1164)],fill='#2d4657',outline='#718c98',width=11)
    d.polygon([(447,843),(603,846),(597,1162),(466,1164)],fill='#182c3b')
    d.line((469,900,478,1097),fill='#617d87',width=6)
    # A visibly wet hand behind the narrow slit (photographic source fragment).
    hand=fit(src,(132,750,417,1005),(182,278),(.64,.54),tone=.15)
    im.paste(hand,(435,850))
    d.line((435,846,439,1168),fill='#738b95',width=8)
    d.line((619,846,616,1168),fill='#536c78',width=9)
    balloon(im,(70,852,379,952),['だれか……'],size=35)
    rain(im,(30,838,994,1170),seed=2,n=60,alpha=85)
    scene(im,src,(0,700,697,1006),(30,1191,994,1505),center=(.46,.48),tone=.36)
    # Rescuer's back in the left foreground with a reflective orange stripe.
    d=ImageDraw.Draw(im)
    d.polygon([(30,1489),(45,1351),(133,1271),(261,1283),(343,1489)],fill='#a66b3e',outline='#2b3943',width=7)
    d.line((49,1433,305,1425),fill='#e0d4a2',width=17)
    boot(im,(490,1195,987,1507))
    balloon(im,(82,1205,488,1322),['開けりゃいいんだな？'],size=34)
    return im


def render_p02(src,portrait):
    im=page()
    scene(im,src,(0,0,697,422),(30,30,994,474),tone=.25)
    sakaki_portrait(im,portrait,(430,70,920,474),smile=True)
    balloon(im,(55,75,422,187),['水、どかせるのか？'],size=32)
    balloon(im,(515,340,974,456),['そんな大仕事できねえよ'],size=30)
    scene(im,src,(0,700,697,1006),(30,495,994,853),tone=.32)
    metal(im,(210,514,825,849),broken=False)
    balloon(im,(48,518,369,617),['壊すのは、ここ'],size=33)
    # Thin interlude; three distinct drops isolated from the rain.
    bg_gradient(im,(30,874,994,1078),'#1b374c','#325873')
    droplets(im,[(418,964,17),(534,952,20),(656,966,16)])
    # Finger entering from left; the droplets do NOT strike the pin yet.
    d=ImageDraw.Draw(im)
    d.polygon([(36,1048),(178,992),(350,969),(367,982),(348,1001),(205,1026),(140,1070),(36,1074)],fill='#b99786')
    frame(im,(30,874,994,1078))
    # Last frame keeps Sakaki's eye and the single pin on one aiming axis.
    scene(im,src,(0,700,697,1006),(30,1099,994,1506),tone=.32)
    paste_face(im,portrait,(32,1144,486,1496),blur=5)
    metal(im,(503,1120,976,1492),broken=False)
    d=ImageDraw.Draw(im);d.line((431,1356,760,1340),fill='#b4dce5',width=2)
    balloon(im,(489,1106,795,1219),['……よし'],size=39)
    return im


def render_p03(src,portrait):
    im=page()
    scene(im,src,(0,700,697,1006),(30,30,994,631),tone=.29)
    metal(im,(405,58,954,615),broken=True,impact=True)
    d=ImageDraw.Draw(im)
    # tiny single white trail, not a powerful torrent
    d.line((40,551,681,405),fill='#e4ffff',width=8)
    d.line((38,566,686,409),fill='#6bc7e0',width=3)
    droplets(im,[(283,490,11),(402,459,9),(524,431,9)])
    draw_text(im,(54,62,342,156),['ピンッ'],size=59,fill='#ecfaff',panel='#25445b')
    scene(im,src,(0,697,697,1007),(30,652,994,974),tone=.27)
    metal(im,(157,658,602,967),broken=True)
    # A gloved rescue worker operates the lever AFTER the retaining pin breaks.
    d=ImageDraw.Draw(im)
    d.line((669,789,907,873),fill='#1f303e',width=45)
    d.line((732,818,920,863),fill='#6d8190',width=10)
    d.line((699,794,614,747),fill='#263d4b',width=32)
    balloon(im,(596,665,936,772),['押せる！'],size=41)
    scene(im,src,(0,0,697,427),(30,996,994,1366),center=(.52,.62),tone=.05)
    # Leave multiple rescuers involved; image already depicts a gloved
    # rescue worker pulling the child, without claiming Sakaki alone saved him.
    scene(im,src,(0,700,697,1006),(30,1387,994,1507),tone=.39)
    d=ImageDraw.Draw(im)
    d.polygon([(343,1465),(354,1437),(412,1418),(493,1427),(533,1456),(620,1469),(630,1495),(362,1495)],fill='#2a3945',outline='#a1adad',width=5)
    d.line((355,1486,637,1490),fill='#e5e6dc',width=6)
    balloon(im,(50,1394,309,1499),['……たすかった'],size=27)
    return im


def render_p04(src,portrait):
    im=page()
    scene(im,src,(0,439,697,696),(30,30,498,331),tone=.17)
    scene(im,src,(0,700,697,1006),(519,30,994,331),tone=.30)
    sakaki_portrait(im,portrait,(593,47,922,330),smile=True)
    balloon(im,(56,42,289,132),['魔法？'],size=36)
    balloon(im,(691,246,974,326),['仕事だよ'],size=33)
    scene(im,src,(0,693,697,1006),(30,353,994,740),tone=.35)
    metal(im,(334,355,950,732),broken=False,repair=True)
    balloon(im,(51,374,330,469),['雨は？'],size=36)
    balloon(im,(50,558,587,709),['オレが壊したもんじゃないからな'],size=31)
    scene(im,src,(0,0,697,422),(30,761,994,1163),tone=.38)
    # Unmistakably a PHONE call to Aki (not a third party in the scene).
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((54,781,319,1118),radius=28,fill='#182733',outline='#bacbd1',width=9)
    d.rounded_rectangle((76,822,298,1041),radius=8,fill='#c4cfca',outline='#657b84',width=4)
    draw_text(im,(82,843,289,908),['着信：安希ちゃん'],size=24)
    balloon(im,(341,773,982,869),['レシートは持って帰って。'],size=30)
    balloon(im,(340,879,977,980),['プリンも二つ'],size=35)
    balloon(im,(340,990,618,1092),['オレのは？'],size=33)
    balloon(im,(649,990,986,1092),['自分で買って'],size=33)
    scene(im,src,(0,0,697,422),(30,1185,994,1506),tone=.17)
    sakaki_portrait(im,portrait,(304,1188,748,1503),smile=True)
    balloon(im,(649,1200,969,1334),['帰るよ'],size=48)
    return im


def main():
    src=Image.open(RESCUE).convert('RGB');portrait=Image.open(SAKAKI).convert('RGB')
    assert src.size==(697,1008) and portrait.size==(240,260)
    manifest_path=BASE/'revision-manifest.json'
    manifest=json.loads(manifest_path.read_text('utf-8')) if manifest_path.exists() else {}
    sources={str(RESCUE.relative_to(BASE)):sha256(RESCUE.read_bytes()).hexdigest(),
             str(SAKAKI.relative_to(BASE)):sha256(SAKAKI.read_bytes()).hexdigest()}
    for n,fn in ((1,render_p01),(2,render_p02),(3,render_p03),(4,render_p04)):
        art=fn(src,portrait)
        assert art.size==(W,H)
        path=BASE/f'p{n:02d}_v01.png';art.save(path,optimize=True)
        raw=path.read_bytes()
        manifest[path.name]={
           'page':n,'status':'candidate-needs-visual-review',
           'width':W,'height':H,'bytes':len(raw),'sha256':sha256(raw).hexdigest(),
           'source':sources,
           'notes':'2024 underpass rescue color collage from saved art fragments + composited props and precise Japanese typesetting; review required for character continuity, physical actions and final art quality.'
        }
        print(path.name,len(raw),manifest[path.name]['sha256'])
    manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,sort_keys=True,indent=2)+'\n','utf-8')

if __name__=='__main__':main()