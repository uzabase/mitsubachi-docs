# helper-text-group

helper-text-group は、複数の [helper-text](./helper-text.md) をひとまとまりとして縦に並べて表示するリストコンテナコンポーネントです。

## 使いどころと選び方

### 使うべきシーン
- 1つの入力要素に対して複数のエラーメッセージや注意事項を同時に表示するとき。
- 段階的なバリデーションルールを一覧で示すとき（例：「8文字以上」「大文字を含む」など）。

### 使わないほうがよいシーン
- 表示するメッセージが1件のみの場合は、[helper-text](./helper-text.md) を直接使用します。

### 他コンポーネントとの違い・使い分け
- **[helper-text](./helper-text.md)**: メッセージが1件だけの場合は helper-text を直接使用します。複数件ある場合に helper-text-group を使用します。

## Figma
- コンポーネント: https://www.figma.com/design/kHQNLM1dnk0EhZwOKBEBkL/Base-Component-Speeda-3.1-MITSUBACHI?node-id=10771-20696
- 各variantの値は Figma MCP（`get_design_context`）で取得

<!-- TODO: mockup kit のクラス有無を確認 -->

## 構成とルール

### バリエーション・状態
- helper-text-group 自体にバリエーションはありません。内包する [helper-text](./helper-text.md) のバリエーションに依存します。
- スロット（slot）に任意の数の [helper-text](./helper-text.md) を配置します。

### コンテンツルール
- 内包する要素は [helper-text](./helper-text.md) のみです。
- 配置する [helper-text](./helper-text.md) の数に制限はありません。ただし表示するメッセージは簡潔にまとめます。

## 振る舞い
- helper-text-group 自体は操作を受け付けません。内包する各 helper-text の振る舞いに従います。
- 内包する [helper-text](./helper-text.md) の数に応じて、縦方向に伸縮します。

## 役割と目的
- helper-text-group は、複数の [helper-text](./helper-text.md) をひとまとまりとして縦に並べて表示するリストコンテナコンポーネントです。
- 1つの入力要素に対して複数のメッセージを表示する必要がある場面で使用します。
- 複数のバリデーション（入力値の検証）エラーや補足情報をまとめて表示することで、ユーザーへの情報伝達を効率化します。
