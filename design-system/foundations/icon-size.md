# icon-size

アイコンのサイズに使用するトークン。

> 具体的な値は Figma MCP（`get_variable_defs`）または [mitsubachi-token](https://github.com/uzabase/mitsubachi-token) を参照。

## スケール（Figma の変数コレクション「✅ icon-size」。2026-07-29 に実物を確認）

| Figma の変数名 | 値 | mockup kit |
|---|---|---|
| `icon-size-2x-small` | 14 | `--icon-size-2x-small` |
| `icon-size-xs-mall` ※ | 16 | `--icon-size-xs-mall` |
| `icon-size-small` | **18** | `--icon-size-small` |
| `icon-size-medium` | **20** | `--icon-size-medium` |
| `icon-size-large` | **22** | `--icon-size-large` |
| `icon-size-x-large` | 24 | `--icon-size-x-large` |
| `icon-size-2x-large` | 26 | `--icon-size-2x-large` |
| `icon-size-3x-large` | 28 | `--icon-size-3x-large` |
| `icon-size-4x-large` | **32** | `--icon-size-4x-large` |
| `icon-size-5x-large` | 36 | `--icon-size-5x-large` |
| `icon-size-6x-large` | 42 | `--icon-size-6x-large` |
| `icon-size-7x-large` | **46** | `--icon-size-7x-large` |
| `icon-size-8x-large` | 52 | `--icon-size-8x-large` |
| `icon-size-9x-large` | 58 | `--icon-size-9x-large` |
| `icon-size-10x-large` | 66 | `--icon-size-10x-large` |

> ※ `icon-size-xs-mall` は Figma 側の typo（`x-small` のはず）。kit は名前をそのまま写している。

> ### Figma MCP から値を取るときの注意（2026-07-29 に検証）
> **`get_variable_defs` が返す「名前」は `icon-size-*` ではない。値だけが正しい。**
>
> | MCP の出力 | 実際に参照している変数 |
> |---|---|
> | `"18px": "14"` | `icon-size-2x-small`（14） |
> | `"24px": "18"` | `icon-size-small`（18） |
> | `"27px": "20"` | `icon-size-medium`（20） |
> | `"30px": "22"` | `icon-size-large`（22） |
>
> **Figma 側では正しく `icon-size-*` を参照している**（アイコンのレイヤーの W/H に `icon-size-small` が
> 割り当てられていることを Figma 上で確認済み）。にもかかわらず MCP は別の名前を返す。
> 名前の数字は値の約 4/3 倍で、`27` `30` は icon-size コレクションに存在しない数字。**原因は未解明。**
>
> → **実装するときは MCP の「名前」を信用せず、「値」を使うこと。**
> それが上の icon-size スケールのどの段階かは、値で照合すれば分かる。

## ルール

- アイコンはフォントサイズと対になる
- アイコン単体で使用する場合（例: icon-button）はコンポーネントで設定されているサイズを使用する
- コンポーネントのアイコンサイズを決める際は、同じコンポーネントで使用しているフォントサイズと合わせることを心がける
