# avatar

ユーザーを視覚的に識別するためのコンポーネントです。画像・イニシャル・アイコンによって「誰か」という情報を直感的に伝えます。

## いつ使うか

- ユーザーアカウントを特定・識別したい場面（ヘッダーメニュー、コメント欄、プロフィール画面など）
- 複数ユーザーをまとめて表示したい場面（グループやチームメンバーの一覧）。複数ユーザーの表示には [avatar-group](./avatar-group.md) を利用する

## いつ使わないか

- ユーザーと無関係な画像やアイコンを表示したい場合（他のコンポーネントや img 要素などで対応する）
- 複数ユーザーをスタック表示したい場合 → [avatar-group](./avatar-group.md)

## Figma

- コンポーネント: https://www.figma.com/design/kHQNLM1dnk0EhZwOKBEBkL/Base-Component-Speeda-3.1-MITSUBACHI?node-id=3769-1412
- 各variantの値は Figma MCP（`get_design_context`）で取得

> mockup で再現する場合は `mockup/mitsubachi-mockup.css` の `.mi-avatar` を使う（自作しない）。

## バリアントプロパティ

| プロパティ | 値 |
|---|---|
| variant | image / text / icon |
| size | small / medium / large / x-large / 2x-large |
| color | plum / violet / blue / viridian / green / brown / red（variant=text のみ） |
| inactive | true / false |

## variant の使い分け

| variant | 使いどころ |
|---------|-----------|
| **image** | ユーザーが設定した画像を表示する。画像がある場合は最優先で使用する |
| **text** | メールアドレスから生成した2文字のイニシャル（アルファベット大文字）を表示する。画像がない場合のデフォルト |
| **icon** | ユーザーを特定できない場合、またはエラー等で画像もテキストも表示できない場合に使用する |

## size の使い分け

| size | 主な使用箇所 |
|------|-----------|
| **small** | avatar-group（スタートアップ情報リサーチのNPコメントなど） |
| **medium** | ヘッダーメニューなど |
| **large** | アカウントメニューを開いた際のユーザー情報表示 |
| **x-large** | プロフィール画面（デスクトップ） |
| **2x-large** | プロフィール画面（モバイル） |

## inactive 状態

- ユーザーが利用停止・アカウント削除された際に、視覚的に休止・停止状態を表すプロパティ
- 操作不能を示す `disabled` とは目的が異なる

## コンテンツルール

- variant=text のイニシャルはメールアドレスの先頭から2文字のアルファベットを大文字で使用する
- 記号・数字は対象外とする
- 条件を満たすアルファベット2文字が取れない場合は、先頭の文字を最大2文字使用する
  - 例: `taro.yamada@uzabase.com` → **TA** / `9.@uzabase.com` → **9.**
- variant=image の場合、画像はアバターのサイズを最小サイズとして扱い、推奨サイズより小さい画像も上下中央配置で引き伸ばして表示する（余白は作らない）

## Do

- 画像がある場合は必ず image variant を使用する
- 名前やラベルと組み合わせる場合、アバターは左側に配置する
- color は variant=text の場合にシステムがランダムに割り振る

## Don't

- avatar-group 内ではなく単体で複数ユーザーを並べない → [avatar-group](./avatar-group.md) を使う
- ユーザーと無関係な画像表示に使わない
