"""
Fetch real quarterly HK macro data from official sources.
Produces data/hk_macro_quarterly_real.csv.

Sources:
  gdp_growth      : C&SD API table 310-30001 (quarterly YoY %)
  cpi_inflation   : C&SD table 510-60001 Composite CPI monthly YoY
                    aggregated to quarterly mean; WB annual spline fallback
  unemployment    : C&SD API table 210-06101 (SAUR M3M -> quarterly avg)
  hibor_3m        : HKMA API hibor.fixing end-of-month (monthly -> quarterly avg)
  china_gdp       : OECD QNA China real GDP YoY; FRED nominal fallback if OECD fails
  us_ffr          : FRED FEDFUNDS monthly -> quarterly avg
  property prices : RVD/data.gov.hk private domestic price indices, monthly
                    -> quarterly sidecar and macro-property extension
"""

import urllib.request
import urllib.error
import json
import ssl
import os
import io
from datetime import date
import numpy as np
import pandas as pd
from scipy.interpolate import CubicSpline
from pandas.errors import EmptyDataError, ParserError

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)

_HEADERS = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
PROPERTY_PRICE_URL = "https://www.rvd.gov.hk/datagovhk/1.4M.csv"


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
    # Use end-of-quarter M3M reading (e.g. March M3M = avg(Jan-Mar)) to avoid
    # double-smoothing from averaging three overlapping 3-month windows.
    return df.resample("QS").last().dropna()


def fetch_hibor_3m() -> pd.DataFrame:
    """HKMA API: end-of-month 3-month HIBOR fixing."""
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
                if yr >= 1998 and 1 <= mo <= 12:
                    rows.append({"date": pd.Timestamp(yr, mo, 1),
                                 "hibor_3m": float(r["ir_3m"])})
        df = pd.DataFrame(rows).set_index("date").sort_index()
        df = df.resample("QS").mean().dropna()
        df.to_csv(cache, float_format="%.4f")
        return df
    except Exception:
        if os.path.exists(cache):
            return pd.read_csv(cache, index_col="date", parse_dates=True)

        macro_path = os.path.join(DATA_DIR, "hk_macro_quarterly_real.csv")
        if os.path.exists(macro_path):
            df = pd.read_csv(macro_path, index_col="date", parse_dates=True)
            if "hibor_3m" in df.columns:
                hibor = df[["hibor_3m"]].dropna()
                hibor.to_csv(cache, float_format="%.4f")
                return hibor
        raise


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


def fetch_china_real_gdp_oecd() -> pd.DataFrame:
    """
    OECD QNA: China quarterly real GDP YoY % growth (B1GQ, GY transformation).
    Source: stats.oecd.org SDMX-JSON API, series CHN.B1_GE.GPSA.Q.
    Falls back to nominal GDP (FRED CHNGDPNQDSMEI) if the OECD API is unavailable.
    """
    url = (
        "https://stats.oecd.org/sdmx-json/data/QNA/CHN.B1_GE.GPSA.Q/all"
        "?startTime=1998-Q1&endTime=2030-Q4"
    )
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "application/json",
    }
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=45, context=_ssl_context()) as resp:
            d = json.loads(resp.read())

        ds = d["data"]["dataSets"][0]["series"]
        struct = d["data"]["structures"][0]
        ser_dims = struct["dimensions"]["series"]
        obs_time = struct["dimensions"]["observation"][0]["values"]

        def _idx(dim_id: str, val_id: str) -> int:
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
                    period = obs_time[int(t_str)]["id"]  # e.g. "2005-Q3"
                    yr, q = period.split("-Q")
                    month = [1, 4, 7, 10][int(q) - 1]
                    rows.append({"date": pd.Timestamp(int(yr), month, 1),
                                 "china_gdp": float(vals[0])})

        if not rows:
            raise ValueError("No CHN B1GQ GY series found in OECD response")

        df = pd.DataFrame(rows).set_index("date").sort_index()
        df = df[df.index >= "1998-01-01"]
        return df.resample("QS").last().dropna()

    except Exception:
        # Fall back to nominal GDP if OECD API is unreachable
        return fetch_china_gdp()


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
    except (
        urllib.error.URLError,
        urllib.error.HTTPError,
        OSError,
        ssl.SSLError,
        json.JSONDecodeError,
        ValueError,
        KeyError,
        TypeError,
        ParserError,
        EmptyDataError,
    ):
        return None


def fetch_hk_cpi_official() -> pd.DataFrame:
    """
    C&SD table 510-60001: official Composite CPI YoY monthly rate.

    This replaces the previous WBR-issue splice, which only covered recent
    years. Table 510-60001 exposes the full official monthly Composite CPI
    series directly through the C&SD API.
    """
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
            rows.append({
                "date": pd.Timestamp(yr, mo, 1),
                "cpi_inflation": float(r["figure"]),
            })

    if not rows:
        return pd.DataFrame(columns=["cpi_inflation"])

    monthly = pd.DataFrame(rows).set_index("date").sort_index()
    monthly = monthly[~monthly.index.duplicated(keep="last")]
    return monthly.resample("QS").mean().dropna()


def fetch_hk_cpi() -> tuple[pd.DataFrame, str, pd.DataFrame]:
    """
    CPI construction strategy:
    1) Use official C&SD table 510-60001 Composite CPI YoY monthly history.
    2) Fall back to World Bank annual+spline only if official CPI is unavailable.
    """
    official = fetch_hk_cpi_official()
    if not official.empty:
        lineage = pd.DataFrame(
            {"source": "official_censtatd_510_60001"},
            index=official.index,
        )
        lineage.index.name = "date"
        source = (
            f"official_censtatd_510_60001_"
            f"{official.index.min().date()}_{official.index.max().date()}"
        )
        return official, source, lineage

    wb = fetch_hk_cpi_wb_fallback()
    lineage = pd.DataFrame({"source": "wb_spline"}, index=wb.index)
    lineage.index.name = "date"
    return wb, "world_bank_spline_only", lineage


def fetch_hk_exports_china() -> pd.DataFrame:
    """
    C&SD table 410-50013: HK total exports to Chinese Mainland, monthly YoY %
    aggregated to quarterly mean. Falls back to cached CSV if API unavailable.
    """
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
            raise ValueError("No Chinese Mainland rows in C&SD response")
        monthly = pd.DataFrame(rows).set_index("date").sort_index()
        df = monthly.resample("QS").mean().dropna()
        df.to_csv(cache, float_format="%.4f")
        return df
    except Exception:
        if os.path.exists(cache):
            df = pd.read_csv(cache, index_col="date", parse_dates=True)
            return df.resample("QS").mean().dropna()
        raise


def _read_csv_url(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=45, context=_ssl_context()) as resp:
        return resp.read().decode("utf-8-sig", errors="ignore")


def fetch_hk_property_price_rvd_monthly() -> pd.DataFrame:
    """
    RVD/data.gov.hk 1.4M: private domestic price indices by class, monthly.

    The official All Classes index is kept as the main property-price measure.
    Class indices are retained so the data can later support a housing-market
    heterogeneity appendix without changing the core macro panel.
    """
    csv_text = _read_csv_url(PROPERTY_PRICE_URL)
    raw = pd.read_csv(io.StringIO(csv_text), header=1)

    rename = {
        "Class A": "property_class_a",
        "Class A - Remarks": "property_class_a_remarks",
        "Class B": "property_class_b",
        "Class B - Remarks": "property_class_b_remarks",
        "Class C": "property_class_c",
        "Class C - Remarks": "property_class_c_remarks",
        "Class D": "property_class_d",
        "Class D - Remarks": "property_class_d_remarks",
        "Class E": "property_class_e",
        "Class E - Remarks": "property_class_e_remarks",
        "Classes A, B & C": "property_classes_abc",
        "Classes A, B & C - Remarks": "property_classes_abc_remarks",
        "Classes D & E": "property_classes_de",
        "Classes D & E - Remarks": "property_classes_de_remarks",
        "All Classes": "hk_property_price_idx",
        "All Classes - Remarks": "hk_property_price_remarks",
    }
    raw = raw.rename(columns=rename)
    raw["date"] = pd.to_datetime(raw["Month"], format="%m-%Y", errors="coerce")
    raw = raw.dropna(subset=["date"]).set_index("date").sort_index()

    value_cols = [
        "property_class_a",
        "property_class_b",
        "property_class_c",
        "property_class_d",
        "property_class_e",
        "property_classes_abc",
        "property_classes_de",
        "hk_property_price_idx",
    ]
    remark_cols = [
        "property_class_a_remarks",
        "property_class_b_remarks",
        "property_class_c_remarks",
        "property_class_d_remarks",
        "property_class_e_remarks",
        "property_classes_abc_remarks",
        "property_classes_de_remarks",
        "hk_property_price_remarks",
    ]

    for col in value_cols:
        raw[col] = pd.to_numeric(raw[col], errors="coerce")
    for col in remark_cols:
        raw[col] = raw[col].fillna("").astype(str).str.strip()

    out = raw[value_cols + remark_cols].copy()
    out.index.name = "date"
    return out


def _quarterly_remark(values: pd.Series) -> str:
    clean = [str(v).strip() for v in values if str(v).strip()]
    if not clean:
        return ""
    return "P" if "P" in clean else ";".join(sorted(set(clean)))


def _quarter_label(ts: pd.Timestamp) -> str:
    return f"{ts.year}Q{((ts.month - 1) // 3) + 1}"


def build_property_extension(
    macro_df: pd.DataFrame | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Build official HK residential property sidecars.

    Outputs:
      data/hk_property_price_rvd_monthly.csv
      data/hk_property_price_rvd_quarterly.csv
      data/hk_macro_quarterly_property_extension.csv
      data/hk_macro_quarterly_property_model.csv
      data/property_source_metadata.json
    """
    monthly = fetch_hk_property_price_rvd_monthly()
    monthly_path = os.path.join(DATA_DIR, "hk_property_price_rvd_monthly.csv")
    monthly.to_csv(monthly_path, float_format="%.4f")

    value_cols = [
        "property_class_a",
        "property_class_b",
        "property_class_c",
        "property_class_d",
        "property_class_e",
        "property_classes_abc",
        "property_classes_de",
        "hk_property_price_idx",
    ]
    remark_cols = [
        "property_class_a_remarks",
        "property_class_b_remarks",
        "property_class_c_remarks",
        "property_class_d_remarks",
        "property_class_e_remarks",
        "property_classes_abc_remarks",
        "property_classes_de_remarks",
        "hk_property_price_remarks",
    ]

    quarterly_values = monthly[value_cols].resample("QS").mean()
    quarterly_remarks = monthly[remark_cols].resample("QS").agg(_quarterly_remark)
    quarterly = quarterly_values.join(quarterly_remarks)
    quarterly = quarterly[quarterly.index >= "1998-01-01"].copy()
    quarterly["hk_property_price_yoy"] = (
        quarterly["hk_property_price_idx"].pct_change(4) * 100
    )
    quarterly["hk_property_price_qoq"] = (
        quarterly["hk_property_price_idx"].pct_change() * 100
    )
    quarterly["hk_property_price_qoq_ann"] = (
        (
            quarterly["hk_property_price_idx"]
            / quarterly["hk_property_price_idx"].shift(1)
        )
        ** 4
        - 1
    ) * 100
    quarterly.index.name = "date"

    quarterly_path = os.path.join(DATA_DIR, "hk_property_price_rvd_quarterly.csv")
    quarterly.to_csv(quarterly_path, float_format="%.4f")

    if macro_df is None:
        macro_path = os.path.join(DATA_DIR, "hk_macro_quarterly_real.csv")
        macro_df = pd.read_csv(macro_path, index_col="date", parse_dates=True)

    extension = macro_df.join(quarterly, how="left")
    extension.index.name = "date"
    extension_path = os.path.join(DATA_DIR, "hk_macro_quarterly_property_extension.csv")
    extension.to_csv(extension_path, float_format="%.4f")

    model_cols = list(macro_df.columns) + [
        "hk_property_price_yoy",
        "hk_property_price_qoq",
    ]
    model_ready = extension[model_cols].dropna()
    model_ready_path = os.path.join(DATA_DIR, "hk_macro_quarterly_property_model.csv")
    model_ready.to_csv(model_ready_path, float_format="%.4f")

    meta = {
        "source": "Rating and Valuation Department / data.gov.hk",
        "dataset": (
            "Private Domestic - Price Indices by Class "
            "(Territory-wide) [Monthly]"
        ),
        "url": PROPERTY_PRICE_URL,
        "raw_frequency": "monthly",
        "quarterly_transform": "quarterly mean of monthly index values",
        "main_measure": (
            "hk_property_price_idx = official RVD All Classes private domestic "
            "price index"
        ),
        "growth_measures": {
            "hk_property_price_yoy": (
                "4-quarter percent change in official All Classes index"
            ),
            "hk_property_price_qoq": (
                "1-quarter percent change in official All Classes index"
            ),
            "hk_property_price_qoq_ann": "annualized 1-quarter growth rate",
        },
        "monthly_range": (
            f"{monthly.index.min().strftime('%Y-%m')} to "
            f"{monthly.index.max().strftime('%Y-%m')}"
        ),
        "quarterly_range": (
            f"{_quarter_label(quarterly.index.min())} to "
            f"{_quarter_label(quarterly.index.max())}"
        ),
        "model_ready_range": (
            f"{_quarter_label(model_ready.index.min())} to "
            f"{_quarter_label(model_ready.index.max())}"
            if not model_ready.empty
            else "empty"
        ),
        "provisional_flag": (
            "RVD remark P means provisional. Quarterly remarks mark P if any "
            "month in the quarter is provisional."
        ),
        "role_in_project": (
            "Optional macro-finance extension. Keep outside the canonical "
            "seven-variable baseline until the research question is explicitly "
            "extended to property-market transmission."
        ),
    }
    with open(
        os.path.join(DATA_DIR, "property_source_metadata.json"),
        "w",
        encoding="utf-8",
    ) as fh:
        json.dump(meta, fh, indent=2)

    return monthly, quarterly, model_ready


def build_dataset() -> pd.DataFrame:
    """Fetch all series and merge into quarterly DataFrame."""
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

    print("[5/7] China real GDP growth YoY (OECD QNA; nominal FRED fallback)...")
    china = fetch_china_real_gdp_oecd()
    china_src = "OECD_QNA_B1GQ_GY" if china["china_gdp"].mean() < 15 else "FRED_nominal_fallback"
    print(f"       {len(china)} quarters ({china_src})")

    print("[6/7] HK CPI inflation (C&SD 510-60001; WB fallback if needed)...")
    cpi, cpi_source, cpi_lineage = fetch_hk_cpi()
    print(f"       {len(cpi)} quarters ({cpi_source})")

    print("[7/7] HK exports to Chinese Mainland YoY (C&SD 410-50013)...")
    exports = fetch_hk_exports_china()
    print(f"       {len(exports)} quarters")

    merged = gdp.join(cpi, how="outer")
    merged = merged.join(unemp, how="outer")
    merged = merged.join(hibor, how="outer")
    merged = merged.join(china, how="outer")
    merged = merged.join(ffr, how="outer")
    merged = merged.join(exports, how="outer")

    col_order = ["gdp_growth", "cpi_inflation", "unemployment",
                 "hibor_3m", "china_gdp", "us_ffr", "hk_exports_china_yoy"]
    merged = merged[[c for c in col_order if c in merged.columns]]
    merged = merged.dropna()
    merged.index.name = "date"

    lineage_path = os.path.join(DATA_DIR, "cpi_lineage.csv")
    cpi_lineage.to_csv(lineage_path)
    official_mask = cpi_lineage["source"].astype(str).str.startswith("official")
    official_share_full = float(official_mask.mean()) if len(cpi_lineage) else 0.0
    official_idx = cpi_lineage.index[official_mask]
    sample_idx = merged.index
    sample_lineage = cpi_lineage.reindex(sample_idx).dropna()
    official_share_sample = (
        float(sample_lineage["source"].astype(str).str.startswith("official").mean())
        if len(sample_lineage) else 0.0
    )
    official_window = (
        f"{official_idx.min().date()} to {official_idx.max().date()}"
        if len(official_idx) else "none"
    )
    print(
        "       CPI lineage -> "
        f"{lineage_path} (official share full={official_share_full:.1%}, "
        f"in-sample={official_share_sample:.1%})"
    )

    # Sidecar metadata for reproducibility
    meta = {
        "gdp_growth": "C&SD table 310-30001 (quarterly YoY %)",
        "cpi_inflation": (
            f"CPI source={cpi_source}; lineage_file=data/cpi_lineage.csv; "
            f"official_window={official_window}; "
            f"official_share_full={official_share_full:.1%}; "
            f"official_share_sample={official_share_sample:.1%}; "
            "C&SD table 510-60001 Composite CPI YoY monthly -> quarterly mean; "
            "WB annual spline only if official CPI unavailable"
        ),
        "unemployment": "C&SD table 210-06101 (SAUR/UR M3M -> quarterly end-of-quarter last, avoids double-smoothing of overlapping M3M windows)",
        "hibor_3m": (
            "HKMA hibor.fixing endperiod API (monthly -> quarterly mean); "
            "falls back to data/hibor_3m_quarterly.csv or the existing "
            "canonical panel if HKMA temporarily times out"
        ),
        "china_gdp": (
            "OECD QNA CHN.B1_GE.GPSA.Q, B1GQ (GDP at market prices), "
            "GY transformation (YoY % growth), quarterly; "
            "falls back to FRED CHNGDPNQDSMEI nominal CNY GDP YoY if OECD unavailable"
        ),
        "us_ffr": "FRED FEDFUNDS monthly -> quarterly mean",
        "hk_exports_china_yoy": (
            "C&SD table 410-50013: total exports to Chinese Mainland, "
            "monthly YoY % -> quarterly mean; cached to data/hk_exports_china_quarterly.csv"
        ),
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

    print("\n[sidecar] HK residential property prices (RVD/data.gov.hk)...")
    _, q_property, q_property_model = build_property_extension(df)
    print(
        "       property quarterly sidecar: "
        f"{len(q_property)} quarters; model-ready: {len(q_property_model)} quarters"
    )
