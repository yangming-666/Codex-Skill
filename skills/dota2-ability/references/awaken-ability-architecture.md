# Awaken Ability Architecture (Project-Specific)

This reference summarizes how abilities are wired in the Awaken codebase. Use only when working in Awaken-style projects.

## Ability KV Layout

- Per-hero KV lives in `scripts/npc/heros_ability/`.
- Each file defines a `"DOTAAbilities"` root and ability blocks.
- This project uses `AbilityValues` blocks instead of classic `AbilitySpecial`.

## Lua Ability Layout

- Hero ability scripts live in `scripts/vscripts/hero/hero_<name>/`.
- Awakening overrides are grouped in `modifier_<hero>_awaken.lua` per hero.
- Shared awakening base lives in `scripts/vscripts/modifiers/modifier_awakening.lua`.

## Awakening Value Overrides

- `modifier_base_awakening` implements `GetModifierOverrideAbilitySpecial` and `GetModifierOverrideAbilitySpecialValue`.
- Hero awakening modifiers inherit from `modifier_base_awakening`.
- `KeyValues.Awakening` (loaded from `scripts/npc/kv/Awakening.kv`) controls which abilities get awakening modifiers.

## Auto-Loading Awakening Modifiers

- `scripts/vscripts/modifiers/modifier_awakening.lua` dynamically requires hero awaken files.
- The hero list is read from `scripts/npc/herolist.txt`.
- If a hero is missing or disabled, the loader prints a warning.

## Common Engine Hooks

- `GetIntrinsicModifierName` is used to convert actives to passives.
- `OnAbilityFullyCast` is used for extra casts, dummy casters, or multi-target logic.
- `OnTakeDamage` is used for reactive triggers or damage-based bonuses.
- `Timers:CreateTimer` (from `scripts/vscripts/base/timers.lua`) is used for delayed sequences.
