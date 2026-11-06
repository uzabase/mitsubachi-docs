# select-menu-item

select-menu-item は、選択状態を持つメニューアイテムです。設定値やフィルター条件などを切り替えるために使い、一覧の中で「現在どれが選択されているか」を伝えます。content-type に **text（単一選択。選択中の項目の右にチェックマーク）** と **checkbox（複数選択。各項目の左にチェックボックス）** があります。

## いつ使うか

- 言語切り替えや表示件数のように、選択肢の中から 1 つを選び、選択中の項目にチェックマークを表示したいとき → content-type=text
- フィルター条件のように、複数の項目を同時にオン/オフしたいとき → content-type=checkbox
- アクションの結果としてシステム状態が変わるが、トリガーのラベルは固定のとき

## いつ使わないか

- 選択した値をトリガーに表示・保持したい場合 → [select-box](../select-box/select-box.md) を使います
- 選択状態の表示が不要なアクション → [action-menu-item](./action-menu-item.md) を使います
- 複数選択が同時に成り立たない選択肢（並び順・表示件数など、どれか 1 つしか選べないもの）に checkbox は使いません → text を使います

## Figma

- コンポーネント: https://www.figma.com/design/kHQNLM1dnk0EhZwOKBEBkL/Base-Component-Speeda-3.1-MITSUBACHI?node-id=8376-4776

> mockup で再現する場合は `mockup-kit/mitsubachi-mockup.css` の `.mi-menu-item` を使う（自作しない）。単一選択（text）で選択中は `--selected` を付けて右に check-small を置く。複数選択（checkbox）は `--checkbox` を付け、中に `.mi-checkbox-label` ＋ `.mi-checkbox` を置いて、選択中は checkbox を checked にする（`--selected` と右の check は付けない）。 組む前に見本 `mockup-kit/components/menu.html` を読んでマークアップ構造を踏襲する。単一選択は新しい項目を選ぶと前の選択は自動解除され menu が閉じる。複数選択は項目を選んでも閉じず、menu の外側をクリックして閉じる。任意選択の場合は未選択を表す「指定なし」という選択肢を用意する。

## バリアントプロパティ

| プロパティ | 値 | 説明 |
|-----------|-----|------|
| viewport | desktop / phone | 表示環境 |
| content-type | text / checkbox / slot | 項目の中身。text=単一選択（選択中は右にチェックマーク）、checkbox=複数選択（左にチェックボックス）、slot=任意の要素を差し込む |
| selected | false / true | 選択状態。text はチェックマーク、checkbox はチェック入りになり、どちらも面色が選択色になる |
| state | default / hover / active / focus / disabled | インタラクション状態 |
| show-icon | true / false | 先頭アイコンの有無（text のとき） |
| show-support-text | true / false | ラベルの下の補助文の有無 |

## content-type の使い分け

| content-type | 使いどころ |
|---|---|
| **text** | 選択肢の中から 1 つを選ぶ（単一選択）。新しい項目を選ぶと前の選択は自動的に解除され、menu は閉じる |
| **checkbox** | 複数の項目を同時にオン/オフする（複数選択）。項目を選んでも menu は閉じず、menu の外側をクリックして閉じる |
| **slot** | 任意の要素を差し込む。kit に単体クラスは無い |

## 振る舞い

- **単一選択（text）**: 選択肢（menu-item-group）の中からどれか 1 つを選択する。未選択も 1 つの選択肢。新しい項目を選択すると、これまでの選択は自動的に解除される
- **複数選択（checkbox）**: 複数の項目を選択できる。閉じるときは menu 以外をクリックする
- **選択必須と任意選択**: 必ず選択する必要がある場合と、任意の場合のどちらもある。任意選択の場合は、未選択状態を表す「指定なし」という選択肢を用意する

## コンテンツルール

- ラベルは選択対象を端的に表す名詞または名詞句で記述します
- ラベルは原則 1 行に収めます。長い場合は省略せず折り返します
- 1 つの menu の中で text と checkbox を混ぜません（どこまでが複数選択でどこからが単一選択か読めなくなる）

## Do

- 選択肢の性質で content-type を選ぶ。1 つだけ選ぶなら text、複数を同時に選ぶなら checkbox
- 任意選択には「指定なし」の選択肢を用意する
- 複数選択の確定は menu の外側クリックで閉じることで行う（確定ボタンなどは置かない）

## Don't

- text の項目を複数選択に使わない（単一選択か複数選択かユーザーが判断できず、複数選んだ場合の確定方法も曖昧になる）→ 複数選択は checkbox を使う
- 複数選択が同時に成り立たない選択肢に checkbox を使わない → text を使う
- 1 つの menu の中で text と checkbox を混ぜない
- 選択状態の表示が不要なアクションに使わない → [action-menu-item](./action-menu-item.md) を使う
- 選択した値をトリガーに表示・保持したい場合には使わない → [select-box](../select-box/select-box.md) を使う
