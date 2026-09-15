# 56｜NL2OR / Abstract Operations Research Modeling 全文编码

- Source: `LLM/56_Abstract-OR-Modeling.md`
- Full-text status: **YES**
- Last read position: **EOF (line >480 empty); no appendix present**
- Corpus: LLM / OR modeling / solver triage / interactive what-if
- Tier: B/C（architecture/cost/error-handling evidence）

## A｜Research Content
- Research problem: OR model development requires specialist knowledge and long development cycles; existing closed-box AMP lacks feasibility/optimality guarantees, while open-box AMP still requires mathematical-programming/solver expertise.
- Problem setting: natural-language creation/editing of abstract OR models, data binding into concrete models, solver triage/execution and report generation for non-expert users.
- Objectives: create solver-agnostic reusable abstract model classes, instantiate them with user data, support multi-turn what-if editing, automatically select solver and produce solution/report.
- Algorithm backbone: NL query → LLM DSL/YAML generation → syntax/schema/AST validation → FORA abstract model → data mapping/concrete model → solver triage/execution → LLM report generator.
- Proposed mechanism: intermediate DSL representing InputData/Variable/Objective/Constraints; deterministic post-processing and JSON-schema validation; automatic solver triage; creation/edit branches; runtime failure can restart generation.
- Decision layer: **Optimizer/model formulation + algorithm/solver selection + runtime workflow control**.
- State / Context: user query; original YAML if editing; few-shot examples/schema; user data contract; generated DSL; validation/error logs; solver status/solution.
- Action / Decision: create/edit abstract model; repair syntax; reject/regenerate irreparable model; select solver; execute; generate report schema/report.
- Feedback / Reward: syntax/schema/undefined-variable validation; runtime error/status; solver result; no scalar learned reward.
- Dynamic mechanism: multi-turn what-if model editing and restart after malformed-model runtime errors; not dynamic scheduling/search-state adaptation.
- LLM role: DSL creation/editing and report generation.
- RL role: NOT PRESENT; RL explicitly future work.
- Claimed contribution: multi-turn abstract-model OR chat system; solver-agnostic abstraction; automatic solver triage; what-if editing; end-to-end implementation.
- Explicit limitation/future work: smaller-model effectiveness requires comprehensive study; RL improvement is future direction. Error pipeline still requires full restart for malformed runtime models; user-data/model mismatches remain possible.
- 与当前 FJSP-AGV 研究关系: indirect but useful for architecture discipline. It shows explicit separation among **model generation, deterministic validation, solver selection, execution and reporting**, and evaluates accuracy/latency/token/cost jointly. Automatic solver triage is algorithm selection, not operator selection. It does not learn operator competence or search/Pareto context.

## B｜Experimental Design Coding
- Dataset / Benchmark: custom practical OR creation set; custom edit scenarios; LPWP/NL4Opt test data.
- Instance scale: **30** OR creation statements across 9 problem categories; **60** edit scenarios derived from 15 validated YAMLs ×4 queries; **287** LPWP test samples.
- Baselines: experiments mainly compare GPT-3.5-turbo-16k, GPT-4-32k, and for LPWP GPT-4o; architecture comparison table includes OptiGuide, OptiMUS, Chain-of-Experts but not a matched numerical baseline experiment.
- Baseline 数量: model comparison 2 in custom creation/edit experiments, 3 in LPWP; architecture comparison 3 prior systems.
- Independent runs: Valid@k uses up to k=1/3/5 attempts; conventional independent algorithm-run count NOT REPORTED.
- Random seeds: NOT REPORTED.
- Population size: NOT APPLICABLE.
- Generations: NOT APPLICABLE.
- Evaluation budget: k=1/3/5 attempts for custom model creation/edit; 287 LPWP samples at temperature .1.
- Fitness / function evaluations: NOT APPLICABLE.
- Real decoding count: reflected by Valid@k attempts; aggregate API completions NOT REPORTED.
- Solver calls: generated models are executed for validity; aggregate NOT REPORTED.
- LLM calls: aggregate NOT REPORTED.
- Token budget: LPWP reports mean prompt tokens: GPT-4o 2230.76±22.12; GPT-4-32k and GPT-3.5-turbo-16k 2852.61±22.34 as table reported.
- Runtime / wall-clock: latency mean/std/P50/P75/P90 reported.
- Hardware: NOT REPORTED.
- Metrics: Valid@1/@3/@5; LPWP accuracy/Valid@1; latency mean/std/percentiles; prompt tokens; total USD cost.
- Statistical tests: NOT REPORTED.
- Confidence interval: NOT REPORTED.
- Ablation: model and temperature comparison; not component ablation.
- Sensitivity analysis: temperature **0.1, 0.2, 0.4, 0.6, 0.8** for GPT-3.5/GPT-4 on custom creation/edit.
- Generalization / OOD: multiple OR categories and external LPWP/NL4Opt dataset; no formal OOD split terminology.
- Robustness: Valid@k repeated attempts and temperature sweep; no statistical hypothesis tests.
- Dynamic-event design: NOT PRESENT.
- LLM API / inference cost: **explicitly reported** for LPWP: GPT-4o $2.84, GPT-4-32k $30.45, GPT-3.5-turbo-16k $0.57 total for experiment, using stated token-price formula.

## C｜Writing Evidence Coding
### Introduction
Actual sequence: **M1 OR/MP practical importance/examples → M4 specialist/development-cycle barrier → M3 closed/open AMP alternatives → M4 limitations of each → M6 NL2OR natural-language DSL/solver pipeline → M6 abstract-model/what-if distinction → M7 dedicated Contributions and Organization subsection with 2 novelty claims + pipeline capabilities**.
- Limitation appears early and is structured by closed-box vs open-box trade-off.
- Method follows after contrasting both AMP families.
- Contribution section is explicitly titled; **2 numbered novelty claims**, followed by 3 pipeline functions.
- Empirical diagnosis before method: NO.

### Related Work
- Standalone Section 2: LLM background/prompting → Automated Mathematical Programming.
- Then a dedicated **Comparison with current work** table compares OptiGuide/OptiMUS/Chain-of-Experts/NL2OR by what-if, E2E, optimizer, external knowledge, validation/error correction, complexity, modeling type.
- This is feature-based competitor positioning rather than chronology.

### Gap language
- Uses closed-box/open-box **capability trade-off** rather than broad absence claims.
- `To mitigate the limitations...` directly links mechanism to identified drawbacks.
- Novelty claims are narrowed to multi-turn abstract-model generation and automatic solver triage, with a competitor feature table supplied immediately afterward.

### Contributions
- Explicit subsection.
- Count: **2 numbered novelty claims**, plus 3 implementation capabilities.
- Method/formulation contribution: abstract reusable OR model generation/editing.
- System contribution: automatic solver triage/end-to-end pipeline.
- Experimental contribution: practical OR scenarios + LPWP model/cost evaluation.
- Benchmark contribution: NOT PRESENT.

### Experimental writing
- Experiments are divided by **creation → editing → external LPWP dataset**, mirroring system capabilities.
- Creation/edit experiments report Valid@k plus latency distribution, not accuracy alone.
- Temperature is treated as a sensitivity dimension.
- LPWP explicitly adds **prompt tokens + USD cost + latency**, allowing model-quality/cost trade-off analysis.
- Results acknowledge cheaper/smaller models can fail on ambiguous mathematical optimization, while editing is easier than creation.
- Missing: seeds, hypothesis tests, CI, hardware and aggregate solver-call accounting.
