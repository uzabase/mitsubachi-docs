#!/usr/bin/env python3
"""mockup kit のリポジトリ整合性チェック（依存なし・標準ライブラリのみ）

    python3 tools/check-kit.py

kit を編集したあとに実行する保守用ツール。モック生成では使わない。
検査ルールは全て「実ファイルから導出」する（固定リストを持たない）ため、
kit が変わってもこのスクリプトの更新は原則不要。

終了コード: 問題なし=0 / 1件以上の指摘=1
"""

import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DS = ROOT / "design-system"
KIT = DS / "mockup-kit"
# 導線が書かれている文書（ここから kit の各ファイルへ辿れる必要がある）
ENTRY_DOCS = [
    ROOT / "README.md",
    ROOT / "AGENTS.md",
    ROOT / "CLAUDE.md",
    DS / "AGENTS.md",
    DS / "component-selection.md",
    KIT / "README.md",
    KIT / "CHEATSHEET.md",
]

problems = []


def report(check, ok_msg, issues):
    """1チェック分の結果を出力。成功時は1行、失敗時のみ詳細を出す。"""
    if issues:
        print(f"✗ {check}: {len(issues)} 件")
        for i in issues:
            print(f"    {i}")
        problems.extend(issues)
    else:
        print(f"✓ {check}: {ok_msg}")


def read(p):
    return p.read_text(encoding="utf-8")


def css_classes(text):
    """CSS 定義側の .mi-* クラス名を集合で返す。"""
    return set(re.findall(r"\.(mi-[\w-]+)", text))


# --- 1) リンク切れ: 入口文書が参照するファイルが実在するか -------------------
def check_broken_links():
    issues = []
    for doc in ENTRY_DOCS:
        if not doc.exists():
            issues.append(f"{doc.relative_to(ROOT)} 自体が存在しない")
            continue
        text = read(doc)
        # markdown リンクと、バッククォート内のパス表記
        refs = set(re.findall(r"\]\(\./([^)#]+)\)", text))
        refs |= {r for r in re.findall(r"`([\w./-]+\.(?:html|css|md))`", text)}
        for ref in refs:
            ref = ref.strip("./")
            if "*" in ref or "<" in ref:  # ワイルドカード表記は対象外
                continue
            # doc からの相対 / design-system 起点 / kit 起点 / リポジトリ起点 で解決。
            # 表組みなどでファイル名だけを書く箇所があるため、最後に basename でも探す
            cands = [doc.parent / ref, DS / ref, KIT / ref, ROOT / ref]
            found = any(c.exists() for c in cands) or any(DS.rglob(Path(ref).name))
            if not found:
                issues.append(f"{doc.relative_to(ROOT)} → {ref}（参照先が無い）")
    report("リンク切れ", f"入口文書 {len(ENTRY_DOCS)} 件の参照は全て実在", issues)


# --- 2) 孤児ファイル: kit の各ファイルに入口文書からの言及があるか -----------
def check_orphan_files():
    joined = " ".join(read(d) for d in ENTRY_DOCS if d.exists())
    issues = []
    for f in sorted(KIT.rglob("*")):
        if not f.is_file() or f.suffix not in (".html", ".css", ".md"):
            continue
        rel = f.relative_to(KIT)
        if f.name not in joined and str(rel) not in joined:
            issues.append(f"{f.relative_to(ROOT)}（どの入口文書からも辿れない）")
    report("孤児ファイル", "kit の全ファイルに導線あり", issues)


# --- 3) md 導線漏れ: components の各 md に kit 導線があるか -------------------
def check_md_coverage():
    # _TEMPLATE.md も対象にする（新規 md は必ずここから作られるため、
    # テンプレに導線の枠が無いと追加した md から導線が抜ける）
    mds = list((DS / "components").rglob("*.md"))
    issues = [
        f"{p.relative_to(ROOT)}（kit 導線の行が無い）"
        for p in mds
        if "mockup" not in read(p)
    ]
    report("md 導線", f"components の {len(mds)} md すべてに導線あり", issues)


# --- 3-2) md のクラス名: md に手書きされた .mi-* が CSS に実在するか -----------
def check_md_class_names():
    """クラス名は各 md の導線・CHEATSHEET・component-selection.md に手書きで散在する。
    CSS 側で rename すると取り残されるため、実在を照合する。"""
    defined = set()
    for css in KIT.glob("*.css"):
        defined |= css_classes(read(css))
    issues, checked = [], 0
    for md in sorted(DS.rglob("*.md")):
        if md.name == "_TEMPLATE.md":  # {クラス名} 等のプレースホルダを含む
            continue
        used = set()
        for cls in re.findall(r"\.(mi-[\w-]+)", read(md)):
            # 末尾が - のものはワイルドカード表記（.mi-banner--* / .mi-icon--<名前>）
            if not cls.endswith("-"):
                used.add(cls)
        checked += len(used)
        for cls in sorted(used - defined):
            issues.append(f"{md.relative_to(ROOT)} → .{cls}（CSS に定義が無い）")
    report("md のクラス名", f"md に書かれた {checked} 件のクラス参照は全て CSS に実在", issues)


# --- 4) 見本の陳腐化: 見本/テンプレが使うクラスが CSS に実在するか -----------
def check_undefined_classes():
    defined = set()
    for css in KIT.glob("*.css"):
        defined |= css_classes(read(css))
    issues = []
    for html in sorted(list((KIT / "components").glob("*.html")) + list((KIT / "templates").glob("*.html"))):
        used = set()
        for attr in re.findall(r'class="([^"]+)"', read(html)):
            used |= {c for c in attr.split() if c.startswith("mi-")}
        for cls in sorted(used - defined):
            issues.append(f"{html.relative_to(ROOT)} → .{cls}（CSS に定義が無い）")
    report("見本の陳腐化", "見本・テンプレの .mi-* は全て CSS に実在", issues)


# --- 5) 併用必須クラスの文書化: 複合セレクタ専用の修飾子が明文化されているか -
def check_compound_only_documented():
    """.mi-x--a.mi-x--b の形でしか定義されない修飾子（単独では効かない）を CSS から
    抽出し、CHEATSHEET に言及があるか照合する。固定リストは持たない。"""
    css = read(KIT / "mitsubachi-mockup.css")
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    compound, standalone = set(), set()
    for sel in re.findall(r"([^{}]+)\{", css):
        for part in (p.strip() for p in sel.split(",")):
            has_pseudo = bool(re.search(r":(hover|active|focus|disabled|checked)", part))
            base = re.sub(r"::?[a-z-]+(\([^)]*\))?", "", part)
            for chain in re.findall(r"((?:\.mi-[\w-]+){2,})(?=\s|$|>|\[)", base):
                mods = [c for c in re.findall(r"\.mi-[\w-]+", chain) if "--" in c]
                if len(mods) >= 2:
                    compound.add(mods[-1])
            m = re.match(r"^(\.mi-[\w-]+--[\w-]+)(\s|$|\[|>)", base.strip())
            if m and not has_pseudo:
                standalone.add(m.group(1))
    only_compound = sorted(c.lstrip(".") for c in compound - standalone)
    cheatsheet = read(KIT / "CHEATSHEET.md")
    issues = [
        f".{c}（単独では効かないクラス。CHEATSHEET に記載が無い）"
        for c in only_compound
        if c not in cheatsheet and c.split("--")[-1] not in cheatsheet
    ]
    report(
        "併用必須クラス",
        f"{len(only_compound)} 件（{', '.join('.' + c for c in only_compound)}）は全て CHEATSHEET に記載あり",
        issues,
    )


# --- 6) 未定義トークンの参照: var(--x, fallback) はトークンを消しても壊れない ---
def check_undefined_tokens():
    """`var(--token, フォールバック)` はトークンが未定義でもフォールバックで描画されるため、
    tokens.css からトークンを消しても壊れず、古い値が黙って生き残る（suggestion が削除済みの
    --banner-shadow を参照し続けていた実例）。参照先の実在を照合する。"""
    tokens = read(KIT / "tokens.css")
    defined = set(re.findall(r"^\s*(--[a-z0-9-]+)\s*:", tokens, re.M))
    issues, checked = [], 0
    for css in sorted(KIT.glob("*.css")):
        if css.name == "tokens.css":
            continue
        body = re.sub(r"/\*.*?\*/", "", read(css), flags=re.S)  # コメント内の例を除く
        local = set(re.findall(r"^\s*(--[a-z0-9-]+)\s*:", body, re.M))  # コンポーネント固有の可変値
        used = set(re.findall(r"var\(\s*(--[a-z0-9-]+)", body))
        checked += len(used)
        for name in sorted(used - defined - local):
            line = next((i for i, l in enumerate(body.splitlines(), 1) if f"var({name}" in l), "?")
            issues.append(f"{css.relative_to(ROOT)} L{line}: var({name}) は tokens.css に定義が無い")
    report("トークンの実在", f"CSS の {checked} 件の var(--*) 参照は全て tokens.css か同ファイルに定義あり", issues)


# --- 7) フォールバック値の陳腐化: var(--x, fallback) の fallback が tokens と食い違わないか ---
def check_fallback_values():
    """`var(--token, フォールバック)` のフォールバックは tokens.css が読まれなかったときの値。
    トークンの値を更新してもフォールバックは自動で追随しないため、古い値が残る
    （layout のヘッダー高さが tokens 60px / フォールバック 56px だった実例）。
    px 値だけを比較する（色やフォントスタックは表記揺れが多く誤検知になるため）。"""
    tokens = read(KIT / "tokens.css")
    defined = {}
    for m in re.finditer(r"^\s*(--[a-z0-9-]+)\s*:\s*([^;]+);", tokens, re.M):
        defined[m.group(1)] = m.group(2).strip()
    issues, checked = [], 0
    for css in sorted(KIT.glob("*.css")):
        if css.name == "tokens.css":
            continue
        body = re.sub(r"/\*.*?\*/", "", read(css), flags=re.S)
        for m in re.finditer(r"var\(\s*(--[a-z0-9-]+)\s*,\s*(-?[\d.]+px)\s*\)", body):
            name, fb = m.group(1), m.group(2)
            if name not in defined or not re.fullmatch(r"-?[\d.]+px", defined[name]):
                continue
            checked += 1
            if fb != defined[name]:
                line = next((i for i, l in enumerate(body.splitlines(), 1) if f"var({name}, {fb})" in l), "?")
                issues.append(f"{css.relative_to(ROOT)} L{line}: var({name}, {fb}) は tokens の {defined[name]} と違う")
    report("フォールバックの鮮度", f"px のフォールバック {checked} 件は tokens.css の値と一致", issues)


# --- 8) 索引の鮮度: kit-index.json が CSS / 見本の現状と一致しているか ---------
def check_index_freshness():
    index_path = KIT / "kit-index.json"
    issues = []
    if not index_path.exists():
        issues.append("kit-index.json が無い（python3 tools/build-kit-index.py を実行）")
    else:
        spec = importlib.util.spec_from_file_location(
            "build_kit_index", ROOT / "tools" / "build-kit-index.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        if json.loads(read(index_path)) != mod.build():
            issues.append("kit-index.json が古い"
                          "（python3 tools/build-kit-index.py で再生成する）")
    report("索引の鮮度", "kit-index.json は CSS・見本と一致", issues)


# --- 9) 見本自身のセルフチェック: 見本・テンプレが check-mockup.py を通るか -----
def check_samples_pass_selfcheck():
    files = [str(p) for p in sorted(list((KIT / "components").glob("*.html")) +
                                    list((KIT / "templates").glob("*.html")))]
    proc = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "check-mockup.py"), *files, "--json"],
        capture_output=True, text=True)
    issues = []
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError:
        issues.append(f"check-mockup.py の実行に失敗（{proc.stderr.strip()[:120]}）")
        data = {"files": []}
    for f in data["files"]:
        for fd in f["findings"]:
            if fd["severity"] == "error":
                rel = Path(f["file"]).relative_to(ROOT) if Path(f["file"]).is_absolute() else f["file"]
                issues.append(f"{rel} L{fd['line']}: {fd['message']}")
    report("見本のセルフチェック",
           f"見本・テンプレ {len(files)} 件は check-mockup.py で error 0", issues)


def main():
    print(f"mockup kit 整合性チェック（{KIT.relative_to(ROOT)}）\n")
    check_broken_links()
    check_orphan_files()
    check_md_coverage()
    check_md_class_names()
    check_undefined_classes()
    check_compound_only_documented()
    check_undefined_tokens()
    check_fallback_values()
    check_index_freshness()
    check_samples_pass_selfcheck()
    print()
    if problems:
        print(f"指摘 {len(problems)} 件。上記を修正してください。")
        return 1
    print("問題なし。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
