# link-menu-item

link-menu-item は、クリックすると別ページへ遷移するメニューアイテムです。HTML の `<a>` タグで実装されるため、ブラウザ標準のリンク挙動（新しいタブで開く、右クリックメニューなど）を持ちます。

## いつ使うか

- メニュー内のアイテムで、クリック時にページ遷移（href による URL 移動）が必要なとき
- 新しいタブで開く、外部 URL へのリンクなど、リンクとしての挙動が求められるとき

## いつ使わないか

- アクションを実行するだけの場合 → [action-menu-item](./action-menu-item.md) を使います
- disabled 状態でリンクを無効化したい場合（`<a>` タグの disabled は標準では存在しないため、設計上の注意が必要です）

## Figma

- コンポーネント: https://www.figma.com/design/kHQNLM1dnk0EhZwOKBEBkL/Base-Component-Speeda-3.1-MITSUBACHI?node-id=8376-4985

> mockup で再現する場合は `mockup-kit/mitsubachi-mockup.css` の `.mi-menu-item`（`<a>` で実装） を使う（自作しない）。 組む前に見本 `mockup-kit/components/menu.html` を読んでマークアップ構造を踏襲する。

## バリアントプロパティ

| プロパティ | 値 | 説明 |
|-----------|-----|------|
| State | default / hover / active / focus | インタラクション状態 |
| New window | true / false | 外部リンクアイコンの表示有無 |

## コンテンツルール

- ラベルはリンク先の内容を端的に表す文言で記述します
- ラベルは1行に収まる長さとします
- 外部サイトへのリンクの場合は、外部リンクアイコンを表示することを検討します

## Do

- ページ遷移が目的のアイテムにはこのコンポーネントを使う
- 外部リンクには New window を true にして外部リンクアイコンを表示する

## Don't

- コマンドの実行に使わない → [action-menu-item](./action-menu-item.md) を使う
