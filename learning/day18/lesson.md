# Day 18 (Week 4, Day 1): The peeking problem

**Time:** about 80 minutes (30 study, 35 homework, 15 quiz)
**Job skill:** "sequential testing" (OpenAI) and "ensure experiments are statistically sound" (Discord). Peeking is the most common way real teams break their own experiments.

## 1. Concepts

### 1.1 What peeking is
A fixed-horizon test (t-test, z-test) guarantees α = 5% **only if you look once, at the planned end**. If you check the dashboard every day and **stop the first time p < 0.05**, you're running many tests and keeping the best one.

### 1.2 How bad it is (your homework, A/A tests)
| Looks over 28 days | False positive rate |
|---|---|
| 1 (planned end only) | **5%** |
| 2 | 8% |
| 5 | 14% |
| 10 | 19% |
| 28 (daily) | **28%** |

The z-statistic wanders like a random walk. Given enough looks, it crosses ±1.96 at some point, even when nothing is going on. Evan Miller's classic essay found the same thing.

### 1.3 Peeking also inflates effect sizes (the winner's curse)
If you stop *because* the result just crossed significance, you tend to stop at a **random high point**. Homework: with a small true effect, effects reported at early stops were **about 3× the truth**. Forecasts built on "stopped-early wins" systematically over-promise.

### 1.4 Looking isn't the problem; stopping is
- Peeking is fine **if you don't change the decision based on it** (for example, monitoring for bugs or SRM).
- Stopping early **for harm** (a guardrail breaking badly) is reasonable, but use a rule designed for it, ideally pre-specified.

### 1.5 Fixes (this week)
| Fix | Idea | Day |
|---|---|---|
| **Pre-register the duration** | Look once; simple, but slow | Today |
| **Bonferroni over the looks** | Valid but very conservative (looks are correlated): FPR 1.7%, so power is lost | Today |
| **Group sequential designs (alpha spending)** | Spend α across planned interim looks, e.g. O'Brien-Fleming | Day 19 |
| **Always-valid inference** (mSPRT, confidence sequences) | Look any time, as often as you like | Day 20 |
| **Bayesian testing** | A different question; not automatically "peeking-proof" | Day 21 |

## 2. Study materials (in this order)
1. 📖 ⭐ **Evan Miller, "How Not To Run an A/B Test"** (about 10 min, the classic): https://www.evanmiller.org/how-not-to-run-an-ab-test.html
2. 📄 **Johari, Koomen, Pekelis & Walsh (2017), "Peeking at A/B Tests: Why it matters, and what to do about it"** (KDD '17, Optimizely). Read §1–2: https://dl.acm.org/doi/10.1145/3097983.3097992
3. 📖 **Netflix TechBlog, "Sequential A/B Testing Keeps the World Streaming Netflix, Part 1: Continuous Data"** (motivation and a preview of the fix): https://netflixtechblog.com/sequential-a-b-testing-keeps-the-world-streaming-netflix-part-1-continuous-data-cba6c7ed49df
4. 📖 Optional: **"Fundamentals of large-scale sequential experimentation"** (KDD '19 tutorial by Aaditya Ramdas et al.; slides for Days 19–20): https://stat.cmu.edu/~aramdas/kdd19/

## 3. Homework
```bash
python learning/day18/homework.py
```
3 parts with automatic checks. Write answers to Q-A, Q-B and Q-C in `learning/day18/answers.md`.

## 4. Quiz
Take [`quiz.md`](quiz.md) (10 questions, pass mark 8/10).

## 5. Check yourself
- [ ] I can explain why repeated looks inflate the false positive rate, using the random-walk picture.
- [ ] I know roughly how bad it gets (5% → about 28% with daily looks over 4 weeks).
- [ ] I can explain the winner's curse from early stopping.
- [ ] I can distinguish harmless monitoring from harmful early stopping.
- [ ] I can name the four families of fixes.
