# テーブル

データを行と列で構造化して表示するコンポーネント。

## Figma
- コンポーネント: https://www.figma.com/design/kHQNLM1dnk0EhZwOKBEBkL/Base-Component-Speeda-3.1-MITSUBACHI?node-id=6055-16930
- Do / Don't は Figma ページ内の「仕様」フレームを参照

> mockup で再現する場合は `mockup-kit/mitsubachi-mockup.css` の `.mi-table`（list 表示は `--list`） を使う（自作しない）。セルの種類は th/td に付ける: 数値列 `.mi-table__num`（右寄せ）/ 行見出し `.mi-table__row-header`（太字）/ 行選択の checkbox 列 `.mi-table__check`（中に `.mi-checkbox`）/ 行アクションの icon-button 列 `.mi-table__actions`。値が無いセル（Null）は既定で「–」（en dash）を表示する（文言指定があればそれに従う）。任意要素のセル（slot）は td に直接置く。増減つき数値セルは値の下に `.mi-tag--positive/--negative`（矢印アイコン＋ラベル）を縦組みで置く（文字色は変えない）。 組む前に見本 `mockup-kit/components/table.html` を読んでマークアップ構造を踏襲する。

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
| **empty / Null** | 値が無いセル | **既定は「–」（en dash）を表示**。文言の指定があればそれに従う（例: AI Agent の「競合企業を分析する」）（Figma「Nullについて」107-8889 由来） |

### 状態
| state | 説明 |
|-------|------|
| **default** | 通常状態 |
| **hover** | マウスオーバー時（行単位でハイライト） |
| **selected** | 選択された行 |

## 振る舞い
- **ソート**: ソート可能な列はヘッダーの**セル全体をクリック**でトグルする（Default → 昇順 → 降順 → 解除）。「解除」は昇順でも降順でもない状態で、そのときの並び順はテーブル次第（作成順・手動順など）。各状態に tooltip を併用する。ソート機能がない列のヘッダーには hover 等の状態変化を付けない
- **カラムに対するアクション**: ヘッダーセルから action-menu（`.mi-menu`）を開いて列単位の操作を提供できる（旧 control-menu は非推奨・削除予定）
- **行 hover**: 任意のセルを hover すると行全体がハイライト。目的は「視線のガイド・情報の読み違い防止・認知負荷の低減」
- **セル内リンク**: 文字列や数値のリンクは text-link のルールに従う。**セル全体をリンクにはしない**（現状の Speeda では使わない）
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
