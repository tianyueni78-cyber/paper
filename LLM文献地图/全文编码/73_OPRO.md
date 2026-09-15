# 73｜Optimization by PROmpting (OPRO) 全文编码

- Source: `LLM/73_OPRO.md`
- Full-text status: **YES**
- Last read position: **EOF (line >1260 empty); Appendices A–E covered**
- Corpus: LLM / LLM-as-optimizer
- Tier: A/A foundational mechanism competitor

## A｜Research Content
- Research problem: use an LLM itself as a derivative-free optimizer by representing an optimization task and optimization history in natural language.
- Problem setting: meta-prompt contains task description + previously generated solution-score pairs; optimizer LLM proposes new solutions; evaluator scores them; new solution-score pairs are appended for subsequent steps.
- Objectives: demonstrate black-box optimization through prompting on mathematical optimization and automate prompt optimization.
- Algorithm backbone: iterative history-conditioned black-box search using an optimizer LLM and external objective evaluator/scorer.
- Proposed mechanism: maintain optimization trajectory; sort prior solutions by score; generate multiple new candidates per step; evaluate candidates; append scores; repeat until no improvement/max steps. Temperature controls exploration/exploitation.
- Decision layer: **Direct solution generation / optimizer search update**. For prompt optimization, generated action is a new instruction; not heuristic/operator selection.
- State / Context: natural-language task description, constraints, selected historical solution-score pairs, task exemplars and meta-instructions.
- Action / Decision: generate new candidate solution(s)/instruction(s).
- Feedback / Reward: scalar objective score/training accuracy/optimality objective; evaluated candidates become future context.
- Dynamic mechanism: **online iterative adaptation to the full optimization trajectory**. Multiple samples stabilize search; old high-scoring solutions shape future generation.
- LLM role: optimizer generating next candidate directly from history.
- RL role: NOT PRESENT in OPRO itself.
- Claimed contribution: simple LLM-as-optimizer paradigm; mathematical optimization demonstrations; iterative prompt optimization with transfer gains.
- Explicit limitation: not intended to beat specialized solvers/gradient methods; context-window limits scale; bumpy landscapes cause failure/stagnation; hallucinated numeric values; duplicate proposals; starting-point sensitivity; overfitting; weak trajectories can trap optimization.
- 与当前 FJSP-AGV 研究关系: **major historical boundary**. The generic mechanism `history of solution + score → LLM infers promising direction → generate next action → evaluate → append realized score` was already explicit in OPRO. Therefore trajectory-conditioned decision generation and realized-score feedback are not novel. Current distinction must involve selecting among structured optimizer operators, joint environment/search/Pareto context, operator-specific multidimensional competence rather than scalar solution score, and context-local competence-gap logic.

## B｜Experimental Design Coding
- Dataset / Benchmark: synthetic linear regression; synthetic Euclidean TSP; GSM8K; 23 Big-Bench Hard tasks; transfer to MultiArith/AQuA and related domains.
- Instance scale: linear regression 50 data points per synthetic problem; TSP n=10/15/20/50, **5 problems per n**; GSM8K optimization uses 3.5% of 7473 training examples then full test; BBH uses 20% train / 80% test by default.
- Baselines: mathematical: NN, FI, Gurobi oracle for TSP. Prompt: human-written/empty instructions, prior prompt methods, one-step generation, EvoPrompt GA/DE.
- Baseline 数量: varies by experiment; no single count.
- Independent runs: linear regression **5 runs per setting**; major prompt ablations/curves **3 optimization repetitions**; TSP uses 5 independently generated problem instances per n rather than repeated stochastic runs on one instance.
- Random seeds: NOT REPORTED numeric.
- Population size: NOT APPLICABLE as EA population; candidate batch default **8 solutions/instructions per step**.
- Generations: prompt optimization default up to **200 steps**; mathematical runs terminate on optimum/stagnation/max settings as specified.
- Evaluation budget: default prompt optimization 200 × 8 = up to **1600 evaluated instructions**; per-step batch sensitivity equalizes total evaluated-instruction budget.
- Fitness/function evaluations: each generated solution/instruction is evaluated by objective/scorer; exact aggregate depends on task.
- Real decoding count: optimizer generates up to 8 candidates per step; aggregate implied by steps but API decoding accounting NOT separately reported.
- Solver calls: Gurobi used for TSP oracle; aggregate calls NOT REPORTED.
- LLM calls: NOT REPORTED as API-call aggregate; candidate-generation count is reported through steps × candidates.
- Token budget: NOT REPORTED as fixed cap; context-window length explicitly discussed as limitation.
- Runtime / wall-clock: NOT REPORTED.
- Hardware: NOT REPORTED.
- Metrics: objective value; optimality gap; steps to optimum; number of unique explored points; success count; training/test accuracy; mean, standard deviation/standard error depending experiment.
- Statistical tests: NOT REPORTED.
- Confidence interval: NOT REPORTED.
- Ablation: instruction ordering; score representation/no scores; number of exemplars; number of generated instructions per step; starting point; temperature; one-step vs iterative trajectory; overfitting analysis; EvoPrompt comparison.
- Sensitivity analysis: temperature {0,.5,1,1.5,2}; candidate batch {1,2,4,8,16}; exemplars; initial instruction; score/order representation.
- Generalization / OOD: GSM8K-optimized instructions transferred to MultiArith/AQuA; prompt transfer across same-domain benchmarks.
- Robustness: multiple optimizer/scorer LLM combinations; 3-repeat ablations; explicit failure-case appendix.
- Dynamic-event design: NOT PRESENT.
- LLM API / inference cost: NOT REPORTED monetary cost.

## C｜Writing Evidence Coding
### Introduction
Actual sequence: **M1 optimization ubiquity → M2 iterative optimization/update problem → M6 OPRO idea very early → M3 prompting/LLM capability → mathematical demonstration → M2 prompt-optimization problem → M4 discrete/API prompt-search difficulty → M6 meta-prompt + full trajectory distinction → experimental preview**.
- There is no conventional numbered contribution list in the Introduction.
- Method is introduced extremely early, before an extended Related Work section.
- Limitation of existing prompt optimization appears after the OPRO concept is introduced.
- Empirical diagnosis before method: NO.

### Related Work
- No standalone early Related Work section; related work is woven into Introduction and task sections/references.
- Direct comparisons are mechanism-oriented: editing one prompt vs generating from full trajectory; EvoPrompt two-parent mutation/crossover vs trajectory + exemplars + scores.

### Gap language
- Main rhetorical move is **mechanism contrast**, not scarcity: existing prompt methods edit/rephrase under narrower information, whereas OPRO uses the full optimization trajectory and explicit scores.
- Limitations are later made unusually explicit in mathematical optimization and Appendix A, including context length, hallucination, duplicate generation and landscape geometry.

### Contributions
- No explicit numbered contribution list in the read paper.
- Method contribution: LLM as optimizer via solution-score trajectory.
- empirical contribution: mathematical optimization demonstrations and broad prompt-optimization evaluation.
- empirical finding: history, scores, exemplars, batch size, temperature and initialization materially affect search behavior.

### Experimental writing
- Mathematical examples precede the main application and function as mechanism demonstrations.
- TSP uses a specialized solver oracle and simple heuristics, explicitly clarifying that OPRO is not intended to beat specialized solvers.
- Ablations are unusually rich and tied directly to meta-prompt components.
- **Budget fairness is explicit** for per-step candidate-count sensitivity: x-axis uses total evaluated instructions and step count is adjusted accordingly.
- Figures report averages across 3 repetitions with standard-deviation shading for prompt ablations; linear regression reports mean±SD; TSP uses mean±SE for steps/gaps as specified.
- Overfitting is analyzed separately with train/validation/test splits rather than ignored.
- Appendix gives concrete failure modes, which is valuable writing evidence for a limitations section.

## Asset Metadata

- FULL TEXT READ: YES
- Source: `LLM/73_OPRO.md`
- Decision Layer: Direct optimization
- Current-study Relation: 说明 history-aware direct optimization 已存在
- Innovation Boundary: 已占据或直接限制的边界：用历史 solution-score trajectory 让 LLM 提议新解，是“LLM as optimizer”最清晰的轨迹型代表。
- Best Writing Claim: 用历史 solution-score trajectory 让 LLM 提议新解，是“LLM as optimizer”最清晰的轨迹型代表。
