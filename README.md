# Hong Kong Quarterly VAR Macro Forecasting Model

Reduced-form VAR model that forecasts core Hong Kong macroeconomic variables
(GDP growth, CPI inflation, unemployment, HIBOR) using two external drivers
(China GDP growth, US federal funds rate).

## Quick start

```bash
pip install -r requirements.txt
python hk_var_model.py
```

Optional controls:

```bash
python hk_var_model.py --lag-criterion bic --max-lags 8 --max-params-ratio 0.75
```

Model controls:

```bash
python hk_var_model.py --model-type auto --auto-bvar-threshold 0.18 --bvar-lambda 1.0
```

## Variables

| Variable | Description | Transform |
|---|---|---|
| `gdp_growth` | HK real GDP growth (YoY %) | level |
| `cpi_inflation` | HK CPI inflation (YoY %) | level |
| `unemployment` | HK unemployment rate (%) | first-differenced if non-stationary |
| `hibor_3m` | 3-month HIBOR (%) | level |
| `china_gdp` | China real GDP growth (YoY %) | level |
| `us_ffr` | US effective federal funds rate (%) | first-differenced if non-stationary |

## Pipeline

1. **Data assembly** — tries FRED public CSV endpoints; falls back to a
   calibrated synthetic dataset that matches Hong Kong's stylised macro facts.
2. **Diagnostics** — ADF stationarity tests, AIC/BIC lag selection with
   parameter-count guardrails, correlation analysis, and reproducibility report.
3. **Estimation** — supports `VAR` (OLS) and `BVAR`-style ridge shrinkage; `auto`
   mode switches to BVAR when parameter load is high.
4. **Backtesting** — expanding-window out-of-sample evaluation vs AR(1) and
   random-walk benchmarks (1Q and 4Q horizons).
5. **Scenarios** — baseline forecast with bootstrapped 80 % confidence bands,
   plus "weak external demand" and "global easing" shock paths.

## Outputs (in `output/`)

| File | Contents |
|---|---|
| `01_raw_data.png` | Panel chart of all six series |
| `02_correlation.png` | Heatmap of transformed-series correlations |
| `03_stability.png` | Companion-matrix eigenvalues vs unit circle |
| `04_irf.png` | Full impulse-response function grid |
| `05_backtest_h1.png` | RMSE bar chart, 1-quarter horizon |
| `05_backtest_h4.png` | RMSE bar chart, 4-quarter horizon |
| `06_scenario_forecast.png` | Scenario fan charts for HK domestic variables |
| `forecast_scenarios.csv` | Tabular forecasts for all scenarios |
| `data_dictionary.csv` | Variable-level source and transform metadata |
| `model_diagnostics.txt` | Transform and lag-selection diagnostics |
| `methods_note.txt` | Full methods note with assumptions and limitations |

## Using real data

Preferred: provide `data/hk_macro_quarterly_real.csv` with columns
`date,gdp_growth,cpi_inflation,unemployment,hibor_3m,china_gdp,us_ffr`.
The script will load it automatically unless `--no-local-real-data` is set.

Fallback path: if local and FRED data are unavailable, the pipeline uses a
calibrated synthetic dataset so estimation/testing still runs end-to-end.
