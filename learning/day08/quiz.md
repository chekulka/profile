# Week 1 review quiz (cumulative, Days 1–7)

**Pass mark: 12/15.** No notes. Answer every question on paper before opening any answer.

---

**Q1.** Treated: pre 50, post 62. Control: pre 48, post 55. What is the DiD estimate?

<details><summary>Answer</summary>

**5.** (62 − 50) − (55 − 48) = 12 − 7 = 5. The control group's +7 stands in for what the treated group would have done without treatment. (Day 1)
</details>

---

**Q2.** Which assumption makes DiD causal, and can you test it directly?

<details><summary>Answer</summary>

**Parallel trends**: without treatment, the treated group's outcome would have changed by the same amount as the control group's. It **can't be tested directly**, because it's about an unobserved counterfactual. Pre-period trends can provide evidence *against* it but can't prove it. (Day 1; week 5 goes deeper.)
</details>

---

**Q3.** s = 10 in each arm, 2,500 users per arm. What is SE(Δ̂)?

<details><summary>Answer</summary>

**≈ 0.283.** √(100/2,500 + 100/2,500) = √0.08. (Day 2)
</details>

---

**Q4.** When is Student's pooled t-test dangerous, and what should you use instead?

<details><summary>Answer</summary>

When the arm sizes **and** variances differ, the pooled SE is wrong, too small or too large depending on which arm has the larger variance. Use **Welch's** test by default; it loses almost nothing when the variances are equal. (Day 2)
</details>

---

**Q5.** True or false: regressing y on a treatment dummy gives β̂ = the difference in means, and HC2 robust SEs equal Welch's SE.

<details><summary>Answer</summary>

**True**, both exactly. That's why CUPED, covariates and DiD are all "regression with more terms". (Day 2)
</details>

---

**Q6.** A revenue metric is 95% zeros with a heavy tail. Name two problems for a standard t-test at small n, and two fixes.

<details><summary>Answer</summary>

**Problems:** the sampling distribution of the mean isn't yet normal, so CIs **under-cover** (your Day 2 homework found about 51% coverage at n = 40 and about 89% at n = 4,000), and the variance is high. **Fixes:** a larger n, capping or winsorizing (which changes the estimand), a bootstrap, or splitting into conversion plus revenue among buyers. (Day 2)
</details>

---

**Q7.** σ = 5, 5,000 users per arm, α = 0.05 two-sided, 80% power. What is the MDE?

<details><summary>Answer</summary>

**≈ 0.28.** 2.80 × 5 × √(2/5,000) = 2.80 × 5 × 0.02 = 0.28. (Day 3)
</details>

---

**Q8.** Baseline conversion is 5%, and you want to detect +0.5 pp with 80% power. About how many users per arm?

<details><summary>Answer</summary>

**≈ 29,800.** 2 × 2.80² × (0.05 × 0.95)/0.005² ≈ 29,826, and Lehr's rule gives 16 × 0.0475/0.000025 = 30,400. (Day 3)
</details>

---

**Q9.** In Day 3's homework, the unclustered panel DiD had about 3% power while the clustered version had about 70%. Was the unclustered version too strict or too loose, and why?

<details><summary>Answer</summary>

**Too strict (conservative).** Its SEs were about 2.3× too big because the unit fixed effects stayed in the residual, so it almost never rejected, with 100% CI coverage and little power. Simulation is what revealed it. (Day 3)
</details>

---

**Q10.** You randomize users and measure CTR per page view. Name three methods that give a correct SE, and one tempting method that doesn't.

<details><summary>Answer</summary>

**Correct:** the delta method on user-level sums, page-level regression with SEs clustered by user, and a bootstrap that resamples **users**. **Wrong:** a two-proportion z-test on page views, or a bootstrap that resamples page views. These treat correlated views as independent, giving a false positive rate of about 11% instead of 5%. (Day 4)
</details>

---

**Q11.** Control CTR is 0.200 (SE 0.002) and treatment is 0.210 (SE 0.002). What is the relative lift, and roughly its 95% CI?

<details><summary>Answer</summary>

**+5%, CI ≈ [+2.2%, +7.8%].** Using the delta method, SE ≈ 1.05 × √((0.002/0.21)² + (0.002/0.20)²) ≈ 1.45 points. (Day 4)
</details>

---

**Q12.** A guardrail shows +3.6% (95% CI −1.6% to +8.8%) against a +5% limit. Write the one sentence you'd put in the TL;DR.

<details><summary>Answer</summary>

Something like: **"Support calls are inconclusive: we can't rule out an increase of up to 8.8%, above our 5% limit."** Not "no impact on support". A non-significant guardrail whose CI includes unacceptable harm isn't safe. (Day 5)
</details>

---

**Q13.** Planned 50/50, observed 20,400 vs 19,600. Is it an SRM, and what's your first move?

<details><summary>Answer</summary>

**Yes: χ² = 4·400²/40,000 = 16, p ≈ 0.00006.** Stop interpreting the metrics. Then localize the cause: segment the SRM check by platform, version, country and day, and find the funnel stage where it appears. Fix it and re-run; don't reweight. (Day 6)
</details>

---

**Q14.** Over 1,000 A/A tests, a new metric's p-values pile up near 0 (FPR 12%). What does that tell you, and what would you check first?

<details><summary>Answer</summary>

The method is **anti-conservative**: its SEs are too small, so it would produce false wins. Check first whether the **analysis unit is finer than the randomization unit** (Day 4), then for heavy outliers (cap them), and for correlation over time or peeking. Don't release the metric for decisions until it passes A/A. (Day 7)
</details>

---

**Q15 (interview, answer out loud in 2–3 minutes).** "A PM brings you an experiment: CTR is up 4% with p = 0.02, and they want to ship tomorrow. What do you check before agreeing?"

<details><summary>Model answer (pulls together the whole week)</summary>

"I'd run a quick trust checklist before looking at the lift. **One, validity:** an SRM check against the planned split. If it fails, we stop and debug. **Two, the analysis method:** we randomized by user, so is CTR analyzed with the delta method or user-clustered SEs? A page-level test can double the false positive rate. **Three, was it pre-planned:** did we run the planned duration (full weeks) without peeking or picking the best day, and is CTR the pre-registered primary metric or one of many? **Four, the effect:** report the relative lift with a delta-method CI, and check whether the numerator rose or the denominator fell. **Five, guardrails:** look at their upper bounds, not just their p-values. **Six, plausibility:** a 4% CTR lift is large, so Twyman's law says check the logging and look for novelty effects; if it's a big launch, consider replicating. If everything passes, I'd recommend shipping, with the range and the remaining risks stated in a one-page readout."

**What scores well:** structure (a numbered checklist), validity before results, the unit of analysis, guardrails and their upper bounds, skepticism (Twyman's law), and a clear recommendation.
</details>

---

### Scoring
| Score | Next step |
|---|---|
| 14–15 | Week 1 mastered 🏹 On to Week 2 |
| 12–13 | Pass. Revisit the days for the questions you missed (see `lesson.md`) |
| ≤ 11 | Spend next weekend re-doing the days you missed before continuing |

Record your score in `learning/day08/answers.md`, e.g. `Week 1 review: 13/15, missed Q8, Q11`.
