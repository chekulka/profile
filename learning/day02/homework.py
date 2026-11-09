"""Day 2 homework: hypothesis testing done right.

Run:  python learning/day02/homework.py
Fill in every TODO. Each check prints PASS or FAIL.
"""
import numpy as np
import statsmodels.api as sm
from scipy import stats


def check(name, got, expected, tol):
    ok = got is not None and abs(float(got) - float(expected)) <= tol
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: got {got}, expected ~{expected:.4f}")
    return ok


rng = np.random.default_rng(7)
print("Day 2 homework: parts with unfinished TODOs are skipped silently.")

# ---------------------------------------------------------------------------
# Part 1: Welch's t-test by hand (unequal sizes AND variances)
# ---------------------------------------------------------------------------
control = rng.normal(loc=10.0, scale=2.0, size=3000)
treatment = rng.normal(loc=10.2, scale=4.0, size=5000)

diff = None  # TODO: treatment mean - control mean
se = None    # TODO: sqrt(var_c/n_c + var_t/n_t), with ddof=1 sample variances
t_stat = None  # TODO: diff / se

ref = stats.ttest_ind(treatment, control, equal_var=False)
if t_stat is not None:
    check("Part 1 Welch t by hand vs scipy", t_stat, ref.statistic, 1e-8)

# ---------------------------------------------------------------------------
# Part 2: a t-test IS a regression
# ---------------------------------------------------------------------------
y = np.concatenate([control, treatment])
T = np.concatenate([np.zeros(len(control)), np.ones(len(treatment))])
X = sm.add_constant(T)

ols_hc2 = None  # TODO: sm.OLS(y, X).fit(cov_type="HC2")
if ols_hc2 is not None and diff is not None and se is not None:
    check("Part 2a beta equals diff in means", ols_hc2.params[1], diff, 1e-10)
    check("Part 2b HC2 SE equals Welch SE", ols_hc2.bse[1], se, 1e-10)
    plain = sm.OLS(y, X).fit()
    print(f"   plain OLS SE = {plain.bse[1]:.4f} vs Welch SE = {se:.4f}  "
          "<- Q-A: which is wrong here, and why?")

# ---------------------------------------------------------------------------
# Part 3: p-values are uniform under H0 (simulated A/A tests)
# ---------------------------------------------------------------------------
def welch_pvalue(a, b):
    return None  # TODO: Welch t-test p-value comparing b and a (scipy.stats.ttest_ind)


def aa_pvalues(n_tests, n_per_arm, draw):
    """Run n_tests A/A tests (both arms drawn from the same distribution)."""
    if welch_pvalue(draw(5), draw(5)) is None:
        return None
    return np.array([welch_pvalue(draw(n_per_arm), draw(n_per_arm)) for _ in range(n_tests)])


normal_draw = lambda n: rng.normal(0, 1, n)
p_normal = aa_pvalues(2000, 200, normal_draw)
fpr_normal = None  # TODO: share of p_normal below 0.05
if fpr_normal is not None:
    check("Part 3 false positive rate is about 5%", fpr_normal, 0.05, 0.015)
    # Q-B (answers.md): plot a histogram of p_normal. What shape is it, and why?

# ---------------------------------------------------------------------------
# Part 4: the CLT and skewed revenue
# ---------------------------------------------------------------------------
# Revenue: 95% of users spend 0, the rest spend a heavy-tailed (lognormal) amount.
def revenue_draw(n):
    buys = rng.random(n) < 0.05
    return np.where(buys, rng.lognormal(mean=3.0, sigma=1.5, size=n), 0.0)


TRUE_MEAN = 0.05 * np.exp(3.0 + 1.5**2 / 2)  # true revenue per user, about 3.09


def ci_contains(value, mean, se):
    return None  # TODO: True if the 95% CI mean +/- 1.96*se contains value


def ci_coverage(n, n_sims=2000):
    """Share of 95% CIs for mean revenue per user (one arm) that contain the truth."""
    hits = 0
    for _ in range(n_sims):
        x = revenue_draw(n)
        inside = ci_contains(TRUE_MEAN, x.mean(), x.std(ddof=1) / np.sqrt(n))
        if inside is None:
            return None
        hits += int(inside)
    return hits / n_sims


coverage = {n: ci_coverage(n) for n in (40, 400, 4000, 20000)}
if coverage[40] is not None:
    print("   coverage by n:", {n: round(c, 3) for n, c in coverage.items()}, "(target 0.95)")
    check("Part 4 n=40 badly under-covers", coverage[40], 0.51, 0.06)
    check("Part 4 n=20000 is close (but still below 0.95)", coverage[20000], 0.92, 0.03)
# Q-C (answers.md): why is coverage still below 95% even at n=4,000? Name 2
# practical fixes and the trade-off each one carries. (Bonus: A/A *differences*
# of two equally skewed arms cover much better. Why? Hint: symmetry.)

# ---------------------------------------------------------------------------
# Part 5: bootstrap CI for a difference in MEDIANS (no simple SE formula)
# ---------------------------------------------------------------------------
sess_a = rng.exponential(scale=5.0, size=1500)   # session minutes, control
sess_b = rng.exponential(scale=5.6, size=1500)   # treatment

def resample(x):
    return None  # TODO: same-size resample of x WITH replacement (rng.choice)


B = 2000
boot = None
if resample(sess_a) is not None:
    boot = np.array([np.median(resample(sess_b)) - np.median(resample(sess_a))
                     for _ in range(B)])

lo, hi = None, None  # TODO: 2.5th and 97.5th percentiles of boot (np.percentile)
true_diff = 5.6 * np.log(2) - 5.0 * np.log(2)  # median of Exp(scale) = scale*ln2
if lo is not None:
    print(f"   bootstrap 95% CI for median diff: [{lo:.3f}, {hi:.3f}], truth {true_diff:.3f}")
    print(f"[{'PASS' if lo <= true_diff <= hi and hi - lo < 1.5 else 'FAIL'}] "
          "Part 5 CI contains the true median difference")

# ---------------------------------------------------------------------------
# Part 6: sample size intuition (the sqrt(n) law)
# ---------------------------------------------------------------------------
# For sigma = 4 and n per arm, SE = sqrt(2*sigma^2/n). You currently have
# n = 10_000 per arm. How many users per arm do you need to HALVE the SE?
n_needed = None  # TODO
if n_needed is not None:
    check("Part 6 users per arm to halve the SE", n_needed, 40_000, 0)
