# banner

banner は、ユーザーに対して一定の情報量を持つ通知や補足説明を確実に届けるためのオーバーレイコンポーネントです。[snackbar](./snackbar.md) より情報密度が高く、ユーザーが内容を読み取るまで確実に表示され続けます。

## いつ使うか
- 画面全体に影響する重要な状態変化（システム障害・メンテナンス・権限の変更など）をユーザーに伝えるとき
- 状態の説明とともに、関連する操作への導線を提示したいとき
- ユーザーに必ず見せたい情報であり、自動で消えては困る通知のとき

## いつ使わないか
- 操作に対する短時間の結果フィードバック（「保存しました」など）には [snackbar](./snackbar.md) を使います
- ユーザーの明示的な確認・決断を要する重要なアクションには [action-dialog](./dialog/action-dialog.md) を使います
- フォームやコンテンツの文脈に紐づいた通知には [inline-notification](./inline-notification.md) を使います
- [snackbar](./snackbar.md): 一時的な操作フィードバックに特化し、数秒後に自動消去されます。banner より情報密度が低く、アクション提示を前提としません
- [inline-notification](./inline-notification.md): オーバーレイではなく UI の一部として埋め込まれます。フォームや特定のコンテンツ領域への文脈づけが強い通知に向いています
- [action-dialog](./dialog/action-dialog.md): ユーザーの操作フローを一時停止させ、明示的な確認を求めます。banner はユーザーの作業を止めずに情報を提示します
- [tooltip](./tooltip.md): ユーザーが意図して操作したときだけ表示される補足情報です。banner は能動的に通知します

## Figma
- コンポーネント: https://www.figma.com/design/kHQNLM1dnk0EhZwOKBEBkL/Base-Component-Speeda-3.1-MITSUBACHI?node-id=5607-6066
- 各variantの値は Figma MCP（`get_design_context`）で取得

> mockup で再現する場合は `mockup/mitsubachi-mockup.css` の `.mi-banner--*` を使う（自作しない）。スマートフォン向け（全幅）には `.mi-banner--phone` を付ける。

## バリアントプロパティ
| プロパティ | 値 |
|---|---|
| status | `information` / `success` / `warning` / `error` |

## variant の使い分け

| status | 使いどころ |
|---|---|
| `information` | 中立的な情報提供に使用します |
| `success` | 処理が正常に完了したことを示します |
| `warning` | 注意が必要な状況を示します |
| `error` | エラーが発生したことを示します |

## コンテンツルール
- タイトルはですます調の丁寧語で、状態を端的に伝える文章にします
- 説明テキストはですます調で、詳細な状況説明やユーザーがとるべきアクションを簡潔に記載します
- アクションリンクのラベルは、遷移先・操作内容が明確に伝わる表現にします
- 1つの banner に表示するメッセージは1件にします

## Do
- 画面全体に影響する重要な状態変化の通知に使う
- ユーザーが内容を読み取るまで表示し続ける必要がある通知に使う

## Don't
- 一瞬で消えるフィードバックに使わない（snackbar を使う）
- ユーザーの操作をブロックする必要がある場面で使わない（dialog を使う）
