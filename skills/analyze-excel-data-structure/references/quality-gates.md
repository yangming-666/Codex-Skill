# Delivery Quality Gates

All applicable gates must pass.

## Source gate

- all inspected inputs were explicitly authorized;
- capability tests exclude prior solutions and reference artifacts unless explicitly authorized;
- authoritative and reference inputs are distinguished;
- every requested measure has field-level lineage;
- unresolved raw references remain explicit;
- no reference workbook is silently treated as source truth.

## Semantic gate

- grain is stated;
- candidate key is unique;
- the authoritative field for each requested measure is selected explicitly;
- auxiliary encoded fields do not downgrade an explicitly stored requested measure;
- functional dependencies are verified with actual values;
- every member of a collapsed candidate dimension is enumerated and tested or explicitly marked unobserved;
- exceptional categories are represented intentionally;
- units and resource identities are unambiguous.

## Completeness gate

- expected key set comes from authoritative rules;
- the analyzed and presented domain preserves every requested dimension and coverage interval;
- a baseline level, representative tier, or observed subset is not substituted for full requested coverage;
- observed, missing, unsupported, and unresolved keys are counted separately;
- blank rows are not deleted to inflate completeness;
- output is not called complete while required values are unresolved.

## Numerical gate

- formulas, multipliers, rounding, caps, and probabilities are verified;
- curves and breakpoints are checked;
- direct, derived, inferred, and unavailable values are not silently mixed;
- duplicate or conflicting authoritative values are resolved or reported.

## Inference gate

- inferred values were explicitly permitted;
- a structural or causal basis exists beyond visual trend fitting;
- holdout or independent validation was performed where authoritative points exist;
- competing plausible models and extrapolation distance were considered;
- a category with zero observations is not presented as exactly completed;
- estimated and unavailable values remain distinguishable from direct and resolved values.

## Structure gate

- at least two candidate layouts were evaluated;
- chosen layout supports every mandatory user operation;
- canonical and presentation views reconcile to the same key/value set;
- dimension cardinalities, expected key combinations, data-cell count, and final row/column count reconcile arithmetically;
- grouped-column width equals key columns plus group count multiplied by measures per group;
- unrequested fields and sheets are absent.

## Operation gate

- the primary lookup/comparison/edit/import path is stated;
- the structure minimizes sheet switches, section switches, filters, and mental joins for that path;
- two ordered dimensions with repeated measures use a continuous cross-tab for human reference unless another primary operation is explicit;
- mandatory continuous comparisons are not split to optimize width alone;
- a composite workbook exists only when distinct mandatory operations justify it.

## Information-density gate

- evidence state is visible but does not duplicate status and basis columns for every measure when a compact encoding is sufficient;
- the main table contains the requested numerical reference, not an audit report disguised as a data table;
- supporting detail exists only when interpretation or implementation genuinely requires it.

## Visual gate

- every user-facing sheet was rendered and inspected;
- grouped dimensions have obvious hierarchy;
- comparison groups use consistent, distinguishable styling;
- merged cells, when used, are limited to presentation headers;
- row keys remain visible with frozen panes;
- widths, wrapping, alignment, borders, units, and number formats are readable;
- result matches or exceeds the supplied reference in scanability and information density.

## File gate

- formula error scan is clean;
- exported workbook re-imports;
- OpenXML parses and every sheet relationship is valid;
- no Excel repair log is produced;
- final artifact is the requested workbook, not an intermediate variant.

## Failure rule

Source, semantic, inference, operation, and file gates are veto gates. They cannot be offset by formatting quality or a high structure score. If any mandatory gate fails, do not deliver as final. Continue, label the artifact as incomplete, or report the exact blocker.
