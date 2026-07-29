---
name: dota2-panorama
description: Author and maintain Dota 2 Panorama source UI under an addon's content panorama directory using XML, CSS, and JS, and maintain a page-specific Dota 2 UI reference catalog. Use for layouts, styles, client behavior, CustomUIElement wiring, GameEvents, CustomNetTables, localization, WorldPanels, design replication, screenshot-feedback correction, or explicit vanilla UI reference research. For new visual design or replication, select a concrete Dota 2 page with matching function, layout, and hierarchy; for targeted corrections, preserve accepted regions. During addon implementation, never inspect compiled game Panorama artifacts; an explicit global reference-catalog research task may inspect/decompile vanilla .vxml_c/.vcss_c/.vjs_c under the evidence and isolation rules below.
---

# Dota 2 Panorama

Create and edit Panorama source while preserving runtime wiring and verified geometry.

## Hard gates

- Locate the matching file under `content/<addon>/panorama/...` before reading or editing UI.
- During addon UI implementation, never read, inspect, or decompile `game/<addon>/panorama/...` or any `_c` artifact. If matching addon source is absent, stop and report the expected source path.
- Exception: when the task explicitly builds or maintains the global Dota 2 UI reference-case catalog, vanilla `.vxml_c`, `.vcss_c`, and `.vjs_c` may be extracted and decompiled for research. Keep outputs outside every addon's source tree, label them as decompiled evidence, and do not copy them into an addon without a separate implementation task and source-level review.
- For a page design or redesign, select one primary Dota page archetype before editing. “Dota style”, a palette, or a mood board is not a prototype.
- For a targeted screenshot correction, freeze accepted regions and repair only the reported contract. Do not reopen the whole page design or replace its prototype unless the user explicitly requests a redesign.
- For a page-level screenshot, Figma, draw.io, or other design-artifact implementation, build a design-coverage ledger before editing. Account for every visible content region, relation, background/decor layer, exact asset, state, and data owner. A local screenshot correction uses the smaller delta contract instead.
- Apply evidence precedence explicitly: the target design owns every region it draws; a designated complete-content reference owns content/layout missing from the target design; the selected Dota prototype owns only visual treatment still unspecified by both. Never let an existing implementation override higher-priority evidence.
- Scale visual process to task size using `references/visual-delivery-loop.md`: use a delta contract for a local correction, a compact evidence/state contract for a component replica, and a full ledger/matrix for a page design. A partial design, complete-content reference, and Dota visual prototype are different owners; never merge their roles implicitly.
- Treat visible backgrounds, separators, masks, overlays, and image-under-text compositions as required structure, not optional polish. Verify exact resource identity for recognizable Dota art instead of substituting a synthetic block.
- Use relationship-first layout. Centering, distribution, and remaining-space placement must be owned by parent structure; do not simulate them with independent pixel offsets.
- Audit the final CSS cascade before every screenshot handoff. Do not accumulate append-only “final override” sections for the same component.
- Do not call a result an original-page replica unless the claimed hierarchy and visual rules are traceable to uncompiled source or directly observed runtime evidence.
- Respect the repository's validation policy. In projects that prohibit automatic Panorama syntax checks, do not run them unless the user explicitly requests them.
- Do not invent web CSS/API features. Verify fragile syntax against a working local source example.

## Workflow

1. Identify the UI load scope and existing source layout, style, script, manifest, localization, events, and net-table contracts.
2. Read the applicable reference:
   - ordinary layout or refactor: `references/layout-contracts.md`;
   - any visual design, screenshot, or reference-driven task: `references/visual-delivery-loop.md`;
   - Figma/draw.io/image replica: `references/coordinate-and-replica.md`;
   - any visual design or redesign: `references/dota2-page-archetypes.md`;
   - vanilla core-page prototype or catalog research: `references/dota2-decompiled-page-cases.md`;
   - entity-anchored panel: `references/worldpanel.md`;
   - validation requested or required by repo: `references/validation.md`.
3. Classify visual scope as local correction, component replica, or page design. Create only the contract required for that scope.
4. For a local correction, preserve accepted regions, identify the owning selector/function, and define the regression boundary. Reuse any existing prototype; do not select a new page prototype solely for the correction.
5. For a component replica, declare evidence roles and relevant component states, then select one component reference.
6. For a page design or redesign, classify shell, task, hierarchy, density, and dynamic behavior; select one primary prototype and at most two secondary component references.
7. For page-level design-artifact work, read `references/coordinate-and-replica.md`, complete its coverage ledger, and record `target region -> prototype region -> evidence -> retained rule -> adaptation`.
8. Preflight the loaded XML subtree, relevant CSS cascade, JS state owners, shared style includes, exact assets, localization tokens, and runtime data.
9. For Figma tasks, invoke the official `figma:figma-design-to-code` workflow before obtaining design context. Treat Figma as the target content/layout contract and the selected Dota page as the visual implementation contract.
10. Build the panel tree and relationship contract before local dimensions, spacing, and typography.
11. Keep XML declarative, CSS responsible for layout/visuals, and JS responsible for state/events/rendering.
12. Wire `custom_ui_manifest.xml` or the relevant include only when required.
13. Preserve runtime data and localization sources. Visible design text is not automatically an XML literal, and a plausible token name is not evidence that the token exists.
14. When structure is stable, update the smallest stable subtree for local interactions. For structural data changes, allow controlled rerendering while preserving stable shell, focus, scroll, and unrelated state.
15. Reconcile the applicable delta, component contract, or page ledger; inspect the final CSS cascade and resource paths; distinguish `source-checked` from `runtime-verified`.
16. Use one early structural smoke check when runtime behavior is uncertain, then batch source-complete visual changes before the final screenshot set.
17. Validate only according to project policy and the requested scope.

## Source conventions

- Use `.xml`, `.css`, and `.js` under `content/<addon>/panorama/`.
- Use `file://{images}/...` for addon images and `file://{resources}/...` for addon layout/style/script includes. Use `s2r://...` for compiled game resources.
- Convert KV `.vtex_c`/`.vsvg_c` paths to Panorama resource forms without the compiled suffix.
- Use localization tokens for player-facing copy.
- Verify a localization token exists before using or constructing it. Prefer an existing config/runtime field when no valid token exists.
- Use `GameEvents` for server messages and `CustomNetTables` for synchronized state.
- Avoid globals; expose shared helpers through `GameUI` only when genuinely shared.
- Use `$.GetContextPanel()` when the layout root is needed; the first actual panel under `<root>` must not have an `id`.
- Resolve external Dota roots through the host project's path resolver. Never encode a Steam library or user path in skill output.

## Dota visual evidence

- **A — source-backed:** uncompiled Valve XML/CSS/JS is available. Reuse its panel hierarchy, selectors, state model, dimensions, gradients, borders, and motion as applicable.
- **D — decompiled-reference-backed:** vanilla VPK artifacts were decompiled during an explicit reference-catalog task. Use them to document page hierarchy, selectors, properties, and state wiring, but label provenance and cross-check important visuals in the running client.
- **B — runtime-backed:** the page can be observed or captured and exact resource identity is known, but uncompiled source is absent. Reproduce only visible behavior and geometry; do not claim hidden implementation details.
- **C — inferred:** only an image or stylistic resemblance exists. Label the result as an adaptation, not an original-page replica.
- Outside an explicit reference-catalog task, use VPK listings only to identify and classify candidate pages.
- During an explicit reference-catalog task, inventory first, extract only the selected page family and its direct style/script dependencies, and record VPK path plus resource identity. Do not bulk-decompile unrelated Panorama resources.
- Check the VPK for raw `.xml`, `.css`, and `.js` before declaring source absent. If only `vxml_c`, `vcss_c`, or `vjs_c` exists, keep the page at identity-only evidence until runtime captures are obtained.
- If the primary prototype is D, B, or C, state the evidence limitation. D evidence still requires runtime visual comparison before claiming pixel fidelity.

## Design-to-Panorama contract

- Separate target content ownership from visual implementation ownership: the product/design document determines content and interaction; the selected Dota prototype determines shell, hierarchy, surfaces, control treatment, and state presentation.
- Preserve the primary prototype's information hierarchy. Do not mix unrelated page shells merely because individual colors or ornaments look useful.
- Secondary references may supply isolated controls only, such as a close button, tab strip, rarity row, or notification transition.
- Split composed views into background/decor, content, overlay, mask/clip, and interaction layers.
- Preserve visual hierarchy in the panel tree.
- Build frame/card elements as an outer shell plus dedicated decor and content children.
- Give avatars and cropped art a dedicated clip window.
- Use runtime bindings for account values, currency, status, and other live data.
- Use existing localization tokens for labels; do not paste Figma text into XML without deciding ownership.
- For independently positioned decorative groups, use fixed/absolute outer placement and flow only inside the group.
- Do not approximate a multi-region design by placing all children in one flow container and nudging margins.
- Use fixed coordinates only for authored outer bounds or independently positioned decorative layers. Implement center, baseline, equal-spacing, and remaining-space relationships through parent layout.

## Runtime behavior

- Keep one owner for each scroll axis.
- Prefer class toggles for finite image/state sets; reserve dynamic `backgroundImage` for truly open-ended paths.
- Use a fixed media wrapper plus verified aspect-preserving background rules for images at stretch risk.
- Separate stable wrapper geometry from label text rendering.
- When state/visibility previously lives on a label that becomes wrapped, move or mirror the behavior to the wrapper.
- Keep one render owner per state. Local toggles update classes, text, and assets in place so unrelated rows do not flash or lose focus.

## References

- `references/layout-contracts.md`: rounded shells, stable layers, layout templates, images, text, and scrolling.
- `references/visual-delivery-loop.md`: evidence roles, state matrix, relationship-first implementation, cascade audit, and screenshot-feedback convergence.
- `references/coordinate-and-replica.md`: coordinate systems, Figma/DZSJ mappings, strict replica pipeline, and acceptance criteria.
- `references/dota2-page-archetypes.md`: mandatory prototype-selection method and source-backed catalog of concrete Dota page implementations.
- `references/dota2-decompiled-page-cases.md`: page-specific D-evidence catalog for vanilla item details, progression, selection, probability, and report screens.
- `references/worldpanel.md`: fixed anchor geometry and flow-safe entity alignment.
- `references/validation.md`: optional syntax, static layout, runtime dump, and replica commands.
- `references/panorama-framework.md`: project framework notes.
- `references/panorama-api2.md`: API reference.
- `references/replica-alignment-rules.md`: compact alignment rules.

## Assets

- `assets/panorama-panel-template/`: base panel.
- `assets/worldpanel-anchor-template/`: entity anchor.
- `assets/replica-shell-template/`: fixed replica shell.

## Scripts

- `scripts/inventory-vpk-panorama.ps1`: read-only VPK source/candidate inventory. Run it before any narrowly scoped reference extraction.
