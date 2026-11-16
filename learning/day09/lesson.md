# Day 9 (Week 2): Metric design: OEC, guardrails, sensitivity and proxies

**Time:** about 90 minutes (35 study, 35 homework, 15 quiz)
**Job skill:** "metric design" (OpenAI), "set the technical bar for experimentation" (Discord), "connect awareness to pipeline" (Anthropic)

## 1. Concepts

### 1.1 Three kinds of metrics (Kohavi's taxonomy)
| Type | Role | Example (chat product) |
|---|---|---|
| **Goal / north star** | What the business ultimately wants; often slow and insensitive | 6-month retention, revenue |
| **Driver / proxy / surrogate** | Moves fast, *predicts* the goal, used to decide tests | 7-day active days, successful sessions |
| **Guardrail** | Must not get worse; protects users and the business | Latency, crash rate, safety flags, support contacts |

The **OEC** (overall evaluation criterion) is the metric, or the weighted combination of metrics, that you pre-commit to as the decision rule.

### 1.2 Two properties of a good decision metric
1. **Sensitivity:** it moves detectably when the product really changes.
   *Sensitivity ≈ P(the change moves the metric) × statistical power.*
2. **Directionality:** when it moves, it moves in the direction of real long-term value. "Time on page" can rise because users are *confused*, and that's a metric that points the wrong way.

### 1.3 Heavy tails kill sensitivity
In today's homework, a change that makes **8% more users buy** is detected:
- **73%** of the time by *conversion*
- **12%** of the time by *raw revenue* (whales add enormous variance)
- **39%** of the time by *revenue capped at the 90th percentile of order value*

Capping (winsorizing) trades a little **bias**, since it changes the estimand to "revenue with orders above $X counted as $X", for a big **variance** reduction. Pre-register the cap. Day 2 covered the CLT side of the same problem.

### 1.4 Proxies must be validated on *past experiments*
A proxy's correlation with the north star **across users** isn't enough. You need the correlation of **treatment effects** across experiments: when an experiment moved the proxy, did it move the north star? Netflix and others learn proxies from hundreds of past experiments. In the homework, the clicks proxy (B) points the **wrong direction on retention 65% of the time**, which is worse than a coin flip.

### 1.5 Goodhart's law
*"When a measure becomes a target, it ceases to be a good measure."* Teams optimizing clicks will find ways to raise clicks that don't create value: notifications, clickbait, friction. Guardrails and a north star review are the defense.

## 2. Study materials (in this order)
1. 📖 ⭐ **Netflix TechBlog, "Improve Your Next Experiment by Learning Better Proxy Metrics From Past Experiments"** (2024, about 6 min): https://netflixtechblog.com/improve-your-next-experiment-by-learning-better-proxy-metrics-from-past-experiments-64c786c2a3ac
2. 📄 **Deng & Shi (2016), "Data-Driven Metric Development for Online Controlled Experiments: Seven Lessons Learned"** (KDD '16, Microsoft). Read the lessons on sensitivity and directionality: https://dl.acm.org/doi/10.1145/2939672.2939700
3. 📄 Related, optional: **"A Dirty Dozen: Twelve Common Metric Interpretation Pitfalls in Online Controlled Experiments"** (KDD '17): https://dx.doi.org/10.1145/3097983.3098024
4. 📘 Optional: Kohavi et al., ch. 6, "Organizational Metrics", and ch. 7, "Metrics for Experimentation and the OEC"

## 3. Homework
```bash
python learning/day09/homework.py
```
2 parts with automatic checks. Write answers to Q-A and Q-B in `learning/day09/answers.md`.

## 4. Quiz
Take [`quiz.md`](quiz.md) (10 questions, pass mark 8/10).

## 5. Check yourself
- [ ] I can define goal, driver and guardrail metrics, and the OEC, with examples.
- [ ] I can explain sensitivity vs. directionality and give a metric that fails each.
- [ ] I can explain why capping improves power and what it costs.
- [ ] I know why proxies must be validated on *experiment-level* effects.
- [ ] I can state Goodhart's law and how guardrails defend against it.
