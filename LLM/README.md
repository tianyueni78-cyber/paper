# LLM 自动算法设计与动态重调度资料

本目录收集与“LLM 离线生成算子、在线选择算子、动态重调度”相关的公开论文与官方源码入口。资料按研究用途筛选，不代表这些工作与机器–AGV 协同动态柔性作业车间问题完全相同。

## 已下载论文

| 文件 | 研究作用 | 官方源码 |
| --- | --- | --- |
| `papers/01_EoH_ICML2024.pdf` | 学习如何用进化搜索驱动 LLM 生成可执行启发式代码 | [EoH](https://github.com/FeiLiu36/EoH) |
| `papers/02_EoH-S_AAAI2026.pdf` | 学习如何生成小规模、互补的启发式集合，最接近“离线算子库” | [EoH-S](https://github.com/FeiLiu36/EoH-S) |
| `papers/03_ReEvo_NeurIPS2024.pdf` | 学习通过文字反思和种群进化改进启发式代码 | [ReEvo](https://github.com/ai4co/reevo) |
| `papers/05_NS4S_IJCAI2025.pdf` | 调度领域直接证据：LLM 辅助邻域搜索设计与验证 | [NS4S](https://github.com/Zoommy/NS4S) |

## 暂只保留链接

| 论文或项目 | 原因 | 链接 |
| --- | --- | --- |
| LLaMEA | arXiv PDF 约 14 MB，当前网络下载过慢；框架源码完整 | [论文](https://arxiv.org/abs/2405.20132) · [源码](https://github.com/XAI-liacs/LLaMEA) |
| RACE-Sched | 官方动态调度源码已公开，但暂未找到可靠的公开论文 PDF | [源码](https://github.com/cls1277/RACE-Sched) |
| LLM4AlgorithmDesign | 持续维护的 LLM 自动算法设计论文与代码导航，适合继续扩展文献池 | [资料库](https://github.com/FeiLiu36/LLM4Opt) |
| LLM4AD Next | 集成 EoH、ReEvo、MEoH 等自动算法设计方法，平台较重 | [源码](https://github.com/Optima-CityU/LLM4AD_Next) |

## 建议学习顺序

1. EoH：理解“模板函数—LLM生成—执行评价—进化更新”的基础闭环。
2. EoH-S：理解为什么需要互补算子集合，而不是寻找一个万能算子。
3. RACE-Sched：理解慢速生成与快速在线决策如何解耦。
4. NS4S：补充调度邻域设计的论文依据。
5. ReEvo：需要增强反思和反馈机制时再引入。

## 证据边界

- EoH、EoH-S、ReEvo 和 LLaMEA提供通用自动启发式设计机制，不直接解决机器–AGV协同动态重调度。
- NS4S最接近调度邻域搜索，但公开仓库以算例和结果为主，不应作为完整复现代码使用。
- RACE-Sched生成在线派工优先级函数，不等同于生成 NSGA-II/QNSGA-II 邻域算子；其双时间尺度结构可作为方法参考。
- 所有第三方方法均应放在已验证基线之外，不能改写原解码器、目标函数或动态事件逻辑。

