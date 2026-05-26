# danger-button

削除・無効化・リセットなど、取り消しが困難または影響範囲の大きい破壊的操作に使用するボタンコンポーネントです。

## いつ使うか

- データの削除（ファイル・レコード・アカウントなど）
- 設定のリセット・初期化
- 機能の無効化・停止など、影響範囲の大きい操作
- 確認ダイアログ内での実行ボタン（「削除する」「リセットする」など）

## いつ使わないか

- 通常の実行・保存・送信など破壊的ではない操作 → [neutral-button](./neutral-button.md)
- AI実行に特化した操作 → [ai-button](./ai-button.md)
- キャンセル・戻るなど、操作を中断するアクション → [neutral-button](./neutral-button.md) の ghost や plane を使用

## Figma

- コンポーネント: https://uzabase.github.io/mitsubachi-ui/?path=/story/button-mi-danger-button--basic
- 各variantの値は Figma MCP（`get_design_context`）で取得

## バリアントプロパティ

| プロパティ | 値 | 説明 |
|-----------|-----|------|
| variant | primary / secondary / ghost | 重要度・強調度 |
| size | medium / large / x-large | サイズ |
| state | default / hover / active / focus / loading / disabled | インタラクション状態 |

## variant の使い分け

| variant | 使いどころ |
|---------|-----------|
| **primary** | 最も強調度の高いスタイル。破壊的操作を実行する主要なボタンに使用 |
| **secondary** | 補助的な破壊的操作に使用 |
| **ghost** | 視覚的に控えめなスタイル。一覧内の各行に配置する削除ボタンなど、繰り返し配置する場面で使用 |

## コンテンツルール

- テキストラベルは必須。破壊的操作の内容を端的に表す動詞句で記述する（例：「削除する」「リセットする」「無効にする」）
- アイコンはオプション。テキストラベルと組み合わせて使用する。アイコンのみの構成にはできない（→ [icon-button](./icon-button.md)）
- 誤操作を防ぐため、確認ダイアログ（dialog コンポーネント）と併用する

## Do

- 破壊的操作には必ず danger-button を使う
- 実行前に確認ダイアログを挟む
- ラベルは「削除する」「リセットする」など結果が明確に予測できる動詞句にする

## Don't

- 確認なしで破壊的操作を実行しない — 削除などの操作はダイアログ等で確認ステップを挟んでから実行する
- 通常の操作に danger-button を使わない — 破壊的操作以外には [neutral-button](./neutral-button.md) を使う
- ラベルを曖昧にしない —「OK」「実行」ではなく「削除する」「リセットする」など具体的な結果を示す
