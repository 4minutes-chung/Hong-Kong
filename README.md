# HK Monetary Transmission — BVAR(4) Evidence

> How do US monetary policy and China growth shocks transmit to Hong Kong GDP under the currency board?
> **1998Q1–2025Q4 | 112 quarters | BVAR(4) Minnesota prior | Cholesky identification**

---

## Transmission Channels

```
US FFR ──→ HIBOR ──┬──→ PROPERTY ──→ ┐
                   │                  ├──→ GDP
                   └──────────────────┘  (direct credit/mortgage)

CHINA GDP ──→ EXPORTS ──────────────────→ GDP
```

---

## GDP Variance Decomposition (FEVD, h=8)

```
property → GDP  ████████████████████░░░░░░░░░░  20.9%  ← dominant driver
exports  → GDP  ████████████████░░░░░░░░░░░░░░  16.5%
hibor    → GDP  ████████░░░░░░░░░░░░░░░░░░░░░░   8.3%
```

---

## IRF Significance Map (90% credibility bands)

```
              h=1    h=2    h=4
hibor → prop   ●      ○      ○     fast, fades after h=1
hibor → gdp    ●      ●      ●     persistent through h=4
prop  → gdp    ●      ●      ○     amplifies h=1–2
exp   → gdp    ●      ●      ○     robust at h=1–2

●  significant (CI excludes zero)
○  CI crosses zero
```

---

## Speed Asymmetry Within Channel 1

```
         h=1    h=2    h=4    h=8
prop     [●]    [○]    [○]    [○]   hits hard, fades
credit   [●]    [●]    [●]    [○]   sustained via mortgage/investment
```

Property is the primary GDP variance amplifier (20.9% FEVD).  
Direct credit channel outlasts it — that's the persistence.

---

## ZLB Asymmetry (HIBOR → Property)

```
Normal rate environment  (FFR ≥ 0.25%)   β = −2.68  ✓  significant
ZIRP                     (FFR < 0.25%)   β = −0.60  ✗  CI spans zero

2009Q1–2022Q1: 36/112 obs at zero bound
```

Monetary transmission impaired when rates are pinned at floor.

---

## Model Spec

```
BVAR(4) Minnesota prior
  pi1 = 0.085   own-lag shrinkage
  pi2 = 1.0     cross-lag shrinkage (no decay)
  pi4 = 100     exogenous (uninformative)
  delta = [0.442, 0.627, 0.418, 0.545, 0.735, 0.991]
          hibor  exp    prop  gdp   cpi   unemp   ← ML-optimised

Cholesky order:  hibor → exports → property → gdp → cpi → unemployment
Exogenous:       us_ffr, china_gdp  (contemporaneous only, q=0)
OOS RMSE:        BVAR wins 18/18 cells vs VARX(1) benchmark
```

---

## Robustness

```
Structural stability   Chow GDP 2008 p=0.15 ✓   GDP 2020 p=0.26 ✓
                       CPI COVID mean break p=0.03  (acknowledged)
                       Bai-Perron: 0 breaks in all variables ✓

LP-IRF (Jordà 2005)    all 4 channels replicated, HAC SEs ✓
Δu robustness          headline IRFs unchanged with Δunemployment ✓
FFR lag sensitivity    VARX(4,1) LB unchanged, keep q=0 ✓
Johansen rank=0        VECM not warranted ✓
```

---

## Files

| File | Role |
|---|---|
| `HK_BVAR_Final.ipynb` | Canonical — all results, 6 sections |
| `HK_BVAR_Exploration.ipynb` | Scratch space |
| `fetch_real_data.py` | Rebuild data from APIs |
| `paper/main.tex` | Paper draft |
| `data_source.md` | Variable definitions and stationarity results |

---

## Refresh Data

```bash
python fetch_real_data.py
# → data/hk_macro_varx_ready.csv
```
