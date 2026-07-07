# Panorama JavaScript API2 (ModDota Wiki)

Use this reference to guide Panorama JS API usage. For full signatures and edge cases, consult the ModDota page:
https://iwasinminedream.github.io/moddota.github.io/api/panorama/api

This is a curated API2 index. Verify details against the wiki when precision matters.

## Core Globals

### `$` (core helpers)

- `$.Msg`, `$.Warning`
- `$.GetContextPanel`
- `$.CreatePanel`, `$.CreatePanelWithProperties`
- `$.RegisterEventHandler`
- `$.RegisterForUnhandledEvent`
- `$.DispatchEvent`, `$.DispatchEventAsync`
- `$.Schedule`, `$.CancelScheduled`
- `$.Localize`, `$.LocalizeSafe`, `$.LocalizeAndReplace`, `$.LocalizeAndReplaceSafe`

### `GameEvents`

- `GameEvents.Subscribe`
- `GameEvents.Unsubscribe`
- `GameEvents.SendCustomGameEventToServer`
- `GameEvents.SendEventClientSide`

### `CustomNetTables`

- `CustomNetTables.GetTableValue`
- `CustomNetTables.SubscribeNetTableListener`
- `CustomNetTables.UnsubscribeNetTableListener`

### `GameUI`

- `GameUI.GetClickBehaviors`, `GameUI.SetClickBehaviors`
- `GameUI.GetCursorPosition`
- `GameUI.GetHUDRootUI`, `GameUI.GetRootUI`
- `GameUI.SetMouseCallback`
- `GameUI.TriggerMouseCallback`
- `GameUI.CustomUIConfig`

### `Game`

- `Game.GetLocalPlayerID`
- `Game.GetGameTime`, `Game.GetGameFrameTime`
- `Game.GetState`
- `Game.IsPaused`, `Game.IsGamePaused`
- `Game.EmitSound` / `Game.StopSound` - resolve the event/resource name with `$dota2-sound-lookup` before wiring UI playback or stop logic.

### `Players`

- `Players.GetLocalPlayer`
- `Players.GetPlayerHeroEntityIndex`
- `Players.GetSelectedEntities`
- `Players.GetPlayerName`
- `Players.GetTeam`, `Players.GetTeamID`
- `Players.GetGold`, `Players.GetGoldPerMin`

### `Entities`

- `Entities.GetAbsOrigin`, `Entities.GetForwardVector`, `Entities.GetHealth`, `Entities.GetMaxHealth`
- `Entities.IsAlive`, `Entities.IsHero`, `Entities.IsBuilding`, `Entities.IsCreature`, `Entities.IsNeutralUnitType`
- `Entities.GetUnitName`, `Entities.GetOwner`, `Entities.GetOwnerEntityID`
- `Entities.GetTeamNumber`
- `Entities.GetAbilityByName`, `Entities.GetItemInSlot`

### `Abilities`

- `Abilities.GetLevel`, `Abilities.GetCooldownTimeRemaining`, `Abilities.GetCooldown`, `Abilities.GetManaCost`
- `Abilities.GetAbilityName`, `Abilities.GetAbilityTextureName`
- `Abilities.IsCooldownReady`, `Abilities.IsActivated`, `Abilities.IsPassive`
- `Abilities.GetSpecialValueFor`, `Abilities.GetLevelSpecialValueFor`

### `Items`

- `Items.GetItemName`, `Items.GetItemCost`
- `Items.GetCooldownTimeRemaining`
- `Items.GetCurrentCharges`, `Items.GetSecondaryCharges`

### `Buffs`

- `Buffs.GetName`, `Buffs.GetDuration`, `Buffs.GetRemainingTime`
- `Buffs.GetCaster`, `Buffs.GetAbility`
- `Buffs.GetStackCount`, `Buffs.IsDebuff`

## Panel API (common methods)

- `panel.FindChildInLayoutFile`, `panel.FindChildTraverse`
- `panel.GetChild`, `panel.GetChildCount`, `panel.GetParent`
- `panel.SetParent`, `panel.RemoveAndDeleteChildren`, `panel.DeleteAsync`
- `panel.AddClass`, `panel.RemoveClass`, `panel.ToggleClass`, `panel.SwitchClass`, `panel.BHasClass`
- `panel.SetHasClass`
- `panel.SetPanelEvent`
- `panel.BLoadLayout`, `panel.BLoadLayoutSnippet`
- `panel.SetDialogVariable`, `panel.SetDialogVariableInt`, `panel.SetDialogVariableTime`
- `panel.SetAttributeString`, `panel.SetAttributeInt`, `panel.SetAttributeFloat`
- `panel.GetAttributeString`, `panel.GetAttributeInt`, `panel.GetAttributeFloat`
- `panel.SetFocus`, `panel.SetAcceptsFocus`

## UI Panel Types (common)

- `Label`, `Image`, `Button`, `TextEntry`, `DropDown`, `Slider`
- `DOTAScenePanel`
- `DOTAAbilityImage`, `DOTAAbilityButton`
- `DOTAItemImage`, `DOTAItemSlot`
- `DOTAHeroImage`, `DOTAHeroMovie`
- `DOTAAvatarImage`, `DOTAUserName`

## Common Patterns

### Panel + events

```js
const panel = $.GetContextPanel();
panel.SetHasClass("Hidden", false);

GameEvents.Subscribe("my_event", (data) => {
  $.Msg("event", data);
});
```

### Custom game event to server

```js
GameEvents.SendCustomGameEventToServer("my_event", {
  PlayerID: Players.GetLocalPlayer(),
});
```

### Net table subscription

```js
CustomNetTables.SubscribeNetTableListener("my_table", (tableName, key, data) => {
  $.Msg(tableName, key, data);
});
```

### Localization

```js
const text = $.Localize("#my_token");
```

## Notes

- Always guard UI-only logic; server logic belongs in Lua.
- Use `$.Schedule` for timed UI changes; cancel when panels are destroyed.
- Use `GameEvents` for actions and `CustomNetTables` for state.
