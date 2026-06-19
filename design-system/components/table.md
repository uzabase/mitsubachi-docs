# テーブル

データを行と列で構造化して表示するコンポーネント。

## Figma
- コンポーネント: https://www.figma.com/design/kHQNLM1dnk0EhZwOKBEBkL/Base-Component-Speeda-3.1-MITSUBACHI?node-id=6055-16930
- Do / Don't は Figma ページ内の「仕様」フレームを参照

> mockup で再現する場合は `mockup/mitsubachi-mockup.css` の `.mi-table`（list 表示は `--list`） を使う（自作しない）。セルの種類は th/td に付ける: 数値列 `.mi-table__num`（右寄せ）/ 行見出し `.mi-table__row-header`（太字）/ 行選択の checkbox 列 `.mi-table__check`（中に `.mi-checkbox`）/ 行アクションの icon-button 列 `.mi-table__actions`。空セルは素の `<td></td>`、任意要素のセル（slot）は td に直接置く。

## 使い分け

### ビューの種類
| 種類 | 用途 |
|------|------|
| **グリッドビュー** | 複数列のデータを一覧表示する標準的なテーブル |
| **リストビュー** | シンプルな1〜2列のデータを表示する |

### 構成パーツ
| パーツ | 説明 |
|--------|------|
| **Table Header** | 列の見出しを表示するヘッダー行 |
| **Table Row** | データを表示する各行 |
| **Table Cell** | 各セル |

### セルの種類（content-type）
| 種類 | 説明 | kit |
|------|------|-----|
| **text** | 文字（リンクにもできる） | `<td>`（リンクは中に `<a>`） |
| **number** | 数値（右寄せ・等幅数字） | `.mi-table__num` |
| **header** | 行見出し（太字） | `.mi-table__row-header`（`<th scope="row">`） |
| **checkbox** | 行選択（ヘッダー＝全選択 / 行＝選択） | `.mi-table__check`（中に `.mi-checkbox`） |
| **icon-button** | 行アクション（kebab 等） | `.mi-table__actions`（中に icon-button） |
| **slot** | 任意要素（tag・link-tag・icon 等） | `<td>` に直接置く |
| **empty** | 値が無いセル | 素の `<td></td>`（プレースホルダ記号は無し） |

### 状態
| state | 説明 |
|-------|------|
| **default** | 通常状態 |
| **hover** | マウスオーバー時（行単位でハイライト） |
| **selected** | 選択された行 |

## 振る舞い
- ヘッダーをクリックでソート可能（対応している場合）
- 行をクリックで選択または詳細へ遷移
- 横スクロール対応（列が多い場合）

## アクセシビリティ
- `<table>` 要素を使用し、適切なセマンティクスを維持する
- ヘッダーには `<th>` と `scope="col"` を使用する
- 行選択がある場合は `aria-selected` を使用する
- ソート可能な列には `aria-sort` を付ける

## 並べ方
- ページの主要コンテンツエリアに配置
- テーブルの上部にフィルターや検索ボックスを配置できる
- ページネーションはテーブルの下部に配置
