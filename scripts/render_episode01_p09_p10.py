#!/usr/bin/env python3
"""Create P09/P10 color review candidates from an original AI color montage.

Original source is stored losslessly in the GitHub color-candidates/sources/ folder.
Never edits the original montage. All lettering added separately with Noto CJK.
Candidates must receive visual review before acceptance.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/art/episode-01/finish/color-candidates'
SOURCE = BASE / 'sources/p09_p12_generated_montage.png'
FONT_FILE = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
FONT_FILE_BOLD = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
PAGESIZE = (1024, 1536)

def crop_clean(src: Image.Image, box):
    return src.crop(box).convert('RGB')

def draw_panel(canvas,panel,region):
    x0,y0,x1,y1=region
    image=ImageOps.fit(panel,(x1-x0,y1-y0),method=Image.Resampling.LANCZOS,centering=(.5,.5))
    canvas.paste(image,(x0,y0))
    ImageDraw.Draw(canvas).rectangle((x0,y0,x1-1,y1-1),outline='#20272b',width=5)

def balloon(canvas, box, lines, fontsize=49, roundness=40):
    d=ImageDraw.Draw(canvas)
    d.rounded_rectangle(box,radius=roundness,fill='#fbf9f3',outline='#283036',width=5)
    font=ImageFont.truetype(FONT_FILE,fontsize)
    x0,y0,x1,y1=box
    line_height=int(fontsize*1.35)
    total=len(lines)*line_height
    for i,t in enumerate(lines):
        bb=d.textbbox((0,0),t,font=font)
        t_width=bb[2]-bb[0]
        if t_width>(x1-x0-24):raise ValueError('Lettering too wide: '+t)
        d.text(((x0+x1-t_width)/2,y0+(y1-y0-total)/2+i*line_height-10),t,font=font,fill='#1f252b')

def new_page():return Image.new('RGB',PAGESIZE,'#f5f1e9')

def make_p09(src):
    canvas=new_page()
    # P09-1: empty hallway after funeral; remove AI's premature line.
    p1=crop_clean(src,(8,7,272,267))
    draw_panel(canvas,p1,(31,30,993,678))
    # P09-2: shoe rack, half suddenly unused; AI narration gets replaced by Aki's broken voice.
    p2=crop_clean(src,(8,274,379,455))
    draw_panel(canvas,p2,(31,698,993,1097))
    balloon(canvas,(557,757,962,1072),['ただいま……'],fontsize=50,roundness=47)
    # P09-3: the exact memo from the original picture, separate foreground and no exposition.
    p3=crop_clean(src,(8,459,379,624))
    draw_panel(canvas,p3,(31,1117,993,1506))
    return canvas

def make_p10(src):
    canvas=new_page()
    # P10-1: hand / stopped pen / open notebook in existing cinematic paint.
    p1=crop_clean(src,(771,184,1071,413))
    draw_panel(canvas,p1,(31,30,993,463))
    # P10-2: empty opposite chair and silent desk, no unwanted generated narration.
    p2=crop_clean(src,(390,8,766,277))
    draw_panel(canvas,p2,(31,483,993,1194))
    balloon(canvas,(62,592,505,880),['次はちゃんと','説明してよ'],fontsize=47,roundness=55)
    # P10-3: ticking clock, image only, deliberately NO sound effect.
    p3=crop_clean(src,(607,11,754,165))
    background=Image.new('RGB',(962,292),'#202e3b')
    d=ImageDraw.Draw(background)
    for y in range(292):
        h=int(33+18*y/292)
        d.line((0,y,962,y),fill=(h,h+10,h+19),width=1)
    clock=ImageOps.fit(p3,(280,280),Image.Resampling.LANCZOS)
    background.paste(clock,(594,6))
    draw_panel(canvas,background,(31,1214,993,1506))
    return canvas

def main():
    BASE.mkdir(parents=True,exist_ok=True)
    src=Image.open(SOURCE).convert('RGB')
    assert src.size==(1536,1024),(src.size,SOURCE)
    manifest_path=BASE/'revision-manifest.json'
    manifest=json.loads(manifest_path.read_text(encoding='utf-8')) if manifest_path.exists() else {}
    source_sha=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    for n,fun in [(9,make_p09),(10,make_p10)]:
        target=BASE/f'p{n:02d}_v01.png'
        rendered=fun(src)
        assert rendered.size==PAGESIZE
        rendered.save(target,optimize=True)
        raw=target.read_bytes()
        assert raw[:8]==b'\x89PNG\r\n\x1a\n'
        manifest[target.name]={
            'page':n,'status':'candidate-needs-visual-review','bytes':len(raw),
            'width':1024,'height':1536,'sha256':hashlib.sha256(raw).hexdigest(),
            'source':{'sources/p09_p12_generated_montage.png':source_sha},
            'notes':'AI generated panorama crops with exact Japanese lettering; requires review of scene details and image sampling.'
        }
        print(target, len(raw), manifest[target.name]['sha256'])
    manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')

if __name__=='__main__':main()