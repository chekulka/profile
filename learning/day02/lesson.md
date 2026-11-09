# Day 2: Hypothesis testing done right

**Time:** about 90–100 minutes (40 study, 40 homework, 15 quiz)
**Job skill:** "Deep expertise in statistics … online experimentation methodology"; this is the basis for every later topic (CUPED, sequential testing, DiD inference)

## 1. Concepts

### 1.1 The difference in means and its standard error
For control (A) and treatment (B), the estimated effect is Δ̂ = Ȳ_B − Ȳ_A, with

  **SE(Δ̂) = √( s_A²/n_A + s_B²/n_B )**

Facure calls the standard error of the mean, σ/√n, "the most dangerous equation": precision grows with **√n**, not n. To halve the SE you need **4×** the users.

### 1.2 Welch's t-test (the default)
t = Δ̂ / SE(Δ̂). Welch's test doesn't assume equal variances, so use it by default. Student's pooled t-test assumes σ_A = σ_B and can be badly wrong when the arm sizes *and* variances differ. With the usual sample sizes in online tests (thousands of users), t ≈ z, and a 95% CI is Δ̂ ± 1.96·SE.

### 1.3 A t-test is a regression
Regress y on a treatment dummy: y = α + β·T + ε. Then **β̂ = Δ̂ exactly**, and with heteroskedasticity-robust **HC2** standard errors, **SE(β̂) equals the Welch SE exactly.** (The plain OLS SE corresponds to the pooled-variance test.) That matters because everything advanced you'll learn, including CUPED, covariate adjustment, DiD and clustering, is this same regression with more terms on the right-hand side.

### 1.4 The CLT and skewed metrics
The t-test doesn't need normally distributed *data*. It needs the *sampling distribution of the mean* to be approximately normal, which the CLT provides as n grows. With heavy-tailed metrics such as revenue, "large enough" can mean *tens of thousands* of users. In today's homework, a nominal 95% CI for revenue per user covers the truth only about 51% of the time at n = 40, and about 89% even at n = 4,000. With small n, skew distorts the false positive rate and the CI coverage. Fixes: more data, winsorizing or capping (which changes the estimand, so say so), log transforms (which change the estimand to something closer to a geometric mean), or the bootstrap.

### 1.5 The bootstrap
Resample each arm *with replacement* B times and recompute the statistic each time. The spread of those recomputed values estimates the sampling distribution. A **percentile CI** is the 2.5th and 97.5th percentiles. Use it for statistics that have no simple SE formula: medians, quantiles, ratios. It struggles with very small n, extreme statistics (maxima), and dependent data, where you need to resample clusters rather than rows.

### 1.6 What a p-value is, and what it isn't
**Is:** P(data at least this extreme | H₀ true).
**Isn't:** P(H₀ true | data), the probability the result is "real", or a measure of effect size. Under H₀, p-values are **uniformly distributed**. You'll check that in the homework, and you'll use it on Week 2's A/A-test day.

## 2. Study materials (in this order)
1. 📖 **Facure, ch. 3, "Stats Review: The Most Dangerous Equation"** (about 20 min): https://matheusfacure.github.io/python-causality-handbook/03-Stats-Review-The-Most-Dangerous-Equation.html
2. 🎥 **StatQuest, "The Standard Error, Clearly Explained"** (about 11 min): https://www.youtube.com/watch?v=XNgt7F6FqDU
3. 🎥 **StatQuest, "Bootstrapping Main Ideas"** and **"Using Bootstrapping to Calculate p-values"**: find "Bootstrapping Part 1: Main Ideas" on the index at https://statquest.org/video_index.html · p-values video: https://www.youtube.com/watch?v=N4ZQQqyIf6k
4. 📖 **Facure, ch. 5, "The Unreasonable Effectiveness of Linear Regression"**, first section only, up to "Regression Theory" (about 15 min): https://matheusfacure.github.io/python-causality-handbook/05-The-Unreasonable-Effectiveness-of-Linear-Regression.html
5. 📘 Optional, if you have it: **Kohavi et al., *Trustworthy Online Controlled Experiments*, ch. 17, "The Statistics behind Online Controlled Experiments"**

## 3. Homework
```bash
python learning/day02/homework.py
```
Fill in every TODO (6 parts). The script checks each answer. Write short answers to the written questions in `learning/day02/answers.md`.

## 4. Quiz
Take [`quiz.md`](quiz.md) (10 questions, pass mark 8/10) and record your score in `answers.md`.

## 5. Check yourself
- [ ] I can write SE(Δ̂) from memory and explain why halving it costs 4× the sample.
- [ ] I can explain why Welch's test, not Student's, is the default.
- [ ] I can show that a t-test equals OLS on a treatment dummy (with HC2 SEs).
- [ ] I can explain when the CLT "kicks in" for revenue, and three ways to handle skew.
- [ ] I can define a p-value correctly and name three things it is *not*.
