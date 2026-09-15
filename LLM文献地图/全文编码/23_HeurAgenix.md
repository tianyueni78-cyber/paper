# 23｜HeurAgenix 全文编码

- Source: `LLM/23_HeurAgenix.md`
- Full-text status: **YES**
- Last read position: **EOF (line >1200 empty); Appendices A–F covered**
- Corpus: LLM / Hyper-Heuristic / AHD
- Tier: **S（Direct Competitor）**

## A｜Research Content
- Research problem: 自动生成可泛化 heuristics，并在求解过程中根据当前 problem state 在线选择最合适 heuristic，减少人工 solver/domain-rule 依赖。
- Problem setting: TSP, CVRP, MKP, JSSP, MaxCut；constructive/improvement heuristics 统一为 `H: Z→O`。
- Objectives: heuristic evolution quality + online state-adaptive heuristic selection；兼顾 inference efficiency/robustness。
- Algorithm backbone: two-stage generation + selection hyper-heuristic；contrastive heuristic evolution + LLM filtering + Monte Carlo test-time search；可选 GRPO fine-tuned lightweight selector。
- Proposed mechanism: offline/evolution stage 从 basic solution 与 better contrastive solution 中识别 critical operation，LLM提取 evolution strategy 并迭代 refine heuristic，形成 diverse pool；online solving stage根据 state 由 LLM 过滤候选 heuristics，再用 Monte Carlo rollout 估计 Q 值并选择；轻量 selector 通过 offline `(z,H,Q_H)` 数据和 POR+CPR dual reward 做 GRPO fine-tuning。
- Decision layer: **Heuristic generation + online heuristic selection**。底层 heuristic 再把 state 映射为具体 operation。
- State / Context: explicit problem-state feature vector + remaining decisions；不同问题有专门 static/dynamic state features。TSP/CVRP/MKP/JSSP/MaxCut state fields 在 Appendix E 明列。
- Action / Decision: selector action = choose heuristic `H` from evolved pool；heuristic action = operation `O` such as Insert/Swap/Reverse/Shift 等。
- Feedback / Reward: evolution uses solution cost/performance and critical-operation contrast；online TTS uses average terminal cost from Monte Carlo rollouts；fine-tuning uses POR + CPR + format/language rewards。
- Dynamic mechanism: **online search-state adaptation YES**；**external dynamic scheduling events NOT PRESENT**。
- LLM role: heuristic evolution/refinement；online candidate filtering/selection；可由 fine-tuned Qwen-7B selector替代 frontier LLM。
- RL role: GRPO fine-tunes lightweight selector using dual reward；not classical Q-learning。
- Claimed contribution: unified automatic heuristic evolution + adaptive online selection；contrastive data-driven evolution；dual-reward robust selector training under noisy long-horizon supervision。
- Explicit limitation: only Qwen-7B fine-tuning backbone tested；POR positive/negative split manually chosen；extension beyond classical CO finite operation spaces to broader finite-state MDP remains future work。
- 与当前 FJSP-AGV 研究关系: **直接压缩创新空间**。`offline heuristic pool generation/evolution + current-state online LLM selection` 已明确存在；`state→heuristic`、online adaptive selection、LLM/TTS selector、RL-trained selector、state-perception reward 都不能单独作为创新。它没有 dynamic FJSP-AGV exogenous event context、multiobjective Pareto state、operator-specific competence profile/uncertainty、predicted-vs-realized context-specific effect model、coverage-gap-triggered slow-timescale redesign。

## B｜Experimental Design Coding
- Dataset / Benchmark: TSPLIB, CVRPLIB, OR-Library MKP/JSSP, Optsicom MaxCut。
- Instance scale: each problem evolution train set 20 generated instances；TSP validation 7/test 12 listed；CVRP validation 7/test 6；MKP validation 7/test 10；JSSP validation LA21–30/test LA01–20；MaxCut validation g11–20/test g1–10。
- Baselines: problem-dependent. TSP GLS, ACO, OR-Tools, EoH+GLS, ReEvo+GLS, ReEvo+ACO; CVRP ACO, OR-Tools, ReEvo+ACO; MKP ACO, ReEvo+ACO, QICSA, PSO; JSSP ACO, PSO, GWO; MaxCut SS, CirCut, VNSPR. Evolution comparison additionally seed heuristics, EoH/ReEvo where interfaces permit. Selector comparison GPT-4o, O3, DeepSeek-R1, raw Qwen7B, GRPO。
- Baseline 数量: no single global count because baseline set differs by problem; TSP main solving **6**, CVRP **3**, MKP **4**, JSSP **3**, MaxCut **3** named comparators excluding Ours。
- Independent runs: **3** for experiments, explicitly to reduce variance。
- Random seeds: numeric seeds **NOT REPORTED**。
- Population size: NOT APPLICABLE / NOT REPORTED for HeurAgenix as population EA。
- Generations: NOT APPLICABLE；heuristic evolution refinement max 5 rounds。
- Evaluation budget: each LLM hyper-heuristic evolution capped at **2000 API calls/problem**；test instance max runtime **2 h**；selection frequency M=5；Monte Carlo search times=10；max perturbation trials P=1000。
- Fitness / function evaluations: exact aggregate count NOT REPORTED。
- Real decoding count: NOT REPORTED。
- Solver calls: no external solver required by claimed framework; exact operation/evaluation call count NOT REPORTED。
- LLM calls: evolution 2000 API calls cap; solving `ceil(N/M)+2` API calls stated for LLM selector。
- Token budget: max tokens 1600 per LLM call; fine-tuning max prompt 2048, completion 768; total tokens NOT REPORTED。
- Runtime / wall-clock: 2-hour per-test-instance cap；actual wall-clock comparison NOT REPORTED in read text。
- Hardware: GNU/Linux kernel 5.15.0-121-generic, Intel Xeon, Appendix E says **4× NVIDIA RTX A6000 48G**, CUDA 12.2。
- Metrics: optimality gap `%`; mean and variance/± dispersion shown; rollout-budget curve。
- Statistical tests: **NOT REPORTED**。
- Confidence interval: **NOT REPORTED**。
- Ablation: raw Qwen-7B vs vanilla GRPO vs POR+CPR；test-time rollout-budget effect；heuristic before/after evolution。No full factorial decomposition of pool design × selector type。
- Sensitivity analysis: rollout budget analyzed；POR threshold sensitivity **NOT PRESENT**；M=5 fixed。
- Generalization / OOD: multiple CO domains and benchmark sizes; explicit claim scalability/domain generality, but no separately labeled OOD protocol analogous train-size→unseen-size across every problem。
- Robustness: three-run variance; noisy-label reward toy analysis; positive-set behavior; fine-tuned selector comparison across TSPLIB states。
- Dynamic-event design: **NOT PRESENT**。
- LLM API / inference cost: qualitative lower inference cost for lightweight model; monetary API cost **NOT REPORTED**。
- Fairness: GPT-4o fixed across LLM-based hyper-heuristic evolution; each method 2000 API calls; 2h test limit; external-source baseline values dagger-marked。

## C｜Writing Evidence Coding
### Introduction
Actual sequence: **M1 CO importance/complexity → M3 heuristics → M4 manual expertise/adaptation → M3 hyper-heuristics → M4 manual selection-rule limits → M3 LLM-AHD → M4 solver/domain-knowledge dependence → M6 HeurAgenix + strong novelty claim → M7 3 bullets**。
- Limitation first appears: paragraph 2 (manual heuristic expertise/adaptation); LLM-specific limitation paragraph 3。
- Method appears: immediately after LLM-AHD limitation, “To address these limitations, we introduce HeurAgenix”。
- Contributions: **3 bullet contributions** at Introduction end。
- Empirical diagnosis before method: NO formal empirical diagnosis; conceptual/literature argument。

### Related Work
- Combined Preliminary and Related Work, organized as definitions + method families: Heuristics for CO → Hyper-Heuristics (generation vs selection) → LLMs for CO → Test-time Scaling → noisy long-term decision-making。
- taxonomy/method family: YES。
- generation vs selection: **YES, explicit central taxonomy**。
- traditional→learning→LLM: partial progression。
- direct solving vs solver-assisted: Table 1 compares paradigms and whether solver required, but not entire section taxonomy。
- single heuristic vs portfolio: central contrast in method motivation, not named taxonomy heading。
- static vs adaptive: explicit contrast in prose。
- offline vs online: explicit distinction between offline evolution and inference-time adaptive selection。

### Gap language
- Contrast/limitation: `Despite their effectiveness...`; `Although...`; `However, as illustrated in Table 1...`; `yet its offline evolutionary loop... does not provide instance-level adaptation`。
- Motivation/transition: `To address these limitations...`; `We therefore require a real-time selector...`; `To address these challenges...`。
- Novelty strength: `To the best of our knowledge... first LLM-based hyper-heuristic framework that simultaneously...`。
- Gap construction is competitor-specific: first acknowledges FunSearch/EoH/ReEvo/AlphaEvolve capabilities, then isolates solver dependence + offline/no instance-level adaptation before positioning two-stage framework。

### Contributions
- Count: **3**；bulleted: YES。
- Verbs: introduce/propose/develop/introduce。
- Method contribution: YES, unified framework。
- Formulation contribution: selection objective/Q-value formulation present but not separate contribution bullet。
- Experimental contribution: performance claim embedded in first bullet, not standalone benchmark contribution。
- Benchmark contribution: NO。
- Empirical finding contribution: NO separate bullet。

### Experimental writing
- Setup first gives five global fairness controls: foundation model, API-call budget, execution time, metric/repeats, platform；then lists five problem benchmarks。
- Baseline selection is problem-specific and explicitly explains copied external results with dagger notation。
- Comparative results use headline figure in main text and exhaustive per-instance tables in appendix。
- Ablation directly asks selector-training contribution: raw → GRPO → dual reward；separate TTS rollout-budget analysis isolates inference search benefit。
- Robustness/generalization is argued through five domains + multiple selector models + repeated runs, rather than a dedicated robustness section。
- Statistical significance: NOT PRESENT。
- Computational cost: unusually explicit API-call cap, per-instance time cap, selection frequency, MC rollouts, hardware and token limits; monetary cost absent。
