---
name: dota2-panorama
description: Dota 2 Panorama UI authoring and maintenance. Use when creating or modifying Panorama layout (VXML), styles (VCSS), or scripts (VJS), wiring CustomUIElement entries, or integrating GameEvents/CustomNetTables/localization in any Dota 2 custom game UI.
---

# Dota2 Panorama

## Overview

Create, edit, and debug Dota 2 Panorama UI with the correct syntax, file types, runtime APIs, and manifest wiring.

## Core Workflow

1) Identify the UI scope
- Decide if this is a new panel, a change to an existing panel, or a new full-screen view.
- Determine where it should load (Hud, HeroSelection, GameSetup, EndScreen).

2) Update layout (VXML)
- Add or edit the panel tree and classes.
- Include required scripts and styles in the layout file.

3) Update styles (VCSS)
- Add or modify class rules, leveraging variables and gradients where needed.
- Avoid relying on unsupported CSS features; keep to Panorama-compatible syntax.

4) Update scripts (VJS)
- Bind events, wire GameEvents or CustomNetTables, and manipulate panels.
- Keep UI logic client-side; server communication via custom game events only.

5) Wire the manifest
- Ensure the layout is registered in the UI manifest with the correct CustomUIElement type.

## Guidelines

- Prefer `file://{resources}/...` for local development assets and `s2r://...` for compiled resources.
- Edit source files under `content/<addon>/panorama/...` (`.xml`, `.js`, `.css`); avoid editing compiled files under `game/<addon>/panorama/...` (`.vxml_c`, `.vjs_c`, `.vcss_c`).
- If only compiled files appear, locate the source in `content/` and rebuild; do not patch `_c` files directly except as a last-resort with explicit user approval.
- The root panel inside a `layout` file must not include an `id` attribute; use `class` and assign `id` on child panels instead.
- For image sources from KV paths, use `s2r://(path in kv).vtex` with no `_c`, e.g. `src="s2r://panorama/images/heroes/selection/npc_dota_hero_invoker_persona1_png.vtex"`.
- For item icons specifically, use `s2r://panorama/images/items/<item_name>_png.vtex`.
- When normalizing image paths in JS, handle `.vtex_c` → `.vtex` and `.vsvg_c` → `.vsvg`, and avoid appending `.vtex` to SVG paths.
- To preserve image aspect ratio safely across Panorama builds, prefer a `Panel` with `background-image` + `background-size: contain` + `background-repeat: no-repeat` + `background-position: center`; avoid relying on `scaling` when parser warnings appear.
- Keep layout files declarative; move behavior to scripts.
- Use `GameEvents` for server messages and `CustomNetTables` for synced state.
- Use localization keys (`#token_name`) for all player-facing text.
- Avoid global pollution; attach shared helpers to `GameUI` only when needed.

## Text Centering

For the simplest case where text must be centered both horizontally and vertically inside a fixed-size container, use a fixed-height parent and let the label fill the width while using `vertical-align: center`.

```css
.TitleWrap {
    width: 360px;
    height: 80px;
}

.TitleLabel {
    width: 100%;
    height: fit-children;
    text-align: center;
    vertical-align: center;
}
```

Notes:
- Horizontal centering comes from `width: 100%` + `text-align: center`.
- Vertical centering comes from the parent having an explicit `height` and the label using `height: fit-children` + `vertical-align: center`.
- If the parent height is not fixed, vertical centering will often be unstable or ineffective.

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

3) Shared size resolver for worldpanel math
- Use one resolver in worldpanel positioning: `fixed > actual > desired`.
- Prefer `worldpanel_size_mode = "actual"` unless a task explicitly needs `desired`.
- If fixed size exists, always use it for panel width/height in anchor calculations.

4) Text isolation
- Keep labels in child containers that do not define anchor size.
- Treat text stroke, noclip, language length, and digit count changes as layout-risk inputs.
- Never let text desired size become the source of worldpanel anchor width.

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

- Panorama framework details and patterns: `references/panorama-framework.md`
- Panorama JavaScript API2 overview: `references/panorama-api2.md`

## Assets

- Base panel template (layout/script/style): `assets/panorama-panel-template/`
- Worldpanel anchor-safe template (layout/style/script/server snippet): `assets/worldpanel-anchor-template/`
