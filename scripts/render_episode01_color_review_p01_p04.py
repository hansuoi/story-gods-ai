#!/usr/bin/env python3
"""Render P01–P04 actual PNGs as a 2x2 manga contact sheet for human QA."""
from pathlib import Path
from hashlib import sha256
import base64, json
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/art/episode-01/finish/color-candidates'
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

def main():
    sheet=Image.new('RGB',(920,1420),'#eeeae2')
    draw=ImageDraw.Draw(sheet)
    font=ImageFont.truetype(FONT,30)
    manifest=json.loads((BASE/'revision-manifest.json').read_text(encoding='utf-8'))
    for i in range(1,5):
        path=BASE/f'p{i:02d}_v01.png'
        assert sha256(path.read_bytes()).hexdigest()==manifest[path.name]['sha256']
        with Image.open(path) as src:
            assert src.size==(1024,1536)
            small=src.convert('RGB').resize((421,632),Image.Resampling.LANCZOS)
        j=i-1;x=22+(j%2)*447;y=22+(j//2)*696
        draw.text((x,y),f'P{i:02d} color candidate',font=font,fill='#25313b')
        sheet.paste(small,(x,y+40))
    dest=BASE/'review_p01_p04.jpg';sheet.save(dest,quality=91,subsampling=0,optimize=True)
    (BASE/'review_p01_p04.jpg.base64').write_text(base64.b64encode(dest.read_bytes()).decode('ascii')+'\n',encoding='ascii')
    print(dest.name,len(dest.read_bytes()),sha256(dest.read_bytes()).hexdigest())
if __name__=='__main__':main()
