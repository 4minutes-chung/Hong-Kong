# Data Source Reference

**Project:** Hong Kong BVAR — Monetary and China Growth Transmission  
**Model:** BVAR(4) Minnesota prior, HIBOR-first Cholesky ordering  
**Sample:** 1998 Q1 – 2026 Q1 | 113 quarterly observations  
**Model-ready file:** `data/hk_macro_varx_ready.csv`

---

## Variable Dictionary

### Exogenous — HK cannot influence these

| Variable | Form | Units | Source | Notes |
|---|---|---|---|---|
| `us_ffr` | Level | % p.a. | FRED `FEDFUNDS` | Monthly → quarterly mean |
| `china_gdp` | YoY % | % | OECD QNA `CHN.B1_GE.GPSA.Q` | GY transform applied |

### Endogenous — HK domestic system

| Variable | Form | Units | Source | Notes |
|---|---|---|---|---|
| `hibor_3m` | Level | % p.a. | HKMA hibor.fixing | Monthly → quarterly mean. |
| `hk_exports_china_yoy` | YoY % | % | C&SD table 410-50013 | Monthly YoY → quarterly mean. Nominal HKD: no reliable quarterly export price deflator |
| `hk_property_price_qoq` | QoQ % | % | RVD All Classes index | Monthly → quarterly mean, then QoQ % change. Recent quarters marked "P" (provisional) by RVD |
| `gdp_growth` | YoY % | % | C&SD table 310-30001 | Real GDP of HONG KONG chain-linked volume |
| `cpi_inflation` | YoY % | % | C&SD table 510-60001 | Composite CPI, monthly → quarterly mean of inflation rate |
| `unemployment` | Level | % | C&SD table 210-06101 | M3M seasonally adjusted → quarterly end-of-quarter |

---

## Why These Transforms

| Variable | Raw form | Used form | Reason |
|---|---|---|---|
| Property price | Level index I(1) | QoQ % I(0) | Level has unit root (ADF p=0.822); QoQ is stationary (p=0.000) |
| GDP | Level | YoY % | Standard HK official release form; stationary |
| HIBOR | Level | Level | Mean-reverts under LERS peg; I(0) confirmed |
| Unemployment | Level | Level | Mean-reverting over full sample; marginally I(1) |
| Exports | Level | YoY % | Standard trade reporting form; stationary |
| CPI | Level | YoY % | Standard inflation reporting form; marginally I(1)|

---

## Variables Considered and Dropped

| Variable | Reason dropped |
|---|---|
| `hk_property_price_idx` | I(1) level -> replaced with QoQ |
| `hk_property_price_yoy` | YoY has base-effect distortions from 1997–98 crash; QoQ cleaner |
| `hk_property_price_qoq_ann` | Annualised QoQ — redundant |
| `property_class_a/b/c/d/e` | Sub-class indices — aggregate used |
| `us_mp_shock_quarterly.csv` | Romer-Romer monetary policy shock series, not incorporated |
| BIS Locational Banking Statistics | China counterparty series suppressed pre-2014 —> financial channel unmodelled |

---

## Stationarity Results (ADF + KPSS, n=113)

| Variable | ADF p | KPSS p | Verdict |
|---|---|---|---|
| `hk_exports_china_yoy` | 0.000 | 0.100 | I(0) |
| `gdp_growth` | 0.018 | 0.100 | I(0) |
| `hibor_3m` | 0.000 | 0.045 | I(0) / ambiguous |
| `hk_property_price_qoq` | 0.000 | 0.099 | I(0) |
| `cpi_inflation` | 0.171 | 0.016 | I(1) |
| `unemployment` | 0.091 | 0.010 | I(1) |

I(1) endogenous variables: unemployment, cpi_inflation. Both enter the BVAR in levels; Minnesota shrinkage handles the near-unit-root behaviour without differencing. Johansen trace and max-eigenvalue tests (endogenous I(1) block only) find rank=0 — no cointegrating relationship; VECM not warranted.

---

## Known Data Limitations

1. `hk_exports_china_yoy` is nominal — no quarterly export price deflator available.
2. `us_ffr` is a monetary-conditions proxy, not a clean monetary policy surprise.
3. Post-2010 China–HK financial transmission (mainly linkage, Stock Connect, mainland property buyers) is unmodelled, as no suitable series available back to 1998.
4. CPI equation shows a mean break at COVID-19 (Chow test p=0.029): disinflationary episode not fully absorbed by fixed-coefficient BVAR prior.
5. 1998 Q1 start date is regime-justified (post-handover), not instrument-forced. HIBOR panel is continuous across 1997.
