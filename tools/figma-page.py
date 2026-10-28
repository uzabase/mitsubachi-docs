#!/usr/bin/env python3
"""Figma の 1 ページ（node）を REST で読み、docs に関わる部分だけを標準出力に出す
（依存なし・標準ライブラリのみ。ファイルには書かない）

    FIGMA_TOKEN=... python3 tools/figma-page.py <fileKey> <nodeId>          # 人/Claude 向け md
    FIGMA_TOKEN=... python3 tools/figma-page.py <fileKey> <nodeId> --json   # 機械向け（ハッシュ元）
    python3 tools/figma-page.py --from-raw <REST 応答の JSON>                # オフライン（fixture）

出すもの: ページ名と状態絵文字 / component set の variant 軸と値・説明文 / ページ内に点在する
テキスト（読み順・frame パス付き）/ do-dont マーカー / 意図が名前に書かれた frame。
出さないもの: 座標・色・寸法（値は Figma MCP で取る）、非表示ノード、Comment Note（作業者メモ）、
コンポーネント内部やインスタンス内部のテキスト、Figma Specs。

tools/figma-watch.py がこのファイルを import して FigmaClient と normalize() を使う。
終了コード: 0 成功 / 1 失敗
"""

import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

API = "https://api.figma.com/v1"
CONTAINER_TYPES = {"CANVAS", "FRAME", "GROUP", "SECTION", "DOCUMENT"}
INTENT_WORDS = ("作らない", "非推奨", "削除予定", "廃止", "検討中", "仕様", "ルール", "Do", "Don't", "（", "(")
MAX_FRAME_DEPTH = 3


class FigmaError(RuntimeError):
    pass


class FigmaClient:
    """REST の薄いクライアント。呼び出し間隔・429・5xx の再試行を担う。"""

    def __init__(self, token=None, interval=2.0, timeout=60, max_retry=5, sleep=time.sleep):
        self.token = token or os.environ.get("FIGMA_TOKEN")
        if not self.token:
            raise FigmaError("FIGMA_TOKEN が未設定です（Figma の設定 → セキュリティ → Personal access tokens で発行）")
        self.interval = interval
        self.timeout = timeout
        self.max_retry = max_retry
        self.sleep = sleep
        self._last = 0.0
        self.calls = 0

    def get(self, path, params=None):
        url = f"{API}{path}"
        if params:
            url += "?" + urllib.parse.urlencode(params)
        for attempt in range(self.max_retry + 1):
            wait = self.interval - (time.monotonic() - self._last)
            if wait > 0:
                self.sleep(wait)
            req = urllib.request.Request(url, headers={"X-FIGMA-TOKEN": self.token})
            try:
                self._last = time.monotonic()
                self.calls += 1
                with urllib.request.urlopen(req, timeout=self.timeout) as res:
                    return json.loads(res.read().decode("utf-8"))
            except urllib.error.HTTPError as e:
                if e.code in (401, 403):
                    raise FigmaError(
                        f"Figma API が {e.code} を返しました（{path}）。FIGMA_TOKEN の期限と"
                        "スコープ（file_content:read / file_versions:read / library_content:read / file_variables:read）"
                        "を確認し、必要なら再発行してください") from None
                if e.code == 404:
                    raise FigmaError(f"Figma API が 404 を返しました（{path}）。fileKey / nodeId を確認してください") from None
                if e.code == 429 and attempt < self.max_retry:
                    retry = e.headers.get("Retry-After")
                    self.sleep(float(retry) if retry and retry.isdigit() else 30 * (attempt + 1))
                    continue
                if e.code in (413, 400):
                    raise FigmaError(f"too-large:{e.code}")
                if e.code >= 500 and attempt < self.max_retry:
                    self.sleep(2 ** attempt)
                    continue
                raise FigmaError(f"Figma API エラー {e.code}（{path}）") from None
            except (urllib.error.URLError, TimeoutError, OSError) as e:
                if attempt < self.max_retry:
                    self.sleep(2 ** attempt)
                    continue
                raise FigmaError(f"Figma API に接続できません（{path}）: {e}") from None
        raise FigmaError(f"Figma API の再試行上限に達しました（{path}）")

    # --- エンドポイント ---------------------------------------------------
    def nodes(self, file_key, ids, depth=None):
        params = {"ids": ",".join(ids)}
        if depth is not None:
            params["depth"] = depth
        return self.get(f"/files/{file_key}/nodes", params)

    def versions(self, file_key):
        return self.get(f"/files/{file_key}/versions")

    def published(self, file_key, kind):
        """kind: components / component_sets / styles"""
        return self.get(f"/files/{file_key}/{kind}")

    def published_variables(self, file_key):
        return self.get(f"/files/{file_key}/variables/published")


def fetch_node(client, file_key, nid, chunk=5):
    """node を 1 発で取り、大きすぎて失敗したら直下の子を分割取得して合成する。
    戻り値は REST の nodes 応答の 1 エントリ相当 {"document", "components", "componentSets"}。"""
    try:
        res = client.nodes(file_key, [nid])
        entry = res["nodes"].get(nid)
        if entry is None or entry.get("document") is None:
            raise FigmaError(f"node {nid} が見つかりません")
        return entry
    except FigmaError as e:
        if not (str(e).startswith("too-large") or "接続できません" in str(e) or "再試行上限" in str(e)):
            raise
    shallow = client.nodes(file_key, [nid], depth=1)["nodes"].get(nid)
    if not shallow or not shallow.get("document"):
        raise FigmaError(f"node {nid} が見つかりません")
    doc = dict(shallow["document"])
    child_ids = [c["id"] for c in doc.get("children", [])]
    children, components, sets = [], {}, {}
    for i in range(0, len(child_ids), chunk):
        part = client.nodes(file_key, child_ids[i:i + chunk])["nodes"]
        for cid in child_ids[i:i + chunk]:
            ent = part.get(cid)
            if ent and ent.get("document"):
                children.append(ent["document"])
                components.update(ent.get("components", {}))
                sets.update(ent.get("componentSets", {}))
    doc["children"] = children
    return {"document": doc, "components": components, "componentSets": sets, "_assembled": True}


# --- 正規化 --------------------------------------------------------------
def split_status(name):
    """ページ名の先頭の状態絵文字（✅ 🚧 など）を分離する。"""
    m = re.match(r"^([^\w\s()（）\[\]\-/]+)\s*(.*)$", name)
    if m and not re.match(r"[぀-ヿ一-鿿]", m.group(1)):
        return m.group(1), m.group(2) or name
    return "", name


def _text_ok(s):
    return bool(re.search(r"[\w぀-ヿ一-鿿]", s))


def _is_comment_note(name):
    return "comment note" in name.lower() or "作業者メモ" in name


def _is_dodont(name):
    n = name.lower().replace(" ", "")
    return n.startswith("do-dont") or n.startswith("dodont") or n in ("do", "don't", "dont", "エリア指定")


def _intent_frame(name):
    return any(w in name for w in INTENT_WORDS)


def normalize(entry):
    """nodes 応答の 1 エントリ（{"document", "components", "componentSets"}）を正規化する。
    フル応答 {"nodes": {...}} を渡した場合は最初のエントリを使う。純関数。"""
    if "nodes" in entry and "document" not in entry:
        entry = next(iter(entry["nodes"].values()))
    doc = entry["document"]
    comps = entry.get("components", {}) or {}
    sets = entry.get("componentSets", {}) or {}
    status, bare = split_status(doc.get("name", ""))
    out = {
        "pageId": doc.get("id"),
        "pageName": doc.get("name", ""),
        "pageStatus": status,
        "pageNameBare": bare,
        "componentSets": [],
        "components": [],
        "texts": [],
        "doDont": [],
        "frames": [],
        "excluded": {"hidden": 0, "widgets": 0, "commentNotes": 0, "instances": 0},
    }
    texts = []

    def walk(node, path, depth):
        if node.get("visible", True) is False:
            out["excluded"]["hidden"] += 1
            return
        t = node.get("type", "")
        name = node.get("name", "")
        if t == "WIDGET" or t.startswith("SPEC"):
            out["excluded"]["widgets"] += 1
            return
        if t == "INSTANCE":
            main = comps.get(node.get("componentId", ""), {})
            mname = main.get("name", "") or name
            if _is_comment_note(mname) or _is_comment_note(name):
                out["excluded"]["commentNotes"] += 1
                return
            if _is_dodont(mname) or _is_dodont(name):
                kind = ""
                for v in (node.get("componentProperties") or {}).values():
                    val = str(v.get("value", "")).lower().replace("'", "").replace("’", "")
                    if val in ("do", "dont"):
                        kind = "Don't" if val == "dont" else "Do"
                if not kind and name.lower() != "do-dont":
                    kind = "Don't" if "don" in name.lower() else ("Do" if name.lower().startswith("do") else "")
                out["doDont"].append({"id": node.get("id"), "kind": kind, "path": path})
                return
            out["excluded"]["instances"] += 1
            return
        if t == "COMPONENT_SET":
            props, other = {}, {}
            for pname, pdef in (node.get("componentPropertyDefinitions") or {}).items():
                base = pname.split("#")[0]
                if pdef.get("type") == "VARIANT":
                    props[base] = sorted(str(v) for v in pdef.get("variantOptions", []))
                else:
                    other[base] = {"type": pdef.get("type"), "default": pdef.get("defaultValue")}
            meta = sets.get(node.get("id"), {})
            out["componentSets"].append({
                "id": node.get("id"), "name": name, "path": path,
                "description": (meta.get("description") or "").strip(),
                "properties": props, "otherProps": other,
                "variants": sorted(c.get("name", "") for c in node.get("children", [])),
            })
            return
        if t == "COMPONENT":
            meta = comps.get(node.get("id"), {})
            out["components"].append({"id": node.get("id"), "name": name, "path": path,
                                      "description": (meta.get("description") or "").strip()})
            return
        if t == "TEXT":
            chars = (node.get("characters") or "").replace(" ", "\n")
            chars = "\n".join(l.rstrip() for l in chars.splitlines()).strip()
            if _text_ok(chars):
                box = node.get("absoluteBoundingBox") or {}
                style = node.get("style") or {}
                texts.append({
                    "id": node.get("id"), "text": chars, "path": path,
                    "heading": bool(style.get("fontSize", 0) >= 20 or style.get("fontWeight", 0) >= 700),
                    "_y": round(float(box.get("y", 0)) / 8), "_x": float(box.get("x", 0)),
                })
            return
        # コンテナ
        if t in CONTAINER_TYPES or node.get("children"):
            if t != "CANVAS" and depth <= MAX_FRAME_DEPTH and _intent_frame(name):
                out["frames"].append({"id": node.get("id"), "name": name, "path": path})
            child_path = path if t == "CANVAS" else path + [name]
            for c in node.get("children", []) or []:
                walk(c, child_path, depth + 1)

    walk(doc, [], 0)
    texts.sort(key=lambda x: (x["_y"], x["_x"]))
    out["texts"] = [{k: v for k, v in x.items() if not k.startswith("_")} for x in texts]
    out["doDont"].sort(key=lambda d: (d["path"], d["id"]))
    out["frames"].sort(key=lambda f: (f["path"], f["name"]))
    out["componentSets"].sort(key=lambda s: s["name"])
    out["components"].sort(key=lambda s: s["name"])
    return out


def to_json(norm):
    return json.dumps(norm, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def content_hash(norm):
    """差分検知用のハッシュ。excluded の件数は含めない（付箋の増減で揺れないように）。"""
    body = {k: v for k, v in norm.items() if k != "excluded"}
    return hashlib.sha256(to_json(body).encode("utf-8")).hexdigest()


def to_markdown(norm, file_key=None):
    lines = [f"# {norm['pageName']}"]
    if norm["pageId"]:
        link = f"https://www.figma.com/design/{file_key}/?node-id={norm['pageId'].replace(':', '-')}" if file_key else norm["pageId"]
        lines.append(f"node: {norm['pageId']}  {link}")
    if norm["pageStatus"]:
        lines.append(f"状態: {norm['pageStatus']}")
    if norm["componentSets"] or norm["components"]:
        lines.append("\n## コンポーネント")
        for s in norm["componentSets"]:
            lines.append(f"- **{s['name']}**（component set {s['id']}、variant {len(s['variants'])} 件）")
            if s["description"]:
                lines.append(f"  - 説明: {s['description']}")
            for axis, vals in s["properties"].items():
                lines.append(f"  - {axis}: {' / '.join(vals)}")
            for pname, p in s["otherProps"].items():
                lines.append(f"  - {pname}（{p['type']}）既定 {p['default']}")
        for c in norm["components"]:
            desc = f" — {c['description']}" if c["description"] else ""
            lines.append(f"- {c['name']}（component {c['id']}）{desc}")
    if norm["texts"]:
        lines.append("\n## ページ内のテキスト（読み順）")
        cur = None
        for t in norm["texts"]:
            p = " › ".join(t["path"]) or "（直下）"
            if p != cur:
                lines.append(f"\n### {p}")
                cur = p
            prefix = "**" if t["heading"] else ""
            body = t["text"].replace("\n", "\n  ")
            lines.append(f"- {prefix}{body}{prefix}  `{t['id']}`")
    if norm["doDont"]:
        lines.append("\n## Do / Don't マーカー")
        for d in norm["doDont"]:
            lines.append(f"- {d['kind'] or '?'}: {' › '.join(d['path'])}  `{d['id']}`")
    if norm["frames"]:
        lines.append("\n## 意図が書かれた frame 名")
        for f in norm["frames"]:
            lines.append(f"- {f['name']}（{' › '.join(f['path']) or '直下'}）  `{f['id']}`")
    ex = norm["excluded"]
    lines.append(f"\n除外: 非表示 {ex['hidden']} / 付箋 {ex['commentNotes']} / widget {ex['widgets']} / インスタンス {ex['instances']}")
    return "\n".join(lines) + "\n"


def main(argv=None):
    import argparse

    ap = argparse.ArgumentParser(description="Figma の 1 ページを読んで docs 向けに整形して出す")
    ap.add_argument("file_key", nargs="?")
    ap.add_argument("node_id", nargs="?", help="9925:5880 または 9925-5880")
    ap.add_argument("--from-raw", help="REST の nodes 応答 JSON を読む（オフライン）")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--hash", action="store_true", help="内容ハッシュだけを出す")
    ap.add_argument("--interval", type=float, default=2.0)
    args = ap.parse_args(argv)

    try:
        if args.from_raw:
            with open(args.from_raw, encoding="utf-8") as f:
                entry = json.load(f)
        else:
            if not (args.file_key and args.node_id):
                ap.error("fileKey と nodeId、または --from-raw を指定してください")
            nid = args.node_id.replace("-", ":")
            entry = fetch_node(FigmaClient(interval=args.interval), args.file_key, nid)
    except FigmaError as e:
        print(f"エラー: {e}", file=sys.stderr)
        return 1
    norm = normalize(entry)
    if args.hash:
        print(content_hash(norm))
    elif args.json:
        print(json.dumps(norm, ensure_ascii=False, sort_keys=True, indent=2))
    else:
        sys.stdout.write(to_markdown(norm, args.file_key))
    return 0


if __name__ == "__main__":
    sys.exit(main())
