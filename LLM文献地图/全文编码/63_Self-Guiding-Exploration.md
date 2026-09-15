# 63｜Self-Guiding Exploration (SGE) 全文编码

- Source: `LLM/63_Self-Guiding-Exploration.md`
- Full-text status: **YES**
- Last read position: **EOF (line >680 empty); Appendix A through complete CP result tables covered**
- Corpus: LLM / direct combinatorial optimization / metaheuristic-like prompting
- Tier: B/A boundary

## A｜Research Content
- Research problem: direct and existing prompting methods degrade on larger NP-hard combinatorial problems and require more sophisticated general-purpose reasoning strategies.
- Problem setting: six CP tasks: Assignment, Knapsack, Bin Packing, TSP, VRP, Job Scheduling; plus arithmetic/commonsense/symbolic reasoning benchmarks.
- Objectives: solve CPs using a task-general LLM prompting method that autonomously discovers task-specific heuristics, decomposes them, executes/refines candidate reasoning and integrates solutions.
- Algorithm backbone: **Explore multiple method trajectories → Decompose each into subtasks → recursively Resolve → obtain Feedback → Refine → Integrate trajectories**.
- Proposed mechanism: each thought trajectory corresponds to a candidate solving heuristic/algorithm; decomposition turns it into executable subtasks; recursive SGE handles difficult subtasks; feedback prompts critique/refine outputs; final LLM integrates all trajectories.
- Decision layer: **Algorithm/heuristic generation/selection inside direct solution reasoning + direct scheduling/CO solution**, not optimizer-internal operator selection.
- State / Context: original problem Q; selected trajectory/method; preceding subtask thoughts; feedback query; all final trajectory thoughts. No persistent empirical competence memory across problem instances.
- Action / Decision: propose solving methods, decompose steps, execute subtasks, refine candidate solution, integrate final answer.
- Feedback / Reward: LLM-generated feedback on candidate subtask output; Code Interpreter can execute/evaluate generated code; solution cost used for evaluation. No learned reward policy.
- Dynamic mechanism: recursive decomposition/refinement within one solve; no external dynamic event or online search-state adaptation.
- LLM role: autonomously generates, executes, critiques, refines and combines heuristic/algorithm trajectories.
- RL role: NOT PRESENT in SGE; RL discussed as prior CP approach.
- Claimed contribution: broad CP application of LLMs; general SGE prompting; improved CP optimization vs CoT/Refine/Decomp; transfer to non-CP reasoning tasks.
- Explicit limitation: performance improvement declines with problem size; strong performance depends materially on Code Interpreter; SGE requires substantially more model calls than Decomposition. No dedicated Limitations section is present.
- 与当前 FJSP-AGV 研究关系: important boundary evidence. `LLM generates multiple heuristic approaches, decomposes, executes, receives feedback, refines and integrates` is already occupied even for Job Scheduling. Thus multi-trajectory heuristic generation/refinement cannot be a standalone novelty. However, SGE has no fixed operator portfolio, no empirical operator competence learned across contexts, no Pareto/search-process state, no predicted-vs-realized effect vector and no localized portfolio coverage-gap redesign.

## B｜Experimental Design Coding
- Dataset / Benchmark: six generated CP task families; reasoning benchmarks AQUA, GSM8K, SVAMP, ASDiv, StrategyQA, CSQA, ARC, LastLetter.
- Instance scale: CP size experiments cover **n=5,8,12,15,20,25,30** in appendix; optimality-gap study uses n=5,8,12. Exact number of CP instances per size/task is NOT REPORTED in the visible text. Qualitative phase inspection uses **5 random instances per CP task**.
- Baselines: IO, zero-shot CoT, Self-Refinement, Decomposition; Google OR-Tools brute-force optimum for small cases; model comparison across GPT-4, Gemini-1.5, GPT-3.5, Llama-2-70B, Llama-2-7B.
- Baseline 数量: **4 prompting methods including IO as reference, 3 alternative prompting baselines against SGE**; exact solver used for small-case optimum.
- Independent runs: NOT REPORTED.
- Random seeds: NOT REPORTED.
- Population size: NOT APPLICABLE.
- Generations: NOT APPLICABLE.
- Evaluation budget: average function calls reported; SGE **58.32 calls/instance** in efficiency table, Decomposition 31.04, CoT/Refine controlled to 58.32 for fair cost comparison.
- Fitness / function evaluations: solution costs computed; no evolutionary fitness budget.
- Real decoding count: reflected in function-call counts; aggregate corpus calls NOT REPORTED.
- Solver calls: OR-Tools brute force for small-size global optimum; Code Interpreter for supported models; aggregate NOT REPORTED.
- LLM calls: average per-instance function calls explicitly reported in efficiency comparison.
- Token budget: NOT REPORTED.
- Runtime / wall-clock: NOT REPORTED.
- Hardware: NOT REPORTED.
- Metrics: percentage improvement vs IO; optimality gap vs OR-Tools optimum; reasoning-task accuracy; average cost; number of LLM function calls.
- Statistical tests: NOT REPORTED.
- Confidence interval: NOT REPORTED.
- Ablation: no clean component-removal ablation of Exploration/Decomposition/Feedback/Integration; qualitative phase analysis only. Baseline comparisons isolate simpler prompting strategies but are not full component ablations.
- Sensitivity analysis: problem size; LLM choice; performance-vs-call cost.
- Generalization / OOD: six heterogeneous CPs + eight non-CP reasoning datasets; task-general meta-prompts.
- Robustness: NOT REPORTED statistically.
- Dynamic-event design: NOT PRESENT.
- LLM API / inference cost: operational cost represented by model function-call count; monetary cost NOT REPORTED.

## C｜Writing Evidence Coding
### Introduction
Actual sequence: **M1 LLM reasoning success → M3 prompting families → M2 CP complexity/industrial relevance → M3 classical metaheuristics → M4 task-specific heuristic dependence → M4 limited LLM CP scalability/coverage → M6 SGE mechanism → M7 four prose contributions**.
- Limitation appears after motivating CP complexity and current methods.
- Method is described before the contribution paragraph.
- Contributions: **4 sequential contributions**, written as `Firstly/Secondly/Thirdly/Lastly`, not numbered bullets.
- Empirical diagnosis before method: NO.

### Related Work
- Standalone Section 2 organized by method family and progression: classical CP → learning/RL CP → LLM CP → prompting strategies.
- This produces a clear **traditional → learning → LLM → prompting mechanism** narrative.

### Gap language
- Uses strong scarcity language (`minimal`, `notable scarcity`, `significant research gap`) based on the paper’s 2024-era review. These cannot be reused as current 2026 gap claims.
- More transferable rhetorical pattern: identify the failure mode `as problem sizes increase, existing prompting strategies yield inadequate responses`, then introduce the mechanism designed to address it.

### Contributions
- Count: **4**.
- Investigation/application contribution; method contribution; CP experimental contribution; cross-domain generalization contribution.
- Uses quantitative improvement numbers directly in contribution statement.

### Experimental writing
- Baselines are selected to correspond to the constituent prompting ideas behind SGE: exploration/CoT, decomposition and refinement.
- Fairness is handled explicitly in cost comparison by controlling CoT and Refine function calls to equal SGE calls.
- Results are decomposed into overall CP performance, qualitative mechanism behavior, size sensitivity, optimality gap, model sensitivity, and cost-efficiency.
- Negative evidence is explicit: SGE advantage decreases with size; Code Interpreter appears crucial; extra performance costs 87.89% more calls than Decomposition.
- Exact small-case solver optimum is used as a separate validation axis rather than relying only on relative improvement against weak IO prompting.
- Missing: repeated runs/seeds, inferential statistics/CI, runtime/token/API-dollar reporting and component-removal ablation.
