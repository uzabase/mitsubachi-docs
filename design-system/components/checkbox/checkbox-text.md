# checkbox-text

checkbox-textは、[checkbox](./checkbox.md)（選択ボックス）と選択肢の内容を示したラベルテキストを組み合わせたコンポーネントです。ユーザーに「何を選択するのか」をラベルで明示しながら、選択操作を提供します。

## いつ使うか

- 複数の選択肢にラベルが必要なすべてのケース。
- フォーム内で複数選択を受け付ける場面。

## いつ使わないか

- 複数の選択肢から必ず1つだけを選ぶ場合は、[radio-button](../radio-button/index.md) を使います。
- [checkbox](./checkbox.md) との違い：checkboxは選択ボックス単体のコンポーネントです。checkbox-textはラベルテキストとセットになっており、操作対象内にラベルも含まれます。

## Figma

- コンポーネント: https://www.figma.com/design/kHQNLM1dnk0EhZwOKBEBkL/Base-Component-Speeda-3.1-MITSUBACHI?node-id=178-267
- 各variantの値は Figma MCP（`get_design_context`）で取得

## バリアントプロパティ

| プロパティ | 値 | 説明 |
|---|---|---|
| checked | false / checked / indeterminate | 選択状態 |
| state | default / hover / active / focus / disabled | インタラクション状態 |

## variant の使い分け

### checked（選択状態）

| 値 | 使いどころ |
|---|---|
| **false** | 未選択の状態。ボックスは空白で表示されます。 |
| **checked** | 選択された状態。ボックス内にチェックマークが表示されます。 |
| **indeterminate** | 一部選択の状態。ボックス内にインジケーター（横線）が表示されます。 |

## コンテンツルール

- ラベルテキストは簡潔に、操作内容が明確に伝わる表現にします。
- ラベルの文字列が折り返すほど長い内容は非推奨です。やむを得ない限り、ラベルは1行に収まる長さにします。
- 複数行になった場合、checkboxはテキストに対して上揃えで配置されます。

## Do

- ラベルテキストは簡潔に、操作内容が明確に伝わる表現にする
- ラベルは1行に収まる長さにする

## Don't

- 複数の選択肢から必ず1つだけを選ぶ場面で使わない → [radio-button](../radio-button/index.md) を使う
- ラベルの文字列を折り返すほど長くしない
