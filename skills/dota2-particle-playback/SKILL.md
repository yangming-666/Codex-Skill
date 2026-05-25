---
name: dota2-particle-playback
description: Inspect Dota 2 particle `.vpcf` files and determine the correct playback attach, control points, and timing before writing Lua or KV that plays effects. Use when a task involves playing, recreating, modifying, or debugging Dota 2 particles and you need to inspect the actual particle file first.
---

# Dota 2 Particle Playback

## Environment

- **Dota 2 Content Root**: `E:\SteamLibrary\steamapps\common\dota 2 beta\content\dota` (derived from `$env:DOTA2_VANILLA_CONTENT_ROOT`)

## Workflow

1. Resolve the Dota 2 content root.
2. Find the exact `.vpcf` file for the particle path.
3. Parse the file in this order: wrapper, control-point contract, attach bindings, timing/lifetime, child files.
4. Build a control-point consumer table before assigning any semantic meaning to a CP component.
5. Inspect the file before writing code that plays the particle.
6. Map the file structure to runtime playback.
7. Report the particle path, attach mode, and the CP component meanings that were actually consumed by the file tree.

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
