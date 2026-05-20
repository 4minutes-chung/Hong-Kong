# Data Handoff

The pipeline loads `data/hk_macro_quarterly_real.csv` first. If that file exists, the old FRED fallback path is mostly irrelevant.

## Canonical CSV Schema

Required columns:

```text
date,gdp_growth,cpi_inflation,unemployment,hibor_3m,china_gdp,us_ffr,hk_exports_china_yoy
```

Rules:

- `date` is the first day of each quarter, e.g. `1998-01-01` for 1998Q1.
- All rates are in percent, not decimals.
- No missing values in the merged estimation sample.
- Keep `data/source_metadata.json` synchronized with the CSV.

## Current Source Hierarchy

| Column | Preferred source | Current status |
|---|---|---|
| `gdp_growth` | C&SD table 310-30001 | Good |
| `cpi_inflation` | C&SD table 510-60001 Composite CPI YoY monthly -> quarterly mean | Good |
| `unemployment` | C&SD table 210-06101, end-of-quarter M3M reading | Good |
| `hibor_3m` | HKMA HIBOR fixing API, monthly -> quarterly mean | Good; cached fallback if HKMA times out |
| `us_ffr` | FRED `FEDFUNDS`, monthly -> quarterly mean | Good |
| `china_gdp` | OECD QNA China real GDP YoY (`B1GQ`, `GY`) | Good if OECD source succeeds; FRED nominal fallback must be labelled |
| `hk_exports_china_yoy` | C&SD table 410-50013, total exports to Chinese Mainland | Integrated |

## Sidecar Data Not In Baseline

| File | Use |
|---|---|
| `data/hk_property_price_rvd_monthly.csv` | Official RVD monthly private domestic price indices by class |
| `data/hk_property_price_rvd_quarterly.csv` | Official RVD quarterly property-price sidecar; main column is `hk_property_price_idx`, the All Classes index |
| `data/hk_macro_quarterly_property_extension.csv` | Canonical macro panel merged with the full property sidecar |
| `data/hk_macro_quarterly_property_model.csv` | Model-ready macro-property panel, 1999Q1-2026Q1, with `hk_property_price_yoy` and `hk_property_price_qoq` |
| `data/property_source_metadata.json` | Source lineage for the RVD property files |
| `data/us_mp_shock_quarterly.csv` | Optional cleaner US monetary-policy shock, but sample ends 2019Q4 |
| `data/china_real_gdp_quarterly.csv` | Backup/check file for China real GDP through 2023Q3 |

## Rebuild Data

```bash
python fetch_real_data.py
MPLCONFIGDIR=/tmp/mpl_cfg python hk_var_model.py --lag-criterion bic --model-type var
MPLCONFIGDIR=/tmp/mpl_cfg python hk_var_model.py --include-property --model-type vecm --lag-criterion bic
MPLCONFIGDIR=/tmp/mpl_cfg python -m pytest tests/ -q --tb=short
```

Before using results, confirm `data/source_metadata.json` says whether `china_gdp` came from OECD real GDP or FRED nominal fallback.

Property source: RVD/data.gov.hk `1.4M.csv`, Private Domestic - Price Indices by Class (Territory-wide) [Monthly]. Use the official `All Classes` index, not a hand-made average of classes.

Property model convention: the baseline remains seven variables. The property-channel VECM is activated explicitly with `--include-property`, which adds `hk_property_price_idx` from the official RVD All Classes index.
