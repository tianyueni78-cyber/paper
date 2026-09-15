# 40｜Planning of Heuristics (PoH) 全文编码

- Source: `LLM/40_Planning-of-Heuristics.md`
- Full-text status: **YES**
- Last read position: **EOF (line >600 empty); Appendix 7.1–7.13 covered**
- Corpus: LLM / AHD / planning / scheduling
- Tier: S（Direct Competitor / mechanism boundary）

## A｜Research Content
- Research problem: automate heuristic optimization for COPs while avoiding unguided/direct iterative LLM evolution that lacks principled long-horizon exploration.
- Problem setting: LLM-generated heuristics embedded in GLS; tested on TSP and Flow Shop Scheduling Problem (FSSP).
- Objectives: reframe heuristic optimization as strategic planning; use trajectory/reward-aware MCTS to search heuristic space efficiently; improve large-scale generalization.
- Algorithm backbone: Guided Local Search executor + LLM heuristic generation/self-reflection + MDP formulation + Monte Carlo Tree Search (selection, expansion, simulation, backpropagation) + early stopping.
- Proposed mechanism: heuristic code = state; LLM improvement suggestion = action; action applied by optimizer LLM produces next heuristic state; generated heuristic is executed inside GLS and evaluated; reward guides MCTS tree search; trajectory heuristics, code/descriptions/evaluation results and improvement suggestions enter state-transition prompts.
- Decision layer: **Heuristic/operator generation / optimizer design**, not online selection from a fixed operator pool. In FSSP generated heuristic controls execution-time-matrix update and which jobs to perturb inside GLS.
- State / Context: current heuristic code/state; current/past heuristic trajectory; descriptions; evaluation reward/optimal gap; improvement suggestions; MCTS node/path statistics. FSSP heuristic additionally receives current job sequence, time matrix, m, n at execution.
- Action / Decision: natural-language improvement suggestion; transition then generates a new executable heuristic. FSSP heuristic outputs updated time matrix + perturbed-job set.
- Feedback / Reward: execute heuristic in GLS on training/validation instances; reward normalized from current objective relative to preselected baseline/best value (`1-gap` style); MCTS accumulates/backpropagates rewards.
- Dynamic mechanism: **search-process dynamic adaptation** through trajectory-dependent MCTS planning and iterative self-reflection; early stopping based on reward thresholds. It is not external dynamic scheduling (no machine/AGV failure/job arrival).
- LLM role: initialize heuristic; analyze current/past heuristics and evaluation results; propose improvement suggestions; generate next heuristic code.
- RL role: no learned RL policy. MDP/MCTS planning supplies state-action-reward formalization; NeuOpt RL appears as baseline.
- Claimed contribution: PoH strategic MCTS heuristic-space planning; performance over AHD/LLM baselines; combination of iterative self-reflection and planning.
- Explicit limitation: MCTS simulation may be time-consuming; future work suggests cheaper simulation such as Gumbel MCTS and practical large-scale COPs. Standalone Limitations heading NOT PRESENT.
- 与当前 FJSP-AGV 研究关系: **major novelty boundary**. PoH already uses `current heuristic + trajectory + historical evaluation results → LLM improvement action → new heuristic → execute → reward → planning/backpropagation`, and its FSSP heuristic explicitly acts on current sequence/time matrix and chooses perturbed jobs. Therefore `search history`, `previous effect`, `feedback-driven redesign`, `trajectory-aware heuristic improvement`, and even `state-action-reward framing` cannot independently establish novelty. The remaining distinction for current work must be tested around **online selection among a complementary operator portfolio rather than generating a new heuristic each transition**, **joint environment/search/Pareto/AGV context**, **multiobjective operator-effect competence profiles**, and potentially **slow-timescale redesign triggered by empirically localized competence gaps**, provided later papers do not already cover this intersection.

## B｜Experimental Design Coding
- Dataset / Benchmark: TSP synthetic training + TSPLIB + ReEvo TSP dataset; FSSP synthetic training + Taillard instances.
- Instance scale: TSP training 64 instances, 100 nodes; ReEvo test sizes TSP20/50/100/200; TSPLIB includes <200 and larger instances; FSSP training 64 random instances, 50 jobs, machines 2–20; full Taillard appendix 11 scales from 20×5 through 200×20, **10 instances per scale**.
- Baselines: TSP includes KGLS, GNNGLS, NeuralGLS, NCO/NeuOpt, EoH, ReEvo, OR-Tools, AM, POMO, LEHD, plus GLS/LS variants in tables; FSSP includes NEH, NEHFF, LS, ILS, PFSPNet, PFSPNet_NEH, EoH, and appendix also GUPTA/CDS/ILS2.
- Baseline 数量: varies by table/problem; no single global count. Main TSP baseline paragraph names **10** methods; main FSSP paragraph names **6 baseline families/methods** before EoH appears in results.
- Independent runs: LLM generalization Table 4: **3 independent runs per LLM** on TSP200. Other main tables do not consistently report repeated runs.
- Random seeds: ReEvo-generated 64-instance experiment uses **seed 1234**; other seeds NOT REPORTED.
- Population size: NOT APPLICABLE as EA population.
- Generations: MCTS **10 iterations**, expansion width 5, max depth 5, exploration weight 2.5.
- Evaluation budget: Appendix: MC samples 72 heuristics/task; Beam 72 nodes at width 3/depth 8; Greedy example 34; Table 5 MCTS explores **60 heuristics**, Greedy 34, Beam 72. TSP heuristic evaluation uses **800 GLS iterations** on TSP200.
- Fitness / function evaluations: heuristic evaluation through GLS objective/gap; exact aggregate objective-evaluation count NOT REPORTED.
- Real decoding count: explored heuristic counts reported for search-strategy comparisons; total LLM generations for complete PoH runs beyond those counts NOT REPORTED.
- Solver calls: Concorde / LKH or baseline algorithms generate reference values; exact call counts NOT REPORTED.
- LLM calls: not directly tabulated; tied to node expansion/action generation/state transition; aggregate NOT REPORTED.
- Token budget: NOT REPORTED.
- Runtime / wall-clock: per-instance execution time reported for TSP20/50/100/200 algorithm execution; heuristic-design/training wall-clock and LLM planning cost NOT REPORTED.
- Hardware: NOT REPORTED.
- Metrics: optimality gap / relative distance to best-known; FSSP average relative makespan gap; per-instance execution time; explored heuristic count; convergence curves; std/error bars in ablation/convergence; reward.
- Statistical tests: NOT REPORTED. Paper repeatedly uses `significantly` descriptively without named test.
- Confidence interval: NOT REPORTED.
- Ablation: search strategy MC vs Greedy vs Beam vs MCTS with identical state transition/action generation; authors state total explored heuristics kept constant for ablation, although Table 5 exploration-efficiency comparison deliberately uses 34/72/60.
- Sensitivity analysis: convergence vs MCTS iterations and tree depth; cross-LLM backbone study.
- Generalization / OOD: TSPLIB scale; TSP20→200; four LLMs; TSP + FSSP; full Taillard scales.
- Robustness: 3 independent LLM runs; std/error bars; multiple scales/instances.
- Dynamic-event design: NOT PRESENT.
- LLM API / inference cost: NOT REPORTED.

## C｜Writing Evidence Coding
### Introduction
Actual sequence: **M1 COP importance → M3 heuristics/GLS-GA-ACO → M4 manual domain/time/error burden → M3 AHD → M3 LLM heuristic-generation/evolution progress → M6 PoH strategic planning mechanism → M7 three bullets**. The sharper gap about direct iterative search without principled guided exploration is stated in Related Work rather than strongly in Introduction.
- Limitation appears paragraph 1 around manual heuristic design.
- Proposed method appears after LLM/AHD background.
- Contributions: **3 bullets**.
- Empirical diagnosis before method: NO.

### Related Work
- Two method-family sections: `LLMs for Optimization`; `LLMs with Self-reflection and Planning`.
- Evolution inside first section: prompt engineering → LLM+EC heuristic generation → FunSearch/EoH/ReEvo.
- Second section supplies conceptual ancestors self-reflection + planning/MCTS.
- Ends with explicit contrast: existing heuristic optimization often evolutionary/reflection-based but direct iterative, whereas PoH combines reflection with principled planning.
- generation vs selection: primarily generation/refinement; selection is MCTS path/node selection, not operator portfolio selection.
- static vs adaptive: adaptive trajectory refinement implicit.

### Gap language
- `However, relying solely on prompt engineering ... limited effectiveness` motivates AHD evolution.
- Central competitor contrast: `However, existing LLM-based heuristic optimization methods ... typically employ direct iterative algorithms without principled strategies for guided exploration. In contrast...`.
- `Therefore, ... introduce` is used in Introduction as proposal transition.
- Strong novelty wording includes `novel framework` and SOTA claim; these are author claims.

### Contributions
- Count: **3**, bullets.
- Method: MCTS planning AHD.
- Formulation: heuristic optimization as MDP/state-action-reward planning.
- Experimental: TSP/FSSP comparisons, ablation, cross-LLM, convergence/generalization.
- Benchmark: NO new benchmark.
- Empirical finding: planning improves large-scale gaps/exploration efficiency in reported tests.

### Experimental writing
- Experimental setup is interleaved after methodology due source formatting, but contains Tasks/Datasets → Baselines → Implementation details before Result and Analysis.
- Baselines are grouped by methodological category, not merely listed.
- Fairness in search ablation explicitly fixes state-transition/action-generation mechanisms and attempts to control explored-heuristic budget; exploration-efficiency analysis then reports budget/performance tradeoff separately.
- Results are organized by problem, then dedicated sections for generalization, ablation, exploration efficiency, convergence and qualitative trajectory.
- Appendix greatly expands reproducibility: search budgets, early-stop rule, reward construction, generated-heuristic execution, prompts, complete TSPLIB/Taillard tables.
- No formal statistical test/CI, despite 3-run and standard-deviation visual reporting.
