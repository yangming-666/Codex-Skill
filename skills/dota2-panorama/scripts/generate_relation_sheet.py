#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def parse_args():
    p = argparse.ArgumentParser(description="Generate simple alignment/gap/ratio sheet from mapping+relations.")
    p.add_argument("--contract", required=True, help="Contract JSON path")
    p.add_argument("--mapping", required=True, help="Mapping JSON path")
    p.add_argument("--relations", required=True, help="Relations JSON path")
    p.add_argument("--out", required=True, help="Output markdown path")
    return p.parse_args()


def selector_of(mapping, drawio_id):
    node = mapping.get(drawio_id, {})
    return node.get("selector", "")


def main():
    args = parse_args()
    contract = json.loads(Path(args.contract).read_text(encoding="utf-8-sig")).get("contract", {})
    mapping = json.loads(Path(args.mapping).read_text(encoding="utf-8-sig"))
    rel = json.loads(Path(args.relations).read_text(encoding="utf-8-sig"))
    rules = rel.get("rules", []) if isinstance(rel, dict) else rel

    lines = []
    lines.append("# Replica Relation Sheet")
    lines.append("")
    lines.append("## Node Mapping")
    lines.append("")
    lines.append("| drawio id | panorama selector | x | y | w | h |")
    lines.append("|---|---|---:|---:|---:|---:|")
    for k, v in mapping.items():
        c = contract.get(k, {})
        lines.append(
            f"| `{k}` | `{v.get('selector','')}` | {c.get('x','')} | {c.get('y','')} | {c.get('width','')} | {c.get('height','')} |"
        )

    lines.append("")
    lines.append("## Relation Rules")
    lines.append("")
    lines.append("| type | A(drawio->selector) | B(drawio->selector) | target | tol |")
    lines.append("|---|---|---|---:|---:|")
    for r in rules:
        a = str(r.get("a", ""))
        b = str(r.get("b", ""))
        t = str(r.get("type", ""))
        target = r.get("value", "")
        tol = r.get("tol", "")
        lines.append(
            f"| `{t}` | `{a}` -> `{selector_of(mapping,a)}` | `{b}` -> `{selector_of(mapping,b)}` | {target} | {tol} |"
        )

    lines.append("")
    lines.append("## Usage")
    lines.append("")
    lines.append("1. In draw.io page 3, duplicate page 1 layout.")
    lines.append("2. Replace each node text with its Panorama selector from the table above.")
    lines.append("3. Keep this file as the readable source for alignment/gap/ratio constraints.")
    lines.append("")

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"generated {out}")


if __name__ == "__main__":
    main()
