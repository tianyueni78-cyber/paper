# 43｜MCTS-AHD 全文编码

- Source: `LLM/43_MCTS-AHD.md`
- Full-text status: **YES**
- Last read position: **EOF (line >1380 empty); Appendices A–H covered**
- Corpus: LLM / AHD / MCTS
- Tier: A（Mechanistically close / direct AHD competitor）

## A｜Research Content
- Research problem: population-based LLM-AHD discards temporarily weak heuristics and can prematurely converge; search should preserve and further develop potentially useful heuristic lineages.
- Problem setting: automatically design key heuristic functions inside predefined frameworks: step-by-step construction, ACO, GLS, and cost-aware BO.
- Objectives: replace population management with MCTS tree exploration; preserve all generated heuristics/evolution relationships; balance exploration/exploitation; exploit path history.
- Algorithm backbone: LLM heuristic generation + MCTS selection/expansion/simulation/backpropagation + progressive widening + exploration decay + elite reference set + thought alignment.
- Proposed mechanism: each non-root MCTS node stores executable heuristic code + linguistic description; six LLM actions i1/e1/e2/m1/m2/s1 create new heuristics; s1 reasons over leaf-to-root evolution trajectory; actual heuristic performance on evaluation dataset is node quality; tree backs up best descendant quality.
- Decision layer: **Operator/heuristic generation and heuristic-space search control**. MCTS chooses which heuristic lineage/node to develop; LLM actions generate/refine heuristic functions. It does not select runtime scheduling operators from a fixed portfolio.
- State / Context: MCTS tree topology; node heuristic code/description/performance; path evolution history; visit counts/Q; elite top-10 heuristics; current evaluation budget; exploration factor.
- Action / Decision: i1 initialize; m1 mechanism/formula mutation; m2 parameter mutation; e1 diverse crossover; e2 parent+elite-reference crossover; s1 tree-path reasoning/refinement.
- Feedback / Reward: execute each generated heuristic on evaluation dataset D; performance g(h) becomes Q; backpropagation updates ancestors; invalid heuristics discarded at evaluation.
- Dynamic mechanism: search-stage adaptation via linearly decaying exploration factor; progressive widening revisits non-leaf nodes as visits grow; elite set updates online; trajectory/history used by s1. No external dynamic scheduling events.
- LLM role: generate code and design idea, mutation/crossover/path reasoning, second-call thought alignment descriptions.
- RL role: NOT PRESENT. MCTS/UCT supplies search control; POMO etc. are NCO baselines.
- Claimed contribution: first tree-search LLM-AHD according to authors; comprehensive exploration of underperforming lineages; tree-path prompt; progressive widening/exploration decay; thought alignment.
- Explicit limitation: MCTS-AHD convergence speed can be improved; authors propose MCTS-population hybrid future work. Black-box/no-description settings substantially weaken it.
- 与当前 FJSP-AGV 研究关系: **important boundary**. MCTS-AHD already uses `search history + actual performance + budget/search stage → adaptive search control`, maintains an evolving elite set, and has an explicit trajectory-based LLM action s1. Therefore history-aware redesign, search-stage exploration scheduling, elite-performance feedback, and trajectory reasoning cannot independently establish novelty. Distinction remains that MCTS-AHD searches/generates new heuristic functions offline/design-time, whereas current target is online **selection among executable scheduling/neighborhood operators under dynamic environment + search + Pareto + AGV context**, possibly with a competence map and slower redesign only when coverage gaps persist. This distinction remains 【待验证】 against later papers.

## B｜Experimental Design Coding
- Dataset / Benchmark: synthetic TSP/KP/CVRP/MKP/BPP/ASP; TSPLIB; synthetic BO functions; task-specific evaluation datasets D.
- Instance scale: main TSP/KP test sets 1,000 instances each; ACO table 64/test set; online BPP 5 instances/test scale; GLS TSP100/200 1,000 each and TSP500/1000 64 each; TSPLIB <500 nodes; detailed D in Table 6.
- Baselines: handcrafted Greedy/ACO/KGLS/EI/EIpu/EI-cool; traditional GP-AHD GHPP; NCO POMO/DeepACO/VRP-DACT/NeuOpt/NeuralGLS/GNNGLS; LLM-AHD Funsearch/EoH/ReEvo/HSEvo; LLM-as-optimizer LEMA/OPRO.
- Baseline 数量: varies by framework/table. Four baseline **categories** are explicitly defined in main experiment setup.
- Independent runs: principal LLM-AHD designs **3 independent runs**; main ablation variants generally five runs with original reference ten; evolution curves at least five; significance experiments 5–10 runs depending task; CAF evolution 5 trials and testing 10 trials.
- Random seeds: NOT REPORTED.
- Population size: MCTS has no population; baseline EoH population 20 online BPP and 10 other tasks; Funsearch 10 multiple populations noted.
- Generations: EoH baseline 20 generations; MCTS-AHD controlled by evaluation budget, not generations.
- Evaluation budget: T=1,000 for most tasks; **T=2,000 online BPP**; each heuristic runtime on D limited to 60 s. CAF evolution at most 12 function samples; testing budget 30.
- Fitness / function evaluations: MCTS-AHD budget is explicit **heuristic performance evaluations g(h)**, i.e. 1,000/2,000 depending task.
- Real decoding count: each heuristic generation uses **two LLM calls** (code/design + thought-alignment description); exact aggregate decoding count depends tree actions and is not separately tabulated.
- Solver calls: LKH3 reference for TSP; OR-Tools for KP; aggregate calls NOT REPORTED.
- LLM calls: two per generated heuristic; aggregate total NOT REPORTED.
- Token budget: example KP T=1000 ≈ **1M input + 0.2M output tokens** with GPT-4o-mini.
- Runtime / wall-clock: KP T=1000 ≈ **3 hours** on Intel i7-12700 CPU; per-heuristic evaluation cap 60 s.
- Hardware: **single Intel(R) i7-12700 CPU** for LLM-AHD heuristic design.
- Metrics: objective values, optimality gaps, gaps to lower bound, explored/evaluation curves, avg/std, p-values, BO gap/cost-aware performance.
- Statistical tests: **single-tailed t-tests** in Appendix F.3; p-values reported (e.g. TSP50 0.002855655; KP100 0.027524885; ACO examples ≈0.039/0.037).
- Confidence interval: no formal CI; text interprets tests as at least 96% confidence in selected scenarios.
- Ablation: remove progressive widening/thought alignment/exploration decay; remove s1/m1/m2; λ0 sensitivity; NI/α/k; black-box vs white-box; cross-LLM.
- Sensitivity analysis: λ0=0.05/0.1/0.2; NI=4/10; α=0.5/0.6; k=1/2; multiple LLM backbones.
- Generalization / OOD: in-domain vs larger/different-scale test sets; multiple CO problems/frameworks; BO; TSPLIB; multiple closed/open LLMs; black-box settings.
- Robustness: 3/5/10-run experiments, avg/std, p-values; multiple frameworks/tasks/scales.
- Dynamic-event design: NOT PRESENT.
- LLM API / inference cost: example **~$0.3** GPT-4o-mini for KP T=1000; tokens/runtime also reported.

## C｜Writing Evidence Coding
### Introduction
Actual sequence: **M1 heuristics/applications → M4 manual design burden → M3 AHD/GP → M4 handcrafted GP operators → M3 LLM-AHD/EoH/Funsearch/ReEvo/HSEvo → M4 population discards inferior heuristics/premature convergence → M5 need comprehensive heuristic-space exploration → M6 MCTS-AHD + components → M7 two numbered advantages plus thought-alignment/experimental statement**.
- Central limitation appears after detailed competitor mechanism discussion, not merely generic motivation.
- Proposed method immediately follows `To address these drawbacks`.
- Contributions are embedded as **two bold numbered advantages** plus additional component statements, rather than a separate contribution bullet block.
- Empirical diagnosis before method: conceptual population failure illustrated by Figure 1; detailed empirical verification comes later.

### Related Work
- Detailed Related Work is Appendix A and is strongly taxonomy/method-family organized: AHD → NCO → LLM for EC → LLM for AHD → LLM for CO → LLM inference with MCTS → LLM code generation.
- It explicitly separates LLM-AHD, LLM-as-optimizer and LLM-as-solver.
- It explicitly describes population-based LLM-AHD as four stages: initialization → operator selection → generation → population update.
- It notes existing population methods **randomly select an operator**, useful evidence for later selector comparisons.
- Multiobjective AHD is explicitly acknowledged but excluded as baseline because this paper optimizes only heuristic performance.

### Gap language
- `However, lower-performance heuristic functions still have the potential...` establishes mechanism failure.
- `still fail to explore the complex space` sharpens the limitation after acknowledging diversity fixes.
- `To address these drawbacks` transitions directly to MCTS-AHD.
- Claim strength is unusually strong: `first tree search method for LLM-based AHD` is an author novelty claim and must not be promoted to corpus fact without verification.
- Discussion uses explicit hypothesis→experiment structure for advantage scope.

### Contributions
- Method contribution: MCTS tree replacing population EC; progressive widening; exploration decay.
- Search-history contribution: tree-path reasoning action s1.
- Representation/reliability contribution: thought alignment after code generation.
- Experimental contribution: multi-task/framework/LLM/OOD, significance, ablation, cost.
- Benchmark contribution: NO new benchmark.

### Experimental writing
- Experimental setup explicitly groups baselines into **four methodological categories**, then explains fairness and why some methods require seed functions.
- Computational fairness is unusually concrete: shared evaluation budget T, 60 s heuristic cap, same seed functions where required, same general frameworks, CPU environment, token/runtime/$ cost.
- Main tables state number of instances and repeated runs directly in captions.
- Significance is not left at decorative `significantly`: Appendix F.3 increases runs and uses **single-tailed t-tests**, reporting raw runs, avg, std, p-value.
- Ablation separates components/actions/parameters and later adds parameter flexibility, black-box scope, cross-LLM and evolution-trajectory evidence.
- Discussion does not claim universal superiority: it identifies weaker black-box settings and hypothesizes why limited MCTS expansion needs higher generation quality.
- Limitation is concise and placed with Conclusion: convergence speed and MCTS-population hybrid future direction.

## Asset Metadata

- FULL TEXT READ: YES
- Source: `LLM/43_MCTS-AHD.md`
- Decision Layer: Search-control
- Current-study Relation: 支撑 search-process-aware 路线
- Innovation Boundary: 已占据或直接限制的边界：用 tree search 管理 heuristic design，保留暂时低性能但有潜力的路径，证明 search topology 本身可被设计。
- Best Writing Claim: 用 tree search 管理 heuristic design，保留暂时低性能但有潜力的路径，证明 search topology 本身可被设计。
