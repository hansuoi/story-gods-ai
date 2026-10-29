#!/usr/bin/env python3
"""Color P27/P28 storyboards with a vacant train seat and paired ledgers.
All page artwork is a review candidate, not an accepted final manga page.
"""
from hashlib import sha256
from PIL import Image,ImageDraw,ImageOps,ImageFilter
import json
from render_episode01_p17_p18 import BASE,SRC,make_page,scene,gradient_panel,balloon,FRAME,W,H,font
from render_episode01_p19_p20 import PHOTO

OLD=BASE/'sources/p13_p16_generated_montage.png'
EARLY=BASE/'sources/p09_p12_generated_montage.png'
P06=BASE/'p06_v03.png'

def p27(src,photo,sakaki):
    page=make_page();d=ImageDraw.Draw(page)
    gradient_panel(page,(30,30,994,680),top=(161,169,171),bottom=(53,70,84))
    window=ImageOps.fit(src.crop((396,787,588,967)),(810,380),Image.Resampling.LANCZOS)
    page.paste(window,(105,72))
    d.rounded_rectangle((83,55,928,469),radius=22,outline='#c4c7c4',width=24)
    d.line((494,61,494,458),fill='#b9c1bc',width=19)
    # Two independent seat backs, deliberately unequal: Aki occupies the
    # left; the right cushion remains fully visible and empty.
    d.rounded_rectangle((61,436,958,645),radius=23,fill='#234156',outline='#162e42',width=12)
    d.rounded_rectangle((93,451,488,631),radius=21,fill='#34586e',outline='#6c8997',width=7)
    d.rounded_rectangle((516,451,926,631),radius=21,fill='#476e80',outline='#8fa5aa',width=7)
    d.line((518,546,926,546),fill='#6b899a',width=5)
    d.line((545,623,901,623),fill='#1f3b51',width=8)
    d.line((501,455,501,635),fill='#172e40',width=12)
    for x in (288,701):
        d.line((x,40,x,236),fill='#a8b3b5',width=9)
        d.ellipse((x-28,200,x+28,261),outline='#d9dcd5',width=11)
    aki=ImageOps.fit(src.crop((914,434,1138,597)),(305,297),Image.Resampling.LANCZOS,centering=(.45,.45))
    mask=Image.new('L',aki.size,0)
    ImageDraw.Draw(mask).ellipse((16,5,aki.width-15,aki.height-2),fill=255)
    # Keep her face attached to the jacket and seat, not floating in the window.
    page.paste(aki,(130,259),mask.filter(ImageFilter.GaussianBlur(9)))
    d.polygon([(93,644),(104,543),(170,496),(235,508),(294,502),
               (398,506),(464,560),(480,644)],fill='#202b39')
    d.line((180,509,251,628),fill='#576876',width=8)
    d.line((284,510,252,626),fill='#73818a',width=5)
    d.line((238,524,276,631),fill='#6c7178',width=7)
    d.line((295,524,277,637),fill='#424b59',width=5)
    d.rectangle((30,30,993,679),outline=FRAME,width=7)
    scene(page,src,(396,786,590,964),(30,701,994,1040),dim=.40)
    left=ImageOps.fit(photo,(453,300),Image.Resampling.LANCZOS)
    right=ImageOps.fit(sakaki.crop((55,35,974,545)),(453,300),Image.Resampling.LANCZOS)
    page.paste(left,(54,719));page.paste(right,(523,719))
    d.rectangle((54,719,507,1019),outline='#dbe3df',width=6)
    d.rectangle((523,719,976,1019),outline='#dbe3df',width=6)
    scene(page,src,(781,787,937,973),(30,1060,994,1506),focus=(.43,.55),dim=.20)
    d.polygon([(52,1220),(404,1180),(460,1491),(52,1497)],fill='#e8e4d8')
    for y in (1260,1320,1380,1440):d.line((98,y,415,y-24),fill='#b6bab0',width=4)
    balloon(page,(471,1174,972,1463),['直せたものも、','戻らない人も、','ここにいる'],size=32)
    return page

def p28(src,old,early):
    page=make_page();d=ImageDraw.Draw(page)
    scene(page,early,(11,9,258,242),(30,30,994,420),focus=(.44,.52),dim=.12)
    d.rounded_rectangle((204,241,288,326),radius=9,fill='#687177',outline='#2b373e',width=7)
    d.ellipse((223,260,274,310),fill='#cab788',outline='#5f6264',width=6)
    d.ellipse((239,274,258,293),fill='#505a5d')
    d.line((252,286,340,334),fill='#cbb78a',width=15)
    d.line((316,321,319,340),fill='#b59f77',width=12)
    scene(page,old,(12,9,372,244),(30,440,994,1003),focus=(.52,.49),dim=.20)
    d.rounded_rectangle((75,515,489,924),radius=12,fill='#eee9dc',outline='#8d9791',width=7)
    d.rounded_rectangle((525,510,959,929),radius=12,fill='#e8e4d8',outline='#8c9690',width=7)
    for x in (75,525):
        for y in (633,701,769,837):d.line((x+20,y,x+373,y),fill='#b9c2b8',width=4)
    d.text((112,565),'当日の経費',font=font(37),fill='#2b383f')
    d.text((558,563),'2018年／汀橋',font=font(37),fill='#2b383f')
    d.text((140,744),'18-07',font=font(51),fill='#3b4547')
    d.text((593,744),'18-07',font=font(51),fill='#3b4547')
    d.line((152,814,382,814),fill='#bc725f',width=7)
    d.line((605,815,840,815),fill='#bc725f',width=7)
    scene(page,old,(14,261,373,501),(30,1023,994,1506),focus=(.48,.50),dim=.24)
    d.rounded_rectangle((398,1147,571,1459),radius=5,fill='#a9ab9d',outline='#49585c',width=8)
    d.rounded_rectangle((428,1197,543,1396),radius=3,fill='#f0eddf',outline='#78867e',width=4)
    d.text((429,1262),'18-07',font=font(30),fill='#24353b')
    balloon(page,(614,1313,975,1449),['……これ？'],size=45)
    return page

def main():
    src=Image.open(SRC).convert('RGB');old=Image.open(OLD).convert('RGB')
    early=Image.open(EARLY).convert('RGB');photo=Image.open(PHOTO).convert('RGB')
    sakaki=Image.open(P06).convert('RGB')
    assert all(im.size==(1536,1024) for im in (src,old,early))
    assert photo.size==(640,790) and sakaki.size==(W,H)
    sources27={'sources/p17_p20_generated_montage.png':sha256(SRC.read_bytes()).hexdigest(),'sources/p19_p20_hinge_photo.png':sha256(PHOTO.read_bytes()).hexdigest(),'p06_v03.png':sha256(P06.read_bytes()).hexdigest()}
    sources28={'sources/p13_p16_generated_montage.png':sha256(OLD.read_bytes()).hexdigest(),'sources/p09_p12_generated_montage.png':sha256(EARLY.read_bytes()).hexdigest()}
    dest=BASE/'revision-manifest.json'
    manifest=json.loads(dest.read_text(encoding='utf-8')) if dest.exists() else {}
    for n,img,sources in ((27,p27(src,photo,sakaki),sources27),(28,p28(src,old,early),sources28)):
        f=BASE/f'p{n:02d}_v01.png';img.save(f,optimize=True)
        raw=f.read_bytes();assert img.size==(W,H) and raw[:8]==b'\x89PNG\r\n\x1a\n'
        manifest[f.name]={'page':n,'status':'candidate-needs-visual-review','width':W,'height':H,'bytes':len(raw),'sha256':sha256(raw).hexdigest(),'source':sources,'notes':'Train interior now shows Aki seated at left beside a visibly vacant right cushion; case-ledger candidate remains provisional and requires final character repaint.'}
        print(f.name,len(raw),manifest[f.name]['sha256'])
    dest.write_text(json.dumps(manifest,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')

if __name__=='__main__':main()
