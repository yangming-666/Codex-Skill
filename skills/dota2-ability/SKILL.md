---
name: dota2-ability
description: Dota 2 custom ability authoring and rewrites with Lua + KV. Use when editing ability KeyValues, creating new Lua abilities/modifiers, or integrating ability logic with Dota 2 APIs in any custom game.
---

# Dota2 Ability

## Overview

Create or rewrite Dota 2 abilities using KV + Lua, using proven patterns for modifiers, events, projectiles, and API-driven behavior.

## Required Local Sources (Portable Resolution)

Do not hardcode machine-specific absolute paths in this skill. Resolve roots dynamically in this order.

1) Dota 2 particles root (`.../content/dota/particles/units/heroes`)
- First: env var `DOTA2_CONTENT_ROOT` (expects `.../dota 2 beta/content/dota`).
- Second: detect common Steam install roots on current OS and append `dota 2 beta/content/dota`.
- Third: if still missing, ask user for the Dota 2 install path.

2) Vanilla KV root (project-provided source KV)
- First: env var `DOTA2_VANILLA_KV_ROOT`.
- Second: repo-relative path `Dota2 原版游戏配置` from current workspace root.
- Third: ask user for the KV root path.

Before implementation, print the resolved paths you will use.

Quick lookup commands (PowerShell, portable):
- `if ($env:DOTA2_CONTENT_ROOT) { Join-Path $env:DOTA2_CONTENT_ROOT "particles/units/heroes" }`
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
- Which vanilla KV fields were mapped.
- Which particle paths were used.
- Which sound events were used.
- Any intentional deviations from vanilla and why.

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
