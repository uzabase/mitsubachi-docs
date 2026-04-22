# mitsubachi-ui デザインシステム

> **このファイルを最初に読んでください。**

## このドキュメントについて

このドキュメント群は、デザインシステム **Speeda 3.1 MITSUBACHI** に基づいた画面を作るためのデザインルール集です。以下、**mitsubachi-ui** と呼びます。

### 対象プロダクト
- **Speeda** — 企業・業界・市場の情報を横断して調べられる統合経済情報プラットフォーム。経営企画・事業開発・営業/マーケティングなどの調査や意思決定を支援する
- **Speeda AI Agent** — Speeda 上で企業分析・調査・比較・要約などの作業を AI で効率化するプロダクト

色の意味・パーツの使い分け・レイアウトのルールなど、守るべきデザインの仕様を定義しています。

### mitsubachi-ui の構成

| リポジトリ | 役割 |
|-----------|------|
| **このリポジトリ（docs）** | AI がデザインシステムを使うためのデザインルール・仕様 |
| [mitsubachi-ui](https://github.com/uzabase/mitsubachi-ui) | Web Component のコンポーネント群 |
| [mitsubachi-ui-react](https://github.com/uzabase/mitsubachi-ui-react) | React のコンポーネント群 |
| [mitsubachi-token](https://github.com/uzabase/mitsubachi-token) | デザイントークン（色・余白・タイポグラフィ等の具体値） |

### 目的

このドキュメントは **AI がデザインシステムに従った画面を作る** ときに使う。モックアップ作成、実装、レビューなど、mitsubachi-ui に基づく作業全般が対象。

### 画面の作成方法

以下の 3 つのモードから 1 つを選ぶ。

| モード | 説明 | 使える環境 |
|--------|------|-----------|
| **react** | mitsubachi-ui-react の React コンポーネントを使って画面を作る | React プロジェクト |
| **web-component** | mitsubachi-ui の Web Component を使って画面を作る | Web Component が動く環境 |
| **html** | 素の HTML + CSS で、デザイン仕様に従って画面を作る | Claude AI / Claude Design など |

**現在のモード: `html`**

> モードを切り替えるには、上の行の値を `html`、`react`、または `web-component` に変更してください。

#### react モードについて

- [GitHub リポジトリ（プライベート）](https://github.com/uzabase/mitsubachi-ui-react)
- [Storybook](https://uzabase.github.io/mitsubachi-ui-react/)

#### web-component モードについて

- [GitHub リポジトリ](https://github.com/uzabase/mitsubachi-ui)
- [Storybook](https://uzabase.github.io/mitsubachi-ui/)

---

## ドキュメント構成

| ファイル | 内容 |
|---------|------|
| **このファイル** | 全体像・ドキュメント構成・モード選択 |
| `foundations/` | デザインの基盤となるトークン・ルール・設計原則・アクセシビリティ・Do/Don't |
| `components/` | 各 UI パーツのデザイン仕様・使い分け・Do/Don't |

### foundations/

| ファイル | 内容 |
|---------|------|
| `primitive-token.md` | Dimension・Typography のベース値 |
| `spacing.md` | 余白トークン（2px〜80px） |
| `border-radius.md` | 角丸トークン（2px〜8px） |
| `icon-size.md` | アイコンサイズ（14px〜66px） |
| `elevation.md` | 影・グラデーション（検討中） |
| `typography.md` | フォントサイズ・ウェイト |
| `color.md` | 色の使い分けルール |
| `principles.md` | 設計原則（一貫性・階層・余白） |
| `accessibility.md` | アクセシビリティの横断ルール |
