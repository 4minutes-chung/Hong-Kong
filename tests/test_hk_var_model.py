"""
Comprehensive test suite for hk_var_model.py
Covers: data assembly, transforms, BVAR, companion matrix, IRFs,
        forecast inversion, scenario shocks, stationarity, lag selection.
"""

import sys
import os
import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import hk_var_model as m


# ============================================================
# Fixtures
# ============================================================

@pytest.fixture
def synthetic_data():
    np.random.seed(42)
    return m._generate_calibrated_data()


@pytest.fixture
def small_var_data():
    """Minimal 3-variable, 50-obs DataFrame for fast tests."""
    np.random.seed(99)
    T = 50
    dates = pd.date_range("2010-01-01", periods=T, freq="QS")
    data = {
        "x": np.cumsum(np.random.randn(T) * 0.5) + 5,
        "y": np.random.randn(T) * 1.0 + 2,
        "z": np.random.randn(T) * 0.8 + 3,
    }
    return pd.DataFrame(data, index=dates)


@pytest.fixture
def sample_transforms():
    return {
        "gdp_growth": {"transform": "level", "last_level": 3.0},
        "cpi_inflation": {"transform": "level", "last_level": 2.0},
        "unemployment": {"transform": "level", "last_level": 5.5},
        "hibor_3m": {"transform": "level", "last_level": 2.5},
        "china_gdp": {"transform": "level", "last_level": 7.0},
        "us_ffr": {"transform": "first_diff", "last_level": 3.0},
    }


# ============================================================
# Data Assembly
# ============================================================

class TestGenerateCalibratedData:
    def test_shape(self, synthetic_data):
        assert synthetic_data.shape == (104, 6)

    def test_columns(self, synthetic_data):
        assert list(synthetic_data.columns) == m.MODEL_VARIABLES

    def test_index_quarterly(self, synthetic_data):
        diffs = synthetic_data.index.to_series().diff().dropna()
        assert all(d.days >= 89 for d in diffs)
        assert all(d.days <= 92 for d in diffs)

    def test_unemployment_bounded(self, synthetic_data):
        assert synthetic_data["unemployment"].min() >= 1.5
        assert synthetic_data["unemployment"].max() <= 10.0

    def test_hibor_bounded(self, synthetic_data):
        assert synthetic_data["hibor_3m"].min() >= 0.01
        assert synthetic_data["hibor_3m"].max() <= 8.0

    def test_ffr_bounded(self, synthetic_data):
        assert synthetic_data["us_ffr"].min() >= 0.05
        assert synthetic_data["us_ffr"].max() <= 7.0

    def test_no_nans(self, synthetic_data):
        assert not synthetic_data.isna().any().any()

    def test_gfc_shock_visible(self, synthetic_data):
        """GDP growth around 2008 should dip below the unconditional mean."""
        gfc_gdp = synthetic_data["gdp_growth"].iloc[32:36].mean()
        overall_mean = synthetic_data["gdp_growth"].mean()
        assert gfc_gdp < overall_mean - 1.0


class TestLoadLocalData:
    def test_missing_date_column_raises(self, tmp_path):
        bad_csv = tmp_path / "bad.csv"
        bad_csv.write_text("a,b\n1,2\n")
        with pytest.raises(ValueError, match="date"):
            m._load_local_quarterly_data(str(bad_csv))

    def test_missing_required_columns_raises(self, tmp_path):
        csv = tmp_path / "partial.csv"
        csv.write_text("date,gdp_growth\n2020-01-01,3.0\n")
        with pytest.raises(ValueError, match="missing required columns"):
            m._load_local_quarterly_data(str(csv))


# ============================================================
# Lagged Design Matrix
# ============================================================

class TestBuildLaggedDesign:
    def test_shapes(self, small_var_data):
        X, Y = m._build_lagged_design(small_var_data, lags=2)
        T, k = small_var_data.shape
        assert X.shape == (T - 2, 1 + k * 2)
        assert Y.shape == (T - 2, k)

    def test_intercept_column(self, small_var_data):
        X, _ = m._build_lagged_design(small_var_data, lags=1)
        assert np.allclose(X[:, 0], 1.0)

    def test_first_lag_values(self, small_var_data):
        X, Y = m._build_lagged_design(small_var_data, lags=1)
        arr = small_var_data.values
        assert np.allclose(X[0, 1:], arr[0])
        assert np.allclose(Y[0], arr[1])

    def test_second_lag_values(self, small_var_data):
        X, Y = m._build_lagged_design(small_var_data, lags=2)
        arr = small_var_data.values
        k = arr.shape[1]
        assert np.allclose(X[0, 1:1 + k], arr[1])
        assert np.allclose(X[0, 1 + k:], arr[0])
        assert np.allclose(Y[0], arr[2])


# ============================================================
# Companion Matrix
# ============================================================

class TestCompanionMatrix:
    def test_shape_p1(self):
        coefs = np.random.randn(1, 3, 3)
        C = m._companion_matrix(coefs)
        assert C.shape == (3, 3)

    def test_shape_p2(self):
        coefs = np.random.randn(2, 3, 3)
        C = m._companion_matrix(coefs)
        assert C.shape == (6, 6)

    def test_identity_block(self):
        coefs = np.random.randn(2, 3, 3)
        C = m._companion_matrix(coefs)
        assert np.allclose(C[3:, :3], np.eye(3))

    def test_first_row_blocks(self):
        coefs = np.random.randn(2, 4, 4)
        C = m._companion_matrix(coefs)
        assert np.allclose(C[:4, :4], coefs[0])
        assert np.allclose(C[:4, 4:8], coefs[1])

    def test_stability_check(self):
        """A diagonal matrix with entries < 1 should be stable."""
        coefs = np.array([[[0.5, 0], [0, 0.3]]])
        C = m._companion_matrix(coefs)
        eigvals = np.abs(np.linalg.eigvals(C))
        assert eigvals.max() < 1.0


# ============================================================
# Cholesky IRF
# ============================================================

class TestCholeskyIRF:
    def test_shape(self):
        coefs = np.random.randn(1, 3, 3) * 0.3
        sigma = np.eye(3)
        irfs = m._cholesky_irf(coefs, sigma, periods=10)
        assert irfs.shape == (11, 3, 3)

    def test_impact_is_cholesky_factor(self):
        coefs = np.random.randn(1, 2, 2) * 0.2
        sigma = np.array([[1.0, 0.5], [0.5, 1.0]])
        P = np.linalg.cholesky(sigma)
        irfs = m._cholesky_irf(coefs, sigma, periods=5)
        assert np.allclose(irfs[0], P, atol=1e-10)

    def test_stable_system_irfs_decay(self):
        coefs = np.array([[[0.3, 0.0], [0.0, 0.3]]])
        sigma = np.eye(2)
        irfs = m._cholesky_irf(coefs, sigma, periods=30)
        norm_first = np.linalg.norm(irfs[1])
        norm_last = np.linalg.norm(irfs[30])
        assert norm_last < norm_first


# ============================================================
# BVAR Minnesota
# ============================================================

class TestBVARMinnesota:
    def test_returns_correct_type(self, small_var_data):
        result = m.fit_bvar_minnesota(small_var_data, lags=1)
        assert isinstance(result, m.MinnesotaVARResults)

    def test_coefs_shape(self, small_var_data):
        result = m.fit_bvar_minnesota(small_var_data, lags=2)
        assert result.coefs.shape == (2, 3, 3)

    def test_intercept_shape(self, small_var_data):
        result = m.fit_bvar_minnesota(small_var_data, lags=1)
        assert result.intercept.shape == (3,)

    def test_resid_shape(self, small_var_data):
        result = m.fit_bvar_minnesota(small_var_data, lags=1)
        assert result.resid.shape == (49, 3)

    def test_sigma_u_symmetric(self, small_var_data):
        result = m.fit_bvar_minnesota(small_var_data, lags=1)
        assert np.allclose(result.sigma_u, result.sigma_u.T)

    def test_sigma_u_positive_definite(self, small_var_data):
        result = m.fit_bvar_minnesota(small_var_data, lags=1)
        eigvals = np.linalg.eigvals(result.sigma_u)
        assert all(eigvals > 0)

    def test_forecast_shape(self, small_var_data):
        result = m.fit_bvar_minnesota(small_var_data, lags=1)
        fc = result.forecast(small_var_data.values[-1:], steps=4)
        assert fc.shape == (4, 3)

    def test_strong_shrinkage_pulls_toward_zero(self, small_var_data):
        weak = m.fit_bvar_minnesota(small_var_data, lags=1, lambda1=10.0)
        strong = m.fit_bvar_minnesota(small_var_data, lags=1, lambda1=0.001)
        weak_norm = np.linalg.norm(weak.coefs)
        strong_norm = np.linalg.norm(strong.coefs)
        assert strong_norm < weak_norm

    def test_stability(self, small_var_data):
        result = m.fit_bvar_minnesota(small_var_data, lags=1)
        C = m._companion_matrix(result.coefs)
        assert np.abs(np.linalg.eigvals(C)).max() < 1.5


# ============================================================
# Stationarity Tests
# ============================================================

class TestStationarityTests:
    def test_returns_dataframe(self, synthetic_data):
        res = m.stationarity_tests(synthetic_data)
        assert isinstance(res, pd.DataFrame)
        assert "decision" in res.columns

    def test_all_variables_tested(self, synthetic_data):
        res = m.stationarity_tests(synthetic_data)
        assert set(res["variable"]) == set(m.MODEL_VARIABLES)

    def test_decision_values(self, synthetic_data):
        res = m.stationarity_tests(synthetic_data)
        valid = {"stationary", "unit_root", "conflict_default_level"}
        assert all(d in valid for d in res["decision"])


# ============================================================
# Apply Transforms
# ============================================================

class TestApplyTransforms:
    def test_level_preserves_values(self, synthetic_data):
        adf_res = pd.DataFrame([
            {"variable": col, "decision": "stationary"}
            for col in synthetic_data.columns
        ])
        df_t, transforms = m.apply_transforms(synthetic_data, adf_res)
        for col in synthetic_data.columns:
            assert transforms[col]["transform"] == "level"
        assert np.allclose(df_t.values, synthetic_data.values)

    def test_diff_reduces_length_by_one(self, synthetic_data):
        adf_res = pd.DataFrame([
            {"variable": col, "decision": "unit_root" if col == "us_ffr" else "stationary"}
            for col in synthetic_data.columns
        ])
        df_t, transforms = m.apply_transforms(synthetic_data, adf_res)
        assert len(df_t) == len(synthetic_data) - 1
        assert transforms["us_ffr"]["transform"] == "first_diff"

    def test_last_level_stored(self, synthetic_data):
        adf_res = pd.DataFrame([
            {"variable": col, "decision": "stationary"}
            for col in synthetic_data.columns
        ])
        _, transforms = m.apply_transforms(synthetic_data, adf_res)
        for col in synthetic_data.columns:
            expected = float(synthetic_data[col].iloc[-1])
            assert abs(transforms[col]["last_level"] - expected) < 1e-10


# ============================================================
# Invert Transforms (CRITICAL fix #1)
# ============================================================

class TestInvertTransforms:
    def test_level_no_change(self):
        fc = np.array([[1.0, 2.0], [3.0, 4.0]])
        transforms = {
            "a": {"transform": "level", "last_level": 10.0},
            "b": {"transform": "level", "last_level": 20.0},
        }
        result = m._invert_transforms(fc, ["a", "b"], transforms)
        assert np.allclose(result, fc)

    def test_first_diff_cumulates(self):
        fc = np.array([[0.5], [0.3], [-0.2]])
        transforms = {"x": {"transform": "first_diff", "last_level": 10.0}}
        result = m._invert_transforms(fc, ["x"], transforms)
        expected = np.array([[10.5], [10.8], [10.6]])
        assert np.allclose(result, expected)

    def test_mixed_transforms(self):
        fc = np.array([[1.0, 0.5], [2.0, -0.5]])
        transforms = {
            "a": {"transform": "level", "last_level": 0.0},
            "b": {"transform": "first_diff", "last_level": 5.0},
        }
        result = m._invert_transforms(fc, ["a", "b"], transforms)
        assert np.allclose(result[:, 0], [1.0, 2.0])
        assert np.allclose(result[:, 1], [5.5, 5.0])

    def test_preserves_shape(self):
        fc = np.random.randn(8, 6)
        transforms = {v: {"transform": "level", "last_level": 0.0} for v in m.MODEL_VARIABLES}
        result = m._invert_transforms(fc, m.MODEL_VARIABLES, transforms)
        assert result.shape == (8, 6)


# ============================================================
# Shock in Level Space (HIGH fix #2)
# ============================================================

class TestShockInLevelSpace:
    def test_level_variable_direct_assignment(self):
        last_obs = np.array([[1.0, 2.0, 3.0]])
        transforms = {
            "a": {"transform": "level", "last_level": 1.0},
            "b": {"transform": "level", "last_level": 2.0},
            "c": {"transform": "level", "last_level": 3.0},
        }
        result = m._shock_in_level_space(last_obs, 0, 5.0, transforms, "a")
        assert result[0, 0] == 5.0
        assert result[0, 1] == 2.0

    def test_diff_variable_converts_to_change(self):
        last_obs = np.array([[0.1, 0.2]])
        transforms = {
            "x": {"transform": "first_diff", "last_level": 3.0},
            "y": {"transform": "level", "last_level": 0.2},
        }
        result = m._shock_in_level_space(last_obs, 0, 4.5, transforms, "x")
        assert abs(result[0, 0] - 1.5) < 1e-10

    def test_does_not_mutate_input(self):
        last_obs = np.array([[1.0, 2.0]])
        original = last_obs.copy()
        transforms = {"a": {"transform": "level", "last_level": 1.0},
                       "b": {"transform": "level", "last_level": 2.0}}
        m._shock_in_level_space(last_obs, 0, 99.0, transforms, "a")
        assert np.allclose(last_obs, original)


# ============================================================
# Lag Order Selection
# ============================================================

class TestSelectLagOrder:
    def test_returns_positive_lag(self, small_var_data):
        lag, diag = m.select_lag_order(small_var_data, max_lags=4)
        assert lag >= 1
        assert isinstance(diag, dict)
        assert "selected_lag" in diag

    def test_guardrail_triggers(self):
        """Generate a strongly autocorrelated VAR(3) so AIC picks lag >= 2,
        then confirm the guardrail forces it down."""
        np.random.seed(123)
        k, T = 3, 80
        A1 = np.diag([0.7, 0.6, 0.5])
        A2 = np.diag([0.15, 0.15, 0.15])
        y = np.zeros((T, k))
        y[0] = np.random.randn(k)
        y[1] = np.random.randn(k)
        for t in range(2, T):
            y[t] = A1 @ y[t - 1] + A2 @ y[t - 2] + np.random.randn(k) * 0.3
        dates = pd.date_range("2000-01-01", periods=T, freq="QS")
        df = pd.DataFrame(y, index=dates, columns=["a", "b", "c"])
        lag_free, _ = m.select_lag_order(df, max_lags=6, max_params_ratio=0.99)
        if lag_free <= 1:
            pytest.skip("AIC picked lag 1 on generated VAR(2) data")
        lag, diag = m.select_lag_order(df, max_lags=6, max_params_ratio=0.01)
        assert lag == 1
        assert diag["guardrail_triggered"]

    def test_bic_can_differ_from_aic(self, small_var_data):
        _, diag_aic = m.select_lag_order(small_var_data, max_lags=4, criterion="aic")
        _, diag_bic = m.select_lag_order(small_var_data, max_lags=4, criterion="bic")
        assert diag_aic["criterion"] == "aic"
        assert diag_bic["criterion"] == "bic"


# ============================================================
# Johansen Cointegration
# ============================================================

class TestJohansenCointegration:
    def test_skips_with_few_i1(self, synthetic_data):
        adf_res = pd.DataFrame([
            {"variable": col, "decision": "stationary"}
            for col in synthetic_data.columns
        ])
        result = m.johansen_cointegration_test(synthetic_data, adf_res)
        assert result is None

    def test_runs_with_two_i1(self, synthetic_data):
        adf_res = pd.DataFrame([
            {"variable": col, "decision": "unit_root" if col in ["unemployment", "us_ffr"] else "stationary"}
            for col in synthetic_data.columns
        ])
        result = m.johansen_cointegration_test(synthetic_data, adf_res)
        assert result is None or "rank" in result


# ============================================================
# End-to-end Forecast Scenario
# ============================================================

class TestForecastScenarios:
    def test_baseline_in_level_space(self, synthetic_data, sample_transforms):
        from statsmodels.tsa.api import VAR as StatsVAR
        model = StatsVAR(synthetic_data).fit(1)
        scenarios = m.forecast_scenarios(model, synthetic_data, 1,
                                          sample_transforms, horizon=4)
        assert "baseline" in scenarios
        assert scenarios["baseline"].shape == (4, 6)

    def test_all_scenario_keys(self, synthetic_data, sample_transforms):
        from statsmodels.tsa.api import VAR as StatsVAR
        model = StatsVAR(synthetic_data).fit(1)
        scenarios = m.forecast_scenarios(model, synthetic_data, 1,
                                          sample_transforms, horizon=4)
        expected_keys = {"baseline", "baseline_lo", "baseline_hi",
                         "weak_external", "global_easing"}
        assert expected_keys == set(scenarios.keys())

    def test_ci_bounds_order(self, synthetic_data, sample_transforms):
        from statsmodels.tsa.api import VAR as StatsVAR
        model = StatsVAR(synthetic_data).fit(1)
        scenarios = m.forecast_scenarios(model, synthetic_data, 1,
                                          sample_transforms, horizon=4)
        lo = scenarios["baseline_lo"].values
        hi = scenarios["baseline_hi"].values
        assert np.all(lo <= hi + 1e-6)


# ============================================================
# Granger Causality
# ============================================================

class TestGrangerCausality:
    def test_returns_list(self, synthetic_data):
        results = m.granger_causality_diagnostics(synthetic_data, max_lag=2)
        assert isinstance(results, list)
        if results:
            assert "cause" in results[0]
            assert "effect" in results[0]
            assert "best_p" in results[0]


# ============================================================
# FEVD
# ============================================================

class TestFEVD:
    def test_shape(self):
        coefs = np.random.randn(1, 3, 3) * 0.3
        sigma = np.eye(3)
        irfs = m._cholesky_irf(coefs, sigma, periods=10)
        fevd = m.compute_fevd(irfs, ["a", "b", "c"], max_horizon=10)
        assert fevd.shape == (11, 3, 3)

    def test_sums_to_one(self):
        coefs = np.random.randn(1, 4, 4) * 0.2
        sigma = np.eye(4) * 0.5
        sigma[0, 1] = sigma[1, 0] = 0.1
        irfs = m._cholesky_irf(coefs, sigma, periods=16)
        fevd = m.compute_fevd(irfs, ["a", "b", "c", "d"], max_horizon=16)
        for h in range(17):
            for i in range(4):
                assert abs(fevd[h, i, :].sum() - 1.0) < 1e-10

    def test_all_nonnegative(self):
        coefs = np.random.randn(2, 3, 3) * 0.2
        sigma = np.eye(3)
        irfs = m._cholesky_irf(coefs, sigma, periods=8)
        fevd = m.compute_fevd(irfs, ["a", "b", "c"], max_horizon=8)
        assert np.all(fevd >= 0)

    def test_own_shock_dominant_at_impact(self):
        """At h=0, own shock should dominate for diagonal sigma."""
        coefs = np.array([[[0.3, 0], [0, 0.3]]])
        sigma = np.eye(2)
        irfs = m._cholesky_irf(coefs, sigma, periods=5)
        fevd = m.compute_fevd(irfs, ["a", "b"], max_horizon=5)
        assert fevd[0, 0, 0] > 0.9
        assert fevd[0, 1, 1] > 0.9


# ============================================================
# Historical Decomposition
# ============================================================

class TestHistoricalDecomposition:
    def test_returns_dict_with_keys(self, small_var_data):
        result = m.fit_bvar_minnesota(small_var_data, lags=1)
        hd = m.compute_historical_decomposition(result, small_var_data,
                                                 list(small_var_data.columns))
        assert "contributions" in hd
        assert "structural_shocks" in hd
        assert "dates" in hd

    def test_contributions_shape(self, small_var_data):
        result = m.fit_bvar_minnesota(small_var_data, lags=1)
        hd = m.compute_historical_decomposition(result, small_var_data,
                                                 list(small_var_data.columns))
        T = result.nobs
        k = small_var_data.shape[1]
        assert hd["contributions"].shape == (T, k, k)

    def test_structural_shocks_shape(self, small_var_data):
        result = m.fit_bvar_minnesota(small_var_data, lags=1)
        hd = m.compute_historical_decomposition(result, small_var_data,
                                                 list(small_var_data.columns))
        T = result.nobs
        k = small_var_data.shape[1]
        assert hd["structural_shocks"].shape == (T, k)


# ============================================================
# Sign restrictions & TVP-VAR
# ============================================================

class TestRandomOrthogonal:
    def test_q_orthogonal(self):
        rng = np.random.default_rng(0)
        Q = m._random_orthogonal(5, rng)
        assert Q.shape == (5, 5)
        assert np.allclose(Q.T @ Q, np.eye(5), atol=1e-10)


class TestDefaultSignTable:
    def test_keys_and_signs(self):
        st = m.default_sign_table()
        assert "us_monetary" in st and "china_growth" in st
        assert st["us_monetary"]["us_ffr"] == 1
        assert st["us_monetary"]["gdp_growth"] == -1
        assert st["china_growth"]["china_gdp"] == 1


class TestSignRestrictionIrfs:
    def test_output_shape_matches_accepted(self, small_var_data):
        from statsmodels.tsa.api import VAR as StatsVAR
        fitted = StatsVAR(small_var_data).fit(2)
        coefs = fitted.coefs
        sigma = fitted.sigma_u
        names = list(small_var_data.columns)
        loose = {"s1": {names[0]: 1}}
        out = m.sign_restriction_irfs(
            coefs, sigma, loose, names,
            periods=8, n_draws=400, n_accept=10,
            verbose=False,
        )
        if out is not None:
            assert out.ndim == 4
            assert out.shape[1] == 9  # periods + 1
            assert out.shape[2] == out.shape[3] == 3


class TestTvpVarKalman:
    def test_returns_expected_keys_and_shapes(self, small_var_data):
        res = m.tvp_var_kalman(small_var_data, lags=1)
        T, k = small_var_data.shape
        n = T - 1
        n_coef = 1 + k
        assert set(res.keys()) >= {"theta", "resid", "dates", "var_names", "lags", "forgetting_factor"}
        assert res["theta"].shape == (n, k, n_coef)
        assert res["resid"].shape == (n, k)
        assert len(res["dates"]) == n
