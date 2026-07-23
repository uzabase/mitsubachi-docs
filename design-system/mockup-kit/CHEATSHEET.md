# mockup kit チートシート

mockup を組む AI が**最初に読む1枚**。全クラスの当て方と、間違えやすい規則をここに集約する。
（詳細な出自・鮮度の話は [README.md](./README.md)、各コンポーネントの使い分けは `../components/*.md`）

## 読み込み（この順で）

```html
<link rel="stylesheet" href="design-system/mockup-kit/tokens.css">
<link rel="stylesheet" href="design-system/mockup-kit/mitsubachi-mockup.css">
<!-- 内蔵10種以外のアイコンを使うときだけ -->
<link rel="stylesheet" href="design-system/mockup-kit/mitsubachi-icons.css">
<!-- ロゴを使うときだけ -->
<link rel="stylesheet" href="design-system/mockup-kit/mitsubachi-logos.css">
```

新規モックは `templates/starter.html` をコピーして組み立てるのが最短。

## 鉄則

1. **コンポーネントを自作しない**。`.mi-*` クラスを当てるだけ。
2. **色・寸法を直書きしない**。見た目は全てクラスが持っている。
3. **構造が深い7種（table / layout / dialog / menu / ai-chat / timeline / suggestion）は、組む前に `components/` の同名見本 HTML を読んで構造を踏襲する**。
4. 迷ったら該当コンポーネントの md（`../components/`）を読む。

## ⚠ 間違えやすい規則（要注意リスト）

| 規則 | 正しい書き方 |
|---|---|
| `--selected` は**単独では効かない** | `.mi-button--secondary.mi-button--selected` のように `--secondary/--tertiary/--ghost` と併用。`.mi-icon-button--selected` も同様。primary / plane に selected は無い |
| danger-button は独立クラスではない | `.mi-button--danger` ＋ variant（`--primary` 等）を**併用** |
| ai-button は専用クラスではない | `.mi-button--primary`（or `--secondary`）＋ 先頭に `<span class="mi-icon mi-icon--magic-fill">` |
| loading は中身が必要 | `.mi-button--loading` ＋ 中に `<span class="mi-loading"></span>` |
| menu-button は chevron を内包 | `.mi-button--menu` ＋ variant 併用、末尾に `<span class="mi-icon mi-icon--chevron-down-small">` |
| `.mi-select` はネイティブ `<select>` | 開いた選択肢メニューは `.mi-menu`（role="listbox"）で組む → 見本 `components/menu.html` |
| icon-button は必ず `aria-label` | アイコンだけでは意味が伝わらないため。tooltip 併用推奨 |
| アイコンは内蔵10種以外 icons.css が必要 | 内蔵: magic / magic-fill / search / check / cross / chevron-down(-small) / chevron-right(-small) / chevron-left。それ以外（home / bell 等97種）は icons.css |
| 空セル・影・プレースホルダを発明しない | table の空セルは素の `<td></td>`。card に影は付けない |

## ボタン系

| コンポーネント | クラス | 変種・規則 |
|---|---|---|
| neutral-button | `.mi-button` | variant: `--primary/--secondary/--tertiary/--ghost/--plane` を必ず1つ、size: `--medium/--large/--x-large` を必ず1つ。配置: primary は右・1画面1つ、間隔8px |
| danger-button | `.mi-button--danger` | variant 併用（primary/secondary/tertiary/ghost） |
| ai-button | （専用クラス無し） | `--primary/--secondary` ＋ magic-fill アイコン。AI実行操作限定 |
| menu-button | `.mi-button--menu` | variant 併用。chevron-down-small 内包（サイズ連動18/20/22px） |
| icon-button | `.mi-icon-button` | variant: `--primary/--secondary/--tertiary/--ghost`、size: `--small`(24)/既定(32)/`--large`(40)。`--selected` は variant 併用 |
| floating-button | `.mi-floating-button` | AIグラデーションリング |
| 状態（全ボタン共通） | | `--selected`（併用必須・上記）/ `--loading`（`.mi-loading` 内包）/ `disabled` 属性 |

## 入力系

| コンポーネント | クラス | 変種・規則 |
|---|---|---|
| text-field | `.mi-text-field` | 既定 large(48px) / `--medium`(40px) / `--error` / `--phone` / `disabled`。ラベル＋エラーの組みは `.mi-text-field-unit` ＋ `.mi-error-text` |
| text-area | `.mi-text-area` | 既定 medium(58px) / `--large`(64px) / `--phone` |
| select-box | `.mi-select` | 既定 medium(40px) / `--small`(32px) / `--secondary`(枠なし) / `--phone`。展開メニューは menu.html |
| search-box | `.mi-search-box` | `--primary/--secondary` 必須 ＋ 中に `__icon`(search) と `__input`。`--phone` |
| checkbox | `.mi-checkbox` | `<input type="checkbox">` に付ける。ラベルは `.mi-checkbox-label` で包む。中間状態 `--indeterminate` |
| radio-button | `.mi-radio` | `.mi-radio-label` で包む |
| radio-button-card | `.mi-radio-card` | 容器 `.mi-radio-card-group`。`--phone` |
| switch | `.mi-switch` | `role="switch"`。desktop 40×24 / `--phone` 56×32。ラベルは左 |
| segmented-control | `.mi-segmented-control` ＋ `.mi-segment` | 選択中 `.mi-segment--selected`（check アイコン内包）/ `--icon` / 容器に `--phone` |
| filter-chip | `.mi-chip` | 容器 `.mi-chip-group`。`--phone` |
| input-chip | `.mi-input-chip` | 中に `__remove`（cross アイコン）。容器 `-group` |
| label-unit | `.mi-label-unit` | `__label` ＋ `__required` |
| 選択肢グループ | `.mi-choice-group` | `--vertical` / `-unit`（横16px・縦4px） |
| suggestion | `.mi-suggestion` | **→ 見本 `components/suggestion.html` を読む** |

## ナビゲーション系

| コンポーネント | クラス | 変種・規則 |
|---|---|---|
| page-tab | `.mi-page-tab` | 下線インジケーター式。ページ全体の切替 |
| section-tab | `.mi-section-tab` | セクション内の切替。`--phone` |
| breadcrumb | `.mi-breadcrumb` | `--phone`（12→14px） |
| pagination | `.mi-pagination` | chevron の icon-button ＋ ページ番号 select ＋「/ 総数」。`--phone` |
| menu | `.mi-menu` ＋ `.mi-menu-item` | **→ 見本 `components/menu.html` を読む**（--selected/--sub/--disabled/--danger/--phone、role の使い分け） |
| notification-badge | `.mi-badge` | 数値 / `--dot`。右上重ねは `.mi-badge-anchor` で包む |

## 表示系

| コンポーネント | クラス | 変種・規則 |
|---|---|---|
| table | `.mi-table` | **→ 見本 `components/table.html` を読む**（grid/`--list`、`__num`/`__row-header`/`__check`/`__actions`、`aria-sort`/`aria-selected`） |
| read-only-tag | `.mi-tag` | `--neutral/--information/--positive/--negative` |
| link-tag | `.mi-link-tag` | x-small / small / medium |
| avatar | `.mi-avatar` | 5サイズ × パレット7色 ＋ inactive。重ねは `.mi-avatar-group`（最大5人） |
| card | `.mi-card` | zabuton 面 / `--outlined`。**影は付けない** |
| loading | `.mi-loading` | `--ai`、6サイズ |
| report-heading | `.mi-report-heading--1〜6` | 読み物見出し。`--phone` |
| timeline | `.mi-timeline` | **→ 見本 `components/timeline.html` を読む**（item の flow/dot/content 構造） |
| ai-chat | `.mi-ai-chat` | **→ 見本 `components/ai-chat.html` を読む**（messages/input/disclaimer の3部） |
| icon | `.mi-icon .mi-icon--<名前>` | 内蔵10種以外は icons.css。一覧 `components/icons.html` |
| logo | `.mi-logo .mi-logo--<名前>` | `--speeda`(既定・symbol付き)/`--speeda-text`/`--speeda-zh`/`--speeda-ai-agent`/`--speeda-expert-research`/各`-inverse`(暗背景)/`--uzabase`。logos.css 必須。一覧 `components/logos.html` |

## 通知・オーバーレイ系

| コンポーネント | クラス | 変種・規則 |
|---|---|---|
| dialog | `.mi-dialog` | **→ 見本 `components/dialog.html` を読む**（backdrop ＋ header/body/footer、--phone） |
| tooltip | `.mi-tooltip` | 位置決めはモック側 |
| snackbar | `.mi-snackbar` | 既定 medium / `--small`。画面隅スタックは `.mi-snackbar-viewport` |
| inline-notification | `.mi-inline-notification` | `--error/--information/--success/--warning/--secondary/--phone` |
| banner | `.mi-banner--*` | 4 status ＋ title/text/close |
| icon-color | `.mi-icon-color--*` | error/information/success/warning。通知系の先頭アイコン |

## レイアウト

| コンポーネント | クラス | 変種・規則 |
|---|---|---|
| 汎用レイアウト（app shell） | `.mi-layout` | **→ 見本 `components/layout.html` を読む**（2カラム・サイドナビ240px・ヘッダー60px。page-title 有無で2バリアント。icons.css＋logos.css 必要） |
| side-navigation-item | `.mi-sidenav-item` | `__icon`/`__label`、`--selected`。グループは `.mi-sidenav-group`、見出し `.mi-sidenav-category` |
| 1カラム（参考） | `.mi-header` | サイドナビ無しの簡易パターン |
