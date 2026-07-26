---
name: dota2-ability
description: Author or rewrite Dota 2 abilities and modifiers with Lua + KV, including vanilla replication, targeting, projectiles, buffs, debuffs, damage, and ability-owned presentation. Use current vanilla KV and `server.dll` resource evidence before implementation; delegate particle and sound playback contracts to their dedicated skills. Do not use for generic game-mode, test-mode, shop, backend, or UI logic.
---

# Dota 2 Ability

## Scope

Use this skill only when the primary object is an ability, modifier, or ability KV contract. Do not use it for generic Lua systems, test commands, Panorama, match flow, shops, accounts, services, or unrelated orchestration.

## Evidence Order

Use the newest local game build and project sources. Treat evidence according to what it can prove:

1. Project Lua/KV: current addon behavior and integration constraints.
2. Current vanilla KV: ability data, targeting, cast fields, specials, and hero registration.
3. Current `server.dll`: native ability-to-resource association.
4. Current VPCF/soundevent files: resource playback contracts.
5. Runtime comparison: final timing and visual validation.
6. `tools/Dota2 ability` or public Lua replicas: fallback hypotheses only.

Never let an older or third-party Lua recreation override current KV, DLL, VPCF, or observed runtime evidence.

## Resolve Sources

Resolve paths without hardcoding a drive:

- Vanilla KV: `DOTA2_VANILLA_KV_ROOT`, then repo-relative `Dota2 原版游戏配置`.
- Dota content root: `DOTA2_CONTENT_ROOT` or `DOTA2_VANILLA_CONTENT_ROOT`, then detect `Steam\steamapps\common\dota 2 beta\content\dota` or its `SteamLibrary` variant.
- Native server binary: `DOTA2_SERVER_DLL`, or derive `game\dota\bin\win64\server.dll` from the content root, then detect Steam installs.
- Optional reference library: repo-relative `tools/Dota2 ability`.

Fail fast when a required source cannot be resolved. State which resolved sources are being used.

## Workflow

1. Inspect the owning project ability/KV and classify the requested change as data-only, behavior, presentation, or full replication.
2. For a vanilla rewrite, read the current vanilla hero/ability KV and record only the fields the implementation consumes.
3. For native presentation resources, run:

   ```powershell
   & "<dota2-ability-skill>\scripts\inspect-server-ability-resources.ps1" `
     -Query "dark_willow_bedlam"
   ```

   The script accepts a raw KV ability name or exact `CDOTA_Ability_*` class and selects the highest-confidence native resource block. Use that block to identify candidate particles, models, and sound events. Do not guess from filenames or recursively scan an entire hero particle directory when the DLL identifies the resource set.
4. Do not infer attach type, control-point values, projectile API, or lifetime from DLL string order. Use `$dota2-particle-playback` for VPCF playback and `$dota2-sound-lookup` for sound events.
5. Implement the smallest owning KV/Lua change. Keep tunable numbers in KV and sequencing/behavior in Lua.
6. Integrate every new runtime asset through the repository-sanctioned, narrowest precache path.
7. Validate only unresolved behavior. Do not build broad candidate matrices when current native calls and resource contracts already establish the answer.

## Implementation Rules

- Guard server logic with `if not IsServer() then return end`.
- Forward-declare local helpers called before their definitions.
- Use `Timers:CreateTimer` for ability-owned sequences; avoid global state.
- Reuse project targeting, battlefield-boundary, projectile, damage, and configuration helpers instead of duplicating them.
- For random projectile directions, analytically sample the legal intervals produced by the project battlefield boundary. Do not use rejection sampling or substitute obstacle AABBs for the playable frame.
- Use `ConfigRuntime` for gameplay KV when required by the repository.
- Do not call a vanilla ability merely to borrow its presentation unless the task explicitly wants the engine-side cast and its gameplay side effects.
- Treat built-in modifier names as engine-provided; do not redefine them.

## Vanilla Replication

Replicate only the layers the task requires:

- Cast: behavior, target contract, cast point, gesture, sound, and cast particle.
- Travel: projectile type, movement owner, speed, radius, and visual lifetime.
- Impact: damage/control rules, area, impact presentation, and cleanup.
- State: modifiers, dispels, immunity, interruption, death, and refresh behavior.

For a full-parity claim, verify gameplay timing and visible behavior at runtime. Report:

- Vanilla KV fields consumed.
- DLL resources selected and their target native ability class.
- Particle/sound contracts verified by the dedicated skills.
- Runtime precache coverage.
- Intentional deviations and unverified edge cases.

## Resource Rules

- A DLL resource string proves native association, not correct custom playback.
- Precache the root resource called by Lua; allow normal child dependency loading unless project evidence requires explicit children.
- Prefer the owning ability/unit precache block or project maintenance tool.
- Do not place ability-specific assets in a global static list without repository policy.
- If a maintenance command rewrites unrelated user work, make the narrow source edit and report the deferred command.

## References

Load only references needed for the current task:

- `references/ability-kv-format.md`: KV authoring.
- `references/lua-ability-patterns.md`: Lua hooks and patterns.
- `references/built-in-modifier-names.md`: engine modifier names.
- `references/awaken-ability-architecture.md` and `references/awaken-ability-examples.md`: awakening work.
- `assets/ability-template/`: new ability templates.
