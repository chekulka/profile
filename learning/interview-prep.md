# Interview prep: target roles

**Targets:** OpenAI (Data Scientist, Core Experimentation) · Discord (Staff Data Scientist, Causal Inference & Experimentation) · Anthropic (Brand Insights, Measurement Lead). Sections 1–6 apply to all three; sections 7–8 are role-specific; section 9 is your readiness checklist.

Typical loop for this kind of role: recruiter screen → technical screen (stats + coding) → onsite with 4–5 rounds: statistics/causal inference, experimentation case, coding (Python/SQL/Spark), experimentation platform system design, and behavioral/leadership.

How to use this file: answer one section out loud every day in week 14, and from week 4 onward answer 3 random questions every Friday. Record yourself, then grade the answer for structure, correctness and clarity.

## 1. Statistics and inference
1. Derive the variance of a difference in means. Why does the CLT matter when revenue is heavily skewed?
2. What is a p-value, in words a PM would understand? What is it *not*?
3. Derive the sample size per arm for a given MDE, α and power. What changes the number most?
4. The metric is clicks/sessions and you randomize by user. Why is the naive SE wrong? Walk through the delta method.
5. When would you use the bootstrap? When does it fail?
6. Explain Type I and Type II error, and what Type S/M (sign and magnitude) errors are.
7. You test 20 metrics and 1 is significant. What do you do? Compare Bonferroni, Holm and Benjamini-Hochberg.

## 2. Experimentation methodology (the job's named topics)
1. **CUPED:** derive θ = cov(Y, X)/var(X) and the variance reduction (1 − ρ²). Which covariate do you pick? What happens for new users with no pre-period data?
2. **CUPED vs. regression adjustment** (Lin 2013): when do they differ? Is there any bias risk?
3. **Sequential testing:** why does peeking inflate false positives? Compare O'Brien-Fleming, mSPRT and confidence sequences. Which would you ship in a platform, and why?
4. **SRM:** a 50/50 test shows 50.6/49.4 with 2M users. Is that an SRM? List 5 root causes and how you'd debug each.
5. **Metric design:** design an OEC for ChatGPT. Include guardrails, how you'd measure sensitivity, and how you'd find long-term surrogates.
6. **Heterogeneous effects:** the effect is +2% overall but −5% for new users. Is that real? How do you validate it (pre-registration, multiple testing, causal forests, holdout replication)?
7. **Novelty effects:** the effect fades over 3 weeks. How do you detect it and decide whether to launch?
8. **Interference:** in a marketplace or social product, why can user-level randomization be biased? Cluster randomization, switchbacks, budget-split designs.
9. **Non-inferiority:** you're switching to a cheaper model. Set up the test, choose the margin, and size it. (Your Deloitte story goes here.)

## 3. Causal inference / quasi-experiments (diff-diff)
1. You launched in 5 cities first, so there's no randomization. How do you estimate the effect? (DiD → parallel trends → placebo tests → SDiD if there are few cities)
2. Why is TWFE biased with staggered adoption? Explain "forbidden comparisons" and negative weights (Goodman-Bacon).
3. What does Callaway-Sant'Anna estimate? Explain ATT(g,t) and the choice between never-treated and not-yet-treated controls.
4. Your pre-trend test is not significant. Are you done? (No: low power (Roth 2022), Honest DiD bounds.)
5. When do you pick synthetic control, SDiD or DiD?
6. You have 8 clusters. How do you do inference? (Wild cluster bootstrap)
7. Eligibility depends on a score ≥ 700. What design? How do you test for manipulation?
8. Walk through the 8-step practitioner workflow from `diff-diff-map.md`.

## 4. Coding (practice in Python, SQL and PySpark)
1. Implement a two-sample t-test and a delta-method SE from scratch in numpy.
2. Implement CUPED as a function and verify the variance reduction by simulation.
3. Simulate peeking: run 10,000 A/A tests with daily looks and report the false positive rate.
4. SQL: compute per-user metrics from an events table, join to assignments, and compute the difference and SE per variant.
5. SQL: detect SRM by day and by platform.
6. PySpark: compute sufficient statistics (n, Σy, Σy², Σxy) per variant per day for 1B rows. Why sufficient statistics?
7. Deterministic hash-based assignment (salted user_id → bucket). Check that it's uniform.

## 5. System design: experimentation platform
Prompt: *"Design an experimentation platform for 500M weekly users and 1,000 concurrent experiments, including ML model experiments."*
Cover: assignment service (hashing, layers/namespaces, holdouts), exposure logging, metric definitions layer (semantic layer), batch and streaming metric computation (Spark), sufficient statistics, the stats engine (CUPED, sequential testing, SRM checks built in), guardrails and auto-stop, interference handling, a self-serve UI and readouts, data quality and observability, and trade-offs (latency vs. correctness, flexibility vs. safety).
Also practice: *"How would you A/B test a new LLM version when outputs are non-deterministic and quality is subjective?"*

## 6. Behavioral and leadership (STAR stories to prepare from your resume)
| Prompt | Your story |
|---|---|
| Influenced technical strategy | Standardized testing and review process at Vanguard → 25% success rate |
| Big measurable impact | Cash Growth: 5 experiments → 19K accounts in a month |
| Rigor under pressure | Deloitte non-inferiority staged rollout (5% → 20% steps) |
| Built something novel | Patented LBP artifact detection, still in production (2025 paper) |
| Mentored / raised the bar | KPI framework + self-serve dashboards adopted across teams |
| Disagreed with a stakeholder | (Prepare: a launch you argued against because of the data) |
| A failure | (Prepare: an experiment that was invalid, e.g. an SRM, and what you changed afterward) |

## 7. Discord: Staff Data Scientist, Causal Inference & Experimentation
*What they emphasize: statistically sound experiments, best-practice methods, setting the Experimentation Platform roadmap, causal inference that drives decisions, and publications (a bonus).*
1. **Network effects:** you test a new voice-channel feature. Users in the same server affect each other. Why is user-level randomization biased, and which way? Compare server-level (cluster) randomization, graph-cluster randomization and ego-network designs, and their power costs.
2. **Two-sided effects:** a feature changes how *senders* behave, but the value lands on *receivers*. How do you measure both? (Hint: think about which unit you randomize and which unit you measure.)
3. **Server-level tests:** there are 10,000 eligible servers with very different sizes. How do you analyze them? (Cluster-robust SEs, ratio metrics, the delta method, stratifying by size, CUPED at the server level.)
4. **Quasi-experiments:** a policy change (e.g. new safety rules) rolled out to all servers in a region on one date. Walk through DiD vs. synthetic control vs. RD on server age or size, and the diagnostics you'd show.
5. **Platform roadmap (Staff-level):** "You join and find teams peeking, ignoring SRM, and analyzing 40 metrics per test. What do you put on the platform roadmap for the next two quarters, in what order, and how do you get teams to adopt it?" (Prioritize by impact on decision quality: SRM auto-checks, a sequential testing default, guardrails and OEC, CUPED, a metric catalog, readout templates, education.)
6. **Long-term effects:** engagement features can look good in 2 weeks and hurt retention in 6 months. Discuss holdouts, surrogate indices and long-running holdbacks.
7. **Teen safety and trust:** how do you run experiments when some outcomes are sensitive (harassment, safety)? Guardrail metrics, ethics review, minimizing exposure, quasi-experimental alternatives.
8. **Publications:** be ready to discuss your paper (week 14) and the patent: the problem, the method, the evidence, and what you'd do differently.

## 8. Anthropic: Brand Insights, Measurement Lead
*What they emphasize: whether marketing spend is working, the brand funnel (awareness → consideration → pipeline), executive readouts, brand health trackers and vendors, MMM, MTA and incrementality.*
1. **"Is our brand spend working?"** Walk the CMO through your measurement framework: triangulating MMM, lift tests and attribution, what each can and can't tell you, and how you resolve disagreements between them.
2. **Geo-lift:** design an incrementality test for a $5M brand campaign in 10 US metros. Market selection, synthetic control vs. synthetic DiD, test length, power, and the readout.
3. **MMM:** explain adstock and saturation. Why does MMM need calibration? How do lift-test results become MMM priors (`to_meridian_roi_prior`, `to_pymc_marketing_lift_test`)?
4. **Attribution:** why is last-touch (and multi-touch) attribution not causal? When is it still useful?
5. **Brand tracker:** awareness rose 4 points quarter over quarter. Is that real? Discuss sampling error, weighting, panel changes, vendor methodology shifts, and seasonality.
6. **B2B vs. prosumer:** how does measurement differ for long B2B sales cycles (lagged pipeline effects, small samples) compared with prosumer signups?
7. **Executive readout:** you have 5 minutes with the CMO and the numbers are mixed. Structure the story: headline, confidence, drivers, recommendation, next test.
8. **Vendor management:** a survey vendor changed its sampling method mid-year. How do you detect the break and bridge the series?

## 9. Readiness checklist
- [ ] I can derive CUPED, the delta method and sample size on a whiteboard without notes
- [ ] I can explain staggered DiD bias and CS/SA in 2 minutes
- [ ] I've built the capstone toolkit and can demo it
- [ ] 3 full mock onsites done, each scored ≥ 4/5
- [ ] 7 STAR stories written and rehearsed
- [ ] Discord: a 2-quarter platform roadmap I can present in 10 minutes
- [ ] Anthropic: a mock "Is brand spend working?" executive readout (week 9 weekend)
