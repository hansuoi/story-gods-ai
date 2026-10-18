#!/usr/bin/env python3
"""Render P05 funeral title page v04 as original reproducible raster art.

Original painterly gradients and vector-like curved brush paths are rasterized.
Japanese title typography remains in an independent PNG layer. A candidate is
never an automatically accepted finished page.
"""
from __future__ import annotations
import argparse
import hashlib
import math
from pathlib import Path
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1400, 2100
SEED = 20261018


def path(draw, pts, fill, outline=None, width=1, samples=18):
    """Draw M/L/C cubic segments as a filled raster shape."""
    xy = []
    pos = None
    for p in pts:
        if p[0] == "M":
            pos = (p[1], p[2])
            xy.append(pos)
        elif p[0] == "L":
            pos = (p[1], p[2])
            xy.append(pos)
        else:
            x0, y0 = pos
            _, x1, y1, x2, y2, x3, y3 = p
            for i in range(1, samples + 1):
                t = i / samples
                s = 1 - t
                xy.append((s**3*x0 + 3*s*s*t*x1 + 3*s*t*t*x2 + t**3*x3,
                           s**3*y0 + 3*s*s*t*y1 + 3*s*t*t*y2 + t**3*y3))
            pos = (x3, y3)
    if fill is not None:
        draw.polygon(xy, fill=fill)
    if outline is not None:
        draw.line(xy + [xy[0]], fill=outline, width=width, joint="curve")


def font(size, serif=False):
    family = "Noto Serif CJK JP" if serif else "Noto Sans CJK JP"
    filename = subprocess.check_output(
        ["fc-match", "-f", "%{file}", family], text=True).strip()
    if not filename or not Path(filename).exists():
        raise RuntimeError("fonts-noto-cjk required")
    return ImageFont.truetype(filename, size)


def haze(im, center, radii, tint, strength):
    yy, xx = np.ogrid[:H, :W]
    a = np.exp(-(((xx-center[0])/radii[0])**2
                 + ((yy-center[1])/radii[1])**2)) * strength
    data = np.asarray(im).astype("float32")
    data += (np.array(tint, dtype="float32")-data) * a[:, :, None]
    return Image.fromarray(np.uint8(np.clip(data, 0, 255)), "RGB")


def render_art():
    rng = np.random.default_rng(SEED)
    yy, xx = np.mgrid[:H, :W].astype("float32")
    light = np.exp(-((xx-1040)**2/980**2+(yy-720)**2/920**2))
    edge = np.clip((xx-760)/640, 0, 1)
    grain = rng.normal(0, 2.3, (H, W))
    data = np.stack([
        np.clip(29+37*light+7*edge+grain, 0, 255),
        np.clip(33+41*light+7*edge+grain, 0, 255),
        np.clip(41+43*light+5*edge+grain, 0, 255)
    ], axis=2).astype("uint8")
    im = Image.fromarray(data, "RGB")
    d = ImageDraw.Draw(im, "RGBA")
    d.polygon([(0, 860), (1400, 745), (1400, 2100), (0, 2100)],
              fill=(76, 81, 87, 98))
    d.line([(0, 861), (1400, 746)], fill=(218, 217, 210, 35), width=5)
    d.polygon([(1100, 0), (1400, 0), (1400, 2100), (1370, 2100)],
              fill=(197, 198, 194, 17))
    for x in (-900, -150, 550, 1240, 2300):
        d.line([(1160, 770), (x, 2100)], fill=(228, 227, 221, 16), width=2)
    for y in (1200, 1660, 2050):
        d.line([(0, y+130), (1400, y-90)], fill=(226, 225, 217, 13), width=2)
    d.polygon([(1090, 112), (1306, 96), (1300, 620), (1094, 642)],
              fill=(237, 239, 232, 52))
    d.line([(1090, 112), (1306, 96), (1300, 620), (1094, 642),
            (1090, 112)], fill=(247, 248, 238, 78), width=9)
    d.line([(1198, 107), (1198, 632)], fill=(248, 250, 244, 56), width=6)
    im = haze(im, (1190, 580), (510, 850), (211, 218, 218), .13)
    mask = Image.new("L", (W, H))
    ImageDraw.Draw(mask).polygon(
        [(530, 1350), (920, 1540), (1310, 800), (1050, 700)], fill=170)
    mask = mask.filter(ImageFilter.GaussianBlur(65))
    im.paste(Image.new("RGB", (W, H), (13, 18, 24)), (0, 0), mask)
    d = ImageDraw.Draw(im, "RGBA")
    d.polygon([(586, 1330), (884, 1502), (1240, 817), (1040, 709)],
              fill=(22, 26, 30, 245))
    d.line([(599, 1340), (886, 1494), (1228, 823)],
           fill=(171, 174, 169, 64), width=8)
    d.polygon([(521, 1215), (858, 1424), (868, 1511), (522, 1303)],
              fill=(178, 184, 186, 255))
    d.polygon([(858, 1424), (1231, 773), (1226, 847), (868, 1511)],
              fill=(141, 149, 152, 255))
    d.polygon([(521, 1215), (593, 1166), (1019, 687), (1114, 686),
               (1231, 773), (858, 1424)], fill=(231, 234, 231, 255))
    path(d, [("M", 566, 1212), ("C", 625, 1157, 778, 978, 1034, 708),
             ("L", 1114, 708), ("L", 1204, 778), ("L", 844, 1389),
             ("L", 566, 1212)], (244, 245, 238, 255),
         (123, 136, 141, 130), 4)
    d.line([(573, 1213), (850, 1390), (1208, 780)],
           fill=(252, 254, 249, 235), width=8)
    d.line([(534, 1265), (864, 1476), (1227, 814)],
           fill=(241, 244, 238, 144), width=5)
    d.line([(569, 1225), (842, 1394)], fill=(118, 128, 131, 93), width=4)
    shine = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(shine, "RGBA").polygon(
        [(595, 1188), (687, 1080), (1140, 723), (1180, 760), (836, 1360)],
        fill=(255, 255, 255, 33))
    shine = shine.filter(ImageFilter.GaussianBlur(38))
    im = Image.alpha_composite(im.convert("RGBA"), shine).convert("RGB")
    d = ImageDraw.Draw(im, "RGBA")
    d.rounded_rectangle((699, 1392, 781, 1412), radius=8,
                        fill=(186, 192, 193, 255),
                        outline=(77, 86, 91, 255), width=4)
    d.arc((713, 1384, 765, 1465), 15, 165,
          fill=(64, 76, 83, 255), width=7)
    d.arc((720, 1392, 757, 1451), 15, 165,
          fill=(239, 240, 232, 255), width=3)
    for cx, cy, r in [(1196, 640, 18), (1162, 628, 13), (1221, 661, 15)]:
        d.line([(cx-4, cy+14), (1135, 710)], fill=(72, 94, 79, 195), width=5)
        for k in range(5):
            a = k * math.tau / 5
            px = cx+math.cos(a)*r
            py = cy+math.sin(a)*r*.65
            d.ellipse((px-r*.56, py-r*.45, px+r*.56, py+r*.45),
                      fill=(236, 239, 233, 235))
        d.ellipse((cx-5, cy-5, cx+5, cy+5), fill=(185, 177, 147, 240))
    mask = Image.new("L", (W, H))
    ImageDraw.Draw(mask).ellipse((-380, 1270, 850, 2580), fill=150)
    mask = mask.filter(ImageFilter.GaussianBlur(55))
    im.paste(Image.new("RGB", (W, H), (6, 9, 14)), (0, 0), mask)
    d = ImageDraw.Draw(im, "RGBA")
    path(d, [("M", 0, 1450), ("C", 100, 1395, 181, 1380, 259, 1426),
             ("C", 349, 1468, 449, 1610, 521, 1775),
             ("L", 696, 2100), ("L", 0, 2100)],
         (12, 16, 24, 255), (4, 7, 13, 255), 8)
    path(d, [("M", 0, 1485), ("C", 80, 1460, 161, 1480, 238, 1560),
             ("C", 319, 1652, 351, 1800, 439, 2100),
             ("L", 206, 2100), ("C", 168, 1830, 98, 1660, 0, 1570)],
         (34, 39, 49, 230))
    path(d, [("M", 200, 1465), ("C", 315, 1502, 398, 1662, 455, 1790),
             ("L", 573, 2100), ("L", 415, 2100),
             ("C", 383, 1928, 298, 1732, 200, 1465)], (6, 9, 16, 225))
    for pts in [
        [(50, 1518), (159, 1540), (278, 1688), (344, 1850)],
        [(201, 1504), (298, 1620), (360, 1744)],
        [(92, 1592), (210, 1745), (267, 1918)],
        [(372, 1750), (426, 1920), (486, 2080)]
    ]:
        d.line(pts, fill=(170, 181, 188, 55), width=5, joint="curve")
    path(d, [("M", 92, 1665), ("C", 160, 1590, 224, 1598, 287, 1674),
             ("C", 344, 1737, 438, 1831, 521, 1851),
             ("L", 563, 1938), ("C", 465, 2001, 327, 1881, 238, 1798),
             ("C", 166, 1736, 132, 1714, 92, 1665)],
         (22, 28, 37, 255), (5, 8, 15, 255), 7)
    path(d, [("M", 374, 1710), ("C", 426, 1659, 479, 1676, 520, 1741),
             ("L", 647, 1871), ("C", 677, 1921, 659, 1970, 625, 1996),
             ("L", 563, 1978), ("C", 507, 1909, 420, 1810, 374, 1710)],
         (19, 25, 34, 255), (5, 8, 15, 255), 7)
    d.line([(135, 1668), (251, 1758), (431, 1911)],
           fill=(175, 181, 188, 55), width=4, joint="curve")
    d.line([(414, 1720), (559, 1881)],
           fill=(175, 181, 188, 50), width=4)
    path(d, [("M", 532, 1816), ("C", 558, 1794, 596, 1792, 624, 1813),
             ("C", 653, 1838, 678, 1876, 670, 1912),
             ("C", 662, 1952, 630, 1985, 595, 1984),
             ("C", 566, 1976, 547, 1960, 522, 1930),
             ("C", 497, 1901, 498, 1848, 532, 1816)],
         (162, 143, 136, 255), (57, 49, 53, 255), 6)
    path(d, [("M", 480, 1853), ("C", 497, 1831, 526, 1824, 552, 1840),
             ("C", 580, 1854, 600, 1882, 609, 1903),
             ("C", 619, 1928, 605, 1945, 590, 1966),
             ("C", 587, 1995, 566, 2024, 534, 2028),
             ("C", 502, 2030, 478, 2005, 456, 1984),
             ("C", 435, 1963, 431, 1928, 448, 1893),
             ("C", 455, 1872, 468, 1862, 480, 1853)],
         (191, 168, 152, 255), (64, 51, 51, 255), 6)
    for j in range(4):
        x = 476+j*24
        y = 1875+j*11
        d.arc((x, y-17, x+43, y+56), 195, 310,
              fill=(99, 73, 67, 230), width=4)
        d.arc((x+8, y-12, x+32, y+19), 205, 295,
              fill=(244, 214, 189, 110), width=2)
    path(d, [("M", 459, 1865), ("C", 470, 1839, 485, 1833, 504, 1838),
             ("C", 524, 1842, 541, 1858, 548, 1878),
             ("C", 555, 1892, 547, 1902, 534, 1905),
             ("C", 513, 1909, 489, 1895, 471, 1882)],
         (211, 185, 164, 255), (93, 69, 65, 255), 4)
    d.arc((482, 1918, 568, 2010), 14, 135,
          fill=(238, 211, 192, 105), width=3)
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay, "RGBA")
    for _ in range(390):
        x = int(rng.integers(0, 680))
        y = int(rng.integers(1510, H))
        od.line([(x, y), (x+int(rng.integers(-7, 12)),
                           y-int(rng.integers(4, 17)))],
                fill=(206, 213, 218, int(rng.integers(5, 16))), width=1)
    return Image.alpha_composite(im.convert("RGBA"), overlay).convert("RGB")


def render_text():
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.text((92, 120), "2026年10月", font=font(43),
           fill=(222, 228, 227, 255))
    d.line([(94, 209), (491, 209)], fill=(221, 225, 223, 140), width=2)
    d.text((88, 274), "神谷家", font=font(126, True),
           fill=(246, 245, 238, 255))
    d.text((99, 465), "- 原状回復 -", font=font(50, True),
           fill=(231, 234, 231, 255))
    d.text((99, 605), "第1話  帰ってきた人", font=font(41),
           fill=(228, 231, 228, 255))
    return im


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", type=Path,
                        default=Path("build/episode01-color/p05-v04"))
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    art, txt = render_art(), render_text()
    result = Image.alpha_composite(art.convert("RGBA"), txt).convert("RGB")
    for name, im in [
        ("p05-funeral-art-v04.png", art),
        ("p05-title-overlay-v04.png", txt),
        ("p05-color-candidate-v04.png", result)
    ]:
        dest = args.out_dir/name
        im.save(dest, optimize=True)
        print(name, hashlib.sha256(dest.read_bytes()).hexdigest(), im.size)


if __name__ == "__main__":
    main()
