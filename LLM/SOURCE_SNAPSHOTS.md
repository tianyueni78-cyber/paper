# 第三方源码快照记录

快照获取日期：2026-09-11。所有项目均作为学习资料收录，未与Python-NEW基线代码混合。上游项目的版权和许可证继续归原作者所有。

| 本地目录 | 上游仓库 | 分支/提交 | 收录范围 | 许可证状态 |
| --- | --- | --- | --- | --- |
| `projects/EoH` | <https://github.com/FeiLiu36/EoH> | `main` / `472545785c936dcfc863d2bc0d6109cf23c7ce62` | 核心`eoh`代码；`fssp_gls`、`fssp_gls_numba`、`evo_dynamic`、`nsga2_pymoo`、`nsga2_crowding`示例；根目录文档 | 已保留上游`LICENSE` |
| `projects/EoH-S` | <https://github.com/FeiLiu36/EoH-S> | `main` / `8310b056ab0d4ea83d194f1d9e8c7873c0a3b892` | 完整`code`核心源码及根目录README；跳过数据集、训练数据、结果、图片和批量启发式输出 | 已保留`code/LICENSE` |
| `projects/LLaMEA` | <https://github.com/XAI-liacs/LLaMEA> | `main` / `2a200f6b48038358223326b45869892b8ca09c4d` | GitHub主分支完整源码压缩快照 | 已保留上游`LICENSE` |
| `projects/RACE-Sched` | <https://github.com/cls1277/RACE-Sched> | `master` / `e44c3aa92f29d93208c3942d6d704216c1d06e62` | GitHub主分支完整源码快照 | 上游仓库未见独立许可证文件，复用或发表前需向作者确认 |
| `projects/LLM4AD-Next` | <https://github.com/Optima-CityU/LLM4AD_Next> | `main` / `d7ca24fe8c0700d5a6752cda9a65b1cb58df9e3c` | `src`核心源码、根目录配置，以及EoH/ReEvo/NSGA-II相关技能和配置；跳过两个演示视频、Docker、第三方内嵌组件和非必要资源 | 已保留BSD-3-Clause `LICENSE`及`THIRD_PARTY_LICENSES.md` |

## 使用边界

1. 这些目录是固定研究快照，不会自动跟随上游更新。
2. 不要把第三方源码直接复制进Python-NEW基线；应先明确接口和许可证，再以独立适配层接入。
3. RACE-Sched没有明确许可证文件，因此当前只用于阅读和方法比较，不建议直接复制其代码进入论文实现。
4. EoH-S和LLM4AD Next采用研究所需源码快照，未收录大体积数据、结果、图片、视频和第三方组件；需要完整实验资产时应从上游仓库按提交号获取。
