# Panorama Framework Reference

Use this reference when implementing or modifying Dota 2 Panorama UI.

## File Types and Paths

- Layout: `.xml` (VXML) compiled to `.vxml_c`
- Styles: `.css` (VCSS) compiled to `.vcss_c`
- Scripts: `.js` (VJS) compiled to `.vjs_c`

Resource path rules:
- `file://{resources}/...` for local project files.
- `s2r://panorama/...` for compiled or Valve-provided resources.

## Layout Basics (VXML)

Typical structure:

```xml
<root>
  <styles>
    <include src="s2r://panorama/styles/dotastyles.vcss_c" />
    <include src="file://{resources}/styles/custom_game/my_panel.css" />
  </styles>
  <scripts>
    <include src="file://{resources}/scripts/custom_game/my_panel.js" />
  </scripts>
  <Panel id="MyPanel" class="MyPanelRoot">
    <Label id="Title" text="#my_title" />
    <Button id="ConfirmBtn" onactivate="OnConfirm()">
      <Label text="#confirm" />
    </Button>
  </Panel>
</root>
```

Notes:
- Use `id` for script access, `class` for styling.
- Prefer small, reusable panels over monolithic trees.
- Use `onactivate`, `onmouseover`, `onmouseout` for interaction hooks.

## Style Basics (VCSS)

Common properties:
- Layout: `flow-children`, `horizontal-align`, `vertical-align`, `margin`, `padding`
- Visual: `background-color`, `background-image`, `wash-color`, `opacity`
- Text: `font-size`, `font-family`, `color`, `text-shadow`
- Animation: `transition-property`, `transition-duration`, `animation-name`

Example:

```css
.MyPanelRoot {
  width: 400px;
  height: 200px;
  flow-children: down;
  background-color: gradient(linear, 0% 0%, 0% 100%, from(#101820), to(#0a0d14));
  border: 1px solid #8b6f3d;
}

.MyPanelRoot.Hidden {
  opacity: 0;
}
```

## Script Basics (VJS)

Core APIs:
- `$.GetContextPanel()` to access the current panel.
- `$.Schedule(delay, callback)` for timers.
- `GameEvents.Subscribe(event, handler)` to receive server events.
- `GameEvents.SendCustomGameEventToServer(name, data)` to send to server.
- `CustomNetTables.SubscribeNetTableListener(table, handler)` for synced state.

Example:

```js
"use strict";

function OnConfirm() {
  GameEvents.SendCustomGameEventToServer("my_confirm", {
    PlayerID: Players.GetLocalPlayer(),
  });
}

(function () {
  const panel = $.GetContextPanel();
  panel.SetHasClass("Hidden", false);
})();
```

## Data Flow Patterns

UI -> Server:
- Use `GameEvents.SendCustomGameEventToServer` for actions.

Server -> UI:
- Use `GameEvents` for push notifications.
- Use `CustomNetTables` for persistent, queryable state.

## Manifest Wiring

Register UI elements in the custom UI manifest:

```xml
<CustomUIElement type="Hud" layoutfile="file://{resources}/layout/custom_game/my_panel.xml" />
```

Choose the correct `type` for where it should appear:
- `Hud`, `HeroSelection`, `GameSetup`, `EndScreen`

## Localization

Always use localization tokens in layout:
- `text="#my_token"`

Add tokens to your localization files in `resource/`.

## Common Pitfalls

- Forgetting to include the script/style in the layout.
- Using unsupported CSS features or web-only APIs.
- Mixing heavy logic into layout instead of scripts.
- Failing to register the layout in the manifest.
