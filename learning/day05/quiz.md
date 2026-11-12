# Day 5 quiz: communicating results

**Pass mark: 8/10.** Answer on paper first, then open the answers.

---

**Q1.** What belongs in the first 3 lines of an experiment readout?
A) Methodology and sample sizes
B) The recommendation, the headline effect with a range, and the biggest risk
C) The p-value table
D) Background on why the feature was built

<details><summary>Answer</summary>

**B.** Executives decide from the TL;DR. Lead with the decision and the evidence, including uncertainty, and leave method details for further down. A failed validity check (like an SRM) belongs in those first three lines too.
</details>

---

**Q2.** Planned split 50/50, observed 100,480 vs 99,520 users. Is that a sample ratio mismatch? Show your reasoning.

<details><summary>Answer</summary>

**Yes (p ≈ 0.03).** Expected 100,000 each, so χ² = (480² + 480²)/100,000 = 4.61 with 1 degree of freedom, p ≈ 0.032. A 0.5-point imbalance looks small, but with 200K users it's very unlikely to happen by chance. Something non-random affected who got counted, and the results can't be trusted until you find the cause. (Week 2 goes deep on this.)
</details>

---

**Q3.** The guardrail "support calls" shows +3.6% (95% CI −1.6% to +8.8%, p = 0.18). The limit is +5%. What do you report?

<details><summary>Answer</summary>

**Inconclusive, not safe.** The CI includes increases up to +8.8%, above the +5% limit, so we can't rule out unacceptable harm. Report the upper bound, and either collect more data (power the test for the guardrail) or decide explicitly whether that risk is acceptable. "Not significant" only means we couldn't detect a difference; it isn't evidence of no difference.
</details>

---

**Q4.** Which sentence correctly describes p = 0.000015 to a VP?
A) "We're 99.998% sure the feature works."
B) "If the feature had no effect, a result this large would almost never happen by chance."
C) "The effect is huge."
D) "There's a 0.0015% chance we're wrong."

<details><summary>Answer</summary>

**B.** A p-value is computed assuming no effect. A and D convert it into the probability of a hypothesis, which it isn't. C confuses significance with size: a tiny effect can have a tiny p-value with a huge sample. Better still, lead with the effect and its CI.
</details>

---

**Q5.** What is Twyman's law, and what should you do when a result looks spectacular?

<details><summary>Answer</summary>

*"Any figure that looks interesting or different is usually wrong."* When a result is unusually large, check harder: SRM, logging and instrumentation, bugs, bots, novelty effects, metric definitions. Then consider **replicating** before a big launch. Netflix notes that surprising results more often come from errors or false positives than from real effects.
</details>

---

**Q6.** A stakeholder points out that "Day 3 alone showed +6%!" How do you respond?

<details><summary>Answer</summary>

Single-day results are noisy and subject to day-of-week and novelty effects. Picking the best day out of 14 is a form of **multiple testing and peeking**, which inflates false positives. The pre-registered analysis over the full duration is the estimate. Daily charts are for spotting bugs and trends, not for picking the result.
</details>

---

**Q7.** Report this as absolute and relative effects: control completion 31.0%, treatment 31.9%, diff CI [+0.49, +1.31] pp.

<details><summary>Answer</summary>

**Absolute: +0.90 percentage points (95% CI +0.49 to +1.31 pp). Relative: +2.9% (95% CI about +1.6% to +4.2%).** Report both. "Points" and "percent" are different things, and mixing them up is a classic credibility killer in executive reviews. Compute the relative CI with the delta method (Day 4).
</details>

---

**Q8.** The primary metric is strongly positive, but there's an SRM. What's the right recommendation?
A) Ship; the effect is big enough to survive any bias
B) Don't ship yet: find the SRM's cause, fix it, re-run (or show the bias can't explain the result), then decide
C) Ignore the SRM; it's only 0.5%
D) Kill the feature

<details><summary>Answer</summary>

**B.** An SRM means the treatment and control populations differ in a non-random way (for example, the feature crashed the app for some users, who then dropped out of the logs). The bias could be in either direction and of any size, so you can't assume the effect survives it. Diagnose first. Killing the feature (D) throws away a promising signal.
</details>

---

**Q9.** How do you adapt the same result for (a) the CEO, (b) the PM, and (c) a fellow data scientist?

<details><summary>Answer</summary>

(a) **CEO:** the decision, business impact in dollars or users, and risk, in a couple of sentences. (b) **PM:** the decision, effects on primary and guardrail metrics, the segments that matter, and next steps for the product. (c) **Data scientist:** the full design, validity checks, estimator, variance method, robustness checks and caveats. The numbers are the same; the depth and the vocabulary differ.
</details>

---

**Q10 (interview, answer out loud in 90 seconds).** "Tell me about a time you had to communicate a complicated or unwelcome experiment result to leadership."

<details><summary>Model answer structure (fill it with your own story)</summary>

Use **STAR**. Candidates from your resume:
- **Vanguard:** the standardized review process. A test that looked like a win but failed a validity check, or one where you recommended against shipping.
- **Deloitte:** a non-inferiority rollout phase where you recommended holding at 20% traffic.

**Situation:** the stakes and the audience. **Task:** what decision was needed. **Action:** how you framed it: the decision first, uncertainty in plain language, a visual, the options with their risks, and a recommendation. **Result:** what leadership decided and what happened afterwards, with a number. End with what you learned, for example that you now include guardrail upper bounds in every TL;DR.

**What interviewers look for:** clarity under pressure, intellectual honesty (you didn't spin the result), and influence (people acted on your recommendation).
</details>

---

### Scoring
| Score | Next step |
|---|---|
| 9–10 | Week 1 done. Weekend project next |
| 8 | Pass. Re-read the explanations for the questions you missed |
| ≤ 7 | Re-read lesson §1.1–1.4 and the Netflix posts, then retake tomorrow |

Record your score in `answers.md`, e.g. `Quiz: 9/10, missed Q2`.
