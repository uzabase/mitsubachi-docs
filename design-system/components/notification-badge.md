# notification-badge

未読件数や通知件数をアイコンやナビゲーション要素に付与して視覚的に示すためのコンポーネントです。

## いつ使うか

- ナビゲーションアイコンやヘッダーの [icon-button](./button/icon-button.md) に未読件数・通知件数を表示するとき
- ユーザーが確認すべき通知の存在を示したいとき。件数が重要な場合は数値表示、存在だけを伝える場合はドット表示を選択する

## いつ使わないか

- ステータスや属性を示すラベルとして使う場合 → [tag](./tag/index.md) を使用する
- 通知と関係のない件数や数値を表示する目的には使用しない

## Figma

- コンポーネント: https://www.figma.com/design/kHQNLM1dnk0EhZwOKBEBkL/Base-Component-Speeda-3.1-MITSUBACHI?node-id=10748-4969
- 各variantの値は Figma MCP（`get_design_context`）で取得

> mockup で再現する場合は `mockup/mitsubachi-mockup.css` の `.mi-badge`（右上重ねは `.mi-badge-anchor`） を使う（自作しない）。

## バリアントプロパティ

| プロパティ | 値 |
|---|---|
| count | true / false |

## count の使い分け

| count | 使いどころ |
|-------|-----------|
| **true**（数値表示） | 通知件数を数値で表示する。件数が 0 のときは非表示 |
| **false**（ドット表示） | 件数を問わず、通知の存在のみを示す点状のバッジ |

## コンテンツルール

- 数値表示（count: true）の場合の桁数ルール:
  - 1〜9: そのまま表示する
  - 10〜99: そのまま表示する
  - 100以上: 99+ と表示する
  - 0: バッジを非表示にする
- 親要素の右上に重ねて配置する

## Do

- 通知の存在を伝える目的に使う
- 件数が重要な場合は count: true、存在だけを伝える場合は count: false を使い分ける

## Don't

- ステータスや属性のラベルとして使わない → [tag](./tag/index.md) を使う
- 通知と関係のない数値表示に使わない
