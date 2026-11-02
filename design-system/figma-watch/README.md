# figma-watch — Figma ライブラリ公開の検知と docs の修正箇所の当たり付け

Figma でライブラリを公開するたびに、デザイナーがバージョン履歴に説明文を残している
（例: 版名「コンポーネント公開」、説明「ステータス：更新 / 変更内容：menu-buttonをmenuへ移動」）。
この仕組みはその **公開を検知して Issue で知らせ**、ローカルの Claude Code が
**説明文から見るべき md と kit クラスに当たりをつけて書き換える** ための道具立てです。

- **Figma の中身はリポジトリに保存しない**（このリポジトリは public）。`state.json` に入るのは版 id・公開要素の名前と更新日時・ページ名と内容ハッシュだけ
- **CI は Issue を立てるだけ**。ブランチも state.json も触らない。書き換えと state の更新はローカルで行い 1 本の PR にする
- 対象は当面 **Base-Component-Speeda-3.1-MITSUBACHI**（md が最も多く参照している fileKey を自動で選ぶ）

## 一連の流れ

```
毎日 08:00 / 19:00 JST  GitHub Actions（.github/workflows/figma-watch.yml）
  tools/figma-watch.py check   version history を読み、state.json の基準より新しい「公開」エントリがあれば
                               Issue（ラベル figma-publish）を立てる。同じ版の Issue があれば立てない

Issue が来たら  ローカルで Claude Code を開き /figma-sync（.claude/skills/figma-sync/SKILL.md）
  tools/figma-watch.py targets ① 説明文の語を md 名・ページ名の辞書と照合
                               ② 公開要素（コンポーネント・コンポーネントセット・スタイル・変数）の差分
                               ③ 保険: 監視対象の全ページを読み、内容ハッシュを前回と比較（説明文の書き漏れを拾う）
                               → targets.local.json（当たりの表）と state.json の更新
  tools/figma-page.py          当たりをつけたページを読み、md を _TEMPLATE.md の方針で書き換える
  tools/figma-watch.py tokens  mitsubachi-token の値と tokens.css を突合（--apply で機械反映）
  tools/figma-watch.py report  PR 本文の骨格
  → build-kit-index.py → check-kit.py → PR（Closes #Issue）→ マージで state.json が main に入り「ここまで確認済み」
```

## ファイル

| パス | 役割 |
|---|---|
| `tools/figma-sources.py` | 監視対象 node と逆引き表（node → md / `.mi-*`）、照合辞書を md と kit README から**自動導出**（固定リストを持たない） |
| `tools/figma-watch.py` | `check` / `targets` / `tokens` / `report` |
| `tools/figma-page.py` | 1 ページを REST で読み、ルールに関わる部分だけを標準出力に出す（ファイルに書かない） |
| `tools/tests/test-figma-watch.py` | unittest。`python3 tools/tests/test-figma-watch.py` |
| `state.json` | 基準（手編集しない。`targets` が更新する） |
| `targets.local.json` | 当たりの表（作業用。.gitignore 済み） |

## 公開の検知のしくみ

- `GET /v1/files/:key/versions` の新しい版のうち、版名に「公開」「published」を含むか、説明文に「ステータス：」「変更内容：」を含むものを **公開エントリ**とみなす
- 自動保存と手動の名前付き版は無視する（`--include-named-versions` で含められる）
- 基準は `state.json` の `lastSeenVersion`。CI はこれより新しい公開エントリがあれば Issue を立てる
- ページ内のルール文だけを直した状態では Figma は公開できない（公開対象はコンポーネント・スタイル・変数）。その種の変更は次の公開時に ③ の保険で拾う

## state.json の中身

```json
{"files": {"<fileKey>": {
  "name": "ファイル名",
  "lastSeenVersion": {"id": "版 id", "created_at": "…"},
  "published": {"<asset key>": {"type": "component_set", "name": "switch", "pageId": "9925:5880", "updated_at": "…"}},
  "variablesHash": "sha256…",
  "pages": {"9925:5880": {"name": "✅ switch", "hash": "sha256…"}}
}}}
```

説明文・ルール文・座標・色は入れない。公開されても問題ない情報に限る。

## 説明文の書き方のお願い（デザイナー向け）

公開の説明文の「変更内容」に **コンポーネント名を英語識別子で**書くと、md と kit に自動で当たりが付きます。

- 例: 「変更内容：menu-button を menu へ移動」「変更内容：switch にラベル位置のルールを追記」
- 日本語だけでも Issue は立ちます（人が読んで判断します）
- Issue・PR 本文・`check` の出力には公開の説明文と日時・版 id だけを載せ、**投稿者名は出さない**（リポジトリが public のため）

## PAT（Figma Personal Access Token）

Figma の 設定 → セキュリティ → Personal access tokens で発行する。期限とスコープを選ぶ。
Enterprise では管理者が発行を制限している場合があるので、その場合は管理者に相談する。

| スコープ | 使う場面 |
|---|---|
| `file_versions:read` | 公開の検知（CI はこれだけで足りる） |
| `library_content:read`・`file_variables:read` | 公開要素の差分（`targets`） |
| `file_content:read` | 保険のページ比較・`figma-page.py` |

置き場は 2 箇所。

| 置き場 | 用途 | 無いとどうなるか |
|---|---|---|
| GitHub Secrets `FIGMA_TOKEN`（できれば共有アカウントで発行） | 朝夕の検知 | Issue が立たない。ローカルで `check` を手動で回せば代替できる |
| ローカルの環境変数 `FIGMA_TOKEN`（リポジトリには置かない） | `targets`・`figma-page.py` | 保険のページ比較が使えない（`targets --no-pages`）。ページは Figma MCP で読む |

期限切れや権限不足は 403 で止まり、メッセージに再発行の案内が出る。
ファイル名の取得に使う `/files/:key/meta` は別スコープ（`file_metadata:read`）で 403 になりやすいが、その場合は `/files/:key?depth=1` から取るので付けなくてよい。
GitHub は 60 日間コミットが無いと schedule を止めるので、止まっていたら Actions から手動実行する。

## 初回

```bash
export FIGMA_TOKEN=...
python3 tools/figma-watch.py targets --init     # 基準を作る（約 80 回の API 呼び出し、8 分前後。大きいページは分割取得になる）
python3 tools/check-kit.py
git add design-system/figma-watch/state.json && git commit -m "figma-watch の基準を作成"
```

Secrets に `FIGMA_TOKEN` を入れ、Actions の `figma-watch` を手動実行して「公開なし」になれば完成。

## 自動実行（ローカルの定期タスク）

Issue を拾って `/figma-sync` を回すところも、保守者の Mac の Claude Code デスクトップに
**定期タスク（scheduled task）`figma-sync-morning`** として置いてある（毎朝 08:30 JST。CI の検知が 08:00）。
中身はタスクの SKILL.md（`~/.claude/scheduled-tasks/figma-sync-morning/SKILL.md`）にあり、要点は:

- 元のチェックアウトを触らず、`origin/main` から **git worktree** を切って作業する（作業中の未コミット変更と衝突しない）
- `check` と `gh issue list --label figma-publish` で公開が無ければ 1 行報告して終了。同じ Issue を `Closes` に書いた open PR があれば二重に作らない
- 公開があれば SKILL.md の手順をそのまま実行し、`Closes #Issue` 付きの PR を出す。kit の見た目の値は Figma MCP が使えるときだけ直し、使えなければ PR 本文にその旨を書く
- Mac が閉じている・アプリが起動していないときは次に開いたときに実行される。CI での Claude 実行や API キーは使わない

止めたいときはデスクトップの定期タスク一覧で無効にする。別の人が引き継ぐときは同じ SKILL.md を自分の Mac に置く。

## 対象ファイルを増やすには

md の `## Figma` に URL を書けば監視対象に入る（自動導出）。ファイル単位で切り替えるときは `--file <fileKey>` を渡す。
URL を監視から外すには、その行か直前の行に `<!-- figma-watch: ignore -->` を書く。

## 将来: webhook で即時化

Figma の LIBRARY_PUBLISH webhook を受ける HTTPS の中継（Cloudflare Worker 等）から
`POST /repos/uzabase/mitsubachi-docs/dispatches`（`event_type: figma-updated`）を叩けば、同じワークフローがすぐ動く。
