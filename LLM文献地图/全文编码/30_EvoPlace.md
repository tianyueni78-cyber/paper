# 30｜EvoPlace 全文编码

- Source: `LLM/30_EvoPlace.md`
- Full-text status: **YES**
- Last read position: **EOF (line >480 empty); no appendix present**
- Corpus: LLM / AHD / EDA placement
- Tier: A（Mechanistically Close）

## A｜Research Content
- Research problem: automate design/evolution of heuristic-heavy optimization components in analytical global placement, and reduce expensive design-space evaluation under resource constraints.
- Problem setting: VLSI global placement on DREAMPlace-4.1; optimization components are initialization, preconditioner, optimizer.
- Objectives: minimize HPWL while maintaining comparable placement-engine runtime; discover case-specific and generalized algorithms; accelerate algorithm-level DSE.
- Algorithm backbone: offline LLM candidate generation + performance/diversity selection + LLM genetic evolution/self-reflection + UCB candidate choice; optional BO/GP/EI DSE surrogate pipeline.
- Proposed mechanism: LLM generates algorithms using CoT, placement inputs and self-reference; feasible candidates evaluated with placement engine; selection jointly considers HPWL and embedding diversity; UCB chooses candidate to evolve; HPWL/execution outcome drives reflection; DSE learns algorithm+instance surrogate from offline HPWL data and updates GP online.
- Decision layer: **Optimizer/component generation + candidate algorithm selection + design-space sampling**. Not scheduling decision.
- State / Context: original/current algorithm code, placement input features, LLM analysis, candidate HPWL, embeddings/diversity, per-candidate UCB Q/trial counts, evolution history/reflection; DSE uses algorithm embedding + placement input + sampled performance.
- Action / Decision: generate/evolve initialization/preconditioner/optimizer code; select candidate to evolve via UCB; select next design point via EI.
- Feedback / Reward: execution success/failure and HPWL improvement/degradation; normalized HPWL for UCB; placement-engine HPWL supervises surrogate.
- Dynamic mechanism: search-process adaptive candidate selection through UCB and iterative self-reflection; GP surrogate updates with newly evaluated designs. External dynamic scheduling: NOT PRESENT.
- LLM role: analyze algorithms, generate high-level ideas/code, dynamically use placement inputs, evolve code, self-reflect on execution/HPWL feedback.
- RL role: no policy-gradient/Q-learning RL in proposed EvoPlace; UCB bandit used for evolution candidate selection. RL placement methods are comparison baselines.
- Claimed contribution: LLM-based placement algorithm evolution framework; benchmark improvements under fair comparison; released code/prompts/discovered algorithms; algorithm-level DSE for constrained resources.
- Explicit limitation: no standalone Limitations section. Text explicitly notes evolution runtime as bottleneck, current objective only HPWL, generalized algorithms can diverge on other cases, some DREAMPlace implementations unavailable prevent full TILOS result release, and inference-scaling phenomenon left to future work.
- 与当前 FJSP-AGV 研究关系: strong boundary evidence. Offline candidate generation + online/evolutionary selection, performance/diversity balancing, UCB exploration-exploitation, execution feedback/reflection, instance/context inputs, performance surrogate with uncertainty, and resource-aware sampling all already exist in a complex industrial optimizer-design setting. A current FJSP-AGV contribution therefore cannot rest on these ingredients alone. Distinction must be tied to dynamic scheduling-specific multidimensional operator competence/Pareto/bottleneck context and competence-gap-driven redesign if later corpus evidence supports it.

## B｜Experimental Design Coding
- Dataset / Benchmark: MMS, modified I/O-freed ISPD2005, ISPD2019; TILOS mentioned but full results withheld.
- Instance scale: MMS table contains 16 named cases; ISPD2005 table 8 named cases; ISPD2019 detailed case count NOT REPORTED in extracted table.
- Baselines: default DREAMPlace-4.1; DREAMPlace w/ Barzilai-Borwein original and self-implementation; AutoDMP; RL placement methods WM/MaskPlace/EfficientPlace; DSE SVM/RF/XGB.
- Baseline 数量: varies by experiment; no single global baseline count.
- Independent runs: **NOT REPORTED** as a fixed number for main benchmark tables. In inference-scaling observation, generated algorithm sets are randomly sampled `multiple times`, count NOT REPORTED.
- Random seeds: fixed for stability, numeric seed **NOT REPORTED**.
- Population size: selected candidate count m symbolic; exact m NOT REPORTED.
- Generations: evolution iterations T symbolic; total trials **1000 per case**.
- Evaluation budget: at least **1000 feasible candidates per optimization component**; evolution total trials **1000 per case**; DSE comparison uses **100 design-point selections**.
- Fitness / function evaluations: candidate placement-engine HPWL evaluations; aggregate beyond stated candidate/trial budgets NOT REPORTED.
- Real decoding count: NOT REPORTED.
- Solver calls: placement-engine evaluations performed; aggregate calls NOT REPORTED.
- LLM calls: NOT REPORTED as total.
- Token budget: NOT REPORTED.
- Runtime / wall-clock: per-case placement runtime and total evolution time TT (hours) reported; DSE runtime ratio reported; DSE reduces runtime 83.50% vs exact search with 3.7% HPWL ratio loss.
- Hardware: distributed cluster **60 RTX 2080 Ti + 150 RTX 3090**; resource-constrained DSE experiment simulates one GPU.
- Metrics: HPWL, normalized HPWL ratio/improvement, placement runtime, total evolution runtime; Rudy-RSMT Pareto frontier in compatibility experiment.
- Statistical tests: **NOT REPORTED**.
- Confidence interval: **NOT REPORTED**.
- Ablation: no formal component-removal ablation section. Component-specific discovered initialization results and DSE competitor comparisons are analyses, not a full causal ablation.
- Sensitivity analysis: NOT PRESENT.
- Generalization / OOD: generalized algorithm across all cases; ISPD2019 generality; cross-benchmark DSE pretrain ISPD2019 → MMS example; TILOS observation; case-specific vs generalized contrast.
- Robustness: fixed seeds; divergence status explicitly reported; self-implementation baseline checks environment variance; formal repeated-run robustness NOT REPORTED.
- Dynamic-event design: NOT PRESENT.
- LLM API / inference cost: GPT-4o API version and embedding API reported; monetary cost NOT REPORTED.
- Fairness: DREAMPlace defaults retained, seeds fixed, latest open-source version used; original vs self-implemented BB results both shown because environment can shift case HPWL ~1%.

## C｜Writing Evidence Coding
### Introduction
Actual sequence: **M1 global-placement importance/SOTA structure → M3 existing placement algorithms → M4 heuristic/customized components and design difficulty → M3 LLM algorithm-design opportunity → M5 industrial-scale placement gap → M6 proposed framework/offline generation+evolution+DSE → empirical key findings → M7 three bullet contributions**.
- Limitation first appears in second substantive paragraph: existing optimization components are highly heuristic/customized.
- LLM-specific gap appears in `Key Motivation`: current algorithm-design works mainly address small-scale problems and not complex placement.
- Method follows immediately with `To address this challenge...`.
- Contributions: **3**, bulleted.
- Empirical diagnosis before method: uses concrete placement algorithm examples and motivating discovered-code/HPWL figures, but not a formal preliminary experiment.

### Related Work
- Two clear method-family sections: global-placement heuristics/customized algorithms; automatic algorithm design/evolution.
- traditional→LLM: YES at section level.
- generation vs selection: NOT a Related Work taxonomy.
- direct solving vs solver-assisted: NOT central.
- single heuristic vs portfolio: NOT central in RW.
- static vs adaptive / offline vs online: not RW taxonomy; appears in proposed framework/DSE.

### Gap language
- `Despite this` narrows unresolved macro initialization difficulty.
- `Nevertheless` introduces the small-scale-to-industrial placement gap.
- `However` used for candidate-selection redundancy and generalized-algorithm failure cases.
- Transition: `To address this challenge, this paper presents...`.
- Novelty strength is comparatively restrained: `current ... does not touch complex NP-hard industry challenges like placement`, not a universal `first` claim.

### Contributions
- Count: **3**; bullets: YES.
- Verbs/functions: `We propose`; `Our results demonstrate`; `We release`.
- Method contribution: algorithm-evolution framework (+ DSE in body).
- Formulation contribution: limited; no headline mathematical formulation contribution.
- Experimental contribution: multiple placement benchmarks/fair comparison.
- Benchmark contribution: NO.
- Artifact contribution: code/prompts/discovered algorithms release.

### Experimental writing
- Experiment starts with implementation/reproducibility/API/hardware/budgets, then benchmark definitions.
- Performance analysis separates case-by-case, generalized, runtime/DSE, observations/discussion.
- Fairness discussion is unusually explicit about software version and environmental differences; original and reproduced baseline variants are both shown.
- Generalization is not asserted only from average score: authors separately test a single generalized algorithm and acknowledge divergence on some cases.
- No formal significance testing/CI; no standard ablation section.
- Computational cost is central: GPU cluster, TT hours, placement runtime, one-GPU DSE simulation and 100-point constrained sampling are reported.
