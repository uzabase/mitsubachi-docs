# mockup kit

mockup パターン（パッケージ非依存の見た目再現）で mitsubachi-ui のコンポーネントを**自作せず正確に組み立てる**ためのアセット群。

## なぜあるか

「ダッシュボードを作って」のような複合指示では、各パーツを毎回 Figma MCP で取りに行く判断が抜け落ち、AI が「それっぽい」独自スタイルを生成してしまいがち。この kit は **正確な見た目をクラスとして同梱**し、AI がクラスを当てるだけで mitsubachi-ui ベースになるようにする。

## ファイル

| ファイル | 役割 |
|---|---|
| `tokens.css` | **値の単一の源**（CSS 変数）。Figma を機械的に写したスナップショット。 |
| `mitsubachi-mockup.css` | `.mi-*` クラス本体。**値は tokens.css の `var(--token)` を参照**し、生の値を持たない。 |
| `mitsubachi-icons.css` | 公式アイコンセット**全97種**（`.mi-icon--<名前>`）。容量が大きいため分離。アイコンを多用するモックで追加読み込み。 |
| `mitsubachi-logos.css` | Speeda / Uzabase の公式ロゴ SVG（容量が大きいため分離。ロゴが必要なモックでのみ追加読み込み）。 |
| `components/*.html` | 各コンポーネントの利用例（見本）。ブラウザで開くと見た目を確認できる。 |

## 使い方（mockup を作るとき）

1. 2つの CSS をこの順で読み込む（tokens.css → mitsubachi-mockup.css）。
2. コンポーネントを自作せず、`.mi-*` クラスを当てて組み立てる。

```html
<link rel="stylesheet" href="design-system/mockup/tokens.css">
<link rel="stylesheet" href="design-system/mockup/mitsubachi-mockup.css">

<!-- primary を右・secondary を左、間隔 8px（neutral-button.md の配置ルール） -->
<div style="display:flex; gap:8px;">
  <button class="mi-button mi-button--secondary mi-button--large">キャンセル</button>
  <button class="mi-button mi-button--primary mi-button--large">保存する</button>
</div>
```

クラスの一覧は `mitsubachi-mockup.css` 冒頭のコメントを参照。

## 値の正・鮮度

- **値の正は常に Figma。** 優先順位は `Figma MCP > mitsubachi-token > このスナップショット`。
- `tokens.css` は**手編集しない**（手で値を書くとハードコードになる）。値を変えたいときは Figma MCP / mitsubachi-token から取り直す。
- 取得元（fileKey / nodeId）と取得日は `tokens.css` のヘッダーに記載。
- 正確さが要る場面で古い疑いがあれば、Figma MCP の `get_design_context` / `get_variable_defs` を正とする。

## 対応コンポーネント

- [x] **neutral-button** — variant: primary / secondary / tertiary / ghost / plane（`--plain` は別名）、size: medium / large / x-large、状態: default / hover / active / focus / disabled / selected（色・状態は mitsubachi-ui 公式実装 button.styles.ts 由来）
- [x] **danger-button**（`.mi-button--danger` ＋ variant 併用）— primary / secondary / tertiary / ghost（公式実装由来）
- [x] **ai-button** — neutral-button の primary / secondary に公式 magic-fill アイコン（`.mi-icon--magic-fill`）を付けたもの（専用色トークンは無い。AI実行操作に限定）
- [x] **read-only-tag**（`.mi-tag`）— variant: neutral / information / positive / negative
- [x] **table**（`.mi-table`）— ヘッダー / セル / 行 hover / 選択行（`aria-selected`）/ 数値列（`.mi-table__num`）
- [x] **notification-badge**（`.mi-badge`）— 数値 / `--dot`、右上重ね配置の `.mi-badge-anchor`
- [x] **text-field**（`.mi-text-field`）— default / hover / focus / error / disabled（mitsubachi-ui 公式実装由来）
- [x] **search-box**（`.mi-search-box`）— variant: primary / secondary（mitsubachi-ui 公式実装由来）
- [x] **page-tab**（`.mi-page-tab`）— 下線インジケーター式。selected / hover / focus / disabled（Figma node `5634-1167` 由来）
- [x] **section-tab**（`.mi-section-tab`）— desktop / phone（`--phone`）。selected は青ボーダー＋青太字（Figma node `5634-1269` 由来）
- [x] **card**（`.mi-card`）— zabuton 面 / `--outlined`。影なし（elevation.md 準拠。専用 Figma コンポーネントが無いことは検索で確認済みの規約ベース構成パーツ）
- [x] **layout**（`.mi-layout` + header / page-title / contents、`.mi-header`）— サイドナビ240px・ヘッダー56px・ページタイトル64px（汎用①は Figma node `11395-2402` 由来）
- [x] **checkbox**（`.mi-checkbox` + `.mi-checkbox-label`）— checked / 中間 / disabled（公式実装由来）
- [x] **radio-button**（`.mi-radio` + `.mi-radio-label`）—（公式実装由来）
- [x] **switch**（`.mi-switch`）— desktop 40×24 / `--phone` 56×32。ON時はノブに check（Figma node `9925-6684` 由来）
- [x] **segmented-control**（`.mi-segmented-control` + `.mi-segment`）—（公式実装由来）
- [x] **text-area**（`.mi-text-area`）— min-height 58px / error / disabled（Figma node `182-4766` 由来）
- [x] **select-box**（`.mi-select`）— 高さ40px / 文字14px（Figma node `8257-8293` 由来）
- [x] **dialog**（`.mi-dialog-backdrop` / `.mi-dialog` + header/body/footer）— small/medium/large（公式実装由来）
- [x] **menu**（`.mi-menu` + `.mi-menu-item`）—（公式実装由来）
- [x] **tooltip**（`.mi-tooltip`）—（公式実装由来。位置決めはモック側）
- [x] **snackbar**（`.mi-snackbar`）—（公式実装由来）
- [x] **inline-notification**（`.mi-inline-notification--error/information/success/warning`）—（公式実装由来）
- [x] **banner**（`.mi-banner--*` + title/text/close）— 4 status のオーバーレイ通知（Figma node `5702-2824` 由来）
- [x] **avatar**（`.mi-avatar`）— 5サイズ × パレット7色 + inactive（公式実装由来）
- [x] **label-unit**（`.mi-label-unit`）— ラベル / 必須 / 補足（公式実装由来）
- [x] **floating-button**（`.mi-floating-button`）— AIグラデーションリング（公式実装由来）
- [x] **loading**（`.mi-loading`）— normal / `--ai`、6サイズ（公式実装由来）
- [x] **breadcrumb**（`.mi-breadcrumb`）— リンク項目は通常色＋hover面 / リンク無し項目は弱色。desktop 12px / `--phone` 14px（Figma node `9926-7237` 由来）
- [x] **pagination**（`.mi-pagination`）— icon-button（chevron）＋ページ番号 select-box（64px）＋「/ 総数」（Figma node `8910-6776` 由来）
- [x] **icon**（`.mi-icon`）— 本体によく使う7種（magic / magic-fill / search / check / chevron-down / chevron-right / cross）。**全97種は `mitsubachi-icons.css` を追加読み込み**（一覧は `components/icons.html`）
- [x] **icon-button**（`.mi-icon-button`）— size: `--small`(24) / 既定(32) / `--large`(40)、variant: `--primary/--secondary/--tertiary/--ghost` + `--selected`（公式実装由来）
- [x] **icon-color**（`.mi-icon-color--error/information/success/warning`）— 多色のステータスアイコン（公式実装由来。通知系の先頭アイコンに使う）
- [x] **text-field-unit / error-text**（`.mi-text-field-unit` / `.mi-error-text`）— ラベル＋フィールド＋エラーの組み立て（公式実装由来）
- [x] **snackbar-viewport**（`.mi-snackbar-viewport`）— snackbar の画面隅スタック。desktop 右上 / phone 下中央（公式実装由来）
- [x] **logo**（`.mi-logo--speeda-ja/speeda-en/speeda-zh/uzabase`）— 公式 SVG。`mitsubachi-logos.css` を追加読み込み
- [x] **filter-chip**（`.mi-chip` + `.mi-chip-group`）— selected / hover / active / focus / disabled、viewport: desktop / `--phone`（Figma node `10771-20108` 由来）
- [x] **link-tag**（`.mi-link-tag`）— クリック可能なタグ。x-small / small / medium（Figma node `5416-7917` 由来）
- [x] **avatar-group**（`.mi-avatar-group`）— 重なりは径の1/4・白い境界線・最大5人（Figma node `4822-682` 由来）
- [x] **report-heading**（`.mi-report-heading--1〜6`）— 読み物見出し h1〜h6（h2=下線、h3=左に赤線。Figma node `9494-1555` 由来）
- [x] **sub-menu-item**（`.mi-menu-item--sub`）— サブメニュー展開項目。右に chevron-right-small 固定（Figma node `8376-4959` 由来）
- [x] **menu-button**（`.mi-button--menu` ＋ variant 併用）— 右8px詰め＋chevron-down-small 固定。primary / secondary / ghost（Figma node `8301-3447` 由来）
- [x] **input-chip**（`.mi-input-chip` + `__remove` + `-group`）— 入力済み値のチップ。×で削除・group は折り返し（Figma node `5815-12862` 由来）
- [x] **radio-button-card**（`.mi-radio-card` + `-group`）— 補足つきカード型ラジオ。選択中は selected 面＋弱枠（Figma node `9333-1828` 由来）
- [x] **suggestion**（`.mi-suggestion` + `__category` + `-item` + `__empty`）— 検索候補リスト（Figma node `7685-7082` 由来）
- [x] **選択肢グループ**（`.mi-choice-group` / `--vertical` / `-unit`）— radio-button-text-group・checkbox-text-group・各 unit のレイアウト（横16px / 縦4px / ラベルと8px。Figma 配置値由来）
- [ ] 残り: timeline（Figma node `6931-5681`）, ai-chat（`9336-8319`）, logo/symbol（md に Figma URL なし・要調査）
  （mitsubachi-ui 公式実装にあるコンポーネントは**全て移植済み**。上記3つ以外の Figma コンポーネントも移植済み）

> **Figma 取得のコツ**: md の Figma URL が「ページ」を指している場合、`get_design_context` は失敗する（nothing selected エラー）。その場合は `get_metadata` でページ内のコンポーネントセット node を特定してから `get_design_context` を呼ぶ。

見本: `components/button.html`（button / ai-button / tag / table）、`components/form.html`（入力系一式）、`components/navigation.html`（tab / filter-chip / badge）、`components/card-layout.html`（card / layout）、`components/feedback.html`（dialog / menu / 通知系）、`components/display.html`（avatar / loading 等）、`test-output/dashboard-v2.html`（複合画面の実例）

## 既知の制約

- variant 名は公式実装・md に合わせ **`plane`**（Figma のプロパティ表記は plain。互換のため `--plain` も同じ見た目になる）。
- **table** は Figma のページが巨大で MCP がタイムアウトするため取得不可。既存トークンと `table.md` の規約に基づく構築（padding 等は妥当な近似。`table-body-cell` という component_set の存在は確認済み）。
- **card** は専用の Figma コンポーネントが無いことを検索で確認済み。zabuton / outlined のみで**影は付けない**（elevation.md: 影は「操作で出現・消える要素」専用）。
- **filter-chip** の selected 時 check アイコンは公式 icons.ts の `check`（24px グリッド）を流用しており、Figma の `check-small` よりグリフがやや大きい**近似**。
- ボタンの `loading` 状態は `.mi-loading` スピナーを組み合わせて表現できるが、ボタン側の loading レイアウトは未実装。

## 位置づけ（思想との両立）

このディレクトリは「**AI の生成エンジン向けアセット層**」であり、`foundations/` や `components/` の「**人間＋AI の判断のためのルール層**（値を持たない）」とは役割が異なる。`tokens.css` は Figma の自動スナップショットなので、「md にトークン値をハードコードしない」という原則とは矛盾しない。
