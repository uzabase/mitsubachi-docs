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

## プロトタイプ実装の必須ルール（mi-* コンポーネント）

- 実装前に該当コンポーネントの `components/<name>/<name>.md` を必ず読む。
  キットCSS(`mitsubachi-mockup.css`)の基本例だけで判断しない（見た目の元であって構成・状態の正ではない）。
- **select-box**: ネイティブ `<select>` 禁止。`<button class="mi-select">` をトリガーにし、
  選択肢は `.mi-menu` + `.mi-menu-item` で構成（選択中は `.mi-menu-item--selected` + check）。
  ※開閉の最小JS・閉じる条件は後述「[メニューの実装パターン（重要）](#メニューの実装パターン重要)」を正とする。
- **icon-button の選択状態**: `.mi-icon-button--selected` を付与する（surface-selected 面 +
  border-selected + object-selected 色）。アイコン glyph の差し替えだけで済ませない。
- selected/error 等の状態は独自の色替えでなく DS の modifier クラスで当て、preview で実測検証する。

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
- [x] **table**（`.mi-table`）— grid view（グレーヘッダー・縦横罫線）/ `--list`（白・横罫線のみ）＋ソート状態・行見出し（`__row-header`）・数値列（`__num`）・**checkbox 列（`__check`・行選択）**・**アクション列（`__actions`・icon-button）**・セル内リンク・行 hover / 選択行（content-type=text/number/header/checkbox/icon-button/slot, content-state=filled/empty まで Figma table-header-cell `6055-17160`・table-body-cell `6055-17729` で確認・収録）
- [x] **notification-badge**（`.mi-badge`）— 数値 / `--dot`、右上重ね配置の `.mi-badge-anchor`
- [x] **text-field**（`.mi-text-field`）— default / hover / focus / error / disabled（mitsubachi-ui 公式実装由来）
- [x] **search-box**（`.mi-search-box`）— variant: primary / secondary（mitsubachi-ui 公式実装由来）
- [x] **page-tab**（`.mi-page-tab`）— 下線インジケーター式。selected / hover / focus / disabled（Figma node `5634-1167` 由来）
- [x] **section-tab**（`.mi-section-tab`）— desktop / phone（`--phone`）。selected は青ボーダー＋青太字（Figma node `5634-1269` 由来）
- [x] **card**（`.mi-card`）— zabuton 面 / `--outlined`。影なし（elevation.md 準拠。専用 Figma コンポーネントが無いことは検索で確認済みの規約ベース構成パーツ）。**領域を囲んで区切る用途はグレー塗りの `.mi-card` でなく白＋border の `.mi-card--outlined` を使う**（後述「プロトタイプ運用ルール」の面の選び方）
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
- [x] **icon**（`.mi-icon`）— 本体に内蔵する10種（magic / magic-fill / search / check / cross / chevron-down / chevron-down-small / chevron-right / chevron-right-small / chevron-left）。**これ以外（home / bell / side-left / question-circle など全97種）は `mitsubachi-icons.css` を追加読み込み**（一覧は `components/icons.html`。基底クラス `.mi-icon` は本体側にあり必ず併用）
- [x] **icon-button**（`.mi-icon-button`）— size: `--small`(24) / 既定(32) / `--large`(40)、variant: `--primary/--secondary/--tertiary/--ghost` + `--selected`（公式実装由来）
- [x] **icon-color**（`.mi-icon-color--error/information/success/warning`）— 多色のステータスアイコン（公式実装由来。通知系の先頭アイコンに使う）
- [x] **text-field-unit / error-text**（`.mi-text-field-unit` / `.mi-error-text`）— ラベル＋フィールド＋エラーの組み立て（公式実装由来）
- [x] **snackbar-viewport**（`.mi-snackbar-viewport`）— snackbar の画面隅スタック。desktop 右上 / phone 下中央（公式実装由来）
- [x] **logo**（`.mi-logo--speeda-ja/speeda-en/speeda-zh/uzabase/speeda-ai-agent`）— 公式 SVG。`mitsubachi-logos.css` を追加読み込み（`speeda-ai-agent` は別 Figma ファイル `3abXEj4vbUt5UUf37Ld2Cn` node `1:709` 由来。symbol付き・ライト背景用）
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
> 見本: `test-output/variant-additions-check.html`（全追加変種を一覧）。

> **Figma 取得のコツ**: md の Figma URL が「ページ」を指している場合、`get_design_context` は失敗する（nothing selected エラー）。その場合は `get_metadata` でページ内のコンポーネントセット node を特定してから `get_design_context` を呼ぶ。

見本: `components/button.html`（button / ai-button / tag / table）、`components/form.html`（入力系一式）、`components/navigation.html`（tab / filter-chip / badge）、`components/card-layout.html`（card / 汎用レイアウト①②（app shell）+ サイドナビ。logos.css・icons.css も読み込む）、`components/feedback.html`（dialog / menu / 通知系）、`components/display.html`（avatar / loading 等）、`test-output/dashboard-v2.html`（複合画面の実例）

## メニューの実装パターン（重要）

`select-box` / `icon-button` / `menu-button` などの「クリックで一覧を開く」UIは、**ネイティブの `<select>`・`<details>` を使わない**（ブラウザ/OSの独自UIが出てデザインが当たらない）。トリガー（`.mi-select` 等）＝閉じた状態の見た目、展開リスト＝ `.mi-menu` + `.mi-menu-item` で構成する。

`.mi-menu` は **CSSのみで振る舞い（開閉・外側クリックで閉じる・ESC・位置決め）は含まれない**ため、下記の最小JSを必ず添える（振る舞いの仕様は [components/menu/index.md](../components/menu/index.md) の「振る舞い」を正とする）。

### 閉じる条件（menu/index.md の「振る舞い」より。これ以外で閉じない）

メニューが閉じるのは次のときだけ。**これ以外の操作では閉じない**。

- メニューの**外側**をクリックした
- **ESC** キーを押した
- **トリガー**を再クリックした
- メニュー内の**項目**をクリックした
- **別のメニュー、または検索候補（suggestion）など別のポップオーバーを開いた** → 先に開いていたものは閉じる。**＝クリック/入力で開く重なりUI（メニュー・suggestion 等）は、画面で同時に開くのは常に1つだけ**

> - **マウスがメニューから外れただけ（mouseleave / hover 解除）では閉じない。** クリック誘発のメニューを hover 外しで閉じると、誤操作・タッチ非対応・到達不能（マウスを項目へ運ぶ途中で消える）の原因になる。閉じるのは上記の明示操作のみ。
> - **スクロールしても閉じない**（menu/index.md）。fixed 配置で画面に対して固定したメニュー（行アクション等）は、スクロール時に**閉じずに位置を追従**させる。

### 最小JS（メニュー・suggestion を1つの共有コントローラで管理し「同時に1つだけ開く」を保証）

> 旧版は各トリガーを独立にバインドし、かつトリガークリックで `stopPropagation` していたため、**先に開いたメニューが閉じず複数同時に開く**不具合があった。
> さらに、メニューと suggestion が別々のハンドラで管理されていると **「片方を開いても、もう片方の開いているものが閉じない」**（例: メニューを開いても開きっぱなしの検索候補が残る）。
> **開く重なりUI（メニュー・suggestion 等）を1つの共有コントローラ（`popovers` レジストリ）にまとめ、何かを開くときは必ず他を全部閉じる**。これで「クリック/入力で開いたら他は閉じる・同時に開くのは常に1つ」を系統をまたいで保証する。

```html
<!-- トリガー（複数可）：select-box / icon-button / menu-button。data-menu-trigger に対応 menu の id -->
<button class="mi-select" data-menu-trigger="menu-1" aria-haspopup="menu" aria-expanded="false">選択してください</button>
<div class="mi-menu" id="menu-1" role="menu" hidden>
  <button class="mi-menu-item" role="menuitem">オプション A</button>
  <button class="mi-menu-item" role="menuitem">オプション B</button>
</div>
```

```js
// 全ポップオーバー共有コントローラ。メニューも suggestion もこの popovers レジストリに登録する。
// 何かを開くときは必ず他を全部閉じる → 画面で同時に開くのは常に1つだけ。
const popovers = [];  // 各要素: { el, trigger, isOpen(), close() }
function registerPopover(p) { popovers.push(p); return p; }
function closeAllPopovers(except) {                       // ★ except 以外の開いているものを全部閉じる
  popovers.forEach(p => { if (p !== except) p.close(); });
}

// --- メニュー（select-box / icon-button / menu-button のトリガー）を登録 ---
document.querySelectorAll('[data-menu-trigger]').forEach(trigger => {
  const menu = document.getElementById(trigger.dataset.menuTrigger);
  const p = registerPopover({
    el: menu, trigger,
    isOpen: () => !menu.hidden,
    close() { menu.hidden = true; trigger.setAttribute('aria-expanded', 'false'); },
  });
  trigger.addEventListener('click', e => {
    e.stopPropagation();
    const willOpen = !p.isOpen();
    closeAllPopovers();                    // ★ 何を開くときも、まず他を全部閉じる（メニューも suggestion も）
    if (willOpen) { menu.hidden = false; trigger.setAttribute('aria-expanded', 'true'); }
  });
  menu.addEventListener('click', e => { if (e.target.closest('.mi-menu-item')) p.close(); }); // 項目クリックで閉じる
});

// 外側クリック / ESC は全ポップオーバー共通（メニュー・suggestion をまとめて閉じる）
document.addEventListener('click', e => {
  const inside = popovers.some(p => p.el.contains(e.target) || (p.trigger && p.trigger.contains(e.target)));
  if (!inside) closeAllPopovers();
});
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeAllPopovers(); });
```

- 選択状態（チェックマーク）を持つ項目は `select-menu-item`、アクション実行は `action-menu-item`、遷移は `link-menu-item` を使い分ける（[components/menu/index.md](../components/menu/index.md)）。
- 表示位置は「基本は下・右、エリアが無いときだけ上・左」（menu/index.md）。簡易プロトタイプでは下・右固定でもよい。
- **先頭アイコン付きの `action-menu-item`（[action-menu-item.md](../components/menu/action-menu-item.md) の Show icon、Figma `8376-4715`）は「アイコン20px(shrink) + ラベル(flex:1)・gap 8px の左寄せ」。** kit の `.mi-menu-item` は trailing アイコン（check / chevron）前提で `justify-content: space-between` のため、先頭アイコン+ラベルだと両端に分離する。**先頭アイコンを持つメニューは項目側を `justify-content: flex-start` に上書きし、先頭アイコンを `flex:none; 20px` にする**（モック側の1行 CSS で対応）。
- **テーブル行などで複数アクションを出す場合は、アイコンをアクションの数だけ横並びにせず、`icon-button`（`kebab-menu` アイコン）+ `menu` の1つにまとめる。** 破壊的操作（削除等）は `.mi-menu-item--danger`。

## プロトタイプ運用ルール（デザインシステムの定義ではない）

> ここに書くのは mitsubachi の正式仕様ではなく、プロトタイプ生成時にそう振る舞わせたい取り決め。
> `components/` の md（DS定義）には書かず、生成アセット層であるこの README で管理する。

- **領域を囲んで区切るときは、白背景（`surface/regular-default` ＝ `zabuton/regular`）＋ `border/regular` のヘアライン枠を基本にする。** グレーの塗り面（`zabuton/semi-strong` などの塗り）で領域を囲まない（ミツバチらしい表現ではない）。グレー面（`zabuton` 系の塗り）は、ヘッダー帯やサムネイル下地など「面そのものに役割がある」用途に限り、区切り・グルーピング目的では枠線で表現する。
  - 実装: mockup kit では `.mi-card`（既定＝`zabuton/semi-strong` 塗り）でなく **`.mi-card--outlined`**（白＋`border/regular`）を使う。色トークンの体系は [foundations/color.md](../foundations/color.md) の Surface ルールを参照。
- **search-box に 1 文字以上入力したら、必ず [suggestion](../components/suggestion.md) をセットで表示する。** 一致候補が無いときも `content-state=empty`（「一致する候補が見つかりません」）を出す。入力が空・クリア時は閉じる。
  - `.mi-search-box` / `.mi-suggestion` は CSS のみで挙動を持たないため、下記の最小JSを添える。**上の「メニューの実装パターン」の共有コントローラ（`registerPopover` / `closeAllPopovers` と外側クリック/ESC のグローバル処理）を前提とし、suggestion もそこに登録する**（メニューを開けば候補は閉じ、候補を出せばメニューは閉じる）。suggestion 単体のページでも、その共有コントローラ部分を必ず併せて入れる。

```html
<div class="mi-search-box">
  <input type="text" data-suggestion-for="sg-1" placeholder="キーワードで検索">
</div>
<div class="mi-suggestion" id="sg-1" hidden>
  <button class="mi-suggestion-item">候補 A</button>
  <button class="mi-suggestion-item">候補 B</button>
  <div class="mi-suggestion__empty" hidden>一致する候補が見つかりません</div>
</div>
```

```js
// 上の共有コントローラ（popovers / registerPopover / closeAllPopovers と外側クリック・ESC）を前提とする。
// 1文字以上の入力で必ず表示・候補ゼロは empty・空で閉じる。外側クリック/ESC は共有コントローラが処理。
document.querySelectorAll('[data-suggestion-for]').forEach(input => {
  const box = document.getElementById(input.dataset.suggestionFor);
  const items = [...box.querySelectorAll('.mi-suggestion-item')];
  const empty = box.querySelector('.mi-suggestion__empty');
  const p = registerPopover({                            // ★ suggestion も同じレジストリに登録
    el: box, trigger: input,
    isOpen: () => !box.hidden,
    close() { box.hidden = true; },
  });
  const render = () => {
    const q = input.value.trim().toLowerCase();
    if (q.length < 1) { box.hidden = true; return; }     // 空なら閉じる
    closeAllPopovers(p);                                  // ★ 候補を出すとき、他のポップオーバー（メニュー等）は閉じる
    box.hidden = false;                                   // 1文字以上は必ず表示
    let hit = 0;
    items.forEach(i => { const m = i.textContent.toLowerCase().includes(q); i.hidden = !m; hit += m; });
    if (empty) empty.hidden = hit > 0;                    // 候補ゼロなら empty
  };
  input.addEventListener('input', render);
  items.forEach(i => i.addEventListener('click', () => { input.value = i.textContent; box.hidden = true; }));
});
```

- **table の一番左の列（先頭セル）を、指示が無い限り header セル（content-type=`header`）にしない。** 既定では `table-body-cell` の `text`（通常の body セル）で表示する。左端を行見出し（header）にするのは、ユーザーが明示的に指示した場合のみ。
- **Figma URL から再現する際、指定のアイコンが kit のアイコンセット（`mitsubachi-icons.css` の全97種）に無い場合は、最も意味の近いアイコンで代替して表示する。** アイコンを自作したりセット外から持ち込んだりしない（[prohibited.md](../foundations/prohibited.md)「アイコン・画像」）。代替したことが分かるよう、該当箇所にコメントを残す。
- **アイコンは原則 outline（線）スタイルを既定で使い、fill（塗り）スタイルは使わない。** 例外として、コンポーネント定義側で fill が固定されているもの（AI 操作を示す `magic-fill` を持つ ai-button など）は、その定義に従って fill を使う。
- **ユーザーが DS 外の色やコンポーネント定義に無い仕様を指定したときは、[prohibited.md](../foundations/prohibited.md) の「DS外を指定されたときの応答プロトコル」に従う**（①DS内で最も近い代替を提案 → ②必要なら「DS外」と明示＋注記コメント付きで暫定適用 → ③勝手に恒久採用しない）。

## 既知の制約

- variant 名は公式実装・md に合わせ **`plane`**（Figma のプロパティ表記は plain。互換のため `--plain` も同じ見た目になる）。
- **table** はページ全体の MCP 取得はタイムアウトするが、コンポーネント単位の node を直接指定すれば取得できる（header `6055-17160` / body-cell `6055-17729` とも取得済みで **Figma 由来**）。content-type は text/number/header/checkbox/icon-button/slot を確認し、checkbox 列（`__check`）・アクション列（`__actions`）を実装済み（2026-06-18）。空セル（content-state=empty）はプレースホルダ記号を持たず素の `<td></td>`、slot セルは td に任意要素を直接置いて表現する。
- **card** は専用の Figma コンポーネントが無いことを検索で確認済み。zabuton / outlined のみで**影は付けない**（elevation.md: 影は「操作で出現・消える要素」専用）。
- **filter-chip** の selected 時 check アイコンは公式 icons.ts の `check`（24px グリッド）を流用しており、Figma の `check-small` よりグリフがやや大きい**近似**。
- ボタンの `loading` 状態は `.mi-button--loading`（中に `.mi-loading` スピナーを置く）で実装済み（2026-06-18）。スピナーの色は公式が画像アセットのため `.mi-loading`（object-regular）で近似。

## 位置づけ（思想との両立）

このディレクトリは「**AI の生成エンジン向けアセット層**」であり、`foundations/` や `components/` の「**人間＋AI の判断のためのルール層**（値を持たない）」とは役割が異なる。`tokens.css` は Figma の自動スナップショットなので、「md にトークン値をハードコードしない」という原則とは矛盾しない。
