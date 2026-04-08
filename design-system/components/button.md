# ボタン

ユーザーのアクションをトリガーするコンポーネント。

## Figma
- コンポーネント: https://www.figma.com/design/kHQNLM1dnk0EhZwOKBEBkL/Base-Component-Speeda-3.1-MITSUBACHI?node-id=3-324&t=2Rf6tpLoFdLSpkiv-1
- Do / Don't は Figma ページ内の「仕様」フレームを参照

## 使い分け

### Neutral ボタン
| variant | 使いどころ |
|---------|-----------|
| **primary** | そのページで最も重要なアクション。1 画面に 1 つだけ |
| **secondary** | primary の次に重要なアクション。キャンセル・戻るなど |
| **tertiary** | 補足的なアクション |
| **ghost** | 目立たせたくないがアクションとして必要なとき |
| **plane** | ツールバーなどコンパクトな UI に |

### Danger ボタン
削除・解除など破壊的操作に使う。実行前に必ず確認ダイアログを挟む。

### AI ボタン
AI 機能のトリガーに使う。✨アイコンは自動表示されるため、アイコンを個別指定しない。

### アイコンボタン
テキストなしでアイコンのみ表示。検索・閉じる・編集など、意味が広く共有されている操作に限定する。

### メニューボタン
複数アクションをドロップダウンで提示する。値の選択には使わない（→ Select を使う）。

## 選択状態（selected）

トグル・タブ・フィルターなど ON/OFF を示す場面で使う。

| variant | selected 対応 |
|---------|:------------:|
| **secondary** | ✅ |
| **tertiary** | ✅ |
| **ghost** | ✅ |
| **primary** | — |
| **plane** | — |
| **Danger** | — |
| **AI** | — |

## アクセシビリティ
- アイコンボタンには必ず `aria-label` を付ける
- `<button>` 要素を使う（`<div>` で代用しない）

## 並べ方
- primary を右、secondary を左
- ボタン間隔は 8px
