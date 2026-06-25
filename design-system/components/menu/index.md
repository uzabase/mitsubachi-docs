# menu

menu は、メニューアイテムを格納するフローティングパネル（浮動表示されるコンテナ）です。ユーザーがトリガー（button、icon-button、close-button など）を操作したときに表示され、複数の選択肢の一覧を提示します。

| コンポーネント | 用途 |
|---|---|
| [action-menu-item](./action-menu-item.md) | クリックでアクションを即時実行する項目 |
| [link-menu-item](./link-menu-item.md) | 別ページへ遷移するリンク項目 |
| [select-menu-item](./select-menu-item.md) | 選択状態（チェックマーク）を持つ項目 |
| [sub-menu-item](./sub-menu-item.md) | サブメニューを持つ項目（ネスト） |

## 使いどころと選び方

### 使うべきシーン
- 複数の選択肢をコンパクトにまとめて提示したいとき（例：カード右上の「…」ボタン、ツールバーの「ファイル」メニュー）
- アクションの選択肢をページの常時表示に適さないとき

### 使わないほうがよいシーン
- 常に表示しておくべきナビゲーションの場合（→ サイドナビゲーションなどを使います）

### 他コンポーネントとの違い・使い分け
現時点では、menu と使い分けを検討すべき比較対象のコンポーネントはありません。

## Figma

- コンポーネント: https://www.figma.com/design/kHQNLM1dnk0EhZwOKBEBkL/Base-Component-Speeda-3.1-MITSUBACHI?node-id=10771-28080

> mockup で再現する場合は `mockup/mitsubachi-mockup.css` の `.mi-menu` + `.mi-menu-item` を使う（自作しない）。

## 構成とルール

### バリエーション・状態
- 表示中 / 非表示（閉じている）の2状態のみです
- 内包するアイテムの種類は [action-menu-item](./action-menu-item.md)、[select-menu-item](./select-menu-item.md)、[link-menu-item](./link-menu-item.md)、[sub-menu-item](./sub-menu-item.md) です。これらの menu-item を、menu-item-group に内包して、menu を構成します。

### コンテンツルール
- メニューの階層は最大2階層まで（menu → sub-menu）です
- 1つの menu 内に異なる種類のアイテムを混在させることができます
- menu-item-group に見出しが必要な場合は、menu-category を使用します。

## 振る舞い

> トリガーは select-box / icon-button / menu-button など。mockup では CSS に振る舞いが無いため、開閉JSを必ず添える（[mockup/README.md](../../mockup/README.md) の「メニューの実装パターン」）。ネイティブ `<select>`/`<details>` での代用は禁止（[prohibited.md](../../foundations/prohibited.md)）。

### メニューの閉じる操作
- メニューの外側をクリックします
- ESC キーを押下します（[dialog](../dialog/index.md) の閉じる操作と共通）
- トリガーとなるボタン・アイコンを再度クリックします
- menu-item をクリックします

> メニューが表示されている状態でブラウザをスクロールしても、メニューは閉じません。

### メニューの表示位置（上下）
トリガーとなる要素を基準とした相対位置です。
- 基本：下
- 上方向：上に表示エリアが確保できないときのみ

### メニューの表示位置（左右）
- 基本：右
- 左方向：右側に表示エリアが確保できないときのみ

## 役割と目的
- アクション実行のための選択肢をコンパクトに束ねる
- ページの常時表示領域を圧迫せずに機能を提供する
- 単独では機能せず、menu-item 系コンポーネント（[action-menu-item](./action-menu-item.md) や [link-menu-item](./link-menu-item.md) など）とともに構成される
