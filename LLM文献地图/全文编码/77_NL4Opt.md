# 77｜NL4Opt Competition 全文编码

- Source: `LLM/77_NL4Opt.md`
- Full-text status: **YES**
- Last read position: **EOF (line >520 empty); no appendix present**
- Corpus: LLM / optimization modeling benchmark
- Tier: B/C

## A｜Research Content
- Research problem: convert natural-language descriptions of optimization problems into solver-usable mathematical formulations.
- Problem setting: LP word problems; two-stage competition: semantic entity recognition followed by formulation/meaning-representation generation. Post-competition ChatGPT experiment combines both stages into direct formulation generation.
- Objectives: improve accessibility/usability of OR solvers for non-experts; benchmark learning-based natural-language interfaces; test generalization to unseen application domains.
- Algorithm backbone: supervised NER and sequence-to-sequence semantic parsing benchmark; winning systems use ensembles, augmentation, adversarial training, prompt/input redesign; ChatGPT direct generation comparison.
- Proposed mechanism: dataset + two linked tasks rather than one new optimizer. Task 1 labels constraint direction/limit, objective direction/name, parameter and variable. Task 2 generates canonical meaning representation convertible to solver format.
- Decision layer: **Optimizer/model formulation generation**.
- State / Context: natural-language LP description; for sub-task 2, ground-truth detected entities and variable mention order are supplied; ChatGPT receives the raw problem description plus formatting instructions.
- Action / Decision: entity tags or canonical objective/constraint declarations.
- Feedback / Reward: micro-F1 for NER; declaration-level mapping accuracy for formulation; OR-expert manual correctness verification for ChatGPT.
- Dynamic mechanism: NOT PRESENT.
- LLM role: ChatGPT direct formulation generator in post-competition experiment; transformer language models also underpin winning supervised systems.
- RL role: NOT PRESENT in the competition methods summarized here.
- Claimed contribution: 1,101 expert-annotated LP word problems across six domains; NeurIPS 2022 two-task benchmark; analysis of winning solutions; post-competition ChatGPT comparison.
- Explicit limitation: dataset complexity below realistic industrial descriptions; ChatGPT generalizability under more realistic/complex descriptions remains unclear; trustworthiness/robustness need study; ensemble methods increase complexity and computational expense.
- 与当前 FJSP-AGV 研究关系: indirect. It provides strong precedent for decomposing LLM system evaluation into intermediate correctness and downstream semantic correctness, and for **holding out entire domains** rather than only random instances. It does not address heuristic/operator selection, dynamic scheduling, Pareto search state or operator competence.

## B｜Experimental Design Coding
- Dataset / Benchmark: NL4Opt LPWP.
- Instance scale: **1,101** annotated problems from six domains; train **713**, dev **99**, test **289**. Source domains: sales, advertising, investment. Target/unseen domains: production, transportation, sciences, reserved for dev/test.
- Dataset creation: 20 AI engineers/OR experts over three months for preliminary 600; remaining 501 assisted by preliminary NER; all new problems/annotations verified and corrected by at least two experts.
- Competition participation: >150 registered teams, >300 valid independent submissions; 19 teams valid for task 1, 9 for task 2.
- Baselines: XLM-RoBERTa-base for NER (F1 0.906); BART encoder-decoder + prompt/copy mechanism for generation (accuracy 0.610). Random/simple baseline NOT REPORTED.
- Baseline 数量: **2 official baselines**, one per sub-task; five ranked winning systems per task are summarized separately.
- Independent runs: paper-level standardized repeated-run count NOT REPORTED. Individual teams sometimes use multiple random initializations/ensembles; Team mcmc trains 9 variants. This must not be coded as corpus-wide independent runs.
- Random seeds: exact values NOT REPORTED; seed sensitivity is reported for UIUC-NLP BART-large.
- Population size: NOT APPLICABLE.
- Generations: NOT APPLICABLE.
- Evaluation budget: fixed dev/test splits; >300 competition submissions. API evaluation budget for ChatGPT NOT REPORTED.
- Fitness/function evaluations: NOT APPLICABLE.
- Real decoding count: NOT REPORTED.
- Solver calls: formulations are designed to be convertible to commercial solvers, but aggregate solver-call count NOT REPORTED.
- LLM calls: NOT REPORTED.
- Token budget: NOT REPORTED.
- Runtime / wall-clock: NOT REPORTED.
- Hardware: NOT REPORTED.
- Metrics: micro-averaged F1 for NER; declaration-level mapping accuracy for formulation; ChatGPT per-declaration accuracy by expert verification.
- Main results: task1 best 0.939 vs baseline 0.906; task2 best 0.899 vs baseline 0.610; ChatGPT combined direct task 0.927 on reserved test set.
- Statistical tests: NOT REPORTED.
- Confidence interval: NOT REPORTED.
- Ablation: summarized team-specific ablations, e.g. Infrrd ensemble/augmentation; UIUC input tagging + decode-all-at-once; Sjang tag embedding/augmentation. No unified organizer ablation protocol.
- Sensitivity analysis: UIUC reports BART-large greater hyperparameter/seed sensitivity; input representation/prompt design discussed.
- Generalization / OOD: **explicit domain holdout**. Target domains production/transportation/sciences excluded from training and present only in dev/test. Organizers re-trained final submissions to ensure dev was not used for training.
- Robustness: adversarial training used by some teams; paper explicitly calls for future LLM trustworthiness/robustness tests. Formal robustness benchmark for ChatGPT NOT PRESENT.
- Dynamic-event design: NOT PRESENT.
- LLM API / inference cost: NOT REPORTED; ensemble computational expense discussed qualitatively.

## C｜Writing Evidence Coding
### Introduction
Actual sequence: **M1 OR importance/applications → M2 modeling workflow → M4 iterative/strenuous formulation bottleneck → M6 NL4Opt learning-based interface → M3 semantic parsing/math-word-problem context → M5 optimization formulation differs from answer generation → M3 related challenges → M6/M7 competition expansion to entity detection + mathematical formulation**.
- Limitation appears in paragraph 1 after domain importance.
- Proposed research direction appears paragraph 2.
- Formal numbered contribution list: NOT PRESENT.
- Empirical diagnosis before method: NO; motivation is workflow/problem based.

### Related Work
- Standalone Related Work section: **NOT PRESENT**.
- Prior work is embedded in Introduction and organized by neighboring task families: semantic parsing, math word problems, scientific-text challenges.
- Contrast is functional: prior NLP often seeks final answers, whereas NL4Opt seeks a solver-usable formulation.

### Gap language
- Functions: practical bottleneck → contrast with adjacent NLP tasks → under-explored formulation task → benchmark motivation.
- The paper uses an explicit historical scarcity phrase (`under-explored`) in its 2022 context, but this is paper-local evidence and must not be reused as a 2026 field-level gap claim.

### Contributions
- No numbered contribution section.
- benchmark/data contribution: 1,101 LPWP dataset + two tasks.
- empirical contribution: competition statistics/winning-method analysis.
- LLM comparison contribution: post-hoc ChatGPT direct-formulation evaluation.

### Experimental writing
- Strong reproducibility/fairness narrative is built into dataset split: source vs target domains and organizer re-training to prevent dev leakage.
- Baseline descriptions state model and metric values directly before winning systems.
- Results are organized by rank/team and then synthesized in Discussion by recurring mechanism (ensemble, augmentation, preprocessing/prompt design).
- Discussion explicitly separates performance from deployment cost/transparency: competition-optimal ensembles may be undesirable for time-sensitive real-world use.
- Failure analysis for ChatGPT lists concrete semantic error categories rather than reporting accuracy alone.
- Weaknesses for statistical corpus: no standardized repeated-run count, seeds, inferential tests, CI, runtime/hardware or API cost.

## Asset Metadata

- FULL TEXT READ: YES
- Source: `LLM/77_NL4Opt.md`
- Decision Layer: Modeling benchmark
- Current-study Relation: 背景定义
- Innovation Boundary: 当前不构成候选 selector 机制的直接新颖性反证；已实现范围为 Modeling benchmark，主要用于背景定义。
- Best Writing Claim: 自然语言优化建模 benchmark，把 entity recognition 与 formulation generation 标准化。
