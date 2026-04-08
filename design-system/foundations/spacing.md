# Spacing

要素間の余白を定義するトークン。

## Figma
- https://www.figma.com/design/DqZ5hW947kqhcIFQrp0QTA/Token-Speeda-3.1-MITSUBACHI?node-id=1-2

## Spacing とは

デザイン要素同士の余白や間隔を表現するルール。
一貫性のあるレイアウトを作成するために基準となる値を定義している。

## 使用箇所

- **padding**: 全てSpacingを使用する
- **gap**: チャートレイアウトを除き全て適用可能
- **margin**: コンポーネント・Trackingの設定から外れる所で適用可能
  - 未検討だが事業Ownのセクション一覧など一部の所を複数する
  - 例: デスク > Editor ↔ Thumbnail周辺など
- **その他**
  - width共通のグリッドシステム向けで複数の拡張が追記される
  - 高さ(min-height)に関しては別途定義がある

## Primitive Token

| Primitive | 値 |
|-----------|-----|
| dimension-scale-10 | 2px |
| dimension-scale-20 | 4px |
| dimension-scale-30 | 6px |
| dimension-scale-40 | 8px |
| dimension-scale-50 | 12px |
| dimension-scale-60 | 14px |
| dimension-scale-70 | 24px |
| dimension-scale-80 | 28px |
| dimension-scale-90 | 32px |
| dimension-scale-100 | 40px |
| dimension-scale-110 | 48px |
| dimension-scale-120 | 64px |
| dimension-scale-130 | 80px |

## Semantic Token

Semantic Token は用途に応じた名前で定義され、Primitive Token を参照する。
詳細は Figma を参照。

## 使い分けの目安

| 値 | 主な用途 |
|-----|---------|
| 2px | 極小の調整 |
| 4px | アイコンとテキストの間 |
| 8px | インライン要素間、ボタン同士の間隔 |
| 12px | コンパクトなパディング |
| 16px | 標準的なパディング、フォーム要素間 |
| 24px | カード内のパディング |
| 32px | セクション間 |
| 48px | 大きなセクション間 |
| 64px | ページセクション間 |
