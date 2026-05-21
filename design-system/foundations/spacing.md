# spacing

コンポーネントやレイアウトの余白に使用するトークン。

> 具体的な値は Figma MCP（`get_variable_defs`）または [mitsubachi-token](https://github.com/uzabase/mitsubachi-token) を参照。

## ルール

- spacing は [primitive-scale](./primitive-scale.md) の dimension-scale を参照する
- ミツバチで定義された値のみを spacing として使用する
- 定義外の値（マジックナンバー）は使用しない
