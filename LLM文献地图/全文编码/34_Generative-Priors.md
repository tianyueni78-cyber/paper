# 34｜Sample-Efficient Optimization over Generative Priors via Coarse Learnability 全文编码

- Source: `LLM/34_Generative-Priors.md`
- Full-text status: **YES**
- Last read position: **EOF (line >1200 empty); Appendices A–C covered**
- Corpus: LLM / generative-prior optimization / MBO
- Tier: B（Supporting; theoretical boundary）

## A｜Research Content
- Research problem: finite-sample zeroth-order optimization when solutions should have low external cost while retaining probability under an expressive generative prior; classical MBO lacks finite-sample guarantees for approximate/misspecified learners.
- Problem setting: target distribution `p_T(s) ∝ L(s) exp(-T d(s))`; continuous non-convex optimization plus proof-of-concept combinatorial/LLM applications.
- Objectives: establish finite-sample guarantees; identify a coverage-style learnability condition; demonstrate the mechanism theoretically and qualitatively with generative models/LLMs.
- Algorithm backbone: TOPIFT heuristic → ALDRIFT model-based optimization with annealing, iterative model fitting and Metropolis-Hastings correction; specialized geometric annealing/rejection-sampling variant for bounded non-convex setting.
- Proposed mechanism: progressively move from prior to cost-weighted target through intermediate temperatures; fit a generative model at each stage; require `coarse learnability`, i.e. polynomial target coverage outside exponentially small atypical mass; use MH correction to prevent model-fitting error accumulation.
- Decision layer: **Optimizer/search-distribution adaptation**. In LLM proof-of-concept, the model distribution itself is adapted by fine-tuning. Not operator selection.
- State / Context: current generative distribution/model, temperature, sampled solutions, zeroth-order costs, target/prior likelihood ratios; prompt encodes local/global instance constraints in applications.
- Action / Decision: sample candidates, accept/correct samples, fit/update generative model; TOPIFT selects elite low-cost samples for fine-tuning.
- Feedback / Reward: zeroth-order objective `d(s)`; no RL scalar-policy training in ALDRIFT.
- Dynamic mechanism: iterative distribution adaptation across temperature/fine-tuning iterations; no external scheduling event.
- LLM role: generative prior and test-time adapted model in motivating/proof-of-concept experiments; GPT-2 used for iterative fitting. Frontier LLMs used only for cycle-capability illustration.
- RL role: NOT PRESENT in proposed algorithm; RL coverage/policy iteration used as conceptual relatives.
- Claimed contribution: coarse learnability; ALDRIFT; polynomial finite-sample convergence under the assumption; `O~(log 1/ε)` instantiation for quadratic-envelope non-convex optimization; theoretical plausibility via MLE/KDE; qualitative LLM evidence.
- Explicit limitation: formal guarantees do **not** yet apply directly to LLM inference-time alignment; general LLM coarse learnability remains open; ALDRIFT assumes tractable likelihood (Assumption 1); non-convex result needs known curvature bounds and ambient-dimension dependence; constrained empirical ALDRIFT stalls as MH acceptance approaches zero; TOPIFT LLM experiments are qualitative and do not verify density-ratio guarantee; spanning-tree optimum not obtained on all 15 test instances.
- 与当前 FJSP-AGV 研究关系: important conceptual boundary. `coverage` is already formalized as a dynamic property regenerated through iterative model fitting, and feedback-driven test-time adaptation can learn previously unknown combinatorial constraints. Therefore `learn from execution feedback`, `coverage gap`, or `iterative adaptation` alone are not novel abstractions. For FJSP-AGV, a competence-gap concept must be operationally different: coverage of **operator effects over scheduling/search contexts**, not probability-mass coverage of solution distributions.

## B｜Experimental Design Coding
- Dataset / Benchmark: synthetic 10-D non-convex objective; cycle detection; simplified line scheduling; low-degree spanning tree.
- Instance scale: non-convex `n=10`; cycle length variable, **50 random instances per k**; line scheduling `K=10`; spanning tree `n=16`, random extra edge probability 0.4, **15 test instances** mentioned.
- Baselines: non-convex ALDRIFT vs TOPIFT; line scheduling BEST-OF-LLM(N=1/400) vs TOPIFT; spanning tree BEST-OF-LLM and BEST-OF-ALG vs TOPIFT; cycle illustration compares GPT-4, Claude 3.5 Sonnet, Claude 3.7 Sonnet.
- Baseline 数量: varies by experiment; no single global count.
- Independent runs: non-convex **10 runs/algorithm**; line scheduling **20 independent TOPIFT runs**; cycle **50 random instances per k**; spanning tree reports 15 test instances but repeated stochastic runs per instance NOT REPORTED.
- Random seeds: NOT REPORTED.
- Population size: NOT APPLICABLE as EA population; TOPIFT elite/sample parameters explicit.
- Generations / iterations: line scheduling `Q=8`; spanning tree `Q=3`; non-convex annealing iterations determined by schedule to `T=20`.
- Evaluation budget: non-convex shared budget with `m=200`, MH chain `M=50` each step; line scheduling TOPIFT `m=4, M=12, Q=8` ≈ 384 samples vs BEST-OF-LLM `N=400`; spanning tree `m=4, M=50, Q=3`, total `N=600`.
- Fitness / function evaluations: zeroth-order costs per generated sample; exact aggregate for non-convex depends on iteration count, not stated as one total.
- Real decoding count: LLM samples correspond to generated solutions; line 384 vs baseline 400; spanning tree 600; cycle 50/model/k.
- Solver calls: NOT REPORTED / no conventional solver in empirical proof-of-concept.
- LLM calls: aggregate API calls NOT REPORTED; GPT-2 generation/fine-tuning sample counts above.
- Token budget: NOT REPORTED.
- Runtime / wall-clock: NOT REPORTED.
- Hardware: NOT REPORTED.
- Metrics: optimization error `||μ-x*||`; MH acceptance probability; algorithm cost/wait time; connected components minus one; degree violations; cycle success rate.
- Statistical tests: NOT REPORTED.
- Confidence interval: NOT REPORTED.
- Ablation: ALDRIFT inflated proposal+correction vs TOPIFT empirical variance/no correction; Appendix A analyzes necessity of MH; one-round vs iterative fine-tuning control in line scheduling (`Q=1` yields waiting time 81).
- Sensitivity analysis: two non-convex parameter settings; no systematic grid sensitivity.
- Generalization / OOD: theoretical multiple model classes; empirical multiple task types. Formal OOD split NOT PRESENT.
- Robustness: repeated runs/instances as above; authors explicitly report non-universal spanning-tree optimum and constrained-sampling stalling.
- Dynamic-event design: NOT PRESENT.
- LLM API / inference cost: NOT REPORTED.

## C｜Writing Evidence Coding
### Introduction
Actual structure is extended/theory-style: **M1 MBO domain/problem → M4 finite-sample limitation for expressive learners → M2 formal generative-prior objective → M4 classical MBO sampling/guarantee gap → M6 ALDRIFT mechanism → theoretical guarantees/instantiation → theoretical plausibility → motivating LLM application → qualitative empirical preview → M7 five-item contribution list**.
- Limitation appears in paragraph 1.
- Method appears in the `Simulated Annealing and ALDRIFT` move after formal problem/motivation.
- Contributions appear late in Introduction after substantial mechanism/theory preview.
- Contribution count: **5**, bulleted and type-labeled.
- Empirical diagnosis before method: NO formal empirical diagnosis; analytical failure modes motivate method. Empirical demonstrations come later.

### Related Work
- Organized by method/theory family: MBO/MRAS; sequential Monte Carlo; bandit convex optimization; Bayesian methods; additional non-convex comparison later in §5.4.
- traditional→learning→LLM: NO.
- generation vs selection: NO.
- direct solving vs solver-assisted: appears later as algorithm–LLM complementarity, not RW taxonomy.
- static vs adaptive: adaptive sampling/model fitting central, not explicit taxonomy.
- offline vs online: test-time/inference-time adaptation discussed later.

### Gap language
- `However` repeatedly narrows exact theoretical failure: asymptotic guarantees do not extend to finite-sample approximate learners; learned proposal can introduce compounding error.
- `In contrast` used for finite-sample guarantees and generative-proxy distinction.
- `Unlike` distinguishes ALDRIFT from exact exponential-family MBO and spatial partitioning.
- `Our work bridges this gap` is used after a precisely stated theory gap, not an unsupported novelty slogan.
- Limitations/future work are explicit in §5.4, empirical discussion and Conclusion rather than a standalone Limitations heading.

### Contributions
- Count: **5**, bulleted with bold functional labels: Conceptual Framework; MBO Algorithm; General Theoretical Guarantee; Unconditional Instantiation; Supporting Evidence.
- Method contribution: YES.
- Formulation/conceptual contribution: YES, coarse learnability/target formulation.
- Theoretical contribution: dominant.
- Experimental contribution: supporting/proof-of-concept, explicitly secondary.
- Benchmark contribution: NO.
- Empirical finding contribution: qualitative mass-covering behavior and failure-mode validation.

### Experimental writing
- Authors explicitly state empirical goal is **not SOTA**, but isolation of the theoretical mechanism under strict sample budgets.
- Fairness: ALDRIFT/TOPIFT share sample budget in non-convex experiment; line scheduling matches TOPIFT sample total approximately to `N=400`; spanning-tree baselines use same `N=600`.
- Results distinguish exact theorem claims from qualitative evidence and repeatedly state what the experiment **does not prove**.
- Negative results are preserved: ALDRIFT does not exactly reach optimum under constrained M; spanning-tree Hamiltonian path not achieved on all 15 instances.
- No significance tests/CI/runtime/hardware/cost, consistent with the paper’s theory-first positioning but relevant for later corpus coding.

## Asset Metadata

- FULL TEXT READ: YES
- Source: `LLM/34_Generative-Priors.md`
- Decision Layer: Hybrid generation/checking
- Current-study Relation: 支撑分工原则
- Innovation Boundary: 当前不构成候选 selector 机制的直接新颖性反证；已实现范围为 Hybrid generation/checking，主要用于支撑分工原则。
- Best Writing Claim: 把生成式模型先验与经典 checker/algorithm 结合，提供“生成负责提议、算法负责验证”的理论混合视角。
