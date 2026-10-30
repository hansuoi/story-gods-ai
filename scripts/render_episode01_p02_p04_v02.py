#!/usr/bin/env python3
"""Preview alternative P02-P04, reusing the exact same painted hinge on P19/P20.

The old paper-flat technical diagrams remain preserved in v01; these v02
candidates are NOT automatically accepted for publication.
"""
from __future__ import annotations
import base64,json
from hashlib import sha256
from PIL import Image,ImageDraw,ImageFont,ImageOps
import render_episode01_p01_p04 as old

BASE=old.BASE
HINGE=BASE/'sources/p19_p20_hinge_photo.png'

def painted_metal(im,box,broken=True,impact=False,repair=False,scale=1):
    x0,y0,x1,y1=map(int,box)
    w,h=x1-x0,y1-y0
    with Image.open(HINGE) as src:
        pic=ImageOps.fit(src.convert('RGB'),(w,h),Image.Resampling.LANCZOS)
    im.paste(pic,(x0,y0))
    d=ImageDraw.Draw(im)
    X=lambda p:x0+round(w*p)
    Y=lambda p:y0+round(h*p)
    # The original reference is a photograph of an ALREADY damaged hinge.
    # On P02 (before impact) and P04 (after repair), erase its old highlighted
    # crack with a feathered patch of nearby steel texture before drawing
    # the still-bent but connected retaining pin. Otherwise the reference
    # would accidentally reveal the P03 damage one page too early.
    if not broken or repair:
        px0,py0,px1,py1=int(w*.32),int(h*.23),int(w*.68),int(h*.79)
        patch=ImageOps.fit(pic.crop((int(w*.12),int(h*.18),int(w*.36),int(h*.86))),
                           (px1-px0,py1-py0),Image.Resampling.LANCZOS)
        mask=Image.new('L',patch.size,0)
        ImageDraw.Draw(mask).ellipse((0,0,patch.width-1,patch.height-1),fill=255)
        mask=mask.filter(__import__('PIL.ImageFilter',fromlist=['GaussianBlur']).GaussianBlur(max(5,round(w*.025))))
        im.paste(patch,(x0+px0,y0+py0),mask)
        d=ImageDraw.Draw(im)
    # Thin retaining pin inside the old bent hinge. At P02 it is not cut.
    points=[(X(.49),Y(.41)),(X(.54),Y(.47)),(X(.48),Y(.55)),(X(.55),Y(.62))]
    d.line(points,fill='#182f3a',width=max(10,round(w*.029)),joint='curve')
    d.line(points,fill='#bacbd0',width=max(5,round(w*.010)),joint='curve')
    if broken and not repair:
        rad=max(7,round(w*.016))
        center=X(.486),Y(.545)
        d.ellipse((center[0]-rad,center[1]-rad,center[0]+rad,center[1]+rad),
                  fill='#192f3c',outline='#d5e4e5',width=2)
        d.line([(X(.46),Y(.54)),(X(.51),Y(.56))],fill='#142936',
               width=max(8,round(w*.024)))
    if repair:
        d.arc((X(.41),Y(.40),X(.62),Y(.70)),35,327,fill='#c5e4e3',
              width=max(3,round(w*.007)))
        d.arc((X(.38),Y(.38),X(.64),Y(.73)),45,300,fill='#69b2c6',
              width=max(2,round(w*.003)))
    if impact:
        target=X(.49),Y(.55)
        # Just three water droplets: not a high-volume spray.
        for i in range(3):
            sx=x0-round(w*.25)-round((i-1)*w*.055)
            sy=Y(.88)+round((i-1)*h*.06)
            d.line([(sx,sy),target],fill='#e2f8fa',width=max(3,round(w*.008)))
            d.ellipse((sx-4,sy-4,sx+4,sy+4),fill='#e8ffff')
        for dx,dy in ((-24,-17),(0,-32),(25,4),(-12,29)):
            d.line([target,(target[0]+dx,target[1]+dy)],fill='#e4f7f9',width=3)

def main():
    assert HINGE.exists(), 'P19 photo generation must precede P02-P04 v02'
    with Image.open(old.RESCUE) as x: rescue=x.convert('RGB')
    with Image.open(old.SAKAKI) as x: portrait=x.convert('RGB')
    assert rescue.size==(697,1008) and portrait.size==(240,260)
    old.metal=painted_metal
    manifest_path=BASE/'revision-manifest.json'
    manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
    sources={str(p.relative_to(BASE)):sha256(p.read_bytes()).hexdigest()
             for p in (old.RESCUE,old.SAKAKI,HINGE)}
    for n,func in ((2,old.render_p02),(3,old.render_p03),(4,old.render_p04)):
        previous_scene=old.scene
        if n==3:
            # Original third panel re-used the OUTSTRETCHED arms from P01,
            # showing no actual rescue. Another crop of the SAME color source
            # contains a boy gripping an orange-jacketed rescue worker.
            # Keep the shot only on P03 after the pin is struck.
            def rescue_contact_scene(im,source,crop,box,center=(.5,.5),tone=0):
                if tuple(box)==(30,996,994,1366):
                    return previous_scene(im,source,(186,842,696,1008),box,
                                          center=(.48,.52),tone=.045)
                return previous_scene(im,source,crop,box,center=center,tone=tone)
            old.scene=rescue_contact_scene
        try:
            result=func(rescue,portrait)
        finally:
            old.scene=previous_scene
        assert result.size==(1024,1536)
        dest=BASE/f'p{n:02d}_v02.png'
        result.save(dest,optimize=True)
        raw=dest.read_bytes()
        manifest[dest.name]={
          'page':n,'status':'candidate-needs-visual-review',
          'width':1024,'height':1536,'bytes':len(raw),
          'sha256':sha256(raw).hexdigest(),'source':sources,
          'notes':'P02/P03/P04 share one painted hinge; retaining pin changes before strike, after strike and repair. P03 now depicts the boy physically gripping an orange-jacketed rescue worker; other artwork remains provisional.'}
        print(dest.name,len(raw),manifest[dest.name]['sha256'])
    manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')
    # Human visual proof sheet: unchanged P01, revised P02-P04.
    sheet=Image.new('RGB',(920,1420),'#eeeae2')
    draw=ImageDraw.Draw(sheet)
    font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',27)
    for n in range(1,5):
        filename=f'p{n:02d}_v01.png' if n==1 else f'p{n:02d}_v02.png'
        with Image.open(BASE/filename) as im:
            assert im.size==(1024,1536)
            reduced=im.convert('RGB').resize((421,632),Image.Resampling.LANCZOS)
        i=n-1;x=22+(i%2)*447;y=22+(i//2)*696
        draw.text((x,y),f'P{n:02d} '+('original' if n==1 else 'hinge v02'),font=font,fill='#25313b')
        sheet.paste(reduced,(x,y+40))
    proof=BASE/'review_p01_p04_v02.jpg'
    sheet.save(proof,quality=90,subsampling=0,optimize=True)
    (BASE/'review_p01_p04_v02.jpg.base64').write_text(
        base64.b64encode(proof.read_bytes()).decode('ascii')+'\n',encoding='ascii')

if __name__=='__main__':
    main()
