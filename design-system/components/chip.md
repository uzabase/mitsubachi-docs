
# チップ

フィルタリングや入力済みの値を表示するコンパクトなコンポーネント。

## Figma
- コンポーネント: https://www.figma.com/design/kHQNLM1dnk0EhZwOKBEBkL/Base-Component-Speeda-3.1-MITSUBACHI?node-id=5305-1950
- Do / Don't は Figma ページ内の「仕様」フレームを参照

## 使い分け

### 種類
| 種類 | 用途 |
|------|------|
| **filter-chip** | フィルター条件の選択・解除に使う。ON/OFF でフィルターを切り替える |
| **input-chip** | ユーザーが入力・選択した値を表示する。削除ボタンで取り消せる |

### filter-chip の選択モード
| モード | 動作 |
|--------|------|
| **Single select** | 1つだけ選択可。他を選ぶと自動で切り替わる。「すべて」を必ず設ける |
| **Multi select** | 複数選択可。未選択状態もOK |

## 振る舞い

### filter-chip
- 選択中は `selected=true` になる
- Single select では未選択状態を許容しない。フィルタ解除には「すべて」を選ぶ
- Multi select では個別に ON/OFF できる

### input-chip
- 削除ボタン（×）をクリックすると削除できる
- 削除中は Loading 状態を表示できる
- 親要素よりも長いテキストは省略記号（...）で切り詰める

## アクセシビリティ
- filter-chip は `role="checkbox"` または `role="radio"` を付ける（選択モードに応じて）
- input-chip の削除ボタンには `aria-label="〇〇を削除"` を付ける
- キーボードで選択・削除できるようにする

## 並べ方
- チップ同士の間隔は 8px
- 親要素の幅を超える場合は折り返して表示する（横スクロールしない）
- filter-chip-group、input-chip-group でまとめる
