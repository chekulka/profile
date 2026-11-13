# Day 6 (Week 2, Day 1): Sample ratio mismatch (SRM)

**Time:** about 90 minutes (35 study, 40 homework, 15 quiz)
**Job skill:** "SRM detection" is named explicitly in the OpenAI posting, and it's also the test of whether an experimentation platform is trustworthy (Discord's platform roadmap).

## 1. Concepts

### 1.1 What SRM is
You planned a split (say 50/50), but the **observed** user counts differ from it by more than chance allows. Test with a **chi-square goodness-of-fit** test:

  χ² = Σ (observedᵢ − expectedᵢ)² / expectedᵢ, with df = number of arms − 1

With two arms at 50/50 and counts N/2 ± k, this reduces to **χ² = 4k²/N**.

### 1.2 Why it's so serious
Randomization guarantees that the two arms are comparable. An SRM means **something non-random removed (or added) users in one arm**, and the users who went missing are rarely random. In today's homework, a crash that drops low-intent Android users from the treatment logs produces a **fake +0.55 pp "win" (z = 3.3) from an experiment with zero true effect**. You can't reliably correct for it after the fact, because you don't know what the missing users would have done.

### 1.3 Where SRMs come from (Fabijan et al., 2019 taxonomy)
| Stage | Examples |
|---|---|
| **Assignment** | Buggy hashing, a changed split mid-test, users re-randomized across devices |
| **Execution** | Treatment crashes or loads slowly, redirects that drop users, a feature that changes eligibility |
| **Log processing** | Bot filtering that triggers differently by arm, lost or delayed logs, joins that drop rows |
| **Analysis** | Wrong trigger condition, inconsistent date ranges, filtering on a post-treatment variable |
| **Experimenter interference** | Ramping traffic up or down unevenly, pausing an arm, overlapping tests |

### 1.4 How to debug one
1. **Confirm** (p < 0.001, a strict threshold because SRM checks run on every test, every day).
2. **Segment the check**: by platform, browser, app version, country, new vs. existing users, and **by day**. SRMs usually concentrate somewhere.
3. Check **when** it starts (a deploy? a ramp-up?) and **where in the funnel** (assignment vs. exposure vs. analysis).
4. Fix it, then **re-run** the test. Analyzing only the unaffected segments (as in Part 4) is a diagnostic, not a final answer, because those segments may not represent everyone.

### 1.5 Sensitivity grows with N
With 1M users, an imbalance of just **±1,645 users (50.16% vs 49.84%)** triggers p < 0.001. Large platforms catch tiny bugs, and that's a good thing. Never dismiss an SRM as "only 0.2%".

## 2. Study materials (in this order)
1. 📄 ⭐ **Fabijan et al. (2019), "Diagnosing Sample Ratio Mismatch in Online Controlled Experiments: A Taxonomy and Rules of Thumb for Practitioners"** (KDD '19, Microsoft and Booking.com). Read the taxonomy and rules-of-thumb sections (about 30 min): https://dl.acm.org/doi/10.1145/3292500.3330722 (author-hosted PDF: https://exp-platform.com/Documents/2019_KDDFabijanGupchupFuptaOmhoverVermeerDmitriev.pdf)
2. 📖 **Statsig, "A quick guide to sample ratio mismatch (SRM)"** (about 10 min): https://www.statsig.com/blog/sample-ratio-mismatch
3. 🛠️ **Lukas Vermeer's SRM FAQ** (one of the paper's co-authors; the Chrome checker is retired, but the FAQ is a good read): https://www.lukasvermeer.nl/srm/docs/faq/
4. 📘 Optional: Kohavi et al., ch. 21, "Sample Ratio Mismatch and Other Trust-Related Guardrail Metrics"

## 3. Homework
```bash
python learning/day06/homework.py
```
5 parts with automatic checks. Write answers to Q-A and Q-B in `learning/day06/answers.md`.

## 4. Quiz
Take [`quiz.md`](quiz.md) (10 questions, pass mark 8/10) and record your score in `answers.md`.

## 5. Check yourself
- [ ] I can compute an SRM chi-square by hand for 2 or 3 arms.
- [ ] I can explain why an SRM invalidates results instead of just adding noise.
- [ ] I can name the 5 stages where SRMs originate, with an example of each.
- [ ] I have a step-by-step debugging plan (segment, time, funnel stage).
- [ ] I know why platforms use p < 0.001 for SRM alarms.
