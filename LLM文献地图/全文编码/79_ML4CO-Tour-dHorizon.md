# 79｜Machine Learning for Combinatorial Optimization: a Methodological Tour d’Horizon 全文编码

- Source: `LLM/79_ML4CO-Tour-dHorizon.md`
- Full-text status: **YES**
- Last read position: **EOF (line >860 empty); no appendix present**
- Corpus: ML / CO methodological foundation
- Tier: A/B

## A｜Research Content
- Research problem: how to integrate ML into combinatorial-optimization algorithms so learned decisions exploit distributions of problem instances while retaining useful CO structure/guarantees.
- Problem setting: partially learned CO algorithms; optimization instances are treated as data sampled from an implicit target distribution.
- Objectives: survey methodological routes, distinguish learning objectives and ML–CO integration patterns, and articulate generalization/evaluation/practical challenges.
- Algorithm backbone: survey/methodological framework; NOT a single proposed optimizer.
- Proposed mechanism/taxonomy: two learning motivations, **demonstration/imitation** vs **experience/reward**; and multiple integration patterns including end-to-end solution generation, ML providing parameters/high-level information, and **ML repeatedly queried alongside a master optimization algorithm using current algorithm state**.
- Decision layer: broad; includes algorithm configuration, branching/cut/heuristic decisions, repeated low-level decisions and direct solution generation. The most relevant category for current work is **recurrent algorithmic decision / runtime control inside a master optimizer**.
- State / Context: in repeated-decision setting, the environment is the **internal state of the optimization algorithm**, possibly including problem definition. A policy maps available state/context to an action.
- Action / Decision: algorithmic decision such as branching variable, cut selection, whether to run a heuristic, node/action choice, parameter/configuration choice.
- Feedback / Reward: imitation uses expert action labels; experience/RL uses reward/return. The paper stresses that surrogate accuracy/reward is not necessarily aligned with the true optimization performance measure.
- Dynamic mechanism: yes at algorithm-execution level. The same learned policy can be queried repeatedly throughout optimization as internal state changes.
- LLM role: NOT PRESENT; paper predates current LLM optimization wave.
- RL role: policy discovery from experience; state-action-reward MDP framing; delayed/sparse reward and reward shaping discussed.
- Claimed contribution: methodological synthesis of ML4CO; instance-distribution/generalization framing; orthogonal taxonomy of learning method and ML–CO integration; practical guidance/challenges.
- Explicit limitation/challenges: feasibility, modeling/representation, scaling, data generation, distribution shift/generalization, sparse/surrogate rewards, learning cost, inability to assume ML accuracy implies optimization performance.
- 与当前 FJSP-AGV 研究关系: **foundational and potentially novelty-reducing**. Search-state-conditioned repeated decisions inside a master optimizer were already a general ML4CO paradigm by 2020. Likewise, predicting whether a heuristic will improve the incumbent and running it conditionally is explicitly surveyed. Therefore `optimizer-internal state → learned selector → operator/heuristic decision` is not a new architecture. The current candidate must distinguish itself through the exact scheduling context, multiobjective empirical effect/competence representation, uncertainty/coverage behavior and redesign mechanism, if those survive competitor audit.

## B｜Experimental Design Coding
- Dataset / Benchmark: survey; NOT APPLICABLE as one experiment.
- Instance scale: NOT APPLICABLE.
- Baselines: NOT APPLICABLE.
- Baseline 数量: NOT APPLICABLE.
- Independent runs: methodological framework explicitly models algorithm/environment randomness `τ`; no original repeated-run experiment.
- Random seeds: NOT APPLICABLE.
- Population size: NOT APPLICABLE.
- Generations: NOT APPLICABLE.
- Evaluation budget: conceptual; performance measure may include objective, bounds, running time and resource usage.
- Fitness/function evaluations: NOT REPORTED as a single protocol.
- Real decoding count: NOT APPLICABLE.
- Solver calls: NOT APPLICABLE.
- LLM calls: NOT APPLICABLE.
- Token budget: NOT APPLICABLE.
- Runtime / wall-clock: central evaluation concern in surveyed examples; no paper-level runtime.
- Hardware: NOT APPLICABLE.
- Metrics: methodological emphasis on **true optimization performance metric** rather than only surrogate ML metric; examples include solution quality, bounds, running time, resource usage, B&B node count.
- Statistical tests: NOT a paper-level experimental protocol.
- Confidence interval: NOT APPLICABLE.
- Ablation: NOT APPLICABLE.
- Sensitivity analysis: NOT APPLICABLE.
- Generalization / OOD: major theme. Separate train/validation/test; instance distribution must match deployment interest; OOD and scale generalization are difficult; learned TSP policies degrade beyond training sizes in surveyed studies.
- Robustness: distribution shift, stochastic trajectories, external parameters and representation are explicitly considered.
- Dynamic-event design: no FJSP event benchmark; dynamics are optimizer/MDP state transitions.
- LLM API / inference cost: NOT APPLICABLE.

## C｜Writing Evidence Coding
### Introduction
Actual sequence: **M1 OR/CO industrial relevance + hardness → M3 practical success via problem structure/expert heuristics → M5 opportunity to learn algorithmic decisions from implicit instance distributions → M3 ML strengths → M6 two ML-for-CO motivations → M2/M6 instance-distribution/generalization framing → M4 exploratory maturity boundary → paper roadmap**.
- Limitation is distributed: NP-hardness first, then expert/manual decision limitations and generalization concerns.
- Methodological framework is introduced through a concrete Montreal-TSP scenario rather than an immediate formal contribution list.
- Explicit numbered contribution list: NOT PRESENT.
- Empirical diagnosis before method: NO; conceptual/example-driven diagnosis.

### Related Work
- The survey body itself is the related-work synthesis.
- Organization is **orthogonal taxonomy**, not chronology: learning by demonstration vs experience; then how ML is embedded relative to the optimization algorithm.
- Particularly relevant writing move: the same paper can fit overlapping integration categories, and the authors explicitly acknowledge overlap instead of forcing mutually exclusive bins.

### Gap language
- Functions: computational bottleneck, unsatisfactory expert decisions, unknown instance distribution, generalization challenge, surrogate-objective mismatch, practical deployment constraints.
- The paper rarely relies on “few studies” as the main argument. It motivates research from **decision cost/quality and distributional structure**.

### Contributions
- No numbered contribution list.
- survey/methodological contribution: ML4CO integration taxonomy.
- conceptual contribution: optimization problems as data drawn from an implicit distribution.
- methodological contribution: true performance objective vs surrogate learning objective; generalization framing.

### Experimental writing
- No original experiment, but unusually strong methodological evaluation guidance.
- Key principle: **classification/policy accuracy is insufficient if it does not reveal downstream optimization cost**. Real optimization performance must also be reported.
- Train/validation/test roles are explicitly separated to avoid selecting on the test set.
- Generalization should be defined relative to the intended distribution of optimization instances, not treated as an abstract universal property.
- Practical evaluation should include feasibility, scaling, data-generation representativeness and deployment/runtime consequences.
- For the current paper this supports separating selector-decision correctness/prediction quality from realized `ΔHV/ΔCmax/ΔTEC/...` optimization effects.

## Asset Metadata

- FULL TEXT READ: YES
- Source: `LLM/79_ML4CO-Tour-dHorizon.md`
- Decision Layer: Field taxonomy
- Current-study Relation: 背景
- Innovation Boundary: 当前不构成候选 selector 机制的直接新颖性反证；已实现范围为 Field taxonomy，主要用于背景。
- Best Writing Claim: 提供 ML4CO 与传统 OR/ML 的全景方法背景，是更大尺度的基础定位文献。
