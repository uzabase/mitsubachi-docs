# mitsubachi-docs

mitsubachi-ui デザインシステムのドキュメント集。デザインルール・使い分け・Do/Don'tを集約した「**デザインシステムの素**」として、人間とAIの両方が参照することを想定しています。

## 何が入っているか

- `foundations/` — デザインの基盤（色・余白・タイポグラフィ・原則など）
- `components/` — 各UIコンポーネントの使い分けとDo/Don't
- `CLAUDE.md` — AIが使うときの入口

## 想定する読み手

- mitsubachi-uiを参照して実装するエンジニア
- mitsubachi-uiに沿ったモックを作るAIアシスタント（Claude / Cursor / ChatGPT など）、およびそれを使うPdM・営業・企画
- デザインシステムを設計・保守する人

## 関連リポジトリ

- [mitsubachi-ui](https://github.com/uzabase/mitsubachi-ui) — Web Components
- [mitsubachi-ui-react](https://github.com/uzabase/mitsubachi-ui-react) — React版（プライベート）
- [mitsubachi-token](https://github.com/uzabase/mitsubachi-token) — デザイントークン