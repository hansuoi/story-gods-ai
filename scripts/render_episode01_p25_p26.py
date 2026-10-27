#!/usr/bin/env python3
"""Color review candidates for Kuzumi's normal senior-worker introduction.
No ominous effects or invented testimony. Character likeness and warm smile
are provisional and must be repainted before acceptance.
"""
from hashlib import sha256
import json
from PIL import Image,ImageDraw
from render_episode01_p17_p18 import BASE,SRC,make_page,scene,balloon,W,H

def p25(src):
    page=make_page()
    scene(page,src,(398,784,588,965),(30,30,994,399),focus=(.55,.53),dim=.16)
    d=ImageDraw.Draw(page)
    d.ellipse((815,275,839,306),fill='#b4a093',outline='#52606c',width=3)
    d.polygon([(807,303),(844,304),(858,367),(791,368)],fill='#212c38')
    d.line((809,360,804,383),fill='#182532',width=9)
    d.line((839,362,851,384),fill='#182532',width=9)
    scene(page,src,(398,245,621,425),(30,419,994,1121),focus=(.45,.44),dim=.09)
    d.rectangle((579,432,985,1105),fill='#3a4e59')
    balloon(page,(612,556,963,738),['今の人は？'],size=41)
    scene(page,src,(16,248,243,431),(30,1141,497,1506),focus=(.45,.5),dim=.08)
    scene(page,src,(399,249,623,422),(516,1141,994,1506),focus=(.4,.5),dim=.08)
    balloon(page,(52,1367,475,1480),['神谷さんの奥さん'],size=30)
    balloon(page,(541,1376,978,1492),['……大変だったな'],size=32)
    return page

def p26(src):
    page=make_page()
    scene(page,src,(16,251,243,429),(30,30,994,482),focus=(.42,.53),dim=.06)
    d=ImageDraw.Draw(page);d.rectangle((535,37,984,474),fill='#344857')
    balloon(page,(556,149,967,389),['夜の点検、','私も入れて'],size=37)
    scene(page,src,(399,249,623,425),(30,502,994,911),focus=(.44,.52),dim=.08)
    d.rectangle((534,509,984,905),fill='#465966')
    balloon(page,(553,607,969,796),['明日、','安全点検から'],size=35)
    scene(page,src,(398,785,591,967),(30,931,994,1506),focus=(.50,.54),dim=.33)
    scene(page,src,(20,249,244,431),(52,1021,502,1441),focus=(.49,.43),dim=.07)
    scene(page,src,(399,249,620,426),(518,1021,974,1441),focus=(.42,.47),dim=.07)
    balloon(page,(115,1358,485,1478),['いつもそれだ'],size=36)
    d.line((506,1082,507,1383),fill='#8e9d9e',width=6)
    return page

def main():
    src=Image.open(SRC).convert('RGB');assert src.size==(1536,1024)
    dest=BASE/'revision-manifest.json';manifest=json.loads(dest.read_text(encoding='utf-8')) if dest.exists() else {}
    source_sha=sha256(SRC.read_bytes()).hexdigest()
    for n,fn in ((25,p25),(26,p26)):
        image=fn(src);assert image.size==(W,H)
        f=BASE/f'p{n:02d}_v01.png';image.save(f,optimize=True)
        raw=f.read_bytes();assert raw[:8]==b'\x89PNG\r\n\x1a\n'
        manifest[f.name]={'page':n,'status':'candidate-needs-visual-review','width':W,'height':H,'bytes':len(raw),'sha256':sha256(raw).hexdigest(),'source':{'sources/p17_p20_generated_montage.png':source_sha},'notes':'Kuzumi is composed as an ordinary senior worker, not a villain. Clothes and friendly smile still need final repaint.'}
        print(f.name,len(raw),manifest[f.name]['sha256'])
    dest.write_text(json.dumps(manifest,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')

if __name__=='__main__':main()
