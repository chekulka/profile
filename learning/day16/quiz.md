# Day 16 quiz: CUPAC and post-stratification

**Pass mark: 8/10.** Answer on paper first, then open the answers.

---

**Q1.** What does CUPAC stand for, and how does it differ from CUPED?

<details><summary>Answer</summary>

**Control Using Predictions As Covariates.** Instead of one pre-period metric, it uses an **ML model's prediction** of the outcome, built from many pre-assignment features, as the covariate in the CUPED formula. The adjustment step is the same; only the covariate changes.
</details>

---

**Q2.** The best single covariate has ρ = 0.26, and the CUPAC prediction has ρ = 0.91. What share of the variance does each keep?

<details><summary>Answer</summary>

**Single covariate: 1 − 0.26² ≈ 93%. CUPAC: 1 − 0.91² ≈ 17%.** CUPAC leaves about 5.5× less variance, which is like having about 5.5× the traffic. That matches your homework.
</details>

---

**Q3.** Why does CUPAC remain unbiased even though an ML model is involved?

<details><summary>Answer</summary>

The prediction is a function of **pre-assignment features only**, so it's independent of treatment assignment, just like a pre-period metric. Subtracting θ(ŷ − ŷ̄) removes noise but has the same expected value in both arms. The model's quality affects **how much** variance is removed, never the bias.
</details>

---

**Q4.** A teammate trains the CUPAC model on the experiment's own data, including treated users' in-experiment outcomes, and predicts on the same users. What's the risk, and the fix?

<details><summary>Answer</summary>

**Leakage and overfitting:** the model can partly learn the treatment effect or overfit each user's own outcome, so the adjustment can absorb part of the effect or produce invalid SEs. Fix: train on **historical (pre-experiment) data**, or use **cross-fitting** (train on some folds, predict on held-out users, rotate), and exclude treatment from the features.
</details>

---

**Q5.** The CUPAC model was trained 6 months ago and the product has changed. Are the results now biased?

<details><summary>Answer</summary>

**No, not biased, just less precise.** A stale model predicts worse, so ρ drops and you get less variance reduction, but unbiasedness depends only on the features being pre-treatment. Monitor the achieved variance reduction and retrain periodically.
</details>

---

**Q6.** Write the post-stratified estimator.

<details><summary>Answer</summary>

**τ̂_ps = Σₛ wₛ (ȳ_T,s − ȳ_C,s)**, with wₛ = the share of users in stratum s. It's the treatment effect within each stratum, averaged with the population weights. It equals a regression with stratum dummies interacted with treatment.
</details>

---

**Q7.** When can post-stratification *increase* variance?

<details><summary>Answer</summary>

With **many small or poorly chosen strata**: some stratum-arm cells have very few users, so their means are noisy, and that noise outweighs the gain. Miratrix et al. show it's nearly as good as blocking in large samples, but in finite samples, pick a few strata that genuinely predict the outcome.
</details>

---

**Q8.** Stratified randomization (blocking) vs. post-stratification: what's the difference, and which do large online platforms usually prefer?

<details><summary>Answer</summary>

**Blocking** balances the strata *at assignment time*. **Post-stratification** randomizes normally and adjusts *at analysis time*. Large platforms usually prefer **post-assignment methods** (post-stratification, CUPED, CUPAC): they're nearly as efficient at scale, don't complicate the assignment service, and can be applied retroactively. Booking.com's experimentation paper makes this point.
</details>

---

**Q9.** You have no user history (all new users), but you know device, country and acquisition channel at signup. Which variance-reduction methods are available?

<details><summary>Answer</summary>

**Post-stratification or regression adjustment** on device, country and channel (all pre-assignment), or **CUPAC** using a model that predicts the outcome from those signup features, trained on past cohorts. Plain CUPED with a pre-period metric isn't possible, because there's no pre-period.
</details>

---

**Q10 (interview, answer out loud in 2 minutes).** "Our experiments take 4 weeks to reach significance. As the platform's Staff DS, what's your variance-reduction roadmap?"

<details><summary>Model answer</summary>

"I'd sequence it by value per unit of effort. **Quarter 1, quick wins:** pre-registered **capping** of heavy-tailed metrics, and **CUPED** on the primary metrics using the same metric from the pre-period. That's often a 30–50% variance cut, so 4 weeks becomes 2–3. I'd validate with A/A tests that the false positive rate stays at 5%, and measure the realized reduction per metric on past experiments. **Quarter 2:** generalize to **Lin-style regression adjustment** with a few strong covariates, plus **post-stratification** for new users using signup attributes. **Quarter 3:** **CUPAC**, an ML model trained on historical data, or cross-fitted, predicting each primary metric from many pre-assignment features. That gives the biggest gains, especially for new users and nonlinear metrics, but needs model monitoring and retraining. Throughout, I'd publish a dashboard of achieved variance reduction and test duration per metric, so teams see the payoff, and I'd make it the default in the stats engine rather than an opt-in."

**What scores well:** sequencing by ROI, concrete expected gains, validation (A/A, unbiasedness), new-user handling, the maintenance cost of ML, and making it the default.
</details>

---

### Scoring
| Score | Next step |
|---|---|
| 9–10 | Move on to Day 17 |
| 8 | Pass. Re-read the explanations for the questions you missed |
| ≤ 7 | Re-read lesson §1.2–1.3 and the DoorDash post, then retake tomorrow |

Record your score in `answers.md`, e.g. `Quiz: 9/10, missed Q7`.
