# 第1話・完成判定の進捗（2026-10-17）

**結論：完成原稿としての採用はまだ0/32ページ。** ただし読書検証用の32ページ全てがリポジトリに存在する。

| 工程 | 状況 | 根拠 |
| --- | --- | --- |
| 第1話脚本・32ページの構成 | 作成済み | [脚本](../../../../scripts/episode-01.md) |
| 仕上げ試作 | 32/32ページ | [読書検証版](reader.md) |
| 説明字幕の整理 | 20ページの別案作成済み | [台詞整理レビュー](../review-2026-10-15-dialogue-pass.md) |
| 作中台詞とページ送りの重要点 | 照合済み | [自動チェック](../../../../../tools/check_episode01_story.py) |
| 構図・SVGの存在と基本構造 | 静的検査済み | [検証スクリプト](../../../../../tools/build_readproof.py) |
| PNG・コンタクトシート・PDF書き出し | **成功・確認済み** | [実行 #38938518724](https://github.com/hansuoi/story-gods-ai/actions/runs/38938518724) |
| 32ページのレンダリング画像を通読 | **初回目視を実施。重要な作画不備を検出** | [2026-10-17実画面レビュー](visual-review-2026-10-17.md) |
| 人物の識別・表情・手指・遠近・文字組みの清書 | **未完了** | 目視確認と再作画が必要 |
| 完成版の最終採用 | **0/32ページ** | 上記の未完了工程が残る |

## 今回の主な原稿修正

P14：安希は捜査員に資料を見つけたことを告げ、写しの提供を申し出る。

P15：安希は『誰に会ったか、自分で確かめる』と自分から現場へ向かう。ただしP16で保全区域へは入らない。

P31：依頼者名の反復を削り、『調査対象：神谷榊』の開示を際立たせる。

P32：同じ書類名の再掲を削り、無言電話に答える安希の台詞を結末の中心にする。

## 出力結果を確認する方法

GitHubの [Episode 01 PDF and image proof](https://github.com/hansuoi/story-gods-ai/actions/workflows/episode01-proof.yml) で実行結果を確認する。成功した実行があれば `episode01-reading-proof` という成果物に `episode01-reading-proof.pdf`、`contact-sheet.png`、個別PNG32枚が含まれる。

**2026-10-17にCI実行と実際のページ画像を確認済み。** なお、画像生成の成功・SVG構造の妥当性は人物の画力・読書体験の合格を意味しない。完成採用は依然0/32ページ。

## 2026-10-17 夜の追加作業: P29〜P31

GitHubのコミット・CI・実際のPNGを分けて評価する。既存の完成採用 0/32ページという判定は変更しない。

| ページ | 原稿の変更 | 検証の根拠 | 完成採用 |
| --- | --- | --- | --- |
| P29 | 安希の手で封筒から資料を取り出す構図を修正 | [コミット 4ad35e7](https://github.com/hansuoi/story-gods-ai/commit/4ad35e753ba6cad7f3856322b96b87897e97c36c)・[CI](https://github.com/hansuoi/story-gods-ai/actions/runs/39025680266) | 未採用 |
| P30 | 3コマ目に資料を持つ手と机上の紙束を描き直し、4コマ目で手が調査対象欄を覆う構図に変更 | [コミット b3ea9f1](https://github.com/hansuoi/story-gods-ai/commit/b3ea9f1c1e94666474e15993628b7478fb70361a)・[CI成功](https://github.com/hansuoi/story-gods-ai/actions/runs/39032104923)・生成PNG目視済み | 未採用 |
| P31 | 2コマ目に綴じ穴と破れた紙の縁を追加。4コマ目に途中で途切れた記載と手を描き直し、1・3コマ目の手と表情も修正 | [コミット b9d3abb](https://github.com/hansuoi/story-gods-ai/commit/b9d3abb0c2761b258ef7a7e4c7eab80d32fb27f1)、[97917ea](https://github.com/hansuoi/story-gods-ai/commit/97917ea27d77755fa068ef2b9fc18c1ca218394c)、[2e31edd](https://github.com/hansuoi/story-gods-ai/commit/2e31eddf733f5e65d2b8861deca60c5e6e0e64b5)・[CI](https://github.com/hansuoi/story-gods-ai/actions/runs/39032264548)。最終コミットの[CI成功](https://github.com/hansuoi/story-gods-ai/actions/runs/39032264548)とPNG目視を確認済み。手は資料右側に移動したが人物作画は未完 | 未採用 |

### 実際のPNGから判明した未解決の問題

- P30: 書類を持つ手の位置は読み取れるようになったが、安希の頭部・目・体と室内背景が単純な図形であり、完成漫画の人物作画には達していない。
- P31: 紙の破れと綴じ穴の表現を確認できたが、書類から1枚が抜かれた事実が一見して明確とは言い切れない。安希の表情・手指と読書体験も未達。
- P29〜31: 同じ資料・同じ人物の連続した動作として自然に読めるか、32ページを通して再確認する必要がある。
- 今回作成したSVGのレンダリング成功は完成採用を意味しない。描き直しと目視検査を継続する。


## 2026-10-17 追加清書: P06〜08

ページの作画修正とレンダリングを実施。完成品質への採用は引き続き **0/32ページ**。

| ページ | 実際の原稿変更 | 検証結果 | 完成判定 |
| --- | --- | --- | --- |
| P06 | 榊の閉眼・顔の輪郭・髪を清書。葬儀担当者の顔を描き分け、安希が榊に触れる寸前で指を止める最後のコマを再構成 | [顔・担当者の修正](https://github.com/hansuoi/story-gods-ai/commit/0fcd9b8651f7d5256f2f61022d96e555f9ee6dfc)、[接触直前の構図修正](https://github.com/hansuoi/story-gods-ai/commit/a086317c5ea51b8fa9145c599850785e6223f652)、[最新CI成功・PNG目視済み](https://github.com/hansuoi/story-gods-ai/actions/runs/39036066963) | 未採用 |
| P07 | 棺に横たわる榊の顔の大ゴマと、安希が『別の人みたい』と感じる顔・喪服・手のコマを描き直し | [修正コミット](https://github.com/hansuoi/story-gods-ai/commit/67dcaadcb5f8032d95bed2daccc47c5aca4eb2da)、[CI成功・PNG目視済み](https://github.com/hansuoi/story-gods-ai/actions/runs/39035796183) | 未採用 |
| P08 | 安希が警察に反論する最終コマの顔・姿勢・手を描き直し。初回の閉眼に見える描線を開眼へ修正 | [姿勢・顔](https://github.com/hansuoi/story-gods-ai/commit/5fcbe09cd1405db1cfa2b359bee8ecf3c6d771b0)、[開眼](https://github.com/hansuoi/story-gods-ai/commit/ebae1f85fdd16dbb2b6ed834559b83251c9029cc)、[最新CI成功・PNG目視済み](https://github.com/hansuoi/story-gods-ai/actions/runs/39036401816) | 未採用 |

### PNG目視後の残課題

- P06: 榊の顔はP07と近づいたが、髪・頬・目・枕の遠近には単純化が残る。手と頬の距離は描いたが、自然な身体動作として再確認が必要。
- P07: 榊の髪型と閉眼の連続性は改善。顔・首・棺の透視と安希の手の解剖学的表現には清書が残る。参列者の人物描写は簡略的。
- P08: 最終コマで安希が目を開けて刑事に向き合う表情を確認。前半3コマの人物作画と面談室の空間表現は依然として簡略的。
- 全32ページの最終通読・人物の統一・視線や動作の連続性の検証は未完了。レンダリング成功や部分的な修正を完成採用数に加えない。

## 2026-10-17 追加清書: P01

P01最終コマの榊のシャツ・両腕・ズボン・革靴を描き直した。顔を見せないという脚本上の制約は維持した。

- 原稿コミット: [89a4efa](https://github.com/hansuoi/story-gods-ai/commit/89a4efa53edfc9f319f842e84062e3c9ea146d63)
- PNG/PDFの書き出し: [CI #39036626178 成功](https://github.com/hansuoi/story-gods-ai/actions/runs/39036626178)
- 実際のP01 PNGを目視済み: シャツの襟・左右の袖、独立した両脚、前へ出した靴と水しぶきを確認。
- 残課題: 救助員が直立していて扉をこじ開ける緊迫した動作が弱い。少年と扉の距離、腕の位置、階段と水位の遠近、画面全体の人体作画を清書する。
- 完成採用: **未採用**。全32ページの完成採用数は **0/32ページ**。
