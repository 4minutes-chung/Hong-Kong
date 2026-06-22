# Data Source Reference

**Project:** Hong Kong External Shock Transmission under LERS  
**Model-ready file:** `data/hk_macro_varx_ready.csv`  
**Sample:** 1998 Q1 to 2026 Q1, 113 quarterly observations  
**Frequency:** Quarterly 

---

## Variable Dictionary

### Exogenous

| Variable | Form | Units | Source | Construction |
|---|---|---|---|---|
| `us_ffr` | Level | % p.a. | FRED `FEDFUNDS` | Monthly average to quarterly |
| `china_gdp` | YoY growth | % | OECD QNA `CHN.B1_GE.GPSA.Q` | Quarterly series |

### Endogenous

| Variable | Form | Units | Source | Construction |
|---|---|---|---|---|
| `hibor_3m` | Level | % p.a. | HKMA HIBOR fixing | Monthly average to quarterly |
| `hk_exports_china_yoy` | YoY growth | % | C&SD table 410-50013 | Monthly average to quarterly |
| `hk_property_price_qoq` | QoQ growth | % | RVD All Classes index | Quarterly mean index, then QoQ percent change |
| `gdp_growth` | YoY growth | % | C&SD table 310-30001 | Quarterly series |
| `cpi_inflation` | YoY inflation | % | C&SD table 510-60001 | Monthly average to quarterly |
| `unemployment` | Level | % | C&SD table 210-06101 | Seasonally adjusted M3M, quarter end |

### Diagnostic only

| Variable | Form | Source | Use |
|---|---|---|---|
| `hk_property_price_idx` | Level index | RVD All Classes index | Stationarity and Johansen checks only |

---

## Stationarity Audit

ADF/KPSS results on the current panel (updated 2026-06-20):

| Variable | ADF p | KPSS p | Verdict |
|---|---:|---:|---|
| `hk_exports_china_yoy` | 0.0000 | 0.1000 | I(0) |
| `gdp_growth` | 0.0161 | 0.1000 | I(0) |
| `hk_property_price_qoq` | 0.0000 | 0.0830 | I(0) |
| `hibor_3m` | 0.0368 | 0.0495 | ambiguous |
| `cpi_inflation` | 0.1526 | 0.0202 | I(1) |
| `unemployment` | 0.0821 | 0.0100 | I(1) |
| `hk_property_price_idx` | 0.8222 | 0.0100 | I(1) |

Johansen tests use only the endogenous I(1) block:
`cpi_inflation`, `unemployment`, and `hk_property_price_idx`, which give rank 0
at 95%, so VECM is not used.

`hibor_3m` enters in levels — ADF rejects at 5% but KPSS also rejects at 5%,
giving ambiguous statistical result. Economic rationale: mean-reverting under
the peg. Robustness check with first-differenced HIBOR leaves headline channels
unchanged (see exploration notebook).

---

## Notes and Limitations

- `hk_exports_china_yoy` is nominal, as there is not reliable full-sample quarterly export price deflator.
- `us_ffr` is a monetary-conditions proxy, which is not a exogenous/surprise series.
- `hk_property_price_qoq` is the BVAR property variable transformed from `hk_property_price_idx`.
- `unemployment` is kept in levels; robustness check for using change in unemployment rate is in the exploration notebook.
- The baseline file keeps only contemporaneous `us_ffr` and `china_gdp`; lag checks are in the exploration notebook.
- China-Hong Kong financial integration after 2010 is not directly modelled due to data limitation: relevant data are not available.
- The 1998 Q1 start is a regime choice due to handover of 1997, rather than a data constraint.
