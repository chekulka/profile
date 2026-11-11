# Experimentation & Causal Inference Mastery: 14-Week Plan

**Goal:** become an expert in the `diff-diff` library and be ready for these target roles:
| Role | Company | Weeks that matter most |
|---|---|---|
| Data Scientist, Core Experimentation | OpenAI | 1–7, 10–13 |
| Staff Data Scientist, Causal Inference & Experimentation | Discord | 1–7, 10–13 (+ the paper in week 14) |
| Brand Insights, Measurement Lead | Anthropic | 1–2, 5–9 (marketing measurement track) |
**Pace:** about 90 minutes on weekdays plus a 2–3 hour weekend project. Each day folder has `lesson.md`, `homework.py` and your `answers.md`.

- [`diff-diff-map.md`](diff-diff-map.md): every diff-diff estimator and tool, mapped to the day it's taught
- [`interview-prep.md`](interview-prep.md): question bank, coding drills, system design, STAR stories
- [`resources.md`](resources.md): curated videos, PDFs and tutorials
- **A new lesson arrives every day at 7am Central.** Weekdays follow the syllabus below; Saturday is the weekend project and Sunday is a weekly review quiz.
- Each day folder contains:
  - `lesson.md`: concepts, plus the videos, PDFs and tutorials to study (with exact chapters and timestamps where possible)
  - `homework.py`: hands-on coding with self-checks
  - `quiz.md`: 10 questions with hidden answers and explanations; pass mark 8/10
  - `answers.md` (you write this): homework answers + your quiz score. Committing it gets you feedback the next morning.

| Job requirement | Where it's covered |
|---|---|
| Statistics, causal inference, online experimentation | Weeks 1–2, 5–7, 10 |
| Variance reduction, CUPED | Week 3 |
| Sequential testing | Week 4 |
| SRM detection, metric design | Week 2 |
| Marketing measurement: MMM, attribution, incrementality, brand surveys (Anthropic) | Weeks 8–9 |
| Heterogeneous effects | Week 11 |
| Python + Spark, scalable pipelines, data models | Week 12 |
| Platform at scale and roadmap; ML, ranking, social and marketplace experiments (OpenAI, Discord) | Week 13 |
| Communicating statistics, technical leadership | Every Friday + Week 14 |

## Phase 1: Experimentation foundations
**Week 1: Causal foundations + first DiD**
1. Potential outcomes, 2x2 DiD by hand and with `DifferenceInDifferences` (Card & Krueger)
2. Hypothesis testing done right: t-test vs. regression, CLT, non-normal metrics, bootstrap
3. Power and MDE: analytical vs. simulation (`compute_mde`, `simulate_power`)
4. Ratio metrics and the delta method (CTR, revenue per session); clustered randomization units
5. Communication: one-page experiment readout + weekend project (simulate and analyze 1,000 A/A tests)

**Week 2: Trustworthy experiments**
1. SRM: chi-square test, root causes, debugging a real SRM case
2. A/A tests, false positive rates, p-value distributions
3. Metric design: OEC, guardrails, sensitivity vs. directionality, surrogate metrics
4. Novelty and primacy effects, carryover, interference/SUTVA violations
5. Multiple testing: FWER vs. FDR, many metrics × many segments

**Week 3: Variance reduction**
1. CUPED derivation (Deng et al. 2013) and implementation from scratch
2. Regression adjustment (Lin 2013), CUPED as OLS, choosing covariates
3. CUPAC/ML-based adjustment; stratification and post-stratification
4. Variance reduction for ratio metrics; how much power you actually gain
5. Weekend: build a `cuped()` function + benchmark notebook (portfolio piece)

**Week 4: Sequential testing**
1. The peeking problem, simulated
2. Group sequential designs: alpha spending, O'Brien-Fleming, Pocock
3. Always-valid inference: mSPRT, confidence sequences (Johari et al.; Howard et al.)
4. Bayesian A/B testing and what "probability to beat control" really means
5. Weekend: sequential testing simulator comparing methods

## Phase 2: Quasi-experiments with `diff-diff`
**Week 5: DiD core**
1. Parallel trends: `check_parallel_trends`, `equivalence_test_trends`, what pre-tests can't prove
2. Covariates, fixed effects, cluster-robust vs. wild bootstrap SEs (few clusters)
3. Placebo tests: `run_all_placebo_tests`, permutation, leave-one-out
4. Power for DiD + pre-trends power (Roth 2022: `compute_pretrends_power`)
5. Weekend: a full 2x2 analysis following the 8-step practitioner workflow

**Week 6: Staggered rollouts (the most common case in industry)**
1. Why TWFE fails: Goodman-Bacon decomposition (`BaconDecomposition`), negative weights
2. Callaway & Sant'Anna (`CallawaySantAnna`) on `mpdta`: ATT(g,t) and aggregations
3. Sun & Abraham event studies (`SunAbraham`), `plot_event_study`
4. Imputation (Borusyak et al.), two-stage (Gardner), stacked DiD: comparing estimators
5. Weekend: analyze a staggered feature rollout with 3 estimators and reconcile them

**Week 7: Sensitivity and few treated units**
1. Honest DiD (Rambachan & Roth): `compute_honest_did`, breakdown values
2. Synthetic control (`SyntheticControl`, Prop 99) and placebo inference
3. Synthetic DiD (`SyntheticDiD`): when you have few treated markets
4. Triple differences, continuous treatment (`ContinuousDiD`), spillovers
5. Weekend: geo-experiment case study (marketing lift in a few markets)

## Phase 2b: Marketing measurement track (for the Anthropic role)
**Week 8: Brand and incrementality measurement**
1. Brand funnel metrics (awareness → consideration → pipeline) and brand health trackers: survey design, weighting, `SurveyDesign`
2. Survey-based DiD: `aggregate_survey` + the diff-diff brand awareness survey tutorial
3. Incrementality and geo-lift tests: matched markets, synthetic control, synthetic DiD for few treated markets
4. Lift-test power and design: how many markets, how long, holdout size (`simulate_power` with `SyntheticDiD`)
5. Weekend: design and analyze a mock geo-lift test for a brand campaign

**Week 9: Media mix modeling and attribution**
1. MMM foundations: adstock, saturation, seasonality, and why MMM is observational
2. Bayesian MMM in practice with PyMC-Marketing or Google Meridian
3. Calibrating MMM with lift tests: `to_pymc_marketing_lift_test`, `to_meridian_roi_prior`
4. Multi-touch attribution: models, privacy limits, and why attribution is not causal; triangulating MMM, MTA and lift tests
5. Weekend: executive readout, "Is our brand spend working?" (dashboard + 5-slide story)

## Phase 3: Beyond DiD, heterogeneity, scale, and platforms
**Week 10: Beyond DiD**
1. Regression discontinuity (`RegressionDiscontinuity`, `RDDensityTest`)
2. Instrumental variables and encouragement designs (non-compliance in experiments)
3. Switchback experiments and time-series designs for marketplaces
4. DML and doubly robust methods (`DMLDiD`); `BusinessReport` for stakeholders
5. Weekend: "method chooser" cheat sheet + mock case interview

**Week 11: Heterogeneous treatment effects**
1. CATE, subgroup analysis pitfalls, interactions with correction
2. Meta-learners (S/T/X-learners) with `econml`
3. Causal forests (Wager & Athey), honest splitting
4. Uplift modeling and policy evaluation (Qini curves)
5. Weekend: targeting policy from an experiment's results

**Week 12: Scale: Spark and pipelines**
1. PySpark fundamentals for experiment data (joins, window functions, skew)
2. Experiment data model: exposures, assignments, events, metric definitions
3. Computing metrics at scale: sufficient statistics, delta method in Spark
4. Pipeline design: Airflow orchestration (you know this), testing, data quality checks
5. Weekend: an end-to-end mini experimentation pipeline in PySpark

**Week 13: Experimentation platforms and ML experiments**
1. Platform architecture: assignment/hashing, bucketing, layers, holdouts
2. Ranking experiments: interleaving, counterfactual evaluation, off-policy estimation
3. Network interference in social and marketplace products (Discord servers, voice channels): cluster/graph randomization, ego-network designs, switchbacks, budget-split designs
4. ML/LLM experiments: offline vs. online evaluation, LLM-as-judge reliability
5. Weekend: system design: "design OpenAI's experimentation platform"

**Week 14: Capstone and interviews**
1. Capstone: open-source experimentation toolkit (CUPED + sequential + SRM + DiD wrappers)
2. Write up Paper #1, *Non-inferiority testing for safe LLM rollouts* (arXiv draft; also EB-1A evidence)
3. Mock interviews: stats theory, product case, causal inference case
4. Mock interviews: coding (Python/SQL/Spark), system design
5. Leadership stories (STAR): influencing strategy, mentoring, raising the technical bar

## Core references
- Kohavi, Tang & Xu, *Trustworthy Online Controlled Experiments* (the A/B testing standard text)
- Cunningham, *Causal Inference: The Mixtape* (free): https://mixtape.scunning.com/
- Huntington-Klein, *The Effect* (free): https://theeffectbook.net/
- Facure, *Causal Inference for the Brave and True* (free, Python): https://matheusfacure.github.io/python-causality-handbook/
- diff-diff docs and tutorials: https://diff-diff.readthedocs.io/ (offline: `diff_diff.get_llm_guide("full")`)
- Key papers: Deng et al. 2013 (CUPED); Fabijan et al. 2019 (SRM); Johari et al. 2017 (always-valid p-values); Goodman-Bacon 2021; Callaway & Sant'Anna 2021; Sun & Abraham 2021; Rambachan & Roth 2023; Arkhangelsky et al. 2021 (SDiD); Roth et al. 2023 ("What's Trending in DiD"); Baker et al. 2025 (DiD practitioner guide); Wager & Athey 2018 (causal forests)

## Progress
- [ ] Week 1 · [ ] Week 2 · [ ] Week 3 · [ ] Week 4 · [ ] Week 5 · [ ] Week 6 · [ ] Week 7
- [ ] Week 8 · [ ] Week 9 · [ ] Week 10 · [ ] Week 11 · [ ] Week 12 · [ ] Week 13 · [ ] Week 14
