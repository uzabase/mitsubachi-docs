#!/usr/bin/env python3
"""作った mockup HTML をセルフチェックする（依存なし・標準ライブラリのみ）

    python3 tools/check-mockup.py <作ったファイル.html> [...]
    python3 tools/check-mockup.py mock.html --strict   # warn も失敗にする
    python3 tools/check-mockup.py mock.html --json     # 機械可読出力

**モックを作り終えたら必ず実行し、error が 0 になるまで直すこと。**

4つの層で検査する。

  層0 kit の使い方   … 存在しないクラス・単独では効かない修飾子・必須の軸/属性/子要素の
                       欠落・幻覚アイコン名・CSS の読み込み・ベースフォント（明朝体化）
  層1 自作していないか … kit に等価物があるタグを素で使っていないか（<table> に .mi-table が
                       無い等）。「クラスを間違える」より重い逸脱をここで捕まえる
  層2 未申告の逸脱   … 独自クラスや style 属性で「見た目」を書いていないか。
                       kit に無い UI をやむを得ず作る場合は直前に
                       <!-- ds-exception: 理由 --> を書いて申告する（書けば免除される）
  層3 レビュー材料   … 申告された DS 外の箇所と、構造見本を読むべきコンポーネントを列挙

判定の根拠は全て mockup-kit/kit-index.json（tools/build-kit-index.py が CSS と見本 HTML
から自動生成）であり、このスクリプトは kit 固有の固定リストを持たない。

終了コード: 0=error なし / 1=error あり（--strict では warn でも 1）
"""

import argparse
import difflib
import json
import re
import sys
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KIT = ROOT / "design-system" / "mockup-kit"
INDEX = KIT / "kit-index.json"

# 「配置」として書いてよいプロパティ（starter.html の方針: 余白・グリッド・並びは可）
LAYOUT_PROPS = {
    "display", "gap", "row-gap", "column-gap", "position", "top", "right", "bottom",
    "left", "inset", "z-index", "order", "width", "height", "box-sizing",
    "text-align", "white-space", "vertical-align", "float", "clear", "visibility",
    "grid", "flex", "align", "justify", "place", "margin", "padding", "min", "max",
    "overflow", "aspect", "list-style", "table-layout", "resize", "cursor",
    "transition", "animation", "transform", "content", "scroll",
}
# 「見た目」＝ kit のクラスが持つべきもの（書いたら申告が必要）
VISUAL_PROPS = {
    "color", "background", "background-color", "background-image", "border",
    "border-radius", "box-shadow", "font-size", "font-weight", "font-family",
    "font", "letter-spacing", "line-height", "text-decoration", "opacity",
    "fill", "stroke", "outline", "text-shadow", "filter", "backdrop-filter",
}
# 免除するセレクタ（ページ全体のリセット）
RESET_SELECTORS = {"body", "html", "*", ":root", "*, *::before, *::after"}
# kit に代替があるため素で使うと指摘する要素（根拠: foundations/prohibited.md のアイコン・画像）
SELF_MADE_ELEMENTS = {
    "svg": ("アイコンは kit の .mi-icon を使う（アイコンセット外の持ち込みは禁止）",
            "グラフ等でやむを得ない場合は ds-exception を書く"),
    "img": ("ロゴは .mi-logo、アイコンは .mi-icon を使う",
            "写真・図版でやむを得ない場合は ds-exception を書く"),
}
# ベースフォントを与えるセレクタ（:where() を剥がして判定する）
BASE_FONT_SELECTORS = {"body", "html", "*", ":root"}
# 明朝系（地の文がこれになると世界観が壊れる）。sans-serif は除外する
SERIF_RE = re.compile(r"(?<!sans-)\bserif\b|mincho|明朝|times|georgia", re.I)
# 和文ゴシックを含む正しいスタック（未指定時の提示用。tokens.css の基礎値と同じ）
FONT_STACK_HINT = ('body { font-family: Arial, YakuHanJPs, "Hiragino Sans", '
                   '"Hiragino Kaku Gothic ProN", Meiryo, "Noto Sans JP", sans-serif; }')
DS_EXCEPTION_RE = re.compile(r"ds-exception\s*[:：]\s*(.+)", re.S)
# ページ全体で層2を免除する宣言（見本カタログ・移植テンプレ用。モックでは使わない）
DS_EXCEPTION_PAGE_RE = re.compile(r"ds-exception-page\s*[:：]\s*(.+)", re.S)


class Finding:
    def __init__(self, layer, severity, line, message, hint=""):
        self.layer, self.severity, self.line = layer, severity, line
        self.message, self.hint = message, hint

    def as_dict(self):
        return {"layer": self.layer, "severity": self.severity, "line": self.line,
                "message": self.message, "hint": self.hint}


class MockupParser(HTMLParser):
    """要素・style ブロック・link・ds-exception 注記を行番号つきで集める。"""

    VOID = {"input", "img", "br", "link", "meta", "hr", "source", "use", "path",
            "circle", "area", "col", "embed", "track", "wbr"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.elements = []
        self.links = []          # (basename, line)
        self.styles = []         # (css text, start line)
        self.scripts = []        # (src basename or None, line, inline text)
        self.exceptions = []     # (line, reason)
        self.page_exception = None
        self._pending_exception = None
        self._in_style = False
        self._style_start = 0
        self._style_buf = []
        self._in_script = False
        self._script_start = 0
        self._script_src = None
        self._script_buf = []

    # --- タグ ---
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        line = self.getpos()[0]
        classes = (d.get("class") or "").split()
        node = {
            "tag": tag, "line": line, "attrs": d,
            "classes": classes,
            "mi": [c for c in classes if c.startswith("mi-")],
            "other": [c for c in classes if not c.startswith("mi-")],
            "desc": set(), "exempt": False,
            "ancestorTags": [a["tag"] for a in self.stack],
        }
        if self._pending_exception is not None:
            node["exempt"] = True
            self._pending_exception = None
        if any(a["exempt"] for a in self.stack):
            node["exempt"] = True
        for anc in self.stack:
            anc["desc"].update(node["mi"])
        self.stack.append(node)
        self.elements.append(node)

        if tag == "link" and d.get("rel") == "stylesheet":
            self.links.append((Path(d.get("href", "")).name, line))
        if tag == "style":
            self._in_style, self._style_start, self._style_buf = True, line, []
        if tag == "script":
            self._in_script, self._script_start = True, line
            self._script_src = Path(d["src"]).name if d.get("src") else None
            self._script_buf = []
        if tag in self.VOID:
            self.stack.pop()

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in self.VOID and self.stack and self.stack[-1]["tag"] == tag:
            self.stack.pop()

    def handle_endtag(self, tag):
        if tag == "style" and self._in_style:
            self.styles.append(("".join(self._style_buf), self._style_start))
            self._in_style = False
        if tag == "script" and self._in_script:
            self.scripts.append((self._script_src, self._script_start,
                                 "".join(self._script_buf)))
            self._in_script = False
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i]["tag"] == tag:
                del self.stack[i:]
                return

    def handle_data(self, data):
        if self._in_style:
            self._style_buf.append(data)
        if self._in_script:
            self._script_buf.append(data)

    def handle_comment(self, data):
        page = DS_EXCEPTION_PAGE_RE.search(data)
        if page:
            self.page_exception = (self.getpos()[0], " ".join(page.group(1).split())[:120])
            return
        m = DS_EXCEPTION_RE.search(data)
        if m:
            reason = " ".join(m.group(1).split())
            self.exceptions.append((self.getpos()[0], reason[:120]))
            self._pending_exception = self.getpos()[0]


# --- ヘルパ -----------------------------------------------------------------
def prop_kind(name):
    """プロパティが「配置」か「見た目」か。判定できないものは None（無視）。"""
    name = name.strip().lower().lstrip("-")
    if name in VISUAL_PROPS:
        return "visual"
    head = name.split("-")[0]
    if name in LAYOUT_PROPS or head in LAYOUT_PROPS:
        return "layout"
    return None


def parse_declarations(text):
    return [(m.group(1), m.group(2).strip())
            for m in re.finditer(r"([a-zA-Z-]+)\s*:\s*([^;{}]+)", text)]


def css_rules(text, start_line):
    """(セレクタ, 宣言部, 行番号, 免除フラグ) を返す簡易 CSS 走査。
    /* ds-exception: 理由 */ は、それ以降そのブロック末尾までのルールを免除する
    （1行ずつ書かせると冗長になるため。免除したルールは層3に件数が出る）。"""
    rules = []
    exempt = False
    for m in re.finditer(r"([^{}]*)\{([^{}]*)\}", text):
        sel_raw, body = m.group(1), m.group(2)
        line = start_line + text.count("\n", 0, m.start(2))
        if re.search(r"/\*[^*]*ds-exception", sel_raw, re.S):
            exempt = True
        lines = [l.strip() for l in re.sub(r"/\*.*?\*/", "", sel_raw, flags=re.S).split("\n")
                 if l.strip()]
        sel = lines[-1] if lines else ""
        if sel.startswith("@"):
            continue
        rules.append((sel, body, line, exempt))
    return rules


def base_font_decls(p):
    """body / html / * / :root に効く font-family 指定を (値, 行) で返す。"""
    out = []
    for css, start in p.styles:
        for sel, body, line, _ in css_rules(css, start):
            plain = re.sub(r":where\(([^)]*)\)", r"\1", sel).lower()
            if not {s.strip() for s in plain.split(",")} & BASE_FONT_SELECTORS:
                continue
            out += [(v, line) for n, v in parse_declarations(body)
                    if n.strip().lower() in ("font-family", "font")]
    for e in p.elements:
        if e["tag"] in ("body", "html") and "style" in e["attrs"]:
            out += [(v, e["line"]) for n, v in parse_declarations(e["attrs"]["style"])
                    if n.strip().lower() in ("font-family", "font")]
    return out


def suggest(name, candidates):
    near = difflib.get_close_matches(name, candidates, n=2, cutoff=0.75)
    return f"（近いもの: {', '.join('.' + c for c in near)}）" if near else ""


# --- 検査本体 ---------------------------------------------------------------
class Checker:
    def __init__(self, index):
        self.idx = index
        self.components = index["components"]
        self.bases = set(self.components)
        self.defined = set(self.components)
        for base, e in self.components.items():
            self.defined |= {base + m for m in e.get("modifiers", [])}
        self.icons_builtin = set(index["icons"]["builtin"])
        self.icons_extra = set(index["icons"]["extra"])
        self.logos = set(index["logos"])

    def check(self, path):
        text = path.read_text(encoding="utf-8")
        p = MockupParser()
        p.feed(text)
        self.css_exempted = 0
        f = []
        f += self.layer0_css(p, text)
        f += self.layer0_classes(p)
        f += self.layer1_self_made(p)
        f += self.layer2_undeclared(p)
        return f, p

    # --- 層0: CSS の読み込み -----------------------------------------------
    def layer0_css(self, p, text):
        out = []
        names = [n for n, _ in p.links]
        required = self.idx["css"]["required"]
        inline_kit = bool(re.search(r"\.mi-[\w-]+\s*\{", text)) and not names
        if inline_kit:
            out.append(Finding("0", "warn", 1,
                               "kit の CSS がインライン展開されている",
                               "可能なら tokens.css → mitsubachi-mockup.css の link 読み込みにする"
                               "（インラインは Figma 更新に追従できない）"))
        else:
            for req in required:
                if req not in names:
                    out.append(Finding("0", "error", 1, f"{req} を読み込んでいない",
                                       "CHEATSHEET.md「読み込み（この順で）」参照"))
            if all(r in names for r in required):
                order = [names.index(r) for r in required]
                if order != sorted(order):
                    out.append(Finding("0", "error", p.links[0][1],
                                       f"CSS の読み込み順が違う（{' → '.join(required)} の順）",
                                       "mitsubachi-mockup.css は tokens.css の変数を参照する"))
        out += self.layer0_base_font(p, names, required)
        if inline_kit:
            return out
        used = {c for e in p.elements for c in e["mi"]}
        icons_used = {c[len("mi-icon--"):] for c in used if c.startswith("mi-icon--")}
        if icons_used - self.icons_builtin and "mitsubachi-icons.css" not in names:
            extra = sorted(icons_used - self.icons_builtin)[:3]
            out.append(Finding("0", "error", 1,
                               f"mitsubachi-icons.css を読み込んでいないのに内蔵以外の"
                               f"アイコンを使っている（{', '.join(extra)} など）",
                               "内蔵は " + " / ".join(sorted(self.icons_builtin))))
        if any(c == "mi-logo" or c.startswith("mi-logo--") for c in used) \
                and "mitsubachi-logos.css" not in names:
            out.append(Finding("0", "error", 1,
                               "mitsubachi-logos.css を読み込んでいないのにロゴを使っている"))
        return out

    # --- 層0: ベースフォント（地の文の明朝体化） -----------------------------
    def layer0_base_font(self, p, names, required):
        """`.mi-*` を当てていない地の文が明朝体で出る状態を検出する。

        mitsubachi-mockup.css の `:where(body)` がベースフォントを与えるので、
        kit の CSS を link で読んでいれば安全。読んでいない場合は自前の
        body 指定が必須（無ければブラウザ既定＝明朝体になる）。"""
        out = []
        decls = base_font_decls(p)
        for value, line in decls:
            if SERIF_RE.search(value):
                out.append(Finding("0", "error", line,
                                   f"ベースフォントに明朝系を指定している（{value.strip()}）",
                                   "和文はゴシック。" + FONT_STACK_HINT))
        if not all(r in names for r in required) and not decls:
            out.append(Finding("0", "error", 1,
                               "ベースフォント未指定（kit の CSS を読み込まず body にも "
                               "font-family が無い）",
                               "`.mi-*` の無い地の文がブラウザ既定の明朝体で出る。"
                               f"CSS を読み込むか {FONT_STACK_HINT} を書く"))
        return out

    # --- 層0: クラスの使い方 -----------------------------------------------
    def layer0_classes(self, p):
        out = []
        for e in p.elements:
            if not e["mi"]:
                continue
            line = e["line"]
            for cls in e["mi"]:
                if cls in self.defined:
                    continue
                if cls.startswith("mi-icon--"):
                    name = cls[len("mi-icon--"):]
                    if name not in self.icons_builtin | self.icons_extra:
                        out.append(Finding("0", "error", line,
                                           f".{cls} — 存在しないアイコン名"
                                           f"{suggest(name, sorted(self.icons_extra))}",
                                           "一覧: mockup-kit/components/icons.html"))
                        continue
                elif cls.startswith("mi-logo--"):
                    if cls[len("mi-logo--"):] not in self.logos:
                        out.append(Finding("0", "error", line,
                                           f".{cls} — 存在しないロゴ名",
                                           "一覧: mockup-kit/components/logos.html"))
                        continue
                else:
                    out.append(Finding("0", "error", line,
                                       f".{cls} — CSS に定義が無いクラス"
                                       f"{suggest(cls, sorted(self.defined))}",
                                       "自作クラスなら .mi- 接頭辞を使わない"))
                    continue

            bases = [c for c in e["mi"] if c in self.bases]
            for base in bases:
                ent = self.components[base]
                raw_mods = [c for c in e["mi"] if c.startswith(base + "--")]
                mods = [c[len(base):] for c in raw_mods
                        if c[len(base):] in ent.get("modifiers", [])]
                low = ent.get("lowConfidence")
                sev = "warn" if low else "error"

                # 必ず1つ選ぶ軸
                for group in ent.get("requiredOneOf", []):
                    if not set(mods) & set(group):
                        out.append(Finding("0", "error", line,
                                           f".{base} に必須の修飾子が無い"
                                           f"（{' / '.join(base + g for g in group)} から1つ）"))
                if ent.get("requiredAnyModifier") and not raw_mods:
                    out.append(Finding("0", "error", line,
                                       f".{base} は単独では使えない"
                                       f"（種類を指定する修飾子が必要）"))
                # 単独では効かない修飾子
                for mod, partners in ent.get("compoundOnly", {}).items():
                    if mod in mods and not (set(mods) & set(partners)):
                        out.append(Finding("0", "error", line,
                                           f".{base}{mod} は単独では効かない",
                                           "併用: " + " / ".join(base + x for x in partners)))
                # 修飾子が要求する子要素
                for mod, children in ent.get("modifierRequiresChild", {}).items():
                    if mod in mods:
                        missing = [c for c in children if c not in e["desc"]]
                        if missing:
                            out.append(Finding("0", sev, line,
                                               f".{base}{mod} の中に "
                                               f"{' / '.join('.' + c for c in missing)} が無い"))
                # 必須の子要素
                missing = [c for c in ent.get("requiredParts", []) if c not in e["desc"]]
                if missing:
                    hint = ""
                    if base in self.idx["requiresSample"]:
                        hint = f"構造は見本を踏襲する（mockup-kit/components/）"
                    out.append(Finding("0", sev, line,
                                       f".{base} の構成要素が足りない"
                                       f"（{' / '.join('.' + c for c in missing)}）", hint))
                # 必須の属性・role
                for attr in ent.get("requiredAttrs", []):
                    if attr not in e["attrs"]:
                        out.append(Finding("0", sev, line,
                                           f".{base} に {attr} が無い"))
                roles = ent.get("requiredRole")
                if roles and e["attrs"].get("role") not in roles:
                    out.append(Finding("0", sev, line,
                                       f".{base} の role は "
                                       f"{' / '.join(roles)} のいずれか"
                                       f"（現在: {e['attrs'].get('role') or 'なし'}）"))
        return out

    # --- 層1: 等価物があるのに自作していないか ------------------------------
    def layer1_self_made(self, p):
        out = []
        for e in p.elements:
            if e["exempt"]:
                continue
            tag, attrs = e["tag"], e["attrs"]
            key = f'input[type={attrs.get("type")}]' if tag == "input" else tag
            rule = self.idx["tagRules"].get(key)
            if rule and tag == "table" and attrs.get("role") == "presentation":
                rule = None
            if rule and not (set(e["classes"]) & set(rule["allowed"])):
                out.append(Finding("1", rule["severity"], e["line"],
                                   f"<{key}> に kit のクラスが無い（自作しない）",
                                   "いずれかを当てる: "
                                   + " / ".join("." + c for c in rule["allowed"])))
            # kit のアイコン・ロゴは CSS の背景画像なので <svg>/<img> は本来不要。
            # 入れ子の svg（path 等）は親だけ指摘すれば足りるので先頭の svg のみ見る。
            if tag in SELF_MADE_ELEMENTS and "svg" not in e["ancestorTags"]:
                msg, hint = SELF_MADE_ELEMENTS[tag]
                out.append(Finding("1", "warn", e["line"],
                                   f"<{tag}> を直接置いている — {msg}", hint))
        return out

    # --- 層2: 未申告の逸脱 --------------------------------------------------
    def layer2_undeclared(self, p):
        out = []
        if p.page_exception:
            line, reason = p.page_exception
            return [Finding("2", "warn", line,
                            f"ページ全体を ds-exception-page で免除している（{reason}）",
                            "見本カタログや移植テンプレ以外では使わない。"
                            "モックは箇所ごとに <!-- ds-exception: 理由 --> で申告する")]
        # <style> ブロック
        for css, start in p.styles:
            for sel, body, line, exempted in css_rules(css, start):
                if not sel:
                    continue
                visual = sorted({n for n, _ in parse_declarations(body)
                                 if prop_kind(n) == "visual"})
                if not visual:
                    continue
                if exempted:
                    self.css_exempted += 1
                    continue
                if sel.lower() in RESET_SELECTORS:
                    continue
                if ".mi-" in sel:
                    out.append(Finding("2", "error", line,
                                       f"kit のクラスを上書きしている（{sel} → "
                                       f"{', '.join(visual)}）",
                                       "コンポーネントの見た目は上書きしない"
                                       "（foundations/prohibited.md）"))
                else:
                    kind = "独自クラス" if ("." in sel or "#" in sel) else "要素セレクタ"
                    out.append(Finding("2", "error", line,
                                       f"{kind}で見た目を定義している"
                                       f"（{sel} → {', '.join(visual)}）",
                                       "kit のクラスで組む。やむを得ない場合は直前に "
                                       "/* ds-exception: 理由 */ を書く"))
        # style 属性
        for e in p.elements:
            if e["exempt"] or "style" not in e["attrs"]:
                continue
            visual = sorted({n for n, _ in parse_declarations(e["attrs"]["style"])
                             if prop_kind(n) == "visual"})
            if visual:
                out.append(Finding("2", "error", e["line"],
                                   f"<{e['tag']}> の style 属性に見た目を書いている"
                                   f"（{', '.join(visual)}）",
                                   "モック側に書いてよいのは配置（余白・グリッド・並び）だけ。"
                                   "必要なら直前に <!-- ds-exception: 理由 --> を書く"))
        return out

    # --- 層3: レビュー材料 --------------------------------------------------
    def layer3_report(self, p):
        notes = []
        for line, reason in p.exceptions:
            notes.append((line, f"ds-exception: {reason}"))
        if getattr(self, "css_exempted", 0):
            notes.append((0, f"ds-exception により CSS {self.css_exempted} ルールを免除"))
        used_bases = {c for e in p.elements for c in e["mi"] if c in self.bases}
        for base in sorted(used_bases & set(self.idx["requiresSample"])):
            ent = self.components[base]
            samples = "・".join(ent.get("samples", []))
            notes.append((0, f".{base} を使用 — 構造は見本 {samples} を踏襲しているか確認"))
        custom = defaultdict(list)
        for e in p.elements:
            if e["mi"] or not e["other"] or e["exempt"]:
                continue
            for c in e["other"]:
                custom[c].append(e["line"])
        shown = sorted(custom.items(), key=lambda kv: -len(kv[1]))
        for c, lines in shown[:5]:
            notes.append((lines[0], f"kit 由来でない独自クラス .{c}"
                                    f"（{len(lines)} 箇所）— 配置用なら問題なし"))
        if len(shown) > 5:
            notes.append((0, f"kit 由来でない独自クラスが他に {len(shown) - 5} 種"))
        scripts = [(src, line) for src, line, body in p.scripts
                   if src != self.idx["css"].get("script") and (src or body.strip())]
        for src, line in scripts:
            notes.append((line, f"独自 JS（{src or 'インライン'}）— 挙動は "
                                f"{self.idx['css'].get('script')} で足りないか確認"))
        return notes


# --- 出力 -------------------------------------------------------------------
LAYER_TITLE = {
    "0": "層0 kit の使い方",
    "1": "層1 自作していないか",
    "2": "層2 未申告の逸脱",
}
MARK = {"error": "✗", "warn": "▲"}


def print_report(path, findings, notes):
    print(f"\nmockup セルフチェック: {path}")
    for layer in ("0", "1", "2"):
        fs = sorted((f for f in findings if f.layer == layer), key=lambda x: x.line)
        print(f"\n  {LAYER_TITLE[layer]}")
        if not fs:
            print("    ✓ 指摘なし")
            continue
        for f in fs:
            print(f"    {MARK[f.severity]} [{f.severity}] L{f.line}: {f.message}")
            if f.hint:
                print(f"        → {f.hint}")
    print("\n  層3 レビュー材料")
    if not notes:
        print("    ✓ DS 外の要素・申告なし")
    for line, text in sorted(notes):
        loc = f"L{line}: " if line else ""
        print(f"    · {loc}{text}")


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("files", nargs="+", help="検査する mockup HTML")
    ap.add_argument("--strict", action="store_true", help="warn も失敗にする")
    ap.add_argument("--json", action="store_true", dest="as_json")
    args = ap.parse_args()

    if not INDEX.exists():
        print(f"✗ {INDEX.relative_to(ROOT)} が無い。"
              f"先に python3 tools/build-kit-index.py を実行してください。", file=sys.stderr)
        return 1
    checker = Checker(json.loads(INDEX.read_text(encoding="utf-8")))

    results, errors, warns = [], 0, 0
    for name in args.files:
        path = Path(name)
        if not path.exists():
            print(f"✗ {name} が見つからない", file=sys.stderr)
            return 1
        findings, parser = checker.check(path)
        notes = checker.layer3_report(parser)
        errors += sum(1 for f in findings if f.severity == "error")
        warns += sum(1 for f in findings if f.severity == "warn")
        if args.as_json:
            results.append({"file": str(path),
                            "findings": [f.as_dict() for f in findings],
                            "notes": [{"line": l, "note": t} for l, t in notes]})
        else:
            print_report(path, findings, notes)

    if args.as_json:
        print(json.dumps({"files": results, "error": errors, "warn": warns},
                         ensure_ascii=False, indent=2))
    else:
        print(f"\n判定: error {errors} 件 / warn {warns} 件", end="  ")
        if errors:
            print("→ error を全て直してから完了とすること")
        elif warns:
            print("→ warn は意図的なら ds-exception を書いて申告する")
        else:
            print("→ 問題なし")
    return 1 if (errors or (args.strict and warns)) else 0


if __name__ == "__main__":
    sys.exit(main())
