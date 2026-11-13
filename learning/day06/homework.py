"""Day 6 homework: sample ratio mismatch (SRM): detect it, find it, see why it matters.

Run:  python learning/day06/homework.py
Fill in every TODO. Parts with unfinished TODOs are skipped.
"""
import numpy as np
import pandas as pd
from scipy import stats

print("Day 6 homework")
ALPHA_SRM = 0.001  # common SRM alarm threshold (strict, because SRM checks run constantly)


def check(name, got, expected, tol):
    ok = got is not None and abs(float(got) - float(expected)) <= tol
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: got {got}, expected ~{expected}")
    return ok


# ---------------------------------------------------------------------------
# Part 1: the SRM test (chi-square goodness of fit)
# ---------------------------------------------------------------------------
def srm_pvalue(counts, expected_ratios):
    """counts: observed users per arm; expected_ratios: planned split (sums to 1)."""
    counts = np.asarray(counts, dtype=float)
    expected = None  # TODO: total * ratios
    if expected is None:
        return None
    return None  # TODO: stats.chisquare(counts, f_exp=expected).pvalue


if srm_pvalue([1, 1], [0.5, 0.5]) is not None:
    check("Part 1a Day 5 scenario (100,480 vs 99,520)", srm_pvalue([100_480, 99_520], [.5, .5]), 0.0318, 5e-4)
    check("Part 1b 3-arm 50/25/25 split, healthy", srm_pvalue([50_210, 24_950, 24_840], [.5, .25, .25]), 0.367, 0.01)

# ---------------------------------------------------------------------------
# Simulation: a NO-EFFECT test with a logging bug
# ---------------------------------------------------------------------------
# The treatment crashes the Android app for low-intent users before the exposure
# event is logged, so those users silently disappear from the treatment arm.
rng = np.random.default_rng(6)
n = 200_000
users = pd.DataFrame({
    "arm": rng.integers(0, 2, n),
    "platform": rng.choice(["ios", "android", "web"], n, p=[0.40, 0.35, 0.25]),
    "intent": rng.random(n),
})
users["converted"] = (rng.random(n) < 0.05 + 0.20 * users["intent"]).astype(int)  # TRUE EFFECT = 0
lost = (users["arm"] == 1) & (users["platform"] == "android") & (users["intent"] < 0.3)
logged = users[~lost]


def effect(df):
    m = df.groupby("arm")["converted"].agg(["mean", "count"])
    d = m.loc[1, "mean"] - m.loc[0, "mean"]
    se = np.sqrt((m["mean"] * (1 - m["mean"]) / m["count"]).sum())
    return d, d / se


d_all, z_all = effect(logged)
print(f"   naive readout: conversion lift {d_all*100:+.2f} pp, z = {z_all:.2f}  <- looks like a win!")

if srm_pvalue([1, 1], [0.5, 0.5]) is not None:
    # -----------------------------------------------------------------------
    # Part 2: run the SRM check on the logged data
    # -----------------------------------------------------------------------
    counts = logged["arm"].value_counts().sort_index().values
    p_overall = srm_pvalue(counts, [0.5, 0.5])
    print(f"   arm counts {counts}, SRM p = {p_overall:.1e}")
    print(f"[{'PASS' if p_overall < ALPHA_SRM else 'FAIL'}] Part 2 SRM detected")

    # -----------------------------------------------------------------------
    # Part 3: segment the SRM check to find the cause
    # -----------------------------------------------------------------------
    seg_p = {}
    for platform, g in logged.groupby("platform"):
        seg_p[platform] = None  # TODO: srm_pvalue of this segment's arm counts vs [0.5, 0.5]
    if None not in seg_p.values():
        print("   segment SRM p-values:", {k: f"{v:.1e}" for k, v in seg_p.items()})
        culprit = None  # TODO: the platform whose SRM p-value is below ALPHA_SRM
        print(f"[{'PASS' if culprit == 'android' else 'FAIL'}] Part 3 culprit segment: {culprit}")
        # Q-A (answers.md): web has p of about 0.05. Is web broken too? Why do we use
        # 0.001, not 0.05, when scanning many segments?

        # -------------------------------------------------------------------
        # Part 4: what the bias did, and an analysis on the unaffected segments
        # -------------------------------------------------------------------
        clean = None  # TODO: logged rows whose platform is NOT the culprit
        if clean is not None:
            d_clean, z_clean = effect(clean)
            print(f"   unaffected segments: lift {d_clean*100:+.2f} pp, z = {z_clean:.2f}")
            print(f"[{'PASS' if abs(z_clean) < 1.96 and z_all > 1.96 else 'FAIL'}] "
                  "Part 4 the 'win' disappears where there is no SRM")
            # Q-B (answers.md): explain in 3 sentences WHY losing low-intent Android
            # users created a fake positive lift. Why can't you just reweight it away?

# ---------------------------------------------------------------------------
# Part 5: how sensitive is the SRM test?
# ---------------------------------------------------------------------------
# N = 1,000,000 users, planned 50/50. Counts are N/2 + k and N/2 - k.
# The chi-square statistic is 4k^2/N. What is the smallest k that triggers p < 0.001?
crit = stats.chi2.ppf(1 - ALPHA_SRM, df=1)  # about 10.83
k_min = None  # TODO: solve 4k^2/N = crit for k
if k_min is not None:
    check("Part 5 smallest detectable shortfall k (users per arm)", k_min, 1645, 5)
    print(f"   that's a split of {0.5 - k_min/1e6:.4%} vs {0.5 + k_min/1e6:.4%}: tiny, but real")
