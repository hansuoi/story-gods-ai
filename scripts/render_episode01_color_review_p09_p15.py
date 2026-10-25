#!/usr/bin/env python3
"""Render a seven-page contact sheet from actual P09–P15 color candidates."""
from pathlib import Path
from hashlib import sha256
import json
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/art/episode-01/finish/color-candidates'
OUTPUT=BASE/'review_p09_p15.jpg'
PAGES=[f'p{i:02d}_v01.png' for i in range(9,16)]
W,H,GAP,LABEL=265,398,20,44

def main():
    sheet=Image.new('RGB',(4*(W+GAP)+GAP,2*(H+LABEL+GAP)+GAP),'#eeebe4')
    d=ImageDraw.Draw(sheet)
    f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',27)
    manifest=json.loads((BASE/'revision-manifest.json').read_text(encoding='utf-8'))
    for i,p in enumerate(PAGES):
        path=BASE/p
        raw=path.read_bytes()
        assert sha256(raw).hexdigest()==manifest[p]['sha256']
        with Image.open(path) as im:
            assert im.size==(1024,1536)
            resized=im.convert('RGB').resize((W,H),Image.Resampling.LANCZOS)
        x=GAP+(i%4)*(W+GAP)
        y=GAP+(i//4)*(H+LABEL+GAP)
        d.text((x,y),f'P{i+9:02d}',font=f,fill='#23303a')
        sheet.paste(resized,(x,y+LABEL))
    sheet.save(OUTPUT,quality=91,subsampling=0,optimize=True)
    print(OUTPUT,OUTPUT.stat().st_size,sha256(OUTPUT.read_bytes()).hexdigest())
if __name__=='__main__':main()
