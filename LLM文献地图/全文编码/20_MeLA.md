# 20｜MeLA 全文编码

- Source: `LLM/20_MeLA.md`
- Full-text status: **YES**
- Last read position: **EOF (line >560 empty); Appendix A.1–A.6 covered**
- Corpus: LLM / HH / AHD
- Tier: B（mechanistically relevant AHD）

## A｜Research Content
- Research problem: Automatic Heuristic Design 中传统 LLM+evolution 方法直接进化 heuristic code，LLM 被当作静态生成器，难以内化“什么推理产生好 heuristic”，且复杂现实问题中代码可执行性差。
- Problem setting: TSP、BPP benchmark，以及 ACS、WSN 现实复杂优化问题。
- Objectives: 将优化对象从 heuristic code 提升到生成 heuristic 的 reasoning/prompt process，提高性能、稳定性、泛化性与可执行率。
- Algorithm backbone: population-based AHD + prompt evolution + metacognitive reflection + automatic problem analysis + error diagnosis/correction。
- Proposed mechanism: Analyze problem → initialize heuristics/thoughts → evaluate fitness/errors → repair invalid code → metacognitively analyze thought/fitness/error/best heuristic → refine prompt → generate next heuristic population。
- Decision layer: **Operator/heuristic generation + optimizer/generative-process design**。不做 runtime scheduling decision 或 operator selection。
- State / Context: problem source code/analysis、population heuristic code、thought-process history、fitness history、execution errors、current best heuristic。
- Action / Decision: 生成/修改 guiding prompt；由该 prompt 生成下一代 heuristic；错误时修复代码。
- Feedback / Reward: empirical heuristic fitness、success/failure、execution error messages、best heuristic components。
- Dynamic mechanism: AHD search-process internal iterative adaptation；NOT dynamic scheduling environment。
- LLM role: problem analyst、heuristic generator、code debugger、metacognitive reflector/prompt optimizer。
- RL role: **NOT PRESENT**。
- Claimed contribution: Prompt Evolution paradigm；metacognitive search engine；automatic problem analysis + error diagnosis for real-world AHD。
- Explicit limitation: Conclusion/Future Work 明确当前只用 DeepSeek-V3-0324，未来需测试不同 underlying LLM 以验证 model-agnostic generalizability。正文还承认 prior methods 在 complex real-world code generation 中的 executable-code problem。
- 与当前 FJSP-AGV 研究关系: 进一步证明“根据历史 performance feedback 反思并改进生成策略/算子设计”已有工作，因此 predicted-vs-realized feedback 若仅用于让 LLM 改 prompt/生成新 operator 并不足以形成独立创新。它没有 context-conditioned runtime operator competence map、Pareto-aware selection、dynamic FJSP-AGV event context。

## B｜Experimental Design Coding
- Dataset / Benchmark: TSP50/TSP larger-scale；BPP500/BPP larger-scale；ACS using OULAD；WSN deployment。
- Instance scale: ACS OULAD 10,000 learners source data，experiment 30 students/20 concepts/120 materials；WSN 200 SN + 50 CN；TSP/BPP detailed generation follows ReEvo, exact base dataset counts NOT REPORTED in this text。
- Baselines: GA, PSO, SCSO, SOA, WO, EoH, ReEvo = **7 named baselines**。
- Independent runs: **3** for main architecture comparison；best-heuristic TSP/BPP generalization uses 10 independent runs over 64 larger-scale instances；ACS/WSN optimal heuristic stability uses 30 executions with different random seeds。
- Random seeds: different seeds stated for ACS/WSN stability, numeric seeds **NOT REPORTED**。
- Population size: TSP/BPP initial 30, subsequent 10；ACS/WSN initial 20, subsequent 10。
- Generations: explicit generation count NOT REPORTED; total generated solutions TSP 100, BPP/ACS/WSN 50。
- Evaluation budget: solutions generated above; ACS heuristic evaluation uses 20 search agents × 50 iterations；WSN 50 agents ×100 iterations。
- Fitness / function evaluations: exact aggregate function-evaluation count NOT REPORTED。
- Real decoding count: NOT REPORTED。
- Solver calls: NOT REPORTED。
- LLM calls: NOT REPORTED。
- Token budget: NOT REPORTED。
- Runtime / wall-clock: NOT REPORTED。
- Hardware: 48-core Intel Xeon Gold 6248R 3.00GHz, Windows 10 Pro, 255GB RAM。
- LLM: DeepSeek-V3-0324, temperature 1。
- Metrics: heuristic Success Rate (SR), objective/fitness mean±dispersion reported in tables/figures, convergence behavior, best-heuristic stability/generalization。
- Statistical tests: **NOT REPORTED**。
- Confidence interval: **NOT REPORTED**。
- Ablation: Prompt Evolution overall comparison；Problem Analysis have/no PA；Metacognitive Search Initial/Meta-1/Meta-2/Meta-3；Error Diagnosis effect argued via success rates。并非所有四项都有严格 one-component-off factorial control。
- Sensitivity analysis: **NOT PRESENT**。
- Generalization / OOD: 64 larger-scale TSP/BPP instances；cross-domain ACS/WSN；single best heuristic repeated testing。
- Robustness: 10-run larger-scale tests + 30-seed ACS/WSN stability tests。
- Dynamic-event design: **NOT PRESENT**。
- LLM API / inference cost: **NOT REPORTED**。
- Fairness: EoH/ReEvo/MeLA same experimental parameters；traditional methods parameters reported Appendix A7。

## C｜Writing Evidence Coding
### Introduction
Actual move sequence: **M1 → M3/M4 human-designed heuristics → M3/M4 classical AHD limits → M3 LLM-AHD → M4 code-evolution/static-generator limitation → M5 leverage point = generative reasoning → M6 Prompt Evolution/MeLA → practical real-world limitations/support mechanisms → M7 contributions**。
- Limitation first appears: opening discussion of hand-designed heuristics/generalization, then sharper AHD/LLM-specific limitation in subsequent paragraphs。
- Method appears: after explicit critique of evolving heuristics, via “true point of leverage ... generative reasoning process”。
- Contributions: Introduction end, **3 numbered contributions**。
- Empirical diagnosis before method: **NO formal diagnostic experiment in Introduction**；argument is conceptual/literature-based, experiments later validate executable-code problems。

### Related Work
- Explicit `Literature Review` with three substantive families + summary gap: Heuristic Design with LLMs → Prompt Evolution → Metacognition → Summary and Identified Research Gap。
- method family: YES。
- traditional→learning→LLM: partial; main organization is three intersecting conceptual fields rather than chronological progression。
- generation vs selection: NO。
- direct solving vs solver-assisted: NO as taxonomy。
- single heuristic vs portfolio: NO。
- static vs adaptive: conceptual contrast between static generator and adaptive/metacognitive learner, but not formal taxonomy。
- offline vs online: NO。

### Gap language
- Contrast/limitation: `However, this paper argues...`; `While powerful... share a common paradigm...`; `However, the application ... remains a critical and unexplored research gap`。
- Challenge: `unguided search, lacking a higher-level intelligence`。
- Unresolved question: explicit question “how can a system learn to evolve its prompts in a principled manner?”
- Motivation/transition: `Given the limitations... logical next step...`; `To this end, we introduce...`; summary uses three-field intersection to bridge to MeLA。
- Novelty strength: strong wording `new paradigm`, `critical and unexplored research gap`, and contribution claim `first LLM-based AHD framework demonstrated ... complex, ill-defined real-world problems`。

### Contributions
- Count: **3**；numbered: YES。
- Verbs/functions: propose/validate Prompt Evolution；introduce metacognitive search mechanism；equip architecture with problem analysis/error diagnosis and real-world demonstration。
- Method contribution: YES。
- Formulation contribution: NO。
- Experimental contribution: YES。
- Benchmark contribution: NO。
- Empirical finding contribution: embedded in validation, not separate bullet。

### Experimental writing
- Setup organization: task categories → per-task settings → fairness → LLM choice → baseline families → Results and Analysis → best-heuristic generality/stability → Ablation。
- Baseline selection: 5 traditional metaheuristics + 2 LLM-AHD methods，explicitly explains what is optimized on benchmark vs real-world tasks。
- Fairness: same parameters for EoH/ReEvo/MeLA；traditional method parameters in appendix。
- Comparative results: table + convergence plot, then three-run quantitative comparison and domain-specific percentage improvements。
- Ablation writing: component-by-component prose, but evidence strength differs by component; PA/Meta have direct tables while Error Diagnosis partly inferred from success-rate comparison。
- Robustness/generalization: separates larger-scale TSP/BPP generalization from ACS/WSN repeated-seed stability。
- Statistical significance: NOT PRESENT。
- Computational cost: hardware reported; wall-clock/token/API cost absent。
