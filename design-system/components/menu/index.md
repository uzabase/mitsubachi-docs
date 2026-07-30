# menu

ドロップダウンで表示されるアクションや選択肢のリスト。

> mockup で再現する場合は `mockup-kit/mitsubachi-mockup.css` の `.mi-menu` + `.mi-menu-item` を使う（自作しない）。項目のグループ区切りは `.mi-menu-group`（グループ間に区切り線。破壊的操作は最後のグループに分離する）、group 内のカテゴリ見出しは `.mi-menu-category`。ラベルが長い場合は折り返す（省略・truncate は禁止）。表示位置はトリガー基準で「下・左揃え」がデフォルト（位置に応じて上/右揃えに切替）。高さはページ端から16px確保し、入りきらなければスクロール。外側クリック or ESC で閉じる。 組む前に見本 `mockup-kit/components/menu.html` を読んでマークアップ構造を踏襲する。 項目に補助文を付ける場合は `.mi-menu-item__text` で包み、中に `.mi-menu-item__support` を置く（12px・行間 1.3・弱色。phone は 14px）。

## 使い分け

| コンポーネント | 用途 |
|---|---|
| [action-menu-item](./action-menu-item.md) | クリックでアクションを即時実行する項目 |
| [link-menu-item](./link-menu-item.md) | 別ページへ遷移するリンク項目 |
| [select-menu-item](./select-menu-item.md) | 選択状態（チェックマーク）を持つ項目 |
| [sub-menu-item](./sub-menu-item.md) | サブメニューを持つ項目（ネスト） |
