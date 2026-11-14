"""Weekend project (Week 1): an A/A test harness that audits analysis methods.

An A/A test compares two groups that received the SAME experience. A trustworthy
analysis method should produce uniformly distributed p-values over many A/A tests
(and about 5% false positives at alpha = 0.05). This harness checks that for any
method, the way experimentation platforms validate themselves.

Run:  python learning/day07/homework.py
Fill in every TODO. Parts with unfinished TODOs are skipped.
"""
import numpy as np
from scipy import stats

rng = np.random.default_rng(7)
print("Weekend project: A/A test harness")


# ---------------------------------------------------------------------------
# Data generator (from Day 4): users with sessions and their own click-through rate
# ---------------------------------------------------------------------------
def simulate_users(n):
    sessions = rng.poisson(5, n) + 1
    clicks = rng.binomial(sessions, rng.beta(2, 8, n))
    return sessions, clicks


# ---------------------------------------------------------------------------
# Part 1: the harness
# ---------------------------------------------------------------------------
def run_aa(analysis, n_tests=1000, n_users=2000):
    """Run n_tests A/A tests and return the array of p-values from `analysis`.

    Each test: draw two independent groups with simulate_users(n_users) and call
    analysis(s_a, c_a, s_b, c_b) -> p-value.
    """
    pvals = []
    for _ in range(n_tests):
        p = None  # TODO: draw groups A and B, then call analysis(...) and store the p-value
        if p is None:
            return None
        pvals.append(p)
    return np.array(pvals)


def audit(name, pvals):
    """Report the false positive rate and a uniformity test (KS) for the p-values."""
    fpr = (pvals < 0.05).mean()
    ks_p = None  # TODO: stats.kstest(pvals, "uniform").pvalue
    if ks_p is None:
        return None
    verdict = "TRUSTWORTHY" if ks_p > 0.01 and abs(fpr - 0.05) < 0.02 else "BROKEN"
    print(f"   {name:<28} FPR={fpr:.3f}  KS p={ks_p:.3f}  -> {verdict}")
    return verdict


# ---------------------------------------------------------------------------
# Part 2: three analysis methods to audit
# ---------------------------------------------------------------------------
def user_level_ttest(s_a, c_a, s_b, c_b):
    """Correct: compare clicks PER USER with Welch's t-test (Day 2)."""
    return stats.ttest_ind(c_b, c_a, equal_var=False).pvalue


def naive_session_ztest(s_a, c_a, s_b, c_b):
    """Wrong: treats every session as independent (Day 4 trap)."""
    ra, rb = c_a.sum() / s_a.sum(), c_b.sum() / s_b.sum()
    pool = (c_a.sum() + c_b.sum()) / (s_a.sum() + s_b.sum())
    z = (rb - ra) / np.sqrt(pool * (1 - pool) * (1 / s_a.sum() + 1 / s_b.sum()))
    return 2 * stats.norm.sf(abs(z))


def delta_method_ztest(s_a, c_a, s_b, c_b):
    """Correct for the ratio metric CTR = clicks/sessions (Day 4)."""
    def var_ratio(s, c):
        n, mx = len(s), s.mean()
        R = c.mean() / mx
        return (c.var(ddof=1) - 2 * R * np.cov(c, s, ddof=1)[0, 1] + R**2 * s.var(ddof=1)) / (n * mx**2), R
    va, ra = var_ratio(s_a, c_a)
    vb, rb = var_ratio(s_b, c_b)
    z = None  # TODO: (rb - ra) / sqrt(va + vb)
    return None if z is None else 2 * stats.norm.sf(abs(z))


results = {}
for name, fn in [("user-level t-test", user_level_ttest),
                 ("naive session z-test", naive_session_ztest),
                 ("delta-method z-test", delta_method_ztest)]:
    p = run_aa(fn)
    if p is None:
        break
    v = audit(name, p)
    if v is None:
        break
    results[name] = v

if len(results) == 3:
    expected = {"user-level t-test": "TRUSTWORTHY", "naive session z-test": "BROKEN",
                "delta-method z-test": "TRUSTWORTHY"}
    ok = results == expected
    print(f"[{'PASS' if ok else 'FAIL'}] Part 2 the harness separates correct from broken methods")

# ---------------------------------------------------------------------------
# Part 3: the harness also audits ASSIGNMENT (SRM rate)
# ---------------------------------------------------------------------------
def srm_rate(assign, n_tests=2000, n=10_000):
    """Share of A/A tests that trip the SRM alarm (p < 0.001) for an assignment function."""
    alarms = 0
    for _ in range(n_tests):
        arms = assign(n)
        counts = np.bincount(arms, minlength=2)
        alarms += stats.chisquare(counts).pvalue < 0.001
    return alarms / n_tests


def good_assign(n):
    return rng.integers(0, 2, n)


def buggy_assign(n):
    """A 'sticky' bug: 2% of users who should be in treatment get forced into control."""
    arms = rng.integers(0, 2, n)
    flip = (arms == 1) & (rng.random(n) < 0.02)
    arms[flip] = 0
    return arms


rate_good = None       # TODO: srm_rate(good_assign)
rate_bug_small = None  # TODO: srm_rate(buggy_assign) with n=10_000 users per test
rate_bug_large = None  # TODO: srm_rate(buggy_assign, n_tests=500, n=200_000)
if None not in (rate_good, rate_bug_small, rate_bug_large):
    print(f"   SRM alarm rate: good {rate_good:.4f} | bug @10k users {rate_bug_small:.3f} "
          f"| bug @200k users {rate_bug_large:.3f}")
    ok = rate_good < 0.005 and rate_bug_small < 0.3 and rate_bug_large > 0.9
    print(f"[{'PASS' if ok else 'FAIL'}] Part 3 the same bug is invisible in small tests, obvious in large ones")
    # Q-B (answers.md): explain the difference using chi2 = 4k^2/N from Day 6.
    # What should a platform do so that small experiments don't hide assignment bugs?
    # (Hint: think about pooling SRM checks across all experiments that share the
    # assignment service.)

# ---------------------------------------------------------------------------
# Part 4 (write-up in answers.md, about 1 page): your portfolio README
# ---------------------------------------------------------------------------
# Q-A: write a short README for this harness as if it were a GitHub project:
#   what problem it solves, how to use it, the results table from Part 2, and one
#   paragraph on why platforms (OpenAI, Discord) run A/A tests continuously.
