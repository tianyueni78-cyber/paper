# 32｜Photonic Structures with LLM-driven Algorithm Discovery 全文编码

- Source: `LLM/32_Photonic-Structures.md`
- Full-text status: **YES**
- Last read position: **EOF (line >500 empty); Appendix A covered**
- Corpus: LLM / AHD / continuous optimization
- Tier: B（Supporting）

## A｜Research Content
- Research problem: adapt LLaMEA automatic algorithm discovery to real-world multilayer photonic optimization, addressing generic prompts and limited evolutionary-strategy diversity.
- Problem setting: continuous black-box inverse design for Bragg mirror, ellipsometry and photovoltaic multilayer structures.
- Objectives: discover algorithms on small instances that achieve strong anytime/final performance and transfer to larger realistic instances; study domain prompts and ES configurations.
- Algorithm backbone: LLaMEA + structured domain prompts + dynamic mutation control + multiple (μ,λ)/(μ+λ) evolutionary strategies.
- Proposed mechanism: enrich task prompt with automatically generated problem descriptions/algorithmic insights; feedback includes AOCC + final best fitness mean/std; mutation percentage sampled from fast heavy-tailed mutation; compare seven ES configurations.
- Decision layer: **Optimizer/metaheuristic generation**. ES determines evolutionary population/selection structure; no runtime heuristic selector.
- State / Context: problem description, domain algorithmic insight, current generated optimizer code, AOCC/final-fitness feedback and std, mutation rate.
- Action / Decision: generate/mutate full optimization algorithm code.
- Feedback / Reward: AOCC convergence metric and final best fitness, both with standard deviation from repeated executions.
- Dynamic mechanism: dynamic mutation rate during algorithm evolution; no external dynamic scheduling event.
- LLM role: full optimizer generation/mutation; GPT-4o also generates domain problem descriptions and algorithmic insights used as prompts.
- RL role: NOT PRESENT.
- Claimed contribution: domain-focused structured prompting for photonic AHD; systematic ES exploration beyond (1,1)/(1+1); small-to-large transfer on realistic photonic tasks.
- Explicit limitation: no standalone Limitations section. Results explicitly show domain-specific prompts can hurt photovoltaic search by restricting exploration; ES differences are often not significant; discovered photovoltaic algorithms are less stable; conclusion/future framing does not claim universal superiority.
- 与当前 FJSP-AGV 研究关系: supports two boundary points. First, explicit domain/context knowledge in LLM prompts and feedback mean/std already guide algorithm generation. Second, optimal search-control configuration is problem dependent and more context can be harmful. This strengthens the need for an empirically learned competence boundary rather than assuming richer context or one strategy is universally beneficial.

## B｜Experimental Design Coding
- Dataset / Benchmark: PyMoosh/IOHexperimenter photonic testbeds: mini-Bragg/Bragg, ellipsometry, photovoltaic/big-photovoltaic/huge-photovoltaic.
- Instance scale: layers: Bragg 10/20; ellipsometry 1; photovoltaic 10/20/32.
- Baselines: DE, CMA-ES, BFGS, QNDE, QODE.
- Baseline 数量: **5** classical photonic optimization baselines; additionally top 3 discovered LLaMEA algorithms compared.
- Independent runs: prompt-setting and ES discovery: **5 LLaMEA runs/configuration**, each generated algorithm executed **3 times**; final benchmarking: **15 runs per algorithm/problem instance**.
- Random seeds: numeric seeds NOT REPORTED.
- Population size: defined by ES: (1,1), (1+1), (1,5), (1+5), (2,10), (2+10), (5+5).
- Generations: not reported as generations; **100 generated algorithms per LLaMEA run**.
- Evaluation budget: mini-Bragg 10,000; Bragg 20,000; ellipsometry 1,000; photovoltaic 5,000; big-photovoltaic 10,000; huge-photovoltaic 16,000 function evaluations.
- Fitness / function evaluations: same explicit per-instance budgets above.
- Real decoding count: each discovery run generates 100 algorithms; prompt comparison/ES experiments structured accordingly. Aggregate final total not stated as one global number.
- Solver calls: black-box function evaluations rather than solver calls; NOT APPLICABLE/NOT REPORTED.
- LLM calls: NOT REPORTED as aggregate.
- Token budget: NOT REPORTED.
- Runtime / wall-clock: NOT REPORTED.
- Hardware: NOT REPORTED.
- Metrics: AOCC, final best fitness y*, convergence curves, distribution of final fitness; mean/std feedback.
- Statistical tests: authors state ES differences are `not significant`, but **specific statistical test/p-value NOT REPORTED**.
- Confidence interval: NOT REPORTED.
- Ablation: prompt variants: no domain info / problem description / description+insight; same-solution rerun for photovoltaic initialization confound; ES configuration comparison.
- Sensitivity analysis: ES strategy comparison and prompt-content variation function as design sensitivity; no continuous parameter sensitivity test.
- Generalization / OOD: algorithms discovered on small mini-Bragg/photovoltaic applied to 20/32-layer larger instances.
- Robustness: each generated algorithm 3 executions; final 15-run distributions/convergence; standard deviations in feedback.
- Dynamic-event design: NOT PRESENT.
- LLM API / inference cost: GPT-4o version mentioned for meta-prompts; monetary cost NOT REPORTED.

## C｜Writing Evidence Coding
### Introduction
Actual sequence: **M1 photonic importance/complexity → M3 LLM algorithm discovery → M4 two explicit LLaMEA limitations → M6 structured domain prompt + ES expansion → paper roadmap**.
- Limitation appears paragraph 3 as a two-item list.
- Method immediately follows with `To overcome these limitations...`.
- Separate contribution list: NOT PRESENT.
- Empirical diagnosis before method: NO.

### Related Work
- Organized into three method/domain families: LLM algorithm discovery; earlier automated algorithm discovery; photonic optimization.
- traditional→LLM: not linear overall; LLM methods first, then earlier methods, then domain methods.
- generation vs selection: NOT central.
- direct solving vs solver-assisted: NOT central.
- single heuristic vs portfolio: NOT central.
- static vs adaptive: mutation/evolution appears method, not RW taxonomy.
- offline vs online: NOT central.

### Gap language
- Introduction uses `by addressing two critical limitations` and explicit bullet labels `Generic Task Prompts`, `Limited Evolutionary Strategy Diversity`.
- Transition: `To overcome these limitations...`.
- Results use `However` to report a negative result where domain prompting harms photovoltaic performance.
- Novelty language is restrained: `we introduce`, `we systematically evaluate`, not a broad first/unexplored claim.

### Contributions
- Formal numbered/bulleted contribution section: NOT PRESENT.
- Method: structured domain prompt + dynamic mutation + ES exploration.
- Formulation: NO headline formulation contribution.
- Experimental: real photonic benchmark + systematic prompt/ES experiments + larger-scale transfer.
- Benchmark contribution: NO new benchmark; existing photonic testbeds migrated to IOHexperimenter.
- Empirical finding: domain knowledge is task-dependent; larger population ES not uniformly superior; generated algorithms competitive with established optimizers.

### Experimental writing
- Setup is explicitly divided into discovery and benchmarking, then Problem Setup → Performance Metric → Prompt Setup → Evolutionary Strategy Exploration → Benchmarking.
- Repetition protocol is stated directly beside each experiment: 5 discovery runs, 3 executions/candidate, 15 final benchmark runs.
- Baseline selection names five established domain algorithms and explains top-3 discovered algorithm selection by average AOCC.
- Negative/counterintuitive result is retained and followed by a control where all runs start from the same initial solution.
- Generalization is tested through small-instance discovery → larger-layer benchmarks.
- Statistical wording `not significant` lacks a reported test, an important audit caution.
- Runtime/hardware/API monetary cost are absent.

## Asset Metadata

- FULL TEXT READ: YES
- Source: `LLM/32_Photonic-Structures.md`
- Decision Layer: AHD / generalization
- Current-study Relation: 支持跨规模实验
- Innovation Boundary: 当前不构成候选 selector 机制的直接新颖性反证；已实现范围为 AHD / generalization，主要用于支持跨规模实验。
- Best Writing Claim: LLaMEA 式领域算法设计并测试跨规模泛化，重要性在于 generalization 评估而非具体应用。
