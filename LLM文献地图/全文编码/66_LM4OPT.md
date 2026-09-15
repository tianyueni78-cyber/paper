# 66｜LM4OPT 全文编码

- Source: `LLM/66_LM4OPT.md`
- Full-text status: **YES**
- Last read position: **EOF (line >360 empty); no appendix present**
- Corpus: LLM / optimization formulation / fine-tuning
- Tier: B/C

## A｜Research Content
- Research problem: translate natural-language optimization descriptions into mathematical formulations and assess whether large pretrained models or progressively fine-tuned smaller models can perform the task.
- Problem setting: NL4Opt descriptions S → intermediate representation R (variables, constraints, objective) → rule-based canonical form C.
- Objectives: benchmark GPT-3.5/GPT-4/Llama-2-7B zero/one-shot; develop LM4OPT progressive fine-tuning for Llama-2-7B.
- Algorithm backbone: prompt optimization for GPT/Llama inference; for LM4OPT, **GSM8K domain adaptation → NL4Opt task-specific fine-tuning using LoRA/PEFT + NEFTune → intermediate representation → rule-based canonical conversion → F1 evaluation**.
- Proposed mechanism: progressive fine-tuning gives smaller LLM broad math adaptation before optimization-specific training; noisy embeddings regularize task fine-tuning.
- Decision layer: **Optimizer/model formulation generation**, not algorithm/operator selection.
- State / Context: natural-language problem description and zero/one-shot prompt; no optimizer state.
- Action / Decision: generate variables, constraints and objective in structured intermediate form.
- Feedback / Reward: supervised fine-tuning targets and F1 scoring; no online feedback loop.
- Dynamic mechanism: NOT PRESENT.
- LLM role: formulation generator; GPT models benchmarked by prompting; Llama-2-7B adapted via progressive fine-tuning.
- RL role: NOT PRESENT.
- Claimed contribution: benchmark popular LLMs on NL→optimization formulation; zero/one-shot comparison; LM4OPT progressive fine-tuning framework; empirical analysis of model/context limitations.
- Explicit limitation: NL4Opt samples are straightforward/domain-jargon-heavy and may not reflect lay-user input; resource limits prevent larger-model progressive FT; rule-based intermediate→canonical conversion penalizes formatting mismatches that humans could interpret.
- 与当前 FJSP-AGV 研究关系: indirect. It reinforces that **representation/interface errors can contaminate measured algorithmic capability**, so an LLM strategy selector should use a constrained schema and separately record parsing validity vs optimization effect. It provides no operator competence/AOS/dynamic/Pareto mechanism.

## B｜Experimental Design Coding
- Dataset / Benchmark: NL4Opt; GSM8K used as first-stage progressive fine-tuning data.
- Instance scale: uses NL4Opt author-provided train/validation/evaluation split; exact counts NOT REPORTED in this paper text.
- Baselines: prior fine-tuned BART NL4Opt baseline; GPT-3.5; GPT-4; pretrained/non-progressively/progressively fine-tuned Llama-2-7B variants.
- Baseline 数量: main Table 2 has **baseline + 3 LLM families**, with zero/one-shot variants; Table 3 contains multiple Llama fine-tuning/NEFTune configurations.
- Independent runs: NOT REPORTED.
- Random seeds: NOT REPORTED.
- Population size: NOT APPLICABLE.
- Generations: training **7 epochs**.
- Evaluation budget: NL4Opt evaluation split; no search-evaluation budget.
- Fitness / function evaluations: NOT APPLICABLE.
- Real decoding count: NOT REPORTED as aggregate.
- Solver calls: NOT PRESENT in LM4OPT evaluation; output is canonical formulation scored by F1.
- LLM calls: NOT REPORTED.
- Token budget: maximum response sequence length **200** for fine-tuning.
- Runtime / wall-clock: NOT REPORTED.
- Hardware: **NVIDIA A40 48GB**.
- Training hyperparameters: batch 4; gradient accumulation 1; AdamW; lr 3e-4; weight decay .001; noisy embedding strength 5; gradient checkpointing.
- Metrics: F1-score; estimated CO2 emissions.
- Statistical tests: NOT REPORTED.
- Confidence interval: NOT REPORTED.
- Ablation: pretrained vs non-progressive FT vs progressive FT; with/without NEFTune; zero vs one-shot.
- Sensitivity analysis: instruction length/context via zero-vs-one-shot; not a systematic continuous prompt-length sweep.
- Generalization / OOD: NOT PRESENT as formal OOD evaluation.
- Robustness: NOT REPORTED.
- Dynamic-event design: NOT PRESENT.
- LLM API / inference cost: API access date reported for GPT models; monetary cost NOT REPORTED. Carbon footprint per Llama fine-tuning session ~**23.52 g CO2**.

## C｜Writing Evidence Coding
### Introduction
Actual sequence: **M1 optimization modeling practical importance → M4 expert barrier → M3 NLP/LLM progress → M5 specific benchmarking/small-model adaptation gap → M7 four bullet contributions**; detailed method comes later.
- Limitation/gap appears after broad LLM motivation.
- Contributions: **4 bullets**.
- Method name LM4OPT appears in contribution 4, then is elaborated in Methodology.
- Empirical diagnosis before method: NO.

### Related Work
- Standalone Related Work.
- Organized as an evolution of optimization-language systems: NL4Opt two-stage NER/formulation → all-in-one model → OptiMUS solver agent → OPRO iterative optimizer → OptiGuide real-world system.
- Includes a structured comparison table with dataset, input, human-in-loop, multiple LLMs, fine-tuning, prompting and objective.
- Ends with an explicit gap paragraph and positioning of LM4OPT.

### Gap language
- Uses strong `uncharted territory`, `gap persists`, `bridge the research gap` language. These are author-era claims and cannot be imported as current claims.
- More useful rhetorical structure: **compare system dimensions in a table → identify missing evaluation/adaptation combination → state the niche addressed**.

### Contributions
- Count: **4**, bulleted.
- Model benchmarking contribution.
- prompting-setting comparison.
- empirical NL4Opt result.
- fine-tuning/method contribution.

### Experimental writing
- Experimental Setup gives hardware and training hyperparameters in one compact paragraph, including optimizer, LR, weight decay, epochs, batch, sequence length and memory technique.
- Fairness language explicitly says the same baseline scoring mechanism is reused, but also transparently notes BART receives named-entity information unavailable to GPT/Llama, so the comparison is not input-identical.
- Results combine aggregate F1 with qualitative failure examples of hallucination/looping.
- Ablation-like table isolates progressive FT and NEFTune effects.
- Limitations explicitly discuss dataset external validity, compute constraints and measurement artifacts from rule-based canonicalization.
- Missing repeated runs/seeds, statistical significance/CI, runtime and API cost.

## Asset Metadata

- FULL TEXT READ: YES
- Source: `LLM/66_LM4OPT.md`
- Decision Layer: Modeling
- Current-study Relation: 外围
- Innovation Boundary: 当前不构成候选 selector 机制的直接新颖性反证；已实现范围为 Modeling，主要用于外围。
- Best Writing Claim: 以 NL4Opt 为基础做 progressive fine-tuning，代表语言到优化建模 benchmark 路线。
