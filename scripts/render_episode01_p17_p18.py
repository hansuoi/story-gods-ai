#!/usr/bin/env python3
"""Recompose P17/18 single-page *review candidates* from saved AI fragments.

P17: Nagi revealed after her offscreen warning, Aki's news, Nagi's reaction,
      and a silent hand-on-blue-thread pin.
P18: skewed seating, the emergency-call witness, Aki's question and Nagi's
      evasive repair-work answer.
All Japanese speech is typeset separately. Bad AI dialogue on the montage
is deliberately cropped away, not copied into the final artwork.
This does not mark either page as accepted or establish character fidelity.
"""
from __future__ import annotations
from pathlib import Path
import json, hashlib, math, sys
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter, ImageEnhance

ROOT = Path(__file__).resolve().parents[1] # scripts/.. when running from repo
BASE = ROOT / 'docs/art/episode-01/finish/color-candidates'
SRC = BASE / 'sources/p17_p20_generated_montage.png'
W, H = 1024, 1536
FRAME = '#1b242d'; PAPER = '#f6f2e9'; BUBBLE = '#fffdf7'
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'


def make_page():
    return Image.new('RGB', (W,H), PAPER)


def font(sz): return ImageFont.truetype(FONT, sz)


def scene(page, source, crop, region, focus=(.5,.5), dim=0):
    # A fixed crop is used to avoid the AI's invented speech blocks.
    x0,y0,x1,y1=region
    art=ImageOps.fit(source.crop(crop),(x1-x0,y1-y0),method=Image.Resampling.LANCZOS,centering=focus)
    if dim:
        art=Image.blend(art,Image.new('RGB',art.size,'#1c2d3b'),dim)
    page.paste(art,(x0,y0))
    ImageDraw.Draw(page).rectangle((x0,y0,x1-1,y1-1),outline=FRAME,width=7)


def gradient_panel(page, region, top=(60,80,90), bottom=(20,32,44)):
    x0,y0,x1,y1=region
    z=Image.new('RGB',(x1-x0,y1-y0))
    d=ImageDraw.Draw(z)
    for y in range(z.height):
        t=y/max(1,z.height-1); c=tuple(round(a*(1-t)+b*t) for a,b in zip(top,bottom))
        d.line((0,y,z.width,y),fill=c)
    page.paste(z,(x0,y0))
    ImageDraw.Draw(page).rectangle((x0,y0,x1-1,y1-1),outline=FRAME,width=6)


def soft_paste(page,source,crop,box,feather=38):
    x0,y0,x1,y1=box
    src=ImageOps.fit(source.crop(crop),(x1-x0,y1-y0),Image.Resampling.LANCZOS,centering=(.48,.5))
    mask=Image.new('L',src.size,0)
    d=ImageDraw.Draw(mask)
    d.rectangle((0,0,src.width-55,src.height),fill=255)
    mask=mask.filter(ImageFilter.GaussianBlur(feather))
    page.paste(src,(x0,y0),mask)


def balloon(page, box, lines, size=36, align='center'):
    d=ImageDraw.Draw(page)
    x0,y0,x1,y1=box
    d.rounded_rectangle(box,radius=min(56,(y1-y0)//3),fill=BUBBLE,outline=FRAME,width=6)
    f=font(size)
    advance=int(size*1.47)
    y=(y0+y1-advance*len(lines))//2+1
    for line in lines:
        bb=d.textbbox((0,0),line,font=f)
        tw=bb[2]-bb[0]
        if tw>x1-x0-27:raise ValueError(f'balloon text overflow {line!r}, width {tw} > {x1-x0-27}')
        x=(x0+x1-tw)//2 if align=='center' else x0+22
        d.text((x,y),line,font=f,fill='#1c2832',stroke_width=0)
        y+=advance


def pin(page,x,y,scale=1.0,hand=False):
    # Realistic prop silhouette of a silver safety pin with a stitched bright
    # blue thread. Draw at 3x and resample to soften pixelation at manga size.
    factor=3
    size=(int(190*scale*factor),int(170*scale*factor))
    im=Image.new('RGBA',size,(0,0,0,0));d=ImageDraw.Draw(im)
    s=scale*factor
    if hand:
        # fingers curl around the pin: no generated human face in this close-up
        d.polygon([(8*s,124*s),(33*s,78*s),(62*s,71*s),(80*s,88*s),(95*s,65*s),(118*s,71*s),(139*s,90*s),(170*s,104*s),(185*s,149*s),(111*s,169*s),(21*s,162*s)],fill=(206,163,143,255))
        d.line([(42*s,114*s),(64*s,118*s),(90*s,142*s)],fill=(132,88,77,255),width=max(1,int(3*s)))
    # pin head, attached arc, and blue thread (without glowing magic effect)
    d.arc((28*s,16*s,120*s,118*s),start=150,end=385,fill=(232,238,235,245),width=max(1,int(7*s)))
    d.line([(45*s,72*s),(128*s,113*s)],fill=(205,217,223,255),width=max(1,int(6*s)))
    d.ellipse((38*s,55*s,55*s,72*s),outline=(244,251,249,255),width=max(1,int(4*s)))
    d.arc((34*s,31*s,152*s,139*s),start=250,end=440,fill=(31,157,219,255),width=max(1,int(7*s)))
    d.line([(124*s,121*s),(157*s,145*s)],fill=(34,145,213,255),width=max(1,int(5*s)))
    im=im.resize((round(im.width/factor),round(im.height/factor)),Image.Resampling.LANCZOS)
    page.paste(im,(x,y),im)


def p17(src):
    page=make_page()
    # 1. A large wordless entrance. Scene/costume are painterly; the generated
    # hairstyle is NOT a trustworthy strict undercut, so remain provisional.
    gradient_panel(page,(30,30,994,673),top=(93,112,121),bottom=(28,43,54))
    scene(page,src,(394,786,624,965),(542,35,989,668),focus=(.50,.55),dim=.17)
    soft_paste(page,src,(10,249,245,433),(34,35,648,668),feather=27)
    # mask potential remnant of generated caption at right; add calm dark area
    d=ImageDraw.Draw(page)
    d.line([(636,53),(648,667)],fill='#506775',width=5)
    # Keep the safety pin on her jacket, never over the face.
    pin(page,232,594,.35)
    d.rectangle((30,30,993,672),outline=FRAME,width=7)
    # 2. Aki speaks; she is drawn from the same painterly montage not SVG.
    scene(page,src,(917,438,1139,597),(30,693,994,1015),focus=(.44,.50),dim=.07)
    d.rectangle((546,707,988,1008),fill='#344450')
    balloon(page,(566,755,969,952),['夫が、ここで','亡くなりました'],size=38)
    # 3. Nagi looks shaken. No sinister visual effects.
    scene(page,src,(20,268,249,421),(30,1035,994,1227),focus=(.32,.47),dim=.12)
    d.rectangle((545,1042,986,1220),fill='#43515b')
    balloon(page,(554,1052,966,1207),['神谷さんの……','奥さん？'],size=36)
    # 4. Entirely silent pin-grip with enough negative space.
    scene(page,src,(66,504,237,599),(30,1247,994,1506),dim=.20)
    pin(page,467,1326,.47)
    ImageDraw.Draw(page).rectangle((30,1247,993,1505),outline=FRAME,width=7)
    return page


def p18(src):
    page=make_page()
    # 1. A two-shot with diagonal seats; original AI wrong lettering never
    # enters the crop. The space reads as a safe waiting-room corner.
    scene(page,src,(11,442,245,600),(30,30,994,578),focus=(.5,.55),dim=.06)
    # 2. Nagi's emergency-call testimony.
    scene(page,src,(14,250,247,431),(30,598,994,947),focus=(.40,.41),dim=.04)
    d=ImageDraw.Draw(page);d.rectangle((551,604,989,940),fill='#3a4850')
    balloon(page,(564,670,967,876),['救急に電話したのは、','あたしです'],size=32)
    # 3. Aki does not interrupt; one concise question.
    scene(page,src,(917,438,1139,597),(30,966,994,1197),focus=(.44,.51),dim=.08)
    d.rectangle((541,972,984,1190),fill='#313f4b')
    balloon(page,(564,1014,963,1142),['なぜ、そこへ？'],size=38)
    # 4. The evasive answer with the blue safety pin in the foreground.
    scene(page,src,(67,510,239,596),(30,1217,994,1506),focus=(.5,.5),dim=.25)
    pin(page,357,1379,.45)
    d.rectangle((534,1225,981,1493),fill='#34424e')
    balloon(page,(548,1277,961,1447),['修復の仕事なんで'],size=34)
    return page


def main():
    src=Image.open(SRC).convert('RGB')
    assert src.size==(1536,1024),src.size
    manifest_path=BASE/'revision-manifest.json'
    manifest=json.loads(manifest_path.read_text(encoding='utf-8')) if manifest_path.exists() else {}
    source_hash=hashlib.sha256(SRC.read_bytes()).hexdigest()
    for n,fun in ((17,p17),(18,p18)):
        page=fun(src)
        assert page.size==(W,H)
        name=f'p{n:02d}_v01.png'; path=BASE/name
        page.save(path,optimize=True)
        raw=path.read_bytes(); assert raw[:8]==b'\x89PNG\r\n\x1a\n'
        manifest[name]={
          'page':n,'status':'candidate-needs-visual-review',
          'width':W,'height':H,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),
          'source':{'sources/p17_p20_generated_montage.png':source_hash},
          'notes':'P17/P18 selected painted fragments, original AI captions excluded and correct name text typeset. Character hair, wardrobe, pin hand need final repaint.'}
        print(name, len(raw),manifest[name]['sha256'])
    manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')

if __name__=='__main__':main()