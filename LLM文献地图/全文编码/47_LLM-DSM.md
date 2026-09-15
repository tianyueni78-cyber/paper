# 47｜LLM-DSM 全文编码

- Source: `LLM/47_LLM-DSM.md`
- Full-text status: **YES**
- Last read position: **EOF (line >500 empty); Appendices 1–2 covered**
- Corpus: LLM / direct combinatorial optimization
- Tier: B（Contextual-selection/direct-solving support）

## A｜Research Content
- Research problem: pure mathematical CO approaches separate optimization from engineering interpretation and may fail to exploit contextual domain semantics in empirical engineering problems.
- Problem setting: sequence Design Structure Matrix nodes to minimize backward dependencies/feedback loops.
- Objectives: test whether LLMs can solve engineering CO directly and whether adding contextual domain knowledge improves solution quality/convergence.
- Algorithm backbone: iterative LLM direct-solution generation + Solution Base memory + mixed elite/random historical sampling + deterministic objective evaluator/checker.
- Proposed mechanism: randomly initialize one sequence; store all valid solutions and scores; each iteration select Kp top-performing + Kq random non-top historical solutions; prompt LLM with topology, optional semantic domain knowledge, meta-instructions, and sampled histories; validate permutation; evaluate; append; return best.
- Decision layer: **direct optimization/scheduling-like sequence decision**, not heuristic/operator generation or selection.
- State / Context: network edge list, node names/domain description, sampled historical sequences and objective scores, solution-base history.
- Action / Decision: generate a complete node ordering/permutation.
- Feedback / Reward: number of backward dependencies; lower is better. Historical solution-score pairs feed subsequent in-context learning.
- Dynamic mechanism: iterative solution-base growth and resampling; no external dynamic event or explicit search-state controller.
- LLM role: direct candidate-solution generator using semantic + mathematical context and in-context historical performance.
- RL role: NOT PRESENT.
- Claimed contribution: LLM framework integrating topology and domain context; empirical evidence of faster convergence/higher quality; domain knowledge improves multiple backbones.
- Explicit limitation: only four small DSM cases (12–17 nodes); needs larger/more diverse networks; generalization to other real CO untested; intermediate LLM reasoning changes not interpreted.
- 与当前 FJSP-AGV 研究关系: contextual evidence rather than direct competitor. It already demonstrates `problem/environment semantic context + historical candidate scores → next decision` and elite+random historical sampling. Thus generic contextual prompting and performance-memory selection are occupied. It does not model search-process/Pareto/operator competence and directly emits full solutions, so the current work's decision layer remains materially different.

## B｜Experimental Design Coding
- Dataset / Benchmark: four real/reference DSMs: UCAV, Microfilm Cartridge, Heat Exchanger, Automobile Brake System.
- Instance scale: N=12–17 nodes, E=32–47.
- Baselines: GA in 3 parameter regimes; 5 deterministic ranking methods; no-knowledge LLM variant; 4 backbone LLMs in ablation.
- Baseline 数量: **8 algorithmic benchmark settings** (3 GA +5 deterministic) plus internal no-knowledge variant.
- Independent runs: **10 runs with different random seeds** for every method where stochastic/tie behavior applies.
- Random seeds: different seeds stated; numeric seed values NOT REPORTED.
- Population size: GA exploration 50, exploitation 10, balanced 20.
- Generations: GA 2,000 generations; LLM maximum 20 iterations.
- Evaluation budget: LLM 1/5/20-trial checkpoints; GA convergence normalized by unique sequences and visualized to first 10,000 explored unique solutions.
- Fitness / function evaluations: LLM one unique candidate per iteration; GA explores multiple per generation; exact aggregate GA unique-evaluation total varies and is normalized for convergence comparison.
- Real decoding count: one candidate sequence per LLM iteration; up to 20 per run.
- Solver calls: NOT APPLICABLE; evaluator directly counts backward dependencies.
- LLM calls: one generation call per iteration; up to 20/run, aggregate across all experiments NOT REPORTED.
- Token budget: NOT REPORTED.
- Runtime / wall-clock: NOT REPORTED.
- Hardware: NOT REPORTED.
- Metrics: backward-dependency objective, convergence by number of unique solutions explored, mean±std solution quality.
- Statistical tests: NOT REPORTED.
- Confidence interval: NOT REPORTED.
- Ablation: contextual domain knowledge removed; backbone Claude-3.5-Sonnet vs Mixtral-7x8B/Llama3-70B/GPT-4-Turbo.
- Sensitivity analysis: LLM trial count 1/5/20; GA exploration/exploitation/balanced settings. Kp=5,Kq=5 fixed, no sensitivity.
- Generalization / OOD: four DSM cases across activity/parameter types and four LLM backbones; no larger-scale or unseen-domain protocol.
- Robustness: 10 seeds and mean±std; domain-knowledge effect across backbones.
- Dynamic-event design: NOT PRESENT.
- LLM API / inference cost: models identified; API/cost/token totals NOT REPORTED.

## C｜Writing Evidence Coding
### Introduction
Actual sequence: **M1 CO importance/examples → M2 traditional engineering CO pipeline → M4 separation of solving/interpretation misses contextual nuance → M3 LLM capabilities/optimization/domain knowledge → M5 two explicit hypotheses → M6 topology+domain-context framework → M2 DSM case/formulation motivation → M7 experiment/result contribution statements**.
- Limitation appears in first paragraph immediately after traditional workflow.
- Method follows explicit hypotheses rather than a conventional numbered gap paragraph.
- Contributions are prose claims, **not numbered**.
- Empirical diagnosis before method: NO new diagnosis; hypotheses motivate method.

### Related Work
- No standalone Related Work section.
- Prior work is embedded in Introduction: traditional engineering CO → LLM optimization → engineering domain knowledge → DSM sequencing.
- Organization is problem/method-family progression, not a detailed taxonomy.

### Gap language
- `This separation ... is limited and incapable to capture contextual nuances` provides direct mechanism limitation.
- `motivated us to explore` transitions capability evidence to research question.
- Two explicit hypotheses make the remaining question unusually testable.
- Conclusion uses `Despite the promising results, there are some limitations` followed by three concrete scope/generalization/interpretability limits.

### Contributions
- No formal contribution list/count.
- Method contribution: topology + domain context + iterative historical solution base.
- Experimental contribution: convergence/quality against GA and deterministic baselines.
- Empirical finding: contextual domain knowledge consistently improves performance across tested backbones.
- Benchmark contribution: NOT PRESENT; uses collected/reference DSM cases.

### Experimental writing
- Setup explicitly states **10 runs with different random seeds**, Kp/Kq, 20 iterations and exact LLM version.
- Baselines are deliberately split into stochastic and deterministic families, with rationale for each family.
- Convergence fairness issue is explicitly recognized: GA explores many candidates/generation while LLM emits one/iteration, so comparison is normalized by **number of unique solutions explored**.
- Deterministic methods with tie randomness are still evaluated over 10 runs, a useful reporting detail.
- Main results report mean±std and 1/5/20-trial LLM checkpoints.
- Domain-knowledge ablation is repeated across four backbone LLMs rather than only the chosen model.
- No formal significance test, CI, hardware/runtime/token/API-cost report.

## Asset Metadata

- FULL TEXT READ: YES
- Source: `LLM/47_LLM-DSM.md`
- Decision Layer: Contextual iterative optimization
- Current-study Relation: 近邻机制参考
- Innovation Boundary: 当前不构成候选 selector 机制的直接新颖性反证；已实现范围为 Contextual iterative optimization，主要用于近邻机制参考。
- Best Writing Claim: 用 topology、domain context 与 historical solutions 驱动迭代优化，是结构+历史共同入模的案例。
