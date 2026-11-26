"""Day 19 homework: group sequential designs with alpha spending (O'Brien-Fleming vs Pocock).

Run:  python learning/day19/homework.py
Fill in every TODO. Parts with unfinished TODOs are skipped.
"""
import numpy as np
from scipy import stats

rng = np.random.default_rng(19)
print("Day 19 homework")

K = 4                                    # 4 equally spaced looks: 25%, 50%, 75%, 100% of the sample
t = np.arange(1, K + 1) / K              # information fractions
ALPHA = 0.05
SIMS = 200_000


def check(name, got, expected, tol):
    ok = got is not None and abs(float(got) - float(expected)) <= tol
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: got {got}, expected ~{expected}")
    return ok


# ---------------------------------------------------------------------------
# Part 1: spending functions: how much alpha may be "used up" by information fraction t
# ---------------------------------------------------------------------------
def obrien_fleming_spending(t, alpha=ALPHA):
    """Lan-DeMets O'Brien-Fleming-type: alpha(t) = 2 - 2*Phi( z_{1-alpha/2} / sqrt(t) )."""
    return None  # TODO: 2 - 2 * stats.norm.cdf(stats.norm.ppf(1 - alpha / 2) / np.sqrt(t))


def pocock_spending(t, alpha=ALPHA):
    """Lan-DeMets Pocock-type: alpha(t) = alpha * ln(1 + (e - 1) * t)."""
    return alpha * np.log(1 + (np.e - 1) * t)


if obrien_fleming_spending(t) is not None:
    obf = obrien_fleming_spending(t)
    print("   cumulative alpha spent, OBF:   ", np.round(obf, 4))
    print("   cumulative alpha spent, Pocock:", np.round(pocock_spending(t), 4))
    check("Part 1a OBF spends all alpha by the end", obf[-1], 0.05, 1e-9)
    check("Part 1b OBF spends almost nothing at the first look", obf[0], 0.0001, 0.00005)

    # -----------------------------------------------------------------------
    # Part 2: turn the spending into z boundaries (by simulation under H0)
    # -----------------------------------------------------------------------
    z_null = rng.normal(0, 1, (SIMS, K)).cumsum(axis=1) / np.sqrt(np.arange(1, K + 1))

    def boundaries(spent):
        """Find |z| boundaries so the chance of FIRST crossing at look k equals the alpha spent at k."""
        alive = np.ones(SIMS, bool)
        out = []
        for k in range(K):
            spend_now = None  # TODO: spent[k] - (spent[k - 1] if k > 0 else 0)
            if spend_now is None:
                return None
            zk = np.abs(z_null[:, k])
            survivors = np.sort(zk[alive])[::-1]
            m = int(round(spend_now * SIMS))
            c = survivors[m - 1] if m > 0 else np.inf
            out.append(c)
            alive &= zk < c
        return np.array(out)

    b_obf = boundaries(obf)
    b_poc = boundaries(pocock_spending(t))
    if b_obf is not None:
        print("   OBF boundaries |z|:   ", np.round(b_obf, 2))
        print("   Pocock boundaries |z|:", np.round(b_poc, 2))
        check("Part 2a OBF's final boundary is close to 1.96", b_obf[-1], 2.04, 0.04)
        print(f"[{'PASS' if b_obf[0] > 3.5 else 'FAIL'}] Part 2b OBF is very strict early")

        # -------------------------------------------------------------------
        # Part 3: false positive rate, power and expected sample size
        # -------------------------------------------------------------------
        def evaluate(bounds, drift):
            z = rng.normal(drift, 1, (100_000, K)).cumsum(axis=1) / np.sqrt(np.arange(1, K + 1))
            cross = np.abs(z) >= bounds
            stop_look = np.where(cross.any(axis=1), cross.argmax(axis=1) + 1, K)
            rejected = None  # TODO: share of simulations that crossed a boundary at any look
            return rejected, stop_look.mean() / K

        fpr_obf, _ = evaluate(b_obf, 0.0)
        if fpr_obf is not None:
            drift = (stats.norm.ppf(0.975) + stats.norm.ppf(0.8)) / np.sqrt(K)  # 80% power if fixed-n
            pw_obf, en_obf = evaluate(b_obf, drift)
            pw_poc, en_poc = evaluate(b_poc, drift)
            print(f"   OBF:    FPR {fpr_obf:.3f} | power {pw_obf:.2f} | expected sample {en_obf:.0%} of max")
            print(f"   Pocock: power {pw_poc:.2f} | expected sample {en_poc:.0%} of max")
            check("Part 3a OBF keeps FPR at 5% despite 4 looks", fpr_obf, 0.05, 0.004)
            check("Part 3b OBF loses almost no power vs the fixed design", pw_obf, 0.79, 0.02)
            print(f"[{'PASS' if en_obf < 0.85 and en_poc < en_obf and pw_poc < pw_obf else 'FAIL'}] "
                  "Part 3c Pocock stops earlier on average but loses more power")
            # Q-A (answers.md): when would you choose OBF, and when Pocock? Which would
            # Spotify-style batch data favor, and why do most platforms default to OBF?
