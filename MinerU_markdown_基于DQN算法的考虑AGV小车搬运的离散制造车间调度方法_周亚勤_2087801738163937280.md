DOI: 10.3901/JME.2024.18.338 

# 基于 DQN 算法的考虑 AGV 小车搬运的离散制造 车间调度方法*

周亚勤 $^{1}$ 肖蒙 $^{1}$ 吕志军 $^{1}$ 汪俊亮 $^{2}$ 张洁 $^{2}$ (1. 东华大学机械工程学院 上海 201620;
2. 东华大学人工智能研究院 上海 201620)

摘要：针对离散制造车间生产调度不仅需要确定工件各工序的加工设备及设备上工序的加工顺序，同时要根据工件调度方案，需要在规定时间点前由AGV小车将各工件运送到工序相应的设备上加工，以提高调度方案执行率的需求，构建考虑车间设备布局、工件工艺路线、AGV小车搬运时间与小车位置等约束，工件完工时间最小化和AGV小车运载均衡为综合目标的离散制造车间调度模型。依据离散制造车间调度数学模型构建强化学习环境，包括工件、机器和小车的状态空间，调度决策动作空间和奖励函数；基于建立的强化学习环境，设计基于DQN算法的工件小车调度方法，设计工件智能体，读取车间局部环境，将局部环境映射到工件状态参数的权重，根据该权重得到工件调度列表实现从车间状态到工件调度的动作选择。设计小车智能体，通过读取工件智能体调度决策和车间信息得到小车搬运相关参数，实现小车智能体与工件智能体的交互，将搬运相关参数和车间局部环境中小车状态信息映射成小车调度相关权重，根据权重得到小车调度列表实现小车调度的动作选择。最后，通过离散制造车间实际案例对算法进行测试，测试结果表明，基于DQN算法的调度算法能够有效地求解考虑小车搬运的离散制造车间调度问题，可最小化工件的最大完工时间，均衡小车的搬运负载，具有良好的综合调度性能。关键词：离散制造车间；工件调度；小车调度；DQN算法

# Study on the Discrete Manufacturing Workshop Scheduling Method Based on DQN Algorithm Considering AGV

ZHOU Yaqin $^{1}$ XIAO Meng $^{1}$ LÜ Zhijun $^{1}$ WANG Junliang $^{2}$ ZHANG Jie $^{2}$ (1. College of Mechanical Engineering, Donghua University, Shanghai 201620; 2. Institute of Artificial Intelligence, Donghua University, Shanghai 201620) 

Abstract: For the production scheduling of discrete manufacturing workshops, it is not only necessary to determine the processing machine of each process of the job and the processing sequence of the processes on the machine, but also according to the job scheduling plan, the AGV needs to transport each job to the corresponding machine for processing before the specified time point. In order to improve the execution rate of the scheduling scheme, a discrete manufacturing workshop scheduling model is constructed that considers constraints such as workshop machine layout, job process route, AGV handling time and AGV position, and minimizes job completion time and AGV load balance as comprehensive goals. Build a reinforcement learning environment based on the discrete manufacturing workshop scheduling mathematical model, including the state space of job, machine and car, scheduling decision action space and reward function; based on the established reinforcement learning environment, design a job car scheduling method based on DQN algorithm, and design job agent, read the local environment of the workshop, map the local environment to the weight of the relevant parameters of the job, and obtain the job scheduling list according to the weight to realize the action selection from the workshop state to the job scheduling. Design the AGV agent, and obtain the relevant parameters of the AGV handling by reading the scheduling decision and workshop information of the job agent, and realize the interaction between the AGV agent and the job agent. The handling related parameters and the car status information in the local environment of the workshop are mapped into the relevant weights of the car scheduling, and the car scheduling list is obtained according to the weights to realize the action selection of the car scheduling. Finally, the algorithm is tested through the actual case of discrete manufacturing workshop. The test results show that the scheduling algorithm based on the DQN algorithm can effectively solve the discrete manufacturing workshop scheduling problem considering the handling of AGVs, minimize the maximum completion time of job, and balance the handling of AGVs load. 

Key words: discrete manufacturing shop; job scheduling; AGV scheduling; DQN algorithm 

## 0 前言

随着快速发展的生产技术和复杂变化的产品需求，离散制造企业生产模式呈现出多种类、小规模离散制造生产模式[1]。这使得离散制造车间工件种类增多，生产过程复杂多变，包含更多的变化和不确定因素。离散制造车间生产过程存在如下特点：①工艺柔性，随着车间设备数字化和智能化水平的提高，工件工艺路线更加柔性化，每道工序可有多台加工设备备选，增加了车间资源调度的复杂性；②生产状态可实时监控，随着车间智能传感设备的使用，车间工件和设备的生产状态可实时监控，采集的生产过程数据可为工件工序设备资源的选择提供参考；③集成物料配送系统，随着智能物流系统的发展，离散制造车间生产过程中，需要配送AGV小车穿梭于不同加工区域之间以完成工件在不同设备间的搬运，保障工件任务能够按照生产调度方案规定的加工顺序和时间在相应的设备上完成加工。这些特点确定了离散制造车间生产能力的提高需要由各种加工资源配置的合理性决定[2]，需要对车间的设备和AGV小车资源进行合理的协同调度，以实现工件完工时间最小化和车间资源均衡利用的综合目标，对提高制造车间生产调度方案的执行率，保证产品交货期和提高制造系统整体性能，具有一定理论意义和工程应用价值[3]。

针对离散制造车间调度优化问题求解方法有传统智能算法，如遗传算法 $^{[4]}$ 、蚁群算法 $^{[5]}$ 、粒子群算法 $^{[6]}$ 等；随着人工智能技术的发展，人工智能算法求解调度优化问题也正在扩大应用。曾创锋等 $^{[7]}$ 提出了一种混合整数规划，结合了遗传变异操作，加强了算法的局部搜索能力，但是单一优化目标在实际生产中存在缺陷。李雯璐等 $^{[8]}$ 提出了一种多目标灰狼算法，以减少完工时间和能源消耗为目标，但是求解较为困难。谢志强等 $^{[9]}$ 提出了一种基于遗传算法和分支定界的混合调度算法，能够协调调度多车间产能。郑重 $^{[10]}$ 为了提升AGV周转率等采用了预调度、重进重出等措施，优化了 AGV 的相关指标。郭沛佩等 $^{[11]}$ 通过确定调度规则与 AGV 数量进行匹配，确定了最佳匹配数量，但应用范围小，存在一定局限性。近年来，因强化学习具有自适应能力，正被应用于求解许多有挑战性的决策问题 $^{[12-13]}$ 。使用强化学习算法求解调度问题也正被广泛研究 $^{[14]}$ 。调度问题可以转化为一个马尔可夫决策过程(Markov decision process, MDP)，其中状态 s 描述了离散制造车间中的状态，调度智能体(Agent)观测车间状态 s，采用调度决策 a，并接受车间环境由调度决策产生的奖励 r，车间环境更新到状态 $s'$ ，智能体再观测状态采取决策。通过这样与车间的交互，产生大量的调度经验，采用数据驱动的方法学习，最大化环境所提供的奖励的同时优化调度的决策 $^{[15-16]}$ 。WANG 等 $^{[17]}$ 设计了一种分层强化学习模型，提高了大型复杂制造系统的交货期准时率。贺俊杰等 $^{[18]}$ 以加权完工时间和为目标，设计了一种在线调度方法，但是其工件和机器种类单一，不适应离散制造车间调度。LUO $^{[19]}$ 利用深度双 Q 网络研究了柔性车间调度问题，提出了六种复合调度规则，能解决一定的工件小车调度问题，无法直接指定工件与小车配对。YANG 等 $^{[20]}$ 利用 DQN 与 DDQN 算法研究了动态置换流水调度问题，与元启发式规则对比，验证了算法的有效性，但是模型未考虑 AGV 小车的搬运。

为解决离散制造车间生产设备和 AGV 小车资源的合理配置与协同调度问题，提高车间生产调度方案执行率，本文基于离散制造车间生产实际需求分析，构建考虑车间设备布局、工件工艺路线、AGV 小车搬运时间与小车位置等约束的离散制造车间调度数学模型；设计基于 DQN 算法的工件小车调度方法，构建包括工件、机器和小车的状态空间，调度决策动作空间和奖励函数的强化学习环境，设计工件智能体与小车智能体，交互实现对工件小车的调度，完成对工件各工序设备的选择、搬运小车的选择及优化排序，从而达到工件的总完工时间最短和小车搬运均衡的目标。

## 1 问题描述

## 1.1 离散制造车间工件小车调度描述

考虑搬运小车的离散制造车间调度问题可以描述如下：车间中有 a 个工件，b 台机器，c 台搬运 AGV 小车。每个工件有多道加工工序，每道工序可在确定的多台可选机器上加工，并且相应的加工时间已经确定，由搬运小车将已完成某道工序的工件搬运至下道工序机器继续进行加工，所有工序加工完成后在机器的缓冲区等待，通过为工件各工序选择加工机器及搬运小车，并对机器上的工件加工顺序及小车搬运任务顺序进行优化排序，使得工件的总完工时间最小，并满足搬运小车负载均衡的目标。

工件小车调度案例约束如表1所示，工件工序在不同机器上加工时间不一致，小车需要在各机器之间对工件进行搬运，其时间如表2所示。通过调度算法为工件各工序选择加工机器与搬运小车，并确定机器上工件加工与小车搬运的顺序和起始结束时间，从而确定工件小车的调度方案，甘特图如图1所示，图中横坐标为单位时间，纵坐标为机器名称。其中工件 $J_{0}$ 三道工序分别在机器 $M_{1}$ 和机器 $M_{2}$ 上进行加工，由AGV0小车进行搬运；工件 $J_{1}$ 三道工序分别在机器 $M_{3}$ 和机器 $M_{4}$ 上进行加工，由AGV1小车进行搬运；工件 $J_{2}$ 两道工序分别在机器 $M_{3}$ 和机器 $M_{5}$ 上进行加工，由AGV1小车进行搬运。


表 1 工件各工序加工设备及时间


<table><tr><td rowspan="2">工件</td><td rowspan="2">工序</td><td colspan="5">在各设备上加工时间</td></tr><tr><td><eq>{M}_{1}</eq></td><td><eq>{M}_{2}</eq></td><td><eq>{M}_{3}</eq></td><td><eq>{M}_{4}</eq></td><td><eq>{M}_{5}</eq></td></tr><tr><td rowspan="3"><eq>{J}_{0}</eq></td><td><eq>{O}_{11}</eq></td><td>12</td><td>18</td><td>—</td><td>18</td><td>—</td></tr><tr><td><eq>{O}_{12}</eq></td><td>—</td><td>8</td><td>6</td><td>20</td><td>20</td></tr><tr><td><eq>{O}_{13}</eq></td><td>—</td><td>8</td><td>—</td><td>—</td><td>18</td></tr><tr><td rowspan="3"><eq>{J}_{1}</eq></td><td><eq>{O}_{21}</eq></td><td>18</td><td>—</td><td>8</td><td>20</td><td>14</td></tr><tr><td><eq>{O}_{22}</eq></td><td>—</td><td>18</td><td>12</td><td>9</td><td>—</td></tr><tr><td><eq>{O}_{23}</eq></td><td>7</td><td>—</td><td>20</td><td>12</td><td>18</td></tr><tr><td rowspan="2"><eq>{J}_{2}</eq></td><td><eq>{O}_{31}</eq></td><td>18</td><td>20</td><td>8</td><td>7</td><td>6</td></tr><tr><td><eq>{O}_{32}</eq></td><td>—</td><td>7</td><td>8</td><td>—</td><td>20</td></tr></table>


表 2 小车在机器间的搬运时间


<table><tr><td>搬运时间</td><td><eq>{M}_{1}</eq></td><td><eq>{M}_{2}</eq></td><td><eq>{M}_{3}</eq></td><td><eq>{M}_{4}</eq></td><td><eq>{M}_{5}</eq></td></tr><tr><td><eq>{M}_{1}</eq></td><td>0</td><td>2</td><td>4</td><td>6</td><td>8</td></tr><tr><td><eq>{M}_{2}</eq></td><td>2</td><td>0</td><td>2</td><td>4</td><td>6</td></tr><tr><td><eq>{M}_{3}</eq></td><td>4</td><td>2</td><td>0</td><td>2</td><td>4</td></tr><tr><td><eq>{M}_{4}</eq></td><td>6</td><td>4</td><td>2</td><td>0</td><td>2</td></tr><tr><td><eq>{M}_{5}</eq></td><td>8</td><td>6</td><td>4</td><td>2</td><td>0</td></tr></table>

![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-13/30ad0010-55e3-43e0-81ea-cef724f48fff/2eb8a9fbaf73e3b46a519f19aab9e1b42854dba823fc1e092a4b18a4c84fa206.jpg)



图1 案例甘特图


## 1.2 数学模型

建立离散制造车间工件小车调度的数学模型需要满足以下基本假设。

(1) 同一工件各工序的加工顺序固定，不同工件的工序加工顺序互不影响。

(2) 每个工件的每道工序只能选择在一台机器上完成加工，加工开始之后不允许中断。

(3) 每台机器一次只能加工一个工件。

(4) 每台小车一次只能运送一个工件，小车行驶速度稳定不变，小车动力充足且不考虑故障。

(5) 小车结束当前搬运任务后从当前位置可以立刻开始进行下一任务，无需空闲等待时间。

(6) 工件被小车搬运时的移动时间及加工开始前的准备时间等辅助时间都被计算在加工时间之内。

(7) 所有机器和小车在零时刻都是可用的。

(8) 所有机器的缓冲区足够大，待加工工件可以提前送到。

为描述离散制造车间工件小车调度过程中的相关参数，建立符号表如表 3 所示。

基于数学模型中的假设与相关符号定义，给出调度目标函数如下

$$
\begin{array}{l} f _ {1} = \min \left(\max _ {1 \leqslant i \leqslant a} (J E T _ {i N J _ {i}})\right) \\ f _ {2} = \min \sqrt {\frac {\sum_ {v = 1} ^ {c} \left(| A M i s s _ {v} | - \frac {\sum_ {v = 1} ^ {c} | A M i s s _ {v} |}{c}\right) ^ {2}}{c}} \end{array}\tag{1}
$$

(2) 

并满足如下约束条件

$$
\sum_ {j = 1} ^ {b} a _ {i n j} = 1\tag{3}
$$

$$
\sum_ {v = 1} ^ {c} b _ {i n v} = 1\tag{4}
$$

$$
P S T _ {i n} = \sum_ {v = 1} ^ {c} \max (J E T _ {i n}, A E T _ {v} + T T _ {J L o _ {i n} A E L o _ {v}})\tag{5}
$$


表 3 数学模型符号表


<table><tr><td>符号</td><td>含义</td></tr><tr><td><eq>J = \{ {J}_{1},{J}_{2},\cdots ,{J}_{i},\cdots ,{J}_{a}\}</eq></td><td>工件集合,其中 <eq>{J}_{i}</eq> 为第 <eq>i</eq> 号工件</td></tr><tr><td><eq>M = \{ {M}_{1},{M}_{2},\cdots ,{M}_{j},\cdots ,{M}_{b}\}</eq></td><td>机器集合,其中 <eq>{M}_{j}</eq> 为第 <eq>j</eq> 台机器</td></tr><tr><td><eq>V = \{ {V}_{1},{V}_{2},\cdots ,{V}_{v},\cdots ,{V}_{c}\}</eq></td><td>小车集合,其中 <eq>{V}_{v}</eq> 为第 <eq>v</eq> 台小车</td></tr><tr><td><eq>{T}_{in} = \{ {T}_{in1},\cdots ,{T}_{inj},\cdots ,{T}_{inb}\}</eq></td><td>工件工序加工时间集合,<eq>{T}_{inj}</eq> 表示工件 <eq>{J}_{i}</eq> 的第 <eq>n</eq> 道工序在对应机器 <eq>j</eq> 上的加工时间,当不能在某一机器上加工时,<eq>{T}_{inj}</eq> 取正极大值</td></tr><tr><td><eq>N{J}_{i}</eq></td><td>工件 <eq>{J}_{i}</eq> 的工序数量</td></tr><tr><td><eq>{O}_{in}</eq></td><td>工件 <eq>{J}_{i}</eq> 的第 <eq>n</eq> 道工序</td></tr><tr><td><eq>JL{o}_{in}</eq></td><td>工件 <eq>{J}_{i}</eq> 的第 <eq>n</eq> 道工序当前所在位置</td></tr><tr><td><eq>F{O}_{i}</eq></td><td>工件 <eq>{J}_{i}</eq> 已完成的工序数</td></tr><tr><td><eq>{JST}_{in}</eq></td><td>工件 <eq>{J}_{i}</eq> 的第 <eq>n</eq> 道工序在机器上开始加工的时间</td></tr><tr><td><eq>{JET}_{in}</eq></td><td>工件 <eq>{J}_{i}</eq> 的第 <eq>n</eq> 道工序在机器上结束加工的时间</td></tr><tr><td><eq>{PST}_{in}</eq></td><td>工件 <eq>{J}_{i}</eq> 的第 <eq>n</eq> 道工序开始被小车搬运的时间</td></tr><tr><td><eq>{PET}_{in}</eq></td><td>工件 <eq>{J}_{i}</eq> 的第 <eq>n</eq> 道工序结束被小车搬运的时间</td></tr><tr><td><eq>{MST}_{j}</eq></td><td>机器 <eq>{M}_{j}</eq> 开始当前加工的时间</td></tr><tr><td><eq>{MET}_{j}</eq></td><td>机器 <eq>{M}_{j}</eq> 结束当前加工的时间</td></tr><tr><td><eq>MLo_{j}</eq></td><td>机器 <eq>{M}_{j}</eq> 在车间中所处的位置</td></tr><tr><td><eq>ASL{o}_{v}</eq></td><td>小车 <eq>{V}_{v}</eq> 下一搬运任务的开始位置</td></tr><tr><td><eq>AELO_{v}</eq></td><td>小车 <eq>{V}_{v}</eq> 下一搬运任务的结束位置</td></tr><tr><td><eq>AST_{v}</eq></td><td>小车 <eq>{V}_{v}</eq> 当前搬运任务的开始时间</td></tr><tr><td><eq>AET_{v}</eq></td><td>小车 <eq>{V}_{v}</eq> 当前搬运任务的结束时间</td></tr><tr><td><eq>AMiss_{v}</eq></td><td>小车 <eq>{V}_{v}</eq> 的搬运任务序列</td></tr><tr><td><eq>TT_{xy}</eq></td><td>小车从车间中的 <eq>x</eq> 位置到 <eq>y</eq> 位置所需要花费的时间</td></tr><tr><td><eq>{a}_{inj}</eq></td><td>如果工序 <eq>{O}_{in}</eq> 在机器 <eq>{M}_{j}</eq> 上加工,则等于 1,否则等于 0</td></tr><tr><td><eq>{b}_{inv}</eq></td><td>如果如果工序 <eq>{O}_{in}</eq> 的搬运任务由小车 <eq>{V}_{v}</eq> 搬运,则等于 1,否则等于 0</td></tr></table>

$$
P E T _ {i n} = P S T _ {i n} + T T _ {J L o _ {i n} J L o _ {i (n + 1)}}\tag{6}
$$

$$
J E T _ {i n} = \sum_ {j = 1} ^ {b} (J S T _ {i n} + T _ {i n j}) \times a _ {i n j}\tag{7}
$$

$$
J S T _ {i n} = \sum_ {j = 1} ^ {b} \left(P E T _ {i (n - 1)}, M E T _ {j}\right) \times a _ {i n j}\tag{8}
$$

$$
M S T _ {j} = \sum_ {j = 1} ^ {b} J S T _ {i n} \times a _ {i n j}\tag{9}
$$

$$
M E T _ {j} = \sum_ {j = 1} ^ {b} J E T _ {i n} \times a _ {i n j}\tag{10}
$$

$$
A E T _ {v} = \sum_ {v = 1} ^ {C} P E T _ {i n} \times b _ {i n v}\tag{11}
$$

$$
A S T _ {v} = \sum_ {v = 1} ^ {C} P S T _ {i n} \times b _ {i n v}\tag{12}
$$

$$
J L o _ {i n} = \sum_ {j = 1} ^ {b} M L o _ {j} \times a _ {i n j}\tag{13}
$$

$$
A E l o _ {v} = \sum_ {v = 1} ^ {C} J L o _ {i (n + 1)} \times b _ {i n v}\tag{14}
$$

$$
A S l o _ {v} = \sum_ {v = 1} ^ {C} J L o _ {i n} \times b _ {i n v}
$$

$$
A M i s s _ {v} = \sum_ {i = 1} ^ {a} \sum_ {n = 1} ^ {N J _ {i}} b _ {i n v}\tag{15}
$$

(16) 

式(1)表示模型以最大完工时间最小为目标；式(2)表示模型考虑小车运送工件任务数量均衡为目标，小车运送任务数量均衡可减少工件等待时间，促进实现最大完工时间最小的目标；式(3)表示工件的每道工序仅可选择在一台机器上进行加工；式(4)说明工件在搬运过程中仅可以被一辆搬运小车进行搬运；式(5)说明在工件加工完成后，工件需要等待小车前往所在位置方可进行搬运；式(6)说明工件被搬运过程中路径是连续的；式(7)和式(10)说明工件的加工是连续的；式(8)和式(9)说明了工件需要到达加工机器并等待机器完成当前加工任务后才开始进行加工；式(11)和式(12)说明工件在搬运至小车上的过程和其他辅助过程所用的时间计入加工时间中；式(13)表达了工件当前工序在加工时位于车间中的位置；式(14)说明了小车所搬运任务的目标机器；式(15)说明小车运送工件时需要先前往工件当前完成工序所在机器处；式(16)表达了小车的负载情况。

在Gurobi上针对上述调度问题数学模型进行建模，并利用小规模实例对模型的正确性进行了验证，验证结果如图2所示。

```txt
Cutting planes:
Gomory: 74
Cover: 1
Implied bound: 179
Projected implied bound: 2
MIR: 56
StrongCG: 1
Flow cover: 176
GUB cover: 3
Zero half: 2
RLT: 18
Relax-and-lift: 9

Explored 3777 nodes (469401 simplex iterations) in 13.76 seconds (10.40 work units)
Thread count was 8 (of 8 available processors)

Solution count 6: 30 32 44 ... 50

Optimal solution found (tolerance 1.00e-04)
Best objective 3.000000000000e+01, best bound 3.000000000000e+01, gap 0.0000% 
```


图2 Gurobi验证结果


## 2 基于DQN算法的调度方法

## 2.1 强化学习环境

在基于强化学习的离散制造车间调度中，智能体与车间环境进行交互，感知车间的状态变化进行各种调度决策，并获得车间提供的奖励，智能体通过不断试错以获取更高的奖励，同时实现其调度决策的优化。基于强化学习的离散制造车间调度交互流程如图 3 所示。由构建的调度数学模型确定离散制造车间的状态空间、动作空间以及奖励函数设计如下。

![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-13/30ad0010-55e3-43e0-81ea-cef724f48fff/bc18839cd4cfa0805dd7122db7e5d66ae7f67ad62e534222c82165df1ac5c429.jpg)



图3 离散制造车间环境与智能体交互框架


## 2.1.1 状态空间

离散制造车间调度信息的主要维度包括工件、机器和小车三个对象，因此设计车间调度强化学习环境状态空间 $S = (S_{1}, S_{2}, S_{3})$ ，对离散制造车间的状态进行描述。其中 $S_{1} = (S_{1,1}, S_{1,2}, S_{1,3}, S_{1,4}, S_{1,5})$ 为工件相关的状态信息； $S_{2} = (S_{2,1}, S_{2,2}, S_{2,3})$ 为机器相关的状态信息； $S_{3} = (S_{3,1}, S_{3,2}, S_{3,3}, S_{3,4})$ 小车相关的状态信息；工件、机器和小车三种状态中的具体含义见表4。


表 4 离散制造车间状态参数表


<table><tr><td>参数</td><td>状态表达式</td><td>含义</td></tr><tr><td rowspan="5">工件</td><td><eq>S_{1,1}</eq></td><td>工件当前工序完工时间</td></tr><tr><td><eq>S_{1,2}</eq></td><td>工件当前工序所在机器</td></tr><tr><td><eq>S_{1,3}</eq></td><td>工件已加工工序数</td></tr><tr><td><eq>S_{1,4}</eq></td><td>工件剩余加工工序数</td></tr><tr><td><eq>S_{1,5}</eq></td><td>工件剩余工序加工时间</td></tr><tr><td rowspan="3">机器</td><td><eq>S_{2,1}</eq></td><td>机器已加工时间</td></tr><tr><td><eq>S_{2,2}</eq></td><td>机器累计加工工序次数</td></tr><tr><td><eq>S_{2,3}</eq></td><td>机器所在位置</td></tr><tr><td rowspan="4">小车</td><td><eq>S_{3,1}</eq></td><td>小车上一任务完工时间</td></tr><tr><td><eq>S_{3,2}</eq></td><td>小车当前所在位置</td></tr><tr><td><eq>S_{3,3}</eq></td><td>小车当前任务开始时间</td></tr><tr><td><eq>S_{3,4}</eq></td><td>小车累计搬运次数</td></tr></table>

## 2.1.2 动作空间

离散制造车间动作空间是指在不同的车间状态下所有可执行的调度决策集合，主要包括工件的加工和小车的搬运工件，因此设计离散制造车间调度强化学习动作空间 $A = (A_{1}, A_{2})$ ，对离散制造车间调度问题中所有可执行的动作进行描述，包括工件调度决策空间 $A_{1}$ 和小车调度决策空间 $A_{2}$ 。

(1) 工件调度决策空间：由数学模型已知车间中共有 a 个工件，工件调度决策将选中某一个工件进行下一工序的加工安排。当某一工件完成所有工序加工任务后，将该工件从工件调度决策空间中去除。工件调度决策空间定义为 $A_{1}=\{J_{1},\cdots,J_{i},\cdots,J_{a}\}$ 。

(2) 小车调度决策空间：由数学模型已知车间中共有 c 台小车，小车调度决策将选中某一小车，由该小车对选中的工件进行搬运。小车调度决策空间定义为 $A_{2}=\{V_{1},\cdots,V_{v},\cdots,V_{c}\}$ 。

## 2.1.3 奖励函数

奖励函数是环境对智能体采取动作的评价规则，是智能体进行学习、改善自身决策的重要指引信号。根据数学模型中的目标函数设计离散制造车间调度奖励函数。将目标函数按照调度结果和调度过程进行分解，实现对智能体的分步奖励，同时在完成全部加工任务时对智能体进行最终奖励。设计离散制造车间调度奖励函数 $R=(Rf, Rs)$ ，其中，Rf为最终奖励集合，Rs为分步奖励集合，分别设计如式(17)～(22)所示，公式中，i为工件调度智能体所做出的决策，v为小车调度智能体所做出的决策。

分步奖励 $R_{s} = \{r s_{1}, r s_{2}, r s_{3}\}$ 

$$
r s _ {1} = \frac {3}{T T _ {A E L o _ {v} J L o _ {i}} + 1}\tag{17}
$$

$$
r s _ {2} = \frac {3}{P S T _ {i F O _ {i}} - A E T _ {v} + 1}\tag{18}
$$

$$
r s _ {3} = \frac {3}{J S T _ {i F O _ {(i + 1)}} - A E T _ {v} + 1}\tag{19}
$$

最终奖励 $Rf = \{rf_{1},rf_{2}\}$ 

$$
r f _ {1} = \frac {2 0}{\ln (\max _ {1 \leqslant k \leqslant a} J E T _ {k N k})}\tag{20}
$$

$$
r f _ {2} = \frac {2 0}{\operatorname{var} (A m i s s) + 1}\tag{21}
$$

$$
\operatorname{var} (A M i s s) = \sqrt {\frac {\sum_ {v = 1} ^ {c} \left(| A M i s s _ {v} | - \frac {\sum_ {v = 1} ^ {c} | A M i s s _ {v} |}{c}\right) ^ {2}}{c}}\tag{22}
$$

为减少小车完成上一搬运任务后前往接收工件所需的行走距离，设计与小车行走距离呈反比的分步奖励函数，如式(17)所示，当小车完成当前任务的位置和将要前往的工件位置之间的距离越远，所得到的 $rs_{1}$ 奖励越少，以促进选择小车的决策使得小车的行走距离更小；为减少工件加工完成后在机器输出缓冲区的等待时间，设计与工件加工完成后等待小车搬运时间呈反比的分步奖励函数，如式(18)

所示，当工件开始搬运时间和小车达到时间之差越大，所得到的 $rs_2$ 奖励越少，以促进选择小车和工件的决策使得工件等待小车的时间更小；为减少工件在搬运完成后在机器输入缓冲区的等待时间，设计与工件在机器上的等待时间呈反比的分步奖励函数，如式(19)所示，当工件到达加工机器的时间和工件开始加工的时间之差越大，所得到的 $rs_3$ 奖励越少，使得工件选择合适的机器进行下一工序的加工；为减少车间中工件的最大完工时间，设计与车间最大完工时间呈反比的最终奖励函数，如式(20)所示，当车间中工件的最大完工时间越大，所得到的 $rf_1$ 奖励越少，以促进调整调度整体决策使得减少最大完工时间；为平衡小车搬运任务数量，设计与小车搬运任务数方差呈反比的最终奖励函数，如式(21)所示，当小车搬运任务数量越均衡，所得到的 $rf_2$ 奖励越大，以促进调整选择小车决策使得平衡小车搬运的任务数量，小车搬运任务数方差计算方法如式(22)所示。

## 2.2 基于DQN算法的调度流程

基于DQN算法的调度流程如图4所示。

![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-13/30ad0010-55e3-43e0-81ea-cef724f48fff/ab7d181cb0056aff8d8c2b35b9fc45d9595f2abee76ffa073e12f529888ff914.jpg)



图4 基于DQN算法的调度流程


(1) 初始化离散制造车间调度环境。

(2) 初始化工件调度智能体和小车调度智能体。

(3) 工件调度智能体读取离散制造车间的状态信息。

(4) 工件调度智能体通过神经网络将车间状态信息映射成为工件调度的决策,执行该工件的调度,包括工件工序的机器选择和加工顺序。

(5) 执行工件调度的决策后，车间部分环境状态信息发生改变。

(6) 小车调度智能体读取离散制造车间状态信息。

(7) 小车调度智能体通过神经网络将已更新的车间状态信息映射成为小车调度决策，执行该小车的调度。

(8) 小车对工件进行搬运，工件进行下一工序的加工。改变车间的状态。

(9) 判断全部工件是否加工完成，如果加工完成则结束。如果存在工件尚未加工完成，则跳转至步骤(3)。

## 2.3 DQN算法的学习过程

初始化工件调度智能体和小车调度智能体实质是初始化智能体自身的网络参数，而网络参数需要从离散制造车间工件小车调度经验中进行学习而得到。DQN算法的学习过程如图5所示。

![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-13/30ad0010-55e3-43e0-81ea-cef724f48fff/f5024a381087ca6161c2211c06af5f1bfbac780ad88f41bca45632b6afa7e2e6.jpg)



图5 DQN算法的学习过程


调度智能体具有一个评价网络和一个目标网络，两个网络的结构一致，但初始的网络参数不同。调度智能体同时具有一个经验池，用于存储离散制造车间调度决策前后的车间状态信息、具体决策信息和奖励信息。从经验池中抽取一批状态信息给目标网络和评价网络，两个网络根据信息做出不同的决策，评价网络根据两个决策进行策略迭代的过程如式(23)所示，两个决策之间的差异构成损失值如式(24)所示，通过神经网络优化器优化这一损失值以训练评价网络的网络参数。每经过一定的间隔，将评价网络的网络参数同步到目标网络中。通过这一方法不断的进行学习，损失值降低到一定程度后学习阶段完成，应用评价网络的网络参数为离散制造车间工件小车调度提供决策。

$$
\begin{array}{c} Q (s _ {t}, a _ {t}; \theta_ {t}) \leftarrow Q (s _ {t}, a _ {t}; \theta_ {t}) + \\ \alpha [ r _ {t} + \gamma \max Q (s _ {t + 1}, a _ {t + 1}; \theta^ {-}) - Q (s _ {t}, a _ {t}; \theta_ {t}) ] \end{array}\tag{23}
$$

式中， $Q(s_{t}, a_{t}; \theta_{t})$ 为离散制造车间状态 $s_{t}$ 经过评价网络后得到的动作 $a_{t}$ 的 Q 值， $\theta_{t}$ 是评价网络的网络参数， $\alpha$ 为学习率， $\gamma$ 为衰减系数， $\theta^{-}$ 为目标网络(Target network)的网络参数。

$$
L o s s (\theta_ {t}) = T ^ {2}\tag{24}
$$

式中， $T$ 为时间差分的偏差值，如式(25)所示

$$
T = r _ {t} + \gamma \max Q (s _ {t + 1}, a _ {t + 1}; \theta^ {-}) - Q (s _ {t}, a _ {t}; \theta_ {t})\tag{25}
$$

## 2.4 智能体的状态、奖励、动作空间

在考虑 AGV 小车搬运的离散制造车间调度中，工件在工序加工设备间的中转需要由 AGV 小车进行搬运，工件调度决策和小车调度决策不能单独进行，需要进行协同考虑。工件调度智能体做出工件调度的决策后，将向小车调度智能体提供工件的当前位置、工件下一工序所在机器位置和工件当前工序完工时间等信息，辅助小车调度智能体做出决策。只有小车调度决策做出后，小车在完成当前自身任务的基础上才能对当前所决策的工件进行搬运。所以，工件调度智能体的可观测的状态空间为离散制造车间本身的状态空间 JS=S，而小车调度智能体的可观测状态空间为离散制造车间本身状态空间与工件调度智能体所提供的状态信息 $AS=(S, JLo_{in}, JLo_{i(n+1)}, JET_{in})$ 。两个智能体可获得的奖励部分不同，其中工件调度智能体可获得的奖励为 $JR=(rs_{2}, rs_{3}, rf_{1})$ ，小车调度智能体可获得的奖励为 $AR=(rs_{1}, rs_{2}, rf_{2})$ 。离散制造车间强化学学习环境的动作空间包含了所有的可执行动作，工件和小车调度智能体分别执行其中部分动作。其中，工件调度智能体的可执行动作空间为 $JA=A_{1}$ ，小车调度智能体的可执行动作空间为 $AA=A_{2}$ 。在不同的离散制造车间内，其工件和小车调度智能体的动作空间维度不一致，无法直接采用工件号与小车号对动作空间进行输出。工件调度智能体将根据读取的车间状态输出五个参数，分别为工件五个状态参数的权重，同时将工件的五个状态参数：工件当前工序完工时间、工件当前工序所在机器、工件的已加工工序数、工件剩余工序、工件剩余加工时间进行归一化并加权求和，得到工件工序的机器选择和调度列表。同理，小车调度智能体将根据小车当前搬运结束时间、小车从当前完工后的位置到工件处距离、小车搬运次数等得到小车调度列表。智能体根据 $\varepsilon$ -greedy 选择策略，如式(26)所示，当随机概率 p 小于 $\varepsilon$ (取 0.1) 时，输出随机的动作决策，大于 $\varepsilon$ 时，输出调度列表中排第一的动作决策。

$$
\varepsilon - \text { greedy } = \left\{ \begin{array}{l l} \text { random   action } & p <   \varepsilon \\ \text { list.index(1) } & p \geqslant \varepsilon \end{array} \right.\tag{26}
$$

## 3 案例测试与分析

在 Windows 10，i5-6300HQ CPU @2.39GHz，GTX 950M，内存 8G 的试验环境下进行案例测试。

## 3.1 案例对比

采用文献[21]试验部分的柔性离散制造车间调度案例，案例存在3台小车、4个工件，工件加工需要由小车从装载站搬运至首道工序的加工机器，工件结束所有加工后需要小车搬运回卸载站，工件在9台机器上加工，且工件加工的工序数不相同。采用该案例对本文提出的基于DQN算法的考虑AGV小车搬运的离散车间调度方法进行测试。文献[21]中所提出的算法在同样的试验条件下求解得到的最大完工时间为67，而利用本文提出的算法求解测试案例，得到最大完工时间为65，加工过程中所有工件一共需要被搬运16次，3辆小车搬运次数分别为6次、5次、5次，小车搬运负载均衡度最高，其中工件在加工前的小车搬运时间为小车从装载站搬运工件至加工机器的时间，工件加工后的小车搬运时间为工件加工完成后搬运至卸载站的时间。通过对比验证本算法相较于文献算法更优。利用所提出的算法求解的调度方案甘特图如图6所示。

![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-13/30ad0010-55e3-43e0-81ea-cef724f48fff/4bae4ad672d9ee1100b8d781abe1f96622c32ba460d3fbb2702d4cf9040c4f5c.jpg)



图6 本文算法测试文献[21]案例的甘特图


## 3.2 基准案例测试对比

BILGE等[22]针对存在搬运AGV小车的条件下设计了81个柔性作业车间调度案例，本文算法选取其中4个调度案例进行试验验证，与文献[22-25]中的其他算法进行对比，其结果如表5所示，本文算法均能获得案例的优化解，其中，本文所提出的算法应用于Ex21案例时优于其他算法，其甘特图如图7所示。


表 5 算法对比


<table><tr><td>案例</td><td><eq>{\mathrm{{STW}}}^{\left\lbrack {22}\right\rbrack }</eq></td><td><eq>{\mathrm{{AGA}}}^{\left\lbrack {23}\right\rbrack }</eq></td><td><eq>{\mathrm{{FDE}}}^{\left\lbrack {24}\right\rbrack }</eq></td><td><eq>{\mathrm{{FMAS}}}^{\left\lbrack {25}\right\rbrack }</eq></td><td>本文算法</td></tr><tr><td>Ex11</td><td>96</td><td>96</td><td>96</td><td>111</td><td>96</td></tr><tr><td>Ex13</td><td>84</td><td>84</td><td>84</td><td>91</td><td>84</td></tr><tr><td>Ex21</td><td>105</td><td>102</td><td>105</td><td>128</td><td>100</td></tr><tr><td>Ex23</td><td>86</td><td>86</td><td>86</td><td>102</td><td>86</td></tr></table>

![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-13/30ad0010-55e3-43e0-81ea-cef724f48fff/9df77e10e09b138b7ce41a1d1a7136884812f40fa991eacf516f3274ab0107e3.jpg)



图7Ex21调度甘特图


## 3.3 实际车间案例测试

针对某离散制造车间实际生产的原始数据，经过整理后，得到8个工件的工序加工工艺信息，如表6所示，包括工件各个工序的名称和加工时间，其中还存在钳、热处理、表面处理和检验工序等非机加工工序。车间中存在四个机器组，分别为数车组、普车组、镗床组和数铣组。表7给出了各个机器(1～8分别对应8台机器)、非机加工位置(9～12分别对应钳、热处理、表面处理和检验等非机加工工序所在位置)之间搬运小车行走所需的时间。车间中8台机器分别对应到相应的设备组，如表8所示。表8同时给出了机加工工序名称和机器组之间的对应关系。


表 6 工件工序信息


<table><tr><td rowspan="2">工件</td><td colspan="2">工序1</td><td colspan="2">工序2</td><td colspan="2">工序3</td><td colspan="2">工序4</td><td colspan="2">工序5</td><td colspan="2">工序6</td></tr><tr><td>名称</td><td>时间</td><td>名称</td><td>时间</td><td>名称</td><td>时间</td><td>名称</td><td>时间</td><td>名称</td><td>时间</td><td>名称</td><td>时间</td></tr><tr><td><eq>J_0</eq></td><td>数控立车</td><td>8</td><td>车端面</td><td>5</td><td>镗孔</td><td>1</td><td>车槽</td><td>6</td><td>钳</td><td>3</td><td>铣平面</td><td>4</td></tr><tr><td><eq>J_1</eq></td><td>车端面</td><td>3</td><td>车外圆</td><td>10</td><td>镗孔</td><td>1</td><td>数控立车</td><td>8</td><td>车槽</td><td>3</td><td>铣平面</td><td>4</td></tr><tr><td><eq>J_2</eq></td><td>车外圆</td><td>6</td><td>铣平面</td><td>4</td><td>镗孔</td><td>7</td><td>表面处理</td><td>9</td><td>数控立车</td><td>2</td><td>车端面</td><td>0.75</td></tr><tr><td><eq>J_3</eq></td><td>热处理</td><td>3</td><td>车槽</td><td>1</td><td>铣平面</td><td>2</td><td>车外圆</td><td>3</td><td>车端面</td><td>0.75</td><td>—</td><td>—</td></tr><tr><td><eq>J_4</eq></td><td>车外圆</td><td>2</td><td>铣平面</td><td>4</td><td>表面处理</td><td>3</td><td>镗孔</td><td>1.25</td><td>—</td><td>—</td><td>—</td><td>—</td></tr><tr><td><eq>J_5</eq></td><td>车外圆</td><td>3</td><td>铣平面</td><td>5</td><td>车槽</td><td>4</td><td>数控立车</td><td>5</td><td>车端面</td><td>3</td><td>镗孔</td><td>3</td></tr><tr><td><eq>J_6</eq></td><td>车外圆</td><td>1</td><td>检验</td><td>3</td><td>数控立车</td><td>6</td><td>铣平面</td><td>7</td><td>镗孔</td><td>3</td><td>车端面</td><td>6</td></tr><tr><td><eq>J_7</eq></td><td>钳</td><td>7</td><td>数控立车</td><td>10</td><td>车端面</td><td>9</td><td>铣平面</td><td>3</td><td>镗孔</td><td>4</td><td>车槽</td><td>10</td></tr></table>


表 7 各个机器和非机加工之间的搬运时间


<table><tr><td>设备位置</td><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td><td>6</td><td>7</td><td>8</td><td>9</td><td>10</td><td>11</td><td>12</td></tr><tr><td>1</td><td>0</td><td>0.1</td><td>0.4</td><td>0.5</td><td>0.6</td><td>0.7</td><td>1</td><td>1.1</td><td>0.8</td><td>0.5</td><td>0.8</td><td>0.1</td></tr><tr><td>2</td><td>0.1</td><td>0</td><td>0.1</td><td>0.4</td><td>0.5</td><td>0.6</td><td>0.9</td><td>1</td><td>0.7</td><td>0.6</td><td>0.9</td><td>0.4</td></tr><tr><td>3</td><td>0.4</td><td>0.1</td><td>0</td><td>0.1</td><td>0.2</td><td>0.3</td><td>0.6</td><td>0.7</td><td>0.6</td><td>0.9</td><td>1.2</td><td>0.5</td></tr><tr><td>4</td><td>0.5</td><td>0.4</td><td>0.1</td><td>0</td><td>0.1</td><td>0.2</td><td>0.5</td><td>0.6</td><td>0.7</td><td>1</td><td>1.3</td><td>0.8</td></tr><tr><td>5</td><td>0.6</td><td>0.5</td><td>0.2</td><td>0.1</td><td>0</td><td>0.1</td><td>0.4</td><td>0.7</td><td>0.8</td><td>1.1</td><td>1.4</td><td>0.9</td></tr><tr><td>6</td><td>0.7</td><td>0.6</td><td>0.3</td><td>0.2</td><td>0.1</td><td>0</td><td>0.1</td><td>0.4</td><td>0.5</td><td>0.8</td><td>1.1</td><td>1</td></tr><tr><td>7</td><td>1</td><td>0.9</td><td>0.6</td><td>0.5</td><td>0.4</td><td>0.1</td><td>0</td><td>0.1</td><td>0.2</td><td>0.5</td><td>0.8</td><td>1.3</td></tr><tr><td>8</td><td>1.1</td><td>1</td><td>0.7</td><td>0.6</td><td>0.7</td><td>0.4</td><td>0.1</td><td>0</td><td>0.1</td><td>0.4</td><td>0.7</td><td>1.4</td></tr><tr><td>9</td><td>0.8</td><td>0.7</td><td>0.6</td><td>0.7</td><td>0.8</td><td>0.5</td><td>0.2</td><td>0.1</td><td>0</td><td>0.1</td><td>0.4</td><td>1.1</td></tr><tr><td>10</td><td>0.5</td><td>0.6</td><td>0.9</td><td>1</td><td>1.1</td><td>0.8</td><td>0.5</td><td>0.4</td><td>0.1</td><td>0</td><td>0.1</td><td>0.8</td></tr><tr><td>11</td><td>0.8</td><td>0.9</td><td>1.2</td><td>1.3</td><td>1.4</td><td>1.1</td><td>0.8</td><td>0.7</td><td>0.4</td><td>0.1</td><td>0</td><td>0.5</td></tr><tr><td>12</td><td>0.1</td><td>0.4</td><td>0.5</td><td>0.8</td><td>0.9</td><td>1</td><td>1.3</td><td>1.4</td><td>1.1</td><td>0.8</td><td>0.5</td><td>0</td></tr></table>


表 8 各工序可选设备


<table><tr><td>工序名称</td><td>机器组</td><td>对应机器设备</td></tr><tr><td>数控立车</td><td>数车组</td><td><eq>{M}_{1},{M}_{2}</eq></td></tr><tr><td>车端面</td><td>普车组</td><td><eq>{M}_{3},{M}_{4},{M}_{5}</eq></td></tr><tr><td>镗孔</td><td>镗床组</td><td><eq>{M}_{6}</eq></td></tr><tr><td>车退刀槽</td><td>普车组</td><td><eq>{M}_{3},{M}_{4},{M}_{5}</eq></td></tr><tr><td>铣平面</td><td>数铣组</td><td><eq>{M}_{7},{M}_{8}</eq></td></tr><tr><td>车外圆</td><td>普车组</td><td><eq>{M}_{3},{M}_{4},{M}_{5}</eq></td></tr></table>

首先通过设置各机器之间的搬运时间为0，得到离散制造车间工件的最大完工时间为43，与文献[26]求到的解一致，其甘特图如图8所示。然后考虑如表7所示的机器间搬运时间，从各个机器、非机加工之间的搬运时间与工件工序信息表可知，离散制造车间中当车辆无限多时，其工件的最大完工时间为45。利用本文所提出的算法对离散制造车间工件小车调度问题求解，得到最短完工时间为45.35，其中各个小车搬运次数均为15次，小车负载均衡，其甘特图如图9所示。图中，当搬运时间很短，无法清晰用相应图框表达AGV时，在工件旁用文字“A0”、“A1”和“A2”分别表示由AGV0、AGV1和AGV2进行搬运。如设备M6上，工件 $\mathrm{J}_{1}$ 由AGV0进行搬运。

![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-13/30ad0010-55e3-43e0-81ea-cef724f48fff/1118e9243518c9cb7edccdda21ba5ad02005bc6d50998ae2bd66ff436ef23696.jpg)



图8 案例甘特图


![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-13/30ad0010-55e3-43e0-81ea-cef724f48fff/171a0623dfc4ed7d76f070eaa15d7fc1e5edec4372e4af7c656ecd87ee5c0cab.jpg)



图9 考虑搬运小车调度时的甘特图


通过上述两个测试案例和某离散制造车间实际生产案例的测试结果，表明了所提出的基于DQN算法的工件小车调度算法能够有效地求解离散制造车间中考虑工件工序间AGV小车搬运的调度问题，并可有效均衡搬运小车的负载。

## 4 总结

本文对考虑 AGV 小车搬运等约束的离散制造车间调度问题进行了研究，提出了基于 DQN 算法的工件小车调度算法对离散制造车间工件小车调度问题进行求解，得出以下结论。

(1) 对离散制造车间实际生产约束进行了抽象，构建了考虑小车搬运的离散制造车间工件小车调度问题模型，建立了考虑工件和小车离散制造车间的强化学习环境。

(2) 采用基于 DQN 算法的工件小车调度算法对问题进行求解，调度的最终目标是车间内任务的总完工时间最小和小车负载均衡，因此设计调度智能体可观测的空间、可获得的奖励以促进完成目标。设计调度智能体的动作选择方法实现从可观测空间到实际调度决策。

(3) 通过实际案例验证了算法的可行性和有效性，并应用于实际的离散制造车间生产，在生产应用的实例测试中，考虑小车搬运的约束，验证算法可以很好地减少车间内工件的最大完工时间、均衡小车的搬运负载，具有一定的工程应用前景，可以推广到其他小车工件搬运的调度问题中。

## 参考文献



[1] 蒋静静. 基于深度强化学习的离散型制造企业车间动态调度研究[D]. 西安：西安理工大学，2020.  
JIANG Jingjing. Research on Dynamic job shop scheduling of discrete manufacturing enterprises based on deep reinforcement learning[D]. Xi'an: Xi'an University of Technology, 2020.





[2] 甄文冬，陈进. 制造车间生产能力的影响因素研究[J]. 轻工机械，2020，38(2)：99-102，107. ZHEN Wendong, CHEN Jin. Study on Influencing Factors of production capacity in manufacturing workshop[J]. Light Industry Machinery, 2020, 38(2): 99-102, 107.





[3] 黎书文，张成龙，周知进. 基于改进粒子群算法的离散制造车间柔性调度优化[J]. 组合机床与自动化加工技术，2018(11)：150-152.
LI Shuwen, ZHANG Chenglong, ZHOU Zhijin. Flexible





scheduling optimization of discrete manufacturing workshop based on improved particle swarm optimization algorithm[J]. Modular Machine Tool & Automatic Manufacturing Technique, 2018(11): 150-152. 





[4] PIROZMAND P, HOSSEINABADI A, FARROKHZAD M, et al. Multi-objective hybrid genetic algorithm for task scheduling problem in cloud computing[J]. Neural Computing & Applications, 2021(33): 13075-13088. 





[5] SZ A, XIANG L A, BZ A, et al. Multi-objective optimisation in flexible assembly job shop scheduling using a distributed ant colony system[J]. European Journal of Operational Research, 2020, 283(2): 441-460. 





[6] MAO C L. Production management of multi-objective flexible job-shop based on improved PSO[J]. International Journal of Simulation Modelling, 2021, 20(2): 422-433. 





[7] 曾创锋，刘建军，陈庆新，等. 求解一类无关并行机调度的遗传迭代贪心算法[J]. 工业工程，2021，24(2): 110-118.
ZENG Chuangfeng, LIU Jianjun, CHEN Qingxin, et al. Genetic iterative greedy algorithm for scheduling a class of unrelated parallel machines[J]. Industrial Engineering Journal, 2021, 24(2): 110-118.





[8] 李雯璐，赵秀栩. 求解不相关并行机调度问题的十进制多目标灰狼算法[J]. 计算机应用研究，2021，38(10)：3067-3071.

LI Wenlu, ZHAO Xiuxu, Decimal multi-objective grey wolf algorithm for unrelated parallel machine scheduling problem[J]. Application Research of Computers, 2021, 38(10): 3067-3071.





[9] 谢志强，夏迎春. 基于遗传算法和分枝定界的多车间空闲产能调度方法[J]. 机械工程学报，2022，58(22)：462-472.

XIE Zhiqiang, XIA Yingchun. Multi-shop idle capacity scheduling method based on genetic algorithm and branch and bound[J]. Journal of Mechanical Engineering, 2022, 58(22): 462-472.





[10] 郑重. 自动化集装箱码头 AGV 调度及路径优化[J]. 中国港口, 2021(3): 34-36.

ZHENG Zhong. AGV scheduling and route optimization in automated container terminal[J]. China Ports, 2021(3): 34-36.





[11] 郭沛佩，付建林，江海凡，等. 基于规则的柔性作业车间机床与 AGV 联合调度优化[J]. 制造技术与机床，2021(9): 107-113.

GUO Peipei, FU Jianlin, JIANG Haifan, et al. Rule based joint scheduling optimization of machine tool and AGV in





flexible job shop[J]. Manufacturing Technology & Machine Tool, 2021(9): 107-113. 





[12] ABBEEL P, COATES A, QUIGLEY M, et al. An application of reinforcement learning to aerobic helicopter flight[C]//Advances in Neural Information Processing Systems, 2007: 1-8. 





[13] VOLODYMYR M, KORAY K, DAVID S, et al. Playing atari with deep reinforcement learning[EB/OL]. https://arxiv.org/pdf/1312.5602.pdf. 





[14] CUNHA B, MADUREIRA A M, FONSECA B, et al. Deep reinforcement learning as a job shop scheduling solver: A literature review[C]//International Conference on Hybrid Intelligent Systems, 2018: 350-359. 





[15] SUTTON R S, BARTO A G. Reinforcement learning: An introduction[J]. Cambridge: MIT Press, 1998. 





[16] LIU C L, CHANG C C, TSENG C J. Actor-critic deep reinforcement learning for solving job shop scheduling problems[J]. IEEE Access, 2020(8): 71752-71762. 





[17] WANG J, HE J, ZHANG J. A reinforcement learning method to optimize the priority of product for scheduling the large-scale complex manufacturing systems[C]//The 48th International Conference on Computers & Industrial Engineering, 2018: 2-5. 





[18] 贺俊杰，张洁，张朋，等. 基于长短期记忆近端策略优化强化学习的等效并行机在线调度方法[J]. 中国机械工程，2022，33(3)：329-338.
HE Junjie, ZHANG Jie, ZHANG Peng, et al. On line scheduling method of equivalent parallel machine based on short-term memory near end strategy optimization and reinforcement learning[J]. China Mechanical Engineering, 2022, 33(3): 329-338.





[19] LUO S. Dynamic scheduling for flexible job shop with new job insertions by deep reinforcement learning[J]. Applied Soft Computing, 2020, 91: 106208. 





[20] YANG S, XU Z, WANG J. Intelligent decision-making of scheduling for dynamic permutation flowshop via deep reinforcement learning[J]. Sensors, 2021, 21(3): 1019. 





[21] 马铭阳. 柔性作业车间加工机器与配送 AGV 双资源集成调度问题[D]. 长春：吉林大学，2021.
MA Mingyang. The dual resource integration scheduling problem of processing machine and distribution AGV in flexible job shop[D]. Changchun: Jilin University, 2021.





[22] BILGE U, ULUSOY G. A time window approach to simultaneous scheduling of machines and material handling system in an FMS[J]. Operations Research, 1995, 43(6): 1058-1070. 





[23] ABDELMAGUID T F, NASSEF A O, KAMAL B A, et al. A hybrid GA/heuristic approach to the simultaneous scheduling of machines and automated guided vehicles[J]. International Journal of Production Research, 2004, 43(2): 267-281. 





[24] KUMAR M V S, JANARDHANA R, RAO C S P. Simultaneous scheduling of machines and vehicles in an FMS environment with alternative routing[J]. The International Journal of Advanced Manufacturing Technology, 2011, 53(1): 339-351. 





[25] SAHIN C, DEMIRTAS M, EROL R, et al. A multi-agent based approach to dynamic scheduling with flexible 





processing capabilities[J]. Journal of Intelligent Manufacturing, 2017, 28(8): 1827-1845. 





[26] 周亚勤，杨长祺，吕佑龙，等. 双资源约束的航天结构件车间生产调度方法[J]. 机械工程学报，2018，54(9)：55-63.

ZHOU Yaqin, YANG Changqi, LÜ Youlong, et al, Production scheduling method for aerospace structural parts workshop with dual resource constraints[J]. Journal of Mechanical Engineering, 2018, 54(9): 55-63.



作者简介：周亚勤(通信作者)，女，1977年出生，博士，副教授。主要研究方向为智能车间生产调度建模、优化调度算法。E-mail: zhouyaqin@dhu.edu.cn