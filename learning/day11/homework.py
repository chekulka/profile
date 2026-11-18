"""Day 11 homework: multiple testing: many metrics, many segments, few true wins.

Run:  python learning/day11/homework.py
Fill in every TODO. Parts with unfinished TODOs are skipped.
"""
import numpy as np
from scipy import stats
from statsmodels.stats.multitest import multipletests

rng = np.random.default_rng(11)
print("Day 11 homework")


def check(name, got, expected, tol):
    ok = got is not None and abs(float(got) - float(expected)) <= tol
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: got {got}, expected ~{expected}")
    return ok


# ---------------------------------------------------------------------------
# Part 1: why "one of my 20 metrics is significant" means little
# ---------------------------------------------------------------------------
z = rng.normal(size=(2000, 20))            # 2,000 A/A experiments x 20 independent metrics
p = 2 * stats.norm.sf(np.abs(z))
share_any = None  # TODO: share of experiments where AT LEAST ONE of the 20 p-values < 0.05
formula = None    # TODO: 1 - 0.95**20
if share_any is not None and formula is not None:
    check("Part 1 P(>=1 false win among 20 metrics)", share_any, formula, 0.03)


# ---------------------------------------------------------------------------
# Part 2: implement Bonferroni and Benjamini-Hochberg yourself
# ---------------------------------------------------------------------------
def bonferroni(pvals, alpha=0.05):
    return None  # TODO: boolean array, reject where p < alpha / m


def benjamini_hochberg(pvals, alpha=0.05):
    """Step-up: sort p-values, find the largest k with p_(k) <= (k/m)*alpha, reject the k smallest."""
    m = len(pvals)
    order = np.argsort(pvals)
    thresholds = None  # TODO: (np.arange(1, m + 1) / m) * alpha
    if thresholds is None:
        return None
    below = pvals[order] <= thresholds
    reject = np.zeros(m, bool)
    if below.any():
        k = np.max(np.where(below)[0])   # last index passing
        reject[order[: k + 1]] = True
    return reject


test_p = rng.uniform(size=50) ** 2  # some arbitrary p-values
if bonferroni(test_p) is not None and benjamini_hochberg(test_p) is not None:
    same_b = np.array_equal(bonferroni(test_p), multipletests(test_p, 0.05, "bonferroni")[0])
    same_bh = np.array_equal(benjamini_hochberg(test_p), multipletests(test_p, 0.05, "fdr_bh")[0])
    print(f"[{'PASS' if same_b and same_bh else 'FAIL'}] Part 2 your Bonferroni and BH match statsmodels")

    # -----------------------------------------------------------------------
    # Part 3: FWER vs FDR vs power: 100 metrics/segments, 10 have real effects
    # -----------------------------------------------------------------------
    m, k_true = 100, 10
    out = {"none": [], "bonferroni": [], "bh": []}
    for _ in range(1000):
        mu = np.zeros(m)
        mu[:k_true] = 3.0
        pv = 2 * stats.norm.sf(np.abs(mu + rng.normal(size=m)))
        for name, rej in [("none", pv < 0.05), ("bonferroni", bonferroni(pv)), ("bh", benjamini_hochberg(pv))]:
            false_rej, true_rej, total = rej[k_true:].sum(), rej[:k_true].sum(), rej.sum()
            out[name].append((false_rej > 0, false_rej / max(total, 1), true_rej / k_true))
    summary = {n: np.array(v, float).mean(axis=0) for n, v in out.items()}
    print("   method       FWER    FDR    power")
    for n, (fwer, fdr, pw) in summary.items():
        print(f"   {n:<11} {fwer:6.3f} {fdr:6.3f} {pw:7.3f}")
    check("Part 3a no correction: FDR is about 33%", summary["none"][1], 0.33, 0.04)
    check("Part 3b Bonferroni controls FWER at about 5%", summary["bonferroni"][0], 0.05, 0.02)
    check("Part 3c BH controls FDR below 5%", summary["bh"][1], 0.045, 0.015)
    print(f"[{'PASS' if summary['bh'][2] > summary['bonferroni'][2] + 0.1 else 'FAIL'}] "
          "Part 3d BH finds more true effects than Bonferroni")
    # Q-A (answers.md): for each case, which would you use and why?
    #   (1) the single primary metric that decides a launch
    #   (2) 4 guardrail metrics
    #   (3) a dashboard of 80 exploratory metrics x segments
