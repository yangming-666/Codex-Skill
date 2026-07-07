---
name: dota2-particle-playback
description: Inspect Dota 2 particle `.vpcf` files and determine the correct playback attach, control points, and timing before writing Lua or KV that plays effects. Use when a task involves playing, recreating, modifying, or debugging Dota 2 particles and you need to inspect the actual particle file first.
---

# Dota 2 Particle Playback

## Overview

Turn an actual particle file into a correct playback call. Do not guess control points, attach modes, or lifetime behavior from the particle name alone.

## Workflow

1. Resolve the Dota 2 content root.
2. Find the exact `.vpcf` file for the particle path.
3. Parse the file in this order: wrapper, control-point contract, attach bindings, timing/lifetime, child files.
4. Build a control-point consumer table before assigning any semantic meaning to a CP component.
5. For projectile-like particles, classify the movement contract before choosing `CreateTrackingProjectile`, manual `ParticleManager`, or timer-driven CP updates.
6. Inspect the file before writing code that plays the particle.
7. Map the file structure to runtime playback.
8. Report the particle path, attach mode, CP component meanings, movement owner, and timing limits that were actually consumed by the file tree.

## Rules

- Inspect the real `.vpcf` first whenever playback, reconstruction, or CP setup matters.
- Treat `m_Children` as a strong signal that the root file is a wrapper and must be expanded before judging runtime behavior.
- Once a wrapper is detected, do not finalize playback from the root file alone; recursively inspect child particles until the active runtime tree is covered.
- Read `m_controlPointConfigurations` for declared CP layout, then scan emitters, operators, initializers, and renderers for `m_nControlPoint`, `m_iControlPoint`, `m_nFilterCP`, `m_nCPInput`, and `m_iAttachType`.
- For every CP index, identify each consumer of `x`, `y`, and `z` separately before naming the runtime meaning of that component.
- Do not label a CP component as "radius", "duration", "speed", or similar until you can point to the exact operators/initializers/child files that consume that component.
- If a component has multiple consumers, prefer the intersection of all observed consumers over any single file's apparent intent.
- Follow child particle references before finalizing playback rules.
- If a particle uses one CP as a packed parameter vector, treat each vector component as an independent contract and document the consumers for each axis.
- Never infer CP meaning from its index. CP1 can be a target point, orientation point, speed override, packed scalar vector, or direction input depending on the operators that consume it.
- For projectile-like particles, explicitly identify the movement owner:
  - `engine-driven` when Dota projectile APIs are expected to move the particle and feed standard CPs.
  - `particle-driven` when operators such as attraction, velocity, max-velocity override, path, or CP interpolation move particles inside the VPCF.
  - `caller-driven` when Lua must update one or more CPs over time.
- For particle-driven projectiles, identify target CPs, velocity/speed override CPs, orientation CPs, and lifetime cutoff before writing Lua.
- Treat `C_OP_MaxVelocity` with `m_nOverrideCP` as a possible speed/velocity parameter, not as a target, until confirmed by consumers or runtime testing.
- If the file contains `C_OP_StopAfterCPDuration`, `C_OP_Decay`, finite emit duration, or short particle lifetime, make playback speed/duration lifetime-aware; fixed speed across different distances can stop at the same world position.
- Do not update an attractor or destination CP every frame unless the VPCF contract says the caller owns movement. For particle-driven projectiles, set destination/parameter CPs once and let the particle simulate.
- Use `CreateTrackingProjectile` only after confirming the VPCF matches the engine projectile CP contract. Non-standard contracts, such as separate target and speed CPs, usually need manual `ParticleManager` setup.
- Suppress or separate endcaps while validating projectile body movement; endcaps can hide that the body stopped early or teleported.
- For ambiguous projectile VPCFs, run a distance sweep and parameter matrix before finalizing:
  - short, medium, and long target distances
  - destination CP set once vs updated over time
  - speed CP as `Vector(speed, 0, 0)` vs target/world values when consumers are unclear
  - visual duration derived from distance when lifetime limits exist
- If the file cannot be found or inspected, say visual parity cannot be guaranteed yet.
- Separate "external playback inputs" from "internal derived inputs":
  - External inputs are the CPs the caller should set from Lua/KV after `CreateParticle`.
  - Internal derived inputs are CPs only consumed or re-emitted inside the particle tree and should not be guessed as mandatory caller inputs unless the tree proves it.
- When a CP is consumed by a child particle, record whether that child is a visual leaf, a helper layer, or an endcap. Do not elevate a helper-only CP to a root-level requirement without evidence from the full tree.
- Assign a confidence label to each CP meaning:
  - `direct` when the file explicitly binds the component.
  - `inferred` when the meaning comes from multiple consumers or child propagation.
  - `low-confidence` when the meaning is only weakly implied by one branch.

## Reference

See [vpcf-inspection.md](references/vpcf-inspection.md) for the file-resolution order, parse order, common keywords, and the output checklist.
