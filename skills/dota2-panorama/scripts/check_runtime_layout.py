#!/usr/bin/env python3
import argparse
import json
import re
import sys
from pathlib import Path


def parse_args():
    p = argparse.ArgumentParser(description="Runtime checker for Panorama layout dump against design contract.")
    p.add_argument("--contract", required=True, help="Contract json from extract_drawio_contract.py")
    p.add_argument("--dump", required=True, help="Path to runtime dump json/text (supports '[LayoutDump] {...}' line)")
    p.add_argument("--map", required=True, help="Mapping json: drawio_id -> selector/property mapping")
    p.add_argument("--relation-rules", default="", help="JSON file for relation checks over mapped ids")
    p.add_argument("--required-selectors", default="", help="Comma-separated selectors that must exist in dump")
    p.add_argument("--require-visible-selectors", default="", help="Comma-separated selectors that must have rect.visible=true")
    p.add_argument("--design-width", type=float, default=1920.0, help="Design canvas width")
    p.add_argument("--design-height", type=float, default=1080.0, help="Design canvas height")
    p.add_argument("--tol", type=float, default=2.0, help="Base px tolerance in design space")
    p.add_argument("--enforce-inside-parent-mapped", action="store_true", help="Require mapped runtime rect to stay inside mapped parent rect")
    return p.parse_args()


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def report(ok, msg):
    prefix = "PASS" if ok else "FAIL"
    print(f"[{prefix}] {msg}")
    return ok


def load_dump_payload(path):
    raw = Path(path).read_text(encoding="utf-8-sig")
    raw = raw.strip()
    if raw.startswith("{"):
        return json.loads(raw)
    m = re.search(r"\{.*\}", raw, flags=re.S)
    if not m:
        raise ValueError("No JSON object found in dump file.")
    return json.loads(m.group(0))


def relation_check(pass_all, relation_rules, rects, tol):
    for r in relation_rules:
        rtype = str(r.get("type", ""))
        a = str(r.get("a", ""))
        b = str(r.get("b", ""))
        rt = float(r.get("tol", tol))
        ra = rects.get(a)
        rb = rects.get(b)
        if not ra or not rb:
            pass_all &= report(False, f"relation resolvable: {rtype} {a} {b}")
            continue
        if rtype == "center_x_equal":
            pass_all &= report(abs((ra["x"] + ra["w"] * 0.5) - (rb["x"] + rb["w"] * 0.5)) <= rt, f"relation center_x_equal: {a} {b}")
        elif rtype == "center_y_equal":
            pass_all &= report(abs((ra["y"] + ra["h"] * 0.5) - (rb["y"] + rb["h"] * 0.5)) <= rt, f"relation center_y_equal: {a} {b}")
        elif rtype == "gap_x":
            expected = float(r.get("value", 0))
            gap = rb["x"] - (ra["x"] + ra["w"])
            pass_all &= report(abs(gap - expected) <= rt, f"relation gap_x: {a}->{b}")
        elif rtype == "gap_y":
            expected = float(r.get("value", 0))
            gap = rb["y"] - (ra["y"] + ra["h"])
            pass_all &= report(abs(gap - expected) <= rt, f"relation gap_y: {a}->{b}")
        elif rtype == "width_ratio":
            expected = float(r.get("value", 1))
            ratio = (ra["w"] / rb["w"]) if rb["w"] else 0
            pass_all &= report(abs(ratio - expected) <= rt * 0.01, f"relation width_ratio: {a}/{b}")
        elif rtype == "left_equal":
            pass_all &= report(abs(ra["x"] - rb["x"]) <= rt, f"relation left_equal: {a} {b}")
        elif rtype == "right_equal":
            pass_all &= report(abs((ra["x"] + ra["w"]) - (rb["x"] + rb["w"])) <= rt, f"relation right_equal: {a} {b}")
        elif rtype == "top_equal":
            pass_all &= report(abs(ra["y"] - rb["y"]) <= rt, f"relation top_equal: {a} {b}")
        elif rtype == "bottom_equal":
            pass_all &= report(abs((ra["y"] + ra["h"]) - (rb["y"] + rb["h"])) <= rt, f"relation bottom_equal: {a} {b}")
        else:
            pass_all &= report(False, f"unknown relation type: {rtype}")
    return pass_all


def main():
    args = parse_args()
    contract = read_json(args.contract).get("contract", {})
    mapping = read_json(args.map)
    relation_rules = []
    if args.relation_rules:
        rr = read_json(args.relation_rules)
        relation_rules = rr.get("rules", rr) if isinstance(rr, dict) else rr
    dump = load_dump_payload(args.dump)

    rows = dump.get("rows", [])
    row_map = {str(r.get("selector", "")): r.get("rect") for r in rows}
    required_selectors = [s.strip() for s in args.required_selectors.split(",") if s.strip()]
    require_visible = [s.strip() for s in args.require_visible_selectors.split(",") if s.strip()]

    sx = (float(dump.get("screen_w", 0)) / args.design_width) if args.design_width else 1.0
    sy = (float(dump.get("screen_h", 0)) / args.design_height) if args.design_height else 1.0
    if sx <= 0:
        sx = 1.0
    if sy <= 0:
        sy = 1.0
    tolx = args.tol * sx
    toly = args.tol * sy

    pass_all = True
    pass_all &= report(bool(rows), "runtime rows present")
    pass_all &= report(sx > 0 and sy > 0, f"runtime scale valid: sx={sx:.4f} sy={sy:.4f}")

    for sel in required_selectors:
        pass_all &= report(sel in row_map and row_map.get(sel) is not None, f"required selector in dump: {sel}")

    for sel in require_visible:
        rect = row_map.get(sel)
        vis = bool(rect and rect.get("visible") is True)
        pass_all &= report(vis, f"selector visible at runtime: {sel}")

    # Compare local geometry against contract local geometry defined by parent_id
    runtime_local = {}
    for drawio_id, rule in mapping.items():
        sel = rule.get("selector", "")
        rect = row_map.get(sel)
        if rect is None:
            pass_all &= report(False, f"runtime rect present: {drawio_id} {sel}")
            continue
        runtime_local[drawio_id] = rect
        target = contract.get(drawio_id)
        if not target:
            pass_all &= report(True, f"helper mapping node (no contract id): {drawio_id} {sel}")
            continue

        parent_id = rule.get("parent_id", "")
        expected_x = float(target["x"])
        expected_y = float(target["y"])
        if parent_id and parent_id in contract:
            expected_x -= float(contract[parent_id]["x"])
            expected_y -= float(contract[parent_id]["y"])
        expected_w = float(target["width"])
        expected_h = float(target["height"])

        rx = float(rect.get("x", 0))
        ry = float(rect.get("y", 0))
        rw = float(rect.get("width", 0))
        rh = float(rect.get("height", 0))

        pass_all &= report(abs(rx - expected_x * sx) <= tolx, f"runtime x within tol: {drawio_id} {sel}")
        pass_all &= report(abs(ry - expected_y * sy) <= toly, f"runtime y within tol: {drawio_id} {sel}")
        pass_all &= report(abs(rw - expected_w * sx) <= tolx, f"runtime w within tol: {drawio_id} {sel}")
        pass_all &= report(abs(rh - expected_h * sy) <= toly, f"runtime h within tol: {drawio_id} {sel}")

    # Rebuild absolute runtime rects from mapping chain for relation checks
    abs_rects = {}
    unresolved = dict(mapping)
    for _ in range(len(mapping) + 2):
        progressed = False
        for drawio_id, rule in list(unresolved.items()):
            rect = runtime_local.get(drawio_id)
            if rect is None:
                unresolved.pop(drawio_id, None)
                continue
            x = float(rect.get("x", 0))
            y = float(rect.get("y", 0))
            w = float(rect.get("width", 0))
            h = float(rect.get("height", 0))
            parent_id = rule.get("parent_id", "")
            if parent_id:
                if parent_id not in abs_rects:
                    continue
                x += abs_rects[parent_id]["x"]
                y += abs_rects[parent_id]["y"]
            abs_rects[drawio_id] = {"x": x, "y": y, "w": w, "h": h}
            unresolved.pop(drawio_id, None)
            progressed = True
        if not unresolved or not progressed:
            break

    if relation_rules:
        # scale relation numeric value to runtime where needed
        scaled_rules = []
        for r in relation_rules:
            nr = dict(r)
            if r.get("type") == "gap_x":
                nr["value"] = float(r.get("value", 0)) * sx
            elif r.get("type") == "gap_y":
                nr["value"] = float(r.get("value", 0)) * sy
            if "tol" in nr:
                nr["tol"] = float(nr["tol"]) * max(sx, sy)
            scaled_rules.append(nr)
        pass_all = relation_check(pass_all, scaled_rules, abs_rects, args.tol * max(sx, sy))

    if args.enforce_inside_parent_mapped:
        for drawio_id, rule in mapping.items():
            parent_id = rule.get("parent_id", "")
            if not parent_id:
                continue
            child = abs_rects.get(drawio_id)
            parent_rect = abs_rects.get(parent_id)
            if not child or not parent_rect:
                pass_all &= report(False, f"runtime inside-parent resolvable: {drawio_id}")
                continue
            inside = (
                child["x"] >= parent_rect["x"] - tolx and
                child["y"] >= parent_rect["y"] - toly and
                (child["x"] + child["w"]) <= (parent_rect["x"] + parent_rect["w"] + tolx) and
                (child["y"] + child["h"]) <= (parent_rect["y"] + parent_rect["h"] + toly)
            )
            pass_all &= report(inside, f"runtime inside parent bounds: {drawio_id} in {parent_id}")

    sys.exit(0 if pass_all else 2)


if __name__ == "__main__":
    main()
