# Open Data &amp; Microservices Reference

*Compiled 2026-09-04 by research agents using live web search/fetch — not from memory. Every entry below was independently verified; anything uncertain is flagged explicitly in its own section rather than smoothed over. This is a reference for what the Gateway (§02 of the engineering plan) could integrate with, organized by domain relevant to the Global Risk, Food Security, and Natural Resource Management platforms.*

## How to read this document

Each entry lists: what it provides, how to access it (API/bulk/Earth Engine/etc.), license/cost, and a one-line fit for a microservices Gateway. Entries marked with ⚠️ have a real caveat (license conflict, stale data, regional-only coverage, or paywalled access) — read those before integrating, not after.

---

## 1. World Population Data

| Dataset | Provider | Resolution | Coverage | Access | License |
|---|---|---|---|---|---|
| WorldPop Global Project Pop | U. Southampton et al. | ~100m (also 1km) | 2000–2030 | REST API (`worldpop.org/rest/data`), bulk, EE `WorldPop/GP/100m/pop` | CC BY 4.0 |
| GPWv4.11 (+ UN-Adjusted) | CIESIN/NASA SEDAC | 1km | 2000–2020, 5-yr steps | EE `CIESIN/GPWv411/*`, Earthdata bulk | Open/free |
| Meta/CIESIN HRSL | Meta Data for Good + CIESIN | ~30m | ~160 countries | AWS S3 (`s3://dataforgood-fb-data/`), HDX | CC BY 4.0 |
| LandScan Global / HD | ORNL + NGA | 1km (Global) / ~90m (HD) | Annual | New open portal `landscan.ornl.gov` | **Newly CC BY 4.0** (was paid/restricted until 2026) |
| GHS-POP (GHSL) | EC Joint Research Centre | 100m | 1975–2030 | EE `JRC/GHSL/P2023A/GHS_POP`, GHSL portal | Open, attribution required |

⚠️ **Meta HRSL**: AWS metadata says "quarterly" updates but multiple sources indicate it hasn't been meaningfully updated since ~2024 — treat as a static/legacy baseline, not a live feed.
⚠️ **GPWv5**: announced, targeting release mid-2026 at 1km — not yet available. Don't reference as current.
⚠️ **LandScan**: the free/open licensing change (2026) is a major and recent shift from decades of paid licensing — the new `landscan.ornl.gov` portal's exact download mechanics weren't independently confirmed (JS-rendered page); verify manually before depending on it operationally.

---

## 2. World Structure / Building Footprint Data

| Dataset | Provider | Coverage | Format | Access | License |
|---|---|---|---|---|---|
| MS Global ML Building Footprints | Microsoft | Global, ~1.4B polygons | GeoJSON bulk / GeoParquet (STAC) | Azure Blob bulk; STAC `ms-buildings` on Planetary Computer | ⚠️ CDLA Permissive 2.0 (repo) vs. ODbL cited on Planetary Computer — **conflicting, verify before redistributing** |
| Google Open Buildings v3 | Google Research | Africa/S&amp;SE Asia/LatAm, 1.8B polygons | CSV, EE `GOOGLE/Research/open-buildings/v3/polygons` | Bulk CSV, EE, HDX | CC-BY-4.0 or ODbL (chooser) |
| Google Open Buildings 2.5D Temporal | Google Research | Same regions, annual 2016–2023 | EE `GOOGLE_Research_open-buildings-temporal_v1` | EE, HDX | CC-BY-4.0 |
| VIDA Combined (Google+MS+OSM) | VIDA / Radiant Earth | Global, 182 countries, ~2.7B deduped polygons | GeoParquet, FlatGeobuf, PMTiles | `source.coop/vida/google-microsoft-osm-open-buildings`, no auth | ODbL-1.0 |
| GHSL GHS-BUILT-S/V/H/C | EC Joint Research Centre | Global raster | COG, EE `JRC/GHSL/P2023A/*` | JRC FTP, EE | Free/open |
| OSM Buildings | OpenStreetMap | Global, uneven density | GeoJSON/Shapefile | Overpass API, HOT Export Tool, Geofabrik | ODbL-1.0 |
| World Settlement Footprint (DLR) | German Aerospace Center | Global raster mask | GeoTIFF | DLR EOC Geoservice download | CC BY 4.0 |

**Recommended default**: VIDA's combined dataset — one cloud-native GeoParquet/PMTiles source stitched from the three major providers, avoiding three separate ingestion pipelines.

---

## 3. World Crop Data

| Dataset | Provider | Coverage | Resolution | Cadence | Access | License |
|---|---|---|---|---|---|---|
| ESA WorldCereal | ESA Consortium | Global | 10m | 2021 only (⚠️ 2023/24 expansion "in progress," no release date) | EE `ESA/WorldCereal/2021/MODELS/v100`, Zenodo, openEO | CC-BY-4.0 |
| USDA NASS CDL | USDA NASS | ⚠️ **US only** | 10m (2024+)/30m | Annual | CroplandCROS, EE `USDA/NASS/CDL` | Public domain |
| NASA Harvest Portal | NASA Harvest (UMD) | Global (aggregator) | Varies | Varies | REST API (`data.harvestportal.org/api-docs`) | Mixed, per-dataset |
| GEOGLAM Crop Monitor | GEOGLAM/NASA Harvest | Global | Assessment, not raster | Monthly | Web/PDF/Zenodo — ⚠️ **no confirmed machine API** | Unverified |
| Copernicus Land Cover / LCFM | Copernicus/EC | Global | 100m legacy / 10m new | Migrating (⚠️ moved to Copernicus Data Space Ecosystem Sept 2025 — old endpoints/accounts invalid) | CDSE, WMS, EE (legacy) | Open |
| FAO GIEWS / ASIS | FAO | Global | Pixel-GAUL2 | Dekadal/quarterly | WMTS, ArcGIS Online, CSV — ⚠️ no unified API | Unverified license |
| JRC ASAP | EC Joint Research Centre | Global, 80-country focus | ~250–500m | 10-daily | WMS/WFS + metadata API | EU open reuse |
| USGS/NASA GFSAD | USGS | Global (regional tiles) | 30m regional / 1km global | ⚠️ Static, 2015 reference year | LP DAAC (30m); EE `USGS/GFSAD1000_V1` (V0 deprecated) | Public domain |
| ESA WorldCover | ESA/VITO | Global | 10m | ⚠️ Only 2020/2021 epochs confirmed | EE `ESA/WorldCover/v200` | CC-BY-4.0 |

**Best fit for JRC ASAP**: already exposes WMS/WFS + a machine-readable indicator-discovery endpoint (`getIndicatorsInfo.php`) — one of the easiest sources to wrap as a Gateway adapter for both map layers and tabular indicators.

---

## 4. World Field Boundary Data

**Honest framing**: this category is genuinely sparse compared to the others. One credible *global* dataset (model-inferred, not surveyed), one strong pan-EU harmonized effort, and a patchwork of national cadastres that are open mainly because they're government subsidy-payment records.

| Dataset | Maintainer | Coverage | Notes | Access | License |
|---|---|---|---|---|---|
| Fields of the World (FTW) — benchmark | NASA Harvest, Taylor Geospatial, Microsoft AI for Good, Clark/ASU/WashU | 24 countries | Training/benchmark data (1.6M polygons), not a wall-to-wall map | `source.coop/kerner-lab/fields-of-the-world`, HF mirror | CC-BY variants |
| FTW — Global wall-to-wall product | Taylor Geospatial + Microsoft + academic partners | **Global**, 195 countries | ⚠️ Model-inferred (not surveyed) — ship confidence scores, don't present as ground truth | `source.coop/ftw/global-data` — GeoParquet/PMTiles/STAC, no auth | CC-BY-4.0 |
| France RPG | ASP (French govt) | France | Annual, majority crop group per parcel | data.gouv.fr | Licence Ouverte v2.0 |
| AI4Boundaries | EU JRC | 7 EU countries | AI-ready, harmonized labels | JRC Open Data Catalogue | Open |
| EuroCrops | TU Munich + partners | 16 EU countries | Adds crop taxonomy (HCAT) on top of boundaries | GitHub + Zenodo | CC-BY-SA 4.0 |
| LPIS (raw, per-country) | Individual EU member states | EU-wide, uneven | ⚠️ Openness **not uniform** — verify per country | Varies (e.g. data.public.lu) | Varies, CC0 in some states |
| Netherlands BRP | RVO | Netherlands | Annual, OGC API | `api.pdok.nl/rvo/gewaspercelen` | Open |
| Denmark "Marker" | Danish Ministry of Food/Agriculture | Denmark | Annual since 2005 | landbrugsgeodata.fvm.dk; also on Source Cooperative | Open |

**Not open — do not present as open data**: Regrow, EOSDA, and Planet's field-boundary APIs are commercial-only. USDA's Common Land Unit (CLU) registry remains non-public.

**Real gap, stated plainly**: no credible open field-boundary dataset exists for India, Brazil, Sub-Saharan Africa, or China beyond FTW's model-inferred global layer. This should be named directly in any platform document rather than papered over.

**Useful meta-resource**: [fiboa](https://github.com/fiboa/data-survey) — a community survey + schema/CLI for normalizing ~30 countries' worth of disparate field-boundary formats into one GeoParquet spec. Worth adopting as the normalization layer if the Gateway ingests multiple national sources.

---

## 5. Adjacent Open EO / Hazard Microservices

| Service | Provides | Access tier | Real-time? |
|---|---|---|---|
| NASA POWER | Solar/met/climate parameters | Fully open/free, no key | Yes (sync REST) |
| Microsoft Planetary Computer | STAC catalog of major EO datasets | Free (data/API); "Pro" is a separate paid enterprise product | Yes |
| Google Earth Engine | Petabyte-scale EO archive + analysis | Free (noncommercial) / paid (commercial — GCP billing required) | Yes |
| Copernicus Data Space Ecosystem | Full Sentinel archive + processing | Free w/ generous quota, registration required | Yes |
| Sentinel Hub | On-the-fly Sentinel/Landsat/PlanetScope processing | Free via CDSE quota; standalone Planet accounts are 30-day trial then paid | Yes |
| USGS Earthquake feeds | Real-time/historical earthquakes | Fully open/free | Yes (polling) |
| USGS M2M (EarthExplorer) | Landsat + 300+ USGS datasets | Free but **approval-gated** (days-long wait for machine access) | Async orders |
| GDACS | Multi-hazard real-time alerts | Open/free (⚠️ unofficial API — no formal spec page) | Yes (polling) |
| NASA GIBS/Worldview | Near-real-time global imagery tiles | Fully open/free | Yes (tiles) |
| OpenET | Field-scale evapotranspiration/water use | Free w/ API key | ⚠️ **US/CONUS only — not usable for international SERVIR regions** |
| GloFAS (via EWDS) | Global flood forecasting | Free w/ registration; ⚠️ moved off general CDS to dedicated EWDS in 2026 | Async/batch (queued, not sync REST) |
| INFORM Risk Index | Composite country-level risk scores | Free/open (light survey) | No — static, biannual |
| PDC DisasterAWARE | Multi-hazard early warning platform | ⚠️ **Gated** — free only for vetted practitioners after approval; broader use is a paid contract | Partner-dependent |

**Quick wins — lowest integration effort, no auth needed**: NASA POWER, USGS Earthquake feeds, NASA GIBS/Worldview, GDACS. These can be wired into a Gateway with a simple server-side proxy/cache and no credential management.

**Needs real lead time**: USGS M2M (approval process), PDC DisasterAWARE (partnership agreement), GloFAS (registration + async batch pattern, not sync REST).

**Scope limitation to flag prominently, not bury**: OpenET is CONUS-only and cannot serve the plan's international food-security/water-security use cases despite the name suggesting a general water-use API.

---

## Cross-cutting flags for whoever integrates this

1. **License conflicts exist and matter**: Microsoft's building footprints have a genuine CDLA-vs-ODbL conflict between the GitHub repo and the Planetary Computer listing. Don't commit to redistribution terms without a direct confirmation.
2. **"Global" often isn't**: USDA CDL, OpenET, and GFSAD30's Africa/South-Asia tiles are frequently cited as if universal — verify actual coverage per source before a regional hub assumes it has data for its area.
3. **Static vs. live matters for architecture**: INFORM Risk, GEOGLAM Crop Monitor, and GFSAD are periodic/static products best served via scheduled ETL into a cache — not appropriate for synchronous request/response Gateway patterns the way NASA POWER or GIBS are.
4. **Field boundaries are the weakest category globally** — any platform promise involving field-level agricultural monitoring outside the EU/US should scope expectations to FTW's model-inferred (not surveyed) global layer, explicitly labeled as such.

*See [`servir-platform-inventory-repo.md`](servir-platform-inventory-repo.md) for the AI memory/decision record, and [`RED_TEAM_REVIEW.md`](RED_TEAM_REVIEW.md) for the adversarial review of the engineering plan itself.*
