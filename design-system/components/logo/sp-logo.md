# sp-logo

Speeda ロゴ（テキスト＋シンボル）を表示するコンポーネントです。ヘッダーやフッター、ログイン画面などでブランドを明示するために使用します。

## 使いどころと選び方

### 使うべきシーン
- ヘッダー、フッター、ログイン画面など Speeda ブランドを表示する場面
- サブブランド（AI Agent、Expert Research）を含むロゴが必要な場面
- 暗い背景に白抜きロゴを表示する場面（inverse）

### 使わないほうがよいシーン
- シンボルマークのみで十分な場合（ファビコン、省スペース） → [sp-symbol](./sp-symbol.md)
- 親会社 Uzabase のロゴを表示する場合 → [ub-logo](./ub-logo.md)

## Figma

<!-- TODO: コンポーネントのnode-idを確認 -->

> mockup で再現する場合は `mockup/mitsubachi-logos.css` を追加読み込みして `.mi-logo--speeda-ja/--speeda-en/--speeda-zh/--speeda-ai-agent` を使う（自作しない）。

## 構成とルール

### バリエーション・状態

| プロパティ | 値 | 説明 |
|-----------|-----|------|
| sub-brand | null / ai-agent / expert-research | サブブランドの指定 |
| language | en / zh | 言語表記 |
| symbol | true / false | シンボルマーク付きかテキストのみか |
| inverse | false / true | 明るい背景用（通常）/ 暗い背景用（白抜き） |

#### sub-brand
| sub-brand | 使いどころ |
|-----------|-----------|
| **null** | Speeda 単体のロゴ |
| **ai-agent** | Speeda AI Agent のロゴ |
| **expert-research** | Speeda Expert Research のロゴ |

### コンテンツルール
- 特に指定がなければ `language=en`、`symbol=true`、`inverse=false` をデフォルトとする
- ロゴのサイズは用途に応じて調整可能だが、アスペクト比は維持する
- 最小サイズを下回らないようにする（視認性確保）

## Do
- ヘッダーでは左端に配置する
- ロゴの周囲には十分な余白（クリアスペース）を確保する
- 暗い背景では `inverse=true` を使用する

## Don't
- ロゴのアスペクト比を変えない
- 他の要素とロゴを密着させない
- 最小サイズを下回るサイズで使用しない
