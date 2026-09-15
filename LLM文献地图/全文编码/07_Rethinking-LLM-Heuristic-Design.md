# 07 DASH｜全文编码

## Audit
- Source: `LLM/07_Rethinking-LLM-Heuristic-Design.md`
- Full text read to EOF: YES
- Title/Abstract, Introduction, Related Work, Method, Framework, Experimental Protocol, main results, ablation/sensitivity/generalization, Conclusion and remaining appendix/reference material: READ where present.

## A. Research Content
- Research problem: LLM-driven heuristic design evaluated only at endpoints misses convergence dynamics and incurs costly re-adaptation under distribution shifts.
- Problem setting: automated heuristic/solver evolution for TSP, CVRP, VRPTW and MKP under runtime constraints and heterogeneous instance distributions.
- Objectives: jointly improve solution quality and runtime efficiency and reduce adaptation cost under distribution shift.
- Algorithm backbone: LHD evolutionary generate-evaluate-select workflow with task-specific heuristic solver backbones.
- Proposed mechanism: tLDR trajectory metric; DASH co-evolves search mechanism and runtime schedule through MDL/MCL/SSL; PLR archives group-specialized solvers for profile-aware retrieval/warm starts.
- State/context: full convergence trajectory, terminal residual, runtime, mechanism/schedule state, instance profiles/groups, global population and group archives.
- Action/decision: LLM edits mechanism code or runtime schedule; acceptance protocol chooses candidates; PLR retrieves specialized solver by nearest profile group.
- Feedback/reward: terminal log residual, trajectory efficiency/tLDR and realized runtime under layer-specific acceptance rules.
- Dynamic mechanism: search-process dynamics explicitly modeled through trajectories; schedule is adapted during offline evolution; online PLR performs profile-conditioned retrieval rather than repeated LLM re-adaptation.
- Claimed contribution: trajectory-aware evaluation, mechanism/schedule co-evolution, profile-specialist archive/retrieval and broad efficiency/generalization validation.
- Explicit limitation: no dedicated limitations section observed; paper frames remaining issues through robustness/generalization/cost analyses and conclusion. `Limitations = NOT PRESENT` as a standalone section.

## B. Experimental Design
- Dataset/benchmark: synthetic TSP, CVRP, VRPTW; TSPLIB transfer; OR-Library MKP.
- Instance scale: TSP 20/100/200/500 plus TSPLIB 14–1000; CVRP 100/500; VRPTW 15/20; MKP 500 items with 10/30 constraints.
- Baselines: conventional solvers Concorde/LKH3/OR-Tools; handcrafted LS/GLS/KGLS; NCO AM/POMO/Sym-NCO/DeepACO/SIL; LHD FunSearch/ReEvo/EoH/MEoH/Hercules.
- Independent runs: base-model sensitivity explicitly reports 5 runs; reference solutions for synthetic TSP/CVRP/VRPTW use mean over five solver runs. A universal repeated-run protocol for every main table is NOT REPORTED as one headline setting.
- Seeds: NOT REPORTED as explicit seed IDs.
- Evaluation budget: 100 solver evaluations during offline evolution for DASH and LHD baselines; task-specific equal wall-clock/solver budgets; TSP examples use 10 s and TSPLIB-large comparison 60 s.
- Metrics: objective value, Gap %, wall-clock Time, tLDR/trajectory signals, token consumption/adaptation cost.
- Statistical tests: named inferential statistical test NOT REPORTED in read text.
- Ablations: full DASH vs w/o MDL, w/o MCL, w/o SSL; trajectory metric alternatives; comparison-margin sensitivity.
- Sensitivity: epsilon, number of profile groups G, base LLM (five models), solver backbones, time-constrained vs unconstrained evaluation.
- Generalization: held-out test sets, TSPLIB external transfer, size/distribution shift, solver-backbone transfer.
- Runtime: central metric; explicit wall-clock reporting.
- Hardware: reported in appendix/reproducibility material where present; no value inferred here if not explicit in captured coding.
- LLM calls/tokens/API cost: tokens explicitly reported for adaptation/generalization comparisons; 100 solver-evaluation budget used as principal evolution control; cost reduction under PLR analyzed.

## C. Writing Evidence
- Introduction moves: broad CO/handcrafted heuristic problem → LHD progress → two explicitly numbered challenges → motivating experiments → dynamics-aware method → PLR → three-item contribution list.
- Related Work organization: method-family sections: real-world CO; heuristics/solver adaptation; LLM-driven heuristic design.
- Limitation location: limitations of prior work appear early and are formalized as `Challenge 1` and `Challenge 2`; no standalone paper-limitations section observed.
- Gap formulation: capability/mechanism-level, centered on endpoint-only evaluation and repeated re-adaptation under heterogeneous distributions.
- Proposed-method transition: `These observations underscore... Accordingly, we propose...` links empirical motivation directly to method.
- Contribution structure: three bullets: metric, framework+PLR, empirical validation.
- Experimental Setup structure: datasets/settings → train/test construction → metrics/references → shared backbones → baseline taxonomy/fairness → RQs → results.
- Comparative-result reporting: reports gap and runtime jointly, separates constrained/unconstrained settings, and interprets efficiency-quality tradeoffs rather than a single objective.
- Ablation-result reporting: states replacement/removal while keeping remaining method unchanged, then explains the observed quality/runtime tradeoff.
- Academic hedging: interpretation uses `indicating`, `suggesting`, `shows`, while broad causal/generalization statements are generally tied to controlled variants or transfer experiments.
- Novelty-claim strength: strong proposal framing but novelty is expressed through the identified evaluation/adaptation mechanism rather than `first-ever` rhetoric in the Introduction.
