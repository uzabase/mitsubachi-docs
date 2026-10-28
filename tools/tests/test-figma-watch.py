#!/usr/bin/env python3
"""figma-sources / figma-page / figma-watch の unittest（標準ライブラリのみ）

    python3 tools/tests/test-figma-watch.py

REST の応答を模した fixtures/figma/*.json を使い、ネットワーク無しで動く。
"""

import contextlib
import copy
import importlib.util
import io
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIX = Path(__file__).resolve().parent / "fixtures" / "figma"


def load(name):
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), ROOT / "tools" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


fw = load("figma-watch")
fs, fp = fw.fs, fw.fp  # figma-watch が読み込んだ同じモジュールを使う（例外クラスや差し替えを共有するため）
BASE = "kHQNLM1dnk0EhZwOKBEBkL"


def fixture(name):
    return json.loads((FIX / name).read_text(encoding="utf-8"))


class FakeClient:
    """FigmaClient の代役。fixture を返し、呼び出しを記録する。"""

    def __init__(self, versions=None, published=None, pages=None, fail_pages=()):
        self.versions_data = versions or fixture("versions.json")
        self.published_data = published or fixture("published-after.json")
        self.pages = pages or {}
        self.fail_pages = set(fail_pages)
        self.calls = 0

    def get(self, path, params=None):
        self.calls += 1
        if path.endswith("/meta"):
            return {"file": {"name": "Base-Component-Speeda-3.1-MITSUBACHI"}}
        raise fp.FigmaError(f"unexpected {path}")

    def versions(self, key):
        self.calls += 1
        return self.versions_data

    def published(self, key, kind):
        self.calls += 1
        return {"meta": {kind: self.published_data.get(kind, [])}}

    def published_variables(self, key):
        self.calls += 1
        raise fp.FigmaError("Figma API が 403 を返しました")

    def nodes(self, key, ids, depth=None):
        self.calls += 1
        out = {}
        for nid in ids:
            if nid in self.fail_pages:
                raise fp.FigmaError("too-large:413")
            out[nid] = self.pages.get(nid)
        return {"nodes": out}


class SourcesTest(unittest.TestCase):
    def test_derive_is_deterministic_and_finds_switch(self):
        a, b = fs.derive(BASE), fs.derive(BASE)
        self.assertEqual(json.dumps(a, sort_keys=True), json.dumps(b, sort_keys=True))
        pages = a["files"][BASE]["pages"]
        self.assertIn("9925:5880", pages)
        self.assertIn("design-system/components/switch.md", pages["9925:5880"]["docs"])
        self.assertIn("mi-switch", pages["9925:5880"]["classes"])
        self.assertEqual(a["defaultFile"], BASE)

    def test_dictionary_and_terms(self):
        d = fs.derive(BASE)["dictionary"]
        hits = fs.find_terms("ステータス：更新\n変更内容：menu-buttonをmenuへ移動", d)
        self.assertEqual([h["term"] for h in hits], ["menu-button", "menu"])
        self.assertIn("design-system/components/button/menu-button.md", d["menu-button"]["docs"])
        self.assertEqual(fs.find_terms("色味の調整のみ", d), [])

    def test_lookup_component_node_via_readme(self):
        d = fs.derive(BASE)
        look = fs.lookup(d, BASE, "9925:6684")  # kit README の component node
        self.assertEqual(look["docs"], ["design-system/components/switch.md"])
        self.assertIn("mi-switch", look["classes"])

    def test_ignore_marker(self):
        text = "<!-- figma-watch: ignore -->\n- https://www.figma.com/design/d1BQzBMWoYWBQ9Kc36aCGZ/x?node-id=1-2\n- https://www.figma.com/design/kHQNLM1dnk0EhZwOKBEBkL/x?node-id=3-4"
        self.assertEqual(fs.md_urls(text), [(BASE, "3:4")])


class PageTest(unittest.TestCase):
    def setUp(self):
        self.raw = fixture("page-switch.json")
        self.norm = fp.normalize(self.raw)

    def test_normalize_extracts_rules_and_excludes_noise(self):
        texts = [t["text"] for t in self.norm["texts"]]
        self.assertTrue(any(t.startswith("ラベルはswitchの左側に置く") for t in texts))
        self.assertFalse(any("除外" in t for t in texts))
        self.assertEqual(self.norm["pageStatus"], "✅")
        self.assertEqual(self.norm["pageNameBare"], "switch")
        cs = self.norm["componentSets"][0]
        self.assertEqual(cs["properties"]["viewport"], ["desktop", "phone"])
        self.assertEqual(cs["description"], "設定や機能のオン/オフを即時に切り替える")
        self.assertEqual([d["kind"] for d in self.norm["doDont"]], ["Do", "Don't"])
        self.assertEqual(self.norm["frames"][0]["name"], "switch-text（作らない、ルールの意に記載）")
        self.assertEqual(self.norm["excluded"]["commentNotes"], 1)
        self.assertEqual(self.norm["excluded"]["widgets"], 1)
        self.assertEqual(self.norm["excluded"]["hidden"], 1)

    def test_reading_order_is_by_position(self):
        texts = [t["text"] for t in self.norm["texts"]]
        self.assertLess(texts.index("パターン"), texts.index("checkboxとswitchの使い分け"))

    def test_hash_is_stable_and_ignores_layout_moves(self):
        h1 = fp.content_hash(self.norm)
        self.assertEqual(h1, fp.content_hash(fp.normalize(fixture("page-switch.json"))))
        moved = copy.deepcopy(self.raw)
        doc = moved["nodes"]["9925:5880"]["document"]
        for n in doc["children"][0]["children"]:
            if "absoluteBoundingBox" in n:
                n["absoluteBoundingBox"]["x"] += 3
                n["absoluteBoundingBox"]["y"] += 1
        self.assertEqual(h1, fp.content_hash(fp.normalize(moved)))
        # 付箋を増やしてもハッシュは変わらない
        noted = copy.deepcopy(self.raw)
        noted["nodes"]["9925:5880"]["document"]["children"][0]["children"].append(
            {"id": "x:1", "name": "Comment Note", "type": "WIDGET", "children": []})
        self.assertEqual(h1, fp.content_hash(fp.normalize(noted)))

    def test_hash_changes_when_rule_text_changes(self):
        edited = copy.deepcopy(self.raw)
        for n in edited["nodes"]["9925:5880"]["document"]["children"][0]["children"]:
            if n["id"] == "9954:1795":
                n["characters"] = "ラベルはswitchの右側に置く。"
        self.assertNotEqual(fp.content_hash(self.norm), fp.content_hash(fp.normalize(edited)))

    def test_markdown_mentions_sections(self):
        md = fp.to_markdown(self.norm, BASE)
        for s in ("## コンポーネント", "## ページ内のテキスト", "## Do / Don't", "## 意図が書かれた frame 名"):
            self.assertIn(s, md)

    def test_fetch_node_falls_back_to_chunks(self):
        raw_entry = self.raw["nodes"]["9925:5880"]
        shallow = {"document": {"id": "9925:5880", "name": "✅ switch", "type": "CANVAS",
                                "children": [{"id": c["id"], "name": c["name"], "type": c["type"]} for c in raw_entry["document"]["children"]]}}

        class C(FakeClient):
            def nodes(self, key, ids, depth=None):
                self.calls += 1
                if ids == ["9925:5880"] and depth is None:
                    raise fp.FigmaError("too-large:413")
                if ids == ["9925:5880"] and depth == 1:
                    return {"nodes": {"9925:5880": shallow}}
                return {"nodes": {i: {"document": next(c for c in raw_entry["document"]["children"] if c["id"] == i),
                                      "components": raw_entry["components"], "componentSets": raw_entry["componentSets"]} for i in ids}}

        entry = fp.fetch_node(C(), BASE, "9925:5880")
        self.assertTrue(entry.get("_assembled"))
        self.assertEqual(fp.content_hash(fp.normalize(entry)), fp.content_hash(self.norm))


class WatchTest(unittest.TestCase):
    def test_new_entries_detects_publish_only(self):
        versions = fixture("versions.json")["versions"]
        base = {"id": "8700", "created_at": "2026-10-10T01:00:00Z"}
        ents = fw.new_entries(versions, base)
        self.assertEqual([v["id"] for v in ents], ["8800", "9000"])  # 自動保存 9001 と手動版 8900 は除く
        self.assertEqual([v["id"] for v in fw.new_entries(versions, base, include_named=True)], ["8800", "8900", "9000"])
        self.assertEqual(fw.new_entries(versions, {"id": "9000", "created_at": "2026-10-27T03:00:00Z"}), [])
        self.assertEqual(fw.change_summary(ents[-1]), "menu-buttonをmenuへ移動")
        self.assertIn("menu-buttonをmenuへ移動", fw.issue_title(ents))
        self.assertIn("ほか 1 件", fw.issue_title(ents))
        self.assertIn("/figma-sync", fw.issue_body(ents, BASE, "Base"))

    def test_diff_published(self):
        def to_map(data):
            c = FakeClient(published=data)
            pub, _ = fw.fetch_published(c, BASE)
            return pub
        changes = fw.diff_published(to_map(fixture("published-before.json")), to_map(fixture("published-after.json")))
        kinds = {(c["change"], c["name"]) for c in changes}
        self.assertIn(("更新", "menu-button"), kinds)
        self.assertIn(("追加", "menu-category"), kinds)
        self.assertIn(("削除", "control-menu"), kinds)
        self.assertIn(("更新", "label/regular"), kinds)

    def test_build_targets_merges_triggers(self):
        derived = fs.derive(BASE)
        entries = fw.new_entries(fixture("versions.json")["versions"], {"id": "8800", "created_at": "2026-10-20T01:00:00Z"})
        c = FakeClient(published=fixture("published-before.json"))
        before, _ = fw.fetch_published(c, BASE)
        after, _ = fw.fetch_published(FakeClient(published=fixture("published-after.json")), BASE)
        pub_changes = fw.diff_published(before, after)
        page_changes = [{"pageId": "9925:5880", "pageName": "✅ switch", "change": "内容が変わった"}]
        targets, unmatched = fw.build_targets(BASE, derived, entries, pub_changes, page_changes, False)
        labels = {t["label"]: t for t in targets}
        self.assertIn("menu-button", labels)
        self.assertEqual(labels["menu-button"]["triggers"], ["説明文"])
        self.assertIn("design-system/components/button/menu-button.md", labels["menu-button"]["docs"])
        ins = [t for t in targets if t["insuranceOnly"]]
        self.assertEqual(len(ins), 1)
        self.assertIn("design-system/components/switch.md", ins[0]["docs"])
        self.assertEqual(unmatched, [])
        self.assertEqual(targets[0]["triggers"][0], "説明文")  # 説明文由来が先頭

    def test_targets_command_updates_state(self):
        import tempfile
        pages = {nid: fixture("page-switch.json")["nodes"]["9925:5880"] for nid in fs.derive(BASE)["files"][BASE]["pages"]}
        fake = FakeClient(pages=pages)
        with tempfile.TemporaryDirectory() as tmp:
            state_path = Path(tmp) / "state.json"
            orig_client, orig_targets = fp.FigmaClient, fw.TARGETS_PATH
            fp.FigmaClient = lambda **kw: fake
            fw.TARGETS_PATH = Path(tmp) / "targets.json"
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    rc = fw.main(["targets", "--file", BASE, "--state", str(state_path), "--init"])
                self.assertEqual(rc, 0)
                st = json.loads(state_path.read_text())
                f = st["files"][BASE]
                self.assertEqual(f["lastSeenVersion"]["id"], "9000")
                self.assertEqual(f["name"], "Base-Component-Speeda-3.1-MITSUBACHI")
                self.assertIn("9925:5880", f["pages"])
                self.assertNotIn("ラベルはswitch", json.dumps(st, ensure_ascii=False))  # 文面は state に入らない
                # 2 回目: 公開が無いので差分なし
                fake.versions_data = fixture("versions.json")
                with contextlib.redirect_stdout(io.StringIO()):
                    rc = fw.main(["targets", "--file", BASE, "--state", str(state_path)])
                self.assertEqual(rc, 0)
                data = json.loads(fw.TARGETS_PATH.read_text())
                self.assertEqual(data["meta"]["entries"], [])
                self.assertEqual(data["targets"], [])
                # 3 回目: 新しい公開 ＋ switch の文面変更 ＋ 1 ページ取得失敗
                newv = copy.deepcopy(fixture("versions.json"))
                newv["versions"].insert(0, {"id": "9100", "created_at": "2026-10-28T01:00:00Z", "label": "コンポーネント公開",
                                             "description": "ステータス：更新\n変更内容：table のソート仕様を追記", "user": {"handle": "A"}})
                fake.versions_data = newv
                edited = copy.deepcopy(fixture("page-switch.json"))["nodes"]["9925:5880"]
                for n in edited["document"]["children"][0]["children"]:
                    if n["id"] == "9954:1795":
                        n["characters"] = "ラベルはswitchの右側に置く。"
                fake.pages["9925:5880"] = edited
                fake.fail_pages = {"6055:16930"}
                with contextlib.redirect_stdout(io.StringIO()):
                    rc = fw.main(["targets", "--file", BASE, "--state", str(state_path)])
                self.assertEqual(rc, 2)
                data = json.loads(fw.TARGETS_PATH.read_text())
                labels = {t["label"]: t for t in data["targets"]}
                self.assertIn("table", labels)
                self.assertTrue(any(t["insuranceOnly"] and "switch" in t["label"] for t in data["targets"]))
                self.assertEqual(data["meta"]["fetchErrors"][0]["pageId"], "6055:16930")
                st = json.loads(state_path.read_text())
                self.assertEqual(st["files"][BASE]["lastSeenVersion"]["id"], "9100")
                report = fw.render_report(data["targets"], data["meta"], None, [12])
                self.assertIn("Closes #12", report)
                self.assertIn("table のソート仕様を追記", report)
                self.assertIn("説明文に無い変更", report)
            finally:
                fp.FigmaClient, fw.TARGETS_PATH = orig_client, orig_targets

    def test_check_command_outputs(self):
        import tempfile
        fake = FakeClient()
        with tempfile.TemporaryDirectory() as tmp:
            state_path = Path(tmp) / "state.json"
            fw.save_state({"files": {BASE: {"name": "Base", "lastSeenVersion": {"id": "8700", "created_at": "2026-10-10T01:00:00Z"}}}}, state_path)
            out_path = Path(tmp) / "out.txt"
            body_path = Path(tmp) / "body.md"
            orig = fp.FigmaClient
            fp.FigmaClient = lambda **kw: fake
            try:
                import os
                os.environ["GITHUB_OUTPUT"] = str(out_path)
                with contextlib.redirect_stdout(io.StringIO()):
                    rc = fw.main(["check", "--file", BASE, "--state", str(state_path), "--github-output", "--issue-body-file", str(body_path)])
            finally:
                fp.FigmaClient = orig
                os.environ.pop("GITHUB_OUTPUT", None)
            self.assertEqual(rc, 0)
            out = out_path.read_text()
            self.assertIn("published=true", out)
            self.assertIn("count=2", out)
            self.assertIn("latest_version_id=9000", out)
            self.assertIn("menu-buttonをmenuへ移動", body_path.read_text())
            # 基準が無いときは published=false
            fw.save_state({"files": {}}, state_path)
            fp.FigmaClient = lambda **kw: fake
            try:
                os.environ["GITHUB_OUTPUT"] = str(out_path)
                out_path.write_text("")
                with contextlib.redirect_stdout(io.StringIO()):
                    fw.main(["check", "--file", BASE, "--state", str(state_path), "--github-output"])
            finally:
                fp.FigmaClient = orig
                os.environ.pop("GITHUB_OUTPUT", None)
            self.assertIn("published=false", out_path.read_text())


class TokensTest(unittest.TestCase):
    def test_compare_and_apply(self):
        up = (FIX / "upstream-tokens.css").read_text()
        kit = ":root {\n  --surface-strong-default: #282828;\n  --surface-regular-default: #ffffff;\n  --surface-semi-strong-disabled: rgba(0, 0, 0, 0.07);\n  --text-regular: #222222;\n  --my-own: 4px;\n}\n"
        res = fw.compare_tokens(up, kit)
        self.assertEqual(res["match"], 3)
        self.assertEqual([m["kit"] for m in res["mismatch"]], ["--text-regular"])
        self.assertEqual(res["mismatch"][0]["upstreamValue"], "#111111")
        self.assertEqual([u["short"] for u in res["unmatchedUpstream"]], ["--object-link", "--text-old"])
        self.assertEqual(res["deprecated"], ["--color-semantic-text-old"])
        applied = fw.apply_tokens(kit, res["mismatch"], today="2026-10-28")
        self.assertIn("--text-regular: #111111;", applied)
        self.assertIn("--surface-strong-default: #282828;", applied)

    def test_apply_updates_header_date(self):
        kit = "/* 1. mitsubachi-token（公式トークン）: lib/mitsubachi-tokens.css\n *   （Generated 2026-05-25 / 取得日 2026-06-11）— semantic カラーの正 */\n:root {\n  --text-regular: #222222;\n}\n"
        applied = fw.apply_tokens(kit, [{"kit": "--text-regular", "upstreamValue": "#111111"}], today="2026-10-28")
        self.assertIn("取得日 2026-10-28", applied)


if __name__ == "__main__":
    unittest.main(verbosity=1)
