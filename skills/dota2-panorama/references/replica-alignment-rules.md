# Replica Alignment Rules

Use this reference for strict draw.io-to-Panorama replication.

## 1) Geometry Contract

Define contract with `extract_drawio_contract.py`, then maintain:

- `x`, `y`, `width`, `height`
- `selector`
- optional `parent_selector`

For child panels, validate position in parent-relative coordinates.

## 2) Relationship Constraints

In addition to raw geometry, define relation rules:

- `center_x(A) == center_x(B)`
- `center_y(A) == center_y(B)` when needed
- `width(A) == width(B)` when design requires equal width
- `group_bbox([A,B,C]) centered in P`
- `left(A) == left(B)` / `right(A) == right(B)` when edge alignment is required

## 3) Outer/Inner Layout Split

- Outer shell (design-critical): fixed px geometry only.
- Inner content slots: controlled adaptive rules only.

Examples:

- Rewards shell fixed.
- Diamond group fixed slots.
- Normal rewards adaptive 1/2/N + scroll.

## 4) Runtime Validation

Static checks are necessary but insufficient.
Collect runtime geometry via `dump_runtime_layout.js` and compare against contract.

Required runtime cases:

- victory + first clear
- victory + non-first clear
- defeat
- normal rewards count: 1, 2, 3+

## 5) Scrollbar Policy

- Scrollbars appear only when content overflows.
- Do not show scrollbars for non-overflow cases in baseline screenshots.

## 6) Replica Completion Criteria

All must pass:

- static checker pass
- runtime geometry pass
- visual comparison pass (no obvious layout drift)
