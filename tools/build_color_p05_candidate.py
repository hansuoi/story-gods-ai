#!/usr/bin/env python3
"""Render P05 funeral title-page as original raster artwork and separate text layer.

No P01 images or third-party generated assets are used. This is a reproducible
composition candidate, not a declaration of finished manga-quality illustration.
"""
from __future__ import annotations

import argparse
import math
import random
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1400, 2100
SEED = 20261018


def font(size: int, serif: bool = True) -> ImageFont.FreeTypeFont:
    family = "Noto Serif CJK JP" if serif else "Noto Sans CJK JP"
    try:
        filename = subprocess.check_output(
            ["fc-match", "-f", "%{file}", family], text=True
        ).strip()
        if filename and Path(filename).exists():
            return ImageFont.truetype(filename, size)
    except (OSError, subprocess.CalledProcessError):
        pass
    raise RuntimeError("Install fonts-noto-cjk for Japanese text")


def polygon(draw, vertices, fill, outline=None, width=4):
    draw.polygon(vertices, fill=fill)
    if outline:
        draw.line(vertices + [vertices[0]], fill=outline, width=width, joint="curve")


def shadow(im, vertices, blur, opacity, color=(12, 16, 22)):
    mask = Image.new("L", (W, H))
    ImageDraw.Draw(mask).polygon(vertices, fill=opacity)
    mask = mask.filter(ImageFilter.GaussianBlur(blur))
    im.paste(Image.new("RGB", (W, H), color), (0, 0), mask)


def render_art():
    rng = np.random.default_rng(SEED)
    yy, xx = np.mgrid[0:H, 0:W].astype("float32")
    light = np.exp(-(((xx - 1110) / 700) ** 2 + ((yy - 650) / 880) ** 2))
    floor = np.clip((yy - 760) / 1100, 0, 1)
    grain = rng.normal(0, 1.65, (H, W))
    rgb = np.empty((H, W, 3), dtype=np.uint8)
    for c, (base, bright, low) in enumerate(((42, 37, 20), (47, 42, 22), (54, 42, 23))):
        rgb[:, :, c] = np.clip(base + bright * light + low * floor + grain, 0, 255)
    im = Image.fromarray(rgb, "RGB")
    d = ImageDraw.Draw(im, "RGBA")
    d.polygon([(0, 720), (1400, 785), (1400, H), (0, H)], fill=(87, 91, 95, 125))
    d.polygon([(0, 0), (210, 0), (0, H)], fill=(17, 22, 30, 110))
    d.line([(0, 722), (1400, 785)], fill=(198, 198, 188, 50), width=3)
    for x in (-200, 180, 600, 1100, 1900):
        d.line([(880, 755), (x, H)], fill=(222, 223, 219, 16), width=2)
    for y in (1120, 1540, 1940):
        d.line([(0, y - 100), (W, y + 40)], fill=(222, 222, 214, 15), width=2)
    d.polygon([(990, 110), (1280, 138), (1280, 615), (990, 590)],
              fill=(198, 205, 201, 45))
    d.line([(988, 112), (1281, 138), (1281, 615), (990, 590), (988, 112)],
           fill=(231, 232, 221, 72), width=8)
    d.line([(1135, 126), (1135, 602)], fill=(236, 238, 234, 50), width=7)
    d.line([(993, 350), (1278, 367)], fill=(235, 238, 232, 45), width=5)
    d.line([(460, 90), (460, 770)], fill=(198, 198, 190, 19), width=4)

    # Closed white coffin on a low bier, extending diagonally into the room.
    shadow(im, [(515, 1350), (950, 1530), (1280, 780), (1030, 670)], 68, 165)
    d = ImageDraw.Draw(im, "RGBA")
    d.polygon([(535, 1320), (922, 1475), (1240, 789), (1040, 690)],
              fill=(31, 36, 40, 245))
    near_l, near_r = (530, 1237), (876, 1420)
    far_l, far_r = (1030, 678), (1220, 766)
    polygon(d, [near_r, far_r, (1218, 831), (876, 1515)],
            (151, 158, 158, 255), (75, 82, 85, 240), 5)
    polygon(d, [near_l, near_r, (876, 1515), (530, 1320)],
            (187, 193, 191, 255), (79, 87, 90, 240), 5)
    polygon(d, [near_l, (575, 1195), far_l, (1105, 680), far_r,
                (1238, 785), near_r, (830, 1410)],
            (222, 225, 217, 255), (97, 103, 102, 235), 6)
    d.line([(581, 1210), (1055, 700), (1194, 772), (850, 1385)],
           fill=(253, 253, 245, 220), width=10, joint="curve")
    d.line([(552, 1245), (876, 1405), (1220, 767)],
           fill=(93, 103, 107, 100), width=4)
    d.line([(543, 1265), (874, 1443), (1224, 793)],
           fill=(240, 240, 229, 175), width=5)
    d.rounded_rectangle((694, 1385, 772, 1407), radius=6,
                        fill=(177, 183, 182, 220), outline=(91, 98, 101, 240), width=3)
    d.arc((715, 1386, 757, 1443), 10, 175, fill=(76, 85, 89, 255), width=7)
    d.arc((717, 1389, 754, 1436), 15, 167, fill=(236, 238, 231, 255), width=3)
    for start, end in [((1070, 740), (1180, 635)), ((1085, 743), (1160, 620))]:
        d.line([start, end], fill=(72, 91, 77, 215), width=5)
    for cx, cy in [(1177, 629), (1155, 618), (1188, 657)]:
        for j in range(5):
            angle = j * math.tau / 5
            px, py = cx + 17 * math.cos(angle), cy + 12 * math.sin(angle)
            d.ellipse((px - 10, py - 7, px + 10, py + 7), fill=(234, 236, 228, 225))
        d.ellipse((cx - 5, cy - 5, cx + 5, cy + 5), fill=(165, 161, 133, 220))

    # Aki: adult woman in black formal clothes, head bowed, hands clasped.
    shadow(im, [(95, 1300), (490, 1280), (650, H), (20, H)], 28, 140)
    d = ImageDraw.Draw(im, "RGBA")
    polygon(d, [(76, H), (88, 1510), (145, 1308), (258, 1245),
                (395, 1232), (505, 1305), (577, 1505), (624, H)],
            (16, 20, 27, 255), (4, 8, 14, 255), 9)
    polygon(d, [(239, 1239), (345, 1270), (399, 1518),
                (310, 1570), (221, 1360)],
            (27, 31, 39, 255), (93, 98, 103, 180))
    polygon(d, [(365, 1250), (476, 1305), (514, 1435),
                (398, 1525), (345, 1280)],
            (13, 17, 23, 255), (87, 91, 98, 160))
    d.line([(305, 1570), (342, H)], fill=(70, 75, 82, 90), width=5)
    d.line([(135, 1400), (104, 1960)], fill=(126, 130, 133, 52), width=7)
    polygon(d, [(319, 1198), (385, 1212), (400, 1310), (318, 1325)],
            (117, 108, 105, 255), (20, 23, 28, 255))
    polygon(d, [(236, 955), (332, 922), (404, 980), (422, 1100),
                (382, 1205), (322, 1248), (271, 1203), (232, 1123)],
            (164, 151, 142, 255), (19, 22, 30, 255), 5)
    polygon(d, [(193, 1100), (202, 981), (248, 900), (329, 863),
                (402, 908), (441, 996), (438, 1124), (407, 1207),
                (374, 1250), (335, 1236), (346, 1172), (388, 1082),
                (367, 1000), (294, 984), (254, 1095), (242, 1220), (205, 1185)],
            (19, 24, 33, 255), (7, 11, 18, 255), 7)
    d.line([(236, 974), (277, 925), (333, 907), (385, 942)],
           fill=(108, 113, 118, 115), width=7)
    d.line([(340, 1064), (371, 1070)], fill=(73, 64, 67, 200), width=4)
    d.arc((338, 1071, 380, 1100), 15, 153, fill=(71, 60, 62, 220), width=4)
    d.line([(382, 1095), (400, 1124), (384, 1137)],
           fill=(111, 94, 90, 175), width=3)
    d.line([(348, 1168), (377, 1172)], fill=(100, 76, 78, 160), width=3)
    polygon(d, [(410, 1490), (475, 1455), (630, 1602),
                (593, 1690), (489, 1635)],
            (26, 30, 37, 255), (9, 12, 20, 255), 7)
    polygon(d, [(198, 1575), (268, 1545), (490, 1690),
                (452, 1758), (276, 1715)],
            (20, 25, 31, 255), (8, 12, 17, 255), 7)
    polygon(d, [(473, 1645), (508, 1618), (554, 1610), (584, 1636),
                (602, 1670), (588, 1725), (552, 1761), (503, 1740), (466, 1695)],
            (162, 146, 136, 255), (52, 45, 47, 255), 5)
    polygon(d, [(418, 1690), (449, 1659), (483, 1661), (526, 1685),
                (559, 1716), (553, 1757), (520, 1783), (468, 1770), (432, 1735)],
            (188, 168, 152, 255), (57, 49, 50, 255), 5)
    for j in range(4):
        x = 449 + j * 24
        d.arc((x, 1680 + j * 4, x + 36, 1743 + j * 3),
              202, 310, fill=(85, 67, 63, 225), width=4)
    d.line([(469, 1644), (487, 1633)], fill=(225, 225, 216, 170), width=7)
    d.line([(443, 1762), (466, 1777)], fill=(218, 218, 212, 150), width=6)
    for i in range(115):
        r = random.Random(SEED + i)
        x, y = r.randrange(90, 550), r.randrange(1370, H)
        d.line([(x, y), (x + 15, y - 20)], fill=(187, 190, 192, 12), width=1)
    return im


def render_text():
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    d.text((104, 135), "2026年10月", font=font(42, False),
           fill=(222, 226, 220, 245))
    d.line([(107, 222), (465, 222)], fill=(222, 222, 214, 145), width=2)
    d.text((103, 286), "神谷家", font=font(112),
           fill=(239, 239, 230, 255))
    d.text((112, 455), "- 原状回復 -", font=font(49),
           fill=(231, 232, 226, 250))
    d.text((112, 590), "第1話  帰ってきた人", font=font(38, False),
           fill=(220, 222, 219, 245))
    return overlay


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--out-dir",
                   default="docs/art/episode-01/finish/final-candidates/p05")
    out = Path(p.parse_args().out_dir)
    out.mkdir(parents=True, exist_ok=True)
    art, overlay = render_art(), render_text()
    art.save(out / "p05-funeral-art-v01.png", optimize=True)
    overlay.save(out / "p05-title-overlay-v01.png", optimize=True)
    Image.alpha_composite(art.convert("RGBA"), overlay).convert("RGB").save(
        out / "p05-color-candidate-v01.png", optimize=True
    )
    print("P05 candidate: 1400x2100, source artwork and title overlay saved")


if __name__ == "__main__":
    main()
