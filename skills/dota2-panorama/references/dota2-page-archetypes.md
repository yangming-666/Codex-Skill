# Dota 2 page archetypes

Use this reference for every new visual design, redesign, or image/Figma implementation. For targeted screenshot corrections, retain the already accepted prototype and regions unless the user explicitly reopens them. This prevents both a generic “Dota-like” treatment and an unnecessary redesign from replacing page-specific evidence.

## Contents

1. Evidence and source rules
2. Mandatory prototype selection
3. Prototype mapping table
4. Source-backed page catalog
5. VPK discovery
6. VPK candidate registry
7. Adding a catalog entry

## Evidence and source rules

Resolve the Dota content root through the current project's approved path resolver. All paths below are relative to `<dota-content-root>`.

Evidence levels:

- **A — source-backed:** uncompiled Valve XML/CSS/JS exists. Exact implementation claims may cite selectors and properties.
- **D — decompiled-reference-backed:** selected vanilla `.vxml_c/.vcss_c/.vjs_c` artifacts were decompiled during an explicit global reference-catalog task. Cite the original VPK resource path, label the evidence as decompiled, and verify visual conclusions in the running client.
- **B — runtime-backed:** a current runtime capture and exact page/resource identity exist, but uncompiled source does not. Replicate visible geometry and behavior only.
- **C — inferred:** only a reference image or resemblance exists. Use it as an adaptation and never describe inferred internals as Valve implementation.

During addon implementation, compiled artifacts are identity-only and must not be opened. During an explicit global reference-catalog task, selected vanilla compiled Panorama artifacts may be decompiled outside addon source and used as D evidence.

For a strict original-page replica, require A evidence or D evidence plus sufficient runtime captures of all relevant states. If neither exists, stop the strict-replica claim and report what evidence is missing.

## Mandatory prototype selection

Before editing XML/CSS for a visual task:

1. Classify the target shell: full-screen page, centered modal, anchored drawer, persistent HUD, transient notification, or loading/information page.
2. Classify the task: browse, inspect/detail, select, compare/status, progress/upgrade, transact/confirm, teach, or notify.
3. Record hierarchy: global title, summary/hero object, primary controls, repeated content, detail/help, footer action, and secondary modal.
4. Record density and dynamic behavior: fixed or variable rows, scroll ownership, long text, locked/disabled/selected states, and aspect-ratio variants.
5. Score catalog candidates on function, shell, hierarchy, interaction, and density. Function and hierarchy outweigh color resemblance.
6. Select exactly one primary prototype. Select no more than two secondary references, each limited to a named component or state.
7. Build the mapping table below. Visual implementation starts only after the table has no unmapped critical region.

Do not combine the page shell from one prototype, the hierarchy from another, and ornamental colors from several unrelated pages. That produces a collage, not a targeted replica.

## Prototype mapping table

Use this working artifact in task notes or the implementation plan:

| Target region | Role and state | Dota prototype region | Evidence path / selector | Retain exactly | Adapt deliberately |
| --- | --- | --- | --- | --- | --- |
| Page shell | Modal, blocks background | `EndScreenWindow` | `.../multiteam_end_screen.xml`, `.EndScreenWindow` | layer order, reveal model | target dimensions |
| Repeated rows | variable count, locked state | `TeamsContainer` rows | source path and selector | row hierarchy, state owner | target data fields |

Every critical region needs a concrete source/evidence entry. “Use Dota style” is not valid evidence.

## Source-backed page catalog

This catalog covers public, uncompiled Valve Panorama sources available with Dota 2. It is a maintained reference set, not a claim that all core client pages have public source.

### A1. Team and lobby selection

**Use for:** two-column setup pages, team/slot assignment, pre-game configuration, pages with a persistent primary action and lock/cancel state.

**Sources**

- `dota/panorama/layout/custom_game/team_select.xml`
- `dota/panorama/styles/custom_game/team_select.css`
- `dota/panorama/scripts/custom_game/team_select.js`

**Hierarchy**

`TeamSelect -> TeamSelectContainer -> TeamsSelectEmptySpace + TeamsList + GameAndPlayersRoot`. The left panel owns header/list/shuffle. The right panel owns game summary/timer, unassigned players, and mutually exclusive lock/start or cancel/unlock actions.

**Implementation**

- Outer layout uses `flow-children: right`; two functional columns are independent owners rather than one mixed flow.
- `TeamsList` is a fixed 400 px full-height column; `GameAndPlayersRoot` is another 400 px full-height vertical column.
- Major surfaces use near-black vertical gradients and black shadows. Repeated list surfaces use `#272b30 -> #181a1e`, inset black shadow, and low-alpha `#49525555` separators.
- Primary action uses a restrained blue vertical gradient (`#2d4881cc -> #486ca9cc`) with brighter blue hover. Cancel/unlock uses a dark red gradient (`#2c1b1b -> #482e2f`) with a stronger red hover.
- Headers and actions are uppercase. Lock, shuffle, timer ring, and directional icons communicate state without adding decorative chrome.
- State changes are class/visibility driven; the stable columns do not move when the available action changes.

**Do not use for:** centered single-object detail modals or transient notifications.

### A2. Flyout scoreboard / anchored detail drawer

**Use for:** edge-anchored drawers, compact comparison tables, inspect-on-demand team/player statistics.

**Sources**

- `dota/panorama/layout/custom_game/multiteam_flyout_scoreboard.xml`
- `dota/panorama/styles/custom_game/multiteam_flyout_scoreboard.css`
- `dota/panorama/styles/custom_game/shared_scoreboard_styles.css`

**Hierarchy**

`FlyoutScoreboardRoot -> Legend + TeamsContainer`. The legend and generated team rows share named column classes so headers and data stay aligned.

**Implementation**

- Root is top-left anchored, vertically flowing, initially translated `-600px`; a state class moves it into view. The transition owner is the root, not every row.
- Columns use explicit widths (`ScoreCol_*`) shared between legend and rows.
- Team sections own their player rows. Portrait, player details, score, K/D/A, and audio state remain separate cells.
- Team identity is expressed by a narrow team-color field and gradient/shadow treatments; the table stays dark and low-noise.
- The trailing fade uses a horizontal transparent-to-black gradient to blend an edge drawer into the game view.

**Do not use for:** a full-screen results ceremony or a centered upgrade modal.

### A3. Post-game result and ranking screen

**Use for:** results, rankings, reward summaries, full-screen comparison tables with a terminal close/continue action.

**Sources**

- `dota/panorama/layout/custom_game/multiteam_end_screen.xml`
- `dota/panorama/styles/custom_game/multiteam_end_screen.css`

**Hierarchy**

`EndScreenRoot -> EndScreenWindow -> VictoryRow + Legend + TeamsContainer + CloseButton`.

**Implementation**

- Full-screen root owns a black top-heavy fade, separating results from the world without an opaque card covering the entire viewport.
- `EndScreenWindow` is a single vertical information owner. Victory identity precedes table legend and rows; the close action follows the complete result.
- Entry state combines opacity, scale, and upward translation on the window. Rows have their own delayed opacity/translation reveal.
- Legend and row cells share explicit column classes, including team, hero, player, score, K/D/A, items, and net worth.
- Close is a compact dark slab with a 3 px neutral border; hover changes border emphasis rather than introducing unrelated ornament.

**Do not use for:** editable forms or a small secondary help popup.

### A4. Hero-selection status overlay

**Use for:** compact phase/status strips, party or lineup previews, countdown plus repeated portraits.

**Sources**

- `dota/panorama/layout/custom_game/multiteam_hero_select_overlay.xml`
- `dota/panorama/styles/custom_game/multiteam_hero_select_overlay.css`

**Hierarchy**

`HeroSelectOverlayRoot -> PhaseInstructions + HeroSelectTeamRowsContainer -> two team containers -> team headers/player portraits`.

**Implementation**

- The overlay is a fixed 210 px-high band; content occupies 80% width and centers horizontally.
- Team rows flow horizontally; each player root flows vertically into portrait and name.
- Timer/ring is a fixed 70 px element; phase labels swap through `.Visible` rather than reflowing the band.
- Player portraits are explicit 90×50 cells with a one-pixel black edge. Team gradients and logos sit in a separate header layer.
- A local-player team receives a light inset/glow overlay. Highlight state desaturates the portrait.
- Aspect-ratio adjustment is explicit through `.AspectRatio4x3` selectors.

**Do not use for:** dense scrolling lists or object-detail pages.

### A5. Full-screen loading state

**Use for:** minimal loading interstitials where no information architecture is required.

**Sources**

- `dota/panorama/layout/custom_game/custom_loading_screen.xml`
- `dota/panorama/styles/custom_game/custom_loading_screen.css`

**Hierarchy**

One full-screen root with one centered loading image.

**Implementation**

- Root fills the viewport with `#212226`.
- The icon is centered and loops through opacity plus `pre-transform-scale2d`: fade in, hold, expand to 4× while fading, reset.
- No fake progress, extra panels, or decorative hierarchy is added.

**Do not use for:** game-information loading pages or any page requiring interactive controls.

### A6. Game information / illustrated instructions

**Use for:** rules, onboarding summaries, “how to play”, a small number of alternating text-and-image explanation rows.

**Sources**

- `dota_addons/overthrow/panorama/layout/custom_game/overthrow_game_info.xml`
- `dota_addons/overthrow/panorama/styles/custom_game/overthrow_game_info.css`

**Hierarchy**

`OverthrowGameInfo -> Title -> objective header/summary -> how-to header -> illustrated InfoRows -> tips`.

**Implementation**

- Page is a single vertical narrative. Each `InfoRow` is horizontal and alternates image/text order to create rhythm.
- Title is large (64 px), uppercase, and light gray; section headers are smaller (18 px), bold, uppercase, with strong vertical spacing.
- Body copy is subdued gray. Semantic terms use localized inline classes: important entities are light gray; items/gold/XP use amber `#fcaf3d`.
- Illustrations use explicit dimensions and deliberate overlap/negative spacing. This is an authored instruction layout, not a reusable data table.

**Do not use for:** variable-length databases, settings, or transaction dialogs.

### A7. Transient item/event notification

**Use for:** item pickup, timed alert, kill/bounty announcement, centered high-priority but short-lived feedback.

**Sources**

- `dota_addons/overthrow/panorama/layout/custom_game/overthrow_item_notification.xml`
- `dota_addons/overthrow/panorama/styles/custom_game/overthrow_item_notification.css`
- `dota_addons/overthrow/panorama/scripts/custom_game/overthrow_notification.js`

**Hierarchy**

`OverthrowNotification -> OverthrowItemNotification -> mutually exclusive AlertTimer / Overtime / AlertMessage / PickupMessage / KillMessage states`.

**Implementation**

- Root covers the viewport, is non-hit-testable, and centers a 640×360 notification stage.
- The stage uses a cool dark gradient (`#42494e -> #252525`). Individual message modes own their specific image/text hierarchy.
- Pickup imagery is grouped separately from copy. Hero, chest, and item images have explicit cells rather than sharing one background.
- Message states begin with opacity 0 and 2× scale, then transition to opacity 1 and scale 1. The animation belongs to the state panel.
- Large headline sizes (48 or 96 px) are reserved for the transient event; supporting lines remain 24 px.

**Do not use for:** a persistent detail modal. The large type and scale-in motion are intentionally brief.

### A8. Tutorial speech/dialog overlay

**Use for:** guided tutorial dialogue, NPC speech, sequential instruction with portrait and continue/close actions.

**Sources**

- `dota_addons/npx_2019/panorama/layout/custom_game/npx_hud_main.xml` (`DialogPanel` and `FloatingDialogPanel`)
- `dota_addons/npx_2019/panorama/styles/custom_game/npx_dialog.css`

**Hierarchy**

`DialogPanel -> background + scene portrait + title + content -> SpeechBubble -> bubble layers + sized/visible text -> button container`.

**Implementation**

- Main dialog is bottom-centered with minimum 500×180 geometry and a stable content/portrait relationship.
- Hidden state uses small pre-scale plus opacity 0. Visible state restores scale/translation and delays opacity slightly.
- Portrait is an independent 128×128 circular scene panel with black border and broad dark shadow.
- Name/title floats above content in a translucent dark label; speech copy belongs to layered bubble panels with a distinct callout.
- Continue and close are separate buttons inside one action container. Confirmation variants add player-state icons without rebuilding the dialog shell.

**Do not use for:** neutral system confirmations without a speaker or sequential teaching context.

## VPK discovery

Use the current project's path resolver to locate `pak01_dir.vpk`, then use `scripts/inventory-vpk-panorama.ps1` with a trusted VPK listing CLI.

The inventory has two meanings:

- raw `xml/css/js` entries are source candidates and may be extracted for inspection;
- `vxml_c/vcss_c/vjs_c` entries are identity-only during implementation, but may be narrowly extracted/decompiled for an explicit global reference-catalog task.

Before decompilation, do not infer hierarchy from compiled byte size, CRC, neighboring filenames, or companion resources. Those facts identify a page family, not its implementation.

For reference extraction:

1. Select the page family from the inventory.
2. Extract only its direct `.vxml_c`, `.vcss_c`, and `.vjs_c` resources into a dedicated research directory outside addon source.
3. Preserve a manifest containing VPK path, resource paths, extraction date, and tool/version.
4. Label all derived XML/CSS/JS as decompiled evidence.
5. Summarize semantic hierarchy and implementation rules into this catalog; do not paste full decompiled files into the skill.
6. Cross-check geometry, imagery, state changes, focus, hover, disabled behavior, and animation in the running client.

On the Dota install initially audited for this catalog, the VPK contained no raw Panorama `.xml`, `.css`, or `.js` entries. Re-run the inventory against the current install because packaging can change.

## VPK candidate registry

These page identities were confirmed from the VPK listing, but their core uncompiled source is not present in the public source set described above. Before extraction or capture they are **identity-only**. Promote them to D after narrow decompilation and to B after obtaining current runtime screenshots of required states.

Detailed D-evidence entries for the first extracted batch are in `dota2-decompiled-page-cases.md`.

| Candidate family | Suitable target | Confirmed VPK resource identities |
| --- | --- | --- |
| Inventory browse/filter | collection, armory, category/tag filters | `panorama/layout/dashboard_page_armory.vxml_c`; `panorama/layout/dashboard_page_collection.vxml_c`; `panorama/layout/popups/popup_armory_filter.vxml_c`; `panorama/layout/popups/popup_armory_tags.vxml_c` |
| Owned item detail | cosmetic/item inspection, ownership, styles, primary actions | `panorama/layout/dashboard_page_owned_item_details.vxml_c`; `_gem`, `_primarycontrols`, and `_style` companion layouts |
| Store and purchase | purchasable item detail and transaction confirmation | `panorama/layout/dashboard_page_store_item_details.vxml_c`; `panorama/layout/popups/popup_purchase_item.vxml_c`; `popup_purchase_item_from_prompt.vxml_c` |
| Item inspection | centered item or stack detail | `panorama/layout/popups/popup_item_details.vxml_c`; `popup_item_stack.vxml_c`; `popup_item_received.vxml_c` |
| Upgrade/progression | upgrade choice, level progress, reward presentation | `panorama/layout/popups/popup_armory_upgrade_opt.vxml_c`; `popup_compendium_level.vxml_c`; `popup_purchase_battle_pass_levels.vxml_c` |
| Quest/challenge | progression page, task detail, weekly objectives | `panorama/layout/dashboard_page_challenge_details.vxml_c`; `dashboard_page_weekly_quests.vxml_c` |
| Item selection | modal browse/select or in-game upgrade picker | `panorama/layout/popups/popup_item_picker.vxml_c`; `panorama/layout/hud/dota_hud_neutral_item_picker.vxml_c`; `dota_hud_aghanim_upgrade_picker.vxml_c`; `dota_hud_imbue_ability_picker.vxml_c` |
| Hero selection | modal hero/facet selection | `panorama/layout/popups/popup_hero_picker.vxml_c`; `popup_hero_facet_picker.vxml_c`; `panorama/layout/hero_selector.vxml_c` |
| Results and battle report | post-game overview, statistics, combat recap | `panorama/layout/dashboard_page_post_game.vxml_c` and its row/detail companions; `panorama/layout/battle_report/popup_battle_report.vxml_c`; `panorama/layout/dashboard_page_profile_battle_stats.vxml_c`; `panorama/layout/hud/dota_hud_fightrecap.vxml_c` |
| Treasure/reward reveal | treasure detail, reward contents, received-item flow | `panorama/layout/dashboard_page_treasure_details.vxml_c`; `panorama/layout/popups/popup_treasure_details.vxml_c`; `popup_item_received.vxml_c` |
| Settings | dense tabbed settings and control binding | `panorama/layout/popups/popup_settings.vxml_c`; `popup_settings_reborn.vxml_c` |
| HUD toast | short in-game item/reward notification | `panorama/layout/hud/dota_hud_found_neutral_item_toast.vxml_c`; `dota_hud_bounty_toast.vxml_c` |

Outside an explicit catalog task, do not open these `_c` resources. For catalog research, follow the narrow extraction workflow above. For strict visual comparison, capture the running client and record viewport, state, focus/hover/disabled variants, and crop boundaries.

## Adding a catalog entry

Add an entry only after inspecting the uncompiled source or obtaining runtime evidence. Record:

- functional role and shell;
- exact source paths or runtime page identity;
- semantic panel hierarchy;
- geometry/flow/scroll ownership;
- surface, border, typography, icon, and motion rules;
- state selectors and interaction behavior;
- dynamic-content and aspect-ratio behavior;
- appropriate and inappropriate target uses;
- evidence level and date/version when runtime-backed.

Do not add entries consisting only of color values, adjectives, or screenshots with no functional analysis.
