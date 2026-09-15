# 69｜Evolution of Heuristics (EoH) 全文编码

- Source: `LLM/69_EoH.md`
- Full-text status: **YES**
- Last read position: **EOF (line >1060 empty); Appendices A–D and detailed TSP/FSSP experiments covered**
- Corpus: LLM / Hyper-Heuristic / AHD
- Tier: S/A foundational direct competitor

## A｜Research Content
- Research problem: automate heuristic design without relying on manually defined primitives/components while using LLM+EC more efficiently than large-scale program search.
- Problem setting: evolutionary search over heuristics, each represented jointly by natural-language thought, executable code and fitness over an instance set.
- Objectives: evolve high-quality heuristics with few thousand LLM queries; test across online bin packing, TSP and flow-shop scheduling.
- Algorithm backbone: population-based evolutionary framework + five LLM prompt strategies.
- Proposed mechanism: initialize LLM-generated heuristics; repeatedly select ranked parents; E1/E2 exploration and M1/M2/M3 modification prompts generate thought+code; execute/evaluate each feasible heuristic; elitist population management retains N best.
- Decision layer: **Heuristic/operator generation and optimizer design**. In TSP/FSSP it designs GLS landscape/perturbation heuristics; not online selector among a fixed portfolio.
- State / Context: parent heuristic thoughts+codes+fitness/rank; task description; for downstream generated FSSP heuristic, current sequence/time matrix/m/n are runtime inputs.
- Action / Decision: generate/modify heuristic thought+code; E1 diversity, E2 common-idea recombination, M1 general modification, M2 parameter modification, M3 simplification.
- Feedback / Reward: heuristic fitness measured by executing downstream algorithm over an instance set; rank biases parent selection. No explicit learned reward model.
- Dynamic mechanism: design-time evolution conditioned on previous heuristic population/performance; generated FSSP heuristic itself reacts to current schedule/time matrix but the EoH controller is not online AOS.
- LLM role: generates high-level heuristic thoughts and executable code, performs crossover-like reasoning/modification.
- RL role: NOT PRESENT in EoH; neural RL methods appear only as baselines/background.
- Claimed contribution: EoH thought+code co-evolution; five prompt strategies; evaluation across three COPs with better performance/sample efficiency than prior AHD/FunSearch in reported settings.
- Explicit limitation/future boundary: domain-specific pretrained LLMs, theoretical understanding of heuristic search space and human-expert interaction remain future work; area described as early-stage.
- 与当前 FJSP-AGV 研究关系: **foundational novelty constraint**. EoH already designs scheduling perturbation/landscape heuristics for FSSP from current sequence and time matrix, and uses historical population performance/rank to evolve operators. Thus LLM-designed scheduling operators, thought+code operator evolution, performance-conditioned redesign and local-search landscape adaptation are occupied. It still lacks dynamic FJSP-AGV external events, multiobjective Pareto state, fixed-portfolio online operator selection and explicit context-conditioned empirical competence/effect learning.

## B｜Experimental Design Coding
- Dataset / Benchmark: online bin packing Weibull; synthetic TSP + TSPLIB; synthetic FSSP + Taillard.
- Instance scale: bin packing evolution 5 Weibull instances size 5k C=100; tests sizes 1k/5k/10k C=100/500, 5 instances/set. TSP evolution 64 TSP100; random test 1000 instances each for n=20/50/100 plus 29 TSPLIB. FSSP evolution 64 random 50-job, 2–20 machine instances; Taillard sets 20–200 jobs, 5–20 machines, 10 instances/set.
- Baselines: problem-specific. Bin packing First Fit, Best Fit, FunSearch. TSP NI/FI, OR-Tools, AM, POMO, LEHD plus extended Concorde/LKH3/NN/GCN/BQ/LS/GLS/EBGLS/KGLS/GNNGLS/NeuralGLS. FSSP GUPTA, CDS, NEH, NEHFF, PFSPNet/PFSPNet-NEH plus extended LS/ILS1/ILS2.
- Baseline 数量: varies by experiment; direct bin packing main comparison 3; TSP/FSSP larger benchmark sets contain many more.
- Independent runs: discussion studies (thought/code variants, different LLMs, expert seed) explicitly **3 runs**. Main benchmark generation run count is NOT REPORTED as a uniform value.
- Random seeds: NOT REPORTED.
- Population size: bin packing **20**; TSP/FSSP **10**.
- Generations: **20** standard EoH generations; ablation variants adjust generations so total evaluated heuristics are equal.
- Evaluation budget: each generation can produce up to 5N new heuristics; online bin packing standard run reports **2,000 LLM queries** in 20 generations. Exact feasible/evaluated heuristic count can be lower because infeasible outputs are filtered; aggregate real evaluations NOT uniformly reported.
- Fitness/function evaluations: downstream instance-set execution for each heuristic. TSP/FSSP GLS max local-search iterations **1000**, max runtime 60s/instance.
- Real decoding count: NOT REPORTED.
- Solver calls: Concorde generates TSP optimum/baseline; OR-Tools used in comparison; aggregate solver calls NOT REPORTED.
- LLM calls: standard online bin packing evolution **2,000**; random GPT3.5 sampling comparator **10,000**; FunSearch described as orders of magnitude larger/millions but use exact source-specific values only where table/text supports.
- Token budget: NOT REPORTED.
- Runtime/wall-clock: 60s/instance max for TSP/FSSP local search; TSP extended table reports per-instance times. EoH design wall-clock NOT REPORTED.
- Hardware: **single CPU i7-9700** for framework experiments.
- Metrics: lower-bound gap/fitness for bin packing; TSP gap to optimal/best-known + runtime; FSSP makespan and gap to Taillard best-known/upper-bound reference; convergence best/mean population performance.
- Statistical tests: NOT REPORTED.
- Confidence interval: NOT REPORTED.
- Ablation: EoC, EoH-e1, EoH-e2, full EoH; C2C/T2T2C/T&C2T2C; different LLMs; expert heuristic seed.
- Sensitivity analysis: not a conventional numeric parameter sensitivity section; representation/prompt-strategy/model/seed-source studies function as component robustness analyses.
- Generalization / OOD: TSP evolved on uniform TSP100 and tested on TSPLIB/OOD; bin packing size/capacity transfer; FSSP synthetic evolution to Taillard sizes.
- Robustness: cross-LLM GPT3.5/Gemini Pro/CodeLlama/Deepseek; repeated 3-run component studies.
- Dynamic-event design: NOT PRESENT as external scheduling events. Online bin packing is sequential arrival but not DFJSP event rescheduling.
- LLM API/inference cost: monetary cost NOT REPORTED.

## C｜Writing Evidence Coding
### Introduction
Actual sequence: **M1 heuristic importance → M4 manual design burden → M3 AHD/GP → M4 hand-crafted primitive limitation → M3 LLM opportunity + existing LLM/EC/FunSearch → M4 standalone LLM/FunSearch efficiency limitation → M6 EoH → M7 three bullet contributions**.
- Limitation is layered: first manual design, then GP search-space construction, then standalone LLM/FunSearch efficiency.
- Method follows the direct competitor limitation.
- Contributions: **3 bullets**.
- Empirical diagnosis before method: NO.

### Related Work
- Standalone Background and Related Works with explicit method-family progression: AHD → LLM heuristic design → LLM+EC.
- This is unusually clean evidence for the technical-evolution writing pattern because each subsection narrows toward the direct competitor FunSearch.
- Appendix adds Neural Solvers and Prompt Engineering context.

### Gap language
- Uses a **progressive bottleneck chain**: manual heuristics costly → GP needs predefined primitives → standalone LLM insufficient → FunSearch computationally expensive → EoH thought+code evolution.
- The gap is mechanism-specific and competitor-specific rather than a literature-volume claim.

### Contributions
- Count: **3**, bulleted.
- Paradigm/method contribution: EoH thought+code evolution.
- mechanism contribution: five prompt strategies.
- experimental contribution: three benchmark families + FunSearch/sample-efficiency comparison.

### Experimental writing
- Benchmark subsection explains task, evolution instances, fitness and baselines together, then implementation details specify exactly what function EoH designs in each downstream optimizer.
- Fairness in ablation is explicit: same initial population and adjusted generations to equalize total evaluated heuristics across variants.
- Convergence curves report both best and mean population behavior.
- Generalization is demonstrated by moving from synthetic evolution distribution to TSPLIB/Taillard and larger/different instance sets.
- Extended appendices contain prompt templates, generated heuristic code and large comparison tables, making the method auditable at implementation level.
- Missing inferential significance tests, CI, numeric random seeds, token budget and monetary LLM cost.

## Asset Metadata

- FULL TEXT READ: YES
- Source: `LLM/69_EoH.md`
- Decision Layer: Heuristic generation
- Current-study Relation: 核心演进文献
- Innovation Boundary: 当前不构成候选 selector 机制的直接新颖性反证；已实现范围为 Heuristic generation，主要用于核心演进文献。
- Best Writing Claim: thought+code co-evolution 的 LLM+EC AHD 代表作，是 heuristic generation 路线的基础锚点。
