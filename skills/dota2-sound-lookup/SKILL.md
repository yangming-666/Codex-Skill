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
3. If the workspace contains `tools/soundevent_finder_gui`, use it first for VPK soundevent lookup. Do not guess event blocks from resource paths.
4. If the project has local soundevent source files, scan them before adding or changing local events.
5. If the code already contains a sound API call, scan it and resolve the concrete event or resource path.
6. Search `pak01_dir.vpk` when the event is not resolved locally.
7. Inspect the best-matching `soundevents/*.vsndevts` or `.vsndevts_c` block first.
8. Follow any referenced `sounds/*.vsnd_c` resource files when available.
9. Report the event name, resource path, source soundevent file, and any loop/fallback/stop relationship.

## Rules

- Treat `AbilitySound`, `EmitSound*`, `StopSound*`, `PrecacheSoundScript`, `PrecacheResource("soundfile")`, and `soundevents` references as lookup inputs, not final answers.
- Prefer the most specific file scope first: hero, item, addon, UI, then global.
- If local source soundevent files are available, prefer them over compiled `.vsndevts_c` files.
- If only compiled files are available, extract printable strings and search those strings for event names and resource hints.
- When scanning code, keep the API call and the resolved string argument together in the report.
- Do not claim a sound mapping is complete until the event file and the resource file have both been checked when both exist.
- In the `E:\PVE` project, use `tools/soundevent_finder_gui` for concrete Dota 2 event lookup. Its default VPK path is resolved from `E:\PVE\tools\soundevent_finder_gui` to `E:\SteamLibrary\steamapps\common\dota 2 beta\game\dota\pak01_dir.vpk`. If that path does not exist, pass the real absolute VPK path explicitly.
- When copying a vanilla event into a local `.vsndevts`, copy the full matched event block parameters (`volume`, `pitch`, `soundlevel`, `mixgroup`, `spread_radius`, limiter/layer/block fields, `vsnd_files`, `vsnd_duration`) unless intentionally changing them.

## Tools

Use `tools/soundevent_finder_gui` in `E:\PVE`:

```powershell
@'
from pathlib import Path
import sys
sys.path.insert(0, str(Path("tools/soundevent_finder_gui").resolve()))
from soundevent_finder_gui import SoundEventFinder

finder = SoundEventFinder(Path("tools/soundevent_finder_gui").resolve())
vpk = finder.resolve_vpk_path("")
finder.build_cache(vpk, force=False)

for query in [
    "sounds/weapons/hero/spectre/dagger_cast.vsnd",
]:
    print("====", query)
    for match in finder.search(query):
        print(match.relative_file)
        print(match.event_name)
        print(match.block_text)
'@ | python -
```

If `finder.resolve_vpk_path("")` points to a missing path, pass the known absolute VPK path:

```python
vpk = Path(r"E:\SteamLibrary\steamapps\common\dota 2 beta\game\dota\pak01_dir.vpk")
```

Use `scripts/lookup_sound.py` only when this project-specific tool is absent or unsuitable.

## Reference

See [sound-workflow.md](references/sound-workflow.md) for path resolution, search order, and output format.
