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
- A CP's semantic meaning comes from its consumers, not from the name of the particle or the Lua value you plan to pass in.
- For packed CP vectors, analyze `x`, `y`, and `z` independently. A single CP index can carry unrelated meanings across different components.
- If the same CP component is consumed in multiple files, document the common meaning only after checking all of them.
- If a component is never consumed explicitly, mark it as unknown instead of inferring a meaning from a nearby effect.

Parse order that works well on real files:

1. Read the header and class/version.
2. Check `m_Children`.
3. Check `m_controlPointConfigurations`.
4. Search the file for CP fields.
5. Check emitters/operators/initializers/renderers for timing or filter dependencies.
6. Inspect each child file and merge the runtime contract.
7. Build a per-component table:
   - CP index
   - vector component
   - consumer file
   - consumer field
   - runtime meaning
   - confidence
8. Only after the table is complete, translate the result into runtime playback inputs.

Practical refinements:

- If `m_Children` is present, treat the root as a wrapper until the active leaf or endcap tree is mapped.
- If the particle family has siblings such as `*_launch`, `*_trail*`, `*_tracking`, and `*_explosion`, inspect them together and merge CP rules across the family before naming caller-facing inputs.
- Keep caller-facing inputs separate from internal derived CPs:
  - caller-facing inputs are the values the Lua caller should set immediately after `CreateParticle`
  - internal derived CPs are only meaningful inside the child tree and should not be assumed mandatory for the caller
- Record confidence per CP meaning:
  - `direct` for explicit file bindings
  - `inferred` for merged child-tree behavior
  - `low-confidence` for single-branch hints

## Map to playback

- Match the attach type to the particle definition instead of forcing `PATTACH_WORLDORIGIN`.
- If the particle uses more than one CP, set all required CPs before assuming it is complete.
- When a child particle is referenced, do not treat the parent file's preview CP layout as the final runtime contract until the child files are checked.
- When a packed CP drives multiple visual layers, consider a small runtime perturbation test only after the file tree has been mapped; use it to confirm uncertain axis meanings, not to replace file inspection.

## Output checklist

When reporting a result, include:

- The exact `.vpcf` path
- Whether the file is a wrapper or a leaf
- The attach mode used
- The CP indices that matter
- The fields that drove the decision
- Any child particle files that had to be inspected
- Any missing information that prevents exact parity
- A short caller-facing playback snippet when the particle has a stable runtime contract
- A CP summary table when the particle tree is non-trivial
