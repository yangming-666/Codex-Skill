# Senior Numerical Planning Reasoning

Use this protocol to distinguish numerical planning from data transcription.

## 1. Reconstruct the mechanic

For each requested output, write the dependency chain:

```text
input dimensions -> rule/parameter -> rounding/boundary -> output measure -> player-facing effect
```

Verify every link from authorized evidence. Distinguish an item instance, a configuration key, a presentation label, and a player-facing value.

## 2. Test functional dependencies

For a proposed key `K` and measure `M`:

- group by `K` and count distinct `M`;
- investigate every group with more than one value;
- add the smallest dimension that resolves ambiguity;
- test whether any retained dimension can be removed without changing a required measure.

Do not preserve a source-table dimension automatically. Source schemas optimize implementation, not planner lookup.

Treat an authoritative player-facing output field as direct evidence even when a lower-level implementation field is encoded or unresolved. Do not downgrade a directly stored requested value merely because an alternative representation of the same mechanic needs decoding.

Before testing whether a dimension can collapse, enumerate all of its authoritative members. A conclusion based on positions 1–3 does not cover positions 5–6. Report the tested member set and exception set explicitly.

## 3. Analyze progression and economy

Use the checks that apply:

- first and second differences;
- adjacent and cumulative ratios;
- marginal value per level/tier;
- cost-to-power and salvage-to-cost ratios;
- source/sink balance and refund behavior;
- plateaus, jumps, caps, unlocks, and tier boundaries;
- integer rounding and low-value distortion;
- monotonicity exceptions and duplicate tiers.

Explain anomalies as intentional design, extraction defects, or unresolved evidence. Do not smooth them away.

## 4. Validate models before extrapolation

Prefer executable/configured formulas over fitted curves. When fitting is unavoidable:

1. define candidate families from mechanic knowledge;
2. reserve authoritative points for holdout validation;
3. compare absolute and relative error, especially at boundaries;
4. test whether coefficients remain stable across neighboring tiers or segments;
5. reject extrapolation across an unseen tier, breakpoint, or regime without independent support;
6. report an interval or scenario when multiple models remain plausible.

A model that reproduces all training points can still be unqualified. Zero observed points for a target category means there is no empirical validation for that category.

## 5. Separate fact, calculation, estimate, and absence

- `direct`: explicitly present in authoritative evidence;
- `resolved`: deterministically derived from direct evidence with verified logic;
- `estimated`: model-dependent and uncertainty-bearing;
- `unavailable`: evidence does not justify a value.

Never relabel `estimated` as `resolved`. Never replace `unavailable` with a convenient number to make the table look complete.

## 6. Design for the actual decision

Identify the user's repeated action: locate one key, compare across categories, edit parameters, import configuration, audit coverage, or balance an economy. Minimize the number of eye movements, filters, sheet switches, and mental joins required for that action.

Width, row count, and sheet count are costs, not universal prohibitions. A wide continuous matrix is correct when cross-category comparison is the primary operation. A long table is correct when exact filtering and import dominate. A composite is justified only when both operations are mandatory.

For two finite ordered dimensions with repeated measures, use this default unless the requirement says otherwise:

```text
human numerical reference/comparison -> larger dimension on rows,
smaller dimension as grouped columns,
measures nested under each group
```

Do not collapse the domain to a baseline level to simplify presentation. Do not multiply every measure into value/state/basis columns when a compact evidence legend preserves meaning.

## 7. Produce an internal decision record

Before workbook authoring, be able to state:

- authoritative sources and excluded inputs;
- grain and unique keys;
- functional dependencies and exceptions;
- formulas and economy interpretation;
- coverage counts by evidence state;
- inference verdict and validation evidence;
- mandatory user operation;
- candidate layouts and vetoed failures;
- chosen structure and why it minimizes user effort.

If this record cannot be completed, analysis is not ready for Excel.
