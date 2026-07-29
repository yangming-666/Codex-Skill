# Panorama visual delivery loop

Use this reference for any screenshot-, design-, or reference-driven Panorama UI.

## 1. Choose process depth

Use the lightest process that protects the requested result:

- **Local correction:** one reported defect or a small related set. Record `issue -> expected relation/state -> owner -> regression boundary`.
- **Component replica:** one reusable control or secondary modal. Record a compact evidence brief and only its relevant states.
- **Page design:** a new page, substantial redesign, or multi-region replica. Build the full evidence brief, coverage ledger, prototype mapping, and state matrix.

Do not promote a local correction into a redesign. Do not skip the full contract for a page-level implementation.

## 2. Evidence brief

Write one brief before editing:

| State/region | Content and interaction owner | Layout owner | Visual owner | Exact assets/data | Explicit exclusions |
| --- | --- | --- | --- | --- | --- |
| summary region | product specification | target design | selected Dota prototype | verified paths and runtime fields | unapproved reference styling |

Rules:

- A design can be partial. It owns only what it actually draws.
- A designated complete reference fills missing content and layout, not visual style unless requested.
- A Dota prototype fills only visual decisions still unspecified.
- The current implementation is wiring evidence, never design evidence.
- Give each independently visible surface or behavior its own row when it has a different evidence owner.

If the user's explanation changes an evidence role, update the brief before touching code. Do not continue from the earlier interpretation.

## 3. State and interaction matrix

For component and page work, select relevant state dimensions:

- visibility and expansion;
- selection, navigation, and pagination;
- enabled, disabled, available, and unavailable;
- empty, loading, populated, and error data;
- current, minimum, maximum, and other meaningful data variants;
- focus, hover, active, submit, cancel, and repeated interaction;
- initial render, local update, and asynchronous response.

For each state record:

- visible regions and text format;
- asset and class selection;
- enabled and hit-test behavior;
- data owner;
- whether the shell geometry must remain stable;
- smallest panel subtree that should update.

Switching state must update every coupled value. A selection that changes its heading but leaves dependent description, controls, or values stale is incomplete.

## 4. Source preflight

Before visual editing:

1. Read the affected XML subtree, every CSS definition for critical or changed selectors, the owning JS render/update functions, includes, and localization/data sources.
2. Build a selector ownership list. Mark the final rule in cascade order for every critical selector.
3. Verify required shared styles such as `dotastyles.vcss_c` before judging fonts or shared controls.
4. Verify every referenced asset exists. Do not guess filenames or generate a substitute when an exact supplied or Dota asset is required.
5. Verify localization tokens exist before calling `$.Localize`. Never construct speculative token names.
6. Separate invalid property planes: XML/JS properties such as `hittest` do not belong in VCSS.

Do not blame compilation, caching, or stale runtime state without a concrete console/load error. In auto-compiling Panorama workflows, a bad result is implementation evidence until logs prove otherwise.

## 5. Relationship-first layout

Implement relationships through parents:

- centered group: parent owns width; group uses `horizontal-align: center`;
- vertically centered row: stable row height; every icon and text wrapper uses `vertical-align: center`;
- centered control with an asymmetric side action: use equal left/right side slots or overlay the side action outside flow;
- action centered in remaining space: make the remaining-space wrapper the layout owner, then center the action inside it;
- left object plus right stacked content: horizontal parent with separate left and right owners; the right owner flows down;
- label and icon: give both stable wrappers and center them; do not compensate with unrelated top margins.

Use pixels for authored sizes, gaps, and outer bounds when evidence provides them. Do not use independent `position`, negative margins, or one-off offsets to simulate centering or alignment. Coordinates verify relationships; they do not replace them.

Apply an optical correction only after structural centering is correct, document the correction, and keep it local.

## 6. Exact-reference implementation

When a concrete Dota source is selected:

1. Reproduce its semantic hierarchy first.
2. Retain its surfaces, spacing, typography, separators, controls, and states unless the evidence brief explicitly replaces them.
3. Override only named differences.
4. Compare every retained property group with the source. “Same colors” is not enough if padding, row borders, background art, shadow, arrow geometry, or state behavior differs.

Reuse shared classes only when they are loaded, supported in addon scope, and free of selector conflicts. Otherwise implement the verified visual contract under project-namespaced classes. Preserve small structural details such as separators, full-width text centering, overlaid affordances, and secondary-modal spacing.

## 7. Implementation and cascade discipline

- Edit the existing semantic rule instead of appending a new restyle block when possible.
- Never leave multiple “final”, “targeted replica”, or temporary override sections for the same component.
- If iteration creates a second override for a critical selector, consolidate that selector before handoff.
- After each edit, search all definitions of every changed selector and resource path. The last applicable rule must express the intended result.
- Removing a background requires auditing the shell, image, rarity layer, sheen, border, shadow, and the source bitmap itself.
- Keep placeholder assets, fallback glyphs, and generated images out of accepted paths unless explicitly approved.

## 8. Interaction discipline

- When structure is stable, update the smallest stable subtree that owns the changed state.
- When collection shape or template structure changes, allow controlled rerendering while preserving the stable shell, focus, scroll, and unrelated state.
- Keep hover/active feedback on the interactive control, not its whole row, unless the reference does so.
- Preserve focus, dropdown position, and shell geometry across local interactions.
- Represent independently styled values and affordances as separate semantic nodes instead of concatenated text.

## 9. Source check before screenshot

Check the applicable delta, component state contract, or page state matrix, not only the default state:

- no overlap, clipping, unexplained border, or incomplete text;
- centers, baselines, edge alignment, and spacing relations hold;
- exact assets and fonts load from verified sources;
- resource formats and colors match the contract;
- state changes update coupled content;
- referenced controls and secondary surfaces match their own contracts;
- repeated interaction does not flash or move unrelated content;
- console warnings introduced by the UI are resolved.

When runtime behavior or panel structure is uncertain, perform one early smoke check before detailed styling. After structure is confirmed, batch source-complete changes and request one final screenshot set covering the affected states. Avoid repeated one-property Computer Use round-trips unless diagnosing a runtime-only defect.

## 10. Feedback convergence

Turn screenshot feedback into a delta list:

| Issue | State | Expected relation/content | Owning selector/function | Root cause | Fix status |
| --- | --- | --- | --- | --- | --- |

Rules:

- Fix the stated issue without redesigning accepted regions.
- Group issues by common owner; solve alignment defects at the parent/layout contract, not per child.
- Recheck previously accepted requirements after every cascade or panel-tree change.
- Report `source-checked` separately from `runtime-verified`.
- Do not claim completion while any reported issue remains unaccounted for.
