# Day 15 (Sunday): Week 2 review (Days 9–14)

**Time:** about 45 minutes. No new topic today.
**Plan:** read the summary below, take the **15-question cumulative quiz** in [`quiz.md`](quiz.md) (pass mark **12/15**), and revisit the day for each question you miss.

## Week 2 on one page
| Day | Topic | The one idea to remember |
|---|---|---|
| 9 | Metric design | Goal vs. driver vs. guardrail. A good decision metric needs **sensitivity and directionality**. Validate proxies on **past experiments' effects**, not on cross-user correlations. Cap heavy tails. |
| 10 | Novelty, carryover, interference | Effects change over time (plot them by day; compare new vs. returning users). Re-randomize with a fresh salt. **SUTVA** breaks in marketplaces (overstated) and social products (understated), so randomize clusters or use switchbacks. |
| 11 | Multiple testing | P(≥1 false win) = 1 − 0.95^m. FWER: Bonferroni or Holm. FDR: Benjamini-Hochberg. One pre-registered primary metric; exploratory findings are hypotheses. |
| 12 | CUPED | Y − θ(X − X̄), θ = Cov/Var. Variance kept = 1 − ρ². Only **pre-experiment** covariates. |
| 13 | Regression adjustment | Lin (2013): center the covariates, **interact** them with treatment, use robust SEs, and adjustment can't hurt. **Never adjust for mediators** (bad controls). |
| 14 | Analyzer project | SRM check → estimation (CUPED, delta method, capping) → BH → decision. Refuse to report when the SRM check fails. |

## How to use your score
| Missed… | Revisit |
|---|---|
| Q1–Q3 | Day 9 |
| Q4–Q7 | Day 10 |
| Q8–Q9 | Day 11 |
| Q10–Q12 | Day 12 |
| Q13–Q14 | Day 13 |
| Q15 | Days 10–14; practice it out loud twice |
