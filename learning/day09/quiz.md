# Day 9 quiz: metric design

**Pass mark: 8/10.** Answer on paper first, then open the answers.

---

**Q1.** Classify each as goal, driver or guardrail for a chat product: (a) page load latency, (b) 6-month retained users, (c) 7-day sessions with a successful answer, (d) safety-policy violations.

<details><summary>Answer</summary>

(a) **Guardrail**, (b) **goal (north star)**, (c) **driver/proxy**, (d) **guardrail**. Goals are what the business ultimately wants but move slowly. Drivers move quickly and predict the goal. Guardrails must not get worse, whatever the goal does.
</details>

---

**Q2.** What is the OEC, and why pre-commit to it?

<details><summary>Answer</summary>

The **overall evaluation criterion**: the metric, or weighted combination of metrics, that decides ship or no-ship. Committing in advance prevents **cherry-picking** (choosing after the fact whichever of 50 metrics looks good), a form of multiple testing that inflates false wins.
</details>

---

**Q3.** In the homework, the same 8% increase in buyers was detected 73% of the time by conversion but only 12% of the time by revenue. Why?

<details><summary>Answer</summary>

Revenue per user has **huge variance**: most users spend 0 and a few whales spend a lot. The signal (more buyers) is the same, but the noise is much larger, so power collapses. Conversion is a 0/1 metric with low, bounded variance.
</details>

---

**Q4.** You cap revenue at the 90th percentile of order value. What do you gain, what do you lose, and what must you do beforehand?

<details><summary>Answer</summary>

**Gain:** much lower variance, so more power (12% → 39% in the homework). **Lose:** the estimand changes, because effects on very large orders are understated. **Beforehand:** pre-register the cap (or the rule for computing it), so you can't choose it after seeing the results.
</details>

---

**Q5.** Give an example of a metric that is sensitive but has poor directionality.

<details><summary>Answer</summary>

**Time on page / time in app** (it can rise because users are confused or stuck), **clicks** (rise with clickbait or extra steps), or **number of searches** (rises when search results get *worse*). They move easily but don't reliably move in the direction of real value. Pair them with success-based metrics.
</details>

---

**Q6.** A metric correlates 0.9 with retention **across users**. Is it validated as a proxy for experiments?

<details><summary>Answer</summary>

**No.** A cross-user correlation shows that engaged users score high on both, which could just be confounding. For experiments, what matters is whether **treatment effects** on the proxy predict **treatment effects** on retention, across many past experiments. Validate it with historical experiments, as Netflix does.
</details>

---

**Q7.** In the homework, proxy B agreed with the sign of the retention effect in only 35% of past experiments. What does that mean in practice?

<details><summary>Answer</summary>

Optimizing B would push the team in the **wrong direction on retention about 65% of the time**, worse than a coin flip. Teams could keep "winning" on B while retention gets worse. That's why proxies need ongoing experiment-level validation.
</details>

---

**Q8.** State Goodhart's law and one way experimentation platforms defend against it.

<details><summary>Answer</summary>

*"When a measure becomes a target, it ceases to be a good measure."* Defenses: **guardrail metrics** (to catch gaming such as more notifications causing more unsubscribes), **periodic re-validation** of proxies against the north star, **long-term holdouts**, and an OEC that combines several metrics instead of a single gameable one.
</details>

---

**Q9.** Which two properties determine a metric's usefulness for decisions?
A) Sensitivity and directionality
B) Popularity and simplicity
C) Low mean and low variance
D) Being a ratio and being a guardrail

<details><summary>Answer</summary>

**A.** Sensitivity (it detectably moves when things change) and directionality (it moves in the direction of real value). A metric needs both: sensitive but misdirected leads you astray, while directional but insensitive never detects anything.
</details>

---

**Q10 (interview, answer out loud in 2 minutes).** "We're testing a new model in ChatGPT [or a new feature in Discord]. How would you choose the metrics?"

<details><summary>Model answer</summary>

"I'd start from the decision and the north star, say long-term retention or weekly active users. That's too slow and insensitive for a two-week test, so I'd pick **driver metrics** shown to predict it, ideally validated on past experiments: for example, the share of sessions with a successful task outcome, return visits within 7 days, or conversations that don't end in a retry. I'd check that each is **sensitive**, with enough power for our traffic (capping or CUPED if needed), and **directional**, meaning it moves the same way as long-term value. Then **guardrails**: latency, error and crash rates, safety-policy flags, cost per query, and user complaints. And **trust metrics**: SRM and logging health. I'd pre-register an OEC with a clear decision rule, for example ship if the driver improves and no guardrail's upper bound crosses its threshold. Finally, to protect against Goodhart's law, I'd keep a long-running holdout to confirm the north star actually moves."

**What scores well:** starting from the decision, separating goal, driver, guardrail and trust metrics, sensitivity *and* directionality, proxy validation, pre-registration, and long-term holdouts.
</details>

---

### Scoring
| Score | Next step |
|---|---|
| 9–10 | Move on to Day 10 |
| 8 | Pass. Re-read the explanations for the questions you missed |
| ≤ 7 | Re-read lesson §1.1–1.4 and the Netflix proxy post, then retake tomorrow |

Record your score in `answers.md`, e.g. `Quiz: 9/10, missed Q6`.
