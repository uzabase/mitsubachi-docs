# select-box-unit

select-box-unit は、ラベル（label-unit）と選択入力欄（select-box）をセットにしたコンポーネントです。フォームの1項目として「何を選択するか」を示すラベルと実際の選択入力欄をまとめて表現します。

## いつ使うか

- フォーム上でラベル付きの選択入力欄を表示するとき
- 必須項目であることを明示したいとき
- 選択内容に関する補足説明（選択形式や制約など）をラベルの近くに表示したいとき

## いつ使わないか

- ラベルを表示する必要がなく、選択入力欄単体で十分な場合は、[select-box](./select-box.md) を直接使用します
- 複数の値を同時に選択させる場合は、チェックボックスグループなど別のコンポーネントを使用します
- ユーザーがテキストを入力しながら候補を動的に絞り込む場合は、search-box-unit を使用します
- select-box は選択入力欄のみを提供します。select-box-unit はこれに label-unit を組み合わせ、ラベル・必須バッジ・補足テキストを含むフォーム項目をワンセットで表現します。通常のフォーム項目では、select-box 単体ではなく select-box-unit を使用します。

## Figma

- コンポーネント: https://www.figma.com/design/kHQNLM1dnk0EhZwOKBEBkL/Base-Component-Speeda-3.1-MITSUBACHI?node-id=8257-5204

> mockup で再現する場合は `mockup/mitsubachi-mockup.css` の `.mi-select` + `.mi-label-unit` を使う（自作しない）。

## バリアントプロパティ

| プロパティ | 値 | 説明 |
|---|---|---|
| viewport | desktop / phone | 表示環境 |
| size | medium / large | サイズ。label-unit と select-box の両方に適用されます |

### Viewport（表示環境）
- `desktop`：デスクトップ向けのレイアウトで表示されます
- `phone`：スマートフォン向けにレイアウトが調整されます

### Size（サイズ）
- `medium`：標準サイズです
- `large`：やや大きなサイズです。タッチ操作が主なモバイル向けや、視覚的な存在感を高めたい場面に適しています。label-unit と select-box の両方に size が適用されます

### 選択入力欄の状態
選択入力欄の状態（default / hover / active / focus / disabled）は、内包する [select-box](./select-box.md) の仕様に準じます。詳細は select-box のドキュメントを参照してください。

## コンテンツルール

### label-unit のコンテンツ
- ラベルテキスト（text）は、選択項目の名称を簡潔に示す文言にします。ユーザーが何を選択するかが一目でわかる言葉を選びます
- 必須バッジ（required）は、入力が必須の項目にのみ表示します。任意項目には表示しません
- 補足テキスト（support-text）は、選択形式の説明や制約など、操作を助ける補足情報を入れます

### select-box のコンテンツ
- 何も選択されていない初期状態では、プレースホルダーテキストを表示します
- 選択後は選択した値のラベルテキストを表示します
- プレースホルダーは「選択してください」のように選択を促す文言にします

## Do

- フォーム項目としてラベル付きの選択入力欄を表示する場面で使う
- 必須項目には必須バッジを表示する
- ラベルテキストは選択項目の名称を簡潔に示す

## Don't

- ラベルが不要な場面では使わない → [select-box](./select-box.md) を直接使う
- 複数の値を同時に選択させる場面で使わない
