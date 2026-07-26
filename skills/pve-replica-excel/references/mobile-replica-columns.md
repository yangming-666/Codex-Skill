# Mobile replica column contract

Use this reference for mobile unpack/config tasks whose workbook separates production wording, numeric payload, and proof.

## Logical columns

1. `程序复刻规则`: a complete implementation requirement in natural Chinese.
2. `数值`: a compact free-form numeric payload for the current mechanism.
3. `证据`: source locations and identifiers sufficient to verify the row.

Existing columns such as `数值/时间/概率`, raw mobile range, and grid conversion may remain separate physical columns while belonging to the same logical numeric bucket.

## 程序复刻规则

State the mechanic, trigger, location, targets, effect, and settlement behavior. Include values needed to implement the feature, so the rule is understandable without reading evidence.

Do not include:

- dereference chains or audit narration;
- unpack IDs as implementation fields;
- PVE Lua/KV field names unless explicitly requested;
- inherited values that the current enhancement does not create or change.

## 数值

Preserve the mobile raw values and summarize only values owned by the current row, for example:

`爆炸伤害倍率=3500‰；爆炸范围半径=2000；表现持续=2000ms；范围换算=1.25格`

Use `范围换算=...格` for a conversion. Do not invent a `PVE范围` implementation field.

## 证据

Record file/table names, row IDs, line numbers, and behavior-node locations. Keep production wording and implementation choices out of this column.

## Dereference boundary

Follow deeper links when the current enhancement creates an independent settlement and the visible row omits an implementation-critical value such as damage, radius, duration, chance, count, or timing.

Do not pull in values from a reused base skill or another enhancement when the current row only changes control, timing, chance, count, or another narrow payload. Current-row ownership controls inclusion.

## Gate

- `程序复刻规则` can be handed directly to an implementer.
- `数值` contains only current-row values.
- `证据` contains proof only.
- No unpack ID or internal proof chain became a production field.
