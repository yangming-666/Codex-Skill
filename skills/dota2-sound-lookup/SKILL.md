---
name: dota2-sound-lookup
description: Inspect Dota 2 sound events and resource paths from vanilla KV, Lua, Panorama, local soundevent sources, or `pak01_dir.vpk`. Use when a task needs to identify, verify, or resolve `AbilitySound`, `EmitSound`, `EmitSoundOn`, `EmitSoundOnLocationWithCaster`, `StopSound*`, `PrecacheSoundScript`, `PrecacheResource("soundfile")`, `.vsndevts`, `.vsndevts_c`, or `.vsnd_c` entries before writing gameplay or UI code.
---

# Dota 2 Sound Lookup

## Overview

Resolve a Dota 2 sound request into the exact sound event and underlying resource file. Do not guess from ability names or voice line names alone.

## Workflow

1. Extract the source token from vanilla KV, Lua, or Panorama code.
2. Normalize the token to an event name, sound alias, or resource hint.
3. If the project has local soundevent source files, scan them first with `scripts/lookup_sound.py --source ...`.
4. If the code already contains a sound API call, scan it with `scripts/lookup_sound.py --source ...`.
5. Search `pak01_dir.vpk` with the helper script when the event is not resolved locally.
6. Inspect the best-matching `soundevents/*.vsndevts` or `soundevents/*.vsndevts_c` file first.
7. Follow any referenced `sounds/*.vsnd_c` resource files.
8. Report the event name, resource path, and any loop/fallback/stop relationship.

## Rules

- Treat `AbilitySound`, `EmitSound*`, `StopSound*`, `PrecacheSoundScript`, `PrecacheResource("soundfile")`, and `soundevents` references as lookup inputs, not final answers.
- Prefer the most specific file scope first: hero, item, addon, UI, then global.
- If local source soundevent files are available, prefer them over compiled `.vsndevts_c` files.
- If only compiled files are available, extract printable strings and search those strings for event names and resource hints.
- When scanning code, keep the API call and the resolved string argument together in the report.
- Do not claim a sound mapping is complete until the event file and the resource file have both been checked when both exist.

## Tools

Use `scripts/lookup_sound.py` to search the Dota 2 VPK archive, scan Lua/Panorama source for sound API calls, and print candidate sound events plus resource paths.

## Reference

See [sound-workflow.md](references/sound-workflow.md) for path resolution, search order, and output format.
