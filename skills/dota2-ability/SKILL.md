---
name: dota2-ability
description: Dota 2 custom ability authoring and rewrites with Lua + KV. Use when editing ability KeyValues, creating new Lua abilities/modifiers, or integrating ability logic with Dota 2 APIs in any custom game.
---

# Dota2 Ability

## Overview

Create or rewrite Dota 2 abilities using KV + Lua, using proven patterns for modifiers, events, projectiles, and API-driven behavior.

## Workflow

1) Decide the change type
- Pure data change: edit KV only.
- Behavior change: add or modify Lua.
- Awakening override: add awakening modifier + KV entry.

2) Update KV
- Locate the hero KV in `scripts/npc/heros_ability/`.
- Add or edit the ability block and `AbilityValues`.
- Keep value formats consistent with the existing file.

3) Update Lua
- Place ability scripts in `scripts/vscripts/hero/hero_<name>/`.
- Add modifiers and link with `LinkLuaModifier`.
- Use `GetIntrinsicModifierName` for passives.
- Use `OnAbilityFullyCast` for extra casts or multi-target logic.

4) Apply project-specific extensions (optional)
- If the project uses an awaken-style system, follow its override and registry rules.
- Otherwise keep changes within KV + Lua and the standard ability/modifier flow.

## Guidance

- Prefer KV edits for numbers; use Lua for behavior changes.
- Avoid hardcoding numbers in Lua if the KV can express them.
- Gate difficulty scaling with `GameRules:GetCustomGameDifficulty()`.
- Use `Timers:CreateTimer` for sequenced effects; avoid global state.
- Keep logic server-side; guard with `if not IsServer() then return end`.
- For projectiles where tracking particles do not move with linear projectiles, use a tracking dummy + tracking projectile for visuals and a linear projectile for damage; destroy the visual projectile on hit/expire via `visual_proj_id` in `ExtraData`.
- Treat the built-in modifier list as valid engine-provided names; do not re-define them in Lua.

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

## Assets

- Ability templates (KV + Lua + optional awakening modifier): `assets/ability-template/`
