# Full process archive (personal — internal log)

**For:** Steven only — not a polished deliverable for readers.  
**Purpose:** One place that records **everything** we built together: theme, motivation, data journey, methods, audits, git mess, and what’s actually next.  
**Explicitly out of scope here:** cover letters, journal formatting checklists, submission admin — that’s bureaucracy, not the research log.

---

## 1. Theme and why this exists

**Institutional hook:** Hong Kong runs a **currency board** (HKD pegged to USD). That means US monetary conditions import into HIBOR and local rates whether or not they match the domestic cycle. At the same time, Hong Kong’s real economy is tied to **mainland China** through trade, tourism, finance, and supply chains.

**Core tension (the idea):**  
- **Interest-rate channel:** anchored to the **US** (peg).  
- **Real activity channel:** heavily influenced by **China**.

**Purpose of the build:** Turn that story into a **repeatable empirical object** — not a one-off chart — so you can answer:

> *How do US monetary policy shocks and China growth shocks propagate to Hong Kong’s real economy under the currency board?*

That sentence became the **research question** written into the code header and the paper draft.

**Modeling choice:** A **quarterly VAR** (plus extensions below), not a DSGE. The goal was **transparent multivariate dynamics**, forecast error shares, and decomposition — something you can defend line-by-line in code and extend without a full macro lab.

---

## 2. What we actually built (inventory)

### 2.1 Core code

| Piece | Role |
|-------|------|
| **`hk_var_model.py`** | End-to-end pipeline: assemble data → stationarity (ADF + KPSS) → Johansen → transforms → lag selection (AIC/BIC + guardrail) → VAR or BVAR or VECM → IRFs (unified Cholesky) → FEVD → historical decomposition → ordering/subsample robustness → TVP-VAR block → sign-restriction draws → backtests → scenario forecasts → methods note / diagnostics exports. |
| **`fetch_real_data.py`** | Pull **C&SD** (GDP, unemployment), **HKMA** (HIBOR 3M), **FRED** (FFR, China quarterly nominal GDP series), **World Bank** annual CPI → spline quarterly (weak link). Writes **`data/hk_macro_quarterly_real.csv`**. Optional **`VERIFY_SSL=1`** for strict TLS. |
| **`tests/test_hk_var_model.py`** | Large pytest suite: data, companion matrix, Cholesky IRFs, BVAR, transforms, scenarios, Johansen smoke, FEVD (sum to one, non-neg), historical decomposition, sign-restriction smoke, TVP shapes, orthogonal draws. |

### 2.2 Identification and “structural” layers (in order of ambition)

1. **Cholesky** — default **external-first** ordering: `us_ffr`, `china_gdp`, then HK variables, then `hibor_3m` (configurable via CLI). Small-open-economy timing assumption.
2. **FEVD** — variance shares from orthogonalized IRFs; `output/07_fevd.png`, `fevd_table.csv`.
3. **Historical decomposition** — shock contributions over time; `output/08_hist_decomp.png`.
4. **VECM** — Johansen rank → `statsmodels` VECM on **levels**; wrapper builds VAR-form coefficients for IRFs/FEVD comparison. **Important empirical finding:** once cointegration is respected, the **US → HIBOR / unemployment** channel looks **much stronger** than in the differenced-only VAR — the peg is a long-run object; differencing can understate it.
5. **Sign restrictions** — random orthogonal rotations of `chol(Sigma_u)`; retain draws satisfying **impact** sign patterns for a **US monetary** and **China growth** narrative (`default_sign_table()`). Median/bands plotted; acceptance rate logged (often low — restrictions are tight).
6. **TVP-VAR (lightweight)** — equation-by-equation Kalman with **forgetting factor**; exploratory time-varying coefficients; **not** a full Bayesian TVP posterior (documented in audit v3).

### 2.3 Robustness machinery

- **Cholesky ordering permutations** — sensitivity of IRFs/FEVD to order.
- **Sub-samples** — full, pre-GFC, post-GFC, ex-COVID-style splits where implemented; eigenvalue / coefficient norm checks.
- **Backtesting** — expanding window vs AR(1) and random walk; h=1 and h=4 RMSE plots.

### 2.4 Outputs (typical `output/`)

Charts `01`–`06` (data, correlation, stability, IRFs, backtests, scenarios), **`07` FEVD**, **`08` historical decomposition**, **`09` ordering**, **`10` subsample**, **`11` sign-restriction IRFs**, **`12` TVP paths**; CSVs for FEVD, forecasts, data dictionary; text diagnostics, methods note, multiple **audit** and **evaluation** text files.

### 2.5 Paper and references

- **`paper/main.tex`** + **`references.bib`** — full draft (intro, data, framework, results, robustness). Content evolved as data and methods evolved (VAR vs VECM emphasis, real data narrative).
- **Not** the focus of this archive: polishing for a specific journal’s style — you explicitly don’t care about that in this log.

### 2.6 Automation and repo hygiene

- **`.cursor/rules/hk-var-auto-run.mdc`** — idea: after edits, run pipeline / tests / LaTeX as appropriate.
- **Git:** `main` on the Desktop folder; **worktrees** (`akd`, `gwu`) caused duplicate folders and two “verification” commits that were **merged** into `main` (see below).
- **Docs:** `AGENTS.md` (agent-oriented process), `IMPLEMENTATION_PLAN.md` (phased plan), `DATA_DOWNLOAD_CHECKLIST.md` (what to download next), `README.md`, plus **`output/model_review_audit_v3.txt`** (skills-based review).

---

## 3. Data story (the real saga)

### Phase A — Synthetic / FRED fallback

- Pipeline had to run **even without HK quarterly FRED IDs** (many series **404** on `fredgraph.csv`).
- **Synthetic DGP** with **GFC/COVID shocks injected as residual shocks** (not bogus regime dummies inside the law of motion) — audit fix.
- **`DATA_SPEC`** listed ideal FRED IDs; **reality:** often only **US `FEDFUNDS`** worked reliably from public CSV.

### Phase B — World Bank annual + spline

- **Annual** WB series for HK GDP, CPI, unemployment, China growth; **cubic spline** to quarterly.
- **HIBOR** often **FFR + spread** when HKMA series wasn’t wired.
- **Honest limitation:** splines **smooth** high-frequency variation; referees would (correctly) push back for publication.

### Phase C — Official APIs (current “real” path)

- **`fetch_real_data.py`** assembles:
  - **C&SD API** — GDP YoY (table **310-30001**), unemployment (**210-06101**, SAUR/UR, M3M → quarterly average).
  - **HKMA API** — **3M HIBOR** end-of-month → quarterly mean.
  - **FRED** — **FFR**, **China `CHNGDPNQDSMEI`** (nominal quarterly GDP → **YoY %**).
  - **World Bank** — **CPI inflation** still **annual → spline** (the **remaining weak variable**).

- Merged sample length is limited by the **shortest** series (China FRED end date → often **~103 quarters** to ~2023Q3, not identical to old 107-quarter spline panel).

### What’s still wrong (for you, not for “reviewers”)

1. **CPI** — still **not** official quarterly/monthly C&SD CPI in the automated build; **highest priority** to replace spline.
2. **China** — series is **nominal** quarterly GDP growth in levels space; interpreting it as “real China activity” is **loose** unless you swap series or relabel in writing.
3. **`DATA_SPEC` / data dictionary** — can still **misreport** “source” when **`hk_macro_quarterly_real.csv`** is loaded (stale FRED IDs in metadata) — known doc debt.

---

## 4. Audits and evaluations ( condensed )

- **Audit v1:** 12 issues (critical through low) — transforms, KPSS, Johansen, unified IRFs, BVAR sigma, etc. — **fixed**.
- **Audit v2:** 4 issues — dead code, scenario plots, RNG split, Cholesky CLI — **fixed**.
- **Academic assessment:** Tool was strong; needed **research question + FEVD + HD** — **done**.
- **Econometric evaluation (skills):** Grade **B+** — execution strong; **data/interpolation** capped the grade.
- **Audit v3:** Sign-restriction **column labeling**; VECM wrapper AIC not canonical; TVP exploratory; SSL; **documented** in `output/model_review_audit_v3.txt`.

---

## 5. Key numerical story (two regimes — don’t mix blindly)

**Old interpolated panel** (spline-heavy): Very **large** China shares for HK GDP in FEVD; **your** headline table in early `AGENTS.md` (e.g. ~77% China → HK GDP) belongs to that world.

**Official-data panel** (C&SD + HKMA + FRED): **Smaller** China FEVD shares for GDP; **US → HIBOR** in VAR more modest than under **VECM**; **VECM** says the **peg/cointegration** story much more aggressively for rates and unemployment.

**Takeaway for future you:** Always note **which CSV + which model** (VAR vs VECM) when quoting a number.

---

## 6. Git and worktrees (why it felt like “two projects”)

- **One repo**, **multiple worktrees**: Desktop `Hong Kong` on **`main`**, plus Cursor paths like **`akd`** / **`gwu`** at **detached commits**.
- You had **two parallel “verification” commits** (`akd` vs `gwu`) on top of the same base; **merged into `main`** with conflict resolution in `hk_var_model.py` docstring and tests.
- **Operational rule:** treat **Desktop `main`** as canonical; delete or reset worktrees when done.

---

## 7. What we explicitly did **not** optimize for

- **Cover letter templates**, **journal formatting**, **submission busywork** — you called that out; this archive agrees. They can exist later; they are **not** part of the scientific build log.
- **Perfect DSGE** or **SVAR-IV** — out of scope for this codebase iteration (could be “new direction” below).

---

## 8. Next steps — substance only (your agreed priorities)

1. **CPI:** Replace spline with **C&SD (or HKMA composite)** monthly/quarterly → YoY % aligned to QS index. **Update** `fetch_real_data.py` + CSV + rerun pipeline.
2. **China:** Replace or **relabel** nominal FRED growth with **real** quarterly series if you can source it consistently.
3. **Re-estimate everything** — one commit: new CSV → new IRFs/FEVD/VECM/sign/TVP outputs → **update `AGENTS.md` headline numbers** or delete stale table.
4. **Paper text** — sync **methods** with **transformed-data sign restrictions** and **VECM vs VAR** narrative (still not “journal formatting,” just honest science).
5. **Optional doc debt:** single metadata file for **true** series IDs per run; fix data dictionary when local CSV loads.

---

## 9. File index (where to look)

| Need | File |
|------|------|
| Agent-oriented chronology | `AGENTS.md` |
| Phased implementation plan | `IMPLEMENTATION_PLAN.md` |
| Manual data priorities | `DATA_DOWNLOAD_CHECKLIST.md` |
| Math/econ/code audit v3 | `output/model_review_audit_v3.txt` |
| Econometric narrative grade | `output/econometric_evaluation.txt` |
| This personal mega-log | **`FULL_PROCESS_ARCHIVE_STEVEN.md`** (this file) |

---

## 10. Closing line

This project went from **“build a HK macro model”** to a **fully instrumented empirical pipeline** with **real institutional data** for almost the whole panel, **multiple identification lenses**, **audited math**, and **tests** — plus a messy but **merged** git history. What’s left is mostly **better CPI and China semantics**, then **honest writing** that matches the **actual CSV and estimator**. Everything else is optional noise.

---

## Update — 2026-03-29 (data lock + paper sync pass)

### What changed in this pass

1. **CPI path upgraded in code**
   - Added official C&SD WBR CPI pull using machine-readable JSON/MDT assets.
   - New strategy in `fetch_real_data.py`: **official CPI splice where available + WB spline fallback**.
   - Current detected official overlap window: **2020Q2–2024Q4**.

2. **China semantics made explicit**
   - Kept `CHNGDPNQDSMEI` for now (nominal quarterly GDP -> YoY %).
   - Relabeled docs/code text to avoid calling it pure real China growth.

3. **Metadata debt reduced**
   - Added `data/source_metadata.json`.
   - `hk_var_model.py` now reads this sidecar when local CSV is loaded so `output/data_dictionary.csv` reflects actual source strings instead of generic `local_csv`.

4. **Full rerun done**
   - `python fetch_real_data.py`
   - `python hk_var_model.py --lag-criterion bic --model-type var`
   - `python -m pytest tests/test_hk_var_model.py -q` -> **63 passed, 1 skipped**
   - `latexmk -pdf paper/main.tex`

### New canonical run snapshot (this pass)

- **Dataset used:** `data/hk_macro_quarterly_real.csv`
- **Sample:** 1998Q1–2023Q3 (103 quarters; 102 after transforms at p=2)
- **VAR lag:** BIC selects **p=2**
- **Johansen rank (90%):** **3**

**FEVD at h=8 (VAR):**
- US FFR -> GDP: **10.1%**
- China GDP -> GDP: **41.2%**
- US FFR -> CPI: **7.4%**
- China GDP -> CPI: **38.1%**
- US FFR -> Unemployment: **22.1%**
- China GDP -> Unemployment: **14.0%**
- US FFR -> HIBOR: **32.3%**
- China GDP -> HIBOR: **4.7%**

**VECM comparison at h=8:**
- US FFR -> HIBOR: **62.3%**
- US FFR -> Unemployment: **35.8%**
- China GDP -> GDP: **27.5%**

### State after this update

- The project is now in a cleaner “data-paper” state: CPI is no longer purely spline in overlapping years, China labeling is explicit, outputs/paper/docs are synchronized to one run.
- Remaining hard problem is still the same: get a long-history **official** CPI and, if possible, a **real** quarterly China growth series with comparable coverage.

*End of archive — March 2026, updated 2026-03-29.*
