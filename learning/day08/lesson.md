# Day 8 (Sunday): Week 1 review

**Time:** about 45 minutes. No new topic today.
**Plan:** read the one-page summary below, take the **15-question cumulative quiz** in [`quiz.md`](quiz.md) (pass mark **12/15**), and use each miss to decide which day to revisit.

## Week 1 on one page
| Day | Topic | The one idea to remember |
|---|---|---|
| 1 | Potential outcomes, 2x2 DiD | Every causal estimate is a guess at a missing counterfactual. DiD uses the control group's *change* and needs parallel trends. |
| 2 | Hypothesis testing | SE = √(s²_A/n_A + s²_B/n_B). Welch by default. A t-test **is** OLS on a dummy (HC2 SEs). Skewed metrics need a large n or bootstrap/capping. |
| 3 | Power and MDE | MDE = 2.80·SE (α = 0.05, 80% power). n ∝ σ²/δ². A 90/10 split costs 1.67× the MDE. Simulate to check your *actual* SEs. |
| 4 | Ratio metrics | Randomize users, analyze sessions → naive SEs too small (FPR about 11%). Fix with the delta method = clustered SEs = user bootstrap. |
| 5 | Readouts | Decision + effect with a range + top risk in 3 lines. A failed validity check goes in the TL;DR. "Not significant" ≠ "safe". |
| 6 | SRM | χ² against the planned split, alarm at p < 0.001. An SRM means biased results: localize it, fix it, re-run; never reweight. |
| 7 | A/A harness | A trustworthy method gives uniform p-values. A spike at 0 means anti-conservative; a pile-up at 1 means conservative. |

## How to use your score
| Missed questions on… | Revisit |
|---|---|
| Q1–Q2 | Day 1 |
| Q3–Q6 | Day 2 |
| Q7–Q9 | Day 3 |
| Q10–Q11 | Day 4 |
| Q12 | Day 5 |
| Q13 | Day 6 |
| Q14 | Day 7 |
| Q15 | All of them; practice it out loud twice |
