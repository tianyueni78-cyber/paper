# 60｜OptLLM / General Natural-Language Optimization 全文编码

- Source: `LLM/60_General-NL-Optimization.md`
- Full-text status: **YES**
- Last read position: **EOF (line >360 empty); no appendix present**
- Corpus: LLM / solver-assisted optimization modeling
- Tier: B/C

## A｜Research Content
- Research problem: general users/domain professionals face domain, mathematical and programming barriers in modeling/solving optimization problems; LLM arithmetic/logical reasoning and privacy are additional concerns.
- Problem setting: natural-language LP/MILP modeling and solving with external solver, optional open-source/fine-tuned LLM, multi-round user refinement and external data files.
- Objectives: complete problem descriptions, formulate and code them, solve with reliable external optimizer, interpret results and permit iterative edits.
- Algorithm backbone: **Interaction Refinement → Converter → Responser**. Query completion check → formulation → code → syntax diagnosis/self-feedback → solver → semantic validity check → user interaction/answer.
- Proposed mechanism: modular LLM+solver pipeline; missing-information detection; iterative dialogue/editing; grammar diagnostic loop; external-data separation; optional LoRA SFT.
- Decision layer: **Optimizer/model formulation + runtime workflow control**, not heuristic/operator selection.
- State / Context: user query/dialogue context, variables/objective/constraints/parameters, formulas, generated code, grammar feedback, solver result, user-defined semantic requirements.
- Action / Decision: request missing information; formulate; generate/reformulate code; call solver; accept/reject semantic result; interpret/refine.
- Feedback / Reward: grammar/syntax diagnostics, solver result, semantic validity and user feedback; no learned online reward in proposed framework.
- Dynamic mechanism: multi-round addition/deletion/modification and iterative correction; not dynamic optimization state/search adaptation.
- LLM role: interaction, formulation, coding, diagnosis and result interpretation; optionally SFT Qwen.
- RL role: NOT PRESENT.
- Claimed contribution: generic LLM+external-solver framework; three practical interaction patterns; prompt-based and fine-tuned model support; self-developed bilingual dataset/evaluation; cloud deployment path.
- Explicit limitation: incomplete problems requiring external/current knowledge can degrade effectiveness; model knowledge cutoff; RAG or model updating future work. Multi-round evaluation deferred due diverse acceptable answers.
- 与当前 FJSP-AGV 研究关系: indirect. It reinforces architectural separation of high-level language reasoning from reliable external numerical execution and explicit feedback loops. It does not address search-state-aware operator selection, operator competence, Pareto effects or adaptive operator redesign.

## B｜Experimental Design Coding
- Dataset / Benchmark: self-developed bilingual optimization data; En100 and CN100; part of En100 from NL4OPT dev data.
- Instance scale: training **15k** English+Chinese instances; test **100 English + 100 Chinese**.
- Baselines: GPT-3.5, GPT-4 prompt-based under OptLLM; Qwen-SFT proposed trained model.
- Baseline 数量: **2 prompt baselines** against Qwen-SFT.
- Independent runs: NOT REPORTED.
- Random seeds: NOT REPORTED.
- Population size: NOT APPLICABLE.
- Generations: NOT APPLICABLE.
- Evaluation budget: 200 test problems; SFT 20 epochs default.
- Fitness / function evaluations: NOT APPLICABLE.
- Real decoding count: NOT REPORTED.
- Solver calls: used by framework for final solution, but formula-generation accuracy is main metric; aggregate NOT REPORTED.
- LLM calls: NOT REPORTED.
- Token budget: NOT REPORTED.
- Runtime / wall-clock: NOT REPORTED.
- Hardware: **8 NVIDIA V100 GPUs** for Qwen-50B LoRA fine-tuning.
- Metrics: exact formula-generation accuracy requiring all variables/objective/constraints match ground truth.
- Statistical tests: NOT REPORTED.
- Confidence interval: NOT REPORTED.
- Ablation: not standard component ablation; studies fine-tuning epochs and training-data diversity/size.
- Sensitivity analysis: epochs 0–20; data sizes 500/1000/2000/4000 while roughly controlling training tokens.
- Generalization / OOD: bilingual EN/CN evaluation; broader real-world/domain generalization NOT formally tested.
- Robustness: NOT REPORTED.
- Dynamic-event design: NOT PRESENT.
- LLM API / inference cost: NOT REPORTED.

## C｜Writing Evidence Coding
### Introduction
Actual sequence: **M1 broad optimization applications → M2 conventional three-step expert workflow → M4 expertise burden → M3 LLM capability → M4 reasoning/privacy limitations → M6 OptLLM three-module solver-assisted framework**. Formal contribution list is NOT PRESENT as a dedicated numbered/bulleted block in the available Introduction.
- Limitation appears before method and distinguishes LLM reasoning weakness from privacy/deployment concern.
- Method is positioned as division of labor: LLM models, external solver calculates.
- Empirical diagnosis before method: NO.

### Related Work
- Standalone Section 2 with two method-family subsections: **Applications of LLMs** and **Techniques of LLMs**.
- Direct solving is contrasted with solver-assisted modeling: arithmetic reasoning remains weak, so external solver handles numerical optimization.
- Prompting vs SFT is introduced before experiments comparing both.

### Gap language
- Uses `However, despite...` to contrast NLP strength with arithmetic/logical weakness.
- `On the other hand` introduces privacy as an independent constraint rather than conflating it with reasoning.
- `In light of these above` transitions directly from the two limitations to a framework that supports both API and open-source models plus external solvers.

### Contributions
- No dedicated contribution enumeration.
- Method/system contribution: three-module OptLLM framework.
- Interaction contribution: multi-round refinement and external-data mode.
- Experimental contribution: prompt-vs-SFT bilingual evaluation.
- Dataset contribution: 15k self-developed training data + 200 manually checked tests, but not presented as a formal public benchmark contribution.

### Experimental writing
- Dataset construction and test set are separated clearly.
- Main metric is deliberately stricter than solver-result equivalence because equivalent objective values can hide incorrect/redundant formulations.
- Baseline prompting protocol and fine-tuning hyperparameters are reported before results.
- Sensitivity evidence isolates **training duration** and **data diversity/size**, with token exposure roughly controlled in the latter.
- Authors explicitly defer multi-round quantitative evaluation because acceptable answers are diverse, an example of not forcing an ill-defined metric.
- Missing: repeated seeds, statistical tests/CI, runtime/API cost and component-level framework ablation.
