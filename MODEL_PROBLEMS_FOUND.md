# Model Problems Found — Hands-On Audit + Council Verdict
Date: 2026-05-20

---

## Problem 1: `china_gdp` Misclassified as I(1) — CONFIRMED, NOT AN ARTIFACT

**Source verified:** OECD QNA CHN.B1_GE.GPSA.Q, seasonally adjusted, GY transformation (YoY % growth). Genuine quarterly data — NOT interpolated from annual. China NBS has published quarterly GDP since 1992.

**Finding:** ADF p=0.0003 → I(0). china_gdp is already a YoY growth rate (mean 8%, range -6.8 to 18.9%). The model first-differences it and includes it in the Johansen I(1) group. Both are wrong.

**Impact:** Inflated Johansen rank. Distorted VECM error correction term.

---

## Problem 2: Johansen Rank Was Inflated — CONFIRMED

Original model Johansen (4 variables including china_gdp wrongly): rank=1 at 90/95/99.

Corrected Johansen (3 true I(1) variables: hk_property_price_idx, cpi_inflation, unemployment):

| det_order | Rank at 90% | Rank at 95% |
|---|---|---|
| -1 | 0 | 0 |
| 0 | 0 | 0 |
| 1 | 1 | 0 |

Rank=1 only under the most permissive spec at 90%. Not robust. VECM has no valid statistical foundation.

---

## Problem 3: Residual Autocorrelation — PRE-EXISTING

Ljung-Box p-values (lag=8), original VECM:
- hk_exports_china_yoy: p=0.0082 → FAIL
- hk_property_price_idx: p=0.0105 → FAIL
- gdp_growth: p=0.0000 → FAIL
- cpi_inflation: p=0.0006 → FAIL
- us_ffr: p=0.9735 → pass
- hibor_3m: p=0.7182 → pass

**This is the primary diagnostic gate.** IRF confidence bands and FEVD standard errors are unreliable in the 4 failing equations. Must be tested in VARX before any results are interpreted.

---

## Problem 4: us_ffr and china_gdp Should Be Exogenous — COUNCIL VERDICT: CONFIRMED

HK cannot move US rates (LERS/currency board) or China growth (small open economy). Standard VAR allows lagged HK variables to feed back into both — economically wrong. Cholesky only fixes contemporaneous feedback.

**Correct specification: VARX** with us_ffr and china_gdp as strictly exogenous regressors.

---

## Problem 5: Financial Channel Gap — CONSTRUCT VALIDITY PROBLEM

Post-2010, China-HK transmission is primarily financial: HKEX listings, Stock Connect (est. 2014), mainland capital flows into HK property. hk_exports_china_yoy measures a declining trade channel.

**HSCEI is NOT a valid proxy:** stock index constituents rotate, and it measures Chinese equity market performance in HK — not how China growth transmits to HK domestic economy (GDP, unemployment, CPI).

**Council verdict:** Bound all China transmission claims to the trade channel for this note. Name the financial channel gap explicitly in the limitations section as the primary scope boundary. Leave HSCEI or capital flow data as the named next extension.

---

## Stationarity Audit Results

| Variable | ADF p (level) | I(?) | Model was | Verdict |
|---|---|---|---|---|
| china_gdp | 0.0003 | I(0) | I(1) | **Model wrong** |
| cpi_inflation | 0.1526 | I(1) at 5% | I(1) | Correct |
| unemployment | 0.0821 | I(1) at 5% | I(1) | Defensible |
| hk_property_price_idx | 0.8215 | I(1) | I(1) | Correct |
| us_ffr, gdp_growth, hk_exports_china_yoy, hibor_3m | — | I(0) | I(0) | Correct (model) |

---

## Council Verdict: What to Do

**Drop VECM.** Run VARX:
- Exogenous: us_ffr, china_gdp
- Endogenous: hk_exports_china_yoy, gdp_growth, cpi_inflation, unemployment, hibor_3m
- Lag: BIC between 1 and 2; bump to VARX(2) if autocorrelation persists at lag 1
- Standard errors: bootstrap CIs on all IRFs and FEVDs (not asymptotic, given autocorrelation history)
- Cholesky ordering within the 5 endogenous variables: needs explicit economic justification

**Research note story:**
- US monetary conditions transmit to HK through HIBOR and unemployment (LERS channel)
- China growth transmits through trade-facing exports and real activity (trade channel)
- Post-2010 financial channel is documented scope limitation and named next extension

---

## Problem 6: No Financial Channel Variable Available — CONFIRMED CLOSED

**Attempted:** BIS LBS liabilities position (Chinese entities' funds in HK banks) — correct inbound direction.

**Result:** BIS suppresses China counterparty series before 2014. Only 48 quarters. Too short.

**Conclusion:** No clean quarterly proxy for inbound China→HK financial flows exists back to 1998. Document as limitations. Do not add anything.

---

## Final Decisions

**Drop:** VECM (rank=0 at 95%, no valid foundation)

**Build:** VARX
- Exogenous: `us_ffr`, `china_gdp`
- Endogenous: `hk_exports_china_yoy`, `gdp_growth`, `cpi_inflation`, `unemployment`, `hibor_3m`, `hk_property_price_idx`
- Lag: BIC 1 or 2; bump to VARX(2) if autocorrelation persists
- CIs: bootstrap throughout

**Do not:**
- Extend sample to 1990
- Add HSCEI or any financial variable (data doesn't exist pre-2014)
- Keep VECM as headline
