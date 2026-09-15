# 22｜Large Language Models for Combinatorial Optimization: A Systematic Review 全文编码

- Source: `LLM/22_Survey-LLM4CO-ACMCS.md`
- Full-text status: **YES**
- Last read position: **EOF (line >1960 empty); Appendices A–F covered**
- Corpus: LLM / CO systematic review
- Tier: B/C（broad supporting systematic evidence）

## A｜Research Content
- Research problem: 系统梳理 LLM 在 Combinatorial Optimization 全流程中的应用。
- Problem setting: PRISMA systematic review；Scopus + Google Scholar + citation tracking；截至 2024 年底研究。
- Objectives: 回答 LLM 如何用于 COP、优化流程哪些任务、LLM architectures/training、应用领域、趋势与未来方向。
- Algorithm backbone: **NOT APPLICABLE**，systematic review。
- Proposed mechanism: PRISMA identification → screening → full-text inclusion → classification by optimization process / LLM / datasets / domains。
- Decision layer: **NOT APPLICABLE as an algorithm**；综述显式区分 problem modeling、solution method、validation、benchmarking，并在 solution method 内区分 code generation、solution generation、parameter tuning、algorithm selection。
- State / Context: NOT APPLICABLE。
- Action / Decision: NOT APPLICABLE。
- Feedback / Reward: NOT APPLICABLE。
- Dynamic mechanism: NOT APPLICABLE。
- LLM role: review taxonomy includes modeling, code/solution generation, parameter tuning, algorithm selection, validation, benchmarking/explainability。
- RL role: background/individual included studies may use RL, review itself NOT APPLICABLE。
- Claimed contribution: first claimed systematic PRISMA review focused specifically on LLMs in CO; 103 included studies；full optimization-process scope；datasets/frameworks/tools/metrics and future directions。
- Explicit limitation: fast-moving field and incomplete coverage risk；evidence/selection bias toward positive LLM studies；excludes CO-for-LLM and continuous optimization；many preprints；closed-source models impede reproducibility。
- 与当前 FJSP-AGV 研究关系: 提供 2022–2024 领域基线而非当前直接 novelty proof。重要历史证据：该综述当时在 103 studies 中只编码 1 个 algorithm selection study，并将“LLM dynamically adjust MH strategies / switch strategies based on current search state / expand local-search neighborhoods”列为 future directions。但该结论时间截断在 2024，且后续 HeurAgenix、ReflecSched 等已明显推进，所以不能拿它直接证明 2026 gap，只能作为技术演进的历史锚点。

## B｜Experimental Design Coding
- Dataset / Benchmark: systematic-review corpus, not optimization experiment。
- Instance scale: identification 2044 database records；1472 distinct after cleaning；citation tracking 420→319 distinct；174 full-text candidates；103 included studies。
- Baselines: NOT APPLICABLE。
- Baseline 数量: NOT APPLICABLE。
- Independent runs: NOT APPLICABLE。
- Random seeds: NOT APPLICABLE。
- Population size: NOT APPLICABLE。
- Generations: NOT APPLICABLE。
- Evaluation budget: NOT APPLICABLE。
- Fitness / function evaluations: NOT APPLICABLE。
- Real decoding count: NOT APPLICABLE。
- Solver calls: NOT APPLICABLE。
- LLM calls: NOT APPLICABLE。
- Token budget: NOT APPLICABLE。
- Runtime / wall-clock: NOT REPORTED / NOT APPLICABLE。
- Hardware: NOT REPORTED / NOT APPLICABLE。
- Metrics: review counts/percentages; included studies' heterogeneous metrics catalogued；no shared universal CO-LLM metric found。
- Statistical tests: no meta-analysis/significance test for synthesized effects；NOT PRESENT。
- Confidence interval: NOT PRESENT。
- Ablation: NOT PRESENT。
- Sensitivity analysis: NOT PRESENT。
- Generalization / OOD: NOT APPLICABLE to review experiment。
- Robustness: cross-check/full-text screening by multiple authors and conflict resolution; no quantitative sensitivity analysis。
- Dynamic-event design: NOT APPLICABLE。
- LLM API / inference cost: NOT APPLICABLE。
- Review methodology details: 4 inclusion + 4 exclusion criteria；3 authors independently read one-third each, collective cross-check, final screening/conflict resolution；PRISMA checklist included。

## C｜Writing Evidence Coding
### Introduction
Sequence: **M2 CO definition/application → M3 traditional modeling/solving → M4 human expertise burden → M3 LLM opportunity → M4 fragmented literature → M5 need for consolidation → M6 systematic review aim/PRISMA → roadmap**。
- Limitation: human-driven optimization burden in paragraph 2；literature fragmentation in paragraph 4。
- Method: PRISMA systematic review introduced after fragmentation rationale。
- Contributions: not conventional numbered M7 contribution bullets in Introduction；Section 2 gives six research questions and Section 3 gives five explicit differences vs prior surveys。
- Empirical diagnosis before method: NO；review motivation is literature-structure based。

### Related Work
- Dedicated Section 3。
- Organization: **survey-by-survey comparative scope**，不是 chronological/method taxonomy。
- It explicitly contrasts coverage dimensions: OR vs CO, LLM-for-optimization vs optimization-for-LLM, EC-only vs full optimization process, systematic vs non-systematic。
- traditional→learning→LLM: NO as section organization。
- generation vs selection: not organizing axis。
- direct solving vs solver-assisted: not organizing axis。

### Gap language
- `While highlighting...` moves from publication growth to navigation difficulty。
- `limited and fragmented` characterizes literature state。
- `Therefore` motivates systematic consolidation。
- Related Work uses `However` and explicit scope contrasts to delimit prior reviews。
- Strong novelty in conclusion: `To our knowledge, this is the first attempt to comprehensively study...`。
- Future directions carefully use `could`, `might`, `promising research direction` rather than treating proposals as established facts。

### Contributions / research questions
- Conventional contribution bullet count: **NOT PRESENT**。
- Section 2 research questions: **6 numbered questions**。
- Section 3 differentiators: **5 numbered points**。
- Methodological contribution: PRISMA systematic review。
- Taxonomy/synthesis contribution: optimization process, LLM, datasets, domains。
- Experimental contribution: NOT APPLICABLE。
- Benchmark contribution: NOT a new benchmark；catalogues benchmark datasets。

### Experimental/review writing
- Methodology sequence: PRISMA → terminology → literature collection process → identification → screening → inclusion。
- Reproducibility writing: exact search dates, databases, keywords/queries, counts at each stage, inclusion/exclusion rules, reviewer workflow and conflict resolution。
- Results writing: always specifies denominator where meaningful, e.g. 64/103 solution-method studies, 38/103 modeling, 7/103 benchmarking, 9/103 validation, 24/103 multi-step。
- Taxonomy writing: top-down from optimization process → activities → algorithm/model types → LLM architecture → benchmark datasets → application domains。
- Limitations: dedicated Section 8 with coverage recency, selection bias, scope exclusions, preprints, closed-source reproducibility。
- Statistical significance/computational cost: NOT APPLICABLE as a systematic review without meta-analysis。

## Asset Metadata

- FULL TEXT READ: YES
- Source: `LLM/22_Survey-LLM4CO-ACMCS.md`
- Decision Layer: Field taxonomy
- Current-study Relation: 背景综述
- Innovation Boundary: 当前不构成候选 selector 机制的直接新颖性反证；已实现范围为 Field taxonomy，主要用于背景综述。
- Best Writing Claim: 系统梳理 LLM4CO 任务、方法、数据与趋势，是领域导航而非直接竞品。
