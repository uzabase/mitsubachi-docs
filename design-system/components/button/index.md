# button

ユーザーのアクションをトリガーするコンポーネント群。

> mockup で再現する場合は `mockup/mitsubachi-mockup.css` の `.mi-button--*` / `.mi-icon-button` / `.mi-floating-button` を使う（自作しない）。

## 使い分け

| コンポーネント | 用途 |
|---|---|
| [neutral-button](./neutral-button.md) | 送信・保存・確認など汎用的な操作 |
| [danger-button](./danger-button.md) | 削除・リセットなど破壊的操作 |
| [ai-button](./ai-button.md) | AI生成・提案など生成系AIのトリガー |
| [icon-button](./icon-button.md) | テキストなし、アイコンのみの操作 |
| [menu-button](./menu-button.md) | 複数アクションをドロップダウンで提示 |
| [floating-button](./floating-button.md) | 画面に常時浮かぶ主要アクション |

## 共通ルール

### 配置

- primary を右、secondary を左に配置する
- ボタン間隔は 8px

### ラベル

- 「保存する」「削除する」のような短い動詞句で書く
- 「OK」「実行」のような曖昧なラベルは避け、結果を予測できる表現にする
- 説明が必要な場合はボタンの外に書く

