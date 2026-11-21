# Day 14 quiz: putting the pipeline together

**Pass mark: 8/10.** Answer on paper first, then open the answers.

---

**Q1.** Why should an analyzer *refuse* to show metric results when the SRM check fails, instead of showing them with a warning?

<details><summary>Answer</summary>

With an SRM, the arms aren't comparable, so the effects are **biased in an unknown direction**. Numbers on a dashboard get screenshotted and acted on whatever warning sits next to them. Withholding them forces the right next step (debug, fix, re-run) and protects trust in the platform.
</details>

---

**Q2.** Put these in pipeline order: BH correction, SRM check, CUPED, decision rule, delta-method SEs.

<details><summary>Answer</summary>

**SRM check → CUPED and delta-method SEs (estimation) → BH correction → decision rule.** Validity first, then correct estimates and SEs, then adjust the final p-values for multiplicity, and finally apply the pre-registered decision rule.
</details>

---

**Q3.** In the clean experiment, why is "sessions per user" adjusted with CUPED but "CTR" handled with the delta method?

<details><summary>Answer</summary>

They solve different problems. **CUPED** reduces *variance* using pre-period data (sessions has a strong pre-period predictor). The **delta method** fixes the *SE* of a **ratio metric** whose denominator (sessions) is random and correlated with the numerator within a user. You can combine them too: CUPED for ratio metrics exists (Deng et al.'s delta-method paper covers it).
</details>

---

**Q4.** The CTR estimate is +0.0089 with SE ≈ 0.0018, while the true effect is +0.005. Is the analyzer broken?

<details><summary>Answer</summary>

**Probably not.** The gap is (0.0089 − 0.005)/0.0018 ≈ **2.2 SEs**, which happens by chance about 3% of the time for any one metric, and more often when you look at several metrics. The right check is **simulation**: run many A/A and A/B datasets and confirm the coverage is about 95% and the false positive rate about 5% (Days 3 and 7). One miss is evidence of nothing; systematic misses are.
</details>

---

**Q5.** Why is revenue capped at p99 before testing?

<details><summary>Answer</summary>

Revenue has a **heavy tail**: a few whales dominate the variance and kill power (Day 9: 12% vs. 39% power), and its CIs under-cover at moderate n (Day 2). Capping trades a little bias (orders above the cap count as the cap) for a large variance reduction. The cap must be **pre-registered**.
</details>

---

**Q6.** The primary metric is significant, a secondary metric isn't, and a guardrail's CI includes harm above its threshold. What should the TL;DR say?

<details><summary>Answer</summary>

Don't just say "SHIP". Something like: **"Primary metric up X (CI …); guardrail Y inconclusive: we can't rule out harm up to Z, above our limit. Recommend extending the test (or ramping with monitoring) before full launch."** A guardrail's upper bound can veto or delay a launch even when the primary metric wins (Day 5).
</details>

---

**Q7.** True or false: if every metric's method passes A/A tests individually, the platform needs no multiple-testing correction.

<details><summary>Answer</summary>

**False.** A/A calibration means each *individual* test has a 5% false positive rate. With many metrics, the chance that *some* metric shows a false win still grows: 64% with 20 metrics (Day 11). Calibration and multiplicity are separate problems; you need both.
</details>

---

**Q8.** Name two things an analyzer should compute on the *pre-period* data, and why.

<details><summary>Answer</summary>

(1) **CUPED covariates** (pre-period metrics) for variance reduction. (2) A **pre-period balance check**: the arms should look the same *before* treatment, and an imbalance suggests an assignment bug or carryover (Day 10). Some platforms also run a "pre-period A/A" on the experiment's own users.
</details>

---

**Q9.** How would you test this analyzer itself, as software?

<details><summary>Answer</summary>

**Simulation-based tests:** (1) A/A datasets should give about 5% false positives per metric and uniform p-values; (2) A/B datasets with known effects should give about 95% CI coverage and the expected power; (3) injected SRM bugs should trigger STOP; (4) edge cases such as zero revenue, single-session users and missing pre-period data shouldn't crash. Put these in CI so every code change is checked.
</details>

---

**Q10 (interview, answer out loud in 2 minutes).** "Walk me through what our stats engine should do, from raw logs to a launch decision."

<details><summary>Model answer</summary>

"Before any statistics: **data quality and validity**. Join assignments to exposures and outcomes, check for missing logs, run the **SRM check**, and check pre-period balance. If SRM fails, we stop and show nothing but the diagnosis. Then **estimation**: compute each metric at the randomization unit, use the **delta method** for ratio metrics, **cap** heavy-tailed metrics with pre-registered thresholds, and apply **CUPED or regression adjustment** with pre-period covariates. Then **inference**: robust SEs, CIs for absolute and relative effects, **sequential-testing-safe** p-values if people look early, and a **multiple-testing correction** across success metrics, with exploratory metrics marked as such. Finally, the **decision layer**: the pre-registered primary metric and guardrail thresholds produce a recommendation, written as a readout with the TL;DR first. And the engine validates itself continuously with **A/A tests and simulations** in CI, so we can show it deserves trust."

**What scores well:** validity → estimation → inference → decision, each step with the right method, self-validation, and the readout. That's exactly what today's analyzer does.
</details>

---

### Scoring
| Score | Next step |
|---|---|
| 9–10 | Week 2 project done 🎉 Sunday review next |
| 8 | Pass. Re-read the explanations for the questions you missed |
| ≤ 7 | Revisit the day each missed question came from |
