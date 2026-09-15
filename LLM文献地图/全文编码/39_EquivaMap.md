# 39｜EquivaMap 全文编码

- Source: `LLM/39_EquivaMap.md`
- Full-text status: **YES**
- Last read position: **EOF (line >900 empty); Appendices A–D covered**
- Corpus: LLM / OR modeling verification
- Tier: B（Supporting）

## A｜Research Content
- Research problem: automatically and reliably determine whether two optimization formulations are equivalent, especially for evaluating LLM-generated optimization models.
- Problem setting: feasible bounded LP/MILP formulations of the same optimization problem; formulations may differ structurally through slack variables, valid inequalities, rescaling, auxiliary variables, variable decomposition, etc.
- Objectives: define a principled equivalence notion; discover variable mappings automatically; verify equivalence without relying on fragile objective/structural heuristics; create a benchmark.
- Algorithm backbone: Quasi-Karp Equivalence + LLM symbolic mapping discovery + solver-derived optimal solution + lightweight feasibility/optimality verification + stochastic K-attempt aggregation.
- Proposed mechanism: LLM receives symbolic variable descriptions, constraints and objective participation; generates a linear mapping from variables of one formulation to another; mapped optimal solution is substituted into target formulation and checked for feasibility/optimality.
- Decision layer: **Verification / formulation mapping**, not scheduling or heuristic/operator selection.
- State / Context: two symbolic formulations; variable descriptions; constraints involving each variable; objective participation; set-level variable structure.
- Action / Decision: output a linear variable mapping; final Boolean equivalence classification after verifier.
- Feedback / Reward: verifier checks mapped solution feasibility and optimal objective equality. No learned reward.
- Dynamic mechanism: stochastic repeated LLM attempts (`K=3`) aggregated by any-valid-mapping rule; no online learning/adaptation.
- LLM role: symbolic mapping finder between formulation variable spaces.
- RL role: NOT PRESENT.
- Claimed contribution: identify failures of existing equivalence metrics; Quasi-Karp equivalence; EquivaMap; EquivaFormulation dataset of equivalent/non-equivalent transformations.
- Explicit limitation: current work focuses on relatively straightforward transformations and omits more intricate reformulations such as decomposition algorithms; future work may need tools for more complex transformations/cross-problem equivalence. LLM call dominates runtime. Standalone Limitations heading NOT PRESENT; limitations appear in Discussion/Runtime.
- 与当前 FJSP-AGV 研究关系: supporting methodological evidence for **LLM proposal + deterministic/external verification**. It does not compete at operator selection, but shows that LLM outputs can be treated as candidate structured decisions and accepted only after objective/feasibility evidence. For current work this supports separating `LLM predicted operator effect/choice` from `actual decoder/search outcome`; however that architecture itself is not a novelty claim.

## B｜Experimental Design Coding
- Dataset / Benchmark: EquivaFormulation constructed from NLP4LP.
- Instance scale: seven equivalent transformations and three non-equivalent transformations. Per transformation sizes vary, e.g. equivalent LP 44–92 and MILP 115–142; non-equivalent LP 53–87 and MILP 120–142. Exact raw fractions are reported in Appendix A.
- Baselines: Canonical Accuracy; Execution Accuracy; WL-test; naive-LLM.
- Baseline 数量: **4**.
- Independent runs: stochastic EquivaMap executes **K=3 attempts per pair**; conventional independent experimental repetitions beyond this NOT REPORTED.
- Random seeds: NOT REPORTED.
- Population size / generations: NOT APPLICABLE.
- Evaluation budget: K=3 LLM mapping attempts; solver obtains optimal solutions for formulations used by verifier. Aggregate total calls NOT REPORTED.
- Fitness / function evaluations: NOT APPLICABLE.
- Real decoding count: up to 3 LLM mapping outputs per formulation pair.
- Solver calls: required for optimal solutions; exact aggregate count NOT REPORTED. Verification itself is described as avoiding additional solver calls after solutions are available.
- LLM calls: K=3 per pair for EquivaMap; naive-LLM call schedule not explicitly quantified beyond evaluation.
- Token budget: NOT REPORTED.
- Runtime / wall-clock: Appendix D mean±std seconds/instance: Execution Accuracy 0.12±0.02; WL-test 0.38±0.07; EquivaMap solving 0.12±0.02 + LLM 11.88±4.48 = **12.00±4.50 s**.
- Hardware: NOT REPORTED.
- Metrics: classification accuracy; raw correct/total fractions; runtime mean±std.
- Statistical tests: NOT REPORTED despite `significantly outperforms` language.
- Confidence interval: NOT REPORTED.
- Ablation: no formal component ablation; naive-LLM acts as mechanism contrast removing explicit mapping+verification.
- Sensitivity analysis: K sensitivity NOT REPORTED.
- Generalization / OOD: LP vs MILP and ten transformation types; no separate OOD split.
- Robustness: random permutation of parameters/variables/constraints and distinct variable names/LLM-generated descriptions to prevent shortcut exploitation; equivalent and non-equivalent transformations test false negatives/positives.
- Dynamic-event design: NOT PRESENT.
- LLM API / inference cost: monetary cost NOT REPORTED; LLM runtime reported.

## C｜Writing Evidence Coding
### Introduction
Actual sequence: **M1 CO importance → M2 formulation equivalence importance/history → M3 optimization copilots create new evaluation need → M4 heuristic equivalence checks lack precise reliable definition → M6 Quasi-Karp + EquivaMap → M7 three bullet contributions**.
- Limitation/gap appears after optimization-copilot motivation.
- Method follows directly with `Towards precise and reliable equivalence checking...`.
- Contributions: **3 bullets**, second bullet bundles formalism+method, third bundles dataset+empirical result.
- Empirical diagnosis before method: conceptual counterexamples/pitfalls are announced, not a data-driven diagnosis.

### Related Work
- Organized by three explicit families: CO/MILP foundations; Language Models for MILP Modeling; Existing Automatic Equivalence Checking Methods.
- traditional→learning→LLM: partially, via foundations → LLM modeling → evaluation methods.
- direct solving vs solver-assisted: not main taxonomy.
- generation vs selection / static vs adaptive / offline vs online: NO.
- The final equivalence-checking subsection is especially mechanism-oriented: canonical declaration matching → objective execution → graph structural similarity, each followed by a failure mode.

### Gap language
- `However, ... hinges on reliable evaluation mechanisms` moves opportunity to requirement.
- `Despite the importance ... existing automatic approaches rely heavily on heuristics ... and lack a precise ... definition` states the central gap.
- `Towards precise and reliable equivalence checking, we propose...` is the method transition.
- Method section deliberately demonstrates **pitfalls of existing methods before formalizing the new definition**, giving a strong problem-diagnosis → formalism → mechanism progression.

### Contributions
- Count: **3**, bullets.
- Problem/diagnostic contribution: identify pitfalls.
- Formulation/theory contribution: Quasi-Karp equivalence.
- Method contribution: EquivaMap mapping+verification.
- Benchmark contribution: EquivaFormulation.
- Experimental contribution: transformation-wise comparison against four baselines.

### Experimental writing
- Experiments first define benchmark transformations, including both positive and negative cases, then actively modify names/order/descriptions to prevent shortcut exploitation.
- Baseline design covers distinct failure mechanisms rather than merely many SOTA systems: declaration matching, objective matching, graph isomorphism, naive LLM.
- Main table reports worst-case plus transformation-level accuracy; appendix gives raw numerator/denominator separately for LP/MILP, making results highly traceable.
- Mechanism contrast is explicit: naive LLM vs structured map finding + verification.
- Runtime reports mean±std and decomposes solver vs LLM time, identifying LLM interaction as bottleneck.
- Discussion openly scopes the limitation to relatively straightforward transformations.
