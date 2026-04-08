# Sound Workflow

Use this reference when a Dota 2 task needs the exact sound event name or the underlying sound resource.

## Known archive path

The known Dota 2 archive for this workspace is:

`E:\SteamLibrary\steamapps\common\dota 2 beta\game\dota\pak01_dir.vpk`

If that path is not available, resolve it in this order:

1. `DOTA2_VPK_PATH`
2. A detected Steam install ending in `dota 2 beta/game/dota/pak01_dir.vpk`
3. Ask the user for the VPK path

## Search inputs

Use these sources as lookup tokens:

- KV: `AbilitySound`
- Lua / Panorama code: `Game.EmitSound`, `EmitSound`, `EmitSoundOn`, `EmitSoundOnLocationWithCaster`, `StopSound`, `StopSoundOn`, `StopSoundEvent`, `PrecacheSoundScript`, `PrecacheResource("soundfile", ...)`
- Local project soundevent sources: `content/<addon>/soundevents/*.vsndevts`
- Soundevent files: `soundevents/*.vsndevts_c`
- Resource files: `sounds/*.vsnd_c`
- Source scan helper: `scripts/lookup_sound.py --source <path>`

## Search order

1. Search the source token in vanilla KV or code.
2. Search local project soundevent sources first when they exist.
3. Search the matching `soundevents/*.vsndevts_c` file by name scope.
4. Search the extracted strings inside that file for event names, aliases, and `sounds/...` references.
5. If needed, search `sounds/*.vsnd_c` for the concrete resource file.

Scope order:

- Hero-specific files first: `soundevents/game_sounds_heroes/*.vsndevts_c`
- Then shared gameplay files: `soundevents/game_sounds*.vsndevts_c`
- Then addon/UI-specific files
- Then global `sounds/*.vsnd_c`

## Interpreting compiled files

`pak01_dir.vpk` mostly contains compiled `.vsndevts_c` and `.vsnd_c` files.

- Treat compiled files as binary containers.
- Use printable-string extraction to recover event names, resource hints, and metadata keys.
- When available, prefer source `.vsndevts` text over compiled output.

## Output format

Report results in this order:

1. Event or alias name
2. Resource file path
3. Loop/one-shot behavior
4. Stop/fade relationship, if any
5. Fallback or variant notes
6. If the lookup started from code, the originating API and string argument

If the mapping is ambiguous, say which file scope was inspected and which piece is still missing.
