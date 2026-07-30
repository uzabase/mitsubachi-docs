# border-radius

コンポーネントの角丸に使用するトークン。primitive と semantic の2層で構成される。

> 具体的な値は Figma MCP（`get_variable_defs`）または [mitsubachi-token](https://github.com/uzabase/mitsubachi-token) を参照。

## primitive

- [primitive-scale](./primitive-scale.md) の dimension-scale の値を参照する
- 9999px は border-radius でのみ使用する特殊値

## semantic

- primitive の値を用途に応じて semantic 名で参照する

## 使い分け

| 用途 | semantic 名 | mockup kit の変数 | 例 |
|------|------------|------------------|-----|
| 最小サイズ。正方形のため丸すぎる印象を避けたいコンポーネント | `radius/x-small` | `--border-radius-x-small` | checkbox |
| 高さが小さいコンポーネント / コンポーネント内部の要素 | `radius/small` | `--border-radius-small` | read-only-tag, tooltip, breadcrumb, 必須バッジ |
| 基準サイズ。コンポーネントの small・medium にあたる部分 | `radius/medium` | `--border-radius-medium` | search-box, text-area, select-box, **segmented-control**, menu, banner, page-tab / section-tab, sidenav-item |
| コンポーネントの large・x-large にあたる部分 | `radius/large` | `--border-radius-large` | カード類（card, radio-button-card） |
| 最大サイズ。高さが大きめのコンポーネント | `radius/x-large` | `--border-radius-x-large` | dialog, 投資実績カード |
| pill（左右が半円） | `9999px` | `--border-radius-full` | button 類（neutral / danger / ai / icon-button）, filter-chip, input-chip, link-tag, notification-badge, switch の track |
| 真円 | `50%` | （`50%` を直接指定） | avatar, floating-button, loading, radio, switch のノブ, timeline の点 |

> **注**: 具体的な px は `mockup-kit/tokens.css` にスナップショットがある（値の正は Figma / mitsubachi-token）。
> `9999px` と `50%` は結果が違う（正方形なら同じだが、横長の要素では `50%` が楕円になる）。左右が半円の pill には `9999px` を使う。
