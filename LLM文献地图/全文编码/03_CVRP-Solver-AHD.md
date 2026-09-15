# 03｜Enhancing CVRP Solver through LLM-driven Automatic Heuristic Design

- Source: `LLM/03_CVRP-Solver-AHD.md`
- Corpus: LLM / AHD
- Full-text audit: **YES**
- EOF verification: fetch after line 800 returned empty; substantive appendices A–G and references were covered.
- Coding rule: only information supported by the repository full text is recorded; absent information is `NOT REPORTED`.

## A. Research Content

| Field | Coding |
|---|---|
| Research problem | Improve CVRP metaheuristic solver performance by automating design of the ruin heuristic inside Adaptive Iterated Local Search (AILS). |
| Problem setting | Capacitated Vehicle Routing Problem; moderate-scale CVRPLib X Set and large-scale AGS Set. |
| Objectives | Single-objective route cost / objective gap to BKS. |
| Algorithm backbone | Adaptive Iterated Local Search (AILS): initialization, iterated local search with ruin-and-recreate perturbation and local search, adaptive updating. |
| Proposed mechanism | AILS-AHD: LLM + evolutionary computation evolves a population of ruin heuristics; candidate heuristic replaces the ruin component and is evaluated in AILS. Adds LLM-driven pre-evaluation/voting plus early stopping acceleration. |
| State/context | Heuristic design inputs include distance matrix, KNN list, number of nodes to remove, node attributes, average nodes per route, random seed/current solution-related node structure. No online LLM selector over search states. |
| Action/decision | LLM generates/modifies executable ruin heuristic code; deployed heuristic selects nodes to remove. |
| Feedback/reward | Fitness is average solver performance/gap over evaluation instances; population update uses fitness. Acceleration judges whether a generated heuristic is worth full evaluation. |
| Dynamic mechanism | No dynamic scheduling/environment mechanism; algorithmic adaptation is heuristic evolution during design. |
| Claimed contribution | LLM-driven automatic ruin-heuristic design in AILS; LLM-based acceleration; empirical comparison with HGS/AILS-II/manual ruin variants and new BKS results. |
| Explicit limitation | Relies on a simple AHD framework; future work targets more efficient AHD and generalization to more VRP variants. |

## B. Experimental Design

| Field | Coding |
|---|---|
| Dataset / benchmark | CVRPLib X Set (100 moderate-scale instances, n≈100–1000); AGS Set (10 large-scale instances, n≈3000–30000). AHD design evaluation uses 10 selected moderate-scale instances. |
| Instance scale | Moderate 100–1000 nodes; large 3000–30000 nodes. |
| Baselines | HGS; AILS-II; hand-crafted AILS-C (K-nearest ruin) and AILS-S (sequence-based ruin). Also compares top-3 designed heuristics PFD, DDD, EN. |
| Number of principal external/manual baselines | 4 (HGS, AILS-II, AILS-C, AILS-S). |
| Independent runs | Main moderate-scale evaluation: 30 independent runs/instance. Large-scale evaluation: 10 independent runs. Neighborhood-expansion ablation: 10 independent experiments across 10 selected instances. AHD candidate evaluation: 10 instances × 2 random seeds = 20 instance-runs per heuristic evaluation. |
| Seeds | AHD evaluation explicitly uses two different random seeds per selected instance; fixed random seed is also described as a feature/reproducibility mechanism. Exact numeric seed values: NOT REPORTED. |
| Evaluation budget | AHD population=25, max generation=10, reported as 1000 LLM calls; candidate evaluation 3×n seconds per instance; main benchmark 3×n seconds; BKS search on large instances 10×n seconds. |
| Metrics | Best objective/BKS; average objective; objective gap (%); mean ± dispersion shown in tables; convergence curves; acceleration U-R/C-R and TT/TF/FT/FF categories. |
| Statistical tests | Statistical significance is reported via (+/−/=), but the specific statistical test and significance threshold are NOT REPORTED in the repository text located during full-text audit. |
| Ablations | Neighborhood expanding factor λ ∈ {2,10,100,500,1000,1500}; acceleration Vote-1/Vote-3/Vote-5 and early-stopping analysis. |
| Sensitivity analysis | λ sensitivity/ablation. |
| Generalization | Tests moderate and large scales; future generalization to additional VRP variants is explicitly left as future work. No unseen-problem-family generalization protocol reported. |
| Runtime | 3×n seconds for standard evaluation; 10×n seconds for large-scale BKS search. |
| Hardware | 2 × Intel Xeon Gold 6254 CPUs. |
| LLM | GPT-4o. |
| LLM calls / tokens / API cost | 1000 LLM calls reported for AHD configuration. Token count and monetary API cost: NOT REPORTED. |

## C. Writing Evidence

### Introduction rhetorical moves

Observed sequence:

`M1 Domain/problem importance → M2 solver families → M3 limitations of existing solver development → M4 LLM opportunity + limitation of current automation → M6 proposed AILS-AHD → M7 numbered/bulleted contributions`

Notes:
- The Introduction does not contain a separately labelled Related Work section; detailed Related Work is moved to Appendix A.
- Limitation/motivation appears before the proposed method: manual metaheuristic development requires expert knowledge and trial-and-error; current LLM routing-solver automation remains below practical requirements.
- Contributions are presented as three bullet points.

### Related Work organization

Appendix A uses **method taxonomy**:
1. Meta-heuristic for CVRP: single-solution-based vs population-based methods.
2. LLM for AHD: automatic heuristic design + evolutionary computation + LLM integration.

This is taxonomy/mechanism organization rather than pure chronology.

### Gap / limitation formulation

Functions observed:
- capability limitation of exact/neural methods;
- human-design cost of metaheuristics;
- under-realized potential of LLM enhancement;
- transition from existing LLM-AHD to solver-level improvement.

Strength: relatively assertive application/method-performance motivation, but explicit future-work limitation is narrow and concrete rather than claiming the entire area is unexplored.

### Proposed-method transition

The paper moves directly from identified limitations to “In this paper, we present AILS-AHD…”, followed by empirical headline results and then contributions.

### Contribution structure

- 3 bullet contributions.
- Types: method/framework contribution; acceleration/computational-efficiency contribution; experimental/SOTA-performance contribution.
- Main verbs/structures: present; further develop; conduct a comprehensive evaluation.

### Experimental Setup organization

Experiment section sequence:
1. AILS-AHD settings and LLM configuration;
2. designed heuristics/convergence;
3. baselines;
4. benchmarks + hardware/runtime/repeats;
5. moderate-scale results;
6. large-scale results;
7. LLM acceleration;
8. ablation.

Appendix adds prompt details, design-evaluation dataset, early stopping, full heuristic code, detailed result tables, convergence/BKS routes, licenses and broader impacts.

### Comparative-result reporting

Rhetorical pattern:
- identify table/figure;
- define metric/significance notation;
- state aggregate performance;
- contrast convergence behavior;
- state new-BKS count.

The paper reports best and average values, dispersion notation, significance symbols and convergence curves rather than only a single best result.

### Ablation-result reporting

Pattern:
- name one design factor;
- enumerate tested levels;
- state independent-run protocol;
- compare central performance and stability/box size;
- infer which factor value is preferred and warn about degradation at large values.

### Academic hedging / novelty strength

- Uses assertive method/result language such as “we present”, “demonstrates”, “superior performance”, “new best-known solutions”.
- Explicit limitation language is cautious and bounded: current framework is simple; efficiency and problem-family generalization remain future work.
- No corpus-level inference is made from this single paper.

## D. Relevance Tier

**Tier A: Mechanistically Close.**

Reason: directly relevant to LLM-driven automatic heuristic/operator design and evaluation-budget issues, but it is not dynamic scheduling and does not perform online context-conditioned operator selection during an evolutionary scheduling run.

## E. Audit Notes

- Related Work: READ (Appendix A).
- Formulation/problem description: READ.
- Method/framework: READ.
- Experimental setup/baselines/benchmark: READ.
- Main results: READ.
- Ablation/sensitivity: READ.
- Limitations/conclusion: READ.
- Relevant appendices B–G: READ through EOF.
- Discussion as a standalone section: NOT PRESENT.
- Separate generalization/robustness section: NOT PRESENT; scale transfer and future generalization are recorded where actually discussed.

## Asset Metadata

- FULL TEXT READ: YES
- Source: `LLM/03_CVRP-Solver-AHD.md`
- Decision Layer: Heuristic generation
- Current-study Relation: 支撑角色分工与 AHD 演进
- Innovation Boundary: 当前不构成候选 selector 机制的直接新颖性反证；已实现范围为 Heuristic generation，主要用于支撑角色分工与 AHD 演进。
- Best Writing Claim: 把 LLM+EC 用于生成 ruin heuristic 并交给传统 AILS 执行，是“LLM 设计、经典优化器执行”的直接实例。
