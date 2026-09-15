# 12 StepORLM｜全文编码

## Audit
- Source: `LLM/12_StepORLM.md`
- Full text read to EOF: YES
- Abstract, Introduction, Related Work, Methodology, Experiments, main results, self-evolution analysis, inference scaling, Ablation, Conclusion, benchmark appendix, case study and reasoning-template appendix: READ where present. Dedicated limitations section: NOT PRESENT.

## A. Research Content
- Research problem: reliable LLM reasoning for operations-research modeling under long-horizon interdependent reasoning, addressing outcome-reward credit assignment and myopia of discriminative stepwise process supervision.
- Problem setting: natural-language OR modeling → mathematical formulation/reasoning → executable solver code across multiple OR benchmarks.
- Objectives: improve process-sound and outcome-correct OR reasoning; train a policy model and reusable process verifier.
- Algorithm backbone: two-stage SFT + iterative co-evolution; policy/GenPRM trained through solver verification, generative process supervision and Weighted DPO.
- Proposed mechanism: solver-verified warm-up data synthesis; policy generates multiple trajectories; external solver gives outcome labels; GenPRM holistically critiques completed trajectory; W-DPO aligns policy; solver-derived process labels refine GenPRM; repeat.
- Decision layer: LLM policy/model training and reasoning verification; not heuristic/operator selection in an optimization algorithm.
- State/context: full OR reasoning trajectory, step structure, solver outcome, GenPRM process judgments, preference pairs and evolving policy/critic state.
- Action/decision: policy generates modeling/reasoning/code trajectory; GenPRM evaluates trajectory; training updates policy and critic.
- Feedback/reward: dual source: definitive external-solver outcome + holistic generative process feedback; weighted preference signal.
- Dynamic mechanism: policy and GenPRM co-evolve across training iterations; not a dynamic scheduling environment.
- LLM role: policy reasoner, teacher for data synthesis, generative process reward model/verifier.
- RL role: preference-based alignment (W-DPO) motivated as alternative/refinement to RL supervision; no scheduling RL selector.
- Claimed contribution: generative trajectory-level process supervision for OR, self-evolving policy–GenPRM loop, SOTA OR modeling performance, transferable inference-time verifier, released models/code.
- Explicit limitation: dedicated limitations section NOT PRESENT; discussion notes benchmark/test-size effects and non-monotonic iteration behavior but does not formalize a limitations section.
- Relation to current FJSP-AGV research: useful mechanism evidence for structured trajectory feedback/credit assignment and external verification, but decision object is OR reasoning/model generation rather than online search-operator selection.

## B. Experimental Design
- Dataset / Benchmark: NL4Opt, MAMO EasyLP/ComplexLP, NLP4LP, ComplexOR, IndustryOR, ReSocratic; paper describes six benchmark families with MAMO split, while tables expose seven score columns.
- Instance scale: appendix reports validated subsets; examples include ComplexOR 18, IndustryOR 42, ReSocratic 403; other benchmark counts specified in appendix.
- Baselines: zero-shot GPT-4o, DeepSeek-V3, Qwen3-32B, Qwen2.5-72B; fine-tuned ORLM, LLMOPT, OptMATH; agentic OptiMUS-v0.3, CoT, CoE, CAFA; inference-scaling strategies majority vote, solver execution, discriminative PRM, initial/final GenPRM.
- Number of baselines: main Table 1 includes 4 zero-shot + 3 specialized named baseline families/models (with original/reproduced LLMOPT entries) + 4 agentic methods; exact denominator should be computed from structured table during final aggregation.
- Independent runs: NOT REPORTED as a repeated-run protocol.
- Random seeds: NOT REPORTED.
- Population size: NOT APPLICABLE.
- Generations: SFT 3 epochs; self-evolving loop analyzed over multiple iterations, with three later iterations visible in analysis; exact total update rounds should be taken from method/training config if needed.
- Evaluation budget: training dataset 50K questions; 4 trajectories generated per response in self-evolving sampling.
- Fitness/function evaluations: NOT APPLICABLE as classical optimizer FE budget.
- Real decoding count: inference-scaling uses multiple sampled trajectories; unified decoding-count budget across all baselines NOT REPORTED.
- Solver calls: solver execution used for data verification/outcome labels; exact total count NOT REPORTED.
- LLM calls: NOT REPORTED as aggregate calls.
- Token budget: max sequence length 8192; aggregate token budget NOT REPORTED.
- Runtime / wall-clock: NOT REPORTED as a principal comparative metric.
- Hardware: single node with 8× NVIDIA H100 80GB GPUs.
- Metrics: Pass@1 accuracy, macro average; iteration-wise accuracy; inference-scaling gains.
- Statistical tests: NOT REPORTED.
- Confidence interval: NOT REPORTED.
- Ablation: w/o SFT, w/o Self-evolution, w/o GenPRM Evolution, w/o W-DPO.
- Sensitivity analysis: inference-scaling strategy comparison; not a conventional hyperparameter sensitivity section.
- Generalization / OOD: GenPRM applied to external ORLM policy model as universal verifier; cross-benchmark evaluation.
- Robustness: reward-hacking/failure case study; broad benchmark performance.
- Dynamic-event design: NOT PRESENT.
- LLM API / inference cost: NOT REPORTED as monetary cost.

## C. Writing Evidence
### Introduction rhetorical moves
- M1 LLM-for-OR domain framing → M3 two research fronts/advanced training → M4 two explicitly named RL supervision flaws → M5 trajectory-level supervision need → M6 StepORLM/co-evolution/dual feedback → M7 four contribution bullets.
- Empirical/conceptual diagnosis appears before method through Figure 1 failure cases.

### Related Work organization
- Method-family taxonomy: LLMs for optimization modeling; advanced training/refinement paradigms.
- Second subsection contrasts outcome RL, process PRMs, preference training and search/evolution, then synthesizes the unresolved trade-off.

### Gap / limitation formulation
- Mechanism-level gap with explicit causal diagnosis: outcome-only reward has credit-assignment failure; discriminative stepwise PRM is myopic for interdependent OR trajectories.
- Uses `However`, `While`, `Thus`, `To bridge this gap`/equivalent transitions and named failure modes.

### Proposed-method transition
- `Therefore, we argue... paradigm shift` → `To this end, we propose... StepORLM`.

### Contribution structure
- 4 bullets: novelty/process supervision claim, framework/mechanism, empirical SOTA+universal verifier, release/reproducibility.
- Includes an explicit `To the best of our knowledge, we are the first...` novelty claim scoped to generative process supervision for OR trajectories.

### Experimental Setup organization
- Benchmarks → baseline taxonomy → implementation details/fairness/solvers → main results → self-evolving-process analysis → inference scaling → ablation.

### Comparative-result reporting
- Reports Pass@1 by benchmark and macro average; compares model scale/categories; distinguishes reproduced vs original published scores and warns when cleaned datasets make scores not directly comparable.

### Ablation-result reporting
- Each variant maps to one component/training stage, followed by benchmark-wise performance and explicit interpretation of which function is lost.

### Academic hedging
- Strong SOTA/novelty rhetoric; methodological interpretation generally tied to ablations and case study. Uses qualifications around non-monotonic behavior and small testing set.

### Novelty-claim strength
- High: explicit `to the best of our knowledge, first` claim, plus SOTA claims. Scope is defined as generative process supervision for OR, not generic LLM optimization.

## Asset Metadata

- FULL TEXT READ: YES
- Source: `LLM/12_StepORLM.md`
- Decision Layer: Verification / process supervision
- Current-study Relation: 支持真实执行结果约束 selector
- Innovation Boundary: 当前不构成候选 selector 机制的直接新颖性反证；已实现范围为 Verification / process supervision，主要用于支持真实执行结果约束 selector。
- Best Writing Claim: 把 solver outcome verification 与过程监督、自进化结合，证明“可验证反馈”应进入 LLM optimization。
