# Day 13 quiz: regression adjustment

**Pass mark: 8/10.** Answer on paper first, then open the answers.

---

**Q1.** Write Lin's (2013) regression for estimating the ATE with one covariate X.

<details><summary>Answer</summary>

**Y = α + τT + β(X − X̄) + γT(X − X̄) + ε**, estimated by OLS with **HC2 (or other robust) SEs**. With X centered, τ̂ estimates the average treatment effect, and the interaction lets each arm have its own slope.
</details>

---

**Q2.** Under what two conditions can ANCOVA without the interaction be *less* precise than the unadjusted difference in means?

<details><summary>Answer</summary>

**(1) Unequal allocation** (e.g. 80/20) **and (2) heterogeneous effects**, meaning the covariate's slope differs between arms. The common slope is then a weighted mix dominated by the larger arm, which adjusts the smaller arm poorly. Homework: SD 0.27 vs. 0.19 unadjusted.
</details>

---

**Q3.** Why must X be centered in Lin's regression?

<details><summary>Answer</summary>

With the interaction T·X, the coefficient on T is the treatment effect **at X = 0**. Centering makes X = 0 correspond to the **sample mean**, so τ̂ becomes the effect at the average covariate value, which is the ATE. Without centering, τ̂ is the effect for a hypothetical user with X = 0, which may not even exist.
</details>

---

**Q4.** Treatment raises sessions, and sessions drive revenue. An analyst "controls for sessions" in the revenue regression and finds no effect. What went wrong?

<details><summary>Answer</summary>

Sessions are a **mediator**, a post-treatment variable on the causal path. Adjusting for them compares users with the *same* sessions, which removes the part of the effect that works through sessions (here, all of it: +$6 became about $0). It's a **bad control**: only adjust for pre-treatment variables.
</details>

---

**Q5.** Which are safe covariates for adjusting an A/B test on 30-day revenue? (Choose all that apply.)
A) Revenue in the 30 days before the experiment
B) Number of purchases during the experiment
C) Country at signup
D) Whether the user saw the new checkout page

<details><summary>Answer</summary>

**A and C.** Both are fixed before randomization. **B** is affected by treatment (a bad control). **D** depends on treatment assignment and behavior (exposure), so adjusting for it biases the comparison. Use "saw the page" to define a *triggered analysis* population carefully (balanced by design), not as a covariate.
</details>

---

**Q6.** You add 20 irrelevant pre-treatment covariates to a regression with n = 5,000. What happens to the treatment SE?

<details><summary>Answer</summary>

**Almost nothing** (homework: 0.0286 → 0.0287). Each extra covariate costs about one degree of freedom, which is trivial at large n. At small n, or with hundreds of covariates, it can hurt and overfit. That's when regularized or cross-fitted adjustment (Lasso, DML) is used.
</details>

---

**Q7.** True or false: with Lin's estimator and robust SEs, adjusting for pre-treatment covariates cannot reduce asymptotic precision compared to no adjustment.

<details><summary>Answer</summary>

**True** (Lin's main result). With a full set of treatment × covariate interactions, OLS adjustment is asymptotically at least as precise as the unadjusted estimator, and the Huber-White sandwich SEs are valid. That's why it's a safe default.
</details>

---

**Q8.** How are CUPED and Lin's estimator related?

<details><summary>Answer</summary>

Both are **regression adjustment with pre-treatment covariates**. CUPED uses one covariate with a pooled slope θ, which is like ANCOVA, and is nearly equivalent with balanced 50/50 splits. Lin generalizes it to many covariates and separate slopes per arm, which protects precision under unequal splits and heterogeneity.
</details>

---

**Q9.** Is every post-treatment variable a bad control?

<details><summary>Answer</summary>

**In experiment readouts, treat them all as bad by default.** Cinelli, Forney and Pearl show that a few special cases exist in causal graphs, but mediators, colliders and anything the treatment can change will bias a standard A/B readout. If you need mechanisms ("did it work *through* sessions?"), that's **mediation analysis**, a separate question with stronger assumptions.
</details>

---

**Q10 (interview, answer out loud in 90 seconds).** "Our platform uses CUPED. A teammate wants to switch to 'full regression adjustment with lots of covariates'. What's your advice?"

<details><summary>Model answer</summary>

"Regression adjustment generalizes CUPED and can add more precision, but three things matter. First, **only pre-treatment covariates**: pre-period metrics, attributes at assignment. Anything measured during the experiment risks bias, because adjusting for a mediator can erase a real effect. Second, use **Lin's specification**: center the covariates, interact them with treatment, and use robust SEs. Plain ANCOVA can be less precise than doing nothing when the split is unequal and effects vary, and Lin's version is guaranteed not to hurt asymptotically. Third, **don't overfit**: a few strong covariates beat hundreds, and with many features I'd use a cross-fitted ML prediction as a single covariate (CUPAC or DML style). Before rolling it out, I'd validate it with A/A tests for calibration (Day 7) and measure the variance reduction on historical experiments, so we know the gain is worth the complexity."

**What scores well:** the pre-treatment rule, Lin's interaction with robust SEs, the overfitting caveat with an ML alternative, and validation before rollout.
</details>

---

### Scoring
| Score | Next step |
|---|---|
| 9–10 | Move on to Day 14 |
| 8 | Pass. Re-read the explanations for the questions you missed |
| ≤ 7 | Re-read lesson §1.2–1.3 and Lin's abstract and §1, then retake tomorrow |

Record your score in `answers.md`, e.g. `Quiz: 9/10, missed Q5`.
