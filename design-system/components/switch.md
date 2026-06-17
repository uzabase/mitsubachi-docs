# switch

Switchは、設定や機能のオン/オフを即時に切り替えるためのコンポーネントです。操作した瞬間に変更が反映されるため、送信ボタンなどの追加アクションは不要です。

## いつ使うか
- 操作した瞬間に即時反映される設定の切り替え（例：通知のオン/オフ、ダークモードの切り替え）
- システムやアプリの状態をリアルタイムで変更する場面
- 単一の機能に対してオン/オフを切り替える場面

## いつ使わないか
- 送信ボタンで確定するフォーム内での選択には、[checkbox](./checkbox/index.md) を使用します
- 複数の選択肢から選ぶ場面には、[checkbox](./checkbox/index.md) を使用します
- ユーザーの同意や選択（利用規約への同意など）には、[checkbox](./checkbox/index.md) を使用します
- SwitchとCheckboxはいずれも二値の状態を扱いますが、用途と反映タイミングが異なります

| | Switch | Checkbox |
|---|---|---|
| 反映タイミング | 操作した瞬間に即時反映 | フォーム送信など別アクションで確定 |
| 用途 | オン/オフの状態切り替え | 選択・同意 |
| 複数選択 | 単体のオン/オフに特化 | 複数選択に対応 |

## Figma
- コンポーネント: https://www.figma.com/design/kHQNLM1dnk0EhZwOKBEBkL/Base-Component-Speeda-3.1-MITSUBACHI?node-id=9925-5880
- 各variantの値は Figma MCP（`get_design_context`）で取得

> mockup で再現する場合は `mockup/mitsubachi-mockup.css` の `.mi-switch`（phone は `--phone`） を使う（自作しない）。

## バリアントプロパティ
| プロパティ | 値 |
|---|---|
| viewport | `desktop` / `phone` |
| selected | `true` / `false` |
| state | `default` / `hover` / `active` / `focus` / `disabled` |

## variant の使い分け

### viewport
- `desktop`: デスクトップブラウザ向けのサイズ
- `phone`: スマートフォン向けのサイズ（より大きいサイズ）

### selected（選択状態）
- `true`（オン）: スイッチがオンの状態。トラックがブルー系の色で塗られ、ノブ（白い丸）がチェックマークアイコンとともに右側に移動します
- `false`（オフ）: スイッチがオフの状態。トラックがグレーで塗られ、ノブが左側に位置します

## コンテンツルール
- Switchにはラベルを付けます。ラベルはSwitchの**左側**に配置します。右側にラベルを置くのは非推奨です（右側にラベルを置く場合はCheckboxが適切なケースが多いため）
- switch-textのような、ラベルとSwitchをひとまとめにしたコンポーネントは提供していません。ラベルとSwitchの組み合わせは、各画面のレイアウト実装側で構成します
- ラベルのテキストは、Switchが何を制御するかを端的に表すものとします

## Do
- 即時反映される設定の切り替えに使う
- ラベルをSwitchの左側に配置する

## Don't
- フォーム送信で確定する選択に使わない（checkbox を使う）
- ラベルをSwitchの右側に配置しない
- 複数選択の用途に使わない（checkbox を使う）
