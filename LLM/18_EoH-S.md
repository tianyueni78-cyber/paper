# **EoH-S: Evolution of Heuristic Set using LLMs for Automated Heuristic Design** 

## **Fei Liu**<sup>1</sup> **, Yilu Liu**<sup>1</sup> **, Qingfu Zhang**<sup>1</sup> **, Xialiang Tong**<sup>2</sup> **, Mingxuan Yuan**<sup>2</sup> 

1Department of Computer Science, City University of Hong Kong 

2Huawei Noah’s Ark Lab 

fliu36-c@my.cityu.edu.hk, qingfu.zhang@cityu.edu.hk 

#### **Abstract** 

Automated Heuristic Design (AHD) using Large Language Models (LLMs) has achieved notable success in recent years. Despite the effectiveness of existing approaches, they only design a single heuristic to serve all problem instances, often inducing poor generalization across different distributions or settings. To address this issue, we propose Automated Heuristic Set Design (AHSD), a new formulation for LLMdriven AHD. The aim of AHSD is to automatically generate a small-sized complementary heuristic set to serve diverse problem instances, such that each problem instance could be optimized by at least one heuristic in this set. We show that the objective function of AHSD is monotone and supermodular. Then, we propose <u>Evolution</u> of <u>Heuristic Set</u> (EoH-S) to apply the AHSD formulation for LLM-driven AHD. With two novel mechanisms of complementary population management and complementary-aware memetic search, EoHS could effectively generate a set of high-quality and complementary heuristics. Comprehensive experimental results on three AHD tasks with diverse instances spanning various sizes and distributions demonstrate that EoH-S consistently outperforms existing state-of-the-art AHD methods and achieves up to 60% performance improvements. 

## **Introduction** 

Automated Heuristic Design (AHD) using Large Language Models (LLMs) has been a success in recent years (Liu et al. 2024e). With the code generation and language comprehension capability of LLMs, the automation and flexibility of algorithm design have been significantly enhanced. Until now, LLM-driven AHD has found successful applications across diverse domains, including optimization (Liu et al. 2024c; Ye et al. 2024; van Stein and B¨ack 2024; Yao et al. 2024; Ye et al. 2025; Dat, Doan, and Binh 2025; Li et al. 2025), mathematics (Romera-Paredes et al. 2024; Novikov et al. 2025), and machine learning (Mo et al. 2025). 

A prevalent paradigm in LLM-driven AHD is to integrate LLMs as heuristic designers within certain iterative search frameworks (Zhang et al. 2024), including evolutionary search (Liu et al. 2024c; Ye et al. 2024; van Stein and B¨ack 2024), neighborhood search (Xie et al. 2025), and Monte Carlo tree search (MCTS) (Zheng et al. 2025). Notable examples include EoH (Liu et al. 2024c), which evolves both thoughts and codes for effective automated 

heuristic design. FunSearch (Romera-Paredes et al. 2024) utilizes a multi-island evolutionary framework with a single prompt strategy for guiding LLMs in function search. Moreover, ReEvo (Ye et al. 2024) integrates short- and long-term reflection strategies to enhance the heuristic design process. 

Despite these advancements, existing methods mainly focus on identifying a single heuristic with the best average performance across a set of training instances. This approach may suffer from generalization limitations due to the following two reasons: 1) finding a single heuristic with the best performance across all diverse instances is inherently difficult (Sim, Renau, and Hart 2025), and 2) even when a heuristic excels on most training instances, it often fails to generalize to unseen test instances with different distributions or scales (Shi et al. 2025). 

A common approach to tackle the generalization limitations of heuristic design is to use an algorithm portfolio (Gomes and Selman 2001; Tang et al. 2021) (i.e., a combination of different algorithms). It is natural for us to leverage this approach to deal with the challenges faced by LLMdriven AHD: using different heuristics rather than a single heuristic. However, given the typically enormous number of problem instances, it is impractical, if not impossible, to find one heuristic for each instance. With these concerns, this paper makes the following contributions: 

- We introduce Automated Heuristic Set Design (AHSD), a new formulation for LLM-driven AHD. AHSD aims to automatically generate a small-sized complementary heuristic set to serve diverse problem instances, such that each problem instance could be optimized by at least one heuristic in this set. We show that the objective function of AHSD is monotone and supermodular. 

- We propose Evolution of Heuristic Set (EoH-S) to apply the AHSD formulation for LLM-driven AHD. EoH incorporates two key components of complementary population management and diversity-aware memetic search to effectively search a set of high-quality and complementary heuristics. 

- We conduct extensive experiments on three AHD tasks with instances of different distributions and sizes, as well as on many benchmark sets. Results show that EoH-S excels in all scenarios and achieves up to 60% performance improvements over state-of-the-art AHD methods. 

## **Automated Heuristic Set Design (AHSD)** 

### **Problem Formulation** 

Suppose we are given a target heuristic design task _T_ (e.g., Traveling Salesman Problem (TSP)) with _m_ diverse problem instances _I_ = _{i_ 1, _. . ._ , _im}_ , the aim of AHSD is to automatically generate a heuristic set _H_ = _{h_ 1, _. . ._ , _hk} ⊆ D_ , where 1 _< k ≪ m_ and _D_ is the search space, such that each problem instance could be optimized by at least one heuristic in this set, which could be mathematically expressed as 



where _fH_<sup>_∗_</sup> , _i_<sup>=min</sup><sup>_h∈H fi_(</sup><sup>_h_), and</sup><sup>_fi_(</sup><sup>_h_) denotes the perfor-</sup> mance score of heuristic _h_ on instance _i_ (lower is better). Since (1) evaluates _H_ from multiple criteria, it is difficult to directly optimize it. To address this issue, we use linear scalarization (Triantaphyllou 2000; Zhang and Yang 2021) to transform (1) into the following optimization objective: 



For clarity, we call _F_ ( _H_ ) as **Complementary Performance Index (CPI)** . Taking CPI as the objective function, the AHSD problem could be formally stated as below. 

_AHSD Problem_ : Given a target heuristic design task _T_ with _m_ task instances _I_ = _{i_ 1, _. . ._ , _im}_ , the aim of AHSD is to automatically generate a heuristic set _H_ = _{h_ 1, _. . ._ , _hk} ⊆ D_ with 1 _< k ≪ m_ such that _F_ ( _H_ ) is minimized. 

When _k_ = 1, the AHSD problem is equal to finding a single optimal heuristic with the best average performance across all instances, which is aligned with the objective of most LLM-driven AHD methods. When _k_ = _m_ , the AHSD problem is equal to finding the best heuristic for each instance independently. Thus, we consider the non-trivial case of 1 _< k ≪ m_ . Next, we demonstrate some theoretical properties of _F_ ( _H_ ). 

### **Theoretical Analysis** 

**Theorem 1** (Optimization Complexity) **.** _The optimization of F_ ( _H_ ) _is NP-hard._ 

_Proof._ We consider an instance of _F_ ( _H_ ) by setting _fi_ ( _h_ ) as 



where _h_<sup>_∗_</sup> _i_<sup>_∈D_istheoptimalheuristicforinstance</sup><sup>_i_and</sup> dis( _h_<sup>_∗_</sup> _i_<sup>,</sup><sup>_h_)denotesacertaindistancebetween</sup><sup>_h∗_</sup> _i_<sup>and</sup><sup>_h_.</sup> Thus, the objective function of this instance is 



We can find that the aim of this instance is equal to finding _k_ centers _{h_ 1, _. . ._ , _hk}_ for _m_ data points _{h_ 1<sup>_∗_,</sup><sup>_. . ._,</sup><sup>_h∗_</sup> _m_<sup>_}_, such</sup> that each data point can be assigned to the optimal center, which is consistent with the aim of the Discrete Clustering 

Problem (DCP) (Drineas et al. 2004). Since DCP is NP-hard when _k >_ 1 (Drineas et al. 2004), the optimization of _F_ ( _H_ ) is also NP-hard, which concludes the proof of Theorem 1. 

**Theorem 2** (Monotonicity and Supermodularity) **.** _For any two heuristic sets U ⊆ V ⊆ D with_ 1 _≤|U | ≤|V |, F_ ( _U_ ) _≥F_ ( _V_ ) _holds. Besides, for any heuristic h_<sup>_′_</sup> _∈ D\V , F_ ( _U_ ) _−F_ ( _U ∪{h_<sup>_′_</sup> _}_ ) _≥F_ ( _V_ ) _−F_ ( _V ∪{h_<sup>_′_</sup> _}_ ) _holds._ 

_Proof._ We first demonstrate that _fU_<sup>_∗_</sup> , _i_<sup>_≥f_</sup> _V_<sup>_∗_</sup> , _i_<sup>holdsforall</sup> instances _i ∈{i_ 1, _. . ._ , _im}_ . For simplicity, we use _j_<sup>_∗_</sup> to denote the index of the best heuristic for _i_ within _V_ , i.e., _j_<sup>_∗_</sup> = _argmin_ 1 _≤j≤|V |fi_ ( _hj_ ). Therefore, we only need to discuss the following two cases: 

1. 1 _≤ j_<sup>_∗_</sup> _≤|U |_ . This case means that the best heuristic for _i_ is in _U_ . As _U ⊆ V_ , we can derive _fU_<sup>_∗_</sup> , _i_<sup>=</sup><sup>_f_</sup> _V_<sup>_∗_</sup> , _i_<sup>.</sup> 

2. _|U | < j_<sup>_∗_</sup> _≤|V |_ . This case means that the best heuristic for _i_ is in _V \U_ , showing that _fU_<sup>_∗_</sup> , _i_<sup>_≥f_</sup> _V_<sup>_∗_</sup> , _i_<sup>.</sup> 

These two cases indicate _fU_<sup>_∗_</sup> , _i_<sup>_≥f_</sup> _V_<sup>_∗_</sup> , _i_<sup>. As</sup><sup>_F_(</sup><sup>_H_) is a convex</sup> combination of _fH_<sup>_∗_</sup> , _i_<sup>, we have</sup><sup>_F_(</sup><sup>_U_)</sup><sup>_≥F_(</sup><sup>_V_), showing that</sup> _F_ ( _H_ ) is monotone. 

Let _U_<sup>_′_</sup> = _U ∪{h_<sup>_′_</sup> _}_ . We then show that _fH_<sup>_∗_</sup> , _i_<sup>is supermodu-</sup> lar, i.e., _fU_<sup>_∗_</sup> , _i_<sup>_−f_</sup> _U_<sup>_∗′_</sup> , _i_<sup>_≥f_</sup> _V_<sup>_∗_</sup> , _i_<sup>_−f_</sup> _V_<sup>_∗′_</sup> , _i_<sup>. For simplicity, we use</sup><sup>_j∗_</sup> to denote the index of the best heuristic for _i_ within _V_<sup>_′_</sup> , i.e., _j_<sup>_∗_</sup> = _argmin_ 1 _≤j≤|V |_ +1 _fi_ ( _hj_ ). Therefore, we only need to discuss the following three cases: 

1. 1 _≤ j_<sup>_∗_</sup> _≤|U |_ . This case means that the best heuristic for _i_ is in _U_ . Thus, we can derive _fU_<sup>_∗_</sup> , _i_<sup>=</sup><sup>_f_</sup> _U_<sup>_∗′_</sup> , _i_<sup>=</sup><sup>_f_</sup> _V_<sup>_∗_</sup> , _i_<sup>=</sup> _fV_<sup>_∗′_</sup> , _i_<sup>, showing that</sup><sup>_f_</sup> _U_<sup>_∗_</sup> , _i_<sup>_−f_</sup> _U_<sup>_∗′_</sup> , _i_<sup>_≥f_</sup> _V_<sup>_∗_</sup> , _i_<sup>_−f_</sup> _V_<sup>_∗′_</sup> , _i_<sup>.</sup> 

2. _|U | < j_<sup>_∗_</sup> _≤|V |_ . This case means that the best heuristic for _i_ is in _V \U_ , showing that _fV_<sup>_∗_</sup> , _i_<sup>=</sup><sup>_f_</sup> _V_<sup>_∗′_</sup> , _i_<sup>. Since</sup><sup>_f_</sup> _U_<sup>_∗_</sup> , _i_<sup>_≥_</sup> _fU_<sup>_∗′_</sup> , _i_<sup>, we have</sup><sup>_f_</sup> _U_<sup>_∗_</sup> , _i_<sup>_−f_</sup> _U_<sup>_∗′_</sup> , _i_<sup>_≥f_</sup> _V_<sup>_∗_</sup> , _i_<sup>_−f_</sup> _V_<sup>_∗′_</sup> , _i_<sup>.</sup> 

3. _j_<sup>_∗_</sup> = _|V |_ + 1. This case means that the best heuristic for _i_ is **_x_**<sup>_′_</sup> , showing that _fU_<sup>_∗′_</sup> , _i_<sup>=</sup><sup>_f_</sup> _V_<sup>_∗′_</sup> , _i_<sup>. Since</sup><sup>_f_</sup> _U_<sup>_∗_</sup> , _i_<sup>_≥f_</sup> _V_<sup>_∗_</sup> , _i_<sup>, we</sup> have _fU_<sup>_∗_</sup> , _i_<sup>_−f_</sup> _U_<sup>_∗′_</sup> , _i_<sup>_≥f_</sup> _V_<sup>_∗_</sup> , _i_<sup>_−f_</sup> _V_<sup>_∗′_</sup> , _i_<sup>.</sup> 

These three cases confirm the supermodularity of _fH_<sup>_∗_</sup> , _i_<sup>. Sim-</sup> ilarly, as _F_ ( _H_ ) is a convex combination of _fH_<sup>_∗_</sup> , _i_<sup>,</sup><sup>_F_(</sup><sup>_U_)</sup><sup>_−_</sup> _F_ ( _U ∪{h_<sup>_′_</sup> _}_ ) _≥F_ ( _V_ ) _−F_ ( _V ∪{h_<sup>_′_</sup> _}_ ) holds, showing that _F_ ( _H_ ) is supermodular. Thus, Theorem 2 holds. 

Given the optimization complexity of _F_ ( _H_ ), evolutionary search is still a useful optimization framework. As evolution often operates on a heuristic population, and _F_ ( _H_ ) is monotone and supermodular, prior work (Nemhauser, Wolsey, and Fisher 1978) has shown that the Greedy Algorithm (GA) could always identify a small-sized complementary heuristic set from such a population while providing the following theoretical performance guarantee. 

**Theorem 3** (Theoretical Performance Guarantee of GA) **.** _Let P_ = _{h_ 1, _. . ._ , _hn} ⊂ D be a heuristic population with n > k and H_<sup>_o_</sup> _be the optimal heuristic set within P for solving F_ ( _H_ ) _. Then, the output of GA, referred to as H_<sup>_ga_</sup> _, satisfies F_ ( _H_ 1) _−F_ ( _H_<sup>_ga_</sup> ) _≥_ (1 _−k/_ ( _ek−e_ ))( _F_ ( _H_ 1) _−F_ ( _H_<sup>_o_</sup> )) _, where H_ 1 = _{argminh∈P F_ ( _{h}_ ) _} and e is the natural constant._ 



<!-- Start of picture text -->
Output:<br>Opt. heuristic set<br>… … (best complementary performance)<br>Generation<br>Complementary Population Management<br>Diversity-aware<br>Management memetic search<br>…<br>Evaluation<br>Performance<br>… Evaluation<br>Heuristic  𝒉<br>+<br>Output: Opt. heuristic  (best avg. performance) … … … Instance  𝒊<br>a) Existing AHD methods b) EoH-S for AHSD<br><!-- End of picture text -->

Figure 1: **a) Existing LLM-driven Automated Heuristic Design (AHD) methods** employ an iterative search framework to identify a single optimal heuristic, optimizing average performance. **b) Automated Heuristic Set Design (AHSD)** seeks to generate a set of complementary heuristics, enhancing performance across diverse problem instances. EoH-S adopts an evolutionary framework with diversity-aware memetic search and complementary population management for effective AHSD. 

## **Evolution of Heuristic Set (EoH-S)** 

### **Framework Overview** 

We propose an evolutionary search framework, named Evolution of Heuristic Set (EoH-S), aimed at automatically designing a set of complementary heuristics. As illustrated in Figure 1, the existing LLM-driven AHD methods aim at generating a single optimal heuristic to optimize the average performance on the target task (Liu et al. 2024c; RomeraParedes et al. 2024; Ye et al. 2024; Zheng et al. 2025). In contrast, EoH-S is proposed for AHSD to design a set of heuristics that complement each other on diverse instances. 

Like prior work (Liu et al. 2024c; Yao et al. 2025), each heuristic in EoH-S is represented by both a high-level thought description and an executable code implementation (in this paper, Python functions). However, unlike existing approaches that use average performance as fitness, EoH-S maintains an instance-wise performance vector (i.e., scores across _m_ instances) for each heuristic, enabling complementary search and management. 

The EoH-S framework operates as follows: 

1. **Initialization:** EoH-S begins with an initial population, _P_ 0, consisting of _n_ heuristics _{h_ 1, _. . ._ , _hn}_ . These heuristics are generated by repeatedly prompting LLMs using an initialization prompt _hi_ = Init( _LLM_ , _pi_ ). The initialization prompt consists of a task description and a function template. The LLM is instructed first to generate a heuristic thought and then implement its code based on the template. Due to space limitations, all prompt details used in EoH-S are in Appendix. 

2. **Evolutionary Cycle:** Start from the initial population, EoH-S iteratively performs the following steps: 

- (a) **Memetic Search:** Two strategies are adopted to create _n_ new heuristics _{ho_ 1, _. . ._ , _hon}_ based on existing ones in the current population: 

- i. Complementary-aware search (CS): _ho_ = CS( _LLM_ , _pcs_ , _hp_ ), where _pcs_ is the prompt used for complementary-aware search and _hp_ are the parent heuristics used in the prompt. In this paper, we use two parent heuristics, which are selected according to their complementary behaviour on diverse instances. CS is used to explore diverse heuristics to enhance the complementary performance of the entire heuristic set. 

- ii. Local search (LS): _ho_ = LS( _LLM_ , _pls_ , _hp_ ), where _pls_ is the local search prompt and _hp_ is one selected heuristic. Local search strategy aims at revising one heuristic to search for a new heuristic close to the parent heuristic. 

- (b) **Population Management:** The _n_ new heuristics and _n_ heuristics from the current population are combined into a candidate pool of size 2 _n_ : _P_<sup>ˆ</sup> _i_ +1 = _Pi ∪ {ho_ 1, _. . ._ , _hon}_ . Then, a Complementary Population Management (CPM) strategy is used to select _n_ heuristics from these 2 _n_ condidates to form the next population: _Pi_ +1 = _CPM_ ( _P_<sup>ˆ</sup> _i_ +1) 

3. **Termination:** The process is terminated when a predefined stopping criterion is met, such as reaching the maximum number of evaluated heuristics _Nmax_ . 

### **Memetic Search** 

EoH-S adopts a complementary-aware memetic search to effectively explore new heuristics. It integrates two reproduc- 

tion strategies: **Complementary-aware Search (CS)** and **Local Search (LS)** . 

**Complementary-aware Search (CS)** CS encourages exploring complementary heuristics through both 1) selecting two parent heuristics _hp_ and 2) the prompt _pcs_ . Specifically, two parent heuristics _hp_ are selected based on their instancewise performance across _m_ instances. The complementary nature between heuristics is measured using Manhattan distance d _ha_ , _hb_ between two heuristics _ha_ and _hb_ . The Manhattan distance measures the sum of the absolute differences between corresponding elements, quantifying the total performance difference between two heuristics across the same set of problem instances. It is computed as: 



where _F_ ( _ha_ ) = _{fi_ 1( _ha_ ), _. . ._ , _fim_ ( _ha_ ) _}_ and _F_ ( _hb_ ) = _{fi_ 1( _hb_ ), _. . ._ , _fim_ ( _hb_ ) _}_ denote the performance scores of heuristics _a_ and _b_ on _m_ instances. We select the pair of heuristics in the current population _P_ with the largest distance: 



In the prompt _pcs_ , we inform LLM that we have this complementary pair of heuristics and instruct LLM to create new heuristics distinct from existing designs. 

**Local Search (LS)** In contrast to CS, LS focuses on refinement of existing heuristics instead of exploring new ones. The one parent heuristic _hp_ is selected according to a weighted random selection where better-ranked functions have higher probabilities (Liu et al. 2024c). The rank is sorted using the average performance on _m_ instances. This strategy promotes exploitation by producing heuristics that preserve the parent’s strengths while improving performance through fine-tuned adjustments. 

We generate _n_ new heuristics in memetic search using the two reproduction strategies with equal probability. Following reproduction, candidate heuristics are evaluated on a set of diverse instances. 

### **Complementary Population Management** 

EoH-S employs a **Complementary Population Management (CPM)** mechanism to select the _n_ heuristics from 2 _n_ candidate pool to form the next population. Unlike conventional LLM-driven AHD methods that select heuristics based solely on average performance, CPM leverages instance-wise performance vectors to maintain population complementarity across problem instances. It greedily select _n_ heuristics from 2 _n_ candidate heuristics to minimize the _F_ ( _H_ ) on _m_ instances, which ensures the performance guarantee established in **Theorem 3** . 

Specifically, the CPM is performed as follows: Firstly, select the heuristic with average performance on _m_ instances from 2 _n_ heuristics to be the first one. Then, iteratively select the next heuristic to maximize the delta CPI until _n_ heuristics have been selected. Given a current heuristic set 

_Hk_ = _{h_ 1, _. . ._ , _hk}_ and a candidate heuristic _hi_ , the delta CPI is defined as: 



where: 

- _fij_ ( _hi_ ) is the performance score of _hi_ on instance _ij_ ( _lower is better_ ). 

- _fH_<sup>_∗_</sup> _k_ , _ij_<sup>=min</sup><sup>_h∈H_</sup> _k_<sup>_fi_</sup> _j_<sup>(</sup><sup>_h_) is the best score in</sup><sup>_Hk_for in-</sup> stance _ij_ . 

The CPM operates as follows: 

1. **Initialize** : Select the heuristic with best average performance from 2 _n_ candidates as _h_ 1. 

2. **Iterative Selection** : 

- = 

- (a) For current set _Hk {h_ 1, _. . ._ , _hk}_ , compute ∆CPI( _hi | Hk_ ) for each remaining heuristic _hi_ in 2 _n − k_ candidates. 

- (b) Select _hi∗_ = _argmaxi∈_ 2 _n−k_ ∆CPI( _hi | Hk_ ) and update _Hk_ +1 = _Hk ∪{hi∗ }_ . 

- (c) Update reference scores: _fH_<sup>_∗_</sup> _k_ +1, _ij_ = min( _fH_<sup>_∗_</sup> _k_ , _ij_<sup>,</sup><sup>_fi_</sup> _j_<sup>(</sup><sup>_hi∗_)).</sup> 

3. **Terminate** when _|Hk|_ = _n_ . 

## **Experimental Studies** 

### **Tasks and Instances** 

We investigate the following three tasks, with detailed descriptions provided in the Appendix: 

- Online Bin Packing (OBP) involves packing items into the minimum number of fixed-capacity bins as items arrive sequentially. The heuristic is used to select the assigned bin for each incoming item. The performance is measured as the relative gap to the lower bound of the optimal number of bins computed as in (Martello and Toth 1990). For heuristic evaluation during automated design (training), _I_ consists of 128 Weibull instances (RomeraParedes et al. 2024) with a bin capacity of 100 and the number of items ranging from 200 to 2000 (2k). For testing, we use six sets with larger capacities 200,500 and more items 1k, 5k, 10k, each set consists of 5 instances following existing works (Romera-Paredes et al. 2024; Liu et al. 2024c) 

- Traveling Salesman Problem (TSP) requires finding the shortest route visiting all cities exactly once before returning to the start. We design a step-by-step construction heuristic. The heuristic is used to iteratively select the next city to visit. The average relative gap from the baseline solution generated by LKH (Helsgaun 2017) is used for performance measurement. For training, _I_ consists of 128 instances with the number of cities ranging from 10 to 200, sampled in [0, 1] using a Gaussian distribution in clusters following Bi et al. (2022). For testing, we use instances in uniform distribution with the number of cities ranging from 50 to 500. 

|Methods|Tra<br>n200-500|ining (c100<br>n500-1k|)<br>n1k-2k|n1k<br>~~c~~200|n1k<br>~~c~~500|Testing<br>n5k<br>~~c~~200|(c200-500)<br>n5k<br>~~c~~500|n10k<br>~~c~~200|n10k<br>~~c~~500|
|---|---|---|---|---|---|---|---|---|---|
|First Fit|0.0652|0.0318|0.0387|0.0240|**0.0124**|0.0173|0.0075|0.0163|0.0055|
|Best Fit|0.0627|0.0310|0.0372|0.0220|**0.0124**|0.0161|0.0070|0.0154|0.0050|
|Random*|0.3638|0.2988|0.1489|0.1939|1.3508|0.0376|0.2816|0.0189|0.1402|
|1+1 EPS*|0.2482|0.2180|0.1246|0.0569|0.2390|0.0101|0.0439|0.0055|0.0224|
|FunSearch*|0.2510|0.2000|0.1326|0.0827|0.6169|0.0193|0.2260|0.0120|0.1211|
|EoH*|0.1216|0.1169|0.0750|0.0190|**0.0124**|0.0044|0.0050|0.0041|0.0042|
|MEoH*|0.0991|0.0749|0.0547|0.1037|0.0149|0.0417|0.0035|0.0326|0.0015|
|CALM*|0.0805|0.0300|0.0470|0.0120|**0.0124**|0.0048|0.0030|0.0034|0.0025|
|ReEvo*|0.0877|0.0344|0.0556|0.0120|**0.0124**|0.0074|0.0040|0.0068|0.0025|
|MCTS-AHD*|0.0974|0.0360|0.0596|0.0150|**0.0124**|0.0046|0.0040|0.0034|0.0022|
|FunSearch|0.0623|0.0298|0.0367|0.0213|**0.0124**|0.0159|0.0070|0.0152|0.0051|
|FunSearch Top10|0.0608|0.0289|0.0361|0.0200|**0.0124**|0.0153|0.0065|0.0123|0.0038|
|EoH|0.0619|0.0307|0.0371|0.0240|0.0133|0.0182|0.0075|0.0170|0.0059|
|EoH Top10|0.0618|0.0299|0.0368|0.0216|**0.0124**|0.0158|0.0065|0.0152|0.0051|
|<br>ReEvo|0.0604|0.0298|0.0362|0.0217|0.0133|0.0162|0.0068|0.0155|0.0053|
|ReEvo Top10|0.0580|0.0285|0.0349|0.0203|**0.0124**|0.0125|0.0063|0.0108|0.0049|
|EoH-S|**0.0515**|**0.0230**|**0.0314**|**0.0113**|**0.0124**|**0.0033**|**0.0025**|**0.0014**|**0.0010**|



Table 1: Evaluation of heuristics designed by different methods on OBP instances. We use 128 Weibull instances with sizes ranging from 200 to 2k for training and six different sets (n1k ~~c~~ 200, n1k ~~c~~ 500, n5k ~~c~~ 200, n5k ~~c~~ 500, n10k ~~c~~ 200, n10k ~~c~~ 500) for testing, where n and c represent the number of items and the bin capacity, respectively. Each method is run three times and we report the average performance. We directly use the best-performing heuristics from their original papers for the methods with _∗_ . The best values are **in bold** with a grey background and the second-best values are in a light-grey background. 

- Capacitated Vehicle Routing Problem (CVRP) extends TSP by incorporating vehicle capacity constraints and customer demands. The goal is minimizing total travel distance while ensuring all customer demands are met without exceeding vehicle capacities. We design a stepby-step construction heuristic. The heuristic is to select the next node. The average relative gap from the baseline solution generated by LKH (Helsgaun 2017) is used for performance measurement. For training, _I_ consists of 256 instances with the number of nodes from 20 to 200 and the capacities from 10 to 150. For testing, we use instances with node sizes ranging from 50 to 500. For both training and testing, the nodes are sampled in [0, 1] using a uniform distribution. We do not consider Gaussion distribution here because the different capacities and sizes have already introduced diversities. 

### **Compared Methods and Settings** 

We compare state-of-the-art LLM-driven AHD methods, including **Random** (i.e., repeated prompt LLMs to generate heuristic without an iterative search framework (Zhang et al. 2024)), **EoH** (Liu et al. 2023, 2024c), **FunSearch** (RomeraParedes et al. 2024), **ReEvo** (Ye et al. 2024), **1+1 EPS** (Zhang et al. 2024), **MEoH** (Yao et al. 2025) **MCTSAHD** (Zheng et al. 2025), and **CALM** (Huang et al. 2025). 

We evaluate these methods under two settings: **1) Direct comparison** : We directly compare the best-performing heuristics reported in the original papers for the online bin packing problem. These heuristics are all designed for the Weibull instances with slightly different distributions. **2)** 

**Controlled comparison** : For some representative methods (EoH, FunSearch, and ReEvo), we conduct training using identical instances to EoH-S, enabling a fair performance comparison. Three independent runs are performed for these methods on all three tasks. 

All experiments are conducted on LLM4AD platform (Liu et al. 2024f) using DEEPSEEK-V3 (Liu et al. 2024a) API with default parameter settings. We set the maximum number of heuristic evaluations to _N_ max = 2,000 for all tasks and fix the population size at _n_ = 10 for EoH-S, EoH, and ReEvo to maintain consistency (FunSearch uses a dynamic population size). The experiments run on one Intel i7-9700 CPU, and the automated heuristic design process completes in under two hours for all methods across different tasks. It is worth noting that although EoH-S explicitly design a set of complementary heuristics, it does not introduce additional running time because we use the same maximum number of evaluations for all methods. 

### **Results on Training & Testing Instances** 

The results on training and testing instances of diverse distributions and sizes are summarized in Table 1 (OBP) and Table 2 (TSP and CVRP), where the best values are in bold with a grey background and the second-best values are in a light-grey background. The values are the gap to baseline results (lower bound for OBP (Romera-Paredes et al. 2024) and LKH for TSP and CVRP (Helsgaun 2017)). We report the average results over three independent runs. The methods with _∗_ denote the best one heuristic from their original paper. For EoH-S, we use 10 heuristics in the final pop- 

|Methods|Training|50|Tes<br>100|ting<br>200|500|
|---|---|---|---|---|---|
|FunSearch|0.156|0.144|0.149|0.169|0.185|
|FunSearch Top10|0.124|0.091|0.105|0.124|0.157|
|EoH|0.152|0.142|0.154|0.168|0.194|
|EoH Top10|0.127|0.079|0.123|0.134|0.175|
|ReEvo|0.155|0.167|0.183|0.223|0.221|
|ReEvo Top10|0.117|0.092|0.123|0.157|0.170|
|EoH-S|**0.097**|**0.040**|**0.065**|**0.090**|**0.111**|
|Methods|Training|50|Tes<br>100|ting<br>200|500|
|FunSearch|0.294|0.315|0.365|0.296|0.241|
|FunSearch Top10|0.245|0.267|0.309|0.247|0.214|
|EoH|0.276|0.274|0.299|0.261|0.221|
|EoH Top10|0.230|0.172|0.232|0.218|0.198|
|ReEvo|0.265|0.274|0.296|0.256|0.203|
|ReEvo Top10|0.240|0.214|0.249|0.173|0.178|
|EoH-S|**0.173**|**0.135**|**0.188**|**0.180**|**0.169**|



Table 2: Evaluation of heuristics designed by different methods on TSP (upper) and CVRP (lower). We use 128 TSP instances with sizes ranging from 10 to 200 and 256 CVRP instances with sizes ranging from 20 to 200 for training, and four different sets with sizes ranging from 50 to 500 for testing. Each method is run three times, and we report the average performance. The best values are **in bold** with a grey background and the second-best values are in a light-grey background. 

ulation. For fair comparison, we also compare the top 10 heuristics from FunSearch, EoH, and ReEvo (denoted as FunSearch Top10, EoH Top10, and ReEvo Top10, respectively). 

As indicated in Table 1, EoH-S consistently outperforms all baseline methods on both training instances (c100 with varying item counts) and testing instances (c200-500 with different problem sizes), achieving the lowest gap values in 8 out of 9 configurations and matching the best performance in the remaining one. In contrast, existing LLM-driven AHD methods from the literature struggle to generalize across different distributions, with some even underperforming first-fit and best-fit heuristics, which is also observed by Xu, Hoos, and Leyton-Brown (2010). 

Table 2 shows that EoH-S performs consistently well on TSP and CVRP. On TSP, EoH-S significantly reduces the optimality gap by 50-60% compared to the second-best method across all test instances of varying sizes (50-500 nodes). For CVRP, EoH-S again achieves the lowest optimality gaps on both training and testing instances, with particularly significant improvements on smaller problem instances. 

### **Results on Benchmark Instances** 

Tabel 3 presents a comprehensive evaluation of our proposed EoH-S method against existing approaches (EoH and ReEvo) across multiple benchmark datasets, including BPPLib (Delorme, Iori, and Martello 2018), TSPLib (Reinelt 1991), and CVRPLib (Uchoa et al. 2017). Our proposed 

|Benchmarks|E|oH|Re|Evo|EoH-S|
|---|---|---|---|---|---|
||Top 1|Top 10|Top 1|Top 10||
|BPPLib Sch<br>~~1~~|0.153|0.153|0.153|0.153|**0.152**|
|BPPLib Sch<br>~~2~~|0.142|0.142|0.142|0.142|**0.141**|
|BPPLib IRUP|0.077|0.075|0.079|0.074|**0.072**|
|BPPLib NonIRUP|0.077|0.076|0.080|0.075|**0.073**|
|BPPLib Scholl<br>H|0.138|0.138|0.138|0.138|**0.095**|
|TSPLib|0.184|0.173|0.220|0.165|**0.093**|
|CVRPLib A|0.326|0.277|0.329|0.261|**0.231**|
|CVRPLib B|0.374|0.310|0.352|0.250|**0.183**|
|CVRPLib E|0.334|0.268|0.305|0.257|**0.242**|
|CVRPLib F|0.539|0.493|0.687|0.547|**0.427**|
|CVRPLib M|0.461|0.377|0.442|0.372|**0.299**|
|CVRPLib P|0.273|0.206|0.270|0.188|**0.169**|
|CVRPLib X|0.270|0.237|0.270|0.224|**0.196**|



Table 3: Results on OPPLib, TSPLib, and CVRPLib Benchmarks. The best values are **in bold** with a grey background and the second-best values are in a light-grey background. 

EoH-S method consistently outperforms both baseline methods across all benchmark instances. On the BPPLib datasets, EoH-S achieves superior results, with particularly notable improvement on the Scholl ~~H~~ instance (0.095 compared to 0.138 for both baselines). 

For the TSPLib benchmark, EoH-S demonstrates substantial performance gains with a score of 0.093, representing a 43.6% improvement over the second-best result (0.165 from ReEvo Top 10). On the CVRPLib benchmarks, EoHS achieves improvements ranging from 5.8% (on set E) to 26.8% (on set B) compared to the second-best results. These results clearly demonstrate the effectiveness and robustness of our proposed approach in designing complementary heuristics. 

### **Complementary Performance** 

We evaluate the complementary performance of heuristic sets generated by different methods. Figure 2 compares the performance (averaged over three independent runs) of heuristic sets as the number of heuristics increases (on a logarithmic scale from 1 to 100). The CPI (Complementary Performance Index) measures the gap to the lower bound. 

For EoH-S, we use the final population of heuristics, capped at 10. For EoH, FunSearch, and ReEvo, we select the top 100 heuristics from all candidates evaluated during the search process. When the set size is 1, we report the performance of the single best heuristic (in terms of average performance). For a set size of 10, we consider the full heuristic set for EoH-S and the top 10 heuristics for other methods. The CPI drop observed when expanding from a single heuristic to a larger set reflects the degree of complementarity, i.e., how effectively additional heuristics contribute to solving diverse problem instances. 

Our results demonstrate three key findings: First, the heuristic set designed by EoH-S consistently outperforms those designed by the compared methods. Second, even when utilizing 100 heuristics, the competing methods struggle to match the performance achieved by just 10 heuristics 



<!-- Start of picture text -->
FunSearch<br>0.15 EoH<br>ReEvo<br>0.14 EoH-S<br>0.13<br>0.12<br>0.11<br>0.10<br>EoH-S range<br>1 2 5 10 20 50 100<br>Number of Heuristics (log scale)<br>0.30<br>FunSearch<br>0.28 EoH<br>ReEvo<br>0.26 EoH-S<br>0.24<br>0.22<br>0.20<br>0.18<br>EoH-S range<br>1 2 5 10 20 50 100<br>Number of Heuristics (log scale)<br>Performance (CPI)<br>Performance (CPI)<br><!-- End of picture text -->

Figure 2: Complementary Performance Index (CPI) comparison across methods with varying numbers of heuristics. For EoH-S, we select heuristics from the final population (maximum 10), while for other methods, we select the best 100 heuristics from the entire search history. 

designed by EoH-S. Third, each heuristic in the EoH-S set makes a meaningful contribution to the overall performance. The significantly steeper performance curve of EoH-S compared to other methods indicates that its heuristics provide greater complementary benefits. 

### **Ablation Studies** 

We conduct ablation studies on OBP to evaluate the contribution of each key component and the impact of population size. The following variants of EoH-S are examined: 

- EoH-S w/o LS: Excludes the Local Search operator (LS). 

- EoH-S w/o CS: Excludes the Complementary-aware Search operator (CS). 

- EoH-S w/o CPM: Disables Complementary Population Management (CPM) and instead uses a population management approach in existing works (retaining the bestperforming heuristics based on average performance). 

|No.|Settings|Gap|
|---|---|---|
|1|First Fit|0.0413|
|2|Best Fit|0.0399|
|3|ReEvo Top 10|0.0371|
|4|EoH-S w/o LS|0.0336|
|5|EoH-S w/o CS|0.0335|
|6|EoH-S w/o CPM|0.0373|
|7|EoH-S n5|0.0333|
|8|EoH-S n15|0.0339|
|9|EoH-S n20|0.0337|
|10|EoH-S|0.0326|



Table 4: Ablation study of key components and settings 

- EoH-S n5–n20: Tests EoH-S with population sizes ranging from 5 to 20. 

The experimental setup matches the main experiments, with 2,000 total samples per run and a population size 10. 

Table 4 presents the average gap to the lower bound across 128 OBP training instances. The first three methods are two hand-designed heuristics and the ReEvo Top 10 (the secondbest one, as indicated in Table 1). The No. 4 to No. 6 are three variants of EoH-S that assess the importance of the search operators and CPM. Results show that all components contribute to performance, with CPM providing the most significant improvements. The remaining variants (No. 7–9) demonstrate that EoH-S consistently outperforms existing methods across population sizes (5–20), with a size of 10 proving optimal for this task. Results demonstrate the contribution of different components and the robustness of EoH-S across different settings. 

## **Conclusion and Future Works** 

In this work, we introduced Automated Heuristic Set Design (AHSD), a novel formulation for LLM-driven AHD that generates a small yet complementary set of heuristics to optimize diverse problem instances effectively. We demonstrated that the AHSD objective function is monotone and supermodular, providing a theoretical foundation for efficient heuristic set optimization. We proposed Evolution of Heuristic Set (EoH-S), which integrates a complementary population management and a memetic search for effectively evolving high-quality and complementary heuristics. Extensive experiments across multiple AHD tasks validated the superiority of EoH-S, achieving up to 60% performance improvements over state-of-the-art AHD methods. Notably, EoH-S demonstrated strong generalization capabilities using a small set of heuristics. 

Our work advances LLM-driven heuristic design by shifting from single-best heuristic design to complementary heuristic set design. Future research directions include exploring heuristic collaboration strategies for further performance gains and additional application studies. 

## **References** 

Bengio, Y.; Lodi, A.; and Prouvost, A. 2021. Machine learning for combinatorial optimization: a methodological tour d’horizon. _European Journal of Operational Research_ , 290(2): 405–421. 

Bezerra, L. C.; L´opez-Ib´anez, M.; and St¨utzle, T. 2015. Automatic component-wise design of multiobjective evolutionary algorithms. _IEEE Transactions on Evolutionary Computation_ , 20(3): 403–417. 

Bi, J.; Ma, Y.; Wang, J.; Cao, Z.; Chen, J.; Sun, Y.; and Chee, Y. M. 2022. Learning generalizable models for vehicle routing problems via knowledge distillation. _Advances in Neural Information Processing Systems_ , 35: 31226–31238. 

Burke, E. K.; Hyde, M. R.; Kendall, G.; Ochoa, G.; Ozcan,<sup>¨</sup> E.; and Woodward, J. R. 2018. A classification of hyperheuristic approaches: revisited. In _Handbook of metaheuristics_ , 453–477. Springer. 

Dat, P. V. T.; Doan, L.; and Binh, H. T. T. 2025. HSEVO: Elevating automatic heuristic design with diversity-driven harmony search and genetic algorithm using llms. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , 26931–26938. 

Delorme, M.; Iori, M.; and Martello, S. 2016. Bin packing and cutting stock problems: Mathematical models and exact algorithms. _European Journal of Operational Research_ , 255(1): 1–20. 

Delorme, M.; Iori, M.; and Martello, S. 2018. BPPLIB: a library for bin packing and cutting stock problems. _Optimization Letters_ , 12(2): 235–250. 

Drineas, P.; Frieze, A.; Kannan, R.; Vempala, S.; and Vinay, V. 2004. Clustering large graphs via the singular value decomposition. _Machine Learning_ , 56: 9–33. 

Fu, Z.-H.; Qiu, K.-B.; and Zha, H. 2021. Generalize a small pre-trained model to arbitrarily large tsp instances. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 35, 7474–7482. 

Gomes, C. P.; and Selman, B. 2001. Algorithm portfolios. _Artificial Intelligence_ , 126(1-2): 43–62. 

Helsgaun, K. 2017. An extension of the Lin-KernighanHelsgaun TSP solver for constrained traveling salesman and vehicle routing problems. _Roskilde: Roskilde University_ , 12: 966–980. 

Huang, Z.; Wu, W.; Wu, K.; Wang, J.; and Lee, W.B. 2025. CALM: Co-evolution of algorithms and language model for automatic heuristic design. _arXiv preprint arXiv:2505.12285_ . 

Jiang, Y.; Wu, Y.; Cao, Z.; and Zhang, J. 2022. Learning to solve routing problems via distributionally robust optimization. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 36, 9786–9794. 

Langdon, W. B.; and Poli, R. 2013. _Foundations of genetic programming_ . Springer Science & Business Media. 

Li, R.; Wang, L.; Sang, H.; Yao, L.; and Pan, L. 2025. LLMassisted automatic memetic algorithm for lot-streaming hybrid job shop scheduling with variable sublots. _IEEE Transactions on Evolutionary Computation_ . 

Liu, A.; Feng, B.; Xue, B.; Wang, B.; Wu, B.; Lu, C.; Zhao, C.; Deng, C.; Zhang, C.; Ruan, C.; et al. 2024a. Deepseekv3 technical report. _arXiv preprint arXiv:2412.19437_ . 

Liu, F.; Lin, X.; Liao, W.; Wang, Z.; Zhang, Q.; Tong, X.; and Yuan, M. 2024b. Prompt Learning for Generalized Vehicle Routing. In _33rd International Joint Conference on Artificial Intelligence (IJCAI 2024)_ , 6976–6984. 

Liu, F.; Tong, X.; Yuan, M.; Lin, X.; Luo, F.; Wang, Z.; Lu, Z.; and Zhang, Q. 2024c. Evolution of heuristics: Towards efficient automatic algorithm design using large language model. In _Proceedings of the International Conference on Machine Learning_ , 32201–32223. 

Liu, F.; Tong, X.; Yuan, M.; Lin, X.; Luo, F.; Wang, Z.; Lu, Z.; and Zhang, Q. 2024d. Evolution of heuristics: towards efficient automatic algorithm design using large language model. In _Proceedings of the International Conference on Machine Learning_ , 32201–32223. 

Liu, F.; Tong, X.; Yuan, M.; and Zhang, Q. 2023. Algorithm evolution using large language model. _arXiv preprint arXiv:2311.15249_ . 

Liu, F.; Yao, Y.; Guo, P.; Yang, Z.; Zhao, Z.; Lin, X.; Tong, X.; Yuan, M.; Lu, Z.; Wang, Z.; et al. 2024e. A systematic survey on large language models for algorithm design. _arXiv preprint arXiv:2410.14716_ . 

Liu, F.; Zhang, R.; Xie, Z.; Sun, R.; Li, K.; Lin, X.; Wang, Z.; Lu, Z.; and Zhang, Q. 2024f. Llm4ad: A platform for algorithm design with large language model. _arXiv preprint arXiv:2412.17287_ . 

Luo, F.; Lin, X.; Liu, F.; Zhang, Q.; and Wang, Z. 2023. Neural combinatorial optimization with heavy decoder: Toward large scale generalization. _Advances in Neural Information Processing Systems_ , 36: 8845–8864. 

Manchanda, S.; Michel, S.; Drakulic, D.; and Andreoli, J.M. 2023. On the Generalization of Neural Combinatorial Optimization Heuristics. In _Machine Learning and Knowledge Discovery in Databases: European Conference, ECML PKDD 2022, Grenoble, France, September 19–23, 2022, Proceedings, Part V_ , 426–442. Springer. 

Martello, S.; and Toth, P. 1990. Lower bounds and reduction procedures for the bin packing problem. _Discrete Applied Mathematics_ , 28(1): 59–70. 

Mo, S.; Wu, K.; Gao, Q.; Teng, X.; and Liu, J. 2025. AutoSGNN: Automatic propagation mechanism discovery for spectral graph neural networks. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , 19493–19502. 

Nemhauser, G. L.; Wolsey, L. A.; and Fisher, M. L. 1978. An analysis of approximations for maximizing submodular set functions - I. _Mathematical Programming_ , 14: 265–294. Novikov, A.; V˜u, N.; Eisenberger, M.; Dupont, E.; Huang, P.-S.; Wagner, A. Z.; Shirobokov, S.; Kozlovskii, B.; Ruiz, F. J.; Mehrabian, A.; et al. 2025. AlphaEvolve: A coding agent for scientific and algorithmic discovery. _arXiv preprint arXiv:2506.13131_ . 

O’Neill, M.; and Ryan, C. 2001. Grammatical evolution. _IEEE Transactions on Evolutionary Computation_ , 5(4): 349–358. 

Pan, X.; Jin, Y.; Ding, Y.; Feng, M.; Zhao, L.; Song, L.; and Bian, J. 2023. H-TSP: Hierarchically Solving the LargeScale Traveling Salesman Problem. In _Proceedings of the AAAI Conference on Artificial Intelligence_ . 

Pillay, N.; and Qu, R. 2018. _Hyper-heuristics: theory and applications_ . Springer. 

Qu, R.; Kendall, G.; and Pillay, N. 2020. The general combinatorial optimization problem: Towards automated algorithm design. _IEEE Computational Intelligence Magazine_ , 15(2): 14–23. 

Reinelt, G. 1991. TSPLIB—A traveling salesman problem library. _ORSA Journal on Computing_ , 3(4): 376–384. 

Romera-Paredes, B.; Barekatain, M.; Novikov, A.; Balog, M.; Kumar, M. P.; Dupont, E.; Ruiz, F. J.; Ellenberg, J. S.; Wang, P.; Fawzi, O.; et al. 2024. Mathematical discoveries from program search with large language models. _Nature_ , 625(7995): 468–475. 

Scholl, A.; Klein, R.; and J¨urgens, C. 1997. Bison: A fast hybrid procedure for exactly solving the one-dimensional bin packing problem. _Computers & Operations Research_ , 24(7): 627–645. 

Shi, Y.; Zhou, J.; Song, W.; Bi, J.; Wu, Y.; and Zhang, J. 2025. Generalizable heuristic generation through large language models with meta-optimization. _arXiv preprint arXiv:2505.20881_ . Sim, K.; Renau, Q.; and Hart, E. 2025. Beyond the hype: Benchmarking llm-evolved heuristics for bin packing. In _Proceedings of the International Conference on the Applications of Evolutionary Computation (Part of EvoStar)_ , 386– 402. Springer. 

St¨utzle, T.; and L´opez-Ib´a˜nez, M. 2018. Automated design of metaheuristic algorithms. In _Handbook of metaheuristics_ , 541–579. Springer. 

Yao, S.; Liu, F.; Lin, X.; Lu, Z.; Wang, Z.; and Zhang, Q. 2025. Multi-objective evolution of heuristic using large language model. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , 27144–27152. 

Yao, Y.; Liu, F.; Cheng, J.; and Zhang, Q. 2024. Evolve cost-aware acquisition functions using large language models. In _Proceedings of the International Conference on Parallel Problem Solving from Nature_ , 374–390. Springer. 

Ye, H.; Wang, J.; Cao, Z.; Berto, F.; Hua, C.; Kim, H.; Park, J.; and Song, G. 2024. ReEvo: Large language models as hyper-heuristics with reflective evolution. _Advances in Neural Information Processing Systems_ , 37: 43571–43608. 

Ye, H.; Xu, H.; Yan, A.; and Cheng, Y. 2025. Large language model-driven large neighborhood search for Largescale MILP problems. In _Proceedings of the International Conference on Machine Learning_ . 

Zhang, R.; Liu, F.; Lin, X.; Wang, Z.; Lu, Z.; and Zhang, Q. 2024. Understanding the importance of evolutionary search in automated heuristic design with large language models. In _International Conference on Parallel Problem Solving from Nature_ , 185–202. Springer. 

Zhang, Y.; and Yang, Q. 2021. A survey on multi-task learning. _IEEE Transactions on Knowledge and Data Engineering_ , 34(12): 5586–5609. 

Zheng, Z.; Xie, Z.; Wang, Z.; and Hooi, B. 2025. Monte Carlo tree search for comprehensive exploration in LLMbased automatic heuristic design. In _Proceedings of the International Conference on Machine Learning_ . 

Zhou, J.; Wu, Y.; Song, W.; Cao, Z.; and Zhang, J. 2023. Towards Omni-generalizable Neural Methods for Vehicle Routing Problems. In _Proceedings of the International Conference on Machine Learning_ . 

Tang, K.; Liu, S.; Yang, P.; and Yao, X. 2021. Few-shots parallel algorithm portfolio construction via co-evolution. _IEEE Transactions on Evolutionary Computation_ , 25(3): 595–607. 

Triantaphyllou, E. 2000. Multi-criteria decision making methods. In _Multi-criteria Decision Making Methods: A Comparative Study_ , 5–21. Springer. 

Uchoa, E.; Pecin, D.; Pessoa, A.; Poggi, M.; Vidal, T.; and Subramanian, A. 2017. New benchmark instances for the capacitated vehicle routing problem. _European Journal of Operational Research_ , 257(3): 845–858. 

van Stein, N.; and B¨ack, T. 2024. Llamea: A large language model evolutionary algorithm for automatically generating metaheuristics. _IEEE Transactions on Evolutionary Computation_ . 

Xie, Z.; Liu, F.; Wang, Z.; and Zhang, Q. 2025. LLM-driven neighborhood search for efficient heuristic design. In _Proceedings of the IEEE Congress on Evolutionary Computation_ , 1–8. IEEE. 

Xu, L.; Hoos, H.; and Leyton-Brown, K. 2010. HYDRA: Automatically configuring algorithms for portfolio-based selection. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , 210–216. 

## **Related Works** 

### **Automated Heuristic Design (AHD)** 

Automated heuristic design, often referred to as hyperheuristics (Burke et al. 2018; St¨utzle and L´opez-Ib´a˜nez 2018), which are designed to automate the selection, combination, generation, or adaptation of simpler heuristics to efficiently solve computational search problems (Pillay and Qu 2018). 

In automated heuristic generation, generation constructive hyperheuristics synthesize new heuristics, often via genetic programming or grammatical evolution (O’Neill and Ryan 2001), producing either instance-specific or reusable heuristics. Generation perturbative methods combine existing perturbative heuristics with acceptance criteria. Recent work extends these classifications through component-based unified solvers, integrating diverse operators and stages to form new algorithms (Bezerra, L´opez-Ib´anez, and St¨utzle 2015; Qu, Kendall, and Pillay 2020), which leverage fundamental components to address a wide range of optimization problems. 

Although methods like genetic programming (Langdon and Poli 2013) and recent unified solvers (Bezerra, L´opez-Ib´anez, and St¨utzle 2015; Qu, Kendall, and Pillay 2020) offer a flexible and explainable approach to algorithm design, they still necessitates tailored hand-crafted components and much domain-specific knowledge. 

### **Neural Combinatorial Optimization** 

In the past decade, neural combinatorial optimization has emerged as a promising paradigm that trains neural networks to learn heuristics for solving complex optimization problems (Bengio, Lodi, and Prouvost 2021). This approach has garnered significant attention due to its effectiveness and computational efficiency in generating high-quality solutions. 

Cross-distribution learning is a key research direction within this field that aim to enhance generalization performance across diverse problem distributions and scales. For instance, Jiang et al. (2022) and Bi et al. (2022) investigated robust optimization techniques across multiple geometric distributions. Complementary work by several researchers (Fu, Qiu, and Zha 2021; Pan et al. 2023; Manchanda et al. 2023; Luo et al. 2023) has explored methods to improve generalization to larger problem instances. Moreover, recent attempts (Zhou et al. 2023; Liu et al. 2024b) have expanded it by simultaneously addressing both problem size and geometric distribution variations. 

Despite these notable advances, neural combinatorial solvers face significant challenges. They typically require substantial expertise in model architecture design and significant computational resources for training. Furthermore, the inherent blackbox nature of these neural approaches limits their interpretability, which presents a considerable barrier to their adoption in real-world applications where solution transparency and explainability are often critical requirements. 

### **LLM-driven AHD** 

Among existing LLM-driven AHD methods, a prominent strategy involves iteratively using LLMs to design and refine algorithms within an evolutionary framework (Zhang et al. 2024). This paradigm has demonstrated promising results across diverse algorithm design tasks, including combinatorial optimization, Bayesian optimization, and black-box optimization (van Stein and B¨ack 2024). Notable examples include EoH (Liu et al. 2024d), which evolves both thoughts and code through five distinct prompt strategies to guide effective algorithm search, significantly enhancing the exploration of the solution space. FunSearch (Romera-Paredes et al. 2024) employs a multi-island evolutionary framework but relies on a single prompt strategy to instruct LLMs in algorithm refinement. Moreover, ReEvo (Ye et al. 2024) incorporates short- and long-term reflection strategies into the evolutionary process to provide additional guidance to LLMs. In addition to evolutionary search, other search frameworks, such as Monte Carlo tree search (MCTS) (Zheng et al. 2025) and neighborhood search (Xie et al. 2025), have also been investigated to enhance the efficiency. 

While these methods have achieved success, they mainly focus on finding a single heuristic that has optimal average performance, which usually suffers from poor generalization performance beyond their training distribution (Sim, Renau, and Hart 2025; Shi et al. 2025). 

## **Heuristic Design Tasks & Setups** 

### **Online Bin Packing (OBP)** 

**Problem Definition** OBP involves packing a sequence of items into a minimum number of bins, each with a fixed capacity _C ∈_ R<sup>+</sup> . Items arrive sequentially and must be assigned to a bin upon arrival, without knowledge of future items. 

- Let _I_ = _{i_ 1, _i_ 2, _. . ._ , _in}_ denote a sequence of _n_ items, where each item _ij_ has a **size** _sj ∈_ (0, _C_ ]. 

- A **bin** is a container with capacity _C_ , and a packing is valid if the sum of item sizes in any bin does not exceed _C_ : 



- The objective is to minimize the total number of bins used: 



In the online setting: 1) Items arrive one-by-one in an unknown order. 2) Each item _ij_ must be assigned to a bin immediately upon arrival. 3) No reallocation or rearrangement of previously packed items is allowed. 

**Designed Heuristic** The design heuristic is used to calculate the priorities of the bins for each incoming item, given the size of the item and the rest capacities of the bins. The heuristic is implemented as a Python function. The performance is measured by the average relative gap to lower bound of the number of used bins. 

#### **Data Generation** 

- **Training Instances:** For training, we sample 128 instances using the Weibull distribution with shape parameters _k ∈ {_ 1, 3, 5 _}_ and scale parameters _λ ∈{_ 5, 10, 20, 40, 80 _}_ . The number of items per instance ranges from 200 to 2000, randomly sampled from this interval. All training instances use a fixed capacity of 100. 

- **Testing Instances:** For testing, we create six sets with larger capacities _{_ 200, 500 _}_ and more items _{_ 1k, 5k, 10k _}_ . Each set contains 5 instances, following the settings established in prior work (Romera-Paredes et al. 2024; Liu et al. 2024c). 

- The task description and template used in the prompts are as follows: 

**OBP Task Description:** Implement a function that returns the priority with which we want to add an item to each bin. 

1 **<mark>import</mark>** <mark>numpy as np</mark> 2 **<mark>def</mark>** <mark>priority(item:</mark> **<mark>float</mark>** <mark>, bins: np.ndarray) -> np.ndarray:</mark> 3 _<mark>"""Returns priority with which we want to add item to each bin.</mark>_ 4 _<mark>Args:</mark>_ 5 _<mark>item: Size of item to be added to the bin.</mark>_ 6 _<mark>bins: Array of capacities for each bin.</mark>_ 7 _<mark>Return:</mark>_ 8 _<mark>Array of same size as bins with priority score of each bin.</mark>_ 9 _<mark>"""</mark>_ 10 **<mark>return</mark>** <mark>item - bins</mark> 

### **Traveling Salesman Problem (TSP)** 

**Problem Definition:** Let _G_ = ( _V_ , _E_ ) be a complete graph where: _V_ = _{v_ 1, _. . ._ , _vn}_ represents _n_ cities with coordinates **x** _i ∈_ [0, 1]<sup>2</sup> and _E_ contains edges with costs _cij_ = _∥_ **x** _i −_ **x** _j∥_ 2 (we consider Euclidean distance). The objective is to find a Hamiltonian cycle _π_ = ( _π_ 1, _. . ._ , _πn_ , _π_ 1) minimizing: 



**Designed Heuristic:** We target a construction heuristic that iteratively builds the tour by selecting the next city. The designed heuristic is the ID of the next city, given the current city, unvisited cities and the distance matrix. Performance is measured by the average relative gap to LKH-3 (Helsgaun 2017): 

#### **Data Generation:** 

- **Training Instances** : 128 instances where cities are arranged in clustered patterns. These distributions generate between 10-200 cities across 32 instances (each configuration 32 instances), with four different clustering configurations that vary in both the number of clusters (3 or 10) and the standard deviation of points within each cluster (0.03 or 0.07). The distribution is implemented by first generating random cluster centers within a bounded region (0.2–0.8), then sampling city locations from normal distributions centered at these points in [0, 1]<sup>2</sup> , with the specified standard deviation controlling how tightly or loosely cities are grouped around their cluster centers (Bi et al. 2022). 

- **Testing Instances:** 80 instances with city counts of 50, 100, 200, 500, and 1000. 16 instances per size where city coordinates are uniformly distributed in [0, 1]<sup>2</sup> . 

The task description and template used are as follows: 

**TSP Task Description:** Given a set of nodes with their coordinates, you need to find the shortest route that visits each node once and returns to the starting node. The task can be solved step-by-step by starting from the current node and iteratively choosing the next node. Help me design a novel algorithm that is different from the algorithms in literature to select the next node in each step. 

1 **<mark>import</mark>** <mark>numpy as np</mark> 2 **<mark>def</mark>** <mark>select_next_node(current_node:</mark> **<mark>int</mark>** <mark>, destination_node:</mark> **<mark>int</mark>** <mark>, unvisited_nodes: np. ndarray, distance_matrix: np.ndarray) -></mark> **<mark>int</mark>** <mark>:</mark> 3 _<mark>"""</mark>_ 4 _<mark>Design a novel algorithm to select the next node in each step.</mark>_ 5 6 _<mark>Args:</mark>_ 7 _<mark>current_node: ID of the current node.</mark>_ 8 _<mark>destination_node: ID of the destination node.</mark>_ 9 _<mark>unvisited_nodes: Array of IDs of unvisited nodes.</mark>_ 10 _<mark>distance_matrix: Distance matrix of nodes.</mark>_ 11 12 _<mark>Return:</mark>_ 13 _<mark>ID of the next node to visit.</mark>_ 14 _<mark>"""</mark>_ 15 <mark>next_node = unvisited_nodes[0]</mark> 16 **<mark>return</mark>** <mark>next_node</mark> 

### **Capacitated Vehicle Routing Problem (CVRP)** 

**Problem Definition:** CVRP aims to minimize the total traveling distances of a fleet of vehicles given a depot and a set of customers with coordinates and demands. Given: 1) Depot _v_ 0 and customers _{v_ 1, ..., _vn}_ with coordinates **x** _i ∈_ [0, 1]<sup>2</sup> , 2) Demands _di ∈_ Z<sup>+</sup> ( _d_ 0 = 0), 3) Vehicle capacity _Q ∈_ Z<sup>+</sup> , 4) Distance metric _cij_ = _∥_ **x** _i −_ **x** _j∥_ 2, find routes _R_ = _{r_ 1, ..., _rm}_ . Each route _rk_ starts/ends at _v_ 0. Capacity constraints are satisfied<sup>�</sup> _vi∈rk_<sup>_di≤Q_and all customers served exactly once. The</sup> objective is to minimize total distance. 

**Designed Heuristic:** Evaluation uses the same gap metric as TSP against 

#### **Data Generation:** 

- **Training Instances:** 256 instances with the number of nodes _n ∼U{_ 20, 200 _}_ nodes (including depot), capacity _Q ∼ U{_ 10, 150 _}_ , and demands _di ∼U{_ 1, 10 _}_ . The coordinates are generated using uniform distribution in [0, 1]<sup>2</sup> 

- **Testing Instances:** 128 test instances are generated with _nc ∈{_ 50, 100, 200, 500 _}_ cities, where each instance contains uniformly distributed coordinates in [0, 1]<sup>2</sup> , random demands _di ∼U{_ 1, 10 _}_ , and vehicle capacities _Q ∼U{_ 40, 150 _}_ . For each city size, 32 instances are created. 

The task description and template used are as follows: 

**CVRP Task Description:** Given a set of customers and a fleet of vehicles with limited capacity, the task is to design a novel algorithm to select the next node in each step, with the objective of minimizing the total cost. 

1 **<mark>import</mark>** <mark>numpy as np</mark> 2 **<mark>def</mark>** <mark>select_next_node(current_node:</mark> **<mark>int</mark>** <mark>, depot:</mark> **<mark>int</mark>** <mark>, unvisited_nodes: np.ndarray, rest_capacity: np.ndarray, demands: np.ndarray, distance_matrix: np.ndarray) -></mark> **<mark>int</mark>** <mark>:</mark> 3 _<mark>"""Design a novel algorithm to select the next node in each step.</mark>_ 4 _<mark>Args:</mark>_ 5 _<mark>current_node: ID of the current node.</mark>_ 6 _<mark>depot: ID of the depot.</mark>_ 7 _<mark>unvisited_nodes: Array of IDs of unvisited nodes.</mark>_ 8 _<mark>rest_capacity: rest capacity of vehicle</mark>_ 9 _<mark>demands: demands of nodes</mark>_ 10 _<mark>distance_matrix: Distance matrix of nodes.</mark>_ 11 _<mark>Return:</mark>_ 12 _<mark>ID of the next node to visit.</mark>_ 13 _<mark>"""</mark>_ 14 <mark>best_score = -1</mark> 15 <mark>next_node = -1</mark> 16 **<mark>for</mark>** <mark>node</mark> **<mark>in</mark>** <mark>unvisited_nodes:</mark> 17 <mark>demand = demands[node]</mark> 18 <mark>distance = distance_matrix[current_node][node]</mark> 19 **<mark>if</mark>** <mark>demand <= rest_capacity:</mark> 20 <mark>score = demand / distance</mark> 21 **<mark>if</mark>** <mark>score > best_score:</mark> 22 <mark>best_score = score</mark> 23 <mark>next_node = node</mark> 24 **<mark>return</mark>** <mark>next_node</mark> 

## **Method Details** 

We present the detailed prompts used in EoH-S. We have three different prompt engineering approaches for: 1) generating heuristics for the initial population, 2) diversity-aware search, and 3) local search. 

I’ll enhance the illustration by using different colours for each part of the prompt where: 

- _{_ Task description _}_ and _{_ Task template _}_ are the task description and template introduced in the last task section. 

- _{_ Heuristics _}_ are selected parent heuristic(s). 

- **Black sentences** are instructions for generating thoughts and codes. 

- Broan sentences are strategy-specific prompts for complementary-aware search and local search. 

- Gray words are additional instructions for robust and efficient inference. 

### **Initialization** 

The initialization phase generates the initial population of heuristic algorithms through the following prompt: 

#### **Initialization Prompt** 

- _{_ task description _}_ 

First, describe your new algorithm and main steps in one sentence. The description must be inside within boxed _{{}}_ . Next, implement the following Python function: 

- _{_ task template _}_ Do not give additional explanations. 

This prompt instructs the language model to generate a concise description of a new algorithm along with its implementation according to the specified function template. The description is required to be enclosed within double curly braces for easy extraction. 

### **Diversity-aware Search** 

The diversity-aware search phase aims to generate new algorithms that are distinct from existing ones in the population: 

#### **Diversity-aware Search Prompt** 

- _{_ task description _}_ 

I have 2 existing algorithms with their codes as follows: 

- _{_ heuristics _}_ 

These algorithms are effective for solving different instance distributions. Please help me create a new algorithm that is different from the given ones. 

First, describe your new algorithm and main steps in one sentence. The description must be inside within boxed _{{}}_ . Next, implement the following Python function: 

_{_ task template _}_ 

Do not give additional explanations. 

This prompt explicitly requests the language model to create an algorithm that differs from the existing ones in the population, promoting diversity in the search space. The existing algorithms are provided as context to guide the model toward unexplored algorithmic approaches. 

### **Local Search** 

The local search phase focuses on refining and improving a specific algorithm: 

#### **Local Search Prompt** 

_{_ task description _}_ 

I have one algorithm with its code as follows: 

- _{_ heuristic _}_ 

Please assist me in creating an improved version of the algorithm provided. 

First, describe your new algorithm and main steps in one sentence. The description must be inside within boxed _{{}}_ . Next, implement the following Python function: 

_{_ task template _}_ 

Do not give additional explanations. 

## **More Results** 

### **Convergence Curve and Complementary Performance** 

Figure 3 analyzes the convergence behaviour of the heuristic set designed using EoH-S on OBP. The upper section tracks performance progression as the number of samples increases, illustrating how the ensemble leverages complementary heuristics to improve solution quality. The lower section visualizes this complementary behavior through a radar plot, capturing the dominance of individual heuristics across three key convergence phases (initial, intermediate, and final). Each radar dimension corresponds to a problem instance (total: 256) and is colored by the top-performing heuristic (out of 10) for that instance. The legend quantifies heuristic dominance by reporting the number of instances where each heuristic ranked first, highlighting their specialized roles across the instance distribution. Figure 5 shows the results of EoH and ReEvo on CVRP. 

These figures demonstrate that EoH-S effectively evolves a set of complementary heuristics, with the following key observations: 

- **EoH-S achieves stable convergence.** The complementary population management in EoH-S adheres to Theorem 3 (see main paper), ensuring convergence within 2,000 samples. In contrast, as shown in Figure 5, both EoH and ReEvo exhibit fluctuations in complementary performance during optimization. While the single best heuristic (red curve) converges in these methods, their heuristic sets lack guaranteed complementary performance. Notably, ReEvo’s final top-10 heuristics underperform compared to those found mid-search, highlighting its instability in maintaining complementary behavior. 

- **EoH-S generates a complementary heuristic set.** On both OBP and CVRP, EoH-S progressively improves heuristic diversity and performance. Initially, one or two heuristics dominate, but EoH-S systematically explores new heuristics to enhance both individual and collective performance. In the final set, all 10 heuristics contribute meaningfully across the 256 instances. In contrast, EoH retains two fully dominated heuristics, and ReEvo’s top one heuristic dominates nearly half the instances (119/256). Although ReEvo’s mid-search heuristics show better complementarity, its focus on optimizing only the single best heuristic (red curve) fails to ensure sustained improvement for the entire set. 

- **Complementary behaviour varies by problem domain.** EoH-S produces a more balanced heuristic set for CVRP than for OBP. On OBP, one heuristic dominates most instances initially, and the top two heuristics still cover over half the instances in the final set. This disparity arises because the 256 CVRP instances with varying capacities and sizes are inherently more diverse and challenging than OBP instances. These results underscore the importance of complementary heuristic design while also revealing a limitation: EoH-S may be less effective when instance diversity is low (e.g., if a single heuristic suffices for all instances). 



<!-- Start of picture text -->
EoH-S Performance on OBP (Population Size 10)<br>0.040<br>0.038<br>0.036<br>0.034<br>0 250 500 750 1000 1250 1500 1750 2000<br>Number of Samples<br>Set at 90 samples H1: 127 insH2: 1 ins Set at 650 samples H1: 68 insH2: 13 ins Set at 2010 samples H1: 53 insH2: 26 ins<br>H1 H3: 9 ins H1 H3: 10 ins<br>H4: 3 ins H4: 13 ins<br>H5: 7 ins H5: 7 ins<br>4 2 4 2 H6: 10 ins 4 2 H6: 4 ins<br>6 6 H7: 5 ins 6 H7: 4 ins<br>H1 8 H2 0.20.0.75 5 0 8 H10 0.20.0.75 5 H8: 7 insH9: 2 ins0 H2 8 H10 0.20.0.75 5 H8: 4 insH9: 3 ins0<br>H9 H10: 4 ins H9 H10: 4 ins<br>H2 H8 H8<br>H7<br>H3<br>H3H4H5 H6 H4 H5H6H7<br>Heuristic 1 Heuristic 3 Heuristic 5 Heuristic 7 Heuristic 9<br>Heuristic 2 Heuristic 4 Heuristic 6 Heuristic 8 Heuristic 10<br>Complementary Performance<br><!-- End of picture text -->

Figure 3: Convergence of EoH-S on OBP: The upper section depicts the performance w.r.t., the number of samples, while the lower section presents a radar plot characterizing the complementary behaviour at three distinct phases of the convergence process (initial, intermediate, and final). The radar plot dimensions represent the best-performing heuristic among the 10 heuristics in the heuristic set for each of the 128 problem instances, with each dimension colored according to the identity of the topperforming heuristic. The accompanying legend reports the number of instances for which each heuristic achieved the highest ranking, providing insight into their complementary behaviour on the 128 diverse instances. 

### **Designed Heuristics** 

We illustrate some example heuristics for EoH, ReEvo, and EoH-S. 



<!-- Start of picture text -->
EoH-S Performance on CVRP (Population Size 10)<br>0.30<br>0.25<br>0.20<br>0.15<br>0 250 500 750 1000 1250 1500 1750 2000<br>Number of Samples<br>H1<br>Set at 30 samples H1: 127 ins Set at 600 samples H1: 40 ins Set at 2000 samples H1: 29 ins<br>H2: 46 ins H3 H2 H2: 20 ins H3 H2 H2: 31 ins<br>H3: 34 ins H3: 43 ins H4 H3: 23 ins<br>H4: 20 ins H4: 28 ins H4: 28 ins<br>0.10.20.30.4H5: 5 insH6: 8 ins H4 0.10.20.3H10.4H5: 17 insH6: 14 ins 0.10.20.3H10.4H5: 25 insH6: 20 ins<br>0.25 0.50H7: 3 insH8: 5 insH9: 1 insH10H9 0.75 H5 0.25 H10 0.50H7: 21 insH8: 27 insH9: 28 ins0.75 H5 0.25 H10 0.50H7: 19 insH8: 27 insH9: 33 ins0.75<br>H10: 7 insH8 H10: 18 ins H6 H10: 21 ins<br>H7 H6<br>H9<br>H2 H6 H7 H7 H9<br>H5 H8 H8<br>H4<br>H3<br>Heuristic 1 Heuristic 3 Heuristic 5 Heuristic 7 Heuristic 9<br>Heuristic 2 Heuristic 4 Heuristic 6 Heuristic 8 Heuristic 10<br>Complementary Performance<br><!-- End of picture text -->

Figure 4: Convergence of EoH-S on CVRP: The upper section depicts the performance w.r.t., the number of samples, while the lower section presents a radar plot characterizing the complementary behaviour at three distinct phases of the convergence process (initial, intermediate, and final). The radar plot dimensions represent the best-performing heuristic among the 10 heuristics in the heuristic set for each of the 256 problem instances, with each dimension colored according to the identity of the topperforming heuristic. The accompanying legend reports the number of instances for which each heuristic achieved the highest ranking, providing insight into their complementary behaviour on the 256 diverse instances. 



<!-- Start of picture text -->
EoH Performance on CVRP<br>0.35<br>Heuristic Set (n=10)<br>Best Single Heuristic<br>0.30<br>0.25<br>0.20<br>0 250 500 750 1000 1250 1500 1750 2000<br>Number of Samples<br>H2<br>H1 H4<br>Set at 30 samples H1: 79 ins Set at 620 samples H1: 59 ins Set at 2000 samples H1: 48 ins<br>H2: 72 ins H2 H2: 33 ins H5 H1H2: 19 ins<br>H3: 17 ins H1 H3: 56 ins H4: 28 ins<br>H2 0.2 0.4H4: 13 insH5: 7 ins H3 0.2 0.4H4: 41 insH7: 35 ins 0.2 0.4H5: 20 insH6: 39 ins<br>0.25 0.50H6: 34 insH7: 8 insH100.75 0.25H1 00.50H8: 13 insH9: 9 ins0.75 H6 0.25 0.50H7: 40 insH9: 24 ins0.75<br>H8: 11 insH9 H9 H10: 10 ins H10: 38 ins<br>H9: 6 insH10: 9 insH8 H4 H7 H8 H10<br>H3 H7<br>H4H5 H6 H7 H9<br>Heuristic 1 Heuristic 3 Heuristic 5 Heuristic 7 Heuristic 9<br>Heuristic 2 Heuristic 4 Heuristic 6 Heuristic 8 Heuristic 10<br>ReEvo Performance on CVRP<br>Heuristic Set (n=10)<br>Best Single Heuristic<br>0.30<br>0.25<br>0.20<br>0 250 500 750 1000 1250 1500 1750 2000<br>Number of Samples<br>Set at 30 samplesH1 H1: 171 insH2: 58 insH3: 8 insH4: 7 ins Set at 620 samplesH2 H1 H1: 66 insH2: 29 insH3: 24 insH4: 11 ins Set at 2000 samplesH1 H1: 119 insH2: 31 insH3: 30 insH4: 14 ins<br>0.2 0.25 0.4 0.50 H4 H1 H6H7H8 H 0.6900.75H6: 3 insH7: 3 insH8: 3 insH9: 1 insH10: 2 ins H4H5H3 0.2 0.25 H100.40.50H5: 30 insH6: 19 insH7: 24 insH8: 18 insH9: 22 insH10: 13 ins0.75 H2 0.2 0.25 0.4H9 H10.5 00H5: 14 insH6: 7 insH7: 8 insH8: 5 insH9: 26 insH10: 2 ins0.75<br>H3 H9<br>H6 H8 H3<br>H2 H7 H4 H5 H6H7H8<br>Heuristic 1 Heuristic 3 Heuristic 5 Heuristic 7 Heuristic 9<br>Heuristic 2 Heuristic 4 Heuristic 6 Heuristic 8 Heuristic 10<br>Performance<br>Performance<br><!-- End of picture text -->

Figure 5: Convergence of EoH and ReEvo on CVRP: The upper section depicts the performance w.r.t., the number of samples, while the lower section presents a radar plot characterizing the complementary behaviour at three distinct phases of the convergence process (initial, intermediate, and final). The red curve indicates the convergence of the single current best heuristic in terms of average performance, while the blue curve is the complementary performance of the top 10 heuristics. The radar plot dimensions represent the best-performing heuristic among the 10 heuristics in the heuristic set for each of the 256 problem instances, with each dimension colored according to the identity of the top-performing heuristic. 

#### **EoH on OBP** 

1 def priority(item: float, bins: np.ndarray) 2 remaining = bins - item 3 valid = remaining >= 0 4 fill_ratio = np.where(bins > 0, item / bins, 0) 5 remaining_norm = np.where(bins > 0, remaining / np.max(bins), 0) 6 weight = 1.0 - (bins / np.max(bins)) ** 2 7 priority_scores = np.where(valid, fill_ratio * 0.3 + remaining_norm * 0.7 * weight, -np.inf) 8 return priority_scores 

#### **ReEvo on OBP** 

1 def priority(item: float, bins: np.ndarray) -> np.ndarray: 2 remaining_space = bins - item 3 valid_mask = remaining_space >= 0 4 5 if not np.any(valid_mask): 6 return np.zeros_like(bins) 7 8 # Moderate exact fit boost 9 exact_fit = (remaining_space == 0).astype(float) * 1e4 10 11 # Adaptive exponent based on global fill ratio 12 residuals = remaining_space[valid_mask] / bins[valid_mask] 13 global_fill = 1 - np.mean(residuals) 14 exponent = 3 + 8 * global_fill # Smoothly varies from 3 to 11 15 16 # Core penalty terms 17 tight_fit = 1 / (1e-6 + residuals**exponent) 18 slack_penalty = 1 / (1e-6 + (1 - residuals)**exponent) 19 20 # Gradual blending with optimized transition 21 transition_point = 0.6 + 0.2 * global_fill # Adaptive transition 22 blend_weight = 1 / (1 + np.exp(-15*(global_fill-transition_point))) 23 24 # Simple harmonic mean 25 harmonic = (2 * tight_fit * slack_penalty) / (1e-6 + tight_fit + slack_penalty) 26 27 # Final priorities 28 priorities = np.zeros_like(bins) 29 priorities[valid_mask] = ( 30 exact_fit[valid_mask] + 31 blend_weight * tight_fit + 32 (1 - blend_weight) * harmonic 33 ) 34 35 return priorities 

Figure 6: Heuristics designed by EoH and ReEvo for OBP. 

#### **EoH-S on OBP (2 Complimentary Heuristics)** 

1 def priority(item: float, bins: np.ndarray) -> np.ndarray: 2 capacity_ratio = np.percentile(bins, 80) / np.percentile(bins, 20) 3 dynamic_target = 0.55 + 0.25 * (1 / (1 + np.exp(-3.0 * (capacity_ratio - 1.1)))) 4 remaining = bins - item 5 valid = remaining >= 0 6 filled = (bins - remaining) / bins 7 # Enhanced multi-tier capacity scoring 8 tier_weights = 0.85 + 0.5 * np.tanh(2.5 * (bins / np.percentile(bins, 65) - 1.2) ) 9 optimal_zone = dynamic_target * (1 + 0.18 * np.sin(1.5 * np.pi * tier_weights)) 10 # Dual-phase attraction-repulsion 11 attraction = np.exp(-5 * np.abs(filled - optimal_zone)) 12 repulsion = 1 - 0.35 * np.power(np.maximum(0, filled - (optimal_zone + 0.15)), 2.0) 13 reward = 3.5 * attraction * repulsion * tier_weights 14 # Density-adaptive dispersion 15 density_gradient = np.abs(filled - np.median(filled[valid])) if np.any(valid) else 0 16 dispersion = 1.4 - 0.4 * np.tanh(6 * density_gradient) * (1 - 0.25 * np.cos(3 * np.pi * filled)) 17 # Resonant harmonic modulation 18 harmonic_factor = 1 + 0.2 * np.sin(3 * np.pi * (filled - dynamic_target + 0.05)) 19 priority_scores = np.where(valid, 20 -np.log1p(remaining) * reward * dispersion * harmonic_factor, 21 np.inf) 22 return priority_scores 23 24 def priority(item: float, bins: np.ndarray) -> np.ndarray: 25 remaining = bins - item 26 valid = remaining >= 0 27 normalized_remaining = np.where(bins > 0, remaining / bins, 0) 28 current_fill = 1 - normalized_remainin 29 # Enhanced dynamic target adaptation 30 mean_bins = np.mean(bins) 31 std_bins = np.std(bins) + 1e-9 32 dynamic_target = 0.65 + 0.15 * (1 / (1 + np.exp(-mean_bins / (std_bins + 1e-9))) ) + 0.02 * np.tanh(mean_bins) 33 # Adaptive sigmoid scaling 34 fill_deviation = current_fill - dynamic_target 35 adaptive_scale = 7.0 + 5.0 * np.tanh(np.var(bins) / (mean_bins**2 + 1e-9)) 36 reward = 2.0 / (1 + np.exp(-fill_deviation * adaptive_scale)) + 1.0 37 # Bin-size-aware logarithmic capacity utilization 38 size_factor = np.log1p(bins / (mean_bins + 1e-9)) ** 0.35 39 capacity_term = (1 - np.exp(-3.5 * normalized_remaining)) * (0.85 + 0.15 * size_factor) 40 # Triple-phase stability mechanism 41 global_fill = np.mean(current_fill[valid]) if np.any(valid) else dynamic_target 42 historical_fill = np.mean(current_fill) if len(bins) > 1 else dynamic_target 43 local_stability = 0.90 + 0.10 * np.exp(-15 * (current_fill - dynamic_target)**2) 44 global_stability = 0.92 + 0.08 * np.exp(-20 * (current_fill - global_fill)**2) 45 historical_stability = 0.94 + 0.06 * np.exp(-25 * (current_fill - historical_fill)**2) 46 # Dynamic fragmentation penalty 47 skewness = np.mean((bins - mean_bins)**3) / (std_bins**3 + 1e-9) 48 kurtosis = np.mean((bins - mean_bins)**4) / (std_bins**4 + 1e-9) - 3 49 fragmentation = (np.abs(normalized_remaining - 0.5) * 0.3 + 50 np.abs(skewness) * 0.4 + 51 np.abs(kurtosis) * 0.3) if np.any(valid) else 0 52 53 priority_scores = np.where(valid, -capacity_term * reward * local_stability * global_stability * historical_stability / (1 + fragmentation), np.inf) 54 return priority_scores 

Figure 7: Two heuristics selected from the heuristic set designed by EoH-S for OBP. 

#### **EoH on TSP** 

1 def select_next_node(current_node: int, destination_node: int, unvisited_nodes: np. ndarray, distance_matrix: np.ndarray) -> int: 2 current_dist = distance_matrix[current_node, unvisited_nodes] 3 dest_dist = distance_matrix[destination_node, unvisited_nodes] 4 5 momentum = np.sum(distance_matrix[unvisited_nodes] - distance_matrix[ current_node, unvisited_nodes].reshape(-1, 1), axis=1) 6 degree_attraction = np.sum(distance_matrix[unvisited_nodes] > 0, axis=1) 7 cluster_penalty = -np.mean(distance_matrix[:, unvisited_nodes], axis=0) 8 exploitation = np.random.rand(len(unvisited_nodes)) 9 10 remaining_nodes = len(unvisited_nodes) 11 total_nodes = len(distance_matrix) 12 progress = remaining_nodes / total_nodes 13 14 momentum_weight = np.tanh(progress) 15 attraction_weight = 1 / (1 + np.exp(-5 * (1 - progress))) 16 penalty_weight = np.tanh(1 - progress) 17 exploitation_weight = 0.1 * progress 18 19 combined_score = (momentum_weight * momentum) + (attraction_weight * degree_attraction) + (penalty_weight * cluster_penalty) + ( exploitation_weight * exploitation) 20 return unvisited_nodes[np.argmax(combined_score)] 

#### **ReEvo on TSP** 

1 def select_next_node(current_node: int, destination_node: int, unvisited_nodes: np. ndarray, distance_matrix: np.ndarray) -> int: 2 if len(unvisited_nodes) == 1: 3 return unvisited_nodes[0] 4 # Current proximity (harmonic to handle zero distances) 5 current_dists = distance_matrix[current_node, unvisited_nodes] 6 proximity = 1 / (current_dists + 1e-8) 7 # Exact future potential via MST approximation 8 future_potential = np.zeros(len(unvisited_nodes)) 9 for i, node in enumerate(unvisited_nodes): 10 remaining_nodes = np.delete(unvisited_nodes, i) 11 if not remaining_nodes.size: 12 future_potential[i] = 0 13 continue 14 # Approximate remaining tour length using nearest neighbor distances 15 remaining_dists = distance_matrix[node, remaining_nodes] 16 future_potential[i] = np.mean(np.sort(remaining_dists)[:3]) # Top-3 nearest 17 # Normalization with stability guarantees 18 def safe_normalize(x): 19 x = x - x.min() 20 return x / (x.max() + 1e-8) 21 p_norm = safe_normalize(proximity) 22 fp_norm = safe_normalize(future_potential) 23 # Adaptive weights using sigmoid transition 24 progress = 1 - len(unvisited_nodes) / distance_matrix.shape[0] 25 exploit_weight = 0.8 / (1 + np.exp(5*(progress - 0.6))) # Sigmoid centered at 60% 26 explore_weight = 0.2 * (1 - progress)**2 # Quadratic decay 27 # Combined score with directional exploration 28 base_score = 0.6*p_norm + 0.4*fp_norm 29 noise = np.random.normal(0, 0.05, len(unvisited_nodes)) * explore_weight 30 combined_score = exploit_weight * base_score + noise 31 return unvisited_nodes[np.argmax(combined_score)] 

Figure 8: Heuristics designed by EoH and ReEvo on TSP. 

#### **EoH-S on TSP** 

1 def select_next_node(current_node: int, destination_node: int, unvisited_nodes: np. ndarray, distance_matrix: np.ndarray) -> int: 2 current_dist = distance_matrix[current_node, unvisited_nodes] 3 dest_dist = distance_matrix[destination_node, unvisited_nodes] 4 progress = distance_matrix[current_node, destination_node] - dest_dist 5 exploration_factor = np.log(len(unvisited_nodes) + 1) * (1 + np.random.rand() * 0.5) 6 centrality = np.mean(distance_matrix[unvisited_nodes][:, unvisited_nodes], axis =1) 7 penalty = np.maximum(0, dest_dist - np.percentile(dest_dist, 85)) 8 k = min(5, len(unvisited_nodes) - 1) 9 if k > 0: 10 sub_matrix = distance_matrix[np.ix_(unvisited_nodes, unvisited_nodes)] 11 cluster_novelty = -np.mean(np.partition(sub_matrix, k, axis=1)[:, :k], axis =1) 12 else: 13 cluster_novelty = np.zeros(len(unvisited_nodes)) 14 if len(unvisited_nodes) < len(distance_matrix) - 1: 15 last_move_dir = distance_matrix[unvisited_nodes, current_node] - distance_matrix[unvisited_nodes, destination_node] 16 momentum = np.abs(last_move_dir - np.mean(last_move_dir)) * (1 + 0.1 * np. random.rand()) 17 else: 18 momentum = np.zeros(len(unvisited_nodes)) 19 path_diversity = np.std(distance_matrix[unvisited_nodes], axis=1) * (1 + 0.1 * np.random.rand()) 20 remaining_path_heuristic = np.mean(distance_matrix[unvisited_nodes], axis=1) * (1 - 0.1 * np.random.rand()) 21 phase = len(unvisited_nodes) / len(distance_matrix) 22 scale_factor = np.mean(distance_matrix) / np.max(distance_matrix) 23 entropy = -np.sum(np.exp(-current_dist) * np.log(np.exp(-current_dist) + 1e-10)) 24 entropy_factor = 0.1 * entropy * (1 - phase) 25 w_dist = (0.25 + (0.05 * phase)) * scale_factor 26 w_progress = (0.15 - (0.05 * phase)) * scale_factor 27 w_explore = (0.15 - (0.05 * phase)) * (1 - scale_factor) + entropy_factor 28 w_centrality = (0.1 + (0.05 * phase)) * scale_factor 29 w_penalty = (0.1 - (0.05 * phase)) * scale_factor 30 w_novelty = (0.1 + (0.05 * phase)) * (1 - scale_factor) 31 w_momentum = (0.05 * (1 - phase)) * scale_factor 32 w_diversity = (0.05 * (1 - phase)) * (1 - scale_factor) 33 w_heuristic = (0.05 * phase) * (1 - scale_factor) 34 score = (w_dist * current_dist) + (w_progress * progress) + (w_explore * exploration_factor) - (w_centrality * centrality) + (w_penalty * penalty) + ( w_novelty * cluster_novelty) + (w_momentum * momentum) + (w_diversity * path_diversity) + (w_heuristic * remaining_path_heuristic) 35 return unvisited_nodes[np.argmin(score)] 

Figure 9: Heuristic designed by EoH-S for TSP. 

#### **EoH on CVRP** 

1 def select_next_node(current_node: int, depot: int, unvisited_nodes: np.ndarray, rest_capacity: np.ndarray, demands: np.ndarray, distance_matrix: np.ndarray) -> int: 2 """Design a novel algorithm to select the next node in each step. 3 Args: 4 current_node: ID of the current node. 5 depot: ID of the depot. 6 unvisited_nodes: Array of IDs of unvisited nodes. 7 rest_capacity: rest capacity of vehicle 8 demands: demands of nodes 9 distance_matrix: Distance matrix of nodes. 10 Return: 11 ID of the next node to visit. 12 """ 13 feasible_nodes = unvisited_nodes[demands[unvisited_nodes] <= rest_capacity] 14 if len(feasible_nodes) == 0: 15 return depot 16 17 current_distances = distance_matrix[current_node, feasible_nodes] 18 depot_distances = distance_matrix[feasible_nodes, depot] 19 distance_savings = (distance_matrix[current_node, depot] + distance_matrix[depot , feasible_nodes]) - current_distances 20 21 demand_ratio = demands[feasible_nodes] / (rest_capacity + 1e-6) 22 23 avg_distances = np.mean(distance_matrix[feasible_nodes][:, feasible_nodes], axis =1) 24 density_ratio = current_distances / (avg_distances + 1e-6) 25 26 capacity_factor = rest_capacity / (np.max(demands[feasible_nodes]) + 1e-6) 27 proximity_factor = np.mean(current_distances) / (np.mean(depot_distances) + 1e -6) 28 29 w1 = max(0.3, 0.7 - capacity_factor * 0.4) 30 w2 = min(0.4, 0.2 + proximity_factor * 0.2) 31 w3 = 1.0 - w1 - w2 32 33 weights = w1 * distance_savings + w2 * demand_ratio + w3 * (1 / (density_ratio + 1e-6)) 34 next_node = feasible_nodes[np.argmax(weights)] 35 return next_node 

Figure 10: Heuristic designed by EoH for CVRP. 

#### **ReEvo on CVRP** 

1 def select_next_node(current_node: int, depot: int, unvisited_nodes: np.ndarray, rest_capacity: np.ndarray, demands: np.ndarray, distance_matrix: np.ndarray) -> int: 2 if not unvisited_nodes.size: 3 return depot 4 # Adaptive capacity buffer with demand characteristics and route progress 5 demand_stats = demands[unvisited_nodes] 6 demand_cv = np.std(demand_stats) / (np.mean(demand_stats) + 1e-10) 7 route_progress = 1 - len(unvisited_nodes) / len(demands) 8 # Three-component adaptive buffer 9 buffer = (0.02 + 0.06 * (1 - np.exp(-3 * (demand_cv - 0.3))) + 0.03 * route_progress * (1 + 0.5 * demand_cv)) 10 feasible_mask = demands[unvisited_nodes] <= rest_capacity * (1 + buffer) 11 feasible_nodes = unvisited_nodes[feasible_mask] 12 if not feasible_nodes.size: 13 return depot 14 # Robust distance metrics using percentile normalization 15 current_dists = distance_matrix[current_node, feasible_nodes] 16 depot_dists = distance_matrix[feasible_nodes, depot] 17 dist_p90 = np.percentile(distance_matrix, 90) 18 # Normalized components with outlier protection 19 norm_current = (current_dists - np.min(current_dists)) / (np.ptp(current_dists) + 1e-10) 20 norm_depot = (depot_dists - np.min(depot_dists)) / (np.ptp(depot_dists) + 1e-10) 21 # Route state analysis with multiple factors 22 remaining_demand = np.sum(demands[unvisited_nodes]) 23 capacity_ratio = min(1.0, remaining_demand / (rest_capacity + 1e-10)) 24 urgency = (len(unvisited_nodes) / len(demands)) ** 0.7 25 # Core scoring components with enhanced formulations 26 proximity = (0.8 / (current_dists + 0.1*dist_p90) + 27 0.2 * (1 - norm_current) * (1 + 0.3 * urgency)) 28 utilization = np.power(demands[feasible_nodes], 0.8) / (rest_capacity + 1e-10) 29 spatial_cohesion = np.exp(-3 * abs(norm_current - (1 - norm_depot))) 30 # Dynamic weight adaptation using route state 31 proximity_weight = 0.7 - 0.2 * (1 / (1 + np.exp(-12 * (capacity_ratio - 0.4)))) 32 utilization_weight = 0.6 / (1 + np.exp(-10 * (1.2 - capacity_ratio))) 33 spatial_weight = 0.4 * (1 - np.exp(-3 * urgency)) 34 # Advanced spatial clustering analysis 35 if len(feasible_nodes) > 1: 36 centroid = np.mean(distance_matrix[feasible_nodes], axis=0) 37 spatial_scores = np.linalg.norm(distance_matrix[feasible_nodes] - centroid, axis=1) 38 spatial_scores = (spatial_scores - np.min(spatial_scores)) / (np.ptp( spatial_scores) + 1e-10) 39 else: 40 spatial_scores = np.zeros(len(feasible_nodes)) 41 # Adaptive critical demand detection 42 demand_ratio = demands[feasible_nodes] / rest_capacity 43 critical_threshold = (0.5 + 0.3 * np.tanh(5 * (demand_cv - 0.4)) + 0.15 * route_progress) 44 critical_bonus = np.where(demand_ratio > critical_threshold, (demand_ratio - critical_threshold) ** 1.5, 0) 45 # Balanced composite scoring 46 scores = (proximity_weight * proximity + utilization_weight * utilization + spatial_weight * spatial_cohesion + 0.7 * spatial_scores + 1.5 * critical_bonus) 47 # Sophisticated tie-breaking mechanism 48 best_idx = np.argmax(scores) 49 if np.sum(np.isclose(scores, scores[best_idx], rtol=1e-8, atol=1e-8)) > 1: 50 tied_nodes = feasible_nodes[np.isclose(scores, scores[best_idx])] 51 tie_breakers = np.column_stack([-critical_bonus[np.isclose(scores, scores[ best_idx])], -spatial_cohesion[np.isclose(scores, scores[best_idx])], current_dists[np.isclose(scores, scores[best_idx])], -utilization[np. isclose(scores, scores[best_idx])]]) 52 return tied_nodes[np.lexsort(tie_breakers.T)[0]] 53 return feasible_nodes[best_idx] 

Figure 11: Heuristic designed by ReEvo for CVRP. 

#### **EoH-S on CVRP** 

- 1 def select_next_node(current_node: int, depot: int, unvisited_nodes: np.ndarray, rest_capacity: np.ndarray, demands: np.ndarray, distance_matrix: np.ndarray) -> int: 

- 2 feasible_nodes = unvisited_nodes[demands[unvisited_nodes] <= rest_capacity] 3 if len(feasible_nodes) == 0: 4 return depot 

5 6 distances = distance_matrix[current_node, feasible_nodes] 7 depot_distances = distance_matrix[feasible_nodes, depot] 8 normalized_demands = demands[feasible_nodes] / np.max(demands[feasible_nodes]) 9 capacity_ratio = rest_capacity / np.max(demands[feasible_nodes]) 10 urgency = np.sum(demands[unvisited_nodes]) / (rest_capacity + 1e-6) 11 entropy = np.std(distance_matrix[feasible_nodes][:, feasible_nodes]) / (np.mean( distance_matrix) + 1e-6) 12 13 pheromone = np.exp(-(distances**0.75 + 1.2*depot_distances**0.65) / (1.3 * np. mean(distance_matrix))) 14 swarm_intensity = 0.7 * (1 + np.tanh(2.1 - capacity_ratio**0.85)) * pheromone 15 fuzzy_factor = 0.3 * (1 - np.exp(-entropy/(np.mean(distances) + 1e-6))) * (1 - 0.25*swarm_intensity) 16 17 proximity_weight = 0.42 * (1 - 0.22 * np.exp(-capacity_ratio**0.9)) * swarm_intensity 18 demand_weight = 0.36 * (1 + 0.55 * np.tanh(urgency**0.7)) * swarm_intensity 19 neighborhood_weight = 0.15 * (1 - entropy**0.6) * (1 - 0.2*swarm_intensity) 20 entropy_weight = 0.05 * np.exp(-np.std(distances)/(np.mean(distances) + 1e-6)) * fuzzy_factor 21 adaptive_weight = 0.02 * (1 - np.exp(-np.std(normalized_demands)/(np.mean( normalized_demands) + 1e-6))) * fuzzy_factor 22 23 proximity_scores = 1.25/(distances + 1e-6)**0.6 + 1.0/(depot_distances + 1e-6) **<sup>0.5</sup> 24 demand_scores = normalized_demands**1.6 * proximity_scores 25 neighborhood_scores = np.array([np.sum(distance_matrix[n][feasible_nodes]) for n in feasible_nodes]) / (distances + 1e-6)**0.3 26 entropy_scores = (rest_capacity - demands[feasible_nodes])**0.85 * depot_distances / (distances + 1e-6) 27 adaptive_scores = (0.45 + 0.55*np.random.rand(len(feasible_nodes)))**1.9 * ( demands[feasible_nodes] / (distances + 1e-6)**0.4) 28 29 combined_scores = ( 30 proximity_weight * proximity_scores + 31 demand_weight * demand_scores + 32 neighborhood_weight * neighborhood_scores + 33 entropy_weight * entropy_scores + 34 adaptive_weight * adaptive_scores 35 ) 36 37 return feasible_nodes[np.argmax(combined_scores)] 

Figure 12: Heuristic designed by EoH-S for CVRP. 

### **Detailed Results on Benchmark Sets** 

**BPPLib** We select several representative benchmark sets from BPPLib (Delorme, Iori, and Martello 2018). The chosen sets and their characteristics are summarized in Table 5, comprising over 700 instances with item counts ranging from 100 to 1,002. For consistency in evaluation, we normalize the bin capacity to 100. Due to space constraints, we omit detailed per-instance results, but the complete data will be available as supplementary materials. 

Table 5: BPPLib benchmark sets. 

|Benchmark Set<br>Number of Instan|ces<br>Capacity|Number of Items|
|---|---|---|
|Schwerin<br>~~1~~(Scholl, Klein, and J¨urgens 1997)<br>100|1k|100|
|Schwerin<br>~~2~~(Scholl, Klein, and J¨urgens 1997)<br>100|1k|120|
|AugmentedIRUP (Delorme, Iori, and Martello 2016)<br>250|_{_2.5K–80K_}_|_{_201-1002_}_|
|AugmentedNonIRUP (Delorme, Iori, and Martello 2016)<br>250|_{_2.5K–80K_}_|_{_201-1002_}_|
|Scholl<br>Hard (Delorme, Iori, and Martello 2018)<br>28|10000|_{_160-200_}_|



**TSPLib** We select commonly used 49 symmetric Euclidean TSPLib instances (Reinelt 1991), with problem sizes ranging from 52 to 1,000 nodes. For consistent evaluation, we normalize all coordinates to the range [0, 1]<sup>2</sup> by scaling both dimensions uniformly using the maximum spatial extent: 



This approach preserves the original aspect ratio while ensuring all instances are comparably scaled. 

The detailed results on all instances are listed in Table 7. We report the relative gap to LKH (Helsgaun 2017). Results show that EoH-S ranks the first on almost all the instances (46 out of 49). 

**CVRPLib** We select 7 commonly used benchmark sets, including A, B, E, F, M, P, and X, from CVRPLib (Uchoa et al. 2017). The chosen sets and their characteristics are summarized in Table 6. Due to the time limit, we do not test on all instances from the X set. For consistent evaluation, we normalize all coordinates to the range [0, 1]<sup>2</sup> by scaling both dimensions uniformly using the maximum spatial extent, similar to TSPLib. 

Table 6: CVRPLib benchmark sets 

|Benchmark Set|Number of Instances|Instance Size|
|---|---|---|
|Set A|27|31-79|
|Set B|23|30-77|
|Set E|11|22-101|
|Set F|3|44-134|
|Set M|5|100-199|
|Set P|23|15-100|
|Set X|43|100-300|



The detailed results are presented in Tables 8, 9, and 10. EoH-S consistently outperforms existing methods across benchmark instances of varying sizes and distributions, ranking first in over half of the instances and achieving the best average performance with significant improvements. 

Table 7: Results on TSPLib instances 

|Instance|Funs|earch|E|oH|Re|evo|EoH-S|
|---|---|---|---|---|---|---|---|
||top 1|top 10|top 1|top 10|top 1|top 10||
|a280|0.197|0.186|0.243|0.239|0.311|0.141|**0.137**|
|berlin52|0.177|0.158|0.163|0.163|0.206|0.112|**0.104**|
|bier127|0.132|0.132|0.174|0.161|0.155|0.155|**0.109**|
|ch130|0.163|0.141|0.158|0.132|0.281|0.160|**0.047**|
|ch150|0.161|0.130|0.213|0.149|0.242|0.203|**0.077**|
|d198|0.257|**0.138**|0.150|0.150|0.188|0.157|0.167|
|d493|0.148|0.148|0.192|0.168|0.186|0.154|**0.123**|
|d657|0.174|0.173|0.207|0.189|0.172|0.169|**0.153**|
|eil51|0.098|0.077|0.156|0.156|0.122|0.075|**0.044**|
|eil76|0.164|0.125|0.131|0.125|0.150|0.136|**0.063**|
|eil101|0.163|0.134|0.145|0.126|0.248|0.134|**0.098**|
|fl417|0.257|0.161|0.292|0.227|0.307|0.296|**0.147**|
|gil262|0.200|0.200|0.208|0.206|0.214|0.183|**0.115**|
|kroA100|0.202|0.108|0.130|0.123|0.342|0.193|**0.061**|
|kroB100|0.176|0.166|0.218|0.211|0.271|0.259|**0.115**|
|kroC100|0.191|0.161|0.177|0.154|0.180|0.180|**0.045**|
|kroD100|0.179|0.173|0.183|0.172|0.149|0.108|**0.092**|
|kroE100|0.133|0.114|0.189|0.173|0.232|0.199|**0.064**|
|kroA150|0.211|0.168|0.145|0.137|0.243|0.231|**0.101**|
|kroB150|0.146|0.117|0.116|0.116|0.283|0.265|**0.093**|
|kroA200|0.142|0.122|0.209|0.177|0.164|0.133|**0.089**|
|kroB200|0.193|0.160|0.203|0.203|0.153|0.099|**0.066**|
|lin105|0.247|0.161|0.149|0.146|0.447|0.179|**0.040**|
|lin318|0.149|0.149|0.121|0.121|0.323|0.200|**0.117**|
|p654|0.200|0.197|0.291|0.265|0.210|0.210|**0.105**|
|pcb442|0.145|0.136|0.184|0.182|0.190|0.158|**0.102**|
|pr76|0.154|0.135|0.156|0.153|0.330|0.070|**0.044**|
|pr107|0.274|0.259|0.142|0.132|0.028|**0.028**|0.045|
|pr124|0.237|0.116|0.251|0.209|0.228|0.205|**0.058**|
|pr136|0.136|0.134|0.174|0.151|0.101|0.101|**0.059**|
|pr144|0.086|0.081|0.179|0.179|0.136|0.136|**0.051**|
|pr152|0.277|0.222|0.211|0.196|0.320|0.164|**0.123**|
|pr226|0.183|0.139|0.199|0.197|0.209|0.209|**0.107**|
|pr264|0.217|0.189|0.244|0.214|0.167|0.148|**0.084**|
|pr299|0.219|0.184|0.288|0.288|0.194|0.194|**0.116**|
|pr439|0.261|0.203|0.231|0.231|0.208|0.164|**0.120**|
|rat99|0.144|**0.127**|0.149|0.148|0.246|0.163|0.128|
|rat195|0.112|0.092|0.071|0.071|0.099|0.096|**0.066**|
|rat575|0.171|0.125|0.152|0.152|0.219|0.182|**0.105**|
|rat783|0.144|0.139|0.204|0.189|0.261|0.204|**0.109**|
|rd100|0.174|0.170|0.158|0.158|0.292|0.203|**0.084**|
|rd400|0.167|0.154|0.156|0.148|0.219|0.195|**0.122**|
|st70|0.182|0.181|0.100|0.095|0.184|0.184|**0.026**|
|ts225|0.073|**0.033**|0.101|0.101|0.192|0.116|**0.033**|
|tsp225|0.149|0.103|0.235|0.215|0.180|0.121|**0.097**|
|u159|0.222|0.215|0.276|0.273|0.303|0.112|**0.083**|
|u574|0.243|0.213|0.207|0.197|0.225|0.194|**0.135**|
|u724|0.241|0.199|0.181|0.175|0.254|0.174|**0.123**|
|pr1002|0.206|0.206|0.226|0.220|0.222|0.209|**0.145**|
|Average|0.181|0.152|0.184|0.173|0.220|0.165|**0.093**|



Table 8: Results on CVRPLib instances (Set A and B) 

|Instance|FunS<br>|earch<br>|E<br>|oH<br>|Re<br>|Evo<br>|EoH-S|
|---|---|---|---|---|---|---|---|
||Top 1|Top 10|Top 1|Top 10|Top 1|Top 10||
|A-n32-k5|0.472|0.329|0.329|0.329|0.357|0.357|**0.309**|
|A-n33-k5|0.229|0.229|0.294|0.274|0.224|0.224|**0.198**|
|A-n33-k6|0.203|**0.203**|0.254|**0.203**|0.331|0.224|0.224|
|A-n34-k5|0.245|0.184|0.222|0.222|0.224|**0.161**|0.167|
|A-n36-k5|0.381|0.352|0.386|0.351|0.382|**0.278**|0.320|
|A-n37-k5|0399|0364|0449|0377|0392|0352|**0308**|
|A-n37-k6|.<br>0.284|.<br>0.281|.<br>0.354|.<br>0.279|.<br>0.366|.<br>**0.147**|**.**<br>0.148|
|A-n38-k5|0.389|0.389|0.356|**0.252**|0.339|0.312|0.256|
|A-n39-k5|0.387|0.336|0.268|0.231|0.200|**0.194**|0.230|
|A-n39-k6|0.332|0.284|**0.249**|**0.249**|0.396|0.285|0.295|
|A-n44-k6|0.347|0.227|0.199|0.199|0.219|0.219|**0.184**|
|A-n45-k6|0.606|0.360|0.315|0.308|0.463|0.398|**0.191**|
|A-n45-k7|0.220|0.213|0.212|0.204|0.195|0.159|**0.120**|
|A-n46-k7|0.367|0.332|0.505|0.385|0.388|**0.251**|0.285|
|A-n48-k7|0.331|**0.267**|0.327|0.307|0.338|0.300|0.271|
|A-n53-k7|0.435|0.317|0.244|0.244|0.380|0.322|**0.201**|
|A-n54-k7|0.234|0.227|0.215|0.215|0.329|0.187|**0.136**|
|A-n55-k9|0.317|0.287|0.369|0.333|0.248|**0.240**|0.278|
|A-n60-k9|0.317|0.317|0.425|0.310|0.323|**0.305**|0.332|
|A-n61-k9|0.506|0.327|0.466|0.244|0.447|0.244|**0.230**|
|A-n62-k8|0.368|0.280|0.329|0.276|0.334|0.250|**0.238**|
|A-n63-k9|0.312|0.309|0.286|0.240|0.182|0.169|**0.145**|
|A-n63-k10|0.486|0.323|0.334|0.257|0.420|0.377|**0.222**|
|A-n64-k9|0.377|0.285|0.333|0.327|0.322|0.245|**0.186**|
|A-n65-k9|0.441|0.359|0.388|**0.324**|0.468|0.345|0.342|
|A-n69-k9|0.409|0.298|0.370|0.297|0.293|0.253|**0.218**|
|A-n80-k10|0.382|0.258|0.311|0.252|0.332|0.245|**0.216**|
|B-n31-k5|0.239|0.238|0.150|0.150|0.086|0.081|**0.073**|
|B-n34-k5|0.095|0.091|0.157|0.091|0.269|0.089|**0.088**|
|B-n35-k5|0.316|0.203|0.203|0.199|0.305|**0.144**|0.200|
|B-n38-k6|0.434|0.431|0.441|0.285|0.332|0.332|**0.235**|
|B-n39-k5|0.919|0.915|0.985|0.778|0.946|0.517|**0.242**|
|B-n41-k6|0.159|0.159|0.204|**0.121**|0.225|0.195|0.131|
|B-n43-k6|0.291|0.191|0.210|0.194|0.204|**0.202**|0.208|
|B-n44-k7|0.308|0.298|0.220|0.220|0.181|**0.175**|0.209|
|B-n45-k5|0.363|0.339|0.283|0.283|0.315|0.315|**0.196**|
|B-n45-k6|0.510|0.490|0.433|0.250|0.593|0.273|**0.219**|
|B-n50-k7|0.327|0.327|0.476|0.350|0.404|0.355|**0.237**|
|B-n50-k8|0.142|0.132|0.192|0.144|0.229|0.136|**0.110**|
|B-n51-k7|0.304|0.205|0.310|0.310|0.333|0.118|**0.114**|
|B-n52-k7|0.661|0.490|0.551|0.539|0.737|0.488|**0.184**|
|B-n56-k7|0.768|0.603|0.734|0.663|0.508|0.429|**0.229**|
|B-n57-k7|0.368|0.368|0.450|0.450|0.406|0.256|**0.187**|
|B-n57-k9|0.224|0.187|0.176|0.176|0.164|0.164|**0.162**|
|B-n63-k10|0.427|0.356|0.307|0.307|0.388|0.269|**0.200**|
|B-n64-k9|0.491|0.380|0.626|0.451|0.431|0.351|**0.192**|
|B-n66-k9|0.283|0.202|0.251|0.251|0.192|0.183|**0.114**|
|B-n67-k10|0.536|0.466|0.394|0.367|0.413|0.246|**0.239**|
|B-n68-k9|0.250|0.219|0.282|0.225|0.195|0.195|**0.164**|
|B-n78-k10|0.362|0.286|0.575|0.333|0.244|**0.232**|0.282|
|Average|0.371|0.310|0.348|0.293|0.340|0.256|**0.209**|



Table 9: Results on CVRPLib instances (Set E, F, M and P) 

|Instance|Fun<br>|Search<br>|E<br>|oH<br>|Re<br>|Evo<br>|EoH-S|
|---|---|---|---|---|---|---|---|
||Top 1|Top 10|Top 1|Top 10|Top 1|Top 10||
|E-n22-k4|0.543|0.260|**0.187**|**0.187**|0.306|0.306|0.263|
|E-n23-k3|0.344|0.290|0.223|0.139|**0.197**|**0.197**|0.202|
|E-n30-k3|0.154|0.146|0.233|0.168|0.161|0.134|**0.133**|
|E-n33-k4|0.200|0.164|0.271|0.153|0.219|0.219|**0.132**|
|E-n51-k5|0.343|0.253|0.299|0.233|0.251|0.168|**0.166**|
|E-n76-k7|0.467|0.467|0.427|0.396|0.505|**0.294**|0.326|
|E-n76-k8|0.533|0.365|0.401|0.334|0.320|**0.274**|0.284|
|E-n76-k10|0.530|0.447|0.337|**0.272**|0.305|0.298|0.326|
|E-n76-k14|0.434|0.369|0.330|0.330|0.245|0.223|**0.212**|
|E-n101-k8|0.605|0.439|0.426|0.351|0.363|0.358|**0.290**|
|E-n101-k14|0.479|0.431|0.545|0.390|0.486|0.360|**0.324**|
|F-n45-k4|0.664|0.509|**0.444**|**0.444**|0.690|0.576|0.507|
|F-n72-k4|0.893|0.605|0.754|0.630|0.759|0.558|**0.452**|
|F-n135-k7|0.437|0.393|0.419|0.406|0.614|0.508|**0.321**|
|M-n101-k10|0.535|0.472|0.486|0.369|0.533|0.392|**0.225**|
|M-n121-k7|0.428|0.386|0.406|0.338|0.467|0.348|**0.231**|
|M-n151-k12|0.496|0.460|0.478|0.368|0.443|0.428|**0.358**|
|M-n200-k16|0.463|0.363|0.467|0.407|0.384|0.346|**0.320**|
|M-n200-k17|0.462|0.362|0.466|0.406|0.383|**0.345**|0.363|
|P-n16-k8|0.110|0.057|0.034|0.034|0.028|**0.010**|0.033|
|P-n19-k2|0.200|0.200|0.153|0.153|0.300|**0.079**|0.100|
|P-n20-k2|0.063|0.063|0.140|0.127|0.239|**0.020**|0.063|
|P-n21-k2|0.151|0.151|0.222|0.100|0.269|**0.065**|0.122|
|P-n22-k2|0.205|0.205|0.194|0.121|0.244|0.154|**0.098**|
|P-n22-k8|0.330|0.211|0.292|**0.210**|0.385|0.302|**0.210**|
|P-n23-k8|0.212|0.212|0.200|0.200|0.169|0.121|**0.087**|
|P-n40-k5|0.380|0.333|**0.203**|**0.203**|0.255|0.210|0.228|
|P-n45-k5|0.340|0.340|0.342|**0.212**|0.453|0.307|0.245|
|P-n50-k7|0.367|0.328|0.299|0.249|**0.201**|**0.201**|0.237|
|P-n50-k8|0.304|0.304|0.258|0.258|0.340|0.237|**0.198**|
|P-n50-k10|0.305|0.299|0.283|0.267|0.214|**0.193**|0.199|
|P-n51-k10|0.347|0.243|0.377|0.314|0.342|0.241|**0.200**|
|P-n55-k7|0.289|0.289|0.285|0.203|0.296|0.248|**0.181**|
|P-n55-k10|0.304|0.273|0.303|0.261|**0.186**|**0.186**|0.237|
|P-n55-k15|0.241|0.157|0.287|0.124|0.152|0.124|**0.104**|
|P-n60-k10|0.358|0.303|0.323|0.216|0.335|0.281|**0.166**|
|P-n60-k15|0.218|0.218|0.396|0.265|0.331|0.253|**0.145**|
|P-n65-k10|0.332|0.332|0.275|**0.212**|0.364|0.290|0.256|
|P-n70-k10|0.352|0.352|0.321|0.214|0.322|0.170|**0.143**|
|P-n76-k4|0.415|0.388|0.434|0.314|**0.200**|**0.200**|0.215|
|P-n76-k5|0.554|0.422|0.267|0.221|0.271|**0.195**|0.223|
|P-n101-k4|0.516|0.285|0.386|0.260|0.320|0.236|**0.190**|
|Average|0.379|0.313|0.330|0.263|0.330|0.254|**0.222**|



Table 10: Results on CVRPLib instances (Set X) 

|Instance|FunS<br>|earch<br>|E<br>|oH<br>|Re<br>|Evo<br>|EoH-S|
|---|---|---|---|---|---|---|---|
||Top 1|Top 10|Top 1|Top 10|Top 1|Top 10||
|X-n101-k25|0.479|0.379|0.488|0.353|0.392|0.312|**0.242**|
|X-n106-k14|0.096|0.091|0.080|0.079|0.107|0.070|**0.066**|
|X-n110-k13|0.285|0.218|0.221|0.214|0.251|**0.147**|0.169|
|X-n115-k10|0.493|0.439|0.487|0.407|0.503|**0.372**|0.394|
|X-n120-k6|0.192|0.189|0.203|0.184|0.202|**0.183**|0.184|
|X-n125-k30|0.226|0.175|0.173|0.173|0.214|0.149|**0.139**|
|X-n129-k18|0.241|0.170|0.199|0.199|0.154|**0.150**|0.167|
|X-n134-k13|0.607|0.469|0.582|0.415|0.538|0.369|**0.248**|
|X-n139-k10|0.224|0.212|0.260|0.230|0.260|0.226|**0.200**|
|X-n143-k7|0.426|0.391|0.545|0.397|0.417|0.366|**0.341**|
|X-n148-k46|0.279|0.275|0.325|0.229|0.168|**0.139**|0.205|
|X-n153-k22|0.429|0.412|0.427|0.395|0.399|0.388|**0.285**|
|X-n157-k13|0.098|0.091|0.068|0.068|0.225|0.212|**0.063**|
|X-n162-k11|0.215|0.205|**0.139**|**0.139**|0.237|0.147|0.173|
|X-n167-k10|0.236|**0.202**|0.275|0.209|0.233|0.213|0.205|
|X-n172-k51|0.495|0.401|0.465|0.395|0.438|0.364|**0.345**|
|X-n176-k26|0.412|0.327|0.363|0.327|0.370|0.314|**0.288**|
|X-n181-k23|0.088|0.081|0.074|0.069|0.170|0.170|**0.066**|
|X-n186-k15|0.212|**0.154**|0.220|0.220|0.211|0.187|0.185|
|X-n190-k8|0.177|0.169|0.177|0.176|0.153|**0.148**|0.181|
|X-n195-k51|0.443|0.309|0.292|0.292|0.367|**0.268**|0.318|
|X-n200-k36|0.190|0.135|0.188|0.149|0.168|0.127|**0.103**|
|X-n204-k19|0.232|0.201|0.229|0.199|0.201|**0.189**|0.199|
|X-n209-k16|0.150|0.127|0.198|0.155|0.164|0.140|**0.126**|
|X-n214-k11|0.327|0.270|0.293|0.290|0.331|0.291|**0.239**|
|X-n219-k73|0.022|0.018|0.018|0.018|0.471|0.467|**0.015**|
|X-n223-k34|0.300|0.289|0.265|0.265|0.166|**0.113**|0.135|
|X-n228-k23|0.383|0.366|0.368|0.335|0.296|**0.244**|0.270|
|X-n233-k16|0.461|0.461|0.519|0.420|0.630|0.441|**0.375**|
|X-n237-k14|0.185|0.185|0.223|0.198|0.194|**0.166**|0.190|
|X-n242-k48|0.174|0.129|0.145|0.145|0.114|**0.081**|0.092|
|X-n247-k50|0.374|0.355|0.378|0.376|0.362|0.327|**0.311**|
|X-n251-k28|**0.090**|**0.090**|0.115|0.098|0.150|0.100|0.102|
|X-n256-k16|0.219|0.202|0.202|0.184|0.184|0.162|**0.148**|
|X-n261-k13|0.405|0.345|0.348|0.348|0.336|0.324|**0.278**|
|X-n266-k58|0.090|**0.064**|0.089|0.078|0.111|0.076|0.081|
|X-n270-k35|0.147|0.147|0.203|0.203|0.231|**0.127**|0.132|
|X-n275-k28|0.134|0.132|0.140|0.135|0.210|0.196|**0.113**|
|X-n280-k17|0.373|0.263|0.257|0.257|0.220|**0.205**|0.273|
|X-n284-k15|0.249|0.227|0.279|**0.209**|0.242|0.227|0.228|
|X-n289-k60|0.228|0.219|0.219|0.219|0.261|0.216|**0.112**|
|X-n294-k50|0.438|0.376|0.500|0.427|0.364|0.344|**0.242**|
|X-n298-k31|0.298|0.298|0.377|0.294|0.204|**0.175**|0.211|
|Average|0.275|0.239|0.270|0.237|0.270|0.224|**0.196**|



