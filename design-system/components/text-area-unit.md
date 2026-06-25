# text-area-unit

text-area-unit は、ラベル（label-unit）と複数行入力欄（[text-area](./text-area.md)）をセットにしたコンポーネントです。フォームの1項目（「何を入力するか」を示すラベルと実際の入力欄）をまとめて表現します。

## 使いどころと選び方

### 使うべきシーン
- フォーム上でラベル付きの複数行テキスト入力欄を表示するとき
- 入力必須項目であることを明示したいとき
- 入力内容に関する補足説明をラベルの近くに表示したいとき

### 使わないほうがよいシーン
- ラベルを表示する必要がなく、入力欄単体で十分な場合は、text-area を直接使用します
- 1行以内に収まる短い入力項目には、[text-field-unit](./text-field-unit.md) を使用します

### 他コンポーネントとの違い・使い分け
- [text-area](./text-area.md) は入力欄のみを提供します。text-area-unit はこれに label-unit を組み合わせ、ラベル・必須バッジ・補足テキストを含むフォーム項目をワンセットで表現します。通常のフォーム項目では、text-area 単体ではなく text-area-unit を使用します。
- [text-field-unit](./text-field-unit.md) は1行入力専用です。複数行の入力項目には text-area-unit を使用します。

## Figma
- コンポーネント: https://www.figma.com/design/kHQNLM1dnk0EhZwOKBEBkL/Base-Component-Speeda-3.1-MITSUBACHI?node-id=10775-10483
- 各variantの値は Figma MCP（`get_design_context`）で取得

<!-- TODO: mockup kit のクラス有無を確認 -->

## 構成とルール

### バリエーション・状態

| プロパティ | 値 |
|---|---|
| viewport | `desktop` / `phone` |
| size | `medium` / `large` |

#### viewport（表示環境）
- `desktop`：デスクトップ向けのレイアウトで表示されます
- `phone`：スマートフォン向けにレイアウトが調整されます

#### size（サイズ）
- `medium`：標準サイズです
- `large`：やや大きなサイズです。label-unit と text-area の両方に size が適用されます

#### 入力欄の状態
入力欄の状態（default / hover / focus / error / error-hover / error-focus / disabled）は、内包する text-area の仕様に準じます。詳細は [text-area](./text-area.md) のドキュメントを参照してください。

## 振る舞い
- 入力欄をクリック・タップするとフォーカスが当たり、キーボードによる文字入力が可能になります
- label-unit のラベルテキストをクリックした場合も、入力欄にフォーカスが当たります
- 入力欄の各状態（hover・focus・disabled など）の振る舞いは text-area の仕様に準じます

## 役割と目的
- text-area-unit は、label-unit と [text-area](./text-area.md) をセットにしたコンポーネントです。フォームの1項目（「何を入力するか」を示すラベルと実際の入力欄）をまとめて表現します。
- ラベルによって入力内容の意味を明確にし、ユーザーが迷わず操作できるようにします
- 必須バッジ（required）で入力必須項目であることを明示します
- 補足テキスト（support-text）で入力に関する補足情報をラベルと併せて表示できます
