# Implementation Plan: HK VAR Model — From Tool to Paper

## Situation Assessment

**What we have:** A mathematically verified VAR/BVAR pipeline with 16 audit issues fixed,
53 unit tests passing, automated diagnostics, and scenario forecasting — all running on
**synthetic data**.

**The problem:** The model is a tool, not a finding. Three blockers prevent any
serious use (academic or policy):

1. **No real data** — synthetic results are unpublishable and unactionable
2. **No structural analysis** — missing FEVD and historical decomposition, which are
   the outputs that produce economic narratives
3. **No robustness** — single ordering, no sub-sample stability, no model comparison

## Constraints

- Data: HK quarterly macro series are publicly available from C&SD, HKMA, FRED, and
  the World Bank. No proprietary access required.
- Tooling: Python + statsmodels + numpy. No new dependencies beyond `requests` for
  data fetching.
- Scope: One self-contained research question, not a survey of all HK macro topics.
- Timeline: Each phase should be independently runnable and testable.

## Recommended Research Question

> **"How do US monetary policy shocks and China growth shocks propagate to
> Hong Kong's real economy under the currency board?"**

This question exploits the unique institutional feature (the peg) to answer something
that cannot be answered for most economies. It is empirically tractable with the
existing 6-variable system and produces clear policy relevance for HKMA.

---

## Phase 1: Real Data Ingestion (CRITICAL — everything depends on this)

**Goal:** Replace synthetic data with actual HK quarterly macro series, 1998Q1–present.

| Task | Detail | Output |
|------|--------|--------|
| 1.1 Scrape/download FRED series | GDP: `NGDPRSAXDCHKQ`, CPI: `CPALCY01HKQ661S`, Unemployment: `LMUNRRTTHKQ156S`, FFR: `FEDFUNDS`, China GDP: `NGDPRSAXDCCNQ` | Raw CSVs in `data/raw/` |
| 1.2 Source HIBOR 3M | HKMA Monthly Statistical Bulletin or Bloomberg (if available); fallback: CEIC via API | `data/raw/hibor_3m.csv` |
| 1.3 Build data pipeline | Merge, align to QS frequency, compute YoY transforms per `DATA_SPEC`, handle missing values | Updated `assemble_data()` |
| 1.4 Write `data/hk_macro_quarterly_real.csv` | The canonical input file the model already expects | Verified CSV |
| 1.5 Validate | Run full pipeline on real data, compare summary stats to known HK macro facts | Sanity-checked output |

**Risk:** HIBOR 3M may require manual download or a paid API. Mitigation: the
FFR + spread proxy is documented and defensible for a first pass.

**Exit criteria:** `python hk_var_model.py` runs end-to-end on real data with no
synthetic fallback. Summary statistics match published C&SD / HKMA figures.

---

## Phase 2: FEVD and Historical Decomposition

**Goal:** Add the two analytical outputs that turn IRFs into economic stories.

| Task | Detail | Output |
|------|--------|--------|
| 2.1 Implement FEVD | From Cholesky IRFs: FEVD_h(i,j) = sum_{s=0}^{h} theta_{ij,s}^2 / MSE_h(i). Add `compute_fevd()` function. | `output/07_fevd.png`, `output/fevd_table.csv` |
| 2.2 Implement historical decomposition | Decompose each observed variable into the sum of contributions from each structural shock over the sample. | `output/08_hist_decomp.png` |
| 2.3 Add to main pipeline | Integrate into `estimate_model()` or as a post-estimation step. | Updated `main()` |
| 2.4 Unit tests | Verify FEVD sums to 1 at each horizon; historical decomp sums to actual values. | Tests in `tests/` |

**Mathematical specification:**

FEVD at horizon h for variable i due to shock j:
\[
\text{FEVD}_{i,j}(h) = \frac{\sum_{s=0}^{h} \theta_{ij,s}^2}{\sum_{s=0}^{h} \sum_{k=1}^{K} \theta_{ik,s}^2}
\]

Historical decomposition:
\[
y_t = \bar{y}_t^{\text{base}} + \sum_{j=1}^{K} \sum_{s=0}^{t} \Theta_s \, e_{j,t-s}
\]
where base path uses no shocks and each shock series contributes additively.

**Exit criteria:** FEVD chart shows which shocks drive HK GDP variance at 1Q, 4Q, 8Q.
Historical decomp correctly attributes GFC/COVID episodes to external shocks.

---

## Phase 3: Robustness and Ordering Sensitivity

**Goal:** Demonstrate results are not artifacts of a single specification.

| Task | Detail | Output |
|------|--------|--------|
| 3.1 Cholesky ordering permutations | Run IRF + FEVD under 3 orderings: (a) default external-first, (b) domestic-first, (c) size-based. Report max deviation. | `output/09_ordering_robustness.png` |
| 3.2 Sub-sample stability | Estimate on (a) pre-GFC, (b) post-GFC, (c) ex-COVID. Compare coefficient norms and IRF shapes. | `output/10_subsample_stability.png` |
| 3.3 VAR vs BVAR comparison | Formal comparison of out-of-sample RMSE, DM test if possible. | Updated backtest table |
| 3.4 Parameter-uncertainty bootstrap | Replace residual-only bootstrap with a pairs bootstrap or wild bootstrap that resamples both data and re-estimates parameters. | Updated CIs in `forecast_scenarios()` |

**Exit criteria:** A robustness table showing key results hold across orderings
and sub-samples, or clearly documenting where they don't.

---

## Phase 4: Paper Write-Up

**Goal:** Produce a draft paper (or thesis chapter) with complete results.

| Task | Detail | Output |
|------|--------|--------|
| 4.1 Introduction | Research question, contribution, preview of results | `paper/introduction.tex` |
| 4.2 Literature review | Position vs Genberg & He (2009), Funke & Paetz (2012), Li & Leung (2011) | `paper/literature.tex` |
| 4.3 Data and Model | Describe variables, transforms, estimation, identification | `paper/model.tex` |
| 4.4 Results | IRFs, FEVD, historical decomp, forecast evaluation, scenarios | `paper/results.tex` |
| 4.5 Robustness | Ordering sensitivity, sub-sample, VAR vs BVAR | `paper/robustness.tex` |
| 4.6 Conclusion | Key findings, policy implications, limitations | `paper/conclusion.tex` |
| 4.7 References | BibTeX file with all cited works | `paper/references.bib` |
| 4.8 Compile and review | `latexmk -pdf main.tex` | `paper/main.pdf` |

**Target venues (in order of fit):**
1. *Pacific Economic Review* — regional, accepts HK-specific empirical work
2. *Journal of Asian Economics* — broader scope, methodologically flexible
3. *International Journal of Forecasting* — if forecast accuracy is the main result

---

## Execution Order and Dependencies

```
Phase 1 (real data)
  ↓
Phase 2 (FEVD + hist decomp)  ←  can prototype on synthetic while Phase 1 in progress
  ↓
Phase 3 (robustness)          ←  requires real data from Phase 1
  ↓
Phase 4 (write-up)            ←  requires all results from Phases 1-3
```

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| HIBOR data unavailable for free | Medium | Medium | Use FFR + spread proxy, document as limitation |
| Real data shows structural break invalidating VAR | Medium | High | Add break dummies or Markov-switching extension |
| FEVD results trivial (one shock dominates) | Low | Medium | This is itself a finding; present honestly |
| Sub-sample instability | Medium | Medium | Document as limitation; consider time-varying parameter VAR |
| Johansen test finds cointegration on real data | Medium | High | Implement VECM as Phase 3.5 extension |

## Current File Map

```
Hong Kong/
├── hk_var_model.py          ← main model (1200 lines, audited + tested)
├── tests/
│   └── test_hk_var_model.py ← 53 tests (52 pass, 1 skip)
├── data/
│   └── hk_macro_quarterly.csv  ← synthetic (to be replaced in Phase 1)
├── output/                  ← charts, tables, reports
├── requirements.txt
└── README.md
```

**Recommended next action:** Start Phase 1 (real data). Everything else is blocked on it.
