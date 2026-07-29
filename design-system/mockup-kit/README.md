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

## 対応コンポーネントと値の出自

**何に対応しているか**は下の表で、**クラスの当て方・変種**は [CHEATSHEET.md](./CHEATSHEET.md) と `kit-index.json` で引く（ここに変種を再掲すると二重管理になるため置かない）。この表は **値をどこから取ったか**の記録に絞る。

出自の区分: **公式実装** = [mitsubachi-ui](https://github.com/uzabase/mitsubachi-ui) の styles / **Figma** = Base-Component-Speeda-3.1-MITSUBACHI（fileKey `kHQNLM1dnk0EhZwOKBEBkL`）の node / **規約ベース** = Figma に専用コンポーネントが無く foundations のルールから構成。

| コンポーネント | クラス | 値の出自 | 近似・注意 |
|---|---|---|---|
| neutral-button | `.mi-button` | 公式実装 button.styles.ts | variant 名は `plane`（Figma 表記は plain。`--plain` も同じ見た目） |
| danger-button | `.mi-button--danger` | 公式実装 | variant との併用が前提 |
| ai-button | `.mi-ai-button` | 公式 `<mi-ai-button>` | 2026-07-23 刷新。**旧「neutral-button ＋ magic-fill」表現は廃止** |
| menu-button | `.mi-button--menu` | Figma `8301-3447` | chevron は size 連動（18/20/22px） |
| icon-button | `.mi-icon-button` | 公式実装 | — |
| floating-button | `.mi-floating-button` | 公式実装 | — |
| text-field | `.mi-text-field` | 公式実装 | — |
| text-field-unit / error-text | `.mi-text-field-unit` / `.mi-error-text` | 公式実装 | — |
| text-area | `.mi-text-area` | Figma `182-4766` | — |
| select-box | `.mi-select` | Figma `8257-8293` | 展開メニューは `.mi-menu` で組む |
| search-box | `.mi-search-box` | 公式実装 | Figma に size 変種が無く単一サイズ |
| checkbox | `.mi-checkbox` | 公式実装 | — |
| radio-button | `.mi-radio` | 公式実装 | — |
| radio-button-card | `.mi-radio-card` | Figma `9333-1828` | — |
| switch | `.mi-switch` | Figma `9925-6684` | — |
| segmented-control | `.mi-segmented-control` / `.mi-segment` | 公式実装 | — |
| filter-chip | `.mi-chip` | Figma `10771-20108` | selected の check は公式 icons.ts の `check`（24px グリッド）を流用。Figma の `check-small` よりグリフがやや大きい**近似** |
| input-chip | `.mi-input-chip` | Figma `5815-12862` | — |
| label-unit | `.mi-label-unit` | 公式実装 | — |
| 選択肢グループ | `.mi-choice-group` | Figma の配置値 | radio/checkbox の text-group と各 unit のレイアウト |
| suggestion | `.mi-suggestion` | Figma `7685-7082` | — |
| page-tab | `.mi-page-tab` | Figma `5634-1167` | — |
| section-tab | `.mi-section-tab` | Figma `5634-1269` | — |
| breadcrumb | `.mi-breadcrumb` | Figma `9926-7237` | — |
| pagination | `.mi-pagination` | Figma `8910-6776` | — |
| menu | `.mi-menu` / `.mi-menu-item` | 公式実装 ＋ Figma 無題ファイル `3dqm7vUqafFzdEkdpyqG9U`（menu 全6ページ） | `.mi-menu-category` は node `96:984` で正値化済み |
| sub-menu-item | `.mi-menu-item--sub` | Figma `8376-4959` | — |
| notification-badge | `.mi-badge` / `.mi-badge-anchor` | Figma `10748-4969` | — |
| table | `.mi-table` | Figma header-cell `6055-17160` / body-cell `6055-17729`（Null 表示・ソートの仕様は Figma ページ内の仕様フレーム） | ページ全体 `6055-16930` は MCP タイムアウト。値が無いセルは「–」が既定 |
| read-only-tag | `.mi-tag` | Figma `5646-1874` | — |
| link-tag | `.mi-link-tag` | Figma `5416-7917` | — |
| avatar | `.mi-avatar` | 公式実装 | variant=icon は未収録 |
| avatar-group | `.mi-avatar-group` | Figma `4822-682` | 最大5人 |
| card | `.mi-card` | **規約ベース** | 専用 Figma コンポーネントが無いことを検索で確認済み。**影は付けない**（elevation.md 準拠） |
| loading | `.mi-loading` | 公式実装 | ボタン内蔵時のスピナー色は公式が画像アセットのため `object-regular` で**近似** |
| report-heading | `.mi-report-heading--1〜6` | Figma `9494-1555` | — |
| timeline | `.mi-timeline` | Figma `6931-5682` | — |
| ai-chat | `.mi-ai-chat` | Figma `10808-18281` のパーツ | 全体フレームは MCP タイムアウトのため**コンテナ余白は近似** |
| dialog | `.mi-dialog-backdrop` / `.mi-dialog` | 公式実装 | — |
| tooltip | `.mi-tooltip` | 公式実装 | 位置決めはモック側 |
| snackbar | `.mi-snackbar` | 公式実装 | — |
| snackbar-viewport | `.mi-snackbar-viewport` | 公式実装 | — |
| inline-notification | `.mi-inline-notification` | 公式実装 | — |
| banner | `.mi-banner--*` | Figma `5702-2824` | — |
| icon-color | `.mi-icon-color--*` | 公式実装 | 通知系の先頭アイコンに使う |
| icon | `.mi-icon` | 公式 icons.ts | 本体に10種内蔵、残り97種は `mitsubachi-icons.css`。基底クラス `.mi-icon` は本体側 |
| グラフの色 | `.mi-chart-fill--*` / `.mi-chart-line--*` | **Notion「グラフの配色ルール（暫定）」**（2026-07-29 取得。Figma のトークンには未反映） | **暫定値**。primitive color のパレット再検討後に多色使いを再検討予定＝値ごと変わる。割り当てルールは `foundations/chart-color.md`。グラフ本体は kit に無い |
| logo | `.mi-logo--*` | Figma Logo ファイル `3abXEj4vbUt5UUf37Ld2Cn` sp-logo frame `1:13`（2026-07-23 取得）。`--uzabase` のみ公式実装 | **旧 `--speeda-ja`（カタカナ）/ `--speeda-en` は廃止** |
| layout（app shell） | `.mi-layout` ＋ `__sidenav` / `__content` / `__header` / `__page-title` / `__contents` | Figma ① page-title 無し `11461-12912` / ② page-title 有り `11461-13900`（サイドナビ詳細 `11461-14147`） | ざっくり版 `11395-2402`（ヘッダー56px）/ `11395-2427`（1カラム）は簡易表現で**正値ではない**（ヘッダーは60px）。`components/` に md が無い net-new |
| （参考）1カラム | `.mi-header` | 簡易パターン | 上記の汎用レイアウトとは別物 |
| side-navigation-item | `.mi-sidenav-item` | Figma component `10664:24442` | hover は系の最小 overlay 0.04 を流用＝**近似**。md が無い net-new |
| side-navigation-category | `.mi-sidenav-category` / `.mi-sidenav-group` | Figma component `10360:4591` | md が無い net-new |

**`components/` の md にあるコンポーネントは全てカバー済み。** ただし **side-navigation-item / -category と汎用レイアウト（app shell）は md が無い net-new**（Figma の詳細レイアウトから kit に先行収録）。

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
