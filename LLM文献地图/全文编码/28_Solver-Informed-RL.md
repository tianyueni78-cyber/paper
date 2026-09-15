# 28｜Solver-Informed RL (SIRL) 全文编码

- Source: `LLM/28_Solver-Informed-RL.md`
- Full-text status: **YES**
- Last read position: **EOF (line >1040 empty); supplementary Sections 6–13/checklist covered**
- Corpus: LLM / OR modeling / RLVR
- Tier: B（Supporting mechanism evidence）

## A｜Research Content
- Research problem: natural-language optimization modeling by LLM often yields syntactically invalid, infeasible or functionally wrong models; offline SFT/preference learning does not directly optimize solver-verifiable correctness.
- Problem setting: NL description → reasoning → mathematical model → Gurobi code → solver execution/objective; optimization-modeling benchmarks.
- Objectives: use classical solver as objective oracle for data synthesis and RLVR; improve authentic/executable/correct optimization modeling.
- Algorithm backbone: instance-enhanced self-consistency data synthesis + REINFORCE++ online RL + Partial KL surrogate + two-stage solver-informed reward curriculum.
- Proposed mechanism: generated code executed to obtain objective, feasibility and `.lp`; `.lp` structural features support consensus and reward; RL samples K trajectories; Partial KL regularizes only model/code segments while leaving reasoning less constrained; stage-1 format/execution/accuracy reward, stage-2 advanced-modeling bonus.
- Decision layer: **Optimizer/model formulation generation and LLM policy adaptation**. Not heuristic/operator/scheduling selection.
- State / Context: NL problem; generated reasoning/model/code trajectory; ground-truth optimal objective; solver execution status/objective; `.lp` direction and variable statistics.
- Action / Decision: generate reasoning/model/code; policy parameter update through REINFORCE++; synthesis roles generate/refine candidates.
- Feedback / Reward: format validity, executable code, objective correctness, feasibility, `.lp` model structure and advanced-technique bonus.
- Dynamic mechanism: online RL policy update/curriculum during training; iterative refinement during synthesis. External dynamic scheduling: NOT PRESENT.
- LLM role: optimization reasoning/model/code generator; synthetic-data generator/judge/refiner.
- RL role: central: REINFORCE++ RLVR with solver-verifiable reward and Partial KL.
- Claimed contribution: claimed first RLVR application directly enhancing LLM optimization modeling; instance-enhanced self-consistency; solver-informed rich reward; Partial KL; two-stage reward curriculum.
- Explicit limitation: conclusion notes reward hacking remains; IndustryOR/OptMATH performance remains limited; future systematic error analysis/targeted improvement. No separate Limitations heading in main text.
- 与当前 FJSP-AGV 研究关系: Not a direct AHD competitor, but it establishes a strong methodological precedent: **external optimization execution can provide objective, structural and process-aware reward instead of subjective LLM judgement**. Thus using real decoder/solver outcomes as feedback is not novel. For current work, any competence/effect model should ground predictions in real decoded scheduling outcomes and explicitly separate prediction from objective verification.

## B｜Experimental Design Coding
- Dataset / Benchmark: NL4OPT, MAMO Easy, MAMO Complex, IndustryOR, OptMATH; seed 686 real-world industry cases + 100 scenarios.
- Instance scale: corrected evaluation counts NL4OPT 245; MAMO Easy 642; MAMO Complex 203; IndustryOR 100; OptMATH table says 166 after correction while text says main results use larger 193 variant, an internal reporting inconsistency that must be retained rather than silently reconciled.
- Baselines: GPT-4, DeepSeek-V3.1, DeepSeek-R1, OpenAI-o3, OptiMUS, ORLM-LLaMA3-8B, LLMOpt-Qwen2.5-14B, OptMATH-Qwen2.5-7B/32B; Base/SFT/RL further comparison; no-solver Math4Opt-RL comparison.
- Baseline 数量: main Table 1 external named baseline models = **9** excluding two SIRL models.
- Independent runs: main deterministic pass@1 repeated-run count NOT REPORTED. Further stochastic sampling reports mean±std across `multiple runs`, but **number of runs NOT REPORTED**.
- Random seeds: **NOT REPORTED**.
- Population size: NOT APPLICABLE.
- Generations: NOT REPORTED as generations.
- Evaluation budget: synthesis uses 10 roles/attempts; trivial filtering threshold 8/10; training dataset ~70k filtered then 10k sampled; rollout number 8; batch size 128.
- Fitness / function evaluations: NOT APPLICABLE as heuristic fitness budget; solver verification performed extensively, aggregate count NOT REPORTED.
- Real decoding count: training rollout number 8 per prompt; aggregate decoding count NOT REPORTED.
- Solver calls: aggregate NOT REPORTED.
- LLM calls: aggregate NOT REPORTED.
- Token budget: max prompt 2048; max response 8192; inference max tokens 8192.
- Runtime / wall-clock: stage 1 ~24h + stage 2 ~24h for 7B; **384 GPU-hours total**.
- Hardware: single compute node with **8×80GB NVIDIA H100** for 7B training.
- Metrics: pass@1 accuracy; execution rate ER; self-consistency accuracy; mean±std under stochastic sampling; error-type distributions.
- Statistical tests: **NOT REPORTED**.
- Confidence interval: **NOT REPORTED**.
- Ablation: Partial KL vs Full KL vs Without KL; two-stage vs stage-1 only vs stage-2 only; instance-enhanced vs value-only self-consistency; base vs SFT vs RL; no-external-solver comparison.
- Sensitivity analysis: no systematic hyperparameter sensitivity reported.
- Generalization / OOD: cross-benchmark transfer to multiple modeling types; not a clearly labeled OOD split.
- Robustness: stochastic top-p evaluation reports mean±std; error taxonomy; multi-role self-consistency.
- Dynamic-event design: NOT PRESENT.
- LLM API / inference cost: monetary API cost **NOT REPORTED**.
- Training: Qwen2.5-7B/32B; REINFORCE++; LR 1e-6; batch 128; KL coefficient .005; rollout 8; PPO minibatch 8; microbatch/GPU 4; clip .20/.28.
- Decoding: n=1, temp=.5, top-p=.9, repetition penalty 1.02; robustness top-p=.95.

## C｜Writing Evidence Coding
### Introduction
Actual sequence: **M1 optimization modeling importance/process → M4 manual NL→model bottleneck → M3 modeling languages + LLM prompt/agent route → M4 frozen-model limitations → M3 offline SFT/alignment → M4 functional-correctness limitation → M3 RLVR/LRM success → M5 optimization artifacts are solver-verifiable → M6 SIRL/solver-informed reward + Partial KL idea → M7 four numbered contributions**.
- Limitation first appears paragraph 1 as manual modeling bottleneck; LLM-specific limitation after prompt/agent route.
- Method appears after RLVR opportunity is built through analogy from math/code verification to solver verification.
- Contributions: **4**, inline numbered `(1)…(4)`.
- Empirical diagnosis before method: NO new experiment; mechanism is motivated by verification properties.

### Related Work
- Organized by method family: LLMs for optimization modeling; LLM-based data synthesis; RL with verifiable reward; external tools as verifier.
- traditional→learning→LLM: partial in Introduction, not RW taxonomy.
- direct solving vs solver-assisted: tool-verifier distinction is central.
- generation vs selection: NO.
- static vs adaptive: prompt/frozen vs offline learning vs online RL distinction is explicit across Intro/RW.
- offline vs online: YES, explicit.

### Gap language
- `However` repeatedly narrows failure from prompt-based to offline learning to correctness guarantees.
- `Recently` introduces RLVR as adjacent capability rather than pretending it arose inside OR.
- Key analogy transition: classical optimization solvers are positioned as the domain-specific objective oracle analogous to Lean/compiler verification.
- Strong novelty: `To the best of our knowledge, this is the first application of RLVR to directly enhance LLMs’ proficiency in optimization modeling.` Narrow scope is explicit.

### Contributions
- Count: **4**; numbered: YES.
- Method: instance-enhanced self-consistency + SIRL + Partial KL/reward.
- Formulation: surrogate/reward design.
- Experimental: 7B/32B benchmark results.
- Benchmark/data: curated/corrected evaluation sets and synthesized training data are important artifacts, though benchmark creation is not the headline contribution.
- Empirical finding: solver-informed RL beats offline/agent/foundation baselines.

### Experimental writing
- Main experiment section is concise and moves detailed setup/hyperparameters/decoding to appendix/supplement.
- Main results first define benchmark validity threshold, then split interpretation by 7B vs 32B scale.
- Ablations are hypothesis-aligned: surrogate design and reward curriculum each get separate subsections.
- Supplement extends experiments with stochastic mean±std, no-solver baseline, SFT baseline, error taxonomy and qualitative Partial-KL case studies.
- Fairness caveat is explicit: some baseline values are copied/reproduced and marked `*` under the same relative-error criterion.
- Statistical significance tests absent; robustness is conveyed with stochastic mean±std and error distributions.
- Computational cost is unusually concrete for training: 8×H100, 48h total, 384 GPU-hours, token limits and rollout hyperparameters; monetary cost absent.
