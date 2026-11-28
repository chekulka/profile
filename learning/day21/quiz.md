# Day 21 quiz: choosing a stopping rule (uses your simulator table)

**Pass mark: 8/10.** Answer on paper first, then open the answers.

---

**Q1.** Naive peeking shows the highest "power" (0.82). Why should it never be used?

<details><summary>Answer</summary>

Its **false positive rate is about 24%**, not 5%. "Power" only means something for a valid test. With an inflated error rate, many of its wins are noise, and its effect estimates suffer from the winner's curse (Day 18).
</details>

---

**Q2.** Which method gives the best power while still allowing early stops, and why?

<details><summary>Answer</summary>

**O'Brien-Fleming (4 looks):** power 0.70 vs. 0.71 for fixed-n, with an average of 84% of the sample used. It spends almost no α early, so its final boundary is close to 1.96 and almost no power is lost, while early stops remain possible for large effects.
</details>

---

**Q3.** Pocock has 0.62 power but uses only 77% of the sample on average. When might you choose it over OBF?

<details><summary>Answer</summary>

When **stopping early matters more than maximum power**: for example, when every day of a bad experience is costly, or traffic is extremely expensive, and the effects you care about are large. You accept lower power (and less persuasive early stops) for faster average decisions.
</details>

---

**Q4.** Why does Bonferroni across 20 looks have such low power (0.40) even though it's valid?

<details><summary>Answer</summary>

Each look must clear |z| ≈ 3.02 (α/20 two-sided), including the final one. Because the looks are highly **correlated**, the realized FPR is only 1.8%, far below 5%, so α is wasted. Alpha-spending methods use the correlation, so they need much smaller final boundaries.
</details>

---

**Q5.** mSPRT has FPR 0.019 and power 0.44. What do you get in exchange for the lower power?

<details><summary>Answer</summary>

**Complete freedom to monitor**: you can look after every single observation, stop at any time, and keep the error guarantee for an unlimited horizon. That's ideal for guardrails, real-time operational metrics, and teams that peek constantly.
</details>

---

**Q6.** For a platform with a daily batch pipeline, which default would you choose for decision metrics?

<details><summary>Answer</summary>

**Group sequential with O'Brien-Fleming spending.** Daily batches map naturally to planned looks, the power loss is negligible (0.70 vs. 0.71), and teams get legitimate early stopping. Spotify made the same choice for the same reason.
</details>

---

**Q7.** Average sample is reported under a *real* effect. Why does that number matter for a platform?

<details><summary>Answer</summary>

It measures **traffic and time saved**: with real effects, sequential methods often stop early, freeing users for the next experiment. Across hundreds of experiments, a 16% saving (OBF) means many more tests per year, a direct business benefit to quote when proposing the method.
</details>

---

**Q8.** True or false: under H₀ (no effect), sequential methods also save sample on average.

<details><summary>Answer</summary>

**Mostly false.** Under H₀, they rarely stop early (that's what keeping FPR at 5% means), so they usually run to the maximum sample. To save traffic on losing ideas, you need **futility boundaries** (pre-specified), which is a stretch goal in today's project.
</details>

---

**Q9.** How would you validate that your platform's sequential implementation is correct?

<details><summary>Answer</summary>

Exactly like today's simulator: **simulate streams under H₀** (FPR ≤ α for the real monitoring pattern) and **under known effects** (power and average sample match the design). Then run live **A/A tests** with the production code path. Add these simulations to CI so regressions are caught (Day 7, Day 14).
</details>

---

**Q10 (interview, answer out loud in 2 minutes).** "Present your sequential-testing recommendation to our head of data science, using evidence."

<details><summary>Model answer</summary>

"I simulated six stopping rules on the same data. Naive peeking, which is what teams do with today's dashboards, has a **24% false positive rate**, so roughly one in four of our 'wins' on null features would be false. My recommendation has three parts. **One:** decision metrics use **group sequential tests with O'Brien-Fleming spending** at daily or weekly looks. That's 70% power vs. 71% for a fixed test, the false positive rate stays at 5%, and it uses about 16% less traffic on average when effects are real. **Two:** guardrails and real-time monitoring use **always-valid mSPRT** or confidence sequences. Power is lower, but we can look at any time and stop for harm safely. **Three:** the UI only shows adjusted results, so peeking stops being harmful, and we add pre-specified futility stops to save traffic on losers. I'd roll it out with A/A validation in CI and a dashboard tracking false positive rate and traffic saved."

**What scores well:** quantified evidence from your own simulation, a clear default plus an exception, the business benefit (traffic saved), UI and process changes, and validation.
</details>

---

### Scoring
| Score | Next step |
|---|---|
| 9–10 | Week 4 project done 🎉 Sunday review next |
| 8 | Pass. Re-read the explanations for the questions you missed |
| ≤ 7 | Revisit Days 18–20 |
