# 62｜ORLM 全文编码

- Source: `LLM/62_ORLM.md`
- Full-text status: **YES**
- Last read position: **EOF (line >1620 empty); Online Supplement Appendix A.1–A.7 covered**
- Corpus: LLM / optimization modeling / synthetic data / specialist open-source LLM
- Tier: A/C

## A｜Research Content
- Research problem: closed-source/prompt-engineered LLM optimization modeling is costly, privacy-sensitive, difficult to customize, and constrained by scarce high-quality domain training data and homogeneous benchmarks.
- Problem setting: natural-language OR problem `p` → mathematical model `m` + solver program `c`, with COPT as default solver; training open-source ~7B models using synthetic optimization-modeling data.
- Objectives: build customizable open-source OR specialist LLMs, improve modeling/executable-code performance, support industrial deployment and human-AI collaboration.
- Algorithm backbone: **OR-Instruct data synthesis → filtering/decontamination → instruction tuning → greedy or sampled inference → solver execution verification**.
- Proposed mechanism: seed industrial cases; expansion; three augmentations (objective/constraint alteration, question rephrasing, multiple modeling techniques); automatic executable-code filtering; customizable domain augmentation; instruction tuning.
- Decision layer: **Optimizer/model formulation + solver-code generation**, not runtime operator selection.
- State / Context: natural-language problem and standardized prompt; training context includes scenario/question/model/code; no online optimizer-search state.
- Action / Decision: generate mathematical model and COPT code; under pass@k generate multiple candidate solutions.
- Feedback / Reward: solver execution/ground-truth optimal value for evaluation; data filters for executability/duplicates/benchmark overlap; no online search reward in main ORLM. RL is proposed for future ranking alignment, not main trained ORLM.
- Dynamic mechanism: training data explicitly augment changing objectives/constraints for environmental adaptability, but this is offline data generation, not online dynamic scheduling control.
- LLM role: GPT-4 synthesizes data; open-source ORLM generates models/code; potential human-AI copilot.
- RL role: **NOT PRESENT in main ORLM**; discussed/proposed as future alignment method to improve pass@1 ranking.
- Claimed contribution: OR-Instruct; IndustryOR industrial benchmark; several trained open-source ORLMs; scaling/inference/limitation studies; human-AI workflow evidence.
- Explicit limitation: complex cases still suffer low model completeness, semantic/translation errors and weak ranking; performance improves with model/data scale; preference/ranked datasets needed for RL; later-stage data scaling has diminishing returns.
- 与当前 FJSP-AGV 研究关系: indirect but experimentally valuable. It shows how to separate **generation capability from ranking/selection capability**: pass@8 can be high while pass@1 remains weak. This supports evaluating an LLM selector independently from whether good operators exist in the pool. It also demonstrates targeted data customization for scheduling-like domains, but does not implement search-process/Pareto-aware AOS or operator competence learning.

## B｜Experimental Design Coding
- Dataset / Benchmark: NL4OPT, MAMO EasyLP/ComplexLP, IndustryOR; general benchmarks GSM8K/HumanEval/MMLU/BBH/TydiQA; human-AI experiment.
- Instance scale: training **32,481** examples from **686** seed industrial cases after 2 OR-Instruct iterations. NL4OPT test 289; MAMO 652 easy + 211 complex; IndustryOR 100. Human baseline: 8 senior undergraduates + 8 experts for benchmark evaluation, 70 questions/person. Human-AI efficiency study: **30 participants**, 14 experts +16 students, split 15/15, **7 problems**.
- Baselines: tag-BART; GPT-3.5 Standard/Reflexion/Chain-of-Experts; GPT-4 Standard/Reflexion/Chain-of-Experts/OptiMUS; open Llama-3.1, DeepSeek-V2, DeepSeek-R1-Distill, Qwen2, Mistral-Nemo; human students/experts; base-vs-ORLM comparisons.
- Baseline 数量: heterogeneous; Table 2 contains numerous model/method rows across PLM, proprietary LLM, open-source LLM, ORLM and human categories. Exact applicable count varies by benchmark.
- Independent runs: main LLM evaluation uses deterministic greedy decoding, not repeated stochastic runs. Human-AI study has 15 participants/group. No standard repeated model-training run count reported.
- Random seeds: NOT REPORTED.
- Population size: NOT APPLICABLE.
- Generations: NOT APPLICABLE.
- Evaluation budget: grid HPO over learning rates `{2e-5,5e-5,7e-5,3e-6,5e-6,7e-6}`, batch `{64,128,256,512}`, epochs `{1,2,3}`; final 2 epochs for reported ORLMs. Pass@k k=2,4,8 sensitivity.
- Fitness / function evaluations: NOT APPLICABLE.
- Real decoding count: one greedy output/query in main evaluation; k outputs/query for pass@k study.
- Solver calls: generated code executed to obtain/verify predicted optimum; aggregate NOT REPORTED.
- LLM calls: data synthesis cycles use expansion **20,000 times/cycle** and each augmentation **6,000 times/cycle**, two iterations; exact aggregate GPT-4 calls depends implementation and is not stated as a single total.
- Token budget: NOT REPORTED.
- Runtime / wall-clock: human solution time measured; LLM training/inference wall-clock NOT REPORTED.
- Hardware: hardware limitations discussed; exact training GPU setup for final ORLM runs NOT REPORTED in visible main/supplement text.
- Metrics: execution accuracy; micro/macro average; general benchmark accuracy; human accuracy/time; pass@k; error proportions.
- Statistical tests: **Shapiro-Wilk, Levene, Mann-Whitney U, independent t-test** in human-AI study.
- Confidence interval: **95% CI** for group differences.
- Effect size / power: **Hedge’s g + statistical power**, all reported in human-AI study.
- Ablation: full synthetic vs seed; remove each augmentation; LP-only vs mixed problem types; customized MILP enhancement; data/model scaling; inference methods.
- Sensitivity analysis: data size 2k–30k; Qwen model size 0.5B–14B; pass@1/2/4/8; temperature/top-p; training data composition.
- Generalization / OOD: multiple benchmarks, IndustryOR, multiple question types/difficulties, general LLM benchmarks; targeted MILP customization.
- Robustness: deterministic greedy decoding chosen for reproducibility; human-AI statistical testing; no repeated stochastic training robustness reported.
- Dynamic-event design: NOT PRESENT as online events; offline objective/constraint alterations simulate environmental adaptability in training data.
- LLM API / inference cost: privacy/cost motivation discussed; exact monetary API/training cost NOT REPORTED.

## C｜Writing Evidence Coding
### Introduction
Actual sequence: **M1 industrial OR value/examples → M4 dynamic-business modeling labor bottleneck → M3 LLM/mathematical reasoning progress → M3 existing proprietary/multi-agent optimization modeling → M4 privacy/customization/capability limits + concrete GPT-4 failure → M4 four enumerated deficiencies → M5/M6 proposed open-source training path → M7 three numbered contributions → empirical summary/limitations/improvement directions → paper organization**.
- Limitation appears early, then is sharpened by a **worked failure example** before the formal gap/method claim.
- Method follows an explicit 4-item diagnosis.
- Contributions: **3 numbered contributions**, each developed at paragraph length.
- Empirical diagnosis before method: **YES**, Figure 1 shows GPT-4 modeling failure before OR-Instruct is introduced.

### Related Work
- Standalone Literature Review with 3 streams: AI for OR solution; automated optimization modeling; synthetic data.
- Each stream ends by explicitly distinguishing the paper’s focus from adjacent work.
- Organization is method-family/task-family rather than purely chronological.

### Gap language
- Uses an explicit `In summary, existing ... exhibit the following deficiencies` followed by four named deficiencies.
- Then `To fill this gap` transitions to method. The paper does use first/first-of-kind language; this is author claim only and cannot be inherited without our own corpus/web verification.
- Stronger reusable rhetorical pattern is **example failure → enumerated deficiencies → design requirements → method components**.

### Contributions
- 3 numbered top-level contributions.
- Data/method contribution: OR-Instruct.
- Benchmark contribution: IndustryOR.
- Model/experimental contribution: ORLMs + broad numerical/limitation/human-collaboration analysis.
- The contribution section includes concrete scale numbers (686 seeds → 32,481 cases) rather than generic claims.

### Experimental writing
- Section 4 separates data generation, training/inference, evaluation/baselines and customization.
- Greedy decoding is explicitly justified as a **fairness/reproducibility choice**, while pass@k is analyzed separately as a capability upper-bound/ranking diagnosis.
- Baselines are grouped by PLM, proprietary GPT-based methods, open-source LLMs, ORLMs and humans.
- Human comparison states participant qualifications, assignment and submission constraints.
- Human-AI study chooses tests after Shapiro-Wilk/Levene diagnostics, then reports p-values, 95% CI, Hedge’s g and statistical power. This is unusually complete statistical-writing evidence in this corpus.
- Ablations use equal-sized datasets and fixed hyperparameters where appropriate, improving causal interpretability.
- Limitation analysis is a full empirical section: aggregate error categories → manually coded failed examples → mechanism-level explanation → targeted future remedies.

## Asset Metadata

- FULL TEXT READ: YES
- Source: `LLM/62_ORLM.md`
- Decision Layer: Domain model / modeling
- Current-study Relation: 外围
- Innovation Boundary: 当前不构成候选 selector 机制的直接新颖性反证；已实现范围为 Domain model / modeling，主要用于外围。
- Best Writing Claim: 用 synthetic OR data 训练专门 LLM 并测 IndustryOR，代表 specialist model 路线。
