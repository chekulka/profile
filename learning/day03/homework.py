"""Day 3 homework: power and MDE, analytical vs. simulation.

Run:  python learning/day03/homework.py
Fill in every TODO. Parts with unfinished TODOs are skipped.
"""
import warnings

import numpy as np
from scipy import stats
import diff_diff as dd

warnings.filterwarnings("ignore")
rng = np.random.default_rng(3)
Z = stats.norm.ppf(0.975) + stats.norm.ppf(0.80)  # about 2.80


def check(name, got, expected, tol):
    ok = got is not None and abs(float(got) - float(expected)) <= tol
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: got {got}, expected ~{expected:.4f}")
    return ok


print("Day 3 homework")

# ---------------------------------------------------------------------------
# Part 1: MDE by formula
# ---------------------------------------------------------------------------
def mde(sigma, n_t, n_c, alpha=0.05, power=0.80):
    return None  # TODO: (z_{1-alpha/2} + z_{power}) * sigma * sqrt(1/n_t + 1/n_c)


if mde(1, 1, 1) is not None:
    check("Part 1 MDE, sigma=20, 10k per arm", mde(20, 10_000, 10_000), 0.7924, 1e-3)

# ---------------------------------------------------------------------------
# Part 2: sample size for a conversion test
# ---------------------------------------------------------------------------
def n_per_arm_conversion(p, abs_lift, alpha=0.05, power=0.80):
    return None  # TODO: 2 * (z sum)^2 * p(1-p) / abs_lift^2   (use stats.norm.ppf)


n_conv = n_per_arm_conversion(0.10, 0.002)
if n_conv is not None:
    check("Part 2 users per arm, p=10%, +0.2pp", n_conv, 353_200, 500)
    print(f"   Lehr rule 16*sigma^2/delta^2 = {16 * 0.09 / 0.002**2:,.0f}")
    # Q-A (answers.md): the PM wants to detect a 1% RELATIVE lift instead (0.1pp).
    # How many users per arm, and roughly how much longer will the test run?

# ---------------------------------------------------------------------------
# Part 3: simulate power and compare with the formula
# ---------------------------------------------------------------------------
def simulated_power(effect, sigma, n, n_sims=2000):
    rejections = 0
    for _ in range(n_sims):
        a = rng.normal(0, sigma, n)
        b = rng.normal(effect, sigma, n)
        p = None  # TODO: Welch t-test p-value comparing b and a
        if p is None:
            return None
        rejections += p < 0.05
    return rejections / n_sims


if mde(1, 1, 1) is not None:
    eff = mde(1.0, 200, 200)  # the 80%-power effect for n=200 per arm
    sp = simulated_power(eff, 1.0, 200)
    if sp is not None:
        check("Part 3 simulated power at the MDE is about 80%", sp, 0.80, 0.03)
        sp_half = simulated_power(eff / 2, 1.0, 200)
        print(f"   power at HALF the MDE: {sp_half:.3f}  <- Q-B: why not 40%?")

# ---------------------------------------------------------------------------
# Part 4: allocation matters
# ---------------------------------------------------------------------------
# Same total N = 20,000. Compare a 50/50 split with a 90/10 split.
ratio = None  # TODO: mde(1, 2_000, 18_000) / mde(1, 10_000, 10_000)
if ratio is not None:
    check("Part 4 MDE inflation for a 90/10 split", ratio, 1.6667, 1e-3)
    # Q-C (answers.md): when would you still choose a 90/10 split?

# ---------------------------------------------------------------------------
# Part 5: diff-diff analytical power for DiD designs
# ---------------------------------------------------------------------------
mde_2x2 = None    # TODO: dd.compute_mde(n_treated=50, n_control=50, sigma=1.0)
mde_panel = None  # TODO: same, but with n_pre=4, n_post=4, rho=0.5
if mde_2x2 is not None and mde_panel is not None and mde(1, 1, 1) is not None:
    check("Part 5a 2x2 DiD MDE is sqrt(2) times the A/B MDE",
          mde_2x2 / mde(1.0, 50, 50), np.sqrt(2), 1e-3)
    check("Part 5b panel MDE (4 pre, 4 post, rho=0.5)", mde_panel, 0.2802, 1e-3)

# ---------------------------------------------------------------------------
# Part 6: simulation catches wrong standard errors
# ---------------------------------------------------------------------------
# Panel data: 100 units, 4 periods, true effect 0.5, with persistent unit effects.
kw = dict(n_units=100, n_periods=4, treatment_effect=0.5, sigma=1.0,
          n_simulations=300, seed=1, progress=False)
naive = dd.simulate_power(dd.DifferenceInDifferences(), **kw)
print(f"   no clustering: power={naive.power:.3f}, mean SE={naive.mean_se:.3f}, "
      f"true sd of estimate={naive.std_estimate:.3f}, CI coverage={naive.coverage:.2f}")

clustered = None  # TODO: dd.simulate_power with DifferenceInDifferences(cluster="unit")
if clustered is not None:
    print(f"   cluster=unit:  power={clustered.power:.3f}, mean SE={clustered.mean_se:.3f}")
    check("Part 6 clustered SE matches the estimator's true sd",
          clustered.mean_se, clustered.std_estimate, 0.03)
    check("Part 6 clustered power", clustered.power, 0.70, 0.06)
    # Q-D (answers.md): the unclustered model's SE is about 2.3x too BIG, so its
    # power is only ~3%. Why are its residuals so noisy? (Hint: what is in the error
    # term that the treated/post dummies don't absorb?) Why would the SE be too
    # SMALL instead if errors were positively correlated over time WITHIN units
    # after removing unit effects?
