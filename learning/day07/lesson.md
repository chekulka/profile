# Day 7 (Weekend project, Week 1): Build an A/A test harness

**Time:** about 2 hours. Catching up first is fine: if Days 1–6 are still open, do **Day 1 + Day 2 this weekend** and come back to this project after.
**Job skill:** "experience building, scaling, or operating experimentation platforms" (OpenAI); "ensure experiments are statistically sound" and "set the platform roadmap" (Discord). This is a **portfolio piece**: put it on GitHub when you're done.

## 1. Concepts

### 1.1 What an A/A test is
Both groups get the **same** experience. Any "effect" is pure noise, so over many A/A tests a correct analysis must produce:
- **About 5% false positives** at α = 0.05
- **Uniformly distributed p-values** on [0, 1] (Day 2 §1.6)

### 1.2 Reading a p-value histogram
| Shape | Meaning |
|---|---|
| Flat | ✅ Calibrated method |
| Spike near 0 | ❌ Anti-conservative: SEs too small (e.g. ignoring clustering, Day 4), so too many false wins |
| Pile-up near 1 | ⚠️ Conservative: SEs too large (e.g. the unclustered panel DiD in Day 3), so real effects get missed |

Because eyeballing a histogram is unreliable, test uniformity formally: **Kolmogorov-Smirnov** (used today) or **Anderson-Darling** (Microsoft ExP's choice).

### 1.3 Three ways platforms use A/A tests
1. **Validate the stats engine**: every metric and variance method (today's Part 2).
2. **Validate assignment**: SRM alarms should fire about 0.1% of the time at p < 0.001 (Part 3).
3. **Continuous monitoring**: always-on A/A tests detect logging and pipeline regressions.

Microsoft also runs **simulated A/A tests on historical data** (randomly splitting past users) to vet a new metric *before* anyone uses it in a real experiment.

### 1.4 Small tests hide bugs
A bug that moves 1% of users between arms produces χ² ≈ 4 at N = 10,000 (rarely alarms) but χ² ≈ 80 at N = 200,000 (always alarms). Platforms should **pool SRM checks across all experiments** that share an assignment service, so small experiments can't hide a systematic bug.

## 2. Study materials
1. 📖 ⭐ **Microsoft ExP, "p-Values for Your p-Values: Validating Metric Trustworthiness by Simulated A/A Tests"** (about 15 min): https://www.microsoft.com/en-us/research/group/experimentation-platform-exp/articles/p-values-for-your-p-values-validating-metric-trustworthiness-by-simulated-a-a-tests/
2. 📖 **"Using the Kolmogorov-Smirnov Test to Validate A/A Tests"** (about 8 min): https://medium.com/@mohsendd/using-the-kolmogorov-smirnov-test-to-validate-a-a-tests-f044f60ff5e4
3. 📘 Optional: Kohavi et al., ch. 19, "The A/A Test"

## 3. Project
```bash
python learning/day07/homework.py
```
- **Part 1:** the harness (`run_aa`, `audit` with a KS test)
- **Part 2:** audit 3 analysis methods. The harness should flag the naive session-level test as BROKEN.
- **Part 3:** audit assignment, and see why a bug hides in small tests
- **Part 4:** write a portfolio README (in `answers.md`). Stretch goal: move the harness into its own GitHub repo with a p-value histogram plot.

## 4. Quiz
Take [`quiz.md`](quiz.md) (10 questions, pass mark 8/10).

## 5. Check yourself
- [ ] I can explain why p-values are uniform under the null, and what spikes at 0 or 1 mean.
- [ ] My harness flags the naive session z-test as broken and passes the other two.
- [ ] I can explain why a 1% assignment bug alarms at 200K users but not at 10K.
- [ ] I can describe 3 ways a platform uses A/A tests.
