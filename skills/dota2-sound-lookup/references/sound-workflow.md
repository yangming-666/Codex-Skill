# Sound workflow

## Resolve the archive

Use this order:

1. Explicit `--vpk-path` or tool parameter.
2. Workspace `tools/resolve_project_paths.ps1` result `pak01_vpk`.
3. `DOTA2_VPK_PATH`.
4. Standard Steam library probing by the bundled script.
5. Fail with the checked candidates; do not silently substitute another archive.

## Search inputs

- KV: `AbilitySound`.
- Lua/Panorama: `Game.EmitSound`, `EmitSound*`, `StopSound*`, `PrecacheSoundScript`, and `PrecacheResource("soundfile", ...)`.
- Local sources: `content/<addon>/soundevents/*.vsndevts`.
- Compiled events/resources: `soundevents/*.vsndevts_c`, `sounds/*.vsnd_c`.
- Source helper: `scripts/lookup_sound.py --source <path>`.

## Search order

1. Preserve the source API/KV field and token.
2. Search local project source soundevents.
3. Search hero/item-specific vanilla soundevents.
4. Search shared gameplay soundevents.
5. Search addon/UI scopes.
6. Search global resources.
7. Follow event dependencies and resource paths.

Treat compiled files as binary containers. Printable-string extraction can establish candidates but does not justify reconstructing unobserved event parameters.

## Report

1. Event or alias.
2. Source soundevent file and evidence type.
3. Underlying resource path.
4. One-shot or loop behavior.
5. Stop/fade/layer/limiter relationships.
6. Originating API and string when lookup began from code.
7. Remaining ambiguity.
