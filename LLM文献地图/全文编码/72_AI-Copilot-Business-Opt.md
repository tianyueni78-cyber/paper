# 72｜Language Models for Business Optimisation with Production Scheduling 全文编码

- Source: `LLM/72_AI-Copilot-Business-Opt.md`
- Full-text status: **YES**
- Last read position: **EOF (line >760 empty); Appendices A–B and loss-convergence figures covered**
- Corpus: LLM / Scheduling / optimization modeling
- Tier: B/B

## A｜Research Content
- Research problem: automate formulation of conventional and real-world business optimization problems, especially JSS/FJSS production scheduling, using a cost-efficient fine-tuned code LLM.
- Problem setting: natural-language problem description → modular formulation code → CP solver execution → solution correctness evaluation.
- Objectives: improve formulation accuracy and scalability beyond prompt-only/commercial LLM approaches while using affordable compute.
- Algorithm backbone: CodeRL/CodeT5 fine-tuning + prompt engineering + formulation-code modularization + OR-Tools/CPMpy execution.
- Proposed mechanism: create problem-description/formulation pairs; split long formulation into self-contained modules/instructions to fit model token limit; fine-tune CodeRL on instruction-expanded data; combine generated modules; execute generated formulation with solver and classify success/failure/exception.
- Decision layer: **Optimizer/model formulation generation**. Scheduling is the modeled application, not an online scheduling policy selected by the LLM.
- State / Context: problem description + module-specific instruction; for real case includes machine groups, quantities, waiting-time preferences, due dates and objectives.
- Action / Decision: generate a code module/formulation component.
- Feedback / Reward: cross-entropy during fine-tuning; solver execution status used for evaluation. CodeRL's original pretrained model used RL, but this paper's adaptation is supervised fine-tuning rather than an online RL controller.
- Dynamic mechanism: NOT PRESENT as dynamic scheduling control.
- LLM role: domain-adapted formulation/code generator.
- RL role: indirect only through CodeRL pretraining; NOT PRESENT as the proposed scheduling/formulation controller.
- Claimed contribution: cost-efficient fine-tuning framework; modularization/prompt technique for scalability; two open datasets for JSS and real-world production scheduling; real-world and LPWP benchmarking.
- Explicit limitation: transport times ignored; real ERP due-date data unavailable and due dates randomized; machine quantities/requirements partly simulated; model has 600-token generation limit requiring modularization; formulation knowledge depends on training-data variety. Further limitations/cost constraints motivate small-model design.
- 与当前 FJSP-AGV 研究关系: scheduling-domain boundary evidence. It demonstrates LLM-based **FJSS formulation generation** on a real production case, but the LLM does not select scheduling operators or control search. Thus “LLM + FJSP” alone is not a contribution; current work remains at a different decision layer: runtime metaheuristic/operator control.

## B｜Experimental Design Coding
- Dataset / Benchmark: conventional JSS dataset created by authors; real-world Australian embroidery production-scheduling dataset; LPWP for external comparison.
- Instance scale: conventional: 100 problem descriptions/formulations; modular instructions expand dataset (exact expanded count should be taken from paper section if used in final statistics). Real-world: 50 base instances × 16 instructions = **800** module-level instances. LPWP: **288** descriptions.
- Data split: **70% train / 10% validation / 20% test** for each dataset.
- Baselines: LPWP comparison with Chain-of-Experts (CoE), Chain-of-Thought (CoT), Progressive-Hint Prompting (PHP), standard GPT.
- Baseline 数量: **4** in LPWP external comparison.
- Independent runs: NOT REPORTED.
- Random seeds: NOT REPORTED.
- Population size: NOT APPLICABLE.
- Generations: NOT APPLICABLE.
- Evaluation budget: multiple batch-size × epoch configurations; no inference-call budget.
- Fitness/function evaluations: NOT APPLICABLE.
- Real decoding count: NOT REPORTED aggregate.
- Solver calls: generated formulations are executed with OR-Tools; aggregate solver-call count NOT REPORTED.
- LLM calls: NOT REPORTED.
- Token budget: CodeRL output maximum **600 tokens**; conventional formulations 1200–1800 tokens; real-world formulations 1800–3400 tokens, motivating modularization.
- Runtime / wall-clock: detailed fine-tuning time reported by batch/epoch. Conventional examples range 429.63s (batch4, epoch1) to 8561.05s (batch1, epoch8); real-world 353.19s to 7010.38s across reported settings.
- Hardware: NOT REPORTED in the read text as a concrete device specification.
- Metrics: cross-entropy loss; solver execution success/failure/exception rates; training time; train/validation loss convergence; LPWP accuracy/comparative performance.
- Statistical tests: NOT REPORTED.
- Confidence interval: NOT REPORTED.
- Ablation: no standard component-removal ablation; batch size/epoch grid and modularized dataset experiments.
- Sensitivity analysis: **batch sizes 1/2/4 × epochs 1/2/4/8**; convergence and training-time trade-off analyzed.
- Generalization / OOD: conventional JSS → real-world FJSS case → LPWP cross-domain formulation benchmark, but no formal OOD protocol.
- Robustness: different stakeholder styles generated for descriptions; PCA embeddings used to inspect representation variety; no stochastic repeated-run robustness.
- Dynamic-event design: NOT PRESENT. Real-world scheduling has due dates/waiting-time business rules but no online machine/AGV failure/new-job event experiment.
- LLM API / inference cost: NOT REPORTED monetary API cost; design motivation emphasizes cost-efficient open model.

## C｜Writing Evidence Coding
### Introduction
Actual sequence: **M1 business optimization importance → M2 formulation/solver process → M3 LLM/code-generation opportunity → M4 complex formulation/data/scalability limitations → M3 recent LLM formulation methods → M4 prompt/commercial-model/token-limit limitations → M6 fine-tuned modular framework → M7 four bullet contributions**.
- Limitation appears before method and is tied to concrete practical bottlenecks: domain data, complex constraints, scalability, token/resource limits.
- Method follows a short direct-competitor paragraph.
- Contributions: **4 bullets**, explicitly listed.
- Empirical diagnosis before method: NO.

### Related Work
- Standalone Literature Review.
- Explicit funnel organization: Business Optimization → Formulation/Solvers → LLM/Code Generation → LLM for Optimization → Challenges of Automating Formulation.
- Table 1 compares prior systems by optimization model, LLM methodology and evaluation metric.
- This is taxonomy/method-family organization rather than simple chronology.

### Gap language
- Rhetorical function is mostly **practical limitation → engineering requirement**: commercial models, prompt dependence, missing optimization knowledge, token limits and scalability motivate fine-tuning/modularization.
- Avoids relying solely on “few studies”; even when claiming limited complex-decision applications, the method case is backed by explicit resource/scalability constraints.

### Contributions
- Count: **4**, bulleted.
- framework/method contribution.
- modularization/prompt engineering contribution.
- dataset contribution.
- empirical/benchmark contribution.

### Experimental writing
- Experiments are structured by increasingly realistic cases: conventional JSS → real-world production FJSS → external LP dataset.
- Hyperparameter analysis jointly reports loss, time and executable correctness rather than optimizing loss alone.
- Train/validation curves are explicitly used to discuss convergence and overfitting.
- Solver execution status is treated as stronger functional evidence than token-level loss.
- Real-world assumptions are disclosed: transportation omitted, quantities simulated, due dates randomly generated because ERP data unavailable.
- Weaknesses for final corpus statistics: no repeated stochastic runs, seeds, inferential tests, CI, inference-token/cost accounting.
