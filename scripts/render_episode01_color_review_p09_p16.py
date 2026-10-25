#!/usr/bin/env python3
"""Publish an eight-page contact sheet of current P09–P16 color review candidates."""
from pathlib import Path
from hashlib import sha256
import json
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/art/episode-01/finish/color-candidates'
OUTPUT=BASE/'review_p09_p16_current.jpg'
PAGES=['p09_v01.png','p10_v01.png','p11_v01.png','p12_v01.png',
       'p13_v02.png','p14_v02.png','p15_v02.png','p16_v01.png']
W,H,GAP,LABEL=265,398,20,44

def main():
    sheet=Image.new('RGB',(4*(W+GAP)+GAP,2*(H+LABEL+GAP)+GAP),'#eeeae2')
    d=ImageDraw.Draw(sheet)
    font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',27)
    m=json.loads((BASE/'revision-manifest.json').read_text(encoding='utf-8'))
    for i,filename in enumerate(PAGES):
        path=BASE/filename
        assert sha256(path.read_bytes()).hexdigest()==m[filename]['sha256']
        with Image.open(path) as png:
            assert png.size==(1024,1536)
            thumb=png.convert('RGB').resize((W,H),Image.Resampling.LANCZOS)
        x=GAP+(i%4)*(W+GAP)
        y=GAP+(i//4)*(H+LABEL+GAP)
        d.text((x,y),f'P{i+9:02d}',font=font,fill='#27333b')
        sheet.paste(thumb,(x,y+LABEL))
    sheet.save(OUTPUT,quality=91,subsampling=0,optimize=True)
    print(OUTPUT,OUTPUT.stat().st_size,sha256(OUTPUT.read_bytes()).hexdigest())
if __name__=='__main__':main()
