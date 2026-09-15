# 75｜Can Language Models Solve Graph Problems in Natural Language? / NLGraph 全文编码

- Source: `LLM/75_Graph-Problems-in-NL.md`
- Full-text status: **YES**
- Last read position: **EOF (line >620 empty); Appendices A–D and detailed case tables covered**
- Corpus: LLM / structured reasoning benchmark
- Tier: C/B

## A｜Research Content
- Research problem: test whether LLMs can explicitly map textual graph descriptions to structured conceptual representations and solve graph-algorithm problems.
- Problem setting: natural-language graph instances spanning eight tasks and controlled difficulty; evaluate direct and prompted LLM reasoning.
- Objectives: benchmark graph reasoning, characterize complexity/prompting/ICL robustness limits, and test two instruction-based improvements.
- Algorithm backbone: benchmark + prompting experiments; no classical optimization search backbone.
- Proposed mechanism: NLGraph synthetic generator; Build-a-Graph prompting to ground graph structure before answering; Algorithmic Prompting to recite/revisit relevant algorithm before examples/problem solving.
- Decision layer: **Direct solution/reasoning generation**, not algorithm/operator selection.
- State / Context: textual graph, query, optional exemplars, CoT/self-consistency/algorithm instruction.
- Action / Decision: output graph answer/path/order/matching/flow/updated embeddings depending task.
- Feedback / Reward: evaluation by exact/partial-credit metrics and external correctness checks; no online feedback loop.
- Dynamic mechanism: NOT PRESENT.
- LLM role: direct graph reasoner.
- RL role: NOT PRESENT.
- Claimed contribution: NLGraph benchmark with 29,370 extended problems/eight tasks; complexity-controlled analysis; empirical findings on prompting/ICL/spurious correlations; BAG and Algorithmic prompting.
- Explicit limitation: benchmark tasks not exhaustive; only four black-box LLMs; monetary cost restricts main evaluation to standard 5,902-problem set; proposed prompts have marginal effects on complex tasks; future code execution/state-maintenance suggested.
- 与当前 FJSP-AGV 研究关系: indirect but useful boundary evidence. It shows **more context/examples/prompt sophistication can degrade performance as structural complexity grows**, and that LLM behavior can rely on spurious state correlations. For current selector design, richer context should not automatically be assumed beneficial; context ablation and adversarial/state-shift robustness become evidence requirements, not novelty claims.

## B｜Experimental Design Coding
- Dataset / Benchmark: NLGraph.
- Instance scale: **29,370 extended problems** total; main experiments use **5,902 standard problems** due monetary cost. Eight tasks: connectivity, cycle, topological sort, shortest path, maximum flow, bipartite matching, Hamilton path, GNN simulation. Easy/medium/hard subsets controlled by graph size/sparsity/task parameters.
- Baselines / methods: RANDOM, ZERO-SHOT, FEW-SHOT, COT, 0-COT, COT+SC, LTM where applicable; proposed BAG and ALGORITHMIC; model comparisons across text-davinci-003, code-davinci-002, GPT-3.5-TURBO, GPT-4.
- Baseline 数量: varies by task; core prompting comparison contains up to **6** baseline prompting configurations before proposed methods.
- Independent runs: NOT REPORTED as repeated stochastic experiment over same benchmark; evaluation is over many generated instances. Self-consistency samples multiple reasoning paths but is not reported as independent experimental runs.
- Random seeds: NOT REPORTED.
- Population size: NOT APPLICABLE.
- Generations: NOT APPLICABLE.
- Evaluation budget: standard set 5,902 problems; extended 29,370 available but not fully evaluated.
- Fitness/function evaluations: NOT APPLICABLE.
- Real decoding count: NOT REPORTED aggregate.
- Solver calls: external programs verify tasks such as topological-sort correctness; aggregate calls NOT REPORTED.
- LLM calls: NOT REPORTED aggregate.
- Token budget: NOT REPORTED.
- Runtime / wall-clock: NOT REPORTED.
- Hardware: NOT REPORTED.
- Metrics: exact-match accuracy plus task-specific partial credit; GNN PC/RE; performance differences across difficulty and perturbations.
- Statistical tests: NOT REPORTED.
- Confidence interval: NOT REPORTED.
- Ablation: prompting-method comparison; number of exemplars; instruction variants; dot controls; graph-definition variants; exemplar difficulty; path length/graph complexity.
- Sensitivity analysis: difficulty easy/medium/hard; graph size/density; exemplar count 0/2/4/8/12/16; instruction wording; representation instantiation.
- Generalization / OOD: synthetic generation reduces exact pretraining overlap; evaluation across eight tasks and complexity levels. No conventional train/OOD split because prompting benchmark rather than learned policy.
- Robustness: strong dedicated tests: chain/clique connectivity counterexamples reverse spurious degree/mention correlations; real-world-object naming variants; model variants.
- Dynamic-event design: NOT PRESENT.
- LLM API / inference cost: monetary cost acknowledged as reason only standard 5,902 examples are evaluated; exact dollar/API cost NOT REPORTED.

## C｜Writing Evidence Coding
### Introduction
Actual sequence: **M1 LLM use in implicitly structured tasks → M5 explicit graph-reasoning question → M6 NLGraph benchmark → M7 four numbered empirical findings → M6 two proposed prompting methods + result preview**.
- Limitation/gap appears immediately as an explicit capability question rather than a long prior-work catalogue.
- Method/benchmark appears early after the research question.
- Contributions/findings are presented as **4 numbered findings**, then improvement methods.
- Empirical diagnosis before proposed prompting method: **YES**. The paper first establishes prompting/ICL/spurious-correlation failures, then proposes BAG/Algorithmic prompting.

### Related Work
- Standalone Section 6 after methods/results.
- Organized by method/application family: implicit graphical structures; explicit graph reasoning; LLM reasoning/prompting.
- Main paper therefore prioritizes benchmark evidence before literature taxonomy.

### Gap language
- Uses unresolved-question framing: implicit graph success does not establish explicit graph reasoning capability.
- Strong empirical gap style: `we observe/find` followed by quantified failure under complexity/spurious-correlation conditions, then method motivation.
- Complexity acts as the main boundary variable rather than generic “few studies” rhetoric.

### Contributions
- Introduction contains **4 numbered empirical findings**.
- benchmark contribution: NLGraph.
- empirical findings: preliminary capability; prompting degradation with complexity; ICL counterproductivity; brittleness/spurious correlation.
- method contribution: BAG and Algorithmic prompting.

### Experimental writing
- Benchmark construction precedes evaluation setup, allowing every later result to be interpreted by controlled difficulty.
- Results section is question/finding-driven rather than table-driven: preliminary ability → prompting limits → ICL failure → brittleness → proposed improvement.
- Robustness failure is demonstrated by deliberately constructed counterexamples, not only average accuracy.
- Proposed methods are tested against semantically irrelevant instruction controls/dot controls in Appendix D, which separates extra-computation effects from instruction content.
- Limitations explicitly disclose cost-driven sampling of 5,902/29,370 instances.
- No inferential statistics, CI, runtime or hardware accounting despite extensive benchmark coverage.

## Asset Metadata

- FULL TEXT READ: YES
- Source: `LLM/75_Graph-Problems-in-NL.md`
- Decision Layer: Direct reasoning evaluation
- Current-study Relation: 支持 OOD/规模测试
- Innovation Boundary: 已占据或直接限制的边界：图 reasoning benchmark 显示复杂度增加时 prompting/ICL 收益衰减，是 scale/generalization 边界证据。
- Best Writing Claim: 图 reasoning benchmark 显示复杂度增加时 prompting/ICL 收益衰减，是 scale/generalization 边界证据。
