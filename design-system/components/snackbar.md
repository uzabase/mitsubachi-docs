# snackbar

snackbar は、ユーザー操作に対する短いフィードバックを、既存 UI の上に重ねて表示する軽量なオーバーレイ通知コンポーネントです。[banner](./banner.md) よりも情報密度が低く、確実に見てもらうことを前提とせず、軽微な状態共有に特化します。

## いつ使うか
- ユーザーが行った操作の完了を短く伝えたいとき（「保存しました」「削除しました」など）
- 通知内容を確実に見てもらう必要がなく、操作フローを妨げたくないとき

## いつ使わないか
- エラーのような重要な情報や、ユーザーに確実に伝えなければならない通知には [banner](./banner.md) を使います
- ユーザーの明示的な確認・決断を要する重要なアクションには [action-dialog](./dialog/action-dialog.md) を使います
- フォームやコンテンツの文脈に紐づいた通知には [inline-notification](./inline-notification.md) を使います
- [banner](./banner.md): 自動消去されず、ユーザーが手動で閉じるまで表示が維持されます。information / success / warning / error の複数ステータスに対応し、より情報密度の高い通知に使います
- [inline-notification](./inline-notification.md): オーバーレイではなく UI の一部として埋め込まれます。フォームや特定のコンテンツ領域への文脈づけが強い通知に向いています
- [action-dialog](./dialog/action-dialog.md): ユーザーの操作フローを一時停止させ、明示的な確認を求めます。snackbar はユーザーの作業を止めずに情報を提示します

## Figma
- コンポーネント: https://www.figma.com/design/kHQNLM1dnk0EhZwOKBEBkL/Base-Component-Speeda-3.1-MITSUBACHI?node-id=5607-6067
- 各variantの値は Figma MCP（`get_design_context`）で取得

> mockup で再現する場合は `mockup/mitsubachi-mockup.css` の `.mi-snackbar`（画面隅スタックは `.mi-snackbar-viewport`）を使う（自作しない）。size は既定が medium、テキストが折り返さない短いメッセージには `.mi-snackbar--small` を付ける。

## バリアントプロパティ
| プロパティ | 値 |
|---|---|
| size | `small` / `medium` |

## variant の使い分け

| size | 使いどころ |
|---|---|
| `small` | テキストが折り返さない短いメッセージに使います。表示エリアが限られている場所で使用してください |
| `medium`（デフォルト） | 基本のサイズです |

## コンテンツルール
- メッセージテキストはですます調で、操作結果を端的に伝える簡潔な文章にします
- snackbar は操作の成功通知に特化しています。エラーや警告などの重要な情報を表示するためには使用しません
- 1 つの snackbar に表示するメッセージは 1 件にします

## Do
- 操作の完了を短く伝える通知に使う
- 簡潔なメッセージで操作結果を端的に伝える

## Don't
- エラーや警告など重要な情報の表示に使わない（banner を使う）
- ユーザーの操作をブロックする必要がある場面で使わない（dialog を使う）
- 長文の説明が必要な場合に使わない（inline-notification を使う）
