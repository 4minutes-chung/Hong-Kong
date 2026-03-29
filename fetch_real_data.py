"""
Fetch real quarterly HK macro data from official sources.
Produces data/hk_macro_quarterly_real.csv.

Sources:
  gdp_growth      : C&SD API table 310-30001 (quarterly YoY %)
  cpi_inflation   : World Bank FP.CPI.TOTL.ZG annual -> cubic spline quarterly
  unemployment    : C&SD API table 210-06101 (SAUR M3M -> quarterly avg)
  hibor_3m        : HKMA API hibor.fixing end-of-month (monthly -> quarterly avg)
  china_gdp       : FRED CHNGDPNQDSMEI quarterly nominal -> YoY % change
  us_ffr          : FRED FEDFUNDS monthly -> quarterly avg
"""

import urllib.request, json, ssl, os
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


def fetch_hk_cpi() -> pd.DataFrame:
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

    print("[5/6] China GDP growth (FRED)...")
    china = fetch_china_gdp()
    print(f"       {len(china)} quarters")

    print("[6/6] HK CPI inflation (World Bank + spline)...")
    cpi = fetch_hk_cpi()
    print(f"       {len(cpi)} quarters")

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
    return merged


if __name__ == "__main__":
    df = build_dataset()
    outpath = os.path.join(DATA_DIR, "hk_macro_quarterly_real.csv")
    df.to_csv(outpath, float_format="%.4f")
    print(f"\nSaved {len(df)} quarters to {outpath}")
    print(f"Range: {df.index[0].date()} to {df.index[-1].date()}")
    print(f"\n{df.describe().round(2)}")
