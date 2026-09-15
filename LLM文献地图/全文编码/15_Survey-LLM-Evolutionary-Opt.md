# 15 A Systematic Survey on Large Language Models for Evolutionary Optimization: From Modeling to Solving｜全文编码

## Audit
- Source: `LLM/15_Survey-LLM-Evolutionary-Opt.md`
- Full text read to EOF: YES
- Abstract, Introduction, survey methodology/taxonomy, modeling, solving paradigms, challenges, empirical study/guidance, applications, vision, conclusion, references and supplementary sections/tables through detailed high-level evaluation: READ.

## A. Research Content
- Research problem: unify LLM-for-optimization research from modeling through solving and distinguish LLM roles by decision level.
- Problem setting: systematic survey of evolutionary optimization plus controlled empirical comparisons.
- Objectives: taxonomy + benchmark systematization + baseline comparisons + practitioner guidance + future directions toward dynamic/self-evolving/agentic optimization.
- Algorithm backbone: survey; empirical sections instantiate OPRO-style optimization and (1+1)-ES parameter control.
- Proposed mechanism/taxonomy: four categories: LLMs for Optimization Modeling; LLMs as Optimizers; Low-level LLM-assisted Optimization Algorithms; High-level LLM-assisted Optimization Algorithms.
- Decision layer: explicitly distinguishes stand-alone solution generation, low-level initialization/operator/configuration/evaluation decisions, and high-level algorithm selection/generation.
- State/context: survey identifies raw trajectory, structured search-state features, problem/algorithm features, performance history and semantic representations as different context types.
- Action/decision: candidate solution, evolutionary operator action, parameter/configuration action, algorithm choice, or generated algorithm depending on paradigm.
- Feedback/reward: objective feedback, search trajectories, solver/execution feedback, normalized benchmark scores; low-level controlled experiment uses relative-improvement reward/state.
- Dynamic mechanism: reviews static vs dynamic configuration/selection/generation and argues for online self-adaptation.
- LLM role: optimizer, component/controller, selector, algorithm designer, modeler.
- RL role: historical/MetaBBO comparator and dynamic-control paradigm; DDQN/PPO are directly compared against LLM controllers.
- Claimed contribution: 152-paper workflow-oriented survey with controlled baseline comparisons and practitioner guidance; identifies dynamic self-adaptation, modeling-solving integration and agentic coordination as future directions.
- Explicit limitations: survey says corpus is representative, not exhaustive; empirical cross-paper environments are not fully homogeneous; LLM numerical search has dimensionality/stagnation/format issues; low-level decisions face scale/interdependence; high-level generation has LLM/evaluation cost, feasibility and novelty/self-assessment problems.
- Relation to FJSP-AGV: extremely close conceptual boundary evidence. It explicitly covers RL-based FJSP control, LAOS search-feature-based adaptive operator selection, dynamic algorithm selection, EoH-S complementary portfolios, multiobjective LLM operators, and calls for dynamic selection/generation. Therefore `search-state-aware LLM AOS`, `dynamic selection`, `portfolio`, and `offline generation + adaptive control` require narrower novelty evidence.

## B. Experimental Design
### Survey corpus
- Literature search: IEEE Xplore, ACM DL, SpringerLink, ScienceDirect, Google Scholar, arXiv; Jan 2023–Sep 2025; 152 retained representative papers after dedup/manual title-abstract-full-text screening.

### Modeling synthesis
- Benchmarks: eight selected modeling benchmarks in main comparison; supplementary table covers NL4Opt, NLP4LP, NL2OPT, ComplexOR, MAMO, IndustryOR, OptiBench, DP-Bench, DCP-Bench, OptMath.
- Main baseline categories: general/reasoning LLMs; prompt-based; learning-based.
- Metric: pass@1/accuracy; main analysis includes methods evaluated on all eight selected benchmarks.
- Cross-paper caveat: solver configs, few-shot examples, temperatures and trial counts differ.

### Controlled LLM-as-optimizer experiment
- Problem suite: four BBOB functions across multiple dimensions.
- Baselines: random search, DE, PSO, CMA-ES.
- LLMs: GPT-5-mini, DeepSeek-V4, Qwen3.5.
- Seeds/runs: five seeds per setting; supplementary reports 60 runs/model across configurations.
- Evaluation budget: 200 sequential API calls/run; function-evaluation curves reported.
- Metric: relative improvement r; median convergence on 10D Sphere.
- Runtime: mean wall-clock 694 s DeepSeek-V4 to 1785 s GPT-5-mini per run; classical optimizer within seconds locally.
- Tokens: across 60 runs/model context described; aggregate three-model consumption 45.90M input + 9.48M output tokens.
- Failure metrics: parse/format failures and stagnation criterion final r<0.2.

### Controlled low-level parameter-control experiment
- Algorithm: (1+1)-ES, dimension 20.
- Functions: Rastrigin, Ackley, Griewank, Schwefel.
- Baselines/controllers: fixed sigma, DDQN, PPO, OpenAI-ES; GPT-5-mini, DeepSeek-V4, Qwen3.5.
- State: remaining budget, stagnation count, relative fitness improvement, recent offspring acceptance, current step size, best solution, best fitness.
- Action: same discrete action space for trained and LLM controllers; additional continuous-vs-discrete representation comparison.
- Evaluation budget: 1000 function evaluations; controller update every 20 generations.
- Seeds: five.
- Metric: relative improvement r, mean over five seeds.
- Result pattern: all three LLM controllers exceed fixed and trained MetaBBO averages in this particular control experiment; discrete structured output explores more effectively than continuous raw output.

### High-level generation synthesis
- Benchmarks: CO-Bench, HeuriGym, FrontierCO.
- Metric: normalized objective/quality scores and validity/feasibility; benchmarks use different standardized protocols.
- Main caveat: intended for regime-level trends, not a unified ranking.
- Statistical tests / confidence intervals: NOT REPORTED as central controlled-analysis tools in the read text.
- Dynamic-event scheduling design: NOT PRESENT in the survey's own controlled experiments.
- Hardware: NOT REPORTED for the controlled experiments in the main/relevant supplementary text read.
- Monetary API cost: NOT REPORTED; API-call counts, token consumption and wall-clock overhead are reported for LLM-as-optimizer.

## C. Writing Evidence
### Introduction
- M1 optimization workflow/algorithm limitations/expert dependence → M3 ML/RL automation → M4 poor unseen generalization/retraining cost → M3 LLM opportunity → M4 current LLM optimization limitations → M5 need for unified role-aware analysis → M6 workflow-oriented survey/empirical framework → M7 contributions.
- Contributions are presented after explicit gap diagnosis, then section roadmap.

### Related Surveys
- Dedicated section precedes technical taxonomy.
- Uses comparison table to establish scope gap, then states two structural gaps and explains exactly how this survey differs.
- This is strong evidence for a `prior surveys → dimensions omitted → proposed organizing frame` review-writing pattern.

### Taxonomy/technical organization
- Workflow-oriented: Modeling → Solving.
- Solving taxonomy is explicitly decision-layer based: stand-alone optimizer → low-level component → high-level selector/designer.
- Within low-level: initialization → evolutionary operators → algorithm configuration → evaluation.
- Within high-level: algorithm selection → algorithm generation; generation history single-step → iterative.

### Gap language
- Repeated structure: observed literature boundary → causal/structural explanation → deployment implication → future research question.
- Uses `However`, `As a result`, `Thus`, `Consequently`, `remain`, `underexplored`, but key claims are backed by survey corpus or controlled experiments.

### Contributions
- Main contribution block combines taxonomy, empirical grounding, practitioner guidance and future research directions rather than only a method claim.

### Experimental writing
- Explicitly states whether evidence is curated cross-paper data or controlled experiment.
- Each empirical subsection follows: comparison protocol → results → practical implication → research opportunity.
- Fairness caveats are unusually explicit: only comparable benchmark coverage included; heterogeneous protocols acknowledged; high-level benchmark comparison framed as regime-level rather than unified ranking.
- Computational cost is reported with API calls, wall-clock and tokens, not merely objective quality.
- Failure analysis operationalizes failure, e.g. stagnation threshold r<0.2.

### Novelty strength
- Survey uses strong structural-gap claims (`rarely form an end-to-end loop`, `dynamic selection and generation remain underexplored`) but these are survey conclusions, not sufficient alone for our paper's novelty claim; original direct competitors still require full verification.

## Innovation-boundary evidence to carry forward
1. LAOS already replaces full trajectories with search-state features for LLM adaptive operator selection.
2. Low-level LLM control is explicitly compared against DDQN/PPO using the same state/action setup in the survey's controlled experiment.
3. EoH-S already targets complementary algorithm portfolios.
4. Dynamic selection/generation and continual self-adaptation are explicitly identified as the next research direction.
5. A narrower potential boundary remains around a rigorously defined context-conditioned operator competence model that links predicted operator effects, observed effects, Pareto/search/environment context and controlled slow-timescale redesign, but this remains a hypothesis until direct competitors are all fully read.
