# checkbox

checkboxは、ひとつの項目に対して選択・解除を行うためのコンポーネントです。ユーザーが複数の選択肢から0個以上の項目を選べるようにします。

## いつ使うか

- ユーザーが複数の選択肢から0個以上を選択できるフォームやリスト。
- 設定のオン・オフを切り替えるインターフェース（送信ボタンで確定するフォーム内）。
- 親子関係のある選択肢において、親checkboxが子の選択状態をまとめて制御する場合（indeterminate状態を活用）。

## いつ使わないか

- 複数の選択肢から必ず1つだけを選ぶ場合は、[radio-button](../radio-button/index.md) を使います。
- 操作と同時に即座にアクションが発生する場合は、[switch](../switch.md) を使います（送信ボタンで確定するフォームにはcheckboxを使います）。
- ラベルを伴う場合は [checkbox-text](./checkbox-text.md) を使います。

## Figma

- コンポーネント: https://www.figma.com/design/kHQNLM1dnk0EhZwOKBEBkL/Base-Component-Speeda-3.1-MITSUBACHI?node-id=178-197
- 各variantの値は Figma MCP（`get_design_context`）で取得

> mockup で再現する場合は `mockup/mitsubachi-mockup.css` の `.mi-checkbox` + `.mi-checkbox-label` を使う（自作しない）。

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
| **indeterminate** | 一部選択の状態。ボックス内にインジケーター（横線）が表示されます。子要素の一部が選択されている親checkboxなどで使用します。 |

## コンテンツルール

- checkboxは選択ボックス単体のコンポーネントです。ラベルなしで使用する場合は、スクリーンリーダー向けに別途アクセシブルなラベルを設定します。
- ラベルを伴う場合は [checkbox-text](./checkbox-text.md) を使います。

## Do

- 複数選択が可能な場面で使う
- 親子関係のある選択肢ではindeterminate状態を活用する
- ラベルなしで使用する場合はアクセシブルなラベルを別途設定する

## Don't

- 複数の選択肢から必ず1つだけを選ぶ場面で使わない → [radio-button](../radio-button/index.md) を使う
- 操作と同時に即座にアクションが発生する場面で使わない → [switch](../switch.md) を使う
