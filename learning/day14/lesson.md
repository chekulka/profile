# Day 14 (Weekend project, Week 2): Build a trustworthy experiment analyzer

**Time:** about 2–3 hours. If Days 1–13 are still open, **do Day 1 and Day 2 this weekend first**. This project ties those days together, so it will make much more sense afterwards.
**Job skill:** "building, scaling, or operating experimentation platforms" (OpenAI); "ensure experiments are statistically sound" and "set the platform roadmap" (Discord). This is your **second portfolio piece**, after the Day 7 A/A harness.

## What you're building
One function, `analyze(df)`, that does what an experimentation platform's stats engine does, in the right order:

| Step | Check / method | From |
|---|---|---|
| 1 | **SRM check**: if it fails, *stop and refuse to report* | Day 6 |
| 2 | Primary metric **sessions/user with CUPED** (pre-period sessions) | Day 12 |
| 3 | **CTR with the delta method** (a ratio metric) | Day 4 |
| 4 | **Revenue, capped at p99** (heavy tails) | Days 2, 9 |
| 5 | **Benjamini-Hochberg** across the metrics | Day 11 |
| 6 | **TL;DR with a decision** | Day 5 |

## Why the order matters
- **SRM first:** if the arms aren't comparable, every number after it is meaningless, and showing them anyway invites people to act on biased results.
- **Variance reduction and correct SEs before testing:** the p-values are only valid once the method is right.
- **Multiple-testing correction last:** it adjusts the final set of p-values that people will actually read.
- **Decision rule pre-registered:** the primary metric decides; the others inform.

## Study materials (short; this is a build weekend)
1. 📖 Re-read your own lessons: Day 5 §1.1 (readout structure) and Day 6 §1.4 (SRM debugging).
2. 📖 **Microsoft ExP, "p-Values for Your p-Values"** (if you skipped it on Day 7): https://www.microsoft.com/en-us/research/group/experimentation-platform-exp/articles/p-values-for-your-p-values-validating-metric-trustworthiness-by-simulated-a-a-tests/
3. 📖 **Spotify, "Risk-Aware Product Decisions in A/B Tests with Multiple Metrics"** (how a real platform turns many metrics into one decision): https://engineering.atspotify.com/2024/03/risk-aware-product-decisions-in-a-b-tests-with-multiple-metrics

## Project
```bash
python learning/day14/homework.py
```
4 TODOs (SRM p-value, CUPED θ, delta-method variance, BH). When they're done:
- On the **clean experiment**, the CIs cover the true effects and the decision is **SHIP**.
- On the **logging-bug experiment**, the analyzer prints ⛔ and **refuses to report**.

Then answer Q-A and Q-B in `learning/day14/answers.md`, and try the stretch goals (your own GitHub repo, a Lin-adjustment option, an A/A mode).

## Quiz
Take [`quiz.md`](quiz.md) (10 questions, pass mark 8/10).

## Check yourself
- [ ] My analyzer passes both scenarios.
- [ ] I can explain why the SRM check comes first and BH comes last.
- [ ] I can explain why one CI out of several missing the truth isn't a bug.
- [ ] (Stretch) The analyzer lives in its own repo with a README and a test.
