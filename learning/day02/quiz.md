# Day 2 quiz: hypothesis testing done right

**Pass mark: 8/10.** Answer on paper first, then open the answers.

---

**Q1.** Control: n = 10,000, s = 20. Treatment: n = 10,000, s = 20. What is SE(Δ̂)?

<details><summary>Answer</summary>

**≈ 0.283.** SE = √(400/10,000 + 400/10,000) = √0.08 ≈ 0.283. Remember that the variances add (each arm contributes s²/n). Standard deviations don't add.
</details>

---

**Q2.** You want a 3× smaller standard error. By what factor must the sample grow?
A) 3 B) 6 C) 9 D) √3

<details><summary>Answer</summary>

**C) 9.** SE ∝ 1/√n, so dividing the SE by 3 needs n × 3² = 9. This √n law is why small effects (e.g. 0.1% lifts) need huge experiments, and why variance reduction (CUPED, week 3) is so valuable.
</details>

---

**Q3.** Why is Welch's t-test the default over Student's pooled t-test?

<details><summary>Answer</summary>

Welch's test doesn't assume equal variances. Student's test pools the variances, and when the arm sizes **and** variances differ, the pooled SE is wrong: too small if the smaller arm has the larger variance, which inflates false positives. Welch loses almost nothing when variances really are equal, so there's no reason not to use it.
</details>

---

**Q4.** True or false: in `y = α + β·T + ε` with a 0/1 treatment dummy T, β̂ equals the difference in means, and its HC2 robust SE equals the Welch SE.

<details><summary>Answer</summary>

**True**, both exactly; you verified this in homework Part 2. The *plain* OLS SE equals the pooled (Student) SE instead. This equivalence is why CUPED, covariate adjustment and DiD are all "just regression with more terms".
</details>

---

**Q5.** The CLT says that, as n grows:
A) The data become normally distributed
B) The sampling distribution of the mean approaches normal
C) The variance of the data shrinks
D) Outliers disappear

<details><summary>Answer</summary>

**B.** The data keep whatever shape they have (revenue stays skewed). Only the distribution of the *sample mean* becomes approximately normal. How fast that happens depends on skewness and tail weight, which is why heavy-tailed metrics need much larger n.
</details>

---

**Q6.** A revenue metric is 95% zeros with a heavy right tail. In your homework, 95% CIs for mean revenue per user covered the truth only about 51% of the time at n = 40, and about 89% even at n = 4,000. Name two fixes and the trade-off of each.

<details><summary>Answer</summary>

(1) **More data:** the CLT eventually works, but it costs time. (2) **Winsorize or cap** at e.g. the 99.9th percentile: lower variance, but it changes the estimand and can hide real effects among whales. (3) **Bootstrap:** fewer assumptions, but it's still unreliable at very small n and more expensive to compute. (4) **Log transform** or analyzing conversion separately from revenue among buyers: well behaved, but it answers a different question than "revenue per user". Any two, with trade-offs, earns full marks.
</details>

---

**Q7.** p = 0.03. Which statement is correct?
A) There's a 3% chance the null hypothesis is true
B) There's a 97% chance the treatment works
C) If there were no effect, data this extreme would occur about 3% of the time
D) The effect is large

<details><summary>Answer</summary>

**C.** A p-value is computed *assuming* H₀ is true, so it can't be the probability of H₀ (A) or of H₁ (B). It also says nothing about magnitude (D): with huge n, tiny effects get tiny p-values. Report the effect and its CI, not just p.
</details>

---

**Q8.** You run 1,000 A/A tests correctly at α = 0.05. About how many are "significant", and what should the histogram of p-values look like?

<details><summary>Answer</summary>

**About 50**, and the histogram should be **flat (uniform on [0, 1])**. Under H₀, a correctly calibrated test has P(p < x) = x. A spike near 0 means the test is anti-conservative (for example, wrong SEs or ignored clustering). That's exactly how A/A tests are used to validate experimentation platforms (Week 2).
</details>

---

**Q9.** When is the bootstrap a good choice, and when can it fail?

<details><summary>Answer</summary>

**Good:** statistics with no easy SE formula, such as medians, percentiles (p90 latency), ratios and trimmed means. **Fails or needs care:** very small n (the resamples can't represent the population), extreme statistics like the max, and **dependent data**: if users have many sessions, resample *users* (cluster bootstrap), not sessions, or the SE will be too small.
</details>

---

**Q10 (interview, answer out loud in 90 seconds).** "Walk me through how you'd test whether a new checkout flow changes revenue per user."

<details><summary>Model answer</summary>

"First I'd define the metric and randomization unit, revenue per *user* randomized by user, and check that the analysis unit matches the randomization unit. Before launch I'd do a power calculation using historical revenue variance and the smallest effect that matters to the business. Revenue is heavily skewed, so I'd plan to cap extreme values at a pre-registered threshold, and maybe use CUPED with pre-period revenue to reduce variance. The primary analysis would be a Welch t-test, equivalently OLS with robust SEs. I'd report the lift with a confidence interval, not just a p-value, and check the result with a bootstrap. I'd also check guardrails like conversion and refund rates, run a sample ratio mismatch check first, and avoid peeking, unless we use a sequential method."

**What scores well:** unit of analysis, power analysis, skew handling, effect plus CI, and the validity checks (SRM, guardrails, peeking).
</details>

---

### Scoring
| Score | Next step |
|---|---|
| 9–10 | Move on to Day 3 |
| 8 | Pass. Re-read the explanations for the questions you missed |
| ≤ 7 | Re-read lesson §1.2–1.6 and Facure ch. 3, then retake tomorrow |

Record your score in `answers.md`, e.g. `Quiz: 9/10, missed Q6`.
