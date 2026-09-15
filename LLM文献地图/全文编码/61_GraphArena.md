# 61｜GraphArena 全文编码

- Source: `LLM/61_GraphArena.md`
- Full-text status: **YES**
- Last read position: **EOF (line >980 empty); appendices through task prompts covered**
- Corpus: LLM / graph computation benchmark / combinatorial optimization boundary
- Tier: B/C

## A｜Research Content
- Research problem: rigorously evaluate whether LLMs can solve realistic graph computational problems, especially higher-complexity and NP-complete tasks, without conflating feasible, optimal and hallucinated outputs.
- Problem setting: 10 graph tasks over real-world graph sources, split into 4 polynomial-time direct algorithmic reasoning tasks and 6 NP-complete meta algorithmic planning tasks; small and large graph regimes.
- Objectives: benchmark LLM reasoning/planning; classify failure modes; test interventions including CoT, instruction tuning, code execution and test-time compute scaling.
- Algorithm backbone: benchmark generation from real-world graphs → natural-language encoding → LLM response → path extraction → feasibility check → optimality verification → categorized outcome.
- Proposed mechanism: realistic graph sampling + task taxonomy + path-based verifier; intervention studies for improving reasoning.
- Decision layer: **Direct solution / algorithmic planning**, not operator selection or optimizer control.
- State / Context: natural-language graph representation, task definition, demonstration; for sequential test-time compute, previous answers/checker results are used as hints.
- Action / Decision: output graph solution/path; in NP tasks implicitly select/use a solving strategy; code-writing intervention generates executable code.
- Feedback / Reward: deterministic feasibility/optimality checker; sequential test-time compute feeds previous answer and checker result back as hints. No learned reward policy in main method.
- Dynamic mechanism: NOT PRESENT as external dynamic optimization. Test-time sequential refinement is iterative but not dynamic scheduling/search control.
- LLM role: direct graph problem solver, code generator, or fine-tuned reasoner depending experiment.
- RL role: NOT PRESENT in proposed benchmark/interventions.
- Claimed contribution: GraphArena benchmark with real-world graph collection, harder task selection including NP-complete planning, rigorous path-based evaluation, broad LLM/baseline evaluation, and intervention analysis.
- Explicit limitation: no standalone Limitations section; conclusion/results explicitly show CoT, fine-tuning and test-time compute remain insufficient for complex/large graph tasks; code execution can degrade small-graph performance; GNN-vs-LLM comparison has paradigm mismatch.
- 与当前 FJSP-AGV 研究关系: strong boundary evidence against treating LLM direct reasoning as a reliable optimization engine. It supports keeping numerical/search execution in the optimizer and using deterministic decoding/evaluation. It also shows that repeated attempts/checker feedback do not automatically solve combinatorial planning at scale. It does not implement operator competence models or online AOS.

## B｜Experimental Design Coding
- Dataset / Benchmark: GraphArena; DBLP, Social Network, DBpedia, OpenFlights, PubChemQC.
- Instance scale: **10 tasks × 1000 = 10,000 problems**, each task 500 small + 500 large. Node ranges vary by task: up to 50 nodes for Neighbor/Distance, 30 for Component/Diameter/MCP/MIS/MVC, 20 for MCS/GED/TSP. Text can reach roughly 6,000 tokens; Appendix reports detailed character lengths.
- Baselines: 10 LLMs; exact/traditional graph algorithms; Random, Greedy, Approximation algorithms; GNNs GIN/GAT/GSAGE; Graph-LLM hybrids; intervention variants.
- Baseline 数量: heterogeneous multi-family comparison; 10 LLMs in main table plus classical/GNN/hybrid baselines. A single scalar baseline count is not meaningful across experiments.
- Independent runs: **single run per LLM across the 10,000 benchmark problems** due computational cost. Test-time scaling deliberately uses multiple attempts as an intervention, not independent experimental replications.
- Random seeds: NOT REPORTED.
- Population size: NOT APPLICABLE.
- Generations: NOT APPLICABLE.
- Evaluation budget: 10,000 problems/model in main LLM benchmark; test-time scaling attempts 1–5 in shown experiments; SFT uses additional 10,000 GraphArena problems.
- Fitness / function evaluations: NOT APPLICABLE.
- Real decoding count: at least one response/problem/model in main benchmark; aggregate exact call count NOT REPORTED.
- Solver calls: exact algorithms generate ground truth/check optimality; aggregate NOT REPORTED.
- LLM calls: main evaluation one response/problem/model; aggregate API calls NOT REPORTED explicitly.
- Token budget: no output-length constraint; input problem text can reach ~6,000 tokens; aggregate tokens NOT REPORTED.
- Runtime / wall-clock: NOT REPORTED.
- Hardware: local smaller open models on **4 NVIDIA H800 PCIe 80GB GPUs**; larger/open and closed models via cloud services.
- Metrics: Accuracy, Feasibility, Hallucination, MRR, Top-1 probability, Top-3 probability; win/tie/lose vs graph algorithms.
- Statistical tests: NOT REPORTED.
- Confidence interval: NOT REPORTED.
- Ablation / intervention: CoT shots; code writing/execution; instruction tuning; parallel repeated sampling; sequential progressive-hint/checker feedback; graph tokenizer comparison.
- Sensitivity analysis: graph size; task complexity P vs NP; model scale; CoT shots; number of test-time attempts; graph encoding/tokenizer.
- Generalization / OOD: real-world vs synthetic graph comparison; small vs large graphs; multiple graph domains/tasks.
- Robustness: broad task/model/scale coverage, but no statistical repeated-run robustness.
- Dynamic-event design: NOT PRESENT.
- LLM API / inference cost: cost motivates single-run design; exact monetary cost NOT REPORTED.

## C｜Writing Evidence Coding
### Introduction
Actual sequence: **M1 LLM evaluation challenge → M3 existing benchmark families → M2 graphs as evaluation substrate → M3 graph benchmarks → M4 three explicit benchmark limitations → M6 GraphArena → M7 three bullet contributions → research questions + headline empirical findings**.
- Limitation appears before method as an explicit three-part diagnosis: synthetic graphs, shallow tasks, weak string-match evaluation.
- Method follows directly as a one-to-one response to those limitations.
- Contributions: **3 numbered/bulleted core improvements**, followed by 2 explicit research questions and summarized findings.
- Empirical diagnosis before method: NO experimental diagnosis, but strong benchmark-design diagnosis.

### Related Work
- Standalone Section 4 after experiments.
- Organization by method family: LLM evaluation → Neural Algorithmic Reasoning → LLM on Graphs.
- It positions GraphArena against prior graph benchmarks by depth/realism rather than chronology.

### Gap language
- Uses concrete enumerated limitations (`First`, `Second`, `Third`) instead of a vague literature-scarcity claim.
- `To address these issues` is the main limitation→method transition.
- The strongest writing pattern is **limitation-to-design correspondence**: each diagnosed weakness maps to a named benchmark feature.

### Contributions
- 3 bullet contributions: realistic graph collection; comprehensive task selection; rigorous path-based evaluation.
- Experimental/empirical contribution follows through two RQs rather than being mixed into the three design bullets.
- Benchmark contribution is central.

### Experimental writing
- Experimental setup explicitly states the reason for **one run per model**: computational demand/cost. This is useful evidence that repeated-run practice depends on experiment type and cost, not ritual.
- Results separate accuracy from feasibility and hallucination, avoiding a single metric that hides infeasible outputs.
- Scale sensitivity is a central axis, not an appendix afterthought.
- Comparisons include deliberately weak Random/Greedy and stronger approximation algorithms, revealing whether LLM performance beats trivial heuristics.
- Improvement experiments report negative findings: more CoT can degrade performance; code execution can hurt small cases; more test-time compute reduces hallucination more reliably than it improves optimal accuracy.
- Appendix extends per-task, baseline, tokenizer, real-vs-synthetic and prompt evidence rather than merely repeating main tables.
