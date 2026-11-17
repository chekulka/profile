# Day 10 quiz: novelty, carryover and interference

**Pass mark: 8/10.** Answer on paper first, then open the answers.

---

**Q1.** A redesigned feed shows +4.6% engagement in week 1, but daily effects are declining. What is likely happening, and what do you report?

<details><summary>Answer</summary>

**A novelty effect.** Users engage because the feed is new, and the lift fades as they get used to it. Don't report the week-1 average as the effect. Plot the effect by day since exposure, compare new vs. returning users, run longer, or model the decay. In the homework, the long-run effect was about 2, less than half of the week-1 number.
</details>

---

**Q2.** A new keyboard-shortcut layout shows −3% productivity in week 1, improving each day. What is this called, and what's the risk if you stop early?

<details><summary>Answer</summary>

**A primacy effect (change aversion):** users need time to relearn. Stopping early would **kill a feature that may be positive** in the long run. Run longer, look at new users (who have no old habits), or use a long-term holdout.
</details>

---

**Q3.** Why does comparing **new users vs. returning users** help diagnose novelty and primacy effects?

<details><summary>Answer</summary>

New users have no prior habits, so for them nothing is "new" or "changed": they show something closer to the **steady-state** effect. If returning users show a much larger (novelty) or smaller (primacy) effect than new users, the difference is likely a learning effect that will fade.
</details>

---

**Q4.** A team reuses last month's treatment/control buckets for a new test. Last month's treatment annoyed users. What happens?

<details><summary>Answer</summary>

**Carryover bias**: the new arms already differ before the new treatment starts, because one group carries lasting damage from the previous test. Even an A/A test then shows a "significant effect" (z ≈ −46 in the homework). Fix: **re-randomize with a fresh hash salt** for every experiment, and allow washout time.
</details>

---

**Q5.** State SUTVA in one sentence.

<details><summary>Answer</summary>

**A unit's outcome depends only on its own treatment, not on other units' treatments** (and there's only one version of each treatment). Marketplaces, social networks and shared budgets often violate it.
</details>

---

**Q6.** In a ride marketplace with fixed supply, a "priority" feature tested with 50/50 user randomization shows +39 pp ride rate for treated riders. The market-level test shows 0. Explain.

<details><summary>Answer</summary>

Treated riders **take rides away from control riders in the same market**, because supply is fixed. The user-level comparison measures **redistribution** (treated vs. control), not **creation** (more rides overall). Randomizing whole markets compares worlds where everyone or no one has the feature, and shows the true global effect: 0.
</details>

---

**Q7.** Discord tests a feature that makes users more likely to reply in group chats. With user-level randomization, is the effect likely over- or under-stated, and why?

<details><summary>Answer</summary>

**Understated.** Treated users reply more, so their **control-group friends in the same servers also receive more messages and engage more** (positive spillover). Control is "contaminated" upward, which shrinks the measured gap. Randomizing whole servers (cluster randomization) or using graph-cluster designs reduces this.
</details>

---

**Q8.** What is a switchback experiment, and what is its main cost?

<details><summary>Answer</summary>

Alternating treatment and control **over time** within a region (e.g. 30-minute blocks per city), so the whole market experiences one condition at a time. Each time × region block is the unit of randomization. **Cost:** far fewer units than a user-level test, so lower precision (DoorDash notes about an order of magnitude), plus possible carryover between adjacent blocks.
</details>

---

**Q9.** You switch from user-level to server-level randomization: 2,000 servers, about 500 users each, ICC = 0.02. Roughly how many "effective" users do you have?

<details><summary>Answer</summary>

**DEFF = 1 + (500 − 1)·0.02 ≈ 11**, so the effective n ≈ 1,000,000 / 11 ≈ **91,000 users**, about 11× fewer than the raw count. That's the price of removing interference bias. Variance reduction (CUPED at the server level, week 3) helps win some of it back.
</details>

---

**Q10 (interview, Discord-style, answer out loud in 2 minutes).** "We want to test a new 'smart reply' feature in Discord DMs and group chats. How would you design the experiment?"

<details><summary>Model answer</summary>

"First, interference. Smart replies change what the *recipients* see, so with user-level randomization, control users in shared conversations get treated messages. That violates SUTVA and probably understates the effect. Options: randomize at the **server or community level** for group chats, and use **graph-cluster** randomization for DMs, grouping users who talk to each other. I'd check what fraction of conversations cross cluster boundaries. Second, I'd measure both sides: senders (reply rate, time to reply) and recipients (engagement, response quality), plus guardrails like report and block rates and message deletions. Third, time effects: smart reply is novel, so I'd plot the effect by day, compare new vs. existing users, and plan for at least 2–4 weeks, maybe a holdout. Fourth, power: clustering cuts the effective sample, so I'd compute the design effect from historical server-level variance and use CUPED with pre-period activity. Finally, fresh randomization to avoid carryover from earlier messaging tests, and SRM checks at the cluster level."

**What scores well:** spotting interference and the direction of its bias, cluster or graph design, measuring both sides, novelty, the power cost, and safety guardrails. That's Staff-level breadth.
</details>

---

### Scoring
| Score | Next step |
|---|---|
| 9–10 | Move on to Day 11 |
| 8 | Pass. Re-read the explanations for the questions you missed |
| ≤ 7 | Re-read lesson §1.1–1.4 and the DoorDash post, then retake tomorrow |

Record your score in `answers.md`, e.g. `Quiz: 9/10, missed Q9`.
