# サジェスト

検索ボックスに入力中、候補を表示するドロップダウンコンポーネント。

## Figma
- コンポーネント: https://www.figma.com/design/kHQNLM1dnk0EhZwOKBEBkL/Base-Component-Speeda-3.1-MITSUBACHI?node-id=7766-3982
- Do / Don't は Figma ページ内の「仕様」フレームを参照

## 使い分け

### 構成
| 要素 | 説明 |
|------|------|
| **suggestion**（コンテナ） | サジェスト全体の入れ物 |
| **suggestion-item** | 各候補項目 |
| **suggestion-category** | カテゴリ見出し（候補をグループ化する場合） |

### suggestion-item のタイプ
| content-type | 用途 |
|--------------|------|
| **text** | テキストのみの候補 |
| **slot** | カスタムコンテンツを含む候補 |

### デバイス別表示
| viewport | 説明 |
|----------|------|
| **desktop** | 標準サイズ（高さ 32px） |
| **phone** | やや大きめ（高さ 40px） |

### 状態
| state | 説明 |
|-------|------|
| **default** | 通常状態 |
| **hover** | マウスオーバー時 |
| **active** | クリック中 |
| **focus** | キーボードフォーカス時 |

### コンテンツ状態
| content-state | 説明 |
|---------------|------|
| **default** | 候補がある状態 |
| **empty** | 候補がない状態（「該当なし」などを表示） |

## 振る舞い
- search-box に文字を入力すると、キーワードに対する候補一覧が表示される
- 候補をクリックまたは Enter で選択
- 候補がない場合は empty 状態を表示
- カテゴリで候補をグループ化できる（例：「企業」「人物」など）

## アクセシビリティ
- `role="listbox"` と `role="option"` を使用する
- 矢印キーで候補間を移動できるようにする
- 選択中の候補は `aria-selected="true"` を付ける
- search-box と `aria-controls` で関連付ける
- 候補の件数を `aria-live` で通知する

## 並べ方
- search-box の直下に表示
- 幅は search-box と同じにする
- 候補が多い場合はスクロール可能にする（最大 7〜8 件程度を表示）
