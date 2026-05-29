# Study Plan — Hong Kong Macroeconomic Transmission (VARX / BVAR / VECM)

**Goal:** Produce a validated, defensible empirical study of monetary and trade transmission in Hong Kong, following Prof. K. Lai's advice received 2026-05-23.
**Status updated:** 2026-05-24

---

## Prof. Lai's Guidance (received 2026-05-23)

Two directions that reshape the remaining work:

1. **VECM as robustness.** "Since the evidence is considered marginal, you may want to do both VECM and VAR specifications, and see if you can obtain similar or rather different results. You may treat this as a robustness check."

2. **Longer sample first.** "I think you can use the longer sample period first, and then repeat the analysis using the post-1997 period as a robustness check."

These two instructions define the new phase structure below.

**Note on BVECM (added 2026-05-24):** The alexandria library has a `VectorErrorCorrection` class that supports Bayesian estimation via `prior_type` (1=uninformative, 2=horseshoe, 3=selection). However, **BVECM is not pre-committed**. The Minnesota BVAR is purpose-built for small samples (Litterman 1986) and the forecasting literature finds that BVAR in levels often beats VECM even under genuine cointegration, because rank misspecification risk typically dominates the efficiency gain from imposing a correct cointegrating restriction (Clements & Hendry 1998; Christoffersen & Diebold 1998). Our current Johansen result — rank=0 at 95%, rank=1 only at 90% — puts us squarely in the rank-uncertain zone where this risk is highest. **BVAR(4) remains the preferred spec.** Frequentist VECM runs as robustness per Prof. Lai. BVECM is only considered if the extended-sample Johansen test gives clean rank ≥ 1 at 95% (see Phase 8.4b).

---

## Completed Phases (do not expand)

- **Phase 0** — Economic context (LERS, currency board, China trade channel). ✓ DONE
- **Phase 1** — Stationarity (ADF), lag selection (BIC vs AIC), Johansen cointegration. ✓ DONE
- **Phase 2A** — VARX baseline built by AI; bugs found and fixed. ✓ DONE
- **Phase 2B** — Student reproduced the code and ran it independently. ✓ DONE
- **Phase 3** — VARX(1) validated and locked: Ljung-Box, bootstrap IRFs, Chow test (2008, 2020), exog coefficients confirmed. ✓ LOCKED
- **Phase 4** — BVAR(4) with Minnesota prior (pi1=0.085, pi2=1.0, pi3=1, ML-optimized); IRF and FEVD comparison vs VARX(1). ✓ COMPLETE
- **Phase 5** — BVAR validation: hyperparameter grid, posterior verification (analytical draws — not MCMC), in-sample fit (R²), OOS expanding-window (RMSE ratio: BVAR wins 15/18 cells). ✓ COMPLETE

Full evidence trail: `TEST.ipynb` cells 37–56. Lesson files 01–20 in the lessons vault.

---

## Phase 6 — Code Verification ✓ COMPLETE (2026-05-25)

- **6.1** Monkey-patch confirmed targeted — replaces broken `exogenous == []` numpy comparison, does not alter inference logic.
- **6.2** OOS loop re-run: training window expands t=85→111, no look-ahead, 15/18 BVAR wins confirmed.
- **6.3** RMSE ratio = RMSE(BVAR)/RMSE(VARX1) — not Theil's U. Ratio < 1 = BVAR beats VARX(1).
- **6.4** No burn-in applies. Minnesota BVAR with fixed Σ has closed-form Normal posterior; alexandria draws analytically (i.i.d.), no Markov chain exists.
- **6.5** pi4=100 (library default, uninformative on exogenous — correct for small open economy). pi2=0.5 sensitivity: BVAR wins 18/18. Results robust.

---

## Literature Sprint (between Phase 6 and Phase 7)

**Why this exists:** Three specific gaps emerged from the code review and methodology discussion that must be read before the extended-sample estimation. All are short and targeted — this is not a full literature review, it is just-in-time reading for known gaps. Each item is tied to a specific decision in Phase 7 or Phase 8.

**Rule:** Read in order. Each item has a pass condition — a one-sentence answer you should be able to write from memory after reading. Write it in the reading list or a notebook cell when done.

---

**LS.1 — Giannone, Lenza & Primiceri (2015)** — *Review of Economics and Statistics*, 97(2), 436–451
Already on reading list. Read before Phase 6.5 hyperparameter documentation.
- Why: Their simultaneous ML optimization of all hyperparameters (pi1, pi2, pi3, pi4) is exactly what the alexandria optimizer does. Their Table 1 reports pi2 ≈ 1.0 in US quarterly data — the direct precedent for your pi2=1.0 result.
- What to extract: one sentence explaining why pi2=1.0 is defensible for HK quarterly data, citing GLP.
- Pass condition: You can state what GLP found for pi2 and why the same logic applies here.

---

**LS.2 — Bai & Perron (2003)** — "Computation and Analysis of Multiple Structural Change Models," *Journal of Applied Econometrics*, 18(1), 1–22
Read/skim during Phase 7 data pull (background reading while waiting for data).
- Why: The Chow test is correct for the known 1997 break. But Bai-Perron is the framework a referee will cite if they ask "did you search for breaks systematically?" You need to know what it does so you can explain why Chow was sufficient for 1997 but Bai-Perron would add value for unknown breaks.
- What to extract: one sentence distinguishing Chow (known date) from Bai-Perron (unknown date) in your own words.
- Pass condition: You can explain to Prof. Lai why you used Chow at 1997 and what Bai-Perron would add.

---

**LS.3 — Johansen (1991), Section 2 only** — *Econometrica*, 59(6), 1551–1580
Read before writing any Phase 8 VECM code. Not before Phase 7.
- Why: You will produce a VECM error-correction coefficient. Without understanding what that coefficient means economically — the speed at which the system corrects back to the long-run equilibrium — you cannot interpret the result. This is the specific failure mode the council identified.
- What to extract: what does the adjustment coefficient α mean? If HIBOR deviates from its long-run relationship with FFR, what does α tell you about how fast it corrects?
- Pass condition: You can answer "what does the error-correction coefficient in the HIBOR equation mean for the LERS peg?" without looking it up.

---

**LS.4 — Cushman & Zha (1997)** — "Identifying Monetary Policy in a Small Open Economy Under Flexible Exchange Rates," *Journal of Monetary Economics*, 40(3), 731–768. **Skim abstract and Section 2 only.**
- Why: This is the canonical reference for treating foreign variables as exogenous in a small open economy VAR — the BVARX justification. A referee who asks "why are us_ffr and china_gdp exogenous?" expects this citation.
- What to extract: one sentence: the block-recursive structure treats foreign-block variables as contemporaneously exogenous to the domestic block.
- Pass condition: You can name the paper and state its argument in one sentence.

---

**Literature Sprint pass condition (overall):** All four pass-condition sentences written. LS.1 and LS.4 must be done before Phase 6.5. LS.2 can be done during Phase 7. LS.3 must be done before Phase 8.4.

---

## Phase 7 — Sample Extension: Data Pull and Stationarity Audit

### 7.1 — Pull extended data ✓ COMPLETE (2026-05-25)

Data availability research conducted. Findings:

| Variable | Earliest available | Binding? |
|---|---|---|
| us_ffr | 1954 | No |
| china_gdp (OECD QNA) | 1992 Q1 | No |
| hk_exports_china_yoy | ~1990 Q1 | No |
| gdp_growth | 1980 Q1 | No |
| cpi_inflation | 1980 Q4 | No |
| unemployment | 1981 Q4 | No |
| **hibor_3m** | **1994 Q1 (period avg) / 1996 Q3 (formal fixing)** | **YES** |
| hk_property_price_idx | 1979 Q4 | No |

**Binding constraint: HIBOR at 1994–1996.** Maximum gain = 6–16 quarters.

**Council verdict (2026-05-25): Keep 1998 Q1. Do not extend.** See Lesson 21.

Reasons: (1) Institutional boundary — LERS credibility only stabilized post-1998 HKMA interventions. Pre-1997 is a different monetary regime. (2) Cost asymmetry — wrong inclusion biases every IRF/FEVD; wrong exclusion loses 6–16 obs. Error (b) >> Error (a). (3) Chow test has near-zero power with 6–16 pre-break obs — "run Chow first" is epistemically circular. (4) HIBOR instrument continuity across 1997 handover unverified — may be a different fixing panel/methodology.

**Prof. Lai's "longest sample first" correctly applied:** 1998 Q1–2026 Q1 IS the longest credible sample for this mechanism. Post-1997 HK is the correct institutional scope. The current dataset is not shortchanging the sample — it is correctly scoping the monetary transmission mechanism under the LERS.

**Phases 7.2 and 7.3 restructured accordingly — see below.**

### 7.2 — I(1) candidate set for VECM ✓ COMPLETE (2026-05-27)

Full ADF+KPSS battery on all series. I(1) confirmed: unemployment, cpi_inflation, hk_property_price_idx (3 series). gdp_growth confirmed I(0) — YoY MA(3) bias resolved by KPSS. Δu robustness check run and PASSED — headline IRFs unchanged. Keep unemployment in levels.

See Lessons 22, 23. Output: `output/phase7_unemployment_robustness.png`. Code: TEST2.ipynb cells 1–5.

### 7.3 — Verify HIBOR instrument continuity at 1997 (new — from council blind spot)

Before permanently closing the extension question: confirm whether pre-1997 and post-1997 HIBOR are the same institutional instrument (same HKMA panel, same fixing definition). One source lookup. If instrument changed at handover, the extension question is closed permanently.

**Pass condition:** One sentence confirming HIBOR instrument continuity or discontinuity at 1997.

---

## Phase 8 — Primary Estimation on Longest Available Sample

**Why longest sample is primary:** Prof. Lai's preference. Longer samples give better-estimated long-run dynamics and more power for cointegration tests. The post-1997 sample becomes robustness, not the main result.

**Objective:** Re-estimate VAR, BVAR, and VECM on the extended sample. Estimate VAR and VECM in parallel during Phase 8; VECM serves as the robustness specification per Prof. Lai's guidance.

**Literature basis:** BVAR specification follows Litterman (1986) and Banbura, Giannone & Reichlin (2010). VECM setup follows Johansen (1991). The BVAR-vs-VECM forecasting framing is grounded in Christoffersen & Diebold (1998) and Clements & Hendry (1998). Hyperparameter re-optimization on the new sample follows Carriero, Clark & Marcellino (2015).

### 8.1 — Re-run lag selection and BIC

BIC-optimal lag may differ on a longer sample. Re-run `model.select_order()` on the extended dataset. Do not assume lag=1 carries forward.

**Pass condition:** Updated BIC/AIC table. New BIC lag choice documented.

### 8.2 — VAR/VARX on extended sample

Refit the VARX specification using the extended data. Exogenous treatment of `us_ffr` and `china_gdp` is unchanged — LERS and small-open-economy logic still apply.

Run Ljung-Box diagnostics. Run Chow tests at 1997, 2008, and 2020. Run bootstrap IRFs. Produce FEVD table.

**Pass condition:** Full diagnostics documented. Key transmission channels (us_ffr→hibor, china_gdp→exports, hibor→property, exports→gdp) reported with CIs.

### 8.3 — BVAR on extended sample

Refit BVAR with Minnesota prior using the extended data. Re-run the ML hyperparameter optimization (pi1, pi2) — optimal shrinkage will likely change with more data and potentially different dynamics pre-1998.

**Pass condition:** Updated (pi1, pi2) from ML grid. OOS Theil-U table re-run on extended sample expanding window. BVAR vs VAR comparison updated.

### 8.4 — Johansen test and VECM ✓ COMPLETE (2026-05-27)

**Run on current (1998 Q1) sample** — extended sample not available (Phase 7.1 verdict: keep 1998 Q1).

Johansen on endogenous I(1) block only (unemployment, cpi_inflation, hk_property_price_idx). **Rank=0 at 95%, both trace and max-eigenvalue tests.** VECM not warranted.

Key lessons:
- `hk_var_model.py` ran Johansen on all 7 variables including exogenous — WRONG, produced spurious rank=1
- HIBOR-FFR moving together is LERS peg mechanics, not equilibrium cointegration
- Rank=0 validates the BVAR-in-levels specification (BVAR wins even under genuine cointegration per Clements & Hendry 1998)

See Lesson 24. Paper sentence written in CLAUDE.md Phase 8.4 section.

### 8.4b — BVECM (conditional — run only if Phase 8.4 Johansen gives rank ≥ 1 at 95%)

**Condition to proceed:** Johansen trace AND max-eigenvalue both support rank ≥ 1 at the 95% level on the extended sample. If either test fails to reject rank = 0 at 95%, skip this step entirely. Document the skip decision.

**If condition is met:** Estimate BVECM using the alexandria `VectorErrorCorrection` class. Use `prior_type=1` (uninformative) as the baseline, then check sensitivity to `prior_type=2` (horseshoe). Literature basis: Strachan (2003) and Koop & Korobilis (2010). Compare BVECM IRFs against BVAR(4) on the same extended sample.

**Pass condition:** BVECM estimated, prior sensitivity reported, and IRF comparison table produced. OR: skip decision documented with Johansen results confirming rank = 0 at 95%.

### 8.5 — Structural break assessment on extended sample

Synthesize: if Chow tests show a break at 1997, the full sample model has a known structural instability. This does not invalidate the estimation, but it must be acknowledged as a limitation and motivates the Phase 9 post-1997 robustness check.

**Pass condition:** One-paragraph written summary: which breaks were found, what they imply for inference, and how Phase 9 addresses them.

---

## Phase 9 — Post-1997 Robustness Check

**Why this is robustness, not primary:** Prof. Lai's logic is "longer sample first, post-1997 as robustness." The current dataset (1998Q2–2026Q1) corresponds approximately to this window. Phase 9 confirms whether the extended-sample results hold when you condition on the post-handover regime.

**Objective:** Re-run the full Phase 8 estimation suite on the post-1997 sample. Compare results systematically.

### What to run

Repeat 8.1 through 8.4 on the post-1997 sample. Use the same model specs (lag choice, prior hyperparameters, Cholesky ordering) as Phase 8 to keep the comparison clean. Deviations are permitted only where the data requires it (e.g., if BIC selects a different lag on the shorter sample — record it).

### What to compare

Build a robustness matrix:

| Result | Extended sample | Post-1997 sample | Verdict |
|---|---|---|---|
| BIC lag | | | |
| Johansen rank | | | |
| us_ffr → hibor coef | | | |
| china_gdp → exports coef | | | |
| hibor → property IRF sign at h=2 | | | |
| exports → gdp IRF sign at h=2 | | | |
| BVAR Theil-U vs VAR | | | |

A result is robust if it holds in sign and rough magnitude in both samples. A result that flips in sign or loses significance in one sample is a caveat, not a failure — document it honestly.

**Pass condition:** Robustness matrix completed. Each row has a written verdict (robust / sensitive / null in both).

---

## Phase 10 — Synthesis

**Why a dedicated synthesis phase:** After running four model variants (VAR and VECM) on two samples (extended and post-1997), you need to step back and state what the evidence collectively says — before writing a paper. Synthesis is an analytical act, not the same as writing.

**Objective:** Consolidate results into a single narrative: what transmission channels are robust, what is sample-sensitive, and what the VECM comparison adds or subtracts.

### Deliverable

A written synthesis note (can live in a notebook cell or a short `.md`) covering:
1. The headline findings that survive both samples and both specifications.
2. Results that are model-sensitive (VAR finds it, VECM does not, or vice versa) — and why.
3. Results that are sample-sensitive (pre-/post-1997 differ) — and why.
4. Limitations that survive into the final paper: BIS data gap, structural breaks, FFR as proxy, linear fixed-coefficient model.
5. Whether VECM adds substantive new information or merely corroborates (or contradicts) VAR.

**Pass condition:** Synthesis note complete and internally consistent. No contradictions between stated findings and diagnostic results.

---

## Phase N — Paper (TBD)

**Held until Phase 10 is complete.** Paper structure depends on what the robustness matrix shows. If VAR and VECM give similar results, the paper frames them as convergent evidence. If they diverge, the paper must explain why.

Tentative structure (to be finalized in Phase 10):
1. Introduction and research question
2. Institutional context: LERS, currency board, China trade channel
3. Data: variable dictionary, stationarity table, sample periods
4. Methodology: VARX/BVAR specification, Cholesky ordering, VECM setup
5. Results: primary (extended sample) and robustness (post-1997, VAR vs VECM)
6. Discussion: what the evidence says about transmission channels
7. Limitations
8. Conclusion

---

## Open Risks (carry forward into each phase)

| Risk | Implication |
|---|---|
| BIS suppresses China counterparty pre-2014 | No financial channel variable on any sample — document as limitation |
| C&SD methodology may change around 1997 handover | Check data notes before committing to a pre-1997 start |
| VECM may fail Johansen rank on extended sample | Report null result; do not silently drop |
| Structural breaks at 1997, 2008, 2020 | Linear fixed-coefficient model cannot span all regimes; acknowledge throughout |
| Alexandria library monkey-patch | Phase 6 gate must sign off before any new BVAR estimation |
