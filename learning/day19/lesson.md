# Day 19 (Week 4, Day 2): Group sequential designs: alpha spending, O'Brien-Fleming, Pocock

**Time:** about 90 minutes (35 study, 35 homework, 15 quiz)
**Job skill:** "sequential testing" (OpenAI). Spotify's experimentation platform uses exactly this method (group sequential tests with Lan-DeMets alpha spending).

## 1. Concepts

### 1.1 The idea
Plan **K interim looks** in advance (e.g. at 25%, 50%, 75% and 100% of the sample). At each look k, stop and declare a winner if |z_k| > c_k. Choose the boundaries c_k so that the **total** chance of a false positive across all looks is α = 5%.

### 1.2 Alpha spending (Lan & DeMets, 1983)
Instead of fixing the boundaries directly, choose a **spending function** α(t): how much of the 5% you're allowed to "use up" by information fraction t (t = share of the planned sample collected).
| Spending function | Formula | Behavior |
|---|---|---|
| **O'Brien-Fleming type** | α(t) = 2 − 2Φ(z₁₋α/₂ / √t) | Spends almost nothing early, keeps most for the end |
| **Pocock type** | α(t) = α·ln(1 + (e − 1)t) | Spends α evenly, so the boundary is almost constant |

Then solve for the boundaries: the probability of *first* crossing at look k equals the α spent at look k. You do this by simulation in today's homework. Lan-DeMets also lets you **change the number or timing of looks** as data arrive, as long as you follow the spending function.

### 1.3 Your homework results (K = 4, α = 0.05)
| | Boundaries \|z\| | Power (fixed-n design: 80%) | Expected sample |
|---|---|---|---|
| **O'Brien-Fleming** | 3.88, 2.78, 2.30, **2.04** | **79%** | 81% of max |
| **Pocock** | 2.37, 2.37, 2.37, 2.35 | 72% | **72%** of max |

- **OBF:** very hard to stop early (you'd need |z| ≈ 3.9 at 25%), and the final boundary is almost the usual 1.96, so you **lose almost no power** while keeping the option to stop early for a huge effect. This is the most common choice, in clinical trials and on tech platforms.
- **Pocock:** stops earlier on average, but the final boundary is 2.35, so **more power is lost**, and an early "win" at p ≈ 0.018 is less persuasive.

### 1.4 In practice
- Fits **batch data**, e.g. daily metric pipelines (Spotify chose group sequential tests for this reason).
- Needs a **planned maximum sample size**, and enough data at each look for the normal approximation to hold.
- Use **futility boundaries** (stopping for lack of effect) only if they're pre-specified.
- Effect estimates at an early stop are still biased upward (the winner's curse, Day 18). Report them with caution, or with bias-adjusted methods.

## 2. Study materials (in this order)
1. 📖 ⭐ **Spotify, "Choosing a Sequential Testing Framework: Comparisons and Discussions"** (why Spotify uses group sequential tests with Lan-DeMets spending; about 15 min): https://engineering.atspotify.com/2023/03/choosing-sequential-testing-framework-comparisons-and-discussions
2. 📖 **CASRAI, "Alpha Spending Function: Pocock vs O'Brien-Fleming"** (a clear comparison): https://casrai.org/guides/group-sequential-design-alpha-spending-stopping-boundaries
3. 📖 **gsDesign documentation, Lan-DeMets spending functions** (the formulas you implemented): https://keaven.github.io/gsDesign/reference/sfLDOF.html
4. 📄 Optional: **Stata manual, "Introduction to group sequential designs"** (a thorough free PDF): https://www.stata.com/manuals/adaptgsdintro.pdf
5. 📄 Reference: **Lan & DeMets (1983), "Discrete sequential boundaries for clinical trials"**, *Biometrika* 70:659–663: https://www.semanticscholar.org/paper/Discrete-sequential-boundaries-for-clinical-trials-Lan-DeMets/b6d0906ba50119fca2843b84ded50ed63eefa6ae

## 3. Homework
```bash
python learning/day19/homework.py
```
3 parts: implement the OBF spending function, derive the boundaries by simulation, then compare FPR, power and expected sample size. Answer Q-A in `learning/day19/answers.md`.

## 4. Quiz
Take [`quiz.md`](quiz.md) (10 questions, pass mark 8/10).

## 5. Check yourself
- [ ] I can explain alpha spending and write the OBF and Pocock spending functions.
- [ ] I can explain why OBF loses almost no power, and why Pocock stops earlier but loses more.
- [ ] I know the practical requirements (planned max sample, batch looks, pre-specified futility).
- [ ] I can explain why platforms like Spotify use group sequential tests.
