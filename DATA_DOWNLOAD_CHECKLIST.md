# Data download checklist (manual / tomorrow)

Use this list to replace or complement programmatic fetches in `fetch_real_data.py` and to refresh `data/hk_macro_quarterly_real.csv`.

## Priority order (what matters most for referees)

1. **HK CPI inflation (quarterly, official)** — currently the **only** series still built from **World Bank annual + cubic spline**. This is the main weakness for *Pacific Economic Review* / *Journal of Asian Economics*.
2. **China real GDP growth (quarterly)** — pipeline uses **FRED `CHNGDPNQDSMEI`** (nominal quarterly levels → YoY %). Prefer **real** growth from NBS or a clearly documented real series.
3. **Everything else** — already from official quarterly/monthly APIs in the automated fetcher (verify files after download).

---

## 1. Hong Kong — Census and Statistics Department (C&SD)

| Variable | Table / product | API / download | Notes |
|----------|-------------------|----------------|--------|
| Real GDP growth (YoY %) | Table **310-30001** | `https://www.censtatd.gov.hk/api/get.php?id=310-30001&lang=en&full_series=1` | Quarterly, Total, YoY % — **preferred for `gdp_growth`** |
| Unemployment | Table **210-06101** | Same pattern `id=210-06101` | Use **SAUR** (seasonally adjusted) + **M3M** if available; else **UR** |
| **CPI (headline or composite)** | Search **Consumer Price Index** on [data.gov.hk](https://data.gov.hk) | Web table CSV/XLSX; table IDs vary by revision | **Target:** quarterly or monthly CPI **YoY %** or index → compute YoY in pipeline |

**Known issues**

- Direct `download_csv=1` URLs sometimes return **HTML** (browser session). The **JSON API** (`api/get.php`) works with a normal `User-Agent` header.
- Some tables require `period=` query for very long histories; `full_series=1` usually works.

**Preference:** For CPI, download **monthly** official series and aggregate to **quarterly average** (or end-quarter), then compute **YoY %** to match the rest of the panel.

---

## 2. Hong Kong — HKMA

| Variable | Endpoint | Field | Notes |
|----------|----------|-------|--------|
| 3-month HIBOR | `.../hk-interbank-ir-endperiod?segment=hibor.fixing` | `ir_3m`, `end_of_month` | Monthly; aggregate to **quarterly mean** (current code) |

**Known issues**

- Pagination: use `offset` + `pagesize` until empty.
- `2021-00` style months appear in **economic-statistics** API (sparse); **HIBOR endpoint** is clean — prefer HIBOR from this API only.

---

## 3. US — FRED (St. Louis Fed)

| Variable | Series ID | Notes |
|----------|-----------|--------|
| Effective federal funds rate | **`FEDFUNDS`** | Monthly → quarterly **mean** |

**Preference:** Keep **FRED CSV** (`fredgraph.csv`) or register for a free **FRED API key** for reproducible dated pulls.

---

## 4. China — real activity

| Variable | Current pipeline | Preferred upgrade |
|----------|------------------|-------------------|
| China growth | **FRED `CHNGDPNQDSMEI`** (nominal quarterly GDP, 4-quarter YoY %) | **Real** quarterly YoY GDP growth from **NBS** or **IMF IFS** (if access works), or FRED real series if available with same frequency |

**Known issues**

- Nominal GDP growth mixes **price and quantity**; interpretation is **not** pure “real China shock” unless you use real data or deflate explicitly.
- FRED China quarterly series may **end earlier** than US/HK — sample length is limited by **shortest** series (currently ~**103** quarters in typical run).

---

## 5. SSL / environment (`fetch_real_data.py`)

- The script may use `ssl` context without hostname verification for **C&SD** in some environments. **Preference:** run on networks that allow `censtatd.gov.hk` and `api.hkma.gov.hk` with normal TLS; set `VERIFY_SSL=1` if implemented to use default verification.
- **Corporate firewalls** sometimes block government APIs — if fetches fail, use **manual CSV** from data.gov.hk and place under `data/` with the column names expected by `hk_macro_quarterly_real.csv`.

---

## 6. Column schema (must match `MODEL_VARIABLES` order in `hk_var_model.py`)

Required columns in the merged CSV:

`gdp_growth`, `cpi_inflation`, `unemployment`, `hibor_3m`, `china_gdp`, `us_ffr`

Index: `date` as first day of quarter (`YYYY-MM-DD`), frequency **QS**.

---

## 7. After you download (tomorrow)

1. Save authoritative CSVs under `data/` (e.g. `data/cpi_monthly_censtatd.csv`).
2. Add a small notebook or script to merge → `hk_macro_quarterly_real.csv` (or extend `fetch_real_data.py`).
3. Run: `python fetch_real_data.py` (regenerates from APIs) **or** replace `hk_macro_quarterly_real.csv` manually.
4. Run: `python hk_var_model.py --lag-criterion bic --model-type var`
5. Run: `pytest tests/ -v`

---

## 8. `DATA_SPEC` in `hk_var_model.py` (legacy FRED IDs)

The dict `DATA_SPEC` still lists **old** FRED IDs for HK (`NGDPRSAXDCHKQ`, etc.) that often **404**. When `hk_macro_quarterly_real.csv` is present, **`assemble_data()` does not use those IDs**. After you stabilize manual sources, update `DATA_SPEC` comments/IDs to match what you actually use so the data dictionary is not misleading.
