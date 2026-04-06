# mitsubachi-ui デザインシステム

> **このファイルを最初に読んでください。**

## このドキュメントについて

このドキュメント群は、デザインシステム**Speeda 3.1 MITSUBACHI** に基づいた画面を作るためのデザインルール集です。以下、**mitsubachi-ui**と呼びます。

色の意味・パーツの使い分け・レイアウトのルールなど、実装技術を問わず守るべきデザインの仕様を定義しています。

---

## ドキュメント構成

| ファイル | 内容 |
|---------|------|
| **このファイル** | 全体像・デザインの基本ルール |
| `foundations/` | カラー運用ルール、設計原則 |
| `components/` | 各 UI パーツのデザイン仕様・使い分け・コード例 |
| `prohibited.md` | **やってはいけないこと（必ず確認）** |

---

## デザインの基本ルール

### 色

| 用途 | 色 | 補足 |
|------|-----|------|
| 主要アクション（ボタン等） | 黒（`rgba(0,0,0,0.84)`） | 白文字と組み合わせる |
| 破壊的操作（削除等） | 赤（`#db351f`） | 白文字と組み合わせる |
| リンク・選択状態 | 青（`#315ce8` 系） | — |
| 見出しテキスト | ほぼ黒 | — |
| 本文テキスト | 濃いグレー | — |
| 補足テキスト | グレー | — |
| ボーダー・区切り線 | 薄いグレー | — |
| 成功 | 緑 | テキストやアイコンと併用する（色だけで伝えない） |
| 警告 | オレンジ | 同上 |
| エラー | 赤 | 同上 |

詳細は `foundations/color.md` を参照。

### 余白

4px 刻みのスケールを使う。関連する要素は近く、無関係な要素は遠く配置する。

| 値 | 主な用途 |
|-----|---------|
| 4px | アイコンとテキストの間 |
| 8px | インライン要素間、ボタン同士の間隔 |
| 12px | コンパクトなパディング |
| 16px | 標準的なパディング、フォーム要素間 |
| 24px | カード内のパディング |
| 32px | セクション間 |
| 48px | 大きなセクション間 |
| 64px | ページセクション間 |

### アイコン

このデザインシステムには独自のアイコンセットがある。

利用できるアイコン（抜粋）:

> `arrow-down`, `arrow-left`, `bell`, `bookmark`, `building`, `calendar`,
> `check`, `chevron-down`, `chevron-left`, `chevron-right`, `chevron-up`,
> `clock`, `copy`, `cross`, `download`, `error-fill`, `exit`, `eye`, `eye-slash`,
> `gear`, `history`, `home`, `information`, `kebab-menu`, `lock`, `magic`,
> `mail`, `menu`, `minus`, `money`, `open-in-new`, `pencil-square`,
> `person`, `person-add`, `plus`, `plus-circle`, `question-circle`,
> `search`, `share`, `success`, `unlock`, `warning-fill`

一覧にないものは使わない。近いものを仮で使い、要確認であることを注記する。

---

## 画面を組むときのルール

1. **`prohibited.md` を守る** — 非推奨のパターンを避ける
2. **アクセシビリティ** — アイコンだけのボタンにはラベルを付ける。色だけで情報を伝えない。プレースホルダーをラベルの代わりにしない
3. **各パーツの仕様は `components/` を確認する** — ボタンの種類、入力フィールドの使い方など

---

## 参考リンク

- [Storybook（コンポーネントの見た目を確認できる）](https://uzabase.github.io/mitsubachi-ui/)
- [GitHub リポジトリ](https://github.com/uzabase/mitsubachi-ui)
