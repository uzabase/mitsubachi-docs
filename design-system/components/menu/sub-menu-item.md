# sub-menu-item

sub-menu-item は、サブメニューを持つメニューアイテムです。右端に「>」（シェブロン）アイコンを表示することで、この項目にサブメニューがあることをユーザーに示します。

## いつ使うか

- アクションの選択肢が多く、カテゴリに分けて階層表示したいとき
- 階層は最大2階層まで（menu → sub-menu）使えます

## いつ使わないか

- 2階層を超える深い階層が必要な場合（ユーザーにとって複雑になりすぎるため、別の設計を検討します）
- サブメニューを持たない単純なアクションの場合 → [action-menu-item](./action-menu-item.md) を使います

## Figma

- コンポーネント: https://www.figma.com/design/kHQNLM1dnk0EhZwOKBEBkL/Base-Component-Speeda-3.1-MITSUBACHI?node-id=8376-4959

> mockup で再現する場合は `mockup-kit/mitsubachi-mockup.css` の `.mi-menu-item--sub` を使う（自作しない）。 組む前に見本 `mockup-kit/components/menu.html` を読んでマークアップ構造を踏襲する。

## バリアントプロパティ

| プロパティ | 値 | 説明 |
|-----------|-----|------|
| State | default / hover / active / focus / disabled | インタラクション状態 |
| Show icon | true / false | アイコンの有無 |

## コンテンツルール

- 右端に「>」アイコンを必ず表示します
- ラベルはサブメニューのカテゴリを端的に表す名詞または名詞句で記述します
- ラベルは1行に収まる長さとします

## Do

- 選択肢が多い場合にカテゴリごとに階層化して整理する
- 階層は最大2階層までに留める

## Don't

- 2階層を超える深い階層にしない（ユーザーにとって複雑になりすぎる）
- サブメニューを持たない単純なアクションには使わない → [action-menu-item](./action-menu-item.md) を使う
