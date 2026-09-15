# 10 AFL / Agentic VRP｜全文编码

## Audit
- Source: `LLM/10_Agentic-VRP.md`
- Full text read to EOF: YES
- Title/Abstract, Introduction, Preliminaries, Methodology, Experiments, Results, Ablation, Broad Applicability, Conclusion/limitation, Related Work appendix, Problem Statement, supplementary methodology/experiments, prompt/output appendix: READ where present.

## A. Research Content
- Research problem: automate end-to-end solving of complex VRPs while improving code reliability, solution feasibility and autonomy of LLM-based optimization frameworks.
- Problem setting: diverse conventional/practical VRP variants represented primarily in VRPLIB, plus JSON/CSV robustness tests.
- Objectives: minimize routing cost/distance under variant-specific constraints; system-level objectives additionally include self-containment, full automation and trustworthiness.
- Algorithm backbone: self-contained destroy-insert heuristic with simulated-annealing acceptance, generated/refined by a multi-agent LLM pipeline.
- Proposed mechanism: three subtasks (problem description, code generation, solution derivation) and four specialized agents (generation, judgment, revision, error analysis); problem/code buffer for reuse.
- Decision layer: optimizer/framework design and executable solver generation, not online heuristic/operator selection.
- State/context: raw instance, generated structured problem description, constraints/input/output/objective specification, existing code, judgments, runtime errors and buffer contents.
- Action/decision: generate/revise problem descriptions and individual solver functions; diagnose execution errors; reuse stored code when applicable.
- Feedback/reward: judgment-agent correctness feedback and runtime error-analysis feedback; final feasibility/objective values evaluate generated solver.
- Dynamic mechanism: iterative agent feedback/revision during framework construction; not dynamic environment control.
- LLM role: knowledgeable developer/agent ensemble for formulation extraction, code generation, verification, revision and debugging.
- RL role: NOT PRESENT.
- Claimed contribution: self-contained, fully automated agentic LLM framework for complex VRPs with high code reliability/solution feasibility.
- Explicit limitation: does not surpass specialized SOTA solvers on well-studied problems such as CVRP; future work proposes evolutionary search for code generation/search efficiency.
- Relation to current FJSP-AGV research: boundary/architecture evidence for LLM optimizer-design and verification roles; not a direct contextual operator-selector competitor.

## B. Experimental Design
- Dataset / Benchmark: 48 standard VRP variants; 8 practical electric VRP variants; TSP/ATSP/ACVRP/SOP additional benchmarks; TSPLib/CVRPLib and ECVRPTW-derived practical settings.
- Instance scale: standard comparisons include n=50/100 with 1,000 instances per problem; ECVRPTW 36 small (5/10/15 customers) + 56 large (100); TSPLib 50–1000; CVRPLib 100–1000; ATSP 17–443; ACVRP 16–200; SOP 9–380; large CVRP appendix experiments also reported.
- Baselines: HGS-PyVRP, OR-Tools, RF-POMO; ACO, Greedy; SGE, DRoC, ReEvo; prompting baselines standard prompting, self-refine, self-debug, self-verification, CoT.
- Number of baselines: varies by experiment; no single fixed baseline count.
- Independent runs: a universal independent-run count for all main experiments is NOT REPORTED.
- Random seeds: NOT REPORTED.
- Population size: NOT APPLICABLE as a population-based EA protocol.
- Generations: NOT APPLICABLE; solution-improvement steps T=500/2000/10000 used in main comparisons.
- Evaluation budget: improvement-step budgets T=500/2000/10000; ACO practical baseline fixed at 500 improvement steps; 10-hour limit noted for DRoC on larger CVRPLib.
- Fitness/function evaluations: NOT REPORTED as a unified FE budget.
- Real decoding count: NOT REPORTED.
- Solver calls: NOT REPORTED as a unified count.
- LLM calls: NOT REPORTED as one universal count.
- Token budget: NOT REPORTED.
- Runtime / wall-clock: objective/gap/time reported; AFL runtime in standard benchmark = problem description + solution derivation, excluding reusable code-generation phase; separate code-generation-time analysis in Appendix C.4.
- Hardware: AMD EPYC 7702P CPU, 64 GB RAM, no GPU acceleration.
- Metrics: objective value, relative Gap, runtime, Runtime Error Rate (RER), Success Rate (SR), problem-description accuracy; code reliability/solution feasibility.
- Statistical tests: NOT REPORTED.
- Confidence interval: NOT REPORTED.
- Ablation: removal/combination of judgment agent and revision agent; compares None, Revision, Judgment+Revision.
- Sensitivity analysis: different LLM backbones (Claude-Sonnet-4, GPT-4.1, GPT-4o); different input formats.
- Generalization / OOD: broad cross-variant benchmarks, input-format robustness, large CVRP and non-Euclidean ATSP/ACVRP/SOP.
- Robustness: code reliability/feasibility across variants and LLMs explicitly analyzed.
- Dynamic-event design: NOT PRESENT.
- LLM API / inference cost: experiments via OpenAI API; monetary/token cost NOT REPORTED in the coded text as a main metric.

## C. Writing Evidence
### Introduction rhetorical moves
- Sequence: M1 domain/problem importance → M3 traditional/neural methods → M3 LLM approaches → M4 limitations of direct/evolving/general-framework routes → M5 automation/self-containment/trustworthiness gap → M6 AFL → M7 contributions.
- Contributions: 3 numbered items, explicitly labeled Conceptually / Methodologically / Experimentally.
- Empirical diagnosis before method: comparison table of representative LLM approaches is used in Introduction to sharpen capability differences before AFL is fully introduced.

### Related Work organization
- Located in Appendix A.
- Method-family organization: ML for VRPs; LLM for VRPs.
- LLM subsection further divides direct solution generation vs code generation, then basic heuristic evolution vs general frameworks.

### Gap / limitation formulation
- Function: contrast and capability/system-level limitation, focusing on external intervention, non-self-containment, lack of full automation, code/solution unreliability.
- Uses calibrated route-by-route limitations rather than a broad `no prior work` statement.

### Proposed-method transition
- Prior limitations → `we address these limitations by proposing` collaborative LLM agents → AFL decomposition and roles.

### Contribution structure
- 3 numbered contributions: conceptual positioning, methodological framework, experimental validation.

### Experimental writing
- Experiment overview first states evaluation sequence and goals.
- Standard benchmark section explicitly states what the method is NOT trying to prove (not surpassing decades-optimized SOTA), then defines a 3% gap acceptance criterion.
- Baseline comparisons are separated by standard solver, practical VRP, LLM-based solver, prompting strategy, ablation and broad applicability.
- Runtime accounting explicitly explains excluded reusable code-generation time and points to appendix analysis.

### Comparative-result reporting
- Reports Obj/Gap/Time together; uses reliability metrics RER/SR for LLM solvers; interprets performance relative to the method’s automation/generalization objective.

### Ablation-result reporting
- Removes agent components and evaluates intermediate correctness (problem-description accuracy) plus final solution gap/reliability, connecting component function to observed degradation.

### Academic hedging
- Strong empirical statements coexist with scope qualification (`objective is not to surpass SOTA...`, `potential`, `can be extended`).

### Novelty-claim strength
- Strong capability claims (`full automation`, `self-contained`, `high trustworthiness`) are operationally defined in Table 1; no unsupported corpus-level novelty inference is added here.

## Asset Metadata

- FULL TEXT READ: YES
- Source: `LLM/10_Agentic-VRP.md`
- Decision Layer: Algorithm workflow
- Current-study Relation: 背景性说明 agentic optimization
- Innovation Boundary: 当前不构成候选 selector 机制的直接新颖性反证；已实现范围为 Algorithm workflow，主要用于背景性说明 agentic optimization。
- Best Writing Claim: 把生成、判断、修正、错误分析拆成多 Agent VRP workflow，是 agentic optimizer 的系统级案例。
