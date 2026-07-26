# Coordinate and replica contract

Use for Figma, draw.io, screenshots, or any request for strict visual reproduction.

## Freeze coordinates

Choose one design coordinate system and record design viewport, runtime viewport, scale policy, origin, safe area, and parent-relative transforms. Build an `id -> parent, x, y, width, height` contract plus alignment, gap, and ratio relations before CSS.

Critical outer shells and regions use fixed geometry. Adaptive layout is allowed only inside explicitly named content slots.

Do not combine anchor alignment and manual offsets on the same critical selector unless allowlisted. Avoid negative margins, `fit-children`, `fill-parent-flow`, or `100%` on design-critical geometry.

## Figma/DZSJ translation

For Figma, first use the official design-to-code workflow to obtain design context and screenshots. Then:

- map background/decor, content, overlay, mask, and hit-area layers;
- use independent positioned groups for independently placed HUD/start/meta-growth regions;
- use flow only within a group;
- model currency chips as shell -> decor -> content row -> icon/value wrappers;
- model profile cards with explicit avatar clip, name, level, and EXP wrappers;
- position navigation buttons independently when their design baselines/heights differ;
- resolve every text node to runtime data, localization, embedded art, or an explicitly temporary stub.

## Replica pipeline

1. Capture design context and screenshots.
2. Extract geometry and relation contracts.
3. Map design IDs to Panorama selectors and direct parents.
4. Build the fixed shell and region tree.
5. Add controlled adaptive content.
6. Implement typography and overflow.
7. Apply only final optical corrections.
8. When validation is authorized, run the checks in `validation.md`.
9. Compare runtime geometry and a final screenshot with the contract.

For draw.io tasks, use the bundled extractor and mapping artifacts. A page-3 mapping view or relation sheet is required only when the task explicitly uses that established draw.io replica workflow.

## Dynamic content

Define a policy before implementation:

- fixed shell and headers;
- scrollable row/list regions for overflow;
- explicit rules for 1, 2, and 3+ item counts;
- stable geometry across win/lose and other state variants.

## Acceptance

- Critical x/y/w/h values meet the agreed tolerance (default ±2 px for strict replicas).
- Parent mappings match direct XML parent chains.
- Center, gap, and ratio relations pass.
- Required labels and art are not clipped.
- Overflow uses the declared policy.
- State variants preserve shell geometry.
- Runtime values and localized copy come from their real owners.
- Final screenshot has no unexplained design drift.

Do not claim “close enough” when any hard gate fails. Report blocked evidence or an explicitly approved deviation.
