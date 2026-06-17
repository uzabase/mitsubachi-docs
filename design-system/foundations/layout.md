# layout

Speeda / Speeda AI Agent プロダクトの画面構成を定義する汎用レイアウト。

**汎用レイアウト = 2カラム（サイドナビ + コンテンツ）のアプリケーションシェル**。Figma では「詳細レイアウト」として定義されており、page-title 行の有無で次の2バリアントに分かれる。

| | バリアント | コンテンツ列の構成 | Figma node |
|---|---|---|---|
| ① | page-title 無し | ヘッダー(60px) → メインコンテンツ | `11461-12912` |
| ② | page-title 有り | ヘッダー(60px) → ページタイトル(64px) → メインコンテンツ | `11461-13900` |

両者は**同じ骨格・同じサイドナビ**で、page-title 行が入るかどうかだけが違う。

> Figma に併載の「ざっくりしたレイアウト」（`11395-2402` = 2カラム・ヘッダー56px / `11395-2427` = 1カラム）は構成を粗く示した簡易表現。**寸法の正値は詳細レイアウト側**（ヘッダーは 60px）を使う。

- Figma①: https://www.figma.com/design/kHQNLM1dnk0EhZwOKBEBkL/Base-Component-Speeda-3.1-MITSUBACHI?node-id=11461-12912
- Figma②: https://www.figma.com/design/kHQNLM1dnk0EhZwOKBEBkL/Base-Component-Speeda-3.1-MITSUBACHI?node-id=11461-13900
- 画面構成・寸法は Figma MCP（`get_design_context` / `get_variable_defs`）で取得

---

## 構成

### 横並び2カラム

- **サイドナビゲーション**（左カラム・幅240px固定）と**コンテンツエリア**（右カラム）の横並び。
- サイドナビ background: `var(--zabuton-semi-strong, #F8F8F8)`
- コンテンツエリア background: `var(--background-regular, #FFF)`

### コンテンツ列

- **ヘッダー（60px）** → （②のみ **ページタイトル（64px）**）→ **メインコンテンツ**。
- これらのセクションは区切り線なく、同一の白背景（`background-regular`）で連続している。

### サイドナビゲーションの内部構造

3つの区画で構成する。

- **ヘッダー（60px）** — ロゴ（Speeda AI Agent 等）＋ 折りたたみ icon-button（`side-left` アイコン）。
- **ボディ** — `side-navigation-item` と `side-navigation-category` によるナビゲーション群（primary / secondary）。
- **フッター（最下部固定）** — 「お知らせ」（`bell`）・「よくある質問」（`question-circle`）等の常設項目。

#### サイドナビゲーションの構成要素

- **side-navigation-item**（Figma component `10664:24442`） — ナビ項目。min-height 32px、任意の先頭アイコン（20px）＋ ラベル（14px）。選択中は `surface/overlay-current`（薄いグレー面）でハイライト。
- **side-navigation-category**（Figma component `10360:4591`） — 関連項目をまとめるグループ見出し（弱色 12px）。

---

## （参考）1カラム

サイドナビを持たず、ヘッダー + コンテンツを縦積みする簡易パターン（Figma ざっくり版 `11395-2427`）。上記2つの汎用レイアウトとは別物。

- ヘッダー background: `var(--zabuton-semi-strong, #F8F8F8)`
- コンテンツエリア background: `var(--background-regular, #FFF)`
