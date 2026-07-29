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
| `CHEATSHEET.md` | **AI が最初に読む1枚**。全クラスの当て方・間違えやすい併用規則のまとめ。 |
| `kit-index.json` | **機械可読の索引**（自動生成）。必須修飾子・併用規則・必須属性/role/子要素・アイコン名一覧・タグ規則を持つ。CSS 本体を読まずに引ける。`tools/check-mockup.py` の判定根拠でもある。**手編集しない**（`tools/build-kit-index.py` で再生成）。 |
| `mitsubachi-mockup.js` | **最小の挙動スクリプト**（任意読み込み）。タブ・メニュー・ダイアログ・snackbar・行選択・ソートを `data-mi-*` の宣言で動かす。見た目は持たない。見本 `components/interactive.html`。 |
| `templates/starter.html` | 新規モックの雛形（CSS 読み込み順＋ app shell 骨格）。コピーして使う。 |
| `templates/error-403.html` / `error-404.html` / `error-500.html` | エラーページ（公式 pages/403・404・500 由来）。**そのまま使える**。ボタンの「{ページ名}」と遷移先だけ差し替える。 |
| `components/*.html` | 各コンポーネントの利用例（見本）。ブラウザで開くと見た目を確認できる。 |

## 使い方（mockup を作るとき）

1. まず [CHEATSHEET.md](./CHEATSHEET.md) を読む（全クラス・併用規則の1枚まとめ）。
2. 新規モックは `templates/starter.html` をコピーする（2つの CSS を tokens.css → mitsubachi-mockup.css の順で読み込み済み）。
3. コンポーネントを自作せず、`.mi-*` クラスを当てて組み立てる。
4. 作り終えたら**セルフチェックを実行し、error が 0 になるまで直す**。

```bash
python3 tools/check-mockup.py <作ったファイル.html>
```

2枚は必ず両方・この順で読み込む（揃って初めて `body` のベースフォントが効く。欠けると地の文がブラウザ既定の明朝体になる）。

```html
<link rel="stylesheet" href="design-system/mockup-kit/tokens.css">
<link rel="stylesheet" href="design-system/mockup-kit/mitsubachi-mockup.css">

<!-- primary を右・secondary を左、間隔 8px（neutral-button.md の配置ルール） -->
<div style="display:flex; gap:8px;">
  <button class="mi-button mi-button--secondary mi-button--large">キャンセル</button>
  <button class="mi-button mi-button--primary mi-button--large">保存する</button>
</div>
```

クラスの一覧は `mitsubachi-mockup.css` 冒頭のコメントを参照。

## kit を編集したら（保守者向け）

索引を再生成し、整合性チェックを実行する。

```bash
python3 tools/build-kit-index.py   # kit-index.json を CSS と見本から再生成
python3 tools/check-kit.py         # 整合性チェック
```

`check-kit.py` はリンク切れ・孤児ファイル・md 導線漏れ・見本の陳腐化（CSS に無いクラスを使っている）・併用必須クラスの文書化漏れ・索引の鮮度・見本自身のセルフチェック結果を検出する。

検査ルールは実ファイルから導出しており固定リストを持たないため、kit を拡張してもスクリプトの更新は原則不要。

## 値の正・鮮度

- **値の正は常に Figma。** 優先順位は `Figma MCP > mitsubachi-token > このスナップショット`。
- `tokens.css` は**手編集しない**（手で値を書くとハードコードになる）。値を変えたいときは Figma MCP / mitsubachi-token から取り直す。
- 取得元（fileKey / nodeId）と取得日は `tokens.css` のヘッダーに記載。
- 正確さが要る場面で古い疑いがあれば、Figma MCP の `get_design_context` / `get_variable_defs` を正とする。

## 対応コンポーネント

- [x] **neutral-button** — variant: primary / secondary / tertiary / ghost / plane（`--plain` は別名）、size: medium / large / x-large、状態: default / hover / active / focus / disabled / selected（selected は `--secondary/--tertiary/--ghost` に `--selected` を併用。単独では効かない）（色・状態は mitsubachi-ui 公式実装 button.styles.ts 由来）
- [x] **danger-button**（`.mi-button--danger` ＋ variant 併用）— primary / secondary / tertiary / ghost（公式実装由来）
- [x] **ai-button**（`.mi-ai-button`）— 公式 `<mi-ai-button>` 準拠のピル型（radius 9999px・weight 400）。variant: `--primary`(黒面)/`--secondary`(黒枠) の2種のみ、size: 既定 medium(32px/12px)/`--large`(40px/14px)/`--x-large`(48px/16px)、disabled/`--loading`。アイコンは magic-fill か magic（font 連動 1.28em）。**2026-07-23 刷新: 旧「neutral-button＋magic-fill」表現は廃止**（AI実行操作に限定）
- [x] **read-only-tag**（`.mi-tag`）— variant: neutral / information / positive / negative
- [x] **table**（`.mi-table`）— grid view（グレーヘッダー・縦横罫線）/ `--list`（白・横罫線のみ）＋ソート状態・行見出し（`__row-header`）・数値列（`__num`）・**checkbox 列（`__check`・行選択）**・**アクション列（`__actions`・icon-button）**・セル内リンク・行 hover / 選択行（content-type=text/number/header/checkbox/icon-button/slot, content-state=filled/empty まで Figma table-header-cell `6055-17160`・table-body-cell `6055-17729` で確認・収録）
- [x] **notification-badge**（`.mi-badge`）— 数値 / `--dot`、右上重ね配置の `.mi-badge-anchor`
- [x] **text-field**（`.mi-text-field`）— default / hover / focus / error / disabled（mitsubachi-ui 公式実装由来）
- [x] **search-box**（`.mi-search-box`）— variant: primary / secondary（mitsubachi-ui 公式実装由来）
- [x] **page-tab**（`.mi-page-tab`）— 下線インジケーター式。selected / hover / focus / disabled（Figma node `5634-1167` 由来）
- [x] **section-tab**（`.mi-section-tab`）— desktop / phone（`--phone`）。selected は青ボーダー＋青太字（Figma node `5634-1269` 由来）
- [x] **card**（`.mi-card`）— zabuton 面 / `--outlined`。影なし（elevation.md 準拠。専用 Figma コンポーネントが無いことは検索で確認済みの規約ベース構成パーツ）
- [x] **layout（汎用レイアウト = Speeda app shell）**（`.mi-layout` + `.mi-layout__sidenav`(-header/-body/-footer) / `__content` / `__header` / `__page-title` / `__contents`）— 2カラム・サイドナビ240px・**ヘッダー60px**。サイドナビ内は header(ロゴ+折りたたみ icon-button=`side-left`) / body(`side-navigation-item`・`-category`) / 最下部固定 footer(お知らせ=`bell` / よくある質問=`question-circle`)。アイコンは `mitsubachi-icons.css` を追加読み込み。**page-title 行の有無で2バリアント**: **①** page-title 無し（header → contents 直結。Figma node `11461-12912`）/ **②** page-title 有り（header → `__page-title`(64px) → contents。Figma node `11461-13900`）。両者は同じ骨格・サイドナビで page-title 行だけが差分。（サイドナビ詳細は `11461-14147`。ざっくり版 `11395-2402`(ヘッダー56px) / `11395-2427`(1カラム) は簡易表現で、正値は詳細レイアウト側）
- [x] **（参考）1カラム**（`.mi-header`）— サイドナビ無しのヘッダー+コンテンツ（背景は zabuton-semi-strong / background-regular）。上記2つの汎用レイアウトとは別の簡易パターン
- [x] **side-navigation-item**（`.mi-sidenav-item` + `__icon` + `__label`、`--selected`）— min-h 32px・選択時は `surface/overlay-current` 面・任意先頭アイコン20px（Figma component `10664:24442` 由来。hover は系の最小 overlay 0.04 を流用＝近似）
- [x] **side-navigation-category**（`.mi-sidenav-category`、`.mi-sidenav-group`）— サイドナビのグループ見出し（弱色12px）とグループ区切り（24px）。（Figma component `10360:4591` 由来）
- [x] **checkbox**（`.mi-checkbox` + `.mi-checkbox-label`）— checked / 中間 / disabled（公式実装由来）
- [x] **radio-button**（`.mi-radio` + `.mi-radio-label`）—（公式実装由来）
- [x] **switch**（`.mi-switch`）— desktop 40×24 / `--phone` 56×32。ON時はノブに check（Figma node `9925-6684` 由来）
- [x] **segmented-control**（`.mi-segmented-control` + `.mi-segment`）—（公式実装由来）
- [x] **text-area**（`.mi-text-area`）— min-height 58px / error / disabled（Figma node `182-4766` 由来）
- [x] **select-box**（`.mi-select`）— 高さ40px / 文字14px（Figma node `8257-8293` 由来）
- [x] **dialog**（`.mi-dialog-backdrop` / `.mi-dialog` + header/body/footer）— small/medium/large（公式実装由来）
- [x] **menu**（`.mi-menu` + `.mi-menu-item`）— 項目3種（action / link=`<a>` / select=listbox）、グループ区切り `.mi-menu-group`、group 内見出し `.mi-menu-category`、`--selected/--sub/--disabled/--danger/--phone`。select は single-select のみ（multi-select 禁止）、link に disabled 無し・新規タブは open-in-new アイコン。表示位置=トリガー基準「下・左揃え」既定／高さ=ページ端16px確保・超えたらスクロール／外側クリック or ESC で閉じる（公式実装＋Figma 無題ファイル `3dqm7vUqafFzdEkdpyqG9U` の menu 全6ページ由来） 
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
- [x] **icon**（`.mi-icon`）— 本体に内蔵する10種（magic / magic-fill / search / check / cross / chevron-down / chevron-down-small / chevron-right / chevron-right-small / chevron-left）。**これ以外（home / bell / side-left / question-circle など全97種）は `mitsubachi-icons.css` を追加読み込み**（一覧は `components/icons.html`。基底クラス `.mi-icon` は本体側にあり必ず併用）
- [x] **icon-button**（`.mi-icon-button`）— size: `--small`(24) / 既定(32) / `--large`(40)、variant: `--primary/--secondary/--tertiary/--ghost`。選択中は variant に `--selected` を併用（secondary/tertiary/ghost のみ。単独では効かない）（公式実装由来）
- [x] **icon-color**（`.mi-icon-color--error/information/success/warning`）— 多色のステータスアイコン（公式実装由来。通知系の先頭アイコンに使う）
- [x] **text-field-unit / error-text**（`.mi-text-field-unit` / `.mi-error-text`）— ラベル＋フィールド＋エラーの組み立て（公式実装由来）
- [x] **snackbar-viewport**（`.mi-snackbar-viewport`）— snackbar の画面隅スタック。desktop 右上 / phone 下中央（公式実装由来）
- [x] **logo**（`.mi-logo--speeda`(symbol付き・既定) / `--speeda-text`(テキストのみ) / `--speeda-zh` / `--speeda-ai-agent` / `--speeda-expert-research`、各 `-inverse`=暗背景用、`--uzabase`）— `mitsubachi-logos.css` を追加読み込み（一覧は `components/logos.html`。Speeda 系は Figma Logo ファイル `3abXEj4vbUt5UUf37Ld2Cn` sp-logo frame `1:13` の最新ブランド由来・2026-07-23 取得。**旧 `--speeda-ja`（カタカナ）/ 旧 `--speeda-en` は廃止**。uzabase のみ公式実装由来）
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
- [x] **timeline**（`.mi-timeline` + `-item` + `__flow/__dot/__content`）— ドット10px＋縦線、`--emphasized`（青ドット）/ `--loose`（Figma node `6931-5682` 由来）
- [x] **ai-chat**（`.mi-ai-chat` + `__messages/__user-message/__answer/__input/__disclaimer`）— ユーザー発言は右寄せグレーバブル、AI回答は地の文スロット（Figma node `10808-18281` のパーツ由来。全体フレームはタイムアウトのためコンテナ余白は近似）
**ドキュメント（components/ の md）にあるコンポーネントは全てカバー済み。** なお **side-navigation-item / -category と汎用レイアウト（app shell）は components/ に md が無い net-new**（Figma の詳細レイアウト `11461-12912` / `11461-13900` から kit に先行収録）。

## 変種の追加（size / viewport=phone / loading / variant個別。Figma 由来。2026-06-18）

Figma にはあるが従来 kit が「desktop の1サイズ・loading 無し」しか写していなかった**変種（コンポーネント内部の軸）**を追加。コンポーネント単位の差分（global-search 系など）とは別レイヤー。

- **size**（Figma に複数 size があるもの）
  - **text-field** — 既定=large(48px/16px) ＋ `--medium`(40px/14px)
  - **text-area** — 既定=medium(58px/14px) ＋ `--large`(64px/16px)
  - **select-box** — 既定=medium(40px) ＋ `--small`(32px)
  - **snackbar** — 既定=medium(min-h 56px) ＋ `--small`(hug・padding 8px)
- **viewport=phone**（`--phone` を併用。主に文字 14→16px・アイコン 20→22px のタッチ最適化）: **text-field / text-area / select-box / search-box / segmented-control（`--phone` は容器側）/ pagination / banner / inline-notification / dialog / report-heading（h1=25px太字・h6=14px のみ差）/ radio-button-card / menu-item**。（従来からある breadcrumb / chip / input-chip / section-tab / switch に加わる）
- **loading**（ボタン全系統）— `.mi-button--loading` ＋ 中に `<span class="mi-loading">`。loading 中は variant 色に依らず disabled 相当の面＋通常文字色（danger 含む）。スピナーは large/x-large=20px・medium=18px。
- **variant個別** — `.mi-menu-item--danger`（危険メニュー項目・赤文字）/ `.mi-inline-notification--secondary`（グレー面固定・補足扱いの小さめ）/ `.mi-select--secondary`（枠なし・auto幅）/ `.mi-segment--icon`（アイコンのみセグメント）

> ※ **search-box** は Figma に size バリアントが無く単一サイズ（追加は `--phone` のみ）。**global-search 系・avatar の icon variant** は「コンポーネント単位の差分」側で別途管理（未収録）。
> 見本: 追加変種は各 `components/*.html`（button / form / feedback / display）に収録済み。

> **Figma 取得のコツ**: md の Figma URL が「ページ」を指している場合、`get_design_context` は失敗する（nothing selected エラー）。その場合は `get_metadata` でページ内のコンポーネントセット node を特定してから `get_design_context` を呼ぶ。

## 見本（components/*.html）

見本は2種類に分かれる。

**① 単独見本（構造が深いコンポーネント。組む前に必ず読んでマークアップ構造を踏襲する）**
- `components/table.html` — grid / list ビュー・ソート状態・全 content-type・状態
- `components/layout.html` — 汎用レイアウト①②（app shell）＋サイドナビ（logos.css・icons.css も読み込む）
- `components/dialog.html` — backdrop ＋ header / body / footer・--phone
- `components/menu.html` — action / link / select の3種・グループ区切り（`.mi-menu-group`）・sub-menu の配置・トリガー使用例（menu-button / kebab / avatar）・--danger・--phone
- `components/ai-chat.html` — messages ＋ input ＋ disclaimer の3部構成
- `components/timeline.html` — item の flow / dot / content 構造
- `components/suggestion.html` — search-box ＋ category / item / empty

**①-2 挙動の見本**
- `components/interactive.html` — `mitsubachi-mockup.js` を読み込んで、タブ・メニュー・ダイアログ・snackbar・表の行選択／ソートを実際に動かす見本。触れるモックを作るときはこれを読む

**② まとめ見本（フラットな部品。クラスを当てるだけでよいもの。目視確認用）**
- `components/button.html`（button / ai-button / tag）、`components/form.html`（入力系一式）、`components/navigation.html`（tab / filter-chip / badge）、`components/feedback.html`（通知系: tooltip / snackbar / icon-color / inline-notification / banner）、`components/display.html`（avatar / card / loading 等）、`components/icons.html`（アイコン一覧）、`components/logos.html`（ロゴ一覧）

## 既知の制約

- variant 名は公式実装・md に合わせ **`plane`**（Figma のプロパティ表記は plain。互換のため `--plain` も同じ見た目になる）。
- **table** はページ全体の MCP 取得はタイムアウトするが、コンポーネント単位の node を直接指定すれば取得できる（header `6055-17160` / body-cell `6055-17729` とも取得済みで **Figma 由来**）。content-type は text/number/header/checkbox/icon-button/slot を確認し、checkbox 列（`__check`）・アクション列（`__actions`）を実装済み（2026-06-18）。空セル（content-state=empty）はプレースホルダ記号を持たず素の `<td></td>`、slot セルは td に任意要素を直接置いて表現する。
- **card** は専用の Figma コンポーネントが無いことを検索で確認済み。zabuton / outlined のみで**影は付けない**（elevation.md: 影は「操作で出現・消える要素」専用）。
- **filter-chip** の selected 時 check アイコンは公式 icons.ts の `check`（24px グリッド）を流用しており、Figma の `check-small` よりグリフがやや大きい**近似**。
- ボタンの `loading` 状態は `.mi-button--loading`（中に `.mi-loading` スピナーを置く）で実装済み（2026-06-18）。スピナーの色は公式が画像アセットのため `.mi-loading`（object-regular）で近似。

## 位置づけ（思想との両立）

このディレクトリは「**AI の生成エンジン向けアセット層**」であり、`foundations/` や `components/` の「**人間＋AI の判断のためのルール層**（値を持たない）」とは役割が異なる。`tokens.css` は Figma の自動スナップショットなので、「md にトークン値をハードコードしない」という原則とは矛盾しない。
