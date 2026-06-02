# BVAR, Minnesota Prior, and BVARX Tuning

Date: 2026-05-30

Scope: project-specific reference for the Hong Kong external-shock transmission project. This note explains what the Minnesota prior is doing, how Alexandria implements it, how to tune it, and how to defend the BVARX specification with `us_ffr` and `china_gdp` as exogenous variables.

## 1. Project Specification

The active project model is a Bayesian VAR with exogenous regressors:

```text
Y_t = c + A_1 Y_{t-1} + ... + A_p Y_{t-p} + C X_t + epsilon_t
epsilon_t ~ N(0, Sigma)
```

Current baseline:

- `p = 4` quarterly lags.
- `T_eff = 108`.
- `n = 6` endogenous variables.
- `m = 2` exogenous variables.
- Endogenous block: Hong Kong exports to China, real GDP growth, CPI inflation, unemployment, 3-month HIBOR, property price QoQ growth.
- Exogenous block: US federal funds rate, China GDP growth.
- Estimator: `alexandria.MinnesotaBayesianVar`.
- Prior: strict Litterman/Minnesota form with fixed `Sigma`.

The basic problem is dimensionality. With 6 endogenous variables, 4 lags, 2 exogenous variables, and an intercept, there are:

```text
6*4 + 2 + 1 = 27 coefficients per equation
27*6 = 162 coefficients total
```

There are fewer effective observations than total coefficients. OLS VARX(4) can fit the sample but loses the trade-channel signal and inflates uncertainty. The Minnesota prior is the regularizer that makes the 4-lag model usable.

## 2. Why BVAR Here

The literature justification is tight:

- Litterman (1986) and Doan, Litterman, Sims (1984) introduced Bayesian VAR forecasting with realistic priors to stabilize over-parameterized macro VARs.
- Banbura, Giannone, Reichlin (2010) show that shrinkage should scale with model dimension and that shrinkage VARs can produce credible structural impulse responses.
- Giannone, Lenza, Primiceri (2015) justify treating prior tightness as a hyperparameter selected by marginal likelihood rather than by arbitrary convention.

For this project, that means:

- The move from VARX(1) to BVAR(4) is not a cosmetic robustness check. It solves the core small-sample lag problem.
- The 4-lag structure is economically needed because quarterly macro transmission is not one-quarter-only.
- The prior prevents VARX(4) from consuming all available degrees of freedom.

## 3. Alexandria's Minnesota Prior

Alexandria stores the prior as a diagonal Normal prior on the vectorized coefficient matrix:

```text
beta ~ N(b, V)
```

The prior mean `b` is:

```text
own first lag of variable i: delta_i
all other lag coefficients: 0
all exogenous coefficients: 0
```

Alexandria source verification:

- `make_b(delta, n, m, p)` stacks zeros for exogenous coefficients, `diag(delta)` for the first own lag, and zeros for higher lags.
- `make_V(s, pi1, pi2, pi3, pi4, n, m, p)` creates the diagonal prior variance vector.
- With `hyperparameter_optimization=True`, Alexandria optimizes `pi1`, `pi2`, `pi3`, `pi4`, and all `delta_i` by marginal likelihood.

For the coefficient in equation `i` on lag `ell` of endogenous variable `j`, the implemented prior variance is:

```text
Var(B_{i,j,ell}) = (s_i / s_j) * [pi1 * d_{ij} / ell^pi3]^2

d_{ij} = 1     if i = j
d_{ij} = pi2  if i != j
```

where `s_i` and `s_j` are univariate AR residual variances. Equivalently, if using residual standard deviations `sigma_i`, the scale term is `(sigma_i / sigma_j)^2`.

For exogenous coefficients:

```text
Var(C_{i,r}) = s_i * (pi1 * pi4)^2
```

This matters because the prior is scale-invariant across variables measured in different units.

## 4. Hyperparameter Meanings

### `pi1`: Overall Tightness

`pi1` is the global prior scale. Smaller `pi1` means tighter prior and less freedom for the data to move coefficients away from the prior mean.

Correct interpretation:

```text
pi1 -> 0        very tight prior, coefficients forced toward prior mean
pi1 large       diffuse prior, posterior approaches OLS
```

Project result:

```text
pi1 = 0.084588
```

This is genuine shrinkage, slightly tighter than the common 0.1 benchmark. It is not "almost OLS." The earlier p=3 optimizer result near `pi1 = 0.01` is a degeneracy signal: the optimizer hits the lower bound and forces the model toward the prior mean. Reject boundary solutions even if marginal likelihood improves.

### `pi2`: Cross-Variable Shrinkage

`pi2` controls whether lags of other variables are shrunk more heavily than own lags.

```text
pi2 = 0.5       conventional Minnesota default; cross-lag variance is 25% of own-lag variance after scale correction
pi2 = 1.0       no extra cross-variable shrinkage
```

Project result:

```text
pi2 = 1.000000
```

This is substantively important. The optimizer is saying that cross-variable dynamics are not noise in this dataset. That aligns with the project structure:

- `us_ffr -> hibor_3m` through LERS.
- `china_gdp -> hk_exports_china_yoy -> gdp_growth` through trade.
- `hibor_3m -> hk_property_price_qoq` through financing conditions.

Paper implication:

```text
The marginal-likelihood-selected prior imposes no additional shrinkage on cross-variable lags (`pi2 = 1.0`), consistent with the model's purpose of measuring external-shock transmission across variables.
```

Do not overclaim: `pi2 = 1.0` supports the need for cross-variable dynamics, but identification still comes from the recursive ordering and institutional assumptions.

### `pi3`: Lag Decay

`pi3` governs how rapidly prior variance shrinks at higher lags:

```text
lag factor = 1 / ell^pi3
```

Project result:

```text
pi3 = 1.000000
```

Alexandria constrains `pi3` to `[1, 5]` during optimization. A manual grid found some improvement around `pi3 = 0.3` to `0.5` when other parameters were fixed, but the full optimizer with `pi4` and `delta` free dominated the manual grid while staying at `pi3 = 1`. Keep `pi3 = 1` unless a new sensitivity exercise changes the full marginal-likelihood comparison.

### `pi4`: Exogenous Slackness

`pi4` controls the prior variance on exogenous coefficients. In this project:

```text
pi1 * pi4 ~= 0.0846 * 99.78 ~= 8.44
```

That is a very wide prior on `us_ffr` and `china_gdp` coefficients. It lets the data estimate the foreign-anchor effects.

Project result:

```text
pi4 = 99.779011
```

Interpretation:

- Correct: the exogenous prior is effectively diffuse.
- Incorrect: the optimizer "proved" `pi4 = 100` is true.

When `pi4` is already large, the marginal likelihood is likely flat in that direction. A value near 100 means the data do not object to a diffuse exogenous prior; it is not a deep empirical finding. If challenged, profile marginal likelihood over:

```text
pi4 in {1, 10, 20, 50, 100, 500}
```

If the curve is flat above 20, report that exogenous coefficients are not prior-constrained.

### `delta_i`: Prior Mean for Own First Lag

The most important new verification: Alexandria optimized the `delta` vector. The model does not use `delta_i = 1` universally.

Original-order in-memory re-fit on 2026-05-30:

| Variable | Optimized `delta_i` |
|---|---:|
| `hk_exports_china_yoy` | 0.626900 |
| `gdp_growth` | 0.544895 |
| `cpi_inflation` | 0.734662 |
| `unemployment` | 0.990883 |
| `hibor_3m` | 0.442175 |
| `hk_property_price_qoq` | 0.417517 |

This resolves the open question in Lesson 999. The prior mean is mixed-persistence, not pure random walk. That is good for this dataset because most modeled variables are stationary growth rates or rates rather than log levels.

Do not compare `delta_i` mechanically to univariate AR(1). The optimized `delta_i` is the prior center for the first own lag in a VAR(4) with exogenous variables and scale-adjusted shrinkage. For example, HIBOR's univariate AR(1) is high, but once `us_ffr` and four HIBOR lags are in the system, the marginal-likelihood-optimal first-lag prior mean can be much lower.

Paper implication:

```text
The Minnesota prior means were optimized jointly with the shrinkage hyperparameters, allowing series-specific persistence rather than imposing a universal random-walk prior mean.
```

## 5. Marginal Likelihood Tuning Protocol

Use this protocol for any future BVAR re-estimation.

### Step 1: Fix the Economic Variable Set

Do not let tuning decide the research question. The endogenous/exogenous split should come first:

- US FFR and China GDP are foreign anchors.
- Hong Kong cannot move US monetary policy or China growth within the quarter.
- Hong Kong variables are domestic transmission outcomes.

### Step 2: Compare Lag Lengths With Hyperparameters Optimized

For each `p`, run marginal-likelihood optimization. Then apply diagnostic vetoes.

Current project result:

- `p = 3` has higher marginal likelihood but hits `pi1 = 0.01` and worsens residual diagnostics.
- `p = 4` has stable `pi1 ~= 0.085`, keeps 2/6 Ljung-Box failures, and preserves headline channels.

Decision rule:

```text
Reject any optimized model where pi1 is at/near the lower bound or upper bound.
Reject any model that improves ML by becoming economically degenerate.
Prefer a slightly lower ML model if it passes diagnostics and preserves identified channels.
```

### Step 3: Check Hyperparameter Boundaries

Boundary checklist:

- `pi1 ~= 0.01`: too tight; data ignored.
- `pi1 ~= 1`: too loose relative to intended Minnesota shrinkage.
- `pi2 ~= 1`: acceptable here; means no extra cross-variable shrinkage.
- `pi3 = 1`: lower optimizer bound; acceptable because it is the standard harmonic decay and full optimizer beats manual alternatives.
- `pi4 ~= 100`: acceptable but not substantively meaningful unless profiled.
- `delta_i` at 0 or 1 for most variables: inspect carefully; may indicate a prior-mean boundary issue.

### Step 4: Posterior Verification, Not MCMC Diagnostics

The strict Minnesota model has a closed-form Normal posterior for coefficients conditional on fixed `Sigma`. Alexandria draws:

```text
beta_draw = b_bar + chol(V_bar) @ z
```

The draws are independent Normal draws, not a Markov chain. Therefore:

- Do not report burn-in.
- Do not report R-hat.
- Do not report ESS.
- Do not treat trace plots as convergence evidence.

Correct verification:

- Posterior signs on key channels.
- Posterior density shapes.
- IRF sign and horizon patterns.
- Residual diagnostics.
- OOS forecast performance.

### Step 5: OOS Validation

The existing project uses expanding-window conditional forecasts and finds BVAR wins 15/18 RMSE cells against VARX(1).

Important wording:

```text
The OOS exercise is conditional on observed future exogenous paths for `us_ffr` and `china_gdp`.
```

That is legitimate for comparing the domestic dynamic block, but it is not a real-time unconditional forecasting competition unless exogenous variables are themselves forecast or scenario-specified.

Paper wording:

```text
In conditional expanding-window forecasts using realized foreign-anchor paths, the BVAR(4) improves RMSE relative to the VARX(1) benchmark in 15 of 18 variable-horizon cells.
```

## 6. BVARX Tuning and Interpretation

### Why BVARX Is Right Here

The BVARX structure encodes small-open-economy block exogeneity:

```text
foreign anchors -> Hong Kong domestic block
Hong Kong domestic block -/-> foreign anchors within the quarter
```

This is not just convenience. Under LERS, Hong Kong's interest-rate environment is anchored to the US dollar system, while China growth is external to Hong Kong's quarterly macro dynamics.

### Exogenous Variables Should Be Few

The current exogenous block is defensible:

- `us_ffr`: monetary anchor / US rate condition.
- `china_gdp`: real external demand anchor.

Do not add weakly justified exogenous controls. Each exogenous variable adds one coefficient per equation and can absorb variation that should be interpreted through the domestic block.

### Exogenous Coefficients Should Usually Be Loosely Shrunk

For this project, large `pi4` is correct. The purpose of the model is to estimate how foreign anchors enter Hong Kong equations. Strongly shrinking `us_ffr` or `china_gdp` would suppress the exact channels of interest.

Recommended sensitivity:

```text
pi4 in {10, 50, 100, 500}
```

Expected result: little change once `pi4` is large enough. If results change materially between 50 and 500, then the exogenous block is more prior-sensitive than currently documented.

### FEVD Limitation in BVARX

Standard FEVD decomposes variance across endogenous structural shocks. Exogenous variables do not appear as FEVD shock bars.

Consequence:

- FFR effects that pass into lagged HIBOR show up as HIBOR own-share.
- China effects that pass into exports show up partly as exports own-share.

This is not a model failure, but it must be named. The post-Phase-9 HIBOR own-share near 93% is consistent with LERS because FFR is outside the endogenous decomposition.

Paper wording:

```text
Because the foreign anchors enter as exogenous regressors, FEVD shares are computed over the domestic endogenous shock block. US rate variation transmitted through lagged HIBOR therefore appears partly as HIBOR own variance rather than as a separate FFR shock contribution.
```

### If the Paper Needs Direct FFR FEVD

Options:

1. Bring `us_ffr` into the endogenous block and order it first.
   - Pros: FFR shock appears in FEVD.
   - Cons: changes the model and may overstate feedback unless block restrictions are imposed.

2. Estimate a two-block VAR/SVAR with foreign block exogeneity.
   - Pros: cleanest structural representation.
   - Cons: more implementation work and more parameters.

3. Keep BVARX and state the FEVD limitation.
   - Pros: consistent with current validated model.
   - Cons: FFR contribution remains indirect.

Recommendation for current paper: keep BVARX and disclose the FEVD limitation.

## 7. Identification and Cholesky Ordering

Cholesky ordering is post-estimation structural identification. It does not change marginal likelihood, fitted values, or OOS RMSE if coefficients are only permuted consistently.

Current Phase 9 ordering:

```text
hibor_3m -> hk_exports_china_yoy -> gdp_growth -> cpi_inflation -> unemployment -> hk_property_price_qoq
```

Rationale:

- Under LERS, HIBOR is disciplined by US dollar funding conditions and currency-board mechanics.
- Domestic Hong Kong GDP/unemployment should not move HIBOR contemporaneously.
- HIBOR can move property conditions contemporaneously or quickly.

The ordering is institutionally stronger than the older ordering with HIBOR fifth.

## 8. Levels, I(1), and VECM

Current stationarity status:

- I(0): exports YoY, GDP growth, property QoQ.
- I(1): CPI inflation, unemployment, property index level.
- Ambiguous/mean-reverting: HIBOR.

Johansen rank on the confirmed I(1) endogenous block is 0 at 95%. VECM is not warranted.

The BVAR-in-levels defense should not rely on "preserving cointegration information" because rank is 0. The better defense is:

- The model is Bayesian and regularized.
- The variables are economically interpretable in the forms used.
- Delta robustness for unemployment passed.
- Johansen rank=0 closes the omitted error-correction concern.
- Sims, Stock, Watson (1990) provide the relevant frequentist time-series background on inference with some unit roots in VAR-like systems.

## 9. Paper-Ready Method Paragraph

```text
We estimate a Bayesian VAR with four quarterly lags and exogenous foreign-anchor variables. The four-lag structure is chosen to capture multi-quarter macroeconomic transmission while avoiding the variance explosion of unrestricted VARX(4) estimation in a 108-observation sample. We use the Litterman/Minnesota prior, selecting the prior tightness parameters by marginal likelihood. The selected prior has overall tightness `pi1 = 0.085`, no additional cross-variable shrinkage (`pi2 = 1.0`), harmonic lag decay (`pi3 = 1.0`), and a diffuse prior on exogenous coefficients (`pi4 ~= 100`). The prior means for own first lags are optimized by series rather than fixed at a universal random-walk value. This specification regularizes the high-dimensional lag structure while preserving the cross-variable channels central to the research question.
```

## 10. Source Map

Primary/official sources consulted:

- Litterman, R. (1986). "Forecasting with Bayesian Vector Autoregressions: Five Years of Experience." Federal Reserve Bank of Minneapolis / JBES. https://www.fedinprint.org/item/fedmwp/42678/original
- Doan, T., Litterman, R., Sims, C. (1984). "Forecasting and Conditional Projection Using Realistic Prior Distributions." NBER Working Paper 1202. https://www.nber.org/papers/w1202
- Banbura, M., Giannone, D., Reichlin, L. (2010). "Large Bayesian Vector Auto Regressions." Journal of Applied Econometrics. https://ideas.repec.org/a/jae/japmet/v25y2010i1p71-92.html
- Giannone, D., Lenza, M., Primiceri, G. (2015). "Prior Selection for Vector Autoregressions." Review of Economics and Statistics. https://econpapers.repec.org/paper/nbrnberwo/18467.htm
- Sims, C., Stock, J., Watson, M. (1990). "Inference in Linear Time Series Models with Some Unit Roots." Econometrica. https://www.princeton.edu/~mwatson/papers/Sims_Stock_Watson_Ecta_1990.pdf
- HKMA. "Linked Exchange Rate System." https://www.hkma.gov.hk/eng/key-functions/money/linked-exchange-rate-system/
- HKMA. "How Does the LERS Work?" https://www.hkma.gov.hk/eng/key-functions/money/linked-exchange-rate-system/how-does-the-lers-work/
- HKMA Research Memorandum 11/2018. "Linked Exchange Rate System Operations - Mechanism and Theory." https://www.hkma.gov.hk/media/eng/publication-and-research/research/research-memorandums/2018/RM11-2018.pdf
- Alexandria local source files inspected:
  - `/opt/miniconda3/lib/python3.13/site-packages/alexandria/vector_autoregression/minnesota_bayesian_var.py`
  - `/opt/miniconda3/lib/python3.13/site-packages/alexandria/vector_autoregression/var_utilities.py`

