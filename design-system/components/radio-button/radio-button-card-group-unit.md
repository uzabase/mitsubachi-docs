# radio-button-card-group-unit

radio-button-card-group-unit は、[label-unit](../label-unit.md)（ラベル・補足テキスト・必須表示）と [radio-button-card-group](./radio-button-card-group.md) を組み合わせたコンポーネントです。フォームにおける「ラベル付きのカード型ラジオボタングループ」として機能し、ユーザーが「何を選ぶのか」を明確に理解した上で選択できるようにします。

## いつ使うか

- フォーム内でラベルとカード型ラジオボタングループをセットで表示する場合。
- 選択肢に「必須」を表示したい場合。
- 選択内容に関する補足説明が必要な場合。

## いつ使わないか

- ラベルが不要でグループだけを表示する場合は [radio-button-card-group](./radio-button-card-group.md) を使います。
- [radio-button-text-group-unit](./radio-button-text-group-unit.md) との違い：内容の補足情報（サポートテキスト）が必要な場合は radio-button-card-group-unit を使います。ラベルのみで充分な場合は radio-button-text-group-unit を使います。

## Figma

- コンポーネント: https://www.figma.com/design/kHQNLM1dnk0EhZwOKBEBkL/Base-Component-Speeda-3.1-MITSUBACHI?node-id=1-182

> mockup で再現する場合は `mockup/mitsubachi-mockup.css` の `.mi-radio-card-group`（+ `.mi-label-unit`） を使う（自作しない）。

## バリアントプロパティ

| プロパティ | 値 | 説明 |
|---|---|---|
| direction | horizontal / vertical | 配置方向 |
| viewport | desktop / phone | 表示環境 |

## variant の使い分け

### direction（配置方向）

| 値 | 使いどころ |
|---|---|
| **horizontal** | 選択肢を横並びに表示します。 |
| **vertical** | 選択肢を縦並びに表示します。 |

### viewport（表示環境）

| 値 | 使いどころ |
|---|---|
| **desktop** | デスクトップ向けの表示。 |
| **phone** | スマートフォン向けの表示。カード内のテキストサイズがやや大きくなります。 |

## コンテンツルール

- [label-unit](../label-unit.md) のラベルテキストは、選択肢の内容（何を選ぶか）が導かれる簡潔な表現にします。
- [label-unit](../label-unit.md) の補足テキスト（support text）は必要な場合のみ表示します。入力内容の補足説明や制約を簡潔に述べます。
- 選択必須な場合は required を true に設定し、「必須」バッジを表示します。

## Do

- ラベルテキストは選択肢の内容が導かれる簡潔な表現にする
- 補足テキストは必要な場合のみ表示する

## Don't

- ラベルが不要な場面で使わない → [radio-button-card-group](./radio-button-card-group.md) を使う
