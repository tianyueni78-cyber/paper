# 16｜AutoPBO 全文编码

- Source: `LLM/16_AutoPBO.md`
- Full-text status: **YES**
- Last read position: **EOF (line >540 empty)**
- Corpus: LLM / HH / AHD
- Tier: B（solver-level automated design supporting evidence）

## A｜Research Content

- Research problem: 自动增强 Pseudo-Boolean Optimization (PBO) 的 local-search solver，减少复杂 solver heuristic 的人工设计与调参。
- Problem setting: general-form PBO solver，包含复杂、相互依赖的多个内部 heuristic functions。
- Objectives: 生成性能更强的 local-search PBO solver，同时降低 LLM 直接处理复杂耦合 solver code 时的语法/逻辑错误。
- Algorithm backbone: structuralized local-search PBO solver `StructPBO` + multi-agent LLM code optimization + greedy sequential propagation.
- Proposed mechanism: 将 solver 结构化为七个可独立修改的函数；Planner 生成修改计划，Editor 修改/运行代码，Evaluator 评价并反馈；每轮生成多个版本，以 feasibility/win/objective performance 选择最佳版本并立即传播到后续函数优化。
- Decision layer: **Optimizer design / operator-component generation**，不是在线 scheduling decision 或 runtime operator selection。
- State / Context: 完整 solver code、当前待修改函数、Planner 建议、编译/运行信息、实验结果、Evaluator feedback，以及前序已接受的函数修改。
- Action / Decision: 生成修改计划、修改特定 solver function、从多个函数版本中选择性能最优版本并传播。
- Feedback / Reward: 编译/运行结果；Feasible/Infeasible；objective value；相对 StructPBO 的 feasible count / win count；Evaluator textual feedback。
- Dynamic mechanism: solver-design search 中的 sequential adaptation / modification propagation；**不是动态调度环境中的在线 adaptation**。
- LLM role: Code Optimization Planner + Code Editor + Modification Evaluator，负责 solver heuristic/component redesign。
- RL role: **NOT PRESENT**。
- Claimed contribution: AutoPBO multi-agent feedback-driven framework；StructPBO structuralized solver；通过逐函数 greedy optimization 处理组件依赖并提升 PBO local-search solver。
- Explicit limitation: 正文未设置独立 Limitations section；Future Work 提出 RAG 以提高修改正确性，并扩展到 MIP/general solvers。作者还在方法动机中明确指出复杂代码的 long-context、tight coupling、syntax/logical inconsistency 是现有 LLM solver design 的困难。
- 与当前 FJSP-AGV 研究关系: 证明 LLM 自动设计已经可从“单一小 heuristic”扩展到**多组件、相互依赖的完整 solver**，因此“LLM 生成多个算子/组件”本身不能作为当前研究的新颖性。可迁移点是组件依赖与 sequential propagation；它没有解决 dynamic FJSP-AGV 中 context-conditioned online selection、Pareto-aware competence learning 或 environment/search-state supervisory control。

## B｜Experimental Design Coding

- Dataset / Benchmark: PB16, MIPLIB, CRAFT, Real-world；共 47 datasets。
- Instance scale: PB16 1600 instances；MIPLIB 267；CRAFT 1025；Real-world = MWCB 24 + SAP 21 + WSNO 18。每个 dataset 随机 1:1 划分 training/test。
- Baselines: StructPBO（框架提升对照）+ 6 SOTA competitors：NuPBO, OraSLS, PBO-IHS, RoundingSat, Gurobi, SCIP。
- Baseline 数量: 主要 SOTA competitor = **6**；另有 StructPBO internal baseline。
- Independent runs: 主表说明每个 solver 在测试 instance 上 one run；Appendix A 进行了 multiple independent runs，但正文未明确给出重复次数。根据表中均值如 25.3/680.7 可知存在重复，但**次数 NOT REPORTED，禁止反推**。
- Random seeds: **NOT REPORTED**。
- Population size: **NOT APPLICABLE / NOT REPORTED**。
- Generations: **NOT APPLICABLE / NOT REPORTED**。
- Evaluation budget: AutoPBO training/generation 使用 60-second cutoff；final evaluation 每 solver 每 instance 300-second cutoff。
- Fitness / function evaluations: **NOT REPORTED**。
- Real decoding count: **NOT REPORTED**。
- Solver calls: **NOT REPORTED**。
- LLM calls: **NOT REPORTED**。
- Token budget: **NOT REPORTED**。
- Runtime / wall-clock: 60 s training cutoff；300 s test cutoff per instance；整体 AutoPBO design wall-clock **NOT REPORTED**。
- Hardware: Ubuntu 20.04.4 LTS；2 × AMD EPYC 7763 @ 2.45 GHz；1 TB RAM；g++ 9.4.0。
- LLM: DeepSeek-R1 default。
- Metrics: `#win`; `avg_score = (best+1)/(solver_solution+1)`，无解时 0；Appendix A mean, standard deviation, coefficient of variation (CV)。
- Statistical tests: **NOT REPORTED**（无显著性检验）。
- Confidence interval: **NOT REPORTED**。
- Ablation: **NOT PRESENT** 作为正式组件消融；AutoPBO vs StructPBO 是整体框架提升对照，不应自动编码成标准 ablation。
- Sensitivity analysis: **NOT PRESENT**。
- Generalization / OOD: train/test 1:1 split across 47 datasets，覆盖 competition/MIP/crafted/real-world problem families；未报告独立的 unseen problem-family OOD protocol。
- Robustness: Appendix A repeated-experiment stability analysis，报告 mean ± std 和 CV。
- Dynamic-event design: **NOT PRESENT**。
- LLM API / inference cost: **NOT REPORTED**。
- Fairness: PBO-IHS, RoundingSat, OraSLS, NuPBO 按 dataset tuning；Gurobi default single thread；调参脚本/最终参数指向 Code & Data Appendix。

## C｜Writing Evidence Coding

### Introduction rhetorical moves

实际顺序可编码为：
1. **M1 Domain importance**：PBO 的表达能力与应用领域。
2. **M2 Problem definition / difficulty**：PBO NP-hard；complete vs incomplete solving。
3. **M3 Existing methods**：MIP/SAT/cutting-plane/IHS；随后 local-search PBO solver 演进。
4. **M4 Limitation**：local-search solver 依赖内部 heuristics，人工设计需要 expert effort/manual tuning。
5. **M3 Existing LLM-AHD methods**：FunSearch → EoH → ReEvo → AutoSAT → AlphaEvolve。
6. **M4/M5 Gap**：general-form solver code 复杂、组件多且耦合；constraint types 更广；作者进一步使用强 novelty claim “to our knowledge ... no prior work”限定到 LLM-driven PBO solver design。
7. **M6 Proposed method**：自动增强现有 PBO local-search solver；从 code comprehension、invalid modification、multi-function composition 三个问题切入；提出 StructPBO + multi-agent AutoPBO。
8. **M7 Contribution/result positioning**：没有独立编号 contribution bullets；通过连续段落描述 framework、StructPBO 和实验提升。

- Limitation 首次明确出现: Introduction 中 local-search heuristic 人工设计段，约第 5 个实质段落；更具体的 automated-design limitation 在随后两段展开。
- Method 首次出现: Abstract 已出现；Introduction 后部在 gap 后正式引入。
- Contribution 位置: Introduction 末段附近，**非编号列表**。
- Contribution 数量: 作者没有正式编号，因此不强行推定固定数量；可识别 framework + StructPBO + empirical performance 三类功能，但统计时应记录 `NOT FORMALLY NUMBERED`。
- Empirical diagnosis before method: **YES**。作者报告 preliminary experiments：EoH from scratch 仅得到 basic scoring/random perturbation；现有 framework 修改复杂 solver 时出现 syntax/logical inconsistency，然后提出 StructPBO。

### Related Work organization

- 独立 `Related Work` section: **NOT PRESENT**。
- 相关工作嵌入 Introduction。
- Organization: **method family + problem-solving route**。先 complete/incomplete PBO solver，再 local search，再 LLM automated algorithm design。
- traditional → learning → LLM: 部分符合，更准确是 traditional solver/local search → LLM-AHD。
- generation vs selection: **NOT USED AS ORGANIZING AXIS**。
- direct solving vs solver-assisted: 隐含区分，但不是显式 taxonomy。
- single heuristic vs portfolio: **NOT USED**。
- static vs adaptive: **NOT USED AS RELATED-WORK TAXONOMY**。
- offline vs online: **NOT USED**。

### Gap language / rhetorical functions

- Contrast/limitation: `However` 用于从已有方法转向人工 heuristic design 成本、PBO solver application gap、复杂 general-form solver 限制。
- Unresolved problem: “still challenging” 用于 general-form optimization algorithm design。
- Strong novelty: “to our knowledge, there is no prior work ...” 明确限定 PBO solver 的 LLM-driven automated design。
- Motivation/transition: “To address these problems...”；“We try to address the above challenges...” 将诊断直接过渡到方法设计。
- Gap 结构特点: **先给 general AHD progress，再把问题缩窄到 complex general-form solver，再列两个结构性困难，再提出限定性 novelty claim**。

### Contributions

- Numbered contribution list: **NO**。
- Dominant verbs: introduce / design / propose / enhance / configure / employ。
- Method contribution: YES，AutoPBO multi-agent + greedy sequential optimization。
- Formulation contribution: NO。
- Solver/framework contribution: YES，StructPBO。
- Experimental contribution: YES，四 benchmark / 47 datasets 与 SOTA comparison。
- Benchmark contribution: NO，新 benchmark 未提出。
- Empirical finding contribution: 有结果性论证，但未单列为正式 contribution bullet。

### Experimental writing

- Setup organization: `5 Experiments → 5.1 Settings → Environment → Benchmarks and Datasets → State-of-the-art Competitors → Performance Metrics → 5.2 Results`。
- Baseline selection: 按 solver family 分类说明 2 incomplete + 4 complete，并逐个解释其角色。
- Fairness writing: 明确指出若干 competitor 按 dataset parameter tuning，并说明 Gurobi default/single-thread。
- Comparative results: 先 AutoPBO vs StructPBO 证明 framework improvement，再与 6 SOTA solvers 比 competitiveness，形成“internal baseline → external SOTA”的两级证据链。
- Ablation writing: NOT PRESENT。
- Robustness writing: Appendix A 用 repeated experiments + mean/std/CV 单独论证 stability/reproducibility。
- Statistical significance writing: NOT PRESENT。
- Computational cost writing: 报告 cutoff/hardware，但不报告 token/API cost 或完整 design cost。

## Asset Metadata

- FULL TEXT READ: YES
- Source: `LLM/16_AutoPBO.md`
- Decision Layer: System/component design
- Current-study Relation: 限制“设计多个组件”创新
- Innovation Boundary: 已占据或直接限制的边界：让 LLM 设计复杂 PBO solver 的多个组件，证明 automated design 已超出单函数生成。
- Best Writing Claim: 让 LLM 设计复杂 PBO solver 的多个组件，证明 automated design 已超出单函数生成。
