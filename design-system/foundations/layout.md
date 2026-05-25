# layout

Speeda プロダクトの画面構成を定義する汎用レイアウト。

---

## 汎用レイアウト①

- Figma: https://www.figma.com/design/kHQNLM1dnk0EhZwOKBEBkL/Base-Component-Speeda-3.1-MITSUBACHI?node-id=11395-2402
- 画面構成は Figma MCP（`get_design_context`）で取得

サイドナビゲーション（左カラム）とコンテンツエリア（右カラム）の横並び2カラム構成。

### レイアウト背景色ルール

画面は大きく2つの背景色エリアに分かれる。

### サイドナビゲーション

- background: `var(--zabuton-semi-strong, #F8F8F8)`

### コンテンツエリア（ヘッダー・ページタイトル・メインコンテンツ）

- background: `var(--background-regular, #FFF)`
- 3つのセクションは区切り線なく、同一の白背景で連続している

---

## 汎用レイアウト②

- Figma: https://www.figma.com/design/kHQNLM1dnk0EhZwOKBEBkL/Base-Component-Speeda-3.1-MITSUBACHI?node-id=11395-2427
- 画面構成は Figma MCP（`get_design_context`）で取得

ヘッダー + コンテンツの縦積み1カラム構成。サイドナビゲーションを持たない。

### レイアウト背景色ルール

画面は大きく2つの背景色エリアに分かれる。

### ヘッダー

- background: `var(--zabuton-semi-strong, #F8F8F8)`

### コンテンツエリア（ページタイトル・メインコンテンツ）

- background: `var(--background-regular, #FFF)`
- 2つのセクションは区切り線なく、同一の白背景で連続している
