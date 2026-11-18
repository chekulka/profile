# Day 11 (Week 2): Multiple testing: many metrics × many segments

**Time:** about 80 minutes (30 study, 30 homework, 15 quiz)
**Job skill:** "statistically sound experiments" (Discord), platform design for "many metrics" (OpenAI). Week 2's last topic before the weekend project.

## 1. Concepts

### 1.1 The problem
Test m independent null hypotheses at α = 0.05 each, and the chance of **at least one false win** is 1 − 0.95^m:
| m | P(≥1 false positive) |
|---|---|
| 1 | 5% |
| 10 | 40% |
| 12 segments | 46% |
| 20 metrics | **64%** (you simulated this in Part 1) |

A dashboard with 20 metrics × 10 segments *will* light up somewhere, even for an A/A test.

### 1.2 Two error rates
- **FWER (family-wise error rate):** P(any false positive). Control it with **Bonferroni** (reject if p < α/m) or **Holm** (step-down, uniformly more powerful, same guarantee).
- **FDR (false discovery rate):** the expected *share* of your "discoveries" that are false. Control it with **Benjamini-Hochberg (BH)**: sort the p-values, find the largest k with p₍ₖ₎ ≤ (k/m)·α, and reject the k smallest.

In the homework (100 metrics, 10 real): no correction gives **FDR 33%**; Bonferroni gives FWER 5% but finds only **32%** of the real effects; BH keeps FDR at **4%** and finds **50%**.

### 1.3 What platforms actually do
| Metric group | Common practice |
|---|---|
| **Primary (decision) metric** | 1 pre-registered metric, so no correction needed. With several success metrics, correct for them (Bonferroni or Holm). |
| **Guardrails** | Often tested per metric for *harm*, with a power check. Missing a real harm is costly, so don't over-correct. |
| **Exploratory dashboards and segments** | BH/FDR, clearly labeled "exploratory"; findings become **hypotheses for the next test**, not launch decisions. |

Spotify's approach: adjust the false-positive rate for the **success metrics** (where you have multiple chances to win), and treat guardrails separately with power in mind.

### 1.4 The segment trap
"It didn't work overall, but it's significant for Android users in Canada!" With 12 segments there's a 46% chance of a false segment win. Treat it as a **hypothesis**: correct for the number of segments, check that it makes sense, and **replicate it** in a new test.

### 1.5 Multiple testing over time
Checking results every day is also multiple testing (peeking). BH doesn't fix that; that's sequential testing, **Week 4**.

## 2. Study materials (in this order)
1. 📖 ⭐ **Spotify Confidence, "Are Optimal Multiple Testing Corrections Optimal for You?"** (about 12 min): https://confidence.spotify.com/blog/multiple-testing-corrections
2. 📖 **Spotify Engineering, "Risk-Aware Product Decisions in A/B Tests with Multiple Metrics"** (2024; success vs. guardrail metrics): https://engineering.atspotify.com/2024/03/risk-aware-product-decisions-in-a-b-tests-with-multiple-metrics
3. 📖 **Statsig, "Speeding up A/B tests with discipline"** (BH for dashboards, and why it doesn't fix peeking): https://www.statsig.com/blog/speeding-up-a-b-tests-with-discipline
4. 🎥 **StatQuest, "False Discovery Rates, FDR, clearly explained"**: find it on the index at https://statquest.org/video_index.html
5. 📖 Reference: **Wikipedia, "False discovery rate"** (the BH procedure, step by step): https://en.wikipedia.org/wiki/False_discovery_rate

## 3. Homework
```bash
python learning/day11/homework.py
```
3 parts, including implementing Bonferroni and BH yourself. Answer Q-A in `learning/day11/answers.md`.

## 4. Quiz
Take [`quiz.md`](quiz.md) (10 questions, pass mark 8/10).

## 5. Check yourself
- [ ] I can compute P(≥1 false positive) for m tests.
- [ ] I can explain FWER vs. FDR and when each fits.
- [ ] I can run Bonferroni, Holm and BH by hand on 5 p-values.
- [ ] I know how platforms treat primary, guardrail and exploratory metrics differently.
- [ ] I can push back on segment-hunting, and I know BH doesn't fix peeking.
