# Day 4: Ratio metrics and the delta method

**Time:** about 100 minutes (40 study, 45 homework, 15 quiz)
**Job skill:** "Practical experimentation challenges in production systems", plus metric design. This mistake is common in real teams, and interviewers love it.

## 1. Concepts

### 1.1 The trap: analysis unit ≠ randomization unit
You randomize **users**, but many metrics are ratios over **sessions, page views or clicks**:
- CTR = total clicks / total page views
- Revenue per session = total revenue / total sessions
- Latency p50 per request, add-to-cart rate per visit, and so on

The sessions of one user are **correlated**: a heavy clicker clicks in every session. If you treat sessions as independent (a "naive" t-test or z-test on sessions), you overstate how much independent information you have, **the SE is too small, and false positives inflate**. In today's homework, naive A/A tests reject **about 11%** of the time instead of 5%.

### 1.2 The delta method for a ratio of means
For each user i, let Yᵢ = clicks and Xᵢ = sessions. The metric is R = Ȳ / X̄, a ratio of *user-level* means, which equals total clicks / total sessions. Because (Ȳ, X̄) are means of i.i.d. **user** rows, the CLT applies to them, and a first-order Taylor expansion gives:

  **Var(R̂) ≈ (1 / (n·μ_X²)) · [ σ²_Y − 2R·σ_XY + R²·σ²_X ]**

with n = number of users, and sample moments plugged in. Intuition: the ratio's noise comes from the numerator's noise, the denominator's noise, and how they move together. A positive covariance (users with more sessions also click more) *reduces* the variance.

### 1.3 Three equivalent ways to get the right SE
1. **Delta method** (closed form, fast, works with sufficient statistics at scale: n, ΣY, ΣX, ΣY², ΣX², ΣXY)
2. **Session-level regression with SEs clustered by user.** This gives *exactly* the delta-method SE (you'll verify it to 10 decimal places)
3. **Bootstrap that resamples users**, never sessions

### 1.4 Ratio of totals vs. mean of ratios
Σclicks/Σsessions (heavy users weigh more) ≠ mean of each user's own CTR (every user weighs equally). These are **different estimands**: choose one deliberately and state it. The mean of per-user ratios is a plain user-level mean, so a normal t-test works for it.

### 1.5 Percent lift
Stakeholders want "+3% CTR". For lift = R_T/R_C − 1, apply the delta method again: Var(R_T/R_C) ≈ (R_T/R_C)² · [Var(R_T)/R_T² + Var(R_C)/R_C²], since the arms are independent. It's covered in section 3 of the Deng et al. paper.

### 1.6 The same idea everywhere
Whenever the randomization unit is coarser than the analysis unit, apply this rule: cluster by the randomization unit. That covers users → sessions, servers → users (Discord), cities → riders (geo tests), and stores → days (Card & Krueger on Day 1).

## 2. Study materials (in this order)
1. 📄 ⭐ **Deng, Knoblich & Lu (2018), "Applying the Delta Method in Metric Analytics: A Practical Guide with Novel Ideas"** (KDD '18, Microsoft ExP). Read §1–2 and the ratio-metric and percent-change examples in §3 (about 30 min): https://arxiv.org/abs/1803.06336 · PDF: https://arxiv.org/pdf/1803.06336
2. 📖 Review **Facure ch. 3** (standard errors) if needed: https://matheusfacure.github.io/python-causality-handbook/03-Stats-Review-The-Most-Dangerous-Equation.html
3. 📘 Optional: **Kohavi et al., ch. 18, "Variance Estimation and Improved Sensitivity: Pitfalls and Solutions"** (the ratio-metric pitfall)

## 3. Homework
```bash
python learning/day04/homework.py
```
5 parts with automatic checks. Write answers to Q-A to Q-C in `learning/day04/answers.md`.

## 4. Quiz
Take [`quiz.md`](quiz.md) (10 questions, pass mark 8/10) and record your score in `answers.md`.

## 5. Check yourself
- [ ] I can explain why session-level t-tests inflate false positives when users are randomized.
- [ ] I can write the delta-method variance for a ratio from memory.
- [ ] I know three equivalent ways to get the correct SE (delta, cluster-robust regression, user bootstrap).
- [ ] I can explain ratio-of-totals vs. mean-of-ratios and when I'd use each.
- [ ] I can apply the "cluster by randomization unit" rule to Discord servers and geo tests.
