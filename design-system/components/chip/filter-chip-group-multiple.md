# filter-chip-group-multiple

複数の選択肢から同時に複数の条件を選択・解除できる [filter-chip](./filter-chip.md) のグループコンポーネントです。選択するたびに条件が追加適用され、コンテンツの絞り込みに使用します。

## 使いどころと選び方

### 使うべきシーン
- 業界、地域、属性など、複数の条件を組み合わせて絞り込むとき
- ユーザーが自由に複数の条件を組み合わせたいとき

### 使わないほうがよいシーン
- 常に1つだけ選択されている必要がある場合 → [filter-chip-group-single](./filter-chip-group-single.md) を使用する
- 条件が排他的で同時に複数選べない場合
- フォームの入力として選択肢を提示する場合はチェックボックスを使用する

### 他コンポーネントとの違い・使い分け
- **[filter-chip-group-single](./filter-chip-group-single.md)**：常に1つだけ選択できます。複数同時選択が必要な場合は filter-chip-group-multiple を使います。
- **[checkbox](../checkbox/index.md)**：フォームの入力として選択肢を提示する場合は checkbox を使います。表示内容の即時絞り込みには filter-chip-group-multiple を使います。

## Figma

- コンポーネント: https://www.figma.com/design/kHQNLM1dnk0EhZwOKBEBkL/Base-Component-Speeda-3.1-MITSUBACHI?node-id=7216-14722
- 各variantの値は Figma MCP(`get_design_context`)で取得

> mockup で再現する場合は `mockup/mitsubachi-mockup.css` の `.mi-chip-group` を使う（自作しない）。

## 構成とルール

### バリエーション・状態

#### viewport
- `desktop`：デスクトップ向けのサイズで表示します。
- `phone`：スマートフォン向けのサイズで表示します。

#### size
- `medium`：現在使用できるサイズは medium のみです。

### コンテンツルール
- [filter-chip](./filter-chip.md) を子要素(slot)として受け取る
- 子要素の [filter-chip](./filter-chip.md) は横並び(折り返しあり)に配置される
- すべての選択を解除することもできる

## 振る舞い
- グループ内の [filter-chip](./filter-chip.md) をクリック/タップするたびに、その filter-chip の選択状態がトグルします。
- 他の filter-chip の選択状態は変わらず、複数の filter-chip を同時に選択した状態にできます。
- すべての選択を解除することもできます。

## Do

- 複数の条件を組み合わせた絞り込みに使用する
- ユーザーが自由に条件を追加・解除できるようにする

## Don't

- 排他的な選択(1つだけ選択)に使わない → [filter-chip-group-single](./filter-chip-group-single.md) を使う
- フォーム入力の選択肢として使わない(チェックボックスを使う)
