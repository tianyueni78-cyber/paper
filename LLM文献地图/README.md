# LLM 文献地图

> 目的：建立与 `LLM/` 原文库隔离、可持续维护的研究前沿型文献体系。`LLM/` 保存论文转换原文，`LLM文献地图/` 保存证据、比较、争议与可修正研究判断。**不写入 Notion，不与 `paper-explaination` 交叉。**

## 当前主库状态

- 原文证据源：`LLM/`，现有 **69 篇有实际正文的 Markdown**。
- V1 研究层：已逐篇纳入角色审计，并建立四张长期维护核心地图。
- 核心原则：**论文是证据，地图才是长期资产。**

研究知识链：

```text
研究问题
↓
解决机制
↓
方法路线
↓
文献证据
↓
实验结果
↓
研究判断
```

---

# 四张核心地图｜长期主入口

1. [11｜问题演进地图](11_问题演进地图.md)
   - 学界的问题为什么一步步从人工设计走向自动选择、LLM-AHD、trajectory-aware search 与 contextual control。

2. [12｜机制演进地图](12_机制演进地图.md)
   - 统一用 `State/Context → Decision Mechanism → Action/Strategy → Executor → Feedback` 比较方法。

3. [13｜前沿信号地图](13_前沿信号地图.md)
   - 按论文密度、独立团队、方法分化、benchmark 与系统问题识别真正加速方向。

4. [14｜机会窗口地图](14_机会窗口地图.md)
   - 只保留“前置条件已成熟、关键能力未稳定解决、且可以公平实验验证”的机会。

## 69篇审计入口

5. [15｜69篇文献角色索引](15_69篇文献角色索引.md)
   - 每篇正文对应到机制角色、地图影响和与当前研究的距离，防止“读过但没进入研究判断”。

---

# 当前研究锚点

研究对象：动态多目标 FJSP-AGV（柔性作业车间 + AGV 协同）。

候选机制：

```text
动态调度环境状态
+ 搜索过程状态
+ Pareto状态
+ 历史策略效果
+ 剩余真实评价预算
↓
LLM Contextual Selector
↓
固定策略/算子库
↓
固定 NSGA-II + 原 decoder
↓
Makespan / TEC / HV / real decoding count
↓
反馈进入下一轮 Context
```

当前核心研究问题：

> 在固定低层策略库、底层优化器、decoder、动态事件与真实评价预算的条件下，LLM 能否利用动态环境状态、Pareto 搜索状态、历史策略效果与剩余预算进行上下文策略选择，并在对 Q-learning selector 的单模块公平替换中取得更好的性能、泛化或样本效率？

**这是候选研究问题，不是已确认创新。**

## 已被 69 篇正文否定的宽泛创新表述

- “LLM 尚未用于动态 FJSP” → **不成立**：ReflecSched（19）已直接进入 dynamic FJSP。
- “LLM 尚未在线从 heuristic pool 选择 heuristic” → **不成立**：HeurAgenix（23）已明确属于 selection hyper-heuristic。
- “LLM 尚未根据 state/action/reward history 在线决策” → **不成立**：Wireless Power Control（58）已有 experience pool 机制。
- “LLM 自动生成 heuristic 本身具有新颖性” → **高度拥挤**：EoH、ReEvo 及大量后续 AHD 已系统覆盖。

因此当前研究必须落到**更细的能力差异和公平实验**，不能靠换术语制造 gap。

---

# 支撑层｜原有 V0 资产

这些文件继续保留，作为四张核心地图的底层结构、核验和历史判断，不因 V1 上线而删除：

1. [01｜三层研究问题地图](01_三层研究问题地图.md)
2. [02｜概念与理论树](02_概念与理论树.md)
3. [03｜核心文献证据库](03_核心文献证据库.md)
4. [04｜方法演进与争议地图](04_方法演进与争议地图.md)
5. [05｜研究缺口与竞争方法地图](05_研究缺口与竞争方法地图.md)
6. [06｜一页研究定位](06_一页研究定位.md)
7. [07｜维护规则与检索队列](07_维护规则与检索队列.md)
8. [08｜来源核验记录](08_来源核验记录.md)
9. [09｜单篇文献证据表模板](09_文献证据表模板.md)
10. [10｜待下载核心文献清单](10_待下载核心文献清单.md)

---

# 证据标签｜必须长期保持

- **【原文事实】**：论文明确写出的方法、实验、作者结论或作者声明的局限。
- **【文献归纳】**：由多篇论文共同支持的结构化规律。
- **【分析判断】**：基于证据做出的研究判断，可被新论文推翻。
- **【待验证】**：当前证据不足，需要继续检索或实验验证。

禁止把【分析判断】伪装成作者原结论。

---

# 文献距离

- **S｜直接竞争者**：研究问题或机制高度重合，必须正面对比。
- **A｜直接支撑**：直接支撑一个关键机制，但不等于完成本研究。
- **B｜机制可迁移**：对象不同，但机制值得借鉴。
- **C｜背景/基础设施**：用于建立领域、benchmark 或系统背景。

---

# 新论文进入主库的固定流程

每新增一篇论文，先回答：

1. 它解决哪个问题节点？
2. 它改变 `State / Decision / Action / Executor / Feedback` 中哪一项？
3. 它属于哪条路线？
4. 它解决上一代什么限制？
5. 它新增了什么成本、风险或假设？
6. 它对四张地图的影响属于：A 改结构 / B 强化 / C 反例 / D 竞争路线 / E 背景？
7. 它是否足以进入核心库？

如果没有新增理论、机制、强证据、benchmark、竞争关系或反例，只归档，不升级地图。

---

# 下一轮最高优先级补证

1. `LLM + online operator selection inside evolutionary search` 的直接论文。
2. `LLM selector vs AOS / Bandit / Q-learning` 且固定同一 operator library 的公平实验。
3. dynamic FJSP / FJSP-AGV 中显式使用 `search-stage / Pareto-state / operator-history` 的 LLM controller。
4. online LLM scheduling 的 latency / token / API cost 是否计入评价。
5. multi-objective HH/AOS 中 operator credit assignment 的专业做法。

这些检索会真正改变 Opportunity 1–4 的判断，优先级高于继续无差别扩文献数量。

最后更新：2026-09-15
