"""Day 1 homework: potential outcomes and your first 2x2 difference-in-differences.

Run:  python learning/day01/homework.py
Fill in every TODO. Each `check_*` call tells you whether your answer is right.
"""
import numpy as np
import pandas as pd
import diff_diff as dd


def check(name, got, expected, tol=1e-6):
    ok = got is not None and abs(float(got) - float(expected)) < tol
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: got {got}, expected {expected}")
    return ok


# ---------------------------------------------------------------------------
# Part 1: potential outcomes on simulated data (we know the truth here)
# ---------------------------------------------------------------------------
panel = dd.generate_did_data(n_units=200, n_periods=4, treatment_effect=5.0, seed=42)
# Columns: unit, period, treated (group), post (time), outcome, true_effect
# Real launches are rarely random: here the treated markets start 3 units higher.
panel.loc[panel["treated"] == 1, "outcome"] += 3.0

# Q1. Compute the 2x2 DiD BY HAND using group means:
#     (treated_post - treated_pre) - (control_post - control_pre)
means = panel.groupby(["treated", "post"])["outcome"].mean()
did_by_hand = None  # TODO: use means.loc[(1, 1)], means.loc[(1, 0)], ...

# Q2. Fit the same thing with diff-diff and read the ATT.
results = dd.DifferenceInDifferences().fit(
    panel, outcome="outcome", treatment="treated", post="post"
)
att_library = None  # TODO: get the ATT from `results` (hint: print(dir(results)))

# Q3. The naive "post-period treated vs control" comparison ignores baseline differences.
naive_post_diff = None  # TODO: means.loc[(1, 1)] - means.loc[(0, 1)]

if did_by_hand is not None and att_library is not None:
    check("Q1 vs Q2 (hand DiD equals library ATT)", did_by_hand, att_library)
print(f"True effect = 5.0 | naive post-only diff = {naive_post_diff}  <- why is this biased?")

# ---------------------------------------------------------------------------
# Part 2: the classic Card & Krueger (1994) minimum-wage study
# ---------------------------------------------------------------------------
ck = dd.load_card_krueger()  # one row per store: emp_pre, emp_post, treated (NJ = 1)

# Q4. Reshape wide -> long so each store has a pre row (post=0) and a post row (post=1)
#     with a single `emp` column. Hint: pd.melt or build two frames and pd.concat.
long = None  # TODO: columns store_id, treated, post, emp

if long is not None:
    # Q5. Estimate the DiD with standard errors clustered by store.
    ck_res = dd.DifferenceInDifferences(cluster="store_id").fit(
        long.dropna(subset=["emp"]), outcome="emp", treatment="treated", post="post"
    )
    ck_res.print_summary()
    # Q6 (write your answer in answers.md): Did NJ's minimum-wage increase reduce
    # employment? State the ATT, its 95% CI, and ONE assumption that must hold
    # for this to be causal.

# ---------------------------------------------------------------------------
# Part 3: interview drill (answers.md, 3-4 sentences each)
# ---------------------------------------------------------------------------
# Q7. Explain potential outcomes Y(1), Y(0) and why the ATT is unobservable directly.
# Q8. A PM says "the feature launched in Texas first; Texas conversions rose 8%,
#     so the feature lifted conversion 8%". What's wrong, and how would DiD fix it?
# Q9. When would you run DiD instead of an A/B test? Give two real product examples.
