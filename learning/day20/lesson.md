# Day 20 (Week 4, Day 3): Always-valid inference: mSPRT and confidence sequences

**Time:** about 90 minutes (35 study, 35 homework, 15 quiz)
**Job skill:** "sequential testing" (OpenAI). Optimizely's Stats Engine and many modern platforms use these methods so people can look at results **any time, as often as they like**.

## 1. Concepts

### 1.1 The goal
Group sequential tests (Day 19) need **planned** looks. Sometimes people check continuously, for real-time ops dashboards, guardrails, or teams that simply peek. **Always-valid** methods keep α controlled **at any stopping time**, however often you look.

### 1.2 mSPRT (mixture sequential probability ratio test)
For paired differences Xᵢ ~ N(δ, V) with S_n = ΣXᵢ, average the likelihood ratio over a "mixing" prior δ ~ N(0, τ²):

  **Λ_n = √(V/(V + nτ²)) · exp( τ²·S_n² / (2V(V + nτ²)) )**

Reject H₀ the first time **Λ_n ≥ 1/α**. Under H₀, Λ_n is a nonnegative martingale with mean 1, so by **Ville's inequality** P(it ever reaches 1/α) ≤ α. The **always-valid p-value** is p_n = min(1, min_{m≤n} 1/Λ_m), and it never increases.

Homework, A/A with a look after **every** observation pair: a naive z-test "wins" **56%** of the time; mSPRT **2.2%** (≤ 5% ✅).

### 1.3 Confidence sequences
Invert the test and you get intervals that cover the truth **at all times simultaneously** (Howard, Ramdas et al.):

  **|mean_n − δ| < √( V(V + nτ²)/(n²τ²) · (2·ln(1/α) + ln((V + nτ²)/V)) )**

Homework: uniform coverage **97.8%** vs. **44%** for the usual 95% CI checked at every step. The price is width: at n = 2,000 the sequence is about **1.55× wider** than a fixed CI.

### 1.4 The trade-off: flexibility vs. power
| | Fixed-n (one look) | Group sequential (Day 19) | Always-valid (mSPRT/CS) |
|---|---|---|---|
| When you can look | Only at the end | At planned looks | **Any time** |
| Power at the same max n | Highest (homework: 71%) | Almost the same | **Lower** (homework: 45%) |
| Early stopping | No | For big effects | Yes, continuously |
| Best for | Simple and disciplined teams | Batch pipelines (Spotify) | Real-time monitoring, guardrails (Optimizely) |

- **τ²** (the mixing variance) tunes where power is concentrated. Set it near the effect sizes you expect.
- Spotify's comparison post recommends always-valid methods for teams that mainly want an **early-detection system with bounded false positives**.

## 2. Study materials (in this order)
1. 📄 ⭐ **Johari, Koomen, Pekelis & Walsh (2017), "Peeking at A/B Tests"** (KDD '17). Now read §3–4 (mSPRT and always-valid p-values): https://dl.acm.org/doi/10.1145/3097983.3097992 (the extended version, "Always Valid Inference", is arXiv:1512.04922)
2. 📖 **Spotify, "Choosing a Sequential Testing Framework"**. Re-read the always-valid vs. group sequential comparison: https://engineering.atspotify.com/2023/03/choosing-sequential-testing-framework-comparisons-and-discussions
3. 📖 **Netflix, "Sequential A/B Testing Keeps the World Streaming, Part 1"** (anytime-valid methods in production): https://netflixtechblog.com/sequential-a-b-testing-keeps-the-world-streaming-netflix-part-1-continuous-data-cba6c7ed49df
4. 📄 Deep dive, optional: **Howard, Ramdas, McAuliffe & Sekhon, "Time-uniform, nonparametric, nonasymptotic confidence sequences"** (Annals of Statistics 2021): https://arxiv.org/abs/1810.08240
5. 🎥 Optional: **KDD '19 tutorial "Fundamentals of large-scale sequential experimentation"** (Ramdas et al.): https://stat.cmu.edu/~aramdas/kdd19/

## 3. Homework
```bash
python learning/day20/homework.py
```
3 parts: the mSPRT statistic, confidence sequences, and the power trade-off. Answer Q-A in `learning/day20/answers.md`, and try other τ² values.

## 4. Quiz
Take [`quiz.md`](quiz.md) (10 questions, pass mark 8/10).

## 5. Check yourself
- [ ] I can explain what makes a p-value "always valid", and why the mSPRT achieves it (martingale + Ville).
- [ ] I can explain confidence sequences vs. confidence intervals.
- [ ] I can state the cost (power and width) and when it's worth paying.
- [ ] I can choose between fixed, group sequential and always-valid for a given team.
