# Day 11 quiz: multiple testing

**Pass mark: 8/10.** Answer on paper first, then open the answers.

---

**Q1.** An A/A test reports 10 independent metrics at α = 0.05. What is the chance at least one is "significant"?

<details><summary>Answer</summary>

**≈ 40%.** 1 − 0.95¹⁰ = 0.401. With 20 metrics it's about 64%, as you simulated. That's why "one metric moved" means little unless it was the pre-registered primary metric.
</details>

---

**Q2.** You test 20 metrics. What is the Bonferroni per-test threshold for FWER = 0.05?

<details><summary>Answer</summary>

**0.0025** (0.05/20). Bonferroni is simple and controls FWER under any dependence, but it's conservative, so you'll miss real effects when m is large.
</details>

---

**Q3.** p-values (m = 5): 0.001, 0.012, 0.03, 0.04, 0.20. Which are rejected at α = 0.05 by (a) Bonferroni, (b) Holm, (c) Benjamini-Hochberg?

<details><summary>Answer</summary>

**(a) Bonferroni:** threshold 0.01, so only 0.001. **(b) Holm:** compare in order with α/5, α/4, α/3, …: 0.001 ≤ 0.01 ✓, 0.012 ≤ 0.0125 ✓, 0.03 > 0.0167 ✗ and stop, so **2** rejections. **(c) BH:** thresholds 0.01, 0.02, 0.03, 0.04, 0.05; the largest k with p₍ₖ₎ ≤ threshold is k = 4 (0.04 ≤ 0.04), so the **4 smallest** are rejected. Same data: 1 vs. 2 vs. 4 discoveries.
</details>

---

**Q4.** In one sentence each: what do FWER and FDR control?

<details><summary>Answer</summary>

**FWER:** the probability of making **even one** false positive across all tests. **FDR:** the expected **fraction of rejections that are false**. With FDR at 5%, about 1 in 20 of your "discoveries" will be wrong, but you'll find more real effects.
</details>

---

**Q5.** Which correction fits an exploratory dashboard of 80 metrics × segments, and why?

<details><summary>Answer</summary>

**BH (FDR control).** The goal is to surface promising leads while keeping the share of junk low. FWER control would be so strict that you'd find almost nothing (homework: 32% vs. 50% power). Label the findings exploratory and **confirm them in a new experiment** before acting.
</details>

---

**Q6.** In the homework, why did "no correction" have an FDR of about 33% even though each test used α = 0.05?

<details><summary>Answer</summary>

There were **90 null** and 10 real hypotheses. About 0.05 × 90 ≈ 4.5 false rejections plus about 8.5 true ones means roughly **4.5/13 ≈ 33%** of rejections are false. When most hypotheses are null, per-test α says little about the share of your discoveries that are wrong.
</details>

---

**Q7.** The launch decision uses one pre-registered primary metric. Do you need a multiple-testing correction for it?

<details><summary>Answer</summary>

**No**, not for that single decision test, as long as it really was chosen before the test and isn't swapped afterwards. Corrections are needed when you have **multiple chances to win**: several success metrics, many segments, or picking the best of many variants.
</details>

---

**Q8.** Guardrails: should you apply a strict Bonferroni correction to 10 guardrail metrics?

<details><summary>Answer</summary>

**Usually not strictly.** For guardrails, the expensive mistake is **missing real harm** (a false negative). Over-correcting makes harm harder to detect. Common practice is to test each guardrail for harm, make sure the test has **enough power** for the harm threshold, and look at the CI's upper bounds (Day 5). Spotify treats success metrics and guardrails differently for exactly this reason.
</details>

---

**Q9.** "No overall effect, but Android users in Canada show p = 0.01!" What is your response?

<details><summary>Answer</summary>

Ask **how many segments were looked at**. With 12 segments, there's a 46% chance that one is significant by luck. Apply a correction for the number of segments, check whether there's a plausible mechanism, and if it still matters, **replicate it in a test targeted at that segment**. Don't launch to the segment based on this result alone.
</details>

---

**Q10 (interview, answer out loud in 90 seconds).** "Our dashboard shows 200 metrics per experiment. Teams keep shipping features because 'some metrics went green'. As a Staff DS, how do you fix this?"

<details><summary>Model answer</summary>

"It's a multiple-testing problem dressed up as a culture problem. First, every experiment **pre-registers one primary metric**, or a small OEC, plus its guardrails and decision rule, and the platform enforces it: the readout leads with those, not the 200. Second, **tiered corrections**: success metrics corrected for their number, guardrails tested for harm with enough power, and the other 190 shown as **exploratory with BH/FDR control** and labeled as hypotheses. Third, the UI stops showing raw green/red p-values for exploratory metrics, and shows effect sizes with corrected intervals instead. Fourth, education plus a quick A/A demo: show teams that even an A/A test 'wins' on about 10 metrics out of 200. Finally, I'd track the platform's replication rate: when we re-test 'wins', how many hold up? That makes the problem visible and the fix measurable."

**What scores well:** pre-registration, tiered treatment of primary, guardrail and exploratory metrics, product and UI changes, education with evidence, and a measurable outcome (replication rate). That's Staff-level platform thinking.
</details>

---

### Scoring
| Score | Next step |
|---|---|
| 9–10 | Move on to the Week 2 weekend project |
| 8 | Pass. Re-read the explanations for the questions you missed |
| ≤ 7 | Re-read lesson §1.1–1.4, redo homework Part 2, then retake tomorrow |

Record your score in `answers.md`, e.g. `Quiz: 9/10, missed Q3`.
