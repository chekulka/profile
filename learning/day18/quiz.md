# Day 18 quiz: the peeking problem

**Pass mark: 8/10.** Answer on paper first, then open the answers.

---

**Q1.** What exactly is "peeking", and why does it break a fixed-horizon test?

<details><summary>Answer</summary>

Looking at results repeatedly during a test **and stopping (or deciding) the first time it's significant**. A fixed-horizon test's 5% guarantee assumes a single look at a planned sample size. Each extra look is another chance for noise to cross the threshold, so the overall false positive rate rises.
</details>

---

**Q2.** A/A tests peeked at daily for 28 days, stopping at the first p < 0.05. Roughly what is the false positive rate?

<details><summary>Answer</summary>

**About 25–30%** (your simulation: 27.8%), more than five times the nominal 5%. Evan Miller's essay reports a similar figure (about 26%).
</details>

---

**Q3.** A team ships whenever its daily dashboard turns green. Over 40 features that actually do nothing, about how many get shipped as "wins"?

<details><summary>Answer</summary>

**About 11** (40 × 0.28), compared with about 2 under a single planned look. That's how teams end up with a long list of "wins" that don't add up to any real metric growth.
</details>

---

**Q4.** Why does the cumulative z-statistic behave like a random walk?

<details><summary>Answer</summary>

Each day adds new independent data, so the cumulative sum of evidence moves up and down randomly, and the z-statistic is that sum rescaled. Under the null it drifts around zero but wanders widely over time, and given enough looks it will eventually cross ±1.96 (by the law of the iterated logarithm, in the limit it always does).
</details>

---

**Q5.** You apply Bonferroni across 28 daily looks (critical |z| ≈ 3.12). The false positive rate drops to about 1.7%. Why so far below 5%, and what's the cost?

<details><summary>Answer</summary>

Bonferroni assumes the worst case, with no correlation between tests. But daily looks are **highly correlated**, since day 20's data includes day 19's, so the correction overshoots. The cost is **lost power**: real effects need much stronger evidence. Alpha-spending designs (Day 19) use the correlation to spend α more efficiently.
</details>

---

**Q6.** When you stop at the first significant look, why is the reported effect exaggerated?

<details><summary>Answer</summary>

You stop *because* the estimate just hit a high point, which is often a random upward fluctuation. Conditioning on significance selects the overestimates. Homework: about 3× the true effect for a small effect. It's the **winner's curse**, and it also appears when picking the best of many variants or metrics.
</details>

---

**Q7.** Is it OK to look at the dashboard daily during a fixed-horizon test?

<details><summary>Answer</summary>

**Yes, as long as you don't change the decision based on it.** Daily monitoring for **bugs, SRM, logging problems or severe harm** is good practice. The problem is stopping early or declaring victory on a significant interim p-value without a sequential method.
</details>

---

**Q8.** A guardrail (crash rate) spikes badly on day 2. Should you stop the test?

<details><summary>Answer</summary>

**Yes, for user protection,** ideally under a **pre-specified harm-stopping rule** (for example, a strict sequential boundary for guardrails). Stopping for safety is different from stopping for a win. You don't conclude "the feature is bad by X%"; you stop the exposure, investigate, and fix it.
</details>

---

**Q9.** Which of these does NOT fix the peeking problem?
A) Pre-registering the duration and looking once
B) Group sequential tests with alpha spending
C) Always-valid p-values (mSPRT)
D) Switching to a two-sided test

<details><summary>Answer</summary>

**D.** A two-sided test still assumes a single look. A–C all control the false positive rate under the planned (B) or arbitrary (C) monitoring scheme. (Bayesian methods are discussed on Day 21: they answer a different question and aren't automatically immune.)
</details>

---

**Q10 (interview, answer out loud in 90 seconds).** "Our PM wants to stop a test on day 4 because it's already significant. What do you say?"

<details><summary>Model answer</summary>

"I'd explain that the significance on day 4 isn't the same as significance at the planned end. Our test assumes we look once. Checking daily and stopping at the first green raises our false positive rate from 5% to roughly 25–30%, and early stops also **exaggerate the effect**, often several-fold, which would inflate our impact forecasts. There's also a practical reason: 4 days doesn't cover a full weekly cycle or let novelty effects wear off. So my recommendation is to run to the planned duration. If speed matters, the right fix is to switch our platform to a **sequential method**: group sequential with O'Brien-Fleming boundaries, or always-valid p-values. Then we *can* stop early legitimately when the evidence is truly strong. In the meantime, we keep monitoring guardrails daily and would stop immediately for harm."

**What scores well:** quantifying the inflation, the winner's curse, weekly cycles and novelty, a clear recommendation, a constructive alternative (sequential testing), and the harm exception.
</details>

---

### Scoring
| Score | Next step |
|---|---|
| 9–10 | Move on to Day 19 |
| 8 | Pass. Re-read the explanations for the questions you missed |
| ≤ 7 | Re-read lesson §1.1–1.4 and Evan Miller's essay, then retake tomorrow |

Record your score in `answers.md`, e.g. `Quiz: 9/10, missed Q5`.
