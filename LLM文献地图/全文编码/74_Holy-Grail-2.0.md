# 74｜Holy Grail 2.0: From Natural Language to Constraint Models 全文编码

- Source: `LLM/74_Holy-Grail-2.0.md`
- Full-text status: **YES**
- Last read position: **EOF (line >300 empty); no appendix present**
- Corpus: LLM / optimization modeling
- Paper type: position paper / early demonstration
- Tier: B/C

## A｜Research Content
- Research problem: bridge natural-language problem descriptions and executable constraint-programming models.
- Problem setting: natural-language description → semantic entities → relations → formal formulation → modeling-language code → compile/run/fix → user refinement.
- Objectives: outline a modular LLM-assisted framework that reduces the expertise barrier of CP modeling and handles descriptions at different abstraction levels.
- Algorithm backbone: decomposition-based modular pipeline using LLM prompting and external modeling/solver tools.
- Proposed mechanism: four modeling subtasks: NER4OPT, relation extraction, formulation, translation; followed by automatic compile/run/debug and interactive model refinement.
- Decision layer: **Optimizer/model formulation generation**.
- State / Context: natural-language problem description; outputs of previous modules such as entities, domains, relations, constraint scopes and formal formulation; modeling-language requirements.
- Action / Decision: extract entities; identify relations; formulate model; translate to CPMpy/MiniZinc-like code; repair code; refine model with user.
- Feedback / Reward: compiler/runtime errors for fixing loop; user verification/refinement proposed for final loop. No scalar reward or learned online policy.
- Dynamic mechanism: modular iterative correction/refinement only; NOT dynamic optimization/search control.
- LLM role: task decomposition modules for extraction, relation identification, formulation, translation and potential bug fixing.
- RL role: NOT PRESENT.
- Claimed contribution: position-paper proposal of a modular step-by-step NL-to-constraint-model framework combining previously demonstrated subtasks; abstraction-level evaluation concept; early GPT-3.5/CPMpy examples.
- Explicit limitation: early/position-paper stage; broad quantitative evaluation is future work; one-step modeling can miss specifications; more LLMs/specialized methods/domain knowledge/fine-tuning/user interaction require study; increasing abstraction is expected to require more interaction.
- 与当前 FJSP-AGV 研究关系: indirect. It reinforces the distinction between **LLM direct monolithic generation** and **typed modular supervisory pipelines with external verification**. It does not address operator selection, Pareto search state, dynamic scheduling events or operator competence.

## B｜Experimental Design Coding
- Dataset / Benchmark: existing NL4Opt proposed for future evaluation; usage example uses one knapsack problem expressed at multiple abstraction levels.
- Instance scale: quantitative benchmark NOT PRESENT in this position paper; four abstraction levels are defined conceptually; examples shown for levels 1 and 4.
- Baselines: one-step modeling approach discussed from prior work, but no formal controlled baseline experiment in this paper.
- Baseline 数量: NOT APPLICABLE / NOT REPORTED as an experiment.
- Independent runs: NOT REPORTED.
- Random seeds: NOT REPORTED.
- Population size: NOT APPLICABLE.
- Generations: NOT APPLICABLE.
- Evaluation budget: NOT REPORTED.
- Fitness/function evaluations: NOT APPLICABLE.
- Real decoding count: NOT REPORTED.
- Solver calls: examples compile/run CPMpy models; aggregate calls NOT REPORTED.
- LLM calls: NOT REPORTED.
- Token budget: NOT REPORTED.
- Runtime / wall-clock: NOT REPORTED.
- Hardware: NOT REPORTED.
- Metrics: formal quantitative metrics NOT PRESENT; planned evaluation concerns modeling/recognition across abstraction levels.
- Statistical tests: NOT PRESENT.
- Confidence interval: NOT PRESENT.
- Ablation: NOT PRESENT.
- Sensitivity analysis: NOT PRESENT.
- Generalization / OOD: proposed four-level abstraction framework, not a completed quantitative generalization experiment.
- Robustness: NOT PRESENT.
- Dynamic-event design: NOT PRESENT.
- LLM API / inference cost: NOT REPORTED.
- Models/tools in demonstration: GPT-3.5 + prompt engineering + CPMpy.

## C｜Writing Evidence Coding
### Introduction
Actual sequence: **M1 CP Holy-Grail vision → M4 NL-to-formal-model expertise bottleneck → M3 LLM opportunity → M3 prior NL4OPT/NER/formulation work → M4 one-step and LP-centric limitations → M6 modular framework → paper organization**.
- Limitation appears in paragraph 2 and repeatedly inside prior-work comparison.
- Method appears after concrete decomposition of prior systems and their limitations.
- Explicit numbered contribution list: NOT PRESENT.
- Empirical diagnosis before method: only early one-step observations are mentioned; no formal empirical diagnosis.

### Related Work
- Related work is embedded in Introduction.
- Organization is method/process-stage based: NER → intermediate representation → relation extraction → formulation → CP translation/fixing.
- Particularly useful writing pattern: prior systems are compared by **which modeling stage they automate**, rather than by model name alone.

### Gap language
- Main rhetorical functions: bottleneck, capability limitation, decomposition motivation and transition.
- Gap is concrete: natural description still must be transformed by an expert; one-step systems can fail to satisfy specifications; prior target formulations mainly linear programs.
- The paper then maps each identified limitation to a specific module.

### Contributions
- No formal numbered/bulleted contribution section.
- Framework/design contribution: modular NL→CP pipeline.
- evaluation-concept contribution: abstraction levels.
- early demonstration: GPT-3.5 + CPMpy examples.

### Experimental writing
- This is not a mature experimental paper. Section 4 defines a planned evaluation axis and Section 5 presents qualitative examples.
- No baseline fairness protocol, repeated runs, inferential statistics, computational cost or quantitative ablation.
- Useful negative corpus evidence: a position paper can propose an architecture and examples without supporting population-level experimental-design claims; therefore it must not be counted as evidence for experimental norms.

## Asset Metadata

- FULL TEXT READ: YES
- Source: `LLM/74_Holy-Grail-2.0.md`
- Decision Layer: Modeling
- Current-study Relation: 外围
- Innovation Boundary: 当前不构成候选 selector 机制的直接新颖性反证；已实现范围为 Modeling，主要用于外围。
- Best Writing Claim: NER→relation→formulation→translation→fix/refine 的模块化建模路线，说明复杂建模依赖 pipeline 而非一次生成。
