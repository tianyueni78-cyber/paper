# 37｜MA-GTS 全文编码

- Source: `LLM/37_MA-GTS.md`
- Full-text status: **YES**
- Last read position: **EOF (line >600 empty); Appendices A–E covered**
- Corpus: LLM / algorithm selection / graph optimization
- Tier: A（Mechanistically Close）

## A｜Research Content
- Research problem: solve noisy, implicit, real-world graph problems where LLMs struggle with graph extraction, scale and algorithm choice.
- Problem setting: natural-language real-world graph task → extract semantics/problem/graph → select graph algorithm based on problem and graph scale → execute code → self-check solution.
- Objectives: improve graph-problem accuracy, scalability, robustness and inference cost; create realistic graph benchmark G-REAL.
- Algorithm backbone: hierarchical multi-agent pipeline IEL → KIL → AEL, backed by Graph Theory Knowledge Base and Graph Theory Algorithm Library.
- Proposed mechanism: specialized agents extract text, problem type and graph structure; SGIA standardizes representation; GTA retrieves candidate algorithms and chooses `Alg*` based on problem constraints, graph properties/size and algorithm applicability/complexity; ASA loads code, executes and repeatedly self-checks.
- Decision layer: **Algorithm selection + runtime algorithm execution/control**. GTA selects a full graph algorithm, not a local search operator.
- State / Context: extracted text/background, problem type/objective/constraints, graph structure, node scale/characteristics, knowledge-base algorithm descriptions/applicability, standardized graph.
- Action / Decision: select algorithm from library; transform representation; invoke matching algorithm code; self-check/refine output.
- Feedback / Reward: execution output, constraint/result verification and self-check; no learned scalar reward.
- Dynamic mechanism: algorithm choice is context-dependent per problem/graph scale; repeated self-check at runtime. No online performance-learning of algorithm competence and no external scheduling events.
- LLM role: semantic/graph extraction, problem classification, algorithm selection/rationale, orchestration and interpretation/self-check.
- RL role: NOT PRESENT.
- Claimed contribution: MA-GTS multi-agent graph framework; G-REAL benchmark; collaboration/algorithm-selection mechanism with high accuracy/cost efficiency.
- Explicit limitation: G-REAL may not capture full real-world diversity; large problems may remain computationally expensive; highly dependent/specialized graph structures may bottleneck LLMs; open-source tool invocation remains insufficient/unstable; future work larger scale and lower cost.
- 与当前 FJSP-AGV 研究关系: **strong direct boundary for contextual selection**. MA-GTS already maps problem context + constraints + graph scale/structure + algorithm applicability to a context-dependent algorithm choice and then executes/verifies it. Therefore `LLM reads context and selects suitable strategy/algorithm` is definitely not enough. Difference for current work must be lower-level **search operator selection within one optimizer**, dynamic scheduling/search/Pareto context, empirical operator-effect competence rather than static knowledge-base applicability, and feedback-driven competence update/redesign if supported by remaining corpus.

## B｜Experimental Design Coding
- Dataset / Benchmark: G-REAL; GraCoRe; NLGraph.
- Instance scale: G-REAL four tasks, node range 8–25; Table 1 reports 900 graphs/task; text §4.2 says each sub-dataset includes 50 instances with distinct structures, creating an internal reporting ambiguity that must not be silently reconciled. Appendix D extends TSP/Coloring to 25/30/35/40 nodes, 5 instances/size.
- Baselines: six standalone LLMs (o3-mini, GPT-4o-mini, GPT-3.5, Qwen2.5-7B, Llama3-7B/8B naming varies, DeepSeek-V3-660B) under Direct/CoT; OWL; GraphTeam; base-model tool-use condition in ablation.
- Baseline 数量: **8 named external baseline systems/models** if counting six LLMs + OWL + GraphTeam; Direct/CoT are inference modes, not separate models.
- Independent runs: sensitivity: 5 randomly selected problems per graph dataset size × **5 queries/problem**; runtime: 5 random 15-node G-REAL-TSP graphs; extended-scale: 5 instances/size.
- Random seeds: NOT REPORTED.
- Population size: NOT APPLICABLE.
- Generations: NOT APPLICABLE; self-check number `Ncheck` symbolic, exact default NOT REPORTED.
- Evaluation budget: no unified call budget reported.
- Fitness / function evaluations: NOT APPLICABLE.
- Real decoding count: multiple agent calls; aggregate count NOT REPORTED.
- Solver calls: algorithm library/tool calls occur; aggregate NOT REPORTED.
- LLM calls: aggregate NOT REPORTED.
- Token budget: input/output tokens reported by task in cost table; no fixed token cap reported.
- Runtime / wall-clock: Appendix D G-REAL-TSP 15-node average: MA-GTS **148.48s**, GraphTeam 251.34s, OWL 139.39s on five graphs.
- Hardware: NOT REPORTED.
- Metrics: `ACC_ALL=0.5 ACC_nodes+0.5 ACC_result`; task accuracy; error rate; input/output tokens; dollar price; runtime; variance/std/mean in repeated-query sensitivity.
- Statistical tests: NOT REPORTED. Text uses `significantly` without inferential test.
- Confidence interval: NOT REPORTED.
- Ablation: w/o IEL; w/o KIL; w/o AEL; tool-use-only; full MA-GTS.
- Sensitivity analysis: repeated-query stability, 5 problems ×5 queries; reports variance/std/mean.
- Generalization / OOD: G-REAL vs simpler GraCoRe/NLGraph; multiple problem types; closed/open base models; larger 25–40 node appendix.
- Robustness: noise/random naming/implicit structure; repeated queries; node-scale analysis.
- Dynamic-event design: NOT PRESENT despite intro mentioning dynamic variations generally.
- LLM API / inference cost: explicit per-task token counts and dollar price; MA-GTS reported ~80.7–94.8% lower dollar cost than o3-mini across G-REAL tasks in Table 3.

## C｜Writing Evidence Coding
### Introduction
Actual sequence: **M1 graph applications/complexity → M3 traditional algorithms/heuristics → M4 scalability/tuning limitations → M3 LLM roles → M4 three explicit LLM/agent challenges → M6 MA-GTS mechanism → benchmark/dataset preview → M7 three contributions**.
- Limitation starts paragraph 1 for traditional methods and becomes explicit three-part LLM limitation in paragraph 2.
- Method follows immediately with `To tackle these challenges...`.
- Contributions: **3**, enumerated with First/Second/Finally.
- Empirical diagnosis before method: NO.

### Related Work
- Two method-family blocks: `LLMs for Graph` and `LLM Agents`.
- Includes task taxonomy Enhancer/Predictor/Alignment for graph+LLM literature.
- generation vs selection: NO.
- direct solving vs solver-assisted: not formal taxonomy.
- single heuristic vs portfolio: NO.
- static vs adaptive/offline vs online: NO.

### Gap language
- Uses `However, significant challenges remain` followed by `Firstly / Secondly / Finally`, giving a clean multi-limitation chain.
- `These limitations highlight... and underscore the need...` converts limitations into motivation.
- Transition: `To tackle these challenges, we propose...`.
- Related Work uses `but ... mainly applied to standard graph structures, and their effectiveness ... remains uncertain` as a narrower evidence-shaped gap.
- Novelty wording `innovative`/`novel` is strong, but no universal first claim in contributions.

### Contributions
- Count: **3**, explicitly sequenced First/Second/Finally.
- Method: hierarchical multi-agent framework/collaboration and algorithm selection.
- Formulation: NO.
- Experimental: broad benchmark/model evaluation + ablations/cost/scale/sensitivity.
- Benchmark: YES, G-REAL.
- Empirical finding: high accuracy/cost efficiency/scalability in reported tests.

### Experimental writing
- Setup separates Datasets and Baselines/Foundation Model, followed by Results subsections by research question: real-world performance, simple problems, dataset effectiveness, node size, cost, ablation, sensitivity.
- Cost is treated as a first-class result with input/output tokens and actual dollar estimates, not merely runtime.
- Ablation directly maps to architecture layers and includes a `tool use only` condition to isolate algorithm-library access from multi-agent orchestration.
- Robustness/generalization evidence is decomposed into semantic noise, node scale, different benchmark difficulty, open/closed models and repeated-query variance.
- Runtime is relegated to appendix but measured against multi-agent baselines under the same base model.
- No inferential significance tests/CI despite repeated use of `significantly`.

## Asset Metadata

- FULL TEXT READ: YES
- Source: `LLM/37_MA-GTS.md`
- Decision Layer: Algorithm selection
- Current-study Relation: 限制宽泛 contextual selection novelty
- Innovation Boundary: 已占据或直接限制的边界：根据约束与图规模动态选择算法，证明 context-aware algorithm selection 已超出 heuristic selection。
- Best Writing Claim: 根据约束与图规模动态选择算法，证明 context-aware algorithm selection 已超出 heuristic selection。
