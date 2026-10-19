#!/usr/bin/env python3
"""Upload existing episode-01 PNG artwork with Git, preserving original bytes.

Run in a local clone with GitHub push access:
  python scripts/upload_episode01_png.py /path/to/kamiya_ep01_p07_lettered_v03.png 7
No extra API subscription required. Never converts the image to SVG.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = Path("docs/art/episode-01/finish/color-png")

def git(*args: str) -> None:
    subprocess.run(["git", "-C", str(ROOT), *args], check=True)

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("page", type=int)
    parser.add_argument("--no-push", action="store_true", help="Commit only; do not push")
    args = parser.parse_args()
    if not 1 <= args.page <= 32:
        parser.error("page must be 1..32")
    src = args.source.resolve()
    data = src.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        parser.error("source must be a PNG")
    target = ROOT / DEST / f"p{args.page:02d}.png"
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, target)
    assert target.read_bytes() == data, "PNG copy failed"
    manifest_path = ROOT / DEST / "sha256.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {}
    manifest[target.name] = {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data), "source_name": src.name}
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    git("add", str(target.relative_to(ROOT)), str(manifest_path.relative_to(ROOT)))
    git("commit", "-m", f"art(ep01): upload original P{args.page:02d} PNG")
    if not args.no_push:
        git("push", "origin", "HEAD")
    print(f"Saved {target.relative_to(ROOT)} SHA256={manifest[target.name]['sha256']}")

if __name__ == "__main__":
    main()
