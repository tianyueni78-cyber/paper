# **Evolving Interdependent Operators with Large Language Models for Multi-Objective Combinatorial Optimization** 

## **Junhao Qiu**<sup>1</sup> **, Xin Chen**<sup>1</sup> **, Liang Ge**<sup>2</sup> **, Liyong Lin**<sup>*2</sup> **, Zhichao Lu**<sup>1</sup> **, Qingfu Zhang**<sup>†1</sup> 

1 Department of Computer Science, City University of Hong Kong 

> 2 Contemporary Amperex Technology Limited 

junhaoqiu2-c@my.cityu.edu.hk, llin5@e.ntu.edu.sg, qingfu.zhang@cityu.edu.hk 

#### **Abstract** 

Neighborhood search operators are critical to the performance of Multi-Objective Evolutionary Algorithms (MOEAs) and rely heavily on expert design. Although recent LLM-based Automated Heuristic Design (AHD) methods have made notable progress, they primarily optimize individual heuristics or components independently, lacking explicit exploration and exploitation of dynamic coupling relationships between operators. In this paper, multi-operator optimization in MOEAs is formulated as a Markov decision process, enabling the improvement of interdependent operators through sequential decision-making. To address this, we propose the **<u>E</u>** <u>volution</u> **<u>o</u>** <u>f</u> **<u>O</u>** <u>perator</u> **<u>C</u>** <u>ombination</u> ( **E2OC** ) framework for MOEAs, which achieves the co-evolution of _design strategies_ and executable _codes_ . E2OC employs Monte Carlo Tree Search to progressively search combinations of operator design strategies and adopts an operator rotation mechanism to identify effective operator configurations while supporting the integration of mainstream AHD methods as the underlying designer. Experimental results across AHD tasks with varying objectives and problem scales show that E2OC consistently outperforms state-of-the-art AHD and other multi-heuristic co-design frameworks, demonstrating strong generalization and sustained optimization capability. 

## **1 Introduction** 

Multiobjective Combinatorial Optimization Problems (MCOPs) are widely encountered in fields such as production scheduling (Neufeld, Schulz, and Buscher 2023; Li et al. 2024a), engineering design (Peng et al. 2023), and hyperparameter tuning in machine learning (Morales-Hernandez,´ Van Nieuwenhuyse, and Rojas Gonzalez 2023). For these NP-hard problems, obtaining the entire Pareto set/frontier using exact algorithms (e.g., dynamic programming) is challenging (Wang et al. 2023). Meta heuristic-based approximation approaches include Multi-Objective Evolutionary Algorithms Multi-Objective Evolutionary Algorithms (MOEAs) (e.g., NSGA-II (Deb et al. 2002), NSGA-III (Deb and Jain 2014), MOEA/D (Qingfu Zhang and Hui Li 2007)), Pareto local search methods (e.g., PLS (Paquete, Chiarandini, and Stutzle¨ 2004a), 2PPLS (Lust and Teghem 2010a), PPLS/D-C (Shi et al. 2022)), and methods combining evolutionary algorithms and local search (Paquete, Chiarandini, 

*Corresponding author. 

> †Corresponding author. 



<!-- Start of picture text -->
obj2 obj2<br>Designer obj1 LLM obj1<br>Ideas/ Ideas/<br>Thoughts ... Thoughts<br>...<br>Code Solver Codes Solver<br>(a) Manual Design (b) LLM-based Design<br>obj2<br>LLM<br>Operators Co-design<br>design strategy obj1<br>coupling Integrate<br>Ideas/Thoughts Codes Solver<br>(c) LLM-based Multi-Operator Co-design<br><!-- End of picture text -->

Figure 1: The single operator design in MOEAs has advanced from (a) expert-dependent methods to (b) LLM-guided iterative improvements of code implementations (e.g., EoH, MCTS-AHD). In comparison, (c) E2OC explicitly accounts for interdependencies among mult-operators and facilitates the coordinated co-evolution of _design strategies_ and executable _codes_ . 

and Stutzle 2004b¨ ; Kumar and Singh 2007; Jaszkiewicz and Zielniewicz 2009). However, the effectiveness of MOEAs depends on the selection and interaction of domain-specific search operators. Different application domains typically require different algorithms and/or configurations. Manually designing and tuning these operators is costly and heavily reliant on expert knowledge. 

Automated Heuristic Design (AHD) is a promising research direction for addressing this problem (Burke et al. 2013; Stutzle and L¨ opez-Ib´ a´nez 2019˜ ). Genetic Programming (GP), one of the earliest techniques for automatic heuristic discovery (Langdon and Poli 2013; Zhang et al. 2023), evolves algorithms via simulated natural selection. However, GP relies on a set of permissible primitives or mutation opera- 

tions; constructing a domain-agnostic set remains fundamentally difficult across diverse multiobjective metaheuristics and problem settings (Pillay and Qu 2018; O’Neill et al. 2010). 

The AHD powered by the code generation and language comprehension capability of the Large Language Models (LLMs) has introduced a new search paradigm in recent years (Liu et al. 2026; Wu et al. 2024). LLMs are employed as a heuristic designer in certain iterative frameworks (Zhang et al. 2024a), such as evolutionary search (Liu et al. 2024a; Ye et al. 2024; van Stein and Back 2024¨ ; Yao et al. 2025), neighborhood search (Xie et al. 2025), and Monte Carlo Tree Search (MCTS) (Zheng et al. 2025a; Kiet et al. 2025). These methods represent a shift from traditional approaches, leveraging LLMs’ reasoning abilities to synthesize algorithmic ideas and adapt them to problem-specific tasks. While these methods have achieved significant progress in evolving single operator, they focus primarily on evolving isolated components rather than multi-operator systems. 

Effective optimization requires combining operators with complementary search biases in complex MCOPs. The overall performance of MOEAs therefore depends on how well these operators complement and interact with one another to balance exploration and exploitation throughout the optimization process. However, both expert-designed and LLM-driven approaches, particularly traditional single-operator evolution methods, remain limited in systematically reasoning about operator interactions and sequencing effects. Consequently, establishing a co-evolutionary mechanism for operators is essential to enhancing the performance and adaptability of MOEAs in multi-objective optimization. 

To bridge this gap, we propose a new algorithm design paradigm, dubbed the **<u>E</u>** <u>volution</u> **<u>o</u>** <u>f</u> **<u>O</u>** <u>perator</u> **<u>C</u>** ombination ( **E2OC** ). This approach searches for _design strategy_ formed by multiple design thoughts of different operators, modeling their interdependencies and synergies to guide the evolution of operator combinations. The design thoughts are textual descriptions of specific improvement suggestions intended to enhance the existing operators, rather than merely expressing the semantic idea of an operator (Liu et al. 2024a). By systematically exploring combinations of these thoughts, the search for effective operator combinations is guided in promising directions. We demonstrate that LLM-assisted co-evolution of design thoughts and executable codes, guided by carefully crafted prompts, achieves state-of-the-art multi-operator design results. We expect E2OC to provide a significant advancement in the automated design of complex algorithms. In summary, our contributions are as follows: 

- We propose E2OC, a new algorithm design paradigm that supports the LLM-based co-evolution of _design strategies_ and _codes_ , achieving automated design of multi-operators in MOEAs with minimum hand-craft. 

- We develop a progressive design strategy search mechanism that explores the coupling between operators by combining the design thoughts of different operators to guide the direction of evolution. 

- We implement operator rotation evolution to systematically explore design strategies and identify optimal operator combinations, while supporting the integration of 

advanced AHD methods as algorithm designer. 

- We comprehensively evaluate E2OC on benchmarks of two widely studied MCOPs. The results demonstrate that E2OC outperforms many existing AHD methods, such as EoH and MCTS-AHD. In two- or three-objective problems, E2OC brings significant enhancements in manually designed MOEAs. In particular, E2OC is able to leverage the evolution of design strategies to achieve sustained enhancements under continued resource investment. 

## **2 Multi-Operator Optimization in MOEAs** 

Based on previous designs of single heuristics (Liu et al. 2024a; Romera-Paredes et al. 2024), recent work has been extended to more complex algorithmic systems, such as heuristic set design (Liu et al. 2025) and multi-strategy optimization (Kiet et al. 2025). In contrast, we focus on the co-design of interdependent operators in MOEAs that involve evaluation uncertainty. 

**Multi-Objective Optimization.** The task of multiobjective optimization is to identify a set of solutions that balance multiple, often conflicting, objectives. A general formulation is given by: 



where _X_ denotes the feasible solution space, **_x_** is a decision vector, and **_f_** : _X →_ R<sup>_M_</sup> represents an objective function vector with _M_ objectives. 

**Pareto Dominance.** Given two solutions **_x_** _a,_ **_x_** _b ∈X_ , **_x_** _a_ is said to dominate **_x_** _b_ (denoted **_x_** _a ≺_ **_x_** _b_ ) if and only if _fi_ ( **_x_** _a_ ) _≤ fi_ ( **_x_** _b_ ) _, ∀i ∈{_ 1 _,_ 2 _, . . . , M }_ , and _fj_ ( **_x_** _a_ ) _< fj_ ( **_x_** _b_ ) for at least one _j_ . 

**Pareto Optimality:** A solution **_x_**<sup>_∗_</sup> _∈X_ is Pareto-optimal if there is no **_x_**<sup>_′_</sup> _∈X_ such that **_x_**<sup>_′_</sup> _≺_ **_x_**<sup>_∗_</sup> . In other words, no feasible solution exists that can improve one objective without degrading another. The set of all Pareto-optimal solutions in the decision space is defined as Pareto set, whose mapping in the objective space yields the Pareto front (PF). 

**Multi-Operator Solver.** The performance of MOEAs depends on the operators or search strategies employed, including their actions and parameter settings. We define a solver _S_ ( _d |_ **_O_** ) parameterized by a combination of _K_ operators **_O_** = ( _O_ 1 _, O_ 2 _, . . . , OK_ ), which generates candidate solution set _A ⊂X_ for a specific problem instance _d_ : 



Each operator _Oi_ , _i ∈_ 1 _, ..., K_ is instantiated through the algorithm generator _G_ ( _· | pi_ ) guided by a prompt _pi_ containing the reference information about the code template of _Oi_ . Prompts are generated by the prompt generator _P_ ( _· | Oi_ ), and all prompts form the tuple **_p_** = ( _p_ 1 _, p_ 2 _, . . . , pK_ ). Operators act on specific decision subspaces and perform search operations to optimize solutions. 

**Operator Combination Optimization.** In the multioperator optimization framework, each operator _Oi_ in the operator combination can be iteratively refined through evolutionary updates to enhance the solver’s overall performance. 

To obtain a scalar performance value from a multi-objective evaluation, the performance of the solution set is evaluated by an aggregation function Φ( _·_ ), mapping it to a scalar in R: 



This function maps the multi-objective performance set into a single-valued score, where Φ( _·_ ) can represent metrics such as the Hypervolume (HV) (Zitzler and Thiele 1999), the Inverted Generational Distance (IGD) (Coello and Cortes´ 2005)). To reduce stochastic variance, multiple independent evaluations are conducted. Given _N_ evaluations on instance _d_ , the performance of the _n_ -th evaluation is doneted as _F_<sup>_n_</sup> ( _d |_ **_O_** ). The averaged performance with _N_ evaluations under the solver _S_ parameterized by **_O_** is calculated as: 



The operator combination **_O_** belongs to the multi-operator space **S** , and **_O_** can be sampled using algorithm and prompt generators. Assuming instance set _D_ , the overall optimization objective given a limited budget is formulated as: 



Although this formulation models operator combination evolution as a higher-level optimization and accounts for their collective contribution, it does not explicitly capture the interdependencies among operators during the search process. These dynamic dependencies can be further analyzed through a Markov Decision Process (see **Appendix** C). 

## **3 Methodology** 

### **3.1 Overall Framework of E2OC** 

E2OC designs multi-operators in MOEAs automatically by using LLM to co-evolve operator combinations and design strategies. The overall framework is shown in Figure 2, including four core components: **1) Warm-start:** the algorithm generator _G_ ( _· |_ **_p_** 0) is employed to generate candidate operator combination set _OS_ with a prompt containing the initial prompt template tuple **_p_** 0 included code templates. Then the elite operators are then analyzed and summarized using the prompt generator _P_ ( _·_ ) to extract different design thoughts. **2) Language space of design ideas:** The multi-domain design thoughts extracted from elite operators constitute the language space of operator design strategies, with complex crossdomain coupling relationships. **3) Progressive search for design strategy:** Different combinations of design thoughts in the language space are explored and evaluated by MCTS to locate the best potential strategy. **4) Multi-Operator Design and Evaluation:** The operators in the operator combinations are designed sequentially rotating one by one based on the design strategy. The newly generated operator combinations will be integrated in MOEAs to evaluate the performance and the scores will be used to update the branching information of the Monte Carlo tree. 

E2CO combines different interdependent operator design thoughts to achieve a co-evolution of the design strategies and 

executable codes. Notably the specific operator improvement suggestions in the design strategy are integrated into the prompts for evolution. Unlike modifying prompts directly with LLM, it enables the exploration and optimization of design knowledge at semantic level. 

### **3.2 Warm-Start Initialization of Multi-Operator Sets** 

Different operators in MOEAs have their own independent coding domains and neighborhood structures, and their effective co-designs are often characterized as strong coupling, diverse and weakly separable. Primarily, E2OC performs independent evolution and knowledge extraction for each operator _Oi_ , _i ∈_ 1 _, ..., K_ (see Algorithm 1): 

**Step 1:** For different operator _i_ , the candidate operators are generated by the algorithm generator _Gi_ ( _· | pi_ ) based on initial prompts _pi ∈_ **_p_** 0. And the operators are checked for validity to remove illegal and invalid operators. 

**Step 2:** Initialize the multi-operator solver _S_ ( _·_ ) with the optimization problem to construct the multi-objective evaluator _Eva_ ( _·_ ). It enables rapid evaluation of operators in the instance set _D_ and computes the performance _F_<sup>¯</sup><sup>_N_</sup> as a score _fit_ for the candidate operator combination set _OS_ . It will be referenced for operator ranking and elite operator filtering. 

**Step 3:** The prompt generator _P_ ( _·_ ) analyzes elite operators for dominance and incorporates them as code templates into the initialized prompt storage _PS_ , highlighting potential improvements and constraints for future iterations. 

Through the above independent evolution, E2OC establishes an interpretable a prior design knowledge surface and a robust code family for each operator, providing reusable design thoughts and code templates support for subsequent strategy search and coupled exploration. 

### **3.3 Language Space of Multi-Domain Thoughts** 

Operator design thoughts correspond to semantic-level representations of operators. Each thought defines a decision paradigm or an improvement direction, and their interactions collectively determine the overall performance. Owing to structural and functional differences, design thoughts for different operators reside in distinct knowledge spaces. Their relationships can be categorized into two types: 

**Internal relationships** refer to topological associations among different design thoughts of the same operator. They characterize the relative strengths, weaknesses, and inheritance relationships of alternative implementations and can be evaluated by keeping other operators fixed. **External relationships** denote cross-domain dependencies between design thoughts of different operators. These include complementary, conflicting, or mutually exclusive effects arising from distinct functional roles. Properly coordinating these design thoughts is crucial for achieving global optimization. 

Since design thoughts are expressed in language and knowledge rather than numerical variables, their coupling relationships cannot be directly optimized using conventional numerical methods. 



<!-- Start of picture text -->
Defining Design Tasks Multi-Operator Design Strategies Progressive Search<br>Selection Expansion Simulation Backpropagation<br>Prompt P 1<br>∈<br>Problem Solver Template P 2<br>Selected node<br>Independent Operator Search P 3<br>Expanded node Update value<br>P 4<br>∈  Prompt Tuple scores<br>Sequential  ... Coupling Multi-Operator Design and Evaluation<br>Algorithm design Operator  B) Search individual operator init prompt Thought i Tuple<br>Generator  Set<br>∈  Multi-Operator  A) Determine<br>... ...... ... Rotation Design and Evolution operator to be designed<br>AI-A Selection & Analysis ...... ... Optimization Operator Combination<br>Prompt Rewrite  ∈  Opt imal<br>Generator  templates  Codes C) Update Operator  Others remain<br>Analysis and Thought Extraction Language Space of Multi-Domain Design Thoughts Combination unchanged<br>AI-S<br>AI-S<br><!-- End of picture text -->

Figure 2: The E2OC framework. **Left:** Warm-start stage, where operator sets are independently designed and improvement suggestions are analyzed for each operator. **Center:** The multi-domain design thought language space, in which prompts generated by different operator design thoughts exhibit complex coupling relationships. **Right:** MCTS-based branch selection and expansion are employed to explore promising design strategies, while operator rotation evolution is used to reinforce dominant search paths. 

### **3.4 Progressive Design Strategy Search** 

To address this challenge, we employ a progressive MCTSbased mechanism to explore synergistic paths within the multi-domain design thought space. By balancing exploration and exploitation, this approach identifies effective strategies to guide downstream operator implementation. Here, the design space is modeled as a tree where states of the nodes represent the design thoughts in different domains, and edges denote feasible transitions between them. For a node _j_ , the state maintains statistical information including the accumulated performance score _scoj_ and the visit count _vsj_ . Let _p_ denote its parent node. Node selection is guided by the Upper Confidence Bound (UCB) criterion: 



where the first term captures empirical performance, while the second promotes exploration of less-visited paths, with the intensity controlled by _c_ (defaulting to _√_ 2). Following the standard MCTS procedure summarized in Algorithm 2, each iteration executes four key stages: 

**Selection.** Starting from the root node, child nodes are recursively selected according to the UCB criterion, allowing the search to focus on high-potential design paths while preserving exploration of alternative strategies. 

**Expansion.** If the selected node has not reached the predefined number _K_ of operators, it is expanded by appending new operator design thoughts sampled from the feasible prompt storage _PS_ , extending the current state. 

**Simulation.** When the length of the operator thoughts reaches _K_ , a multi-operator rotation design and evaluation 

is performed. Otherwise, additional thoughts are randomly sampled to complete the design state, enabling stochastic rollout and approximate evaluation. 

**Backpropagation.** After simulation, the obtained performance feedback is propagated along the search path. The accumulated score _scoj_ of each visited node is updated using the fitness value _fitj_ , reinforcing effective design strategies and guiding subsequent search decisions. 

After each external iteration, MCTS selects the operator combination **_O_** _best_ (output **_O_**<sup>_∗_</sup> when the iteration ends) and prompt tuple **_p_** _best_ with the highest score as the best. 

### **3.5 Operator Rotation Evolution** 

The operator rotation mechanism performs multi-operator design and evaluation guided by a design strategy, using an algorithm generator integrated with LLM. During rotation, the operator combination is progressively updated by replacing individual operators and evaluating their impact on overall performance. 

Initially, a evaluator _Eva_ ( _·_ ) assesses the performance of the initial operator combination **_O_** 1 on the instance set _D_ , yielding an initial fitness value _fit_ . During each inner iteration, for a given operator _Oi_ , its design prompt _pi_ is retrieved from the prompt tuple **_p_** , and a candidate operator set _OSi_ is generated accordingly. The candidate operator _Oi_<sup>_′_with the</sup> highest fitness is selected to replace _Oi ∈ OSi_ , producing an updated operator combination **_O_**<sup>_′_</sup> (see Algorithm 3). 

The updated combination **_O_**<sup>_′_</sup> is then evaluated to obtain a new fitness value _fit_<sup>_′_</sup> . If _fit_<sup>_′_</sup> exceeds the current best fitness, both the optimal operator combination **_O_** _best_ and its fitness are updated. Through repeated inner iterations and operator 

rotations, the operator combination is progressively refined, resulting in a high-performing operator set and its associated design prompts. 

## **4 Experiments** 

### **4.1 Experimental Setting** 

**Benchmarks and Datasets.** The proposed E2OC is evaluated on two classical MCOPs: the Multi-objective Flexible Job Shop Scheduling Problem (FJSP) (Dauzere-P` er´ es` et al. 2024) and the Traveling Salesman Problem (TSP) (Lust and Teghem 2010b). Both problems are investigated in both bi-objective and tri-objective settings, as detailed in Appendix F and G. 

- **FJSP:** Experiments are conducted on the Brandimarte benchmark set (Brandimarte 1993), which consists of 15 instances of varied scale and complexity, including the highly constrained mk15 instance. The optimization objectives include the minimization of makespan, total machine load, and maximum machine load. 

- **TSP:** Following the _M_ -objective formulation (Chen et al. 2023), each instance is defined by _M_ distinct twodimensional coordinate sets for _k_ nodes. A candidate solution is evaluated by _M_ objectives, where the _m_ -th objective represents the total tour length calculated within the _m_ -th coordinate space. We evaluate performance across problem scales _k ∈{_ 20 _,_ 50 _,_ 100 _}_ . 

**Hyperparameters.** E2OC is designed offline (similar to offline training) to obtain high-quality multi-operator combinations before online evaluation. The control parameters of E2OC are configured as follows: the external iteration count, intermediate iteration number for operator alternation, and inner iteration number for the algorithm generator are set to 30, 5, and 10, respectively, with a population size of 10. After experimental validation of different models and parameters(see **Appendix** ), deepseek-chat is selected as the large language model, with the initial number of newly generated prompts set to 3. The computational resources used in the evaluation process are larger than training. 

Detailed parameter specifications of MOEAs for different problems and the configurations of different AHD method are presented in Appendix I.3. 

**Baselines.** We compare with several MOEAs using classical operators, advanced AHD methods and co-design frameworks: (1) MOEAs include: a) the dominance-relation-based **NSGA-II** (Deb et al. 2002) and **NSGA-III** (Deb and Jain 2014) which represent one of the mainstream solutions for MCOPs, and b) the decomposition-based **MOEA/D** (Qingfu Zhang and Hui Li 2007). These methods employ commonly used crossover, mutation, and neighborhood search operators, as described in **Appendix** F.2 and G.2. (2) Advanced LLMbased single-heuristic design methods: **Random** (Zhang et al. 2024b), **FunSearch** (Romera-Paredes et al. 2024), **EoH** (Liu et al. 2024a), **ReEvo** (Ye et al. 2024) and **MCTSAHD** (Zheng et al. 2025b). All experiments are conducted on LLM4AD platform (Liu et al. 2024b). (3) Different multiheuristic co-design frameworks, such as those based on Coordinate-Descent ( **CD** ), Upper-Confidence-Bound( **UCB** ), 

**LLM** , **MCTS** and their variants, are described in detail in **Appendix** I.2. All AHD methods are configured to use the same evaluation budget. 

**Metrics.** MOEAs are evaluated with Hypervolume (HV) and Inverted Generational Distance (IGD). Results are reported as means over multiple independent runs. For automatic design methods, we assess performance with Relative Improvement (RI), code accuracy, computational cost, and quality cost, highlighting best values in bold. Further details are available in the **Appendix** . 

### **4.2 Main results** 

**Comparison with Expert Design.** This section compares operator combinations generated by E2OC with expert-designed combinations on multi-objective FJSP and TSP instances in NSGA-II, NSGA-III and MOEA/D. The operator setting details are provided in Appendix F.2 and G.2. Instances are split into training, testing, and all sets. All algorithms are independently executed five times, and the average HV, IGD, and RI are Summarized in Table 1. 

_Bi-objective FJSP & TSP._ On bi-objective problems, E2OC consistently outperforms expert-designed operators. Although NSGA-II with expert operators initially performs best, E2OC improves its HV by 22.00% (FJSP) and 14.00% (TSP), and even improved the MOEA/D (TSP) by 16.92%. Across all algorithms, E2OC delivers at least a 10% improvement, indicating that the evolved operators expand the coverage of high-quality solutions in the objective space. 

_Tri-objective FJSP & TSP._ On tri-objective problems, performance gains remain significant, albeit slightly lower. With equal evaluation budgets, E2OC improves HV by 17.36% in tri-objective FJSP under NSGA-II, surpassing human-designed paradigms. Notably, E2OC achieves the highest average improvement across all testing instances, demonstrating strong generalization and robustness without overfitting to the training data. 

**Comparison with LLM-based AHD Methods** Table 6 compares existing LLM-based AHD methods and multi-heuristic design frameworks on the Bi-FJSP. All methods design operators for NSGA-II starting from identical initial combinations, under the same evaluation budget. Details of the methods are provided in **Appendix** I.2. 

_Single-heuristic design._ In single-heuristic design methods, each operator is designed sequentially with equal budget. On the training instance, FunSearch achieves the best mean HV (0.1712) over five independent runs. On testing and all instances, MCTS-AHD performs best, highlighting the effectiveness of MCTS in such co-design scenarios. E2OC consistently outperforms all methods across all instances, reaching the HV of 0.2435. This demonstrates that co-evolving design strategies and codes yields greater advantages than sequentially optimizing operators independently. 

_Multi-heuristic design._ Among multi-operator co-design frameworks, methods based on CD, UCB, and direct LLM-guided decisions degrade in performance; the purely LLM-driven approach performs worst. This confirms that relying solely on LLMs or expert knowledge to directly control operator combination design in MOEAs is ineffective. 



<!-- Start of picture text -->
HV (mean ± CI) 5400 Pareto Front (best run per method) 3.5 IGD (mean ± CI)<br>0.18 5350 3.0<br>0.17<br>5300 2.5<br>0.16<br>5250 2.0<br>0.15<br>0.14 5200 1.5<br>5150<br>0.13 1.0<br>0.12 5100<br>0.5<br>0.11 5050<br>0.0<br>0 4 8 12 16 20 24 28 800 1000 1200 1400 1600 0 4 8 12 16 20 24 28<br>Generation obj1 Generation<br>(a) HV on testing instance (b) IGD on testing instance (c) PF on testing instance<br>Random EoH MCTS-AHD UCB Win-UCB<br>FunSearch ReEvo CD LLM E2OC<br>HV obj2 IGD<br><!-- End of picture text -->

Figure 3: Performance of different AHD methods on BIFJSP testing (mk14) instances. 

Win-UCB achieves the second-best result after E2OC, with an HV of 0.1763 on the training instance, which significantly surpasses all single-heuristic designs, but it underperforms on other instances. E2OC attains the highest average performance across all instances, indicating that its learned strategies generalize robustly to different problem instances rather than overfitting to the training data. 

### **4.3 Ablation Studies** 

The core components of E2OC comprise progressive design-strategy search and operator-rotation evaluation. We perform ablations on these components to examine their respective contributions. In variant **MCTS** **~~O~~ C** , the progressive search of operator combinations is replaced with a single fixed design strategy. In variant **E2OC-SD** , the operator-rotation mechanism is replaced with sequential operator design, where the evaluation budget is uniformly allocated across operators and design proceeds sequentially. We further test several advanced AHD methods to verify compatibility with different operator designers. The HV and IGD performance across instance are reported in Table 3. 

Removing progressive search causes notable performance degradation in MCTS ~~O~~ C, indicating that under a fixed evaluation budget, the ability to switch design strategies is more effective than sequential operator design with a fixed strategy. Moreover, compared to sequential independent design, the operator rotation mechanism finds local optima more efficiently in complex algorithm spaces, which significantly accelerates the evaluation of operator strategies. The choice of operator designer also affects overall performance, with EoH achieving the best results. 

## **5 Discussion and Future Works** 

### **5.1 Discussion** 

**Different LLMs** The performance of E2OC and other LLM-based AHD methods depends significantly on the underlying LLM, which influences the quality of generated design thoughts and operator code. We evaluate six representative LLMs from the DeepSeek, GPT, Qwen, and 

Gemini families on the NSGA-II operator design task for Bi-FJSP under consistent experimental conditions. Search performance, evaluation performance, and computational cost are summarized in Table 4. Results indicate that stronger general-purpose LLMs do not consistently achieve better performance in improvement summarization or operator design on E2OC . Although gpt-4.1-mini attains the best search performance on some instances, deepseek-chat offers a more favorable trade-off overall, with competitive performance, lower evaluation cost, and a higher quality-cost ratio. Therefore, deepseek-chat is selected as the default backbone model in subsequent experiments. 

**Different MCTS variants** MCTS supports effective reuse of branching information and offers a structured framework for modeling dependencies among multiple operators. We compare four MCTS variants for multi-operator co-design according to state representation and expansion mechanisms: MCTS ~~O~~ C progressively searches operator combinations; MCTS ~~T~~ uple progressively searches design strategies with node states as design-thought tuples; MCTS ~~S~~ ample progressively samples and searches design thoughts during expansion; and E2OC searches a warm-start-built design thought space (details in **Appendix** E). 

For fairness, MCTS ~~O~~ C and MCTS ~~T~~ uple impose no restriction on LLM sampling, while MCTS ~~S~~ ample and E2OC limit the sampled design thoughts per operator to _AP_ , with E2OC pre-constructing the design strategy space. Experimental results are summarized in Table 5. Under a fixed evaluation budget, E2OC attains the best performance across all instance sets, achieving HV values of 0.1985 (training), 0.2467 (testing), and 0.2435 (all). These results demonstrate that searching in a fixed, structured design-thought space identifies high-quality design strategies more efficiently than dynamically sampling thoughts during tree expansion. 

**Continuous Optimization Analysis** The design thought space of E2OC is initialized from an elite operator set obtained during the warm-start phase, allowing progressive discovery of strategies and operator combinations that surpass expert-designed baselines. To examine its potential for sus- 

Table 1: Comparison with expert-designed MOEAs. The mk15 (FJSP) and 100-node TSP instances are used for training, and all other instances form the testing set. Each method is run 5 times, and the mean HV and IGD are reported. RI indicates the relative improvement in HV over the baseline. 

|**Bi-F**|**JSP**<br>Method|**All ins**<br>HV_↑_|**tances**<br>IGD_↓_|**Train i**<br>HV_↑_|**nstance**<br>IGD_↓_|**Test in**<br>HV_↑_|**stances**<br>IGD_↓_|RI_↑_|
|---|---|---|---|---|---|---|---|---|
|ert|NSGA-II|0.1996|2.2487|0.1515|1.2512|0.2030|2.3199|-|
|xp|NSGA-III|0.1927|2.4938|0.1470|1.3507|2.5755|0.2217|-|
|E|MOEA/D|0.1853|2.8155|0.1493|1.2450|0.1879|2.9276|-|
|C|NSGA-II|0.2435|1.1579|0.1985|0.6830|0.2467|1.1918|22.00%|
|2O|NSGA-III|0.2182|1.6684|0.1695|0.8806|0.2217|1.7247|13.27%|
|E|MOEA/D|0.2256|1.4585|0.1763|0.7566|0.2292|1.5086|21.78%|
|**Bi-T**|**SP**|**Bi-T**|**SP20**|**Bi-T**|**SP50**|**Bi-TS**|**P100**|RI|
||Method|HV_↑_|IGD_↓_|HV_↑_|IGD_↓_|HV_↑_|IGD_↓_|_↑_|
|ert|NSGA-II|0.3881|0.3439|0.3484|0.3638|0.4079|0.3340|-|
|xp|NSGA-III|0.3656|0.3971|0.3244|0.4097|0.3862|0.3908|-|
|E|MOEA/D|0.3674|0.4045|0.3293|0.4050|0.3865|0.4042|-|
|C|NSGA-II|0.4424|0.2257|0.4281|0.2206|0.4495|0.2282|14.00%|
|2O|NSGA-III|0.4125|0.2957|0.3854|0.2851|0.4260|0.3009|12.81%|
|E|MOEA/D|0.4296|0.2279|0.4060|0.2336|0.4414|0.2251|16.92%|
|**Tri-**|**FJSP**|**All ins**|**tances**|**Train i**|**nstance**|**Test in**|**stances**|RI|
||Method|HV_↑_|IGD_↓_|HV_↑_|IGD_↓_|HV_↑_|IGD_↓_|_↑_|
|ert|NSGA-II|0.1266|1.8398|0.0960|0.9831|0.1287|1.9010|-|
|xp|NSGA-III|0.1200|2.1074|0.0928|1.0744|0.1220|2.1812|-|
|E|MOEA/D|0.1116|2.3652|0.0786|1.2435|0.1139|2.4454|-|
|C|NSGA-II|0.1485|1.1619|0.1183|0.6368|0.1507|1.1994|17.36%|
|2O|NSGA-III|0.1407|1.4379|0.1111|0.7956|0.1428|1.4838|17.24%|
|E|MOEA/D|0.1229|1.9366|0.0820|1.1123|0.1258|1.9955|10.15%|
|**Tri-**|**TSP**|**Bi-T**|**SP20**|**Bi-T**|**SP50**|**Bi-TS**|**P100**||
||Method|HV_↑_|IGD_↓_|HV_↑_|IGD_↓_|HV_↑_|IGD_↓_|RI_↑_|
|rt|NSGA-II|0.1824|0.2235|0.1266|0.2020|0.2104|0.2342|-|
|xpe|NSGA-III|0.1773|0.2251|0.1215|0.2028|0.2052|0.2363|-|
|E|MOEA/D|0.1800|0.2221|0.1251|0.1997|0.2074|0.2333|-|
|C|NSGA-II|0.1939|0.2200|0.1333|0.2075|0.2243|0.2262|6.30%|
|2O|NSGA-III|0.1873|0.2110|0.1292|0.1983|0.2163|0.2173|5.63%|
|E|MOEA/D|0.1867|0.2052|0.1286|0.1858|0.2157|0.2149|3.73%|



tained optimization, we conduct three consecutive E2OC runs on the NSGA-II operators design task for Bi-FJSP, where the output strategies and operators of each run are reused as inputs for the next. 

The results show consistent performance improvements in both the second E2OC<sup>_′_</sup> and third E2OC<sup>_′′_</sup> runs compared with the previous ones in Table 5, demonstrating that initializing E2OC with increasingly stronger design strategies and operator sets further enhances performance. This iterative reconstruction of the design thought space endows E2OC with clear continuous optimization capability. 

### **5.2 Future Works** 

Although LLM-based AHD has recently gained attention, it remains at an early stage of development. Existing studies indicate substantial potential in automatic algorithm design, warranting deeper and more systematic investigation. 

**Semantic-level Optimization** LLMs introduce an optimization paradigm that operates in semantic spaces rather than purely numerical or combinatorial domains. Future research should focus on developing principled formulations and tools for semantic-level optimization, where language and knowledge representations define the search space and optimization dynamics. 

Table 2: Comparison of AHD methods on Bi-FJSP. All operator combinations are evaluated 5 times independently in NSGA-II, with mean performance reported. Best values are in bold. 

|**T**|**Mthd**|**All insta**|**ces**|**Train in**|**stace**|**Test ins**|**taces**|
|---|---|---|---|---|---|---|---|
|**ype**|**eo**|HV_↑_|IGD_↓_|HV_↑_|IGD_↓_|HV_↑_|IGD_↓_|
||Random|0.2263|1.4193|0.1702|0.8546|0.2303|1.4597|
|e|FunSearch|0.2265|1.4070|0.1712|0.8386|0.2210|1.4193|
|gl|EoH|0.2258|1.4352|0.1694|0.8409|0.2298|1.4777|
|Sin|ReEvo|0.2185|1.6551|0.1669|0.8712|0.2222|1.7110|
||MCTS-AHD|0.2269|1.3950|0.1709|0.8371|0.2309|1.4348|
||CD|0.2170|1.6536|0.1630|0.9572|0.2209|1.7033|
|ti|UCB|0.2182|1.6300|0.1663|0.9296|0.2219|1.6800|
|ul|LLM|0.2148|1.8772|0.1654|0.9424|0.2183|1.9440|
|M|Win-UCB|0.2256|1.4619|0.1763|0.7566|0.2292|1.5123|
||E2OC|**0.2435**|**1.1423**|**0.1985**|**0.6830**|**0.2467**|**1.1751**|



Table 3: Ablation study with different design baselines. All designs are evaluated 5 times in NSGA-II; mean performance is reported, with best values in bold. 

|**Method**|**All inst**<br>HV_↑_|**ancess**<br>IGD_↓_|**Train in**<br>HV_↑_|**stances **<br>IGD_↓_|**Test ins**<br>HV_↑_|**tancess**<br>IGD_↓_|
|---|---|---|---|---|---|---|
|MCTS<br>~~O~~C|0.2085|1.8893|0.1583|1.1519|0.2121|1.9420|
|E2OC-SD|0.2187|1.8893|0.1713|0.8272|0.2221|1.6484|
|E2OC[EoH]|**0.2435 **|**0.2264 **|**0.1985**|**0.7349**|**0.2467 **|**1.1752**|
|E2OC[FunSearch]|0.2264|1.4115|0.1754|0.7908|0.2300|1.4558|
|E2OC[MCTS-AHD]|0.2269|1.3961|0.1785|0.7924|0.2303|1.4393|
|E2OC[ReEvo]|0.2213|1.5289|0.1719|0.8340|0.2248|1.5786|



Table 4: Comparison of different LLMs. The<sup>_∗_</sup> denotes opensource models, which are less expensive for local deployment. Ratio denotes the quality-cost ratio, defined as performance improvement over the baseline divided by cost. Shading marks the most cost-effective model. 

||**Search**|**perform**|**ance**|**Evalu**|**ation**|**E**|**xpenditu**|**re**|
|---|---|---|---|---|---|---|---|---|
|**LLM**|ValidR_↑_|Mean_↑_|Range_↑_|HV_↑_|IGD_↓_|Tok.(M)|Cost($)_↓_|Ratio_↓_|
|deepseek-chat|99.76%|0.1485|**0.168**|**0.2271**|1.5437|3.34|**1.14**|**41.53**|
|gpt-4.1-mini|99.97%|**0.1502**|0.043|0.2266|**1.4234**|3.41|1.22|45.23|
|gpt-4o-mini|**100.00%**|0.1458|0.161|0.2211|1.5840|**2.44**|2.23|103.29|
|qw3-8b<sup>_∗_</sup>|99.93%|0.1475|0.163|0.2258|1.4556|2.83|3.19|121.99|
|qw3-30b-A3b<sup>_∗_</sup>|99.93%|0.1473|0.165|0.2244|1.4997|5.39|13.56|222.87|
|gemini-2.5-pro|99.90%|0.1482|0.163|0.2223|1.5745|14.35|117.84|5196.28|



Table 5: Comparison of MCTS variants and validation of continuous optimization. Gray highlighting indicates the best single-run performance; bold denotes the global optimum. 

|**Mthd**|**All inst**|**ancess**|**Train in**|**stances**|**Test ins**|**tancess**|
|---|---|---|---|---|---|---|
|**eo**|HV_↑_|IGD_↓_|HV_↑_|IGD_↓_|HV_↑_|IGD_↓_|
|MCTS<br>~~O~~C|0.2085|2.3828|0.1583|2.0977|0.2121|2.4031|
|MCTS<br>~~T~~uple|0.2186|2.0888|0.1655|1.9628|0.2224|2.0978|
|MCTS<br>~~S~~ample|0.2181|2.1088|0.1633|1.9905|0.2220|2.1172|
|E2OC|0.2435|1.7749|0.1985|1.1188|0.2467|1.8217|
|E2OC<sup>_′_</sup>|0.2454|1.6617|0.1986|1.1095|0.2487|1.7012|
|E2OC<sup>_′′_</sup>|**0.2475**|**1.5453**|**0.1999**|**1.0238**|**0.2509**|**1.5826**|



**Human–AI Co-design** The design strategies in E2OC provide continuous guidance for heuristic evolution and improve 

interpretability. However, practical deployment under complex constraints requires effective integration of expert knowledge. Future work could explore interactive optimization frameworks that incorporate human preferences or expert evaluations to guide and accelerate algorithm design. 

**Autonomous Algorithmic System Evolution** Current LLM-based AHD frameworks have demonstrated promise but often rely on limited supervision and relatively simple algorithm structures. A key direction is to exploit LLMs’ selfreflection and multi-agent coordination capabilities to support autonomous, iterative evolution of algorithmic systems, which calls for systematic modeling of algorithm representations and their dynamic evolution mechanisms. 

## **6 Conclusion** 

This paper investigates the automated evolution of the interdependent operators in MOEAs. We propose an E2OC framework that co-evolves design strategies with executable codes of operator combination. Progressive search based on Monte Carlo trees is employed to explore combinations of different operator design thoughts. The optimal operator combination is systematically searched and determined through operator rotation evolution, and supports the integration of mainstream AHD methods as the underlying algorithm generator. We evaluate E2OC on both bi-objective and tri-objective FJSP and TSP. The experimental results show that E2OC consistently outperforms mature human-designed operators across multiple MOEAs. By explicitly modeling and exploring interdependencies among operators, E2OC also achieves superior performance compared to state-of-the-art AHD methods. 

## **Acknowledgements** 

The work described in this paper was supported by the Research Grants Council of the Hong Kong Special Administrative Region, China (GRF Project No. CityU11217325), and the Natural Science Foundation of China (Project No: 62276223). 

## **Impact Statement** 

This paper presents work whose goal is to advance the field of Machine Learning. There are many potential societal consequences of our work, none of which we feel must be specifically highlighted here. 

## **References** 

Akiba, T.; Sano, S.; Yanase, T.; Ohta, T.; and Koyama, M. 2019. Optuna: A next-generation hyperparameter optimization framework. In _Proceedings of the 25th ACM SIGKDD international conference on knowledge discovery & data mining_ , 2623–2631. 

Ardeh, M. A.; Mei, Y.; and Zhang, M. 2021. Genetic programming with knowledge transfer and guided search for uncertain capacitated arc routing problem. _IEEE Transactions on Evolutionary Computation_ , 26(4): 765–779. Brandimarte, P. 1993. Routing and scheduling in a flexible job shop by tabu search. _Annals of Operations Research_ , 41(3): 157–183. 

Burke, E. K.; Gendreau, M.; Hyde, M.; Kendall, G.; Ochoa, G.; Ozcan, E.; and Qu, R. 2013.<sup>¨</sup> Hyper-heuristics: A survey of the state of the art. _Journal of the Operational Research Society_ , 64: 1695–1724. 

Burke, E. K.; Hyde, M. R.; Kendall, G.; Ochoa, G.; Ozcan,<sup>¨</sup> E.; and Woodward, J. R. 2019. A classification of hyperheuristic approaches: revisited. _Handbook of metaheuristics_ , 453–477. 

Chen, J.; Zhang, Z.; Cao, Z.; Wu, Y.; Ma, Y.; Ye, T.; and Wang, J. 2023. Neural multi-objective combinatorial optimization with diversity enhancement. _Advances in Neural Information Processing Systems_ , 36: 39176–39188. 

Chen, P.; Liang, J.; Qiao, K.-J.; Song, H.; Suganthan, P. N.; Dai, L.-L.; and Ban, X.-X. 2025. A Reinforced Neighborhood Search Method Combined With Genetic Algorithm for Multi-Objective Multi-Robot Transportation System. _IEEE Transactions on Intelligent Transportation Systems_ . 

Coello, C. A. C.; and Cortes, N. C. 2005.´ Solving multiobjective optimization problems using an artificial immune system. _Genetic Programming and Evolvable Machines_ , 6: 163–190. Coulom, R. 2007. Computing “elo ratings” of move patterns in the game of go. _ICGA journal_ , 30(4): 198–208. 

d O Costa, P. R.; Rhuggenaath, J.; Zhang, Y.; and Akcay, A. 2020. Learning 2-opt heuristics for the traveling salesman problem via deep reinforcement learning. In _Asian conference on machine learning_ , 465–480. PMLR. 

Dat, P. V. T.; Doan, L.; and Binh, H. T. T. 2025. HSEVO: Elevating automatic heuristic design with diversity-driven harmony search and genetic algorithm using llms. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , 26931–26938. 

Dauzere-P` er´ es,` S.; Ding, J.; Shen, L.; and Tamssaouet, K. 2024. The flexible job shop scheduling problem: A review. _European Journal of Operational Research_ , 314(2): 409–432. Deb, K.; and Jain, H. 2014. An Evolutionary Many-Objective Optimization Algorithm Using Reference-Point-Based Nondominated Sorting Approach, Part I: Solving Problems With Box Constraints. _IEEE Transactions on Evolutionary Computation_ , 18(4): 577–601. 

Deb, K.; Pratap, A.; Agarwal, S.; and Meyarivan, T. 2002. A fast and elitist multiobjective genetic algorithm: NSGAII. _IEEE Transactions on Evolutionary Computation_ , 6(2): 182–197. 

Drake, J. H.; Kheiri, A.; Ozcan, E.; and Burke, E. K. 2020.<sup>¨</sup> Recent advances in selection hyper-heuristics. _European Journal of Operational Research_ , 285(2): 405–428. 

Fu, Z.-H.; Qiu, K.-B.; and Zha, H. 2021. Generalize a small pre-trained model to arbitrarily large tsp instances. In _Proceedings of the AAAI conference on artificial intelligence_ , volume 35, 7474–7482. 

Garivier, A.; and Cappe, O. 2011.´ The KL-UCB algorithm for bounded stochastic bandits and beyond. In _Proceedings of the 24th annual conference on learning theory_ , 359–376. JMLR Workshop and Conference Proceedings. 

Gupta, S.; Chaudhari, S.; Joshi, G.; and Yagan,˘ O. 2021. Multi-armed bandits with correlated arms. _IEEE Transactions on Information Theory_ , 67(10): 6711–6732. 

Helsgaun, K. 2000. An effective implementation of the Lin– Kernighan traveling salesman heuristic. _European journal of operational research_ , 126(1): 106–130. 

Hong, L.; Drake, J. H.; Woodward, J. R.; and Ozcan,<sup>¨</sup> E. 2018. A hyper-heuristic approach to automated generation of mutation operators for evolutionary programming. _Applied Soft Computing_ , 62: 162–175. 

Huang, C.; Li, Y.; and Yao, X. 2019. A survey of automatic parameter tuning methods for metaheuristics. _IEEE transactions on evolutionary computation_ , 24(2): 201–216. 

Jaszkiewicz, A.; and Zielniewicz, P. 2009. Pareto memetic algorithm with path relinking for bi-objective traveling salesperson problem. _European Journal of Operational Research_ , 193(3): 885–890. 

Jia, Y.-H.; Mei, Y.; and Zhang, M. 2022. Learning heuristics with different representations for stochastic routing. _IEEE Transactions on Cybernetics_ . 

Kiet, N. V. T.; Van Tung, D.; Dao, T. C.; and Binh, H. T. T. 2025. MOTIF: Multi-strategy Optimization via Turn-based Interactive Framework. _arXiv preprint arXiv:2508.03929_ . Kumar, R.; and Singh, P. 2007. Pareto evolutionary algorithm hybridized with local search for biobjective TSP. _Hybrid Evolutionary Algorithms_ , 75(1): 361–398. 

Lan, W.; Ye, Z.; Ruan, P.; Liu, J.; Yang, P.; and Yao, X. 2021. Region-focused memetic algorithms with smart initialization for real-world large-scale waste collection problems. _IEEE Transactions on Evolutionary Computation_ , 26(4): 704–718. 

Langdon, W. B.; and Poli, R. 2013. _Foundations of genetic programming_ . Springer Science & Business Media. Li, F.; Gao, L.; and Shen, W. 2022. Surrogate-assisted multiobjective evolutionary optimization with Pareto front modelbased local search method. _IEEE Transactions on Cybernetics_ , 54(1): 173–186. 

Li, R.; Wang, L.; Gong, W.; and Ming, F. 2024a. An evolutionary multitasking memetic algorithm for multi-objective distributed heterogeneous welding flow shop scheduling. _IEEE Transactions on Evolutionary Computation_ . 

Li, R.; Wang, L.; Gong, W.; and Ming, F. 2024b. An evolutionary multitasking memetic algorithm for multi-objective distributed heterogeneous welding flow shop scheduling. _IEEE Transactions on Evolutionary Computation_ . 

Li, R.; Wang, L.; Sang, H.; Yao, L.; and Pan, L. 2025. LLMassisted automatic memetic algorithm for lot-streaming hybrid job shop scheduling with variable sublots. _IEEE Transactions on Evolutionary Computation_ . 

Liao, R.; Qiu, J.; Chen, X.; and Li, X. 2025. LLM4EO: Large Language Model for Evolutionary Optimization in Flexible Job Shop Scheduling. _arXiv preprint arXiv:2511.16485_ . Liu, F.; Liu, Y.; Zhang, Q.; Tong, X.; and Yuan, M. 2025. EoH-S: Evolution of heuristic set using llms for automated heuristic design. _arXiv preprint arXiv:2508.03082_ . 

Liu, F.; Tong, X.; Yuan, M.; Lin, X.; Luo, F.; Wang, Z.; Lu, Z.; and Zhang, Q. 2024a. Evolution of heuristics: Towards efficient automatic algorithm design using large language model. In _Proceedings of the International Conference on Machine Learning_ , 32201–32223. 

Liu, F.; Yao, Y.; Guo, P.; Yang, Z.; Lin, X.; Zhao, Z.; Tong, X.; Mao, K.; Lu, Z.; Wang, Z.; et al. 2026. A systematic survey on large language models for algorithm design. _ACM Computing Surveys_ . 

Liu, F.; Zhang, R.; Xie, Z.; Sun, R.; Li, K.; Lin, X.; Wang, Z.; Lu, Z.; and Zhang, Q. 2024b. Llm4ad: A platform for algorithm design with large language model. _arXiv preprint arXiv:2412.17287_ . 

Lust, T.; and Teghem, J. 2010a. The multiobjective traveling salesman problem: A survey and a new approach. In _Advances in Multi-Objective Nature Inspired Computing_ , 119– 141. Springer. 

Lust, T.; and Teghem, J. 2010b. The multiobjective traveling salesman problem: A survey and a new approach. In _Advances in Multi-Objective Nature Inspired Computing_ , 119– 141. Springer. 

Ma, Z.; Guo, H.; Gong, Y.-J.; Zhang, J.; and Tan, K. C. 2025. Toward automated algorithm design: A survey and practical guide to meta-black-box-optimization. _IEEE Transactions on Evolutionary Computation_ . 

Mara, S. T. W.; Norcahyo, R.; Jodiawan, P.; Lusiantoro, L.; and Rifai, A. P. 2022. A survey of adaptive large neighborhood search algorithms and applications. _Computers & Operations Research_ , 146: 105903. 

Mei, Y.; Chen, Q.; Lensen, A.; Xue, B.; and Zhang, M. 2022. Explainable artificial intelligence by genetic programming: A survey. _IEEE Transactions on Evolutionary Computation_ . Mo, S.; Wu, K.; Gao, Q.; Teng, X.; and Liu, J. 2025. AutoSGNN: Automatic propagation mechanism discovery for spectral graph neural networks. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , 19493–19502. 

Morales-Hernandez,´ A.; Van Nieuwenhuyse, I.; and Rojas Gonzalez, S. 2023. A survey on multi-objective hyperparameter optimization algorithms for machine learning. _Artificial Intelligence Review_ , 56(8): 8043–8093. 

Neufeld, J. S.; Schulz, S.; and Buscher, U. 2023. A systematic review of multi-objective hybrid flow shop scheduling. _European Journal of Operational Research_ , 309(1): 1–23. 

Nguyen, S.; Mei, Y.; and Zhang, M. 2017. Genetic programming for production scheduling: a survey with a unified framework. _Complex & Intelligent Systems_ , 3(1): 41–66. Novikov, A.; Vu, N.; Eisenberger, M.; Dupont, E.; Huang, P.-S.; Wagner, A. Z.; Shirobokov, S.; Kozlovskii, B.; Ruiz, F. J.; Mehrabian, A.; et al. ???? AlphaEvolve: A coding agent for scientific and algorithmic discovery, 2025. _URL: https://arxiv. org/abs/2506.13131_ . 

O’Neill, M.; Vanneschi, L.; Gustafson, S.; and Banzhaf, W. 2010. Open issues in genetic programming. _Genetic Programming and Evolvable Machines_ , 11(3): 339–363. 

Paquete, L.; Chiarandini, M.; and Stutzle, T. 2004a.¨ Pareto local optimum sets in the biobjective traveling salesman problem: An experimental study. In _Metaheuristics for multiobjective optimisation_ , 177–199. Springer. 

Paquete, L.; Chiarandini, M.; and Stutzle, T. 2004b.¨ Pareto local optimum sets in the biobjective traveling salesman problem: An experimental study. In _Metaheuristics for multiobjective optimisation_ , 177–199. Springer. 

Pei, J.; Mei, Y.; Liu, J.; Zhang, M.; and Yao, X. 2025. Adaptive operator selection for meta-heuristics: A survey. _IEEE Transactions on Artificial Intelligence_ . 

Peng, B.; Wei, Y.; Qin, Y.; Dai, J.; Li, Y.; Liu, A.; Tian, Y.; Han, L.; Zheng, Y.; and Wen, P. 2023. Machine learningenabled constrained multi-objective design of architected materials. _Nature Communications_ , 14(1): 6630. 

Pillay, N.; and Qu, R. 2018. _Hyper-heuristics: theory and applications_ . Springer. 

Qingfu Zhang; and Hui Li. 2007. MOEA/D: A Multiobjective Evolutionary Algorithm Based on Decomposition. _IEEE Transactions on Evolutionary Computation_ , 11(6): 712–731. Qiu, J.; Zhuang, H.; Liu, F.; Liu, J.; and Zhang, Q. 2026. LLM-Assisted Automatic Dispatching Rule Design for Dynamic Flexible Assembly Flow Shop Scheduling. _arXiv preprint arXiv:2601.15738_ . 

Romera-Paredes, B.; Barekatain, M.; Novikov, A.; Balog, M.; Kumar, M. P.; Dupont, E.; Ruiz, F. J.; Ellenberg, J. S.; Wang, P.; Fawzi, O.; et al. 2024. Mathematical discoveries from program search with large language models. _Nature_ , 625(7995): 468–475. 

Shi, J.; Sun, J.; Zhang, Q.; Zhang, H.; and Fan, Y. 2022. Improving pareto local search using cooperative parallelism strategies for multiobjective combinatorial optimization. _IEEE Transactions on Cybernetics_ , 54(4): 2369–2382. 

Shinn, N.; Cassano, F.; Gopinath, A.; Narasimhan, K.; and Yao, S. 2023. Reflexion: Language agents with verbal reinforcement learning. _Advances in Neural Information Processing Systems_ , 36: 8634–8652. 

Silver, D.; Huang, A.; Maddison, C. J.; Guez, A.; Sifre, L.; Van Den Driessche, G.; Schrittwieser, J.; Antonoglou, I.; Panneershelvam, V.; Lanctot, M.; et al. 2016. Mastering the game of Go with deep neural networks and tree search. _nature_ , 529(7587): 484–489. 

Stutzle, T.; and L¨ opez-Ib´ a´nez, M. 2019.˜ Automated design of metaheuristic algorithms. _Handbook of metaheuristics_ , 541–579. 

Swiechowski, M.; Godlewski, K.; Sawicki, B.; and Ma´ ndziuk,´ J. 2023. Monte Carlo tree search: A review of recent modifications and applications. _Artificial Intelligence Review_ , 56(3): 2497–2562. 

Tang, K.; Mei, Y.; and Yao, X. 2009. Memetic algorithm with extended neighborhood search for capacitated arc routing problems. _IEEE Transactions on Evolutionary Computation_ , 13(5): 1151–1166. 

van Stein, N.; and Back, T. 2024.¨ Llamea: A large language model evolutionary algorithm for automatically generating metaheuristics. _IEEE Transactions on Evolutionary Computation_ . 

Wang, Z.; Yao, S.; Li, G.; and Zhang, Q. 2023. Multiobjective combinatorial optimization using a single deep reinforcement learning model. _IEEE transactions on cybernetics_ , 54(3): 1984–1996. 

Wei, J.; Wang, X.; Schuurmans, D.; Bosma, M.; Xia, F.; Chi, E.; Le, Q. V.; Zhou, D.; et al. 2022. Chain-of-thought prompting elicits reasoning in large language models. _Advances in neural information processing systems_ , 35: 24824–24837. 

Wright, S. J. 2015. Coordinate descent algorithms. _Mathematical programming_ , 151(1): 3–34. 

Wu, X.; Wu, S.-h.; Wu, J.; Feng, L.; and Tan, K. C. 2024. Evolutionary computation in the era of large language model: Survey and roadmap. _IEEE Transactions on Evolutionary Computation_ . 

Xie, Z.; Liu, F.; Wang, Z.; and Zhang, Q. 2025. LLM-Driven Neighborhood Search for Efficient Heuristic Design. In _2025 IEEE Congress on Evolutionary Computation (CEC)_ , 1–8. IEEE. 

Xu, Z.; Zhang, Y.; Bao, W.; Wang, H.; Chen, M.; Ye, H.; Jiang, W.; Yan, H.; and Wang, J. 2025. AutoEP: LLMsDriven Automation of Hyperparameter Evolution for Metaheuristic Algorithms. _arXiv preprint arXiv:2509.23189_ . 

Yao, S.; Liu, F.; Lin, X.; Lu, Z.; Wang, Z.; and Zhang, Q. 2025. Multi-objective evolution of heuristic using large language model. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 39, 27144–27152. 

Yao, S.; Yu, D.; Zhao, J.; Shafran, I.; Griffiths, T.; Cao, Y.; and Narasimhan, K. 2023. Tree of thoughts: Deliberate problem solving with large language models. _Advances in neural information processing systems_ , 36: 11809–11822. 

Ye, H.; Wang, J.; Cao, Z.; Berto, F.; Hua, C.; Kim, H.; Park, J.; and Song, G. 2024. Reevo: Large language models as hyper-heuristics with reflective evolution. _Advances in neural information processing systems_ , 37: 43571–43608. 

Ye, H.; Xu, H.; Yan, A.; and Cheng, Y. 2025. Large language model-driven large neighborhood search for Largescale MILP problems. In _Proceedings of the International Conference on Machine Learning_ . 

Zhang, F.; Mei, Y.; Nguyen, S.; and Zhang, M. 2023. Survey on Genetic Programming and Machine Learning Techniques for Heuristic Design in Job Shop Scheduling. _IEEE Transactions on Evolutionary Computation_ . 

Zhang, R.; Liu, F.; Lin, X.; Wang, Z.; Lu, Z.; and Zhang, Q. 2024a. Understanding the importance of evolutionary search in automated heuristic design with large language models. In _International Conference on Parallel Problem Solving from Nature_ , 185–202. Springer. 

Zhang, R.; Liu, F.; Lin, X.; Wang, Z.; Lu, Z.; and Zhang, Q. 2024b. Understanding the importance of evolutionary search in automated heuristic design with large language models. In _International Conference on Parallel Problem Solving from Nature_ , 185–202. Springer. 

Zhao, F.; Zhou, G.; and Wang, L. 2023. A cooperative scatter search with reinforcement learning mechanism for the distributed permutation flowshop scheduling problem with sequence-dependent setup times. _IEEE Transactions on Systems, Man, and Cybernetics: Systems_ . 

Zheng, Z.; Xie, Z.; Wang, Z.; and Hooi, B. 2025a. Monte carlo tree search for comprehensive exploration in llm-based automatic heuristic design. _arXiv preprint arXiv:2501.08603_ . 

Zheng, Z.; Xie, Z.; Wang, Z.; and Hooi, B. 2025b. Monte Carlo tree search for comprehensive exploration in LLMbased automatic heuristic design. In _Proceedings of the International Conference on Machine Learning_ . 

Zitzler, E.; and Thiele, L. 1999. Multiobjective evolutionary algorithms: A comparative case study and the strength Pareto approach. _IEEE Transactions on Evolutionary Computation_ , 3(4): 257–271. 

## **A Reproducibility Statement** 

The formulation and Markov Decision Process of multi-operator optimization are presented in Section 2 and Section C, respectively. The technical foundation of the E2OC framework is detailed in Section 3, with further explanations provided in Appendix D, and prompts are detailed in Appendix D.4. To ensure full reproducibility, all essential experimental components are documented in the supplementary material. This material includes descriptions of the different problems and operator settings (Appendix F and G), hyperparameters settings (Appendix I.3), details of the comparison methods (Appendix E and I.2), and additional results (Appendix J). In addition, the supplementary material contains source code to enable direct replication of all reported experiments. 

## **B Related Works** 

### **B.1 Automatic Heuristic Design (AHD)** 

**General AHD Method.** Automatic heuristic design, also known as hyper-heuristics (Burke et al. 2013; Stutzle and L¨ opez-´ Iba´nez 2019˜ ), aims to automatically generate, select, or adapt heuristics for complex optimization problems, reducing reliance on expert knowledge and enhancing cross-domain applicability (Burke et al. 2019; Akiba et al. 2019). 

Genetic Programming (GP)-based methods form a major paradigm within AHD (Langdon and Poli 2013). They encode heuristics as tree-structured programs or executable code and evolve high-performing rules through genetic operators such as crossover, mutation, and selection within a defined search space (Jia, Mei, and Zhang 2022; Mei et al. 2022). Genetic Programming (GP)-based AHD has been applied to domains such as production scheduling (Nguyen, Mei, and Zhang 2017; Zhang et al. 2023) and path planning (Jia, Mei, and Zhang 2022; Ardeh, Mei, and Zhang 2021), demonstrating its ability to discover complex heuristic strategies, including priority rules in scheduling and composite heuristics for combinatorial problems. 

Despite their effectiveness, these methods rely on manually designed genetic operators and fixed terminal and function sets (Pillay and Qu 2018; O’Neill et al. 2010). The resulting heuristics often have complex, hard-to-interpret structures, which limits scalability and practical applicability. 

**LLM-driven AHD.** LLMs have enabled a new paradigm for AHD, in which heuristic construction is guided by language-based generative models (Liu et al. 2026; Zhang et al. 2024a). In this setting, AHD is often formulated as an evolutionary program search, where LLMs generate and modify algorithmic code within an evolutionary optimization framework. These approaches have shown strong empirical performance in optimization (Liu et al. 2024a; Ye et al. 2024; van Stein and Back 2024¨ ; Ye et al. 2025; Dat, Doan, and Binh 2025; Yao et al. 2025; Li et al. 2025; Qiu et al. 2026), mathematical discovery (Romera-Paredes et al. 2024; Novikov et al.), black-box optimization (Ma et al. 2025; Xu et al. 2025) and machine learning (Mo et al. 2025). 

FunSearch provides a baseline by using an island-based evolutionary framework with a single prompting strategy for LLM-driven code optimization (Romera-Paredes et al. 2024). Building on this, the EoH jointly evolves heuristic ideas and executable code (Liu et al. 2024a), introducing multiple prompting strategies to enhance diversity and exploration. MEOH further incorporates dominance-based selection on objective vectors (Yao et al. 2025), enabling efficient multi-objective heuristic design within the same LLM-driven evolutionary setting. 

Beyond evolutionary approaches, alternative search paradigms have been explored. Monte Carlo Tree Search (MCTS) guides LLM-based heuristic synthesis through structured exploration (Zheng et al. 2025b; Kiet et al. 2025), while neighborhood search improves sample efficiency and local refinement (Xie et al. 2025). Collectively, these LLM-driven methods reduce dependence on manually predefined symbol sets and operate in semantically richer spaces, enabling more flexible and expressive heuristic synthesis. 

### **B.2 Operator Selection and Design in Evolutionary Algorithms** 

The effectiveness of evolutionary algorithms largely depends on the employed operators. Existing research on operator selection and design can be broadly categorized into two directions: adaptive operator selection based on search feedback, and the design of problem-informed operators that exploit domain-specific structures (Pei et al. 2025). 

**Operator Selection.** Operator selection is commonly studied as an online decision-making problem, where operator usage is adapted according to the current search state and historical performance. In many studies, this process is further formulated within the frameworks of adaptive parameter control (Huang, Li, and Yao 2019) or selection hyper-heuristics (Drake et al. 2020), in which each candidate operator is treated as an alternative parameter configuration or heuristic strategy to be selected during the evolutionary search. Methods such as adaptive large neighborhood search (Mara et al. 2022; Tang, Mei, and Yao 2009) and reinforcement learning model (d O Costa et al. 2020; Zhao, Zhou, and Wang 2023) selection as a policy mapping states to operator choices, with feedback derived from fitness gain or diversity preservation. This allows operator distributions to adapt dynamically, reducing reliance on fixed schedules or expert heuristics. 

**Operator Design.** Operator design is undergoing a transition from expert-crafted operators (Helsgaun 2000; Lan et al. 2021) tailored to specific problems and objectives toward automated design approaches. Early methods based on GP evolve operator components and compositions within predefined structural spaces (Hong et al. 2018). More recently, LLM–based approaches have demonstrated the ability to automatically generate and explore operator structures via natural language specifications or code synthesis (Liao et al. 2025), providing a more expressive and flexible design space. 

**Operator Combination in Multi-Objective EAs.** In multi-objective EAs (MOEAs), operators must balance convergence toward the Pareto front with preservation of solution diversity (Li, Gao, and Shen 2022). Single operators often bias the search toward specific regions. To mitigate this, methods combine multiple mutation or recombination operators with complementary behaviors and manage their usage through cooperative or competitive strategies (Chen et al. 2025; Li et al. 2024b). The challenge lies in designing operator sets and selection mechanisms that adapt to dynamic Pareto fronts while accounting for inter-operator interactions rather than evaluating operators in isolation. 

### **B.3 MCTS with LLM for Structured Reasoning and Decision-Making** 

Monte Carlo Tree Search (MCTS) is a simulation-based heuristic search for large, structured decision spaces, providing approximate solutions when exhaustive search is infeasible (Coulom 2007). It operates through a cycle of selection, expansion, simulation, and backpropagation, balancing exploration of uncertain paths with exploitation of promising ones (Swiechowski et al.<sup>´</sup> 2023). Beyond passive evaluation, MCTS can actively guide decision-making by coordinating with deep neural networks (Silver et al. 2016; Fu, Qiu, and Zha 2021), demonstrating effectiveness in complex spaces. 

**MCTS with LLM.** Recent work integrates MCTS with LLMs for structured reasoning and algorithm design (Zheng et al. 2025b; Kiet et al. 2025). In one approach, LLMs generate reasoning steps while MCTS evaluates and selects promising paths, as in the Tree of Thoughts framework, enabling self-correcting multi-step reasoning (Wei et al. 2022; Yao et al. 2023). In another, MCTS-AHD (Zheng et al. 2025b), LLMs produce candidate heuristic configurations and MCTS manages search via progressive expansion in large program spaces. MOTIF extends this to multi-strategy co-design, facilitating turn-based optimization between two LLM agents (Kiet et al. 2025). 

These methods combine LLMs’ generative flexibility with MCTS’s selective control. LLMs provide diverse candidate solutions, while MCTS guides efficient search through hierarchical selection and backpropagation. This integration enhances structured reasoning and offers a scalable framework for complex decision problems, transforming MCTS into a dynamic controller of LLM outputs. 

### **B.4 Reflective Prompting** 

Reflective prompting enables LLMs to iteratively generate, evaluate, and revise outputs, forming a generate-reflect-revise loop to improve quality (Shinn et al. 2023). In automated algorithm design, ReEvo embeds reflection into evolutionary search (Ye et al. 2024), allowing LLMs to compare algorithm variants and extract insights to guide subsequent search. LLM4EO applies reflective prompting in operator design to identify patterns from successful instances and enable knowledge reuse (Liao et al. 2025). By integrating reflection with optimization, these methods support multi-round self-assessment and learning from past errors, improving efficiency and generalization in complex design tasks. 

## **C Markov Decision Process for Multi-Operator Optimization** 

The interdependent multi-operator evolution process is inherently dynamic rather than a static multi-variable optimization problem. Modifying one operator changes the generation distributions of other operators, continuously reshaping the overall search landscape during evolution. This process can be formulated as a Markov Decision Process (MDP), represented by the tuple ( _S, A, P, R_ ), where the optimization proceeds iteratively over time steps _t ∈ T_ . 

**State Space.** At iteration _t_ , the state _st ∈ S_ represents the current operator combination and its associated prompt information, defined as: 



where _Oi,t_ denotes the _i_ -th operator at step _t_ , and **_P_** _t_ = ( _p_ 1 _,t, p_ 2 _,t, . . . , pK,t_ ) represents the corresponding prompt tuple, with _pi,t_ being the prompt template used for the generation of _Oi,t_ . 

**Action Space.** During the operator combination evolution, each action determines which operator _i_ should be evolved and whether its corresponding prompt should be regenerated. Let _wi ∈{_ 0 _,_ 1 _}_ denote the binary decision to rewrite the prompt _pi_ . Thus, each action _at_ = ( _i, wi_ ) specifies both the target operator and its prompt update decision. Changing a prompt directly affects the generation distribution of the LLM-based algorithm constructor _Gi_ ( _· | pi,t_ ). 

**Reward Function.** The reward function guides the evolution of the operator combination toward the optimization objective. Based on scalarized evaluation, the reward improvement at step _t_ + 1 is defined as: 



where **_O_** and **_O_**<sup>_′_</sup> represent the operator combinations before and after applying action _at_ , respectively. A positive reward indicates an improvement in the scalarized performance metric, guiding the evolutionary search toward more effective operator configurations. 

Given a total computational budget _T_ , the overall optimization objective is to maximize the expected cumulative reward: 



where _π_ ( _at | st_ ) denotes the decision policy over actions (e.g., operator selection and prompt rewriting), and **_O_** denotes the operator set and their corresponding prompts to be evolved by the prompt generator _G_ ( _· | P_ ( _·_ )). The expectation is taken over problem instances _d ∈D_ and the stochasticity introduced by the solver _S_ , the generator _G_ , and the evaluation process. This formulation captures the adaptive evolution of operator and prompt configurations within the given computational budget _T_ , aiming to maximize the cumulative improvement in scalarized multi-objective performance. 

**Transition Probability.** Given a state _st_ and an action _at_ at decision step _t_ , the generator _Gi_ ( _· | pi,t_ ) samples _q_ operator codes _{ci,_ 1 _, ci,_ 2 _, . . . , ci,q}_ . Fixing all other operators, _q_ new combinations _{s_ 1<sup>_′, s′_</sup> 2<sup>_, . . . , s′_</sup> _q_<sup>_}_are evaluated. The next state</sup><sup>_st_+1is</sup> selected according to the transition probability _P_ ( _st_ +1 _| st, at_ ), which depends on the performance of the sampled combinations. 

## **D Methodology Details** 

This section provides a comprehensive description of the algorithmic details and the prompts employed. The implementation of E2OC co-evolves design strategies and executable codes through three key stages: warm-start, progressive search, and operator rotation evolution. 

### **D.1 Warm-start** 

Before the warm-start phase, the operator combinations to be searched and the corresponding code templates (which serve as key components of the prompts for the algorithm generator) should be pre-specified to form the initial prompt tuple. Additionally, the instance set _D_ for algorithm design and the number of newly introduced prompts need to be determined. This parameters serves as input to E2OC, which then constructs an initial multi-operator set and extracts the corresponding design thoughts. 

The detailed procedure is outlined in Algorithm 1. First, an initial population is generated for each operator based on the provided prompt templates. This population is evaluated using a multi-objective evaluator composed of MOEAs and the target optimization problem. Next, a prompt generator extracts design thoughts from the higher-performing operators. It should be noted that each prompt incorporates a different design thought and a fixed structural components. Therefore, in order to make it easier for the reader to understand, this paper directly uses prompts to represent design thoughts. For each initial operator set, a specialized prompt is constructed to instruct the LLM to summarize valuable design insights from elite operators, resulting in the initial operator design prompt storage _PS_ . The multiple design thoughts belonging to different operators in PSform an interdependent language space. A progressive search strategy based on MCTS is then employed to explore design strategies within this space. 

### **D.2 Progressive Search** 

After obtaining the prompt storage _PS_ and hyperparameters such as the iteration count, the MCTS-based progressive search process is executed as outlined in Algorithm 2. The search iterates through four core phases: selection, expansion, simulation, and backpropagation. Initially, a root node _N_ 0 is selected, and a design thought from _PS_ is chosen as the initial state. It is important to note that nodes in the MCTS tree can be organized into multiple domains, with each domain representing design strategies for the same operator. Thus, a complete design strategy path is formed by concatenating design thoughts across different domains (i.e., design thoughts for different operators). During the expansion phase, a new child node is created and linked to its parent, corresponding to line 17 in the algorithm. In the simulation phase, the operator-rotation evaluation (corresponding to the OperatorRotationEvaluation in Algorithm 2) is performed only when the path length equals the total number of operators. If this condition is not met, a new design thought (i.e., prompt) is randomly sampled for temporary evaluation, corresponding to lines 21–25. Finally, the resulting fitness score _fitj_ from the evaluation is used to update the scores of the corresponding branches in the Monte Carlo tree. 

In each subsequent iteration, a new node is selected based on the scores _fit_ of the existing nodes, and the cycle of expansion, simulation, and backpropagation continues. Through continuous exploration and exploitation of the design thoughts in _PS_ , the optimal design strategy **_P_** _best_ is identified to guide the generation of multiple operators. 

### **D.3 Operator Rotation Evolution** 

For node states _Pj_ that satisfy the length requirement, operator rotation evolution is performed, as outlined in Algorithm 3. Similar to coordinate rotation strategies, the number of rotations is controlled by the Max number of middle iterations. In each iteration, the design prompt (containing design thoughts) for the corresponding operator is extracted from the design strategy, and the algorithm generator produces candidate algorithms. Notably, the algorithm generator can incorporate state-of-the-art AHD modules, implying that parameters must be customized for different algorithm design tasks. The generated operators are then evaluated by a multi-objective evaluator, where the average HV performance obtained over multiple runs of NSGA-II with the 

Algorithm 1: Warm-start for Design Thought Extraction. 1: **Input:** Initial operator combination **_O_** 1 and prompt tuple _P_ 1 at iteration step _t_ = 1; Instance set _D_ ; Number of initial added prompt _AP_ ; Candidate operator combination set _OS_ ; Number _K_ of operators to be evolved. 2: **Output:** Initial operator design prompt storage _PS_ . 3: Initialize multi-objective optimization evaluator _Eva_ ; 4: **for** _i_ = 1 _, . . . , K_ **do** 5: _pi ← Pi,_ 1; # _Pi,_ 1 _∈ P_ 1 6: Initialize algorithm generator _Gi_ ( _· | pi_ ) of _Oi_ ; 7: **for** _j_ = 1 _, . . . , ONmax_ **do** 8: _Oi,j ←Gi_ ( _· | pi_ ); 9: **_O_** 1<sup>**_′_**</sup><sup>_←_Update the operator</sup><sup>_i_in</sup><sup>**_O_**1with</sup><sup>_Oi,j_;</sup> 10: _fiti,j ← Eva_ ( _D|_ **_O_** 1<sup>**_′_**);</sup> 11: _OSi,j ←_ ( _Oi,j, fiti,j_ ); 12: **end for** 13: **end for** 14: _OS_<sup>�</sup> _←_ Sort by _fiti,j_ and filter invalid operators in _OS_ ; 15: Initialize prompt storage _PS_ ; 16: **for** _i_ = 1 _, . . . , K_ **do** 17: _ONi ←_ select the the smaller of _AP_ and _OS_<sup>�</sup> _i_ ; 18: _PSi,_ 1 _← Pi,_ 1; 19: **for** _g_ = 1 _, . . . , ONi −_ 1 **do** 20: _Oi,g_ +1 _← OS_<sup>�</sup> _i,g_ ; 21: Initialize prompt generator _P_ ( _· | Oi,g_ +1) of _Oi_ ; 22: _PSi,g_ +1 _←P_ ( _· | Oi,g_ +1); 23: **end for** 24: **end for** 

integrated operators serves as the fitness score. If a superior operator is found, it replaces the original operator in the combination, and the process continues to optimize the next operator. Through repeated iterations, multiple operators are rapidly rotated and evaluated, thereby obtaining scores for the design strategy. These scores are used to update the branching information between nodes in the search tree. 

### **D.4 Prompt Engineering** 

The prompts used in E2OC are for algorithm and prompt generation. During algorithm generation, E2OC adopts heuristic prompting strategies consistent with those used in existing single-heuristic design methods. For example, EoH employs evolution prompts including Exploration prompts (E1, E2) and Modification prompts (M1, M2, M3) (Liu et al. 2024a), while MCTS-AHD uses prompts such as i1, e1, e2, m1, m2, and s1 for MCTS initialization and tree expansion (Zheng et al. 2025b). Other baseline methods similarly follow the prompt strategies specified in their original studies (Romera-Paredes et al. 2024; Yao et al. 2025; Ye et al. 2024). 

When constructing the language space of design strategies, dedicated prompts are used to analyze existing design thoughts and reformulate them, as illustrated in Figure 4. To ensure compatibility across different algorithm design frameworks, design strategies are embedded into structured algorithm-parameter description blocks, corresponding to the improvement suggestions shown in the figure. These prompts typically include three components. First, **Elite Candidate Operator** (new ~~a~~ lg) obtained from the warm-start phase are provided as reference targets. Second, an **Expert-designed Operator** (ini ~~t~~ emplate) designed by domain experts is supplied to ground the design process. Third, an Output Femplate (output ~~t~~ emplate) is specified to standardize the format of the LLM responses. As highlighted in the improvement suggestion task description in Figure 4, the LLM is guided to analyze the strengths and weaknesses of the reference algorithm. The model then produces a revised algorithm template augmented with explicit improvement suggestions. Each such template represents a distinct design strategy and is subsequently incorporated into the prompt strategies of different algorithm design frameworks for downstream use. 

## **E Different MCTS variants** 

From the perspective of multi-variable optimization, the application of MCTS to multi-operator co-design can be categorized into four types based on state representation and expansion mechanisms, as illustrated in Figure 5. 

- **Progressive multi-operator search** , where each node represents a single operator. The final operator set is obtained by selecting the highest-scoring path whose depth equals the total number of operators. During expansion, an algorithm generator is invoked to generate new operators as child nodes. 

Algorithm 2: Progressive Search for Design Strategy. 1: **Input:** Max number of outer iterations _Nouter_ ; Number of operators to be evolved _K_ ; Operator design prompt storage _PS_ ; Storage of operator combination **_SO_** . 2: **Output:** Top scoring operator combination **_O_** _best_ and prompt combination **_P_** _best_ . 3: _N_ 0 _←_ root node (empty state); 4: **for** _j_ = 1 _, . . . , Nouter_ **do** 5: _# Selection_ 6: _Nj ←N_ 0; 7: **while** _Nj_ has child node **do** 8: _NS ←_ get the child node set of _Nj_ ; 9: _Nj ←_ select the node of highest UCB score in _NS_ ; 10: **end while** 11: _# Expansion_ 12: _i ←_ the size of state in _Nj_ ; 13: _staj ←_ get the state of _Nj_ ; 14: **if** _i<_ **then** 15: **for** _pg ∈ PSi_ **do** 16: _stag ← staj_ + [ _pg_ ]; 17: Add a new child node _N_<sup>_′_</sup> of _Nj_ with state _stag_ ; 18: **end for** 19: **end if** 20: _# Simulation_ 21: **while** _i<K_ **do** 22: _pi ←_ random sampling a prompt in _PSi_ ; 23: _staj ← staj_ + [ _pi_ ]; 24: update the new state _staj_ of _Nj_ ; 25: **end while** 26: **_P_** _j ←_ get the prompt storage of _staj_ ; 27: ( **_SO_** _j, fitj_ ) _←_ get the operator combination and score of _Nj_ by OperatorRotationEvaluation( **_P_** _j_ ); 28: _# Backpropagation_ 29: _Np ←Nj_ ; 30: **while** If the node _Np_ exists **do** 31: _scoj ← scoj_ + _fitj_ ; _# Default node score is 0._ 32: _vsj ← vsj_ + 1; _# Default visit count is 0._ 33: _Np ←_ get the parent node of _Nj_ ; 34: **end while** 35: **end for** 36: **_O_** _best ←_ get the highest score combination in **_SO_** ; 37: **_P_** _best ←_ get the state of the highest scoring node; 

- **Progressive design strategy search with tuple states** , where each node represents a tuple of design rationales across operators. Expansion is performed by randomly modifying one element of the tuple, yielding a new candidate strategy. The highest-scoring tuple is then used for multi-operator design. 

- **Progressive sampling and search of design thoughts** , where each node corresponds to a design thought for a single operator. During expansion, the LLM is queried to generate new thoughts for the target operator, and the highest-scoring root-to-leaf path defines the final design strategy. 

- **Progressive design strategy search with warm-start** , corresponding to E2OC, where nodes represent individual design thoughts but the thought space at each depth is predefined during the warm-start phase and does not grow dynamically during expansion. 

All four variants are capable of supporting collaborative multi-operator design. However, for thought-based search strategies (b–d in Figure 5), an additional operator design stage is required once a complete design strategy has been identified. A comparison and analysis of these variants can be found in Seciton 5.1. 

Algorithm 3: Operator Rotation Evolution Mechanism. 

- 1: **Input:** Max number of middle iterations _Nmiddle_ ; Number of operators to be evolved _K_ ; Operator design prompt tuple **_P_** ; Instance set _D_ ; Initial operator combination **_O_** 1. 



<!-- Start of picture text -->
2: Output:  The ( BO , fit ) of the highest fitness.<br>3: Initialize evaluator of multi-objective optimization  Eva ;<br>4: fit ← Eva ( D| O 1);<br>5: BO ← O 1;<br>6: for  k = 1 , . . . , Nmiddle  do<br>7: for  i  = 1 , . . . , K do<br>8: pi ← get the prompt of operator  i  in  P  ;<br>9: OSi ← generate operators set by  Gi ( · | pi );<br>10: Oi ′ ← get the highest fitness operator in  OSi ;<br>11: O ′ ← update  i -operator with  Oi ′ ;<br>12: fit ′ ← Eva ( D| O ′ );<br>13: if  fit ′ ≥ fit  then<br>14: fit ← fit ′ ;<br>15: BO ← O ′ ;<br>16: end if<br>17: end for<br>18: end for<br><!-- End of picture text -->

## **F Multi-Objective Flexible Job Shop Scheduling Problem** 

### **F.1 Problem Description** 

The FJSP extends the classical job shop scheduling problem by allowing each operation to be processed on multiple eligible machines with varying processing times. In multi-objective FJSPs, the objectives typically include minimizing the makespan, the maximum machine load, and the total machine load, which reflect distinct and often conflicting performance criteria. While makespan measures the completion time of the last job, maximum machine load emphasizes the balance of heavily loaded machines, and total load captures overall resource utilization. In the Bi-FJSP, we focus on makespan and maximum machine load, whereas the Tri-FJSP additionally considers total machine load. The conflicting nature of these objectives complicates scheduling, as improvements in one criterion may degrade others. 

To tackle these challenges, MOEAs are commonly employed, leveraging sophisticated operator designs for both operation sequencing and machine assignment. Designing effective operators is particularly demanding due to the combinatorial complexity, the interdependence between operations and machines, and the need to balance exploration and exploitation across objectives. The benchmark instances proposed by Brandimarte provide a standard testing platform for evaluating algorithm performance (Brandimarte 1993). The combination of multiple objectives, practical constraints, and operator design complexity makes two- and three-objective FJSP a highly challenging setting for advanced multi-objective optimization methods. 

### **F.2 Operator Implementation Details** 

The MOEAs used to solve the multi-objective FJSP employ four operators to explore the solution space within the two-part encoding, as shown in Figure 6. Two operators target operation sequencing, performing crossover and mutation on the first part of the encoding to optimize the order of operations across jobs. The other two operators focus on machine assignment, applying crossover and mutation to the second part to refine machine selection for each operation. Each operator addresses specific optimization tasks within its respective encoding segment and is designed according to its functional requirements. 

These operators exhibit interdependencies, as modifications in operation sequencing affect the performance of machine assignment, and vice versa. Designing these operators independently often leads to suboptimal performance, since improvements achieved by one operator may be offset or invalidated by another. The complex couplings among operators make it difficult to achieve balanced exploration and exploitation across multiple objectives while maintaining feasibility. Consequently, effective multi-operator evolutionary algorithm design requires mechanisms that consider operator interactions and enable their coordinated evolution to ensure consistent and robust performance in both two- and three-objective FJSP scenarios. 

## **G Multi-Objective Traveling Salesman Problem** 

### **G.1 Problem Description** 

The Traveling Salesman Problem (TSP) is a classical combinatorial optimization problem, where a salesman must visit a set of cities exactly once and return to the starting point, minimizing the total travel distance. In multi-objective TSPs, the objectives are typically derived by applying different weights to the distance, allowing the formulation of two- or three-objective problems that reflect trade-offs among alternative optimization criteria. While the specific objectives may vary, they are inherently conflicting, 



<!-- Start of picture text -->
Prompt for thought extraction and prompt rewriting<br> ∙<br>You are an AI Python expert specializing in multi-objective optimization algorithms.<br>Your task is to refine the provided prompt template to generate more advanced and<br>robust Python implementations.<br>Elite<br>Reference Algorithm (Analyze its strengths for inspiration):​ <new_alg> Candidate Operator AI-A<br>Original Template to Improve:​ Expert- Analysis and<br><Ini_template> designed  rewriting<br>operator<br>Code templates with design thought<br>Refinement Requirements:​<br>1. Return a complete, runnable Python function​ including: import <required_libraries><br>     - All necessary import statements.<br>     - Preserved function name, input parameters (with type hints), and return type. def <function_name>(<parameter>: <type>) -> <return_type>:<br>    """<br>     - Full function body implementation.<br><Function description><br>2. Strictly adhere to PEP 8 guidelines: Args:<br>     - Correct any syntax errors in the original template         <param_name> (<type>): <parameter_description><br>Improvement Suggestions:<br>3. Enhance the docstring by adding an "Improvement Suggestions"​. Add 2-3<br>        - <Suggestion 1 based on reference algorithm><br>specific recommendations from the following perspectives:         - <Suggestion 2 for HV optimization><br>     - Leverage strengths of the reference algorithm. Design<br>     - Focus on Hypervolume (HV) optimization strategies. Returns: thought<br>        <return_type>: <return_description><br>    """<br>Output Format:​<br># <Implemented function body><br>Return ONLY the final refined template as a single string, structured as follows: return <result><br><Output_template><br><!-- End of picture text -->

Figure 4: Prompt for design thought analysis and prompt rewriting. 

as improvements along one weighted distance can lead to deteriorations in others. Benchmark instances from publicly available datasets, such as TSPLIB, are commonly used to evaluate the performance of MOEAs in this context. 

### **G.2 Operator Implementation Details** 

To explore the solution space of multi-objective TSPs, MOEAs employ multiple domain-specific search operators that act on the same path representation, as shown in Figure 7. These operators, including crossover and mutation variants, have overlapping functionalities but differ in the manner and scope of exploration. Each operator is designed to improve certain aspects of the tour, such as segment reordering, edge exchange, or route inversion. Despite acting on the same encoding region, the operators are interdependent: the effect of one operator may enhance or interfere with the effect of another. This overlapping and mutually influencing behavior makes independent design of operators insufficient and may result in suboptimal performance if interactions are ignored. Effectively coordinating these operators to balance exploration and exploitation across multiple objectives remains a significant challenge in multi-operator evolutionary algorithm design. 

## **H Metric Definition** 

To evaluate the effectiveness of the proposed MOEAs, this study primarily employs two widely accepted performance metrics, hypervolume (HV) and inverted generational distance (IGD). Higher HV values and lower IGD values indicate better overall convergence and diversity performance. These metrics jointly assess the convergence and diversity of the obtained Pareto fronts, providing a comprehensive measure of algorithm performance in multi-objective optimization tasks. The following sections provide detailed definitions and formulations of HV and IGD. 

### **H.1 HV** 

Hypervolume is a widely used performance metric in multi-objective optimization that measures the volume of the objective space dominated by the obtained Pareto front relative to a reference point. A larger hypervolume indicates better convergence and diversity of solutions. In this study, the reference point _r_ is manually set to ensure it dominates all obtained solutions. Formally, given a set of Pareto-optimal solutions _P_ = _{p_ 1 _, p_ 2 _, . . . , pn}_ , the hypervolume is defined as 



where [ _p, r_ ] denotes the hyper-rectangle spanned by solution _p_ and the reference point _r_ , and vol( _·_ ) represents the Lebesgue measure in the corresponding objective space. 



<!-- Start of picture text -->
Progressive multi- Progressive design strategy  Progressive sampling and  Progressive design strategy<br>operator search search with tuple states search of design thoughts search with warm up<br>O 1-1 ( p 1-0,  p 2-0,  p 3-0,  p 4-0) P 1-1 P 1-1<br>O 1 P 1 P 1<br>Generate<br>O 2-2 AI-A thoughts P 2-1 P 2-2 P 2-1 P 2-2<br>O 2 P 2 P 2<br>( p 1-0,  p 2-0 ,  p 3-0,  p 4-0)<br>O 3 O 3-1 O 3-2 … P 3 P 3-1 P 3 P 3-1<br>Randomly select<br>O 4-1 Design  P 4-1 Generate  P 4-1<br>O 4 operator ( p 1-0,  p 2-0,  p 3-0,  p 4-0 ) P 4 AI-A thoughts P 4<br>highest score highest score highest score highest score<br>Evaluation Design  & Evaluation Design  & Evaluation Design  & Evaluation<br>(a) (b) (c) (d)<br>AI-S<br><!-- End of picture text -->

Figure 5: Different MCTS variants for multi-operator design. 

|0.1<br>Priorit|0.4<br>0.6<br>**operatio**<br>y of operation|0.2<br>0.3<br>**n crossove**|0.4<br>**r ope**|0.8<br>**rator**|0.2|1<br>3<br>1<br>**machin**<br>Machine index|4<br>2<br>**e crossover**|5<br>2<br>1<br>**operator**<br>_Machine_<br>_assignment_|
|---|---|---|---|---|---|---|---|---|
|_Op_<br>_sequ_|_eration_<br>_encing_||||||||
||**operatio**|**n mutation**|**ope**|**rator**||**machin**|**e mutation**|**operator**|



Figure 6: Encoding representation and operators in FJSP. 

### **H.2 IGD** 

Inverted generational distance evaluates both convergence and diversity of an obtained Pareto front by measuring its average distance to a reference Pareto front. In this study, the reference Pareto front _P_<sup>_∗_</sup> = _{p_ 1<sup>_∗, p∗_</sup> 2<sup>_, . . . , p∗_</sup> _m_<sup>_}_is constructed from the</sup> union of non-dominated solutions obtained by all compared algorithms to approximate the true Pareto front. Given an obtained solution set _P_ = _{p_ 1 _, p_ 2 _, . . . , pn}_ , the IGD is computed as 



where _d_ ( _p, p_<sup>_∗_</sup> ) is the Euclidean distance between solution _p_ and reference solution _p_<sup>_∗_</sup> in the objective space. Lower IGD values indicate that the obtained solutions are closer to and more uniformly distributed along the reference Pareto front. 

### **H.3 RI** 

The Relative Improvement (RI) metric quantifies the percentage improvement of a new method’s performance relative to a baseline method. It is calculated using the formula: 



where _A_ represents the performance value of the new method and _B_ represents the performance value of the baseline method. 

## **I Experiment Design and Implementation Detail** 

### **I.1 Experimental Design.** 

The proposed E2OC is used to co-design multi-operators in MOEAs, which reduces manual design effort and enhances algorithmic performance. The key research questions are as follows: (1) Can automatically designed operator combinations outperform expert-designed counterparts? (2) Can high efficiency be maintained across additional objectives and diverse problem instances? (3) Does E2OC exhibit superior performance compared to advanced methods that evolve operators independently? (4) Is E2OC more efficient than alternative multi-operator design strategies? (5) Does the approach possess potential for continuous optimization? (6) Are all constituent modules of E2OC effective? 



<!-- Start of picture text -->
Neighborhood search operator combination<br>5 3 6 4 7 1 2 8<br>Path<br>City index Representation<br><!-- End of picture text -->

Figure 7: Encoding representation and operators in TSP. 

To rigorously address these questions, the following experiments are designed: (1) comparison with state-of-the-art multiobjective evolutionary algorithms on bi-objective and tri-objective FJSP and TSP; (2) comparison with recent single-heuristic automatic design methods; (3) evaluation against different multi-operator design strategies; (4) evaluate the potential for continuous optimization of E2OC across multiple iterations; (5) analysis of performance and computational cost under varying LLMs and key parameter _AP_ (Number of initial added prompt); (6) ablation studies. Moreover, in order to observe the improvement brought by the designed operator combinations over the classical operators, We compare them on several MOEAs and analyze the effect of different combinations and orders of classical operators on optimization performance. 

### **I.2 Comparison Method Detail** 

In addition to recent SOTA single-heuristic design methods, this study compares E2OC with a range of multi-heuristic design frameworks. These methods can be categorized along three dimensions, namely whether algorithmic thoughts are explicitly incorporated, whether prompt rewriting is employed, and whether a warm-start phase is required, as summarized in Table 6. Single-heuristic methods focus on designing a single algorithm and therefore do not rely on warm-start mechanisms to balance exploration and exploitation across multiple design tasks. 

Table 6: Comparison of different methods on ideas inclusion, prompt rewriting, and warm-start 

|**Type**|**Methods**|**Thoughts**|**Prompts**|**Warm-start**|
|---|---|---|---|---|
|tic|Random|✗|✗|✗|
|ris|FunSearch|✗|✗|✗|
|heu|EoH|✓|✗|✗|
|le-|MEoH|✓|✗|✗|
|ng|ReEvo|✗|✓|✗|
|Si|MCTS-AHD|✓|✗|✗|
||CD|✓|✗|✗|
|tic|UCB|✓|✗|✓|
|ris|Win-UCB|✓|✓|✓|
|eu|LLM|✓|✓|✗|
|ti-h|MCTS<br>~~O~~C|✓|✗|✗|
|ul|MCTS<br>~~T~~uple|✓|✓|✓|
|M|MCTS<br>~~S~~ampling|✓|✓|✓|
||E2OC|✓|✓|✓|



In this context, an _idea_ is defined as a language description that represents the high-level logic of a heuristic (Liu et al. 2024a). Methods such as EoH (Liu et al. 2024a), MEOH (Yao et al. 2025), and MCTS-AHD (Zheng et al. 2025b) manage ideas together with executable code as part of the population archive. Among the compared approaches, only ReEvo explicitly incorporates prompt rewriting. Empirical evidence suggests that dynamic prompt adjustment is effective in reducing code generation errors and improving the quality of generated algorithms. 

Existing LLM-based collaborative algorithm design frameworks can be categorized according to how they formulate the multi-heuristic design task and organize decision-making over interacting algorithms. From this perspective, prior studies can be broadly divided into four classes: coordinate-descent (CD)-based (Wright 2015), upper-confidence-bound(UCB)-based (Garivier and Capp´e 2011; Gupta et al. 2021), MCTS-based (Zheng et al. 2025b; Kiet et al. 2025), and LLM-driven approaches. 

Coordinate-descent-based methods formulate multi-heuristic collaboration as a deterministic continuous optimization problem over the algorithm space (Wright 2015). Multiple algorithms are optimized in a rotational manner, where one algorithm is updated while others are fixed, and the process iterates to identify high-performing combinations, corresponding to **CD** in Table 6. These methods emphasize structured and controllable search dynamics and are most effective when inter-heuristic interactions are relatively stable. 

UCB-based methods model collaborative algorithm design as a stochastic decision-making problem (Garivier and Cappe´ 2011), typically using a multi-armed bandit formulation. Each algorithm or operator is treated as an arm with an unknown reward 

distribution, and the search explicitly balances exploration and exploitation **UCB** , corresponding to in Table 6. When LLMgenerated prompts are introduced, reward distributions may shift over time, complicating estimation. Moreover, dependencies among algorithms often motivate extensions to combinatorial bandit settings (Gupta et al. 2021), where window-constrained UCB strategies are used to adapt to non-stationary environments, corresponding to **Win-UCB** in Table 6. 

MCTS-based methods cast multi-heuristic design as a sequential decision-making process, in which each design action influences subsequent states. A search tree is incrementally constructed to encode historical design trajectories, enabling a principled trade-off between exploration and exploitation. To control search complexity and handle non-stationary feedback, practical implementations commonly restrict search horizons or limit tree depth. This paradigm has been applied to both single-heuristic design and collaborative search over algorithm combinations or design strategies, corresponding to **MCTS-OC, MCTS-Tuple and MCTS-Sampling** in Table 6. 

Finally, fully LLM-driven approaches dispense with explicit search heuristics and rely on structured prompts to enable LLMs to autonomously perform operator selection, algorithm composition, and resource allocation. These methods exploit high-level semantic reasoning to dynamically adjust collaborative optimization strategies, offering greater flexibility at the cost of reduced explicit control, corresponding to **LLM** in Table 6. 

Notably, most multi-heuristic design frameworks treat single-heuristic design methods as modular building blocks. In this study, EoH is adopted as the foundational single-heuristic design module across all compared frameworks, with explicit management of algorithm thoughts. Among these frameworks, UCB-based methods and those constructing explicit design spaces typically require a warm-start phase for initialization. 

### **I.3 Other Parameter Settings** 

In the offline design phase, the deepseek-chat model is selected based on quality-cost performance, and all model temperature values default to 1. The proposed E2OC can be divided into four components: the outer MCTS, the middle operator rotation and the inner algorithm generator and evaluator, with hyperparameter settings specifically shown in Table 7. The offline evaluators are used to rapidly assess newly designed operators and are configured with half of the computational budget used in online evaluations. 

Specifically, for the FJSP, the offline setting uses 15 iterations and a population size of 50, while for the TSP it uses 100 iterations and a population size of 100. Both problems are evaluated three times in the offline stage to achieve a rapid assessment. 

The online evaluation settings follow established practices in prior studies. For the FJSP, 30 iterations and a population size of 200 are used. For the TSP, 200 iterations and a population size of 200 are adopted, with five independent runs conducted for each configuration. The mean performance over all runs is reported as the final performance of each multi-objective optimization algorithm. 

Table 7: Overview of hyperparameters used in E2OC on Bi-FJSP. The values of the parameters with * are defined by the experiment, all others are default values. 

|**Type**|**Component**|**Hyperparameters**|**Value**|
|---|---|---|---|
||LLM|Model|**deepseek-chat***<br>|
|||Temperature|1.0|
||MCTS|Outer iteration|30|
|||Number of initial operator|4|
|**le**||Number of initial added prompt|**3***|
|**flin**|Operator Rotation|Middle iteration|5|
|**Ofl**|Generator|Inner iteration|10|
|**l**||Operator population size|10|
|||Max sampling number|25|
||Evaluator|Iteration|FJSP-15, TSP-30|
|||Solution population size<br>Number of validations|FJSP-50, TSP-100<br>3|
|**ne**|Evaluation|Iteration|FJSP-30, BiTSP-200,TriTSP-100|
|**Onli**||Solution population size<br>Number of validations|FJSP-100, TSP-200<br>5|



### **I.4 Resource Consumption** 

The authors of ReEvo (Ye et al. 2024) argued that efficiency benchmarking for LLM-EPS methods should focus on the number of fitness evaluations rather than the number of LLM calls. Similarly, MCTS-AHD, as the most recent LLM-based AHD method at the time of its submission, also follows this benchmarking protocol (Zheng et al. 2025b). Accordingly, in this study, the performance of different methods is compared by controlling for a similar number of fitness evaluations, ensuring consistency in assessment. 

The key algorithmic parameters of E2OC for solving FJSP are summarized in Table 7, including the outer-layer MCTS configuration, the number of operator-rotation iterations, as well as parameters related to the algorithm generator and the evaluator. Each newly designed operator combination is repeatedly embedded into MOEAs for optimization, and its performance is assessed by averaging the resulting HV or IGD values. The overall multi-heuristic design process of E2OC is realized through iterative interactions between the algorithm generator and the prompt generator. 

(13) 

The number of evaluations required for algorithm design equals the number of generated algorithms and is given by 

( _iter_ out + 1) _× iter_ mid _× K × sam_ max _._ 

Here, _iter_ out + 1 denotes the sum of the warm-start stage and the outer MCTS iterations, _iter_ mid represents the number of operator-rotation steps, and _sam_ max is the maximum number of newly generated algorithms accumulated by the internal algorithm generator. The algorithm generator supports different design modules, such as EoH and ReEvo. To eliminate the influence of heterogeneous population selection mechanisms across different generators, _sam_ max is used as a unified upper bound on the number of algorithms generated per design task, while the remaining parameters follow the settings reported in the corresponding literature. 

Compared with other methods, E2OC additionally relies on the prompt generator to construct the design strategy space for operator combinations, which incurs _K × AP_ calls to the LLM interface. 

### **I.5 MOEAs Parameter Settings** 

Directly applying newly designed operator combinations in MOEAs to optimize MCOPs does not yield reliable quantitative performance. Instead, as shown in Table 7 regarding the number of verifications, multiple validations are required, and performance must be assessed based on the aggregated results of these repeated evaluations, which incurs higher computational costs. 

In this study, three classical multi-objective evolutionary algorithms (MOEAs) are employed as baseline methods: NSGAII (Deb et al. 2002), NSGA-III (Deb and Jain 2014), and MOEA/D (Qingfu Zhang and Hui Li 2007). The key parameter settings are summarized below, serving as default values for all benchmark experiments. These settings can be adjusted according to problem scale and complexity. 

- **NSGA-II and NSGA-III:** For Bi-FJSP and Tri-FJSP, the population size is set to 100 with a maximum of 250 generations. For Bi-TSP and Tri-TSP, the population size and maximum generations are set to 100 and 250, respectively. 

- **MOEA/D:** The population size is set to 150, with a maximum of 200 generations. The neighborhood size is 20, and the probability of selecting individuals from the neighborhood is 0.9. 

All algorithms employ the same initial neighborhood operators. For FJSP, Simulated Binary Crossover (SBX) and polynomial mutation are used with consistent crossover and mutation probabilities. For TSP, the local search operators OR-Opt, 2-Opt, and 3-Opt are applied. Reference points are set identically across all benchmark instances. These parameter settings ensure a reasonable balance between exploration and exploitation across all MOEAs while maintaining consistency for fair comparisons in benchmark evaluations. 

### **I.6 Implementation of different AHD methods** 

To ensure a fair and consistent comparison with existing LLM-based automated algorithm design methods, we normalize the computational budget across all competing approaches using a unified algorithm evaluation resources. 

**Single-heuristic Design Methods.** When comparing against single-heuristic design methods, the multi-heuristic design problem is decomposed into a sequence of independent single-heuristic design tasks. The total evaluation budget is fixed and evenly distributed across these sub-tasks. For EoH, the population size is set to 20, consistent with the original implementation, while the algorithm terminates upon reaching a predefined maximum number of sampled candidates rather than a fixed number of generations. ReEvo explicitly constrains the number of newly constructed prompts. To ensure comparability, this limit is set to _K × AP_ , matching the prompt budget used in E2OC. All remaining baseline methods adopt the parameter settings recommended in their respective studies and are likewise terminated based on the maximum number of sampled designs. 

**Multi-heuristic Design Methods.** For the comparison with multi-heuristic design frameworks, we still use the same total evaluation budget. To accurately compare the performance of different multi-heuristic search frameworks, we ensure that the evaluation resources for each operator design task are consistent and that all evaluations are performed on EoH. Specifically, the maximum number of evaluations allocated to a single algorithm design task within one decision round is fixed and defined as a _standard design resource_ . This definition enables a principled comparison across frameworks with fundamentally different control structures. 

In CD framework, the number of rotation iterations determines how many times algorithms are optimized in an alternating manner. Within each rotation, operators are designed sequentially, and the design of one operator consumes exactly one standard design resource. Accordingly, the total number of rotation steps is set to ( _iterout_ + 1) _× itermid_ , which aligns the overall resource usage with that of E2OC. 

UCB-based framework do not follow a predetermined design order but instead dynamically select algorithms based on estimated utility. Under the unified resource definition, the total number of available standard design resource is set to ( _iterout_ + 1) _× itermid × K_ , reflecting the additional flexibility introduced by operator-level selection. 

Among the MCTS-based variants, MCTS ~~O~~ C does not perform explicit search over design strategy spaces. As a result, its effective outer-loop iteration count is set to ( _iterout_ + 1) _× itermid × K_ , where each tree node corresponds to one standard 

design resource. In contrast, MCTS-Tuple and MCTS-Fixing explicitly explore strategy-level decision spaces and therefore adopt the same parameter settings as E2OC. 

It is worth noting that the parameter settings of the LLM-based AHD methods are consistent with those of UCB-related methods. Under these unified resource allocation rules, all methods are evaluated with an equivalent number of standard design resources, ensuring that observed performance differences can be attributed to the quality of the multi-heuristic search mechanisms rather than disparities in evaluation budgets. 

## **J Additional Experiment Results** 

### **J.1 More Visualization Results** 

This section supplements the visualization results of the experiments. Comparisons with the convergence processes and PF of classical operators in different MOEAs, different AHD methods, and different MCTS variants methods in training and testing instances are included. 

**Comparison with Expert Design Operators.** The experimental performance of the multi-operator designed by E2OC compared with classic operator combinations across different MOEAs is shown in Table 1. E2OC builds upon existing expert operators (serving as the initial operator combination) to further customize and design superior operator combinations for different methods. The HV, IGD convergence process, and PF for different methods on Bi-FJSP and Tri-TSP in this experiment are illustrated in Figure 8 and 9. 

In the Bi-FJSP experiments, it can be observed that, except for the training instance mk15, the operators designed by E2OC continue to perform remarkably well in the other two similar instances in Figure 8. In terms of the PF, the operator combinations designed by E2OC achieve greater diversity, which fully demonstrates their superior performance and generalization capability. 

In the Tri-TSP experiments, all methods achieve relatively similar performance within 100 iterations on the 100-node training set. However, it is also evident from the PF that the operator combinations designed by E2OC (represented by the blue-green point set) exhibit significantly greater diversity and occupy a superior region in Figure 9. The improvement is particularly notable in small-scale scenarios, where both the HV convergence curves and PF distributions clearly outperform the initial operators designed by human experts. 

**Comparison with AHD Methods.** Experimental results are summarized in Table 6, while Fig. 10 illustrates the convergence trends of HV and IGD, as well as the final PF obtained by different AHD methods on both training and testing instances. It is worth noting that the evaluation phase is conducted on both the training set and the test set, where a larger population size and more iterations are used than in the design phase. In Bi-FJSP, the testing instance is selected to evaluate the algorithms on mk13 or mk14, which have larger number of processes and devices. All operator designs are executed 5 independent runs in NSGA-II, and performance is reported as the average over these runs. The PF shown in the figure corresponds to the run that finds the most non-dominated solutions out of the five repeated runs. 

The results reveal that LLM-based multi-operator co-search methods achieve relatively good performance on training data, but their performance degrades sharply on testing instances. It converts decision information, such as the historical performance characteristics of different operators, into language descriptions and rely directly on the LLM to make operator-search decisions. Although prolonged iteration can lead to strong training-set performance, such approaches struggle to maintain effectiveness in new scenarios. 

In addition to a multi-operator codesign framework that allows dynamic modification of prompts, such as Win-UCB and E2OC, classical AHD methods yield similar outcomes on both training and testing instances under the same evaluation budget, which indicates their tendency to converge toward local optima in algorithm design. By adjusting its prompts, Win-UCB achieves the second-best HV performance on the training set. This result shows that modifying prompts and design thoughts during the search process can help escape local optima and lead to better-performing algorithms. 

E2OC achieves the best performance on both training and testing instances, confirming that constructing a prior design-knowledge surface and performing local search at the higher strategic domain is more effective than operating under a fixed algorithmic generation distribution(fixed prompts or code templates). Furthermore, the optimization performance of E2OC on new instances is significantly better than that of other methods. 

**Comparison with Different Methods of MCTS variants.** The experimental results of different MCTS variants are summarized in Table 5. Fig. 11 further illustrates the convergence trends of HV and IGD as well as the final Pareto front (PF) obtained by these methods on both training and testing instances. The plotting settings follow those described in Section J.1. 

The results show that MCTS ~~O~~ C, which directly searches operator combinations, performs poorly. This suggests that under fixed prompts or code templates, the algorithm is prone to converge to local optima, with limited ability to break through the existing generation distribution. MCTS ~~T~~ uple and MCTS ~~S~~ ample differ in their node-state representations, but both allow unrestricted dynamic sampling of new design thoughts. While MCTS ~~T~~ uple achieves better performance on the training set, the unrestricted sampling continuously updates branch information in the Monte Carlo tree, making it difficult to identify superior combinations within a limited evaluation budget. In contrast, E2OC consistently delivers superior performance, indicating that progressive search over a warm-start-constructed local design space is more effective. 



<!-- Start of picture text -->
HV (mean ± CI) Pareto Front (best run per method) IGD (mean ± CI)<br>0.24 5200<br>2.00<br>0.22 5100 1.75<br>5000 1.50<br>0.20<br>4900 1.25<br>0.18<br>4800 1.00<br>0.16 4700 0.75<br>0.14 4600 0.50<br>4500 0.25<br>0.12<br>0 4 8 12 16 20 24 28 500 600 700 800 900 0 4 8 12 16 20 24 28<br>Generation obj1 Generation<br>(a) HV of Bi-FJSP(mk15) (b) PF of Bi-FJSP(mk15) (c) IGD of Bi-FJSP(mk15)<br>IGD (mean ± CI)<br>HV (mean ± CI)<br>Pareto Front (best run per method) 3.5<br>0.18 5250<br>3.0<br>0.17<br>5200 2.5<br>0.16<br>0.15 2.0<br>5150<br>0.14 1.5<br>0.13 5100 1.0<br>0.12<br>0.5<br>0.11 5050<br>0.0<br>0 4 8 12 16 20 24 28 700 800 900 1000 1100 1200 1300 0 4 8 12 16 20 24 28<br>Generation obj1 Generation<br>(d) HV of Bi-FJSP(mk14) (e) PF of Bi-FJSP(mk14) (f) IGD of Bi-FJSP(mk14)<br>IGD (mean ± CI)<br>HV (mean ± CI) Pareto Front (best run per method)<br>0.26<br>4400 2.5<br>0.24<br>4300<br>2.0<br>0.22<br>4200<br>0.20 1.5<br>4100<br>0.18<br>4000 1.0<br>0.16<br>3900<br>0.5<br>0.14<br>3800<br>0.12 0.0<br>0 4 8 12 16 20 24 28 500 600 700 800 900 1000 0 4 8 12 16 20 24 28<br>Generation obj1 Generation<br>(g) HV of Bi-FJSP(mk13) (h) PF of Bi-FJSP(mk13) (i) IDG of Bi-FJSP(mk13)<br>NSGA2 NSGA3 MOEAD<br>NSGA2_E2OC NSGA3_E2OC MOEAD_E2OC<br>HV obj2 IGD<br>HV obj2 IGD<br>HV obj2 IGD<br><!-- End of picture text -->

Figure 8: HV, IDG and PF performance of different operators in MOEAs on Bi-FJSP. 



<!-- Start of picture text -->
Pareto Front (best run per method)<br>IGD (mean ± CI)<br>HV (mean ± CI)<br>0.09 0.6<br>0.08 30<br>35 0.5<br>0.07<br>40<br>0.06 45 0.4<br>50<br>0.05 55 0.3<br>60<br>0.04<br>0.03 35 0.2<br>40<br>0.02 55 50 45 5045obj2 0.1<br>40 55<br>0 15 30 45 60 75 90 obj1 35 0 15 30 45 60 75 90<br>Generation 30 Generation<br>(a) HV of Tri-TSP100 (b) PF of Tri-TSP100 (c) IGD of Tri-TSP100<br>Pareto Front (best run per method)<br>IGD (mean ± CI)<br>HV (mean ± CI)<br>0.18<br>0.5<br>0.16<br>15<br>0.14 0.4<br>20<br>0.12<br>25 0.3<br>0.10<br>30<br>0.2<br>0.08<br>12.5<br>15.0<br>0.06 17.5 0.1<br>30 20.0<br>25 22.5 obj2<br>0 15 30 45 60 75 90 20 25.0 0 15 30 45 60 75 90<br>Generation obj1 15 27.5 Generation<br>(d) HV of Tri-TSP50 (e) PF of Tri-TSP50 (f) IGD of Tri-TSP50<br>Pareto Front (best run per method)<br>IGD (mean ± CI)<br>HV (mean ± CI)<br>0.45<br>0.6<br>4<br>0.40 6 0.5<br>8 0.4<br>0.35<br>10<br>0.3<br>0.30 12<br>4 0.2<br>5<br>0.25 6<br>12 7 0.1<br>10 8 obj2<br>8 9<br>0 15 30 Generation45 60 75 90 obj1 6 4 10 0 15 30 Generation45 60 75 90<br>(g) HV of Tri-TSP20 (h) PF of Tri-TSP20 (i) IDG of Tri-TSP20<br>NSGA2 NSGA3 MOEAD<br>NSGA2_E2OC NSGA3_E2OC MOEAD_E2OC<br>HV IGD<br>HV IGD<br>HV IGD<br><!-- End of picture text -->

Figure 9: HV, IDG and PF performance of different operators in MOEAs on Tri-TSP. 



<!-- Start of picture text -->
0.24 HV (mean ± CI) Pareto Front (best run per method) 2.00 IGD (mean ± CI)<br>0.22 4800 1.75<br>1.50<br>0.20<br>4700 1.25<br>0.18<br>1.00<br>0.16 4600 0.75<br>0.14 0.50<br>4500<br>0.25<br>0.12<br>0 4 8 12 16 20 24 28 500 600 700 800 900 1000 0 4 8 12 16 20 24 28<br>Generation obj1 Generation<br>(a) HV on training instance (b) PF on training instance (c) IGD on training instance<br>HV (mean ± CI) 5400 Pareto Front (best run per method) 3.5 IGD (mean ± CI)<br>0.18 5350 3.0<br>0.17<br>5300 2.5<br>0.16<br>5250 2.0<br>0.15<br>0.14 5200 1.5<br>5150<br>0.13 1.0<br>0.12 5100<br>0.5<br>0.11 5050<br>0.0<br>0 4 8 12 16 20 24 28 800 1000 1200 1400 1600 0 4 8 12 16 20 24 28<br>Generation obj1 Generation<br>(d) HV on testing instance (e) PF on testing instance (f) IGD on testing instance<br>Random EoH MCTS-AHD UCB Win-UCB<br>FunSearch ReEvo CD LLM E2OC<br>HV obj2 IGD<br>HV obj2 IGD<br><!-- End of picture text -->

Figure 10: Performance of different AHD methods on BIFJSP training (mk15) and testing (mk14) instances. 

### **J.2 Different Parameters** 

The number of initial added prompts _AP_ controls the number of operator design thoughts generated during the warm-start phase. Larger _AP_ values increase the diversity of initial design thoughts and cover a broader range of improvement directions, but they also expand the design strategy search space, making it more difficult to identify optimal strategy paths. 

With four operators, each associated with _AP_ design thoughts, the number of possible design strategies scales as _AP_<sup>4</sup> . All experiments use the same manually designed initial operator code templates, design thoughts, and warm-start operator sets, and _AP_ is varied solely to control the number of LLM-generated design thoughts. We evaluate _AP ∈_ [1 _,_ 3 _,_ 5 _,_ 7], corresponding to strategy spaces of sizes [4<sup>2</sup> _,_ 4<sup>4</sup> _,_ 4<sup>6</sup> _,_ 4<sup>8</sup> ], respectively. 

To assess the impact of different _AP_ settings, instances are split into training and testing sets, and the search behavior and performance of generated operators are analyzed. The results, summarized in Table 8, show that larger _AP_ values increase the difficulty of invalid branches caused by the pruning conflict design strategy in MCTS, leading to a higher proportion of illegal operator code. Although _AP_ = 5 achieves the best HV on the training set, _AP_ = 3 delivers the most stable and best overall performance across all instances and the test set. To avoid overfitting, _AP_ = 3 is adopted in all subsequent experiments. 

### **J.3 Comparison with Expert-Designed Operators** 

To systematically assess the performance gap between E2OC and expert-designed operators, we conduct comparative experiments against classical operators and their manually constructed combinations on the TSP. NSGA-II is adopted as the multi-objective baseline algorithm. The evaluated operator set includes classical local search heuristics for TSP, named **2opt** , **3opt** , and **oropt** , as well as commonly used genetic operators such as ox and swap. These operators are organized into three categories. The first category consists of individual operators (2opt, 3opt, and oropt). The second category includes hybrid combinations of crossover, mutation, and local search, namely **ox** **~~s~~ wap** , **ox** **~~s~~ wap** **~~2~~ opt** , **ox** **~~s~~ wap** **~~3~~ opt** , and **ox** **~~s~~ wap** **~~o~~ ropt** . The third category contains sequential compositions of classical local search operators with different execution orders, including **2opt** **~~3~~ opt** **~~o~~ ropt** , **3opt 2opt** **~~o~~ ropt** , and **oropt 2opt** **~~3~~ opt** . Among these, the combination oropt ~~2~~ opt ~~3~~ opt exhibits the worst average performance and is therefore selected as the initial operator configuration for E2OC. The RI is measured with respect to this baseline, following the definition in Section H.3. The experimental results are summarized in Table 9. 



<!-- Start of picture text -->
HV (mean ± CI) Pareto Front (best run per method) IGD (mean ± CI)<br>0.24 3.5<br>0.22 4900 3.0<br>2.5<br>0.20<br>4800<br>2.0<br>0.18<br>1.5<br>4700<br>0.16<br>1.0<br>0.14 4600 0.5<br>0.12 0.0<br>0 4 8 12 16 20 24 28 500 600 700 800 0 4 8 12 16 20 24 28<br>Generation obj1 Generation<br>(a) HV on training instance (b) PF on training instance (c) IGD on training instance<br>IGD (mean ± CI)<br>HV (mean ± CI) Pareto Front (best run per method)<br>0.26 4300<br>5<br>0.24<br>4200<br>4<br>0.22<br>4100<br>0.20 3<br>0.18 4000<br>2<br>0.16<br>3900 1<br>0.14<br>3800 0<br>0.12<br>0 4 8 12 16 20 24 28 500 550 600 650 700 750 800 850 0 4 8 12 16 20 24 28<br>Generation obj1 Generation<br>(d) HV on testing instance (e) IGD on testing instance (f) PF on testing instance<br>MCTS_OC MCTS_Tuple MCTS_Sample E2OC<br>HV obj2 IGD<br>HV obj2 IGD<br><!-- End of picture text -->

Figure 11: Performance of different MCTS variants on BIFJSP training (mk15) and testing (mk13) instances. 

Table 8: Comparison of different number of initial added prompt _AP_ (see Algorithm 1). The performance metrics of the search process include: ValidRate (correctness of generated code), Mean, Range, and standard values Std of the scores. 

|**Parameter**|_AP_|**1**|**3**|**5**|**7**|
|---|---|---|---|---|---|
|**Search**|ValidR_↑_|**0.9969**|0.9965|0.9946|0.9930|
|**performance**|Mean_↑_|0.1508|**0.1574**|0.1498|0.1511|
||Range_↑_|0.1638|**0.1749**|0.1639|0.1654|
||Std_↑_|0.0087|0.0120|0.0098|**0.0127**|
|**All instances**|HV_↑_|0.2199|**0.2260**|0.2198|0.2185|
||IGD_↓_|1.5762|**1.3966**|1.5782|1.5891|
|**Train instance**|HV_↑_|0.1732|0.1709|**0.1746**|0.1726|
||IGD_↓_|0.7796|0.8532|**0.7734**|0.7735|
|**Test instances**|HV_↑_|0.2232|**0.2300**|0.2230|0.2218|
||IGD_↓_|1.6331|**1.4355**|1.6357|1.6474|



The results indicate that the standalone 2opt operator achieves the best HV performance, surpassing multiple manually designed operator combinations. The convergence trends of HV and IGD, and the Pareto front for all operators in Bi-TSP20, 50, and 100 are shown in Figure 12. Although the combination of ox and swap yields a relative improvement of 2.76% on the bi-objective TSP20 instance, further incorporating local search operators such as 2opt leads to performance degradation. To analyze the influence of operator ordering, different permutations of 2opt, 3opt, and oropt are evaluated within the third category. All reordered combinations exhibit inferior performance, with varying degrees of degradation, suggesting the presence of implicit operator incompatibilities that are difficult to resolve through manual composition. Using the consistently worst-performing oropt ~~2~~ opt ~~3~~ opt as the starting configuration, E2OC achieves the best performance on TSP50 and TSP100. Through a progressive search over operator design principles and composition strategies, E2OC not only substantially improves upon the initial configuration but also outperforms the best expert-designed operator, 2opt. 



<!-- Start of picture text -->
HV (mean ± CI) HV (mean ± CI) HV (mean ± CI)<br>0.65 0.55<br>0.40<br>0.50<br>0.60<br>0.35<br>0.45<br>0.55<br>0.40 0.30<br>0.50 0.35 0.25<br>0.30<br>0.45 0.20<br>0.25<br>0.40 0.15<br>0.20<br>0.35 0.15 0.10<br>0 25 50 75 100 125 150 175 200 0 25 50 75 100 125 150 175 200 0 25 50 75 100 125 150 175 200<br>Generation Generation Generation<br>(a) HV of Bi-TSP20 (b) HV of Bi-TSP50 (c) HV of Bi-TSP100<br>Pareto Front (best run per method) Pareto Front (best run per method)<br>Pareto Front (best run per method)<br>25.0<br>10 45<br>22.5<br>9<br>20.0 40<br>8<br>7 17.5 35<br>15.0<br>6<br>30<br>12.5<br>5<br>25<br>10.0<br>4<br>3 7.5 20<br>4 6 8 10 12 10 15 20 25 25 30 35 40 45<br>obj1 obj1 obj1<br>(d) PF of Bi-TSP20 (e) PF of Bi-TSP50 (f) PF of Bi-TSP100<br>IGD (mean ± CI) IGD (mean ± CI) IGD (mean ± CI)<br>0.7<br>1.0<br>0.6 0.8<br>0.5 0.8<br>0.6<br>0.4<br>0.6<br>0.3 0.4<br>0.4<br>0.2<br>0.2<br>0.2<br>0.1<br>0.0 0.0 0.0<br>0 25 50 75 100 125 150 175 200 0 25 50 75 100 125 150 175 200 0 25 50 75 100 125 150 175 200<br>Generation Generation Generation<br>(g) IGD of Bi-TSP20 (h) IDG of Bi-TSP50 (i) IDG of Bi-TSP100<br>2opt oropt ox_swap_2opt ox_swap_oropt 3opt_2opt_oropt E2OC<br>3opt ox_swap ox_swap_3opt 2opt_3opt_oropt oropt_2opt_3opt<br>HV HV HV<br>obj2 obj2 obj2<br>IGD IGD IGD<br><!-- End of picture text -->

Figure 12: HV, IDG and PF performance of different operators in solving Bi-TSPs. 

|**Method**|HV_↑_|**Bi-TSP20**<br>IGD_↓_|RI_↑_|HV_↑_|**Bi-TSP50**<br>IGD_↓_|RI_↑_|HV_↑_|**Bi-TSP100**<br>IGD_↓_|RI_↑_|
|---|---|---|---|---|---|---|---|---|---|
|2opt|**0.6117±0.0523**|**0.0684±0.1124**|**9.29%**|0.4255±0.1016|0.2122±0.2124|22.11%|0.2882±0.0907|0.3322±0.2708|12.54%|
|3opt|0.6003±0.0497|0.0821±0.1082|7.26%|0.4143±0.0971|0.2310±0.2074|18.90%|0.2797±0.0868|0.3555±0.2643|9.22%|
|oropt|0.5932±0.0489|0.1041±0.1026|5.99%|0.4001±0.0839|0.2587±0.1850|14.82%|0.2842±0.0792|0.3436±0.2418|10.98%|
|ox<br>~~s~~wap|0.5751±0.0473|0.1348±0.0994|2.76%|0.3604±0.0641|0.3081±0.1487|3.43%|0.2513±0.0554|0.3970±0.1823|-1.89%|
|ox<br>~~s~~wap<br>~~2~~opt|0.5472±0.0365|0.1971±0.0851|-2.22%|0.3312±0.0510|0.3746±0.1219|-4.94%|0.2342±0.0466|0.4459±0.1562|-8.55%|
|ox<br>~~s~~wap<br>~~3~~opt|0.5540±0.0420|0.1859±0.0870|-1.02%|0.3332±0.0533|0.3677±0.1300|-4.36%|0.2339±0.0481|0.4548±0.1638|-8.67%|
|ox<br>swap<br>oropt|0.5350±0.0349|0.2127±0.0786|-4.41%|0.3279±0.0496|0.3790±0.1217|-5.90%|0.2282±0.0422|0.4646±0.1462|-10.89%|
|2opt<br>~~3~~opt<br>~~o~~ropt|0.5576±0.0399|0.1710±0.0897|-0.37%|0.3505±0.0575|0.3618±0.1373|0.60%|0.2517±0.0579|0.4292±0.1844|-1.70%|
|3opt<br>~~2~~opt<br>~~o~~ropt|0.5637±0.0428|0.1637±0.0894|0.71%|0.3517±0.0586|0.3459±0.1354|0.94%|0.2546±0.0581|0.4174±0.1847|-0.58%|
|oropt<br>~~2~~opt<br>~~3~~opt|0.5597±0.0430|0.1698±0.0929|0.00%|0.3484±0.0610|0.3596±0.1434|0.00%|0.2561±0.0584|0.4165±0.1871|0.00%|
|E2OC|0.6104±0.0522|0.0710±0.1132|9.06%|**0.4312±0.1023**|**0.1023±0.0105**|**23.75%**|**0.2929±0.0930**|**0.3628±0.2928**|**14.38%**|



Table 9: Comparison of NSGA-II solving TSP with different classical operators. The ox is the sequential crossover operator and swap is the random swap mutation operator. The results are divided into three groups: group 1 is a single operator solved independently, group 2 is a cross-variable operator plus other neighborhood operators, and group 3 is a different order in the combinations. Bold text indicates optimal performance, and gray highlighting represents the baseline operator combination, which is the initial operator for E2OC. 

### **J.4 Generalization Comparison on TSPs with Different Scales** 

This section further examines the generalization capability of operators designed by E2OC by comparing them with the best expert-designed operator (2opt) and the initial operator configuration (oropt ~~2~~ opt ~~3~~ opt) on larger-scale Bi-TSP150 and Bi-TSP200 instances, as summarized in Table 10. In Bi-TSP150 and Bi-TSP200, E2OC achieves relative improvements of approximately 30.93% and 22.06%, respectively, over oropt ~~2~~ opt ~~3~~ opt. In contrast, the performance of the 2opt operator deteriorates as the problem scale increases. The convergence trends of HV and IGD, and the Pareto front of different method in Bi-TSP150 and 200 are shown in Figure 13. In terms of average HV, E2OC consistently achieves the best results across small-scale instances (Bi-TSP20-200), large-scale instances (Bi-TSP150-200), and the complete benchmark set, thereby demonstrating strong generalization performance across different problem scales. 

|||**Bi-TSP150**|||**Bi-TSP200**|||**Mean HV**_↑_||
|---|---|---|---|---|---|---|---|---|---|
|**Method**|HV_↑_|IGD_↓_|RI_↑_|HV_↑_|IGD_↓_|RI_↑_|TSP20-100|TSP150-200|TSP20-200|
|2opt|0.1205±0.0550|0.5239±0.2611|-10.48%|0.1026±0.0442|0.5905±0.2845|-18.27%|0.4418|0.1116|0.3097|
|oropt<br>~~2~~opt<br>~~3~~opt|0.1346±0.0485|0.4477±0.2232|0.00%|0.1256±0.0454|0.4591±0.2672|0.00%|0.3881|0.1301|0.2849|
|E2OC|**0.1762±0.0647**|0.7430±0.5519|**30.93%**|**0.1533±0.0554**|0.5150±0.4603|**22.06%**|**0.4448**|**0.1648**|**0.3328**|



Table 10: Comparison of NSGA-II for solving TSP of different sizes with different operators. TSP20-100 refers to the instance set containing TSP20, 50, and 100, and the same applies to others. 

### **J.5 Interpretability Analysis** 

During the warm-start phase, E2OC constructs a language space of design thoughts for each operator, composed of multiple improvement suggestions. Similar to multi-operator combinations, these design thoughts exhibit complex and hard-to-quantify coupling relationships. In E2OC, the number of initial added prompts is controlled by the parameter _AP_ . A larger _AP_ yields a richer set of operator design thoughts, but also enlarges the combinatorial design space, thereby requiring more computational resources to identify effective design strategies, i.e., optimal combinations of thoughts. This results in an inherent trade-off between search cost and design space expressiveness. To investigate this effect, we conduct a sensitivity analysis on _AP_ , as reported in Table 8. 

Moreover, different operator design thoughts often possess implicit coupling relations, such as mutual reinforcement, competition, or redundancy. The progressive search of design thought combinations via MCTS in E2OC can be interpreted as an attempt to quantify and exploit these latent interactions through performance-driven evaluation. Taking the Bi-FJSP as an example, we analyze the multi-domain operator design thought space generated by E2OC with _AP_ = 3 and NSGA-II as the warm-start baseline. For the FJSP setting, this space includes design thoughts associated with operators acting on different coding regions of the chromosome, namely **operation crossover** and **operation mutation** operators, as well as **machine crossover** and **machine mutation** operators, and it has been distinguished by different colors in Figure 14. 

In E2OC, initial design thoughts, code templates, and semantic descriptions are required for each operator prior to the warm-start phase. For multi-objective optimization operators, we adopt a minimal and generic initialization principle: ensuring legality and robustness while pursuing performance improvement. The design thoughts of other operators are automatically derived by the LLM through advantage analysis of high-performing operators observed during warm-start, resulting in structured 



<!-- Start of picture text -->
IGD (mean ± CI)<br>HV (mean ± CI) Pareto Front (best run per method)<br>0.25 70 1.2<br>1.0<br>65<br>0.20<br>60 0.8<br>0.15<br>55 0.6<br>0.10 50 0.4<br>0.05 45 0.2<br>40 0.0<br>0 25 50 75 100 125 150 175 200 35 40 45 50 55 60 65 70 0 25 50 75 100 125 150 175 200<br>Generation obj1 Generation<br>(a) HV of Bi-TSP150 (b) PF of Bi-TSP150 (c) IDG of Bi-TSP150<br>IGD (mean ± CI)<br>HV (mean ± CI) Pareto Front (best run per method)<br>0.225 100 1.2<br>95<br>0.200<br>1.0<br>90<br>0.175<br>85 0.8<br>0.150<br>80<br>0.125 0.6<br>75<br>0.100<br>0.4<br>70<br>0.075<br>65 0.2<br>0.050<br>60<br>0.025 0.0<br>0 25 50 75 100 125 150 175 200 60 70 80 90 0 25 50 75 100 125 150 175 200<br>Generation obj1 Generation<br>(d) HV of Bi-TSP200 (e) PF of Bi-TSP200 (f) IDG of Bi-TSP200<br>oropt_2opt_3opt E2OC 2opt<br>HV obj2 IGD<br>HV obj2 IGD<br><!-- End of picture text -->

Figure 13: HV, IDG and PF performance of different operators in solving Bi-TSPs with different scales. 

improvement suggestions. As summarized in Table 11, these suggestions emphasize different design focuses across operators. The combinations of such heterogeneous focuses constitute the diversity of design strategies and form the basis of interpretability in E2OC. 

Table 11: The focus of different operator design suggestions in the language space constructed by E2OC in Bi-FJSP. 

|**Operator**|**Notation**|**Focus**|
|---|---|---|
|Operation<br>~~C~~rossover|_p_1-0<br>_p_1-1<br>_p_1-2<br>_p_1-3|Predefined: Constraint- and robustness-first performance optimization<br>Pareto preservation and generation-aware exploration<br>Hypervolume-driven offspring selection<br>Parent-proximity control and convergence|
|Operation<br>~~M~~utation|_p_2-0<br>_p_2-1<br>_p_2-2<br>_p_2-3|Predefined: Constraint- and robustness-first performance optimization<br>HV-aware adaptivity and diversity preservation<br>Exploration control via mutation rate adaptation<br>Structural diversification driven by HV contribution|
|Machine<br>Crossover|_p_3-0<br>_p_3-1<br>_p_3-2<br>_p_3-3|Predefined: Constraint- and robustness-first performance optimization<br>Performance-aware crossover and diversity maintenance<br>Fitness-weighted recombination and feasibility handling<br>Fitness-landscape-guided exploration|
|Machine<br>Mutation|_p_4-0<br>_p_4-1<br>_p_4-2<br>_p_4-3|Predefined: Constraint- and robustness-first performance optimization<br>Multi-point exploration with experience guidance<br>Structural diversity through value replacement<br>Adaptivity and exploration intensity control|





<!-- Start of picture text -->
- Recommends non-uniform,<br>Design suggestions: generation dependent mutation for<br>Improve performance while  exploration.<br>meeting legality and robustness  p1-2 - Emphasizes maintaining the<br>requirements. Initial p1-0 Pareto front during crossover.<br>- Introduces non-uniform crossover<br>- Advocates specialized mutation to<br>expand objective-space coverage. p1-3 to preserve parent similarity.<br>- Suggests post-crossover mutation<br>- Highlights selecting offspring that  p1-4<br>to accelerate HV convergence.<br>directly improve HV.<br>OP_Crossover<br>Suggests adaptive mutation guided<br>Design suggestions:<br>p2-2 by hypervolume improvement.<br>Improve performance while  p2-0 Proposes blending-based mutations<br>meeting legality and robustness<br>to maintain solution diversity.<br>requirements.<br>Initial<br>- Advocates adaptive mutation rates<br>- Recommends non-uniform<br>p2-3 using hypervolume contribution.<br>mutation to strengthen exploration.<br>- Introduces two-point exchange or<br>- Emphasizes adaptive mutation  p2-4 inversion for stronger search-space<br>rates based on solution  OP_Mutation diversification.<br>performance and HV.<br>Design suggestions: - Suggests adaptive crossover points<br>Improve performance while  p3-0 p3-2 driven by performance metrics.<br>meeting legality and robustness  - Proposes blending strategies to<br>requirements. Initial preserve diversity and improve HV.<br>- Recommends fitness-weighted<br>- Introduces adaptive crossover<br>gene blending.- Advocates non-uniform crossover  p3-3 points based on the fitness<br>landscape.<br>for broader exploration. p3-4 - Utilizes non-uniform crossover to<br>- Emphasizes repair mechanisms to  MA_Crossover<br>maintain diversity and enhance HV.<br>ensure feasibility under machine<br>constraints. - Proposes multi-point mutation to<br>explore multiple regions<br>Design suggestions:<br>Improve performance while  p4-0 p4-2 simultaneously.<br>- Suggests heuristic, performance-<br>meeting legality and robustness  informed selection of mutation<br>requirements. Initial indices.<br>- Recommends swap-based  p4-3 - Suggests increasing perturbation<br>mutation for stronger diversity. range for broader exploration.<br>- Advocates Gaussian or smooth  p4-4 - Emphasizes adaptive mutation rates<br>mutations for controlled exploration. MA_Mutation based on population performance.<br><!-- End of picture text -->

Figure 14: Example of a language space constructed by E2OC in Bi-FJSP 

### **J.6 Evolutionary Process Visualization** 

Understanding the progressive search process of E2OC’s semantic-level design strategies is essential for exploring the complex coupling relationships among multiple operators or their corresponding design concepts. The evolution process of the crossover and mutation operators for processes and machines in NSGA-II for solving BIFJSP is optimized by E2OC, as shown in Figure 15. During the warm-start phase, all operators (represented by colored circles) generate different design thoughts (indicated by numeric indices). Throughout the optimization, MCTS is employed to explore various combinations of these design thoughts, ultimately identifying the most effective design strategy. 

Over 30 iterations, design thoughts from different operators form composite design strategies. The algorithm generator then employs an operator rotation evolution mechanism to design operator combinations, which are integrated into NSGA-II for three independent multi-objective optimization runs. The average HV across these runs serves as the performance score for both the operators and the design strategy. Notably, generation 11 and generation 24 use the same design strategy (3,1,0,1), yet yield different performance outcomes. A single evaluation of an operator combination in multi-objective optimization cannot provide an accurate score, requiring iterative evaluation sampling. 

During the iterative process, MCTS continuously computes the exploration and exploitation scores for each node, favoring the expansion and simulation of branches with higher scores. It is worth noting that (0,0,0,0) represents the manually defined initial design thoughts, as shown in Figure 14. The green curve tracks the best operator score discovered by E2OC across iterations. From generation 3 (HV 169.4) to generation 4 (HV 175.6), a locally optimal design strategy is obtained. Subsequent attempts focus on varying combinations around design thoughts of index 0 for the **operation mutation** and index 2 for the **machine** 



<!-- Start of picture text -->
Design & evaluate operator combination  181.9<br>based on design strategies<br>obj2<br>1 Final Design Strategy and<br>1 operator Combination<br>178.6<br>178.5<br>1<br>178.0<br>obj1<br>1 177.4 177.3<br>176.8 2 176.8<br>176.6 HV fluctuations 0<br>2 1<br>175.6 1 175.5 3<br>175.0175.1 2 3 175.1 11 2 174.4 30 174.6174.5 174.9 3 03 0<br>169.4 172.7 12 2003 3121 2021 174.0 303 171.6 1 172.5 00 220 101 0103 30 3213 172.8 02 172.6 23 2 172.0 3 173.4 033 1102 2203 3101 173.8 010 1301 173.2 21 203 00 1<br>3 3 0 1 1 3 3 2 0 0<br>1<br>1 167.7 3 2 0 1 3 23<br>1<br>3 - Recommends non-uniform, generation  - Suggests adaptive crossover points<br>dependent mutation for exploration. driven by performance metrics.<br>2 0 - Emphasizes maintaining the Pareto front  - Proposes blending strategies to<br>0 3 AI-A during crossover. 1 preserve diversity and improve HV. 1<br>2 Design  - Suggests adaptive mutation guided by  - Proposes multi-point mutation to explore<br>hypervolume improvement. multiple regions simultaneously.<br>0 strategy - Proposes blending-based mutations to  - Suggests heuristic, performance-<br>maintain solution diversity. 1 informed selection of mutation indices. 1<br>0 10 20 30<br>Iteration<br>AI-S<br>180<br>175<br>170<br>165<br>-3<br>Scores (HV 10   )<br><!-- End of picture text -->

Figure 15: The evolution process of E2OC to design the operator combinations in NSGA-II for solving Bi-FJSP. The optimal design strategy is searched through the iteration of MCTS. Different colored balls denote different FJSP operators, and the number indicates the corresponding design thought index. 

**crossover** , but none yield further improvement. Performance improves to 176.8 by generation 10, and by generation 12 a superior strategy combination (1,1,1,1) is identified, achieving an HV of 181.9, which significantly outperforms the initial design strategy. 

For an LLM-based algorithm designer, the input text directly shapes the distribution and direction of the generated algorithms. Compared with other possible combinations, these four design thoughts constitute a complete and complementary design space that covers key dimensions such as parameter adaptation, strategy hybridization, information utilization, and goal orientation. In practice, any set of design thoughts must balance “dimensional coverage” and “synergy.” The present combination achieves a favorable trade-off between these two aspects. Focusing solely on a single dimension (e.g., parameter adaptation) tends to limit generalization capability. By conducting a refined search within this validated and effective design space, the LLM is more likely to produce high-performance algorithms. 

### **J.7 Designed Operators** 

This section compares the FJSP crossover operators generated by E2OC with those obtained from manual design and EoH, focusing on their design motivations and implementation characteristics. Although EoH and E2OC both employ LLMs to assist operator construction, they differ in how design knowledge is represented and incorporated into the final operators. The specific implementations of these operators are shown in Figure 17 and Figure 16. The performance differences are shown in Table 3. 

For the machine-selection crossover, shown in Figure 17, the manually designed operator applies a single-point positional recombination, which is simple and problem-agnostic but ignores solution-level feedback. The EoH-designed operator emphasizes structural preservation by explicitly retaining identical decision components and introducing random exchanges only on divergent positions, reflecting a design bias toward stable inheritance within a single-operator evolution setting. In contrast, the E2OC-designed operator incorporates objective-space distance into the crossover decision, adaptively adjusting recombination strength according to parent similarity. This behavior emerges from E2OC’s progressive design strategy search, where different 

recombination principles are explored and selected through operator rotation under performance feedback, rather than being fixed a priori. 



<!-- Start of picture text -->
def  Operation_Crossover (parent1: np.ndarray, parent2: np.ndarray, n_vars: int) -><br>def  Operation_Crossover (parent1: np.ndarray, parent2: np.ndarray, n_vars:  Tuple[np.ndarray, np.ndarray]:<br>int) -> Tuple[np.ndarray, np.ndarray]:<br># Placeholder for fitness-based alpha calculation<br># Implement operation priority crossover     def  calculate_alpha (fitness1, fitness2):<br>    if n_vars < 2: return  0.5 + 0.2 * (fitness1 - fitness2) / (abs(fitness1) + abs(fitness2) + 1e-10)<br># Direct copy for extremely small length to avoid randint(1,1) error<br>return  parent1.copy(), parent2.copy() # Assume fitness is the negative of the objective function value for HV maximization<br>    # Replace with actual fitness evaluation logic<br>    cp = np.random.randint(1, n_vars)     fitness1 = -np.sum(parent1)<br>    fitness2 = -np.sum(parent2)<br>    child1 = np.concatenate([parent1[:cp], parent2[cp:]])     alpha = calculate_alpha(fitness1, fitness2)<br>    child2 = np.concatenate([parent2[:cp], parent1[cp:]])     r1 = np.linalg.norm(parent1)<br>    r2 = np.linalg.norm(parent2)<br>return  child1, child2     theta1 = np.arctan2(parent1[1:], parent1[:-1]) if n_vars > 1 else np.array([])<br>    theta2 = np.arctan2(parent2[1:], parent2[:-1]) if n_vars > 1 else np.array([])<br>Initial<br># Cyclic rotation of angles<br>    theta_child1 = np.roll(theta1, 1) * (1 - alpha) + theta2 * alpha<br>    theta_child2 = np.roll(theta2, 1) * (1 - alpha) + theta1 * alpha<br>def  Operation_Crossover (parent1: np.ndarray, parent2: np.ndarray, n_vars:<br>int) -> Tuple[np.ndarray, np.ndarray]: # Blend radii<br>    r_child1 = alpha * r1 + (1 - alpha) * r2<br>    if parent1.shape != (n_vars,) or parent2.shape != (n_vars,):     r_child2 = (1 - alpha) * r1 + alpha * r2<br>        return parent1.copy(), parent2.copy()<br># Convert back to Cartesian coordinates<br>    try:     def  polar_to_cartesian (r, angles):<br>        point1, point2 = np.sort(np.random.choice(range(1, n_vars), size=2,          if n_vars == 1:<br>replace=False)) return  np.array([r])<br>        elif n_vars == 2:<br>        child1 = np.concatenate([parent1[:point1], parent2[point1:point2],  return  np.array([r * np.cos(angles[0]), r * np.sin(angles[0])])<br>parent1[point2:]])         else:<br>        child2 = np.concatenate([parent2[:point1], parent1[point1:point2],              coords = np.zeros(n_vars)<br>parent2[point2:]])             coords[0] = r<br>            for i in range(1, n_vars - 1):<br>        child1 = np.clip(child1, 0, 1)                 coords[i] = r * np.prod(np.cos(angles[:i])) * np.sin(angles[i - 1])<br>        child2 = np.clip(child2, 0, 1)             coords[-1] = r * np.prod(np.cos(angles[: n_vars - 2]))<br>return  coords<br>return  child1, child2<br>    child1 = polar_to_cartesian(r_child1, theta_child1)<br>    except:     child2 = polar_to_cartesian(r_child2, theta_child2)<br>return  parent1.copy(), parent2.copy()<br>EOH return  child1, child2 E2OC<br><!-- End of picture text -->

Figure 16: Operation crossover operators designed by EoH and E2OC on FJSP. 

For the operation-sequence crossover, shown in Figure 16, manually designed and EoH-designed operators remain within positional segment exchange, differing mainly in recombination granularity. The E2OC-designed operator instead reformulates crossover in a continuous geometric space, where offspring are generated via fitness-aware interpolation between parent representations. This design reflects E2OC’s ability to explore couplings between operators and evaluation feedback, as the operator form is shaped not only by structural validity but also by how effectively it cooperates with other operators under repeated evaluation. Such non-positional recombination strategies are difficult to obtain through isolated heuristic evolution but naturally arise under E2OC’s multi-operator co-evolution framework. 

Overall, the observed performance advantages of E2OC-designed operators stem not from increased operator complexity, but from the systematic exploration of design strategies and their interactions enabled by operator rotation evolution. By allowing multiple design thoughts to be decoupled, recombined, and empirically validated across operators, E2OC produces operators that exhibit more adaptive and context-aware recombination behaviors, leading to more robust performance on FJSP instances. 

## **K Limitations** 

Compared to existing single-heuristic design methods, E2OC has achieved promising performance in MOEAs through the co-evolution of design strategies and executable codes for multiple operators. However, this approach still presents several limitations: 

**High Evaluation Cost of Design Thoughts Search.** Expanding the search for design thoughts significantly increases computational demands. This results in substantial resource consumption during evaluation, presenting a major challenge for 



<!-- Start of picture text -->
def  Machine_Crossover (parent1: np.ndarray, parent2: np.ndarray, n_vars: int) -<br>def  Machine_Crossover (parent1: np.ndarray, parent2: np.ndarray, n_vars: int) -<br>> Tuple[np.ndarray, np.ndarray]:<br>> Tuple[np.ndarray, np.ndarray]:<br># Randomly select crossover point<br>    common_mask = parent1 == parent2<br>    cross_point = np.random.randint(1, n_vars)<br>    divergent_mask = ~common_mask<br># Create offspring<br>    child1 = np.empty(n_vars, dtype=parent1.dtype)<br>    child1 = np.concatenate([parent1[:cross_point], parent2[cross_point:]])<br>    child2 = np.empty(n_vars, dtype=parent1.dtype)<br>    child2 = np.concatenate([parent2[:cross_point], parent1[cross_point:]])<br>return  child1, child2<br>Initial     child1[common_mask] = parent1[common_mask]<br>    child2[common_mask] = parent1[common_mask]<br>def  Machine_Crossover (parent1: np.ndarray, parent2: np.ndarray, n_vars: int) -     swap_mask = np.random.random(n_vars) < 0.5<br>> Tuple[np.ndarray, np.ndarray]:     swap_mask &= divergent_mask<br>    obj_distance = np.linalg.norm(parent1 - parent2)     child1[swap_mask] = parent2[swap_mask]<br>    child2[swap_mask] = parent1[swap_mask]<br># Adjust crossover probability based on objective space distance<br>    crossover_prob = 0.5 + 0.3 * (1 - obj_distance / np.max([obj_distance, 1e-6]))     keep_mask = divergent_mask & ~swap_mask<br>    child1[keep_mask] = parent1[keep_mask]<br>    mask = np.random.rand(n_vars) < crossover_prob     child2[keep_mask] = parent2[keep_mask]<br>    child1 = np.where(mask, parent1, parent2)<br>    child2 = np.where(~mask, parent1, parent2) return  child1, child2<br>return  child1, child2 E2OC EOH<br><!-- End of picture text -->

Figure 17: Machine crossover operators designed by EoH and E2OC on FJSP. 

achieving efficient algorithm iteration in practice. 

**Dependence on Domain Knowledge and Capability Boundaries of LLMs.** E2OC heavily relies on domain knowledge provided by LLMs, as its core mechanism involves the combinatorial search of algorithmic design knowledge. The effectiveness of this approach, however, is constrained by the quality of the domain knowledge, which is inherently dependent on the capabilities of the underlying large language model. 

These challenges highlight key issues that mainstream LLM-based AHD methods need to address in future research. 

