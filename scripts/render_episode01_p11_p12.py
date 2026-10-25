#!/usr/bin/env python3
"""Compose P11/P12 color review candidates from the P09–12 AI source montage.

Keep exact Japanese name lettering separate from AI-generated explanatory text.
Neither page counts as accepted finished art without a visual continuity review.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter

from render_episode01_p09_p10 import balloon, draw_panel, new_page, SOURCE, BASE, PAGESIZE, FONT_FILE


def text_center(draw, txt, x, y, font, fill='#222c31'):
    box=draw.textbbox((0,0),txt,font=font)
    draw.text((x-(box[2]-box[0])/2,y),txt,font=font,fill=fill)


def shade_shirt(canvas, src):
    """Use actual AI-painted blouse textile as fabric for the abandoned shirt."""
    x0,y0=352,321
    w,h=320,246
    fabric=src.crop((786,218,909,327)).convert('RGB')
    fabric=ImageOps.fit(fabric,(w,h),Image.Resampling.LANCZOS)
    # No invented skin or graphic text in the cloth crop. Soften fabric folds.
    mask=Image.new('L',(w,h),0)
    m=ImageDraw.Draw(mask)
    m.polygon([(79,30),(124,16),(166,28),(207,8),(241,28),(285,75),(318,112),(275,143),(245,100),(239,244),(81,244),(75,101),(39,146),(4,118),(24,72)],fill=245)
    mask=mask.filter(ImageFilter.GaussianBlur(2))
    canvas.paste(fabric,(x0,y0),mask)
    d=ImageDraw.Draw(canvas)
    # collar, placket and natural material creases kept visually light
    d.line([(477,344),(519,397),(555,340)],fill='#d5dedf',width=8)
    d.line([(517,399),(516,560)],fill='#98a7a7',width=4)
    d.line([(432,414),(438,555)],fill='#8d9f9e',width=3)
    d.line([(595,415),(600,554)],fill='#8f9e9f',width=3)
    for cx,cy in [(518,444),(517,489),(516,526)]:
        d.ellipse((cx-2,cy-2,cx+2,cy+2),fill='#91a3a3')


def make_p11(src):
    canvas=new_page()
    # Old office: empty chair first; avoid all AI's incorrect captions.
    empty=src.crop((390,12,766,265)).convert('RGB')
    draw_panel(canvas,empty,(31,30,993,580))
    # The generated picture puts an incorrect narration box in the upper left.
    # Replace that region with the office's dark file shelves before layering shirt.
    d=ImageDraw.Draw(canvas)
    d.rectangle((59,124,427,338),fill='#26333f')
    for y in (184,257,333):
        d.line((70,y,426,y),fill='#66717a',width=6)
    for i in range(13):
        xx=79+i*27
        height=49+(i%3)*7
        d.rounded_rectangle((xx,182-height,xx+20,180),radius=2,fill=('#4b5a64' if i%3 else '#7b7b78'),outline='#27303b',width=2)
    shade_shirt(canvas,src)
    d=ImageDraw.Draw(canvas)
    title=ImageFont.truetype(FONT_FILE,31)
    d.rounded_rectangle((60,54,392,112),radius=12,fill='#e9e5db',outline='#5f6667',width=3)
    text_center(d,'神谷探偵事務所',226,64,title)
    # Notebook and hands: no overlay text on Aki's action.
    work=src.crop((780,178,1123,405)).convert('RGB')
    draw_panel(canvas,work,(31,600,993,1220))
    # Final partial panel: calculator and a finger paused above the next key.
    desk=src.crop((823,300,1126,410)).convert('RGB')
    draw_panel(canvas,desk,(31,1240,993,1506))
    d=ImageDraw.Draw(canvas)
    d.rounded_rectangle((440,1253,866,1490),radius=23,fill='#34414b',outline='#1e2831',width=7)
    d.rounded_rectangle((465,1264,842,1318),radius=7,fill='#b6c7be',outline='#617470',width=4)
    fnum=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',28)
    d.text((703,1274),'0000',font=fnum,fill='#354b45')
    for row in range(3):
        for col in range(4):
            x=468+col*92; y=1333+row*48
            d.rounded_rectangle((x,y,x+78,y+37),radius=6,fill='#a7b2b0',outline='#42515a',width=2)
    finger=Image.new('RGBA',canvas.size,(0,0,0,0))
    f=ImageDraw.Draw(finger)
    f.line([(901,1458),(859,1410),(797,1397)],fill=(196,147,125,252),width=31,joint='curve')
    f.ellipse((781,1383,811,1410),fill=(224,184,161,252))
    canvas.paste(finger,(0,0),finger)
    f=ImageFont.truetype(FONT_FILE,31)
    d.rounded_rectangle((64,1286,338,1365),radius=25,fill='#f6f3ea',outline='#2c3438',width=4)
    text_center(d,'カタ、カタ',201,1304,f)
    return canvas


def draw_schedule(canvas,box):
    x0,y0,x1,y1=box
    d=ImageDraw.Draw(canvas)
    d.polygon([(x0+18,y0),(x1-15,y0+11),(x1,y1),(x0,y1-14)],fill='#f1eada',outline='#999388',width=6)
    f=ImageFont.truetype(FONT_FILE,31)
    d.text((x0+52,y0+25),'予定表　10月',font=f,fill='#444c4b')
    for i,t in enumerate(['14:00','15:00','16:00','17:00','18:00','19:00']):
        yy=y0+93+i*48
        d.line((x0+37,yy,x1-45,yy),fill='#b9bcb3',width=3)
        d.text((x0+52,yy+5),t,font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18),fill='#66706c')
    d.line((x0+155,y0+95,x0+155,y1-33),fill='#adb6b2',width=2)
    # Afternoon ends empty; absence of appointments is the clue.
    d.text((x0+184,y0+110),'調整',font=ImageFont.truetype(FONT_FILE,24),fill='#77827c')


def make_p12(src):
    canvas=new_page()
    # Afternoon entries end abruptly; the vacant evening is the clue.
    desk=src.crop((784,156,1135,408)).convert('RGB')
    draw_panel(canvas,desk,(31,30,993,459))
    draw_schedule(canvas,(73,45,620,443))
    balloon(canvas,(631,109,966,279),['本当に','休みだった？'],fontsize=37)
    # Keep the real-looking taxi receipt and map. Remove invented AI captions.
    receipt=src.crop((1160,5,1529,150)).convert('RGB')
    draw_panel(canvas,receipt,(31,480,993,890))
    # Explicitly identify the information we may conclude, no invented dates.
    d=ImageDraw.Draw(canvas)
    d.rounded_rectangle((591,782,957,867),radius=16,fill='#fcfaf4',outline='#5d6261',width=4)
    text_center(d,'汀橋方面の交通費',774,803,ImageFont.truetype(FONT_FILE,29))
    # Two receipts overlap but clock-times are intentionally not guessed.
    d.rectangle((31,910,993,1099),fill='#746c61',outline='#1e292e',width=5)
    for xo,yo,ang in [(105,934,-8),(478,930,6)]:
        label=Image.new('RGBA',(365,143),(248,246,235,255))
        g=ImageDraw.Draw(label)
        g.rectangle((2,2,361,139),outline='#9c9b95',width=3)
        g.text((22,12),'タクシー領収書',font=ImageFont.truetype(FONT_FILE,25),fill='#4d5a58')
        g.line((25,60,341,60),fill='#bac1bb',width=3)
        g.text((26,67),'汀橋方面',font=ImageFont.truetype(FONT_FILE,27),fill='#404b4b')
        g.line((25,112,341,112),fill='#bac1bb',width=3)
        rotated=label.rotate(ang,expand=True,resample=Image.Resampling.BICUBIC)
        canvas.paste(rotated,(xo,yo),rotated)
    # Aki, side profile, reasoning, inside office rather than at the scene already.
    face=src.crop((772,419,1022,588)).convert('RGB')
    draw_panel(canvas,face,(31,1119,993,1506))
    balloon(canvas,(491,1227,967,1461),['仕事もないのに、','なんで……'],fontsize=44)
    return canvas


def main():
    src=Image.open(SOURCE).convert('RGB')
    assert src.size==(1536,1024)
    manifest_path=BASE/'revision-manifest.json'
    manifest=json.loads(manifest_path.read_text(encoding='utf-8')) if manifest_path.exists() else {}
    for n,render in [(11,make_p11),(12,make_p12)]:
        result=render(src)
        assert result.size==PAGESIZE
        target=BASE/f'p{n:02d}_v01.png'
        result.save(target,optimize=True)
        raw=target.read_bytes()
        assert raw.startswith(b'\x89PNG\r\n\x1a\n')
        manifest[target.name]={
            'page':n,'status':'candidate-needs-visual-review','bytes':len(raw),'width':1024,'height':1536,
            'sha256':hashlib.sha256(raw).hexdigest(),
            'source':{'sources/p09_p12_generated_montage.png':hashlib.sha256(SOURCE.read_bytes()).hexdigest()},
            'notes':'P11 or P12 photo-collage composition, hand-typeset Japanese and diagram elements; visual review required.'
        }
        print(str(target),len(raw),manifest[target.name]['sha256'])
    manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')

if __name__=='__main__':main()