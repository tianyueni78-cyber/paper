# LLM 自动算法设计与动态重调度资料

本目录收集与“LLM 离线生成算子、在线选择算子、动态重调度”相关的公开论文、官方源码快照和研究构想。资料按研究用途筛选，不代表这些工作与机器–AGV 协同动态柔性作业车间问题完全相同。

## 已下载论文

| 文件 | 研究作用 | 官方源码 |
| --- | --- | --- |
| `papers/01_EoH_ICML2024.pdf` | 学习如何用进化搜索驱动 LLM 生成可执行启发式代码 | [EoH](https://github.com/FeiLiu36/EoH) |
| `papers/02_EoH-S_AAAI2026.pdf` | 学习如何生成小规模、互补的启发式集合，最接近“离线算子库” | [EoH-S](https://github.com/FeiLiu36/EoH-S) |
| `papers/03_ReEvo_NeurIPS2024.pdf` | 学习通过文字反思和种群进化改进启发式代码 | [ReEvo](https://github.com/ai4co/reevo) |
| `papers/04_LLaMEA_TEVC2025.pdf` | 学习如何用统一评价接口生成和改进元启发式代码 | [LLaMEA](https://github.com/XAI-liacs/LLaMEA) |
| `papers/05_NS4S_IJCAI2025.pdf` | 调度领域直接证据：LLM 辅助邻域搜索设计与验证 | [NS4S](https://github.com/Zoommy/NS4S) |

## 已收录源码

| 目录 | 主要学习内容 | 收录范围 |
| --- | --- | --- |
| `projects/EoH` | 模板、提示、候选评价及进化循环 | 核心框架及FSSP、动态优化、NSGA-II相关示例 |
| `projects/EoH-S` | 互补启发式集合生成与管理 | 完整核心代码；未收录训练数据、结果和图片 |
| `projects/LLaMEA` | 统一评估器、算法代码生成与迭代 | GitHub当前完整源码快照 |
| `projects/RACE-Sched` | 离线慢速规则生成与在线快速调度 | GitHub当前完整源码快照 |
| `projects/LLM4AD-Next` | 自动算法设计平台、EoH/ReEvo/NSGA-II技能 | 核心源码及相关配置；未收录视频、Docker和第三方组件 |

具体上游提交号、许可证和删减边界见 [`SOURCE_SNAPSHOTS.md`](SOURCE_SNAPSHOTS.md)。

## 扩展资料入口

| 项目 | 用途 | 链接 |
| --- | --- | --- |
| RACE-Sched论文 | 仓库代码已公开，但尚未确认可靠公开论文PDF | [源码主页](https://github.com/cls1277/RACE-Sched) |
| LLM4AlgorithmDesign | 持续维护的LLM自动算法设计论文与代码导航 | [资料库](https://github.com/FeiLiu36/LLM4Opt) |

## 建议学习顺序

1. EoH：理解“模板函数—LLM生成—执行评价—进化更新”的基础闭环。
2. EoH-S：理解为什么需要互补算子集合，而不是寻找一个万能算子。
3. RACE-Sched：理解慢速生成与快速在线决策如何解耦。
4. NS4S：补充调度邻域设计的论文依据。
5. ReEvo：需要增强反思和反馈机制时再引入。
6. LLM4AD Next：需要统一比较多种自动算法设计框架时再研究。

## 证据边界

- EoH、EoH-S、ReEvo 和 LLaMEA提供通用自动启发式设计机制，不直接解决机器–AGV协同动态重调度。
- NS4S最接近调度邻域搜索，但公开仓库以算例和结果为主，不应作为完整复现代码使用。
- RACE-Sched生成在线派工优先级函数，不等同于生成 NSGA-II/QNSGA-II 邻域算子；其双时间尺度结构可作为方法参考。
- 所有第三方方法均应放在已验证基线之外，不能改写原解码器、目标函数或动态事件逻辑。
