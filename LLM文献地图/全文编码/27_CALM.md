# 27｜CALM 全文编码

- Source: `LLM/27_CALM.md`
- Full-text status: **YES**
- Last read position: **EOF (line >1100 empty); Appendices A–J covered**
- Corpus: LLM / AHD / RL
- Tier: **A（Mechanistically Close）**

## A｜Research Content
- Research problem: fixed-LLM AHD only uses prompt/verbal gradients and wastes performance feedback as model-training signal; CALM asks whether heuristic search and underlying LLM can co-evolve.
- Problem setting: reusable heuristic design for OBP, constructive TSP, ACO-CVRP, ACO-OP.
- Objectives: jointly optimize prompt-generation/evolution process and LLM generator itself using heuristic performance feedback.
- Algorithm backbone: evolutionary heuristic pool + operator-generated prompts + local Qwen2.5-7B-Instruct-INT4 + online GRPO fine-tuning.
- Proposed mechanism: maintain heuristic idea/code/performance pool; select injection/replacement/crossover/simplification/initialization operator; sample G responses; execute/evaluate; derive graded reward; update LLM by GRPO each round; add feasible heuristics; stagnation-driven collapse resets pool to seed + global best.
- Decision layer: **Heuristic/operator generation and LLM-generator adaptation**. Evolutionary operator is sampled by fixed weights/feasibility rules, not learned contextual operator selection.
- State / Context: heuristic pool, rank/performance, idea-token diversity, historical injected component summaries, base heuristics in prompt, stagnation counter, pool size, response feasibility/performance.
- Action / Decision: choose evolutionary operator; sample base heuristic(s); generate prompt; LLM generates idea+code; GRPO changes model parameters; collapse may reset population.
- Feedback / Reward: executable heuristic performance g(h); infeasible hierarchy penalties; feasible reward compares new heuristic to best base heuristic, includes reproduction penalty and relative performance gap.
- Dynamic mechanism: **search-process co-adaptation YES**: LLM weights change on-the-fly; operator feasibility/probability depends on pool state; stagnation counter triggers probabilistic/hard-cap collapse. External dynamic scheduling event: NOT PRESENT.
- LLM role: heuristic generator and continuously fine-tuned search component.
- RL role: **GRPO updates LLM online during heuristic evolution using numerical performance feedback**.
- Claimed contribution: claimed first LLM-AHD framework jointly optimizing prompt generation and LLM model; fine-grained mutation/diversity crossover/collapse; performance-based numerical gradients on compact local model.
- Explicit limitation: reward learning requires explicit heuristics in prompt/response; trajectories without them provide no signal; only compact LLM/single 24GB GPU evaluated due compute cost; larger-scale model/infrastructure evaluation future work.
- 与当前 FJSP-AGV 研究关系: Strong boundary expansion. `performance feedback → online learning → generator adaptation`, `stagnation detection → structural reset`, component-level descriptions/memory, instance-dependent rewrite, context-dependent credit differentiation, and search-process co-evolution already exist. Therefore “LLM根据反馈自己学/停滞时重新设计”本身也不能作为创新。Potential remaining distinction must be much narrower: context-specific operator competence/effect modelling tied to dynamic FJSP-AGV and Pareto/bottleneck/search context, with explicit predicted-vs-realized multidimensional effects and coverage-gap diagnosis rather than generic performance-driven generator fine-tuning/reset.

## B｜Experimental Design Coding
- Dataset / Benchmark: OBP, TSP, CVRP, OP using same datasets/protocols as MCTS-AHD/HSEvo where stated.
- Instance scale: OBP four training instances and five testing instances spanning six scales; TSP train 64×N=50, test 3×1000 at N=50/100/200; CVRP train 10×N=50, test 3×64 at N=50/100/200; OP train 5×N=50, test 3×64 at N=50/100/200.
- Baselines: hand-crafted Best-Fit/First-Fit/Greedy Construct/ACO; NCO POMO/DeepACO; LLM-AHD FunSearch, EoH, ReEvo, HSEvo, MCTS-AHD; EvoTune where possible.
- Baseline 数量: varies by task; no one global count. LLM-AHD named comparator family contains **6** external methods including EvoTune, though not all appear in every table.
- Independent runs: **3**, including main tables and training curves/ablations.
- Random seeds: numeric seeds **NOT REPORTED**.
- Population size: exact Lp numeric value **NOT REPORTED** in read text.
- Generations / rounds: **T=500** CALM rounds; G=4 responses/prompt.
- Evaluation budget: baselines 1000 heuristic evaluations; CALM fixed **2000 LLM queries** for all tasks except wording notes OBP prior methods use >4000 queries while CALM stays 2000; verbal-only API CALM uses T=4000 OBP, 2000 others with G=1.
- Fitness / function evaluations: baseline 1000; CALM governed by query/response execution, exact real-evaluation count can vary and is **NOT REPORTED as a single fixed count**.
- Real decoding count: up to G=4 per round × T=500 = budget structure 2000 responses/queries; actual feasible heuristics vary.
- Solver calls: heuristic evaluation environment executes candidates; exact aggregate solver/evaluator calls NOT REPORTED.
- LLM calls: **2000-query fixed budget** for CALM main setting; API verbal variant as above.
- Token budget: **NOT REPORTED**.
- Runtime / wall-clock: average CALM runtime OBP 6.8h, CVRP 7.2h, OP 5.3h, TSP 5.5h for T=500; heuristic eval timeout 60s.
- Hardware: NVIDIA A30 24GB + Intel Xeon Gold 5220R CPU; INT4 Qwen2.5-7B, 1.15% weights fine-tuned.
- Metrics: objective and optimality gap; training best-objective curves with std shading.
- Statistical tests: **NOT REPORTED**.
- Confidence interval: **NOT REPORTED**.
- Ablation: local w/GRPO vs API/no GRPO vs local/no GRPO; two alternative reward designs; no collapse; four δ0/C collapse settings; w/o diversity; w/o crossover/injection/replacement/simplification.
- Sensitivity analysis: collapse δ0/C variants; yes. Other GRPO hyperparameter sensitivity NOT PRESENT.
- Generalization / OOD: explicit train N=50 → test N=100/200 for TSP/CVRP/OP; OBP includes OOD scales.
- Robustness: three-run averages; stochastic runtime variability acknowledged; no formal robustness stress test.
- Dynamic-event design: NOT PRESENT. OBP is online sequential arrival but not exogenous rescheduling event design analogous machine/AGV failures.
- LLM API / inference cost: monetary cost NOT REPORTED; emphasizes local single-GPU avoidance of commercial APIs.
- GRPO learning rate: 5e-5; G=4; δ0=0.0005; C=25; operator sampling ratio simplification:injection:modification:crossover = 1:1:2:4.
- ACO CVRP: 30 ants ×100 iterations; OP 20 ants ×50 iterations.

## C｜Writing Evidence Coding
### Introduction
Actual sequence: **M1 real optimization/manual heuristics → M3 classic AHD limitation → M3 LLM-AHD paradigm → M4 fixed LLM/verbal-gradient limitation → M6 CALM co-evolution/numerical gradient → M6 operator/collapse/GRPO details + strong novelty → empirical headline**.
- Limitation first appears in paragraph 1 for classic AHD; LLM-specific limitation paragraph 2.
- Method appears paragraph 3 with `We propose... CALM to capture this opportunity`.
- Formal contribution list: **NOT PRESENT** as separate bullets; contribution claims integrated into prose.
- Empirical diagnosis before method: NO; limitation is conceptual/mechanistic.

### Related Work
- Organized by **role/decision layer**, unusually useful for this audit: RL for Optimization → (1) Instance-Level Solution Generator vs (2) Heuristic Generator; LLM for Optimization → same two categories. Appendix adds LLM code generation + RL fine-tuning.
- taxonomy/method family: YES.
- direct solving vs algorithm design: **explicit central distinction**.
- generation vs selection: not main taxonomy.
- static vs adaptive: fixed LLM vs continuously fine-tuned LLM is explicit gap.
- offline vs online: not named taxonomy, but on-the-fly adaptation is central.

### Gap language
- Uses `Nevertheless` to transition classic/LLM AHD limitations.
- `Consequently, these methods inherently neglect the opportunity...` converts limitation to opportunity rather than claiming absence broadly.
- `Our approach improves this by...`; direct comparison to very recent EvoTune then enumerates four differences, an important competitor-aware gap-writing pattern.
- Strong novelty: `CALM is the first LLM-based AHD framework that jointly optimizes both the prompt generation process and the LLM model itself.`

### Contributions
- Separate numbered list: **NO**.
- Method contribution: co-evolution framework, operators, collapse, reward/GRPO integration.
- Formulation contribution: reward formulation and collapse expectation approximation.
- Experimental contribution: compact local model vs stronger API baselines, OOD scales, ablations.
- Benchmark contribution: NO.
- Empirical finding contribution: RL produces largest ablation impact; verbal-only CALM remains competitive.

### Experimental writing
- Setup begins with implementation/model-resource constraints, then explains why chosen tasks are deliberately challenging rather than saturated benchmarks, then baseline taxonomy/fairness budgets.
- Fairness explicitly distinguishes **heuristic-evaluation budget** for baselines from **LLM-query budget** for CALM instead of pretending these are identical units.
- Overall Results is problem-by-problem with train/test scale details immediately after tables.
- A dedicated Discussion section decomposes efficacy of verbal gradient, power of RL, reward design, collapse and operators; Table 4 centralizes mechanism ablations.
- Generalization language explicitly labels in-domain/OOD scales.
- Statistical significance tests: absent; three-run averages/std used instead.
- Computational cost: hardware, quantization, trainable fraction, query budget, 60s evaluation timeout and task-level wall-clock all reported; monetary API cost absent.

## Asset Metadata

- FULL TEXT READ: YES
- Source: `LLM/27_CALM.md`
- Decision Layer: Co-evolution / feedback
- Current-study Relation: 混合反馈参考
- Innovation Boundary: 当前不构成候选 selector 机制的直接新颖性反证；已实现范围为 Co-evolution / feedback，主要用于混合反馈参考。
- Best Writing Claim: 让算法与底层 LLM 共同进化，并混合 prompt feedback 与 RL numerical feedback。
