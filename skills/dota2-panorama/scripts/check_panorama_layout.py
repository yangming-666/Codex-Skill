#!/usr/bin/env python3
import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


BLOCK_RE = re.compile(r"([^{]+)\{([^}]*)\}", re.S)
DECL_RE = re.compile(r"([a-zA-Z\-]+)\s*:\s*([^;]+);")
PX_RE = re.compile(r"(-?\d+(?:\.\d+)?)px")


def parse_args():
    p = argparse.ArgumentParser(description="Static checker for Panorama layout against design contract.")
    p.add_argument("--contract", required=True, help="Contract json from extract_drawio_contract.py")
    p.add_argument("--xml", required=True, help="Panorama xml path")
    p.add_argument("--css", required=True, help="Panorama css path")
    p.add_argument("--map", default="", help="Mapping json: drawio_id -> selector/property mapping")
    p.add_argument("--required-map-ids", default="", help="Comma-separated drawio ids that must exist in mapping")
    p.add_argument("--required-selectors", default="", help="Comma-separated selectors that must exist in xml+css")
    p.add_argument("--relation-rules", default="", help="JSON file for relation checks over mapped ids")
    p.add_argument("--critical-selectors", default="", help="Comma-separated selectors to enforce strict rules")
    p.add_argument("--flow-allowed-selectors", default="", help="Comma-separated selectors allowed to use flow-children")
    p.add_argument("--anchor-offset-allowed-selectors", default="", help="Comma-separated selectors allowed to mix align anchors and manual offsets")
    p.add_argument("--scroll-selectors", default="", help="Comma-separated selectors that must support scroll")
    p.add_argument("--enforce-direct-parent-mapped", action="store_true", help="Require mapped selector's direct xml parent to match mapped parent selector")
    p.add_argument("--enforce-inside-parent-mapped", action="store_true", help="Require mapped selector geometry to stay inside its mapped parent rect")
    p.add_argument("--tol", type=float, default=2.0, help="Pixel tolerance")
    return p.parse_args()


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def parse_css(css_text):
    out = {}
    for m in BLOCK_RE.finditer(css_text):
        selectors = [s.strip() for s in m.group(1).split(",") if s.strip()]
        body = m.group(2)
        decls = {}
        for d in DECL_RE.finditer(body):
            decls[d.group(1).strip().lower()] = d.group(2).strip().lower()
        for s in selectors:
            out[s] = decls
    return out


def parse_xml_index(xml_path):
    root = ET.parse(xml_path).getroot()
    ids = {}
    classes = {}
    parent = {}

    for p in root.iter():
        for c in list(p):
            parent[id(c)] = p

    for elem in root.iter():
        elem_id = elem.get("id")
        elem_cls = elem.get("class")
        if elem_id:
            ids[elem_id] = elem
        if elem_cls:
            for c in elem_cls.split():
                if c:
                    classes.setdefault(c, []).append(elem)
    return root, ids, classes, parent


def parse_px(v):
    if not v:
        return None
    m = PX_RE.search(v)
    if not m:
        return None
    try:
        return float(m.group(1))
    except ValueError:
        return None


def report(ok, msg):
    prefix = "PASS" if ok else "FAIL"
    print(f"[{prefix}] {msg}")
    return ok


def selector_offset(css_map, selector):
    decls = css_map.get(selector, {})
    x = parse_px(decls.get("margin-left"))
    y = parse_px(decls.get("margin-top"))
    if x is None:
        x = parse_px(decls.get("left"))
    if y is None:
        y = parse_px(decls.get("top"))
    return (x or 0.0), (y or 0.0)


def selector_size(css_map, selector):
    decls = css_map.get(selector, {})
    w = parse_px(decls.get("width")) or 0.0
    h = parse_px(decls.get("height")) or 0.0
    return (w, h)


def resolve_selector_xml(selector, xml_ids, xml_classes):
    if not selector:
        return None
    if selector.startswith("#"):
        return xml_ids.get(selector[1:])
    if selector.startswith("."):
        arr = xml_classes.get(selector[1:], [])
        return arr[0] if arr else None
    return xml_ids.get(selector)


def selector_exists_in_xml(selector, xml_ids, xml_classes):
    return resolve_selector_xml(selector, xml_ids, xml_classes) is not None


def build_mapped_rects(mapping, css_map):
    rects = {}
    unresolved = dict(mapping)
    for _ in range(len(mapping) + 2):
        progressed = False
        for drawio_id, rule in list(unresolved.items()):
            sel = rule.get("selector", "")
            if not sel:
                unresolved.pop(drawio_id, None)
                continue
            decls = css_map.get(sel, {})
            if not decls:
                unresolved.pop(drawio_id, None)
                continue

            x_prop = rule.get("x_prop", "margin-left")
            y_prop = rule.get("y_prop", "margin-top")
            w_prop = rule.get("w_prop", "width")
            h_prop = rule.get("h_prop", "height")
            parent_selector = rule.get("parent_selector", "")
            parent_id = rule.get("parent_id", "")

            x = parse_px(decls.get(x_prop))
            y = parse_px(decls.get(y_prop))
            w = parse_px(decls.get(w_prop))
            h = parse_px(decls.get(h_prop))
            if x is None:
                x = 0.0
            if y is None:
                y = 0.0
            if w is None:
                w, _ = selector_size(css_map, sel)
            if h is None:
                _, h = selector_size(css_map, sel)

            if parent_id:
                if parent_id not in rects:
                    continue
                x += rects[parent_id]["x"]
                y += rects[parent_id]["y"]
            elif parent_selector:
                px, py = selector_offset(css_map, parent_selector)
                x += px
                y += py

            rects[drawio_id] = {"x": x, "y": y, "w": w, "h": h}
            unresolved.pop(drawio_id, None)
            progressed = True
        if not unresolved or not progressed:
            break
    return rects


def build_expected_abs(mapping, contract_map, css_map):
    """
    Build expected absolute x/y for both contract-backed ids and helper mapping ids.
    - If drawio id exists in contract: use contract absolute x/y.
    - Else (helper id): derive from parent expected abs + selector x/y props.
    """
    expected = {}
    unresolved = dict(mapping)
    for _ in range(len(mapping) + 3):
        progressed = False
        for drawio_id, rule in list(unresolved.items()):
            sel = rule.get("selector", "")
            if not sel:
                unresolved.pop(drawio_id, None)
                continue
            decls = css_map.get(sel, {})
            if not decls:
                unresolved.pop(drawio_id, None)
                continue

            if drawio_id in contract_map:
                c = contract_map[drawio_id]
                expected[drawio_id] = {"x": float(c["x"]), "y": float(c["y"])}
                unresolved.pop(drawio_id, None)
                progressed = True
                continue

            parent_id = rule.get("parent_id", "")
            parent_selector = rule.get("parent_selector", "")
            x_prop = rule.get("x_prop", "margin-left")
            y_prop = rule.get("y_prop", "margin-top")
            vx = parse_px(decls.get(x_prop))
            vy = parse_px(decls.get(y_prop))
            if vx is None:
                vx = 0.0
            if vy is None:
                vy = 0.0

            if parent_id:
                if parent_id not in expected:
                    continue
                expected[drawio_id] = {
                    "x": expected[parent_id]["x"] + vx,
                    "y": expected[parent_id]["y"] + vy
                }
                unresolved.pop(drawio_id, None)
                progressed = True
            elif parent_selector:
                px, py = selector_offset(css_map, parent_selector)
                expected[drawio_id] = {"x": px + vx, "y": py + vy}
                unresolved.pop(drawio_id, None)
                progressed = True
            else:
                expected[drawio_id] = {"x": vx, "y": vy}
                unresolved.pop(drawio_id, None)
                progressed = True
        if not unresolved or not progressed:
            break
    return expected


def check_relation_rules(pass_all, relation_rules, rects, tol_default):
    for r in relation_rules:
        rtype = str(r.get("type", ""))
        a = str(r.get("a", ""))
        b = str(r.get("b", ""))
        tol = float(r.get("tol", tol_default))
        ra = rects.get(a)
        rb = rects.get(b)
        if not ra or not rb:
            pass_all &= report(False, f"relation resolvable: {rtype} {a} {b}")
            continue
        if rtype == "center_x_equal":
            ca = ra["x"] + ra["w"] * 0.5
            cb = rb["x"] + rb["w"] * 0.5
            pass_all &= report(abs(ca - cb) <= tol, f"relation center_x_equal: {a} {b}")
        elif rtype == "center_y_equal":
            ca = ra["y"] + ra["h"] * 0.5
            cb = rb["y"] + rb["h"] * 0.5
            pass_all &= report(abs(ca - cb) <= tol, f"relation center_y_equal: {a} {b}")
        elif rtype == "gap_x":
            expected = float(r.get("value", 0))
            gap = rb["x"] - (ra["x"] + ra["w"])
            pass_all &= report(abs(gap - expected) <= tol, f"relation gap_x: {a}->{b}")
        elif rtype == "gap_y":
            expected = float(r.get("value", 0))
            gap = rb["y"] - (ra["y"] + ra["h"])
            pass_all &= report(abs(gap - expected) <= tol, f"relation gap_y: {a}->{b}")
        elif rtype == "width_ratio":
            expected = float(r.get("value", 1))
            ratio = (ra["w"] / rb["w"]) if rb["w"] else 0
            pass_all &= report(abs(ratio - expected) <= tol * 0.01, f"relation width_ratio: {a}/{b}")
        elif rtype == "left_equal":
            pass_all &= report(abs(ra["x"] - rb["x"]) <= tol, f"relation left_equal: {a} {b}")
        elif rtype == "right_equal":
            ra_r = ra["x"] + ra["w"]
            rb_r = rb["x"] + rb["w"]
            pass_all &= report(abs(ra_r - rb_r) <= tol, f"relation right_equal: {a} {b}")
        elif rtype == "top_equal":
            pass_all &= report(abs(ra["y"] - rb["y"]) <= tol, f"relation top_equal: {a} {b}")
        elif rtype == "bottom_equal":
            ra_b = ra["y"] + ra["h"]
            rb_b = rb["y"] + rb["h"]
            pass_all &= report(abs(ra_b - rb_b) <= tol, f"relation bottom_equal: {a} {b}")
        else:
            pass_all &= report(False, f"unknown relation type: {rtype}")
    return pass_all


def main():
    args = parse_args()
    contract = read_json(args.contract)
    css_map = parse_css(Path(args.css).read_text(encoding="utf-8"))
    _, xml_ids, xml_classes, xml_parent = parse_xml_index(args.xml)

    mapping = {}
    if args.map:
        mapping = read_json(args.map)
    relation_rules = []
    if args.relation_rules:
        rr = read_json(args.relation_rules)
        if isinstance(rr, dict):
            relation_rules = rr.get("rules", [])
        elif isinstance(rr, list):
            relation_rules = rr
    required_map_ids = [s.strip() for s in args.required_map_ids.split(",") if s.strip()]
    required_selectors = [s.strip() for s in args.required_selectors.split(",") if s.strip()]

    critical_selectors = [s.strip() for s in args.critical_selectors.split(",") if s.strip()]
    flow_allowed = {s.strip() for s in args.flow_allowed_selectors.split(",") if s.strip()}
    anchor_offset_allowed = {s.strip() for s in args.anchor_offset_allowed_selectors.split(",") if s.strip()}
    scroll_selectors = [s.strip() for s in args.scroll_selectors.split(",") if s.strip()]
    pass_all = True

    # 1) required selectors and critical selector existence
    all_required = []
    all_required.extend(required_selectors)
    for sel in critical_selectors:
        if sel not in all_required:
            all_required.append(sel)
    for sel in all_required:
        pass_all &= report(sel in css_map, f"selector in css: {sel}")
        pass_all &= report(selector_exists_in_xml(sel, xml_ids, xml_classes), f"selector exists in xml: {sel}")

    # 2) prohibited patterns on critical selectors
    for sel in critical_selectors:
        decls = css_map.get(sel, {})
        flow = decls.get("flow-children", "")
        fit = decls.get("height", "") == "fit-children" or decls.get("width", "") == "fit-children"
        width_pct = decls.get("width", "").strip() == "100%"
        fill_parent = "fill-parent-flow" in decls.get("width", "") or "fill-parent-flow" in decls.get("height", "")
        h_align_val = decls.get("horizontal-align", "").strip()
        v_align_val = decls.get("vertical-align", "").strip()
        m_left = parse_px(decls.get("margin-left"))
        m_top = parse_px(decls.get("margin-top"))
        left = parse_px(decls.get("left"))
        top = parse_px(decls.get("top"))
        has_x_offset = ((m_left is not None and abs(m_left) > 0.01) or (left is not None and abs(left) > 0.01))
        has_y_offset = ((m_top is not None and abs(m_top) > 0.01) or (top is not None and abs(top) > 0.01))
        h_conflict = h_align_val in ("center", "right") and has_x_offset
        v_conflict = v_align_val in ("center", "bottom") and has_y_offset
        mixed_anchor_offset = h_conflict or v_conflict
        has_negative_margin = (m_left is not None and m_left < 0) or (m_top is not None and m_top < 0)
        if sel in flow_allowed:
            pass_all &= report(True, f"flow-children allowed by config: {sel}")
        else:
            pass_all &= report(not flow, f"no flow-children on critical selector: {sel}")
        pass_all &= report(not fit, f"no fit-children on critical selector: {sel}")
        pass_all &= report(not width_pct, f"no width:100% on critical selector: {sel}")
        pass_all &= report(not fill_parent, f"no fill-parent-flow on critical selector: {sel}")
        if sel in anchor_offset_allowed:
            pass_all &= report(True, f"anchor+offset mix allowed by config: {sel}")
        else:
            pass_all &= report(not mixed_anchor_offset, f"no anchor+offset conflict: {sel}")
        pass_all &= report(not has_negative_margin, f"no negative margin on critical selector: {sel}")

    # 3) scroll requirements
    for sel in scroll_selectors:
        decls = css_map.get(sel, {})
        overflow = decls.get("overflow", "")
        pass_all &= report("scroll" in overflow, f"scroll enabled: {sel}")

    if mapping:
        c = contract.get("contract", {})
        expected_abs = build_expected_abs(mapping, c, css_map)

        # 4) required mapping ids
        for rid in required_map_ids:
            pass_all &= report(rid in mapping, f"required mapping id present: {rid}")

        # 5) mapping geometry checks
        for drawio_id, rule in mapping.items():
            target = c.get(drawio_id)
            sel = rule.get("selector", "")
            decls = css_map.get(sel, {})
            if not sel or not decls:
                pass_all &= report(False, f"mapping resolvable: {drawio_id} -> {sel}")
                continue
            if not target:
                pass_all &= report(True, f"helper mapping node (no contract id): {drawio_id} -> {sel}")
                continue
            x_prop = rule.get("x_prop", "margin-left")
            y_prop = rule.get("y_prop", "margin-top")
            w_prop = rule.get("w_prop", "width")
            h_prop = rule.get("h_prop", "height")
            parent_selector = rule.get("parent_selector", "")
            parent_id = rule.get("parent_id", "")

            vx, vy = parse_px(decls.get(x_prop)), parse_px(decls.get(y_prop))
            vw, vh = parse_px(decls.get(w_prop)), parse_px(decls.get(h_prop))

            expected_x = float(target["x"])
            expected_y = float(target["y"])
            if parent_id and parent_id in expected_abs:
                expected_x -= float(expected_abs[parent_id]["x"])
                expected_y -= float(expected_abs[parent_id]["y"])
            elif parent_selector:
                px, py = selector_offset(css_map, parent_selector)
                expected_x -= px
                expected_y -= py

            if vx is not None:
                pass_all &= report(abs(vx - expected_x) <= args.tol, f"x within tol: {drawio_id} {sel}")
            if vy is not None:
                pass_all &= report(abs(vy - expected_y) <= args.tol, f"y within tol: {drawio_id} {sel}")
            if vw is not None:
                pass_all &= report(abs(vw - float(target["width"])) <= args.tol, f"w within tol: {drawio_id} {sel}")
            if vh is not None:
                pass_all &= report(abs(vh - float(target["height"])) <= args.tol, f"h within tol: {drawio_id} {sel}")

        # 6) direct parent checks over xml tree (catches wrong parent mapping)
        if args.enforce_direct_parent_mapped:
            for drawio_id, rule in mapping.items():
                sel = rule.get("selector", "")
                child_elem = resolve_selector_xml(sel, xml_ids, xml_classes)
                if child_elem is None:
                    pass_all &= report(False, f"xml child resolvable: {drawio_id} {sel}")
                    continue
                expected_parent_elem = None
                parent_id = rule.get("parent_id", "")
                parent_selector = rule.get("parent_selector", "")
                if parent_id:
                    parent_rule = mapping.get(parent_id, {})
                    psel = parent_rule.get("selector", "")
                    expected_parent_elem = resolve_selector_xml(psel, xml_ids, xml_classes)
                    pass_all &= report(expected_parent_elem is not None, f"xml parent resolvable by parent_id: {drawio_id} -> {parent_id}")
                elif parent_selector:
                    expected_parent_elem = resolve_selector_xml(parent_selector, xml_ids, xml_classes)
                    pass_all &= report(expected_parent_elem is not None, f"xml parent resolvable by parent_selector: {drawio_id}")
                else:
                    continue

                if expected_parent_elem is None:
                    continue
                direct_parent = xml_parent.get(id(child_elem))
                pass_all &= report(direct_parent is expected_parent_elem, f"direct parent match: {drawio_id} {sel}")

        # 7) mapped inside parent checks
        rects = build_mapped_rects(mapping, css_map)
        if args.enforce_inside_parent_mapped:
            for drawio_id, rule in mapping.items():
                parent_id = rule.get("parent_id", "")
                if not parent_id:
                    continue
                child = rects.get(drawio_id)
                parent_rect = rects.get(parent_id)
                if not child or not parent_rect:
                    pass_all &= report(False, f"inside-parent resolvable: {drawio_id}")
                    continue
                inside = (
                    child["x"] >= parent_rect["x"] - args.tol and
                    child["y"] >= parent_rect["y"] - args.tol and
                    (child["x"] + child["w"]) <= (parent_rect["x"] + parent_rect["w"] + args.tol) and
                    (child["y"] + child["h"]) <= (parent_rect["y"] + parent_rect["h"] + args.tol)
                )
                pass_all &= report(inside, f"inside parent bounds: {drawio_id} in {parent_id}")

        # 8) relation checks
        if relation_rules:
            pass_all = check_relation_rules(pass_all, relation_rules, rects, args.tol)

    sys.exit(0 if pass_all else 2)


if __name__ == "__main__":
    main()
