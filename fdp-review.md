# Forest Data Partnership — deep review

**10 September 2026.** Corrects the 10 Sep entry in `planscape-ceo-fdp-review`, which reported FDP as
"in the plan, no gap." Its *presence* was fine. Its *depth* was not: the plan treated FDP as a map
feed, and it is a code and model ecosystem.

## What FDP actually is

WRI-convened partnership (public launch Nov 2022) to build a shared land-use data ecosystem for
commodity-driven deforestation, with FAO and Google. Five workstreams; the two that matter here are
"deploy consistent open-source validated data" and "align stakeholders around key datasets."

| Surface | What's there |
|---|---|
| `google/forest-data-partnership` | MIT. **Downloadable TensorFlow models**, Earth Engine notebooks, cloud functions, method paper `arXiv:2405.09530`. 53★ |
| `forestdatapartnership` org | 6 repos — `whisp` (Python, MIT), `whisp-app` (TS), `whisp-plugin` (QGIS), `whisp-dashboards`, `commodity-recognition-book`, `models` (Apache-2.0) |
| Earth Engine catalogue | `projects/forestdatapartnership/assets` — commodity probability models, 10 m |
| Whisp service | Live API `whisp.openforis.org/api/docs`, ≤5,000 geometries; PyPI `openforis-whisp` for unlimited |

## Correction 1 — palm oil is not missing

The plan's commodity matrix marked palm oil a **New build**, on the reasoning "FDP covers
cocoa/coffee/rubber — palm is the missing fourth."

Wrong. The Earth Engine catalogue publishes **`palm_model_2025a`, `2025b`, `2026a`** alongside cocoa,
coffee and rubber. Google's own write-up confirms: "coffee, cocoa, oil palm and rubber," 10 m,
CC BY 4.0, 2020 and 2024 available with a backfill underway for every year 2017–2025.

That flips the most expensive cell in the palm row from a from-scratch build to a partner adoption.
No soy layer exists — soy is `Risk_ACrop` in Whisp via other datasets, so the plan's soy row stands.

Two caveats now recorded in the plan: these are **probability surfaces**, not classified maps (you
choose the threshold), and FDP's own catalogue notes they are **not yet peer-reviewed** — an
operational input, not citable ground truth.

## Correction 2 — Whisp's attribution

The plan said "Whisp (Open Foris, MIT)." MIT is right; the rest was imprecise. Whisp lives at
`forestdatapartnership/whisp`, ships on PyPI as `openforis-whisp`, and is Open Foris/FAO-*associated*
via the AIM4Forests programme (`open-foris@fao.org`). v3.0.0a14, 569 commits, 34★.

More usefully: it is **callable today**. A live API, a QGIS plugin and a TypeScript app already exist.
The §05 EUDR Compliance Agent does not need Whisp built or wrapped from source to start — it needs an
MCP shim over an existing endpoint.

## The finding — consume the maps, or retrain the models

A published map is a fixed answer at a fixed threshold. A published *model* is something a hub can
fine-tune on its own reference plots. FDP publishes both.

§05's largest build item is regional crop-type classifiers via `servir-aces` (Decision #20). For the
four EUDR tree crops that build may be avoidable: retraining an FDP model on hub reference data is
materially smaller than training from scratch and inherits a pan-tropical baseline. **This should be
tested before Decision #20 prioritises tree crops for a from-scratch build.**

The models run on Google's **Satellite Embedding** (AlphaEarth Foundations), already named in §03's
foundation-model stack. FDP is the plan's clearest instance of that stack in production rather than
in principle — a template for how §03's other foundation models get applied.

## The partnership opening is closer than it looks

SERVIR is not listed as an FDP partner. But FDP's published data contributors include the **Alliance
of Bioversity International and CIAT** — the lead institution of SERVIR's own **Tropical South
America** hub (§07). The institutional bridge already exists.

The fit is two-way, not a favour: FDP's workstreams want validated regional reference data, which is
exactly what SERVIR hubs and Collect Earth Online sample archives produce. SERVIR wants pan-tropical
tree-crop coverage it would otherwise build.

## Plan edits

| Where | Change |
|---|---|
| §05 palm oil × Clock 1 | **New build → Partner**; names `palm_model_2026a` |
| §05 cocoa / coffee / rubber cells | Asset IDs, CC BY 4.0, probability-surface and peer-review caveats |
| §05 "EUDR tree-crop coverage" row | All **four** commodities; notes models are downloadable |
| §05 Whisp row | Attribution corrected; live API, QGIS plugin, PyPI name recorded |
| §05 | New element **F7** — consume-vs-retrain, the AlphaEarth link, the Alliance/CIAT bridge |
| Appendix | All five FDP sources recorded |
