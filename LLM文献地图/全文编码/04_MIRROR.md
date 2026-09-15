# 04｜MIRROR: A Multi-Agent Framework with Iterative Adaptive Revision and Hierarchical Retrieval for Optimization Modeling in Operations Research

- Source: `LLM/04_MIRROR.md`
- Corpus: LLM / automated OR modeling
- Full-text audit: **YES**
- EOF verification: full text covered through page 17/17 and references.

## A. Research Content

|Field|Coding|
|---|---|
|Research problem|Automatically translate natural-language OR problems into mathematical models and executable solver code without task-specific fine-tuning.|
|Problem setting|General OR optimization modeling across simple and complex benchmarks.|
|Objectives|Correct end-to-end optimization modeling/solving; pass@1 accuracy; reliability and token efficiency.|
|Algorithm backbone|Multi-agent pipeline: parameter extraction → modeling advisor → mathematical modeling → code generation → execution/revision.|
|Proposed mechanism|MIRROR combines HRAG hierarchical exemplar retrieval, IAR execution-driven iterative adaptive revision, local task-specific memories and global memory.|
|State/context|Original problem, extracted parameters, advisor output, retrieved exemplars, model/code history, executor error messages and revision tips.|
|Action/decision|Generate/revise mathematical model and solver code; retrieve exemplars; switch modeling/code agents into revision roles after failure.|
|Feedback/reward|External solver execution returns numerical solution or failure/error; ground truth is used during exemplar-library construction.|
|Dynamic mechanism|Iterative feedback-driven revision after execution failure; not dynamic scheduling.|
|Claimed contribution|Training-free end-to-end multi-agent OR modeling; IAR; HRAG; strong benchmark performance including complex industrial sets and small-model transfer.|
|Explicit limitation|No dedicated Limitations section observed. Introduction/Related Work identifies prior limitations; Conclusion does not state a separate self-limitation.|

## B. Experimental Design

|Field|Coding|
|---|---|
|Datasets|NL4Opt; Mamo-EasyLP; Mamo-ComplexLP; IndustryOR; ComplexOR.|
|Test split detail|Last 163 Mamo-EasyLP instances reserved as exemplar-library source; remaining 489 used as test set. Exemplar library built from 1,127 raw problems, 652 verified pairs retained before annotation/filtering, final library 602.|
|Baselines|Traditional CoT prompting on backbone, DeepSeek-v3, glm-5.1, qwen3-30B; learning-based MiniOpt, LLMOPT, OptMATH, ORLM, SIRL; agent-based OptiMUS, ORMind, OptiTree, Chain-of-Experts.|
|Fairness control|Agent-based methods implemented with same backbone model; temperature=0 for deterministic/reproducible output.|
|Backbone|qwen-plus-2025-09-11; additional small-model validation qwen3-30b-a3b-instruct-2507.|
|Solver|Gurobi.|
|Metric|pass@1 accuracy with relative-error tolerance; macro average/rank; token consumption; ablation additionally reports wrong-answer and compile-error rates.|
|Repeated runs|NOT REPORTED as an independent repeated-run protocol.|
|Seeds|NOT REPORTED.|
|Statistical tests|NOT REPORTED.|
|Ablation|Full; w/o IAR; w/o HRAG; w/o both across five datasets. Fine-grained agent ablation removes Parameter Extraction, Modeling Advisor, or Mathematical Modeling agent on IndustryOR and ComplexOR.|
|Sensitivity|No conventional hyperparameter sensitivity study reported.|
|Generalization|Cross-benchmark evaluation; complex industrial benchmarks; transfer to smaller open-source model without fine-tuning.|
|Runtime|NOT REPORTED as wall-clock comparison.|
|Hardware|NOT REPORTED in the inspected full text.|
|LLM token/cost|Total token consumption reported for agent-based methods on IndustryOR and ComplexOR; monetary API cost NOT REPORTED.|

## C. Writing Evidence

### Introduction rhetorical moves

Observed sequence:
`M1 OR importance/application → M2 practical modeling bottleneck → M3 LLM capability → M3 existing learning-based and agent-based routes → M4 two explicit route limitations → M6 proposed MIRROR → M7 three bullet contributions → headline empirical result`

Contributions: **3 bullet points**, corresponding to framework, IAR mechanism, HRAG mechanism.

### Related Work organization

Explicit taxonomy:
1. LLMs for Math and Code Generation;
2. Learning-based LLM Optimization Modeling;
3. Agent-based LLM Optimization Modeling;
4. Summary and Gaps.

The section ends with a dedicated synthesis paragraph rather than merely listing papers.

### Gap formulation

Gap is written at two levels:
- learning-based models: annotated-data cost, black-box diagnosis/adaptation difficulty;
- agent frameworks: hallucination/lack of external domain knowledge and weak use of solver feedback for correction.

Transition is explicit: “To bridge these gaps, we propose MIRROR…”

### Experimental section organization

`Experimental Setup → Results Analysis → Ablation Study`.
Setup is internally organized as Benchmarks, Baselines, Implementation Details, Evaluation Metric. Results are organized by comparison purpose: overall, agent baselines, token efficiency, learning-based methods, prompting, small-model transfer.

### Comparative-result reporting

Typical rhetorical functions in this paper:
1. state overall rank/accuracy;
2. identify strongest comparator within a method family;
3. quantify absolute percentage-point gains on named datasets;
4. discuss resource/token trade-off separately from accuracy;
5. connect improvement to the proposed mechanisms.

### Ablation-result reporting

Two levels:
- component ablation tests IAR × HRAG using full / remove one / remove both, effectively exposing complementary contribution;
- agent ablation removes one generation-stage agent at a time.
Results are decomposed into accuracy, wrong-answer rate and compile-error rate to connect performance loss to failure mode.

### Academic hedging / novelty strength

Uses assertive performance language (“highest rank”, “state of the art among multi-agent approaches”, “outperforms”), but the gap is framed as concrete deficiencies of named method families rather than broad “no work exists” claims. No corpus-level inference is drawn here.

## D. Relevance Tier

**Tier B: Supporting.** Relevant for execution-feedback loops, hierarchical retrieval/memory, ablation structure and cost reporting, but the decision object is OR model/code generation rather than scheduling search/operator control.

## E. Audit

- Intro: READ
- Related Work: READ
- Formulation/problem framing: READ
- Method: READ, including HRAG, IAR, dual memory and examples
- Experimental Setup: READ
- Results: READ
- Ablation: READ
- Discussion/Limitations: NOT PRESENT as dedicated self-limitations section
- Conclusion: READ
- Appendix: NOT PRESENT as a separate appendix in this Markdown; supplementary analyses are in main text
- EOF: READ through page 17/17 and references

## Asset Metadata

- FULL TEXT READ: YES
- Source: `LLM/04_MIRROR.md`
- Decision Layer: Modeling / feedback
- Current-study Relation: 支持反馈闭环原则
- Innovation Boundary: 当前不构成候选 selector 机制的直接新颖性反证；已实现范围为 Modeling / feedback，主要用于支持反馈闭环原则。
- Best Writing Claim: 用多 Agent、局部/全局 memory 与执行反馈迭代修正 OR 建模，是闭环建模而非直接求解代表。
