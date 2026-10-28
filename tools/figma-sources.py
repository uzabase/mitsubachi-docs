#!/usr/bin/env python3
"""Figma 監視の対象と逆引き表を md / kit README から導出する（依存なし・標準ライブラリのみ）

    python3 tools/figma-sources.py                 # 一覧を表で表示
    python3 tools/figma-sources.py --json          # 機械可読
    python3 tools/figma-sources.py --file <fileKey>

tools/figma-watch.py と tools/check-kit.py がこのファイルを import して使う。
固定リストは持たず、すべて実ファイルから導出する:
  - 監視する Figma node        → components/*.md・foundations/*.md の `## Figma` などに書かれた URL
  - node → 見る md             → その URL を書いている md
  - md → kit クラス            → md の kit 導線行（「mockup で再現する場合は …」）に書かれた .mi-*
  - component node → kit クラス → mockup-kit/README.md「対応コンポーネントと値の出自」表
  - 照合辞書（公開の説明文に出てくる語 → md / クラス） → md のファイル名・H1・README 表の 1 列目

終了コード: 0
"""

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DS = ROOT / "design-system"
KIT = DS / "mockup-kit"

URL_RE = re.compile(
    r"figma\.com/(?:design|file)/([A-Za-z0-9]{22,128})[^)\s`]*?node-id=(\d+)[-:](\d+)")
CLASS_RE = re.compile(r"\.(mi-[\w-]+)")
LEAD_MARK = "mockup で再現する場合は"  # kit 導線行の決まり文句（check-kit.py と同じ前提）
README_SECTION = "## 対応コンポーネントと値の出自"
IGNORE_MARK = "figma-watch: ignore"
MIN_TERM_LEN = 3  # 正規化後にこれより短い語は照合に使わない（誤爆防止）


def read(p):
    return p.read_text(encoding="utf-8")


def normalize_term(s):
    """照合用の正規化。小文字化し、区切り記号（- _ 空白）を落とす。"""
    return re.sub(r"[\s\-_　]+", "", s.strip().lower())


def node_id(a, b):
    return f"{a}:{b}"


def md_files():
    """走査対象の md。test/ と _TEMPLATE.md は除く（DUMMY URL とプレースホルダ）。"""
    for p in sorted(DS.rglob("*.md")):
        if p.name == "_TEMPLATE.md" or (DS / "test") in p.parents:
            continue
        yield p


def md_term(p):
    """md のファイル名から照合語を得る。index.md は親ディレクトリ名。"""
    return p.parent.name if p.name == "index.md" else p.stem


def md_h1(text):
    m = re.search(r"^#\s+(.+?)\s*$", text, re.M)
    return m.group(1).strip() if m else ""


def md_lead_classes(text):
    """kit 導線行（引用ブロック）に書かれた .mi-*。導線が無い md は本文全体から拾う。"""
    lines = [l for l in text.splitlines() if l.startswith(">") and LEAD_MARK in l]
    src = "\n".join(lines) if lines else text
    return sorted({c for c in CLASS_RE.findall(src) if not c.endswith("-")})


def md_urls(text):
    """(fileKey, nodeId) の列。URL と同じ行か直前行に ignore マーカーがあれば除く。"""
    out = []
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if IGNORE_MARK in line or (i > 0 and IGNORE_MARK in lines[i - 1]):
            continue
        for key, a, b in URL_RE.findall(line):
            out.append((key, node_id(a, b)))
    return out


def readme_rows():
    """kit README の出自表を行ごとに {name, classes, fileKey, nodes} で返す。"""
    path = KIT / "README.md"
    if not path.exists():
        return [], None
    text = read(path)
    start = text.find(README_SECTION)
    if start < 0:
        return [], None
    section = text[start + len(README_SECTION):]
    nxt = re.search(r"^## ", section, re.M)
    if nxt:
        section = section[: nxt.start()]
    m = re.search(r"fileKey\s*`([A-Za-z0-9]{22,128})`", section)
    default_key = m.group(1) if m else None
    rows = []
    for line in section.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3 or set(cells[0]) <= set("-: ") or cells[0] in ("コンポーネント",):
            continue
        name = re.sub(r"[*`（(].*$", "", cells[0]).strip()  # 「layout（app shell）」→ layout
        classes = sorted({c for c in CLASS_RE.findall(cells[1]) if not c.endswith("-")})
        source = cells[2]
        keys = re.findall(r"`([A-Za-z0-9]{22,128})`", source)
        nodes = [node_id(a, b) for a, b in re.findall(r"`(\d+)[-:](\d+)`", source)]
        rows.append({
            "name": name,
            "classes": classes,
            "fileKey": keys[0] if keys else default_key,
            "nodes": nodes,
        })
    return rows, default_key


def derive(file_key=None):
    """監視対象と逆引き表を導出する。

    戻り値:
      files: {fileKey: {"pages": {nodeId: {"docs": [...], "classes": [...]}},
                        "componentNodes": {nodeId: {"name": str, "classes": [...]}}}}
      dictionary: {語: {"docs": [...], "classes": [...], "nodes": [...]}}
      defaultFile: md から最も多く参照されている fileKey
    """
    files = defaultdict(lambda: {"pages": defaultdict(lambda: {"docs": set(), "classes": set()}),
                                 "componentNodes": {}})
    dictionary = defaultdict(lambda: {"docs": set(), "classes": set(), "nodes": set()})

    for p in md_files():
        text = read(p)
        rel = str(p.relative_to(ROOT))
        classes = md_lead_classes(text)
        urls = md_urls(text)
        for key, nid in urls:
            files[key]["pages"][nid]["docs"].add(rel)
            files[key]["pages"][nid]["classes"].update(classes)
        if (DS / "components") in p.parents:
            terms = {md_term(p), md_h1(text)}
            for t in terms:
                if len(normalize_term(t)) < MIN_TERM_LEN:
                    continue
                d = dictionary[t]
                d["docs"].add(rel)
                d["classes"].update(classes)
                d["nodes"].update(nid for _, nid in urls)

    rows, _ = readme_rows()
    for r in rows:
        if not r["fileKey"]:
            continue
        for nid in r["nodes"]:
            files[r["fileKey"]]["componentNodes"][nid] = {"name": r["name"], "classes": r["classes"]}
        if len(normalize_term(r["name"])) >= MIN_TERM_LEN:
            d = dictionary[r["name"]]
            d["classes"].update(r["classes"])
            d["nodes"].update(r["nodes"])

    counts = {k: len(v["pages"]) for k, v in files.items()}
    default_file = max(counts, key=counts.get) if counts else None

    def finish_files(items):
        out = {}
        for key, v in sorted(items.items()):
            if file_key and key != file_key:
                continue
            out[key] = {
                "pages": {nid: {"docs": sorted(pv["docs"]), "classes": sorted(pv["classes"])}
                          for nid, pv in sorted(v["pages"].items())},
                "componentNodes": dict(sorted(v["componentNodes"].items())),
            }
        return out

    dict_out = {t: {"docs": sorted(d["docs"]), "classes": sorted(d["classes"]), "nodes": sorted(d["nodes"])}
                for t, d in sorted(dictionary.items())}
    return {"files": finish_files(files), "dictionary": dict_out, "defaultFile": default_file}


def find_terms(text, dictionary):
    """説明文から辞書の語を探す。長い語から順に、正規化した文字列上で重ならないように拾う。
    戻り値: [{"term": 語, "start": 正規化後の位置}]（出現順）"""
    norm = normalize_term(text)
    terms = sorted(dictionary, key=lambda t: -len(normalize_term(t)))
    taken = [False] * len(norm)
    hits = []
    for t in terms:
        nt = normalize_term(t)
        if len(nt) < MIN_TERM_LEN:
            continue
        start = 0
        while True:
            i = norm.find(nt, start)
            if i < 0:
                break
            if not any(taken[i:i + len(nt)]):
                for j in range(i, i + len(nt)):
                    taken[j] = True
                hits.append({"term": t, "start": i})
            start = i + 1
    return sorted(hits, key=lambda h: h["start"])


def lookup(derived, file_key, nid):
    """node → 見る md / kit クラス。ページ node でも component node でも引ける。"""
    f = derived["files"].get(file_key, {})
    page = f.get("pages", {}).get(nid)
    comp = f.get("componentNodes", {}).get(nid)
    docs = set(page["docs"]) if page else set()
    classes = set(page["classes"]) if page else set()
    if comp:
        classes.update(comp["classes"])
        if not docs:  # component node は辞書経由で md を引く
            d = derived["dictionary"].get(comp["name"])
            if d:
                docs.update(d["docs"])
    return {"docs": sorted(docs), "classes": sorted(classes)}


def main(argv=None):
    import argparse

    ap = argparse.ArgumentParser(description="Figma 監視対象と逆引き表の導出")
    ap.add_argument("--file", help="この fileKey に絞る")
    ap.add_argument("--json", action="store_true", help="JSON で出力")
    args = ap.parse_args(argv)

    d = derive(args.file)
    if args.json:
        print(json.dumps(d, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    for key, f in d["files"].items():
        print(f"fileKey {key}{'（既定）' if key == d['defaultFile'] else ''}: "
              f"md が参照する node {len(f['pages'])} 件 / kit README の component node {len(f['componentNodes'])} 件")
        for nid, pv in f["pages"].items():
            print(f"  {nid:>14}  {', '.join(pv['docs'])}  {' '.join('.' + c for c in pv['classes'])}")
    print(f"\n照合辞書: {len(d['dictionary'])} 語")
    return 0


if __name__ == "__main__":
    sys.exit(main())
