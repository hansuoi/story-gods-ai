#!/usr/bin/env python3
"""Color candidate revision P13–P16 from stored P13–P16 AI mosaic.

Only visual source fragments are reused. Discard the AI's invented dialogue
and typeset the actual Japanese episode name separately. Do not overwrite
existing v01 candidates. All new pages need visual approval.
"""
from __future__ import annotations
from pathlib import Path
from hashlib import sha256
import json
from PIL import Image,ImageDraw,ImageFont,ImageOps
from render_episode01_p09_p10 import BASE, FONT_FILE, new_page, draw_panel, balloon

SRC=BASE/'sources/p13_p16_generated_montage.png'

def note(page,box,lines,fontsize=32):
    d=ImageDraw.Draw(page)
    x0,y0,x1,y1=box
    d.rounded_rectangle(box,radius=18,fill='#f4efe3',outline='#646b6a',width=5)
    f=ImageFont.truetype(FONT_FILE,fontsize)
    y=(y0+y1-len(lines)*int(fontsize*1.5))/2
    for line in lines:
        d.text((x0+25,y),line,font=f,fill='#253239')
        y+=int(fontsize*1.5)


def make_p13(src):
    p=new_page()
    # Eight-year-old materials, worn envelope; do not show AI's exposition.
    original_p13=Image.open(BASE/'p13_v01.png').convert('RGB')
    draw_panel(p,original_p13.crop((33,32,991,721)),(30,30,994,703))
    # Multiple lives represented by many ordinary records (personal details unreadable).
    draw_panel(p,src.crop((6,733,378,983)),(30,723,500,1162))
    d=ImageDraw.Draw(p)
    d.rectangle((71,760,469,1137),fill='#e5e0d4',outline='#7a827d',width=4)
    d.text((98,782),'水害住所一覧',font=ImageFont.truetype(FONT_FILE,28),fill='#505a5b')
    for y in range(847,1127,45):
        d.line((88,y,449,y),fill='#b2b8b0',width=3)
        d.line((170,y-39,170,y),fill='#b2b8b0',width=3)
    # Reuse the actual district map, not a randomly drawn location.
    draw_panel(p,src.crop((17,516,259,718)),(520,723,994,1162))
    # HOLD should be obvious, but the underlying decision remains unknown.
    draw_panel(p,src.crop((133,337,376,508)),(30,1182,994,1506))
    return p


def make_p14(src):
    p=new_page()
    # Earlier file number carried forward; date comes from old dossier.
    draw_panel(p,src.crop((12,520,226,724)),(30,30,994,285))
    note(p,(518,53,965,239),['2018年／汀橋','案件番号 18-07'],fontsize=35)
    # Aki talking by phone, no AI-generated hesitation dialogue.
    draw_panel(p,src.crop((392,251,654,440)),(30,305,615,820))
    ImageDraw.Draw(p).rectangle((617,307,993,819),fill='#465561')
    balloon(p,(622,388,967,657),['当日の行き先に','関係する資料が','あります'],fontsize=29)
    # Detective's existing color character art, correct warning.
    draw_panel(p,src.crop((392,11,635,237)),(30,840,615,1216))
    ImageDraw.Draw(p).rectangle((617,842,993,1214),fill='#3b4b56')
    balloon(p,(621,899,967,1179),['現場には','近づかないで','ください'],fontsize=34)
    # Wordless action: Aki chooses to leave rather than continuing the call.
    draw_panel(p,src.crop((400,791,623,980)),(30,1236,994,1506))
    return p


def make_p15(src):
    p=new_page()
    # Office lock in close-up, including original quiet click sound.
    draw_panel(p,src.crop((778,251,988,376)),(30,30,994,370))
    # Aki heading beneath elevated bridge: painterly figure not an icon.
    # Crop toward Aki's head rather than the AI caption on the right.
    region=(30,390,994,1163)
    x0,y0,x1,y1=region
    full=src.crop((783,475,999,729))
    walking=ImageOps.fit(full,(x1-x0,y1-y0),Image.Resampling.LANCZOS,centering=(.5,.22))
    p.paste(walking,(x0,y0))
    ImageDraw.Draw(p).rectangle((x0,y0,x1-1,y1-1),outline='#20272b',width=5)
    # Unanswered interior thought over nighttime underpass (no character in this small panel).
    draw_panel(p,src.crop((786,770,1137,980)),(30,1183,994,1506))
    balloon(p,(474,1238,965,1447),['……誰に会う','つもりだったの'],fontsize=39)
    return p


def make_p16(src):
    p=new_page()
    # The abandoned utility building with old gate and water gauge area.
    draw_panel(p,src.crop((1157,123,1375,269)),(30,30,994,724))
    # Fresh-looking fastener on corroded hinge, visible through site fence area.
    draw_panel(p,src.crop((1156,283,1399,430)),(30,744,502,1112))
    # Aki stops at boundary, not physically reaching the hinge.
    draw_panel(p,src.crop((1154,447,1386,588)),(521,744,994,1112))
    # The offscreen voice comes from behind; don't prematurely show Nagi.
    draw_panel(p,src.crop((1163,866,1393,980)),(30,1132,994,1506))
    balloon(p,(483,1195,970,1379),['そこ、工事中ですよ'],fontsize=41)
    return p


def main():
    src=Image.open(SRC).convert('RGB')
    assert src.size==(1536,1024)
    manifest_path=BASE/'revision-manifest.json'
    manifest=json.loads(manifest_path.read_text(encoding='utf-8')) if manifest_path.exists() else {}
    for name,fun in [('p13_v02.png',make_p13),('p14_v02.png',make_p14),('p15_v02.png',make_p15),('p16_v01.png',make_p16)]:
        im=fun(src)
        assert im.size==(1024,1536)
        path=BASE/name
        im.save(path,optimize=True)
        raw=path.read_bytes()
        assert raw[:8]==b'\x89PNG\r\n\x1a\n'
        manifest[name]={'page':int(name[1:3]),'status':'candidate-needs-visual-review','width':1024,'height':1536,'bytes':len(raw),
          'sha256':sha256(raw).hexdigest(), 'source':{'sources/p13_p16_generated_montage.png':sha256(SRC.read_bytes()).hexdigest(),**({'p13_v01.png':sha256((BASE/'p13_v01.png').read_bytes()).hexdigest()} if name=='p13_v02.png' else {})},
          'notes':'P13–P16 cinematic color mosaic crop, independently typeset exact name dialogue; no final acceptance.'}
        print(name,len(raw),manifest[name]['sha256'])
    manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')

if __name__=='__main__': main()