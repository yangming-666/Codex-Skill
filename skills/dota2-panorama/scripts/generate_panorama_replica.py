#!/usr/bin/env python3
import argparse
import html
import json
import re
from pathlib import Path


def safe_name(raw):
    return re.sub(r"[^a-zA-Z0-9_]", "_", raw)


def parse_args():
    p = argparse.ArgumentParser(description="Generate Panorama replica shell from drawio contract JSON.")
    p.add_argument("--contract", required=True, help="Path to contract JSON from extract_drawio_contract.py")
    p.add_argument("--xml-out", required=True, help="Output xml path")
    p.add_argument("--css-out", required=True, help="Output css path")
    p.add_argument("--panel-class", default="ReplicaCanvas", help="Class for root design panel")
    p.add_argument("--canvas-width", type=int, default=1920, help="Design canvas width")
    p.add_argument("--canvas-height", type=int, default=1080, help="Design canvas height")
    p.add_argument("--id-prefix", default="", help="Only emit ids with this prefix")
    return p.parse_args()


def format_px(v):
    return f"{int(round(float(v)))}px"


def clean_value(v):
    s = str(v or "")
    s = s.replace("<br>", "\n").replace("&#xa;", "\n")
    s = re.sub(r"<[^>]+>", "", s)
    return s.strip()


def main():
    args = parse_args()
    data = json.loads(Path(args.contract).read_text(encoding="utf-8-sig"))
    contract = data.get("contract", {})
    rows = []
    for node_id, node in contract.items():
        if args.id_prefix and not node_id.startswith(args.id_prefix):
            continue
        rows.append((node_id, node))
    rows.sort(key=lambda it: (float(it[1].get("y", 0)), float(it[1].get("x", 0))))

    xml_lines = [
        "<root>",
        "    <styles>",
        "        <include src=\"s2r://panorama/styles/dotastyles.vcss_c\" />",
        f"        <include src=\"file://{{resources}}/styles/custom_game/{Path(args.css_out).name}\" />",
        "    </styles>",
        "    <Panel class=\"ReplicaHost\">",
        f"        <Panel id=\"ReplicaCanvas\" class=\"{args.panel_class}\">",
    ]

    css_lines = [
        ".ReplicaHost {",
        "    width: 100%;",
        "    height: 100%;",
        "}",
        "",
        f".{args.panel_class} {{",
        f"    width: {args.canvas_width}px;",
        f"    height: {args.canvas_height}px;",
        "    horizontal-align: center;",
        "    vertical-align: center;",
        "}",
        "",
    ]

    for node_id, node in rows:
        node_key = safe_name(node_id)
        panel_id = f"Node_{node_key}"
        class_name = f"ReplicaNode_{node_key}"
        value_text = clean_value(node.get("value", ""))
        xml_lines.append(f"            <Panel id=\"{panel_id}\" class=\"{class_name}\">")
        if value_text:
            escaped = html.escape(value_text)
            xml_lines.append(f"                <Label class=\"ReplicaLabel\" text=\"{escaped}\" />")
        xml_lines.append("            </Panel>")

        css_lines.extend(
            [
                f".{class_name} {{",
                f"    margin-left: {format_px(node.get('x', 0))};",
                f"    margin-top: {format_px(node.get('y', 0))};",
                f"    width: {format_px(node.get('width', 0))};",
                f"    height: {format_px(node.get('height', 0))};",
                "}",
                "",
            ]
        )

    xml_lines.extend(
        [
            "        </Panel>",
            "    </Panel>",
            "</root>",
            "",
        ]
    )

    css_lines.extend(
        [
            ".ReplicaLabel {",
            "    width: 100%;",
            "    height: 100%;",
            "    text-align: center;",
            "    vertical-align: center;",
            "    text-overflow: shrink;",
            "}",
            "",
        ]
    )

    xml_path = Path(args.xml_out)
    css_path = Path(args.css_out)
    xml_path.parent.mkdir(parents=True, exist_ok=True)
    css_path.parent.mkdir(parents=True, exist_ok=True)
    xml_path.write_text("\n".join(xml_lines), encoding="utf-8")
    css_path.write_text("\n".join(css_lines), encoding="utf-8")
    print(f"generated xml={xml_path} css={css_path} nodes={len(rows)}")


if __name__ == "__main__":
    main()
