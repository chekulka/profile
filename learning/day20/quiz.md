# Day 20 quiz: always-valid inference

**Pass mark: 8/10.** Answer on paper first, then open the answers.

---

**Q1.** What does "always-valid" mean for a p-value?

<details><summary>Answer</summary>

For **any** stopping rule, including stopping whenever you like after looking continuously, P(p_T ≤ α) ≤ α under H₀. Ordinary p-values only guarantee this at the single pre-planned sample size.
</details>

---

**Q2.** In the mSPRT, what is "mixed" over, and why?

<details><summary>Answer</summary>

The likelihood ratio is **averaged over a prior distribution of effect sizes** δ ~ N(0, τ²), instead of testing one specific alternative. That makes the test sensitive to a range of effects, and gives a statistic Λ_n that's a **martingale under H₀**, which is the property behind its validity.
</details>

---

**Q3.** Why can't Λ_n reach 1/α with probability more than α under H₀?

<details><summary>Answer</summary>

Under H₀, Λ_n is a **nonnegative martingale starting at 1**. **Ville's inequality** says the chance it *ever* exceeds 1/α is at most α. That's a bound over the whole infinite path, which is why stopping at any time is safe.
</details>

---

**Q4.** In the homework, under continuous monitoring, the naive z-test had a false positive rate of 56% and the mSPRT 2.2%. Why is the mSPRT's rate *below* 5%?

<details><summary>Answer</summary>

Ville's inequality is a **conservative upper bound**: the martingale often doesn't reach exactly 1/α, and the test is horizon-free, designed for infinitely long monitoring. Over a finite horizon (2,000 steps), the realized error rate is below α. The flip side is lost power.
</details>

---

**Q5.** What is a confidence sequence, and how does it differ from a confidence interval?

<details><summary>Answer</summary>

A **sequence of intervals** (one per n) that covers the true effect **at all n simultaneously** with probability ≥ 1 − α. A 95% CI covers the truth only at a single, pre-chosen n. Checked at every step, the usual CI's uniform coverage collapsed to 44% in the homework, while the confidence sequence held 97.8%.
</details>

---

**Q6.** What is the cost of always-valid inference, in numbers from the homework?

<details><summary>Answer</summary>

At the same maximum sample (2,000 pairs): **power 45% vs. 71%** for a single fixed look, and intervals **about 1.55× wider** at the end. Flexibility isn't free. You pay in power or in sample size.
</details>

---

**Q7.** How does the mixing parameter τ² affect the mSPRT?

<details><summary>Answer</summary>

τ² sets **which effect sizes the test is most powerful for**. Choose it near the effects you realistically expect (often estimated from historical experiments). Too large wastes power on implausibly big effects; too small makes the test slow to detect real ones. Validity holds for any τ².
</details>

---

**Q8.** Match each team to a method: (a) a team with daily batch metrics that wants early stopping for big wins, (b) an ops team watching a latency guardrail in real time, (c) a disciplined team with plenty of traffic.

<details><summary>Answer</summary>

(a) **Group sequential with OBF spending** (Day 19). (b) **Always-valid**: an mSPRT or confidence sequence on the guardrail. (c) A **fixed-horizon test** with a pre-registered duration, which has the most power and is simplest. Matching the method to how people actually look is the platform DS's job.
</details>

---

**Q9.** Is the always-valid p-value allowed to increase over time?

<details><summary>Answer</summary>

**No.** It's defined as the running minimum of 1/Λ_m (capped at 1), so it only goes down or stays flat. Once evidence has been seen, it isn't "unseen", which is what makes stopping at any time consistent.
</details>

---

**Q10 (interview, answer out loud in 90 seconds).** "Product teams refuse to stop peeking at dashboards. Should we switch the whole platform to always-valid p-values?"

<details><summary>Model answer</summary>

"Always-valid inference fixes the false-positive problem whatever the monitoring behavior, which is exactly what you want when teams peek. With an mSPRT or confidence sequences, the error rate stays at 5% even if they look every minute. But it costs power: in a simulation I ran, about 45% vs. 71% at the same sample size, and intervals about 1.5× wider. So I wouldn't make it the only option. I'd make it the default for **monitoring views and guardrails**, where continuous looks are natural and catching harm early matters, and use **group sequential with O'Brien-Fleming** for decision metrics on our daily pipeline, which allows early stops with almost no power loss. Teams that run to a planned duration could keep fixed-horizon tests. I'd tune τ² from historical effect sizes, validate everything with A/A tests under realistic peeking, and show only adjusted p-values and intervals in the UI, so peeking stops being dangerous."

**What scores well:** acknowledging the benefit, quantifying the cost, a mixed policy matched to use cases, tuning τ², validation, and the UI design.
</details>

---

### Scoring
| Score | Next step |
|---|---|
| 9–10 | Move on to Day 21 |
| 8 | Pass. Re-read the explanations for the questions you missed |
| ≤ 7 | Re-read lesson §1.2–1.4 and Johari et al. §3, then retake tomorrow |

Record your score in `answers.md`, e.g. `Quiz: 9/10, missed Q3`.
