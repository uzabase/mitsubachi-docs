# アイコン

情報を視覚的に伝えるためのシンボル。ボタンやラベルと組み合わせて使用する。

## Figma
- https://www.figma.com/design/0TyVfKpH9I54YV21lcOLeQ/Iconography?node-id=0-1&t=QkVMCef1Qcm5klSE-1

## SVG の取得元
- [icons.ts](https://github.com/uzabase/mitsubachi-ui/blob/main/src/components/icon/icons.ts) - 各アイコンの SVG パスデータ

## 利用可能なアイコン

### 方向・ナビゲーション
`arrow-down`, `arrow-left`, `arrow-right`, `arrow-up`,
`chevron-down`, `chevron-left`, `chevron-right`, `chevron-up`,
`double-chevron-left`, `double-chevron-right`

### アクション
`check`, `cross`, `plus`, `minus`, `plus-circle`, `minus-circle`,
`copy`, `download`, `share`, `exit`, `open-in-new`,
`pencil-square`, `trash`, `drag`

### オブジェクト
`bell`, `bell-fill`, `bookmark`, `bookmark-fill`,
`building`, `calendar`, `clock`, `history`,
`document`, `folder`, `mail`, `money`,
`gear`, `lock`, `unlock`, `key`

### ユーザー
`person`, `person-add`, `person-fill`, `person-gear`

### ステータス・フィードバック
`success`, `error-fill`, `warning-fill`, `information`,
`question-circle`

### 表示・非表示
`eye`, `eye-slash`

### その他
`search`, `menu`, `kebab-menu`, `home`, `magic`, `language`, `route`

> 最新の一覧は [icons.ts](https://github.com/uzabase/mitsubachi-ui/blob/main/src/components/icon/icons.ts) を参照

## サイズ

アイコンのサイズは CSS で指定する。トークンの値は `foundations/icon-size.md` を参照。

| サイズ名 | アイコンサイズ | 用途 |
|---------|--------------|------|
| 2x-small | 14px | インラインアイコン |
| x-small | 16px | 小さいボタン内 |
| small | 18px | テキスト横の補助 |
| medium | 20px | 標準的なUI（ボタン内など） |
| large | 22px | 強調したいアイコン |
| x-large | 24px | ナビゲーション |

## 使い分け

### 単独で使う場合
- 意味が明確なアイコンのみ（例: `search`, `menu`, `cross`）
- 必ず `aria-label` を付ける

### テキストと併用する場合
- アイコンはテキストの補助として使用
- アイコンとテキストの間隔は 4px

### ボタン内で使う場合
- アイコンのみのボタン: `aria-label` 必須
- テキスト付きボタン: アイコンは左側に配置（慣例）

## アクセシビリティ

- アイコンのみで意味を伝える場合は `aria-label` を必ず付ける
- 装飾目的のアイコンには `aria-hidden="true"` を付ける
- 色だけで状態を伝えない（テキストやアイコン形状と併用）

## Do / Don't

### Do
- ラベルと一緒に使い、意味を明確にする
- 一貫したアイコンを使う（同じ操作には同じアイコン）
- 対応するサイズトークンを使う

### Don't
- 意味が曖昧なアイコンを単独で使う
- 独自のアイコンを追加する（一覧にないものは使わない）
- アイコンだけで重要な情報を伝える
- **存在しないアイコンを推測で使わない** — 一覧にないものは使わず、近い意味のものを仮で使い、要確認であることを注記する
