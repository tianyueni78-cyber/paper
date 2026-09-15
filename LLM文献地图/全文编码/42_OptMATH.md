# 42｜OptMATH 全文编码

- Source: `LLM/42_OptMATH.md`
- Full-text status: **YES**
- Last read position: **EOF (line >1360 empty); Appendices A–E covered**
- Corpus: LLM / optimization modeling / data synthesis
- Tier: C/B（Background-supporting）

## A｜Research Content
- Research problem: lack of large, high-quality, complex optimization-modeling datasets limits LLM modeling robustness/generalization.
- Problem setting: synthesize aligned natural-language description (NL), mathematical formulation (MF), and problem data/solver code (PD), then train an AutoFormulator.
- Objectives: scalable controllable PD generation; bidirectional backtranslation/forward-modeling validation; verified training set + hard benchmark; study data/model scaling.
- Algorithm backbone: expert seed generators + feedback-driven LLM parameter tuning + backtranslation/self-critique/refinement + AutoFormulator forward modeling + Gurobi rejection sampling + augmentation + LoRA SFT.
- Proposed mechanism: LLM adjusts generator parameters from complexity/solve-time/feasibility feedback; generated MF/PD are backtranslated to NL; AutoFormulator reconstructs MF/PD; original and reconstructed solver objectives are compared and mismatches rejected; accepted data fine-tune AutoFormulator.
- Decision layer: **dataset/instance generation control + optimization formulation generation**, not search-operator selection.
- State / Context: generator code/configuration, target complexity/time/feasibility, aggregate generated-instance statistics; for modeling, NL plus prompt instruction.
- Action / Decision: adjust generator configuration; generate/refine NL; generate MF + Gurobi code.
- Feedback / Reward: complexity score, solving time, feasibility rate, rejection-sampling objective-value equality; no RL reward.
- Dynamic mechanism: iterative feedback loop for generator configuration and a data/model flywheel; not dynamic scheduling/search control.
- LLM role: configuration tuner, backtranslator/self-critic/refiner, augmentation generator; fine-tuned AutoFormulator performs NL→MF/PD.
- RL role: NOT PRESENT.
- Claimed contribution: scalable bidirectional synthesis; OptMATH-Train; OptMATH-Bench; broad model/data scaling evidence.
- Explicit limitation: solution-value matching does not guarantee exact formulation equivalence; exact equivalence remains open. Hard benchmarks remain difficult even for larger models. No standalone Limitations section.
- 与当前 FJSP-AGV 研究关系: indirect methodological support. It shows a useful `proposal/generation → external objective/solver verification → rejection/feedback` architecture and explicit complexity/cost control. It does not challenge the current operator-selection novelty directly, but reinforces that LLM decisions should be validated by downstream objective/search effects rather than linguistic plausibility.

## B｜Experimental Design Coding
- Dataset / Benchmark: OptMATH-Train; OptMATH-Bench; NL4OPT; MAMO EasyLP/ComplexLP.
- Instance scale: >600,000 quality-filtered generated LP files across 53 problem types/five hardness levels during generation; OptMATH-Train >150k reverse-generated + 50k augmented; NL4OPT test 245; MAMO EasyLP 652, ComplexLP 211. OptMATH-Bench size is not clearly stated in the read text.
- Baselines: GPT-3.5-turbo, GPT-4, DeepSeek-V3; Chain-of-Experts, Optimus; ORLM-LLaMA-3-8B; base Qwen2.5 variants; own 7B/32B models.
- Baseline 数量: main Table 1 contains **6 external baseline systems/models** before two OptMATH models if GPT-3.5/GPT-4/DeepSeek-V3/Chain-of-Experts/Optimus/ORLM are counted individually; base-vs-finetuned scaling adds six Qwen2.5 sizes.
- Independent runs: NOT REPORTED.
- Random seeds: generator supports seed but experimental seed values NOT REPORTED.
- Population size / generations: NOT APPLICABLE; SFT 1–3 epochs generally; model-size study uses 100k examples due compute constraints.
- Evaluation budget: pass@1; backtranslation T ablation uses 500 randomly selected instances; manual quality analysis samples 1% of total dataset.
- Fitness / function evaluations: NOT APPLICABLE.
- Real decoding count: augmentation samples each augmented description **twice independently**; other aggregate decoding counts NOT REPORTED.
- Solver calls: Gurobi solves original and generated PD for rejection sampling; exact aggregate count NOT REPORTED.
- LLM calls: iterative generator tuning/backtranslation/augmentation entail multiple calls; aggregate exact count NOT REPORTED.
- Token budget: NOT REPORTED. Self-refine T chosen partly for token efficiency.
- Runtime / wall-clock: generated-instance solve time is controlled as a criterion, but aggregate training/inference wall-clock NOT REPORTED.
- Hardware: NOT REPORTED in paper text read.
- Metrics: pass@1 accuracy, Macro AVG, Micro AVG, rejection acceptance rate, dataset/problem length distributions, complexity/feasibility/solve-time criteria.
- Statistical tests: NOT REPORTED.
- Confidence interval: NOT REPORTED.
- Ablation: model size 0.5B–32B; data size/proportion; self-refine iterations T; raw vs augmented vs 50/50 mixture.
- Sensitivity analysis: five difficulty ranges; T ∈ {0,1,3,5,7,9,10}; model/data scaling.
- Generalization / OOD: cross-benchmark NL4OPT/MAMO/OptMATH-Bench; LP/MILP/IP/NLP/SOCP; >10 application domains.
- Robustness: manual 1% equivalence audit gives 99.6%; conventional repeated-run robustness NOT REPORTED.
- Dynamic-event design: NOT PRESENT.
- LLM API / inference cost: monetary/token cost NOT REPORTED.

## C｜Writing Evidence Coding
### Introduction
Actual sequence: **M1 optimization-modeling importance → M4 manual ambiguity/expertise burden → M3 general LLM progress → M4 optimization modeling remains semi-open/knowledge-heavy and direct LLM is suboptimal → M3 prompt-based modeling → M4 prompting limitations → M3 fine-tuning → M4 small/inconsistent/low-complexity synthetic data limits generalization → M3 data synthesis/instance generation → M6 OptMATH → M7 three contribution paragraphs**.
- Limitation appears in opening paragraph and repeatedly after each prior route.
- Method/contribution transition occurs under `Our Contributions`.
- Contributions: **3 prose paragraphs**, not numbered bullets.
- Empirical diagnosis before method: prior-study evidence plus data-complexity argument, not a new diagnostic experiment.

### Related Work
- No standalone `Related Work` heading; literature review is embedded in Introduction through labeled mini-sections: LLMs for Optimization Modeling; LLM-Based Data Synthesis; Instance Generation.
- Organization is method-family/taxonomic rather than chronological.
- prompt-based vs fine-tuning is an explicit two-route taxonomy.
- direct solving vs solver-assisted / generation vs selection / offline vs online are not primary dimensions.

### Gap language
- `However, optimization modeling presents unique challenges` narrows general LLM capability to domain difficulty.
- `However, most of these methods generate small amounts ... inconsistent quality and insufficient complexity. Consequently... generalize ... limited` supplies the main training-data gap.
- `To address these challenges, we propose...` appears already in Abstract; Introduction uses `We propose... addresses the critical challenge...`.
- Rejection Sampling section explicitly hedges validation: objective equality `may not guarantee perfect equivalence`, followed by manual audit evidence and an open research question.

### Contributions
- Count: **3 contribution paragraphs**.
- Framework/method contribution: bidirectional triplet-aligned synthesis with optimal-value matching.
- Dataset contribution: OptMATH-Train.
- Benchmark contribution: OptMATH-Bench.
- Experimental contribution: cross-benchmark and scaling experiments.
- Formulation contribution: complexity scoring/control mechanism is methodological but not framed as main standalone contribution.

### Experimental writing
- Experiments begin with dataset statistics before model evaluation, appropriate because dataset quality/coverage is itself the artifact under study.
- Evaluation explicitly fixes the same prompt across models for fairness.
- Main results compare proprietary, prompt-based, fine-tuned and own models by category.
- Ablations are distributed between main text and appendices: model size, data size, self-refine iterations, augmentation composition.
- Cost trade-off is used causally in selecting T=1: acceptance improvement versus computational/token efficiency.
- Negative/limited findings are retained: larger models still perform modestly on hard benchmarks; augmentation-only can hurt simple datasets; objective matching is not proof of exact equivalence.
- No statistical significance/CI/repeated-run reporting.

## Asset Metadata

- FULL TEXT READ: YES
- Source: `LLM/42_OptMATH.md`
- Decision Layer: Data verification
- Current-study Relation: 支持可验证数据/结果
- Innovation Boundary: 当前不构成候选 selector 机制的直接新颖性反证；已实现范围为 Data verification，主要用于支持可验证数据/结果。
- Best Writing Claim: 用 solver/rejection verification 构造优化建模数据，说明 solver 可作为训练数据质量门。
