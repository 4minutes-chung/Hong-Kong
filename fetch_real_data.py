"""
Fetch HK macro data from official sources and produce the model-ready dataset.

Output: data/hk_macro_varx_ready.csv
  - 9 columns: us_ffr, china_gdp, hibor_3m, hk_exports_china_yoy,
               gdp_growth, cpi_inflation, unemployment,
               hk_property_price_qoq (+ hk_property_price_idx as level)
  - Quarterly, 1998 Q1 onwards
  - Run: python fetch_real_data.py
"""

import urllib.request
import urllib.error
import json
import os
import io
import warnings
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)

_HEADERS = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
PROPERTY_PRICE_URL = "https://www.rvd.gov.hk/datagovhk/1.4M.csv"


def _fetch_json(url):
    req = urllib.request.Request(url, headers=_HEADERS)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())


def fetch_hk_gdp():
    """C&SD table 310-30001: quarterly real GDP YoY %."""
    data = _fetch_json(
        "https://www.censtatd.gov.hk/api/get.php?id=310-30001&lang=en&full_series=1"
    )
    rows = []
    for r in data["dataSet"]:
        if (
            r["freq"] == "Q"
            and r.get("GDP_COMPONENTDesc", "") == "Total"
            and "Year-on-year" in r.get("svDesc", "")
            and r["figure"] not in ("", None)
            and int(r["period"][:4]) >= 1998
        ):
            yr, mo = int(r["period"][:4]), int(r["period"][4:6])
            qs_map = {3: 1, 6: 4, 9: 7, 12: 10}
            if mo in qs_map:
                rows.append({"date": pd.Timestamp(yr, qs_map[mo], 1),
                             "gdp_growth": float(r["figure"])})
    return pd.DataFrame(rows).set_index("date").sort_index()


def fetch_hk_unemployment():
    """C&SD table 210-06101: seasonally adjusted unemployment rate (M3M)."""
    data = _fetch_json(
        "https://www.censtatd.gov.hk/api/get.php?id=210-06101&lang=en&full_series=1"
    )
    for sv_code in ("SAUR", "UR"):
        recs = [
            r for r in data["dataSet"]
            if r["sv"] == sv_code
            and r["SEXDesc"] == "Total"
            and r["freq"] == "M3M"
            and r["figure"] not in ("", None)
            and int(r["period"][:4]) >= 1998
        ]
        if len(recs) >= 50:
            break
    rows = []
    for r in recs:
        yr, mo = int(r["period"][:4]), int(r["period"][4:6])
        if 1 <= mo <= 12:
            rows.append({"date": pd.Timestamp(yr, mo, 1),
                         "unemployment": float(r["figure"])})
    df = pd.DataFrame(rows).set_index("date").sort_index()
    return df.resample("QS").last().dropna()


def fetch_hibor_3m():
    """HKMA API: 3-month HIBOR fixing, monthly -> quarterly mean."""
    cache = os.path.join(DATA_DIR, "hibor_3m_quarterly.csv")
    try:
        all_records = []
        offset = 0
        while True:
            url = (
                "https://api.hkma.gov.hk/public/market-data-and-statistics/"
                "monthly-statistical-bulletin/er-ir/hk-interbank-ir-endperiod"
                f"?segment=hibor.fixing&offset={offset}&pagesize=500"
            )
            data = _fetch_json(url)
            recs = data["result"]["records"]
            if not recs:
                break
            all_records.extend(recs)
            offset += 500
            if len(recs) < 500:
                break
        rows = []
        for r in all_records:
            if r.get("ir_3m") is not None:
                parts = r["end_of_month"].split("-")
                yr, mo = int(parts[0]), int(parts[1])
                if yr >= 1998:
                    rows.append({"date": pd.Timestamp(yr, mo, 1),
                                 "hibor_3m": float(r["ir_3m"])})
        df = pd.DataFrame(rows).set_index("date").sort_index()
        df = df.resample("QS").mean().dropna()
        df.to_csv(cache, float_format="%.4f")
        return df
    except Exception as exc:
        if os.path.exists(cache):
            cached = pd.read_csv(cache, index_col="date", parse_dates=True)
            warnings.warn(
                f"HKMA API failed ({type(exc).__name__}); using cached HIBOR data "
                f"through {cached.index.max().date()}: {cache}",
                RuntimeWarning,
                stacklevel=2,
            )
            return cached
        raise RuntimeError("HKMA API failed and no cache found. Run once with internet access.")


def fetch_us_ffr():
    """FRED FEDFUNDS: monthly -> quarterly mean."""
    url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=FEDFUNDS&cosd=1998-01-01"
    df = pd.read_csv(url, na_values=".")
    date_col = "DATE" if "DATE" in df.columns else "observation_date"
    df[date_col] = pd.to_datetime(df[date_col])
    df = df.set_index(date_col).dropna()
    df.columns = ["us_ffr"]
    return df.resample("QS").mean().dropna()


def fetch_china_gdp():
    """OECD QNA: China real GDP YoY % (B1GQ, GY). No fallback — must succeed."""
    url = (
        "https://stats.oecd.org/sdmx-json/data/QNA/CHN.B1_GE.GPSA.Q/all"
        "?startTime=1998-Q1&endTime=2030-Q4"
    )
    req = urllib.request.Request(url, headers=_HEADERS)
    with urllib.request.urlopen(req, timeout=45) as resp:
        d = json.loads(resp.read())

    ds = d["data"]["dataSets"][0]["series"]
    struct = d["data"]["structures"][0]
    ser_dims = struct["dimensions"]["series"]
    obs_time = struct["dimensions"]["observation"][0]["values"]

    def _idx(dim_id, val_id):
        for dim in ser_dims:
            if dim["id"] == dim_id:
                return next(i for i, v in enumerate(dim["values"]) if v["id"] == val_id)
        raise KeyError(dim_id)

    targets = {
        "FREQ": _idx("FREQ", "Q"),
        "REF_AREA": _idx("REF_AREA", "CHN"),
        "TRANSACTION": _idx("TRANSACTION", "B1GQ"),
        "TRANSFORMATION": _idx("TRANSFORMATION", "GY"),
        "UNIT_MEASURE": _idx("UNIT_MEASURE", "PC"),
    }
    dim_order = [dim["id"] for dim in ser_dims]

    rows = []
    for key, sdata in ds.items():
        parts = dict(zip(dim_order, (int(x) for x in key.split(":"))))
        if all(parts.get(k) == v for k, v in targets.items()):
            for t_str, vals in sdata["observations"].items():
                period = obs_time[int(t_str)]["id"]
                yr, q = period.split("-Q")
                month = [1, 4, 7, 10][int(q) - 1]
                rows.append({"date": pd.Timestamp(int(yr), month, 1),
                             "china_gdp": float(vals[0])})

    if not rows:
        raise ValueError("No CHN B1GQ GY series found in OECD response.")

    df = pd.DataFrame(rows).set_index("date").sort_index()
    return df[df.index >= "1998-01-01"].resample("QS").last().dropna()


def fetch_hk_cpi():
    """C&SD table 510-60001: Composite CPI YoY monthly -> quarterly mean. No fallback."""
    data = _fetch_json(
        "https://www.censtatd.gov.hk/api/get.php?id=510-60001&lang=en&full_series=1"
    )
    rows = []
    for r in data["dataSet"]:
        if (
            r.get("freq") == "M"
            and r.get("sv") == "CC_CM_1920"
            and r.get("svDesc") == "Year-on-year % change"
            and r.get("figure") not in ("", None)
            and int(r["period"][:4]) >= 1998
        ):
            yr, mo = int(r["period"][:4]), int(r["period"][4:6])
            rows.append({"date": pd.Timestamp(yr, mo, 1),
                         "cpi_inflation": float(r["figure"])})
    if not rows:
        raise RuntimeError("C&SD CPI API returned no data.")
    monthly = pd.DataFrame(rows).set_index("date").sort_index()
    monthly = monthly[~monthly.index.duplicated(keep="last")]
    return monthly.resample("QS").mean().dropna()


def fetch_hk_exports_china():
    """C&SD table 410-50013: exports to China, monthly YoY % -> quarterly mean."""
    cache = os.path.join(DATA_DIR, "hk_exports_china_quarterly.csv")
    try:
        data = _fetch_json(
            "https://www.censtatd.gov.hk/api/get.php?id=410-50013&lang=en&full_series=1"
        )
        rows = []
        for r in data.get("dataSet", []):
            if (
                r.get("COUNTRYDesc") == "Chinese Mainland"
                and r.get("freq") == "M"
                and r.get("svDesc") == "Year-on-year % change"
                and r.get("figure") not in ("", None)
                and str(r.get("period", ""))[:4] >= "1998"
            ):
                period = str(r["period"])
                yr, mo = int(period[:4]), int(period[4:6])
                rows.append({"date": pd.Timestamp(yr, mo, 1),
                             "hk_exports_china_yoy": float(r["figure"])})
        if not rows:
            raise ValueError("No Chinese Mainland rows in C&SD response.")
        df = pd.DataFrame(rows).set_index("date").sort_index()
        df = df.resample("QS").mean().dropna()
        df.to_csv(cache, float_format="%.4f")
        return df
    except Exception as exc:
        if os.path.exists(cache):
            cached = pd.read_csv(cache, index_col="date", parse_dates=True).resample("QS").mean().dropna()
            warnings.warn(
                f"C&SD exports API failed ({type(exc).__name__}); using cached exports data "
                f"through {cached.index.max().date()}: {cache}",
                RuntimeWarning,
                stacklevel=2,
            )
            return cached
        raise RuntimeError("C&SD exports API failed and no cache found.")


def fetch_hk_property():
    """RVD/data.gov.hk: property price index, monthly -> quarterly mean + QoQ transform."""
    csv_text_raw = urllib.request.urlopen(
        urllib.request.Request(PROPERTY_PRICE_URL, headers={"User-Agent": "Mozilla/5.0"}),
        timeout=45
    ).read().decode("utf-8-sig", errors="ignore")

    raw = pd.read_csv(io.StringIO(csv_text_raw), header=1)
    raw = raw.rename(columns={"All Classes": "hk_property_price_idx"})
    raw["date"] = pd.to_datetime(raw["Month"], format="%b-%y", errors="coerce")
    raw = raw.dropna(subset=["date"]).set_index("date").sort_index()
    raw["hk_property_price_idx"] = pd.to_numeric(raw["hk_property_price_idx"], errors="coerce")

    quarterly = raw[["hk_property_price_idx"]].resample("QS").mean()
    quarterly["hk_property_price_qoq"] = quarterly["hk_property_price_idx"].pct_change() * 100
    quarterly = quarterly[quarterly.index >= "1998-01-01"].dropna()
    return quarterly


def build_dataset():
    """Fetch all series and merge into model-ready quarterly DataFrame."""
    print("[1/7] HK GDP growth (C&SD)...")
    gdp = fetch_hk_gdp()
    print(f"       {len(gdp)} quarters")

    print("[2/7] HK unemployment (C&SD)...")
    unemp = fetch_hk_unemployment()
    print(f"       {len(unemp)} quarters")

    print("[3/7] HIBOR 3M (HKMA)...")
    hibor = fetch_hibor_3m()
    print(f"       {len(hibor)} quarters")

    print("[4/7] US FFR (FRED)...")
    ffr = fetch_us_ffr()
    print(f"       {len(ffr)} quarters")

    print("[5/7] China real GDP YoY (OECD QNA)...")
    china = fetch_china_gdp()
    print(f"       {len(china)} quarters")

    print("[6/7] HK CPI inflation (C&SD)...")
    cpi = fetch_hk_cpi()
    print(f"       {len(cpi)} quarters")

    print("[7/7] HK exports to China YoY (C&SD)...")
    exports = fetch_hk_exports_china()
    print(f"       {len(exports)} quarters")

    print("[+] HK property prices (RVD)...")
    prop = fetch_hk_property()
    print(f"       {len(prop)} quarters")

    merged = (gdp
              .join(cpi, how="outer")
              .join(unemp, how="outer")
              .join(hibor, how="outer")
              .join(china, how="outer")
              .join(ffr, how="outer")
              .join(exports, how="outer")
              .join(prop, how="outer"))

    col_order = [
        "us_ffr", "china_gdp",
        "hibor_3m", "hk_exports_china_yoy", "hk_property_price_qoq",
        "gdp_growth", "cpi_inflation", "unemployment",
        "hk_property_price_idx",
    ]
    merged = merged[[c for c in col_order if c in merged.columns]]
    merged = merged.dropna(subset=[c for c in col_order if c != "hk_property_price_idx"])
    merged.index.name = "date"
    return merged


if __name__ == "__main__":
    df = build_dataset()
    outpath = os.path.join(DATA_DIR, "hk_macro_varx_ready.csv")
    df.to_csv(outpath, float_format="%.4f")
    print(f"\nSaved {len(df)} quarters to {outpath}")
    print(f"Range: {df.index[0].date()} to {df.index[-1].date()}")
    print(f"\n{df.describe().round(2)}")
