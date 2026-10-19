#!/usr/bin/env python3
"""Fail fast on common episode-01 SVG failures before GitHub Actions renders PNGs.

Checks the exact source pages: all 32 are present and parse; Japanese speech has a
CJK-capable font; cross-page PNG links cannot silently render blank; the story's
major reveal lines are represented. This is structural QA, NOT a finished-art review.
"""
from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs/art/episode-01/finish/vector-candidates"
SVG_NS = "{http://www.w3.org/2000/svg}"
JP = re.compile(r"[\u3040-\u30ff\u3400-\u9fff]")
REQUIRED: dict[int, tuple[str, ...]] = {
    1: ("2024年", "扉が開かない！", "開けりゃいいんだな？"),
    2: ("壊すのは、ここ", "……よし"),
    3: ("ピンッ", "押せる！"),
    4: ("帰るよ", "プリンも二つ"),
    5: ("2026年10月", "神谷家 - 原状回復 -", "第1話 帰ってきた人"),
    6: ("死因は？", "警察が調べています"),
    7: ("父を助けて", "いい人で", "いつも笑って", "別の人みたい"),
    8: ("事故ですか？", "まだ断定できません"),
    9: ("経費、帰ってから",),
    10: ("説明してよ",),
    11: ("神谷探偵事務所",),
    12: ("汀橋方面", "タクシー領収書"),
    13: ("2018年／汀橋", "保留"),
    14: ("現場には近づかないで",),
    15: ("……誰に会う",),
    16: ("そこ、工事中ですよ",),
    17: ("亡くなりました", "奥さん？"),
    18: ("救急に電話したのは、", "修復の仕事なんで"),
    19: ("直るのを止めました",),
    20: ("留め針", "一箇所だけ。", "戻ったの？"),
    21: ("誰がやったかは、", "事故だったとも、"),
    22: ("2018年／汀橋", "まだ、持ってたんだ"),
    23: ("ごめんなさい", "ないでしょ"),
    24: ("神谷探偵事務所", "受付は、まだいます"),
    25: ("今の人は？", "……大変だったな"),
    26: ("夜の点検、", "安全点検から", "いつもそれだ"),
    27: ("戻らない人も、",),
    28: ("18-07", "……これ？"),
    29: ("本人へ返却",),
    30: ("依頼者：神谷榊", "自分で、自分に"),
    31: ("調査対象：神谷榊", "一枚、ない……"),
    32: ("非通知", "神谷探偵事務所です", "夫のことなら、", "第1話終"),
}


def run() -> list[str]:
    errors: list[str] = []
    for page in range(1, 33):
        file = SOURCE / f"p{page:02d}.svg"
        if not file.is_file():
            errors.append(f"P{page:02d}: missing SVG source")
            continue
        try:
            tree = ET.parse(file)
        except ET.ParseError as exc:
            errors.append(f"P{page:02d}: malformed SVG: {exc}")
            continue
        root = tree.getroot()
        if root.tag != SVG_NS + "svg":
            errors.append(f"P{page:02d}: unexpected XML root: {root.tag}")
        if root.attrib.get("width") != "1024" or root.attrib.get("height") != "1536":
            errors.append(f"P{page:02d}: wrong page dimensions")
        texts: list[str] = []
        parents = {child: parent for parent in root.iter() for child in parent}
        def inherited_cjk_font(element: ET.Element) -> bool:
            current: ET.Element | None = element
            while current is not None:
                if "Noto Sans CJK JP" in current.attrib.get("font-family", ""):
                    return True
                current = parents.get(current)
            return False
        for el in root.iter():
            if el.tag == SVG_NS + "image":
                errors.append(f"P{page:02d}: external <image> can render blank; inline vectors instead")
            if el.tag == SVG_NS + "text":
                body = "".join(el.itertext()).strip()
                if body:
                    texts.append(body)
                    if JP.search(body) and not inherited_cjk_font(el):
                        errors.append(f"P{page:02d}: missing Noto CJK font on Japanese text {body!r}")
        content = "\n".join(texts)
        for token in REQUIRED[page]:
            if token not in content:
                errors.append(f"P{page:02d}: required story text missing: {token!r}")
        if page in (20, 21, 27) and "M147 151L123 182" not in file.read_text(encoding="utf-8"):
            errors.append(f"P{page:02d}: missing characteristic P19 hinge fracture")
    return errors


def main() -> int:
    errors = run()
    for error in errors:
        print("ERROR", error, file=sys.stderr)
    if errors:
        print(f"FAIL: {len(errors)} error(s)", file=sys.stderr)
        return 1
    print("PASS: 32 SVG pages parse, required dialogue/reveals are present, no missing CJK fonts or external-image dependencies")
    print("NOTE: A passing lint does not establish visual quality or final acceptance.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
