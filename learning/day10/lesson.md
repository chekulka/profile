# Day 10 (Week 2): Novelty, carryover and interference: when "the effect" lies

**Time:** about 90 minutes (35 study, 35 homework, 15 quiz)
**Job skill:** "practical experimentation challenges in production systems" (OpenAI); marketplace, ranking and social experiments (OpenAI, Discord); "Discord has a highly engaged community", which means network effects everywhere

## 1. Concepts

### 1.1 Novelty and primacy effects (effects that change over time)
- **Novelty:** users engage with something new *because it's new*. The effect starts big and decays.
- **Primacy (change aversion):** users dislike change at first (they have to relearn a UI). The effect starts negative and recovers.

Either way, a **short test measures the wrong thing**. In today's homework, a 1-week test reports +4.6 while the true long-run effect is +2.0.
**How to detect it:** plot the treatment effect **by day since exposure**, compare **new vs. returning users** (new users have no habits to break), run longer, or keep a long-term holdout. Google's ads study (Hohnhold et al., 2015) found long-term user learning effects big enough to change product strategy.

### 1.2 Carryover
Users remember past treatments. If you **reuse bucket assignments** from a previous experiment, the new "control" and "treatment" groups differ in their history, which biases the new test (z = −46 in an A/A test in the homework!). Fix: **re-randomize with a fresh hash salt** for each experiment, and leave washout time after harmful tests.

### 1.3 Interference: SUTVA violations
The **Stable Unit Treatment Value Assumption** says one unit's outcome depends only on its *own* treatment. It fails when units interact:
| Setting | What goes wrong | Direction of bias |
|---|---|---|
| **Marketplace / shared supply** (rides, inventory, ad budget) | Treated users take resources from control users | **Overstates** the effect (homework: +39 pp fake, true 0) |
| **Social / network** (messaging, Discord servers) | Treated users' behavior spills onto control friends | Usually **understates** it (control also benefits) |
| **Two-sided** (creators and viewers) | An effect on one side shows up on the other | Either way |

### 1.4 Designs that handle interference
- **Cluster randomization:** randomize whole markets, cities, **servers** or communities. Unbiased if clusters don't interact, but **power drops** (design effect, Day 3).
- **Switchbacks:** alternate treatment and control over time within a region (DoorDash). Each time × region block is a unit.
- **Graph-cluster / ego-network randomization:** for social networks.
- **Budget-split designs:** for ad marketplaces (split the budget, not just the users).

## 2. Study materials (in this order)
1. 📖 ⭐ **DoorDash, "Switchback Tests and Randomized Experimentation Under Network Effects at DoorDash"** (about 12 min): https://careersatdoordash.com/blog/switchback-tests-and-randomized-experimentation-under-network-effects-at-doordash/
2. 📄 **Hohnhold, O'Brien & Tang (2015), "Focusing on the Long-term: It's Good for Users and Business"** (KDD '15, Google). Read the introduction and the user-learning results: https://dl.acm.org/doi/10.1145/2783258.2788583
3. 📖 **Unofficial Google Data Science blog, "Experiment design and modeling for long-term studies in ads"** (the same work, explained): https://www.unofficialgoogledatascience.com/2015/10/experiment-design-and-modeling-for-long.html
4. 📘 Optional: Kohavi et al., ch. 22, "Leakage and Interference between Variants", and ch. 23, "Measuring Long-Term Treatment Effects"

## 3. Homework
```bash
python learning/day10/homework.py
```
3 parts with automatic checks. Write answers to Q-A and Q-B in `learning/day10/answers.md`.

## 4. Quiz
Take [`quiz.md`](quiz.md) (10 questions, pass mark 8/10).

## 5. Check yourself
- [ ] I can tell novelty from primacy effects and name two ways to detect them.
- [ ] I can explain carryover and why every experiment gets a fresh hash salt.
- [ ] I can state SUTVA and give a marketplace and a social example of violating it.
- [ ] I know which way each kind of interference biases the estimate.
- [ ] I can pick between cluster randomization, switchbacks and budget-split designs, and state their power cost.
