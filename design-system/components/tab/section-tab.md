# section-tab

section-tab（セクションタブ）は、ページ内の特定セクションにおける表示内容を切り替えるためのナビゲーションコンポーネントです。ページ全体の構造や文脈は維持したまま、同一セクション内の情報や表示形式のみを切り替えます。

## いつ使うか

- 企業詳細ページ内で財務データを「損益計算書 / 貸借対照表 / キャッシュフロー」などで切り替えるとき
- 国・地域別データの表示を切り替えるとき（例：日本 / 海外）
- ページ内の特定セクションで、同じ情報を異なる視点や形式で比較・閲覧したいとき

## いつ使わないか

- タブの切り替えによって、ページ全体の文脈（画面全体の情報内容）が変わる場合は [page-tab](./page-tab.md) を使います
- タブが1つしかない場合は、タブ自体を表示しません

### 他コンポーネントとの違い・使い分け

| コンポーネント | 概要 | 切り替えスコープ |
|---|---|---|
| [page-tab](./page-tab.md) | ページ全体の表示内容を切り替えるタブ | ページレベル（画面全体の文脈が変わる） |
| section-tab | ページ内の特定セクションの表示内容を切り替えるタブ | セクションレベル（ページ構造を維持したまま） |

## Figma

- コンポーネント: https://uzabase.github.io/mitsubachi-ui-react/?path=/story/components-sectiontab-sectiontab--normal

## バリアントプロパティ

| プロパティ | 値 | 説明 |
|---|---|---|
| viewport | desktop / phone | 表示環境 |
| selected | true / false | 選択状態 |
| state | default / hover / active / focus / disabled | インタラクション状態 |
| show-flag | true / false | 国旗の表示状態 |

### viewport
- `desktop`：コンパクトなサイズで表示されます
- `phone`：タッチ操作を考慮した大きめのサイズで表示されます

### selected（選択状態）
- `False`（未選択）：通常の背景色で表示されます
- `True`（選択済み）：選択状態の背景色・ボーダー・テキストカラーで強調表示されます

### state（インタラクション状態）
- `default`：通常の表示
- `hover`：マウスオーバー時に背景色が変化します
- `active`：クリック／タップ中に背景色が変化します
- `focus`：キーボードフォーカス時にフォーカスリング（操作対象を示す輪郭線）が表示されます
- `disabled`：操作不能な状態。テキストが薄く表示されます

### show-flag（国旗の表示状態）
- ラベル左側に任意でフラグアイコン（国旗など）を表示できます
- disabled 状態では、フラグは半透明で表示されます

## コンテンツルール

- ラベルテキストは簡潔にまとめます。長い文字列は非推奨です
- ラベルは1行で表示されます（折り返しなし）
- section-tab は [section-tab-group](./section-tab-group.md) に内包される形で使用し、section-tab単体で使用することはありません。必ず、[section-tab-group](./section-tab-group.md) として使用します
- section-tab-group の desktop では、タブが折り返して並びます
- section-tab-group の phone では、タブが横一列で並び、水平スクロール可能です

## Do

- ページ内のセクション単位でコンテンツを切り替える場面で使う
- ラベルテキストは簡潔にまとめる
- 必ず [section-tab-group](./section-tab-group.md) に内包して使用する

## Don't

- ページ全体の文脈が変わる切り替えに使わない → [page-tab](./page-tab.md) を使う
- section-tab 単体で使用しない → [section-tab-group](./section-tab-group.md) に内包する
- タブが1つしかない場合はタブ自体を表示しない
