---
name: dota2-panorama
description: Author and maintain Dota 2 Panorama source UI under an addon's content panorama directory using XML, CSS, and JS. Use for layouts, styles, client behavior, CustomUIElement wiring, GameEvents, CustomNetTables, localization, WorldPanels, or design replication from Figma, draw.io, or images. Never inspect compiled game panorama artifacts or files ending in _c; stop when matching source is missing. For design replication, require an explicit coordinate/layout contract and evidence-backed validation.
---

# Dota 2 Panorama

Create and edit Panorama source while preserving runtime wiring and verified geometry.

## Hard gates

- Locate the matching file under `content/<addon>/panorama/...` before reading or editing UI.
- Never read, inspect, decompile, or infer from `game/<addon>/panorama/...` or any `_c` artifact.
- If matching source is absent, stop and report the expected source path.
- Respect the repository's validation policy. In projects that prohibit automatic Panorama syntax checks, do not run them unless the user explicitly requests them.
- Do not invent web CSS/API features. Verify fragile syntax against a working local source example.

## Workflow

1. Identify the UI load scope and existing source layout, style, script, manifest, localization, events, and net-table contracts.
2. Read the applicable reference:
   - ordinary layout or refactor: `references/layout-contracts.md`;
   - Figma/draw.io/image replica: `references/coordinate-and-replica.md`;
   - entity-anchored panel: `references/worldpanel.md`;
   - validation requested or required by repo: `references/validation.md`.
3. For Figma tasks, invoke the official `figma:figma-design-to-code` workflow before obtaining design context. Translate the resulting design hierarchy into Panorama; do not introduce a second Figma-specific Panorama workflow.
4. Build the panel tree and geometry contract before local spacing and typography.
5. Keep XML declarative, CSS responsible for layout/visuals, and JS responsible for state/events/rendering.
6. Wire `custom_ui_manifest.xml` or the relevant include only when required.
7. Preserve runtime data and localization sources. Visible design text is not automatically an XML literal.
8. Validate only according to project policy and the requested scope.

## Source conventions

- Use `.xml`, `.css`, and `.js` under `content/<addon>/panorama/`.
- Prefer `file://{resources}/...` for addon assets and `s2r://...` for compiled game resources.
- Convert KV `.vtex_c`/`.vsvg_c` paths to Panorama resource forms without the compiled suffix.
- Use localization tokens for player-facing copy.
- Use `GameEvents` for server messages and `CustomNetTables` for synchronized state.
- Avoid globals; expose shared helpers through `GameUI` only when genuinely shared.
- Use `$.GetContextPanel()` when the layout root is needed; the first actual panel under `<root>` must not have an `id`.

## Design-to-Panorama contract

- Split composed views into background/decor, content, overlay, mask/clip, and interaction layers.
- Preserve visual hierarchy in the panel tree.
- Build frame/card elements as an outer shell plus dedicated decor and content children.
- Give avatars and cropped art a dedicated clip window.
- Use runtime bindings for account values, currency, status, and other live data.
- Use existing localization tokens for labels; do not paste Figma text into XML without deciding ownership.
- For independently positioned decorative groups, use fixed/absolute outer placement and flow only inside the group.
- Do not approximate a multi-region design by placing all children in one flow container and nudging margins.

## Runtime behavior

- Keep one owner for each scroll axis.
- Prefer class toggles for finite image/state sets; reserve dynamic `backgroundImage` for truly open-ended paths.
- Use a fixed media wrapper plus verified aspect-preserving background rules for images at stretch risk.
- Separate stable wrapper geometry from label text rendering.
- When state/visibility previously lives on a label that becomes wrapped, move or mirror the behavior to the wrapper.

## References

- `references/layout-contracts.md`: rounded shells, stable layers, layout templates, images, text, and scrolling.
- `references/coordinate-and-replica.md`: coordinate systems, Figma/DZSJ mappings, strict replica pipeline, and acceptance criteria.
- `references/worldpanel.md`: fixed anchor geometry and flow-safe entity alignment.
- `references/validation.md`: optional syntax, static layout, runtime dump, and replica commands.
- `references/panorama-framework.md`: project framework notes.
- `references/panorama-api2.md`: API reference.
- `references/replica-alignment-rules.md`: compact alignment rules.

## Assets

- `assets/panorama-panel-template/`: base panel.
- `assets/worldpanel-anchor-template/`: entity anchor.
- `assets/replica-shell-template/`: fixed replica shell.
