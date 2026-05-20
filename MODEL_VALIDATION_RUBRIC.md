# Model Validation Rubric (Portfolio Build)

Date: 2026-05-15  
Scope: 48-96h modeling sprint, macro-econometric side project (not journal paper)

## 1) Objective and Model Hierarchy

Primary question:

> How do US monetary conditions and China activity transmit to Hong Kong under the currency board?

Pre-committed hierarchy for this sprint:

1. **Headline model**: full-system property-channel VECM
2. **Benchmark**: 7-variable VAR
3. **Robustness**: one-pass BVAR (shrinkage check)

Dropped for this sprint:

- Logistic/AUC downturn layer

## 2) Pre-Committed Specifications

### Headline VECM

- Command: `MPLCONFIGDIR=/tmp/mpl_cfg python hk_var_model.py --include-property --model-type vecm --lag-criterion bic`
- Deterministic term: `ci` (headline)
- Cointegration rank: Johansen trace @95% auto-selected rank
- Lag differences: `lag_diff = max(selected_VAR_lag - 1, 1)` (default)

### Required Sensitivity Grid

Run and report at least:

1. `deterministic in {ci, co}`
2. `lag_diff in {1, 2}` (if feasible given sample size)
3. `rank in {r, r+1}` where `r` is trace@95% rank (bounded by feasible system size)

### Benchmark / Robustness

1. VAR benchmark with BIC lag selection
2. BVAR with one fixed lambda (`--bvar-lambda1 0.2`)

## 3) Pass/Fail Gates

## Gate A: Data Provenance (must pass)

1. `data/source_metadata.json` must explicitly state `china_gdp` source.
2. If China source falls back to nominal FRED, all interpretation text must say **nominal activity proxy**.
3. No missing values in final estimation panel.

Failure action:

- Freeze claims, relabel interpretation, rerun before comparing models.

## Gate B: Claim Discipline (must pass)

Allowed language:

- reduced-form transmission
- dynamic association
- forecast-error shares

Not allowed:

- clean causal monetary shock identification

Failure action:

- Rewrite claims before any publish/export step.

## Gate C: Residual Diagnostics (graded)

Use Ljung-Box p-values at lag 8 from `output/vecm_diagnostics.txt`.

1. **Pass**: at most 4 equations reject at 5%, and `us_ffr` + `hibor_3m` do not reject.
2. **Warning**: more than 4 equations reject OR one of `us_ffr`/`hibor_3m` rejects.

Warning action:

- Run sensitivity with higher `lag_diff` and alternate deterministic term; downgrade confidence if unchanged.

## Gate D: Structural Coherence (must pass)

1. Johansen rank should be stable enough across confidence levels (no extreme jumps).
2. Impulse directions should be economically coherent in early horizons:
   - US tightening shock should not lower HIBOR on impact.
   - China activity shock should not imply immediate collapse in HK China-facing exports absent offsetting justification.

Failure action:

- Demote VECM from headline to sensitivity model for this cycle.

## Gate E: Forecast Comparison (must pass for VECM headline)

From `output/var_vecm_backtest_comparison.csv`, VECM should outperform VAR in RMSE on at least two of:

1. `us_ffr`
2. `hibor_3m`
3. `china_gdp`

Failure action:

- Keep VECM for interpretation, but switch headline to VAR for portfolio narrative.

## 4) Time-Gated Kill Criteria

## T+24h checkpoint

If both conditions hold:

1. Gate C is Warning, and
2. Gate E fails,

Then force fallback:

- **Fallback headline**: VAR
- **VECM role**: sensitivity appendix/check

## T+48h checkpoint

If sensitivity grid still unstable (rank/deterministic materially flips key conclusions), lock final message to:

- channel-consistent findings only
- uncertainty-first interpretation
- explicit limitation bullets

## 5) Minimum Portfolio Deliverables

1. One model comparison table (VECM vs VAR vs BVAR; FEVD + RMSE highlights)
2. Two readable figures (IRF panel + FEVD panel)
3. One limitations section with:
   - residual autocorrelation
   - VECM specification sensitivity
   - `us_ffr` as monetary-conditions proxy
