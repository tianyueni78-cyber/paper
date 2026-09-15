# 59｜OptiMUS-0.3 全文编码

- Source: `LLM/59_OptiMUS-0.3.md`
- Full-text status: **YES**
- Last read position: **EOF (line >1300 empty); Appendices A–H covered**
- Corpus: LLM / optimization modeling / agentic solver-assisted system
- Tier: A/C

## A｜Research Content
- Research problem: automate and accelerate real-world MILP modeling/implementation despite long descriptions, large structured data, hallucination, and inefficient formulations.
- Problem setting: natural-language optimization description → mathematical model → Gurobi code → execution/debugging; human-in-the-loop webapp available.
- Objectives: improve modeling correctness, scalability and computational efficiency for optimization practitioners.
- Algorithm backbone: modular sequential agent: parameter/clause extraction → formulation/variables → per-clause coding → assembly/execution/debugging, with persistent JSON state and connection graph.
- Proposed mechanism: state/connection graph for context localization; reflective error correction; confidence-triggered stronger-LLM/user escalation; iterative execution debugging; structure-detection pool; advanced optimization coding/sifting.
- Decision layer: **Optimizer/model design + solver/structure selection + runtime workflow control**.
- State / Context: parameters, clauses, variables, background, mathematical/code representations, connection graph, errors, confidence, solver results.
- Action / Decision: extract/formulate/code components; correct or regenerate outputs; request stronger LLM/user help; detect solver structures; generate advanced solver code.
- Feedback / Reward: reflective checks, confidence score, execution/runtime errors, solver feasibility/objective correctness, user/stronger-LLM feedback.
- Dynamic mechanism: state incrementally updated across pipeline; iterative debugging max 5 attempts; confidence-based escalation; not search-process AOS.
- LLM role: modular reasoning/modeling/coding/error correction/structure detection.
- RL role: NOT PRESENT.
- Claimed contribution: NLP4LP 361-problem benchmark; modular OptiMUS-0.3; self-reflective/confidence error correction; advanced solver structure/coding modules; systematic ablation; webapp.
- Explicit limitation: current scope assumes sufficiently precise MILP-suitable descriptions; solver-level large-scale scalability not claimed; ambiguity, reliability/trust, fast solver choice, larger datasets and non-MILP paradigms remain future work.
- 与当前 FJSP-AGV 研究关系: indirect mechanism evidence. It strongly supports persistent structured state, targeted feedback/error correction, confidence-aware escalation and mechanism-specific ablation. It also explicitly identifies future fast-solver/heuristic/parameter selection from natural-language + structured problem information. It does **not** implement operator competence learning, search/Pareto state, predicted-vs-realized operator effect, or coverage-gap redesign.

## B｜Experimental Design Coding
- Dataset / Benchmark: NLP4LP, NL4OPT, IndustryOR; NLP4LP case studies.
- Instance scale: NLP4LP **361** = easy 289, hard 65, case studies 7; easy+hard dev 23/test 331; case descriptions avg 2578 chars. Data-scale tests 3KB–935KB / 2KB–385KB.
- Baselines: direct GPT-4o/o3, Reflexion, LLMOPT, ORLM, CoE, OptiMUS-0.2; plus naive full-data prompting in data-scale study.
- Baseline 数量: main comparison contains 7 named comparator method/configuration families before OptiMUS-0.3 variants; exact applicable count varies by benchmark.
- Independent runs: authoritative main accuracy primarily one pipeline outcome per instance; stochasticity study **30 instances × 5 seeds = 150 runs**; data-scale study **5 seeds per scale**.
- Random seeds: five independent seeds used; numeric seed values NOT REPORTED.
- Population size: NOT APPLICABLE.
- Generations: NOT APPLICABLE.
- Evaluation budget: debugging maximum **5 attempts**; 331 NLP4LP test instances plus case studies; data-scale 5 seeds/scale.
- Fitness / function evaluations: NOT APPLICABLE.
- Real decoding count: NOT REPORTED.
- Solver calls: repeated through execution/debugging/sifting; aggregate NOT REPORTED.
- LLM calls: modular calls throughout pipeline; aggregate NOT REPORTED.
- Token budget: max output tokens: GPT-4o 16,384; o1/o3 100,000; Llama3.1-70B 8,192. Aggregate token consumption NOT REPORTED.
- Runtime / wall-clock: 85 random NLP4LP instances, ≤350s, median **108s**; stage-level distribution; solver budget **600s** in data-scale study.
- Hardware: NOT REPORTED in paper text.
- Metrics: solve/correct rate, feasible rate, objective gap, pass@1/pass@5, error rates/confusion matrices, confidence calibration, runtime, correct-formulation rate.
- Statistical tests: NOT REPORTED.
- Confidence interval: NOT REPORTED.
- Ablation: w/o Debugging, Extraction EC, Modeling EC, LLM Feedback; different LLM capability; debugging iterations; structure/coding efficiency examples.
- Sensitivity analysis: debugging iteration count; model capability; data scale; description/problem complexity.
- Generalization / OOD: seven real-world case studies; IndustryOR; fine-tuned-model generalization comparison; large-data scaling.
- Robustness: 5-seed stochasticity study; easy vs hard consistency and pass@5.
- Dynamic-event design: NOT PRESENT.
- LLM API / inference cost: retraining-cost advantage discussed; exact API monetary cost NOT REPORTED.

## C｜Writing Evidence Coding
### Introduction
Actual sequence: **M1 optimization impact/expertise bottleneck → M2 practitioner-scoped task → M3 LLM opportunity → M4 four concrete scalability/reliability challenges → M6 OptiMUS and empirical system-architecture diagnosis → M2/M5 three scalability dimensions and explicit non-claims → M7 five bullet contributions**.
- Limitation/challenge appears before method and is unusually concrete: description length, data scale, hallucination, bad formulations.
- Method is preceded by explicit empirical framing: system architecture vs model capability.
- Contributions: **5 top-level bullets**, with one bullet containing 2 numbered subcomponents.
- Empirical diagnosis before method: YES in the revised paper framing; architecture bottleneck is stated as an ablation-supported finding and later demonstrated.

### Related Work
- Standalone Section 2 organized by method family: optimization modeling expertise → progress in LLMs → chatbots for optimization → benchmark-driven optimization modeling/fine-tuning/agentic approaches.
- Closest competitors are differentiated by output type, end-to-end capability, fine-tuning vs prompting/agents and benchmark scope.

### Gap language
- Strong practice: scope the claim and **explicitly state what is not claimed**, e.g. solver-level scalability outside current evidence.
- Uses named failure mechanisms rather than generic `few studies` language.
- Future-work gaps are phrased as concrete technical questions: reliability guarantees, trust/feedback, ambiguity resolution, fast solver/heuristic selection, larger datasets, beyond MILP.

### Contributions
- Count: **5 top-level contributions**.
- Benchmark: NLP4LP.
- Method/system: modular OptiMUS.
- Mechanism: reflective EC, confidence feedback, advanced modeling/coding.
- Experimental: ablation + benchmark/case-study comparisons.
- Artifact: public human-in-the-loop webapp.

### Experimental writing
- Evaluation is explicitly aligned to three scalability dimensions defined in Introduction.
- Main comparison groups methods by **direct prompting / fine-tuning / agentic frameworks**, a useful fairness/positioning structure.
- Repeated-run study clearly distinguishes `consistency across seeds` from authoritative accuracy, avoiding denominator abuse.
- Ablation states that each row removes one component while holding all others fixed and interprets percentage-point marginal changes.
- Failure analysis uses manual qualitative coding and separates extraction/formulation/coding failure mechanisms.
- Data-scale experiment fixes solver budget, success tolerance and seeds, and identifies two distinct baseline failure modes.
- Limitations/non-claims are carried into Results and Conclusion instead of being buried in a token final paragraph.
