# Behavioral Evaluation Cases

Use these cases to test reasoning, not to prescribe a fixed schema. Pass only when the result explains its source authority, semantic model, candidate structures, chosen design, and failed/cleared quality gates.

## Trigger regression

The Skill should trigger for explicit invocation and for concise requests whose real task is game-data modeling plus spreadsheet structure, including:

- “整理这个手游数值表”；
- “根据这些字段分析关系，决定Excel行列”；
- “制作等级、品质对应攻击力和分解资源的表”；
- “把解包配置整理成可读的策划Excel”；
- “这个配置表数据全不全，结构合理吗”；
- “补齐品质11–14并区分实测和推测”；
- “简单表还是复合表，分析数据后决定”。

The Skill should not trigger for unrelated spreadsheet work with no game-numerical modeling or structure decision, such as changing one cell color, translating worksheet text, or calculating a generic household budget.

## Case A: raw evidence plus polished reference

Inputs include authoritative decoded records and a manually organized workbook. The workbook is visually strong but incomplete.

Pass behavior:

- use decoded records for numerical truth;
- use the workbook only for terminology and visual benchmark;
- report authoritative coverage independently from the reference;
- do not fill raw gaps from the reference without explicit evidence.

If the task is explicitly a clean capability test, pass behavior changes: do not inspect the reference at all unless the user authorizes it as an input to the test.

## Case B: two dimensions, several measures, one exceptional category

Most categories share one measure value; one category differs only for that measure. Users need exact lookup and cross-dimension comparison.

Pass behavior:

- verify the difference with actual records;
- evaluate dedicated measure, category dimension, and separate relation;
- avoid carrying an irrelevant category into every row;
- choose a composite workbook when lookup and comparison both matter;
- reconcile canonical and presentation values.

## Case C: sparse multidimensional coverage

Some dimension combinations are observed, some unsupported by rules, and some unresolved due to missing extraction.

Pass behavior:

- derive expected keys from authoritative rules;
- separate observed, unsupported, missing, and unresolved counts;
- preserve required keys without inventing measures;
- refuse to label the artifact complete while required keys are unresolved.

## Case D: comparison-heavy presentation

A reference cross-tab uses grouped headers, distinct group colors, frozen row keys, and compact numeric density.

Pass behavior:

- evaluate the reference's scan path and useful visual grammar;
- use merged presentation headers when they clarify hierarchy;
- apply consistent distinguishable group styling;
- render and compare the result;
- fail the visual gate if the new view is less readable than the benchmark even when the values and XML are valid.

## Case E: simple one-dimensional progression

One key determines all measures and users only need editing and lookup.

Pass behavior:

- choose one simple table;
- do not create a cross-tab, extra analysis sheet, or decorative hierarchy;
- keep the schema minimal and typed.

## Case F: unseen target tier

Direct attack values exist for earlier tiers, partial values exist for one tier, and the next tier has zero attack records. A regression fits the partial tier closely.

Pass behavior:

- distinguish interpolation, within-regime extrapolation, and extrapolation to an unseen tier;
- use holdout tests for the partial tier;
- refuse to call the unseen tier exact or complete without independent structural evidence;
- keep unsupported values unavailable or place user-authorized scenarios outside the primary fact table;
- do not treat a maximum error on training points as validation.

## Case G: continuous comparison versus width

Users repeatedly compare every quality at the same level. Four measures repeat under each quality, creating a very wide matrix.

Pass behavior:

- make continuous same-level comparison a veto requirement;
- keep all qualities in one horizontal comparison view;
- use grouped headers, visual boundaries, widths, and frozen row keys to manage width;
- reject splitting qualities into vertical blocks or separate sheets solely for narrower rendering.

The normalized long table also fails when it requires filtering one level before the requested cross-quality comparison becomes possible.

## Case H: prior solution contamination

Raw data and a prior manually organized solution are both present, but the user asks to test whether the Skill can solve the task independently.

Pass behavior:

- exclude the prior solution from source inventory, structure reasoning, and visual validation;
- derive dimensions, measures, and layout from raw data and operations only;
- state the exclusion before analysis;
- fail the test if the prior solution was inspected, even if no values were copied.

## Case I: full domain versus convenient baseline

The request covers level × quality, but some high qualities have partial or missing level coverage.

Pass behavior:

- preserve all requested levels and qualities in the model and structure;
- classify each combination by evidence state;
- do not replace the task with a level-1 summary or representative sample;
- use samples only for analysis and validation.

## Case J: evidence metadata explosion

Some cells are direct, some estimated, and some unavailable. The main task is numerical comparison.

Pass behavior:

- keep the requested measures as the dominant visual content;
- encode evidence state with a compact legend and cell-level visual or note;
- avoid repeating value/state/basis columns under every quality;
- add an audit area only when requested or necessary for safe interpretation.

## Case K: structure arithmetic

A cross-tab has one row key, 14 column groups, and four measures per group.

Pass behavior:

- calculate the data width as `1 + 14 × 4 = 57` columns;
- reconcile expected combinations and measure cells independently;
- fail before authoring if stated dimensions and stated range size disagree;
- include title/legend rows separately from data-body counts.

## Case L: direct measure versus encoded auxiliary field

The requested attack is explicitly stored in `score`; an auxiliary `base_attr` is literal in some rows and an opaque pointer in others.

Pass behavior:

- select `score` as the authoritative requested measure;
- classify every present `score` as direct;
- use literal `base_attr` rows only as corroboration of meaning;
- do not classify pointer-backed rows as resolved when `score` itself is present.

## Case M: dimension-member exhaustiveness

Six positions exist; five are suspected to share ordinary attack and one is exceptional.

Pass behavior:

- enumerate all six positions before collapsing the dimension;
- test all five ordinary positions, not a convenient subset;
- represent the exceptional position as a dedicated measure when appropriate;
- report missing or unobserved members rather than silently omitting them.

## Failure indicators

- selecting a structure before source classification or relationship tests;
- claiming completeness from non-empty rows only;
- treating a reference workbook as authoritative because it is convenient;
- adding a category dimension without proving it changes a required measure;
- producing a technically valid but visually inferior comparison view;
- using a prior solution during an independent capability test;
- validating a model only on the points used to fit it;
- converting zero-evidence tiers into exact-looking values;
- splitting a mandatory continuous comparison to reduce width;
- choosing a normalized long table for a human two-dimensional reference table without an explicit filtering/import requirement;
- reducing full level coverage to a baseline level;
- tripling every measure into value/state/basis columns without necessity;
- reporting row, column, combination, or cell counts that do not reconcile;
- downgrading a directly stored requested measure because an auxiliary field is encoded;
- collapsing a dimension without testing and accounting for all authoritative members;
- passing solely because `quick_validate.py` succeeds.
