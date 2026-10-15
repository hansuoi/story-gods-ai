# 読書検証版の画像書き出し・検査

第1話の[32ページ比較版](../docs/art/episode-01/finish/readproof/reader.md)を、ファイルの存在とXMLの妥当性を確認し、画像で読めるようにする補助スクリプト。

まず Python 3 の標準ライブラリだけで静的検査：

```bash
python tools/build_readproof.py
```

ページ画像と4列のコンタクトシートを生成する場合：

```bash
python -m pip install cairosvg Pillow
python tools/build_readproof.py --render
```

生成先は `build/readproof/`。ページごとのPNGと `contact-sheet.png` が作られる。コマのデジタル読書順はP01からP32、一覧図の同じ行では右から左。

**制限:** 実行時のSVG/XMLチェックやPNG書き出しは、絵の上手さ、人物の同一性、台詞の読みやすさ、演出を保証しない。画像の目視検証と読書テストが必要。スクリプトをリポジトリに追加することと、実際に描画テストを実行したことは別。

PDF用の32ページ書き出しと合わせて、物語上の重要な台詞の検査も実行する。

```bash
python tools/check_episode01_story.py
python tools/export_episode01.py --out build/episode01
```

GitHub Actions の [Episode 01 PDF and image proof](../.github/workflows/episode01-proof.yml) は、実行に成功するとPDF、32枚のPNG、一覧画像をアーティファクトとして保存する。**ワークフローを登録しただけでは実行成功の確認にはならない。**
