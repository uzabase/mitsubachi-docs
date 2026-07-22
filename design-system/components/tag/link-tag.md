# link-tag

link-tag は、コンテンツの属性や分類を簡潔に示すためのコンポーネントです。タグ自体がクリック可能で、関連するカテゴリや項目へのナビゲーションリンクとして機能します。

## いつ使うか

- コンテンツのタグ・カテゴリ・分類・出所を表示し、関連コンテンツへの遷移を可能にしたい場合
- ユーザーがタグをクリックして別ページへ移動する動線が必要な場合

## いつ使わないか

- タグをクリックしても何も起きない、ナビゲーション機能が不要な場合（→ [read-only-tag](./read-only-tag.md) を使います）
- コンテンツの状態や意味的な分類（ポジティブ/ネガティブなど）を色で区別して伝えたい場合（→ [read-only-tag](./read-only-tag.md) を使います）
- **[read-only-tag](./read-only-tag.md) との違い**: link-tag はクリック可能なナビゲーションリンクです。read-only-tag はクリック不可の表示専用ラベルで、中立・情報・ポジティブ・ネガティブの意味的なバリアントを持ちます。タグに意味的な色分けが必要な場合や、クリック操作が不要な場合は read-only-tag を使います。
- **[link-tag-group](./link-tag-group.md) との関係**: 複数の link-tag を横並びにまとめて表示する場合は link-tag-group を使います。

## Figma

- コンポーネント: https://www.figma.com/design/kHQNLM1dnk0EhZwOKBEBkL/Base-Component-Speeda-3.1-MITSUBACHI?node-id=5416-7917

> mockup で再現する場合は `mockup-kit/mitsubachi-mockup.css` の `.mi-link-tag` を使う（自作しない）。

## バリアントプロパティ

| プロパティ | 値 | 説明 |
|---|---|---|
| size | x-small / small / medium | サイズ |
| state | default / hover / active / focus | インタラクション状態 |

### Size
- `x-small`: 最小サイズ。文中や文末に置く出所などは、x-smallを使用。
- `small`: 小サイズ
- `medium`: 標準サイズ

### State
- `default`: 通常表示
- `hover`: カーソルが重なった状態
- `active`: クリック中の状態
- `focus`: フォーカスが当たった状態（キーボード操作時など）

## コンテンツルール

- テキストのみで構成されます。アイコンは含みません。
- テキストはタグの内容を簡潔に表します。
- 表示するサイズはコンテキストに合わせて統一します。

## Do

- コンテンツのカテゴリや分類をクリック可能なラベルで表現する場面で使う
- テキストはタグの内容を簡潔に表す
- 表示するサイズはコンテキストに合わせて統一する

## Don't

- ナビゲーション機能が不要な場面で使わない → [read-only-tag](./read-only-tag.md) を使う
- 意味的な色分け（ポジティブ/ネガティブなど）が必要な場面で使わない → [read-only-tag](./read-only-tag.md) を使う
