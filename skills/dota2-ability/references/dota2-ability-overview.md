# Dota 2 Ability Overview

Use this reference for general Dota 2 ability authoring (KV + Lua) without project-specific systems.

## Core Files

- Ability KV: `scripts/npc/npc_abilities_custom.txt` (or per-hero KV in some projects)
- Hero KV: `scripts/npc/npc_heroes_custom.txt`
- Lua: `scripts/vscripts/` (ability and modifier scripts)

## Ability KV Basics

- Abilities are defined as KV blocks under `DOTAAbilities`.
- Specials live in `AbilitySpecial` or in a project-specific `AbilityValues` block.
- Link Lua with `ScriptFile` when the ability is implemented in Lua.

## Lua Ability Basics

- Ability class: `my_ability = class({})`
- Common hooks: `OnSpellStart`, `OnAbilityFullyCast`, `OnChannelFinish`
- Link modifiers with `LinkLuaModifier`.
- Use intrinsic modifiers for passives via `GetIntrinsicModifierName`.

## Common API Usage

- Projectiles: `ProjectileManager:CreateLinearProjectile` / `CreateTrackingProjectile`
- Damage: `ApplyDamage`
- Timers: use a Timers library if present, otherwise `Timers:CreateTimer` in custom frameworks
- Unit checks: `IsNull()`, `IsAlive()`, `IsServer()`

## Typical Workflow

1) Update KV specials and metadata.
2) Add or edit Lua behavior.
3) Add modifiers for passives and persistent effects.
4) Test in a local lobby or test map.
