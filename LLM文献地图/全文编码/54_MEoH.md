# 54｜MEoH 全文编码

- Source: `LLM/54_MEoH.md`
- Full-text status: **YES**
- Last read position: **EOF (line >820 empty); Appendices A–I covered**
- Corpus: LLM / AHD / multi-objective heuristic design
- Tier: A（direct multi-objective boundary evidence）

## A｜Research Content
- Research problem: single-objective LLM-AHD optimizes target performance while neglecting practical criteria such as efficiency/complexity/readability.
- Problem setting: automatic heuristic design for online BPP and TSP+GLS under multiple heuristic-level objectives.
- Objectives: generate a nondominated set of heuristics in one run, initially balancing optimal gap and runtime, with 3-objective readability extension.
- Algorithm backbone: MOEA-style population search + LLM offspring generation.
- Proposed mechanism: dominance-dissimilarity mechanism combines Pareto dominance in objective space with AST code dissimilarity in search space; used in parent selection and population management; five LLM search operators inherited/adapted from EoH.
- Decision layer: **Operator/heuristic generation + multi-objective population management**, not online scheduling selection.
- State / Context: heuristic description, code, multiobjective fitness, pairwise Pareto dominance, AST structural similarity/dissimilarity, current population.
- Action / Decision: probabilistic parent selection; LLM generates offspring heuristic; remove worst individuals by dominance-dissimilarity score.
- Feedback / Reward: optimal gap, runtime, dominance relations, code dissimilarity; 3-objective appendix adds Halstead difficulty/readability.
- Dynamic mechanism: iterative evolutionary population update; no external dynamic event or runtime context-conditioned operator switching.
- LLM role: zero-shot generation/refinement of heuristic descriptions and Python implementations through five prompt operators.
- RL role: NOT PRESENT.
- Claimed contribution: multiobjective LLM-based heuristic design; dominance-dissimilarity selection/management; BPP/TSP empirical evidence producing trade-off heuristic sets.
- Explicit limitation: main study primarily two objectives; three-objective appendix preliminary; many-objective and broader heuristic-design tasks remain future work.
- 与当前 FJSP-AGV 研究关系: direct novelty boundary. Multiobjective LLM heuristic design, Pareto-aware population control, heuristic-set generation, quality/runtime trade-offs and even 3-objective heuristic design already exist. Current paper cannot claim Pareto-aware LLM operator design or multidimensional operator quality as novelty by itself. MEoH does **not** model context-specific operator competence, predicted-vs-realized effects, dynamic FJSP-AGV environment/search state, or coverage-gap-triggered targeted redesign.

## B｜Experimental Design Coding
- Dataset / Benchmark: online BPP; TSP random instances + TSPLIB.
- Instance scale: BPP evolution 5 Weibull 5k C100; generalization 5 instances each for sizes 5k/10k/100k and capacities 100/500. TSP evolution 64 random TSP100; tests TSP100/500/1000 plus TSPLIB up to 1002 nodes.
- Baselines: closest LLM-AHD baselines FunSearch and EoH; conventional MOEA comparison NSGA-II and MOEA/D; task-level TSP exact best-known via Concorde.
- Baseline 数量: core LLM-AHD = 2; conventional MOEA mechanism comparison = 2.
- Independent runs: **3 repetitions** for experiments.
- Random seeds: NOT REPORTED.
- Population size: BPP **20**; TSP **10**.
- Generations: **20**.
- Evaluation budget: EoH/MEoH settings imply 2000 generated heuristics BPP and 1000 TSP; FunSearch 10000 heuristics.
- Fitness / function evaluations: heuristic evaluations implied by generated-heuristic counts; aggregate low-level GLS evaluations NOT REPORTED.
- Real decoding count: NOT REPORTED.
- Solver calls: Concorde used for random TSP best-known solutions; aggregate NOT REPORTED.
- LLM calls: aggregate exact count NOT REPORTED separately from generated heuristics.
- Token budget: NOT REPORTED.
- Runtime / wall-clock: heuristic runtime is an optimization objective and reported in seconds; overall design-process wall-clock NOT REPORTED.
- Hardware: Intel Core i7-11700, 32GB memory.
- Metrics: heuristic optimal Gap, runtime; HV, IGD; Pareto front; dominance-dissimilarity score; 3-objective Halstead difficulty.
- Statistical tests: NOT REPORTED.
- Confidence interval: NOT REPORTED.
- Ablation: dominance-dissimilarity mechanism vs conventional NSGA-II/MOEA-D population management; evolution visualizations; any-time EoH comparison.
- Sensitivity analysis: NOT PRESENT as conventional parameter sweep.
- Generalization / OOD: BPP size/capacity shifts including C500 OOD; random TSP size scaling and TSPLIB external instances.
- Robustness: three repetitions + cross-size/OOD tests; no formal statistical robustness test.
- Dynamic-event design: NOT PRESENT.
- LLM API / inference cost: GPT-3.5-turbo; monetary/token cost NOT REPORTED.

## C｜Writing Evidence Coding
### Introduction
Actual sequence: **M1 heuristic importance/manual burden → M3 classical AHD categories → M3 LLM+EC AHD → M4 single-objective limitation → M5 need nondominated heuristic set across conflicting criteria → M6 MEoH → M7 three bullet contributions**.
- Limitation appears after establishing existing LLM-AHD capability.
- Method follows immediately after the explicit multiobjective gap.
- Contributions: **3 bullets**, unnumbered bullets.
- Empirical diagnosis before method: NO; gap is literature/method-structure based.

### Related Work
- Standalone Section 2 with three method-family subsections: Automated Heuristic Design → LLM-based AHD → Multi-objective Heuristic Design.
- Explicitly distinguishes configuration, selection, composition.
- Existing non-LLM multiobjective design is acknowledged before positioning LLM integration, avoiding false claim that multiobjective heuristic design itself is new.

### Gap language
- `However, all existing LLM-based evolutionary heuristic search methods focus on a single objective...` states scoped limitation with citations.
- `Although some studies... combining them into a single objective` acknowledges partial capability before explaining why scalarization does not return a trade-off set.
- `remains unexplored` is attached to the narrower claim of searching a nondominated heuristic set in a single LLM-AHD run, not multiobjective optimization generally.

### Contributions
- Count: **3**.
- Method contribution: multiobjective LLM-AHD framework.
- Mechanism contribution: dominance-dissimilarity selection/management.
- Experimental contribution: BPP/TSP comparison against single-objective LLM-AHD.
- Formulation contribution: heuristic design explicitly modeled as MOP.
- Benchmark contribution: NOT PRESENT.

### Experimental writing
- Setup first fixes tasks/low-level algorithm and search budgets, then hardware/LLM/repetition count, then objectives/metrics/baselines.
- Fairness: EoH default T/N/d settings inherited by MEoH; same design tasks.
- Comparative evidence is layered: convergence (HV/IGD), final Pareto fronts, OOD/scaling tables, conventional MOEA mechanism comparison, any-time comparison, qualitative code inspection, 3-objective extension.
- Generalization claims are tied to explicit BPP capacity shift and TSP scale/TSPLIB tests.
- Computational cost is an **objective** rather than merely supplementary reporting.
- Missing: seeds, statistical significance/CI, token/API cost, total AHD wall-clock.

## Asset Metadata

- FULL TEXT READ: YES
- Source: `LLM/54_MEoH.md`
- Decision Layer: Multi-objective heuristic design
- Current-study Relation: 限制“多目标 heuristic set”创新
- Innovation Boundary: 已占据或直接限制的边界：把 heuristic search 做成多目标并输出 non-dominated heuristic set，说明多目标 heuristic portfolio 已存在。
- Best Writing Claim: 把 heuristic search 做成多目标并输出 non-dominated heuristic set，说明多目标 heuristic portfolio 已存在。
