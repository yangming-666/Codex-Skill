---
name: dota2-panorama
description: Dota 2 Panorama UI authoring and maintenance. Use when creating or modifying Panorama layout (VXML), styles (VCSS), or scripts (VJS), wiring CustomUIElement entries, integrating GameEvents/CustomNetTables/localization, or reproducing UI from a design spec (draw.io/Figma/image). For design-replica requests, enforce strict coordinate contracts, hard validation gates, and no "close enough" delivery.
---

# Dota2 Panorama

## Overview

Create, edit, and debug Dota 2 Panorama UI with correct syntax, runtime APIs, and manifest wiring.

## Repo Path Rules

- In this repo, Panorama source lives under `content/dzsj/panorama/...`.
- Compiled/build artifacts live under `game/dzsj/panorama/...` and usually end with `_c` (`.vjs_c`, `.vxml_c`, `.vcss_c`).
- When a compiled file is present, always search for the matching source file in `content/dzsj/panorama/...` before editing anything.
- Use the same relative subpath and replace the compiled extension with the source extension:
  - `game/dzsj/panorama/scripts/custom_game/camera.vjs_c` -> `content/dzsj/panorama/scripts/custom_game/camera.js`
  - `game/dzsj/panorama/layout/custom_game/camera.vxml_c` -> `content/dzsj/panorama/layout/custom_game/camera.xml`
- If both source and compiled files exist, edit the source only and leave compiled artifacts untouched.

## Core Workflow

1) Identify scope
- Decide new panel vs existing panel change.
- Decide load type (Hud, HeroSelection, GameSetup, EndScreen).

2) Update layout (VXML)
- Edit panel tree and classes.
- Keep layout declarative; move behavior to scripts.

3) Update styles (VCSS)
- Implement geometry and visuals.
- Avoid unsupported CSS features.

4) Update scripts (VJS)
- Wire events, net tables, and client-side rendering.
- Use custom game events for server calls.

5) Wire manifest
- Ensure `custom_ui_manifest.xml` has the target CustomUIElement.

6) Run syntax guard
- For any new or modified Panorama file, run `python scripts/check_panorama_syntax.py --paths <changed files...>` before claiming completion.
- If the task adds a new `layout/custom_game/worldpanels/*.xml`, run the syntax guard on that file even if no other checks are requested.

## Panorama Syntax Guardrails

- Treat Panorama XML parser constraints as hard rules, not style preferences.
- The first actual root panel in a layout file must not include an `id` attribute. Use `class` on the root panel and put `id` only on descendants.
- For new layout files, prefer copying the nearest existing working template in the repo instead of hand-writing the outer structure from memory.
- For new worldpanels, compare against an existing worldpanel in the repo before editing behavior or styling.
- For worldpanels with placement precision requirements, default to the `boss_health` pattern, not the `shop1_dummy_level` pattern:
  - explicit fixed-size root
  - explicit fixed-size inner frame
  - server-provided `worldpanel_fixed_width` / `worldpanel_fixed_height`
  - `horizontal-align: left`, `vertical-align: top`, `position: 0px 0px 0px` on the anchor root
- Do not rely on memory for Panorama-only syntax. If the structure is fragile, verify it against an existing local file first.
- If a JS file needs the layout root, use `$.GetContextPanel()` rather than assuming the root has an `id`.

## New Layout Checklist

Run this checklist for any newly created `.xml` Panorama layout, especially under `layout/custom_game/worldpanels/`:

1) Structure
- The file has a `<root>` wrapper.
- The first actual panel node under `<root>` does not have an `id`.
- `styles` / `scripts` includes appear before the actual panel tree.

2) Reference integrity
- Included CSS and JS files exist on disk.
- Referenced panorama resource paths use the correct `file://{resources}` or `s2r://` scheme.
- File naming is consistent across `layout/`, `scripts/`, and `styles/` when the feature is intended to be a matched set.

3) Template parity
- If the file is a worldpanel, compare its root structure with one existing compiled worldpanel in the repo.
- If the file is a full HUD panel or popup, compare against a same-category existing layout before finishing.
- If the worldpanel must appear exactly over an in-world target, require fixed-size parity with `boss_health` unless the repo already contains a different verified fixed-size template for the same category.

4) Validation
- Run `python scripts/check_panorama_syntax.py --paths <changed files...>`.
- If local compile is available for the task, compile after syntax guard and treat compile failure as blocking.

## Strict Design-Replica Mode

Trigger when user asks to "按设计图实现/对照 draw.io/像素级还原/严格一致".

### Non-Negotiable Rules

1) Freeze one coordinate system
- If draw.io uses absolute px, implement absolute px for all design-critical blocks.
- Do not mix proportional and ad-hoc margin tuning.

2) Output a geometry contract before coding
- Build `id -> x,y,width,height` from draw.io first.
- Use `scripts/extract_drawio_contract.py` to generate contract JSON.
- Do not start CSS until contract exists.
- Build relation contract at the same time (center lines, group gaps, proportional widths).

3) Use hybrid layout model (fixed outside, adaptive inside)
- Outer shell (`main panel`, section containers, headers, button bar) must be fixed geometry.
- Adaptive behavior is allowed only inside designated content slots.

4) Respect prohibited patterns on critical chains
- Do not use `fit-children` on design-critical blocks.
- Do not use `fill-parent-flow` or `width: 100%` for design-critical geometry.
- Do not solve one alignment problem with both flow positioning and manual offsets.
- If a critical selector must use flow (for controlled text/button stacking), declare it explicitly in a flow-allowed list during validation.
- Do not mix anchor alignment (`horizontal-align`/`vertical-align`) with manual offsets (`margin-left/top` or `left/top`) on the same selector unless explicitly allowlisted.
- Treat as hard conflict: `horizontal-align:center/right` with x-offsets, `vertical-align:center/bottom` with y-offsets.
- Do not use negative margins for design-critical positioning.

5) Separate geometry and typography phases
- Phase A: structure + geometry only.
- Phase B: text centering and overflow handling (`text-overflow: shrink`).
- Phase C: optional optical +/-1px corrections only.

6) Handle HUD interference explicitly
- For full-screen end-state replicas, verify whether foreign HUD panels are visible.
- If visible and conflicting with design intent, add explicit hide/show rules for end-state.

## Replica Pipeline (Required)

Execute in this order for replica tasks:

1) Extract contract from draw.io.
2) Build relation rules (alignment, spacing, ratio) from draw.io.
3) Create a draw.io page-3 "Panorama Mapping View":
- Duplicate the design page on page 3.
- Replace node text with Panorama class/selector names.
- Keep all alignment lines, spacing labels, and ratio labels visible.
- Page-3 annotation rules (required):
  - Class text in container must use adaptive font sizing first.
  - If class text cannot fit or is covered by child containers, switch to external callout + connector.
  - External callouts can be placed around all sides (360-degree), not only one side.
  - Connector lines must be straight (no polyline bends), non-overlapping, and use the same color as the callout box stroke/text.
  - External callout boxes must be outside `Class Mapping Area (inside 1920x1080)`.
  - `Alignment Relation Area` must be placed to the right of callout area (further right than class callouts).
4) Generate a readable relation sheet file from contract + mapping + relations.
5) Generate fixed shell skeleton from contract.
6) Apply controlled adaptive behavior only inside content slots.
7) Run static checker with geometry + relation checks.
8) Dump runtime geometry and compare with contract.
9) Perform final visual check against design screenshot.

## Dynamic Content Contract (Required in Replica Tasks)

Use this model unless user asks otherwise:

- `Outer`: fixed by draw.io contract.
- `Damage rows`: scroll container for overflow.
- `Reward panel`: fixed two-group shell.
- `Star rewards`: fixed slot count (1/2/3 star cards).
- `Normal rewards`: controlled adaptive policy:
  - 1 item: centered single card.
  - 2 items: centered two-column.
  - 3+ items: wrap + vertical scroll.

## Acceptance Gate (Definition of Done)

Do not claim completion until all checks pass:

1) Geometry fidelity
- Critical blocks are within ±2px of contract in x/y/w/h.
- For child blocks inside a positioned parent, validate with parent-relative offsets using mapping `parent_selector`.
- Mapping must include relation-critical child ids, not only container ids.
- Mapping parent chain must match XML direct parent chain for mapped critical ids.

2) Relation fidelity (required)
- Center-line relations (for example title vs section center) must pass.
- Gap relations (vertical rhythm and horizontal spacing) must pass.
- Group-level ratio/width relations must pass.

3) No clipping
- Key labels are not clipped (rating text, button text, reward labels).
- Mapped critical children remain inside mapped parent bounds unless explicitly allowlisted.

4) Overflow behavior
- Damage and reward content overflow via scroll (not truncation by logic).

5) State stability
- Win/lose, first-clear/non-first-clear, 1/2/N reward counts preserve shell geometry.

6) Validation artifacts
- Save contract JSON and checker report for the task.

7) Runtime geometry and visual parity
- Runtime panel geometry dump must satisfy contract/relations.
- Final screenshot must not have obvious drift from the design.

8) Page-3 annotation quality
- No class-text clipping in mapped containers.
- For external callouts, connector crossings are not allowed.
- Class mapping area and relation area must be visually separated and non-overlapping.

## Validation Scripts

Use bundled scripts for replica tasks:
Run commands from this skill root (`C:/Users/ym199/.codex/skills/dota2-panorama`) or call scripts via absolute path.

General syntax validation for any Panorama task:
```bash
python scripts/check_panorama_syntax.py --paths <changed panorama files...>
```

This check is required for:
- new `.xml` layout files
- new worldpanels
- refactors that move or rename included CSS/JS files
- any task that changes Panorama resource paths

1) Extract contract
```bash
python scripts/extract_drawio_contract.py --drawio <path/to/design.drawio> --out <contract.json>
```

2) Generate replica shell
```bash
python scripts/generate_panorama_replica.py \
  --contract <contract.json> \
  --xml-out <layout.xml> \
  --css-out <style.css>
```

3) Check panorama layout
```bash
python scripts/check_panorama_layout.py \
  --contract <contract.json> \
  --xml <layout.xml> \
  --css <style.css> \
  --map <mapping.json> \
  --relation-rules <relations.json> \
  --required-map-ids "main-panel,summary-card,result-title,stage-name,remain-hp,rating-container,reward-panel,reward-title,unlock-banner,button-bar,primary-button,secondary-button,diamond-group,normal-group" \
  --required-selectors ".EndResultTitle,.EndStageName,.EndRemainHp,.EndRatingContainer,.EndDamageRow,.EndRewardTitle,.EndUnlockBanner" \
  --critical-selectors ".EndMainPanel,.EndSummaryCard,.EndDamagePanel,.EndRewardPanel,.EndButtonBar" \
  --flow-allowed-selectors ".EndDamagePanel" \
  --scroll-selectors ".EndDamageRows.NeedScroll,.EndRewardBody.NeedScroll" \
  --enforce-direct-parent-mapped \
  --enforce-inside-parent-mapped
```

`mapping.json` supports parent-relative checks:
```json
{
  "summary-card": {
    "selector": ".EndSummaryCard",
    "parent_id": "main-panel",
    "x_prop": "margin-left",
    "y_prop": "margin-top",
    "w_prop": "width",
    "h_prop": "height"
  }
}
```

Use `parent_id` as the preferred parent chain mechanism for nested layouts. Use `parent_selector` only when parent is not part of mapping.
For design-critical mapped nodes, `parent_id` should point to the direct XML parent mapping.

`relations.json` example:
```json
{
  "rules": [
    {"type": "center_x_equal", "a": "result-title", "b": "stage-name", "tol": 2},
    {"type": "center_x_equal", "a": "reward-title", "b": "reward-panel", "tol": 2},
    {"type": "center_x_equal", "a": "primary-button", "b": "button-bar", "tol": 2},
    {"type": "gap_x", "a": "diamond-group", "b": "normal-group", "value": 20, "tol": 2}
  ]
}
```

4) Generate relation sheet (human-readable handoff artifact)
```bash
python scripts/generate_relation_sheet.py \
  --contract <contract.json> \
  --mapping <mapping.json> \
  --relations <relations.json> \
  --out <replica_relations.md>
```

This file is required for replica acceptance and must clearly show:
- draw.io id -> Panorama selector mapping
- alignment/gap/ratio constraints
- page-3 mapping-view usage notes

5) Dump runtime geometry in Panorama JS
```js
GameUI.ReplicaDumpLayout("#GameFlowRoot", [
  ".EndMainPanel",
  ".EndSummaryCard",
  ".EndDamagePanel",
  ".EndRewardPanel",
  ".EndButtonBar"
], "");
```

6) Check runtime geometry dump
```bash
python scripts/check_runtime_layout.py \
  --contract <contract.json> \
  --dump <runtime_dump.txt> \
  --map <mapping.json> \
  --relation-rules <relations.json> \
  --required-selectors ".EndMainPanel,.EndSummaryCard,.EndResultTitle,.EndStageName,.EndRemainHp,.EndRatingContainer,.EndDamagePanel,.EndRewardPanel,.EndRewardTitle,.EndUnlockBanner,.EndDiamondGroup,.EndNormalGroup,.EndButtonBar,.EndPrimaryButton,.EndSecondaryButton" \
  --require-visible-selectors ".EndResultTitle,.EndStageName,.EndRemainHp,.EndRatingContainer,.EndRewardTitle,.EndUnlockBanner,.EndPrimaryButton,.EndSecondaryButton" \
  --enforce-inside-parent-mapped
```

If check fails, revise skill workflow/rules before retrying implementation.

## Guidelines

- Prefer `file://{resources}/...` for local development assets and `s2r://...` for compiled resources.
- Edit source files under `content/<addon>/panorama/...` (`.xml`, `.js`, `.css`); avoid editing compiled files under `game/<addon>/panorama/...` (`.vxml_c`, `.vjs_c`, `.vcss_c`).
- If only compiled files appear, locate the source in `content/` and rebuild; do not patch `_c` files directly except as a last-resort with explicit user approval.
- The root panel inside a `layout` file must not include an `id` attribute; use `class` and assign `id` on child panels instead.
- For image sources from KV paths, use `s2r://(path in kv).vtex` with no `_c`, e.g. `src="s2r://panorama/images/heroes/selection/npc_dota_hero_invoker_persona1_png.vtex"`.
- For item icons specifically, use `s2r://panorama/images/items/<item_name>_png.vtex`.
- When normalizing image paths in JS, handle `.vtex_c` → `.vtex` and `.vsvg_c` → `.vsvg`, and avoid appending `.vtex` to SVG paths.
- Image aspect ratio is a hard-compatibility rule in Panorama:
  - Default safe pattern: use a wrapper `Panel` with fixed geometry, then render the image via `background-image`.
  - Preferred CSS on that image panel:
    ```css
    .SomeImagePanel {
        width: 100%;
        height: 100%;
        background-image: url("file://{images}/...");
        background-size: contain;
        background-position: center;
        background-repeat: no-repeat;
    }
    ```
  - If the image path is dynamic in JS, set `panel.style.backgroundImage`, not a child `Image` with unsupported CSS hacks.
  - Do not use `preserve-aspect-fit`; Panorama parser does not support it.
  - Do not invent CSS properties based on web habits. If a property is not known to Panorama, assume it is unsupported until verified.
  - Do not claim an image will keep aspect ratio unless the implementation uses `background-size: contain` or another Panorama-verified approach.
  - Treat plain `Image` panels with both width and height forced as stretch-risk by default. Only use them when distortion is acceptable or behavior is explicitly verified in this repo.
  - When migrating an existing stretched image, prefer replacing the visual node with `Panel + background-image` rather than stacking more properties onto `Image`.
- Keep layout files declarative; move behavior to scripts.
- For text blocks that need vertical centering or stable anchor geometry, separate box geometry from text rendering:
  - If a `Label` is currently responsible for both container geometry and text rendering, wrap it in a `Panel`.
  - Let the wrapper `Panel` own box concerns: `width/height`, margins, anchor alignment, background/border visuals, clipping, and state/visibility classes.
  - Let the `Label` own text concerns only: text content, `width: 100%` when needed for wrapping/centering, `height: fit-children`, `vertical-align`, `text-align`, `font-*`, `color`, `text-overflow`, and small optical corrections.
  - When the text should be centered inside a fixed wrapper, default the `Label` to:
    ```css
    width: 100%;
    height: fit-children;
    vertical-align: center;
    text-align: center;
    ```
  - Do not use `horizontal-align: center` alone as a text-centering strategy; it centers the `Label` panel, not necessarily the glyphs.
  - Only add `horizontal-align: center` to a `Label` when the `Label` itself is intentionally narrower than its parent and must be positioned as a panel.
  - Prefer this wrapper + label pattern over `height: 100%` or `line-height` hacks. Use `line-height` or tiny offsets only as final optical correction after the wrapper/label split is correct.
  - Apply the same rule to dynamically created Panorama JS content: build `Panel(wrapper) + Label`, not one heavily styled `Label`.
  - If state classes or visibility were previously toggled on the `Label`, move or mirror that logic to the wrapper so behavior does not regress.
- Use `GameEvents` for server messages and `CustomNetTables` for synced state.
- Use localization keys (`#token_name`) for all player-facing text.
- Avoid global pollution; attach shared helpers to `GameUI` only when needed.

## WorldPanel Alignment Rules (Flow-Safe)

Use these rules whenever a worldpanel is anchored to entities and the visible content uses flow/text.

1) Alignment contract first
- Define one alignment owner panel (for example `BossHealthFrame`).
- Define fixed alignment size (`fixed_width`, `fixed_height`) for each variant (for example boss/elite).
- Define align policy (`hAlign`, `vAlign`) and lock it on both server and client.

2) Fixed geometry for anchor chain
- Any panel participating in anchor math must use explicit `width` and `height`.
- Do not use `fit-children` on the final aligned container.
- `flow-children` is allowed only inside non-anchor subtrees.
- For centered text inside an anchored panel, use a fixed-size wrapper panel as the anchor owner and keep the `Label` as a child responsible only for text layout.

3) Shared size resolver for worldpanel math
- Use one resolver in worldpanel positioning: `fixed > actual > desired`.
- Prefer `worldpanel_size_mode = "actual"` unless a task explicitly needs `desired`.
- If fixed size exists, always use it for panel width/height in anchor calculations.

4) Text isolation
- Keep labels in child containers that do not define anchor size.
- Treat text stroke, noclip, language length, and digit count changes as layout-risk inputs.
- Never let text desired size become the source of worldpanel anchor width.
- Do not put anchor-critical positioning, backgrounds, or state classes on the text `Label` when a wrapper panel can own them more stably.

5) Variant consistency
- Boss/Elite must share one alignment logic path and differ only by fixed size constants.
- Keep placement offsets (`entityHeight`, `offsetX`, `offsetY`) separate from panel geometry.

6) Required validation
- Check `dCenter.x` in debug logs: target `0 ± 1px`.
- `dCenter.y` may be a fixed non-zero value when UI is intentionally above the unit.
- Validate with value-length changes (`x9` -> `x10`), language changes, and resolution changes.

## Common Tasks

- Add a new window or panel: create a layout, include scripts/styles, then register in the manifest.
- Hook UI to game data: subscribe to a net table and update panels on change.
- Trigger server actions: call `GameEvents.SendCustomGameEventToServer` from UI interactions.

## References

- Panorama framework: `references/panorama-framework.md`
- Panorama API2: `references/panorama-api2.md`
- Replica alignment rules: `references/replica-alignment-rules.md`
- Standard mapping template: `references/mapping-template.json`
- Runtime dump collection template: `references/runtime-dump-template.md`

## Assets

- Base panel template: `assets/panorama-panel-template/`
- Worldpanel anchor template: `assets/worldpanel-anchor-template/`
- Replica shell template: `assets/replica-shell-template/`
