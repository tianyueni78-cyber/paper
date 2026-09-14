**Monte Carlo Tree Search for Comprehensive Exploration in LLM-Based Automatic Heuristic Design** 

**Zhi Zheng**<sup>1</sup> **Zhuoliang Xie**<sup>2</sup> **Zhenkun Wang**<sup>2</sup> **Bryan Hooi**<sup>1</sup> 

# **Abstract** 

Handcrafting heuristics for solving complex optimization tasks (e.g., route planning and task allocation) is a common practice but requires extensive domain knowledge. Recently, Large Language Model (LLM)-based automatic heuristic design (AHD) methods have shown promise in generating high-quality heuristics without manual interventions. Existing LLM-based AHD methods employ a population to maintain a fixed number of top-performing LLM-generated heuristics and introduce evolutionary computation (EC) to iteratively enhance the population. However, these population-based procedures cannot fully develop the potential of each heuristic and are prone to converge into local optima. To more comprehensively explore the space of heuristics, this paper proposes to use Monte Carlo Tree Search (MCTS) for LLM-based heuristic evolution. The proposed MCTS-AHD method organizes all LLMgenerated heuristics in a tree structure and can better develop the potential of temporarily underperforming heuristics. In experiments, MCTS-AHD delivers significantly higher-quality heuristics on various complex tasks. Our code is available<sup>3</sup> . 



<!-- Start of picture text -->
Heuristic functions in the original  √ √ Heuristic functions preserved<br>elite population in the updated elite population<br>LLM(       )-based heuristic evolutionNewly generated heuristic functions  √ ❌ ❌ Discarded heuristic functions<br>√<br>Population √<br>√<br>√<br>Update<br>❌ ❌<br>❌ ❌<br>❌<br> Feature of heuristic functions  Feature of heuristic functions<br>(a) Populations in LLM-based AHD<br>k Tree node of heuristic function on MCTS depth k 5 Better-performing tree nodes of heuristics outside local optima 5 5<br>Exsiting MCTS Edges New MCTS expansions<br>3 3<br>4<br>3 Iterations of 3<br>2 2 2 2 4<br>Tree Search<br>3 3 3 3<br>1 2 1 2 4<br>4 4<br> Feature of heuristic functions  Feature of heuristic functions<br>(b) MCTS for higher-quality LLM-based AHD (Ours)<br>Performance Performance<br>Performance Performance<br><!-- End of picture text -->

_Figure 1._ The generally adopted population (a) in existing LLMbased AHD methods (Liu et al., 2024b; Ye et al., 2024a) directly discards low-performance heuristics (under the red dashed line in (a)), thus falling into local optima. MCTS provides chances to develop low-performance heuristics, so it can more comprehensively explore the space of heuristic functions with different features. 

# **1. Introduction** 

Manually designed heuristics are promising in addressing complex optimization tasks (e.g., combinatorial optimization (CO) problems) (Desale et al., 2015). They are widely used in real-world applications, such as traffic control (He et al., 2011), job scheduling (Rajendran, 1993), and robotics (Tan et al., 2021). However, manually crafted heuristics often contain intricate workflows and parameter settings, making their design labor-intensive and reliant on task-specific expert knowledge. To achieve easier heuristic design across 

1School of Computing, National University of Singapore, Singapore<sup>2</sup> School of System Design and Intelligent Manufacturing, Southern University of Science and Technology, Shenzhen, China. Correspondence to: Bryan Hooi _<_ bhooi@comp.nus.edu.sg _>_ . 

> 3Our code is available at https://github.com/ zz1358m/MCTS-AHD-master/tree/main. 

various tasks, the concept of Automatic Heuristic Design (AHD) (Burke et al., 2013) (also known as Hyper-Heuristics (Ye et al., 2024a)) has attracted extensive attention. It seeks the best-performing heuristic algorithm among valid options. Genetic Programming (GP) (Langdon & Poli, 2013) is commonly employed for AHD, with GP-based AHD methods introducing a series of mutation operators to gradually refine heuristic algorithms (Duflo et al., 2019). Nevertheless, the effectiveness of GP-based methods still relies on human definitions of permissible operators (Liu et al., 2024b), which poses additional implementation difficulties. 

In recent years, large language models (LLMs) have shown exceptional effectiveness in various domains (Hadi et al., 2023; 2024; Naveed et al., 2023). Leveraging LLMs to automatically enhance heuristics, LLM-based AHD methods (Liu et al., 2024c; Yu & Liu, 2024) can design high-quality 

1 

**Monte Carlo Tree Search for Comprehensive Exploration in LLM-Based Automatic Heuristic Design** 

heuristics for various complex tasks without manual interventions. EoH (Liu et al., 2023; 2024b) and Funsearch (Romera-Paredes et al., 2024) innovatively apply LLMs to AHD by designing a population-based evolutionary computation (EC) procedure. For a given task, several established general frameworks may exist for implementing heuristics, e.g., greedy solving frameworks or frameworks with searchbased ideas for CO problems. LLM-based AHD methods focus on designing key heuristic functions within one of these predefined general frameworks, rather than developing heuristics from scratch. These methods maintain a population of outstanding heuristic functions based on their performances on an evaluation dataset and iteratively prompt LLMs to generate new heuristic functions taking the existing ones as starting points. Building on this population-based EC framework, studies also introduce effective components. EoH develops several prompt strategies that guide LLMs in generating effective heuristics. ReEvo (Ye et al., 2024a) incorporates the reflection mechanism (Shinn et al., 2024) to enhance the reasoning of LLMs among heuristic function samples. HSEvo (Dat et al., 2024) presents diversity metrics and harmony search (Shi et al., 2013) to increase the diversity of the population without compromising effectiveness. 

These population-based methods eliminate inferior heuristic functions in order to focus more on top-performance ones. However, lower-performance heuristic functions still have the potential to be outstanding after steps of LLM-based refinement. Thus, as shown in Figure 1, the population structure may guide the evolution of heuristics getting stuck in suboptimal local optima. Funsearch and HSEvo employ multiple-population structures (Cantu-Paz et al.´ , 1998) and diversity metrics, respectively, to improve the diversity of populations. Populations with these components can reduce the probability of premature convergence but still fail to explore the complex space of heuristics. 

To address these drawbacks, this paper proposes MCTSAHD, the first tree search method for LLM-based AHD, which employs a tree structure over all the heuristic functions generated so far and uses the Monte Carlo Tree Search (MCTS) algorithm with progressive widening technique (Coulom, 2007) to guide the evolution of further heuristics. Its advantages are: **1)** Instead of directly discarding inferior heuristic functions, MCTS-AHD enables steps of LLMbased evolution on temporarily underperforming heuristic functions while keeping focus on better-performing ones, achieving a more comprehensive exploration of the heuristic space. **2)** The tree structure in MCTS can benefit the LLMbased heuristic refinement, where MCTS-AHD presents a novel tree-special prompt strategy to inspire LLMs with the organized function samples in the MCTS tree paths. Moreover, as components, MCTS-AHD proposes an explorationdecay technique, which linearly decreases the rate at which we perform branching in MCTS as the algorithm progresses. 

We also present a novel thought-alignment procedure to generate precise linguistic descriptions of functions. In experiments, we implement MCTS-AHD to design heuristics with several general frameworks for a wide range of NPhard (Ausiello et al., 2012) CO problems and a Bayesian Optimization (BO)-related optimization task. MCTS-AHD achieves significantly higher-quality heuristics than handcrafted heuristics and existing LLM-based AHD methods. 

# **2. Preliminary** 

## **2.1. Definition: AHD & LLM-based AHD** 

**AHD:** For a given task _P_ (e.g., a CO problem), AHD methods search for the best-performing heuristic _h_<sup>_∗_</sup> within a heuristic space _H_ as follows: 



The heuristic space _H_ contains all feasible heuristics for tasks _P_ . Given a task _P_ , _heuristic h ∈ H_ is an algorithm mapping the set of task inputs (also called instances) _IP_ into the corresponding set of solutions _SP_ , i.e., _h_ : _IP → SP_ . For example, heuristics for an NP-hard CO task, Traveling Salesman Problem (TSP), map city coordinates (TSP instances) to travel tours (solutions). The function _g_ ( _·_ ) is a performance measure function for heuristics, _g_ : _H →_ R. For a CO task _P_ minimizing an objective function _f_ : _SP →_ R, AHD methods estimate the performance function _g_ by evaluating the heuristic _h_ on a task-specific dataset _D_ . Formally, we enumerate instances **_ins_** _∈ D ⊆ IP_ , obtain their solutions _h_ ( **_ins_** ) by _h_ , and calculate the expectation of the objective function values for the solutions as follows: 



The heuristics in _H_ belong to a wide range of general frameworks, and the optimal heuristic could be implemented with multiple frameworks. To focus more on critical heuristic designs within each framework, AHD methods typically predefine a general framework and design only a **key heuristic function** with specified inputs and outputs within this framework. For example, heuristics for TSP within a step-by-step construction framework sequentially build TSP tours one city after another. AHD methods within this framework for TSP will design a key heuristic function to select the next city based on the partial tour of previously visited cities. For simplicity, we still denote the function to be designed as _h_ . 

**LLM-based AHD:** LLM-based AHD introduces LLMs into the search process for the optimal heuristic function _h_<sup>_∗_</sup> (within a predefined framework). Existing LLM-based AHD methods (Liu et al., 2024b; Ye et al., 2024a) maintain a population of _M_ heuristic functions _{h_ 1 _, . . . , hM }_ and employ EC to update the population iteratively. Imitating mutation or crossover operators in EC, LLM-based 

2 

**Monte Carlo Tree Search for Comprehensive Exploration in LLM-Based Automatic Heuristic Design** 



<!-- Start of picture text -->
Action: i1 Action: m1 Action: m2<br>Initialization : Generate a heuristic function for  Mutation : Modify the given heuristic function  Mutation : Modify the given heuristic function<br>with its description (    ), e.g., add new  with its description (    ), e.g., change parameter<br>Task P & general framework mechanisms or code segments. settings.<br>Prompt Prompt Prompt<br>Function Description Function Description Function Description<br>New MCTS node New MCTS node New MCTS node<br>Action: e1 Action: e2 Action: s1<br>Crossover : Given several functions with their  Crossover : Based on a function with its  Reasoning : Given several related functions with<br>descriptions and performances(      ), generate a  description and performance (    ), learn from  their descriptions and performances, reason and<br>totally different one. another one (    ) and generate a new function. generate a new function with better performance.<br>��<br>Prompt Function Description Sample Prompt Function Description Prompt Function Description<br>... ��<br>�(·)�(·)�(·) New MCTS node Elite set � �(·) New MCTS node �(·)�(·)�(·)�(·)�(·) New MCTS node<br><!-- End of picture text -->

_Figure 2._ LLM-based actions in MCTS-AHD for heuristic evolution. Actions include initializing a new heuristic (i1); two mutation actions (m1 and m2) to mutate an existing heuristic function into a new one with diverse mechanism or detail settings; two crossover actions (e1 and e2) to generate a new heuristic from multiple existing ones; and a novel tree-path reasoning action (s1) to get a better heuristic function from organized function samples on an MCTS tree path from the root node _nr_ to a leaf node _nl_ . 

AHD methods prompt LLMs to generate heuristics given existing heuristics from the population. In these methods, a heuristic _h_ will only be retained for the next iteration if its performance _g_ ( _h_ ) estimated in the evaluation dataset _D_ exceeds the worst-performing heuristic in the original population, i.e., _g_ ( _h_ ) _>_ min _i∈{_ 1 _,...,M } g_ ( _hi_ ). This property makes it difficult for population-based methods to adopt a worse-before-better strategy for the optimal heuristic _h_<sup>_∗_</sup> . 

## **2.2. Monte Carlo Tree Search** 

**MCTS Algorithm.** MCTS (Swiechowski et al.<sup>´</sup> , 2023) is a decision-making algorithm widely used in games (Silver et al., 2016) and complex decision-making tasks (Fu et al., 2021). Recent studies also verify the power of MCTS in assisting LLMs to conduct multi-hop reasoning (Feng et al., 2023). In the MCTS tree, each node _nc_ represents a state, and the MCTS will repeatedly select and expand the node with the highest potential judged by a UCT algorithm (Kocsis & Szepesvari´ , 2006). Each MCTS tree node _nc_ records a quality value _Q_ ( _nc_ ) and a visit count _N_ ( _nc_ ) representing the number of times the node has been selected. From an initial root node _nr_ , MCTS gradually builds the MCTS tree to explore the entire state space. Each round of MCTS consists of four stages as follows: 

_Selection_ : The selection stage identifies the most potential MCTS tree node for subsequent node expansions. From the root node _nr_ , the selection stage iteratively selects the child node with the largest UCT value until it reaches a leaf node. Given a current node _nc_ , the UCT values for its child nodes 



_Expansion_ : The expansion stage obtains multiple child nodes from the current (leaf) node _nc_ by sampling several actions from the state of _nc_ among all possible options. 

_Simulation_ : The simulation stage evaluates all newly expanded leaf nodes for their quality value _Q_ ( _·_ ). 

_Backpropagation_ : The backpropagation process uses the results of simulations to update the values of _Q_ ( _·_ ) _, N_ ( _·_ ) for nodes on the tree path from _nc_ to the root _nr_ . 

After several iterations of MCTS, the MCTS tree can contain nodes with high-quality states for games or tasks. 

**Progressive Widening.** Conventional MCTS is not suitable for tasks with extensive action options or dynamically changing environments (Lee et al., 2020b). Progressive widening (Coulom, 2007) is a technique designed for MCTS to fit such tasks. It gradually adds new child nodes to non-leaf nodes as their visit counts _N_ ( _·_ ) increases. Formally, for node _nc_ with child nodes children( _nc_ ), a new child node will be added every time the following condition is satisfied: 



where _|_ children( _nc_ ) _|_ is the number of child nodes of _nc_ . 

# **3. MCTS-AHD** 

To address the challenges faced by population-based LLMbased AHD methods in overcoming local optima and explor- 

3 

**Monte Carlo Tree Search for Comprehensive Exploration in LLM-Based Automatic Heuristic Design** 



<!-- Start of picture text -->
Repeated until evaluating g(       ) for T times<br>Selection Expansion Simulation Backpropagation<br>MCT Root �(·)�(·) MCT Root MCT Root MCT Root �(·)<br>A virtual node �(·)<br>Initialnodes �(·)�(·) �(·)�(·) �(·)�(·) �(·)�(·) Initialnodes e1 Initialnodes e1 Initialnodes �(·) �(·) e1<br>Potential  e2 e2 �(·) = 1�(·) = g(      ) e2<br>�(·)�(·) �(·)�(·) �(·)�(·) Progressive  �(·) �(·)<br>Widening e2 m1 m2 s1 e2 m1 m2 s1 �(·) = 1�(·) = g(      ) e2 m1 m2 s1<br>To a child node with the largest UCT(·) �(·) = 1<br>�(·) = 1 �(·) = g(      )<br>�(·) = g(      ) �(·) = 1 �(·) = 1<br>�(·) = g(      ) �(·) = g(      )<br><!-- End of picture text -->

_Figure 3._ The MCTS process in MCTS-AHD contains four stages, i.e., _selection_ , _expansion_ , _simulation_ , and _backpropagation_ . MCTSAHD simulates the quality value of each node as the performance function values of their heuristics and the MCTS will terminate after total _T_ performance evaluations. MCTS-AHD introduces the progressive widening technique to better crossover original heuristic functions with continuously generated new ones. It conducts the crossover actions e1 for the root node and action e2 for other nodes. 

ing complex heuristic spaces, this paper proposes a novel method called MCTS-AHD. It preserves all heuristic functions LLMs generated so far in an MCTS tree and employs MCTS with progressive widening for heuristic evolution. The MCTS root node _nr_ is a virtual node without representing any heuristics, and each of the other nodes represents an executable Python implementation of a heuristic function _h ∈ H_ along with its linguistic description. As LLM-based actions for MCTS node expansion, MCTS-AHD prompts LLMs in existing strategies (e.g., mutation, crossover) and a novel tree-path reasoning strategy. Moreover, to encourage the exploration of the heuristic space _H_ in the early stages of MCTS and ensure convergence in the later stages, MCTSAHD presents an exploration-decay technique that linearly reduces the exploration factor in UCT. 

## **3.1. LLM-based actions in MCTS-AHD** 

To simulate the mutation or crossover operators in EC, LLMbased AHD methods prompt LLMs with several prompt strategies to generate new heuristic functions from existing ones (Liu et al., 2024b). Utilizing the advantage that the MCTS tree can record the relationships of all the generated heuristics, as shown in Figure 2, MCTS-AHD presents a novel MCTS-specific set of actions for LLM-based heuristic evolution, including action i1, e1, e2, m1, m2, and s1. The detailed prompts for these actions are in Appendix E.1. As a commonality, all prompts contain descriptions of the task _P_ , the predefined general framework, and the inputs and outputs of the key heuristic function along with their meanings. For actions except i1, prompts also contain implementations and descriptions of existing heuristic functions. For each action, LLMs are supposed to output the Python code of a heuristic function and its linguistic description. 

_Initial Action i1_ : As an action for initialization, the action i1 aims to directly generate a heuristic function and its corresponding description from scratch by LLMs. 

_Mutation Action m1 & m2_ : MCTS-AHD incorporates two mutation actions, m1 & m2, to attempt more detailed designs within the original function workflow. Based on the inputted heuristic function, action m1 prompts LLMs to introduce new mechanisms and formulas, and action m2 prompts LLMs to modify the parameter settin <mark>gs.</mark> 

_Crossover Action e1_ : To explore heuristic functions with new workflows, we employ a crossover action e1 to generate a new heuristic function that diverges from multiple existing ones. These existing heuristic functions are inputted to LLMs with their performances _g_ ( _·_ ) and descriptions. 

_Crossover Action e2_ : The crossover action e2 prompts LLMs with a parent heuristic function, a reference heuristic function, and their respective performances. LLMs are supposed to identify the beneficial traits and settings in the reference one and craft an improved heuristic function based on the parent one. The reference is sampled from a dynamically maintained **elite heuristic function set** _E_ consisting of heuristic functions with top 10 performances _g_ ( _·_ ). 

_Tree-path Reasoning Action s1_ : The MCTS tree paths from the root _nr_ to leaf nodes record the evolution history of heuristic functions. So, utilizing this feature, MCTS-AHD presents a novel action s1 to analyze all unique heuristic functions from the leaf node to be developed _nl_ up to the root _nr_ , identify advantageous designs in these heuristics, and generate an enhanced heuristic function. 

**Generating Descriptions: The Thought-Alignment Process** . Linguistic descriptions of heuristic functions can assist the reasoning of LLMs (Liu et al., 2024b), where EoH prompts LLMs for a description before outputting the function code. However, due to LLM hallucination (Huang et al., 2023), such a procedure could lead to uncorrelated codes and descriptions. For correlated and detailed descriptions, MCTS-AHD proposes a thought-alignment process that summarizes descriptions after the code generations. There- 

4 

**Monte Carlo Tree Search for Comprehensive Exploration in LLM-Based Automatic Heuristic Design** 

fore, performing all the MCTS-AHD actions calls LLMs twice. In the first call, we adopt the LLM-generated Python implementation of a heuristic function with action prompts. Then, we conduct a thought-alignment process, prompting LLMs to generate linguistic code descriptions in up to three sentences (refer to Appendix E.2 for prompts). The second LLM call is significantly shorter than the first one, so it will not cause a severe increase in execution time and token cost. 

## **3.2. MCTS settings** 

Figure 3 displays the MCTS process in MCTS-AHD. It first generates _NI_ initial nodes representing and links them to a virtual root node _nr_ that does not represent any heuristics. Subsequently, similar to the regular MCTS introduced in Section2.2, MCTS-AHD repeatedly performs the selection, expansion, simulation, and backpropagation stages as follows until the number of evaluations of heuristics approaches a limit _T_ : 

_Selection:_ In the selection process of MCTS-AHD, MCTSAHD normalizes the quality value _Q_ ( _·_ ) to enhance the homogeneity of different tasks in calculating UCT value for child nodes _c ∈_ Children( _nc_ ) of a node _nc_ as follows: 



where _qmax_ and _qmin_ are the upper and lower limits of quality values _Q_ ( _·_ ) that ever encountered in MCTS, respectively. From the root _nr_ , MCTS iteratively selects a child node with the largest UCT value until reaching a leaf node. 

_Expansion_ : For the leaf node selected in the selection stage, the expansion stage prompts LLMs with actions e2, m1, m2, and s1 to build its child nodes. To attempt various detail designs, in a single expansion stage, MCTS-AHD generates _k_ child nodes with the actions m1 and m2, one with e2 and s1, respectively (2 _k_ + 2 child nodes in total). 

_Simulation_ : Then, MCTS-AHD evaluates these newly generated heuristic functions _h_ on the evaluation dataset _D_ for their performances _g_ ( _h_ ) and directly sets their quality value as their performances, i.e., _Q_ ( _nl_ ) _← g_ ( _h_ ). We also record their visit count _N_ ( _nl_ ) _←_ 1. Simultaneously, the elite set _E_ for the action e2, _qmax_ , and _qmin_ will be updated. 

_Backpropagation_ : The backpropagation process updates the quality values and the visit counts in MCTS as follows: 



**Progressive Widening** . Since the elite heuristic function set _E_ for the action e2 updates gradually as the search progresses. MCTS-AHD introduces the progressive widening 

technique to enable the re-exploration of non-leaf nodes, especially nodes with higher visit counts. The progressive widening process will occur when the condition in Eq.(4) is satisfied and we have _α_ = 0 _._ 5 for MCTS-AHD. We call the **action e1** for a new child node when the root node _nr_ qualifies the condition in Eq.(4), and we call **action e2** when other nodes qualify. Heuristic functions inputted to the action e1 are uniformly selected from 2 to 5 different subtrees of MCTS. We implement the progressive widening process during the selection stage, then these nodes will also be processed in the simulation and backpropagation stages. 

Eventually, MCTS-AHD will output a heuristic function with the highest performance value throughout the MCTS. 

## **3.3. Exploration-Decay** 

The setting of the exploration factor _λ_ in Eq.(5) determines the preferences of MCTS on exploration or exploitation (Browne et al., 2012). A larger _λ_ promotes the exploration of temporarily inferior nodes, while a smaller _λ_ stimulates concentration on nodes with higher quality values _Q_ ( _·_ ). To facilitate a more comprehensive exploration in the early iterations of MCTS and ensure convergence in the later ones, MCTS-AHD presents an exploration-decay technique, linearly decaying the exploration factor _λ_ in Eq.(5) as follows: 



Although having a task-specific setting _λ_ 0 is helpful for high-quality heuristics, MCTS-AHD strives to keep the generalization ability, so we set _λ_ 0 = 0 _._ 1 for all tasks. 

# **4. Experiments** 

This section evaluates the proposed MCTS on complex tasks, including NP-hard CO problems and a Cost-aware Acquisition Function (CAF) design task for BO (Yao et al., 2024c). The definitions of these tasks are in Appendix B. We implement MCTS-AHD to design key functions of a wide range of general frameworks (detailed in Appendix C) for these tasks, including step-by-step construction, Ant Colony Optimization (ACO), Guided Local Search (GLS), and BO. 

**Settings.** For experiments in this section, we set the number of initial tree nodes _NI_ = 4, _λ_ 0 = 0 _._ 1, _α_ = 0 _._ 5. The running time of each heuristic on the evaluation dataset _D_ is limited to 60 seconds. The composition of evaluation datasets _D_ for each task is detailed in Appendix D as well as the settings of general frameworks. Valuable LLM-based AHD methods should be flexible for various pre-trained LLMs, so we include both _GPT-3.5-turbo_ and _GPT-4o-mini_ . 

**Baselines.** To verify the ability of heuristics designed by MCTS-AHD, we introduce four types of heuristics as baselines: **(a)** Manually designed heuristics, e.g., Nearest-greedy 

5 

**Monte Carlo Tree Search for Comprehensive Exploration in LLM-Based Automatic Heuristic Design** 

_Table 1._ Designing heuristics with the step-by-step construction framework for TSP and KP. We evaluate methods on 6 test sets with 1,000 instances each. Test sets with in-domain scales (i.i.d. to the evaluation dataset _D_ ) are underlined. Since AHD methods have no guarantees for generalization ability, the effect on in-domain datasets is more important. Optimal for TSP is obtained by LKH (Lin & Kernighan, 1973), and Optimal for KP is the result of OR-Tools. Each LLM-based AHD method is run three times and we report the average performances. The best-performing method with each LLM is shaded, and each test set’s overall best result is in bold. 

|Task||||TSP|||||K|P|||
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|N=|_N_|=50|_N_=|100|_N_=|200|_N_=50,|_W_=12.5|_N_=100,|_W_=25|_N_=200|,_W_=25|
|Methods|Obj.↓|Gap|Obj.↓|Gap|Obj.↓|Gap|Obj.↑|Gap|Obj.↑|Gap|Obj.↑|Gap|
|Optimal|5.675|-|7.768|-|10.659|-|20.037|-|40.271|-|57.448|-|
|Greedy Construct|6.959|22.62%|9.706|24.94%|13.461|26.29%|19.985|0.26%|40.225|0.12%|57.395|0.09%|
|POMO|**5.697**|**0.39%**|**8.001**|**3.01%**|12.897|20.45%|19.612|2.12%|39.676|1.48%|57.271|0.09%|
|||||LLM|-based AH|D:_GPT-3.5-t_|_urbo_||||||
|Funsearch|6.683|17.75%|9.240|18.95%|12.808|19.61%|19.985|0.26%|40.225|0.12%|57.395|0.09%|
|EoH|6.390|12.59%|8.930|14.96%|12.538|17.63%|19.994|0.21%|40.231|0.10%|57.400|0.08%|
|MCTS-AHD(Ours)|6.346|11.82%|8.861|14.08%|12.418|16.51%|19.997|0.20%|40.233|0.09%|57.393|0.10%|
|||||LL|M-based AH|D:_GPT-4o-_|_mini_||||||
|Funsearch|6.357|12.00%|8.850|13.93%|12.372|15.54%|19.988|0.24%|40.227|0.11%|57.398|0.09%|
|EoH|6.394|12.67%|8.894|14.49%|12.437|16.68%|19.993|0.22%|40.231|0.10%|57.399|0.09%|
|MCTS-AHD(Ours)|6.225|9.69%|8.684|11.79%|**12.120**|**13.71%**|**20.015**|**0.11%**|**40.252**|**0.05%**|**57.423**|**0.04%**|



(Rosenkrantz et al., 1977), ACO (Dorigo et al., 2006), EI (Mockus, 1974). **(b)** Traditional AHD method: GHPP (Duflo et al., 2019) **(c)** Neural Combinatorial Optimization (NCO) methods under the same general frameworks, e.g. POMO (Kwon et al., 2020) and DeepACO (Ye et al., 2024b). **(d)** Existing LMM-based AHD methods: Funsearch (Romera-Paredes et al., 2024), EoH (Liu et al., 2024b), ReEvo (Ye et al., 2024a), and the most recent work HSEvo (Dat et al., 2024). Funsearch, ReEvo, and HSEvo design heuristics from a handcrafted low-quality seed function, and we provide the same seed function for each design scenario without providing external knowledge. Instead, running EoH and MCTS-AHD does not require manually setting a seed function to initiate the heuristic evolution, so both methods demonstrate better applicability. 

We design heuristics with the proposed MCTS-AHD and LLM-based AHD baselines on a single Intel(R) i7-12700 CPU. Following similar settings of Liu et al. (2024b), for almost all tasks, we set the evaluation budget of LLM-based AHD methods on the evaluation dataset _D_ as _T_ = 1 _,_ 000. In designing heuristics for each application scenario, we conduct three independent runs for each LLM-based AHD method to reduce statistical biases. To verify the significant advantages of MCTS-AHD, we perform more runs on some tasks in Appendix F.3 to obtain the p-value. In designing heuristics with the step-by-step construction framework for the 0-1 Knapsack Problem (KP), executing MCTS-AHD with _T_ =1,000 takes approximately three hours, 1M input tokens, 0.2M output tokens, about 0.3$ with _GPT-4o-mini_ . Compared to LLM-based AHD baselines, there is no significant efficiency degradation or cost improvement. 

## **4.1. MCTS-AHD for NP-hard CO Problems** 

As commonly recognized complex tasks (Korte et al., 2011), this subsection evaluates MCTS-AHD on NP-hard CO prob- 

lems, including TSP, KP, Capacitated Vehicle Routing Problem (CVRP), Multiple Knapsack Problem (MKP), BinPacking Problem (BPP) with both online and offline settings (online BPP & offline BPP), and Admissible Set Problem (ASP). For these NP-hard CO problems, we apply MCTSAHD to automatically design heuristics with several general frameworks, including step-by-step construction, ACO, and GLS (GLS results are shown in Appendix F.2). 

**Step-by-Step Construction Framework.** The step-by-step construction framework (also known as the constructive heuristic framework) is simple but flexible for task solving, which constructs nodes in feasible CO solutions one by one (Asani et al., 2023). Besides being a general framework for LLM-based AHD methods, it is also the most common framework adopted in NCO methods (Vinyals et al., 2015; Bello et al., 2016). We use MCTS-AHD to design heuristics with the step-by-step construction framework for TSP, KP, online BPP, and ASP (with ASP results in Appendix F.1). 

_TSP & KP_ . We first evaluate MCTS-AHD by designing TSP and KP heuristics within step-by-step construction frameworks. The key heuristic function to be designed should select the next TSP node or the next KP item to join taking the temporary solving state (e.g., selected and remaining TSP nodes or KP items) as inputs. This function will be executed recursively until a complete feasible solution is constructed. For all LLM-based AHD methods, the evaluation dataset _D_ contains 64 50-node ( _N_ =50) TSP instances for TSP and 64 100-item ( _N_ =100) KP instances with capacity _W_ = 25 for KP. Table 1 shows the performance of baseline heuristics and LLM-based AHD methods. The Greedy Construct baseline is the Nearest-greedy heuristic algorithm for TSP and it constructs KP solutions by the item with the largest value-weight-ratio. MCTS-AHD exhibits significant advantages on almost all test sets, surpassing manually designed heuristics and LLM-based AHD methods EoH and Fun- 

6 

**Monte Carlo Tree Search for Comprehensive Exploration in LLM-Based Automatic Heuristic Design** 

_Table 2._ Designing heuristics with the ACO general framework for solving TSP, CVRP, MKP, and offline BPP. Each test set contains 64 instances and LLM-based AHD methods’ performances are averaged over three runs. 

|||T|SP|||CV|RP|||M|KP|||Offli|lne BPP||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Test sets|_N_=|50|_N_=|100|_N_=50|,_C_=50|_N_=100|,_C_=50|_N_=100|,_m_=5|_N_=200|,_m_=5|_N_=500,|_C_=150|_N_=1,000|,_C_=150|
|Methods|Obj.↓|Gap|Obj.↓|Gap|Obj.↓|Gap|Obj.↓|Gap|Obj.↑|Gap|Obj.↑|Gap|Obj.↓|Gap|Obj.↓|Gap|
|ACO|5.992|3.28%|8.948|9.40%|11.355|27.77%|18.778|25.76%|22.738|2.28%|40.672|4.30%|208.828|2.81%|417.938|3.15%|
|DeepACO|5.842|0.71%|8.282|1.26%|**8.888**|**0.00% **|**14.932 **|**0.00%**|23.093|0.75%|41.988|1.20%|**203.125 **|**0.00% **|**405.172**|**0.00%**|
|||||||LLM-b|ased AH|D:_GPT_|_-4o-mini_||||||||
|EoH|5.828|0.45%|8.263|1.03%|9.359|5.31%|15.681|5.02%|23.139|0.56%|41.994|1.19%|204.646|0.75%|408.599|0.85%|
|ReEvo|5.856|0.94%|8.340|1.98%|9.327|4.94%|16.092|7.77%|23.245|0.10%|42.416|0.19%|206.693|1.76%|413.510|2.06%|
|MCTS-AHD(Ours)|**5.801**<br>|**0.00%**|**8.179**|**0.00%**|9.286|4.48%|15.782|5.70%|**23.269**|**0.00%**|**42.498**|**0.00%**|204.094|0.48%|407.323|0.53%|



search. Moreover, compared to an advanced NCO method POMO which requires task-specific training, MCTS-AHD can design better heuristics in 200-node TSP and KP test sets, exhibiting its power to solve NP-hard CO problems. 

_Online BPP_ . As another widely considered NP-hard CO problem, online BPP is the online variant of BPP. It allows only immediate bin packing decisions once a new item is received. It is generally adopted as a common evaluation scenario for LLM-based AHD methods. We follow (Liu et al., 2024b) to generate WeiBull BPP instances (Castineiras et al.˜ , 2012) and use four WeiBull instances with diverse scales as the evaluation dataset _D_ . As shown in Table 3, online BPP heuristics designed by MCTS-AHD demonstrate a superior average performance of six test sets. 

_Table 3._ Design step-by-step construction heuristics for solving online BPP. The table exhibits the performance gaps of heuristics to the lower bound. Each LLM-based AHD method is run three times for the average gaps. Each test set contains five WeiBull BPP instances and we underline the four (in-domain) scales contained in _D_ . The scale notations of test sets are abbreviated, e.g., 1k ~~1~~ 00 represents 1,000 items and capacity _W_ = 100. 

||||Online|BPP||||
|---|---|---|---|---|---|---|---|
|Test sets|1k<br>~~1~~00|1k<br>~~5~~00|5k<br>~~1~~00|5k<br>~~5~~00|10k<br>~~1~~00|10k<br>500|Avg.|
|Best Fit|4.77%|0.25%|4.31%|0.55%|4.05%|0.47%|2.40%|
|First Fit|5.02%|0.25%|4.65%|0.55%|4.36%|0.50%|2.56%|
||L|LM-bas|ed AHD:|_GPT-4o_|_-mini_|||
|Funsearch|2.45%|0.66%|1.30%|0.25%|1.05%|0.21%|0.99%|
|EoH|2.69%|0.25%|1.63%|0.53%|1.47%|0.45%|1.17%|
|ReEvo|3.94%|0.50%|2.72%|0.40%|2.39%|0.31%|1.71%|
|HSEvo|2.64%|1.07%|1.43%|0.32%|1.13%|0.21%|1.13%|
|MCTS-AHD|2.45%|0.50%|1.06%|0.32%|0.74%|0.26%|**0.89%**|



**Ant Colony Optimization Framework** . The ACO is an optimization algorithm inspired by the foraging behavior of ants, which contains a heuristic matrix and implements a path selection mechanism to solve combinatorial optimization problems by simulating the transfer of pheromones between ants (Dorigo et al., 2006; Kim et al., 2024). LLMbased AHD can design a generation function of the heuristic matrix, thereby transforming ACO into a framework and applying it to a variety of tasks. Following Ye et al. (2024a), MCTS-AHD designs heuristics within the ACO framework 

for four NP-hard CO problems: TSP, CVRP, MKP, and offline BPP. The design results using _GPT-4o-mini_ as LLMs are shown in Table 2, where MCTS-AHD exhibits significant leads to EoH and ReEvo in all in-domain test sets across four CO problems and three out-of-domain test sets. Moreover, the proposed MCTS-AHD can consistently outperform manually designed ACO heuristics in all eight test sets and surpass an outstanding NCO method DeepACO (Ye et al., 2024b) in TSP and MKP test sets. 

## **4.2. MCTS-AHD for Other Complex Tasks** 

To assess whether MCTS-AHD can still perform well in optimization tasks beyond CO problems, we follow Yao et al. (2024c) to evaluate MCTS-AHD by designing heuristic CAFs for BO. The CAF is a crucial component for Cost-aware BO, helping to reach the global optimum in a cost-efficient manner. There are several advanced handcrafted heuristic CAFs, including EI (Mockus, 1974), EIpu (Snoek et al., 2012), and EI-cools (Lee et al., 2020a). We employ two synthetic instances with different landscapes and input dimensions (Ackley and Rastrigin in Table 4) as the evaluation dataset _D_ for LLM-based AHD and also test the manually and automatically designed heuristics on ten other synthetic instances. During heuristic evolutions, we set the sampling budget to 12 and run 5 independent trials for average performances. As shown in Table 4, heuristic CAFs designed by the proposed MCTS-AHD demonstrate superior BO results that outperform both manually designed heuristics and EoH in six out of twelve synthetic instances. It verifies that MCTS-AHD not only performs well in NPhard CO problems but can also show great power in other complex optimization tasks. 

# **5. Discussion** 

Experiments have demonstrated the effectiveness of the proposed MCTS-AHD in designing high-quality heuristics for a wide range of application scenarios. This section first conducts essential ablation studies. Then, we will also analyze the advantages of utilizing MCTS in LLM-based AHD compared to the original population-based EC. 

7 

**Monte Carlo Tree Search for Comprehensive Exploration in LLM-Based Automatic Heuristic Design** 

_Table 4._ Designing CAFs for BO. The table shows the gaps to optimal when running BO on instances with manually designed CAFs and CAFs designed by LLM-based AHD methods. LLM-based AHD methods are run three times for the average gaps. In testing, the evaluation budgets for BO are 30 and we run 10 trials for average gaps. The results of EI, EIpu, and EI-cool are from Yao et al. <u>(2024c).</u> 

|Instances|Ackley|Rastrigin|Griewank|Rosenbrock|Levy|ThreeHumpCamel|StyblinskiTang|Hartmann|Powell|Shekel|Hartmann|Cosine8|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|EI|2.66%|4.74%|0.49%|**1.26%**|**0.01%**|0.05%|0.03%|0.00%|18.89%|7.91%|0.03%|0.47%|
|EIpu|2.33%|5.62%|0.34%|2.36%|0.01%|0.12%|**0.02%**|0.00%|19.83%|7.92%|0.03%|0.47%|
|EI-cool|2.74%|5.78%|**0.34%**|2.29%|0.01%|0.07%|0.03%|**0.00%**|14.95%|8.21%|**0.03%**|0.54%|
||||||LLM-|based AHD:_GPT-4_|_o-mini_||||||
|EoH|2.45%|0.90%|0.54%|56.78%|0.20%|0.26%|0.79%|0.04%|70.89%|4.56%|0.33%|0.36%|
|MCTS-AHD|**2.40%**|**0.77%**|0.36%|1.68%|0.01%|**0.02%**|0.20%|0.01%|**1.27%**|**3.94%**|0.38%|**0.34%**|



## **5.1. Ablation on Parameters and Components** 

To validate the necessity of its components, as shown in Table 5, we first remove three proposed components of MCTS-AHD (Progressive Widening, Thought-alignment, and Exploration-decay) and use these variants to design stepby-step heuristics for TSP and KP. Line 3 to Line 5 in Table 5 reports their average optimality gaps over three runs, and all these variants exhibit a clear performance degradation in at least one task compared to the original MCTS-AHD. 

The actions for node expansion in MCTS-AHD are also essential. Actions e1 and e2 are associated with the progressive widening, so they cannot be ablated individually. According to Table 5, MCTS-AHD variants without actions s1, m1, and m2 could only design worse heuristics in at least one task, proving the significance of these LLM-based actions. The importance of action s1 also demonstrates that MCTS-AHD benefits from its organized tree structure. 

Meanwhile, we measure the sensitivity of the main parameter _λ_ 0. Results in the last two lines of Table 5 show that although the TSP and KP tasks may have respective preferences in the _λ_ 0 setting, the default setting (i.e., _λ_ 0 = 0 _._ 1) exhibits generally good quality. 

_Table 5._ Ablations on the components, actions, and parameter settings of MCTS-AHD. We use MCTS-AHD variants to design heuristics with the step-by-step construction framework for their optimality <u>gaps on 1,000-instance test sets averaged over</u> **five runs** . 

|Methods|_TSP50_|_KP100_|
|---|---|---|
|MCTS-AHD(Original, 10 runs)|10.661%|0.059%|
|_w/o_Progressive Widening|12.132%|0.064%|
|_w/o_Thought-alignment|11.640%|0.061%|
|_w/o_Exploration-decay|11.606%|0.064%|
|_w/o_Action s1|11.919%|0.062%|
|_w/o_Action m1|10.921%|0.083%|
|_w/o_Action m2|11.679%|0.061%|
|MCTS-AHD variant_λ_0= 0.05|11.080%|0.056%|
|MCTS-AHD variant_λ_0= 0.2|12.124%|0.034%|



## **5.2. MCTS versus Population-based EC** 

**Ability of MCTS-AHD in Escaping from Local Optima** . As the main contribution of this paper, instead of populationbased EC, MCTS-AHD can manage inferior but potential 

heuristic functions, achieving a more comprehensive exploration of the heuristic space _H_ thus avoiding falling into local optima. To verify this, we plot the performance curves of MCTS-AHD and LLM-based AHD baselines in designing step-by-step construction heuristics for TSP and designing CAFs for BOs. Each curve is averaged over at least **five runs** . As illustrated in Figure 4, all baseline methods with populations exhibit early convergences on performances, but MCTS-AHD can converge to significantly better performance via quick and continuous performance updates. 



<!-- Start of picture text -->
Evolution Curves of LLM-based AHD Methods Evolution Curves of LLM-based AHD Methods<br>2<br>6.4<br>3<br>6.6<br>4<br>6.8 Funsearch 5<br>EoH<br>7.0 ReEvo 6<br>HSEvo EoH<br>7.2 MCTS-AHD (Ours) 7 MCTS-AHD (Ours)<br>200 400 600 800 1000 200 400 600 800 1000<br>Number of Evaluations on D Number of Evaluations on Ackley and Rastrigin<br>(a) Design Step-by-step Con- (b) Design CAFs for BO<br>struction heuristics for TSP<br>Performance of Heuristics on D<br>Performance on Ackley and Rastrigin<br><!-- End of picture text -->

_Figure 4._ Evolution curves on two diverse application scenarios. 

**Advantage scopes of MCTS-AHD** . Compared to population-based baselines, we claim that MCTS-AHD demonstrates greater advantages in application scenarios with more complex heuristic spaces _H_ and application scenarios with more descriptions as knowledge. We analyze these two claims with experiments in Appendix F.8. 

# **6. Conclusion** 

In conclusion, this paper first applies MCTS to LLM-based AHD. The proposed MCTS-AHD achieves a comprehensive exploration of the heuristic space and can finally design higher-quality heuristics for NP-hard complex tasks. For LLM-based AHD, MCTS can be a more promising evolution method compared to population-based EC. 

**Limitation and Future Work** : As a limitation of MCTSAHD, the convergence speed of MCTS-AHD can still be improved. In the future, we will consider designing MCTSpopulation hybrid methods for better evolution efficiency. 

8 

**Monte Carlo Tree Search for Comprehensive Exploration in LLM-Based Automatic Heuristic Design** 

# **Impact Statement** 

This paper presents work whose goal is to advance the field of Machine Learning. There are many potential societal consequences of our work, none which we feel must be specifically highlighted here. 

# **References** 

- Abgaryan, H., Harutyunyan, A., and Cazenave, T. Llms can schedule. _arXiv preprint arXiv:2408.06993_ , 2024. 

- Alhindi, A., Alhindi, A., Alhejali, A., Alsheddy, A., Tairan, N., and Alhakami, H. Moea/d-gls: a multiobjective memetic algorithm using decomposition and guided local search. _Soft Computing_ , 23:9605–9615, 2019. 

- Ansari, Z. N. and Daxini, S. D. A state-of-the-art review on meta-heuristics application in remanufacturing. _Archives of Computational Methods in Engineering_ , 29(1):427– 470, 2022. 

- Arnold, F. and Sorensen, K.¨ Knowledge-guided local search for the vehicle routing problem. _Computers & Operations Research_ , 105:32–46, 2019. 

- Arnold, F., Gendreau, M., and Sorensen,¨ K. Efficiently solving very large-scale routing problems. _Computers & operations research_ , 107:32–42, 2019. 

- Asani, E. O., Okeyinka, A. E., and Adebiyi, A. A. A computation investigation of the impact of convex hull subtour on the nearest neighbour heuristic. In _2023 International Conference on Science, Engineering and Business for Sustainable Development Goals (SEB-SDG)_ , volume 1, pp. 1–7. IEEE, 2023. 

- Ausiello, G., Crescenzi, P., Gambosi, G., Kann, V., Marchetti-Spaccamela, A., and Protasi, M. _Complexity and approximation: Combinatorial optimization problems and their approximability properties_ . Springer Science & Business Media, 2012. 

- Back, T., Fogel, D. B., and Michalewicz, Z.¨ Handbook of evolutionary computation. _Release_ , 97(1):B1, 1997. 

- Bello, I., Pham, H., Le, Q. V., Norouzi, M., and Bengio, S. Neural combinatorial optimization with reinforcement learning. _arXiv preprint arXiv:1611.09940_ , 2016. 

- Berto, F., Hua, C., Zepeda, N. G., Hottung, A., Wouda, N., Lan, L., Park, J., Tierney, K., and Park, J. Routefinder: Towards foundation models for vehicle routing problems. _arXiv preprint arXiv:2406.15007_ , 2024. 

- Biggs, N. The traveling salesman problem a guided tour of combinatorial optimization, 1986. 

- Blot, A., Hoos, H. H., Jourdan, L., Kessaci-Marmion, M.-E.,<sup>´</sup> and Trautmann, H. Mo-paramils: A multi-objective automatic algorithm configuration framework. In _Learning and Intelligent Optimization: 10th International Conference, LION 10, Ischia, Italy, May 29–June 1, 2016, Revised Selected Papers 10_ , pp. 32–47. Springer, 2016. 

- Brandfonbrener, D., Henniger, S., Raja, S., Prasad, T., Loughridge, C. R., Cassano, F., Hu, S. R., Yang, J., Byrd, W. E., Zinkov, R., et al. Vermcts: Synthesizing multistep programs using a verifier, a large language model, and tree search. In _The 4th Workshop on Mathematical Reasoning and AI at NeurIPS’24_ , 2024. 

- Brecklinghaus, J. and Hougardy, S. The approximation ratio of the greedy algorithm for the metric traveling salesman problem. _Operations Research Letters_ , 43(3):259–261, 2015. 

- Browne, C. B., Powley, E., Whitehouse, D., Lucas, S. M., Cowling, P. I., Rohlfshagen, P., Tavener, S., Perez, D., Samothrakis, S., and Colton, S. A survey of monte carlo tree search methods. _IEEE Transactions on Computational Intelligence and AI in games_ , 4(1):1–43, 2012. 

- Burke, E. K., Gendreau, M., Hyde, M., Kendall, G., Ochoa, G., Ozcan, E., and Qu, R.<sup>¨</sup> Hyper-heuristics: A survey of the state of the art. _Journal of the Operational Research Society_ , 64(12):1695–1724, 2013. 

- Burke, E. K., Hyde, M. R., Kendall, G., Ochoa, G., Ozcan,<sup>¨</sup> E., and Woodward, J. R. A classification of hyperheuristic approaches: revisited. _Handbook of metaheuristics_ , pp. 453–477, 2019. 

- Cantu-Paz, E. et al.´ A survey of parallel genetic algorithms. _Calculateurs paralleles, reseaux et systems repartis_ , 10 (2):141–171, 1998. 

- Castineiras, I., De Cauwer, M., and O’Sullivan, B.˜ Weibullbased benchmarks for bin packing. In _International Conference on Principles and Practice of Constraint Programming_ , pp. 207–222. Springer, 2012. 

- Christofides, N. Worst-case analysis of a new heuristic for the travelling salesman problem. In _Operations Research Forum_ , volume 3, pp. 20. Springer, 2022. 

- Coulom, R. Computing “elo ratings” of move patterns in the game of go. _ICGA journal_ , 30(4):198–208, 2007. 

- Dainese, N., Merler, M., Alakuijala, M., and Marttinen, P. Generating code world models with large language models guided by monte carlo tree search. _arXiv preprint arXiv:2405.15383_ , 2024. 

- Dat, P. V. T., Doan, L., and Binh, H. T. T. Hsevo: Elevating automatic heuristic design with diversity-driven harmony 

9 

**Monte Carlo Tree Search for Comprehensive Exploration in LLM-Based Automatic Heuristic Design** 

- search and genetic algorithm using llms. _arXiv preprint arXiv:2412.14995_ , 2024. 

- DeLorenzo, M., Chowdhury, A. B., Gohil, V., Thakur, S., Karri, R., Garg, S., and Rajendran, J. Make every move count: Llm-based high-quality rtl code generation using mcts. _arXiv preprint arXiv:2402.03289_ , 2024. 

- Desale, S., Rasool, A., Andhale, S., and Rane, P. Heuristic and meta-heuristic algorithms and their relevance to the real world: a survey. _Int. J. Comput. Eng. Res. Trends_ , 351(5):2349–7084, 2015. 

- Dorigo, M., Birattari, M., and Stutzle, T. Ant colony optimization. _IEEE computational intelligence magazine_ , 1 (4):28–39, 2006. 

- Drakulic, D., Michel, S., and Andreoli, J.-M. Goal: A generalist combinatorial optimization agent learning. _arXiv preprint arXiv:2406.15079_ , 2024. 

- Duflo, G., Kieffer, E., Brust, M. R., Danoy, G., and Bouvry, P. A gp hyper-heuristic approach for generating tsp heuristics. In _2019 IEEE International Parallel and Distributed Processing Symposium Workshops (IPDPSW)_ , pp. 521–529. IEEE, 2019. 

- Eiben, A. E. and Smith, J. E. _Introduction to evolutionary computing_ . Springer, 2015. 

- Feng, X., Wan, Z., Wen, M., McAleer, S. M., Wen, Y., Zhang, W., and Wang, J. Alphazero-like tree-search can guide large language model decoding and training. _arXiv preprint arXiv:2309.17179_ , 2023. 

- Fischetti, M., Lodi, A., and Toth, P. Exact methods for the asymmetric traveling salesman problem. _The traveling salesman problem and its variations_ , pp. 169–205, 2007. 

- Fu, Z.-H., Qiu, K.-B., and Zha, H. Generalize a small pre-trained model to arbitrarily large tsp instances. In _Proceedings of the AAAI conference on artificial intelligence_ , volume 35, pp. 7474–7482, 2021. 

- Gao, C., Shang, H., Xue, K., Li, D., and Qian, C. Towards generalizable neural solvers for vehicle routing problems via ensemble with transferrable local policy, 2024. 

- Guo, P.-F., Chen, Y.-H., Tsai, Y.-D., and Lin, S.-D. Towards optimizing with large language models. _arXiv preprint arXiv:2310.05204_ , 2023. 

- Hadi, M. U., Qureshi, R., Shah, A., Irfan, M., Zafar, A., Shaikh, M. B., Akhtar, N., Wu, J., Mirjalili, S., et al. A survey on large language models: Applications, challenges, limitations, and practical usage. _Authorea Preprints_ , 2023. 

- Hadi, M. U., Al Tashi, Q., Shah, A., Qureshi, R., Muneer, A., Irfan, M., Zafar, A., Shaikh, M. B., Akhtar, N., Wu, J., et al. Large language models: a comprehensive survey of its applications, challenges, limitations, and future prospects. _Authorea Preprints_ , 2024. 

- He, K., Zhang, X., Ren, S., and Sun, J. Deep residual learning for image recognition. In _Proceedings of the IEEE conference on computer vision and pattern recognition_ , pp. 770–778, 2016. 

- He, Q., Head, K. L., and Ding, J. Heuristic algorithm for priority traffic signal control. _Transportation research record_ , 2259(1):1–7, 2011. 

- Helsgaun, K. An extension of the lin-kernighan-helsgaun tsp solver for constrained traveling salesman and vehicle routing problems. _Roskilde: Roskilde University_ , 12: 966–980, 2017. 

- Hemberg, E., Moskal, S., and O’Reilly, U.-M. Evolving code with a large language model. _Genetic Programming and Evolvable Machines_ , 25(2):21, 2024. 

- Huang, L., Yu, W., Ma, W., Zhong, W., Feng, Z., Wang, H., Chen, Q., Peng, W., Feng, X., Qin, B., et al. A survey on hallucination in large language models: Principles, taxonomy, challenges, and open questions. _ACM Transactions on Information Systems_ , 2023. 

- Huang, X., Liu, W., Chen, X., Wang, X., Wang, H., Lian, D., Wang, Y., Tang, R., and Chen, E. Understanding the planning of llm agents: A survey. _arXiv preprint arXiv:2402.02716_ , 2024. 

- Hudson, B., Li, Q., Malencia, M., and Prorok, A. Graph neural network guided local search for the traveling salesperson problem. _arXiv preprint arXiv:2110.05291_ , 2021. 

- Jiang, X., Wu, Y., Wang, Y., and Zhang, Y. Unco: Towards unifying neural combinatorial optimization through large language model. _arXiv preprint arXiv:2408.12214_ , 2024. 

- Kambhampati, S., Valmeekam, K., Guan, L., Verma, M., Stechly, K., Bhambri, S., Saldyt, L., and Murthy, A. Llms can’t plan, but can help planning in llm-modulo frameworks. _arXiv preprint arXiv:2402.01817_ , 2024. 

- Kim, M., Choi, S., Kim, H., Son, J., Park, J., and Bengio, Y. Ant colony sampling with gflownets for combinatorial optimization. _arXiv preprint arXiv:2403.07041_ , 2024. 

- Kocsis, L. and Szepesvari,´ C. Bandit based monte-carlo planning. In _European conference on machine learning_ , pp. 282–293. Springer, 2006. 

- Kool, W., Van Hoof, H., and Welling, M. Attention, learn to solve routing problems! _arXiv preprint arXiv:1803.08475_ , 2018. 

10 

**Monte Carlo Tree Search for Comprehensive Exploration in LLM-Based Automatic Heuristic Design** 

- Korte, B. H., Vygen, J., Korte, B., and Vygen, J. _Combinatorial optimization_ , volume 1. Springer, 2011. 

- Kwon, Y.-D., Choo, J., Kim, B., Yoon, I., Gwon, Y., and Min, S. Pomo: Policy optimization with multiple optima for reinforcement learning. _Advances in Neural Information Processing Systems_ , 33:21188–21198, 2020. 

- Kwon, Y.-D., Choo, J., Yoon, I., Park, M., Park, D., and Gwon, Y. Matrix encoding networks for neural combinatorial optimization. _Advances in Neural Information Processing Systems_ , 34:5138–5149, 2021. 

- Lam, R., Willcox, K., and Wolpert, D. H. Bayesian optimization with a finite budget: An approximate dynamic programming approach. _Advances in Neural Information Processing Systems_ , 29, 2016. 

- Langdon, W. B. and Poli, R. _Foundations of genetic programming_ . Springer Science & Business Media, 2013. 

- Lange, R., Tian, Y., and Tang, Y. Large language models as evolution strategies. In _Proceedings of the Genetic and Evolutionary Computation Conference Companion_ , pp. 579–582, 2024. 

- Lee, E. H., Perrone, V., Archambeau, C., and Seeger, M. Cost-aware bayesian optimization. _arXiv preprint arXiv:2003.10870_ , 2020a. 

- Lee, J., Jeon, W., Kim, G.-H., and Kim, K.-E. Montecarlo tree search in continuous action spaces with value gradients. In _Proceedings of the AAAI conference on artificial intelligence_ , volume 34, pp. 4561–4568, 2020b. 

- Lehman, J., Gordon, J., Jain, S., Ndousse, K., Yeh, C., and Stanley, K. O. Evolution through large models. In _Handbook of Evolutionary Machine Learning_ , pp. 331– 366. Springer, 2023. 

- Lin, S. and Kernighan, B. W. An effective heuristic algorithm for the traveling-salesman problem. _Operations research_ , 21(2):498–516, 1973. 

- Liu, F., Tong, X., Yuan, M., and Zhang, Q. Algorithm evolution using large language model. _arXiv preprint arXiv:2311.15249_ , 2023. 

- Liu, F., Lin, X., Wang, Z., Zhang, Q., Xialiang, T., and Yuan, M. Multi-task learning for routing problem with cross-problem zero-shot generalization. In _Proceedings of the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining_ , pp. 1898–1908, 2024a. 

- Liu, F., Xialiang, T., Yuan, M., Lin, X., Luo, F., Wang, Z., Lu, Z., and Zhang, Q. Evolution of heuristics: Towards efficient automatic algorithm design using large language model. In _Forty-first International Conference on Machine Learning_ , 2024b. 

- Liu, F., Yao, Y., Guo, P., Yang, Z., Lin, X., Tong, X., Yuan, M., Lu, Z., Wang, Z., and Zhang, Q. A systematic survey on large language models for algorithm design. _arXiv preprint arXiv:2410.14716_ , 2024c. 

- Liu, F., Zhang, R., Xie, Z., Sun, R., Li, K., Lin, X., Wang, Z., Lu, Z., and Zhang, Q. Llm4ad: A platform for algorithm design with large language model. _arXiv preprint arXiv:2412.17287_ , 2024d. 

- Liu, S., Chen, C., Qu, X., Tang, K., and Ong, Y.-S. Large language models as evolutionary optimizers. In _2024 IEEE Congress on Evolutionary Computation (CEC)_ , pp. 1–8. IEEE, 2024e. 

- Lopez-Ib´ a´nez,˜ M., Dubois-Lacoste, J., Caceres,´ L. P., Birattari, M., and Stutzle,¨ T. The irace package: Iterated racing for automatic algorithm configuration. _Operations Research Perspectives_ , 3:43–58, 2016. 

- Luong, P., Nguyen, D., Gupta, S., Rana, S., and Venkatesh, S. Adaptive cost-aware bayesian optimization. _Knowledge-Based Systems_ , 232:107481, 2021. 

- Lusby, R. M., Larsen, J., Ehrgott, M., and Ryan, D. An exact method for the double tsp with multiple stacks. _International Transactions in Operational Research_ , 17 (5):637–652, 2010. 

- Ma, Y., Li, J., Cao, Z., Song, W., Zhang, L., Chen, Z., and Tang, J. Learning to iteratively solve routing problems with dual-aspect collaborative transformer. _Advances in Neural Information Processing Systems_ , 34:11096– 11107, 2021. 

- Mei, Y., Chen, Q., Lensen, A., Xue, B., and Zhang, M. Explainable artificial intelligence by genetic programming: A survey. _IEEE Transactions on Evolutionary Computation_ , 27(3):621–641, 2022. 

- Merz, P. and Freisleben, B. Genetic local search for the tsp: New results. In _Proceedings of 1997 IEEE International Conference on Evolutionary Computation (ICEC’97)_ , pp. 159–164. IEEE, 1997. 

- Meyerson, E., Nelson, M. J., Bradley, H., Gaier, A., Moradi, A., Hoover, A. K., and Lehman, J. Language model crossover: Variation through few-shot prompting. _arXiv preprint arXiv:2302.12170_ , 2023. 

- Mockus, J. On bayesian methods for seeking the extremum. In _Proceedings of the IFIP Technical Conference_ , pp. 400–404, 1974. 

- Naveed, H., Khan, A. U., Qiu, S., Saqib, M., Anwar, S., Usman, M., Akhtar, N., Barnes, N., and Mian, A. A comprehensive overview of large language models. _arXiv preprint arXiv:2307.06435_ , 2023. 

11 

**Monte Carlo Tree Search for Comprehensive Exploration in LLM-Based Automatic Heuristic Design** 

- Qi, Z., Ma, M., Xu, J., Zhang, L. L., Yang, F., and Yang, M. Mutual reasoning makes smaller llms stronger problemsolvers. _arXiv preprint arXiv:2408.06195_ , 2024. 

- Rajendran, C. Heuristic algorithm for scheduling in a flowshop to minimize total flowtime. _International Journal of Production Economics_ , 29(1):65–73, 1993. 

- Reinelt, G. Tsplib—a traveling salesman problem library. _ORSA journal on computing_ , 3(4):376–384, 1991. 

- Romera-Paredes, B., Barekatain, M., Novikov, A., Balog, M., Kumar, M. P., Dupont, E., Ruiz, F. J., Ellenberg, J. S., Wang, P., Fawzi, O., et al. Mathematical discoveries from program search with large language models. _Nature_ , 625 (7995):468–475, 2024. 

- Rosenkrantz, D. J., Stearns, R. E., and Lewis, II, P. M. An analysis of several heuristics for the traveling salesman problem. _SIAM journal on computing_ , 6(3):563–581, 1977. 

- Sanchez-D´ ´ıaz, X., Ortiz-Bayliss, J. C., Amaya, I., CruzDuarte, J. M., Conant-Pablos, S. E., and Terashima-Mar´ın, H. A feature-independent hyper-heuristic approach for solving the knapsack problem. _Applied Sciences_ , 11(21): 10209, 2021. 

- Sengupta, L., Mariescu-Istodor, R., and Franti, P.¨ Which local search operator works best for the open-loop tsp? _Applied Sciences_ , 9(19):3985, 2019. 

- Shahriari, B., Swersky, K., Wang, Z., Adams, R. P., and De Freitas, N. Taking the human out of the loop: A review of bayesian optimization. _Proceedings of the IEEE_ , 104 (1):148–175, 2015. 

- Shi, W. W., Han, W., and Si, W. C. A hybrid genetic algorithm based on harmony search and its improving. In _Informatics and Management Science I_ , pp. 101–109. Springer, 2013. 

- Shinn, N., Cassano, F., Gopinath, A., Narasimhan, K., and Yao, S. Reflexion: Language agents with verbal reinforcement learning. _Advances in Neural Information Processing Systems_ , 36, 2024. 

- Silver, D., Huang, A., Maddison, C. J., Guez, A., Sifre, L., Van Den Driessche, G., Schrittwieser, J., Antonoglou, I., Panneershelvam, V., Lanctot, M., et al. Mastering the game of go with deep neural networks and tree search. _nature_ , 529(7587):484–489, 2016. 

- Snoek, J., Larochelle, H., and Adams, R. P. Practical bayesian optimization of machine learning algorithms. _Advances in neural information processing systems_ , 25, 2012. 

- Stutzle,¨ T. and Lopez-Ib´ a´nez,˜ M. Automated design of metaheuristic algorithms. _Handbook of metaheuristics_ , pp. 541–579, 2019. 

- Sui, J., Ding, S., Xia, B., Liu, R., and Bu, D. Neuralgls: learning to guide local search with graph convolutional network for the traveling salesman problem. _Neural Computing and Applications_ , 36(17):9687–9706, 2024. 

- Swiechowski,´ M., Godlewski, K., Sawicki, B., and Mandziuk, J.´ Monte carlo tree search: A review of recent modifications and applications. _Artificial Intelligence Review_ , 56(3):2497–2562, 2023. 

- Tan, C. S., Mohd-Mokhtar, R., and Arshad, M. R. A comprehensive review of coverage path planning in robotics using classical and heuristic algorithms. _IEEE Access_ , 9: 119310–119342, 2021. 

- Tuononen, J. Analysis of rebuild local search operator for tsp. Master’s thesis, It¨a-Suomen yliopisto, 2022. 

- Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł., and Polosukhin, I. Attention is all you need. _Advances in neural information processing systems_ , 30, 2017. 

- Vinyals, O., Fortunato, M., and Jaitly, N. Pointer networks. _Advances in neural information processing systems_ , 28, 2015. 

- Voudouris, C. and Tsang, E. Guided local search and its application to the traveling salesman problem. _European journal of operational research_ , 113(2):469–499, 1999. 

- Wei, J., Wang, X., Schuurmans, D., Bosma, M., Xia, F., Chi, E., Le, Q. V., Zhou, D., et al. Chain-of-thought prompting elicits reasoning in large language models. _Advances in neural information processing systems_ , 35:24824–24837, 2022. 

- Weston, J. and Sukhbaatar, S. System 2 attention (is something you might need too). _arXiv preprint arXiv:2311.11829_ , 2023. 

- Williams, C. K. and Rasmussen, C. E. _Gaussian processes for machine learning_ , volume 2. MIT press Cambridge, MA, 2006. 

- Wu, Y., Song, W., Cao, Z., Zhang, J., and Lim, A. Learning improvement heuristics for solving routing problems.. _IEEE Transactions on Neural Networks and Learning Systems_ , 2021. 

- Wu, Z., Qi, Q., Zhuang, Z., Sun, H., and Wang, J. Pretokenization of numbers for large language models. In _The Second Tiny Papers Track at ICLR 2024_ , 2024. 

12 

**Monte Carlo Tree Search for Comprehensive Exploration in LLM-Based Automatic Heuristic Design** 

- Xin, L., Song, W., Cao, Z., and Zhang, J. Neurolkh: Combining deep learning model with lin-kernighan-helsgaun heuristic for solving the traveling salesman problem. _Advances in Neural Information Processing Systems_ , 34: 7472–7483, 2021. 

- Yang, C., Wang, X., Lu, Y., Liu, H., Le, Q. V., Zhou, D., and Chen, X. Large language models as optimizers, 2024. URL https://arxiv.org/abs/2309.03409. 

- Yao, S., Liu, F., Lin, X., Lu, Z., Wang, Z., and Zhang, Q. Multi-objective evolution of heuristic using large language model. _arXiv preprint arXiv:2409.16867_ , 2024a. 

- Yao, S., Yu, D., Zhao, J., Shafran, I., Griffiths, T., Cao, Y., and Narasimhan, K. Tree of thoughts: Deliberate problem solving with large language models. _Advances in Neural Information Processing Systems_ , 36, 2024b. 

- Yao, Y., Liu, F., Cheng, J., and Zhang, Q. Evolve cost-aware acquisition functions using large language models. In _International Conference on Parallel Problem Solving from Nature_ , pp. 374–390. Springer, 2024c. 

   - Zhang, Y., Pan, Y., Wang, Y., and Cai, J. Pybench: Evaluating llm agent on various real-world coding tasks. _arXiv preprint arXiv:2407.16732_ , 2024c. 

   - Zheng, Z., Yao, S., Li, G., Han, L., and Wang, Z. Pareto improver: Learning improvement heuristics for multiobjective route planning. _IEEE Transactions on Intelligent Transportation Systems_ , 2023. 

   - Zheng, Z., Yao, S., Wang, Z., Tong, X., Yuan, M., and Tang, K. Dpn: Decoupling partition and navigation for neural solvers of min-max vehicle routing problems. _arXiv preprint arXiv:2405.17272_ , 2024a. 

   - Zheng, Z., Zhou, C., Xialiang, T., Yuan, M., and Wang, Z. Udc: A unified neural divide-and-conquer framework for large-scale combinatorial optimization problems. _arXiv preprint arXiv:2407.00312_ , 2024b. 

   - Zhou, A., Yan, K., Shlapentokh-Rothman, M., Wang, H., and Wang, Y.-X. Language agent tree search unifies reasoning acting and planning in language models. _arXiv preprint arXiv:2310.04406_ , 2023. 

- Ye, H., Wang, J., Cao, Z., Berto, F., Hua, C., Kim, H., Park, J., and Song, G. Reevo: Large language models as hyper-heuristics with reflective evolution. _arXiv preprint arXiv:2402.01145_ , 2024a. 

- Ye, H., Wang, J., Cao, Z., Liang, H., and Li, Y. Deepaco: neural-enhanced ant systems for combinatorial optimization. _Advances in Neural Information Processing Systems_ , 36, 2024b. 

- Ye, H., Wang, J., Liang, H., Cao, Z., Li, Y., and Li, F. Glop: Learning global partition and local construction for solving large-scale routing problems in real-time. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , 2024c. 

- Yin, H., Kononova, A. V., Back,¨ T., and van Stein, N. Controlling the mutation in large language models for the efficient evolution of algorithms. _arXiv preprint arXiv:2412.03250_ , 2024. 

- Yu, H. and Liu, J. Deep insights into automated optimization with large language models and evolutionary algorithms. _arXiv preprint arXiv:2410.20848_ , 2024. 

- Zhang, D., Huang, X., Zhou, D., Li, Y., and Ouyang, W. Accessing gpt-4 level mathematical olympiad solutions via monte carlo tree self-refine with llama-3 8b. _arXiv preprint arXiv:2406.07394_ , 2024a. 

- Zhang, D., Zhoubian, S., Hu, Z., Yue, Y., Dong, Y., and Tang, J. Rest-mcts*: Llm self-training via process reward guided tree search. _arXiv preprint arXiv:2406.03816_ , 2024b. 

13 

**Monte Carlo Tree Search for Comprehensive Exploration in LLM-Based Automatic Heuristic Design** 

# **A. Related Work** 

This section presents a detailed literature review of various research areas related to LLM, AHD, MCTS, and CO problems. 

## **A.1. AHD** 

Automatic Heuristic Design, also known as Hyper-Heuristics, (Burke et al., 2013) aims to find the best-performing heuristic among an extensive set of valid heuristics, i.e., the heuristic space. As the search strategy, AHD generally adopts the evolutionary algorithm to update heuristic algorithms automatically (Stutzle & L¨ opez-Ib´ a´nez˜ , 2019) using various effective methodologies and frameworks (Blot et al., 2016; Lopez-Ib´ a´nez et al.˜ , 2016; Burke et al., 2019). GP (Mei et al., 2022) is a prevailing and effective approach for AHD. However, it requires hand-crafted operators for heuristic mutation and crossover (Duflo et al., 2019; S´anchez-D´ıaz et al., 2021). 

## **A.2. Neural Combinatorial Optimization (NCO)** 

Traditional methods for NP-hard CO problems contain exact algorithms (Fischetti et al., 2007; Lusby et al., 2010) and approximation algorithms (including handcrafted heuristics) (Merz & Freisleben, 1997; Helsgaun, 2017). Integrating the deep learning technique (He et al., 2016; Vaswani et al., 2017), Neural Combinatorial Optimization (NCO) methods can obtain near-optimal results with less time consumption compared to traditional methods (Bello et al., 2016; Kool et al., 2018). These methods train neural networks for decision-making with diverse solving process (e.g., the LKH algorithm (Xin et al., 2021), the GLS algorithm (Sui et al., 2024; Hudson et al., 2021), improvement-based framework (Wu et al., 2021; Zheng et al., 2023), or step-by-step construction (Vinyals et al., 2015; Zheng et al., 2024a)). NCO methods can be regarded as a special kind of Hyper-Heuristics (AHD) (Ye et al., 2024a), where the solving process is the general framework of AHD and training NCO methods searches for the optimal parameter settings within a parameterized heuristic space. In contrast to traditional heuristics, NCO does not require expert knowledge so some NCO methods can be applied to multiple CO problems (Ye et al., 2024c; Zheng et al., 2024b; Liu et al., 2024a; Drakulic et al., 2024; Berto et al., 2024). 

Compared to NCO methods, designing heuristics with LLM-based AHD methods for NP-hard CO problems demonstrates better efficiency, better applicability, and lower implementation difficulty. Training an NCO model on a given framework would take several days or even several weeks on an advanced GPU (Kwon et al., 2020), whereas a high-quality heuristic can be generated in a few hours using the LLM-based AHD methods without GPU requirements. Considering applicability, NCO methods require special framework and network designs to solve special CO problems (Kwon et al., 2021), but LLM-based AHD methods can be applied to new CO problems without task-specific adaptations. NCO methods also bring implementation difficulties when creating complicated task environments for model training (Zheng et al., 2024b). Instead, LLM-based AHD methods only need some linguistic descriptions as the task environment. Moreover, LLM-based AHD methods can even demonstrate better results than NCO methods in some application scenarios, as shown in Table 1, Table 2, and Table 8, heuristics designed by the proposed MCTS-AHD can outperform advanced NCO methods under the same solving framework (e.g. POMO (Kwon et al., 2020), DeepACO (Ye et al., 2024b)) in 10 out of 16 test sets. 

## **A.3. LLM for EC** 

EC is a generic optimization principle inspired by natural evolution (Back et al.¨ , 1997; Eiben & Smith, 2015). The core idea of EC is to generate a set of candidate solutions (called populations) by simulating genetic variation and natural selection in the process of biological evolution and to gradually optimize these solutions through an iterative process over multiple generations. Some recent work focuses on stimulating the crossover or mutation operators in the original evolutionary computation framework by prompting LLMs (Lehman et al., 2023; Meyerson et al., 2023; Lange et al., 2024) or introducing LLMs to generate auxiliary information (Ye et al., 2024a). LLM-based EC approaches can be specified to plenty of application scenarios, including planning (Kambhampati et al., 2024), code generation (Hemberg et al., 2024), and LLM-based AHD discussed in this article (Romera-Paredes et al., 2024). 

## **A.4. LLM for AHD** 

LLM-based AHD methods with populations can be summarized as a four-part process (Liu et al., 2023; Romera-Paredes et al., 2024; Liu et al., 2024b; Ye et al., 2024a; Dat et al., 2024; Liu et al., 2024d), **1):** Heuristics Initialization: LLM-based AHD methods employ LLMs to generate multiple initial heuristic functions or directly handcraft seed functions as initial heuristic functions. **2):** Operator selection: Existing methods design a variety of prompts corresponding to mutation or 

14 

**Monte Carlo Tree Search for Comprehensive Exploration in LLM-Based Automatic Heuristic Design** 

crossover operators on parent heuristics. In this step, population-based methods will randomly select an operator to be executed. Afterward, these methods also select the parent heuristic(s) to be operated from the current population (Yin et al., 2024). **3):** New heuristic generation: Next, LLM-based AHD methods will prompt LLMs for the Python code implementation of a new heuristic function based on the description of the task _P_ , general framework, the prompt of selected operators, and the selected parent heuristics. **4):** Population update: As the final step in each iteration, each newly generated heuristic _h_ will run on the evaluation dataset _D_ to obtain _g_ ( _h_ ). The invalid heuristics will be discarded. The population will update according to performances _g_ ( _·_ ) of heuristics. The last three processes will run in a loop until the number of heuristic evaluations reaches a given budget _T_ . 

Yao et al. (2024a) considers multiple objectives (for example, heuristic performance and execution efficiency) in LLM-based AHD. This article focuses only on heuristic performances, so we do not involve it as a baseline. 

## **A.5. LLM for CO** 

Besides LLM-based AHD, there are also two ways to utilize LLMs for CO problems, including LLM-as-optimizer methods and (fine-tuned) LLM-as-solver methods. Yang et al. (2024) first develop LLMs as the optimizer for TSP tours. LLM-asoptimizer methods (Guo et al., 2023; Liu et al., 2024e) initially generate several feasible solutions for a single CO instance. Then, the LLM is iteratively prompted for better solutions by taking the existing top-performing solutions and their objective values as in-context information. Then, the newly generated solution in each iteration is evaluated for its objective value and inserted back into the in-context. LLM-as-solver methods directly treat LLMs as end-to-end CO instance solvers (Abgaryan et al., 2024; Jiang et al., 2024). These methods consider LLMs as pre-trained NCO models and establish environments to fine-tune LLMs for better performances on CO instances. 

LLM-based AHD methods, especially MCTS-AHD, are still the most promising directions for solving complex NP-hard CO problems. LLM-as-optimizer methods pose high demand for LLM’s reasoning ability and knowledge storage, and current LLMs (Huang et al., 2024) can only offer extremely limited results on infamous and large-scale CO instances (refer to comparisons in Table 12). It should be noted that Kambhampati et al. (2024) also recommends using LLMs for module design instead of instance solving for planning tasks, where the module design process corresponds to the idea of LLM-based AHD. (Fine-tuned) LLM-as-solver methods (Abgaryan et al., 2024; Jiang et al., 2024) require additional training and face difficulties in configuring training environments. Moreover, unlike NCO models that represent each coordinate value as a piece of embeddings, LLMs face challenges in tokenizing high-precision coordinate numbers in a linguistic way (Wu et al., 2024). 

## **A.6. LLM Inference with MCTS** 

With the great success of CoT (Wei et al., 2022) and ToT (Yao et al., 2024b) in enhancing the ability of LLM reasoning, a series of System 2 techniques (Weston & Sukhbaatar, 2023) have been proposed. Among them, MCTS has recently emerged as a powerful technique to enhance the reasoning capabilities of LLMs (Zhang et al., 2024b). These methods mainly construct MCTS in two ways (Feng et al., 2023), representing each node with a complete answer refined from the parents (Zhang et al., 2024a; Zhou et al., 2023) or a reasoning step following its parents (Qi et al., 2024). The MCTS-AHD in this paper belongs to the former, where each node represents a complete piece of executable function and its description. When dealing with commonsense QA or mathematical problems, System 2 techniques often use self-evaluation for MCTS simulation (Zhang et al., 2024a), but MCTS-AHD does not involve the self-evaluation or rollout (Silver et al., 2016) since AHD methods can easily obtain performances _g_ ( _·_ ) for tasks. 

## **A.7. LLM for Code Generation** 

Recent LLMs have strong coding capabilities (Zhang et al., 2024c), and some recent papers have designed a series of structures based on reflection and MCTS (Dainese et al., 2024; DeLorenzo et al., 2024) to promote this ability. The LLM for code generation is a similar domain to LLM-based AHD. Compared to code generation tasks aiming at passing algorithm tests, LLM-based AHD faces significantly more challenges in finding the optimal heuristic (Liu et al., 2024c). LLM-based AHD needs to consider more on exploring the entire heuristic space and optimizing code performances by modifying parameter settings and detail designs. 

As a similar method to this paper, Brandfonbrener et al. (2024) uses MCTS with the progressive widening technique for code generation, but its specific MCTS and progressive widening procedure are totally different from the proposed MCTS-AHD. 

15 

**Monte Carlo Tree Search for Comprehensive Exploration in LLM-Based Automatic Heuristic Design** 

# **B. Definition of Tasks** 

## **B.1. NP-hard CO Problems** 

This paper conducts experiments on six NP-hard representative CO problems, including TSP, CVRP, KP, MKP, ASP, and BPP. For BPP, we consider both its online setting (online BPP) and offline setting (offline BPP). In this section, we will introduce the mathematical definitions of these CO problems in detail. 

**Traveling Salesman Problem** TSP is one of the most representative COPs (Biggs, 1986), which aims at finding the shortest path to visit each city once and returns to the starting point. An _N_ -node TSP instance **_ins_** contains distance matrix _{_ **_D_** = _dj,k, j_ = 1 _, . . . , N, k_ = 1 _. . . , N } ∈_ R<sup>_N×N_</sup> , where _dj,k_ denotes the cost between nodes _k_ and _j_ , the goal is to minimize the following objective function (Zheng et al., 2024b): 



where the solution **_s_** = ( _s_ 1 _, s_ 2 _, . . . , sN_ ) is a permutation of all node indexes. All the feasible solutions satisfy the constraint of the degree of each node being two and containing no loop with lengths less than N. 

**Capacitated Vehicle Routing Problem** CVRP aims to plan several capacity-constrained vehicles starting at and returning to a depot, meeting the demands of multiple customers, and minimizing the total travel distance. Each CVRP instance contains a depot (the 0-th node) and several customers. With a distance matrix _{_ **_D_** = _dj,k, j_ = 0 _, . . . , N, k_ = 0 _. . . , N }_ , the CVRP can be expressed as follows: 



where **_s_** is a solution representing the complete route of vehicles and consists of _q_ sub-routes **_s_** = _{_ **_ρ_**<sup>1</sup> _,_ **_ρ_**<sup>2</sup> _, . . . ,_ **_ρ_**<sup>_q_</sup> _}_ . Each sub-route **_ρ_**<sup>_j_</sup> = ( _ρ_<sup>_j_</sup> 1<sup>_, . . . , ρj_</sup> _nj_<sup>)</sup><sup>_,j∈{_1</sup><sup>_, . . . , q}_starts from the depot</sup><sup>_s_0and goes back to</sup><sup>_s_0,</sup><sup>_nj_represents the number of</sup> customer nodes in it. _n_ =<sup>�</sup><sup>_q_</sup> _j_ =1<sup>_nj_is the total number of customer nodes;</sup><sup>_δi_denotes the demand of node</sup><sup>_i_;</sup><sup>_C_denotes the</sup> capacity of the vehicle. This paper follows the settings of ReEvo (Ye et al., 2024a) when generating CVRP data sets, fixing the depot coordinates to (0.5, 0.5). 

**0-1 Knapsack Problem** KP is a typical CO problem, consider loading items of a maximum total value to a _W_ -capacity knapsack. Each item can only be picked once. KP solution **_s_** _⊆{_ 1 _,_ 2 _, ..., N }_ records the selection item indexes. A KP instance **_ins_** records the value _vi ∼_ Uniform(0 _,_ 1) and weight _wi ∼_ Uniform(0 _,_ 1) of each candidate item. We follow the settings in Kool et al. (2018) in generating instances and have _W_ = 25 for 100-item and 200-item KP instances and _W_ = 12 _._ 5 for 50-item ones. 

We adopt a traditional greedy heuristic algorithm for the Greedy Construct in Table 1 (Kwon et al., 2020). This algorithm starts with an empty knapsack (as solution **_s_** ) and recursively adds the item that meets the capacity limit and has the maximum value-weight-ratio ( _w_<sup>_<u>vi</u>_</sup> _i_<sup>) from the remaining items into the current knapsack (add this item to solution</sup><sup>**_s_**as well).</sup> The algorithm will stop when the knapsack can no longer load more items. 

**Multiple Knapsack Problem** We follow the ReEvo (Ye et al., 2024a) settings for MKP instances, uniformly sampling the value _vi ∼_ Uniform(0 _,_ 1) and weight for the _m_ knapsack _wij ∼_ Uniform(0 _,_ 1) _, i ∈{_ 1 _, . . . , m}, j ∈{_ 1 _, . . . , n}_ . We also uniformly sample the capacity of the _m_ knapsacks _Ci, i ∈{_ 1 _, . . . , m}_ from (max _j wij,_<sup>�</sup> _j_<sup>_wij_).</sup> 

**Admissible Set Problem** ASP constructs a set of _n_ -dimensional vectors _A_ (called an admissible set) where vectors **_a_** _∈A ⊂{_ 0 _,_ 1 _,_ 2 _}_<sup>_n_</sup> and the number of non-zero items is constrained to be _w_ . ASP aims to maximize the size of the admissible set _A_ under a certain constraint that for any three distinct vectors there is a coordinate in which their three 

16 

**Monte Carlo Tree Search for Comprehensive Exploration in LLM-Based Automatic Heuristic Design** 

respective values are _{_ 0 _,_ 0 _,_ 1 _}_ , _{_ 0 _,_ 0 _,_ 2 _}_ , or _{_ 0 _,_ 1 _,_ 2 _}_ . We formulate the objective function and constraints as follows: 



where I[ _ai̸_ = 0] represents the number of non-zero items in vector **_a_** = ( _a_ 1 _, . . . , an_ ). 

**Bin Packing Problem** BPP is a classic NP-hard CO problem that aims to place a set of items with different sizes into as few _W_ -capacity bins as possible. Online BPP requires making an immediate decision on which bin to place once a new item is received, while offline BPP does not require this. We follow Romera-Paredes et al. (2024) and Liu et al. (2024b) to generate WeiBull instances for online BPP and follow Ye et al. (2024a) to generate offline BPP instances with _W_ = 150 and the size of items uniformly sampled from 20 to 100. 

## **B.2. Cost-Aware Acquisition Function Design in Bayesian Optimization** 

Please refer to Appendix C.4 for relevant introductions. 

17 

**Monte Carlo Tree Search for Comprehensive Exploration in LLM-Based Automatic Heuristic Design** 

# **C. Definition of General Frameworks** 

For NP-hard combinatorial optimization (CO) problems, we employ MCTS-AHD to design key functions within given general frameworks. To verify the framework-agnosticism of MCTS-AHD, we include three general frameworks for CO in experiments, e.g., step-by-step construction, GLS, and ACO, as well as the CAF design task using BO as the outer framework. Next, in this section, we will introduce these involved general frameworks in detail. 

## **C.1. Step-by-Step Construction** 

Step-by-step construction is an intuitive framework capable of handling almost all CO problems. It considers gradually extending a solution ( **_s_** ) of an NP-hard CO problem from scratch until a complete and feasible solution is constructed. In each step of the construction (i.e., solution extension), the step-by-step construction framework assigns priority to each candidate (decision variable), and the candidate with the highest priority will be added to the solution. 

In the step-by-step construction framework, MCTS-AHD and LLM-based AHD baselines design the same key heuristic function that will be repeatedly executed to calculate the priority of candidates. This paper adopts the step-by-step construction framework for solving four CO problems, including TSP, KP, ASP, and online BPP. Built on this framework, Nearest-greedy is a prevailing manually designed heuristic for TSP that scores candidate nodes based sorely on their distance from the current node. Similarly, a greedy process that evaluates KP items based on their value-weight ratio is also commonly used. We consider these two handcrafted heuristics as the Greedy Construct baseline in Table 1. Additionally, in both TSP and KP, there is a series of NCO methods that train deep neural networks based on the step-by-step construction framework. Their neural networks can be considered as more efficient and sophisticated key functions for evaluating all candidate nodes or items. For involved CO problems, the detailed settings of the key heuristic function in the step-by-step construction frameworks are as follows: 

- For TSP, MCTS-AHD is responsible for designing a function to select the next node to visit based on node coordinates, starting point, distance matrix, and all unvisited nodes. 

- For KP, MCTS-AHD is responsible for selecting the next item to add to the knapsack based on the value and weight of all items to be chosen and the remaining capacity of the knapsack. 

- For ASP, the key function provides a score for the current vector to determine to what extent it is suitable to be added to the admissible set ( _A_ ). 

- In MCTS-AHD, the function required for online BPP gives a preference score for adding the current newly input item to each bin based on the item’s size and the remaining capacity of all bins. 

## **C.2. Ant Colony Optimization** 

ACO is a meta-heuristic and evolutionary algorithm (EA) inspired by the behavior of ants to find the shortest route between their colony and food sources (Dorigo et al., 2006; Ansari & Daxini, 2022). 

ACO records a pheromone matrix **_τ_** and a heuristic matrix **_η_** . Each item in the matrix _τij_ indicates the priority of including that edge ( _i, j_ ) in a solution. The pheromone trails are iteratively updated based on the quality of the solutions found, encouraging future ants to follow better paths. The heuristic information on each edge (i.e., _ηij_ ) is a problem-specific measure that indicates the immediate benefit of choosing a particular path. For solving TSP with ACO and a manually designed heuristic matrix, _ηij_ is often set to the inverse of the distance between cities _i_ and _j_ , that is, _ηij_ = _d_ <u>1</u> _ij_<sup>.LLM-based</sup> AHD methods are employed to design a more effective heuristic matrix **_η_** based on the necessary problem-specific inputs. 

Ants construct solutions by moving from node to node, probabilistically choosing the next node based on a combination of pheromone and heuristic information. After all the ants have constructed their solutions, the pheromone levels update. An ACO iteration typically involves solution construction, optional local search, and pheromone update. By iteratively applying these steps, ACO algorithms can effectively explore the solution space and converge toward optimal or near-optimal solutions for NP-hard CO problems. We follow the settings in Ye et al. (2024a), evaluating MCTS-AHD by designing the heuristic metrics generation functions for TSP, CVRP, MKP, and offline BPP as follows: 

- For TSP, the function inputs the distance matrix. We adopt the parameter settings in ReEvo (Ye et al., 2024a), the number of ants is set to 30 during heuristic evaluation (when evaluating on the evaluation dataset _D_ ), and the number 

18 

**Monte Carlo Tree Search for Comprehensive Exploration in LLM-Based Automatic Heuristic Design** 

of iterations is 100. In testing, we allow more optimization for all ACO baselines and increase the number of iterations to 500. 

- Functions for CVRP input the distance matrix, coordinates and demands of nodes, and the capacity _C_ . Numbers of ants and iterations are set the same as TSP. 

- For MKP, the function inputs the values and weights of items. The number of ants is set to 10. The number of iterations is 50 for running on the evaluation dataset _D_ and 100 for test sets. 

- For offline BPP, the function inputs the size of items and the capacity of bins. The number of ants is set to 20. The number of iterations is 15 for running on the evaluation dataset _D_ and 100 for test sets. 

**ACO for Black-box Settings** Black-box settings are proposed in ReEvo (Ye et al., 2024a) as novel application scenarios for LLM-based AHD. The black-box settings do not provide descriptions for the task _P_ and the predefined general framework for heuristic design. The names of inputs in the to-be-designed key function will also be erased. These settings can simulate the application scenarios that cannot find any linguistic descriptions. This paper will evaluate AHD methods on both regular settings and black-box settings in Appendix F.8. For a better initial perception of the heuristic space _H_ , we set _NI_ = 10 for MCTS-AHD in designing heuristics with black-box settings. 

## **C.3. Guided Local Search** 

The GLS framework uses local search algorithms (e.g., using 2-opt operators) for solution iterations and introduces a penalty mechanism to guide the search process escaping local optima. It shows capability on a wide range of CO problems with manually designed key functions (Voudouris & Tsang, 1999; Alhindi et al., 2019). We use LLM-based AHD methods to design the key heuristic function for generating knowledge-based matrices in the knowledge-guided local search (KGLS) framework (Arnold & Sorensen¨ , 2019). Taking the TSP as an example, KGLS maintains a TSP solution while also preserving the ever-encountered best-performing solution. In each iteration of KGLS, KGLS first perturbs the TSP solution based on the generated knowledge matrix and then performs local searches using both 2-opt and relocate operators (Sengupta et al., 2019; Tuononen, 2022). We conduct 1200 iterations when running GLS heuristics on both the heuristic evolution process and testing for each CO instance. The number of perturbations to each solution is set to 30. 

## **C.4. Bayesian Optimization** 

BO (Shahriari et al., 2015) is a method for solving the black-box optimization problem where the objective is to find the global minimum of an unknown function _f_ ( **x** ) over a search space _X_ , represented as: 



Two core components of BO are the probabilistic surrogate model and the acquisition function (Mockus, 1974; Lam et al., 2016). In each iteration of BO, the probabilistic surrogate model is first trained using the available samples in the search space (BO typically employs a Gaussian process (GP) model (Williams & Rasmussen, 2006)). Then, the acquisition function utilizes the posterior information of the surrogate model to guide the subsequent search. Specifically, the next solution to evaluate at iteration _t_ , denoted as **x** _t_ , is chosen by maximizing the acquisition function: 



where _Mt_ represents the information from the surrogate model at iteration _t_ , and _α_ ( **x** _, Mt_ ) represents the acquisition function value at **x** . After performing an expensive evaluation at **x** _t_ , this point is added to the available training dataset of samples. BO iteratively executes surrogate benchmark training and sampling based on the acquisition function until a termination criterion is met. Finally, the best solution among those evaluated samples is returned as the solution to the problem. 

This article focuses on the cost-aware BO (Yao et al., 2024c; Luong et al., 2021; Snoek et al., 2012), which takes the number of expensive sample evaluations as the termination criterion. It not only focuses on optimizing the objective function but also considers the cost of evaluating the objective function. This method is beneficial in practical applications, especially when the evaluation cost of the objective function is high, like experimental design and hyper-parameter optimization of 

19 

**Monte Carlo Tree Search for Comprehensive Exploration in LLM-Based Automatic Heuristic Design** 

machine learning models. BO employs a CAF as the acquisition function in cost-aware settings to manage the sample efficiency, which is the design focus of the cost-aware BO methods. We adopt LLM-based AHD methods for designing the CAF. During CAF evolutions, MCTS-AHD and EoH run 5 independent cost-aware BO trails with at most 12 function samples. In testing, we set the evaluation budget to 30 and report the average result of 10 trials. 

# **D. Details of Evaluations & Experiments** 

In this section, we provide a more detailed introduction to the setup of evaluation budgets _T_ and evaluation datasets _D_ used in the heuristic evaluation phase. Evaluation Settings in this paper are generally adopted from Funsearch (Romera-Paredes et al., 2024), EoH (Liu et al., 2024b), and ReEvo (Ye et al., 2024a). 

**The Setting of** _T_ . The number of generations in EoH is set to 20. Its population size is 20 for online BPP and 10 for TSP and FSSP (810 evaluations for TSP, FFSP, and 1620 for online BPP). So, this paper designs a similar number for the maximum number of evaluations _T_ , setting the _T_ to 2,000 for online BPP (under the step-by-step construction framework) and setting _T_ = 1 _,_ 000 for other tasks. 

**The Setting of** _D_ . For most involved tasks, MCTS-AHD adopts the same settings in LLM-based baseline methods (e.g., EoH, ReEvo, Funsearch) for the evaluation dataset _D_ . As a special case, for online BPP under the step-by-step construction framework, baselines adopt 5 5,000-item WeiBull BPP instances with _W_ =100. However, such a dataset setting often leads to heuristics that completely fail at other scales (e.g., 5,000-item with _W_ =500), so we used a varying-scale setup (Gao et al., 2024) that included data with different characteristics in the evaluation dataset _D_ . The detailed settings of the evaluation datasets are exhibited in Table 6 

**Pre-Trained Large Language Models** . The pre-trained LLM is _gpt-4o-mini-2024-07-18_ for _GPT-4o-mini_ and _gpt3.5-turbo-0125_ for _GPT-3.5-turbo_ , we also use _Claude-3.5-sonnet-20241022_ for _Claude-3.5-sonnet_ and _DeepSeek-v3_ , _Qwen2.5-Coder-32b-Instruct_ in Appendix F.4. 

_Table 6._ Compositions of the evaluation dataset _D_ on involved general frameworks and tasks. 

|Framework|Step-by-step|Construction|
|---|---|---|
|Task|TSP|KP|
|Evaluation dataset_D_|64 50-node TSP instances|64 100-item KP instances (W=25)|
|Framework|Step-by-step|Construction|
|Task|ASP|Online BPP|
||1 instance (n=15, w=10)|4 WeiBull BPP instances<br>1,000-item instance with W=100|
|Evaluation dataset_D_||1,000-item instance with W=500<br>5,000-item instance with W=100<br>5,000-item instance with W=500|
|Framework|A|CO|
|Task|TSP|CVRP|
|Evaluation dataset_D_|5 50-node TSP instances|10 50-node CVRP instances|
|Framework|A|CO|
|Task|MKP|Offline BPP|
|Evaluation dataset_D_|5 100-item MKP instances (m=5)|5 500-item BPP instances (W=150)|
|Framework|GLS|CAF Design|
|Task|TSP|-|
||10 TSP200 instances|2 synthetic instances|
|Evaluation dataset_D_||The Ackley instance<br>The Rastrigin instance|



**Other Parameters.** MCTS-AHD adopts the same set of parameters for all tasks involved, and here we will summarize the other parameters of MCTS-AHD in the evaluation phase. The temperature of LLMs is fixed at 1 _._ 0. The number of initial nodes _NI_ = 4, the maximum depth of the MCTS tree _H_ = 10, the number of mutations in each expansion _k_ = 2, the maximum number of references in action e1 _p ∈{_ 2 _,_ 3 _,_ 4 _,_ 5 _}_ , the initial exploration parameter _λ_ 0 = 0 _._ 1, and the progressive widening parameter _α_ = 0 _._ 5. We consider _λ_ 0 = 0 _._ 1 to be the most important setting of these and therefore ablate it in the main text, and we discuss the rest of the settings in Appendix F.7 to illustrate that none of these parameters are sensitive. 

20 

**Monte Carlo Tree Search for Comprehensive Exploration in LLM-Based Automatic Heuristic Design** 

# **E. Detailed Methodology** 

## **E.1. Prompts of MCTS Actions** 

MCTS-AHD contains 6 distinct actions i1, e1, e2, m1, m2, and s1 for MCTS initialization and expansion. Next, we describe the meaning and prompt engineering of each action. These prompts contain the problem description, existing heuristic functions as contexts, function name, input name, and output name according to the task _P_ and the current MCTS. We execute the first LLM call through the following action prompts to obtain a design idea and its Python implementation for a heuristic function. The rest of this subsection provides examples for prompts, in which we highlight the unique part of each prompt in red colors (for all actions, we use the TSP task and the step-by-step construction framework as an example): 

- **Initial Action i1** : Action i1 represents directly getting an idea of designing a valid heuristic function from scratch and a Python implementation directly through LLM. 

## **Prompt for Action i1** 

Solving Traveling Salesman Problem (TSP) with constructive heuristics. TSP requires finding the shortest path that visits all given nodes and returns to the starting node. 

First, describe the design idea and main steps of your algorithm in one sentence. The description must be inside a brace outside the code implementation. Next, implement it in Python as a function named ’select ~~n~~ ext ~~n~~ ode’. 

This function should accept 4 input(s): ’current ~~n~~ ode’, ’destination ~~n~~ ode’, ’unvisited ~~n~~ odes’, ’distance ~~m~~ atrix’. The function should return 1 output(s): ’next ~~n~~ ode’. The select ~~n~~ ext ~~n~~ ode function takes as input the current node, the destination ~~n~~ ode, a set of unvisited nodes, and a distance matrix, and returns the next node to visit. 

Do not give additional explanations. 

- **Crossover Action e1** : Action e1 inputs several distinct heuristic functions with their codes, their descriptions, and their performances. The prompt asks the LLM to get an idea for a new heuristic function different from all these heuristic functions and its corresponding Python implementation. The heuristics are selected from 2 to 5 subtrees of the MCTS root. 

## **Prompt for Action e1** 

Solving Traveling Salesman Problem (TSP) with constructive heuristics. TSP requires finding the shortest path that visits all given nodes and returns to the starting node. 

I have k existing algorithms with their codes as follows: 

No.1 algorithm’s description, its corresponding code and its objective value are: 

# Its Description 

# Its Python Code Implementation of A Function 

Objective value: # The Objective Value of the heuristic algorithm with the python code on a evaluation dataset. 

No.k algorithm’s description, its corresponding code and its objective value are: 

- # Its Description 

# Its Python Code Implementation of A Function 

Objective value: # The Objective Value of the heuristic algorithm with the python code on a evaluation dataset. 

Please create a new algorithm that has a totally different form from the given algorithms. Try generating codes with different structures, flows or algorithms. The new algorithm should have a relatively low objective value. 

First, describe the design idea and main steps of your algorithm in one sentence. The description must be inside 

21 

**Monte Carlo Tree Search for Comprehensive Exploration in LLM-Based Automatic Heuristic Design** 

a brace outside the code implementation. Next, implement it in Python as a function named ’select ~~n~~ ext ~~n~~ ode’. 

This function should accept 4 input(s): ’current ~~n~~ ode’, ’destination ~~n~~ ode’, ’unvisited ~~n~~ odes’, ’distance ~~m~~ atrix’. The function should return 1 output(s): ’next ~~n~~ ode’. The select ~~n~~ ext ~~n~~ ode function takes as input the current node, the destination ~~n~~ ode, a set of unvisited nodes, and a distance matrix, and returns the next node to visit. 

Do not give additional explanations. 

- **Crossover Action e2** : Action e2 inputs one parent heuristic function (with its code, description, and performance) and one reference heuristic function sampled from a 10-size top-performing elite heuristic function set _E_ (we follow Liu et al. (2024b) in selecting a heuristic function from the set, the heuristic function in the set with rank _ri_ will be sampled with a priority _pi_ = _ri_ +101<sup>).The following prompt asks the LLM to design a new heuristic function based on the parent</sup> one and learn from the advantageous designs of the reference one. 

## **Prompt for Action e2** 

Solving Traveling Salesman Problem (TSP) with constructive heuristics. TSP requires finding the shortest path that visits all given nodes and returns to the starting node. 

I have 2 existing algorithms with their codes as follows: 

No.1 algorithm’s description, its corresponding code and its objective value are: # Its Description # Its Python Code Implementation of A Function Objective value: # The Objective Value of the heuristic algorithm with the python code on a evaluation dataset. 

No.2 algorithm’s description, its corresponding code and its objective value are: # Its Description # Its Python Code Implementation of A Function Objective value: # The Objective Value of the heuristic algorithm with the python code on a evaluation dataset. 

Please create a new algorithm that has a similar form to the No.2 algorithm and is inspired by the No.1 algorithm. The new algorithm should have an objective value lower than both algorithms. 

Firstly, list the common ideas in the No.1 algorithm that may give good performances. Secondly, based on the common idea, describe the design idea based on the No.len(indivs) algorithm and main steps of your algorithm in one sentence. The description must be inside a brace. Next, implement it in Python as a function named ’select next ~~n~~ ode’. 

This function should accept 4 input(s): ’current ~~n~~ ode’, ’destination ~~n~~ ode’, ’unvisited ~~n~~ odes’, ’distance ~~m~~ atrix’. The function should return 1 output(s): ’next ~~n~~ ode’. The select ~~n~~ ext ~~n~~ ode function takes as input the current node, the destination ~~n~~ ode, a set of unvisited nodes, and a distance matrix, and returns the next node to visit. 

Do not give additional explanations. 

- **Mutation Action m1** : Action m1 inputs a heuristic function with its description and code, it attempts to introduce more new mechanisms and new formulas or program segments to the input code through LLM. 

## **Prompt for Action m1** 

Solving Traveling Salesman Problem (TSP) with constructive heuristics. TSP requires finding the shortest path that visits all given nodes and returns to the starting node. 

22 

**Monte Carlo Tree Search for Comprehensive Exploration in LLM-Based Automatic Heuristic Design** 

I have one algorithm with its code as follows.: 

# Its Description # Its Python Code Implementation of A Function 

Please create a new algorithm that has a different form but can be a modified version of the provided algorithm. Attempt to introduce more novel mechanisms and new equations or programme segments. 

First, describe the design idea and main steps of your algorithm in one sentence. The description must be inside a brace outside the code implementation. Next, implement it in Python as a function named ’select ~~n~~ ext ~~n~~ ode’. 

This function should accept 4 input(s): ’current ~~n~~ ode’, ’destination ~~n~~ ode’, ’unvisited ~~n~~ odes’, ’distance ~~m~~ atrix’. The function should return 1 output(s): ’next ~~n~~ ode’. The select ~~n~~ ext ~~n~~ ode function takes as input the current node, the destination ~~n~~ ode, a set of unvisited nodes, and a distance matrix, and returns the next node to visit. 

Do not give additional explanations. 

- **Mutation Action m2** : Action m2 also inputs the description and implementation of a heuristic function, it attempts to generate a heuristic function with different parameter settings through LLM. 

## **Prompt for Action m2** 

Solving Traveling Salesman Problem (TSP) with constructive heuristics. TSP requires finding the shortest path that visits all given nodes and returns to the starting node. 

I have one algorithm with its code as follows.: 

# Its Description 

# Its Python Code Implementation of A Function 

Please identify the main algorithm parameters and help me in creating a new algorithm that has different parameter settings to equations compared to the provided algorithm. 

First, describe the design idea and main steps of your algorithm in one sentence. The description must be inside a brace outside the code implementation. Next, implement it in Python as a function named ’select ~~n~~ ext ~~n~~ ode’. 

This function should accept 4 input(s): ’current ~~n~~ ode’, ’destination ~~n~~ ode’, ’unvisited ~~n~~ odes’, ’distance ~~m~~ atrix’. The function should return 1 output(s): ’next ~~n~~ ode’. The select ~~n~~ ext ~~n~~ ode function takes as input the current node, the destination ~~n~~ ode, a set of unvisited nodes, and a distance matrix, and returns the next node to visit. 

Do not give additional explanations. 

- **Tree-Path Reasoning Action s1** : Action s1 is a tree-special action that takes all diverse heuristic functions (with their codes, descriptions, and performances) on a leaf-to-root tree path as input. The following prompt asks the LLM to get a better heuristic function based on these inputted in-contexts. When there is only one unique heuristic function in the tree path, we do not perform the action s1. 

## **Prompt for Action s1** 

Solving Traveling Salesman Problem (TSP) with constructive heuristics. TSP requires finding the shortest path that visits all given nodes and returns to the starting node. 

23 

**Monte Carlo Tree Search for Comprehensive Exploration in LLM-Based Automatic Heuristic Design** 

I have k existing algorithms with their codes as follows: No.1 algorithm’s description, its corresponding code and its objective value are: # Its Description # Its Python Code Implementation of A Function Objective value: # The Objective Value of the heuristic algorithm with the python code on a evaluation dataset. ... No.k algorithm’s description, its corresponding code and its objective value are: # Its Description # Its Python Code Implementation of A Function Objective value: # The Objective Value of the heuristic algorithm with the python code on a evaluation dataset. 

Please help me create a new algorithm that is inspired by all the above algorithms with its objective value lower than any of them. 

Firstly, list some ideas in the provided algorithms that are clearly helpful to a better algorithm. Secondly, based on the listed ideas, describe the design idea and main steps of your new algorithm in one sentence. The description must be inside a brace. Thirdly, implement it in Python as a function named ’select ~~n~~ ext ~~n~~ ode’. 

This function should accept 4 input(s): ’current ~~n~~ ode’, ’destination ~~n~~ ode’, ’unvisited ~~n~~ odes’, ’distance ~~m~~ atrix’. The function should return 1 output(s): ’next ~~n~~ ode’. The select ~~n~~ ext ~~n~~ ode function takes as input the current node, the destination ~~n~~ ode, a set of unvisited nodes, and a distance matrix, and returns the next node to visit. 

Do not give additional explanations. 

## **E.2. The Prompt of the Thought-Alignment Process** 

After obtaining the design idea and implementation by calling LLMs with the previous action prompts, MCTS-AHD will conduct the second LLM call. In the second LLM call, we will input the design idea and implementation obtained from the previous LLM call into the thought-alignment prompt as shown below for a more detailed and correlated heuristic function description. 

## **The thought-alignment Prompt** 

Solving Traveling Salesman Problem (TSP) with constructive heuristics. TSP requires finding the shortest path that visits all given nodes and returns to the starting node. 

Following is the Design Idea of a heuristic algorithm for the problem and the code with function name ’select ~~n~~ ext node’ for implementing the heuristic algorithm. 

The select ~~n~~ ext ~~n~~ ode function takes as input the current node, the destination ~~n~~ ode, a set of unvisited nodes, and a distance matrix, and returns the next node to visit. 

Design Idea: # The Design Idea 

Code: 

# The Python Code Implementation of A Function 

The content of the Design Idea idea cannot fully represent what the algorithm has done informative. So, now you should re-describe the algorithm using less than 3 sentences. Hint: You should reference the given Design Idea and highlight the most critical design ideas of the code. You can analyse the code to describe which variables are given higher priorities and which variables are given lower priorities, the parameters and the structure of the code. 

24 

**Monte Carlo Tree Search for Comprehensive Exploration in LLM-Based Automatic Heuristic Design** 

## **E.3. Examples of LLM Outputs** 

This subsection provides two examples of LLM output in designing heuristics with MCTS-AHD. Every single LLM-based heuristic generation includes two LLM calls. The first call generates **the Python code of a heuristic function** with action prompts and the second call generates **linguistic descriptions** for heuristic functions with thought-alignment prompts. 

## **Example of LLM output #1: Designing TSP heuristics within the step-by-step solving framework.** 

## **First Call Input:** 

The prompt for an MCTS-AHD action. 

## **First Call Output:** 

_{_ The new algorithm will utilize a hybrid approach that weighs the immediate distance (1.2) more heavily while still considering the connection strength (0.6), ensuring that we select paths that are both cost-effective in the short term and reasonable in the longer term by optimizing the total accumulated cost. _}_ 

def select_next_node(current_node, destination_node, unvisited_nodes, distance_matrix): if not unvisited_nodes: return None 

next_node = None min_combined_cost = float(’inf’) 

for candidate in unvisited_nodes: 

immediate_distance = distance_matrix[current_node][candidate] connection_strength = sum(distance_matrix[candidate][n] for n in unvisited_nodes if n != candidate) / (max(len(unvisited_nodes) - 1, 1)) 

total_cost = immediate_distance current_candidate = candidate remaining_nodes = unvisited_nodes - {candidate} 

while remaining_nodes: 

best_next_node = min(remaining_nodes, key=lambda node: distance_matrix[ current_candidate][node]) total_cost += distance_matrix[current_candidate][best_next_node] current_candidate = best_next_node remaining_nodes.remove(best_next_node) 

total_cost += distance_matrix[current_candidate][destination_node] 

combined_cost = (1.2 * immediate_distance) + (0.6 / (connection_strength + 1)) + total_cost 

- if combined_cost < min_combined_cost: min_combined_cost = combined_cost next_node = candidate 

return next_node 

## **Second Call Input:** 

The prompt of the thought-alignment process. 

## **Second Call Output:** 

The algorithm utilizes a hybrid approach to solve the Traveling Salesman Problem by prioritizing immediate distance (with a weight of 1.2) over connection strength (with a weight of 0.6) to select the next node to visit from a set of unvisited nodes. It calculates a combined cost that considers the immediate distance to a candidate node, the average connection strength to remaining unvisited nodes, and the total cost of visiting all remaining nodes before returning to the destination. The algorithm systematically evaluates candidate nodes based on this combined cost, ensuring a balance between short-term efficiency and overall path optimization. 

25 

**Monte Carlo Tree Search for Comprehensive Exploration in LLM-Based Automatic Heuristic Design** 

## **Example of LLM output #2: Designing CAF for Cost-aware BO.** 

## **First Call Input:** 

The prompt for an MCTS-AHD action. 

## **First Call Output:** 

_{_ The new algorithm evaluates the potential improvement over the best observed value while incorporating a compound risk factor based on both uncertainty and evaluation costs, adjusts the utility through a combination of historical performance scaling, and normalizes the results across the test inputs to favor those with high expected returns and low associated costs. _}_ 

import torch 

def utility(train_x, train_y, best_x, best_y, test_x, mean_test_y, std_test_y, cost_test_y, budget_used, budget_total): 

# Calculate remaining budget remaining_budget = budget_total - budget_used 

# Adjust the mean based on uncertainty risk_factor = std_test_y / (std_test_y + 1e-10) adjusted_mean = mean_test_y * (1 - risk_factor) 

# Improvement over the best observed value improvement_score = adjusted_mean - best_y 

# Calculate cost-effectiveness with exponential decay based on evaluation costs cost_effectiveness = (improvement_score / (cost_test_y + 1e-10)) * torch.exp(cost_test_y / (remaining_budget + 1e-10)) 

# Historical risk/variance for budget scaling historical_variance = torch.var(train_y, unbiased=False) 

budget_scaling = remaining_budget / (remaining_budget + historical_variance + 1e -10) 

# Combine cost-effectiveness with budget scaling final_utility = cost_effectiveness * budget_scaling 

# Normalize the utility values utility_value = (final_utility - torch.min(final_utility)) / (torch.max( final_utility) - torch.min(final_utility) + 1e-10) 

return utility_value 

## **Second Call Input:** 

The prompt of the thought-alignment process. 

## **Second Call Output:** 

The algorithm evaluates potential improvements over the best observed value by leveraging a risk-adjusted mean of the predicted function, where uncertainty is factored in through the standard deviation. It incorporates costeffectiveness by weighing the expected improvement against evaluation costs, applying an exponential decay influenced by the remaining budget. Finally, the utility values are scaled by historical variance to prioritize inputs that promise higher expected returns while accounting for their associated costs, ultimately normalizing the output to facilitate comparison across test inputs. 

26 

**Monte Carlo Tree Search for Comprehensive Exploration in LLM-Based Automatic Heuristic Design** 

## **E.4. Total Algorithm** 

Algorithm 1 provides a pseudo-code for the proposed MCTS-AHD method, which provides details of the flow and parameter settings. The procedure of MCTS-AHD mainly includes an initialization process (up to line 8) and a four-stage MCTS process (line 8 to line 39). 

**Algorithm 1** MCTS-AHD: Monte Carlo Tree Search for Automatic Heuristic Design 

- 1: **Input:** Evaluation dataset _D_ , The number of initial nodes _NI_ , Maximal evaluation times _T_ , Maximal tree depth _H_ = 10, Action set _{i_ 1 _, e_ 1 _, e_ 2 _, m_ 1 _, m_ 2 _, s_ 1 _}_ , The number of mutation in each expansion _k_ = 2, The number of subtrees in action e1 _{_ 2 _,_ 3 _,_ 4 _,_ 5 _}_ , UCT initial exploration parameter _λ_ 0 = 0 _._ 1, Progressive widening parameter _α_ = 0 _._ 5. 

- 2: **Output:** Code _C_<sup>_∗_</sup> for the best found heuristic functions _h_<sup>_∗_</sup> . 

- 3: Initialize a virtual root node _nr_ . _// The virtual root node does not contain any codes._ 4: Set _t ←_ 0. _// t represents the current number of evaluations._ 

- 5: Initialize a code and its description with Action i1, and get all other _NI −_ 1 initial nodes with Action e1. 6: _qmax ←−_ 1 _e_ 5, _qmin ←_ 0 7: Link all the _NI_ nodes to the MCTS root. 

- 8: Evaluating the newly generated codes with evaluation dataset _D_ , setting the Q, N values for these nodes. 9: **while** _t ≤ T_ **do** 

- 10: _λ ← λ_ 0 _∗_<sup>_<u>T</u>_</sup> _T_<sup>_−t_</sup> _//_ **_Exploration-decay._** _// MCTS Selection Stage: Selecting a node to expand_ 

- 11: **if** _⌊N_ ( _nr_ )<sup>_α_</sup> _⌋≥|_ Children( _nr_ ) _|_ **then** 12: Expand _nr_ with action e1, doing simulation and backpropagation. _//_ **_Progressive Widening for the root node._** 13: _t ← t_ + 1. _// Updating evaluation time t._ 14: **end if** 15: _nc ← nr // Selecting from root node._ 16: **while** _nc_ is not a leaf and its depth is less than _H_ **do** _<u>Q</u>_ <u>(</u> _c_ <u>)</u> _−qmin_ ln _N_ <u>(</u> _nc_ <u>+1)</u> 

- 17: _nc ←_ arg max _c∈_ Children( _nc_ ) � _qmax−qmin_<sup>+</sup><sup>_λ ·_</sup> ~~�~~ _N_ ( _c_ ) � 18: **if** _⌊N_ ( _nc_ )<sup>_α_</sup> _⌋≥|_ Children( _nc_ ) _|_ **then** 19: Expand _nc_ with action e2, doing simulation and backpropagation. _//_ **_Progressive Widening non-root nodes._** 20: _t ← t_ + 1. _// Updating evaluation time t._ 

- 21: **end if** 

22: **end while** _// MCTS Expansion Stage: Add new nodes to the tree_ 

23: Conducting action e2, s1, _k_ times of m1, and _k_ times of m2 to the _nc_ by LLM. _// MCTS Simulation Stage: Get Q values for newly expanded nodes_ 

- 24: Evaluating the newly generated heuristic function with evaluation dataset _D_ , 

- 25: Setting the Q, N values for these nodes. 26: If a better heuristic function is found, update the best found code _C_<sup>_∗_</sup> with its implementation. 

27: Updating the elite set _E_ if new top 10 heuristic functions emerge. 28: _t ← t_ + 2 _k_ + 2. _// Updating the number of evaluations t._ 29: **for** _c ∈_ Children( _nc_ ) **do** 30: _qmax ←_ max( _qmax, Q_ ( _c_ )), _qmin ←_ min( _qmin, Q_ ( _c_ )) _// Updating qmax and qmin._ 31: **end for** _// MCTS Backpropagation Stage: Update Q and N values_ 32: **while** _nc_ is not the root _nr_ **do** 33: _Q_ ( _nc_ ) _←_ max _c∈_ Children( _nc_ ) _Q_ ( _c_ ) _// Updating the Q value._ 34: _N_ ( _nc_ ) _← N_ ( _nc_ ) + 2 _k_ + 2 _// Updating visit times._ 35: _nc ←_ Father( _nc_ ) 36: **end while** 37: _Q_ ( _nr_ ) _←_ max _c∈_ Children( _nr_ ) _Q_ ( _c_ ) _// Updating the Q value._ 38: _N_ ( _nr_ ) _← N_ ( _nr_ ) + 2 _k_ + 2 _// Updating visit times._ 39: **end while** 40: **Return:** The best found code _C_<sup>_∗_</sup> for heuristics. 

27 

**Monte Carlo Tree Search for Comprehensive Exploration in LLM-Based Automatic Heuristic Design** 

# **F. Experiment Details** 

## **F.1. Designing Heuristics with the Step-by-step Construction Framework for ASP** 

We apply MCTS-AHD to another NP-hard CO problem ASP (Romera-Paredes et al., 2024). ASP constructs a set of n-dimensional vectors _A_ (named an admissible set) in which each vector _∈{_ 0 _,_ 1 _,_ 2 _}_<sup>_n_</sup> and the number of non-zero items in each vector is constrained to be _w_ . ASP aims to maximize the size of the admissible set _A_ with another certain constraint between the vectors in the admissible set (detailed in Appendix B.1). LLM-based AHD methods are responsible for designing a priority function: _{_ 0 _,_ 1 _,_ 2 _}_<sup>_n_</sup> _→_ R, which is executed iteratively to construct _A_ step by step. We use a single instance with _n_ =15 and _w_ =10 as the evaluation dataset _D_ . The experiments in Table 7 test the heuristics on four different scales where MCTS-AHD also exhibits the best results compared to other existing LLM-based AHD methods in most test sets. 

_Table 7._ Designing step-by-step construction heuristics for ASP. Each LLM-based AHD method is run three times for its average performance. The size of _A_ has a theoretically upper bound � _wn_ �, and we take this value as Optimal. The test set of each scale contains only one instance and we underline the in-domain scale. The best-performing method for each LLM model is shaded and the overall best result is in bold. 

|Task||A|SP||
|---|---|---|---|---|
|Methods|_n_=12,_w_=7|_n_=15,_w_=10<br>:|_n_=21,_w_=15:|_n_=24,_w_=17:|
|Optimal|792|3003|43596|237984|
||LLM-ba|sed AHD:_GPT-3.5-tur_|_bo_||
|Funsearch|612.0|2057.0|10664.0|37323.0|
|EoH|772.0|2759.0|30869.3|147323.0|
|MCTS-AHD(Ours)|784.0|2784.0|30608.0|150729.0|
||LLM-b|ased AHD:_GPT-4o-mi_|_ni_||
|Funsearch|622.0|2410.0|10758.7|43217.0|
|ReEvo|**784.0**|2733.0|25753.7|115709.0|
|HSEvo|744.0|2307.0|18756.3|81185.0|
|EoH|779.0|2776.0|32716.7|160024.0|
|MCTS-AHD (Ours)|775.0|**2780.0**|**32900.3**|**163832.0**|



## **F.2. Guided Local Search Framework** 

To evaluate the performance of MCTS-AHD in designing the penalty heuristics of the GLS framework, we follow Ye et al. (2024a) in using MCTS-AHD for the key heuristic function to generate the knowledge matrix of KGLS (Arnold et al., 2019) and employing 10 TSP200 instances for performance evaluations (as _D_ ). The number of local search iterations in GLS is set to 1200 for both heuristic designs and heuristic testings. We compare MCTS-AHD to LLM-based AHD baselines, NCO methods with GLS frameworks, and the original KGLS with manually designed heuristic functions. As shown in Table 8, the proposed MCTS-AHD can refine the KGLS on both the TSP200 and TSP500 test sets and MCTS-AHD generally outperforms other LLM-based AHD methods using _GPT-4o-mini_ as the black-box pre-trained LLM. 

_Table 8._ Designing heuristics within the GLS general framework for solving TSP. KGLS, NCO methods, and heuristics from LLM-based AHD allow 1200 iterations of local search. The test sets of TSP with _N_ =100 and _N_ =200 are 1,000-instance test sets from Table 1 and for TSP500 and TSP1000, we prepare two 64-instance test sets. For NeuralGLS* and GNNGLS*, we use the results reported in Ye et al. (2024a). The table shows the gaps to optimal and each LLM-based AHD method is run three times for the average optimality gaps. 

||TSP-G|LS|||
|---|---|---|---|---|
|N=|100|200|500|1,000|
|Optimal|0.0000%|0.0000%|0.0000%|0.0000%|
|KGLS|**0.0034%**|0.2270%|0.9578%|**1.5348%**|
|_NCO_|_methods with the G_|_LSgeneralframewor_|_k_||
|VRP-DACT (Ma et al.,2021)|1.7943%|91.9267%|-|-|
|NeuOpt (**?**)|0.2950%|0.9152%|-|-|
|NeuralGLS* (Sui et al.,2024)|0.470%*|3.622%*|-|-|
|GNNGLS*(Hudson et al.,2021)|0.705%*|3.522%*|-|-|
||_LLM-based AHD:_|_GPT-4o-mini_|||
|EoH|0.0065%|**0.2025%**|0.9534%|1.6083%|
|ReEvo|0.0076%|0.2210%|0.9993%|1.6155%|
|MCTS-AHD (Ours)|0.0060%|0.2106%|**0.9495%**|1.5985%|



28 

**Monte Carlo Tree Search for Comprehensive Exploration in LLM-Based Automatic Heuristic Design** 

## **F.3. P-values for Significance** 

The design performance of the LLM-based AHD method follows an implicit distribution. Although running a method three times can preliminarily indicate the advantages and disadvantages of this method, it still cannot prove the significant difference between its performance distribution algorithm and the performance distributions of comparison algorithms. In this section, we introduce the p-value to demonstrate the significant advantage of MCT-AHD compared to the main LLM-based AHD baseline EoH. We employ both EoH and MCTS-AHD to design up to ten heuristics for a portion of CO problems considered in this paper, and the results and p-values for each run are shown in Table 9. In any of the four application scenarios, there is at least a 96% confidence in satisfying the hypothesis that MCTS-AHD leads compared to an LLM-based AHD baseline with population EoH. 

_Table 9._ Up to ten runs of EoH and MCTS-AHD on a portion of NP-hard CO problems with step-by-step construction frameworks and ACO frameworks. “avg“ in the Table below represents the average and “std“ means the standard variant. The p-value is calculated with single-tailed t-tests. 

|CO Problem|Methods|run1|run2|run3|run4|run5|run6|run7|run8|run9|run10|avg|std|p-value|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|||G|eneral Fr|amewor|k: Step-|by-stepC|onstruct|ion, LL|M:_GPT-_|_4o-mini_|||||
|TSP50|EoH<br>MCTS-AHD|6.452<br>6.174|6.447<br>6.156|6.284<br>6.347|6.386<br>6.356|6.316<br>6.285|6.372<br>6.274|6.480<br>6.257|6.480<br>6.365|6.259<br>6.289|6.388<br>6.302|6.386<br>6.280|0.080<br>0.071|0.002855655|
|KP100,_W_ = 25|EoH<br>MCTS-AHD|40.229 <br> 40.259|40.231 <br> 40.265|40.232 <br> 40.231|40.231 <br> 40.236|40.234 <br> 40.233|40.264 <br> 40.262|40.240 <br> 40.264|40.235 <br> 40.233|40.229 <br> 40.233|40.235 <br> 40.262|40.236 <br> 40.248|0.010<br> 0.015|0.027524885|
|||||General|Framew|ork: AC|O, LLM:|_GPT-4o_|_-mini_||||||
|5|EoH|5.827|5.825|5.831|5.830|5.828|-|-|-|-|-|5.828|0.003||
|TSP0|MCTS-AHD|5.798|5.779|5.827|5.742|5.830|-|-|-|-|-|5.795|0.036|0.039230447|
|MKP100 5|EoH|23.149|23.133|23.136|23.311|23.266|-|-|-|-|-|23.199|0.083||
|,_m_=|MCTS-AHD|23.235|23.284|23.287|23.294|23.294|-|-|-|-|-|23.279|0.025|0.037268388|



## **F.4. MCTS-AHD with Other LLMs** 

Besides using GPT models as LLMs (as shown in the other part of this article), MCTS-AHD can cooperate with other open-source or closed-source LLMs as well. This subsection evaluates MCTS-AHD on designing step-by-step construction heuristics for TSP and KP utilizing other advanced pre-trained LLMs, including closed-source LLM _Claude-3.5-sonnet_ and Open-source LLM _DeepSeek-v3_ , _Qwen2.5-Coder-32b-Instruct_ . Performances of the designed heuristics are shown in Table 10, where heuristics design with _Claude-3.5-sonnet_ , _DeepSeek-v3_ , and _Qwen2.5-Coder-32b-Instruct_ can still surpass handcrafted heuristics in both TSP and KP test sets and outperform the advanced NCO method POMO (which needs task-specific training) in KP. Moreover, MCTS-AHD runs with _GPT-4o-mini_ exhibit the best performance in each test set, demonstrating that _GPT-4o mini_ could be the best choice in LLM for MCTS-AHD. 

_Table 10._ An extension of Table 1, employing both GPT models and open-source LLMs for MCTS-AHD. Each MCTS-AHD result is averaged over three runs and we highlight the MCTS-AHD result with the best performance on each test set. 

|||T|SP|||K|P||
|---|---|---|---|---|---|---|---|---|
|N=|_N_|=50|_N_|=100|_N_=100,|_W_=25|_N_=200|,_W_=25|
|Method|Obj.↓|Gap|Obj.↓|Gap|Obj.↑|Gap|Obj.↑|Gap|
|Optimal|5.675|-|7.768|-|40.271|-|57.448|-|
|Greedy Construct|6.959|22.62%|9.706|24.94%|40.225|0.12%|57.395|0.09%|
|POMO|5.697|0.39%|8.001|3.01%|39.676|1.48%|57.271|0.09%|
||Clos|ed-Source|LLMs||||||
|MCTS-AHD(_GPT-3.5-turbo_)|6.346|11.82%|8.861|14.08%|40.233|0.09%|57.393|0.10%|
|MCTS-AHD(_GPT-4o-mini_)|6.225|9.69%|8.684|11.79%|40.252|0.05%|57.423|0.04%|
|MCTS-AHD(_Claude-3.5-sonnet_)|6.503|14.57%|9.036|16.32%|40.233|0.10%|57.396|0.09%|
||Ope|n-Source|LLMs||||||
|MCTS-AHD(_DeepSeek-v3_)|6.348|11.85%|8.859|14.04%|40.233|0.10%|57.402|0.08%|
|MCTS-AHD(_Qwen2.5-Coder-32b-Instruct_)|6.272|10.52%|8.685|11.81%|40.235|0.09%|57.402|0.08%|



29 

**Monte Carlo Tree Search for Comprehensive Exploration in LLM-Based Automatic Heuristic Design** 

## **F.5. Results on TSPLib: Compare to GP-based AHD Methods** 

We conduct tests on a well-known real-world TSP benchmark TSPLib (Reinelt, 1991) (we adopt instances with nodes less than 500 in this article) to compare the quality of MCTS-AHD to a GP-based AHD method GHPP (Duflo et al., 2019). Christofides (Christofides, 2022), Greedy (Brecklinghaus & Hougardy, 2015), Nearest insertion, and nearest-greedy (Rosenkrantz et al., 1977) are famous manually designed heuristics for TSP. We use the reported results of these algorithms in the article (Duflo et al., 2019). Meanwhile, the results of GHPP also come from Duflo et al. (2019). 

For LLM-based AHD methods EoH and MCTS-AHD, we use the best-performing step-by-step constructive heuristic among their three runs with _GPT-4o-mini_ for their performances. We use the best-performing heuristic of ReEvo according to their report in Ye et al. (2024a). On each TSPLib instance, We run the heuristics of EoH, ReEvo, and MCTS-AHD three times with different starting nodes for an average performance. As shown in Table 11, the heuristic from MCTS-AHD can surpass manually designed baselines, the GP-based AHD method GHPP, and LLM-based AHD baselines in the average optimality gap. 

_Table 11._ Results of GP-based AHD method GPHH, LLM-based methods on designing heuristics for TSP with the step-by-step construction framework. Christofides, Greedy, Nearest insertion, and Nearest-greedy are manually designed heuristics for TSP where their results are also drawn from (Duflo et al., 2019). We report the optimality gap of each instance and heuristics designed by LLM-based AHD methods are run 3 times with different starting nodes for average performances. The leading LLM-designed heuristic on each instance is <u>marked in shaded and the overall best heuristic is in bold.</u> 

|Instance|Christofides|Greedy|Nearest insertion|Nearest-greedy|GPHH-best|EoH|ReEvo|MCTS-AHD|
|---|---|---|---|---|---|---|---|---|
|ts225.tsp|5.67%|**5.38%**|19.93%|16.82%|7.71%|5.57%|6.56%|10.84%|
|rat99.tsp|**9.43%**|22.30%|21.05%|21.79%|14.09%|18.78%|12.41%|10.46%|
|bier127.tsp|13.03%|19.50%|23.05%|23.25%|15.64%|14.05%|10.79%|**7.56%**|
|lin318.tsp|13.80%|18.75%|24.44%|25.78%|14.30%|**14.03%**|16.63%|14.07%|
|eil51.tsp|15.18%|13.03%|16.14%|31.96%|10.20%|8.37%|**6.47%**|15.98%|
|d493.tsp|**9.52%**|16.68%|20.39%|24.00%|15.58%|12.41%|13.43%|11.73%|
|kroB100.tsp|**9.82%**|16.59%|21.53%|26.26%|14.06%|13.46%|12.20%|11.43%|
|kroC100.tsp|9.08%|12.94%|24.25%|25.76%|16.22%|16.85%|15.88%|**8.27%**|
|ch130.tsp|10.09%|28.40%|19.21%|25.66%|14.77%|12.26%|**9.40%**|10.18%|
|pr299.tsp|**11.23%**|31.42%|25.05%|31.42%|18.24%|23.58%|20.63%|**11.23%**|
|fl417.tsp|15.57%|12.64%|25.52%|32.42%|22.72%|20.47%|19.15%|**10.20%**|
|kroA150.tsp|13.44%|20.24%|19.09%|26.08%|15.59%|18.36%|11.62%|**10.08%**|
|pr264.tsp|**11.28%**|11.89%|34.28%|17.87%|23.96%|18.03%|16.78%|12.27%|
|pr226.tsp|14.17%|21.44%|28.02%|24.65%|15.51%|19.90%|18.02%|**7.15%**|
|pr439.tsp|**11.16%**|20.08%|24.67%|27.36%|21.36%|21.96%|19.25%|15.12%|
|Average Gap|11.50%|18.09%|23.11%|25.41%|16.00%|15.87%|13.95%|**11.10%**|



## **F.6. Compare to LLM-as-Optimizer Methods** 

As discussed in Appendix A, another LLM-based approach for CO problems, LLM-as-optimizer methods cannot achieve outstanding performance in large-scale instances. Here we compare this type of method with the proposed MCTS-AHD. As shown in Table 12, LLM-as-optimizer methods LEMA (Liu et al., 2024e) and OPRO (Yang et al., 2024) can provide better solutions in very-small-scale TSP20 instances, but as the scale increases to TSP50, these methods will fail to achieve convergence in LLM-based solution optimizations. 

_Table 12._ Comparison of LLM-as-optimizer methods and MCTS-AHD designed heuristics. We display the optimality gap of MCTS-AHD on TSP20 and TSP50 test sets with 1,000 instances, respectively. Results of LEMA and OPRO are drawn from the original literature and the LLM for all methods in this table is _<u>GPT-3.5-turbo</u>_ <u>.</u> 

|Methods|LEMA*|OPRO*|MCTS-AHD(step-by-stepconstruction)|
|---|---|---|---|
|TSP20|3.94%|4.40%|7.71%|
|TSP50|-|133.00%|11.82%|



30 

**Monte Carlo Tree Search for Comprehensive Exploration in LLM-Based Automatic Heuristic Design** 

## **F.7. Discussion: Ablation of Other Parameters** 

In 5.1, we have provided partial ablation experiments, focusing mainly on verifying that _λ −_ 0 = 0 _._ 1 is a reasonable setting and validating the effectiveness of the three proposed components (Progressive Widening, Thought Alignment, and Exploration decay) and MCTS-AHD’s expansion actions. MCTS-AHD also includes other parameters, such as the number of initial solutions _NI_ , the threshold parameter for progressive widening _α_ , and the number of actions m1 and m2 in each expansion _k_ . We believe that MCTS-AHD is not sensitive to the settings of these parameters. In this section, we will introduce the reasons for their default settings and demonstrate their flexibility through ablation experiments. 

_NI_ determines the number of initial nodes (i.e., heuristic samples), which affects the perception of heuristic space by LLM in the early iterations of the heuristic evolution. Table 13 shows that adjusting it to _NI_ = 10 has no significant effect on the results, indicating that using _NI_ = 4 is sufficient. Under the setting of evaluating _T_ times in total, progressive widening allows the maximum number of level-1 tree nodes connected to the root to be at most _⌊T_<sup>_α_</sup> _⌋_ . Larger _α_ settings will drive the MCTS tree shallow, affecting the quality of multi-hop reasoning brought by MCTS. Therefore, we choose to set _α_ = 0 _._ 5 to balance the depth of the MCTS tree and the importance of progressive widening. According to Table 13, changing this setting to _α_ = 0 _._ 6 does not result in significant effect degradation. The setting of _k_ = 2 allows MCTS to utilize the randomness brought about by LLM in trying different search directions in each expansion, and setting it to _k_ = 1 does not cause a significant degradation in performances as well. 

_Table 13._ Ablation on the number of initial solution _NI_ , the threshold parameter for progressive widening _α_ , the number of actions m1 and m2 in each expansion _k_ . The performances of MCTS-AHD variants are averaged over five runs. 

||TSP50|KP100|
|---|---|---|
|_NI_ = 4(Default Setting in MCTS-AHD, 10 runs)|10.661%|0.059%|
|_NI_ = 10|11.094%|0.047%|
|_α_= 0_._5(Default Setting in MCTS-AHD, 10 runs)|10.661%|0.059%|
|_α_= 0_._6|10.891%|0.063%|
|_k_ = 2(Default Setting in MCTS-AHD, 10 runs)|10.661%|0.059%|
|_k_ = 1|11.380%|0.049%|



## **F.8. Discussion: The Advantage Scope of MCTS** 

MCTS-AHD shows greater strengths in application scenarios with a more complex heuristic space _H_ and tasks with more descriptions as knowledge. 



<!-- Start of picture text -->
Relationship of Space Size and Gap Ratio<br>35%<br>TSP-SC-3.5<br>30% TSP-SC-4o<br>KP-SC-3.5<br>25%<br>KP-SC-4o<br>ASP-SC-3.5<br>20%<br>ASP-SC-4o<br>15% TSP-GLS-4o<br>CAF-BO-4o<br>10% TSP-ACO-4o<br>CVRP-ACO-4o<br>5%<br>Trend line<br>0%<br>-5%<br>-10%<br>7.5 10.0 12.5 15.0 17.5 20.0 22.5 25.0<br>Approximate Size of Heuristic Space H<br>Optimality Gap Ratio<br><!-- End of picture text -->

_Figure 5._ The relation of approximate heuristic space size _n_ and the optimality gap ratio between EoH and MCTS-AHD (i.e., 1 _−_ Gap _MCT S−AHD/_ Gap _EoH_ ). We consider EoH as a baseline for its applicability in all tasks. We do not include tasks with unavailable optimal objective values (e.g., online BPP). The legends have been simplified, for example, TSP-GLS-4o represents designing GLS heuristics for TSP with _GPT-4o-mini_ . SC in the figure is an abbreviation for step-by-step construction. 

> • **Better in Application Scenarios with a More Complex Heuristic Space** _H_ . Each heuristic function can be expressed in the form of _a_ 1 _f_ 1( _x_ ) + _a_ 2 _f_ 2( _x_ ) + _a_ 3 _f_ 3( _x_ ) + _. . ._ + _anfn_ ( _x_ ), representing linear combinations of different sub- 

31 

**Monte Carlo Tree Search for Comprehensive Exploration in LLM-Based Automatic Heuristic Design** 

functions, where _x_ denotes the particular input ( **_ins_** ) of the heuristic function _h_ . The heuristic space _H_ to be explored for an application scenario can be defined as the set of all meaningful sub-functions, i.e., _H_ = Span _{f_ 1( _x_ ) _, . . .}_ . To estimate the size of the set consisting of all meaningful sub-functions, we use OpenAI _o1-mini-2024-09-12_ to analyze the top 10 heuristic functions of EoH and MCTS-AHD in their respective 3 runs (6 runs and 60 heuristic functions in total), ordering LLM to break functions down into linearly independent sub-functions and use the number of sub-functions _n_ to estimate the size of the heuristic space. 

We hypothesize that for more complex heuristic spaces, MCTS-AHD can explore the heuristic space more comprehensively compared to population-based methods such as EoH. To test this hypothesis, in Figure 5, we plot the relation of estimated heuristic space size _n_ and the leads in optimality gap between MCTS-AHD and EoH (the y-axis in Figure, 1 _−_ Gap _MCT S−AHD/_ Gap _EoH_ ). The results verify our hypothesis. As the trend line demonstrates, MCTS-AHD tends to achieve a more significant lead compared to the population-based baseline EoH in application scenarios with larger _n_ . It indicates that MCTS-AHD may be more suitable for application scenarios with more complex heuristic spaces _H_ . 

- **Better in Application Scenarios with More Descriptions** . As shown in Table 14, MCTS-AHD demonstrates a significant decrease in effectiveness in black-box settings, taking the lead only in the TSP task. This suggests that MCTS-AHD will perform better in application scenarios with more descriptions (e.g.,white-box cases). 

_Table 14._ Implementing MCTS-AHD on Black-box CO tasks with ACO general frameworks. We follow the settings of Ye et al. (2024a) in heuristic evolution and run each LLM-based method three times for average performance. The white-box results are the same as Table 2. 

||TSP|CVRP|MKP|Offline BPP|
|---|---|---|---|---|
|N=|_N_=50|_N_=50,_C_=50|_N_=100,_m_=5|_N_=500,_C_=150|
|Methods|Obj.↓|Obj.↓|Obj.↑|Obj.↓|
|ACO|5.992|11.355|22.738|208.828|
|DeepACO|5.842|8.888|23.093|203.125|
||Whi<br>|te-box Setting: _GPT-4o_<br>|_-mini_<br>||
|EoH|5.828|9.359|23.139|204.646|
|ReEvo|5.856|9.327|23.245|206.693|
|MCTS-AHD(Ours)|5.801|9.286|23.269|204.094|
||Bla|ck-box Setting: _GPT-4o_|_-mini_||
|EoH|5.831|9.401|23.240|204.615|
|ReEvo|5.860|9.404|23.196|206.021|
|MCTS-AHD(Ours)|5.830|9.444|23.191|205.375|



We can explain that MCTS-AHD’s better performance in application scenarios with complex heuristic space is highly beneficial from its ability to explore complex function spaces and escape from local optima. 

For its mediocre performance in black-box application scenarios, I believe this is mainly because compared to MCTS, which only performs limited expansion on each heuristic, the population structure is computationally intensive and often involves many rounds of LLM-based operations on a heuristic function in the population. So, the effectiveness of MCTS-AHD may require LLMs more on its generation quality in limited number of MCTS expansions. In contrast, black-box application scenarios make it difficult for LLMs to guarantee this condition, so these application scenarios will be tough for MCTS-AHD. 

# **G. Examples of Evolution** 

To visually demonstrate the workflow of MCTS-AHD and its ability on exploration, we provide two examples of the evolution of heuristics in two tasks, as shown in Figure 6. 

The two examples of evolution clearly exhibit how MCTS-AHD conducts comprehensive explorations. For example, in designing heuristics with a step-by-step construction framework for TSP, MCTS-AHD can expand potential child nodes from nodes (e.g., MCTS node with ”Expansion: t=611”) that are not among the top 10 optimal ones (the performance range of the top 10 optimal heuristics is the yellow shade), and ultimately reach the best heuristic. It reflects the superiority of employing MCTS as an optimization framework instead of population-based EC. Population-based LLM-based AHD methods such as EoH, ReEvo, and HSEvo lack consideration of worse-performing but potential heuristics. These algorithms will be obsessed with processing top-performance heuristic functions. When the top 10 heuristics cannot obtain new heuristics surpassing the top 10 performances with one LLM-based operation on heuristics, the evolution of heuristics will trap into local optima. 

32 

**Monte Carlo Tree Search for Comprehensive Exploration in LLM-Based Automatic Heuristic Design** 



<!-- Start of picture text -->
Expansion , i.e., MCTS Links Evolution of  Step-by-step Constrction heuristics for TSP<br>MCTS nodes<br>The performance range of the<br>Top10 Heuristics<br>Expansion: t = 985,<br>Action: s1,       g(·): -6.27814.<br>Code:...<br>Expansion: t = 611,        Action: m2,       g(·): -6.305. Description: ...<br>Code:...<br>Description: ...<br>Expansion: t = 502,        Action: e2,       g(·): -6.36016.<br>Code: Expansion: t = 784,<br>MCTS-Root(Virtual) def select_next_node(current_node, destination_node, unvisited_nodes, distance_matrix):    scaling_factor, constant_penalty, bias_factor = 0.5, 2, 0.4    average_distance = sum(distance_matrix[current_node][node] for node in unvisited_nodes) / len(unvisited_nodes) if unvisited_nodes else 0    connectivity_scores = {node: sum(distance_matrix[node][other_node] for other_node in unvisited_nodes if node != other_node) for node in unvisited_nodes}    def adjusted_cost(node):        immediate_cost = distance_matrix[current_node][node]        distance_to_destination = distance_matrix[node][destination_node]        connectivity_penalty = scaling_factor * (len(unvisited_nodes) - connectivity_scores[node]) / len(unvisited_nodes)        penalty = 0.5 * (immediate_cost + average_distance)        return immediate_cost + penalty + constant_penalty + connectivity_penalty - (bias_factor * distance_to_destination)    return min(unvisited_nodes, key=adjusted_cost, default=None)Description: ... Code:def select_next_node(current_node, destination_node, unvisited_nodes, distance_matrix):    scaling_factor, constant_penalty, bias_factor = 0.6, 0.5, 0.7    average_distance = sum(distance_matrix[current_node][node] for node in unvisited_nodes) / len(unvisited_nodes) if unvisited_nodes else 0    connectivity_scores = {node: sum(distance_matrix[node][other_node] for other_node in unvisited_nodes if node != other_node) for node in unvisited_nodes}    def adjusted_cost(node):        immediate_cost = distance_matrix[current_node][node]        distance_to_destination = distance_matrix[node][destination_node]        connectivity_penalty = scaling_factor * (len(unvisited_nodes) - connectivity_scores[node]) / len(unvisited_nodes)        penalty = 0.3 * (immediate_cost + average_distance)        return immediate_cost + penalty + constant_penalty + connectivity_penalty - (bias_factor * distance_to_destination)    return min(unvisited_nodes, key=adjusted_cost, default=None)Description: ...Action: m2,       g(·): -6.45066 Expansion: t = 810, Action: m2,       g(·): -6.311.Code:...Description: ...<br>Expansion: t = 996,        Action: s1,       g(·): -6.26859.<br>Expansion: t = 122,        Action: e1,       g(·): -7.18502.Code:def select_next_node(current_node, destination_node, unvisited_nodes, distance_matrix):    connectivity_scores = {node: sum(distance_matrix[node][other_node] for other_node in unvisited_nodes if node != other_node) for node in unvisited_nodes}    def total_cost(node):        travel_cost = distance_matrix[current_node][node]        connectivity_penalty = (len(unvisited_nodes) - connectivity_scores[node]) / len(unvisited_nodes)        return travel_cost + connectivity_penalty    return min(unvisited_nodes, key=total_cost, default=None)Description: ... Expansion: t = 528,        Action: m2,       g(·): -6.52703.Code:def select_next_node(current_node, destination_node, unvisited_nodes, distance_matrix):    scaling_factor, constant_penalty, bias_factor = 0.7, 3, 0.5    average_distance = sum(distance_matrix[current_node][node] ** 2 for node in unvisited_nodes) / len(unvisited_nodes) if unvisited_nodes else 0    connectivity_scores = {node: sum(distance_matrix[node][other_node] ** 2 for other_node in unvisited_nodes if node != other_node) for node in unvisited_nodes}    def adjusted_cost(node):        immediate_cost = distance_matrix[current_node][node]        distance_to_destination = distance_matrix[node][destination_node]        connectivity_penalty = scaling_factor * (len(unvisited_nodes) - connectivity_scores[node]) / len(unvisited_nodes)        penalty = 0.75 * (immediate_cost ** 2 + average_distance)        return immediate_cost + penalty + constant_penalty + connectivity_penalty - (bias_factor * distance_to_destination ** 2)    return min(unvisited_nodes, key=adjusted_cost, default=None)Description: ... Code:def select_next_node(current_node, destination_node, unvisited_nodes, distance_matrix):    scaling_factor, constant_penalty, bias_factor = 0.7, 0.4, 0.5    average_distance = calculate_average_distance(unvisited_nodes, current_node, distance_matrix)    connectivity_scores = calculate_connectivity_score(unvisited_nodes, distance_matrix)    min_total_cost, next_node = float('inf'), None    for node in unvisited_nodes:        immediate_cost = distance_matrix[current_node][node]        distance_to_destination = distance_matrix[node][destination_node]        remaining_unvisited = unvisited_nodes - {node}        mst_cost = minimum_spanning_tree(remaining_unvisited, distance_matrix) if remaining_unvisited else 0        connectivity_penalty = scaling_factor * (len(unvisited_nodes) - connectivity_scores[node]) / len(unvisited_nodes)        penalty = 0.4 * (immediate_cost + average_distance + mst_cost)        adjusted_cost = immediate_cost + penalty + constant_penalty + connectivity_penalty - (bias_factor * distance_to_destination)        if adjusted_cost < min_total_cost:            min_total_cost, next_node = adjusted_cost, node    return next_nodeDescription: ...<br>0 Evolution Steps 1000<br>0.1 Exploration<br>�0<br>Exploitation<br>0<br>Exploration Decay<br>(a) An Example of MCTS-AHD Evolution on Designing Step-by-step Construction Heuristics for TSP<br>Expansion , i.e., MCTS Links Evolution of  Step-by-step Constrction heuristics for KP<br>MCTS nodes<br>The performance range of the<br>Top10 Heuristics<br>Expansion: t = 414,        Action: e1,       g(·): 40.17773.<br>Code:def select_next_node(current_node, destination_node, unvisited_nodes, distance_matrix):    scaling_factor, constant_penalty, bias_factor = 0.5, 2, 0.4    average_distance = sum(distance_matrix[current_node][node] for node in unvisited_nodes) / len(unvisited_nodes) if unvisited_nodes else 0    connectivity_scores = {node: sum(distance_matrix[node][other_node] for other_node in unvisited_nodes if node != other_node) for node in unvisited_nodes}    def adjusted_cost(node):        immediate_cost = distance_matrix[current_node][node]        distance_to_destination = distance_matrix[node][destination_node]        connectivity_penalty = scaling_factor * (len(unvisited_nodes) - connectivity_scores[node]) / len(unvisited_nodes)        penalty = 0.5 * (immediate_cost + average_distance)        return immediate_cost + penalty + constant_penalty + connectivity_penalty - (bias_factor * distance_to_destination)    return min(unvisited_nodes, key=adjusted_cost, default=None)Description: ... Expansion: t = 694,  Action: s1,   g(·): 40.17621.Code:import numpy as npdef select_next_item(remaining_capacity, weights, values):    n = len(weights)    best_value, result = float('-inf'), -1    weight_per_value = weights / values      # Calculate weight-to-value ratios and sort items    items_sorted = sorted(range(n), key=lambda i: (weight_per_value[i], weights[i]))    for index in items_sorted:        if weights[index] <= remaining_capacity:            total_value, total_weight = values[index], weights[index]            for next_index in items_sorted:                if next_index != index and total_weight + weights[next_index] <= remaining_capacity:                    total_value += values[next_index]                    total_weight += weights[next_index]            total_value -= total_weight / (total_value + 1) if total_weight > 0 else 0            if total_value > best_value:                best_value, result = total_value, index    return resultDescription: ...<br>MCTS-Root<br>(Virtual) Expansion: t = 892,        Action: e2,       g(·): 40.17971.<br>Expansion: t = 580,        Action: e2,       g(·): 40.13461.Code:import numpy as npdef select_next_item(remaining_capacity, weights, values):    n = len(weights)    best_value, result = float('-inf'), -1    # Calculate value-to-weight ratios and sort items    value_per_weight = values / weights    items_sorted = sorted(range(n), key=lambda i: (-value_per_weight[i], weights[i]))    for index in items_sorted:        if weights[index] <= remaining_capacity:            total_value, total_weight = values[index], weights[index]            for next_index in items_sorted:                if next_index != index and total_weight + weights[next_index] <= remaining_capacity:                    total_value += values[next_index]                    total_weight += weights[next_index]            total_value -= (total_weight ** 2) / (total_value + 1) if total_weight > 0 else 0            if total_value > best_value:                best_value, result = total_value, index Code:import numpy as npdef select_next_item(remaining_capacity, weights, values):    n = len(weights)    best_value, result = float('-inf'), -1    # Calculate penalty-adjusted scores    penalty_scores = np.array(values) / (np.array(weights) + np.log(np.array(weights) + 1))    penalty_scores *= remaining_capacity / np.maximum(weights, 1)    # Sort items by penalty-adjusted scores    items_sorted = sorted(range(n), key=lambda i: (-penalty_scores[i], weights[i]))    for index in items_sorted:        if weights[index] <= remaining_capacity:            total_value, total_weight = values[index], weights[index]            for next_index in items_sorted:                if next_index != index and total_weight + weights[next_index] <= remaining_capacity:                    total_value += values[next_index]                    total_weight += weights[next_index]            total_value -= total_weight / (total_value + 1) if total_weight > 0 else 0            if total_value > best_value:                best_value, result = total_value, index    return result<br>    return result Description: ...<br>Description: ...<br>0 Evolution Steps 1000<br>0.1 Exploration<br>�0<br>Exploitation<br>0<br>Exploration Decay<br>(b) An Example of MCTS-AHD Evolution on Designing Step-by-step Construction Heuristics for KP<br>Performances g(·)<br>Performances g(·)<br><!-- End of picture text -->

_Figure 6._ Two examples of the heuristic evolution process of MCTS-AHD. We provide the performance function value _g_ ( _·_ ) of the heuristic function within each MCTS tree node. The ”Action” in each node represents one of the six actions of expanding this node. Codes are simplified by OpenAI _GPT_ to reduce the space occupations. 

33 

**Monte Carlo Tree Search for Comprehensive Exploration in LLM-Based Automatic Heuristic Design** 

# **H. Baselines & Licenses** 

**For the optimal value** in Table 1 and Table 8. We run LKH3 for TSP instances with adopting the commonly used setting in NCO methods (Kool et al., 2018). We set the LKH parameters RUNS = 10 and MAX ~~T~~ RAILS = 1,0000. For KP instances, we use Google OR-Tools for the optimal value. 

**For manually designed heuristics with general frameworks** , this paper includes Greedy Construct, the ACO algorithm (Dorigo et al., 2006), the KGLS algorithm (Arnold & Sorensen¨ , 2019), and EI (Mockus, 1974), EIpu (Snoek et al., 2012), EI-cools (Lee et al., 2020a) for the CAF design task in BO. We implement KGSL by setting the heuristic matrix to the distance matrix, using the implementation of ACO in DeepACO (Ye et al., 2024b), and use the results reported in Yao et al. (2024c) for EI, EIpu, and EI-cools. 

**For NCO baselines** , this article implements POMO (Kwon et al., 2020), DeepACO (Ye et al., 2024b), VRP-DACT (Ma et al., 2021), and NeuOpt ( **?** ). For a fair comparison, in Table 1, the reported POMO solutions are from a single start and generated without augmentations. The maximum operation on a solution is set to _T_ = 1200 for VRP-DACT and NeuOpt. 

**For AHD baselines** , in TSPLib, we adopt the results of GHPP reported in (Duflo et al., 2019). 

**For LLM-based AHD baselines** , this article considers Funsearch (Romera-Paredes et al., 2024), EoH (Liu et al., 2024b), ReEvo (Ye et al., 2024a), and HSEvo (Dat et al., 2024), we follow all their parameter settings in evolutions (e.g., setting population size _M_ = 20 for online BPP and _M_ = 10 for other tasks). We try not to introduce too much external expert information. However, in implementations, Funsearch needs to maintain 10 relatively independent multiple populations from a certain inferior seed heuristic function. ReEvo relies more on the seed heuristic function, and the ReEvo method will become unavailable when all individuals in the elite population have the same objective function value. So, in some application scenarios (e.g., step-by-step construction for the KP task), it is too hard to find a good seed heuristic function that ensures the availability of the algorithm while trying not to provide too much external knowledge. 

In experiments, we use the same seed functions for baselines (Funsearch, ReEvo, and HSEvo), using seed functions proposed in Ye et al. (2024a) for ACO frameworks and GLS frameworks, random selection functions for step-by-step constructing TSP and ASP, and the best-known function proposed in Romera-Paredes et al. (2024) for online BPP. The proposed MCTS-AHD, exhibits better applicability and superior performance in most application scenarios, without the requirement of seed function design. In our seed function settings, ReEvo and its follow-up method HSEvo are not available in some application scenarios (e.g., KP, ACO), where we do not report their effects. 

## **H.1. License** 

The licenses and URL of baselines are listed in Table 15. 

|||_Table_|_15._ A s|ummaryof licenses.|
|---|---|---|---|---|
|Resources|Type|License|URL||
|LKH3|Code|Available for academic research use|http://|webhotel4.ruc.dk/˜keld/research/LKH-3/|
|OR-Tools|Code|MIT License|https:/|/developers.google.com/optimization/pack/knapsack?hl=zh-cn|
|POMO|Code|Available online|https:/|/github.com/yd-kwon/POMO/tree/master|
|DeepACO|Code|MIT License|https:/|/github.com/henry-yeh/DeepACO|
|VRP-DACT|Code|MIT License|https:/|/github.com/yining043/VRP-DACT|
|NeuOpt|Code|MIT License|https:/|/github.com/yining043/NeuOpt|
|Funsearch|Code|Apache License|https:/|/github.com/google-deepmind/funsearch|
|EoH|Code|MIT License|https:/|/github.com/FeiLiu36/EoH/tree/main|
|ReEvo|Code|MIT License|https:/|/github.com/ai4co/reevo|
|HSEvo|Code|Available online|https:/|/github.com/datphamvn/HSEvo|
|Synthetic problem|s Dataset|Available Online|https:/|/github.com/FeiLiu36/EoH/tree/main/examples/user_bo_caf|
|TSPLib|Dataset|Available for anynon-commercial use|http://|comopt.ifi.uni-heidelberg.de/software/TSPLIB95|



34 

