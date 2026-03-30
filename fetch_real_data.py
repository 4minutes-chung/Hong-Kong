"""
Fetch real quarterly HK macro data from official sources.
Produces data/hk_macro_quarterly_real.csv.

Sources:
  gdp_growth      : C&SD API table 310-30001 (quarterly YoY %)
  cpi_inflation   : C&SD WBR CPI monthly YoY (spliced where available)
                    + World Bank annual fallback via cubic spline
  unemployment    : C&SD API table 210-06101 (SAUR M3M -> quarterly avg)
  hibor_3m        : HKMA API hibor.fixing end-of-month (monthly -> quarterly avg)
  china_gdp       : FRED CHNGDPNQDSMEI quarterly nominal -> YoY % change
  us_ffr          : FRED FEDFUNDS monthly -> quarterly avg
"""

import urllib.request
import json
import ssl
import os
import io
from datetime import date
import numpy as np
import pandas as pd
from scipy.interpolate import CubicSpline

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)

_HEADERS = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}


def _ssl_context() -> ssl.SSLContext:
    """Use VERIFY_SSL=1 for strict certificate verification (recommended on trusted networks)."""
    if os.environ.get("VERIFY_SSL", "").strip() in ("1", "true", "yes"):
        return ssl.create_default_context()
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


def _fetch_json(url: str) -> dict:
    req = urllib.request.Request(url, headers=_HEADERS)
    with urllib.request.urlopen(req, timeout=30, context=_ssl_context()) as resp:
        return json.loads(resp.read())


def fetch_hk_gdp() -> pd.DataFrame:
    """C&SD table 310-30001: quarterly real GDP YoY % change."""
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


def fetch_hk_unemployment() -> pd.DataFrame:
    """C&SD table 210-06101: seasonally adjusted unemployment rate (M3M)."""
    data = _fetch_json(
        "https://www.censtatd.gov.hk/api/get.php?id=210-06101&lang=en&full_series=1"
    )
    # Prefer SAUR (seasonally adjusted); fall back to UR
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
    return df.resample("QS").mean().dropna()


def fetch_hibor_3m() -> pd.DataFrame:
    """HKMA API: end-of-month 3-month HIBOR fixing."""
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
            if yr >= 1998 and 1 <= mo <= 12:
                rows.append({"date": pd.Timestamp(yr, mo, 1),
                             "hibor_3m": float(r["ir_3m"])})
    df = pd.DataFrame(rows).set_index("date").sort_index()
    return df.resample("QS").mean().dropna()


def fetch_us_ffr() -> pd.DataFrame:
    """FRED FEDFUNDS: monthly effective federal funds rate."""
    url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=FEDFUNDS&cosd=1998-01-01"
    df = pd.read_csv(url, na_values=".")
    date_col = "DATE" if "DATE" in df.columns else "observation_date"
    df[date_col] = pd.to_datetime(df[date_col])
    df = df.set_index(date_col).dropna()
    df.columns = ["us_ffr"]
    return df.resample("QS").mean().dropna()


def fetch_china_gdp() -> pd.DataFrame:
    """FRED CHNGDPNQDSMEI: China quarterly nominal GDP -> YoY % change."""
    url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=CHNGDPNQDSMEI&cosd=1993-01-01"
    df = pd.read_csv(url, na_values=".")
    date_col = "DATE" if "DATE" in df.columns else "observation_date"
    df[date_col] = pd.to_datetime(df[date_col])
    df = df.set_index(date_col).dropna()
    df.columns = ["china_gdp_nominal"]
    df["china_gdp"] = df["china_gdp_nominal"].pct_change(4) * 100
    df = df[["china_gdp"]].dropna()
    df = df[df.index >= "1998-01-01"]
    return df.resample("QS").mean().dropna()


def fetch_hk_cpi_wb_fallback() -> pd.DataFrame:
    """World Bank FP.CPI.TOTL.ZG: annual CPI inflation -> cubic spline quarterly."""
    url = (
        "https://api.worldbank.org/v2/country/HKG/indicator/"
        "FP.CPI.TOTL.ZG?format=json&per_page=500"
    )
    req = urllib.request.Request(url, headers=_HEADERS)
    with urllib.request.urlopen(req, timeout=15, context=_ssl_context()) as resp:
        wb_data = json.loads(resp.read())

    annual = sorted(
        [{"year": int(r["date"]), "val": float(r["value"])}
         for r in wb_data[1] if r["value"] is not None],
        key=lambda x: x["year"],
    )
    annual = [r for r in annual if r["year"] >= 1997]

    years = np.array([r["year"] for r in annual])
    vals = np.array([r["val"] for r in annual])
    cs = CubicSpline(years, vals)

    q_dates = pd.date_range("1998-01-01", periods=120, freq="QS")
    q_years = np.array([d.year + (d.month - 1) / 12.0 for d in q_dates])
    q_vals = cs(q_years)
    df = pd.DataFrame({"cpi_inflation": q_vals}, index=q_dates)
    return df[df.index.year <= int(years[-1])]


def _build_recent_cpi_ecodes(max_reports: int = 84) -> list[str]:
    """
    Build recent monthly ecode candidates for C&SD CPI WBR reports.
    Format: B1060001YYYYMM## where ## is month number.
    """
    today = date.today()
    y, m = today.year, today.month
    out = []
    for _ in range(max_reports):
        out.append(f"B1060001{y}MM{m:02d}")
        m -= 1
        if m == 0:
            m = 12
            y -= 1
    return out


def _fetch_cpi_mdt_for_ecode(ecode: str) -> pd.DataFrame | None:
    """
    Fetch Composite CPI YoY monthly values from one C&SD WBR issue.
    Returns monthly rows with date index, or None if unavailable.
    """
    pcode = ecode[:8]
    base = f"https://www.censtatd.gov.hk/wbr/{pcode}/{ecode}/data/"

    try:
        comp_url = base + "table_CPI_R_2_01A_comp.json"
        comp = _fetch_json(comp_url)
        theme_id = comp.get("theme_id")
        table_id = comp.get("tb_code")
        if not theme_id or not table_id:
            return None

        # cnds_cdm.js naming rule:
        # MDT_<theme>_<table>_<stat_var>_<stat_pres>.csv
        mdt_name = f"MDT_{theme_id}_{table_id}_CC_CM_1920_YoY_1dp_percent_s.csv"
        req = urllib.request.Request(base + mdt_name, headers=_HEADERS)
        with urllib.request.urlopen(req, timeout=20, context=_ssl_context()) as resp:
            csv_txt = resp.read().decode("utf-8", errors="ignore")

        df = pd.read_csv(io.StringIO(csv_txt))
        if not {"CCYY", "MM", "obs_value"}.issubset(df.columns):
            return None

        df = df.dropna(subset=["MM", "obs_value"]).copy()
        if df.empty:
            return None
        df["CCYY"] = df["CCYY"].astype(int)
        df["MM"] = df["MM"].astype(int)
        df["date"] = pd.to_datetime(
            dict(year=df["CCYY"], month=df["MM"], day=1), errors="coerce"
        )
        df = df.dropna(subset=["date"])
        df = df.set_index("date").sort_index()
        return df[["obs_value"]].rename(columns={"obs_value": "cpi_inflation"})
    except Exception:
        return None


def fetch_hk_cpi_official(max_reports: int = 360, max_empty_streak: int = 36) -> pd.DataFrame:
    """
    Fetch official HK composite CPI YoY from recent C&SD WBR issues.
    Combines unique monthly values across issues and returns quarterly mean.
    """
    pieces = []
    empty_streak = 0
    for ecode in _build_recent_cpi_ecodes(max_reports=max_reports):
        m = _fetch_cpi_mdt_for_ecode(ecode)
        if m is not None and not m.empty:
            pieces.append(m)
            empty_streak = 0
        else:
            empty_streak += 1
            if empty_streak >= max_empty_streak and pieces:
                # Stop probing very old issues after a long miss streak.
                break
    if not pieces:
        return pd.DataFrame(columns=["cpi_inflation"])

    monthly = pd.concat(pieces).sort_index()
    # Duplicate month entries from overlapping issues -> keep latest value
    monthly = monthly[~monthly.index.duplicated(keep="last")]
    monthly = monthly[(monthly.index >= "1998-01-01")]
    return monthly.resample("QS").mean().dropna()


def fetch_hk_cpi() -> tuple[pd.DataFrame, str, pd.DataFrame]:
    """
    CPI construction strategy:
    1) Build long history from WB annual+spline
    2) Overwrite overlapping dates with official C&SD monthly YoY aggregates
    """
    wb = fetch_hk_cpi_wb_fallback()
    official = fetch_hk_cpi_official()
    if official.empty:
        lineage = pd.DataFrame(
            {"source": "wb_spline"},
            index=wb.index,
        )
        lineage.index.name = "date"
        return wb, "world_bank_spline_only", lineage

    # Prefer official quarterly CPI where available; fall back to WB spline elsewhere.
    merged = official.combine_first(wb).sort_index()
    merged = merged[(merged.index >= "1998-01-01")]

    lineage = pd.DataFrame({"source": "wb_spline"}, index=merged.index)
    lineage.loc[merged.index.intersection(official.index), "source"] = "official"
    lineage.index.name = "date"

    official_idx = lineage.index[lineage["source"] == "official"]
    if len(official_idx):
        source = (
            f"official_splice_{official_idx.min().date()}_{official_idx.max().date()}"
            f"_share_{(lineage['source'] == 'official').mean():.2%}"
        )
    else:
        source = "world_bank_spline_only_no_overlap"
    return merged, source, lineage


def build_dataset() -> pd.DataFrame:
    """Fetch all series and merge into quarterly DataFrame."""
    print("[1/6] HK GDP growth (C&SD)...")
    gdp = fetch_hk_gdp()
    print(f"       {len(gdp)} quarters")

    print("[2/6] HK unemployment (C&SD)...")
    unemp = fetch_hk_unemployment()
    print(f"       {len(unemp)} quarters")

    print("[3/6] HIBOR 3M (HKMA)...")
    hibor = fetch_hibor_3m()
    print(f"       {len(hibor)} quarters")

    print("[4/6] US FFR (FRED)...")
    ffr = fetch_us_ffr()
    print(f"       {len(ffr)} quarters")

    print("[5/6] China nominal GDP growth YoY (FRED)...")
    china = fetch_china_gdp()
    print(f"       {len(china)} quarters")

    print("[6/6] HK CPI inflation (C&SD splice + WB fallback)...")
    cpi, cpi_source, cpi_lineage = fetch_hk_cpi()
    print(f"       {len(cpi)} quarters ({cpi_source})")

    merged = gdp.join(cpi, how="outer")
    merged = merged.join(unemp, how="outer")
    merged = merged.join(hibor, how="outer")
    merged = merged.join(china, how="outer")
    merged = merged.join(ffr, how="outer")

    col_order = ["gdp_growth", "cpi_inflation", "unemployment",
                 "hibor_3m", "china_gdp", "us_ffr"]
    merged = merged[[c for c in col_order if c in merged.columns]]
    merged = merged.dropna()
    merged.index.name = "date"

    lineage_path = os.path.join(DATA_DIR, "cpi_lineage.csv")
    cpi_lineage.to_csv(lineage_path)
    official_share = float((cpi_lineage["source"] == "official").mean()) if len(cpi_lineage) else 0.0
    official_idx = cpi_lineage.index[cpi_lineage["source"] == "official"]
    official_window = (
        f"{official_idx.min().date()} to {official_idx.max().date()}"
        if len(official_idx) else "none"
    )
    print(f"       CPI lineage -> {lineage_path} (official share {official_share:.1%})")

    # Sidecar metadata for reproducibility
    meta = {
        "gdp_growth": "C&SD table 310-30001 (quarterly YoY %)",
        "cpi_inflation": (
            f"CPI source={cpi_source}; lineage_file=data/cpi_lineage.csv; "
            f"official_window={official_window}; official_share={official_share:.1%}; "
            "C&SD WBR CPI_R_2_01A where available, else WB spline"
        ),
        "unemployment": "C&SD table 210-06101 (SAUR/UR M3M -> quarterly mean)",
        "hibor_3m": "HKMA hibor.fixing endperiod API (monthly -> quarterly mean, primary path only)",
        "china_gdp": "FRED CHNGDPNQDSMEI nominal quarterly GDP -> YoY %",
        "us_ffr": "FRED FEDFUNDS monthly -> quarterly mean",
    }
    with open(os.path.join(DATA_DIR, "source_metadata.json"), "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=2)

    return merged


if __name__ == "__main__":
    df = build_dataset()
    outpath = os.path.join(DATA_DIR, "hk_macro_quarterly_real.csv")
    df.to_csv(outpath, float_format="%.4f")
    print(f"\nSaved {len(df)} quarters to {outpath}")
    print(f"Range: {df.index[0].date()} to {df.index[-1].date()}")
    print(f"\n{df.describe().round(2)}")
