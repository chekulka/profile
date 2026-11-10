# Day 3 quiz: power and MDE

**Pass mark: 8/10.** Use z₀.₉₇₅ = 1.96 and z₀.₈ = 0.84 (sum 2.80). Answer on paper first, then open the answers.

---

**Q1.** σ = 20, 10,000 users per arm, α = 0.05 two-sided, power 80%. What is the MDE?

<details><summary>Answer</summary>

**≈ 0.79.** SE = 20·√(2/10,000) = 0.283, and MDE = 2.80 × 0.283 ≈ 0.79. Note that the MDE is 2.8 SEs, not 1.96: you need room for the estimate to land beyond the rejection threshold 80% of the time.
</details>

---

**Q2.** Baseline conversion is 10%. You want to detect +0.2 percentage points (a 2% relative lift) with 80% power. About how many users per arm?
A) 35,000 B) 88,000 C) 353,000 D) 1.4 million

<details><summary>Answer</summary>

**C.** n = 2·(2.80)²·(0.1·0.9)/0.002² ≈ 353,000. Lehr's rule gives 16·0.09/0.000004 = 360,000. Small relative lifts on low base rates need enormous samples, which is why variance reduction matters so much.
</details>

---

**Q3.** The PM now wants to detect half that lift (+0.1pp). What happens to the required sample?

<details><summary>Answer</summary>

**It quadruples, to about 1.41M per arm.** n ∝ 1/δ², so halving δ multiplies n by 4. Before agreeing, ask whether a 1% relative lift is worth 4× the test duration, or whether a lower-variance metric could do the job.
</details>

---

**Q4.** Same total traffic, but you switch from a 50/50 to a 90/10 split (10% treatment). The MDE:
A) stays the same B) grows about 1.25× C) grows about 1.67× D) grows 9×

<details><summary>Answer</summary>

**C.** The ratio is √((1/0.1 + 1/0.9)/(1/0.5 + 1/0.5)) = √(11.11/4) ≈ 1.67. The small arm dominates the variance. A 90/10 split is still sensible for risky launches, where you want to limit exposure, but you pay for it in power or duration.
</details>

---

**Q5.** You run the test sized for the MDE, but the true effect is only half the MDE. What is the approximate power?
A) 40% B) 29% C) 50% D) 10%

<details><summary>Answer</summary>

**B (≈ 29%).** The true effect is now 1.40 SEs. Power = P(Z > 1.96 − 1.40) = P(Z > 0.56) ≈ 0.29. Power isn't linear in effect size, so it falls off steeply below the MDE, as you saw in homework Part 3.
</details>

---

**Q6.** Going from 80% to 90% power (same α and δ) multiplies the sample size by about:
A) 1.12 B) 1.34 C) 1.5 D) 2

<details><summary>Answer</summary>

**B.** ((1.96 + 1.28)/(1.96 + 0.84))² = (3.24/2.80)² ≈ 1.34. A third more data buys 10 points of power, and teams often decide that isn't worth it.
</details>

---

**Q7.** Why does a 2x2 DiD (repeated cross-section) with the same units have a √2 larger MDE than an A/B test?

<details><summary>Answer</summary>

DiD subtracts **two** noisy differences, post (T − C) minus pre (T − C), so the variances add: Var = 2 × the variance of a single difference. In a **panel** where units are persistent (high ρ), differencing within units cancels the stable part of the noise, and DiD can be *more* precise. That's why `compute_mde(..., rho=0.5, n_pre=4, n_post=4)` gave 0.28 instead of 0.79.
</details>

---

**Q8.** You randomize by city: 40 cities, 5,000 users each, ICC = 0.01. What is the design effect, and the effective sample size?

<details><summary>Answer</summary>

**DEFF = 1 + (5,000 − 1)·0.01 ≈ 51**, so the effective n ≈ 200,000/51 ≈ **3,900 users**. Even a tiny ICC destroys power when clusters are large, which is why geo experiments need methods built for few units (synthetic control or synthetic DiD, week 7). Always analyze at, or cluster by, the randomization unit.
</details>

---

**Q9.** A test finishes "not significant", and a stakeholder asks for the "observed power" to see whether the test was underpowered. What do you say?

<details><summary>Answer</summary>

Observed (post-hoc) power is a one-to-one function of the p-value, so it adds no new information. A non-significant result always gives low observed power. Instead, report the **confidence interval**: it shows which effect sizes the data rule out. Power is a **design-stage** tool. If the CI is wide, the honest conclusion is that the test was inconclusive, not that there's no effect.
</details>

---

**Q10 (interview, answer out loud in 90 seconds).** "We want to test a new onboarding flow. How long should the experiment run?"

<details><summary>Model answer</summary>

"I'd work backwards from the decision. First, agree on the primary metric, say 7-day activation, and the smallest effect worth shipping, with the PM and finance. Then I'd take the baseline rate and variance from historical data, set α = 0.05 and 80% power, and compute the sample per arm, adjusting for the allocation and for variance reduction like CUPED if we have pre-period data. Dividing by eligible daily traffic gives the duration. I'd round up to full weeks to cover day-of-week effects, and run at least one to two weeks to limit novelty effects. If the duration is unacceptable, the levers are a more sensitive metric, variance reduction, a larger MDE, or more traffic. I'd also confirm by simulation if the design is unusual, for example cluster randomization or ratio metrics, and commit to the duration up front, or use a sequential method, to avoid peeking."

**What scores well:** the business-driven MDE, the four quantities, traffic → duration, full weeks/novelty, the levers when it's too long, and no peeking.
</details>

---

### Scoring
| Score | Next step |
|---|---|
| 9–10 | Move on to Day 4 |
| 8 | Pass. Re-read the explanations for the questions you missed |
| ≤ 7 | Re-read lesson §1.2–1.6 and redo homework Parts 1–4, then retake tomorrow |

Record your score in `answers.md`, e.g. `Quiz: 8/10, missed Q5, Q8`.
