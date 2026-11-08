# Day 1: Potential outcomes and your first difference-in-differences

**Time:** about 90 minutes (45 reading, 45 homework)
**Job skill:** "Deep expertise in statistics, causal inference, and online experimentation methodology"

## 1. Concepts (read and take notes)
1. **Potential outcomes:** every unit has two outcomes: Y(1) if treated and Y(0) if not. You only ever see one of them, so a causal effect is a comparison against a *counterfactual* you have to estimate.
2. **Why A/B tests work:** randomization makes treatment independent of Y(0), so the control group's mean is an unbiased estimate of the treated group's counterfactual.
3. **When you can't randomize** (geo launches, policy changes, staggered rollouts, a sales-team-led pilot), you need a *quasi-experiment*. Difference-in-differences (DiD) is the most common one in industry.
4. **2x2 DiD:** ATT = (T_post − T_pre) − (C_post − C_pre). The control group's change stands in for the trend the treated group would have followed without treatment.
5. **Key assumption, parallel trends:** without treatment, the treated and control groups would have moved in parallel. It can't be tested directly; you can only look for evidence against it (Day 3).
6. **Equivalent regression:** `y = a + b*treated + c*post + ATT*(treated*post) + e`. diff-diff fits this for you, with robust or clustered standard errors.

## 2. Read and watch
- *Causal Inference: The Mixtape* (Cunningham, free online): chapter 4 "Potential Outcomes Causal Model" and the opening of chapter 9 "Difference-in-Differences". https://mixtape.scunning.com/
- *Causal Inference for the Brave and True* (Facure, free): ch. 1 "Introduction to Causality" and ch. 13 "Difference-in-Differences". https://matheusfacure.github.io/python-causality-handbook/
- diff-diff Quickstart and Tutorial 01 (basic DiD): https://diff-diff.readthedocs.io/en/stable/quickstart.html
- Offline: `python -c "import diff_diff; print(diff_diff.get_llm_guide('practitioner'))"` prints the library's 8-step practitioner workflow (Baker et al. 2025). Skim it now; you'll master it by week 6.

## 3. Homework
```bash
pip install -r learning/requirements.txt
python learning/day01/homework.py
```
Complete every `TODO` in `homework.py` and write answers to Q6–Q9 in `learning/day01/answers.md`.

## 4. Quiz
Take [`quiz.md`](quiz.md) (10 questions, answers hidden, pass mark 8/10) and record your score in `answers.md`. Commit when you're done, and I'll review it at the next lesson.

## 5. Check yourself
- [ ] I can explain why the "naive post-only difference" is biased in Part 1.
- [ ] My hand-computed DiD matches diff-diff's ATT exactly.
- [ ] I can state the Card & Krueger result and the parallel-trends assumption in plain English.
