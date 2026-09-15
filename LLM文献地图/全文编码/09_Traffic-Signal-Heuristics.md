# 09 TPET｜全文编码

## Audit
- Source: `LLM/09_Traffic-Signal-Heuristics.md`
- Full text read to EOF: YES
- Title/Abstract, Introduction, Related Work, Formulation/Method, Experiments, Results, Ablation, Case Study, Conclusion: READ. Dedicated Discussion/Limitations and Appendix: NOT PRESENT.

## A. Research Content
- Research problem: traffic signal control tradeoff among fast but simplistic heuristics, specialized but opaque/poorly generalizing DRL, and high-latency generic online LLM actors.
- Problem setting: dynamic high-frequency sequential traffic signal control in CityFlow, intersections modeled as MDPs.
- Objectives: minimize travel time, queue length and waiting time while producing lightweight, interpretable, environment-specialized policies.
- Algorithm backbone: NeRM-style prompt/algorithm co-evolution adapted to sequential decision making.
- Proposed mechanism: Structured State Abstraction (SSA) translates numeric state/history into temporal-logical predicates; Credit Assignment Feedback (CAF) back-traces simulation logs and converts sparse macro fitness into actionable defect critiques; LLM evolves policy code offline.
- State/context: queue length, waiting time, persistent history/starvation timers and structured congestion/fairness/balance predicates.
- Action/decision: signal-phase selection by evolved lightweight heuristic policy; during evolution LLM modifies policy code.
- Feedback/reward: final simulation fitness plus CAF defect critique linking micro-decisions to macro outcomes.
- Dynamic mechanism: online policy consumes real-time dynamic state/history through SSA; LLM itself is offline evolution engine rather than high-frequency actor.
- Claimed contribution: evolutionary discovery paradigm for TSC; SSA + CAF; empirical comparison against transport, RL and online-LLM approaches.
- Explicit limitation: dedicated limitation section NOT PRESENT.

## B. Experimental Design
- Dataset/benchmark: three real-world traffic-flow datasets, Jinan-1, Jinan-2, Hangzhou, simulated in CityFlow.
- Instance scale: Jinan datasets 12 intersections; Hangzhou 16 intersections.
- Baselines: Random, FixedTime, Maxpressure; MPLight, AttendLight, PressLight, CoLight; LLMLight with GPT-4, ChatGPT-3.5, Qwen, Llama2, Llama3; NeRM.
- Independent runs: 3 runs per experiment.
- Seeds: NOT REPORTED.
- Evaluation budget: 20 evolutionary iterations; 20 candidates generated each iteration; top 3 retained.
- Metrics: Average Travel Time (ATT), Average Queue Length (AQL), Average Wait Time (AWT); mean and standard deviation.
- Statistical tests: NOT REPORTED.
- Ablations: TPET full vs w/o SSA vs w/o CAF.
- Sensitivity analysis: NOT PRESENT as a dedicated parameter study.
- Generalization: cross-dataset performance reported; unseen-distribution protocol NOT REPORTED.
- Runtime: online-LLM latency motivates method, but a detailed wall-clock comparative runtime table is NOT REPORTED in the read experimental section.
- Hardware: NVIDIA RTX 3070Ti, Intel i7-11700K, 32 GB RAM.
- LLM calls/tokens/API cost: NOT REPORTED.

## C. Writing Evidence
- Introduction moves: domain importance → three-way method tradeoff → limitations of heuristics/DRL/online LLM → explicit argument about LLM role → TPET → scientific hypothesis/modules → three contribution bullets.
- Related Work organization: two method-family subsections: TSC paradigms and LLM heuristic evolution. TSC subsection explicitly progresses classic transport → RL → online LLM.
- Limitation location: limitations appear in Introduction and adaptation-challenges subsection; no dedicated paper-limitations section.
- Gap formulation: mechanism/system-role gap: LLM should not be high-frequency generic actor but offline discoverer; sequential setting additionally needs semantic state abstraction and temporal credit assignment.
- Proposed-method transition: `To address these limitations, We argue...` followed immediately by role reframing and TPET.
- Contribution structure: 3 bullets covering paradigm, two mechanisms, and empirical demonstration.
- Experimental Setup structure: datasets → metrics → implementation/hardware/repeated runs → compared models, then performance, ablation and qualitative case study.
- Comparative-result reporting: interprets table by baseline family and metric, then singles out NeRM as mechanistic comparator; variance/error bars support stability claims.
- Ablation-result reporting: removes one module at a time and attributes degradation to missing abstraction/critique functions.
- Academic hedging: comparatively strong rhetoric in performance/role claims; mechanism interpretation uses `indicating`, `demonstrating`, `confirming` tied to observed ablations.
- Novelty-claim strength: uses `novel, practical alternative` and strong role-framing, but no unqualified `first` claim observed in Introduction.
