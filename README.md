# Platform-Inventory

Canonical, version-controlled home for the SERVIR Platform Ecosystem engineering plan — so the plan,
its decisions, and their rationale are readable by people and by other LLM sessions without depending
on a specific claude.ai conversation.

**Live site:** https://servir-ai.github.io/Platform-Inventory/

## Contents

- [`index.html`](index.html) — the full engineering plan (architecture, gateway, GeoAI strategy,
  Global Risk / Food Security / Natural Resource Management platforms, shared infrastructure,
  decisions log, services, NASA asset mapping, appendix). Pulled from the claude.ai artifact
  `Platform Ecosystem Engineering Plan` (`b9ee9e79-474b-4e3f-962e-8ac3c3b0072e`) on 2026-09-03.
- [`servir-platform-inventory-repo.md`](servir-platform-inventory-repo.md) — decision/context record:
  why this repo is the canonical source, what was and wasn't carried over, and constraints future
  sessions (Claude or otherwise) should know about before changing how this is maintained.
- [`RED_TEAM_REVIEW.md`](RED_TEAM_REVIEW.md) — adversarial review of the engineering plan: architectural
  risk, feasibility gaps, governance/equity issues, internal inconsistencies, and a prioritized list of
  the top 5 fixes needed before the plan should be treated as fundable/buildable.
- [`OPEN_DATA_SOURCES.md`](OPEN_DATA_SOURCES.md) — verified reference of open datasets and microservices
  the Gateway could integrate with: world population, building/settlement footprints, crop data, field
  boundaries, and adjacent open EO/hazard APIs — each with access method, license, and integration notes.

## Status

`index.html` is deployed as a live static site via GitHub Pages (source: `main` branch root). The repo
is **public** — it was made public specifically to enable Pages on the org's free GitHub plan, so the
plan's content (including internal names and Google Drive doc IDs) is publicly visible. It's still a
single-page document, not yet split into per-section pages. See the editorial note at the end of
`servir-platform-inventory-repo.md` for what else is outstanding.
