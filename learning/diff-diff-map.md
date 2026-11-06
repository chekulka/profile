# diff-diff (Isaac Gerber) coverage map

Library: https://github.com/igerber/diff-diff · Docs: https://diff-diff.readthedocs.io · Tested here with v4.0.0
Offline docs: `python -c "import diff_diff as d; print(d.get_llm_guide('full'))"`

Every major class and function in the library, mapped to the day it's taught. "Interview priority" says how likely it is to come up for an industry experimentation role: H = very likely, M = sometimes, L = niche, know it exists.

## Estimators
| Item | What it's for | Day | Interview priority |
|---|---|---|---|
| `DifferenceInDifferences` (`DiD`) | Basic 2x2; robust/cluster SEs, wild bootstrap, formula API | W1D1, W5D2 | H |
| `TwoWayFixedEffects` (`TWFE`) | Panel FE; `event_study=True` | W6D1 | H |
| `BaconDecomposition` (`Bacon`), `decompose_twfe_weights` | Why TWFE is biased with staggered timing | W6D1 | H |
| `CallawaySantAnna` (`CS`) | Staggered ATT(g,t) + `aggregate('group'/'event_study')` | W6D2 | H |
| `SunAbraham` (`SA`) | Interaction-weighted event study | W6D3 | H |
| `ImputationDiD` (`BJS`), `TwoStageDiD` | Borusyak-Jaravel-Spiess imputation, Gardner two-stage | W6D4 | M |
| `StackedDiD` | Wing et al. stacked sub-experiments | W6D4 | M |
| `WooldridgeDiD` (`ETWFE`) | Extended TWFE, logit/Poisson for binary/count outcomes | W6D4 | M |
| `LPDiD` | Local-projections DiD, reversible treatment | W6 weekend | L |
| `EfficientDiD` (`EDiD`) | Optimal weighting, tighter SEs | W6 weekend | L |
| `ChaisemartinDHaultfoeuille` (`DCDH`) | Treatments that turn on **and** off | W7D4 | M |
| `SyntheticControl` (`SCM`) | One treated unit (Prop 99) | W7D2 | H |
| `SyntheticDiD` (`SDiD`) | Few treated markets: geo tests | W7D3 | H |
| `TROP` | Triply robust panel with factor adjustment | W7 weekend | L |
| `TripleDifference` (`DDD`) | Two eligibility criteria | W7D4 | M |
| `ContinuousDiD`, `HeterogeneousAdoptionDiD` (`HAD`) | Dose-response; no never-treated units | W7D4 | M |
| `SpilloverDiD` | Effects leaking onto nearby controls | W7D4 | M |
| `ChangesInChanges` (`CiC`) | Distributional / quantile effects | W8D4 | L |
| `LWDiD` | Lee-Wooldridge rolling transformation, small-N exact inference | W8D4 | L |
| `DMLDiD` | Double ML DiD with high-dimensional covariates | W8D4 | M |
| `DurationDiD` | Binary "spell ended" outcomes (churn timing) | W8D4 | L |
| `RegressionDiscontinuity` (`RDD`), `RDPlot`, `RDDensityTest` | Thresholds (eligibility cutoffs), manipulation test | W8D1 | H |

## Diagnostics, sensitivity, inference
| Item | Day | Priority |
|---|---|---|
| `check_parallel_trends`, `check_parallel_trends_robust`, `equivalence_test_trends` | W5D1 | H |
| `run_all_placebo_tests`, `placebo_timing_test`, `placebo_group_test`, `permutation_test`, `leave_one_out_test` | W5D3 | H |
| `wild_bootstrap_se` (few clusters) | W5D2 | H |
| `compute_honest_did`, `HonestDiD`, `plot_sensitivity` | W7D1 | H |
| `compute_pretrends_power`, `PreTrendsPower` | W5D4 | M |
| Conley spatial HAC SEs (`vcov_type="conley"`) | W7 weekend | L |
| `SurveyDesign`, `aggregate_survey` | W8 weekend | L |

## Design and power
| Item | Day | Priority |
|---|---|---|
| `compute_mde`, `compute_power`, `compute_sample_size`, `PowerAnalysis` | W1D3 | H |
| `simulate_power`, `simulate_mde`, `simulate_sample_size`, `plot_power_curve` | W1D3, W5D4 | H |

## Data prep, reporting, workflow
| Item | Day | Priority |
|---|---|---|
| `generate_*_data`, `load_card_krueger`, `load_mpdta`, `load_prop99`, `load_castle_doctrine`, `load_walmart` | Throughout | — |
| `validate_did_data`, `balance_panel`, `wide_to_long`, `make_treatment_indicator`, `make_post_indicator`, `create_event_time`, `profile_panel` | W5D1 | M |
| `plot_event_study`, `plot_group_effects`, `plot_group_time_heatmap`, `plot_bacon`, `plot_synth_weights` | W6 | H (communication) |
| `BusinessReport`, `DiagnosticReport` | W8D4 | M |
| `practitioner_next_steps`, `get_llm_guide("practitioner")`: the 8-step Baker et al. (2025) workflow | W1D1 → W5 weekend | H |
| `to_pymc_marketing_lift_test`, `to_meridian_roi_prior` (MMM calibration) | W7 weekend | L |

## The 8-step workflow (memorize this for interviews)
1. Define the target parameter (ATT, ATT(g,t), event-time ATT; weighted or not)
2. State the identifying assumptions (which parallel-trends variant, no anticipation, overlap)
3. Probe parallel trends (and know that a non-significant pre-trend test proves nothing)
4. Choose the estimator (staggered → CS/SA/BJS, not TWFE; few treated → SDiD; simple → 2x2)
5. Estimate with the right inference (≥50 clusters: cluster-robust; fewer: wild bootstrap)
6. Sensitivity analysis (Honest DiD, placebos)
7. Heterogeneity (group / event-time aggregations)
8. Robustness (2–3 estimators, with and without covariates)
