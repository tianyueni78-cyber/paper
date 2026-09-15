# 44｜QUBE 全文编码

- Source: `LLM/44_QUBE.md`
- Full-text status: **YES**
- Last read position: **EOF (line >730 empty); Appendices A–F covered**
- Corpus: LLM / LLM+EA / AHD
- Tier: A（Direct AHD/search-control competitor）

## A｜Research Content
- Research problem: FunSearch-style LLM+EA heuristic evolution inadequately balances exploitation and exploration because its priority criterion uses current sample score rather than evolutionary potential and uncertainty.
- Problem setting: evolve Python heuristic functions inside predefined algorithms for online bin packing, cap set, and TSP.
- Objectives: redesign evolutionary priority so parent selection and island reset account for both expected offspring quality and uncertainty.
- Algorithm backbone: FunSearch multi-island EA + frozen LLM variation + Quality-Uncertainty Trade-off Criterion (QUTC) + Uncertainty-Inclusive Quality (UIQ).
- Proposed mechanism: cluster programs producing identical outputs; estimate each cluster's quality by mean score of offspring previously generated from that cluster; use parent-selection count as uncertainty; combine quality and uncertainty via UCB-inspired UIQ; choose top-UIQ clusters as parents and use UIQ for island reset.
- Decision layer: **heuristic-generation search control / parent selection**, not runtime scheduling operator selection.
- State / Context: cluster identity, historical offspring scores, number of times cluster used as parent, island membership/performance, current timestep/evolution history.
- Action / Decision: select two clusters/parents for LLM variation; choose underperforming islands for reset; LLM generates new heuristic code.
- Feedback / Reward: deterministic heuristic execution score; offspring performance updates cluster quality estimate; parent usage updates uncertainty.
- Dynamic mechanism: UIQ changes online as offspring outcomes and visit counts accumulate; exploration pressure naturally decays as uncertainty falls; periodic island reset.
- LLM role: frozen code-generation variation operator using selected parents as few-shot examples.
- RL role: NOT PRESENT; UCB inspiration only.
- Claimed contribution: diagnose FunSearch exploitation/exploration failure; propose QUTC/UIQ and QUBE; demonstrate gains on NP-complete tasks.
- Explicit limitation: does not beat original FunSearch cap-set result; results depend on LLM/sample count/randomness; very high compute; generated code creates security/explainability risks.
- 与当前 FJSP-AGV 研究关系: **strong boundary evidence**. QUBE already implements a primitive empirical `candidate/context → expected offspring quality + uncertainty` competence estimate and uses it for online parent selection. Therefore historical operator/candidate performance, uncertainty-aware selection, and exploration-to-exploitation adaptation are not independently novel. The remaining distinction must be stronger: operator competence conditioned on explicit dynamic FJSP-AGV environment/search/Pareto context and multi-dimensional realized effects, rather than global cluster-level offspring quality/visit uncertainty in offline heuristic evolution.

## B｜Experimental Design Coding
- Dataset / Benchmark: OR-Library OBP OR1–OR4; generated Weibull OBP; cap set n=8; TSP20/50/100.
- Instance scale: Weibull 5 test instances each with 1k/5k/10k items; TSP 1,000 test instances per size; cap set n=8.
- Baselines: original FunSearch, reproduced FunSearch*, EoH; ablations Parent Selection Only and Quality Only.
- Baseline 数量: 3 named external/baseline variants in main comparison if FunSearch and FunSearch* are distinguished; 2 internal ablation variants.
- Independent runs: **10 runs each experiment**, best reported unless specified; ablations report average/std across 10. Cap-set hyperparameter search uses 5 runs.
- Random seeds: NOT REPORTED.
- Population size: multi-island database; 10 islands for OBP/cap set, 1 for TSP. Cluster population sizes are dynamic and NOT REPORTED as fixed population size.
- Generations: NOT APPLICABLE; sample-generation budget used.
- Evaluation budget: total generated samples: OR OBP 80K, Weibull 80K, cap set 2M, TSP 2K.
- Fitness / function evaluations: generated executable samples are evaluated; aggregate equals successful/evaluated sample process but exact valid-evaluation count NOT REPORTED.
- Real decoding count: samples per prompt 4 for OBP/cap set, 1 for TSP; total prompts/decodes not explicitly summarized.
- Solver calls: Concorde used to calculate TSP optimal solutions; aggregate calls NOT REPORTED.
- LLM calls: aggregate NOT REPORTED.
- Token budget: NOT REPORTED.
- Runtime / wall-clock: cap-set complete experiment 2.5M programs reported as >3 days on their GPU server; other wall-clock NOT REPORTED.
- Hardware: one server, **8 NVIDIA A100 GPUs + 2 Intel Xeon Platinum 8358 CPUs**; SGLang inference services.
- Metrics: excess ratio, cap-set size, Recent Best Score, Recent Proportion of Change, best run, average, std.
- Statistical tests: NOT REPORTED.
- Confidence interval: NOT REPORTED.
- Ablation: parent selection only; quality only; LLM backbone OpenCoder vs DeepSeek-Coder.
- Sensitivity analysis: UIQ k search: OR3 0.01→0.0001; Weibull5k 0.001→0.00001; cap set 16/32/48/64.
- Generalization / OOD: multiple problem types, OBP distributions/scales, TSP scales, two LLM backbones.
- Robustness: 10-run averages/std in ablation and progress curves; no formal significance tests.
- Dynamic-event design: NOT PRESENT.
- LLM API / inference cost: local inference; monetary/token cost NOT REPORTED.

## C｜Writing Evidence Coding
### Introduction
Actual sequence: **M1 NP-complete/heuristics + EA/LLM opportunity → M3 LLM+EA/FunSearch → M4 exploitation/exploration open challenge + FunSearch priority diagnosis → M6 QUBE/QUTC/UIQ → M7 three numbered contributions**.
- Limitation/gap appears in paragraph 2 after concise domain/method setup.
- Method follows immediately after explicit diagnostic claim.
- Contributions: **3 numbered items**.
- Empirical diagnosis before method: YES. Intro references analysis of FunSearch priority; Section 3 then performs dedicated quantitative diagnosis before Section 4 method.

### Related Work
- Standalone Section 2 with method-family progression: heuristics for math problems → LLM+EA → FunSearch and scaling.
- Traditional heuristic/HH → learning-assisted EA → LLM+EA progression is explicit.
- EoH and ReEvo are framed as prompt/reflection improvements, then FunSearch as scale expansion.
- generation vs selection appears implicitly through LLM variation vs parent-selection priority, but is not the section taxonomy.

### Gap language
- `However, achieving this balance long remains an open challenge` states unresolved exploration/exploitation problem.
- `Through analysis, we observe...` ties gap to a specific mechanism rather than generic absence.
- `Despite these advancements... still face challenges` broadens prior-method limitations.
- `To address these issues` is the direct transition to QUBE.
- Limitations section begins `Despite making non-trivial improvements...` and openly records failure against original FunSearch cap-set result.

### Contributions
- Count: **3**, numbered.
- Empirical/diagnostic contribution: identify FunSearch priority-criterion failure.
- Method contribution: QUBE/QUTC/UIQ.
- Experimental contribution: OBP/TSP/cap-set gains.
- Benchmark/formulation contribution: NOT PRESENT.

### Experimental writing
- Before proposing the method, Section 3 defines **two diagnostic metrics** and empirically demonstrates the exact mechanism failure the method claims to repair. This is strong diagnosis→mechanism writing.
- Setup reports hardware, local LLM service, concurrency, benchmark construction, repeated-run policy and reproduction caveat.
- Main table uses best-of-10, but Section 5.5 explicitly acknowledges randomness and then reports average trajectories/ranges; ablation reports mean/std.
- Fairness caveat is unusually explicit: original FunSearch hardware/LLM differ, so authors reproduce FunSearch* locally and separately retain reported FunSearch results.
- Hyperparameter search is moved to appendix with run counts and full candidate values.
- Computational limitation is quantified for cap set (>3 days / 2.5M programs), and failure to reproduce original FunSearch SOTA is not concealed.
- No statistical significance tests or confidence intervals.

## Asset Metadata

- FULL TEXT READ: YES
- Source: `LLM/44_QUBE.md`
- Decision Layer: Search-control
- Current-study Relation: 限制“加入不确定性”创新
- Innovation Boundary: 已占据或直接限制的边界：用 quality-uncertainty trade-off 控制 LLM heuristic search，说明 uncertainty 已成为搜索状态。
- Best Writing Claim: 用 quality-uncertainty trade-off 控制 LLM heuristic search，说明 uncertainty 已成为搜索状态。
