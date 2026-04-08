# チェックボックス

複数の選択肢から任意の数を選べる入力コンポーネント。

## Figma
- コンポーネント: https://www.figma.com/design/kHQNLM1dnk0EhZwOKBEBkL/Base-Component-Speeda-3.1-MITSUBACHI?node-id=0-1
- Do / Don't は Figma ページ内の「仕様」フレームを参照

## 使い分け

### チェック状態
| checked | 説明 |
|---------|------|
| **false** | 未選択 |
| **checked** | 選択済み |
| **indeterminate** | 一部選択（親チェックボックスで子の一部が選択されている状態） |

### ラジオボタンとの使い分け
| コンポーネント | 使いどころ |
|--------------|-----------|
| **Checkbox** | 複数選択可。0個選択もOK |
| **Radio Button** | 1つだけ選択。必ず1つ選ぶ必要がある |

## グループの配置

複数のチェックボックスをまとめる場合：

| direction | 使いどころ |
|-----------|-----------|
| **horizontal** | 選択肢が少なく、横幅に余裕がある場合 |
| **vertical** | 選択肢が多い場合、または選択肢のラベルが長い場合 |

## アクセシビリティ
- `<input type="checkbox">` を使う（カスタム要素で代用しない）
- グループには `<fieldset>` と `<legend>` を使う
- indeterminate 状態は `aria-checked="mixed"` で伝える
- ラベルは `<label>` で関連付ける（クリック範囲が広がる）

## 並べ方
- チェックボックスとラベルの間隔は 4px
- 選択肢同士の間隔は vertical の場合 8px、horizontal の場合 16px
- エラー時はグループ全体の下にエラーメッセージを表示
