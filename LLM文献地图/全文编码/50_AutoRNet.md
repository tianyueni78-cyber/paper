# 50｜AutoRNet 全文编码

- Source: `LLM/50_AutoRNet.md`
- Full-text status: **YES**
- Last read position: **EOF (line >460 empty); Appendices A–C covered**
- Corpus: LLM / EA / complete heuristic generation
- Tier: A（AHD/domain-context/adaptive-fitness competitor）

## A｜Research Content
- Research problem: automatically design complete heuristics for robust network optimization rather than only LLM-generated scoring/weighting components, while handling a vast method space and hard structural constraints.
- Problem setting: improve robustness of scale-free and real-world networks against targeted highest-degree-node attacks, with edge-count/degree-distribution considerations.
- Objectives: generate complete domain-informed heuristics; use network knowledge to improve variation; progressively enforce structural constraints while preserving exploration/diversity.
- Algorithm backbone: EA over heuristic programs + GPT-4 Turbo code generation + Network Optimization Strategy (NOS)-conditioned variation + Adaptive Fitness Function (AFF).
- Proposed mechanism: individuals contain natural-language algorithm description, executable heuristic code and fitness; initialize diverse heuristics from task specification/optional seeds; E1/M1/M2 variation operators use domain NOSs for exploration/guided modification/local adjustment; AFF evaluates heuristics over training graphs and increases structural-deviation penalty with generation t; roulette-wheel survivor selection.
- Decision layer: **complete heuristic/operator generation + evolutionary search control + adaptive fitness shaping**; not online selection among a fixed operator portfolio.
- State / Context: heuristic population and fitness, generation index, training graph set, domain NOS library (features/strategies/actions), selected parent heuristic(s), structural deviation and robustness outcomes.
- Action / Decision: E1 creates substantially new heuristic from two parents + 12 random NOSs; M1 modifies heuristic with NOS guidance; M2 local-adjusts without NOS; survivor selection retains next population.
- Feedback / Reward: network robustness R plus AFF structural reward/penalty based on degree-distribution and edge-count deviations; penalty strength increases over generations.
- Dynamic mechanism: **generation-conditioned adaptive fitness** progressively tightens constraints; E1/M1/M2 are fixed-probability variation modes, not dynamically selected from search state.
- LLM role: generates initialization and complete executable heuristics; integrates domain knowledge supplied via NOS-conditioned prompts.
- RL role: NOT PRESENT.
- Claimed contribution: complete heuristic generation for complex domain; NOS domain-informed variation; AFF soft-to-hard constraint schedule; synthetic+real-network empirical gains.
- Explicit limitation: no dedicated Limitations section. General limitations NOT REPORTED. Paper itself notes LLMs with generic prompts struggled to exploit deep domain knowledge, motivating NOS; fixed NOS design remains manually constructed domain scaffolding.
- 与当前 FJSP-AGV 研究关系: strong boundary evidence. AutoRNet already provides **domain-contextual operator/heuristic generation**, distinct exploration/local-improvement modes, and **search-stage-dependent fitness shaping**. Therefore `domain knowledge + LLM operator design`, `different operators for exploration/exploitation`, and `search-stage adaptation` are not standalone novelty. Its variation-mode probabilities are fixed and it does not learn context-specific competence of each operator, compare predicted vs realized multiobjective effects, or trigger redesign from uncovered dynamic contexts.

## B｜Experimental Design Coding
- Dataset / Benchmark: synthetic BA scale-free networks + real EU power-grid network.
- Instance scale: training 24 graphs: N=50/100 × M0=2..5 ×3 instances. Testing: sparse BA N=100/200/300/500; BA N=100 with density parameter M0=2..5; EU grid N=1,494, E=2,066.
- Baselines: Hill Climbing (HC), Simulated Annealing (SA), Smart Rewiring (SR).
- Baseline 数量: **3**.
- Independent runs: **100 runs** for N=100–300; **30 runs** for N=500; **10 runs** for EU power grid.
- Random seeds: NOT REPORTED.
- Population size: **10**.
- Generations: **50**.
- Evaluation budget: training max_attempts=100 per heuristic; test BA max_attempts=3×10^4; EU grid=5×10^4, matched to baselines.
- Fitness / function evaluations: robustness R called repeatedly up to max_attempts; aggregate total across evolution NOT REPORTED.
- Real decoding count: initialization repeated to popsize; E1/M1/M2 generate offspring at pe1=.8, pm1=.1, pm2=.1 × popsize each generation; exact successful decoding count NOT REPORTED.
- Solver calls: NOT APPLICABLE.
- LLM calls: aggregate NOT REPORTED.
- Token budget: NOT REPORTED.
- Runtime / wall-clock: NOT REPORTED.
- Hardware: NOT REPORTED.
- Metrics: robustness R; Best, Worst, Average ± Variance; structural constraint preservation qualitatively/through heuristic behavior.
- Statistical tests: NOT REPORTED.
- Confidence interval: NOT REPORTED.
- Ablation: no formal component ablation table/experiment found. Comparisons among generated v1/v2/v3 reveal properties but are not controlled ablations.
- Sensitivity analysis: NOT PRESENT. AFF p fixed 1.5; variation probabilities fixed.
- Generalization / OOD: train on 50/100-node BA graphs, test up to 500-node BA plus 1,494-node real EU grid; density variation.
- Robustness: extensive independent runs and synthetic→real test; reports variance.
- Dynamic-event design: NOT PRESENT.
- LLM API / inference cost: GPT-4 Turbo, temperature=1; token/API monetary cost NOT REPORTED.

## C｜Writing Evidence Coding
### Introduction
Actual sequence: **M1 network robustness importance → M2 NP-hard problem/current methods → M4 manual/data/trial burden → M3 FunSearch/EoH → M4 only scoring/weighting components, not whole algorithms → M5 explicit need for whole-algorithm generation → M6 AutoRNet/NOS/AFF → M7 four bullet contributions**.
- Main limitation appears in paragraph 2 after naming closest LLM-AHD methods.
- Method follows immediately after an italicized explicit need statement.
- Contributions: **4 bullets**, not numbered numerically.
- Empirical diagnosis before method: limited. Section 4.4 reports an experimental observation that generic prompts only produce simple node/link operations, but the method is already being presented by then.

### Related Work
- Standalone Section 2 split by **domain-method family**: network robustness methods; LLMs in combinatorial optimization.
- Network robustness progression: traditional/local → metaheuristics → GNN/deep learning, each followed by limitations.
- LLM subsection narrows from general prompting to FunSearch/EoH and then whole-algorithm gap.
- Generation granularity, scoring component vs complete algorithm, is the key taxonomy boundary.

### Gap language
- `However, both FunSearch and EoH depend primarily on existing optimization algorithms...` is direct closest-competitor limitation.
- Italicized `There is a need to generate whole algorithms directly...` converts limitation into design target.
- Related Work repeats this exact gap and makes a stronger applicability claim; for our audit this remains an author claim, not corpus-wide fact.
- `To deal with...`, `To overcome...`, `To cure this problem...` repeatedly connect each diagnosed mechanism to a named component.

### Contributions
- Count: **4 bullet contributions**.
- Framework/method: EA+LLM complete heuristic generation.
- Operator/design contribution: NOS-based domain-specific variation.
- Fitness contribution: AFF softens/tightens hard structural constraints.
- Experimental contribution: eight scale-free settings + real-world network and baseline gains.
- Benchmark contribution: NOT PRESENT.

### Experimental writing
- Setup clearly separates **training graph construction**, **test graph scale/density/real network**, evaluation budget (`max_attempts`), EA parameters, LLM settings and independent-run counts.
- Fairness is explicit for search effort: test max_attempts is matched across generated heuristics and three baseline algorithms.
- Generalization is structurally meaningful: much larger test networks and a real graph are outside the small synthetic training sizes.
- Results do not hide heterogeneity: v2 is acknowledged as not best on every dense-network setting; v1 is discussed for constraint preservation/stability rather than only mean score.
- Reports Best/Worst/Average±Variance rather than only best-of-run.
- No formal significance test, CI, runtime, hardware, token/cost or controlled NOS/AFF ablation.

## Asset Metadata

- FULL TEXT READ: YES
- Source: `LLM/50_AutoRNet.md`
- Decision Layer: Algorithm generation
- Current-study Relation: 限制“整算法生成”创新
- Innovation Boundary: 已占据或直接限制的边界：从 scoring function 扩展到完整 domain heuristic / algorithm generation，说明自动设计对象持续扩大。
- Best Writing Claim: 从 scoring function 扩展到完整 domain heuristic / algorithm generation，说明自动设计对象持续扩大。
