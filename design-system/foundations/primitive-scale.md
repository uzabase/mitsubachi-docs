# primitive-scale

デザインシステムの基礎となるスケール値。dimension-scale と font-scale の2種類で構成される。

> 具体的な値は Figma MCP（`get_variable_defs`）または [mitsubachi-token](https://github.com/uzabase/mitsubachi-token) を参照。

## なぜ primitive-scale を定めるか

デザイナーが新しい要素を作るたびに「何pxが適切か」をゼロから検討するコストを削減し、システムで定義された共通の選択肢から選べるようにする。個人の感覚による微細な数値のバラつき（マジックナンバー）を排除し、プロダクト全体で視覚的な一貫性と開発スピードを両立させる。

## dimension-scale

- 8px をベースに、小さい方は細かく、大きい方は粗く刻む
- 小さいサイズ: 4px と 8px の差は2倍。ボタンの余白や角丸では見た目の印象を大きく変える
- 大きいサイズ: 80px と 84px の差はわずか 5%。選択肢が多いとかえって迷いを生む
- [spacing](./spacing.md)、[border-radius](./border-radius.md) で使用される

## font-scale

- 14px を基準とした Major Second Type Scale で値を算出している
- 表にない大きな値を使いたい場合は、同じ Major Second Type Scale に則り値を採択することを許可する
- [typography](./typography.md) で使用される
