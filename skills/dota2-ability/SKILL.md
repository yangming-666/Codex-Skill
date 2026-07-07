---
name: dota2-ability
description: "Dota 2 custom ability authoring and rewrites with Lua + KV. Use only for ability-scoped work: editing ability KeyValues, creating or changing ability/modifier Lua, or implementing ability-specific targeting, projectile, cast, buff, debuff, or damage behavior. Do not use for generic Lua game logic such as test mode, shop/account/backend/service flow, UI, game mode orchestration, or unrelated systems unless the change directly modifies an ability or modifier."
---

# Dota2 Ability

## Overview

Create or rewrite Dota 2 abilities using KV + Lua, using proven patterns for modifiers, events, projectiles, and API-driven behavior.

This skill is intentionally narrow. It applies to gameplay logic that belongs to an ability, modifier, or ability KV contract.

Use this skill for:
- Ability KV blocks and special values.
- Ability Lua classes and intrinsic/passive logic.
- Modifier Lua tied to an ability.
- Ability targeting, cast flow, cooldown/mana handling, projectile behavior, damage/heal/control effects.
- Vanilla ability rewrites or full-fidelity replications.

Do not use this skill for:
- Generic Lua gameplay systems not owned by an ability or modifier.
- `test_mode.lua`, debug commands, whitelist gating, or GM tooling.
- Shop, payment, account, backend sync, or service callback logic.
- Panorama UI, generic HUD, or other frontend work.
- Match flow, spawn systems, wave systems, selection flow, or other gamemode orchestration.

If a task touches Lua but the primary object being changed is not an ability/modifier, do not trigger this skill.

## Required Local Sources (Portable Resolution)

Do not hardcode machine-specific absolute paths in this skill. Resolve roots dynamically in this order.

1) Vanilla KV root (project-provided source KV)
- First: env var `DOTA2_VANILLA_KV_ROOT`.
- Second: repo-relative path `Dota2 原版游戏配置` from current workspace root.
- Third: ask user for the KV root path.

2) Dota 2 Ability Source Library (Reference Lua/KV)
- First: repo-relative path `tools/Dota2 ability` from current workspace root.
- Purpose: Provides comprehensive Lua source (`spellLib/lua/heroes/`) and KV definitions (`spellLib/kv/abilities/`) for vanilla abilities.

Before implementation, print the resolved paths you will use.

Quick lookup commands (PowerShell, portable):
- `if ($env:DOTA2_VANILLA_KV_ROOT) { Get-ChildItem $env:DOTA2_VANILLA_KV_ROOT -Recurse -File }`
- `if (Test-Path ".\\Dota2 原版游戏配置") { Get-ChildItem ".\\Dota2 原版游戏配置" -Recurse -File }`
- `if (Test-Path ".\\tools\\Dota2 ability") { Get-ChildItem ".\\tools\\Dota2 ability\\spellLib" -Recurse -File }`

## Workflow

1) Classify change type
- Pure data change: edit KV only.
- Behavior change: add or modify Lua.
- Awakening override: add awakening modifier + KV entry.

2) Pull vanilla reference first (mandatory for rewrites)
- Read source ability block from resolved vanilla KV root.
- **Reference Lua Logic**: Check `tools/Dota2 ability/spellLib/lua/heroes/` for the corresponding hero/ability implementation.
- Extract and list: `AbilityBehavior`, `AbilityUnitTarget*`, cast point/range, key specials.
- For hero abilities, prefer `<vanilla_kv_root>/heroes/npc_dota_hero_<hero>.txt`.

3) Resolve original presentation helpers
- For sound event and resource lookup, use the dedicated `$dota2-sound-lookup` skill.
- For visual playback, use the dedicated `$dota2-particle-playback` skill.
- If the visual reference cannot be found or inspected, explicitly say visual parity cannot be guaranteed yet.

4) Implement KV + Lua
- KV numbers stay in KV when possible.
- Lua handles behavior, sequencing, targeting, and complex projectile logic.
- Place/modify scripts according to project layout and existing patterns.

## Guidance

- Prefer KV edits for numbers; use Lua for behavior changes.
- Avoid hardcoding numbers in Lua if the KV can express them.
- Never hardcode machine-specific filesystem paths (for example `C:\...`, `E:\...`) in skill instructions or templates.
- Gate difficulty scaling with `GameRules:GetCustomGameDifficulty()`.
- Use `Timers:CreateTimer` for sequenced effects; avoid global state.
- Keep logic server-side; guard with `if not IsServer() then return end`.
- For projectiles where the visual effect does not move with the logic projectile, use a tracking dummy + tracking projectile for visuals and a linear projectile for damage; destroy the visual projectile on hit/expire via `visual_proj_id` in `ExtraData`.
- Treat the built-in modifier list as valid engine-provided names; do not re-define them in Lua.

## Vanilla-Replication Standard (for KV -> Lua rewrites)

When converting a vanilla ability to Lua, replicate baseline presentation unless task explicitly changes it:

1) Cast phase
- Correct cast gesture/cast point.

2) Projectile/travel phase
- Use linear projectile logic when the vanilla behavior is straight-line.
- Use tracking dummy plus tracking logic when the behavior needs a separate visual path.
- Keep speed, width/radius, and travel timing aligned with vanilla specials.

3) Impact/area phase
- Apply the intended damage, stun, root, slow, or buff/debuff effect.
- Keep linger/burn timing aligned with vanilla specials.
- If user asks for visual-only burn, keep the damage logic unchanged and adjust only the effect timing.

4) Verification checklist (must report)
- Confirm no engine-side vanilla cast path was used (`ExecuteOrderFromTable`/`OnSpellStart` for vanilla ability playback).
- Confirm which vanilla KV fields were mapped.
- Any intentional deviations from vanilla and why.

5) Full-replication claim guardrail
- Do not state "完全复刻" unless the gameplay timing and visible behavior are validated against vanilla behavior.
- **Logic Parity**: Cross-check with `tools/Dota2 ability/spellLib/lua/heroes/` to ensure all edge cases and hidden mechanics (e.g., static field interactions, specific modifier behaviors) match the original implementation.

## Task Mapping

- "Adjust numbers by difficulty" -> KV scaling or project-specific override logic.
- "Make ability passive" -> `GetIntrinsicModifierName` + intrinsic modifier logic.
- "Add extra casts/targets" -> `OnAbilityFullyCast` + dummy caster or manual calls.
- "Rewrite projectile behavior" -> create projectiles and handle `OnProjectileHit`.
- "Add new ability" -> KV block + new Lua ability file + LinkLuaModifier.

## References

- ModDota VScripts API: https://iwasinminedream.github.io/moddota.github.io/api/vscripts/
- ModDota Game Events: https://iwasinminedream.github.io/moddota.github.io/api/events
- ModDota Original Abilities: https://iwasinminedream.github.io/moddota.github.io/api/abilities
- ModDota Original Modifiers: https://iwasinminedream.github.io/moddota.github.io/api/modifiers
- Dota 2 ability overview: `references/dota2-ability-overview.md`
- Ability KV format: `references/ability-kv-format.md`
- Lua patterns and hooks: `references/lua-ability-patterns.md`
- Awaken examples (project-specific): `references/awaken-ability-examples.md`
- Built-in modifier names (authoritative list): `references/built-in-modifier-names.md`
- Awaken architecture notes: `references/awaken-ability-architecture.md`
- Sound lookup: `$dota2-sound-lookup`
- Dota 2 Ability Source Library (Lua/KV Reference): [tools/Dota2 ability](file:///tools/Dota2%20ability)
- Hero Lua Reference Path: `tools/Dota2 ability/spellLib/lua/heroes/`
- Ability KV Reference Path: `tools/Dota2 ability/spellLib/kv/abilities/`

## Assets

- Ability templates (KV + Lua + optional awakening modifier): `assets/ability-template/`
