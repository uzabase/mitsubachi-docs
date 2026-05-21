# elevation

影（box-shadow）に使用するトークン。要素の浮き具合を表現する。

> 具体的な値は Figma MCP（`get_variable_defs`）または [mitsubachi-token](https://github.com/uzabase/mitsubachi-token) を参照。

## 使い分け

| トークン | 使い分け | コンポーネント例 |
|---------|---------|----------------|
| **elevation-30** | 操作で出現・消える要素 | menu, suggestion, tooltip, snackbar, banner, drawer |
| **brand-elevation** | 常時表示し浮いている要素 | floating-button |
| **elevation-50** | overlay とセットで使う要素 | dialog, side navigation |
