# Ability KV Format (Awaken)

Use this when editing ability KV files. Some projects store per-hero KV in `scripts/npc/heros_ability/*.txt`.

## Structure

- Root: `"DOTAAbilities"`
- Each ability is a block with general fields and `AbilityValues` for specials.

Example:

```kv
"my_hero_my_ability"
{
  "AbilityBehavior" "DOTA_ABILITY_BEHAVIOR_UNIT_TARGET"
  "AbilityUnitTargetTeam" "DOTA_UNIT_TARGET_TEAM_ENEMY"
  "AbilityUnitTargetType" "DOTA_UNIT_TARGET_HERO | DOTA_UNIT_TARGET_BASIC"
  "AbilityCooldown" "12 11 10 9"

  "AbilityValues"
  {
    "damage" "100 150 200 250"
    "radius"
    {
      "value" "300"
      "affected_by_aoe_increase" "1"
    }
  }
}
```

## Notes

- `AbilityValues` supports inline values or nested `value` blocks.
- Talent and facet overrides are declared under the special value key.
- Some projects still use `AbilitySpecial` instead of `AbilityValues`; follow the file’s existing pattern.
- Use consistent spacing and quote style to avoid KeyValue parsing errors.
