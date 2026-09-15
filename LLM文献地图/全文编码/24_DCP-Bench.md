# 24｜DCP-Bench-Open 全文编码

- Source: `LLM/24_DCP-Bench.md`
- Full-text status: **YES**
- Last read position: **EOF (line >1000 empty); Appendices A–E and prompt listings covered**
- Corpus: LLM / OR modelling benchmark
- Tier: C（Boundary / Benchmark evidence）

## A｜Research Content
- Research problem: 评估 LLM 将自然语言 discrete combinatorial problem 转换为可执行 constraint model 的能力，并解决既有 benchmark 小、同质、domain-specific、缺乏 multi-instance robustness evaluation 的问题。
- Problem setting: CP/CSP/COP natural-language-to-model；164 problems，三种 modelling frameworks（CPMpy, MiniZinc, OR-Tools CP-SAT）。
- Objectives: benchmark construction；framework/interface effect；prompt/inference-time compute effect；error taxonomy；multi-instance generalization/robustness。
- Algorithm backbone: LLM model generation + external constraint solver execution/evaluation；test-time methods RAICL, reasoning, repeated sampling/solution majority voting, iterative self-verification。
- Proposed mechanism: benchmark-level solution validation plus multiple inference-time generation/refinement strategies；not heuristic optimization.
- Decision layer: **Optimizer/model formulation generation**，不是 scheduling/heuristic/operator selection。
- State / Context: natural-language problem description + optional default instance + system prompt/docs/examples + previous generated model/execution output for self-verification。
- Action / Decision: generate executable CP model code；during self-verification revise model；during repeated sampling select model by solution majority voting。
- Feedback / Reward: solver execution outcome, solution feasibility/optimality, runtime/error traceback, structured-output correctness。
- Dynamic mechanism: iterative inference-time self-verification；NOT dynamic optimization environment。
- LLM role: formal model/code generator and self-verifier/debugger。
- RL role: **NOT PRESENT** in proposed method。
- Claimed contribution: DCP-Bench-Open 164-problem benchmark; systematic 3-framework/LLM evaluation; inference-time compute adaptations up to ~91% SIA; multi-instance strict robustness evaluation。
- Explicit limitation: benchmark problems diverse/realistic but often textbook-derived; industrial problems with larger data/more constraints/objectives/long descriptions rarely public；future multi-turn modelling, more frameworks/solvers, SFT, multi-instance-aware prompting, efficiency/model selection。
- 与当前 FJSP-AGV 研究关系: 非直接竞争，但实验设计价值高。它说明 LLM optimization work可以用 **hidden instances + strict multi-instance correctness** 检查“对一个实例有效但并未学到抽象机制”的问题。对当前研究可对应为 unseen dynamic scenarios/instances 的泛化审计，但不能把该做法冒充 scheduling 文献惯例。

## B｜Experimental Design Coding
- Dataset / Benchmark: DCP-Bench-Open v0.1.0, 164 problems；sources CSPLib 39, CPMpy examples 16, Håkan K. 80, Course 18, ComplexOR 11；23 problems have multiple instances, total 167 instances for multi-instance evaluation。
- Instance scale: constraints 1–2463, decision variables 2–716, 349 unique constraint relations；54 optimization problems。
- Baselines: comparisons are LLMs/frameworks/prompt/test-time configurations rather than algorithm baselines. 7 LLMs in core setup；3 frameworks；3 prompt levels；Q3 six inference-time configurations。
- Baseline 数量: conventional optimization baseline **NOT APPLICABLE**。
- Independent runs: API generation primarily deterministic seed/temp settings; repeated sampling explicitly k=10. Generic repeated independent experimental runs **NOT REPORTED**。
- Random seeds: **42 for all API calls**。
- Population size: NOT APPLICABLE。
- Generations: NOT APPLICABLE。
- Evaluation budget: output max 12k tokens；generated model execution timeout 10 s normally；final multi-instance ITC experiment 30 min；sampling k=10；self-verification max 10 iterations；RAICL e=8 examples。
- Fitness / function evaluations: NOT APPLICABLE。
- Real decoding count: repeated sampling = 10 generated candidate models/configuration; exact total corpus decoding count NOT REPORTED。
- Solver calls: generated models executed for evaluation; exact aggregate solver-call count NOT REPORTED。
- LLM calls: per method implied by sampling/self-verification loops but aggregate count NOT REPORTED。
- Token budget: max output 12k per answer; aggregate token budget NOT REPORTED。
- Runtime / wall-clock: solver timeout 10 s, final experiment 30 min; total wall-clock NOT REPORTED。
- Hardware: Ubuntu 24.04.3, 32GB RAM, Intel Core Ultra 7 165Hx22 processor。
- Metrics: Single Instance Accuracy (SIA), Multiple Instance Accuracy (MIA), Averaged Instance Accuracy (AIA), detectable-error counts, modelling-error counts。
- Statistical tests: **NOT REPORTED**。
- Confidence interval: **NOT REPORTED**。
- Ablation: prompt Level1/2/3; baseline vs RAICL/reasoning/sampling/self-verification/sampling+self-verification; error analysis; not called classical ablation but controlled configuration comparisons。
- Sensitivity analysis: sampling fixed k=10 and SV max=10; parameter sweep **NOT PRESENT**。
- Generalization / OOD: **YES**, hidden data instances for same problem type; 23-problem/167-instance strict evaluation。
- Robustness: SIA vs AIA vs MIA explicitly designed to expose default-instance overfitting。
- Dynamic-event design: NOT PRESENT。
- LLM API / inference cost: providers named; monetary cost **NOT REPORTED**。
- Frameworks: MiniZinc, CPMpy, OR-Tools CP-SAT。
- Models: gpt-5.1-2025-11-13, gpt-oss-120B, DeepSeek-V3.2, Qwen3-Coder-480B-A35B, Qwen3 235B A22B Instruct, Kimi K2 Instruct, Cogito v2.1 671B。

## C｜Writing Evidence Coding
### Introduction
Actual sequence: **M1 DCP importance/solver landscape → M2 formal modelling bottleneck → M3 prior constraint acquisition + LLM modelling → M4 declarative modelling-specific challenges → M3 recent LLM formalization work → M4 complex/diverse scaling problem → explicit 3-part limitations/gap → M6 benchmark + systematic frameworks + inference-time methods → M7 3 contributions → publication-history delta**。
- Limitation first appears: paragraph 2 as modelling bottleneck; sharper LLM-specific challenges after central question。
- Method appears: after explicit `(a)(b)(c)` limitations, `To address... developed DCP-Bench-Open`。
- Contributions: **3 bullet contributions**。
- Empirical diagnosis before method: NO new experiment in Introduction; benchmark comparison rationale uses prior evidence.

### Related Work
- Dedicated Section 7 placed **after experiments**, not before method。
- Organization: three method-family themes: Inference-Time Compute and Scaling → LLMs for Formal Modelling and Optimization → Existing Formal Modelling Benchmarks。
- chronological: secondary within families。
- taxonomy/method family: YES。
- traditional→learning→LLM: NO as main axis。
- direct solving vs solver-assisted: neuro-symbolic/formal representations discussed, but not formal taxonomy。
- generation vs selection: NO。
- static vs adaptive: parallel vs sequential inference-time scaling is explicit, but not heuristic adaptation taxonomy。
- offline vs online: NO as main axis。

### Gap language
- Contrast: `However, while...`; `Nevertheless`; `Although promising...`; `while existing repositories... are not suitable...`。
- Limitation: explicit paragraph `Existing limitations can be summarized as follows (a)...(b)...(c)...`。
- Challenge: declarative-vs-imperative differences, viewpoint selection, verification difficulty。
- Motivation: `To address the lack...`; `With inference-time computation... we adapt and evaluate...`。
- Novelty strength: `novel benchmark`; Related Work uses `To the best of our knowledge` narrowly for CP benchmark state rather than claiming entire LLM modelling field unexplored。

### Contributions
- Count: **3**；bulleted: YES。
- Benchmark contribution: YES, central。
- Experimental contribution: YES, systematic 3-framework + LLM comparison。
- Method contribution: adaptation of prompt/inference-time methods, not a new optimizer。
- Formulation contribution: benchmark evaluation formalization SIA/MIA/AIA, but not listed separately as a contribution bullet。
- Empirical findings: interface accuracy and ITC gains embedded in contribution bullets。

### Experimental writing
- Experiments are organized by **five explicit research questions Q1–Q5** before setup/results。
- Setup reports model selection rationale, API providers, seed=42, temperatures, token cap, execution timeout and hardware。
- Comparative results use question-by-question narrative, not one omnibus table。
- Failure analysis separates detectable errors from semantic modelling errors, preventing executable-code success from being conflated with correctness。
- Generalization has its own Q4 using hidden instances and strict SIA/AIA/MIA definitions before experiments。
- Final Q5 integrates best prior findings into a stronger combined configuration, a staged experimental narrative rather than indiscriminate grid search。
- Statistical significance: NOT REPORTED despite prose occasionally saying `significantly`; no named test found。
- Computational cost: operational budgets/timeouts reported, monetary API cost absent。

## Asset Metadata

- FULL TEXT READ: YES
- Source: `LLM/24_DCP-Bench.md`
- Decision Layer: Evaluation
- Current-study Relation: 支持 benchmark/正确性设计
- Innovation Boundary: 当前不构成候选 selector 机制的直接新颖性反证；已实现范围为 Evaluation，主要用于支持 benchmark/正确性设计。
- Best Writing Claim: 强调约束建模 benchmark 与严格评估，把 LLM+optimization 从 demo 推向可审查比较。
