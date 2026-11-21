"""Weekend project (Week 2): a trustworthy experiment analyzer.

One function, analyze(df), that runs the full checklist from Days 2-13 on a raw
user-level experiment table and prints a readout:
  1. SRM check (Day 6)                     -> stop if it fails
  2. Sessions per user with CUPED (Day 12)
  3. CTR = clicks/sessions with the delta method (Day 4)
  4. Revenue per user, capped (Day 9)
  5. Benjamini-Hochberg across the metrics (Day 11)
  6. A one-line TL;DR with a decision (Day 5)

Run:  python learning/day14/homework.py
Fill in every TODO. Parts with unfinished TODOs are skipped.
"""
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests

rng = np.random.default_rng(14)
print("Weekend project: experiment analyzer")


# ---------------------------------------------------------------------------
# Synthetic experiment. Truth: sessions +0.30/user, CTR +0.005, revenue: no effect.
# ---------------------------------------------------------------------------
def make_experiment(n=40_000, srm_bug=False):
    arm = rng.integers(0, 2, n)
    pre_sessions = rng.gamma(4, 2.5, n)                         # last month, per user
    sessions = np.maximum(1, np.round(0.8 * pre_sessions + rng.normal(2, 3, n) + 0.30 * arm)).astype(int)
    ctr_user = np.clip(rng.beta(2, 8, n) + 0.005 * arm, 0, 1)
    clicks = rng.binomial(sessions, ctr_user)
    buys = rng.random(n) < 0.05
    revenue = np.where(buys, rng.lognormal(3.5, 1.4, n), 0.0)
    df = pd.DataFrame(dict(arm=arm, pre_sessions=pre_sessions, sessions=sessions,
                           clicks=clicks, revenue=revenue))
    if srm_bug:   # treatment drops 6% of its users from the logs
        df = df[~((df.arm == 1) & (rng.random(len(df)) < 0.06))]
    return df


# ---------------------------------------------------------------------------
# Building blocks: fill these in (each is a few lines; reuse your earlier days)
# ---------------------------------------------------------------------------
def srm_p(df):
    counts = df["arm"].value_counts().sort_index().values
    return None  # TODO: chi-square p-value vs a 50/50 split (stats.chisquare)


def welch(a, b):
    """Return (effect, se, p) for mean(b) - mean(a)."""
    d = b.mean() - a.mean()
    se = np.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))
    return d, se, 2 * stats.norm.sf(abs(d / se))


def cuped_sessions(df):
    """Sessions effect after CUPED with pre_sessions (theta pooled over both arms)."""
    y, x = df["sessions"].values, df["pre_sessions"].values
    theta = None  # TODO: cov(y, x) / var(x)
    if theta is None:
        return None
    y_adj = y - theta * (x - x.mean())
    t = df["arm"].values
    return welch(y_adj[t == 0], y_adj[t == 1])


def ctr_delta(df):
    """CTR (ratio of totals) per arm with the delta method; return (effect, se, p)."""
    out = []
    for a in (0, 1):
        g = df[df.arm == a]
        s, c = g["sessions"].values, g["clicks"].values
        n, mx = len(s), s.mean()
        R = c.mean() / mx
        var = None  # TODO: (var(c) - 2R cov(c,s) + R^2 var(s)) / (n mx^2)   [Day 4]
        if var is None:
            return None
        out.append((R, var))
    (r0, v0), (r1, v1) = out
    d, se = r1 - r0, np.sqrt(v0 + v1)
    return d, se, 2 * stats.norm.sf(abs(d / se))


def revenue_capped(df, q=99):
    cap = np.percentile(df.loc[df.revenue > 0, "revenue"], q)
    r = np.minimum(df["revenue"].values, cap)
    t = df["arm"].values
    return welch(r[t == 0], r[t == 1])


# ---------------------------------------------------------------------------
# The analyzer
# ---------------------------------------------------------------------------
def analyze(df, alpha_srm=0.001):
    p_srm = srm_p(df)
    if p_srm is None:
        return None
    if p_srm < alpha_srm:
        print(f"   ⛔ SRM detected (p={p_srm:.1e}). Results withheld: debug assignment and logging first.")
        return {"decision": "STOP", "srm_p": p_srm}

    results = {"sessions (CUPED)": cuped_sessions(df), "CTR (delta)": ctr_delta(df),
               "revenue (capped p99)": revenue_capped(df)}
    if any(v is None for v in results.values()):
        return None
    names = list(results)
    raw_p = np.array([results[k][2] for k in names])
    adj_p = None  # TODO: Benjamini-Hochberg adjusted p-values: multipletests(raw_p, method="fdr_bh")[1]
    if adj_p is None:
        return None

    print(f"   SRM p = {p_srm:.3f} ✅")
    print(f"   {'metric':<22}{'effect':>10}{'95% CI':>24}{'BH p':>9}")
    for k, pa in zip(names, adj_p):
        d, se, _ = results[k]
        print(f"   {k:<22}{d:>10.4f}   [{d - 1.96*se:>8.4f}, {d + 1.96*se:>8.4f}]{pa:>9.3f}")
    primary_d, _, _ = results["sessions (CUPED)"]
    primary_sig = adj_p[0] < 0.05
    decision = "SHIP" if primary_sig and primary_d > 0 else "DON'T SHIP"
    print(f"   TL;DR: {decision}: sessions/user {primary_d:+.2f} (BH p={adj_p[0]:.3g}); "
          f"CTR {results['CTR (delta)'][0]:+.4f}; revenue unchanged within CI.")
    return {"decision": decision, "srm_p": p_srm, "results": results, "adj_p": adj_p}


# ---------------------------------------------------------------------------
# Run it on a clean experiment and on one with an SRM bug
# ---------------------------------------------------------------------------
print("\n[Clean experiment]")
clean = analyze(make_experiment())
if clean is not None:
    def covers(res, truth):
        d, se, _ = res
        return d - 1.96 * se <= truth <= d + 1.96 * se
    r = clean["results"]
    ok = (clean["decision"] == "SHIP" and covers(r["sessions (CUPED)"], 0.30)
          and covers(r["revenue (capped p99)"], 0.0))
    print(f"[{'PASS' if ok else 'FAIL'}] clean experiment: CIs cover the true effects and decision = SHIP")
    # Q-B (answers.md): the true CTR shift is about +0.005, yet the estimate is about
    # +0.009 and its 95% CI just misses 0.005. Is the analyzer broken? (Hint: how many
    # SEs away is it, and with several metrics, how often will one CI miss by chance?
    # How would you check with the A/A and A/B simulations from Days 3 and 7?)

    print("\n[Experiment with a logging bug]")
    bugged = analyze(make_experiment(srm_bug=True))
    print(f"[{'PASS' if bugged['decision'] == 'STOP' else 'FAIL'}] the analyzer refuses to report when SRM fails")

# ---------------------------------------------------------------------------
# Stretch goals (portfolio)
# ---------------------------------------------------------------------------
# 1. Move this into its own GitHub repo: `experiment-analyzer/` with a README,
#    a requirements.txt and a test that runs the two scenarios above.
# 2. Add Lin-style regression adjustment (Day 13) as an option next to CUPED.
# 3. Add an A/A mode (Day 7): run analyze() on 500 A/A datasets and report the
#    false positive rate per metric.
# Q-A (answers.md): paste your clean-experiment readout and explain, in 3 sentences,
#    why each step comes in that order (why SRM first, why BH last).
