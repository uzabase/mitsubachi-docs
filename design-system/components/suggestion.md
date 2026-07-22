# suggestion

suggestion は、検索ボックス（[search-box](./search-box.md)）や入力フィールドに対してユーザーがクリックまたはキーワードを入力した際に表示される候補リストのコンポーネントです。入力中の文字列に基づいて候補を提示し、選択による入力の補助やキーワードの補完（autocomplete）を通じて、入力の手間を減らし操作効率を高めます。

## いつ使うか
- 検索ボックスにキーワードを入力した際に、候補の一覧を文字を入力するたびにリアルタイムで更新しながら提示したいとき
- フィールドにフォーカスが当たった時点で、最近の検索履歴や推奨キーワードを提示したいとき
- 候補の性質が複数の種類に分かれる場合に、suggestion-category でグループ化して提示したいとき

## いつ使わないか
- ユーザーが入力した値に対してリアルタイムに選択肢を絞り込む [select-box](./select-box/index.md) の代替としての使用（選択肢が事前に確定している場合は [select-box](./select-box/index.md) を使います）
- 検索候補の提示ではなく、操作メニューやナビゲーションの表示目的（その場合は [menu](./menu/index.md) を使います）
- suggestion と [select-box](./select-box/index.md) はどちらもテキストフィールドと組み合わせてドロップダウン形式で選択肢を表示しますが、目的が異なります。suggestion は入力途中の補完・提案に使い、選択肢が入力内容に応じて動的に変化します。[select-box](./select-box/index.md) は事前に確定した固定の選択肢から選ばせる場合に使います
- [menu](./menu/index.md) は操作コマンドの一覧表示に使用するコンポーネントであり、検索候補の提示を目的としていません。候補リストには suggestion を使います

## Figma
- コンポーネント: https://www.figma.com/design/kHQNLM1dnk0EhZwOKBEBkL/Base-Component-Speeda-3.1-MITSUBACHI?node-id=7766-3982
- 各variantの値は Figma MCP（`get_design_context`）で取得

> mockup で再現する場合は `mockup-kit/mitsubachi-mockup.css` の `.mi-suggestion`（+ `__category`/`-item`/`__empty`） を使う（自作しない）。

## バリアントプロパティ
| プロパティ | 値 |
|---|---|
| viewport | `desktop` / `phone` |
| content-state | `default` / `empty` |

### suggestion-item のバリエーション
| プロパティ | 値 |
|---|---|
| viewport | `desktop` / `phone` |
| content-type | `text` / `slot` |
| state | `default` / `hover` / `active` / `focus` |

## variant の使い分け

### content-type（suggestion-item）
| content-type | 使いどころ |
|---|---|
| `text` | テキストのみの候補 |
| `slot` | 任意のコンテンツをスロットに挿入する候補 |

### content-state（suggestion コンテナ）
| content-state | 使いどころ |
|---|---|
| `default` | 候補がある状態 |
| `empty` | 候補がない状態（「一致する候補が見つかりません」というメッセージが表示されます） |

## コンテンツルール
- [label-unit](./label-unit.md)（コンテンツのオブジェクトを示すラベル）でオブジェクトが明示されている場合、suggestion-item のアイコンは不要です。明示されていない場合は、補足情報としてアイコンを表示します
- suggestion-category で候補の種別が明示されている場合も、suggestion-item のアイコンは不要です
- suggestion-item の性質が異なる場合は、suggestion-category でグループ化して表示します
- suggestion-item のテキストは候補の内容を簡潔に表します。過度に長いテキストは推奨しません
- suggestion-itemとsuggestion-category内のラベルが長い場合は折り返して表示します。省略してはいけません

## Do
- 検索ボックスの入力に応じて候補をリアルタイムに提示する
- 候補の種類が複数ある場合は suggestion-category でグループ化する

## Don't
- 事前に確定した固定の選択肢を表示するために使わない（select-box を使う）
- 操作メニューやナビゲーションの表示に使わない（menu を使う）
- suggestion-item のラベルを省略しない（折り返して表示する）
