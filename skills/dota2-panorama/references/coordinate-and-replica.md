# Coordinate and replica contract

Use for Figma, draw.io, screenshots, or any request for strict visual reproduction.

Before this contract, complete the evidence brief and state matrix in `visual-delivery-loop.md`, then the prototype selection and mapping table in `dota2-page-archetypes.md`. The design artifact controls the regions it draws; a designated complete reference controls missing content/layout; the selected Dota page controls only still-unspecified visual treatment. A screenshot of the target alone does not justify a generic Dota-like restyle.

## Design-coverage gate

Before editing, inventory every visible requirement in a ledger:

| ID | Design evidence | Evidence owner | Required content/relation | Required layers/assets | Runtime owner | Panorama selectors | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `summary.badge` | crop and coordinates | target design | image under status value | exact verified badge resource | summary state | wrapper, image, label | mapped |

Use these evidence owners in descending priority:

1. **Target design:** owns all content, geometry, layering, and assets it visibly specifies.
2. **Designated complete-content reference:** owns content and layout absent from the target design.
3. **Selected Dota prototype:** owns visual treatment only where both higher-priority sources are silent.
4. **Existing implementation:** supplies reusable wiring only; it is never evidence that a visible requirement is already satisfied.

Split composed regions into separate ledger rows for background art, tint/mask, content, overlay, separator, and hit area. Record relations such as `left: image with overlaid number` and `right: top copy row over bottom progress bar`; listing only the outer rectangle is insufficient.

For recognizable Dota imagery, verify the exact resource identity from allowed source, VPK identity listing, or runtime evidence. A gradient, colored rectangle, glyph, or guessed filename is not an acceptable placeholder unless the user explicitly approves it.

Do not start implementation until all required rows are `mapped`. After editing, update each row through:

- `implemented`: XML/CSS/JS and real data/resource ownership are present;
- `source-checked`: the final cascade and panel tree cannot reintroduce superseded backgrounds, borders, offsets, or placeholders;
- `runtime-verified`: the current runtime screenshot matches the design relation and has no clipping, overlap, or unexplained drift.

If the user owns screenshot feedback, stop at `source-checked`, request the screenshot, and state that runtime verification remains pending. Never report “all design requirements implemented” when the ledger still contains `mapped`, `assumed`, or visually unverified rows.

## Geometry policy

Choose one design coordinate system and record design viewport, runtime viewport, scale policy, origin, safe area, and parent-relative transforms. Build parent, alignment, center, gap, distribution, and ratio relations before recording local coordinates.

Use fixed geometry for authored outer shells and independently placed design regions when the viewport contract requires it. Inside those regions, implement alignment through flow, stable slots, and parent alignment. Coordinates are measurements for validation, not a substitute for layout structure.

Do not combine anchor alignment and manual offsets on the same critical selector unless allowlisted. Avoid negative margins for alignment. `fit-children`, `fill-parent-flow`, and `100%` are valid only when their parent/remaining-space behavior is explicitly defined in the relation contract.

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
2. Classify the target and select a concrete Dota primary prototype.
3. Establish target-design, complete-reference, Dota-prototype, and existing-code precedence.
4. Build the design-coverage ledger, including every visible layer, exact asset, relation, state, and data owner.
5. Build the state/interaction matrix and target-to-prototype mapping table with evidence paths/selectors.
6. Preflight the complete selector cascade, shared includes, assets, localization, data, and render owners.
7. Extract relation contracts first, then authored geometry.
8. Map design IDs to Panorama selectors and direct parents.
9. Build the shell and region tree using the prototype's hierarchy and state ownership.
10. Add controlled adaptive content.
11. Implement prototype-backed surfaces, controls, typography, motion, and overflow.
12. Exercise every state in source logic and update coupled values from one owner.
13. Reconcile the final panel tree, resource paths, and CSS cascade against every ledger and state row.
14. Apply only final optical corrections.
15. When validation is authorized, run the checks in `validation.md`.
16. Compare runtime geometry and a final screenshot set with the target contract and prototype mapping.

For draw.io tasks, use the bundled extractor and mapping artifacts. A page-3 mapping view or relation sheet is required only when the task explicitly uses that established draw.io replica workflow.

## Dynamic content

Define a policy before implementation:

- fixed shell and headers;
- scrollable row/list regions for overflow;
- explicit rules for 1, 2, and 3+ item counts;
- stable geometry across win/lose and other state variants.

## Acceptance

- Authored outer bounds meet the agreed tolerance; internal acceptance prioritizes center, baseline, edge, gap, and distribution relations over independently tuned x/y offsets.
- Parent mappings match direct XML parent chains.
- Center, gap, and ratio relations pass.
- Required labels and art are not clipped.
- Overflow uses the declared policy.
- State variants preserve shell geometry.
- Runtime values and localized copy come from their real owners.
- Every critical visual region maps to the chosen Dota prototype or an explicitly named adaptation.
- Every visible target-design layer and relation is present; no recognizable resource is replaced by an unapproved synthetic approximation.
- The final CSS cascade has no later rule that restores a removed background, border, shadow, offset, or placeholder.
- Final screenshot has no unexplained design drift.

Do not claim “close enough” when any hard gate fails. Report blocked evidence or an explicitly approved deviation.
