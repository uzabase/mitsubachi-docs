# color

ミツバチのカラーシステム。primitive-color → ui-primitive-color → semantic-color の3層で構成される。

> 具体的な値は Figma の variable が正。実装では [mitsubachi-token](https://github.com/uzabase/mitsubachi-token) を参照。

## カラーパレットの階層

| 階層 | 実装への読み込み | 説明 |
|------|:---:|------|
| **primitive-color** | 不可 | Speeda ブランドで使用できる全てのカラー |
| **ui-primitive-color** | 可 | primitive-color からプロダクトで使用する色のみを抽出 |
| **semantic-color** | 可 | ui-primitive-color を参照し、役割ごとに命名したカラー。**画面で使うのはこれ** |

---

## primitive-color

### 設計原則

- **知覚的同一性**: CIE Lab 色空間を基準に設計。スケール値が同じであれば色相を問わず視覚的な明るさ（L値）が一致する
- **コントラスト予見性**: L値を固定することで、色相に依存せず WCAG AA 基準のコントラスト比を担保する
- **汎用性と拡張性**: UIだけでなくグラフィックデザインや販促物でも一貫したトーンを維持する

### カラー構成

- **有彩色（19色）**: 10刻みの明度スケールを展開
- **無彩色（Neutral）**: 最大値は `#191919`（純黒を避け、画面全体のコントラストを和らげる）
- **アルファ**: White Alpha は `#FFFFFF`、Black Alpha は `#000000` を基準

### モード対応

primitive-color は固定値。Light/Dark の切り替えは semantic-color 側で行う。

---

## ui-primitive-color

### 設計原則

- すべての値は primitive-color を参照し、独自のカラーコードは持たない
- エンジニア・デザイナーが使う色を限定し、実装時のミス削減とアセットの軽量化を図る

### カラー構成（13種類）

| 色 | 主な用途 |
|----|---------|
| black | 状態変化での使用 |
| neutral / neutral(alpha) | 基本的な色 |
| white / white(alpha) | 基本的な白 |
| red | ブランドカラー |
| tomato | エラー・危険・ネガティブな状態 |
| yellow | 警告 |
| blue | 選択中・インフォメーション |
| green | 成功・ポジティブな状態 |
| brown / plum / violet / viridian | avatar の色バリエーション |

### モード対応

ui-primitive-color 自体にダークモード用の反転ロジックは持たせない。切り替えは semantic-color で制御する。

---

## semantic-color

### 設計原則

- すべての値は ui-primitive-color を参照し、役割ごとに命名する
- WCAG AA コントラスト比を満たす組み合わせで運用する

### 命名の構成要素

**UI要素**

| 要素 | 意味 |
|------|------|
| background | ページ全体の基盤となる最背面の色 |
| zabuton | 状態変化がない独立した面の背景色 |
| focus-ring | キーボード操作・入力中の focus を表す枠線 |
| border | 線の色 |
| text | 文字色 |
| object | アイコンや装飾的な要素の色 |
| surface | background・zabuton・object 以外のコンポーネント背景の面塗り |
| chart | グラフの色（現在はヒートマップのみ） |
| palette | 意味を持たない色のバリエーション（avatar 等） |

**強弱（5段階）**

| 強弱 | 意味 |
|------|------|
| strong | 強い |
| semi-strong | やや強い |
| regular | 普通（基準） |
| semi-weak | やや弱い |
| weak | 弱い |

**役割**

| 役割 | 意味 |
|------|------|
| danger | 破壊的変更 |
| error | エラー |
| information | 情報 |
| link | リンク |
| negative | 売上減少、ロック中などネガティブな要素 |
| positive | 売上増加、推奨などポジティブな要素 |
| required | 必須項目 |
| success | 成功 |
| warning | 警告 |
| notice | お知らせの通知 |
| emphasized | 強調 |

**状態変化**

default / hover / focus / active / selected / checked / unchecked / disabled / inactive / overlay / current

### Surface の使い分けルール

- neutral カラーのデフォルト時の色は4パターン。それぞれに対応する状態変化の色が決まっている
- default と同じ強弱の色を状態変化に使う（例: `surface/regular-default` → `surface/regular-hover`）
- 強弱をまたいだ組み合わせはしない（例: `surface/regular-default` → `surface/strong-hover` は NG）

### Alpha の使用ルール

surface では alpha を限定的に使用する。

| 適用箇所 | 理由 |
|---------|------|
| 全コンポーネントの disabled | どの背景でも非活性であることをわかりやすくする |
| button の hover・active | どの背景に乗ってもほぼ一律同じに見せたい |
| thumbnail の hover | 画像を少し暗く見せるために透過が必要 |
| menu の hover・active | ダークモードで背景色と状態変化の色が同化するのを防ぐ |
| side navigation の hover・active・current | 既存の surface/semi-strong 系と同化するのを防ぐ |
| radio-button・checkbox の hover・active | カード内でhover時に色が浮くのを防ぐ |

---

## 禁止事項

- 実装時に primitive-color / ui-primitive-color を直接指定しない。必ず semantic-color を使用する
- 「色が同じだから」という理由で、本来の意味と異なる役割の色を流用しない（例: エラーではないが文字を赤くしたい場合に `text/error` を使用しない）
- 該当する semantic-color がない場合は、既存色を当て込まず新設を検討する

## アクセシビリティ

- text: コントラスト比 4.5:1 以上（WCAG AA）
- object（アイコン等）: コントラスト比 3.0:1 以上（WCAG AA）
