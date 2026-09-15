# 71｜Synthesizing MILP Models from Natural Language 全文编码

- Source: `LLM/71_MILP-from-NL.md`
- Full-text status: **YES**
- Last read position: **EOF (line >760 empty); Appendix A.1–A.2 covered**
- Corpus: LLM / optimization modeling
- Tier: B/C

## A｜Research Content
- Research problem: synthesize MILP models from unstructured natural-language decision-problem descriptions, including binary variables and logic constraints.
- Problem setting: full problem description is manually partitioned into paragraphs, each describing an objective or constraint; framework converts text to a MILP formulation.
- Objectives: improve accessibility and correctness of automatic MILP formulation beyond one-shot LLM generation and simple LP datasets.
- Algorithm backbone: three-stage pipeline plus two preparation modules.
- Proposed mechanism: Stage 1 variable identification and binary-indicator generation; Stage 2 fine-tuned LLM constraint classification into objective + 13 constraint types; Stage 3 template-guided expression generation and automatic supplementation of linking constraints. Knowledge representation and templates constrain generation.
- Decision layer: **Optimizer/model formulation generation**.
- State / Context: full problem description, paragraph-level objective/constraint description, identified variable list, predicted constraint class, class-specific template.
- Action / Decision: identify variables; classify constraint/objective type; generate mathematical expression; add linking constraints.
- Feedback / Reward: no online reward/feedback loop. Fine-tuning uses labeled constraint descriptions.
- Dynamic mechanism: NOT PRESENT.
- LLM role: variable recognizer, fine-tuned classifier, template-conditioned formula generator.
- RL role: NOT PRESENT.
- Claimed contribution: three-stage unstructured-text-to-MILP framework; 30-problem MILP word-problem set with logic constraints/binary variables; fine-tuned constraint classifier; constraint templates.
- Explicit limitation: proof-of-concept covers limited constraint types; equality constraints largely absent; input paragraphs are manually partitioned; assumes full problem description; solver-language translation is future work; dataset needs expansion; hyperparameter tuning not performed.
- 与当前 FJSP-AGV 研究关系: indirect. It is evidence that **decomposing LLM decisions into typed intermediate representations/templates can outperform unconstrained direct generation**. It does not address heuristic/operator selection, search state, Pareto state, dynamic scheduling or empirical operator competence.

## B｜Experimental Design Coding
- Dataset / Benchmark: modified NL4Opt development set for classifier training/validation; new 30-problem MILP word-problem test set.
- Instance scale: 574 objective/constraint descriptions for fine-tuning = 391 decomposed NL4Opt descriptions + 183 created logic-constraint descriptions; train 464, validation 110. Test set: 30 problems, 30 objectives, 147 constraints.
- Baselines: direct zero-shot ChatGPT (GPT-3.5) and Bard (PaLM 2).
- Baseline 数量: **2** direct baselines; proposed framework has GPT and PaLM variants.
- Independent runs: NOT REPORTED.
- Random seeds: NOT REPORTED.
- Population size: NOT APPLICABLE.
- Generations: NOT APPLICABLE.
- Evaluation budget: fixed validation/test datasets; NOT REPORTED as call budget.
- Fitness/function evaluations: NOT APPLICABLE.
- Real decoding count: NOT REPORTED.
- Solver calls: NOT PRESENT for evaluation; translation to modeling languages/solver integration is future work.
- LLM calls: NOT REPORTED aggregate.
- Token budget: NOT REPORTED.
- Runtime / wall-clock: NOT REPORTED.
- Hardware: NOT REPORTED.
- Metrics: classifier accuracy; ACC1 complete-model accuracy; ACC2 expression-level classification accuracy; ACC3 expression-level formulation accuracy.
- Statistical tests: NOT REPORTED.
- Confidence interval: NOT REPORTED.
- Ablation: no formal component-removal ablation. Comparison of multi-stage GPT/PaLM vs direct chatbots and stage-specific accuracy/error analysis.
- Sensitivity analysis: NOT PRESENT. Hyperparameter tuning explicitly left to future work.
- Generalization / OOD: NOT FORMALLY REPORTED; new MILP logic-constraint test set differs from NL4Opt but is purpose-built rather than a formal OOD protocol.
- Robustness: error analysis by constraint type and variable identification; no stochastic robustness protocol.
- Dynamic-event design: NOT PRESENT.
- LLM API / inference cost: NOT REPORTED.
- Fine-tuning hyperparameters: GPT-3 ada epochs 4, batch 1, default LR multiplier; PaLM text-bison001 epochs 20, batch 24, LR 0.02.

## C｜Writing Evidence Coding
### Introduction
Actual sequence: **M1 real-world MILP/CO importance → M3 OR/IP background → M3 LLM opportunity → M6 broad research motivation → M3/M4 extensive literature review with method-specific limitations → M5 limitations of NL4Opt/simple LP and missing logic/binary structure → M6 proposed three-stage approach → M7 four explicit contribution bullets**.
- Limitation appears throughout the embedded literature review, with direct critiques of data-driven synthesis, equation extraction, OptiMUS/SNOP, NL4Opt and other modeling frameworks.
- Method contribution appears after the literature-review narrowing and is restated in Section 1.2.
- Contributions: **4 bullets**, explicitly listed.
- Empirical diagnosis before method: NO; literature/mechanism diagnosis precedes method.

### Related Work
- Related work is embedded as `1.1 Literature review` inside Introduction.
- Organization is roughly chronological + method-family narrowing: data-driven model synthesis → math word problems → LLM equation extraction → automated optimization modeling → NL4Opt → logic-constraint synthesis → newer LLM frameworks.
- Comparisons repeatedly state exactly which input structure/constraint types each predecessor can or cannot handle.

### Gap language
- Uses contrast and explicit limitation functions heavily: data availability/interpretability limits; structured-input assumptions; simple-sentence restrictions; limited constraint types; absence of binary variables/logic constraints.
- Strong writing pattern: **describe predecessor mechanism → identify a concrete representational limitation → contrast proposed stage/template design**.
- Some broad scarcity wording appears, but the actual methodological case is carried by concrete capability differences.

### Contributions
- Count: **4**, bulleted.
- Method/framework contribution.
- Benchmark/dataset contribution.
- classifier/fine-tuning contribution.
- knowledge/template contribution.

### Experimental writing
- Experiment section first defines model variants and direct baselines, then separates training data, test data, metrics, fine-tuning results, framework results and detailed failure analysis.
- Fairness: GPT/PaLM classifier variants use the same training/validation split.
- Results are decomposed into complete-model, classification and expression-level accuracy, making pipeline failure localization possible.
- Error analysis gives concrete missed/extra constraints, wrong coefficients/variables, binary-variable and linking-constraint failures rather than only aggregate accuracy.
- Weaknesses for corpus statistics: no repeated-run protocol, seeds, significance tests, CI, runtime, hardware, token/cost reporting or conventional ablation.

## Asset Metadata

- FULL TEXT READ: YES
- Source: `LLM/71_MILP-from-NL.md`
- Decision Layer: Modeling
- Current-study Relation: 外围
- Innovation Boundary: 当前不构成候选 selector 机制的直接新颖性反证；已实现范围为 Modeling，主要用于外围。
- Best Writing Claim: 把变量识别、约束分类和模板化 synthesis 拆开，代表结构化 MILP 建模 pipeline。
