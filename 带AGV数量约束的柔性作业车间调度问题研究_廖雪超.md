# 带 AGV 数量约束的柔性作业车间调度问题研究\*

廖雪超 $^{1,2}$ ，向桂宏 $^{1,2}$ ，阮兵 $^{3}$ ，田芮利 $^{3}$ ，钟实 $^{4}$

（1 武汉科技大学计算机科学与技术学院，武汉 430065；
2 智能信息处理与实时工业系统湖北省重点实验室，武汉 430065；
3 中国汽车工业工程有限公司，天津 300113；
4 武汉钢铁股份有限公司设备管理部技术室，武汉 430081）

摘要: 在实际工业生产过程中,由于自动导引车(Automated Guided Vehicles, AGVs)资源有限,因此在柔性作业车间调度问题(Flexible Job-shop Scheduling Problem, FJSP)中考虑有限AGV数量约束(FJSP-AGV)的集成问题有重要的研究价值。传统的进化算法容易陷入局部最优,不适用于求解此类复杂程度较高的调度问题。针对以上难点,首先对FJSP-AGV集成问题建立数学模型;然后提出了基于启发式规则引导的改进遗传算法,算法针对不同编码段采用多种交叉、变异方式进化种群,同时在进化过程中作参数自适应调整,并通过启发式规则引导变异进行局部搜索,提高算法跳出局部最优的能力,从而实现系统最大完工时间的最小化。通过在两组中小规模数据集上与其他先进算法的对比分析可知,所提算法的整体求解效果最优。

关键词: 柔性作业车间调度; 自动导引车; 车辆调度; 遗传算法; 启发式规则

中图分类号：TP390 文献标志码：A 文章编号：1671-3133(2025)06-0011-11

DOI: 10.16731/j.cnki.1671-3133.2025.06.002

# Research on flexible job-shop scheduling problem with

AGV quantity constraints

LIAO Xuechao $^{1,2}$ , XIANG Guihong $^{1,2}$ , RUAN Bing $^{3}$ , TIAN Ruili $^{3}$ , ZHONG Shi $^{4}$

(1 School of Computer Science and Technology, Wuhan University of Science and Technology, Wuhan 430065, China;

2 Hubei Province Key Laboratory of Intelligent Information Processing and Real-time Industrial System, Wuhan 430065, China;

3 Automotive Engineering Co., Ltd., Tianjin 300113, China;

4 Technical Office of Equipment Management Department, Wuhan Iron and Steel Co., Ltd., Wuhan 430081, China)

Abstract: In the actual industrial production process, due to the limited resources of Automate Guided Vehicles (AGVs), the integrated problem FJSP-AGV considering the constraint of alimited number of AGVs in the Flexible Job-shop Scheduling Problem (FJSP) has significant research value. Traditional evolutionary algorithms are easy to fall into local optimum and are not suitable for solving this scheduling problem with high complexity. In light of the aforementioned challenges, it initially established a mathematical model for FJSP-AGV and subsequently proposed an improved genetic algorithm guided by heuristic rules. The algorithm utilized various crossover and mutation methods to evolve the population for different coding segments. Simultaneously, it adjusted parameters adaptively during the evolutionary process and guided mutations through heuristic rules for local search, thereby enhancing the algorithm's capability to escape local optima and consequently minimize the maximum completion time of the system. Comparison and analysis with other advanced algorithms on two small and medium-sized datasets demonstrated that the algorithm proposed yielded the most comprehensive solving effect.

Keywords: Flexible Job–shop Scheduling Problem (FJSP); Automated Guided Vehicles (AGV); vehicle scheduling; Genetic Algorithms (GA); heuristic rules

## 0 引言

随着大规模定制和自动化生产的不断发展，柔性作业车间调度问题(Flexible Job-shop Scheduling Problem, FJSP)扩展了许多更加贴近实际生产制造的方向。经典的FJSP没有考虑运输资源，即假设车间内的自动导引车(Automated Guided Vehicles, AGVs)的数量是无限的，但在实际车间中存在AGV成本高且数量有限、车间轨道有限等因素，而对车间资源的合理调度是提升车间生产效率、减少生产成本和能耗的重要途径，因此，研究有限数量AGV的FJSP(FJSP-AGV)集成问题更符合实际生产需求，具有重要的理论研究价值。FJSP-AGV需要同时解决4个子问题，即：将每个生产工序分配给一台可以处理它的机器（作业路由子问题）；在每台机器上调度生产工序(机器调度子问题)；分配每个运输任务到AGV(运输分配子问题)，并在每辆AGV上调度运输任务(车辆调度子问题)。显然，FJSP-AGV集成问题是一个比FJSP更复杂的NP-hard问题。

FJSP-AGV 集成问题的最基本研究目标是求解一组最优解，使系统最大完工时间最小化。研究算法主要分为精确算法、启发式算法、仿真算法和智能优化算法。由于 FJSP-AGV 集成问题的复杂性，当前研究的求解算法主要集中在智能优化算法及其混合算法。

部分学者通过精确算法、启发式算法、仿真算法及深度学习等方法对FJSP-AGV集成问题进行研究。HAM[1]开发了2种约束规划模型来解决FJSP-AGV的最优问题。YAO等人[2]基于序列的建模思想开发了一种新颖的混合整数线性规划(Mixed Integer Linear Programming, MILP)模型，该模型被证明比其他MILP模型更有效。LIM等人[3]提出了一种基于两阶段迭代数学规划的启发式算法，它使用以机器工序分配为中心的分解方案来优化完工时间。EROL等人[4]开发了一种基于多代理的方法，该方法在实时环境下工作，并使用代理之间的协商/投标机制产生可行的时间表。孙爱红等人[5]提出一种基于卷积神经网络和深度强化学习的集成算法框架，在小规模问题上与基于多智体系统的算法相比具有更好的求解质量。

在 FJSP-AGV 集成问题的研究中, 智能优化算法及其混合算法应用最为广泛。ZHENG 等人 $^{[6]}$ 设计了新颖的二维解表示方法和两个相邻解的生成方法。CHAUDHRY等人[7]设计了一个基于MicrosoftExcel电子表格的解决方案，使用MicrosoftExcel专有的优化插件GAEvolver来优化问题。YAN等人[8]提出了一种改进的遗传算法，其中设计了3层冗余编码、纠错解码和实体javascript对象表示法。FONTES等人[9]建立了一种新颖的MILP模型来解决小型算例的最优问题，后对该模型进行改进，提出了一种基于相邻序列的MILP模型来求解FJSP-AGV集成问题的最优解[10]，并提出了一种后期接受爬山（LateAcceptanceHillClimbing,LAHC)算法来有效地求解FJSP-AGV集成问题。HAN等人[11]提出了一种新颖的混合整数线性规划模型和双群体协作遗传算法（DualpopulationCollaborativeGeneticAlgorithm,DCGA），并对现有研究中的基准改进了18个当前最佳解决方案。LI等人[12]基于FJSP-AGV集成问题的隐式特征，提出了一种多策略驱动的遗传算法（Multi-strategy-drivenGeneticAlgorithm,Multstra GA）。

算法的融合是提高算法求解质量的有效途径。混合算法往往比单一智能优化算法能取得更好的优化效果。DEROUSSI等人 $^{[13]}$ 设计了一个邻近系统，其中包括3种不同的元启发式算法，即迭代局部搜索、模拟退火及其混合算法。KUMAR等人 $^{[14]}$ 使用差分进化算法，其中专门设计了机器选择启发式和车辆分配启发式。PAN等人 $^{[15]}$ 开发了一种基于学习的多群体算法，其中设计了基于合作的初始化、基于强化学习的交配选择和特定的局部搜索。陈魁等人 $^{[16]}$ 结合竞争学习机制和随机重启机制提出了一种可有效避免早熟的混合离散粒子群优化（Hybrid Discrete Particle Swarm Optimization, HDPSO）算法。胡晓阳等人 $^{[17]}$ 提出了一种融合贪心启发式规则的改进迭代局部搜索算法，该算法对FJSP-AGV集成问题进行了有效求解。FONTES等人 $^{[19]}$ 设计了一种结合贪婪启发式规则的多启动偏置随机密钥遗传算法（Biased Random Key Genetic Algorithm, BRKGA） $^{[18]}$ ，以及一种结合粒子群优化算法和模拟退火算法的混合算法 $^{[19]}$ 用于求解FJSP-AGV集成问题。TANG等人 $^{[20]}$ 开发了一种改进的遗传算法，该算法包含滑动时间窗口启发式算法和车辆分配算法。WEN等人 $^{[21]}$ 设计了一种基于非支配遗传算法（Non-dominated Sorting Genetic Algorithm-II，

NSGA-Ⅱ）结合和谐搜索(Harmony Search, HS)算法的混合算法(HSNSGA-Ⅱ)。

综上所述，FJSP-AGV 集成问题的复杂程度较高，求解难度高于传统的 FJSP，需要算法具备较好的全局寻优能力。遗传算法是一种全局优化算法，它通过模拟自然进化机制来寻求最优解，具有较强的全局搜索能力，但本身也存在过早收敛的缺陷。针对以上难点，本文首先对 FJSP-AGV 集成问题建立数学模型，然后提出了基于启发式规则引导的改进遗传算法（Improved Genetic Algorithm based on Heuristic Guidance, HGIGA），将算法应用于求解 FJSP-AGV 数学模型，实现系统最大完工时间的最小化。

## 1 带 AGV 数量约束的 FJSP

## 1.1 问题描述

本文研究的 FJSP-AGV 集成问题描述如下: 作业车间中有一组机器 $M=\{M_{1},M_{2},\cdots,M_{m},\cdots,M_{l},\cdots,M_{Q}\}$ 、一组作业 $J=\{J_{1},J_{2},\cdots,J_{i},\cdots,J_{N}\}$ 和一组相同的自动导引车 $A=\{A_{1},A_{2},\cdots,A_{k},\cdots,A_{K}\}$ 。每个作业 $J_{i}$ 由一组 $n_{i}$ 个优先级受限的工序组成。作业 $J_{i}$ 的第 j 道工序为 $O_{i,j}$ 。如果工序 $O_{i,j}$ 可以在机器 $M_{m}$ 上处理，则处理时间 $P_{i,j,m}$ 是已知并确定的。作业车间中的作业转移任务由 AGV 执行。在开始加工之前，所有作业和 AGV 都位于装载/卸载（Loading/Unloading, LU）区域。AGV 从 LU 区域到每台机器、每台机器到每台机器，以及每台机器到 LU 区域之间的运输时间是已知和确定的。为方便理解，本文使用来自 DEROUSSI 等人 $^{[22]}$ 的经典数据集中的一个算例。表 1 所示为 FJSP-AGV 经典数据集中的一个算例。由表 1 可知，8 台机器上有 5 个作业要处理，此算例的特点是同一工序在不同机器上的加工时间均相同。表 2 所示为经典数据集中 AGV 的运输时间。

表 1 FJSP-AGV 经典数据集中的一个算例

<table><tr><td>作业</td><td>工序</td><td>可用机器</td><td>加工时间/min</td></tr><tr><td rowspan="3"> ${J}_{1}$ </td><td> ${O}_{1,1}$ </td><td> ${M}_{1},{M}_{2}$ </td><td>12,12</td></tr><tr><td> ${O}_{1,2}$ </td><td> ${M}_{3},{M}_{4}$ </td><td>24,24</td></tr><tr><td> ${O}_{1,3}$ </td><td> ${M}_{7},{M}_{8}$ </td><td>18,18</td></tr><tr><td rowspan="3"> ${J}_{2}$ </td><td> ${O}_{2,1}$ </td><td> ${M}_{1},{M}_{2}$ </td><td>36,36</td></tr><tr><td> ${O}_{2,2}$ </td><td> ${M}_{5},{M}_{6}$ </td><td>12,12</td></tr><tr><td> ${O}_{2,3}$ </td><td> ${M}_{3},{M}_{4}$ </td><td>30,30</td></tr><tr><td rowspan="3"> ${J}_{3}$ </td><td> ${O}_{3,1}$ </td><td> ${M}_{5},{M}_{6}$ </td><td>18,18</td></tr><tr><td> ${O}_{3,2}$ </td><td> ${M}_{7},{M}_{8}$ </td><td>6,6</td></tr><tr><td> ${O}_{3,3}$ </td><td> ${M}_{1},{M}_{2}$ </td><td>24,24</td></tr></table>

<table><tr><td>作业</td><td>工序</td><td>可用机器</td><td>加工时间/min</td></tr><tr><td rowspan="2"> $J_{4}$ </td><td> $O_{4,1}$ </td><td> $M_{7},M_{8}$ </td><td>12,12</td></tr><tr><td> $O_{4,2}$ </td><td> $M_{3},M_{4}$ </td><td>30,30</td></tr><tr><td rowspan="2"> $J_{5}$ </td><td> $O_{5,1}$ </td><td> $M_{5},M_{6}$ </td><td>6,6</td></tr><tr><td> $O_{5,2}$ </td><td> $M_{1},M_{2}$ </td><td>18,18</td></tr></table>

表 1(续)

表 2 经典数据集中 AGV 的运输时间

<table><tr><td>终点位置\运输时间\起点位置</td><td>LU</td><td> ${M}_{1}$ </td><td> ${M}_{2}$ </td><td> ${M}_{3}$ </td><td> ${M}_{4}$ </td><td> ${M}_{5}$ </td><td> ${M}_{6}$ </td><td> ${M}_{7}$ </td><td> ${M}_{8}$ </td></tr><tr><td>LU</td><td>0</td><td>6</td><td>8</td><td>6</td><td>8</td><td>10</td><td>12</td><td>10</td><td>12</td></tr><tr><td> ${M}_{1}$ </td><td>8</td><td>0</td><td>2</td><td>8</td><td>2</td><td>4</td><td>6</td><td>4</td><td>6</td></tr><tr><td> ${M}_{2}$ </td><td>6</td><td>10</td><td>0</td><td>10</td><td>8</td><td>2</td><td>4</td><td>6</td><td>4</td></tr><tr><td> ${M}_{3}$ </td><td>12</td><td>4</td><td>6</td><td>0</td><td>6</td><td>8</td><td>10</td><td>8</td><td>10</td></tr><tr><td> ${M}_{4}$ </td><td>10</td><td>2</td><td>4</td><td>6</td><td>0</td><td>6</td><td>8</td><td>2</td><td>8</td></tr><tr><td> ${M}_{5}$ </td><td>8</td><td>8</td><td>2</td><td>8</td><td>6</td><td>0</td><td>6</td><td>4</td><td>2</td></tr><tr><td> ${M}_{6}$ </td><td>6</td><td>10</td><td>8</td><td>10</td><td>8</td><td>6</td><td>0</td><td>6</td><td>4</td></tr><tr><td> ${M}_{7}$ </td><td>12</td><td>4</td><td>6</td><td>4</td><td>2</td><td>8</td><td>10</td><td>0</td><td>10</td></tr><tr><td> ${M}_{8}$ </td><td>10</td><td>6</td><td>4</td><td>6</td><td>4</td><td>2</td><td>8</td><td>2</td><td>0</td></tr></table>

该经典数据集的车间设备布局如图1所示，图1中LU为装卸区域， $M_{1}\sim M_{8}$ 为8台加工机器，箭头表示该路径允许的运输方向，单箭头为单向路径，双箭头为双向路径。由图1可知，部分路径为单向路径，故表2中相同机器之间的运输时间因方向差异而不同。

![](images/f46d99df85dc58da9de67b563312f8c6e7afe21a8137a1b4b7c58868e6c2da79.jpg)  
图1 车间设备布局

## 1.2 数学模型

本文采用如下假设。

1) 作业之间是相互独立的, 具有相同的优先级, 并且所有作业在开始时刻都是可运输并加工的。

2) 不允许机器资源抢占。

3) 每道工序只能由预定备用机器子集中的一台机器处理,且一次只能在一台机器上执行。

4) 一台机器一次最多只能执行一道工序。

5) 除了每个作业的最后一道工序完成后直接留在当前机器处进行后续处理(或存储)，无需额外运输至 LU 区域外，其他所有工序均需要将作业从当前位置运输至下一个机器的缓冲区。

6) 一旦机器完成任何一道工序, 就可以进行另一道工序。

7) 车辆空载与负载的运输时间均一致。

8) 机器有足够的缓冲空间存放待加工作业和已加工作业及停放运输车辆。

表 3 所示为本文建立数学模型的符号说明。

表 3 本文建立数学模型的符号说明

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
符号 说明
J 作业集合, $J=\{J_{1},J_{2},\cdots,J_{i},\cdots,J_{N}\}$ $O_{i}$  作业 $J_{i}$  的工序集合, $O_{i}=\{O_{i,1},O_{i,2},\cdots,O_{i,j},\cdots,O_{i,n_{i}}\}$ 
M 机器集合, $M=\{M_{1},M_{2},\cdots,M_{m},\cdots,M_{l},\cdots,M_{Q}\}$ $SMT_{m}$  机器 $M_{m}$  开始加工时刻的集合, $SMT_{m}=\{SMT_{n,1},SMT_{m,2},\cdots,SMT_{m,u},\cdots,SMT_{m,U_{m}}\}$ , $U_{m}$  为机器 $M_{m}$ 
当前总加工次数
$EMT_{m}$  机器 $M_{m}$  结束加工时刻的集合, $EMT_{m}=\{EMT_{n,1},EMT_{m,2},\cdots,EMT_{m,u},\cdots,EMT_{m,U_{m}}\}$ 
A 车辆集合, $A=\{A_{1},A_{2},\cdots,A_{k},\cdots,A_{K}\}$ $O_{i,j}$  第 i 个作业的第 j 道工序
$P_{i,j,m}$  第 i 个作业的第 j 道工序在机器 $M_{m}$ 上的加工时刻
$SJ_{i,j,m}$  第 i 个作业的第 j 道工序在机器 $M_{m}$ 加工的开始时刻
$EJ_{i,j,m}$  第 i 个作业的第 j 道工序在机器 $M_{m}$ 加工的结束时刻
$SA_{i,j,k}$  第 i 个作业的第 j 道工序由车辆 $A_{k}$ 运输的开始时刻
$EA_{i,j,k}$  第 i 个作业的第 j 道工序由车辆 $A_{k}$ 运输的结束时刻
$EAt_{k}$  车辆 $A_{k}$ 前一次运输的结束时刻
$T_{m,l}$  机器 $M_{m}$ 与机器 $M_{l}$ 之间的运输时间
$Eat_{k,O_{i,j}}$  车辆 $A_{k}$ 运输 $O_{i,j}$ 前空载的结束时刻
$X_{i,j,m}$  若 $O_{i,j}$ 在机器 $M_{m}$ 上加工则为1，否则为0
$Y_{i,j,k}$  若 $O_{i,j}$ 由车辆 $A_{k}$ 运输则为1，否则为0
$L_{m,u+1}$  若机器 $M_{m}$ 存在第u+1段加工时间则为0，否则为+∞
$C_{i}$  作业 $J_{i}$ 的完工时间
$C_{max}$  系统最大完工时间
</div>

本文 FJSP-AGV 集成问题的优化目标是使系统最大完工时间最小化, 即:

$$
C _ {\max} = \min (\max _ {1 \leqslant i \leqslant N} C _ {i})\tag{1}
$$

系统遵循如下约束条件。

1) 任意工序都只由一台机器加工完成, 即:

$$
\sum_ {m \in Q} X _ {i, j, m} = 1\tag{2}
$$

2) 任意工序的运输任务最多只由一台 AGV 完成, 即:

$$
\sum_ {k \in K} Y _ {i, j, k} \leqslant 1\tag{3}
$$

3) 各作业的工序紧前紧后关系, 即:

$$
E J _ {i, j - 1, m} <   S J _ {i, j, l}\tag{4}
$$

4) AGV 的每一次可用调度都必须在上一次运输结束之后, 即:

$$
E A t _ {k} <   E a t _ {k, O _ {i, j}}\tag{5}
$$

5) 作业运输的开始时刻 $SA_{i,j,k}$ 取决于前一道工序加工结束时刻与 AGV 空载结束时刻之间的最大值，即：

$$
S A _ {i, j, k} = \max (E J _ {i, j - 1, m}, E a t _ {k, O _ {i, j}})\tag{6}
$$

6) 作业运输的结束时刻 $EA_{i,j,k}$ 与运输需求 $Y_{i,j,k}$ 及机器之间的运输时间 $T_{m,l}$ 有关, 即:

$$
E A _ {i, j, k} = S A _ {i, j, k} + T _ {m, l} \cdot Y _ {i, j, k}\tag{7}
$$

7) 作业在机器上加工的开始时刻 $SJ_{i,j,m}$ 取决于机器结束加工时刻 $EMT_{m,u}$ 与 AGV 运输结束时刻 $EA_{i,j,k}$ 之间的最大值，即：

$$
S J _ {i, j, m} = \max (E M T _ {m, u}, E A _ {i, j, k})\tag{8}
$$

8) 作业在机器上加工的结束时刻与处理时间 $P_{i,j,m}$ 及加工开始时刻有关, 即:

$$
E J _ {i, j, m} = S J _ {i, j, m} + P _ {i, j, m}\tag{9}
$$

9) 往机器加工队列中插入新作业时, 作业开始时间 $SJ_{i,j,m}$ 需在机器的某一空闲时间内, 且该空闲时间应不小于新作业加工时间, 即:

$$
E M T _ {m, u} \leqslant S J _ {i, j, m}\tag{10}
$$

$$
S J _ {i, j, m} + P _ {i, j, m} \leqslant S M T _ {m, u + 1} + L _ {m, u + 1}\tag{11}
$$

10) 若有新工序插入加工队列, 则更新机器 $M_{m}$ 当前总加工次数 $U_{m}, U_{m}$ 初始为 0, 即:

$$
U _ {m} = U _ {m} + 1\tag{12}
$$

11) 新工序插入机器加工队列后, 机器新增一段新的使用时间段, 即 $u+1$ , 则该使用时间段的开始加工时刻为:

$$
S M T _ {m, u + 1} = S J _ {i, j, m}\tag{13}
$$

12) 新工序插入机器加工队列后, 机器新增一段新的使用时间段, 即 $u+1$ , 则该使用时间段的结束加工时刻为:

$$
E M T _ {m, u + 1} = E J _ {i, j, m}\tag{14}
$$

13) 各作业的完工时间由最后一道工序的结束时刻决定, 即:

$$
C _ {i} = \max _ {j \in n _ {i}, m \in Q} E J _ {i, j, m}\tag{15}
$$

## 2 改进遗传算法求解FJSP-AGV集成问题

## 2.1 算法整体流程

HGIGA 流程如图 2 所示。由图 2 可知，HGIGA 流程主要包括编码、解码、遗传进化、精英库和启发式引导等。

1) 编码、解码: 编码采用基于工序的 3 层编码方案, 解码时考虑工序插入约束。

2) 种群初始化: 为了保证种群的多样性, 兼顾算法收敛效率, 通过 2 种生成方式得到初始种群。种群的 80% 随机生成, 20% 由启发式规则生成, 以最小加工时间为主要规则, 选择加工机器。

3) 进化算子与进化参数: 采用多种方式进行交叉变异, 设计进化参数自适应调整。

4) 种群多样性保持: 采用外部精英库, 并以一定概率参与进化。进化陷入局部最优时对最优解进行启发式规则引导变异。

![](images/1fe38dea85549ed7b834aae3b50d3caa070ff8ab3feae5567b0c0dbd7b3c9e2a.jpg)  
图2 HGIGA流程

## 2.2 染色体编码与解码

针对 FJSP-AGV 集成问题,本文采用基于工序的 3 层编码方案,每个个体的染色体长度均为 3n,其中 n 为作业集中的生产工序总数。染色体中的 1\~n 位代表所有作业的加工排序,记为 OS; $n+1\sim2n$ 位代表与工序排序对应的加工机器分配,记为 MS; $2n+1\sim3n$ 位代表对应的运输车辆指派,记为 AS。本文第 1.1 节中提及的 5 个作业,8 台机器,2 辆 AGV 的可行调度编码示例如图 3 所示。

<table><tr><td>对应工序</td><td> $O_{2,1}$ </td><td> $O_{3,1}$ </td><td> $O_{1,1}$ </td><td> $O_{4,1}$ </td><td> $O_{1,2}$ </td><td> $O_{5,1}$ </td><td> $O_{2,2}$ </td><td> $O_{5,2}$ </td><td> $O_{4,2}$ </td><td> $O_{3,2}$ </td><td> $O_{2,3}$ </td><td> $O_{3,3}$ </td><td> $O_{1,3}$ </td></tr><tr><td>OS</td><td>2</td><td>3</td><td>1</td><td>4</td><td>1</td><td>5</td><td>2</td><td>5</td><td>4</td><td>3</td><td>2</td><td>3</td><td>1</td></tr><tr><td>MS</td><td>2</td><td>5</td><td>1</td><td>7</td><td>4</td><td>5</td><td>5</td><td>2</td><td>3</td><td>8</td><td>4</td><td>1</td><td>7</td></tr><tr><td>对应机器</td><td> $M_2$ </td><td> $M_5$ </td><td> $M_1$ </td><td> $M_7$ </td><td> $M_4$ </td><td> $M_5$ </td><td> $M_5$ </td><td> $M_2$ </td><td> $M_3$ </td><td> $M_8$ </td><td> $M_4$ </td><td> $M_1$ </td><td> $M_7$ </td></tr><tr><td>AS</td><td>2</td><td>1</td><td>2</td><td>1</td><td>1</td><td>2</td><td>1</td><td>1</td><td>2</td><td>2</td><td>1</td><td>2</td><td>1</td></tr></table>

图3 可行调度编码示例

图3中，OS段为工序编码，每个数字即是作业的编号，从左到右，同一编号出现的次数对应该作业的工序编号。如OS段的前5个数字：2、3、1、4、1，分别对应作业 $J_{2}, J_{3}, J_{1}, J_{4}, J_{1}$ ，而1出现2次，分别依次代表 $J_{1}$ 的第一道工序 $O_{1,1}$ 和第二道工序 $O_{1,2}$ ，数字2、3、4当前仅出现1次，代表各自作业的第一道工序；MS段为机器编码，每个数字对应机器编号；AS段为车辆编码，每个数字对应AGV编号。3段编码长度一致，同一位置的3个数字组合后具体含义为：由AS中的车辆运输OS中的作业工序到MS中的机器上去加工。

图 4 所示为机器加工队列安排。解码过程中需要遍历机器所有可用时间，当遍历过程中没找到满足可插入条件的可用时间节点的时，将新到来的工序安排在队列最后，见 4a)。如果找到了满足可插入条件的可用时间节点，则插入新工序，见图 4b)。

![](images/8309845b188409b7b1521885991063032e0c71f0e92436edc79e3685c2e6d110.jpg)  
a) 不满足可插入条件

![](images/a715eb95704975d8107e40290a4d06017647d723f8a7bc242735ffe2439f9921.jpg)  
b) 满足可插入条件  
图4 机器加工队列安排

## 2.3 进化算子选择与进化参数自适应

为了改进遗传算法的性能,本文针对进化算子的选择及进化参数进行改进。首先,对于交叉算子的选择,可以考虑使用多种不同的交叉方式,如针对 OS 基因段,本文选择基于工序编码的交叉(Precedence Operation Crossover, POX)变异方式,其产生的子代能够很好地继承父代优良特征并且总是可行的;MS 和 OS 基因段的交叉受限于问题本身的资源条件,比如可用机器和可用车辆的数量,因此本文选择简单的基于位置的交叉(Position-Based Crossover, PBX)变异方式。然后,引入自适应机制来调整交叉概率,使其在算法的不同阶段或不同种群状态下动态变化,以增加算法的灵活性和适应性。交叉概率 Pc 为:

$$
P c = \max \left(1 - \frac {g e n}{m a x g e n}, P c _ {0}\right)\tag{15}
$$

式中: Pc 为交叉概率; gen 为当前迭代次数; maxgen 为总迭代次数; $Pc_{0}$ 为最小交叉概率。

最小交叉概率保证迭代至后期也能有一定数量的新个体产生,保持种群的多样性。

对于变异算子的选择,本文在 MS 基因段和 AS 基因段均选择单点变异,针对工序编码 OS 基因段选择了一种邻域变异方案,邻域变异流程如图 5 所示。图 5 中,rand 为 $[0,1]$ 之间的随机数; Pm 为变异概率; r 为集合 D 序列数, $r=1,2,\cdots,R$ ; Z 为邻域解集。

![](images/284951d63ec58c9fa7a6abc854d269c16ec72249994f7a0dec07dcf8daf83441.jpg)  
图5 邻域变异流程

在此邻域变异方案中，得到新的OS编码后，旧OS基因段对应的机器编码MS存在失效的情况，因此需要以和OS编码同样的交换顺序 $d_{r}$ 变异MS基因段，才能得到有效的新个体 $X_{n,r}^{\prime}$ 。图6所示为邻域变异关键步骤示例。图6中，将选中的作业 $J' = \{J_3, J_5\}$ 按位置序列 $d_{2} = \{6, 10\}$ 顺序插入，进行作业位置的交换，得到新OS，同样按 $d_{2} = \{6, 10\}$ 的位置顺序交换原MS对应位置的编码，得到新MS。

选中的作业 $J'=\{J_{3},J_{5}\}$ 选中的位置  
全排列集合  
$D = \{\{10,6\},\{6,10\}\} ,d_{1} = \{10,6\} ,d_{2} = \{6,10\}$  
![](images/a05516fffc8d58f7fb912b5f4ba08a4e979113397fa14ecc960522bb1ee7fdd0.jpg)  
图6 邻域变异关键步骤示例

在变异概率的设计上,本文同样引入参数自适应机制来调整变异概率和变异程度,以确保在算法的迭代过程中保持种群多样性,并避免陷入局部最优解,采用 HUANG 等人 $^{[23]}$ 改进的变异概率,即

$$
P m = P m _ {0} + \frac {q}{1 0 0}\tag{16}
$$

式中: Pm 为变异概率; $Pm_{0}$ 为初始变异概率; q 为最佳适应度值保持连续不变的迭代次数。

## 2.4 外部精英库

在遗传算法中,优秀个体在进化过程中存在丢失的可能,影响算法寻优的效率。为了改变这一影响,本文使用外部精英库,若迭代产生新的最优解,则将当前种群的前10%优秀个体保存在外部精英库中。

此外,本文还设计了精英参与概率,即 Pe=0.5。外部精英库中的优秀个体在概率 Pe 下参与种群的交叉和变异,最优值发生变化时更新外部精英库,在保持种群多样性的同时也避免了优秀个体丢失的情况。

## 2.5 启发式规则引导变异

考虑到遗传算法经常出现“早熟”现象，影响寻优效果，本文采取当最优值连续 $t$ 次迭代无变化时，由启发式规则引导个体变异，尝试产生更优个体。

## 3 对比实验及分析

## 3.1 实验数据集以及参数设置

本文改进的 HGIGA 在配备 Intel Core i5-12400F

CPU(2.5 GHz、16 GB RAM) 的计算机上实现, 实验平台为 MATLAB R2022a。

实验数据集采用 2 个基准数据集, 数据集 1 是 DEROUSSI 等人 $^{[22]}$ 提出的 10 个考虑作业运输的柔性作业车间调度问题基准算例, 该数据集共 10 组算例, 分为 fjsp1\~fjsp10, 每组算例有 5\~8 个作业, 每个作业有 2\~5 道工序, 有 8 台机器, 2 辆 AGV。图 7 所示为启发式规则引导变异算法流程。

```txt
Algorithm 1: 启发式规则引导变异

Input: 优秀个体，车辆集合，加工机器，加工时间，机器间行驶时间
Output: 启发式规则引导变异后的新个体
For Chrom_elite工序码OS段每一个作业J
    #获取作业上一次加工结束时间及作业当前机器位置
    [E_J_last, J_site] ← Get_info(J);
    For m=1:M
    For v=1:V
    A_site ← Get_AGV(v); #获取车辆信息
    #计算当前运输信息
    Burden_End[v] ← Get_End(v; E_J_last, ET_A_site, T_j_ske,m);
    #默认开工时间取作业达到时间与机器上次加工结束时间两者中最大值
    M_start ← max(Burden_End[v], E_M_last[m]);
    If Firstuse(m)==1 #若机器第一次加工
    #将作业达到时间作为开工时间存入
    Start_Array[m,v] ← Burden_End[v];
    Else #若机器不是第一次加工
    #遍历机器占用时间，进行机器调度插入条件判断
    For u=1:L_usetime
    #若作业达到时间早于第u段占用时间末
    且第u、u+1段之间空闲时间>=处理时间
    If MuT_Array[u,2] > Burden_End[v] && u ≠ L_usetime
    && MuT_Array[u+1,1] - MuT_Array[u,2] >= P(m)
    M_start ← MuT_Array[u,2]; #开工时间为第u段占用时间末
    Break;
    #若作业达到时间晚于第u段占用时间末
    且第u+1段占用时间始-作业到达时间>=处理时间
    ElseIf MuT_Array[u,2] < Burden_End[v] && u ≠ L_usetime
    && MuT_Array[u+1,1] - Burden_End[v] >= P(m)
    M_start ← Burden_End[v]; #开工时间为作业达到时间
    Break;
    End
    End
    Start_Array[m,v] ← M_start; #将各个组合的开工时间存入
    End
End
End
选择Start_Array中开工最快的组合，更新对应MS与AS段编码；
更新作业、机器、车辆信息；
```  
图7启发式规则引导变异算法流程

数据集 2 是由 KUMAR 等人 $^{[14]}$ 改编的 EX 系列算例，该数据集考虑到每个工序都可以在 3 台替代机器中完成。数据集 2 基于 10 组算例、4 种布局和 3 辆 AGV，数据被组合为 EX11～EX104，其中末位数字表示布局（1～4），前面的数字表示第 1～第 10 组作业（算例）。由于数据源自身的原因，第 3、6 和 10 组作业数据无法使用。为了使计算结果更有意义，本文在算法运行时连续运行每个测试算例 10 次。HGIGA 实验参数如表 4 所示。

表 4 HGIGA 实验参数

<table><tr><td>参数</td><td>参数值</td></tr><tr><td>最小交叉概率  $Pc_0$ </td><td>0.5</td></tr><tr><td>初始变异概率  $Pm_0$ </td><td>0.2</td></tr><tr><td>精英参与概率  $Pe$ </td><td>0.5</td></tr><tr><td>总迭代次数 maxgen</td><td>100</td></tr><tr><td>种群大小 popsize</td><td>100</td></tr><tr><td>轮盘赌选择概率  $Ps$ </td><td>0.8</td></tr></table>

## 3.2 HGIGA与GA实验对比

为了更好地验证 HGIGA 的改进效果,本节将 HGIGA 分别与未改进的 GA 和改进遗传算法(IGA)使用数据集 1 进行实验对比,对比指标为完工时间最优值和平均值。表 5 所示为对比算法介绍,实验结果如表 6 所示,表 6 中 Best 为求解得到的完工时间最优值,Mean 为完工时间平均值,HGIGA 下方加粗数值表示等于或优于对比算法。从表 7 中可以看出,HGIGA 的所有求解结果均明显优于 GA 和 IGA,三者对比,可见 HGIGA 的改进效果明显。

表 5 对比算法介绍

<table><tr><td>对比算法</td><td>算法介绍</td></tr><tr><td>GA</td><td>未改进遗传算法</td></tr><tr><td>IGA</td><td>参数自适应和进化算子改进</td></tr><tr><td>HGIGA</td><td>参数自适应和进化算子改进、启发式规则引导变异</td></tr></table>

表 6 实验结果

<table><tr><td rowspan="2">算例</td><td colspan="2">GA</td><td colspan="2">IGA</td><td colspan="2">HGIGA</td></tr><tr><td>Best</td><td>Mean</td><td>Best</td><td>Mean</td><td>Best</td><td>Mean</td></tr><tr><td>fjsp1</td><td>146.0</td><td>149.8</td><td>144.0</td><td>149.4</td><td>144.0</td><td>148.6</td></tr><tr><td>fjsp2</td><td>118.0</td><td>121.0</td><td>118.0</td><td>120.2</td><td>114.0</td><td>120.2</td></tr><tr><td>fjsp3</td><td>126.0</td><td>127.6</td><td>122.0</td><td>125.4</td><td>120.0</td><td>126.2</td></tr><tr><td>fjsp4</td><td>120.0</td><td>125.6</td><td>122.0</td><td>124.8</td><td>118.0</td><td>123.4</td></tr><tr><td>fjsp5</td><td>94.0</td><td>94.8</td><td>94.0</td><td>95.2</td><td>94.0</td><td>94.6</td></tr><tr><td>fjsp6</td><td>144.0</td><td>148.4</td><td>146.0</td><td>149.0</td><td>144.0</td><td>147.8</td></tr><tr><td>fjsp7</td><td>124.0</td><td>126.6</td><td>120.0</td><td>124.2</td><td>112.0</td><td>122.2</td></tr><tr><td>fjsp8</td><td>181.0</td><td>186.7</td><td>181.0</td><td>185.0</td><td>180.0</td><td>183.9</td></tr><tr><td>fjsp9</td><td>146.0</td><td>151.2</td><td>146.0</td><td>149.8</td><td>144.0</td><td>148.6</td></tr><tr><td>fjsp10</td><td>182.0</td><td>190.8</td><td>180.0</td><td>187.4</td><td>178.0</td><td>187.0</td></tr></table>

为了更直观对比改进效果,本文选择算例 fjsp1 的收敛曲线进行对比。图 8 所示为 3 种算法收敛曲线对比。

![](images/902c69d519ae8be6774906381430512b9489d035b4abfdedefe8641d4bd9b09d.jpg)  
a) HGIGA与GA收敛的情况对比

![](images/b08ff648006fe505f243870280cb7ea7f4f6cced36ce31fdd16df4b931888d0e.jpg)  
b) HGIGA与IGA收敛的情况对比  
图83种算法收敛曲线对比

由图 8 可见, GA 收敛速度较慢, 且 “早熟” 现象明显, 寻优效果差, 经过 IGA 收敛速度得到提升, 但依旧存在明显的 “早熟” 情况, 而 HGIGA 在后期具备一定跳出局部最优的能力, 寻优效果均优于前两者。

## 3.3 HGIGA与其他算法的对比

为了验证本文改进的 HGIGA 求解 FJSP-AGV 集成问题的能力,本文分别对数据集 1 和数据集 2 与其他优化算法进行对比。

## 3.3.1 数据集1的实验对比

对于数据集 1, 本文选择了 3 个基于群体的先进算法进行对比, 表 7 所示为数据集 1 对比算法介绍。

表 7 数据集 1 对比算法介绍

<table><tr><td>对比算法</td><td>算法介绍</td></tr><tr><td>HDPSO[16]</td><td>结合竞争学习机制和随机重启机制的混合离散粒子群优化算法</td></tr><tr><td>HSNSGA-II[21]</td><td>基于 NSGA-II 和和谐搜索算法的混合算法</td></tr><tr><td>GA Evolver[7]</td><td>基于 Microsoft Excel 专有的优化算法</td></tr></table>

HGIGA 与其他算法在数据集 1 上的对比结果如表 8 所示, 对比指标为完工时间最优值 Best 和平均值 Mean。表 8 中 “一” 处表示该算法未公布该指标。

由表 8 可见, HGIGA 仅在 fjsp8 上寻优结果稍差于 GA Evolver, 但在整体上优于 GA Evolver。此外, HGIGA 的寻优结果均优于 HDPSO 和 HNSGA-Ⅱ。

表 8 HGIGA 与其他算法在数据集 1 上的对比结果

<table><tr><td rowspan="2">算例</td><td colspan="2">HDPSO</td><td colspan="2">HSNSGA-II</td><td colspan="2">GA Evolver</td><td colspan="2">HGIGA</td></tr><tr><td>Best</td><td>Mean</td><td>Best</td><td>Mean</td><td>Best</td><td>Mean</td><td>Best</td><td>Mean</td></tr><tr><td>fjsp1</td><td>148.0</td><td>154.4</td><td>150.0</td><td>153.1</td><td>144.0</td><td>—</td><td>144.0</td><td>148.6</td></tr><tr><td>fjsp2</td><td>118.0</td><td>130.4</td><td>120.0</td><td>129.6</td><td>118.0</td><td>—</td><td>114.0</td><td>120.2</td></tr><tr><td>fjsp3</td><td>130.0</td><td>135.4</td><td>132.0</td><td>133.2</td><td>124.0</td><td>—</td><td>120.0</td><td>126.2</td></tr><tr><td>fjsp4</td><td>126.0</td><td>133.4</td><td>132.0</td><td>136.0</td><td>124.0</td><td>—</td><td>118.0</td><td>123.4</td></tr><tr><td>fjsp5</td><td>94.0</td><td>95.2</td><td>96.0</td><td>97.2</td><td>94.0</td><td>—</td><td>94.0</td><td>94.6</td></tr><tr><td>fjsp6</td><td>150.0</td><td>154.0</td><td>148.0</td><td>152.8</td><td>144.0</td><td>—</td><td>144.0</td><td>147.8</td></tr><tr><td>fjsp7</td><td>126.0</td><td>131.0</td><td>126.0</td><td>133.2</td><td>120.0</td><td>—</td><td>112.0</td><td>122.2</td></tr><tr><td>fjsp8</td><td>186.0</td><td>190.3</td><td>188.0</td><td>190.3</td><td>179.0</td><td>—</td><td>180.0</td><td>183.9</td></tr><tr><td>fjsp9</td><td>152.0</td><td>154.8</td><td>154.0</td><td>156.8</td><td>146.0</td><td>—</td><td>144.0</td><td>148.6</td></tr><tr><td>fjsp10</td><td>190.0</td><td>196.8</td><td>192.0</td><td>196.8</td><td>182.0</td><td>—</td><td>178.0</td><td>187.0</td></tr></table>

## 3.3.2 数据集2的实验对比

数据集 2 与数据集 1 的最大不同点在于,作业会出现在同一机器连续加工的情况,作业加工和运输有更多的组合。对于数据集 2,本文选择了 4 个最新的寻优算法进行对比,数据集 2 对比算法介绍如表 9 所示。

表 9 数据集 2 对比算法介绍

<table><tr><td>对比算法</td><td>算法介绍</td></tr><tr><td>GA Evolver[7]</td><td>基于 Microsoft Excel 专有的优化算法</td></tr><tr><td>BRKGA[18]</td><td>基于工序的多启动偏置随机密钥遗传算法</td></tr><tr><td>DCGA[11]</td><td>双群体协作遗传算法</td></tr><tr><td>LAHC[10]</td><td>基于局部迭代搜索的晚期接受爬山法</td></tr><tr><td>Mult-stra-GA[12]</td><td>多策略驱动遗传算法</td></tr></table>

对比指标为完工时间最优值和百分比偏差 Dev，HGIGA 与其他算法在数据集 2 上的对比结果如表 10 所示。

表 10 中, Dev 大于 0 表示 HGIGA 优于该算法, 等于 0 表示 2 种算法寻优结果一致, 小于 0 表示 HGIGA 差于该算法。表 10 中下界 $^{[10]}$ 表示通过简化模型计算出的该算例的最优值下限。

百分比偏差的计算公式为:

$$
Dev = \frac {C _ {\mathrm{other}} - C _ {\mathrm{HGIGA}}}{C _ {\mathrm{HGIGA}}} \times 100\%
$$

式中: Dev 为百分比偏差; $C_{other}$ 和 $C_{HGIGA}$ 分别为对比算法和 HGIGA 的完工时间最优值。

表 10 HGIGA 与其他算法在数据集 2 上的对比结果

<table><tr><td rowspan="2">算例</td><td rowspan="2">下界</td><td colspan="2">GA Evolver</td><td colspan="2">BRKGA</td><td colspan="2">DCGA</td><td colspan="2">LAHC</td><td colspan="2">Mult-stra-GA</td><td colspan="2">HGIGA</td></tr><tr><td>Best</td><td>Dev</td><td>Best</td><td>Dev</td><td>Best</td><td>Dev</td><td>Best</td><td>Dev</td><td>Best</td><td>Dev</td><td>Best</td><td>Mean</td></tr><tr><td>EX11</td><td>57</td><td>70</td><td>0.00</td><td>70</td><td>0.00</td><td>70</td><td>0.00</td><td>70</td><td>0.00</td><td>78</td><td>11.43</td><td>70</td><td>71.2</td></tr><tr><td>EX12</td><td>51</td><td>56</td><td>-6.67</td><td>59</td><td>-1.67</td><td>56</td><td>-6.67</td><td>56</td><td>-6.67</td><td>52</td><td>-13.33</td><td>60</td><td>61.6</td></tr><tr><td>EX13</td><td>55</td><td>62</td><td>0.00</td><td>62</td><td>0.00</td><td>62</td><td>0.00</td><td>62</td><td>0.00</td><td>58</td><td>-6.45</td><td>62</td><td>62.8</td></tr><tr><td>EX14</td><td>57</td><td>78</td><td>8.33</td><td>78</td><td>8.33</td><td>78</td><td>8.33</td><td>78</td><td>8.33</td><td>79</td><td>9.72</td><td>72</td><td>73.8</td></tr><tr><td>EX21</td><td>48</td><td>74</td><td>1.37</td><td>76</td><td>4.11</td><td>74</td><td>1.37</td><td>74</td><td>1.37</td><td>86</td><td>17.81</td><td>73</td><td>77.3</td></tr><tr><td>EX22</td><td>42</td><td>62</td><td>-1.59</td><td>62</td><td>-1.59</td><td>62</td><td>-1.59</td><td>62</td><td>-1.59</td><td>59</td><td>-6.35</td><td>63</td><td>66.7</td></tr><tr><td>EX23</td><td>44</td><td>67</td><td>0.00</td><td>67</td><td>0.00</td><td>67</td><td>0.00</td><td>67</td><td>0.00</td><td>61</td><td>-8.96</td><td>67</td><td>70.8</td></tr><tr><td>EX24</td><td>47</td><td>84</td><td>9.09</td><td>87</td><td>12.99</td><td>84</td><td>9.09</td><td>84</td><td>9.09</td><td>85</td><td>10.39</td><td>77</td><td>80.1</td></tr><tr><td>EX41</td><td>52</td><td>72</td><td>41.18</td><td>72</td><td>41.18</td><td>72</td><td>41.18</td><td>72</td><td>41.18</td><td>65</td><td>27.45</td><td>51</td><td>52.1</td></tr><tr><td>EX42</td><td>49</td><td>59</td><td>40.48</td><td>58</td><td>38.10</td><td>56</td><td>33.33</td><td>56</td><td>33.33</td><td>36</td><td>-14.29</td><td>42</td><td>45.2</td></tr><tr><td>EX43</td><td>51</td><td>62</td><td>34.78</td><td>63</td><td>36.96</td><td>61</td><td>32.61</td><td>61</td><td>32.61</td><td>40</td><td>-13.04</td><td>46</td><td>46.8</td></tr><tr><td>EX44</td><td>52</td><td>80</td><td>50.94</td><td>82</td><td>54.72</td><td>80</td><td>50.94</td><td>80</td><td>50.94</td><td>65</td><td>22.64</td><td>53</td><td>55.7</td></tr><tr><td>EX51</td><td>46</td><td>59</td><td>5.36</td><td>61</td><td>8.93</td><td>59</td><td>5.36</td><td>59</td><td>5.36</td><td>68</td><td>21.43</td><td>56</td><td>59.1</td></tr><tr><td>EX52</td><td>44</td><td>47</td><td>0.00</td><td>49</td><td>4.26</td><td>47</td><td>0.00</td><td>48</td><td>2.13</td><td>33</td><td>-29.79</td><td>47</td><td>49.6</td></tr><tr><td>EX53</td><td>43</td><td>52</td><td>1.96</td><td>53</td><td>3.92</td><td>52</td><td>1.96</td><td>52</td><td>1.96</td><td>40</td><td>-21.57</td><td>51</td><td>54.1</td></tr><tr><td>EX54</td><td>46</td><td>64</td><td>6.67</td><td>68</td><td>13.33</td><td>64</td><td>6.67</td><td>64</td><td>6.67</td><td>68</td><td>13.33</td><td>60</td><td>63.1</td></tr><tr><td>EX71</td><td>48</td><td>82</td><td>-2.38</td><td>81</td><td>-3.57</td><td>81</td><td>-3.57</td><td>81</td><td>-3.57</td><td>104</td><td>23.81</td><td>84</td><td>88.5</td></tr><tr><td>EX72</td><td>44</td><td>63</td><td>-7.35</td><td>62</td><td>-8.82</td><td>61</td><td>-10.29</td><td>62</td><td>-8.82</td><td>55</td><td>-19.12</td><td>68</td><td>73</td></tr><tr><td>EX73</td><td>47</td><td>67</td><td>-14.10</td><td>67</td><td>-14.10</td><td>66</td><td>-15.38</td><td>66</td><td>-15.38</td><td>64</td><td>-17.95</td><td>78</td><td>81.7</td></tr><tr><td>EX74</td><td>48</td><td>95</td><td>1.06</td><td>97</td><td>3.19</td><td>94</td><td>0.00</td><td>94</td><td>0.00</td><td>106</td><td>12.77</td><td>94</td><td>98.7</td></tr><tr><td>EX81</td><td>66</td><td></td><td></td><td>93</td><td>22.37</td><td>91</td><td>19.74</td><td>94</td><td>23.68</td><td>90</td><td>18.42</td><td>76</td><td>80.4</td></tr><tr><td>EX82</td><td>59</td><td></td><td></td><td>80</td><td>21.21</td><td>80</td><td>21.21</td><td>82</td><td>24.24</td><td>56</td><td>-15.15</td><td>66</td><td>69.5</td></tr><tr><td>EX83</td><td>61</td><td></td><td></td><td>84</td><td>21.74</td><td>84</td><td>21.74</td><td>85</td><td>23.19</td><td>65</td><td>-5.80</td><td>69</td><td>72.9</td></tr><tr><td>EX84</td><td>63</td><td></td><td></td><td>102</td><td>24.39</td><td>102</td><td>24.39</td><td>102</td><td>24.39</td><td>88</td><td>7.32</td><td>82</td><td>85</td></tr><tr><td>EX91</td><td>68</td><td>82</td><td>32.26</td><td>82</td><td>32.26</td><td>82</td><td>32.26</td><td>82</td><td>32.26</td><td>71</td><td>14.52</td><td>62</td><td>66.1</td></tr><tr><td>EX92</td><td>61</td><td>69</td><td>23.21</td><td>69</td><td>23.21</td><td>69</td><td>23.21</td><td>69</td><td>23.21</td><td>45</td><td>-19.64</td><td>56</td><td>60.6</td></tr><tr><td>EX93</td><td>63</td><td>74</td><td>25.42</td><td>74</td><td>25.42</td><td>73</td><td>23.73</td><td>73</td><td>23.73</td><td>54</td><td>-8.47</td><td>59</td><td>60.4</td></tr><tr><td>EX94</td><td>66</td><td>87</td><td>29.85</td><td>89</td><td>32.84</td><td>87</td><td>29.85</td><td>87</td><td>29.85</td><td>71</td><td>5.97</td><td>67</td><td>69.2</td></tr></table>

表 11 所示为 HGIGA 与其他算法在数据集 2 上对比统计, 表 11 中, Same 表示 HGIGA 的结果与该算法相同的算例个数, Better 表示 HGIGA 的结果优于该算法的算例个数, Worse 表示 HGIGA 的结果差于该算法的算例个数, Avg Dev 表示百分比偏差的平均值。

表 11 HGIGA 与其他算法在数据集 2 上对比统计

<table><tr><td rowspan="2"></td><td colspan="3">算例个数</td><td rowspan="2">Avg Dev</td></tr><tr><td>Same</td><td>Better</td><td>Worse</td></tr><tr><td>GA Evolver</td><td>4</td><td>15</td><td>5</td><td>11.66</td></tr><tr><td>BRKGA</td><td>3</td><td>20</td><td>5</td><td>14.42</td></tr><tr><td>DCGA</td><td>5</td><td>18</td><td>5</td><td>12.48</td></tr><tr><td>LAHC</td><td>4</td><td>19</td><td>5</td><td>12.91</td></tr><tr><td>Mult stra GA</td><td>0</td><td>14</td><td>14</td><td>0.61</td></tr></table>

由表 10 与表 11 的结果可以看出, HGIGA 在数据集 2 的 28 个算例上优于其他算法。在部分算例上表现尤其出色。由于数据集 2 整体作业规模较小, 以上算法在小规模算例上都表现出良好的性能。对比之下, HGIGA 与 Mult-stra-GA 在这方面的表现更加突出, 可以有效地探索并找到较小规模问题的最佳解决方案。

图 9 所示为 EX14 通过 HGIGA 求解得到的最优调度甘特图。图 9 中，机器部分矩形代表作业加工过程，车辆部分矩形代表作业运输过程，空白矩形代表车辆空载过程。矩形内第一个数字代表作业编号，括号内数字代表加工时间段。如编号为 5 的矩形代表作业 $J_{5}$ ，先由车辆 $A_{2}$ 从 LU 区域运输至机器 $M_{1}$ 处，进行第一道工序加工，从第 4 min 开始至第 19 min 加工结束；第 19 min 后由 $A_{2}$ 耗费 4 min 运输至 $M_{2}$ ，等待 3 min 后进行第二道工序加工；在第 52 min 由 $A_{1}$ 将 $J_{5}$ 从 $M_{2}$ 运输至 $M_{4}$ 进行最后一道工序加工。

![](images/afca9dc411983039695b0df897539de99b2458bba5434d98eeeb56906a720351.jpg)  
图9EX14通过HGIGA求解得到的最优调度甘特图

车辆 $A_{1}$ 在第 0 min 运输 $J_{4}$ 到 $M_{2}$ ，第 8 min 后空载 20 min 到达 LU 区域，耗费 8 min 将 $J_{1}$ 运输至 $M_{2}$ 处，并在 $M_{2}$ 处停留至第 52 min，后开始运输 $J_{5}$ 至 $M_{4}$ 处加工。

从图 9 看出, EX14 所有作业最后在第 72 min 完成加工, 即最大完工时间为 72 min。可以观察到, 多次出现一个作业连续在一台机器上加工的情况, 减少了运输耗时, 极大提升了作业加工效率。

表 12 所示为算例 EX14 的作业数据, 表 13 所示为数据集 2 布局 4 的 AGV 在不同位置间的运输时间。

表 12 算例 EX14 作业数据

<table><tr><td>作业</td><td>工序</td><td>可用机器</td><td>加工时间/min</td></tr><tr><td rowspan="3"> ${J}_{1}$ </td><td> ${O}_{1,1}$ </td><td> ${M}_{1},{M}_{2},{M}_{4}$ </td><td>8,16,12</td></tr><tr><td> ${O}_{1,2}$ </td><td> ${M}_{2},{M}_{3},{M}_{1}$ </td><td>9,14,13</td></tr><tr><td> ${O}_{1,3}$ </td><td> ${M}_{3},{M}_{4},{M}_{2}$ </td><td>9,17,10</td></tr><tr><td rowspan="3"> ${J}_{2}$ </td><td> ${O}_{2,1}$ </td><td> ${M}_{1},{M}_{3},{M}_{2}$ </td><td>20,10,18</td></tr><tr><td> ${O}_{2,2}$ </td><td> ${M}_{3},{M}_{1},{M}_{4}$ </td><td>18,13,17</td></tr><tr><td> ${O}_{2,3}$ </td><td> ${M}_{2},{M}_{4},{M}_{3}$ </td><td>21,8,19</td></tr><tr><td rowspan="3"> ${J}_{3}$ </td><td> ${O}_{3,1}$ </td><td> ${M}_{3},{M}_{4},{M}_{1}$ </td><td>12,8,15</td></tr><tr><td> ${O}_{3,2}$ </td><td> ${M}_{4},{M}_{2},{M}_{3}$ </td><td>11,10,14</td></tr><tr><td> ${O}_{3,3}$ </td><td> ${M}_{1},{M}_{3},{M}_{2}$ </td><td>11,7,17</td></tr><tr><td rowspan="3"> ${J}_{4}$ </td><td> ${O}_{4,1}$ </td><td> ${M}_{4},{M}_{2}$ </td><td>14,18</td></tr><tr><td> ${O}_{4,2}$ </td><td> ${M}_{1},{M}_{3}$ </td><td>16,16</td></tr><tr><td> ${O}_{4,3}$ </td><td> ${M}_{3},{M}_{1}$ </td><td>16,16</td></tr><tr><td rowspan="3"> ${J}_{5}$ </td><td> ${O}_{5,1}$ </td><td> ${M}_{3},{M}_{1}$ </td><td>10,15</td></tr><tr><td> ${O}_{5,2}$ </td><td> ${M}_{2},{M}_{4}$ </td><td>9,16</td></tr><tr><td> ${O}_{5,3}$ </td><td> ${M}_{4},{M}_{3}$ </td><td>11,14</td></tr></table>

表 13 数据集 2 布局 4 的 AGV 在不同位置间的运输时间 min

<table><tr><td>终点位置\时间\起点位置</td><td>LU</td><td> ${M}_{1}$ </td><td> ${M}_{2}$ </td><td> ${M}_{3}$ </td><td> ${M}_{4}$ </td></tr><tr><td>LU</td><td>0</td><td>4</td><td>8</td><td>10</td><td>14</td></tr><tr><td> ${M}_{1}$ </td><td>18</td><td>0</td><td>4</td><td>6</td><td>10</td></tr><tr><td> ${M}_{2}$ </td><td>20</td><td>14</td><td>0</td><td>8</td><td>6</td></tr><tr><td> ${M}_{3}$ </td><td>12</td><td>8</td><td>6</td><td>0</td><td>6</td></tr><tr><td> ${M}_{4}$ </td><td>14</td><td>14</td><td>12</td><td>6</td><td>0</td></tr></table>

## 4 结语

本文对FJSP-AGV进行研究，为了最大限度地减小最大完工时间，提出了一种基于启发式规则引导遗传算法（HGIGA）。HGIGA从编码、解码方法、种群初始化方法、进化算子和种群多样性保持等方面进行了具体设计。为了证明HGIGA的有效性和效率，在2组基准数据集上进行实验后与其他算法进行了比较。实验结果表明，本文HGIGA在求解FJSP-AGV中小规模算例上有明显优势,效果显著。

在未来的研究中,将考虑 FJSP-AGV 更加细节的研究,比如装卸时间、机器调整时间等。此外还将考虑更多的目标,比如最小化机器负载差和能源消耗。

## 参考文献:

[1] HAM A. Transfer-robot task scheduling in flexible job shop [J]. Journal of Intelligent Manufacturing, 2020, 31(7): 1-11.

[2] YAO Y J, LIU Q H, LI X Y, et al. A novel MILP model for job shop scheduling problem with mobile robots [J]. Robotics and Computer-Integrated Manufacturing, 2023, 81: 102506.

[3] LIM H C, MOON K S. A Two-Phase Iterative Mathematical Programming-Based Heuristic for a Flexible Job Shop Scheduling Problem with Transportation [J]. Applied Sciences, 2023, 13(8): 13085215.

[4] EROL R, SAHIN C, BAYKASOGLU A, et al. A multi-agent based approach to dynamic scheduling of machines and automated guided vehicles in manufacturing systems [J]. Applied Soft Computing Journal, 2012, 12(6): 1720-1732.

[5] 孙爱红, 雷琦, 宋豫川, 等. 基于深度强化学习求解作业车间机器与 AGV 联合调度问题 [J]. 控制与决策, 2024, 39(1): 253-262.

[6] ZHENG Y, XIAO Y, SEO Y. A tabu search algorithm for simultaneous machine/AGV scheduling problem [J]. International Journal of Production Research, 2014, 52(19): 5748-5763.

[7] CHAUDHRY I, RAFIQUE A, ELBADAWI I, et al. Integrated scheduling of machines and Automated Guided Vehicles (AGVs) in flexible job shop environment using genetic algorithms [J]. International Journal of Industrial Engineering Computations, 2022, 13(3): 343-362.

[8] YAN J, LIU Z, ZHANG C, et al. Research on flexible job shop scheduling under finite transportation conditions for digital twin workshop [J]. Robotics and Computer-Integrated Manufacturing, 2021, 72: 102198.

[9] FONTES M M B D, HOMAYOUNI M S. Joint production and transportation scheduling in flexible manufacturing systems [J]. Journal of Global Optimization, 2019, 74(4): 879-908.

[10] HOMAYOUNI M S, FONTES M M B D. Production and transport scheduling in flexible job shop manufacturing systems [J]. Journal of Global Optimization, 2021, 79(2): 463-502.

[11] HAN X, CHENG W, MENG L, et al. A dual population collaborative genetic algorithm for solving flexible job shop scheduling problem with AGV [J]. Swarm and Evolutionary Computation, 2024, 86: 101538.

[12] LI Wenlong, LI Huan, WANG Yuting, et al. Optimizing flexible job shop scheduling with automated guided vehicles using a multi-strategy-driven genetic algorithm [J]. Egyptian Informatics Journal, 2024, 25: 100437.

[13] DEROUSSI L, GOURGAND M, TCHERNEV N. A simple metaheuristic approach to the simultaneous scheduling of machines and automated guided vehicles [J]. International Journal of Production Research, 2007, 46(8): 2143-2164.

[14] KUMAR S V M, JANARDHANA R, RAO P S C. Simultaneous scheduling of machines and vehicles in an FMS environment with alternative routing [J]. The International Journal of Advanced Manufacturing Technology, 2011, 53(1/2/3/4): 339-351.

[15] PAN Z, WANG L, ZHENG J, et al. A learning-based multi-population evolutionary optimization for flexible job shop scheduling problem with finite transportation resources [J]. IEEE Transactions on Evolutionary Computation, 2022, 27(6): 1590-1603.

[16] 陈魁, 毕利, 王文雅. 柔性作业车间 AGV 与机器双资源集成调度研究 [J]. 系统仿真学报, 2022, 34(3): 461-469.

[17] 胡晓阳, 姚锡凡, 黄鹏, 等. 改进迭代局部搜索算法求解多 AGV 柔性作业车间调度问题 [J]. 计算机集成制造系统, 2022, 28(7): 2198-2212.

[18] HOMAYOUNI S M, FONTES D B M M, GONCALVES J F. A multistart biased random key genetic algorithm for the flexible job shop scheduling problem with transportation [J]. International Transactions in Operational Research, 2020, 30(2): 688-716.

[19] FONTES D B M M, HOMAYOUNI S M, GONÇALVES J F. A hybrid particle swarm optimization and simulated ann-

## (上接第83页)

[12] MA Z S, GUO D S. Discrete-time recurrent neural network for solving bound-constrained time-varying underdetermined linear system [J]. IEEE Transactions on Industrial Informatics, 2021, 17(6): 3869-3878.

[13] KONG Y, HU T L, LEI J S, et al. A finite-time convergent neural network for solving time-varying linear equations with inequality constraints applied to redundant manipulator [J]. Neural Processing Letters, 2022, 54(1): 125-144.

[14] LI W B, CHIU P W Y, LI Z. A novel neural approach to infinity-norm joint-velocity minimization of kinematically redundant robots under joint limits [J]. IEEE Transactions on Neural Networks and Learning Systems, 2023, 34(1): 409-420.

[15] LI S, ZHANG Y N, JIN L. Kinematic control of redundant manipulators using neural networks [J]. IEEE Transactions on Neural Networks and Learning Systems, 2017, 28(10): 2243-2254.

[16] ZHANG Y Y, LI S, GUI J, et al. Velocity-level control with compliance to acceleration-level constraints: a novel scheme

ealing algorithm for the job shop scheduling problem with transport resources [J]. European Journal of Operational Research, 2023, 306(3): 1140–1157.

[20] TANG H, WANG J, YANG Z. Research on the Integration and Scheduling of AGVs and Machines in Sample Testing Laboratory [J]. IEEE Access, 2023(11): 70652-70667.

[21] WEN X, FU Y, YANG W, et al. An effective hybrid algorithm for joint scheduling of machines and AGVs in flexible job shop [J]. Measurement and Control, 2023, 56(9/10): 1582-1598.

E-mail: liaoxuechao@wust.edu.cn; 2868307592@qq.com 收稿日期：2024-08-21

[22] DEROUSSI L, NORRE S. Simultaneous scheduling of machines and vehicles for the flexible job shop problem [C] // International conference on metaheuristics and nature inspired computing. Tunisia: Djerba Island, 2010.

[23] HUANG X, YANG L. A hybrid genetic algorithm for multi-objective flexible job shop scheduling problem considering transportation time [J]. International Journal of Intelligent Computing and Cybernetics, 2019, 12(2): 154-174.

作者简介: 廖雪超, 博士, 副教授, 主要研究方向为大数据和计算机应用。
向桂宏, 硕士研究生, 主要研究方向为智能优化调度。
阮兵, 通信作者, 本科, 高级工程师, 主要研究方向为计算机软件及计算机应用、自动化技术。

for manipulator redundancy resolution [J]. IEEE Transactions on Industrial Informatics, 2018, 14(3): 921-930.

[17] BU X, HE G, WEI D. A new prescribed performance control approach for uncertain nonlinear dynamic systems via back-stepping [J]. Journal of the Franklin Institute-Engineering and Applied Mathematics, 2018, 355 (17): 8510-8536.

[18] ZHONG N, LI X, YAN Z, et al. A neural control architecture for joint-drift-free and fault-tolerant redundant robot manipulators [J]. IEEE Access, 2018, 6: 66178-66187.

[19] BORWEIN J, LEWIS A. Convex Analysis [M]. [S.l.]: Springer, 2006.

E-mail: malee83@126.com; didiz82@126.com

收稿日期:2024-06-25