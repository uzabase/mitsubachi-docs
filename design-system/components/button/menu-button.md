# menu-button

menu（複数の操作や遷移先をリスト形式で提示するコンポーネント）を表示するためのトリガーとなるボタンコンポーネントです。

## いつ使うか

- 1つのボタンから複数の操作（アクション）を提供したいとき
- クリックで menu を開き、ユーザーに次のアクションを選ばせたいとき

## いつ使わないか

- 単一のアクションを実行する場合 → [neutral-button](./neutral-button.md)
- 「何が選ばれているか」という選択状態を示す場合 → select-box を使う
- フォームの選択肢としてオプションを提示する場合 → select-box を使う
- 値の選択には使わない（選択状態を持たず、アクションの起点として機能する）

## Figma

- コンポーネント: https://www.figma.com/design/kHQNLM1dnk0EhZwOKBEBkL/Base-Component-Speeda-3.1-MITSUBACHI?node-id=8301-3447
- 各variantの値は Figma MCP（`get_design_context`）で取得

## バリアントプロパティ

| プロパティ | 値 | 説明 |
|-----------|-----|------|
| variant | primary / secondary / ghost | バリアント |
| size | medium / large / x-large | サイズ |
| state | default / hover / active / focus / loading / disabled | インタラクション状態 |

## variant の使い分け

| variant | 使いどころ |
|---------|-----------|
| **primary** | 最も強調度の高いスタイル |
| **secondary** | 標準的なスタイル |
| **ghost** | 視覚的に控えめなスタイル |

## コンテンツルール

- ラベル（label）はボタンがトリガーする操作の内容を端的に示すテキストを設定する。1行に収まる長さとする
- 先頭アイコン（leading icon）は任意。ラベルの意味を補完する場合に使用する
- 末尾アイコン（trailing icon）は chevron-down アイコンが常に表示される。メニューが展開可能であることをユーザーに示す
- menu 展開中は chevron アイコンが上向きに反転する

## Do

- 複数のアクションを提示したい場合に使う
- ラベルは操作の内容を端的に示す
- `aria-haspopup="menu"` と `aria-expanded` を適切に設定する

## Don't

- 値の選択に menu-button を使わない → select-box を使う
- 単一のアクションに menu-button を使わない → [neutral-button](./neutral-button.md) を使う
- ラベルを長文にしない — 1行に収まる長さにする
