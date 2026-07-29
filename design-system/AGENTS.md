# mitsubachi-ui デザインシステム

> このファイルは AI（Claude等）が mitsubachi-ui に基づく作業を行うときに最初に読むファイルです。
> 人間向けの概要は [README.md](./README.md) を参照してください。

## 目的

mitsubachi-ui に基づくモック作成・実装・レビューを行う AI が、デザインシステムの構造とルールを把握するための入口です。

## 対象プロダクト

このデザインシステムは以下のプロダクトで使われています：

- **Speeda** — 企業・業界・市場の情報を横断して調べられる統合経済情報プラットフォーム。経営企画・事業開発・営業/マーケティングなどの調査や意思決定を支援する
- **Speeda AI Agent** — Speeda 上で企業分析・調査・比較・要約などの作業を AI で効率化するプロダクト

## ドキュメント構成

| 場所 | 内容 |
|---|---|
| `foundations/` | デザインの基盤（トークン・原則・文言・Do/Don't） |
| `components/` | 各UIパーツの使い分け・Do/Don't・Figma URL |
| `component-selection.md` | **やりたいこと → 何を使うか**の逆引き（選定の判断基準） |
| `mockup-kit/` | mockup パターン用のアセット（CSS・見本・雛形・索引・挙動 JS） |

### foundations/

| ファイル | 内容 |
|---|---|
| `primitive-scale.md` | Dimension・Typography のベース値 |
| `spacing.md` | 余白トークン（2px〜80px） |
| `border-radius.md` | 角丸トークン（2px〜8px） |
| `icon-size.md` | アイコンサイズ（14px〜66px） |
| `elevation.md` | 影・グラデーション（検討中） |
| `typography.md` | フォントサイズ・ウェイト |
| `color.md` | 色の使い分けルール |
| `principles.md` | 設計原則（印象・トーン・一貫性） |
| `prohibited.md` | 禁止事項（カラー等の逸脱パターン） |
| `layout.md` | 汎用レイアウト（2カラムのアプリケーションシェル） |
| `writing.md` | 文言のルール（ボタン・エラー・空状態・数値表記） |

## 使い方の3パターン

mitsubachi-ui は、出力するコードの種類によって3つのパターンで使われます。

| パターン | 出力 | 使われる場面 |
|---|---|---|
| **react** | mitsubachi-ui-react を使った React コード | React プロジェクトでの実装 |
| **web-component** | mitsubachi-ui の `<mi-*>` タグを使ったHTML | Web Component が動く環境での実装 |
| **mockup** | 見た目だけを再現したコード（パッケージ非依存） | AIによるモック生成（Claude.ai、Cursor 等） |

**どのパターンを使うかは利用環境側で指定してください**（例: Claude.aiの手順欄、Cursorの`.cursor/rules`等）。AGENTS.md自体は環境非依存のため、ここでパターンを固定しません。

- **react**: [mitsubachi-ui-react (プライベート)](https://github.com/uzabase/mitsubachi-ui-react) / [Storybook](https://uzabase.github.io/mitsubachi-ui-react/)
- **web-component**: [mitsubachi-ui](https://github.com/uzabase/mitsubachi-ui) / [Storybook](https://uzabase.github.io/mitsubachi-ui/)
- **mockup**: 下の「mockup パターンの作業手順」に従う

---

# mockup パターンの作業手順

**大原則**: コンポーネントを**自作しない**。色・寸法を**直書きしない**。`.mi-*` クラスを当てるだけ。

## A. 新しい画面を作る

1. **[mockup-kit/CHEATSHEET.md](./mockup-kit/CHEATSHEET.md) を読む** — 全クラスの当て方と間違えやすい併用規則の1枚まとめ
2. **`mockup-kit/templates/starter.html` をコピー**して組み立てる（CSS の読み込み順と app shell の骨格が入っている）
   - エラーページ（403 / 404 / 500）は `mockup-kit/templates/error-*.html` を**そのまま使う**（自作しない）
3. **何を使うか迷ったら [component-selection.md](./component-selection.md)** — 「絞り込みたい」「知らせたい」から候補と選定基準を引く
4. **構造が深い7種（table / layout / dialog / menu / ai-chat / timeline / suggestion）は、組む前に `mockup-kit/components/` の同名見本 HTML を読む** — 入れ子・aria 属性・列クラスの付け場所をクラス名だけで推測すると誤る。フラットな部品はクラスを当てるだけでよい
5. **文言は [foundations/writing.md](./foundations/writing.md) に従う** — ボタンは動詞（「保存する」）、値が無いセルは「–」など
6. **触れるモックにするなら `mockup-kit/mitsubachi-mockup.js` を読み込む**（独自 JS を書かない）— タブ・メニュー・ダイアログ・snackbar・行選択・ソートが `data-mi-*` の宣言で動く。見本 `mockup-kit/components/interactive.html`
7. **最後に必ずセルフチェックを実行し、error が 0 になるまで直す**

   ```bash
   python3 tools/check-mockup.py <作ったファイル.html>
   ```

   4つの層で検査する: 層0 = クラスの使い方（存在しないクラス・必須修飾子の欠落・幻覚アイコン名・ベースフォント未指定＝地の文の明朝体化）/ 層1 = kit に等価物があるタグを素で使っていないか / 層2 = 未申告の逸脱（独自クラスや style 属性で見た目を書いていないか）/ 層3 = レビュー材料の列挙

## B. 既存のモックを直す

1. 直す対象のファイルをまず `tools/check-mockup.py` に通し、**今の状態の指摘を把握する**
2. 変更を加える（構造を変えるなら該当する見本 HTML を読み直す）
3. 再度セルフチェックし、**新たな error を増やしていないこと**を確認する

## C. モックをレビューする

1. `tools/check-mockup.py <ファイル>` を実行する（機械で分かる逸脱はここで尽きる）
2. 層3の「レビュー材料」を見る — `ds-exception` で申告された DS 外の箇所、独自クラス、構造見本を読むべきコンポーネントが列挙される
3. 機械で分からない点を `foundations/principles.md`・`component-selection.md`・`foundations/writing.md` に照らして確認する

## kit に無い UI が必要になったとき

日付選択・アコーディオン・グラフなどは kit にありません。対応は**どう指示されたか**で分かれます。

**① ユーザーが明示的に新規コンポーネントを指示した場合**（「日付選択を作って」など）
→ **代替の検討は不要。そのまま作ってよい**。既存部品での代替案を提案して回り道しないこと。下記の申告だけ書きます。

**② 組み立てる途中で「kit に無い」と気づいた場合**（ユーザーは指定していない）
→ まず既存の部品で代替できないか検討します（[component-selection.md の 9.](./component-selection.md)）。それでも必要なら作り、申告を書きます。

### 申告の書き方

**CSS** は `<style>` 内の該当箇所の直前に1行。**そのブロックの以降のルールがまとめて免除される**ので、コンポーネント1つにつき1行で足ります。

```css
/* ds-exception: date picker は mitsubachi-ui に無いためユーザー指示で新規作成 */
.datepicker { ... }
.datepicker__day { ... }
```

**HTML** は要素の直前に1行。**その要素と子孫が免除されます**。

```html
<!-- ds-exception: date picker は mitsubachi-ui に無いため -->
<div class="datepicker">...</div>
```

申告があれば層2の指摘は出ず、**層3のレビュー材料に残ります**（申告の無い逸脱は error）。層3に残るのは「デザインシステムに無いものを作った」記録で、後から kit に取り込むかを判断する材料になります。

## クラスの正確な情報を引く（kit-index.json）

`mockup-kit/kit-index.json` は CSS と見本 HTML から自動生成された機械可読の索引です。**3116 行の CSS を読まずに**次を引けます。

| 引きたいこと | キー |
|---|---|
| そのクラスに必須の修飾子（variant / size） | `components.<基底クラス>.requiredOneOf` |
| 単独では効かない修飾子と併用相手 | `components.<基底クラス>.compoundOnly` |
| 必須の属性・role・子要素 | `requiredAttrs` / `requiredRole` / `requiredParts` |
| 使える全アイコン名（97種）・ロゴ名 | `icons.extra` / `icons.builtin` / `logos` |
| そのタグに必ず付けるクラス | `tagRules` |
| 構造見本を読むべきコンポーネント | `requiresSample` |

kit を編集したら `python3 tools/build-kit-index.py` で再生成します（手編集しない）。

## デザイントークンの取得

コンポーネントの実装・モック作成時に、色・角丸・スペーシング・フォント・シャドウなどのデザイントークンの具体値が必要な場合は、Figma MCP の `get_variable_defs` を使用してコンポーネントの node から取得してください。

```
get_variable_defs(fileKey, nodeId)
```

- 各コンポーネントの `nodeId` は、対応する md ファイルの `## Figma` セクションの URL から取得できる
- 返却されるトークンには色（`surface/*`, `border/*`, `text/*`）だけでなく、角丸（`*px`）、タイポグラフィ（`label/*`）、シャドウ（`focus-ring`）なども含まれる
- `foundations/` 配下の md ファイルはトークンの **使い分けルール** を記述したもので、具体値は含まない。具体値は常に Figma MCP またはトークンリポジトリ（[mitsubachi-token](https://github.com/uzabase/mitsubachi-token)）を正とする
- md にトークン値をハードコードしない（Figma 側の変更と乖離するため）
- mockup パターンでは `mockup-kit/tokens.css`（Figma のスナップショット）が値を持つため、通常は Figma MCP を呼ぶ必要はない。**kit に未収録のコンポーネント**の値が必要なときだけ取得する（対応一覧は [mockup-kit/README.md](./mockup-kit/README.md)）
