"""Day 16 homework: CUPAC (ML-based variance reduction) and post-stratification.

Run:  python learning/day16/homework.py
Needs scikit-learn (pip install scikit-learn).
Fill in every TODO. Parts with unfinished TODOs are skipped.
"""
import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor

rng = np.random.default_rng(16)
print("Day 16 homework")


def check(name, got, expected, tol):
    ok = got is not None and abs(float(got) - float(expected)) <= tol
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: got {got}, expected ~{expected}")
    return ok


# ---------------------------------------------------------------------------
# World: 8 pre-assignment features + platform (0/1/2) drive the outcome NONLINEARLY.
# No single pre-period feature predicts the outcome well.
# ---------------------------------------------------------------------------
def features(n):
    return rng.normal(size=(n, 8)), rng.integers(0, 3, n)


def outcome(X, platform):
    return (10 + 3 * np.sin(X[:, 0]) + 2 * X[:, 1] * X[:, 2] + 1.5 * (X[:, 3] > 0)
            + 2 * platform + X[:, 4] + rng.normal(0, 1.5, len(platform)))


def variance_kept(y, covariate):
    """CUPED with a single covariate: share of Var(y) left after adjustment."""
    theta = np.cov(y, covariate)[0, 1] / covariate.var(ddof=1)
    return (y - theta * (covariate - covariate.mean())).var() / y.var()


# ---------------------------------------------------------------------------
# Part 1: CUPAC: train a model on HISTORICAL data, use its prediction as the covariate
# ---------------------------------------------------------------------------
X_hist, p_hist = features(30_000)          # last quarter, before the experiment
y_hist = outcome(X_hist, p_hist)

model = None  # TODO: HistGradientBoostingRegressor(max_iter=300).fit(np.column_stack([X_hist, p_hist]), y_hist)

n = 20_000
X, plat = features(n)                       # the experiment's users (features fixed pre-assignment)
t = rng.integers(0, 2, n)
y = outcome(X, plat) + 0.2 * t              # true effect = 0.2

if model is not None:
    prediction = model.predict(np.column_stack([X, plat]))
    kept_single = variance_kept(y, X[:, 4])      # best single linear feature
    kept_cupac = variance_kept(y, prediction)
    print(f"   variance kept: CUPED on one feature {kept_single:.2f} | CUPAC {kept_cupac:.2f}")
    print(f"[{'PASS' if kept_cupac < 0.3 and kept_single > 0.85 else 'FAIL'}] "
          "Part 1 CUPAC removes far more variance than a single covariate")

    # -----------------------------------------------------------------------
    # Part 2: CUPAC stays unbiased (the model never saw treatment or outcomes after assignment)
    # -----------------------------------------------------------------------
    estimates = []
    for _ in range(200):
        Xs, ps = features(4000)
        ts = rng.integers(0, 2, 4000)
        ys = outcome(Xs, ps) + 0.2 * ts
        pred = model.predict(np.column_stack([Xs, ps]))
        theta = np.cov(ys, pred)[0, 1] / pred.var(ddof=1)
        ya = ys - theta * (pred - pred.mean())
        estimates.append(None)  # TODO: replace None with the effect estimate from ya (treated mean - control mean)
    if None not in estimates:
        print(f"   mean CUPAC estimate {np.mean(estimates):.3f} (truth 0.200), sd {np.std(estimates):.3f}")
        check("Part 2 CUPAC is unbiased", np.mean(estimates), 0.2, 0.03)
        # Q-A (answers.md): what would go wrong if you trained the model on the
        # experiment's OWN outcomes (including treated users)? How does cross-fitting help?


# ---------------------------------------------------------------------------
# Part 3: post-stratification by platform
# ---------------------------------------------------------------------------
def post_stratified(y, t, strata):
    """Sum over strata of weight_s * (treated mean_s - control mean_s); weight = stratum share."""
    est = 0.0
    for s in np.unique(strata):
        in_s = strata == s
        w = None  # TODO: share of all users in stratum s
        if w is None:
            return None
        est += w * (y[in_s & (t == 1)].mean() - y[in_s & (t == 0)].mean())
    return est


plain, strat = [], []
for _ in range(500):
    Xs, ps = features(4000)
    ts = rng.integers(0, 2, 4000)
    ys = outcome(Xs, ps) + 0.2 * ts
    plain.append(ys[ts == 1].mean() - ys[ts == 0].mean())
    strat.append(post_stratified(ys, ts, ps))
if None not in strat:
    ratio = np.std(strat) / np.std(plain)
    print(f"   sd: unadjusted {np.std(plain):.4f} | post-stratified {np.std(strat):.4f} (ratio {ratio:.2f})")
    check("Part 3a post-stratification is unbiased", np.mean(strat), 0.2, 0.02)
    print(f"[{'PASS' if ratio < 0.95 else 'FAIL'}] Part 3b post-stratifying on platform reduces noise")
    # Q-B (answers.md): platform explains about 18% of the variance here, and CUPAC
    # explains about 82%. When would post-stratification still be the right tool?
    # (Hint: simplicity, transparency, few strong categorical predictors, no history.)
