#!/usr/bin/env python3
"""Figma ライブラリ公開を検知し、docs の修正箇所に当たりをつける（依存なし・標準ライブラリのみ）

    python3 tools/figma-watch.py check   [--file <fileKey>] [--json] [--github-output]
    python3 tools/figma-watch.py targets [--file <fileKey>] [--init] [--no-pages] [--dry-run]
    python3 tools/figma-watch.py tokens  [--apply] [--from-css <file>]
    python3 tools/figma-watch.py report  [--issue N ...]

  check   : version history を読み、state.json の基準より新しい「公開」エントリを列挙する（state は書かない。
            CI が朝夕に実行して Issue を立てる。ローカルでは /figma-sync の先頭で使う）
  targets : 公開の説明文の照合 ＋ 公開要素の差分 ＋ 保険のページ比較 から「見る md / kit クラス」を出し、
            state.json を更新する（ローカルで実行。FIGMA_TOKEN が要る）
  tokens  : mitsubachi-token の lib/mitsubachi-tokens.css と kit の tokens.css を突合する（--apply で機械反映）
  report  : targets の結果から PR 本文の骨格を出す

state.json に入るのは 版 id・公開要素の名前と更新日時・ページ名と内容ハッシュ だけ。Figma の文面は入れない。
仕組みと運用は design-system/figma-watch/README.md を参照。

終了コード: 0 成功 / 1 失敗 / 2 一部ページの取得に失敗（結果は書く）
"""

import datetime as _dt
import hashlib
import importlib.util
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DS = ROOT / "design-system"
KIT = DS / "mockup-kit"
WATCH = DS / "figma-watch"
STATE_PATH = WATCH / "state.json"
TARGETS_PATH = WATCH / "targets.local.json"  # 作業用（.gitignore 済み）
UPSTREAM_CSS = "https://raw.githubusercontent.com/uzabase/mitsubachi-token/main/lib/mitsubachi-tokens.css"
SEMANTIC_PREFIX = "--color-semantic-"

PUBLISH_LABEL_RE = re.compile(r"(公開|published)", re.I)
PUBLISH_DESC_RE = re.compile(r"(ステータス|変更内容)\s*[:：]")


def _load(name):
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), ROOT / "tools" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


fp = _load("figma-page")
fs = _load("figma-sources")


# --- state ---------------------------------------------------------------
def load_state(path=STATE_PATH):
    if not Path(path).exists():
        return None
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save_state(state, path=STATE_PATH):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def rel(p):
    p = Path(p)
    try:
        return str(p.relative_to(ROOT))
    except ValueError:
        return str(p)


def file_state(state, key):
    return (state or {}).get("files", {}).get(key)


# --- 公開エントリの判定 ---------------------------------------------------
def is_publish(v):
    return bool(PUBLISH_LABEL_RE.search(v.get("label") or "") or PUBLISH_DESC_RE.search(v.get("description") or ""))


def is_named(v):
    return bool((v.get("label") or "").strip() or (v.get("description") or "").strip())


def new_entries(versions, baseline, include_named=False):
    """基準より新しい公開エントリを古い順に返す。baseline が None なら全部。"""
    out = []
    for v in versions:
        if baseline and (v.get("id") == baseline.get("id") or (v.get("created_at") or "") <= (baseline.get("created_at") or "")):
            continue
        if is_publish(v) or (include_named and is_named(v)):
            out.append(v)
    return sorted(out, key=lambda v: v.get("created_at") or "")


def change_summary(v):
    """説明文から「変更内容：…」の 1 行目を取る。無ければ説明文の 1 行目、それも無ければ label。"""
    desc = (v.get("description") or "").strip()
    m = re.search(r"変更内容\s*[:：]\s*(.+)", desc)
    if m:
        return m.group(1).strip().splitlines()[0]
    for line in desc.splitlines():
        if line.strip():
            return line.strip()
    return (v.get("label") or "").strip()


def day(v):
    return (v.get("created_at") or "")[:10]


def user_name(v):
    u = v.get("user") or {}
    return u.get("handle") or u.get("email") or ""


def issue_title(entries):
    latest = entries[-1]
    extra = f" ほか {len(entries) - 1} 件" if len(entries) > 1 else ""
    return f"Figma 公開: 「{change_summary(latest)}」（{day(latest)}）{extra}"


def issue_body(entries, file_key, file_name):
    lines = [f"Figma ライブラリ **{file_name or file_key}**（`{file_key}`）が公開されました。",
             "", "## 公開の説明文（バージョン履歴の原文）", ""]
    for v in entries:
        lines.append(f"### {v.get('label') or '（版名なし）'} — {day(v)} / {user_name(v)} / 版 `{v.get('id')}`")
        desc = (v.get("description") or "").strip() or "（説明文なし）"
        lines += ["> " + l for l in desc.splitlines()]
        lines.append("")
    lines += ["## 次にやること", "",
              "ローカルで Claude Code を開き `/figma-sync` を実行する（手順は `.claude/skills/figma-sync/SKILL.md`）。",
              "説明文に出てくるコンポーネント名から見る md と kit クラスに当たりをつけ、Figma を読み直して直し、",
              "`design-system/figma-watch/state.json` を更新した PR にこの Issue を `Closes` で紐づける。", ""]
    return "\n".join(lines)


def github_output(pairs, path=None):
    path = path or os.environ.get("GITHUB_OUTPUT")
    if not path:
        return
    with open(path, "a", encoding="utf-8") as f:
        for k, v in pairs.items():
            v = str(v)
            if "\n" in v:
                f.write(f"{k}<<__EOF__\n{v}\n__EOF__\n")
            else:
                f.write(f"{k}={v}\n")


# --- 公開要素 -------------------------------------------------------------
def fetch_published(client, key):
    """公開要素を {assetKey: {type, name, pageId, pageName, updated_at}} と variables のハッシュで返す。"""
    pub = {}
    for kind in ("components", "component_sets", "styles"):
        meta = client.published(key, kind).get("meta", {})
        for item in meta.get(kind, []):
            frame = item.get("containing_frame") or {}
            pub[item["key"]] = {
                "type": kind[:-1] if kind != "styles" else "style",
                "name": item.get("name", ""),
                # variant（component）は親の component set 名でまとめて扱う
                "setName": frame.get("name", "") if kind == "components" else "",
                "nodeId": item.get("node_id", ""),
                "pageId": frame.get("pageId", ""),
                "pageName": frame.get("pageName", ""),
                "updated_at": item.get("updated_at", ""),
            }
    variables_hash = None
    try:
        vmeta = client.published_variables(key).get("meta", {})
        items = sorted((vid, v.get("updatedAt", "")) for vid, v in (vmeta.get("variables") or {}).items())
        variables_hash = hashlib.sha256(json.dumps(items).encode()).hexdigest()
    except fp.FigmaError as e:
        if "403" not in str(e) and "401" not in str(e):
            raise
    return pub, variables_hash


def fetch_file_name(client, key):
    """ファイル名（Tier 3 の /meta）。取れなくても致命ではない。"""
    try:
        return (client.get(f"/files/{key}/meta").get("file") or {}).get("name", "")
    except fp.FigmaError:
        return ""


def diff_published(before, after):
    """追加 / 更新 / 削除 を [{change, key, ...}] で返す。"""
    out = []
    for k, v in after.items():
        if k not in before:
            out.append({"change": "追加", **v})
        elif v.get("updated_at") != before[k].get("updated_at") or v.get("name") != before[k].get("name"):
            out.append({"change": "更新", **v, "previousName": before[k].get("name")})
    for k, v in before.items():
        if k not in after:
            out.append({"change": "削除", **v})
    return sorted(out, key=lambda c: (c["type"], c["name"]))


# --- 当たり付け -----------------------------------------------------------
def build_targets(key, derived, entries, pub_changes, page_changes, variables_changed):
    """説明文の照合・公開要素の差分・ページ変更を 1 つの表にまとめる。"""
    rows = {}  # (kind, label) -> row

    def add(label, trigger, docs, classes, pages, note=""):
        r = rows.setdefault(label, {"label": label, "triggers": [], "docs": set(), "classes": set(), "pages": set(), "note": note})
        if trigger not in r["triggers"]:
            r["triggers"].append(trigger)
        r["docs"].update(docs)
        r["classes"].update(classes)
        r["pages"].update(pages)

    unmatched = []
    for v in entries:
        text = f"{v.get('label') or ''}\n{v.get('description') or ''}"
        hits = fs.find_terms(text, derived["dictionary"])
        if not hits:
            unmatched.append(change_summary(v))
        for h in hits:
            d = derived["dictionary"][h["term"]]
            add(h["term"], "説明文", d["docs"], d["classes"], d["nodes"])

    for c in pub_changes:
        if c["type"] == "style":
            docs = {"design-system/foundations/color.md", "design-system/foundations/typography.md",
                    "design-system/foundations/elevation.md"}
            add(f"style `{c['name']}` {c['change']}", "公開要素", docs, set(), set(), "style は foundations とトークンに影響")
            continue
        look = fs.lookup(derived, key, c["pageId"]) if c["pageId"] else {"docs": [], "classes": []}
        shown = c.get("setName") or c["name"]
        hits = fs.find_terms(shown, derived["dictionary"])
        for h in hits:
            d = derived["dictionary"][h["term"]]
            look = {"docs": sorted(set(look["docs"]) | set(d["docs"])), "classes": sorted(set(look["classes"]) | set(d["classes"]))}
        add(f"{c['type']} `{shown}` {c['change']}", "公開要素", look["docs"], look["classes"],
            {c["pageId"]} if c["pageId"] else set(), c.get("pageName", ""))
    if variables_changed:
        add("variables 更新", "公開要素", {"design-system/mockup-kit/tokens.css"}, set(), set(),
            "色の値は mitsubachi-token 経由で取り込む（tokens --apply）")

    for pc in page_changes:
        look = fs.lookup(derived, key, pc["pageId"])
        add(f"ページ {pc['pageName']}（{pc['pageId']}）", "ページ変更", look["docs"], look["classes"], {pc["pageId"]}, pc["change"])

    out = []
    for r in rows.values():
        out.append({**r, "docs": sorted(r["docs"]), "classes": sorted(r["classes"]), "pages": sorted(r["pages"]),
                    "insuranceOnly": r["triggers"] == ["ページ変更"]})
    order = {"説明文": 0, "公開要素": 1, "ページ変更": 2}
    out.sort(key=lambda r: (min(order[t] for t in r["triggers"]), r["label"]))
    return out, unmatched


# --- tokens（mitsubachi-token との突合） ----------------------------------
def parse_css_vars(text):
    """`--name: value;` を宣言順の dict で返す。Deprecated コメント付きの名前も返す。"""
    vars_, deprecated = {}, set()
    for m in re.finditer(r"^\s*(--[A-Za-z0-9-]+)\s*:\s*([^;]+);(.*)$", text, re.M):
        name, value, rest = m.group(1), m.group(2).strip(), m.group(3)
        vars_[name] = value
        if "deprecated" in rest.lower():
            deprecated.add(name)
    return vars_, deprecated


def resolve_var(name, vars_, seen=None):
    seen = seen or set()
    if name in seen or name not in vars_:
        return None
    seen.add(name)
    value = vars_[name]

    def repl(m):
        inner, fallback = m.group(1), m.group(2)
        r = resolve_var(inner, vars_, seen)
        return r if r is not None else (fallback.strip() if fallback else m.group(0))

    return re.sub(r"var\(\s*(--[A-Za-z0-9-]+)\s*(?:,\s*([^)]+))?\)", repl, value).strip()


def normalize_color(v):
    s = v.strip().lower()
    m = re.fullmatch(r"#([0-9a-f]{3,4})", s)
    if m:
        s = "#" + "".join(c * 2 for c in m.group(1))
    s = re.sub(r"\s+", "", s)
    s = re.sub(r"(\d)\.0+(?=[,)])", r"\1", s)
    return s


def fetch_upstream_css(src=None):
    if src and Path(src).exists():
        return Path(src).read_text(encoding="utf-8")
    with urllib.request.urlopen(src or UPSTREAM_CSS, timeout=30) as res:
        return res.read().decode("utf-8")


def compare_tokens(upstream_css, kit_css):
    up, deprecated = parse_css_vars(upstream_css)
    kit, _ = parse_css_vars(kit_css)
    result = {"mismatch": [], "match": 0, "unmatchedUpstream": [], "deprecated": sorted(deprecated)}
    for name in up:
        if not name.startswith(SEMANTIC_PREFIX):
            continue
        short = "--" + name[len(SEMANTIC_PREFIX):]
        resolved = resolve_var(name, up) or ""
        if short in kit:
            if normalize_color(kit[short]) == normalize_color(resolved):
                result["match"] += 1
            else:
                result["mismatch"].append({"kit": short, "upstream": name, "kitValue": kit[short], "upstreamValue": resolved})
        else:
            result["unmatchedUpstream"].append({"upstream": name, "value": resolved, "short": short})
    return result


def apply_tokens(kit_css, mismatches, today=None):
    """tokens.css の該当行の値だけを差し替える。ヘッダーの mitsubachi-token の取得日も更新する。"""
    text = kit_css
    for m in mismatches:
        pat = re.compile(r"^(\s*" + re.escape(m["kit"]) + r"\s*:\s*)([^;]+)(;)", re.M)
        text, n = pat.subn(lambda mm: mm.group(1) + m["upstreamValue"] + mm.group(3), text, count=1)
    today = today or _dt.date.today().isoformat()
    text = re.sub(r"(mitsubachi-token[^\n]*\n[^\n]*取得日 )\d{4}-\d{2}-\d{2}", lambda mm: mm.group(1) + today, text, count=1)
    return text


# --- report ---------------------------------------------------------------
def render_report(targets, meta, tokens_result, issues=()):
    entries = meta.get("entries", [])
    head = f"「{change_summary(entries[-1])}」（{day(entries[-1])} / {user_name(entries[-1])}）" if entries else "（公開エントリなし）"
    lines = [f"# Figma 公開: {head}"]
    for n in issues:
        lines.append(f"Closes #{n}")
    base = meta.get("baseline") or {}
    lines.append(f"基準: main の state.json（前回確認 {base.get('created_at', '')[:10] or '—'} の版 `{base.get('id', '—')}` まで）")
    lines += ["", "## 公開の説明文（原文）", ""]
    for v in entries:
        lines.append(f"**{v.get('label') or '（版名なし）'}** — {day(v)} / {user_name(v)}")
        lines += ["> " + l for l in ((v.get("description") or "").strip() or "（説明文なし）").splitlines()]
        lines.append("")
    main_rows = [r for r in targets if not r["insuranceOnly"]]
    ins_rows = [r for r in targets if r["insuranceOnly"]]
    lines += ["## 当たりをつけた箇所", "", "| 語 / 要素 | きっかけ | 見る md | kit クラス | Figma node |", "|---|---|---|---|---|"]
    for r in main_rows:
        lines.append(f"| {r['label']} | {' / '.join(r['triggers'])} | {'<br>'.join(r['docs']) or '—'} | "
                     f"{' '.join('.' + c for c in r['classes']) or '—'} | {', '.join(r['pages']) or '—'} |")
    if not main_rows:
        lines.append("| （無し） | | | | |")
    if meta.get("unmatched"):
        lines += ["", "当たり無しの説明文（読んで判断）: " + " / ".join(f"「{u}」" for u in meta["unmatched"])]
    lines += ["", "## 説明文に無い変更（保険のページ比較で見つかったもの）", ""]
    if meta.get("pagesSkipped"):
        lines.append("（保険のページ比較は実行していない: " + meta["pagesSkipped"] + "）")
    elif ins_rows:
        lines += ["| Figma ページ | 見る md | kit クラス |", "|---|---|---|"]
        for r in ins_rows:
            lines.append(f"| {r['label']} | {'<br>'.join(r['docs']) or '—'} | {' '.join('.' + c for c in r['classes']) or '—'} |")
    else:
        lines.append("（無し）")
    if meta.get("fetchErrors"):
        lines.append("\n取得できなかったページ: " + ", ".join(f"{e['pageId']}（{e['error']}）" for e in meta["fetchErrors"]))
    lines += ["", "## 公開された要素（LIBRARY_PUBLISH 相当）", ""]
    if meta.get("publishedChanges"):
        lines += ["| 種別 | 名前 | 変化 | ページ |", "|---|---|---|---|"]
        grouped = {}
        for c in meta["publishedChanges"]:
            k = (c["type"], c.get("setName") or c["name"], c["change"], c.get("pageName", "") or "—")
            grouped[k] = grouped.get(k, 0) + 1
        for (t, n, ch, pg), cnt in grouped.items():
            extra = f"（variant {cnt} 件）" if t == "component" and cnt > 1 else ""
            lines.append(f"| {t} | {n}{extra} | {ch} | {pg} |")
    else:
        lines.append("（差分なし）")
    if meta.get("variablesChanged"):
        lines.append("\nvariables にも更新あり（mitsubachi-token 経由で取り込む）")
    lines += ["", "## mitsubachi-token（lib/mitsubachi-tokens.css）", ""]
    if tokens_result:
        if tokens_result["mismatch"]:
            lines += ["| kit 変数 | tokens.css の値 | mitsubachi-token の値 |", "|---|---|---|"]
            for m in tokens_result["mismatch"]:
                lines.append(f"| `{m['kit']}` | `{m['kitValue']}` | `{m['upstreamValue']}` |")
        else:
            lines.append(f"一致 {tokens_result['match']} 件、値のズレなし")
        if tokens_result["unmatchedUpstream"]:
            lines.append("\nkit に同名が無い semantic: " + ", ".join(f"`{u['short']}`" for u in tokens_result["unmatchedUpstream"]))
        if tokens_result["deprecated"]:
            lines.append("\nDeprecated: " + ", ".join(f"`{d}`" for d in tokens_result["deprecated"]))
    else:
        lines.append("（未確認）")
    lines += ["", "## 直した内容", "", "（ここに書く）", "", "## 対応しなかったもの・判断に迷った点", "", "（ここに書く）", ""]
    return "\n".join(lines)


# --- コマンド -------------------------------------------------------------
def _file_key(args, derived=None):
    if args.file:
        return args.file
    derived = derived or fs.derive()
    if not derived["defaultFile"]:
        raise SystemExit("監視対象の fileKey を導出できません。--file で指定してください")
    return derived["defaultFile"]


def cmd_check(args):
    key = _file_key(args)
    state = load_state(args.state)
    fstate = file_state(state, key) or {}
    baseline = fstate.get("lastSeenVersion")
    try:
        client = fp.FigmaClient(interval=args.interval)
        versions = client.versions(key).get("versions", [])
    except fp.FigmaError as e:
        print(f"エラー: {e}", file=sys.stderr)
        return 1
    entries = new_entries(versions, baseline, args.include_named_versions)
    published = bool(entries and baseline)
    name = fstate.get("name") or key
    result = {"fileKey": key, "fileName": name, "baseline": baseline, "published": published,
              "entries": entries, "latestPublish": next((v for v in versions if is_publish(v)), None)}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif not baseline:
        print(f"基準なし（state.json に {key} の lastSeenVersion が無い）。"
              f"ローカルで `python3 tools/figma-watch.py targets --init` を実行して基準を作ってください。")
        for v in [v for v in versions if is_publish(v)][:5]:
            print(f"  公開: {day(v)} {v.get('label')} — {change_summary(v)}")
    elif entries:
        print(f"公開あり: {len(entries)} 件（{key}）")
        for v in entries:
            print(f"  {day(v)} {v.get('label')} / {user_name(v)} — {change_summary(v)}")
    else:
        print(f"公開なし（基準 {baseline.get('created_at', '')[:10]} の版 {baseline.get('id')} 以降）")
    if args.github_output or args.issue_body_file:
        body = issue_body(entries, key, name) if entries else ""
        if args.issue_body_file:
            Path(args.issue_body_file).write_text(body, encoding="utf-8")
        github_output({
            "published": "true" if published else "false",
            "count": len(entries),
            "latest_version_id": entries[-1].get("id") if entries else "",
            "issue_title": issue_title(entries) if entries else "",
            "search_key": entries[-1].get("id") if entries else "",
        })
    return 0


def cmd_targets(args):
    derived_all = fs.derive()
    key = _file_key(args, derived_all)
    derived = fs.derive(key)
    state = load_state(args.state) or {"files": {}}
    fstate = state["files"].get(key, {})
    baseline = fstate.get("lastSeenVersion")
    if not baseline and not args.init:
        print("基準がありません。初回は `targets --init` で基準を作ってください", file=sys.stderr)
        return 1
    try:
        client = fp.FigmaClient(interval=args.interval)
        versions = client.versions(key).get("versions", [])
        entries = [] if args.init else new_entries(versions, baseline, args.include_named_versions)
        pub, variables_hash = fetch_published(client, key)
    except fp.FigmaError as e:
        print(f"エラー: {e}", file=sys.stderr)
        return 1
    pub_changes = [] if args.init else diff_published(fstate.get("published", {}), pub)
    variables_changed = (not args.init) and fstate.get("variablesHash") not in (None, variables_hash)

    pages_state = dict(fstate.get("pages", {}))
    page_changes, fetch_errors, pages_skipped = [], [], ""
    watched = derived["files"].get(key, {}).get("pages", {})
    if args.no_pages:
        pages_skipped = "--no-pages"
    else:
        for nid in watched:
            try:
                norm = fp.normalize(fp.fetch_node(client, key, nid))
            except fp.FigmaError as e:
                fetch_errors.append({"pageId": nid, "error": str(e)[:80]})
                continue
            h = fp.content_hash(norm)
            prev = pages_state.get(nid)
            if not args.init and prev and prev.get("hash") != h:
                page_changes.append({"pageId": nid, "pageName": norm["pageName"], "change": "内容が変わった"})
            elif not args.init and not prev:
                page_changes.append({"pageId": nid, "pageName": norm["pageName"], "change": "初めて確認したページ"})
            pages_state[nid] = {"name": norm["pageName"], "hash": h}
        for nid in list(pages_state):
            if nid not in watched:
                del pages_state[nid]

    targets, unmatched = build_targets(key, derived, entries, pub_changes, page_changes, variables_changed)
    newest_publish = next((v for v in versions if is_publish(v)), None) or (versions[0] if versions else None)
    new_baseline = ({"id": newest_publish.get("id"), "created_at": newest_publish.get("created_at")}
                    if (args.init or entries) and newest_publish else baseline)
    file_name = fstate.get("name") or fetch_file_name(client, key) or key
    meta = {"fileKey": key, "fileName": file_name, "baseline": baseline, "newBaseline": new_baseline, "entries": entries,
            "unmatched": unmatched, "publishedChanges": pub_changes, "variablesChanged": variables_changed,
            "pageChanges": page_changes, "fetchErrors": fetch_errors, "pagesSkipped": pages_skipped, "init": args.init}
    TARGETS_PATH.parent.mkdir(parents=True, exist_ok=True)
    TARGETS_PATH.write_text(json.dumps({"meta": meta, "targets": targets}, ensure_ascii=False, indent=2), encoding="utf-8")

    if not args.dry_run:
        state["files"][key] = {
            "name": file_name,
            "lastSeenVersion": new_baseline,
            "published": pub,
            "variablesHash": variables_hash,
            "pages": pages_state,
        }
        save_state(state, args.state)

    if args.init:
        print(f"基準を作成: 版 {new_baseline and new_baseline.get('id')} / 公開要素 {len(pub)} 件 / ページ {len(pages_state)} 件"
              f"（取得失敗 {len(fetch_errors)}）→ {rel(args.state)}")
    else:
        print(f"公開エントリ {len(entries)} 件 / 公開要素の差分 {len(pub_changes)} 件 / ページ変更 {len(page_changes)} 件"
              f" / 取得失敗 {len(fetch_errors)} → {rel(TARGETS_PATH)}")
        for r in targets:
            print(f"  [{' / '.join(r['triggers'])}] {r['label']}: {', '.join(r['docs']) or '—'} {' '.join('.' + c for c in r['classes'])}")
        if unmatched:
            print("  当たり無し: " + " / ".join(unmatched))
    print(f"API 呼び出し {client.calls} 回")
    return 2 if fetch_errors else 0


def cmd_tokens(args):
    kit_path = KIT / "tokens.css"
    try:
        upstream = fetch_upstream_css(args.from_css)
    except OSError as e:
        print(f"エラー: mitsubachi-token の CSS を取得できません: {e}", file=sys.stderr)
        return 1
    kit_css = kit_path.read_text(encoding="utf-8")
    res = compare_tokens(upstream, kit_css)
    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        print(f"semantic 突合: 一致 {res['match']} / 値のズレ {len(res['mismatch'])} / kit に無い {len(res['unmatchedUpstream'])}")
        for m in res["mismatch"]:
            print(f"  {m['kit']}: {m['kitValue']} → {m['upstreamValue']}")
        if res["unmatchedUpstream"]:
            print("  kit に無い: " + ", ".join(u["short"] for u in res["unmatchedUpstream"]))
        if res["deprecated"]:
            print("  Deprecated: " + ", ".join(res["deprecated"]))
    if args.apply and res["mismatch"]:
        kit_path.write_text(apply_tokens(kit_css, res["mismatch"]), encoding="utf-8")
        print(f"tokens.css の {len(res['mismatch'])} 行を更新しました")
    return 0


def cmd_report(args):
    if not TARGETS_PATH.exists():
        print("targets の結果がありません。先に `targets` を実行してください", file=sys.stderr)
        return 1
    data = json.loads(TARGETS_PATH.read_text(encoding="utf-8"))
    tokens_result = None
    try:
        tokens_result = compare_tokens(fetch_upstream_css(args.from_css), (KIT / "tokens.css").read_text(encoding="utf-8"))
    except OSError:
        pass
    sys.stdout.write(render_report(data["targets"], data["meta"], tokens_result, args.issue or []))
    return 0


def main(argv=None):
    import argparse

    ap = argparse.ArgumentParser(description="Figma ライブラリ公開の検知と当たり付け")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(p):
        p.add_argument("--file", help="fileKey（省略時は md が最も多く参照するファイル）")
        p.add_argument("--state", default=str(STATE_PATH))
        p.add_argument("--interval", type=float, default=2.0, help="API 呼び出し間隔（秒）")
        p.add_argument("--include-named-versions", action="store_true", help="手動の名前付き版も公開とみなす")

    p = sub.add_parser("check"); common(p)
    p.add_argument("--json", action="store_true")
    p.add_argument("--github-output", action="store_true")
    p.add_argument("--issue-body-file")
    p = sub.add_parser("targets"); common(p)
    p.add_argument("--init", action="store_true", help="差分を出さず基準だけ作る")
    p.add_argument("--no-pages", action="store_true", help="保険のページ比較を省く")
    p.add_argument("--dry-run", action="store_true", help="state.json を更新しない")
    p = sub.add_parser("tokens")
    p.add_argument("--apply", action="store_true")
    p.add_argument("--from-css", help="mitsubachi-tokens.css のローカルファイル（オフライン）")
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("report")
    p.add_argument("--issue", type=int, action="append", help="Closes に書く Issue 番号（複数可）")
    p.add_argument("--from-css")
    args = ap.parse_args(argv)
    return {"check": cmd_check, "targets": cmd_targets, "tokens": cmd_tokens, "report": cmd_report}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
