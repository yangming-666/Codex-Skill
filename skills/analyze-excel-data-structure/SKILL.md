---
name: analyze-excel-data-structure
description: Analyze game numerical, config, unpacked, or runtime data; infer system rules, field relationships, functional dependencies, evidence strength, and player-economy implications; then design or audit implementation-ready Excel workbooks. Use for 游戏数值策划、配置表整理、解包数据分析、等级×品质/成本/奖励/属性对照、缺失数据考据与补全、曲线和经济验证、根据字段关系决定Excel行列结构，或检查数值表的完整性、可读性、可追溯性与策划可用性。Trigger for requests such as “整理这个数值表”“分析字段后决定表结构”“用解包数据生成Excel”“补齐品质数据并找证据”“检验这个数值表是否合理”, even without an explicit Skill name.
---

# Senior Game Numerical Planning to Excel

Formatting is the final expression of a correct numerical model, never proof of one. Do not author a workbook until the analysis gates below pass.

## Required references

Read [references/senior-planner-reasoning.md](references/senior-planner-reasoning.md) before analyzing values. Read [references/decision-model.md](references/decision-model.md) before choosing a workbook structure. Read [references/quality-gates.md](references/quality-gates.md) before delivery. Use [references/evaluation-cases.md](references/evaluation-cases.md) when revising or auditing this Skill.

## 1. Lock scope and isolate evidence

Write an internal requirement contract:

```text
question/decision the data must answer:
required dimensions and measures:
units and expected coverage:
mandatory user operations and comparison path:
authorized inputs:
inference permission and acceptable uncertainty:
requested deliverable only:
```

Treat any input not explicitly authorized as out of scope. During a capability test, do not inspect a prior solution, reference workbook, screenshot, or generated report unless the user explicitly authorizes it as test input. A visual reference can contaminate structure reasoning even when no numbers are copied.

Do not add dimensions, measures, sheets, explanations, or provenance columns unless they serve the contract.

Never reduce requested coverage to a convenient sample, baseline level, representative tier, or observed subset. Samples may support analysis, but the decision record and final structure must preserve the full requested dimension domain. If coverage intent is genuinely ambiguous and changes the structure, state the ambiguity and obtain clarification or make one explicit reversible assumption.

## 2. Establish source authority and lineage

Classify every authorized input:

1. authoritative: raw config, decoded table, runtime dump, executable rule;
2. resolved evidence: reproducible transformation from authoritative data;
3. contextual: design document or user-confirmed rule;
4. reference: manually organized workbook, screenshot, or report;
5. target: artifact to create or edit.

Build field-level lineage for every requested measure. Never promote reference or contextual material to numerical truth. If an encoded pointer, formula, unit, resource identity, or expected key cannot be resolved, preserve the uncertainty.

Select the authoritative field that directly represents each requested measure before consulting auxiliary implementation fields. If the requested player-facing output is explicitly stored, its values are direct even when an alternative lower-level representation is encoded. Auxiliary fields may corroborate or explain a direct measure but must not downgrade its evidence state.

## 3. Build the system model before the table model

Profile actual records and determine:

- dimensions, measures, identifiers, units, and metadata;
- the smallest unique key for every measure;
- functional dependencies proven by duplicate/group comparison;
- complete member lists for every candidate dimension, with each retained or collapsed member accounted for;
- exceptional categories that genuinely change a required measure;
- formulas, multipliers, probabilities, rounding, caps, unlocks, tiers, and breakpoints;
- expected keys from system rules versus observed keys from extracted records;
- player-facing meaning: source, sink, progression pace, marginal gain/cost, refund rate, and boundary behavior where applicable.

Remove a candidate dimension only after proving it does not change any required measure and is not required for lookup or comparison. Represent one exceptional category as a dedicated measure when that reduces redundant dimensionality and matches the user's query path.

Do not generalize from a subset of dimension members. Before collapsing a dimension, enumerate its full authoritative domain, test every ordinary member, identify every exception, and report any unobserved member separately.

## 4. Apply the inference admission gate

Classify each value as `direct`, `resolved`, `estimated`, or `unavailable`.

- `direct`: the requested measure is explicitly stored in authoritative evidence; corroborating it with another field does not change it to resolved;
- `resolved`: the requested measure is deterministically calculated or decoded from direct evidence by a verified rule;
- `estimated`: the result depends on a model and carries uncertainty;
- `unavailable`: evidence does not justify a value.

An estimate may enter a user-facing table only when the user permits inference and all of these hold:

- a causal or structural rule is identified, not merely a visually plausible trend;
- the model is tested on withheld authoritative points or equivalent independent evidence;
- competing models are compared and material ambiguity is reported;
- extrapolation distance, error, rounding, breakpoints, and confidence are recorded;
- the estimate is visually and structurally distinguishable from facts.

Fitting known points is not validation. An adjacent-quality ratio, regression with no holdout, or a rule reused for a quality with zero observations cannot produce an “exact” or “complete” value. Keep such values unavailable or in a separate scenario area, never silently in the primary fact table.

Completeness means complete accounting of expected, observed, unsupported, unresolved, and unavailable keys—not filling every cell.

## 5. Decide the workbook structure from operations

Generate at least two viable structures and use [references/decision-model.md](references/decision-model.md). Mandatory operations are veto conditions, not soft score weights.

- normalized table: exact lookup, filtering, import, maintenance;
- cross-tab: repeated side-by-side comparison across dimensions;
- composite: only when distinct required operations genuinely need distinct shapes;
- summary: only for requested aggregation.

Preserve the user's comparison path. If users must compare every category for one row key, keep those categories in one continuous view; do not split them across sections or sheets merely to reduce width. Do not create a canonical/detail/parameter sheet automatically when the requested result is one comparison table and auditability can be retained without extra sheets.

For a human-facing table where two finite ordered dimensions jointly determine several repeated measures and the request is to view “corresponding values”, compare them, or make a numerical reference table, prefer one cross-tab: put the dimension with more values on rows and group the other dimension across columns with measures nested beneath it. A normalized long table may replace this only when filtering, import, editing records, or machine processing is explicitly the primary operation. Width alone cannot overturn this rule.

Record why the rejected structures fail the mandatory operations before authoring.

Reconcile structure arithmetic before authoring. Compute expected key combinations, data cells, rows, and columns from dimension and measure cardinalities, then verify them independently against the proposed range. For a cross-tab:

```text
data rows = row-dimension members
data columns = row-key columns + column-dimension members × measures per group
data cells = expected key combinations × measures
```

Any mismatch, including an off-by-one header/key column, is a veto failure.

## 6. Engineer only the approved structure

For canonical data, use one header row, one row per verified key, typed numeric values, stable keys, filters, auditable formulas, and no merged body cells.

For comparison views, use grouped multi-row headers when dimensions contain repeated measures, merge only group headers, visually separate adjacent groups, anchor the row key, preserve information density, and encode fact/estimate/unavailable states without obscuring numbers.

Keep evidence metadata compact. Prefer a legend plus cell fill, note, or comment over repeating `value / state / basis` beside every measure. Add detailed lineage columns or a separate audit area only when the user requests it or when the value cannot be interpreted safely without it.

Use formatting to express hierarchy and evidence state. Never use formatting to conceal missing coverage or compensate for a weak model.

## 7. Fail closed

Run every gate in [references/quality-gates.md](references/quality-gates.md). Reconcile all views to the same verified model, render every user-facing sheet, re-import the export, scan formulas, and validate OpenXML.

If any analysis, inference, operation, or file gate fails, do not deliver a final artifact. Continue investigating, deliver an explicitly incomplete evidence table if requested, or report the precise blocker.

Use the spreadsheet artifact tool for workbook authoring and rendering. Deliver only the requested artifact.
