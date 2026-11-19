"""Day 12 homework: CUPED from scratch.

Run:  python learning/day12/homework.py
Fill in every TODO. Parts with unfinished TODOs are skipped.
"""
import numpy as np
import statsmodels.api as sm
from scipy import stats

rng = np.random.default_rng(12)
print("Day 12 homework")


def check(name, got, expected, tol):
    ok = got is not None and abs(float(got) - float(expected)) <= tol
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: got {got}, expected ~{expected}")
    return ok


def generate(n, effect=0.1, rho=0.7):
    """x = pre-period metric (e.g. last month's sessions); y = in-experiment metric."""
    x = rng.normal(10, 2, n)
    noise = rng.normal(0, 2 * np.sqrt(1 - rho**2), n)
    t = rng.integers(0, 2, n)
    y = 10 + rho * (x - 10) + noise + effect * t
    return x, y, t


# ---------------------------------------------------------------------------
# Part 1: implement CUPED
# ---------------------------------------------------------------------------
def cuped(y, x):
    """Return the CUPED-adjusted metric y - theta * (x - mean(x)), theta = cov(y,x)/var(x).

    theta is computed on the POOLED data (both arms), which keeps the estimate unbiased.
    """
    theta = None  # TODO: np.cov(y, x)[0, 1] / x.var(ddof=1)
    if theta is None:
        return None
    return y - theta * (x - x.mean())


x, y, t = generate(20_000)
y_adj = cuped(y, x)
if y_adj is not None:
    rho = np.corrcoef(x, y)[0, 1]
    var_ratio = y_adj.var() / y.var()
    print(f"   corr(x, y) = {rho:.3f}; variance kept after CUPED = {var_ratio:.3f}")
    check("Part 1 variance reduction equals 1 - rho^2", var_ratio, 1 - rho**2, 1e-6)

    # -----------------------------------------------------------------------
    # Part 2: CUPED is (essentially) regression adjustment
    # -----------------------------------------------------------------------
    d_cuped = y_adj[t == 1].mean() - y_adj[t == 0].mean()
    ols = None  # TODO: sm.OLS(y, sm.add_constant(np.column_stack([t, x]))).fit(cov_type="HC1")
    if ols is not None:
        check("Part 2 CUPED effect matches OLS with the pre-period covariate", d_cuped, ols.params[1], 1e-3)
        # Q-A (answers.md): why are they nearly (not exactly) identical? (Hint: theta
        # is pooled vs. the OLS slope is estimated holding t fixed.)

    # -----------------------------------------------------------------------
    # Part 3: power and unbiasedness over 500 simulated experiments (n = 4,000)
    # -----------------------------------------------------------------------
    rej_raw = rej_cuped = 0
    estimates = []
    for _ in range(500):
        xs, ys, ts = generate(4000)
        ya = cuped(ys, xs)
        rej_raw += stats.ttest_ind(ys[ts == 1], ys[ts == 0]).pvalue < 0.05
        rej_cuped += None or 0  # TODO: replace `None or 0` with the CUPED t-test rejection (ya)
        estimates.append(ya[ts == 1].mean() - ya[ts == 0].mean())
    print(f"   power: raw {rej_raw/500:.2f} | CUPED {rej_cuped/500:.2f}")
    print(f"   mean CUPED estimate {np.mean(estimates):.4f} (true effect 0.1000)")
    check("Part 3a CUPED is unbiased", np.mean(estimates), 0.1, 0.01)
    print(f"[{'PASS' if rej_cuped / 500 > rej_raw / 500 + 0.15 else 'FAIL'}] "
          "Part 3b CUPED adds a lot of power")
    # Q-B (answers.md): CUPED kept about 51% of the variance. How many users does
    # the raw analysis need to match CUPED's precision at n = 4,000?

    # -----------------------------------------------------------------------
    # Part 4: new users have no pre-period data
    # -----------------------------------------------------------------------
    x4, y4, t4 = generate(20_000)
    has_history = rng.random(20_000) < 0.7      # 30% are new users
    x_filled = None  # TODO: x4 where has_history, else the mean of x4 over users WITH history
    if x_filled is not None:
        y4_adj = cuped(y4, x_filled)
        kept = y4_adj.var() / y4.var()
        print(f"   variance kept with 30% new users: {kept:.3f}")
        check("Part 4 variance kept is about 0.7*(1-rho^2) + 0.3", kept, 0.7 * 0.51 + 0.3, 0.03)
        # Q-C (answers.md): what other pre-period covariates could you use for new
        # users (e.g. signup channel, device)? Why must the covariate never be affected
        # by the treatment?
