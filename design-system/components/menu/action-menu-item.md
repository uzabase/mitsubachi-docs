# action-menu-item

action-menu-item は、クリックするとアクション（コマンド）を即座に実行するメニューアイテムです。選択後に値を保持しません（選択肢の記憶が不要な操作に使います）。

## いつ使うか

- コピー、削除、編集、移動、ダウンロードなど、クリックで即時実行されるコマンドを提供するとき
- 操作の結果として値が保持されない場合

## いつ使わないか

- 選択状態（チェックマーク）を表示・保持したい場合 → [select-menu-item](./select-menu-item.md) を使います
- ページ遷移が必要な場合 → [link-menu-item](./link-menu-item.md) を使います
- サブメニューを持たせたい場合 → [sub-menu-item](./sub-menu-item.md) を使います

## Figma

- コンポーネント: https://www.figma.com/design/kHQNLM1dnk0EhZwOKBEBkL/Base-Component-Speeda-3.1-MITSUBACHI?node-id=8376-4715

> mockup で再現する場合は `mockup-kit/mitsubachi-mockup.css` の `.mi-menu-item` を使う（自作しない）。削除など破壊的操作を赤文字で示す場合は `.mi-menu-item--danger`、スマートフォン向けには `.mi-menu-item--phone` を付ける。 組む前に見本 `mockup-kit/components/menu.html` を読んでマークアップ構造を踏襲する。

## バリアントプロパティ

| プロパティ | 値 | 説明 |
|-----------|-----|------|
| State | default / hover / active / focus / disabled | インタラクション状態 |
| Show icon | true / false | アイコンの有無 |

## コンテンツルール

- ラベルはアクションを端的に表す動詞または動詞句で記述します（例：「コピー」「削除する」）
- ラベルは1行に収まる長さとします
- disabled 状態では理由をツールチップなどで補足することを検討します

## Do

- ラベルはアクションの結果を予測できる動詞句にする
- [select-menu-item](./select-menu-item.md) との違いを意識し、選択状態が不要な操作に使う

## Don't

- 選択状態を保持する用途に使わない → [select-menu-item](./select-menu-item.md) を使う
- ページ遷移に使わない → [link-menu-item](./link-menu-item.md) を使う
