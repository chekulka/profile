"""Day 18 homework: the peeking problem, simulated.

Run:  python learning/day18/homework.py
Fill in every TODO. Parts with unfinished TODOs are skipped.
"""
import numpy as np
from scipy import stats

rng = np.random.default_rng(18)
print("Day 18 homework")


def check(name, got, expected, tol):
    ok = got is not None and abs(float(got) - float(expected)) <= tol
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: got {got}, expected ~{expected}")
    return ok


# ---------------------------------------------------------------------------
# Setup: a 28-day test. Each day adds an equal batch of users. Under H0, each day's
# data contributes an independent N(0, 1) "z-increment"; the cumulative z after k days
# is (sum of the first k increments) / sqrt(k). This is exactly what a dashboard
# re-computing the t-test every day shows.
# ---------------------------------------------------------------------------
SIMS, DAYS = 20_000, 28
increments = rng.normal(0, 1, (SIMS, DAYS))
z_daily = None  # TODO: increments.cumsum(axis=1) / np.sqrt(np.arange(1, DAYS + 1))


# ---------------------------------------------------------------------------
# Part 1: false positive rate when you stop at the first "significant" look
# ---------------------------------------------------------------------------
def fpr_with_looks(z, looks):
    """Peek `looks` times at evenly spaced days (the last look is day 28); 'win' if any |z| > 1.96."""
    days = np.round(DAYS * np.arange(1, looks + 1) / looks).astype(int) - 1
    return None  # TODO: share of simulations where ANY of z[:, days] has |z| > 1.96


if z_daily is not None and fpr_with_looks(z_daily, 1) is not None:
    rates = {k: fpr_with_looks(z_daily, k) for k in (1, 2, 5, 10, 28)}
    for k, r in rates.items():
        print(f"   {k:>2} looks -> false positive rate {r:.3f}")
    check("Part 1a one look = 5%", rates[1], 0.05, 0.006)
    check("Part 1b peeking daily for 4 weeks", rates[28], 0.28, 0.02)
    # Q-A (answers.md): a team checks the dashboard daily and ships the first time it's
    # green. Over 40 A/A-like tests (features that do nothing), about how many "wins"?

    # -----------------------------------------------------------------------
    # Part 2: a naive fix, Bonferroni across the 28 looks
    # -----------------------------------------------------------------------
    crit = None  # TODO: stats.norm.ppf(1 - 0.05 / 2 / 28)  (two-sided, split over 28 looks)
    if crit is not None:
        fpr_bonf = (np.abs(z_daily) > crit).any(axis=1).mean()
        print(f"   Bonferroni over 28 looks: critical |z| = {crit:.2f}, FPR = {fpr_bonf:.3f}")
        print(f"[{'PASS' if fpr_bonf < 0.05 else 'FAIL'}] Part 2 Bonferroni controls FPR (but is too strict)")
        # Q-B (answers.md): why is FPR well BELOW 5% here? (Hint: are the 28 looks independent?)
        # What does that over-strictness cost you? (Preview of Day 19: alpha spending.)

    # -----------------------------------------------------------------------
    # Part 3: the winner's curse: peeking also exaggerates the effect you report
    # -----------------------------------------------------------------------
    true_effect = 0.2268          # small true effect (final-day power about 22%)
    inc = rng.normal(true_effect, 1, (SIMS, DAYS))
    z_eff = inc.cumsum(axis=1) / np.sqrt(np.arange(1, DAYS + 1))
    running_estimate = inc.cumsum(axis=1) / np.arange(1, DAYS + 1)
    significant = np.abs(z_eff) > 1.96
    stopped = significant.any(axis=1)
    first_day = significant.argmax(axis=1)
    est_at_stop = None  # TODO: running_estimate at first_day, for the simulations that stopped
    if est_at_stop is not None:
        exaggeration = est_at_stop.mean() / true_effect
        print(f"   reported effect when stopping early = {exaggeration:.1f}x the true effect")
        check("Part 3 winner's curse exaggeration", exaggeration, 3.1, 0.4)
        # Q-C (answers.md): leadership plans revenue based on 'stopped-early' wins.
        # What happens to the forecast, and how would a pre-registered duration help?
