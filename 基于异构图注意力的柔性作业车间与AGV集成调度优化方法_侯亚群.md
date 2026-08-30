![](images/036ed8e8578839feb9fece0e32b3b75d383ac1e52b3d3c0852ac887b8120281b.jpg)  
控制理论与应用  
Control Theory & Applications  
ISSN 1000-8152, CN 44-1240/TP

# 《控制理论与应用》网络首发论文

题目：基于异构图注意力的柔性作业车间与AGV集成调度优化方法

作者： 侯亚群，王玉亭，韩玉艳，罗涛，陈庆达

收稿日期： 2026-06-28

网络首发日期： 2026-08-12

引用格式： 侯亚群，王玉亭，韩玉艳，罗涛，陈庆达．基于异构图注意力的柔性作业车间与AGV集成调度优化方法[J/OL].控制理论与应用. https://link.cnki.net/urlid/44.1240.TP.20260812.0947.002

![](images/52c5e14cea14a592c96e505374c8c03bebd99fde7363b5ecfdbd1db5516bce66.jpg)

![](images/9130abeb6ee7c6660d89403b26f853bedf320764ed8d5a49642c3ebe19ab04ef.jpg)

网络首发：在编辑部工作流程中，稿件从录用到出版要经历录用定稿、排版定稿、整期汇编定稿等阶段。录用定稿指内容已经确定，且通过同行评议、主编终审同意刊用的稿件。排版定稿指录用定稿按照期刊特定版式（包括网络呈现版式）排版后的稿件，可暂不确定出版年、卷、期和页码。整期汇编定稿指出版年、卷、期、页码均已确定的印刷或数字出版的整期汇编稿件。录用定稿网络首发稿件内容必须符合《出版管理条例》和《期刊出版管理规定》的有关规定；学术研究成果具有创新性、科学性和先进性，符合编辑部对刊文的录用要求，不存在学术不端行为及其他侵权行为；稿件内容应基本符合国家有关书刊编辑、出版的技术标准，正确使用和统一规范语言文字、符号、数字、外文字母、法定计量单位及地图标注等。为确保录用定稿网络首发的严肃性，录用定稿一经发布，不得修改论文题目、作者、机构名称和学术内容，只可基于编辑规范进行少量文字的修改。

出版确认：纸质期刊编辑部通过与《中国学术期刊（光盘版）》电子杂志社有限公司签约，在《中国学术期刊（网络版）》出版传播平台上创办与纸质期刊内容一致的网络版，以单篇或整期出版形式，在印刷出版之前刊发论文的录用定稿、排版定稿、整期汇编定稿。因为《中国学术期刊（网络版）》是国家新闻出版广电总局批准的网络连续型出版物（ISSN 2096-4188，CN 11-6037/Z），所以签约期刊的网络版上网络首发论文视为正式出版。

# 基于异构图注意力的柔性作业车间与AGV集成调度优化方法

侯亚群 $^{1}$ , 王玉亭 $^{1\dagger}$ , 韩玉艳 $^{1}$ , 罗涛 $^{2}$ , 陈庆达 $^{3}$

(1. 聊城大学 人工智能与计算机学院, 山东 聊城 252059;

2. 浪潮云洲工业互联网有限公司 山东 济南 250013;

3. 内蒙古大学 电子信息工程学院, 内蒙古 呼和浩特 010021)

摘要: 针对考虑运输约束的柔性作业车间调度问题(FJSPT)中生产资源与物流资源高度耦合、传统方法难以实现全局协同优化的问题, 提出了一种融合异构图神经网络与深度强化学习的端到端调度方法. 首先, 构建包含工序、机器与自动导引车(AGV)的异构图状态表示, 将加工、运输关系及其时间信息等统一编码到图结构中, 以表征生产系统中的资源关联特性. 其次, 将调度过程建模为马尔可夫决策过程, 通过联合动作空间实现工序排序、机器分配与AGV调度的协同决策. 进一步, 设计一种引入动态注意力机制的异构图融合网络(HGFN), 以增强多类型节点之间的特征交互能力, 并结合近端策略优化算法(PPO)实现策略学习. 实验结果表明, 所提方法在解质量、训练稳定性与泛化性能方面均优于对比方法, 验证了其在生产-运输耦合调度场景中的有效性.

关键词: 柔性作业车间调度问题; 自动导引车; 图神经网络; 深度强化学习; 近端策略优化; 动态注意力机制

引用格式: 侯亚群, 王玉亭, 韩玉艳, 罗涛, 陈庆达. 基于异构图注意力的柔性作业车间与AGV集成调度优化方法[J]. 控制理论与应用, 2026, 43(x): 1-10.

DOI: 10.7641/CTA.2026.60211

# Optimization Method for Flexible Job Shop and AGV Integrated Scheduling Based on Heterogeneous Graph Attention

HOU Yaqun $^{1}$ , WANG Yuting $^{1\dagger}$ , HAN Yuyan $^{1}$ , LUO Tao $^{2}$ , CHEN Qingda $^{3}$

(1. School of Artificial Intelligence and Computer Science, Liaocheng University, Liaocheng 252059; 2. Inspur Yunzhou Industrial Internet Co., Ltd., Jinan 250013;

3. College of Electronic Information Engineering, Inner Mongolia University, Hohhot 010021)

Abstract: The flexible job shop scheduling problem with transportation constraints (FJSPT) involves strong coupling between production and transportation resources, making global collaborative optimization difficult for traditional methods. To address this issue, an end-to-end scheduling framework integrating heterogeneous graph neural networks and deep reinforcement learning is proposed. First, the shop-floor state is represented as a heterogeneous graph composed of operations, machines, and automated guided vehicles (AGVs). Processing relations, transportation relations, and related temporal information are uniformly encoded into the graph structure to characterize resource interaction in the production system. Then, the scheduling process is formulated as a Markov decision process, where a joint action space is constructed for collaborative decision-making on operation sequencing, machine assignment, and AGV scheduling. Furthermore, a heterogeneous graph fusion network (HGFN) with a dynamic attention mechanism is designed to enhance feature interaction among different types of nodes, and the proximal policy optimization (PPO) algorithm is employed for policy learning. Experimental results demonstrate that the proposed method achieves superior performance in solution quality, training stability, and generalization ability compared with existing methods, validating its effectiveness in production – transportation coupled scheduling scenarios.

Key words: Flexible job shop scheduling problem; Automated guided vehicles; Graph neural networks; Deep reinforcement learning; Proximal policy optimization; Dynamic attention mechanism

Citation: HOU Yaqun, WANG Yuting, HAN Yuyan, LUO Tao, CHEN Qingda. Optimization Method for Flexible Job Shop and AGV Integrated Scheduling Based on Heterogeneous Graph Attention. Control Theory & Applications, 2026, 43(x): 1–10.

## 1 引言

柔性作业车间调度问题(Flexible Job Shop Scheduling Problem, FJSP)长期以来被视为智能制造系统中的典型优化问题. 然而, 在面向多品种、小批量及高度个性化需求的生产模式下[1-2], 传统FJSP建模方法在实际应用中逐渐显现出适应性不足, 尤其在物料流动与运输过程的描述方面存在明显欠缺. 随着智能制造技术的不断发展, 自动导引车(Automated Guided Vehicles, AGVs)因具备高度自动化和运行灵活等特点, 已广泛应用于车间内部物流环节[3], 使得生产作业调度由单纯的加工资源配置, 逐步演化为涵盖工序安排、设备选择与运输资源协同决策的综合优化问题. 因此, 考虑运输约束的柔性作业车间调度问题(Flexible Job Shop Scheduling Problem with Transportation constraints, FJSPT)逐渐成为学术界和工程实践中的重要研究课题.

FJSPT在问题特性上呈现出显著的复杂性, 其核心原因在于生产资源与运输资源之间的高度耦合. 一方面, 在进行工序调度时, 不仅需要为每道工序选择可兼容的加工机器, 还必须同步协调有限数量的AGV以执行运输任务, 从而引入大量新增决策变量, 并显著扩大了问题的解空间. 另一方面, 不同AGV的选择及其运输路径差异会导致运输时间具有不确定性, 而运输任务的完成时间又直接决定后续工序的开始与完成时间, 使加工调度与物流调度形成紧密的时序依赖关系 $^{[4]}$ .

围绕FJSPT,学术界已从传统智能优化方法逐步拓展至学习驱动型方法.早期研究主要基于精确建模与智能优化算法,通过统一刻画加工与运输过程,提升调度方案的可行性与解的质量.Fontes和Homayouni[5]采用混合整数线性规划构建了机器与AGV联合调度模型.郑和龚[6]利用四种邻域结构与左移解码策略改进人工蜂群算法.Lyu等[7]将最短路径规划与遗传算法相结合,实现了AGV路径与调度的协同优化.Meng等[8]提出了一种新型约束规划模型,并在此基础上设计了CP辅助的双种群协同遗传算法(DCGA-CP).Yang等[9]提出了一种多种群协同进化算法(MPCEA),设计了一种选择相对高质量个体的策略加快收敛速度,并引入变邻域搜索提升局部寻优能力.此类方法在中小规模问题中能够获得较优解,但随着问题规模扩大,其计算复杂度显著上升,实时适应能力亦受到明显制约.

近年来, 强化学习(Reinforcement Learning, RL)因其具备通过与环境交互自主学习序列决策策略的能力, 在复杂调度领域受到广泛关注. 为进一步提升算法的自适应性, 部分研究尝试将强化学习与传统智能优化算法相融合, 利用学习机制辅助优化搜索过程, 例如, V Sagar和Jerald $^{[10]}$ 提出了一种融合基于规则策略的双Q-learning方法实现多AGV协同控制, Jiang 和Shang $^{[11]}$ 将Q-learning与进化算法相融合, 利用学习机制设计交叉算子, Pan等 $^{[12]}$ 通过强化学习促进多种群进化算法间的协同优化. 陈等 $^{[13]}$ 设计了一种基于混合学习策略的算法, 采用四段式染色体编码与差异化交叉变异算子, 并引入Q-learning动态调整邻域结构. 上述方法通过引入强化学习机制增强了传统智能优化算法的搜索能力. 然而, 此类方法中强化学习主要用于算子选择、参数调整或邻域结构控制. 因此, 调度状态的演化通常还受到交叉、变异及局部搜索等优化操作的共同影响, 使得学习过程与调度决策过程存在间接耦合关系.

进一步地, 深度强化学习(Deep Reinforcement Learning, DRL)通过引入深度神经网络对高维、非线性状态进行自动表征, 显著提升了算法在复杂动态环境下的建模能力与泛化性能[14-15]. 孟等[16]提出了一种基于双重深度Q网络的分布式多智能体强化学习(DMA-DDQN)方法进行求解, 针对三类智能体分别设计状态和动作表示, 以实现更高效的决策. Li等[17]构建异构图以刻画工序、机器与AGV之间的加工与运输依赖关系, 提出一种基于图变换器的遗传算法引导的深度强化学习方法, 实现高质量表示学习与复合调度. Shen等[18]提出了基于PPO与Transformer的分层深度强化学习框架(MA-Trans), 通过协同双智能体架构和自注意力机制优化工件调度与AGV派发. Li等[19]提出了一种基于多智能体强化学习的实时调度框架, 结合高效动作解码与针对动态事件的状态和奖励设计, 有效应对调度中的不确定性. 然而, 此类方法通常将状态建模、特征提取与决策生成分离处理, 学习过程依赖人工先验, 难以形成统一、端到端的建模框架.

在此背景下, 端到端学习范式逐渐受到关注, 旨在实现从原始问题输入到最终调度方案的“直接映射”. 于此同时, 图神经网络(Graph Neural Networks, GN-Ns)因其在处理结构化数据和关系建模方面的优势, 能够通过节点与边的消息传递机制有效刻画多资源交互关系, 以提升状态表征能力和调度决策质量. 黄宇晗等 $^{[20]}$ 针对分布式柔性作业车间调度问题提出了一种深度强化学习驱动的多尺度窗口异构图注意力框架(MWHGA), 实现了工序-机器-工厂的联合决策. Moon等 $^{[21]}$ 设计了一个集成异质GNN与强化算法的异构作业调度器, 实现了工序-机器决策的端到端优化, 但在AGV分配上仍然依赖最近车辆选择规则. Zhang等 $^{[22]}$ 将GNN与DRL相结合, 用于工序、机器和AGV的端到端决策, 但由于嵌入计算以及对自动导引车的等距假设, 其可扩展性受到限制. Ren等 $^{[23]}$ 提出一种融合三维析取图与Dueling双深度Q网络的调度优化框架, 实现动态事件下AGV与机器的集成实时调度. 该类方法提升了复杂资源关系的建模能力, 但在端到端联合优化与动态协同决策方面仍存在不足.

尽管现有研究在FJSPT求解方面取得了显著进展,但仍存在一些共性不足.传统智能优化方法在大规模问题中面临搜索空间急剧增长和求解效率下降的问题.强化学习方法虽提升了决策的自适应能力,但部分研究仍依赖人工设计特征、启发式规则或分阶段决策机制,限制了协同优化效果.近年来,图强化学习方法增强了复杂资源关系的建模能力,但部分研究未能充分刻画机器与AGV之间的动态耦合关系,且难以实现统一的端到端联合决策 $^{[24]}$ .

综上所述, 针对上述问题, 本文提出了一种融合图神经网络与深度强化学习的端到端调度框架. 首先, 将FJSPT建模为包含三类节点(工序节点、机器节点和AGV节点)以及三类边(工序顺序关系、加工关系和运输关系)的异构图结构, 并将加工时间、运输时间等关键信息嵌入到相应的边特征中. 其次, 将调度过程形式化为马尔可夫决策过程(M-arkov Decision Process, MDP), 其中每个决策动作同时确定工序-机器-AGV的联合分配, 从而在统一的策略框架下实现工序排序、机器选择与AGV调度的协同优化. 再次, 设计了一种异构图融合网络(Heterog-eneous Graph Fusion Network, HGFN)以提取多层状态特征, 并引入动态注意力嵌入方法, 以增强机器节点和AGV节点在动态生产环境下的表征能力. 最后, 结合近端策略优化算法(Proximal Policy Optimization, PPO) $^{[25]}$ , 所提出的框架能够直接从图结构状态中学习高效的调度策略, 在优化性能、训练稳定性和泛化能力等方面均优于对比算法.

## 本文的主要贡献可概括如下:

(1)提出了一种面向FJSPT的异构图多资源状态表示方法, 将工序、机器与AGV统一建模为异构图节点及其关联关系, 并将调度过程形式化为马尔可夫决策过程, 为联合调度提供了结构化的状态建模基础.

(2)设计了一种异构图融合网络,用于多资源特征提取与交互建模.通过引入动态注意力机制,根据系统实时状态自适应调整注意力权重,从而增强节点特征表示的表达能力和环境适应性.

(3)构建一种端到端的图强化学习集成调度框架，能在统一决策过程中同时优化工序排序、机器分配与AGV调度,适用于多种规模的FJSPT,并在不同规模实例上取得优于现有启发式规则和部分深度强化学习方法的调度性能.

## 2 问题描述及其图表示

## 2.1 问题描述

在车间中有 $m$ 台机器、 $n$ 个工件和 $v$ 辆相同的AGV.每个工件 $i$ 由 $n_i$ 个具有先后顺序约束的工序组成，工件 $i$ 的第 $j$ 道工序记为 $O_{ij}$ ，每道工序 $O_{ij}$ 可以在其候选机器集合 $K_{ij}$ 中的任一台上加工.若工序 $O_{ij}$ 可在机器 $k$ 上加工，则其加工时间 $p_{i,j,k}$ 已知且确定，在不同机器上的加工时间 $p_{i,j,k}$ 可能不同.在调度开始前，所有工件和AGV均位于仓库，车间内的工件搬运任务由AGV执行.基本的假设条件如下：(1)每个工序必须且只能分配到一台可选机器上进行加工，且加工过程中不可中断.(2)初始时刻，所有工件和AGV均位于仓库.(3)初始时刻，所有机器和AGV均处于空闲状态.(4)机器缓冲区容量视为无限，允许工件在机器前等待加工.(5)AGV的行驶速度恒定，且负载状态不影响其速度.(6)每辆AGV一次只能运输一个工件(即一个工序).(7)AGV完成当前运输任务后，可停靠在当前机器处等待下一个指派任务，无需返回仓库或固定停靠点.(8)若同一工件的相邻两道工序在同一台机器上加工，则它们之间的转移无需AGV参与运输.(9)AGV在执行运输任务过程中不会出现延迟或故障

## 2.2 异构图表示

鉴于FJSPT问题在结构和决策上的复杂性与多样性,本文借鉴Song等人 $^{[26]}$ 对FJSP的建模思想,构建了一种新的异构图模型,对FJSPT问题进行结构化表示.由于工序加工依赖机器选择,运输过程依赖AGV分配,而传统基于向量表示或分阶段建模的方法难以同时刻画多资源之间的交互依赖.因此本文采用异构图显式表示加工决策与运输决策之间的耦合关系,为后续图特征传播与策略学习提供结构化状态表示.该异构图定义为 $H=(O\cup M\cup V,C,E\cup Z)$ ,包含三类节点和三类边.其中,O表示工序节点集合,并额外引入两个虚拟节点,分别用于表示调度过程的起始与结束;M和V分别表示机器节点集合和AGV节点集合.C为有向边集合,用于刻画工序之间的先后约束关系.表示工序-机器(O-M)边集合,其中每一条边 $E_{ijk}\in E$ 连接工序节点 $O_{ij}$ 与一台可加工该工序的机器节点 $M_{k}$ .表示工序-AGV(O-V)边集合,其中边 $Z_{iju}\in Z$ 表示一种候选运输关系,即AGV u具备运输工序 $O_{ij}$ 的能力.本文在初始状态下,每个工序节点均与所有AGV节点建立候选运输关系.

![](images/eae27362e39625b97028062b0805e1ccf4951a6a0cbcdc098d5bc8351fe0e3b6.jpg)  
图 1 FJSPT 异构图: (a) 一个实例; (b) 一种可行解.

Fig. 1 Heterogeneous graph of FJSPT: (a) An instance, (b) A feasible solution.  
![](images/588c2a56791b3542bea4ca4d465e315a0ae2739ac8c267c36c78105c83536ec8.jpg)  
图 2 FJSPT 实例可行调度解的甘特图.  
Fig. 2 The Gantt chart of a feasible schedule for the instance.

图1直观展示了一个FJSPT实例所对应的异构图结构. 在图中, 虚线表示所有潜在的可行关系, 包括工序与可加工机器之间的匹配关系以及工序与可执行运输任务的AGV之间的候选分配关系; 实线则表示在某一具体调度方案中实际被选取和执行的加工与运输分配关系. 基于图1(b)所示的可行解, 可以得到相应的调度结果, 其甘特图如图2所示.

## 3 算法

## 3.1 马尔可夫决策过程

在每一个决策步t, 智能体在环境时间 $T(t)$ 根据当前状态 $s_{t}$ , 选择一个动作 $a_{t}$ , 该动作将一道尚未加工的工序分配至一台可行机器, 并指派一辆AGV执行相应的运输任务. 系统执行该动作后将环境时间推进至 $T(t+1)$ , 环境转移到新的状态 $s_{t+1}$ , 并获得一个即时奖励 $r_{t+1}$ . 上述交互过程持续进行, 直至所有工序均被完成调度. 具体的MDP模型定义如下.

## 1)状态

在MDP的每一个决策步t中, 状态 $s_{t}$ 表示为一个异构图 $H_{t}(O \cup M \cup V, C, E_{t} \cup Z_{t})$ . 在该异构图中, 针对不同类型的节点与边分别构建相应的特征向量表示, 以全面刻画工序、机器和AGV的实时状态. 原始特征向量如表1所示.

$$
T r _ {i j} (t) = \left\{ \begin{array}{c} {{t _ {l _ {v} k _ {3}} + t _ {k _ {3} k _ {2}},}} \\ {{O _ {i j} \text {和} O _ {i (j - 1)} \text {均已调度}}} \\ {{\frac {1}{| M | + 1} \sum_ {k _ {1} = 0} ^ {| M |} t _ {k _ {1} k _ {3}} + \frac {1}{| K _ {i j} |} \sum_ {M _ {k _ {2}} \in K _ {i j}} t _ {k _ {3} k _ {2}},}} \\ {{O _ {i (j - 1)} \text {已调度而} O _ {i j} \text {未调度}}} \\ {{\frac {1}{(| M | + 1)   | K _ {i (j - 1)} |} \sum_ {k _ {1} = 0} ^ {| M |} \sum_ {M _ {k _ {3}} \in K _ {i (j - 1)}} t _ {k _ {1} k _ {3}} ,}} \\ {\frac {1}{| K _ {i (j - 1)} | | K _ {i j} |} \sum_ {M _ {k _ {3}} \in K _ {i (j - 1)}   \sum_ {k _ {2} \in K _ {i j}} t _ {k _ {3} k _ {2}},}} \\ {{O _ {i j} \text {和} O _ {i (j - 1)} \text {均未调度}}} \\ {{O _ {i j} \text {和} O _ {i (j - 1)} \text {均已调度}}} \end{array} \right.,\tag{1}
$$

$$
S _ {i j} \left(t\right) = \left\{ \begin{array}{c} {{S _ {i j}, O _ {i j} \text {和} O _ {i (j - 1)} \text {均已调度}}} \\ {{S _ {i (j - 1)} + p _ {i (j - 1) k _ {3}} + T r _ {i j} (t),}} \\ {{O _ {i (j - 1)} \text {已调度而} O _ {i j} \text {未调度}}} \\ {{S _ {i (j - 1)} (t) + \bar {p} _ {i (j - 1)} + T r _ {i j} (t),}} \\ {{O _ {i j} \text {和} O _ {i (j - 1)} \text {均未调度}}} \end{array} \right.,\tag{2}
$$

其中， $k_{2}$ 为当前工序 $O_{ij}$ 的加工机器编号， $k_{3}$ 为前序工序 $O_{i(j-1)}$ 的加工机器编号。 $l_{v}$ 为执行运输任务的 AGV $V_{u}$ 的当前位置。 $S_{ij}$ 为工序 $O_{ij}$ 的实际开始时间， $\overline{p}_{i(j-1)}$ 表示 $O_{i(j-1)}$ 在可选机器集上的平均加工时间。

值得注意的是, 运输时间 $Tr_{ij}(t)$ 并未作为单一整体特征直接建模, 而是根据其物理过程拆分为“AGV行驶至工件位置”和“工件运输至目标机器”两个阶段, 分别编码于工序 - AGV边与工序 - 机器边中. 基于该分解形式, 运输时间可在决策过程中通过递归方式动态估计, 从而在保持表示紧凑性的同时, 提高对加工 - 运输耦合关系的刻画能力.

2)动作

在每一个决策步 $t$ ，动作被定义为一个复合三元决策 $a_{t} = (O_{ij},M_{k},V_{u})$ ，即为一个尚未调度的工序 $O_{ij}$ 选择一台可加工该工序的机器 $M_{k}\in K_{ij}$ ，并指派一辆空闲的AGV $V_{u}$ 负责其运输任务.可行的动作 $a_{t}=(O_{ij},M_{k},V_{u})$ 需满足以下条件:工序 $O_{ij}$ 尚未被调度,且该工序是工件 $J_{i}$ 的首道工序或其直接前驱工序 $O_{i(j-1)}$ 已经完成调度;机器 $M_{k}$ 属于工序 $O_{ij}$ 的可选机器集合 $K_{ij}$ ;AGV $V_{u}$ 在时刻t处于空闲状态.

Table 1 Raw Feature Vectors of Nodes and Undirected Edges

<table><tr><td>类别</td><td>原始特征向量组成</td></tr><tr><td>工序节点 $O_{ij}$ 的原始特征向量: $\mu_{ij} \in \mathbb{R}^{8}$ </td><td>状态:二值变量,表示在决策步t时工序 $O_{ij}$ 是否已被调度(已调度为1,未调度为0).相邻机器数量 $N_{t}^{M}(O_{ij})$ .相邻AGV数量 $N_{t}^{V}(O_{ij})$ .工件i中尚未调度的工序数量.加工时间:若 $O_{ij}$ 已被调度,则为其在所选机器上的加工时间 $p_{ijk}$ ;否则,取其在所有可选机器集合 $K_{ij}$ 上的平均加工时间 $\overline{p}_{ij} = \sum_{k \in K_{ij}} p_{ijk} / |K_{ij}|$ .运输时间 $Tr_{ij}(t)$ ,动态更新,根据调度状态进行递归估计,见公式(1).开始时间 $S_{ij}(t)$ ,动态更新,根据调度状态进行递归估计,见公式(2).工件完工时间.</td></tr><tr><td>机器节点 $M_{k}$ 的原始特征向量: $\mu_{k} \in \mathbb{R}^{3}$ </td><td>相邻工序数量 $N_{t}^{O}(M_{k})$ .可用时间:机器 $M_{k}$ 完成已分配工序并可开始加工新工序的时间.利用率:机器 $M_{k}$ 的非空闲时间与总生产时间之比,取值范围为[0,1].</td></tr><tr><td>AGV节点 $V_{u}$ 的原始特征向量: $\mu_{u} \in \mathbb{R}^{3}$ </td><td>相邻工序数量 $N_{t}^{O}(V_{u})$ .可用时间.利用率.</td></tr><tr><td>工序-机器边 $E_{ijk}$ 的原始特征向量: $\mu_{ijk} \in \mathbb{R}^{2}$ </td><td>运输时间:工序 $O_{ij}$ 从其前序工序 $O_{i(j-1)}$ 的加工机器运输至机器 $M_{k}$ 所需的时间.若前序工序已被调度,则按其实际加工时间计算,否则取其在所有候选机器上的平均运输时间.加工时间 $p_{ijk}$ .</td></tr><tr><td>工序-AGV边 $Z_{iju}$ 的原始特征向量: $\mu_{iju} \in \mathbb{R}$ </td><td>运输时间:AGV  $V_{u}$ 从其当前位置 $l_{v}$ 行驶至前序工序 $O_{i(j-1)}$ 所对应机器的时间;若前序工序已被调度,则按其实际加工机器计算,否则取其可选机器集合 $K_{i(j-1)}$ 上的平均运输时间.</td></tr></table>

在每一决策步中,本文基于当前状态动态构建合法动作集合 $A_{t}$ ，并仅对集合 $A_{t}$ 中的候选动作进行评分与采样，而非对完整组合动作空间进行统一输出.

## 3)状态转移

在执行动作 $a_{t}$ 后，环境以确定性的方式转移到下一状态 $s_{t+1}$ . 异构图由 $H_{t}$ 更新为 $H_{t+1}$ ，其核心体现在边集合 $E_{t}$ 和 $Z_{t}$ 的变化上. 具体而言，当动作 $a_{t}=(O_{ij},M_{k},V_{u})$ 被执行后，仅保留工序 $O_{ij}$ 与所选机器 $M_{k}$ 之间的O-M边 $E_{ijk}$ ，以及工序 $O_{ij}$ 与所选AGV $V_{u}$ 之间的O-A边 $Z_{iju}$ . 与工序 $O_{ij}$ 相关的其他候选O-M边和O-V边将被置为不可选状态. 相应地，图中节点的邻接关系随之发生变化，所有节点和边的特征向量也会随状态转移进行动态更新.

## 4)奖励

奖励函数的设计直接服务于最小化最大完工时间这一优化目标. 在每一个决策步 $t$ , 根据当前已调度工序所形成的部分调度方案, 定义状态 $s_t$ 下的部分完工时间 $C(s_t)$ 为所有机器最早可用时间的最大值. 在此基础上, 即时奖励 $r_t$ 被定义为相邻两个状态 $s_t$ 与 $s_{t+1}$ 之间部分调度完工时间的变化量:

$$
r _ {t} = r \left(s _ {t}, a _ {t}, s _ {t + 1}\right) = C \left(s _ {t}\right) - C \left(s _ {t + 1}\right).\tag{3}
$$

该奖励函数刻画了单次调度决策对系统时间推进的直接影响. 当折扣因子 $\gamma = 1$ 时, 一个完整调度回合内的累计回报 $G$ 可表示为:

$$
G = \sum_ {t = 0} ^ {T} r _ {t} = C (s _ {0}) - C (s _ {T}),\tag{4}
$$

其中, 对于给定调度实例, 初始状态下 $C(s_{0}) = 0$ ; 在终止状态 $s_{T}$ 下, 所有工序均已完成调度, 此时 $C(s_{T})$ 即为最终调度方案的最大完工时间.

## 5)策略

策略 $\pi(a_{t}\mid s_{t})$ 描述了在状态 $s_{t}$ 下采取动作 $a_{t}$ 的概率分布.在第3.2节中,将进一步通过神经网络对调度状态进行特征提取与表示学习,并结合强化学习方法实现调度策略的优化.

## 3.2 网络架构和特征提取

本文提出了一种用于求解FJSPT的异构图融合网络(Heterogeneous Graph Fusion Network, HGFN), 其整体架构和工作流程如图3所示. 在每个决策步, 当前调度状态首先被表示为异构图 $H_{t}$ , 并输入至HGFN进行特征编码. 随后, 网络分别对工序、机器与AGV节点进行嵌入学习, 构成面向多类型节点建模的三阶段嵌入过程, 并通过多层异构图信息传播实现不同类型节点之间的特征交互. 经过 $L$ 层嵌入后, 分别得到三类节点的最终表示; 随后, 通过对各类型节点嵌入进行平均池化与拼接操作, 构建统一的图级状态表示, 以增强全局状态信息表达能力. 最终, 结合节点嵌入与图嵌入对候选动作进行优先级评分, 并生成联合动作概率分布, 实现对工序排序、机器分配及AGV调度的联合决策. 具体过程如下.

![](images/85c964e4c11d972a8d60c37a6e302fc9616378aed0c664a18abf1be7c531001c.jpg)  
图 3 网络架构及其工作流程.  
Fig. 3 The network architecture and its workflow.

## 1)机器节点嵌入

在传统图注意力网络(Graph Attention Network, GAT) $^{[27]}$ 中, 计算得到的注意力系数的排序不受查询节点的影响, 即任意查询节点对同一键节点具有相同的注意力权重, 这属于一种静态注意力机制. 为此, GATv2 $^{[28]}$ 通过调整注意力中的计算顺序, 将非线性激活前置于注意力权重向量的点积操作, 从而实现了动态注意力机制. 该机制允许不同查询节点对同一键节点分配不同的注意力权重, 从而更准确地刻画异构节点间的交互关系.

本文在机器节点的嵌入过程中引入GATv2的动态注意力机制. 具体而言, 首先, 对于具有特征向量 $\mu_{k}$ 的机器节点 $M_{k}$ , 针对其每一个相邻的工序节点 $O_{ij} \in N_{t}^{O}(M_{k})$ , 计算对应的注意力系数 $e_{ijk}$ :

$$
e _ {i j k} =\tag{5}
$$

$$
\mathbf {a} ^ {\top} \text { LeakyReLU } \left(\mathbf {W} _ {1} ^ {O} \boldsymbol {\mu} _ {i j} + \mathbf {W} ^ {M} \boldsymbol {\mu} _ {k} + \mathbf {W} ^ {E} \boldsymbol {\mu} _ {i j k}\right)
$$

其中 $\mu_{ij} \in \mathbb{R}^8$ 表示工序节点 $O_{ij}$ 的特征向量, $\mu_k \in \mathbb{R}^3$ 表示机器节点 $M_k$ 的特征向量, $\mu_{ijk} \in \mathbb{R}^2$ 为连接工序节点与机器节点的O-M边特征. $\mathbf{W}_1^O \in \mathbb{R}^{d \times 8}$ 、 $\mathbf{W}^M \in \mathbb{R}^{d \times 3}$ 和 $\mathbf{W}^E \in \mathbb{R}^{d \times 2}$ 分别为可学习的权重矩阵, 用于对节点特征和边特征进行独立线性变换. 经线性变换与LeakyReLU激活后, 通过权重向量 $\mathbf{a} \in \mathbb{R}^d$ 计算加权求和.

随后, 对注意力系数进行softmax归一化, 以保证每个机器节点对其所有相邻工序节点的注意力权重之和为1:

$$
\alpha_ {i j k} = \frac {\exp (e _ {i j k})}{\sum_ {O _ {i j} \in N _ {t} ^ {O} (M _ {k})} \exp (e _ {i j k})}.\tag{6}
$$

在此基础上,根据归一化后的注意力权重 $\alpha_{ijk}$ ,对相邻工序节点的特征进行加权聚合,得到机器节点 $M_{k}$ 的邻域聚合表示:

$$
\boldsymbol {\mu} _ {k} ^ {(n e i g h)} = \sum_ {O _ {i j} \in N _ {t} ^ {O} (M _ {k})} \alpha_ {i j k} \mathbf {W} _ {\mathbf {1}} ^ {O} \boldsymbol {\mu} _ {i j}.\tag{7}
$$

此外, 机器节点的嵌入更新不仅依赖于邻域信息, 还包含其自身特征的更新. 该过程通过一个由全连接层和ReLU激活函数构成的多层感知机实现:

$$
\boldsymbol {\mu} _ {k} ^ {(s e l f)} = \operatorname{MLP} \left(\boldsymbol {\mu} _ {k}\right).\tag{8}
$$

由此, 机器节点的最终嵌入特征 $\mu_{k}^{\prime}$ 为:

$$
\boldsymbol {\mu} _ {k} ^ {\prime} = \frac {1}{2} \left(\boldsymbol {\mu} _ {k} ^ {(n e i g h)} + \boldsymbol {\mu} _ {k} ^ {(s e l f)}\right),\tag{9}
$$

## 2)AGV节点嵌入

与机器节点嵌入方法类似,本文同样采用动态注意力机制对AGV节点的特征进行嵌入表示.节点 $V_{u}$ 的嵌入特征的计算过程如下:

$$
e _ {i j u} = \mathbf {a} ^ {\top} \text {LeakyReLU} \left(\mathbf {W} _ {\mathbf {2}} ^ {O} \boldsymbol {\mu} _ {i j} + \mathbf {W} ^ {V} \boldsymbol {\mu} _ {u} + \mathbf {W} ^ {Z} \boldsymbol {\mu} _ {i j u}\right)
$$

$$
\alpha_ {i j u} = \frac {\exp (e _ {i j u})}{\sum_ {O _ {i j} \in N _ {t} ^ {O} (V _ {u})} \exp (e _ {i j u})},\tag{10}
$$

(11)

$$
\boldsymbol {\mu} _ {u} ^ {(n e i g h)} = \sum_ {O _ {i j} \in N _ {t} ^ {O} (V _ {u})} \alpha_ {i j u} \mathbf {W} _ {\mathbf {2}} ^ {O} \boldsymbol {\mu} _ {i j},\tag{12}
$$

$$
\boldsymbol {\mu} _ {u} ^ {(s e l f)} = \mathrm{MLP} \left(\boldsymbol {\mu} _ {u}\right),\tag{13}
$$

$$
\boldsymbol {\mu} _ {u} ^ {\prime} = \frac {1}{2} \left(\boldsymbol {\mu} _ {u} ^ {(n e i g h)} + \boldsymbol {\mu} _ {u} ^ {(s e l f)}\right).\tag{14}
$$

3)工序节点嵌入

在 $H_{t}$ 中，工序 $O_{ij}$ 的邻居节点包括其直接前驱工序 $O_{i,j - 1}$ 、直接后继工序 $O_{i,j + 1}$ ，以及来自可选机器集合 $N_{t}(O_{ij},M)$ 的机器和来自可选AGV集合 $N_{t}(O_{ij},V)$ 的AGV.本文中使用六个不同的MLP来处理来自不同信息源的数据.工序 $O_{ij}$ 的嵌入计算公

式如下:

$$
\begin{array}{l} \boldsymbol {\mu} _ {i j} ^ {\prime} = \\ \mathrm{MLP} _ {\theta_ {0}} \left(\mathrm{ELU} \left[ \mathrm{MLP} _ {\theta_ {1}} \left(\boldsymbol {\mu} _ {i, j - 1}\right) \| \mathrm{MLP} _ {\theta_ {2}} \left(\boldsymbol {\mu} _ {i, j + 1}\right) \| \right. \right. \\ \left. \mathrm{MLP} _ {\theta_ {3}} \left(\overline {{\boldsymbol {\mu}}} _ {i j} ^ {M}\right) \| \mathrm{MLP} _ {\theta_ {4}} \left(\overline {{\boldsymbol {\mu}}} _ {i j} ^ {V}\right) \| \mathrm{MLP} _ {\theta_ {5}} \left(\boldsymbol {\mu} _ {i j}\right) ]\right). \end{array}\tag{15}
$$

具体而言, $MLP_{\theta_{1}},\ldots,MLP_{\theta_{5}}$ 分别用于处理来自前驱工序 $O_{i,j-1}$ 、后继工序 $O_{i,j+1}$ 、邻居机器 $M_{k}\in N_{t}^{M}(O_{ij})$ 、邻居AGV $V_{u}\in N_{t}^{V}(O_{ij})$ 以及工序 $O_{ij}$ 本身的信息.其中,输入 $MLP_{\theta_{3}}$ 的为 $\bar{\mu}_{ij}^{M}=\sum_{M_{k}\in N_{t}^{M}(O_{ij})}\mu_{k}^{\prime}$ ,输入 $MLP_{\theta_{4}}$ 的为 $\bar{\mu}_{ij}^{V}=\sum_{V_{u}\in N_{t}^{V}(O_{ij})}\mu_{u}^{\prime}.MLP_{\theta_{0}}$ 负责最终投影,将所有信息进行拼接和特征融合.所有六个MLP结构相同,输出维度为d,包含两个 $d_{h}$ 维的隐藏层,并采用ELU激活函数.

## 4)图嵌入

通过堆叠L层结构相同但参数相互独立的嵌入层，可以分别得到工序节点、机器节点和AGV节点的最终嵌入表示 $\boldsymbol{\mu}_{ij}^{(L)}$ 、 $\boldsymbol{\mu}_{k}^{(L)}$ 和 $\boldsymbol{\mu}_{u}^{(L)}$ .随后,为了构建图级别的状态向量,分别对三类节点的嵌入特征进行平均池化,并将结果进行拼接,得到最终的图嵌入表示:

$$
\mathbf {h} _ {t} = \left[ \frac {1}{| O |} \sum_ {O _ {i j} \in O} \boldsymbol {\mu} _ {i j} ^ {(L)} \left\| \frac {1}{| M |} \sum_ {M _ {k} \in M} \boldsymbol {\mu} _ {k} ^ {(L)} \right\| \frac {1}{| V |} \sum_ {V _ {u} \in V} \boldsymbol {\mu} _ {u} ^ {(L)} \right]\tag{16}
$$

在第3.1节中，调度动作为 $a_{t}=(O_{ij},M_{k},V_{u})$ . 在完成异构图特征提取后，需要进一步基于所学习的节点嵌入生成联合调度动作. 为计算调度过程中动作 $a_{t}$ 被选中的概率，本文设计了一种调度动作优先级评分方法. 在时间步t，将工序嵌入 $\mu_{ij}^{(L)}$ 、机器嵌入 $\mu_{k}^{(L)}$ 、AGV嵌入 $\mu_{u}^{(L)}$ 以及图嵌入 $h_{t}$ 进行拼接，并输入至一个MLP中，以得到状态 $s_{t}$ 下每一个候选动作 $a_{t}$ 的优先级得分：

$$
P \left(a _ {t} | s _ {t}\right) = \mathrm{MLP} _ {\omega} \left[ \mu_ {i j} ^ {(L)} \| \mu_ {k} ^ {(L)} \| \mu_ {u} ^ {(L)} \| \mathbf {h} _ {t} \right].\tag{17}
$$

随后, 采用softmax函数对所有候选动作组合 $(O_{ij}, M_{k}, V_{u})$ 的优先级得分进行归一化, 得到最终的策略概率分布:

$$
\pi_ {\omega} \left(a _ {t} | s _ {t}\right) = \frac {\exp \left(P \left(a _ {t} | s _ {t}\right)\right)}{\sum_ {a _ {t} ^ {\prime} \in A _ {t}} \exp \left(P \left(a _ {t} ^ {\prime} | s _ {t}\right)\right)}.\tag{18}
$$

## 3.3 训练

本文进一步采用强化学习方法对调度策略进行训练与优化, 使用近端策略优化(PPO)算法, 通过智能体与调度环境之间的交互不断更新策略网络参数, 从而学习高质量调度策略. 如算法1所示, 模型的训练过程共进行 $N_{ep}$ 个训练轮次. 在每一轮训练中, 数据加载器以批处理方式提供训练样本, 每个批次包含B个相互独立的FJSPT实例. 智能体同时与这B个并行环境进行交互, 并基于当前策略为每个实例选择相应的调度动作. 在并行交互过程中, 智能体从环境中同步接收奖励信号, 并将状态转移过程存储至经验缓存中.

该方法采用Actor-Critic结构, 其中Actor(策略网络 $\pi_{\omega}$ 负责根据当前状态选择调度动作), Critic(价值网络 $v_{\varphi}$ 用于估计状态价值函数). 两类网络均由多层感知机构成, 包含多层隐藏层, 并采用tanh作为激活函数. 二者在输入上有所不同: 策略网络以维度为6d的特征作为输入, 该特征由节点嵌入与图级全局池化特征拼接而成; 而价值网络仅以维度为3d的图级全局池化特征作为输入, 用于评估当前状态的整体价值.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
算法1基于PPO的训练流程  
输入：总训练周期数 $N_{ep}$ ，批大小 $\mathcal{B}$ ,PPO子周期数 $\mathcal{R}$ ，网络及其参数 $\theta ,\omega ,\varphi$ ，策略更新周期K，验证周期H  
1: for epoch = 1 to $N_{ep}$ do  
2: for DataLoader中大小为 $\mathcal{B}$ 的实例do  
3: for $b = 1$ to $\mathcal{B}$ do ▷并行执行  
4: 基于FJSPT实例b初始化状态 $s_t$   
5: while $s_t$ 非终止状态do  
.6: 使用HGFN提取状态嵌入  
7: 根据策略采样动作 $a_{t}\sim \pi_{\theta}(\cdot |st)$   
8: 获得奖励 $r_t$ 与下一状态 $s_{t + 1}$   
9: 收集 $(s_t,a_t,r_t,s_{t + 1})$ 并存入缓冲区  
10: $s_t\gets s_{t + 1};$   
11: end while  
12: end for  
13: episode $\leftarrow$ episode $+1$   
14: if episode% $\mathcal{K} = 0$ then  
15: 计算GAE $\hat{A}_t$ ，计算损失  
16: 在 $\mathcal{R}$ 个子周期内优化 $\theta ,\omega ,\varphi$ ，清空缓冲区  
17: end if  
18: if episode% $\mathcal{H} = 0$ then  
19: 在验证集上评估当前策略性能  
20: end if  
21: end for  
22: end for
</div>

## 4 仿真实验

本节介绍用于评估所提出算法(以下简称HGFN-PPO)性能的实验设计方案.所有实验均在一台配备Intel(R) Core(TM)i7-10700 CPU和NV-IDIA GeForce GTX 1650 SUPER GPU的个人计算机上完成.

## 4.1 实验设置

为训练与评估所提出的模型,首先生成了一批合成的FJSPT实例[26,29]. 训练与验证阶段共考虑了四种问题规模 $(10\times 5\times 2$ 、 $10\times 5\times 5$ 、 $20\times 5\times 5$ 和 $20\times$ $10\times 10)$ ，每种规模均包含100个验证实例.其中， $10\times 5\times 2$ 配置对应于运输资源相对稀缺的场景，而 $20\times 5\times 5$ 配置则反映了加工资源受限的情形.相比之下， $10\times 5\times 5$ 和 $20\times 10\times 10$ 配置代表机器与AGV资源均较为充足的环境.生成测试集的参数及详细配置总结于表2中.

表 2 合成实例生成的参数  
Table 2 Synthetic Instance Generation Distributions

<table><tr><td>参数</td><td>取值</td></tr><tr><td>工件i的工序数量ni</td><td>U(0.8m, 1.2m)</td></tr><tr><td>可加工工序Oi,j的机器数量Kij</td><td>U(1,m)</td></tr><tr><td>工序Oi,j的平均加工时间pi̅j</td><td>U(1,20)</td></tr><tr><td>工序Oi,j在机器k上的加工时间pi̅jk</td><td>U(0.8p̅ij, 1.2p̅ij)</td></tr></table>

除合成数据外,还选取了三个公开基准数据集以进一步验证算法的有效性与泛化能力.

基准集D1: 由Homayouni和Fontes $^{[30]}$ 设计的20个中小规模FJSP实例(SFJS1-10、MFJS1-10)，包含2-12个工件和2-8台机器。基于与合成数据相同的布局方案，将其扩展为FJSPT实例。AGV数量按机器数量的0.8m-1.2m配置，运输路径由机器布局确定。车间布局及运输时间矩阵的构建方式参照Homayouni和Fontes所提出的布局设置，详见https://fastmanufacturingproject.wordpress.com/2019/04/11/fjspt-instances/.

基准集D2: 包含10个大规模实例(Mk01-Mk10) $^{[29]}$ ，规模范围为 $10\times6$ 至 $20\times15$ ，工序数为55-240. AGV数量与运输路径配置方式与D1相同.

基准集D3: 包含10个实例(FJSPT1-FJSPT10) $^{[31]}$ ，每个实例均由8个工件组成，工序数为13-21，且AGV数量固定为2。该基准集主要用于评估模型在运输资源受限条件下的泛化性能。

所提出的方法与以下六种方法进行了对比:

优先调度规则(PDRs) $^{[29,32-33]}$ ：先进先出(FIFO)、剩余工序最多(MOR)和最短加工时间(SPT)，并结合最早空闲AGV规则；

基于深度强化学习的方法: Moon等 $^{[21]}$ 提出的异构图调度器(Heterogeneous Job Scheduler, HGS), Wang等 $^{[34]}$ 提出的注意力增强强化学习方法(Attention enhanced reinforcement learning, 记为DRL-A), 以及Zhang等 $^{[22]}$ 提出的一种基于异构图神经网络与深度强化学习相结合的调度方法(记为DRL-D).

算法性能通过完工时间的相对百分比偏差(Rela-

tive Percentage Increase, RPI)进行评估, 其定义如下:

$$
RPI = \frac{\left|C_{max} - C_{\text{max}}^{best}\right|}{C_{\text{max}}^{best}}\times 100\% .\tag{19}
$$

对于拟建HGFN-PPO的网络架构, 网络架构设置和训练配置如表3所示.

表 3 网络架构与训练配置  
Table 3 Network Architecture and Training Configuration

<table><tr><td>参数</td><td>配置</td></tr><tr><td>HGFN嵌入层数</td><td> $L = 2$ </td></tr><tr><td>动态注意力头数</td><td> $h = 2$ </td></tr><tr><td>嵌入维度</td><td> $d = {10}$ </td></tr><tr><td>节点嵌入MLP隐藏层维度</td><td> ${d}_{h} = {128}$ </td></tr><tr><td>损失系数</td><td>policy=1,value=0.5,entropy=0.01</td></tr><tr><td>训练</td><td> $N_{ep} = {1000},\mathcal{B} = {20},\mathcal{R} = 3,$  $K = 1,H = {10}$ </td></tr><tr><td>学习率</td><td> $\eta = 2\times {10}^{-4}$ </td></tr><tr><td>折扣因子</td><td> $\gamma = {0.99}$ </td></tr><tr><td>裁剪因子</td><td> $\epsilon = {0.2}$ </td></tr><tr><td>策略/价值网络</td><td>3个隐藏层,每层维度64</td></tr></table>

## 4.2 在合成算例上的性能表现

为验证所提出的算法的性能,本文在四种问题规模下进行了全面的仿真实验.每种规模均经过训练,并在固定的100个测试算例上进行评估.评估指标包括最大完工时间和相对性能指标.如图4所示, $10\times5\times5$ 和 $20\times10\times10$ 规模算例的收敛曲线表明,该模型在不同规模下均呈现稳定的学习特性.曲线逐渐收敛至稳定区间,且波动逐渐减小,证明智能体能够有效学习高质量的调度策略,并在无需人工调参的情况下自主选择适宜的动作.

![](images/d207882841cb00d83dd99dfe4d6d929beb690e3e89c7bb7fb0d2d0458687a601.jpg)  
(a) $10 \times 5 \times 5$

![](images/9a5e1c5df9bf2981c3bdc25341d899425395d80eca1b6987a94ef11643abde46.jpg)  
(b) $20 \times 10 \times 10$  
图 4 训练所得平均Makespan的收敛曲线.  
Fig. 4 The average makespan convergence curves obtained through training.

本小节对所提方法与其他多种基线算法在不同规模合成FJSPT算例上的性能进行了全面对比. 表4汇总的结果表明, 所提方法在所有对比算法中均取得了显著的优越性能, 且随着问题规模和资源复杂度的增加, 该方法相较其他算法的优势进一步扩大.

具体而言, HGFN-PPO始终优于FIFO、MOR和S-PT等传统启发式方法, 其RPI均达到48.98%以上, 表明所提出方法能够有效学习复杂调度环境中的决策规律. 相比于传统规则驱动策略, 基于DRL的方法能够通过与环境交互持续优化调度策略, 从而获得更优的调度结果, 而在所有DRL方法中, HGFN-PPO同样表现出最优性能. 相比之下, HGS方法仍采用启发式规则进行AGV选择, 整体调度性能受到一定限制.

此外, 在 $20 \times 10 \times 10$ 的大规模场景中, HGFN-PPO展现出更加显著的优势. 在100个测试算例上, 其平均最大完工时间仅为292.54, 相较于其他基线方法可进一步降低 $44.01\% \sim 115.86\%$ . 这表明, 随着问题规模与资源耦合复杂度的增加, 所提出的异构图建模方式能够更有效地刻画工序、机器与AGV之间的交互依赖关系. 与此同时, HGFN通过异构节点间的信息传播与特征融合, 能够学习加工资源与运输资源之间的协同调度规律, 从而在复杂场景下仍保持较优的调度性能. 此外, 联合动作决策机制避免了传统分阶段调度中局部最优累积的问题, 使模型能够在统一策略框架下实现多资源协同优化.

在运行时间方面, HGFN-PPO比PDR方法需要稍多的计算量, 与其他基于DRL的基线方法相当. 对于小规模算例 $(10\times5\times2$ 和 $10\times5\times5)$ , HGFN-PPO耗时约2-3秒, 而PDR方法为1-2秒. 随着问题规模增大, 运行时间增加至约8-19秒. 计算开销的增加源于异构图建模与策略学习的结合, 这需要对复杂的节点交互进行更深层次的特征提取和推理. 尽管如此, 考虑到其在调度质量上的显著提升,这一额外成本是合理且可接受的.

## 4.3 在公开基准数据集上的性能表现

本节进一步在两个广泛使用的公开基准数据集上评估所提方法的泛化能力. 模型在 $10 \times 5 \times 5$ 算例上训练完成后, 直接用于评估, 未进行重新训练.

表5给出了各算法在公开基准数据集D1、D2和D3的40个算例上的调度性能对比结果. 从整体结果可以看出, HGFN-PPO在所有基准数据集上均取得了最优的Makespan, 表现出稳定且显著的性能优势. 具体而言, HGFN-PPO在绝大多数算例中均优于对比方法, 在约 $90\%$ 的算例中取得了 $0.00\%$ 的RPI. 在剩余算例中, RPI范围在 $4.54\%$ 至 $9.15\%$ 之间, 表明其解仍接近最优. 相比之下, PDRs能够在小型算例上获得可行解, 但其性能随问题规模增大而迅速下降, 在大规模算例中RPI值常超过 $40\%$ . 这些结果凸显了HGFN-PPO的优越性, 表明其能够适应不同问题规模, 在保证解质量的同时展现出更好的泛化能力. 这也说明所提出的异构图状态表示能够较好地保留不同规模调度问题中的结构化信息, 从而增强模型对未见实例的泛化能力.

![](images/2e30301b479328b64068541c0749f83600d8471c02a51918903e76fd8d0488f7.jpg)  
图 5 所有方法在公开基准数据集上的RPI分布箱线图.  
Fig. 5 Box plots of the RPI distribution for all methods on public benchmark.

图5通过箱线图提供了各方法RPI分布情况的可视化对比. 可以观察到, HGFN-PPO箱体较短且在大多数情况下RPI接近0%, 整体波动范围极小.

## 4.4 统计分析

本节从统计学角度严格评估了各算法之间的整体性能差异, 并在不同问题规模下进行了显著性分析. 首先进行了Friedman检验. 基于所有公共基准数据集, 检验结果为 $\chi^{2}=180.59$ , 显著性水平 $p=2.55\times10^{-36}$ . p值远低于0.05的显著性阈值, 明确拒绝了“算法间无性能差异”的原假设, 表明观测到的性能差异具有统计显著性. 基于Makespan和RPI的详细Friedman检验结果如表6所示. 在所有数据集上, 所提方法均始终获得最佳的平均排名. 为进一步探究成对差异, 本文进行了Nemenyi事后检验, 结果以热力图形式可视化于图6. 在这些热力图中, 单元格值代表p值, 蓝色越深表示统计显著性越强. HGFN-PPO均展现出统计显著的优越性, 从而进一步印证了其可扩展性.

表 4 各算法在合成训练算例上的性能表现  
Table 4 Performances of All Compared Algorithms on Synthetic Training Instances

<table><tr><td>规模</td><td></td><td>DRL-D</td><td>HGS</td><td>DRL-A</td><td>FIFO</td><td>MOR</td><td>SPT</td><td>HGFN-PPO</td></tr><tr><td rowspan="3">10×5×2</td><td>Makespan</td><td>355.76</td><td>352.81</td><td>309.51</td><td>508.96</td><td>480.31</td><td>474.20</td><td>286.65</td></tr><tr><td>RPI</td><td>24.11%</td><td>23.08%</td><td>7.98%</td><td>77.55%</td><td>67.56%</td><td>65.43%</td><td>0.00%</td></tr><tr><td>Time(s)</td><td>2.33</td><td>1.67</td><td>1.69</td><td>1.28</td><td>1.44</td><td>1.52</td><td>2.94</td></tr><tr><td rowspan="3">10×5×5</td><td>Makespan</td><td>193.39</td><td>226.38</td><td>186.84</td><td>260.15</td><td>239.30</td><td>243.34</td><td>160.63</td></tr><tr><td>RPI</td><td>20.40%</td><td>40.94%</td><td>16.32%</td><td>61.96%</td><td>48.98%</td><td>51.49%</td><td>0.00%</td></tr><tr><td>Time(s)</td><td>2.97</td><td>2.86</td><td>2.72</td><td>1.61</td><td>1.55</td><td>1.75</td><td>3.06</td></tr><tr><td rowspan="3">20×5×5</td><td>Makespan</td><td>310.68</td><td>385.80</td><td>358.76</td><td>461.37</td><td>533.35</td><td>473.14</td><td>258.1</td></tr><tr><td>RPI</td><td>20.37%</td><td>49.47%</td><td>39.00%</td><td>78.76%</td><td>106.64%</td><td>83.31%</td><td>0.00%</td></tr><tr><td>Time(s)</td><td>5.64</td><td>6.07</td><td>5.26</td><td>2.56</td><td>2.89</td><td>3.62</td><td>8.42</td></tr><tr><td rowspan="3">20×10×10</td><td>Makespan</td><td>426.8</td><td>457.98</td><td>421.31</td><td>631.49</td><td>585.52</td><td>570.94</td><td>292.54</td></tr><tr><td>RPI</td><td>45.89%</td><td>56.55%</td><td>44.01%</td><td>115.86%</td><td>100.15%</td><td>95.16%</td><td>0.00%</td></tr><tr><td>Time(s)</td><td>20.36</td><td>23.14</td><td>19.94</td><td>9.57</td><td>10.71</td><td>11.08</td><td>19.07</td></tr></table>

表 5 各算法在公开基准数据集上的性能表现

Table 5 Performance of All Algorithms on Public Benchmarks

<table><tr><td>算例集</td><td></td><td>DRL-D</td><td>HGS</td><td>DRL-A</td><td>FIFO</td><td>MOR</td><td>SPT</td><td>HGFN-PPO</td></tr><tr><td rowspan="2"> $D1$ </td><td>Makespan</td><td>711.1</td><td>667.45</td><td>658.5</td><td>898.85</td><td>932.4</td><td>960.9</td><td>537.5</td></tr><tr><td>RPI</td><td>32.30%</td><td>24.18%</td><td>22.51%</td><td>67.23%</td><td>73.47%</td><td>78.77%</td><td>0.00%</td></tr><tr><td rowspan="2"> $D2$ </td><td>Makespan</td><td>410.65</td><td>448.55</td><td>432.05</td><td>721.1</td><td>696.6</td><td>649.4</td><td>321.5</td></tr><tr><td>RPI</td><td>27.73%</td><td>39.52%</td><td>34.39%</td><td>124.29%</td><td>116.67%</td><td>101.99%</td><td>0.00%</td></tr><tr><td rowspan="2"> $D3$ </td><td>Makespan</td><td>161.2</td><td>184.8</td><td>220.9</td><td>320</td><td>271.2</td><td>291.4</td><td>143.1</td></tr><tr><td>RPI</td><td>12.65%</td><td>29.14%</td><td>54.37%</td><td>123.62%</td><td>89.52%</td><td>103.63%</td><td>0.00%</td></tr></table>

![](images/a4bf353027a31b281cac99f642975cb8eea8609922065c6f3aaf93254674ba8c.jpg)  
图 6 Nemenyi事后检验热力图.  
Fig. 6 Nemenyi post-test heat map.

为提供更精确的成对证据,本文进行了Wilcoxon符号秩检验,结果见表7.这些结果进一步支持:在 $\alpha=0.05$ 的显著性水平下,无论是基于Makespan还是RPI,HGFN-PPO与所有基线算法比较得出的p值均远低于0.05.因此,在所有情况下均可拒绝原假设,表明HGFN-PPO在统计意义上优于基线方法.

综上所述, 通过Friedman和检验、Nemenyi事后检验以及Wilcoxon符号秩检验, 结果表明所提出的方法在解质量、稳定性和泛化能力等方面均表现出显著的优势, 具有一致且稳健的统计学支撑.

## 4.5 工程应用案例

为进一步验证所提方法的有效性,本文将其应用于中国某煤矿机械结构件生产车间的实际案例中.车间包含6类加工设备,其中部分工序采用并行机器配置,因此车间内共有11台机器.工件在各机器之间的运输由2辆AGV完成.各设备类型及其对应加工工序如表8所示.AGV在各机器之间的运输时间如表9所示.本案例共包含20个工件,其工艺路线和加工时间详见表10

表 6 公共基准算例上基于Makespan和RPI的Friedman检验结果  
Table 6 Results of Friedman Test by Makespan and RPI on Public Benchmarks

<table><tr><td rowspan="2">方法</td><td rowspan="2">排名</td><td colspan="4">Makespan</td><td colspan="4">RPI</td></tr><tr><td>均值</td><td>标准差</td><td>最小值</td><td>最大值</td><td>均值</td><td>标准差</td><td>最小值</td><td>最大值</td></tr><tr><td>DRL-D</td><td>2.925</td><td>498.5125</td><td>463.1394</td><td>70</td><td>2091</td><td>17.9980</td><td>16.2665</td><td>0</td><td>60.82</td></tr><tr><td>HGS</td><td>2.975</td><td>492.0625</td><td>448.1979</td><td>70</td><td>1938</td><td>18.4108</td><td>15.6733</td><td>0</td><td>55.71</td></tr><tr><td>DRL-A</td><td>3.275</td><td>492.4875</td><td>411.4021</td><td>70</td><td>1747</td><td>23.9778</td><td>23.1620</td><td>0</td><td>108.51</td></tr><tr><td>FIFO</td><td>5.975</td><td>709.7000</td><td>591.2135</td><td>103</td><td>2467</td><td>81.7213</td><td>36.0383</td><td>4.15</td><td>158.02</td></tr><tr><td>MOR</td><td>5.8625</td><td>708.1500</td><td>567.7888</td><td>95</td><td>2373</td><td>78.4028</td><td>34.7736</td><td>10.86</td><td>155.93</td></tr><tr><td>SPT</td><td>5.7375</td><td>715.6500</td><td>640.0242</td><td>95</td><td>2590</td><td>76.3095</td><td>36.5462</td><td>0</td><td>143.05</td></tr><tr><td>HGFN-PPO</td><td>1.25</td><td>396.3750</td><td>325.0006</td><td>70</td><td>1441</td><td>0.3423</td><td>1.5784</td><td>0</td><td>9.15</td></tr></table>

表 7 公共基准数据集上基于Makespan和RPI的Wilcoxon符号秩检验结果

Table 7 Results of Wilcoxon Signed-Rank Test by Makespan and RPI on Public Benchmarks

<table><tr><td rowspan="2">对比方法 (HGFN-PPO vs)</td><td colspan="3">Makespan</td><td colspan="3">RPI</td></tr><tr><td>p-value</td><td>是否显著(p≤0.05)</td><td>决策</td><td>p-value</td><td>是否显著(p≤0.05)</td><td>决策</td></tr><tr><td>DRL-D</td><td>0.00003790</td><td>是</td><td>拒绝原假设</td><td>0.00000379</td><td>是</td><td>拒绝原假设</td></tr><tr><td>HGS</td><td>0.00010802</td><td>是</td><td>拒绝原假设</td><td>0.00007144</td><td>是</td><td>拒绝原假设</td></tr><tr><td>DRL-A</td><td>0.00002696</td><td>是</td><td>拒绝原假设</td><td>0.00002701</td><td>是</td><td>拒绝原假设</td></tr><tr><td>FIFO</td><td>0.00000000</td><td>是</td><td>拒绝原假设</td><td>0.00000000</td><td>是</td><td>拒绝原假设</td></tr><tr><td>MOR</td><td>0.00000000</td><td>是</td><td>拒绝原假设</td><td>0.00000000</td><td>是</td><td>拒绝原假设</td></tr><tr><td>SPT</td><td>0.00000256</td><td>是</td><td>拒绝原假设</td><td>0.00000256</td><td>是</td><td>拒绝原假设</td></tr></table>

实验根据工件数量将20个工件划分为4组不同规模的生产任务实例,并分别进行调度测试.测试结果如表11所示.可以看出,本文所提方法在不同规模生产任务下均能够在较短时间内快速生成可行调度方案.这说明所提调度框架在柔性制造场景中具有良好的工程应用潜力,可为实际智能制造系统中的快速调度决策提供有效支持.

表 8 车间六类工序对应的可选机器  
Table8 Optional machines for the six processes in workshop

<table><tr><td>编号</td><td>工序</td><td>可选机器</td></tr><tr><td>1</td><td>激光切割</td><td>M1, M2, M3</td></tr><tr><td>2</td><td>火焰切割</td><td>M4, M5</td></tr><tr><td>3</td><td>钢板矫平</td><td>M6, M7</td></tr><tr><td>4</td><td>折弯</td><td>M8</td></tr><tr><td>5</td><td>铣削</td><td>M9, M10</td></tr><tr><td>6</td><td>钻孔</td><td>M11</td></tr></table>

表 9 车间机器之间的运输时间矩阵  
Table9 Travel time between machines in the workshop

<table><tr><td></td><td>0</td><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td><td>6</td><td>7</td><td>8</td><td>9</td><td>10</td><td>11</td></tr><tr><td>0</td><td>0</td><td>26</td><td>34</td><td>42</td><td>50</td><td>58</td><td>20</td><td>50</td><td>36</td><td>48</td><td>62</td><td>74</td></tr><tr><td>1</td><td>26</td><td>0</td><td>18</td><td>26</td><td>34</td><td>42</td><td>36</td><td>56</td><td>42</td><td>52</td><td>70</td><td>78</td></tr><tr><td>2</td><td>34</td><td>18</td><td>0</td><td>18</td><td>26</td><td>34</td><td>44</td><td>50</td><td>34</td><td>44</td><td>58</td><td>70</td></tr><tr><td>3</td><td>42</td><td>26</td><td>18</td><td>0</td><td>18</td><td>26</td><td>52</td><td>40</td><td>38</td><td>48</td><td>50</td><td>62</td></tr><tr><td>4</td><td>50</td><td>34</td><td>26</td><td>18</td><td>0</td><td>18</td><td>60</td><td>30</td><td>46</td><td>56</td><td>40</td><td>54</td></tr><tr><td>5</td><td>58</td><td>42</td><td>34</td><td>26</td><td>18</td><td>0</td><td>68</td><td>40</td><td>54</td><td>64</td><td>50</td><td>46</td></tr><tr><td>6</td><td>20</td><td>36</td><td>44</td><td>52</td><td>60</td><td>68</td><td>0</td><td>40</td><td>26</td><td>38</td><td>52</td><td>62</td></tr><tr><td>7</td><td>50</td><td>56</td><td>50</td><td>40</td><td>30</td><td>40</td><td>40</td><td>0</td><td>26</td><td>36</td><td>20</td><td>34</td></tr><tr><td>8</td><td>36</td><td>42</td><td>34</td><td>38</td><td>46</td><td>54</td><td>26</td><td>26</td><td>0</td><td>20</td><td>38</td><td>50</td></tr><tr><td>9</td><td>48</td><td>52</td><td>44</td><td>48</td><td>56</td><td>64</td><td>38</td><td>36</td><td>20</td><td>0</td><td>48</td><td>60</td></tr><tr><td>10</td><td>62</td><td>70</td><td>58</td><td>50</td><td>40</td><td>50</td><td>52</td><td>20</td><td>38</td><td>48</td><td>0</td><td>46</td></tr><tr><td>11</td><td>74</td><td>78</td><td>70</td><td>62</td><td>54</td><td>46</td><td>62</td><td>34</td><td>50</td><td>60</td><td>46</td><td>0</td></tr></table>

## 5 结论

本文针对FJSPT提出了一种融合GNN与DRL的端到端调度方法,实现了工序排序、机器分配与AGV调度的协同优化.通过异构图状态表示与图强化学习框架,所提方法能够有效刻画加工资源与物流资源之间的耦合关系,并直接从图结构状态中学习调度策略.实验结果表明,所提方法在不同规模基准算例上均能够获得较优的调度性能,验证了该方法的有效性.

表 10工件的工艺路线与加工时间  
Table10 The process route and processing time for jobs

<table><tr><td>工件编号</td><td>工艺路线</td><td>加工时间(30分钟)</td></tr><tr><td>1</td><td>3-1-3-4-5</td><td>0.83-3.63-0.83-1.27-2.6</td></tr><tr><td>2</td><td>3-2-3-4</td><td>0.83-3.63-0.83-1.27</td></tr><tr><td>3</td><td>3-2-3</td><td>0.83-7.39-0.83</td></tr><tr><td>4</td><td>3-1-3-4-6</td><td>0.83-10.49-0.83-1.47-4</td></tr><tr><td>5</td><td>2-5-6</td><td>1.83-4-5</td></tr><tr><td>6</td><td>1-6-5</td><td>1.83-4-5</td></tr><tr><td>7</td><td>1-5-6</td><td>1.64-4-5</td></tr><tr><td>8</td><td>2-3-5-6</td><td>1.64-4-5-4</td></tr><tr><td>9</td><td>3-1-3</td><td>0.83-5.71-0.83</td></tr><tr><td>10</td><td>3-1-3-4-5</td><td>0.83-10.49-0.83-1.47</td></tr><tr><td>11</td><td>3-5-1</td><td>0.83-6-11</td></tr><tr><td>12</td><td>3-2-3-4</td><td>0.83-10.23-0.83-1.96</td></tr><tr><td>13</td><td>2-4</td><td>3.77-0.63</td></tr><tr><td>14</td><td>1-4</td><td>3.77-0.63</td></tr><tr><td>15</td><td>3-5-1-3</td><td>0.83-8-25.56-0.83</td></tr><tr><td>16</td><td>3-2-3-4</td><td>0.83-16.44-0.83-3.65</td></tr><tr><td>17</td><td>1-6</td><td>2.12-0.72</td></tr><tr><td>18</td><td>3-1-3-6</td><td>0.83-10.23-0.83-1.96</td></tr><tr><td>19</td><td>3-2-3-5-6</td><td>0.83-10.23-0.83-1.97-1.8</td></tr><tr><td>20</td><td>3-1-3-4-6-5</td><td>0.83-10.23-0.83-1.98-1.8-1.97</td></tr></table>

表 11 生产任务实例的调度结果

Table11 Scheduling results for production tasks

<table><tr><td>算例</td><td>工件数</td><td>Makespan</td><td>时间(s)</td></tr><tr><td>算例A</td><td>5</td><td>31884</td><td>0.5</td></tr><tr><td>算例B</td><td>10</td><td>43224</td><td>1.08</td></tr><tr><td>算例C</td><td>15</td><td>65250</td><td>1.85</td></tr><tr><td>算例D</td><td>20</td><td>67994</td><td>2.02</td></tr></table>

此外,本文方法对于智能制造中生产与物流协同管理具有一定启示意义.所提出的端到端协同调度框架能够在统一决策过程中综合考虑加工资源与物流资源之间的耦合关系,从而降低设备等待与运输冲突带来的系统效率损失.该方法尤其适用于存在多设备、多运输资源以及复杂工艺约束的离散制造场景,例如柔性制造单元、自动化车间等.此外,基于图神经网络的状态表示方式具备较好的结构泛化能力,为后续面向动态订单、柔性扩产以及数字孪生车间的智能调度应用提供了潜在支持.

与此同时,本文方法仍存在一定局限性.一方面,基于图神经网络与深度强化学习的训练框架在大规模实例下仍存在较高的训练成本与推理开销,其计算效率与可扩展性仍有进一步提升空间.另一方面,本文主要关注加工与运输协同调度问题,在建模过程中未进一步考虑多AGV路径冲突、死锁避免及动态避碰等复杂运输过程约束. 因此, 如何在保证求解效率的同时进一步增强模型对复杂实际制造环境的适应能力, 仍是值得深入研究的问题.

未来研究可进一步拓展所提方法在复杂真实制造环境中的适用性. 一方面, 实际生产系统普遍存在新工件动态到达、订单变更以及机器或AGV故障等随机扰动, 后续工作可引入不确定性建模, 使调度策略能够在动态环境中持续自适应更新. 另一方面, 除完工时间外, 现代制造系统还需综合考虑能源消耗、设备利用率和交付准时性等多维性能指标, 未来可通过多目标强化学习或帕累托优化实现多目标协同优化.

## 参考文献:

[1] 蔡文柯, 李佳, 刘钢兵, 等. 基于端到端深度强化学习的动态柔性作业车间调度问题研究[J/OL]. 系统仿真学报, 2026: 1-14.

(Cai W K, Li J, Liu G B, et al. Dynamic Flexible Job Shop Scheduling Based on End-to-End Deep Reinforcement Learning[J]. Journal of System Simulation, 2026: 1-14.).

[2] 李瑞, 龚文引. 改进的基于分解的多目标进化算法求解双目标模糊柔性作业车间调度问题[J/OL]. 控制理论与应用, 2022, 39(1): 31. (Li R, Gong W Y. Improved decomposition-based multi-objective evolutionary algorithm for bi-objective fuzzy flexible job shop scheduling problem[J]. Control Theory & Applications, 2022, 39(1): 31.)

[3] QIN H, XIANG Y, HAN Y, 等. A knowledge region selection enhanced quality-diversity algorithm for real-world flexible job shop scheduling with Automated Guided Vehicles transportation[J/OL]. Engineering Applications of Artificial Intelligence, 2026, 164: 113352.

[4] CHEN R, WU B. Double deep Q-network based multi-objective optimization for flexible job shop scheduling problem with heterogeneous automatic guided vehicles[J/OL]. Expert Systems with Applications, 2026, 296: 128992.

[5] FONTES D B M M, HOMAYOUNI S M. Joint production and transportation scheduling in flexible manufacturing systems[J/OL]. Journal of Global Optimization, 2019, 74(4): 879–908.

[6] 郑小操, 龚文引. 改进人工蜂群算法求解模糊柔性作业车间调度问题[J/OL]. 控制理论与应用, 2020, 37(6): 1284.
(Zheng X C, Gong W Y. Improved artificial bee colony algorithm for fuzzy flexible job shop scheduling problem[J]. Control Theory & Applications, 2020, 37(6): 1284.)

[7] LYU X, SONG Y, HE C, 等. Approach to Integrated Scheduling Problems Considering Optimal Number of Automated Guided Vehicles and Conflict-Free Routing in Flexible Manufacturing Systems[J/OL]. IEEE Access, 2019, 7: 74909–74924.

[8] MENG L, CHENG W, ZHANG C, 等. Novel CP Models and CP-Assisted Meta-Heuristic Algorithm for Flexible Job Shop Scheduling Benchmark Problem With Multi-AGV[J/OL]. IEEE Transactions on Systems, Man, and Cybernetics: Systems, 2025, 55(11): 8455–8468.

[9] YANG S, MENG L, ULLAH S, 等. MILP Modeling and Optimization of Multi-Objective Three-Stage Flexible Job Shop Scheduling Problem With Assembly and AGV Transportation[J/OL]. IEEE Access, 2025, 13: 25369–25386.

[10] V SAGAR K, JERALD J. Real-time Automated Guided vehicles scheduling with Markov Decision Process and Double Q-Learning algorithm[J/OL]. Materials Today: Proceedings, 2022, 64: 279–284.

[11] JIANG T, SHANG C. A Q-learning-driven evolutionary algorithm for energy-aware flexible job shop scheduling with preventive maintenance and finite AGVs[J/OL]. Expert Systems with Applications, 2026, 307: 131024.

[12] PAN Z, WANG L, ZHENG J, 等. A Learning-Based Multipopulation Evolutionary Optimization for Flexible Job Shop Scheduling Problem With Finite Transportation Resources[J/OL]. IEEE Transactions on Evolutionary Computation, 2023, 27(6): 1590–1603.

[13] 陈仁胜, 吴斌, 闫飞一. 基于混合学习策略的可变速AGV与机器绿色集成调度[J/OL]. 控制与决策, 2024, 39(12): 3955–3963.
(Chen R S, Wu B, Yan F Y. Green integrated scheduling of variable-speed AGVs and machines based on hybrid learning strategy[J]. Control and Decision, 2024, 39(12): 3955–3963.)

[14] 杨媛媛, 胡蓉, 钱斌, 等. 深度强化学习算法求解动态流水车间实时调度问题[J/OL]. 控制理论与应用, 2024, 41(6): 1047-1055. (Yang Y Y, Hu R, Qian B, et al. Deep Reinforcement Learning For Real-Time Scheduling Of Dynamic Flow Shop[J]. Control Theory and Applications, 2024, 41(6): 1047-1055.)

[15] LIU R, PIPLANI R, TORO C. Deep reinforcement learning for dynamic scheduling of a flexible job shop[J/OL]. International Journal of Production Research, 2022, 60(13): 4049–4069.

[16] 孟繁威, 郭宏, 延小龙, 等. 基于多智能体强化学习求解柔性作业车间联合调度问题[J/OL]. 计算机集成制造系统, 2024: 1-29.

(Meng F W, Guo H, Yan X L, et al. Multi-Agent Reinforcement Learning For Integrated Scheduling Of Flexible Job Shop[J], Computer Integrated Manufacturing System, 2024: 1-29.)

[17] LI C, LIN L, QIU X, 等. Evolutionary experience-guided deep reinforcement learning for job shop scheduling with AGV transportation constraints in flexible manufacturing system[J/OL]. Computers & Industrial Engineering, 2025, 209: 111465.

[18] SHEN Y, ZHANG X, JIN T. Transformer-based multi-agent reinforcement learning for flexible job shop scheduling with AGVs[J/OL]. Applied Soft Computing, 2026, 193: 114899.

[19] LI Y, WANG Q, LI X, 等. Real-Time Scheduling for Flexible Job Shop With AGVs Using Multiagent Reinforcement Learning and Efficient Action Decoding[J/OL]. IEEE Transactions on Systems, Man, and Cybernetics: Systems, 2025, 55(3): 2120–2132.

[20] 黄宇晗, 张梓琪, 李贤, 等. 深度强化学习驱动的多尺度窗口异构图注意力框架解决分布式柔性作业车间调度问题[J/OL]. 控制理论与应用, 2026: 1-17. (Huang Y H, Zhang Z Q, Li X, et al. Deep reinforcement learning driven multi-scale window heterogeneous graph attention framework for distributed flexible job shop scheduling[J]. Control Theory & Applications, 2026: 1-17.)

[21] MOON S, LEE S, PARK K J. Graph-based Reinforcement Learning for Flexible Job Shop Scheduling with Transportation Constraints[C/OL]. IECON 2023-49th Annual Conference of the IEEE Industrial Electronics Society. 2023: 1–6.

[22] ZHANG M, WANG L, QIU F, 等. Dynamic scheduling for flexible job shop with insufficient transportation resources via graph neural network and deep reinforcement learning[J/OL]. Computers & Industrial Engineering, 2023, 186: 109718.

[23] REN F, LIU H, HUANG H, 等. Dynamic scheduling of flexible job-shop considering automatic guided vehicle transportation via deep reinforcement learning[J/OL]. Future Generation Computer Systems, 2026, 182: 108450.

[24] 杨晓宇, 韩玉艳, 王玉亭, 等. 融入流体松弛模型的决斗双深度Q网络求解动态多重柔性作业车间调度问题[J]. 控制理论与应用, 2025, 42(11): 2332-2340. (Yang X Y, Han Y Y, Wang Y T, et al. Dueling Double Deep Q-Network With Fluid Relaxation Model For Dynamic Flexible Job Shop Scheduling[J]. Control Theory and Applications, 2025, 42(11): 2332-2340.)

[25] 王艳红, 付威通, 张俊, 等. 基于改进近端策略优化算法的柔性作业车间调度[J/OL]. 控制与决策, 2025, 40(06): 1883-1891. (Wang Y H, Fu W T, Zhang J, et al. Flexible Job Shop Scheduling Based On Improved Proximal Policy Optimization[J]. Control and Decision, 2025, 40(06): 1883-1891.)

[26] SONG W, CHEN X, LI Q, 等. Flexible Job-Shop Scheduling via a Graph Neural Network and Deep Reinforcement Learning[J/OL]. IEEE Transactions on Industrial Informatics, 2023, 19(2): 1600–1610.

[27] VELI?KOVI? P, CUCURULL G, CASANOVA A, 等. Graph Attention Networks[A/OL]. arXiv, 2018.

[28] BRODY S, ALON U, YAHAV E. How Attentive are Graph Attention Networks?[A/OL]. arXiv, 2022.

[29] BRANDIMARTE P. Routing and scheduling in a flexible job shop by tabu search[J/OL]. Annals of Operations Research, 1993, 41(3): 157–183.

[30] HOMAYOUNI S M, FONTES D B M M. Production and transport scheduling in flexible job shop manufacturing systems[J/OL]. Journal of Global Optimization, 2021, 79(2): 463–502.

[31] DEROUSSI L, NORRE S. Simultaneous scheduling of machines and vehicles for the flexible job shop problem[C]. International conference on metaheuristics and nature inspired computing. Djerba Island Tunisia, 2010: 1–2.

[32] DOH H H, YU J M, KIM J S, 等. A priority scheduling approach for flexible job shops with multiple process plans[J/OL]. International Journal of Production Research, 2013, 51(12): 3748–3764.

[33] MONTAZERI M, VAN WASSENHOVE L N. Analysis of scheduling rules for an FMS[J/OL]. International Journal of Production Research, 1990, 28(4): 785–802.

[34] WANG Y, WANG R, SUN J, 等. Attention enhanced reinforcement learning for flexible job shop scheduling with transportation constraints[J/OL]. Expert Systems with Applications, 2025, 282: 127671.

## 作者简介：

侯亚群 硕士研究生, 目前研究方向为智能优化调度, E-mail: houyaqun0908@163.com;

王玉亭 副教授, 目前研究方向为数学建模、智能优化算法、软件开发, E-mail: wangyuting@lcu-cs.com;

韩玉艳 副教授, 目前研究方向为进化计算、多目标优化、流水车间调度, E-mail: hanyuyan@lcu-cs.com;

罗涛 浪潮云洲工业互联网有限公司, 目前研究方向为工业物联网、工业大数据治理、AI智能等, E-mail: 412288853@qq.com;

陈庆达 研究员, 目前研究方向: 智能计算理论及应用, 复杂工业过程优化, E-mail: qdchen@imu.edu.cn.