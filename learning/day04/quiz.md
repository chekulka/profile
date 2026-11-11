# Day 4 quiz: ratio metrics and the delta method

**Pass mark: 8/10.** Answer on paper first, then open the answers.

---

**Q1.** You randomize users and measure CTR = total clicks / total page views. Your analyst runs a two-proportion z-test treating every page view as independent. What is wrong?

<details><summary>Answer</summary>

The **analysis unit (page view) differs from the randomization unit (user)**. One user's page views are correlated, since some users click a lot, so the observations aren't independent. The naive SE is **too small**, and false positives inflate: about 11% instead of 5% in your homework. Use the delta method, cluster by user, or bootstrap users.
</details>

---

**Q2.** n = 10,000 users. Per user: mean clicks 2, mean sessions 10 (so R = 0.2), Var(clicks) = 4, Var(sessions) = 25, Cov(clicks, sessions) = 8. What is the delta-method SE of R?

<details><summary>Answer</summary>

**≈ 0.00134.** Var(R) = [4 − 2(0.2)(8) + 0.2²(25)] / (10,000 × 10²) = (4 − 3.2 + 1.0)/1,000,000 = 1.8×10⁻⁶, and SE = √(1.8×10⁻⁶) ≈ 0.00134. Notice how the positive covariance term (−3.2) shrinks the variance.
</details>

---

**Q3.** Which of these gives the correct SE for a user-randomized CTR? (Choose all that apply.)
A) Delta method on user-level sums
B) Session-level OLS with SEs clustered by user
C) Bootstrap that resamples sessions
D) Bootstrap that resamples users

<details><summary>Answer</summary>

**A, B and D.** You confirmed that A and B match to 10 decimal places, and that D comes within about 2%. **C is wrong**: resampling sessions breaks the within-user correlation, just like the naive test. Always resample at the randomization unit.
</details>

---

**Q4.** Why does a *positive* covariance between clicks and sessions reduce Var(R̂)?

<details><summary>Answer</summary>

When a user with more sessions also has more clicks, the numerator and denominator move **together**, so their ratio stays more stable than either one alone. Mathematically, it's the −2R·σ_XY term. If clicks and sessions moved in opposite directions, the ratio would swing more and the variance would increase.
</details>

---

**Q5.** In your homework the delta SE was about 1.22× the naive SE. What is the design effect, and what does it mean?

<details><summary>Answer</summary>

**DEFF ≈ 1.22² ≈ 1.50.** The true variance is 1.5× what the naive analysis assumes, so your sessions carry only about as much information as **1/1.5 ≈ 67%** as many independent observations. It also means a sample size computed from the naive variance would leave the test underpowered.
</details>

---

**Q6.** Control CTR = 0.200 (SE 0.002), treatment CTR = 0.210 (SE 0.002). Using the delta method, what is the relative lift and its approximate 95% CI?

<details><summary>Answer</summary>

**Lift = 5%, 95% CI ≈ [2.2%, 7.8%].** Var(R_T/R_C) ≈ (1.05)² × [(0.002/0.21)² + (0.002/0.20)²], which gives SE ≈ 0.0145 (1.45 points), so the CI is 5% ± 1.96 × 1.45% ≈ ±2.8%. Report relative lifts with their own delta-method CI. Don't just divide the absolute CI by the baseline.
</details>

---

**Q7.** "Ratio of totals" (Σclicks/Σviews) versus "mean of per-user ratios" (average of each user's CTR):
A) They always give the same number
B) They're different estimands; heavy users dominate the first, while every user counts equally in the second
C) The second needs the delta method
D) The first is always biased

<details><summary>Answer</summary>

**B.** They answer different questions. The mean of per-user ratios is a plain user-level average, so a normal t-test works for it (C is backwards). Neither is "biased"; pick the one that matches the product question and say which you chose. They diverge sharply when heavy users behave differently from light users, which is common.
</details>

---

**Q8.** Discord randomizes **servers**, and you measure messages per active user. What is the randomization unit, what is the analysis unit, and how do you compute the SE?

<details><summary>Answer</summary>

Randomization unit: **server**. Analysis unit: **user** (or message). Treat it as a ratio metric at the server level, Σmessages/Σactive users per server, and use the delta method over servers, or cluster SEs by server. With few large servers, effective n is the number of servers, not users, so power will be much lower than it looks.
</details>

---

**Q9.** Why is the delta method popular in large experimentation platforms instead of the bootstrap?

<details><summary>Answer</summary>

It needs only **sufficient statistics** per arm (n, ΣY, ΣX, ΣY², ΣX², ΣXY), which can be aggregated in SQL or Spark over billions of rows in a single pass. A bootstrap needs repeated resampling of the full user-level data, which is far too slow for thousands of experiments × hundreds of metrics daily. That's why week 12 (Spark) builds on this.
</details>

---

**Q10 (interview, answer out loud in 90 seconds).** "The PM says CTR went up 3%, p = 0.01, from a test on page views. Can we ship?"

<details><summary>Model answer</summary>

"Before shipping I'd check how the p-value was computed. We randomized by user but measured page views. If the test treated page views as independent, the SE is too small and the p-value is overstated; in A/A tests that approach can double the false positive rate. I'd recompute using the delta method (or user-clustered SEs), and report the relative lift with a delta-method CI. I'd also check SRM and our guardrails, and whether the CTR increase came from more clicks or fewer page views, since a ratio can rise because its denominator fell. If it's still significant and the guardrails are fine, we ship. If not, we may need more traffic, or variance reduction like CUPED."

**What scores well:** spotting the unit mismatch, naming the fix, delta-method CI for the lift, and checking whether the numerator or the denominator moved.
</details>

---

### Scoring
| Score | Next step |
|---|---|
| 9–10 | Move on to Day 5 |
| 8 | Pass. Re-read the explanations for the questions you missed |
| ≤ 7 | Re-read lesson §1.1–1.3 and Deng et al. §2, then retake tomorrow |

Record your score in `answers.md`, e.g. `Quiz: 9/10, missed Q6`.
