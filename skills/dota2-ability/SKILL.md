---
name: dota2-ability
description: Dota 2 custom ability authoring and rewrites with Lua + KV. Use only for ability-scoped work: editing ability KeyValues, creating or changing ability/modifier Lua, or implementing ability-specific targeting, projectile, cast, buff, debuff, or damage behavior. Do not use for generic Lua game logic such as test mode, shop/account/backend/service flow, UI, game mode orchestration, or unrelated systems unless the change directly modifies an ability or modifier.
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

1) Dota 2 particles root (`.../content/dota/particles/units/heroes`)
- First: env var `DOTA2_CONTENT_ROOT` (expects `.../dota 2 beta/content/dota`).
- Second: detect common Steam install roots on current OS and append `dota 2 beta/content/dota`.
  - On Windows, check both `Steam\steamapps\common\dota 2 beta` and `SteamLibrary\steamapps\common\dota 2 beta` under available drives, not only `C:`.
- Third: if still missing, ask user for the Dota 2 install path.

2) Vanilla KV root (project-provided source KV)
- First: env var `DOTA2_VANILLA_KV_ROOT`.
- Second: repo-relative path `Dota2 原版游戏配置` from current workspace root.
- Third: ask user for the KV root path.

Before implementation, print the resolved paths you will use.

Quick lookup commands (PowerShell, portable):
- `if ($env:DOTA2_CONTENT_ROOT) { Join-Path $env:DOTA2_CONTENT_ROOT "particles/units/heroes" }`
- ``$roots = @(); Get-PSDrive -PSProvider FileSystem | ForEach-Object { $roots += (Join-Path $_.Root 'Steam\\steamapps\\common\\dota 2 beta\\content\\dota'); $roots += (Join-Path $_.Root 'SteamLibrary\\steamapps\\common\\dota 2 beta\\content\\dota') }; $roots | Where-Object { Test-Path $_ }``
- `if ($env:DOTA2_VANILLA_KV_ROOT) { Get-ChildItem $env:DOTA2_VANILLA_KV_ROOT -Recurse -File }`
- `if (Test-Path ".\\Dota2 原版游戏配置") { Get-ChildItem ".\\Dota2 原版游戏配置" -Recurse -File }`

## Workflow

1) Classify change type
- Pure data change: edit KV only.
- Behavior change: add or modify Lua.
- Awakening override: add awakening modifier + KV entry.

2) Pull vanilla reference first (mandatory for rewrites)
- Read source ability block from resolved vanilla KV root.
- Extract and list: `AbilityBehavior`, `AbilityUnitTarget*`, `AbilitySound`, cast point/range, key specials.
- For hero abilities, prefer `<vanilla_kv_root>/heroes/npc_dota_hero_<hero>.txt`.

3) Resolve original visual/audio assets (mandatory for rewrites)
- Search particles under:
  `<dota2_content_root>/particles/units/heroes/hero_<hero>/`
- Match projectile/impact/linger/cast particles with vanilla behavior.
- Reuse vanilla sound events from KV or scripts (do not invent names unless required by mod assets).

3.1) Inspect the actual particle definition before coding (mandatory when touching vanilla VFX playback/modification)
- If the task involves playing, reconstructing, or modifying a vanilla particle, open the actual `.vpcf` file first.
- Read the file to identify required control points, attach hints, named children, and likely playback expectations before writing Lua.
- Do not guess CP usage from memory or from the particle filename alone.
- If the `.vpcf` cannot be found or inspected, explicitly say visual parity cannot be guaranteed yet.

Useful commands (PowerShell):
- ``$particle = 'earthshaker_aftershock.vpcf'; Get-ChildItem $dota2ContentRoot -Recurse -Filter $particle``
- ``Get-Content '<full path to .vpcf>' -TotalCount 260``
- ``Select-String -Path '<full path to .vpcf>' -Pattern 'control point|cp|attach|snapshot|remap' -CaseSensitive:$false``

3.2) Enforce full-fidelity playback rules (mandatory when user asks "完全复刻"/"与原版一致")
- Full replication means Lua-driven effect reconstruction, not engine-side skill playback.
- Mandatory restrictions for full replication tasks:
  - Do not use `ExecuteOrderFromTable` to cast the vanilla ability for visuals.
  - Do not call `ability:OnSpellStart()` to let C++ play original effects.
  - Do not claim full replication if implementation only uses bare `CreateParticle(...)` + one control point.
- Implement visual playback manually in Lua:
  - Reproduce original attach type (`PATTACH_*`).
  - Base CP decisions on the inspected `.vpcf`, not on memory.
  - Reproduce all required control points (not only `CP0`) via `SetParticleControl` / `SetParticleControlEnt`.
  - Reproduce cast/impact timing from vanilla cast point and behavior.
  - Reuse vanilla particle path and sound resource/event mapping unless task explicitly changes them.

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
- For projectiles where tracking particles do not move with linear projectiles, use a tracking dummy + tracking projectile for visuals and a linear projectile for damage; destroy the visual projectile on hit/expire via `visual_proj_id` in `ExtraData`.
- Treat the built-in modifier list as valid engine-provided names; do not re-define them in Lua.

## Vanilla-Replication Standard (for KV -> Lua rewrites)

When converting a vanilla ability to Lua, replicate baseline presentation unless task explicitly changes it:

1) Cast phase
- Correct cast gesture/cast point.
- Correct cast/start sound event.

2) Projectile/travel phase
- If particle is linear-compatible, use linear projectile effect directly.
- If particle is not linear-compatible, use tracking visual + linear logic projectile.
- Keep speed, width/radius, and travel timing aligned with vanilla specials.

3) Impact/area phase
- Use vanilla impact particle and sound event.
- Spawn linger/burn visuals when vanilla has them.
- If user asks visual-only burn, apply VFX duration only and keep damage logic unchanged.

4) Verification checklist (must report)
- Confirm no engine-side vanilla cast path was used (`ExecuteOrderFromTable`/`OnSpellStart` for vanilla ability playback).
- Confirm the actual `.vpcf` file was inspected and name the file path used.
- Exact `PATTACH_*` mode and CP indices/values that were set.
- Which vanilla KV fields were mapped.
- Which particle paths were used.
- Which sound events were used.
- Any intentional deviations from vanilla and why.

5) Full-replication claim guardrail
- If attach mode/CP mapping cannot be verified, explicitly say "cannot guarantee full visual parity yet".
- Do not state "完全复刻" unless playback path and visual timing are validated against vanilla behavior.

## Task Mapping

- "Adjust numbers by difficulty" -> KV scaling or project-specific override logic.
- "Make ability passive" -> `GetIntrinsicModifierName` + intrinsic modifier logic.
- "Add extra casts/targets" -> `OnAbilityFullyCast` + dummy caster or manual calls.
- "Rewrite projectile behavior" -> create projectiles and handle `OnProjectileHit`.
- "Add new ability" -> KV block + new Lua ability file + LinkLuaModifier.

## References

- Dota 2 ability overview: `references/dota2-ability-overview.md`
- Ability KV format: `references/ability-kv-format.md`
- Lua patterns and hooks: `references/lua-ability-patterns.md`
- Awaken examples (project-specific): `references/awaken-ability-examples.md`
- Built-in modifier names (authoritative list): `references/built-in-modifier-names.md`
- Awaken architecture notes: `references/awaken-ability-architecture.md`

## Assets

- Ability templates (KV + Lua + optional awakening modifier): `assets/ability-template/`
