# 25｜Using Reasoning Models to Generate Search Heuristics 全文编码

- Source: `LLM/25_Reasoning-Models-Heuristics.md`
- Full-text status: **YES**
- Last read position: **EOF (line >750 empty); Appendices A–B covered**
- Corpus: LLM / AHD / mathematical discovery
- Tier: B（Mechanistically relevant）

## A｜Research Content
- Research problem: 用 reasoning LLM 自动生成、调参和优化 heuristic search programs，尝试构造长期未解的 combinatorial design open instances。
- Problem setting: 16 Handbook combinatorial design types + 4 Feb-2025 problems + Cap Sets/Deletion Codes；输入为 textual definition + Dev/Open instance lists + Python verifier。
- Objectives: generate effective search strategies/programs that construct verifier-valid open-instance solutions；compare reasoning vs non-reasoning LLMs；analyze protocol components。
- Algorithm backbone: **CPro1 protocol**: massive candidate generation → automated grid hyperparameter tuning → verifier scoring → top-5 code-speed optimization → long dev test → top-2 48h open-instance execution。
- Proposed mechanism: LLM open-endedly proposes strategy, elaborates details, implements C code + hyperparameter ranges；external execution/verifier supplies empirical feedback；automated tuning/ranking filters candidates；LLM repeatedly optimizes top code。
- Decision layer: **Heuristic/operator/optimizer generation**，open-ended search-strategy design；not runtime heuristic selection。
- State / Context: textual problem definition, strategy/detail conversation context, candidate C code, hyperparameter ranges, execution score/performance feedback。
- Action / Decision: generate strategy/code; tune parameters; modify code for speed/performance; rank/filter candidates。
- Feedback / Reward: verifier validity + Dev-instance execution score + runtime performance；final open solution must pass verifier。
- Dynamic mechanism: iterative generate-evaluate-optimize protocol; NOT dynamic scheduling environment。
- LLM role: strategy ideation, implementation, reasoning, code optimization。
- RL role: proposed protocol does **NOT** train RL；reasoning LLMs themselves were pretrained with RL, but that is model provenance, not CPro1 algorithm role。
- Claimed contribution: reasoning LLM+CPro1 resolves open instances in 7/16 Handbook design types, 3/4 recent design problems, and improves Deletion Codes; demonstrates automated computational experimentation for research-level constructions。
- Explicit limitation: positive results may exploit low-hanging fruit where computational effort historically limited; cannot prove non-existence; only one full-scale run per LLM/problem and LLM nondeterminism means repeat runs may differ; fails on heavily studied Covering Arrays and FunSearch Cap Set result; 1000 candidates far below FunSearch scale; randomized solutions often have little mathematical structure。
- 与当前 FJSP-AGV 研究关系: 进一步封死“LLM生成策略 + verifier/真实性能反馈 + 自动调参 + 反复改进代码”作为单独创新。它强调真实执行反馈和严格 verifier，但不做 online state-conditioned operator selection、multiobjective Pareto feedback、dynamic events 或 competence-region modelling。

## B｜Experimental Design Coding
- Dataset / Benchmark: 16 selected Handbook combinatorial design types; 4 Feb-2025 literature problems; Cap Sets and Deletion Codes from FunSearch work。
- Instance scale: per problem Dev instances + specific Open instances; exact total instance count across all tasks **NOT REPORTED as one aggregate**。
- Baselines: CPro1 GPT-4o non-reasoning; o3-mini-high; DeepSeek R1 on prototyping set; FunSearch comparisons on Cap Sets/Deletion Codes; hand-coded/local specialized literature methods contextually compared。
- Baseline 数量: varies by experiment; no single global baseline count。
- Independent runs: full-scale **one run per included LLM per design type**; scaled-down analysis **25 repeated runs** for 4 Handbook problems derived from 1000/40 candidate partitions。
- Random seeds: **NOT REPORTED**。
- Population size: initial **1000 candidate programs** = 50 reps × 20 strategies；top 5 → top 2。
- Generations: not EA generations; code optimization max **5 rounds**, 50 proposed improvements/round。
- Evaluation budget: initial candidates up to 50 sec; hyper-tune up to 1000 grid points×0.5s, top100×5s, top10×50s; top5 final Dev 2h; top2 Open 48h; scaled-down 40 candidates/run and 2h open runtime。
- Fitness / function evaluations: verifier/execution based; exact aggregate evaluations NOT REPORTED beyond protocol budgets。
- Real decoding count: initial strategy/detail/code generation pipeline yields 1000 candidate programs; optimization can query 50 proposals × up to 5 rounds × top5; exact realized count after early breaks NOT REPORTED。
- Solver calls: no generic external solver; candidate executable runs + Python verifier; aggregate calls NOT REPORTED。
- LLM calls: implied many calls; exact total API calls NOT REPORTED。
- Token budget: **NOT REPORTED**。
- Runtime / wall-clock: full CPro1 run/problem **~6–10 days**；2h Dev, 48h Open final budgets。
- Hardware: Linux, AMD Ryzen 9 7950X3D CPU, 128GB memory, machine dedicated to one run at a time。
- Metrics: number/open instances solved; candidate score on Dev; scaled-down success rate。
- Statistical tests: scaled-down o3-mini-high vs GPT-4o uses **Z-test, p<0.0001** for each of 4 problems。
- Confidence interval: **95% Clopper-Pearson CI** for 25-run success rates。
- Ablation: cumulative removal/reduction: Reduce runtime 48h→2h; No final dev test; No optimization; No hyper tuning；performed for o3-mini-high and GPT-4o on successful Handbook problems。
- Sensitivity analysis: no general parameter sensitivity sweep beyond hyperparameter tuning and scaled-down protocol study。
- Generalization / OOD: tests Dev→Open unseen/open instances; adjacent open instances after success; cross-problem types including recent literature。
- Robustness: scaled-down 25 repeated runs provide stochastic success-rate evidence; full-scale repeat robustness explicitly limited to one run。
- Dynamic-event design: NOT PRESENT。
- LLM API / inference cost: monetary cost **NOT REPORTED**。

## C｜Writing Evidence Coding
### Introduction
Actual sequence: **M2 combinatorial-design existence/open-instance definition → concrete SymmW example → M3 heuristic computational search + prior CPro1 → M6 reasoning-LLM extension → empirical headline results → boundary where sustained specialized research defeats method**。
- Domain/problem is introduced immediately rather than broad motivational rhetoric。
- Limitation/gap: open instances and difficulty of computational/manual search appear from opening; reasoning-vs-nonreasoning extension framed as direct continuation rather than elaborate “gap paragraph”。
- Method appears: paragraph 3 through prior CPro1 + current reasoning LLM modification。
- Contributions: conventional numbered/bulleted M7 list **NOT PRESENT**；headline achievements stated in prose/Table 1。
- Empirical diagnosis before method: NO。

### Related Work
- Dedicated Section 2, short and method-family based: LLM code generation/heuristics → LLM mathematics/proof → prior CPro1 → AI mathematical construction/FunSearch。
- chronological: secondary。
- generation vs selection: NO taxonomy。
- direct solving vs solver-assisted: contrast is proof generation vs verifier-checkable constructive search, not formal taxonomy。
- single heuristic vs portfolio: NO。
- static vs adaptive/offline vs online: NO。

### Gap language
- Paper uses restrained problem-driven framing more than formulaic novelty rhetoric。
- Contrast: `But these may leave behind...`; `While we don’t see success... we do see strong results...`; `Compared to FunSearch...`。
- Limitation/challenge: open existence status, lengthy proof difficulty, heavily studied problem classes, computational scale。
- Motivation: builds directly on earlier CPro1 and asks whether reasoning LLM improves it。
- Strong `first/few/unexplored` novelty claims: NOT prominent in Introduction。

### Contributions
- Formal contribution list: **NOT PRESENT**。
- Method contribution: reasoning-model use within CPro1 is incremental protocol extension。
- Experimental/empirical contribution: central, resolving verified open instances and comparing model/protocol variants。
- Benchmark contribution: NO new benchmark, but curated open-problem set。
- Empirical finding contribution: YES, dominant paper contribution。

### Experimental writing
- Protocol is specified algorithmically **before** Results with unusually concrete compute funnels: 1000 → 5 → 2 candidates and seconds/hours/days budgets。
- Problem selection has explicit inclusion logic and distinguishes prototyping set from evaluation problems, reducing contamination/development leakage ambiguity。
- Main Results begin with solved-instance outcomes rather than aggregate objective values。
- Ablation is cumulative protocol simplification and records which problem-specific strategy still succeeds, rather than conventional scalar metric-only ablation。
- Scaled-down repeated-run section separately repairs the lack of repetition in expensive full-scale runs and supplies 95% CI + Z-test。
- Limitations has a dedicated section and explicitly acknowledges single-run nondeterminism, scale disadvantage vs FunSearch, negative results, and lack of mathematical structure。
- Computational cost is described in wall-clock budgets and total 6–10 day run duration; token/API money absent。

## Asset Metadata

- FULL TEXT READ: YES
- Source: `LLM/25_Reasoning-Models-Heuristics.md`
- Decision Layer: Heuristic generation
- Current-study Relation: 反馈机制参考
- Innovation Boundary: 当前不构成候选 selector 机制的直接新颖性反证；已实现范围为 Heuristic generation，主要用于反馈机制参考。
- Best Writing Claim: 用 reasoning LLM 与 verifier feedback 生成组合设计 heuristic，证明 verifier-assisted generation 路线已存在。
