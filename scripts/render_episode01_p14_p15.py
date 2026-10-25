#!/usr/bin/env python3
"""P14/P15 color-collage review candidates using versioned original source art.

Painted source images provide setting and characters; exact name dialogue is placed
with NotoSansCJK. The new art is not accepted without individual visual checks.
"""
from __future__ import annotations
import hashlib, json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
from render_episode01_p09_p10 import SOURCE, BASE, FONT_FILE, PAGESIZE, new_page, draw_panel, balloon


def font(sz): return ImageFont.truetype(FONT_FILE,sz)

def simple_phone(canvas,xywh,title):
    """A muted phone prop; no fabricated conversation contents."""
    x,y,w,h=xywh
    d=ImageDraw.Draw(canvas)
    d.rounded_rectangle((x,y,x+w,y+h),radius=20,fill='#18232d',outline='#6f7d85',width=7)
    d.rounded_rectangle((x+11,y+20,x+w-11,y+h-26),radius=6,fill='#718d96')
    bb=d.textbbox((0,0),title,font=font(28))
    d.text((x+(w-bb[2]+bb[0])/2,y+h*.47),title,font=font(28),fill='#f1efe8')
    d.ellipse((x+w*.45,y+h-17,x+w*.55,y+h-6),fill='#b5c2c1')


def make_p14(src):
    page=new_page()
    # Note the old case number in AkI's notebook.
    data=src.crop((1181,282,1523,450)).convert('RGB')
    draw_panel(page,data,(31,30,993,355))
    d=ImageDraw.Draw(page)
    d.rounded_rectangle((534,72,962,278),radius=16,fill='#f3e9d6',outline='#6e6c64',width=5)
    d.text((572,104),'2018年／汀橋',font=font(38),fill='#414b4d')
    d.text((573,169),'案件番号 18-07',font=font(31),fill='#465255')
    # AkI telephones; source shows her face and serious gaze, not a fake detective.
    side=src.crop((783,415,1034,589)).convert('RGB')
    draw_panel(page,side,(31,375,993,926))
    simple_phone(page,(69,487,146,288),'刑事')
    balloon(page,(521,476,965,687),['当日の行き先に','関係する資料が','あります'],fontsize=35)
    # Offscreen detective warning: same office desk, audio only, no invented face.
    interior=src.crop((544,9,760,254)).convert('RGB')
    draw_panel(page,interior,(31,946,993,1232))
    balloon(page,(81,972,899,1186),['現場には近づかないでください'],fontsize=41)
    # Silent choice. Aki leaves the office carrying a dark coat; do not add speech.
    walking=src.crop((18,70,270,215)).convert('RGB')
    draw_panel(page,walking,(31,1252,993,1506))
    return page


def make_p15(src):
    page=new_page()
    # Office door / keys. Small metallic click is non-verbal.
    door=src.crop((18,70,267,220)).convert('RGB')
    draw_panel(page,door,(31,30,993,380))
    d=ImageDraw.Draw(page)
    # Brass locking key, near edge; clear at reading size.
    d.ellipse((877,184,922,229),fill='#d6bc86',outline='#7c6a50',width=7)
    d.ellipse((890,196,907,213),fill='#45515b')
    d.line((879,206,787,227),fill='#c9b489',width=17)
    d.line((815,221,810,241),fill='#bba477',width=13)
    d.line((791,230,786,248),fill='#bba477',width=12)
    # Underpass to waterfront: the landscape matters more than tiny figure detail.
    scenery=src.crop((1160,588,1387,785)).convert('RGB')
    draw_panel(page,scenery,(31,400,993,1197))
    # Aki advancing is small and off-centre so ordinary city scale dominates.
    d=ImageDraw.Draw(page)
    # Foreground concrete pedestrian edge places the figure ON LAND, not in the water.
    d.polygon([(32,1111),(232,1070),(320,1126),(344,1196),(31,1196)],fill='#34424d')
    d.line((33,1110,232,1071),fill='#778691',width=5)
    d.ellipse((202,1061,215,1078),fill='#bc9f91')
    d.polygon([(201,1076),(219,1075),(230,1131),(194,1131)],fill='#212d38')
    d.line((201,1131,198,1155),fill='#192331',width=6)
    d.line((220,1131,230,1155),fill='#192331',width=6)
    # Unanswered question, grounded in Aki's profile under same viaduct.
    face=src.crop((1164,795,1381,985)).convert('RGB')
    draw_panel(page,face,(31,1217,993,1506))
    balloon(page,(497,1266,968,1453),['……誰に会う','つもりだったの'],fontsize=40)
    return page


def main():
    src=Image.open(SOURCE).convert('RGB')
    assert src.size==(1536,1024)
    manifest_path=BASE/'revision-manifest.json'
    manifest=json.loads(manifest_path.read_text(encoding='utf-8')) if manifest_path.exists() else {}
    for n,render in [(14,make_p14),(15,make_p15)]:
        page=render(src)
        assert page.size==PAGESIZE
        p=BASE/f'p{n:02d}_v01.png'
        page.save(p,optimize=True)
        raw=p.read_bytes()
        assert raw.startswith(b'\x89PNG\r\n\x1a\n')
        manifest[p.name]={
            'page':n,'status':'candidate-needs-visual-review','bytes':len(raw),'width':1024,'height':1536,
            'sha256':hashlib.sha256(raw).hexdigest(),
            'source':{'sources/p09_p12_generated_montage.png':hashlib.sha256(SOURCE.read_bytes()).hexdigest()},
            'notes':'Existing painted montage reused; P14 phone and P15 key/action include locally composed props, see visual review.'
        }
        print(p,p.stat().st_size,manifest[p.name]['sha256'])
    manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')

if __name__=='__main__':main()