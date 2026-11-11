"""Day 4 homework: ratio metrics and the delta method.

Run:  python learning/day04/homework.py
Fill in every TODO. Parts with unfinished TODOs are skipped.
"""
import numpy as np
import statsmodels.api as sm

rng = np.random.default_rng(4)
print("Day 4 homework")


def check(name, got, expected, tol):
    ok = got is not None and abs(float(got) - float(expected)) <= tol
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: got {got}, expected ~{expected:.6f}")
    return ok


def simulate_users(n):
    """Each user has a number of sessions and their own click-through rate."""
    sessions = rng.poisson(5, n) + 1                 # X_i
    user_ctr = rng.beta(2, 8, n)                     # heavy and light clickers
    clicks = rng.binomial(sessions, user_ctr)        # Y_i
    return sessions, clicks


# ---------------------------------------------------------------------------
# Part 1: implement the delta method for R = mean(Y) / mean(X)
# ---------------------------------------------------------------------------
def delta_var(sessions, clicks):
    """Return (Var(R_hat), R_hat) using user-level sample moments (ddof=1)."""
    n = len(sessions)
    mx, my = sessions.mean(), clicks.mean()
    R = my / mx
    var_x, var_y = sessions.var(ddof=1), clicks.var(ddof=1)
    cov_xy = np.cov(clicks, sessions, ddof=1)[0, 1]
    var_R = None  # TODO: (var_y - 2*R*cov_xy + R**2*var_x) / (n * mx**2)
    return var_R, R


s, c = simulate_users(5000)
var_R, R = delta_var(s, c)

if var_R is not None:
    # Session-level regression with SEs clustered by user = delta method, exactly
    user_id = np.repeat(np.arange(len(s)), s)
    y = np.concatenate([np.r_[np.ones(k), np.zeros(m - k)] for k, m in zip(c, s)])
    clustered = sm.OLS(y, np.ones_like(y)).fit(cov_type="cluster", cov_kwds={"groups": user_id})
    check("Part 1 delta SE equals clustered-regression SE", np.sqrt(var_R), clustered.bse[0], 1e-10)

    # -----------------------------------------------------------------------
    # Part 2: the naive SE (treating every session as independent)
    # -----------------------------------------------------------------------
    naive_se = None  # TODO: sqrt(R*(1-R) / total_sessions)
    if naive_se is not None:
        ratio = np.sqrt(var_R) / naive_se
        print(f"   delta SE / naive SE = {ratio:.3f}")
        check("Part 2 naive SE is too small by about 18%", ratio, 1.22, 0.06)
        # Q-A (answers.md): (ratio)^2 is the design effect. What does it mean in words?

    # -----------------------------------------------------------------------
    # Part 3: bootstrap by resampling USERS
    # -----------------------------------------------------------------------
    def boot_ratio_se(sessions, clicks, B=1000):
        stats_ = []
        for _ in range(B):
            idx = None  # TODO: resample user indices with replacement (rng.integers or rng.choice)
            if idx is None:
                return None
            stats_.append(clicks[idx].sum() / sessions[idx].sum())
        return np.std(stats_, ddof=1)

    bse = boot_ratio_se(s, c)
    if bse is not None:
        check("Part 3 user bootstrap SE is close to the delta SE", bse / np.sqrt(var_R), 1.0, 0.08)


# ---------------------------------------------------------------------------
# Part 4: A/A tests - naive vs delta false positive rates
# ---------------------------------------------------------------------------
def aa_rates(n_tests=1000, n_users=2000):
    naive_rej = delta_rej = 0
    for _ in range(n_tests):
        s1, c1 = simulate_users(n_users)
        s2, c2 = simulate_users(n_users)
        v1, R1 = delta_var(s1, c1)
        v2, R2 = delta_var(s2, c2)
        if v1 is None:
            return None, None
        p_pool = (c1.sum() + c2.sum()) / (s1.sum() + s2.sum())
        z_naive = (R2 - R1) / np.sqrt(p_pool * (1 - p_pool) * (1 / s1.sum() + 1 / s2.sum()))
        z_delta = None  # TODO: (R2 - R1) / sqrt(v1 + v2)
        if z_delta is None:
            return None, None
        naive_rej += abs(z_naive) > 1.96
        delta_rej += abs(z_delta) > 1.96
    return naive_rej / n_tests, delta_rej / n_tests


fpr_naive, fpr_delta = aa_rates()
if fpr_delta is not None:
    print(f"   A/A false positive rate: naive {fpr_naive:.3f} | delta {fpr_delta:.3f} (target 0.05)")
    check("Part 4 delta FPR is about 5%", fpr_delta, 0.05, 0.02)
    check("Part 4 naive FPR is inflated (about 11%)", fpr_naive, 0.11, 0.03)
    # Q-B (answers.md): your team has shipped 40 "significant" CTR wins analyzed
    # the naive way. Roughly how many might be false positives, and what would you do?


# ---------------------------------------------------------------------------
# Part 5: ratio of totals vs mean of per-user ratios
# ---------------------------------------------------------------------------
ratio_of_totals = c.sum() / s.sum()
mean_of_ratios = None  # TODO: mean over users of clicks_i / sessions_i
if mean_of_ratios is not None:
    print(f"   ratio of totals = {ratio_of_totals:.4f} | mean of ratios = {mean_of_ratios:.4f}")
    print("[PASS] Part 5 computed" if abs(mean_of_ratios - np.mean(c / s)) < 1e-12 else "[FAIL] Part 5")
    # Q-C (answers.md): they are almost equal here because, in this simulation, a
    # user's number of sessions is independent of their CTR. Describe a real
    # product where they would diverge sharply, and say which one you'd report.
