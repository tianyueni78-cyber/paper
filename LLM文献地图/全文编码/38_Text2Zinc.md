# 38｜TEXT2ZINC 全文编码

- Source: `LLM/38_Text2Zinc.md`
- Full-text status: **YES**
- Last read position: **EOF (line >1000 empty); Appendices A1–A3 covered**
- Corpus: LLM / OR modeling / constraint programming
- Tier: B（Supporting）

## A｜Research Content
- Research problem: translate natural-language optimization/satisfaction problems into executable solver-agnostic MiniZinc models and provide a cross-domain benchmark for this task.
- Problem setting: natural-language problem description + parameter/data specification → MiniZinc model; both optimization and satisfaction; LP/MIP/CP and multiple application domains.
- Objectives: build TEXT2ZINC; establish baseline execution/solution accuracy; compare prompting/decomposition/intermediate-representation strategies.
- Algorithm backbone: GPT-4 prompting pipeline with vanilla, CoT, compositional multi-call, and knowledge-graph intermediate representation variants; MiniZinc execution/ground-truth objective validation.
- Proposed mechanism: progressively expose nomenclature/examples/shape/KG or decompose model generation into parameters+variables, constraints, objective, and stitch into complete code.
- Decision layer: **Optimizer/model formulation generation**, not scheduling/operator selection.
- State / Context: problem description, parameter definitions/symbols/shapes, data examples, metadata, optional knowledge graph, previously generated code components in compositional approach.
- Action / Decision: generate MiniZinc model or model components.
- Feedback / Reward: execution success and equality of generated objective value to ground truth; no online feedback loop used to revise a generated model in the reported baseline pipeline.
- Dynamic mechanism: NOT PRESENT.
- LLM role: direct formal-model/code generator and optional intermediate KG generator.
- RL role: NOT PRESENT.
- Claimed contribution: unified cross-domain optimization+satisfaction dataset; solver-agnostic MiniZinc representation; baseline study of prompting/composition/KG; public leaderboard.
- Explicit limitation: LLMs are not plug-and-play for combinatorial modeling; low solution accuracy; syntax/type/indexing/constraint errors; LLMs can misclassify optimization as satisfaction; KG did not reliably improve solution quality; future work needs alternative intermediate representations/agentic frameworks and larger high-quality datasets. Standalone `Limitations` heading NOT PRESENT.
- 与当前 FJSP-AGV 研究关系: boundary/supporting evidence. It strengthens the distinction between **LLM as formal-model generator** and **LLM as search supervisor/operator selector**. Its execution-vs-solution gap is also a useful warning that syntactic/executable validity is not equivalent to optimization quality; for current work, valid LLM strategy output must be separated from actual downstream Pareto/search effect.

## B｜Experimental Design Coding
- Dataset / Benchmark: TEXT2ZINC overall 110 curated problems; experiments use NLP4LP subset.
- Instance scale: TEXT2ZINC table: 64 LP, 31 MIP, 15 CP = 110; experimental NLP4LP sample reports 66 problems before excluding 9/26/27 and **63 final problems**. Earlier dataset-source paragraph says NLP4LP 65 included; this is an internal count inconsistency and must not be silently reconciled.
- Baselines / variants: Basic; +Data & examples; +Shape; +Knowledge Graph; CoT with data; CoT+Examples; CoT+Shape; Multi-Call+Composition.
- Baseline 数量: **8 prompting/method variants**.
- Independent runs: NOT REPORTED.
- Random seeds: NOT REPORTED.
- Population size: NOT APPLICABLE.
- Generations: NOT APPLICABLE.
- Evaluation budget: one generated model per problem/strategy is implied by Algorithm 1, but repeated-call sampling budget NOT REPORTED; compositional method uses multiple sequential calls per problem.
- Fitness / function evaluations: NOT APPLICABLE.
- Real decoding count: aggregate NOT REPORTED.
- Solver calls: generated models are compiled/executed for evaluation; aggregate exact calls NOT REPORTED.
- LLM calls: vanilla/CoT one CallLLM in high-level algorithm; compositional uses multiple component calls + stitch, but aggregate exact call count NOT REPORTED.
- Token budget: NOT REPORTED.
- Runtime / wall-clock: NOT REPORTED.
- Hardware: NOT REPORTED.
- Metrics: Execution Accuracy; Solution Accuracy.
- Statistical tests: NOT REPORTED.
- Confidence interval: NOT REPORTED.
- Ablation: the eight progressively modified prompting variants function as component/information ablations, although not labeled a formal ablation section.
- Sensitivity analysis: NOT PRESENT.
- Generalization / OOD: dataset itself spans 11 domains and LP/MIP/CP, but reported baseline experiment is restricted to NLP4LP optimization problems; no formal OOD experiment.
- Robustness: error taxonomy in Appendix A3; repeated stochastic robustness NOT REPORTED.
- Dynamic-event design: NOT PRESENT.
- LLM API / inference cost: NOT REPORTED.

## C｜Writing Evidence Coding
### Introduction
Actual sequence: **M2/M4 natural-language constraint-modeling problem and cognitive bottleneck → M3 solver-agnostic modeling languages → M4 LLM mathematical/logical consistency gap → M7 contribution/dataset introduction**. The detailed literature gap and method baselines are developed later in Background/Related Work and Experimental Methodology rather than a conventional M6-heavy introduction.
- Limitation: paragraph 1 and paragraph 3.
- Method: dataset contribution appears in `Our Contributions`; experimental prompting methods appear later.
- Contributions: prose, not a numbered contribution list; primary contribution plus dataset construction/curation framing.
- Empirical diagnosis before method: NO.

### Related Work
- Organization: roughly chronological/method progression from NL4OPT/entity recognition → modeling assistants/annotation → multi-agent systems → training/custom LLMs → CP/RAG/domain-specific applications.
- traditional→learning→LLM: background separates classical modeling languages from LLM work, but RW itself is LLM-centric.
- generation vs selection: NO.
- direct solving vs solver-assisted: modeling/code generation vs solver-specific systems is discussed.
- static vs adaptive / offline vs online: NO.
- Ends with an explicit three-part differentiation of TEXT2ZINC from prior work.

### Gap language
- `However, these systems remain tied to specific solvers...` narrows a concrete dependency limitation.
- `remained constrained by single-solver dependency` repeats solver dependence as evidence.
- Own gap paragraph uses `addresses several key limitations`, then `First / Second / Finally` to map limitation → contribution.
- Strong claim `first to encompass optimization and satisfaction problems` appears in Dataset Statistics and should be treated as an author claim, not corpus fact.

### Contributions
- No clean numbered list.
- Benchmark/dataset contribution: dominant.
- Method contribution: baseline prompting/compositional/KG study, not a new optimization algorithm.
- Formulation contribution: unified MiniZinc task representation.
- Experimental contribution: eight-strategy baseline and error analysis.
- Empirical finding: examples/CoT/composition improve execution/solution differently; extra shape/KG can hurt.

### Experimental writing
- Methodology explicitly states the goal is to establish a **reasonable lower-bound baseline**, which calibrates claim strength.
- Variants are introduced cumulatively so the effect of added information/structure can be isolated.
- Results are organized by method family, then end with cross-method observations: execution-solution gap, execution errors, information sweet spot, reasoning-vs-structure.
- Negative/counter-intuitive results are reported rather than hidden: shape information can degrade performance; KG improves execution but worsens solution accuracy; compositional best execution does not yield best solution accuracy.
- No repeated-run variance/significance/CI/runtime/cost reporting.

## Asset Metadata

- FULL TEXT READ: YES
- Source: `LLM/38_Text2Zinc.md`
- Decision Layer: Modeling
- Current-study Relation: 说明直接生成并不天然可靠
- Innovation Boundary: 已占据或直接限制的边界：NL→constraint model 的结果暴露 push-button modeling 可靠性边界，是直接生成模型的反例型证据。
- Best Writing Claim: NL→constraint model 的结果暴露 push-button modeling 可靠性边界，是直接生成模型的反例型证据。
