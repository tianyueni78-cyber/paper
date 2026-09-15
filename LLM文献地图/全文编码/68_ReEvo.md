# 68｜ReEvo 全文编码

- Source: `LLM/68_ReEvo.md`
- Full-text status: **YES**
- Last read position: **EOF (line >1240 empty); Appendices A–F covered**
- Corpus: LLM / Language Hyper-Heuristic / AHD
- Tier: S/A direct mechanism competitor

## A｜Research Content
- Research problem: automate open-ended heuristic design for COPs while improving sample efficiency and reasoning, including black-box settings.
- Problem setting: LHH takes COP/task specification and searches an LLM-generated open-ended heuristic code space; meta-objective is expected heuristic performance over problem instances.
- Objectives: define Language Hyper-Heuristics; develop Reflective Evolution; apply across heterogeneous algorithm types/COPs; improve evaluation reliability/sample efficiency.
- Algorithm backbone: genetic-programming-style evolutionary search over heuristic code + generator LLM + reflector LLM.
- Proposed mechanism: initialization → selection → short-term reflection on relative parent performance → reflection-conditioned crossover → long-term reflection accumulating experience → elitist mutation conditioned on accumulated reflection; evaluate crossover/mutation heuristics.
- Decision layer: **Operator/heuristic generation and optimizer design**, not online operator selection during a single downstream search trajectory.
- State / Context: task specification, seed heuristic, parent/elite code, relative/meta-objective performance, short-term reflections, accumulated long-term reflection; black-box variant hides COP semantics.
- Action / Decision: generate new heuristic code through crossover/mutation; reflector produces verbal design gradients.
- Feedback / Reward: evaluated meta-objective F and relative performance between heuristics; short-term comparative feedback is verbalized, then distilled into long-term memory.
- Dynamic mechanism: evolutionary feedback changes generation context across heuristic-design iterations; long-term reflection accumulates experience. This is design-time adaptation, not external dynamic scheduling response.
- LLM role: generator and reflector.
- RL role: no learned RL in ReEvo; verbal feedback is discussed analogically as verbal RL.
- Claimed contribution: LHH concept; ReEvo reflective evolutionary search; fitness-landscape analysis and black-box prompting; applications across five algorithmic types/six COPs.
- Explicit limitations: results capped at 100 heuristic evaluations may not scale to large budgets; rule-based LHH may underfit complex environments; reflection depends on capable LLMs; benchmark cost accounting is nontrivial.
- 与当前 FJSP-AGV 研究关系: **major novelty boundary**. Relative heuristic performance → short-term reflection → accumulated long-term experience → targeted generation of improved heuristics is already explicit. It also directly evolves GA crossover/mutation operators. Thus “historical operator effect + reflection + redesign” is not new. Remaining distinction must concern online selection among a portfolio under joint dynamic environment/search/Pareto context and an explicit empirical context-conditioned competence/effect model, not reflective AHD itself.

## B｜Experimental Design Coding
- Dataset / Benchmark: TSP, CVRP, OP, MKP, BPP, DPP; TSPLIB; DPP test set; synthetic DeepACO-style instances; NCO generalization tests.
- Instance scale: varied up to TSP/CVRP/OP/BPP 1000; MKP up to 1000; DPP 10×10 PDN. Each ReEvo run generally selects best validation heuristic then tests on **64 held-out instances**.
- Baselines: problem-specific. Includes EoH as direct LHH competitor; expert GLS/ACO/GA/constructive heuristics; NeuOpt/GNNGLS/NeuralGLS; DeepACO; DevFormer and RL DPP methods; GHPP; POMO/LEHD/DAR.
- Baseline 数量: varies by downstream experiment; no single corpus-wide count appropriate.
- Independent runs: **3 ReEvo runs per COP setting** unless otherwise stated; EoH/ReEvo comparisons 3 runs/setting; landscape analysis 3 runs; TSP constructive 3 starting-node runs.
- Random seeds: NOT REPORTED as numeric seed.
- Population size: ReEvo **10**; initial generation **30**. DPP downstream GA population 20, elite 4. ACO downstream population varies 10–30.
- Generations: ReEvo controlled by max evaluations rather than a single reported generation count; DPP downstream GA uses 10 iterations during training evaluation.
- Evaluation budget: **maximum 100 heuristic evaluations** for standard ReEvo runs. Landscape random walk 3×40 heuristics.
- Fitness/function evaluations: heuristic evaluation is principal budget; downstream solution-evaluation counts depend on COP/solver.
- Real decoding count: NOT REPORTED.
- Solver calls: NOT APPLICABLE/NOT REPORTED aggregate.
- LLM calls: not used as primary budget; aggregate NOT REPORTED.
- Token budget: NOT REPORTED as cap; discussion explicitly argues token usage is a better inference-cost driver than query count.
- Runtime/wall-clock: one ReEvo run ~2 minutes to hours depending on evaluation/hardware; LHH evolution often described as <100 evaluations/about 5 minutes in representative settings.
- Hardware: runtime comparison single **AMD EPYC 7742 CPU core + RTX 3090 GPU**.
- Metrics: objective/optimality gap, execution time, relative improvement, best objective over evaluations, correlation length, mean±std, downstream task metrics.
- Statistical tests: NOT REPORTED as formal named test for main comparisons; discussion references statistical significance limitations of reflection literature but does not supply a corpus-wide test here.
- Confidence interval: NOT REPORTED.
- Ablation: LLM-only; w/o long-term reflection; w/o short-term reflection; w/o crossover; w/o mutation; white-box vs black-box.
- Sensitivity analysis: fitness landscape/random-walk mechanism analysis; different LLMs; problem sizes/distribution shifts. No conventional parameter sweep over population/rates reported in main coding.
- Generalization/OOD: strong emphasis: same ACO heuristic trained/evolved at smallest size applied up to 1000; NCO trained on 100 applied to 200/500/1000; black-box prompts; multiple distributions.
- Robustness: cross-LLM comparisons GPT-3.5 Turbo/GPT-4 Turbo/Llama3-70B; black-box settings.
- Dynamic-event design: NOT PRESENT.
- LLM API/inference cost: about **$0.06 per ReEvo run using GPT-3.5 Turbo**; average stated ~**$0.0003/call**, asynchronous/batched response under 1 s average in discussion.

## C｜Writing Evidence Coding
### Introduction
Actual sequence: **M1 COP importance/heuristic-design burden → M3 classic HH → M4 predefined human heuristic-space limitation → M6 LHH concept → M4 pure-LHH sample inefficiency/black-box weakness → M6 ReEvo → empirical application preview → M7 three numbered contributions**.
- Limitation appears very early, first for classic HH and then for vanilla LHH.
- Method follows each limitation immediately.
- Contributions: **3 numbered items**.
- Empirical diagnosis before method: NO; conceptual limitation precedes method.

### Related Work
- Standalone Related Work organized by method families: Traditional HH → NCO → LLM code/optimization → LLM self-reflection.
- Explicitly positions concurrent EoH and FunSearch and distinguishes ReEvo by sample efficiency, applications and evaluation methodology.
- Appendix A.1 provides an unusually direct competitor comparison with EoH across search algorithm, applications and evaluation methodology.

### Gap language
- Strong contrast structure: classic HH has predefined spaces; LLM opens them; pure LHH is inefficient/weak on black-box problems; reflective evolution addresses this.
- Gap is therefore built as **successive mechanism limitations**, not simply “few studies”.
- Uses `Despite`-style conceptual contrast less than direct declarative limitation statements.

### Contributions
- Count: **3**, explicitly numbered.
- Concept/formulation contribution: LHH.
- Method contribution: ReEvo + evaluation methods.
- Experimental/application contribution: five algorithmic types/six COPs and SOTA/competitive solvers.

### Experimental writing
- Experiments are organized first by downstream application, then a dedicated Section 6 evaluates the proposed search mechanism itself.
- Fairness: direct EoH comparison explicitly follows original EoH code/hyperparameters and uses a common 100-evaluation framing.
- Mechanism evidence goes beyond endpoint performance: fitness-landscape correlation length is used to test the claim that reflection smooths/structures the search neighborhood.
- Ablation removes each reflective/evolutionary component in both white- and black-box settings.
- Generalization is written as size/distribution transfer of the same evolved heuristic, not just another benchmark table.
- Cost discussion explicitly argues why heuristic evaluations, rather than raw LLM query count, should be the primary AHD budget.

## Asset Metadata

- FULL TEXT READ: YES
- Source: `LLM/68_ReEvo.md`
- Decision Layer: Heuristic generation / reflection
- Current-study Relation: AHD演进关键点
- Innovation Boundary: 当前不构成候选 selector 机制的直接新颖性反证；已实现范围为 Heuristic generation / reflection，主要用于AHD演进关键点。
- Best Writing Claim: Language Hyper-Heuristic + reflective evolution + verbal gradient，是“性能反馈转语言反思再改 heuristic”的代表。
