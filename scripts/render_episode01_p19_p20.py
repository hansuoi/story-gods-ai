#!/usr/bin/env python3
"""Two color *review candidates* for P19–P20 with a shared hinge evidence image.

The AI source montage incorrectly contains a loose bent rod and invented evidence.
It is not presented as a literal scene: the photo is a separately composed
crooked hinge, identically reused in both pages, with exact Japanese lettering.
Not accepted as final artwork or forensic evidence. Character art still needs
repaint to meet the episode's design sheet.
"""
from __future__ import annotations
from pathlib import Path
from hashlib import sha256
from PIL import Image,ImageDraw,ImageOps,ImageEnhance,ImageFilter
import json
from render_episode01_p17_p18 import BASE,SRC,make_page,scene,gradient_panel,balloon,pin,FRAME,W,H

PHOTO=BASE/'sources/p19_p20_hinge_photo.png'
SOURCE_NAME='sources/p17_p20_generated_montage.png'


def build_photo(src):
    # The source provides rainy concrete, metal, and a scale/ruler only. The
    # hinges themselves are composed carefully to make the deformation clear.
    base=ImageOps.fit(src.crop((912,256,1137,421)),(640,790),Image.Resampling.LANCZOS,centering=(.48,.55))
    base=ImageEnhance.Color(base).enhance(.52)
    base=ImageEnhance.Contrast(base).enhance(.94)
    tint=Image.new('RGB',base.size,'#2e5364');base=Image.blend(base,tint,.29)
    overlay=Image.new('RGBA',base.size,(0,0,0,0));d=ImageDraw.Draw(overlay)
    # Cast shadow behind both plates and the steel barrel.
    d.rounded_rectangle((139,73,295,716),radius=16,fill=(15,27,36,171),outline=(27,38,44,200),width=6)
    d.rounded_rectangle((346,62,508,706),radius=15,fill=(14,26,34,185),outline=(29,40,46,218),width=7)
    # Riveted iron plates under grazing wet light.
    d.polygon([(129,68),(290,58),(309,710),(151,724)],fill=(121,143,153,246))
    d.line([(142,75),(280,68),(298,694)],fill=(208,218,218,241),width=12)
    d.line([(169,112),(281,105)],fill=(67,85,95,234),width=12)
    d.polygon([(352,63),(500,55),(522,704),(361,708)],fill=(86,111,122,248))
    d.line([(365,77),(489,68),(508,689)],fill=(195,208,211,233),width=10)
    # Lower and upper hinge knuckles, with a crucial bent barrel in the middle.
    for box in [(274,109,377,264),(286,494,388,660)]:
        d.rounded_rectangle(box,radius=14,fill=(162,179,184,253),outline=(34,55,66,248),width=9)
    d.polygon([(292,262),(363,244),(379,364),(347,393),(379,477),(310,491),(288,376),(316,351)],fill=(112,133,141,253))
    d.line([(317,257),(354,254),(367,351),(341,390),(368,473)],fill=(210,225,225,244),width=12,joint='curve')
    d.line([(303,261),(314,356),(298,376),(312,489)],fill=(32,51,62,243),width=7)
    # Crack is irregular, only within narrow damaged hinge area.
    crack=[(316,319),(300,333),(324,350),(304,379),(339,395),(314,424),(348,446)]
    d.line(crack,fill=(18,31,40,255),width=13,joint='curve')
    d.line(crack,fill=(177,216,222,228),width=3,joint='curve')
    # Blue-white preserving outline, not an explosion or blanket time reversal.
    d.arc((263,267,400,482),start=70,end=286,fill=(202,236,238,240),width=6)
    d.arc((257,262,415,493),start=65,end=286,fill=(62,166,203,180),width=3)
    for cx,cy in [(203,142),(210,621),(444,132),(457,625)]:
        d.ellipse((cx-13,cy-13,cx+13,cy+13),fill=(34,49,56,255),outline=(198,213,215,244),width=5)
        d.line([(cx-5,cy-5),(cx+5,cy+5)],fill=(139,166,168,245),width=3)
    # Surface rain streaks emphasize a genuine photographed texture.
    for x,y in [(91,110),(118,534),(541,256),(564,587)]:
        d.line([(x,y),(x+7,y+82)],fill=(212,235,238,65),width=3)
    base=Image.alpha_composite(base.convert('RGBA'),overlay).convert('RGB')
    base.save(PHOTO,optimize=True)
    return base


def phone_insert(page,photo,region):
    x0,y0,x1,y1=region
    d=ImageDraw.Draw(page)
    d.rounded_rectangle(region,radius=36,fill='#101923',outline='#0b1219',width=12)
    inset=(x0+24,y0+72,x1-24,y1-66)
    art=ImageOps.fit(photo,(inset[2]-inset[0],inset[3]-inset[1]),Image.Resampling.LANCZOS)
    page.paste(art,inset[:2])
    d.rectangle((inset[0],inset[1],inset[2]-1,inset[3]-1),outline='#4a606c',width=4)
    # Time comes from the previously established candidate photo; a visual
    # placeholder pending story fact-check, not independently corroborated.
    d.text((x0+33,y0+25),'17:42',fill='#eef3ee',font=__import__('render_episode01_p17_p18').font(30))
    d.text((x0+100,y1-55),'IMG_1742',fill='#c9d7d9',font=__import__('render_episode01_p17_p18').font(23))
    d.ellipse((x0+(x1-x0)//2-7,y1-40,x0+(x1-x0)//2+7,y1-26),fill='#7f979b')


def p19(src,photo):
    page=make_page()
    gradient_panel(page,(30,30,994,960),top=(95,105,111),bottom=(30,41,55))
    scene(page,src,(386,789,624,968),(34,36,989,954),focus=(.5,.5),dim=.52)
    phone_insert(page,photo,(190,75,825,921))
    ImageDraw.Draw(page).rectangle((30,30,993,959),outline=FRAME,width=7)
    # Aki recognizes the site once fitted with a replacement part.
    scene(page,src,(916,437,1141,597),(30,982,994,1225),focus=(.48,.47),dim=.09)
    d=ImageDraw.Draw(page);d.rectangle((548,990,985,1217),fill='#3e4a52')
    balloon(page,(561,1041,968,1173),['今は直ってた'],size=41)
    # Nagi states only the narrow ten-minute effect.
    scene(page,src,(13,250,247,434),(30,1246,994,1506),focus=(.40,.5),dim=.09)
    d.rectangle((540,1253,985,1499),fill='#3b4851')
    balloon(page,(552,1280,968,1450),['十分だけ、','直るのを止めました'],size=32)
    return page


def p20(src,photo):
    page=make_page()
    # Close detail of the pin. It is the object's name, not a power tutorial.
    scene(page,src,(67,509,237,599),(30,30,994,300),focus=(.46,.5),dim=.20)
    pin(page,169,55,.96)
    balloon(page,(568,90,955,224),['留め針'],size=49)
    # The exact same hinge photo is reused verbatim, not an alternative angle.
    gradient_panel(page,(30,320,994,898),top=(90,105,112),bottom=(34,44,57))
    d=ImageDraw.Draw(page)
    inset=(98,341,552,864)
    art=ImageOps.fit(photo,(inset[2]-inset[0],inset[3]-inset[1]),Image.Resampling.LANCZOS)
    page.paste(art,inset[:2])
    d.rectangle((inset[0],inset[1],inset[2]-1,inset[3]-1),outline='#d4dbd7',width=8)
    # Visual mark of the localized deformation; ensure the photo remains legible.
    d.arc((255,499,469,724),start=20,end=330,fill='#bee8e9',width=7)
    balloon(page,(555,473,962,742),['一箇所だけ。','十分だけ'],size=39)
    # Aki's question hangs in the room; no invented definitive answer.
    scene(page,src,(916,437,1141,597),(30,918,994,1275),focus=(.45,.5),dim=.12)
    d.rectangle((524,926,985,1268),fill='#394957')
    balloon(page,(542,967,963,1206),['榊の身体も……','こうやって','戻ったの？'],size=33)
    # Silent pin grip. It is still a provisional hand pose to repaint.
    scene(page,src,(66,506,237,597),(30,1295,994,1506),focus=(.45,.51),dim=.22)
    pin(page,437,1321,.52)
    ImageDraw.Draw(page).rectangle((30,1295,993,1505),outline=FRAME,width=7)
    return page


def main():
    src=Image.open(SRC).convert('RGB');assert src.size==(1536,1024)
    photo=build_photo(src);raw_photo=PHOTO.read_bytes(); assert photo.size==(640,790)
    photo_sha=sha256(raw_photo).hexdigest();source_sha=sha256(SRC.read_bytes()).hexdigest()
    path=BASE/'revision-manifest.json';manifest=json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}
    for n,fun in ((19,p19),(20,p20)):
        im=fun(src,photo);assert im.size==(W,H)
        out=BASE/f'p{n:02d}_v01.png';im.save(out,optimize=True)
        b=out.read_bytes(); assert b[:8]==b'\x89PNG\r\n\x1a\n'
        manifest[out.name]={
           'page':n,'width':W,'height':H,'bytes':len(b),'sha256':sha256(b).hexdigest(),
           'status':'candidate-needs-visual-review',
           'source':{SOURCE_NAME:source_sha,'sources/p19_p20_hinge_photo.png':photo_sha},
           'notes':'Painterly montage fragments, same composited hinge photograph on P19/P20, correct independent Japanese lettering; the photo is illustrated, not actual forensic evidence.'}
        print(out.name,len(b),manifest[out.name]['sha256'])
    path.write_text(json.dumps(manifest,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')
    print('Evidence photo',PHOTO.name,len(raw_photo),photo_sha)

if __name__=='__main__':main()