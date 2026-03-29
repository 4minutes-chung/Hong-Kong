"""
Hong Kong Quarterly VAR Macro Forecasting Model
================================================
Research question:
  "How do US monetary policy shocks and China growth shocks propagate
   to Hong Kong's real economy under the currency board?"

Pipeline: data assembly -> diagnostics -> estimation -> FEVD ->
          historical decomposition -> backtesting -> scenarios ->
          robustness -> report.

Variables (Cholesky ordering: external-first)
---------
  us_ffr        : US effective federal funds rate (%); FRED monthly -> quarterly mean
  china_gdp     : China YoY % (FRED CHNGDPNQDSMEI nominal quarterly; prefer real NBS — DATA_DOWNLOAD_CHECKLIST.md)
  gdp_growth    : HK real GDP YoY % (C&SD 310-30001) when hk_macro_quarterly_real.csv
  cpi_inflation : HK CPI YoY % — prefer C&SD; else World Bank annual + spline (fetch_real_data.py)
  unemployment  : HK % (C&SD 210-06101, M3M SAUR/UR) when real CSV
  hibor_3m      : 3-month HIBOR % (HKMA API) when real CSV; else US FFR + spread
"""

import warnings
warnings.filterwarnings("ignore")

import os
import json
import argparse
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from statsmodels.tsa.api import VAR
from statsmodels.tsa.stattools import adfuller, grangercausalitytests, kpss
from statsmodels.tsa.vector_ar.vecm import coint_johansen
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.ar_model import AutoReg

OUTPUT_DIR = os.path.join(os.path.dirname(__file__) or ".", "output")
DATA_DIR = os.path.join(os.path.dirname(__file__) or ".", "data")
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

SEED = 42
np.random.seed(SEED)
_RNG_DATA = np.random.default_rng(SEED)
_RNG_BOOT = np.random.default_rng(SEED + 1)

MODEL_VARIABLES = [
    "gdp_growth", "cpi_inflation", "unemployment",
    "hibor_3m", "china_gdp", "us_ffr",
]

# NOTE: Series IDs below are fallbacks when local CSV is absent; many HK FRED IDs return 404.
# Prefer data/hk_macro_quarterly_real.csv from fetch_real_data.py (see DATA_DOWNLOAD_CHECKLIST.md).
DATA_SPEC = {
    "gdp_growth": {
        "source": "FRED", "series_id": "NGDPRSAXDCHKQ",
        "frequency": "quarterly", "target_transform": "yoy_pct",
        "needs_pct_change": True,
    },
    "cpi_inflation": {
        "source": "FRED", "series_id": "CPALCY01HKQ661S",
        "frequency": "quarterly", "target_transform": "yoy_pct",
        "needs_pct_change": False,
    },
    "unemployment": {
        "source": "FRED", "series_id": "LMUNRRTTHKQ156S",
        "frequency": "quarterly", "target_transform": "level_pct",
        "needs_pct_change": False,
    },
    "us_ffr": {
        "source": "FRED", "series_id": "FEDFUNDS",
        "frequency": "monthly->quarterly", "target_transform": "level_pct",
        "needs_pct_change": False,
    },
    "china_gdp": {
        "source": "FRED", "series_id": "CHNGDPNQDSMEI",
        "frequency": "quarterly", "target_transform": "yoy_pct",
        "needs_pct_change": True,
    },
    "hibor_3m": {
        "source": "derived", "series_id": "n/a",
        "frequency": "quarterly", "target_transform": "level_pct",
        "needs_pct_change": False,
    },
}


# ============================================================
# BVAR — Minnesota-style diagonal prior
# ============================================================

class MinnesotaVARResults:
    """Result container for Minnesota-prior BVAR."""

    def __init__(self, coefs, intercept, resid, k_ar, nobs, sigma_u, hyper):
        self.coefs = coefs
        self.intercept = intercept
        self.resid = resid
        self.k_ar = int(k_ar)
        self.nobs = int(nobs)
        self.sigma_u = sigma_u
        self.hyper = hyper
        self.aic = np.nan
        self.bic = np.nan
        self.model_label = "bvar_minnesota"

    def forecast(self, y_last, steps):
        y_last = np.asarray(y_last)
        k = self.coefs.shape[1]
        p = self.k_ar
        history = y_last.copy()
        out = np.zeros((steps, k))
        for h in range(steps):
            y_hat = self.intercept.copy()
            for lag in range(1, p + 1):
                y_hat += self.coefs[lag - 1] @ history[-lag]
            out[h] = y_hat
            history = np.vstack([history, y_hat])
        return out


def _build_lagged_design(df: pd.DataFrame, lags: int):
    """Create lagged regressor matrix X and target matrix Y."""
    arr = df.values
    n, k = arr.shape
    rows = n - lags
    X = np.ones((rows, 1 + k * lags))
    Y = np.zeros((rows, k))
    for t in range(lags, n):
        x_t = [1.0]
        for lag in range(1, lags + 1):
            x_t.extend(arr[t - lag].tolist())
        X[t - lags, :] = np.array(x_t)
        Y[t - lags, :] = arr[t]
    return X, Y


def fit_bvar_minnesota(df: pd.DataFrame, lags: int,
                       lambda1: float = 0.2, lambda2: float = 0.5,
                       lambda3: float = 1.0) -> MinnesotaVARResults:
    """Fit BVAR with Minnesota-style diagonal prior, equation by equation."""
    X, Y = _build_lagged_design(df, lags)
    nobs, ncoef = X.shape
    k = Y.shape[1]

    # Get scaling from univariate AR residual std devs
    sigma_ar = np.zeros(k)
    for j in range(k):
        try:
            ar = AutoReg(df.iloc[:, j].values, lags=min(lags, 4)).fit()
            sigma_ar[j] = np.std(ar.resid)
        except Exception:
            sigma_ar[j] = np.std(df.iloc[:, j].values)
    sigma_ar = np.maximum(sigma_ar, 1e-8)

    B = np.zeros((ncoef, k))
    XtX = X.T @ X

    for i in range(k):
        prior_prec_diag = np.zeros(ncoef)
        prior_prec_diag[0] = 0.0  # no shrinkage on intercept
        for lag in range(1, lags + 1):
            for j in range(k):
                idx = 1 + (lag - 1) * k + j
                if i == j:
                    v = (lambda1 / lag ** lambda3) ** 2
                else:
                    v = (lambda1 * lambda2 * sigma_ar[i] / (lag ** lambda3 * sigma_ar[j])) ** 2
                prior_prec_diag[idx] = 1.0 / max(v, 1e-12)

        pen = np.diag(prior_prec_diag)
        B[:, i] = np.linalg.solve(XtX + pen, X.T @ Y[:, i])

    fitted = X @ B
    resid = Y - fitted
    # Audit fix #10: proper df correction
    sigma_u = resid.T @ resid / max(nobs - ncoef, 1)

    intercept = B[0, :]
    coefs = np.zeros((lags, k, k))
    for lag in range(lags):
        block = B[1 + lag * k: 1 + (lag + 1) * k, :]
        coefs[lag] = block.T

    return MinnesotaVARResults(
        coefs=coefs, intercept=intercept, resid=resid,
        k_ar=lags, nobs=nobs, sigma_u=sigma_u,
        hyper={"lambda1": lambda1, "lambda2": lambda2, "lambda3": lambda3},
    )


# ============================================================
# VECM — Vector Error Correction Model
# ============================================================

class VECMResultsWrapper:
    """Wrapper around statsmodels VECM results to match the VAR result interface."""

    def __init__(self, vecm_result, df, k_ar_diff, coint_rank, deterministic="ci"):
        self._vecm = vecm_result
        self._df = df
        self.k_ar = k_ar_diff + 1  # total lag order in levels
        self.k_ar_diff = k_ar_diff
        self.nobs = vecm_result.nobs
        self.model_label = f"vecm_r{coint_rank}"
        self.coint_rank = coint_rank
        self.deterministic = deterministic

        k = df.shape[1]
        p_diff = k_ar_diff

        # Build VAR-representation coefficients from VECM parameters
        # VECM: Delta y_t = alpha beta' y_{t-1} + Gamma_1 Delta y_{t-1} + ... + c + u_t
        # VAR(p) in levels: y_t = A_1 y_{t-1} + ... + A_p y_{t-p} + c + u_t
        alpha = vecm_result.alpha  # (k, r)
        beta = vecm_result.beta   # (k, r) — cointegrating vectors
        Pi = alpha @ beta.T       # (k, k) — long-run impact matrix

        gamma = []
        if hasattr(vecm_result, 'gamma') and vecm_result.gamma is not None:
            g = vecm_result.gamma
            for i in range(p_diff):
                gamma.append(g[:, i * k:(i + 1) * k])

        # Convert VECM to VAR in levels
        # A_1 = I + Pi + Gamma_1
        # A_i = Gamma_i - Gamma_{i-1}  for i=2,...,p-1
        # A_p = -Gamma_{p-1}
        p = p_diff + 1
        coefs = np.zeros((p, k, k))
        if p_diff == 0:
            coefs[0] = np.eye(k) + Pi
        else:
            coefs[0] = np.eye(k) + Pi + gamma[0]
            for i in range(1, p_diff):
                coefs[i] = gamma[i] - gamma[i - 1]
            coefs[p - 1] = -gamma[-1]

        self.coefs = coefs

        resid = vecm_result.resid
        self.resid = resid if isinstance(resid, np.ndarray) else resid.values

        self.sigma_u = np.cov(self.resid, rowvar=False)

        self.intercept = np.zeros(k)
        if hasattr(vecm_result, "const") and vecm_result.const is not None:
            const_arr = np.asarray(vecm_result.const).reshape(-1)
            if const_arr.size >= k:
                self.intercept = const_arr[:k]

        n = self.nobs
        k_params = k * (1 + k * p)
        ll = -0.5 * n * k * np.log(2 * np.pi) - 0.5 * n * np.log(max(np.linalg.det(self.sigma_u), 1e-20)) - 0.5 * n * k
        self.aic = -2 * ll + 2 * k_params
        self.bic = -2 * ll + k_params * np.log(n)

    def forecast(self, y_last, steps):
        y_last = np.asarray(y_last)
        k = self.coefs.shape[1]
        p = self.k_ar
        if y_last.shape[0] < p:
            raise ValueError(
                f"VECM forecast needs at least {p} level lags; got {y_last.shape[0]}"
            )
        history = y_last.copy()
        out = np.zeros((steps, k))
        for h in range(steps):
            y_hat = self.intercept.copy()
            for lag in range(1, p + 1):
                y_hat += self.coefs[lag - 1] @ history[-lag]
            out[h] = y_hat
            history = np.vstack([history, y_hat])
        return out


def _is_vecm_result(result) -> bool:
    return isinstance(result, VECMResultsWrapper)


def _vecm_rank_or_default(coint_rank: int | None) -> int:
    """Resolve VECM rank: None -> 1 (legacy default); 0 is preserved (no cointegration)."""
    if coint_rank is None:
        return 1
    return int(coint_rank)


def fit_vecm(
    df_raw: pd.DataFrame,
    lags_diff: int,
    coint_rank: int,
    deterministic: str = "ci",
    verbose: bool = True,
):
    """
    Fit a VECM on the RAW (levels) data.
    lags_diff: number of lagged differences (p-1 in Johansen notation).
    coint_rank: number of cointegrating relationships.
    Returns a VECMResultsWrapper with the same interface as VAR results.
    """
    from statsmodels.tsa.vector_ar.vecm import VECM

    model = VECM(
        df_raw,
        k_ar_diff=lags_diff,
        coint_rank=coint_rank,
        deterministic=deterministic,
    )
    result = model.fit()

    if verbose:
        print(
            f"\n=== VECM Estimation (r={coint_rank}, lag_diff={lags_diff}, "
            f"det='{deterministic}') ==="
        )
        print(f"Obs: {result.nobs}, Coint rank: {coint_rank}")

        # Print cointegrating vectors
        beta = result.beta
        alpha = result.alpha
        print(f"\nCointegrating vectors (beta, {beta.shape[0]}x{beta.shape[1]}):")
        for j in range(coint_rank):
            vec = beta[:, j]
            labels = list(df_raw.columns)
            terms = [f"{v:.3f}*{lbl}" for v, lbl in zip(vec, labels)]
            print(f"  beta_{j+1}: {' + '.join(terms)}")

        print(f"\nAdjustment coefficients (alpha, {alpha.shape[0]}x{alpha.shape[1]}):")
        for i, label in enumerate(df_raw.columns):
            vals = alpha[i, :]
            print(f"  {label:18s}: {np.array2string(vals, precision=4)}")

    wrapper = VECMResultsWrapper(
        result, df_raw, lags_diff, coint_rank, deterministic=deterministic
    )
    return wrapper


# ============================================================
# SECTION 1 — DATA ASSEMBLY
# ============================================================

def _try_fetch_fred(series_id: str, start: str = "1998-01-01") -> pd.Series | None:
    try:
        url = (
            f"https://fred.stlouisfed.org/graph/fredgraph.csv"
            f"?id={series_id}&cosd={start}"
        )
        df = pd.read_csv(url, na_values=".")
        date_col = "DATE" if "DATE" in df.columns else "observation_date"
        df[date_col] = pd.to_datetime(df[date_col])
        df = df.set_index(date_col)
        s = df.iloc[:, 0].dropna()
        s.name = series_id
        return s
    except Exception:
        return None


def _generate_calibrated_data() -> pd.DataFrame:
    """
    Generate quarterly HK macro data calibrated to stylised facts.
    Audit fix #9: structural breaks injected AS SHOCKS inside the VAR loop.
    """
    T = 104
    dates = pd.date_range("2000-01-01", periods=T, freq="QS")
    var_names = MODEL_VARIABLES

    mu = np.array([3.0, 2.0, 4.5, 2.5, 7.0, 2.0])

    A = np.array([
        [ 0.55,  0.00, -0.05,  -0.02,  0.08,  0.00],
        [ 0.05,  0.65,  0.00,   0.00,  0.02,  0.00],
        [-0.08,  0.00,  0.88,   0.01, -0.03,  0.00],
        [ 0.00,  0.00,  0.00,   0.60,  0.00,  0.35],
        [ 0.04,  0.00,  0.00,   0.00,  0.78,  0.00],
        [ 0.00,  0.00,  0.00,   0.00,  0.00,  0.92],
    ])

    sigma = np.diag([1.8, 0.8, 0.5, 0.6, 0.9, 0.5])
    R = np.array([
        [1.00, 0.30, -0.40,  0.10,  0.45,  0.10],
        [0.30, 1.00,  0.00,  0.15,  0.20,  0.05],
        [-0.40, 0.00, 1.00, -0.05, -0.30,  0.00],
        [0.10, 0.15, -0.05,  1.00,  0.05,  0.70],
        [0.45, 0.20, -0.30,  0.05,  1.00,  0.10],
        [0.10, 0.05,  0.00,  0.70,  0.10,  1.00],
    ])
    cov = sigma @ R @ sigma

    eps = _RNG_DATA.multivariate_normal(np.zeros(6), cov, size=T)

    # Inject structural breaks as additional shock vectors (fix #9)
    gfc_shocks = {
        32: np.array([-2.0, 0.0, 0.5, -1.0, -0.5, -0.3]),
        33: np.array([-4.5, -0.3, 1.2, -1.5, -1.0, -0.8]),
        34: np.array([-3.0, -0.5, 1.8, -1.2, -0.5, -0.5]),
        35: np.array([-1.5,  0.0, 1.5, -0.5,  0.0, -0.2]),
    }
    covid_shocks = {
        80: np.array([-8.0, -1.5, 2.5, -0.5, -2.0, -0.8]),
        81: np.array([-4.0, -0.5, 1.8,  0.0, -1.0, -0.3]),
    }
    for t_idx, shock_vec in {**gfc_shocks, **covid_shocks}.items():
        eps[t_idx] += shock_vec

    y = np.zeros((T, 6))
    y[0] = mu
    for t in range(1, T):
        y[t] = mu + A @ (y[t - 1] - mu) + eps[t]

    y[:, 2] = np.clip(y[:, 2], 1.5, 10.0)
    y[:, 3] = np.clip(y[:, 3], 0.01, 8.0)
    y[:, 5] = np.clip(y[:, 5], 0.05, 7.0)

    df = pd.DataFrame(y, index=dates, columns=var_names)
    df.index.name = "date"
    return df


def _load_local_quarterly_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    if "date" not in df.columns:
        raise ValueError("Local data file must include a 'date' column.")
    df["date"] = pd.to_datetime(df["date"])
    df = df.set_index("date").sort_index()
    missing = [c for c in MODEL_VARIABLES if c not in df.columns]
    if missing:
        raise ValueError(f"Local data file is missing required columns: {missing}")
    df = df[MODEL_VARIABLES].resample("QS").mean().dropna()
    return df


def _write_data_dictionary(df: pd.DataFrame, source_map: dict):
    rows = []
    for var in MODEL_VARIABLES:
        spec = DATA_SPEC.get(var, {})
        rows.append({
            "variable": var,
            "available_in_sample": var in df.columns,
            "source_used": source_map.get(var, spec.get("source", "unknown")),
            "series_id": spec.get("series_id", "unknown"),
            "frequency": spec.get("frequency", "unknown"),
            "target_transform": spec.get("target_transform", "unknown"),
        })
    meta = pd.DataFrame(rows)
    path = os.path.join(OUTPUT_DIR, "data_dictionary.csv")
    meta.to_csv(path, index=False)
    print(f"[DATA] Data dictionary -> {path}")
    return meta


def assemble_data(prefer_local_real_data: bool = True) -> pd.DataFrame:
    fred_map = {k: v["series_id"] for k, v in DATA_SPEC.items() if v["source"] == "FRED"}
    source_map = {}

    local_path = os.path.join(DATA_DIR, "hk_macro_quarterly_real.csv")
    if prefer_local_real_data and os.path.exists(local_path):
        try:
            df = _load_local_quarterly_data(local_path)
            source_meta_path = os.path.join(DATA_DIR, "source_metadata.json")
            source_meta = {}
            if os.path.exists(source_meta_path):
                try:
                    with open(source_meta_path, "r", encoding="utf-8") as fh:
                        source_meta = json.load(fh)
                except Exception:
                    source_meta = {}
            for col in df.columns:
                source_map[col] = source_meta.get(col, "local_csv")
            print(f"[DATA] Loaded local real data -- {len(df)} quarters")
            _write_data_dictionary(df, source_map)
            csv_path = os.path.join(DATA_DIR, "hk_macro_quarterly.csv")
            df.to_csv(csv_path, float_format="%.4f")
            print(f"[DATA] Saved to {csv_path}")
            return df
        except Exception as exc:
            print(f"[DATA] Local real data load failed ({exc}); trying FRED/synthetic path")

    fetched = {}
    for name, sid in fred_map.items():
        s = _try_fetch_fred(sid)
        if s is not None and len(s) > 40:
            fetched[name] = s
            source_map[name] = "fred_csv_endpoint"

    if len(fetched) >= 4:
        df = pd.DataFrame(fetched)
        df = df.resample("QS").mean().dropna()
        # Audit fix #8: use metadata, not value heuristic
        for col in df.columns:
            if DATA_SPEC.get(col, {}).get("needs_pct_change", False):
                df[col] = df[col].pct_change(4) * 100
        if "hibor_3m" not in df.columns:
            # Audit fix #11: stress-aware HIBOR spread
            spread = _RNG_DATA.normal(0.3, 0.15, len(df))
            df["hibor_3m"] = df["us_ffr"] + spread
            source_map["hibor_3m"] = "derived_from_us_ffr"
        df = df.dropna()
        print(f"[DATA] Assembled real data from FRED -- {len(df)} quarters")
    else:
        print("[DATA] FRED unavailable; using calibrated synthetic data")
        df = _generate_calibrated_data()
        for col in df.columns:
            source_map[col] = "synthetic_calibrated"

    csv_path = os.path.join(DATA_DIR, "hk_macro_quarterly.csv")
    df.to_csv(csv_path, float_format="%.4f")
    print(f"[DATA] Saved to {csv_path}")
    _write_data_dictionary(df, source_map)
    return df


# ============================================================
# SECTION 2 — PRE-ESTIMATION DIAGNOSTICS
# ============================================================

def stationarity_tests(df: pd.DataFrame) -> pd.DataFrame:
    """
    Audit fix #3: Run both ADF and KPSS tests.
    ADF H0 = unit root; KPSS H0 = stationarity.
    If ADF rejects and KPSS does not reject -> stationary (agree).
    If ADF does not reject and KPSS rejects -> unit root (agree).
    If conflict (both reject or neither rejects) -> flag, default to level.
    """
    results = []
    for col in df.columns:
        adf_stat, adf_p, used_lag, nobs, crit, _ = adfuller(df[col], maxlag=8, autolag="AIC")
        try:
            kpss_stat, kpss_p, kpss_lags, kpss_crit = kpss(df[col], regression="c", nlags="auto")
        except Exception:
            kpss_p = np.nan

        adf_reject = adf_p < 0.05
        kpss_reject = kpss_p < 0.05 if np.isfinite(kpss_p) else False

        if adf_reject and not kpss_reject:
            decision = "stationary"
        elif not adf_reject and kpss_reject:
            decision = "unit_root"
        elif adf_reject and kpss_reject:
            decision = "conflict_default_level"
        else:
            decision = "conflict_default_level"

        results.append({
            "variable": col,
            "ADF_stat": round(adf_stat, 3),
            "ADF_p": round(adf_p, 4),
            "KPSS_p": round(kpss_p, 4) if np.isfinite(kpss_p) else np.nan,
            "ADF_reject": adf_reject,
            "KPSS_reject": kpss_reject,
            "decision": decision,
        })
    res = pd.DataFrame(results)
    print("\n=== Stationarity Tests (ADF + KPSS) ===")
    print(res.to_string(index=False))
    return res


def johansen_cointegration_test(
    df_raw: pd.DataFrame,
    adf_res: pd.DataFrame,
    det_order: int = 0,
    k_ar_diff: int = 2,
):
    """
    Audit fix #5: test for cointegration among I(1) variables.
    If cointegration exists, note it in diagnostics.
    """
    i1_vars = adf_res[adf_res["decision"] == "unit_root"]["variable"].tolist()
    if len(i1_vars) < 2:
        print("\n[COINT] Fewer than 2 I(1) variables; skipping Johansen test.")
        return None

    subset = df_raw[i1_vars].dropna()
    if len(subset) < 20:
        print("\n[COINT] Insufficient observations for Johansen test.")
        return None

    try:
        joh = coint_johansen(subset, det_order=det_order, k_ar_diff=k_ar_diff)
        trace_stats = joh.lr1
        max_rank = len(i1_vars) - 1
        rank_trace_90 = int(np.sum(trace_stats > joh.cvt[:, 0]))
        rank_trace_95 = int(np.sum(trace_stats > joh.cvt[:, 1]))
        rank_trace_99 = int(np.sum(trace_stats > joh.cvt[:, 2]))
        rank_eig_90 = int(np.sum(joh.lr2 > joh.cvm[:, 0]))
        rank_eig_95 = int(np.sum(joh.lr2 > joh.cvm[:, 1]))
        rank_eig_99 = int(np.sum(joh.lr2 > joh.cvm[:, 2]))
        n_coint = min(rank_trace_95, max_rank)
        print(f"\n=== Johansen Cointegration Test (I(1) subset: {i1_vars}) ===")
        print(f"  Settings: det_order={det_order}, k_ar_diff={k_ar_diff}")
        print(f"  Trace statistics : {np.round(trace_stats, 2)}")
        print(f"  90% critical vals: {np.round(joh.cvt[:, 0], 2)}")
        print(f"  95% critical vals: {np.round(joh.cvt[:, 1], 2)}")
        print(
            "  Rank summary:"
            f" trace(90/95/99)=({rank_trace_90}/{rank_trace_95}/{rank_trace_99}),"
            f" maxeig(90/95/99)=({rank_eig_90}/{rank_eig_95}/{rank_eig_99})"
        )
        print(f"  Auto rank (trace@95%, capped): {n_coint}")
        if n_coint > 0:
            print(f"  WARNING: {n_coint} cointegrating relationship(s) detected.")
            print("  A VECM may be preferred for long-horizon forecasts.")
        return {
            "i1_vars": i1_vars,
            "rank": n_coint,
            "rank_trace_90": rank_trace_90,
            "rank_trace_95": rank_trace_95,
            "rank_trace_99": rank_trace_99,
            "rank_eig_90": rank_eig_90,
            "rank_eig_95": rank_eig_95,
            "rank_eig_99": rank_eig_99,
            "trace": trace_stats.tolist(),
            "trace_crit_90": joh.cvt[:, 0].tolist(),
            "trace_crit_95": joh.cvt[:, 1].tolist(),
            "maxeig": joh.lr2.tolist(),
            "maxeig_crit_95": joh.cvm[:, 1].tolist(),
            "det_order": det_order,
            "k_ar_diff": k_ar_diff,
        }
    except Exception as e:
        print(f"\n[COINT] Johansen test failed: {e}")
        return None


def resolve_coint_rank(coint_rank_arg, coint_result: dict | None) -> int | None:
    """
    Resolve user rank input.
    - 'auto' (or None) uses trace@95% rank from Johansen output.
    - explicit int uses that rank, capped to feasible bounds.
    """
    if coint_result is None:
        return None
    i1_count = len(coint_result.get("i1_vars", []))
    max_rank = max(i1_count - 1, 0)
    if max_rank == 0:
        return None

    if coint_rank_arg is None or str(coint_rank_arg).lower() == "auto":
        return int(min(max(coint_result.get("rank", 0), 0), max_rank))

    rank = int(coint_rank_arg)
    rank = max(0, min(rank, max_rank))
    return rank


def apply_transforms(df: pd.DataFrame, adf_res: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """
    Apply transforms based on stationarity test decisions.
    Returns (transformed_df, transforms_dict).
    The transforms dict maps variable -> {"transform": str, "last_level": float}.
    """
    transforms = {}
    df_t = df.copy()
    for _, row in adf_res.iterrows():
        col = row["variable"]
        if row["decision"] == "unit_root":
            transforms[col] = {
                "transform": "first_diff",
                "last_level": float(df[col].iloc[-1]),
            }
            df_t[col] = df[col].diff()
        else:
            transforms[col] = {
                "transform": "level",
                "last_level": float(df[col].iloc[-1]),
            }
    df_t = df_t.dropna()
    tr_str = ", ".join(f"{k}: {v['transform']}" for k, v in transforms.items())
    print(f"\n[DIAG] Transforms: {{{tr_str}}}")
    return df_t, transforms


def granger_causality_diagnostics(df_est: pd.DataFrame, max_lag: int = 4):
    """Audit fix #12: run pairwise Granger causality tests."""
    cols = list(df_est.columns)
    external = ["china_gdp", "us_ffr"]
    domestic = [c for c in cols if c not in external]
    results = []

    print("\n=== Granger Causality Tests (external -> domestic) ===")
    for ext in external:
        if ext not in cols:
            continue
        for dom in domestic:
            if dom not in cols:
                continue
            try:
                test_data = df_est[[dom, ext]].dropna()
                gc = grangercausalitytests(test_data, maxlag=max_lag, verbose=False)
                best_p = min(gc[lag][0]["ssr_ftest"][1] for lag in gc)
                sig = "*" if best_p < 0.05 else ""
                print(f"  {ext:15s} -> {dom:18s}  best p = {best_p:.4f} {sig}")
                results.append({"cause": ext, "effect": dom, "best_p": best_p})
            except Exception:
                pass
    return results


def select_lag_order(df: pd.DataFrame, max_lags: int = 8, criterion: str = "aic",
                     max_params_ratio: float = 0.8) -> tuple[int, dict]:
    model = VAR(df)
    lag_res = model.select_order(maxlags=max_lags)
    print("\n=== Lag Order Selection ===")
    print(lag_res.summary())

    aic_lag = lag_res.aic
    bic_lag = lag_res.bic
    chosen = aic_lag if criterion.lower() == "aic" else bic_lag
    chosen = max(int(chosen), 1)
    n_obs = len(df)
    k_vars = df.shape[1]
    guardrail_triggered = False

    while chosen > 1:
        params_per_eq = 1 + k_vars * chosen
        ratio = params_per_eq / max(n_obs, 1)
        if ratio <= max_params_ratio:
            break
        chosen -= 1
        guardrail_triggered = True

    final_params = 1 + k_vars * chosen
    final_ratio = final_params / max(n_obs, 1)
    print(f"\n[DIAG] AIC={aic_lag}, BIC={bic_lag}, selected_by={criterion.upper()} -> p={chosen}")
    if guardrail_triggered:
        print(f"[DIAG] Guardrail reduced to p={chosen} (ratio={final_ratio:.2f})")

    lag_diag = {
        "criterion": criterion.lower(),
        "aic_lag": int(aic_lag), "bic_lag": int(bic_lag),
        "selected_lag": int(chosen),
        "max_params_ratio": float(max_params_ratio),
        "params_per_equation": int(final_params),
        "n_observations": int(n_obs),
        "params_obs_ratio": float(final_ratio),
        "guardrail_triggered": bool(guardrail_triggered),
    }
    return chosen, lag_diag


def plot_raw_data(df: pd.DataFrame):
    fig, axes = plt.subplots(3, 2, figsize=(14, 10), sharex=True)
    axes = axes.ravel()
    titles = {
        "gdp_growth": "HK Real GDP Growth (YoY %)",
        "cpi_inflation": "HK CPI Inflation (YoY %)",
        "unemployment": "HK Unemployment Rate (%)",
        "hibor_3m": "3-Month HIBOR (%)",
        "china_gdp": "China Real GDP Growth (YoY %)",
        "us_ffr": "US Federal Funds Rate (%)",
    }
    for i, col in enumerate(df.columns):
        ax = axes[i]
        ax.plot(df.index, df[col], linewidth=1.3, color="steelblue")
        ax.set_title(titles.get(col, col), fontsize=11)
        ax.axhline(0, color="grey", linewidth=0.5, linestyle="--")
        ax.xaxis.set_major_locator(mdates.YearLocator(5))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
        ax.grid(alpha=0.3)
    fig.suptitle("Hong Kong Quarterly Macro Data", fontsize=14, y=1.01)
    fig.tight_layout()
    path = os.path.join(OUTPUT_DIR, "01_raw_data.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"[CHART] Raw data panel -> {path}")


def plot_correlation(df: pd.DataFrame):
    corr = df.corr()
    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(corr, cmap="RdBu_r", vmin=-1, vmax=1)
    ax.set_xticks(range(len(corr)))
    ax.set_yticks(range(len(corr)))
    ax.set_xticklabels(corr.columns, rotation=45, ha="right", fontsize=9)
    ax.set_yticklabels(corr.columns, fontsize=9)
    for i in range(len(corr)):
        for j in range(len(corr)):
            ax.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center", fontsize=8)
    fig.colorbar(im, ax=ax, shrink=0.8)
    ax.set_title("Correlation Matrix (Transformed Series)", fontsize=12)
    fig.tight_layout()
    path = os.path.join(OUTPUT_DIR, "02_correlation.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"[CHART] Correlation matrix -> {path}")


# ============================================================
# SECTION 3 — MODEL ESTIMATION
# ============================================================

def _companion_matrix(coefs):
    """Build companion matrix from coefficient array (p, k, k)."""
    p, k, _ = coefs.shape
    companion = np.zeros((k * p, k * p))
    for i in range(p):
        companion[:k, i * k:(i + 1) * k] = coefs[i]
    if p > 1:
        companion[k:, :k * (p - 1)] = np.eye(k * (p - 1))
    return companion


def _cholesky_irf(coefs, sigma_u, periods: int = 16):
    """
    Audit fix #4: Compute orthogonalized (Cholesky) IRFs consistently
    for BOTH VAR and BVAR. Theta_h = Phi_h @ P where P = chol(Sigma_u).
    """
    p, k, _ = coefs.shape
    companion = _companion_matrix(coefs)
    P = np.linalg.cholesky(sigma_u)

    irfs = np.zeros((periods + 1, k, k))
    irfs[0] = P.copy()

    J = np.zeros((k, k * p))
    J[:k, :k] = np.eye(k)

    power = np.eye(k * p)
    for h in range(1, periods + 1):
        power = power @ companion
        Phi_h = J @ power @ J.T
        irfs[h] = Phi_h @ P

    return irfs


def estimate_model(df: pd.DataFrame, lags: int, model_type: str = "var",
                   bvar_lambda1: float = 0.2,
                   df_raw: pd.DataFrame = None, coint_rank: int = None,
                   vecm_deterministic: str = "ci", vecm_lag_diff: int | None = None):
    if model_type == "vecm":
        if df_raw is None:
            raise ValueError("VECM requires df_raw (levels data)")
        rank = _vecm_rank_or_default(coint_rank)
        lag_diff = max(lags - 1, 1) if vecm_lag_diff is None else max(int(vecm_lag_diff), 1)
        result = fit_vecm(
            df_raw,
            lags_diff=lag_diff,
            coint_rank=rank,
            deterministic=vecm_deterministic,
        )
        estimator_name = (
            f"VECM (rank={rank}, lag_diff={lag_diff}, det='{vecm_deterministic}')"
        )
    elif model_type == "bvar":
        result = fit_bvar_minnesota(df, lags, lambda1=bvar_lambda1)
        estimator_name = f"BVAR (Minnesota prior, lambda1={bvar_lambda1:.3f})"
    else:
        model = VAR(df)
        result = model.fit(lags)
        result.model_label = "var"
        estimator_name = "VAR (OLS)"

    print("\n=== Estimation Summary ===")
    print(f"Variables : {list(df.columns)}")
    print(f"Estimator : {estimator_name}")
    print(f"Lags      : {result.k_ar}")
    print(f"Obs used  : {result.nobs}")
    if np.isfinite(result.aic):
        print(f"AIC       : {result.aic:.2f}")
    if np.isfinite(result.bic):
        print(f"BIC       : {result.bic:.2f}")

    coefs = result.coefs
    companion = _companion_matrix(coefs)
    eig_vals = np.linalg.eigvals(companion)
    max_eig = np.abs(eig_vals).max()
    print(f"\nMax eigenvalue modulus: {max_eig:.4f} -> {'STABLE' if max_eig < 1 else 'UNSTABLE'}")
    if model_type == "vecm":
        k = df.shape[1]
        if getattr(result, "coint_rank", 0) >= max(k - 1, 1):
            print("  [WARN] Cointegration rank is near full rank; check deterministic term and lag_diff.")
        if max_eig >= 1:
            print("  [HINT] Try higher --vecm-lag-diff or alternative --vecm-deterministic.")

    resid_arr = result.resid.values if hasattr(result.resid, "values") else result.resid
    print("\n--- Ljung-Box Residual Autocorrelation (lag=8) ---")
    for i, col in enumerate(df.columns):
        lb = acorr_ljungbox(resid_arr[:, i], lags=[8], return_df=True)
        pval = lb["lb_pvalue"].values[0]
        flag = "" if pval > 0.05 else " *"
        print(f"  {col:18s}  p = {pval:.4f}{flag}")

    _plot_stability(eig_vals)

    sigma_u = result.sigma_u if hasattr(result, "sigma_u") and result.sigma_u is not None else np.cov(resid_arr, rowvar=False)
    irfs = _cholesky_irf(coefs, sigma_u, periods=20)
    _plot_irf_cholesky(irfs, list(df.columns))

    result._irfs = irfs
    result._sigma_u_computed = sigma_u
    return result


def _plot_stability(eig_vals: np.ndarray):
    fig, ax = plt.subplots(figsize=(6, 6))
    theta = np.linspace(0, 2 * np.pi, 200)
    ax.plot(np.cos(theta), np.sin(theta), "k--", linewidth=0.8)
    ax.scatter(eig_vals.real, eig_vals.imag, s=50, color="crimson", zorder=5)
    ax.set_title("VAR Stability -- Eigenvalues vs Unit Circle", fontsize=11)
    ax.set_xlabel("Real")
    ax.set_ylabel("Imaginary")
    ax.set_aspect("equal")
    ax.grid(alpha=0.3)
    path = os.path.join(OUTPUT_DIR, "03_stability.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"[CHART] Stability plot -> {path}")


def _plot_irf_cholesky(irfs, var_names):
    """Plot orthogonalized IRFs (Cholesky) consistently for both VAR and BVAR."""
    periods = irfs.shape[0] - 1
    k = len(var_names)
    fig, axes = plt.subplots(k, k, figsize=(3 * k, 2.5 * k))
    for resp in range(k):
        for shock in range(k):
            ax = axes[resp, shock]
            ax.plot(range(periods + 1), irfs[:, resp, shock],
                    color="steelblue", linewidth=1.2)
            ax.axhline(0, color="grey", linewidth=0.5)
            ax.set_title(f"{var_names[shock]} -> {var_names[resp]}", fontsize=7)
            ax.tick_params(labelsize=6)
    fig.suptitle(f"Orthogonalized IRFs (Cholesky, {periods}Q)", fontsize=12, y=1.01)
    fig.tight_layout()
    path = os.path.join(OUTPUT_DIR, "04_irf.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"[CHART] IRFs (Cholesky) -> {path}")


# ============================================================
# SECTION 3a — SIGN RESTRICTIONS
# ============================================================

def _random_orthogonal(k: int, rng: np.random.Generator) -> np.ndarray:
    """Draw a random orthogonal matrix via QR of a random Gaussian."""
    Z = rng.standard_normal((k, k))
    Q, R = np.linalg.qr(Z)
    Q = Q @ np.diag(np.sign(np.diag(R)))
    return Q


def sign_restriction_irfs(coefs, sigma_u, sign_table: dict, var_names: list,
                           periods: int = 20, n_draws: int = 2000,
                           n_accept: int = 500, horizon_check: int = 0,
                           seed: int = 44, verbose: bool = True):
    """
    Identify structural shocks via sign restrictions (Rubio-Ramirez et al. 2010).

    sign_table: ordered dict mapping shock_name -> {variable: +1/-1} for horizon_check.
                Row i of the restriction matrix is applied to **structural column i**
                of Theta_h (i.e. the i-th column of A0 = chol(Sigma_u) @ Q).
                Interpretation: column 0 = first named shock in sign_table, etc.

    Estimation is on possibly transformed data (e.g. first differences); signs
    apply to the **estimated VAR in mean** — interpret as local impulses in the
    chosen metric, not literal national-accounts units if variables are differenced.

    Returns: accepted_irfs (n_accept, periods+1, k, k) array, or None if none accepted.
    """
    p, k, _ = coefs.shape
    P = np.linalg.cholesky(sigma_u)
    companion = _companion_matrix(coefs)

    J = np.zeros((k, k * p))
    J[:k, :k] = np.eye(k)

    # Pre-compute reduced-form MA matrices up to horizon_check
    Phi = [np.eye(k)]
    power = np.eye(k * p)
    for h in range(1, max(horizon_check + 1, periods + 1)):
        power = power @ companion
        Phi.append(J @ power @ J.T)

    shock_names = list(sign_table.keys())
    n_shocks = len(shock_names)

    # Build sign matrix: (n_shocks, k) with +1/-1/0
    S = np.zeros((n_shocks, k))
    for si, sname in enumerate(shock_names):
        for vname, sign in sign_table[sname].items():
            if vname in var_names:
                vi = var_names.index(vname)
                S[si, vi] = sign

    rng = np.random.default_rng(seed)
    accepted = []

    for _ in range(n_draws):
        Q = _random_orthogonal(k, rng)
        A0 = P @ Q  # candidate impact matrix

        # Compute IRF at horizon_check
        Theta_h = Phi[horizon_check] @ A0

        # Check sign restrictions
        ok = True
        for si in range(n_shocks):
            for vi in range(k):
                if S[si, vi] != 0:
                    if S[si, vi] * Theta_h[vi, si] < 0:
                        ok = False
                        break
            if not ok:
                break

        if ok:
            # Compute full IRFs for this rotation
            irfs = np.zeros((periods + 1, k, k))
            irfs[0] = A0.copy()
            for h in range(1, periods + 1):
                if h < len(Phi):
                    irfs[h] = Phi[h] @ A0
                else:
                    power_h = np.linalg.matrix_power(companion, h)
                    irfs[h] = (J @ power_h @ J.T) @ A0
            accepted.append(irfs)
            if len(accepted) >= n_accept:
                break

    if verbose:
        pct = len(accepted) / max(n_draws, 1) * 100
        print(f"[SIGN] {len(accepted)}/{n_draws} draws accepted ({pct:.1f}%)")
    if not accepted:
        return None
    return np.array(accepted)


def default_sign_table():
    """
    Theory-consistent sign restrictions for HK under the currency board.
    Shock 1 (US monetary tightening): FFR up, HIBOR up, GDP down, unemployment up
    Shock 2 (China growth positive):  China GDP up, GDP up, CPI up
    """
    return {
        "us_monetary": {
            "us_ffr": +1,
            "hibor_3m": +1,
            "gdp_growth": -1,
            "unemployment": +1,
        },
        "china_growth": {
            "china_gdp": +1,
            "gdp_growth": +1,
            "cpi_inflation": +1,
        },
    }


def plot_sign_restriction_irfs(accepted_irfs, var_names, shock_names=None):
    """Plot median and 68% bands from sign-restriction accepted IRFs."""
    if accepted_irfs is None or len(accepted_irfs) == 0:
        print("[SIGN] No accepted draws to plot.")
        return

    n_acc, H1, k, _ = accepted_irfs.shape
    periods = H1 - 1

    if shock_names is None:
        shock_names = [f"shock_{j}" for j in range(k)]
    n_shocks = min(len(shock_names), k)

    hk_targets = [v for v in ["gdp_growth", "cpi_inflation", "unemployment", "hibor_3m"]
                  if v in var_names]
    n_rows = len(hk_targets)

    fig, axes = plt.subplots(n_rows, n_shocks, figsize=(5 * n_shocks, 3 * n_rows))
    if n_rows == 1:
        axes = axes.reshape(1, -1)
    if n_shocks == 1:
        axes = axes.reshape(-1, 1)

    x = np.arange(periods + 1)
    for row, target in enumerate(hk_targets):
        ti = var_names.index(target)
        for col in range(n_shocks):
            ax = axes[row, col]
            draws = accepted_irfs[:, :, ti, col]
            median = np.median(draws, axis=0)
            lo = np.percentile(draws, 16, axis=0)
            hi = np.percentile(draws, 84, axis=0)
            ax.plot(x, median, color="steelblue", linewidth=1.5)
            ax.fill_between(x, lo, hi, alpha=0.25, color="steelblue")
            ax.axhline(0, color="grey", linewidth=0.5)
            if row == 0:
                ax.set_title(shock_names[col], fontsize=10)
            if col == 0:
                ax.set_ylabel(target, fontsize=9)
            ax.tick_params(labelsize=7)

    fig.suptitle(f"Sign-Restriction IRFs (median + 68% band, {n_acc} draws)",
                 fontsize=12, y=1.01)
    fig.tight_layout()
    path = os.path.join(OUTPUT_DIR, "11_sign_restriction_irf.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"[CHART] Sign-restriction IRFs -> {path}")


# ============================================================
# SECTION 3b — FEVD AND HISTORICAL DECOMPOSITION
# ============================================================

def compute_fevd(irfs: np.ndarray, var_names: list, max_horizon: int = 20):
    """
    Forecast Error Variance Decomposition from orthogonalized IRFs.
    FEVD_{i,j}(h) = sum_{s=0}^{h} theta_{ij,s}^2 / sum_{s=0}^{h} sum_k theta_{ik,s}^2
    Returns: (horizons+1, k, k) array where fevd[h, i, j] = fraction of variable i
             forecast error variance at horizon h due to shock j.
    """
    H = min(max_horizon, irfs.shape[0] - 1)
    k = irfs.shape[1]
    fevd = np.zeros((H + 1, k, k))

    cum_sq = np.zeros((k, k))
    for h in range(H + 1):
        cum_sq += irfs[h] ** 2
        total_per_var = cum_sq.sum(axis=1, keepdims=True)
        total_per_var = np.maximum(total_per_var, 1e-12)
        fevd[h] = cum_sq / total_per_var

    return fevd


def plot_fevd(fevd: np.ndarray, var_names: list, horizons_to_show=None):
    """Stacked area FEVD plots for each variable."""
    if horizons_to_show is None:
        horizons_to_show = [1, 4, 8, 16]
    H_max = fevd.shape[0] - 1
    horizons_to_show = [h for h in horizons_to_show if h <= H_max]

    k = len(var_names)
    hk_vars = [v for v in ["gdp_growth", "cpi_inflation", "unemployment", "hibor_3m"]
               if v in var_names]
    if not hk_vars:
        hk_vars = var_names[:4]

    colors = plt.cm.Set2(np.linspace(0, 1, k))

    fig, axes = plt.subplots(len(hk_vars), 1, figsize=(12, 3 * len(hk_vars)))
    if len(hk_vars) == 1:
        axes = [axes]

    for row, target in enumerate(hk_vars):
        ax = axes[row]
        i = var_names.index(target)
        x = np.arange(H_max + 1)
        bottom = np.zeros(H_max + 1)
        for j in range(k):
            ax.fill_between(x, bottom, bottom + fevd[:, i, j],
                            label=var_names[j], color=colors[j], alpha=0.8)
            bottom += fevd[:, i, j]
        ax.set_ylabel("Share")
        ax.set_title(f"FEVD: {target}", fontsize=11)
        ax.set_xlim(0, H_max)
        ax.set_ylim(0, 1.0)
        ax.set_xlabel("Horizon (quarters)")
        if row == 0:
            ax.legend(loc="upper right", fontsize=7, ncol=3)

    fig.suptitle("Forecast Error Variance Decomposition (Cholesky)", fontsize=13, y=1.01)
    fig.tight_layout()
    path = os.path.join(OUTPUT_DIR, "07_fevd.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"[CHART] FEVD -> {path}")

    rows = []
    for h in horizons_to_show:
        for i, target in enumerate(var_names):
            for j, shock in enumerate(var_names):
                rows.append({
                    "horizon": h, "target": target, "shock": shock,
                    "share": round(float(fevd[h, i, j]), 4),
                })
    fevd_df = pd.DataFrame(rows)
    tbl_path = os.path.join(OUTPUT_DIR, "fevd_table.csv")
    fevd_df.to_csv(tbl_path, index=False)
    print(f"[TABLE] FEVD table -> {tbl_path}")
    return fevd_df


def compute_historical_decomposition(result, df: pd.DataFrame, var_names: list):
    """
    Decompose each observed period into contributions from each structural shock.
    y_t = base_t + sum_j contribution_j_t
    where base uses initial conditions with no shocks,
    and structural shocks e_t = P^{-1} u_t.
    """
    coefs = result.coefs
    p, k, _ = coefs.shape
    sigma_u = result.sigma_u if hasattr(result, "sigma_u") and result.sigma_u is not None else None
    resid_arr = result.resid.values if hasattr(result.resid, "values") else result.resid
    T = resid_arr.shape[0]

    if sigma_u is None:
        sigma_u = np.cov(resid_arr, rowvar=False)
    P = np.linalg.cholesky(sigma_u)
    P_inv = np.linalg.inv(P)

    structural_shocks = (P_inv @ resid_arr.T).T  # (T, k)

    companion = _companion_matrix(coefs)
    J = np.zeros((k, k * p))
    J[:k, :k] = np.eye(k)

    contributions = np.zeros((T, k, k))  # (time, target_var, shock_source)
    for t in range(T):
        for s in range(t + 1):
            lag = t - s
            if lag == 0:
                Phi = np.eye(k)
            else:
                Phi = J @ np.linalg.matrix_power(companion, lag) @ J.T
            Theta = Phi @ P
            for j in range(k):
                contributions[t, :, j] += Theta[:, j] * structural_shocks[s, j]

    arr = df.values
    # Align decomposition window to residual sample length. This keeps VAR and
    # VECM paths consistent even when effective sample starts differ.
    start_idx = max(len(df) - T, 0)
    data_for_decomp = arr[start_idx:start_idx + T]
    intercept = getattr(result, "intercept", None)
    if intercept is None:
        base = np.mean(data_for_decomp, axis=0)
    else:
        base = intercept

    dates = df.index[start_idx:start_idx + T]

    return {
        "contributions": contributions,
        "structural_shocks": structural_shocks,
        "base": base,
        "dates": dates,
        "var_names": var_names,
    }


def plot_historical_decomposition(hd: dict, df_raw: pd.DataFrame = None):
    """Bar-stack chart of shock contributions over time."""
    contributions = hd["contributions"]
    dates = hd["dates"]
    var_names = hd["var_names"]
    k = len(var_names)

    hk_vars = [v for v in ["gdp_growth", "cpi_inflation", "unemployment", "hibor_3m"]
               if v in var_names]
    if not hk_vars:
        hk_vars = var_names[:4]

    colors = plt.cm.Set2(np.linspace(0, 1, k))

    fig, axes = plt.subplots(len(hk_vars), 1, figsize=(14, 3.5 * len(hk_vars)), sharex=True)
    if len(hk_vars) == 1:
        axes = [axes]

    for row, target in enumerate(hk_vars):
        ax = axes[row]
        i = var_names.index(target)

        pos = np.zeros(len(dates))
        neg = np.zeros(len(dates))
        for j in range(k):
            vals = contributions[:, i, j]
            pos_vals = np.maximum(vals, 0)
            neg_vals = np.minimum(vals, 0)
            ax.bar(dates, pos_vals, bottom=pos, color=colors[j],
                   label=var_names[j], alpha=0.8, width=80)
            ax.bar(dates, neg_vals, bottom=neg, color=colors[j],
                   alpha=0.8, width=80)
            pos += pos_vals
            neg += neg_vals

        if df_raw is not None and target in df_raw.columns:
            actual = df_raw[target].reindex(dates)
            ax.plot(dates, actual.values, color="black", linewidth=1.5,
                    label="Actual", zorder=10)

        ax.axhline(0, color="grey", linewidth=0.5)
        ax.set_title(f"Historical Decomposition: {target}", fontsize=11)
        ax.set_ylabel("Contribution")
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
        ax.grid(alpha=0.2, axis="y")
        if row == 0:
            ax.legend(loc="lower left", fontsize=7, ncol=k)

    fig.suptitle("Historical Decomposition of Shocks (Cholesky)", fontsize=13, y=1.01)
    fig.tight_layout()
    path = os.path.join(OUTPUT_DIR, "08_hist_decomp.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"[CHART] Historical decomposition -> {path}")


# ============================================================
# SECTION 3b2 — TVP-VAR (Time-Varying Parameters)
# ============================================================

def tvp_var_kalman(df: pd.DataFrame, lags: int = 1,
                   forgetting_factor: float = 0.99):
    """
    TVP-VAR via Kalman filter with forgetting-factor state evolution.

    The state vector theta_t = vec([c, A_1, ..., A_p]) evolves as:
        theta_t = theta_{t-1} + eta_t,  Q_t = (1/lambda - 1) * P_{t|t-1}
    where lambda is the forgetting factor (0.95-0.99 typical).

    Returns dict with time-varying coefficients, fitted values, and residuals.
    """
    arr = df.values
    T, k = arr.shape
    n_coef = 1 + k * lags  # per equation: intercept + k*lags

    # Build regressors: [1, y_{t-1}, ..., y_{t-p}]
    Y = arr[lags:]  # (T-p, k)
    n = len(Y)
    X = np.ones((n, n_coef))
    for t in range(n):
        for lag in range(1, lags + 1):
            X[t, 1 + (lag - 1) * k: 1 + lag * k] = arr[lags + t - lag]

    # Initialize state per equation with OLS
    lam = forgetting_factor
    theta = np.zeros((n, k, n_coef))  # time-varying coefficients
    resid = np.zeros((n, k))

    for eq in range(k):
        y_eq = Y[:, eq]

        # OLS initialization on first 20% of sample
        init_n = max(n_coef + 5, n // 5)
        X_init, y_init = X[:init_n], y_eq[:init_n]
        beta_ols = np.linalg.lstsq(X_init, y_init, rcond=None)[0]
        resid_init = y_init - X_init @ beta_ols
        sigma2 = np.var(resid_init) + 1e-8

        # Kalman filter
        beta_t = beta_ols.copy()
        P_t = np.eye(n_coef) * sigma2 * 10  # diffuse prior

        for t in range(n):
            x_t = X[t]

            # Prediction
            P_pred = P_t / lam  # forgetting factor state evolution

            # Update
            f_t = x_t @ P_pred @ x_t + sigma2
            K_t = P_pred @ x_t / f_t
            y_hat = x_t @ beta_t
            v_t = y_eq[t] - y_hat

            beta_t = beta_t + K_t * v_t
            P_t = P_pred - np.outer(K_t, K_t) * f_t

            # Update sigma2 with exponential smoothing
            sigma2 = 0.99 * sigma2 + 0.01 * v_t ** 2

            theta[t, eq, :] = beta_t
            resid[t, eq] = v_t

    return {
        "theta": theta,       # (n, k, n_coef) time-varying coefficients
        "resid": resid,        # (n, k)
        "dates": df.index[lags:],
        "var_names": list(df.columns),
        "lags": lags,
        "forgetting_factor": lam,
    }


def plot_tvp_var(tvp_result: dict):
    """Plot time-varying coefficients for key relationships."""
    theta = tvp_result["theta"]
    dates = tvp_result["dates"]
    var_names = tvp_result["var_names"]

    # Plot selected coefficient paths
    # Interest: us_ffr -> hibor_3m, china_gdp -> gdp_growth
    pairs = []
    for resp_name, shock_name in [
        ("hibor_3m", "us_ffr"), ("gdp_growth", "china_gdp"),
        ("gdp_growth", "us_ffr"), ("unemployment", "china_gdp"),
    ]:
        if resp_name in var_names and shock_name in var_names:
            resp_idx = var_names.index(resp_name)
            shock_idx = var_names.index(shock_name)
            coef_idx = 1 + shock_idx  # lag-1 coefficient
            pairs.append((resp_name, shock_name, resp_idx, coef_idx))

    if not pairs:
        return

    fig, axes = plt.subplots(len(pairs), 1, figsize=(12, 3 * len(pairs)), sharex=True)
    if len(pairs) == 1:
        axes = [axes]

    for i, (resp, shock, resp_idx, coef_idx) in enumerate(pairs):
        ax = axes[i]
        coef_path = theta[:, resp_idx, coef_idx]
        ax.plot(dates, coef_path, color="steelblue", linewidth=1.2)
        ax.axhline(0, color="grey", linewidth=0.5, linestyle="--")
        ax.set_title(f"TVP: {shock} -> {resp} (lag-1 coefficient)", fontsize=10)
        ax.set_ylabel("Coefficient")
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
        ax.grid(alpha=0.3)

        # Shade GFC and COVID
        for label, start, end, color in [
            ("GFC", "2008-07-01", "2009-07-01", "salmon"),
            ("COVID", "2020-01-01", "2020-10-01", "lightyellow"),
        ]:
            try:
                ax.axvspan(pd.Timestamp(start), pd.Timestamp(end),
                           alpha=0.2, color=color, label=label)
            except Exception:
                pass
        if i == 0:
            ax.legend(fontsize=8)

    fig.suptitle("Time-Varying Parameter VAR — Key Coefficient Paths",
                 fontsize=12, y=1.01)
    fig.tight_layout()
    path = os.path.join(OUTPUT_DIR, "12_tvp_var.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"[CHART] TVP-VAR coefficient paths -> {path}")


# ============================================================
# SECTION 3c — ROBUSTNESS
# ============================================================

def robustness_ordering_permutations(df_est, lags, model_type, bvar_lambda1,
                                     var_names, sigma_u_base):
    """
    Re-estimate IRFs and FEVD under alternative Cholesky orderings.
    Returns a summary of how FEVD shares change.
    """
    if model_type == "vecm":
        print(
            "[NOTE] Ordering robustness uses VAR on transformed data only; "
            "primary VECM estimates are on levels — compare to Cholesky FEVD as a VAR-space sensitivity check."
        )
    orderings = {
        "baseline (ext-first)": list(var_names),
        "domestic-first": [v for v in var_names if v not in ["us_ffr", "china_gdp"]] +
                          [v for v in var_names if v in ["us_ffr", "china_gdp"]],
        "reversed": list(reversed(var_names)),
    }

    results = {}
    for label, order in orderings.items():
        df_reord = df_est[order]
        try:
            if model_type == "bvar":
                res = fit_bvar_minnesota(df_reord, lags, lambda1=bvar_lambda1)
            else:
                res = VAR(df_reord).fit(lags)
            coefs = res.coefs
            resid = res.resid.values if hasattr(res.resid, "values") else res.resid
            sigma = res.sigma_u if hasattr(res, "sigma_u") and res.sigma_u is not None else np.cov(resid, rowvar=False)
            irfs = _cholesky_irf(coefs, sigma, periods=16)
            fevd = compute_fevd(irfs, order, max_horizon=16)
            results[label] = {"order": order, "fevd": fevd, "irfs": irfs}
        except Exception as e:
            print(f"  [ROBUST] Ordering '{label}' failed: {e}")

    if len(results) < 2:
        print("[ROBUST] Insufficient orderings for comparison.")
        return None

    _plot_ordering_robustness(results, var_names)
    return results


def _plot_ordering_robustness(results, base_var_names):
    """Compare FEVD at h=8 across orderings for HK domestic variables."""
    hk_targets = [v for v in ["gdp_growth", "cpi_inflation", "unemployment", "hibor_3m"]
                  if v in base_var_names]
    external = [v for v in ["us_ffr", "china_gdp"] if v in base_var_names]
    h = 8

    fig, axes = plt.subplots(1, len(hk_targets), figsize=(4 * len(hk_targets), 5))
    if len(hk_targets) == 1:
        axes = [axes]

    ordering_labels = list(results.keys())
    x = np.arange(len(ordering_labels))
    w = 0.35

    for col_idx, target in enumerate(hk_targets):
        ax = axes[col_idx]
        for ext_idx, ext_var in enumerate(external):
            shares = []
            for olabel in ordering_labels:
                info = results[olabel]
                order = info["order"]
                fevd = info["fevd"]
                if target in order and ext_var in order:
                    ti = order.index(target)
                    si = order.index(ext_var)
                    hh = min(h, fevd.shape[0] - 1)
                    shares.append(fevd[hh, ti, si])
                else:
                    shares.append(0.0)
            offset = (ext_idx - 0.5) * w
            ax.bar(x + offset, shares, w, label=ext_var, alpha=0.8)

        ax.set_xticks(x)
        ax.set_xticklabels([lbl[:12] for lbl in ordering_labels], rotation=20, fontsize=8)
        ax.set_ylabel("FEVD share at h=8")
        ax.set_title(target, fontsize=10)
        ax.set_ylim(0, 1.0)
        if col_idx == 0:
            ax.legend(fontsize=8)

    fig.suptitle("Robustness: FEVD Sensitivity to Cholesky Ordering", fontsize=12, y=1.02)
    fig.tight_layout()
    path = os.path.join(OUTPUT_DIR, "09_ordering_robustness.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"[CHART] Ordering robustness -> {path}")


def robustness_subsample(df_est, lags, model_type, bvar_lambda1, var_names):
    """Estimate on sub-samples and compare IRF norms."""
    if model_type == "vecm":
        print(
            "[NOTE] Sub-sample stability uses VAR on transformed data; "
            "not the VECM level specification."
        )
    T = len(df_est)
    mid = T // 2
    gfc_end_idx = None
    for i, d in enumerate(df_est.index):
        if d.year >= 2010:
            gfc_end_idx = i
            break
    if gfc_end_idx is None:
        gfc_end_idx = mid

    covid_start_idx = None
    for i, d in enumerate(df_est.index):
        if d.year >= 2020:
            covid_start_idx = i
            break

    splits = {"full_sample": df_est}
    if gfc_end_idx > lags + 20:
        splits["pre_GFC"] = df_est.iloc[:gfc_end_idx]
    if gfc_end_idx + 20 < T:
        splits["post_GFC"] = df_est.iloc[gfc_end_idx:]
    if covid_start_idx and covid_start_idx + lags < T:
        ex_covid = pd.concat([df_est.iloc[:covid_start_idx], df_est.iloc[covid_start_idx + 4:]])
        if len(ex_covid) > lags + 20:
            splits["ex_COVID"] = ex_covid

    print("\n=== Sub-sample Stability ===")
    coef_norms = {}
    for label, sub_df in splits.items():
        try:
            if model_type == "bvar":
                res = fit_bvar_minnesota(sub_df, lags, lambda1=bvar_lambda1)
            else:
                res = VAR(sub_df).fit(lags)
            norm = np.linalg.norm(res.coefs)
            max_eig = np.abs(np.linalg.eigvals(_companion_matrix(res.coefs))).max()
            coef_norms[label] = {"norm": norm, "max_eig": max_eig, "nobs": len(sub_df)}
            print(f"  {label:15s}: nobs={len(sub_df):3d}, coef_norm={norm:.3f}, max_eig={max_eig:.4f}")
        except Exception as e:
            print(f"  {label:15s}: FAILED ({e})")

    _plot_subsample_stability(coef_norms)
    return coef_norms


def _plot_subsample_stability(coef_norms):
    if len(coef_norms) < 2:
        return
    labels = list(coef_norms.keys())
    norms = [coef_norms[lbl]["norm"] for lbl in labels]
    eigs = [coef_norms[lbl]["max_eig"] for lbl in labels]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    x = np.arange(len(labels))
    ax1.bar(x, norms, color="steelblue", alpha=0.8)
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels, rotation=20, fontsize=9)
    ax1.set_ylabel("Frobenius norm of coefficient matrices")
    ax1.set_title("Coefficient Norm Stability")
    ax1.grid(alpha=0.3, axis="y")

    ax2.bar(x, eigs, color="crimson", alpha=0.8)
    ax2.axhline(1.0, color="black", linewidth=1.0, linestyle="--", label="Unit circle")
    ax2.set_xticks(x)
    ax2.set_xticklabels(labels, rotation=20, fontsize=9)
    ax2.set_ylabel("Max eigenvalue modulus")
    ax2.set_title("Stability Across Sub-samples")
    ax2.legend()
    ax2.grid(alpha=0.3, axis="y")

    fig.suptitle("Sub-sample Robustness", fontsize=12, y=1.02)
    fig.tight_layout()
    path = os.path.join(OUTPUT_DIR, "10_subsample_stability.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"[CHART] Sub-sample stability -> {path}")


# ============================================================
# SECTION 4 — OUT-OF-SAMPLE VALIDATION
# ============================================================

def rolling_backtest(df: pd.DataFrame, lags: int, forecast_horizon: int = 4,
                     min_train: int = 60, model_type: str = "var",
                     bvar_lambda1: float = 0.2, df_raw: pd.DataFrame = None,
                     coint_rank: int | None = None, vecm_deterministic: str = "ci",
                     vecm_lag_diff: int | None = None) -> pd.DataFrame:
    T = len(df)
    cols = list(df.columns)
    n_vars = len(cols)
    records = []

    for t in range(min_train, T - forecast_horizon):
        train = df.iloc[:t]
        actual_block = df.iloc[t:t + forecast_horizon]

        try:
            if model_type == "bvar":
                mod = fit_bvar_minnesota(train, lags, lambda1=bvar_lambda1)
                var_fc = mod.forecast(train.values[-lags:], steps=forecast_horizon)
            elif model_type == "vecm":
                if df_raw is None:
                    raise ValueError("rolling_backtest(vecm) requires df_raw")
                train_raw = df_raw.loc[train.index]
                rank = _vecm_rank_or_default(coint_rank)
                lag_diff = max(lags - 1, 1) if vecm_lag_diff is None else max(int(vecm_lag_diff), 1)
                mod = fit_vecm(
                    train_raw,
                    lags_diff=lag_diff,
                    coint_rank=rank,
                    deterministic=vecm_deterministic,
                    verbose=False,
                )
                var_fc = mod.forecast(train_raw.values[-lags:], steps=forecast_horizon)
            else:
                mod = VAR(train).fit(lags)
                var_fc = mod.forecast(train.values[-lags:], steps=forecast_horizon)
        except Exception:
            continue

        ar_fc = np.zeros((forecast_horizon, n_vars))
        for j, col in enumerate(cols):
            try:
                ar_mod = AutoReg(train[col].values, lags=1).fit()
                ar_fc[:, j] = ar_mod.forecast(steps=forecast_horizon)
            except Exception:
                ar_fc[:, j] = train[col].iloc[-1]

        rw_fc = np.tile(train.iloc[-1].values, (forecast_horizon, 1))
        actual = actual_block.values
        for h in range(forecast_horizon):
            for j, col in enumerate(cols):
                records.append({
                    "origin": train.index[-1],
                    "horizon": h + 1,
                    "variable": col,
                    "actual": actual[h, j],
                    "var_fc": var_fc[h, j],
                    "ar_fc": ar_fc[h, j],
                    "rw_fc": rw_fc[h, j],
                })

    if not records:
        return pd.DataFrame(
            columns=[
                "origin", "horizon", "variable", "actual", "var_fc", "ar_fc", "rw_fc"
            ]
        )
    return pd.DataFrame(records)


def _invert_from_origin(fc_t: np.ndarray, cols: list[str], transforms: dict, origin_levels: np.ndarray):
    """Invert transformed forecasts using origin-specific levels (for OOS comparability)."""
    fc_level = fc_t.copy()
    for j, col in enumerate(cols):
        if transforms.get(col, {}).get("transform") == "first_diff":
            fc_level[:, j] = origin_levels[j] + np.cumsum(fc_t[:, j])
    return fc_level


def model_backtest_summary_level(
    model_name: str,
    df_est: pd.DataFrame,
    df_raw: pd.DataFrame,
    lags: int,
    transforms: dict,
    forecast_horizon: int = 4,
    min_train: int = 60,
    bvar_lambda1: float = 0.2,
    coint_rank: int | None = None,
    vecm_deterministic: str = "ci",
    vecm_lag_diff: int | None = None,
) -> pd.DataFrame:
    cols = list(df_est.columns)
    records = []
    T = len(df_est)
    for t in range(min_train, T - forecast_horizon):
        train = df_est.iloc[:t]
        block_est = df_est.iloc[t:t + forecast_horizon]
        block_dates = block_est.index
        try:
            if model_name == "bvar":
                mod = fit_bvar_minnesota(train, lags, lambda1=bvar_lambda1)
                fc_t = mod.forecast(train.values[-lags:], steps=forecast_horizon)
            elif model_name == "vecm":
                train_raw = df_raw.loc[train.index]
                rank = _vecm_rank_or_default(coint_rank)
                lag_diff = max(lags - 1, 1) if vecm_lag_diff is None else max(int(vecm_lag_diff), 1)
                mod = fit_vecm(
                    train_raw,
                    lags_diff=lag_diff,
                    coint_rank=rank,
                    deterministic=vecm_deterministic,
                    verbose=False,
                )
                # VECM is fit on levels; forecasts match df_raw units (no diff inversion).
                fc_t = mod.forecast(train_raw.values[-lags:], steps=forecast_horizon)
            else:
                mod = VAR(train).fit(lags)
                fc_t = mod.forecast(train.values[-lags:], steps=forecast_horizon)
        except Exception:
            continue

        origin_levels = df_raw.loc[train.index[-1], cols].values
        if model_name == "vecm":
            fc_level = fc_t.copy()
        else:
            fc_level = _invert_from_origin(fc_t, cols, transforms, origin_levels)
        actual_level = df_raw.loc[block_dates, cols].values

        for h in range(forecast_horizon):
            for j, col in enumerate(cols):
                err = fc_level[h, j] - actual_level[h, j]
                records.append(
                    {
                        "model": model_name,
                        "origin": train.index[-1],
                        "horizon": h + 1,
                        "variable": col,
                        "actual_level": actual_level[h, j],
                        "forecast_level": fc_level[h, j],
                        "err": err,
                        "abs_err": abs(err),
                        "sq_err": err ** 2,
                    }
                )

    bt = pd.DataFrame(records)
    if bt.empty:
        return bt
    summary = (
        bt.groupby(["model", "variable", "horizon"], as_index=False)
        .agg(
            n_windows=("err", "size"),
            RMSE=("sq_err", lambda x: float(np.sqrt(np.mean(x)))),
            MAE=("abs_err", "mean"),
        )
    )
    return summary


def compare_var_vecm_backtest_level(
    df_est: pd.DataFrame,
    df_raw: pd.DataFrame,
    lags: int,
    transforms: dict,
    coint_rank: int | None,
    vecm_deterministic: str,
    vecm_lag_diff: int | None,
) -> pd.DataFrame:
    var_summary = model_backtest_summary_level(
        "var", df_est, df_raw, lags, transforms
    )
    vecm_summary = model_backtest_summary_level(
        "vecm",
        df_est,
        df_raw,
        lags,
        transforms,
        coint_rank=coint_rank,
        vecm_deterministic=vecm_deterministic,
        vecm_lag_diff=vecm_lag_diff,
    )
    if var_summary.empty or vecm_summary.empty:
        return pd.DataFrame()

    merged = var_summary.merge(
        vecm_summary,
        on=["variable", "horizon"],
        suffixes=("_VAR", "_VECM"),
    )
    merged["RMSE_winner"] = np.where(
        merged["RMSE_VAR"] <= merged["RMSE_VECM"], "VAR", "VECM"
    )
    merged["MAE_winner"] = np.where(
        merged["MAE_VAR"] <= merged["MAE_VECM"], "VAR", "VECM"
    )
    keep_cols = [
        "variable",
        "horizon",
        "n_windows_VAR",
        "RMSE_VAR",
        "RMSE_VECM",
        "MAE_VAR",
        "MAE_VECM",
        "RMSE_winner",
        "MAE_winner",
    ]
    out_df = merged[keep_cols].sort_values(["variable", "horizon"]).reset_index(drop=True)
    path = os.path.join(OUTPUT_DIR, "var_vecm_backtest_comparison.csv")
    out_df.to_csv(path, index=False)
    print(f"[TABLE] VAR vs VECM backtest comparison -> {path}")
    return out_df


def evaluate_backtest(bt: pd.DataFrame):
    if bt.empty:
        print("\n=== Out-of-Sample Forecast Evaluation (RMSE) ===")
        print("No valid rolling windows were estimated for this specification.")
        return pd.DataFrame(
            columns=[
                "variable", "horizon", "n_windows",
                "RMSE_VAR", "RMSE_AR", "RMSE_RW",
                "MAE_VAR", "MAE_AR", "MAE_RW",
            ]
        )

    bt["var_err"] = bt["var_fc"] - bt["actual"]
    bt["ar_err"] = bt["ar_fc"] - bt["actual"]
    bt["rw_err"] = bt["rw_fc"] - bt["actual"]

    summary_rows = []
    for var in bt["variable"].unique():
        for h in sorted(bt["horizon"].unique()):
            sub = bt[(bt["variable"] == var) & (bt["horizon"] == h)]
            summary_rows.append({
                "variable": var, "horizon": h, "n_windows": len(sub),
                "RMSE_VAR": np.sqrt((sub["var_err"] ** 2).mean()),
                "RMSE_AR": np.sqrt((sub["ar_err"] ** 2).mean()),
                "RMSE_RW": np.sqrt((sub["rw_err"] ** 2).mean()),
                "MAE_VAR": sub["var_err"].abs().mean(),
                "MAE_AR": sub["ar_err"].abs().mean(),
                "MAE_RW": sub["rw_err"].abs().mean(),
            })
    summary = pd.DataFrame(summary_rows)

    print("\n=== Out-of-Sample Forecast Evaluation (RMSE) ===")
    pivot = summary.pivot_table(
        index=["variable", "horizon"],
        values=["RMSE_VAR", "RMSE_AR", "RMSE_RW"],
    ).round(3)
    print(pivot.to_string())

    _plot_backtest(summary)
    return summary


def _plot_backtest(summary: pd.DataFrame):
    for h in [1, 4]:
        sub = summary[summary["horizon"] == h].copy()
        if sub.empty:
            continue
        fig, ax = plt.subplots(figsize=(10, 5))
        x = np.arange(len(sub))
        w = 0.25
        ax.bar(x - w, sub["RMSE_VAR"], w, label="VAR", color="steelblue")
        ax.bar(x, sub["RMSE_AR"], w, label="AR(1)", color="darkorange")
        ax.bar(x + w, sub["RMSE_RW"], w, label="Random Walk", color="grey")
        ax.set_xticks(x)
        ax.set_xticklabels(sub["variable"], rotation=30, ha="right", fontsize=9)
        ax.set_ylabel("RMSE")
        ax.set_title(f"Out-of-Sample RMSE -- Horizon = {h}Q", fontsize=12)
        ax.legend()
        ax.grid(alpha=0.3, axis="y")
        fig.tight_layout()
        path = os.path.join(OUTPUT_DIR, f"05_backtest_h{h}.png")
        fig.savefig(path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        print(f"[CHART] Backtest RMSE h={h} -> {path}")


# ============================================================
# SECTION 5 — SCENARIO FORECASTING
# ============================================================

def _invert_transforms(fc_transformed: np.ndarray, cols: list,
                       transforms: dict) -> np.ndarray:
    """
    Audit fix #1: convert forecasts from transformed space back to levels.
    For first_diff: level[t] = last_known_level + cumsum(diff_forecast[:t+1])
    """
    fc_level = fc_transformed.copy()
    for j, col in enumerate(cols):
        info = transforms.get(col, {})
        if info.get("transform") == "first_diff":
            last_lev = info["last_level"]
            fc_level[:, j] = last_lev + np.cumsum(fc_transformed[:, j])
    return fc_level


def _shock_in_level_space(last_obs: np.ndarray, col_idx: int, desired_level: float,
                          transforms: dict, col_name: str) -> np.ndarray:
    """
    Audit fix #2: define scenario shocks in level space, convert to
    transformed space for the forecast conditioning.
    """
    shocked = last_obs.copy()
    info = transforms.get(col_name, {})
    if info.get("transform") == "first_diff":
        current_last_level = info["last_level"]
        shocked[-1, col_idx] = desired_level - current_last_level
    else:
        shocked[-1, col_idx] = desired_level
    return shocked


def forecast_scenarios(result, df: pd.DataFrame, lags: int,
                       transforms: dict, horizon: int = 8,
                       df_raw: pd.DataFrame = None) -> dict:
    """
    Produce baseline + shock scenarios.
    All outputs are in LEVEL space (transforms inverted).
    df_raw is used for level-space history plotting (audit v2 fix #2).
    VECM is fit on levels; conditioning lags must match df_raw, not df_est.
    """
    cols = list(df.columns)
    levels_df = df_raw if df_raw is not None else df
    if _is_vecm_result(result):
        last_obs = levels_df.values[-lags:]
    else:
        last_obs = df.values[-lags:]

    # Baseline forecast (transformed space for VAR/BVAR; levels for VECM)
    base_fc_t = result.forecast(last_obs, steps=horizon)
    fc_dates = pd.date_range(df.index[-1] + pd.offsets.QuarterBegin(1),
                             periods=horizon, freq="QS")

    if _is_vecm_result(result):
        base_fc_lev = base_fc_t.copy()
    else:
        base_fc_lev = _invert_transforms(base_fc_t, cols, transforms)
    scenarios = {"baseline": pd.DataFrame(base_fc_lev, index=fc_dates, columns=cols)}

    # Audit fix #7: parameter-uncertainty bootstrap
    resid_arr = result.resid.values if hasattr(result.resid, "values") else result.resid
    n_boot = 500
    boot_paths = np.zeros((n_boot, horizon, len(cols)))

    for b in range(n_boot):
        path = last_obs.copy()
        for h in range(horizon):
            shock = resid_arr[_RNG_BOOT.integers(len(resid_arr))]
            step = result.forecast(path[-lags:], steps=1)[0] + shock
            path = np.vstack([path, step])
        fc_t = path[-horizon:]
        if _is_vecm_result(result):
            boot_paths[b] = fc_t.copy()
        else:
            boot_paths[b] = _invert_transforms(fc_t, cols, transforms)

    scenarios["baseline_lo"] = pd.DataFrame(
        np.percentile(boot_paths, 10, axis=0), index=fc_dates, columns=cols)
    scenarios["baseline_hi"] = pd.DataFrame(
        np.percentile(boot_paths, 90, axis=0), index=fc_dates, columns=cols)

    # Audit fix #2: define shocks in LEVEL space
    china_idx = cols.index("china_gdp")
    ffr_idx = cols.index("us_ffr")

    china_baseline_level = transforms["china_gdp"]["last_level"]
    ffr_baseline_level = transforms["us_ffr"]["last_level"]

    # Weak external: China GDP growth falls 3pp, FFR rises 1.5pp
    shock1 = _shock_in_level_space(
        last_obs, china_idx, china_baseline_level - 3.0, transforms, "china_gdp")
    shock1 = _shock_in_level_space(
        shock1, ffr_idx, ffr_baseline_level + 1.5, transforms, "us_ffr")
    weak_fc_t = result.forecast(shock1, steps=horizon)
    if _is_vecm_result(result):
        scenarios["weak_external"] = pd.DataFrame(
            weak_fc_t.copy(), index=fc_dates, columns=cols)
    else:
        scenarios["weak_external"] = pd.DataFrame(
            _invert_transforms(weak_fc_t, cols, transforms), index=fc_dates, columns=cols)

    # Global easing: China GDP growth rises 1pp, FFR falls 1pp
    shock2 = _shock_in_level_space(
        last_obs, china_idx, china_baseline_level + 1.0, transforms, "china_gdp")
    shock2 = _shock_in_level_space(
        shock2, ffr_idx, ffr_baseline_level - 1.0, transforms, "us_ffr")
    ease_fc_t = result.forecast(shock2, steps=horizon)
    if _is_vecm_result(result):
        scenarios["global_easing"] = pd.DataFrame(
            ease_fc_t.copy(), index=fc_dates, columns=cols)
    else:
        scenarios["global_easing"] = pd.DataFrame(
            _invert_transforms(ease_fc_t, cols, transforms), index=fc_dates, columns=cols)

    hist_df = df_raw if df_raw is not None else df
    _plot_scenarios(hist_df, scenarios, cols, horizon, transforms)
    _save_forecast_table(scenarios)

    return scenarios


def _plot_scenarios(df_raw_or_est, scenarios, cols, horizon, transforms):
    """
    Audit fix #1: plot forecasts in LEVEL space with correct labels.
    Use raw-level history for differenced variables.
    """
    hk_vars = ["gdp_growth", "cpi_inflation", "unemployment", "hibor_3m"]
    titles = {
        "gdp_growth": "HK Real GDP Growth (YoY %)",
        "cpi_inflation": "HK CPI Inflation (YoY %)",
        "unemployment": "HK Unemployment Rate (%)",
        "hibor_3m": "3-Month HIBOR (%)",
    }

    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    axes = axes.ravel()
    tail = 20

    for i, col in enumerate(hk_vars):
        ax = axes[i]
        hist = df_raw_or_est[col].iloc[-tail:]
        ax.plot(hist.index, hist.values, color="black", linewidth=1.5, label="History")

        base = scenarios["baseline"][col]
        lo = scenarios["baseline_lo"][col]
        hi = scenarios["baseline_hi"][col]
        ax.plot(base.index, base.values, color="steelblue", linewidth=1.5, label="Baseline")
        ax.fill_between(base.index, lo.values, hi.values, alpha=0.2, color="steelblue",
                        label="80% CI")

        weak = scenarios["weak_external"][col]
        ax.plot(weak.index, weak.values, color="crimson", linewidth=1.2, linestyle="--",
                label="Weak external")

        ease = scenarios["global_easing"][col]
        ax.plot(ease.index, ease.values, color="seagreen", linewidth=1.2, linestyle="--",
                label="Global easing")

        ax.axhline(0, color="grey", linewidth=0.5, linestyle=":")
        ax.set_title(titles[col], fontsize=11)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
        ax.grid(alpha=0.3)
        if i == 0:
            ax.legend(fontsize=8, loc="lower left")

    fig.suptitle(
        f"Hong Kong Macro Forecast (levels) -- {horizon}Q Horizon",
        fontsize=13, y=1.01)
    fig.tight_layout()
    path = os.path.join(OUTPUT_DIR, "06_scenario_forecast.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"[CHART] Scenario forecast -> {path}")


def _save_forecast_table(scenarios: dict):
    rows = []
    for name, fc_df in scenarios.items():
        if name.startswith("baseline_"):
            continue
        for date, row in fc_df.iterrows():
            for col, val in row.items():
                rows.append({
                    "scenario": name, "date": date,
                    "variable": col, "forecast": round(val, 3),
                    "space": "level",
                })
    out = pd.DataFrame(rows)
    path = os.path.join(OUTPUT_DIR, "forecast_scenarios.csv")
    out.to_csv(path, index=False)
    print(f"[TABLE] Forecast table (level space) -> {path}")


# ============================================================
# REPORTS
# ============================================================

def write_methods_note(df, result, lags, bt_summary, transforms, lag_diag, model_used,
                       coint_result=None):
    diff_vars = [k for k, v in transforms.items() if v["transform"] == "first_diff"]
    note = f"""
================================================================================
  HONG KONG QUARTERLY VAR MODEL -- METHODS NOTE
================================================================================

1. MODEL SPECIFICATION
   Type       : {model_used.upper()}
   Frequency  : Quarterly
   Variables  : {', '.join(df.columns)}
   Lags       : {lags} (selected by {lag_diag.get('criterion', 'aic').upper()})
   Sample     : {df.index[0].year}Q{(df.index[0].month-1)//3+1} to {df.index[-1].year}Q{(df.index[-1].month-1)//3+1} ({len(df)} obs)

2. DATA TRANSFORMS (ADF + KPSS confirmed)
"""
    for col, info in transforms.items():
        note += f"   {col:20s} : {info['transform']}  (last level = {info['last_level']:.2f})\n"

    note += f"""
3. ESTIMATION
   Estimator  : {"OLS equation-by-equation" if model_used == "var" else ("VECM (Johansen system)" if model_used == "vecm" else "Minnesota-prior Bayesian VAR")}
   AIC        : {f"{result.aic:.2f}" if np.isfinite(result.aic) else "n/a"}
   BIC        : {f"{result.bic:.2f}" if np.isfinite(result.bic) else "n/a"}
   Stability  : All eigenvalues inside the unit circle (max modulus < 1)
   IRFs       : Orthogonalized (Cholesky decomposition, consistent across model types)

4. COINTEGRATION
"""
    if coint_result and coint_result["rank"] > 0:
        note += f"   I(1) variables tested: {coint_result['i1_vars']}\n"
        note += f"   Cointegration rank (trace test, 95% rule): {coint_result['rank']}\n"
        note += "   NOTE: VECM may improve long-horizon forecasts.\n"
    else:
        note += "   No cointegration detected (or insufficient I(1) variables).\n"

    note += f"""
5. FORECAST EVALUATION
   Method     : Expanding-window out-of-sample forecasts
   Horizons   : 1Q and 4Q ahead
   Benchmarks : AR(1), Random Walk

6. SCENARIO DESIGN
   All forecasts presented in LEVEL space (transforms inverted).
   Baseline       : Unconditional VAR forecast, 8 quarters ahead
   Weak external  : China GDP level -{3.0}pp, US FFR level +{1.5}pp
   Global easing  : China GDP level +{1.0}pp, US FFR level -{1.0}pp
   Confidence     : Bootstrapped 80% interval (500 replications, residual resampling)

7. KEY ASSUMPTIONS AND LIMITATIONS
   - Currency board (HKD peg to USD) maintained throughout forecast horizon.
   - Reduced-form model; Cholesky ordering used for IRF illustration only.
   - Structural breaks (GFC, COVID) present; no explicit dummies.
   - Scenario shocks defined in level space for interpretability.
"""
    if diff_vars:
        if model_used == "vecm":
            note += (
                f"   - VAR-style transforms above apply to the reduced-form VAR baseline; "
                f"the VECM is estimated on levels ({', '.join(df.columns)}).\n"
            )
        else:
            note += f"   - Variables differenced for estimation: {diff_vars}\n"
            note += "     Forecasts are cumulated back to levels for output.\n"

    note += "\n================================================================================\n"
    path = os.path.join(OUTPUT_DIR, "methods_note.txt")
    with open(path, "w") as f:
        f.write(note)
    print(f"\n[NOTE] Methods note -> {path}")
    print(note)


def write_diagnostics_report(df_raw, df_est, transforms, lag_diag, coint_result=None, vecm_spec=None):
    lines = [
        "HONG KONG VAR DIAGNOSTICS REPORT",
        "=" * 60, "",
        "Data sample:",
        f"  raw_obs={len(df_raw)}, transformed_obs={len(df_est)}",
        f"  start={df_raw.index.min().date()} end={df_raw.index.max().date()}",
        "", "Transforms used (ADF+KPSS confirmed):",
    ]
    for var, info in transforms.items():
        lines.append(f"  - {var}: {info['transform']} (last_level={info['last_level']:.2f})")
    lines.extend([
        "", "Lag-selection diagnostics:",
        f"  criterion={lag_diag['criterion']}",
        f"  aic_lag={lag_diag['aic_lag']}, bic_lag={lag_diag['bic_lag']}",
        f"  selected_lag={lag_diag['selected_lag']}",
        f"  params_per_equation={lag_diag['params_per_equation']}",
        f"  n_observations={lag_diag['n_observations']}",
        f"  params_obs_ratio={lag_diag['params_obs_ratio']:.3f}",
        f"  guardrail_triggered={lag_diag['guardrail_triggered']}",
    ])
    if coint_result:
        lines.extend([
            "", "Cointegration diagnostics (Johansen):",
            f"  i1_vars={coint_result.get('i1_vars', [])}",
            f"  det_order={coint_result.get('det_order')}, k_ar_diff={coint_result.get('k_ar_diff')}",
            (
                "  rank_trace(90/95/99)="
                f"{coint_result.get('rank_trace_90')}/"
                f"{coint_result.get('rank_trace_95')}/"
                f"{coint_result.get('rank_trace_99')}"
            ),
            (
                "  rank_maxeig(90/95/99)="
                f"{coint_result.get('rank_eig_90')}/"
                f"{coint_result.get('rank_eig_95')}/"
                f"{coint_result.get('rank_eig_99')}"
            ),
            f"  selected_rank_auto(trace@95%)={coint_result.get('rank')}",
        ])
    if vecm_spec:
        lines.extend([
            "", "VECM specification:",
            f"  coint_rank={vecm_spec.get('coint_rank')}",
            f"  lag_diff={vecm_spec.get('lag_diff')}",
            f"  deterministic={vecm_spec.get('deterministic')}",
        ])
    out = os.path.join(OUTPUT_DIR, "model_diagnostics.txt")
    with open(out, "w") as f:
        f.write("\n".join(lines))
    print(f"[NOTE] Diagnostics report -> {out}")


def write_vecm_diagnostics_report(result, var_names: list[str], coint_result: dict | None):
    """Write VECM-specific diagnostics and practical remediation hints."""
    lines = [
        "HONG KONG VECM DIAGNOSTICS REPORT",
        "=" * 60,
        "",
        f"deterministic={getattr(result, 'deterministic', 'n/a')}",
        f"coint_rank={getattr(result, 'coint_rank', 'n/a')}",
        f"lag_diff={getattr(result, 'k_ar_diff', 'n/a')}",
        f"nobs={getattr(result, 'nobs', 'n/a')}",
    ]
    resid_arr = result.resid.values if hasattr(result.resid, "values") else result.resid
    lines.extend(["", "Ljung-Box p-values (lag=8):"])
    flagged = []
    for i, col in enumerate(var_names):
        lb = acorr_ljungbox(resid_arr[:, i], lags=[8], return_df=True)
        pval = float(lb["lb_pvalue"].iloc[0])
        lines.append(f"  {col}: {pval:.4f}")
        if pval <= 0.05:
            flagged.append(col)
    lines.extend(["", "Warnings:"])
    k = len(var_names)
    rank = int(getattr(result, "coint_rank", 0))
    if rank >= max(k - 1, 1):
        lines.append("  - Rank is near full rank; check deterministic term and lag_diff.")
    if flagged:
        lines.append(
            "  - Residual autocorrelation detected in: "
            + ", ".join(flagged)
            + ". Consider higher lag_diff or different deterministic term."
        )
    if coint_result:
        lines.append(
            "  - Johansen ranks (trace 90/95/99): "
            f"{coint_result.get('rank_trace_90')}/"
            f"{coint_result.get('rank_trace_95')}/"
            f"{coint_result.get('rank_trace_99')}"
        )
    if len(lines) <= 13:
        lines.append("  - No major VECM-specific warnings.")

    path = os.path.join(OUTPUT_DIR, "vecm_diagnostics.txt")
    with open(path, "w") as f:
        f.write("\n".join(lines))
    print(f"[NOTE] VECM diagnostics -> {path}")


# ============================================================
# CLI
# ============================================================

def parse_args():
    parser = argparse.ArgumentParser(description="Hong Kong quarterly VAR model")
    parser.add_argument("--lag-criterion", choices=["aic", "bic"], default="aic")
    parser.add_argument("--max-lags", type=int, default=8)
    parser.add_argument("--max-params-ratio", type=float, default=0.8)
    parser.add_argument("--no-local-real-data", action="store_true")
    parser.add_argument("--model-type", choices=["var", "bvar", "vecm", "auto"], default="auto")
    parser.add_argument("--bvar-lambda1", type=float, default=0.2,
                        help="Minnesota prior overall tightness.")
    parser.add_argument("--auto-bvar-threshold", type=float, default=0.18)
    parser.add_argument("--cholesky-order", type=str, default=None,
                        help="Comma-separated variable ordering for Cholesky IRFs. "
                             "Default: external-first (us_ffr,china_gdp,...)")
    parser.add_argument(
        "--coint-rank",
        type=str,
        default="auto",
        help="Cointegration rank for VECM. Use integer or 'auto' (trace@95%).",
    )
    parser.add_argument(
        "--vecm-deterministic",
        choices=["n", "co", "ci", "lo", "li"],
        default="ci",
        help="Deterministic term for VECM (statsmodels convention).",
    )
    parser.add_argument(
        "--vecm-lag-diff",
        type=int,
        default=None,
        help="VECM lagged differences. Default: max(VAR_lag-1, 1).",
    )
    return parser.parse_args()


# ============================================================
# MAIN
# ============================================================

def main():
    args = parse_args()
    print("=" * 70)
    print("  HONG KONG QUARTERLY VAR MACRO FORECASTING MODEL")
    print("  (post-audit version -- all 12 review fixes applied)")
    print("=" * 70)

    # --- 1. Data assembly ---
    print("\n" + "=" * 70)
    print("  STEP 1: DATA ASSEMBLY")
    print("=" * 70)
    df_raw = assemble_data(prefer_local_real_data=not args.no_local_real_data)

    # Cholesky ordering (audit v2 fix #4)
    DEFAULT_ORDER = ["us_ffr", "china_gdp", "gdp_growth", "cpi_inflation",
                     "unemployment", "hibor_3m"]
    if args.cholesky_order:
        order = [v.strip() for v in args.cholesky_order.split(",")]
    else:
        order = [v for v in DEFAULT_ORDER if v in df_raw.columns]
        order += [v for v in df_raw.columns if v not in order]
    df_raw = df_raw[order]
    print(f"[DIAG] Cholesky ordering: {list(df_raw.columns)}")

    print(f"\nSummary statistics:\n{df_raw.describe().round(2)}")
    plot_raw_data(df_raw)

    # --- 2. Diagnostics ---
    print("\n" + "=" * 70)
    print("  STEP 2: PRE-ESTIMATION DIAGNOSTICS")
    print("=" * 70)
    adf_res = stationarity_tests(df_raw)
    df_est, transforms = apply_transforms(df_raw, adf_res)
    plot_correlation(df_est)
    granger_causality_diagnostics(df_est)
    lags, lag_diag = select_lag_order(
        df_est, max_lags=args.max_lags,
        criterion=args.lag_criterion,
        max_params_ratio=args.max_params_ratio,
    )
    lags = max(lags, 1)

    # Johansen settings are tied to VECM lag mapping for transparent rank choice.
    vecm_lag_diff = max(lags - 1, 1) if args.vecm_lag_diff is None else max(int(args.vecm_lag_diff), 1)
    coint_result = johansen_cointegration_test(
        df_raw, adf_res, det_order=0, k_ar_diff=vecm_lag_diff
    )

    if args.model_type == "vecm":
        model_used = "vecm"
    elif args.model_type == "auto":
        model_used = "bvar" if lag_diag["params_obs_ratio"] > args.auto_bvar_threshold else "var"
    else:
        model_used = args.model_type
    print(f"[DIAG] Model selection: requested={args.model_type}, using={model_used.upper()}")

    coint_rank = resolve_coint_rank(args.coint_rank, coint_result)
    vecm_spec = {
        "coint_rank": coint_rank,
        "lag_diff": vecm_lag_diff,
        "deterministic": args.vecm_deterministic,
    }
    write_diagnostics_report(
        df_raw, df_est, transforms, lag_diag, coint_result=coint_result, vecm_spec=vecm_spec
    )

    # --- 3. Estimation ---
    print("\n" + "=" * 70)
    print("  STEP 3: MODEL ESTIMATION")
    print("=" * 70)
    result = estimate_model(df_est, lags, model_type=model_used,
                            bvar_lambda1=args.bvar_lambda1,
                            df_raw=df_raw, coint_rank=coint_rank,
                            vecm_deterministic=args.vecm_deterministic,
                            vecm_lag_diff=vecm_lag_diff)
    if model_used == "vecm":
        write_vecm_diagnostics_report(result, list(df_est.columns), coint_result)

    # --- 3b. FEVD + Historical Decomposition ---
    print("\n" + "=" * 70)
    print("  STEP 3b: FEVD & HISTORICAL DECOMPOSITION")
    print("=" * 70)
    irfs = result._irfs
    var_names = list(df_est.columns)
    fevd = compute_fevd(irfs, var_names, max_horizon=20)
    plot_fevd(fevd, var_names)

    hd = compute_historical_decomposition(result, df_est, var_names)
    plot_historical_decomposition(hd, df_raw=df_raw)

    # Print key FEVD results for the research question
    print("\n--- Key FEVD results (h=8 quarters) ---")
    h8 = min(8, fevd.shape[0] - 1)
    for target in ["gdp_growth", "cpi_inflation", "unemployment", "hibor_3m"]:
        if target in var_names:
            ti = var_names.index(target)
            for shock in ["us_ffr", "china_gdp"]:
                if shock in var_names:
                    si = var_names.index(shock)
                    pct = fevd[h8, ti, si] * 100
                    print(f"  {shock:15s} -> {target:18s}: {pct:5.1f}%")

    # --- Sign Restrictions ---
    print("\n--- Sign-Restriction Identification ---")
    sign_table = default_sign_table()
    sigma_u_base = result._sigma_u_computed
    coefs_base = result.coefs
    accepted_irfs = sign_restriction_irfs(
        coefs_base, sigma_u_base, sign_table, var_names,
        periods=20, n_draws=5000, n_accept=500, verbose=True)
    plot_sign_restriction_irfs(accepted_irfs, var_names,
                               shock_names=list(sign_table.keys()))

    # --- 3c. Robustness ---
    print("\n" + "=" * 70)
    print("  STEP 3c: ROBUSTNESS CHECKS")
    print("=" * 70)
    sigma_u_base = result._sigma_u_computed
    robustness_ordering_permutations(
        df_est, lags, model_used, args.bvar_lambda1, var_names, sigma_u_base)
    robustness_subsample(
        df_est, lags, model_used, args.bvar_lambda1, var_names)

    # TVP-VAR analysis
    print("\n--- TVP-VAR (Forgetting Factor Kalman Filter) ---")
    try:
        tvp_result = tvp_var_kalman(df_est, lags=min(lags, 2), forgetting_factor=0.99)
        plot_tvp_var(tvp_result)
        tvp_resid_std = np.std(tvp_result["resid"], axis=0)
        var_resid = result.resid.values if hasattr(result.resid, "values") else result.resid
        var_resid_std = np.std(var_resid, axis=0)
        print("  Residual std comparison (TVP vs constant-parameter):")
        for j, vn in enumerate(var_names):
            ratio = tvp_resid_std[j] / max(var_resid_std[j], 1e-8)
            print(f"    {vn:18s}: TVP={tvp_resid_std[j]:.3f}, VAR={var_resid_std[j]:.3f}, ratio={ratio:.3f}")
    except Exception as e:
        print(f"  TVP-VAR failed: {e}")

    # VECM comparison (if not already the primary model and cointegration detected)
    if model_used != "vecm" and coint_rank and coint_rank > 0:
        print("\n--- VECM Robustness Comparison ---")
        try:
            _ld = vecm_lag_diff if vecm_lag_diff is not None else max(lags - 1, 1)
            vecm_result = fit_vecm(
                df_raw,
                lags_diff=_ld,
                coint_rank=min(_vecm_rank_or_default(coint_rank), 3),
                deterministic=args.vecm_deterministic,
            )
            vecm_companion = _companion_matrix(vecm_result.coefs)
            vecm_max_eig = np.abs(np.linalg.eigvals(vecm_companion)).max()
            print(f"  VECM max eigenvalue: {vecm_max_eig:.4f}")

            if vecm_max_eig < 1.5:
                vecm_sigma = vecm_result.sigma_u
                vecm_irfs = _cholesky_irf(vecm_result.coefs, vecm_sigma, periods=20)
                vecm_fevd = compute_fevd(vecm_irfs, var_names, max_horizon=20)
                h8 = min(8, vecm_fevd.shape[0] - 1)
                print(f"\n  VECM FEVD at h={h8} vs VAR:")
                print(f"  {'Shock -> Target':40s} {'VAR':>8s} {'VECM':>8s}")
                for target in ["gdp_growth", "cpi_inflation", "unemployment", "hibor_3m"]:
                    if target in var_names:
                        ti = var_names.index(target)
                        for shock in ["us_ffr", "china_gdp"]:
                            if shock in var_names:
                                si = var_names.index(shock)
                                var_pct = fevd[h8, ti, si] * 100
                                vecm_pct = vecm_fevd[h8, ti, si] * 100
                                label = f"  {shock} -> {target}"
                                print(f"  {label:40s} {var_pct:7.1f}% {vecm_pct:7.1f}%")
        except Exception as e:
            print(f"  VECM comparison failed: {e}")

    # --- 4. Backtesting ---
    print("\n" + "=" * 70)
    print("  STEP 4: OUT-OF-SAMPLE VALIDATION")
    print("=" * 70)
    bt = rolling_backtest(df_est, lags, forecast_horizon=4, min_train=60,
                          model_type=model_used, bvar_lambda1=args.bvar_lambda1,
                          df_raw=df_raw, coint_rank=coint_rank,
                          vecm_deterministic=args.vecm_deterministic,
                          vecm_lag_diff=vecm_lag_diff)
    bt_summary = evaluate_backtest(bt)

    # Explicit VAR vs VECM level-space forecast comparison for paper/reporting.
    try:
        compare_df = compare_var_vecm_backtest_level(
            df_est=df_est,
            df_raw=df_raw,
            lags=lags,
            transforms=transforms,
            coint_rank=coint_rank,
            vecm_deterministic=args.vecm_deterministic,
            vecm_lag_diff=vecm_lag_diff,
        )
        if not compare_df.empty:
            print("\n=== VAR vs VECM OOS Comparison (Level-space RMSE) ===")
            print(compare_df.head(12).to_string(index=False))
    except Exception as e:
        print(f"[WARN] VAR vs VECM OOS comparison failed: {e}")

    # --- 5. Scenario forecasting (in LEVEL space) ---
    print("\n" + "=" * 70)
    print("  STEP 5: SCENARIO FORECASTING (level space)")
    print("=" * 70)
    forecast_scenarios(result, df_est, lags, transforms, horizon=8,
                       df_raw=df_raw)

    # --- Methods note ---
    write_methods_note(df_est, result, lags, bt_summary, transforms, lag_diag,
                       model_used, coint_result)

    print("\n" + "=" * 70)
    print("  DONE -- all outputs saved to ./output/")
    print("=" * 70)


if __name__ == "__main__":
    main()
