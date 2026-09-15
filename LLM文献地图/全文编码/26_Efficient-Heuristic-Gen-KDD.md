# 26｜Hercules / Efficient Heuristics Generation 全文编码

- Source: `LLM/26_Efficient-Heuristic-Gen-KDD.md`
- Full-text status: **YES**
- Last read position: **EOF (line >720 empty); Appendices A–G covered**
- Corpus: LLM / Hyper-Heuristic / AHD
- Tier: **A（Mechanistically Close）**

## A｜Research Content
- Research problem: LLM-based heuristic generation 的两个成本/质量瓶颈：搜索方向缺乏 task-specific specificity；大量语义等价候选仍需真实 COP fitness evaluation。
- Problem setting: four HG tasks across TSP/CVRP/BPP/MKP/OP and NCO attention reshaping.
- Objectives: improve generated heuristic quality while reducing expensive real evaluations/search time.
- Algorithm backbone: EC-style population heuristic generation based on EoH/ReEvo crossover/mutation + rank-based parent selection + CAP; Hercules-P adds LLM performance prediction.
- Proposed mechanism: CAP abstracts core components from top-k elite heuristics and uses them as prior knowledge to produce specific search directions. PPP predicts new heuristic fitness from semantic similarity to previously evaluated examples; EXEMPLAR selects informative examples; ConS uses LLM confidence to decide prediction acceptance vs real reevaluation.
- Decision layer: **Operator/heuristic generation + heuristic performance prediction/evaluation gating**. Not runtime scheduling decision or online operator selection.
- State / Context: current heuristic population, elite/parent heuristic code, fitness ranks, historical evaluated heuristics, core components, predicted fitness/confidence, iteration phase.
- Action / Decision: select parents; abstract components; produce search direction; crossover/mutate heuristic code; predict fitness; choose prediction acceptance or real COP evaluation.
- Feedback / Reward: real fitness F(x) on COP training instances; predicted fitness ξ and confidence φ; rank-based population update.
- Dynamic mechanism: search-process phase adaptation: first λ fraction uses elite-core abstraction, later uses parent components to preserve diversity; ConS acceptance count decays over iterations. External dynamic scheduling event: NOT PRESENT.
- LLM role: abstraction, search-direction generation, heuristic code generation, semantic fitness prediction/confidence.
- RL role: **NOT PRESENT** in Hercules/Hercules-P.
- Claimed contribution: zero-shot CAP with information-gain argument; first claimed LLM performance predictor PPP for HG; EXEMPLAR+ConS; resource-efficient Hercules-P.
- Explicit limitation: no dedicated Limitations section. Text acknowledges PPP prediction can be inaccurate/moderately correlated, some candidates require real reevaluation, LLM choice strongly affects results, NCO domain knowledge can be insufficient; future work proposes beam-search integration to improve PPP.
- 与当前 FJSP-AGV 研究关系: Important boundary evidence. `operator capability abstraction from elite heuristics`, `historical performance as context`, `LLM-predicted candidate performance`, `confidence-aware real-evaluation gating`, and iteration-dependent adaptation already exist. Therefore a competence model cannot be novel merely because it stores operator descriptions/performance or predicts effects. Current candidate must distinguish **context-conditioned multidimensional competence under dynamic FJSP-AGV + predicted-vs-realized effect vectors + context-region coverage gap + targeted redesign**, if corpus evidence ultimately supports it.

## B｜Experimental Design Coding
- Dataset / Benchmark: four HG tasks; TSP, CVRP, BPP, MKP, OP; TSPLIB; NCO POMO/LEHD tasks; 49-node US capitals case study.
- Instance scale: TSP 100/200 and TSPLIB 18 instances; BPP/MKP 120/500/1000; NCO TSP/CVRP 200/500/1000; exact all training/test instance counts delegated to prior study [53], therefore **NOT REPORTED in this paper text as a complete count**.
- Baselines: Random, EoH, ReEvo; seed algorithms/functions KGLS, GP constructive seed, ACO, DAR/POMO/LEHD depending task.
- Baseline 数量: core LLM-HG comparator set = **3** excluding ours; underlying seed varies by task.
- Independent runs: **3** for LLM-based HG performance unless otherwise specified; EXEMPLAR predictive-accuracy experiment **10 runs**.
- Random seeds: **NOT REPORTED**.
- Population size: **15**.
- Generations: exact T not numerically reported in Table 8; maximum **100 fitness evaluations**. λ=0.7 controls early/late phase.
- Evaluation budget: max number of evaluations **100**.
- Fitness / function evaluations: max **100**.
- Real decoding count: NOT REPORTED.
- Solver calls: NOT REPORTED.
- LLM calls: NOT REPORTED as aggregate.
- Token budget: context/generation token consumption measured per compared search in Table 2; no universal hard total token budget reported. Example TSP GPT-4o-mini: Hercules 95.8k context/33.3k generation; Hercules-P 143.4k/31.2k.
- Runtime / wall-clock: search time explicitly reported; examples range from ~9.51 min to hundreds of minutes depending NCO scale; Hercules-P reduces search time 7%–59% vs Hercules.
- Hardware: Intel Xeon W-2235 CPU.
- Metrics: Gain %, task-specific objective/gap; search time; context/generation tokens; PPP prediction accuracy; Pearson correlation.
- Statistical tests: EXEMPLAR analysis: significance p=0.048 and p=0.004 for median accuracy comparisons (specific named test for these pairwise median comparisons NOT REPORTED in visible text); **one-way ANOVA p=0.6** for predicted-vs-true mean difference; Pearson correlation coefficient **0.39**.
- Confidence interval: **NOT REPORTED**.
- Ablation: w/o CAP; w/o rank-based selection; λ variants 0.5/0.9/1 vs 0.7; w/o ConS; w/o EXEMPLAR; δ variants 0.2/0.3 vs 0.1; EXEMPLAR-U; PPP accuracy analysis.
- Sensitivity analysis: λ and δ variants; yes, embedded in Table 7.
- Generalization / OOD: four HG tasks, five COPs, eight LLMs; train/test split; TSPLIB; small→large NCO scales; black-box vs white-box CVRP; real-world TSP case.
- Robustness: 3-run mean/std; 10-run prediction analysis; cross-LLM and cross-task evaluation.
- Dynamic-event design: **NOT PRESENT**.
- LLM API / inference cost: token counts and search time reported; monetary API cost **NOT REPORTED**.
- LLM temperature: 1; initial phase +0.3 for diversity.
- CAP k=5, λ=0.7; crossover=1, mutation=0.5; ConS δ=0.1, α=0.5, β=0.8.

## C｜Writing Evidence Coding
### Introduction
Actual sequence: **M1 heuristics/COP + HG → M3 EC-HG → M3 LLM-HG/EoH/ReEvo → M4 two explicit challenges → M6 Hercules/CAP → M6 Hercules-P/PPP+EXEMPLAR+ConS → empirical headline → M7 3 numbered contributions**.
- Limitation first appears: after existing LLM-HG mechanism is explained, as an explicit two-challenge paragraph.
- Method appears immediately after the two challenges with `To better address the first challenge...` then `To better address the second challenge...`.
- Contribution count: **3**, Roman-numbered i–iii.
- Empirical diagnosis before method: YES in lightweight form via Figure 1/2 concrete examples of vague directions and semantically equivalent heuristics, before proposing CAP/PPP.

### Related Work
- Organized by **method family**: LLM-based Heuristic Generation; LLM-based Performance Prediction; Neural Combinatorial Optimization Solvers.
- chronological: secondary.
- traditional→LLM: YES within 2.1.
- generation vs selection: not main taxonomy; focus generation/prediction.
- direct solving vs solver-assisted: NCO section distinguishes independent/collaborative solvers but not central taxonomy.
- single heuristic vs portfolio: NOT central.
- static vs adaptive: search phase adaptation appears in method, not RW organization.
- offline vs online: NOT central RW taxonomy.

### Gap language
- Limitation uses `However` repeatedly to isolate unspecificity and expensive reevaluation.
- Contrast uses `In contrast` for conventional EC vs LLM HG and Hercules vs prior RP.
- Motivation/transition: `To better address the first challenge...`; `To better address the second challenge...`; `Motivated by this concept...`.
- Strong novelty: `To the best of our knowledge, our work proposes the first LLM-based performance predictor for the HG task.` This is narrowly scoped to PPP rather than entire HG framework.

### Contributions
- Count: **3**; numbered: YES.
- Verbs: `We propose`, `we develop`, `experimental results demonstrate`.
- Method contribution: CAP, PPP, EXEMPLAR, ConS.
- Formulation/theory contribution: information-gain proof for CAP.
- Experimental contribution: cross-task/COP/LLM SOTA + efficiency + ablation.
- Benchmark contribution: NO.
- Empirical finding: performance/resource results included in contribution iii.

### Experimental writing
- Main Results is task-by-task rather than one global experiment section: GLS-TSP → constructive TSP → ACO multiple COPs → NCO → ablation.
- Baselines are introduced at first relevant task and tied to prior study [53]; fairness uses same crossover/mutation and seed configurations.
- Results report both quality and computational-resource metrics, especially tokens/search time.
- Ablation maps each named mechanism directly to a controlled removal/parameter variant and then adds a 10-run prediction-quality experiment for meaningful statistical analysis.
- Generalization is argued across task types, COPs, LLMs, sizes, TSPLIB, NCO and black-box/white-box settings rather than one dedicated OOD heading.
- Statistical writing reports exact p-values and Pearson coefficient where prediction quality is specifically investigated, but no global significance test over all optimization tables.
- Computational-cost writing is central to the paper's claim, with search minutes and context/generation tokens reported alongside gain.

## Asset Metadata

- FULL TEXT READ: YES
- Source: `LLM/26_Efficient-Heuristic-Gen-KDD.md`
- Decision Layer: Performance prediction
- Current-study Relation: 支持预算与真实评价成本控制
- Innovation Boundary: 当前不构成候选 selector 机制的直接新颖性反证；已实现范围为 Performance prediction，主要用于支持预算与真实评价成本控制。
- Best Writing Claim: 用 core abstraction 与 performance prediction 降低昂贵 heuristic evaluation，是评价成本控制的关键证据。
