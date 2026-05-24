# Data Source and Variable Reference
**Project:** Hong Kong VARX — Monetary and China Growth Transmission
**Sample:** 1998 Q1 – 2026 Q1 | 113 quarterly observations
**Last updated:** 2026-05-23

---

## Model-Ready Dataset

**File used in model:** `data/hk_macro_quarterly_property_extension.csv`
- 113 rows × 26 columns (only 8 used in model after column-select + dropna)
- Select needed columns BEFORE `.dropna()` — remark columns are 112/113 NaN

**Corrected model file (post Phase 3):** `data/hk_macro_varx_ready.csv`
- Replaces `hk_property_price_idx` (I(1)) with `hk_property_price_qoq` (I(0))
- 112 obs (one lost to QoQ differencing)

---

## Variable Dictionary — All Variables Used

### Exogenous (HK cannot influence these)

| Variable | Role | Real/Nominal | Form | Units | Source |
|---|---|---|---|---|---|
| `us_ffr` | Exogenous | Nominal | Level | % p.a. | FRED FEDFUNDS, monthly → quarterly mean |
| `china_gdp` | Exogenous | Real (SA, chain-linked) | YoY % growth | % | OECD QNA `CHN.B1_GE.GPSA.Q`, GY transform |

### Endogenous (HK domestic system)

| Variable | Role | Real/Nominal | Form | Units | Source |
|---|---|---|---|---|---|
| `hk_exports_china_yoy` | Endogenous | Nominal HKD value | YoY % | % | C&SD table 410-50013, monthly YoY → quarterly mean |
| `gdp_growth` | Endogenous | Real (chain-linked volume) | YoY % | % | C&SD table 310-30001 |
| `cpi_inflation` | Endogenous | Price index change | YoY % | % | C&SD table 510-60001, Composite CPI, monthly → quarterly mean |
| `unemployment` | Endogenous | Rate | Level | % | C&SD table 210-06101, M3M SA → quarterly end-of-quarter |
| `hibor_3m` | Endogenous | Nominal | Level | % p.a. | HKMA hibor.fixing, monthly → quarterly mean |
| `hk_property_price_qoq` ✓ | Endogenous | Nominal price index | QoQ % change | % | RVD All Classes index, QoQ % of quarterly mean |

---

## ADF Stationarity Results (ADF with BIC lag selection, n=113)

| Variable | ADF p-value | Decision | Notes |
|---|---|---|---|
| `us_ffr` | 0.036 | I(0) | Stationary at 5% |
| `china_gdp` | 0.000 | I(0) | Confirmed in Phase 1 — growth rate, not level |
| `hk_exports_china_yoy` | 0.000 | I(0) | Growth rate |
| `gdp_growth` | 0.016 | I(0) | Stationary at 5% |
| `cpi_inflation` | 0.153 | Borderline | Fails at 5%, passes at 10% — long HK deflation episode (1998–2004) creates persistence; already a growth rate, not differenced further |
| `unemployment` | 0.082 | Borderline | Fails at 5%, passes at 10% — treated as I(0) in levels; unemployment is mean-reverting over full sample |
| `hibor_3m` | 0.037 | I(0) | Pegged to USD via LERS, mean-reverts |
| `hk_property_price_idx` | 0.822 | **I(1) — DROPPED** | Raw price index level; replaced with QoQ growth |
| `hk_property_price_qoq` | 0.000 | **I(0) — USED** | First difference of index; no stochastic trend |

---

## What Was Dropped and Why

| Variable | Status | Reason |
|---|---|---|
| `hk_property_price_idx` | Dropped from model | I(1) level series; using in VAR creates unit root problem |
| `hk_property_price_yoy` | Not used | YoY (p=0.021) has base-effect distortions; QoQ is cleaner |
| `hk_property_price_qoq_ann` | Not used | Annualised version of QoQ — same information as QoQ |
| `property_class_a/b/c/d/e` | Not used | Sub-indices; aggregate used |
| `us_mp_shock_quarterly.csv` | Not used | Romer-Romer monetary policy shock series — not yet incorporated |

---

## Property Data Detail

**Source:** Rating and Valuation Department (RVD) / data.gov.hk
**Dataset:** Private Domestic — Price Indices by Class (Territory-wide), Monthly
**Raw frequency:** Monthly → quarterly mean
**Provisional flag:** RVD marks recent quarters "P" (provisional)

| Measure | Column | ADF p | Used? |
|---|---|---|---|
| All-classes price index (level) | `hk_property_price_idx` | 0.822 | No — I(1) |
| YoY % change | `hk_property_price_yoy` | 0.021 | No — base effects |
| QoQ % change | `hk_property_price_qoq` | 0.000 | **Yes** |
| Annualised QoQ | `hk_property_price_qoq_ann` | 0.000 | No — redundant |

---

## Model Specification (Current — post Phase 3 correction)

```
VARX(1)
Exogenous:  us_ffr, china_gdp
Endogenous: hk_exports_china_yoy, gdp_growth, cpi_inflation,
            unemployment, hibor_3m, hk_property_price_qoq
Lag:        1 (BIC)
Sample:     1999 Q2 – 2026 Q1 (112 obs after 1 lag lost)
```

Cholesky ordering:
```
hk_exports_china_yoy → gdp_growth → cpi_inflation →
unemployment → hibor_3m → hk_property_price_qoq
```

---

## Residual Autocorrelation (Ljung-Box, lag=8)

### Before fix (property in levels)

| Equation | p-value | Result |
|---|---|---|
| hk_exports_china_yoy | 0.097 | pass |
| gdp_growth | 0.000 | FAIL |
| cpi_inflation | 0.001 | FAIL |
| unemployment | 0.171 | pass |
| hibor_3m | 0.959 | pass |
| hk_property_price_idx | 0.005 | FAIL |

### After fix (property_qoq) — hk_macro_varx_ready.csv

| Equation | p-value | Result |
|---|---|---|
| hk_exports_china_yoy | 0.094 | pass |
| gdp_growth | 0.000 | **FAIL** |
| cpi_inflation | 0.005 | **FAIL** |
| unemployment | 0.170 | pass |
| hibor_3m | 0.884 | pass |
| hk_property_price_qoq | 0.106 | pass |

2/6 fail. Proven structural breaks (Chow test): gdp at 2008+2020, cpi at 2020.

---

## Known Limitations

1. **Residual autocorrelation** in `gdp_growth` and `cpi_inflation` — reflects near-unit-root persistence and long HK business cycles (1998 deflation, 2003 SARS, GFC, COVID), not fixable with additional lags at this sample size. Crisis dummies (AFC/SARS/GFC/COVID) tested — no improvement.
2. **`hk_exports_china_yoy` is nominal** — no quarterly export price deflator available. CPI is wrong basket; working in YoY growth rates partially cancels slow price trends.
3. **No financial channel variable back to 1998** — BIS Locational Banking Statistics suppress China counterparty series pre-2014. Post-2010 China–HK financial transmission (Stock Connect, mainland property buyers) is unmodelled.
4. **`us_ffr` is a monetary-conditions proxy**, not a clean policy surprise (Romer-Romer shock series available but not yet incorporated).
5. **BVAR extension** — Minnesota prior BVAR is the correct fix for small-sample persistence but is out of scope for this research note.
