# Day 12 quiz: CUPED

**Pass mark: 8/10.** Answer on paper first, then open the answers.

---

**Q1.** Write the CUPED-adjusted metric and the formula for θ.

<details><summary>Answer</summary>

**Y_cuped = Y − θ(X − X̄), θ = Cov(Y, X)/Var(X)**, where X is the user's pre-experiment value. θ is the regression slope of Y on X, computed on pooled data from both arms.
</details>

---

**Q2.** Cov(Y, X) = 3 and Var(X) = 4. What is θ?

<details><summary>Answer</summary>

**θ = 0.75.** A user whose pre-period value is 2 above average gets 1.5 subtracted from their in-experiment value.
</details>

---

**Q3.** Why doesn't CUPED bias the treatment-effect estimate?

<details><summary>Answer</summary>

X is measured **before randomization**, so its distribution is the same in both arms in expectation, and the term θ(X − X̄) has the same expected value in each arm. Subtracting it removes noise without shifting the difference in means. You confirmed this in the homework: mean estimate ≈ 0.10, the true effect.
</details>

---

**Q4.** corr(X, Y) = 0.7. What fraction of the variance remains, and how much does the MDE shrink?

<details><summary>Answer</summary>

**51% of the variance remains (1 − 0.49).** SE scales with √0.51 ≈ 0.71, so the **MDE shrinks by about 29%**. Equivalently, it's like having 1/0.51 ≈ **1.96×** the users.
</details>

---

**Q5.** With CUPED at ρ = 0.5, a test that needed 4 weeks now needs about how long?

<details><summary>Answer</summary>

**About 3 weeks.** Variance kept is 1 − 0.25 = 75%, so the required sample (and duration) is 0.75 × 4 = 3 weeks. Statsig's duration-planning post walks through exactly this calculation.
</details>

---

**Q6.** A teammate wants to use "sessions during the experiment's first 3 days" as the CUPED covariate for a 14-day test. What is wrong with that?

<details><summary>Answer</summary>

That covariate is measured **after treatment starts**, so the treatment may have affected it. Adjusting for it can remove part of the real effect or introduce bias. CUPED requires covariates that the treatment can't influence: pre-experiment data, or pre-assignment attributes.
</details>

---

**Q7.** 30% of users are new and have no pre-period data. What happens to CUPED's benefit, and what can you do?

<details><summary>Answer</summary>

New users get **no variance reduction** if you fill their X with the mean, so the overall gain shrinks (homework: about 51% → 66% of the variance kept). Options: use other **pre-assignment** features (signup channel, device, country, acquisition campaign), analyze new and existing users separately, or use CUPAC to predict Y from whatever features are available.
</details>

---

**Q8.** True or false: CUPED and OLS regression of Y on treatment plus X give essentially the same treatment estimate.

<details><summary>Answer</summary>

**True**, nearly identical (Part 2 matched to about 10⁻⁶). The small difference comes from θ being estimated on pooled data, while OLS estimates the slope holding treatment fixed. Both are forms of **regression adjustment**, and with randomized treatment both are consistent.
</details>

---

**Q9.** What is CUPAC, and why can it beat plain CUPED?

<details><summary>Answer</summary>

**CUPAC** (DoorDash) uses an **ML model's prediction** of the outcome, built from many pre-experiment features, as the covariate X. A good prediction correlates more strongly with Y than any single pre-period metric does, so ρ is higher and the variance reduction bigger. The same rule applies: the features must be pre-treatment. (Covered in depth on Day 14.)
</details>

---

**Q10 (interview, answer out loud in 90 seconds).** "Explain CUPED to a product manager, and tell me when it won't help."

<details><summary>Model answer</summary>

"A lot of what makes experiment results noisy is that users are just different: some use the product ten times a day and some once a week, regardless of what we test. CUPED uses each user's behavior **from before the experiment** to subtract out that predictable part, so we compare treatment and control on what changed, not on who happened to be in each group. Because we only use pre-experiment data, it can't bias the result; it just makes it sharper. For engagement metrics it often cuts the noise by about half, which is like doubling our traffic, so tests can finish in about half the time. It **won't help much** when the metric has little relationship to past behavior (one-off purchases, first-time actions), when many users are new and have no history, or when the effect we care about is on brand-new users. In those cases we look at other pre-assignment features, or a model-based version called CUPAC."

**What scores well:** a non-technical intuition, the no-bias argument, the business payoff in time saved, and honest limits.
</details>

---

### Scoring
| Score | Next step |
|---|---|
| 9–10 | Move on to Day 13 |
| 8 | Pass. Re-read the explanations for the questions you missed |
| ≤ 7 | Re-read lesson §1.1–1.4 and Deng et al. §3, then retake tomorrow |

Record your score in `answers.md`, e.g. `Quiz: 9/10, missed Q6`.
