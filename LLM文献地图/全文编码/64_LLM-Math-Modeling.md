# 64｜LLMs for Mathematical Modeling / Mamo 全文编码

- Source: `LLM/64_LLM-Math-Modeling.md`
- Full-text status: **YES**
- Last read position: **EOF (line >840 empty); Appendices A–T covered**
- Corpus: LLM / mathematical modeling benchmark / solver-based evaluation
- Tier: B/C

## A｜Research Content
- Research problem: automatic, faithful evaluation of LLM mathematical modeling when multiple formulations can be equivalent and direct formula/string matching is inadequate.
- Problem setting: natural-language question Q → LLM mathematical model M* → external solver → numerical answer A* → compare with ground truth A. Domains are ODE, Easy LP and Complex LP/MILP.
- Objectives: isolate and evaluate modeling capability through solver-based process evaluation; build a benchmark that is automatically verifiable.
- Algorithm backbone: benchmark construction/quality control → LLM formalization → solver execution → numerical answer matching; optional syntax-only code modifier.
- Proposed mechanism: goal-driven but process-oriented evaluation; solver validates the consequences of the generated model. A code modifier repairs syntax/format without seeing the original problem so modeling logic is intended to remain unchanged.
- Decision layer: **Optimizer/model formulation generation and evaluation**, not heuristic/operator selection.
- State / Context: natural-language problem plus few-shot examples; code modifier receives generated code and execution error only.
- Action / Decision: generate Python ODE program or `.lp` optimization model; code modifier outputs syntax-corrected artifact.
- Feedback / Reward: solver execution result and exact/tolerance-based answer matching; compile/execution errors feed the syntax modifier.
- Dynamic mechanism: iterative syntax repair only; no online dynamic optimization/search control.
- LLM role: mathematical model/code generator; optional syntax modifier; GPT-4 also used in benchmark synthesis/quality checking.
- RL role: NOT PRESENT.
- Claimed contribution: solver-based automatic modeling evaluation framework and Mamo benchmark of 1,209 curated questions.
- Explicit limitation: required code/.lp formalization can confound conceptual modeling with formalization ability; future benchmarks should better distinguish these.
- 与当前 FJSP-AGV 研究关系: provides strong evaluation-design evidence for separating **valid LLM output** from **downstream optimization consequence**. For the current selector, syntactically valid strategy selection must not be treated as successful selection; actual decoded/search/Pareto effect must be measured. It does not implement AOS, competence learning, Pareto state or dynamic FJSP-AGV control.

## B｜Experimental Design Coding
- Dataset / Benchmark: Mamo.
- Instance scale: **1,209 total** = 346 ODE + 652 Easy LP + 211 Complex LP. ODE breakdown 196 first-order, 110 second-order, 40 systems.
- Baselines / evaluated models: proprietary GPT-4 family, Claude family, Gemini family, o1-preview; open DeepSeek, Llama-3.1, Qwen-2.5, Mixtral; raw/self-modified/GPT-4-modified conditions.
- Baseline 数量: Table 4 evaluates **20 model rows** across proprietary/open-source families; applicable modification comparisons vary by analysis.
- Independent runs: NOT REPORTED as repeated stochastic runs.
- Random seeds: NOT REPORTED.
- Population size: NOT APPLICABLE.
- Generations: NOT APPLICABLE.
- Evaluation budget: full benchmark evaluation; few-shot sensitivity 0/1/3/5/10 shots for ODE on 11 models and 0/1/3/5 for optimization on 10 models.
- Fitness / function evaluations: NOT APPLICABLE.
- Real decoding count: one generated artifact per benchmark item/condition is implied by protocol; aggregate decoding total NOT REPORTED.
- Solver calls: solver execution per generated model; aggregate total NOT REPORTED.
- LLM calls: code modifier can be iterative in diagnostic study; GPT-4 modifier diagnostic reports average **1.68 passes** to fix format errors, but experiments use **one modifier pass** for efficiency/accuracy balance.
- Token budget: locally deployed models max_length **4096 tokens**.
- Runtime / wall-clock: NOT REPORTED.
- Hardware: locally deployed models use vLLM on **8×A100** Slurm cluster; others via API.
- Metrics: modeling accuracy/correct rate; execution success/format-correct rate; weighted overall score; Cohen’s Kappa and reviewer accuracy for data review.
- Statistical tests: NOT REPORTED for model comparisons.
- Confidence interval: NOT REPORTED.
- Ablation: raw vs self-modified vs GPT-4-modified; not a conventional component ablation of a solver algorithm.
- Sensitivity analysis: model scale; few-shot count; answer tolerance threshold ξ; modifier pass count diagnostic.
- Generalization / OOD: multiple modeling categories and real-world scenario categories; no explicit unseen-distribution OOD protocol.
- Robustness: cross-review of 50 ODE questions by four independent reviewers; pairwise Cohen’s Kappa average 0.60, range 0.50–0.71.
- Dynamic-event design: NOT PRESENT.
- LLM API / inference cost: reviewer compensation ~US$473 reported; LLM API/inference monetary cost NOT REPORTED.

## C｜Writing Evidence Coding
### Introduction
Actual sequence: **M1 LLM mathematical reasoning importance → M2 natural vs mathematical language/modeling → M3 LLM+solver/OptiMUS → M4 evaluation difficulty → M6 solver-based evaluation + Mamo → M7 two bullet contributions**.
- Limitation/evaluation challenge appears before method in the second substantive paragraph.
- Method appears in the next paragraph.
- Contributions: **2 bullets**, benchmark/evaluation oriented.
- Empirical diagnosis before method: NO.

### Related Work
- Standalone Section 5, unusually placed **after experiments**.
- Organized into mathematical benchmark/data work and LLM+solver/problem-solving approaches.
- Method-family organization, not chronology.

### Gap language
- Main rhetorical device is not literature-count scarcity but **evaluation inadequacy**: direct/manual comparison cannot capture equivalent mathematical formulations.
- `To address this` directly links evaluation limitation to solver-based framework.
- The paper repeatedly distinguishes modeling errors from coding/format errors, turning construct validity into the central gap.

### Contributions
- Count: **2**, bulleted.
- Evaluation-framework contribution.
- Benchmark/data contribution.
- No standalone algorithmic optimization contribution.

### Experimental writing
- Protocol explicitly explains the causal chain `NL → model/code → solver → answer comparison` before results.
- Fairness/construct validity is unusually explicit: code modifier is denied problem information and is instructed not to alter logic, so syntax correction should not repair modeling mistakes.
- Results use labeled `Take-away 1...5` after empirical subsections, compressing findings into reusable claims.
- Reports negative/nuanced findings: complex modeling remains difficult; o1 can underperform on easy LP; scaling can plateau; format repair changes executability more than ranking.
- Appendix carries substantial reproducibility evidence: data review, modifier passes, metric threshold sensitivity, error taxonomy, few-shot sensitivity, settings, prompts and evaluation script.
- Missing: repeated stochastic runs, seeds, inferential significance tests, runtime and API cost.

## Asset Metadata

- FULL TEXT READ: YES
- Source: `LLM/64_LLM-Math-Modeling.md`
- Decision Layer: Modeling evaluation
- Current-study Relation: 支持执行验证
- Innovation Boundary: 当前不构成候选 selector 机制的直接新颖性反证；已实现范围为 Modeling evaluation，主要用于支持执行验证。
- Best Writing Claim: 用 solver-based process evaluation 测数学建模正确性，强调过程验证。
