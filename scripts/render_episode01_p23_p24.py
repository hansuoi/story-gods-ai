#!/usr/bin/env python3
"""Reproducible color review candidates P23/P24; no final acceptance."""
from hashlib import sha256
import json
from PIL import Image, ImageDraw
from render_episode01_p17_p18 import BASE, SRC, make_page, scene, gradient_panel, balloon, FRAME, W, H, font

def flood_gauge(page,src,region):
    x0,y0,x1,y1=region
    # Tight crop omits the source collage's AI-generated text area.
    scene(page,src,(389,783,589,967),region,focus=(.50,.45),dim=.27)
    d=ImageDraw.Draw(page)
    gx=x0+145;top=y0+25;bottom=y1-27
    d.rounded_rectangle((gx-30,top,gx+34,bottom),radius=6,fill='#dadcd5',outline='#667577',width=7)
    for i in range(1,8):
        y=top+30+i*52
        d.line((gx-17,y,gx+31,y),fill='#334a56',width=5)
        if i in (1,3,5,7):
            d.text((gx-12,y-41),str(8-i),font=font(29),fill='#344a55')
    d.line((x0+40,y0+int((y1-y0)*.79),x1-28,y0+int((y1-y0)*.71)),fill='#b1d3db',width=8)

def p23(src):
    page=make_page()
    scene(page,src,(916,436,1140,598),(30,30,994,398),focus=(.48,.48),dim=.07)
    d=ImageDraw.Draw(page);d.rectangle((539,38,984,391),fill='#3e5059')
    balloon(page,(550,110,968,302),['昔からこの近くに？'],size=35)
    flood_gauge(page,src,(30,418,994,1022))
    balloon(page,(466,785,968,971),['あの雨の日、','母もここにいました'],size=32)
    scene(page,src,(920,442,1139,596),(30,1042,503,1506),focus=(.48,.38),dim=.10)
    balloon(page,(73,1351,465,1474),['ごめんなさい'],size=34)
    scene(page,src,(13,250,247,430),(523,1042,994,1506),focus=(.5,.37),dim=.10)
    balloon(page,(544,1291,978,1476),['謝るの、安希さんじゃ','ないでしょ'],size=30)
    return page

def p24(src):
    page=make_page()
    scene(page,src,(916,438,1139,597),(30,30,994,344),focus=(.48,.46),dim=.07)
    d=ImageDraw.Draw(page);d.rectangle((518,39,983,337),fill='#43515b')
    balloon(page,(536,93,967,275),['話してくれて、','ありがとう'],size=37)
    scene(page,src,(27,446,207,566),(30,364,994,680),focus=(.5,.40),dim=.08)
    scene(page,src,(11,447,247,601),(30,700,994,1116),focus=(.5,.53),dim=.08)
    d=ImageDraw.Draw(page)
    d.rounded_rectangle((392,941,686,1086),radius=5,fill='#f4f0e4',outline='#859594',width=5)
    d.text((417,984),'神谷探偵事務所',font=font(25),fill='#29353b')
    balloon(page,(546,758,969,928),['探偵さん、','もういないのに？'],size=33)
    gradient_panel(page,(30,1136,994,1506),top=(79,88,94),bottom=(33,43,53))
    card=Image.new('RGBA',(615,215),(0,0,0,0));cd=ImageDraw.Draw(card)
    cd.rounded_rectangle((9,9,600,205),radius=10,fill=(248,246,238,255),outline=(157,165,160,255),width=8)
    cd.text((53,63),'神谷探偵事務所',font=font(47),fill='#28343b')
    cd.line((53,132,548,132),fill='#b1b7ae',width=4)
    cd.text((57,157),'KAMIYA DETECTIVE OFFICE',font=font(19),fill='#5c686d')
    card=card.rotate(7,expand=True,resample=Image.Resampling.BICUBIC)
    page.paste(card,(64,1199),card)
    balloon(page,(625,1200,968,1401),['受付は、','まだいます'],size=35)
    return page

def main():
    src=Image.open(SRC).convert('RGB'); assert src.size==(1536,1024)
    dest=BASE/'revision-manifest.json'
    manifest=json.loads(dest.read_text(encoding='utf-8')) if dest.exists() else {}
    source_sha=sha256(SRC.read_bytes()).hexdigest()
    for n,fun in ((23,p23),(24,p24)):
        image=fun(src);assert image.size==(W,H)
        output=BASE/f'p{n:02d}_v01.png';image.save(output,optimize=True)
        raw=output.read_bytes();assert raw[:8]==b'\x89PNG\r\n\x1a\n'
        manifest[output.name]={'page':n,'status':'candidate-needs-visual-review',
           'width':W,'height':H,'bytes':len(raw),'sha256':sha256(raw).hexdigest(),
           'source':{'sources/p17_p20_generated_montage.png':source_sha},
           'notes':'P23/P24 painterly fragments, flood gauge and detective-office card composed with exact Japanese lettering; final art still needs character/hand consistency review.'}
        print(output.name,len(raw),manifest[output.name]['sha256'])
    dest.write_text(json.dumps(manifest,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')

if __name__=='__main__':main()
