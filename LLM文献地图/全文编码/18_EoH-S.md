# 18｜EoH-S 全文编码

- Source: `LLM/18_EoH-S.md`
- Full-text status: **YES**
- Last read position: **EOF (line >980 empty); appendix/supplementary task setups, prompts, convergence and detailed benchmark tables covered**
- Corpus: LLM / HH / AHD
- Tier: A（mechanistically close）

## A｜Research Content

- Research problem: 现有 LLM-AHD 以“单个平均性能最优 heuristic”为目标，在跨分布/跨规模实例上泛化不足。
- Problem setting: Automated Heuristic Set Design (AHSD)，为多样实例设计小规模 complementary heuristic set。
- Objectives: 最小化 heuristic set 的 Complementary Performance Index (CPI)，使每个实例至少能由集合中某个 heuristic 获得较好性能。
- Algorithm backbone: evolutionary AHD / EoH-style thought+code representation + memetic search + complementary population management。
- Proposed mechanism: instance-wise performance vector；Complementary-aware Search (CS) 以 Manhattan-distance 最大的两个 heuristic 为 parents；Local Search (LS) 精炼单 heuristic；CPM 贪心按 delta-CPI 选取互补集合；AHSD objective 被证明 monotone + supermodular，并给出 greedy performance guarantee。
- Decision layer: **Operator/heuristic generation + portfolio/set design**。不是在线 per-state heuristic selector。
- State / Context: heuristic thought/code、每个 heuristic 在 m 个 training instances 上的 instance-wise performance vector、当前 population、parent complementarity。
- Action / Decision: LLM 生成新 heuristic thought + executable code；CPM 选择进入下一 population 的 heuristic set。
- Feedback / Reward: 每个 heuristic 的 instance-wise task performance；CPI / delta-CPI；average gap。
- Dynamic mechanism: evolutionary design-process adaptation；**没有动态环境事件驱动的 online selection**。
- LLM role: heuristic generator/designer，执行 initialization、complementary-aware generation、local refinement prompts。
- RL role: **NOT PRESENT**。
- Claimed contribution: AHSD formulation；CPI monotonicity/supermodularity；EoH-S 的 complementary population management + complementary-aware memetic search；跨任务/分布/规模实验。
- Explicit limitation: supplementary convergence discussion明确指出，当 instance diversity 很低、单一 heuristic 已足够时，EoH-S 的 complementary-set design 可能较不有效；Future Work 提出 heuristic collaboration strategies 与更多应用。
- 与当前 FJSP-AGV 研究关系: 直接封死“LLM 设计 complementary operator/heuristic portfolio”作为单独创新点。它已经使用**instance-conditioned competence evidence**（instance-wise performance vector）来设计互补集合，但没有建立 runtime context → operator competence → online selection → feedback learning 的机制。因此当前研究若保留 portfolio，必须把创新放在**运行时上下文条件化能力模型/选择与反馈闭环**，不能停在“互补算子库”。

## B｜Experimental Design Coding

- Dataset / Benchmark: OBP, TSP, CVRP；外部 benchmark BPPLib, TSPLib, CVRPLib。
- Instance scale:
  - OBP training 128 Weibull instances, n=200–2000, capacity=100；testing 6 sets，capacity 200/500，n=1k/5k/10k，每 set 5 instances。
  - TSP training 128 clustered instances, n=10–200；testing正文概述 n=50–500，supplementary明确 80 instances，n=50/100/200/500/1000，每 size 16。
  - CVRP training 256, n=20–200, capacity 10–150；testing supplementary 128, n=50/100/200/500，每 size 32。
  - TSPLib 49 symmetric Euclidean instances, n=52–1000；CVRPLib A/B/E/F/M/P/X；BPPLib >700 selected instances。
- Baselines: Random, EoH, FunSearch, ReEvo, 1+1 EPS, MEoH, MCTS-AHD, CALM；hand-designed First Fit/Best Fit；controlled top-10 portfolio comparisons for EoH/FunSearch/ReEvo。
- Baseline 数量: LLM-AHD named baseline methods = **8**；另含 task-specific hand heuristics/top-k variants。
- Independent runs: **3** for controlled methods / EoH-S across all three tasks；results averaged over 3 runs。
- Random seeds: **NOT REPORTED**。
- Population size: n=10 for EoH-S, EoH, ReEvo；FunSearch dynamic population；ablation n∈{5,10,15,20}。
- Generations: **NOT REPORTED as generation count**。
- Evaluation budget: Nmax = **2,000 heuristic evaluations/samples** for all tasks/methods in controlled comparison。
- Fitness / function evaluations: 2,000 heuristic evaluations；instance-wise evaluation across training set。
- Real decoding count: **NOT REPORTED**。
- Solver calls: LKH used as baseline solution for TSP/CVRP; call count **NOT REPORTED**。
- LLM calls: **NOT REPORTED**。
- Token budget: **NOT REPORTED**。
- Runtime / wall-clock: automated heuristic design process **under 2 hours** for all methods/tasks。
- Hardware: one Intel i7-9700 CPU。
- LLM: DeepSeek-V3 API default parameters；LLM4AD platform。
- Metrics: relative gap to OBP lower bound；relative gap to LKH for TSP/CVRP；CPI；benchmark average gap；convergence curves。
- Statistical tests: **NOT REPORTED**。
- Confidence interval: **NOT REPORTED**。
- Ablation: w/o LS；w/o CS；w/o CPM；population sizes 5/15/20 vs default 10；OBP，2,000 samples/run。
- Sensitivity analysis: population-size analysis 5–20，可编码为 parameter sensitivity。
- Generalization / OOD: 强。训练→不同 distribution、capacity、problem size；TSP clustered training → uniform testing；external BPPLib/TSPLib/CVRPLib benchmarks。
- Robustness: population-size robustness + benchmark/generalization evidence；formal stochastic robustness test **NOT REPORTED**。
- Dynamic-event design: **NOT PRESENT**。
- LLM API / inference cost: **NOT REPORTED**。
- Fairness: controlled comparison 对 EoH/FunSearch/ReEvo 使用 identical training instances；统一 Nmax=2000；EoH-S/EoH/ReEvo population=10；明确声称 portfolio design 不增加 evaluation budget。

## C｜Writing Evidence Coding

### Introduction rhetorical moves

实际顺序：
1. M1/M3：LLM-driven AHD 已取得成功并扩展至 optimization/math/ML。
2. M3：介绍 iterative search paradigm，EoH/FunSearch/ReEvo 等。
3. M4：现有方法聚焦 single heuristic + best average performance。
4. M4/M5：给出两条 generalization failure 原因。
5. M3/M6 bridge：引入 algorithm portfolio 作为解决 generalization 的已知思路，同时指出 one-heuristic-per-instance 不现实。
6. M7：直接进入 **3 个编号 contributions**。

- Limitation 首次出现: Introduction 第 3 个实质段落。
- Method/AHSD idea: 第 4 个实质段落以 algorithm portfolio 过渡，随后 contribution bullet 正式提出 AHSD/EoH-S。
- Contributions: Introduction 尾部；**3 项；编号 bullet**。
- Empirical diagnosis before method: **NO**，主要是理论/文献动机，不是先做本文 empirical diagnosis。

### Related Work organization

- Related Works 存在，但被排在 references 后的 supplementary 部分。
- 三个 method-family subsections：`Automated Heuristic Design` → `Neural Combinatorial Optimization` → `LLM-driven AHD`。
- traditional → learning → LLM: **YES**，结构上非常清楚。
- generation vs selection: AHD subsection有 taxonomy 背景，但不是全文主轴。
- single heuristic vs portfolio: **YES，核心 gap axis**。
- static vs adaptive: NO。
- offline vs online: NO。

### Gap language / rhetorical functions

- Contrast: `Despite these advancements` 将进展转为 single-heuristic limitation。
- Limitation: `mainly focus on identifying a single heuristic...`; `may suffer from generalization limitations`。
- Causal elaboration: 用 numbered reasons `1)... 2)...` 解释为什么 single-best heuristic 泛化差。
- Motivation bridge: `A common approach ... is to use an algorithm portfolio`; `It is natural for us to leverage this approach...`。
- Constraint on naive solution: `impractical, if not impossible, to find one heuristic for each instance`。
- Transition: `With these concerns, this paper makes the following contributions`。
- Novelty strength: 使用 `new formulation`，但核心论证主要通过问题重构而非泛化式“first/no studies”口号。

### Contributions

- Contribution count: **3**。
- Numbered/bulleted: **YES**。
- Verbs: introduce / propose / conduct。
- Formulation contribution: AHSD + theoretical properties。
- Method contribution: EoH-S + CPM + memetic search。
- Experimental contribution: 3 AHD tasks、多分布/规模/benchmarks，报告 up to 60% improvement。
- Benchmark contribution: NO。
- Empirical finding contribution: 泛化与 complementarity findings 作为实验贡献的一部分。

### Experimental writing

- Setup sequence: `Experimental Studies → Tasks and Instances → Compared Methods and Settings → Results on Training & Testing → Results on Benchmark Instances → Complementary Performance → Ablation Studies`。
- Baseline selection: 先列广泛 SOTA，再明确拆成 **Direct comparison** 与 **Controlled comparison**，很好地区分复用原论文 heuristic 和同预算重训。
- Fairness: identical instances + same Nmax + aligned population size；还单独解释 heuristic set 不增加 evaluation count。
- Comparative results: 先 training/testing distribution shift，再 external benchmark，再直接测 complementarity。
- Ablation writing: 明确列 w/o LS / CS / CPM，再做 population-size sensitivity，并解释哪个组件贡献最大。
- Generalization writing: 不只说“泛化好”，而是通过 distribution/size/capacity shift 和标准 benchmark 分层证明。
- Statistical significance: NOT PRESENT。
- Computational cost: hardware + <2h + equal heuristic-evaluation budget；token/API monetary cost未报。
