![](images/491af8e445c85a8328a883ceb35885008363686b2fa10e39956db0ba27ac9d03.jpg)



中国机械工程China Mechanical EngineeringISSN1004-132X,CN42-1294/TH


# 《中国机械工程》网络首发论文

题目：基于Q-learning改进果蝇算法的针织车间AGV资源配置优化 

作者： 李西兴，刘晨明，王际鹏，汪俊亮，杨妍，李立军 

网络首发日期： 2026-03-23 

引用格式： 李西兴，刘晨明，王际鹏，汪俊亮，杨妍，李立军．基于Q-learning改进果蝇算法的针织车间AGV资源配置优化[J/OL]．中国机械工程. https://link.cnki.net/urlid/42.1294.th.20260320.1734.016 

![](images/87c6171f5e01f2e9488090bd04956c2d82e636c7745eb14705d407f65c0555f5.jpg)


![](images/09e0ae38060fd2c56c81494e5738d4dcfe879a00fd3d7987c5597d3a2eb25364.jpg)


网络首发：在编辑部工作流程中，稿件从录用到出版要经历录用定稿、排版定稿、整期汇编定稿等阶段。录用定稿指内容已经确定，且通过同行评议、主编终审同意刊用的稿件。排版定稿指录用定稿按照期刊特定版式（包括网络呈现版式）排版后的稿件，可暂不确定出版年、卷、期和页码。整期汇编定稿指出版年、卷、期、页码均已确定的印刷或数字出版的整期汇编稿件。录用定稿网络首发稿件内容必须符合《出版管理条例》和《期刊出版管理规定》的有关规定；学术研究成果具有创新性、科学性和先进性，符合编辑部对刊文的录用要求，不存在学术不端行为及其他侵权行为；稿件内容应基本符合国家有关书刊编辑、出版的技术标准，正确使用和统一规范语言文字、符号、数字、外文字母、法定计量单位及地图标注等。为确保录用定稿网络首发的严肃性，录用定稿一经发布，不得修改论文题目、作者、机构名称和学术内容，只可基于编辑规范进行少量文字的修改。 

出版确认：纸质期刊编辑部通过与《中国学术期刊（光盘版）》电子杂志社有限公司签约，在《中国学术期刊（网络版）》出版传播平台上创办与纸质期刊内容一致的网络版，以单篇或整期出版形式，在印刷出版之前刊发论文的录用定稿、排版定稿、整期汇编定稿。因为《中国学术期刊（网络版）》是国家新闻出版广电总局批准的网络连续型出版物（ISSN 2096-4188，CN 11-6037/Z），所以签约期刊的网络版上网络首发论文视为正式出版。 

# 基于 Q-learning 改进果蝇算法的针织车间 AGV 资源配置优化

李西兴 $^{1,2,6}$ 刘晨明 $^{1,2}$ 王际鹏 $^{1,2*}$ 汪俊亮 $^{3}$ 杨妍 $^{4,5}$ 李立军 $^{6}$ 1.湖北工业大学机械工程学院，武汉，430068 

2. 湖北工业大学现代制造质量工程湖北省重点实验室，武汉，430068  
3. 东华大学纺织工业人工智能技术教育部工程研究中心，上海，201620  
4. 北京科技大学智能科学与技术学院，北京，100083  
5. 北京科技大学智能仿生无人系统教育部重点实验室，北京，100083  
6. 宁波慈星股份有限公司，慈溪，315336 

摘要：自动导引车(AGV)是针织车间数字化转型的重要组成部分。由于纱线种类和数量繁多且需同时供应，导致 AGV 资源利用率不足，制约产能扩张。为了提高产能，本文提出考虑异构 AGV 和机器顺序相关准备时间的资源配置优化问题，构建以最小化最大完工时间为目标的 AGV 资源配置优化模型，并采用基于 Q-learning 改进果蝇优化算法(QFOA)求解。首先，构建基于任务的三层编码方案，采用四种不同的初始化策略来提高初始种群质量。其次，将 Q-learning 与嗅觉搜索相结合，提升算法的局部搜索能力；在视觉搜索阶段引入种群合并策略，以增强全局搜索能力。最后，通过消融实验、对比实验和案例分析，对 QFOA 及其相关策略的有效性进行验证。案例分析结果表明，QFOA 与 FOA 相比完工时间减少 10.45%，与 QABC 相比减少 4.42%。在不同规模的算例中，QFOA 均表现出较高的稳定性和优越性。 

关键词：针织车间；AGV；资源配置；Q-learning；果蝇优化算法 

中图分类号：TS183.92 

文献标志码：A 

# Optimization of AGV resource allocation in knitting workshops by using Q-learning-based fruit fly algorithm

LI Xixing $^{1,2,6}$ LIU Chenming $^{1,2}$ WANG Jipeng $^{1,2*}$ WANG Junliang $^{3}$ YANG Yan $^{4,5}$ LI Lijun $^{6}$ 

1. School of Mechanical Engineering, Hubei University of Technology, Wuhan, 430068  
2. Hubei Key Laboratory of Modern Manufacturing Quantity Engineering, Hubei University of Technology, Wuhan, 430068 

3. Engineering Research Center of Artificial Intelligence for Textile Industry Ministry of Education, Donghua University, Shanghai, 201620 

4. School of Intelligence Science and Technology, University of Science and Technology Beijing, Beijing, 100083  
5. Key Laboratory of Intelligent Bionic Unmanned Systems, Ministry of Education, University of Science and Technology Beijing, Beijing, 100083  
6. Ningbo Cixing Co., Ltd., Cixi, 315336 

Abstract: The Automated Guided Vehicle (AGV) system is a critical component in the digital transformation of knitting workshops. Due to the diverse types and quantities of yarn that must be supplied simultaneously, under utilization of AGV resources limits the expansion of production capacity. To enhance production capacity, this paper proposes an optimization problem for resource allocation that accounts for heterogeneous AGVs and machine setup times associated with processing sequences. A Q-learning-based fruit fly optimization algorithm (QFOA) is introduced to minimize the makespan. First, a task-oriented three-layer encoding scheme is constructed, and four distinct initialization strategies are employed to improve the quality of the initial population. Next, the Q-learning algorithm is integrated into the smell search stage to enhance the algorithm's local search capability. Additionally, a population merging strategy is introduced in the visual search stage to improve global search performance. Finally, the effectiveness of the proposed QFOA and its associated strategies is comprehensively validated through comparative experiments, ablation studies, and a practical case study. The case study results demonstrate that QFOA reduces the makespan by $10.45\%$ compared to FOA and by $4.42\%$ compared to QABC. Across test cases of varying sizes, QFOA consistently exhibits high stability and superior performance.

Keywords: knitting workshops; AGV; resource allocation; Q-learning; fruit fly optimization algorithm 

## 0 引言

随着针织业数字化转型，个性化消费需求推动行业快速发展[1]。在订单驱动的生产模式下，针织生产面临小批量、多品种和高时效的挑战。小批量生产导致订单规模小且种类繁多，纱线规格差异大，且需精确比例混纺。针织车间中的自动导引车(Automated Guided Vehicle, AGV)需同步配送多种原料纱并严格控制投料顺序，以保障针织横机的正常运行[2]。此外，原料纱的投料过程必须在2-3分钟内完成，以满足针织生产的高时效要求。AGV资源配置需确保每次配送的时效性，且与作业节拍精确协同。然而，同质AGV难以满足生产需求，忽略AGV的异构性会导致调度偏差。此外，针织横机有更换纱线和穿线等操作，在加工前需要准备时间，即顺序相关准备时间。因此，本文提出考虑异构AGV和顺序相关准备时间的AGV资源配置问题，旨在优化AGV与机器配置的同时，最小化完工时间。 

目前，许多学者在资源配置领域已取得一些进展。董玉龙等[3]基于博弈论建立飞机总装物流配送系统资源配置模型，考虑因产品尺寸和装配工艺差异引起的物料配送延迟。郭笛等[4]提出基于FlexSim平台的仿真方法，解决智慧仓库同质AGV配置不合理导致作业效率低的问题。Cheng等[5]聚焦智能仓库货品存取问题，并提出融合协同调度策略的改进遗传算法。Mumtaz等[6]在定制印刷电路板装配线的研究中，提出同时考虑工位负载均衡与同质AGV资源配置问题。陈炫锐等[7]考虑平均任务周期与同质AGV数量约束，构建资源配置模型。张维维等[8]考虑同质AGV与机器资源配置问题，建立机器-AGV双层资源配置模型。胡晓阳等[9]引入“先到先得”启发式规则，为每个运输任务分配最合适的AGV。Wen等[10]综合考虑机器、作业和AGV三类约束，采用改进的NSGA-II算法求解多目标资源配置问题。陈魁等[11]提出混合离散粒子群算法来解决机器与同质AGV资源配置问题。Yuan等[12]提出改进双重深度Q网络算法，解决同质AGV资源配置问题。Zhang等[13]基于深度强化学习方法，解决机器与AGV资源配置问题。Yao等[14]考虑同质AGV资源的有限性，提出基于深度Q网络的多目标模因算法，旨在最小化最大完工时间和能耗。Wang等[15]解决装配车间中有限AGV与装配站资源配置问题。现有研究大多集中于同质AGV的资源配置问题，涉及异构AGV资源配置的研究仍较为稀缺。 

Li等[16]针对多任务并行场景下夹具冲突问题，采用改进遗传算法解决加工夹具资源配置难题。Liu等[17]进一步研究了同时考虑机器-夹具-托盘的资源配置问题。郑建风等[18]采用融合排队论和合作博弈论的三段优化策略，优化港口的泊位资源配置。李兴春等[19]构建双层模型，以解决岸桥同质AGV的资源配置。Liu等[20]以最小化最大完工时间为目标，建立机器与同质AGV双资源配置模型。Yunusoglu等[21]考虑机器资源受限，建立以最小化最大完工时间为目标的资源配置模型。Wan等[22]探讨制造资源分配与需求预测问题，通过预测不同周期所需的制造资源数量，并制定最优配置方案。Guo等[23]针对复杂航空航天产品装配中的多资源约束问题，提出可重构制造单元车间的资源配置方法。Mlekusch等[24]在丝网印刷场景下，提出同时考虑机器与工人双资源约束的资源配置问题。Barak等[25]也考虑了类似的机器与工人双资源约束问题。Li等[26]在船舶平面分段装配生产中，提出同时考虑工人和配件双重约束的资源配置问题。Zheng等[27]提出改进的FOA算法，采用多种群机制，并根据问题特征设计搜索算子，以解决有限资源和顺序相关准备时间的资源配置问题。Guo等[28]设计嗅觉搜索机制，实验证明FOA在求解具有顺序相关准备时间的资源配置问题具有较好效果。虽然许多研究已考虑机器资源，但较少研究关注顺序相关准备时间的影响。 

综上所述，现有AGV资源配置研究较少同时考虑异构AGV和机器相关准备时间。针织车间中的异构AGV需要同步配送多类型纱线，并满足物料完整性和配送时序要求。本文在实际约束下，提出同时考虑异构AGV和机器顺序相关准备时间的资源配置问题，构建以最小化最大完工时间为目标的AGV资源配置模型，并提出基于Q-learning改进的果蝇算法(Q-learning-based Fruit Fly Optimization Algorithm, QFOA)。填补了针织车间场景下的AGV资源配置研究空白，具有理论创新和实际应用价值。 

## 1 问题描述与模型构建

## 1.1 问题描述

针织车间中运输任务主要由AGV完成，各运输任务紧密衔接，保障针织车间的生产效率。第一类任务为原材料运输，根据订单信息确定所需纱线种类，并将纱线配送任务分配给带有末端机械臂的复合AGV，运输至目标横机。第二类任务为半成品中转，粗加工完成的半成品由带有末端机械臂的复合AGV送至质检区，经过照灯、缝补、藏头、水洗和整烫等步骤，最后打包为成品。第三类任务是成品入库，成品由半潜式AGV运输至成品库，完成整个生产流程。 

针织车间 AGV 资源配置问题可表述为：在已知生产任务、纱线库存、AGV 实时状态及工件工艺路径的前提下，依据订单需求确定 AGV 的配置方案，从而确保 AGV 高效完成纱线配送任务，同时兼顾工件转运以及成品入库，提升整体生产效率。有 n 个待加工的工件位于原料区，每个工件 i 包含 $m_{i}$ 道工 序。车间内配备 $n$ 台针织横机和 $x$ 台运输能力各异的AGV。由于纱线的规格存在差异，AGV和纱线可以划分为 $s$ 类。任一纱线仅能选择同一类别中的AGV进行运输，每一个类别中的AGV数量 $a_{s} \geq 1$ 。AGV在车间内运输任务的流程如图1所示。 

![](images/53c61861f93933caedb27f76b67219a8205b889c1e49e033fd465d2c09b67cdd.jpg)



图 1 针织车间布局示意图



Fig.1 Knitting workshop layout diagram


## 1.2 问题假设

(1) 在零时刻，所有机器和AGV都是可用的，AGV和工件均在原料区； 

(2) 工件开始加工时从原料区运输, 加工完成后运回成品区, 即代表加工完成; 

(3) 同一工件的工序之间存在先后加工次序; 

(4) 在同一时间，AGV只能运输一个工件，每个工件只能由一台AGV运输； 

(5) 任务一旦开始在完成前不允许中断； 

(6) 已经完成运输任务的AGV在原始位置等待下一运输任务的发布; 

(7) 每台针织横机的缓存区的容量足够，可以容纳需要的工件； 

(8) 所有AGV和机器均处于正常工作状态; 

(9) 原料区、生产区、质检区和成品区的运输距离已知，不考虑路径冲突。 

## 1.3 符号及变量定义


表 1 符号定义



Tab.1 Symbol definitions


<table><tr><td>符号</td><td>定义</td></tr><tr><td>i</td><td>工件索引,<eq>i \in \{1,2,3,\cdots,m\}</eq>,<eq>m \in Z^{+},Z^{+}</eq>为正整数集合</td></tr><tr><td>j</td><td>工序索引,<eq>j \in \{1,2,3,\cdots,m_{i}\}</eq>,<eq>m_{i} \in Z^{+}</eq></td></tr><tr><td>k</td><td>机器索引,<eq>k \in \{0,1,2,\cdots,n\}</eq>,<eq>n \in Z^{+}</eq></td></tr><tr><td>l</td><td>AGV 索引,<eq>l \in \{1,2,\cdots,x\}</eq>,<eq>x \in Z^{+}</eq></td></tr><tr><td><eq>J_{i}</eq></td><td>表示第i个工件</td></tr><tr><td><eq>O_{ij}</eq></td><td>第i个工件的第j道工序</td></tr><tr><td><eq>M_{k}</eq></td><td>第k台加工机器,<eq>M_{0}</eq>表示成品仓</td></tr><tr><td><eq>A_{l}</eq></td><td>第l台 AGV</td></tr><tr><td><eq>P_{ij}</eq></td><td><eq>O_{ij}</eq>的加工任务</td></tr><tr><td><eq>T_{ij}</eq></td><td><eq>O_{ij}</eq>的运输任务</td></tr><tr><td><eq>J_{si}</eq></td><td>第i个工件对应的类别,<eq>J_{si} \in \{1,2,\cdots,s\}</eq></td></tr><tr><td><eq>A_{sl}</eq></td><td>第l台 AGV 对应的类别,<eq>A_{sl} \in \{1,2,\cdots,s\}</eq></td></tr><tr><td><eq>T_{ij}^{RS}</eq></td><td><eq>P_{ij}</eq>准备时间开始的时间</td></tr><tr><td><eq>T_{ii}^{RE}</eq></td><td><eq>P_{ij}</eq>准备时间结束的时间</td></tr><tr><td><eq>T_{ij}^{PS}</eq></td><td><eq>P_{ij}</eq>加工时间开始的时间</td></tr><tr><td><eq>T_{ij}^{PE}</eq></td><td><eq>P_{ij}</eq>加工时间结束的时间</td></tr><tr><td><eq>M_{ij}</eq></td><td><eq>P_{ij}</eq>分配的机器编号</td></tr><tr><td><eq>A_{ij}</eq></td><td><eq>T_{ij}</eq>分配的AGV编号</td></tr><tr><td><eq>T_{ij}^{US}</eq></td><td><eq>T_{ij}</eq>空载运输的开始时间</td></tr><tr><td><eq>T_{ij}^{UE}</eq></td><td><eq>T_{ij}</eq>空载运输的结束时间</td></tr><tr><td><eq>T_{ij}^{LS}</eq></td><td><eq>T_{ij}</eq>负载运输的开始时间</td></tr><tr><td><eq>T_{ij}^{LE}</eq></td><td><eq>T_{ij}</eq>负载运输的结束时间</td></tr><tr><td><eq>RT_{i'j}^{M_{ij}}</eq></td><td>加工任务的准备时间</td></tr><tr><td><eq>AM_{ij}^{US}</eq></td><td><eq>T_{ij}</eq>空载的起点机器</td></tr><tr><td><eq>AM_{ij}^{UE}</eq></td><td><eq>T_{ij}</eq>空载的终点机器</td></tr><tr><td><eq>AM_{ij}^{LS}</eq></td><td><eq>T_{ij}</eq>负载的起点机器</td></tr><tr><td><eq>AM_{ij}^{LE}</eq></td><td><eq>T_{ij}</eq>负载的终点机器</td></tr><tr><td><eq>DT_{ijl}</eq></td><td><eq>T_{ij}</eq>在<eq>A_l</eq>上的运输时间</td></tr><tr><td><eq>PT_{ijk}</eq></td><td><eq>P_{ij}</eq>在<eq>M_k</eq>上的加工时间</td></tr><tr><td><eq>C_i</eq></td><td>工件i的完成时间</td></tr><tr><td>L</td><td>一个足够大的常数,用于松弛约束、激活特定约束条件</td></tr></table>

表 2 决策变量 


Tab.2 Decision variables


<table><tr><td>决策变量</td><td>定义</td></tr><tr><td><eq>\delta_{ij}</eq></td><td>等于1表示任务<eq>T_{ij}</eq>存在,否则为0</td></tr><tr><td><eq>X_{ijk}</eq></td><td>等于1表示任务<eq>P_{ij}</eq>在<eq>M_k</eq>上加工,否则为0</td></tr><tr><td><eq>Y_{ijl}</eq></td><td>等于1表示任务<eq>T_{ij}</eq>在<eq>A_l</eq>上运输,否则为0</td></tr><tr><td><eq>p_{ij,bc}^k</eq></td><td>等于1表示任务<eq>P_{bc}</eq>早于<eq>P_{ij}</eq>在<eq>M_k</eq>上加工,否则为0</td></tr><tr><td><eq>q_{ij,bc}^l</eq></td><td>等于1表示任务<eq>T_{bc}</eq>早于<eq>T_{ij}</eq>在<eq>A_l</eq>上运输,否则为0</td></tr><tr><td><eq>L_{ijl}^T</eq></td><td>等于1表示工件<eq>J_i</eq>第j个运输任务可由第l类AGV运输,否则为0</td></tr><tr><td><eq>L_{ijk}^M</eq></td><td>等于1表示工件<eq>J_i</eq>第j道工序可由<eq>M_k</eq>加工,否则为0</td></tr></table>

## 1.4 模型建立

针织车间AGV资源配置问题受机器、AGV和任务数量的影响，具有较大的不确定性。本文的目标是根据不同的任务数量确定最佳AGV配比，以最小化最大完工时间。通过优化任务分配、机器选择和AGV选择，有效缩短完工时间，以提升针织车间生产效率。 

## 1.4.1 目标函数

根据前文分析，目标函数确定为最小化最大完工时间，如式(1)所示。 

$$
\min C _ {\max} = \min \left(\max _ {i = 1, 2, \dots , m} C _ {i}\right)
$$

## 1.4.2 约束条件

(1) 

$$
Y _ {i j l} \leq L _ {i j l} ^ {T}\tag{2}
$$

$$
T _ {i j} ^ {P S} \geq T _ {i (j - 1)} ^ {P E}\tag{3}
$$

$$
T _ {i j} ^ {L S} \geq T _ {i (j - 1)} ^ {L E}\tag{4}
$$

$$
X _ {i j k} \leq L _ {i j k} ^ {M}\tag{5}
$$

$$
\sum_ {k} ^ {n} X _ {i j k} = 1\tag{6}
$$

$$
M _ {i j} = \sum_ {k = 1} ^ {n} X _ {i j k} \bullet k\tag{7}
$$

$$
T _ {i j} ^ {P E} \geq T _ {i j} ^ {P S} + \sum_ {k = 1} ^ {n} X _ {i j k} \bullet P T _ {i j k}\tag{8}
$$

$$
\delta_ {i j} \leq L \bullet \left(2 - X _ {i j k} - X _ {i (j - 1) k}\right)\tag{9}
$$

$$
\delta_ {i j} \leq 1 - L \bullet \left(2 - X _ {i j k} - X _ {i (j - 1) k ^ {\prime}}\right), k \neq k ^ {\prime}
$$

$$
\sum_ {l = 1} ^ {a} Y _ {i j k} = \delta_ {i j}\tag{10}
$$

(11) 

$$
A _ {i j} = l \bullet \sum_ {l} ^ {a} Y _ {i j k}\tag{12}
$$

$$
A M _ {i j} ^ {U S} = M _ {i ^ {\prime} j ^ {\prime}}\tag{13}
$$

$$
A M _ {i j} ^ {U E} = M _ {i (j - 1)}\tag{14}
$$

$$
T _ {i j} ^ {U S} \geq \delta_ {i j} \bullet \left[ T _ {b c} ^ {L E} - L \left(1 - q _ {i j, b c} ^ {l}\right) \right] + (1 - \delta_ {i j}) \bullet T _ {i (j - 1)} ^ {P E}\tag{15}
$$

$$
T _ {i j} ^ {U E} = T _ {i j} ^ {U S} + \delta_ {i j} \bullet D T _ {A _ {i j}, A M _ {i j} ^ {U S}, A M _ {i j} ^ {U E}}\tag{16}
$$

$$
A M _ {i j} ^ {L S} = A M _ {i j} ^ {U E}\tag{17}
$$

$$
A M _ {i j} ^ {L E} = M _ {i j}\tag{18}
$$

$$
T _ {i j} ^ {L S} \geq T _ {i j} ^ {U E}\tag{19}
$$

$$
T _ {i j} ^ {L S} \geq T _ {i, j - 1} ^ {P E}\tag{20}
$$

$$
T _ {i j} ^ {L E} = T _ {i j} ^ {L S} + \delta_ {i j} \bullet D T _ {A _ {i j}, A M _ {i j} ^ {L S}, A M _ {i j} ^ {L E}}\tag{21}
$$

$$
T _ {i j} ^ {R S} \geq T _ {b c} ^ {P E} - L \left(1 - p _ {i j, b c} ^ {k}\right)\tag{22}
$$

$$
T _ {i j} ^ {R E} = T _ {i j} ^ {R S} + R T _ {i ^ {\prime} j} ^ {M _ {i j}}\tag{23}
$$

$$
T _ {i j} ^ {P S} \geq T _ {i j} ^ {S E}\tag{24}
$$

$$
T _ {i j} ^ {P S} \geq T _ {i j} ^ {L E}\tag{25}
$$

其中，式(2)表示同一种类AGV运输对应种类工件。式(3)和(4)表示每个工件的加工和运输任务的开始时间不得早于上一工件的结束时间。式(5)和(6)表示每个工件的加工任务只能在一台机器上完成。式(7)表示当前加工任务所在的机器编号。式(8)表示加工任务的结束时间不得早于加工任务的开始时间和加工任务的持续时间。式(9)和(10)表示运输任务仅能在同一工件的相邻加工机器编号不相同时存在。式(11)和(12)表示当运输任务存在时，需要选择AGV并且完成运输任务的AGV编号。式(13)和(14)表示AGV空载运输的起点和终点机器。式(15)和(16)表示同一台AGV上运输任务的先后顺序，空载运输的开始时间要早于结束时间。式(17)和(18)表示同一台AGV负载运输起点和终点。式(19)、(20)和(21)表示 $T_{ij}$ 负载运输开始时间和结束时间。式(22)和(23)表示加工顺序相关准备的开始和结束时间，且同一台机器上加工任务的先后顺序约束。式(24)和(25)表示加工任务的开始时间不得早于运输任务的结束时间和上一加工任务的结束时间。 

## 2 基于Q-learning改进果蝇优化算法

传统的进化算法存在早熟问题，且缺乏有效的自适应搜索机制，难以有效解决针织车间AGV资源配置问题。FOA具有参数少、结构简单、易于实现和强大的全局搜索能力，但在解决复杂问题时存在一定局限性。因此，本文提出一种基于Q-learning的改进果蝇优化算法(QFOA)。QFOA采用基于任务的三层编码方案，并引入四种初始化策略，以提高初始种群的质量。在嗅觉搜索阶段，引入Q-learning自适应选择最优的邻域搜索策略，改善探索与利用之间的平衡。此外，在视觉阶段采用了种群合并机制。这些改进可有效提升QFOA的收敛速度和求解精度。 

## 2.1 QFOA总体流程

QFOA的运作流程如图2所示，具体步骤如下： 

Setp1：采用四种策略生成初始种群 $(Ps)$ 

Step2：在嗅觉搜索阶段，每个果蝇个体利用Q-learning选择邻域结构并生成新解； 

Step3：将嗅觉搜索阶段产生的新种群与原始种群合并，并根据适应度值按降序排序，选取前 $P_{s}$ 个个体组成新的种群； 

Step4：重复执行Step2~Step3，直至满足算法的终止条件并输出最优解。 

## 2.2 编码

针织车间AGV资源配置问题包括加工任务排序、机器分配、运输任务排序和AGV分配四个子问题。现有研究的编码方式一般采用基于工序“运输任务和加工任务捆绑”的任务-机器-AGV三层编码方式，在半主动解码的情况下不会出现工件先运输后加工的情况，无法覆盖所有的解空间。为弥补这一缺陷，本文设计了基于任务的任务-机器-AGV三层编码方式来解决运输任务和加工任务捆绑问题。 

![](images/df009a7fc46395b5c3a5e766441cb5a83a7f0751d6d897df2fd72a191c1d000d.jpg)



图2 QFOA流程图



Fig.2 QFOA flowchart


任务层(Ts)用于确定运输任务和加工任务排序，工件 $J_{i}$ 的第h次出现代表工件 $J_{i}$ 的第h个任务。若h为奇数，则该任务为工件 $J_{i}$ 的第 $(h+1)/2$ 个运输任务，用 $T_{i,(h+1)/2}$ 表示；若h为偶数，则该任务为工件 $J_{i}$ 的第h/2个加工任务，用 $P_{i,h/2}$ 表示。机器层(Ms)的编码对应每个加工任务 $\{P_{11},P_{12},\cdots\}$ 所选的机器编号，其中0表示虚拟加工任务的机器编号，即成品入库。AGV层(As)的编码对应每个运输任务 $\{T_{11},T_{12},\cdots\}$ 对应的AGV编号。 

图3为编码示意图，Ts层的第2个基因表示运输任务 $T_{II}$ ，第4个表示加工任务 $P_{II}$ ；Ms层的第一个基因表示 $P_{II}$ 在 $M_{2}$ 上加工；As层中的第1个基因表示 $T_{II}$ 选择 $A_{I}$ 运输。 

![](images/0035cd684e9d65fc986821de82c833aafc73178a1cbc28f0df26b0c68e2c8fb2.jpg)



图3 编码示意图



Fig.3 Encoding diagram


## 2.3 解码

为提高求解效率，采用主动解码策略，充分利用任务间的逻辑关系，降低AGV空闲与等待时间。具体解码步骤如下： 

Setp1：根据任务层编码Ts获取待解码的任务顺序，其中Ts包含所有的加工任务和运输任务。 

Step2：从任务层编码Ts中的第一个任务开始，按顺序逐个取出任务，记作当前任务Tc。若当前任务为加工任务 $P_{ij}$ ，则根据机器层编码Ms指定的机器进行加工；若当前任务为运输任务 $T_{ij}$ ，则根据AGV层编码As指定的AGV进行运输。 

Step3：识别当前任务 $Tc$ 所在的设备的任务队列，找到所有可能的插入位置，形成候选插入位置集合。对于每一个位置，判断前插的可能性：对于加工任务 $P_{ij}$ 需要满足机器约束、工序约束和相关准备的约束；对于运输任务 $T_{ij}$ ，需要满足AGV类型约束，空载与负载运输时间约束。 

Step4：在所有满足前插条件的候选位置中，选择最早能完成当前任务的位置。若多个位置具有相同完成时间，则进一步考虑设备的负载均衡，选择负载较轻的位置。将当前任务 $Tc$ 插入选定位置，并更新设备任务队列。 

Step5：每插入一个任务后，实时更新任务对应设备的时间安排；基于更新后的任务队列，重新计算包括加工任务准备时间、加工时间、运输任务的空载时间与负载时间等的完整任务序列；记录当前的完工时间。 

Step6：重复Step2至Step5，依次处理任务层编码Ts中的所有任务，直到所有任务完成前插调度；当任务层编码Ts中的所有任务均完成解码后，输出最终的任务安排方案，并计算最小的完工时间。 

## 2.4 种群初始化

种群初始化的质量对算法求解过程具有较大影响。结合针织车间生产特点，为提高初始种群的质量和多样性，且避免产生非法解，本文在初始化种群阶段提出四种初始化策略。每种策略占种群的 $25\%$ 。这一设置参考了文献[29]中类似的比例，以保证种群在初始阶段能够覆盖不同的解空间，同时提高算法的搜索效率和解的质量。四种初始化策略如下： 

任务排序初始化(IS1): 所有任务按照最早开始时间进行升序排序。 

机器选择初始化(IS2): 根据各任务的加工需求, 从可用的机器中优先选择加工时间较短的机器, 同时确保机器负载均衡, 避免任务延迟。 

AGV选择初始化(IS3): 优先安排最早开工时间的AGV, 并选择同类AGV安排。 

随机初始化(IS4)：对任务顺序进行随机排序，为每个加工任务随机分配机器，并为每个运输任务随机分配AGV。 

## 2.5 嗅觉搜索

嗅觉搜索作为FOA的核心步骤，果蝇个体通过邻域搜索找到潜在解。考虑针织车间AGV资源配置问题的特点，本文提出五种邻域结构，结合Q-learning机制，为每个果蝇个体选择更合适的邻域结构，以找到更好的解。 

针织车间AGV资源配置问题是以最小化最大完工时间为目标，通过上述编码、解码阶段可以看出，影响最小化最大完工时间的主要因素是任务排序和AGV分配。因此，主要是针对任务排序和AGV分配来设计邻域结构。在QFOA中，引入五个邻域结构以生成邻域解，提高QFOA嗅觉阶段的寻优能力。第一种是针对AGV层，包括N1：AGV互换；N2：AGV随机插入；N3：AGV重新分配。第二种是针对任务层，包括N4：任务互换；N5：任务重新分配。五种邻域结构示意图如图4所示。 

AGV整体互换(N1)：在AGV层随机选择两个位置点，将该位置前后部分进行互换，目的是改变AGV的执行顺序。 

AGV随机插入(N2)：随机选择两个位置点，然后交换这两个位置上的AGV。能够模拟AGV执行任务的顺序，帮助种群在搜索空间中更广泛地探索可能的解。 

AGV重新分配(N3): 在AGV层随机选取一个位置, 然后用一个从1到AGV总数大小的随机数替换原来的值。 

任务互换(N4)：随机选择两个任务点，并交换两个任务点包含的元素整体互换，从而改变任务的处理顺序。 

任务重新分配(N5)：选取当前任务排序Ts与当前最优任务排序 $T_{best}$ 进行交叉操作，生成一个与Ts长度相等的概率矩阵R。若R中的值若小于概率d，则对应任务保留至下一代，其余位置由 $T_{best}$ 填充。 

![](images/65cac001e06993c05e2066207dba3a5d56887859790410cec59467136f2a735c.jpg)



N1 AGV整体互换


![](images/d5fe405745496e3109d47f3b0ac1593d19294e85da73856e922361977086f0e3.jpg)



N2 AGV随机插入



N5 任务重新分配


![](images/949188859c10c5f8cba9a8e2daaa00958dde81997b90411683ca70faf804757d.jpg)



图4 邻域结构示意图



Fig.4 Neighborhood structure diagram


## 2.6 基于Q-learning的邻域结构自适应选择

Q-learning是一种经典的强化学习算法，其核心思想是构建 $Q$ 表，并存储各状态-动作对的 $Q$ 值，随后根据 $Q$ 值选择能够获得最大回报的动作。用 $Q(s, a)$ 表示在状态 $s$ 下执行动作 $a$ 所获得的期望回报，则智能体通过环境反馈的奖励来优化其策略，该原理的示意图如图5所示。其中， $Q$ 值的计算如式(26)所示。 

$$
Q \left(s _ {t}, a _ {t}\right) = Q \left(s _ {t}, a _ {t}\right) + \alpha \left[ R _ {t} + \gamma \max \left(Q \left(s _ {t + 1}, a\right)\right) - Q \left(s _ {t}, a _ {t}\right) \right]\tag{26}
$$

在式(26)中， $s_{t}$ 和 $a_{t}$ 分别表示 t 时刻的状态和所选的动作； $R_{t}$ 表示智能体在 t 时刻执行动作 $a_{t}$ 后获得的奖励值， $\max\left(Q(s_{t+1},a)\right)$ 表示在状态 $s_{t+1}$ 下 Q 表中对应的最大 Q 值； $\alpha$ 是学习率， $\gamma$ 是折扣因子。 

![](images/e008eeff6b257b307ace922d2f48068fe5a5763759fa2190d0fe933dbc20ff9a.jpg)



图5 QFOA中的Q-learning示意图



Fig.5 Diagram of the Q-learning principle in QFOA


## 2.6.1 智能体和动作定义

本文是以最小化最大完工时间作为目标函数，通过Q-learning引导种群选择合适的邻域结构，以得到更好的潜在解。在优化AGV资源配置时，智能体根据当前状态选择动作。在QFOA中，五种邻域结构算子（N1~N5）被定义为动作集。 

## 2.6.2 状态定义

在QFOA中，状态的定义是智能体进行动作选择的关键。参考文献[30]，定义最小完工时间和平均完工时间。公式如下所示： 

$$
A C = \frac {1}{N} \sum_ {i} ^ {N} p o p _ {i}\tag{27}
$$

$$
M C = \min (p o p _ {i}), i = 1, 2,.., N\tag{28}
$$

$$
\Delta A C = A C _ {t - 1} - A C _ {t}, t = 1, 2,..., T\tag{29}
$$

$$
\Delta M C = M C _ {t - 1} - M C _ {t}, t = 1, 2, \dots , T\tag{30}
$$

式(27)中， $N$ 代表种群数量，式(29)和(30)中， $AC_{t}$ 和 $MC_{t}$ 分别表示第 $t$ 次迭代时种群的平均适应度值 和最小适应度值。在迭代过程中，存在四种组合情况：(1) $\Delta AC > 0$ ， $\Delta MC > 0$ ；(2) $\Delta AC > 0$ ， $MC\leq 0$ (3) $\Delta AC\leq 0$ ， $\Delta MC > 0$ ；(4) $\Delta AC\leq 0$ ， $MC\leq 0$ 。这四种情况被定义为智能体的四种状态。其中，状态(2)和(3)主要反映算法提升全局搜索能力和发现更优解的能力，而状态(1)和(4)则对应当前种群的收敛行为。 

## 2.6.3 奖励函数定义

当智能体选择某一动作时，果蝇个体将获得相应的奖励值。在QFOA中，奖励值的定义如下 

$$
R e w a r d = \left\{ \begin{array}{l} 1 0, \Delta M C > 0. \\ 0, \Delta M C \leq 0. \end{array} \right.\tag{31}
$$

如果 $\Delta MC > 0$ ，则所选择的动作将获取奖励并更新 $Q$ 表；反之，奖励值为0。为更好地降低惩罚奖励的影响并增强奖励值的显著性，惩罚项设为0，奖励值设为10。较大的奖励值能够增强对有益动作的正向激励。对于未改进的动作不设负向惩罚，以避免稀释正向奖励的效果。二元奖励机制使算法能够更专注于强化改进，从而促进更快的收敛速度并提升搜索性能。 

## 2.7 视觉搜索

在标准FOA中，当种群确定新的中心位置时，其他个体将在该中心位置的基础上进行局部搜索，以探索更优解；若未确定新的中心位置，则保持现有中心位置不变。为防止算法过早收敛于局部最优，本文提出一种改进的视觉搜索策略。在视觉搜索阶段，尽管部分解会被舍弃，但其邻域附近可能存在更优解，因此应保留这些被舍弃解的信息。为避免浪费这些解的潜在价值，在嗅觉搜索阶段，由邻域结构生成的新解与原始种群的解进行合并。合并后的解集合按照适应度值从高到低排序，选取前 $P_{s}$ 个个体作为新种群，用于下一次迭代。该策略不仅能够保持种群多样性，还充分考虑了被舍弃解的潜在价值，从而提升算法在针织车间AGV资源配置问题上的求解效率。通过改进视觉搜索策略，不仅保留了标准FOA的原有优势，还进一步增强解空间的探索能力，降低了陷入局部最优的风险，提高算法的全局搜索能力。 

## 3 仿真实验

## 3.1 实验设计及参数设置

由于针织车间AGV资源配置优化问题缺乏标准算例，本文结合问题特点构造了27个不同规模的测试算例，分为小规模、中规模和大规模。通过消融实验和对比实验，分析所提策略的有效性和算法性能。算例JxMyAz表示 $x$ 个工件在 $y$ 个机器上加工使用 $z$ 个AGV，测试算例的总体信息如表3所示。根据针织车间生产过程加工信息，每个工件的前两道工序的加工时间为{10,60}，第三道入库工序的加工时间设为0。 


表 3 测试案例信息



Tab.3 Test instance information


<table><tr><td>参数</td><td>取值范围</td></tr><tr><td>工件数</td><td>{25, 50, 100}</td></tr><tr><td>机器数</td><td>{5, 25, 50}</td></tr><tr><td>AGV 数</td><td>{2, 10, 16}</td></tr><tr><td>AGV 种类</td><td>2</td></tr><tr><td>工序数</td><td>3</td></tr><tr><td>运输时间</td><td>[5, 30]</td></tr></table>

QFOA的主要参数包括种群规模 $Ps$ 、贪心因子 $\varepsilon$ 、折扣因子 $\gamma$ 和学习率 $\alpha$ 。采用正交实验法确定算法的最优参数组合，最多迭代200次。参数水平范围及参数值如表4所示以算例“J50M25A10”为例，在MATLAB2023a中进行实验。算法运行环境为i5-9300H处理器，主频2.40GHz，内存8GB。QFOA的最佳参数设置为： $Ps = 200$ ， $\varepsilon = 0.8$ ， $\gamma = 0.6$ ， $\alpha = 0.2$ 。 


表 4 QFOA 参数设置



Tab.4 Parameter setting for QFOA


<table><tr><td>参数</td><td>参数水平</td><td>参数值</td></tr><tr><td><eq>P_s</eq></td><td>{50, 100, 150, 200}</td><td>200</td></tr><tr><td><eq>\varepsilon</eq></td><td>{0.8, 0.85, 0.90, 0.95}</td><td>0.8</td></tr><tr><td><eq>\gamma</eq></td><td>{0.6, 0.7, 0.8, 0.9}</td><td>0.6</td></tr><tr><td><eq>\alpha</eq></td><td>{0.1, 0.2, 0.3, 0.4}</td><td>0.2</td></tr></table>

## 3.2 消融实验

为了评估初始化策略、Q-learning和种群合并策略的有效性，本文将QFOA、FOA-1和FOA-2进行对比。QFOA结合初始化策略、Q-learning和种群合并策略；FOA-1仅包含Q-learning；FOA-2则包括初始化策 略和Q-learning。使用相对百分比偏差(Relative Percentage Deviation, RPD)衡量算法的综合性能[31]。 

$$
R P D = \frac {C _ {t} - C _ {b e s t}}{C _ {b e s t}} \times 1 0 0\tag{32}
$$

式(32)中 $C_t$ 表示当前算法运行10次的最优值， $C_{best}$ 表示所有算法运行10次的最优值。RPD的值越小，算法的性能越好。 

采用最小值(minimum, min)、平均值(average, avg)和RPD三个指标对算法的性能进行评估，实验数据来自27个不同规模的算例。消融实验结果见表5和表6。在min和RPD值方面，QFOA优于FOA-1和FOA-2。此外，QFOA在所有实例中始终实现最佳avg值，突出了其稳定性和整体优势。消融实验结果证明了初始化策略、Q-learning和种群合并策略的有效性，为所提出的算法的有效性提供了强有力的支持。 


表 5 极值和均值实验结果



Tab.5 Experimental results on extremes and means


<table><tr><td rowspan="2">算例</td><td colspan="2">QFOA</td><td colspan="2">FOA-1</td><td colspan="2">FOA-2</td></tr><tr><td>min</td><td>avg</td><td>min</td><td>avg</td><td>min</td><td>avg</td></tr><tr><td>J25M5A2</td><td>606</td><td>625.50</td><td>678</td><td>719.20</td><td>656</td><td>668.00</td></tr><tr><td>J25M5A10</td><td>614</td><td>621.50</td><td>696</td><td>715.50</td><td>644</td><td>665.30</td></tr><tr><td>J25M5A16</td><td>602</td><td>624.20</td><td>692</td><td>720.10</td><td>653</td><td>661.70</td></tr><tr><td>J25M25A2</td><td>603</td><td>624.30</td><td>697</td><td>717.50</td><td>661</td><td>669.60</td></tr><tr><td>J25M25A10</td><td>623</td><td>630.90</td><td>719</td><td>728.30</td><td>654</td><td>669.10</td></tr><tr><td>J25M25A16</td><td>603</td><td>621.40</td><td>683</td><td>717.60</td><td>645</td><td>666.60</td></tr><tr><td>J25M50A2</td><td>610</td><td>625.00</td><td>709</td><td>717.40</td><td>654</td><td>665.80</td></tr><tr><td>J25M50A10</td><td>609</td><td>623.80</td><td>702</td><td>718.40</td><td>645</td><td>669.10</td></tr><tr><td>J25M50A16</td><td>601</td><td>617.10</td><td>713</td><td>724.10</td><td>654</td><td>663.90</td></tr><tr><td>J50M5A2</td><td>626</td><td>631.60</td><td>696</td><td>721.80</td><td>656</td><td>670.60</td></tr><tr><td>J50M5A10</td><td>611</td><td>619.90</td><td>698</td><td>719.50</td><td>652</td><td>671.30</td></tr><tr><td>J50M5A16</td><td>612</td><td>620.60</td><td>708</td><td>721.30</td><td>660</td><td>670.20</td></tr><tr><td>J50M25A2</td><td>612</td><td>623.30</td><td>695</td><td>713.60</td><td>654</td><td>665.80</td></tr><tr><td>J50M25A10</td><td>606</td><td>622.30</td><td>698</td><td>715.70</td><td>659</td><td>667.00</td></tr><tr><td>J50M25A16</td><td>615</td><td>629.20</td><td>697</td><td>713.10</td><td>657</td><td>668.80</td></tr><tr><td>J50M50A2</td><td>618</td><td>627.00</td><td>702</td><td>717.20</td><td>651</td><td>669.00</td></tr><tr><td>J50M50A10</td><td>608</td><td>619.50</td><td>702</td><td>715.10</td><td>654</td><td>671.00</td></tr><tr><td>J50M50A16</td><td>617</td><td>623.40</td><td>700</td><td>718.00</td><td>638</td><td>668.50</td></tr><tr><td>J100M5A2</td><td>607</td><td>621.60</td><td>693</td><td>721.50</td><td>648</td><td>666.40</td></tr><tr><td>J100M5A10</td><td>608</td><td>621.70</td><td>695</td><td>719.50</td><td>639</td><td>658.10</td></tr><tr><td>J100M5A16</td><td>612</td><td>625.10</td><td>712</td><td>722.70</td><td>658</td><td>670.40</td></tr><tr><td>J100M25A2</td><td>610</td><td>626.00</td><td>701</td><td>717.20</td><td>651</td><td>668.80</td></tr><tr><td>J100M25A10</td><td>608</td><td>620.60</td><td>687</td><td>717.40</td><td>650</td><td>667.30</td></tr><tr><td>J100M25A16</td><td>605</td><td>621.20</td><td>708</td><td>719.80</td><td>645</td><td>665.90</td></tr><tr><td>J100M50A2</td><td>610</td><td>625.00</td><td>704</td><td>718.10</td><td>644</td><td>665.40</td></tr><tr><td>J100M50A10</td><td>611</td><td>621.30</td><td>684</td><td>713.60</td><td>655</td><td>667.70</td></tr><tr><td>J100M50A16</td><td>601</td><td>621.90</td><td>682</td><td>713.20</td><td>651</td><td>667.30</td></tr></table>


表 6 RPD 实验结果



Tab.6 RPD test results


<table><tr><td>算例</td><td>QFOA</td><td>FOA-1</td><td>FOA-2</td></tr><tr><td>J25M5A2</td><td>0.00</td><td>11.88</td><td>8.25</td></tr><tr><td>J25M5A10</td><td>0.00</td><td>13.36</td><td>4.89</td></tr><tr><td>J25M5A16</td><td>0.00</td><td>14.95</td><td>8.47</td></tr><tr><td>J25M25A2</td><td>0.00</td><td>15.59</td><td>9.62</td></tr><tr><td>J25M25A10</td><td>0.00</td><td>15.41</td><td>4.98</td></tr><tr><td>J25M25A16</td><td>0.00</td><td>13.27</td><td>6.97</td></tr><tr><td>J25M50A2</td><td>0.00</td><td>16.23</td><td>7.21</td></tr><tr><td>J25M50A10</td><td>0.00</td><td>15.27</td><td>5.91</td></tr><tr><td>J25M50A16</td><td>0.00</td><td>18.64</td><td>8.82</td></tr><tr><td>J50M5A2</td><td>0.00</td><td>11.18</td><td>4.79</td></tr><tr><td>J50M5A10</td><td>0.00</td><td>14.24</td><td>6.71</td></tr><tr><td>J50M5A16</td><td>0.00</td><td>15.69</td><td>7.84</td></tr><tr><td>J50M25A2</td><td>0.00</td><td>13.56</td><td>6.86</td></tr><tr><td>J50M25A10</td><td>0.00</td><td>15.18</td><td>8.75</td></tr><tr><td>J50M25A16</td><td>0.00</td><td>12.36</td><td>6.83</td></tr><tr><td>J50M50A2</td><td>0.00</td><td>13.59</td><td>5.34</td></tr><tr><td>J50M50A10</td><td>0.00</td><td>15.46</td><td>7.57</td></tr><tr><td>J50M50A16</td><td>0.00</td><td>13.45</td><td>3.40</td></tr><tr><td>J100M5A2</td><td>0.00</td><td>14.17</td><td>6.75</td></tr><tr><td>J100M5A10</td><td>0.00</td><td>14.31</td><td>5.10</td></tr><tr><td>J100M5A16</td><td>0.00</td><td>16.34</td><td>7.52</td></tr><tr><td>J100M25A2</td><td>0.00</td><td>14.92</td><td>6.72</td></tr><tr><td>J100M25A10</td><td>0.00</td><td>12.99</td><td>6.91</td></tr><tr><td>J100M25A16</td><td>0.00</td><td>17.02</td><td>6.61</td></tr><tr><td>J100M50A2</td><td>0.00</td><td>15.41</td><td>5.57</td></tr><tr><td>J100M50A10</td><td>0.00</td><td>11.95</td><td>7.20</td></tr><tr><td>J100M50A16</td><td>0.00</td><td>13.48</td><td>8.32</td></tr></table>


为了验证所提算法的有效性，图6展示了在不同规模下三种算法运行10次的箱形图。QFOA结果比其他算法更集中，表明QFOA具有更好的稳定性。 


![](images/23394a14c9ea4dab08fe0cf0502b1f467144108488cca6606968318c77f5b146.jpg)


![](images/c669252b496b82cd5874463ba2adca69ef2bf7405e361006fa55add5f2a79f3d.jpg)



图6 不同规模下实验结果箱线图



Fig.6 Box plots of experimental results at different scales


![](images/2d35bdd139b9c3f7a95a19f16cd6bb590b1bc26ad074ae87dbe1ac3f933f6bd1.jpg)


图7展示了不同规模算例的收敛曲线。结果表明，引入初始化策略的QFOA和FOA-2在首次迭代后均获得优于其他算法的解，凸显初始化策略的有效性。此外，在视觉搜索阶段引入种群合并策略的QFOA在整个优化过程中表现优于FOA-2，验证种群合并策略在提升优化结果方面的有效性。 

![](images/67bb6d89a5114b330fcff4c7bdd09ed21a1e0ee65f65016e777c379fa302b224.jpg)



(a) J25M5A10


![](images/f2bbd5ecb66c421f9846701ac7ba2278df65fd3b585c82fd8cf3d230c678a948.jpg)



图7 不同实验规模下算法收敛曲线


![](images/4878dbbc8aa08e9466911600f1fd0792d0140c9620703731edfd6bcb90cf7cfa.jpg)



(c) J100M25A10



Fig.7 Algorithm convergence curves at different scales


## 3.3 对比实验

为了验证本文所提QFOA算法的有效性，将QFOA与FOA以及其他五种广泛用于解决车间调度问题的算法进行对比。其他五种比较算法分别为：采用精英保留策略的改进遗传算法(Improved Genetic Algorithm, IGA)、采用基于概率交叉的离散更新方法进化种群的改进灰狼算法(Improved Grey Wolf Optimization, IGWO) $^{[32]}$ 、采用离散粒子更新方法的改进粒子群算法(Improved Particle Swarm Optimization, IPSO) $^{[33]}$ 、采用外部档案集方法的改进人工蜂群算法(Improved Artificial Bee Colony, IABC) $^{[34]}$ 以及基于Q-learning的改进人工蜂群算法(Q-learning-based Artificial Bee Colony, QABC) $^{[35]}$ 。 

为保证对比实验的公平性，采用正交实验法确定各算法的最优参数组合，最多迭代200次。各对比算法的参数水平范围及确定值如表7所示。为保证实验公平，各算法的解码方式和运行环境保持一致。七种算法的迭代次数均设置为200次，每个算法独立运行10次。表8和表9分别列出各算法在不同规模算例下的min、avg和RPD值，最优值以粗体显示。从表中数据可知，QFOA在所有算例中均达到最优的avg值，且在所有算例中QFOA的RPD值最小，表现出最优性能。 


表 7 对比算法参数设置



Tab.7 Parameter setting for comparison algorithms


<table><tr><td>算法</td><td>参数水平</td><td>参数</td></tr><tr><td>QFOA</td><td><eq>P_s=\{50,100,150,200\}, \varepsilon=\{0.8,0.85,0.90,0.95\}, \gamma=\{0.6,0.7,0.8,0.9\}, \alpha=\{0.1,0.2,0.3,0.4\}</eq></td><td><eq>P_s=200,\varepsilon=0.8,\gamma=0.6,\alpha=0.2</eq></td></tr><tr><td>FOA</td><td><eq>P_s=\{50,100,150,200\}</eq></td><td><eq>P_s=200</eq></td></tr><tr><td>IGA</td><td><eq>P_c=\{0.6,0.7,0.8,0.9\}, P_m=\{0.1,0.2,03,04\}, P_s=\{50,100,150,200\},elite number=\{3,4,5,6\}</eq></td><td><eq>P_c=0.8,P_m=0.1,P_s=150,elite number=4</eq></td></tr><tr><td>IGWO[32]</td><td><eq>GL=\{0.3,0.4,0.5,0.6\}, GP=\{0.6,0.7,0.8,0.9\}, P_s=\{50,100,150,200\}</eq></td><td><eq>GL=0.5,GP=0.6,P_s=200</eq></td></tr><tr><td>IPSO[33]</td><td><eq>c1=\{0.6,0.7,0.8,0.9\}, c2=\{0.6,0.7,0.8,0.9\}, P_s=\{50,100,150,200\}</eq></td><td><eq>c1=0.6,c2=0.8,P_s=150</eq></td></tr><tr><td>IABC[34]</td><td>Archives number = {35,40,45,50}, limit = {10,20,30,40}, <eq>P_s=\{50,100,150,200\}</eq></td><td>Archives number =40, limit = 30, <eq>P_s=200</eq></td></tr><tr><td>QABC[35]</td><td>Archives number = {35,40,45,50}, limit = {10,20,30,40}, <eq>P_s=\{50,100,150,200\}, \varepsilon=\{0.8,0.85,0.90,0.95\}, \gamma=\{0.6,0.7,0.8,0.9\}, \alpha=\{0.1,0.2,0.3,0.4\}</eq></td><td>Archives number =40, limit = 30, <eq>P_s=200,\varepsilon=0.8,\gamma=0.6,\alpha=0.3</eq></td></tr></table>


表 8 对比算法的极值和均值实验结果



Tab.8 Extreme and mean experimental results of comparison algorithms


<table><tr><td rowspan="2">算例</td><td colspan="2">QFOA</td><td colspan="2">FOA</td><td colspan="2">IGA</td><td colspan="2">IPSO</td><td colspan="2">IGWO</td><td colspan="2">IABC</td><td colspan="2">QABC</td></tr><tr><td>min</td><td>avg</td><td>min</td><td>avg</td><td>min</td><td>avg</td><td>min</td><td>avg</td><td>min</td><td>avg</td><td>min</td><td>avg</td><td>min</td><td>avg</td></tr><tr><td>J25M5A2</td><td>609</td><td>624.20</td><td>681</td><td>703.60</td><td>681</td><td>717.70</td><td>678</td><td>702.10</td><td>691</td><td>727.60</td><td>683</td><td>718.50</td><td>630</td><td>653.50</td></tr><tr><td>J25M5A10</td><td>615</td><td>624.80</td><td>700</td><td>708.50</td><td>696</td><td>719.80</td><td>683</td><td>702.30</td><td>707</td><td>733.10</td><td>690</td><td>719.00</td><td>645</td><td>655.30</td></tr><tr><td>J25M5A16</td><td>612</td><td>622.00</td><td>687</td><td>706.90</td><td>685</td><td>717.00</td><td>685</td><td>703.20</td><td>707</td><td>732.50</td><td>702</td><td>717.50</td><td>653</td><td>665.20</td></tr><tr><td>J25M25A2</td><td>612</td><td>625.30</td><td>692</td><td>706.20</td><td>680</td><td>709.30</td><td>684</td><td>715.70</td><td>718</td><td>738.50</td><td>706</td><td>724.30</td><td>659</td><td>663.50</td></tr><tr><td>J25M25A10</td><td>605</td><td>617.80</td><td>681</td><td>698.20</td><td>689</td><td>717.80</td><td>670</td><td>706.20</td><td>697</td><td>703.80</td><td>696</td><td>718.20</td><td>644</td><td>656.10</td></tr><tr><td>J25M25A16</td><td>609</td><td>619.60</td><td>682</td><td>697.70</td><td>691</td><td>714.30</td><td>681</td><td>704.90</td><td>712</td><td>725.90</td><td>686</td><td>712.20</td><td>645</td><td>663.20</td></tr><tr><td>J25M50A2</td><td>606</td><td>624.40</td><td>673</td><td>703.20</td><td>695</td><td>725.00</td><td>679</td><td>713.50</td><td>695</td><td>734.90</td><td>695</td><td>714.10</td><td>654</td><td>665.80</td></tr><tr><td>J25M50A10</td><td>606</td><td>624.10</td><td>679</td><td>701.60</td><td>654</td><td>698.60</td><td>665</td><td>699.50</td><td>691</td><td>715.50</td><td>694</td><td>710.80</td><td>650</td><td>660.10</td></tr><tr><td>J25M50A16</td><td>617</td><td>625.10</td><td>685</td><td>706.30</td><td>685</td><td>716.70</td><td>683</td><td>711.10</td><td>689</td><td>729.40</td><td>689</td><td>712.70</td><td>657</td><td>667.90</td></tr><tr><td>J50M5A2</td><td>619</td><td>629.10</td><td>672</td><td>698.70</td><td>660</td><td>716.10</td><td>666</td><td>712.60</td><td>664</td><td>735.80</td><td>660</td><td>718.50</td><td>659</td><td>670.60</td></tr><tr><td>J50M5A10</td><td>602</td><td>624.30</td><td>691</td><td>704.80</td><td>700</td><td>727.30</td><td>684</td><td>712.50</td><td>715</td><td>734.90</td><td>669</td><td>724.20</td><td>632</td><td>651.30</td></tr><tr><td>J50M5A16</td><td>612</td><td>626.70</td><td>688</td><td>705.90</td><td>671</td><td>722.60</td><td>687</td><td>708.20</td><td>716</td><td>735.70</td><td>701</td><td>725.00</td><td>642</td><td>661.20</td></tr><tr><td>J50M25A2</td><td>612</td><td>627.20</td><td>696</td><td>706.60</td><td>687</td><td>716.80</td><td>691</td><td>710.80</td><td>693</td><td>725.00</td><td>703</td><td>719.80</td><td>654</td><td>665.80</td></tr><tr><td>J50M25A10</td><td>607</td><td>621.90</td><td>697</td><td>704.90</td><td>680</td><td>720.70</td><td>676</td><td>698.40</td><td>702</td><td>730.90</td><td>670</td><td>714.00</td><td>649</td><td>657.00</td></tr><tr><td>J50M25A16</td><td>607</td><td>621.90</td><td>666</td><td>701.70</td><td>689</td><td>720.90</td><td>675</td><td>713.70</td><td>722</td><td>733.20</td><td>691</td><td>720.20</td><td>647</td><td>658.80</td></tr><tr><td>J50M50A2</td><td>600</td><td>623.20</td><td>690</td><td>703.70</td><td>696</td><td>717.70</td><td>687</td><td>709.50</td><td>688</td><td>730.50</td><td>688</td><td>714.30</td><td>633</td><td>651.30</td></tr><tr><td>J50M50A10</td><td>610</td><td>620.40</td><td>677</td><td>699.40</td><td>660</td><td>703.90</td><td>667</td><td>705.40</td><td>674</td><td>716.20</td><td>672</td><td>709.90</td><td>654</td><td>671.00</td></tr><tr><td>J50M50A16</td><td>610</td><td>622.60</td><td>681</td><td>699.90</td><td>672</td><td>718.40</td><td>681</td><td>711.20</td><td>709</td><td>732.70</td><td>684</td><td>725.60</td><td>638</td><td>658.50</td></tr><tr><td>J100M5A2</td><td>602</td><td>618.10</td><td>686</td><td>701.80</td><td>691</td><td>726.50</td><td>686</td><td>705.10</td><td>698</td><td>737.30</td><td>673</td><td>718.40</td><td>648</td><td>665.40</td></tr><tr><td>J100M5A10</td><td>601</td><td>621.70</td><td>684</td><td>702.40</td><td>681</td><td>714.40</td><td>682</td><td>705.30</td><td>703</td><td>731.20</td><td>696</td><td>720.80</td><td>635</td><td>653.10</td></tr><tr><td>J100M5A16</td><td>600</td><td>625.10</td><td>681</td><td>705.30</td><td>687</td><td>724.20</td><td>687</td><td>711.70</td><td>707</td><td>735.20</td><td>706</td><td>723.80</td><td>629</td><td>647.40</td></tr><tr><td>J100M25A2</td><td>608</td><td>621.50</td><td>692</td><td>705.10</td><td>695</td><td>725.20</td><td>694</td><td>713.80</td><td>714</td><td>746.50</td><td>695</td><td>721.60</td><td>641</td><td>658.80</td></tr><tr><td>J100M25A10</td><td>605</td><td>621.10</td><td>695</td><td>702.80</td><td>688</td><td>717.70</td><td>689</td><td>711.20</td><td>694</td><td>735.40</td><td>699</td><td>721.70</td><td>640</td><td>657.30</td></tr><tr><td>J100M25A16</td><td>609</td><td>618.10</td><td>686</td><td>705.40</td><td>682</td><td>716.20</td><td>673</td><td>707.10</td><td>709</td><td>733.20</td><td>686</td><td>713.10</td><td>635</td><td>655.90</td></tr><tr><td>J100M50A2</td><td>606</td><td>622.90</td><td>677</td><td>699.70</td><td>675</td><td>712.20</td><td>667</td><td>706.30</td><td>719</td><td>737.50</td><td>669</td><td>713.70</td><td>634</td><td>655.40</td></tr><tr><td>J100M50A10</td><td>604</td><td>625.30</td><td>687</td><td>703.10</td><td>689</td><td>719.50</td><td>698</td><td>713.60</td><td>698</td><td>733.90</td><td>692</td><td>719.10</td><td>645</td><td>657.70</td></tr><tr><td>J100M50A16</td><td>608</td><td>627.80</td><td>685</td><td>698.00</td><td>697</td><td>721.60</td><td>698</td><td>710.90</td><td>708</td><td>733.70</td><td>697</td><td>727.80</td><td>641</td><td>657.30</td></tr></table>


表 9 对比算法 RPD 实验结果



Tab.9 RPD experimental results of comparison algorithms


<table><tr><td>算例</td><td>QFOA</td><td>FOA</td><td>IGA</td><td>IPSO</td><td>IGWO</td><td>IABC</td><td>QABC</td></tr><tr><td>J25M5A2</td><td>0.00</td><td>11.82</td><td>11.82</td><td>11.33</td><td>13.46</td><td>12.15</td><td>3.44</td></tr><tr><td>J25M5A10</td><td>0.00</td><td>13.82</td><td>13.17</td><td>11.06</td><td>14.96</td><td>12.20</td><td>4.87</td></tr><tr><td>J25M5A16</td><td>0.00</td><td>12.25</td><td>11.93</td><td>11.93</td><td>15.52</td><td>14.71</td><td>6.69</td></tr><tr><td>J25M25A2</td><td>0.00</td><td>13.07</td><td>11.11</td><td>11.76</td><td>17.32</td><td>15.36</td><td>7.67</td></tr><tr><td>J25M25A10</td><td>0.00</td><td>12.56</td><td>13.88</td><td>10.74</td><td>15.21</td><td>15.04</td><td>6.44</td></tr><tr><td>J25M25A16</td><td>0.00</td><td>11.99</td><td>13.46</td><td>11.82</td><td>16.91</td><td>12.64</td><td>5.91</td></tr><tr><td>J25M50A2</td><td>0.00</td><td>11.06</td><td>14.69</td><td>12.05</td><td>14.69</td><td>14.69</td><td>7.92</td></tr><tr><td>J25M50A10</td><td>0.00</td><td>12.05</td><td>7.92</td><td>9.74</td><td>14.03</td><td>14.52</td><td>7.26</td></tr><tr><td>J25M50A16</td><td>0.00</td><td>11.02</td><td>11.02</td><td>10.70</td><td>11.67</td><td>11.67</td><td>6.48</td></tr><tr><td>J50M5A2</td><td>0.00</td><td>8.56</td><td>6.62</td><td>7.59</td><td>7.27</td><td>6.62</td><td>6.46</td></tr><tr><td>J50M5A10</td><td>0.00</td><td>14.78</td><td>16.28</td><td>13.62</td><td>18.77</td><td>11.13</td><td>4.98</td></tr><tr><td>J50M5A16</td><td>0.00</td><td>12.42</td><td>9.64</td><td>12.25</td><td>16.99</td><td>14.54</td><td>4.90</td></tr><tr><td>J50M25A2</td><td>0.00</td><td>13.73</td><td>12.25</td><td>12.91</td><td>13.24</td><td>14.87</td><td>6.86</td></tr><tr><td>J50M25A10</td><td>0.00</td><td>14.83</td><td>12.03</td><td>11.37</td><td>15.65</td><td>10.38</td><td>6.91</td></tr><tr><td>J50M25A16</td><td>0.00</td><td>9.72</td><td>13.51</td><td>11.20</td><td>18.95</td><td>13.84</td><td>6.58</td></tr><tr><td>J50M50A2</td><td>0.00</td><td>15.00</td><td>16.00</td><td>14.50</td><td>14.67</td><td>14.67</td><td>5.50</td></tr><tr><td>J50M50A10</td><td>0.00</td><td>10.98</td><td>8.20</td><td>9.34</td><td>10.49</td><td>10.16</td><td>7.21</td></tr><tr><td>J50M50A16</td><td>0.00</td><td>11.64</td><td>10.16</td><td>11.64</td><td>16.23</td><td>12.13</td><td>4.59</td></tr><tr><td>J100M5A2</td><td>0.00</td><td>13.95</td><td>14.78</td><td>13.95</td><td>15.95</td><td>11.79</td><td>7.64</td></tr><tr><td>J100M5A10</td><td>0.00</td><td>13.81</td><td>13.31</td><td>13.48</td><td>16.97</td><td>15.81</td><td>5.65</td></tr><tr><td>J100M5A16</td><td>0.00</td><td>13.50</td><td>14.50</td><td>14.50</td><td>17.83</td><td>17.67</td><td>4.83</td></tr><tr><td>J100M25A2</td><td>0.00</td><td>13.82</td><td>14.31</td><td>14.14</td><td>17.43</td><td>14.31</td><td>5.42</td></tr><tr><td>J100M25A10</td><td>0.00</td><td>14.88</td><td>13.72</td><td>13.88</td><td>14.71</td><td>15.54</td><td>5.78</td></tr><tr><td>J100M25A16</td><td>0.00</td><td>12.64</td><td>11.99</td><td>10.51</td><td>16.42</td><td>12.64</td><td>4.26</td></tr><tr><td>J100M50A2</td><td>0.00</td><td>11.72</td><td>11.39</td><td>10.07</td><td>18.65</td><td>10.40</td><td>4.62</td></tr><tr><td>J100M50A10</td><td>0.00</td><td>13.74</td><td>14.07</td><td>15.56</td><td>15.56</td><td>14.57</td><td>6.78</td></tr><tr><td>J100M50A16</td><td>0.00</td><td>12.66</td><td>14.64</td><td>14.80</td><td>16.45</td><td>14.64</td><td>5.42</td></tr></table>

选取J25M5A10、J50M25A10、J100M25A10三种不同规模的算例来评估算法的整体性能。图8展示了七种算法在不同规模算例上独立执行10次结果的箱线图，用于评估算法的稳定性。随着算例规模的增加，QFOA算法表现出了良好的稳定性，其性能优于其他六种算法。 

![](images/a88a98ee5a86968e0189cb39d941415995a78cdbd0cb6e4bef171b65f93f1bb0.jpg)


![](images/c8feb9ada440f79afa16f46b6f7fe3bf60ed3de9c6611d1a69364afa89d7cacd.jpg)



图8 不同规模下对比算法实验结果箱线图


![](images/742604e8599d5d98cd2145fc1a685edc67d3cb0688872abd5c70e61e5c80e783.jpg)



(c) J100M25A10



Fig.8 Box plots of experimental results of comparison algorithms at different scales


为进一步分析各算法在迭代过程中的表现，绘制了不同算法在不同实验规模算例下的收敛曲线（如图9所示）。QFOA算法的结果比其他算法更好，收敛速度明显更快，性能更优越。 

![](images/31d369982c59f7265790fe6d5284ed6479ddd5895344b33c4dede31bec9ddac4.jpg)



(a) J25M5A10


![](images/bca1b3b330fc6b4860f3bed98d7ff763346dedf89f52fc82cc2fc499a79aa984.jpg)


![](images/14bd2f98d7e48f9d318a41e17fbf5c17c18bc7c36b9915f4de7a86d2a8c4d4b1.jpg)



(c) J100M25A10



图 9 不同实验规模下对比算法的收敛曲线



Fig.9 Convergence curves of comparison algorithms at different experimental scales


为了评估AGV资源配置模型的有效性，本文将QFOA与CPLEX及其他六种算法进行比较，统计了最小完工时间和算法运行时间，算法运行时间单位为秒，具体结果见表10。CPLEX通过分支切割算法精确求解问题，从而获得最优完工时间。相比之下，QFOA凭借四种初始化策略、Q-learning与嗅觉搜索的结合，以及视觉搜索阶段引入的种群合并策略，有效缩短了完工时间，验证了所提模型的有效性。 

表10还展示了各算法的计算时间。通过对比实验，CPLEX在小规模算例中表现出优势，得益于其分支切割算法能够快速求解。然而，在中、大规模算例中，QFOA的运行时间更短，验证了其改进策略的有效性，且在计算效率和稳定性方面具有显著优势。因此，QFOA在中、大规模资源配置问题中表现优越，展现出良好的稳定性。 


表 10 CPLEX 与七种算法的在最小完工时间和运行时间对比结果



Tab.10 The comparison results of CPLEX and seven algorithms in terms of minimum makespan and running time


<table><tr><td rowspan="2">算例</td><td colspan="2">CPLEX</td><td colspan="2">QFOA</td><td colspan="2">FOA</td><td colspan="2">IGA</td><td colspan="2">IPSO</td><td colspan="2">IGWO</td><td colspan="2">IABC</td><td colspan="2">QABC</td></tr><tr><td>完工时间</td><td>运行时间</td><td>完工时间</td><td>运行时间</td><td>完工时间</td><td>运行时间</td><td>完工时间</td><td>运行时间</td><td>完工时间</td><td>运行时间</td><td>完工时间</td><td>运行时间</td><td>完工时间</td><td>运行时间</td><td>完工时间</td><td>运行时间</td></tr><tr><td>J25M5A2</td><td>621</td><td>30.89</td><td>609</td><td>45.25</td><td>681</td><td>71.28</td><td>681</td><td>67.28</td><td>678</td><td>61.67</td><td>691</td><td>49.04</td><td>683</td><td>67.35</td><td>630</td><td>57.63</td></tr><tr><td>J25M5A10</td><td>610</td><td>46.95</td><td>615</td><td>59.40</td><td>700</td><td>72.33</td><td>696</td><td>68.94</td><td>683</td><td>63.76</td><td>707</td><td>57.68</td><td>690</td><td>73.49</td><td>645</td><td>63.94</td></tr><tr><td>J25M5A16</td><td>612</td><td>53.39</td><td>612</td><td>63.71</td><td>687</td><td>75.12</td><td>685</td><td>78.62</td><td>685</td><td>68.88</td><td>707</td><td>63.59</td><td>702</td><td>72.09</td><td>653</td><td>67.71</td></tr><tr><td>J25M25A2</td><td>653</td><td>73.63</td><td>612</td><td>70.82</td><td>692</td><td>80.79</td><td>680</td><td>90.08</td><td>684</td><td>73.81</td><td>718</td><td>72.61</td><td>706</td><td>84.16</td><td>659</td><td>74.59</td></tr><tr><td>J25M25A10</td><td>668</td><td>75.26</td><td>605</td><td>76.38</td><td>681</td><td>89.20</td><td>689</td><td>99.31</td><td>670</td><td>84.35</td><td>697</td><td>76.02</td><td>696</td><td>89.70</td><td>644</td><td>79.51</td></tr><tr><td>J25M25A16</td><td>650</td><td>74.13</td><td>609</td><td>84.09</td><td>682</td><td>90.15</td><td>691</td><td>105.79</td><td>681</td><td>98.27</td><td>712</td><td>93.56</td><td>686</td><td>93.67</td><td>645</td><td>87.63</td></tr><tr><td>J25M50A2</td><td>635</td><td>82.89</td><td>606</td><td>82.29</td><td>673</td><td>93.53</td><td>695</td><td>100.51</td><td>679</td><td>96.04</td><td>695</td><td>95.36</td><td>695</td><td>95.32</td><td>654</td><td>86.36</td></tr><tr><td>J25M50A10</td><td>685</td><td>109.34</td><td>606</td><td>79.23</td><td>679</td><td>102.34</td><td>654</td><td>104.34</td><td>665</td><td>108.12</td><td>691</td><td>101.16</td><td>694</td><td>115.73</td><td>650</td><td>97.58</td></tr><tr><td>J25M50A16</td><td>683</td><td>110.83</td><td>617</td><td>99.54</td><td>685</td><td>115.80</td><td>685</td><td>108.47</td><td>683</td><td>120.39</td><td>689</td><td>112.38</td><td>689</td><td>127.82</td><td>657</td><td>109.36</td></tr><tr><td>J50M5A2</td><td>669</td><td>112.89</td><td>619</td><td>115.25</td><td>672</td><td>215.40</td><td>660</td><td>218.56</td><td>666</td><td>256.86</td><td>664</td><td>267.05</td><td>660</td><td>270.48</td><td>659</td><td>187.84</td></tr><tr><td>J50M5A10</td><td>702</td><td>120.95</td><td>602</td><td>119.40</td><td>691</td><td>230.21</td><td>700</td><td>225.35</td><td>684</td><td>215.40</td><td>715</td><td>246.58</td><td>669</td><td>298.46</td><td>632</td><td>165.79</td></tr><tr><td>J50M5A16</td><td>710</td><td>126.39</td><td>612</td><td>126.71</td><td>688</td><td>256.28</td><td>671</td><td>212.48</td><td>687</td><td>232.52</td><td>716</td><td>290.59</td><td>701</td><td>310.22</td><td>642</td><td>173.25</td></tr><tr><td>J50M25A2</td><td>693</td><td>145.63</td><td>612</td><td>143.82</td><td>696</td><td>266.58</td><td>687</td><td>242.49</td><td>691</td><td>233.97</td><td>693</td><td>283.24</td><td>703</td><td>339.48</td><td>654</td><td>187.51</td></tr><tr><td>J50M25A10</td><td>697</td><td>143.26</td><td>607</td><td>144.38</td><td>697</td><td>286.59</td><td>680</td><td>280.12</td><td>676</td><td>295.76</td><td>702</td><td>317.69</td><td>670</td><td>361.32</td><td>649</td><td>195.37</td></tr><tr><td>J50M25A16</td><td>712</td><td>168.13</td><td>607</td><td>167.09</td><td>666</td><td>288.92</td><td>689</td><td>286.27</td><td>675</td><td>267.41</td><td>722</td><td>324.84</td><td>691</td><td>359.33</td><td>647</td><td>201.59</td></tr><tr><td>J50M50A2</td><td>688</td><td>165.89</td><td>600</td><td>162.29</td><td>690</td><td>296.33</td><td>696</td><td>255.73</td><td>687</td><td>235.67</td><td>688</td><td>356.13</td><td>688</td><td>326.96</td><td>633</td><td>187.67</td></tr><tr><td>J50M50A10</td><td>703</td><td>318.34</td><td>610</td><td>157.23</td><td>677</td><td>295.21</td><td>660</td><td>289.54</td><td>667</td><td>269.52</td><td>674</td><td>374.53</td><td>672</td><td>337.32</td><td>654</td><td>198.63</td></tr><tr><td>J50M50A16</td><td>694</td><td>340.83</td><td>610</td><td>198.54</td><td>681</td><td>336.64</td><td>672</td><td>299.84</td><td>681</td><td>287.55</td><td>709</td><td>387.72</td><td>684</td><td>356.61</td><td>638</td><td>215.93</td></tr><tr><td>J100M5A2</td><td>689</td><td>442.41</td><td>602</td><td>268.54</td><td>686</td><td>311.34</td><td>691</td><td>308.34</td><td>686</td><td>340.39</td><td>698</td><td>309.16</td><td>673</td><td>327.73</td><td>648</td><td>288.26</td></tr><tr><td>J100M5A10</td><td>705</td><td>477.81</td><td>601</td><td>307.04</td><td>684</td><td>330.80</td><td>681</td><td>316.47</td><td>682</td><td>356.86</td><td>703</td><td>327.38</td><td>696</td><td>354.82</td><td>635</td><td>315.18</td></tr><tr><td>J100M5A16</td><td>700</td><td>474.33</td><td>600</td><td>345.89</td><td>681</td><td>374.40</td><td>687</td><td>398.56</td><td>687</td><td>415.40</td><td>707</td><td>367.05</td><td>706</td><td>460.48</td><td>629</td><td>385.63</td></tr><tr><td>J100M25A2</td><td>695</td><td>490.59</td><td>608</td><td>362.52</td><td>692</td><td>462.21</td><td>695</td><td>395.35</td><td>694</td><td>420.48</td><td>714</td><td>446.58</td><td>695</td><td>498.46</td><td>641</td><td>438.29</td></tr><tr><td>J100M25A10</td><td>713</td><td>481.37</td><td>605</td><td>372.39</td><td>695</td><td>436.28</td><td>688</td><td>412.48</td><td>689</td><td>433.97</td><td>694</td><td>490.59</td><td>699</td><td>510.22</td><td>640</td><td>462.16</td></tr><tr><td>J100M25A16</td><td>698</td><td>498.61</td><td>609</td><td>361.55</td><td>686</td><td>436.58</td><td>682</td><td>442.49</td><td>673</td><td>435.76</td><td>709</td><td>483.24</td><td>686</td><td>539.48</td><td>635</td><td>452.37</td></tr><tr><td>J100M50A2</td><td>713</td><td>510.28</td><td>606</td><td>363.19</td><td>677</td><td>456.59</td><td>675</td><td>480.12</td><td>667</td><td>567.41</td><td>719</td><td>517.69</td><td>669</td><td>561.32</td><td>634</td><td>486.19</td></tr><tr><td>J100M50A10</td><td>699</td><td>534.18</td><td>604</td><td>363.55</td><td>687</td><td>458.92</td><td>689</td><td>486.27</td><td>698</td><td>435.67</td><td>698</td><td>524.84</td><td>692</td><td>559.33</td><td>645</td><td>472.25</td></tr><tr><td>J100M50A16</td><td>702</td><td>554.49</td><td>608</td><td>365.06</td><td>685</td><td>456.33</td><td>697</td><td>445.73</td><td>698</td><td>469.52</td><td>708</td><td>556.13</td><td>697</td><td>526.96</td><td>641</td><td>465.82</td></tr></table>

## 3.4 案例分析

本文以浙江某针织车间的实际生产情况进行案例分析，验证所提算法的可行性和实用性。通过调研企业实际生产情况，车间设备包括150台针织横机和40台AGV。根据订单历史数据，产品数量为300件，每件产品包含三道工序。在实际生产过程中，第三道工序为入库，工作时间可以忽略不记，因此设为0。 

图10展示应用于实际情况的七种算法的箱形图和收敛曲线。图10(a)显示，QFOA获得的结果最接近X轴，并且QFOA的箱形图分布的范围较窄，表明QFOA相较于其他算法具有好的稳定性。如图10(b)所示，QFOA在解的质量和收敛速度方面优于其他算法，突出QFOA在寻找最优解方面的优势。 

![](images/a9d3c608ee2d7e7fd761f305728401fa41cc9671b7016662289d2f6d02239905.jpg)



(a) 实际案例箱线图


![](images/b3d11024eb83c10fc0399f0f28a55c4712a70e28cda428d77609cfc0d3117fab.jpg)



(b) 实际案例收敛曲线图



图10 实际案例箱线图和收敛曲线图



Fig.10 Box plot and convergence curve of a practical case


表11比较了七种算法在解决实际案例时的优化性能，以最小完工时间作为主要评估指标。QFOA相较于FOA减少71秒的完工时间，提升 $10.45\%$ 的性能，证明所提出的策略的有效性。为了进一步评估QFOA的性能，将其与FOA、IGA、IPSO、IGWO、IABC和QABC六种算法进行比较，其中QABC是最有效的。结果表明，与QABC相比，QFOA减少30秒的完工时间，提升 $4.42\%$ ，显著缩短了生产周期，进一步凸显QFOA的优越性能。QFOA相较于其他算法的优势，不仅源自Q-learning的辅助作用，还得益于其独特的算法结构、初始化策略和种群合并策略的综合优化。 


表 11 七种算法的最小完工时间比较



Tab.11 Minimum makespan comparison of seven algorithms


<table><tr><td>算法</td><td>QFOA</td><td>FOA</td><td>IGA</td><td>IPSO</td><td>IGWO</td><td>IABC</td><td>QABC</td></tr><tr><td>完工时间</td><td>679</td><td>750</td><td>767</td><td>748</td><td>773</td><td>742</td><td>709</td></tr></table>

## 3.5 发现与讨论

表12展示七种算法在不同任务数量下AGV资源配置最小完工时间对比。实验结果表明，AGV与机器的合理配置是提高生产效率的关键因素。当任务数量增加时完工时间也会随之增加，而增加AGV数量有助于缩短完工时间。不同AGV数量和机器配置组合对完工时间的影响有所差异。 

随着任务数量的增加，完工时间呈上升趋势，尤其在任务数量为100和200时，完工时间显著增加，表明任务量越大，导致完工时间延长。在相同任务数量下，增加AGV数量通常能有效缩短完工时间，特别是在任务数量较多的情况下，更多AGV能够更有效地分担运输任务，提升整体运输效率。然而，AGV数量的增加并非线性，达到一定数量后，增加AGV的效果逐渐减小，表明进一步增加AGV数量对完工时间改善作用有限。 

此外，在相同AGV数量下，增加机器数量能够有效减少完工时间，特别是在任务量较大时，更多机 器能够分担加工任务，减少等待时间，提高生产效率。然而，机器数量的增加需要合理配置，否则可能导致资源浪费，尤其在任务量较少时，过多机器配置可能反而增加浪费。 

在相同任务数量下，合理配置AGV和机器数量能显著降低完工时间，提升生产效率。当任务数量为50时，增加AGV数量能有效减少完工时间，但在50台AGV配置下，进一步增加AGV数量的效果减小，说明在任务量较小的情况下，增加AGV并不一定带来显著提升。随着任务数量增加到100和200，更多AGV和机器能够更好地分担任务，提高资源利用率，显著减少完工时间。因此，随着任务数量的增加，合理配置AGV和机器数量变得尤为重要，以确保系统在高负载下高效运作，避免瓶颈和资源浪费。 


表 12 七种算法下不同 AGV 资源配置最小完工时间对比


<table><tr><td>任务数</td><td>针织横机</td><td>AGV</td><td>QFOA</td><td>FOA</td><td>IGA</td><td>IPSO</td><td>IGWO</td><td>IABC</td><td>QABC</td></tr><tr><td rowspan="9">50</td><td>5</td><td>2</td><td>609</td><td>681</td><td>681</td><td>678</td><td>691</td><td>683</td><td>630</td></tr><tr><td>5</td><td>10</td><td>615</td><td>700</td><td>696</td><td>683</td><td>707</td><td>690</td><td>645</td></tr><tr><td>5</td><td>16</td><td>612</td><td>687</td><td>685</td><td>685</td><td>707</td><td>702</td><td>653</td></tr><tr><td>25</td><td>2</td><td>612</td><td>692</td><td>680</td><td>684</td><td>718</td><td>706</td><td>659</td></tr><tr><td>25</td><td>10</td><td>605</td><td>681</td><td>689</td><td>670</td><td>697</td><td>696</td><td>644</td></tr><tr><td>25</td><td>16</td><td>609</td><td>682</td><td>691</td><td>681</td><td>712</td><td>686</td><td>645</td></tr><tr><td>50</td><td>2</td><td>606</td><td>673</td><td>695</td><td>679</td><td>695</td><td>695</td><td>654</td></tr><tr><td>50</td><td>10</td><td>606</td><td>679</td><td>654</td><td>665</td><td>691</td><td>694</td><td>650</td></tr><tr><td>50</td><td>16</td><td>617</td><td>685</td><td>685</td><td>683</td><td>689</td><td>689</td><td>657</td></tr><tr><td rowspan="9">100</td><td>5</td><td>2</td><td>619</td><td>672</td><td>660</td><td>666</td><td>664</td><td>660</td><td>659</td></tr><tr><td>5</td><td>10</td><td>602</td><td>691</td><td>700</td><td>684</td><td>715</td><td>669</td><td>632</td></tr><tr><td>5</td><td>16</td><td>612</td><td>688</td><td>671</td><td>687</td><td>716</td><td>701</td><td>642</td></tr><tr><td>25</td><td>2</td><td>612</td><td>696</td><td>687</td><td>691</td><td>693</td><td>703</td><td>654</td></tr><tr><td>25</td><td>10</td><td>607</td><td>697</td><td>680</td><td>676</td><td>702</td><td>670</td><td>649</td></tr><tr><td>25</td><td>16</td><td>607</td><td>666</td><td>689</td><td>675</td><td>722</td><td>691</td><td>647</td></tr><tr><td>50</td><td>2</td><td>600</td><td>690</td><td>696</td><td>687</td><td>688</td><td>688</td><td>633</td></tr><tr><td>50</td><td>10</td><td>610</td><td>677</td><td>660</td><td>667</td><td>674</td><td>672</td><td>654</td></tr><tr><td>50</td><td>16</td><td>610</td><td>681</td><td>672</td><td>681</td><td>709</td><td>684</td><td>638</td></tr><tr><td rowspan="9">200</td><td>5</td><td>2</td><td>602</td><td>686</td><td>691</td><td>686</td><td>698</td><td>673</td><td>648</td></tr><tr><td>5</td><td>10</td><td>601</td><td>684</td><td>681</td><td>682</td><td>703</td><td>696</td><td>635</td></tr><tr><td>5</td><td>16</td><td>600</td><td>681</td><td>687</td><td>687</td><td>707</td><td>706</td><td>629</td></tr><tr><td>25</td><td>2</td><td>608</td><td>692</td><td>695</td><td>694</td><td>714</td><td>695</td><td>641</td></tr><tr><td>25</td><td>10</td><td>605</td><td>695</td><td>688</td><td>689</td><td>694</td><td>699</td><td>640</td></tr><tr><td>25</td><td>16</td><td>609</td><td>686</td><td>682</td><td>673</td><td>709</td><td>686</td><td>635</td></tr><tr><td>50</td><td>2</td><td>606</td><td>677</td><td>675</td><td>667</td><td>719</td><td>669</td><td>634</td></tr><tr><td>50</td><td>10</td><td>604</td><td>687</td><td>689</td><td>698</td><td>698</td><td>692</td><td>645</td></tr><tr><td>50</td><td>16</td><td>608</td><td>685</td><td>697</td><td>698</td><td>708</td><td>697</td><td>641</td></tr></table>

综上所述，合理配置AGV和机器数量对提升生产效率至关重要。在相同任务数量下，增加AGV和机器数量能够有效缩短完工时间。针织车间中，异构AGV的灵活配置能够更好地适应多种纱线配送需求，减少配送时序和物料完整性问题。尽管增加AGV数量有助于提高效率，但过度增加可能导致效果趋于平稳。因此，优化AGV和机器数量的组合是提高生产效率和最小化完工时间的关键。 

## 4 总结与展望

本文针对考虑异构AGV和机器顺序相关准备时间的针织车间AGV资源配置优化问题，以最小化最大完工时间为目标建立针织车间AGV资源配置模型，并提出QFOA对模型进行求解。首先，针对传统编码中将加工任务与运输任务绑定的问题，提出了基于任务的三段式编码方式，实现问题解空间的完全映射。其次，设计四种初始化策略以提高初始种群的质量和多样性。随后，将Q-learning与嗅觉搜索相结合，提高了算法的局部搜索能力；在视觉搜索阶段引入种群合并策略，提高算法的全局搜索能力。最后，通过对比实验、消融实验和案例分析，综合验证所提出的QFOA及相关策略的有效性。同时分析不同AGV配置对完工时间的影响，从而为针织车间配置AGV提供参考。然而，本文仍然存在一定的局限性，未考虑订单插单和机器故障。因此未来研究应考虑各种动态因素，以贴合真实的生产场景。 

## 参考文献



[1] 张洁，徐楚桥，汪俊亮，等. 数据驱动的机器人化纺织生产智能管控系统研究进展[J]. 纺织学报, 2022, 43(09): 1-10.

ZHANG Jie, XU Chuqiao, WANG Junliang, et al. Advancement in Data-driven Intelligent Control System for Roboticized Textile Production[J]. Journal of Textile Research, 2022, 43(09): 1-10. 





[2] 郑小虎，刘正好，陈峰，等. 纺织工业智能发展现状与展望[J]. 纺织学报, 2023, 44(08): 205-216. 





[8] 张维维，胡明珠，李继伟，等. 基于多智能体非合作-进化博弈的柔性作业车间机器-AGV 协同调度[J/OL]. 计算机集成制造系统, 1-19[2025-09-28]. http://dx.chinadoi.cn/10.13196/j.cims.2024.0215.

ZHANG Weiwei, HU Mingzhu, LI Jiwei, et al. Flexible Job Shop Machine-AGV Collaborative Scheduling Based on Multiagent Non-cooperative and Evolutionary Game[J/OL]. Computer Integrated Manufacturing Systems, 1-19[2025-09-28]. http://dx.chinadoi.cn/10.13196/j.cims.2024.0215. 





ZHENG Xiaohu, LIU Zhenghao, CHEN Feng, et al. Current Status and Prospect of Intelligent Development in Textile Industry[J]. Journal of Textile Research, 2023, 44(08): 205-216. 





[3] 董玉龙，陈璐，鲍中凯. 基于博弈论的飞机总装物流配送系统资源配置[J]. 浙江大学学报(工学版)，2025, 59(01): 120-129.

DONG Yulong, CHEN Lu, BAO Zhongkai. Resource Allocation of Aircraft Final Assembly Logistics Distribution System Based on Game Theory[J]. Journal of Zhejiang University (Engineering Science), 2025, 59(01): 120-129. 





[4] 郭笛，谢旦岚，纪媛. 多重约束下智慧仓储机器人配置仿真优化研究[J]. 系统仿真学报, 2020, 32(10): 2066-2072. GUO Di, XIE Danlan, JI Yuan. Research on Simulation Optimization of Intelligent Storage Robot Configuration under Multiple Constraints[J]. Journal of System Simulation, 2020, 32(10): 2066-2072. 





[5] CHENG W, MENG W. An Efficient Genetic Algorithm for Multi AGV Scheduling Problem about Intelligent Warehouse[J]. Robotic Intelligence and Automation, 2023, 43(4): 382-393. 





[6] MUMTAZ J, MINHAS K A, RAUF M, et al. Solving Line Balancing and AGV Scheduling Problems for Intelligent Decisions Using a Genetic-Artificial Bee Colony Algorithm[J]. Computers & Industrial Engineering, 2024, 189: 109976. 





[7] 陈炫锐，刘晓鹏，陈庆新，等．考虑充电的多层级货架自动小车存取系统的资源配置优化[J].计算机集成制造系统，2024,30(09):3310-3329.  
CHEN Xuanrui, LIU Xiaopeng, CHEN Qingxin, et al. Resource Configuration Optimization of Multi-level Rack Autonomous Vehicle Storage and Retrieval Systems Considering Charging[J]. Computer Integrated Manufacturing Systems, 2024, 30(09): 3310-3329. 





[9] 胡晓阳，姚锡凡，黄鹏，等. 改进迭代局部搜索算法求解多 AGV 柔性作业车间调度问题[J]. 计算机集成制造系统，2022, 28(07): 2198-2212.

HU Xiaoyang, YAO Xifan, HUANG Peng, et al. Improved Iterative Local Search Algorithm for Solving Multi-AGV Flexible Job Shop Scheduling Problem[J]. Computer Integrated Manufacturing Systems, 2022, 28(07): 2198-2212. 





[10] WEN X, FU Y, YANG W, et al. An Effective Hybrid Algorithm for Joint Scheduling of Machines and AGVs in Flexible Job Shop[J]. Measurement and Control, 2023, 56(9-10): 1582-1598. 





[11] 陈魁，毕利，王文雅. 柔性作业车间 AGV 与机器双资源集成调度研究[J]. 系统仿真学报, 2022, 34(03): 461-469.

CHEN Kui, BI Li, WANG Wenya. Research on Integrated Scheduling of AGV and Machine in Flexible Job Shop[J]. Journal of System Simulation, 2022, 34(03): 461-469. 





[12] YUAN M, ZHENG L, HUANG H, et al. Research on Flexible Job Shop Scheduling Problem with AGV Using Double DQN[J]. Journal of Intelligent Manufacturing, 2025, 36(1): 509-535. 





[13] ZHANG M, WANG L, QIU F, et al. Dynamic Scheduling for Flexible Job Shop with Insufficient Transportation Resources via Graph Neural Network and Deep Reinforcement Learning[J]. Computers & Industrial Engineering, 2023, 186: 109718. 





[14] YAO Y, LI X, GAO L. A DQN-based Memetic Algorithm for Energy-efficient Job Shop Scheduling Problem with Integrated Limited AGVs[J]. Swarm and Evolutionary Computation, 2024, 87: 101544. 





[15] WANG H, PENG T, Li X, et al. An Integrated Simulation—optimization Method for Flexible Assembly Job Shop Scheduling with Lot Streaming and Finite Transport resources[J]. Computers & Industrial Engineering, 2025, 200: 110790. 





[16] LI J, LIU Q, WANG C, et al. A Disjunctive Graph-based Metaheuristic for Flexible Job-Shop Scheduling Problems Considering Fixture Shortages in Customized Manufacturing Systems[J]. Robotics and Computer-Integrated Manufacturing, 2025, 95: 102981. 





[17] LIU M, LV J, DU S, et al. Multi-resource Constrained Flexible Job Shop Scheduling Problem with Fixture-pallet Combinatorial Optimisation[J]. Computers & Industrial Engineering, 2024, 188: 109903. 





[18] 郑建风, 赵煜星, 刘欣桐, 等. 多港口区域泊位资源的最优配置与分配[J]. 交通运输工程学报, 2023, 23(05): 183-191.

ZHENG Jianfeng, ZHAO Yuxing, LIU Xintong, et al. Optimal Configuration and Allocation of Berth Resources in Multi-port 





Regions[J]. Journal of Traffic and Transportation Engineering, 2023, 23(5): 183-191. 





[19] 李兴春, 李明泽, 曾庆成, 等. 数据驱动的自动化码头岸桥与 AGV 双层优化调度模型[J]. 工程管理科技前沿, 2024, 43(06): 25-32.

LI Xingchun, LI Mingze, ZENG Qingcheng, et al. Two-layer Optimization Scheduling Model of Quay Cranes and Automated Guided Vehicles with Data-driven Methods at Automated Container Terminals[J]. Frontiers of Science and Technology of Engineering Management, 2024, 43(06): 25-32. 





[20] LIU Q, WANG N, LI J, et al. Research on Flexible Job Shop Scheduling Optimization Based on Segmented AGV[J]. Computer Modeling in Engineering & Sciences (CMES), 2023, 134(3). 





[21] YUNUSOGLU P, TOPALOGLU Y. Constraint Programming Approach for Multi-resource-constrained Unrelated Parallel Machine Scheduling Problem with Sequence-dependent Setup Times[J]. International Journal of Production Research, 2022, 60(7): 2212-2229. 





[22] WAN J. Demand Prediction and Optimization of Workshop Manufacturing Resources Allocation: a New Method and a Case Study[J]. Advances in Production Engineering & Management, 2022, 17(4): 413-424. 





[23] GUO H, LI K, LIU J, et al. Dynamic Integrated Process Planning and Scheduling under Multi-resource Constraints in Workshops with Reconfigurable Manufacturing Cells: a Novel Hyper-heuristic Approach[J]. Expert Systems with Applications, 2025, 289: 128337. 





[24] MLEKUSCH J, HARTL R. The Dual-resource-constrained Re-entrant Flexible Flow Shop a Constraint Programming Approach and a Hybrid Genetic Algorithm[J]. International Journal of Production Research, 2025, 63(5): 1803-1824. 





[25] BARAK S, JAVANMARD S, MOGHDANI R. Dual Resource Constrained Flexible Job Shop Scheduling with Sequence - dependent Setup Time[J]. Expert Systems, 2024, 41(10): e13669. 





[26] LI J, LIN P, WU X, et al. Scheduling Optimization of Ship Plane Block Flow Line Considering Dual Resource Constraints[J]. Scientific Reports, 2024, 14(1): 30765. 





[27] ZHENG X, WANG L, WANG S. A Novel Fruit Fly Optimization Algorithm for the Semiconductor Final Testing Scheduling Problem[J]. Knowledge-Based Systems, 2014, 57: 95-103. 





[28] GUO H, SANG H, ZHANG B, et al. An Effective Metaheuristic with a Differential Flight Strategy for the Distributed Permutation Flowshop Scheduling Problem with Sequence-dependent Setup Times[J]. Knowledge-Based Systems, 2022, 242: 108328. 





[29] XIA L, CHEN S, ZHOU W, et al. Dual Evolutionary Algorithm Based on Dyna-Q for Distributed Heterogeneous Hybrid Flow Shop Problems with LR Trapezoidal Fuzzy Numbers[J]. Memetic Computing, 2025, 17(3): 1-26. 





[30] LI R, GONG W, LU C. A Reinforcement Learning Based RMOEA/D for Bi-objective Fuzzy Flexible Job Shop Scheduling[J]. Expert Systems with Applications, 2022, 203: 117380. 





[31] ZHAO F, HU X, WANG L, et al. A Memetic Discrete Differential Evolution Algorithm for the Distributed Permutation Flow Shop Scheduling Problem[J]. Complex & Intelligent Systems, 2022, 8(1): 141-161. 





[32] GU J, JIANG T, ZHU H, et al. Low-carbon Job Shop Scheduling Problem with Discrete Genetic-Grey Wolf Optimization Algorithm[J]. Journal of Advanced Manufacturing Systems, 2020, 19(1), 1-14. 





[33] ZHANG J, WANG W, XU X. A Hybrid Discrete Particle Swarm Optimization for Dual-resource Constrained Job Shop Scheduling with Resource Flexibility[J]. Journal of intelligent Manufacturing, 2017, 28, 1961-1972. 





[34] LI X, WU C, WU R, et al. Multi-objective Fuzzy Green Scheduling Optimization Method of Special Vehicle Body-in-white Prototype Shop Considering Equipment Preventive Maintenance[J]. Journal of Cleaner Production, 2024, 462, 142660. 





[35] MA M, WANG Y, LI H, et al. A Reinforcement Learning-integrated Discrete Artificial Bee Colony Algorithm for Hybrid Flow Shop Scheduling with Batch Processing and Variable Sublot Sizes[J]. Swarm and Evolutionary Computation, 2026, 100: 102253. 





作者简介:李西兴，男，1990年生，副教授、博士研究生导师。研究方向为生产调度优化、机械手智能抓取、制造业信息化。E-mail: lixixing@hbut.edu.cn. 王际鹏（通信作者），男，1987年生，讲师、硕士研究生导师。研究方向为生产调度优化、多机器人系统、Petri网理论与应用。E-mail: jp.wang@hbut.edu.cn. 

