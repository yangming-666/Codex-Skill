# Structure Decision Model

Use this model after building the semantic and numerical model.

## Candidate structures

Always consider at least two:

- normalized: dimensions as key columns, measures as value columns;
- cross-tab: one dimension on rows, one grouped across columns, measures nested under groups;
- composite: canonical normalized data plus one or more linked comparison views;
- summary: explicit aggregation only.

## Apply vetoes before scoring

Reject a candidate immediately if it breaks a mandatory user operation, changes the evidence meaning, hides missing coverage, requires repeated sheet/section switching for the primary comparison, or adds an unrequested maintenance layer without operational value.

Examples:

- If one level must be compared across all qualities, splitting qualities into multiple vertical blocks or sheets fails even if each block is narrower.
- If two ordered dimensions jointly determine repeated measures for human reference, a long table fails unless filtering/import/editing is explicitly the primary operation.
- If estimates must not be mixed with facts, a layout without an evidence-state mechanism fails even if compact.
- If evidence metadata triples every value column when a legend or cell-level mark is sufficient, the layout fails information-density and scope discipline.
- If the user only needs one comparison view, a composite workbook fails scope discipline unless a second layer is necessary for audit or implementation.

## Score surviving candidates

Score 0–3 and record the reason:

| Criterion | 0 | 3 |
|---|---|---|
| Answers the requested decision | indirect or ambiguous | immediate |
| Lookup/filter/import | impractical | direct and stable |
| Side-by-side comparison | difficult | visually immediate |
| Completeness visibility | missing keys are hidden | coverage is obvious |
| Numerical auditability | transformations obscure | keys and formulas traceable |
| Scalability | requires redesign | extends predictably |
| Maintenance risk | manual duplication | single controlled truth |
| Visual scanability | weak hierarchy | clear groups and reading path |
| Scope discipline | extra fields/sheets | only required content |

Weight the criteria from the requirement contract. Scores rank only candidates that passed every veto.

## Relationship rules

- Keep a field as a key dimension only if it can change a required measure or the user needs that breakdown.
- If a category changes one measure but not the others, compare three representations: dedicated measure column, category dimension, separate relation. Choose by required lookup and comparison behavior.
- A merged header is presentation, not data modeling.
- A simple shape is not inherently better. A complex shape is justified only when it reduces user effort or ambiguity.
- Never choose a structure by analyzing only one convenient level or tier when the requested grain includes the full dimension.
- Inspect or use a reference layout only when it is an authorized input. In capability tests, exclude prior solutions and reference workbooks unless the user explicitly includes them.

## Composite workbook rule

Use a composite workbook only when distinct operations genuinely require distinct shapes. The canonical table owns values. Comparison views must be formula-driven or deterministically generated from the same model. Validate key counts and values between views.
