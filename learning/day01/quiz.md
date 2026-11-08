# Day 1 quiz: potential outcomes and 2x2 DiD

**Pass mark: 8/10.** Answer every question on paper before opening any answer. If you score below 8, re-read the lesson section named in each explanation you missed, then retake the quiz tomorrow.

---

**Q1.** For one user, Y(1) = 12 and Y(0) = 9. What is this user's individual treatment effect, and why can you never compute it from real data?

<details><summary>Answer</summary>

**3.** You only ever observe one potential outcome per unit, Y(1) if treated or Y(0) if not. This is the *fundamental problem of causal inference*. Any causal estimate is really an estimate of the missing counterfactual. (Lesson §1)
</details>

---

**Q2.** Why does randomization let a simple difference in means estimate the average treatment effect?
A) It makes the sample larger
B) It makes treatment assignment independent of the potential outcomes
C) It removes measurement error
D) It guarantees parallel trends

<details><summary>Answer</summary>

**B.** Randomization ensures treatment ⟂ (Y(0), Y(1)), so the control group's mean is an unbiased estimate of what the treated group *would have* looked like. A is about precision, not bias. D is a DiD assumption, not something randomization gives you. (Lesson §2)
</details>

---

**Q3.** Treated group: pre = 20, post = 30. Control group: pre = 15, post = 21. What is the DiD estimate?

<details><summary>Answer</summary>

**4.** (30 − 20) − (21 − 15) = 10 − 6 = 4. The control group's change (+6) is the estimate of what would have happened to the treated group without treatment. (Lesson §4)
</details>

---

**Q4.** Using Q3's numbers, what would the naive "post-period treated minus control" comparison give, and why is it wrong?

<details><summary>Answer</summary>

**9** (30 − 21). It mixes the treatment effect with the **pre-existing gap** of 5 (20 − 15) between the groups. DiD removes that fixed gap by differencing. This is exactly the bias you saw in Part 1 of the homework, where treated markets started 3 units higher.
</details>

---

**Q5.** What is the parallel trends assumption?
A) The groups have equal outcome levels before treatment
B) Without treatment, the treated group's outcome would have changed by the same amount as the control group's
C) The pre-period trends are statistically indistinguishable
D) The treatment effect is constant over time

<details><summary>Answer</summary>

**B.** It concerns the **counterfactual change**, not levels (A). DiD allows the levels to differ. C is something you can *test*, but passing that test doesn't prove the assumption: it's untestable for the post period (more on Day 3 and in week 5). D is a different assumption that DiD doesn't need. (Lesson §5)
</details>

---

**Q6.** In the regression `y = a + b·treated + c·post + δ·(treated×post) + e`, which coefficient is the DiD estimate, and what do *b* and *c* capture?

<details><summary>Answer</summary>

**δ** is the ATT. **b** is the baseline gap between the groups, **c** is the common time shock, and **δ** is the extra change in the treated group after treatment. diff-diff fits this model and adds the correct standard errors. (Lesson §6)
</details>

---

**Q7.** In Card & Krueger, why did we cluster standard errors by `store_id`?

<details><summary>Answer</summary>

Each store contributes **two correlated observations**, pre and post. Treating them as independent overstates the information in the data and makes the SEs too small. Clustering by the unit of repeated observation fixes that. The general rule is to cluster at the level of treatment assignment or repeated measurement, whichever is coarser.
</details>

---

**Q8.** Card & Krueger found ATT ≈ +2.75 FTE (full-time-equivalent) employees per store, with p ≈ 0.04. A colleague says, "So minimum wage increases always raise employment." What are two problems with that claim?

<details><summary>Answer</summary>

(1) **External validity:** it's one policy, one industry (fast food), one place and one time period (NJ vs. PA, 1992). (2) It's only causal **if parallel trends holds**. Pennsylvania has to be a valid counterfactual for New Jersey, and later work questioned the data. It's also an **average** effect, which can hide heterogeneity. On top of that, the CI [0.19, 5.32] is wide: the data rule out large job losses, but they don't pin down the effect's size.
</details>

---

**Q9.** Which situation calls for DiD rather than an A/B test?
A) Testing a new button color on the web
B) A feature that legal requires to launch in all EU countries on one date, with the US launching later
C) Comparing two ranking models offline
D) Testing email subject lines

<details><summary>Answer</summary>

**B.** Assignment is decided by policy at the region level, so you can't randomize users. The US is the natural control group as long as EU and US trends were parallel beforehand. A and D can simply be randomized. C is offline evaluation, not a causal design.
</details>

---

**Q10 (interview style, answer out loud in 60 seconds).** A PM says, "We launched in Texas first, Texas conversions rose 8%, so the feature lifted conversion by 8%." How do you respond?

<details><summary>Model answer</summary>

"The 8% is a before/after change, so it also includes seasonality, marketing and other trends that would have happened anyway. I'd estimate the counterfactual using comparable states that didn't get the launch. If their conversion rose 5%, the DiD estimate is about 3 points. Before trusting that number, I'd check that Texas and the control states moved in parallel for several months before launch. I'd also run placebo tests, cluster standard errors by state, and since there's only one treated state, consider synthetic control or synthetic DiD to build a better comparison group. If possible, I'd randomize the next rollout."

**What interviewers look for:** naming the counterfactual, naming the assumption, a diagnostic, and a better design for next time.
</details>

---

### Scoring
| Score | Next step |
|---|---|
| 9–10 | Move on to Day 2 |
| 8 | Pass. Re-read the explanations for the questions you missed |
| ≤ 7 | Re-read the lesson and Mixtape ch. 9, then retake tomorrow |

Record your score in `answers.md`, e.g. `Quiz: 9/10, missed Q7`.
