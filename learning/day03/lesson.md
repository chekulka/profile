# Day 3: Power and MDE (analytical vs. simulation)

**Time:** about 100 minutes (40 study, 45 homework, 15 quiz)
**Job skill:** experiment design, "practical experimentation challenges", and power for quasi-experiments with diff-diff

## 1. Concepts

### 1.1 The four quantities
Power analysis links four numbers. Fix any three and you get the fourth:
- **α**, the false positive rate (usually 0.05, two-sided)
- **power = 1 − β**, the chance of detecting a true effect of the given size (usually 0.8)
- **n**, the sample size
- **δ**, the effect size, which is the **MDE** (minimum detectable effect) when you solve for it

### 1.2 The core formula (two arms, difference in means)
  **MDE = (z₁₋α/₂ + z₁₋β) · σ · √(1/n_T + 1/n_C)**

At α = 0.05 (two-sided) and 80% power, z₀.₉₇₅ + z₀.₈ = 1.960 + 0.842 = **2.80**. With equal arms (n per arm):

  **n per arm = 2 · (2.80)² · σ² / δ² ≈ 15.7 · σ²/δ²**, which is **Lehr's rule of thumb, n ≈ 16σ²/δ²**

Intuition: the test rejects when Δ̂ > 1.96·SE. For that to happen 80% of the time, the true effect has to sit 0.84 SEs *beyond* that threshold. So MDE = 2.80 SE.

### 1.3 Conversion metrics
For a Bernoulli metric, σ² = p(1 − p). At p = 10% and an absolute lift of δ = 0.2 percentage points (a 2% relative lift), you need about **353,000 users per arm**. Small relative lifts on low base rates are *expensive*.

### 1.4 Levers that change the MDE
| Lever | Effect |
|---|---|
| 4× the sample | MDE halves (√n) |
| Unequal split (90/10 instead of 50/50) | MDE × 1.67 for the same total n |
| Lower variance (CUPED, capping, a better metric) | MDE ∝ σ: the cheapest lever (week 3) |
| 90% power instead of 80% | n × 1.34 |
| Clustered randomization (e.g. by city) | inflate by the design effect, DEFF = 1 + (m − 1)·ICC |

### 1.5 Power for DiD (diff-diff)
DiD differences *two* periods. In a repeated cross-section with one pre and one post period, the variance of the DiD estimate is **2×** that of an A/B test with the same units, so the MDE is √2 times larger. With **panel data**, serial correlation ρ within units helps, because differencing cancels the persistent part: `compute_mde(..., n_pre, n_post, rho)` captures this. diff-diff provides:
- `compute_mde`, `compute_power`, `compute_sample_size`, `PowerAnalysis`: analytical, for 2x2 and basic panel designs
- `simulate_power`, `simulate_mde`, `simulate_sample_size`: Monte Carlo for **any** estimator (including staggered designs, where no closed form exists)

### 1.6 Why simulate?
Analytical formulas assume a particular variance structure. Simulation tests **your actual estimator with your actual standard errors**. Today's homework shows the payoff: fitted without clustering, the DiD gives **about 3% power** on panel data, because its SEs are far too large. The same model with SEs clustered by unit gives **about 70% power**. Always check power *and* coverage by simulation before trusting a design.

### 1.7 Post-hoc power is meaningless
"Observed power" computed from the observed effect is a one-to-one function of the p-value, so it adds no information. Do power analysis **before** the experiment, and after it, report the confidence interval.

## 2. Study materials (in this order)
1. 🎥 **StatQuest, "Power Analysis, Clearly Explained"**: https://www.youtube.com/watch?v=VX_M3tIyiYk (also watch "Statistical Power, Clearly Explained" from https://statquest.org/video_index.html first if power is fuzzy)
2. 🛠️ **Evan Miller's sample size calculator**: https://www.evanmiller.org/ab-testing/ Reproduce §1.3 with it, then read his article "How Not To Run an A/B Test", linked from https://www.evanmiller.org/
3. 📖 **diff-diff power analysis API** (analytical + simulation): https://diff-diff.readthedocs.io/en/stable/api/power.html (offline: `python -c "import diff_diff as d; help(d.compute_mde)"`)
4. 📖 **Facure ch. 3**, the "Confidence Intervals" and "Hypothesis Testing" sections (a review of Day 2): https://matheusfacure.github.io/python-causality-handbook/03-Stats-Review-The-Most-Dangerous-Equation.html
5. 📘 Optional: Kohavi et al., ch. 17 (the "Statistical Power" section) and ch. 18 (variance estimation pitfalls)

## 3. Homework
```bash
python learning/day03/homework.py
```
6 parts with automatic checks. Write the answers to Q-A to Q-D in `learning/day03/answers.md`.

## 4. Quiz
Take [`quiz.md`](quiz.md) (10 questions, pass mark 8/10) and record your score in `answers.md`.

## 5. Check yourself
- [ ] I can derive MDE = 2.80·SE and explain where 0.84 comes from.
- [ ] I can size a conversion test from a baseline rate and a relative lift, without a calculator.
- [ ] I know how the MDE changes with n, allocation, σ, power level and clustering.
- [ ] I can explain why DiD needs more data than an A/B test, and why panel correlation helps.
- [ ] I can explain why simulation caught the unclustered-SE problem, and why post-hoc power is useless.
