# Day 13 (Week 3, Day 2): Regression adjustment done right

**Time:** about 90 minutes (35 study, 35 homework, 15 quiz)
**Job skill:** "variance reduction" and "deep expertise in statistics" (OpenAI); "best practices in causal inference" (Discord). This is the theory behind CUPED, and interviewers love the bad-control trap.

## 1. Concepts

### 1.1 From CUPED to regression adjustment
Yesterday, CUPED subtracted θ(X − X̄). Regression does the same thing with any number of pre-treatment covariates:

  **Y = α + τ·T + β·(X − X̄) + ε**, where τ̂ is the adjusted treatment effect

### 1.2 Freedman's critique, and Lin's fix
Freedman (2008) showed that the common-slope regression above (**ANCOVA**) can actually be *less* precise than doing nothing when:
- the split is **unequal** (e.g. 80/20), **and**
- the covariate's slope **differs by arm** (heterogeneous effects).

**Lin (2013)'s fix:** include the **interaction**, which gives each arm its own slope:

  **Y = α + τ·T + β·(X − X̄) + γ·T·(X − X̄) + ε**, with **HC2 robust SEs**

With **centered** X, τ̂ is the ATE, and adjustment **can't hurt asymptotic precision**. In today's homework (80/20 split, slope 3 vs. 0), the SD of the estimate is 0.19 unadjusted, **0.27 with ANCOVA (worse!)** and **0.18 with Lin**.
Practical rule: **center the covariates, interact them with treatment, and use robust SEs.**

### 1.3 Choosing covariates
✅ **Good:** anything fixed **before randomization**: pre-period metrics (the best), signup cohort, country, device at assignment.
❌ **Bad controls:** anything the treatment can affect: in-experiment sessions, clicks, "converted users only", time spent. Adjusting for a **mediator** removes the very effect you're measuring (homework: a real +$6 becomes −$0.07).
- Adding a few **irrelevant** pre-treatment covariates costs almost nothing at large n (Part 3), but don't add hundreds with small n.

### 1.4 How this connects
- **CUPED** = adjustment with one pre-period covariate.
- **CUPAC / ML adjustment** = adjustment with a model's prediction (Day 14).
- **DiD with covariates** in diff-diff (week 5) relies on the same idea: covariates that are pre-treatment.

## 2. Study materials (in this order)
1. 📄 ⭐ **Lin (2013), "Agnostic notes on regression adjustments to experimental data: Reexamining Freedman's critique"** (Annals of Applied Statistics). Read the abstract, §1 and the main result in §3 (about 30 min): https://arxiv.org/abs/1208.2301
2. 📄 **Cinelli, Forney & Pearl, "A Crash Course in Good and Bad Controls"** (*Sociological Methods & Research*). Read the first few "models" with their diagrams (about 20 min): https://journals.sagepub.com/doi/full/10.1177/00491241221099552
3. 📖 Review **Facure ch. 5, "The Unreasonable Effectiveness of Linear Regression"** (the regression and bias sections): https://matheusfacure.github.io/python-causality-handbook/05-The-Unreasonable-Effectiveness-of-Linear-Regression.html

## 3. Homework
```bash
python learning/day13/homework.py
```
3 parts with automatic checks. Write answers to Q-A and Q-B in `learning/day13/answers.md`.

## 4. Quiz
Take [`quiz.md`](quiz.md) (10 questions, pass mark 8/10).

## 5. Check yourself
- [ ] I can write Lin's regression and explain why X is centered and interacted.
- [ ] I can explain when ANCOVA without interaction can hurt (Freedman).
- [ ] I can spot a bad control (mediator or post-treatment variable) and explain the bias.
- [ ] I know what makes a good covariate and why junk covariates are cheap at large n.
