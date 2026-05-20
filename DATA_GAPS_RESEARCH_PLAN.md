# Current Data and Research Gaps

Research question:

> How do US monetary policy shocks and China growth shocks transmit to Hong Kong's real economy under the currency board?

## What Claude Added

| Addition | Status | Use now? |
|---|---|---|
| China real GDP growth | Integrated in canonical `china_gdp` column when OECD succeeds | Yes, but verify metadata |
| HK exports to Mainland China YoY | Integrated as `hk_exports_china_yoy` | Yes |
| HK property price data | Official RVD All Classes index is now fetched, quarterly, and merged into a model-ready sidecar | See `CLAUDE.md` for active use |
| US monetary-policy shock data | Available as sidecar through 2019Q4 | Optional, not baseline |

## Current Baseline

The baseline is now a **7-variable quarterly VAR**, not the old 6-variable setup.

| Variable | Research role | Status |
|---|---|---|
| `us_ffr` | US monetary conditions | Usable baseline shock proxy |
| `china_gdp` | China real activity in current data | Usable if OECD source verified |
| `hk_exports_china_yoy` | China-to-HK trade channel | Strong addition |
| `gdp_growth` | HK real economy outcome | Good |
| `cpi_inflation` | Price outcome | Good |
| `unemployment` | Labor-market outcome | Good |
| `hibor_3m` | Currency-board interest-rate channel | Good |

## Main Problems Still Left

1. **China source naming is fragile.**
   - Code still calls the column `china_gdp`.
   - Current metadata says OECD real GDP YoY.
   - If the OECD pull fails later, the fetcher falls back to FRED nominal GDP.
   - Practical fix: before writing claims, check `data/source_metadata.json`; if using OECD, call it China real GDP growth; if fallback, call it China nominal activity.

2. **Residual autocorrelation remains.**
   - BIC chooses VAR(1), but Ljung-Box rejects for `us_ffr`, `china_gdp`, `hk_exports_china_yoy`, `gdp_growth`, and `cpi_inflation`.
   - Practical fix: see `CLAUDE.md` for the active model hierarchy; if making stronger claims, report BVAR/AIC-lag or VAR(2) robustness.

3. **VECM is interesting but sensitive.**
   - Johansen trace rank is 2 on the I(1) subset.
   - VECM improves many level-space forecast RMSEs, but rank and deterministic choices matter.
   - Practical fix: follow `CLAUDE.md`, report rank sensitivity, and compare against simpler alternatives.

4. **US FFR is not a pure monetary surprise.**
   - It is a monetary-conditions variable.
   - A cleaner shock file exists (`data/us_mp_shock_quarterly.csv`), but it ends in 2019Q4.
   - Practical fix: keep FFR for full-sample baseline; use the shock file only for a shorter-sample robustness check.

5. **Property prices are economically important, but need a clear role.**
   - Hong Kong is property-heavy, so property prices are a serious transmission channel candidate.
   - The official RVD All Classes index is available in `data/hk_property_price_rvd_quarterly.csv`.
   - The merged model-ready file is `data/hk_macro_quarterly_property_model.csv`.
   - Practical fix: treat property prices as an asset-price transmission channel under the same topic; see `CLAUDE.md` for the active model role.

## Best Simple Plan

Use `CLAUDE.md` as the active plan. This file should not duplicate the final model hierarchy.

## Topic Discipline

The topic is still:

> How do US monetary policy shocks and China growth shocks transmit to Hong Kong's real economy under the currency board?

Property prices do not replace the topic. They enter as a Hong Kong asset-price transmission channel that can sit between external shocks, domestic financial conditions, and real-economy outcomes.

## Bottom Line

The old biggest data gap is mostly fixed: the project now has China real activity, an HK-China trade channel, and official property prices. Use `CLAUDE.md` for the current closeout plan and keep the claims reduced-form and cautious.
