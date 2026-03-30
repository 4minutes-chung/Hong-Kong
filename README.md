# Hong Kong Quarterly VAR Macro Forecasting Model

Six-variable quarterly VAR/VECM pipeline for Hong Kong: external drivers (US effective federal funds rate, China nominal GDP growth) and domestic series (real GDP growth, CPI inflation, unemployment, 3-month HIBOR). Research focus: shock propagation under the currency board (Cholesky ordering is external-first by default).

## Quick start

```bash
pip install -r requirements.txt
MPLCONFIGDIR=/tmp/mpl_cfg python hk_var_model.py --lag-criterion bic --model-type var
```

Recommended: **`--lag-criterion bic`** (parsimonious lags; AIC can pick many lags on short samples). Use `MPLCONFIGDIR` to avoid matplotlib cache warnings.

## Common options

```bash
# Same as project default checks
MPLCONFIGDIR=/tmp/mpl_cfg python hk_var_model.py --lag-criterion bic --max-lags 8 --max-params-ratio 0.8 --model-type var

# Bayesian VAR (Minnesota-style)
MPLCONFIGDIR=/tmp/mpl_cfg python hk_var_model.py --lag-criterion bic --model-type bvar --bvar-lambda1 0.2

# VECM (Johansen rank; see --coint-rank, --vecm-deterministic)
MPLCONFIGDIR=/tmp/mpl_cfg python hk_var_model.py --lag-criterion bic --model-type vecm

# Auto: VAR unless parameter load exceeds threshold, then BVAR
MPLCONFIGDIR=/tmp/mpl_cfg python hk_var_model.py --model-type auto --auto-bvar-threshold 0.18 --bvar-lambda1 0.2
```

## Variables and ordering

**Estimation column order** (default Cholesky / recursive identification):  
`us_ffr`, `china_gdp`, `gdp_growth`, `cpi_inflation`, `unemployment`, `hibor_3m`  
Override with `--cholesky-order col1,col2,...`.

**Transforms** are data-driven (ADF + KPSS): variables classified as unit-root are first-differenced for VAR/BVAR; VECM uses levels. The README table is illustrative only — see `output/model_diagnostics.txt` after a run.

| Variable | Role |
|----------|------|
| `us_ffr` | US effective federal funds rate (%) |
| `china_gdp` | China nominal quarterly GDP, YoY % (FRED `CHNGDPNQDSMEI`) |
| `gdp_growth` | HK real GDP YoY % (official series when using real CSV) |
| `cpi_inflation` | HK CPI YoY % |
| `unemployment` | HK unemployment rate (%) |
| `hibor_3m` | 3-month HIBOR (%) |

## Pipeline (high level)

1. **Data** — Prefer `data/hk_macro_quarterly_real.csv` (see `fetch_real_data.py`, `DATA_DOWNLOAD_CHECKLIST.md`); else FRED CSV endpoints; else calibrated synthetic data.
2. **Diagnostics** — Stationarity (ADF + KPSS), lag selection (AIC/BIC + parameter guardrail), Johansen cointegration (for VECM reporting).
3. **Estimation** — VAR (OLS), Minnesota BVAR, or VECM.
4. **Structural** — Cholesky IRFs, FEVD, historical decomposition; optional sign-restriction IRFs; robustness (ordering, subsamples); exploratory TVP-VAR block.
5. **Evaluation** — Expanding-window backtests vs AR(1) and random walk; scenario forecasts with residual bootstrap bands.

## Outputs (`output/`)

Key artifacts include `01_raw_data.png` … `10_subsample_stability.png`, `fevd_table.csv`, `forecast_scenarios.csv`, `model_diagnostics.txt`, `methods_note.txt`, `vecm_diagnostics.txt` (when VECM runs). Forecast dates start the **first quarter after** the last observation in the estimation sample.

## Real data

Provide `data/hk_macro_quarterly_real.csv` with columns  
`date,gdp_growth,cpi_inflation,unemployment,hibor_3m,china_gdp,us_ffr`  
(quarter-start dates). Loaded automatically unless `--no-local-real-data`.

## Tests

```bash
pip install -r requirements-dev.txt
MPLCONFIGDIR=/tmp/mpl_cfg python -m pytest tests/test_hk_var_model.py -v --tb=short
```

## Paper

LaTeX draft under `paper/` (compile per project rules if you edit `.tex`/`.bib`).
