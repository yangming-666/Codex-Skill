# Panorama validation

Run validation only when the user requests it or the repository policy requires/allows it. A repository prohibition on automatic Panorama checks overrides the defaults below.

Resolve commands relative to the current skill directory; never embed a user directory or `$CODEX_HOME`.

## Syntax

```powershell
python scripts/check_panorama_syntax.py --paths <changed-source-files>
```

Use for new layouts, new WorldPanels, include/path changes, or structural refactors when authorized.

## Draw.io contract and shell

```powershell
python scripts/extract_drawio_contract.py --drawio <design.drawio> --out <contract.json>
python scripts/generate_panorama_replica.py --contract <contract.json> --xml-out <layout.xml> --css-out <style.css>
```

## Static layout

```powershell
python scripts/check_panorama_layout.py --contract <contract.json> --xml <layout.xml> --css <style.css> --map <mapping.json> --relation-rules <relations.json> --enforce-direct-parent-mapped --enforce-inside-parent-mapped
```

Add required IDs/selectors, critical selectors, allowed flow selectors, and scroll selectors for the actual task rather than copying an unrelated screen's list.

Mapping entries should identify selector, direct `parent_id`, and geometry properties. Relations should encode center equality, gaps, ratios, and the agreed tolerance.

## Relation sheet

```powershell
python scripts/generate_relation_sheet.py --contract <contract.json> --mapping <mapping.json> --relations <relations.json> --out <replica_relations.md>
```

## Runtime

Collect geometry with `scripts/dump_runtime_layout.js` or the project's `GameUI.ReplicaDumpLayout` integration, then run:

```powershell
python scripts/check_runtime_layout.py --contract <contract.json> --dump <runtime_dump.txt> --map <mapping.json> --relation-rules <relations.json> --enforce-inside-parent-mapped
```

Require the selectors and visible selectors appropriate to the current screen. Finish with a screenshot comparison when strict visual fidelity is in scope.
