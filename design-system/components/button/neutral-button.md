# neutral-button

neutral-button は、プロダクト内で最も標準的に使用する基本のボタンコンポーネントです。画面内の主要なアクションや一般的な操作に使用します。

## 使いどころと選び方

### 使うべきシーン
- 送信・保存・確認など、通常の実行操作をユーザーに促す場合
- [danger-button](./danger-button.md) や [ai-button](./ai-button.md) では意味づけが強すぎる、汎用的なアクションに使用する場合
- 複数のアクションを並置する場合（primary・secondary など variant で重要度を区別）
- ページ内でフォームや設定変更の完了ボタンとして配置する場合

### 使わないほうがよいシーン
- 削除・リセットなど取り消しが困難な破壊的操作（→ [danger-button](./danger-button.md) を使用）
- AIによる生成・提案を実行する操作（→ [ai-button](./ai-button.md) を使用）
- テキストを持たずアイコンのみで操作を表現したい場合（→ [icon-button](./icon-button.md) を使用）
- 画面に常時浮かんで表示する主要アクション（→ [floating-button](./floating-button.md) を使用）

### 他コンポーネントとの違い・使い分け
- **[danger-button](./danger-button.md) との違い**: neutral-button は破壊的操作には使用しません。削除・無効化などリスクを伴うアクションには danger-button を選択します
- **[ai-button](./ai-button.md) との違い**: AI実行に特化したアクションには ai-button を使用します。neutral-button は AI に限らない汎用操作に使います
- **[floating-button](./floating-button.md) との違い**: floating-button はページに固定表示される円形ボタンです。コンテンツのフロー内に配置するボタンには neutral-button を使用します
- **[icon-button](./icon-button.md) との違い**: テキストラベルを持たずアイコンのみで操作を表現する場合は icon-button を使用します

## Figma

- コンポーネント: https://www.figma.com/design/kHQNLM1dnk0EhZwOKBEBkL/Base-Component-Speeda-3.1-MITSUBACHI?node-id=178-3446
- 各variantの値は Figma MCP（`get_design_context`）で取得

> mockup で再現する場合は `mockup/mitsubachi-mockup.css` の `.mi-button--primary/--secondary/--tertiary/--ghost/--plane` を使う（自作しない）。処理中（loading）を示す場合は全 variant 共通で `.mi-button--loading` を付け、中に `<span class="mi-loading">` を置く。

## 構成とルール

### バリエーション・状態

| プロパティ | 値 |
|---|---|
| variant | `primary` / `secondary` / `tertiary` / `ghost` / `plane` |
| size | `medium` / `large` / `x-large` |
| selected | `true` / `false` |
| state | `default` / `hover` / `active` / `focus` / `loading` / `disabled` |

#### variant（重要度・強調度）
- `primary`: 「送信」「保存」「購入」「次へ」 など、画面内で最も強く促したいアクションに使います。主アクションがない画面では置かないことも正しい選択です
- `secondary`: primary の次に重要なアクションに使用します。primary が無い画面では、secondary が事実上その画面の最上位ボタンとして機能します
- `tertiary`: 補助的なアクションや重要度の低い操作に使用します。複数並んでも煩雑に見えないため、リストのすべての行に配置したりできます
- `ghost`: 背景に馴染む控えめなスタイルです。primary を使う最重要ボタンと対になる「キャンセル」などでも使用します
- `plane`: 最も視覚的な存在感を抑えたスタイルです。ほぼテキストリンクに近い見た目（「詳細を見る」「すべて表示」などのインライン操作）

#### size
- `medium`: 標準的なサイズです。一覧、テーブル行内、ツールバー、カード内アクション、一般的な画面のボタンなど、最も汎用的な場面に使用します。特に、多くのボタンが並ぶ画面では medium に統一し、画面全体の密度・リズムを整えます
- `large`: やや大きいサイズです。dialog やフォームの主要アクションなど、「その場で意思決定・確定をさせたい」文脈で使用します
- `x-large`: 最も大きいサイズです。ログインやユーザー登録など、「迷わせず、容易に押させたい」ことを最優先する単独・主目的の画面で使います

#### selected
- `true`: 選択中の状態を示します
- `false`: 選択されていない通常の状態です

| variant | selected 対応 |
|---------|:------------:|
| **secondary** | ✅ |
| **tertiary** | ✅ |
| **ghost** | ✅ |
| **primary** | — |
| **plane** | — |

#### state
button 共通です。詳細は [button](./index.md) を参照してください。

### コンテンツルール
- テキストラベルは必須です。ボタンの目的を端的に表す動詞句で記述します（例：「保存する」「送信する」）
- アイコンはオプションです。テキストラベルと組み合わせて使用します。アイコンのみの構成にはできません（→ [icon-button](./icon-button.md)）
- テキストラベルは簡潔に保ちます。長い文章はラベルとして使用しません

## 振る舞い
- **クリック／タップ時**: active 状態を経てアクションを実行します。処理中は loading 状態に遷移します
- **ホバー時**: hover 状態に遷移し、インタラクティブであることを視覚的にフィードバックします
- **フォーカス時**: フォーカスリングを表示し、キーボード操作での位置を明示します。`Enter` キーまたは `Space` キーでアクションを実行します
- **loading 状態**: アクション実行中はボタンの操作を受け付けません。処理が完了すると default 状態に戻ります
- **disabled 状態**: ボタンの操作を受け付けません。操作できない理由をユーザーに伝える手段を別途検討します
- **selected 状態**: 選択・アクティブな状態を視覚的に示します。トグルのような操作に使用します

## Do

- ラベルは「保存する」「送信する」のような短い動詞句にする
- 複数ボタンを並べるときは variant で重要度を区別する
- primary は 1 画面に 1 つだけ使う
- primary を右、secondary を左に配置する
- ボタン間隔は 8px

## Don't

- primary ボタンを 1 画面に複数配置しない
- 破壊的操作に neutral-button を使わない → [danger-button](./danger-button.md) を使う
- ラベルを長文にしない — 説明が必要な場合はボタンの外に書く
- ラベルを曖昧にしない —「OK」「実行」ではなく「保存」「削除」など結果を予測できるラベルを付ける
- 配置を画面ごとに変えない — 主要アクションは右、キャンセルは左
- アイコンのみの構成にしない（→ [icon-button](./icon-button.md)）

## 役割と目的
- **解決する課題**: 特定の意味（危険・AI生成など）を持たない汎用的なボタンが必要な場面に対応します
- **UI上での基本的な役割**: 画面内のあらゆるアクションのエントリーポイントとして機能します
- **ユーザーにとっての意味**: ラベルを通じてアクションの内容を明示し、操作への誘導を担います
