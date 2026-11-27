"""Day 20 homework: always-valid inference: mSPRT and confidence sequences.

Run:  python learning/day20/homework.py
Fill in every TODO. Parts with unfinished TODOs are skipped.
"""
import numpy as np

rng = np.random.default_rng(20)
print("Day 20 homework")

# Each step adds one treatment/control PAIR; X_i = (treatment - control) ~ N(delta, v).
SIMS, N = 4000, 2000          # monitor after EVERY pair, up to 2,000 pairs
V = 2.0                       # variance of each paired difference (sigma = 1 per arm)
TAU2 = 0.01                   # mixing variance: the prior "guess" of effect size (tau = 0.1)
ALPHA = 0.05
n = np.arange(1, N + 1)


def check(name, got, expected, tol):
    ok = got is not None and abs(float(got) - float(expected)) <= tol
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: got {got}, expected ~{expected}")
    return ok


# ---------------------------------------------------------------------------
# Part 1: the mSPRT statistic (mixture sequential probability ratio test)
# ---------------------------------------------------------------------------
# With S_n = sum of the first n differences, the mixture likelihood ratio is
#   Lambda_n = sqrt(V / (V + n*TAU2)) * exp( TAU2 * S_n^2 / (2 * V * (V + n*TAU2)) )
# Reject H0 the first time Lambda_n >= 1/ALPHA. Valid at ANY stopping time.
def log_lambda(S):
    return None  # TODO: 0.5*np.log(V / (V + n*TAU2)) + TAU2 * S**2 / (2*V*(V + n*TAU2))


S_null = rng.normal(0, np.sqrt(V), (SIMS, N)).cumsum(axis=1)
if log_lambda(S_null) is not None:
    fpr_msprt = (log_lambda(S_null) >= np.log(1 / ALPHA)).any(axis=1).mean()
    z = S_null / np.sqrt(n * V)
    fpr_naive = (np.abs(z) > 1.96).any(axis=1).mean()
    print(f"   A/A with a look after EVERY pair: naive z-test FPR {fpr_naive:.2f} | mSPRT FPR {fpr_msprt:.3f}")
    print(f"[{'PASS' if fpr_msprt <= ALPHA and fpr_naive > 0.4 else 'FAIL'}] "
          "Part 1 mSPRT stays below 5% under continuous peeking; the naive test explodes")

    # -----------------------------------------------------------------------
    # Part 2: confidence sequences: a CI that is valid at all times simultaneously
    # -----------------------------------------------------------------------
    # Inverting the mSPRT gives: |mean_n - delta| < half_width_n, with
    #   half_width_n = sqrt( V*(V + n*TAU2) / (n^2 * TAU2) * (2*log(1/ALPHA) + log((V + n*TAU2)/V)) )
    half_width = None  # TODO: implement the formula above (a vector over n)
    if half_width is not None:
        mean = S_null / n                      # true delta = 0
        cs_cover = (np.abs(mean) < half_width).all(axis=1).mean()
        ci_cover = (np.abs(mean) < 1.96 * np.sqrt(V / n)).all(axis=1).mean()
        ratio = half_width[-1] / (1.96 * np.sqrt(V / N))
        print(f"   covers the truth at EVERY n: confidence sequence {cs_cover:.3f} | naive 95% CI {ci_cover:.2f}")
        print(f"   price: at n = {N}, the confidence sequence is {ratio:.2f}x wider than the fixed CI")
        print(f"[{'PASS' if cs_cover >= 0.95 and ci_cover < 0.6 else 'FAIL'}] "
              "Part 2 uniform coverage holds for the confidence sequence only")
        check("Part 2 width penalty at the end", ratio, 1.55, 0.05)

    # -----------------------------------------------------------------------
    # Part 3: power and stopping time under a real effect
    # -----------------------------------------------------------------------
    delta = 0.08
    S_alt = rng.normal(delta, np.sqrt(V), (SIMS, N)).cumsum(axis=1)
    hit = log_lambda(S_alt) >= np.log(1 / ALPHA)
    power_msprt = hit.any(axis=1).mean()
    stop_time = np.where(hit.any(axis=1), hit.argmax(axis=1) + 1, N)
    power_fixed = None  # TODO: share of sims with |S_alt[:, -1] / sqrt(N*V)| > 1.96 (one look at the end)
    if power_fixed is not None:
        print(f"   power: fixed-n (one look at n={N}) {power_fixed:.2f} | mSPRT (any time, up to n={N}) {power_msprt:.2f}")
        print(f"   mSPRT average stopping point: {stop_time.mean():.0f} pairs")
        print(f"[{'PASS' if power_msprt < power_fixed else 'FAIL'}] "
              "Part 3 always-valid flexibility costs some power at the same max n")
        # Q-A (answers.md): when is that cost worth paying? (Hint: real-time ops
        # dashboards, guardrail monitoring, teams that can't resist peeking.) How does the
        # choice of TAU2 affect power? Try TAU2 = 0.0064 (tau = 0.08) and TAU2 = 0.1.
