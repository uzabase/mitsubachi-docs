# mitsubachi-docs

mitsubachi-ui デザインシステムのドキュメント集。**人間と AI の両方が参照する「デザインシステムの素」**です。

AI（Claude / Cursor / ChatGPT など）にこのリポジトリを読ませることで、mitsubachi-ui に沿ったモック生成・実装・レビューができます。

## 導入方法

使い方は2通りあります。どちらの場合も、AI には「**まず `design-system/AGENTS.md` を読むこと**」と伝えてください。

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

## AI 向けの入口案内

AI が読む順序は決まっています。**上から順に辿れば、必要な情報にたどり着けます**。

1. **[design-system/AGENTS.md](./design-system/AGENTS.md)** — 最初に読むファイル。デザインシステムの構造・3つのパターン・**mockup の作業手順（新規／改修／レビュー）**
2. **[design-system/mockup-kit/CHEATSHEET.md](./design-system/mockup-kit/CHEATSHEET.md)** — mockup を作るなら次にこれ。全クラスの当て方と間違えやすい規則の1枚まとめ
3. **`design-system/mockup-kit/templates/starter.html`** — 新規モックはこの雛形をコピーして組み立てる
4. **[design-system/component-selection.md](./design-system/component-selection.md)** — 「絞り込みたい」「知らせたい」から**何を使うか**を引く逆引きガイド
5. **`design-system/components/<名前>.md`** — 使うコンポーネントの使い分け・Do/Don't。各 md に kit への導線（使うクラス名）が1行入っています
6. **`design-system/mockup-kit/components/<名前>.html`** — 構造が深いコンポーネント（table / layout / dialog / menu / ai-chat / timeline / suggestion）は、組む前にこの見本を読んでマークアップ構造を踏襲します
7. **`python3 tools/check-mockup.py <作ったファイル>`** — **作り終えたら必ず実行**。クラスの誤用・自作・未申告の逸脱を機械的に検出します（error が 0 になるまで直す）

> `design-system/CLAUDE.md` は Claude Code 互換のための薄いポインタで、中身は AGENTS.md を指しているだけです。

### AI の逸脱を止める仕組み

AI は「クラスを間違える」よりも「**kit を使わずに自作する**」「**独自 CSS で見た目を作る**」ことで世界観を壊します。これを機械的に止めるのが `tools/check-mockup.py` です。

| 層 | 何を見るか |
|---|---|
| 層0 | クラスの使い方（存在しないクラス・必須修飾子の欠落・単独では効かない修飾子・幻覚アイコン名・CSS の読み込み・ベースフォント未指定＝地の文の明朝体化） |
| 層1 | kit に等価物があるタグを素で使っていないか（`<table>` に `.mi-table` が無い等） |
| 層2 | 未申告の逸脱（独自クラスや `style` 属性で「見た目」を書いていないか） |
| 層3 | レビュー材料（申告された DS 外の箇所・独自クラス・構造見本を読むべきコンポーネント） |

kit に無い UI（日付選択・グラフ等）を作らざるを得ない場合は、HTML の直前に `<!-- ds-exception: 理由 -->` と申告します。**申告があれば層2は通り、層3のレビュー材料に載ります**（申告の無い逸脱は error）。判定の根拠は `kit-index.json`（CSS と見本 HTML から自動生成）で、スクリプトは固定リストを持ちません。

## リポジトリ構成

```
├── README.md            ← このファイル（人間向けの導入方法）
├── AGENTS.md            ← AI 向けの入口ポインタ
├── CLAUDE.md            ← AGENTS.md への薄いポインタ
├── tools/
│   ├── check-mockup.py       ← 作ったモックのセルフチェック（AI が毎回実行）
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
| `CHEATSHEET.md` | 全クラス・併用規則の1枚まとめ（AI が最初に読む） |
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
