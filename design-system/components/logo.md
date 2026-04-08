# ロゴ

Speeda および関連ブランドのロゴを表示するコンポーネント。

## Figma
- コンポーネント: https://www.figma.com/design/3abXEj4vbUt5UUf37Ld2Cn/Logo?node-id=0-1
- Do / Don't は Figma ページ内の「仕様」フレームを参照

## コンポーネント一覧

| コンポーネント | 役割 | いつ使うか |
|---------------|------|-----------|
| **sp-logo** | Speeda ロゴ（テキスト＋シンボル） | ヘッダー、フッター、ログイン画面など |
| **sp-symbol** | Speeda シンボルマークのみ | ファビコン、アイコン的な用途、省スペースな場所 |
| **ub-logo** | Uzabase ロゴ | フッターなど親会社ブランドを表示する場合 |

## 使い分け

### よくあるパターン

| シーン | 指定 |
|--------|------|
| Speeda のヘッダー | `sp-logo`（symbol=true, sub-brand=null） |
| Speeda AI Agent のヘッダー | `sp-logo`（symbol=true, sub-brand=ai-agent） |
| 暗い背景（ダークモード等） | 上記に `inverse=true` を追加 |
| ファビコン・最小表示 | `sp-symbol` |
| フッターに親会社ロゴ | `ub-logo` |

特に指定がなければ `language=en`、`symbol=true`、`inverse=false` をデフォルトとする。

### sp-logo のバリアント

| プロパティ | 値 | 説明 |
|-----------|-----|------|
| **sub-brand** | `null` | Speeda 単体 |
| | `ai-agent` | Speeda AI Agent |
| | `expert-research` | Speeda Expert Research |
| **language** | `en` | 英語表記 |
| | `zh` | 中国語表記 |
| **symbol** | `true` | シンボルマーク付き |
| | `false` | テキストのみ |
| **inverse** | `false` | 明るい背景用（通常） |
| | `true` | 暗い背景用（白抜き） |

### sp-symbol / ub-logo のバリアント

| プロパティ | 値 | 説明 |
|-----------|-----|------|
| **inverse** | `false` | 明るい背景用（通常） |
| | `true` | 暗い背景用（白抜き） |

## 振る舞い
- ロゴはリンクとして機能させる場合、クリックでトップページへ遷移する
- ロゴのサイズは用途に応じて調整可能だが、アスペクト比は維持する
- 最小サイズを下回らないようにする（視認性確保）

## アクセシビリティ
- リンクとして使用する場合、`aria-label="Speeda トップページへ"` などを付ける
- 装飾目的のみの場合は `alt=""` で空にする
- 画像として表示する場合は適切な `alt` テキストを設定する

## 並べ方
- ヘッダーでは左端に配置するのが基本
- ロゴの周囲には十分な余白（クリアスペース）を確保する
- 他の要素と密着させない
