# Study Plan — Hong Kong VAR/VECM: Own the Model

**Goal:** Move from running AI-generated code to understanding, validating, and updating the model yourself.  
**Format:** Code-to-code. Every phase ends with a hands-on checkpoint you can run and verify.  
**Timeline:** 4–5 weeks at roughly 3–4 hours per week. Non-negotiable minimum.

---

## The Learning Hierarchy

```
Economic intuition  (why does this model make sense for HK?)
        ↓
Statistical theory  (what do the estimators actually assume?)
        ↓
Code reading        (how does hk_var_model.py implement each step?)
        ↓
Validation          (how do you know if something is wrong?)
        ↓
Updating            (how do you rerun, respecify, and compare?)
```

You cannot skip levels. People who skip straight to code cannot validate. People who skip theory cannot understand the code.

---

## Phase 0 — Economic Context (Week 1)

**Objective:** Before touching statistics, understand *why* a VAR makes sense for Hong Kong specifically.

### Readings (from your reading list — download these first)

Priority order:
1. **HKMA RM 11/2018** — LERS mechanics. Read this first. It explains the institutional constraint that justifies your Cholesky ordering (FFR first, HIBOR last).
2. **Genberg, Liu, Jin (2006) HKMA RM 11/2006** — US vs China channel decomposition for HK. This is your benchmark.
3. **Chen & Tsang (2020) Pacific Economic Review** — closest paper to your project. US shocks → financial conditions; China shocks → real activity.

**NotebookLM upload:** Upload all three PDFs as a single source group. Ask it to generate a podcast episode on: "How do US monetary policy and China growth transmit to Hong Kong's real economy under the currency board?"

### Checkpoint Questions (write answers, don't just think them)

1. Why does HIBOR track the US Federal Funds Rate? What is the mechanism? (Hint: LERS, Aggregate Balance, Currency Board Operations)
2. Why can't HK run independent monetary policy? What does that mean for your model's identification?
3. What is the difference between the US channel (financial/rate channel) and the China channel (real/trade channel) in HK?
4. Why does exports-to-China belong in the ordering between China GDP and HK domestic variables?

---

## Phase 1 — Statistical Foundations (Week 2)

**Objective:** Understand the three core statistical concepts that underpin every decision in the model.

### Concept A: Stationarity and Unit Roots

**What it means:** A series is stationary if its mean and variance don't change over time. Most macro series are non-stationary — they drift. A "unit root" means the series has no tendency to revert to any mean.

**Why it matters for your model:**  
- You cannot run a VAR directly on I(1) series (series with a unit root) — you get spurious regression
- The model first tests each series with ADF (Augmented Dickey-Fuller) and KPSS tests
- Series that are I(1) get first-differenced before entering the VAR
- But if multiple I(1) series share a long-run equilibrium (cointegration), you lose information by differencing both — that's why VECM exists

**Your model's result (from `output/model_diagnostics.txt`):**
```
Transforms used (ADF+KPSS confirmed):
  us_ffr: level              ← stationary, no differencing needed
  china_gdp: first_diff      ← I(1), differenced
  hk_exports_china_yoy: level
  hk_property_price_idx: first_diff  ← I(1)
  gdp_growth: level
  cpi_inflation: first_diff  ← I(1)
  unemployment: first_diff   ← I(1)
  hibor_3m: level
```

Four series are I(1): china_gdp, property prices, CPI, unemployment.

**Code location in `hk_var_model.py`:** Look for `adfuller()` and `kpss()` calls. The function that runs stationarity tests is `_determine_transforms()`.

**Reading:** Engle & Granger (1987) is the foundational paper on cointegration. You don't need to derive the math — read the introduction and the concept sections.

**Checkpoint:** Run just the stationarity test block manually in a Python notebook. Load `data/hk_macro_quarterly_real.csv`. For `china_gdp`, run `adfuller(df['china_gdp'], autolag='BIC')`. Look at the p-value. If p > 0.05, the series has a unit root (fail to reject H0 of a unit root). Then difference it and run again — p should be < 0.05. Write down what changed and why.

---

### Concept B: Lag Selection (BIC vs AIC)

**What it means:** A VAR(p) model says "today's value of every variable depends on the last p quarters of all variables." Choosing p is not arbitrary — too few lags and you miss dynamics; too many lags and you overfit (burn degrees of freedom on a small sample).

**The formulas:**
- AIC = -2·log(L) + 2k  (penalizes by 2 per parameter)
- BIC = -2·log(L) + k·log(n)  (penalizes by log(n) ≈ 4.7 per parameter for n=112)

BIC penalizes more harshly. On small samples with many variables (your case: 112 obs, 8 variables), BIC almost always picks fewer lags.

**Your model's result:**
```
aic_lag=8, bic_lag=1, selected_lag=1
```

AIC wants 8 lags (captures more dynamics but costs 8×8×8 = 512 parameters). BIC says 1 lag — at n=112 with 8 variables, that's more honest. Your code uses BIC by default (`--lag-criterion bic`).

**What you lose with VAR(1):** You cannot capture effects that take more than one quarter to transmit. For monetary policy (which is known to have long and variable lags), this is a real cost. Your limitations section should mention this.

**Code location:** Look for `model.select_order()` in `hk_var_model.py`. The `select_order()` method from statsmodels returns a table of AIC/BIC/HQIC/FPE for each lag order. You can print this table.

**Checkpoint:** In a Python notebook, load your data and run:
```python
from statsmodels.tsa.api import VAR
model = VAR(df_stationary)
results = model.select_order(maxlags=8)
print(results.summary())
```
Read the table. Write down: what is the AIC and BIC value at lag 1 vs lag 2 vs lag 4? How much does each criterion change? What is the tradeoff?

---

### Concept C: Cointegration and VECM

**What it means:** Even if individual series are I(1) (random walks), they can be "cointegrated" — meaning there exists a linear combination that is stationary. That linear combination is the long-run equilibrium.

**Example for your model:** China GDP (I(1)) and HK CPI (I(1)) might both wander, but if China's economy booms, HK inflation tends to follow. The *gap* between them is stationary — it mean-reverts. That's cointegration.

**Johansen test:** Tests how many independent cointegrating relationships exist among your I(1) variables. The "rank" r tells you how many long-run equilibria there are.

**Your model's result:**
```
i1_vars = ['china_gdp', 'hk_property_price_idx', 'cpi_inflation', 'unemployment']
rank_trace(90/95/99) = 1/1/1
```

Rank = 1 means exactly one long-run equilibrium ties these four I(1) variables together. This is clean — the test agrees at 90%, 95%, and 99% confidence levels (no ambiguity).

**VECM vs VAR:** A VAR on differenced I(1) variables discards long-run information. VECM keeps it by adding an "error correction term" — a term that pulls variables back toward the long-run equilibrium whenever they deviate.

**What the error correction term looks like:**
```
Δy_t = α·(β'y_{t-1}) + Γ₁·Δy_{t-1} + ε_t
```
- β'y_{t-1} is the cointegrating vector (the long-run equilibrium)
- α is the speed of adjustment (how fast the system corrects)
- Γ₁ captures short-run dynamics

**Reading:** Johansen (1991) is the reference. Read the introduction and section on the trace test statistic. You don't need to derive the ML estimator — understand what the test is asking and how to read the rank table.

**Checkpoint:** Run the Johansen test manually:
```python
from statsmodels.tsa.vector_ar.vecm import coint_johansen
i1_cols = ['china_gdp', 'hk_property_price_idx', 'cpi_inflation', 'unemployment']
df_i1 = df[i1_cols].dropna()
result = coint_johansen(df_i1, det_order=0, k_ar_diff=1)
print("Trace statistic:", result.lr1)
print("Critical values (90/95/99):", result.cvt)
```
Read the output. The rank is where the trace statistic first falls *below* the critical value. Write down: what is the rank, and what happens to it if you change `det_order` from 0 to -1 or 1? (This is sensitivity analysis — det_order controls whether a constant goes inside or outside the cointegrating vector.)

---

## Phase 2 — Code Reading (Week 3)

**Objective:** Read `hk_var_model.py` top to bottom. Understand what every major section does.

### Section Map

| Lines | What it does |
|-------|-------------|
| 1–120 | Docstring, imports, constants, data specs |
| 125–350 | BVAR and VECM class definitions |
| 350–550 | Data loading, stationarity, transforms |
| 550–750 | VAR estimation, lag selection, stability check |
| 750–950 | IRF computation, FEVD |
| 950–1150 | Historical decomposition |
| 1150–1350 | Backtesting and forecast RMSE |
| 1350–1550 | Scenario forecasting |
| 1550–1750 | Robustness: sign restrictions, ordering sensitivity, TVP-VAR sketch |
| 1750+ | Report generation, main() |

### Reading Exercise (do these in order)

**Step 1: Data loading**  
Find `load_data()` or the equivalent data assembly block. Answer: where does the data come from? What happens if a CSV is missing? What are the fallback sources?

**Step 2: Stationarity block**  
Find where ADF and KPSS are called. Understand: what decision rule does the code use to decide whether to difference a series? (Hint: look for something like `if adf_pval > threshold and kpss_pval < threshold`)

**Step 3: The VECM wrapper**  
Read `VECMResultsWrapper` (lines 265–349). Understand: why does the code wrap statsmodels' VECM result? What interface does it expose that the rest of the code uses? The key insight: the code converts the VECM back to its VAR representation (`var_rep`) for IRF and FEVD computation.

**Step 4: FEVD computation**  
Find where FEVD is computed. Understand: FEVD is computed from the Cholesky decomposition of the error covariance matrix. The ordering of variables determines the decomposition. This is why ordering matters — it's not cosmetic.

**Step 5: Backtesting**  
Find the backtest block. Understand: the model is estimated on a training window, then used to forecast h steps ahead. RMSE is computed against actuals. This is how you compare VAR vs VECM — not by R², but by out-of-sample forecast accuracy.

### Checkpoint

For each section above, write one sentence in plain English: "This section does X, using Y as input, producing Z as output."

---

## Phase 3 — Validation (Week 4)

**Objective:** Learn how to tell if the model is well-specified and what to do when it isn't.

### Validation Test 1: Residual Autocorrelation (Ljung-Box)

**What it tests:** After fitting the model, residuals should be white noise — no predictable patterns left. If residuals are autocorrelated, the model missed some dynamics.

**Your result (from `output/vecm_diagnostics.txt`):**
```
hk_exports_china_yoy: p=0.0082   ← FAIL (significant autocorrelation)
hk_property_price_idx: p=0.0105  ← FAIL
gdp_growth: p=0.0000             ← FAIL
cpi_inflation: p=0.0006          ← FAIL
us_ffr: p=0.9735                 ← PASS
hibor_3m: p=0.7182               ← PASS
```

Four equations fail. This means the model is missing dynamics in those series. **This does not mean the model is useless** — but it must be disclosed and the implications understood.

**What to try:** Increase `lag_diff` from 1 to 2 or 3. Run again. Check if autocorrelation improves. Document what changes.

**Checkpoint:** Change `--lag-criterion bic` to a fixed lag 2 run. Look at the Ljung-Box output. Does autocorrelation improve? What does it cost (more parameters, fewer effective observations)?

---

### Validation Test 2: Stability (Eigenvalues)

**What it tests:** A VAR/VECM is stable if the impulse responses eventually decay to zero — shocks don't explode. Stability requires all eigenvalues of the companion matrix to be inside the unit circle (modulus < 1).

**VECM special case:** In a VECM, the I(1) variables by construction have unit roots — some eigenvalues will equal exactly 1 (not inside, on the circle). This is normal and expected. Stability for VECM means: r eigenvalues at 1 (one per cointegrating relationship), and all others strictly inside.

**Your result:** Eigenvalue check passes — the model is stable.

**Code location:** Find the stability plot (`output/03_stability.png`) and the eigenvalue computation in the code.

**Checkpoint:** Open `output/03_stability.png`. Describe what you see. Are all points inside the unit circle? How many are at or near 1.0?

---

### Validation Test 3: Rank Sensitivity

**What it tests:** Does your main result change if you use rank 2 instead of rank 1?

**How to test:** Change `coint_rank` in the code and rerun. Compare FEVD tables. If the US FFR → HIBOR share at h=8 changes from 75% to 40%, your result is sensitive. If it stays near 75%, it's robust.

**Checkpoint:** Manually modify the VECM call to force rank=2. Rerun. What changes in the FEVD table? Write a two-sentence summary.

---

### Validation Test 4: Ordering Sensitivity

**What it tests:** Does changing the Cholesky ordering materially change your IRFs and FEVD?

**Your code already does this:** Look at `output/09_ordering_robustness.png`. This chart runs the model with alternative variable orderings and overlays the IRFs.

**What robust means:** The sign and rough magnitude of the main results should not flip with alternative orderings. If they do, the model is over-identified by the ordering assumption — the story depends on an untestable structural assumption.

**Checkpoint:** Look at `output/09_ordering_robustness.png`. Describe: does the US FFR → HIBOR transmission direction flip in any ordering? Does the magnitude change substantially?

---

### Validation Test 5: Subsample Stability

**What it tests:** Does the model give consistent results across different time periods? If the HK-China channel was weak pre-2003 and strong post-2003, a full-sample FEVD averages across a structural change and is misleading.

**Your code:** Look at `output/10_subsample_stability.png`.

**Checkpoint:** Does the China GDP → HK GDP growth FEVD share look similar in the first half vs second half of the sample? Write one sentence on what you see.

---

## Phase 4 — Updating the Model (Ongoing)

**Objective:** Own the update workflow. When new data arrives or you change a specification, run through this checklist.

### The Update Protocol (run in this order)

**Step 1: Fetch new data**
```bash
python fetch_real_data.py
```
Check that the new quarter's data loaded correctly. Open `data/hk_macro_quarterly_real.csv` and verify the last row.

**Step 2: Re-run stationarity tests**  
After adding new data, unit root status can technically change (especially for borderline series). Check that the same variables are still flagged as I(1). If status changes, document why.

**Step 3: Re-run lag selection**  
BIC optimal lag can shift as the sample grows. With n=112 it's very likely still VAR(1), but check:
```bash
MPLCONFIGDIR=/tmp/mpl_cfg python hk_var_model.py --lag-criterion bic --model-type var
```
Check `output/model_diagnostics.txt` for `bic_lag`.

**Step 4: Re-run Johansen test**  
Rank should still be 1. If it shifts to 0 or 2, that's news — document it and investigate before proceeding.

**Step 5: Rerun VECM**
```bash
MPLCONFIGDIR=/tmp/mpl_cfg python hk_var_model.py --include-property --model-type vecm --lag-criterion bic
```

**Step 6: Check diagnostics**  
Compare new `output/vecm_diagnostics.txt` and `output/model_diagnostics.txt` to prior run. Specifically:
- Did residual autocorrelation get worse or better?
- Did eigenvalue stability hold?
- Did FEVD shares shift materially (> 5 percentage points)?

**Step 7: Run tests**
```bash
python -m pytest tests/ -q --tb=short
```
All should pass.

**Step 8: Update CLAUDE.md**  
Log the date, the BIC lag, the Johansen rank, and any FEVD changes.

### The Respecification Protocol

When you want to try a different spec (different lag, deterministic term, or ordering), always do this:

1. Run baseline → note key FEVD numbers (US FFR → HIBOR, China GDP → GDP growth)
2. Change one thing only
3. Rerun → compare FEVD numbers
4. Document the delta: "Changing lag from 1 to 2 moves US FFR → HIBOR from 75.8% to X%"
5. Decide: is the change economically meaningful, or is it noise?

**Never change two things at once.** You won't know which change caused the difference.

---

## Checkpoint Master List

At the end of Phase 4, you should be able to answer all of these without notes:

| # | Question |
|---|---------|
| 1 | Why did BIC select VAR(1) over AIC's VAR(8)? |
| 2 | Which series are I(1) in your model and how do you know? |
| 3 | What does Johansen rank = 1 mean economically? |
| 4 | Why is FFR ordered first and HIBOR last? |
| 5 | What does the Ljung-Box test tell you and which equations fail? |
| 6 | What is the error correction term in a VECM and what does α measure? |
| 7 | What does FEVD tell you that OLS regression does not? |
| 8 | What is an IRF and what does "at horizon h=4" mean? |
| 9 | What happens to your main result if rank = 2? |
| 10 | What is the first thing you check when new quarterly data arrives? |

---

## NotebookLM Strategy

Upload these documents as one source group in NotebookLM:

**Week 1 (economic context):** HKMA RM 11/2018, Genberg et al. (2006), Chen & Tsang (2020)  
**Week 2 (statistics):** Johansen (1991) intro + Section 2, Engle-Granger (1987) intro, Sims (1980) intro  
**Week 3 (validation):** Giacomini-White (2006) intro, Clark-McCracken (2001) intro  

Ask NotebookLM to generate: "Explain how a Vector Error Correction Model differs from a VAR, and why cointegration matters for macro forecasting." Use the audio overview as listening material while commuting.

Do not upload the advanced readings yet. Save those for Phase 3–4 when you hit specific diagnostic problems.

---

## One Non-Negotiable Rule

Every time you run the model, read the diagnostics file before looking at the charts. The charts tell you the story. The diagnostics tell you whether you're allowed to tell that story.
