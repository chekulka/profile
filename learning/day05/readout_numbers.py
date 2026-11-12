"""Day 5 helper: the numbers for the readout scenario. No TODOs; run it and use the output.

Run:  python learning/day05/readout_numbers.py
"""
import numpy as np
from scipy import stats

# Scenario: "Smart reminders" A/B test, 50/50 split by user, 14 days
n_c, n_t = 100_480, 99_520

# 1) Validity check: sample ratio mismatch (SRM) against the planned 50/50 split
chi2, p_srm = stats.chisquare([n_c, n_t], f_exp=[(n_c + n_t) / 2] * 2)
print(f"SRM check: control {n_c:,} vs treatment {n_t:,} | chi2={chi2:.2f}, p={p_srm:.4f}")

# 2) Primary metric: 7-day journey completion rate (a user-level proportion)
p_c, p_t = 0.310, 0.319
diff = p_t - p_c
se = np.sqrt(p_c * (1 - p_c) / n_c + p_t * (1 - p_t) / n_t)
lo, hi = diff - 1.96 * se, diff + 1.96 * se
lift = p_t / p_c - 1
# delta method for the relative lift (Day 4): Var(Rt/Rc) ~ (Rt/Rc)^2 [Var_t/Rt^2 + Var_c/Rc^2]
se_lift = (p_t / p_c) * np.sqrt((p_c * (1 - p_c) / n_c) / p_c**2 + (p_t * (1 - p_t) / n_t) / p_t**2)
print(f"Primary  completion: {p_c:.1%} -> {p_t:.1%} | diff {diff*100:+.2f} pp "
      f"[{lo*100:+.2f}, {hi*100:+.2f}] | z={diff/se:.2f}, p={2*stats.norm.sf(abs(diff/se)):.1e} "
      f"| relative {lift:+.1%} [{lift-1.96*se_lift:+.1%}, {lift+1.96*se_lift:+.1%}]")

# 3) Guardrail: support calls per user (user-level mean, sd about 0.25 in both arms)
m_c, m_t, sd = 0.0420, 0.0435, 0.25
gdiff = m_t - m_c
gse = np.sqrt(sd**2 / n_c + sd**2 / n_t)
glo, ghi = gdiff - 1.96 * gse, gdiff + 1.96 * gse
print(f"Guardrail calls/user: {m_c:.4f} -> {m_t:.4f} | diff {gdiff:+.4f} [{glo:+.4f}, {ghi:+.4f}] "
      f"| p={2*stats.norm.sf(abs(gdiff/gse)):.2f} | relative {gdiff/m_c:+.1%} "
      f"(CI {glo/m_c:+.1%} to {ghi/m_c:+.1%})")
