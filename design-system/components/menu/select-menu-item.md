# select-menu-item

select-menu-item は、選択状態（チェックマーク）を持つメニューアイテムです。一覧の中から「現在どれが選択されているか」を視覚的に伝えます。

## いつ使うか

- 言語切り替えのように、選択中の項目にチェックマークを表示したいとき
- フィルタ設定や表示切り替えなど、現在の状態を一覧内で示したいとき
- アクションの結果としてシステム状態が変わるが、トリガーのラベルは固定のとき

## いつ使わないか

- 選択した値をトリガーに表示・保持したい場合 → Select を使います
- 選択状態の表示が不要なアクション → [action-menu-item](./action-menu-item.md) を使います

## Figma

- コンポーネント: https://www.figma.com/design/kHQNLM1dnk0EhZwOKBEBkL/Base-Component-Speeda-3.1-MITSUBACHI?node-id=8376-4776

> mockup で再現する場合は `mockup-kit/mitsubachi-mockup.css` の `.mi-menu-item`（選択中は `--selected`） を使う（自作しない）。

## バリアントプロパティ

| プロパティ | 値 | 説明 |
|-----------|-----|------|
| Selected | false / true | 選択状態。true のときチェックマークを表示 |
| State | default / hover / active / focus / disabled | インタラクション状態 |
| Show icon | true / false | アイコンの有無 |

## コンテンツルール

- ラベルは選択対象を端的に表す名詞または名詞句で記述します
- ラベルは1行に収まる長さとします

## Do

- 現在の選択状態をチェックマークで示す用途に使う
- ラジオボタン型のメニュー（単一選択）として使う

## Don't

- 選択状態の表示が不要なアクションに使わない → [action-menu-item](./action-menu-item.md) を使う
- 選択した値をトリガーに表示・保持したい場合には使わない → Select を使う
