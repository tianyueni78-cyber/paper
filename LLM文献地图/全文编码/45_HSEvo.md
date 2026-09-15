# 45｜HSEvo 全文编码

- Source: `LLM/45_HSEvo.md`
- Full-text status: **YES**
- Last read position: **EOF (line >760 empty); Appendices A–D covered**
- Corpus: LLM / LLM-EPS / AHD
- Tier: A（Direct AHD competitor）

## A｜Research Content
- Research problem: LLM-based evolutionary program search lacks explicit understanding/control of heuristic-space diversity and can suffer a diversity-versus-objective-performance trade-off.
- Problem setting: automatic heuristic design for online BPO, TSP with GLS, and OP with ACO.
- Objectives: define measurable code-population diversity; empirically diagnose prior LLM-EPS; design an adaptive framework balancing diversity and convergence while reducing reflection cost.
- Algorithm backbone: GA-style LLM-EPS + SWDI/CDI diversity diagnostics + diverse role initialization + random parent selection + flash reflection + LLM crossover + elitist mutation + Harmony Search parameter tuning.
- Proposed mechanism: encode code via AST cleanup/style standardization/CodeT5+ embeddings; measure cluster entropy SWDI and MST-distance entropy CDI; use empirical diversity diagnosis to motivate HSEvo; flash reflection aggregates/ranks parent pairs and compares current/prior effective/ineffective reflections; Harmony Search extracts/tunes numeric parameters of best individuals.
- Decision layer: **operator/heuristic generation + population/search control + parameter tuning**. It does not perform runtime scheduling operator selection.
- State / Context: current heuristic population, objective rankings, code diversity archive/metrics, current and previous reflection summaries, elite individual and extracted parameters.
- Action / Decision: random parent-pair selection; LLM reflection/crossover/mutation; Harmony Search numerical parameter updates.
- Feedback / Reward: heuristic objective scores; SWDI/CDI as search-analysis/performance descriptors; successful vs ineffective reflection history.
- Dynamic mechanism: flash reflection explicitly compares time t analysis with t−1 and retains good/bad reflection experience; Harmony Search applied to unmarked best individuals; diversity trajectories monitored over token/time progression. No external dynamic event.
- LLM role: heuristic generator, reflector, crossover/mutation operator, parameter extractor/range proposer.
- RL role: NOT PRESENT; verbal reinforcement analogy cited only.
- Claimed contribution: SWDI/CDI diversity metrics; diversity analysis of FunSearch/EoH/ReEvo; HSEvo balancing diversity/objective performance.
- Explicit limitation: no standalone Limitations section. Experimental caveat: FunSearch could not be reasonably extended to OP due implementation conflicts. General limitations NOT REPORTED.
- 与当前 FJSP-AGV 研究关系: **important boundary**. HSEvo already tracks explicit search/population diversity, objective performance, previous reflection outcomes, and uses those histories to guide later generation; it also separates discrete heuristic redesign from numerical parameter tuning. Therefore `search diversity + historical reflection + adaptive redesign` is occupied. However its selection remains random and diversity metrics are population-level, not a context-conditioned estimate of each fixed operator's multi-dimensional effect in a dynamic Pareto scheduling state.

## B｜Experimental Design Coding
- Dataset / Benchmark: BPO, TSP100, OP50.
- Instance scale: BPO five Weibull instances size 5k C=100; TSP 64 instances ×100 nodes; OP50 synthetic 50 nodes.
- Baselines: FunSearch, EoH, ReEvo; ablation ReEvo+HS and ReEvo+Flash Reflection.
- Baseline 数量: **3 principal LLM-EPS baselines**; two component variants in ablation.
- Independent runs: **3 per experiment**.
- Random seeds: NOT REPORTED.
- Population size: EoH/ReEvo/HSEvo 30 initial, 10 later; FunSearch 10 islands ×4 samples/prompt; OP ACO population 20.
- Generations: NOT REPORTED as fixed generations; token budget used as common search budget.
- Evaluation budget: maximum **425K tokens** main setting; diversity analysis appendix says 450K; flash-reflection ablation 150K; heuristic runtime cap 100s TSP-GLS, 50s others.
- Fitness / function evaluations: NOT REPORTED as total count.
- Real decoding count: NOT REPORTED.
- Solver calls: Concorde generates TSP optimal reference; GLS/ACO repeatedly evaluate heuristics; aggregate calls NOT REPORTED.
- LLM calls: NOT REPORTED.
- Token budget: 425K main; 450K diversity analysis; 150K flash-reflection short-budget ablation.
- Runtime / wall-clock: per-heuristic caps reported; aggregate wall-clock NOT REPORTED.
- Hardware: heuristic search/evaluation single core of Xeon processor; exact model NOT REPORTED.
- Metrics: objective score, SWDI, CDI, mean ± std.
- Statistical tests: NOT REPORTED.
- Confidence interval: NOT REPORTED.
- Ablation: Harmony Search via ReEvo+HS; flash reflection via ReEvo+F.R.; diversity diagnosis across prior frameworks.
- Sensitivity analysis: NOT PRESENT for core HSEvo hyperparameters.
- Generalization / OOD: three structurally different AHD tasks; no explicit unseen-distribution/OOD protocol.
- Robustness: three independent runs and mean±std; no formal significance tests.
- Dynamic-event design: NOT PRESENT.
- LLM API / inference cost: GPT-4o-mini-2024-07-18, temperature 1; token budgets reported; monetary cost NOT REPORTED.

## C｜Writing Evidence Coding
### Introduction
Actual sequence: **M1 heuristics/metaheuristics importance → M4 manual design burden → M3 AHD/HH/NCO → M4 HH/NCO limitations → M3 LLM and LLM-EPS/FunSearch/EoH/ReEvo → M4 function-space diversity underexplored → M5 need to understand heuristic search space → M6 diversity metrics + empirical analysis + HSEvo → M7 two bullet contributions**.
- Limitations are layered after each method family.
- Proposed method comes only after an explicit conceptual search-space distinction and announced empirical analysis.
- Contributions: **2 bullets** in the rendered text.
- Empirical diagnosis before method: YES. Section 3.4–3.5 analyzes ReEvo/FunSearch/EoH diversity before Section 4 HSEvo.

### Related Work
- Section 2 is short and taxonomy/method-family based: LLM-EPS; diversity in evolutionary computation.
- Intro supplies traditional→HH/NCO→LLM-EPS evolution.
- FunSearch/EoH/ReEvo are mechanism-described rather than chronologically catalogued.
- Diversity is imported from conventional EC to expose a missing analytical dimension in LLM-EPS.

### Gap language
- `However` repeatedly contrasts HH/NCO/standalone LLM limitations.
- `This aspect has been largely unconsidered` states the heuristic-search-space understanding gap.
- Related Work uses the stronger author claim `to the best of our knowledge, no existing studies...`, which is an author claim, not corpus fact.
- Abstract uses `there is still a gap in understanding... and achieving a balance...`.
- Method transition is evidence-driven: `With this finding in mind, we introduce HSEvo`.

### Contributions
- Count: **2 explicit bullets**.
- Measurement/empirical contribution: SWDI/CDI and analysis of evolutionary progress.
- Method contribution: HSEvo diversity/objective balancing.
- Experimental findings are central but not a separate numbered contribution.
- Benchmark/formulation contribution: NOT PRESENT.

### Experimental writing
- The paper devotes an entire pre-method section to **diagnostic experiments**, then uses those findings to justify Harmony Search and flash reflection. This is a strong empirical-diagnosis→design pattern.
- Fairness is expressed through identical environmental settings and shared token/runtime budgets; benchmark appendix gives solver/problem parameters.
- Results consistently report objective and diversity jointly, usually mean±std over three runs.
- Ablation is not simple component deletion: HS is transplanted into ReEvo and flash reflection replaces ReEvo reflection, allowing mechanism-specific comparison.
- A negative implementation fact is disclosed: FunSearch→OP extension failed due unresolved conflicts.
- No statistical significance tests, CI, monetary cost or full wall-clock reporting.

## Asset Metadata

- FULL TEXT READ: YES
- Source: `LLM/45_HSEvo.md`
- Decision Layer: Search-control
- Current-study Relation: 限制“多样性状态”创新
- Innovation Boundary: 已占据或直接限制的边界：显式度量 heuristic population diversity 以平衡 exploration/exploitation，说明 diversity 已是控制变量。
- Best Writing Claim: 显式度量 heuristic population diversity 以平衡 exploration/exploitation，说明 diversity 已是控制变量。
