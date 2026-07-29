# mitsubachi-docs

## 導入方法

使い方は2通りあります。

### ① URL を指定して参照させる

チャット型の AI（Claude.ai など）で使う場合。リポジトリの URL を渡して参照させます。

```
https://github.com/uzabase/mitsubachi-docs
```

指示の例:

```
https://github.com/uzabase/mitsubachi-docs を参照して、
design-system/AGENTS.md のルールに従ってモックを作ってください。
mockup パターンで、design-system/mockup-kit/ の CSS を使うこと。
```

> プライベートリポジトリのため、AI 側にアクセス権が無い場合は②のローカル参照を使ってください。

### ② ローカルにダウンロードして参照させる

コーディングエージェント（Claude Code / Cursor など）で使う場合。手元にクローンして、そのディレクトリで作業させます。

```bash
git clone git@github.com:uzabase/mitsubachi-docs.git
```

- **Claude Code**: リポジトリ内で起動すれば `design-system/CLAUDE.md` → `AGENTS.md` が自動で読まれます。別プロジェクトから使う場合は、クローン先のパスを伝えてください
- **Cursor**: `.cursor/rules` に「`<クローン先>/design-system/AGENTS.md` を参照する」旨と、使用するパターン（後述）を書いておきます
- **モックの HTML から CSS を読み込む場合**: `design-system/mockup-kit/tokens.css` → `mitsubachi-mockup.css` の順でリンクします

最新の状態を保つため、使う前に `git pull` してください。

### 使い方のパターンを指定する

mitsubachi-ui は出力するコードの種類によって3つのパターンがあります。**どれを使うかは利用環境側で指定**してください（AGENTS.md 自体は環境非依存のため、そこでは固定していません）。

| パターン | 出力 | 使う場面 |
|---|---|---|
| **mockup** | 見た目だけを再現した HTML（パッケージ非依存） | AI によるモック生成 |
| **react** | mitsubachi-ui-react を使った React コード | React プロジェクトでの実装 |
| **web-component** | `<mi-*>` タグを使った HTML | Web Components が動く環境での実装 |

## できあがったモックを検査する

AI が作ったモックは、クラスの誤用・kit を使わない自作・独自 CSS での見た目づくりを機械的に検査できます。

```bash
python3 tools/check-mockup.py <モックのファイル.html>
```

error が 0 なら kit のルールに沿っています。検査の中身と `ds-exception`（kit に無い UI を作る場合の申告）の書き方は [design-system/AGENTS.md](./design-system/AGENTS.md) を参照してください。

## もっと詳しく

- [design-system/AGENTS.md](./design-system/AGENTS.md) — ドキュメントの構成・mockup の作業手順・トークンの取得方法
- [design-system/mockup-kit/README.md](./design-system/mockup-kit/README.md) — kit に入っているもの・対応コンポーネント・値の正と鮮度

## 関連リポジトリ

- [mitsubachi-ui](https://github.com/uzabase/mitsubachi-ui) — Web Components / [Storybook](https://uzabase.github.io/mitsubachi-ui/)
- [mitsubachi-ui-react](https://github.com/uzabase/mitsubachi-ui-react) — React 版（プライベート） / [Storybook](https://uzabase.github.io/mitsubachi-ui-react/)
- [mitsubachi-token](https://github.com/uzabase/mitsubachi-token) — デザイントークン
