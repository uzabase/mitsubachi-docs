---
name: figma-sync
description: Figma ライブラリ公開の Issue（ラベル figma-publish）を受けて、公開の説明文から見るべき md と kit クラスに当たりをつけ、Figma を読み直して docs と kit を書き換え、state.json を更新した PR を出す。「figma-sync」「Figma の公開を反映して」「figma-publish の Issue を処理して」で発動。
---

# figma-sync — Figma 公開を docs に反映する

仕組みの全体は `design-system/figma-watch/README.md`。ここは手順だけ。

## 前提

- `FIGMA_TOKEN` が環境変数にあるか確認する。無ければ保険のページ比較を省き（`--no-pages`）、ページは Figma MCP（`get_metadata` → `get_design_context`）で読む
- **Figma Specs は読まない**。ページ内に点在するテキスト・do-dont マーカー・frame 名を材料にする
- 作業ブランチ: `git switch -c docs/figma-sync-YYYYMMDD origin/main`

## 手順

1. **公開エントリを取る**
   ```bash
   python3 tools/figma-watch.py check --json
   gh issue list --label figma-publish --state open
   ```
   公開が無ければ終了。Issue 番号を控える（複数あれば全部）。

2. **当たりをつける**
   ```bash
   python3 tools/figma-watch.py targets          # FIGMA_TOKEN が無ければ --no-pages
   ```
   `design-system/figma-watch/targets.local.json` に表が出る。きっかけは 3 種:
   - **説明文**: 説明文の語が辞書（md 名・ページ名）に当たったもの。最優先
   - **公開要素**: コンポーネント・スタイル・変数の追加/更新/削除
   - **ページ変更**: 保険のページ比較だけで見つかったもの（「説明文に無い変更」）。ページを読んで docs に関係する変更か判断してから手を付ける（使用例モックの編集などは無視してよい）
   説明文の語が当たらなかったものは原文を読み、自分で該当 md を判断して足す。

3. **ページを読み直す**（当たりをつけた md ごと）
   ```bash
   python3 tools/figma-page.py <fileKey> <nodeId>     # md の ## Figma の URL の node
   ```
   PAT が無ければ Figma MCP `get_metadata(fileKey, nodeId)` でページ構造を取り、本文テキストを読む。

4. **md を更新する**（`design-system/components/_TEMPLATE.md` の方針）
   - 冒頭 1 行（description）/ バリアントプロパティ表（軸と値）/ いつ使うか・いつ使わないか・使い分け・コンテンツルール・振る舞い / Do・Don't
   - **今の Figma に合わせる**。Figma に無くなった記述は消す。既存の文面に引きずられない
   - kit 導線行（`> mockup で再現する場合は …`）は変えない。md にトークン値を書かない
   - 説明文が「移動」「統合」「削除」なら md のファイル移動・統合・削除とリンク張り替えも行う（`check-kit.py` のリンク切れ検査が効く）
   - md が無いページ（新コンポーネント）は作らず、PR 本文の「対応しなかったもの」に候補として書く

5. **kit の値を直す**（見た目が変わった要素だけ）
   - Figma MCP `get_design_context` / `get_variable_defs` で正値を取り、`mockup-kit/tokens.css`・`mitsubachi-mockup.css`（`var(--x, fallback)` の fallback 含む）・`mockup-kit/README.md` 出自表を直す。手で値を決めない
   - component-set の node は `python3 tools/figma-sources.py --json` の `componentNodes` か kit README の出自表で引く

6. **色を合わせる・検査する**
   ```bash
   python3 tools/figma-watch.py tokens --apply
   python3 tools/build-kit-index.py && python3 tools/check-kit.py
   python3 tools/check-mockup.py design-system/mockup-kit/components/<触った見本>.html
   ```

7. **PR を出す**
   ```bash
   python3 tools/figma-watch.py report --issue <Issue 番号> > /tmp/pr-body.md
   ```
   「直した内容」「対応しなかったもの・判断に迷った点」を埋め、`state.json` の変更も含めてコミットし PR を作る。
   マージで Issue が閉じ、state.json が main に入る（＝この公開まで確認済み）。
   対応しないと決めた項目は `BACKLOG.md` に 1 行残す。
