# 41｜GraphThought 全文编码

- Source: `LLM/41_GraphThought.md`
- Full-text status: **YES**
- Last read position: **EOF (line >1240 empty); Appendices A–L covered**
- Corpus: LLM / Graph CO / thought generation
- Tier: B（Mechanistically supporting）

## A｜Research Content
- Research problem: improve LLM reasoning on graph combinatorial optimization by systematically constructing high-quality intermediate thought trajectories rather than directly mapping problems to answers.
- Problem setting: ten GraphArena graph tasks spanning polynomial and NP-hard problems; generate structured reasoning data then SFT Llama-3-8B-Instruct.
- Objectives: formalize Optimal Thoughts Design (OTD); construct state/action thought spaces; provide forward heuristic-guided and backward solver-guided thought generation; train Llama-GT.
- Algorithm backbone: GraphThought = Selector + Constructor + Meta-Thought Programming; Forward MTP decomposes classical heuristics; Backward MTP reconstructs reasoning from high-quality solver solutions; generated traces are used for LoRA SFT.
- Proposed mechanism: select task-relevant action/state thought pairs from predefined spaces, synthesize executable program P, execute P on instances to create structured reasoning corpus, fine-tune LLM. For NP-hard tasks backward MTP uses solver output as target and reconstructs incremental steps.
- Decision layer: **Reasoning-program / thought-component design and direct solution reasoning**. The Selector selects action-state thought components for dataset/program construction, not runtime search operators in an optimizer.
- State / Context: task identity and graph/problem characteristics at design time; runtime thought states include instance description/simplification/reduction, current solution, solving flag, node/edge sets.
- Action / Decision: 16 canonical thought actions involving node/edge add/remove under optimal-solution guidance, rules, simple priors, complex priors; task-specific subset selected and assembled.
- Feedback / Reward: no online RL reward. Backward construction uses exact/approximate solver solutions as supervision; evaluation uses optimality/solution quality.
- Dynamic mechanism: instance state evolves stepwise during reasoning and state thoughts explicitly track it; no external dynamic scheduling and no adaptive online operator-selection loop.
- LLM role: final fine-tuned direct reasoner; supplementary automated synthesis uses Qwen2.5-Coder-32B-Instruct to generate thought-program code.
- RL role: NOT PRESENT in GraphThought mechanism; DRL/GNN appear as prior approaches.
- Claimed contribution: OTD formalization; dual forward/backward MTP; Llama-GT performance on GraphArena.
- Explicit limitation: performance degradation on TSP/GED/MCS or knowledge-scarce/long-chain tasks; LLM solver inference latency/resource demand; poor scaling to thousands/millions of nodes due sequential text/context length; automated LLM-designed thought programs remain weaker than human-designed ones on NP-hard tasks.
- 与当前 FJSP-AGV 研究关系: supporting boundary. GraphThought already formalizes **state space + action space + context-aware component selection**, and shows that explicit state tracking can reduce hallucination and that mixed/complementary heuristic thoughts can matter. But its selector is primarily an offline task-level reasoning-program constructor, not an online evolutionary-search operator selector. Therefore `state/action formalization` or `context-aware selection` alone cannot establish novelty; current work still needs a distinct decision layer and search/dynamic/Pareto competence mechanism.

## B｜Experimental Design Coding
- Dataset / Benchmark: GraphArena original test datasets; GraphThought training corpus 30,000 instruction-following examples.
- Instance scale: 10 tasks. Each small/large task evaluation has **500 instances**. Node ranges: Neighbor/Distance 4–19 vs 20–50; Connected/Diameter/MCP/MIS/MVC 4–14 vs 15–30; MCS/GED/TSP 4–9 vs 10–20.
- Baselines: original GraphArena LLMs, code-augmented DeepSeek-V2-Coder/GPT-4o-Coder, Qwen2-7B-SFT, few-shot models, STaR variants, reasoning models, Llama-GT w/o Thought, classical heuristics for MIS, Gurobi reference.
- Baseline 数量: varies by experiment/table; complete main table contains many model baselines and should not be collapsed to one count without table-specific coding.
- Independent runs: API-based models use **single-pass inference per test instance** due compute constraints. Conventional repeated independent training runs NOT REPORTED.
- Random seeds: NOT REPORTED.
- Population size: NOT APPLICABLE.
- Generations: training 4 epochs; STaR four iterative cycles. These are not EA generations.
- Evaluation budget: 500 instances/task/size for principal GraphArena comparison; BoN uses N up to 32 candidates/instance.
- Fitness / function evaluations: NOT APPLICABLE.
- Real decoding count: one pass per API model/test instance in standard evaluation; BoN N=16/32 explicitly generates N candidates.
- Solver calls: Gurobi obtains exact optimal solutions for optimality ratios/backward guidance; aggregate exact call count NOT REPORTED.
- LLM calls: aggregate NOT REPORTED; API inference single-pass per test instance except BoN; automated thought synthesis uses LLM but total call count NOT REPORTED.
- Token budget: max sequence length 3,000 tokens; inference maximum token threshold discussed but exact threshold NOT REPORTED.
- Runtime / wall-clock: training ≈138,828 s / 38 h; inference 0.0694 s base, 0.0703 s Llama-GT, 0.1643 s Llama-GT BoN N=16.
- Hardware: single NVIDIA H800 PCIe 80GB GPU for training.
- Metrics: GraphArena optimal solution rate/optimality; generalized optimality ratio; average solution size for MIS; inference time; relative improvement across model scales.
- Statistical tests: NOT REPORTED.
- Confidence interval: NOT REPORTED.
- Ablation: Llama-GT w/o Thought vs full; action-only vs no-thought vs full state+action; STaR with GraphThought vs LLM thoughts; LLM-designed vs human-designed thought datasets.
- Sensitivity analysis: BoN N=1/16/32; model-scale comparison 3B vs 8B.
- Generalization / OOD: 10 heterogeneous graph tasks, polynomial vs NP-hard, small vs large graph ranges, 3B vs 8B model scale. Large-scale beyond GraphArena ranges remains a stated limitation.
- Robustness: cross-task/scale evaluation; repeated stochastic-run statistics NOT REPORTED.
- Dynamic-event design: NOT PRESENT.
- LLM API / inference cost: runtime reported; monetary API/token cost NOT REPORTED.

## C｜Writing Evidence Coding
### Introduction
Actual sequence: **M1/M2 GCO importance and NP-hardness → M3 traditional heuristics → M4 manual/fixed-pattern limitations → M3 DRL/GNN → M4 task-specific architecture/prior limitations → M3 direct LLM reasoning → M4 hallucination/poor optimality/long-horizon limitations → M5 explicit question about incorporating classical search principles → M3 thought prompting → M4 thought-generation limitations for NP-hard tasks → M6 OTD + GraphThought forward/backward → M7 three numbered inline contributions**.
- Limitation appears early after traditional heuristics and repeatedly deepens across method families.
- Central method follows an explicit unresolved-question/challenge sequence.
- Contributions: **3**, numbered inline rather than bullets.
- Empirical diagnosis before method: benchmark evidence from prior work is used to motivate poor LLM validity/optimality, but no new paper-specific diagnostic experiment precedes the method.

### Related Work
- Main detailed RW is Appendix A.
- Organization: taxonomy/method family: LLMs for GCO → prompt engineering/benchmarks → architectures/frameworks → graph representation/encoding → empirical factors → CoT/ToT/GoT → self-correction/planning/search learning.
- traditional→learning→LLM: Introduction carries this evolution more strongly than Appendix A.
- direct solving vs solver-assisted: discussed through direct LLM graph reasoning and solver/search-guided reasoning.
- generation vs selection: not an AHD operator taxonomy.
- static vs adaptive/offline vs online: NOT a principal organizing dimension.

### Gap language
- Repeated `However` transitions progressively expose limitations of traditional heuristics, specialized neural solvers, direct LLM reasoning, and generic thought prompting.
- Explicit unresolved question: whether classical GCO solver search principles can be incorporated into LLM output/reasoning.
- `However, thought generation in GCO presents a unique challenge...` narrows the final gap to NP-hard thought construction.
- `To address this` directly transitions into OTD and GraphThought.
- Standalone Limitations section uses `Despite ... limitations remain`, then three named limitation categories.

### Contributions
- Count: **3**, numbered inline.
- Formulation contribution: OTD with state/action thought spaces.
- Method contribution: forward heuristic-guided + backward solver-guided MTP.
- Experimental/model contribution: Llama-GT/GraphArena results.
- Benchmark contribution: NO new benchmark; reasoning dataset is generated.
- Empirical finding contribution: structured state+action thoughts outperform action-only/no-thought on selected task groups; human-designed thought construction remains stronger than automated LLM design for NP-hard tasks.

### Experimental writing
- Main Experiments starts with model/training/inference framework and benchmark metric/scale definitions, then comparison blocks by baseline family rather than a single giant narrative.
- Main table explicitly notes **500 instances per task for each graph size** and distinguishes code-augmented, few-shot, SFT and thought variants.
- Ablation reporting includes negative evidence: thought integration hurts GED and action-only is worse than no-thought; later Appendix J offers mechanism hypotheses instead of hiding the regression.
- Appendix B provides exact training hyperparameters and explicitly admits API models received single-pass inference due computational constraints.
- Appendix D isolates training and inference cost; Appendix I separates thought-type, heuristic comparison and model-scale analyses; Appendix K compares automated vs human thought-design pipelines.
- No formal significance tests/CI despite `significantly` wording.

## Asset Metadata

- FULL TEXT READ: YES
- Source: `LLM/41_GraphThought.md`
- Decision Layer: Reasoning / feedback
- Current-study Relation: 外围
- Innovation Boundary: 当前不构成候选 selector 机制的直接新颖性反证；已实现范围为 Reasoning / feedback，主要用于外围。
- Best Writing Claim: 把 forward heuristic 与 backward solver-guided reasoning 结合，代表双向推理与 solver feedback 路线。
