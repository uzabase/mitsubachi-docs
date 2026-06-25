# radio-button

複数の選択肢から1つだけを選ぶためのコンポーネント群。radio-button は円形の選択インジケーターで、上位コンポーネントを構成する内部部品（プリミティブ）として使われます。

## 使いどころと選び方

| コンポーネント | 内容 | 用途 |
|---|---|---|
| radio-button | 円形の選択インジケーター（内部部品） | 上位コンポーネントの内部部品。単体での配置は非推奨 |
| radio-button-text | radio-button + ラベルテキスト | ラベル付きのラジオボタン単体 |
| [radio-button-text-group](./radio-button-text-group.md) | radio-button-text を複数並べたグループ | 複数のradio-button-textをグループとしてまとめる |
| [radio-button-text-group-unit](./radio-button-text-group-unit.md) | label-unit + radio-button-text-group | radio-button-text-groupにラベル・必須表示・補足テキストを加えたフォーム用セット |
| [radio-button-card](./radio-button-card.md) | radio-button + カード型ラベル | カード型のラジオボタン単体。ラベルとサポートテキストを表示できる |
| [radio-button-card-group](./radio-button-card-group.md) | radio-button-card を複数並べたグループ | 複数のradio-button-cardをグループとしてまとめる |
| [radio-button-card-group-unit](./radio-button-card-group-unit.md) | label-unit + radio-button-card-group | radio-button-card-groupにラベル・必須表示・補足テキストを加えたフォーム用セット |

### 使うべきシーン
- 上位コンポーネント（radio-button-text や radio-button-card）の内部部品として自動的に使われます。
- デザイナーが直接配置する場合は、ラベルとセットになった radio-button-text を使います。

### 使わないほうがよいシーン
- radio-button 単体でUIに配置するのは非推奨です。必ず radio-button-text、または radio-button-card を使います。
- 複数選択が必要な場合は [checkbox](../checkbox/index.md) コンポーネント群を使います。

> mockup で再現する場合は `mockup/mitsubachi-mockup.css` の `.mi-radio` + `.mi-radio-label`（カード型は `.mi-radio-card`） を使う（自作しない）。

## 構成とルール

### バリエーション・状態

| プロパティ | 値 |
|---|---|
| selected | `false` / `true` |
| state | `default` / `hover` / `active` / `focus` / `disabled` |

#### selected（選択状態）
- `false`：未選択。空白の円形で表示されます。
- `true`：選択済み。円形の内側に塗りつぶしのドットを表示します。

#### state（インタラクション状態）
- `default`：通常の状態。
- `hover`：マウスカーソルが重なっている状態。オーバーレイで視覚フィードバックを表示します。
- `active`：クリック・タップ中の状態。
- `focus`：フォーカスされている状態。フォーカスリングで視覚化します。
- `disabled`：操作不可の状態。グレーアウトで表示されます。

## 振る舞い
- 円形ボタンをクリック・タップすると選択状態に切り替わります。
- 同じグループ内では必ず1つが選択され、他の選択肢を選ぶと前の選択が解除されます。
- `focus` 状態ではフォーカスリングが表示されます。

## 役割と目的
radio-button は、複数の選択肢から**1つだけ**を選択するための円形のインタラクティブ要素です。
- radio-button-text、radio-button-card など上位コンポーネントを構成する内部部品（内部層のプリミティブ）として使用します。
- 選択状態（selected）とインタラクション状態（state）に応じた視覚フィードバックを提供し、現在の選択を明確に伝えます。
