# section-tab-group

section-tab-group（セクションタブグループ）は、複数の section-tab（セクションタブ）をまとめて管理するためのコンテナコンポーネントです。section-tab の並びを管理し、セクションレベルのナビゲーション構造を形成します。

## いつ使うか

- section-tab-group は、[section-tab](./section-tab.md) の親コンポーネントとして常に [section-tab](./section-tab.md) とセットで使います
- 企業詳細ページ内で財務データを「損益計算書 / 貸借対照表 / キャッシュフロー」などで切り替えるなど、ページ内のセクションで複数の [section-tab](./section-tab.md) を束ねる必要があるとき
- 国・地域別データの表示を切り替えるなど、同じ情報を異なる視点で比較・閲覧するセクションを構築するとき

## いつ使わないか

- タブの切り替えによってページ全体の文脈が変わる場合は [page-tab-group](./page-tab-group.md) を使います
- タブが1つしかない場合は、グループ自体を表示しません

### 他コンポーネントとの違い・使い分け

| コンポーネント | 概要 | 切り替えスコープ |
|---|---|---|
| [page-tab-group](./page-tab-group.md) | ページ全体の表示内容を切り替えるタブのグループ | ページレベル（画面全体の文脈が変わる） |
| section-tab-group | ページ内の特定セクションの表示内容を切り替えるタブのグループ | セクションレベル（ページ構造を維持したまま） |

## Figma

- コンポーネント: https://www.figma.com/design/kHQNLM1dnk0EhZwOKBEBkL/Base-Component-Speeda-3.1-MITSUBACHI?node-id=5634-1222

## バリアントプロパティ

| プロパティ | 値 | 説明 |
|---|---|---|
| viewport | desktop / phone | 表示環境 |

### viewport
- `desktop`：内包する section-tab が折り返して並びます
- `phone`：内包する section-tab が横一列で並び、水平スクロール可能です

### タブの配置
- desktop では、タブ数がグループ幅を超えると折り返して複数行に並びます
- phone では、タブは横一列に並び、グループ幅を超えた場合は水平スクロールで表示します

## コンテンツルール

- グループ内には1つ以上の [section-tab](./section-tab.md) を含めます
- タブは同一セクション内で切り替えるビューやカテゴリを表すラベルで構成します
- section-tab（個々のタブアイテム）と section-tab-group（タブをまとめたグループ）の2つのコンポーネントで、section-tab の機能全体が構成されます

## Do

- 複数の section-tab をまとめるコンテナとして使う
- グループ内で常に1つのタブが選択された状態を維持する
- phone バリアントでは、選択中のタブが表示されるよう自動スクロールする

## Don't

- ページ全体の文脈が変わる切り替えに使わない → [page-tab-group](./page-tab-group.md) を使う
- タブが1つしかない場合はグループ自体を表示しない
