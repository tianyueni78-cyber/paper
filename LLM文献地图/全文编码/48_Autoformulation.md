# 48｜Autoformulation 全文编码

- Source: `LLM/48_Autoformulation.md`
- Full-text status: **YES**
- Last read position: **EOF (line >880 empty); Appendices A–E covered**
- Corpus: LLM / optimization modeling / MCTS
- Tier: B（search/evaluation mechanism support）

## A｜Research Content
- Research problem: automatically transform natural-language requirements into solver-ready mathematical optimization formulations while handling a vast problem-dependent hypothesis space, uncertainty/redundancy in search, and semantic correctness evaluation.
- Problem setting: LP/IP/MILP optimization modeling from natural language.
- Objectives: formalize autoformulation as search; systematically explore hierarchical formulation components; prune trivial equivalence; guide search with partial/complete correctness evaluation.
- Algorithm backbone: hierarchical decomposition + LLM-enhanced MCTS + SMT symbolic pruning + deterministic parser + LLM/solver dual evaluation.
- Proposed mechanism: decompose formulation into parameters/decision variables, objective, equality constraints, inequality constraints; LLM generates H children conditioned on partial formulation; SMT/LLM removes equivalent branches; LLM ranks partial formulations and retains top I; terminal formulations receive comparative LLM correctness plus solver feedback; reward is backpropagated; UCT balances value and visit uncertainty.
- Decision layer: **optimizer/model formulation design and search-path selection**, not runtime scheduling/operator selection.
- State / Context: original problem description, current partial formulation/path, candidate sibling formulations, LLM prior value, backpropagated reward, visit counts, baseline formulations.
- Action / Decision: generate next formulation component; prune; select MCTS branch; output a set of functionally distinct complete formulations.
- Feedback / Reward: LLM comparative semantic-correctness evaluation + solver optimal-solve feedback; partial-node normalized rank priors; terminal reward backpropagated to path.
- Dynamic mechanism: node values evolve with accumulated terminal feedback; UCT changes exploration/exploitation as visit counts and values change; no external dynamic environment.
- LLM role: conditional hypothesis generator, decision-variable equivalence judge, partial-formulation ranker, complete-formulation comparative evaluator.
- RL role: NOT PRESENT.
- Claimed contribution: formal search framing/challenges; LLM+MCTS hierarchical exploration with symbolic pruning and dual evaluation; benchmark gains and component evidence.
- Explicit limitation: SMT equivalence may be undecidable for nonlinear/complex formulations; deterministic parser may need more sophisticated handling for complex transformations; objective-value proxy is not semantic correctness; benchmarks need larger/more diverse problem types; critical use requires expert oversight.
- 与当前 FJSP-AGV 研究关系: indirect but strong mechanism boundary. This paper already has **context/path-specific value estimates + uncertainty/visit counts + realized downstream feedback + backpropagated competence-like values + uncertainty-guided selection**. Therefore `contextual value estimation + uncertainty + feedback-updated selection` is not novel by itself. Current work must distinguish operator-specific, multidimensional realized effects under dynamic environment/search/Pareto context and competence-region coverage diagnosis, rather than MCTS node value over a formulation tree.

## B｜Experimental Design Coding
- Dataset / Benchmark: NL4OPT, IndustryOR, MAMO ComplexLP, ComplexOR.
- Instance scale: main text reports NL4OPT curated 244; IndustryOR 100; MAMO ComplexLP 211; ComplexOR benchmark 37, while Appendix B.3 says all 18 publicly available ComplexOR problems used. Appendix B.3 also describes labelled NL4OPT as 289. **Internal reporting discrepancy retained, not reconciled.**
- Baselines: Standard zero-shot, Reflexion, Chain-of-Experts, OptiMUS, ORLM; appendix Tree-of-Thought DFS and naive Sequential.
- Baseline 数量: 5 principal named baseline methods + 2 additional structural-search baselines.
- Independent runs: NOT REPORTED for main benchmark search.
- Random seeds: NOT REPORTED.
- Population size: NOT APPLICABLE; MCTS H=10 generated candidates, I=3 retained children.
- Generations: NOT APPLICABLE; T=16 rollouts.
- Evaluation budget: H=10, I=3, T=16; Pass@1/3/All; ORLM fair Pass@N uses N independent samples.
- Fitness / function evaluations: formulation correctness executions; aggregate count NOT REPORTED.
- Real decoding count: multiple LLM calls per expansion/evaluation; aggregate NOT REPORTED.
- Solver calls: terminal formulations parsed/executed; aggregate NOT REPORTED. Appendix E uses 100 random samples per solver/problem-size condition.
- LLM calls: aggregate NOT REPORTED.
- Token budget: NOT REPORTED.
- Runtime / wall-clock: main autoformulation wall-clock NOT REPORTED. Appendix E reports solver times.
- Hardware: NOT REPORTED.
- Metrics: execution accuracy with 5% objective tolerance, Pass@k, Best-of-N, search-space retained nodes/efficiency, biserial correlation, p-values, tree entropy, expert component error rates; Appendix E success rate/optimality gap/solve time.
- Statistical tests: biserial correlation significance for complete-formulation evaluator: r=0.48, p=2.0681e-3; direct scoring r=0.23, p=1.1185e-1. Other formal tests NOT REPORTED.
- Confidence interval: NOT REPORTED.
- Ablation: Tree-of-Thought and Sequential structural baselines; ranking/comparative evaluation analyses; symbolic pruning/search-selection analysis.
- Sensitivity analysis: rollout count N and discovery curve; no systematic H/I/UCT-constant sensitivity reported.
- Generalization / OOD: four benchmarks spanning LP/IP/MILP and real domains; Appendix categorizes Type I–III but main empirical autoformulation evaluation remains concentrated on linear/integer/mixed-integer problems.
- Robustness: expert review of 18 ComplexOR autoformulations; 82% agreement with objective-value proxy; no repeated-seed robustness report.
- Dynamic-event design: NOT PRESENT.
- LLM API / inference cost: GPT4-0613 for experiments; token/API monetary cost NOT REPORTED.

## C｜Writing Evidence Coding
### Introduction
Actual sequence: **M1 optimization importance → M2 traditional modeling pipeline → M4 human formulation bottleneck → M2 autoformulation definition/value → M5 three explicit search challenges → M3 prior LLM autoformulation capabilities → M5 focus on systematic exploration/correctness → M6 three innovations → M7 three numbered contributions**.
- Limitation/bottleneck appears immediately after domain/process setup.
- Method follows an explicit three-challenge diagnosis.
- Contributions: **3 numbered items**.
- Empirical diagnosis before method: NO dedicated new empirical section before method, but conceptual diagnosis is unusually formal; empirical mechanism validation follows in Section 5.

### Related Work
- Standalone Section 4 after method.
- Organized by **method family/function**: Advances in LLMs → Autoformulation → Planning.
- Explicitly contrasts complete-formulation multi-agent generation with hierarchical MCTS search, and plan generation/selection with domain-specific symbolic pruning/evaluation.
- Not chronological as primary structure.

### Gap language
- `Despite major advances... still relies largely on human expertise` establishes bottleneck by contrast.
- Three named challenges [C1–C3] convert vague gap rhetoric into concrete unresolved mechanisms.
- `Building upon these contributions, our work focuses...` avoids claiming absence and narrows the remaining question.
- `Our approach builds on these works, differing in three key ways` performs competitor-relative positioning.
- Limitations are expressed through scope/decidability/proxy validity rather than a generic limitation list.

### Contributions
- Count: **3**, numbered.
- Formulation/conceptual contribution: formalize autoformulation as search and identify challenges.
- Method contribution: LLM + MCTS + symbolic pruning + dual evaluation.
- Experimental contribution: benchmark gains and component analysis.
- New benchmark contribution: NOT PRESENT.

### Experimental writing
- Experiment section announces three evaluation questions before results: benchmark performance, correctness evaluation, pruning efficiency, then broader failure analysis.
- Baseline rationale distinguishes prompting, reasoning, specialized multi-agent autoformulators, and finetuned specialist model.
- Fairness: same GPT4-0613 for applicable baseline experiments; ORLM Pass@N uses matched N independent samples; convergence/search comparison explicitly recognizes candidate-count differences.
- Component validation is mechanism-aligned rather than generic ablation: evaluator correlation, partial-value greedy-vs-random, pruning retained fraction, structural baselines, discovery curve, expert error analysis.
- Authors preserve proxy limitations by manually auditing 18 cases and reporting mismatches, rather than treating matching objective value as semantic proof.
- Appendix E separately demonstrates why formulation choice and solver choice affect optimality/runtime, using 100 random samples.
- Main paper does not report hardware, total runtime, token budget, API cost, CI, or repeated random seeds.
