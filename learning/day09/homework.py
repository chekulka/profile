"""Day 9 homework: metric design: sensitivity, capping, and choosing a proxy metric.

Run:  python learning/day09/homework.py
Fill in every TODO. Parts with unfinished TODOs are skipped.
"""
import numpy as np
from scipy import stats

rng = np.random.default_rng(9)
print("Day 9 homework")


def check(name, got, expected, tol):
    ok = got is not None and abs(float(got) - float(expected)) <= tol
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: got {got}, expected ~{expected}")
    return ok


# ---------------------------------------------------------------------------
# Scenario: a checkout change makes 8% MORE users buy (4.00% -> 4.32%).
# Order values are heavy-tailed (a few whales). Which metric detects this best?
# ---------------------------------------------------------------------------
def draw(n, lift):
    buy = rng.random(n) < 0.04 * (1 + lift)
    revenue = np.where(buy, rng.lognormal(4, 1.6, n), 0.0)
    return buy.astype(float), revenue


def cap(x, threshold):
    return None  # TODO: winsorize x at threshold (np.minimum)


def power_of(metric, sims=300, n=50_000):
    """Share of simulated A/B tests (true lift 8%) where the metric is significant."""
    rejections = 0
    for _ in range(sims):
        buy_c, rev_c = draw(n, 0.0)
        buy_t, rev_t = draw(n, 0.08)
        a, b = metric(buy_c, rev_c, buy_t, rev_t)
        if a is None:
            return None
        p = None  # TODO: Welch t-test p-value comparing b vs a
        if p is None:
            return None
        rejections += p < 0.05
    return rejections / sims


def conversion(bc, rc, bt, rt):
    return bc, bt


def revenue(bc, rc, bt, rt):
    return rc, rt


def revenue_capped_p90(bc, rc, bt, rt):
    buyers = np.r_[rc, rt]
    t = np.percentile(buyers[buyers > 0], 90)  # cap at the 90th percentile of order value
    a, b = cap(rc, t), cap(rt, t)
    return (None, None) if a is None else (a, b)


# ---------------------------------------------------------------------------
# Part 1: metric sensitivity: same behavior change, three metrics
# ---------------------------------------------------------------------------
pw = {name: power_of(fn) for name, fn in
      [("conversion", conversion), ("revenue", revenue), ("revenue capped p90", revenue_capped_p90)]}
if None not in pw.values():
    for k, v in pw.items():
        print(f"   power of {k:<20} {v:.2f}")
    check("Part 1a conversion power", pw["conversion"], 0.72, 0.08)
    check("Part 1b raw revenue power", pw["revenue"], 0.14, 0.07)
    print(f"[{'PASS' if pw['revenue capped p90'] > pw['revenue'] + 0.1 else 'FAIL'}] "
          "Part 1c capping makes revenue clearly more sensitive")
    # Q-A (answers.md): the business cares about REVENUE, yet conversion is 5x more
    # sensitive. How would you set up the OEC, primary and guardrail metrics for this
    # test? What does capping at p90 change about what you're measuring?

# ---------------------------------------------------------------------------
# Part 2: choosing a proxy metric from past experiments
# ---------------------------------------------------------------------------
# 40 past experiments. For each: the 1-week effect on two candidate proxy metrics
# (A = "7-day active days", B = "7-day clicks"), and the 6-month retention effect
# that leadership actually cares about (the north star). Effects are in z-units.
K = 40
north_star = rng.normal(0, 1, K)
proxy_A = 0.8 * north_star + rng.normal(0, 0.6, K)
proxy_B = 0.2 * north_star + rng.normal(0, 1.0, K)

corr_A = None  # TODO: correlation of proxy_A with north_star across experiments
corr_B = None  # TODO: same for proxy_B
if corr_A is not None and corr_B is not None:
    print(f"   corr with 6-month retention: A={corr_A:.2f}  B={corr_B:.2f}")
    sign_agree_A = None  # TODO: share of experiments where sign(proxy_A) == sign(north_star)
    sign_agree_B = np.mean(np.sign(proxy_B) == np.sign(north_star))
    if sign_agree_A is not None:
        print(f"   directional agreement: A={sign_agree_A:.0%}  B={sign_agree_B:.0%}")
        best = None  # TODO: "A" or "B", whichever proxy you'd adopt (decide from the numbers)
        print(f"[{'PASS' if best == 'A' and corr_A > corr_B else 'FAIL'}] Part 2 chose proxy {best}")
        # Q-B (answers.md): proxy B (clicks) is what the product team already
        # optimizes. Using sign agreement, how often would B have pointed them the
        # WRONG way on retention? How would you convince them to switch?
