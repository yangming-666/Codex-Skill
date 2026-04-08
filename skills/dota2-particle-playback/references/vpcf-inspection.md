# VPCF Inspection

Use this reference when you need to determine how a Dota 2 particle should be played from its actual `.vpcf` file.

## Resolve the file

1. Start from the Dota 2 content root.
2. Append `particles/...` to reach the particle path.
3. Open the exact `.vpcf` file before deciding on CPs or attach mode.

Portable resolution order:

1. `DOTA2_CONTENT_ROOT`
2. A detected Steam install that ends at `dota 2 beta/content/dota`
3. Ask the user for the install path if nothing is found

Useful PowerShell patterns:

```powershell
if ($env:DOTA2_CONTENT_ROOT) { Join-Path $env:DOTA2_CONTENT_ROOT 'particles' }
```

```powershell
$roots = @()
Get-PSDrive -PSProvider FileSystem | ForEach-Object {
  $roots += (Join-Path $_.Root 'Steam\steamapps\common\dota 2 beta\content\dota')
  $roots += (Join-Path $_.Root 'SteamLibrary\steamapps\common\dota 2 beta\content\dota')
}
$roots | Where-Object { Test-Path $_ }
```

## Inspect the file

Look for these fields first:

- `m_nBehaviorVersion`
- `_class`
- `m_controlPointConfigurations`
- `m_Children` and `m_ChildRef`
- `m_drivers`
- `m_iAttachType`
- `m_iControlPoint`
- `m_nControlPoint`
- `m_nCP1`, `m_nCP2`, and similar CP fields
- `m_nFilterCP`
- `m_nFirstMultipleOverride_BackwardCompat`

Interpretation rules:

- `m_nBehaviorVersion` and `_class` help you tell which generation of VPCF syntax you are reading.
- `m_iAttachType` tells you how the particle expects to bind at runtime.
- `m_iControlPoint` means a specific control point gets its own driver or follow binding.
- Control-point operators tell you which CPs must be set from Lua.
- `m_nFilterCP` usually means one CP is used as a selector or mask, not just a position/value.
- Child references mean the root file is a wrapper; inspect children too.
- Preview data in the file is not always the runtime playback contract, so verify the actual drivers and operators.

Parse order that works well on real files:

1. Read the header and class/version.
2. Check `m_Children`.
3. Check `m_controlPointConfigurations`.
4. Search the file for CP fields.
5. Check emitters/operators/initializers/renderers for timing or filter dependencies.
6. Inspect each child file and merge the runtime contract.

## Map to playback

- Use `SetParticleControl` for literal positions, values, and timing CPs.
- Use `SetParticleControlEnt` when the CP should follow an entity or attachment.
- Match the attach type to the particle definition instead of forcing `PATTACH_WORLDORIGIN`.
- If the particle uses more than one CP, set all required CPs before assuming it is complete.
- When a child particle is referenced, do not treat the parent file's preview CP layout as the final runtime contract until the child files are checked.

## Output checklist

When reporting a result, include:

- The exact `.vpcf` path
- Whether the file is a wrapper or a leaf
- The attach mode used
- The CP indices that matter
- The fields that drove the decision
- Any child particle files that had to be inspected
- Any missing information that prevents exact parity
