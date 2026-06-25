# radio-button-card-group

radio-button-card-group は、複数の [radio-button-card](./radio-button-card.md) をまとめて**1つの選択グループ**として扱うコンポーネントです。各選択肢はカード形式で表示され、ラベルに加えてサポートテキスト（補足情報）を表示できます。

## 使いどころと選び方

### 使うべきシーン
- 選択肢に補足説明（サポートテキスト）が必要な場合。
- 各選択肢間の違いや内容を視覚的に強調して伝えたい場合。
- ラベルとセットで使う場合は [radio-button-card-group-unit](./radio-button-card-group-unit.md) を使います。

### 使わないほうがよいシーン
- 補足説明が不要でラベルのみで十分な場合は [radio-button-text-group](./radio-button-text-group.md) を使います。
- 同時に複数を選択する必要がある場合は [checkbox-text-group](../checkbox/checkbox-text-group.md) を使います。

### 他コンポーネントとの違い・使い分け
- **[radio-button-text-group](./radio-button-text-group.md) との違い**：radio-button-text-group はラベルのみを表示します。radio-button-card-group はカード形式で補足情報も表示できます。選択肢の内容をより詳しく説明したい場合に適しています。
- **[checkbox-text-group](../checkbox/checkbox-text-group.md) との違い**：radio-button-card-group は常に1つの選択肢だけが選ばれる排他的選択です。

## Figma

- コンポーネント: https://www.figma.com/design/kHQNLM1dnk0EhZwOKBEBkL/Base-Component-Speeda-3.1-MITSUBACHI?node-id=1-182

> mockup で再現する場合は `mockup/mitsubachi-mockup.css` の `.mi-radio-card-group` を使う（自作しない）。

## 構成とルール

### バリエーション・状態

| プロパティ | 値 |
|---|---|
| direction | `horizontal` / `vertical` |
| state | `default` / `error` |
| viewport | `desktop` / `phone` |

#### direction（配置方向）
- `horizontal`：選択肢を横並びに表示します。全カードが等分で幅を分け合います。
- `vertical`：選択肢を縦並びに表示します。カードが幅いっぱいに広がります。

#### state（グループ全体の状態）
- `default`：通常の状態。
- `error`：バリデーションエラーがある状態。グループの下部に helper-text（エラーメッセージ）が表示されます。

#### viewport（表示環境）
- `desktop`：デスクトップ向けのテキストサイズで表示します。
- `phone`：スマートフォン向けのテキストサイズ（やや大きめ）で表示します。

#### 選択状態の視覚表現
- 未選択：白背景・やや濃いボーダー
- 選択済み：淡い青背景・薄いボーダー

### コンテンツルール
- 各カードのラベル（選択肢名）は選択肢が明確に伝わる簡潔な表現にします。
- サポートテキストは選択肢の補足説明や特徴を簡潔に述べます。長すぎる内容はカードの高さを増やし、横並びのインターフェースでは列の高さがそろわなくなるため、できるだけ簡潔にします。
- エラーメッセージ（helper-text）は、選択肢を選ぶまでの指示や未選択の原因を簡潔に伝える内容にします。

## 振る舞い
- グループ内の radio-button-card は排他的選択で、常に1つのカードだけが選ばれます。
- カードをクリック・タップすると選択状態に切り替わり、背景色とボーダー色が変化します。
- `error` 状態では helper-text がグループの下部に自動で表示されます。

## Do

- 各カードのラベルは選択肢が明確に伝わる簡潔な表現にする
- サポートテキストは簡潔にまとめる

## Don't

- 補足説明が不要な場面でカード型グループを使わない → [radio-button-text-group](./radio-button-text-group.md) を使う
- サポートテキストを長くしすぎない（横並びでカードの高さがそろわなくなる）

## 役割と目的
radio-button-card-group は、複数の radio-button-card をまとめて**1つの選択グループ**として扱うコンポーネントです。
- 各選択肢はカード形式で表示され、ラベルに加えてサポートテキスト（補足情報）を表示できます。
- 選択肢の内容や違いを視覚的にわかりやすく伝えるため、単純なラベルだけでは伝えきれない選択肢に適しています。
- viewport プロパティにより、デスクトップ・スマートフォンそれぞれに適したテキストサイズで表示できます。
