# VPCF Inspection

Use this reference after the root particle has been selected.

## Resolve Current Files

Resolve the content root in this order:

1. `DOTA2_CONTENT_ROOT`
2. `DOTA2_VANILLA_CONTENT_ROOT`
3. Detected `Steam\steamapps\common\dota 2 beta\content\dota`
4. Detected `SteamLibrary\steamapps\common\dota 2 beta\content\dota`

Fail fast if the exact VPCF cannot be opened. For native abilities with an unknown path, use the `dota2-ability` server-DLL extractor before searching particle directories.

## Parse the Contract

Read the root in this order:

1. `_class`, `m_nBehaviorVersion`, and `m_controlPointConfigurations`
2. `m_Children` and enabled `m_ChildRef` branches
3. CP fields such as `m_iControlPoint`, `m_nControlPoint`, `m_nCP`, `m_nCPInput`, `m_nFilterCP`, and `m_nOverrideCP`
4. Movement operators and initializers
5. Emitters, decay/stop operators, constant/random lifetime, and endcaps
6. Renderers only when visual duplication, orientation, tint, or material behavior matters

Follow a child when it:

- consumes a caller-facing CP;
- owns or modifies movement/lifetime;
- is the requested visual leaf or endcap;
- conflicts with the root contract.

Do not expand children that cannot affect caller inputs, movement, timing, or the requested visual.

## Interpret CPs

- Name a CP from its consumer and caller evidence, never from its number.
- Distinguish world/entity attachment from scalar/vector parameters.
- Treat `x`, `y`, and `z` separately only for packed or conflicting vectors.
- Mark a CP as internal when an operator generates it and only descendants consume it.
- Use `direct` confidence for explicit caller/consumer agreement, `inferred` for consistent multi-file evidence, and `unknown` when no consumer proves the meaning.

Build a CP table only for packed, conflicting, projectile, or undocumented contracts:

| CP/component | Consumer | Caller value | Meaning | Confidence |
|---|---|---|---|---|

## Classify Movement

- `engine-driven`: a projectile API owns position and standard projectile CPs.
- `particle-driven`: VPCF velocity, attraction, path, or interpolation operators own movement.
- `caller-driven`: Lua must update CPs over time.

Check `C_OP_AttractToControlPoint`, `C_OP_MaxVelocity`, velocity initializers, path/interpolation operators, and orientation operators. A velocity override CP is not a destination without a destination consumer.

Check `C_OP_StopAfterCPDuration`, emitter duration, particle lifetime, `C_OP_Decay`, and endcap timing. If distance changes but the stop position does not, test lifetime/speed coupling before changing the destination.

## Map to Lua

- Match the proven `PATTACH_*` mode.
- Set every proven caller CP and leave internal derived CPs alone.
- Set particle-driven destinations once.
- Release finite one-shots after setup; explicitly destroy persistent/follow particles at the owning lifecycle boundary.
- Use a minimal wrapper only for a proven root/child CP conflict.

## Focused Validation

Test only unresolved hypotheses. For moving effects, short/long distance usually distinguishes destination errors from lifetime cutoffs. Disable or separate an endcap only if it hides the body movement.

## Output Checklist

- Root VPCF and relevant children
- Native/custom resource-selection evidence
- Attach mode
- Caller CPs and internal CPs
- Movement owner
- Lifetime and cleanup
- Precache owner
- Remaining uncertainty
