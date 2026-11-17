"""Day 10 homework: novelty effects, carryover, and interference: when "the effect" lies.

Run:  python learning/day10/homework.py
Fill in every TODO. Parts with unfinished TODOs are skipped.
"""
import numpy as np
from scipy.optimize import curve_fit

rng = np.random.default_rng(10)
print("Day 10 homework")


def check(name, got, expected, tol):
    ok = got is not None and abs(float(got) - float(expected)) <= tol
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: got {got}, expected ~{expected}")
    return ok


# ---------------------------------------------------------------------------
# Part 1: novelty effect: a shiny new UI gets clicks at first, then users get used to it
# ---------------------------------------------------------------------------
days = np.arange(28)
true_daily_effect = 2 + 6 * np.exp(-days / 3)           # long-run effect = 2
daily_estimate = true_daily_effect + rng.normal(0, 0.6, 28)  # what your dashboard shows

week1 = daily_estimate[:7].mean()
print(f"   week-1 average effect {week1:.2f}  <- what a 1-week test would report")


def decay(t, long_run, novelty, tau):
    return long_run + novelty * np.exp(-t / tau)


params = None  # TODO: curve_fit(decay, days, daily_estimate, p0=[1, 5, 2])[0]
if params is not None:
    long_run = params[0]
    print(f"   fitted long-run effect {long_run:.2f}, novelty {params[1]:.2f}, decay tau {params[2]:.1f} days")
    check("Part 1 long-run effect recovered", long_run, 2.0, 0.5)
    # Q-A (answers.md): the 1-week test overstates the effect by how much? Name two
    # ways to detect novelty in a REAL experiment (hint: plot the effect by day, and
    # compare new vs. returning users).

# ---------------------------------------------------------------------------
# Part 2: carryover: reusing the same buckets as a previous experiment
# ---------------------------------------------------------------------------
# A previous experiment's treatment annoyed users and lowered their engagement by 3
# points, and the damage persisted. The new experiment is an A/A test (no effect).
n = 100_000
previous_arm = rng.integers(0, 2, n)
engagement = rng.normal(50, 10, n) - 3 * previous_arm


def aa_effect(arm):
    d = engagement[arm == 1].mean() - engagement[arm == 0].mean()
    se = np.sqrt(engagement[arm == 1].var() / (arm == 1).sum() + engagement[arm == 0].var() / (arm == 0).sum())
    return d, d / se


reused = previous_arm.copy()  # the bucket assignment was reused (same hash salt)
fresh = None  # TODO: a fresh random 0/1 assignment for n users (a new hash salt)
if fresh is not None:
    d_r, z_r = aa_effect(reused)
    d_f, z_f = aa_effect(fresh)
    print(f"   reused buckets: 'effect' {d_r:+.2f} (z={z_r:.1f}) | fresh buckets: {d_f:+.2f} (z={z_f:.1f})")
    print(f"[{'PASS' if abs(z_r) > 10 and abs(z_f) < 3 else 'FAIL'}] Part 2 re-randomizing removes carryover")

# ---------------------------------------------------------------------------
# Part 3: interference: a ride marketplace with FIXED supply
# ---------------------------------------------------------------------------
# Treatment: a "priority" feature. Each market has 1,000 riders and only 400 rides.
# Treated riders get matched first. Does the feature create MORE rides overall?
M, R, SUPPLY = 50, 1000, 400


def run_market(frac_treated):
    treated = rng.random(R) < frac_treated
    wants_ride = rng.random(R) < 0.6
    priority = np.where(treated, 3.0, 1.0) * wants_ride + rng.random(R) * 0.01
    got = np.zeros(R, bool)
    got[np.argsort(-priority)[:min(SUPPLY, wants_ride.sum())]] = True
    return treated, got & wants_ride


# (a) User-level randomization: 50/50 inside every market
t_all, g_all = zip(*[run_market(0.5) for _ in range(M)])
t_all, g_all = np.concatenate(t_all), np.concatenate(g_all)
user_level = None  # TODO: ride rate of treated riders minus ride rate of control riders
# (b) Market-level (cluster) randomization: half the markets fully treated, half fully control
rates = np.array([run_market(1.0 if m < M // 2 else 0.0)[1].mean() for m in range(M)])
cluster_level = None  # TODO: mean ride rate of treated markets minus control markets
if user_level is not None and cluster_level is not None:
    print(f"   user-level estimate {user_level:+.3f} | market-level estimate {cluster_level:+.3f}")
    check("Part 3a user-level shows a big fake effect", user_level, 0.39, 0.05)
    check("Part 3b market-level reveals no real gain", cluster_level, 0.0, 0.01)
    # Q-B (answers.md): explain why the user-level test lies (SUTVA). Which design
    # would you use at Discord for a feature that changes how users message each
    # other inside a server? What does it cost you in power?
