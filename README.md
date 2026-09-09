# Platform-Inventory

Canonical, version-controlled home for the SERVIR Platform Ecosystem engineering plan — so the plan,
its decisions, and their rationale are readable by people and by other LLM sessions without depending
on a specific claude.ai conversation.

**Live site:** https://servir-ai.github.io/Platform-Inventory/

## Contents

### The plan, as a site

| Page | Section |
|---|---|
| [`index.html`](index.html) | Overview and contents |
| [`01-architecture.html`](01-architecture.html) | How to build this — the shared build order |
| [`02-gateway.html`](02-gateway.html) | Gateway & integration architecture · 230-repo triage |
| [`03-geoai.html`](03-geoai.html) | GeoAI strategy alignment |
| [`04-global-risk.html`](04-global-risk.html) | Global Risk (RiskMap) — 12 perils × 3 clocks |
| [`05-food-security.html`](05-food-security.html) | Food Security (AgriNexus) |
| [`06-nrm.html`](06-nrm.html) | Natural Resource Management (LCEM) |
| [`07-shared-infra.html`](07-shared-infra.html) | Cross-platform shared infrastructure |
| [`08-decisions.html`](08-decisions.html) | 22 tracked decisions · phased roadmap |
| [`09-services.html`](09-services.html) | 123 hub services, with status and user institution |
| [`10-nasa.html`](10-nasa.html) | 34 NASA programme assets beyond SERVIR |
| [`11-appendix.html`](11-appendix.html) | Terminology and the source record |
| [`full-plan.html`](full-plan.html) | The entire plan on one page — for Ctrl-F and printing |

Shared styling lives in [`assets/style.css`](assets/style.css). `.nojekyll` stops GitHub Pages
running the files through Jekyll.

### Supporting records

- [`servir-platform-inventory-repo.md`](servir-platform-inventory-repo.md) — decision/context record:
  why this repo is the canonical source, what was and wasn't carried over, and constraints future
  sessions (Claude or otherwise) should know about before changing how this is maintained.
- [`RED_TEAM_REVIEW.md`](RED_TEAM_REVIEW.md) — adversarial review of the engineering plan: architectural
  risk, feasibility gaps, governance/equity issues, internal inconsistencies, and a prioritized list of
  the top 5 fixes needed before the plan should be treated as fundable/buildable.
- [`OPEN_DATA_SOURCES.md`](OPEN_DATA_SOURCES.md) — verified reference of open datasets and microservices
  the Gateway could integrate with: world population, building/settlement footprints, crop data, field
  boundaries, and adjacent open EO/hazard APIs — each with access method, license, and integration notes.

## Maintenance

Keeping this register current is a repo job, not a person's job. [`.github/workflows/inventory-sweep.yml`](.github/workflows/inventory-sweep.yml)
runs [`scripts/sweep.py`](scripts/sweep.py) on a schedule (Mondays 14:00 UTC) and on demand via
**Actions → Inventory sweep → Run workflow**.

The sweep refreshes the two mechanical parts of the register:

1. the SERVIR GitHub organisations' repository inventory, and
2. the SERVIR App Center service status badges.

It writes `data/servir-repos.json`, `data/appcenter.json` and `data/CHANGES.md`, and **opens a pull
request only when something actually changed** — a quiet week produces no PR. It runs on the built-in
`GITHUB_TOKEN`; no secret needs configuring.

Three deliberate safeguards, because a silent failure here is worse than no sweep at all:

- **Empty fetch.** If a fetch returns nothing for every org, the sweep **keeps the previous snapshot**
  rather than overwriting the baseline with an empty one — otherwise one blocked run would make the
  next run report every service as new.
- **Unparseable badges.** If App Center pages fetch fine but 80%+ carry no recognisable status badge,
  the sweep treats that as a markup change, keeps the previous snapshot and says so. Without this, a
  changed page template would give every service an empty status, the diff would go quiet, and the
  sweep would look healthy while reporting nothing at all.
- **Per-subsystem, not global.** A stale subsystem has its snapshot substituted back in, so its own
  diff is empty by construction. The PR gate is `changed = bool(changes)` and nothing more — an
  earlier version also gated on "did anything go stale", which meant *a blocked GitHub fetch would
  suppress a real App Center status change in the same run*. It no longer does.

Any run that fell back says so under **Attention** in `data/CHANGES.md`.

**Verified against the live site, 9 September 2026.** The crawler parses the *listing* page, not
detail pages: status is a CSS class on each card (`inactive`, or absent), which is the only status
this source publishes — a binary, not a graded badge. Detail pages carry no status at all and their
`<title>` is boilerplate identical for every app. An earlier version of this script walked 95 detail
pages looking for status words in the page text; it would have found none and reported silence
forever. The shipped pattern was checked against the live DOM: **79 of 79 cards parsed, all 5
inactive entries correct.** One request now, not 95.

Note for anyone re-testing from a Claude sandbox: `appcenter.servirglobal.net` is not in the
default egress allowlist there, so the crawl returns nothing and the first safeguard fires. That is
the sandbox, not the script. GitHub Actions runners reach it fine.
