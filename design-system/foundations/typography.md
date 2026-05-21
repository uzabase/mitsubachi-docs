# typography

フォント・文字サイズ・行間・字間に関するトークンとルール。

> 具体的な値は Figma MCP（`get_variable_defs`）または [mitsubachi-token](https://github.com/uzabase/mitsubachi-token) を参照。

## フォント選定

Figma と実装は欧文を Arial に揃える。

| 項目 | macOS・iOS | Windows |
|------|-----------|---------|
| 和文 | Hiragino Sans / Hiragino Kaku Gothic | Meiryo |
| 欧文 | Arial | Arial |

## font-family

- 基礎値: `Arial, YakuHanJPs, Hiragino Sans, Hiragino Kaku Gothic ProN, Meiryo, Noto Sans JP, sans-serif`
- 日本語（`:lang(ja)`）・英語（`:lang(en)`）: weight を `bold:600, normal:300` に調整（Hiragino Sans の weight 400 が太字すぎるため）
- 中国語（`:lang(zh)`）: `PingFang SC`, `Microsoft YaHei` 等を使用。weight は `bold:700, normal:400`

## font-scale

- [primitive-scale](./primitive-scale.md) の font-scale（14px 基準の Major Second Type Scale）を参照する

## line-height

| 値 | 対象フォントサイズ | ルール・意図 |
|----|-----------------|-------------|
| **130%** | 小さいサイズ（〜14px） | 高さを抑えたいコンポーネント用。改行時に情報の塊感を維持する |
| **130%** | 大きいサイズ（20px〜） | 大きいサイズで文字が散らばって見えるのを防ぐ |
| **150%** | 中間サイズ（12px〜18px） | 基本的な値 |
| **175%** | 読み物サイズ（14px・16px） | 文字の密集を軽減し、読了感を高める |

## letter-spacing

| 値 | 分類 | 対象フォントサイズ | ルール・意図 |
|----|------|-----------------|-------------|
| **2%** | text | 12px〜16px | 読み物コンテンツの「文字文字しさ」を軽減する |
| **1%** | label / headline | 10px〜16px | 視認性を確保しつつ少し広めに留める |
| **-1%** | headline | 20px〜24px | 情報の塊感を出すために少し詰める |
| **-2%** | headline | 25px〜32px | 間延びを防ぎ、情報の塊感を出す |

## font-weight

| | headline | label・text |
|---|---------|------------|
| **normal (400)** | 必要なもののみ用意 | 全 font-size / line-height の組み合わせで展開 |
| **bold (700)** | 必要なもののみ用意 | 全 font-size / line-height の組み合わせで展開 |

- headline: 使用用途が決まっているため限定的に展開
- label・text: 今後使用する可能性が高いため網羅的に展開

## semantic-type-scale（headline / text / label の使い分け）

| | headline | text | label |
|---|---------|------|-------|
| **まとめると** | 見出し | 文章 | システムの操作・情報を整理する手がかり |
| **これは何か** | 情報の名前や構造を示す。何の話が始まるかを伝える | 詳しい内容を伝えてしっかり理解してもらう | 機能を識別する名札 / 情報を特定する属性データ / 入力を導くガイド |
| **言葉** | 体言止め・要約したタイトル | 文章・データの詳細。「。」が入る文章 | 動詞・短い名詞・単語 |
| **文字の量** | 数単語〜2行 | 複数行〜数段落（制限なし） | 数単語〜2行 |

### 判断に迷ったら

- **headline**: それが消えたら何の塊（ページやセクション）かわからなくなる看板
- **text**: ユーザーへのメッセージや内容を理解してもらうための文章
- **label**: パッと見で判断できるもの、クリック時に実行される機能名、属性データ、入力を助けるガイド

### 迷いやすいポイント

| 項目 | 分類 | 説明 |
|------|------|------|
| 日付 | label | 形式が決まっており、UIを構成する固定的な枠組み |
| ページ番号 | label | 日付と同じ理由 |
| table th | label | 固定的な枠組み |
| ディスクレーマー | text | 読ませるための文章 |
| 混在時の判断 | — | メインの文章の一部であれば text、端的な補足であれば label |
