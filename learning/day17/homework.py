"""Day 17 homework: variance reduction for RATIO metrics, and what the gain is really worth.

Run:  python learning/day17/homework.py
Fill in every TODO. Parts with unfinished TODOs are skipped.
"""
import math
import numpy as np

rng = np.random.default_rng(17)
print("Day 17 homework")


def check(name, got, expected, tol):
    ok = got is not None and abs(float(got) - float(expected)) <= tol
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: got {got}, expected ~{expected}")
    return ok


# ---------------------------------------------------------------------------
# Data: CTR = clicks / sessions, randomized by user. Treatment lifts CTR by 3%.
# Each user has a persistent activity level and a persistent click-through rate.
# ---------------------------------------------------------------------------
n = 40_000
t = rng.integers(0, 2, n)
activity = rng.gamma(3, 2, n)
user_ctr = rng.beta(3, 12, n)
sessions = rng.poisson(activity) + 1
clicks = rng.binomial(sessions, np.clip(user_ctr * (1 + 0.03 * t), 0, 1))

# Pre-period data: a 1-week window and a 4-week window
s_pre1 = rng.poisson(activity) + 1
c_pre1 = rng.binomial(s_pre1, user_ctr)
s_pre4 = rng.poisson(4 * activity) + 1
c_pre4 = rng.binomial(s_pre4, user_ctr)


def delta_method(s, c):
    """(ratio, variance of ratio) from Day 4."""
    m, mx = len(s), s.mean()
    R = c.mean() / mx
    v = (c.var(ddof=1) - 2 * R * np.cov(c, s, ddof=1)[0, 1] + R**2 * s.var(ddof=1)) / (m * mx**2)
    return R, v


def diff_and_se(metric, t):
    a, b = metric[t == 0], metric[t == 1]
    return b.mean() - a.mean(), np.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))


# ---------------------------------------------------------------------------
# Part 1: linearization turns a ratio metric into a per-user metric
# ---------------------------------------------------------------------------
def linearize(s, c):
    """Per-user linearized CTR: L_i = (c_i - R * s_i) / mean(s), with R = sum(c)/sum(s) pooled."""
    R = c.sum() / s.sum()
    return None  # TODO: (c - R * s) / s.mean()


L = linearize(sessions, clicks)
if L is not None:
    R0, v0 = delta_method(sessions[t == 0], clicks[t == 0])
    R1, v1 = delta_method(sessions[t == 1], clicks[t == 1])
    d_lin, se_lin = diff_and_se(L, t)
    print(f"   delta method: diff {R1 - R0:.6f}, SE {np.sqrt(v0 + v1):.6f}")
    print(f"   linearized:   diff {d_lin:.6f}, SE {se_lin:.6f}")
    check("Part 1a linearized diff equals delta-method diff", d_lin, R1 - R0, 1e-5)
    check("Part 1b linearized SE equals delta-method SE (ratio)", se_lin / np.sqrt(v0 + v1), 1.0, 0.01)
    # Q-A (answers.md): why is linearization useful? (Hint: once the metric is
    # per-user, CUPED, regression and every per-user tool apply directly.)

    # -----------------------------------------------------------------------
    # Part 2: CUPED on the linearized metric; does the pre-period window matter?
    # -----------------------------------------------------------------------
    def cuped_kept(L, L_pre):
        theta = None  # TODO: cov(L, L_pre) / var(L_pre)
        if theta is None:
            return None
        return (L - theta * (L_pre - L_pre.mean())).var() / L.var()

    kept_1w = cuped_kept(L, linearize(s_pre1, c_pre1))
    kept_4w = cuped_kept(L, linearize(s_pre4, c_pre4))
    if kept_1w is not None:
        print(f"   variance kept: 1-week pre-period {kept_1w:.2f} | 4-week pre-period {kept_4w:.2f}")
        check("Part 2 a 4-week pre-period window gives about a 24% cut", kept_4w, 0.76, 0.04)
        print(f"[{'PASS' if kept_4w < kept_1w - 0.05 else 'FAIL'}] Part 2 a longer pre-period window helps")

        # -------------------------------------------------------------------
        # Part 3: what is the gain worth in calendar time?
        # -------------------------------------------------------------------
        # Without CUPED, this CTR test needs 35 days. Sample size (and so duration)
        # scales with variance. Tests should run in full weeks (Day 3, Day 5).
        raw_days = 35
        days_needed = None  # TODO: raw_days * kept_4w
        weeks_needed = None  # TODO: round days_needed UP to whole weeks (math.ceil(days / 7))
        if days_needed is not None and weeks_needed is not None:
            print(f"   with CUPED: {days_needed:.1f} days, which is {weeks_needed} full weeks (was 5)")
            check("Part 3 duration in full weeks", weeks_needed, 4, 0)
            # Q-B (answers.md): with only the 1-week pre-period, how many full weeks?
            # What does this tell you about reporting "x% variance reduction" to PMs?
