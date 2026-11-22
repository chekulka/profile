# Week 2 review quiz (cumulative, Days 9–14)

**Pass mark: 12/15.** No notes. Answer every question on paper before opening any answer.

---

**Q1.** For a Discord test, classify each as goal, driver or guardrail: (a) 90-day retained users, (b) messages sent per active user in week 1, (c) block and report rate, (d) app crash rate.

<details><summary>Answer</summary>

(a) **Goal**, (b) **driver/proxy**, (c) **guardrail** (safety), (d) **guardrail** (quality). (Day 9)
</details>

---

**Q2.** Give one metric that is sensitive but has poor directionality, and explain why.

<details><summary>Answer</summary>

For example, **time spent** (it rises when users are confused), **number of searches** (it rises when results get worse), or **clicks** (they rise with clickbait). It moves easily, but not reliably in the direction of real value. (Day 9)
</details>

---

**Q3.** A proxy metric correlates 0.8 with retention across users. Why isn't that enough to adopt it as a decision metric?

<details><summary>Answer</summary>

A cross-user correlation can come from **confounding**: engaged users score high on both. What matters is whether **treatment effects** on the proxy predict treatment effects on retention, across many past experiments (Netflix's approach). In the Day 9 homework, a "clicks" proxy pointed the wrong way 65% of the time. (Day 9)
</details>

---

**Q4.** A new feature shows +6% in week 1, +3% in week 2 and +2% in week 3. What is likely going on, and what would you check?

<details><summary>Answer</summary>

A **novelty effect** that's decaying toward a smaller long-run effect. Check the effect by day since exposure, compare **new vs. returning users**, run longer or keep a holdout, and report the stabilized effect, not the week-1 number. (Day 10)
</details>

---

**Q5.** Why does every experiment need a fresh hash salt?

<details><summary>Answer</summary>

To avoid **carryover**: if you reuse old buckets, the new arms differ by their history in past experiments (for example, lasting damage from an earlier annoying treatment). That biases even an A/A test (z ≈ −46 in Day 10's homework). (Day 10)
</details>

---

**Q6.** In a ride marketplace with fixed supply, does user-level randomization of a "priority" feature over- or under-state the effect? Which design fixes it?

<details><summary>Answer</summary>

**It overstates it.** Treated riders take rides from control riders, so the comparison measures redistribution, not creation (+39 pp fake vs. 0 true). Fix: **market-level (cluster) randomization or switchbacks**. (Day 10)
</details>

---

**Q7.** 1,000 servers × 200 users each, ICC = 0.05. What is the design effect, and the effective sample size?

<details><summary>Answer</summary>

**DEFF = 1 + 199 × 0.05 ≈ 10.95; effective n ≈ 200,000/10.95 ≈ 18,300 users.** Cluster randomization removes interference bias but costs a lot of power, so pair it with variance reduction. (Days 3, 10)
</details>

---

**Q8.** An experiment reports 15 independent metrics with no true effects, at α = 0.05. What is P(at least one significant)?

<details><summary>Answer</summary>

**≈ 54%** (1 − 0.95¹⁵ = 0.537). (Day 11)
</details>

---

**Q9.** p-values 0.004, 0.02, 0.025, 0.30 (m = 4). How many are rejected at 0.05 by Bonferroni, and by BH?

<details><summary>Answer</summary>

**Bonferroni: 1** (threshold 0.0125). **BH: 3**, using thresholds 0.0125, 0.025, 0.0375, 0.05: 0.004 ✓, 0.02 ✓, 0.025 ✓, 0.30 ✗. (Day 11)
</details>

---

**Q10.** Cov(Y, X) = 6 and Var(X) = 8. What is the CUPED θ?

<details><summary>Answer</summary>

**θ = 0.75.** (Day 12)
</details>

---

**Q11.** corr(X, Y) = 0.6. What share of the variance is kept, how much does the MDE shrink, and how long does a 5-week test now take?

<details><summary>Answer</summary>

**64% of the variance is kept** (1 − 0.36), the **MDE shrinks by 20%** (√0.64 = 0.8), and the test takes about **0.64 × 5 ≈ 3.2 weeks**. (Day 12)
</details>

---

**Q12.** Which covariates are valid for CUPED? (a) last month's sessions, (b) sessions in the experiment's first week, (c) signup country, (d) whether the user clicked the new button.

<details><summary>Answer</summary>

**(a) and (c).** Both are fixed before treatment. (b) and (d) can be affected by treatment, so adjusting for them risks bias. (Days 12–13)
</details>

---

**Q13.** When can ANCOVA (a common slope, no interaction) be less precise than no adjustment, and what fixes it?

<details><summary>Answer</summary>

With **unequal allocation and heterogeneous slopes by arm** (Freedman's critique). The fix is **Lin's estimator**: center X, include T × X, and use robust SEs, which is never worse asymptotically (Day 13 homework: SD 0.27 vs. 0.19 unadjusted vs. 0.18 Lin). (Day 13)
</details>

---

**Q14.** Treatment increases sessions, and sessions increase revenue. What happens if you "control for sessions" when estimating the revenue effect?

<details><summary>Answer</summary>

You remove the effect that works through sessions. Sessions are a **mediator** (a bad control), so the estimate collapses toward 0 (Day 13: +$6 became −$0.07). Only adjust for pre-treatment variables. (Day 13)
</details>

---

**Q15 (interview, answer out loud in 3 minutes).** "Discord wants to test a feature that suggests channels to join inside a server. Traffic is limited, results are needed in 3 weeks, and leadership cares about long-term retention. Design the experiment and the analysis."

<details><summary>Model answer (pulls together the whole week)</summary>

"**Unit and interference:** suggestions change where people talk, so treated users affect control users in the same server. I'd randomize at the **server level**, accepting the power cost. **Metrics:** the goal is long-term retention, which is too slow for 3 weeks, so the decision metric is a **validated driver**, such as days active in week 2–3 or members joining at least one new channel. I'd check on past server-level experiments that it actually predicts retention. Guardrails: notification opt-outs, leave-server rate, reports and blocks, and latency. **Power:** compute the design effect from historical server-level variance. To fit 3 weeks, use **CUPED or Lin-style adjustment** with server-level pre-period activity, cap heavy-tailed metrics, and keep the primary metric single and pre-registered. **Time effects:** suggestions are novel, so plot the effect by day, compare new vs. established servers, and keep a **small long-term holdout** to confirm the retention impact. **Analysis:** SRM check at the server level first, ratio metrics with the delta method at the server level, **BH** for the secondary and exploratory metrics, and a readout whose TL;DR gives the decision, the range, and the guardrails' upper bounds."

**What scores well:** spotting interference, a cluster design, a validated proxy for a slow goal, variance reduction to meet the deadline, novelty plus a holdout, and a validity-first analysis with a multiplicity plan. That's Staff-level coverage.
</details>

---

### Scoring
| Score | Next step |
|---|---|
| 14–15 | Week 2 mastered 🏹 On to the rest of Week 3 |
| 12–13 | Pass. Revisit the days for the questions you missed |
| ≤ 11 | Spend next weekend re-doing the days you missed |

Record your score in `learning/day15/answers.md`, e.g. `Week 2 review: 13/15, missed Q7, Q13`.
