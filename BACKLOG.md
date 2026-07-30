# BACKLOG

「やると決めたが未着手」「判断待ち」の項目。**人間向けの作業候補リストで、デザインシステムのルールではありません**（AI が従う指示は `design-system/AGENTS.md`）。

最終更新: 2026-07-29

---

## A. AI の出力精度を上げる（着手すると決めたもの）

AI が崩すのは「部品」ではなく「部品の間（画面としての組み立て）」と「kit に無いものへの対処」という整理から出た施策。

| # | 項目 | 何をするか | なぜ効くか |
|---|---|---|---|
| **A-2** | 画面テンプレート集 | 頻出画面の完成形を `mockup-kit/templates/` に追加する（一覧＋フィルタ / 検索結果 / 企業・レポート詳細 / ダッシュボード / 設定・フォーム / AI チャット併設） | 現在の雛形は `starter.html` とエラーページ3枚だけ。AI は「どのクラスか」より「**どう並べるか**」で外す |
| **A-3** | レイアウト・余白の規約 | コンテンツ最大幅・セクション間の縦余白・カードグリッドの列数と gap・フォーム項目の縦間隔を決める。`.mi-stack` / `.mi-grid` / `.mi-section` のような**配置専用ユーティリティを kit に足す**案 | `starter.html` は「モック側で書いてよいのは配置だけ」と言うのに、**その配置の正解が書かれていない**＝現在唯一 AI の自由記述に委ねられている領域。`starter.html` のヘッダー中央テキストが `ds-exception` 申告になっているのがこの不足の実例 |
| **A-4** | kit に無い UI のフォールバック方針 | 「発明禁止 ＋ 既存プリミティブでの代替レシピ」を明文化する（例: アコーディオン → card ＋ icon-button(chevron)、グラフ → table）。対象: 日付選択・アコーディオン・ドロワー・ステッパー・ファイルアップロード・ツリー・カレンダー | **`check-mockup.py` の層1・層2 はこれとセットで初めて実効性が出る**。現状は「作らない・作ったら申告する」までしか言えていない |

## B. 未着手・要判断

| # | 項目 | 内容 | 判断が必要な点 |
|---|---|---|---|
| **A-5** | チャートの見本（**配色ルールは 2026-07-29 に取り込み済み**） | 残っているのは**グラフ本体の見本 HTML**（CSS だけで組めるバー・スパークライン・ドーナツ）。配色は Notion から取り込み済み（`foundations/chart-color.md` ＋ `.mi-chart-fill--*` / `.mi-chart-line--*`） | Speeda はプロトにグラフがほぼ必ず出る。色は当てられるようになったが、**軸・目盛り・凡例のレイアウトは毎回 AI が組む**ことになる。なお `--chart-*` は Notion 由来の**暫定値**で、primitive color のパレット再検討後に変わる |
| **C-1** | 状態バリエーションの規約 | empty / loading / error / 権限なし / 初回のパターン定義 | 空状態は検索主体の Speeda で頻出。文言は `foundations/writing.md` に書いたが、**画面構成のパターンは未定義** |
| **C-3** | 評価ハーネス | `design-system/test/test-prompts.md` に合格条件（ルーブリック）を付け、生成 → `check-mockup.py` → スクショで回帰確認する | 現在の test-prompts.md は **Figma URL が全て `DUMMY`** のまま。作り直すか、URL を確定させるかの判断が必要 |
| **C-4** | アンチパターン集 | AI が実際にやった失敗の before / after コード | `foundations/prohibited.md` は抽象的。実例収集のコストがかかる |
| ~~**hook**~~ | セルフチェックの自動実行 | **見送り（2026-07-29 決定）** | 理由: ① hook は Claude Code 限定で、デザイナーが Claude.ai で作る**主要経路には効かない** ② A-3 が未整備なうちは「kit にクラスが無いから申告するしかない」error が毎回出るため、書くたびに割り込まれると邪魔 ③ 完成時の自主実行は `design-system/AGENTS.md` 手順7で担保されている。**運用は「チャットで頼まれたら実行」＋「AI がモック完成時に1回」**とする |

## C. ドキュメントの整理（2026-07-29 の洗い出しの残り）

| # | 項目 | 内容 |
|---|---|---|
| **①** | `components/badge.md` と `notification-badge.md` の重複 | **同じコンポーネントの md が2つある**。badge.md は H1 が「# バッジ」で旧体裁・Figma node `5305-2124`、notification-badge.md が現行体裁・node `10748-4969`（kit が正としているのはこちら）。badge.md にしかない情報は「`aria-label="3件の未読通知"` の例」と「1つの要素に1つのバッジ」の2点。**それを移して badge.md を削除**するのが妥当 |
| **③** | `design-system/test/test-prompts.md` | Figma URL が全て `DUMMY`。C-3 で作り直す前提なら削除でよい |
| **⑦** | H1 の日英混在 | 7ファイルが日本語（`ai-chat.md`「AI チャット」/ `badge.md`「バッジ」/ `icon/icon.md`「アイコン」/ `table.md`「テーブル」/ `text-area.md` / `text-field.md` / `timeline.md`）。他67件は英語のコンポーネント名。AI は名前で照合するので英語統一の方が事故が少ない |
| **⑧** | `design-system/AGENTS.md` の foundations 表がリンクでない | コードスパンのみで辿れない（`foundations/icon-size.md` がどこからも参照されない状態の原因） |
| — | **テキストが 1px 上寄りになるコンポーネントが残っている**（2026-07-29 に tag / link-tag は解決） | ブラウザは行ボックス内のベースライン位置をフォントメトリクスで決めるため、`line-height × font-size` の端数によってテキストが上に寄る（Figma はテキストを行の中央に置くのでズレて見える）。**font-size 12px 系は均等だが、14px / 16px 系は 1px 上寄り**: `button--large` / `button--x-large` / `page-tab` / `menu-item` / `sidenav-item` / `inline-notification`。これらは**長文で複数行になり得るため `line-height: 1` にできず**、tag と同じ手法では直せない。1px（font 14px に対し約7%）を許容するか、別の方法（テキストを包む要素を作る等）を採るかの判断が必要 |
| — | `design-system/README.md` が古い | 「`CLAUDE.md` — AIが使うときの入口」（現在の入口は `AGENTS.md`）。`component-selection.md` と `mockup-kit/` に触れていない。ルート README を薄くしたので、**削除か全面更新**の判断が必要 |

## C-2. Figma × 実測の監査（2026-07-29 に**全コンポーネント一巡・完了**）

kit の**48コンポーネント＋テンプレート1件を Figma の正値とブラウザ実測で突き合わせ、155箇所を修正**した。
`check-kit.py` に検査を2件追加（トークンの実在 / フォールバックの鮮度）し**全11チェック**に。
**ズレ 0件だったのは 5件**（filter-chip / page-tab / section-tab / notification-badge / card）。

### 出自でズレの量が決まる（監査の最大の収穫）
| 出自 | ズレ |
|---|---|
| Figma node 由来（2026-06-18 前後の取り込み） | **0〜2件** |
| **公式実装（mitsubachi-ui）由来** | **毎回 2〜8件** |
| Figma に対応物なし（規約から組んだ） | 値は 0件だが**規約 md 自体の欠落**が出る |

**公式実装由来の独自トークン群は塊で疑う**のが最も効率的（checkbox 6件・radio 3件・button 4件・danger 2件・segment 4件が全滅）。
今後 kit に値を足すときは、**公式実装ではなく Figma から取る**ことでこの種のズレを防げる。

### 影 → **elevation トークンに統合（2026-07-29 完了）**

| 対象 | 変更後 |
|---|---|
| dialog | `--elevation-50`（`0 0 10px rgba(0,0,0,.1)` ＋ `0 16px 32px rgba(0,0,0,.13)`） |
| menu | `--elevation-30`（`0 0 6px` ＋ `0 8px 16px`） |

独自トークン `--dialog-shadow` / `--menu-shadow` は tokens から削除。**kit 内に独自の影はゼロ**になった。
dialog は枠線も監査で削除済みなので、**影だけで境界を作る Figma と完全一致**。

### kit に無い要素 → **3件すべて追加（2026-07-29 完了）**

| コンポーネント | 追加したもの | 実装 |
|---|---|---|
| search-box | 入力値があるときの**消去ボタン** | 既存の `.mi-icon-button--small` を置く。`:has()` でボタンがあるときだけ右 padding が 4px に詰まる |
| text-area | **文字数カウント**（`0/100`） | 新クラス `.mi-text-area-count`（12px・右寄せ・弱色・上 4px） |
| menu-item | **support text**（補助文） | 新クラス `.mi-menu-item__text` / `.mi-menu-item__support`（12px・lh 1.3・弱色、phone は 14px） |

いずれも**見本 HTML と md の導線**にも追加済み（`check-kit.py` の全11チェック通過）。

### hover / active の面が公式実装と Figma で食い違う（2026-07-29 判明・要確認）

ai-button の監査で、**hover / active の overlay が公式実装由来のトークンだと Figma より 1段薄い**ことが分かった。

| トークン | 公式実装由来の値 | Figma | 状況 |
|---|---|---|---|
| `--button-overlay-hover` / `-active` | 0.04 / 0.07 | **0.07 / 0.1**（`surface/overlay-hover` / `-active`） | **修正済み**（トークンを廃止し汎用に統合。icon-button は元から 0.07/0.1 だった） |
| `--segment-overlay-hover` / `-active` | 0.04 / 0.07 | **不透明色** #f5f5f5 / #ededed（`surface/regular-*`） | **修正済み**。1段ずれではなく「値は同じで実装が違う」型（白背景では 0.04/0.07 の重ねと同値） |
| `--radio-*` 3件 | 枠 **#cbcbcb**（不透明）/ checked-active #214dde | 枠 **0.2（半透明）** / **#143dd0** | **修正済み**。#cbcbcb は「半透明を白背景で焼いた」値で、色付きの面に置くと差が出る |
| `--checkbox-*` 6件 | 枠 0.29 / ring 0.04・0.07 / checked-hover #2666bf / disabled #e5e5e5・枠 0.05 | 枠 **0.2** / ring **0.07・0.1** / **#315ce8** / 白面・枠 **0.07**（チェック済みは面 **0.18**） | **修正済み**。**6件すべて誤り**で、トークン群を丸ごと汎用トークンに統合。radio が共有していた ring も一緒に直った |
| ai-button | （同じ 1段ずれ ＋ 未定義トークン名） | 0.07 / 0.1 | **修正済み** |
| `--danger-button-overlay-*` | #fff4f2 / #ffedeb | **#ffedeb / #ffebe8**（`surface/semi-weak-danger-*`） | **修正済み**（hover が Figma に存在しない値だった） |

**「1段ずれ」は公式実装由来トークンの定番の壊れ方**で、ai-button / neutral-button / danger-button の**3件連続で同じ型**だった。
hover に Figma に無い値が入り、active に Figma の hover 値が入る。**ボタン系3件で確認、segment は別の型だった**。

text-field の border と同じ「公式実装由来の値が Figma と違う」構図。ai-button と neutral-button は修正済みで、
**`--segment-overlay-*` だけが未確認**。

**教訓1: 「公式実装由来の独自トークン群」は塊で疑う。** checkbox は6件すべてが誤っていた。
**教訓2: トークンを2系統持つとどちらかが必ず古くなる。** `--button-overlay-*`（公式実装）と `--surface-overlay-*`（Figma）が
併存し、icon-button は後者・button は前者を使っていた。neutral-button の監査で `--button-overlay-*` を廃止して統合した。

### 未定義トークンの参照（2026-07-29 の横断検査で判明 → 解消済み）

`var(--token, フォールバック)` は**トークンが未定義でもフォールバックで動く**ため、tokens.css からトークンを消しても壊れず、誤った値が生き残る（suggestion が削除済みの `--banner-shadow` を参照し続けていた実例）。CSS 全体を検査した結果、未定義参照は **ai-button に3件だけ**だった。

| 参照 | 状況 |
|---|---|
| `--typography-font-weight-regular` | 正しくは `-normal`（値は同じ 400） |
| `--surface-overlay-default` | `.mi-ai-button--secondary:hover`。**実際に値も誤り**で、Figma は 0.07 |
| `--focus-ring` | `.mi-ai-button:focus-visible`。**実際に値も誤り**で、Figma は #191919（kit の他と同じ） |

3件すべて ai-button の監査で修正済み。**未定義参照が 0 になったので `check-kit.py` に「トークンの実在」検査を追加した**（全10チェック）。
教訓: **未定義トークン参照は値のズレのサイン**だった（3件とも実際に間違った値だった）。

### 選択肢のラベルの letter-spacing が不統一（2026-07-29 判明・未確定）

同じ「選択肢のテキスト」なのに2系統ある。**Figma のどちらが正か未確定**なので保留。

| クラス | line-height | letter-spacing | Figma の対応 |
|---|---|---|---|
| `.mi-radio-label` / `.mi-checkbox-label` | 1.3 | 0.02em（**2%**） | `text/✅medium-N-tight` |
| `.mi-radio-card__label` | 1.5 | 0.14px（**1%**） | `label/✅medium-N-normal` ← **2026-07-29 に確定**（node 9333:1832） |

**radio-card 側は確定**（label 系 1%・kit は正しい）。残るのは `.mi-radio-label` / `.mi-checkbox-label`（lh 1.3 ＋ 2%）が
正しいかどうかで、**radio-button-text / checkbox-text の symbol を個別に見れば確定する**。
radio-card の support text は `text/✅small-N-tight`（12px・lh 1.3・**2%**）で kit と一致していた。

### letter-spacing 未指定 → **全件完了（2026-07-29）**

当初 26件を「まとめて方針判断が必要」と考えたが、**Figma に必ず型（`label/*` または `text/*`）が指定されている**ため、
監査で1件ずつ確定させれば済む通常作業だった。**残件ゼロ**。

確定した規則（監査で全件確認）:

| 系統 | letter-spacing | 該当 |
|---|---|---|
| **`text/*`（本文・自由入力）** | font-size の **2%** | text-field, text-area, search-box, ai-chat（入力欄・発言・回答・免責）, dialog の body, inline-notification, table のセル, tooltip, suggestion の empty, error-text |
| **`label/*`（UI ラベル）** | font-size の **1%** | button 類, menu-item, segment, filter-chip, chip, snackbar の文言, table のヘッダー, select-box, breadcrumb, avatar, label-unit |
| **`headline/*`（見出し）** | 32・25px は **−2%** / 20px は **−1%** / 18px 以下は **+1%** | dialog の title（18px → +1%） |

**思い込みで外した例**（監査で判明）:
- **snackbar の文言**は見た目が本文的だが `label/*`（**1%**）
- **table のセル**は UI 的に見えるが `text/*`（**2%**）
- **ai-chat の免責 10px** は極小だが `text/*`（**2%**）
→ **サイズや見た目で判断せず、Figma の型指定を個別に見る**しかない。


### 監査で分かった副産物（対応済み・記録のみ）

- **Figma の Tailwind 出力 `drop-shadow-[…]` をそのまま box-shadow に写すと blur が半分になる**（banner で実害。`filter: drop-shadow()` は Figma の radius の約半分で描画されるため、box-shadow には Figma の radius をそのまま使う）
- **`.mi-icon-color`（CSS 後方・20px）が `__icon` 系クラスを詳細度で上書きする**。banner は 22px が 20px になっていた（修正済み）。`inline-notification__icon` / `snackbar__icon` は値が偶然一致していて今は無害だが同じ脆弱性を持つ
- **Figma 側の不整合**: breadcrumb は hover / active のときだけ letter-spacing が 2%（default は 1%）。そのまま実装すると hover でレイアウトが動くため kit は 1% に統一している（デザイナー確認の価値あり）
- **「Figma に忠実 ≠ 正しい実装」の例**: textarea の `overflow-clip`（スクロールを壊す）/ tag の `line-height: 1.3`（小数 px で字が上に寄る）/ breadcrumb の hover
- **フォールバック値の陳腐化**（2026-07-29 判明）: `var(--token, フォールバック)` のフォールバックは tokens.css が読まれないときの値で、**トークンを更新しても追随しない**。layout のヘッダー高さが tokens 60px / フォールバック 56px だった。横断チェック（px 382件）で不一致は1件のみと確認し、**`check-kit.py` に「フォールバックの鮮度」検査を追加**（全11チェック）
- **Figma MCP の `get_variable_defs` が返す「変数名」が実際の変数名と違う**（2026-07-29 検証・**原因未解明**）: アイコンサイズについて、Figma 上では正しく `icon-size-small`(18) 等を参照しているのに、MCP は `"24px": "18"` のように**別の名前**で返す（`18px`→14 / `24px`→18 / `27px`→20 / `30px`→22。名前の数字は値の約 4/3 倍で、`27`・`30` は icon-size コレクションに存在しない数字）。**値は正しいので実装は「値」で照合すれば問題ない**が、名前を信じると 4/3 倍の大きさで作ってしまう。`icon-size-small` の変数定義がエイリアス（別変数への参照）になっているかを Figma で見れば切り分けられる
- **Figma 側で headline の新旧トークンが混在**（2026-07-29 判明）: layout の page-title は `Headline/3XL`（22px・ls 2%・✅ なし・`font-weight/regular`）に従っているが、radio-button の frame には `❌削除/❌headline/❌3x-large-B-normal`（22px bold）もある。**22px の headline は廃止方向**とも読め、letter-spacing 規則に当てると 32・25px −2% / **22px +2%** / 20px −1% / 18px 以下 +1% と**符号が不連続**になる。デザイナー確認の価値あり

## D. kit の欠落・保留（2026-06-18 の Figma 差分調査より）

Figma にあって kit・md・公式実装のいずれにも無いもの。**取り込むかの指示待ち。**

| 項目 | 内容 |
|---|---|
| global-search 系 | `global-search-box` / `global-search-suggest`（＋ `-category` / `-group` / `-item`）。Speeda のグローバル検索 UI で、汎用部品化されていない |
| `text-area-unit` | `.mi-text-field-unit` はあるが text-area 版が無い |
| avatar の `variant=icon` | 値未取得・低優先 |
| menu の微差（未決） | **menu-item の右 padding は 2026-07-29 の監査で 16px に修正済み**。残っているのは shadow のみ（Figma は elevation-30、kit は `--menu-shadow`）。上の「影」の判断待ちに含まれる |
| `--button-plane-hover` / `-active` | plane variant の hover 面（rgba(49,92,232,0.08) / 0.12）は公式実装由来で **Figma 未確認**。plain の hover symbol（node `5128:4013`）で確定できる。使用頻度が低いので後回し |

## E. 検証

| 項目 | 内容 |
|---|---|
| まっさらな AI での生成再検証 | 3回目。`test/test-prompts.md` を採点軸付きで使う構想（C-3 と一体） |
