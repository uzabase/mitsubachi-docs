# icon-button

icon-button は、テキストを持たずアイコンのみで操作を表現するコンパクトなボタンコンポーネントです。

## 使いどころと選び方

### 使うべきシーン
- 検索・閉じる・編集・削除など、アイコンの意味が広く共有されている操作を配置する場合
- スペースが限られており、テキストラベルを配置できない場所（ヘッダー・ツールバー・カード右上など）
- 他のUI要素と並べて配置する場合

### 使わないほうがよいシーン
- アイコンだけでは意味が伝わりにくいアクション（ツールチップで補完できない場合は、テキスト付きの [neutral-button](./neutral-button.md) を使います）
- ページ内でもっとも重要な主要アクション（[floating-button](./floating-button.md) の使用を検討します）

### 他コンポーネントとの違い・使い分け
- **[floating-button](./floating-button.md) との違い**: floating-button は画面に固定（fixed）で常時浮かんで表示されますが、icon-button はページ内のコンテンツフローやUI要素と並べて配置します。スクロールしても消えずに表示し続けたい主要アクションには floating-button、他のUI要素と組み合わせて使う場合は icon-button を選びます

## Figma

- コンポーネント: https://www.figma.com/design/kHQNLM1dnk0EhZwOKBEBkL/Base-Component-Speeda-3.1-MITSUBACHI?node-id=5831-6556
- 各variantの値は Figma MCP（`get_design_context`）で取得

> mockup で再現する場合は `mockup/mitsubachi-mockup.css` の `.mi-icon-button` を使う（自作しない）。
> クリックでメニューを開く用途では、ネイティブ要素を使わず [menu](../menu/index.md)（`.mi-menu`）をトリガーに紐づける。開閉JSは [mockup/README.md](../../mockup/README.md) の「メニューの実装パターン」を参照。

## 構成とルール

### バリエーション・状態

| プロパティ | 値 |
|---|---|
| variant | `primary` / `secondary` / `tertiary` / `ghost` |
| size | `small` / `medium` / `large` |
| selected | `true` / `false`（secondary・tertiary・ghost のみ） |
| state | `default` / `hover` / `active` / `focus` / `loading` / `disabled` |

#### variant（重要度・強調度）
- `primary`: 塗りつぶし背景で最も視覚的に目立つスタイルです。ページ内で強調したい操作に使います
- `secondary`: 強いボーダーを持ち、塗りつぶしのない輪郭スタイルです
- `tertiary`: 薄いボーダーを持つ、控えめなスタイルです
- `ghost`: ボーダーも背景もなく、最も目立たないスタイルです。インタラクション時のみ背景が現れます

#### size（サイズ）
- `small`: 小さなコンポーネント（input-chip・snackbar など）の内部や、スペースが特に限られた箇所に使います
- `medium`: ツールバーや検索エリアなど、コンパクトながらも操作しやすい場面に使います
- `large`: ヘッダーやバナーなど、十分な視認性とタップ領域を確保したい場面に使います

#### selected（選択状態）
secondary・tertiary・ghost では `selected` プロパティにより選択済み状態を表現できます。フィルタのオン/オフやトグル操作を伴う場面で使います。primary では `selected` は使いません。

| variant | selected 対応 |
|---------|:------------:|
| **secondary** | ✅ |
| **tertiary** | ✅ |
| **ghost** | ✅ |
| **primary** | — |

#### state（インタラクション状態）
button 共通です。詳細は [button](./index.md) を参照してください。

### コンテンツルール
- アイコンのみで構成します。テキストラベルは持ちません
- 配置するアイコンは 1 つです
- アイコンの意味が視覚的に伝わりにくいため、必ずツールチップと組み合わせて使います
- loading 状態では、アイコンの代わりに loading コンポーネントが自動的に表示されます
- `aria-label` を必ず付ける

## 振る舞い
- **クリック/タップ時**: active 状態を経てアクションを実行します。処理中は loading 状態に遷移します
- **ホバー時**: hover 状態に遷移し、インタラクティブであることを視覚的にフィードバックします
- **フォーカス時**: フォーカスリングが表示され、キーボードで操作中の位置を明示します。`Enter` または `Space` キーでアクションを実行します
- **loading 状態**: ボタンは操作を受け付けません。処理が完了すると default 状態に戻ります
- **disabled 状態**: ボタンは操作を受け付けません。なぜ操作できないかを周辺のUIやツールチップで伝えます

## Do

- アイコンの意味が広く共有されている操作に限定して使う（検索・閉じる・編集など）
- 必ずツールチップと組み合わせて使う
- 必ず `aria-label` を付ける

## Don't

- アイコンだけでは意味が伝わりにくいアクションに使わない
- テキストラベルが必要な場面で icon-button を使わない → [neutral-button](./neutral-button.md) を使う
- `aria-label` を省略しない

## 役割と目的
- **解決する課題**: スペースが限られた場所で、アイコンを通じて操作のエントリーポイントを提供します
- **UI上での基本的な役割**: クリック/タップ可能なアイコンによるアクション起点として機能します
- **ユーザーにとっての意味**: 視覚的に認識しやすいアイコンで素早くアクションできます
