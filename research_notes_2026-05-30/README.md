# Research Notes 2026-05-30

These notes document the BVAR, Minnesota prior, BVARX, local projection, and project-specific methodology learning requested on 2026-05-30.

No existing project files were edited for this research pass. The notes here are new files only.

## Read Order

1. `bvar_minnesota_bvarx_tuning.md`
   - Main technical reference.
   - Covers Minnesota prior mechanics, Alexandria implementation details, hyperparameter tuning, BVARX/exogenous-variable issues, and project-specific conclusions.

2. `local_projections_and_extensions.md`
   - Practical guide for Jordà local projections as an IRF robustness appendix.
   - Includes recursive-identification mapping, HAC inference, and ZLB/asymmetry extensions.

3. `project_decision_memo.md`
   - Shorter synthesis for paper writing.
   - Includes decisions, caveats, and paper-ready wording.

## Current Project Baseline

Active project memory is `CLAUDE.md`.

Final current baseline:

- Model: BVAR(4) with Minnesota prior and exogenous US/China block.
- Endogenous variables: `hk_exports_china_yoy`, `gdp_growth`, `cpi_inflation`, `unemployment`, `hibor_3m`, `hk_property_price_qoq`.
- Exogenous variables: `us_ffr`, `china_gdp`.
- Final optimized prior in original model order:
  - `pi1 = 0.084588`
  - `pi2 = 1.000000`
  - `pi3 = 1.000000`
  - `pi4 = 99.779011`
  - log10 marginal likelihood: `-528.979647`
- Optimized prior means, original order:
  - `hk_exports_china_yoy`: `delta = 0.626900`
  - `gdp_growth`: `delta = 0.544895`
  - `cpi_inflation`: `delta = 0.734662`
  - `unemployment`: `delta = 0.990883`
  - `hibor_3m`: `delta = 0.442175`
  - `hk_property_price_qoq`: `delta = 0.417517`

The `delta` vector was verified by an in-memory re-fit on 2026-05-30. The current model does not use a universal random-walk prior mean.

