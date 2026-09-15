# 14 Large Language Models in Operations Research: Methods, Applications, and Challenges｜全文编码

## Audit
- Source: `LLM/14_Survey-LLM-in-OR.md`
- Full text read to EOF: YES
- Abstract, Introduction, basic principles, automatic modeling, assisted optimization, direct solving, benchmarks, domain applications, Conclusion/Outlook, references: READ.
- Primary experimental setup/results/ablation for this survey itself: NOT PRESENT.

## A. Research Content
- Research problem: systematically organize LLM-driven OR methods, applications, evaluation and challenges.
- Problem setting: survey across OR modeling and solving, including combinatorial/evolutionary/multiobjective/scheduling applications.
- Objectives: unify fragmented perspectives into automatic modeling, auxiliary/assisted optimization and direct solving; map applications and future directions.
- Algorithm backbone: NOT APPLICABLE (survey).
- Proposed mechanism: taxonomy/review framework rather than an optimizer.
- Decision layer: survey spans modeling, operator/heuristic generation, selection/search control and direct solving; paper itself has no runtime decision layer.
- State / Context, Action / Decision, Feedback / Reward: NOT APPLICABLE to the survey itself.
- Dynamic mechanism: NOT APPLICABLE; survey includes dynamic scheduling and adaptive optimization literature.
- LLM role: taxonomy includes modeler, heuristic/operator generator, search collaborator/controller, direct solver and multimodal reasoner.
- RL role: reviewed as a fusion route with LLM, including heuristic-pool selection and preference/RL training.
- Claimed contribution: cross-paradigm review unifying automatic modeling, assisted optimization and direct solving, plus domain applications and frontier outlook.
- Explicit limitations/challenges: unstable semantic-to-structure mapping; fragmented research/unified framework absence; limited generalization/interpretability; insufficient evaluation; computational/industrial deployment barriers.
- Relation to FJSP-AGV: high-value landscape/boundary source. It explicitly covers SeEvo dynamic scheduling, HeurAgenix strategy evolution/selection, RL heuristic-pool selection, multiobjective LLM evolution, search-trajectory control and JSSP applications. It therefore weakens novelty claims based only on `LLM + dynamic scheduling`, `LLM + operator generation`, `LLM + selection`, or `LLM + multiobjective optimization`.

## B. Experimental Design
- Dataset / Benchmark: NOT APPLICABLE as original experiment; survey reviews NL4OPT, MAMO, IndustryOR, OptiBench, CP-Bench, NLGraph, GraphArena, ORQA, CO-Bench, FrontierCO, HeuriGym, ALE-Bench, OPT-BENCH and others.
- Instance scale: NOT APPLICABLE as one experiment.
- Baselines / count: NOT APPLICABLE.
- Independent runs / seeds / population / generations / FE / real decoding / solver calls / LLM calls / token budget / runtime / hardware / statistical tests / CI: NOT REPORTED for an original experiment because none is conducted.
- Metrics: survey discusses accuracy/equivalence, feasibility/optimality, quality/yield, efficiency, robustness, interpretability, but does not define one original evaluation protocol.
- Ablation / sensitivity / generalization / robustness / dynamic-event design / LLM cost: NOT PRESENT as original experimental analyses.

## C. Writing Evidence
### Introduction
- M1 OR importance and traditional limitations → M3 LLM opportunity/capabilities → M4 current instability/fragmentation/interpretability limits → M5 need for systematic review → M6 three-perspective review framework → M7 three bullet contributions → comparison against prior surveys.
- Contribution count: 3 bullets, followed by explicit differentiation from prior surveys.

### Review organization
- Top-level taxonomy: Basic principles → LLM-based OR methods → Domain problems → Conclusion/outlook.
- Method section: Automatic Modeling vs LLM-assisted Optimization; assisted optimization then hybrid mechanisms vs LLM-dominated solving.
- Hybrid mechanisms further divide heuristic structure evolution, multiobjective collaboration, and cross-paradigm fusion.
- Direct solving divides single-modal and multimodal structure-aware approaches.
- Strong taxonomy + method-family + evolutionary-phase organization.

### Gap language
- Uses contrast and synthesis: `Although recent studies...`, `remain confined`, `has yet to emerge`, `limitations remain evident`, `Yet they remain limited`, followed by explicit future-work directions.
- Gap claims are usually attached to categories/benchmarks rather than a single new method.

### Contributions
- 3 labeled bullets: Methodological Paradigm Summary, Domain Application Analysis, Frontier Trends Outlook.
- Survey contribution types: taxonomy/synthesis, application synthesis, future-trend analysis.

### Experimental writing
- NOT APPLICABLE as original experiment.
- For reviewed benchmarks, prose often follows benchmark purpose → scale/coverage → evaluation mechanism → observed limitation.

### Novelty strength
- Moderate survey-positioning claim: emphasizes unification/comprehensiveness relative to earlier surveys, without claiming invention of optimization mechanisms.

## Evidence relevant to later technical-evolution testing
- Survey explicitly describes heuristic evolution from LLM generation to multi-agent strategy evolution/selection and dynamic scheduling.
- Multiobjective route explicitly includes LLM offspring generation, LLM search operators, stagnation-triggered low-cost invocation, executable mutation-operator generation, multiobjective heuristic evolution and system-level coordination.
- Cross-paradigm route explicitly includes classical operators, RL, neuro-symbolic systems, and search trajectory control/reasoning.
- These are survey-level claims and must be verified against original direct competitors before final Research Gap statements.

## Asset Metadata

- FULL TEXT READ: YES
- Source: `LLM/14_Survey-LLM-in-OR.md`
- Decision Layer: Field taxonomy
- Current-study Relation: 定义大类，不直接证明 novelty
- Innovation Boundary: 当前不构成候选 selector 机制的直接新颖性反证；已实现范围为 Field taxonomy，主要用于定义大类，不直接证明 novelty。
- Best Writing Claim: 提供 modeling、auxiliary optimization、direct solving 等宏观分类，是定位 LLM 在 OR 中角色的基础入口。
