#!/usr/bin/env python3
"""Episode 1 plot/callback checks on the 32-page SVG reading proof.

Not a substitute for visual assessment, dialogue editing, or finished-art signoff.
"""
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
PROOF = ROOT / "docs/art/episode-01/finish/readproof"
PAGE_COUNT = 32
# The strings on each page form essential beats, not comprehensive dialogue transcripts.
REQUIRED = {
    1: ("2024年", "だれか", "開けりゃ"),
    2: ("保持ピン", "ここだけ"),
    3: ("ピンッ", "レバー"),
    4: ("雨は直らないの？", "帰るよ"),
    5: ("2026年10月",),
    6: ("……死因は？", "警察が調べています"),
    9: ("経費、帰ってから",),
    10: ("次はちゃんと説明してよ。",),
    12: ("タクシー領収書", "旧汀橋方面"),
    13: ("2018年", "保 留"),
    14: ("写しを渡します。", "現場には近づかないで。"),
    15: ("自分で確かめる。",),
    16: ("そこ、工事中ですよ。",),
    17: ("奥さん？",),
    18: ("救急に通報したのは", "修復の仕事"),
    19: ("10分だけ",),
    20: ("留め針", "夫の身体も"),
    21: ("誰が", "事故とも"),
    24: ("受付は、まだいます",),
    25: ("神谷さんの奥さん",),
    26: ("危ない仕事は俺がやる",),
    28: ("TB-18-042",),
    29: ("本人へ返却",),
    30: ("依頼者：神谷榊",),
    31: ("調査対象：神谷榊",),
    32: ("番号非通知", "夫のことなら、", "私が聞きます"),
}
# Facts deliberately withheld until a later page must not leak via UI lettering.
FORBIDDEN = {
    1: ("2018年", "2026年"),
    5: ("調査対象：", "依頼者："),
    14: ("調査対象：神谷榊",),
    30: ("調査対象：神谷榊",),
    32: ("調査対象：神谷榊",),
}

def check() -> None:
    errors = []
    for n in range(1, PAGE_COUNT + 1):
        path = PROOF / f"p{n:02d}.svg"
        if not path.is_file():
            errors.append(f"P{n:02d}: missing file")
            continue
        try:
            root = ET.parse(path).getroot()
        except ET.ParseError as err:
            errors.append(f"P{n:02d}: invalid XML: {err}")
            continue
        text = " ".join((el.text or "").strip() for el in root.iter() if el.tag.endswith("}text"))
        # Stripping whitespace entirely allows the same dialogue to span balloons/lines.
        flat = re.sub(r"\s+", "", text)
        for phrase in REQUIRED.get(n, ()):
            if re.sub(r"\s+", "", phrase) not in flat:
                errors.append(f"P{n:02d}: missing story beat {phrase!r}")
        for phrase in FORBIDDEN.get(n, ()):
            if re.sub(r"\s+", "", phrase) in flat:
                errors.append(f"P{n:02d}: early or repeated reveal {phrase!r}")
        if not list(root.iter()):
            errors.append(f"P{n:02d}: empty page")
    if errors:
        print("STORY CHECK FAILED:\n" + "\n".join(errors), file=sys.stderr)
        raise SystemExit(1)
    print("Episode 1 story-beat checks passed for 32 SVG pages.")
    print("Artistic, visual and lettering quality remain NOT APPROVED.")

if __name__ == "__main__":
    check()
