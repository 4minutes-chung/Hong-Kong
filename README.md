# Hong Kong External Shock Transmission under LERS

> 1998Q1-2026Q1 | 113 quarters | BVAR(4), Minnesota prior | HIBOR-first Cholesky ordering

## Figures

![HIBOR vs US FFR](output/readme_hibor_ffr.png)

![FEVD summary](output/phase9a_canonical_fevd.png)

![GDP channel IRFs](output/phase10a_gdp_channels.png)

![LP IRFs vs BVAR IRFs](output/phase10b_lp_irf_4panel.png)

![Conditional OOS RMSE benchmarks](output/oos_rmse_benchmarks.png)

OOS diagnostic is conditional on realized future `us_ffr` and `china_gdp`.

---

## Main Results

| Channel | Main estimate | Timing | Read |
|---|---:|---|---|
| Property -> GDP | 20.5% of GDP FEVD | h=1-2 | largest GDP variance channel |
| Exports -> GDP | 16.6% of GDP FEVD | h=1-2 | China demand channel |
| HIBOR -> GDP | 8.7% of GDP FEVD | h=1-4 | slower direct monetary channel |
| HIBOR -> property | 12.3% of property FEVD | h=1 | fast rate-to-property pass-through |

Timing = BVAR horizons where 90% posterior bands exclude zero.

---

## Robustness

| Check | Result |
|---|---|
| Chow tests | GDP stable at GFC/COVID; CPI has COVID mean break |
| Bai-Perron | 0 residual breaks in all six equations |
| LP-IRF | HIBOR-property, HIBOR-GDP, and property-GDP supported; exports-GDP weaker |
| Delta-u | Headline channels unchanged |
| Exogenous lag | `us_ffr_lag1` does not remove GDP/CPI LB failures; keep q=0 |
| Johansen | Rank 0 on endogenous I(1) block; VECM not used |

---

## Model

| Item | Choice |
|---|---|
| Sample | 1998Q1-2026Q1, 113 quarters |
| Model | BVAR(4), Minnesota prior |
| Exogenous | `us_ffr`, `china_gdp` |
| Ordering | HIBOR, exports, property, GDP, CPI, unemployment |

---

## Files

| File | Role |
|---|---|
| `HK_BVAR_Final.ipynb` | Canonical result notebook |
| `HK_BVAR_Exploration.ipynb` | Baseline development and supplementary checks |
| `fetch_real_data.py` | Rebuild data from APIs |
| `data_source.md` | Data sources and stationarity audit |
| `paper/main.tex` | Paper draft |

---

## Refresh Data

```bash
python fetch_real_data.py
```
