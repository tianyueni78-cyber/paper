# 78｜Automated Design of Metaheuristic Algorithms: A Survey 全文编码

- Source: `LLM/78_Survey-Metaheuristic-Design.md`
- Full-text status: **YES**
- Last read position: **EOF (line >800 empty); no appendix present**
- Corpus: LLM / HH / automated metaheuristic design conceptual foundation
- Tier: A

## A｜Research Content
- Research problem: systematize automated design of metaheuristic algorithms and distinguish it from adjacent fields.
- Problem setting: offline automated metaheuristic design over a target problem/domain, abstracted into design space, design strategy, performance evaluation strategy and target problems.
- Objectives: provide taxonomy, compare representative techniques, discuss strengths/weaknesses/usability, identify future directions.
- Algorithm backbone: survey/taxonomy; NOT an experimental algorithm.
- Proposed mechanism: four-module abstraction: **Design Space → Design Strategy → Performance Evaluation Strategy → Target Problem**.
- Decision layer: primarily **Optimizer design / Operator generation / algorithm composition**. The paper explicitly distinguishes automated design from **Algorithm selection**, and places online AOS/hyper-heuristic outside its primary offline scope.
- State / Context: conceptual. Offline design targets a finite set of instances; online design may instead use search trajectory, but online AOS/HH is outside survey scope.
- Action / Decision: choose/combine computational primitives or existing algorithmic operators and configure parameters to instantiate algorithms.
- Feedback / Reward: algorithm performance on target instances; metrics include solution quality, running time, anytime performance and multiple metrics.
- Dynamic mechanism: paper explicitly recognizes offline vs online distinction. RL is described as suitable for fine-grained design, long-term planning and online design; AOS/HH is associated with online search trajectory.
- LLM role: model-based design strategy that can bootstrap human knowledge, generate code/algorithms without an explicit predefined design space, and support human-machine interaction. This is a survey-level conceptual category, not a tested LLM mechanism here.
- RL role: model-based design strategy; sequentially chooses design components using state/action/reward; can reveal component contribution and support online design.
- Claimed contribution: broad taxonomy beyond prior configuration/design surveys; four-module view; usability/challenge comparison; future trends.
- Explicit limitation/scope: survey focuses on **offline automated design**; online design is largely left to HH/AOS literature. It also notes unclear causal contribution of design space/strategy/evaluation strategy, computational expense, benchmark-heavy literature and need for real-world problems.
- 与当前 FJSP-AGV 研究关系: **highly relevant conceptual boundary**. It makes a clean distinction between (1) designing/customizing an algorithm, (2) selecting an existing algorithm from a portfolio, and (3) online AOS/HH using search trajectory. Therefore the current paper must state whether LLM changes the **action space** (operator design) or **action selection** (operator selection), rather than collapsing both into “LLM-assisted optimization.” It also provides historical precedent for performance models/surrogates and algorithm portfolios, so competence estimation alone is not novel.

## B｜Experimental Design Coding
- Dataset / Benchmark: survey; NOT APPLICABLE as a single experiment. Reviewed targets include CEC continuous benchmarks, DTLZ/WFG, JSS/TSP/SAT, scheduling and real-world problems.
- Instance scale: NOT APPLICABLE.
- Baselines: NOT APPLICABLE.
- Baseline 数量: NOT APPLICABLE.
- Independent runs: survey states stochastic metaheuristics require multiple runs/different seeds to estimate expected performance; no paper-level experiment.
- Random seeds: conceptual discussion only; exact values NOT APPLICABLE.
- Population size: NOT APPLICABLE.
- Generations: NOT APPLICABLE.
- Evaluation budget: survey emphasizes fixed computational budget and function evaluations as reproducible budget measure when function evaluations dominate cost.
- Fitness/function evaluations: explicitly discussed as preferred reproducible time-budget proxy under appropriate cost structure.
- Real decoding count: NOT APPLICABLE.
- Solver calls: NOT APPLICABLE.
- LLM calls: NOT APPLICABLE.
- Token budget: NOT APPLICABLE.
- Runtime / wall-clock: wall-clock/CPU discussed but cautioned as hardware/language/implementation dependent.
- Hardware: NOT APPLICABLE.
- Metrics: solution quality; running time; AUC anytime performance; hypervolume of quality-time Pareto profile; multiple metrics including quality+memory, convergence+diversity, HV and Δspread.
- Statistical tests: survey reports literature use of **Friedman test** and **t-test**; Friedman nonparametric and described as potentially preferable when normality is not justified. This is survey evidence, not a corpus frequency.
- Confidence interval: NOT REPORTED as a standard recommendation in the inspected sections.
- Ablation: NOT APPLICABLE.
- Sensitivity analysis: NOT APPLICABLE.
- Generalization / OOD: explicit principle: after design on finite target instances, test generalization on unseen instances outside the design set.
- Robustness: overfitting/underfitting and generalization are explicit challenges.
- Dynamic-event design: NOT PRESENT in scheduling-event sense.
- LLM API / inference cost: NOT APPLICABLE.
- Performance-evaluation acceleration mechanisms reviewed: intensification, racing, dual population, surrogate models, capping/early stopping.

## C｜Writing Evidence Coding
### Introduction
Actual sequence: **M1 metaheuristic definition/broad applicability → M3 manual tailoring practice → M4 four concrete limitations of manual design → M6 automated design motivation → M3 detailed discrimination from algorithm selection/configuration/AOS/HH → M5 missing comprehensive taxonomy → M7 Contributions → paper organization**.
- Limitation appears paragraph 2.
- Automated-design method/domain framing appears paragraph 3.
- Contributions appear after an unusually detailed conceptual-boundary section.
- Contribution list: prose block, effectively **three major contributions**: taxonomy; technique review/usability comparison; future trends.
- Empirical diagnosis before method: NO; conceptual diagnosis and scope discrimination precede taxonomy.

### Related Work
- Related work is embedded in Introduction.
- Organization is explicitly **conceptual taxonomy/boundary based**, not chronological: algorithm selection vs algorithm configuration vs AOS/HH vs automated design.
- This is especially useful writing evidence for the current paper because neighboring methods are separated by **what decision is automated and what output is produced**.

### Gap language
- Functions: limitation of manual design; conceptual confusion; scope mismatch of prior surveys; missing taxonomy; future unresolved challenges.
- Gap is not “nobody studied automation”; it is narrower: prior surveys cover selection/configuration or only method perspective, while design space/representation/evaluation/application taxonomy is missing.

### Contributions
- Not numbered, but introduced under bold `Contributions:`.
- taxonomy contribution: four modules.
- synthesis/usability contribution: strengths, weaknesses, challenges, scenario fit.
- future-research contribution: trends.

### Experimental writing
- No original experiment.
- Methodological guidance relevant to experimental prose: stochastic algorithms require repeated evaluations; evaluation should account for target-instance heterogeneity; function evaluations can improve fairness/reproducibility; generalization requires unseen instances.
- Important caution: statements about Friedman/t-test/function-evaluation budgets are **survey-derived methodological discussion**, not evidence that a majority of the 69-paper LLM corpus uses them. They cannot be converted into corpus norms without the final coding statistics.
