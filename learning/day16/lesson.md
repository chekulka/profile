# Day 16 (Week 3, Day 3): CUPAC (ML-based variance reduction) and post-stratification

**Time:** about 90 minutes (35 study, 40 homework, 15 quiz)
**Job skill:** "variance reduction, CUPED" (OpenAI). CUPAC is what you propose when CUPED isn't enough, and it's a strong talking point for the Staff-level platform-roadmap question (Discord).

## 1. Concepts

### 1.1 Where CUPED runs out
CUPED's gain is 1 − ρ² for **one** covariate. When no single pre-period metric predicts the outcome well (new users, nonlinear behavior, many weak signals), ρ is small and so is the gain. In today's homework, the best single feature keeps **93%** of the variance.

### 1.2 CUPAC: Control Using Predictions As Covariates (DoorDash, 2020)
1. Train an ML model on **historical** data to predict the outcome from **pre-assignment features** (past behavior, platform, geography, time).
2. For each experiment user, compute the prediction ŷ from features fixed *before* assignment.
3. Use ŷ as the CUPED covariate: **Y − θ(ŷ − ŷ̄)**.

The model squeezes many nonlinear signals into a single highly correlated covariate. Homework: **variance kept drops from 93% to 17%**, nearly 6× the effective traffic. It stays unbiased (mean estimate ≈ the true 0.2) because ŷ depends only on pre-treatment information.

**Rules:**
- Features must be **unaffected by treatment** (the same rule as for any covariate).
- **Don't train on the experiment's own post-assignment outcomes** in a way that leaks treatment. Use historical data, or **cross-fitting** (train on folds and predict on held-out users), as in double ML.
- Monitor model drift: a stale model still gives unbiased results, just smaller gains.

### 1.3 Stratification and post-stratification
- **Stratified randomization (blocking):** randomize within strata (platform, country) so the arms are balanced by design.
- **Post-stratification:** randomize normally, then estimate **Σₛ wₛ(ȳ_T,s − ȳ_C,s)** with wₛ = stratum share. Miratrix, Sekhon & Yu (2013) show it performs almost as well as blocking in large samples, but too many tiny strata can *increase* variance.
- It equals regression with stratum dummies and interactions, a special case of Lin's estimator (Day 13).
- Homework: post-stratifying on platform cuts the SD by about 9%. That's a modest gain, but it's simple and transparent.

### 1.4 The variance-reduction toolbox so far
| Method | Uses | Typical gain | Complexity |
|---|---|---|---|
| Capping (Day 9) | Heavy tails | Large for revenue | Low |
| Post-stratification | A few strong categories | Small–moderate | Low |
| CUPED (Day 12) | One strong pre-period metric | 1 − ρ², often about 50% | Low |
| Lin regression (Day 13) | Several covariates | ≥ CUPED | Medium |
| **CUPAC / ML** | Many nonlinear pre-period signals | Often the largest | Higher (a model to maintain) |

## 2. Study materials (in this order)
1. 📖 ⭐ **DoorDash, "Improving Experimental Power through Control Using Predictions as Covariate (CUPAC)"** (about 12 min): https://careersatdoordash.com/blog/improving-experimental-power-through-control-using-predictions-as-covariate-cupac/
2. 📄 **Miratrix, Sekhon & Yu (2013), "Adjusting treatment effect estimates by post-stratification in randomized experiments"** (JRSS-B). Read the abstract and introduction (free on Harvard DASH): https://dash.harvard.edu/entities/publication/73120379-04ed-6bd4-e053-0100007fdf3b
3. 📖 **TOPBOTS, "Online Experiments Tricks: Variance Reduction"** (an overview comparing CUPED, CUPAC and stratification): https://www.topbots.com/online-experiments-variance-reduction/
4. 📄 Optional: **Tang et al., "Control Using Predictions as Covariates in Switchback Experiments"** (CUPAC for marketplace switchbacks): https://www.researchgate.net/publication/345698207_Control_Using_Predictions_as_Covariates_in_Switchback_Experiments

## 3. Homework
```bash
pip install scikit-learn   # added to learning/requirements.txt
python learning/day16/homework.py
```
3 parts with automatic checks. Write answers to Q-A and Q-B in `learning/day16/answers.md`.

## 4. Quiz
Take [`quiz.md`](quiz.md) (10 questions, pass mark 8/10).

## 5. Check yourself
- [ ] I can explain the CUPAC recipe in 3 steps and why it stays unbiased.
- [ ] I know the leakage risk and how cross-fitting or historical training prevents it.
- [ ] I can write the post-stratified estimator and explain when it helps or hurts.
- [ ] I can choose a variance-reduction method for a given situation (the table in §1.4).
