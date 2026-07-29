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
| — | `design-system/README.md` が古い | 「`CLAUDE.md` — AIが使うときの入口」（現在の入口は `AGENTS.md`）。`component-selection.md` と `mockup-kit/` に触れていない。ルート README を薄くしたので、**削除か全面更新**の判断が必要 |

## D. kit の欠落・保留（2026-06-18 の Figma 差分調査より）

Figma にあって kit・md・公式実装のいずれにも無いもの。**取り込むかの指示待ち。**

| 項目 | 内容 |
|---|---|
| global-search 系 | `global-search-box` / `global-search-suggest`（＋ `-category` / `-group` / `-item`）。Speeda のグローバル検索 UI で、汎用部品化されていない |
| `text-area-unit` | `.mi-text-field-unit` はあるが text-area 版が無い |
| avatar の `variant=icon` | 値未取得・低優先 |
| menu の微差（未決） | Figma の shadow は elevation-30 だが kit は公式実装由来の `--menu-shadow` のまま。menu-item の右 padding も Figma 16px vs kit 12px。**どちらを正とするか未決**のため据え置き |

## E. 検証

| 項目 | 内容 |
|---|---|
| まっさらな AI での生成再検証 | 3回目。`test/test-prompts.md` を採点軸付きで使う構想（C-3 と一体） |
