# SERVIR brand assets — one step outstanding

The site is styled on the SERVIR design system, read live from Figma
(`SERVIR Design System`, file `Fq6ffqege1xqUeCDyLYTfK`, modified 2026-08-27) via the
platform's `ui_design` tool. Colour, type and the usage rules are already applied.

**The logo is in place.** `assets/servir-logo.png` — the white/mono lockup
(SERVIR + Global Collaborative, 393x54, transparent PNG), taken from
`SERVIR-AI/global-platform` at `apps/web/src/assets/servir.png`. That is the platform's own
shipped asset, so the site and the platform UI carry the identical mark.

It is **white on transparency** and therefore belongs on dark grounds only. The header band
(`--servir-bar`, `#1c212a`) is dark in both themes, so it reads correctly in each. For any
light-ground use, composite it onto the navy first — `brand/doc-masthead.png` in the build
directory is exactly that, and is what the Google Doc export uses.

Other treatments (Primary, Black, Grayscale, Reversed Color, Reversed Mono; Horizontal and
Stacked) are available from the design file via
`ui_component(name="SERVIR/Logo/Lockup", treatment=..., layout=...)`. Those render URLs
expire in ~30 days, so download rather than hotlink.

## Rules applied here, so they survive future edits

- **Brand blue `#2380B0` leads; brand green `#91AF3D` is the supporting accent.**
- **The identity navy is for headers and hero surfaces, not body backgrounds.** It has its
  own token, `--servir-bar`, which stays dark in *both* light and dark themes. It must not
  be bound to `--space`, which flips to a light accent in dark mode — that was a real bug
  here, caught at 1.23:1 contrast.
- **Brand green is NOT a verdict colour.** The status scale (built / partner / build / gap)
  is deliberately held off the brand hues so no accent can read as a verdict. Status uses
  `#1F6B52`, `#485E88`, `#8F5E06`, `#9B2C2C` — none of them brand blue or brand green.
- Every page carries the platform header: the SERVIR mark plus the domain name.

## One deliberate deviation

The shipped `platform_header` recipe carries the sub-line "SERVIR Global Risk Platform".
This document spans Global Risk, Food Security **and** Natural Resource Management, so
stamping one platform's name on it would be inaccurate. The mark and the domain slot follow
the recipe; only the sub-line states this document's real scope.

## Type

Display is **Roboto Condensed** (the design file's face, at 300/400/500/600/700).
Body is **Inter** — the design file uses Roboto Condensed down to 13–14px, but this is a
long document and a condensed face is hard work at reading sizes, so Inter carries running
text. Mono stays IBM Plex Mono; the brand file specifies no monospace face.
Both load from Google Fonts, the one font host the page is allowed to reach.
