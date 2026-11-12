# Day 5 written exercise

## Scenario
A fintech app tested **"Smart reminders"**: personalized nudges to finish incomplete account tasks.
- **Design:** randomized by user, planned 50/50 split, 14 days (two full weeks). The pre-registered MDE for the primary metric was +0.6 pp.
- **Primary metric:** 7-day journey completion rate.
- **Guardrail:** support calls per user. The business considers a **+5% increase** in calls unacceptable.
- **Your numbers:** run `python learning/day05/readout_numbers.py`. It reports the SRM check, the primary metric and the guardrail.

## Part A: write the one-page readout (in `answers.md`)
Use the structure from lesson §1.1. Limits: **TL;DR ≤ 3 lines; whole readout ≤ 1 page.** Your readout must:
1. Notice what the SRM check says, and decide what that means for the recommendation.
2. Report the primary result as absolute (pp) and relative (%) with CIs.
3. Interpret the guardrail correctly against the +5% threshold.
4. End with a concrete recommendation and next steps. Hint: "ship" may not be the right call *yet*, even though the primary metric is strongly positive.

## Part B: critique this bad readout (list at least 6 problems)
> **Smart Reminders: HUGE WIN 🎉**
> We ran the test and the treatment group had way more completions! p-value was 0.000015 so we're 99.99% sure reminders work. Support calls were not significant so there's no impact on support. The split was a little uneven but that's normal. Some days looked even better (Day 3 was +6%!). We should roll out to everyone immediately and also add reminders to every other journey.

## Part C (2 sentences): explain to a VP, without jargon, why we don't ship the moment a dashboard turns green on Day 3.

---

<details><summary>Model answer for Part A (open only after writing yours)</summary>

**TL;DR:** **Don't ship yet. Fix and re-run.** Reminders appear to raise 7-day completion by **+0.9 pp (31.0% → 31.9%, +2.9%; 95% CI +1.6% to +4.2%)**, but the test failed its **sample-ratio check (100,480 vs 99,520, p = 0.03)**, so the estimate may be biased. Support calls are inconclusive: we can't rule out up to a +8.8% increase, above our +5% limit.

**Context:** Reminders aim to increase completion of unfinished account tasks. This test decides whether to launch to all users.

**Design:** User-level randomization, 50/50, 14 days. Primary: 7-day completion (MDE +0.6 pp). Guardrail: support calls per user (unacceptable if ≥ +5%).

**Validity:** ⚠️ **SRM detected**: treatment has 480 fewer users than the expected 100,000 (960 fewer than control; χ² = 4.61, p = 0.03). Possible causes include reminder-triggered app crashes, logging differences, or bot filtering. Until we find the cause, the results may be biased.

**Results:**
| Metric | Control | Treatment | Change (95% CI) |
|---|---|---|---|
| 7-day completion | 31.0% | 31.9% | +0.90 pp [+0.49, +1.31]; +2.9% [+1.6%, +4.2%] |
| Support calls/user | 0.0420 | 0.0435 | +3.6% [−1.6%, +8.8%] (inconclusive) |

**Interpretation and risks:** The primary effect is large relative to the MDE and would be a clear win **if** the SRM is benign. The guardrail can't rule out harm above our threshold.

**Recommendation and next steps:**
1. Debug the SRM (check assignment and exposure logs by day, platform and app version).
2. Fix it, then re-run with power sized for the guardrail at +5%.
3. Ship if completion holds and the guardrail's upper bound stays below +5%.
</details>

<details><summary>Model answer for Part B</summary>

1. "HUGE WIN" with no effect size or range: the headline is hype, not information.
2. **Misreads the p-value**: "99.99% sure reminders work" isn't what p = 0.000015 means.
3. **Ignores the SRM**: "a little uneven but normal" is false (p = 0.03). It could invalidate everything.
4. **"Not significant = no impact" on the guardrail**: the CI allows up to +8.8%, above the +5% limit.
5. **Cherry-picks a day** ("Day 3 was +6%"): daily noise, peeking, and novelty effects.
6. **No absolute or relative effect with a CI**, and no baseline.
7. **Over-generalizes** ("add reminders to every other journey") beyond what was tested.
8. No design details (unit, duration, metrics), and no stated decision criteria.
</details>
