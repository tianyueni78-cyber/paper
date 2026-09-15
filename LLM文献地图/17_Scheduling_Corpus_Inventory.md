# Scheduling Corpus Inventory

> 目的：从整个 `paper/main` 识别 Scheduling / FJSP / FJSP-AGV / dynamic scheduling / AGV integrated scheduling 候选正文。此表是 corpus discovery，不等于最终纳入。最终 N 必须经逐篇全文 inclusion/exclusion audit 后冻结。

## Discovery 状态

- Repository recursive tree traversal: completed, `truncated=false`.
- `文献综述/` 与 `LLM文献地图/`：仅导航/交叉核验，不作为原论文正文替代。
- `原始论文/*.pdf`：若没有等价 Markdown 正文，需单独全文读取后决定是否纳入；不得只凭文件名编码。
- 当前所有下列候选均为 `FULL TEXT AUDIT PENDING`，除非后续在 `16_全文阅读审计与进度.md` 明确认证。

## 核心 Scheduling 候选正文

| Candidate ID | Repository File | Initial reason for candidacy | Inclusion Status |
|---|---|---|---|
| S01 | `MinerU_markdown_L025_动态FJSP_机器故障_多目标RL_2024_2087801465660006400.md` | dynamic FJSP + machine breakdown + multi-objective RL | PENDING FULL TEXT |
| S02 | `MinerU_markdown_L026_动态FJSP_AGV故障_DDQN_2022_2087801505828851712.md` | dynamic FJSP + AGV failure + DDQN | PENDING FULL TEXT |
| S03 | `MinerU_markdown_L031_机器故障_右移与完全重调度_GA_2023_2087801543195906048.md` | machine breakdown + rescheduling + GA | PENDING FULL TEXT |
| S04 | `MinerU_markdown_一种解决有AGV小车约束的车间智能调度问题的算法_柳赛男_2087802416789741568.md` | shop scheduling with AGV constraint | PENDING FULL TEXT |
| S05 | `MinerU_markdown_基于DQN算法的考虑AGV小车搬运的离散制造车间调度方法_周亚勤_2087801738163937280.md` | DQN + AGV transport + shop scheduling | PENDING FULL TEXT |
| S06 | `MinerU_markdown_基于多智能体强化学习求解柔性作业车间联合调度问题_孟繁威_2087801954837487616.md` | MARL + flexible job-shop joint scheduling | PENDING FULL TEXT |
| S07 | `MinerU_markdown_基于改进花授粉算法的共融AGV作业车间调度_刘二辉_2087801999854948352.md` | metaheuristic + AGV + job-shop scheduling | PENDING FULL TEXT |
| S08 | `MinerU_markdown_智能制造车间AGV与机器双资源集成调度问题（英文）_苑明海_2087802521114660864.md` | machine-AGV dual-resource integrated scheduling | PENDING FULL TEXT |
| S09 | `MinerU_markdown_绿色作业车间与变速充电AGV协同调度研究_张毅_2087802188787372032.md` | green job shop + variable-speed charging AGV | PENDING FULL TEXT |
| S10 | `MinerU_markdown_考虑工时不确定的动态柔性作业车间机器与AGV联合调度方法_周亚勤_2087802148522057728.md` | dynamic FJSP + machine-AGV joint scheduling | PENDING FULL TEXT |
| S11 | `MinerU_markdown_面向智能制造的AGV与柔性作业车间协同调度模型与算法_林国义_2087802292558647296.md` | FJSP + AGV collaborative scheduling | PENDING FULL TEXT |
| S12 | `MinerU_markdown_面向智能生产车间的多AGV系统多目标调度优化_杨智飞_2087802246886875136.md` | multi-objective multi-AGV scheduling | PENDING FULL TEXT |
| S13 | `基于Q-learning改进果蝇算法的针织车间AGV资源配置优化_李西兴.md` | Q-learning + adaptive metaheuristic + AGV resource configuration | PENDING FULL TEXT |
| S14 | `基于异构图注意力的柔性作业车间与AGV集成调度优化方法_侯亚群.md` | FJSP-AGV integrated scheduling | PENDING FULL TEXT |
| S15 | `带AGV数量约束的柔性作业车间调度问题研究_廖雪超.md` | FJSP with AGV-number constraint | PENDING FULL TEXT |
| S16 | `原始论文/原QNSGA-II论文正文.md` | user's direct algorithmic baseline; dynamic/multi-objective FJSP-AGV | PENDING STRICT RE-CERTIFICATION |

## AGV 调度 / 路径 / 系统候选，需全文判断是否进入主 Scheduling corpus 或边界 corpus

| Candidate ID | Repository File | Initial reason | Inclusion Status |
|---|---|---|---|
| B01 | `MinerU_markdown_3C智能制造工厂的AGV智慧物料传输与调度综述_孙孝飞_2087801893529341952.md` | AGV scheduling review; likely background/boundary | PENDING FULL TEXT |
| B02 | `MinerU_markdown_仓库多AGV路径冲突问题研究综述_颜伟_2087801640445042688.md` | multi-AGV path-conflict review | PENDING FULL TEXT |
| B03 | `MinerU_markdown_分布式AGV调度研究综述与发展趋势分析_张中伟_2087801696384475136.md` | distributed AGV scheduling review | PENDING FULL TEXT |
| B04 | `MinerU_markdown_势博弈深度强化学习驱动的AGV群能量均衡研究_许波桅_2087802335332163584.md` | DRL + AGV fleet energy | PENDING FULL TEXT |
| B05 | `MinerU_markdown_半导体生产车间智能AGV路径规划与调度_李昆鹏_2087801585684205568.md` | AGV path planning + scheduling | PENDING FULL TEXT |
| B06 | `MinerU_markdown_基于改进近端策略优化算法的AGV路径规划与任务调度_祁璇_2087802590769467392.md` | PPO + AGV task scheduling/path planning | PENDING FULL TEXT |
| B07 | `MinerU_markdown_基于深度强化学习的AGV行人避让策略研究_王贺_2087802090091204608.md` | AGV DRL but likely navigation boundary | PENDING FULL TEXT |
| B08 | `MinerU_markdown_基于近端策略优化算法的自动化集装箱码头自动导引车防冲突路径规划_肖世昌_2087802055261708288.md` | PPO AGV conflict-free routing; likely boundary | PENDING FULL TEXT |
| B09 | `MinerU_markdown_数字孪生驱动的物流仓储无人仓多AGV全局路径规划研究_李明万_2087802381817634816.md` | multi-AGV global path planning | PENDING FULL TEXT |
| B10 | `MinerU_markdown_智能仓储交通信号与多AGV路径规划协同控制方法_司明_2087802456023257088.md` | multi-AGV routing/control | PENDING FULL TEXT |
| B11 | `MinerU_markdown_智能仓库中多AGV在线任务指派与全局路径规划问题研究_李昆鹏_2087802485140119552.md` | online task assignment + multi-AGV routing | PENDING FULL TEXT |
| B12 | `MinerU_markdown_自动化集装箱码头双循环AGV与场桥的集成调度研究_田宇_2087802560079745024.md` | AGV integrated scheduling outside FJSP | PENDING FULL TEXT |
| B13 | `基于递阶强化学习的多智能体AGV调度系统_李晓萌.md` | hierarchical RL multi-agent AGV scheduling | PENDING FULL TEXT |

## 原始 PDF 候选

| Candidate ID | Repository File | Initial reason | Inclusion Status |
|---|---|---|---|
| P01 | `原始论文/2023-1708“基于混合学习策略的可变速 AGV 与机器绿色集成调度”.pdf` | green integrated machine-AGV scheduling + learning | PENDING PDF FULL TEXT / DEDUP |
| P02 | `原始论文/【录用】1-s2.0-S2210650224001962-main (1).pdf` | title not sufficient; must inspect full text and deduplicate | PENDING PDF FULL TEXT / DEDUP |

## 下一步冻结规则

1. 对每个候选阅读全文。
2. 判断是否直接属于本文 Scheduling methodology corpus，还是 AGV routing/system boundary corpus。
3. 检查 PDF 与 Markdown 是否为重复版本；重复论文只计一次统计分母，但保留来源映射。
4. 冻结最终 `Scheduling Corpus N = X` 后，才计算 Scheduling corpus 频数与比例。
5. 不以本 inventory 的候选数量直接充当统计分母。