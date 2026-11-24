# Day 17 quiz: variance reduction for ratio metrics

**Pass mark: 8/10.** Answer on paper first, then open the answers.

---

**Q1.** Why can't you apply CUPED directly to CTR = Σclicks/Σsessions?

<details><summary>Answer</summary>

CUPED adjusts a **per-user** metric with a per-user covariate. CTR as a ratio of totals isn't an average of independent per-user values, and its variance comes from the delta method. You first need a per-user representation: **linearization**.
</details>

---

**Q2.** Write the linearized metric for CTR.

<details><summary>Answer</summary>

**Lᵢ = (cᵢ − R·sᵢ)/s̄**, with R = Σc/Σs (pooled over both arms) and s̄ = mean sessions per user. Each user's contribution is their clicks minus what the overall CTR predicts from their sessions, scaled by average sessions.
</details>

---

**Q3.** True or false: the t-test SE of the linearized metric's difference matches the delta-method SE for the CTR difference.

<details><summary>Answer</summary>

**True** to first order. Part 1 matched it to about 0.005%. That's why linearization is safe: it gives the same inference as the delta method, but in a per-user form.
</details>

---

**Q4.** After linearizing, which tools become available? (Choose all that apply.) A) CUPED, B) Lin regression adjustment, C) post-stratification, D) CUPAC.

<details><summary>Answer</summary>

**All four.** Once the metric is per-user, every per-user method applies, using the linearized pre-period metric (or a model's prediction of it) as the covariate. Budylin et al. show that this preserves the original ratio test's directionality and significance level.
</details>

---

**Q5.** Why might ratio metrics gain less from CUPED than count metrics like "sessions per user"?

<details><summary>Answer</summary>

A ratio already divides out much of each user's activity level, the main source of between-user variance that a pre-period metric predicts well. What's left (variation in click-propensity, plus per-session noise) correlates less strongly with the pre-period, so ρ is lower and the variance reduction smaller (homework: 13–24% vs. about 50% for sessions on Day 12).
</details>

---

**Q6.** In the homework, a 4-week pre-period window kept 76% of the variance vs. 87% for a 1-week window. Why?

<details><summary>Answer</summary>

A longer window averages over more sessions, so each user's **pre-period CTR estimate is less noisy** and closer to their true propensity. A less noisy covariate correlates more strongly with the outcome, so ρ rises and more variance is removed. Too long a window can backfire, though, if users' behavior drifts.
</details>

---

**Q7.** A test needs 35 days without CUPED. With 13% variance reduction, how many full weeks does it need? With 24%?

<details><summary>Answer</summary>

**13%:** 35 × 0.87 = 30.5 days → still **5 weeks** (no saving). **24%:** 35 × 0.76 = 26.6 days → **4 weeks** (one week saved). Variance reductions only pay off in practice when they cross a whole-week threshold, or meaningfully shrink the MDE.
</details>

---

**Q8.** 24% variance reduction shrinks the MDE by about how much at the same sample size?

<details><summary>Answer</summary>

**≈ 13%.** The MDE scales with √(variance): √0.76 ≈ 0.87, so the MDE is about 13% smaller. At fixed duration you can detect effects about 13% smaller.
</details>

---

**Q9.** Linearization uses R estimated from pooled data. Why pooled rather than per arm?

<details><summary>Answer</summary>

Using one common R for both arms keeps the transformation **identical across arms**, so the linearized difference reflects the treatment's effect rather than arm-specific centering. With a per-arm R, each arm's linearized mean would be exactly zero, which tells you nothing. Pooling is also what makes the first-order equivalence to the delta method hold.
</details>

---

**Q10 (interview, answer out loud in 90 seconds).** "Our main metric is messages per active user, a ratio. Teams say CUPED doesn't help it. What do you tell them?"

<details><summary>Model answer</summary>

"First, CUPED needs a per-user metric, so for a ratio like messages per active user we **linearize** it: each user's messages minus the overall ratio times their active days, scaled by the average denominator. Its t-test matches the delta method, so inference doesn't change. Then CUPED applies, with the **linearized pre-period metric** as the covariate. Second, set expectations: ratio metrics typically gain less than count metrics because the denominator already absorbs much of the between-user variation. We can increase the gain with a **longer pre-period window** (4 weeks instead of 1), adding covariates via regression adjustment, or **CUPAC** with an ML prediction. Third, I'd report the gain as **weeks saved or MDE reduction**, not just percent variance, because a 13% cut might not change the test's length in whole weeks, while 25% might save one. If it still doesn't help, we should check whether the metric is the right decision metric at all, or whether a more sensitive proxy exists (Day 9)."

**What scores well:** linearization, setting honest expectations, concrete ways to boost the gain, translating it into time, and stepping back to question the metric.
</details>

---

### Scoring
| Score | Next step |
|---|---|
| 9–10 | Move on to the Week 3 weekend project |
| 8 | Pass. Re-read the explanations for the questions you missed |
| ≤ 7 | Re-read lesson §1.2–1.4, redo homework Part 1, then retake tomorrow |

Record your score in `answers.md`, e.g. `Quiz: 9/10, missed Q9`.
