# Project Decision Memo

Date: 2026-05-30

Purpose: concise project-facing synthesis from the BVAR/Minnesota/BVARX/local-projection research pass.

## 1. Main Decision

Keep BVAR(4) with Minnesota prior as the main model.

Reason:

- VARX(1) is too short for multi-quarter transmission.
- VARX(4) OLS is too high-variance for `T_eff ~= 108`.
- BVAR(4) solves the lag/variance tradeoff through shrinkage.
- Optimized `pi1 ~= 0.085` is genuine shrinkage, not a flat/OLS prior.
- Optimized `pi2 = 1.0` preserves cross-variable transmission channels.
- OOS conditional RMSE favors BVAR in 15/18 cells.
- Phase 9 structural-stability tests show BVAR residual mean breaks disappear for GDP/CPI/property, while HIBOR residual breaks map to Fed cycles.

## 2. What Changed From Earlier Understanding

### Delta Is Verified

The prior mean vector `delta` is optimized by Alexandria. It is not a universal random-walk prior.

Original-order optimized values:

```text
hk_exports_china_yoy       0.626900
gdp_growth                 0.544895
cpi_inflation              0.734662
unemployment               0.990883
hibor_3m                   0.442175
hk_property_price_qoq      0.417517
```

This removes a potential limitation from the paper. Do not write that the model imposes `delta_i = 1` for all variables.

### Pi4 Should Be Treated Carefully

`pi4 ~= 100` means the exogenous prior is diffuse. It does not mean the data strongly identified 100 as a meaningful value.

Write:

```text
The exogenous-coefficient prior is set to be diffuse (`pi4 ~= 100`), so the US FFR and China GDP coefficients are not materially constrained by the prior.
```

Do not write:

```text
The data validate pi4 = 100.
```

### OOS Forecasts Are Conditional

The OOS RMSE exercise uses realized future `us_ffr` and `china_gdp`. That is valid for comparing domestic dynamics conditional on foreign-anchor paths, but it is not a fully real-time unconditional forecast.

Write:

```text
In conditional expanding-window forecasts using realized foreign-anchor paths, the BVAR improves RMSE relative to VARX(1) in 15 of 18 variable-horizon cells.
```

## 3. Paper Methodology Paragraph

```text
We estimate a Bayesian VAR with four quarterly lags and two exogenous foreign-anchor variables: the US federal funds rate and China GDP growth. The four-lag structure captures multi-quarter macroeconomic propagation, while the Minnesota prior regularizes the otherwise over-parameterized VARX(4) system. Prior hyperparameters are selected by marginal likelihood. The selected prior has overall tightness `pi1 = 0.085`, no additional cross-variable shrinkage (`pi2 = 1.0`), harmonic lag decay (`pi3 = 1.0`), and a diffuse exogenous-coefficient prior (`pi4 ~= 100`). The own-lag prior means are optimized by series rather than fixed at a universal random-walk value. This specification allows the model to retain the cross-variable channels central to the research question while controlling small-sample overfitting.
```

## 4. Paper Identification Paragraph

```text
Structural impulse responses are identified recursively with HIBOR ordered first in the domestic block. Under Hong Kong's Linked Exchange Rate System, HIBOR is disciplined by US dollar funding conditions and the currency-board adjustment mechanism, and should not respond contemporaneously to domestic GDP or labor-market shocks. The recursive ordering is therefore `HIBOR -> exports -> GDP -> CPI -> unemployment -> property prices`.
```

## 5. FEVD Caveat

Use this exact caveat or close variant:

```text
Because US FFR and China GDP enter as exogenous regressors, FEVD shares are computed over the domestic endogenous shock block. Foreign-anchor effects transmitted through lagged HIBOR or exports therefore appear partly as HIBOR or exports own variance rather than as separate FFR or China shock shares.
```

This explains why HIBOR own-share can be high under LERS without contradicting the US-rate transmission story.

## 6. Local Projection Role

LP should be a robustness appendix, not the main model.

Run only:

1. HIBOR shock -> property prices.
2. Exports shock -> GDP growth.

Success criterion:

- Same sign and timing as BVAR.
- Preferably 90% HAC bands excluding zero near key horizons.
- If bands cross zero but medians match, report directional consistency and lower LP precision.

Suggested paper sentence if confirmed:

```text
Local-projection IRFs using the same recursive shock ordering deliver the same sign pattern as the BVAR(4), indicating that the headline responses are not solely an artifact of iterating the Bayesian VAR coefficient matrix.
```

## 7. ZLB / ZIRP Extension

Use threshold LP rather than sub-sample BVAR.

Reason:

- Sub-sample BVAR is underpowered.
- LP keeps the full sample.
- Interactions are easy to interpret.

Test:

```text
property_{t+h} = alpha_h
               + beta_normal_h * hibor_shock_t * (1 - ZIRP_t)
               + beta_zirp_h   * hibor_shock_t * ZIRP_t
               + controls_t
               + error_{t+h}
```

This is optional but promising. It is more novel than rerunning another BVAR variant.

## 8. Do Not Do

- Do not reopen the core BVAR unless a specific diagnostic fails.
- Do not run MCMC convergence diagnostics on strict Minnesota posterior draws.
- Do not claim VECM is needed; Johansen rank is 0 at 95%.
- Do not interpret HIBOR FEVD own-share as "HIBOR self-driven."
- Do not treat `pi4 ~= 100` as strong evidence; treat it as a diffuse-prior setting.
- Do not use old files that describe VECM as headline; `CLAUDE.md` supersedes them.

## 9. Next Best Work

1. Add Phase 9A/9B cells to `HK_BVAR_Project.ipynb` when editing is allowed.
2. Implement LP-IRF appendix on the two headline channels.
3. If LP confirms signs, write the paper.
4. If LP is directionally consistent but imprecise, still write the paper and frame LP as lower-power robustness.
5. If LP contradicts BVAR, debug shock construction and horizon indexing before changing the model.

## 10. Sources Used

- Litterman (1986), Federal Reserve Bank of Minneapolis / JBES: https://www.fedinprint.org/item/fedmwp/42678/original
- Doan, Litterman, Sims (1984), NBER: https://www.nber.org/papers/w1202
- Banbura, Giannone, Reichlin (2010), Journal of Applied Econometrics: https://ideas.repec.org/a/jae/japmet/v25y2010i1p71-92.html
- Giannone, Lenza, Primiceri (2015), Review of Economics and Statistics: https://econpapers.repec.org/paper/nbrnberwo/18467.htm
- Jordà (2005), American Economic Review: https://topcat.aeaweb.org/articles?id=10.1257%2F0002828053828518
- Plagborg-Moller and Wolf (2021), Econometrica: https://www3.nd.edu/~nmark/Climate/EconometricaPlagborgMollerSameImpulseResponses.pdf
- Li, Plagborg-Moller, Wolf (2022), NBER: https://www.nber.org/papers/w30207
- HKMA LERS overview: https://www.hkma.gov.hk/eng/key-functions/money/linked-exchange-rate-system/
- HKMA LERS mechanism: https://www.hkma.gov.hk/eng/key-functions/money/linked-exchange-rate-system/how-does-the-lers-work/
- HKMA RM 11/2018: https://www.hkma.gov.hk/media/eng/publication-and-research/research/research-memorandums/2018/RM11-2018.pdf

