# Panorama layout contracts

## Rounded surfaces

Give each rounded card one visual owner. That panel owns radius, clipping, background, border, and shadow when they form one shell. Put internal tint/highlight layers inside the clipped owner and avoid stacking same-radius opaque panels that create seams.

## Stable layer model

Use these layers when a composed view needs them:

1. `ContainerBase`: page slot and outer flow.
2. `Frame`: fixed four-sided inset.
3. `Root`: page content and major regions.
4. Local wrappers: icons, labels, masks, badges, and controls.

Geometry belongs to the nearest stable owner. Use margins only as final local spacing after parent/child structure is correct.

## Templates

### Horizontal

Use a fixed shell with `flow-children: right`, then explicit left/center/right slots. Each slot owns its internal layout.

### Vertical

Use an explicit-width/height container with `flow-children: down`. Use top/bottom spacer panels with `fill-parent-flow(1)` only for non-critical centering.

### Hybrid

Use a horizontal outer shell whose columns each own a vertical layout. Keep navigation and detail slots separate. Do not force one global flow rule across both axes.

For fixed four-sided inset, prefer `ContainerBase -> Frame -> Root`. For a strict replica, outer geometry is fixed and adaptive behavior is confined to named content slots.

## Image contract

- Use `s2r://(kv path without _c)` for KV image paths.
- Use item icons from `s2r://panorama/images/items/<name>_png.vtex`.
- Normalize `.vtex_c` to `.vtex` and `.vsvg_c` to `.vsvg`.
- For finite image sets, define stable VCSS classes and toggle classes from JS.
- For stretch-risk art, use a fixed wrapper plus background image with `contain`, centered position, and no repeat.
- Use dynamic `panel.style.backgroundImage` only for open-ended runtime paths.
- Do not use unsupported `preserve-aspect-fit`.

## Text contract

Separate box geometry from glyph layout:

- wrapper owns width/height, alignment, background, clipping, and visibility/state;
- label owns text, font, color, overflow, and text alignment.

For centered text, give the wrapper stable height and the label full width, `height: fit-children`, `vertical-align: center`, and `text-align: center`. Use small offsets only as an approved optical correction.

## Scroll contract

- The panel directly owning overflowing content owns `overflow: ... scroll`.
- Use one scroll owner per axis.
- A decorative/clipping outer wrapper must not become an accidental second scroll owner.
- Hidden scrollbars do not disable native scrolling.
- Treat `scrolloffset_x/y` as observations, not writable control APIs.
- For finite custom carousels, let an outer panel clip and an inner strip own explicit translation.

Diagnose native scroll by checking owner, overflow size, and parity with a working local source example before adding custom behavior.

## Syntax-sensitive structure

- Keep a `<root>` wrapper.
- Put style/script includes before the panel tree.
- The first actual panel under `<root>` has no `id`.
- Verify included source files and resource paths exist.
- Copy the nearest same-category working source template when creating a fragile layout.
