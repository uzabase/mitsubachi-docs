# inline-notification

inline-notification は、ユーザーの操作に対して即座に理解すべきエラーや、時間的制約のある情報を画面の文脈の中で提示するためのコンポーネントです。オーバーレイではなく、UI の一部として自然に組み込まれる形で表示されます。

## いつ使うか
- フォームの送信結果（エラー・成功）をフォームの近くに表示したいとき
- ユーザーが行った操作に対して、即座に状態を伝える必要があるとき
- 画面を離れずに確認できる補足情報や注意事項を提示したいとき

## いつ使わないか
- ユーザーの判断や確認を必要とする重要な通知には [dialog](./dialog/index.md) を使用します
- 画面全体への影響を伴う警告（システム障害など）には、より目立つ通知パターンを検討します
- 一時的なアクション確認（「保存しました」など短命な通知）には [snackbar](./snackbar.md) を検討します
- inline-notification はページ内に固定表示されるため、ユーザーが操作を続けながらメッセージを参照できます
- [snackbar](./snackbar.md) はページ上に一時的に浮かび上がり、数秒後に自動消滅します
- [dialog](./dialog/index.md) はユーザーの操作フローを一時停止させ、明示的な確認を求めます。情報の緊急度・永続性・ユーザーへの介入度に応じて使い分けます

## Figma
- コンポーネント: https://www.figma.com/design/kHQNLM1dnk0EhZwOKBEBkL/Base-Component-Speeda-3.1-MITSUBACHI?node-id=5638-4139
- 各variantの値は Figma MCP（`get_design_context`）で取得

> mockup で再現する場合は `mockup/mitsubachi-mockup.css` の `.mi-inline-notification--error/--information/--success/--warning` を使う（自作しない）。グレー面で控えめに見せる secondary には `.mi-inline-notification--secondary`、スマートフォン向けには `.mi-inline-notification--phone` を付ける。

## バリアントプロパティ
| プロパティ | 値 |
|---|---|
| variant | `primary` / `secondary` |
| status | `information` / `success` / `warning` / `error` |
| viewport | `desktop` / `phone` |

## variant の使い分け

### variant（表示スタイル）
- `primary` はステータスに対応した背景色で強調表示します。ユーザーが即座に気づく必要のある情報（エラーや成功など）に使用します
- `secondary` はグレーの背景で控えめに表示します。補足情報や優先度の低い注意喚起に使用します。secondary は `information` と `warning` の2種類のステータスのみ対応しています

### status（通知の種類）
| status | 使いどころ |
|---|---|
| `information` | 情報提供。中立的なメッセージに使用します |
| `success` | 処理が正常に完了したことを示します（primary のみ） |
| `warning` | 注意が必要な状況を示します |
| `error` | エラーが発生したことを示します（primary のみ） |

## コンテンツルール
- テキストは簡潔にまとめます。長文の説明が必要な場合は、リンクや別のコンテンツへの誘導を検討します
- 1行目は、状態を伝える文章をですます調の丁寧語で記載。2行目は、詳細な説明や、ユーザーがとるべきアクションを文章で簡潔に、ですます調の丁寧語で記載
- 1コンポーネントに表示するメッセージは1件にします
- secondary の `information` と `warning` では、テキストが弱い色（weak）で表示されます

## Do
- フォームの送信結果をフォームの近くに表示する
- 操作結果の状態を即座に伝える

## Don't
- ユーザーの操作をブロックする必要がある場面で使わない（dialog を使う）
- 一時的な操作フィードバックに使わない（snackbar を使う）
