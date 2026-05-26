# ai-button

AIによる生成・提案・自動補完など、生成系AIを実行する操作に限定して使用するボタンコンポーネントです。

## いつ使うか

- AIによる文章生成・要約・翻訳などを実行する操作
- AI提案・自動補完の適用を実行する操作
- 生成系AIが処理を担うアクション全般

## いつ使わないか

- AI以外の通常の操作 → [neutral-button](./neutral-button.md)
- 削除・リセットなど破壊的な操作 → [danger-button](./danger-button.md)
- アイコンのみで操作を表現したい場合 → [icon-button](./icon-button.md)

## Figma

- コンポーネント: https://uzabase.github.io/mitsubachi-ui/?path=/story/button-mi-ai-button--basic
- 各variantの値は Figma MCP（`get_design_context`）で取得

## バリアントプロパティ

| プロパティ | 値 | 説明 |
|-----------|-----|------|
| variant | primary / secondary | 重要度・強調度 |
| size | medium / large / x-large | サイズ |
| state | default / hover / active / focus / loading / disabled | インタラクション状態 |

## variant の使い分け

| variant | 使いどころ |
|---------|-----------|
| **primary** | 画面内でもっとも重要なAIアクション。1画面に1つが原則 |
| **secondary** | primary の次に重要なAIアクション、または補助的なAIアクション |

## コンテンツルール

- テキストラベルは必須。AIが実行するアクションの内容を端的に表す動詞句で記述する（例：「AI生成する」「要約する」）
- アイコンは magic-fill アイコンが固定で表示される。任意のアイコンへの差し替えはできない
- AI実行以外の用途には使用しない

## Do

- AI機能のトリガーには必ず ai-button を使う
- ラベルでAIが実行する内容を明確に伝える

## Don't

- AI以外の操作に ai-button を使わない — 通常の操作には [neutral-button](./neutral-button.md) を使う
- アイコンを差し替えない — magic-fill アイコンは固定
- 破壊的操作にAIボタンを使わない — AIによる操作であっても、削除等には [danger-button](./danger-button.md) を使う
