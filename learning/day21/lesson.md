# Day 21 (Weekend project, Week 4): A sequential-testing simulator

**Time:** about 2 hours. If Days 1–20 are still open, do **Day 1 and Day 2 first** this weekend.
**Job skill:** "sequential testing" (OpenAI) and "set the experimentation platform roadmap" (Discord). This is your **third portfolio piece**, after the A/A harness (Day 7) and the analyzer (Day 14).

## What you're building
One simulator that runs **six stopping rules on the same data streams** and reports false positive rate, power and average sample used. This is the evidence a platform team needs before picking a default.

## Expected results (from my test run)
| Method | FPR | Power | Avg sample (under a real effect) |
|---|---|---|---|
| fixed (one look) | 0.049 | **0.71** | 100% |
| naive peek every 100 | **0.244 ❌** | 0.82 (inflated) | 50% |
| Bonferroni × 20 looks | 0.018 | 0.40 | 83% |
| **OBF (4 looks)** | 0.049 | **0.70** | **84%** |
| Pocock (4 looks) | 0.051 | 0.62 | 77% |
| mSPRT (every pair) | 0.019 | 0.44 | 81% |

**How to read it:**
- Naive peeking "has the most power" only because its false positive rate is invalid. Its wins can't be trusted.
- **OBF keeps almost all the power** of a fixed test and still saves about 16% of the sample on average. That's why it's a common platform default.
- **mSPRT** buys complete freedom to look whenever you want, at a real power cost. It's ideal for guardrails and real-time monitoring.
- **Bonferroni** across looks is valid but wastes power (correlated looks), and it's dominated by OBF.

## Study materials (short; this is a build day)
1. Re-read your Day 18–20 lessons (§1 of each).
2. 📖 **Spotify, "Choosing a Sequential Testing Framework"**, especially its comparison table, which you're reproducing in spirit: https://engineering.atspotify.com/2023/03/choosing-sequential-testing-framework-comparisons-and-discussions

## Project
```bash
python learning/day21/homework.py
```
3 TODOs (the Bonferroni critical value, Pocock, the mSPRT stopping rule). Then write your **recommendation memo** (Q-A) in `learning/day21/answers.md`, citing numbers from your table.

**Stretch goals:** add a non-binding futility rule to OBF, plot power vs. effect size for each method, and publish the simulator in a GitHub repo next to your A/A harness and analyzer.

## Quiz
Take [`quiz.md`](quiz.md) (10 questions, pass mark 8/10).

## Check yourself
- [ ] All three checks pass, and I can explain every row of the table.
- [ ] My memo recommends a default for decision metrics and one for guardrails, with numbers.
- [ ] I can explain why "most power" for naive peeking is an illusion.
