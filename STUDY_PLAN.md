# Study Plan — Hong Kong VARX: Own the Model

**Goal:** Move from AI-generated VECM to a validated, understood VARX you can defend.
**Status updated:** 2026-05-20

---

## What We Found (Audit Summary)

Before continuing, here is what the hands-on audit established:

| Finding | Status |
|---|---|
| `china_gdp` is I(0), not I(1) — model was wrong | CONFIRMED |
| Johansen rank fragile — rank=0 at 95%, rank=1 only at 90%/det_order=1 | CONFIRMED |
| VECM has no valid statistical foundation | CONFIRMED → DROP VECM |
| VARX is correct — us_ffr and china_gdp are exogenous by LERS | CONFIRMED |
| No financial channel variable exists back to 1998 (BIS suppressed pre-2014) | CONFIRMED → DOCUMENT GAP |
| Residual autocorrelation in 4/8 equations | PRE-EXISTING → fix in VARX |

---

## Phase 0 — Economic Context ✓ DONE

NotebookLM audio generated. PDFs uploaded. Chen & Tsang (2020), HKMA RM 11/2018, Genberg et al. (2006) loaded.

---

## Phase 1 — Statistical Foundations ✓ DONE

All three concepts completed through hands-on notebook work (TEST.ipynb).

### Concept A: Stationarity ✓
- Ran ADF on all variables manually
- Found `china_gdp` is I(0) — model error confirmed
- Learned: being a "rate" doesn't guarantee stationarity
- Confirmed I(1): `hk_property_price_idx` (p=0.8215), `cpi_inflation` (p=0.1526), `unemployment` (p=0.0821)

### Concept B: BIC vs AIC ✓
- Ran `model.select_order(maxlags=8)`
- BIC=1, AIC=8 — tension understood
- VAR(1) is parsimonious but may miss longer monetary policy lags

### Concept C: Johansen Cointegration ✓
- Ran corrected Johansen (3 true I(1) variables, without `china_gdp`)
- det_order sensitivity: rank=0 at all specs at 95%; rank=1 only under det_order=1 at 90%
- VECM foundation is fragile → dropped

---

## Phase 2A — VARX Built by AI ✓ (2026-05-21)

Code is in `TEST.ipynb` Phase 2 section. Bugs found and fixed, results recorded. Full details in `07_varx_build_phase2_findings.md`.

**Key results reference:**

| Check | Result |
|---|---|
| BIC lag | 1 (AIC also 1) |
| Residual autocorrelation | 3/6 fail: gdp_growth, cpi_inflation, hk_property_price_idx |
| us_ffr → hibor_3m | +0.508 ✓ LERS |
| china_gdp → hk_exports_china_yoy | +1.163 ✓ trade channel |
| us_ffr → hk_property_price_idx | -0.737 ✓ rate channel |

---

## Phase 2B — Run It Yourself ✓ DONE (2026-05-22)

**Objective:** Open `TEST.ipynb`. Run each Step cell yourself. After each one, answer the question below before moving on. You are not done until you can answer without looking.

---

### Step 1 — Data load + lag selection

Run the cell. Output should say `n=112 obs, 8 columns`.

**Answer before moving on:**
- Why can't you call `.dropna()` on the full 26-column CSV?
- Why is `maxlags=2` the ceiling, not 4 or 8?
- BIC selected lag=__. Why no BIC/AIC tension this time (there was in Phase 1)?

---

### Step 2 — Fit VARX

Run the cell. A long summary table prints. Skim it — you don't need to read every coefficient.

**Answer before moving on:**
- What does it mean that `us_ffr` and `china_gdp` appear in the model but are NOT endogenous?
- How many equations are being estimated? How many parameters per equation at lag=1?

---

### Step 3 — Ljung-Box residual diagnostics

Run the cell. Three equations should say FAIL.

**Answer before moving on:**
- What is the Ljung-Box test actually checking? (What is the null hypothesis?)
- Which 3 equations fail?
- Why does this force you to use bootstrap CIs instead of asymptotic ones?

---

### Step 4 — Exogenous transmission (LERS + trade channel)

Run the cell. Find the `us_ffr → hibor_3m` and `china_gdp → hk_exports_china_yoy` coefficients.

**Answer before moving on:**
- What sign did you expect for `us_ffr → hibor_3m`, and why? (One sentence: LERS.)
- What sign did you expect for `china_gdp → hk_exports_china_yoy`, and why?
- What does `us_ffr → gdp_growth = +0.448` mean, and why is it unexpected?
- Why is this table (Step 4) your primary evidence for LERS — not the FEVD you'll run in Step 6?

---

### Step 5 — IRF plot

Run the cell. Opens `output/phase2_irf.png`.

**Answer before moving on:**
- What does an IRF at h=4 actually represent? (Complete sentence.)
- Find the panel for `hibor_3m` shock → `hk_property_price_idx` response. What sign is it? Does that match the rate channel story?
- Why do `cpi_inflation`, `unemployment`, and `hk_property_price_idx` responses look permanent instead of decaying to zero?
- Why does this IRF plot NOT show what happens after a `us_ffr` shock?

---

### Step 6 — FEVD

Run the cell. A table prints for each equation at h=1 through h=8.

**Answer before moving on:**
- What does FEVD tell you that OLS cannot? (One sentence.)
- At h=8, what fraction of `hk_property_price_idx` variance is explained by `hibor_3m`? By `gdp_growth`? By own shock?
- HIBOR's own shock explains 78% of its forecast variance. Does this mean FFR doesn't matter for HIBOR? Why not?
- Why don't `us_ffr` and `china_gdp` appear anywhere in the FEVD output?

---

**Phase 2B is done when:** You can answer every question above from memory in under 2 minutes each. Then mark Phase 2 complete and move to Phase 3.

---

## Phase 3 — Validate the Results ← CURRENT

**Objective:** Confirm you are *allowed* to tell the story the FEVD suggests. Each validation either strengthens the result or forces a caveat.

---

### Validation 1: Autocorrelation — before vs after

Already done. Record the table and write one sentence: what improved, what persists, and what it forces you to do (bootstrap).

**Pass condition:** You can state the before/after counts and explain why the persisting failures don't invalidate the results, just change the CI method.

---

### Validation 2: Cholesky ordering sensitivity

Swap `hibor_3m` and `unemployment` in the endogenous list and rerun FEVD.

```python
# Swap ordering: put unemployment before hibor
endog_cols_alt = ['hk_exports_china_yoy', 'gdp_growth', 'cpi_inflation',
                  'hibor_3m', 'unemployment', 'hk_property_price_idx']
endog_alt = df[endog_cols_alt]
model_alt = VAR(endog_alt, exog=exog)
results_alt = model_alt.fit(maxlags=1)
fevd_alt = results_alt.fevd(periods=8)
print(fevd_alt.summary())
```

**Record:** hibor share in hk_property_price_idx at h=8 under original ordering vs swapped ordering.

**Pass condition:** If the share stays within ~3pp, result is robust. If it moves >5pp, that's a caveat to document.

---

### Validation 3: Bootstrap confidence intervals on IRFs

Asymptotic CIs are invalid when residual autocorrelation exists. Replace with Monte Carlo bootstrap.

```python
irf = results.irf(periods=8)
fig = irf.plot(orth=True, stderr_type='mc', repl=1000)
fig.savefig('output/phase3_irf_bootstrap.png', dpi=100, bbox_inches='tight')
```

**Record:** Does the `hibor_3m` → `hk_property_price_idx` IRF still have a clearly negative band at h=2–4? Or does zero sit inside the CI?

**Pass condition:** Negative sign survives bootstrap at h=2. If not, the rate channel story needs a caveat.

---

### Validation 4: VARX(1) vs VARX(2) sensitivity

Refit at lag=2. Compare the two FEVD tables at h=8.

```python
results2 = model.fit(maxlags=2)
fevd2 = results2.fevd(periods=8)
print(fevd2.summary())
```

**Record:** For each key cell (hibor→property, exports→gdp, gdp→cpi), how many percentage points does the share change between lag=1 and lag=2?

**Pass condition:** If no key cell changes by more than 5pp, report lag=1 (BIC choice) as robust. If a cell shifts materially, report both and note sensitivity.

---

## Phase 4 — Write the Research Note

**Structure:**
1. Research question and institutional context (LERS, currency board)
2. Data and variable description — include stationarity table
3. Model: VARX specification, Cholesky ordering with justification
4. Results: FEVD table + IRF signs for 2 key channels
5. Limitations: residual autocorrelation, rank fragility, financial channel gap, FFR as proxy

**Limitations paragraph (draft):**
> "Several limitations apply. First, residual autocorrelation persists in [N] of 6 endogenous equations, suggesting the model misses higher-frequency dynamics; bootstrap confidence intervals are used throughout. Second, no publicly available quarterly proxy for inbound China–HK financial flows exists back to 1998 — BIS Locational Banking Statistics suppress the China counterparty series before 2014 — so the model captures the China real-activity channel but not the financial channel dominant post-2010. Third, us_ffr is a monetary-conditions proxy, not a clean policy surprise. Fourth, VAR(1) lag may miss longer monetary transmission lags known to extend 4–8 quarters."

---

## Checkpoint Master List (Updated)

| # | Question | Status |
|---|---|---|
| 1 | Why did BIC select VAR(1) over AIC's VAR(8)? | ✓ Can answer |
| 2 | Which series are I(1) and how do you know? | ✓ Can answer |
| 3 | Why is `china_gdp` treated as exogenous, not endogenous? | ✓ Can answer |
| 4 | Why is FFR ordered first? | ✓ Can answer (LERS) |
| 5 | What does the Ljung-Box test tell you? Which equations fail? | ✓ Can answer |
| 6 | Why was VECM dropped? | ✓ Can answer |
| 7 | What does FEVD tell you that OLS does not? | ✓ Can answer |
| 8 | What is an IRF at horizon h=4? | ✓ Can answer |
| 9 | Why is there no financial channel variable? | ✓ Can answer |
| 10 | What is the first thing you check when new data arrives? | Phase 4 |
