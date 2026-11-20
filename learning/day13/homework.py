"""Day 13 homework: regression adjustment done right (Lin 2013) and the bad-control trap.

Run:  python learning/day13/homework.py
Fill in every TODO. Parts with unfinished TODOs are skipped.
"""
import numpy as np
import statsmodels.api as sm

rng = np.random.default_rng(13)
print("Day 13 homework")


def ate(y, design):
    """OLS coefficient on the FIRST column of `design` (the treatment), with HC2 SEs."""
    fit = sm.OLS(y, sm.add_constant(design)).fit(cov_type="HC2")
    return fit.params[1], fit.bse[1]


# ---------------------------------------------------------------------------
# Part 1: Freedman's critique and Lin's fix
# ---------------------------------------------------------------------------
# 80/20 split, and the covariate x matters very differently in each arm
# (heterogeneous effects): control outcome = 3x + noise, treated = 1 + 0x + noise.
# The true average treatment effect is 1.
def one_experiment(n=500):
    x = rng.normal(0, 1, n)
    t = (rng.random(n) < 0.2).astype(float)
    y = np.where(t == 1, 1 + 0 * x, 3 * x) + rng.normal(0, 1, n)
    xc = x - x.mean()                       # center the covariate!
    unadjusted = np.column_stack([t])
    ancova = np.column_stack([t, xc])       # one common slope
    lin = None  # TODO: np.column_stack([t, xc, t * xc])  (a separate slope per arm)
    return y, unadjusted, ancova, lin


est = {"unadjusted": [], "ancova": [], "lin": []}
for _ in range(1000):
    y, d_u, d_a, d_l = one_experiment()
    if d_l is None:
        est = None
        break
    est["unadjusted"].append(ate(y, d_u)[0])
    est["ancova"].append(ate(y, d_a)[0])
    est["lin"].append(ate(y, d_l)[0])

if est is not None:
    sd = {k: np.std(v) for k, v in est.items()}
    mean = {k: np.mean(v) for k, v in est.items()}
    for k in est:
        print(f"   {k:<11} mean {mean[k]:.3f}  sd of estimate {sd[k]:.3f}")
    ok1 = all(abs(m - 1) < 0.03 for m in mean.values())
    ok2 = sd["ancova"] > 1.2 * sd["unadjusted"]
    ok3 = sd["lin"] <= sd["unadjusted"] + 0.005
    print(f"[{'PASS' if ok1 else 'FAIL'}] Part 1a all three are unbiased for the ATE of 1")
    print(f"[{'PASS' if ok2 else 'FAIL'}] Part 1b ANCOVA (no interaction) is NOISIER than doing nothing here")
    print(f"[{'PASS' if ok3 else 'FAIL'}] Part 1c Lin's estimator is never worse than unadjusted")
    # Q-A (answers.md): why does a common slope hurt when the split is 80/20 AND the
    # slopes differ by arm? Why must x be centered for the T coefficient to be the ATE?

# ---------------------------------------------------------------------------
# Part 2: the bad-control trap (adjusting for a post-treatment variable)
# ---------------------------------------------------------------------------
# Treatment raises sessions (+2), and each session earns $3. True effect on revenue: +$6.
n = 50_000
t = rng.integers(0, 2, n).astype(float)
sessions = rng.poisson(5 + 2 * t)                 # measured DURING the experiment
revenue = 3 * sessions + rng.normal(0, 5, n)

effect_right = None  # TODO: ate(revenue, np.column_stack([t]))[0]
effect_bad = None    # TODO: ate(revenue, np.column_stack([t, sessions]))[0]
if effect_right is not None and effect_bad is not None:
    print(f"   revenue effect: unadjusted {effect_right:+.2f} | 'controlling' for sessions {effect_bad:+.2f}")
    print(f"[{'PASS' if abs(effect_right - 6) < 0.3 and abs(effect_bad) < 0.3 else 'FAIL'}] "
          "Part 2 adjusting for a mediator erases a real $6 effect")
    # Q-B (answers.md): name two variables you must NEVER adjust for in an
    # experiment readout, and one you safely can.

# ---------------------------------------------------------------------------
# Part 3: adding useless (but pre-treatment) covariates costs almost nothing
# ---------------------------------------------------------------------------
n = 5000
t = rng.integers(0, 2, n).astype(float)
x_good = rng.normal(0, 1, n)
junk = rng.normal(0, 1, (n, 20))                   # 20 irrelevant pre-period features
y = 0.2 * t + 2 * x_good + rng.normal(0, 1, n)

se_good = ate(y, np.column_stack([t, x_good]))[1]
se_junk = None  # TODO: SE when you include t, x_good AND all 20 junk columns
if se_junk is not None:
    print(f"   SE with the good covariate {se_good:.4f} | plus 20 junk covariates {se_junk:.4f}")
    print(f"[{'PASS' if se_junk / se_good < 1.02 else 'FAIL'}] Part 3 junk covariates barely matter at this n")
