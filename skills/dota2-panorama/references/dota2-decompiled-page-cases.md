# Decompiled Dota 2 page cases

Use this catalog when public uncompiled source does not cover the target page type. All entries are D evidence reconstructed from vanilla VPK resources and must be visually cross-checked in the running client before claiming pixel fidelity.

## Contents

1. Evidence batch
2. Selection index
3. D1 Owned item details
4. D2 Item-details navigation popup
5. D3 Armory introduction popup
6. D4 Compendium level popup
7. D5 Item picker
8. D6 Treasure odds details
9. D7 Battle report
10. D8 Collection browse sort dropdown
11. D9 Generic text-entry popup
12. F1 Dota item rarity foundation

## Evidence batch

- Extraction date: 2026-07-28
- Tool: Source 2 Viewer CLI 18.0.0.0
- Manifest: `<analysis-root>/dota2_panorama_reference/2026-07-28_cloak_related/evidence-manifest.md`
- Provenance: `pak01_dir.vpk`; shared popup style also comes from the Core VPK
- Scope: selected layouts and direct visual dependencies only; no bulk Panorama extraction
- 2026-07-29 addition: Core VPK generic text-entry popup and shared popup styles, plus current Dota `dotastyles` dropdown rules

## Selection index

| Case | Shell | Primary task | Density | Dynamic behavior | Best use |
| --- | --- | --- | --- | --- | --- |
| D1 Owned item details | dashboard subpage / large detail panel | inspect and edit one owned object | high | conditional sections, scroll body, fixed footer | equipment, cosmetic, upgradeable object details |
| D2 Item-details popup | large 16:9 nested popup | navigate a stack of item pages | medium-high | history/back stack, page transition | drill-down detail flows |
| D3 Armory introduction | illustrated promotional popup | explain and enter a feature | low | simple close/CTA | first-use onboarding only |
| D4 Compendium level | centered progression popup | announce and explain a level | low-medium | progress state, number animation | level-up result or compact progression |
| D5 Item picker | centered selection popup | choose one item | medium-high | wrapped choices, vertical scroll | plan/item/variant selection |
| D6 Treasure odds details | centered data popup | inspect probability by count/state | high | generated rows, current-row highlight, optional column | rarity chances and probability tables |
| D7 Battle report | full-screen report | browse multi-page statistics | very high | intro sequence, tabs, screen transitions | complex reports and multi-tab progression |
| D8 Collection sort dropdown | compact popup selector | choose one named option | low | open/current/hover | sort, filter, or named-option selector |
| D9 Generic text entry | centered secondary modal | edit short or multiline text | low | focus/submit/cancel | rename/edit-description popup |

## D1. Owned item details

**Use for:** a large single-object page where identity, rarity, mutable properties, repeated configuration rows, and a footer action coexist.

**Resources**

- `panorama/layout/dashboard_page_owned_item_details.vxml_c`
- `panorama/layout/dashboard_page_owned_item_details_primarycontrols.vxml_c`
- `panorama/layout/dashboard_page_owned_item_details_style.vxml_c`
- matching styles plus `tooltip_econ_item.vcss_c`

**Semantic hierarchy**

`SubpageRoot -> Body.Root -> ItemEditBackground -> ItemEditContainer`

1. `EconTooltipHeader`
   - `EconItemTitleBar`: item icon, original/editable name, set, close
   - `RarityStripe`
   - `Banner`: seasonal/hero imagery, rarity, quality, source, creation date, slot
2. `ItemEditBody`
   - preview
   - bundle, equip, tool, socket, gift, styles, properties, description sections
3. `ItemEditFooter`
   - centered action row

**Geometry and ownership**

- `ItemEditBackground` owns the full panel surface: `#2D2E30 -> #202529`, black border, dark outer shadow.
- The title bar is 160 px high. The rarity stripe is 10 px, reduced to 6 px in popup mode.
- The banner is normally 100 px and grows to 120 px for unusual items.
- The body owns vertical scrolling and 16 px internal padding.
- The footer is a fixed 64 px surface with top divider and upward shadow. Body scrolling never moves the footer.
- Repeated sections own their own header, rows, footer, and state controls.

**Surface hierarchy**

- Title bar: cool charcoal horizontal gradient around `#2b2e2f`.
- Banner: deeper `#191a1c` gradient with a black lower edge.
- Section: `#00000058`, one-pixel dark border, 12 px padding.
- Row: `#0000008d`, minimum 54 px, 2 px vertical separation.
- Footer: `#1d2023`, subtle white top edge, stronger shadow than internal rows.
- Rarity is a dedicated stripe and semantic text color; it is not used as the page background.

**Information implementation**

- Keep the object image, item name, set/source, rarity, quality, and slot as separate semantic nodes.
- Put mutable name controls inside an `EditableTitle` sub-surface. Collapse edit/reset/info affordances under `CannotModify`.
- Put hero/season identity in a dedicated `BannerIcons` group; do not merge it into the item image.
- Use `ItemRarityBackgroundColor` for the stripe/surface and `ItemRarityColor` for text.

**State model**

- Root classes control complete feature sections: `IsBundle`, `CannotEquip`, `HasTool`, `IsSocketable`, `HasRareSockets`, `MultipleStyles`, `AutoStyle`, `HasUneditableDescription`, and modification permissions.
- Style rows independently represent active, unlocked, available, auto, and unavailable states.
- Lock/check icons and button visibility change by class; row geometry stays stable.

**Controls**

- Primary actions use shared `ButtonPrimary` variants; internal utility actions may use `ButtonBevel`.
- Disabled controls desaturate and dim instead of changing layout.
- The primary-controls overlay keeps rarity, quality, style pagination, model/team selectors, and item name in a bottom-right information group.

**Do not use for:** a short confirmation, a probability-only popup, or a promotional first-use message.

## D2. Item-details navigation popup

**Use for:** a large nested detail flow that needs close, optional back navigation, and a page stack.

**Resources**

- `panorama/layout/popups/popup_item_details.vxml_c`
- `panorama/styles/popups/popup_item_details.vcss_c`

**Hierarchy**

`PopupItemDetails -> PageContainer + hidden PageStack + overlaid PopupHeader -> NavigationControls + CloseButton`.

**Implementation**

- The page viewport is 1560 px wide at 16:9 (`height: width-percentage(56.25%)`) with a 24 px outer margin and one-pixel `#5e6869` border.
- Header controls ignore parent flow and overlay the content rather than consuming a header row.
- Close is top-right. Back remains collapsed until `.HasHistory`.
- A hidden popup starts at 0.85 pre-scale and opacity 0, then enters over 0.15–0.2 s.
- Individual pages are stacked and opacity-swapped. Opening a nested page briefly scales/lowers brightness on the popup while the new page fades in.

**Do not use for:** a self-contained secondary popup with no navigation history.

## D3. Armory introduction popup

**Important classification:** despite the resource name `popup_armory_upgrade_opt`, this is a first-time armory/collection introduction, not a numerical upgrade screen.

**Resources**

- `panorama/layout/popups/popup_armory_upgrade_opt.vxml_c`
- `panorama/styles/popups/popup_armory_upgrade_opt.vcss_c`

**Hierarchy**

`Popup -> background art + right screenshot/shadow + right hero art + left PopupContents + scene rays + overlaid close`.

**Implementation**

- Fixed 1160 px width with height equal to 55% of width.
- No parent flow: promotional art and text are independently layered.
- Left copy column is 420 px wide with 80 px left margin and vertical centering.
- Screenshot group is 640 px wide, right-aligned, and translated down/right. Hero art is 400 px and independently translated.
- Close is a 16 px-inset dark primary button.
- Visual depth comes from authored background/hero/screenshot art; it is not a reusable data-page shell.

**Do not use for:** progression rows, probability tables, or any data-heavy object editor.

## D4. Compendium level popup

**Use for:** compact level-up feedback, one level/progress summary, and an emphasized continue action.

**Resources**

- `panorama/layout/popups/popup_compendium_level.vxml_c`
- `panorama/styles/popups/popup_compendium_level.vcss_c`

**Hierarchy**

`PopupCompendiumLevel -> BackgroundImage + MainBox -> header + body + BlackBanner -> LeftSide level + separator + RightSide progress -> ContinueButton + edge decor`.

**Implementation**

- Main content is 660×450 and vertically stacked.
- Header uses uppercase title-font typography, 28 px size, 2 px tracking, and a gold gradient.
- Supporting copy is centered green, 20 px.
- A 200 px black translucent banner owns a 400 px level region, a fading one-pixel separator, and a fill-width progress region.
- The level label is 35 px; the number is 50 px with strong shadow and a fixed/shrink-safe box.
- Progress is a compact 200×16 bar with a two-pixel black border.
- `.LevelingUp` expands the left side to 700 px while fading the separator and right side, preserving one animation owner per region.
- Number emphasis uses short scale/opacity slams of 0.15–0.25 s.

**Do not use for:** browsing multiple levels, displaying probability tables, or editing repeated properties. Use it only as a secondary reference for level emphasis and progress.

## D5. Item picker

**Use for:** selecting one item/plan/variant from a moderate list while retaining an inspect action.

**Resources**

- `panorama/layout/popups/popup_item_picker.vxml_c`
- `panorama/styles/popups/popup_item_picker.vcss_c`
- shared `popups_shared.vcss_c`

**Hierarchy**

`PopupItemPicker -> title + optional header item + description + Choices + cancel row`.

Each generated `DOTAItemPickerChoice` owns item media, a vertical detail group, label content, inspect action, and select action.

**Implementation**

- Popup shared shell supplies charcoal vertical gradient, border, shadow, centered placement, and scale/translate hidden state.
- Header item is 100 px high at a 3:2 aspect.
- Choices use a 771 px, right-wrapped, vertically scrollable black region with an eight-pixel framing edge.
- Each choice is 370 px wide, producing two columns, with a one-pixel low-alpha light border and 8 px gaps.
- Item names are 20 px, white, shrink-safe, and capped at 26 px height.
- Inspect is visible only for `.IsInspectable`; its empty spacer collapses at the same time so the action row keeps stable distribution.
- Select is compact, uppercase, and 18 px.

**Do not use for:** a persistent object detail page or a five-row modifier list.

## D6. Treasure odds details

**Use for:** probability tables, chance-by-level/count inspection, current-tier highlighting, and optional diagnostic columns.

**Resources**

- `panorama/layout/popups/popup_ui_treasure_odds_details.vxml_c`
- `panorama/styles/popups/popup_ui_treasure_odds_details.vcss_c`

**Hierarchy**

`DOTAPopupUITreasureOddsDetails -> Title/Close -> TitleBar columns -> scroll Body -> generated TreasureOddsDetailsEntry rows`.

**Implementation**

- Default width is 700 px; `.ShowMetadata` expands it to 1000 px without changing row semantics.
- Shell uses a left-to-right charcoal-to-black gradient, no border, a 20 px black fill shadow, and no internal padding.
- Title background is 100 px high and translucent black. Title is centered, uppercase, 30 px, with 1 px tracking.
- Column header is 32 px high, black, uppercase, thin, and 2 px tracked.
- Body owns vertical scrolling and caps at 600 px.
- Rows are exactly 38 px, alternate between two dark horizontal gradients, and share column-width classes with the header.
- The current row receives an amber wash and reveals a 16 px information icon. Hover raises label brightness without moving the row.
- Two-column mode uses 50/50 widths. Metadata mode uses three 33% columns.

**Do not use for:** a visual item hero section or a level-up celebration. It is a strong primary prototype for compact probability tables.

## D7. Battle report

**Use for:** a full-screen, multi-tab report with cinematic entry, stable header/footer, and horizontally transitioned screens.

**Resources**

- `panorama/layout/battle_report/popup_battle_report.vxml_c`
- `panorama/styles/battle_report/popup_battle_report.vcss_c`
- `panorama/styles/battle_report/battle_report_shared.vcss_c`

**Hierarchy**

`PopupBattleReport -> AsyncDataPanel -> IntroContainer + MainContainer -> Header + ScreenNav + Screens + Footer`.

**Implementation**

- The popup itself fills the viewport and removes the standard popup surface.
- Intro logo/title/date are separate reveal owners.
- Main report is 1440×900, centered, dark, and enters from 0.92 scale with a 0.7 s eased transition.
- Header separates report identity on the left from account identity/close on the right.
- Tab navigation shares a one-pixel baseline; selection adds a Dota Plus gold lower border.
- Screens remain in one fixed viewport. Before/after states offset 100 px left/right; active removes offset and restores opacity.
- Footer is fixed, shadowed upward, and owns previous/next/done actions. Done replaces next through a root state class.
- Shared report layouts use 64 px container margins and explicit filter/content columns.

**Do not use for:** a compact modal, simple object detail, or shallow single-state data screen.

## D8. Collection browse sort dropdown

**Use for:** compact sort, filter, or named-option selectors that should match the Dota 2 Armory/Collection dropdown shown beside `#DOTA_Collection_SortByLabel`.

**Resources**

- `dota/pak01_dir.vpk: panorama/layout/dashboard_page_collection.vxml_c`
- `dota/pak01_dir.vpk: panorama/styles/dashboard_page_collection.vcss_c`
- `dota/pak01_dir.vpk: panorama/styles/dotastyles.vcss_c`

**Hierarchy**

`#BrowseSortByDropDownContainer.DropDownContainer -> label #DOTA_Collection_SortByLabel + #BrowseSortByDropDown.SortByDropDown`.

**Implementation**

- The page-specific stylesheet only sets `.SortByDropDown` to 200 px wide. The visual contract comes from the shared `DropDown` and `DropDownMenu` rules in `dotastyles`.
- Closed control: vertical gradient from `#292e2e` to `#191e1e`, `2px solid #5e686966`, and `#00000055 0 0 1px 3px` shadow.
- Hover control: vertical gradient from `#393e3e` to `#292e2e`.
- Arrow: `s2r://panorama/images/control_icons/arrow_dropdown_png.vtex`, rendered at 32×32 without a divider.
- Menu: `#3d4448` background and `#00000066 0 0 6px` fill shadow. Hover/current row uses `#585e62`; normal text is `#ffffff99`.
- Every menu label has one-pixel `#00000066` top and bottom borders. These dark separators are part of the control and must not be dropped by a custom option renderer.
- When adapting this control, keep the popup menu exactly the same width as the closed button. If the target requires full-control text centering, overlay the arrow at the right so it does not shift the text center.

**Do not use for:** action buttons, rarity selectors whose surface itself must communicate rarity, or selectors that need a green confirmation state.

## D9. Generic text-entry popup

**Use for:** renaming an object, entering a short label, or adapting the Dota item-description text-entry popup.

**Resources**

- `core/pak01_dir.vpk: panorama/layout/popups/popup_generic_text_entry.vxml_c`
- `core/pak01_dir.vpk: panorama/styles/popups/popup_generic_text_entry.vcss_c`
- `core/pak01_dir.vpk: panorama/styles/popups/popups_shared.vcss_c`

Evidence is D-level decompiled reference from the exact Core VPK resources above. Runtime fidelity still requires a current capture.

**Hierarchy**

`PopupPanel -> PopupTitle -> MessagePanel(ImageContainer + MessageLabel) -> TextEntry -> PopupButtonRow`.

**Implementation**

- Shared `PopupPanel` owns the charcoal vertical gradient, one-pixel `#5e6869` border, 64 px horizontal and 32 px vertical padding, black 8 px shadow, centered placement, and vertical flow.
- `PopupTitle` is centered, 30 px, thin, `#afb4b4`, with 15 px lower spacing.
- `MessagePanel` centers a horizontal image-plus-copy group. With no image, keep the message label centered; do not retain an empty image slot.
- `MessageLabel` is centered vertically, white, 24 px, and capped at 400 px.
- `TextEntry` is full-width, centered, has 24 px top spacing and 32 px horizontal padding. The multiline state is 128 px high with normal whitespace.
- `PopupButtonRow` is centered, horizontal, with 25 px top and 20 px bottom spacing. Use the project-loaded Dota shared button class instead of repainting every button property.
- Hidden state changes opacity, pre-scale, vertical translation, shadow, and sound on the popup owner.

**Adaptation rule**

For a text-entry adaptation, change only the specified content and interaction, collapse unused media slots, select single- or multiline entry deliberately, and bind submit/cancel. Preserve the source hierarchy and shared surface/spacing contract. Do not copy the source values and then add a second custom restyle that changes the same properties.

**Do not use for:** a destructive warning with specialized red treatment, a complex settings form, or a multi-step flow.

## F1. Dota item rarity foundation

Use the exact Dota item rarity token names and colors. Do not substitute mobile-game rarity labels.

| Runtime class/token | Simplified Chinese | Color |
| --- | --- | --- |
| `common` / `Rarity_Common` | 普通 | `#b0c3d9` |
| `uncommon` / `Rarity_Uncommon` | 罕见 | `#5e98d9` |
| `rare` / `Rarity_Rare` | 稀有 | `#4b69ff` |
| `mythical` / `Rarity_Mythical` | 神话 | `#8847ff` |
| `legendary` / `Rarity_Legendary` | 传说 | `#d32ce6` |
| `ancient` / `Rarity_Ancient` | 远古 | `#eb4b4b` |
| `immortal` / `Rarity_Immortal` | 不朽 | `#e4ae39` |
| `arcana` / `Rarity_Arcana` | 至宝 | `#ade55c` |
| `seasonal` / `Rarity_Seasonal` | 赛季 | `#fff34f` |

Implementation contract:

- Put `ItemRarity_<name>` on the semantic item/row owner.
- Use `ItemRarityBackgroundColor` only on stripes, badges, icons, or tightly scoped rarity surfaces.
- Use `ItemRarityColor` on rarity text.
- Keep primary page surfaces charcoal. Rarity color identifies content and must not flood the entire shell.
- Use one naming set consistently in data, CSS classes, localization, and probability configuration.
