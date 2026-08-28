# A �-Learning based NSGA-II for dynamic flexible job shop scheduling with limited transportation resources

Rensheng Chen <sup>a</sup>, Bin Wu <sup>a,∗</sup>, Hua Wang <sup>b</sup>, Huagang Tong <sup>a</sup>, Feiyi Yan <sup>a</sup> 

<sup>a</sup> School of Economics and Management, Nanjing Tech University, Nanjing, 211816, China 

<sup>b</sup> School of Mechanical and Power Engineering, Nanjing Tech University, Nanjing, 211816, China 

A R T I C L E I N F O 

Keywords: Flexible job shop scheduling problem Limited transportation resources Dynamic scheduling NSGA-II �-Learning algorithm 

## A B S T R A C T

With the widespread adoption of intelligent transportation equipment such as AGVs in the manufacturing field, the flexible job shop scheduling considering limited transportation resources has increasingly attracted attention. However, current research does not consider various dynamic disturbances in real production scenarios, resulting in lower executability of scheduling solutions. To solve this problem, a dynamic flexible job shop scheduling model with limited transportation resources is established, aiming to minimize makespan and total energy consumption. Considering three types of disturbances: job cancellation, machine breakdown, and AGV breakdown, the corresponding event-driven rescheduling strategy is proposed, and a rescheduling instability index is designed to measure the performance of the rescheduling strategy. A �-Learning-based NSGA-II algorithm (QNSGA-II) is proposed. By learning the feedback historical search experience, it adaptively selects the appropriate neighborhood structures for local search; and a hybrid initialization strategy tailored to the problem characteristics is designed to improve the optimization performance of the algorithm. Through simulation experiments, the effectiveness of the rescheduling strategies and the superiority of the QNSGA-II algorithm in solving such problems are validated. 

## 1. Introduction

Multi-variety and small-batch production is one of the most im portant production modes in today’s manufacturing industry. In response to its complex production planning and scheduling characteristics, many companies have established flexible manufacturing systems (FMS) that integrate information and equipment [1]. As the basis of the flexible job shop production system, how to reasonably arrange its scheduling solution in FMS affects the process of manufacturing to a great extent, so the flexible job shop scheduling problem (FJSP) has been paid more and more attention [2]. Meanwhile, Automated Guided Vehicles (AGVs) are widely employed as crucial intelligent logistics equipment in FMS [3]. There is a strong coupling relationship between the AGVs, the machines and the processing sequence of the job. The former will affect the start time of subsequent operations of the job, and the latter will also affect the selection of AGV [4]. In practical manufacturing systems, the lack of rational and efficient transportation solutions not only leads to increased transportation and time costs but also escalates AGV energy consumption and charging frequency. Thus, considering the flexible job shop scheduling problem with transportation resources (FJSP-T) has become a research hotspot in recent years [5]. 

Most of the existing research on FJSP-T does not take into account the impact of disturbances [6]. However, in the current complex and dynamic manufacturing scenarios, traditional job shop scheduling methods are difficult to meet the manufacturing demands under various interference events. Continuing to execute the initial solution under disturbance events will seriously reduce the stability of the overall scheduling and the efficiency of the subsequent manufacturing process [7,8]. Especially for more complex scheduling problems such as FJSP-T, when disturbance events occur, it is necessary to replan the machine and AGV at the same time to ensure that the whole schedul ing system can respond to various disturbance events in time [9,10]. Therefore, this paper constructs a dynamic flexible job shop scheduling problem with limited transportation resources (DFJSP-T). Based on the characteristics of DFJSP-T, we investigate the disturbance events of the three parts of job, machine and AGV respectively, and propose an event-driven rescheduling strategy for each of the three types of disturbance events. 

DFJSP-T is an extension of the classical FJSP, which has been proved to be an NP-hard problem [11]. In addition, most FJSPs in volve the simultaneous optimization of multiple objectives [12]. In recent years, the multi-objective optimization problems (MOPs) have garnered significant scholarly interest, and many scholars have con structed meta-heuristic algorithms to solve MOPs [13]. Among them, the non-dominated sorting genetic algorithm (NSGA-II) characterized by natural evolution has been considered as one of the optimal al gorithms for solving MOPs [14]. However, most meta-heuristic algo rithms in the existing literature only perform local search strategies through the polling mode, which makes the search have a certain blindness [15]. In contrast, �-Learning, as a reinforcement learning method, maximizes the target reward by using the learning strategy for the agent to select the appropriate action in the interaction with the environment. Related literature shows that the meta-heuristic algorithm combined with �-Learning can obtain better solutions than the traditional meta-heuristic algorithm [16]. 

In summary, this paper establishes a dynamic scheduling model for flexible job shop considering transportation resources and proposes a �-Learning based NSGA-II (QNSGA-II) algorithm. Specific contribu tions are as follows: 

(1) A mixed-integer dynamic scheduling model for the flexible job shop with limited transportation resources is established. The makespan and total energy consumption (TEC) are taken as the optimization objectives, and the charging constraints of AGV are consid ered. Three rescheduling strategies are proposed to solve the problems of order cancellation, machine breakdown and AGV breakdown, and a rescheduling instability index is designed to measure the performance of the rescheduling strategies. 

(2) A NSGA-II optimization algorithm based on �-Learning is proposed. A hybrid population strategy is designed to construct an initial population by combining three problem-oriented subpopulations to improve the convergence speed and diversity of the algorithm. �- Learning is employed to guide the selection of neighborhood structures in local search, and six neighborhood search operators are constructed as executable actions. 

The rest of the paper is as follows. Section 2 reviews the literature on FJSP-T, dynamic scheduling, �-Learning and meta-heuristic algo rithms. Section 3 designs the scheduling model of FJSP-T. Section 4 proposes rescheduling strategies to deal with three disturbance events and a rescheduling instability index. Section 5 describes the improved QNSGA-II in detail. Section 6 demonstrates the simulation experiments and analysis results of the dynamic scheduling model and QNSGA-II. The summary of this article is provided in Section 7. 

## 2. Literature review

This section provides a concise review of previous research in three domains: FJSP-T, dynamic scheduling, �-Learning and meta-heuristics. 

## 2.1. FJSP-T

As the production scale increases, the transportation tasks become more intensive, and it is unrealistic to simply consider the FJSP with infinite transportation resources. In order to simulate the actual produc tion scenarios, some researchers have considered limited transportation resources constraints in FJSP. 

FJSP-T was first proposed by Deroussi and Norre [17], who de signed an iterated local search algorithm and built a benchmark for FJSP-T. Pan et al. [18] proposed a learning-based multi-population evolutionary optimization (LMEO) to deal with FJSP-T. Different sub populations are designed and an improved selection method is proposed to choose appropriate individuals during the iteration of the algorithm. Liu et al. [19] discussed the AGV and machine integrated scheduling problem under conflict-free paths, proposed a self-learning genetic algorithm, and two different vehicle dispatching strategies are designed. Homayouni and Fontes [6] proposed a scheduling model and designed a late acceptance hill-climbing algorithm. Yan et al. [20] investigated FJSP-T under the condition of limited transportation of digital twin workshop, a novel three-segment encoding scheme is proposed to improve the performance of genetic algorithm in solving the minimization of makespan problem. Liu et al. [10] proposed a new job insertion FJSP-T and designed a two-stage multi-objective MILP model, and an adaptive large neighborhood search (MOALNS) algorithm is proposed, the validity of MOALNS is verified by the experiments. Xu et al. [21] designed an effective heuristic algorithm (EHA) to solve the multi-objective MILP model in order to minimize TEC and makespan as the objectives of green FJSP-T. Similarly, Li et al. [22] proposed an improved Jaya (IJaya) algorithm to solve FJSP-T with the goal of simultaneously optimizing the TEC and makespan, and developed several problem-oriented local search operators to perform exploitation tasks. LYU et al. [23] considered the AGV path conflict and the optimal number of AGVs in FJSP-T, and proposed an improved genetic algorithm combining time window and Dijkstra algorithm. Kumar et al. [24] designed a novel evolution algorithm to solve the FJSP-T for minimizing the makespan, and proposed a vehicle allocation algorithm and machine selection heuristic embedded into the DE method. Nour et al. [25] proposed a hybrid meta-heuristic based on the cluster holographic multi-agent model to minimize the makespan of FJSP-T. 

## 2.2. Dynamic scheduling

According to different strategies to deal with disturbance events, dynamic scheduling can be roughly classified into three categories: completely-reactive scheduling(CRS), robust proactive scheduling(RPS) and predictive-reactive scheduling(PRS). 

Completely-reactive scheduling is a strategy for manufacturing systems to generate scheduling solutions immediately according to realtime states and information. Luo [26] used DRL to solve the DFJSP of new job insertion in the continuous job shop state, and proposed six composite scheduling rules. Cai et al. [27] proposed a real-time information update mechanism and constructed a dynamic job shop scheduling model considering logistics factors. Ghaleb et al. [28] analyzed the effect of using real-time shop floor updates on scheduling decisions in flexible job shop production processes and developed three specific heuristics to deal with order arrivals and machine breakdown in FJSP. In addition, Luo et al. [29] applied RFID technology to obtain real-time data of the production process, and on this basis developed a multi-period hierarchical scheduling mechanism to coordinate and control the production schedule and workload. Li et al. [30] studied FJSP-T based on real-time data, and used the hybrid deep Q network to deal with the dynamic disturbance of machine breakdown and new job insertion. 

Robust proactive scheduling means to develop an effective schedul ing solution in advance according to the frequent disturbance factors to prevent frequent rescheduling. Liu et al. [31] considered robustness and stability in single-machine scheduling with random machine breakdown. The right-shift rearrangement strategy is adopted to avoid sequence deviation, but this method has shortcomings in resource utilization. Duan et al. [8] proposed a rescheduling strategy considering the overall system effectiveness to study the dynamic scheduling problem including machine breakdown and new job arrivals, and new evaluation indexes were designed from the perspectives of system and processing tasks. Liu et al. [10] discussed FJSP with job insertion under traffic resource constraints, proposed a two-stage multi-objective MILP model, and introduced instability minimization to deal with the impact of disturbances. Yang et al. [32] discussed the dual-objective FJSP with machine breakdown, and developed an alternative measurement index through extreme learning machine to measure the impact of perturbations on system robustness. 

Predictive reactive scheduling generates an initial scheduling solution at the beginning, and modifies the initial scheduling solution when disturbance events occur to reduce disturbance to the scheduling objective. The rescheduling methods mainly include left/right shift rescheduling, partial rescheduling and complete rescheduling. Zhu 

Literature review of DFJSP. 


Table 1


<table><tr><td>Strategy</td><td>AGV</td><td>Disturbances</td><td>Constraints</td><td>Objectives</td><td>Solving method</td><td>Refs.</td></tr><tr><td rowspan="5">CRS</td><td>×</td><td>Job insertion</td><td>×</td><td>Total tardiness</td><td>Deep Q network</td><td>[26]</td></tr><tr><td>√</td><td>Machine breakdown, job insertion</td><td>×</td><td>Customer satisfaction, equipment utilization, TEC</td><td>Simulation-based model with new type</td><td>[27]</td></tr><tr><td>×</td><td>Machine breakdown, job arrival</td><td>×</td><td>Total weighted tardiness</td><td>Hybrid genetic algorithm</td><td>[28]</td></tr><tr><td>×</td><td>Job arrival</td><td>×</td><td>Total earliness, total tardiness, makespan</td><td>Multi-period hierarchical scheduling mechanism</td><td>[29]</td></tr><tr><td>√</td><td>Machine breakdown, job insertion</td><td>×</td><td>Makespan, TEC</td><td>Hybrid deep Q network</td><td>[30]</td></tr><tr><td rowspan="5">RPS</td><td>×</td><td>Machine breakdown, job arrival</td><td>×</td><td>TEC, makespan, comprehensive reusability</td><td>Particle swarm arithmetic optimization</td><td>[8]</td></tr><tr><td>√</td><td>Job insertion</td><td>×</td><td>Makespan, workload balance, stability</td><td>Adaptive large neighborhood search algorithm</td><td>[10]</td></tr><tr><td>×</td><td>Machine breakdown</td><td>×</td><td>Total weighted tardiness</td><td>Two-stage genetic algorithm</td><td>[31]</td></tr><tr><td>×</td><td>Machine breakdown</td><td>×</td><td>Makespan, robustness</td><td>NSGA-II combined with RMc</td><td>[32]</td></tr><tr><td>×</td><td>Job arrival</td><td>×</td><td>Discontinuity rate, makespan deviation, sequence deviation</td><td>Improved particle swarm optimization algorithm</td><td>[7]</td></tr><tr><td rowspan="6">PRS</td><td>×</td><td>Job cancellation</td><td>×</td><td>Makespan, TEC</td><td>Reformative memetic algorithm</td><td>[33]</td></tr><tr><td>×</td><td>Machine breakdown, job arrival</td><td>Fuzzy processing time, variable machine speed</td><td>Makespan, TEC, average agreement index</td><td>Q-Learning based immune algorithm</td><td>[34]</td></tr><tr><td>×</td><td>Machine breakdown</td><td>×</td><td>Makespan, expected mean tardiness</td><td>Genetic algorithm</td><td>[35]</td></tr><tr><td>×</td><td>Machine breakdown, job insertion</td><td>×</td><td>Makespan, tardiness</td><td>VNS and artificial neural network</td><td>[36]</td></tr><tr><td>√</td><td>Job cancellation, machine breakdown, job insertion</td><td>×</td><td>Makespan</td><td>Hybrid artificial bee colony algorithm</td><td>[37]</td></tr><tr><td>√</td><td>Job cancellation, machine breakdown, AGV breakdown</td><td>AGV charging constraint</td><td>Makespan, TEC, rescheduling instability</td><td>Q-Learning based NSGA-II</td><td>our work</td></tr></table>

et al. [33] proposed a reformative memetic algorithm to solve the problem of job cancellation in distributed FJSP, and discussed the solution of job cancellation under different processing degrees of jobs. Chen et al. [34] adopted a predictive reactive rescheduling method for fuzzy scheduling problems under dynamic disturbances, and proposed an offline-based MILP model and an online-based rescheduling model. Gholami et al. [35] combined simulation and genetic algorithms to solve the dynamic scheduling problem of machine breakdown and generated a new scheduling solution through event-driven strategies and right-shift heuristics. Likewise, Adibi et al. [36] considered two event-driven rescheduling problems, random job arrivals and machine breakdown, and used artificial neural networks to adjust VNS parameters to improve algorithm performance. Li et al. [37] developed a hybrid artificial bee colony algorithm and used corresponding strategies for three kinds of emergency events. 

## 2.3. �-Learning and meta-heuristics

At present, some scholars have begun to notice that combining �-Learning and meta-heuristic algorithms to solve combinatorial op timization problems can improve the performance of algorithms. In the algorithms, �-Learning is mainly applied to adaptively adjust key parameters and strategy selection. Chen et al. [38] used �-Learning to adaptively adjust the crossover and mutation operations in their GA. Shahrabi et al. [39] used �-Learning to select three parameters for variable neighborhood search (VNS): the number of external iterations, the number of internal iterations, and the acceptance threshold. In addition, Yao et al. [40] proposed a MA combined with deep Q-network to adjust the crossover based on the population evolution. On the other hand, Zhang et al. [41] used the MA algorithm based on deep �-Learning to solve the integrated scheduling problem, and designed local search operators based on critical blocks. Zhao et al. [42] used the �-Learning method to select an appropriate low-level heuristic strategy according to historical information. Li et al. [43] improved the artificial bee colony (ABC) algorithm with �-Learning, designed a set of neighborhood structures based on knowledge and problem charac teristics, and used �-Learning to adaptively select the neighborhood search operator in each iteration. Similarly, Wang et al. [44] proposed a �-learning based ABC algorithm, which uses 12 types of population quality as states and 6 neighborhood search operators as actions. Wang et al. [45] established a dynamic rescheduling model based on multi agent technology, and developed a clustering and weighted �-Learning algorithm to select the optimal strategy in the dynamic scheduling process. Cheng et al. [46] proposed a bi-criteria �-Learning algorithm based on Pareto and index selection (QHH-BS). In each iteration, the algorithm can adaptively select an optimizer from three operators. 

Table 1 provides a summary of the literature concerning DFJSP and outlines the contributions of this paper. Based on the literature above, we can draw the following conclusions: 

(1) The dynamic scheduling problem has received widespread attention, but the dynamic scheduling problem in FJSP-T and the impact of AGV charging constraints are rarely considered. 

(2) Machine breakdown and job changes (such as job cancellation and insertion) are the most frequent disturbance events in DFJSP. In addition, there has been no relevant research on AGV breakdown thus far. 

(3) There are some literatures that combine the �-Learning algorithm and the metaheuristic algorithm, but there is no research on improving NSGA-II based on �-Learning to solve dynamic FJSP-T. 

Based on the above analysis, a rescheduling model for FJSP-T con sidering AGV charging constraints is constructed. We investigate two frequent disturbance events: job cancellation and machine breakdown, as well as the newly introduced disturbance event of AGV breakdown in FJSP-T, and propose three event-driven rescheduling strategies. An improved NSGA-II combined with �-Learning is innovatively developed to solve DFJSP-T. 

## 3. EJSP-T model

FJSP-T can be described in detail as follows: a job $i \in \{ 1 , 2 , \ldots , N \}$ is processed on machines � $\equiv \{ 1 , 2 , \dots , M \}$ , each job � has $O _ { i }$ operations, and each job is transported through AGV $a \in \{ 1 , 2 , \dots , A \} . ~ O _ { i j }$ denotes the $j _ { t h }$ operation of job �. The operation and AGV start from the loading and unloading area. According to the process route of each operation, the transportation task of each operation $O _ { i j }$ can be transported by any AGV, and each operation $O _ { i j }$ can be processed by any one of its optional machines. After the operation processing is completed, the AGV transports the operation to the unloading area. When the AGV is below the minimum power threshold, it needs to go to the charging area for charging. The schematic diagram of FJSP-T is shown in Fig. 1. More precisely, the problem consists of three sub-problems: 

<table><tr><td>Symbol</td><td>Description</td></tr><tr><td><eq>i, d, k</eq></td><td>Index of jobs</td></tr><tr><td><eq>j, h, f</eq></td><td>Index of operations</td></tr><tr><td><eq>t_{i,j,m}</eq></td><td>Processing time of operation <eq>O_{ij}</eq> on machine <eq>m</eq></td></tr><tr><td><eq>C_i</eq></td><td>Completion time of job <eq>i</eq></td></tr><tr><td><eq>C_m</eq></td><td>Completion time of machine <eq>m</eq></td></tr><tr><td><eq>C_{max}</eq></td><td>Makespan</td></tr><tr><td><eq>P_{m}^{busy}</eq></td><td>Unit processing energy consumption of machine <eq>m</eq></td></tr><tr><td><eq>P_{m}^{idle}</eq></td><td>Unit idle energy consumption of machine <eq>m</eq></td></tr><tr><td><eq>TEC</eq></td><td>Total machine energy consumption</td></tr><tr><td><eq>E_{idle}</eq></td><td>Total idle energy consumption of all machines</td></tr><tr><td><eq>E_{busy}</eq></td><td>Total processing energy consumption of all machines</td></tr><tr><td><eq>T_{i,j,m}^{s}</eq></td><td>Processing start time of <eq>O_{ij}</eq> on machine <eq>m</eq></td></tr><tr><td><eq>T_{i,j,a}^{l,e}</eq></td><td>Load end time of AGV <eq>a</eq> transport <eq>O_{ij}</eq></td></tr><tr><td><eq>T_{k,f,m}^{e}</eq></td><td>End processing time of <eq>O_{kf}</eq> on machine <eq>m</eq></td></tr><tr><td><eq>T_{i,j,a}^{l,s}</eq></td><td>Load start time of AGV <eq>a</eq> transport <eq>O_{ij}</eq></td></tr><tr><td><eq>T_{i,j,a}^{u,e}</eq></td><td>No-load end time of the AGV <eq>a</eq> transport <eq>O_{ij}</eq></td></tr><tr><td><eq>T_{i,j-1,m}^{e}</eq></td><td>Completion time of <eq>O_{i,j-1}</eq> on machine <eq>m</eq></td></tr><tr><td><eq>T_{d,h,a}^{u,s}</eq></td><td>No-load start time of the AGV <eq>a</eq> transport operation <eq>O_{dh}</eq></td></tr><tr><td><eq>t_a^{m\rightarrow c}</eq></td><td>Transportation time of AGV <eq>a</eq> from machine <eq>m</eq> to charging area</td></tr><tr><td><eq>t_a^{charge}</eq></td><td>Charging time of AGV <eq>a</eq></td></tr><tr><td><eq>T_a^{charge}</eq></td><td>Charging start time of AGV <eq>a</eq></td></tr><tr><td><eq>TQ_a</eq></td><td>Maximum power threshold of AGV <eq>a</eq></td></tr><tr><td><eq>LQ_a</eq></td><td>Minimum power threshold of AGV <eq>a</eq></td></tr><tr><td><eq>Q_{i,j,a}^{l,e}</eq></td><td>End-of-load power of <eq>O_{ij}</eq> transported by AGV <eq>a</eq></td></tr><tr><td><eq>Q_{d,h,a}^{u,s}</eq></td><td>No-load starting power of <eq>O_{dh}</eq> transported by AGV <eq>a</eq></td></tr><tr><td><eq>P_a^a</eq></td><td>Unit no-load transportation energy consumption of AGV <eq>a</eq></td></tr><tr><td><eq>P_a^l</eq></td><td>Unit load transportation energy consumption of AGV <eq>a</eq></td></tr><tr><td><eq>P_a^{charge}</eq></td><td>The charging rate of AGV <eq>a</eq></td></tr><tr><td><eq>x_{i,j,m}</eq></td><td>1 if <eq>O_{ij}</eq> is processed on machine <eq>m</eq>, otherwise 0</td></tr><tr><td><eq>y_{i,j,a}</eq></td><td>1 if <eq>O_{ij}</eq> is transported by AGV <eq>a</eq>, otherwise 0</td></tr><tr><td><eq>w_{i,j,a}</eq></td><td>1 if AGV <eq>a</eq> needs to be charged after transporting <eq>O_{ij}</eq>, otherwise 0</td></tr></table>

(1) the scheduling sequence problem (OS). 

(2) Assign operations to appropriate machines (MS). 

(3) Use the appropriate AGV transport operation (AS). 

For the FJSP-T model proposed in this paper, the following assump tions are made: 

(1) A job can only be transported by one AGV at the same time. 

(2) Each operation of the job can only be processed on one machine at the same time; 

(3) the energy consumption per unit time of AGV is different in no-load and load states 

(4) The minimum power threshold of AGV can complete a furthest distance task with the highest energy consumption and return to the charging area. There is no case of power loss midway, and AGV is not allowed to return to the charging area when it is loaded; 

(5) Assume that the AGV charging process is not interrupted unti the power reaches the highest threshold; 

(6) Path conflict is not considered. 

The notations used in this paper are given in Table 2. The FJSP-T model with the optimization objective of minimizing the makespan and TEC is established as follows. 

$$
\min C _ {m a x} = \max _ {1 \leq i \leq N} C _ {i}, \forall i.\tag{1}
$$

$$
\min T E C = E _ {b u s y} + E _ {i d l e}.\tag{2}
$$

![](images/0fca48d486af33dbf7b8d31a235bacf9f7d00865d3f8421ffdaa6a782e88fbad.jpg)



Fig. 1. An illustrative example of FJSP-T.


$$
E _ {b u s y} = \sum_ {m = 1} ^ {M} \sum_ {i = 1} ^ {N} \sum_ {j = 1} ^ {O _ {i}} t _ {i, j, m} \cdot x _ {i, j, m} \cdot P _ {m} ^ {b u s y}.\tag{3}
$$

$$
E _ {i d l e} = \sum_ {m = 1} ^ {M} (C _ {m} - \sum_ {i = 1} ^ {N} \sum_ {j = 1} ^ {O _ {i}} t _ {i, j, m} \cdot x _ {i, j, m}) \cdot P _ {m} ^ {i d l e}.
$$

$$
\sum_ {m = 1} ^ {M} x _ {i, j, m} \leq 1, \forall i, j.\tag{4}
$$

$$
\sum_ {a = 1} ^ {A} y _ {i, j, a} \leq 1, \forall i, j.\tag{5}
$$

(6) 

$$
T _ {i, j, m} ^ {s} \geq \max \{T _ {i, j, a} ^ {l, e}, T _ {k, f, m} ^ {e} \}, \forall i, j, k, f, m, a.\tag{7}
$$

$$
T _ {i, j, a} ^ {l, s} \geq \max \{T _ {i, j, a} ^ {u, e}, T _ {i, j - 1, m} ^ {e} \}, \forall i, j, m, a.
$$

$$
T _ {d, h, a} ^ {u, s} \geq T _ {i, j, a} ^ {l, e} + w _ {i, j, a} \left(t _ {a} ^ {m \to c} + t _ {a} ^ {c h a r g e}\right), \forall i, j, d, h, m, a.\tag{8}
$$

$$
t _ {a} ^ {\text {charge}} = \left(T Q _ {a} - \left(Q _ {i, j, a} ^ {l, e} - t _ {a} ^ {m \to c} \cdot P _ {a} ^ {u}\right)\right) / P _ {a} ^ {\text {charge}},\tag{9}
$$

$$
\forall i, j, k, r.\tag{10}
$$

$$
Q _ {k, f, a} ^ {u, s} = \left(1 - w _ {i, j, a}\right) \cdot Q _ {i, j, a} ^ {l, e} + w _ {i, j, a} \cdot T Q _ {a}, \forall i, j, a.
$$

$$
T _ {a} ^ {c h a r g e} = T _ {i, j, a} ^ {l, e} + t _ {a} ^ {m \rightarrow c}, \forall i, j, k, a.\tag{11}
$$

(12) 

Eqs. (1), (2) are the two objective functions of the model, which are makespan and TEC, respectively. Eqs. (3), (4) describe in detail the energy consumption when the machine is processing and idle. Eqs. (5), (6) respectively indicate that a job can only be transported by one AGV and processed by one machine at the same time. Eq. (7) represents the job processing time constraint. The start processing time of the $j _ { t h }$ operation of job � depends on the arrival time of the job as well as the completion time of the previous job on machine �. Eq. (8) represents the load start time constraint of AGV �. The start time of AGV � performing the transport task of operation $O _ { i j }$ depends on the end time of the no-load of AGV � as well as the end time of the previous operation of job �. Eq. (9) represents the no-load start time of AGV transportation operation. After an AGV completes the previous delivery task, if there is no need to charge, the AGV waits for the next task in the original position. If charging is required, the AGV needs to go to the charging area to charge to the highest power threshold before starting the next task. Eq. (10) represents the charging time. Eq. (11) indicates that if the AGV goes to the charging area for charging after the previous delivery task, the power of the AGV will be updated to the highest power. Otherwise, the current power is the remaining power after the completion of the previous transport task. Eq. (12) respectively represents the charging start time when the AGV arrives at the charging area. 

## 4. Rescheduling strategy and index

## 4.1. Rescheduling strategy

In dynamic scheduling problems, when disturbance events occur, appropriate rescheduling heuristics need to be employed to address them. Due to the inclusion of AGV scheduling with charging constraints in DFJSP-T, traditional rescheduling strategies may not be suitable for the dynamic scheduling of production systems. Therefore, this paper designs three rescheduling strategies for the three types of disturbance events in DFJSP-T, including job cancellation, machine breakdown, and AGV breakdown, and compares them with the complete rescheduling strategy in 6.5. In order to determine the status of jobs, machines and AGVs after different disturbance events, Algorithm1 is designed to obtain rescheduling information. 

Algorithm 1: Obtain Rescheduling Information

Input: Machine and AGV schedule $\tilde{M}_{m}$ , $\tilde{A}_{a}$ , event occur time $T_{d}$ , breakdown equipment $M_{b}$ , $A_{b}$ , machine and AGV maintenance time $mt_{m}$ , $at_{m}$ Output: Earliest available time of machine and AGV $ET_{m}$ , $ET_{a}$ , remaining operations $O_{ij}^{n}$ , job and AGV position $i_{position}$ , $a_{position}$ for each $m$ in $\tilde{M}_{m}$ do

if $T_{i,j,m}^{s} < T_{d} < T_{i,j,m}^{e}$ then

Machine $m$ stops after the current operation;

end

else if $T_{d} = T_{i,j,m}^{e}$ or machine is idle at time $T_{d}$ then

Machine $m$ stops immediately;

end $ET_{m\neq M_b} \leftarrow T_{stop}^m$ , $ET_{m=M_b} \leftarrow T_{stop}^m + mt_m$ ;

end

for each $a$ in $\tilde{A}_{a}$ do

//AGV is in a transport task or a charging task;

if Task start time < $T_{d}$ < Task end time then

AGV $a$ stops after the current task;

end

else if $T_{d}$ = Task end time or AGV is in idle then

AGV $a$ stops immediately;

end $ET_{a\neq A_b} \leftarrow T_{stop}^a$ , $ET_{a=A_b} \leftarrow T_{stop}^a + at_m$ ;

end

Determine $i_{position}$ and $a_{position}$ ;

Record the number of unfinished operations $O_{ij}^{n}$ ;

To clearly illustrate the DFJSP-T, we use an example, shown in Fig. 2(a), which is the gantt chart of an FJSP-T containing three jobs, three machines, and two AGVs. The operands of $J_1$ , $J_2$ , and $J_3$ are 4, 4, and 4, respectively. The makespan is 34, the TEC is 276.8, and the completion time of $J_1$ , $J_2$ , and $J_3$ is 34, 29, and 28, respectively. 

$$
J _ {c}
$$

$$
J _ {c}
$$

$$
O _ {i j} ^ {n}
$$

$$
J _ {c};
$$

$$
A S ^ {\prime} \leftarrow
$$

$$
O _ {2 3}, O _ {2 4}
$$

second operation of job 2 continues processing on machine $M _ { 2 }$ until completion. The order of operations on all machines remains the same as in the original solution. 

��_2: When the disturbance event is machine breakdown, it will disturb the initial solution more than the job cancellation, so the rescheduling strategy as follows is considered. 

For the operations on the non-broken machine, the original machine is still used for processing, so as to reduce other scheduling costs caused by the transformation of the processing machine. The job on the broken machine will continue processing on the machine after the machine repair is completed; In addition, the processing machine is randomly arranged for the subsequent unprocessed operation process of the broken machine. Note that changes in the AGV used for transport after rescheduling have little impact on the system, so the AGV used for all jobs in the rescheduling process can be changed to ensure that jobs are transported by the most suitable AGV and enter the process as soon as possible. Algorithm 3: Rescheduling Strategy 2 Input: Rescheduling information, initial solution, $M _ { b }$ Output: Rescheduling solution if the operation $O _ { i j }$ is processed on $M _ { b }$ then Randomly inserted into a machine on the optional machine set; else $O _ { i j }$ continues to process on the initial machine, and all operations maintain the initial order; end $A S ^ { \prime } $ random select; The rescheduling solution is obtained using QNSGA-II; As shown in Fig. 2(c), when machine $M _ { 1 }$ breaks down at time 10 and the maintenance time is $^ { 5 , }$ for the jobs on $M _ { 2 } , \ M _ { 3 } ,$ the original machine is still kept for processing. When the breakdown occurs, $O _ { 2 1 }$ is still processing on $M _ { 1 } ,$ so the second half of the processing of $O _ { 2 1 }$ will be carried out immediately after the maintenance of machine $M _ { 1 }$ Due to the delay of the completion time of the second lane operation of job 2 due to the breakdown of $M _ { 1 }$ , the scheduling solution of $A _ { 2 }$ is modified to transport job 3 in advance and then transport job 2. ��_3: For the DFJSP-T problem in this paper, AGV breakdown will also have an impact on the overall scheduling solution. Usually AGV breakdown may occur in two situations. First, the AGV is in transport operation, and the second AGV is in the process of no-load movement. In the case of AGV load transportation, the jobs currently transported by the AGV will continue to be transported by the AGV after the repair of the AGV, so the arrival time of the job will be affected. Based on this consideration, we decide that all jobs will still be processed on the original machine, but the processing sequence of the jobs can be exchanged. The AGV used by all jobs can also be adjusted to maximize the utilization of transportation resources in the event of an AGV breakdown. For the case of no-load transport movement of AGV. when the maintenance of AGV is completed, it will continue to run the end point of this sub-movement task in the initial solution, and then wait for the allocation of new tasks according to the new solution. Algorithm 4: Rescheduling Strategy 3 Input: Rescheduling information, initial solution, $A _ { b }$ Output: Rescheduling solution The processing machine ��<sup>′</sup> is constant for all operations, the processing order $o s \prime$ can be changed; $A S ^ { \prime } $ random select; The rescheduling solution is obtained using QNSGA-II; As shown in Fig. 2(d), AGV 1 fails next to machine $M _ { 3 }$ at time 1, and the power of AGV 1 reaches the lowest threshold. After a maintenance time of 5, the AGV continues to the charging area for charging. Al jobs are still fixed to the original machine for processing, and it can be found that in the rescheduling solution, all operations still maintain the original processing order 

![](images/2f287666a4611902fa3fb7e0caa872eb5c9f5e62cc11225d7a35740fc84080f8.jpg)


![](images/56d56d6ba8f41d51ac8d45bde065daf6427f822b68d8558721e4377d012a7adc.jpg)



(c) Machine breakdown


![](images/b1e390c9f96212c87d0925a5abba9a08066b8ae3eb26a1262d4c3f3f90bb2ce1.jpg)


![](images/e1edb0ad5c1d04e63d7493d07927be893faa3e588d91b7624bf34a904b1a696e.jpg)



(d) AGV breakdown



Fig. 2. Gantt chart of the example of DFJSP-T.


## 4.2. Rescheduling index

In DFJSP-T, a very important point to evaluate the quality of rescheduling solution is the instability of rescheduling. Rescheduling instability is generally defined as the change of the rescheduling solution with respect to the initial solution in all aspects. To measure the instability of a rescheduling solution, this paper defines a new index, rescheduling instability (RSI), which consists of the following three sub-indicators. 

(1)Machine change rate(MCR) 

$$
\min M C R = \min \frac {\widetilde {n} _ {o p}}{\min \{n _ {o r i} , n _ {n o w} \}}\tag{13}
$$

In Eq. (13), if the disturbance event is machine breakdown and AGV breakdown, MCR is equal to the ratio of the number of processes changed by the processing machine on the initial scheduling solution to the number of processes in the initial scheduling solution. If the disturbance event is a job cancellation, MCR measures the ratio of the number of processes in the rescheduling solution that changed the machine relative to the initial solution to the number of processes in the rescheduling solution. 

(2)AGV energy consumption balance rate(� ) 

$$
\min \sigma_ {a} = \min \sqrt {\frac {\sum_ {a = 1} ^ {A} \left(E _ {a} - \overline {{E}} _ {a}\right) ^ {2}}{A}}\tag{14}
$$

In this equation, 

$$
\overline {{E}} _ {a} = \frac {\sum_ {a = 1} ^ {A} E _ {a}}{A}\tag{15}
$$

$\sigma _ { a }$ calculates the standard deviation of energy consumption of all AGVs in the system to measure the degree of difference in energy consumption of each AGV during transportation. The smaller $\sigma _ { a }$ is, the more balanced job distribution of AGV is indicated. Here, $E _ { a }$ represents the total energy consumption of AGV �. 

(3)Average processing start-time deviation(APSD) 

$$
A P S D = \min \frac {\sum_ {i = 1} ^ {n} \sum_ {j = 1} ^ {O _ {i}} \left| \widehat {x} _ {i j} - x _ {i j} \right|}{n}\tag{16}
$$

APSD represents the average change in the job start processing time in the rescheduling solution relative to the initial scheduling solution, $\widehat { x } _ { i j }$ represents the start processing time of operation $O _ { i j }$ in the rescheduling solution, $x _ { i j }$ represents the start processing time of operation $O _ { i j }$ in the initial scheduling solution, � represents the operation after the disturbance event quantity. 

$$
\min R S I = \lambda_ {1} \cdot M C R + \lambda_ {2} \cdot \sigma_ {a} + \lambda_ {3} \cdot A P S D\tag{17}
$$

Considering the disturbance degree of the three subsystems of job, machine and AGV in DFJSP-T after dynamic events, the weight coeffi cients are given after normalization respectively, and finally the index to measure the instability of the rescheduling solution (RSI) is formed. It can be seen from the Eq. (17) that a higher RSI value indicates poorer robustness of the rescheduling solution. 

## 5. �-Learning based NSGA-II

## 5.1. Encoding and decoding

The proposed DFJSP-T involves scheduling three resources: jobs, machines, and AGVs. A three-segment coding method is utilized to encode the problem. As depicted in Fig. 3, the first segment is the job coding segment (OS), where each element represents the job number of its corresponding operation. The $j _ { t h }$ occurrence of a job number signifies the $j _ { t h }$ operation of that particular job. The second segment is the machine coding segment (MS), the number on MS represents the $m _ { t h }$ machine in the machine candidate set of the corresponding job. MS is arranged based on both the job number and operation number in ascending order. Lastly, we have AGV coding segment (AS) which follows a similar arrangement as MS, indicating that each process of a job is transported by its respective AGV. This encoding approach ensures simplicity and flexibility while guaranteeing feasibility of generated chromosome solutions during subsequent operations, thereby eliminating complex chromosome repair procedures. 

A left shift insertion active decoding rule is designed for DFJSP-T. The decoding process mainly includes three steps: (1) power check, (2) charging process, and (3) left shift insertion. The decoding process is described in detail in Algorithm 5. 

![](images/51770f2fc35068de514d77d92a0014b85951af747aff1a89e7e928cb48e98abe.jpg)



Fig. 3. Encoding of a three-segment code.


## 5.2. Hybrid initialization strategy

The quality of the initial population directly affects the convergence speed and performance of the algorithm, and individuals are usually generated by random initialization because there is no prior information. However, sometimes individuals are not evenly distributed in the search domain, which may make individuals far away from the global optimal solution and lead to low convergence speed. In the process of population initialization, chaotic variable search has more advantages than random search [47]. The equation of tent chaotic mapping (TCM) is as follows: 

$x_{t+1}=\left\{\begin{array}{c}2x_{t},0\leq x_{t}\leq0.5\\2\left(1-x_{t}\right),0.5<x_{t}\leq1\end{array}\right.$ (18)

Algorithm 5: Decoding Strategy

Input: OS, MS, AS, initial parameters
Output: Solution
for each $O_{ij}$ in OS do
    Find $M_{k}$ and $agv_{a}$ in MS and AS;
    for each AGV do
    if $Q_{a}\leq LQ_{a}$ then
    AGV immediately goes to charging;
    Update the data of $agv_{a}$ ;
    end
    end
    Get $T_{k,f,m}^{e}$ and $T_{i,j,a}^{l,e}$ and calculate $T_{i,j,a}^{l,e}$ by Eq. (7);
    Calculate time required for transportation;
    Update the data of $agv_{a}$ ;
    Get $T_{i,j,a}^{u,e}$ and $T_{i,j-1,m}^{e}$ to calculate $T_{i,j,a}^{l,s}$ by Eq. (8);
    Calculate $O_{ij}$ processing duration time;
    Inserted into the earliest available period of $M_{k}$ ;
    Update the data of $M_{k}$ ;
end 

To ensure the efficacy of TCM for small periodic and unstable periodic points generated in the iterative sequence, random variable rand(0.1) is introduced. Based on the characteristics of DFJSP-T and tent chaotic map, we design a variety of heuristic rules for each coding segment, and constructs a hybrid initialization strategy (HIS) containing three sub-populations. 

The size of the first sub-population is 60% of the population size, and the three coding segments of OS, MS and AS of the first sub population are initialized using tent chaotic map to form a sub-popula tion that is evenly distributed in space. 

The second sub-population is 20% of the population size. For the individuals in this population, tent chaotic map is used to generate the OS coding segment, and each operation is processed using the machine with the shortest current cumulative processing time and transported by the AGV closest to the job. The purpose of this sub-population is to improve machine utilization and reduce the energy consumption of AGVs when unloaded. 

The remaining 20% individuals are used as the third sub-population, and the operation on each individual in the population prefers the machine with the least processing energy consumption with a certain probability. In the OS coding segment, the AGV with the current minimum load is selected for transportation, and the load of the AGV is measured by the electricity consumption of the AGV in this paper. This sub-population ensures a lower TEC as well as load balancing of AGVs. 

Through the hybrid population strategy, the convergence speed of the iterative process can be increased while ensuring the diversity and distribution of the population. In the subsequent process of solving DFJSP-T, only part of the coding segments need to be initialized again according to the requirements of different rescheduling strategies in Section 4.1. The hybrid initialization strategy is described in Algorithm 6. 

Algorithm 6: Hybrid Initialization Strategy
Input: $M_{ij}$ , opera_set, pop
Output: Initial solution
Generate the first population by TCM;
Generate 20% × pop size OS codes by TCM;
for each individual in 20% × pop do
    for each $O_{ij}$ in OS do
    Select $M_k$ with the shortest cumulative processing time in $M_{ij}$ ;
    Update the cumulative processing time of $M_k$ ;
    Select $agv_a$ closest to the job;
    Update the position and power of $agv_a$ ;
    end
end
Generate 20% × pop size OS codes by TCM;
for each individual in 20% × pop do
    for each $O_{ij}$ in OS do
    if rand < 0.5 then
    Select $M_k$ with the minimum energy consumption in $M_{ij}$ ;
    else
    Randomly select a machine $M_k$ in $M_{ij}$ ;
    end
    Select $agv_a$ with the lowest cumulative load;
    Update the position and power of $agv_a$ ;
    end
end 

## 5.3. Selection, crossover and mutation operator

The role of the selection operator is to retain the genes of excellent individuals, which have high fitness values. By randomly selecting two individuals from the population for comparison, the binary tournament selection operator continuously selects good parent individuals to construct the population of the new generation. 

The crossover operation improves the exploration ability of the algorithm. According to the characteristics of DFJP-T, a crossover mechanism for three-segment coding is proposed. For OS coding segments, the precedence operation crossover [48] (POX) is used to ensure OS legitimacy in the offspring chromosome. The multi-point crossover [49] (MPX) is used for the machine coding segment MS. Because MPX operator is the crossover of the processing machines used in the same process, the generated offspring chromosome MS is a feasible solution. 

![](images/8d7bd4aeba07cbe6471c09566f3e2dec5095e459327d68cf687afed2242ce043.jpg)



Fig. 4. Schematic diagram of the population structure.


Similarly, the same crossover operator as MS is used in the AGV coding segment AS. 

The mutation operator enhances population diversity, enabling the algorithm to escape local optima and explore the solution space more extensively. Similar to the crossover operation, different mutation op erators are used according to the characteristics of the three-segment encoding. In OS, the process positions of two different jobs are exchanged arbitrarily. For MS and AS, replace the current device with another device from the set of available devices for the current process. 

## 5.4. Non-dominated sorting and crowding distance sorting

In MOPs, for two solutions � and �, � dominates � if � outperforms � under all objective functions. The process of non-dominated solution ranking is to divide all solutions into different levels according to their dominance relationship. For the solutions in each level, by giving priority to the solutions with low crowding degree, the diversity in the level can be preserved as much as possible to prevent the algorithm from falling into local optimal solutions. Both techniques are used in each iteration, and the population structure in the Q-NSGA-II iteration is shown in Fig. 4. 

## 5.5. �-Learning based local search

�-Learning algorithm has shown excellent performance in solving various heuristic problems, it usually consists of five elements, respectively is the agent, environment, action set, state set and reward function, forming a quintuple $( A , E , C , S , R )$ . At each decision time point, the agent selects the appropriate action based on the current state of the environment, and then updates the table of state–action mapping (�-table) based on the immediate rewards given by the environment. The �-table records the long-term expected reward for each state–action mapping, thus guiding the agent to make decisions and gradually learn the optimal strategy as it continuously interacts with the environment. The update equation of �-table is as follows. 

$$
\begin{array}{c} Q \left(S _ {t}, a _ {t}\right) = \alpha \left[ R + \gamma \max Q \left(S _ {t + 1}, a\right) \right] + (1 - \alpha) \\ \cdot Q \left(S _ {t}, a _ {t}\right) \end{array}\tag{19}
$$

In $\mathrm { E q . ~ } ( 1 9 ) , \mathrm { ~ } Q \left( S _ { t } , a _ { t } \right)$ represents the � value generated by taking the action $A _ { t }$ in the current $S _ { t }$ state. � represents the learning rate, � represents the discount factor, and � is the reward after performing the action $A _ { t } .$ . max $\boldsymbol { Q } \left( \boldsymbol { S } _ { t + 1 } , \boldsymbol { a } \right)$ represents the highest �-value for which the next state $S _ { t + 1 }$ takes all actions A. 

By combining the learning ability of �-learning and the global search ability of NSGA-II, the convergence and search efficiency of NSGA-II are improved. �-learning can be used in local search in so lution space to find high quality solutions near pareto frontier faster, thus speeding up the convergence process of the algorithm. The main concepts of �-learning are defined as follows. 


Table 3


<table><tr><td>State</td><td>Description</td><td>State</td><td>Description</td></tr><tr><td rowspan="2">1</td><td><eq>\gamma_n \in \varphi_1(1)</eq></td><td rowspan="2">2</td><td><eq>\gamma_n \in \varphi_1(1)</eq></td></tr><tr><td><eq>\gamma_n \in \varphi_2(1)</eq></td><td><eq>\gamma_n \in \varphi_2(2)</eq></td></tr><tr><td rowspan="2">3</td><td><eq>\gamma_n \in \varphi_1(2)</eq></td><td rowspan="2">4</td><td><eq>\gamma_n \in \varphi_1(2)</eq></td></tr><tr><td><eq>\gamma_n \in \varphi_2(1)</eq></td><td><eq>\gamma_n \in \varphi_2(2)</eq></td></tr></table>

![](images/a232d95c3647b9a6de8f6978a75e4ae44bad4736133e1eaf5e798e0454f444c5.jpg)



Fig. 5. Diagram of state division and reward setting.


�����. The exploitation ability of the algorithm is improved by determining the state in which the current solution is located and selecting the best action for each solution. This paper considers two conflicting objectives, makespan and TEC, so it is necessary to make a corresponding tradeoff between them. As shown in Fig. 5, the fitness values of all � individuals in the population under the �1 objective are calculated and sorted in ascending order, and the target value located on the median in the $f 1$ direction is found. The � individuals are divided into two regions with the target value as the limit. Likewise, find the median in the �2 direction and partition the space. In this way, the whole pareto plane is divided into four regions as states in �- learning. The detailed definitions of the four states are given in Table 3, where $\varphi _ { i } ( 1 )$ denotes the first part after all individuals are sorted in ascending order according to the $i _ { t h }$ objective value, and $\varphi _ { i } ( 2 )$ denotes the second part. 

������. In this paper, we classify reward values into three types based on the dominance relationship between the newly generated solution, denoted as �, and the old solution, represented by �. These categories entail three distinct cases: when the newly generated solution dominates the old one $\left( \alpha \ \succ \ \beta \right)$ , when it is dominated by the old solution $\left( \alpha \prec \beta \right) ,$ , and when neither solution dominates the other $\left( \alpha \simeq \beta \right)$ . The detailed reward �� function is defined as follows. 

$$
r d = \left\{ \begin{array}{c} \delta_ {1} + \sum_ {k = 1} ^ {K} \frac {f _ {\max} ^ {k} - \hat {f} ^ {k}}{f _ {\max} ^ {k} - f _ {\min} ^ {k}}, i f \alpha > \beta \\ 0, i f \alpha <   \beta \\ \delta_ {2} + \sum_ {k = 1} ^ {K} \frac {f _ {\max} ^ {k} - \hat {f} ^ {k}}{f _ {\max} ^ {k} - f _ {\min} ^ {k}}, i f \alpha \simeq \beta \end{array} \right.\tag{20}
$$

The reward function �� considers the dominance relationship between the newly generated solution and the initial solution, as well as the degree of optimization of the new solution on each objective. This method can assign higher rewards to actions that have better optimization effects on objective values. $\delta _ { 1 }$ and $\delta _ { 2 }$ as rewards for measuring the dominance relationship are set to 2 and 1, respectively. In addition, for two solutions that do not dominate each other, if the new solution is better than the old solution in one objective value, but worse than the old solution to a greater extent for another obiective value, the reward function will reduce the reward for that action. Such a reward function solves the problem of global exploration capability and local exploitation capability. 

![](images/d250db17ab339d39790e1b70b6e80062ad9c860613d2bf9d8d906e01ee71ac07.jpg)



Fig. 6. Framework for solving DFJSP-T model.


������. The �-greedy method is used for each individual action. Specifically, when the random probability is less than �, the action corresponding to the largest � value in the �-table in the current state is selected. When the random probability is greater than �, then one of the actions is randomly selected. In this paper, a dynamic � function is designed to guide the action selection in different iteration periods. The equation is as follows: 

$$
\varepsilon (g) = \frac {1}{1 + e ^ {1 . 1 - \frac {5 g}{G E N}}}\tag{21}
$$

Eq. (21) shows that in the early iteration process, the algorithm prefers to use more random actions to train the �-table. As the number of iterations � increases, the agent can select the most appropriate action by using the existing knowledge in the �-table to enhance the development ability of local search. 

������. In QNSGA-II, actions are defined as six neighborhood struc tures. The algorithm selects one neighborhood structure to enter the local search in each iteration. The design of the relevant domain structure is as follows. 

��_1: The operation of randomly selecting two adjacent positions and inserting any position in reverse order. 

��_2: Two operations are deleted randomly, and then inserted into the operation coding segment in the order of deletion. 

��_3: Randomly select the machine used in an operation and replace it with any other machine in its optional machine set for processing. 

��_4: Find the machine with the most processing jobs, process any operation from this machine, and modify it to the machine with the least load in the set of optional equipment. 

��_5: On the AGV coding segment, a random point position is used for transportation using other AGVs. 

��_6: The waiting time of a no-load AGV arriving in advance is used for the transportation of other jobs, that is, during the waiting time, a transportation task of other AGVs is replaced by this AGV for transportation, and it is set as the previous task of this no-load task. 

## 5.6. Framework for solving DFJSP-T

The framework for solving DFJSP-T proposed in this paper is shown in Fig. 6. The initial scheduling solution is generated by offline mode. When an disturbance event occurs, the corresponding rescheduling strategy is selected according to the type of disturbance event in online mode, and the new chromosome is re-decoded after obtaining the rescheduling information. It then returns to offline mode and regenerates the subsequent solution using the QNSGA-II algorithm guided by the rescheduling strategy. 

## 6. Experimental analysis

In this paper, we extend the MK benchmark proposed by Brandimarte [50] to construct the EMK benchmark for DFJSP-T. The number of AGVs is determined according to the number of operations, i.e., {job number - AGV number}, and we set three benchmarks of different sizes: {10-3}. {15-4}. {20-5}. All programs are coded and implemented in Matlab 2021b and run on an Intel(R) Core(TM) i9-13900K CPU @ 3.00 GHz with 128-GB RAM. 

## 6.1. Algorithm performance measures

For multi-objective optimization problems, the solutions generated by the algorithm are non-dominated on the pareto front, and therefore cannot be evaluated directly on the basis of the individual objective values. In order to measure the performance of QNSGA-II in solving DFJSP-T, we comprehensively investigates the algorithm in terms of convergence, diversity, and solution quality, using three evaluation criteria, including Hypervolume (HV) [51], Inverted Generational Distance (IGD) [52], and C-metric [53], respectively. HV measures the comprehensive performance of the algorithm, the larger HV, the better the algorithm performance. IGD measures the convergence and diversity of the algorithm. Contrary to HV, smaller IGD of the algorithm is better. C-metric measures the degree of dominance between the solutions produced by two algorithms. 


Table 4 Orthogonal table.


<table><tr><td>Serial number</td><td><eq>P_c</eq></td><td><eq>P_m</eq></td><td>α</td><td>γ</td><td>Value</td></tr><tr><td>1</td><td>0.7</td><td>0.05</td><td>0.1</td><td>0.7</td><td>0.5352</td></tr><tr><td>2</td><td>0.7</td><td>0.1</td><td>0.2</td><td>0.8</td><td>0.4754</td></tr><tr><td>3</td><td>0.7</td><td>0.15</td><td>0.3</td><td>0.9</td><td>0.4789</td></tr><tr><td>4</td><td>0.8</td><td>0.05</td><td>0.2</td><td>0.9</td><td>0.5513</td></tr><tr><td>5</td><td>0.8</td><td>0.1</td><td>0.3</td><td>0.7</td><td>0.6229</td></tr><tr><td>6</td><td>0.8</td><td>0.15</td><td>0.1</td><td>0.8</td><td>0.6675</td></tr><tr><td>7</td><td>0.9</td><td>0.05</td><td>0.3</td><td>0.8</td><td>0.2994</td></tr><tr><td>8</td><td>0.9</td><td>0.1</td><td>0.1</td><td>0.9</td><td>0.6879</td></tr><tr><td>9</td><td>0.9</td><td>0.15</td><td>0.2</td><td>0.7</td><td>0.4932</td></tr></table>

![](images/371ed663c3e3a67ea6a85c1fde4cb052d1d22c5f5437d401126c2996210d49c1.jpg)



Fig. 7. Main effects plot for HV index.


It is worth noting that the $P F _ { t r u e }$ is usually given in advance when computing the IGD, but there is no $P F _ { t r u e }$ for DFJSP-T so far. Therefore, we use the non-dominated solutions from the set of solutions obtained by all the comparison algorithms instead of $P F _ { t r u e } .$ 

## 6.2. Parameter setting

In order to investigate the effect of parameter settings on the performance of the proposed QNSGA-II, the Taguchi design of experiments methodology is used to analyze four key parameters: crossover probability $P _ { c } ,$ mutation probability $P _ { m } ,$ learning rate $\alpha ,$ and discount factor $\gamma .$ The orthogonal array L9 $( 3 ^ { 4 } )$ is shown in Table 4, where the QNSGA-II is repeated 20 times for each parameter combination, and the obtained main effects plot of the mean HV values is shown in Fig. 7. 

Fig. 7 shows the horizontal trend of the four parameters with respect to the HV index at the three levels. It can be observed that the QNSGA-II algorithm achieves better performance in terms of HV measure when the parameter levels are set to $P _ { c } = 0 . 8 , P _ { m } = 0 . 1 , \alpha = 0 . 1 \mathrm { a n d } \gamma = 0 . 9$ 

## 6.3. Effectiveness of new strategies on QNSGA-II

The main improvement of NSGA-II is the design of the hybrid initialization strategy and the local search based on �-Learning. In order to test the effectiveness of these improved strategies, we designed three corresponding variants of QNSGA-II. The classical NSGA-II algorithm is denoted as A, which uses the random generation method to construct the initialization population. The NSGA-II based on the hybrid initialization strategy is denoted B. C represents replacing the �-Learning-based neighborhood search in QNSGA-II with a general neighborhood search, that is, the choice of neighborhood structure is obtained by a random method. The parameter settings of the three algorithms A,B and C are the same as those of QNSGA-II. QNSGA-II and the three variants are run 20 times randomly on each instance. Table 5 shows the obtained HV average and IGD average on each instance for each algorithm. 

As shown in Table $^ { 5 , }$ algorithm A outperforms algorithm B in both the HV average and the IGD average in all instances. It is worth noting that the difference between the results of the two algorithms is very obvious, which indicates that the hybrid initialization strategy in this paper has a great effect on improving NSGA-II. Similarly, the results of algorithms B and C illustrate that the neighborhood search strategy in this paper is necessary. Finally, the results of QNSGA-II are better than that of algorithm C on most instances, which verifies the effectiveness of �-Learning algorithm. Table 6 shows that a large fraction of the solutions obtained by QNSGA-II can dominate the solutions produced by other algorithms. 

## 6.4. Comparative analysis with other algorithms

In this section, QNSGA-II is compared with three algorithms to verify the performance of the proposed algorithm. The three algorithms are NSGA-II, MOEA/D and MOPSO. Set the public parameter N = 100, the CPU running time of the three comparison algorithms is the same as QNSGA-II. The respective parameters of the algorithms are shown in Table 9. Each algorithm is run 20 times on each instance, and the average HV, IGD and C-metric values obtained by each algorithm for each instance are presented in Table 7 and Table 8. Furthermore, three different scale instances EMK01, EMK04 and EMK05 are selected, and the boxplots of the two objective values solved by the four algorithms are depicted. From Fig. 8, it can be observed that QNSGA-II performs the best in minimizing makespan and TEC. The test results above demonstrate the superiority of the QNSGA-II algorithm compared to others. 

## 6.5. Effectiveness of the rescheduling strategies

In order to evaluate the performance of the three rescheduling strategies, including their performance in minimizing the two objec tive values of makespan and TEC, and the stability of the generated rescheduling solution, we use (1) the strategy of executing the original scheduling scheme IS, (2) the rescheduling strategy of this paper RS, (3) the complete rescheduling strategy CS for strategy comparison. In order to simulate the demand for timely response of rescheduling solution in flexible job shop in real production environment, this paper sets the running time of rescheduling to be half of the running time of the initial scheduling, and the CPU running time of the three reschedul ing strategies on the same instance is equal. Examples of different scales are selected for each of the three disturbance events. In each instance, the disturbances generated in different periods are analyzed, and the impact of maintenance time after machine breakdown and AGV breakdown on the rescheduling solution is studied. 

$$
\bar {\tau} _ {i, j} = \frac {\tau_ {i , j} - \min \tau_ {i}}{\max \tau_ {i} - \min \tau_ {i}}\tag{22}
$$

For example, EMK01-20-5 in Table 11 represents a breakdown occurred at time 10 for a machine in instance EMK02 with a repair time of 5 units. Each instance is independently run 20 times to calculate average values for two objectives: makespan and TEC from 10 solutions obtained. The average values for three sub-indicators mentioned in 4.2: MCR, $\sigma _ { a } ,$ APSD are also calculated. The solutions generated by all three algorithms are combined and normalized using Eq. (22), with weights $\lambda _ { 1 } , \lambda _ { 2 } , \lambda _ { 3 }$ set as 0.3333,0.3333,0.3333. RSI is then calculated according to Eq. (17) and averaged across all three algorithms’ RSI values. Detailed results for job cancellation, machine breakdown, and AGV breakdown are shown in Table 10, Table 11, and Table 12 respectively. The tables show the objective values obtained by three rescheduling strategies, including makespan and TEC. Additionally, the tables display their performance in terms of three rescheduling-related sub-indicators and the RSI. 

Table 10 shows the results under the disturbance event of job cancellation. We can find that the solution obtained by RS 1 is better 


Table 5



Result of the HV and IGD obtained by QNSGA-II, A, B and C on each instance.


<table><tr><td rowspan="2">Instances</td><td colspan="2">QNSSGA-II</td><td colspan="2">A</td><td colspan="2">B</td><td colspan="2">C</td></tr><tr><td>HV</td><td>IGD</td><td>HV</td><td>IGD</td><td>HV</td><td>IGD</td><td>HV</td><td>IGD</td></tr><tr><td>EMK01</td><td>1.1319</td><td>0.0937</td><td>0.0320</td><td>1.1968</td><td>0.8918</td><td>0.1919</td><td>1.0380</td><td>0.1474</td></tr><tr><td>EMK02</td><td>1.1194</td><td>0.0384</td><td>0.0379</td><td>1.1998</td><td>0.8036</td><td>0.2552</td><td>1.0648</td><td>0.1142</td></tr><tr><td>EMK03</td><td>1.0923</td><td>0.0600</td><td>0.0204</td><td>1.2881</td><td>0.6646</td><td>0.3885</td><td>0.9317</td><td>0.2371</td></tr><tr><td>EMK04</td><td>1.0789</td><td>0.0655</td><td>0.0158</td><td>1.3000</td><td>0.9864</td><td>0.1459</td><td>0.9895</td><td>0.1568</td></tr><tr><td>EMK05</td><td>1.0806</td><td>0.0623</td><td>0.0294</td><td>1.2126</td><td>0.9849</td><td>0.1818</td><td>1.0251</td><td>0.0813</td></tr><tr><td>EMK06</td><td>1.0604</td><td>0.0683</td><td>0.0214</td><td>1.2371</td><td>0.6465</td><td>0.4552</td><td>0.7958</td><td>0.3134</td></tr><tr><td>EMK07</td><td>1.1466</td><td>0.0347</td><td>0.0286</td><td>1.1940</td><td>0.9151</td><td>0.1478</td><td>0.9999</td><td>0.1530</td></tr><tr><td>EMK08</td><td>1.0707</td><td>0.1078</td><td>0.0252</td><td>1.3060</td><td>0.8085</td><td>0.2898</td><td>0.9462</td><td>0.2067</td></tr><tr><td>EMK09</td><td>1.0148</td><td>0.0979</td><td>0.0225</td><td>1.2098</td><td>0.6693</td><td>0.3742</td><td>0.8914</td><td>0.2252</td></tr><tr><td>EMK10</td><td>1.1103</td><td>0.0603</td><td>0.0171</td><td>1.3187</td><td>0.5728</td><td>0.4713</td><td>1.0577</td><td>0.1081</td></tr></table>


Table 6



Result of the C-metric on by QNSGA-II, A, B and C each instance.


<table><tr><td>Instances</td><td>C(QNSGA-II,A)</td><td>C(A,QNSGA-II)</td><td>C(QNSGA-II,B)</td><td>C(B,QNSGA-II)</td><td>C(QNSGA-II,C)</td><td>C(C,QNSGA-II)</td></tr><tr><td>EMK01</td><td>1.0000</td><td>0.0000</td><td>0.8000</td><td>0.1000</td><td>0.6933</td><td>0.1333</td></tr><tr><td>EMK02</td><td>1.0000</td><td>0.0000</td><td>0.9000</td><td>0.1000</td><td>0.6000</td><td>0.1000</td></tr><tr><td>EMK03</td><td>1.0000</td><td>0.0000</td><td>1.0000</td><td>0.0000</td><td>0.6000</td><td>0.1817</td></tr><tr><td>EMK04</td><td>1.0000</td><td>0.0000</td><td>0.5714</td><td>0.3476</td><td>0.5714</td><td>0.3333</td></tr><tr><td>EMK05</td><td>1.0000</td><td>0.0000</td><td>0.5600</td><td>0.3400</td><td>0.4167</td><td>0.3500</td></tr><tr><td>EMK06</td><td>1.0000</td><td>0.0000</td><td>0.7778</td><td>0.1154</td><td>0.5741</td><td>0.0598</td></tr><tr><td>EMK07</td><td>1.0000</td><td>0.0000</td><td>0.6833</td><td>0.1917</td><td>0.7946</td><td>0.0000</td></tr><tr><td>EMK08</td><td>1.0000</td><td>0.0000</td><td>0.8750</td><td>0.1250</td><td>0.4063</td><td>0.5000</td></tr><tr><td>EMK09</td><td>1.0000</td><td>0.0000</td><td>1.0000</td><td>0.0000</td><td>0.3167</td><td>0.1026</td></tr><tr><td>EMK10</td><td>1.0000</td><td>0.0000</td><td>1.0000</td><td>0.0000</td><td>0.4444</td><td>0.4167</td></tr></table>


Table 7



Result of the HV and IGD obtained by multiple algorithms on each instance.


<table><tr><td rowspan="2">Instances</td><td colspan="2">QNSSGA-II</td><td colspan="2">NSGA-II</td><td colspan="2">MOEA/D</td><td colspan="2">MOPSO</td></tr><tr><td>HV</td><td>IGD</td><td>HV</td><td>IGD</td><td>HV</td><td>IGD</td><td>HV</td><td>IGD</td></tr><tr><td>EMK01</td><td>1.1954</td><td>0.0000</td><td>0.3909</td><td>0.6508</td><td>0.3100</td><td>0.7310</td><td>0.0567</td><td>1.1709</td></tr><tr><td>EMK02</td><td>1.1980</td><td>0.0000</td><td>0.4422</td><td>0.6270</td><td>0.4629</td><td>0.5816</td><td>0.0456</td><td>1.2503</td></tr><tr><td>EMK03</td><td>1.1996</td><td>0.0000</td><td>0.3540</td><td>0.7313</td><td>0.3754</td><td>0.6880</td><td>0.0560</td><td>1.2160</td></tr><tr><td>EMK04</td><td>1.2079</td><td>0.0000</td><td>0.3949</td><td>0.6588</td><td>0.3879</td><td>0.6510</td><td>0.0577</td><td>1.2116</td></tr><tr><td>EMK05</td><td>1.2076</td><td>0.0000</td><td>0.2776</td><td>0.7835</td><td>0.2139</td><td>0.8614</td><td>0.0298</td><td>1.2555</td></tr><tr><td>EMK06</td><td>1.2094</td><td>0.0000</td><td>0.4368</td><td>0.6412</td><td>0.3787</td><td>0.6947</td><td>0.0366</td><td>1.2889</td></tr><tr><td>EMK07</td><td>1.2099</td><td>0.0000</td><td>0.4354</td><td>0.6471</td><td>0.4557</td><td>0.6085</td><td>0.1021</td><td>1.1342</td></tr><tr><td>EMK08</td><td>1.2098</td><td>0.0000</td><td>0.3964</td><td>0.6966</td><td>0.3344</td><td>0.7477</td><td>0.0302</td><td>1.2020</td></tr><tr><td>EMK09</td><td>1.1969</td><td>0.0000</td><td>0.5895</td><td>0.4982</td><td>0.6604</td><td>0.4298</td><td>0.0584</td><td>1.2228</td></tr><tr><td>EMK10</td><td>1.1989</td><td>0.0000</td><td>0.4781</td><td>0.5812</td><td>0.3741</td><td>0.6841</td><td>0.0413</td><td>1.2696</td></tr></table>


Table 8



Result of the C-metric obtained by multiple algorithms on each instance.


<table><tr><td>Instances</td><td>C(QNSGA-II, NSGA-II)</td><td>C(NSGA-II, QNSGA-II)</td><td>C(QNSGA-II, MOPSO)</td><td>C(MOPSO, QNSGA-II)</td><td>C(QNSGA-II, MOEA/D)</td><td>C(NSGA-II, QNSGA-II)</td></tr><tr><td>EMK01</td><td>1.0000</td><td>0.0000</td><td>1.0000</td><td>0.0000</td><td>1.0000</td><td>0.0000</td></tr><tr><td>EMK02</td><td>1.0000</td><td>0.0000</td><td>1.0000</td><td>0.0000</td><td>1.0000</td><td>0.0000</td></tr><tr><td>EMK03</td><td>1.0000</td><td>0.0000</td><td>1.0000</td><td>0.0000</td><td>1.0000</td><td>0.0000</td></tr><tr><td>EMK04</td><td>1.0000</td><td>0.0000</td><td>1.0000</td><td>0.0000</td><td>1.0000</td><td>0.0000</td></tr><tr><td>EMK05</td><td>1.0000</td><td>0.0000</td><td>1.0000</td><td>0.0000</td><td>1.0000</td><td>0.0000</td></tr><tr><td>EMK06</td><td>1.0000</td><td>0.0000</td><td>1.0000</td><td>0.0000</td><td>1.0000</td><td>0.0000</td></tr><tr><td>EMK07</td><td>1.0000</td><td>0.0000</td><td>1.0000</td><td>0.0000</td><td>1.0000</td><td>0.0000</td></tr><tr><td>EMK08</td><td>1.0000</td><td>0.0000</td><td>1.0000</td><td>0.0000</td><td>1.0000</td><td>0.0000</td></tr><tr><td>EMK09</td><td>1.0000</td><td>0.0000</td><td>1.0000</td><td>0.0000</td><td>1.0000</td><td>0.0000</td></tr><tr><td>EMK10</td><td>1.0000</td><td>0.0000</td><td>1.0000</td><td>0.0000</td><td>1.0000</td><td>0.0000</td></tr></table>


Table 9


<table><tr><td>Algorithm</td><td>Parameters</td></tr><tr><td>QNSGGA-II</td><td><eq>P_c=0.8, P_m=0.1, \alpha=0.1, \gamma=0.9</eq></td></tr><tr><td>NSGA-II</td><td><eq>P_c=0.8, P_m=0.1</eq></td></tr><tr><td>MOEA/D</td><td>T=5</td></tr><tr><td>MOPSO</td><td>W=0.4, <eq>C_1=2, C_2=2</eq></td></tr></table>

than the IS solution in all instances. In the disturbance event ofjob can cellation, the RS_1 strategy and the IS strategy optimize the makespan and TEC by shifting the subsequent operations of the cancellation job to the left, using the idle time of the machine and AGV. The difference between the RS_1 solution and the IS solution is that RS_1 can reschedule the AGV to advance the start processing time of the job to a greater extent at the expense of the start processing time deviation of a small number of jobs. 

Compared with the CS solution, the RS_1 solution also performs better in most instances. This is because RS_1 maintains the machine sequence of each operation and the sequential processing order of jobs on all machines, maintains the stability of the OS and MS coding segments, and reduces the running complexity of the algorithm. In limited solution time, RS_1 can converge to a satisfactory solution faster. For the CS strategy, it is better than the RS_1 solution only on the small-scale instance EMK02-20. As the instance size increases it becomes increasingly difficult for CS to obtain a solution of high quality. At the same time, the CS strategy cannot guarantee the stability of the rescheduling solution, which is reflected in its poor performance on RSI. 

![](images/65e98427ca64af30eeb525fa01d94f9f1402d5b32b64acd6540ed52fd29b2d23.jpg)



(a)


![](images/9f33ff6ab2c57406cb3c3c4a90a136f9fdc72e3c9647c522e96d5a4d57428fee.jpg)



(b)


![](images/ae176f7ab6d41296e3f83159327e8dc50fb169a18397086b9b3f77fe101b2e05.jpg)



(c)


![](images/640abd99afc3ea37637f1693ce8f7b3a8e85080878544ff8c68e1738a7f1ec68.jpg)



(d)


![](images/3e3dd3a99ac4d26d8e640c42ee40221f5d94d3204351206e9e3f1868e70c4e8f.jpg)



(e)


![](images/abb70df9497dab5ba26975a2fc9583bdd4de8af27148decc272da983ba9728d8.jpg)



(f)



Fig. 8. Boxplots of the four algorithms solving for the objective values.



Table 10



Rescheduling results of three strategies under job cancellation event


<table><tr><td rowspan="2">Instances</td><td colspan="4">IS</td><td colspan="4">RS-3</td><td colspan="4">CS</td></tr><tr><td colspan="2">Makespan</td><td colspan="2">TEC</td><td colspan="2">Makespan</td><td colspan="2">TEC</td><td colspan="2">Makespan</td><td colspan="2">TEC</td></tr><tr><td>EMK02–20</td><td colspan="2">68.5000</td><td colspan="2">924.0600</td><td colspan="2">67.0000</td><td colspan="2">910.5500</td><td colspan="2">61.0000</td><td colspan="2">879.3000</td></tr><tr><td>EMK02–50</td><td colspan="2">72.6000</td><td colspan="2">946.6333</td><td colspan="2">67.6667</td><td colspan="2">913.3000</td><td colspan="2">69.4161</td><td colspan="2">933.4750</td></tr><tr><td>EMK07–50</td><td colspan="2">173.8633</td><td colspan="2">3097.7823</td><td colspan="2">173.0000</td><td colspan="2">3088.4333</td><td colspan="2">173.3333</td><td colspan="2">3116.9153</td></tr><tr><td>EMK07–100</td><td colspan="2">181.0000</td><td colspan="2">3154.0153</td><td colspan="2">174.6667</td><td colspan="2">3144.3333</td><td colspan="2">180.6125</td><td colspan="2">3158.8908</td></tr><tr><td rowspan="2">Instances</td><td colspan="3">Sub-indicators</td><td rowspan="2">RSI</td><td colspan="3">Sub-indicators</td><td rowspan="2">RSI</td><td colspan="3">Sub-indicators</td><td rowspan="2">RSI</td></tr><tr><td>MCR</td><td><eq>\sigma_a</eq></td><td>APSD</td><td>MCR</td><td><eq>\sigma_a</eq></td><td>APSD</td><td>MCR</td><td><eq>\sigma_a</eq></td><td>APSD</td></tr><tr><td>EMK02–20</td><td>0.0000</td><td>3.2413</td><td>1.0000</td><td>0.2409</td><td>0.0000</td><td>3.2381</td><td>1.2800</td><td>0.2412</td><td>0.1667</td><td>2.8575</td><td>2.0386</td><td>0.4218</td></tr><tr><td>EMK02–50</td><td>0.0000</td><td>3.3246</td><td>0.0000</td><td>0.3452</td><td>0.0000</td><td>3.1687</td><td>1.1333</td><td>0.3878</td><td>0.6667</td><td>2.2378</td><td>5.0475</td><td>0.7233</td></tr><tr><td>EMK07–50</td><td>0.0000</td><td>4.8235</td><td>1.3533</td><td>0.2361</td><td>0.0000</td><td>4.7147</td><td>1.4500</td><td>0.1874</td><td>0.5113</td><td>4.9863</td><td>4.2271</td><td>0.8069</td></tr><tr><td>EMK07–100</td><td>0.0000</td><td>4.6197</td><td>0.6667</td><td>0.1021</td><td>0.0000</td><td>4.6476</td><td>0.7518</td><td>0.1156</td><td>0.4051</td><td>5.6330</td><td>4.0897</td><td>0.8824</td></tr></table>


Table 11



Rescheduling results of three strategies under machine breakdown event.


<table><tr><td rowspan="2">Instances</td><td colspan="4">IS</td><td colspan="4">RS-3</td><td colspan="4">CS</td></tr><tr><td colspan="2">Makespan</td><td colspan="2">TEC</td><td colspan="2">Makespan</td><td colspan="2">TEC</td><td colspan="2">Makespan</td><td colspan="2">TEC</td></tr><tr><td>EMK01-20-5</td><td colspan="2">98.0000</td><td colspan="2">1027.2000</td><td colspan="2">98.5600</td><td colspan="2">973.0160</td><td colspan="2">112.3200</td><td colspan="2">1276.0040</td></tr><tr><td>EMK01-20-10</td><td colspan="2">104.4100</td><td colspan="2">1084.9017</td><td colspan="2">99.6667</td><td colspan="2">1057.3707</td><td colspan="2">117.2800</td><td colspan="2">1195.6080</td></tr><tr><td>EMK01-50-5</td><td colspan="2">95.3100</td><td colspan="2">1093.8417</td><td colspan="2">94.5933</td><td colspan="2">1069.1813</td><td colspan="2">105.7933</td><td colspan="2">1166.4920</td></tr><tr><td>EMK01-50-10</td><td colspan="2">99.3133</td><td colspan="2">1118.5597</td><td colspan="2">97.7633</td><td colspan="2">1108.1387</td><td colspan="2">112.0100</td><td colspan="2">1193.3600</td></tr><tr><td>EMK06-100-15</td><td colspan="2">328.0367</td><td colspan="2">5134.4385</td><td colspan="2">326.6800</td><td colspan="2">5185.8900</td><td colspan="2">354.5250</td><td colspan="2">5268.4910</td></tr><tr><td>EMK06-100-25</td><td colspan="2">336.2950</td><td colspan="2">5273.7233</td><td colspan="2">328.9633</td><td colspan="2">5185.4540</td><td colspan="2">359.7900</td><td colspan="2">5566.0987</td></tr><tr><td>EMK06-200-15</td><td colspan="2">337.8600</td><td colspan="2">5826.9648</td><td colspan="2">324.7800</td><td colspan="2">5758.5085</td><td colspan="2">350.8650</td><td colspan="2">5905.6420</td></tr><tr><td>EMK06-200-25</td><td colspan="2">335.0186</td><td colspan="2">5943.9803</td><td colspan="2">330.5129</td><td colspan="2">5717.1657</td><td colspan="2">370.5000</td><td colspan="2">6317.6500</td></tr><tr><td rowspan="2">Instances</td><td colspan="3">Sub-indicators</td><td>RSI</td><td colspan="3">Sub-indicators</td><td>RSI</td><td colspan="3">Sub-indicators</td><td>RSI</td></tr><tr><td>MCR</td><td><eq>\sigma_a</eq></td><td>APSD</td><td></td><td>MCR</td><td><eq>\sigma_a</eq></td><td>APSD</td><td></td><td>MCR</td><td><eq>\sigma_a</eq></td><td>APSD</td><td></td></tr><tr><td>EMK01-20-5</td><td>0.0000</td><td>4.6798</td><td>1.1323</td><td>0.0620</td><td>0.0089</td><td>5.3600</td><td>2.7333</td><td>0.2265</td><td>0.3637</td><td>6.0233</td><td>37.1565</td><td>0.9412</td></tr><tr><td>EMK01-20-10</td><td>0.0000</td><td>4.2708</td><td>3.4829</td><td>0.1322</td><td>0.0554</td><td>4.2987</td><td>4.9303</td><td>0.2204</td><td>0.3024</td><td>4.9370</td><td>22.4174</td><td>0.9028</td></tr><tr><td>EMK01-50-5</td><td>0.0000</td><td>4.2335</td><td>1.0817</td><td>0.1847</td><td>0.0945</td><td>4.0718</td><td>2.9739</td><td>0.3245</td><td>0.4103</td><td>3.9385</td><td>7.0952</td><td>0.6611</td></tr><tr><td>EMK01-50-10</td><td>0.0000</td><td>3.7295</td><td>3.0498</td><td>0.0902</td><td>0.0476</td><td>3.7759</td><td>4.1460</td><td>0.2497</td><td>0.2049</td><td>5.0606</td><td>25.7684</td><td>0.9021</td></tr><tr><td>EMK06-100-15</td><td>0.0000</td><td>5.8984</td><td>5.8845</td><td>0.2073</td><td>0.1057</td><td>5.8459</td><td>6.9594</td><td>0.3039</td><td>0.5409</td><td>6.5227</td><td>35.9147</td><td>0.8016</td></tr><tr><td>EMK06-100-25</td><td>0.0000</td><td>6.0978</td><td>10.9820</td><td>0.2241</td><td>0.1789</td><td>6.0616</td><td>19.0565</td><td>0.3330</td><td>0.4785</td><td>6.5162</td><td>26.9355</td><td>0.7183</td></tr><tr><td>EMK06-200-15</td><td>0.0000</td><td>5.8218</td><td>5.6706</td><td>0.2236</td><td>0.0783</td><td>5.7249</td><td>11.0223</td><td>0.2767</td><td>0.5749</td><td>6.2887</td><td>39.6907</td><td>0.7826</td></tr><tr><td>EMK06-200-25</td><td>0.0000</td><td>5.6031</td><td>7.5661</td><td>0.1099</td><td>0.0920</td><td>5.7141</td><td>10.7027</td><td>0.1823</td><td>0.6549</td><td>8.6600</td><td>31.1610</td><td>0.7205</td></tr></table>


Table 12



Rescheduling results of three strategies under AGV breakdown event.


<table><tr><td rowspan="2">Instances</td><td colspan="2">IS</td><td colspan="2">RS-3</td><td colspan="2">CS</td></tr><tr><td>Makespan</td><td>TEC</td><td>Makespan</td><td>TEC</td><td>Makespan</td><td>TEC</td></tr><tr><td>EMK04-20-5</td><td>148.3100</td><td>2114.7778</td><td>146.1250</td><td>2049.9528</td><td>157.3260</td><td>2358.6018</td></tr><tr><td>EMK04-20-10</td><td>153.0550</td><td>2088.6893</td><td>151.0775</td><td>2095.4343</td><td>162.8540</td><td>2449.1048</td></tr><tr><td>EMK04-50-5</td><td>140.1960</td><td>2057.6994</td><td>137.9575</td><td>2053.0273</td><td>149.0940</td><td>2252.3120</td></tr><tr><td>EMK04-50-10</td><td>156.6140</td><td>2149.6112</td><td>144.3800</td><td>2102.8510</td><td>148.3880</td><td>2293.5832</td></tr><tr><td>EMK10-200-15</td><td>475.5750</td><td>14134.0370</td><td>461.9900</td><td>13583.7320</td><td>505.9775</td><td>14922.8278</td></tr><tr><td>EMK10-200-25</td><td>473.0567</td><td>13745.3540</td><td>464.4133</td><td>13044.8563</td><td>507.4400</td><td>14888.2853</td></tr><tr><td>EMK10-300-15</td><td>464.2450</td><td>14168.0208</td><td>453.0933</td><td>14003.3750</td><td>480.9275</td><td>14684.8393</td></tr><tr><td>EMK10-300-25</td><td>473.8840</td><td>14215.8230</td><td>460.7500</td><td>14095.9243</td><td>468.7580</td><td>14537.8930</td></tr></table>

<table><tr><td rowspan="2">Instances</td><td colspan="3">Sub-indicators</td><td rowspan="2">RSI</td><td colspan="3">Sub-indicators</td><td rowspan="2">RSI</td><td colspan="3">Sub-indicators</td><td rowspan="2">RSI</td></tr><tr><td>MCR</td><td><eq>\sigma_a</eq></td><td>APSD</td><td>MCR</td><td><eq>\sigma_a</eq></td><td>APSD</td><td>MCR</td><td><eq>\sigma_a</eq></td><td>APSD</td></tr><tr><td>EMK04-20-5</td><td>0.0000</td><td>5.5158</td><td>7.8220</td><td>0.1966</td><td>0.0000</td><td>5.7033</td><td>9.6450</td><td>0.2691</td><td>0.2579</td><td>5.9589</td><td>29.5960</td><td>0.7852</td></tr><tr><td>EMK04-20-10</td><td>0.0000</td><td>5.6930</td><td>11.9950</td><td>0.1853</td><td>0.0000</td><td>5.9219</td><td>13.9350</td><td>0.2687</td><td>0.2972</td><td>6.1601</td><td>21.8640</td><td>0.7221</td></tr><tr><td>EMK04-50-5</td><td>0.0000</td><td>5.0160</td><td>4.9360</td><td>0.1588</td><td>0.0000</td><td>5.1199</td><td>9.1550</td><td>0.2253</td><td>0.2595</td><td>5.4789</td><td>17.3960</td><td>0.6466</td></tr><tr><td>EMK04-50-10</td><td>0.0000</td><td>5.2354</td><td>14.8640</td><td>0.2062</td><td>0.0000</td><td>5.1818</td><td>11.5733</td><td>0.1637</td><td>0.2657</td><td>5.4399</td><td>18.5720</td><td>0.5856</td></tr><tr><td>EMK10-200-15</td><td>0.0000</td><td>6.5146</td><td>2.7625</td><td>0.0911</td><td>0.0000</td><td>6.4368</td><td>14.8200</td><td>0.1490</td><td>0.5764</td><td>7.0042</td><td>37.5425</td><td>0.7683</td></tr><tr><td>EMK10-200-25</td><td>0.0000</td><td>6.3175</td><td>24.7167</td><td>0.1376</td><td>0.0000</td><td>6.3428</td><td>25.5567</td><td>0.1463</td><td>0.5136</td><td>7.1298</td><td>75.5000</td><td>0.8352</td></tr><tr><td>EMK10-300-15</td><td>0.0000</td><td>7.2898</td><td>9.7475</td><td>0.2029</td><td>0.0000</td><td>6.7194</td><td>9.7933</td><td>0.1576</td><td>0.5292</td><td>6.9116</td><td>22.4125</td><td>0.6279</td></tr><tr><td>EMK10-300-25</td><td>0.0000</td><td>6.1827</td><td>18.1900</td><td>0.2612</td><td>0.0000</td><td>6.2469</td><td>14.4050</td><td>0.2548</td><td>0.4980</td><td>6.4224</td><td>27.3440</td><td>0.7195</td></tr></table>

![](images/e7b779fe15ee93627a6f4c37a64a8bc7e3c293cebe4c6f2c31585f055c85dc87.jpg)



(a) Instance of job cancellation


![](images/8b4c1d85c2c851ed877f68f153d2ce11f2f2e282b89824b74eb4e6d035f98ecf.jpg)



(b) Instance of machine breakdown


![](images/0476774b3b4a7d2df7d389d18ed7871a91b789e1d8dd473ab33c87e9ef97dda8.jpg)



(c) Instance of AGV breakdown



Fig. 9. RSI of different strategies under three disturbance events.


![](images/5ada0f583251fdc5be00d6fd2f8e3b5ffc812952fe00f62dd5fe1dd4ade748c8.jpg)



Fig. 10. Gantt chart of EMK02 instance(Makespan = 65, TEC = 960.5).


Table 11 shows the results of three rescheduling solutions under machine breakdown. Similarly, since the RS_2 strategy ensures that jobs on non-broken machines are still processed on the original machine, RS_2 can still obtain a more satisfactory solution in a limited number of iterations, and also maintains good stability. Under different breakdown occurrence times and different maintenance durations, the solutions obtained by the RS_2 strategy are better than the IS solution and the CS solution in most instances. In instances EMK01-20-5 and EMK06-100-15, the RS_2 solution does not dominate the IS solution, probably because the disturbance caused by machine breakdown is more likely to be absorbed by the subsequent scheduling process. 

![](images/adf8a2955dc513d5216308ba54dd8ce26675e6da81ce2f9bdb48c48b6ecfbb57.jpg)



Fig. 11. Gantt chart of rescheduling solution for RS_1 strategy(Makespan = 63, TEC = 897.8).


![](images/e4a545c212c026c49537e2abffb0883ce81a623130cd58258be3150ca81d694f.jpg)



Fig. 12. Gantt chart of rescheduling solution for RS_2 strategy(Makespan = 71, TEC = 986.9).


Table 12 shows the comparison results under the disturbance event of AGV breakdown. Similarly, we can find that RS_3 is better than the other two solutions in both targets of makespan and TEC. Compared with the IS strategy, the RS_3 strategy reduces the constraints on the job processing sequence and AGV scheduling. In this way, the processing time of other jobs on the machine can be reasonably advanced and the delaved arrival time of jobs due to AGV breakdown can be reduced. In addition, we found that the RSI value of the RS_3 solution is better than that of the IS solution on the EMK04-50-10, EMK10-300-15, and EMK10-300-25 instances. This may indicate that under the condition of tight transportation resources, if the AGV breakdown occurs for a long time in the later scheduling period, the disturbance caused by the breakdown cannot be eliminated well by continuing to execute the initial solution. 

Fig. 9 illustrates the RSI of different strategies under three types of disturbance events. It can be observed that the RSI of the proposed RS strategy is comparable to that of the IS strategy. Particularly in sce narios involving job cancellation and AGV breakdown, the RS strategy even outperforms the IS strategy in some instances, demonstrating its effectiveness in maintaining rescheduling stability. Furthermore, when comparing the RSI across the three disturbance events, it can be found that the machine breakdown is the most disturbing to the scheduling solution. Additionally, the RSI of the CS strategy is significantly higher than that of the other two strategies, indicating a substantial deviation from the initial scheduling solution, which undermines the stability of the rescheduling solution. 

To sum up, this paper designs three different rescheduling strategies RS based on the characteristics of different disturbance events, which can simplify the algorithm complexity to obtain better performance solutions under the condition of limited scheduling time, while taking into account the stability of rescheduling solutions. Due to the lim ited rescheduling time, the algorithm of complete rescheduling cannot converge to the optimal solution in the specified time. Comparing the RS solution with the CS solution, it can be found that the complete rescheduling solution is inferior to the RS solution in terms of the values on the two objectives as well as the RSI. It follows that complete rescheduling is not an appropriate strategy in time-limited rescheduling problems. 

Fig. 10 shows the gantt chart of the initial scheduling solution for the EMK02 instance. The occurrence time of the disturbance events is set at time 10, and the maintenance time for machine and AGV breakdown is set to 10. The gantt charts of the rescheduling solution under the influence of three disturbance events such as job cancellation, machine breakdown, and AGV breakdown are shown in Fig. 11, 12, and 13. Makespan and TEC are also calculated for each rescheduling solution. 

![](images/f0064b19492dd44eab4e4d16c9824318f90920b968423a6382086b6be744981a.jpg)



Fig. 13. Gantt chart of rescheduling solution for RS_3 strategy(Makespan = 74, TEC = 1004).


## 7. Conclusions

This paper proposes a dynamic scheduling problem for the flex ible job shop with limited transportation resources. A rescheduling model is constructed to minimize makespan and TEC; corresponding rescheduling strategies under three disturbance events such as job cancellation, machine breakdown and AGV breakdown are proposed, and a rescheduling instability indicator is introduced. Compared with the strategy of continuing to execute the initial scheduling solution and the complete rescheduling strategy, the rescheduling strategies RS can obtain the best solution at the two target values. At the same time, it also performs well in terms of the stability of the rescheduling solution. Furthermore, a �-Learning based QNSGA-II is proposed to solve this problem. By combining �-Learning and local search, historical search experience is used to guide the selection of neighborhood structures. And a problem-oriented mixed population strategy is proposed, which effectively improves the quality and distribution of the initial popula tion. A large number of comparative experiments show that QNSGA-II can effectively solve DFJSP-T. 

In future work, we will continue to study other disturbance events that may occur in DFJSP-T. At the same time, we will also explore how to apply deep reinforcement learning to solve this problem. In addition, how to design an efficient neighborhood structure for the FJSP-T problem is also a focus of future research. 

## CRediT authorship contribution statement

Rensheng Chen: Writing – original draft, Methodology, Conceptu alization. Bin Wu: Writing – review & editing, Supervision, Conceptual ization. Hua Wang: Writing – review & editing, Project administration. Huagang Tong: Visualization, Validation. Feiyi Yan: Software. 

## Declaration of competing interest

The authors declare that they have no known competing finan cial interests or personal relationships that could have appeared to influence the work reported in this paper. 

## Data availability

No data was used for the research described in the article. 

## Acknowledgments

This work is supported by the General Project of the National Social Science Fund of China (Grant No. 20BGL025), the National Key Research and Development Program of China (Grant No. 2021YFB3301300). 

## References



[1] P.L. Mareddy, S.R. Narapureddy, V.R. Dwivedula, P.R. Karanam, Development of scheduling methodology in a multi-machine flexible manufacturing system without tool delay employing flower pollination algorithm, Eng. Appl. Artif. Intell. 115 (2022) 105275, http://dx.doi.org/10.1016/j.engappai.2022.105275. 





[2] J. Xie, L. Gao, K. Peng, X. Li, H. Li, Review on flexible job shop scheduling, IET Collaborat. Intell. Manuf. 1 (3) (2019) 67–77. 





[3] M. Mousavi, H.J. Yap, S.N. Musa, F. Tahriri, S.Z. Md Dawal, Multi-objective AGV scheduling in an FMS using a hybrid of genetic algorithm and particle swarm optimization, PLoS One 12 (3) (2017) e0169817. 





[4] B. Reddy, C. Rao, A hybrid multi-objective GA for simultaneous scheduling of machines and AGVs in FMS, Int. J. Adv. Manuf. Technol. 31 (5) (2006) 602–613. 





[5] I.A. Chaudhry, S. Mahmood, M. Shami, Simultaneous scheduling of machines and automated guided vehicles in flexible manufacturing systems using genetic algorithms, J. Cent. S. Univ. 18 (2011) 1473–1486. 





[6] S.M. Homayouni, D.B. Fontes, Production and transport scheduling in flexible job shop manufacturing systems, J. Global Optim. 79 (2) (2021) 463–502. 





[7] Z. Wang, J. Zhang, S. Yang, An improved particle swarm optimization algorithm for dynamic job shop scheduling problems with random job arrivals, Swarm Evol. Comput. 51 (2019) 100594. http://dx.doi.org/10.1016/i.swevo.2019.100594 





[8] J. Duan, J. Wang, Robust scheduling for flexible machining job shop subject to machine breakdowns and new job arrivals considering system reusability and task recurrence, Expert Syst. Appl. 203 (2022) 117489, http://dx.doi.org/10. 1016/i.eswa.2022.117489 





[9] W. Ren, Y. Yan, Y. Hu, Y. Guan, Joint optimisation for dynamic flexible job shop scheduling problem with transportation time and resource constraints, Int. J. Prod. Res. 60 (18) (2022) 5675–5696. 





[10] J. Liu, B. Sun, G. Li, Y. Chen, Multi-objective adaptive large neighbourhood search algorithm for dynamic flexible job shop schedule problem with trans portation resource, Eng. Appl. Artif. Intell. 132 (2024) 107917, http://dx.doi. org/10.1016/j.engappai.2024.107917. 





[11] I. Driss, K.N. Mouss, A. Laggoun, A new genetic algorithm for flexible job-shop scheduling problems, J. Mech. Sci. Technol. 29 (2015) 1273–1281. 





[12] P. Ngatchou, A. Zarei, A. El-Sharkawi, Pareto multi objective optimization, in: Proceedings of the 13th International Conference on. Intelligent Systems Application To Power Systems. JEEE. 2005, pp. 84–91 





[13] K. Gao, Z. Cao, L. Zhang, Z. Chen, Y. Han, Q. Pan, A review on swarm ll d l l h f l fl bl b h h d l problems, IEEE/CAA J. Autom. Sin. 6 (4) (2019) 904–916. 





[14] K. Deb, A. Pratap, S. Agarwal, T. Meyarivan, A fast and elitist multiobjective genetic algorithm: NSGA-II, IEEE Trans. Evol. Comput, 6 (2) (2002) 182–197. 





[15] M.E.H. Sadati, B. Çatay, A hybrid variable neighborhood search approach for the multi-depot green vehicle routing problem, Transp. Res. Part E: Logist. Transp. Rey. 149 (2021) 102293, http://dx.doi.org/10.1016/i,tre.2021.102293 





[16] Z. Pan, L. Wang, J. Wang, J. Lu, Deep reinforcement learning based optimiza tion algorithm for permutation flow-shop scheduling, IEEE Trans. Emerg. Top. Comput. Intell. 7 (4) (2021) 983–994. 





[17] L. Deroussi, S. Norre, Simultaneous scheduling of machines and vehicles for the flexible job shop problem, in: International Conference on Metaheuristics and Nature Inspired Computing, Djerba Island Tunisia, 2010, pp. 1–2. 





[18] Z. Pan, L. Wang, J. Zheng, J.-F. Chen, X. Wang, A learning-based multi population evolutionary optimization for flexible job shop scheduling problem with finite transportation resources, IEEE Trans. Evol. Comput. (2022). 





[19] J. Liu, B. Sun, G. Li, Y. Chen, An integrated scheduling approach considering dispatching strategy and conflict-free route of AMRs in flexible job shop, Int. J. Adv. Manuf. Technol. 127 (3) (2023) 1979–2002. 





[20] J. Yan, Z. Liu, C. Zhang, T. Zhang, Y. Zhang, C. Yang, Research on flexible job shop scheduling under finite transportation conditions for digital twin workshop, Robot. Comput.-Integr. Manuf. 72 (2021) 102198. 





[21] G. Xu, Q. Bao, H. Zhang, Multi-objective green scheduling of integrated flexible job shop and automated guided vehicles, Eng. Appl. Artif. Intell. 126 (2023) 106864. 





[22] J. Li, J. Deng, C. Li, Y. Han, J. Tian, B. Zhang, C. Wang, An improved Jaya algorithm for solving the flexible job shop scheduling problem with transportation and setup times, Knowl.-Based Syst. 200 (2020) 106032, http: //dx.doi.org/10.1016/i.knosys.2020.106032 





[23] X. Lyu, Y. Song, C. He, Q. Lei, W. Guo, Approach to integrated scheduling prob lems considering optimal number of automated guided vehicles and conflict-free routing in flexible manufacturing systems, IEEE Access 7 (2019) 74909–74924. 





[24] M.S. Kumar, R. Janardhana, C. Rao, Simultaneous scheduling of machines and vehicles in an FMS environment with alternative routing, Int. J. Adv. Manuf. Technol. 53 (2011) 339–351. 





[25] H.E. Nouri, O. Belkahla Driss, K. Ghédira, Simultaneous scheduling of machines and transport robots in flexible job shop environment using hybrid metaheuristic based on clustered holonic multiagent model, Comput. Ind. Eng. 102 (2016) 488–501, http://dx.doi.org/10.1016/i.cie.2016.02.024. 





[26] S. Luo, Dynamic scheduling for flexible job shop with new job insertions by deep reinforcement learning, Appl. Soft Comput. 91 (2020) 106208, http://dx. doi.org/10.1016/j.asoc.2020.106208. 





[27] L. Cai, W. Li, Y. Luo, L. He, Real-time scheduling simulation optimisation of job shop in a production-logistics collaborative environment, Int. J. Prod. Res. 61 (5) (2023) 1373–1393. 





[28] M. Ghaleb, H. Zolfagharinia, S. Taghipour, Real-time production scheduling in the Industry-4.0 context: Addressing uncertainties in job arrivals and machine breakdowns, Comput. Oper. Res. 123 (2020) 105031, http://dx.doi.org/10.1016/ j.cor.2020.105031. 





[29] H. Luo, J. Fang, G.Q. Huang, Real-time scheduling for hybrid flowshop in ubiquitous manufacturing environment, Comput. Ind. Eng. 84 (2015) 12–23. 





[30] Y. Li, W. Gu, M. Yuan, Y. Tang, Real-time data-driven dynamic scheduling for flexible job shop with insufficient transportation resources using hybrid deep q network. Robot, Comput-Integr. Manuf, 74 (2022) 102283. 





[31] L. Liu. H.-v. Gu. Y.-g. Xi. Robust and stable scheduling of a single machine with random machine breakdowns. Int. J. Ady. Manuf, Technol. 31 (2007) 645–654 





[32] Y. Yang, M. Huang, Z. Yu Wang, Q. Bing Zhu, Robust scheduling based l h f b b fl bl b h bl h machine breakdowns, Expert Syst. Appl. 158 (2020) 113545, http://dx.doi.org/ 10.1016/j.eswa.2020.113545. 





[33] N. Zhu, G. Gong, D. Lu, D. Huang, N. Peng, H. Qi, An effective reformative memetic algorithm for distributed flexible job-shop scheduling problem with order cancellation, Expert Syst. Appl. 237 (2024) 121205. 





[34] X. long Chen, J. qing Li, Y. Xu, Q-learning based multi-objective immune algorithm for fuzzy flexible job shop scheduling problem considering dynamic disruptions, Swarm Evol. Comput. 83 (2023) 101414, http://dx.doi.org/10.1016/ j.swevo.2023.101414. 





[35] M. Gholami, M. Zandieh, Integrating simulation and genetic algorithm to schedule a dynamic flexible job shop, J. Intell. Manuf. 20 (2009) 481–498. 





[36] M. Adibi, M. Zandieh, M. Amiri, Multi-objective scheduling of dynamic job shop using variable neighborhood search, Expert Syst. Appl. 37 (1) (2010) 282–287, http://dx.doi.org/10.1016/j.eswa.2009.05.001, URL: https://www.sciencedirect. com/science/article/pii/S0957417409004199 





[37] X. Li, Z. Peng, B. Du, J. Guo, W. Xu, K. Zhuang, Hybrid artificial bee colony algorithm with a rescheduling strategy for solving flexible job shop scheduling problems, Comput. Ind. Eng. 113 (2017) 10–26. 





[38] R. Chen, B. Yang, S. Li, S. Wang, A self-learning genetic algorithm based on reinforcement learning for flexible job-shop scheduling problem, Comput. Ind Eng. 149 (2020) 106778, http://dx.doi.org/10.1016/j.cie.2020.106778. 





[39] J. Shahrabi, M.A. Adibi, M. Mahootchi, A reinforcement learning approach to parameter estimation in dynamic job shop scheduling, Comput. Ind. Eng. 110 (2017) 75–82, http://dx.doi.org/10.1016/j.cie.2017.05.026, URL: https://www. sciencedirect.com/science/article/pii/S0360835217302309. 





[40] Y. Yao, X. Li, L. Gao, A DQN-based memetic algorithm for energy-efficient job shop scheduling problem with integrated limited AGVs, Swarm Evol. Comput. 87 (2024) 101544. 





[41] F. Zhang, R. Li, W. Gong, Deep reinforcement learning-based memetic algorithm for energy-aware flexible job shop scheduling with multi-AGV, Comput. Ind. Eng. 189 (2024) 109917. 





[42] F. Zhao, S. Di, L. Wang, A hyperheuristic with Q-learning for the multiobjective energy-efficient distributed blocking flow shop scheduling problem, IEEE Trans. Cybern. (2022). 





[43] H. Li, K. Gao, P.-Y. Duan, J.-Q. Li, L. Zhang, An improved artificial bee colony algorithm with Q-learning for solving permutation flow-shop scheduling problems, IEEE Trans. Syst., Man. Cybern. Syst. 53 (5) (2022) 2684–2693. 





[44] J. Wang, D. Lei, J. Cai, An adaptive artificial bee colony with reinforcement learning for distributed three-stage assembly scheduling with maintenance, Appl. Soft Comput. 117 (2022) 108371, http://dx.doi.org/10.1016/j.asoc.2021. 108371. 





[45] Y.-F. Wang, Adaptive job shop scheduling strategy based on weighted Q-learning algorithm, J. Intell. Manuf. 31 (2) (2020) 417–432. 





[46] L. Cheng, Q. Tang, L. Zhang, Z. Zhang, Multi-objective Q-learning-based hyperheuristic with bi-criteria selection for energy-aware mixed shop scheduling, Swarm Evol. Comput. 69 (2022) 100985, http://dx.doi.org/10.1016/j.swevo. 2021.100985. 





[47] Y. Li. M. Han, O. Guo, Modified whale optimization algorithm based on tent chaotic mapping and its application in structural optimization, KSCE J. Civ. Eng. 24 (12) (2020) 3703–3713 





[48] R. Li, W. Gong, L. Wang, C. Lu, S. Jiang, Two-stage knowledge-driven evolu tionary algorithm for distributed green flexible job shop scheduling with type-2 fuzzy processing time, Swarm Evol. Comput. 74 (2022) 101139. 





[49] Y. An, X. Chen, K. Gao, L. Zhang, Y. Li, Z. Zhao, Integrated optimization of real-time order acceptance and flexible job-shop rescheduling with multi-level imperfect maintenance constraints. Swarm Evol. Comput. 77 (2023) 101243 





[50] P. Brandimarte, Routing and scheduling in a flexible job shop by tabu search, Ann. Oper. Res. 41 (3) (1993) 157–183. 





[51] A.P. Guerreiro, C.M. Fonseca, L. Paquete, The hypervolume indicator: Coml bl d l h ( ) ( ) 1-42. 





[52] H. Ishibuchi, H. Masuda, Y. Tanigaki, Y. Nojima, Modified distance calculation in generational distance and inverted generational distance, in: Evolutionary Multi Criterion Optimization: 8th International Conference, EMO 2015. GuimarãEs Portugal, March 29–April 1, 2015. Proceedings, Part II 8, Springer, 2015, pp. 110-125. 





[ ] i l k f i i l i bj i optimization, in: 2015 Latin American Computing Conference, CLEI, IEEE, 2015, 

