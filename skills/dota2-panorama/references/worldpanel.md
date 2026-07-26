# WorldPanel alignment

## Anchor contract

Define one alignment owner, fixed width/height per variant, horizontal/vertical alignment policy, and placement offsets. Keep placement offsets separate from panel geometry.

Any panel participating in anchor math uses explicit width and height. The final aligned container must not use `fit-children`; flow is allowed only in non-anchor subtrees.

Use one size resolver in positioning: `fixed > actual > desired`. Prefer actual size unless the task explicitly requires desired size; fixed size wins whenever configured.

## Server/client parity

Lock the same fixed size and alignment policy on server and client. For precise placement, follow a verified fixed-size local source pattern with:

- fixed root and inner frame;
- server-provided fixed width/height;
- top-left anchor root at position zero;
- text and flow isolated below the anchor owner.

## Text isolation

Place labels inside fixed wrappers. Text desired size, stroke, language length, or digit count must not change anchor width/height.

## Variants and validation

Boss/elite variants share one alignment path and differ only through fixed constants. When validation is authorized, verify center-x drift is within one pixel and test value length, language, and resolution changes. A deliberate vertical offset may remain non-zero.
