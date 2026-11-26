# Day 19 quiz: group sequential designs

**Pass mark: 8/10.** Answer on paper first, then open the answers.

---

**Q1.** What does an alpha-spending function α(t) specify?

<details><summary>Answer</summary>

The **cumulative share of the total Type I error (α) that may be used** by information fraction t, the share of the planned sample collected. α(0) = 0 and α(1) = α. The boundaries at each look are derived from it, so the overall false positive rate stays at α however many looks happen.
</details>

---

**Q2.** Write the O'Brien-Fleming-type spending function, and say roughly how much α it spends at t = 0.25 for α = 0.05.

<details><summary>Answer</summary>

**α(t) = 2 − 2Φ(z₁₋α/₂/√t).** At t = 0.25, z/√t = 1.96/0.5 = 3.92, so α(0.25) = 2 − 2Φ(3.92) ≈ **0.0001**. Almost nothing is spent early, which is why the first boundary is so strict (|z| ≈ 3.9).
</details>

---

**Q3.** Why does the O'Brien-Fleming design lose almost no power compared with a fixed-sample test?

<details><summary>Answer</summary>

It saves almost all of α for the final look, so the **final boundary (≈ 2.04) is close to the fixed-sample 1.96**. Early looks only stop for overwhelming evidence, which barely costs anything. Homework: 79% vs. 80% power, while still allowing early stops (expected sample 81% of the maximum).
</details>

---

**Q4.** Pocock's boundaries are roughly constant (about 2.37 for 4 looks). What's the advantage, and what's the cost?

<details><summary>Answer</summary>

**Advantage:** earlier stopping on average (expected sample 72% vs. 81% for OBF) when effects are real. **Cost:** a stricter final boundary (2.35), so **more power is lost** (72% vs. 79%), and an early stop at p ≈ 0.018 is less convincing to stakeholders.
</details>

---

**Q5.** You planned 4 looks, but for operational reasons you can only look at 30%, 60% and 100%. Is the Lan-DeMets approach still valid?

<details><summary>Answer</summary>

**Yes.** This is a key advantage of alpha spending: compute the α spent at the *actual* information fractions (0.3, 0.6, 1.0) from the same function, and derive the boundaries from those. The overall α stays controlled, as long as you don't choose the timing of looks *based on* the observed results.
</details>

---

**Q6.** Which data setting suits group sequential tests best: streaming data looked at every minute, or daily batch updates?

<details><summary>Answer</summary>

**Daily (or other batch) updates.** Group sequential designs were built for a small number of planned interim analyses, like medical trials with batches of data, which is why Spotify uses them with daily pipelines. For truly continuous monitoring, always-valid methods (mSPRT, confidence sequences; Day 20) fit better.
</details>

---

**Q7.** Your OBF test stops at the second look with |z| = 2.9. Is the reported effect estimate unbiased?

<details><summary>Answer</summary>

**No, it's biased upward** (the winner's curse). Stopping *because* the estimate crossed a high boundary selects the overestimates. The test decision (the effect isn't zero) is valid, but report the effect size with caution, use bias-adjusted estimates, or keep collecting data on a holdout for a cleaner estimate.
</details>

---

**Q8.** True or false: with group sequential designs, you no longer need to plan a sample size.

<details><summary>Answer</summary>

**False.** You need a planned **maximum** sample size (or maximum information) to compute the information fractions t, and to size the test for the target power. Sequential designs let you stop *before* the maximum; they don't remove the need for a power analysis.
</details>

---

**Q9.** What is a futility boundary, and what is the rule for using one?

<details><summary>Answer</summary>

A boundary for stopping early when the result is **unlikely to become significant**, which saves traffic on losing ideas. It must be **pre-specified** (binding or non-binding), because adding an ad-hoc futility stop changes the design's error properties and power. Non-binding futility boundaries are a common, safe choice.
</details>

---

**Q10 (interview, answer out loud in 2 minutes).** "Design a sequential testing policy for our experimentation platform so teams can stop early safely."

<details><summary>Model answer</summary>

"I'd make a **group sequential design with Lan-DeMets O'Brien-Fleming spending** the default for success metrics. It fits our daily batch pipeline, costs about 1% power versus a fixed-horizon test, and still allows early stops for large effects. Each experiment pre-registers a **maximum sample size** from the power analysis, and the platform computes the information fraction at each daily look and shows **boundary-adjusted** results only, never raw p-values for success metrics. For **guardrails**, I'd use a stricter harm-detecting sequential rule, perhaps always-valid inference, so we can stop for harm at any time. **Futility** stops are optional, non-binding and pre-specified. For teams that need continuous monitoring, like real-time ops, we'd offer **always-valid confidence sequences** (mSPRT). Readouts would flag that effect sizes at early stops are biased upward. Finally, I'd validate the whole policy with simulated and real A/A tests to confirm the false positive rate stays at 5% under the actual monitoring patterns."

**What scores well:** the right default (OBF spending) with reasoning (batch data, small power cost), operational details (max sample, information fraction, adjusted displays), separate guardrail and futility handling, an always-valid option, winner's-curse awareness, and validation.
</details>

---

### Scoring
| Score | Next step |
|---|---|
| 9–10 | Move on to Day 20 |
| 8 | Pass. Re-read the explanations for the questions you missed |
| ≤ 7 | Re-read lesson §1.2–1.3 and the Spotify post, then retake tomorrow |

Record your score in `answers.md`, e.g. `Quiz: 9/10, missed Q5`.
