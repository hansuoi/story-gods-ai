#!/usr/bin/env python3
"""Render visual QA contact sheets for P17–20 and P21–24 color page candidates.

Preview images are not publication proofs. The full-resolution page PNGs remain
the quality-review objects. Source and resulting hashes are checked by the
color revision workflow.
"""
from pathlib import Path
from hashlib import sha256
from PIL import Image, ImageDraw, ImageFont
import json, base64

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/art/episode-01/finish/color-candidates'
SIZE=(1024,1536)
TW,TH,GAP,LABEL=446,669,20,42

def main():
    manifest=json.loads((BASE/'revision-manifest.json').read_text(encoding='utf-8'))
    font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',27)
    for a,b in ((17,20),(21,24)):
        contact=Image.new('RGB',(2*TW+3*GAP,2*(TH+LABEL)+3*GAP),'#efebe3')
        d=ImageDraw.Draw(contact)
        for n in range(a,b+1):
            name=f'p{n:02d}_v01.png';f=BASE/name
            raw=f.read_bytes()
            assert sha256(raw).hexdigest()==manifest[name]['sha256'],name
            with Image.open(f) as im:
                assert im.size==SIZE
                thumbnail=im.convert('RGB').resize((TW,TH),Image.Resampling.LANCZOS)
            i=n-a
            x=GAP+(i%2)*(TW+GAP)
            y=GAP+(i//2)*(TH+LABEL+GAP)
            d.text((x,y),f'P{n:02d}',fill='#202b32',font=font)
            contact.paste(thumbnail,(x,y+LABEL))
        out=BASE/f'review_p{a:02d}_p{b:02d}.jpg'
        contact.save(out,quality=90,optimize=True,subsampling=0)
        data=out.read_bytes()
        (BASE/(out.name+'.base64')).write_text(base64.b64encode(data).decode('ascii')+'\n',encoding='ascii')
        print(out.name,len(data),sha256(data).hexdigest())

if __name__=='__main__':main()
