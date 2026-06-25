# radio-button-text-group

radio-button-text-group は、複数の radio-button-text をまとめて**1つの選択グループ**として扱うコンポーネントです。選択肢の並び方（横並び・縦並び）をコントロールし、バリデーションエラー時にはグループの下部にエラーメッセージ（helper-text）を表示します。

## 使いどころと選び方

### 使うべきシーン
- 複数の radio-button-text を一つの選択グループとしてまとめて表示する場合。
- 選択肢の整列方向（横・縦）を指定したい場合。
- バリデーションエラーをグループ全体に表示したい場合。

### 使わないほうがよいシーン
- ラベルとセットで表示する場合は [radio-button-text-group-unit](./radio-button-text-group-unit.md) を使います。

### 他コンポーネントとの違い・使い分け
- **[radio-button-card-group](./radio-button-card-group.md) との違い**：radio-button-card-group はサポートテキスト（補足情報）を含むカード型のradio-buttonです。radio-button-text-group はradio-buttonとラベルを組み合わせたコンポーネントです。
- **[checkbox-text-group](../checkbox/checkbox-text-group.md) との違い**：checkbox-text-group は複数選択が可能です。radio-button-text-group は常に1つの選択肢が選ばれる排他的選択のみです。

## Figma

- コンポーネント: https://www.figma.com/design/kHQNLM1dnk0EhZwOKBEBkL/Base-Component-Speeda-3.1-MITSUBACHI?node-id=1-182

> mockup で再現する場合は `mockup/mitsubachi-mockup.css` の `.mi-choice-group`（縦並びは `--vertical`） を使う（自作しない）。

## 構成とルール

### バリエーション・状態

| プロパティ | 値 |
|---|---|
| direction | `horizontal` / `vertical` |
| state | `default` / `error` |

#### direction（配置方向）
- `horizontal`：選択肢を横並びに表示します。エリア幅に入りきらない場合は折り返します。
- `vertical`：選択肢を縦並びに表示します。選択肢が多い場合や、ラベル文字数が多い場合に向いています。

#### state（グループ全体の状態）
- `default`：通常の状態。
- `error`：バリデーションエラーがある状態。グループの下部に helper-text（エラーメッセージ）が表示されます。

### コンテンツルール
- グループ内の radio-button-text の数に制限はありませんが、多すぎると選択しにくくなるため、選択肢の絞り込みを検討します。
- エラーメッセージ（helper-text）は選択肢を選ぶまでの指示や、未選択の原因を簡潔に伝える内容にします。

## 振る舞い
- グループ内の radio-button-text は排他的選択で、常に1つの選択肢だけが選ばれます。
- `error` 状態では helper-text がグループの下部に自動で表示されます。
- `horizontal` 時、選択肢がエリア幅を超える場合は自動で折り返します。

## Do

- 各選択肢のラベルは選択肢の内容が明確に伝わる簡潔な表現にする
- 選択肢が多すぎる場合は絞り込みを検討する

## Don't

- ラベルとセットで表示する場面で単体で使わない → [radio-button-text-group-unit](./radio-button-text-group-unit.md) を使う

## 役割と目的
radio-button-text-group は、複数の radio-button-text をまとめて**1つの選択グループ**として扱うコンポーネントです。
- 選択肢の並び方（横並び・縦並び）をコントロールします。
- バリデーションエラーが発生した際には、グループの下部にエラーメッセージ（helper-text：ヘルパーテキスト）を表示します。
- ラベルとセットで使う場合は [radio-button-text-group-unit](./radio-button-text-group-unit.md) を使います。
