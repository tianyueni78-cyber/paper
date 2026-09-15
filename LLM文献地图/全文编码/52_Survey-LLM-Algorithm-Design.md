# 52｜A Systematic Survey on Large Language Models for Algorithm Design 全文编码

- Source: `LLM/52_Survey-LLM-Algorithm-Design.md`
- Full-text status: **YES**
- Last read position: **EOF (line >1250 empty); no appendix present**
- Corpus: LLM / automated algorithm design systematic survey
- Tier: A（taxonomy/evolution/gap-boundary evidence）

## A｜Research Content
- Research problem: fragmented LLM-assisted algorithm-design literature lacks a systematic end-to-end taxonomy spanning ideation, implementation, evaluation and algorithm types.
- Problem setting: LLM4AD broadly defined as substantive LLM contribution to conception, synthesis or refinement of algorithms; excludes mere general-purpose code translation.
- Objectives: define scope; systematically collect/screen literature; classify LLM roles; map algorithm-design stages/applications; synthesize challenges/future directions.
- Algorithm backbone: NOT APPLICABLE; systematic survey.
- Proposed mechanism/taxonomy: four LLM roles: **LLM as Optimizer (LLMaO), Predictor (LLMaP), Extractor (LLMaE), Designer (LLMaD)**; three design stages: **ideation, implementation, evaluation**.
- Decision layer: literature spans solution generation, hyperparameter/strategy adjustment, performance prediction, feature extraction, operator/component/complete algorithm generation and evaluation; no single controller.
- State / Context: NOT APPLICABLE as one method. Survey explicitly notes LLMaO can condition on problem description, constraints, evaluated solutions and history/trajectories.
- Action / Decision: NOT APPLICABLE as one method.
- Feedback / Reward: survey identifies execution/performance feedback, historical results, reflection, benchmarks, surrogate prediction and RL/fine-tuning across prior works.
- Dynamic mechanism: survey documents real-time hyperparameter recommendation/adaptation, reflection, closed-loop code refinement, online RL updating, dynamic test-instance evolution and co-evolution.
- LLM role: optimizer/predictor/extractor/designer.
- RL role: appears in reviewed methods for value guidance, reward design and online algorithm-discovery fine-tuning; not the survey’s own method.
- Claimed contribution: systematic definition/scope; 180+ paper corpus; four-role taxonomy; three-stage pipeline; cross-domain application synthesis; challenges in scalability/generalization/interpretability/efficiency/benchmarking.
- Explicit limitation: authors state corpus cannot guarantee exhaustive coverage due field/domain scale; aim is representative systematic landscape.
- 与当前 FJSP-AGV 研究关系: highly important boundary evidence. The survey explicitly documents **history-conditioned optimization, adaptive hyperparameters, reflective search, online model updating, instance-specific heuristic generation/selection, complementary heuristic sets, multiobjective heuristic design, and dynamic evaluation/test generation**. Hence broad claims around contextual adaptation, portfolio, online adaptation or multiobjective LLM design are untenable. The remaining candidate must be formulated at the precise mechanism level and verified against cited 2025 works, especially instance-specific generation/selection and online algorithm discovery.

## B｜Experimental Design Coding
- Dataset / Benchmark: systematic literature corpus, not optimization benchmark.
- Instance scale: Stage I ~3000 deduplicated search hits; title/abstract screen ~500; full-text screen ~150; snowballing/manual cross-check final **over 180 papers**.
- Baselines: NOT APPLICABLE.
- Baseline 数量: NOT APPLICABLE.
- Independent runs: NOT APPLICABLE.
- Random seeds: NOT APPLICABLE.
- Population size: NOT APPLICABLE.
- Generations: NOT APPLICABLE.
- Evaluation budget: NOT APPLICABLE.
- Fitness / function evaluations: NOT APPLICABLE.
- Real decoding count: NOT APPLICABLE.
- Solver calls: NOT APPLICABLE.
- LLM calls: NOT APPLICABLE.
- Token budget: NOT APPLICABLE.
- Runtime / wall-clock: NOT REPORTED for review process.
- Hardware: NOT APPLICABLE.
- Metrics: publication trend; role distribution; qualitative/taxonomic synthesis. Figure reports role shares: LLMaD 59.7%, LLMaO 22.8%, LLMaP 10.7%, LLMaE 6.7%.
- Statistical tests: NOT PRESENT.
- Confidence interval: NOT PRESENT.
- Ablation: NOT PRESENT.
- Sensitivity analysis: NOT PRESENT.
- Generalization / OOD: discussed as field challenge; not own experiment.
- Robustness: literature collection uses three databases + full-text screening + backward snowballing + expert cross-check; exhaustive coverage explicitly not claimed.
- Dynamic-event design: NOT APPLICABLE.
- LLM API / inference cost: field-level efficiency challenge only.

## C｜Writing Evidence Coding
### Introduction
Actual sequence: **M1 importance/manual algorithm-design burden → M3 rise of LLM4AD → M4 existing surveys cover narrow/adjacent scopes → M5 lack of systematic end-to-end survey → M6 scope definition + role taxonomy + 180+ synthesis → M7 intended resource/value + roadmap**.
- Limitation/gap appears in paragraph 3 and is supported by a comparison table rather than naked rhetoric.
- Method/survey design follows in paragraph 4.
- Contributions are prose, not a numbered contribution list.
- Empirical diagnosis before method: **YES in a survey sense**: Table 1 audits prior survey coverage by stages/types before claiming scope gap.

### Related Work / organization
- No conventional standalone Related Work because the entire paper is the review.
- Multi-axis organization: **role taxonomy → design stage → application domain → challenges**.
- Role taxonomy cleanly separates optimizer/predictor/extractor/designer, preventing all “LLM use” from being treated as one category.
- Stage taxonomy separates ideation/implementation/evaluation.
- Within LLMaD and algorithm optimization, progression distinguishes simple evolutionary search, reflection/diversity, MCTS/LNS, offline vs online fine-tuning.
- Generalization section explicitly contrasts single algorithm vs portfolio/complementary set and global vs instance-specific design.

### Gap language
- `Despite this surge of interest... lacks a systematic survey` followed immediately by named neighboring survey categories and Table 1 evidence.
- Challenges sections use `remains an open question`, `significant challenge`, `key open question`, and `there remains a need` after summarizing concrete existing capabilities.
- Strong pattern: **existing capability → concrete failure mode → recent mitigation → residual question**, rather than “few studies”.
- Survey itself warns against exhaustive-coverage claims.

### Contributions
- No numbered list.
- Conceptual contribution: definition/scope of algorithm design vs code generation.
- Taxonomy contribution: four LLM roles.
- Process contribution: three design stages.
- Evidence contribution: systematic collection/screening of 180+ works and cross-domain synthesis.
- Future-direction contribution: five challenges.
- New empirical algorithm/benchmark contribution: NOT PRESENT.

### Experimental / evidence writing
- Methodology explicitly reports search databases, query logic, date cutoff, duplicate removal, staged screening, exclusion criteria, full-text review, snowballing and manual expert additions.
- Authors distinguish initial retrieval count, abstract-screen count, full-text inclusion count and final snowballed corpus.
- They explicitly disclose non-exhaustiveness, which is useful wording discipline for our final gap claims.
- Quantitative field claims are tied to the defined survey corpus, e.g. paradigm distribution, rather than universalized to all world literature.
- No statistical significance/CI because this is a systematic taxonomy survey, not meta-analysis.
