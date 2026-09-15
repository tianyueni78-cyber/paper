# 21｜MPaGE / Pareto-Grid-MOCO 全文编码

- Source: `LLM/21_Pareto-Grid-MOCO.md`
- Full-text status: **YES**
- Last read position: **EOF (line >1120 empty); Appendices A–H covered**
- Corpus: LLM / HH / AHD / Multi-objective
- Tier: **A（Mechanistically Close）**

## A｜Research Content
- Research problem: Multi-objective combinatorial optimization 中自动设计 LLM heuristics，同时处理 solution quality、runtime efficiency 与 heuristic semantic diversity。
- Problem setting: Bi-TSP, Tri-TSP, Bi-CVRP, Bi-KP；SEMO 作为底层 multiobjective search paradigm。
- Objectives: heuristic-design level 两目标主要为 negative HV + running time；最终评估同时关注 HV/IGD 与 semantic/population diversity。
- Algorithm backbone: SEMO + Language Multi-Criteria Heuristic Design + Pareto Front Grid (PFG) + LLM semantic clustering + reflective crossover/mutation。
- Proposed mechanism: objective-space PFG 将 heuristics 按 quality/runtime 分区并保留 elite；LLM 按代码语义聚类；cluster 内 mutation、跨 cluster crossover；reflection总结 parents strengths/weaknesses 后生成 offspring；non-dominated heuristic population 迭代更新。
- Decision layer: **Operator/heuristic generation + heuristic population management**。生成的 heuristic 本身同时实现 SEMO archive solution selection + neighborhood exploration；不是运行时在预定义 operator library 中选择一个 operator。
- State / Context: heuristic code+NL description、quality/runtime objective vector、PFG cell/neighborhood、semantic cluster、parent heuristics、reflection feedback。
- Action / Decision: 选择 parent region/cluster；mutation/crossover；LLM生成新的 selection+neighborhood heuristic。
- Feedback / Reward: negative HV、runtime；LLM textual reflection；population non-dominance；semantic-diversity measures用于分析。
- Dynamic mechanism: heuristic-design evolutionary dynamics；NOT dynamic scheduling events。
- LLM role: heuristic generator、semantic reviewer/clusterer、reflection/synthesis module。
- RL role: **NOT PRESENT**。
- Claimed contribution: MPaGE + SEMO/PFG；LLM semantic-logic clustering/cross-cluster recombination；multiobjective benchmark evidence on quality/runtime/diversity。
- Explicit limitation: 独立 Limitations section **NOT PRESENT**。正文指出 prior/NCO retraining、AST semantic mismatch 等边界；自身 Conclusion 未明确列 limitations/future work。
- 与当前 FJSP-AGV 研究关系: 对创新边界冲击很大。它已经覆盖 **multiobjective heuristic design + Pareto-front management + heuristic diversity + runtime cost + LLM reflection + selection/neighborhood operator generation**。因此“Pareto-aware LLM operator design”“质量+成本双目标 operator design”“semantic diversity operator portfolio”均不能单独作为创新。它仍不是 dynamic FJSP-AGV runtime operator selector，也没有 context-conditioned competence model 或 predicted-vs-realized per-context operator effect learning。

## B｜Experimental Design Coding
- Dataset / Benchmark: Bi-TSP, Tri-TSP, Bi-CVRP, Bi-KP synthetic standard MOCOP；additional NCO comparisons。
- Instance scale: design evaluation 10 instances/problem at sizes 20/20/50/50；generalization Bi-TSP 20/50/100/150/200, Tri-TSP 20/50/100, Bi-KP 50/100/200, each stated 10 instances；Table 3 reports averages over 50 instances for benchmark comparison。
- Baselines: LLM-AHD = EoH, ReEvo, HSEvo, MEoH (**4**); conventional = NSGA-II, MOEA/D, SEMO, PFG-MOEA (**4**); NCO = PMOCO, NHDE-P, NHDE-M (**3**); clustering controls = SWDI cluster, K-Means, AST similarity (**3**).
- Independent runs: **NOT REPORTED** for main MPaGE AHD experiments in the text read。
- Random seeds: **NOT REPORTED**。
- Population size: LLM-AHD population **10**；conventional MOEA comparison population **300**。
- Generations: LLM-AHD **20**；conventional MOEA **300**。
- Evaluation budget: SEMO design/evaluation runtime constraint 2000 iterations + 60s stated in main setup；Appendix conventional evaluation uses 20,000 iterations for Bi-/Tri-TSP and 10,000 for Bi-KP/Bi-CVRP。
- Fitness / function evaluations: exact total AHD function-evaluation count **NOT REPORTED**。
- Real decoding count: NOT REPORTED。
- Solver calls: NOT REPORTED。
- LLM calls: NOT REPORTED。
- Token budget: NOT REPORTED。
- Runtime / wall-clock: heuristic runtime explicitly optimized/reported; total AHD design wall-clock **NOT REPORTED**。
- Hardware: Apple M1 Mac, 8 GB RAM。
- LLM: GPT-4o-mini temp=0.7 generation；GPT-4o assessing/clustering。
- Metrics: heuristic-design objectives NHV + running time；evaluation HV, IGD, SWDI, CDI, speedup, Gap in NCO table。
- Statistical tests: **NOT REPORTED**。
- Confidence interval: **NOT REPORTED**。
- Ablation: MPaGE w/o Feedback; PFG comparison against NSGA-II/MOEA-D; clustering alternatives SWDI/K-Means/AST; these are mechanism/component comparisons rather than full factorial ablation。
- Sensitivity analysis: **NOT PRESENT** for epsilon/gamma/grid segment values。
- Generalization / OOD: explicit in-/out-of-distribution size generalization, no retraining; multiple MOCOP types。
- Robustness: cross-size/cross-problem evidence；stochastic repeated-run robustness **NOT REPORTED**。
- Dynamic-event design: **NOT PRESENT**。
- LLM API / inference cost: **NOT REPORTED**。
- Fairness: EoH/ReEvo/HSEvo/MEoH use 20 generations, population 10; conventional MOEAs population 300/generations 300; SEMO iteration budgets specified；HV normalization/reference procedure shared across methods。

## C｜Writing Evidence Coding
### Introduction
Actual sequence: **M1 MOCOP importance/problem → M3 traditional MOEAs/neural → M4 retraining/cost/generalization limits → M3 LLM-AHD → M4 single-objective focus → M3 closest multiobjective LLM works → M4 runtime/diversity limitations → M6 MPaGE → strong novelty positioning → M7 3 bullets**。
- Limitation first appears: paragraph 2 for neural/traditional methods; direct LLM-AHD gap in paragraph 3。
- Method appears: after closest-work paragraph, “To address the aforementioned issues, we propose MPaGE”。
- Contributions: Intro end, **3 bullet contributions**。
- Empirical diagnosis before method: NO。

### Related Work
- 3 explicit method-family sections: Multi-objective Optimization Algorithms → LLMs for Heuristic Design → Multi-Objective Optimization with LLMs。
- traditional→learning→LLM: YES at macro level。
- generation vs selection: NO as taxonomy。
- direct solving vs solver-assisted: NO。
- single heuristic vs portfolio: implicit via populations/non-dominated heuristic set, not primary organization axis。
- static vs adaptive: NO。
- offline vs online: NO。

### Gap language
- Contrast: `Although...`; `Nevertheless`; `However`。
- Limitation: `primarily target single-objective`; `limited exploration`; `runtime efficiency ... remains underexplored`; `tend to produce populations ... similar operational logic`; `overlook computational cost`。
- Motivation transition: `To address this...`; `To address the aforementioned issues...`。
- Strong novelty: `To the best of our knowledge, this is the first comprehensive evaluation...`; contribution uses `first framework to systematically combine...`。
- Gap style: progressively narrows from general MOCOP limitations → LLM single-objective gap → acknowledges direct multiobjective competitors → identifies **runtime + semantic diversity** residual limitations before proposing method。

### Contributions
- Count: **3**；bulleted: YES。
- Method contribution: MPaGE/SEMO/PFG。
- Mechanism contribution: semantic clustering + cross-cluster recombination。
- Experimental contribution: standard MOCOP benchmarks, LLM baselines + MOEAs + NCO。
- Formulation contribution: LMHD formulation exists in Method but not separately emphasized as contribution bullet。
- Benchmark contribution: NO new benchmark。
- Empirical finding: embedded in third bullet。

### Experimental writing
- Setup sequence: Benchmarks → Experiment settings → Performance Metric (Objectives/Metrics) → Baseline Methods。
- Baseline selection: explicitly separates LLM-based AHD from conventional MOEAs; Appendix adds NCO and explains SEMO backbone motivation。
- Fairness: separate Appendix B details equal settings for LLM methods and uniform conventional budgets; normalization/reference points specified for HV。
- Comparative results: Pareto fronts/convergence → best/fast heuristics → OOD size generalization → reflection/diversity analysis → conventional MOEA → full benchmark speed/quality → NCO appendix。
- Ablation writing: names a specific mechanism question before each controlled comparison, e.g. Reflection, PFG, semantic clustering。
- Robustness/generalization: explicit ID/OOD size section。
- Statistical significance: NOT PRESENT。
- Computational cost: unusually central，runtime is itself a design objective and speedup is reported extensively；但 total LLM token/API/design cost未报。
