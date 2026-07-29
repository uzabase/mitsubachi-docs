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
<!-- 触れるモックにするときだけ（独自 JS は書かない） -->
<script src="design-system/mockup-kit/mitsubachi-mockup.js" defer></script>
```

**`tokens.css` と `mitsubachi-mockup.css` は必ず両方・この順で読み込む。** 2枚揃って初めて `body` のベースフォント（Arial ＋ 和文ゴシック）が効く。片方でも欠けると `.mi-*` を当てていない地の文（見出し・段落・素の `div` / `td`）が**ブラウザ既定の明朝体**で出る。CSS を読み込めない環境（単体 HTML・別プロジェクトへの貼り込み等）では、代わりに `body { font-family: Arial, YakuHanJPs, "Hiragino Sans", "Hiragino Kaku Gothic ProN", Meiryo, "Noto Sans JP", sans-serif; }` を自分で書く。

新規モックは `templates/starter.html` をコピーして組み立てるのが最短。

## 鉄則

1. **コンポーネントを自作しない**。`.mi-*` クラスを当てるだけ。
2. **色・寸法を直書きしない**。見た目は全てクラスが持っている（モック側に書いてよいのは配置＝余白・グリッド・並びだけ）。
3. **構造が深い7種（table / layout / dialog / menu / ai-chat / timeline / suggestion）は、組む前に `components/` の同名見本 HTML を読んで構造を踏襲する**。
4. **kit に無い UI（日付選択・アコーディオン・グラフ等）**: ユーザーの指示で作る場合は**代替検討をスキップして作ってよい**（代替案を提案して回り道しない）。指示が無いのに「無い」と気づいた場合はまず代替を検討する。**どちらの場合も申告を1行書く** → CSS は `/* ds-exception: 理由 */`（ブロックの以降がまとめて免除）、HTML は `<!-- ds-exception: 理由 -->`（その要素と子孫が免除）。
5. **作り終えたらセルフチェックを実行し、error 0 にする** → `python3 tools/check-mockup.py <ファイル>`
6. 迷ったら: 何を使うか＝[../component-selection.md](../component-selection.md) / 使い分けの詳細＝該当コンポーネントの md（`../components/`）/ 文言＝[../foundations/writing.md](../foundations/writing.md) / クラスの厳密な仕様＝`kit-index.json`

## 挙動（触れるモックにする）

`mitsubachi-mockup.js` を読み込むと、次が動く。**独自の JS は書かない**（見本: `components/interactive.html`）。

| 動かすもの | 書き方 |
|---|---|
| タブ / セグメント / チップ / スイッチ / 表の行選択・ソート | **属性不要**（クラスだけで自動） |
| メニュー開閉 | トリガーに `data-mi-menu="<メニューの id>"`、`.mi-menu` に `hidden`。listbox なら `data-mi-menu-label` でトリガーに選択値を反映 |
| ダイアログ開閉 | `data-mi-dialog-open="<id>"` / 閉じる側に `data-mi-dialog-close`（幕の外側クリック・ESC でも閉じる） |
| snackbar を出す | `data-mi-snackbar="メッセージ"`（他の `data-mi-*` と併記できる） |
| タブでパネルを切り替える | タブに `data-mi-tab-panel="<id>"` / パネルに `data-mi-panel="<id>"` |

## ⚠ 間違えやすい規則（要注意リスト）

| 規則 | 正しい書き方 |
|---|---|
| `--selected` は**単独では効かない** | `.mi-button--secondary.mi-button--selected` のように `--secondary/--tertiary/--ghost` と併用。`.mi-icon-button--selected` も同様。primary / plane に selected は無い |
| danger-button は独立クラスではない | `.mi-button--danger` ＋ variant（`--primary` 等）を**併用** |
| ai-button は `.mi-button` ではない | 専用クラス `.mi-ai-button`（ピル型）＋ variant を併用。中に magic-fill アイコン。**旧「`.mi-button`＋magic-fill」表現は廃止（2026-07-23）** |
| loading は中身が必要 | `.mi-button--loading` ＋ 中に `<span class="mi-loading"></span>` |
| menu-button は chevron を内包 | `.mi-button--menu` ＋ variant 併用、末尾に `<span class="mi-icon mi-icon--chevron-down-small">` |
| `.mi-select` はネイティブ `<select>` | 開いた選択肢メニューは `.mi-menu`（role="listbox"）で組む → 見本 `components/menu.html` |
| icon-button は必ず `aria-label` | アイコンだけでは意味が伝わらないため。tooltip 併用推奨 |
| アイコンは内蔵10種以外 icons.css が必要 | 内蔵: magic / magic-fill / search / check / cross / chevron-down(-small) / chevron-right(-small) / chevron-left。それ以外（home / bell 等97種）は icons.css |
| Null 表示・影を発明しない | table の値が無いセルは**「–」（en dash）が既定**（文言指定があればそれに従う）。card に影は付けない |

## ボタン系

| コンポーネント | クラス | 変種・規則 |
|---|---|---|
| neutral-button | `.mi-button` | variant: `--primary/--secondary/--tertiary/--ghost/--plane` を必ず1つ、size: `--medium/--large/--x-large` を必ず1つ。配置: primary は右・1画面1つ、間隔8px |
| danger-button | `.mi-button--danger` | variant 併用（primary/secondary/tertiary/ghost） |
| ai-button | `.mi-ai-button` | ピル型。variant: `--primary/--secondary` を必ず1つ（この2種のみ。tertiary/ghost は無い）、size: 既定 medium(32px)/`--large`/`--x-large`。中に magic-fill（or magic）アイコン。AI実行操作限定 |
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
| menu | `.mi-menu` ＋ `.mi-menu-item` | **→ 見本 `components/menu.html` を読む**（action/link/select の3種・`.mi-menu-group` 区切り・`.mi-menu-category` 見出し・--selected/--sub/--disabled/--danger/--phone）。select は single のみ・**selected は select-menu-item だけ**（action に selected は無い。check-small 20px）・link に disabled 無し・長文は折り返し（省略禁止）。表示位置は「下・左揃え」既定 |
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
| グラフの色 | `.mi-chart-fill--<色相>-<シェード>` / `.mi-chart-line--<1〜16>` | 棒・円は 5色相(blue/viridian/green/leaf/lemon)×5シェード(25/60/100/140/160)、折れ線は16色（9番目以降は破線が自動）。**どの凡例にどの色を割り当てるかは [../foundations/chart-color.md](../foundations/chart-color.md)**（凡例数で変わる。★暫定ルール）。グラフ本体は kit に無いので枠組みは申告して組む |
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
| エラーページ（403/404/500） | （テンプレート） | `templates/error-403.html / error-404.html / error-500.html` を**そのまま使う**（ボタンの「{ページ名}」と遷移先だけ差し替え。自作しない） |
