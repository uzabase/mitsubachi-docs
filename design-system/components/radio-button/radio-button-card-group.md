# radio-button-card-group

radio-button-card-group は、複数の [radio-button-card](./radio-button-card.md) をまとめて**1つの選択グループ**として扱うコンポーネントです。各選択肢はカード形式で表示され、ラベルに加えてサポートテキスト（補足情報）を表示できます。

## いつ使うか

- 選択肢に補足説明（サポートテキスト）が必要な場合。
- 各選択肢間の違いや内容を視覚的に強調して伝えたい場合。
- ラベルとセットで使う場合は [radio-button-card-group-unit](./radio-button-card-group-unit.md) を使います。

## いつ使わないか

- 補足説明が不要でラベルのみで十分な場合は [radio-button-text-group](./radio-button-text-group.md) を使います。
- 同時に複数を選択する必要がある場合は [../checkbox/checkbox-text-group.md](../checkbox/checkbox-text-group.md) を使います。
- radio-button-text-groupとの違い：radio-button-text-group はラベルのみを表示します。radio-button-card-group はカード形式で補足情報も表示できます。選択肢の内容をより詳しく説明したい場合に適しています。

## Figma

- コンポーネント: https://www.figma.com/design/kHQNLM1dnk0EhZwOKBEBkL/Base-Component-Speeda-3.1-MITSUBACHI?node-id=1-182

> mockup で再現する場合は `mockup-kit/mitsubachi-mockup.css` の `.mi-radio-card-group` を使う（自作しない）。

## バリアントプロパティ

| プロパティ | 値 | 説明 |
|---|---|---|
| direction | horizontal / vertical | 配置方向 |
| state | default / error | グループ全体の状態 |
| viewport | desktop / phone | 表示環境 |

## variant の使い分け

### direction（配置方向）

| 値 | 使いどころ |
|---|---|
| **horizontal** | 選択肢を横並びに表示します。全カードが等分で幅を分け合います。 |
| **vertical** | 選択肢を縦並びに表示します。カードが幅いっぱいに広がります。 |

### state（グループ全体の状態）

| 値 | 使いどころ |
|---|---|
| **default** | 通常の状態。 |
| **error** | バリデーションエラーがある状態。グループの下部に helper-text（エラーメッセージ）が表示されます。 |

### viewport（表示環境）

| 値 | 使いどころ |
|---|---|
| **desktop** | デスクトップ向けのテキストサイズで表示します。 |
| **phone** | スマートフォン向けのテキストサイズ（やや大きめ）で表示します。 |

### 選択状態の視覚表現

| 状態 | 表現 |
|---|---|
| 未選択 | 白背景・やや濃いボーダー |
| 選択済み | 淡い青背景・薄いボーダー |

## コンテンツルール

- 各カードのラベル（選択肢名）は選択肢が明確に伝わる簡潔な表現にします。
- サポートテキストは選択肢の補足説明や特徴を簡潔に述べます。長すぎる内容はカードの高さを増やし、横並びのインターフェースでは列の高さがそろわなくなるため、できるだけ簡潔にします。
- エラーメッセージ（helper-text）は、選択肢を選ぶまでの指示や未選択の原因を簡潔に伝える内容にします。

## Do

- 各カードのラベルは選択肢が明確に伝わる簡潔な表現にする
- サポートテキストは簡潔にまとめる

## Don't

- 補足説明が不要な場面でカード型グループを使わない → [radio-button-text-group](./radio-button-text-group.md) を使う
- サポートテキストを長くしすぎない（横並びでカードの高さがそろわなくなる）
