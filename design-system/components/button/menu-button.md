# menu-button

menu-button は、menu（複数の操作や遷移先をリスト形式で提示するコンポーネント）を表示するためのトリガーとなるボタンコンポーネントです。

## 使いどころと選び方

### 使うべきシーン
- クリックで menu を開き、ユーザーに次のアクションを選ばせたいとき
- 例：ファイル形式を選択してダウンロードさせたいとき
- 例：ユーザーを招待する際に、メールアドレスを個別に指定して招待するか、CSVファイルをアップロードして一括招待するかを選ばせたいとき

### 使わないほうがよいシーン
- 単一のアクションを実行する場合（→ [button](./index.md) を使います）
- 「何が選ばれているか」という選択状態を示す場合（→ select-box を使います）
- フォームの選択肢としてオプションを提示する場合（→ select-box を使います）

### 他コンポーネントとの違い・使い分け
- **[button](./index.md) との違い**: button は単一のアクションを直接実行します。menu-button はクリックで menu を展開し、複数の選択肢を提示する点が異なります
- **select-box との違い**: select-box は現在選択中の値を表示し、値を選ばせる目的で使います。menu-button は選択状態を持たず、アクションの起点となります

## Figma

- コンポーネント: https://www.figma.com/design/kHQNLM1dnk0EhZwOKBEBkL/Base-Component-Speeda-3.1-MITSUBACHI?node-id=8301-3447
- 各variantの値は Figma MCP（`get_design_context`）で取得

> mockup で再現する場合は `mockup/mitsubachi-mockup.css` の `.mi-button--menu`（+ variant 併用） を使う（自作しない）。size は neutral-button と同じ `.mi-button--medium/--large/--x-large`（既定=medium）。末尾の chevron は size に追従（medium 18 / large 20 / x-large 22px）。
> 展開リストは [menu](../menu/index.md)（`.mi-menu`）で構成し、ネイティブ `<select>`/`<details>` は使わない。開閉JSは [mockup/README.md](../../mockup/README.md) の「メニューの実装パターン」を参照。

## 構成とルール

### バリエーション・状態

| プロパティ | 値 |
|---|---|
| variant | `primary` / `secondary` / `ghost` |
| size | `medium` / `large` / `x-large` |
| state | `default` / `hover` / `active` / `focus` / `loading` / `disabled` |

#### variant（重要度）
- `primary`: 「送信」「保存」「購入」「次へ」 など、画面内で最も強く促したいアクションに使います。主アクションがない画面では置かないことも正しい選択です
- `secondary`: primary の次に重要なアクションに使用します。primary が無い画面では、secondary が事実上その画面の最上位ボタンとして機能します
- `ghost`: 背景に馴染む控えめなスタイルです。複数並んでも煩雑に見えないため、リストのすべての行に配置したりできます

#### size（サイズ）
- `medium`: 標準的なサイズです。一覧、テーブル行内、ツールバー、カード内アクション、一般的な画面のボタンなど、最も汎用的な場面に使用します。特に、多くのボタンが並ぶ画面では medium に統一し、画面全体の密度・リズムを整えます

#### state（状態）
button 共通です。詳細は [button](./index.md) を参照してください。

### コンテンツルール
- **ラベル（label）**: ボタンがトリガーする操作の内容を端的に示すテキストを設定します。1行に収まる長さとします
- **先頭アイコン（leading icon）**: 任意で追加できます。ラベルの意味を補完する場合に使用します
- **末尾アイコン（trailing icon）**: chevron-down アイコンが常に表示されます。メニューが展開可能であることをユーザーに示します
- disabled 状態では、操作ができない理由をツールチップなどで補足することを検討します

## 振る舞い
- クリック（タップ）すると、関連する menu が展開します
- menu が展開中（active 状態）は、末尾の chevron アイコンが上向きに反転します
- menu が閉じると、ボタンは default 状態に戻ります
- loading 状態では、ラベルと chevron アイコンの代わりにローディングインジケーターが表示されます
- hover 時にボタンの背景色が変化します
- focus 時にフォーカスリングが表示されます
- disabled 状態ではクリック・キーボード操作どちらも無効となります
- キーボードの `Enter` または `Space` でメニューを開閉できます

## Do

- 複数のアクションを提示したい場合に使う
- ラベルは操作の内容を端的に示す
- `aria-haspopup="menu"` と `aria-expanded` を適切に設定する

## Don't

- 値の選択に menu-button を使わない → select-box を使う
- 単一のアクションに menu-button を使わない → [neutral-button](./neutral-button.md) を使う
- ラベルを長文にしない — 1行に収まる長さにする

## 役割と目的
- クリック（またはタップ）することで、関連する menu を展開し、ユーザーが実行できる操作の一覧を提示します
- 「操作の入り口」としての役割を担います
- 現在選択されている値を表示したり、値を選択させる目的では使用しません
