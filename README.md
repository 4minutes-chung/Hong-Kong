# Hong Kong External-Shock Transmission Research Note

Quarterly macro-econometric project for the question:

> How do US monetary policy shocks and China growth shocks transmit to Hong Kong's real economy under the currency board?

The current canonical panel has **113 quarters, 1998Q1-2026Q1**, and **7 variables**. For the active research plan and model hierarchy, use `CLAUDE.md`.

## Quick Start

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
MPLCONFIGDIR=/tmp/mpl_cfg python hk_var_model.py --lag-criterion bic --model-type var
MPLCONFIGDIR=/tmp/mpl_cfg python hk_var_model.py --include-property --model-type vecm --lag-criterion bic
MPLCONFIGDIR=/tmp/mpl_cfg python -m pytest tests/ -q --tb=short
python -m ruff check .
```

## Current Variables

Default Cholesky / recursive ordering:

`us_ffr`, `china_gdp`, `hk_exports_china_yoy`, `gdp_growth`, `cpi_inflation`, `unemployment`, `hibor_3m`

Property-extension ordering:

`us_ffr`, `china_gdp`, `hk_exports_china_yoy`, `hk_property_price_idx`, `gdp_growth`, `cpi_inflation`, `unemployment`, `hibor_3m`

| Variable | Meaning | Current source |
|---|---|---|
| `us_ffr` | US effective federal funds rate, quarterly mean | FRED `FEDFUNDS` |
| `china_gdp` | China real GDP YoY growth in current dataset; name kept for code compatibility | OECD QNA `B1GQ`, `GY`; FRED nominal fallback only if OECD fails |
| `hk_exports_china_yoy` | HK total exports to Chinese Mainland, YoY growth | C&SD table 410-50013 |
| `gdp_growth` | HK real GDP YoY growth | C&SD table 310-30001 |
| `cpi_inflation` | HK Composite CPI YoY inflation | C&SD table 510-60001 |
| `unemployment` | HK unemployment rate | C&SD table 210-06101 |
| `hibor_3m` | 3-month HIBOR | HKMA HIBOR fixing API |
| `hk_property_price_idx` | HK private domestic property-price index; optional asset-price channel | RVD/data.gov.hk `1.4M` official All Classes index |

## VAR Benchmark Run

Command:

```bash
MPLCONFIGDIR=/tmp/mpl_cfg python hk_var_model.py --lag-criterion bic --model-type var
```

Current diagnostics:

| Item | Result |
|---|---|
| Sample | 1998Q1-2026Q1 raw; 112 transformed observations |
| Selected VAR lag | BIC p=1 |
| Stability | max eigenvalue 0.9389, stable |
| Johansen rank on I(1) subset | trace@95% rank 2 |
| Main remaining model issue | residual autocorrelation in several equations |

Key FEVD shares at horizon 8 from the current 7-variable VAR:

| Shock | Target | Share |
|---|---:|---:|
| `hk_exports_china_yoy` | HK GDP growth | 24.9% |
| `china_gdp` | HK GDP growth | 16.1% |
| `us_ffr` | HIBOR 3M | 53.7% |
| `us_ffr` | HK unemployment | 10.6% |

## Main Property VECM

Command:

```bash
MPLCONFIGDIR=/tmp/mpl_cfg python hk_var_model.py --include-property --model-type vecm --lag-criterion bic
```

This keeps the same research question. Property prices enter as a Hong Kong asset-price transmission channel under the currency board, not as a new topic and not as a causal claim.

## Important Files

| File | Purpose |
|---|---|
| `hk_var_model.py` | Estimates the VAR, BVAR, and VECM models |
| `fetch_real_data.py` | Rebuilds official/API data panel |
| `data/hk_macro_quarterly_real.csv` | Canonical local data loaded first |
| `data/source_metadata.json` | Source lineage for each variable |
| `data/hk_macro_quarterly_property_model.csv` | Optional macro-property panel with RVD property-price growth |
| `data/property_source_metadata.json` | Source lineage for the official RVD property sidecar |
| `DATA_DOWNLOAD.md` | Data schema and source notes |
| `DATA_GAPS_RESEARCH_PLAN.md` | Current macro research problems and next steps |
| `output/model_diagnostics.txt` | Latest stationarity, lag, cointegration diagnostics |
| `output/methods_note.txt` | Latest generated methods summary |

## Current Caveats

- The code column is still named `china_gdp`; in the current dataset it is documented as China real GDP YoY from OECD. If OECD fails during a future rebuild, it can fall back to FRED nominal GDP, so always check `data/source_metadata.json`.
- For the current model hierarchy, use `CLAUDE.md`.
- Property prices matter for Hong Kong. They are now available from the official RVD All Classes index in `data/hk_property_price_rvd_quarterly.csv` and the model-ready merged panel `data/hk_macro_quarterly_property_model.csv`. Use them as an asset-price transmission channel under the same research question.
- Use `--include-property --model-type vecm` for the property-channel VECM. The default command remains the cleaner 7-variable VAR run.
- `data/us_mp_shock_quarterly.csv` is a sidecar research extension for cleaner US monetary-policy shocks, not part of the canonical 7-variable baseline.
