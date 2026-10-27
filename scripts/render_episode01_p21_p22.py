#!/usr/bin/env python3
"""P21/P22 color review candidates with the identical P19/P20 evidence photo.
The AI collage is only a source of fragments; dialogue is typeset from the name.
Neither is accepted final artwork. P22 reuses the original P13 envelope art.
"""
from pathlib import Path
from hashlib import sha256
from PIL import Image, ImageDraw, ImageOps
import json
from render_episode01_p17_p18 import BASE, SRC, make_page, scene, balloon, pin, FRAME, W, H, font
from render_episode01_p19_p20 import PHOTO

OLD_SRC = BASE / 'sources/p13_p16_generated_montage.png'

def page21(src, hinge):
    page = make_page()
    scene(page,src,(13,249,247,432),(30,30,994,417),focus=(.40,.5),dim=.06)
    d=ImageDraw.Draw(page)
    d.rectangle((526,37,985,409),fill='#465660')
    balloon(page,(545,96,970,330),['誰がやったかは、','写ってない'],size=37)
    scene(page,src,(917,435,1140,595),(30,437,994,821),focus=(.46,.48),dim=.10)
    d.rectangle((521,446,984,812),fill='#3e4e59')
    balloon(page,(538,512,969,755),['事故だったとも、','まだ言えない'],size=37)
    scene(page,src,(10,444,244,599),(30,841,994,1506),focus=(.46,.51),dim=.15)
    d.rounded_rectangle((347,1172,752,1484),radius=18,fill='#192832',outline='#c2cbcb',width=7)
    view=ImageOps.fit(hinge,(356,262),Image.Resampling.LANCZOS)
    page.paste(view,(371,1197))
    d.rectangle((366,1192,732,1465),outline='#d4dddd',width=4)
    balloon(page,(676,884,956,1008),['……はい'],size=39)
    return page

def page22(src,old):
    page=make_page()
    # Keep old document visible, not the generator's invented explanatory text.
    scene(page,old,(23,9,365,143),(30,30,994,395),focus=(.5,.44),dim=.08)
    d=ImageDraw.Draw(page)
    d.rounded_rectangle((78,266,439,366),radius=16,fill='#e8dfcb',outline='#5d6562',width=5)
    d.text((99,287),'2018年／汀橋',font=font(34),fill='#404949')
    scene(page,src,(13,446,247,599),(30,415,994,776),focus=(.45,.5),dim=.11)
    d.rectangle((538,421,982,768),fill='#404e58')
    balloon(page,(554,480,961,695),['まだ、持ってたんだ'],size=36)
    pin(page,288,675,.34)
    scene(page,src,(916,438,1140,597),(30,796,994,1032),focus=(.46,.49),dim=.13)
    d.rectangle((540,804,985,1026),fill='#3b4a54')
    balloon(page,(562,836,960,982),['「まだ」？'],size=47)
    scene(page,src,(13,249,246,433),(30,1052,994,1506),focus=(.45,.66),dim=.18)
    d.rectangle((522,1058,985,1497),fill='#3a4751')
    balloon(page,(539,1156,970,1378),['仕事でも古い資料を','使うので'],size=34)
    return page

def main():
    src=Image.open(SRC).convert('RGB')
    old=Image.open(OLD_SRC).convert('RGB')
    hinge=Image.open(PHOTO).convert('RGB')
    assert src.size==(1536,1024) and old.size==(1536,1024) and hinge.size==(640,790)
    original={'sources/p17_p20_generated_montage.png':sha256(SRC.read_bytes()).hexdigest(),
              'sources/p19_p20_hinge_photo.png':sha256(PHOTO.read_bytes()).hexdigest()}
    dest=BASE/'revision-manifest.json'
    manifest=json.loads(dest.read_text(encoding='utf-8')) if dest.exists() else {}
    for n,page,extra in ((21,page21(src,hinge),{}),(22,page22(src,old),{'sources/p13_p16_generated_montage.png':sha256(OLD_SRC.read_bytes()).hexdigest()})):
        assert page.size==(W,H)
        out=BASE/f'p{n:02d}_v01.png'
        page.save(out,optimize=True)
        b=out.read_bytes()
        assert b[:8]==b'\x89PNG\r\n\x1a\n'
        manifest[out.name]={'page':n,'status':'candidate-needs-visual-review','bytes':len(b),'width':W,'height':H,'sha256':sha256(b).hexdigest(),'source':{**original,**extra},'notes':'P21 shares the exact P19/P20 composited hinge image; P22 reuses P13 envelope. Color candidates require character costume/gesture repaint and final review.'}
        print(out.name,len(b),manifest[out.name]['sha256'])
    dest.write_text(json.dumps(manifest,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')

if __name__=='__main__':main()
