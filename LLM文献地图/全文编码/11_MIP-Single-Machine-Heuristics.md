# 11 LLM-discovered SMTT heuristics｜全文编码

## Audit
- Source: `LLM/11_MIP-Single-Machine-Heuristics.md`
- Full text read to EOF: YES
- Abstract, Introduction, Literature Review, formulation/exact methods, LLM heuristic-discovery method, experimental setup/training, discovered algorithms, datasets, computational results, runtime analysis, Conclusion/future directions, Appendix: READ where present.

## A. Research Content
- Research problem: discover scalable construction heuristics for single-machine total tardiness scheduling (SMTT), an NP-hard scheduling/MIP problem.
- Problem setting: non-preemptive single-machine sequencing with processing times and due dates; objective sum of tardiness.
- Objectives: minimize total tardiness; discover reusable heuristics that improve classical rules and scale beyond exact methods.
- Algorithm backbone: FunSearch-inspired island-based program evolution with LLM mutation, evaluator and program database.
- Proposed mechanism: start from EDD/SPT/MDD assignment functions; LLM iteratively edits heuristic code; feasibility/performance evaluator filters/ranks programs; island evolution and best-shot prompting produce EDDC/MDDC.
- Decision layer: heuristic/operator generation (offline algorithm discovery), not online scheduling control by LLM.
- State/context: initial heuristic code, problem specification/docstring, sampled high-performing programs/database, training-instance performance.
- Action/decision: LLM mutates/generates scheduling assignment functions.
- Feedback/reward: average total tardiness over training dataset with penalties for infeasible/manipulated schedules; optimality gaps used in testing.
- Dynamic mechanism: evolutionary heuristic discovery; scheduling problem itself is static deterministic SMTT.
- LLM role: frozen inference model used as mutation/program-generation operator.
- RL role: NOT PRESENT in proposed method.
- Claimed contribution: LLM-human discovery of EDDC and MDDC; rigorous benchmarking against exact and heuristic methods; scale transfer from 25-job training to up to 500 jobs.
- Explicit limitation: EDDC does not match leading heuristics; discovery is computationally intensive (up to 72 h); generated logic can be difficult to interpret; later iterations may be redundant; future directions include explainable/tree methods, adaptive sampling/stopping and broader scheduling/CO problems.
- Relation to current FJSP-AGV research: direct Scheduling×LLM crossover evidence that LLM can design reusable scheduling heuristics offline, but does not address dynamic multiobjective FJSP-AGV, contextual online selection, Pareto state or AGV state.

## B. Experimental Design
- Dataset / Benchmark: synthetic SMTT instances using established TF/RDD generation; Shang et al. larger benchmark solutions.
- Instance scale: training 10,000 instances at n=25; testing n=20,100,200,500; n=20 has 800 uniform + 800 normal/OOS instances; n=100/200/500 each 200 sourced instances.
- Baselines: EDD, MDD, Panneerselvam, PSK; exact MIP, MIP+valid inequalities, DP; Branch & Memorize provides larger-instance optima; augmented MDD/MDDC comparisons.
- Number of baselines: varies by experiment; main heuristic tables compare EDD, EDDC, MDD, MDDC, Panneerselvam, PSK against exact optimum.
- Independent runs: NOT REPORTED as repeated stochastic runs of final heuristic evaluation; results aggregate many generated problem instances/classes.
- Random seeds: NOT REPORTED.
- Population size: 10 islands; population is program database/island-based rather than conventional EA population size.
- Generations: up to 10,000 LLM/evolution iterations; reset every 14,400 seconds.
- Evaluation budget: discovery stops at 72 hours or 10,000 iterations; one sampler/evaluator, single-threaded.
- Fitness/function evaluations: generated functions evaluated on 10,000 n=25 training instances; exact total FE count NOT REPORTED.
- Real decoding count: NOT REPORTED.
- Solver calls: Gurobi/DP exact comparisons; unified solver-call count NOT REPORTED.
- LLM calls: effectively iterative generation up to 10,000 iterations, but exact API/inference-call accounting NOT REPORTED separately.
- Token budget: NOT REPORTED.
- Runtime / wall-clock: discovery up to 72 h; exact-method CPU time; final heuristic CPU seconds by problem size.
- Hardware: Nvidia A100 80GB GPU, AMD EPYC 7742 Zen 2; Python 3.11, Transformers 4.43.3, Tensorboard 2.17.0, PyTorch 2.3.0, Gurobi 11.0.1.
- Metrics: total tardiness, percent optimality gap, CPU solution time; training convergence average tardiness.
- Statistical tests: NOT REPORTED.
- Confidence interval: NOT REPORTED.
- Ablation: no conventional component-removal ablation of the discovery framework; comparisons of starting heuristic pipelines and augmented heuristic variants serve mechanism/variant analyses but are not labeled framework ablation.
- Sensitivity analysis: NOT PRESENT as formal parameter sensitivity.
- Generalization / OOD: normal-distribution OOS n=20 dataset; scale transfer from n=25 training to n=100/200/500 without retraining.
- Robustness: discussed through performance across TF/RDD difficulty classes and OOS/scale tests.
- Dynamic-event design: NOT PRESENT.
- LLM API / inference cost: open-source Mixtral 8x7B local inference; monetary API cost NOT APPLICABLE/NOT REPORTED.

## C. Writing Evidence
### Introduction rhetorical moves
- M1 formal problem definition/importance → M3 LLM scientific discovery → M3/M4 prior scheduling/exact/heuristic landscape → M6 proposed LLM discovery pipeline → early empirical preview of EDDC/MDDC → contribution/value/generalization/reproducibility framing.
- Contributions are prose rather than a compact numbered contribution list.

### Related Work organization
- Dedicated Literature Review.
- Starts with chronological/theoretical SMTT evolution: DP/dominance/decomposition/exact/MIP/branch-and-bound/heuristics.
- Then transitions to LLM scientific discovery and adjacent ML/optimization work.
- Hybrid chronological + method-family organization.

### Gap / limitation formulation
- Gap is application+evaluation-level: adapt LLM program discovery to MIP-based scheduling with stronger feasibility/optimality evaluation and resource-efficient implementation.
- Prior LLM limitations are framed as unreliability/hallucination and need for structured iterative validation.

### Proposed-method transition
- `Our study contributes...` and `We implement an LLM-backed algorithmic discovery pipeline...` introduce method after positioning scheduling and LLM discovery.

### Contribution structure
- No numbered contribution list; contributions are distributed across Introduction: discovered heuristics, rigorous exact/heuristic benchmarking, scalability/generalization, resource-efficient implementation and reproducibility.

### Experimental Setup organization
- Method section contains dedicated `Experimental Setup and Training`; later Results separates dataset generation and computational results, then exact-method comparison, heuristic performance, augmented variants and runtime.

### Comparative-result reporting
- Explains optimality-gap definition before tables; classifies instance difficulty; reports representative rows plus aggregate averages; discusses both wins and failure classes rather than only best results.

### Ablation-result reporting
- Conventional component ablation NOT PRESENT; variant comparisons are interpreted in terms of starting heuristic and augmentation.

### Academic hedging
- Mixes strong claims (`advances the state-of-the-art`) with explicit failure/limitation statements (`falls short`, `fails to deliver robust performance in some instance classes`, computational intensity).

### Novelty-claim strength
- Strong discovery/SOTA language, but claims are tied to SMTT benchmark comparisons; no corpus-wide first claim is inferred here.

## Asset Metadata

- FULL TEXT READ: YES
- Source: `LLM/11_MIP-Single-Machine-Heuristics.md`
- Decision Layer: Heuristic generation
- Current-study Relation: 调度侧背景
- Innovation Boundary: 当前不构成候选 selector 机制的直接新颖性反证；已实现范围为 Heuristic generation，主要用于调度侧背景。
- Best Writing Claim: 用 LLM 辅助生成可解释单机调度 heuristic，说明调度 heuristic generation 已并非空白。
