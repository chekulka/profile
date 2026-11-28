"""Weekend project (Week 4): a sequential-testing simulator that compares stopping rules.

Methods compared on the same simulated data streams:
  fixed       : one look at the planned end                         (Day 3)
  naive_peek  : look every 100 pairs, stop at first |z| > 1.96       (Day 18)
  bonferroni  : 20 looks, each at alpha/20                           (Day 18)
  obf         : 4 looks with O'Brien-Fleming spending                (Day 19)
  pocock      : 4 looks with Pocock spending                         (Day 19)
  msprt       : always-valid, look after EVERY pair                  (Day 20)

Run:  python learning/day21/homework.py
Fill in every TODO. Parts with unfinished TODOs are skipped.
"""
import numpy as np
from scipy import stats

rng = np.random.default_rng(21)
print("Weekend project: sequential testing simulator")

N, V, ALPHA, TAU2 = 2000, 2.0, 0.05, 0.01
SIMS = 4000
n = np.arange(1, N + 1)


def z_path(S):
    return S / np.sqrt(n * V)


# ---------------------------------------------------------------------------
# Group sequential boundaries (from Day 19), computed once by simulation
# ---------------------------------------------------------------------------
LOOKS_GS = np.array([500, 1000, 1500, 2000]) - 1   # 0-based indices of the 4 planned looks


def gs_boundaries(spending, sims=200_000):
    t = (LOOKS_GS + 1) / N
    spent = spending(t)
    z = rng.normal(0, 1, (sims, len(t))).cumsum(axis=1) / np.sqrt(np.arange(1, len(t) + 1))
    alive, out = np.ones(sims, bool), []
    for k in range(len(t)):
        m = int(round((spent[k] - (spent[k - 1] if k else 0)) * sims))
        zk = np.abs(z[:, k])
        c = np.sort(zk[alive])[::-1][m - 1] if m > 0 else np.inf
        out.append(c)
        alive &= zk < c
    return np.array(out)


B_OBF = gs_boundaries(lambda t: 2 - 2 * stats.norm.cdf(stats.norm.ppf(1 - ALPHA / 2) / np.sqrt(t)))
B_POC = gs_boundaries(lambda t: ALPHA * np.log(1 + (np.e - 1) * t))


# ---------------------------------------------------------------------------
# Part 1: each method returns, per simulation, (rejected?, number of pairs used)
# ---------------------------------------------------------------------------
def run_looks(z, look_idx, bounds):
    """Generic: stop at the first planned look where |z| >= bound."""
    cross = np.abs(z[:, look_idx]) >= bounds
    rejected = cross.any(axis=1)
    used = np.where(rejected, look_idx[cross.argmax(axis=1)] + 1, N)
    return rejected, used


def fixed(S):
    return run_looks(z_path(S), np.array([N - 1]), np.array([1.96]))


def naive_peek(S):
    looks = np.arange(100, N + 1, 100) - 1
    return run_looks(z_path(S), looks, np.full(len(looks), 1.96))


def bonferroni(S):
    looks = np.arange(100, N + 1, 100) - 1
    crit = None  # TODO: stats.norm.ppf(1 - ALPHA / 2 / len(looks))
    if crit is None:
        return None
    return run_looks(z_path(S), looks, np.full(len(looks), crit))


def obf(S):
    return run_looks(z_path(S), LOOKS_GS, B_OBF)


def pocock(S):
    return None  # TODO: same as obf, but with the Pocock boundaries B_POC


def msprt(S):
    log_lam = 0.5 * np.log(V / (V + n * TAU2)) + TAU2 * S**2 / (2 * V * (V + n * TAU2))
    hit = None  # TODO: boolean array, log_lam >= log(1 / ALPHA)
    if hit is None:
        return None
    rejected = hit.any(axis=1)
    return rejected, np.where(rejected, hit.argmax(axis=1) + 1, N)


METHODS = {"fixed": fixed, "naive_peek": naive_peek, "bonferroni": bonferroni,
           "obf": obf, "pocock": pocock, "msprt": msprt}

# ---------------------------------------------------------------------------
# Part 2: the comparison table
# ---------------------------------------------------------------------------
S0 = rng.normal(0.0, np.sqrt(V), (SIMS, N)).cumsum(axis=1)     # no effect
S1 = rng.normal(0.08, np.sqrt(V), (SIMS, N)).cumsum(axis=1)    # real effect (about 71% fixed-n power)

table = {}
for name, fn in METHODS.items():
    r0, r1 = fn(S0), fn(S1)
    if r0 is None or r1 is None:
        table = None
        break
    table[name] = (r0[0].mean(), r1[0].mean(), r1[1].mean() / N)

if table is not None:
    print(f"   {'method':<11}{'FPR':>7}{'power':>8}{'avg sample':>12}")
    for k, (fpr, pw, es) in table.items():
        flag = "  ❌ invalid" if fpr > 0.06 else ""
        print(f"   {k:<11}{fpr:>7.3f}{pw:>8.2f}{es:>11.0%}{flag}")
    valid = [k for k, v in table.items() if v[0] <= 0.06]
    ok1 = set(valid) == {"fixed", "bonferroni", "obf", "pocock", "msprt"}
    ok2 = table["obf"][1] > table["pocock"][1] > table["msprt"][1]
    ok3 = table["obf"][2] < 0.95 and table["fixed"][2] == 1.0
    print(f"[{'PASS' if ok1 else 'FAIL'}] Part 2a only naive peeking breaks the 5% guarantee")
    print(f"[{'PASS' if ok2 else 'FAIL'}] Part 2b among the sequential methods, power ranks OBF > Pocock > mSPRT")
    print(f"[{'PASS' if ok3 else 'FAIL'}] Part 2c OBF saves sample on average; fixed always uses all of it")

# ---------------------------------------------------------------------------
# Part 3 (answers.md): your recommendation memo (half a page)
# ---------------------------------------------------------------------------
# Q-A: using YOUR table, write a recommendation for an experimentation platform:
#   default method for decision metrics, method for guardrails/real-time monitoring,
#   and what to tell teams who peek. Cite numbers from the table.
# Stretch: add a futility rule to OBF, or plot power vs. effect size for each method,
#   and publish the simulator in a GitHub repo next to your A/A harness and analyzer.
