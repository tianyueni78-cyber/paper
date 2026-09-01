# N1 Notion—GitHub 文献对照表

## 1. 匹配规则

- **已匹配**：规范化标题一致，或正文一级标题与 Notion 标题构成唯一对应。
- **缺原文**：仓库中没有合理候选。
- **待确认**：存在候选，但当前证据不能唯一确认。
- 机械规范化仅移除 `MinerU_markdown_`、导出编号、扩展名、空白和明显作者尾缀；英文题名、内部编号及实质性题名差异必须读取正文标题。
- 本表证明资产对应关系，不代表 Notion 中作者、年份、DOI或结论已经核验；这些属于 N2。

## 2. 全量对照

| # | Notion 论文名称 | Notion | GitHub 原文转换文本 | 状态 | 匹配依据 | 备注 |
|---:|---|---|---|---|---|---|
| 1 | 3C智能制造工厂的AGV智慧物料传输与调度综述 | [记录](https://app.notion.com/3bc36ea815e481418c8fd1863a632d29) | [原文](../../MinerU_markdown_3C智能制造工厂的AGV智慧物料传输与调度综述_孙孝飞_2087801893529341952.md) | 已匹配 | 规范化标题一致 | — |
| 2 | A genetic algorithm-based approach for FJSP rescheduling with machine failure | [记录](https://app.notion.com/3bc36ea815e481879e7af7639ca5c78c) | [原文](../../MinerU_markdown_L031_机器故障_右移与完全重调度_GA_2023_2087801543195906048.md) | 已匹配 | 正文标题为 *A genetic algorithm-based approach for flexible job shop rescheduling problem with machine failure interference*，与 Notion 简写唯一对应 | Notion 使用简写题名；N2 核验正式题名 |
| 3 | Dual-resource integrated scheduling of AGV and machine | [记录](https://app.notion.com/3bc36ea815e4813ca208fcd63835d3c8) | [原文](../../MinerU_markdown_智能制造车间AGV与机器双资源集成调度问题（英文）_苑明海_2087802521114660864.md) | 已匹配 | 正文题名为 *Dual-resource integrated scheduling method of AGV and machine in intelligent manufacturing job shop* | Notion 使用简写题名；正文含 DOI |
| 4 | Dynamic scheduling for flexible job shop based on MachineRank algorithm and reinforcement learning | [记录](https://app.notion.com/3bc36ea815e481c39090cc1ca79823b3) | [原文](../../MinerU_markdown_L025_动态FJSP_机器故障_多目标RL_2024_2087801465660006400.md) | 已匹配 | 正文一级标题完全一致 | — |
| 5 | Memetic Algorithm for Dynamic Joint Flexible Job Shop Scheduling with Machines and Transportation Robots | [记录](https://app.notion.com/3bc36ea815e481669f69e43bf145f2a6) | [原文](../../MinerU_markdown_L026_动态FJSP_AGV故障_DDQN_2022_2087801505828851712.md) | 已匹配 | 正文一级标题完全一致 | 文件名中的 `DDQN` 与正文所述 GA+VNS 不一致，列入异常报告 |
| 6 | 一种解决有AGV约束的车间智能调度算法 | [记录](https://app.notion.com/3bc36ea815e48103bbbaf77fbe81e2ba) | [原文](../../MinerU_markdown_一种解决有AGV小车约束的车间智能调度问题的算法_柳赛男_2087802416789741568.md) | 已匹配 | 正文题名仅比 Notion 多“小车”“问题”二词，主题与作者文件唯一 | Notion 使用简写题名 |
| 7 | 仓库多AGV路径冲突问题研究综述 | [记录](https://app.notion.com/3bc36ea815e481eabbf3c3c1ee6918e0) | [原文](../../MinerU_markdown_仓库多AGV路径冲突问题研究综述_颜伟_2087801640445042688.md) | 已匹配 | 规范化标题一致 | — |
| 8 | 分布式AGV调度研究综述与发展趋势分析 | [记录](https://app.notion.com/3bc36ea815e481608b01d8b4b3187312) | [原文](../../MinerU_markdown_分布式AGV调度研究综述与发展趋势分析_张中伟_2087801696384475136.md) | 已匹配 | 规范化标题一致 | — |
| 9 | 势博弈深度强化学习驱动的AGV群能量均衡 | [记录](https://app.notion.com/3bc36ea815e481b1b8c8ee8518e50c37) | [原文](../../MinerU_markdown_势博弈深度强化学习驱动的AGV群能量均衡研究_许波桅_2087802335332163584.md) | 已匹配 | 仓库题名仅增加“研究”，且候选唯一 | Notion 使用简写题名 |
| 10 | 半导体生产车间智能AGV路径规划与调度 | [记录](https://app.notion.com/3bc36ea815e481948cc3d8e952312b0a) | [原文](../../MinerU_markdown_半导体生产车间智能AGV路径规划与调度_李昆鹏_2087801585684205568.md) | 已匹配 | 规范化标题一致 | — |
| 11 | 基于DQN算法的考虑AGV搬运的离散制造车间调度 | [记录](https://app.notion.com/3bc36ea815e481b3935be40ef3d1a338) | [原文](../../MinerU_markdown_基于DQN算法的考虑AGV小车搬运的离散制造车间调度方法_周亚勤_2087801738163937280.md) | 已匹配 | 正文题名仅比 Notion 多“小车”“方法”，候选唯一 | Notion 使用简写题名 |
| 12 | 基于PPO的自动化码头AGV防冲突路径规划 | [记录](https://app.notion.com/3bc36ea815e4819ca842f1cca6817d56) | [原文](../../MinerU_markdown_基于近端策略优化算法的自动化集装箱码头自动导引车防冲突路径规划_肖世昌_2087802055261708288.md) | 已匹配 | PPO 与“近端策略优化”同义，场景和防冲突路径题名唯一 | Notion 使用算法缩写及简写题名 |
| 13 | 基于多智能体强化学习求解柔性作业车间联合调度问题 | [记录](https://app.notion.com/3bc36ea815e481b0869ee91eb9ffd197) | [原文](../../MinerU_markdown_基于多智能体强化学习求解柔性作业车间联合调度问题_孟繁威_2087801954837487616.md) | 已匹配 | 规范化标题一致 | — |
| 14 | 基于改进PPO的AGV路径规划与任务调度 | [记录](https://app.notion.com/3bc36ea815e481d183f5df99805cb9f3) | [原文](../../MinerU_markdown_基于改进近端策略优化算法的AGV路径规划与任务调度_祁璇_2087802590769467392.md) | 已匹配 | PPO 与“近端策略优化算法”同义，正文题名唯一 | Notion 使用算法缩写 |
| 15 | 基于改进花授粉算法的共融AGV作业车间调度 | [记录](https://app.notion.com/3bc36ea815e4810286cceaaed2369007) | [原文](../../MinerU_markdown_基于改进花授粉算法的共融AGV作业车间调度_刘二辉_2087801999854948352.md) | 已匹配 | 规范化标题一致 | — |
| 16 | 基于深度强化学习的AGV行人避让策略 | [记录](https://app.notion.com/3bc36ea815e481fbb312fd0557263b30) | [原文](../../MinerU_markdown_基于深度强化学习的AGV行人避让策略研究_王贺_2087802090091204608.md) | 已匹配 | 仓库题名仅增加“研究”，候选唯一 | Notion 使用简写题名 |
| 17 | 数字孪生驱动的无人仓多AGV全局路径规划 | [记录](https://app.notion.com/3bc36ea815e4817fada6f9146d8fa4f8) | [原文](../../MinerU_markdown_数字孪生驱动的物流仓储无人仓多AGV全局路径规划研究_李明万_2087802381817634816.md) | 已匹配 | 仓库题名增加“物流仓储”“研究”，核心题名和候选唯一 | Notion 使用简写题名 |
| 18 | 智能仓储交通信号与多AGV路径协同控制 | [记录](https://app.notion.com/3bc36ea815e481da968afce26e6f8630) | [原文](../../MinerU_markdown_智能仓储交通信号与多AGV路径规划协同控制方法_司明_2087802456023257088.md) | 已匹配 | 仓库题名增加“规划”“方法”，候选唯一 | Notion 使用简写题名 |
| 19 | 智能仓库中多AGV在线任务指派与全局路径规划 | [记录](https://app.notion.com/3bc36ea815e48179846dfa91ff713d62) | [原文](../../MinerU_markdown_智能仓库中多AGV在线任务指派与全局路径规划问题研究_李昆鹏_2087802485140119552.md) | 已匹配 | 仓库题名增加“问题研究”，候选唯一 | Notion 使用简写题名 |
| 20 | 绿色作业车间与变速充电AGV协同调度 | [记录](https://app.notion.com/3bc36ea815e48179aa48c4585939847d) | [原文](../../MinerU_markdown_绿色作业车间与变速充电AGV协同调度研究_张毅_2087802188787372032.md) | 已匹配 | 仓库题名仅增加“研究”，候选唯一 | Notion 使用简写题名 |
| 21 | 考虑工时不确定的动态FJSP机器与AGV联合调度 | [记录](https://app.notion.com/3bc36ea815e4815cbd9bd1001fbc7673) | [原文](../../MinerU_markdown_考虑工时不确定的动态柔性作业车间机器与AGV联合调度方法_周亚勤_2087802148522057728.md) | 已匹配 | FJSP 与“柔性作业车间”同义，仓库题名增加“方法” | 转换正文一级标题疑似漏掉 `AGV`，N2 核查正式题名 |
| 22 | 自动化集装箱码头双循环AGV与场桥集成调度 | [记录](https://app.notion.com/3bc36ea815e48172b572efe3cd98bfb7) | [原文](../../MinerU_markdown_自动化集装箱码头双循环AGV与场桥的集成调度研究_田宇_2087802560079745024.md) | 已匹配 | 仓库题名增加“的”“研究”，候选唯一 | Notion 使用简写题名 |
| 23 | 面向智能制造的AGV与FJSP协同调度模型与算法 | [记录](https://app.notion.com/3bc36ea815e4811e93e5c57db5c29edb) | [原文](../../MinerU_markdown_面向智能制造的AGV与柔性作业车间协同调度模型与算法_林国义_2087802292558647296.md) | 已匹配 | FJSP 与“柔性作业车间”同义，其余题名一致 | — |
| 24 | 面向智能生产车间的多AGV多目标调度优化 | [记录](https://app.notion.com/3bc36ea815e4819eb5d2eaf102fd0bf1) | [原文](../../MinerU_markdown_面向智能生产车间的多AGV系统多目标调度优化_杨智飞_2087802246886875136.md) | 已匹配 | 仓库题名增加“系统”，候选唯一 | Notion 使用简写题名 |

## 3. 汇总

| 状态 | Notion 记录数 |
|---|---:|
| 已匹配 | 24 |
| 缺原文 | 0 |
| 待确认 | 0 |
| **合计** | **24** |

所有已匹配路径均为仓库中真实存在的文件；24 条 Notion 记录分别对应 24 个不同的 GitHub 文件，没有一对多或多对一占用。

## 4. GitHub 中没有 Notion 记录的可识别文献

以下 5 篇文本没有对应 Notion 行。第 1 篇是明确的研究对象原文；其余 4 篇是后续加入仓库的相关文献，不能在 N1 中擅自补建 Notion 记录。

| 类型 | GitHub 文件 | 状态说明 |
|---|---|---|
| 研究对象 | [原QNSGA-II论文正文](../../原始论文/原QNSGA-II论文正文.md) | Notion 数据库未收录 |
| 相关文献 | [带AGV数量约束的柔性作业车间调度问题研究](../../带AGV数量约束的柔性作业车间调度问题研究_廖雪超.md) | Notion 数据库未收录 |
| 相关文献 | [基于递阶强化学习的多智能体AGV调度系统](../../基于递阶强化学习的多智能体AGV调度系统_李晓萌.md) | Notion 数据库未收录 |
| 相关文献 | [基于异构图注意力的柔性作业车间与AGV集成调度优化方法](../../基于异构图注意力的柔性作业车间与AGV集成调度优化方法_侯亚群.md) | Notion 数据库未收录 |
| 相关文献 | [基于Q-learning改进果蝇算法的针织车间AGV资源配置优化](../../基于Q-learning改进果蝇算法的针织车间AGV资源配置优化_李西兴.md) | Notion 数据库未收录 |

## 5. N1 边界说明

- `已匹配` 只表示记录与原文文件对应关系可靠。
- 正式题名、作者、年份、期刊、DOI及 Notion 分析字段是否忠实于原文，必须在 N2 逐项核验。
- 文件名或转换标题出现的异常保留在重复与缺失报告，不修改原始文件。
