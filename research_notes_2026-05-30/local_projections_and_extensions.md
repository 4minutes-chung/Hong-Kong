# Local Projections and Project Extensions

Date: 2026-05-30

Scope: how to use local projections (LPs) as an IRF robustness check for the Hong Kong BVAR project, plus how to extend the LP framework to ZLB/asymmetry tests.

## 1. What Local Projections Estimate

Jordà local projections estimate an impulse response one horizon at a time:

```text
y_{r,t+h} = alpha_h + beta_h shock_{j,t} + Gamma_h' controls_t + u_{t+h}
```

The coefficient `beta_h` is the response of variable `r` at horizon `h` to shock `j`.

Unlike a VAR IRF, LP does not estimate one full dynamic system and iterate it forward. It runs one regression per horizon. That makes it flexible and easy to adapt to nonlinear/state-dependent questions, but it also costs precision.

## 2. What the Literature Says

Use LP as robustness, not as a replacement for the BVAR baseline.

Key points:

- Jordà (2005) introduced LPs as a way to estimate impulse responses without specifying the whole multivariate dynamic system.
- Plagborg-Moller and Wolf (2021) show that LPs and VARs estimate the same population impulse responses under unrestricted lag structures; the difference is finite-sample behavior.
- Li, Plagborg-Moller, and Wolf (2022/2024) find a bias-variance tradeoff: LP has lower bias but higher variance at intermediate and long horizons; shrinkage BVARs are attractive when precision matters.
- Barnichon and Brownlees (2019) propose smooth LPs to reduce the wiggliness/high variance of standard LP estimates.

Project implication:

```text
BVAR(4) remains the baseline because the sample is small and precision matters. LP-IRFs are a robustness appendix designed to show that the two headline channels do not depend entirely on the BVAR's parametric dynamics.
```

## 3. Channels to Estimate

Run LPs only on the two headline channels first:

1. `hibor_3m` shock -> `hk_property_price_qoq` response.
2. `hk_exports_china_yoy` shock -> `gdp_growth` response.

Optional third channel:

3. `gdp_growth` shock -> `cpi_inflation` response.

Do not run a full 6x6 LP grid initially. It will create noise, multiple-testing clutter, and hard-to-explain figures.

## 4. Horizon Indexing

Use horizons:

```text
h = 0, 1, ..., 8
```

For comparison with Alexandria and statsmodels IRFs:

- `h = 0`: impact quarter.
- `h = 1`: one quarter after shock.
- `h = 2`: two quarters after shock.

The current project headline often discusses `h = 2`, so the LP figure should label horizons clearly.

## 5. Identification: Mapping Cholesky to LP

A LP regression still needs a shock definition. It is not identification-free.

To mimic the current recursive BVAR ordering:

```text
hibor_3m -> hk_exports_china_yoy -> gdp_growth -> cpi_inflation -> unemployment -> hk_property_price_qoq
```

use this rule:

```text
For an impulse variable x_j, control contemporaneously for variables ordered before x_j, and do not control contemporaneously for variables ordered after x_j. Always control for lags of the full endogenous block.
```

### HIBOR -> Property

HIBOR is ordered first. There are no contemporaneous preceding endogenous controls.

Suggested first-stage shock:

```text
hibor_3m_t = a + lags(Y_t, 1..4) + us_ffr_t + china_gdp_t + e_hibor_t
shock_hibor_t = e_hibor_t / sd(e_hibor_t)
```

LP response equation:

```text
property_qoq_{t+h} = alpha_h
                    + beta_h shock_hibor_t
                    + lags(Y_t, 1..4)
                    + us_ffr_t + china_gdp_t
                    + u_{t+h}
```

This produces a one-standard-deviation HIBOR innovation response.

### Exports -> GDP

Exports are ordered after HIBOR and before GDP. Control contemporaneously for HIBOR.

Suggested first-stage shock:

```text
exports_t = a + kappa * hibor_3m_t
              + lags(Y_t, 1..4)
              + us_ffr_t + china_gdp_t
              + e_exports_t
shock_exports_t = e_exports_t / sd(e_exports_t)
```

LP response equation:

```text
gdp_growth_{t+h} = alpha_h
                  + beta_h shock_exports_t
                  + lambda * hibor_3m_t
                  + lags(Y_t, 1..4)
                  + us_ffr_t + china_gdp_t
                  + u_{t+h}
```

This aligns the LP with the recursive structural interpretation.

## 6. Inference

LP residuals are serially correlated because the dependent variable overlaps across horizons. Use HAC/Newey-West standard errors.

Practical setting:

```text
cov_type = "HAC"
maxlags = max(4, h)
```

For small samples, use 90% bands to match the BVAR figures. Report that the LP bands are HAC-robust.

If the LP bands are much wider than BVAR bands, that is expected. It is not automatic evidence against the BVAR. The finite-sample literature predicts higher LP variance.

## 7. Baseline LP Implementation Skeleton

This is a future notebook pattern, not run in this research pass:

```python
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.regression.linear_model import OLS

def add_lags(df, cols, max_lag):
    out = []
    for lag in range(1, max_lag + 1):
        lagged = df[cols].shift(lag).add_suffix(f"_L{lag}")
        out.append(lagged)
    return pd.concat(out, axis=1)

Y_cols = [
    "hibor_3m",
    "hk_exports_china_yoy",
    "gdp_growth",
    "cpi_inflation",
    "unemployment",
    "hk_property_price_qoq",
]
X_cols = ["us_ffr", "china_gdp"]

L = add_lags(df, Y_cols, 4)

# Example: HIBOR innovation
X_first = sm.add_constant(pd.concat([L, df[X_cols]], axis=1))
y_first = df["hibor_3m"]
mask = y_first.notna() & X_first.notna().all(axis=1)
first = OLS(y_first[mask], X_first[mask]).fit()
shock = first.resid / first.resid.std()

rows = []
for h in range(0, 9):
    y = df["hk_property_price_qoq"].shift(-h)
    X = sm.add_constant(pd.concat([shock.rename("shock"), L, df[X_cols]], axis=1))
    mask = y.notna() & X.notna().all(axis=1)
    res = OLS(y[mask], X[mask]).fit(cov_type="HAC", cov_kwds={"maxlags": max(4, h)})
    ci = res.conf_int(alpha=0.10).loc["shock"]
    rows.append({
        "h": h,
        "beta": res.params["shock"],
        "lo90": ci.iloc[0],
        "hi90": ci.iloc[1],
        "n": int(mask.sum()),
    })

lp_irf = pd.DataFrame(rows)
```

## 8. Interpreting LP Outcomes

### Strong Confirmation

LP median response has the same sign as BVAR and 90% bands exclude zero near the key horizon.

Paper wording:

```text
Local-projection IRFs using the same recursive shock ordering produce responses with the same sign and timing as the BVAR(4), confirming that the headline channels are not an artifact of iterating the Bayesian VAR dynamics.
```

### Partial Confirmation

LP median has same sign, but bands cross zero.

Paper wording:

```text
Local-projection estimates are directionally consistent with the BVAR but less precise, as expected in a 108-observation quarterly sample. The LP exercise therefore supports the sign pattern but not independent horizon-specific significance.
```

### Disagreement

LP median has opposite sign near key horizons.

Action:

- Check horizon indexing.
- Check shock scaling.
- Check contemporaneous controls matching recursive ordering.
- Check whether the LP is using levels, leads, or cumulative changes differently from the BVAR IRF.
- Check influential crisis observations.

Do not immediately discard BVAR. First determine whether the LP is estimating the same estimand.

## 9. Structural Breaks and LP

LPs help because each horizon is estimated separately. A break around 2020 contaminates only observations where `t+h` crosses the break window, rather than forcing one VAR coefficient matrix to average the whole regime.

Still, LP does not make breaks disappear. Recommended sensitivity:

- Baseline LP with HAC bands.
- LP excluding 2020Q1-2021Q2.
- LP with GFC/COVID pulse dummies.
- Compare medians and bands.

Keep the appendix focused. The point is robustness, not a new paper inside the paper.

## 10. ZLB / ZIRP Asymmetry Extension

Research question:

```text
Does HIBOR -> property transmission weaken or strengthen during near-zero US rate regimes?
```

Define:

```text
ZIRP_t = 1 if us_ffr_t <= 0.25, else 0
```

State-dependent LP:

```text
property_qoq_{t+h} =
    alpha_h
  + beta_normal_h * shock_hibor_t * (1 - ZIRP_t)
  + beta_zirp_h   * shock_hibor_t * ZIRP_t
  + phi_h * ZIRP_t
  + controls_t
  + u_{t+h}
```

Test:

```text
H0: beta_normal_h = beta_zirp_h
```

Interpretation:

- `beta_zirp_h` closer to zero: HIBOR-property pass-through weakens at the lower bound.
- `beta_zirp_h` more negative: property prices are especially sensitive to rate shocks in ZIRP states.
- Wide bands: sample is too small for a strong asymmetry claim.

This is the cleanest way to study asymmetry because sub-sample BVARs are underpowered.

## 11. Smooth Local Projections

If standard LP estimates are too jagged, use smooth LP as a second-stage sensitivity. Barnichon and Brownlees (2019) show that smoothing can improve precision while preserving LP flexibility.

Recommendation:

- Do not start with smooth LP.
- Start with plain LP.
- If the median path is economically implausibly jagged, add smooth LP as a figure-cleaning robustness check.

## 12. What LP Cannot Do Here

LP does not replace:

- FEVD.
- Historical decomposition.
- Full multivariate forecast evaluation.
- The BVAR's shrinkage solution to the p=4 parameter problem.

LP answers one narrower question:

```text
Do the headline IRF signs and timing survive a horizon-by-horizon estimator?
```

That is enough for the appendix.

## 13. Source Map

Primary/official sources consulted:

- Jordà, O. (2005). "Estimation and Inference of Impulse Responses by Local Projections." American Economic Review. https://topcat.aeaweb.org/articles?id=10.1257%2F0002828053828518
- Plagborg-Moller, M., Wolf, C. K. (2021). "Local Projections and VARs Estimate the Same Impulse Responses." Econometrica. https://www3.nd.edu/~nmark/Climate/EconometricaPlagborgMollerSameImpulseResponses.pdf
- Li, D., Plagborg-Moller, M., Wolf, C. K. (2022). "Local Projections vs. VARs: Lessons From Thousands of DGPs." NBER Working Paper 30207. https://www.nber.org/papers/w30207
- Barnichon, R., Brownlees, C. (2019). "Impulse Response Estimation by Smooth Local Projections." Review of Economics and Statistics. https://www3.nd.edu/~nmark/Climate/BarnichonBrownless_ReStat2019.pdf

