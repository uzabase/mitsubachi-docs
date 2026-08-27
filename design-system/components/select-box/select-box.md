# select-box

select-box は、あらかじめ定められた選択肢の中から単一の値を選択するための入力コンポーネントです。現在選択されている値をトリガー領域に表示し、クリックすると選択肢を含むメニューが展開します。

## いつ使うか

- フォーム内で、あらかじめ確定した選択肢から1つを選ばせるとき
- 現在の選択値を常にトリガーに表示しておく必要があるとき
- 住所の都道府県選択、設定画面の言語設定、表示件数の切り替えなど

## いつ使わないか

- 複数の値を同時に選択させる場合（→ [checkbox](../checkbox/index.md) を使います）
- ユーザーがテキストを入力しながら候補を動的に絞り込む場合（→ [search-box](../search-box.md) と [suggestion](../suggestion.md) を使います）
- アクション（保存・削除・移動など操作）の一覧を提示する場合（→ [menu-button](../button/menu-button.md) を使います）
- **[menu-button](../button/menu-button.md) との違い**：menu-button はアクションを呼び出すためのトリガーであり、選択状態を持ちません。select-box は「現在何が選ばれているか」という値を表示・保持する点が異なります
- **[suggestion](../suggestion.md) との違い**：suggestion は入力テキストに応じて候補を動的に絞り込む補完UIです。select-box は事前に確定した固定の選択肢から選ばせる場合に使います

## Figma

- コンポーネント: https://www.figma.com/design/kHQNLM1dnk0EhZwOKBEBkL/Base-Component-Speeda-3.1-MITSUBACHI?node-id=8257-5204

> mockup で再現する場合は `mockup-kit/mitsubachi-mockup.css` の `.mi-select` を使う（自作しない）。枠なし・auto 幅の補助的な見た目には `.mi-select--secondary`、size は既定が medium で小さくする場合は `.mi-select--small`、タッチ操作向けには `.mi-select--phone` を付ける。`.mi-select` はネイティブ `<select>` なので、クリックで開く選択肢メニュー（active 状態）を再現する場合は `.mi-menu` ＋ select-menu-item（選択中は `.mi-menu-item--selected` ＋ check）で組む（位置決めはモック側）。展開メニューの見本は `mockup-kit/components/menu.html` を読んでマークアップ構造を踏襲する。

## バリアントプロパティ

| プロパティ | 値 | 説明 |
|---|---|---|
| viewport | desktop / phone | 表示環境 |
| size | medium / large | サイズ |
| state | default / hover / active / focus / disabled | インタラクション状態 |

### Viewport（表示環境）
- `desktop`：デスクトップ向けのレイアウトで表示されます
- `phone`：スマートフォン向けにレイアウトが調整されます

### Size（サイズ）
- `medium`：標準サイズです
- `large`：やや大きなサイズです。タッチ操作が主なモバイル向けや、視覚的な存在感を高めたい場面に適しています
- ※Figma 実体の size は small / medium です（kit のクラスは `.mi-select`＝medium、`.mi-select--small`＝small に対応します）

### State（状態）
- `default`：通常の選択待ち状態です
- `hover`：マウスポインターが乗っている状態です
- `active`：menu が展開されている状態です
- `focus`：フォーカスが当たっている状態です
- `disabled`：操作不能な状態です

## コンテンツルール

- 何も選択されていない初期状態では、プレースホルダーテキストを表示します
- 選択後は選択した値のラベルテキストを表示します
- 末尾には chevron-down-small アイコン（下向きの山形記号。20px）が常に表示されます。menu が展開中（active 状態）は上向きに反転します
- プレースホルダーは「選択してください」のように選択を促す文言にします

## Do

- フォーム内であらかじめ確定した選択肢から1つを選ばせる場面で使う
- 現在の選択値を常にトリガーに表示しておく
- プレースホルダーは「選択してください」のように選択を促す文言にする

## Don't

- 複数の値を同時に選択させる場面で使わない → [checkbox](../checkbox/index.md) を使う
- ユーザーがテキスト入力で候補を絞り込む場面で使わない → [search-box](../search-box.md) と [suggestion](../suggestion.md) を使う
- アクションの一覧を提示する場面で使わない → [menu-button](../button/menu-button.md) を使う
