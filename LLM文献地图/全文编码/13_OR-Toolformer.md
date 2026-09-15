# 13 OR-Toolformer｜全文编码

## Audit
- Source: `LLM/13_OR-Toolformer.md`
- Full text read to EOF: YES
- Title/Abstract, Introduction, Methodology, Experiments, Related Work, Conclusion, Limitations, prompt appendices/data availability: READ where present.
- Dedicated mathematical formulation section: NOT PRESENT beyond fine-tuning objective/formal notation.
- Ablation: NOT PRESENT.

## A. Research Content
- Research problem: automate OR problem modeling and solving with a small open-source LLM while reducing closed-API privacy dependence and avoiding training-from-scratch cost.
- Problem setting: natural-language OR tasks across LP/IP/MILP/TSP/max-flow and unseen assignment/min-cost-flow types.
- Objectives: generate structured solver parameters/API calls and achieve accurate, generalizable solver-grounded OR solutions.
- Algorithm backbone: semi-automatic synthetic instruction-data generation + LoRA fine-tuning of Llama-3.1-8B-Instruct + external OR solver tool execution.
- Proposed mechanism: sample validated OR parameters → Gemini synthesizes problem/CoT/API answer → execute and filter by solver agreement → instruction tune → model emits API calls → NEOS/Google OR services solve.
- Decision layer: optimizer/modeling tool-use generation; not scheduling/operator selection.
- State/context: natural-language problem, system tool list with distractors, learned solver API descriptions/structured parameters.
- Action/decision: generate chain-of-thought and solver API invocation.
- Feedback/reward: data-generation filtering compares generated-call result with parameter-grounded solver result; evaluation uses execution accuracy.
- Dynamic mechanism: NOT PRESENT.
- LLM role: data synthesizer (Gemini) and fine-tuned tool-using OR model.
- RL role: NOT PRESENT.
- Claimed contribution: solver-tool-augmented fine-tuning for small open-source OR LLM, benchmark accuracy and zero-shot task-type generalization.
- Explicit limitation: weak complex/industrial accuracy; only one open-source model fine-tuned/evaluated; synthetic prompts/domain contexts limited; no user-centered evaluation.
- Relation to FJSP-AGV: boundary evidence for solver-grounded LLM tool use and privacy/efficiency; not a direct adaptive-search or scheduling-control competitor.

## B. Experimental Design
- Dataset / Benchmark: NL4OPT, MAMO-EasyLP, MAMO-ComplexLP, IndustryOR; synthetic TSP/MF/AP/MCF test set.
- Instance scale: training 17,508 total: LP 3502, IP 3501, MILP 3493, TSP 3516, MF 3496. Test 175: TSP 50, MF 50, AP 50, MCF 25.
- Baselines: GPT-3.5, GPT-4, Gemini-2.0 Flash, DeepSeek-R1-685B; DeepSeek-LLM-7B-Chat, Llama-3.1-8B-Instruct, Mistral-7B-Instruct-v0.3, Qwen-2.5-7B-Instruct; DeepSeek-Math-7B-Instruct/RL, Qwen-2.5-Math-7B, JiuZhang-3.0-7B/8B. Unseen-type table compares Qwen-2.5-7B-Instruct.
- Baseline count: 13 named baseline model rows in main benchmark table; zero-shot test table uses 1 baseline.
- Independent runs: NOT REPORTED.
- Random seeds: NOT REPORTED.
- Population size: NOT APPLICABLE.
- Generations: NOT APPLICABLE; training epoch count NOT REPORTED in visible text.
- Evaluation budget: benchmark-defined test sets + 175 synthetic test instances; no optimizer FE budget.
- Fitness/function evaluations: NOT APPLICABLE.
- Real decoding count: NOT REPORTED.
- Solver calls: used in synthesis filtering and evaluation; total count NOT REPORTED.
- LLM calls: NOT REPORTED.
- Token budget: output-token efficiency reported; average output 449 tokens for OR-Toolformer, 500 Qwen-2.5-7B-Instruct, 1422 Qwen-2.5-Math-7B.
- Runtime / wall-clock: NOT REPORTED.
- Hardware: single GPU, 10 GB VRAM; exact GPU model NOT REPORTED.
- Metrics: execution accuracy; zero-shot accuracy; average output token length.
- Statistical tests: NOT REPORTED.
- Confidence interval: NOT REPORTED.
- Ablation: NOT PRESENT.
- Sensitivity analysis: NOT PRESENT.
- Generalization / OOD: unseen AP and MCF task types; familiar TSP/MF consistency test.
- Robustness: task/expression diversity built into synthesis; no dedicated robustness experiment beyond generalization.
- Dynamic-event design: NOT PRESENT.
- LLM API / inference cost: NOT REPORTED.

## C. Writing Evidence
### Introduction
- Sequence: M1 OR workflow/importance → M3 LLM potential → M4 privacy and compute limitations → M3 tool-learning/fine-tuning opportunity → M6 OR-Toolformer.
- Formal numbered contribution list: NOT PRESENT.
- Method appears after limitations/opportunity framing.

### Related Work
- Placed after experiments, not before method.
- Organized by method family: tool learning first, LLMs for OR second.
- Contrasts calculator/general tool use with solver learning and direct/agentic OR approaches.

### Gap language
- Functions: privacy constraint, compute barrier, arithmetic weakness, scarcity of solver-API training data.
- Uses contrastive `However` and problem→alternative→method transition rather than aggressive first/unexplored claims.

### Contributions
- Distributed through Abstract/Introduction/Conclusion rather than numbered bullets: synthesis pipeline, tool-augmented fine-tuning, benchmark/generalization evidence.

### Experimental writing
- Setup sequence: Data generation → Training → Evaluation/baselines.
- Results sequence: standard benchmarks → unseen synthetic test → token efficiency.
- Fairness: emphasizes size-matched baselines; separates large general-purpose models from 7–8B comparisons and excludes first group from ranking.
- Statistical significance writing: NOT PRESENT.
- Ablation writing: NOT PRESENT.
- Cost writing: output-token efficiency reported, monetary/API cost absent.

### Novelty strength
- Moderate. Uses `We introduce` and efficacy/generalization claims, without a `first` claim in the read text.

## Asset Metadata

- FULL TEXT READ: YES
- Source: `LLM/13_OR-Toolformer.md`
- Decision Layer: Tool-use / solver calling
- Current-study Relation: 说明 LLM 与 solver 分工
- Innovation Boundary: 当前不构成候选 selector 机制的直接新颖性反证；已实现范围为 Tool-use / solver calling，主要用于说明 LLM 与 solver 分工。
- Best Writing Claim: 让 LLM 学会调用 OR solver/API，代表工具增强而不是让 LLM 独自算到底。
