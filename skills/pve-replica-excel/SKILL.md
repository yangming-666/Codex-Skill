---
name: pve-replica-excel
description: Update PVE hero skill configuration Excel workbooks in implementation-ready replica planning style. Use when editing 英雄技能强化配置.xlsx or similar PVE考据 sheets that must turn game config, buffs, passives, and behavior trees into concise策划复刻说明 rather than raw dumps.
---

# PVE Replica Excel

## Core Rule

Treat the workbook as a replica implementation planning document, not a config dump.

Write for someone implementing the skill behavior. Convert raw config into stable behavior contracts: trigger, target, range, timing, damage coefficient, tick cadence, duration, cooldown, caps, exclusions, and branch relationships.

Workbook cells should contain the final design contract, not the audit trail. Prefer positive implementation statements: what to trigger, what range to use, what numbers to apply, and how branches stack.

## Mobile PVE Concept Layers

Keep these layers separate before writing `复刻说明`:

- `主技能入口`: `SkillData__data_skill_lev_up.lua` defines the hero display skill, display levels, and links to `logic_dmg_skill_id` / `logic_cooling_skill_id`. Use this to decide which skill row is the main active/passive being documented.
- `合成星级设计`: `HeroData__data_get_base.lua` defines `hero_dmg_rate`, `star_atk_factor`, `star_atk_speed_factor`, and `star_buff`. `tools/build_hero_merge_star_md.py` is the canonical planning derivation for main-skill 1-4 star damage and cooldown/interval curves.
- `底层逻辑技能`: `SkillData__data_skill_lev.lua` gives base skill coefficients such as `dmg_factor`, `interval_time`, `cooling_time`, target counts, bullet counts, passives, and config ranges. These are bottom-layer anchors, not final per-star replica multipliers by themselves.
- `Buff/Passive机制`: `BuffData` and `PassiveData` define DOT ticks, debuffs, triggered skills, durations, and condition chains. Express these as their own behavior contracts, then project star-only coefficients only when the damage path supports that formula.
- `局内强化/增强`: `RogueData`, `LevelEventData`, strengthening buffs, and hero-specific enhancement passives alter the base skill. Do not fold them into base 1-4 star main-skill coefficients unless the user explicitly asks for a strengthened-state row.
- `行为树/反编译运行时`: extracted skill blocks and C# sources resolve custom geometry, visual timing, runtime hitbox construction, target filters, and display/runtime disagreements. Use them to audit facts, especially when screenshots conflict with table geometry.

## Row Scope Rule

Before writing or updating an Excel row, identify the row's active scope: base main skill, display/skill-level summary, hero step-up or unlock layer, rogue/strengthening layer, special/ultimate layer, or runtime audit note.

Only include effects that are active inside that row's scope. Current-row scope beats same-name aggregation: when several config entries share the same skill name, use the display level, passive/action, and runtime behavior that belong to the target row instead of combining every same-name level.

For a base main skill row, do not write concrete values from later step-up, rogue, totem, equipment, skin, co-op, ultimate, or other strengthening layers. If a later layer matters for implementation, mention only that it is configured in its own unlock/strengthening layer, without copying its numbers into the base row.

If the target row is explicitly an unlock, strengthening, or level-summary row, write that layer's concrete values and keep base values separate.

For main skill star planning, use this design口径:

- Direct skill damage multiplier: `hero_dmg_rate / 1000 * logic_dmg.dmg_factor / 1000 * star_atk_factor / 100`, equivalent to `hero_dmg_rate * dmg_factor * star_atk_factor / 100000000`.
- Skills driven by `interval_time`: `actual interval = interval_time / (star_atk_speed_factor / 100)`.
- Fixed cooldown skills: start from `cooling_time`, then apply confirmed star cooldown/passive modifiers only if present.
- Persistent damage effects: describe only the fields needed to reproduce that specific effect. Typical fields include trigger, target, duration, tick cadence, stack/refresh rule, damage倍率, damage type, and caps, but do not force every effect into the same template.
- Runtime internal modifiers such as ordered-hit `finalDmgRatio` tables are hit-distribution or final-damage adjustments, not star multipliers. Add them only when they must be implemented; keep them out when they do not affect the requested row.

## Required Output Voice

Match the target sheet's actual口径 before editing. In `复刻_技能配置`, most rows use this shape:

- `【技能定位】`: one sentence describing the gameplay role.
- `【基础机制】`: behavior chain and hard parameters needed to implement it. Complex active skills usually fit most runtime facts here.
- Optional named paragraph such as `【召唤物属性】`, `【行为时序】`, `【中毒/降疗】`, or `【吞噬结算】`: use only when that sub-mechanic would make `【基础机制】` too dense.
- `【合成星级】`: active skill star damage/cooldown/interval summary.
- `【技能等级】`: passive or display-level summaries. Use this for rows whose `索敌范围` is `被动`.
- `【复刻注意】`: implementation cautions, branch ownership, and what not to collapse.

Do not write a pure program dump. Do not include source IDs, config table names, code class names, formula names, or audit-only anchors in workbook cells unless the user explicitly asks for source traceability in the workbook. Prefer "吞噬索敌半径4格，冷却60秒，单目标" over "40505 geometry_atk_range radius=6400 target_num=1 cooling_time=60000".

Keep row style consistent with neighbors:

- Active complex rows may mention separate behavior links by design name only, not by source ID.
- Simple active rows should stay short: positioning, main mechanism, star curve.
- Passive rows should use `【技能定位】初始被动技能。`, `【基础机制】`, then `【技能等级】`.
- Avoid more than one or two optional named paragraphs unless the row is summon/entity-heavy like 安妮.

## Hard Rules

- Always preserve workbook structure, sheet names, headers, and existing style.
- Update only the requested rows/cells unless the user asks for broader cleanup.
- Keep `复刻说明` as the implementation-facing behavior contract.
- Keep `复核结论` short. Use existing sentence patterns:
  - `无确认缺失。`
  - `无关键缺口；...已确认。`
  - `缺失：...。 已确认：...。`
- Convert units:
  - distance: `1600 = 1格`.
  - milliseconds to seconds for prose; keep exact milliseconds only when precision matters.
  - thousandths coefficients to readable multipliers or percentages.
- Separate display text from runtime behavior when they differ.
- Separate config coefficients from final replica multipliers. If star/display/effective damage curves exist, write only the implementation-facing star curve in the workbook cell; keep bottom-layer coefficients in private notes.
- For persistent damage buffs, write the minimum complete implementation contract for that effect. Include star倍率 only when the row asks for star-scaled damage or the effect's damage changes by star; keep derivation details outside the workbook cell.
- For custom behavior-tree actions, write the positive implementation behavior only. Avoid negative contrast such as "not 1格 x 0.625格"; write "按长条手臂处理：长度约6格起，沿目标方向延展".
- Do not summarize future display levels in a current active skill row unless the row is explicitly a level summary or the user asks for all levels.
- If a source has `lev=1/2/3` variants but higher variants are unlocked by hero step-up, rogue, or another progression layer, keep only the active variant in the base row.
- Treat behavior-tree timing fields as relative to their owning action unless the source proves they are relative to cast start. For example, an arm action's `atkWaitTime` is not automatically "after attach/cast".
- When live screenshots conflict with a config-only interpretation, update the prose to preserve the live behavior and move the uncertain config relationship into `复核结论`.
- Do not hide confirmed hard values in `复核结论`; put them in `复刻说明`.
- Do not overstate. If a behavior-tree field still needs live validation, mark it as "仍需实机确认".
- If a UI文案 duration conflicts with Buff duration, state both and identify which one is runtime.

## Cell Content Filter

Before finalizing any cell, reduce each sentence to one of these roles:

- `实现参数`: direct implementation values such as duration, radius, target count, hit cap, cooldown, tick cadence, and 1-4 star倍率.
- `行为关系`: trigger chain, owner/target relationship, stacking relationship, and branch relationship.
- `必要注意`: only include when it changes implementation behavior or prevents mixing two implemented layers in the same row scope.

Remove sentences whose only role is source proof, derivation, contrast against a wrong hypothesis, broad caveats without a concrete branch, or concrete values from another row scope.

## Source Priority

Use these sources in order:

1. Existing workbook wording and row conventions.
2. Main-skill star design sources: `HeroData__data_get_base.lua`, `SkillData__data_skill_lev_up.lua`, `SkillData__data_skill_lev.lua`, and `tools/build_hero_merge_star_md.py`.
3. `BuffData`, `PassiveData`, `RogueData`, and `LevelEventData` for buffs, passives, and strengthening layers.
4. Extracted behavior trees under `reports/skill_behavior_trees.../extracted_skill_blocks` and decompiled C# sources for custom actions, hitboxes, and runtime display formulas.
5. Existing audit/update notes under `outputs/hero_skill_enhance_update` and `reports/hero_skill_enhance`.

## Spreadsheet Workflow

1. Render or inspect the target sheet before editing.
2. Locate the target row by hero and skill/enhancement name.
3. Read current values in the target row.
4. Read 5-10 nearby or analogous rows to match length, section names, and conclusion style.
5. Gather only the source rows needed for the requested mechanism.
6. Write concise replica prose using the required output voice.
7. Put hard confirmed values in `复刻说明`; put residual uncertainty in `复核结论`.
8. Compare the edited row against analogous rows before saving.
9. Inspect the edited range and scan for formula errors.
10. Render the edited range if the workbook tool supports it.

## Avoid

- Long lists of raw table fields.
- Repeating every passive/buff ID when one behavior sentence is enough.
- Source IDs, table names, code class names, and formula derivation in workbook cells.
- Adding speculative mechanics not supported by source rows.
- Replacing the workbook's策划口径 with code-review language.
- Mixing base main-skill star coefficients with rogue/enhancement/stateful battle modifiers.
- Negative framing such as "不是/不能按/不包含" unless it prevents a concrete implementation bug that cannot be stated positively.
- Aggregating same-name display levels into a base skill row.
- Copying concrete values from other scopes into `复刻注意` just because they are accurate elsewhere.
