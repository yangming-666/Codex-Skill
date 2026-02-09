# Awaken Ability Examples

This reference summarizes frequent modification patterns observed in Awaken hero abilities. Treat these as optional patterns for Awaken-style projects.

## Pattern Index

- Passive conversions: move actives into intrinsic modifiers.
- AbilitySpecial overrides: adjust values by difficulty or awakening state.
- Multi-cast and dummy casters: call `OnSpellStart` multiple times.
- Projectiles: implement custom linear/tracking projectile logic.
- Triggered attacks: use `PerformAttack` on damage or casts.
- Charge/cooldown rework: change `AbilityCharges` and restore time.

## Examples

- Passive conversion with refresh: use `GetIntrinsicModifierName` and refresh modifiers on upgrade.
- Multi-target casts: in `OnAbilityFullyCast`, find enemies and invoke `OnSpellStart` per target.
- Custom projectile AOE: in `OnProjectileHit`, find units in radius and apply damage + debuffs.
- Timed extra triggers: use `Timers:CreateTimer` to schedule extra activations.
- Difficulty scaling: read `GameRules:GetCustomGameDifficulty()` and scale specials.
