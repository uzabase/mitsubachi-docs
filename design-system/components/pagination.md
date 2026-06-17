# pagination

pagination（ページネーション）は、大量のデータやコンテンツを複数のページに分割し、ユーザーがページ単位で内容を切り替えて閲覧できるようにするナビゲーションコンポーネントです。

## いつ使うか
- テーブルやリスト形式で表示するデータが多く、一画面に収まらない場合
- ユーザーが前後のページや特定のページへ移動する必要がある場合

## いつ使わないか
- コンテンツ量が少なく、1ページで収まる場合は不要です
- 無限スクロールや「さらに読み込む」で代替するほうが適切な場合（例：フィードやタイムライン形式のコンテンツ）
- [select-box](./select-box/index.md)（セレクトボックス、ドロップダウン選択UI）: pagination 内でページ番号の選択に使用します。pagination 単体のコンポーネントとして select-box をそのまま利用するのではなく、pagination コンポーネントを通じて使います
- [icon-button](./button/icon-button.md): 「前へ」「次へ」の操作ボタンとして pagination 内部で使用します

## Figma
- コンポーネント: https://www.figma.com/design/kHQNLM1dnk0EhZwOKBEBkL/Base-Component-Speeda-3.1-MITSUBACHI?node-id=8909-6683
- 各variantの値は Figma MCP（`get_design_context`）で取得

> mockup で再現する場合は `mockup/mitsubachi-mockup.css` の `.mi-pagination` を使う（自作しない）。

## バリアントプロパティ
| プロパティ | 値 |
|---|---|
| viewport | `desktop` / `phone` |

## variant の使い分け

### viewport（表示対象デバイス）
| viewport | 配置ルール |
|---|---|
| `desktop` | 表やリストの下に配置します（デフォルト）。大量のデータを扱う場合は、リストの上部にも配置できます |
| `phone` | リストの下部のみに配置します。上部への配置はしません。中央揃えで配置します |

### Disabled状態のルール
- 先頭ページを表示している時 → 「前へ」ボタンが Disabled になります
- 最後のページを表示している時 → 「次へ」ボタンが Disabled になります

## コンテンツルール
- 「前へ」「次へ」ボタンには、それぞれ操作内容を補足する [tooltip](./tooltip.md)（ツールチップ、ホバー時に表示される補足テキスト）を表示します
- ページ番号は全ページ数とともに表示します（例: 1 / 10）

## Do
- テーブルやリストの下に配置する
- ページ番号と全ページ数を合わせて表示する

## Don't
- コンテンツ量が少なく1ページで収まる場合に使わない
- モバイルでリストの上部に配置しない
