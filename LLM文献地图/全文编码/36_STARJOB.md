# 36｜Starjob: Dataset for LLM-Driven Job Shop Scheduling 全文编码

- Source: `LLM/36_STARJOB.md`
- Full-text status: **YES**
- Last read position: **EOF (line >400 empty); no appendix present**
- Corpus: LLM / Scheduling / JSSP
- Tier: A（Mechanistically close scheduling boundary）

## A｜Research Content
- Research problem: end-to-end JSSP scheduling with a fine-tuned LLM and lack of supervised JSSP data suitable for LLM training.
- Problem setting: static JSSP; natural-language problem description → generated full schedule; objective makespan minimization under precedence/machine constraints.
- Objectives: create a large supervised dataset; fine-tune Llama to generate feasible/high-quality schedules; test generalization to standard larger JSSP benchmarks.
- Algorithm backbone: Starjob supervised dataset generated with OR-Tools labels + 4-bit Llama-3.1-8B-Instruct + rsLoRA fine-tuning + inference sampling + explicit feasibility validator + best-feasible-makespan selection.
- Proposed mechanism: convert matrix JSSP to natural language; generate feasible solver labels; supervised autoregressive fine-tuning; sample `S=20` complete schedules; validate all constraints and choose minimum-makespan feasible output.
- Decision layer: **Scheduling decision / direct end-to-end schedule generation**. The LLM outputs complete operation timings/order rather than selecting operators/heuristics.
- State / Context: full natural-language JSSP instance (jobs, machines, processing times/sequence); no search-process state.
- Action / Decision: generate a complete schedule representation; at outer inference layer select best feasible of 20 candidates.
- Feedback / Reward: supervised NLL during training; no online optimization feedback at inference. Feasibility/makespan used post-generation for filtering/selection.
- Dynamic mechanism: NOT PRESENT; static JSSP only.
- LLM role: direct scheduler trained by supervised fine-tuning.
- RL role: NOT PRESENT in proposed method; L2D PPO is a baseline.
- Claimed contribution: Starjob ~130k supervised JSSP dataset; fine-tuned LLM end-to-end scheduling; benchmark comparison vs four PDRs + L2D; natural-language interaction/transparency.
- Explicit limitation: dedicated `Limitations and Future Work` is brief and proposes advanced sampling, more LLM architectures, RL/GNN integration. Elsewhere: OR-Tools labels for `NJ>10,NM>10` are not guaranteed optimal due 300s cap; zero-shot/prompt engineering failed; 40k context limits scale; inference can be slow (~217.41s/sample at largest tested token length).
- 与当前 FJSP-AGV 研究关系: direct scheduling boundary evidence. LLM direct scheduling for static JSSP already exists, including best-of-N sampling, feasibility validation and makespan-based selection. Therefore current work should not position itself as `LLM for scheduling` or `LLM-generated schedules`; its LLM role is instead supervisory operator/strategy control inside an optimizer, with dynamic AGV/machine events and multiobjective Pareto search.

## B｜Experimental Design Coding
- Dataset / Benchmark: Starjob training data; Taillard (TAI); DMU.
- Instance scale: training ~130,000 random JSSP instances, mainly `2×2` to `20×20`, operation duration 5–500; ~1,000 larger/asymmetric examples incl. `30×15`, `50×20`; benchmark scales TAI 15×15 to 50×20; DMU 20×15 to 50×15 in table.
- Baselines: SPT, MWKR, MOPNR, FDD/MWKR, L2D.
- Baseline 数量: **5** (4 PDR + 1 DRL/GNN neural method).
- Independent runs: NOT REPORTED for benchmark method comparison.
- Random seeds: NOT REPORTED.
- Population size: NOT APPLICABLE.
- Generations: NOT APPLICABLE.
- Evaluation budget: inference sample size **S=20 outputs/instance**; OR-Tools label generation max **300s/problem**, 42 workers.
- Fitness / function evaluations: NOT REPORTED.
- Real decoding count: 20 schedule generations per benchmark instance.
- Solver calls: OR-Tools used for dataset label generation; total calls roughly per generated instance but exact completed-call count NOT REPORTED.
- LLM calls: inference generates 20 outputs per instance; aggregate call count NOT REPORTED.
- Token budget: context length **40k** train/inference; largest tested instance ~22,224–23,000 tokens.
- Runtime / wall-clock: fine-tuning ~**70 h**; largest instance ~**217.41 s/sample** at cited 102.22 tokens/s llama.cpp A6000 benchmark; inference runtime otherwise not comprehensively measured.
- Hardware: single **NVIDIA A6000**, ~30GB memory training/inference; 4-bit model.
- Metrics: Percentage Gap to best-known makespan; makespan/feasibility; average gap by size.
- Statistical tests: NOT REPORTED. Text uses `significantly lower` colloquially, without a statistical test.
- Confidence interval: NOT REPORTED.
- Ablation: no formal component ablation. Representation comment compares with/without summation operation qualitatively, but numeric ablation NOT REPORTED.
- Sensitivity analysis: NOT PRESENT.
- Generalization / OOD: train mostly ≤20×20 plus some larger examples; evaluate TAI/DMU up to 50×20 / graph ~1000 nodes.
- Robustness: feasibility validator; repeated stochastic benchmark runs NOT REPORTED.
- Dynamic-event design: NOT PRESENT.
- LLM API / inference cost: open-source local model; monetary inference cost NOT REPORTED.

## C｜Writing Evidence Coding
### Introduction
Actual sequence: **M4 prevailing limitation/perception of LLMs for NP-hard CO → M6 challenge claim + proposed fine-tuned JSSP LLM → M2 JSSP definition/application → M3 traditional/RL/graph/LLM background → M5 scheduling application gap → M6 Starjob+rsLoRA → M7 four bullet contributions**.
- Limitation begins immediately in paragraph 1.
- Method/proposal appears paragraph 2 and is restated after JSSP/background.
- Contributions: **4**, bulleted.
- Empirical diagnosis before method: NO.
- Novelty strength: unusually strong, including `first fine-tuned LLM model for JSSP` and `to the best of our knowledge, for any NP-hard combinatorial problem`; these are author claims and should not be generalized beyond this paper.

### Related Work
- Organization: traditional JSSP/search/PDR → deep learning/DRL → LLM mathematical/optimization/graph reasoning.
- traditional→learning→LLM: YES.
- generation vs selection: NO.
- direct solving vs solver-assisted: not formal taxonomy.
- single heuristic vs portfolio: NO.
- static vs adaptive / offline vs online: NO.

### Gap language
- Introduction: `despite`, `limited`, `lack of examples`, `Consequently`, `remains unexplored` build a strong novelty narrative.
- `To address this` introduces prompting work in cited graph literature; own transition uses `To this end, we introduce...`.
- Related Work repeats `currently no papers that directly address...` and `remains largely unexplored`.
- This paper is a useful example of **strong novelty wording that requires historical/date-scoped interpretation**, not a reusable corpus fact.

### Contributions
- Count: **4**, bullets.
- Method: fine-tuned end-to-end LLM scheduler.
- Formulation: NO.
- Experimental: TAI/DMU comparison/generalization.
- Benchmark/dataset: YES, Starjob dataset.
- Empirical finding: fine-tuned model outperforms listed PDRs/L2D on reported gap tables.
- Usability contribution: natural-language interaction/transparency.

### Experimental writing
- Dataset generation/training details precede Evaluation, making data provenance part of methodology.
- Fairness rationale explicitly explains why L2D was chosen as neural comparator, but no compute-budget equivalence is established across methods.
- Baseline taxonomy is simple: four PDRs + one early neural DRL method.
- Results report per-size and average Percentage Gap; no variance, repeated-run statistics, significance tests or CI.
- Computational feasibility is unusually concrete: quantization, GPU memory, training hours, context length, token length and estimated per-sample inference time.
- Limitations section is brief; several more consequential limitations are disclosed earlier in method/evaluation rather than there.
