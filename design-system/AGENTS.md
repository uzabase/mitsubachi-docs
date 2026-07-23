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
| `foundations/` | デザインの基盤（トークン・原則・アクセシビリティ・Do/Don't） |
| `components/` | 各UIパーツの使い分け・Do/Don't・Figma URL |

### foundations/

| ファイル | 内容 |
|---|---|
| `primitive-token.md` | Dimension・Typography のベース値 |
| `spacing.md` | 余白トークン（2px〜80px） |
| `border-radius.md` | 角丸トークン（2px〜8px） |
| `icon-size.md` | アイコンサイズ（14px〜66px） |
| `elevation.md` | 影・グラデーション（検討中） |
| `typography.md` | フォントサイズ・ウェイト |
| `color.md` | 色の使い分けルール |
| `principles.md` | 設計原則（一貫性・階層・余白） |
| `accessibility.md` | アクセシビリティの横断ルール |

## 使い方の3パターン

mitsubachi-ui は、出力するコードの種類によって3つのパターンで使われます。

| パターン | 出力 | 使われる場面 |
|---|---|---|
| **react** | mitsubachi-ui-react を使った React コード | React プロジェクトでの実装 |
| **web-component** | mitsubachi-ui の `<mi-*>` タグを使ったHTML | Web Component が動く環境での実装 |
| **mockup** | 見た目だけを再現したコード（パッケージ非依存） | AIによるモック生成（Claude.ai、Cursor 等） |

**どのパターンを使うかは利用環境側で指定してください**（例: Claude.aiの手順欄、Cursorの`.cursor/rules`等）。AGENTS.md自体は環境非依存のため、ここでパターンを固定しません。

### デザイントークンの取得

コンポーネントの実装・モック作成時に、色・角丸・スペーシング・フォント・シャドウなどのデザイントークンの具体値が必要な場合は、Figma MCP の `get_variable_defs` を使用してコンポーネントの node から取得してください。

```
get_variable_defs(fileKey, nodeId)
```

- 各コンポーネントの `nodeId` は、対応する md ファイルの `## Figma` セクションの URL から取得できる
- 返却されるトークンには色（`surface/*`, `border/*`, `text/*`）だけでなく、角丸（`*px`）、タイポグラフィ（`label/*`）、シャドウ（`focus-ring`）なども含まれる
- `foundations/` 配下の md ファイルはトークンの **使い分けルール** を記述したもので、具体値は含まない。具体値は常に Figma MCP またはトークンリポジトリ（[mitsubachi-token](https://github.com/uzabase/mitsubachi-token)）を正とする
- md にトークン値をハードコードしない（Figma 側の変更と乖離するため）

### 各パターンの参照先

- **react**: [mitsubachi-ui-react (プライベート)](https://github.com/uzabase/mitsubachi-ui-react) / [Storybook](https://uzabase.github.io/mitsubachi-ui-react/)
- **web-component**: [mitsubachi-ui](https://github.com/uzabase/mitsubachi-ui) / [Storybook](https://uzabase.github.io/mitsubachi-ui/)
- **mockup**: パッケージ非依存。コンポーネントを**自作せず** [mockup-kit/](./mockup-kit/) の kit を使う。**まず [mockup-kit/CHEATSHEET.md](./mockup-kit/CHEATSHEET.md) を読む**（全クラスの当て方と間違えやすい併用規則の1枚まとめ）。新規モックは `mockup-kit/templates/starter.html` をコピーして組み立てる。`mockup-kit/tokens.css` と `mockup-kit/mitsubachi-mockup.css` を読み込み、`.mi-*` クラスを当てて組み立てる（例: `<button class="mi-button mi-button--primary mi-button--large">保存する</button>`）。複合画面（ダッシュボード等）でも各パーツは kit のクラスで組むこと。対応コンポーネントとクラス一覧は [mockup-kit/README.md](./mockup-kit/README.md) を参照。ボタン系（neutral / danger / ai / icon / floating）・入力系（text-field / text-area / select-box / checkbox / radio / switch / search-box / segmented-control / filter-chip）・ナビ系（tab / breadcrumb / pagination / menu）・表示系（table / tag / badge / avatar / card / label-unit / loading / logo）・通知系（dialog / tooltip / snackbar / inline-notification / banner / icon-color）・layout・icon（全97種。`mockup-kit/mitsubachi-icons.css` を追加読み込み）に対応。対応一覧は [mockup-kit/README.md](./mockup-kit/README.md) を参照（未対応コンポーネントの値は従来どおり Figma MCP で取得）。**構造が深いコンポーネント（table / layout / dialog / menu / ai-chat / timeline / suggestion）は、組む前に `mockup-kit/components/` の同名見本 HTML を読んでマークアップ構造（入れ子・aria 属性・列クラスの付け場所）を踏襲する**（クラス名だけで組むと構造を誤りやすい。フラットな部品はクラスを当てるだけでよい）。