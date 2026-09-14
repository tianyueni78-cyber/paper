**PathWise: Planning through World Model for Automated Heuristic Design via Self-Evolving LLMs** 

**Oguzhan Gungordu**<sup>1</sup> **Siheng Xiong**<sup>1</sup> **Faramarz Fekri**<sup>1</sup> 

# **Abstract** 

Large Language Models (LLMs) have enabled automated heuristic design (AHD) for combinatorial optimization problems (COPs), but existing frameworks’ reliance on fixed evolutionary rules and static prompt templates often leads to myopic heuristic generation, redundant evaluations, and limited reasoning about how new heuristics should be derived. We propose a novel multi-agent reasoning framework, referred to as **P** l **a** nning **th** rough **W** orld Model for Automated Heurist **i** c Design via **S** elf- **E** volving LLMs (PathWise), which formulates heuristic generation as a sequential decision process over an _entailment graph_ serving as a compact, stateful memory of the search trajectory. This approach allows the system to carry forward past decisions and reuse or avoid derivation information across generations. A policy agent plans evolutionary actions, a world model agent generates heuristic rollouts conditioned on those actions, and critic agents provide routed reflections summarizing lessons from prior steps, shifting LLM-based AHD from trialand-error evolution toward state-aware planning through reasoning. Experiments across diverse COPs show that PathWise converges faster to better heuristics, generalizes across different LLM backbones, and scales to larger problem sizes. 

# **1. Introduction** 

Heuristic algorithms are central to solving COPs, which arise in many real-world complex decision-making tasks such as routing, scheduling, logistics, and design automation (Desale et al., 2015; Ma et al., 2019; Tam et al., 2024). Since many COPs are NP-hard, heuristics are often the only practical approach for obtaining high-quality solutions 

> 1Georgia Institute of Technology. Correspondence to: Oguzhan Gungordu _<_ ogungordu3@gatech.edu _>_ . 

_Proceedings of the 43_<sup>_rd_</sup> _International Conference on Machine Learning_ , Seoul, South Korea. PMLR 306, 2026. Copyright 2026 by the author(s). 



<!-- Start of picture text -->
−6.2 −9.0<br>−9.2<br>−6.4<br>−9.4<br>−6.6 −9.6<br>−9.8<br>−6.8<br>ReEvo −10.0 ReEvo<br>−7.0 HSEvoMCTS-AHD −10.2 HSEvoMCTS-AHD<br>PathWise (Ours) PathWise (Ours)<br>−7.2<br>0 100 200 300 400 500 600 700 800 900 1000 0 100 200 300 400 500 600 700 800 900 1000<br>Number of Evaluations on D Number of Evaluations on D<br>(a) TSP - Constructive (b) CVRP - ACO<br>Performance of Heuristics on D Performance of Heuristics on D<br><!-- End of picture text -->

_Figure 1._ Evolution curves of LLM-based AHD methods on (a) TSP and (b) CVRP under different search frameworks, showing best-so-far heuristic performance as a function of evaluation number for representative population-based and tree-based methods using GPT-4o-mini. PathWise is run with a limit of _ne_ = 500 evaluations while all baselines use _ne_ = 1000, yet achieves stronger performance with lower variance and faster convergence. 

within reasonable time, leading to the widespread adoption of methods such as simulated annealing, tabu search, and iterated local search (Kirkpatrick et al., 1983; Glover, 1990; Lourenc¸o et al., 2003). Despite their success, constructing effective heuristics remains manual, requiring substantial domain expertise to design solver-specific algorithmic components, making the process costly and difficult to generalize across problems (Choong et al., 2018; Pillay & Qu, 2018). To address these challenges, AHD has emerged as a framework for automatically generating heuristics for a given problem class, aiming to reduce dependence on expertcrafted designs and enabling systematic discovery through Genetic Programming (GP) (Burke et al., 2013; Langdon & Poli, 2013). However, GP-based AHD methods represent heuristics as syntax trees and rely on evolutionary operators confined to human-defined arithmetic operators, limiting their flexibility and effectiveness (Duflo et al., 2019). 

Recently, LLMs have shown capability in reasoning and code generation, opening new directions for AHD (Chen et al., 2021; Gandhi et al., 2023; Yang et al., 2024b). Given these capabilities, LLM-based AHD methods integrate LLMs into evolutionary search to automatically generate heuristics with minimal human intervention (Liu et al., 2023). Many approaches adopt population-based evolutionary procedures, where LLMs iteratively refine a population of candidate algorithms using evolutionary 

1 

**PathWise: Planning through World Model for Automated Heuristic Design via Self-Evolving LLMs** 

search (Chen et al., 2023; Meyerson et al., 2024). Early methods such as FunSearch (Romera-Paredes et al., 2023) and EoH (Liu et al., 2024a) employ LLM-guided operators to evolve high-performing heuristics, enabling fast heuristic search. ReEvo (Ye et al., 2024) further incorporates a reflection mechanism to analyze generated heuristics and guide search (Shinn et al., 2023). Following this, HSEvo (Dat et al., 2025) introduces diversity-aware population management and harmony search to improve population diversity (Shi et al., 2013). Beyond population-based approaches, tree-based methods have been explored (Wang et al., 2025a). Specifically, MCTS-AHD (Zheng et al., 2025) integrates LLMs with Monte Carlo Tree Search (MCTS), applying the UCT algorithm to guide selection and expansion of heuristic nodes in a tree structure to search the heuristic space (Swiechowski et al.<sup>´</sup> , 2023). 

However, existing LLM-based AHD methods are limited by how heuristic search is structured. Population-based approaches rely on fixed selection and replacement rules, which can lead to premature convergence by discarding intermediate heuristics. Tree-based methods, such as MCTSAHD, impose a hierarchical structure, but selection and expansion are driven by performance-based UCT criteria instead of semantic understanding of the search landscape or the relationships between heuristics. Exploration is guided by visitation statistics instead of distinctions between heuristic transformations, and node expansion follows a singlepath, with long training time. Overall, both populationbased and tree-based frameworks treat heuristic generation as isolated or statistically linked sampling steps and rely on fixed sets of operators or prompt templates that do not adapt to evolving search dynamics or different problem settings (van Stein et al., 2025). They lack a stateful, semantic representation of how heuristics are derived, how edits propagate across generations, or why modifications succeed or fail. This lack of memory and state-aware planning leads to redundant evaluations, similar heuristic rediscovery, and inefficient use of LLM calls (Liu et al., 2025d) (see Figure 1). 

To address these limitations, we propose **P** l **a** nning **th** rough **W** orld Model for Automated Heurist **i** c Design via **S** elf- **E** volving LLMs (PathWise), a _structured multi-agent reasoning framework_ formulating heuristic discovery as a sequential decision process over an _entailment graph_ (Dalvi et al., 2021; Xiong et al., 2025b). The entailment graph provides a compact, stateful representation of the search trajectory, capturing how heuristics are derived and how edits compose across generations, enabling memory and state-aware planning to guide heuristic evolution. 

We summarize our major contributions as follows. **(1)** We introduce a hybrid graph-based and population-based formulation of heuristic evolution, where an entailment graph encodes derivation rationale, parent information, and perfor- 

mance history, serving as a shared state through which the policy and world model interact to guide heuristic discovery. **(2)** We propose a coordinated multi-agent LLM framework where a policy agent controls high-level evolutionary strategy by generating evolutionary actions, including parent selection and derivation rationale, a world model executes these actions through low-level heuristic generation to update the entailment graph, and critic agents analyze graph structure and provide routed reflections that adapt the behavior of the policy and world model, enabling self-evolving, state-aware heuristic generation. **(3)** To ensure variety during heuristic generation, we introduce prompt-level diversity at the level of policy actions and world model rollouts, enabling broader exploration over the entailment graph. **(4)** Through extensive experiments across diverse COPs, we demonstrate that PathWise consistently discovers stronger heuristics using fewer evaluations, achieves faster convergence, and scales more effectively to larger problem sizes. 

# **2. Preliminaries** 

## **2.1. LLM-based AHD for Combinatorial Optimization** 

AHD considers a COP with instance space _X_ and solution space _S_ . A heuristic is an executable program _h ∈H_ that maps each instance to a feasible solution, _h_ : _X →S_ , where _x ∈X_ denotes a problem instance and _s_ = _h_ ( _x_ ) _∈S_ is the corresponding solution. A cost function _f_ : _S →_ R evaluates solution quality. For example, in the Traveling Salesman Problem, an instance provides distance matrix, the solution is a tour, and the cost is its total length. 

Performance is assessed over a distribution or dataset _D_ of instances using the expected negative cost 



so higher values of _P_ ( _h_ ; _D_ ) correspond to stronger heuristics. Under an evaluation budget, AHD aims to identify 



While the space _H_ encompasses diverse heuristics, searching for a full solver implementation from scratch is often inefficient. Instead, LLM-based AHD methods design a heuristic function _h_ within a chosen search framework. 

## **2.2. Structured Reasoning via Entailment Graphs.** 

We conceptualize heuristic discovery as multi-step reasoning for solving a search problem via the construction of an entailment graph _G_ = ( _V, E_ ). Each node _v ∈V_ represents a tuple ( _h, κ, d, P_ ( _h_ ; _D_ ) _,_ PM), consisting of heuristic code _h_ , a natural-language derivation rationale _κ_ used to generate _h_ , a natural-language algorithmic description _d_ , performance _P_ ( _h_ ; _D_ ), and compact parent metadata PM. Each directed 

2 

**PathWise: Planning through World Model for Automated Heuristic Design via Self-Evolving LLMs** 



(a) Population-based search combined with entailment-graph reasoning at outer iteration _r_ . The graph _Gt_ = ( _Vt, Et_ ) expands over inner steps _t_ starting from population _Pr_ , where new nodes are derived from selected parents and added to the graph. The next population _Pr_ +1 is formed from nodes generated in _r_ . 



(b) Illustration of an entailment step. The policy agent proposes actions, the world model generates rollouts, and critic agents analyze the resulting outputs at step _t_ to produce reflections conditioning agents at step _t_ +1. 

_Figure 2._ Overview of _PathWise_ . (a) AHD is orchestrated across two timescales, with inner entailment steps within each outer iteration; example shown with _Np_ = 4 (parent metadata in nodes omitted for simplicity). (b) Entailment step showing policy and world model interaction with critics, carrying forward lessons to guide heuristic generation; illustrated at _t_ = 1 resulting in the entailment of _v_ 6. 

edge _e ∈E_ connects a parent set _S_ to the child node _v_ , encoding _how_ the heuristic was derived from its parents. The entailment graph enables conditioning future decisions on derivation history rather than independent steps, providing a structured memory of the search process. 

the current state _st_ , and _κ_ is a natural-language _derivation rationale_ generated by the policy (Figure 2(b)). Rather than selecting from a fixed set of rigid operators, _κ_ specifies how the selected heuristics should be transformed or combined to generate a child heuristic. 

## **2.3. Sequential Decision View of Heuristic Evolution** 

We formulate the heuristic discovery as a sequential Markov Decision Process (MDP) rather than a stateless evolutionary algorithm. The search iteratively constructs an _entailment graph_ and is represented as (S _,_ A _,_ T _,_ R), where: 

   - **Transition** T **.** The transition T( _st, at_ ) corresponds to an entailment step (Figure 2(a)) resulting in _st_ +1. Given ( _S, κ_ ), the world model generates a new heuristic _h_ and its algorithmic description _d_ , inserts a corresponding node into the entailment graph, and adds an edge recording derivation from _S_ under directive _κ_ . 

- **State** S **.** The state _st ∈_ S corresponds to the current _entailment graph_ with its active frontier of nodes available for selection (Figure 2(a)). This structured state encodes how existing heuristics were derived, providing a compact, stateful memory of the search trajectory without requiring access to the entire search history. 

- **Action** A **.** An action _at ∈_ A is defined as a tuple ( _S, κ_ ), where _S ⊆ st_ is a set of nodes selected from 

- **Reward** R **.** The reward function R( _st, at_ ) measures the quality of action _at_ given state _st_ and generated heuristics (Figure 2(b)). It serves as a signal for evolving agents, which translate performance values into natural-language feedback for the next step. 

PathWise is training-free in the sense that no LLM parameters are updated. The MDP formulation serves as a structural backbone for state-aware planning, where the policy and 

3 

**PathWise: Planning through World Model for Automated Heuristic Design via Self-Evolving LLMs** 

world model are reinforced through natural-language reflections from critic agents rather than gradient-based policy optimization. Following (Hao et al., 2023), we use the term _world model_ to denote an LLM that predicts the next state given the current state and action through its pretrained knowledge, distinct from learned-dynamics models. 

# **3. Methodology** 

PathWise orchestrates heuristic discovery across two timescales using a _hybrid graph-based and populationbased_ approach (Figure 2(a)). The _outer loop_ , indexed by _r_ , maintains a population _Pr_ of root nodes of size _Np_ . Initial population _P_ 0 is formed by prompting an LLM with an initialization prompt to generate _Np_ candidates. Within each outer iteration, an _inner loop_ , indexed by _t_ , explores the local search space by incrementally constructing an entailment graph _Gt_ rooted at _Pr_ . At each inner step, the entailment graph is expanded through an entailment operation that derives a new node from its selected parent nodes while recording the corresponding derivation relationship. Each entailment operation is realized by coordinated LLM agents that jointly perform planning, code synthesis, and reflective feedback (Figure 2(b)), with their roles and interaction detailed in the remainder of this section. 

Unlike population-based evolutionary methods that discard intermediate results, derivation history is retained in the graph structure, compressing the search trajectory. Additionally, unlike tree-based approaches that preserve all generated heuristics and require selecting among ever-growing candidate sets, the population mechanism restricts exploration to a compact set of root nodes at each outer iteration. 

node _v⋆_ and transitions from _Gt_ to _Gt_ +1. This operation is represented by a directed edge _S_ = _⇒κ v⋆_ , indicating that the parent set _S ⊆ st_ entails _v⋆_ under derivation rationale _κ_ . To control search complexity, the state is updated after each entailment step according to _st_ +1 = ( _st ∪{v⋆}_ ) _\_ ( _S_<sup>(</sup><sup>_i⋆_)</sup> _\ {v_<sup>_⋆_</sup> _}_ ), where the newly entailed node _v⋆_ is added, the parent nodes used in the selected entailment are removed, and the global best node _v_<sup>_⋆_</sup> is retained. This update rule balances exploration via entailment, exploitation via the retained global best, and complexity control via pruning of used parent nodes, keeping the state compact. 

## **3.2. Multi-Agent Entailment Step.** 

PathWise employs coordinated LLM agents for heuristic discovery, interacting through a cycle of planning, execution, and reflection to navigate the entailment graph construction. A _Policy Agent_ **_π_ p** observes state _st_ and proposes actions by selecting a parent set _S_ and formulating a derivation rationale _κ_ . A _World Model Agent_ **_π_ wm** executes each action by generating heuristic rollouts. Two critic agents guide this process: a _Policy Critic_ **_π_ p** **~~c~~ ritic**<sup>reflects on evolutionary</sup> strategy, and a _World Model Critic_ **_π_ wm** **~~c~~ ritic**<sup>reflects on</sup> heuristic generation quality. Their feedback guides stateaware planning over the entailment graph, as illustrated in Figure 2(b). We sample _Na_ actions per inner step and generate _Nw_ heuristic rollouts per action to insert a single entailed node _v⋆_ into the entailment graph. The prompt templates used by agents are provided in Appendix F.1 

**Policy Agent Sampling.** The Policy Agent **_π_ p** acts as the high-level planner. Conditioned on the current state _st_ and the routed policy reflection _ρp_ ( _t_ ), it samples _Na_ candidate entailment actions _{a_<sup>(</sup> _t_<sup>_i_)</sup><sup>_}N_</sup> _i_ =1<sup>_a_according to</sup> 

## **3.1. Entailment Graph Construction** 

**State Representation.** We denote the entailment graph at inner step _t_ as _Gt_ = ( _Vt, Et_ ). At the start of each inner loop, the graph is initialized with the current population of root nodes, setting _s_ 0 = _V_ 0 = _Pr_ and _E_ 0 = _∅_ . As entailment proceeds, each newly generated node _v_ at step _t_ , derived from a parent set _S ⊆ st_ , is represented by a tuple ( _h, κ, d, P_ ( _h_ ; _D_ ) _,_ PM). The parent metadata PM provides a compressed summary of the parent set _S_ , and is defined as PM = _{_ ( _dk, P_ ( _hk_ ; _D_ )) _| vk ∈ S}_ , recording compact algorithmic descriptions and performance values of the parent heuristics. This compressed representation allows the model to condition on how a heuristic was derived and on the relative performance of its parents, without including full parent code in the context, thereby minimizing context usage when prompting LLMs. 

**Entailment and State Transition.** The entailment graph is incrementally constructed through a sequence of entailment operations. At each inner step _t_ , the system entails a new 



Each action _a_<sup>(</sup> _t_<sup>_i_)</sup> = ( _S_<sup>(</sup><sup>_i_)</sup> _, κ_<sup>(</sup><sup>_i_)</sup> ) consists of a parent set _S_<sup>(</sup><sup>_i_)</sup> _⊆ st_ and a natural-language directive _κ_<sup>(</sup><sup>_i_)</sup> that specifies how the selected heuristics should be modified or combined. For each action, the parent metadata is defined from the selected parent nodes as PM<sup>(</sup><sup>_i_)</sup> = _{_ ( _dk, P_ ( _hk_ ; _D_ )) _| vk ∈ S_<sup>(</sup><sup>_i_)</sup> _}_ . This action design enables the policy to operate at a semantic level, reasoning over evolutionary strategy. Consequently, the policy can dynamically invent new operator types through _κ_<sup>(</sup><sup>_i_)</sup> and adapt its edit strategy to the evolving search landscape, instead of using fixed operator templates. 

**World Model Rollouts.** The World Model Agent **_π_ wm** acts as a low-level executor that translates the policy’s highlevel actions into code-level heuristics. For each policygenerated action _a_<sup>(</sup> _t_<sup>_i_),itgenerates</sup><sup>_Nw_candidaterollouts</sup> _{_ ( _h_<sup>ˆ(</sup><sup>_i,j_)</sup> _, d_<sup>ˆ(</sup><sup>_i,j_)</sup> ) _}_<sup>_N_</sup> _j_ =1<sup>_w_conditioned on the selected parents, the</sup> 

4 

**PathWise: Planning through World Model for Automated Heuristic Design via Self-Evolving LLMs** 



Each heuristic rollout is evaluated on _D_ , and the bestperforming candidate ( _i⋆, j⋆_ ) = arg max _i,j P_ ( _h_<sup>ˆ(</sup><sup>_i,j_)</sup> ; _D_ ) is selected. We denote the corresponding heuristic and its algorithmic description as _h⋆_ = _h_<sup>ˆ(</sup><sup>_i⋆,j⋆_)</sup> and _d⋆_ = _d_<sup>ˆ(</sup><sup>_i⋆,j⋆_)</sup> . The heuristic is inserted into the entailment graph as an entailed node _v⋆_ = ( _h⋆, κ_<sup>(</sup><sup>_i⋆_)</sup> _, d⋆, P_ ( _h⋆_ ; _D_ ) _,_ PM<sup>(</sup><sup>_i⋆_)</sup> ) and added via the edge _S_<sup>(</sup><sup>_i⋆_)</sup> ===<sup>_κ_(</sup><sup>_i⋆_</sup> _⇒_<sup>)</sup> _v⋆_ , yielding _Vt_ +1 _← Vt ∪{v⋆}_ and _Et_ +1 _← Et ∪{S_<sup>(</sup><sup>_i⋆_)</sup> ===<sup>_κ_(</sup><sup>_i⋆_</sup> _⇒_<sup>)</sup> _v⋆}_ . It extends the graph and conditions subsequent policy and world model decisions. 

## **3.3. Diversity in Policy and World Model Rollouts** 

A key bottleneck in PathWise occurs when, at an inner step _t_ , the policy and world model produce low-diversity outputs, resulting in similar parent selections, directives, and heuristic rollouts. When the policy repeatedly selects the same parent sets with similar directives and the world model generates nondiverse rollouts, the critic agents observe little contrast and cannot generate informative reflections. To address this, we introduce two diversity mechanisms that operate at the prompt level and deliberately alter the posterior distributions of **_π_ p** and **_π_ wm** without modifying the underlying graph topology. 

**Diversity-Aware Prompt Perturbation.** To encourage diverse sampling from both agents, we introduce a promptlevel perturbation mechanism controlled by a time-varying exploration rate _ε_ ( _ℓ_ ). Each agent is associated with a rolespecific inventory of exploratory phrases, Φp and Φwm, designed to diversify action proposals and heuristic rollout generation. The exploration rate decays linearly with evaluation count _ℓ ∈{_ 0 _, . . . , ne}_ , with _ε_<sup>init</sup> = 0 _._ 5 and _ε_<sup>final</sup> = 0 _._ 25: 



During sampling, the prompts for **_π_ p** and **_π_ wm** are perturbed by sampling _ϕ_<sup>(</sup><sup>_i_)</sup> _∼_ Φp and _ψ_<sup>(</sup><sup>_i,j_)</sup> _∼_ Φwm with probability _ε_ ( _ℓ_ ), respectively. These perturbations reshape the sampling distributions, promoting broader exploration early in search and more focused refinement later. The full phrase inventories are provided in Appendix F.2. 

**State Shuffling.** To reduce positional bias, where LLMs tend to select parents appearing earlier in the context window (Li et al., 2024; Schilcher et al., 2025; Bito et al., 2025), we randomly permute the order of nodes in _st_ before prompting **_π_ p** and **_π_ p** **~~c~~ ritic**<sup>,encouragingparentselectiontobe</sup> driven by semantic suitability rather than positional effects. 

## **3.4. Critic Models and Routed Reflections** 

We employ two critic agents, **_π_ p critic**<sup>and</sup><sup>**_π_**</sup> **wm** **~~c~~ ritic**<sup>, to</sup> synthesize verbal gradients (Shinn et al., 2023; Madaan 

et al., 2023) from the outputs generated by the agents at step _t_ . Based on these outputs, the critics generate routed reflections that condition the policy and world model at step _t_ +1, enabling state-aware adaptation over the entailment graph without updating LLM parameters. 

**Policy Critic (** **_π_ p** **~~c~~ ritic**<sup>**).**The policy critic reflects on the</sup> evolutionary strategy induced by the actions generated by the policy. For each action _a_<sup>(</sup> _t_<sup>_i_),itaggregatestheperfor-</sup> mance values of the associated heuristic rollouts into 



which summarizes action effectiveness and serves as a reward signal to _rank_ actions. Together with a per-action rollout descriptor bundle _Bp_<sup>(</sup><sup>_i_)</sup> = _{_ ( _d_<sup>ˆ(</sup><sup>_i,j_)</sup> _, P_ ( _h_<sup>ˆ(</sup><sup>_i,j_)</sup> ; _D_ )) _}_<sup>_N_</sup> _j_ =1<sup>_w_,</sup> which compactly captures variation across rollouts, the critic produces a policy reflection 



By analyzing how different derivation rationales and parent selections interact with the current topology and performance landscape, the policy critic injects routed feedback to **_π_ p** to adjust its strategy at step _t_ +1. 

**World Model Critic (** **_π_ wm critic**<sup>**).**The world model critic</sup> reflects on code-synthesis quality by contrasting the bestperforming heuristic rollout with the worst-performing one. The index of the worst-performing rollout is identified as ( _i_ min _, j_ min) = arg min _i,j P_ ( _h_<sup>ˆ(</sup><sup>_i,j_)</sup> ; _D_ ). Using the best-performing rollout ( _i⋆, j⋆_ ) and the corresponding worst-performing rollout, we form the comparison tuples **best** = ( _h_<sup>ˆ(</sup><sup>_i⋆,j⋆_)</sup> _, d_<sup>ˆ(</sup><sup>_i⋆,j⋆_)</sup> _, P_ ( _h_<sup>ˆ(</sup><sup>_i⋆,j⋆_)</sup> ; _D_ )) and **worst** = ( _h_<sup>ˆ(</sup><sup>_i_min</sup><sup>_,j_min)</sup> _, d_<sup>ˆ(</sup><sup>_i_min</sup><sup>_,j_min)</sup> _, P_ ( _h_<sup>ˆ(</sup><sup>_i_min</sup><sup>_,j_min)</sup> ; _D_ )). Using these inputs, the critic produces a routed reflection 



This world model reflection _ρwm_ conditions **_π_ wm** at step _t_ +1, guiding its code-synthesis through heuristic contrast. 

## **3.5. Evolutionary Cycle and Population Management** 

The inner entailment graph expansion runs until either the maximum number of entailment steps _I_ max is reached or no further entailment actions are possible (i.e., the frontier _st_ collapses to a single node). Upon completion of the inner loop at its final step _t_<sup>_′_</sup> _∈{_ 1 _, . . . , I_ max _−_ 1 _}_ , the resulting entailment graph _Gt′_ captures the trajectory explored during the inner loop. The population _Pr_ +1 for the next outer iteration is then formed using a _leaf-first selection strategy_ . 

Let _F_ = LeafNodes( _Gt_<sup>_′_</sup> ) denote the set of leaf nodes with no outgoing edges that involved in at least one entailment 

5 

**PathWise: Planning through World Model for Automated Heuristic Design via Self-Evolving LLMs** 

_Table 1._ Comparison of methods designing step-by-step construction heuristics on TSP and KP (7 test sets, 250 instances each). LKH3 (Helsgaun, 2017) and OR-Tools (Perron & Furnon, 2025) provide optimal baselines for TSP and KP, respectively. We report mean performance over 3 runs for each LLM-based AHD method. The best-performing method for each LLM is shaded, and each test set’s overall best result is shown in bold. Entries marked “N/A” indicate that the method was not available for that task. 

|Task|||T|SP||||||K|P||||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Test sets|_N_|=50|_N_=|100|_N_=|200|_N_=50,|_W_=12_._5|_N_=100,|_W_=25|_N_=200,|_W_=25|_N_=500|,_W_=25|
|Methods|Obj._↓_|Gap|Obj._↓_|Gap|Obj._↓_|Gap|Obj._↑_|Gap|Obj._↑_|Gap|Obj._↑_|Gap|Obj._↑_|Gap|
|Optimal|5.687|-|7.767|-|10.709|-|20.089|-|40.254|-|57.132|-|90.763|-|
|Greedy Construct|6.992|22.95%|9.702|24.91%|13.430|25.41%|20.033|0.28%|40.205|0.12%|57.079|0.09%|90.712|0.06%|
|POMO|**5.711**|**0.42%**|**8.028**|**3.36%**|13.014|21.52%|19.669|2.09%|39.626|1.56%|56.909|0.39%|87.931|3.12%|
||||||LLM-|based AHD|:_GPT-4o_|_-mini_|||||||
|Funsearch|6.452|13.45%|9.050|16.52%|12.806|19.58%|20.037|0.26%|40.190|0.16%|57.035|0.17%|90.110|0.72%|
|EoH|6.602|16.09%|9.179|18.18%|12.853|20.02%|20.043|0.23%|40.198|0.14%|57.035|0.17%|90.173|0.65%|
|ReEvo|6.457|13.54%|9.033|16.30%|12.667|18.28%|N/A|N/A|N/A|N/A|N/A|N/A|N/A|N/A|
|HSEvo|6.429|13.05%|8.903|14.63%|12.359|15.41%|N/A|N/A|N/A|N/A|N/A|N/A|N/A|N/A|
|MCTS-AHD|6.358|11.80%|8.839|13.80%|12.403|15.82%|20.035|0.27%|40.206|0.12%|57.020|0.20%|89.061|1.88%|
|PathWise(Ours)|6.245|9.81%|8.758|12.76%|12.276|14.63%|20.046|0.21%|40.216|0.09%|57.082|0.09%|90.719|0.05%|
|||||LLM|-based A|HD:_GPT-5_|_-nano_ (re|asoning: l|ow)||||||
|Funsearch|6.389|12.35%|8.941|15.12%|12.701|18.60%|20.037|0.26%|40.173|0.20%|57.035|0.17%|90.609|0.17%|
|EoH|6.380|12.19%|8.920|14.85%|12.541|17.11%|20.043|0.23%|40.182|0.18%|57.046|0.15%|90.609|0.17%|
|ReEvo|7.287|28.13%|10.115|30.23%|14.083|31.51%|N/A|N/A|N/A|N/A|N/A|N/A|N/A|N/A|
|HSEvo|6.346|11.59%|8.792|13.20%|12.223|14.14%|N/A|N/A|N/A|N/A|N/A|N/A|N/A|N/A|
|MCTS-AHD|6.383|12.24%|8.814|13.48%|12.254|14.43%|20.042|0.23%|40.215|0.10%|57.081|0.09%|90.651|0.12%|
|PathWise(Ours)|6.202|9.06%|8.620|10.98%|12.132|13.29%|20.044|0.22%|40.217|0.09%|57.081|0.09%|90.724|0.04%|
|||||LLM-b|ased AHD|:_GPT-5-n_|_ano_ (reas|oning: me|dium)||||||
|Funsearch|6.321|11.15%|8.761|12.80%|12.159|13.54%|20.039|0.25%|40.190|0.16%|57.041|0.16%|90.627|0.15%|
|EoH|6.354|11.73%|8.809|13.41%|12.222|14.12%|20.045|0.22%|40.215|0.10%|57.051|0.14%|90.654|0.12%|
|ReEvo|6.284|10.50%|8.848|13.92%|12.463|16.38%|N/A|N/A|N/A|N/A|N/A|N/A|N/A|N/A|
|HSEvo|6.274|10.32%|8.744|12.58%|12.178|13.72%|N/A|N/A|N/A|N/A|N/A|N/A|N/A|N/A|
|MCTS-AHD|6.238|9.69%|8.694|11.94%|12.148|13.44%|20.043|0.23%|40.212|0.10%|57.080|0.09%|90.674|0.10%|
|PathWise(Ours)|6.165|8.41%|8.687|11.85%|**12.009**|**12.14%**|**20.073**|**0.08%**|**40.239**|**0.04%**|**57.109**|**0.04%**|**90.742**|**0.02%**|



step. Define _R_ = ( _Vt′ ∪ Vt_<sup>disc</sup><sup>_′_</sup> ) _\ F_ , where _Vt_<sup>disc</sup><sup>_′_</sup> contains all nodes evaluated but not entailed during the inner loop. Thus, _R_ consists of nodes that are not leaves of _Gt′_ . 

Population management prioritizes _F_ based on performance: 



By carrying forward both high-performing heuristics and the structurally informative leaf nodes, the outer loop forms the next population from the best individuals while retaining the contextual structure captured during entailment. 

# **4. Experiments** 

We evaluate the performance of PathWise on complex optimization tasks, focusing on NP-hard COPs. For our experimental evaluation, PathWise is applied to design heuristic functions within three search frameworks: the step-by-step constructive framework, Ant Colony Optimization (ACO), and Guided Local Search (GLS). Detailed framework definitions and configurations are provided in Appendix C. Our code is publicly available at https: //github.com/oguzhangungordu/PathWise. 

**Benchmarks.** PathWise is evaluated across diverse problem domains and search spaces using the following benchmarks: Traveling Salesman Problem (TSP), Knapsack Problem (KP), Capacitated Vehicle Routing Problem (CVRP), 

Multiple Knapsack Problem (MKP), Orienteering Problem (OP), and Bin Packing Problem (BPP; including both offline and online variants). Details of the problem definitions and dataset construction procedures are provided in Appendix B. 

**Experimental Settings.** Parameters of PathWise balance search depth and exploration. In experiments, we set _Na_ = 2, _Nw_ = 2, _Np_ = 6, and _I_ max = 3. We use GPT-5-nano<sup>1</sup> with low and medium reasoning levels, and GPT-4o-mini as a non-reasoning model. The sampling temperature for all agents is set to 1.0. Details of training/test sets and further experimental settings are in Appendix D. 

**Baselines.** PathWise is evaluated against a comprehensive set of state-of-the-art baselines, categorized by their underlying search frameworks. For the step-by-step construction framework, we compare against manually designed NearestGreedy constructive heuristics and POMO (Kwon et al., 2020), a representative Neural Combinatorial Optimization (NCO) method. In the online BPP task, performance is measured against classic heuristics, specifically Best Fit and First Fit (Seiden, 2002). Within the ACO framework, we benchmark against the original ACO (Dorigo et al., 2006) and its neural-enhanced variant, DeepACO (Ye et al., 2023). For the GLS framework, we compare against Knowledgeguided Local Search (KGLS) (Arnold & Sorensen¨ , 2019) and several iterative NCO solvers, including VRP-DACT 

> 1GPT-5-nano(low) and GPT-5-nano(medium) denote different reasoning levels of the same base model. 

6 

**PathWise: Planning through World Model for Automated Heuristic Design via Self-Evolving LLMs** 

_Table 2._ Designing heuristics with the ACO search framework for solving TSP, CVRP, MKP, OP, and offline BPP. Each test set contains 250 instances for TSP and CVRP, and 100 instances for the remaining problems. Performance of LLM-based AHD methods is averaged over 3 runs. Gaps are computed relative to the best-performing solver within each test set. 

|Task|T|SP||CV|RP||M|KP||O|P|||Offli|lne BPP||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Test sets|_N_=50|_N_=100|_N_=50,|_C_=50|_N_=100,_C_=50|_N_=10|0,_m_=5|_N_=300,_m_=5|_N_=|50|_N_=|200|_N_=500,|_C_=150|_N_=1000|,_C_=150|
|Methods|Obj._↓_<br>Gap|Obj._↓_<br>Gap|Obj._↓_|Gap|Obj._↓_<br>Gap|Obj._↑_|Gap|Obj._↑_<br>Gap|Obj._↑_|Gap|Obj._↑_|Gap|Obj._↓_|Gap|Obj._↓_|Gap|
|ACO|6.143 6.19%|9.191 12.66%|13.358|50.77%|22.587 50.32%|21.258|3.59%|53.640 7.77%|14.128|6.63%|49.556|8.43%|210.670|3.40%|420.630|3.73%|
|DeepACO|**5.785 0.00%**|**8.158 0.00%**|**8.860**|**0.00%**|**15.026 0.00%**|21.649|1.82%|56.250 3.28%|**15.132 **|**0.00%**|53.609|0.94%|**203.740 **|**0.00%**|**405.490**|**0.00%**|
||||||LLM|-based A|HD:_G_|_PT-4o-mini_|||||||||
|EoH|5.892 1.85%|8.382 2.75%|9.451|6.67%|16.796 11.78%|21.884|0.75%|56.740 2.44%|14.792|2.25%|53.180|1.74%|207.388|1.79%|414.585|2.24%|
|ReEvo|5.896 1.92%|8.351 2.37%|9.484|7.04%|16.749 11.47%|22.024|0.12%|57.051 1.91%|14.760|2.46%|51.602|4.65%|206.787|1.50%|412.943|1.84%|
|HSEvo|5.927 2.45%|8.361 2.49%|9.836|11.02%|17.112 13.88%|21.838|0.96%|56.672 2.56%|14.839|1.94%|53.678|0.81%|206.010|1.11%|411.145|1.39%|
|MCTS-AHD|5.908 2.13%|8.494 4.12%|9.915|11.91%|17.260 14.87%|21.900|0.68%|56.992 2.01%|14.810|2.13%|52.366|3.24%|205.255|0.74%|409.410|0.97%|
|PathWise(Ours)|5.874<br>1.54%|8.333<br>2.15%|9.350|5.53%|16.574<br>10.30%|22.037|0.06%|57.879<br>0.48%|14.915|1.43%|**54.119**|**0.00%**|205.100|0.67%|409.590|1.01%|
||||||LLM-based A|HD:_GP_|_T-5-na_|_no_(reasoning: lo|w)||||||||
|EoH|5.967 3.14%|8.685 6.46%|10.226|15.42%|17.696 17.77%|21.886|0.74%|56.682 2.54%|14.589|3.59%|50.210|7.21%|205.087|0.66%|408.707|0.79%|
|ReEvo|6.148 6.27%|9.352 14.64%|10.669|20.42%|18.141 20.73%|21.870|0.82%|56.215 3.34%|14.662|3.11%|49.209|9.07%|205.610|0.92%|410.330|1.19%|
|HSEvo|5.979 3.35%|8.910 9.22%|10.676|20.50%|18.188 21.04%|21.909|0.64%|56.774 2.38%|14.614|3.42%|50.507|6.67%|205.577|0.90%|409.793|1.06%|
|MCTS-AHD|5.930 2.51%|8.588 5.27%|10.763|21.48%|18.518 23.24%|21.874|0.80%|56.683 2.54%|14.639|3.26%|49.979|7.65%|206.590|1.40%|412.747|1.79%|
|PathWise(Ours)|5.859<br>1.28%|8.313<br>1.90%|9.648|8.89%|16.515<br>9.91%|22.026|0.11%|58.083<br>0.13%|14.682|2.97%|52.208|3.53%|204.360|0.30%|407.837|0.58%|
||||||LLM-based AH|D:_GPT-_|_5-nano_|(reasoning: med|ium)||||||||
|EoH|5.945 2.76%|8.638 5.88%|9.605|8.41%|16.886 12.38%|21.973|0.35%|57.378 1.34%|14.578|3.66%|51.048|5.66%|205.248|0.74%|409.788|1.06%|
|ReEvo|6.047 4.53%|8.935 9.52%|10.034|13.25%|17.226 14.64%|21.808|1.10%|55.983 3.74%|14.686|2.95%|48.511|10.36%|205.510|0.87%|410.177|1.16%|
|HSEvo|6.050 4.58%|9.105 11.61%|10.552|19.10%|17.998 19.78%|21.803|1.12%|56.119 3.51%|14.457|4.46%|40.910|24.41%|206.155|1.19%|411.725|1.54%|
|MCTS-AHD|6.026 4.17%|8.764 7.43%|9.619|8.57%|16.908 12.52%|22.015|0.16%|57.404 1.30%|14.672|3.04%|49.465|8.60%|205.725|0.97%|410.610|1.26%|
|PathWise(Ours)|5.812<br>0.47%|8.309<br>1.85%|9.637|8.77%|16.646<br>10.78%|**22.050**|**0.00%**|**58.159**<br>**0.00%**|14.795|2.23%|54.035|0.16%|204.885|0.56%|408.535|0.75%|





<!-- Start of picture text -->
−9.5 22.50<br>−10.0<br>22.45<br>−10.5<br>−11.0 22.40<br>−11.5 ReEvo ReEvo<br>HSEvo 22.35 HSEvo<br>−12.0 MCTS-AHD MCTS-AHD<br>PathWise (Ours) PathWise (Ours)<br>−12.5 0 100 200 300 400 500 22.30 0 100 200 300 400 500<br>Number of Evaluations on D Number of Evaluations on D<br>(a) CVRP - ACO (b) MKP - ACO<br>Performance of Heuristics on D Performance of Heuristics on D<br><!-- End of picture text -->

_Figure 3._ Evolution curves of LLM-based AHD methods using GPT-5-nano (low) on (a) CVRP and GPT-5-nano (medium) on (b) MKP, with a limit of _ne_ = 500 heuristic evaluations. Each curve is averaged over the 3 runs used in Table 2. 

(Ma et al., 2021), NeuOpt (Ma et al., 2023), NeuralGLS (Sui et al., 2023), and GNNGLS (Hudson et al., 2022). 

PathWise is also benchmarked against leading open-source LLM-based AHD methods: FunSearch (Romera-Paredes et al., 2023), EoH (Liu et al., 2024a), ReEvo (Ye et al., 2024), HSEvo (Dat et al., 2025), and MCTS-AHD (Zheng et al., 2025). For LLM-based AHD methods, we report the mean performance over three independent runs with a limit of _ne_ = 500 heuristic evaluations per task and a 60-second execution time per heuristic on the training dataset _D_ train. 

## **4.1. Overall Results** 

The overall performance of PathWise on the test sets _D_ test is shown in Table 1 for the step-by-step construction framework and Table 2 for the ACO framework, with results 

for the GLS framework provided in Appendix E. Additional cost analysis and output examples are provided in Appendix H and Appendix G, respectively. 

**Step-by-Step Construction Framework.** The step-bystep construction (constructive) framework builds a solution incrementally by selecting one feasible component at a time. At each step, the heuristic evaluates available choices based on the partial solution and selects the next component (Pacheco-Valencia et al., 2019; Asani et al., 2023). Within this framework, AHD focuses on generating heuristic functions that prioritize candidate components during construction. Experiments are conducted on TSP and KP, with additional results on online BPP reported in Appendix E. 

Table 1 shows that PathWise consistently outperforms the manually designed Greedy Construct heuristics and all LLM-based AHD methods on both TSP and KP across all test sets, showing that the improvements over baselines hold for both in-domain (ID) and out-of-domain (OOD) test sets and remain stable across different LLM backbones. Furthermore, performance improves systematically with model capability, with optimality gaps decreasing when moving from GPT-4o-mini to GPT-5-nano and with higher reasoning levels. To quantify improvements, we calculate the _mean relative gap improvement_ (MRGI) of PathWise over existing LLM-based AHD baselines, obtained by averaging the relative gap improvements of PathWise across LLM-based methods for each test set and LLM backbone (see Appendix E for details). On TSP, PathWise achieves an overall average improvement of 20 _._ 38%, averaged across test sets and 

7 

**PathWise: Planning through World Model for Automated Heuristic Design via Self-Evolving LLMs** 

LLM backbones, with improvement of 31 _._ 82% observed for GPT-5-nano (low). Similarly, on KP, PathWise achieves average improvements of 49 _._ 89% (GPT-4o-mini), 20 _._ 26% (GPT-5-nano (low)), and 65 _._ 20% (GPT-5-nano (medium)). PathWise further exhibits strong scalability with respect to problem size. When averaging the MRGI of each test set across LLM backbones, performance increases from 31 _._ 67% on the ID test set ( _N_ =100, _W_ =25) to 81 _._ 34% on the largest OOD test set ( _N_ =500, _W_ =25), indicating that the effectiveness grows as problem complexity increases. Moreover, PathWise achieves better performance on TSP ( _N_ =200) and KP test sets than the neural solver POMO, even though POMO requires task-specific training. 

**Ant Colony Optimization Framework.** ACO is a population-based framework inspired by the collective foraging behavior of ants, where multiple ants construct solutions by repeatedly choosing the next move according to both accumulated search experience and heuristic guidance (Kim et al., 2025; Abir et al., 2025). Within this framework, AHD focuses on generating heuristic functions that guide ants’ local decisions. Experiments are conducted TSP, CVRP, MKP, OP, and offline BPP, with extended results on a wider range of problem instances provided in Appendix E. 

Table 2 shows that PathWise outperforms LLM-based AHD methods on 5 CO problems in both 4 ID test sets and 4 OOD test sets across all LLM backbones. PathWise achieves overall average MRGI gains of 60 _._ 22% on TSP, 38 _._ 73% on CVRP, 89 _._ 35% on MKP, 54 _._ 81% on OP, and 44 _._ 86% on offline BPP, averaged across test sets and LLM backbones within each problem. Furthermore, PathWise demonstrates strong scalability; for example, the average MRGI on OP across LLM backbones increases from 25 _._ 40% on the ID test set ( _N_ =50) to 84 _._ 22% on the OOD test set ( _N_ =200), consistent with the trends in the constructive framework. PathWise also consistently outperforms manually designed ACO heuristics across all test sets and LLM backbones. Moreover, PathWise achieves better performance on OP ( _N_ =200) and MKP than the neural solver DeepACO, even though DeepACO requires specialized per-scale training. 

To evaluate heuristic evolution efficiency and stability, we compare best-so-far heuristic performance as a function of evaluation number. As shown in Figure 3, PathWise exhibits faster convergence and lower variance across tasks and LLM backbones. Notably, this behavior persists even when allowing twice the evaluation budget for LLM-based AHD baselines, as shown in Figure 1 (averaged over 5 runs). 

## **4.2. Ablation Study** 

We conduct an ablation study on the TSP constructive task to evaluate the impact of core components in PathWise, using GPT-5-nano(low), with results averaged over 5 runs. These experiments examine how planning through a 

world model, critic-driven feedback, and prompt-level diversity jointly improve heuristic discovery and generalizability. Parameter ablations are provided in Appendix F.4. 

_Table 3._ Ablations on critic agents in _PathWise_ . We report optimality gaps (%) on training ( _<u>TSP50</u>_ ) and validation sets ( _TSP20_ , _TSP50_ ) for the step-by-step construction framework on TSP. 

|Methods|_TSP20_|_TSP50_|_TSP50_|
|---|---|---|---|
|PathWise|6.08%|9.72%|8.79%|
|_w/o_Policy Critic|8.51%|11.24%|10.21%|
|_w/o_World Model Critic|7.23%|10.44%|9.63%|
|_w/o_PolicyCritic & World Model Critic|11.73%|14.85%|14.42%|



**Contribution of Policy and World Model Critics.** To assess the impact of critic agents in PathWise, we selectively remove the policy critic and the world model critic with other components fixed. As shown in Table 3, removing either critic consistently degrades performance, indicating that critic feedback is central to effective heuristic evolution. Among the two, removing the policy critic results in a larger performance drop than removing the world model critic, highlighting the importance of feedback in guiding parent selection and operator choices. The world model critic provides complementary benefits by refining codelevel modifications, often simplifying algorithmic structure or reducing time complexity, which improves execution efficiency and stabilizes training. Removing both critics causes a substantial drop, demonstrating their complementary roles in maintaining collaboration between the policy and world model over the entailment graph. 

_Table 4._ Ablations on prompt perturbation and state shuffling in _PathWise_ . We report optimality gaps and the Selection Diversity Rate (SDR) on training ( _<u>TSP50</u>_ ) and validation sets ( _TSP20_ , _TSP50_ ) for the step-by-step construction framework on TSP. 

|Methods|_TSP20_|_TSP50_|_TSP50_||
|---|---|---|---|---|
||Gap (%)|Gap (%)|Gap (%)|SDR(%)|
|PathWise|6.08%|9.72%|8.79%|75.79%|
|_w/o_Prompt Perturbation & State Shuffling|9.19%|11.98%|11.43%|53.76%|
|_w/o_Prompt Perturbation|8.52%|10.15%|9.58%|70.30%|
|_w/o_State Shuffling|6.08%|9.93%|9.02%|61.03%|



**Effect of Prompt-level Diversity Mechanisms.** To evaluate prompt-level diversity in PathWise, we ablate prompt perturbation and state shuffling with all other components fixed. As shown in Table 4, removing both causes the largest performance drop and sharply reduces the Selection Diversity Rate (SDR), indicating that prompt-level diversity is critical for effective exploration. SDR measures the diversity of parent sets selected by the policy agent across entailment steps. Specifically, it is the ratio of the number of unique parent selections to the total number of policy selections over the evolutionary run, reflecting how broadly the policy explores the state. Among the two, removing prompt perturbation results in a larger performance drop, showing that 

8 

**PathWise: Planning through World Model for Automated Heuristic Design via Self-Evolving LLMs** 

semantic variation in sampled actions is the primary driver of exploration. In contrast, removing state shuffling has a smaller effect on solution quality but significantly reduces SDR, suggesting it mainly mitigates positional bias and improves selection diversity rather than directly affecting heuristic quality. Higher SDR correlates with improved performance, indicating that selection diversity is essential for preventing premature convergence. These results suggest prompt-level diversity mechanisms enhance performance by increasing action and rollout contrast, yielding more informative feedback for heuristic evolution. 

# **5. Conclusion** 

In this paper, we propose PathWise, a novel hybrid graphbased and population-based framework formulating AHD as state-aware planning through reasoning over an entailment graph, enabling reasoning about heuristic derivation over time. Through collaboration of policy, world model, and critic agents, PathWise supports structured, memory-aware, and diverse heuristic generation guided by past decisions and outcomes. Experiments show PathWise discovers better heuristics with fast convergence and strong generalizability. 

# **Acknowledgements** 

This work is supported in part by the DARPA SciFy program, Award No. HR001125C0302. 

# **Impact Statement** 

This paper presents work whose goal is to advance the field of Machine Learning. There are many potential societal consequences of our work, none which we feel must be specifically highlighted here. 

# **References** 

- Abir, A. R., Nayeem, M. A., Rahman, M. S., and Arefeen, M. A. Gtg-aco: Graph transformer guided ant colony optimization for learning heuristics and pheromone dynamics for combinatorial optimization. _Swarm and Evolutionary Computation_ , 99:102147, 2025. 

- Arnold, F. and Sorensen, K.¨ Knowledge-guided local search for the vehicle routing problem. _Computers & Operations Research_ , 105, 2019. 

- Asani, E. O., Okeyinka, A. E., and Adebiyi, A. A. A computation investigation of the impact of convex hull subtour on the nearest neighbour heuristic. In _2023 International Conference on Science, Engineering and Business for Sustainable Development Goals (SEB-SDG)_ , volume 1, pp. 1–7, 2023. 

- Back, T., Fogel, D. B., and Michalewicz, Z.¨ _Handbook of Evolutionary Computation_ . CRC Press, 1st edition, 1997. 

- Bito, E., Ren, Y., and He, E. Evaluating position bias in large language model recommendations. _arXiv preprint arXiv:2508.02020_ , 2025. 

- Bradley, H., Fan, H., Galanos, T., Zhou, R., Scott, D., and Lehman, J. _The OpenELM Library: Leveraging Progress in Language Models for Novel Evolutionary Algorithms_ , pp. 177–201. Springer Nature Singapore, 2024. 

- Branke, J., Nguyen, S., Pickardt, C. W., and Zhang, M. Automated design of production scheduling heuristics: A review. _IEEE Transactions on Evolutionary Computation_ , 20(1):110–124, 2016. 

- Burke, E., Gendreau, M., Hyde, M., Kendall, G., Ochoa, G., Ozcan, E., and Qu, R.<sup>¨</sup> Hyper-heuristics: A survey of the state of the art. _Journal of the Operational Research Society_ , 64:1695–1724, 07 2013. 

- Chen, A., Dohan, D., and So, D. Evoprompting: Language models for code-level neural architecture search. In _Advances in Neural Information Processing Systems_ , volume 36, pp. 7787–7817, 2023. 

- Chen, M., Tworek, J., Jun, H., Yuan, Q., de Oliveira Pinto, H. P., Kaplan, J., Edwards, H., Burda, Y., Joseph, N., Brockman, G., et al. Evaluating large language models trained on code. _arXiv preprint arXiv:2107.03374_ , 2021. 

- Chhikara, P., Khant, D., Aryan, S., Singh, T., and Yadav, D. Mem0: Building production-ready ai agents with scalable long-term memory. _arXiv preprint arXiv:2504.19413_ , 2025. 

- Chitturi, S. R., Ramdas, A., Wu, Y., Rohr, B., Ermon, S., Dionne, J., Jornada, F. H. d., Dunne, M., Tassone, C., Neiswanger, W., et al. Targeted materials discovery using bayesian algorithm execution. _npj Computational Materials_ , 10(1), 2024. 

- Choong, S. S., Wong, L.-P., and Lim, C. P. Automatic design of hyper-heuristic based on reinforcement learning. _Information Sciences_ , 436-437:89–107, 2018. 

- Cowling, P., Kendall, G., and Soubeiga, E. A hyperheuristic approach to scheduling a sales summit. In _Practice and Theory of Automated Timetabling III_ , pp. 176–190. Springer Berlin Heidelberg, 2001. 

- Dalvi, B., Jansen, P., Tafjord, O., Xie, Z., Smith, H., Pipatanangkura, L., and Clark, P. Explaining answers with entailment trees. In _Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing_ , pp. 7358–7370, 2021. 

9 

**PathWise: Planning through World Model for Automated Heuristic Design via Self-Evolving LLMs** 

- Dat, P. V. T., Doan, L., and Binh, H. T. T. Hsevo: Elevating automatic heuristic design with diversity-driven harmony search and genetic algorithm using llms. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 39, pp. 26931–26938, 2025. 

- Desale, S., Rasool, A., Andhale, S., and Priti, R. Heuristic and meta-heuristic algorithms and their relevance to the real world: A survey. _International Journal of Computer Engineering in Research Trends_ , 2(5):296–304, 2015. 

- Dokeroglu, T., Kucukyilmaz, T., and Talbi, E.-G. Hyperheuristics: A survey and taxonomy. _Computers & Industrial Engineering_ , 187:109815, 2024. 

- Doppa, J. R. Adaptive experimental design for optimizing combinatorial structures. In _Proceedings of the Thirtieth International Joint Conference on Artificial Intelligence, IJCAI-21_ , pp. 4940–4945, 2021. 

- Dorigo, M., Birattari, M., and Stutzle, T. Ant colony optimization. _IEEE Computational Intelligence Magazine_ , 1 (4):28–39, 2006. 

- Duflo, G., Kieffer, E., Brust, M. R., Danoy, G., and Bouvry, P. A gp hyper-heuristic approach for generating tsp heuristics. In _2019 IEEE International Parallel and Distributed Processing Symposium Workshops (IPDPSW)_ , pp. 521–529, 2019. 

- Dunning, I., Gupta, S., and Silberholz, J. What works best when? a systematic evaluation of heuristics for max-cut and qubo. _INFORMS J. on Computing_ , 30(3):608–624, 2018. 

- Eiben, A. E. and Smith, J. E. _Introduction to Evolutionary Computing_ . Springer, 2nd edition, 2015. 

- Fernando, C., Banarse, D., Michalewski, H., Osindero, S., and Rocktaschel, T.¨ Promptbreeder: self-referential selfimprovement via prompt evolution. In _Proceedings of the 41st International Conference on Machine Learning_ , ICML’24, 2024. 

- Fukunaga, A. Automated discovery of composite sat variable-selection heuristics. In _Eighteenth National Conference on Artificial Intelligence_ , pp. 641–648, 2002. 

- Gandhi, A., Nguyen, T. Q., Jiao, H., Steen, R., and Bhatawdekar, A. Natural language commanding via program synthesis. _arXiv preprint arXiv:2306.03460_ , 2023. 

- Gao, H.-a., Geng, J., Hua, W., Hu, M., Juan, X., Liu, H., Liu, S., Qiu, J., Qi, X., Wu, Y., et al. A survey of self-evolving agents: On path to artificial super intelligence. _arXiv preprint arXiv:2507.21046_ , 2025. 

- Glover, F. Tabu search—part ii. _ORSA Journal on Computing_ , 2(1):4–32, 1990. 

- Grie _β_ haber, D., Kimmich, M., Maucher, J., and Vu, T. A toolbox for improving evolutionary prompt search. In _Proceedings of the 2nd LUHME Workshop_ , pp. 58–66, 2025. 

- Guo, P.-F., Chen, Y.-H., Tsai, Y.-D., and Lin, S.-D. Towards optimizing with large language models. In _Fourth Workshop on Knowledge-infused Learning_ , 2024a. 

- Guo, Q., Wang, R., Guo, J., Li, B., Song, K., Tan, X., Liu, G., Bian, J., and Yang, Y. Connecting large language models with evolutionary algorithms yields powerful prompt optimizers. In _The Twelfth International Conference on Learning Representations_ , 2024b. 

- Hao, S., Gu, Y., Ma, H., Hong, J., Wang, Z., Wang, D., and Hu, Z. Reasoning with language model is planning with world model. In _Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing_ , pp. 8154–8173, 2023. 

- Helsgaun, K. An extension of the lin–kernighan–helsgaun tsp solver for constrained traveling salesman and vehicle routing problems. Technical report, Roskilde University, 2017. 

- Hemberg, E., Moskal, S., and O’Reilly, U.-M. Evolving code with a large language model. _Genetic Programming and Evolvable Machines_ , 25(2), 2024. 

- Hudson, B., Li, Q., Malencia, M., and Prorok, A. Graph neural network guided local search for the traveling salesperson problem. In _International Conference on Learning Representations_ , 2022. 

- Jardee, W. and Sheppard, J. Ant colony optimization with policy gradients and replay. In _Proceedings of the Genetic and Evolutionary Computation Conference_ , GECCO ’25, pp. 240–248, 2025. 

- Kieffer, E., Danoy, G., Brust, M. R., Bouvry, P., and Nagih, A. Tackling large-scale and combinatorial bi-level problems with a genetic programming hyper-heuristic. _IEEE Transactions on Evolutionary Computation_ , 24(1):44–56, 2020. 

- Kim, M., Choi, S., Kim, H., Son, J., Park, J., and Bengio, Y. Ant colony sampling with gflownets for combinatorial optimization. In _Proceedings of The 28th International Conference on Artificial Intelligence and Statistics_ , volume 258 of _Proceedings of Machine Learning Research_ , pp. 469–477, 2025. 

- Kirkpatrick, S., Gelatt, C. D., and Vecchi, M. P. Optimization by simulated annealing. _Science_ , 220(4598): 671–680, 1983. 

10 

**PathWise: Planning through World Model for Automated Heuristic Design via Self-Evolving LLMs** 

- Kool, W., van Hoof, H., and Welling, M. Attention, learn to solve routing problems! In _International Conference on Learning Representations_ , 2019. 

- Kwon, Y.-D., Choo, J., Kim, B., Yoon, I., Gwon, Y., and Min, S. Pomo: Policy optimization with multiple optima for reinforcement learning. In _Advances in Neural Information Processing Systems_ , volume 33, pp. 21188–21198, 2020. 

- Lanchantin, J., Chen, A., Dhuliawala, S., Yu, P., Weston, J., Sukhbaatar, S., and Kulikov, I. Diverse preference optimization. _arXiv preprint arXiv:2501.18101_ , 2025. 

- Langdon, W. and Poli, R. _Foundations of Genetic Programming_ . Springer-Verlag, 2013. 

- Lange, R., Tian, Y., and Tang, Y. Large language models as evolution strategies. In _Proceedings of the Genetic and Evolutionary Computation Conference Companion_ , GECCO ’24 Companion, pp. 579–582, 2024. 

- Lehman, J., Gordon, J., Jain, S., Ndousse, K., Yeh, C., and Stanley, K. O. Evolution through large models. In _Handbook of Evolutionary Machine Learning_ , pp. 331– 366. Springer, 2024. 

- Levine, J. and Ducatelle, F. Ant colony optimization and local search for bin packing and cutting stock problems. _Journal of the Operational Research Society_ , 55(7):705– 716, 2004. 

- Li, Y., Lin, Z., Zhang, S., Fu, Q., Chen, B., Lou, J.-G., and Chen, W. Making language models better reasoners with step-aware verifier. In _Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_ , pp. 5315–5333, 2023. 

- Li, Z., Wang, C., Ma, P., Wu, D., Wang, S., Gao, C., and Liu, Y. Split and merge: Aligning position biases in LLMbased evaluators. In _Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing_ , pp. 11084–11108, 2024. 

- Liang, X., Tao, M., Xia, Y., Wang, J., Li, K., Wang, Y., He, Y., Yang, J., Shi, T., Wang, Y., Zhang, M., and Wang, X. Sage: Self-evolving agents with reflective and memoryaugmented abilities. _Neurocomput._ , 647, 2025. 

- Liu, A., Mei, A., Lin, B., Xue, B., Wang, B., Xu, B., Wu, B., Zhang, B., Lin, C., Dong, C., et al. Deepseek-v3. 2: Pushing the frontier of open large language models. _arXiv preprint arXiv:2512.02556_ , 2025a. 

- Liu, F., Tong, X., Yuan, M., and Zhang, Q. Algorithm evolution using large language model. _arXiv preprint arXiv:2311.15249_ , 2023. 

- Liu, F., Tong, X., Yuan, M., Lin, X., Luo, F., Wang, Z., Lu, Z., and Zhang, Q. Evolution of heuristics: towards efficient automatic algorithm design using large language model. In _Proceedings of the 41st International Conference on Machine Learning_ , ICML’24, 2024a. 

- Liu, F., Lin, X., Yao, S., Wang, Z., Tong, X., Yuan, M., and Zhang, Q. Large language model for multiobjective evolutionary optimization. In _Evolutionary Multi-Criterion Optimization_ , pp. 178–191, 2025b. 

- Liu, F., Liu, Y., Zhang, Q., Tong, X., and Yuan, M. Eoh-s: Evolution of heuristic set using llms for automated heuristic design. _arXiv preprint arXiv:2508.03082_ , 2025c. 

- Liu, F., Zhang, Q., Shi, J., Tong, X., Mao, K., and Yuan, M. Fitness landscape of large language modelassisted automated algorithm search. _arXiv preprint arXiv:2504.19636_ , 2025d. 

- Liu, S., Chen, C., Qu, X., Tang, K., and Ong, Y.-S. Large language models as evolutionary optimizers. In _2024 IEEE Congress on Evolutionary Computation (CEC)_ , pp. 1–8, 2024b. 

- Lourenc¸o, H. R., Martin, O. C., and Stutzle, T.¨ Iterated local search. In _Handbook of metaheuristics_ , pp. 320–353. Springer, 2003. 

- Ma, W., He, J., Snell, C., Griggs, T., Min, S., and Zaharia, M. Reasoning models can be effective without thinking. _arXiv preprint arXiv:2504.09858_ , 2025. 

- Ma, Y., Li, J., Cao, Z., Song, W., Zhang, L., Chen, Z., and Tang, J. Learning to iteratively solve routing problems with dual-aspect collaborative transformer. In _Advances in Neural Information Processing Systems_ , volume 34, pp. 11096–11107, 2021. 

- Ma, Y., Cao, Z., and Chee, Y. M. Learning to search feasible and infeasible regions of routing problems with flexible neural k-opt. In _Thirty-seventh Conference on Neural Information Processing Systems_ , volume 36, pp. 49555– 49578, 2023. 

- Ma, Y.-N., Gong, Y.-J., Xiao, C.-F., Gao, Y., and Zhang, J. Path planning for autonomous underwater vehicles: An ant colony algorithm incorporating alarm pheromone. _IEEE Transactions on Vehicular Technology_ , 68(1):141– 154, 2019. 

- Madaan, A., Tandon, N., Gupta, P., Hallinan, S., Gao, L., Wiegreffe, S., Alon, U., Dziri, N., Prabhumoye, S., Yang, Y., et al. Self-refine: Iterative refinement with self-feedback. In _Thirty-seventh Conference on Neural Information Processing Systems_ , 2023. 

11 

**PathWise: Planning through World Model for Automated Heuristic Design via Self-Evolving LLMs** 

- Meyerson, E., Nelson, M. J., Bradley, H., Gaier, A., Moradi, A., Hoover, A. K., and Lehman, J. Language model crossover: Variation through few-shot prompting. _ACM Trans. Evol. Learn. Optim._ , 4(4), 2024. 

- Nasir, M. U., Earle, S., Togelius, J., James, S., and Cleghorn, C. Llmatic: neural architecture search via large language models and quality diversity optimization. In _proceedings of the Genetic and Evolutionary Computation Conference_ , pp. 1110–1118, 2024. 

- Ouyang, S., Yan, J., Hsu, I., Chen, Y., Jiang, K., Wang, Z., Han, R., Le, L. T., Daruki, S., Tang, X., et al. Reasoningbank: Scaling agent self-evolving with reasoning memory. _arXiv preprint arXiv:2509.25140_ , 2025. 

- Pacheco-Valencia, V., Hernandez-Aguilar, J. A., Sigarreta,´ J., and Vakhania, N. Simple constructive, insertion, and improvement heuristics based on the girding polygon for the euclidean traveling salesman problem. _Algorithms_ , 13:5, 12 2019. 

- Papenmeier, L., Nardi, L., and Poloczek, M. Bounce: reliable high-dimensional bayesian optimization for combinatorial and mixed spaces. In _Proceedings of the 37th International Conference on Neural Information Processing Systems_ , 2023. 

- Perron, L. and Furnon, V. Or-tools. Google, Version v9.12, https://developers.google.com/ optimization/, 2025. 

- Pillay, N. and Qu, R. Introduction to hyper-heuristics. In _Hyper-Heuristics: Theory and Applications_ . Springer, 2018. 

- Pisinger, D. An exact algorithm for large multiple knapsack problems. _European Journal of Operational Research_ , 114(3):528–541, 1999. 

- Pryzant, R., Iter, D., Li, J., Lee, Y., Zhu, C., and Zeng, M. Automatic prompt optimization with “gradient descent” and beam search. In _Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing_ , pp. 7957–7968, 2023. 

- Qian, X., Yoon, B.-J., Arroyave,´ R., Qian, X., and Dougherty, E. R. Knowledge-driven learning, optimization, and experimental design under uncertainty for materials discovery. _Patterns_ , 4(11):100863, 2023. 

- Qiu, J., Yuan, H., Zhang, J., Chen, W., Wang, H., and Wang, M. Tree search-based evolutionary bandits for protein sequence optimization. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 38, pp. 14686–14694, 2024. 

- Reinelt, G. Tsplib—a traveling salesman problem library. _ORSA journal on computing_ , 3(4):376–384, 1991. 

- Reinhart, W. F. and Statt, A. Large language models design sequence-defined macromolecules via evolutionary optimization. _npj Computational Materials_ , 10(1):262, 2024. 

- Romera-Paredes, B., Barekatain, M., Novikov, A., Balog, M., Kumar, M. P., Dupont, E., Ruiz, F. J. R., Ellenberg, J., Wang, P., Fawzi, O., Kohli, P., and Fawzi, A. Mathematical discoveries from program search with large language models. _Nature_ , 2023. 

- Sabar, N. R., Ayob, M., Kendall, G., and Qu, R. Grammatical evolution hyper-heuristic for combinatorial optimization problems. _IEEE Transactions on Evolutionary Computation_ , 17(6):840–861, 2013. 

- Schilcher, P., Karasin, D., Schopf, M., Saleh, H., Tommasel,¨ A., and Schedl, M. Characterizing positional bias in large language models: A multi-model evaluation of prompt order effects. In _Findings of the Association for Computational Linguistics: EMNLP 2025_ , pp. 20643–20664, 2025. 

- Seiden, S. S. On the online bin packing problem. _J. ACM_ , 49(5):640–671, September 2002. ISSN 0004-5411. 

- Shi, W. W., Han, W., and Si, W. C. A hybrid genetic algorithm based on harmony search and its improving. In _Informatics and Management Science I_ , pp. 101–109. Springer, 2013. 

- Shinn, N., Cassano, F., Gopinath, A., Narasimhan, K. R., and Yao, S. Reflexion: language agents with verbal reinforcement learning. In _37th Conference on Neural Information Processing Systems_ , 2023. 

- Sim, K., Renau, Q., and Hart, E. Beyond the hype: Benchmarking llm-evolved heuristics for bin packing. In _Applications of Evolutionary Computation_ , pp. 386–402, 2025. 

- Singh, A., Fry, A., Perelman, A., Tart, A., Ganesh, A., El-Kishky, A., McLaughlin, A., Low, A., Ostrow, A., Ananthram, A., et al. Openai gpt-5 system card. _arXiv preprint arXiv:2601.03267_ , 2025. 

- Slocum, S., Parker-Sartori, A., and Hadfield-Menell, D. Diverse preference learning for capabilities and alignment. In _The Thirteenth International Conference on Learning Representations_ , 2025. 

- Smith-Miles, K., Baatar, D., Wreford, B., and Lewis, R. Towards objective measures of algorithm performance across instance space. _Computers & Operations Research_ , 45, 2014. 

12 

**PathWise: Planning through World Model for Automated Heuristic Design via Self-Evolving LLMs** 

- Smith-Miles, K., Christiansen, J., and Munoz, M. A.˜ Revisiting where are the hard knapsack problems? via instance space analysis. _Computers & Operations Research_ , 128, 2021. 

- Srivastava, G., Hussain, A., Bi, Z., Roy, S., Pitre, P., Lu, M., Ziyadi, M., and Wang, X. Beyondbench: Benchmarkfree evaluation of reasoning in language models. _arXiv preprint arXiv:2509.24210_ , 2025. 

- Sui, J., Ding, S., Xia, B., Liu, R., and Bu, D. Neuralgls: learning to guide local search with graph convolutional network for the traveling salesman problem. _Neural Comput. Appl._ , 36(17):9687–9706, 2023. 

- Sun, H., Chai, Y., Wang, S., Sun, Y., Wu, H., and Wang, H. Curiosity-driven reinforcement learning from human feedback. In _Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_ , pp. 23517–23534, 2025. 

- Swiechowski,´ M., Godlewski, K., Sawicki, B., and Mandziuk, J.´ Monte carlo tree search: A review of recent modifications and applications. _Artificial Intelligence Review_ , 56(3):2497–2562, 2023. 

- Tam, N. T., Khanh Ly, T. H., Duc, B. T., Hung, T. H., and Thanh Binh, H. T. Multi-objective virtual network functions placement and traffic routing problem. In _2024 IEEE Congress on Evolutionary Computation (CEC)_ , pp. 01–08, 2024. 

- Toth, P. and Vigo, D. Models, relaxations and exact approaches for the capacitated vehicle routing problem. _Discrete Applied Mathematics_ , 123(1):487–512, 2002. 

- van Stein, N., V. Kononova, A., Kotthoff, L., and Back, T.¨ Code evolution graphs: Understanding large language model driven design of algorithms. In _Proceedings of the Genetic and Evolutionary Computation Conference_ , pp. 943–951, 2025. 

- Vansteenwegen, P., Souffriau, W., and Oudheusden, D. V. The orienteering problem: A survey. _European Journal of Operational Research_ , 209(1):1–10, 2011. 

- Voudouris, C. and Tsang, E. Guided local search and its application to the traveling salesman problem. _European Journal of Operational Research_ , 113(2):469–499, 1999. 

- Wang, H., Zhang, X., and Mu, C. Planning of heuristics: Strategic planning on large language models with monte carlo tree search for automating heuristic optimization. _arXiv preprint arXiv:2502.11422_ , 2025a. 

- Wang, T., Liu, Z., Chen, Y., Light, J., Liu, W., Chen, H., Zhang, X., and Cheng, W. On the effect of sampling diversity in scaling llm inference. _arXiv preprint arXiv:2502.11027_ , 2025b. 

- Wei, J., Wang, X., Schuurmans, D., Bosma, M., ichter, b., Xia, F., Chi, E., Le, Q. V., and Zhou, D. Chain-of-thought prompting elicits reasoning in large language models. In _Advances in Neural Information Processing Systems_ , volume 35, pp. 24824–24837, 2022. 

- Wu, X., Wu, S.-H., Wu, J., Feng, L., and Tan, K. C. Evolutionary computation in the era of large language model: Survey and roadmap. _IEEE Transactions on Evolutionary Computation_ , 29(2):534–554, 2025. 

- Xiang, J., Zhang, J., Yu, Z., Liang, X., Teng, F., Tu, J., Ren, F., Tang, X., Hong, S., Wu, C., and Luo, Y. Selfsupervised prompt optimization. In _Findings of the Association for Computational Linguistics: EMNLP 2025_ , pp. 9017–9041, 2025. 

- Xiong, S., Payani, A., and Fekri, F. Enhancing long chainof-thought reasoning through multi-path plan aggregation. _arXiv preprint arXiv:2510.11620_ , 2025a. 

- Xiong, S., Payani, A., Yang, Y., and Fekri, F. Deliberate reasoning in language models as structure-aware planning with an accurate world model. In _Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_ , pp. 31900–31931, 2025b. 

- Xiong, S., Gungordu, O., Johnson, B., Kerce, J. C., and Fekri, F. Scaling search-augmented llm reasoning via adaptive information control. _arXiv preprint arXiv:2602.01672_ , 2026a. 

- Xiong, S., Payani, A., and Fekri, F. Enhancing language model reasoning with structured multi-level modeling. In _The Fourteenth International Conference on Learning Representations_ , 2026b. 

- Xu, C., Sun, Q., Zheng, K., Geng, X., Zhao, P., Feng, J., Tao, C., Lin, Q., and Jiang, D. WizardLM: Empowering large pre-trained language models to follow complex instructions. In _The Twelfth International Conference on Learning Representations_ , 2024. 

- Xu, W., Liang, Z., Mei, K., Gao, H., Tan, J., and Zhang, Y. A-mem: Agentic memory for LLM agents. In _The Thirty-ninth Annual Conference on Neural Information Processing Systems_ , 2025. 

- Yang, C., Wang, X., Lu, Y., Liu, H., Le, Q. V., Zhou, D., and Chen, X. Large language models as optimizers. In _The Twelfth International Conference on Learning Representations_ , 2024a. 

- Yang, Y., Xiong, S., Payani, A., Shareghi, E., and Fekri, F. Can LLMs reason in the wild with programs? In _Findings of the Association for Computational Linguistics: EMNLP 2024_ , 2024b. 

13 

**PathWise: Planning through World Model for Automated Heuristic Design via Self-Evolving LLMs** 

- Yang, Y., Xiong, S., Payani, A., Shareghi, E., and Fekri, F. Harnessing the power of large language models for natural language to first-order logic translation. In _Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_ , pp. 6942–6959, 2024c. 

- Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K. R., and Cao, Y. React: Synergizing reasoning and acting in language models. In _The Eleventh International Conference on Learning Representations_ , 2023. 

   - Zhou, D., Scharli, N., Hou, L., Wei, J., Scales, N., Wang,¨ X., Schuurmans, D., Cui, C., Bousquet, O., Le, Q. V., and Chi, E. H. Least-to-most prompting enables complex reasoning in large language models. In _The Eleventh International Conference on Learning Representations_ , 2023a. 

   - Zhou, Y., Muresanu, A. I., Han, Z., Paster, K., Pitis, S., Chan, H., and Ba, J. Large language models are humanlevel prompt engineers. In _The Eleventh International Conference on Learning Representations_ , 2023b. 

- Yao, S., Liu, F., Lin, X., Lu, Z., Wang, Z., and Zhang, Q. Multi-objective evolution of heuristic using large language model. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , 2025. 

- Ye, H., Wang, J., Cao, Z., Liang, H., and Li, Y. DeepACO: Neural-enhanced ant systems for combinatorial optimization. In _Thirty-seventh Conference on Neural Information Processing Systems_ , 2023. 

- Ye, H., Wang, J., Cao, Z., Berto, F., Hua, C., Kim, H., Park, J., and Song, G. Reevo: large language models as hyperheuristics with reflective evolution. In _Proceedings of the 38th International Conference on Neural Information Processing Systems_ , 2024. 

- Yuan, H., Ni, C., Wang, H., Zhang, X., Cong, L., Szepesvari,´ C., and Wang, M. Bandit theory and thompson samplingguided directed evolution for sequence optimization. _Advances in Neural Information Processing Systems_ , 35: 38291–38304, 2022. 

- Zhang, Q., Hu, C., Upasani, S., Ma, B., Hong, F., Kamanuru, V., Rainton, J., Wu, C., Ji, M., Li, H., et al. Agentic context engineering: Evolving contexts for self-improving language models. _arXiv preprint arXiv:2510.04618_ , 2025. 

- Zhang, Y., Bai, R., Qu, R., Tu, C., and Jin, J. A deep reinforcement learning based hyper-heuristic for combinatorial optimisation with uncertainties. _European Journal of Operational Research_ , 300(2):418–427, 2022. 

- Zhao, E., Awasthi, P., and Gollapudi, S. Sample, scrutinize and scale: Effective inference-time search by scaling verification. In _Forty-second International Conference on Machine Learning_ , 2025. 

- Zhao, Z., Lee, W. S., and Hsu, D. Large language models as commonsense knowledge for large-scale task planning. In _Thirty-seventh Conference on Neural Information Processing Systems_ , 2023. 

- Zheng, Z., Xie, Z., Wang, Z., and Hooi, B. Monte carlo tree search for comprehensive exploration in LLM-based automatic heuristic design. In _Forty-second International Conference on Machine Learning_ , 2025. 

14 

**PathWise: Planning through World Model for Automated Heuristic Design via Self-Evolving LLMs** 

# **A. Related Work** 

## **A.1. AHD and Hyper-Heuristics** 

Heuristic algorithms are central to solving COPs in domains such as logistics, scheduling, and design, where exact methods are often impractical due to NP-hardness (Kieffer et al., 2020). Consequently, metaheuristic approaches such as simulated annealing, tabu search, and iterated local search have been widely adopted to obtain high-quality solutions under limited computational budgets (Kirkpatrick et al., 1983; Glover, 1990; Lourenc¸o et al., 2003; Desale et al., 2015; Tam et al., 2024). Despite their effectiveness, heuristic development has relied on domain expertise and manual trial-and-error, resulting in solvers that are costly to develop and generalize poorly across problem variants (Pillay & Qu, 2018; Choong et al., 2018). 

AHD and hyper-heuristics aim to reduce this reliance on manual design by shifting the search from solutions to heuristics themselves (Burke et al., 2013). Early hyper-heuristic frameworks introduced the idea of selecting or generating heuristics at a higher level, either by choosing among predefined low-level heuristics or by constructing new heuristics from reusable components (Cowling et al., 2001; Sabar et al., 2013). A common realization of this paradigm is GP, where heuristics are represented as executable programs and evolved through mutation and recombination (Langdon & Poli, 2013). GP-based AHD has produced competitive heuristics for satisfiability, scheduling, routing, and packing problems (Fukunaga, 2002; Branke et al., 2016; Duflo et al., 2019). In parallel, learning-based hyper-heuristics model heuristic selection as a sequential decision problem and apply RL to adaptively choose heuristics during search, showing improved performance over static selection strategies in several optimization settings (Zhang et al., 2022; Dokeroglu et al., 2024). 

## **A.2. Evolutionary Algorithms with LLMs** 

Evolutionary algorithms (EAs) are search and optimization methods inspired by biological mechanisms such as natural selection, mutation, and recombination. They provide a general framework for search processes, where a population of candidates is iteratively improved through variation and selection (Back et al.¨ , 1997; Eiben & Smith, 2015). Within this framework, LLMs are typically used as generative operators that produce new candidates conditioned on selected parents, while fitness evaluation and population updates are handled externally following standard EAs. Several recent works adopt this paradigm by prompting LLMs to perform mutation- and crossover-like transformations on existing candidates, leveraging the LLM’s ability to generate code or structured text rather than operating on fixed symbolic representations (Lehman et al., 2024; Meyerson et al., 2024; Lange et al., 2024). The resulting evolutionary loop maintains a population, selects parents based on performance, and uses the LLM to generate offspring that modify and combine prior solutions. 

EAs with LLMs have been applied to program synthesis and algorithmic code generation, where candidate programs are refined over generations by iteratively improving promising implementations (Chen et al., 2023; Hemberg et al., 2024; Bradley et al., 2024). Other approaches apply evolutionary search to natural language outputs, evolving textual solutions under task-specific evaluation criteria, which shows that EA principles extend naturally to purely linguistic search spaces (Fernando et al., 2024; Xu et al., 2024). Closely related methods focus on evolving prompts themselves, using evolutionary operators to discover prompts that consistently elicit higher-quality outputs (Guo et al., 2024b; Grie _β_ haber et al., 2025). Overall, EAs provide a practical way to structure LLM-based search by handling evaluation and selection externally while using LLMs for candidate generation (Wu et al., 2025). 

## **A.3. LLM-based AHD** 

Prior to LLM-based AHD, LLM-as-optimizers have been used for COPs, where the model directly improves solutions for individual problem instances rather than discovering reusable algorithms. In this paradigm, LLMs generate candidate solutions through in-context learning and iteratively refine them by conditioning on previously generated high-quality solutions together with their objective values (Yang et al., 2024a; Guo et al., 2024a; Liu et al., 2024b). This optimization process typically follows a loop in which an initial set of feasible solutions is produced for a given instance, the bestperforming solutions are retained, and the LLM is repeatedly prompted to propose improved candidates that are evaluated and fed back into the context. While effective for improving solution quality on individual instances, LLM-as-optimizer methods face challenges on problems with large or complex search spaces, including limited exploration capability and sensitivity to context design (Nasir et al., 2024; Zhao et al., 2023; Liu et al., 2025b). 

Moving beyond instance-level optimization, LLM-based AHD methods integrate LLMs into evolutionary search to automatically generate heuristics with minimal human intervention (Liu et al., 2023). Many approaches adopt population-based evolutionary procedures, where LLMs iteratively refine a population of candidate algorithms using evolutionary search 

15 

**PathWise: Planning through World Model for Automated Heuristic Design via Self-Evolving LLMs** 

(Chen et al., 2023; Meyerson et al., 2024). Early methods such as FunSearch (Romera-Paredes et al., 2023) and EoH (Liu et al., 2024a) employ LLM-guided operators to evolve high-performing heuristics, enabling efficient exploration of large heuristic spaces. ReEvo (Ye et al., 2024) further incorporates a reflection mechanism to analyze generated heuristics and guide subsequent search steps (Shinn et al., 2023). Building on this, HSEvo (Dat et al., 2025) introduces diversity-aware population management and harmony search to promote population diversity and mitigate premature convergence (Shi et al., 2013). Beyond population-based approaches, tree-based methods have also been explored (Wang et al., 2025a). In particular, MCTS-AHD (Zheng et al., 2025) integrates LLMs with Monte Carlo Tree Search, applying the UCT algorithm to guide selection and expansion of heuristic nodes in a tree structure, enabling more structured exploration of the heuristic space (Swiechowski et al.<sup>´</sup> , 2023). 

Several LLM-based AHD works extend beyond single-heuristic, single-objective settings. (Liu et al., 2025c) focuses on generating a small set of complementary heuristics to improve coverage across diverse instance distributions; however, it does not learn or predict which heuristic to apply to a given instance at inference time, and thus operates at a set-level evaluation. (Yao et al., 2025) formulates heuristic generation as a multi-objective optimization problem, incorporating efficiency criteria in addition to heuristic performance. In PathWise and the baselines considered in this paper, heuristics are evaluated under the same search framework, sharing the same heuristic space and fitness landscape, with a focus on heuristic performance using an explicit instance-level inference procedure. 

## **A.4. LLM for Reasoning and Code Generation** 

LLMs have demonstrated capabilities in complex logical reasoning, mathematical problem-solving, and code generation (Yang et al., 2024b). However, standard chain-of-thought prompting often becomes unreliable on multi-step tasks due to error accumulation and limited long-horizon consistency, motivating structured reasoning approaches that make intermediate state, verification, and search more explicit (Yao et al., 2023; Li et al., 2023). Reasoning can be formulated as structure-aware planning with world models for symbolic state tracking and validation (Hao et al., 2023; Xiong et al., 2025b; 2026b), or combined with programmatic tools and formal representations to decompose subproblems and verify intermediate outputs (Yang et al., 2024c). Exploring multiple reasoning trajectories and aggregating their outcomes further mitigates failures associated with single forward-pass inference (Xiong et al., 2025a; 2026a). 

Recently, learning from feedback and experience has emerged as a way to improve LLM reasoning, by evolving the context provided to the model across attempts and tasks (Gao et al., 2025). Iterative critique-and-revision mechanisms allow models to generate feedback on their own outputs and refine them over multiple passes (Shinn et al., 2023; Madaan et al., 2023). Other approaches treat prompts and instructions as objects of search, using performance feedback and textual edits to construct more effective and reusable contexts (Zhou et al., 2023b; Pryzant et al., 2023; Xiang et al., 2025; Zhang et al., 2025). In parallel, memory-based methods store, retrieve, and update information from prior interactions so that agents can reuse effective reasoning patterns and workflows across tasks, rather than relearning them each time (Liang et al., 2025; Ouyang et al., 2025; Chhikara et al., 2025; Xu et al., 2025). Together, these directions indicate that improving reasoning and code generation depends not only on better prompting for individual instances, but also on mechanisms that accumulate feedback and experience into reusable context over time (Gao et al., 2025). These frameworks generally are evaluated on tasks such as question answering or tool use, which focus on solving individual problem instances. In contrast, AHD introduces additional challenges, as it requires learning executable algorithms that generalize across instance distributions and evolve under long-horizon heuristic discovery. PathWise addresses these challenges by applying learning from feedback and experience to the heuristic discovery setting, using state-aware reasoning over an entailment graph that provides a stateful representation of derivation history and structured reasoning to guide heuristic evolution over time. 

# **B. Details of Benchmark Problems** 

This section presents the problem definitions, mathematical formulations, and the procedures used for benchmark instance generation. Experiments are conducted on a set of representative NP-hard COPs, including the Traveling Salesman Problem (TSP), Knapsack Problem (KP), Capacitated Vehicle Routing Problem (CVRP), Multiple Knapsack Problem (MKP), Orienteering Problem (OP), and Bin Packing Problem (BPP). For BPP, both offline and online settings are considered. 

## **B.1. Traveling Salesman Problem (TSP)** 

**Definition.** The Traveling Salesman Problem (TSP) seeks a minimum-length Hamiltonian tour that visits each city exactly once and returns to the starting city. 

16 

**PathWise: Planning through World Model for Automated Heuristic Design via Self-Evolving LLMs** 

**Formulation.** Let _G_ = ( _V, E_ ) be a complete graph with _V_ = _{_ 1 _, . . . , n}_ and edge costs _cij ≥_ 0. Let _xij ∈{_ 0 _,_ 1 _}_ . 



where _∀i, j ∈ V_ and _∀S ⊂ V,_ 2 _≤|S| ≤ n −_ 1. 

**Instance generation.** Node coordinates are uniformly sampled from [0 _,_ 1]<sup>2</sup> . The distance matrix is computed using Euclidean distances, with diagonal elements set to 1 to prevent self-loops, and a small constant (10<sup>_−_5</sup> ) added to diagonal to prevent numerical issues in the GLS framework. 

## **B.2. Knapsack Problem (KP)** 

**Definition.** The Knapsack Problem (KP) aims to select a subset of items with maximum total value subject to a single weight constraint. 

**Formulation.** Given values _vi_ , weights _wi_ , and weight _W_ , let _xi ∈{_ 0 _,_ 1 _}_ . 



**Instance generation.** Item weights and values are uniformly sampled from [0 _,_ 1]. The knapsack weight capacity is set to 25 for all problem sizes, except 12.5 for the 50-item instances, following the settings of ReEvo (Ye et al., 2024). 

## **B.3. Capacitated Vehicle Routing Problem (CVRP)** 

**Definition.** The Capacitated Vehicle Routing Problem (CVRP) seeks a set of minimum-cost vehicle routes originating and ending at a depot, such that all customer demands are satisfied without exceeding vehicle capacity. 

**Formulation.** Let _G_ = ( _V, E_ ) include depot 0, customers _V \ {_ 0 _}_ , demands _di_ , capacity _C_ , and _xij ∈{_ 0 _,_ 1 _}_ (Toth & Vigo, 2002). 



where _∀i, j ∈ V \ {_ 0 _}_ and _∀S ⊆ V \ {_ 0 _}_ . 

**Instance generation.** Node coordinates are uniformly sampled from [0 _,_ 1]<sup>2</sup> . A depot is fixed at coordinates [0 _._ 5 _,_ 0 _._ 5]. Customer demands are uniformly sampled from _{_ 1 _,_ 2 _, . . . ,_ 9 _}_ . The vehicle capacity is set to 50, following the settings of ReEvo (Ye et al., 2024). 

## **B.4. Multiple Knapsack Problem (MKP)** 

**Definition.** The Multiple Knapsack Problem (MKP) generalizes the knapsack problem to multiple knapsacks, where items must be assigned to at most one knapsack. 

**Formulation.** Let _vi_ be the value of item _i_ , _wij_ be the weight of item _i_ in knapsack _j_ , _Cj_ be the capacity of knapsack _j_ , and 

17 

**PathWise: Planning through World Model for Automated Heuristic Design via Self-Evolving LLMs** 

_xij ∈{_ 0 _,_ 1 _}_ indicate whether item _i_ is assigned to knapsack _j_ (Pisinger, 1999). 



**Instance generation.** For MKP with _n_ items and _m_ = 5 knapsacks, item values _vi_ are uniformly sampled from [0 _,_ 1]. The weight _wij_ of item _i_ in knapsack _j_ is uniformly sampled from [0 _,_ 1]. For each knapsack _j_ , the capacity _Cj_ is uniformly sampled from [max _i wij,_<sup>�</sup> _i_<sup>_wij_], then all weights are normalized as</sup><sup>_wij←wij/Cj_such that</sup><sup>_Cj_= 1 after normalization,</sup> ensuring well-defined instances, following the settings of ReEvo (Ye et al., 2024). 

## **B.5. Orienteering Problem (OP)** 

**Definition.** The Orienteering Problem (OP) seeks a path that maximizes collected rewards from visited nodes while satisfying a total travel budget constraint. 

**Formulation.** Let rewards be _ri_ , travel costs be _cij_ , and the budget be _B_ (Vansteenwegen et al., 2011). 



**Instance generation.** Node coordinates are uniformly sampled from [0 _,_ 1]<sup>2</sup> . The travel costs _cij_ are computed as Euclidean distances between nodes. Prize values are computed as _ri_ = (1 + _⌊_ 99 _· di/d_ max _⌋_ ) _/_ 100 where _di_ is the Euclidean distance from node _i_ to the depot (node 0), normalized by the maximum distance _d_ max, and then normalized such that max _i ri_ = 1, following the settings of ReEvo (Ye et al., 2024). The travel budget _B_ varies by problem size: _B_ = 3 _._ 0 for _n_ = 50, _B_ = 4 _._ 0 for _n_ = 100, _B_ = 5 _._ 0 for _n_ = 200, _B_ = 6 _._ 0 for _n_ = 300, and _B_ = 7 _._ 0 for larger instances (Kool et al., 2019). 

## **B.6. Bin Packing Problem (BPP)** 

**Definition.** The Bin Packing Problem (BPP) aims to pack items of varying sizes into the minimum number of bins with fixed capacity. In the offline setting, all item sizes are known in advance, whereas in the online setting, items arrive sequentially and must be assigned to bins without knowledge of future items. 

**Formulation.** Let item sizes be _si_ and bin capacity be _C_ . 



**Instance generation.** For the offline version, item demands are uniformly sampled from _{_ 20 _,_ 21 _, . . . ,_ 100 _}_ , following the protocol used in Funsearch (Romera-Paredes et al., 2023) and EoH (Liu et al., 2024a). The bin capacity is set to 150. For the online version, item sizes are sampled from a Weibull distribution with shape parameter 3 and scale parameter 45, then clipped to a maximum value of 100. The bin capacity is set to 100 or 500 depending on the evaluation setting (Levine & Ducatelle, 2004), following the protocol used in ReEvo (Ye et al., 2024) and MCTS-AHD (Zheng et al., 2025). 

# **C. Details of General Search Frameworks** 

This section provides detailed descriptions of the general search frameworks used in our experiments. These frameworks provide the algorithmic backbone within which our LLM-evolved heuristics operate. For each framework, we describe the underlying search mechanism and specify the particular heuristic functions that LLM-based AHD methods learn for different COPs. 

18 

**PathWise: Planning through World Model for Automated Heuristic Design via Self-Evolving LLMs** 

## **C.1. Step-by-Step Construction** 

**Framework Description.** Step-by-step construction (also known as greedy constructive heuristics) is a classical approach for solving COPs where solutions are built incrementally by making sequential decisions. Starting from an empty or partial solution, the algorithm iteratively selects the next component to add based on a selection rule until a complete feasible solution is constructed. This approach is characterized by its computational efficiency and ability to quickly generate reasonable solutions, though it typically cannot backtrack from previously made decisions. 

**Search Procedure.** Let _St_ denote the partial solution at step _t_ , and _Ct_ represent the set of feasible components that can be added to _St_ . At each step, a selection function _h_ : _St × Ct →_ R assigns a score to each candidate component _c ∈ Ct_ . The next component is selected as: 



The algorithm terminates when no more components can be added, yielding the final solution _S_<sup>_∗_</sup> = _ST_ . 

**Problem-Specific Heuristics.** We apply this framework to three problems, where LLM-based methods evolve the selection function _h_ : 

- **TSP-Constructive** : Starting from a depot node, the algorithm iteratively selects the next city to visit until all cities are visited and the tour returns to the depot. The evolved heuristic _h_ determines which unvisited city should be selected next based on the current city, remaining unvisited cities, and the distance matrix. 

- **KP-Constructive** : Items are sequentially selected for inclusion in the knapsack until no more items can fit within the capacity constraint. The evolved heuristic _h_ ranks items based on remaining capacity, item weights, and item values to determine the next item to select. 

- **BPP-Online** : Items arrive sequentially and must be immediately assigned to bins without future knowledge. For each arriving item, the evolved heuristic _h_ computes a priority score for each bin based on the item size and bin remaining capacities, selecting the bin with the highest priority. 

## **C.2. Ant Colony Optimization** 

**Framework Description.** Ant Colony Optimization (ACO) is a population-based metaheuristic inspired by the foraging behavior of ants, originally proposed by Dorigo et al. (Dorigo et al., 2006). The algorithm maintains a probabilistic model in the form of pheromone trails _τij_ defined over solution components (e.g., edges in routing problems), which guide the stochastic construction of solutions by a population of artificial ants. At each construction step, ants sample solution components according to a transition rule that combines pheromone information with heuristic measures, typically controlled by weighting parameters. Through repeated solution construction and pheromone update cycles, ACO balances exploration and exploitation, progressively reinforcing high-quality components while evaporating inferior ones to improve solution quality over time (Jardee & Sheppard, 2025). 

**Search Procedure.** Each ant _k_ constructs a solution by probabilistically selecting components based on pheromone levels _τij_ and heuristic information _ηij_ . The probability of selecting component _j_ from component _i_ is: 



where _Ni_<sup>_k_isthesetoffeasiblecomponentsforant</sup><sup>_k_atcomponent</sup><sup>_i_,and</sup><sup>_α, β_areparameterscontrollingtherelative</sup> importance of pheromone and heuristic information. 

After all ants construct solutions with costs _L_<sup>_k_</sup> , pheromones are updated as: 



where _ρ ∈_ (0 _,_ 1) is the evaporation rate and _m_ is the number of ants. 

**Problem-Specific Heuristics.** The heuristic information matrix _ηij_ plays a crucial role in guiding solution construction. We apply ACO to five problems where LLM-based methods evolve problem-specific heuristics: 

19 

**PathWise: Planning through World Model for Automated Heuristic Design via Self-Evolving LLMs** 

- **TSP-ACO** : The heuristic _ηij_ provides edge-level guidance for including edge ( _i, j_ ) in the tour. The evolved heuristic takes the distance matrix as input and returns a matrix indicating how promising each edge is for tour construction. 

- **CVRP-ACO** : For vehicle routing with capacity constraints, the heuristic _ηij_ incorporates both distance information and customer demands to guide route construction. The evolved heuristic considers the distance matrix, node coordinates, customer demands, and vehicle capacity to produce edge-level guidance. 

- **MKP-ACO** : The heuristic _ηi_ provides item-level guidance indicating how promising each item is for inclusion. The evolved heuristic takes item prizes and the multi-dimensional weight matrix as input, returning a vector of heuristic values for items, considering the normalized capacity constraints. 

- **OP-ACO** : The heuristic _ηij_ balances prize collection and distance constraints. The evolved heuristic takes prize values, the distance matrix, and the maximum path length budget as input, producing an edge-level heuristic matrix that guides path construction toward high-value nodes while respecting the travel budget. 

- **BPP-Offline-ACO** : For offline bin packing, the heuristic _ηij_ indicates how promising it is to pack items _i_ and _j_ in the same bin. The evolved heuristic takes item demands and bin capacity as input, returning a pairwise affinity matrix that guides the grouping of items into bins. 

## **C.3. Guided Local Search (GLS)** 

**Framework Description.** Guided Local Search (GLS) is a metaheuristic that enhances local search by strategically escaping local optima through solution modification (Voudouris & Tsang, 1999). The algorithm maintains penalty weights on solution features (e.g., edges in TSP) that dynamically adjust during the search. When local search converges to a local optimum, GLS penalizes features that contribute to the current solution’s cost, effectively modifying the search landscape to encourage exploration of different regions. This mechanism combines the efficiency of local search with the ability to escape local optima through adaptive penalties. In our experiments, the GLS-family framework is instantiated as Knowledge-Guided Local Search (KGLS) (Arnold & Sorensen¨ , 2019), which injects a learned knowledge matrix to guide when and how features are penalized and how the current solution is perturbed. This design follows prior LLM-based AHD work that evolves penalty/knowledge heuristics for GLS and deploys them within KGLS (Ye et al., 2024; Zheng et al., 2025). 

**Search Procedure.** Let _st_ denote the current solution at iteration _t_ , _f_ ( _s_ ) the original objective function, and _pi_ the penalty associated with feature _i_ (e.g., an edge in TSP). GLS considers an augmented objective: 



where _I_ ( _s_ ) is the set of features present in solution _s_ , and _λ_ controls the penalty strength (typically set as _λ_ = _α · f_ ( _s_<sup>_∗_</sup> ) _/n_ , where _s_<sup>_∗_</sup> is the best solution found, _n_ is the problem size, and _α_ is a scaling parameter). 

When local search reaches a local optimum under _g_ ( _·_ ), penalties are updated using a utility score. In KGLS, the utility is modulated by a learned knowledge matrix _η_ : 



where _ηij_ is the learned knowledge signal for feature (edge) ( _i, j_ ), and _cij_ is the cost contribution of feature ( _i, j_ ) (e.g., edge distance _dij_ for edge ( _i, j_ ) in TSP). Features with maximal utility are identified and penalized: _pij ← pij_ + 1. This penalty update modifies the augmented objective _g_ ( _s_ ), and local search resumes under the updated landscape. 

KGLS alternates between two phases: (i) Local Improvement, where classical local search operators (e.g., 2-opt and relocate for TSP) are applied to improve the current solution under the augmented objective _g_ ( _s_ ); and (ii) Guided Perturbation, where upon convergence to a local optimum, features with high utility scores (computed using the learned knowledge matrix) are penalized to modify the search landscape. The algorithm maintains and updates the best solution _s_<sup>_∗_</sup> encountered throughout the search, returning it upon termination. 

**Problem-Specific Heuristic.** We apply the GLS framework to TSP, where the LLM-based methods evolve the knowledge matrix that guides the penalty mechanism: 

20 

**PathWise: Planning through World Model for Automated Heuristic Design via Self-Evolving LLMs** 

- **TSP-GLS** : Edges are penalized when they appear in local optima. The evolved heuristic takes the distance matrix as input and returns a knowledge matrix _η ∈_ R<sup>_n×n_</sup> , where _ηij_ encodes distance-weighted knowledge about how problematic or undesirable edge ( _i, j_ ) is for solution quality. When local search converges, the utility of each edge ( _i, j_ ) in the current tour is computed as util( _i, j_ ) = _ηij/_ (1 + _pij_ ), where _pij_ is the accumulated penalty on edge ( _i, j_ ). Edges with maximum utility are then penalized to guide perturbation. This allows the search to prioritize penalizing edges identified as problematic by the learned heuristic while accounting for how frequently they have already been penalized, leading to more effective escape from local optima. 

# **D. Experimental Details** 

This section provides the experimental configuration used across reported results, including dataset construction, LLM-based AHD settings, NCO baselines, and the hyperparameters of the underlying search frameworks. 

## **D.1. Dataset Configuration** 

The datasets used in the experiments are organized according to the underlying search framework and problem type. For each framework–problem pair, a fixed training dataset _D_ train and a separate test dataset _D_ test are constructed. The instance size (e.g., number of nodes, items, or customers) and the number of instances for both datasets are reported in Table 5. 

During heuristic design, all LLM-based AHD methods are evaluated only on the training set _D_ train, which represents the in-distribution data used to guide the search through performance feedback. Once the stopping criterion is met, defined by reaching the heuristic evaluation budget _ne_ , the final heuristic produced by each method is evaluated on the held-out test set _D_ test, which is used to assess out-of-distribution generalization. For each problem domain, _D_ train and _D_ test are synthesized by sampling random instances under fixed settings, following ReEvo (Ye et al., 2024), EoH (Liu et al., 2024a), and MCTS-AHD (Zheng et al., 2025). Compared to these prior works, we evaluate on test sets with larger instance sizes and a greater number of instances, in order to assess performance under more challenging and diverse problem settings (Smith-Miles et al., 2014; Dunning et al., 2018; Smith-Miles et al., 2021; Sim et al., 2025). 

_Table 5._ Benchmark dataset configuration across frameworks and problems. 

|Framework|Problem|_D_|train|_D_test||
|---|---|---|---|---|---|
|||Size|#Instances|Size|#Instances|
||TSP|50|64|_{_50,100,200_}_|250|
|Constructive|KP|100|64|_{_50,100,200,500_}_|250|
||Online BPP|_{_1k,5k_}_|4|_{_1k,5k,10k_}_|10|
||TSP|50|5|_{_50,100_}_|250|
||CVRP|50|10|_{_50,100_}_|250|
|ACO|MKP|100|5|_{_100,200,300,500,1k_}_|100|
||OP|50|10|_{_50,100,200,500_}_|100|
||Offline BPP|500|5|_{_500,1000_}_|100|
|GLS|TSP|200|10|_{_100,200,500,1k_}_|250|



## **D.2. LLM-Based AHD Methods Configuration** 

Details of the evaluation budget, language model choices, and settings used by LLM-based AHD methods are provided below. 

**Evaluation Budget** _ne_ For all LLM-based AHD methods, the maximum number of heuristic evaluations is fixed to _ne_ = 500 for all problem domains. A uniform evaluation budget is used to ensure fair comparison across methods and to attribute performance differences to the quality of the search strategy rather than to unequal computational effort. Although increasing _ne_ enables broader exploration, overly large evaluation budgets can mask methodological differences due to the stochastic nature of LLMs. With sufficiently many sampled heuristics, improvements may primarily reflect the effects of generating many random candidate heuristics rather than consistent search guidance or convergence behavior (Zhao et al., 2025; Wang et al., 2025b). By setting _ne_ to a moderate value, the evaluation emphasizes a method’s ability to efficiently guide heuristic generation and achieve reliable improvements within a bounded computational budget, rather than relying on large-scale sampling. In addition, all heuristic evaluations are executed on a single AMD Ryzen Threadripper PRO 7985WX CPU, and each method’s total training time is capped at 6 hours per run. 

21 

**PathWise: Planning through World Model for Automated Heuristic Design via Self-Evolving LLMs** 

**Large Language Models Configuration.** Both non-reasoning and reasoning LLMs are evaluated to study how models with different reasoning capabilities behave in AHD. The pre-trained LLM is _gpt-4o-mini-2024-07-18_ for GPT-4o-mini and GPT-5-nano for the GPT-5 family, which provides a fast and cost-efficient reasoning-capable model with strong performance on reasoning benchmarks involving multi-step inference and algorithmic problem solving (Srivastava et al., 2025; Singh et al., 2025). For PathWise, the temperature is fixed to 1 _._ 0 for all agents. For other LLM-based AHD methods, temperature settings follow their original configurations; for example, ReEvo increases the temperature to 0 _._ 3 during the initialization phase to promote diverse heuristic sampling. An exception is GPT-5-nano, for which the temperature is fixed to 1 _._ 0 as it is not configurable. Experiments with GPT-5-nano are conducted using low verbosity and two reasoning levels (low and medium). 

**Baselines Configuration** We follow the original algorithmic configurations for all baseline LLM-based AHD methods (e.g., number of parents in operators, operator ordering, mutation rate, number of islands, and harmony search hyperparameters). For ReEvo and HSEvo, the population size is set to 30 during the initialization stage and reduced to 10 in subsequent stages. For EoH, the population size is set to 20 for Online BPP and to 10 for all other tasks. 

ReEvo and HSEvo require seed heuristic functions to initialize the search and maintain sufficient variation among candidate heuristics. When all individuals in the population converge to the same objective value, no further optimization is possible and the search terminates. Following the setup in MCTS-AHD (Zheng et al., 2025), we use the seed functions proposed in (Ye et al., 2024) for ACO and GLS frameworks, random selection heuristics for constructive TSP, and the best-known heuristic from (Romera-Paredes et al., 2023) for Online BPP. 

Although HSEvo does not originally report results for certain problem–framework combinations, including CVRP-ACO, MKP-ACO, TSP-ACO, and constructive settings, its architecture closely follows ReEvo with additional diversity mechanisms. We therefore include these configurations to provide a comprehensive comparison. For some tasks, such as constructive KP for ReEvo and HSEvo, results are not reported due to early termination caused by convergence of the heuristics in the population to identical objective values (Zheng et al., 2025). 

## **D.3. NCO Methods Configuration** 

For the step-by-step constructive framework, we report results of POMO (Kwon et al., 2020) on TSP and KP, where solutions are constructed sequentially using a learned constructive policy. POMO solutions are generated using a single start without test-time augmentation. Within the ACO framework, we compare against DeepACO (Ye et al., 2023) on TSP, CVRP, MKP, OP, and Offline BPP, where neural networks provide learned heuristic guidance for ant decision rules and are trained separately for each dataset size. Following DeepACO (Ye et al., 2023), the number of steps per epoch is set to 128 and the number of training epochs is set to 5, while the number of ants (ant population size) and graph sparsification parameters are chosen according to problem-specific settings across different instance sizes. ACO results are generated using the baseline heuristic configurations described in (Ye et al., 2023). For the GLS framework, we include iterative NCO solvers—VRP-DACT (Ma et al., 2021), NeuOpt (Ma et al., 2023), NeuralGLS (Sui et al., 2023), and GNNGLS (Hudson et al., 2022)—and report their performance on TSP instances, where the maximum number of operations applied to a solution is fixed to _T_ = 1200 for VRP-DACT and NeuOpt. 

## **D.4. Search Frameworks Configuration** 

Table 6 details the search framework hyperparameters used for heuristic evaluations during heuristic evolution. These configurations specify the population size for ACO, perturbation moves for GLS, and the total number of iterations for both frameworks. 

_Table 6._ Search framework hyperparameters used during heuristic evolution across problems. 

|Framework|Problem|Search Hyperparameters||
|---|---|---|---|
|||Population Size(#Ants)<br>Perturbation Moves|#Iterations|
|GLS|TSP|—<br>30|1200|
||TSP|30<br>—|100|
||CVRP|30<br>—|100|
|ACO|MKP|10<br>—|50|
||OP|20<br>—|50|
||Offline BPP|20<br>—|15|



22 

**PathWise: Planning through World Model for Automated Heuristic Design via Self-Evolving LLMs** 

# **E. Extended Results** 

This section presents evaluation metric details and extended experimental results. We report additional results for the step-by-step construction framework on online BPP in Table 7, results for the GLS framework on TSP in Table 8, extended ACO results on larger-size MKP and OP instances in Table 9, results on TSPLIB instances in Table 10, results with the opensource LLM backbone DeepSeek-V3.2 in Table 11, and statistical significance testing on TSP-ACO and KP-Constructive in Tables 12 and 13. Together, these results provide a more comprehensive view of PathWise’s performance across different search frameworks, problem variants, problem sizes, and LLM backbones. 

**Evaluation Metric.** To quantify performance improvements over LLM-based AHD baseline methods, let Gap _m_ denote the optimality gap of a baseline method _m_ on a given test set, and let GapPW denote the corresponding gap achieved by PathWise. The _relative gap improvement_ (RGI) of PathWise over method _m_ is defined as 



For a fixed test set and LLM backbone, we compute the _mean relative gap improvement_ (MRGI) by averaging the RGI values of PathWise over all available LLM-based AHD baselines for that test set: 



where _M_ denotes the set of LLM-based AHD methods included in the comparison for the corresponding CO problem. This yields an MRGI value for each combination of CO problem, test set, and LLM backbone. These MRGI values are used to compare the performance of PathWise across different LLM backbones and problem sizes. By averaging MRGI values over test sets of the same problem, we evaluate how performance differs between ID and OOD settings. Averaging MRGI across test sets for a fixed LLM backbone summarizes the effect of model capability, while averaging across LLM backbones reflects overall robustness independent of a specific model choice. 

**Online BPP under the Step-by-Step Construction Framework.** In online BPP, the heuristic decides how each incoming item is assigned to a bin sequentially based on the current bin states. Table 7 reports results on 6 test sets covering both ID and OOD problem sizes. Across all LLM backbones, PathWise consistently achieves the lowest average gap to the lower bound when averaged over the 6 test sets. When comparing average performance, PathWise yields higher MRGI over existing LLM-based AHD baselines: 54 _._ 48% under GPT-4o-mini, 33 _._ 86% under GPT-5-nano (low), and 50 _._ 96% under GPT-5-nano (medium). 

_Table 7._ Designing step-by-step construction heuristics for online BPP. Performance gaps to the lower bound are reported, averaged over 3 runs for each LLM-based AHD method. Each test set consists of 10 Weibull BPP instances, with in-domain scales in _Dtest_ underlined. Test-set scales are abbreviated (e.g., 1k ~~1~~ 00 denotes 1,000 items with capacity _W_ =100). 

||||Online B|PP||||
|---|---|---|---|---|---|---|---|
|Test sets|1k<br>100|1k<br>500|5k<br>~~1~~00|5k<br>~~5~~00|10k<br>~~1~~00|10k<br>500|Avg.|
|Best Fit|4.73%|0.25%|4.19%|0.50%|3.99%|0.45%|2.35%|
|First Fit|5.05%|0.62%|4.56%|0.52%|4.31%|0.46%|2.59%|
|||LL|M-based AHD:|_GPT-4o-mini_||||
|EoH|4.80%|0.38%|3.66%|0.49%|3.29%|0.45%|2.18%|
|ReEvo|4.66%|0.25%|3.27%|0.50%|2.70%|0.44%|1.97%|
|HSEvo|4.11%|0.66%|3.20%|0.53%|3.01%|0.45%|1.99%|
|MCTS-AHD|4.79%|0.25%|4.15%|0.48%|4.01%|0.45%|2.36%|
|PathWise(Ours)|2.46%|0.29%|1.38%|0.38%|1.23%|0.33%|**1.01%**|
|||LLM-based|AHD:_GPT-5-n_|_ano_ (reasoning:|low)|||
|EoH|3.38%|0.37%|2.04%|0.74%|1.82%|0.63%|1.50%|
|ReEvo|4.70%|0.25%|4.20%|0.47%|4.02%|0.45%|2.35%|
|HSEvo|3.96%|0.52%|1.77%|0.55%|1.28%|0.51%|1.43%|
|MCTS-AHD|4.36%|0.44%|3.93%|0.50%|3.77%|0.45%|2.24%|
|PathWise(Ours)|3.10%|0.37%|2.11%|0.54%|1.65%|0.48%|**1.38%**|
|||LLM-based A|HD:_GPT-5-nan_|_o_ (reasoning: m|edium)|||
|EoH|4.27%|0.25%|2.32%|0.50%|1.95%|0.62%|1.65%|
|ReEvo|3.22%|0.37%|2.62%|0.47%|2.52%|0.42%|1.60%|
|HSEvo|4.42%|0.48%|3.70%|0.50%|3.49%|0.45%|2.17%|
|MCTS-AHD|3.19%|0.29%|2.09%|0.39%|1.91%|0.35%|1.37%|
|PathWise(Ours)|2.92%|0.29%|0.92%|0.26%|0.84%|0.23%|**0.91%**|



23 

**PathWise: Planning through World Model for Automated Heuristic Design via Self-Evolving LLMs** 

**TSP under the GLS Framework.** Table 8 reports optimality gaps for designing heuristics within the GLS framework on TSP. Performance improves systematically with model capability, with gaps generally decreasing when moving from GPT-4omini to GPT-5-nano (medium). In terms of performance comparison among LLM-based AHD methods, PathWise achieves average MRGI values of 3 _._ 77% under GPT-4o-mini, 13 _._ 91% under GPT-5-nano (low), and 25 _._ 04% under GPT-5-nano (medium), where averages are computed across MRGI values of test sets for each LLM backbone. 

_Table 8._ Designing heuristics within the GLS general framework for solving TSP. We report optimality gaps (%) to the optimum. Each LLM-based AHD method is run 3 times and we report average optimality gaps. 

|||TSP-GLS|||
|---|---|---|---|---|
|_N_ =|100|200|500|1,000|
|Optimal|0.0000%|0.0000%|0.0000%|0.0000%|
|KGLS|**0.0034%**|0.2270%|0.9578%|1.5348%|
||NCO methods<br>|with the GLSgeneral fram<br>|ework<br>||
|VRP-DACT|1.7943%|91.9267%|N/A|N/A|
|NeuOpt|0.2950%|0.9152%|N/A|N/A|
|NeuralGLS|0.470%|3.622%|N/A|N/A|
|GNNGLS|0.705%|3.522%|N/A|N/A|
||LLM-b|ased AHD:_GPT-4o-mini_|||
|ReEvo|0.0068%|0.1981%|0.9969%|1.5974%|
|HSEvo|0.0059%|0.2008%|0.9810%|1.6097%|
|MCTS-AHD|0.0078%|0.2053%|1.0094%|1.5929%|
|PathWise(Ours)|0.0060%|0.1919%|1.0009%|1.6021%|
||LLM-based AH<br>|D:_GPT-5-nano_ (reasoning<br>|: low)<br>||
|ReEvo|0.0060%|**0.1815%**|0.9699%|1.5947%|
|HSEvo|0.0122%|0.2185%|0.9558%|1.5568%|
|MCTS-AHD|0.0134%|0.2414%|0.9352%|1.4960%|
|PathWise(Ours)|0.0052%|0.2015%|0.9295%|1.4745%|
||LLM-based AHD<br>|:_GPT-5-nano_ (reasoning: <br>|medium)<br>||
|ReEvo|0.0110%|0.2169%|0.9825%|1.6103%|
|HSEvo|0.0154%|0.2132%|0.9273%|1.4930%|
|MCTS-AHD|0.0113%|0.2228%|0.9950%|1.6128%|
|PathWise(Ours)|0.0036%|0.1896%|**0.9090%**|**1.4039%**|



**MKP and OP under the ACO Framework on Larger-Size Instances.** Table 9 shows extended ACO results for MKP and OP on a wider range of instance sizes. Across both problems, PathWise consistently outperforms existing LLM-based AHD methods across all problem sizes and LLM backbones. On MKP, PathWise achieves the best performance on all evaluated test sets and surpasses DeepACO under GPT-5-nano (medium). On OP, PathWise surpasses DeepACO on the OOD _N_ =200 test set under GPT-4o-mini. These results demonstrate that PathWise remains effective at larger scales and can match or exceed DeepACO, which is a task-specific neural solver baseline. 

_Table 9._ Designing heuristics with the ACO general framework for solving MKP and OP. Each test set contains 100 instances, and the performance of LLM-based AHD methods is averaged over 3 runs. Gaps are computed relative to the best-performing solver within each test set. 

|Task|||||MKP|(_m_= 5)|||||||||OP||||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Test sets|_N_=|100|_N_=|200|_N_=|300|_N_=|500|_N_=1|000|_N_=|50|_N_=|100|_N_=|200|_N_=|500|
|Methods|Obj._↑_|Gap|Obj._↑_|Gap|Obj._↑_|Gap|Obj._↑_|Gap|Obj._↑_|Gap|Obj._↑_|Gap|Obj._↑_|Gap|Obj._↑_|Gap|Obj._↑_|Gap|
|ACO|21.258|3.59%|41.446|1.74%|53.640|7.77%|100.986|3.77%|183.450|5.15%|14.128|6.63%|29.199|3.82%|49.556|8.43%|107.870|12.46%|
|DeepACO|21.649|1.82%|41.980|0.47%|56.250|3.28%|102.535|2.29%|186.550|3.55%|**15.132 **|**0.00%**|**30.358**|**0.00%**|53.609|0.94%|**123.218**|**0.00%**|
||||||||LLM-|based A|HD:_GPT-_|_4o-mini_|||||||||
|EoH|21.884|0.75%|41.463|1.70%|56.740|2.44%|101.949|2.85%|186.275|3.69%|14.792|2.25%|30.002|1.17%|53.180|1.74%|116.719|5.27%|
|ReEvo|22.024|0.12%|41.724|1.08%|57.051|1.91%|102.057|2.75%|184.660|4.53%|14.760|2.46%|29.285|3.53%|51.602|4.65%|106.049|13.93%|
|HSEvo|21.838|0.96%|41.358|1.94%|56.672|2.56%|101.814|2.98%|185.874|3.90%|14.839|1.94%|30.089|0.89%|53.678|0.81%|118.600|3.75%|
|MCTS-AHD|21.900|0.68%|41.544|1.50%|56.992|2.01%|102.416|2.41%|187.024|3.30%|14.810|2.13%|30.042|1.04%|52.366|3.24%|115.665|6.13%|
|PathWise(Ours)|22.037|0.06%|42.043|0.32%|57.879|0.48%|104.378|0.54%|192.138|0.66%|14.915|1.43%|30.283|0.25%|**54.119**|**0.00%**|118.971|3.45%|
|||||||LLM|-based A|HD:_GP_|_T-5-nano_|(reasonin|g: low)||||||||
|EoH|21.886|0.74%|41.386|1.87%|56.682|2.54%|101.835|2.96%|185.788|3.94%|14.589|3.59%|29.274|3.57%|50.210|7.21%|93.210|24.35%|
|ReEvo|21.870|0.82%|41.300|2.08%|56.215|3.34%|101.075|3.68%|180.189|6.84%|14.662|3.11%|28.760|5.26%|49.209|9.07%|99.252|19.45%|
|HSEvo|21.909|0.64%|41.478|1.66%|56.774|2.38%|102.056|2.75%|186.665|3.49%|14.614|3.42%|28.771|5.23%|50.507|6.67%|108.405|12.02%|
|MCTS-AHD|21.874|0.80%|41.443|1.74%|56.683|2.54%|101.802|2.99%|185.246|4.22%|14.639|3.26%|28.734|5.35%|49.979|7.65%|107.064|13.11%|
|PathWise(Ours)|22.026|0.11%|42.150|0.07%|58.083|0.13%|104.829|0.11%|193.093|0.17%|14.682|2.97%|29.716|2.11%|52.208|3.53%|113.932|7.54%|
|||||||LLM-|based AH|D:_GPT-_|_5-nano_ (re|asoning:|medium|)|||||||
|EoH|21.973|0.35%|41.631|1.30%|57.378|1.34%|102.706|2.13%|185.393|4.15%|14.578|3.66%|29.438|3.02%|51.048|5.66%|114.316|7.22%|
|ReEvo|21.808|1.10%|40.997|2.80%|55.983|3.74%|100.287|4.44%|181.652|6.08%|14.686|2.95%|28.572|5.88%|48.511|10.36%|105.295|14.55%|
|HSEvo|21.803|1.12%|41.066|2.64%|56.119|3.51%|100.563|4.17%|182.750|5.51%|14.457|4.46%|26.977|11.14%|40.910|24.41%|57.929|52.99%|
|MCTS-AHD|22.015|0.16%|41.832|0.82%|57.404|1.30%|104.154|0.75%|191.478|1.00%|14.672|3.04%|28.922|4.73%|49.465|8.60%|111.069|9.86%|
|PathWise(Ours)|**22.050**|**0.00%**|**42.178**|**0.00%**|**58.159**|**0.00%**|**104.942**|**0.00%**|**193.416**|**0.00%**|14.795|2.23%|30.005|1.16%|54.035|0.16%|120.198|2.45%|



24 

**PathWise: Planning through World Model for Automated Heuristic Design via Self-Evolving LLMs** 

**Comparison of LLM-based AHD Methods on TSPLIB.** Evaluation is conducted on real-world TSP benchmarks from the TSPLIB dataset (Reinelt, 1991). Table 10 compares LLM-based AHD methods on TSPLIB instances using the step-by-step construction framework. Each heuristic is executed three times with different starting nodes, and optimality gaps are computed from the averaged objective values. Across instances, PathWise achieves the lowest average optimality gap and attains the best result on the majority of TSPLIB instances. 

_Table 10._ Results of LLM-based AHD methods for the TSP on TSPLIB instances using a step-by-step construction framework. For each instance, heuristics are run 3 times with different starting nodes, and the reported optimality gap is computed from the averaged results. The best result per instance is highlighted in bold. 

|Instance|ReEvo|HSEvo|MCTS-AHD|PathWise|
|---|---|---|---|---|
|ts225.tsp|20.60%|13.38%|**5.57%**|15.31%|
|rat99.tsp|14.65%|17.02%|16.48%|**10.63%**|
|bier127.tsp|9.46%|16.85%|14.83%|**8.15%**|
|lin318.tsp|21.31%|**13.01%**|17.63%|15.48%|
|eil51.tsp|13.10%|**6.52%**|9.42%|12.32%|
|d493.tsp|18.24%|13.84%|12.74%|**12.47%**|
|kroB100.tsp|12.28%|15.41%|**10.35%**|12.43%|
|kroC100.tsp|15.33%|9.95%|12.97%|**9.82%**|
|ch130.tsp|19.74%|11.59%|**9.60%**|10.55%|
|pr299.tsp|24.34%|17.23%|20.59%|**12.53%**|
|fl417.tsp|27.57%|22.07%|20.81%|**16.59%**|
|d657.tsp|24.62%|20.12%|**15.14%**|15.63%|
|kroA150.tsp|19.90%|16.44%|15.51%|**11.93%**|
|pr264.tsp|17.87%|18.49%|19.84%|**15.40%**|
|pr226.tsp|17.84%|23.10%|19.77%|**8.90%**|
|pr439.tsp|21.95%|23.03%|17.96%|**13.65%**|
|Average Opt. Gap|18.68%|16.13%|14.95%|**12.61%**|



**Evaluation with an Open-Source LLM Backbone.** To assess the dependence of PathWise on proprietary LLMs, we additionally evaluate it with the open-source model DeepSeek-V3.2 (Liu et al., 2025a) on TSP under the ACO framework and KP under the step-by-step construction framework, using the same evaluation protocol as in Section 4. As shown in Table 11, PathWise continues to outperform LLM-based AHD baselines across problems and test sets with this open-source backbone, indicating that the framework generalizes beyond closed-source models. MCTS-AHD is excluded from the TSP-ACO comparison due to its prohibitively long training time per run. 

_Table 11._ Designing heuristics with the open-source DeepSeek-V3.2 model on TSP-ACO and KP-Constructive. We report mean optimality gaps (%). Entries marked “N/A” indicate that the method was not run for that task in this evaluation. 

|Task|TSP|-ACO||KP-Constructive||
|---|---|---|---|---|---|
|Test sets|_N_=50|_N_=100|_N_=50,_W_=12_._5|_N_=200,_W_=25|_N_=500,_W_=25|
|||LLM-b|ased AHD:_DeepSeek-_|_V3.2_||
|ReEvo|3.53%|8.59%|N/A|N/A|N/A|
|HSEvo|2.77%|6.40%|N/A|N/A|N/A|
|MCTS-AHD|N/A|N/A|0.25%|0.09%|0.06%|
|PathWise(Ours)|1.86%|3.78%|0.21%|0.07%|0.04%|



**Statistical Significance Testing.** To assess the statistical significance of PathWise’s improvements over LLM-based AHD baselines, we conduct 6 independent runs of PathWise and the baselines on TSP-ACO and KP-Constructive across multiple LLM backbones. For each test set, we report mean optimality gap, standard deviation (Std), and the p-value of a one-sided _t_ -test comparing PathWise to each baseline. Tables 12 and 13 show that PathWise improvements over all baselines are statistically significant ( _p <_ 0 _._ 05) across problems, sizes, and LLM backbones. MCTS-AHD is excluded from the TSP-ACO comparison due to its prohibitively long training time per run. 

25 

**PathWise: Planning through World Model for Automated Heuristic Design via Self-Evolving LLMs** 

_Table 12._ Statistical significance testing on TSP-ACO. Mean optimality gap (%), standard deviation (Std), and one-sided _t_ -test p-values between each baseline and PathWise are reported over 6 runs. 

|Test sets||_N_=50|||_N_=100||
|---|---|---|---|---|---|---|
|Methods|Gap_↓_|Std|_p_-value|Gap_↓_|Std|_p_-value|
||LLM-bas|ed AHD:_GPT_|_-5-nano_ (reaso|ning: medium|)||
|ReEvo|7.70%|3.62%|0.0047|14.19%|4.79%|0.0015|
|HSEvo|4.77%|0.69%|0.0014|10.91%|2.03%|0.0006|
|PathWise(Ours)|1.93%|1.41%|-|4.67%|2.62%|-|
|||LLM-based A|HD:_DeepSee_|_k-V3.2_|||
|ReEvo|3.53%|0.98%|0.0034|8.59%|2.96%|0.0043|
|HSEvo|2.77%|1.00%|0.0403|6.40%|2.74%|0.0377|
|PathWise(Ours)|1.86%|0.41%|-|3.78%|1.50%|-|



_Table 13._ Statistical significance testing on KP-Constructive. Mean optimality gap (%), standard deviation (Std), and one-sided _t_ -test p-values between each baseline and PathWise are reported over 6 runs. 

|Test sets|_N_|=50,_W_=12_._5||_N_|=100,_W_=25||
|---|---|---|---|---|---|---|
|Methods|Gap_↓_|Std|_p_-value|Gap_↓_|Std|_p_-value|
|||LLM-based|AHD:_GPT-4o-_|_mini_|||
|MCTS-AHD|0.2583%|0.0133%|0.0002|0.1117%|0.0098%|0.0096|
|PathWise(Ours)|0.2217%|0.0075%|-|0.0983%|0.0041%|-|
||LLM-b|ased AHD:_GPT_|_-5-nano_ (reaso|ning: medium)|||
|MCTS-AHD|0.2167%|0.0151%|0.0020|0.0900%|0.0126%|0.0026|
|PathWise(Ours)|0.1117%|0.0538%|-|0.0517%|0.0214%|-|



# **F. Further Methodological Details & Extended Ablation Studies** 

In this section, Appendix F.1 presents the prompt templates used by the policy, world model, and critic agents. Appendix F.2 lists the exploration phrase inventories used for prompt-level diversity. Appendix F.3 provides the algorithmic pseudocode summarizing the overall procedure. Appendix F.4 reports extended ablation studies on PathWise hyperparameters. 

## **F.1. Prompt Templates for Agents** 

Prompts used across different agents are provided below. The initialization prompt used to generate heuristics in the initial population is described first, followed by the complete prompt templates governing the Policy, World Model, and Critic agents. Each agent operates under a predefined system prompt defining its functional role, paired with a structured user prompt dynamically populated from the current search state. These templates map how the entailment graph, routed reflections, and heuristic evaluations condition agent behavior. The problem descriptions, function descriptions, function signatures, and task-specific contexts follow formats used in ReEvo (Ye et al., 2024). 

## **Initialization Prompt** 

[SYSTEM PROMPT] 

You are an expert in the domain of optimization heuristics. 

[USER PROMPT] Write a {function_name} function for {problem_description} {function_description} Function signature: {function_signature} Create a novel heuristic approach for this problem. Format your response as: ‘‘‘python 

26 

**PathWise: Planning through World Model for Automated Heuristic Design via Self-Evolving LLMs** 

[your generated code here] ‘‘‘ Description: [Algorithmic description of this heuristic’s approach and key features less than 30 words] Derivation Rationale: [Brief explanation of the reasoning behind this heuristic design and why it should perform well for this problem] 

## **Policy Agent Prompt** 

[SYSTEM PROMPT] You are an expert in heuristic evolution and search strategy design. Your task is to select parent(s) from the given candidates and provide a directive that guides the generation of better heuristics. -----------------------------------------------------------[USER PROMPT] You are controlling the evolutionary search for {problem_description} {function_description} I have k existing heuristics listed below. For each heuristic, I provide its ID, description, the heuristics used to derive it with their descriptions and objective values, its derivation logic, its full code, and its own objective value: ID: # Heuristic identifier Description: # High-level description of the heuristic idea Heuristics used to derive this candidate: # List of parent heuristics with their descriptions and objective values used to generate this heuristic Derivation logic: # Description of how this heuristic was constructed or modified (derivation rationale) Code: # Full Python implementation of the heuristic function Objective value: # Objective value on the evaluation dataset ... ID: # Heuristic identifier Description: # High-level description of the heuristic idea Heuristics used to derive this candidate: # List of parent heuristics with their descriptions and objective values used to generate this heuristic Derivation logic: # Description of how this heuristic was constructed or modified (derivation rationale) Code: # Full Python implementation of the heuristic function Objective value: # Objective value on the evaluation dataset Reflection: # Reflection generated by the Policy Critic Agent based on the outputs of the previous entailment step Task: Choose one or more parent(s) and propose a directive for deriving a new heuristic, based on the reflection and current heuristic candidates. Your selected parent(s) and directive should help guide the creation of heuristics that achieve lower objective values in future generations. {exploratory_phrase} You must choose parent ID(s) only from the k heuristics listed above. Consider the following when choosing parent(s) and generating the directive: - Objective values and performance trends - Diversity of approaches in the current candidates - Derivation history (what has been tried and what has not been explored yet) Format your response as: PARENTS: [list of ID(s) selected from current heuristic candidates] DIRECTIVE: [novel instruction less than 2 sentences describing how to modify, extend, or invent new logic from the selected parent(s)] Do not give additional explanations. 

27 

**PathWise: Planning through World Model for Automated Heuristic Design via Self-Evolving LLMs** 

## **World Model Agent Prompt** 

[SYSTEM PROMPT] You are an expert in the domain of optimization heuristics. -----------------------------------------------------------[USER PROMPT] Write a {function_name} function for {problem_description} {function_description} I have k existing algorithms with their codes and objective values as follows: ID: # Parent heuristic identifier # Parent heuristic description # Parent heuristic full code Objective value: # Objective value on the evaluation dataset ... ID: # Parent heuristic identifier # Parent heuristic description # Parent heuristic full code Objective value: # Objective value on the evaluation dataset Directive: # Derivation rationale generated by the Policy Agent describing how to # modify, combine, or invent new logic from the parent heuristic(s) {exploratory_phrase} Reflection: # Reflection generated by the World Model Critic Agent based on the outputs of the previous entailment step Write an improved function {function_signature}_v2 that follows the directive and reflection by keeping the same function signature. The new algorithm should have an objective value lower than all algorithms. 

Output algorithm description and code. First write: ‘‘‘Description: <Algorithmic description of the heuristic’s approach using less than 30 words>‘‘‘. Then enclose your code with Python code block:‘‘‘python ...‘‘‘ 

## **Policy Critic Prompt** 

[SYSTEM PROMPT] You are an expert in analyzing heuristic evolution. Your task is to give hints for how future parent choices and directive designs should improve the heuristic evolution process. -----------------------------------------------------------[USER PROMPT] Analyze heuristic evolution for {problem_description} {function_description} I have k existing heuristics listed below. For each heuristic, I provide its ID, description, the heuristics used to derive it with their descriptions and objective values, its derivation logic, its full code, and its own objective value: ID: # Heuristic identifier Description: # High-level description of the heuristic idea Heuristics used to derive this candidate: # List of parent heuristics with their descriptions and objective values used to generate this heuristic Derivation logic: # Description of how this heuristic was constructed or modified (derivation rationale) Code: # Full Python implementation of the heuristic function Objective value: # Objective value on the evaluation dataset ... ID: # Heuristic identifier Description: # High-level description of the heuristic idea Heuristics used to derive this candidate: # List of parent heuristics with their descriptions and objective values used to generate this heuristic Derivation logic: # Description of how this heuristic was constructed or modified (derivation rationale) Code: # Full Python implementation of the heuristic function 

28 

**PathWise: Planning through World Model for Automated Heuristic Design via Self-Evolving LLMs** 

Objective value: # Objective value on the evaluation dataset Actions taken and their results: Based on the heuristic candidates above, several evolution steps (called actions) were performed. Each action consists of: - a chosen parent set, - a directive describing how to modify or combine those parents, and - the rollouts generated from that directive. The actions below are listed from best to worst by the average objective value of their rollouts. Each rollout is one heuristic produced from an action, including its description and objective value. Action 0 Parent IDs: # Parent IDs selected in this action Directive: # Directive (derivation rationale) used in this action Rollouts: rollout_0: # Rollout description and objective value rollout_1: # Rollout description and objective value ... Action N_a - 1 Parent IDs: # Parent IDs selected in this action Directive: # Directive (derivation rationale) used in this action Rollouts: rollout_0: # Rollout description and objective value rollout_1: # Rollout description and objective value 

Reflection Task: 1. Analyze the outcomes of the taken actions based on current heuristic candidates. Identify patterns behind which actions performed best and which performed worst, evaluate how their rollouts improved upon or became worse than their parent heuristics, and diagnose the key reasons behind these shifts to ground your hints. 2. Correlate success with the parent selection strategies and directives above. You respond with concise hints for both improving parent selection and directives toward lower objective values. 

Do not refer to specific parent IDs, rollout names, or code blocks. Write your reflection using less than 60 words. 

## **World Model Critic Prompt** 

[SYSTEM PROMPT] You are an expert in the domain of optimization heuristics. Your task is to give hints for designing better heuristics. 

-----------------------------------------------------------[USER PROMPT] Below are two {function_signature} functions for {problem_description} {function_description} 

You are provided with two code versions below, where the second version performs better than the first one. Worse code: Description: # Description of the lower-performing heuristic Objective value: # Objective value of the lower-performing heuristic Code: # Full Python implementation of the lower-performing heuristic Better code: Description: # Description of the higher-performing heuristic Objective value: # Objective value of the higher-performing heuristic Code: # Full Python implementation of the higher-performing heuristic 

You respond with some hints for designing better heuristics to achieve lower objective values, based on the two code versions. Phrase your hints as design principles, not tied to names, paths, or labels appearing in the code. Write less than 30 words. 

29 

**PathWise: Planning through World Model for Automated Heuristic Design via Self-Evolving LLMs** 

## **F.2. Exploration Phrase Inventories** 

Exploration phrase inventories used to perturb the prompts of the Policy and World Model agents during heuristic evolution are provided below. As shown in Algorithm 3, at each inner entailment step _t_ , an exploration phrase is sampled from Φp for the Policy Agent and from Φwm for the World Model Agent with probability _ε_ ( _t_ ). These phrases encourage novelty early in the search and gradually diminish as the exploration rate anneals, promoting behavioral diversity without modifying the entailment-graph state. 

## **Policy Agent Explorative Phrase Inventory (** Φp **)** 

- •Favor unusual parent combinations. 

- •Explore less common heuristic structures. 

- •Prioritize novelty in parent selection. 

- •Try a nonstandard way to blend parent logic. 

- •Choose parents that differ the most in style. 

- •Favor unconventional directives. 

- •Promote risky or experimental parent mixes. 

- •Favor out-of-pattern directive ideas. 

- •Choose parents with conflicting logic for innovation. 

- •Prioritize exploration over refinement for this step. 

- •Encourage a fresh angle on how parents are merged. 

- •Introduce a twist in the directive logic. 

- •Propose a directive unlike previously tried patterns. 

- •Inject a novel angle into how parents are combined. 

- •Favor creativity over safety in directive formation. 

- •Promote a directive that breaks common heuristic habits. 

- •Invent a directive that departs from usual conventions. 

- •Attempt to introduce more novel mechanisms. 

## **World Model Agent Explorative Phrase Inventory (** Φwm **)** 

- •Create a new algorithm that has a totally different form from the given algorithms. 

- •Try generating codes with different structures, flows or algorithms. 

- •Introduce a novel program segment that fundamentally changes the logic. 

- •Create new mechanisms or equations that have not appeared before. 

- •Attempt to introduce more novel mechanisms and new equations or programme segments. 

- •Modify the structure of the algorithm rather than refining existing parts. 

- •Develop a new pathway in the code that changes how decisions are made. 

- •Construct a new rule or formulation that improves the existing methods. 

- •Come up with an original computational idea that changes the overall procedure. 

## **F.3. Algorithmic Pseudocode** 

Algorithm 1 summarizes the overall **PathWise** procedure, which organizes heuristic search across outer population updates and inner entailment graph construction. Algorithm 2, ENTAILMENTGRAPHCONSTRUCTION, corresponds to the inner entailment graph construction shown in Figure 2(a). Algorithm 3, ENTAILMENTSTEP, specifies the multi-agent interaction underlying each inner update, aligning with Figure 2(b). 

Across all algorithms, each node is represented as _v_ = ( _h, κ, d, P_ ( _h_ ; _D_ ) _,_ PM), where _h_ denotes executable heuristic code, _κ_ the derivation rationale, _d_ a compact algorithmic description, _P_ ( _h_ ; _D_ ) performance on the training set, and PM the parent metadata. In the initial population _P_ 0, parent metadata is empty since no entailment has yet occurred; in later populations, root nodes inherit their stored fields, including PM when available. 

30 

**PathWise: Planning through World Model for Automated Heuristic Design via Self-Evolving LLMs** 

**Algorithm 1** PathWise: Planning through World Model for Automated Heuristic Design via Self-Evolving LLMs **Inputs:** Training instance set _D_ ; performance _P_ ( _h_ ; _D_ ); population size _Np_ ; actions per step _Na_ ; rollouts per action _Nw_ ; max inner entailment steps _I_ max; max total evaluations _ne_ ; linear schedule ( _ε_<sup>init</sup> _, ε_<sup>final</sup> ); phrase lists Φp, Φwm. **Outputs:** Best overall heuristic _h_<sup>_⋆_</sup> ; entailment graphs _{G}_ across outer iterations. 1: Initialize agents **_π_ p** _,_ **_π_ wm** _,_ **_π_ p** **~~c~~ ritic**<sup>_,_</sup><sup>**_π_**</sup> **wm critic** _▷_ Instantiate policy, world model, and critic LLMs 2: _r ←_ 0; _ℓ ←_ 0 _▷ℓ_ : evaluation counter over all rollouts 3: Initialize population _P_ 0; evaluate _P_ ( _h_ ; _D_ ) for each _h_ stored in nodes _v ∈P_ 0 4: _v_<sup>_⋆_</sup> _←_ arg max _{ P_ ( _h_ ; _D_ ) _| h ∈P_ 0 _} ▷_ Initialize best overall node (implicitly includes _h_<sup>_⋆_</sup> ) 5: _ρp_ (0) _←_ ∅; _ρwm_ (0) _←_ ∅ _▷_ Initial reflections are empty 6: **while** _ℓ< ne_ **do** 7: _\\ Inner entailment graph construction for population Pr_ 8: ( _Gt′, Vt_<sup>disc</sup><sup>_′_</sup> _, ρp, ρwm, ℓ, v_<sup>_⋆_</sup> ) _←_ ENTAILMENTGRAPHCONSTRUCTION( _Pr, ρp, ρwm, ℓ, v_<sup>_⋆_</sup> ) 9: _\\ Population update (leaf-first)_ 10: _F ←_ LeafNodes( _Gt′_ ) _▷_ Leaf nodes of _Gt′_ that involved in at least one entailment step 11: _R ←_ ( _Vt_<sup>_′_</sup> _∪ Vt_<sup>disc</sup><sup>_′_</sup> ) _\ F ▷_ All evaluated nodes (entailed or non-entailed), excluding leaf nodes of _Gt_<sup>_′_</sup> 12: **if** _|F| ≥ Np_ **then** 13: _Pr_ +1 _←_ Top _Np_ ( _F_ ) _▷_ Next population from best leaves 14: **else** 15: _Pr_ +1 _←F ∪_ Top _Np−|F|_ ( _R_ ) _▷_ Fill remaining slots from best non-leaves 16: **end if** 17: _r ← r_ + 1 18: **end while** 19: _h_<sup>_⋆_</sup> _←_ heuristic code stored in _v_<sup>_⋆_</sup> 20: **Output:** _h_<sup>_⋆_</sup> and entailment graphs _{G}_ 

**Population Initialization and Management Details.** In the initial population construction, we prompt the LLM 5 _Np_ times using the initialization prompt, evaluate all generated heuristics on _D_ train, and form _P_ 0 by selecting the top _Np_ heuristics with _distinct_ performance values _P_ ( _h_ ; _D_ train). This filtering avoids retaining multiple heuristics with identical evaluation outcomes arising from stochastic sampling. The same principle is applied during population management in later outer iterations: when the number of selected leaf nodes is insufficient, remaining population slots are filled by selecting non-leaf nodes with the highest performance values, again enforcing distinct performance values among selected heuristics. Together, these initialization and management rules promote a diverse set of heuristics in the population while preserving performance-based selection. 

**Algorithm 2** ENTAILMENTGRAPHCONSTRUCTION: Inner Entailment Loop for One Population **Inputs:** Population _Pr_ ; reflections _ρp_ (0) _, ρwm_ (0); counter _ℓ_ ; best overall node _v_<sup>_⋆_</sup> . **Outputs:** Graph _Gt′_ ; non-entailed nodes set _Vt_<sup>disc</sup><sup>_′_</sup> ; updated reflections; updated _ℓ_ and _v_<sup>_⋆_</sup> . 1: _V_ 0 _←Pr ▷_ Population elements are root nodes of the entailment graph, _v_ = ( _h, κ, d, P_ ( _h_ ; _D_ ) _,_ PM) 2: _E_ 0 _←_ ∅; _V_ 0<sup>disc</sup> _←_ ∅ 3: _s_ 0 _← V_ 0 _▷_ Initial state is the initial node set 4: _t ←_ 0 5: **while** ( _t < I_ max) _∧_ ( _|st| >_ 1) **do** _▷_ Run until _I_ max steps or the frontier collapses to one node 6: _\\ Entailment step_ 7: ( _Vt_ +1 _, Et_ +1 _, st_ +1 _, Vt_<sup>disc</sup> +1<sup>_, ρp_(</sup><sup>_t_+1)</sup><sup>_, ρwm_(</sup><sup>_t_+1)</sup><sup>_, v⋆, ℓ_)</sup> 8: _←_ ENTAILMENTSTEP( _Vt, Et, st, Vt_<sup>disc</sup> _, ρp_ ( _t_ ) _, ρwm_ ( _t_ ) _, v_<sup>_⋆_</sup> _, ℓ_ ) 9: _t ← t_ + 1 10: **end while** 11: _t_<sup>_′_</sup> _← t ▷_ Index of the final inner step for this outer iteration 12: _Gt′ ←_ ( _Vt′, Et′_ ) 13: **return** ( _Gt′, Vt_<sup>disc</sup><sup>_′_</sup> _, ρp_ ( _t_<sup>_′_</sup> ) _, ρwm_ ( _t_<sup>_′_</sup> ) _, ℓ, v_<sup>_⋆_</sup> ) 

31 

**PathWise: Planning through World Model for Automated Heuristic Design via Self-Evolving LLMs** 

**Algorithm 3** ENTAILMENTSTEP: Multi-Agent Entailment Update **Inputs:** ( _Vt, Et_ ); state _st_ ; non-entailed nodes set _Vt_<sup>disc</sup> ; reflections _ρp_ ( _t_ ) _, ρwm_ ( _t_ ); best overall node _v_<sup>_⋆_</sup> ; counter _ℓ_ . **Outputs:** ( _Vt_ +1 _, Et_ +1 _, st_ +1 _, Vt_<sup>disc</sup> +1<sup>);</sup><sup>_ρ_</sup> _p_<sup>(</sup><sup>_t_+1)</sup><sup>_, ρ_</sup> _wm_<sup>(</sup><sup>_t_+1); updated</sup><sup>_v⋆_and</sup><sup>_ℓ_.</sup> 1: _\\ Exploration schedule_ 2: _ε_ ( _ℓ_ ) _← ε_<sup>init</sup> + ( _ε_<sup>final</sup> _− ε_<sup>init</sup> ) _· ℓ/ne ▷_ Linear annealing with evaluation count 3: _\\ State shuffling_ 4: Randomly permute the order of nodes in _st_ before prompting 5: _\\ Policy agent sampling_ 6: **for all** _i ∈{_ 1 _, . . . , Na}_ **in parallel do** 7: _ui ∼_ Unif(0 _,_ 1) 8: **if** _ui < ε_ ( _ℓ_ ) **then** 9: _ϕ_<sup>(</sup><sup>_i_)</sup> _∼_ Uniform(Φp) 10: **else** 11: _ϕ_<sup>(</sup><sup>_i_)</sup> _←_ ∅ 12: **end if** 13: _a_<sup>(</sup> _t_<sup>_i_)</sup> = ( _S_<sup>(</sup><sup>_i_)</sup> _, κ_<sup>(</sup><sup>_i_)</sup> ) _∼_ **_π_ p** ( _· | st, ρp_ ( _t_ ) _,_ phrase = _ϕ_<sup>(</sup><sup>_i_)</sup> ) 14: PM<sup>(</sup><sup>_i_)</sup> _←{_ ( _dk, P_ ( _hk_ ; _D_ )) _| vk ∈ S_<sup>(</sup><sup>_i_)</sup> _} ▷_ Parent metadata for action _a_<sup>(</sup> _t_<sup>_i_)</sup> 15: **end for** 16: _\\ World model rollouts and evaluation_ 17: **for all** _i ∈{_ 1 _, . . . , Na}_ **in parallel do** 18: **for all** _j ∈{_ 1 _, . . . , Nw}_ **in parallel do** 19: _βi,j ∼_ Unif(0 _,_ 1) 20: **if** _βi,j < ε_ ( _ℓ_ ) **then** 21: _ψ_<sup>(</sup><sup>_i,j_)</sup> _∼_ Uniform(Φwm) 22: **else** 23: _ψ_<sup>(</sup><sup>_i,j_)</sup> _←_ ∅ 24: **end if** 25: ( _h_<sup>ˆ(</sup><sup>_i,j_)</sup> _, d_<sup>ˆ(</sup><sup>_i,j_)</sup> ) _∼_ **_π_ wm** � _·_ ��� _{_ ( _hk, dk_ ) _}vk∈S_ ( _i_ ) _, κ_ ( _i_ ) _, ρwm_ ( _t_ ) _,_ phrase = _ψ_ ( _i,j_ )� 26: Evaluate _P_ ( _h_<sup>ˆ(</sup><sup>_i,j_)</sup> ; _D_ ) _▷_ Cache _P_ ( _h_<sup>ˆ(</sup><sup>_i,j_)</sup> ; _D_ ) for selection/critics 27: **end for** 28: **end for** 29: _ℓ ← ℓ_ + _NaNw_ 30: _\\ Select best rollout and update graph_ 31: ( _i⋆, j⋆_ ) _←_ arg max _i,j P_ ( _h_<sup>ˆ(</sup><sup>_i,j_)</sup> ; _D_ ) 32: _v⋆ ←_ � _h_ ˆ ( _i⋆,j⋆_ ) _, κ_ ( _i⋆_ ) _, d_ ˆ( _i⋆,j⋆_ ) _, P_ (ˆ _h_ ( _i⋆,j⋆_ ); _D_ ) _,_ PM( _i⋆_ )� _▷_ Create entailed node _κ_<sup>(</sup><sup>_i⋆_)</sup> 33: _Vt_ +1 _← Vt ∪{v⋆}_ ; _Et_ +1 _← Et ∪{ S_<sup>(</sup><sup>_i⋆_)</sup> === _⇒ v⋆ } ▷_ Insert entailed node and edge 34: _Vt_<sup>disc</sup> +1<sup>_←V_</sup> _t_<sup>disc</sup> _∪_ � ( _h_<sup>ˆ(</sup><sup>_i,j_)</sup> _, κ_<sup>(</sup><sup>_i_)</sup> _, d_<sup>ˆ(</sup><sup>_i,j_)</sup> _, P_ ( _h_<sup>ˆ(</sup><sup>_i,j_)</sup> ; _D_ ) _,_ PM<sup>(</sup><sup>_i_)</sup> ) _|_ ( _i, j_ ) _̸_ = ( _i⋆, j⋆_ ) � _▷_ Accumulate non-entailed rollouts 35: **if** _P_ ( _h_<sup>ˆ(</sup><sup>_i⋆,j⋆_)</sup> ; _D_ ) _> P_ ( _h_<sup>_⋆_</sup> ; _D_ ) **then** 36: _v_<sup>_⋆_</sup> _← v⋆ ▷_ Update best overall node (implicitly updates best heuristic) 37: **end if** 38: _st_ +1 _←_ ( _st ∪{v⋆}_ ) _\_ ( _S_<sup>(</sup><sup>_i⋆_)</sup> _\ {v_<sup>_⋆_</sup> _}_ ) _▷_ Keep new node and best node; prune other used parents 39: _\\ Critic reflections_ 40: **for** _i_ = 1 **to** _Na_ **do** 41: _Rp_ ( _a_<sup>(</sup> _t_<sup>_i_))</sup><sup>_←_</sup> _N_ <u>1</u> _w_ � _Nj_ =1 _w_<sup>_P_(ˆ</sup><sup>_h_(</sup><sup>_i,j_);</sup><sup>_D_)</sup> _▷_ Reward signal used to rank actions for the policy critic 42: _Bp_<sup>(</sup><sup>_i_)</sup> _←{_ ( _d_<sup>ˆ(</sup><sup>_i,j_)</sup> _, P_ ( _h_<sup>ˆ(</sup><sup>_i,j_)</sup> ; _D_ )) _}_<sup>_N_</sup> _j_ =1<sup>_w_</sup> 43: **end for** 44: _ρp_ ( _t_ +1) _←_ **_π_ p critic** � _{_ ( _at_<sup>(</sup><sup>_i_)</sup><sup>_, Rp_(</sup><sup>_a_(</sup> _t_<sup>_i_))</sup><sup>_, B_</sup> _p_<sup>(</sup><sup>_i_))</sup><sup>_}N_</sup> _i_ =1<sup>_a,st_</sup> � _▷Rp_ used for action ranking; _Bp_<sup>(</sup><sup>_i_)</sup> summarizes rollout variation 45: ( _i_ min _, j_ min) _←_ arg min _i,j P_ ( _h_<sup>ˆ(</sup><sup>_i,j_)</sup> ; _D_ ) 46: **best** _←_ ( _h_<sup>ˆ(</sup><sup>_i⋆,j⋆_)</sup> _, d_<sup>ˆ(</sup><sup>_i⋆,j⋆_)</sup> _, P_ ( _h_<sup>ˆ(</sup><sup>_i⋆,j⋆_)</sup> ; _D_ )) 47: **worst** _←_ ( _h_<sup>ˆ(</sup><sup>_i_min</sup><sup>_,j_min)</sup> _, d_<sup>ˆ(</sup><sup>_i_min</sup><sup>_,j_min)</sup> _, P_ ( _h_<sup>ˆ(</sup><sup>_i_min</sup><sup>_,j_min)</sup> ; _D_ )) 48: _ρwm_ ( _t_ +1) _←_ **_π_ wm** **~~c~~ ritic**<sup>(</sup><sup>**best**</sup><sup>_,_</sup><sup>**worst**)</sup> 49: **return** ( _Vt_ +1 _, Et_ +1 _, st_ +1 _, Vt_<sup>disc</sup> +1<sup>_, ρ_</sup> _p_<sup>(</sup><sup>_t_+1)</sup><sup>_, ρ_</sup> _wm_<sup>(</sup><sup>_t_+1)</sup><sup>_, v⋆, ℓ_)</sup> 

## **F.4. Ablation on Hyperparameters of PathWise** 

In Section 4.2, we presented an ablation study using the step-by-step construction framework on TSP training and validation sets to evaluate performance across in-domain and out-of-distribution settings, focusing on the effectiveness of the core 

32 

**PathWise: Planning through World Model for Automated Heuristic Design via Self-Evolving LLMs** 

architectural choices and high-level mechanisms of PathWise. In this section, we further analyze the sensitivity of PathWise to additional hyperparameters that control the breadth and depth of the entailment and search process. These ablations examine the robustness of PathWise to reasonable parameter variations and clarify the rationale behind the selected default settings in terms of performance stability and computational efficiency. 

_Table 14._ Ablations on the number of policy actions per entailment step _Na_ and the number of world model rollouts per action _Nw_ in PathWise. We report optimality gaps (%) on training ( _<u>TSP50</u>_ <u>) and validation sets (</u> _TSP20_ , _TSP50_ ) for the step-by-step construction framework on TSP. 

|Methods|_TSP20_|_TSP50_|_TSP50_|
|---|---|---|---|
|PathWise(_Na_=2_, Nw_=2)|6.08%|9.72%|8.79%|
|_Na_=2_, Nw_=1|7.70%|10.76%|9.64%|
|_Na_=2_, Nw_=3|7.16%|10.36%|9.38%|
|_Na_=3_, Nw_=1|7.35%|11.39%|10.10%|
|_Na_=3_, Nw_=2|6.67%|10.06%|9.16%|
|_Na_=3_, Nw_=3|9.03%|11.44%|10.70%|



**Ablation on the number of policy actions and world model rollouts.** Table 14 studies the effect of the number of policy actions per entailment step _Na_ and the number of world model rollouts per action _Nw_ . These parameters control the local branching factor and the amount of simulated feedback available to the policy and critic agents. The results show that configurations with _Na>_ 1 and _Nw>_ 1 achieve comparable performance, indicating that both multiple actions and multiple rollouts are required for effective entailment. 

Comparisons between increasing _Na_ and increasing _Nw_ show that generating more candidate actions is more beneficial than adding additional rollouts for the same action. For example, increasing _Na_ with moderate _Nw_ ( _Na_ =3 _, Nw_ =2) outperforms increasing _Nw_ with fewer actions ( _Na_ =2 _, Nw_ =3). This is consistent with the design of the policy critic, which operates on compact heuristic descriptions rather than full executable code, and aligns with the critic ablations in Table 3 that highlight the dominant role of policy-level feedback. Exposing the critic to a more diverse set of action candidates therefore provides stronger comparative signals than repeatedly simulating the same action through additional world model rollouts. 

Increasing both _Na_ and _Nw_ to larger values ( _Na_ =3 _, Nw_ =3) degrades performance due to the excessive amount of context passed to the policy and critic agents. Conversely, reducing the configuration to smaller values, such as ( _Na_ =2 _, Nw_ =1), limits rollout diversity and reduces the comparative signals available to the critics. Overall, these observations support the default setting ( _Na_ =2 _, Nw_ =2) as a stable and efficient choice. 

_Table 15._ Ablations on the population size _Np_ in PathWise. We report optimality gaps (%) on training ( _<u>TSP50</u>_ ) and validation sets ( _TSP20_ , _TSP50_ ) for the step-by-step construction framework on TSP. 

|Methods|_TSP20_|_TSP50_|_TSP50_|
|---|---|---|---|
|PathWise(_Np_=6)|6.08%|9.72%|8.79%|
|_Np_=7|6.32%|10.12%|9.16%|
|_Np_=8|6.35%|10.15%|9.38%|
|_Np_=10|6.59%|11.28%|10.11%|



**Ablation on population size** _Np_ **.** Table 15 shows the effect of the population size _Np_ , which controls the number of heuristics retained across outer iterations. PathWise is insensitive to moderate increases in _Np_ , with similar performance for _Np_ =6 _,_ 7 _,_ 8. In contrast, increasing the population to _Np_ =10 degrades performance, as the larger context passed to the policy and policy critic during early entailment steps reduces their ability to reason about high-quality entailments. These results support the default choice _Np_ =6 as a balanced setting, providing a better performance–cost trade-off. 

_Table 16._ Ablations on the maximum number of inner entailment steps _I_ max in PathWise. We report optimality gaps (%) on training ( _<u>TSP50</u>_ <u>) and validation sets (</u> _TSP20_ , _TSP50_ ) for the step-by-step construction framework on TSP. 

|Methods|_TSP20_|_TSP50_|_TSP50_|
|---|---|---|---|
|PathWise(_I_max=3)|6.08%|9.72%|8.79%|
|_I_max=4|6.24%|10.20%|9.12%|



33 

**PathWise: Planning through World Model for Automated Heuristic Design via Self-Evolving LLMs** 

**Ablation on inner entailment steps** _I_ max **.** Table 16 evaluates the impact of the maximum number of inner entailment steps _I_ max, which controls the depth of multi-step entailment within each outer iteration. The results show that PathWise is not sensitive to this parameter within the tested range, with no significant performance differences observed. This reflects a trade-off in which too few entailment steps limit multi-step reasoning, while too many steps progressively reduce the available parent set and thereby reduce diversity, supporting the default choice _I_ max=3. 

In summary, these ablation results demonstrate that PathWise is not overly sensitive to its secondary hyperparameters within reasonable ranges, and they further justify the default parameter choices used in the main experiments. 



<!-- Start of picture text -->
def select_next_node(current_node,destination_node,unvisited_nodes,distance_matrix):    if not unvisited_nodes: return int(destination_node)    N=distance_matrix.shape[0]; frac=(N-len(unvisited_nodes))/max(1,N)    dw=1.0; sw=max(0.6*(1-frac),0.2); tw=0.8+0.9*frac; lw=0.3+0.7*frac  # s1 components (adaptive with lookahead and pruning)    cands=list(unvisited_nodes)    pool=sorted(cands,key=lambda c:float(distance_matrix[current_node,c]))[:6] if len(cands)>6 else cands    s1={}    for c in pool:        R=unvisited_nodes-{c}        avg=(sum(float(distance_matrix[c,u]) for u in R)/len(R)) if R else 0.0        look=(min(float(distance_matrix[c,u]) for u in R)) if R else float(distance_matrix[c,destination_node])        s1[c]=float(distance_matrix[current_node,c])*dw+avg*sw-float(distance_matrix[c,destination_node])*tw-look*lw-(1e-6 if c==destination_node else 0.0)    dest_in=(destination_node in unvisited_nodes); a,b,cp=1.0,2.0,1.0  # s2 components: dispersion toward distant unvisited, across all candidates    s2={}    for v in unvisited_nodes:        R=unvisited_nodes-{v}        md=(min(float(distance_matrix[v,u]) for u in R)) if R else 0.0        s2[v]=a*float(distance_matrix[current_node,v])+b*(float(distance_matrix[v,destination_node]) if dest_in else 0.0)-cp*md    w=0.2+0.8*frac  # Adaptive convex weight    best=min(pool,key=lambda c:w*s1[c]+(1-w)*s2.get(c,0.0)) if pool else min(unvisited_nodes,key=lambda c:distance_matrix[current_node,c])    return int(best) def select_next_node(current_node,destination_node,unvisited_nodes,distance_matrix):    if not unvisited_nodes: return int(destination_node)    N=distance_matrix.shape[0]; frac=(N-len(unvisited_nodes))/max(1,N)    dw=1.0; sw=max(0.6*(1-frac),0.2); tw=0.8+0.9*frac; lw=0.3+0.7*frac  # s1: adaptive, lookahead-aware score (near-neighbor pruning)    cands=list(unvisited_nodes)    pool=sorted(cands,key=lambda c:float(distance_matrix[current_node,c]))[:6] if len(cands)>6 else cands    dest_in=(destination_node in unvisited_nodes); a,b,c=1.0,2.0,1.0      # s2: dispersion-driven score toward distant unvisited nodes    w=min(0.95,max(0.05,0.3+0.6*frac))                                     # Adaptive convex combination    best=None; bv=1e100    for cand in pool:        R=unvisited_nodes-{cand}        avg=(sum(float(distance_matrix[cand,u]) for u in R)/len(R)) if R else 0.0        look=(min(float(distance_matrix[cand,u]) for u in R)) if R else float(distance_matrix[cand,destination_node])        s1=float(distance_matrix[current_node,cand])*dw+avg*sw-float(distance_matrix[cand,destination_node])*tw-look*lw-(1e-6 if cand==destination_node else 0.0)        md=(min(float(distance_matrix[cand,u]) for u in R)) if R else 0.0        s2=a*float(distance_matrix[current_node,cand])+b*(float(distance_matrix[cand,destination_node]) if dest_in else 0.0)-c*md        sc=w*s1+(1-w)*s2        if sc<bv: best,bv=cand,sc    return int(best if best is not None else min(unvisited_nodes,key=lambda c:distance_matrix[current_node,c])) def select_next_node(current_node,destination_node,unvisited_nodes,distance_matrix):    if not unvisited_nodes: return int(destination_node)    N=distance_matrix.shape[0]; frac=(N-len(unvisited_nodes))/max(1,N)    dens={c:sum(sorted(float(distance_matrix[c,o]) for o in unvisited_nodes if o!=c)[:3]) for c in unvisited_nodes}    pool=sorted(unvisited_nodes,key=lambda c:float(distance_matrix[current_node,c])-0.5*dens[c])[:6] if len(unvisited_nodes)>6 else list(unvisited_nodes)    if not pool: return int(min(unvisited_nodes,key=lambda c:distance_matrix[current_node,c]))    dw=1.0; sw=max(0.6*(1-frac),0.2); tw=0.8+0.9*frac; lw=0.3+0.7*frac  # S1: entail_1_0's normalized monotone-weighted score over a small pool    s1={}; s2={}    for c in pool:        R=unvisited_nodes-{c}; dcur=float(distance_matrix[current_node,c]); ddst=float(distance_matrix[c,destination_node])        avg=(sum(float(distance_matrix[c,u]) for u in R)/len(R)) if R else 0.0; look=(min(float(distance_matrix[c,u]) for u in R)) if R else ddst        s1[c]=dcur*dw+avg*sw-ddst*tw-look*lw        md=(min(float(distance_matrix[c,u]) for u in R)) if R else 0.0  # S2: rollout_0_3's monotone convex combination (score1 and score2 rolled together)        s2[c]=dcur+0.8*(ddst if destination_node in unvisited_nodes else 0.0)-0.9*md    w=min(0.95,max(0.05,0.2+0.75*frac))  # Combine via progress-dependent weight, then normalize and tie-break by proximity    comb={c:w*s1[c]+(1-w)*s2[c] for c in pool}; mn,mx=min(comb.values()),max(comb.values())    return int(min(pool,key=lambda c:(((comb[c]-mn)/(mx-mn)) if mx>mn else 0.0,distance_matrix[current_node,c],c))) def select_next_node(current_node,destination_node,unvisited_nodes,distance_matrix):    if not unvisited_nodes: return int(destination_node)    N=distance_matrix.shape[0]; frac=(N-len(unvisited_nodes))/max(1,N)                      # progress    dw=1.0; sw=max(0.6*(1-frac),0.2); tw=0.8+0.9*frac; lw=0.3+0.7*frac                       # adaptive weights    ALPHA=0.6; K=3; MAXP=6                                                                   # density params + cap    cands=list(unvisited_nodes); pool=sorted(cands,key=lambda c:float(distance_matrix[current_node,c]))[:MAXP] if len(cands)>MAXP else cands  # near-pool    if not pool: return int(min(unvisited_nodes,key=lambda c:distance_matrix[current_node,c]))  # fallback    s1={}; s2={}    for c in pool:        R=unvisited_nodes-{c}; dcur=float(distance_matrix[current_node,c]); ddst=float(distance_matrix[c,destination_node])        avg=(sum(float(distance_matrix[c,u]) for u in R)/len(R)) if R else 0.0; look=(min(float(distance_matrix[c,u]) for u in R)) if R else ddst  # 1-step lookahead        s1[c]=dcur*dw+avg*sw-ddst*tw-look*lw                                                   # S1: lookahead + destination bias        ds=sorted(distance_matrix[c,u] for u in R) if R else []; ld=sum(ds[:min(K,len(ds))]) if ds else 0.0  # local kNN density        s2[c]=dcur-ALPHA*ld+ddst                                                               # S2: diversify via density penalty    w=min(0.95,max(0.05,0.2+0.75*frac))                                                        # monotone mix    comb={c:w*s1[c]+(1-w)*s2[c] for c in pool}; mn,mx=min(comb.values()),max(comb.values())    # combine    norm={c:(comb[c]-mn)/(mx-mn) if mx>mn else 0.0 for c in pool}                              # normalize    return int(min(pool,key=lambda c:(norm[c],distance_matrix[current_node,c],c)))             # tie-break def select_next_node(current_node,destination_node,unvisited_nodes,distance_matrix):    if not unvisited_nodes: return int(destination_node)    N=distance_matrix.shape[0]; frac=(N-len(unvisited_nodes))/max(1,N)    MAX_POOL=6; cands=list(unvisited_nodes)    pool=sorted(cands,key=lambda c:float(distance_matrix[current_node,c]))[:MAX_POOL] if len(cands)>MAX_POOL else cands  # cap candidate pool    dw=1.0; sw=max(0.6*(1-frac),0.2); tw=0.8+0.9*frac; lw=0.3+0.7*frac        # s1: adaptive, lookahead-aware score    dest_in=(destination_node in unvisited_nodes); a,b,c=1.0,2.0,1.0          # s2: dispersion-driven score    s1={}; s2={}; dcur={}    for v in pool:        dcur[v]=float(distance_matrix[current_node,v]); R=unvisited_nodes-{v}; ddst=float(distance_matrix[v,destination_node])        avg=(sum(float(distance_matrix[v,u]) for u in R)/len(R)) if R else 0.0        look=(min(float(distance_matrix[v,u]) for u in R)) if R else ddst        s1[v]=dcur[v]*dw+avg*sw-ddst*tw-look*lw        md=(min(float(distance_matrix[v,u]) for u in R)) if R else 0.0        s2[v]=a*dcur[v]+b*(ddst if dest_in else 0.0)-c*md    mn1,mx1=min(s1.values()),max(s1.values()); mn2,mx2=min(s2.values()),max(s2.values())    n1={v:(s1[v]-mn1)/(mx1-mn1) if mx1>mn1 else 0.0 for v in pool}    n2={v:(s2[v]-mn2)/(mx2-mn2) if mx2>mn2 else 0.0 for v in pool}    w=max(0.05,min(0.95,0.25+0.65*frac))                                      # Monotone, progress-aware convex combination weight    return int(min(pool,key=lambda v:(w*n1[v]+(1-w)*n2[v],dcur[v])))<br>Hybrid adaptive scoring combining near-neighbor lookahead withdispersion, weighted by progress to minimize a combined score. Hybrid adaptive scoring: blend near-neighbor lookahead with dispersiontoward distant nodes using a fraction-based convex weight. Density-aware dual-score heuristic weighted by progress, thennormalized with proximity-based tie-break. Hybrid adaptive scoring with density diversification, destination bias, and1-step lookahead, using a monotone weight and a small pool,normalizing scores for robust choice. Blend adaptive s1-based score with local-density score, normalizeacross a capped candidate pool, and convexly combine with amonotone, progress-aware weight.<br>s1 from entail_0_0’s adaptive, lookahead-aware design with near-neighbor pruning,Construct a hybrid heuristic that computes two scores for each unvisited candidate:destination. Combine them with an adaptive convex weight w(fraction_visited) andand s2 from init_1’s dispersion toward distant unvisited nodes toward theselect the candidate minimizing w*s1 + (1-w)*s2. s1 from entail_0_0’s adaptive, lookahead-aware design with near-neighbor pruning,Construct a hybrid heuristic that computes two scores for each unvisited candidate:destination. Combine them with an adaptive convex weight w(fraction_visited) andand s2 from init_1’s dispersion toward distant unvisited nodes toward theselect the candidate minimizing w*s1 + (1-w)*s2. dependent weight, normalize across the pool, and tie-break by closer distance to theDerive a new heuristic by computing two scores per candidate: S1 via entail_1_0'snormalized monotone-weighted score over a small pool, and S2 via rollout_0_3'smonotone convex combination; then combine them with a fraction-visited–current node. candidate pruning, using a monotone progress weight and a small capped pool, thenselect the candidate with the lowest normalized score (tie-break by smaller distancenormalization with rollout_0_4's destination-biased 1-step lookahead and nearest-Derive a new heuristic by merging entail_0_2's adaptive s1+s2 hybrid andto current node). convex combination using a monotone weight w(fraction_visited). Normalize scoresCreate a new heuristic by blending entail_0_1’s adaptive s1 with near-neighborlookahead and dispersion, with init_5’s local-density-based score into a singleacross candidates and cap the candidate pool to a small fixed size to reduceinstability.<br>6.777 6.755 6.717 6.696 6.931<br>- Prioritize parent pairs that combine<br>complementary signals (adaptive lookahead<br>+ dispersion) and validate across multiple<br>instances to avoid overfitting to a single case.<br>- Use stable, bounded monotone weights with<br>consistent normalization; guard against pool-<br>size bias by adaptive but capped candidate<br>pools.<br>- Include robust fallback to<br>nearest/destination when needed.<br>- Use simple, deterministic tie-breakers tostabilize evolution.<br>Create a new select_next_node that combinesv4's adaptive lookahead/density scoring with v3's Select parents that are complementary (one providinglookahead/destination bias, another providing<br>normalization over a density-aware candidate density/diversification) rather than redundant; prefer parents<br>pool, using a monotone, fraction-visited weight to with proven normalization/stability. Directives should enforce<br>blend two scores (S1 and S2) and tie-break bydistance from the current node. small capped candidate pools, normalize component scores,use monotone progress-dependent convex weights, includelight 1 ‑ step lookahead and simple deterministic tie ‑ breaks;<br>avoid oversized pools.<br>- Blend diverse signals (local gain +<br>global dispersion).<br>- Use density-aware candidate pools to<br>preserve diversity, with bounded size for<br>efficiency.<br>- Normalize before combining; adjust<br>weight by progress; tie-break by<br>proximity.<br>def select_next_node_v2(current_node,destination_node,unvisited_nodes,distance_matrix):    if not unvisited_nodes: return int(destination_node)    N=distance_matrix.shape[0]; frac=(N-len(unvisited_nodes))/max(1,N)    CAND_POOL_MAX=7; K=3; K2=3    cands=list(unvisited_nodes)    dens={c:sum(sorted(float(distance_matrix[c,o]) for o in cands if o!=c)[:K]) for c in cands}  # Density scores: sum of distances to the K nearest other unvisited nodes    pool=sorted(cands,key=lambda c:distance_matrix[current_node,c]-0.4*dens[c])[:CAND_POOL_MAX] if len(cands)>CAND_POOL_MAX else cands  # density-aware candidate pool    if not pool: return int(min(unvisited_nodes,key=lambda c:distance_matrix[current_node,c]))    dw=1.0; sw=max(0.5*(1-frac),0.15); tw=0.7+0.9*frac; lw=0.25+0.65*frac; ALPHA=0.65  # S1: adaptive lookahead    s1={}; s2={}    for c in pool:        dcur=float(distance_matrix[current_node,c]); R=unvisited_nodes-{c}; ddst=float(distance_matrix[c,destination_node])        avg=(sum(float(distance_matrix[c,u]) for u in R)/len(R)) if R else 0.0        look=(min(float(distance_matrix[c,u]) for u in R)) if R else ddst        s1[c]=dcur*dw+avg*sw-ddst*tw-look*lw        ds=sorted(distance_matrix[c,u] for u in R) if R else []; ld=sum(ds[:min(K2,len(ds))]) if ds else 0.0  # S2: dispersion-focused dispersion toward unvisited nodes        ddst2=ddst if destination_node in unvisited_nodes else 0.0        s2[c]=dcur+0.65*ddst2-0.85*ld    w=min(0.95,max(0.05,0.2+0.75*frac))  # Blend scores with progress-based weight    comb={c:w*s1[c]+(1-w)*s2[c] for c in pool}    mn,mx=min(comb.values()),max(comb.values())    norm={c:(comb[c]-mn)/(mx-mn) if mx>mn else 0.0 for c in pool}  # Normalize across the pool    return int(min(pool,key=lambda c:(norm[c],distance_matrix[current_node,c],c)))  # Tie-breaker: smallest normalized score, then smallest distance to current, then smallest id Balance exploration and exploitation with progress-dependent weights; pre-filter candidate pool by<br>density; normalize blended scores; consider local<br>Density-aware blend of adaptive lookahead and dispersion scores, normalizedand merged with progress-based weight, selecting the next unvisited node. density and dispersion to steer toward diverse, under-visited areas.<br>then combine them with a fraction-visited–dependent weight, normalize across the pool, andmonotone-weighted score over a small pool, and S2 via vDerive a new heuristic by computing two scores per candidate: S1 via vtie-break by closer distance to the current node.3's monotone convex combination;4's normalized<br>6.554<br><!-- End of picture text -->

_Figure 4._ Example of PathWise at outer iteration _r_ = 1 and entailment step _t_ = 2, showing the entailed node _v⋆_ . The current state _st_ contains nodes _{v_ 1 _, . . . , v_ 5 _}_ . The policy agent _πp_ selects a parent set and generates a derivation rationale, which is executed by the world model _πwm_ to entail a new node. The resulting entailed node is _v⋆_ with _i⋆_ = 0 and _j⋆_ = 1, as shown. The policy and world model critics provide routed reflections at step _t_ , while shaded boxes indicate the updated reflections at step _t_ + 1, conditioning the next step. 

# **G. Output Examples of PathWise** 

In this section, we provide example outputs of PathWise, where Figures 4 and 5 visualize representative entailment steps during heuristic design for TSP using GPT-5-nano (medium) within the constructive framework. Each figure highlights the entailed node selected at a given outer iteration and inner entailment step, together with the associated policy action, world model rollout, and routed critic feedbacks that guide the entailment of _v⋆_ . Due to space constraints, the heuristic code displayed in the nodes is simplified and refactored by GPT-5.2, and parent metadata is omitted. In the derivation 

34 

**PathWise: Planning through World Model for Automated Heuristic Design via Self-Evolving LLMs** 

rationales of nodes in _st_ , nodes are referred to by unique identifiers of the form entail ~~X Y~~ or rollout ~~X Y~~ , indicating whether the node is entailed or discarded at outer iteration _X_ and inner entailment step _Y_ ; otherwise, we use the notation _v_ for notational convenience in the figures. 

We observe that parent selection by the policy agent is not driven purely by performance ranking; instead, it reflects higher-level reasoning over derivation history, diversity, and prior entailment context encoded in the graph state. In addition, feedback from the world model critic frequently emphasizes reducing algorithmic complexity and improving execution efficiency through code-level refinements, such as removing redundant computations. Finally, the heuristics often maintain an internal state—implemented via function attributes such as a step counter and progress-dependent variables—which allows the selection behavior to adapt over construction steps rather than remaining static throughout the solution process. 



<!-- Start of picture text -->
def select_next_node_v2(current_node,destination_node,unvisited_nodes,distance_matrix):    if not unvisited_nodes: return int(destination_node)    s=state; N=distance_matrix.shape[0]; frac=(N-len(unvisited_nodes))/max(1,N); cands=list(unvisited_nodes)    div=estimate_diversity_v2(set(cands),distance_matrix)  # diversity entropy from sampled pair distances    k=pool_size_v2(s,div,frac)  # pool size via monotone gate and diversity    dd={c:float(distance_matrix[c,destination_node]) for c in cands}; dens=knn_density_v2(cands,distance_matrix,K=max(2,int(round(3-frac))))  # kNN density sum    base=base_score_v2(current_node,unvisited_nodes,distance_matrix,dd,alpha=s["alpha"],beta=s["beta"])  # dist - alpha*avg_rem - beta*dest    fs=refine_score_v2(cands,unvisited_nodes,distance_matrix,base,dens,div,gamma=s["gamma"],ent_w=s["entropy_weight"])  # add entropy + cross-div penalty    pool=sorted(cands,key=lambda c:fs[c])[:k] if len(cands)>k else cands  # density-aware candidate pool    if not pool: return int(min(unvisited_nodes,key=lambda c:distance_matrix[current_node,c]))    sc=lookahead_score_v2(current_node,destination_node,unvisited_nodes,distance_matrix,pool,dd,dens,gamma=s["gamma"],frac=frac)  # 1-step lookahead score    norm=normalize_scores_v2(sc)  # min-max normalize across pool    bests=argmin_bucket_v2(norm,tol=1e-12)  # candidates within tolerance of best    # Updates: last_best, history, plateau, velocity, gate, gamma, cooldown    update_progress_state_v2(s,best=min(norm[c] for c in bests),frac=frac,div=div)    # Chooses: stratified/pareto reservoir from near-best candidates    chosen=reservoir_pick_v2(bests,norm,current_node,distance_matrix,s)    return int(chosen) def select_next_node(current_node,destination_node,unvisited_nodes,distance_matrix):    if not unvisited_nodes: return int(destination_node)    s=state  # persistent state: pools, gates, weights, history, velocity    s["step_counter"]=s.get("step_counter",0)+1; N=distance_matrix.shape[0]; frac=(N-len(unvisited_nodes))/max(1,N); cands=list(unvisited_nodes)    # helpers assumed defined: candidate_entropy_v2, estimate_diversity_v3, knn_density_v2, base_score_v2, lookahead_score_v2, normalize_scores_v2, stratified_reservoir, pareto_reservoir_v2_simple    div=estimate_diversity_v3(set(cands),distance_matrix); PM,PMX=int(s["POOL_MIN"]),int(s["POOL_MAX"]); gate=float(s["progress_gate"])    k=int(round(PM+(PMX-PM)*div*(1-frac))); pm=max(2,int(round(PM*(0.5+0.5*gate)))); px=max(pm,int(round(PMX*(0.5+0.5*gate)))); k=max(pm,min(max(PM,k),px)); s["pool_size"]=k  # diversity + gate-driven pool size    a,b,ew=float(s["alpha"]),float(s["beta"]),float(s["entropy_weight"]); gam=float(s["gamma"]); dd={c:float(distance_matrix[c,destination_node]) for c in cands}    dens=knn_density_v2(cands,distance_matrix,K=max(2,int(round(3-frac)))); base=base_score_v2(current_node,unvisited_nodes,distance_matrix,dd,alpha=a,beta=b)  # density + base score    fs={c:base[c]-gam*dens[c]-ew*candidate_entropy_v2(c,unvisited_nodes,distance_matrix) for c in cands}  # density + entropy refinement    pool=(sorted(cands,key=lambda c:fs[c])[:k] if len(cands)>k else cands) or [min(unvisited_nodes,key=lambda c:distance_matrix[current_node,c])]  # pool + fallback    norm=normalize_scores_v2(lookahead_score_v2(current_node,destination_node,unvisited_nodes,distance_matrix,pool,dd,dens,gamma=gam,frac=frac))  # pool lookahead + normalize    best=min(norm.values()); bests=[c for c,v in norm.items() if abs(v-best)<=1e-12]; RES=max(2,min(int(round(0.5*max(PM,k))),len(bests))); mode=s.get("reservoir_mode","stratified")    res=(pareto_reservoir_v2_simple(bests,RES,scores=norm,dist_current={c:distance_matrix[current_node,c] for c in bests}) if mode=="pareto" else stratified_reservoir(bests,RES)); chosen=(res[0] if res else min(pool,key=lambdac:distance_matrix[current_node,c]))    delta=(0.0 if s.get("last_norm_best") is None else s["last_norm_best"]-best); s["last_norm_best"]=best; s["velocity"]=0.7*s.get("velocity",0.0)+0.3*delta    s["progress_gate"]=min(1.0,gate+0.15) if delta>0 else max(s["progress_gate"],gate); s["gamma"]=max(0.05,min(0.95,gam*(0.5+0.5*s["progress_gate"])))  # monotone gate + gamma    s["improvement_history"].append(delta); plateau=(len(s["improvement_history"])>=3 and all(abs(g)<1e-6 for g in s["improvement_history"])); s["stagnation_counter"]=s.get("stagnation_counter",0)+1 if plateau else 0    if s["stagnation_counter"]>=2: s["reservoir_mode"]="pareto" if mode=="stratified" else "stratified"    if s["stagnation_counter"]>0: s["progress_gate"]=max(s["progress_gate"]-0.05,0.0)    return int(chosen) def select_next_node(current_node,destination_node,unvisited_nodes,distance_matrix)->int:    # assumes available: candidate_entropy,estimate_diversity,stratified_reservoir,pareto_reservoir    if not hasattr(select_next_node,"_st"):select_next_node._st={"PM":4,"PX":16,"a":0.35,"b":0.50,"g":0.25,"ew":0.35,"gate":0.5,"mode":"stratified","last":None,"stag":0,"t":0,"sw":-2}    st=select_next_node._st;st["t"]+=1    if not unvisited_nodes:return int(destination_node) # safety    N=distance_matrix.shape[0];fv=(N-len(unvisited_nodes))/max(1,N);cand=list(unvisited_nodes)    div=estimate_diversity(set(cand),distance_matrix) # diversity estimate    pool=max(2,min(int(round(st["PM"]+(st["PX"]-st["PM"])*div*(1-fv))),int(round(st["PX"]*(0.5+0.5*st["gate"]))))) # diversity+gate pool size    K=max(2,int(round(3-fv)))    dens={c:sum(sorted(float(distance_matrix[c,o]) for o in cand if o!=c)[:min(K,max(0,len(cand)-1))]) if len(cand)>1 else 0.0 for c in cand} # local density    base={c:float(distance_matrix[current_node,c])-st["a"]*(sum(float(distance_matrix[c,o]) for o in (unvisited_nodes-{c}))/max(1,len(unvisited_nodes)-1))-st["b"]*float(distance_matrix[c,destination_node]) for c in cand} # base lookahead score    fs={c:base[c]-st["g"]*dens[c]-st["ew"]*candidate_entropy(c,unvisited_nodes,distance_matrix) for c in cand} # entropy+density refinement    pool_c=sorted(cand,key=lambda c:fs[c])[:pool]    if not pool_c:return int(min(unvisited_nodes,key=lambda c:distance_matrix[current_node,c])) # fallback    w=0.25+0.50*fv    s={c:float(distance_matrix[current_node,c])-w*(sum(float(distance_matrix[c,o]) for o in (unvisited_nodes-{c}))/max(1,len(unvisited_nodes)-1))-0.4*float(distance_matrix[c,destination_node])-0.25*min((float(distance_matrix[c,o]) for o in (unvisited_nodes-{c})),default=float(distance_matrix[c,destination_node]))-st["g"]*dens.get(c,0.0) for c in pool_c} # pool rescoring    lo,hi=min(s.values()),max(s.values());ns={c:((s[c]-lo)/(hi-lo) if hi>lo else 0.0) for c in pool_c} # normalize    best=min(ns.values());best_c=[c for c,v in ns.items() if abs(v-best)<=1e-12] # select ties    RES=max(2,min(len(best_c),pool//2));res=pareto_reservoir(best_c,RES,scores=ns,dist_current={c:float(distance_matrix[current_node,c]) for c in best_c}) if st["mode"]=="pareto" else stratified_reservoir(best_c,RES) # reservoir    delta=0.0 if st["last"] is None else (st["last"]-best);st["last"]=best;st["stag"]=st["stag"]+1 if abs(delta)<1e-6 else 0 # stagnation proxy    st["gate"]=min(1.0,st["gate"]+0.15) if delta>0 else max(0.0,st["gate"]-0.15);st["g"]=max(0.05,min(0.95,st["g"]*(0.5+0.5*st["gate"]))) # adaptive gate+gamma    if st["stag"]>=2 and (st["t"]-st["sw"]>=2):st["mode"]="pareto" if st["mode"]=="stratified" else "stratified";st["sw"]=st["t"] # switch reservoir    return int(res[0] if res else min(pool_c,key=lambda c:distance_matrix[current_node,c])) # final pick def select_next_node(current_node:int,destination_node:int,unvisited_nodes:Set[int],distance_matrix:np.ndarray)->int:    # assumes: candidate_entropy,estimate_diversity,stratified_reservoir,pareto_reservoir (and uses only their outputs)    if not hasattr(select_next_node,"_st"):from collections import deque;select_next_node._st={"PM":4,"PX":16,"ps":6,"a":0.40,"b":0.50,"g":0.25,"ew":0.35,"gate":0.5,"stag":0,"hist":deque(maxlen=8),"mode":"stratified","last":None,"cool":0,"t":0,"sw":-2}    st=select_next_node._st;st["t"]+=1    if not unvisited_nodes:return int(destination_node) # safety    N=distance_matrix.shape[0];fv=(N-len(unvisited_nodes))/max(1,N);cand=list(unvisited_nodes)    div=estimate_diversity(set(cand),distance_matrix);pool=int(round(st["PM"]+(st["PX"]-st["PM"])*div*(1-fv))) # diversity pool    pool=max(max(2,int(round(st["PM"]*(0.5+0.5*st["gate"])))),min(pool,int(round(st["PX"]*(0.5+0.5*st["gate"]))))) # gate pool    K=max(2,int(round(3-fv)));dens={c:sum(sorted(float(distance_matrix[c,o]) for o in cand if o!=c)[:min(K,len(cand)-1)]) if len(cand)>1 else 0.0 for c in cand} # density    base={c:float(distance_matrix[current_node,c])-st["a"]*(sum(float(distance_matrix[c,o]) for o in (unvisited_nodes-{c}))/max(1,len(unvisited_nodes)-1))-st["b"]*float(distance_matrix[c,destination_node]) for c in cand} # base lookahead    fs={c:base[c]-st["g"]*dens[c]-st["ew"]*candidate_entropy(c,unvisited_nodes,distance_matrix)-0.8*div*((sum(1.0/(float(distance_matrix[c,o])+1e-9) for o in cand if o!=c)/max(1,len(cand)-1))/(1.0+(sum(1.0/(float(distance_matrix[c,o])+1e-9) for o in cand ifo!=c)/max(1,len(cand)-1)))) for c in cand} # entropy+cross    pool_c=sorted(cand,key=lambda c:fs[c])[:max(2,min(pool,len(cand)))]    if not pool_c:return int(min(unvisited_nodes,key=lambda c:distance_matrix[current_node,c])) # fallback    w=0.25+0.50*fv;remavg={c:(sum(float(distance_matrix[c,o]) for o in (unvisited_nodes-{c}))/max(1,len(unvisited_nodes)-1)) for c in pool_c}    s={c:float(distance_matrix[current_node,c])-w*remavg[c]-0.4*float(distance_matrix[c,destination_node])-0.25*min((float(distance_matrix[c,o]) for o in (unvisited_nodes-{c})),default=float(distance_matrix[c,destination_node]))-st["g"]*dens.get(c,0.0) for c inpool_c} # pool rescoring    lo,hi=min(s.values()),max(s.values());ns={c:((s[c]-lo)/(hi-lo) if hi>lo else 0.0) for c in pool_c};best=min(ns.values());best_c=[c for c,v in ns.items() if abs(v-best)<=1e-12] # normalize+tied best    RES=max(2,min(len(best_c),max(2,pool//2)));res=(pareto_reservoir(best_c,RES,scores=ns,dist_current={c:float(distance_matrix[current_node,c]) for c in best_c}) if st["mode"]=="pareto" else stratified_reservoir(best_c,RES)) # reservoir    delta=0.0 if st["last"] is None else (st["last"]-best);st["last"]=best;st["hist"].append(delta);plateau=(len(st["hist"])>=3 and all(abs(x)<1e-6 for x in st["hist"])) # progress    st["stag"]=st["stag"]+1 if plateau else 0;st["gate"]=min(1.0,st["gate"]+0.15) if delta>0 else max(0.0,st["gate"]-(0.05 if st["stag"]>0 else 0.0)) # gate update    st["g"]=max(0.05,min(0.95,st["g"]*(0.5+0.5*st["gate"]))) # gamma update    if st["stag"]>=2 and st["cool"]==0 and (st["t"]-st["sw"]>=2):st["mode"]="pareto" if st["mode"]=="stratified" else "stratified";st["cool"]=2;st["sw"]=st["t"] # switch mode    if st["cool"]>0:st["cool"]-=1 # cooldown    return int((res[0] if res else min(pool_c,key=lambda c:distance_matrix[current_node,c]))) # final pick<br>Entropy-driven diversity integrated into a velocity-damped monotone-gate reservoir framework with progress-gate linking pool size andgamma; uses 2-step reservoir cooldown. velocity-damped reservoir switching, and a 2-step reservoir cooldown,Balance diversity, entropy, and lookahead with a monotone gate,preserving per-candidate entropy/diversity refinement. stagnation-aware reservoir switching, velocity damping, and NN fallbackMonotone-progress pool with entropy and diversity penalties,for robust TSP next-node selection. refinement, cross-diversity penalty, 2-step cooldown, and NN fallback.Monotone gate with velocity-damped reservoir, entropy/diversity<br>Integrate entail_32_0's per-candidate entropy refinement and cross-diversity penaltyinto rollout_31_2's velocity-damped monotone-gate reservoir-switching framework,and tie pool_size and gamma strictly to a single monotone progress_gate with a 2-step reservoir cooldown. velocity-capped monotone gate tying pool_size and gamma; implement a cooldownMerge entail_28_2's cross-diversity penalty and damped gate with entail_29_1'son reservoir switches (e.g., every 2 steps) and a velocity-aware reservoir modetoggle, while preserving per-candidate entropy/diversity refinement. gamma to a single monotone progress gate while preserving NN fallback and usingFuse stagnation-aware reservoir switching from entail_33_1 with velocity-dampedreservoir switching (and a short cooldown) from entail_32_1, tying pool size andan adaptive cross-diversity/entropy penalty that adjusts with stagnation. entail_32_2/rollout_33_2's per-candidate entropy refinement and cross-diversitypenalties, add a 2-step reservoir cooldown with a stagnation-aware toggle, andpreserve velocity-damped reservoir switching plus a nearest-neighbor fallback. Integrate entail_29_1's monotone gate coupling of pool_size and gamma with<br>6.246 6.246 6.254 6.286<br>Prioritize parents that couple monotone<br>progress with entropy/diversity in a unified<br>gate; bind pool_size and gamma to a single<br>progress_gate controlled by velocity; keep a<br>2-step reservoir cooldown with stagnation-<br>triggered toggling; preserve NN fallback; tune<br>cross-diversity penalty to context (avoid over-<br>penalizing early). Small stochastic<br>perturbations can help escape plateaus but<br>must be constrained.<br>Merge monotone progress gate linking pool_size and - Favor parents promoting a cohesive monotone gate linking pool_size<br>gamma with velocity-damped reservoir switching and a and gamma, with velocity-damped reservoir switching and a cooldown;<br>2-step cooldown, incorporating per-candidate entropyrefinement plus cross-diversity penalty from both, and - For directives, keep a monotone gate governing pool_size, gamma,include entropy/diversity refinement, cross-diversity penalties, andavoid merging many similar ideas with the same objective values.<br>retain nearest-neighbor fallback with stagnation-driven and reservoir; add damping with cooldown; retain per-candidate<br>reservoir mode toggling. entropy refinement and add cooldowns/safeguards plus simple<br>reservoir-switch rules to prevent numerical instability.<br>Balance exploration and exploitation with<br>adaptive pool sizing, integrate diversity,<br>density, and lookahead penalties, apply<br>reservoir switching with cooldown, and<br>enforce stagnation-aware monotone<br>progress.<br>def select_next_node_v2(current_node:int,destination_node:int,unvisited_nodes:Set[int],distance_matrix:np.ndarray)->int:    # assumes defined elsewhere: candidate_entropy_v2,estimate_diversity_v2,stratified_reservoir_v2,pareto_reservoir_v2,greedy_completion_cost    sk="_select_next_node_v2_state"    if not hasattr(select_next_node_v2,sk):from collections import deque;setattr(select_next_node_v2,sk,{"PM":4,"PX":16,"g":0.25,"gate":0.5,"stag":0,"hist":deque(maxlen=8),"last":None,"mode":"stratified","cool":0,"vel":0.0})    st=getattr(select_next_node_v2,sk)    if not unvisited_nodes:return int(destination_node)    N=distance_matrix.shape[0];fv=(N-len(unvisited_nodes))/max(1,N);cand=list(unvisited_nodes)    div=estimate_diversity_v2(set(cand),distance_matrix);PM,PX=st["PM"],st["PX"];pool=int(round(PM+(PX-PM)*div*(1-fv)));pool=max(max(2,int(round(PM*(0.5+0.5*st["gate"])))),min(pool,int(round(PX*(0.5+0.5*st["gate"]))))) # pool size    K=max(2,int(round(3-fv)));dens={c:sum(sorted(float(distance_matrix[c,o]) for o in cand if o!=c)[:min(K,len(cand)-1)]) if len(cand)>1 else 0.0 for c in cand} # density    fs={}    for c in cand:        rem=set(unvisited_nodes);rem.remove(c);cost=float(distance_matrix[current_node,c])+greedy_completion_cost(c,rem,distance_matrix,destination_node) # 2-step lookahead        sim=(sum(1.0/(float(distance_matrix[c,o])+1e-9) for o in cand if o!=c)/max(1,len(cand)-1));sim=sim/(1.0+sim) # cross penalty        fs[c]=cost-st["g"]*dens[c]-0.35*candidate_entropy_v2(c,unvisited_nodes,distance_matrix)-0.8*div*sim    pool_c=sorted(cand,key=lambda c:fs[c])[:max(2,min(pool,len(cand)))]    if not pool_c:return int(min(unvisited_nodes,key=lambda c:distance_matrix[current_node,c]))    w=0.25+0.50*fv;s={c:float(distance_matrix[current_node,c])+w*greedy_completion_cost(c,unvisited_nodes-{c},distance_matrix,destination_node)-st["g"]*dens.get(c,0.0) for c in pool_c} # final scoring    lo,hi=min(s.values()),max(s.values());ns={c:((s[c]-lo)/(hi-lo) if hi>lo else 0.0) for c in pool_c};best=min(ns.values());best_c=[c for c,v in ns.items() if abs(v-best)<=1e-12]    RES=max(2,min(len(best_c),max(2,pool//2)));use_pareto=(st["mode"]=="pareto" and st["cool"]<=0)    res=pareto_reservoir_v2(best_c,RES,scores=ns,dist_current={c:float(distance_matrix[current_node,c]) for c in best_c}) if use_pareto else stratified_reservoir_v2(best_c,RES)    delta=0.0 if st["last"] is None else (st["last"]-best);st["last"]=best;st["hist"].append(delta);plateau=(len(st["hist"])>=3 and all(abs(x)<1e-6 for x in st["hist"])) # stagnation    st["stag"]=st["stag"]+1 if plateau else 0;st["vel"]=max(-0.8,min(0.8,(st["vel"]+(0.25 if delta>0 else -0.25))))    st["gate"]=min(1.0,st["gate"]+0.25*max(0.0,st["vel"])) if st["stag"]==0 else max(0.0,st["gate"]-0.05) # gate update    st["g"]=max(0.05,min(0.95,st["g"]*(0.5+0.5*st["gate"]))) # gamma update    if st["stag"]>=2:st["mode"]="pareto" if st["mode"]=="stratified" else "stratified";st["cool"]=2    if st["cool"]>0:st["cool"]-=1    return int(res[0] if res else min(pool_c,key=lambda c:distance_matrix[current_node,c])) use damped velocity and detect stagnation to trigger- Balance exploration/exploitation with adaptive poolincorporate lookahead costs; penalize redundancy;sizing driven by diversity and remaining nodes;diversification; dampen momentum; cachecomputations.<br>pool size tied to a monotone progress gate; velocity-damped reservoirAdaptive reservoir-based TSP with entropy, diversity, and lookahead;switching and a 2-step cooldown<br>Merge monotone progress gate linking pool_size and gamma with velocity-damped<br>reservoir switching and a 2-step cooldown, incorporating per-candidate entropyrefinement plus cross-diversity penalty from both, and retain nearest-neighbor<br>fallback with stagnation-driven reservoir mode toggling.<br>6.172<br><!-- End of picture text -->

_Figure 5._ Example of PathWise at outer iteration _r_ = 34 and entailment step _t_ = 1, showing the entailed node _v⋆_ . The current state _st_ contains nodes _{v_ 1 _, . . . , v_ 4 _}_ . The policy agent _πp_ selects a parent set and generates a derivation rationale, which is executed by the world model _πwm_ to entail a new node. The resulting entailed node is _v⋆_ with _i⋆_ = 1 and _j⋆_ = 1, as shown. The policy and world model critics provide routed reflections at step _t_ , while shaded boxes indicate the updated reflections at step _t_ + 1, conditioning the next step. 

35 

**PathWise: Planning through World Model for Automated Heuristic Design via Self-Evolving LLMs** 

_Table 17._ Training time, token usage, and estimated monetary cost of LLM-based AHD methods across different LLMs. 

|Task|Method|TrainingTime(hrs)|Input Tokens|Output Tokens|Overall Token Cost($)|
|---|---|---|---|---|---|
|||LLM-based AH|D:_GPT-4o-mini_|||
||ReEvo|0.34|814,870|276,557|0.29|
|i|HSEvo|0.56|516,752|153,691|0.17|
|TSP-Constructve|MCTS-AHD|2.10|690,216|228,349|0.24|
||PathWise(Ours)|0.89|2,093,699|281,979|0.48|
||ReEvo|1.12|1,027,245|340,184|0.36|
||HSEvo|1.00|448,491|129,941|0.15|
|MKP-ACO|MCTS-AHD|3.10|845,442|266,019|0.29|
||PathWise(Ours)|1.12|2,000,540|235,161|0.44|
||ReEvo|1.73|849,334|281,124|0.30|
|Offli BPPACO|HSEvo|1.52|441,953|126,667|0.14|
|lne -|MCTS-AHD|3.50|695,488|206,948|0.23|
||PathWise(Ours)|1.72|2,125,645|252,723|0.47|
|||LLM-based AHD:_GPT_|_-5-nano_ (reasoning: low)|||
||ReEvo|0.37|1,199,659|678,508|0.33|
|TSPCi|HSEvo|0.66|1,452,251|755,014|0.37|
|-onstructve|MCTS-AHD|3.00|1,541,230|868,033|0.42|
||PathWise(Ours)|1.19|3,583,414|862,143|0.52|
||ReEvo|0.69|2,087,945|851,566|0.45|
||HSEvo|2.55|1,410,072|737,132|0.37|
|MKP-ACO|MCTS-AHD|2.70|1,526,566|792,639|0.39|
||PathWise(Ours)|1.28|4,841,499|846,706|0.58|
||ReEvo|0.62|1,611,296|637,464|0.34|
|l|HSEvo|1.74|1,064,308|505,791|0.26|
|Offline BPP-ACO|MCTS-AHD|3.30|1,320,616|800,247|0.39|
||PathWise(Ours)|1.34|3,053,028|801,179|0.47|
|||LLM-based AHD:_GPT-5_|_-nano_ (reasoning: medium|)||
||ReEvo|2.05|2,377,468|3,226,613|1.41|
||HSEvo|1.53|1,811,748|2,763,571|1.20|
|TSP-Constructive|MCTS-AHD|5.90|1,232,508|2,887,261|1.22|
||PathWise(Ours)|5.05|6,360,001|2,901,738|1.48|
||ReEvo|1.32|1,888,283|2,269,843|1.00|
||HSEvo|2.99|2,010,936|2,724,171|1.19|
|MKP-ACO|MCTS-AHD|6.40|1,172,054|2,673,922|1.13|
||PathWise(Ours)|5.20|5,328,958|2,814,809|1.39|
||ReEvo|1.49|1,617,676|2,016,702|0.89|
|Offli BPPACO|HSEvo|2.78|1,748,237|2,685,562|1.16|
|lne -|MCTS-AHD|7.32|1,692,991|3,039,435|1.30|
||PathWise (Ours)|5.02|5,959,261|3,051,760|1.52|



# **H. Cost Analysis** 

This section reports the computational and monetary costs associated with LLM-based AHD methods. We decompose cost into two primary components: (i) wall-clock training time, and (ii) LLM token usage (input and output) together with the resulting monetary cost induced by model-specific pricing. These metrics provide a complementary perspective to solution quality by characterizing the practical efficiency and scalability of each method. 

**Runtime Considerations.** Training time in LLM-based AHD is influenced not only by the number of heuristic evaluations but also by the computational complexity of the generated heuristics themselves. Heuristics that contain expensive operations, nested loops, or inefficient data structures can significantly increase per-evaluation runtime, even when the evaluation budget is fixed. As a result, methods that generate structurally complex or poorly optimized heuristics may incur higher wall-clock costs despite using the same number of evaluations. Conversely, generating simpler and more execution-efficient heuristics can substantially reduce overall training time. 

**Token Usage & Model Pricing.** In LLM-based AHD methods, LLM-related cost is driven by both input tokens (prompt context, parent heuristics, metadata, and reflections) and output tokens (generated heuristic code, descriptions, and reasoning traces). In this paper, GPT-4o-mini and GPT-5-nano are used as the underlying LLMs for heuristic generation. Their pricing follows the official OpenAI specifications<sup>2</sup> . For both models, output tokens are substantially more expensive than input tokens. Specifically, for both GPT-4o-mini and GPT-5-nano, output tokens are approximately 8 _×_ more expensive than input tokens. As a consequence, output token generation is the dominant contributor to total monetary cost, making methods that reduce unnecessary generations or verbose outputs significantly more cost-efficient. 

**Analysis.** Table 17 summarizes training time, token usage, and total cost for different AHD methods across tasks. Across tasks and LLM configurations, PathWise achieves training times that are comparable to ReEvo (Ye et al., 2024) and 

> 2https://platform.openai.com/docs/pricing 

36 

**PathWise: Planning through World Model for Automated Heuristic Design via Self-Evolving LLMs** 

HSEvo (Dat et al., 2025), while reducing wall-clock training time by half relative to MCTS-AHD (Zheng et al., 2025). While ReEvo and HSEvo exhibit comparable training times, the heuristics they generate are consistently weaker in solution quality, as reflected in Table 1, Table 2, and Appendix E. Notably, despite having comparable output token usage, MCTS-AHD exhibits substantially longer training time, indicating that for LLM-based AHD the runtime overhead mainly arises from the inefficiency of the generated heuristics and their evaluation cost rather than from LLM API latency or the autoregressive nature of output token generation. 

In terms of token usage, PathWise uses more input tokens than prior methods. This increase is expected, as parent selection and directive generation are explicitly handled by the LLM, requiring richer contextual inputs such as parent metadata and heuristic representations. At the same time, PathWise avoids providing full heuristic code whenever possible and instead relies on compact summaries and structured metadata to reduce unnecessary input length. Importantly, this additional input does not lead to prohibitive cost, since output tokens remain the dominant cost factor, allowing PathWise to maintain competitive monetary cost while achieving stronger performance. 

Across all methods, increasing the reasoning level of GPT-5-nano leads to higher output token generation due to the generation of internal reasoning tokens, as shown in Table 17. Higher levels of explicit reasoning are known to produce longer outputs and higher token consumption in LLMs (Wei et al., 2022; Zhou et al., 2023a; Ma et al., 2025), highlighting the importance of controlling reasoning verbosity when scaling LLM-based AHD methods. 

In many practical applications, training time is often a more critical constraint than monetary cost. As training is extended to NP-hard problems that require learning heuristics on larger instances or involve expensive heuristic evaluations (e.g., large-scale TSP or CVRP instances, high-dimensional packing and scheduling problems), or to combinatorial problems coupled with costly simulation or experimentation, methods with long training cycles become impractical due to the cumulative overhead of repeated heuristic evaluations. Such expensive evaluations commonly arise in scientific and engineering settings, including adaptive experimental design for combinatorial structures (Doppa, 2021), protein and molecular sequence optimization (Yuan et al., 2022; Qiu et al., 2024; Reinhart & Statt, 2024), materials discovery with sequential experimentation (Qian et al., 2023; Chitturi et al., 2024), and high-dimensional black-box optimization over combinatorial or mixed spaces (Papenmeier et al., 2023). 

# **I. Extended Discussions** 

This section discusses limitations of PathWise and LLM-based AHD methods in general, followed by directions for future work. 

## **I.1. Limitations** 

PathWise enhances AHD by combining a hybrid graph-based and population-based formulation with state-aware planning through reasoning over an entailment graph. This structured representation enables memory of derivation history and more informed evolutionary decisions. However, several limitations remain. First, heuristic generation relies on stochastic LLM outputs, and even with structured planning and critic feedback, generated implementations may vary in quality, leading to temporary instability. Such variability can reduce effective diversity in the entailment graph, limiting the contrast available to critic agents and weakening feedback at some steps. More broadly, this behavior is common to LLM-based AHD methods, as they rely on black-box LLMs whose stochastic sampling introduces non-determinism into both heuristic generation and the overall search process, causing runs to diverge even under fixed settings. Second, heuristic performance varies across problem domains when different LLM backbones or reasoning levels are used. This variation likely arises from differences in model training and post-processing (Slocum et al., 2025; Sun et al., 2025; Lanchantin et al., 2025), which can directly impact the diversity of generated heuristics. In addition, different backbones tend to produce heuristics with distinct implementation styles, such as differences in code complexity or abstraction level, and the impact of these differences can vary across problem domains. 

Due to the multi-agent design of PathWise and the inherent stochasticity of LLM-based generation, both intermediate trajectories and final outcomes can vary across backbones and problem settings. In our experiments, this variability was most pronounced in the early stages of the search, where some runs exhibited limited early progress and met the stopping criterion before reaching the more stable improvement patterns observed in other runs. This suggests that PathWise is sensitive to early-step randomness, and improving robustness across runs remains an important direction for future work. 

37 

**PathWise: Planning through World Model for Automated Heuristic Design via Self-Evolving LLMs** 

## **I.2. Future Work** 

Future work includes extending PathWise to settings where heuristic evaluation is significantly more expensive and training time becomes a primary constraint. In many real-world NP-hard optimization problems, learning effective heuristics requires operating on large instances or under costly evaluation pipelines coupled with simulation or experimentation. In such problems, long evolutionary cycles with repeated evaluations are often impractical. PathWise offers a natural direction by allowing policy, world model, and critic agents to be trained to capture problem-domain knowledge and reusable evolutionary strategies in a state-aware manner, rather than relying on fixed search parameters or static operators. Developing training algorithms that balance efficiency with the diversity required for effective heuristic discovery is a promising direction. 

# **J. License** 

The licenses and URLs of baseline methods and software resources are provided in Table 18. 

|||_Table 18._ A summary of licenses.|
|---|---|---|
|Resources|Type License|URL|
|LKH3|Code Available for academic re|search use http://webhotel4.ruc.dk/˜keld/research/LKH-3/|
|OR-Tools|Code MIT License|https://developers.google.com/optimization/pack/knapsack?hl=zh-cn|
|POMO|Code Available online|https://github.com/yd-kwon/POMO/tree/master|
|ACO/DeepACO|Code MIT License|https://github.com/henry-yeh/DeepACO|
|VRP-DACT|Code MIT License|https://github.com/yining043/VRP-DACT|
|NeuOpt|Code MIT License|https://github.com/yining043/NeuOpt|
|Funsearch|Code Apache License|https://github.com/google-deepmind/funsearch|
|EoH|Code MIT License|https://github.com/FeiLiu36/EoH/tree/main|
|ReEvo|Code MIT License|https://github.com/ai4co/reevo|
|HSEvo|Code Available online|https://github.com/datphamvn/HSEvo|
|MCTS-AHD|Code Available online|https://github.com/zz1358m/MCTS-AHD-master|



38 

