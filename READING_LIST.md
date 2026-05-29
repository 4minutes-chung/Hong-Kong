# Reading List — HK External-Shock Transmission Project

Date: 2026-05-24  
Purpose: Learning-focused reading plan for model interpretation and validation (portfolio side project, not journal submission).

## Core 10 (Must Read)

1. Sims, C. A. (1980), "Macroeconomics and Reality," *Econometrica*, 48(1), 1-48.  
   Why: Foundation for reduced-form VAR interpretation and claim boundaries.  
   Extract: Keep claims as dynamic associations; justify identification assumptions.

2. Johansen, S. (1991), "Estimation and Hypothesis Testing of Cointegration Vectors in Gaussian VAR Models," *Econometrica*, 59(6), 1551-1580.  
   Why: Core reference for VECM rank and deterministic-term decisions.  
   Extract: Rank and deterministic specification sensitivity must be reported.

3. Banbura, M., Giannone, D., Reichlin, L. (2010), "Large Bayesian VARs," *Journal of Applied Econometrics*, 25(1), 71-92.  
   Why: Practical BVAR robustness logic for larger systems.  
   Extract: Shrinkage should scale with model dimensionality.

4. Giannone, D., Lenza, M., Primiceri, G. (2015), "Prior Selection for VARs," *Review of Economics and Statistics*, 97(2), 436-451.  
   Why: Data-informed prior tuning for BVAR.  
   Extract: Avoid arbitrary prior strength; show prior sensitivity.

5. Giacomini, R., White, H. (2006), "Tests of Conditional Predictive Ability," *Econometrica*, 74(6), 1545-1578.  
   Why: Stronger forecast-comparison discipline than RMSE alone.  
   Extract: Compare models conditionally, not only on full-sample averages.

6. Genberg, H., Liu, L.-g., Jin, X. (2006), "Hong Kong's Economic Integration and Business Cycle Synchronisation with Mainland China and the US," HKMA RM 11/2006.  
   Why: HK-specific benchmark for US-vs-China channel decomposition.  
   Extract: Distinguish common global factors from direct China effects.

7. He, D., Liao, W., Wu, T. (2015), "Hong Kong's Growth Synchronization with China and the U.S.: A Trend and Cycle Analysis," IMF WP/15/82.  
   Why: Closest framing to dual-anchor HK transmission.  
   Extract: Trend/cycle separation changes interpretation.

8. Kang, J. S. (2016), "Private Sector Activity in Hong Kong SAR and the Fed," IMF WP/16/35.  
   Why: Currency-board pass-through framing for US rates to HK conditions.  
   Extract: Transmission strength can vary by macro-financial state.

9. Chen, H., Tsang, A. (2020), "Impact of US monetary policy rate shock and other external shocks on the Hong Kong economy," *Pacific Economic Review*, 25(1), 3-20.  
   Why: External-shock decomposition directly relevant to current project.  
   Extract: US shocks load on rates/financial conditions; China on real activity.

10. HKMA (2018), "Linked Exchange Rate System Operations — Mechanism and Theory," RM 11/2018.  
    Why: Institutional mechanics needed for interpreting HIBOR behavior.  
    Extract: LERS mechanics should anchor US -> HIBOR narrative.

## Advanced 10 (Optional Deepening)

1. Hills, R. et al. (2019), "The international transmission of monetary policy through financial centres: evidence from the UK and Hong Kong," *JIMF*, 90, 76-98.  
2. Buch, C. et al. (2018), "The International Transmission of Monetary Policy," NBER WP 24454.  
3. Wu, T., Wong, K., Cheng, M. (2017), HKMA RM 03/2017 (HK housing short-run dynamics).  
4. Genberg, H. (2005), BIS WP 187 / HKIMR WP 06/2005 (external shocks in Asia).  
5. Bai, J., Perron, P. (2003), *JAE*, 18(1), 1-22 (multiple structural breaks).  
6. Gregory, A., Hansen, B. (1996), *Journal of Econometrics*, 70(1), 99-126 (cointegration with regime shifts).  
7. Clark, T., McCracken, M. (2001), *Journal of Econometrics*, 105(1), 85-110 (nested forecast tests).  
8. Engle, R., Granger, C. (1987), *Econometrica*, 55(2), 251-276 (ECM representation).  
9. Romer, C., Romer, D. (2004), *AER*, 94(4), 1055-1084 (clean monetary shock construction).  
10. Rey, H. (2015), "Dilemma not Trilemma," NBER WP 21162.

## Newly Added (May 2026)

Added following Prof. K. Lai's advice (2026-05-23) and the BVAR vs. VECM discussion that followed.

### Papers cited in today's discussion

1. Litterman, R. (1986), "Forecasting with Bayesian VARs — Five Years of Experience," *Journal of Business & Economic Statistics*, 4(1), 25-38.  
   Why: The original Minnesota prior paper — the primary justification for why BVAR(4) is the preferred spec over VECM in small samples.  
   Extract: Minnesota shrinkage was designed precisely for short macro time series; its small-sample dominance over unrestricted OLS is the reason BVAR, not VARX(4), is the baseline here.

2. Clements, M.P., Hendry, D.F. (1998), *Forecasting Economic Time Series*, Cambridge University Press.  
   Why: The foundational reference for the empirical finding that VARs in levels often beat ECMs/VECMs in forecasting competitions, even when cointegration is genuine.  
   Extract: Rank misspecification in VECM — estimating the wrong number of cointegrating vectors — typically costs more forecast accuracy than the efficiency gain from imposing a correct cointegrating restriction.

3. Christoffersen, P.F., Diebold, F.X. (1998), "Cointegration and Long-Horizon Forecasting," *Journal of Business & Economic Statistics*, 16(4), 450-458.  
   Why: The most direct empirical result relevant to the BVAR-vs-VECM decision: even when cointegration exists, BVAR in levels can dominate VECM at short-to-medium horizons.  
   Extract: Cointegration improves forecasts mainly at long horizons (h >> 8); at h=1–4 (our OOS window), BVAR in levels is competitive or better.

### Additional recommended papers

4. Strachan, R.W. (2003), "Valid Bayesian Estimation of the Cointegrating Error Correction Model," *Journal of Business & Economic Statistics*, 21(1), 185-195.  
   Why: Canonical reference for Bayesian VECM estimation — the methodology behind the alexandria `VectorErrorCorrection` class with `prior_type` parameter. Read this before running BVECM to understand what the priors are actually doing.  
   Extract: Priors on the cointegration space must be placed carefully; a flat prior on the full parameter space does not translate into a flat prior on the cointegrating rank, which can bias rank inference in small samples.

5. Koop, G., Korobilis, D. (2010), "Bayesian Multivariate Time Series Methods for Empirical Macroeconomics," *Foundations and Trends in Econometrics*, 3(4), 267-358.  
   Why: The most comprehensive reference covering both BVAR and BVECM methodology in a single source — directly relevant to the conditional BVECM step in Phase 8.4b.  
   Extract: Chapter-level comparisons of Minnesota BVAR vs. BVECM in small samples; the authors note BVAR in levels is often preferred when cointegrating rank is uncertain, which is exactly our situation (rank=0 at 95%, rank=1 only at 90%).

6. Carriero, A., Clark, T., Marcellino, M. (2015), "Bayesian VARs: Specification Choices and Forecast Accuracy," *Journal of Applied Econometrics*, 30(1), pp. TBC.  
   Why: Systematic evaluation of BVAR specification choices (lag length, prior strength, shrinkage form) under different sample sizes — directly relevant to the Phase 8 re-estimation on an extended sample where prior-tuning needs revisiting.  
   Extract: Optimal shrinkage is sample-size dependent; hyperparameters calibrated on one sample should be re-optimized when the sample length changes materially.

### Literature Sprint additions (May 2026 — targeted gaps for Phase 6–8)

7. Cushman, D.O., Zha, T. (1997), "Identifying Monetary Policy in a Small Open Economy Under Flexible Exchange Rates," *Journal of Monetary Economics*, 40(3), 731–768. **Skim abstract + Section 2 only.**  
   Why: Canonical reference for the block-recursive SVAR where foreign variables (FFR, China GDP) are treated as exogenous to the domestic block. Direct justification for the BVARX specification. A referee who asks "why exogenous?" expects this citation.  
   Extract: Block recursion is the standard small-open-economy identification assumption — the domestic economy cannot contemporaneously affect foreign variables within the quarter.

8. Del Negro, M., Schorfheide, F. (2011), "Bayesian Macroeconometrics," in *Handbook of Bayesian Econometrics*, Oxford University Press, Chapter 7.  
   Why: Authoritative handbook chapter on BVAR methodology. Relevant specifically for the prior sensitivity discussion (Section 3) — how ML-selected hyperparameters change as sample size grows. Read before Phase 8.3 hyperparameter re-optimization.  
   Extract: As T → ∞, optimal shrinkage (pi1) decreases toward zero — with large samples, data dominate the prior. Re-optimizing pi1 after extending the sample is not optional; it is expected.

9. Dungey, M., Pagan, A. (2000), "A Structural VAR Model of the Australian Economy," *Economic Record*, 76(235), 321–342. **Skim only.**  
   Why: Applied example of block-recursive BVARX for a small open economy (Australia). Shows exactly how to implement and defend the exogenous-block assumption in practice. Useful as a template for the methodology section of the paper.  
   Extract: Treating the foreign block as exogenous is standard for small open economies; the key identifying assumption is contemporaneous non-response of foreign variables to domestic shocks.

## 7-Day Reading Sprint

1. Day 1: HKMA RM 11/2018 + RM 11/2006; produce one-page LERS transmission map.  
2. Day 2: IMF WP/15/82 + Chen/Tsang (2020); map US-vs-China channels.  
3. Day 3: IMF WP/16/35 + Hills et al. (2019); list transmission assumptions.  
4. Day 4: Sims (1980) + Johansen (1991); write claim-boundary checklist.  
5. Day 5: Banbura et al. (2010) + Giannone et al. (2015); write BVAR prior protocol.  
6. Day 6: Giacomini/White (2006) + Clark/McCracken (2001); write forecast-test protocol.  
7. Day 7: Bai/Perron (2003) + Gregory/Hansen (1996) + HKMA RM 03/2017; write break/cointegration robustness addendum.

## Do-Not-Overread (For This Cycle)

Skip for now:

- Deep DSGE monetary theory
- High-frequency shock-identification stacks
- Large multi-country GVAR builds

Current bottlenecks are VECM specification robustness, forecast validation discipline, and HK/LERS interpretation quality.
