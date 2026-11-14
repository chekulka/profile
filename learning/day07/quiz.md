# Day 7 quiz: A/A tests and platform validation

**Pass mark: 8/10.** Answer on paper first, then open the answers.

---

**Q1.** You run 2,000 correctly analyzed A/A tests at α = 0.05. About how many are significant, and what should the p-value histogram look like?

<details><summary>Answer</summary>

**About 100, with a flat histogram.** Under the null, a calibrated test gives P(p < x) = x for every x, so the p-values are uniform on [0, 1]. Some random scatter around 100 is normal, roughly ±10 (binomial SD √(2000·0.05·0.95) ≈ 9.7).
</details>

---

**Q2.** Your p-value histogram has a big spike near 0. What does it mean, and what is a likely cause?

<details><summary>Answer</summary>

**The method is anti-conservative**: its SEs are too small, so it produces too many false wins. A classic cause is analyzing at a finer unit than you randomized (sessions vs. users, Day 4) without the delta method or clustering. Other causes: heavy outliers, peeking, or unmodeled correlation over time.
</details>

---

**Q3.** The histogram piles up near 1 instead. Is that fine because there are few false positives?

<details><summary>Answer</summary>

**No.** It's **conservative**: the SEs are too large, so the test will miss real effects (low power). You saw this on Day 3, where the unclustered panel DiD had about 3% power and 100% coverage. A good method is calibrated, neither too strict nor too loose.
</details>

---

**Q4.** Why use a KS or Anderson-Darling test instead of eyeballing the histogram?

<details><summary>Answer</summary>

Histograms of a few hundred p-values look lumpy even when they're perfectly uniform, and real problems can be subtle, for example a 7% FPR. A formal test gives an objective, automatable pass/fail check, which is what a platform needs to run across thousands of metrics. Microsoft ExP uses Anderson-Darling for this.
</details>

---

**Q5.** In your harness, the naive session z-test had FPR ≈ 11.4%. If your team used it for 50 launch decisions where no feature truly worked, how many false "wins" would you expect, compared with a correct method?

<details><summary>Answer</summary>

**About 5.7 vs. about 2.5.** That's 50 × 0.114 versus 50 × 0.05, roughly double the false wins. Each false win ships a useless or harmful change and teaches the team the wrong lessons.
</details>

---

**Q6.** A bug moves 2% of treatment users (1% of all users) into control, as in your homework. Counts become N/2 + k and N/2 − k with k = 0.01·N. Using χ² = 4k²/N, what is χ² at N = 10,000 and at N = 200,000?

<details><summary>Answer</summary>

**4 and 80.** At N = 10,000, k = 100 and χ² = 4·100²/10,000 = 4 (p ≈ 0.05, below the 10.8 needed for p < 0.001). At N = 200,000, k = 2,000 and χ² = 4·2,000²/200,000 = 80. For a fixed-percentage bug, χ² grows **linearly with N**, so small tests rarely alarm while large ones always do. That matches your homework's 10% vs. 100% alarm rates.
</details>

---

**Q7.** How can a platform catch assignment bugs that individual small experiments are too small to detect?

<details><summary>Answer</summary>

**Pool the evidence**: run SRM checks across all experiments that share the assignment service, or on aggregate traffic per assignment code path, plus always-on A/A tests with large traffic. Also monitor the distribution of SRM p-values across experiments: it should be uniform too.
</details>

---

**Q8.** What is a "simulated A/A test on historical data", and why is it useful?

<details><summary>Answer</summary>

You take past users (with no experiment running), randomly split them many times, and compute the metric's test each time. It's a cheap, risk-free way to vet a **new metric** or variance method before it's used for real decisions. Microsoft found, for example, that metrics with heavy outliers fail this check until they're capped.
</details>

---

**Q9.** Which of these would an A/A test NOT catch?
A) A broken variance formula
B) An assignment bug causing an SRM
C) A treatment that harms long-term retention
D) A logging pipeline that drops events in one arm

<details><summary>Answer</summary>

**C.** An A/A test has no treatment, so it can't reveal a real treatment's effects. It validates the **measurement system** (stats, assignment, logging) so that A/B results can be trusted. Long-term harm needs holdouts and long-running experiments.
</details>

---

**Q10 (interview, answer out loud in 2 minutes).** "You're joining to own the stats engine of our experimentation platform. How would you know whether it's trustworthy?"

<details><summary>Model answer</summary>

"I'd treat trustworthiness as something we measure continuously. First, **simulated A/A tests on historical data** for every metric and variance method: the p-values should be uniform (KS or Anderson-Darling), and the false positive rate should be about α. That catches unclustered ratio metrics, outlier-heavy metrics and broken variance formulas. Second, **live A/A tests** running all the time on real traffic, to catch logging and pipeline regressions. Third, **automatic SRM checks** on every experiment, plus pooled checks across experiments that share the assignment service, because small tests can't detect small assignment bugs. Fourth, I'd check **power and coverage** with simulations where we inject a known effect, to make sure we're not too conservative either. Finally, I'd publish a dashboard of these health checks so teams can see that the platform deserves their trust, and I'd add any failure to the roadmap with an owner."

**What scores well:** a systematic, automated and continuous approach, both directions of error (false positives and lost power), and making trust visible (Staff-level).
</details>

---

### Scoring
| Score | Next step |
|---|---|
| 9–10 | Week 1 complete 🎉 Sunday review next |
| 8 | Pass. Re-read the explanations for the questions you missed |
| ≤ 7 | Re-read lesson §1.1–1.4 and the Microsoft article, then retake |
