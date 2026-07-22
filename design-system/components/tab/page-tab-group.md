# page-tab-group

page-tab-group（ページタブグループ）は、複数の page-tab（ページタブ）をまとめて管理するためのコンテナコンポーネントです。page-tab の並びを水平方向に整理し、ページレベルのナビゲーション構造を形成します。

## いつ使うか

- page-tab-group は、[page-tab](./page-tab.md) の親コンポーネントとして常に [page-tab](./page-tab.md) とセットで使います
- グローバル検索結果のカテゴリ切り替え（例：企業 / 記事 / レポート）など、ページレベルで複数の [page-tab](./page-tab.md) を束ねる必要があるとき
- マイページのセクション間移動など、同一レベルにある複数のページを切り替えるナビゲーションを構築するとき

## いつ使わないか

- ページ内の特定セクションのみを切り替える場合は [section-tab-group](./section-tab-group.md) を使います
- タブが1つしかない場合は、グループ自体を表示しません

### 他コンポーネントとの違い・使い分け

| コンポーネント | 概要 | 切り替えスコープ |
|---|---|---|
| page-tab-group | ページ全体の表示内容を切り替えるタブのグループ | ページレベル（画面全体の文脈が変わる） |
| [section-tab-group](./section-tab-group.md) | ページ内の特定セクションの表示内容を切り替えるタブのグループ | セクションレベル（ページ構造を維持したまま） |

## Figma

- コンポーネント: https://www.figma.com/design/kHQNLM1dnk0EhZwOKBEBkL/Base-Component-Speeda-3.1-MITSUBACHI?node-id=5634-1160

> mockup で再現する場合は `mockup-kit/mitsubachi-mockup.css` の `.mi-page-tab`（並べて使う） を使う（自作しない）。

## バリアントプロパティ

| プロパティ | 値 | 説明 |
|---|---|---|
| viewport | desktop | 表示環境（desktop のみ対応。phone バリアントはありません） |

### タブの配置
- 内包する [page-tab](./page-tab.md) は横一列に並びます。折り返しは行いません

## コンテンツルール

- グループ内には1つ以上の [page-tab](./page-tab.md) を含めます
- タブは同一レベルにある複数のページを表すラベルで構成します
- page-tab（個々のタブアイテム）と page-tab-group（タブをまとめたグループ）の2つのコンポーネントで、page-tab の機能全体が構成されます

## Do

- 複数の page-tab をまとめるコンテナとして使う
- グループ内で常に1つのタブが選択された状態を維持する

## Don't

- ページ内のセクション切り替えに使わない → [section-tab-group](./section-tab-group.md) を使う
- タブが1つしかない場合はグループ自体を表示しない
