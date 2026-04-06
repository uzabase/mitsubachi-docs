# アイコン

UI 上の操作や状態を視覚的に伝える小さなシンボル。

---

## 仕様

- すべて 24×24 の SVG で統一
- アイコンのサイズはテキストサイズに連動させる

### コード例（webcomponent）

```html
<!-- 単体 -->
<mi-icon type="search"></mi-icon>
<mi-icon type="chevron-right"></mi-icon>

<!-- サイズ変更は親の font-size で -->
<span style="font-size: 32px;">
  <mi-icon type="bell"></mi-icon>
</span>

<!-- ボタンにアイコンを付ける場合は icon-type 属性 -->
<mi-neutral-button variant="primary" icon-type="plus">新規作成</mi-neutral-button>
<mi-icon-button icon-type="search" aria-label="検索"></mi-icon-button>
```

### コード例（html）

```html
<!-- アイコンは SVG またはテキスト/絵文字で代替する -->
<!-- 実際のプロジェクトでは SVG スプライトやアイコンフォントを使う -->
<span role="img" aria-hidden="true" style="
  display: inline-flex; align-items: center; justify-content: center;
  width: 24px; height: 24px; font-size: 16px;
">🔍</span>

<!-- ボタンにアイコンを付ける -->
<button style="
  display: inline-flex; align-items: center; gap: 4px;
  min-height: 32px; padding: 2px 12px;
  background: #282828; color: #fff; border: none; border-radius: 9999px;
  font-size: 12px; font-weight: 700; cursor: pointer;
">＋ 新規作成</button>
```

---

## アイコン一覧

### ナビゲーション・方向

| 名前 | 用途 |
|------|------|
| `arrow-down` | 下方向への移動 |
| `arrow-down-small` | 小さい下矢印 |
| `arrow-left` | 戻る、左方向への移動 |
| `arrow-up-down` | 並び替え |
| `arrow-up-small` | 小さい上矢印 |
| `chevron-down` | 開閉（アコーディオン、ドロップダウン） |
| `chevron-down-fill` | 塗りつぶしの下シェブロン |
| `chevron-down-small` | 小さい下シェブロン |
| `chevron-left` | 前のページ、パンくず |
| `chevron-left-small` | 小さい左シェブロン |
| `chevron-right` | 次のページ、詳細へ |
| `chevron-right-fill` | 塗りつぶしの右シェブロン |
| `chevron-right-small` | 小さい右シェブロン |
| `chevron-up` | 閉じる、上方向 |
| `chevron-up-small` | 小さい上シェブロン |
| `double-chevron-right` | 末尾へ移動（ページネーション） |
| `home` | ホーム画面 |
| `home-fill` | ホーム（塗りつぶし・選択中） |
| `route` | 経路、ルート |

### アクション

| 名前 | 用途 |
|------|------|
| `check` | 確認、完了 |
| `check-small` | 小さいチェック |
| `copy` | コピー |
| `cross` | 閉じる、キャンセル |
| `cross-small` | 小さい閉じる |
| `download` | ダウンロード |
| `drag` | ドラッグハンドル |
| `exit` | ログアウト、退出 |
| `maximize` | 最大化 |
| `minimize` | 最小化 |
| `open-in-new` | 別タブで開く |
| `pencil-square` | 編集 |
| `plus` | 追加 |
| `plus-small` | 小さい追加 |
| `plus-circle` | 丸囲みの追加 |
| `plus-circle-fill` | 丸囲みの追加（塗りつぶし） |
| `minus` | 削除、減らす |
| `minus-circle` | 丸囲みの削除 |
| `minus-circle-fill` | 丸囲みの削除（塗りつぶし） |
| `search` | 検索 |
| `search-fill` | 検索（塗りつぶし） |
| `share` | 共有 |
| `chain` | リンク、URL |
| `stop-fill` | 停止 |

### ステータス・フィードバック

| 名前 | 用途 |
|------|------|
| `success` | 成功（丸にチェック） |
| `success-fill` | 成功（塗りつぶし） |
| `error-fill` | エラー（八角形にバツ） |
| `information` | 情報（丸に i） |
| `information-fill` | 情報（塗りつぶし） |
| `warning-fill` | 警告（三角に !） |

### オブジェクト・コンテンツ

| 名前 | 用途 |
|------|------|
| `app` | アプリ一覧（グリッドドット） |
| `bell` | 通知 |
| `bell-fill` | 通知（塗りつぶし・未読あり等） |
| `book-ai` | AI 関連の資料 |
| `bookmark` | ブックマーク |
| `bookmark-fill` | ブックマーク済み |
| `building` | 企業、組織 |
| `building-add` | 企業を追加 |
| `building-cancel-fill` | 企業を除外 |
| `calendar` | カレンダー、日付 |
| `calendar-event` | イベント付きカレンダー |
| `calendar-fill` | カレンダー（塗りつぶし） |
| `clock` | 時刻、タイマー |
| `gear` | 設定 |
| `headset` | サポート、問い合わせ |
| `headset-face` | サポート（顔付き） |
| `history` | 履歴 |
| `kebab-menu` | その他メニュー（縦三点） |
| `language` | 言語切り替え（地球） |
| `lock` | ロック |
| `lock-fill` | ロック（塗りつぶし） |
| `unlock` | ロック解除 |
| `unlock-fill` | ロック解除（塗りつぶし） |
| `magic` | AI・自動生成（✨） |
| `magic-fill` | AI・自動生成（塗りつぶし） |
| `mail` | メール |
| `mail-gear` | メール設定 |
| `menu` | ハンバーガーメニュー（横三本線） |
| `money` | 金額、料金 |
| `person` | ユーザー |
| `person-add` | ユーザー追加 |
| `person-cancel-fill` | ユーザー除外 |
| `person-fill` | ユーザー（塗りつぶし） |
| `person-gear` | ユーザー設定 |
| `report` | レポート、ドキュメント |

### 表示・レイアウト

| 名前 | 用途 |
|------|------|
| `eye` | 表示中 |
| `eye-slash` | 非表示 |
| `list-close` | リストを閉じる（サイドバー等） |
| `list-open` | リストを開く |
| `side-left` | 左パネル表示 |
| `side-right` | 右パネル表示 |

### フォロー・エンゲージメント

| 名前 | 用途 |
|------|------|
| `follow` | フォロー（☆） |
| `follow-fill` | フォロー済み（★） |
| `follow-list` | フォローリスト |
| `follow-list-fill` | フォローリスト（塗りつぶし） |

---

## `-fill` バリアントについて

多くのアイコンに線画版と塗りつぶし版（`-fill`）がある。

- **線画（デフォルト）** — 通常の状態で使う
- **塗りつぶし（`-fill`）** — 選択中・アクティブな状態を示す（例: `bookmark` → 未保存、`bookmark-fill` → 保存済み）

ステータスアイコン（`error-fill`、`warning-fill`）は塗りつぶし版のみ。

---

## Do / Don't

### ✅ Do

- **アイコン単体のボタンにはラベルを付ける** — スクリーンリーダー用のラベルは必須。ツールチップとしても機能する
- **テキストと併用する** — アイコンだけでは意味が伝わらない場合、必ずラベルやテキストを添える
- **`-fill` で状態を表現する** — オン/オフの切り替え（ブックマーク、フォロー等）には線画と塗りつぶしを使い分ける
- **一覧にあるアイコンだけを使う** — 存在しないアイコン名を指定すると何も表示されない

### ❌ Don't

- **色だけでステータスを伝えない** — `error-fill` を赤くするだけでなく、テキストでも「エラー」と伝える
- **一覧にないアイコンを使わない** — 近い意味のものを仮で使い、`<!-- TODO: アイコン要確認 -->` と注記する
- **ボタン内にアイコンを直接ネストしない** — ボタンコンポーネントが提供するアイコン指定の仕組みを使う

