# action-menu-item

action-menu-item は、クリックするとアクション（コマンド）を即座に実行するメニューアイテムです。選択後に値を保持しません（選択肢の記憶が不要な操作に使います）。

## 使いどころと選び方

### 使うべきシーン
- コピー、削除、編集、移動、ダウンロードなど、クリックで即時実行されるコマンドを提供するとき
- 操作の結果として値が保持されない場合

### 使わないほうがよいシーン
- 選択状態（チェックマーク）を表示・保持したい場合（→ [select-menu-item](./select-menu-item.md) を使います）
- ページ遷移が必要な場合（→ [link-menu-item](./link-menu-item.md) を使います）
- サブメニューを持たせたい場合（→ [sub-menu-item](./sub-menu-item.md) を使います）

### 他コンポーネントとの違い・使い分け
- **[select-menu-item](./select-menu-item.md) との違い**：action-menu-item は選択状態を持ちません。選択中の状態をチェックマークで示す必要がある場合は select-menu-item を使います。
- **[link-menu-item](./link-menu-item.md) との違い**：action-menu-item はアクションを実行します。href による URL 遷移には link-menu-item を使います。

## Figma

- コンポーネント: https://www.figma.com/design/kHQNLM1dnk0EhZwOKBEBkL/Base-Component-Speeda-3.1-MITSUBACHI?node-id=8376-4715

> mockup で再現する場合は `mockup/mitsubachi-mockup.css` の `.mi-menu-item` を使う（自作しない）。削除など破壊的操作を赤文字で示す場合は `.mi-menu-item--danger`、スマートフォン向けには `.mi-menu-item--phone` を付ける。

## 構成とルール

### バリエーション・状態

#### State
- `default`：通常の状態。
- `hover`：マウスカーソルが重なっている状態。オーバーレイで視覚フィードバックを表示します。
- `active`：クリック・タップ中の状態。
- `focus`：フォーカスされている状態。フォーカスリングで視覚化します。
- `disabled`：操作不可の状態。グレーアウトで表示されます。

#### Show icon
- アイコンの有無を切り替えられます（任意）

### コンテンツルール
- ラベルはアクションを端的に表す動詞または動詞句で記述します（例：「コピー」「削除する」）
- ラベルは1行に収まる長さとします
- disabled 状態では理由をツールチップなどで補足することを検討します

## 振る舞い

- クリック（タップ）でアクションが実行されます。アクション実行後、[menu](./index.md) は閉じます
- hover 時に背景色が変化します
- キーボードの上下矢印キーでフォーカスを移動できます
- Enter または Space でアクションが実行されます
- disabled 状態ではクリック・キーボード操作どちらも無効となります

## Do

- ラベルはアクションの結果を予測できる動詞句にする
- [select-menu-item](./select-menu-item.md) との違いを意識し、選択状態が不要な操作に使う

## Don't

- 選択状態を保持する用途に使わない → [select-menu-item](./select-menu-item.md) を使う
- ページ遷移に使わない → [link-menu-item](./link-menu-item.md) を使う

## 役割と目的
- ユーザーがクリックすると、コピー・削除・移動などのコマンドが実行される、または次のダイアログへ進みます
- 選択後に値を保持しません（選択肢の記憶が不要な操作に使います）
- [menu](./index.md) コンポーネント内で使うアイテムとして機能します
