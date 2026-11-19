# Day 12 (Week 3, Day 1): CUPED: variance reduction from pre-experiment data

**Time:** about 90 minutes (35 study, 40 homework, 15 quiz)
**Job skill:** "variance reduction, CUPED" is named **word for word** in the OpenAI posting. It's also the cheapest way to make every experiment faster (Discord's platform roadmap).

## 1. Concepts

### 1.1 The idea
Much of the noise in a metric like "sessions this month" comes from **who the user is**: heavy users are heavy before and during the experiment. If you know each user's **pre-experiment** value X, you can subtract out the predictable part:

  **Y_cuped = Y − θ·(X − X̄), with θ = Cov(Y, X) / Var(X)**

Because X is measured **before** randomization, it is independent of treatment, so the adjustment **removes noise without adding bias**: E[Y_cuped] differences equal E[Y] differences.

### 1.2 How much it helps
  **Var(Y_cuped) = Var(Y)·(1 − ρ²)**, where ρ = corr(X, Y)
| ρ | Variance kept | Equivalent sample multiplier | MDE shrinks by |
|---|---|---|---|
| 0.3 | 91% | 1.10× | 5% |
| 0.5 | 75% | 1.33× | 13% |
| **0.7** | **51%** | **1.96×** | **29%** |
| 0.9 | 19% | 5.3× | 56% |

At ρ = 0.7 (typical for engagement metrics), CUPED is like **doubling your traffic for free**. Homework: power went from 34% to 58%.

### 1.3 CUPED = regression adjustment
Regressing Y on treatment **and** X gives almost the same estimate and SE (Part 2). That's why "CUPED" and "ANCOVA" or "regression adjustment" (Lin 2013) are often used interchangeably, and why Day 2's "a t-test is a regression" matters.

### 1.4 Practical rules
- **The covariate must not be affected by treatment.** Use pre-experiment data only. Using an in-experiment covariate can introduce bias.
- **The best covariate is usually the same metric in the pre-period**, measured over a similar time window.
- **New users have no history:** fill in the mean (they get no reduction) or use other pre-assignment features such as signup channel or device. The gain shrinks with the share of new users (Part 4: 51% → 66% of the variance kept with 30% new users).
- **CUPAC** (DoorDash) and ML-based CUPED use a *prediction* of Y from many pre-period features as X, which pushes ρ higher. That's Day 14.

## 2. Study materials (in this order)
1. 📄 ⭐ **Deng, Xu, Kohavi & Walker (2013), "Improving the Sensitivity of Online Controlled Experiments by Utilizing Pre-Experiment Data"** (WSDM '13, the original CUPED paper). Read §1–3 (about 30 min): https://dl.acm.org/doi/10.1145/2433396.2433413
2. 📖 **Booking.com, "How Booking.com increases the power of online experiments with CUPED"** (about 12 min; a practical take, including missing pre-period data): https://booking.ai/how-booking-com-increases-the-power-of-online-experiments-with-cuped-995d186fff1d
3. 📖 **Statsig, "CUPED Explained"** (about 8 min): https://www.statsig.com/blog/cuped · and **"How to plan test duration when using CUPED"**: https://www.statsig.com/blog/how-to-plan-test-duration-cuped
4. 📘 Optional: Kohavi et al., ch. 22 (the "Improving Sensitivity" section)

## 3. Homework
```bash
python learning/day12/homework.py
```
4 parts with automatic checks. Write answers to Q-A, Q-B and Q-C in `learning/day12/answers.md`.

## 4. Quiz
Take [`quiz.md`](quiz.md) (10 questions, pass mark 8/10).

## 5. Check yourself
- [ ] I can write the CUPED formula and θ from memory.
- [ ] I can explain why CUPED adds no bias when X is pre-experiment.
- [ ] I can convert ρ into variance kept, equivalent sample size and MDE reduction.
- [ ] I can explain the link to regression adjustment.
- [ ] I know how to handle users without history, and what CUPAC adds.
