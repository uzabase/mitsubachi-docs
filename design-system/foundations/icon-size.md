# Icon Size

アイコンのサイズを定義するトークン。

## Figma
- https://www.figma.com/design/DqZ5hW947kqhcIFQrp0QTA/Token-Speeda-3.1-MITSUBACHI?node-id=1071-307

## アイコンサイズの算出

アイコンサイズは対応するフォントサイズと紐づいている。

| 命名 | アイコンサイズ | フォントサイズ |
|------|--------------|--------------|
| icon-size-2x-small | 14px | 10px |
| icon-size-x-small | 16px | 11px |
| icon-size-small | 18px | 12px |
| icon-size-medium | 20px | 14px |
| icon-size-large | 22px | 16px |
| icon-size-x-large | 24px | 18px |
| icon-size-2x-large | 26px | 20px |
| icon-size-3x-large | 28px | 22px |
| icon-size-4x-large | 32px | 25px |
| icon-size-5x-large | 36px | 28px |
| icon-size-6x-large | 42px | 32px |
| icon-size-7x-large | 46px | 36px |
| icon-size-8x-large | 52px | 40px |
| icon-size-9x-large | 58px | 45px |
| icon-size-10x-large | 66px | 51px |

## 使い分け

| サイズ | 用途 |
|--------|------|
| **2x-small〜small** | インラインアイコン、テキスト横の補助アイコン |
| **medium** | 標準的なUIアイコン（ボタン内など） |
| **large〜x-large** | 強調したいアイコン、ナビゲーション |
| **2x-large以上** | ヒーローエリア、空状態の表示など |

## 注意点
- アイコンとテキストを並べる場合は、対応するフォントサイズを使用する
- アイコンだけのボタンには `aria-label` を必ず付ける
