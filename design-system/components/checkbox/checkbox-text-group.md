# checkbox-text-group

checkbox-text-groupは、複数の [checkbox-text](./checkbox-text.md)（チェックボックスとラベルの組み合わせ）を一つのグループとしてまとめるコンポーネントです。複数の選択肢を水平方向（horizontal）または垂直方向（vertical）に並べて表示します。

## いつ使うか

- 複数のcheckbox-textを流れに沿って並べたい場合。
- フォーム内で複数選択をまとめてグループ化する場合。
- エラー状態の表示が必要な入力グループに使用します。

## いつ使わないか

- ラベル（入力内容の説明）や入力必須表示が必要な場合は、[checkbox-text-group-unit](./checkbox-text-group-unit.md) を使います。
- [checkbox-text-group-unit](./checkbox-text-group-unit.md) との違い：checkbox-text-groupは選択肢のグループのみです。[label-unit](../label-unit.md)（ラベル・必須表示・補足テキスト）を含めたセットとして使う場合はcheckbox-text-group-unitを使います。

## Figma

- コンポーネント: https://www.figma.com/design/kHQNLM1dnk0EhZwOKBEBkL/Base-Component-Speeda-3.1-MITSUBACHI?node-id=5133-21598
- 各variantの値は Figma MCP（`get_design_context`）で取得

## バリアントプロパティ

| プロパティ | 値 | 説明 |
|---|---|---|
| direction | horizontal / vertical | 配置方向 |
| state | default / error | グループの状態 |

## variant の使い分け

### direction（配置方向）

| 値 | 使いどころ |
|---|---|
| **horizontal** | 水平方向に並びます。コンテナの幅に応じて折り返しが発生します。 |
| **vertical** | 垂直方向に一列で並びます。 |

## コンテンツルール

- グループ内のcheckbox-textは複数配置できます。
- **水平方向では**、checkbox-text内のラベル文字列の折り返しは禁止です。checkbox-textを一かたまりとして折り返すのは許可されます。
- **垂直方向では**、checkbox-text内のラベル文字列の折り返しが許可されます。

## Do

- 水平方向ではラベル文字列を1行に収める
- エラー状態時にはhelper-textにエラー内容を表示する

## Don't

- 水平方向でラベル文字列を折り返さない
- ラベルや必須表示が必要な場合にcheckbox-text-groupを単体で使わない → [checkbox-text-group-unit](./checkbox-text-group-unit.md) を使う
