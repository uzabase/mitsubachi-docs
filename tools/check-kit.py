#!/usr/bin/env python3
"""mockup kit のリポジトリ整合性チェック（依存なし・標準ライブラリのみ）

    python3 tools/check-kit.py

kit を編集したあとに実行する保守用ツール。モック生成では使わない。
検査ルールは全て「実ファイルから導出」する（固定リストを持たない）ため、
kit が変わってもこのスクリプトの更新は原則不要。

終了コード: 問題なし=0 / 1件以上の指摘=1
"""

import re
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
    mds = [p for p in (DS / "components").rglob("*.md") if p.name != "_TEMPLATE.md"]
    issues = [
        f"{p.relative_to(ROOT)}（kit 導線の行が無い）"
        for p in mds
        if "mockup" not in read(p)
    ]
    report("md 導線", f"components の {len(mds)} md すべてに導線あり", issues)


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


def main():
    print(f"mockup kit 整合性チェック（{KIT.relative_to(ROOT)}）\n")
    check_broken_links()
    check_orphan_files()
    check_md_coverage()
    check_undefined_classes()
    check_compound_only_documented()
    print()
    if problems:
        print(f"指摘 {len(problems)} 件。上記を修正してください。")
        return 1
    print("問題なし。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
