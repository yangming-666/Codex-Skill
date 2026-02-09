# Lua Ability Patterns

Use this reference when creating or rewriting Lua abilities and modifiers in any Dota 2 custom game.

## File Placement

- Ability scripts: `scripts/vscripts/` (often under `hero/hero_<name>/` in hero-split projects)
- Awakening modifier: `modifier_<hero>_awaken.lua` (project-specific)
- Shared base: `scripts/vscripts/modifiers/modifier_awakening.lua` (project-specific)

## Common Patterns

### Override ability specials

- If the project has an awakening system, use `modifier_base_awakening` and implement:
  - `GetModifierOverrideAbilitySpecial`
  - `GetModifierOverrideAbilitySpecialValue`
- Read base values with `GetLevelSpecialValueNoOverride`.
- Gate by `GameRules:GetCustomGameDifficulty()` if needed.

### Passive conversion

- Use `GetIntrinsicModifierName` to attach a hidden modifier.
- Apply logic in `OnAttackLanded`, `OnTakeDamage`, or `OnCreated`.

### Multi-cast / extra targets

- Listen in `OnAbilityFullyCast` and manually call `OnSpellStart`.
- Use dummy casters for repeated casts when the base ability expects a caster.

### Projectiles and AOE

- Create projectiles with `ProjectileManager`.
- Handle impact in `OnProjectileHit` and apply damage or modifiers explicitly.

### Timed sequences

- Use `Timers:CreateTimer` for delayed effects or repeated loops.
- Always check `IsNull()` / `IsAlive()` before acting on entities.

## Safety Checks

- Validate ability and caster are not nil.
- Respect server-only execution; guard with `if not IsServer() then return end`.
- Avoid global state when per-instance state is needed.
