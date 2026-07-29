#!/usr/bin/env python3
"""kit-index.json を生成する（依存なし・標準ライブラリのみ）

    python3 tools/build-kit-index.py

mockup-kit/kit-index.json を出力する。AI が 3116 行の CSS を読まずに
「クラスの正しい当て方」を機械的に引けるようにするための索引で、
tools/check-mockup.py（生成物のセルフチェック）もこれを唯一の根拠として動く。

【思想】固定リストを持たない。ルールは全て実ファイルから導出する。
  - どのクラスが存在するか            → *.css の定義
  - 単独では効かないクラス            → CSS の複合セレクタ
  - 必ず1つ選ぶ修飾子（variant 等）   → 見本 HTML で 100% 使われている修飾子グループ
  - 必須の属性・role・子孫要素        → 見本 HTML の全インスタンスに共通するもの
  - あるタグに必ず付けるクラス        → 見本 HTML でそのタグが素で使われた実績が無いこと
つまり「見本 HTML が満たしていることは規則」とみなす。kit を拡張すれば索引も自動で追従し、
このスクリプトの更新は原則不要。

終了コード: 0=生成成功 / 1=生成物に矛盾があり中断
"""

import json
import re
import sys
from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DS = ROOT / "design-system"
KIT = DS / "mockup-kit"
OUT = KIT / "kit-index.json"

# 必須と見なしてよい属性（見た目や中身に依存しないもの）。
# placeholder / rows / style などは「たまたま見本が全部持っていた」だけなので除外する。
ATTR_ALLOW = {"role", "href", "type", "name", "scope", "alt", "for"}
# 見本の n が少ないクラスは「全インスタンス共通」の信頼度が低いので警告扱いにする閾値
CONFIDENT_N = 3
# 修飾子が多い軸（アイコン名など）は列挙せずフラグで表す
MAX_GROUP_ENUM = 12
# 同じ軸と見なすプロパティ集合の類似度（見本に出ていない修飾子を軸へ吸収する閾値）
AXIS_SIMILARITY = 0.6
# kit に必ず等価コンポーネントがあるタグ（自作したら error、それ以外のタグは warn）。
# 規則自体は見本から導出しており、これは重大度の判断にのみ使う。
STRICT_TAGS = {"button", "input", "select", "textarea", "table"}


# --- HTML 走査 ---------------------------------------------------------------
class Collector(HTMLParser):
    """開始タグごとに (タグ, クラス, 属性, 子孫クラス) を集める。"""

    VOID = {"input", "img", "br", "link", "meta", "hr", "source", "use", "path",
            "circle", "area", "col", "embed", "track", "wbr"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.nodes = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        cls = [c for c in (d.get("class") or "").split() if c.startswith("mi-")]
        node = {
            "tag": tag,
            "type": d.get("type"),
            "cls": cls,
            "attrs": {k for k in d if k in ATTR_ALLOW or k.startswith("aria-")},
            "role": d.get("role"),
            "desc": set(),
        }
        for anc in self.stack:
            anc["desc"].update(cls)
        self.stack.append(node)
        self.nodes.append(node)
        if tag in self.VOID:
            self.stack.pop()

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in self.VOID:
            self.stack.pop()

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i]["tag"] == tag:
                del self.stack[i:]
                return


def read(p):
    return p.read_text(encoding="utf-8")


def sample_files():
    return sorted(list((KIT / "components").glob("*.html")) +
                  list((KIT / "templates").glob("*.html")))


def collect_nodes():
    nodes = []
    for f in sample_files():
        c = Collector()
        c.feed(read(f))
        rel = str(f.relative_to(KIT))
        for n in c.nodes:
            n["file"] = rel
        nodes += c.nodes
    return nodes


# --- CSS 走査 ---------------------------------------------------------------
def css_classes(text):
    return set(re.findall(r"\.(mi-[\w-]+)", text))


def compound_only_modifiers(css):
    """.mi-x--a.mi-x--b の形でしか定義されない修飾子（単独では効かない）を返す。
    check-kit.py の同名検査と同じ導出ロジック。"""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    compound, standalone = set(), set()
    for sel in re.findall(r"([^{}]+)\{", css):
        for part in (p.strip() for p in sel.split(",")):
            has_pseudo = bool(re.search(r":(hover|active|focus|disabled|checked)", part))
            base = re.sub(r"::?[a-z-]+(\([^)]*\))?", "", part)
            for chain in re.findall(r"((?:\.mi-[\w-]+){2,})(?=\s|$|>|\[)", base):
                mods = [c for c in re.findall(r"\.mi-[\w-]+", chain) if "--" in c]
                if len(mods) >= 2:
                    compound.add(mods[-1].lstrip("."))
            m = re.match(r"^(\.mi-[\w-]+--[\w-]+)(\s|$|\[|>)", base.strip())
            if m and not has_pseudo:
                standalone.add(m.group(1).lstrip("."))
    return compound - standalone


def modifier_props(css):
    """修飾子ごとに「単独セレクタで宣言している CSS プロパティ名の集合」を返す。
    variant（色を宣言）と size（寸法を宣言）のような軸の判別に使う。"""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    props = defaultdict(set)
    for sel, body in re.findall(r"([^{}]*)\{([^{}]*)\}", css):
        # @media 等のネストを含む場合は最後の行がセレクタ
        lines = [l.strip() for l in sel.split("\n") if l.strip()]
        if not lines:
            continue
        names = set(re.findall(r"([a-z-]+)\s*:", body))
        for part in lines[-1].split(","):
            m = re.fullmatch(r"\.(mi-[\w-]+--[\w-]+)(::?[a-z-]+(\([^)]*\))?)?", part.strip())
            if m:
                props[m.group(1)] |= names
    return props


def absorb_into_axis(base, group, all_mods, seen_mods, props):
    """見本に出ていない修飾子を、プロパティ構成が同じ軸へ吸収する。
    例: 見本に --information/--warning しか無い banner に、CSS 上の --error/--success を加える。
    見本に出ている修飾子は共起関係で既に分類済みなので対象にしない（誤って軸に混ぜないため）。"""
    core = set.intersection(*[props.get(m, set()) for m in group]) if group else set()
    if not core:
        return group
    added = []
    for mod in all_mods:
        if mod in group or mod in seen_mods:
            continue
        p = props.get(mod, set())
        if not p:
            continue
        sim = len(p & core) / len(p | core)
        if sim >= AXIS_SIMILARITY:
            added.append(mod)
    return sorted(group + added)


def compound_partners(css, modifier):
    """単独では効かない修飾子が、どの修飾子と併用されて定義されているかを返す。"""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    partners = set()
    for sel in re.findall(r"([^{}]+)\{", css):
        for part in (p.strip() for p in sel.split(",")):
            base = re.sub(r"::?[a-z-]+(\([^)]*\))?", "", part)
            for chain in re.findall(r"((?:\.mi-[\w-]+){2,})(?=\s|$|>|\[)", base):
                mods = [c.lstrip(".") for c in re.findall(r"\.mi-[\w-]+", chain) if "--" in c]
                if modifier in mods:
                    partners |= {m for m in mods if m != modifier}
    return partners


# --- 修飾子グループの導出 ----------------------------------------------------
def exclusive_groups(instances, modifiers):
    """見本での共起関係から「互いに併用されない修飾子のグループ」を作る。
    variant（primary/secondary/…）や size（medium/large/…）がここに落ちる。"""
    cooccur = defaultdict(set)
    for inst in instances:
        mods = [m for m in inst if m in modifiers]
        for a in mods:
            cooccur[a] |= {b for b in mods if b != a}
    groups = []
    for mod, _ in Counter(
        m for inst in instances for m in inst if m in modifiers
    ).most_common():
        for g in groups:
            if not (cooccur[mod] & set(g)):
                g.append(mod)
                break
        else:
            groups.append([mod])
    return [sorted(g) for g in groups if len(g) >= 2]


def required_group(groups, instances):
    """全インスタンスで必ず1つ使われているグループ（＝必須の軸）を返す。"""
    required = []
    for g in groups:
        if all(set(inst) & set(g) for inst in instances):
            required.append(sorted(g))
    return required


# --- 索引の組み立て ---------------------------------------------------------
def build():
    css_main = read(KIT / "mitsubachi-mockup.css")
    css_icons = read(KIT / "mitsubachi-icons.css")
    css_logos = read(KIT / "mitsubachi-logos.css")

    defined = set()
    for css in sorted(KIT.glob("*.css")):
        defined |= css_classes(read(css))

    icons_builtin = sorted(c[len("mi-icon--"):] for c in css_classes(css_main)
                           if c.startswith("mi-icon--"))
    icons_extra = sorted(c[len("mi-icon--"):] for c in css_classes(css_icons)
                         if c.startswith("mi-icon--"))
    logos = sorted(c[len("mi-logo--"):] for c in css_classes(css_logos)
                   if c.startswith("mi-logo--"))

    compound_only = sorted(compound_only_modifiers(css_main))
    mod_props = modifier_props(css_main)

    nodes = collect_nodes()
    bases = sorted(c for c in defined if "--" not in c)

    # base ごとにインスタンスを集める（base クラスを直接持つ要素）
    by_base = defaultdict(list)
    for n in nodes:
        for c in n["cls"]:
            if c in bases:
                by_base[c].append(n)

    components = {}
    for base in bases:
        insts = by_base.get(base)
        mods = sorted(c for c in defined if c.startswith(base + "--"))
        entry = {"modifiers": [m[len(base):] for m in mods]}

        # 見本にあるクラスからだけ「規則」を導出する。見本に無いものは索引に載せるだけ。
        if insts:
            n = len(insts)
            entry["samples"] = sorted({i["file"] for i in insts})
            entry["sampleCount"] = n

            mod_sets = [[c for c in i["cls"] if c in mods] for i in insts]
            seen_mods = {m for s in mod_sets for m in s}
            groups = exclusive_groups(mod_sets, set(mods))
            req = required_group(groups, mod_sets)
            # 見本に出ていない同軸の修飾子（--error など）を CSS から軸へ補う。
            # これをしないと「見本に無い variant を使ったら必須欠落」と誤判定する。
            groups = [absorb_into_axis(base, g, mods, seen_mods, mod_props) for g in groups]
            req = [absorb_into_axis(base, g, mods, seen_mods, mod_props) for g in req]
            # 修飾子が多すぎる軸（アイコン名・ロゴ名）は列挙せずフラグにする
            big = [g for g in req if len(g) > MAX_GROUP_ENUM]
            groups = [g for g in groups if len(g) <= MAX_GROUP_ENUM]
            req = [g for g in req if len(g) <= MAX_GROUP_ENUM]
            if big:
                entry["requiredAnyModifier"] = True
            if groups:
                entry["exclusiveGroups"] = [[m[len(base):] for m in g] for g in groups]
            if req:
                entry["requiredOneOf"] = [[m[len(base):] for m in g] for g in req]
            required_axis_mods = {m for g in req for m in g} | {m for g in big for m in g}

            attrs = set.intersection(*[i["attrs"] for i in insts])
            if attrs:
                entry["requiredAttrs"] = sorted(attrs)
            roles = {i["role"] for i in insts}
            if None not in roles:
                entry["requiredRole"] = sorted(roles)

            # 必須の子孫は base__* の要素クラスに限る（無関係な共起を拾わないため）
            common = set.intersection(*[i["desc"] for i in insts])
            parts = sorted(c for c in common if c.startswith(base + "__"))
            if parts:
                entry["requiredParts"] = parts

            # 修飾子固有の必須子孫（--loading → mi-loading など）。
            # variant / size のような必須軸は「その色だから中身が決まる」わけがないので除く
            # （見本の偶然で --secondary → mi-icon--search 等を拾ってしまうため）。
            plain = [i for i in insts if not [c for c in i["cls"] if c in mods]]
            mod_requires = {}
            for m in mods:
                if m in required_axis_mods:
                    continue
                withm = [i for i in insts if m in i["cls"]]
                if len(withm) < 2:
                    continue
                c = set.intersection(*[i["desc"] for i in withm])
                c -= common
                if plain:
                    c -= set.union(*[i["desc"] for i in plain])
                c = {x for x in c if not x.startswith(base + "__")}
                if c:
                    mod_requires[m[len(base):]] = sorted(c)
            if mod_requires:
                entry["modifierRequiresChild"] = mod_requires
            if n < CONFIDENT_N:
                entry["lowConfidence"] = True

        co = [m[len(base):] for m in mods if m in compound_only]
        if co:
            entry["compoundOnly"] = {
                m: sorted(p[len(base):] for p in compound_partners(css_main, base + m)
                          if p.startswith(base + "--"))
                for m in co
            }
        components[base] = entry

    # タグ → 必ず付けるクラス（素で使われた実績が無いタグだけ規則化する）
    tag_usage = defaultdict(Counter)
    for n in nodes:
        key = f'input[type={n["type"]}]' if n["tag"] == "input" else n["tag"]
        head = next((c for c in n["cls"] if c in bases), None) or (
            n["cls"][0] if n["cls"] else None)
        tag_usage[key][head or "(none)"] += 1
    tag_rules = {}
    for tag, counter in sorted(tag_usage.items()):
        if counter["(none)"] or tag in ("html", "head", "body"):
            continue
        allowed = sorted(k for k in counter if k != "(none)")
        total = sum(counter.values())
        tag_rules[tag] = {
            "allowed": allowed,
            "sampleCount": total,
            "severity": "error" if tag.split("[")[0] in STRICT_TAGS else "warn",
        }

    # 構造が深く「見本を読む」ことが必須のコンポーネント（CHEATSHEET の鉄則から抽出）
    cheat = read(KIT / "CHEATSHEET.md")
    m = re.search(r"構造が深い\d*種?[（(]([^）)]+)[)）]", cheat)
    requires_sample = []
    if m:
        for name in re.split(r"\s*/\s*", m.group(1)):
            name = name.strip()
            cand = f"mi-{name}"
            if cand in components:
                requires_sample.append(cand)
            elif name == "layout":
                requires_sample.append("mi-layout")
    requires_sample = sorted(set(requires_sample))

    # クラス → ルールを書いた md（components/*.md）
    docs = defaultdict(set)
    for md in sorted((DS / "components").rglob("*.md")):
        if md.name == "_TEMPLATE.md":
            continue
        text = read(md)
        rel = str(md.relative_to(DS))
        for cls in css_classes(text):
            if cls in components:
                docs[cls].add(rel)
    for cls, paths in docs.items():
        components[cls]["docs"] = sorted(paths)

    index = {
        "_readme": (
            "mockup kit の機械可読索引。tools/build-kit-index.py が CSS と "
            "見本 HTML から自動生成する（手編集しない）。"
            "components[基底クラス] に修飾子・必須の軸/属性/role/子孫・見本・md を持つ。"
            "requiredOneOf は「各グループから必ず1つ選ぶ」、compoundOnly は"
            "「単独では効かないので併用相手が必要」、tagRules は"
            "「そのタグを使うなら allowed のどれかを必ず付ける（＝自作しない）」。"
        ),
        "generatedBy": "tools/build-kit-index.py",
        "sources": ["mitsubachi-mockup.css", "mitsubachi-icons.css",
                    "mitsubachi-logos.css", "components/*.html", "templates/*.html"],
        "css": {
            "required": ["tokens.css", "mitsubachi-mockup.css"],
            "optional": {"mitsubachi-icons.css": "内蔵以外のアイコンを使うとき",
                         "mitsubachi-logos.css": "ロゴを使うとき"},
            "order": ["tokens.css", "mitsubachi-mockup.css"],
            "script": "mitsubachi-mockup.js",
        },
        "icons": {"builtin": icons_builtin, "extra": icons_extra},
        "logos": logos,
        "requiresSample": requires_sample,
        "tagRules": tag_rules,
        "components": components,
    }
    return index


def main():
    index = build()
    problems = []
    if not index["icons"]["extra"]:
        problems.append("mitsubachi-icons.css からアイコンを抽出できなかった")
    if not index["requiresSample"]:
        problems.append("CHEATSHEET から「構造が深い」コンポーネントを抽出できなかった")
    if len(index["components"]) < 50:
        problems.append(f"基底クラスが {len(index['components'])} 件しか無い（抽出漏れの疑い）")
    if problems:
        for p in problems:
            print(f"✗ {p}", file=sys.stderr)
        return 1

    OUT.write_text(json.dumps(index, ensure_ascii=False, indent=2,
                              sort_keys=False) + "\n", encoding="utf-8")
    c = index["components"]
    print(f"✓ {OUT.relative_to(ROOT)} を生成")
    print(f"    基底クラス {len(c)} 件 / 見本に実績があるもの "
          f"{sum(1 for v in c.values() if 'sampleCount' in v)} 件")
    print(f"    必須の軸を持つ {sum(1 for v in c.values() if 'requiredOneOf' in v)} 件 / "
          f"単独では効かない修飾子 {sum(len(v['compoundOnly']) for v in c.values() if 'compoundOnly' in v)} 件")
    print(f"    タグ規則 {len(index['tagRules'])} 件 / アイコン "
          f"内蔵{len(index['icons']['builtin'])}+追加{len(index['icons']['extra'])} 種 / "
          f"ロゴ {len(index['logos'])} 種")
    return 0


if __name__ == "__main__":
    sys.exit(main())
