# Runtime Dump Collection Template

## 1) Panorama command

Use one-line command in Panorama console:

```js
gDZSJGameFlow.DumpEndLayoutGeometry()
```

Copy the full line:

- `[EndLayoutDump] {...}`
- or `[LayoutDump] {...}`

Save each case to a separate file:

- `runtime_victory_first_clear.txt`
- `runtime_victory_non_first_clear.txt`
- `runtime_defeat.txt`
- `runtime_reward_1.txt`
- `runtime_reward_2.txt`
- `runtime_reward_3plus.txt`

## 2) Case matrix (required)

- victory + first clear
- victory + non-first clear
- defeat
- normal rewards: 1, 2, 3+

## 3) Runtime checker command

```bash
python scripts/check_runtime_layout.py \
  --contract <contract.json> \
  --dump <runtime_dump.txt> \
  --map <mapping.json> \
  --relation-rules <relations.json> \
  --required-selectors ".EndMainPanel,.EndSummaryCard,.EndResultTitle,.EndStageName,.EndRemainHp,.EndRatingContainer,.EndDamagePanel,.EndRewardPanel,.EndRewardTitle,.EndUnlockBanner,.EndDiamondGroup,.EndNormalGroup,.EndButtonBar,.EndPrimaryButton,.EndSecondaryButton,.EndDamageRow,.EndDamageRank,.EndDamageAvatar,.EndDamageName,.EndDamageBarBg,.EndDamageValue,.EndDamageMvp" \
  --require-visible-selectors ".EndResultTitle,.EndStageName,.EndRemainHp,.EndRatingContainer,.EndRewardTitle,.EndUnlockBanner,.EndPrimaryButton,.EndSecondaryButton,.EndDamageRow,.EndDamageRank,.EndDamageAvatar,.EndDamageName,.EndDamageBarBg,.EndDamageValue" \
  --enforce-inside-parent-mapped
```

## 4) Interpretation rules

- If required selector is missing: runtime tree or dump profile is incomplete.
- If visible check fails: likely clipping/collapse/wrong parent chain.
- If relation fails: alignment/gap/ratio drift exists under runtime scaling.
- All cases must pass before claiming replica done.
