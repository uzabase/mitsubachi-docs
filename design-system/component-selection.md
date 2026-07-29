# コンポーネント選定ガイド（やりたいこと → 何を使うか）

「**何を使えばいいか**」を意図から引くための表。クラスの当て方は [mockup-kit/CHEATSHEET.md](./mockup-kit/CHEATSHEET.md)、各コンポーネントの詳細は `components/` の md を見る。

> ここは選定の判断基準だけを書く（値は持たない）。クラス名は mockup パターンで使うものを併記する。

---

## 1. 入力を受け取る

| やりたいこと | 使うもの | 判断基準 |
|---|---|---|
| 1行の文字を入れる | text-field `.mi-text-field` | 40文字程度まで |
| 複数行の文字を入れる | text-area `.mi-text-area` | 改行が入る／長文 |
| 検索語を入れる | search-box `.mi-search-box` | 「検索」が目的のとき。text-field と混同しない |
| 検索語の候補を出す | suggestion `.mi-suggestion` | search-box とセット。見本 `components/suggestion.html` |
| 選択肢から1つ選ぶ | 下の「2. 選択肢の数で選ぶ」を見る | |
| 値を短く並べて消せるようにする | input-chip `.mi-input-chip` | 選択済みの値を可視化したいとき |
| 日付・期間を指定する | **kit に無い** | select-box の組み合わせで代替する。作る場合は申告（→ 5.） |

参照: [text-field](./components/text-field.md) / [text-area](./components/text-area.md) / [search-box](./components/search-box.md) / [suggestion](./components/suggestion.md)

## 2. 選択肢の数で選ぶ（迷いやすいところ）

| 排他性 | 選択肢の数 | 使うもの | 補足 |
|---|---|---|---|
| 1つだけ選ぶ | 2〜3個・常に見せたい | segmented-control `.mi-segmented-control` | 表示の切替（表／グラフ）に向く |
| 1つだけ選ぶ | 2〜5個・説明が必要 | radio-button `.mi-radio` / radio-button-card `.mi-radio-card` | 補足文が要るならカード型 |
| 1つだけ選ぶ | 5個以上 | select-box `.mi-select` | 展開メニューは `.mi-menu`（`role="listbox"`） |
| 複数選ぶ | 数個 | checkbox `.mi-checkbox` | 「すべて選択」が要るならヘッダーに置く |
| 複数選ぶ | 一覧を絞り込む | filter-chip `.mi-chip` | 下の「3. 絞り込む」を見る |
| ON / OFF を即時に切り替える | 1個 | switch `.mi-switch` | **押した瞬間に効く**設定だけ。保存ボタンが要るなら checkbox |

参照: [segmented-control](./components/segmented-control.md) / [radio-button](./components/radio-button/index.md) / [checkbox](./components/checkbox/index.md) / [select-box](./components/select-box/index.md) / [switch](./components/switch.md)

## 3. 絞り込む・並べ替える

| やりたいこと | 使うもの | 判断基準 |
|---|---|---|
| よく使う条件を数個、常に見せる | filter-chip `.mi-chip` | 選択状態が一目で分かる。1画面に10個以上は置かない |
| 条件の候補が多い | select-box `.mi-select` | 選択肢が長い／階層があるとき |
| 表示形式を切り替える | segmented-control | 絞り込みではなく「見せ方」の切替 |
| 語句で絞る | search-box | |
| 列で並べ替える | table のヘッダー（`aria-sort`） | 未ソート → 昇順 → 降順 → 解除。`mitsubachi-mockup.js` が自動で処理する |
| 件数が多い一覧を分割する | pagination `.mi-pagination` | table の下に置く |

参照: [filter-chip](./components/chip/filter-chip.md) / [table](./components/table.md) / [pagination](./components/pagination.md)

## 4. 情報を一覧で見せる

| やりたいこと | 使うもの | 判断基準 |
|---|---|---|
| 複数の項目を列で比較する | table（grid）`.mi-table` | 列同士を比べたいとき。**先に見本 `components/table.html` を読む** |
| 1〜2列の単純な並び | table（list）`.mi-table--list` | 罫線を減らして軽く見せる |
| 項目ごとに情報の塊を見せる | card `.mi-card` | 比較より閲覧が目的のとき。**影は付けない** |
| 時系列の出来事を見せる | timeline `.mi-timeline` | 見本 `components/timeline.html` |
| 少数の重要指標を見せる | card ＋ 数値（KPI） | 数値は `.mi-table__num` ではなくカード内に置く |
| グラフで見せる | グラフ本体は **kit に無い**（配色ルールはある） | 表で代替できないか先に検討する。作る場合は色を `.mi-chart-fill--*` / `.mi-chart-line--*` で当て（[chart-color.md](./foundations/chart-color.md)）、グラフの枠組みは申告して作る（→ 9.） |
| 読み物・レポートを見せる | report-heading `.mi-report-heading--1〜6` | 通常の見出しとは別物 |

参照: [table](./components/table.md) / [timeline](./components/timeline.md) / [report-heading](./components/report-heading.md) / [elevation](./foundations/elevation.md)

## 5. 画面・領域を切り替える

| やりたいこと | 使うもの | 判断基準 |
|---|---|---|
| ページ全体を切り替える | page-tab `.mi-page-tab` | 下線インジケーター式。URL が変わる粒度 |
| セクション内の表示を切り替える | section-tab `.mi-section-tab` | ページ内の一部だけが変わる |
| 表示形式だけを切り替える | segmented-control | 2〜3択のとき |
| 操作の一覧から選ばせる | menu `.mi-menu` ＋ トリガー | **先に見本 `components/menu.html` を読む** |
| 現在位置を示す | breadcrumb `.mi-breadcrumb` | 階層が3段以上あるとき |
| 画面の骨格を作る | layout `.mi-layout` | 2カラムの app shell。**先に見本 `components/layout.html` を読む** |

参照: [page-tab](./components/tab/page-tab.md) / [section-tab](./components/tab/section-tab.md) / [menu](./components/menu/index.md) / [breadcrumb](./components/breadcrumb.md) / [layout](./foundations/layout.md)

## 6. 知らせる・確認する

| 伝えたいこと | 使うもの | 判断基準 |
|---|---|---|
| 操作が完了した | snackbar `.mi-snackbar` | 数秒で消えてよい。画面隅に出す |
| その場所の状況・注意 | inline-notification `.mi-inline-notification` | 関係する要素の近くに置く。消えない |
| サービス全体の告知 | banner `.mi-banner--*` | 画面上部。閉じられる |
| 操作の前に確認する | dialog `.mi-dialog` | 取り消せない操作のときだけ。**先に見本 `components/dialog.html` を読む** |
| 補足を短く見せる | tooltip `.mi-tooltip` | hover で出る1行。必須情報は入れない |
| 未読・件数を示す | notification-badge `.mi-badge` | 数値 or `--dot` |
| 状態・分類を示す | read-only-tag `.mi-tag--*` | クリックできない。押せるなら link-tag |
| 処理中を示す | loading `.mi-loading` | AI 処理は `--ai` |

文言の書き方は [foundations/writing.md](./foundations/writing.md) を参照（snackbar は「〜しました」、確認ダイアログは疑問形など）。

## 7. 操作を置く

| やりたいこと | 使うもの | 判断基準 |
|---|---|---|
| その画面の主たる操作 | `.mi-button--primary` | **1画面に1つ**。右側に置く |
| 並列の操作・キャンセル | `.mi-button--secondary` | primary の左、間隔8px |
| 補助的な操作 | `.mi-button--tertiary` / `--ghost` | 情報量が多い画面では ghost |
| 取り消せない操作 | `.mi-button--danger` ＋ variant | 必ず variant を併用する |
| アイコンだけの操作 | `.mi-icon-button` | `aria-label` 必須。tooltip 併用を推奨 |
| 操作の一覧を開く | `.mi-button--menu` | chevron を内包する |
| AI を実行する | `.mi-ai-button` | **AI 実行操作限定**。variant は primary / secondary のみ |
| 画面に常に浮かせる | `.mi-floating-button` | AI への入口など、画面内に1つ |

参照: [neutral-button](./components/button/neutral-button.md) / [danger-button](./components/button/danger-button.md) / [ai-button](./components/button/ai-button.md) / [icon-button](./components/button/icon-button.md)

## 8. AI 機能を見せる

| やりたいこと | 使うもの | 注意 |
|---|---|---|
| AI と対話する | ai-chat `.mi-ai-chat` | 見本 `components/ai-chat.html`。免責文（`__disclaimer`）を必ず置く |
| AI 実行のきっかけを置く | ai-button / floating-button | 通常のボタンで代用しない |
| AI の処理中を示す | `.mi-loading--ai` | |
| AI らしさを演出する | グラデーションは**線で・1画面の1〜2割まで** | 面塗り・グラデ文字は Don't（[principles](./foundations/principles.md)） |

## 9. kit に無いものが必要になったとき

日付選択・アコーディオン・ドロワー・ステッパー・ファイルアップロード・グラフなどは kit に無い。

- **ユーザーが「〇〇を作って」と指示した場合** — 代替の検討は不要。**そのまま作ってよい**（代替案を提案して回り道しない）。申告だけ書く
- **指示が無いのに「kit に無い」と気づいた場合** — まず既存の部品で代替できないか考える（例: アコーディオン → card ＋ icon-button(chevron)、グラフ → table）

どちらの場合も**申告を1行書く**。CSS は該当箇所の直前に `/* ds-exception: 理由 */`（**そのブロックの以降がまとめて免除**されるのでコンポーネント1つに1行で足りる）、HTML は要素の直前に `<!-- ds-exception: 理由 -->`（**その要素と子孫が免除**）。

最後に `python3 tools/check-mockup.py <ファイル>` を実行し、申告漏れが無いことを確認する（未申告の逸脱は error）。

> 代替の作り方（レシピ）は今後整備する。現時点では「作ったら申告する」を守る。

## 迷ったときの原則

- 有彩色は限定的に使う。重要度が違うものを同じ色にしない（[color](./foundations/color.md)）
- 情報の塊はグレー面や線で区切る。細かい粒度で区切らない（[principles](./foundations/principles.md)）
- 影は「操作で出現・消える要素」だけに付ける（[elevation](./foundations/elevation.md)）
- 同等の機能を持つ独自コンポーネントを作らない（[prohibited](./foundations/prohibited.md)）
