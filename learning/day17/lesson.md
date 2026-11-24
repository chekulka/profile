# Day 17 (Week 3, Day 4): Variance reduction for ratio metrics, and what the gain is really worth

**Time:** about 80 minutes (30 study, 35 homework, 15 quiz)
**Job skill:** "variance reduction, CUPED, … metric design" (OpenAI). Most product metrics are ratios (CTR, revenue per session, messages per active user), so this is where CUPED meets real dashboards.

## 1. Concepts

### 1.1 The problem
CUPED (Day 12) works on **per-user** metrics. CTR = Σclicks/Σsessions isn't a per-user average; it's a **ratio of totals**, and its SE needs the delta method (Day 4). So how do you apply CUPED to it?

### 1.2 Linearization
Turn the ratio into a per-user metric with the same first-order behavior:

  **Lᵢ = (cᵢ − R·sᵢ) / s̄**, with R = Σc/Σs (pooled) and s̄ = mean sessions

- The difference in mean L between arms ≈ the difference in CTR, and **its plain t-test SE equals the delta-method SE** (Part 1: equal to 4 decimal places).
- Now L is per-user, so **CUPED, regression adjustment, post-stratification and CUPAC all apply**, using the linearized pre-period metric as the covariate.
- Budylin et al. (Yandex, WSDM 2018) prove this transformation keeps the **directionality and significance level** of the original ratio test.

### 1.3 Ratio metrics usually gain less, and the pre-period window matters
Ratio metrics are already "normalized" by the denominator, so their correlation with the pre-period is often lower than for count metrics. Homework:
| Pre-period window | ρ | Variance kept |
|---|---|---|
| 1 week | about 0.35 | **87%** |
| 4 weeks | about 0.49 | **76%** |

A **longer pre-period** averages away noise in each user's history, which gives a better covariate and a bigger gain.

### 1.4 What a variance cut is really worth
Duration ∝ variance, but tests run in **whole weeks** (Days 3, 5):
- 35-day test × 0.76 = 26.6 days → **4 weeks** (saves a week ✅)
- 35-day test × 0.87 = 30.5 days → **still 5 weeks** (saves nothing ❌)

So when you tell a PM "CUPED cuts variance by 13%", translate it into **weeks saved** or **MDE reduction**. That's the number that changes decisions.

## 2. Study materials (in this order)
1. 📄 ⭐ **Budylin, Drutsa, Katsev & Tsoy (2018), "Consistent Transformation of Ratio Metrics for Efficient Online Controlled Experiments"** (WSDM '18). Read the abstract, §1 and the transformation section (PDF on ResearchGate): https://dl.acm.org/doi/10.1145/3159652.3159699 · PDF: https://www.researchgate.net/profile/Roman-Budylin/publication/322969314_Consistent_Transformation_of_Ratio_Metrics_for_Efficient_Online_Controlled_Experiments/links/5b054bbb45851588c6d4a1aa/Consistent-Transformation-of-Ratio-Metrics-for-Efficient-Online-Controlled-Experiments.pdf
2. 📄 Review: **Deng, Knoblich & Lu (2018), the delta method paper** (Day 4), the ratio-metric sections: https://arxiv.org/abs/1803.06336
3. 📖 **Statsig, "How to plan test duration when using CUPED"** (turning variance reduction into time): https://www.statsig.com/blog/how-to-plan-test-duration-cuped
4. 📄 Optional, newer: **"Variance Reduction in Ratio Metrics for Efficient Online Experiments"** (2024): https://arxiv.org/html/2401.04062

## 3. Homework
```bash
python learning/day17/homework.py
```
3 parts with automatic checks. Write answers to Q-A and Q-B in `learning/day17/answers.md`.

## 4. Quiz
Take [`quiz.md`](quiz.md) (10 questions, pass mark 8/10).

## 5. Check yourself
- [ ] I can write the linearized metric and explain why its SE matches the delta method.
- [ ] I can apply CUPED to a ratio metric through linearization.
- [ ] I know why a longer pre-period window can increase the gain.
- [ ] I translate variance reduction into weeks saved or MDE reduction for stakeholders.
