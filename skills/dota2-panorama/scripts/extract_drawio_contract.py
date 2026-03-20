#!/usr/bin/env python3
import argparse
import json
import xml.etree.ElementTree as ET
from pathlib import Path


def to_float(v, default=0.0):
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


def parse_args():
    p = argparse.ArgumentParser(description="Extract draw.io geometry contract.")
    p.add_argument("--drawio", required=True, help="Path to .drawio file")
    p.add_argument("--out", required=True, help="Path to output JSON")
    p.add_argument("--diagram", default="", help="Diagram name or id (default: first diagram)")
    p.add_argument("--id-prefix", default="", help="Only include ids with this prefix")
    return p.parse_args()


def pick_diagram(root, wanted):
    diagrams = root.findall("diagram")
    if not diagrams:
        raise ValueError("No <diagram> found in drawio file.")
    if not wanted:
        return diagrams[0]
    for d in diagrams:
        if d.get("name") == wanted or d.get("id") == wanted:
            return d
    raise ValueError(f"Diagram not found: {wanted}")


def main():
    args = parse_args()
    drawio_path = Path(args.drawio)
    out_path = Path(args.out)

    root = ET.parse(drawio_path).getroot()
    diagram = pick_diagram(root, args.diagram)
    if len(diagram):
        graph = diagram[0]
    else:
        raw = (diagram.text or "").strip()
        if not raw:
            raise ValueError("Diagram has no mxGraphModel content.")
        graph = ET.fromstring(raw)

    contract = {}
    for cell in graph.findall(".//mxCell"):
        if cell.get("vertex") != "1":
            continue
        cell_id = cell.get("id", "")
        if not cell_id:
            continue
        if args.id_prefix and not cell_id.startswith(args.id_prefix):
            continue
        geo = cell.find("mxGeometry")
        if geo is None:
            continue

        x = to_float(geo.get("x"), 0.0)
        y = to_float(geo.get("y"), 0.0)
        w = to_float(geo.get("width"), 0.0)
        h = to_float(geo.get("height"), 0.0)
        contract[cell_id] = {
            "x": x,
            "y": y,
            "width": w,
            "height": h,
            "value": cell.get("value", ""),
        }

    out = {
        "source": str(drawio_path),
        "diagram_name": diagram.get("name", ""),
        "diagram_id": diagram.get("id", ""),
        "count": len(contract),
        "contract": contract,
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"extracted={len(contract)} -> {out_path}")


if __name__ == "__main__":
    main()
