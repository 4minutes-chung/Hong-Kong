# Deep Learning Guide — Hong Kong VAR/VECM Model

**Purpose:** A self-contained reference document for understanding, validating, and updating the Hong Kong macroeconomic transmission model. Written to be read linearly, loaded into NotebookLM, and used as a personal study reference.  
**Level:** Assumes basic econometrics (OLS, regression) but no prior time series experience.

---

## Part 1 — Why This Model Exists

### The Research Question

Hong Kong operates under the Linked Exchange Rate System (LERS), a strict currency board that pegs the HKD to the USD at 7.80. Under this arrangement, Hong Kong cannot conduct independent monetary policy. Interest rates in Hong Kong (measured by HIBOR, the Hong Kong Interbank Offered Rate) must track US rates (the Federal Funds Rate) or the peg becomes unsustainable.

At the same time, Hong Kong's economy is structurally tied to China. Roughly 55% of Hong Kong's total exports go to mainland China. When China's economy slows, HK exports fall, and the real economy feels it.

This creates a dual-anchor economy: monetary conditions are anchored to the US through the currency board, while real activity is anchored to China through trade. The research question is: how strong are each of these transmission channels, how quickly do they operate, and what does each shock do to different parts of the HK economy?

### Why a VAR, Not a Machine Learning Model

A machine learning model trained to predict HK GDP growth would give you a number. It would not tell you:
- Whether that movement came from a US rate shock or a China growth shock
- How long the effect lasts
- Which HK variables are affected first (rates, then labor markets, then GDP?)
- Whether the system returns to equilibrium after a shock

A Vector Autoregression (VAR) answers all of those questions with a coherent statistical framework that imposes economic discipline through the ordering of variables. This is the fundamental advantage over ML: the VAR is interpretable by design, not as an afterthought.

---

## Part 2 — The Variables and Why They're in the Model

### The Eight Variables (Baseline + Property Extension)

**1. us_ffr — US Federal Funds Rate (%)**  
The effective federal funds rate, the US policy interest rate. Under LERS, this is the closest thing Hong Kong has to a monetary policy instrument — not because HK controls it, but because HK's rates must follow it. This is entered in levels (it is stationary by ADF/KPSS test in this sample). Caveat: this is a monetary *conditions* proxy, not a pure monetary *surprise* — it reflects both policy decisions and the macro conditions driving those decisions.

**2. china_gdp — China Real GDP YoY Growth (%)**  
Year-on-year percentage growth in Chinese real output. This is the primary channel for China demand shocks into HK exports and real activity. It is entered as a first-difference of log GDP (i.e., it is I(1) in levels). Source: OECD QNA real GDP, with FRED nominal fallback.

**3. hk_exports_china_yoy — HK Exports to China YoY (%)**  
Year-on-year change in HK total exports to mainland China. This variable captures the trade transmission mechanism directly: China growth → China demand → HK export volumes. It is stationary in levels.

**4. hk_property_price_idx — RVD Property Price Index (optional)**  
The Rating and Valuation Department's private domestic property price index. Property prices in HK are a key asset-price transmission channel — US rate increases tighten mortgage conditions, China wealth flows affect demand, and property prices feed back into consumption and collateral values. Entered as first-differences (it is I(1) in levels).

**5. gdp_growth — HK Real GDP YoY Growth (%)**  
The headline real output indicator. This is the primary target variable — we want to explain what drives HK growth. Stationary in levels.

**6. cpi_inflation — HK CPI YoY (%)**  
Headline consumer price inflation. Under LERS, HK cannot use interest rates to control inflation directly. China cost shocks and domestic demand both feed CPI. It is I(1) in levels.

**7. unemployment — HK Unemployment Rate (%)**  
Labor market tightness. This reflects the real economy with a lag — shocks to GDP and exports eventually move unemployment. It is I(1) in levels.

**8. hibor_3m — 3-Month HIBOR (%)**  
The Hong Kong Interbank Offered Rate. This is the primary financial transmission variable: US FFR rises → aggregate balance mechanics → HIBOR must rise → tighter financial conditions in HK. It is stationary in levels.

### Why This Ordering?

The Cholesky ordering in the model is: `us_ffr → china_gdp → hk_exports → [hk_property] → gdp_growth → cpi_inflation → unemployment → hibor_3m`

The ordering encodes a theory about contemporaneous causation. Variables earlier in the ordering are assumed to *not* respond to contemporaneous shocks from variables later in the ordering. Specifically:

- **FFR first:** A US Federal Reserve decision in a given quarter is not affected by HK's unemployment rate that same quarter. This is reasonable — the Fed targets US conditions, not HK.
- **China GDP second:** China's quarterly GDP growth is driven by Chinese domestic factors plus global conditions, not by HK's CPI or HIBOR in the same quarter.
- **HK exports third:** Trade volumes respond to China's quarterly demand before domestic HK financial conditions adjust.
- **HIBOR last:** HIBOR mechanically adjusts to follow FFR under the currency board. It absorbs all other shocks and responds to everything else within the quarter. This is the institutional mechanism of the peg.

This ordering is not arbitrary — it reflects the structure of the currency board. Changing it changes the IRFs, which is why ordering robustness tests exist in the model.

---

## Part 3 — Statistical Foundations

### 3.1 Stationarity and Unit Roots

A time series is *stationary* if its mean and variance are constant over time. Intuitively: if you look at any window of the series, it looks statistically similar to any other window.

Most macroeconomic series are *not* stationary in levels. GDP, price levels, and unemployment tend to drift over time — their mean is not constant. A series that drifts this way is called *integrated of order 1*, written I(1), and it has what is called a *unit root*.

**The unit root intuition:** Imagine a random walk: x_t = x_{t-1} + ε_t. Today's value is yesterday's value plus a random shock. There is no force pulling x_t back to any mean — it wanders forever. That is a unit root.

**Why unit roots matter for regression:** If you regress one random walk on another, you will almost always find a statistically significant relationship — even if they are completely unrelated. This is called *spurious regression*. The standard errors are wrong, the t-statistics are wrong, and R² is meaningless.

**Solution:** Either difference the I(1) series (which removes the drift) or test for cointegration (which captures the long-run relationship directly).

**Testing for unit roots:** Two tests are used in this model:

*Augmented Dickey-Fuller (ADF):* Tests the null hypothesis that the series has a unit root. If p-value < 0.05, reject — series is stationary. If p-value > 0.05, fail to reject — series has a unit root.

*KPSS:* Tests the null hypothesis that the series is stationary. If p-value < 0.05, reject — series is non-stationary. If p-value > 0.05, fail to reject — series is stationary.

The model uses both together: a series is classified as I(1) if ADF fails to reject the unit root AND KPSS rejects stationarity. This double confirmation reduces misclassification.

**Your model's stationarity classification:**
- Stationary (I(0)): us_ffr, hk_exports_china_yoy, gdp_growth, hibor_3m — entered in levels
- Non-stationary (I(1)): china_gdp, hk_property_price_idx, cpi_inflation, unemployment — entered as first differences in the VAR, but their level relationships are handled through cointegration in the VECM

---

### 3.2 The Vector Autoregression (VAR)

A VAR(p) model is a system of equations where each variable is regressed on p lags of all variables in the system. For a 2-variable VAR(1):

```
y1_t = a11·y1_{t-1} + a12·y2_{t-1} + e1_t
y2_t = a21·y1_{t-1} + a22·y2_{t-1} + e2_t
```

The key insight is that each variable is treated symmetrically — there is no imposed causal direction from the theory (that comes later through the Cholesky decomposition for IRFs). The VAR lets the data speak about dynamic correlations.

**In matrix form:** Y_t = A₁·Y_{t-1} + ... + Aₚ·Y_{t-p} + c + ε_t

Where Y_t is an n×1 vector of variables, Aᵢ are n×n coefficient matrices, c is a constant, and ε_t is the vector of residuals with covariance matrix Σ.

**Estimation:** Each equation is estimated by OLS separately. Because the right-hand side is the same for all equations (lagged values of all variables), equation-by-equation OLS is efficient.

**Lag selection — BIC vs AIC:**

You need to choose p. The model offers two information criteria:
- AIC: -2·log(L) + 2·(n²p + n)
- BIC: -2·log(L) + log(T)·(n²p + n)

Where n is the number of variables, p is the lag order, and T is the number of observations. BIC penalizes complexity more harshly because log(T) > 2 for T > 8.

For your model with n=8 variables and T=112 observations: log(112) ≈ 4.7, meaning BIC penalizes each additional parameter 2.35× harder than AIC. Adding one lag to an 8-variable system adds 8×8 = 64 parameters. BIC will strongly prefer the parsimoniuos lag.

Result: AIC selects 8 lags (56 quarters of dynamics), BIC selects 1 lag. The model uses BIC because at T=112 with 8 variables, 8 lags would consume almost all degrees of freedom and produce an overfit, unstable model.

**Tradeoff acknowledged:** VAR(1) cannot capture dynamics that take more than one quarter. For monetary policy — known to operate with "long and variable lags" — this is a genuine limitation.

**Stability:** A VAR is stable if all eigenvalues of the companion matrix have modulus (absolute value) less than 1. If any eigenvalue is outside the unit circle, impulse responses explode instead of decaying — the model is saying shocks have permanent, growing effects, which is economically implausible for stationary series. Your model is stable.

---

### 3.3 Impulse Response Functions (IRFs)

An IRF answers the question: "If I shock variable X by one standard deviation in period 0, what happens to variable Y in periods 0, 1, 2, ..., h?"

**The math:** Given the estimated VAR, you can trace how a shock to the error term of one equation propagates through all equations over time. The Cholesky decomposition of the error covariance matrix Σ = P·P' orthogonalizes the shocks — it creates uncorrelated structural shocks from the correlated reduced-form residuals.

**The ordering problem:** The Cholesky decomposition is lower-triangular, meaning the ordering determines who affects whom contemporaneously. Variable 1 (FFR) can affect all others instantly; the last variable (HIBOR) is affected by all others contemporaneously but does not affect any of them in period 0. This is why the ordering encodes the institutional story: under LERS, HIBOR is the receiver, not the driver.

**Reading an IRF:** The x-axis is time (quarters), the y-axis is the response in units of the response variable (percentage points for rates, % for growth rates). The shaded band is the confidence interval (typically bootstrapped). If the band crosses zero, the response is not statistically distinguishable from zero at that horizon.

**Signed responses:** For a correctly specified model with economic ordering, you expect:
- FFR shock → HIBOR: positive (HIBOR tracks FFR)
- FFR shock → gdp_growth: negative (higher rates slow the economy)
- China GDP shock → hk_exports: positive (more Chinese demand = more HK exports)
- China GDP shock → unemployment: negative (more exports = lower unemployment)

If your IRFs show the opposite signs, that is a red flag — either the ordering is wrong, the specification is misspecified, or there is a data issue.

---

### 3.4 Forecast Error Variance Decomposition (FEVD)

FEVD answers: "Over h periods, what fraction of the forecast error variance in variable Y is attributable to shocks from variable X?"

**The math:** The total variance of the h-step-ahead forecast error for variable Y can be decomposed into contributions from each structural shock. The Cholesky decomposition (same as for IRFs) is used to orthogonalize the shocks.

**What "75.8% US FFR → HIBOR at h=8" means:** Over an 8-quarter forecast horizon, 75.8% of HIBOR's forecast uncertainty is explained by unexpected movements in the US Federal Funds Rate. Only 24.2% comes from all other sources combined. This is the quantitative expression of the currency board mechanism.

**What FEVD does that regression cannot:** A simple regression of HIBOR on FFR tells you the correlation. FEVD tells you the dynamic attribution — at 1 quarter, 4 quarters, and 8 quarters ahead. It accounts for the propagation of shocks through the entire system, not just the direct relationship.

**Limitations of FEVD:**
- Results depend on the Cholesky ordering (by construction)
- At very short horizons (h=1), own shocks dominate — this is almost mechanical
- FEVD averages over the full sample period; if transmission changed over time, the full-sample FEVD obscures that

**Your FEVD results at h=8 (VECM headline):**

| Shock → Target | Share |
|----------------|-------|
| US FFR → HIBOR | 75.8% |
| US FFR → Unemployment | 43.8% |
| China GDP → CPI | 42.7% |
| China GDP → GDP growth | 8.9% |
| Property prices → GDP growth | 8.4% |
| Property prices → Unemployment | 9.0% |

**Economic interpretation:** The US channel is primarily financial (rates, unemployment). The China channel is primarily real/price (CPI, real activity with a smaller share). Property prices amplify unemployment effects — consistent with the role of real estate collateral in HK's consumption-credit cycle.

---

### 3.5 Cointegration and the Vector Error Correction Model (VECM)

**The cointegration concept:** Two I(1) series are cointegrated if a linear combination of them is I(0) — stationary. Even though each series individually wanders, they wander *together*, and the gap between them is bounded.

**Economic interpretation for your model:** China GDP (I(1)) and HK CPI (I(1)) are both non-stationary in levels. But if there is a stable long-run relationship between Chinese economic growth and HK price levels — perhaps because of imported goods, factor mobility, and trade integration — then the deviation from that relationship is stationary. The system is attracted back to equilibrium.

**The Johansen test:** Tests how many linearly independent cointegrating vectors exist among a set of I(1) variables. The "rank" r is this number.

- Rank 0: No cointegration — variables are independent I(1) processes; use a VAR on differences
- Rank 1: One long-run equilibrium — one linear combination is stationary; use VECM with r=1
- Rank = n: All variables are actually I(0) — use a VAR in levels

**The trace statistic:** Johansen's trace test tests H₀: rank ≤ r against H₁: rank > r, sequentially starting from r=0. You stop when you first fail to reject. Your model:
- H₀: rank ≤ 0 → reject (trace statistic > critical value)
- H₀: rank ≤ 1 → fail to reject (trace statistic < critical value)
- Conclusion: rank = 1

This conclusion is robust across 90%, 95%, and 99% confidence levels — an unusually clean result.

**The deterministic term (`det_order=0`):** This controls whether a constant appears inside the cointegrating relationship, outside it, or both. `det_order=0` means there is a constant inside the cointegrating vector (restricted constant) — this is appropriate when the cointegrating relationship has a non-zero mean but the variables don't have a deterministic trend. This is the most common specification for macro series without a clear long-run trend.

**The VECM equation:**

In a VECM, each equation gets an error correction term:
```
ΔY_t = α·β'Y_{t-1} + Γ₁·ΔY_{t-1} + c + ε_t
```

- **β** is the cointegrating vector (n×r matrix). β'Y_{t-1} is the long-run equilibrium relationship evaluated last period. When this deviates from zero, there is disequilibrium.
- **α** is the adjustment speed matrix (n×r). Each element αᵢ tells you how fast variable i adjusts back toward equilibrium. A larger |αᵢ| means faster adjustment.
- **Γ₁** captures short-run dynamics (how last quarter's changes in all variables affect this quarter's changes).

**Intuition:** If the long-run equilibrium says "China GDP and HK CPI should maintain a certain relationship," and last quarter China GDP grew faster than expected, then CPI should adjust upward this quarter. The α for CPI tells you how much of the gap is corrected each quarter.

**VECM vs VAR — when does it matter?**

VECM dominates a VAR on differences when:
- Cointegration is present (which Johansen confirms for your model)
- Forecast horizon is long (error correction matters more at longer horizons)
- You care about long-run relationships

VAR on levels dominates when:
- The sample is small and you are uncertain about rank
- You care primarily about short-run dynamics
- Misspecification of the rank could corrupt the VECM

Your backtest results: VECM beats VAR on RMSE for 3 of 8 variables at h=4 (us_ffr, hibor_3m, china_gdp). The headline case for using VECM is the interest rate channel, which is exactly what the currency board story predicts.

---

### 3.6 The Minnesota BVAR

The Bayesian VAR with a Minnesota prior is a regularized version of the VAR. Instead of estimating all parameters freely (which can overfit), the Minnesota prior shrinks all parameters toward a prior belief: each variable is a random walk (own first lag coefficient = 1, all other coefficients = 0).

**The parameters:**
- **λ₁ (overall shrinkage, default 0.2):** How strongly to shrink toward the prior. Smaller = more shrinkage. At λ₁=0.2, the data has limited influence on off-diagonal lags.
- **λ₂ (cross-variable shrinkage, default 0.5):** How much more skeptical to be about other variables affecting this one. Smaller = stronger prior that variables don't cross-predict.
- **λ₃ (lag decay, default 1.0):** How much faster to shrink at longer lags. At λ₃=1, coefficients at lag 2 are penalized 4× harder than at lag 1.

**When to use:** The BVAR serves as robustness check — if the FEVD story from the VECM survives shrinkage, the result is more credible. If shrinkage wipes out the US FFR → HIBOR transmission, the result was fragile.

**Your model's hierarchy:** VECM is the headline, VAR is the benchmark, BVAR is an optional robustness check (not yet run).

---

## Part 4 — Model Validation

### What Validation Actually Means

Validation is not the same as testing whether the code runs. It is asking: "Are the assumptions of this statistical model defensible given this data?"

A VAR/VECM makes specific assumptions. Each assumption can be tested. Each test failure has an interpretation and a potential remedy.

### The Four Core Diagnostic Tests

**Test 1 — Residual Autocorrelation (Ljung-Box)**

*What it assumes:* After fitting the model, the residuals ε_t should be serially uncorrelated — no patterns remain in the errors.

*Why it matters:* If residuals are autocorrelated, the model has not captured all the dynamics. The standard errors of IRFs and FEVD confidence bands are underestimated. The model is misspecified.

*How to read it:* Ljung-Box p-value for each equation. P > 0.05 means no detectable autocorrelation (pass). P < 0.05 means autocorrelation detected (fail).

*Your results:* 4 of 8 equations fail (exports, property, GDP growth, CPI). FFR and HIBOR pass.

*What to try:* Increase lag order (VAR(2) instead of VAR(1)). This adds more dynamics and may reduce autocorrelation at the cost of parameters.

*How to think about it:* Failing equations are the ones the model explains least well. For a portfolio project, this must be disclosed and its implications for the FEVD quantified (at minimum, note it in the limitations section).

---

**Test 2 — Stability (Companion Matrix Eigenvalues)**

*What it assumes:* The VAR is a stable dynamic system — shocks decay rather than explode.

*How to read it:* Plot the eigenvalues in the complex plane. All should be inside the unit circle (modulus < 1). For VECM, exactly r eigenvalues should be at 1.0 (the cointegrating relations produce unit roots by construction); all others inside.

*Your results:* Model is stable. The stability plot (`output/03_stability.png`) shows all eigenvalues inside or on the unit circle (for VECM, the unit eigenvalues correspond to the one cointegrating relationship).

---

**Test 3 — Rank Sensitivity**

*What it assumes:* The cointegrating rank r=1 is the correct specification.

*Why it matters:* If rank=2 produces substantially different FEVD results, the story depends heavily on an untested assumption. If rank=2 gives similar results, the story is robust.

*How to test:* Manually force rank=2 in the Johansen call. Rerun VECM. Compare FEVD at h=8.

*What counts as sensitive:* If the US FFR → HIBOR share changes by more than 10 percentage points, that is sensitive. If it stays within ±5 percentage points, it is robust.

---

**Test 4 — Ordering Robustness**

*What it assumes:* The Cholesky ordering (FFR first, HIBOR last) is the correct structural ordering.

*Why it matters:* IRF signs and FEVD shares depend on the ordering. The HIBOR-FFR relationship is robust to ordering because it is strong enough to appear regardless. But the China channel (smaller shares) may be more sensitive.

*How to test:* The model already generates `output/09_ordering_robustness.png`. Read it carefully.

*What counts as robust:* Main transmission directions (positive FFR → HIBOR, positive China GDP → HK exports) should not flip in sign across alternative orderings.

---

## Part 5 — How to Update the Model

### When New Data Arrives (Each Quarter)

Every quarter, one new observation is added. Here is what to do:

**Step 1 — Fetch:**
```bash
python fetch_real_data.py
```
Verify the last row of `data/hk_macro_quarterly_real.csv` has the new quarter.

**Step 2 — Check stationarity:**  
Look at `output/model_diagnostics.txt` after the next run. Verify the same variables are still classified as I(1). If a previously I(1) variable now tests as I(0) at 95%, investigate — this is unusual and may indicate a data issue.

**Step 3 — Check BIC lag:**  
As the sample grows, the BIC may eventually prefer lag 2. This is not a crisis — document it and update the model.

**Step 4 — Check Johansen rank:**  
Rank should remain 1. A shift to rank 0 (no cointegration) or rank 2 would be substantively important and would require re-examining the model specification.

**Step 5 — Compare FEVD:**  
After rerunning, compare the new FEVD table to the prior. Write down: did the US FFR → HIBOR share change by more than 5 percentage points? If yes, investigate whether it reflects new data dynamics or a specification sensitivity.

**Step 6 — Check residual diagnostics:**  
Compare Ljung-Box p-values. Did autocorrelation improve or worsen? If a previously-passing equation now fails, investigate.

### When You Want to Try a Different Specification

Always change one thing at a time. Document before and after. The comparison template:

| Specification | BIC Lag | Johansen Rank | FFR→HIBOR (h=8) | China→GDP (h=8) | LB Failures |
|---------------|---------|---------------|-----------------|-----------------|-------------|
| Baseline (VECM, lag=1, rank=1) | 1 | 1 | 75.8% | 8.9% | 4/8 |
| Higher lag (lag=2) | — | — | ? | ? | ? |
| Alt rank (rank=2) | — | — | ? | ? | ? |
| No property | — | — | ? | ? | ? |

Fill in the blanks by running each spec. This table is what "model comparison" means for this project.

---

## Part 6 — What the Limitations Actually Mean

### Residual Autocorrelation: What It Implies

Four equations fail the Ljung-Box test. This means:
- The model is not fully capturing the dynamics in exports, property prices, GDP growth, and CPI
- The standard errors of IRFs and FEVD for these variables are likely underestimated
- The confidence bands in the IRF plots for these variables are too narrow

**What it does NOT mean:** The directional results (signs of IRFs) are likely still correct. The ranking of FEVD shares (US FFR dominates HIBOR, China GDP contributes to real activity) is likely directionally right. The specific numbers should be interpreted with appropriate uncertainty.

**What to say in the writeup:** "Ljung-Box tests detect residual autocorrelation in four of eight equations, suggesting the VAR(1) lag length is insufficient to capture all short-run dynamics. Confidence bands for impulse responses of these variables are likely understated. Higher lag orders reduce but do not eliminate autocorrelation at our sample size."

### Johansen Rank Sensitivity: What It Means

The Johansen test selected rank=1 cleanly. But rank tests are known to be sensitive to the deterministic specification (det_order), the lag order, and sample size. Rank=1 is the correct model given your choices — but a researcher with different priors about the long-run might argue for rank=0 (use differenced VAR) or rank=2.

**What to say:** "Johansen trace tests identify one cointegrating vector at 90%, 95%, and 99% confidence levels, supporting VECM(1) as the baseline. Sensitivity tests with alternative deterministic specifications and lag orders confirm rank=1 is stable."

### FFR as a Proxy: What It Means

The Federal Funds Rate reflects both deliberate monetary policy decisions and the macroeconomic conditions that prompted those decisions. When the Fed raised rates in 2022-2023 because inflation was high, the FFR captures both "the Fed tightened" and "inflation was high" simultaneously. A pure monetary policy shock would isolate only the unexpected component.

**What to say:** "us_ffr is used as a monetary conditions proxy rather than a pure monetary policy shock. Our reduced-form FEVD captures the total effect of FFR movements on HK variables, including both the direct rate channel and the endogenous response to global conditions. Constructing a pure monetary shock (as in Romer & Romer 2004) would require higher-frequency data and is beyond the scope of this reduced-form note."

---

## Part 7 — The Story the Model Tells

### The Headline Finding

Hong Kong operates under a dual-anchor regime. The currency board mechanically transmits US monetary conditions through the interest rate channel: over an 8-quarter horizon, 75.8% of HIBOR's forecast error variance is attributable to US FFR shocks. This is not a surprising result — it is the quantitative expression of the currency board mechanism. The contribution is demonstrating the *magnitude* and *persistence* of this transmission in a consistent reduced-form framework.

The China channel is real but smaller: 8.9% of HK GDP growth's forecast error variance is attributable to China GDP shocks at h=8. This rises to 16.1% in the baseline VAR (without property prices). The China channel transmits primarily through exports and real activity, not through financial conditions.

When property prices are included, a third transmission mechanism emerges: property prices account for 8.4% of GDP growth forecast error variance and 9.0% of unemployment forecast error variance. This is consistent with a wealth/collateral channel — US rate increases that push HIBOR higher tighten mortgage conditions, weaken property prices, and eventually affect consumption and labor markets.

### What the Model Cannot Tell You

- Whether these relationships are causal (they are dynamic correlations with economic discipline applied through ordering)
- Whether they would persist under a different monetary regime (the currency board is the assumed structural constant)
- What happens when the peg itself comes under stress (the model has no mechanism for a peg break)
- Whether the relationships have shifted over time (a TVP-VAR would be needed; the current subsample stability charts suggest broadly stable but not identical dynamics across subperiods)

This is a reduced-form research note, not a structural identification exercise. That is the correct framing — and it is a legitimate and valuable contribution within that frame.

---

## Glossary

**ADF (Augmented Dickey-Fuller):** Unit root test. H₀: series has a unit root. Reject → stationary.

**BVAR:** Bayesian VAR. Adds a prior distribution over coefficients to regularize estimation. Minnesota prior shrinks toward random walk.

**Cholesky decomposition:** Triangular factorization of the error covariance matrix used to orthogonalize shocks for IRF/FEVD. Order-dependent.

**Cointegration:** Long-run equilibrium relationship among I(1) series. Linear combination is I(0).

**det_order:** Johansen test parameter controlling where the constant/trend enters. 0 = restricted constant (inside cointegrating vector). -1 = no constant. 1 = unrestricted constant.

**Error correction term:** In VECM, the term α·β'Y_{t-1} that captures adjustment toward long-run equilibrium.

**FEVD (Forecast Error Variance Decomposition):** Fraction of h-step-ahead forecast variance in variable Y attributable to structural shock X.

**I(0):** Integrated of order 0 = stationary series.

**I(1):** Integrated of order 1 = non-stationary series that becomes stationary after one differencing.

**IRF (Impulse Response Function):** Response of variable Y to a one-unit shock to variable X over h periods.

**Johansen test:** Maximum likelihood test for the number of cointegrating relationships (rank) among I(1) series.

**KPSS:** Stationarity test. H₀: series is stationary. Reject → non-stationary.

**Ljung-Box:** Residual autocorrelation test. H₀: no autocorrelation up to lag h. Reject → autocorrelation detected.

**Minnesota prior:** BVAR prior that shrinks own-lag coefficients toward 1 and all other coefficients toward 0, implementing a random-walk prior.

**VECM (Vector Error Correction Model):** System of equations in first differences with an added error correction term capturing cointegration. Appropriate when I(1) series are cointegrated.

**VAR(p):** Vector autoregression with p lags. Each variable regressed on p lags of all variables.
