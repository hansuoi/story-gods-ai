#!/usr/bin/env python3
"""Render P05 funeral title-page v03 as a shoulder-cropped, quiet composition.

Independent P05 v03 renderer. Crops Aki above the shoulders to avoid
unsupported facial detail; emphasizes the closed coffin and clenched hands.
This renderer is NOT claimed to reproduce any separately created conversation
image with the same version number; verify the output image independently.
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

    # Aki is intentionally cropped at the shoulder; the clenched hands,
    # not a simplified portrait, communicate her grief. Her head is off-frame.
    shadow(im, [(0, 1560), (255, 1400), (685, H), (0, H)], 54, 155)
    d = ImageDraw.Draw(im, "RGBA")
    polygon(d, [(0, 1445), (105, 1408), (220, 1414), (304, 1474),
                (470, 1610), (558, 1870), (685, H), (0, H)],
            (14, 19, 28, 255), (4, 8, 14, 255), 9)
    polygon(d, [(0, 1490), (140, 1480), (254, 1550), (323, 1660),
                (442, H), (245, H), (207, 1820), (120, 1620)],
            (34, 41, 52, 190))
    polygon(d, [(0, 1540), (132, 1510), (260, 1580), (360, 1730),
                (615, H), (415, H), (375, 1910), (180, 1700)],
            (6, 10, 18, 220))
    d.line([(8, 1518), (125, 1526), (252, 1658), (342, 1870)],
           fill=(143, 155, 166, 47), width=6, joint="curve")
    d.line([(178, 1517), (252, 1588), (327, 1720)],
           fill=(170, 181, 191, 52), width=5, joint="curve")
    # Forearms converge on the clasped hands.
    polygon(d, [(105, 1620), (164, 1578), (237, 1610), (298, 1660),
                (466, 1808), (529, 1848), (531, 1902), (499, 1943),
                (462, 1950), (309, 1912), (168, 1770)],
            (19, 26, 36, 255), (5, 9, 16, 255), 7)
    polygon(d, [(390, 1655), (437, 1627), (485, 1644), (528, 1692),
                (625, 1820), (657, 1868), (653, 1919), (624, 1950),
                (578, 1950), (487, 1892), (425, 1820)],
            (24, 31, 42, 255), (5, 9, 16, 255), 7)
    d.line([(146, 1652), (257, 1760), (420, 1908)],
           fill=(175, 182, 188, 60), width=4, joint="curve")
    d.line([(445, 1703), (558, 1870)],
           fill=(172, 181, 191, 55), width=4)
    # Two distinct hands: one fist enclosed by the other, four bent knuckles.
    polygon(d, [(494, 1820), (517, 1798), (557, 1798), (581, 1817),
                (615, 1845), (626, 1895), (611, 1926), (592, 1962),
                (554, 1976), (514, 1953), (484, 1932), (472, 1854)],
            (164, 145, 135, 255), (64, 52, 53, 255), 6)
    polygon(d, [(455, 1842), (472, 1818), (495, 1821), (524, 1842),
                (561, 1872), (585, 1915), (576, 1951), (562, 1987),
                (526, 2005), (490, 1990), (449, 1970), (426, 1890)],
            (192, 170, 153, 255), (68, 54, 54, 255), 6)
    for j in range(4):
        x = 456 + j * 26
        y = 1878 + j * 9
        d.arc((x, y - 15, x + 39, y + 54), 193, 314,
              fill=(96, 73, 68, 235), width=5)
        d.line([(x + 7, y + 12), (x + 22, y + 6)],
               fill=(240, 211, 188, 120), width=2)
    polygon(d, [(447, 1845), (469, 1817), (495, 1818), (516, 1838),
                (529, 1855), (536, 1877), (523, 1889), (493, 1894),
                (473, 1868)], (218, 191, 170, 255),
            (100, 76, 71, 255), 4)
    d.line([(452, 1954), (485, 1980), (512, 1990)],
           fill=(239, 213, 193, 94), width=3)
    for j in range(180):
        r = random.Random(30000 + j)
        x, y = r.randrange(5, 615), r.randrange(1580, H)
        d.line([(x, y), (x + r.randint(-15, 15),
                         y - r.randint(8, 23))],
               fill=(200, 211, 222, r.randint(4, 13)), width=1)
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
    art.save(out / "p05-funeral-art-v03-rendered.png", optimize=True)
    overlay.save(out / "p05-title-overlay-v03-rendered.png", optimize=True)
    Image.alpha_composite(art.convert("RGBA"), overlay).convert("RGB").save(
        out / "p05-color-candidate-v03-rendered.png", optimize=True
    )
    print("P05 candidate: 1400x2100, source artwork and title overlay saved")


if __name__ == "__main__":
    main()
