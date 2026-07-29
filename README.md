# mitsubachi-docs

## 導入方法

使い方は2通りあります。どちらの場合も、AI には「**まず [design-system/AGENTS.md](./design-system/AGENTS.md) を読むこと**」と伝えてください。読む順序・作業手順・守るべきルールはすべてそこに書いてあります。

### ① URL を指定して参照させる

チャット型の AI（Claude.ai など）で使う場合。リポジトリの URL を渡して参照させます。

```
https://github.com/uzabase/mitsubachi-docs
```

指示の例:

```
https://github.com/uzabase/mitsubachi-docs を参照して、
design-system/AGENTS.md のルールに従ってモックを作ってください。
mockup パターンで、design-system/mockup-kit/ の CSS を使うこと。
```

> プライベートリポジトリのため、AI 側にアクセス権が無い場合は②のローカル参照を使ってください。

### ② ローカルにダウンロードして参照させる

コーディングエージェント（Claude Code / Cursor など）で使う場合。手元にクローンして、そのディレクトリで作業させます。

```bash
git clone git@github.com:uzabase/mitsubachi-docs.git
```

- **Claude Code**: リポジトリ内で起動すれば `design-system/CLAUDE.md` → `AGENTS.md` が自動で読まれます。別プロジェクトから使う場合は、クローン先のパスを伝えてください
- **Cursor**: `.cursor/rules` に「`<クローン先>/design-system/AGENTS.md` を参照する」旨と、使用するパターン（後述）を書いておきます
- **モックの HTML から CSS を読み込む場合**: `design-system/mockup-kit/tokens.css` → `mitsubachi-mockup.css` の順でリンクします

最新の状態を保つため、使う前に `git pull` してください。

### 使い方のパターンを指定する

mitsubachi-ui は出力するコードの種類によって3つのパターンがあります。**どれを使うかは利用環境側で指定**してください（AGENTS.md 自体は環境非依存のため、そこでは固定していません）。

| パターン | 出力 | 使う場面 |
|---|---|---|
| **mockup** | 見た目だけを再現した HTML（パッケージ非依存） | AI によるモック生成 |
| **react** | mitsubachi-ui-react を使った React コード | React プロジェクトでの実装 |
| **web-component** | `<mi-*>` タグを使った HTML | Web Components が動く環境での実装 |

## できあがったモックを検査する

AI が作ったモックは、クラスの誤用・kit を使わない自作・独自 CSS での見た目づくりを機械的に検査できます。

```bash
python3 tools/check-mockup.py <モックのファイル.html>
```

error が 0 なら kit のルールに沿っています。検査の中身と `ds-exception`（kit に無い UI を作る場合の申告）の書き方は [design-system/AGENTS.md](./design-system/AGENTS.md) を参照してください。

## リポジトリ構成

```
├── README.md            ← このファイル（人間向けの導入方法）
├── AGENTS.md            ← AI 向けの入口ポインタ
├── CLAUDE.md            ← AGENTS.md への薄いポインタ
├── tools/
│   ├── check-mockup.py       ← 作ったモックの検査
│   ├── check-kit.py          ← kit の整合性チェック（保守用）
│   └── build-kit-index.py    ← kit-index.json の生成（保守用）
└── design-system/
    ├── AGENTS.md               ← AI 向けの指示の本体
    ├── CLAUDE.md               ← AGENTS.md への薄いポインタ
    ├── README.md               ← ドキュメント集としての概要
    ├── component-selection.md  ← やりたいこと → 何を使うかの逆引き
    ├── foundations/            ← デザインの基盤（11ファイル）
    ├── components/             ← 各 UI パーツのルール（75ファイル）
    └── mockup-kit/             ← AI の生成エンジン向けアセット（CSS・JS・見本・雛形・索引）
```

ルートの `AGENTS.md` / `CLAUDE.md` は、エージェントがリポジトリのルートで起動しても入口を見つけられるようにするためのポインタです。指示の本体は `design-system/AGENTS.md` にあります。

役割は3層に分かれています。

| 層 | 場所 | 中身 | 値を持つか |
|---|---|---|---|
| **ルール層** | `foundations/` | 色・余白・タイポグラフィ・設計原則・アクセシビリティなど、**使い分けの判断基準** | 持たない（具体値は Figma / トークンリポジトリが正） |
| **ルール層** | `components/` | 各コンポーネントの使い分け・Do/Don't・Figma URL・kit への導線 | 持たない |
| **ルール層** | `component-selection.md` | やりたいことからコンポーネントを選ぶ判断基準（逆引き） | 持たない |
| **アセット層** | `mockup-kit/` | `.mi-*` クラスの CSS・挙動 JS・見本 HTML・テンプレート・索引。**AI がクラスを当てるだけで正しい見た目になる** | 持つ（Figma のスナップショット） |

`mockup-kit/` の中身:

| ファイル | 役割 |
|---|---|
| `CHEATSHEET.md` | 全クラス・併用規則の1枚まとめ |
| `kit-index.json` | 機械可読の索引（必須修飾子・併用規則・必須属性・アイコン名一覧）。**自動生成・手編集しない** |
| `tokens.css` | 値の単一の源（CSS 変数）。**手編集しない**（Figma から取り直す） |
| `mitsubachi-mockup.css` | `.mi-*` クラス本体。値は `tokens.css` を参照 |
| `mitsubachi-mockup.js` | 最小の挙動（タブ・メニュー・ダイアログ・snackbar・行選択・ソート）。任意読み込み |
| `mitsubachi-icons.css` | 公式アイコン全97種（容量が大きいため分離・任意読み込み） |
| `mitsubachi-logos.css` | 公式ロゴ SVG（同上） |
| `components/*.html` | コンポーネント見本。ブラウザで開いて見た目を確認できる |
| `templates/` | `starter.html`（新規モックの雛形）、`error-403.html` / `error-404.html` / `error-500.html`（そのまま使えるエラーページ） |

詳細は [design-system/mockup-kit/README.md](./design-system/mockup-kit/README.md) を参照してください。

## 値の正・鮮度

- **値の正は常に Figma。** 優先順位は `Figma MCP > mitsubachi-token > mockup-kit のスナップショット`
- md にトークン値をハードコードしない（Figma 側の変更と乖離するため）
- `mockup-kit/tokens.css` は Figma を機械的に写したスナップショットなので、上記の原則とは矛盾しません

## 関連リポジトリ

- [mitsubachi-ui](https://github.com/uzabase/mitsubachi-ui) — Web Components / [Storybook](https://uzabase.github.io/mitsubachi-ui/)
- [mitsubachi-ui-react](https://github.com/uzabase/mitsubachi-ui-react) — React 版（プライベート） / [Storybook](https://uzabase.github.io/mitsubachi-ui-react/)
- [mitsubachi-token](https://github.com/uzabase/mitsubachi-token) — デザイントークン
