# 19｜ReflecSched 全文编码

- Source: `LLM/19_ReflecSched.md`
- Full-text status: **YES**
- Last read position: **EOF (line >1380 empty); appendices A–H and granular results/hyperparameters covered**
- Corpus: LLM / Scheduling direct competitor
- Tier: **S（Direct Competitor）**

## A｜Research Content

- Research problem: Dynamic Flexible Job-Shop Scheduling (DFJSP) 的实时决策。直接 LLM scheduler 存在 long-context paradox、expert heuristic underutilization、myopic greed。
- Problem setting: event-driven online DFJSP，flexible machine routing；动态事件包括 new job arrival、machine breakdown/repair、job cancellation、high-priority emergency jobs；工业验证含 semiconductor cluster-tool scenario。
- Objectives: minimize makespan；通过 long-horizon strategic reflection 改善直接 LLM 的短视决策，同时保持 zero-shot deployment 和可解释性。
- Algorithm backbone: event-driven simulator + 24 PDR-combination randomized base policy + hierarchical multi-horizon rollouts + LLM reflection + LLM immediate decision module。
- Proposed mechanism: `Simulate → Reflect → Refine` hierarchical planning。高层做 sparse long-range heuristic-driven rollouts，低层对 feasible actions forced rollout；比较 best/worst trajectories；LLM 将差异压缩为 textual `Strategic Experience E`；E 与 immediate state 共同指导下一 scheduling action。Reflection 仅在 dynamic event 时触发。
- Decision layer: **Scheduling decision + runtime strategic control**。最终 action 是 `(job, operation, machine)`；Reflection 层控制的是 strategic guidance，而非从固定 operator pool 中选 operator。
- State / Context: 系统状态 Sτ=(active jobs, arrival times, machine availability, interrupted ops)；prompt 包含 machine states/contention、ready operations、candidate actions、emergency jobs、immediate dynamic state；Reflection 还使用 originating state、previous Strategic Experience、best/worst simulated trajectories及 makespan evidence。
- Action / Decision: 最终选择一个 feasible `(job, op, machine)`；reflection action 是生成/更新 Strategic Experience。
- Feedback / Reward: rollout estimated partial makespan / best-vs-worst trajectory cost；最终 makespan/RPD。无训练型 scalar RL reward。
- Dynamic mechanism: **YES**。event-driven trigger；new jobs, breakdown/repair, cancellation, emergency jobs；事件后重新 reflection 更新 E。Lookahead 内假定无新 stochastic event。
- LLM role: strategic analyst/policy synthesizer + experience-guided scheduling actor。
- RL role: **NO learned RL in ReflecSched**；理论上以 Approximate Policy Iteration / rollout algorithm 解释；RL algorithms作为 baselines。
- Claimed contribution: empirical diagnosis of 3 LLM scheduling failure modes；hierarchical reflection scheduling paradigm；GEN/PDR/MK/JMS multi-tier benchmark ecosystem。
- Explicit limitation: Faithful Reflection 与 cost-to-go approximation 是 working assumptions；longer horizon/larger machine count 可稀释 trajectory differences；randomized PDR base policy 若覆盖窄则 cost approximation 可能失效；lookahead 内不模拟新动态事件；LLM per-instance inference 比训练完成的 DRL 慢，适合 high-variability 而非 massive repetitive static deployment。
- 与当前 FJSP-AGV 研究关系: **极强直接竞争**。它已经占据 `dynamic scheduling + event-triggered LLM + environment state + heuristic-driven simulation + search/trajectory feedback + slow strategic reflection + fast online action`。因此当前研究不能再把“动态事件上下文”“slow-fast LLM supervisory control”“基于 trajectory 的 LLM strategic decision”单独当创新。仍存在的结构差异是：ReflecSched直接做 scheduling action，不是 NSGA-II 内 operator selection；单目标 makespan，不是 Pareto-aware multiobjective FJSP-AGV；没有 operator capability/competence model，也没有 predicted-vs-realized operator effect learning/coverage-gap redesign。这些只能暂记【待验证】，不能先宣称 Gap。

## B｜Experimental Design Coding

- Dataset / Benchmark: GEN-Bench, PDR-Bench, MK-Bench (Brandimarte MK01–MK10 dynamic transformation), JMS-Bench semiconductor cluster tool。
- Instance scale: GEN Normal 20 + Small 18；PDR Normal 111 + Small 12；MK 10；JMS 10 reported granular instances。Generator pool initially 200 instances per scale。
- Baselines:
  - Direct LLM baseline: LLM-Direct。
  - Heuristic/PDR references: 24 PDR combinations；single best/average/oracle instance-best heuristic。
  - Specialized algorithms: GP, DAN, IDDQN, PPO-OC, HMPSAC = **5** external scheduling baselines。
  - Multiple LLM backends: GPT-4o, DeepSeek-V3/V3.2, Qwen3 8B/14B/32B, GPT-5 nano depending experiment。
- Baseline 数量: external specialized scheduling algorithms = 5；另有 LLM-Direct、PDR/oracle controls、多 LLM backends。
- Independent runs: **3 independent runs per problem instance** for primary comparison；diagnostic behavior uses 5 independent generations voting at T=0.8。
- Random seeds: MK dynamic transformation explicitly uses a deterministic random seed, but numeric seed **NOT REPORTED** in text read；general run seeds **NOT REPORTED**。
- Population size: NOT APPLICABLE to ReflecSched；baseline-specific values NOT REPORTED except hyperparameters shown。
- Generations: NOT APPLICABLE；RL training episodes IDDQN/PPO-OC/DAN 2000, HMPSAC 1000 per Table H.1。
- Evaluation budget: ReflecSched search configuration Nroll=24, Lmax=6, Niter=3；sensitivity fixes L×R=24。
- Fitness / function evaluations: simulation rollouts, exact total per instance varies with decision/event structure; aggregate FE **NOT REPORTED**。
- Real decoding count: **NOT REPORTED**。
- Solver calls: simulator rollouts used extensively；exact total **NOT REPORTED**。
- LLM calls: **NOT REPORTED as total call count**。
- Token budget: Max Tokens 8192 per inference configuration；total token consumption per instance reported in Table 4。
- Runtime / wall-clock: cumulative wall-clock/break-even analysis；DS-V3.2 break-even ≈74 instances and GPT-5-nano ≈50 vs HMPSAC；exact all per-instance times not fully tabulated in read text。
- Hardware: Intel Xeon Platinum 8468V CPU + NVIDIA H100 80GB；vLLM serving。
- Metrics: makespan, RPD, Average Rank, Win Rate, Greedy Decision Ratio, token consumption, cumulative wall-clock/break-even。
- Statistical tests: **Wilcoxon signed-rank test**；Figure 7 uses thresholds * p<0.05, ** p<0.01, *** p<0.001；oracle comparison two-sided Wilcoxon。
- Confidence interval: **NOT REPORTED**。
- Ablation: hierarchical vs single-level；Experience Quality = Full/Shuffled/Generic/Noise；Evidence Selection = Full/Top-K Best/Top-K Worst/Quartile。
- Sensitivity analysis: L/R under fixed L×R=24；single-level rollout breadth R=1/3/6/12/24。
- Generalization / OOD: GEN→MK dynamic Brandimarte + JMS semiconductor manufacturing；multiple problem scales and multiple LLM backends；zero-shot no retraining。
- Robustness: cross-benchmark, cross-model, dynamic-event scenarios, repeated runs。
- Dynamic-event design:
  - General generator: job arrivals first half of horizon；machine failure p=0.5 Normal /0.3 Small；job cancellation p=0.3/0.2；1 emergency job；repair U(1,4)。
  - MK transformation: 60% jobs at t=0；later arrivals exponential first half horizon；resource breakdown probability 0.5；repair U(1,4)；cancellation p=0.3；urgent job arrival 25%–75% horizon and targeted bottleneck machines。
  - case study: PM5 fail 8.78→repair 10.74；PM3 fail 14.80→17.41。
- LLM API / inference cost: monetary API cost **NOT REPORTED**；token totals reported。
- Token consumption: Normal average LLM-Direct 146.1k vs ReflecSched 124.0k；Small 22.6k vs 47.9k (models listed in Table 4)。
- Fairness: baseline canonical/optimal settings from original literature；adapted state/action interfaces to shared event model；three runs/instance；Wilcoxon sample size defined by number of problem instances, not replicate count。

## C｜Writing Evidence Coding

### Introduction rhetorical moves

实际顺序：
1. **M1/M2** DFJSP importance + NP-hard + stochastic events + manufacturing impact。
2. **M3/M4** traditional heuristic/metaheuristic → generalization limitation。
3. **M3/M4** DRL → state/action engineering, opacity, simulator/training cost。
4. **M3/Motivation** LLM natural-language scheduler opportunity。
5. **M4/M5 empirical gap diagnosis** direct LLM suboptimal，并明确列 3 pitfalls。
6. **M6** ReflecSched，重构 LLM role，hierarchical reflection + Strategic Experience + event-triggered decision module。
7. **M7** `Our contributions are threefold`，3 个 bullet。

- Limitation first appears: Introduction 第1–2段即开始 traditional/DRL limitation；LLM-specific limitation 在第4个核心论证段明确。
- Method appears: 3 pitfalls 之后立即提出 ReflecSched。
- Contribution: Introduction末，**3项、bulleted**。
- Empirical diagnosis before method: **YES，而且是核心写法**。正文随后单设 Section 4 Motivational Analysis 对三类 failure mode 做实验验证。

### Related Work organization

四个显式 method-family subsections：
1. Heuristic and Metaheuristic Approaches
2. Deep Reinforcement Learning Approaches
3. Large Language Models Paradigms
4. Hierarchical Memory and Reasoning Paradigms

- traditional → learning → LLM: **YES**。
- direct solving vs solver-assisted: LLM subsection区分 end-to-end solver / modeler-to-traditional-solver / hyper-heuristic generator。
- static vs dynamic: **YES，LLM gap 明确以 static focus → complex dynamic scheduling 收束**。
- offline vs online: 非主 taxonomy。
- single heuristic vs portfolio: 非主轴。

### Gap language / rhetorical functions

- Contrast: `However, our work finds...` 将 LLM promise 转为 direct-application failure。
- Empirical gap: `Through a motivational analysis, we identify and empirically validate three key pitfalls`。
- Strong novelty: contribution中使用 `We are the first to systematically identify and validate...`，限定在 complex DFJSP domain 的 failure diagnosis。
- Related-work gap: `Despite their potential... primary focus on static problems...`。
- Mechanism differentiation: `Diverging from these methods...` 区分 persistent memory 与 planning-time hierarchical reflection。
- Transition: `To address these shortcomings, we introduce ReflecSched`。
- 写作特点: **不是只引用别人说 limitation，而是先提出具体可测 failure hypotheses，再用 Section 4 三个诊断实验把 gap 变成 empirical evidence，之后才进入 Method。**

### Contributions

- Count: **3**。
- Numbered/bulleted: YES。
- Types:
  1. empirical diagnosis contribution
  2. method/framework contribution
  3. benchmark/open-source ecosystem contribution
- Verbs: identify/validate, propose, introduce。
- Formulation contribution: DFJSP formalization存在，但不是 contribution bullet。
- Benchmark contribution: YES，GEN/PDR/MK/JMS ecosystem。

### Experimental writing

- Experiment roadmap 在 Section 6 开头明确告诉读者每个 subsection 做什么。
- Setup: datasets → metrics/models → evaluation protocol。
- Fairness: 明确解释 repeated runs 与 Wilcoxon 的 sample unit；baseline canonical settings；动态模型兼容 adaptation。
- Comparative results: 先 LLM-Direct + heuristic/oracle，再 specialized GP/DRL，再 MK cross-benchmark，再 JMS industrial scenario。
- Ablation: core hierarchy → experience quality → evidence selection → budget-constrained sensitivity，因果链很清楚。
- Dynamic scenario writing: 给事件概率/分布/repair window/urgent-job placement，不只是“随机故障”。
- Statistical significance: figure直接用星号阈值，另给 p-value table；明确 two-sided oracle test。
- Computational cost: 独立 Section 6.7，wall-clock + hardware + token + break-even deployment argument；同时诚实说明 LLM marginal per-instance latency 更高。
- Limitation writing: 一部分放 Method theoretical-assumption discussion，一部分放 runtime tradeoff，而不是只在 Conclusion 放一句 future work。

## Asset Metadata

- FULL TEXT READ: YES
- Source: `LLM/19_ReflecSched.md`
- Decision Layer: Dynamic scheduling control
- Current-study Relation: 直接卡住宽泛 novelty
- Innovation Boundary: 已占据或直接限制的边界：dynamic FJSP 中用 hierarchical reflection 与 strategic experience 支持即时调度，是“LLM+动态FJSP”最直接边界文献。
- Best Writing Claim: dynamic FJSP 中用 hierarchical reflection 与 strategic experience 支持即时调度，是“LLM+动态FJSP”最直接边界文献。
