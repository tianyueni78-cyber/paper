# 05 PathWise｜全文编码

## Audit
- Source: `LLM/05_PathWise.md`
- Full text read to EOF: YES
- Main text, references, appendices A–J: READ where present.
- Explicit limitations: Appendix I.1.

## A. Research Content
- Research problem: LLM-based automated heuristic design (AHD) for combinatorial optimization; addresses myopic/local evolutionary decisions by planning over heuristic derivation history.
- Problem setting: heuristic design across step-by-step constructive search, ACO, and GLS; evaluated on TSP, KP, CVRP, MKP, OP, offline/online BPP.
- Objectives: evolve high-performing heuristics while exploiting derivation structure, diversity, prior outcomes and state-aware planning.
- Algorithm backbone: hybrid graph-based + population-based AHD with an entailment graph; outer population management plus inner entailment graph construction.
- Proposed mechanism: policy agent selects parent subsets and directives; world-model agent generates candidate heuristics; policy/world-model critics produce reflections; graph state retains derivation history; leaf-first population update.
- State/context: current entailment-graph frontier, heuristic descriptions/code/performances, parent metadata, derivation history, critic reflections, exploration schedule/evaluation count.
- Action/decision: policy selects parent heuristic subset and derivation rationale/directive; world model generates new heuristic implementations.
- Feedback/reward: actual heuristic performance on training instances; action reward for policy critic is mean rollout performance; best/worst rollout information feeds critics.
- Dynamic mechanism: search-process adaptation through evolving graph state, reflections, exploration schedule and population; not a dynamic scheduling environment.
- Claimed contribution: formulates AHD as state-aware planning over an entailment graph with policy/world-model agents and critics, enabling multi-parent derivation and history-aware evolutionary decisions.
- Explicit limitations: stochastic LLM generation causes non-determinism and early-stage instability; performance varies with LLM backbone/reasoning level; multi-agent trajectories/outcomes vary; robustness across runs remains an open direction.

## B. Experimental Design
- Dataset / benchmark: TSP, KP, CVRP, MKP, OP, offline BPP, online BPP; TSPLIB real-world TSP also used.
- Instance scale: multiple in-domain and OOD scales; examples include TSP/CVRP 50/100 and larger scales, MKP/OP multiple N values, BPP up to large item counts; exact per-task scales are reported in tables/appendices.
- Baselines: manually designed heuristics; POMO; Best Fit/First Fit; ACO/DeepACO; KGLS; VRP-DACT, NeuOpt, NeuralGLS, GNNGLS; LLM-AHD FunSearch, EoH, ReEvo, HSEvo, MCTS-AHD.
- Number of baselines: varies by framework/task; NOT represented as one fixed count because baseline applicability differs across frameworks.
- Independent runs: LLM-based AHD methods generally reported as mean over 3 independent runs in principal comparisons; Appendix significance analysis uses 6 independent runs for selected tasks/method comparisons.
- Seeds: explicit seed identifiers NOT REPORTED in the read text.
- Evaluation budget: `ne = 500` heuristic evaluations per task for LLM-based AHD comparisons; 60-second execution time per heuristic on training dataset.
- Metrics: objective values, optimality/performance gap, MRGI/generalization improvement measures where applicable, evolution curves; runtime/token/cost analysis.
- Statistical tests: one-sided t-test in significance analysis; significance level reported in appendix analysis.
- Ablations: component/agent and mechanism analyses including policy/world-model/critic-related components and search behavior; parameter/schedule analyses appear in appendices.
- Sensitivity analysis: parameter/exploration-related analyses reported in appendices.
- Generalization: extensive in-domain/OOD scale tests, cross-scale tests and TSPLIB evaluation.
- Runtime: wall-clock training time reported and compared.
- Hardware: hardware information appears in experimental appendices/settings; retain exact hardware string as source-level detail for later extraction if required; do not infer missing values.
- LLM calls / tokens / API cost: token usage (input/output) and monetary cost explicitly analyzed in Appendix H; GPT-4o-mini and GPT-5-nano configurations compared. A single universal LLM-call count is NOT REPORTED as a headline protocol variable in the coded text.

## C. Writing Evidence
### Introduction rhetorical moves
- Domain/problem motivation → limitations of existing LLM-AHD evolutionary search → planning/world-model motivation → proposed PathWise mechanism → contributions/empirical scope.
- Gap is mechanism-level: existing AHD search decisions lack sufficiently structured reasoning over derivation history/search state rather than an application-level claim.

### Related Work organization
- Related Work is placed in Appendix A rather than as a conventional main-text section.
- Organized primarily by method family: AHD/hyper-heuristics and planning/world-model/reasoning foundations, rather than simple chronology.

### Limitation location
- Explicit dedicated `I.1 Limitations` near the end of appendices/extended discussion.

### Gap formulation
- Existing heuristic evolution is framed as insufficiently state/history-aware and prone to local/myopic decisions; motivates graph-based planning over heuristic derivations.

### Proposed-method transition
- Limitation/challenge is followed by a planning formulation and then the policy-agent/world-model/critic architecture.

### Contribution structure
- Contributions combine methodological formulation, algorithmic architecture and broad empirical evaluation/generalization evidence.

### Experimental Setup organization
- Main Experiment section begins with evaluation scope/frameworks, Benchmarks, Experimental Settings, Baselines, then Overall Results; detailed datasets/configurations/results/costs are delegated to appendices.

### Comparative-result reporting
- Reports objective/gap tables by framework and LLM backbone, followed by task/framework-specific prose interpreting where PathWise improves, matches or trails baselines.

### Ablation-result reporting
- Ablation/analysis sections state the component or design question, compare controlled variants, and interpret the effect on search/evolution behavior and performance.

### Academic hedging
- Uses calibrated language around stochasticity, backbone dependence and robustness; explicit limitations use `may`, `likely`, `suggests`, and `remains an important direction` rather than converting observations into universal claims.

### Novelty-claim strength
- Strong mechanism proposal language is used for PathWise, while limitations and generalization claims are comparatively hedged. No corpus-level novelty inference is made from this single paper.

## Asset Metadata

- FULL TEXT READ: YES
- Source: `LLM/05_PathWise.md`
- Decision Layer: Search-control
- Current-study Relation: 直接支撑 search-process-aware 机制，同时限制 novelty
- Innovation Boundary: 已占据或直接限制的边界：把 heuristic design 变成带 trajectory memory、world model 与高层 policy 的 stateful search，直接证明“搜索过程状态”已进入 AHD。
- Best Writing Claim: 把 heuristic design 变成带 trajectory memory、world model 与高层 policy 的 stateful search，直接证明“搜索过程状态”已进入 AHD。
