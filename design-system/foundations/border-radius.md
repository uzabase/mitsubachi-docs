# Border Radius

角丸の値を定義するトークン。

## Figma
- https://www.figma.com/design/DqZ5hW947kqhcIFQrp0QTA/Token-Speeda-3.1-MITSUBACHI?node-id=1-4

## 基本ルール

- 基本的には下記と設定する
- 特殊コンポーネントは2px以外の値が適用されることがあり、コンポーネント設計していくなかで随時整理していく方針
- 検討状況での値は確定次第追加される(Tokenを増やす方向に考える)

## Primitive Token | ワンスピーダ

| 値 | 倍率 | 使用トークン | 使用プロダクト | 備考 |
|----|------|-------------|--------------|------|
| 2px | 0.25x | border-radius | スタートアップ情報リサーチ... | 化粧品類・チェックボックス |
| 4px | 0.5x | border-radius, Spacing | 経済情報リサーチ、開発企業 | 未定/空室・table/block・text等 |
| 6px | 0.75x | border-radius | | 検討優先 ボタン |
| 8px | 1x | border-radius, Spacing | 経済情報リサーチ、開発企業 | 未定/空室・テーブル・モラン |

## Semantic Token

| Primitive Token | Semantic Token |
|-----------------|----------------|
| dimension-scale-10 (2px) | border-radius-2x-small |
| dimension-scale-20 (4px) | border-radius-x-small |
| dimension-scale-30 (6px) | border-radius-small |
| dimension-scale-40 (8px) | border-radius-medium |

## 使い分け

| 値 | 用途 |
|----|------|
| **2px** | 小さい要素（チェックボックス、小さいタグなど） |
| **4px** | 標準的な要素（カード、入力フィールドなど） |
| **6px** | ボタン |
| **8px** | 大きめの要素（モーダル、大きいカードなど） |
