# AGENTS.md — Full Process Documentation

## Project: Hong Kong Quarterly VAR Macro Forecasting Model

**Research Question:**
> "How do US monetary policy shocks and China growth shocks propagate to Hong Kong's real economy under the currency board?"

**Author:** Steven Chung
**Date range:** March 2026
**Status:** Working paper ready; needs official quarterly **CPI** (and ideally **real** China growth) for strongest journal submission.

**Data handoff:** See **`DATA_DOWNLOAD_CHECKLIST.md`** for preferred sources, known API issues, and tomorrow’s manual download steps. Third-party audit of identification and data risks: **`output/model_review_audit_v3.txt`**.

**Data handoff (manual downloads):** See `DATA_DOWNLOAD.md` — variable priorities, CSV schema, API caveats (CPI and China real GDP are the main gaps).

**Verification bundle:** `output/verification_report_2026.txt` — Super Codex checklist, model-review-math-econ, econometrics-modeling, code-reviewer, and test scope.

---

## 1. Project Overview

A six-variable quarterly Vector Autoregression (VAR) model for Hong Kong, designed to quantify how external shocks — US monetary policy and China real growth — transmit to Hong Kong's domestic economy under the Linked Exchange Rate System (currency board peg to USD).

### Key Findings (VAR, BIC p=3, 1998Q1–2024Q3)

| Shock source | Target | FEVD share (h=8Q) |
|---|---|---|
| China GDP growth | HK GDP growth | 77.5% |
| China GDP growth | HK CPI inflation | 28.7% |
| US FFR | HK HIBOR 3M | 59.2% |
| US FFR | HK GDP growth | < 5% |

**Headline:** China drives the real economy; the US drives interest rates through the currency board.

---

## 2. Development Process (Chronological)

### Phase 0: Inception and Model Design

1. **Initial request:** Build a macro model for Hong Kong.
2. **Scope decision:** Quarterly VAR for 6 variables — 4 domestic (GDP growth, CPI inflation, unemployment, HIBOR 3M) + 2 external (US FFR, China GDP growth).
3. **Model style:** Simple empirical VAR/BVAR (not DSGE).
4. **Implementation plan:** Written as `IMPLEMENTATION_PLAN.md` with 4 phases.

### Phase 1: Core Pipeline Build

Built the end-to-end pipeline in `hk_var_model.py`:

- **Data assembly:** FRED API → fallback to calibrated synthetic data
- **Stationarity testing:** ADF test on all 6 variables
- **Lag selection:** AIC/BIC with parameter-count guardrail
- **Estimation:** OLS-based VAR via `statsmodels`
- **BVAR option:** Minnesota-prior Bayesian VAR with ridge penalty
- **Stability check:** Companion matrix eigenvalue analysis
- **IRFs:** Cholesky-orthogonalized impulse response functions
- **Out-of-sample backtesting:** Expanding window vs AR(1) and Random Walk benchmarks
- **Scenario forecasting:** Baseline + shock paths with bootstrapped 80% CIs

### Phase 2: First Audit and Bug Fixes

**Bugs found and fixed:**

| Bug | Root Cause | Fix |
|---|---|---|
| `AttributeError: 'VARResults' object has no attribute 'companion_matrix'` | `statsmodels` version API change | Built companion matrix manually from `result.coefs` |
| `InvalidIndexError` with `result.resid` slicing | `result.resid` is a DataFrame, not ndarray | Converted to `.values` before slicing |
| `SyntaxError` in f-string | Nested curly braces in f-string | Used intermediate variable |

### Phase 3: Comprehensive Model Audit (Round 1)

Used `model-review-math-econ` skill. Found **12 issues** (1 Critical, 4 High, 4 Medium, 3 Low):

| # | Severity | Issue | Fix |
|---|---|---|---|
| 1 | CRITICAL | Forecasts plotted in transformed space, not levels | Added `_invert_transforms()` with cumulative sum for diffs |
| 2 | HIGH | Scenario shocks defined in transformed space | Added `_shock_in_level_space()` converting levels to diffs |
| 3 | HIGH | Only ADF test; no KPSS confirmation | Dual ADF+KPSS with conflict resolution logic |
| 4 | HIGH | Cholesky IRFs inconsistent between VAR/BVAR | Unified `_cholesky_irf()` using companion matrix for both |
| 5 | HIGH | No cointegration test before differencing | Added Johansen test on I(1) subset |
| 6 | MEDIUM | Minnesota prior structure mismatch | Fixed per-equation diagonal prior in `fit_bvar_minnesota()` |
| 7 | MEDIUM | Bootstrap ignores parameter uncertainty | Documented as limitation; residual-only bootstrap |
| 8 | MEDIUM | FRED transform via value heuristic | Switched to metadata flag `needs_pct_change` in `DATA_SPEC` |
| 9 | MEDIUM | Synthetic structural breaks as regime dummies | Changed to additive shock vectors in VAR DGP loop |
| 10 | LOW | No df correction in BVAR sigma_u | Fixed: `resid.T @ resid / (nobs - ncoef)` |
| 11 | LOW | HIBOR proxy not documented | Added inline documentation |
| 12 | LOW | No Granger causality tests | Added `granger_causality_diagnostics()` |

All 12 issues fixed and verified.

### Phase 4: Model Audit (Round 2)

Second-pass audit found **4 remaining issues** (2 Medium, 2 Low):

| # | Severity | Issue | Fix |
|---|---|---|---|
| 1 | MEDIUM | Dead code: `_minnesota_prior_precision()` never called | Removed entirely |
| 2 | MEDIUM | Scenario history plotted from transformed df, not raw levels | Pass `df_raw` to `_plot_scenarios()` |
| 3 | LOW | Global `np.random.seed` shared across stages | Split into `_RNG_DATA` and `_RNG_BOOT` generators |
| 4 | LOW | Cholesky ordering not configurable | Added `--cholesky-order` CLI arg; default: external-first |

All 4 issues fixed and verified.

### Phase 5: Academic Assessment

Used `academic-mentor` skill. Key findings:

- **Novelty:** Adequate — HK-specific VAR under currency board is useful but not methodologically novel
- **Feasibility:** Strong — pipeline runs end-to-end, diagnostics automated
- **Impact:** Depends on research question and real data
- **Methodology:** Strong post-audit
- **Positioning:** Needs a research question + FEVD + historical decomposition to be publishable

**Research question adopted:**
> "How do US monetary policy shocks and China growth shocks propagate to Hong Kong's real economy under the currency board?"

### Phase 6: Real Data Ingestion

**Challenge:** Programmatic quarterly HK data proved difficult to obtain from free APIs.

- FRED: Only US FFR available as genuine quarterly data; HK/China series returned errors
- World Bank: Only annual data available for HK GDP, China GDP, CPI, unemployment
- OECD/IMF APIs: Returned 403/404 errors

**Solution adopted:**
1. Fetched FRED US FFR (monthly) → aggregated to quarterly
2. Fetched World Bank annual data (HK GDP growth, CPI inflation, unemployment, China GDP)
3. Interpolated annual to quarterly using cubic spline (`scipy.interpolate.CubicSpline`)
4. Derived HIBOR 3M as FFR + calibrated spread (currency board proxy)
5. Output: `data/hk_macro_quarterly_real.csv` — 107 quarters (1998Q1–2024Q3)

**Limitation:** Spline interpolation smooths short-run variation. Official C&SD quarterly data recommended for final publication.

### Phase 7: FEVD and Historical Decomposition

Implemented two structural analysis functions:

- **`compute_fevd()`:** Forecast Error Variance Decomposition from orthogonalized IRFs
  - Formula: FEVD_{i,j}(h) = Σ_{s=0}^{h} θ_{ij,s}² / Σ_{s=0}^{h} Σ_k θ_{ik,s}²
  - Output: `output/07_fevd.png`, `output/fevd_table.csv`

- **`compute_historical_decomposition()`:** Decomposes each observed period into shock contributions
  - Formula: y_t = base_t + Σ_j Σ_{s=0}^{t} Θ_s · e_{j,t-s}
  - Output: `output/08_hist_decomp.png`

### Phase 8: Robustness Checks

- **Cholesky ordering permutations:** Tested 3 orderings (external-first, domestic-first, reversed). FEVD shares qualitatively robust.
- **Sub-sample stability:** Estimated on full sample, pre-GFC, post-GFC, ex-COVID. Post-GFC shows mild instability (max eigenvalue 1.09). Output: `output/09_ordering_robustness.png`, `output/10_subsample_stability.png`

### Phase 9: Unit Test Suite

60 tests in `tests/test_hk_var_model.py` covering:

| Test class | Count | Coverage |
|---|---|---|
| TestGenerateCalibratedData | 8 | Data shape, bounds, structural breaks |
| TestLoadLocalData | 2 | Error handling for bad CSV inputs |
| TestBuildLaggedDesign | 4 | Matrix dimensions, intercept, lag values |
| TestCompanionMatrix | 5 | Shape, identity block, stability |
| TestCholeskyIRF | 3 | Shape, impact = Cholesky factor, decay |
| TestBVARMinnesota | 9 | Type, shape, symmetry, PD, shrinkage, stability |
| TestStationarityTests | 3 | DataFrame output, all variables tested, valid decisions |
| TestApplyTransforms | 3 | Level preservation, diff length, last_level stored |
| TestInvertTransforms | 4 | Level no-change, diff cumulation, mixed, shape |
| TestShockInLevelSpace | 3 | Level direct, diff conversion, no mutation |
| TestSelectLagOrder | 3 | Positive lag, guardrail trigger, BIC vs AIC |
| TestJohansenCointegration | 2 | Skip with few I(1), run with two I(1) |
| TestForecastScenarios | 3 | Baseline shape, all keys, CI ordering |
| TestGrangerCausality | 1 | Returns list with expected fields |
| TestFEVD | 4 | Shape, sums to 1, non-negative, own-shock dominant |
| TestHistoricalDecomposition | 3 | Dict keys, contributions shape, shocks shape |

**Result:** 59 passed, 1 skipped (guardrail test skips when AIC picks lag=1)

### Phase 10: LaTeX Paper Draft

Full paper in `paper/main.tex` (~380 lines):
- Title: "External Shock Propagation to Hong Kong Under the Currency Board: A VAR Analysis of US Monetary Policy and China Growth Spillovers"
- Sections: Abstract, Introduction, Literature Review, Data, Econometric Framework, Results, Robustness, Conclusion
- JEL codes: E32, E52, F41, F42
- Bibliography: `paper/references.bib`

### Phase 11: Econometric Evaluation

Full evaluation in `output/econometric_evaluation.txt` using `econ-answering` and `econometrics-modeling` skills:

**Strengths:**
- Correct pipeline: stationarity → cointegration → lag selection → estimation → FEVD → historical decomp → backtest
- 16 mathematical audit issues identified and fixed across 2 rounds
- 60 unit tests passing
- Both VAR and BVAR compared
- Robustness across 3 Cholesky orderings and 4 sub-samples

**Weaknesses:**
- Interpolated annual data (biggest issue for publication)
- HIBOR proxy inflates US FFR → HIBOR channel by construction
- Cointegration present but not modelled (should use VECM)
- Residual autocorrelation in 3 of 6 equations
- No structural identification beyond Cholesky

**Grade: B+** — strong execution, data limitations prevent A.

### Phase 12: Auto-Run Rule

Created `.cursor/rules/hk-var-auto-run.mdc` to automatically run:
1. VAR pipeline (`--lag-criterion bic --model-type var`) after `hk_var_model.py` changes
2. pytest suite after model or test file changes
3. LaTeX compilation after paper file changes

---

## 3. File Map

```
Hong Kong/
├── hk_var_model.py                    # Main model (1592 lines)
├── tests/
│   ├── __init__.py
│   └── test_hk_var_model.py           # 60 tests (59 pass, 1 skip)
├── data/
│   ├── hk_macro_quarterly.csv         # Working dataset (copied from real or synthetic)
│   └── hk_macro_quarterly_real.csv    # Real data: WB annual→quarterly spline + FRED FFR
├── output/
│   ├── 01_raw_data.png                # Panel chart of 6 variables
│   ├── 02_correlation.png             # Correlation heatmap
│   ├── 03_stability.png               # Eigenvalue unit circle plot
│   ├── 04_irf.png                     # 6×6 Cholesky IRF grid
│   ├── 05_backtest_h1.png             # RMSE comparison h=1
│   ├── 05_backtest_h4.png             # RMSE comparison h=4
│   ├── 06_scenario_forecast.png       # Scenario fan charts
│   ├── 07_fevd.png                    # FEVD stacked area charts
│   ├── 08_hist_decomp.png             # Historical decomposition bars
│   ├── 09_ordering_robustness.png     # Cholesky ordering sensitivity
│   ├── 10_subsample_stability.png     # Sub-sample coefficient norms
│   ├── fevd_table.csv                 # FEVD numeric table
│   ├── forecast_scenarios.csv         # Forecast values (level space)
│   ├── data_dictionary.csv            # Variable metadata
│   ├── model_diagnostics.txt          # Lag selection + transforms
│   ├── methods_note.txt               # Full methods note
│   ├── model_review_audit.txt         # Audit round 1 (12 issues)
│   ├── model_review_audit_v2.txt      # Audit round 2 (4 issues)
│   ├── academic_assessment.txt        # Academic mentor evaluation
│   └── econometric_evaluation.txt     # Econometrics skill evaluation
├── paper/
│   ├── main.tex                       # LaTeX paper draft
│   ├── references.bib                 # BibTeX references
│   ├── main.pdf                       # Compiled PDF
│   └── (aux/log/bbl/blg/out/toc)     # LaTeX build artifacts
├── IMPLEMENTATION_PLAN.md             # 4-phase plan document
├── AGENTS.md                          # This file
├── README.md                          # Quick-start guide
├── requirements.txt                   # Python dependencies
└── .cursor/rules/
    └── hk-var-auto-run.mdc            # Auto-run rule for pipeline/tests/LaTeX
```

---

## 4. Econometric Framework Summary

### Model

```
y_t = c + A_1 y_{t-1} + A_2 y_{t-2} + A_3 y_{t-3} + u_t
```

where y_t = [us_ffr, china_gdp, gdp_growth, cpi_inflation, unemployment, hibor_3m]'

### Identification

- **Strategy:** Recursive (Cholesky) identification with external-first ordering
- **Assumption:** US FFR and China GDP do not respond contemporaneously to HK domestic shocks (small open economy assumption)
- **Ordering:** [us_ffr, china_gdp, gdp_growth, cpi_inflation, unemployment, hibor_3m]

### Stationarity

- **Tests:** Dual ADF + KPSS
- **Decision tree:** Both agree stationary → level; both agree unit root → first-diff; conflict → default level
- **Result:** china_gdp, cpi_inflation, unemployment differenced; rest in levels

### Lag Selection

- **Criteria:** AIC and BIC; BIC preferred (more parsimonious)
- **Guardrail:** params_per_equation / n_obs < 0.80 threshold
- **Result:** BIC selects p=3

### Structural Analysis

- **IRFs:** Θ_h = (J · F^h · J') · P, where P = chol(Σ_u)
- **FEVD:** FEVD_{i,j}(h) = Σ_{s=0}^{h} θ²_{ij,s} / Σ_{s=0}^{h} Σ_k θ²_{ik,s}
- **Historical decomposition:** y_t = base + Σ_j Σ_{s=0}^{t} Θ_s · e_{j,t-s}

### Forecast Evaluation

- Expanding-window out-of-sample at h=1Q and h=4Q
- Benchmarks: AR(1), Random Walk
- Metric: RMSE and MAE

---

## 5. Data Sources and Transforms

| Variable | Source | Raw Frequency | Transform to Quarterly | Final Transform |
|---|---|---|---|---|
| us_ffr | FRED (FEDFUNDS) | Monthly | Quarterly mean | Level |
| china_gdp | World Bank (NY.GDP.MKTP.KD.ZG) | Annual | Cubic spline interpolation | First diff |
| gdp_growth | World Bank (NY.GDP.MKTP.KD.ZG, HK) | Annual | Cubic spline interpolation | Level |
| cpi_inflation | World Bank (FP.CPI.TOTL.ZG, HK) | Annual | Cubic spline interpolation | First diff |
| unemployment | World Bank (SL.UEM.TOTL.ZS, HK) | Annual | Cubic spline interpolation | First diff |
| hibor_3m | Derived: FFR + calibrated spread | — | — | Level |

**Sample:** 1998Q1–2024Q3 (107 quarters raw, 106 after transforms)

**Known limitation:** Cubic spline interpolation smooths genuine quarterly variation. For publication, use official C&SD/HKMA quarterly releases.

---

## 6. Known Limitations and Future Work

### Limitations

1. **Interpolated data:** Annual → quarterly via cubic spline smooths short-run dynamics
2. **HIBOR proxy:** FFR + spread mechanically inflates the us_ffr → hibor_3m FEVD share
3. **Cointegration ignored:** Johansen detects 1 cointegrating relationship among I(1) variables; current model differences away this long-run information instead of using VECM
4. **Residual autocorrelation:** 3 of 6 equations show significant Ljung-Box at lag=8
5. **No structural identification beyond Cholesky:** Sign restrictions or external instruments would strengthen causal claims
6. **Bootstrap:** Residual-only; does not account for parameter uncertainty
7. **Post-GFC sub-sample instability:** Max eigenvalue 1.09 suggests borderline instability

### Recommended Next Steps

1. **Replace interpolated data** with official C&SD quarterly GDP/CPI/unemployment and HKMA HIBOR
2. **Implement VECM** as an alternative for long-horizon forecasts given cointegration
3. **Add sign restrictions** or external instrument identification
4. **Time-varying parameter VAR** (TVP-VAR) to handle structural breaks formally
5. **Factor-augmented VAR (FAVAR)** to incorporate richer information sets
6. **Wild bootstrap** for heteroskedasticity-robust confidence intervals

---

## 7. How to Reproduce

```bash
# Install dependencies
pip install -r requirements.txt

# Run the full pipeline (BIC lag selection, VAR model)
python hk_var_model.py --lag-criterion bic --model-type var

# Run with BVAR instead
python hk_var_model.py --lag-criterion bic --model-type bvar --bvar-lambda1 0.2

# Run tests
python -m pytest tests/ -v

# Compile paper (requires LaTeX distribution)
cd paper && latexmk -pdf main.tex
```

### CLI Arguments

| Argument | Default | Description |
|---|---|---|
| `--lag-criterion` | `aic` | Lag selection criterion: `aic` or `bic` |
| `--max-lags` | `8` | Maximum lags to consider |
| `--max-params-ratio` | `0.8` | Guardrail: max params/obs ratio |
| `--model-type` | `auto` | `var`, `bvar`, or `auto` |
| `--bvar-lambda1` | `0.2` | Minnesota prior overall tightness |
| `--auto-bvar-threshold` | `0.18` | Params ratio above which auto switches to BVAR |
| `--no-local-real-data` | `false` | Skip loading `data/hk_macro_quarterly_real.csv` |
| `--cholesky-order` | external-first | Comma-separated variable ordering |

---

## 8. Dependencies

- Python 3.10+
- numpy
- pandas
- matplotlib
- statsmodels
- scipy
- pytest (dev)

---

## 9. Audit Trail

| Date | Event | Details |
|---|---|---|
| Mar 2026 | Project inception | Chose VAR model for HK macro forecasting |
| Mar 2026 | Core pipeline built | 1200-line Python script with data→diagnostics→estimation→backtest→scenarios |
| Mar 2026 | Bug fixes (3) | statsmodels API compat, f-string syntax, matplotlib config |
| Mar 2026 | Audit round 1 | 12 issues found (1C, 4H, 4M, 3L) — all fixed |
| Mar 2026 | Audit round 2 | 4 issues found (2M, 2L) — all fixed |
| Mar 2026 | Academic assessment | "Strong tool, needs research question + FEVD + HD" |
| Mar 2026 | Research question adopted | External shock propagation under currency board |
| Mar 2026 | Real data ingestion | WB annual + FRED FFR → cubic spline quarterly |
| Mar 2026 | FEVD + historical decomp | Structural analysis answering the research question |
| Mar 2026 | Robustness checks | 3 Cholesky orderings + 4 sub-samples |
| Mar 2026 | Unit tests | 60 tests written, 59 pass |
| Mar 2026 | LaTeX paper draft | Full paper with abstract, lit review, results, robustness |
| Mar 2026 | Econometric evaluation | B+ grade; data limitations prevent A |
| Mar 2026 | Auto-run rule | Pipeline/test/LaTeX auto-execution on file changes |
| Mar 2026 | AGENTS.md + git init | Final documentation and version control |
| Mar 2026 | **Real data upgrade** | 5/6 vars from official sources (C&SD, HKMA, FRED). Only CPI still interpolated. 103 quarterly obs 1998Q1-2023Q3 |
| Mar 2026 | **VECM implementation** | Vector Error Correction Model with Johansen cointegration (rank 3-4). VECM reveals US channel 2-3x stronger than Cholesky VAR |
| Mar 2026 | **Sign restrictions** | Theory-consistent sign identification (US monetary tightening, China growth shock). 80/5000 accepted draws |
| Mar 2026 | **TVP-VAR** | Kalman filter with forgetting factor lambda=0.99. Shows deepening China coefficient post-GFC |
| Mar 2026 | **Paper revision v2** | Complete rewrite with VECM, sign restrictions, TVP-VAR results. Targeting Pacific Economic Review / J. Asian Economics |
