#!/usr/bin/env python3
"""P29–P32: casebook identity reveal and anonymous call. Color review candidates.
Keep the P30 'client' reveal separate from the P31 'target' page-turn reveal.
"""
from hashlib import sha256
import json
from PIL import Image,ImageDraw,ImageOps
from render_episode01_p17_p18 import BASE,SRC,make_page,scene,gradient_panel,balloon,FRAME,W,H,font
OLD=BASE/'sources/p13_p16_generated_montage.png'
PORTRAIT=BASE/'sources/sakaki_living_portrait.png'

def paper(page,box,color='#eee8db',border='#8a938d'):
    d=ImageDraw.Draw(page)
    d.rounded_rectangle(box,radius=9,fill=color,outline=border,width=8)
    return d

def p29(src,old):
    page=make_page();d=ImageDraw.Draw(page)
    scene(page,old,(26,11,188,115),(30,30,994,387),focus=(.55,.49),dim=.08)
    d.rounded_rectangle((176,76,839,336),radius=10,fill='#cdbb9f',outline='#806d5d',width=9)
    d.line((181,81,499,236,837,81),fill='#a98e75',width=6)
    d.text((314,207),'本人へ返却',font=font(58),fill='#464443')
    scene(page,old,(11,268,375,509),(30,407,994,855),focus=(.52,.50),dim=.12)
    paper(page,(66,454,481,827))
    paper(page,(519,453,960,823))
    for x in (77,530):
        for y in (583,654,725,780):d.line((x+22,y,x+375,y),fill='#b5b9b1',width=4)
    d.text((132,528),'保留',font=font(54),fill='#666662')
    d.text((637,528),'榊',font=font(54),fill='#666662')
    scene(page,old,(15,0,368,224),(30,875,994,1506),focus=(.55,.52),dim=.32)
    paper(page,(226,937,786,1460),color='#d7d5c9')
    paper(page,(253,967,750,1431),color='#e9e7d9')
    d.polygon([(747,1428),(752,1248),(681,1309),(683,1428)],fill='#f5efe2')
    return page

def p30(src,old):
    page=make_page();d=ImageDraw.Draw(page)
    scene(page,old,(24,5,369,217),(30,30,994,863),focus=(.49,.48),dim=.35)
    paper(page,(145,94,869,821),color='#ebe8de')
    d.text((275,189),'汀橋水害・再調査',font=font(52),fill='#2b3539')
    d.line((230,294,782,294),fill='#a8b1a7',width=6)
    d.text((251,427),'依頼者：神谷榊',font=font(58),fill='#25353b')
    d.line((221,491,783,491),fill='#b4bcb2',width=4)
    d.rounded_rectangle((223,596,786,751),radius=7,fill='#d9d9cf',outline='#abb3aa',width=4)
    scene(page,src,(917,436,1139,596),(30,883,994,1279),focus=(.43,.49),dim=.10)
    d.rectangle((532,891,985,1271),fill='#44535c')
    balloon(page,(553,979,970,1177),['自分で、自分に','依頼？'],size=38)
    scene(page,old,(17,259,371,501),(30,1299,994,1506),focus=(.42,.48),dim=.35)
    d.rounded_rectangle((257,1318,765,1495),radius=4,fill='#f0eee5',outline='#929b95',width=6)
    return page

def p31(src,old,portrait):
    page=make_page();d=ImageDraw.Draw(page)
    scene(page,old,(24,5,369,217),(30,30,994,796),focus=(.49,.48),dim=.35)
    paper(page,(143,76,871,763),color='#eeeade')
    d.text((255,152),'汀橋水害・再調査',font=font(52),fill='#39484d')
    d.line((218,262,789,262),fill='#a7b1a9',width=6)
    d.text((228,355),'依頼者：神谷榊',font=font(38),fill='#536163')
    d.line((218,405,790,405),fill='#b1b6b0',width=4)
    d.rounded_rectangle((194,474,814,660),radius=10,fill='#e2e0d5',outline='#8e9b95',width=5)
    d.text((209,546),'調査対象：神谷榊',font=font(58),fill='#23343a')
    scene(page,src,(396,781,588,963),(30,815,994,1258),dim=.46)
    # The photographed Sakaki is alive, smiling at the office. Using the P06
    # coffin crop here turned an office photograph into a photo of the body.
    # The reference crop is taken INSIDE a framed living portrait, avoiding
    # its funeral-frame border and most flowers. Aki's hand shadows its right half.
    photo=ImageOps.fit(portrait.crop((76,35,265,285)),(567,392),Image.Resampling.LANCZOS)
    page.paste(photo,(227,843))
    shadow=Image.new('RGBA',page.size,(0,0,0,0))
    sd=ImageDraw.Draw(shadow)
    sd.polygon([(555,839),(806,835),(803,1243),(483,1245),(548,1140)],
               fill=(20,25,31,143))
    page=Image.alpha_composite(page.convert('RGBA'),shadow).convert('RGB')
    d=ImageDraw.Draw(page)
    d.rectangle((219,835,803,1247),outline='#bfc9c6',width=10)
    gradient_panel(page,(30,1278,994,1506),top=(92,98,101),bottom=(44,54,60))
    paper(page,(100,1298,594,1493),color='#e8e5db')
    for y in (1323,1385,1443):d.ellipse((119,y,141,y+23),fill='#5e7177')
    d.line((165,1339,543,1339),fill='#b9c2ba',width=5)
    balloon(page,(618,1340,970,1470),['一枚、ない……'],size=32)
    return page

def p32(src,old):
    page=make_page();d=ImageDraw.Draw(page)
    gradient_panel(page,(30,30,994,276),top=(118,126,127),bottom=(41,54,64))
    d.rounded_rectangle((300,53,786,250),radius=32,fill='#111b24',outline='#30454e',width=12)
    d.rounded_rectangle((349,90,735,184),radius=7,fill='#c2ccc1',outline='#52656b',width=5)
    d.text((456,117),'非通知',font=font(49),fill='#273b44')
    scene(page,old,(22,6,320,222),(30,297,994,623),focus=(.49,.51),dim=.38)
    d.rounded_rectangle((581,344,832,531),radius=14,fill='#26343b',outline='#141f29',width=8)
    d.arc((620,366,798,496),start=205,end=333,fill='#c0cdc9',width=15)
    scene(page,src,(917,438,1139,597),(30,644,994,995),focus=(.49,.46),dim=.09)
    d.rectangle((513,651,985,988),fill='#3b4c56')
    balloon(page,(535,729,968,938),['はい。','神谷探偵事務所です'],size=34)
    # The last panel must not repeat the same face crop as the preceding
    # "Hello, Kamiya Detective Office" panel. Use the separate low-angle,
    # side-lit Aki profile with visible grief, preserving fear as well as will.
    scene(page,src,(1285,790,1495,959),(30,1015,994,1506),focus=(.52,.53),dim=.05)
    d.rectangle((522,1023,985,1497),fill='#354854')
    balloon(page,(539,1161,968,1408),['夫のことなら、','私が聞きます'],size=38)
    d.text((812,1455),'第1話終',font=font(25),fill='#dbe3e0')
    return page

def main():
    src=Image.open(SRC).convert('RGB')
    old=Image.open(OLD).convert('RGB')
    portrait=Image.open(PORTRAIT).convert('RGB')
    assert src.size==(1536,1024) and old.size==(1536,1024) and portrait.size==(285,340)
    dest=BASE/'revision-manifest.json'
    manifest=json.loads(dest.read_text(encoding='utf-8')) if dest.exists() else {}
    common={'sources/p17_p20_generated_montage.png':sha256(SRC.read_bytes()).hexdigest(),'sources/p13_p16_generated_montage.png':sha256(OLD.read_bytes()).hexdigest()}
    for n,page in ((29,p29(src,old)),(30,p30(src,old)),(31,p31(src,old,portrait)),(32,p32(src,old))):
        assert page.size==(W,H)
        file=BASE/f'p{n:02d}_v01.png'
        page.save(file,optimize=True)
        data=file.read_bytes();assert data[:8]==b'\x89PNG\r\n\x1a\n'
        sources=dict(common)
        if n==31:sources['sources/sakaki_living_portrait.png']=sha256(PORTRAIT.read_bytes()).hexdigest()
        manifest[file.name]={'page':n,'status':'candidate-needs-visual-review','width':W,'height':H,'bytes':len(data),'sha256':sha256(data).hexdigest(),'source':sources,'notes':'P29–P32 casebook reveal and anonymous call; correct dialogue and page-turn timing, P31 office portrait is Sakaki alive; P32 final profile crop centered on the tearful eye of Aki and mouth (not her ear), different from earlier answering crop; hand/receiver pose still needs repaint.'}
        print(file.name,len(data),manifest[file.name]['sha256'])
    dest.write_text(json.dumps(manifest,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')

if __name__=='__main__':main()
