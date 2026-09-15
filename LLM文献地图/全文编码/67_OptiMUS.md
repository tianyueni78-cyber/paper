# 67｜OptiMUS 全文编码

- Source: `LLM/67_OptiMUS.md`
- Full-text status: **YES**
- Last read position: **EOF (line >940 empty); Appendix A and prompt Appendix B covered**
- Corpus: LLM / optimization modeling agent
- Tier: A/C

## A｜Research Content
- Research problem: automatically formulate and solve LP/MILP from long, ambiguous natural-language descriptions and large data while detecting/correcting unreliable LLM outputs.
- Problem setting: natural language optimization problem → structured problem → multi-agent formulation/programming/evaluation → Gurobi execution/debugging.
- Objectives: improve accuracy and scalability of LLM optimization modeling; support long descriptions/data; release NLP4LP.
- Algorithm backbone: preprocessing + manager/formulator/programmer/evaluator agents + connection graph + external solver.
- Proposed mechanism: preprocessing separates parameters/data/clauses/background; connection graph links clauses to relevant variables/parameters so each prompt retrieves local context; manager repeatedly selects specialist agents; evaluator executes code and returns errors; programmer/formulator repair identified faults.
- Decision layer: **Optimizer/model formulation generation + agent/task selection + runtime modeling workflow control**. It is not heuristic/operator selection inside an optimization search.
- State / Context: structured problem, connection graph, conversation history, agent messages, runtime errors; manager sees conversation history to choose next agent/task.
- Action / Decision: manager chooses formulator/programmer/evaluator and task; formulator creates/fixes formulations; programmer creates/fixes code; evaluator executes/checks.
- Feedback / Reward: solver/runtime evaluation and error explanations; no scalar learned reward.
- Dynamic mechanism: iterative manager-driven agent routing and debugging until Done; harder instances induce more calls.
- LLM role: all specialist/manager reasoning and generation roles.
- RL role: NOT PRESENT; RL for manager agent selection is explicitly proposed as future work.
- Claimed contribution: NLP4LP 67-instance difficult benchmark; modular OptiMUS architecture; connection graph/local context mechanism; strong empirical accuracy gains.
- Explicit limitation/future boundary: small models perform poorly; user feedback may help; automatic solver selection and RL-based manager selection are future directions; failure analysis shows incorrect modeling/missing constraints/coding errors.
- 与当前 FJSP-AGV 研究关系: important mechanism-boundary evidence. **History/context → LLM chooses next expert/action → execute → error feedback → route/repair** existed in 2024 optimization modeling. Therefore generic context-aware supervisory routing and feedback-driven correction are not novel. It does not model search-state/Pareto-state operator competence or dynamic FJSP-AGV scheduling.

## B｜Experimental Design Coding
- Dataset / Benchmark: NL4OPT; modified ComplexOR; NLP4LP.
- Instance scale: NL4OPT 1101; ComplexOR 21 used of 37; NLP4LP 67 = 54 LP + 13 MILP.
- Baselines: Standard prompting, Reflexion, Chain-of-Experts (CoE).
- Baseline 数量: **3 external framework baselines** in main comparison.
- Independent runs: NOT REPORTED.
- Random seeds: NOT REPORTED.
- Population size: NOT APPLICABLE.
- Generations: NOT APPLICABLE.
- Evaluation budget: dataset-wide; manager maximum agent-call sensitivity 3–10.
- Fitness/function evaluations: NOT APPLICABLE.
- Real decoding count: NOT REPORTED aggregate.
- Solver calls: evaluator executes generated Gurobi code; aggregate count NOT REPORTED.
- LLM calls: variable by instance; average per-agent call frequencies plotted; exact aggregate NOT REPORTED.
- Token budget: NOT REPORTED as cap; prompt lengths reported as mean±std.
- Runtime/wall-clock: NOT REPORTED.
- Hardware: NOT REPORTED.
- Metrics: final accuracy; prompt length; agent call frequency; normalized failure categories. CE/RE discussed but deliberately not used for main comparison because executable irrelevant code can game them.
- Statistical tests: NOT REPORTED.
- Confidence interval: NOT REPORTED.
- Ablation: w/o debugging; GPT-3.5 manager; all GPT-3.5; Mixtral-8x7B.
- Sensitivity analysis: maximum manager agent calls 3–10; internal agent-call patterns; prompt length/scalability.
- Generalization/OOD: three datasets with different complexity/length; no formal unseen-distribution OOD split.
- Robustness: failure-case taxonomy; no stochastic robustness protocol.
- Dynamic-event design: NOT PRESENT.
- LLM API/inference cost: NOT REPORTED.

## C｜Writing Evidence Coding
### Introduction
Actual sequence: **M1 optimization importance → M4 expert-access barrier → M3 LLM opportunity → M4 four concrete LLM limitations (ambiguity, long descriptions, large data, unreliable outputs) → M7 explicit Contributions → paper structure**.
- Limitation appears before method and is unusually concrete, decomposed into four operational failure modes.
- Method is introduced in Abstract/Figure 1 and contribution bullet 2, then detailed Section 3.
- Contributions: **2 main bullets**, one benchmark and one method/performance contribution.
- Empirical diagnosis before method: NO, but the problem diagnosis is highly operational.

### Related Work
- Standalone Background and Related Work.
- Organized by method family: LLM progress/tool use; chatbots for optimization; benchmark-driven optimization modeling; comparison to MIPLIB boundary.
- Explicitly distinguishes direct LLM optimization, assistant/chatbot roles and end-to-end modeling.

### Gap language
- Gap is framed through **specific failure modes and scalability constraints**, not generic scarcity.
- Strong rhetorical pattern: concrete real-world requirement → why existing prompt-based approach breaks → architectural mechanism targeted at that failure.

### Contributions
- 2 explicit bullets.
- Benchmark contribution: NLP4LP.
- Method contribution: modular agent + connection graph + data separation, accompanied by empirical performance claims.

### Experimental writing
- Baselines are justified by role: Reflexion as high-performing general-purpose framework; CoE as SOTA NL optimization modeling method.
- Metric choice is defended by identifying how compilation/runtime-error metrics can be gamed; accuracy is therefore retained as outcome metric.
- Ablation directly maps architectural components/models to performance.
- Sensitivity probes an internal control parameter, maximum agent calls, and explains why hard datasets benefit from iterative repair.
- Failure analysis classifies incorrect modeling, missing constraints and coding errors rather than hiding unsuccessful cases.
- Computational-cost reporting is weak: prompt length/call frequency are shown, but runtime, hardware and monetary API cost are NOT REPORTED.
