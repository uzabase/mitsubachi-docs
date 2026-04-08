# メニュー

ドロップダウンで表示されるアクションや選択肢のリスト。

## Figma
- コンポーネント: https://www.figma.com/design/kHQNLM1dnk0EhZwOKBEBkL/Base-Component-Speeda-3.1-MITSUBACHI?node-id=3070-328
- Do / Don't は Figma ページ内の「仕様」フレームを参照

## 使い分け

### 構成
| 要素 | 説明 |
|------|------|
| **Menu（入れ物）** | メニュー全体のコンテナ |
| **Menu Item** | メニュー内の各項目 |

### Menu Item の種類
| 種類 | 用途 |
|------|------|
| **action-menu-item** | クリックでアクションを実行する項目 |
| **link-menu-item** | 別ページへ遷移するリンク項目 |
| **multi-menu-item** | サブメニューを持つ項目（ネスト） |
| **control-menu-item** | チェックボックスやラジオボタンを含む項目 |

### サイズ
| size | 使いどころ |
|------|-----------|
| **medium** | 標準的なメニュー |
| **large** | タッチ操作が多い場合やモバイル |

## 振る舞い
- トリガー要素（ボタン等）をクリックで開く
- メニュー外をクリックで閉じる
- Escape キーで閉じる
- 項目を選択すると閉じる（control-menu-item を除く）
- multi-menu-item はホバーまたはクリックでサブメニューを開く

## アクセシビリティ
- `role="menu"` と `role="menuitem"` を使用する
- 矢印キーで項目間を移動できるようにする
- Enter または Space で項目を選択できるようにする
- 開閉状態は `aria-expanded` で示す
- disabled な項目は `aria-disabled="true"` を付ける

## 並べ方
- トリガー要素の下または上に表示（画面端では自動調整）
- 項目が多い場合はスクロール可能にする
- 関連する項目はグループ化し、区切り線で分ける
