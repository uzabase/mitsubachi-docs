# select-box

あらかじめ定められた選択肢の中から単一の値を選択するためのコンポーネント群。

> mockup で再現する場合は `mockup/mitsubachi-mockup.css` の `.mi-select` を使う（自作しない）。
> 展開する選択肢リストはネイティブ `<select>` を使わず、[menu](../menu/index.md)（`.mi-menu` + `.mi-menu-item` / 選択状態は select-menu-item）で構成する。開閉JSは [mockup/README.md](../../mockup/README.md) の「メニューの実装パターン」を参照。

## 使い分け

| コンポーネント | 用途 |
|---|---|
| [select-box](./select-box.md) | 選択肢の中から単一の値を選択する入力コンポーネント |
| [select-box-unit](./select-box-unit.md) | ラベルと選択入力欄をセットにしたフォーム用コンポーネント |
