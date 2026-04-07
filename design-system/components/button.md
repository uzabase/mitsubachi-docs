# ボタン

ユーザーのアクションをトリガーするコンポーネント。

## Figma
- URL: https://www.figma.com/design/kHQNLM1dnk0EhZwOKBEBkL/Base-Component-Speeda-3.1-MITSUBACHI?node-id=3-324&t=2Rf6tpLoFdLSpkiv-1
- バリアント・サイズ・色・寸法の詳細は Figma を参照

## Do / Don't

### ✅ Do
- primary は 1 画面に 1 つ
- danger の前に確認ダイアログを挟む
- アイコンボタンには aria-label を付ける
- 選択状態は secondary / tertiary / ghost で使う
- ラベルは短い動詞にする

### ❌ Don't
- primary / plane を選択状態にしない
- Danger / AI ボタンを選択状態にしない
- AI ボタンにアイコンを指定しない（✨は自動表示）
- メニューボタンを値の選択に使わない
- danger を確認なしで実行しない
- ラベルを長文にしない

## 並べ方
- primary を右、secondary を左
- ボタン間隔は 8px