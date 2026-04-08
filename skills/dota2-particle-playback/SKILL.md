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
4. Inspect the file before writing Lua.
5. Map the file structure to runtime playback.
6. Report the particle path, attach mode, and control points used.

## Rules

- Inspect the real `.vpcf` first whenever playback, reconstruction, or CP setup matters.
- Treat `m_Children` as a strong signal that the root file is a wrapper and must be expanded before judging runtime behavior.
- Read `m_controlPointConfigurations` for declared CP layout, then scan emitters, operators, initializers, and renderers for `m_nControlPoint`, `m_iControlPoint`, `m_nFilterCP`, and `m_iAttachType`.
- Follow child particle references before finalizing playback rules.
- Use `SetParticleControl` for value-based CPs and `SetParticleControlEnt` when the particle binds to an entity, bone, or attachment.
- If the file cannot be found or inspected, say visual parity cannot be guaranteed yet.

## Reference

See [vpcf-inspection.md](references/vpcf-inspection.md) for the file-resolution order, parse order, common keywords, and the output checklist.
