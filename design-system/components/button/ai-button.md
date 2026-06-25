# ai-button

ai-button は、AIによる生成・提案・自動補完など、生成系AIを実行する操作に限定して使用するボタンコンポーネントです。

## 使いどころと選び方

### 使うべきシーン
- AIによる文章生成・要約・翻訳などを実行する操作
- AI提案・自動補完の適用を実行する操作
- 生成系AIが処理を担うアクション全般

### 使わないほうがよいシーン
- AI以外の通常の操作 → [neutral-button](./neutral-button.md) を使用
- 削除・リセットなど破壊的な操作 → [danger-button](./danger-button.md) を使用
- アイコンのみで操作を表現したい場合 → [icon-button](./icon-button.md) を使用

### 他コンポーネントとの違い・使い分け
- **[neutral-button](./neutral-button.md) との違い**: neutral-button はAI以外の汎用操作に使用します。ai-button はAI実行に限定された専用ボタンです
- **[danger-button](./danger-button.md) との違い**: danger-button は破壊的操作の警告を伝えるためのボタンです。AIによる操作であっても、破壊的操作ではない限り ai-button を使用します

## Figma

- コンポーネント: https://www.figma.com/design/kHQNLM1dnk0EhZwOKBEBkL/Base-Component-Speeda-3.1-MITSUBACHI?node-id=8357-5237
- 各variantの値は Figma MCP（`get_design_context`）で取得

> mockup で再現する場合は `mockup/mitsubachi-mockup.css` の `.mi-button--primary/--secondary` + `.mi-icon--magic-fill` を使う（自作しない）。

## 構成とルール

### バリエーション・状態

| プロパティ | 値 |
|---|---|
| variant | `primary` / `secondary` |
| size | `medium` / `large` / `x-large` |
| state | `default` / `hover` / `active` / `focus` / `loading` / `disabled` |

#### variant（重要度・強調度）
- `primary`: 画面内でもっとも重要なAIアクションに使用します。1画面に1つが原則です
- `secondary`: primary の次に重要なAIアクション、または補助的なAIアクションに使用します

#### size
- `medium`: 標準的なサイズです
- `large`: やや大きいサイズです
- `x-large`: 最も大きいサイズです

#### state
button 共通です。詳細は [button](./index.md) を参照してください。

### コンテンツルール
- テキストラベルは必須です。AIが実行するアクションの内容を端的に表す動詞句で記述します（例：「AI生成する」「要約する」）
- アイコンは magic-fill アイコンが固定で表示されます。任意のアイコンへの差し替えはできません
- AI実行以外の用途には使用しません

## 振る舞い
- **クリック／タップ時**: active 状態を経てAI処理を実行します。処理中は loading 状態に遷移します
- **ホバー時**: hover 状態に遷移し、インタラクティブであることを視覚的にフィードバックします
- **フォーカス時**: フォーカスリングを表示し、キーボード操作での位置を明示します。`Enter` キーまたは `Space` キーでアクションを実行します
- **loading 状態**: AI処理実行中はボタンの操作を受け付けません。処理が完了すると default 状態に戻ります
- **disabled 状態**: ボタンの操作を受け付けません。操作できない理由をユーザーに伝える手段を別途検討します

## Do

- AI機能のトリガーには必ず ai-button を使う
- ラベルでAIが実行する内容を明確に伝える

## Don't

- AI以外の操作に ai-button を使わない — 通常の操作には [neutral-button](./neutral-button.md) を使う
- アイコンを差し替えない — magic-fill アイコンは固定
- 破壊的操作にAIボタンを使わない — AIによる操作であっても、削除等には [danger-button](./danger-button.md) を使う

## 役割と目的
- **解決する課題**: AIが関与するアクションを通常の操作ボタンと視覚的に区別し、「AIによる処理が発生する」ことを明確に伝えます
- **UI上での基本的な役割**: AI生成・提案・補完などのトリガーとなるエントリーポイントを提供します
- **ユーザーにとっての意味**: ボタンを押すとAIが動作することを事前に認識でき、安心して操作できます
