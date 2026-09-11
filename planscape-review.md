# Three checks — Planscape, Collect Earth Online, Forest Data Partnership

**10 September 2026**

| Asked about | In the plan? |
|---|---|
| **Collect Earth Online** | **Yes** — 6 mentions, load-bearing |
| **Forest Data Partnership** | **Yes** — 6 mentions, load-bearing |
| **Planscape** | **No** — zero. Now added. |

---

## Already in, and properly integrated

**Collect Earth Online** sits in the §06/§07 land-cover backbone: `RLCMS + CEO`, with CEO doing
sample-based labelling and accuracy assessment against the RLCMS product. It appears in the N2
change-detection diagram, the stack table ("None — SERVIR's strongest existing asset"), and the
Already-built cards, citing `SERVIR/RLCMS` and `Servir-Mekong/rlcms`. Also listed as App Center
`/detail/7`. No gap.

**Forest Data Partnership** carries the tree-crop half of §05. It is the named partner source for
cocoa, coffee and rubber in the commodity matrix ("10 m annual, pan-tropical"), sits in the crop-type
backbone row alongside WorldCereal and `servir-aces`, and is a named tool of the **EUDR Compliance
Agent**. The related **Whisp** (Open Foris, MIT) is the adopted risk-flagging workflow. Open Foris and
SEPAL both appear too. No gap.

---

## Planscape — the gap, and it is a structural one

`github.com/OurPlanscape/Planscape` · planscape.org · ~7,200 commits, 26 stars, 10 forks
Angular + Django REST + PostgreSQL/PostGIS, Dockerised. Wraps **ForSys** (Ager, Day, Evers — USFS)
for the optimisation, alongside FVS, GridFire, TreeMap, PROMOTe.
**Licence: CC0 1.0** — public domain, no attribution obligation. The most permissive dependency
anywhere in this plan.
Built by **SIG for the US Forest Service**.

### Why it matters more than "one more tool"

Planscape is not a monitoring capability, and that is the point. Every element specified across
§04–06 answers a monitoring question — what is happening now, what the annualised baseline is, how
it shifts under climate. That is the three-clock grammar and it is deliberate. It also stops one
step short of the question a land manager actually arrives with: **given a fixed budget, where do we
intervene, and what do we get for it?**

Nothing in the plan answered that. The omission was hidden in plain sight, because three use cases
already in §06 imply it:

- where rangers patrol in Prey Lang
- which degraded mining sites in Ghana get remediated first
- which stretches of Vietnamese coast get mangrove protection against shrimp aquaculture

Each is the same constrained-optimisation problem, answered ad hoc, per use case, by hand.
Planscape/ForSys is the reference implementation, and it is SIG's own.

### The constraint — and it is now a pattern, not a coincidence

Planscape runs on **California Regional Resource Kits**: ten resilience pillars, 30 m,
California-only (Sierra Nevada, Southern California, Central Coast, North Coast). Custom dataset
upload is still unbuilt; extension beyond California has been "planned" since 2024.

That is the same shape as `pyretechnics`, which runs on **LANDFIRE** fuel models, US-only. In both
cases the method transfers and the data pipeline does not.

**SIG's fire and land-treatment stack is portable in code and locked in data.** The recurring cost of
adopting any of it into SERVIR is the same line item every time: build the regional input layer.
That is one procurement question, not two, and it should be scoped as one.

---

## Plan edits

| Where | Change |
|---|---|
| §06 | New element **N7 — "The layer this plan does not have"**: the intervention-prioritisation gap, Planscape as reference implementation, the portable-in-code/locked-in-data pattern |
| §08 | New **Decision #23** — adopt Planscape/ForSys, or leave optimisation per use case. Flagged to be scoped *together* with Decision #16's fuel-model layer, since it is the same cost |
| Appendix | `github.com/OurPlanscape` recorded as a partner-tool org alongside `github.com/pyregence` |

The architectural point stands whichever way #23 goes: **if the platform only ever tells governments
what is happening, it stops exactly where their decision begins.**
