# Day 6 quiz: sample ratio mismatch

**Pass mark: 8/10.** Answer on paper first, then open the answers.

---

**Q1.** Planned 50/50. Observed 50,600 control vs 49,400 treatment. Compute χ² and decide.

<details><summary>Answer</summary>

**χ² = 14.4, p ≈ 0.00015: SRM.** Expected 50,000 each, so χ² = (600² + 600²)/50,000 = 14.4 (or use 4k²/N = 4·600²/100,000). That's well below the 0.001 alarm threshold, so stop interpreting the results and debug.
</details>

---

**Q2.** Observed 500,600 vs 499,400 (planned 50/50). SRM?

<details><summary>Answer</summary>

**No: χ² = 1.44, p ≈ 0.23.** The absolute gap (1,200 users) is twice Q1's, but relative to N = 1M it's tiny (50.06%). SRM depends on the gap **relative to √N**, not on the raw gap or the raw percentage alone.
</details>

---

**Q3.** Why is an SRM worse than simply "a bit less data in one arm"?

<details><summary>Answer</summary>

Because the users who went missing are usually **not random**. A crash, a redirect or a bot filter removes a particular kind of user, so the two arms are no longer comparable and the effect estimate is **biased**, in an unknown direction. Less data only makes estimates noisier; an SRM makes them wrong.
</details>

---

**Q4.** Planned 10% treatment / 90% control. Observed 10,300 / 89,700. SRM at the 0.001 threshold?

<details><summary>Answer</summary>

**Not at 0.001 (χ² = 10.0, p ≈ 0.0016), but it's close enough to investigate.** Expected 10,000/90,000: χ² = 300²/10,000 + 300²/90,000 = 9 + 1 = 10. Always use the **planned** ratios, not 50/50. A borderline result deserves a segment check and a look at the trend over time.
</details>

---

**Q5.** In the homework, why did losing low-intent Android users from treatment create a *positive* fake lift?

<details><summary>Answer</summary>

The treatment arm lost users who were **unlikely to convert**, so the users who remained in treatment were, on average, higher-intent than control. That makes treatment's conversion rate look better even though the feature did nothing. This is selection bias created after randomization.
</details>

---

**Q6.** Which is NOT a typical SRM cause?
A) The treatment page loads slower and some users leave before the exposure event is logged
B) Bot filtering that flags more bots in one arm
C) The treatment truly increases conversion by 5%
D) Traffic was ramped from 10% to 50% for treatment only on day 3

<details><summary>Answer</summary>

**C.** A real effect on an *outcome* doesn't change *how many users were assigned or counted*. A (execution), B (log processing) and D (experimenter interference) all change the counts. Exception: if the "count" itself is post-treatment (e.g. counting only users who reached checkout), a real effect can cause an SRM, which is why you should define the analysis population carefully.
</details>

---

**Q7.** You scan 30 segments for SRM and one has p = 0.04. What now?

<details><summary>Answer</summary>

On its own, that's expected noise: with 30 tests at α = 0.05, you'd expect about 1.5 false alarms. That's why SRM scans use a strict threshold like **0.001**. Note it, check whether it persists over time or lines up with a known change, but don't declare a bug from one marginal p-value. (In the homework, web had p ≈ 0.05: that's noise, while Android had p ≈ 0.)
</details>

---

**Q8.** After you find an SRM, a colleague suggests reweighting the arms to 50/50 and moving on. Why is that wrong?

<details><summary>Answer</summary>

Reweighting fixes the **counts** but not the **composition**: you still don't know what the missing users would have done, so the bias remains. The fix is to find and remove the cause, then re-run the test. At most, analyze clearly unaffected segments as a **diagnostic**, and say that they may not represent everyone.
</details>

---

**Q9.** Put these SRM debugging steps in a sensible order: (a) re-run the experiment, (b) segment the SRM check by platform, version, country and day, (c) confirm with p < 0.001, (d) find when the imbalance started and at which funnel stage, (e) fix the root cause.

<details><summary>Answer</summary>

**c → b → d → e → a.** Confirm it, localize it (segment, then time and funnel stage), fix it, and re-run. Skipping the segmentation leads to guessing, and skipping the re-run means you ship a decision based on biased data.
</details>

---

**Q10 (interview, answer out loud in 90 seconds).** "Your experiment shows an SRM. Walk me through what you'd do."

<details><summary>Model answer</summary>

"First, I'd stop interpreting the metrics: with an SRM, the arms aren't comparable and any effect could be bias. I'd confirm it with a chi-square against the planned ratio, using a strict threshold like 0.001. Then I'd localize it: segment the check by platform, app version, browser, country and new vs. returning users, and plot the ratio by day to see whether it started with a deploy or a ramp. Next, I'd find the funnel stage where it appears. Is it imbalanced at assignment, at exposure logging, or only after an analysis filter? Common culprits are crashes or latency in the treatment, redirects, bot filtering, and triggers defined on post-treatment behaviour. Once I find the cause, I'd fix it and re-run the test. I wouldn't reweight, because that doesn't fix who's missing. Finally, I'd make sure the platform runs automated SRM checks on every experiment, so this gets caught on day one instead of at the readout."

**What scores well:** stopping interpretation, segment + time + funnel localization, no reweighting, re-running, and the platform-level prevention (the Staff-level angle for Discord).
</details>

---

### Scoring
| Score | Next step |
|---|---|
| 9–10 | Move on to Day 7 |
| 8 | Pass. Re-read the explanations for the questions you missed |
| ≤ 7 | Re-read lesson §1.2–1.4 and the Fabijan taxonomy, then retake tomorrow |

Record your score in `answers.md`, e.g. `Quiz: 9/10, missed Q4`.
