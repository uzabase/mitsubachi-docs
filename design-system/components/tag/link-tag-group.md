# link-tag-group

link-tag-group は、複数の link-tag（クリック可能なナビゲーションリンク型タグ）を一まとめに表示するコンポーネントです。複数のタグを横並びに配置してコンテンツの分類情報をまとめて表示します。

## いつ使うか

- 一つのコンテンツに複数の link-tag を並べて表示する場合
- タグの一覧表示でサイズの統一が必要な場合

## いつ使わないか

- link-tag が一つだけの場合（[link-tag](./link-tag.md) を直接使います）
- クリックできない表示専用タグを並べたい場合（[read-only-tag](./read-only-tag.md) を使います）
- **[link-tag](./link-tag.md) との関係**: link-tag-group は link-tag を内包するコンテナーです。包含する link-tag のサイズは link-tag-group のサイズで一括制御されます。

## Figma

- コンポーネント: https://www.figma.com/design/kHQNLM1dnk0EhZwOKBEBkL/Base-Component-Speeda-3.1-MITSUBACHI?node-id=5615-1410

## バリアントプロパティ

| プロパティ | 値 | 説明 |
|---|---|---|
| size | x-small / small / medium | サイズ |
| show-more | true / false | 「もっと見る」ボタンの表示 |

### サイズ
- `x-small`: 最小サイズ
- `small`: 小サイズ
- `medium`: 標準サイズ

### Show More（もっと見る）
- Show More を有効にすると、表示しきれないタグがある場合に「もっと見る」のボタンを表示します。
- Show More を無効にすると、全てのタグを表示します。

## コンテンツルール

- link-tag-group は複数の link-tag を内包します。
- 内包する link-tag のサイズは link-tag-group のサイズプロパティで一括制御されます。個別の link-tag のサイズを内側で変更しません。

## Do

- 複数の link-tag をまとめて表示する場面で使う
- サイズはグループのプロパティで一括制御する
- 表示しきれないタグがある場合は Show More を有効にする

## Don't

- link-tag が一つだけの場合は使わない → [link-tag](./link-tag.md) を直接使う
- 個別の link-tag のサイズをグループ内で変更しない
- クリックできない表示専用タグを並べる場面で使わない → [read-only-tag](./read-only-tag.md) を使う
