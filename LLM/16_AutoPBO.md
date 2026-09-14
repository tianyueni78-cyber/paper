# **AutoPBO: LLM-powered Optimization for Local Search PBO Solvers** 

## **Jinyuan Li**<sup>1, 2</sup> **, Yi Chu**<sup>3</sup> **, Yiwen Sun**<sup>4</sup> **, Mengchuan Zou**<sup>1</sup> **, Shaowei Cai**<sup>1, 2*</sup> 

1Key Laboratory of System Software, Institute of Software, Chinese Academy of Sciences, Beijing, China 2School of Computer Science and Technology, University of Chinese Academy of Sciences, Beijing, China 

3Institute of Software, Chinese Academy of Sciences, Beijing, China 

4School of Data Science, Fudan University, Shanghai, China lijy@ios.ac.cn, chuyi2020@iscas.ac.cn, ywsun22@m.fudan.edu.cn, zoumc@ios.ac.cn, caisw@ios.ac.cn 

#### **Abstract** 

Pseudo-Boolean Optimization (PBO) provides a powerful framework for modeling combinatorial problems through pseudo-Boolean (PB) constraints. Local search solvers have shown excellent performance in PBO solving, and their efficiency is highly dependent on their internal heuristics to guide the search. Still, their design often requires significant expert effort and manual tuning in practice. While Large Language Models (LLMs) have demonstrated potential in automating algorithm design, their application to optimizing PBO solvers remains unexplored. In this work, we introduce _AutoPBO_ , a novel LLM-powered framework to automatically enhance PBO local search solvers. We conduct experiments on a broad range of four public benchmarks, including one real-world benchmark, a benchmark from PB competition, an integer linear programming optimization benchmark, and a crafted combinatorial benchmark, to evaluate the performance improvement achieved by _AutoPBO_ and compare it with six state-of-the-art competitors, including two local search PBO solvers _NuPBO_ and _OraSLS_ , two complete PB solvers _PBO-IHS_ and _RoundingSat_ , and two mixed integer programming (MIP) solvers _Gurobi_ and _SCIP_ . _AutoPBO_ demonstrates significant improvements over previous local search approaches, while maintaining competitive performance compared to state-of-the-art competitors. The results suggest that _AutoPBO_ offers a promising approach to automating local search solver design. 

## **1 Introduction** 

Pseudo-Boolean Optimization (PBO) plays an important role in solving a wide range of combinatorial problems (Boros and Hammer 2002), which seeks an assignment of values to a set of Boolean variables that optimizes a linear objective function under Pseudo-Boolean (PB) constraints. Due to its powerful expressiveness and the convenience to make use of properties of boolean variables, PBO has demonstrated broad applicability across various domains, including VLSI design, economic modeling, computer vision, and manufacturing optimization (Wille, Zhang, and Drechsler 2011; Zhang et al. 2011; Roussel and Manquinho 2021). 

Along with the wide usages of the PBO problem in industrial and application domains, solving the PBO is then 

*Corresponding author 

a non-negligible topic. However, the solving of PBO is a challenging task as the problem is NP-hard (Buss and Nordstr¨om 2021). In previous studies, the solving methods can be divided into two classes: complete methods and incomplete methods. The complete methods solves the problem to optimal and proves the optimality, while incomplete methods do not guarantee to compute the optimal assignment but try to compute good solutions in a short time. 

Research on complete methods for solving PBO has developed multiple approaches. First, since PB constraints can be naturally treated as 0-1 linear constraints, mixed-integer programming (MIP) solvers such as _SCIP_ (Bestuzheva et al. 2021) and _Gurobi_ (Gurobi Optimization, LLC 2021) can be directly applied to solve PBO problems. Second, by translating PB constraints into conjunctive normal form (CNF), the problem can be solved using SAT solvers based on ConflictDriven Clause Learning (CDCL), including _MINISAT+_ (E´en and S¨orensson 2006), _Open-WBO_ (Martins, Manquinho, and Lynce 2014), and _NaPS_ (Sakai and Nabeshima 2015). Beyond these, advanced methods have been developed for more efficient PBO solving. The cutting planes technique, which goes beyond the resolution power of CDCL, is implemented in solvers like _sat4j_ (Le Berre and Parrain 2010) and _RoundingSat_ (Elffers and Nordstr¨om 2018, 2020; Devriendt et al. 2021). Additionally, the implicit hitting set (IHS) method has been successfully adapted to PBO in solvers such as _PBO-IHS_ (Smirnov, Berg, and J¨arvisalo 2021; Smirnov, Berg, and J¨arvisalo 2022). 

Complete algorithms often struggle with large-scale instances, leading to the development of incomplete approaches, among which local search stands out as a representative strategy (Lei et al. 2021; Chu et al. 2023; Zhou et al. 2023). The first notable solver _LS-PBO_ (Lei et al. 2021) introduced a weighting scheme and a scoring function that jointly handle hard and soft constraints. Several key extensions followed: _DeciLS-PBO_ (Jiang et al. 2023) enhanced the framework by incorporating unit propagation; _NuPBO_ (Chu et al. 2023) proposed enhanced scoring functions and weighting schemes; and _DLS-PBO_ (Chen et al. 2024) implemented dynamic scoring functions. Additionally, _OraSLS_ (Iser, Berg, and J¨arvisalo 2023) utilizes a oracle mechanism to guide the local search approach in PBO. 

The efficiency of local search solvers heavily relies on internal heuristics to guide the search process. In the past, 

many works on designing different algorithmic components such as weighting scheme and score functions have been proposed, as in (Thornton 2005; Cai and Su 2013; Cai et al. 2014; Cai and Lei 2020; Lei et al. 2021; Chu, Cai, and Luo 2023; Chu et al. 2024). However, those works are based on human-designed techniques and designing these heuristics often demands substantial expert effort and manual tuning in practice. On the other hand, recent developments on the LLM-based algorithm design start a new paradigm of algorithm design and show the capability of large language models (LLMs) in automating algorithm design. However, the application of LLMs to building PBO solvers remains unexplored, presenting a promising direction for future research. 

Current works on automated algorithm design for combinatorial optimization problems are mainly on designing evolutionary algorithms for specific problems or optimizing heuristics in simple solvers. FunSearch (RomeraParedes et al. 2024) pioneered the integration of pretrained LLMs with evolutionary search, initiating heuristic discovery through iterative code generation. Then, EoH (Liu et al. 2024) extends this paradigm through dual-representation evolution, and ReEvo (Ye et al. 2024) introduces a structured reflection mechanism to guide evolutionary search. What is more, AutoSAT (Sun et al. 2024, 2025) focus on optimizing heuristics in SAT solvers, AlphaEvolve (Novikov et al. 2025) pushes the paradigm further by ensembling LLMs with automated evaluators in an evolutionary loop, enabling the discovery of entire algorithmic codebases. 

The works on automated heuristic design for the general form problem (i.e. problems with general constraints types, such as Integer Programming, Pseudo Boolean Optimization, etc) is rare, and current approaches of designing heuristics for specific types of problems face critical limitations in this scenario: 1) the general-problem solver usually have complex structure with various algorithm components, and thus results in long-context of source codes, being much more sophisticated than evolutionary algorithms for specific types of problems; 2) A general form problem usually allows a wide range of types of constraints rather than specific types of problems normally has quite limited and known types of constraints, making the heuristics design for these two scenarios quite different. Thus, the algorithm design for the general form optimization problem is still challenging, and to our knowledge, there is no prior work on the LLM-driven automated design for PBO solver. 

We consider the automated optimization for local search solvers of the PBO problem. Specifically, we consider to enhance the existing state-of-the-art local search solver for PBO by leveraging the power of LLM. We try to address the above challenges by designing methods from three considerations:1) Enhancing LLMs’ comprehension of solver codes with complex structures; 2) Reducing errors or invalid modifications during code generation; 3) Improving the solver’s efficiency by optimizing its algorithm as a composition that involves multiple functions. 

In this work, we design a novel LLM-powered framework to automatically enhance PBO local search solvers. We propose a multi-agent system integrated with a greedy search strategy, enabling closed-loop, feedback-driven op- 

timization. Furthermore, we introduce a structuralized local search PBO solver _StructPBO_ , with a clearer structure of codes, that could be used as an input for automatic optimization frameworks. This design helps LLMs to effectively comprehend and optimize PBO-specific search algorithms and was adopted in our system. 

Bring the above ideas together, we design our _AutoPBO_ framework to automatically enhancing local search solvers of PBO. Experimental results demonstrate that _AutoPBO_ significantly improves the performance of local search PBO solvers, offering a promising approach to automating local search solver design. 

## **2 Preliminaries** 

### **2.1 Pseudo-Boolean Optimization** 

A linear pseudo-Boolean (PB) constraint is expressed as: � _nj_ =1<sup>_ajlj_▷</sup><sup>_b_, where</sup><sup>_aj, b ∈_Z are integer coefficients,</sup><sup>_b_is</sup> the threshold, ▷ _∈{_ = _, >, ≥, <, ≤}_ is a relational operator, and each _lj_ is a literal (either a Boolean variable _xi_ or its negation _¬xi_ ). 

In this work, we assume all PB constraints are in the normalized form<sup>�</sup><sup>_n_</sup> _j_ =1<sup>_ajlj≥b_with</sup><sup>_aj, b ∈_N</sup> 0<sup>+(non-negative</sup> integers). This assumption is without loss of generality since all PB constraints can be converted to this form by expressing equalities as inequality pairs and applying the identity _xi_ = 1 _−¬xi_ to ensure non-negative coefficients (Roussel and Manquinho 2021). 

An assignment _α_ is a mapping from variables to _{_ 0 _,_ 1 _}_ . A PB constraint _c_ is _satisfied_ under _α_ if the inequality � _nj_ =1<sup>_ajlj≥b_holds; otherwise,</sup><sup>_c_is</sup><sup>_violated_. The</sup><sup>_violation_</sup> _degree_ of _c_ under _α_ , denoted viol( _c_ ), quantifies how far _c_ is from being satisfied: viol( _c_ ) = max �0 _, b −_<sup>�</sup><sup>_n_</sup> _j_ =1<sup>_ajlj_</sup> �, which is zero if _c_ is satisfied, and otherwise measures the shortfall. A _PB formula F_ is a conjunction of PB constraints, and an assignment that satisfies all constraints in _F_ is called a _feasible solution_ . 

A pseudo-Boolean optimization (PBO) instance consists of a PB formula _F_ together with a linear Boolean objective function<sup>�</sup><sup>_n_</sup> _j_ =1<sup>_ejlj_+</sup><sup>_d_, where</sup><sup>_ej∈_N+and</sup><sup>_d∈_Z. Since</sup> all PB constraints must hold, they are treated as _hard constraints_ . For any assignment _α_ , its objective value is denoted as _obj_ ( _α_ ). A feasible solution _α_ 1 is considered superior to another solution _α_ 2 if _obj_ ( _α_ 1) _< obj_ ( _α_ 2). The objective of PBO is to identify a feasible assignment _α_ that minimizes _obj_ ( _α_ ). 

### **2.2 Local Search for PBO** 

The local search is a general algorithmic paradigm fo solving combinatorial optimization problems. It typically begins with an initial solution and iteratively explores the neighborhood of the current solution, seeking an improved candidate solution. If such a solution is found, it replaces the current one; otherwise, the search either terminates or employs strategies to escape local optima. The process continues until a stopping criterion is met, such as reaching a maximum number of iterations, a time limit, or a satisfactory solution quality threshold. 

In a typical local search process of PBO, given an instance _F_ , the local search algorithm starts from an initial solution _α_ , then iteratively modifies _α_ by selecting variables heuristically and applying corresponding **operators** (e.g., the _flip_ operator in pseudo-Boolean optimization) until a feasible solution is found. An operation is obtained when an operator is specified with a variable, and it is easy to see there could be multiple operations for generating a new solution. During this process, **scoring functions** evaluate candidate operations, prioritizing operations that are likely to improve solution quality. An important factor normally included in scoring functions is the weights of constraints. A **weighting scheme** is adopted to compute the weights of constraints in the scoring function, representing the importance of the constraints. 

In general, for greedy variable flipping, PBO local search (LS) algorithms employ a scoring function integrated with the weights of constraints. Let _w_ ( _c_ ) denote the weight of a hard constraint _c_ , and _w_ ( _o_ ) denote the weight of the objective function _o_ . For instance, in _LS-PBO_ , the penalty for a constraint _c_ is defined as _penalty_ ( _c_ ) = _w_ ( _c_ ) _× viol_ ( _c_ ), and the penalty for the objective function under the current assignment _α_ is _penalty_ ( _o_ ) = _w_ ( _o_ ) _× obj_ ( _α_ ). In _NuPBO_ , a smoothed penalty method is proposed to balance the _viol_ values across constraints. Specifically, for a hard constraint _c_ , the penalty function is redefined as: _penalty_ ( _c_ ) = _wsmooth_ <u>(</u> _c_ <u>)</u> _×viol_ ( _c_ <u>()</u> _c_ <u>)</u> where _smooth_ ( _c_ ) represents a smoothing coefficient derived from constraint properties. Similarly, for the objective function _o_ , the penalty is adjusted to: _penalty_ ( _o_ ) =<sup>_w_</sup> _smooth_<sup><u>(</u></sup><sup>_o_</sup><sup><u>)</u></sup><sup>_×obj_</sup> (<sup><u>(</u></sup> _o_<sup>_α_</sup> )<sup><u>)</u>; with</sup><sup>_smooth_(</sup><sup>_o_) often</sup> calculated as the average of the objective function’s coefficients. Across these algorithms, the hard score _hscore_ ( _x_ ) of a variable _x_ quantifies the reduction in the total penalty of all hard constraints when _x_ is flipped. The soft score _oscore_ ( _x_ ) measures the reduction in the objective function’s penalty after flipping _x_ . The scoring function of _x_ is defined as _score_ ( _x_ ) = _hscore_ ( _x_ )+ _oscore_ ( _x_ ), a linear combination of the hard and soft scores. 

## **3 A New Structuralized Local Search PBO Solver:** **_StructPBO_** 

As we mentioned in Section 1, previous studies on automated algorithm design usually focus on combinatorial optimization problems with known types and usually result in simple-architecture algorithms, which are quite different from general form problem solvers that have complex structures. Notably, the Local Search PBO solvers typically employ advanced programming techniques and multiple algorithmic components in the code to achieve high efficiency in finding high-quality solutions within a short time period. Thus, it is still challenging for LLMs to process the codes of general problem solvers. 

In our preliminary experiments, using LLMs to generate a PBO solver from scratch under the EoH mechanism resulted in local search algorithms that were limited to basic scoring functions and random perturbation stages (see Appendix A). Furthermore, when attempting to optimize existing Lo- 

- **Algorithm 1:** the structPBO solver **Input:** PBO instance _F_ , cutoff time _cutoff_ . **Output:** The best solution _α_<sup>_∗_</sup> found and its objective function value _obj_<sup>_∗_</sup> , or “No solution found”. 

- **1** _α_<sup>_∗_</sup> := ∅, _obj_<sup>_∗_</sup> := + _∞_ ; **2** _α_ := InitializeAssignment(); **3 while** _elapsed time < cutoff_ **do 4 if** _α is feasible_ **_and_** _obj_ ( _α_ ) _< obj_<sup>_∗_</sup> **then** // Update best solution and its objective function value 

- **5** _α_<sup>_∗_</sup> := _α_ , _obj_<sup>_∗_</sup> := _obj_ ( _α_ ); **6 for** _each variable x_ **do 7** hscore( _x_ ) := ∆Penaltyhard( _x_ ); **8** oscore( _x_ ) := ∆Penaltyobj( _x_ ); **9** score( _x_ ) := CalculateScore(hscore( _x_ ) _,_ oscore( _x_ )); 

- **10 if** _D_ := _{x|Score_ ( _x_ ) _>_ 0 _}̸_ = ∅ **then** // A variable is picked accordingly 

- **11** _x_ := PickBestVariable( _D_ ); **12 else** // Stuck in a local optimum 

- **13** UpdateWeights(F); // A variable is picked according to local-optima-escaping heuristics 

- **14** _x_ := PickEscapeVariable( _F_ ); **15** _α_ := _α_ with _x_ flipped; **16 if** _α_<sup>_∗̸_</sup> = ∅ **then return** _α_<sup>_∗_</sup> and _obj_<sup>_∗_</sup> ; **17 else return** No solution found; 

cal Search PBO solvers using established solver optimization frameworks (see Appendix A), the high complexity and tight coupling of the codebase led to a significant increase in syntactic errors and logical inconsistencies in the LLMgenerated code. 

To address these problems, we propose a predefined, structured Local Search PBO Solver framework named _StructPBO_ . Aligning the basic components of local search routine, we defines the functionalities of different parts of a local search solver and build a structuralized solver _StructPBO_ , following the SOTA PBO local search solver _NuPBO_ (Chu et al. 2023). 

As presented in Algorithm 1, a local search solver maintains a complete assignment (line 2). During the search, it keeps track of the best solution found (lines 4-5) and returns it when the termination condition is reached (lines 1617). The effectiveness of the proposed local search PBO solver lies in its heuristic-driven variable selection mechanism, which hinges on the interplay between dynamic constraint weighting and penalty-based scoring functions, designed to systematically navigate the search space while balancing constraint satisfaction and objective optimization (lines 6-15). Specifically, for each variable _x_ , the algorithm 

evaluates flip candidates through a composite score (line 9) that combines _hscore_ ( _x_ ) and _oscore_ ( _x_ ) – the respective penalty reductions for hard constraints and objective optimization (lines 7-8), where penalties are weighted according to constraint criticality. This weighting adapts dynamically: during feasibility-seeking phases, hard constraints dominate through exponentially higher weights, while objective constraints gain influence when approaching optimality. When trapped in local optima (line 13), the solver strategically updates these weights to escape stagnation. The resulting score-driven variable selection (lines 10-15) thus automatically shifts focus between constraint repair and objective improvement based on real-time search progress. 

In this paper, we work on a structuralized local search framework that defines seven functions which are independently implemented: 

- **InitializeAssignment** : Heuristically generates an initial complete assignment 

- **Penalty hard** : Heuristically computes the hard constraint penalty reduction 

- **Penalty obj** : Heuristically computes the objective penalty reduction 

- **CalculateScore** : Heuristically combines hard and soft penalties into a dynamic composite score 

- **PickBestVariable** : Heuristically selects the most promising variable 

- **UpdateWeights** : Heuristically selects the most promising variable 

- **PickEscapeVariable** : Heuristically identifies variables for diversification when stagnation is detected 

This modular architecture enables isolated function optimization while maintaining global coherence through our convergence mechanism described in Section 4.3. 

## **4 The Automated Optimization Framework** 

For automating the optimization of codes for local search solver of PBO, we propose a LLM-based multi-agent framework, named _AutoPBO_ . Our framework is based on three types of agents and a greedy-based iterative method to achieve a better performance solver. 

As illustrated in Figure 1, our framework begins by loading a local search PBO solver, then a number of iterative code optimizing rounds are launched. In each round, we perform several distinct and independent code modifications work, each modification work is realized by the three LLM agents collaboratively. After an optimization round, several versions of code are generated and then a greedy-based selection strategy is applied to select the most effective version for the next iteration. By repeating, the framework ultimately generates the resulting solver. 

### **4.1 Optimization by Multiple Agents** 

There are three specialized LLM agents in our framework, each of which has its own functionality and distinct roles, i.e., the Code Optimization Planner, Code Editor, and Modification Evaluator. Each of them serves different functionalities in our framework as follows: 

- Code Optimization Planner: Analyze key code segments to recognize the function targeted for modification and generate modification plans. 

- Code Editor: Realize the code modification to improve the code, following the advice generated by the Code Optimization Planner. 

- Modification Evaluator: Evaluate the modified code and generate advice for future improvement. 

Those three agents operate through an automated cycle of modification plan generation, code edit iteration, and dynamic evaluation. 

A code optimization round is consist of two phases: the planning phase and the editing phase. In the planning phase, the Code Optimization Planner Agent identifies possible optimization ways and generates preliminary improvement plans, such as ”Dynamic Score Ratios: Adjust h ~~s~~ core ~~r~~ atio and s ~~s~~ core ~~r~~ atio dynamically based on the current state of the search (e.g., increase the weight of hard constraints when the solution is infeasible”, ”Include a term that considers the age of the variable (time since last flip) to encourage diversification and escape local optima”, etc. The details of the implementations of the Code Optimization Planner is presented in Section 4.2. 

The editing phase is built by interactions of the Code Editor and the Modification Evaluator, for multiple times. The Code Editor Agent performs the actual work of code modifications and runs for multiple times in the editing phase. Initially, it modifies the code modifications with the optimization plans provided by the Code Optimization Planner as input, and generates the first version of the code. It identifies if the modification has actual significant meanings, by excluding trivial modifications such as variable re-naming, parameter changing, etc. An actual compilation and running of the code is also performed at this time, to collect information such as the existence of compilation errors or running information. 

The running information and the evaluation results from the Modification Evaluator will then be sent to the code Editor as feedback for the next modification. This interaction will be performed by the Code Editor, Modification Evaluator several times, resulting in a final version of code for the current code optimization round. 

In the following, we will first present the implementation of different agents, then introduce the greedy-based iterative methods on top of code optimization rounds, which jointly form our whole optimization framework for PBO local search solver. 

### **4.2 Implementation of Agents** 

The three agents are implemented by different prompt, which are designed following the principles proposed by OpenAI’s foundational guidelines(OpenAI 2023), we have developed a structured prompt to implement different functionalities for them. 

Our prompt includes A _Role_ set to the agent, the _Tasks_ definitions, the _Tips_ to provide suggestions and the complete PBO solver code appended at the end to ensure all agents share the same context. All three agents share a common 



<!-- Start of picture text -->
LLM-based Multi-agent<br>Local Search PBO Solver Convergence to Optimal Solution<br>Framework<br>Local Search Multi-agent Framework<br>Search Better Functions<br>void Solver::LocalSearch{…)<br>{<br>  while(!SatisfyEndCondition(…))<br>  {    InitializeLocalSearch(…); ModificationEvaluator 3<br>if(FindBetterSolution(…))UpdateBestResult{…); Give FeedbackEvaluate Code Functions 1<br>    CalculateScore(…);<br>    if(!NoBetterFlip(…)}PickBetterFlip(…);<br>    else<br>    {      UpdateWeights(…); Code Planner  1 Functions 2<br>      PickEscapeFlip(…};    }    Flipvar(…); + Generate RecoAnalyze Codemmendations Running Code<br>  } Functions 3<br>}<br>void Solver::SatisfyEndCondition{…){…}<br>void Solver::InitializeLocalSearch(…){…}<br>void Solver::FindBetterSolution(…){…}<br>void Solver::UpdateBestResult(…}{…} Code Editor 2 Functions 4<br>void Solver::CalculateScore(…}{…}<br>void Solver::NoBetterFlip(…){…} Write Code<br>void Solver::PickBetterFlip(…){…} Run Code<br>void Solver::UpdateWeights(…){…} Refine Code<br>void Solver::PickEscapeFlip(…){…}<br>void Solver::Flipvar(…){…}<br>Greedy<br>Output: Better Solver<br>Input: structialized Solver<br>Multi-agent Framework<br><!-- End of picture text -->

Figure 1: Architecture of AutoPBO. With a structuralized local search PBO solver as input, AutoPBO implements greedy strategy to optimize heuristic functions iteratively. For each iteration, AutoPBO employs the original solver code to instantaneously create an understanding and recommendations for heuristic functions, subsequently engages in code generation and performance assessment by three agents. Upon completion, AutoPBO returns the optimal solver code. 

_Role_ configuration as a solver researcher attempting to improve the heuristics in a PBO solver. This foundational _Role_ description establishes the professional identity and overarching objective for each agent in the optimization process. _Tasks_ and _Tips_ of every agent are shown in Table 1. 

### **4.3 Convergence to Optimal Solution** 

As illustrated in Figure 1, we implement an iterative greedy algorithm that progressively constructs the improved solver through three steps: 

- **Code Optimization Round** : Agents optimize one function at a time, while keeping others functions fixed. For example, we first generate multiple optimized versions of the UpdateWeights function through LLM agents, then select the best-performing version before proceeding to optimize CalculateScore. Implementation Process is that the LLM agents first generate multiple optimized versions of the function as illustrated in 4.1. Then our framework automates the following workflow: it constructs solver instances for each function version, runs these solvers in parallel on certain dataset, and automatically collects their outputs—including feasibility status (Feasible or Infeasible) and objective values( _obj_ ) across all test instances. Finally, the framework determines the best-performing version through automatic comparison by tallying the total feasible solutions (Feasible count) and the number of instances where a solver’s _obj_ outperforms _StructPBO_ (Win count), selecting the version that achieves the highest count on both metrics. 

- **Modification Propagating** : The selected optimal function (e.g., improved UpdateWeights) is immediately integrated into _StructPBO_ . Subsequent optimizations (e.g., CalculateScore refinement) are then performed on this updated _StructPBO_ . 

- **Iterative Improvement** : This process repeats until all target functions are optimized. 

This approach addresses the inherent dependency between functions. Consider the interaction between UpdateWeights and CalculateScore: The scoring function in CalculateScore must reflect the latest clause weights from UpdateWeights to properly prioritize constraint satisfaction. If we independently optimize both functions and combine their best versions, the scoring mechanism might ignore updated weight distributions, leading to inconsistent optimization behavior. Our greedy strategy prevents such conflicts by enforcing sequential adaptation - the improved CalculateScore automatically adapts to the newly integrated UpdateWeights through Modification Propagating. 

Together with these three steps and the three agents involved, we iteratively improve our code, trying to get a better performance solver. 

## **5 Experiments** 

In this section, we introduce the experimental settings and present extensive experiments on 4 PBO benchmarks. First, we evaluate the effectiveness of _AutoPBO_ as a framework for enhancing baseline solvers, demonstrating that it consistently improves performance across multiple benchmarks. 

|**Agent**|**Tasks**|**Tips **|
|---|---|---|
|Code|1. Comprehensively analyzing all key code|1. Complete review of all relevant code sections|
|Optimization<br>Planner|segments<br>2. Proposing possible modification manners|2. Generation of both practical and theoretically promising proposals<br>3. Strict JSON format adherence|
||Phase 1:<br>1. Precise interpretation of Planner's<br>description|Phase 1:<br>1. Preserve original function signatures<br>2. Prevent undefined variable introduction|
|Code Editor|2. Directional suggestions for code changes<br>Phase 2:<br>1. Analyze experimental outcomes<br>2. Produce superior code versions|3. Guarantee differentiation from previous codes<br>Phase 2:<br>1. Maintain code formatting<br>2. Avoid redundant modifications|
|Code||1. Thorough syntax verification|
|Modification<br>Evaluator|1. Evaluation and classification of outputs|2. Comparative analysis for meaningful improvements<br>3. Categorical classification|



Table 1: Agent Tasks and Tips Overview 

Second, we compare _AutoPBO_ with state-of-the-art PBO solvers to highlight its strong competitiveness. Finally, in Appendix A we provide variance analysis through repeated experiments to demonstrate the statistical stability of _AutoPBO_ ’s performance. 

### **5.1 Settings** 

**Environment** Our PBO solver is implemented in C++, while the interface for interacting with LLMs is developed in Python. The solver is compiled using g++ 9.4.0. All experiments are performed on an Ubuntu 20.04.4 LTS server, which is equipped with two AMD EPYC 7763 processors. Each processor operates at a base frequency of 2.45 GHz. The server is configured with 1TB of RAM. For all experiments, the DeepSeek<sup>1</sup> LLM is employed. 

**Benchmarks and Datasets** We evaluate _AutoPBO_ on four widely-used PBO benchmarks, comprising 47 datasets in total. For each dataset, we randomly split the instances into training and test sets with a 1:1 ratio. The training set is used to generate the enhanced solver via _AutoPBO_ , while the test set is reserved for final evaluation. Detailed instance information is provided in Code & Data Appendix. A summary is provided below: 

- PB16: The OPT-SMALLINT-LIN benchmark from the 2016 pseudo-Boolean competition, comprising 1600 diverse instances from multiple categories.<sup>2</sup> Following the categorization in (Smirnov, Berg, and J¨arvisalo 2021), we divide PB16 into 42 datasets based on their applications. 

- MIPLIB: A benchmark of 0-1 integer linear programming problems, containing 267 instances of various types, as introduced in (Devriendt et al. 2021).<sup>3</sup> 

- CRAFT: A collection of 1025 crafted combinatorial problems with small integer coefficients, also from (Devriendt 

1We utilize the DeepSeek-R1 as default in this paper. 

- 2http://www.cril.univ-artois.fr/PB16/bench/PB16-used.tar 

3https://zenodo.org/record/3870965 

et al. 2021).<sup>4</sup> 

- Real-world: A benchmark set containing three application-driven problems: the Minimum-Width Confidence Band Problem (MWCB, 24 instances), the Seating Arrangements Problem (SAP, 21 instances), and the Wireless Sensor Network Optimization Problem (WSNO, 18 instances). All problem descriptions, encodings, and instances are from (Lei et al. 2021).<sup>5</sup> 

**State-of-the-art Competitors.** We compare _AutoPBO_ with 6 state-of-the-art solvers, including 2 incomplete solver ( _i.e., NuPBO_ and _OraSLS_ ) and 4 complete solvers. The 4 complete solvers include 2 PB solvers ( _i.e., PBO-IHS_ and _RoundingSat_ ) and 2 MIP solvers ( _i.e., Gurobi_ and _SCIP_ ): 

- _NuPBO_ (Chu et al. 2023): The state-of-the-art local search solver for solving PBO. 

- _OraSLS_ (Iser, Berg, and J¨arvisalo 2023): a recent oraclebased SLS algorithm for PBO, which improves upon previous pure SLS approaches. 

- _PBO-IHS_ (Smirnov, Berg, and J¨arvisalo 2022): A PBO solver that utilizes the implicit hitting set approach and building upon _RoundingSat_ (Elffers and Nordstr¨om 2018). 

- _RoundingSat_ (Devriendt et al. 2021): A PBO solver combining core-guided search with cutting planes reasoning. 

- _Gurobi_ (Gurobi Optimization, LLC 2021): One of the most powerful commercial MIP solvers (Version 12.0.2). The default configuration is used, along with a single thread. 

- _SCIP_ (Gamrath et al. 2020): One of the fastest noncommercial solvers for MIP (Version 8.0.4). 

**Performance Metrics** In our experiments, _AutoPBO_ first generates optimization strategies on the training set with a 60-second cutoff time. Then, each solver performs one run 

- 4https://zenodo.org/record/4036016 

- 5https://lcs.ios.ac.cn/ _\_ %7ecaisw/Resource/LS-PBO/ 

|Benchmark|_Str_|_uctPBO_|_Au_|_toPBO_|
|---|---|---|---|---|
||#_win_|_avg_<br>_~~s~~core_|#_win_|_avg_<br>_~~s~~core_|
|Real-world|17|0.9962|**29**|**0.9998**|
|CRAFT|488|0.9472|**513**|**0.9474**|
|MIPLIB|101|0.8450|**112**|**0.8598**|
|PB16|697|0.8272|**775**|**0.8447**|
|Total|1303|0.8738|**1429**|**0.8849**|



Table 2: _AutoPBO_ vs _StructPBO_ Performance Comparison (By Benchmark) 



Figure 2: # _win_ differences between _AutoPBO_ and _StructPBO_ . Each bar represents _AutoPBO_ ’s # _win_ minus _StructPBO_ ’s # _win_ . Positive values (orange bars) indicate _AutoPBO_ ’s advantage. 

within a given cutoff time (300 seconds) on every instance in the testing set for evaluation. We record the cost of the best solution found by solver _Sj_ on instance _Ik_ , denoted as _solSj Ik_ . The cost of the best solution found among all solvers in the same table on instance _Ik_ is denoted as _bestIk_ . Following previous research on PBO, we measure the performance of each solver using two metrics: 

- # _win_ : the number of instances where the corresponding _bestIk_ can be obtained by solver _S_ on _Bi_ ( _i.e.,_ the number of winning instances). 

- _avg_ _~~s~~ core_ : in our experiments, the competition score of solver _Sj_ on instance _Ik_ is represented by _scoreSj Ik_ = _bestIk_ +1 

- _solSj Ik_ +1<sup>, which measures the gap between</sup><sup>_solSjIk_and</sup> _bestIk_ . If solver _Sj_ could not report a solution on instance _Ik_ , then _scoreSj Ik_ = 0. We use _avg_ _~~s~~ core_ to denote the average competition score of a solver on a dataset. 

For each of the above two metrics, if a solver obtains a larger metric value on a dataset, then the solver exhibits better performance on the dataset. The results highlighted in **bold** indicate the best performance for the corresponding metric. 

### **5.2 Results** 

**Improvements of Local Search PBO solver** We first evaluate _AutoPBO_ on top of _StructPBO_ across 47 datasets from 4 benchmarks. Figures 2 and 3 present the datasets with changes in # _win_ and _avg_ _~~s~~ core_ respectively along with the 



Figure 3: _avg_ _~~s~~ core_ differences between _AutoPBO_ and _StructPBO_ . Each bar represents _AutoPBO_ ’s _avg_ _~~s~~ core_ minus _StructPBO_ ’s _avg_ _~~s~~ core_ ( _AutoPBO − StructPBO_ ). Positive values (orange bars) indicate _AutoPBO_ ’s higher _avg_ _~~s~~ core_ , while negative values (dark-blue bars) indicate _StructPBO_ ’s higher _avg_ _~~s~~ core_ (after non-linear scaling for better visibility). 

magnitude of these changes. _AutoPBO_ demonstrates consistent performance gains: improving # _win_ on 24 datasets and _avg_ _~~s~~ core_ on 23 datasets, with only a single case of marginal degradation in _avg_ _~~s~~ core_ . This consistent nonnegative trend confirms that _AutoPBO_ not only avoids harming performance but also delivers significant gains on nearly half of the datasets across all benchmarks. 

Table 2 provides a benchmark-level comparison between _AutoPBO_ and _StructPBO_ in terms of both # _win_ and _score_ . Across all 4 benchmarks, _AutoPBO_ demonstrates consistent improvements, raising the total number of # _win_ and increasing the overall _avg_ _~~s~~ core_ . 

These benchmark-level results highlight the generality and robustness of _AutoPBO_ . 

**Competitive Results of** **_AutoPBO_** We conduct a comprehensive comparison between _AutoPBO_ and state-of-the-art solvers, as shown in Table 3. To ensure fair comparison, we performed parameter tuning for _PBO-IHS_ , _RoundingSat_ , _OraSLS_ , and _NuPBO_ on each dataset. The tuning scripts and final parameter configurations are documented in Code & Data Appendix. The experimental results demonstrate that _AutoPBO_ outperforms all open-source solvers in both # _win_ and _avg_ _~~s~~ core_ . Notably, _AutoPBO_ shows competitive performance compared to the commercial solver _Gurobi_ . 

At the dataset level (see Appendix A), _AutoPBO_ achieves the highest # _win_ on 31 out of 47 datasets and obtains the best _avg_ _~~s~~ core_ on 32 datasets. The complete per-dataset comparison reveals that _AutoPBO_ consistently delivers robust performance across diverse problem types. 

## **6 Conclusions and Future Work** 

This paper is devoted to develop a novel LLM-powered framework to automatically enhance PBO local search solvers. First, we introduced our structuralized local search PBO solver framework. Furthermore, we configured multiple LLM agents and employed a greedy strategy to generate an optimized and efficient solver. Experimental results 

||_G_|_urobi_|_S_|_CIP_|_PBO-I_|_HS_-Tuned|_Roundi_|_ngSat_-Tuned|_OraS_|_LS_-Tuned|_NuPB_|_O_-Tuned|_Au_|_toPBO_|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Benchmark|#_win _|_avg_<br>_~~s~~core_|#_win _|_avg_<br>_~~s~~core_|#_win _|_avg_<br>_~~s~~core_|#_win _|_avg_<br>_~~s~~core_|#_win _|_avg_<br>_~~s~~core_|#_win _|_avg_<br>_~~s~~core_|#_win _|_avg_<br>_~~s~~core_|
|Real-world|3|0.5319|0|0.1417|0|0.3503|0|0.0000|2|0.3322|19|0.9956|**26**|**0.9977**|
|CRAFT|**479**|**0.9783**|289|0.8337|277|0.7959|302|0.8341|406|0.9620|454|0.9447|460|0.9449|
|MIPLIB|**101**|0.8313|33|0.5625|55|0.7051|47|0.7619|53|0.7236|74|0.8259|73|**0.8367**|
|PB16|**680**|**0.8461**|353|0.5974|513|0.7542|397|0.5297|529|0.8026|600|0.8190|624|0.8204|
|Total|**1263**|**0.8836**|675|0.6660|845|0.7555|746|0.6442|990|0.8404|1147|0.8668|1183|0.8687|



Table 3: Multi-Solver Performance Comparison (By Benchmark) 

demonstrate that AutoPBO can improve the efficiency of local search PBO solver to a very high level. 

In the future, we will integrate advanced LLM technologies into more general solvers to enhance their flexibility and performance. For instance, techniques like retrievalaugmented generation (RAG) could help LLM generating correct modifications. We will also enhance other solvers such as MIP solvers using LLM-based framework. This approach would enable faster modifications and more efficient solver customization. 

## **References** 

Bestuzheva, K.; Besanc¸on, M.; Chen, W.-K.; Chmiela, A.; Donkiewicz, T.; Van Doornmalen, J.; Eifler, L.; Gaul, O.; Gamrath, G.; Gleixner, A.; et al. 2021. The SCIP optimization suite 8.0. _arXiv preprint arXiv:2112.08872_ . 

Boros, E.; and Hammer, P. L. 2002. Pseudo-boolean optimization. _Discrete applied mathematics_ , 123(1-3): 155–225. Buss, S.; and Nordstr¨om, J. 2021. Proof complexity and SAT solving. In _Handbook of Satisfiability_ , 233–350. IOS Press. Cai, S.; and Lei, Z. 2020. Old techniques in new ways: Clause weighting, unit propagation and hybridization for maximum satisfiability. _Artificial Intelligence_ , 287: 103354. Cai, S.; Luo, C.; Thornton, J.; and Su, K. 2014. Tailoring local search for partial MaxSAT. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 28. 

Cai, S.; and Su, K. 2013. Local search for boolean satisfiability with configuration checking and subscore. _Artificial Intelligence_ , 204: 75–98. 

Chen, Z.; Lin, P.; Hu, H.; and Cai, S. 2024. ParLS-PBO: A Parallel Local Search Solver for Pseudo Boolean Optimization. _arXiv preprint arXiv:2407.21729_ . 

Chu, Y.; Cai, S.; and Luo, C. 2023. NuWLS: Improving local search for (weighted) partial MaxSAT by new weighting techniques. In _Proceedings of AAAI 2023_ , volume 37, 3915–3923. 

Chu, Y.; Cai, S.; Luo, C.; Lei, Z.; and Peng, C. 2023. Towards more efficient local search for pseudo-boolean optimization. In _29th International Conference on Principles and Practice of Constraint Programming (CP 2023)_ , 12–1. 

Chu, Y.; Li, C.; Ye, F.; and Cai, S. 2024. Enhancing MaxSAT Local Search via a Unified Soft Clause Weighting Scheme. In _In Proceedings of SAT 2024_ , volume 305, 8:1–8:18. 

Devriendt, J.; Gocht, S.; Demirovic, E.; Nordstr¨om, J.; and Stuckey, P. J. 2021. Cutting to the Core of Pseudo-Boolean 

Optimization: Combining Core-Guided Search with Cutting Planes Reasoning. In _Proceedings of AAAI 2021_ , 3750– 3758. 

E´en, N.; and S¨orensson, N. 2006. Translating pseudoboolean constraints into SAT. _Journal on Satisfiability, Boolean Modeling and Computation_ , 2(1-4): 1–26. 

Elffers, J.; and Nordstr¨om, J. 2018. Divide and Conquer: Towards Faster Pseudo-Boolean Solving. In Lang, J., ed., _Proceedings of IJCAI 2018_ , 1291–1299. 

Elffers, J.; and Nordstr¨om, J. 2020. A Cardinal Improvement to Pseudo-Boolean Solving. In _Proceedings of AAAI 2020_ , 1495–1503. 

Gamrath, G.; Anderson, D.; Bestuzheva, K.; Chen, W.-K.; Eifler, L.; Gasse, M.; Gemander, P.; Gleixner, A.; Gottwald, L.; Halbig, K.; Hendel, G.; Hojny, C.; Koch, T.; Le Bodic, P.; Maher, S. J.; Matter, F.; Miltenberger, M.; M¨uhmer, E.; M¨uller, B.; Pfetsch, M. E.; Schl¨osser, F.; Serrano, F.; Shinano, Y.; Tawfik, C.; Vigerske, S.; Wegscheider, F.; Weninger, D.; and Witzig, J. 2020. The SCIP Optimization Suite 7.0. Technical report, Optimization Online. Gurobi Optimization, LLC. 2021. Gurobi Optimizer Reference Manual. 

Iser, M.; Berg, J.; and J¨arvisalo, M. 2023. Oracle-based local search for pseudo-boolean optimization. In _ECAI 2023_ , 1124–1131. IOS Press. 

Jiang, L.; Ouyang, D.; Zhang, Q.; and Zhang, L. 2023. DeciLS-PBO: an Effective Local Search Method for Pseudo-Boolean Optimization. _arXiv preprint arXiv:2301.12251_ . 

Le Berre, D.; and Parrain, A. 2010. The Sat4j library, release 2.2. _Journal on Satisfiability, Boolean Modeling and Computation_ , 7(2-3): 59–64. 

Lei, Z.; Cai, S.; Luo, C.; and Hoos, H. 2021. Efficient local search for pseudo boolean optimization. In _Theory and Applications of Satisfiability Testing–SAT 2021: 24th International Conference, Barcelona, Spain, July 5-9, 2021, Proceedings 24_ , 332–348. Springer. 

Liu, F.; Xialiang, T.; Yuan, M.; Lin, X.; Luo, F.; Wang, Z.; Lu, Z.; and Zhang, Q. 2024. Evolution of Heuristics: Towards Efficient Automatic Algorithm Design Using Large Language Model. In _the 41st International Conference on Machine Learning_ . 

Martins, R.; Manquinho, V.; and Lynce, I. 2014. OpenWBO: A modular MaxSAT solver. In _International Conference on Theory and Applications of Satisfiability Testing_ , 438–445. Springer. 

Novikov, A.; V˜u, N.; Eisenberger, M.; Dupont, E.; Huang, P.-S.; Wagner, A. Z.; Shirobokov, S.; Kozlovskii, B.; Ruiz, F. J.; Mehrabian, A.; et al. 2025. AlphaEvolve: A coding agent for scientific and algorithmic discovery. _arXiv preprint arXiv:2506.13131_ . 

OpenAI. 2023. OpenAI API Documentation. 

Romera-Paredes, B.; Barekatain, M.; Novikov, A.; Balog, M.; Kumar, M. P.; Dupont, E.; Ruiz, F. J.; Ellenberg, J. S.; Wang, P.; Fawzi, O.; et al. 2024. Mathematical discoveries from program search with large language models. _Nature_ , 625(7995): 468–475. 

Roussel, O.; and Manquinho, V. 2021. Pseudo-Boolean and cardinality constraints. In _Handbook of satisfiability_ , 1087– 1129. IOS Press. 

Sakai, M.; and Nabeshima, H. 2015. Construction of an ROBDD for a PB-Constraint in Band Form and Related Techniques for PB-Solvers. _IEICE Transactions on Information & Systems_ , 98-D(6): 1121–1127. 

Smirnov, P.; Berg, J.; and J¨arvisalo, M. 2021. Pseudoboolean optimization by implicit hitting sets. In _27th International Conference on Principles and Practice of Constraint Programming (CP 2021)_ , 51–1. Schloss DagstuhlLeibniz-Zentrum f¨ur Informatik. Smirnov, P.; Berg, J.; and J¨arvisalo, M. 2022. Improvements to the Implicit Hitting Set Approach to Pseudo-Boolean Optimization. In _Proceedings of SAT 2022_ , 13:1–13:18. Sun, Y.; Ye, F.; Chen, Z.; Wei, K.; and Cai, S. 2025. Automatically discovering heuristics in a complex SAT solver with large language models. _arXiv preprint arXiv:2507.22876_ . 

Sun, Y.; Ye, F.; Zhang, X.; Huang, S.; Zhang, B.; Wei, K.; and Cai, S. 2024. Autosat: Automatically optimize sat solvers via large language models. _arXiv preprint_ . Thornton, J. 2005. Clause weighting local search for SAT. _Journal of Automated Reasoning_ , 35: 97–142. 

Wille, R.; Zhang, H.; and Drechsler, R. 2011. ATPG for Reversible Circuits Using Simulation, Boolean Satisfiability, and Pseudo Boolean Optimization. In _2011 IEEE Computer Society Annual Symposium on VLSI_ , 120–125. 

Ye, H.; Wang, J.; Cao, Z.; Berto, F.; Hua, C.; Kim, H.; Park, J.; and Song, G. 2024. Reevo: Large language models as hyper-heuristics with reflective evolution. _Advances in neural information processing systems_ , 37: 43571–43608. 

Zhang, Y.; Hartley, R.; Mashford, J.; and Burn, S. 2011. Superpixels via pseudo-Boolean optimization. _International Conference on Computer Vision,International Conference on Computer Vision_ . 

Zhou, W.; Zhao, Y.; Wang, Y.; Cai, S.; Wang, S.; Wang, X.; and Yin, M. 2023. Improving local search for pseudo boolean optimization by fragile scoring function and deep optimization. In _29th International Conference on Principles and Practice of Constraint Programming (CP 2023)_ , 41–1. 

||Real|-world|CR|AFT|MI|PLIB|PB16|
|---|---|---|---|---|---|---|---|
|Solver|Win(_µ ± σ_)|Score(_µ ± σ_)|Win(_µ ± σ_)|Score(_µ ± σ_)|Win(_µ ± σ_)|Score(_µ ± σ_)|Win(_µ ± σ_)<br>Score(_µ ± σ_)|
|_Gurobi_|3.3_±_0.6|0.523_±_0.013|**479.0**_±_**0.0 **|**0.978**_±_**0.000**|**102.0**_±_**1.0 **|**0.839**_±_**0.008**|**680.7**_±_**0.6 0.846**_±_**0.001**|
|_SCIP_|0.0_±_0.0|0.145_±_0.005|288.7_±_0.6|0.834_±_0.000|41.3_±_16.2|0.561_±_0.010|358.0_±_7.0 0.601_±_0.007|
|_PBO-IHS_-Tuned|0.0_±_0.0|0.351_±_0.001|276.7_±_0.6|0.793_±_0.005|55.0_±_0.0|0.710_±_0.004|514.7_±_1.5 0.753_±_0.002|
|_RoundingSat_-Tuned|0.0_±_0.0|0.000_±_0.000|301.7_±_1.5|0.834_±_0.000|46.7_±_0.6|0.762_±_0.000|397.3_±_0.6 0.529_±_0.001|
|_OraSLS_-Tuned|2.0_±_0.0|0.340_±_0.013|406.0_±_0.0|0.962_±_0.000|51.3_±_1.5|0.723_±_0.001|529.3_±_0.6 0.801_±_0.001|
|_NuPBO_-Tuned|19.0_±_1.0|0.996_±_0.001|454.0_±_0.0|0.945_±_0.000|71.7_±_2.1|0.823_±_0.003|601.7_±_1.5 0.818_±_0.001|
|_AutoPBO_|**25.3**_±_**1.2**|**0.997**_±_**0.000**|460.0_±_0.0|0.944_±_0.001|70.7_±_2.1|0.836_±_0.001|624.7_±_1.2 0.819_±_0.001|



Table 4: Solver Stability Analysis Across Experiments 

## **A Extended Experimental Results** 

### **A.1 Statistical Analysis of Repeated Experiments** 

To ensure the reliability and reproducibility of our experimental results, we conducted multiple independent runs of our experiments to evaluate the stability of solver performance across different conditions. 

For each benchmark category (Real-world, CRAFT, MIPLIB, and PB16), we calculated the mean ( _µ_ ) and standard deviation ( _σ_ ) of both win counts and average scores across the experimental runs. The coefficient of variation (CV = _σ_ /( _µ_ ) × 100%) was used as a measure of relative variability to assess the consistency of each solver’s performance. 

Our statistical analysis reveals that most solvers demonstrate excellent stability across repeated experiments. AutoPBO shows particularly consistent performance with CV values mostly below 5% for both win counts and scores across all benchmark categories. For instance, in the Real-world benchmark, AutoPBO achieves a win count of 25.3 ± 1.2 (CV = 4.6%) and a score of 0.997 ± 0.000 (CV = 0.0%), indicating highly stable performance. Similarly, other solvers like Gurobi, PBO-IHS-Tuned, and RoundingSat-Tuned also exhibit low variability, with most CV values remaining under 3%. 

The low variance observed across multiple experimental runs confirms that our results are not artifacts of specific random initializations or environmental conditions, but rather reflect the genuine algorithmic performance of each solver. This statistical validation strengthens the reliability of our comparative analysis and supports the robustness of our experimental conclusions. 

### **A.2 Detailed Experimental Results** 

Tables 5 and 6 present the detailed per-dataset evaluation results of _AutoPBO_ across all 47 datasets, extending the benchmarklevel analysis in Section 5.2. These comprehensive results demonstrate that _AutoPBO_ consistently outperforms _StructPBO_ while maintaining competitive performance against state-of-the-art solvers. Specifically, _AutoPBO_ achieves superior performance in both # _win_ and _avg score_ metrics across diverse problem types, further validating its robust performance. 

|Dataset|_StructPBO_ #_wi_|_n_<br>_AutoPBO_ #_win_|_StructPBO avg_<br>_~~s~~cor_|_e_<br>_AutoPBO avg_<br>_~~s~~core_|
|---|---|---|---|---|
|BA|5|**11 (+6)**|0.9820|**1.0000 (+0.0180)**|
|EmployeeSche|8|<br>**9 (+1)**|0.8789|<br>**0.8889 (+0.0100)**|
|MIPLIB01<br>~~2~~67|101|**112 (+11)**|0.8450|**0.8598 (+0.0148)**|
|NG|14|**15 (+1)**|0.9977|**1.0000 (+0.0023)**|
|PBOins<br>~~l~~wsa|1|**10 (+9)**|0.9949|**0.9999 (+0.0050)**|
|PBOins<br>~~m~~wcb|7|**10 (+3)**|0.9945|**0.9997 (+0.0052)**|
|PBOins<br>~~w~~sno|**9**|**9**|**1.0000**|**1.0000**|
|area|13|**15 (+2)**|0.9810|**1.0000 (+0.0190)**|
|areaDelay|**15**|**15**|**1.0000**|**1.0000**|
|bounded<br>~~g~~olo|**9**|**9**|**0.4444**|**0.4444**|
|course-ass|2|**3 (+1)**|0.9998|**1.0000 (+0.0002)**|
|crafted<br>~~o~~pb|488|**513 (+25)**|0.9472|**0.9474 (+0.0002)**|
|cudf|**11**|**11**|**0.5455**|**0.5455**|
|data|30|**39 (+9)**|0.4452|**0.5223 (+0.0771)**|
|decomp|2|**5 (+3)**|0.9333|**1.0000 (+0.0667)**|
|domset|**8**|**8**|**1.0000**|**1.0000**|
|dt-problems|**30**|**30**|**1.0000**|**1.0000**|
|factor|86|**88 (+2)**|0.8756|**0.9066 (+0.0310)**|
|fctp|**16**|**16**|**0.1250**|**0.1250**|
|featureSubsc|**10**|**10**|**1.0000**|**1.0000**|
|flexray|**5**|**5**|**0.4000**|**0.4000**|
|frb|**20**|**20**|**1.0000**|**1.0000**|
|garden|**4**|**4**|**1.0000**|**1.0000**|
|golomb-ruler|6|**8 (+2)**|0.6433|**0.6589 (+0.0156)**|
|graca|**10**|**10**|**1.0000**|**1.0000**|
|haplotype|**4**|**4**|**1.0000**|**1.0000**|
|heinz|20|**23 (+3)**|0.6494|**0.6522 (+0.0028)**|
|kullmann|3|**4 (+1)**|0.9826|**1.0000 (+0.0174)**|
|logic-synthe|36|**37 (+1)**|0.9989|**1.0000 (+0.0011)**|
|market-split|11|**20 (+9)**|0.3244|**0.5500 (+0.2256)**|
|milp|**17**|**17**|**0.7059**|**0.7059**|
|minlplib|**49**|**49**|**1.0000**|**1.0000**|
|miplib|36|**51 (+15)**|**0.7706**|0.7665 (-0.0041)|
|mps|**2**|**2**|**1.0000**|**1.0000**|
|oliveras|57|**63 (+6)**|0.9975|**0.9992 (+0.0017)**|
|pbfvmc-formu|**11**|**11**|**1.0000**|**1.0000**|
|poldner|**3**|**3**|**1.0000**|**1.0000**|
|primes-dimac|75|**77 (+2)**|0.8077|**0.8332 (+0.0255)**|
|radar|**6**|**6**|**1.0000**|**1.0000**|
|random|13|**22 (+9)**|0.7725|**0.7727 (+0.0002)**|
|routing|**8**|**8**|**1.0000**|**1.0000**|
|synthesis-pt|**5**|**5**|**1.0000**|**1.0000**|
|trarea<br>~~a~~c|**5**|**5**|**1.0000**|**1.0000**|
|ttp|3|**4 (+1)**|0.9965|**1.0000 (+0.0035)**|
|unibo|17|**18 (+1)**|0.3886|**0.3889 (+0.0003)**|
|vtxcov|**8**|**8**|**1.0000**|**1.0000**|
|wnq|4|**7 (+3)**|0.9895|**0.9971 (+0.0076)**|
|Total|1303|**1429 (+126)**|0.8738|**0.8849 (+0.0110)**|



Table 5: _AutoPBO_ vs _StructPBO_ Performance Comparison (By Dataset) 

|Dataset|_G_<br>#_win_|_urobi_<br>_avg_<br>_~~s~~core_|#_win_|_SCIP_<br>_avg_<br>_~~s~~core_|_PBO-I_<br>#_win_|_HS_-Tuned<br>_avg_<br>_~~s~~core_|_Roundi_<br>#_win_|_ngSat_-Tuned<br>_avg_<br>_~~s~~core_|_OraS_<br>#_win_|_LS_-Tuned<br>_avg_<br>_~~s~~core_|_NuPB_<br>#_win_|_O_-Tuned<br>_avg_<br>_~~s~~core_|_A_<br><br>#_win_|_utoPBO_<br>_avg_<br>_~~s~~core_|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|BA|<br>**13**|<br><br>**0.9995**|<br>0|<br><br>0.2554|<br>0|<br><br>0.8295|<br>0|<br><br>0.0000|<br>1|<br><br>0.8780|<br>0|<br><br>0.9676|3|<br><br>0.9830|
|EmployeeSc|7|0.7579|1|0.0000|2|0.5786|1|0.0000|6|0.8195|8|0.8789|**9**|**0.8889**|
|MIPLIB01<br>~~2~~|**101**|0.8313|33|0.5625|55|0.7051|47|0.7619|53|0.7236|74|0.8259|73|**0.8367**|
|NG|**11**|0.9466|0|0.0000|0|0.8847|0|0.0000|0|0.9176|7|**0.9847**|7|**0.9847**|
|PBOins<br>~~l~~ws|0|0.0811|0|0.0000|0|0.0000|0|0.0000|0|0.0000|3|0.9957|**9**|**0.9997**|
|PBOins<br>~~m~~wc|2|0.8082|0|0.1080|0|0.6113|0|0.0000|0|0.2956|9|0.9950|**10**|**0.9970**|
|PBOins<br>~~w~~sn|1|0.7144|0|0.3599|0|0.4305|0|0.0000|2|0.7871|**7**|**0.9962**|**7**|**0.9962**|
|area|**15**|**1.0000**|8|0.8974|10|0.9265|14|0.9892|10|0.9430|13|0.9769|14|0.9949|
|areaDelay|**15**|**1.0000**|0|0.8691|8|0.9690|14|0.9957|6|0.9683|**15**|**1.0000**|**15**|**1.0000**|
|bounded<br>~~g~~o|5|0.5215|3|0.2753|4|0.6140|2|0.0000|**7**|**0.6610**|3|0.2561|3|0.3172|
|course-ass|**3**|**1.0000**|1|0.7863|1|0.9871|2|0.9998|2|0.9976|2|0.9998|**3**|**1.0000**|
|crafted<br>~~o~~p|**479**|**0.9783**|289|0.8337|277|0.7959|302|0.8341|406|0.9620|454|0.9447|460|0.9449|
|cudf|6|0.5455|6|0.5455|**10**|**0.9987**|6|0.5455|4|0.3636|6|0.5455|6|0.5455|
|data|**42**|**0.6591**|13|0.1445|13|0.3422|18|0.3950|19|0.5079|16|0.4398|17|0.4517|
|decomp|1|0.7381|0|0.7788|0|0.3150|0|0.0000|0|0.9355|1|0.9206|**5**|**1.0000**|
|domset|1|0.9872|0|0.9035|0|0.9774|0|0.0000|0|0.9269|7|0.9993|**8**|**1.0000**|
|dt-problem|**30**|**1.0000**|**30**|**1.0000**|**30**|**1.0000**|16|0.5333|24|0.8000|**30**|**1.0000**|**30**|**1.0000**|
|factor|**96**|**0.9583**|**96**|**0.9583**|**96**|**0.9583**|**96**|**0.9583**|**96**|**0.9583**|**96**|**0.9583**|87|0.9006|
|fctp|**16**|**01250**|15|01211|14|00000|14|00000|**16**|**01250**|**16**|**01250**|**16**|**01250**|
|featureSub|3|**.**<br>0.9869|0|.<br>0.7037|**10**|.<br>**1.0000**|**10**|.<br>**1.0000**|**10**|**.**<br>**1.0000**|**10**|**.**<br>**1.0000**|**10**|**.**<br>**1.0000**|
|flexray|**5**|**0.4000**|**5**|**0.4000**|**5**|**0.4000**|**5**|**0.4000**|3|0.0000|**5**|**0.4000**|**5**|**0.4000**|
|frb|2|0.9966|0|0.9880|0|0.9942|0|0.9808|0|0.9922|**20**|**1.0000**|**20**|**1.0000**|
|garden|3|0.9057|1|0.8628|3|0.7500|2|0.9256|2|0.9050|**4**|**1.0000**|**4**|**1.0000**|
|golomb-rul|6|0.6599|5|0.5486|**8**|**0.8485**|1|0.0000|7|0.6667|4|0.5707|3|0.5740|
|graca|**10**|**1.0000**|0|0.0098|9|0.9997|**10**|**1.0000**|**10**|**1.0000**|**10**|**1.0000**|**10**|**1.0000**|
|haplotype|**4**|**1.0000**|0|0.3886|3|0.9931|**4**|**1.0000**|**4**|**1.0000**|**4**|**1.0000**|**4**|**1.0000**|
|heinz|18|**0.6515**|8|0.3848|15|0.6131|14|0.5739|14|0.5598|18|0.6487|**19**|0.6487|
|kullmann|2|0.8196|0|0.3577|2|0.8122|0|0.0000|1|0.6816|3|0.9817|**4**|**1.0000**|
|logic-synt|36|0.9986|12|0.8932|35|0.9459|23|0.9250|25|0.9781|36|0.9989|**37**|**1.0000**|
|market-spl|**20**|**0.5500**|11|0.1146|9|0.0130|9|0.1705|12|0.3659|11|0.2544|11|0.3186|
|milp|**17**|**0.8235**|5|0.2727|9|0.5556|10|0.4745|13|0.6964|7|0.5197|7|0.5389|
|minlplib|**38**|0.9972|9|0.9321|14|0.7229|12|0.9620|10|0.9612|36|**0.9996**|36|0.9994|
|miplib|**52**|**0.8946**|16|0.3904|25|0.6048|5|0.0000|27|0.7191|25|0.7028|28|0.7099|
|mps|1|**1.0000**|**2**|**1.0000**|0|0.8824|**2**|**1.0000**|**2**|**1.0000**|**2**|**1.0000**|**2**|**1.0000**|
|oliveras|47|0.7930|21|0.4640|47|0.8322|47|0.8998|**70**|**1.0000**|42|0.9790|41|0.9800|
|pbfvmc-for|10|0.9992|1|0.5562|0|0.5031|2|0.4258|3|0.5180|**11**|**1.0000**|**11**|**1.0000**|
|poldner|**3**|**1.0000**|2|0.9841|**3**|**1.0000**|**3**|**1.0000**|**3**|**1.0000**|**3**|**1.0000**|**3**|**1.0000**|
|primes-dim|**73**|0.8205|57|0.6871|68|0.7436|10|0.0000|72|0.8290|70|0.8073|**73**|**0.8329**|
|radar|**6**|**1.0000**|0|0.9743|**6**|**1.0000**|2|0.9770|3|0.9714|**6**|**1.0000**|**6**|**1.0000**|
|random|**22**|**0.7727**|6|0.5740|**22**|**0.7727**|**22**|**0.7727**|**22**|**0.7727**|13|0.7725|**22**|**0.7727**|
|routing|**8**|**1.0000**|5|0.6250|**8**|**1.0000**|**8**|**1.0000**|**8**|**1.0000**|**8**|**1.0000**|**8**|**1.0000**|
|synthesis-|**5**|**1.0000**|3|0.9745|**5**|**1.0000**|**5**|**1.0000**|3|0.9869|**5**|**1.0000**|**5**|**1.0000**|
|trarea<br>~~a~~c|**5**|**1.0000**|2|0.9822|3|0.9704|0|0.0000|3|0.9636|**5**|**1.0000**|**5**|**1.0000**|
|ttp|1|0.7154|1|0.7040|0|0.9296|0|0.0000|1|0.9594|2|0.9894|**4**|**1.0000**|
|unibo|**16**|0.4853|8|0.1142|13|**0.4908**|8|0.0000|10|0.3881|8|0.2980|8|0.3161|
|vtxcov|5|0.9995|0|0.9736|3|0.9986|0|0.0000|0|0.9711|**8**|**1.0000**|**8**|**1.0000**|
|wnq|1|0.9719|0|0.0000|0|0.9572|0|0.0000|0|0.3860|4|0.9895|**7**|**0.9995**|
|Total|**1263**|**0.8836**|675|0.6660|845|0.7555|746|0.6442|990|0.8404|1147|0.8668|1183|0.8687|



Table 6: Multi-Solver Performance Comparison (By Dataset) 

