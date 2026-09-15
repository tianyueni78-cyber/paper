# 33｜OR-LLM-Agent 全文编码

- Source: `LLM/33_OR-LLM-Agent.md`
- Full-text status: **YES**
- Last read position: **EOF (line >400 empty); no appendix present**
- Corpus: LLM / OR modeling agents
- Tier: B（Supporting）

## A｜Research Content
- Research problem: automate natural-language OR modeling, solver-code generation and debugging; examine whether reasoning LLMs and task decomposition improve OR solving and whether existing benchmarks discriminate model capability.
- Problem setting: NL OR problem → mathematical model → Python solver code → execution/debugging → numeric answer.
- Objectives: improve accuracy/executability without fine-tuning or complex prompt engineering; construct a more discriminative OR benchmark BWOR.
- Algorithm backbone: three-stage multi-agent pipeline: Math Agent → Code Agent → Debugging Agent; maximum five execution/repair attempts.
- Proposed mechanism: dedicated reasoning LLM sub-agents separate modeling and code generation; execution errors trigger code self-repair for early failures, fourth failure triggers mathematical-model repair; fifth failure terminates.
- Decision layer: **Optimizer/model formulation generation + solver-code generation + runtime debugging control**. Not heuristic/operator selection.
- State / Context: natural-language task, generated mathematical model, current code, execution status/solution/error message, failed-attempt count.
- Action / Decision: generate model; generate Gurobi code; execute; repair code; escalate to model repair; terminate on success/fifth failure.
- Feedback / Reward: solver execution result/error messages; no scalar learned reward.
- Dynamic mechanism: conditional runtime repair/escalation based on execution feedback and attempt count; no external scheduling dynamics.
- LLM role: reasoning sub-agents for modeling, coding and repair.
- RL role: NOT PRESENT.
- Claimed contribution: reasoning-LLM OR agent without retraining; three-subtask decomposition; BWOR benchmark; multi-model/five-dataset evaluation.
- Explicit limitation: no standalone Limitations section. Service interruption prevents some DeepSeek-R1 results; authors find existing benchmarks can produce counterintuitive reasoning-vs-nonreasoning rankings and therefore exclude four datasets from core comparison after diagnosis. Other general limitations NOT REPORTED.
- 与当前 FJSP-AGV 研究关系: indirect but useful control-architecture evidence. It demonstrates conditional escalation based on repeated execution failure and explicit separation of reasoning roles. Thus a hierarchical `select → execute → diagnose → escalate/redesign` loop is not unique by itself. Current work needs scheduling/operator-specific competence semantics and causal evaluation rather than merely multiple LLM roles or fallback escalation.

## B｜Experimental Design Coding
- Dataset / Benchmark: NL4OPT, MAMO EasyLP, MAMO ComplexLP, IndustryOR, BWOR.
- Instance scale: NL4OPT 289; EasyLP 652; ComplexLP 211; IndustryOR 100; BWOR 82.
- Baselines: SOTA tag-BART, Chain-of-Experts, OptiMUS, ORLM; reasoning GPT-o3/GPT-o4-mini/Gemini2.5Pro/DeepSeek-R1; non-reasoning GPT-4o/Gemini2.0Flash/DeepSeek-V3; open-source LLAMA3-8B Base/Instruct and DeepSeek-R1-Distill-32B.
- Baseline 数量: named external comparison entries = **15** if counting 4 SOTA + 4 reasoning + 3 non-reasoning + 4 open-source entries including ORLM-LLAMA3-8B as SOTA; table grouping overlaps taxonomy, so no single family count should be inferred beyond explicit names.
- Independent runs: NOT REPORTED.
- Random seeds: NOT REPORTED.
- Population size: NOT APPLICABLE.
- Generations: NOT APPLICABLE.
- Evaluation budget: Debugging Agent maximum **5 attempts/problem**; other inference budget NOT REPORTED.
- Fitness / function evaluations: NOT APPLICABLE.
- Real decoding count: up to initial model/code plus repair generations; aggregate NOT REPORTED.
- Solver calls: up to five execution attempts/problem in agent workflow; aggregate NOT REPORTED.
- LLM calls: aggregate NOT REPORTED.
- Token budget: NOT REPORTED.
- Runtime / wall-clock: NOT REPORTED.
- Hardware: NOT REPORTED.
- Metrics: solution accuracy (absolute error <0.1); code error rate; mathematical model accuracy among runnable code.
- Statistical tests: NOT REPORTED.
- Confidence interval: NOT REPORTED.
- Ablation: Direct Code Generation vs Math+Code vs Math+Code+Debugging on BWOR; incremental average accuracy gains 4.06% and 5.49% reported.
- Sensitivity analysis: NOT PRESENT.
- Generalization / OOD: five datasets and multiple LLM families; no formal OOD split.
- Robustness: error-rate analysis and cross-model/cross-dataset comparison; repeated-run stochastic robustness NOT REPORTED.
- Dynamic-event design: NOT PRESENT.
- LLM API / inference cost: NOT REPORTED.
- Missing-data handling: DeepSeek-R1 ComplexLP/EasyLP agent results unavailable due service interruption and explicitly marked.

## C｜Writing Evidence Coding
### Introduction
Actual sequence: **M1 OR importance/manual modeling barrier → M3 LLM/reasoning-model capability → M3 OR automation → M4 two explicit challenges (non-reasoning reliance; benchmark scope) → M6 OR-LLM-Agent + BWOR → M7 four bullet contributions**.
- Limitation appears after two capability/background paragraphs.
- Method immediately follows `To address these challenges...`.
- Contributions: **4**, bulleted.
- Empirical diagnosis before method: NO; benchmark anomaly is previewed in abstract/contribution and analyzed experimentally later.

### Related Work
- Organized by method family: code generation/debugging; LLM-based methods for OR.
- traditional→learning→LLM: NO.
- direct solving vs solver-assisted: OR agent/tool approaches discussed, but not a formal taxonomy.
- generation vs selection: NO.
- static vs adaptive: iterative debugging mentioned; not taxonomy.
- offline vs online: fine-tuning vs agent prompting is part of gap, not section organization.

### Gap language
- `However, existing research ... still faces several challenges` introduces a numbered two-part gap.
- `primarily rely on non-reasoning LLMs` narrows the target rather than claiming no prior OR agents.
- Related Work uses `However` and `Nevertheless` to connect complex prompting/fine-tuning compensation to underlying model limitation.
- Transition: `To address these challenges, we propose...`.
- Novelty wording uses `We propose` rather than `first`.

### Contributions
- Count: **4**; bullets: YES.
- Method: three-agent reasoning pipeline.
- Formulation: NO.
- Experimental: five datasets/multiple reasoning and nonreasoning LLMs; task-decomposition ablation/error analysis.
- Benchmark: YES, BWOR.
- Empirical finding: existing OR benchmarks can rank reasoning models counterintuitively; BWOR more discriminative according to their analysis.

### Experimental writing
- Experimental Setup separates benchmarks/metric and baseline taxonomy.
- A notable writing pattern is **benchmark validation before core method comparison**. Authors detect a counterintuitive dataset behavior, provide math/code benchmark comparison, then explicitly designate BWOR as primary and demote other datasets to supplementary evidence.
- Main comparison table marks copied results, reproduced results and unavailable service results with superscripts, improving provenance transparency.
- Ablation is directly aligned with architectural decomposition and reports incremental average gains.
- Error analysis decomposes failure into code executability vs mathematical-model correctness rather than reporting only final accuracy.
- No repeated-run statistics/significance/CI/runtime/cost reporting.

## Asset Metadata

- FULL TEXT READ: YES
- Source: `LLM/33_OR-LLM-Agent.md`
- Decision Layer: Agentic solving
- Current-study Relation: 背景
- Innovation Boundary: 当前不构成候选 selector 机制的直接新颖性反证；已实现范围为 Agentic solving，主要用于背景。
- Best Writing Claim: 用 Math/Code/Debugging agents 处理 OR，并以 BWOR benchmark 测试，是模块化 agentic OR 代表。
