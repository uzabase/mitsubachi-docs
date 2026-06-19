# dialog

ユーザーの注意を引き、確認や入力を求めるモーダルウィンドウ。

> mockup で再現する場合は `mockup/mitsubachi-mockup.css` の `.mi-dialog`（+ `.mi-dialog-backdrop`）を使う（自作しない）。スマートフォン向け（本文を大きめにし、フッターに区切り線を入れる）には `.mi-dialog--phone` を付ける。

## 使い分け

| コンポーネント | 用途 |
|---|---|
| [action-dialog](./action-dialog.md) | 削除・一括変更など、取り消し不可能なアクションの実行確認 |
| [form-dialog](./form-dialog.md) | ページ遷移せずにフォーム入力を完結させる |
| [information-dialog](./information-dialog.md) | 重要な情報やお知らせをユーザーに確実に伝える |

## 共通ルール

### Figma

- コンポーネント: https://www.figma.com/design/kHQNLM1dnk0EhZwOKBEBkL/Base-Component-Speeda-3.1-MITSUBACHI?node-id=4179-586

### デバイス別表示

| viewport | full-screen | 説明 |
|----------|:-----------:|------|
| **desktop** | false | 画面中央にオーバーレイ表示 |
| **phone** | false | 画面中央にオーバーレイ表示（幅が狭い） |
| **phone** | true | 画面全体を覆う（フルスクリーン） |

### 配置

- タイトルは上部に配置
- 本文・フォームは中央に配置
- ボタンは下部（フッター）に配置
- 主要アクションのボタンは右側、キャンセルは左側
