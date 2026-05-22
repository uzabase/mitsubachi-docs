# radio-button-text-group

radio-button-text-group は、複数のradio-button-textをまとめて**1つの選択グループ**として扱うコンポーネントです。選択肢の並び方（横並び・縦並び）をコントロールし、バリデーションエラー時にはグループの下部にエラーメッセージ（helper-text）を表示します。

## いつ使うか

- 複数のradio-button-textを一つの選択グループとしてまとめて表示する場合。
- 選択肢の整列方向（横・縦）を指定したい場合。
- バリデーションエラーをグループ全体に表示したい場合。

## いつ使わないか

- ラベルとセットで表示する場合は [radio-button-text-group-unit](./radio-button-text-group-unit.md) を使います。

## Figma

- コンポーネント: https://www.figma.com/design/kHQNLM1dnk0EhZwOKBEBkL/Base-Component-Speeda-3.1-MITSUBACHI?node-id=1-182

## バリアントプロパティ

| プロパティ | 値 | 説明 |
|---|---|---|
| direction | horizontal / vertical | 配置方向 |
| state | default / error | グループ全体の状態 |

## variant の使い分け

### direction（配置方向）

| 値 | 使いどころ |
|---|---|
| **horizontal** | 選択肢を横並びに表示します。エリア幅に入りきらない場合は折り返します。 |
| **vertical** | 選択肢を縦並びに表示します。選択肢が多い場合や、ラベル文字数が多い場合に向いています。 |

### state（グループ全体の状態）

| 値 | 使いどころ |
|---|---|
| **default** | 通常の状態。 |
| **error** | バリデーションエラーがある状態。グループの下部に helper-text（エラーメッセージ）が表示されます。 |

## コンテンツルール

- グループ内の radio-button-text の数に制限はありませんが、多すぎると選択しにくくなるため、選択肢の絞り込みを検討します。
- エラーメッセージ（helper-text）は選択肢を選ぶまでの指示や、未選択の原因を簡潔に伝える内容にします。

## Do

- radio-button-card-groupとの違いを理解して使い分ける。radio-button-card-group はサポートテキスト（補足情報）を含むカード型のradio-buttonです。radio-button-text-group はradio-buttonとラベルを組み合わせたコンポーネントです。
- [../checkbox/checkbox-text-group.md](../checkbox/checkbox-text-group.md) との違いを理解して使い分ける。checkbox-text-group は複数選択が可能です。radio-button-text-group は常に1つの選択肢が選ばれる排他的選択のみです。

## Don't

- ラベルとセットで表示する場面で単体で使わない → [radio-button-text-group-unit](./radio-button-text-group-unit.md) を使う
