# HK VAR Independent Audit

Date: 2026-03-30
Scope: Full post-implementation audit of data pipeline, model code, outputs, and paper consistency.

## 1) Objective

Provide an independent, evidence-based audit after recent plan execution so the next iteration can focus on the highest-impact improvements.

## 2) What Was Done (Process Log)

1. Reviewed implemented changes across:
   - `fetch_real_data.py`
   - `hk_var_model.py`
   - `hk_var/scenario_utils.py`
   - `paper/main.tex`
   - `pytest.ini`
   - refreshed data/output artifacts
2. Ran code-centric review and math/econ review with independent reviewer profiles.
3. Re-ran full verification suite on current workspace:
   - unit tests
   - full model pipeline (VAR, BIC)
   - full LaTeX compilation chain
4. Compared committed snapshot outputs against fresh regenerated outputs.

## 3) Verification Evidence

## 3.1 Commands Executed

- `MPLCONFIGDIR=/tmp/mpl_cfg python -m pytest tests/test_hk_var_model.py -q --tb=short`
- `MPLCONFIGDIR=/tmp/mpl_cfg python hk_var_model.py --lag-criterion bic --model-type var`
- `cd paper && pdflatex -interaction=nonstopmode main.tex && bibtex main && pdflatex -interaction=nonstopmode main.tex && pdflatex -interaction=nonstopmode main.tex`

## 3.2 Results

- Tests: `70 passed, 1 skipped`
- Pipeline: successful end-to-end run with local real data (`103` quarters, ending `2023-07-01`)
- Paper build: successful PDF compile (with minor overfull-box warnings)

## 3.3 Reproducibility Check Outcome

- Fresh run produced `output/forecast_scenarios.csv` starting at `2023-10-01` (consistent with `data/hk_macro_quarterly_real.csv` ending `2023-07-01`).
- Current committed snapshot previously contained forecasts starting `2026-01-01`.
- Therefore: committed outputs and reproducible outputs were inconsistent; a fresh rerun resolves to 2023-start forecasts.

## 4) Findings (Code + Interpretation)

### High

1. Snapshot reproducibility inconsistency
   - Symptom: committed output tables/charts did not match fresh run from committed data.
   - Impact: replication confusion for reviewers and future you.
   - Evidence: committed `forecast_scenarios.csv` had 2026 starts; fresh run has 2023-10 starts.

2. Scenario conditioning for differenced variables is mathematically ambiguous
   - Code uses level gap mapping for differenced variables in `hk_var/scenario_utils.py`.
   - Risk: stated level scenario at quarter `T` may not equal the actual implied transformed state unless carefully defined.
   - Impact: scenario interpretation may be off in paper and policy narrative.

### Medium

3. Cointegration rank selection is computed on I(1) subset, then used in full-system VECM
   - Risk: rank logic and estimated system are not perfectly aligned.
   - Impact: long-run interpretation can be challenged by referees.

4. CPI series still dominated by fallback history
   - Official CPI share is improved and documented but still limited (metadata currently reports ~21% official share).
   - Impact: inference for CPI dynamics remains sensitive to splice design.

5. Residual diagnostics still flag at least one equation
   - Example from current run: Ljung-Box p-value for `china_gdp` equation indicates autocorrelation.
   - Impact: standard errors / impulse interpretation should be presented with caution.

### Low

6. Public API change in `fetch_hk_cpi()` return signature (2-tuple -> 3-tuple)
   - Internal caller updated, but external scripts may break.

7. Minor LaTeX layout warnings
   - Overfull hbox warnings remain but do not block build.

## 5) Completed Improvements (from current implementation)

- Added CPI lineage artifact: `data/cpi_lineage.csv`
- Enhanced data metadata in `data/source_metadata.json`
- Improved semantics to "China nominal GDP growth" across code/paper
- Added pytest warning filters in `pytest.ini`
- Extracted scenario utilities to `hk_var/scenario_utils.py`
- Added scenario mapping explanation to methods output and paper

## 6) Priority Next Steps

### P0 (Do Immediately)

1. Reconcile and commit reproducible output snapshots
   - Action: decide canonical dataset; regenerate all output artifacts from it; commit as one snapshot.
   - Acceptance: no date-window mismatch between `data/hk_macro_quarterly_real.csv` and `output/forecast_scenarios.csv`.

2. Lock scenario mapping definition
   - Action: choose one of:
     - true level-target conditioning in transformed system, or
     - transformed-shock interpretation with explicit wording.
   - Acceptance: equation in paper and implementation in `hk_var/scenario_utils.py` are identical in meaning.

### P1 (High Value)

3. Align rank-selection and VECM estimation domain
   - Action: either estimate rank on the full modeled system or justify/document subset-to-full transfer rule.
   - Acceptance: methods section and code use a single coherent rank-selection story.

4. CPI splice robustness
   - Action: add one robustness check around splice seam (pre/post splice sensitivity).
   - Acceptance: robustness note/table in paper appendix.

### P2 (Polish)

5. Stabilize residual diagnostics
   - Action: test lag/deterministic alternatives where autocorrelation remains.
6. Add compatibility wrapper or migration note for `fetch_hk_cpi()` signature.
7. Clean overfull hbox warnings in paper.

## 7) Suggested Execution Order (Next Cycle)

1. Snapshot reconciliation commit (P0.1)
2. Scenario math-text alignment fix (P0.2)
3. VECM rank-domain alignment (P1.3)
4. CPI seam robustness note (P1.4)
5. Remaining polish (P2)

## 8) Current Workspace Note

After this verification run, local uncommitted changes exist in regenerated artifacts:
- `output/06_scenario_forecast.png`
- `output/forecast_scenarios.csv`
- `output/var_vecm_backtest_comparison.csv`
- `paper/main.pdf`

These reflect fresh reproducible outputs and should be either committed as the new canonical snapshot or intentionally discarded with a documented reason.
