---
name: dota2-particle-playback
description: Identify and play Dota 2 particles correctly by using current `server.dll` evidence for vanilla ability resource selection and real `.vpcf` files for attach, control-point, movement, lifetime, child, and precache contracts. Use for particle playback, recreation, modification, or debugging; avoid filename guessing and unnecessary full-family scans.
---

# Dota 2 Particle Playback

## Evidence Boundary

Use each source only for what it proves:

- Current `server.dll`: which resources a native ability references.
- Current VPCF tree: attach drivers, CP consumers, movement operators, emitters, lifetime, and children.
- Current Lua/native call evidence: caller-provided attach mode, CP values, API choice, and cleanup.
- Runtime test: residual ambiguity and visual parity.

DLL strings do not prove playback parameters. VPCF preview drivers do not necessarily prove caller inputs.

## Workflow

1. Resolve the current Dota content root from `DOTA2_CONTENT_ROOT` or `DOTA2_VANILLA_CONTENT_ROOT`, then detected Steam installs.
2. Select the exact root particle:
   - For a vanilla native ability with an unknown or disputed particle, use the `$dota2-ability` DLL workflow and `scripts\inspect-server-ability-resources.ps1`.
   - For a known custom/root path, skip DLL extraction.
   - Do not guess from filenames or scan an entire hero particle directory when DLL/current caller evidence identifies the resource.
3. Open the exact root VPCF. Follow only child branches that consume caller CPs, own movement/lifetime, or materially contribute the requested visual. Do not recursively dump unrelated visual leaves.
4. Establish the caller contract:
   - Prefer a current known-good caller or native-call evidence for attach mode and CP values.
   - Verify those values against actual VPCF consumers.
   - Separate caller inputs from internally generated CPs.
5. For projectile-like effects, classify movement as engine-driven, particle-driven, or caller-driven before choosing `CreateTrackingProjectile`, manual `ParticleManager`, or timer updates.
6. Check emit duration, particle lifetime, decay, stop operators, endcaps, and cleanup.
7. Precache the root VPCF through the repository-sanctioned narrowest owner.
8. Run focused runtime tests only for unresolved parameters. Preserve confirmed-good facts and stop retesting confirmed-bad candidates.

## Analysis Depth

Use the lightest analysis that establishes correctness:

- Simple one-shot with a proven caller: verify the root, relevant CP consumers, lifetime, and precache. No full CP table.
- Follow/buff particle: verify attachment drivers, caller CPs, endcap behavior, and cleanup.
- Projectile or moving particle: verify movement owner, destination/speed/orientation CPs, and cutoff.
- Packed, conflicting, or undocumented CPs: build a per-component consumer table and assign confidence.

Never infer CP meaning from its index or filename.

## Playback Rules

- Treat `m_Children` as a wrapper signal, but inspect only relevant active branches.
- Treat `m_nOverrideCP` as an input reference whose meaning must be proven by its operator and caller.
- Set particle-driven destinations once unless the contract explicitly makes Lua the movement owner.
- Avoid per-frame Lua motion when the VPCF or projectile engine owns movement.
- Do not use `CreateTrackingProjectile` for a nonstandard manual CP contract.
- Do not guess HSV/tint CPs or overwrite internally derived CPs.
- If root and child consume the same CP component incompatibly, use a minimal wrapper/remap instead of forcing one value to satisfy both.
- Suppress or separate endcaps only when they obscure movement diagnosis.
- Precache the caller's root VPCF; do not list every child unless project/runtime evidence requires it.

## Validation

For ambiguous moving effects, test the smallest matrix that distinguishes the remaining hypotheses:

- short and long distance;
- destination set once versus caller-updated, only if ownership is unclear;
- candidate packed-CP values supported by actual consumers;
- lifetime-derived speed/duration when a cutoff exists.

Do not run a broad parameter sweep after native-call and VPCF evidence already agree.

## Report

Report only consumed evidence:

- exact root VPCF and relevant children;
- why the particle belongs to the target ability;
- attach mode and caller CPs;
- movement owner and update policy;
- lifetime/cleanup;
- precache entry;
- remaining uncertainty and focused test, if any.

See `references/vpcf-inspection.md` for field-level inspection and portable root resolution.
