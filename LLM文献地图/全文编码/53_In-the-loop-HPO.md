# 53｜In-the-loop Hyper-Parameter Optimization for LLM-Based Automated Design of Heuristics 全文编码

- Source: `LLM/53_In-the-loop-HPO.md`
- Full-text status: **YES**
- Last read position: **EOF (line >700 empty); Appendices A–B and generated-code listings covered**
- Corpus: LLM / AHD / LLaMEA / HPO
- Tier: A（direct mechanism/efficiency evidence）

## A｜Research Content
- Research problem: LLM-driven AHD spends costly LLM calls on numerical hyperparameter tuning instead of structural algorithm innovation.
- Problem setting: automatic heuristic/metaheuristic design for Online Bin Packing, BBOB continuous optimization and TSP+GLS.
- Objectives: separate structural code/algorithm search from numerical hyperparameter optimization to reduce LLM cost while retaining/improving solution quality.
- Algorithm backbone: LLaMEA (1+1 evolutionary code search) + SMAC3 in-the-loop HPO.
- Proposed mechanism: LLM generates algorithm plus ConfigSpace; SMAC tunes parameters on a subset/instance budget; tuned algorithm evaluated consistently on full training benchmark; fitness/std/errors/best code/optimized parameters/history names+scores feed next LLM mutation; repeat under LLM-query budget.
- Decision layer: **optimizer/heuristic structure generation + parameter configuration delegated to HPO**.
- State / Context: task prompt; list of previously generated algorithm names/scores; best-so-far full code; optimized hyperparameters; mean fitness; std; runtime/compile errors.
- Action / Decision: LLM refine/redesign control flow/algorithmic structure and configuration space; SMAC chooses numerical parameter settings; best-so-far replacement.
- Feedback / Reward: benchmark fitness, std-dev, error trace; optimized hyperparameters; historical candidate scores.
- Dynamic mechanism: iterative feedback loop; per-generated algorithm HPO; no external scheduling dynamic event. Authors explicitly propose future dynamic adjustment of HPO budget.
- LLM role: structural algorithm/code generation and mutation, configuration-space generation, self-debugging.
- RL role: NOT PRESENT.
- Claimed contribution: LLaMEA-HPO hybrid; reduced LLM-query/cost through division of labor; empirical evidence on three benchmarks; insight that LLM should focus on structural creativity while HPO handles numerical tuning.
- Explicit limitation: HPO adds benchmark-evaluation cost; BP example can require more evaluations despite fewer prompts; TSP training/test instances may be insufficiently representative and induce overfitting; future work suggests more advanced HPO and dynamically adjusted HPO budgets.
- 与当前 FJSP-AGV 研究关系: strong architecture lesson. It demonstrates that **different decision types should be assigned to different mechanisms based on competence/cost**, rather than asking LLM to control everything. For current work this supports preserving deterministic/EA execution and restricting LLM to a high-level decision layer. However, LLaMEA-HPO does not learn operator-by-context competence or dynamically choose operators from environment/search/Pareto context.

## B｜Experimental Design Coding
- Dataset / Benchmark: Online Bin Packing; BBOB 24 noiseless functions (d=5); TSP+GLS training/test plus Euclidean TSPLib.
- Instance scale: BP training 5 Weibull instances size 5000, capacity100. BBOB loop 24 functions ×3 instances ×3 random seeds =216 instance runs per full benchmark. TSP training 64 TSP100; final synthetic test 3000 instances (1000 each TSP20/50/100); additional all Euclidean TSPLib instances, sizes up to ~6000.
- Baselines: EoH, vanilla LLaMEA; BBOB additionally original best LLaMEA algorithm; TSP additionally Concorde, AM, GCN, LS, GLS, EBGLS, KGLS, GNNGLS, NeuralGLS and EoH variants.
- Baseline 数量: varies by benchmark. Core AHD baselines = **2 frameworks (EoH, LLaMEA)**; TSP table includes 9 non-EoH classical/neural/exact baselines plus EoH variants.
- Independent runs: BBOB convergence figure **5 individual runs**; final generated BBOB algorithms discussed from **3 independent LLaMEA-HPO runs**; TSP/EoH generated variants show 3 independent runs. Exact BP run count from text/figure not unambiguously stated in retrieved prose, so NOT REPORTED here rather than inferred.
- Random seeds: BBOB full benchmark explicitly uses **3 random seeds**, numeric seed values NOT REPORTED.
- Population size: LLaMEA uses **(1+1)** search.
- Generations: governed by LLM prompt budget, not conventional fixed generations.
- Evaluation budget: BP LLaMEA-HPO total 100 LLM queries, 10 full benchmark evals/iteration; HPO 40 instance evaluations. BBOB HPO budget 2000 instance evals ≈9.25 full benchmark evals/LLM query; objective-function budget B=10,000 per run. TSP HPO max 256 instance evals =5 full benchmark evals/LLM iteration; table reports LLaMEA-HPO 100 prompts/500 evals, while final best training convergence discussed at 20 prompts; EoH 100 and 2000 prompt checkpoints.
- Fitness / function evaluations: explicit and benchmark-dependent; BBOB each optimization run max 10,000 function evaluations.
- Real decoding count: one main LLM generation/mutation per LLaMEA iteration plus self-debugging on errors; aggregate debugging calls NOT REPORTED.
- Solver calls: Concorde used to obtain TSP optimal solutions; aggregate calls NOT REPORTED.
- LLM calls: explicitly central budget; EoH uses two prompts per solution, LLaMEA one; benchmark-specific counts reported above.
- Token budget: NOT REPORTED.
- Runtime / wall-clock: evaluation-time tradeoff reported conceptually/through benchmark evaluations and TSP time; total wall-clock NOT REPORTED.
- Hardware: NOT REPORTED.
- Metrics: BP lower-bound/bin ratio fitness; BBOB normalized AOCC/ECDF-style anytime performance, Glicko-2; TSP optimality Gap %, runtime; convergence vs LLM prompts and benchmark evaluations; mean/std.
- Statistical tests: **Wilcoxon-Holm** critical-difference comparison on Euclidean TSPLib, alpha **0.05**.
- Confidence interval: NOT REPORTED.
- Ablation: generated algorithms before vs after HPO; comparison of HPO vs vanilla LLaMEA/EoH; not a broad component ablation suite.
- Sensitivity analysis: HPO budgets differ by benchmark; no systematic sensitivity sweep of HPO budget reported.
- Generalization / OOD: TSP synthetic training → TSP20/50/100 test → diverse TSPLib up to ~6000; authors explicitly diagnose overfitting/representativeness issue.
- Robustness: multiple independent runs, mean/std curves, TSPLib statistical comparison.
- Dynamic-event design: NOT PRESENT.
- LLM API / inference cost: GPT-4o used for proposed approach; GPT-4-Turbo noted ~5× GPT-4o cost at time of writing; actual monetary totals NOT REPORTED.

## C｜Writing Evidence Coding
### Introduction
Actual sequence: **M1 LLM AHD promise → M4 high financial/computational budget + numerical HPO misuse → M5 separation-of-concerns opportunity → M6 LLaMEA-HPO/SMAC hybrid → M7 three explicit bullet contributions → paper roadmap**.
- Limitation appears immediately in abstract and early Introduction.
- Method is presented as a direct response to an observed behavior from prior LLaMEA code diffs, not a generic novelty claim.
- Contributions: **3 bullets**.
- Empirical diagnosis before method: **YES, literature/previous-run diagnosis** that LLM search spends calls fine-tuning hyperparameters.

### Related Work
- Standalone Section 2.
- Organized as **method-family/evolution**: FunSearch/AEL/EoH → benchmark evidence on evolutionary search → LLaMEA → limitations/cost/hyperparameter behavior.
- Closest baseline LLaMEA receives detailed architectural comparison rather than citation-only treatment.
- Gap narrows from general cost to a specific source of wasted budget: LLM numerical parameter tuning.

### Gap language
- `However, one significant limitation...` introduces measurable cost bottleneck.
- `parts of the evolutionary search... focuses purely on fine-tuning hyper-parameters` turns prior empirical observation into mechanism diagnosis.
- `Despite significant advancements...` acknowledges capability before cost/behavior limitations.
- `These gaps... serve as the main motivation` connects diagnosis directly to hybrid architecture.

### Contributions
- Count: **3 bullet contributions**.
- Method contribution: LLaMEA + SMAC in-loop HPO.
- Experimental contribution: lower LLM-query/computational cost with competitive/SOTA benchmark performance.
- Empirical/insight contribution: division of labor between algorithmic creativity and numerical parameter tuning.
- New benchmark contribution: NOT PRESENT.

### Experimental writing
- Section 4 explicitly defines **two resource axes** before benchmark details: LLM prompts and full benchmark evaluations. This prevents a cheap-in-tokens method from hiding extra evaluation cost.
- Fairness is unusually explicit: same BP settings as EoH; same GPT-4o for proposed/EoH where possible; BBOB acknowledges LLaMEA GPT-4-Turbo is more expensive; HPO instance evaluations are converted into full-benchmark equivalents.
- Results plot convergence against both LLM prompts and benchmark evaluations, revealing tradeoffs rather than one favorable x-axis.
- Generalization failure is openly diagnosed in TSP and followed by TSPLib validation.
- Statistical comparison uses Wilcoxon-Holm α=.05 on TSPLib.
- Computational cost is operationalized through prompt/evaluation budgets, but hardware, total wall-clock, token count and actual dollars remain unreported.

## Asset Metadata

- FULL TEXT READ: YES
- Source: `LLM/53_In-the-loop-HPO.md`
- Decision Layer: HPO / cost control
- Current-study Relation: 支持因果拆解与公平预算
- Innovation Boundary: 已占据或直接限制的边界：把 HPO 从 LLM generation 中拆出，直接提醒模块解耦和计算/token 成本控制。
- Best Writing Claim: 把 HPO 从 LLM generation 中拆出，直接提醒模块解耦和计算/token 成本控制。
