# 76｜Towards an Automatic Optimisation Model Generator Assisted with Generative Pre-trained Transformer 全文编码

- Source: `LLM/76_Auto-Model-Generator.md`
- Full-text status: **YES**
- Last read position: **EOF (line >140 empty); no appendix present**
- Corpus: LLM / optimization modeling
- Tier: B/C

## A｜Research Content
- Research problem: automatically generate executable optimization models from user-specified features and repair compilation failures with GPT.
- Problem setting: prompt → GPT-generated MiniZinc model → compile/solve with Gecode → if build error, feed model + error message to edit model → repeat → return model/solution.
- Objectives: test feasibility of GPT-3.5 for automatic optimization-model generation and automatic error repair.
- Algorithm backbone: generator–solver–repair loop.
- Proposed mechanism: text-davinci-003 generates initial MiniZinc; MiniZinc/Gecode validates execution; compilation errors trigger text-davinci-edit-001 with explicit error feedback; loop terminates on valid solve or experiment step cap.
- Decision layer: **Optimizer/model formulation generation + code repair**.
- State / Context: user prompt/specification; generated MiniZinc source; compiler/solver error message during repair.
- Action / Decision: generate or edit MiniZinc code.
- Feedback / Reward: binary solver/build status and concrete error text; manual correctness inspection checks whether executable model actually matches requested specification.
- Dynamic mechanism: iterative error-triggered code repair, not dynamic scheduling/search control.
- LLM role: initial model generator and error-driven code editor.
- RL role: NOT PRESENT.
- Claimed contribution: proof-of-concept automatic optimization-model generator with solver-in-the-loop repair.
- Explicit limitation: only 10 simple test instances, MiniZinc/GPT-3.5 setup; valid execution does not guarantee requested semantics; all_different cases fail after 10 repair steps; future work should test other LLMs/languages and richer error messages.
- 与当前 FJSP-AGV 研究关系: indirect but important verification precedent. It explicitly separates **valid/executable** from **correct according to requested specification**. For current LLM selector, syntactically valid operator/strategy selection must likewise be separated from realized optimization effect. Solver/decoder feedback loops are not novel by themselves.

## B｜Experimental Design Coding
- Dataset / Benchmark: author-designed 10 MiniZinc generation instances; supporting data on Figshare.
- Instance scale: **10**: first 5 discrete variables, last 5 matrix/array discrete variables; vary open/defined domain and no/constraint/all_different conditions.
- Baselines: NOT PRESENT.
- Baseline 数量: 0.
- Independent runs: NOT REPORTED; each listed instance appears as one generation/repair trajectory.
- Random seeds: NOT REPORTED.
- Population size: NOT APPLICABLE.
- Generations: NOT APPLICABLE; repair loop capped/observed at up to **10 steps** in failed cases.
- Evaluation budget: 10 instances; repair steps per instance reported.
- Fitness/function evaluations: NOT APPLICABLE.
- Real decoding count: generation/edit step count reported per instance: 1, 2 or 10; aggregate decoding count can be derived but paper does not label it as such.
- Solver calls: at least one validation per generated/repaired model; exact aggregate NOT REPORTED explicitly.
- LLM calls: step count is reported per instance, but aggregate API call count NOT REPORTED explicitly.
- Token budget: generation `max_tokens=200`; Table 1 reports per-instance total token values: 170–1787.
- Runtime / wall-clock: NOT REPORTED.
- Hardware: NOT REPORTED.
- Models/tools: text-davinci-003 generation; text-davinci-edit-001 repair; MiniZinc 2.7.1; Gecode 6.3.0; MiniZinc Python runtime validation.
- Metrics: `Valid`, `Correct`, repair `Step`, `Token`; manual source inspection for semantic correctness.
- Statistical tests: NOT PRESENT.
- Confidence interval: NOT PRESENT.
- Ablation: NOT PRESENT.
- Sensitivity analysis: NOT PRESENT.
- Generalization / OOD: NOT PRESENT.
- Robustness: NOT PRESENT beyond variation of variable/domain/constraint specification.
- Dynamic-event design: NOT PRESENT.
- LLM API / inference cost: token use reported, monetary cost NOT REPORTED.

## C｜Writing Evidence Coding
### Introduction
Actual sequence: **M1 optimization-model importance → M4 modeling-language/expertise/time burden → M6 proposed GPT generator/repair approach → M3 GPT/code-repair capability → M6 restated goal/value**.
- Limitation appears immediately in first paragraph.
- Proposed method also appears in first paragraph, before any substantial literature review.
- Explicit contribution list: NOT PRESENT.
- Empirical diagnosis before method: NO.

### Related Work
- Standalone Related Work section: **NOT PRESENT**.
- Prior work is minimal and embedded in Introduction, mainly NLP/code generation and GPT bug fixing.

### Gap language
- Main function is practical bottleneck → automation motivation.
- Does not build a sophisticated scarcity-based research gap; instead argues that model creation is time-consuming and expertise-heavy, then proposes a generator/repair loop.

### Contributions
- No numbered contribution list.
- method/proof-of-concept contribution: generator–solver–repair framework.
- empirical feasibility contribution: 10 MiniZinc instances with validity/correctness/step/token reporting.

### Experimental writing
- Experimental protocol is compact and reproducible at API-parameter level: exact GPT models, temperature, max tokens, MiniZinc/Gecode versions and 10-instance design are given.
- Particularly strong evaluation distinction: `Valid` means executable, `Correct` means matches prompt specification, verified manually.
- Failure cases are reported directly rather than hidden: all_different omissions survive 10 repair steps; several array models execute but violate requested specification.
- Weaknesses: no baseline, repeated runs, seeds, statistical inference, CI, runtime/hardware, robustness/generalization or conventional ablation.
