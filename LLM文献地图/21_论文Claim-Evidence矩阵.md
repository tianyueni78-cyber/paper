# 21｜论文 Claim-Evidence 矩阵

> 原则：论文写作不再按 Paper→Summary 组织，而按 Claim→Evidence 组织。

| Claim ID | Claim | Evidence Papers | Existing Capability | Remaining Question | Evidence Type | Confidence | Paper Section |
|---|---|---|---|---|---|---|---|
|C1|自动算法设计与策略选择应区分 generation、selection、configuration、AOS/HH 等不同决策层|78,15,52|领域已有明确方法分类|当前研究到底处在 selection 还是 generation 层？|【原文事实】|高|Related Work / Method Positioning|
|C2|LLM 已能通过 EC/反思生成并持续改进可执行 heuristic|69,68|LLM-AHD 已成熟到可重复 heuristic generation|仅“LLM 生成 heuristic”还能否构成创新？基本不能|【原文事实】|高|Related Work|
|C3|AHD 已从 endpoint fitness 推进到 trajectory、uncertainty、diversity、runtime 等 search-process-aware control|05,07,43,44,45|搜索过程状态已成为算法设计信息|这些过程状态能否用于运行时策略选择，而非只用于离线 AHD？|【跨文献统计】|高|Related Work / Gap|
|C4|LLM 自动优化已从单 heuristic 推进到 heuristic set、multi-operator 与 Pareto-aware design|18,06,21,54|portfolio / operator-system / multiobjective design 已存在|运行时如何根据动态状态选择既有策略仍需单独讨论|【跨文献统计】|高|Related Work|
|C5|LLM 根据 current problem state 从 heuristic pool 在线选择 heuristic 已存在|23|state-aware selection HH 已被直接实现|当前研究必须在哪些 state / feedback / objective / evaluator 上产生实质差异？|【原文事实】|高|Direct Competitors / Gap|
|C6|LLM 已进入 dynamic FJSP 并承担 strategic / instantaneous scheduling decision|19|dynamic FJSP + LLM strategic decision 已存在|dynamic multi-objective FJSP-AGV 中 search-process-aware supervisory selection 是否仍有未解决能力？|【原文事实】|高|Direct Competitors / Gap|
|C7|LLM 使用 state-action-reward history 在线决策并非空白|58|history-aware online LLM decision 已存在|历史信息是否能被用于更长时间尺度的 strategy-effect credit，而非简单经验池？|【原文事实】|高|Direct Competitors / Gap|
|C8|高频 online LLM actor 存在 latency / cost 风险，慢 LLM + 快 policy 是真实竞争路线|09|离线/低频 LLM 生成快速在线 policy 已存在|在线 LLM selector 的质量增益是否足以抵消延迟和成本？|【原文事实】|高|Gap / Experimental Design|
|C9|solver / executor feedback 与 objective verification 是 LLM optimization 可靠性的重要机制|12,24,28,39,42,59,64,76|闭环验证比仅靠自然语言理由更可靠|本研究应怎样用真实优化效果约束 selector，而非相信解释文本？|【跨文献统计】|高|Methodology|
|C10|direct LLM solving 在规模、结构复杂度与可行性上存在明显边界|61,75|规模扩大后 LLM 直接求解并不天然可靠|将 LLM 放在高层 supervisory layer 是否能避开低层数值/组合推理弱点？|【跨文献统计】|高|Method Positioning|
|C11|evaluation cost、runtime、token/调用成本已经成为 automated optimization 的设计问题，而不是附属指标|07,26,53,09|研究已开始显式控制评价与推理成本|LLM selector 必须在同真实解码预算下比较，否则性能差异不可归因|【跨文献统计】|高|Experimental Design|
|C12|多目标 heuristic design 已使用 Pareto / non-dominated 思路|21,54|Pareto-aware design 已存在|动态搜索过程中如何给 selector 做 Pareto-aware credit 仍需核验|【原文事实】|中高|Gap / Method|
|C13|当前 69 篇中尚未观察到“动态 FJSP-AGV + 环境状态 + search-process state + Pareto state + strategy-effect history + remaining budget”的统一高层 selector|19,23,58,05,07,21,54|各组成机制分别存在|这些机制的统一是否已有更直接工作，尤其 2025–2026 文献？|【分析判断】|中|Research Gap|
|C14|因此“LLM selector”不能作为 novelty，候选贡献只能落在信息结构、反馈机制、公平比较与可验证能力上|23,19,58,09|宽泛 novelty 已被直接竞品占领|联合 context、credit、Pareto、budget 哪一项能在实验中产生稳定独立增益？|【分析判断】|高|Gap / Contributions|
|C15|最公平的主实验是固定 optimizer、decoder、strategy library、dynamic-event process 和 real evaluation budget，只替换 selector|23,09,26,53 + 当前系统约束|可隔离 selector 的因果贡献|是否还需 matched latency / call-frequency 版本作为第二层公平性控制？|【分析判断】|高|Experimental Design|
|C16|当前候选主问题应从“LLM 是否更智能”收窄为 state representation、credit assignment、generalization、budget efficiency 中可测能力|05,07,09,23,58|相邻路线已分别暴露这些能力维度|哪一能力在 FJSP-AGV 上最稳定、最可复述？|【分析判断】|高|Introduction / RQs|

## 当前最关键的四条论文级 Claim

### Claim A｜已有能力

LLM 已经能够生成 heuristic、管理 heuristic-design search、构建 portfolio，并根据 current state 在线选择 heuristic。

Supporting Papers：`69,68,05,07,18,06,23`

### Claim B｜直接边界

LLM contextual selection、dynamic FJSP strategic decision、history-aware online decision 都已经分别出现，因此不能把这些宽泛标签写成创新。

Supporting Papers：`23,19,58`

### Claim C｜真正剩余问题

现有证据尚未证明：在动态多目标 FJSP-AGV 中，一个读取**环境状态 + 搜索过程状态 + Pareto 状态 + 历史策略效果 + 剩余预算**的 LLM supervisory selector，能否在完全相同低层执行条件下优于 Q-learning selector。

Evidence Type：`【分析判断】`，仍需 Scheduling Corpus 与新直接竞品检索继续攻击。

### Claim D｜实验必须回答

即使 LLM selector 提升解集质量，也必须同时证明增益不是额外评价预算、更多策略、调用频率或更高运行成本造成的。

Supporting Papers：`09,26,53` + 当前研究公平比较要求。

## 使用规则

1. 写段落前先选 Claim ID。
2. 只有能支持该 Claim 的文献才进入段落。
3. `【分析判断】`不能伪装成“已有文献证明”。
4. `【待验证】`必须在正文定稿前清零或转为明确限制。
5. 新文献进入 Corpus 时，优先判断它会不会改变 C5–C16，而不是先写摘要。
