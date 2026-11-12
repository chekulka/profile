# Day 5: Communicating results: the one-page experiment readout

**Time:** about 75 minutes (25 reading, 35 writing, 15 quiz). This is a lighter day, so **use the spare time to catch up on Days 1–4.**
**Job skill:** "Ability to communicate complex statistical concepts clearly to technical and non-technical audiences" (OpenAI), "executive readouts" (Anthropic), "help the company make business decisions" (Discord)

## 1. Concepts

### 1.1 A readout exists to support a decision
Executives read the first three lines. Put the **decision and the evidence** first and the method last. The structure that works:

1. **TL;DR (3 lines):** recommendation (ship / don't ship / iterate / extend), the headline effect **with a range**, and the biggest risk.
2. **Context:** the hypothesis, why it matters, and the decision this test informs.
3. **Design:** randomization unit, split, duration, primary metric, guardrails, and MDE (Day 3).
4. **Validity checks:** SRM, A/A or pre-period balance, logging issues. **If a check fails, it goes in the TL;DR**, because the results may be invalid.
5. **Results:** primary metric and guardrails, as effect + 95% CI, in absolute **and** relative terms (Day 4 delta method for the relative lift).
6. **Interpretation and risks:** what we know, what we don't, and what could make this wrong.
7. **Recommendation and next steps.**

### 1.2 Say uncertainty in plain language
| Don't say | Say |
|---|---|
| "p = 0.03, significant" | "Completion rose about 2.9% (likely between 1.6% and 4.2%)" |
| "Not significant, so no effect" | "We can't rule out anything from a 1.6% decrease to an 8.8% increase in support calls" |
| "Trending positive" | "The data are consistent with no effect; we'd need about N more users to tell" |
| "95% chance the effect is real" | (Don't. That's not what a p-value or CI means; see Day 2.) |

### 1.3 Twyman's law
*"Any figure that looks interesting or different is usually wrong."* Kohavi calls this a pillar of trustworthy experimentation. A surprisingly large win should prompt **more** checking (SRM, logging, bugs, novelty) before celebrating. Netflix's posts make the same point: surprising results more often come from implementation errors or false positives than from real effects, and **replication** is the surest way to build confidence.

### 1.4 "Not significant" on a guardrail ≠ safe
A guardrail with a wide CI that includes meaningful harm is **inconclusive, not reassuring**. Report the upper bound of the harm, and decide whether that risk is acceptable.

### 1.5 SRM (preview of Week 2)
If you planned a 50/50 split, the observed split should be close to 50/50. A chi-square test on the counts tells you whether it is. **An SRM means something non-random affected who was counted** (bugs, bots, redirects, crashes), and the effect estimates can't be trusted until you find the cause.

## 2. Study materials (in this order)
1. 📖 ⭐ **Netflix TechBlog, "Interpreting A/B test results: false positives and statistical significance"** (about 10 min): https://netflixtechblog.com/interpreting-a-b-test-results-false-positives-and-statistical-significance-c1522d0db27a
2. 📖 **Netflix TechBlog, "Interpreting A/B test results: false negatives and power"** (about 10 min): https://netflixtechblog.com/interpreting-a-b-test-results-false-negatives-and-power-6943995cf3a8
3. 📖 **Netflix TechBlog, "Building confidence in a decision"** (about 10 min): https://netflixtechblog.com/building-confidence-in-a-decision-8705834e6fd8
4. 📘 Optional: Kohavi et al., ch. 3, "Twyman's Law and Experimentation Trustworthiness"

## 3. Written exercise (instead of homework.py)
1. Run the scenario numbers (no TODOs):
   ```bash
   python learning/day05/readout_numbers.py
   ```
2. Read [`exercise.md`](exercise.md). Write the **one-page readout** and the **critique of a bad readout** in `learning/day05/answers.md`.

## 4. Quiz
Take [`quiz.md`](quiz.md) (10 questions, pass mark 8/10) and record your score in `answers.md`.

## 5. Check yourself
- [ ] My TL;DR states a decision, an effect with a range, and the top risk, in 3 lines.
- [ ] I report effects as absolute + relative with CIs, not as p-values.
- [ ] I put a failed validity check (SRM) at the top, not in an appendix.
- [ ] I can explain why "not significant" on a guardrail isn't the same as "no harm".
- [ ] I can explain Twyman's law and when to replicate.
