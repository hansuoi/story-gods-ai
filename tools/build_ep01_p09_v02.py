#!/usr/bin/env python3
"""第1話P09 カラー原稿候補: 無文字原画と日本語文字レイヤーを独立生成。"""
from pathlib import Path
import hashlib, json, math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = Path(os.getenv('P09_OUTPUT_DIR', Path(__file__).parent / 'p09-build-v02'))
OUT.mkdir(parents=True, exist_ok=True)
W, H = 1400, 2100
rng = np.random.default_rng(2026101909)
fontpath = '/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc'

def panel(width, height, top, bottom):
    t = np.linspace(0, 1, height)[:, None, None]
    noise = rng.normal(0, 2.5, (height, width, 1))
    pixels = np.array(top)[None,None,:]*(1-t)+np.array(bottom)[None,None,:]*t+noise
    return Image.fromarray(np.uint8(np.clip(pixels,0,255)), 'RGB')

def polygon(draw, points, fill, outline=None, width=3):
    draw.polygon(points, fill=fill)
    if outline: draw.line(points+[points[0]], fill=outline, width=width, joint='curve')

def glow(img, center, radius, color, amount):
    pixels=np.asarray(img).astype('float32')
    yy,xx=np.ogrid[:img.height,:img.width]
    f=np.exp(-2*(((xx-center[0])/radius[0])**2+((yy-center[1])/radius[1])**2))[...,None]*amount
    return Image.fromarray(np.uint8(np.clip(pixels*(1-f)+np.array(color)*f,0,255)),'RGB')

# 1. 暗い玄関。靴棚の右半分は空。扉と床は同一の消失点を共有する。
a=panel(1304,1180,(28,36,46),(16,26,35)); d=ImageDraw.Draw(a)
polygon(d,[(0,0),(1304,0),(1304,590),(0,640)],(40,47,52))
polygon(d,[(790,0),(1170,0),(1140,635),(755,650)],(36,48,57),(14,21,29),7)
polygon(d,[(820,28),(1132,28),(1100,600),(807,610)],(58,69,76),(85,87,87),4)
d.ellipse((1030,326,1047,347),fill=(202,183,135))
polygon(d,[(0,595),(1304,575),(1304,1180),(0,1180)],(49,55,56))
for x in (-600,-100,350,800,1400,1900):d.line([(900,580),(x,1180)],fill=(92,92,88),width=3)
for y in (750,880,1040):d.line([(0,y+30),(1304,y-30)],fill=(95,93,86),width=3)
# The cabinet occupies the near left; shelves share one perspective.
polygon(d,[(88,280),(686,307),(686,1000),(88,1110)],(27,28,31),(12,14,17),8)
polygon(d,[(88,280),(686,307),(731,262),(144,235)],(82,70,62),(31,27,26),5)
polygon(d,[(686,307),(731,262),(727,947),(686,1000)],(19,23,27))
polygon(d,[(128,392),(634,414),(634,903),(130,986)],(13,18,24),(81,74,68),11)
polygon(d,[(159,423),(600,444),(600,874),(158,950)],(23,32,39))
polygon(d,[(149,644),(618,659),(617,698),(149,716)],(74,67,60),(21,23,24),3)
for x,y in [(233,561),(369,574)]:
    polygon(d,[(x-55,y+61),(x-42,y+1),(x+5,y-13),(x+50,y+21),(x+60,y+60)],(32,32,34),(119,104,88),3)
    d.line([(x-53,y+61),(x+60,y+60)],fill=(15,17,20),width=9)
# The vacant place is highlighted by reflected light, not explanatory arrows.
polygon(d,[(733,824),(1125,778),(1220,956),(821,1040)],(60,64,64))
d.arc((802,842,1022,974),30,160,fill=(95,96,90),width=2)
d.arc((982,824,1183,936),15,155,fill=(95,96,90),width=2)
d.line([(59,469),(66,856)],fill=(127,106,79),width=7)
d.arc((39,439,82,493),180,350,fill=(150,124,83),width=6)
a=glow(a,(1050,190),(550,650),(190,182,153),.22).filter(ImageFilter.GaussianBlur(.4))

# 2. Aki stops before finishing her habitual greeting.
b=panel(1304,300,(32,38,46),(18,25,35)); d=ImageDraw.Draw(b)
polygon(d,[(80,0),(610,0),(650,300),(120,300)],(48,52,53),(17,20,24),5)
for x in (133,624):d.line([(x,0),(x+8,300)],fill=(88,80,70),width=7)
polygon(d,[(904,300),(950,177),(1006,145),(1077,145),(1134,220),(1170,300)],(16,18,24),(8,11,14),5)
d.ellipse((1005,66,1100,191),fill=(141,112,96))
polygon(d,[(998,151),(1003,73),(1044,50),(1093,69),(1124,115),(1102,201),(1076,207),(1059,157),(1028,177)],(25,25,30))
d.arc((999,63,1114,207),10,135,fill=(79,69,66),width=4)
d.arc((930,167,1160,425),190,300,fill=(99,86,77),width=14)
b=glow(b,(300,140),(600,400),(142,128,105),.14)

# 3. Desk and Sakaki's handwritten expense note, hand at one corner.
c=panel(1304,395,(91,73,61),(46,39,37)); d=ImageDraw.Draw(c)
for i in range(13):
    y=i*35+int(rng.integers(-8,8));d.line([(0,y),(1304,y+int(rng.integers(-17,18)))],fill=(115,90,73),width=1)
polygon(d,[(146,66),(1103,35),(1194,326),(231,381)],(128,101,82),(49,38,34),5)
polygon(d,[(386,85),(872,59),(913,290),(431,329)],(214,197,133),(48,40,35),7)
polygon(d,[(381,80),(861,51),(902,279),(422,317)],(232,214,152),(146,132,94),3)
polygon(d,[(848,251),(903,280),(870,207)],(192,171,123),(126,111,82),2)
polygon(d,[(848,251),(882,240),(870,207)],(250,233,175))
polygon(d,[(1100,395),(1021,336),(952,281),(906,251),(893,230),(908,211),(932,222),(965,250),(951,221),(962,203),(985,210),(1013,245),(1005,209),(1027,201),(1047,221),(1091,292),(1159,333),(1249,395)],(191,150,126),(106,80,70),3)
polygon(d,[(1165,395),(1095,321),(1143,290),(1284,395)],(18,21,27),(7,10,14),3)
for line in [[(906,220),(924,231)],[(963,211),(979,226)],[(1026,210),(1042,227)]]:d.line(line,fill=(239,190,161),width=3)
c=glow(c,(640,125),(600,380),(235,204,166),.1)

page=Image.new('RGB',(W,H),(247,245,240)); d=ImageDraw.Draw(page)
for im,x,y in [(a,48,48),(b,48,1257),(c,48,1612)]:
    page.paste(im,(x,y));d.rectangle((x,y,x+im.width,y+im.height),outline=(28,30,34),width=8)
art=OUT/'p09_art_v02.png';page.save(art,optimize=True)
letter=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(letter)
font=ImageFont.truetype(fontpath,46)
d.rounded_rectangle((136,1310,448,1500),radius=78,fill=(253,251,247,250),outline=(27,27,28),width=5)
d.polygon([(428,1443),(482,1490),(429,1480)],fill=(253,251,247,250))
d.text((201,1366),'ただい……',font=font,fill=(29,27,26))
# The exact Japanese text is typeset on a separate layer and skewed with the paper.
fontnote=ImageFont.truetype(fontpath,40)
text=Image.new('RGBA',(490,180),(0,0,0,0)); td=ImageDraw.Draw(text)
td.text((15,50),'経費、帰ってから',font=fontnote,fill=(56,52,46))
text=text.rotate(4,Image.Resampling.BICUBIC,expand=False)
letter.alpha_composite(text,(48+407,1612+102))
d=ImageDraw.Draw(letter);d.text((1310,2074),'09',font=ImageFont.truetype(fontpath,22),fill=(35,35,34),anchor='rb')
letterpath=OUT/'p09_lettering_v02.png';letter.save(letterpath,optimize=True)
final=OUT/'p09_candidate_v02.png';Image.alpha_composite(page.convert('RGBA'),letter).convert('RGB').save(final,optimize=True)
manifest={'page':'P09','status':'art-candidate','size':[W,H],'source':'build_ep01_p09_v02.py','assets':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (art,letterpath,final)}}
(OUT/'manifest_v02.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(manifest,ensure_ascii=False))
