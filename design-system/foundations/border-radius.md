# border-radius

コンポーネントの角丸に使用するトークン。primitive と semantic の2層で構成される。

> 具体的な値は Figma MCP（`get_variable_defs`）または [mitsubachi-token](https://github.com/uzabase/mitsubachi-token) を参照。

## primitive

- [primitive-scale](./primitive-scale.md) の dimension-scale の値を参照する
- 9999px は border-radius でのみ使用する特殊値

## semantic

- primitive の値を用途に応じて semantic 名で参照する

## 使い分け

| 用途 | 例 |
|------|-----|
| 最小サイズ。正方形のため丸すぎる印象を避けたいコンポーネント | checkbox |
| 高さが小さいコンポーネント / コンポーネント内部の要素 | read-only-tag, toolchip, breadcrumb, segment-control |
| 基準サイズ。コンポーネントの small・medium にあたる部分 | search-box, text-area |
| コンポーネントの large・x-large にあたる部分 | カード類 |
| 最大サイズ。高さが大きめのコンポーネント | dialog, 投資実績カード |
| 丸い形状が一般的なアクション要素 | floating-button |
