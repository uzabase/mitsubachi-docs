# AI チャット

AI との対話を表示するコンポーネント。

## 使いどころと選び方

AI が生成した回答や、ユーザーからの質問を表示する専用の UI。通常のチャットやコメント機能には使わない。

### 他コンポーネントとの違い・使い分け
| 種類 | 用途 |
|------|------|
| **ai-chat** | ページ内に埋め込んで使う場合 |
| **floating-ai-chat** | 画面上にフローティングで表示する場合 |

## Figma
- コンポーネント: https://www.figma.com/design/kHQNLM1dnk0EhZwOKBEBkL/Base-Component-Speeda-3.1-MITSUBACHI?node-id=9336-8319
- Do / Don't は Figma ページ内の「仕様」フレームを参照

> mockup で再現する場合は `mockup/mitsubachi-mockup.css` の `.mi-ai-chat`（+ `__messages`/`__user-message`/`__answer`/`__input`/`__disclaimer`） を使う（自作しない）。

## 構成とルール

### 構成要素
| 要素 | 用途 |
|------|------|
| **ユーザーメッセージ** | ユーザーが入力した質問・指示を表示 |
| **AI メッセージ** | AI が生成した回答を表示 |
| **ローディング** | AI が回答を生成中であることを示す |

### コンテンツルール
- メッセージは時系列で上から下に並べる
- ユーザーとAIのメッセージは視覚的に区別する（配置や背景色）
