# 51｜LLMOPT 全文编码

- Source: `LLM/51_LLMOPT.md`
- Full-text status: **YES**
- Last read position: **EOF (line >1050 empty); Appendices A–M covered**
- Corpus: LLM / optimization modeling / learning-based solver generation
- Tier: B/C（generalization/self-correction evidence）

## A｜Research Content
- Research problem: natural-language optimization formulation and solving suffer limited accuracy and generality across problem types/domains.
- Problem setting: NL descriptions → mathematical formulation → Pyomo solver code → execution/correction across LP/IP/MIP/NLP/CO/MOP and other tasks.
- Objectives: improve “optimization generalization”, defined as accuracy + generality.
- Algorithm backbone: five-element intermediate formulation + multi-instruction SFT + KTO alignment + execution-based auto-testing/self-correction.
- Proposed mechanism: represent problems using Sets/Parameters/Variables/Objective/Constraints; augment and expert-label formulation/code data; SFT formulation and code-generation instructions; KTO on desirable/undesirable completions; at inference generate formulation/code, execute solver, inspect logs/results/errors, decide whether to return to formulation or code generation and self-correct.
- Decision layer: **optimizer/model formulation generation + solver-code generation + runtime correction routing**.
- State / Context: NL problem, five-element formulation, generated solver code, execution output/error logs; during alignment, instruction/completion/desirability triples.
- Action / Decision: formulate five elements; generate Pyomo code; self-correction judge chooses accept vs revise formulation vs revise code.
- Feedback / Reward: expert desirability labels for KTO; solver execution/error/output for self-correction; final correctness/optimal solution.
- Dynamic mechanism: iterative self-correction up to 12 re-solves; no external dynamic optimization environment/search-state operator control.
- LLM role: formulation, code generation, aligned optimization specialist, execution-error analysis/self-correction.
- RL role: KTO preference/model alignment; not scheduling/operator-selection RL.
- Claimed contribution: unified five-element definition; learning pipeline with multi-instruction SFT + KTO; automated self-correction; broad six-dataset generalization evaluation.
- Explicit limitation: optimization training data scarce/label quality problematic; expert labeling labor-intensive; structured data in databases/files not handled; performance varies with formulation difficulty; larger models improve results but increase training/deployment cost; o1 evaluation limited by access/cost.
- 与当前 FJSP-AGV 研究关系: indirect. It confirms that **real execution outcome/error → iterative LLM correction and routing** is established. Thus decoder/solver feedback followed by LLM revision is not novel alone. It does not model operator-specific competence, search/Pareto/environment context, or dynamic scheduling actions.

## B｜Experimental Design Coding
- Dataset / Benchmark: NL4Opt, Mamo Easy, Mamo Complex, IndustryOR, NLP4LP, ComplexOR.
- Instance scale: source datasets 1101/652/211/100(+3000 unlabeled)/65/19 respectively; main test totals shown as 100/100/100/100/37/11 after filtering/splitting. Approx. 20 scenarios and 7 optimization classes.
- Baselines: prompt-based Reflexion, Chain-of-Experts, OptiMUS; learning-based ORLM variants (Mistral-7B, Deepseek-Math-7B-Base, LLaMa3-8B); GPT-4 Direct/GPT-4 Turbo/GPT-4o; appendix correction comparisons.
- Baseline 数量: 3 named prompt frameworks + ORLM family/3 backbones + GPT-4 family; exact unique comparator configuration count varies by experiment, so no single aggregate baseline count is imposed.
- Independent runs: NOT REPORTED as repeated stochastic benchmark runs. Best-of-12 is an inference/correction comparator, not 12 independent algorithm runs.
- Random seeds: NOT REPORTED.
- Population size: NOT APPLICABLE.
- Generations: SFT 20 epochs; KTO 20 epochs.
- Evaluation budget: max self-correction = 12 re-solves; appendix Best-of-12 matched to this budget.
- Fitness / function evaluations: NOT APPLICABLE.
- Real decoding count: up to repeated formulation/code/correction calls; aggregate NOT REPORTED.
- Solver calls: up to 12 re-solves per test under correction; aggregate NOT REPORTED.
- LLM calls: aggregate NOT REPORTED.
- Token budget: training/inference max length 2048; API token totals NOT REPORTED.
- Runtime / wall-clock: NOT REPORTED.
- Hardware: training **8×A100 80GB**; inference **1×A100**.
- Metrics: Execution Rate (ER), Solving Accuracy (SA), Average Solving Times (AST); task-generalization accuracy.
- Statistical tests: NOT REPORTED.
- Confidence interval: NOT REPORTED.
- Ablation: w/o five-element, w/o KTO, w/o self-correction; joint removal; correction by GPT-4o vs Best-of-12 vs self-correction; larger-model comparison.
- Sensitivity analysis: no conventional parameter sweep; max correction budget fixed 12.
- Generalization / OOD: six datasets, ~20 domains, 7 optimization classes; NLP4LP and ComplexOR entirely excluded from training; 10 non-optimization task families used for seesaw/general capability check.
- Robustness: correction mechanism and cross-domain/type evaluation; repeated-seed robustness NOT REPORTED.
- Dynamic-event design: NOT PRESENT.
- LLM API / inference cost: cost discussed qualitatively for Qwen2-72B/o1; monetary/token cost NOT REPORTED.

## C｜Writing Evidence Coding
### Introduction
Actual sequence: **M1 optimization ubiquity → M2 expert-heavy formulation/solver-code problem → M3 prompt-based and learning-based LLM methods → M4 optimization generalization limitation → M5 define gap as accuracy + generality → M6 LLMOPT/five-element/SFT/alignment/self-correction → M7 empirical outcome embedded in method/contribution paragraph**.
- Limitation appears after prior-method overview, before method.
- Method follows immediately after formally defining the gap construct.
- No standalone numbered contribution list in Introduction.
- Empirical diagnosis before method: NO; gap is literature/problem based.

### Related Work
- Standalone Section 2.
- Organized by **functional method family**: LLMs for formulating/solving optimization problems; LLMs as optimizer components.
- First subsection explicitly splits prompt-based vs learning-based.
- Second broadens to LLM as crossover/mutation, trajectory generator, multiobjective optimizer, BO component.

### Gap language
- `Although previous research has established... their optimization generalization remains limited` performs capability acknowledgment + limitation.
- The paper immediately operationalizes the vague limitation into two measurable dimensions: accuracy and generality.
- `To narrow the gap between methods and practical applications` is motivation, not a “no prior work” claim.
- Discussion uses concrete remaining issues: scarce labeled data, expert cost, structured-data understanding, formulation difficulty.

### Contributions
- No formal numbered contribution list.
- Method contributions: five-element formulation; multi-instruction SFT + KTO alignment; execution-based self-correction.
- Data contribution: expert-reviewed/augmented training data pipeline.
- Experimental contribution: six-dataset, multi-domain/type generalization evaluation and component ablations.
- Benchmark contribution: NOT PRESENT as a new benchmark.

### Experimental writing
- Section 4 begins with **four explicit research questions Q1–Q4**, then answers them in named result paragraphs.
- Setup separates dataset split rules, metrics and correction budget.
- Fairness is explicitly discussed for Best-of-12 vs max-12 self-correction; external baseline results are cited from original papers to maintain reproduction consistency.
- Ablation directly maps components to RQs: five-element→Q3, KTO→Q4, self-correction→additional mechanism audit.
- Generalization is decomposed by dataset, domain and optimization type rather than asserted from one average score.
- Discussion includes model-size/cost tradeoff and general-task seesaw audit.
- Missing from empirical reporting: repeated stochastic runs, seeds, significance tests, CI, total wall-clock, total solver/API calls and monetary inference cost.

## Asset Metadata

- FULL TEXT READ: YES
- Source: `LLM/51_LLMOPT.md`
- Decision Layer: Modeling
- Current-study Relation: 外围
- Innovation Boundary: 当前不构成候选 selector 机制的直接新颖性反证；已实现范围为 Modeling，主要用于外围。
- Best Writing Claim: 用结构化 formulation 元素、SFT/alignment/self-correction 追求跨优化类型泛化。
