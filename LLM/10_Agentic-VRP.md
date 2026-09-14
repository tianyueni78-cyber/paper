Published as a conference paper at ICLR 2026 

# AN AGENTIC FRAMEWORK WITH LLMS FOR SOLVING COMPLEX VEHICLE ROUTING PROBLEMS 

**Ni Zhang**<sup>1</sup> **, Zhiguang Cao**<sup>1</sup> **, Jianan Zhou**<sup>2</sup> **, Cong Zhang**<sup>2</sup> **, Yew-Soon Ong**<sup>2</sup> 1School of Computing and Information Systems, Singapore Management University, Singapore 2 College of Computing and Data Science, Nanyang Technological University, Singapore ni.zhang.2025@phdcs.smu.edu.sg, zgcao@smu.edu.sg jianan004@e.ntu.edu.sg, cong.zhang92@gmail.com, asysong@ntu.edu.sg 

## ABSTRACT 

Complex vehicle routing problems (VRPs) remain a fundamental challenge, demanding substantial expert effort for intent interpretation and algorithm design. While large language models (LLMs) offer a promising path toward automation, current approaches still rely on external intervention, which restrict autonomy and often lead to execution errors and low solution feasibility. To address these challenges, we propose an <u>Agentic Framework</u> with <u>LLMs</u> (AFL) for solving complex vehicle routing problems, achieving _full automation_ from problem instance to solution. AFL directly extracts knowledge from raw inputs and enables _selfcontained_ code generation without handcrafted modules or external solvers. To improve trustworthiness, AFL decomposes the overall pipeline into three manageable subtasks and employs four specialized agents whose coordinated interactions enforce cross-functional consistency and logical soundness. Extensive experiments on 60 complex VRPs, ranging from standard benchmarks to practical variants, validate the effectiveness and generality of our framework, showing comparable performance against meticulously designed algorithms. Notably, it substantially outperforms existing LLM-based baselines in both code reliability and solution feasibility, achieving rates close to 100% on the evaluated benchmarks. 

## 1 INTRODUCTION 

Vehicle routing problems (VRPs) are fundamental to industrial and commercial applications such as logistics (Bochtis & Sørensen, 2010; Konstantakopoulos et al., 2022) and transportation (Cattaruzza et al., 2017; Zhang et al., 2022), yet they remain challenging to solve due to their diverse variants with intricate real-world constraints. Traditional approaches (Furnon & Perron; Helsgaun, 2017; Vidal, 2022; Wouda et al., 2024) often require substantial expert effort, either to translate problem statements into mathematical formulations or to design specialized algorithms. Although recent neural solvers (Kool et al., 2018; Kwon et al., 2020) alleviate the dependence on domain knowledge, they still require a certain degree of manual adaptation to address more complex VRPs. 

More recently, large language models (LLMs) (Zhao et al., 2023), with their strong natural language understanding and code generation capabilities (Ma et al., 2026), may offer a promising avenue for automation, reducing reliance on manual effort and enabling flexible solver development across diverse VRP variants. Some early attempts (Yang et al., 2024; Liu et al., 2024b) directly prompt LLMs to generate solutions but fall short in terms of solution optimality and feasibility. Other approaches (Romera-Paredes et al., 2024) explore the use of LLMs to generate programming code as a proxy for addressing challenges in VRP optimization, which can be broadly categorized into two directions. The first direction centers on _evolving basic heuristics_ tailored for conventional VRPs, with representative examples including EoH (Liu et al., 2024a) and ReEvo (Ye et al., 2024). In contrast, the second direction emphasizes _developing general frameworks_ capable of handling diverse VRP variants, making it more practical and application-oriented. 

Early research efforts have started to address this challenging second direction. Their workflow generally comprises two phases: _framework-design_ , in which the architecture and generation strategy are specified (see Section 3), and _framework-execution_ , in which the resulting framework is deployed 

1 

Published as a conference paper at ICLR 2026 

Table 1: Comparison of representative LLM-based approaches for VRPs. 

||ARS<br>(Li et al., 2025a)|DRoC<br>(Jiang et al., 2025b)|SGE<br>(Iklassov et al., 2024)|**AFL**<br>(This Work)|
|---|---|---|---|---|
|Complex VRPs<br>|✓|✓|✗|✓|
|Self-Containment<sup>_§_</sup><br>|✗|✗|✓|✓|
|Full Automation<sup>_†_</sup>|✗|✗|✗|✓|
|High Trustworthiness<sup>_∗_</sup>|✗|✗|✗|✓|



> _§ LLMs produce complete code without relying on handcrafted modules or external solvers during framework-design._ 

> _† The entire workflow proceeds from raw input to final solution without human intervention during framework-execution._ 

> _∗ Achieving high code reliability and solution feasibility (e.g., ≥_ 95% _)._ 

to solve diverse problem instances. ARS (Li et al., 2025a) constructs constraint-checking functions by retrieving and adapting templates from a predefined constraint library, while DRoC (Jiang et al., 2025b) employs a retrieval-augmented generation (RAG) strategy to produce code that invokes ORTools (Furnon & Perron) for problem solving. Although both ARS and DRoC can handle complex VRPs, these module-level generation methods are not self-contained, depending on handcrafted code modules or external solvers during framework-design, and not fully automated, as they still require human involvement to extract instance-specific information during framework-execution. This dependence may introduce misalignment between LLM-generated code and external systems, which can result in execution errors and reduced solution feasibility. In contrast, SGE (Iklassov et al., 2024) achieves self-containment but is limited to relatively simple problems like the Traveling Salesman Problem (TSP), as it lacks effective mechanisms for handling complex constraints and fails to provide full automation or reliable code and solution validity. In this paper, as summarized in Table 1, we address these limitations by proposing a general framework of collaborative LLMempowered agents that can tackle complex VRPs with self-containment, full automation, and high trustworthiness in both code and solutions. 

We introduce an **<u>A</u>** <u>gentic</u> **<u>F</u>** <u>ramework</u> with **<u>L</u>** LMs (AFL) that solves complex VRPs end-to-end, from problem instance to solution. Specifically, it derives domain knowledge directly from instance inputs and leverages this knowledge to guide code generation. To enhance the feasibility and reliability of the generated code and the resulting VRP solutions under complex constraints, the pipeline is decomposed into three tractable subtasks: _problem description_ , _code generation_ , and _solution derivation_ , each handled by multiple LLM agents tailored to their tasks. In total, we design four specialized agents, including _generation agent_ , _judgment agent_ , _revision agent_ , and _error analysis agent_ , collaborating to ensure cross-functional consistency, logical soundness, and constraint satisfaction. The overview of AFL is presented in Fig. 1. Our main contributions are summarized as follows. 

- 1) Conceptually, we position LLMs as knowledgeable developers of self-contained frameworks for solving complex VRPs, achieving full automation from problem instance to solution without reliance on handcrafted modules or external solvers. 

- 2) Methodologically, we propose AFL, an agentic LLM framework that decomposes the inherently intractable pipeline into three manageable subtasks and employs four specialized agents to collaboratively enhance trustworthiness in both code and solutions. 

- 3) Experimentally, we evaluate AFL on 60 VRPs, comprising 48 representative VRPs from the literature, 8 complex electric VRPs from practical scenarios, and 4 classical VRPs in broader settings. Extensive results demonstrate the effectiveness and generality of our framework, showing competitive performance against carefully tailored algorithms while delivering superior code reliability and solution feasibility compared to existing LLM-based approaches. 

## 2 PRELIMINARIES 

The VRP is a fundamental combinatorial optimization task. It seeks a set of minimum-cost routes that allow a fleet of vehicles to serve geographically distributed customers while satisfying practical constraints such as vehicle capacity, route length, or customer time windows. Classic variants include the Capacitated VRP (CVRP), where each vehicle has a fixed capacity limit; the VRP with Time Windows (VRPTW), where every customer must be served within a specific time interval; and the Electric VRP (EVRP), which incorporates battery capacity and recharging requirements. These 

2 

Published as a conference paper at ICLR 2026 

Table 2: Constraint descriptions and corresponding VRPLib-format fields. 

|**Constraint**|**VRPLib Field**|**Description**|
|---|---|---|
|Capacity (C)|CAPACITY<br>DEMAND<br>~~S~~ECTION|Each vehicle has a maximum load capacity, and each<br>customer is associated with a demand that must be<br>satisfied without exceeding this capacity.|
|Duration Limit (L)|DISTANCE<br>~~L~~IMIT|Each vehicle route is constrained by a maximum<br>travel distance, and the total distance of any route<br>must not exceed this limit.|
|Time Windows (TW)|TIME<br>~~W~~INDOW<br>~~S~~ECTION<br>SERVICE<br>TIME<br>SECTION|Each customer must be served within a specified time<br>interval, and service times must be included in the<br>schedule to maintain feasibility.|
|Open Route (O)|DEPOT<br>~~S~~ECTION|Vehicles may not be required to return to the depot after<br>serving their assigned customers, relaxing the standard<br>closed-route assumption.|
|Electric Vehicle (E)|FUEL<br>CAPACITY<br>FUEL<br>CONSUMPTION<br>~~R~~ATE<br>REFUEL<br>RATE<br>STATION<br>~~S~~ECTION|Electric vehicles are constrained by limited battery<br>capacity; they consume energy during travel and<br>refuel at recharging stations.|
|Multi Depot (MD)|DEPOT<br>~~S~~ECTION|Multiple depots are defined, allowing vehicles to start<br>and/or end at different depots, enabling flexible re-<br>source allocation across regions.|
|Backhaul (B)|DEMAND<br>~~S~~ECTION|Each route includes both deliveries (linehauls) and<br>pickups (backhauls), where pickups occur after all<br>deliveries.|
|Mixture Backhaul (MB)|DEMAND<br>~~S~~ECTION|Linehaul and backhaul customers appear in mixed<br>order within the same route.|



formulations capture diverse real-world delivery, ride-sharing, and service-dispatch applications. A detailed introduction to each variant considered in this paper is provided in Appendix B. 

To represent benchmark instances in a consistent way, we adopt the VRPLIB format (Uchoa et al., 2017), a plain-text specification similar to TSPLIB (Reinelt, 1991). A VRPLIB file begins with general information such as the instance name and an optional comment, followed by key sections specifying the problem type, edge weight type, dimension, and the coordinates of each location. Additional sections may cover parameters such as vehicle capacity, customer demands (with positive values for linehaul and negative for backhaul), distance limits, depot IDs, time windows, service times, and energy-related data for electric vehicles (e.g., fuel capacity, consumption rate, refueling rate, and charging station locations). 

The mapping between constraints and their corresponding VRPLIB fields is summarized in Table 2, with further details on each field provided in Table 8 in the Appendix. Our AFL directly takes VRPLIB-format instances as input. We also evaluate AFL on JSON and CSV formats to demonstrate its robustness to different data representations. The results are reported in Section C.11 and Table 17. 

## 3 METHODOLOGY 

In this section, we introduce AFL, an agentic LLM framework for solving complex VRPs by structuring the pipeline into three subtasks: _problem description_ , _code generation_ , and _solution derivation_ . Within these subtasks, specialized agents, including the _generation agent (GA)_ , _judgment agent (JA)_ , _revision agent (RA)_ , and _error analysis agent (EAA)_ , collaborate to fulfill their respective roles, ultimately enhancing the trustworthiness of both the generated code and the derived solutions under the constraints of the given problem instance. 

The overview of AFL is presented in Fig. 1. Specifically, given a VRP instance _G_ , the system first generates a problem description _D_ ( _G_ ) through the collaborative operation of the GA, JA, and RA. This problem description is then used to query the buffer which stores previously tested problem codes, to check whether relevant code has been previously stored. If such code exists, the workflow proceeds directly to the solution derivation stage. Otherwise, the GA progressively generates the required functions one by one, while the JA and RA iteratively evaluate and refine the code until it meets all requirements and constraints. Once a complete implementation is produced, it is executed 

3 

Published as a conference paper at ICLR 2026 



<!-- Start of picture text -->
Subtask 1: Problem Description Subtask 3: Solution Derivation<br>Description Generation Description Judgement and Revision Code Execution<br>TYPEDIMENSION CAPACITY  : CVRP : 1: 51 What this  description right? Is this  CVRP.py ERROR!<br>EDGE_WEIGHT_TYPE  :  problem is? Judgement   If no, why?<br>EUC_2D NODE_COORD_SECTION Agent Code Python  Error<br>1 0.191519 0.622109 Considering the<br>2 0.437728 0.7853593 0.779976 0.272593…… Generation  DescriptionProblem  Revision   judgment, I need description and to revise the  Error Analysis  Given the problem<br>Instance Agent Agent description. description, code,<br>and error, why<br>Subtask 2: Code Generation does this error<br>Code Existence Check InstanceTYPEDIMENSION CAPACITYEDGE_WEIGHT_TYPE  EUC_2D NODE_COORD_SECTION 1 0.191519 0.6221092 0.437728 0.7853593 0.779976 0.272593……: CVRP: 1: 51 :  DescriptionInput ConstrainOutput Code Generation generate the initial/destrI need to  CVRP.py Error Analysis  Code Revision Agent occur and how can it be solved? Error Analysis<br>Objective Code Generation  oy/insert/…  function<br>Agent Code Revision   Judgement<br>Problem Description Buffer Agent Agent<br>Code Judgement and Revision True<br>Iterate and Store Final Code<br>Base on the problem<br>description, function  False Is this code right? If  Description Constr<br>Revision  Agent requirement, code and judgement, I need to revise the code. Judgement and SuggestionJudgement  Agent revision suggestions.no, I need to explain why and provide  ObjectiveInput OutputCodeain<br>Problem Descriptionand Code Buffer<br><!-- End of picture text -->

Figure 1: Overview of an agentic framework with LLMs for solving complex VRPs. 

to derive a solution. If execution errors occur, the EAA diagnoses their causes and provides explanations and suggestions, which the RA and JA use to revise the code. This iterative process continues until the code passes validation and produces a feasible solution. Finally, the corresponding problem description and code are stored in the buffer for future reuse. Examples of the agents’ prompts and outputs for each subtask are provided in Appendix D. In the following, we present each specialized agent and pipeline stage in detail. 

### 3.1 SPECIALIZED AGENT 

**Generation Agents (GA)** are responsible for producing descriptions and code. In the problem description subtask, they generate a description _D_ ( _G_ ) for the input VRPLib-format instance _G_ . In the code generation subtask, they generate function code _C_ ( _G, D_ ( _G_ ) _, P_ ( _f_ )) in an end-to-end manner, guided by the instance, the generated description, and the specific prompts _P_ ( _f_ ) associated with function _f_ . The resulting description and code are then forwarded to the JA for evaluation. 

**Judgment Agents (JA)** evaluate the validity of the generated description and code. In the problem description subtask, they verify whether _D_ ( _G_ ) aligns with the instance context. In the code generation and solution derivation subtasks, they further assess whether the generated or revised code satisfies the prompt requirements and is free from syntactic and logical errors. If the judgment is positive, the description or code is accepted and the process advances to the next step. Otherwise, the JA provides explanations of identified issues along with suggestions for resolution by the RA. 

**Revision Agents (RA)** refine both the description and the code. Description revision is guided by the JA’s feedback and the instance context, while code revision additionally leverages the previously generated description. After each revision, the updated description or code is returned to the JA for re-evaluation, and this process continues until a positive judgment is reached. 

**Error Analysis Agents (EAA)** operate exclusively in the solution derivation subtask, where they analyze the causes of errors during code execution and provide suggestions for resolving them. The analysis is then passed to the RA for code revision. 

### 3.2 SUBTASK 1: PROBLEM DESCRIPTION 

**Description Generation.** Given a VRPLib-format instance _G_ , our framework automatically extracts domain knowledge from the instance context without human intervention, offering a user-friendly interface for problem setup. The VRPLib format is a widely adopted benchmark specification for VRPs, defining essential elements such as the problem type, number of nodes, node coordinates, depot ID, and various constraint-related parameters, as summarized in Table 2. Based on this, the 

4 

Published as a conference paper at ICLR 2026 

GA generates the problem description for the given instance _D_ ( _G_ ) = _{P, S, K, X, Y, Z}_ . A detailed example is provided in Appendix D.1. Here, we define the components of _D_ ( _G_ ) as follows: 

- 1) _P_ specifies the _type of problem_ (e.g., CVRP, VRPTW, ECVRPTW). It is inferred from the problem type and the constraint-related parameters defined in the instance context, and it determines the name of the generated code file (e.g., CVRP.py). 

- 2) _S_ denotes the _textual description_ of the instance’s problem type. It is provided to the code generation subtask to inform the agents about the problem definition. 

- 3) _K_ represents the set of _constraints_ along with their explanations. These are derived from the constraint-related parameters and problem type specified in the instance context. In addition, _K_ includes visit and depot constraints, which are supplementary requirements automatically analyzed and inferred by the GA. Within the code generation subtask, _K_ guides the agents in embedding these constraints into function design, thereby enhancing the solution feasibility. 

- 4) _X_ denotes the _required input_ for solving the given instance. In the code generation subtask, it specifies the information that must be read from the instance and enforces consistency by requiring input variable names to match those in _X_ , thereby reducing potential errors. For example, in CVRP, _X_ includes node coordinates, depot ID, customer demands, and vehicle capacity. 

- 5) _Y_ refers to the _expected output_ . For instance, in CVRP, the solver should produce a set of vehicle routes, each starting and ending at the depot, visiting every customer exactly once, ensuring that no vehicle route exceeds capacity and that all demands are satisfied. Moreover, the returned route should represent the best feasible solution among the candidates. 

- 6) _Z_ represents the _objective function_ , such as minimizing the total travel distance, which is further used in constructing the cost function code. 

**Description Judgment and Revision.** After the GA generates the above problem description _D_ ( _G_ ), the JA evaluates its correctness. The evaluation checks: (i) whether any component of _D_ ( _G_ ) conflicts with the instance, (ii) whether the components are internally consistent, and (iii) whether the input definition _X_ is properly specified in the instance context. If a conflict is detected, the instance context serves as the reference standard. If no issues are found, the output is set to TRUE, the problem description subtask terminates, and the process advances to the next code generation subtask. Otherwise, the output is set to FALSE, accompanied by explanations of the negative judgment and suggestions for the RA to make correction. The RA then revises _D_ ( _G_ ) based on the JA’s feedback and the instance context. The revised description is returned to the JA for re-evaluation, and this iterative process continues until the JA confirms that _D_ ( _G_ ) is correct. This iterative procedure improves the accuracy of _D_ ( _G_ ), as demonstrated by the ablation study in Section 4.5. The problem description subtask provides the essential information required for code generation and enforces unified naming conventions and constraints, which must remain consistent throughout the entire pipeline. 

### 3.3 SUBTASK 2: CODE GENERATION 

We adopt a unified destroy-insert heuristic for solving VRPs, as it offers greater flexibility than others and can handle complex, practical problem variants. The code generation subtask consists of interdependent functions: _read_ _~~v~~ rp_ , _distance_ , _cost_ , _initial_ , _destroy_ , _insert_ , _validate_ , and _main_ , which together form a complete VRP solver. Generating the full solver code, however, is challenging, as it requires maintaining consistency across multiple functions while satisfying all requirements. To address this, the GA produces the functions sequentially, with each building upon the previously generated code to ensure correctness and reduce the burden on the LLM. In addition, the JA and RA iteratively refine the code by correcting unmet requirements, syntactic errors, and logical inconsistencies after each function is generated. We describe each step in detail below. 

**Code Generation.** The code structure of the problem-solving workflow is shown in Fig. 2. We specify the role of each function to provide a structured foundation for guiding the GA in generating the corresponding code. Note that these functions are executed only in the solution derivation subtask and are fixed by the EAA if any runtime errors occur. First, _read_ _~~v~~ rp_ parses a VRPLibformat instance file into a structured dictionary containing all required fields specified by the input _X ∈D_ ( _G_ ), ensuring that each variable in _X_ is accurately extracted from the instance context _G_ . Next, _distance_ computes the distance matrix from the node coordinates. _initial_ constructs a solution using a greedy strategy that respects constraints in _K_ . The feasibility of the solution 

5 

Published as a conference paper at ICLR 2026 

is verified by _validate_ . _cost_ evaluates the objective value of a given solution according to the objective function _Z_ . To enable iterative improvement, _destroy_ removes a subset of customers from the current solution, following the strategy described in Appendix C.2 and Algorithm 1. Then, the _insert_ function reinserts the removed customers into feasible positions while minimizing the additional cost. If no feasimulated sible insertion exists, a new vehicle is assigned to serve these cusread_vrp annealing tomers in compliance with constraints in _K_ . At each improvement step, the feasibility of the resulting solution is verified by distance cost _validate_ to ensure that every constraint in _K_ is satisfied. In the event of a constraint violation, the function must raise an error, initial validate thereby aiding the EAA in debugging. Finally, _main_ orchestrates the entire workflow, encompassing initialization, iterative validate insert improvement, and overall solution management, as illustrated in Fig. 2. In the initialization phase, an initial feasible solution is cost destroy generated, while in the improvement phase ( _T_ steps in total), the solution is iteratively refined through destruction, insertion, valiInitialization Improvement dation, and cost evaluation, with new solutions accepted according to the simulated annealing criterion (see Appendix C.3). Figure 2: Code structure. 

**Code Judgment and Revision.** For each function generated by 

the GA, the JA assesses the correctness of the code produced thus far, checking compliance with the requirements and detecting any syntactic or logical errors. If issues are identified, the RA revises the code based on the JA’s feedback and the instance context. The revised code is then returned to the _JA_ for re-evaluation, and this process is repeated until the _JA_ delivers a positive judgment. By validating and correcting each code segment before generating the next function, this mechanism reduces the burden on subsequent code generation and revision, improves efficiency, and enhances the reliability of the final solver implementation. Moreover, constraint considerations are enforced throughout the code generation process. The generated code is repeatedly checked to ensure that all constraints in _K_ are properly incorporated. This iterative enforcement helps the final solver produce solutions feasible with respect to the instance constraints. 

### 3.4 SUBTASK 3: SOLUTION DERIVATION 

The functions produced in the code generation subtask is not always executable, as constructing a full VRP solver is highly complex. Bugs may arise for several reasons: some stem from syntactic errors, others from logical flaws, and still others from unmet requirements, such as failing to incorporate certain constraints. Although we have designed strategies such as enforcing constraint considerations during code generation, guaranteeing the correctness of LLM-generated code remains non-trivial. To address this challenge and enhance the trustworthiness of the generated VRP solver, we leverage an EAA to identify the cause of errors and provide explanations along with suggestions for correction. Similar to the code generation subtask, the RA then modifies the code based on this feedback, after which the JA evaluates the revision. If the code remains unsatisfactory, the RA further adjusts it according to the JA’s feedback, and this process repeats until the JA delivers a positive judgment. The revised code is then re-executed to obtain a feasible solution. Eventually, the model stores the problem description _D_ ( _G_ ) together with the corresponding generated code in the buffer. If the same problem is encountered again, the framework can directly reuse the stored code, thereby improving efficiency and avoiding redundant computation. 

## 4 EXPERIMENT 

We first evaluate AFL against traditional and neural approaches on 48 standard benchmarks incorporating common constraints such as capacity (C), duration limit (L), time window (TW), open route (O), multi depot (MD), backhaul (B), and mixture backhaul (MB), which are widely used to assess traditional algorithms. We then extend the evaluation to 8 practical electric (E) VRPs, which remain challenging for traditional solvers. Next, we benchmark AFL against LLM-based approaches, assessing code reliability, solution feasibility, and overall performance. We also conduct ablation studies to examine the effectiveness of our agentic design. In addition, we report comparisons under different prompt strategies in the main text. We further evaluate AFL’s robustness across different 

6 

Published as a conference paper at ICLR 2026 

Table 3: Comparison results on standard benchmarks. More results are shown in Table 11. 

|||n=50|||n=100|||n=50|||n=100||
|---|---|---|---|---|---|---|---|---|---|---|---|---|
||Obj.|Gap (%)|Time (m)|Obj.|Gap (%)|Time (m)|Obj.|Gap (%)|Time (m)|Obj.|Gap (%)|Time (m)|
|HGS-PyVRP|10.37|–|10.40|15.62|–|20.80|10.59|–|10.40|15.77|–|20.80|
|OR-Tools|10.57|1.91|10.40|16.28|4.18|20.80|10.83|2.34|10.40|16.47|5.30|20.80|
|RF-POMO|RP<br>10.51|1.31|0.03|15.91|1.83|0.12|RPL<br>10.75|1.52|0.02|16.11|2.17|0.10|
|AFL (_T_=500)|CV<br>10.89|5.01|0.18|16.66|6.66|0.32|CV<br>11.35|7.18|0.33|17.36|10.08|1.03|
|AFL (_T_=2000)|10.70|3.18|0.46|16.22|3.84|1.02|11.25|6.23|1.13|17.03|7.99|7.35|
|AFL (_T_=10000)|**10.59**|**2.12**|2.10|**15.99**|**2.38**|4.38|11.18|5.57|6.93|16.84|6.79|25.48|
|HGS-PyVRP|16.03|–|10.40|25.42|–|20.80|6.51|–|10.40|9.73|–|20.80|
|OR-Tools|W<br>16.08|0.35|10.40|25.81|1.51|20.80|6.55|0.69|10.40|10.00|2.73|20.80|
|RF-POMO|PT<br>16.37|2.09|0.02|26.34|3.58|0.12|VRP<br>6.70|2.90|0.02|10.18|4.66|0.10|
|AFL (_T_=500)|VR<br>**16.49**|**2.87**|0.59|26.60|4.64|2.15|OC<br>6.79|4.30|0.31|10.37|6.58|0.4|
|AFL (_T_=2000)|C<br>**16.28**|**1.56**|2.26|**26.02**|**2.36**|8.92|**6.69**|**2.76**|0.66|10.11|3.91|1.16|
|AFL (_T_=10000)|**16.19**|**0.99**|9.31|**25.79**|**1.46**|38.45|**6.64**|**2.00**|2.20|**9.99**|**2.67**|5.52|
|HGS-PyVRP|16.36|–|10.40|25.76|–|20.80|6.51|–|10.40|9.72|–|20.80|
|OR-Tools|W<br>16.44|0.50|10.40|26.26|1.90|20.80|L<br>6.55|0.67|10.40|10.00|2.79|20.80|
|RF-POMO|PLT<br>16.75|2.38|0.02|26.78|3.95|0.12|RP<br>6.70|2.95|0.02|10.18|4.66|0.1|
|AFL (_T_=500)|VR<br>17.07|4.34|0.61|27.60|7.14|1.95|OCV<br>6.81|4.61|0.43|10.37|6.68|1.03|
|AFL (_T_=2000)|C<br>**16.78**|**2.57**|1.95|26.96|4.66|7.21|6.71|3.07|1.21|10.15|4.42|3.68|
|AFL (_T_=10000)|**16.61**|**1.53**|8.90|26.56|3.11|35.33|**6.64**|**1.99**|5.65|**9.99**|**2.78**|16.27|
|HGS-PyVRP|10.51|–|10.40|16.93|–|20.80|10.51|–|10.40|16.93|–|20.80|
|OR-Tools|W<br>10.52|0.08|10.40|17.03|0.58|20.80|TW<br>10.50|0.11|10.40|17.02|0.73|20.80|
|RF-POMO|PT<br>10.66|1.38|0.02|17.39|2.72|0.12|PL<br>10.66|1.38|0.02|17.39|2.73|0.12|
|AFL (_T_=500)|CVR<br>**10.64**|**1.24**|0.67|**17.36**|**2.54**|0.75|VR<br>**10.74**|**2.12**|1.05|17.61|4.02|3.63|
|AFL (_T_=2000)|O<br>**10.57**|**0.57**|2.86|**17.14**|**1.24**|10.63|OC<br>**10.64**|**1.24**|3.76|**17.32**|**2.30**|16.75|
|AFL (_T_=10000)|**10.55**|**0.38**|11.15|**17.04**|**0.65**|49.05|**10.58**|**0.67**|17.27|**17.19**|**1.54**|70.31|
|HGS-PyVRP|9.69|–|10.40|14.38|–|20.80|10.19|–|10.40|14.78|–|20.80|
|OR-Tools|9.80|1.16|10.40|14.93|3.85|20.80|L<br>10.33|1.39|10.40|15.43|4.34|20.80|
|RF-POMO|RPB<br>10.00|3.17|0.02|15.02|4.47|0.10|PB<br>10.59|3.94|0.02|15.63|5.70|0.10|
|AFL (_T_=500)|CV<br>10.24|5.68|2.62|15.48|7.65|5.56|VR<br>10.87|6.67|0.31|16.18|9.47|2.15|
|AFL (_T_=2000)|10.09|4.13|6.51|15.07|4.80|14.47|C<br>10.64|4.42|3.31|15.71|6.29|4.80|
|AFL (_T_=10000)|**9.95**|**2.27**|31.54|**14.74**|**2.50**|70.59|10.52|3.24|11.06|15.41|4.26|20.18|
|HGS-PyVRP|18.29|–|10.40|29.47|–|20.80|6.90|–|10.40|10.34|–|20.80|
|OR-Tools|W<br>18.37|0.38|10.40|29.95|1.60|20.80|B<br>6.93|0.21|10.40|10.58|2.32|20.80|
|RF-POMO|BT<br>18.60|1.67|0.02|30.34|2.96|0.12|RP<br>7.09|2.69|0.02|10.84|4.82|0.12|
|AFL (_T_=500)|VRP<br>19.06|4.21|0.99|31.50|6.89|3.75|OCV<br>7.57|9.71|0.72|11.67|12.86|3.50|
|AFL (_T_=2000)|C<br>**18.75**|**2.52**|1.76|30.63|3.94|17.20|7.40|7.24|2.64|11.34|9.67|16.30|
|AFL (_T_=10000)|**18.61**|**1.75**|14.88|**30.17**|**2.38**|70.69|7.30|5.80|7.97|11.12|7.54|56.08|
|HGS-PyVRP|18.36|–|10.40|29.03|–|20.80|6.90|–|10.40|10.34|–|20.80|
|OR-Tools|W<br>18.42|0.33|10.40|29.83|2.77|20.80|L<br>6.93|0.39|10.40|10.58|2.36|20.80|
|RF-POMO|BLT<br>18.94|1.85|1.00|30.80|3.28|0.12|PB<br>7.09|2.69|1.00|10.84|4.83|0.12|
|AFL (_T_=500)|RP<br>19.09|3.98|0.85|31.31|7.85|3.02|CVR<br>7.16|3.77|1.05|10.95|5.90|4.57|
|AFL (_T_=2000)|CV<br>**18.87**|**2.78**|2.53|30.64|5.55|5.75|O<br>**7.05**|**2.17**|4.02|10.72|3.68|8.72|
|AFL (_T_=10000)|**18.78**|**2.29**|20.19|30.33|4.48|69.12|**7.03**|**1.74**|23.50|**10.58**|**2.32**|76.06|
|HGS-PyVRP|11.67|–|10.40|19.16|–|20.80|11.67|–|10.40|19.16|–|20.80|
|OR-Tools|TW<br>11.68|0.11|10.40|19.30|0.76|20.80|TW<br>11.68|0.11|10.40|19.31|0.77|20.80|
|RF-POMO|PB<br>11.80|1.15|1.00|19.61|2.34|0.12|PBL<br>11.81|1.16|1.00|19.61|2.34|0.13|
|AFL (_T_=500)|VR<br>**11.80**|**1.11**|0.68|**19.67**|**2.66**|1.95|VR<br>**11.81**|**1.20**|0.57|**19.67**|**2.66**|4.65|
|AFL (_T_=2000)|OC<br>**11.73**|**0.51**|2.26|**19.41**|**1.30**|15.71|C<br>**11.75**|**0.69**|4.92|**19.41**|**1.30**|18.15|
|<br>AFL (_T_=10000)|**11.71**|**0.34**|26.32|**19.29**|**0.68**|83.60|O<br>**11.71**|**0.34**|10.75|**19.29**|**0.68**|39.73|



**Note:** The term _obj._ denotes the objective value, _gap_ represents the relative gap with respect to HGS-PyVRP, and _time_ indicates the total runtime. For all three metrics, lower values are better. Bold numbers highlight our cases where the gap from the SOTA is within 3%, which is considered acceptable given that our framework is fully automated and self-contained. 

LLM backbones, and these results are presented in Section C.10 and Table C.9 in the Appendix. Finally, we evaluate 4 additional open benchmarks, including TSP, ATSP, ACVRP, and SOP, to demonstrate the broad applicability of our framework. All experiments were conducted via the OpenAI API using GPT-4.1 (OpenAI, 2024) on a server equipped with an AMD EPYC 7702P CPU and 64 GB of RAM, without GPU acceleration. All results shown below are derived using the same heuristic for the same variant on a given instance. This setting is more practical for real-world applications and significantly reduces code-generation overhead. The code and dataset is available at https://github.com/ZHANG-NI/AFL.git 

7 

Published as a conference paper at ICLR 2026 

Table 4: Comparison results on practical benchmarks. 

||S|mall Instan|ces|L|arge Instanc|es||S|mall Instan|ces|L|arge Instan|ces|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||Obj.|Gap (%)|Time (m)|Obj.|Gap (%)|Time (m)||Obj.|Gap (%)|Time (m)|Obj.|Gap (%)|Time (m)|
|ACO|270.68|0.00|0.23|1384.15|0.00|6.89||341.74|0.00|0.24|952.07|0.00|7.92|
|Greedy|P<br>309.63|14.39|0.05|1407.97|1.72|0.13|PL|714.34|109.03|0.06|7298.83|666.63|0.20|
|AFL (_T_=500)|CVR<br>**266.21**|**-1.65**|0.18|**1145.51**|**-17.24**|0.26|VR|**276.95**|**-18.96**|0.18|**885.15**|**-7.03**|0.43|
|AFL (_T_=2000)|E<br>**264.21**|**-2.39**|0.24|**1100.11**|**-20.52**|0.54|EC|**276.94**|**-18.96**|0.25|**866.87**|**-8.95**|1.22|
|AFL (_T_=10000)|**263.33**|**-2.72**|0.51|**1045.74**|**-24.45**|2.19||**276.94**|**-18.96**|0.53|**861.05**|**-9.56**|4.95|
|ACO|323.88|0.00|0.25|1129.67|0.00|7.00||179.30|0.00|0.22|796.97|0.00|6.81|
|Greedy|TW<br>379.88|17.29|0.06|1868.64|65.41|0.22|RP|197.03|9.89|0.06|866.02|8.66|0.20|
|AFL (_T_=500)|VRP<br>**306.50**|**-5.37**|0.18|**1101.14**|**-2.53**|0.40|CV|**166.76**|**-6.99**|0.19|**632.73**|**-20.61**|0.61|
|AFL (_T_=2000)|EC<br>**300.95**|**-7.08**|0.23|**1071.22**|**-5.17**|1.17|EO|**166.02**|**-7.41**|0.40|**628.34**|**-21.16**|1.90|
|AFL (_T_=10000)|**300.23**|**-7.30**|0.51|**1044.63**|**-7.53**|4.52||**165.41**|**-7.75**|1.20|**623.36**|**-21.78**|10.82|
|ACO|419.85|0.00|0.44|2842.17|0.00|13.88||204.87|0.00|0.34|759.24|0.00|10.50|
|Greedy|LTW<br>434.29|3.44|0.09|3039.87|6.96|0.34|PL|221.34|8.04|0.08|896.92|18.13|0.30|
|AFL (_T_=500)|RP<br>**388.36**|**-7.50**|0.21|**2729.73**|**-3.96**|0.50|CVR|**173.43**|**-15.35**|0.21|**726.34**|**-4.33**|0.54|
|AFL (_T_=2000)|ECV<br>**386.84**|**-7.86**|0.30|**2612.83**|**-8.07**|1.54|EO|**172.90**|**-15.61**|0.36|**693.71**|**-8.63**|1.50|
|AFL (_T_=10000)|**381.84**|**-9.05**|0.87|**2527.87**|**-11.06**|7.07||**172.53**|**-15.79**|1.12|**669.43**|**-11.83**|9.29|
|ACO|223.91|0.00|0.39|1139.12|0.00|11.98||205.77|0.00|27.55|1184.48|0.00|14.12|
|Greedy|PTW<br>241.22|7.73|0.08|1219.73|7.08|0.33|RP<br>|222.89|8.32|0.10|1230.85|3.91|0.37|
|AFL (_T_=500)|VR<br>**183.26**|**-18.15**|0.19|**856.13**|**-24.84**|0.43|CV<br>LTW|**181.74**|**-11.68**|0.20|**785.53**|**-33.68**|0.48|
|AFL (_T_=2000)|EOC<br>**183.11**|**-18.22**|0.24|**835.03**|**-26.70**|1.20|EO<br>|**181.43**|**-11.83**|0.26|**777.02**|**-34.40**|1.26|
|AFL (_T_=10000)|**182.88**|**-18.32**|0.49|**815.64**|**-28.40**|4.75||**181.27**|**-11.91**|0.53|**775.03**|**-34.57**|5.84|



### 4.1 COMPARISON ON STANDARD BENCHMARK 

We compare AFL with the traditional solvers HGS (implemented in PyVRP) (Vidal, 2022; Wouda et al., 2024) and OR-Tools (Furnon & Perron), as well as the neural solver RF-POMO (Berto et al., 2025b). The experimental settings and testing data follow Berto et al. (2025b), including 1,000 instances for each problem. Note that _our objective is not to surpass SOTA solvers on conventional VRPs, which reflect decades of expert effort, but to develop a fully automated and self-contained framework for tackling complex VRPs_ . Therefore, in the comparison shown in Table 3, we regard a 3% relative gap with respect to SOTA solvers as an acceptable criterion. We report the results of AFL after 500, 2,000, and 10,000 iterations of solution improvement. The runtime of AFL is measured as the sum of the problem description and solution derivation phases. The code generation phase, analogous to the training phase of a neural solver, is excluded, since once the solver code is produced, it can be reused across instances without incurring repeated generation overhead, and the runtime analysis of code generation phase is shown in Section C.4 in Appendix. Results are partly shown in Table 3, with the rest provided in Table 11 in the Appendix due to space limitations. 

AFL automatically generates a complete VRP solver without any manual intervention. As shown in Table 3, it achieves a relative gap within 3% of the SOTA HGS on most benchmark problems, demonstrating competitive performance. It is worth noting that the reported runtimes exhibit stochastic variation: more complex problems do not necessarily result in longer execution times. For example, the runtime on OCVRPL is shorter than that on CVRPL. This variability arises from the LLM-based code generation process, where the model may occasionally produce implementations (e.g., sorting) with higher algorithmic complexity, leading to longer runtimes. 

### 4.2 COMPARISON ON PRACTICAL BENCHMARK 

Traditional solvers like HGS (Vidal, 2022; Wouda et al., 2024) and OR-Tools (Furnon & Perron) are inherently constrained by their internal implementations and cannot be directly adapted to new problem settings without substantial modifications to the core codebase, whereas AFL can naturally accommodate practical VRPs. To demonstrate this, we conduct experiments on a widely used benchmark for ECVRPTW (Schneider et al., 2014), a representative variant of the electric vehicle routing problem (EVRP). Specifically, the dataset contains 36 small instances with 5, 10, and 15 customers, as well as 56 large instances with 100 customers. To further assess generality, we extend this benchmark to 7 additional EVRP variants, namely ECVRP, ECVRPL, EOVRPL, EOCVRP, EOCVRPTW, ECVRPLTW, and EOCVRPLTW, enabling a more comprehensive evaluation across 

8 

Published as a conference paper at ICLR 2026 

Table 5: RER and SR. Table 6: Gap comparison on benchmark instances. 

||RER_↓_|SR_↑_|||TSPLib|||CVRPLib||CV|RPL|
|---|---|---|---|---|---|---|---|---|---|---|---|
|||||50–200|200–500|500–1000|100–200|200–500|500–1000|50|100|
|SGE|94.1%|5.9%|SGE|109.59%|287.53%|660.36%|–|–|–|–|–|
|DRoC|824%|176%|DRoC|3.02%|3.96%|4.22%|3.93%|8.35%|–|6.80%|8.31%|
||.<br>|.<br>|ReEvo|5.18%|9.13%|14.78%|8.77%|14.88%|19.81%|–|–|
|AFL|**0%**|**100%**|AFL|**1.28%**|**2.68%**|**2.98%**|**1.93%**|**5.20%**|**6.66%**|**5.57%**|**6.79%**|



diverse and challenging problem settings. Given the intrinsic difficulty of these problems and the lack of directly applicable advanced solvers, we adopt ACO and Greedy as baselines, as both are widely recognized flexible heuristics for complex VRPs. For ACO, the number of improvement steps is fixed at 500. The results in Table 4 demonstrate the consistent effectiveness of AFL. Although ACO is executed with 500 improvement steps, our framework attains better objective values in shorter runtimes. These empirical findings highlight the superiority of AFL on complex and practical VRPs, where traditional solvers often face limitations. 

### 4.3 COMPARISON WITH LLM-BASED SOLVER 

We compare AFL in trustworthiness and performance with representative LLM-based approaches for diverse VRPs (above 16 variants plus TSP), namely SGE (Iklassov et al., 2024) and DRoC (Jiang et al., 2025b), while excluding ARS (Li et al., 2025a) due to the unavailability of its source code. 

To assess trustworthiness, we report the _Runtime Error Rate (RER)_ , which measures the percentage of generated code that executes with errors, and the _Success Rate (SR)_ , which measures the percentage of generated code that produces feasible solutions. As summarized in Table 5 and detailed in Appendix C.6, SGE is limited to solving only TSP, attaining an RER of 94.1% and an SR of 5.9%. DRoC extends to TSP, CVRP, and VRPL, with an RER of 82.4% and an SR of 17.6%. In contrast, AFL successfully handles all 17 tested VRP variants, reaching 0% RER and 100% SR, highlighting its superior code reliability and solution feasibility. 

To assess performance, we further evaluate AFL on the problem classes (i.e., TSP, CVRP, and CVRPL) solvable by SGE and DRoC. Specifically, we conduct experiments on TSPLib (Reinelt, 1991), a real-world TSP benchmark containing 50 instances with sizes ranging from 50 to 1,000 customers, and on CVRPLib (Uchoa et al., 2017), a real-world CVRP benchmark containing 100 instances with sizes ranging from 100 to 1,000 customers. We further report the results of ReEvo (Ye et al., 2024) on TSPLib and CVRPLib, as both TSP and CVRP are solved in the original paper, to provide a broader assessment. For CVRPL, we adopt the same benchmark setting as in Section 4.1. The results are shown in Table 6, where gaps for TSPLib and CVRPLib are reported relative to their best-known solutions, while CVRPL gaps are measured against HGS. DRoC is able to solve CVRPLib instances only with fewer than 500 customers within the 10-hour time limit. Across all evaluated benchmarks, AFL consistently outperforms both SGE, DRoC, and ReEvo. 

### 4.4 COMPARISON WITH PROMOTING STRATEGY 

To evaluate the effectiveness of our model, we compare AFL with several classical prompting strategies, including standard prompting (Brown et al., 2020), self-refine (Madaan et al., 2023), self-debug (Chen et al., 2023), self-verification (Weng et al., 2022), and chain-of-thought (CoT) prompting (Wei et al., 2022). Table 9 presents the results, where the gaps are measured with respect to HGS-PyVRP. All strategies employ the same step-by-step function generation process for a fair comparison. The results show that AFL achieves the lowest runtime error rate and the highest success rate, as well as the best overall solution quality. 

### 4.5 ABLATION STUDY 

To study the necessity of the judgement agent (JA) and revision agent (RA), we run ablation experiments by removing them from AFL. The results are shown in Fig. 3. Without JA and RA, the framework frequently produces incorrect problem descriptions and invalid code. With RA included, the framework becomes more robust, yielding more accurate problem descriptions and executable 

9 

Published as a conference paper at ICLR 2026 



<!-- Start of picture text -->
Accuracy of Problem Descriptions on Standard Benchmark Accuracy of Problem Descriptions on Practical Benchmark<br>100 100<br>80 80<br>60 60<br>40 40<br>None None<br>20 Revision 20 Revision<br>Judgement+Revision Judgement+Revision<br>0 0<br>CVRP VRPL VRPTW OVRP VRPLTW OVRPL OVRPTW OVRPLTW ECVRP EVRPL EVRPTW EOVRP EVRPLTW EOVRPL EOVRPTW EOVRPLTW<br>Problem Type Problem Type<br>40 Gap (%) on Standard Benchmark (n=50) 35 Gap (%) on Standard Benchmark (n=100)<br>3530 RevisionJudgement+Revision 3025 RevisionJudgement+Revision<br>25<br>20<br>20<br>15<br>15<br>10 10<br>5 5<br>0 0<br>CVRP VRPL VRPTW OVRP VRPLTW OVRPL OVRPTW OVRPLTW CVRP VRPL VRPTW OVRP VRPLTW OVRPL OVRPTW OVRPLTW<br>Problem Type Problem Type<br>Accuracy (%) Accuracy (%)<br>Gap (%) Gap (%)<br><!-- End of picture text -->

Figure 3: Ablation studies on the JA and RA. 

code. With both JA and RA, the accuracy of problem description reaches almost 100%, and the framework produces reliable code and feasible solutions. This improvement arises because these agents ensures that all operator requirements are adequately considered during the code generation. These results verify our agentic design, showing that JA and RA are crucial for maintaining accurate problem descriptions and ensuring the trustworthiness of the generated code and derived solutions. 

### 4.6 BROAD APPLICABILITY 

We further evaluate AFL on four additional open benchmarks: TSP, ATSP, ACVRP, and SOP. Results for TSP are presented in Table 6. ATSP and ACVRP capture asymmetric routing, which frequently arises in real-world applications, while SOP introduces precedence-constrained path planning, another realistic and challenging setting. All three variants are formulated using non-Euclidean distance metrics. Specifically, the ATSP benchmark (Johnson & McGeoch, 1997) contains 18 instances ranging from 17 to 443 nodes. The ACVRP dataset (Helsgaun, 2017) provides 120 capacityconstrained cases with asymmetric distance matrices covering 16 to 200 customers. The SOP benchmark (Renaud et al., 1996) includes 39 precedence-constrained instances with sizes between 9 and 380 nodes. Experimental results for ATSP, ACVRP, and SOP are presented in Table 13, Table 14, and Table 15 in the Appendix, respectively. By achieving competitive performance across these diverse datasets, AFL demonstrates broad applicability, indicating that our framework has the potential to be extended to a wider range of problem variants. 

## 5 CONCLUSION 

This paper introduces AFL, an agentic LLM-based framework for solving complex vehicle routing problems (VRPs). Unlike prior approaches that depend on human intervention or predefined modules, AFL achieves self-containment and full automation by extracting domain knowledge directly from raw inputs and generating executable code and feasible solutions end-to-end. By decomposing the pipeline into three tractable subtasks and coordinating four specialized agents, AFL substantially improves code reliability and solution feasibility. Extensive experiments on 60 standard and practical VRP variants demonstrate the effectiveness, applicability, and trustworthiness of AFL. 

The main limitation lies in performance, which do not yet surpass state-of-the-art solvers specifically designed for well-studied problems such as CVRP, a trade-off we consider acceptable given AFL’s automation and generality. As future work, we plan to incorporate strategies such as evolutionary search to guide code generation and further enhance both code quality and search efficiency. Overall, our work highlights the potential of agentic LLMs as a general and trustworthy paradigm for solving complex combinatorial optimization problems with minimal domain knowledge, paving the way for more autonomous and adaptive optimization frameworks and democratizing access to advanced optimization techniques for non-expert users. 

10 

Published as a conference paper at ICLR 2026 

## ACKNOWLEDGMENTS AND DISCLOSURE OF FUNDING 

This research is supported by the National Research Foundation, Singapore under the AI Singapore Programme (AISG Award No: AISG3-RPGV-2025-017). 

## REFERENCES 

- Irwan Bello, Hieu Pham, Quoc V. Le, Mohammad Norouzi, and Samy Bengio. Neural combinatorial optimization with reinforcement learning. In _ICLR Workshop Track_ , 2017. 

- Federico Berto, Chuanbo Hua, Junyoung Park, Laurin Luttmann, Yining Ma, Fanchen Bu, Jiarui Wang, Haoran Ye, Minsu Kim, Sanghyeok Choi, Nayeli Gast Zepeda, Andr´e Hottung, Jianan Zhou, Jieyi Bi, Yu Hu, Fei Liu, Hyeonah Kim, Jiwoo Son, Haeyeon Kim, Davide Angioni, Wouter Kool, Zhiguang Cao, Jie Zhang, Kijung Shin, Cathy Wu, Sungsoo Ahn, Guojie Song, Changhyun Kwon, Lin Xie, and Jinkyoo Park. RL4CO: an Extensive Reinforcement Learning for Combinatorial Optimization Benchmark. In _Proceedings of the 31st ACM SIGKDD Conference on Knowledge Discovery and Data Mining_ , 2025a. 

- Federico Berto, Chuanbo Hua, Nayeli Gast Zepeda, Andr´e Hottung, Niels Wouda, Leon Lan, Junyoung Park, Kevin Tierney, and Jinkyoo Park. RouteFinder: Towards foundation models for vehicle routing problems. _Transactions on Machine Learning Research_ , 2025b. ISSN 2835-8856. 

- Jieyi Bi, Yining Ma, Jianan Zhou, Wen Song, Zhiguang Cao, Yaoxin Wu, and Jie Zhang. Learning to handle complex constraints for vehicle routing problems. In _Advances in Neural Information Processing Systems_ , 2024. 

- DD Bochtis and Claus G Sørensen. The vehicle routing problem in field logistics: Part ii. _Biosystems engineering_ , 105(2):180–188, 2010. 

- Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, et al. Language models are few-shot learners. _Advances in neural information processing systems_ , 33:1877–1901, 2020. 

- Diego Cattaruzza, Nabil Absi, Dominique Feillet, and Jes´us Gonz´alez-Feliu. Vehicle routing problems for city logistics. _EURO Journal on Transportation and Logistics_ , 6(1):51–79, 2017. 

- Xinyun Chen, Maxwell Lin, Nathanael Sch¨arli, and Denny Zhou. Teaching large language models to self-debug. _arXiv preprint arXiv:2304.05128_ , 2023. 

- Pham Vu Tuan Dat, Long Doan, and Huynh Thi Thanh Binh. HSEvo: Elevating automatic heuristic design with diversity-driven harmony search and genetic algorithm using llms. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 39, pp. 26931–26938, 2025. 

- Darko Drakulic, Sofia Michel, Florian Mai, Arnaud Sors, and Jean-Marc Andreoli. BQ-NCO: Bisimulation quotienting for efficient neural combinatorial optimization. _Advances in Neural Information Processing Systems_ , 36:77416–77429, 2023. 

- Vincent Furnon and Laurent Perron. OR-Tools routing library. URL https://developers. google.com/optimization/routing/. 

- Chengrui Gao, Haopu Shang, Ke Xue, Dong Li, and Chao Qian. Towards generalizable neural solvers for vehicle routing problems via ensemble with transferrable local policy. In _Proceedings of the Thirty-Third International Joint Conference on Artificial Intelligence_ , pp. 6914–6922, 2024. 

- Keld Helsgaun. An extension of the lin-kernighan-helsgaun TSP solver for constrained traveling salesman and vehicle routing problems. _Roskilde: Roskilde University_ , pp. 24–50, 2017. 

- Andr´e Hottung and Kevin Tierney. Neural large neighborhood search for routing problems. _Artificial Intelligence_ , 313:103786, 2022. 

- Zangir Iklassov, Yali Du, Farkhad Akimov, and Martin Takac. Self-guiding exploration for combinatorial problems. _Advances in Neural Information Processing Systems_ , 37:130569–130601, 2024. 

11 

Published as a conference paper at ICLR 2026 

- Xia Jiang, Yaoxin Wu, Minshuo Li, Zhiguang Cao, and Yingqian Zhang. Large language models as end-to-end combinatorial optimization solvers. In _The Thirty-ninth Annual Conference on Neural Information Processing Systems_ , 2025a. URL https://arxiv.org/abs/2509.16865. 

- Xia Jiang, Yaoxin Wu, Chenhao Zhang, and Yingqian Zhang. DRoC: Elevating large language models for complex vehicle routing via decomposed retrieval of constraints. In _13th international Conference on Learning Representations_ , 2025b. 

- David S Johnson and Lyle A McGeoch. The traveling salesman problem: A case study in local optimization. _Local search in combinatorial optimization_ , 1(1):215–310, 1997. 

- Chaitanya K Joshi, Quentin Cappart, Louis-Martin Rousseau, and Thomas Laurent. Learning TSP requires rethinking generalization. In _International Conference on Principles and Practice of Constraint Programming_ , 2021. 

- Chaitanya K Joshi, Quentin Cappart, Louis-Martin Rousseau, and Thomas Laurent. Learning the travelling salesperson problem requires rethinking generalization. _Constraints_ , 27(1):70–98, 2022. 

- Grigorios D Konstantakopoulos, Sotiris P Gayialis, and Evripidis P Kechagias. Vehicle routing problem and related algorithms for logistics distribution: A literature review and classification. _Operational research_ , 22(3):2033–2062, 2022. 

- Wouter Kool, Herke van Hoof, and Max Welling. Attention, learn to solve routing problems! In _International Conference on Learning Representations_ , 2018. 

- Yeong-Dae Kwon, Jinho Choo, Byoungjip Kim, Iljoo Yoon, Youngjune Gwon, and Seungjai Min. POMO: Policy optimization with multiple optima for reinforcement learning. In _Advances in Neural Information Processing Systems_ , volume 33, pp. 21188–21198, 2020. 

- Kai Li, Fei Liu, Zhenkun Wang, Xialiang Tong, Xiongwei Han, Mingxuan Yuan, and Qingfu Zhang. ARS: Automatic routing solver with large language models. _arXiv preprint arXiv:2502.15359_ , 2025a. 

- Sirui Li, Zhongxia Yan, and Cathy Wu. Learning to delegate for large-scale vehicle routing. In _Advances in Neural Information Processing Systems_ , volume 34, pp. 26198–26211, 2021. 

- Tianyou Li, Haijun Zou, Jiayuan Wu, and Zaiwen Wen. Lmask: Learn to solve constrained routing problems with lazy masking. _arXiv preprint arXiv:2505.17938_ , 2025b. 

- Fei Liu, Xialiang Tong, Mingxuan Yuan, Xi Lin, Fu Luo, Zhenkun Wang, Zhichao Lu, and Qingfu Zhang. Evolution of heuristics: Towards efficient automatic algorithm design using large language model. In _41st International Conference on Machine Learning (ICML 2024)_ , pp. 32201–32223. ML Research Press, 2024a. 

- Shengcai Liu, Caishun Chen, Xinghua Qu, Ke Tang, and Yew-Soon Ong. Large language models as evolutionary optimizers. In _2024 IEEE Congress on Evolutionary Computation (CEC)_ , pp. 1–8. IEEE, 2024b. 

- Fu Luo, Xi Lin, Fei Liu, Qingfu Zhang, and Zhenkun Wang. Neural combinatorial optimization with heavy decoder: Toward large scale generalization. In _NeurIPS_ , 2023. 

- Yining Ma, Zhiguang Cao, and Yeow Meng Chee. Learning to search feasible and infeasible regions of routing problems with flexible neural k-opt. _Advances in Neural Information Processing Systems_ , 36:49555–49578, 2023. 

- Zeyuan Ma, Yue-Jiao Gong, Hongshu Guo, Jiacheng Chen, Yining Ma, Zhiguang Cao, and Jun Zhang. Llamoco: Instruction tuning of large language models for optimization code generation. _IEEE Transactions on Evolutionary Computation_ , 2026. 

- Aman Madaan, Niket Tandon, Prakhar Gupta, Skyler Hallinan, Luyu Gao, Sarah Wiegreffe, Uri Alon, Nouha Dziri, Shrimai Prabhumoye, Yiming Yang, et al. Self-refine: Iterative refinement with self-feedback. _Advances in Neural Information Processing Systems_ , 36:46534–46594, 2023. 

12 

Published as a conference paper at ICLR 2026 

- OpenAI. Gpt-4 technical report. https://arxiv.org/abs/2303.08774, 2024. Accessed: 2025-09-18. 

- Wenbin Ouyang, Sirui Li, Yining Ma, and Cathy Wu. Learning to segment for capacitated vehicle routing problems. _arXiv preprint arXiv:2507.01037_ , 2025. 

- Wenzheng Pan, Hao Xiong, Jiale Ma, Wentao Zhao, Yang Li, and Junchi Yan. UniCO: On unified combinatorial optimization via problem reduction to matrix-encoded general TSP. In _The Thirteenth International Conference on Learning Representations_ , 2025. 

- Gerhard Reinelt. TSPLIB—A traveling salesman problem library. _ORSA journal on computing_ , 3 (4):376–384, 1991. 

- Jacques Renaud, Fayez F Boctor, and Gilbert Laporte. A fast composite heuristic for the symmetric traveling salesman problem. _INFORMS Journal on computing_ , 8(2):134–143, 1996. 

- Bernardino Romera-Paredes, Mohammadamin Barekatain, Alexander Novikov, Matej Balog, M Pawan Kumar, Emilien Dupont, Francisco JR Ruiz, Jordan S Ellenberg, Pengming Wang, Omar Fawzi, et al. Mathematical discoveries from program search with large language models. _Nature_ , 625(7995):468–475, 2024. 

- Michael Schneider, Andreas Stenger, and Dominik Goeke. The electric vehicle-routing problem with time windows and recharging stations. _Transportation science_ , 48(4):500–520, 2014. 

- Zhiqing Sun and Yiming Yang. Difusco: Graph-based diffusion solvers for combinatorial optimization. _Advances in neural information processing systems_ , 36:3706–3731, 2023. 

- Eduardo Uchoa, Diego Pecin, Artur Pessoa, Marcus Poggi, Thibaut Vidal, and Anand Subramanian. New benchmark instances for the capacitated vehicle routing problem. _European Journal of Operational Research_ , 257(3):845–858, 2017. 

- Thibaut Vidal. Hybrid genetic search for the CVRP: Open-source implementation and swap* neighborhood. _Computers & Operations Research_ , 140:105643, 2022. 

- Oriol Vinyals, Meire Fortunato, and Navdeep Jaitly. Pointer networks. In _NeurIPS_ , volume 28, 2015. 

- Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia, Ed Chi, Quoc V Le, Denny Zhou, et al. Chain-of-thought prompting elicits reasoning in large language models. _Advances in neural information processing systems_ , 35:24824–24837, 2022. 

- Yixuan Weng, Minjun Zhu, Fei Xia, Bin Li, Shizhu He, Shengping Liu, Bin Sun, Kang Liu, and Jun Zhao. Large language models are better reasoners with self-verification. _arXiv preprint arXiv:2212.09561_ , 2022. 

- Niels A Wouda, Leon Lan, and Wouter Kool. PyVRP: A high-performance VRP solver package. _INFORMS Journal on Computing_ , 36(4):943–955, 2024. 

- Yaoxin Wu, Wen Song, Zhiguang Cao, Jie Zhang, and Andrew Lim. Learning improvement heuristics for solving routing problems. _IEEE transactions on neural networks and learning systems_ , 33(9):5057–5069, 2021. 

- Chengrun Yang, Xuezhi Wang, Yifeng Lu, Hanxiao Liu, Quoc V Le, Denny Zhou, and Xinyun Chen. Large language models as optimizers. In _International Conference on Learning Representations_ , 2024. 

- Haoran Ye, Jiarui Wang, Zhiguang Cao, Federico Berto, Chuanbo Hua, Haeyeon Kim, Jinkyoo Park, and Guojie Song. ReEvo: Large language models as hyper-heuristics with reflective evolution. _Advances in neural information processing systems_ , 37:43571–43608, 2024. 

- Haifei Zhang, Hongwei Ge, Jinlong Yang, and Yubing Tong. Review of vehicle routing problems: Models, classification and solving algorithms. _Archives of Computational Methods in Engineering_ , 29(1):195–221, 2022. 

13 

Published as a conference paper at ICLR 2026 

- Ni Zhang and Zhiguang Cao. Hybrid-balance gflownet for solving vehicle routing problems. In _Advances in Neural Information Processing Systems_ , 2025. 

- Wayne Xin Zhao, Kun Zhou, Junyi Li, Tianyi Tang, Xiaolei Wang, Yupeng Hou, Yingqian Min, Beichen Zhang, Junjie Zhang, Zican Dong, et al. A survey of large language models. _arXiv preprint arXiv:2303.18223_ , 2023. 

- Zhi Zheng, Zhuoliang Xie, Zhenkun Wang, and Bryan Hooi. Monte carlo tree search for comprehensive exploration in llm-based automatic heuristic design. In _Forty-second International Conference on Machine Learning_ , 2025. 

- Jianan Zhou, Yaoxin Wu, Wen Song, Zhiguang Cao, and Jie Zhang. Towards omni-generalizable neural methods for vehicle routing problems. In _International Conference on Machine Learning_ , pp. 42769–42789, 2023. 

- Jianan Zhou, Zhiguang Cao, Yaoxin Wu, Wen Song, Yining Ma, Jie Zhang, and Xu Chi. MVMoE: Multi-task vehicle routing solver with mixture-of-experts. In _International Conference on Machine Learning_ , pp. 61804–61824. PMLR, 2024. 

- Jianghan Zhu, Yaoxin Wu, Zhuoyi Lin, Zhengyuan Zhang, Haiyan Yin, Zhiguang Cao, Senthilnath Jayavelu, and Xiaoli Li. Bridging synthetic and real routing problems via llm-guided instance generation and progressive adaptation. In _AAAI_ , 2026. 

14 

Published as a conference paper at ICLR 2026 

|A|PPEN|DIX||
|---|---|---|---|
|**A **|**Rela**|**ted Work**|**16**|
||A.1|ML for VRPs . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . .<br>16|
||A.2|LLM for VRPs<br>. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . .<br>16|
|**B**|**Pro**|**blem Statement**|**17**|
|**C **|**Sup**|**plementary Methodology and Experimental Details**|**24**|
||C.1|VRPLib Component<br>. . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . .<br>24|
||C.2|Destroy Strategy<br>. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . .<br>24|
||C.3|Simulated Annealing Criterion . . . . . . . . . . . . . . . . . . . . . . . .|. . . .<br>24|
||C.4|Code Generation Time Analysis<br>. . . . . . . . . . . . . . . . . . . . . . .|. . . .<br>26|
||C.5|Comparison on 48 Standard Benchmark . . . . . . . . . . . . . . . . . . .|. . . .<br>26|
||C.6|Details of Comparison of Code Reliability and Solution Feasibility . . . . .|. . . .<br>26|
||C.7|Comparison on ATSP Benckmark<br>. . . . . . . . . . . . . . . . . . . . . .|. . . .<br>27|
||C.8|Comparison on ACVRP Benckmark . . . . . . . . . . . . . . . . . . . . .|. . . .<br>27|
||C.9|Comparison on SOP Benckmark . . . . . . . . . . . . . . . . . . . . . . .|. . . .<br>29|
||C.10|AFL’s Sensitivity to Different LLMs . . . . . . . . . . . . . . . . . . . . .|. . . .<br>29|
||C.11|Experiment on Different Input Format . . . . . . . . . . . . . . . . . . . .|. . . .<br>29|
||C.12|Experiment on Large CVRP Instances . . . . . . . . . . . . . . . . . . . .|. . . .<br>30|
|**D **|**Exa**|**mples of Prompts and Outputs**|**31**|
||D.1|Subtask 1: Problem Description<br>. . . . . . . . . . . . . . . . . . . . . . .|. . . .<br>31|
|||D.1.1<br>Generation Agent(GA) . . . . . . . . . . . . . . . . . . . . . . . .|. . . .<br>31|
|||D.1.2<br>Judgment Agent (JA) . . . . . . . . . . . . . . . . . . . . . . . . .|. . . .<br>33|
|||D.1.3<br>Revision Agents (RA)<br>. . . . . . . . . . . . . . . . . . . . . . . .|. . . .<br>34|
||D.2|Subtask 2: Code Generation<br>. . . . . . . . . . . . . . . . . . . . . . . . .|. . . .<br>36|
|||D.2.1<br>Generation Agent (GA) . . . . . . . . . . . . . . . . . . . . . . . .|. . . .<br>36|
|||D.2.2<br>Judgment Agent (JA) . . . . . . . . . . . . . . . . . . . . . . . . .|. . . .<br>38|
|||D.2.3<br>Revision Agent (RA) . . . . . . . . . . . . . . . . . . . . . . . . .|. . . .<br>40|
||D.3|Subtask 3: Solution Derivation . . . . . . . . . . . . . . . . . . . . . . . .|. . . .<br>40|
|||D.3.1<br>Error Analysis Agents (EAA)<br>. . . . . . . . . . . . . . . . . . . .|. . . .<br>40|
|**E**|**The**|**Use of Large Language Models**|**41**|



15 

Published as a conference paper at ICLR 2026 

## A RELATED WORK 

### A.1 ML FOR VRPS 

Existing neural approaches to solving VRPs generally follow two directions: learning to construct and learning to improve them. In the construction paradigm, a model either directly generates a feasible solution (Vinyals et al., 2015; Bello et al., 2017) or produces a probability heatmap (Joshi et al., 2021; Sun & Yang, 2023) from which a solution is sampled. AM (Kool et al., 2018) first introduces attention mechanisms for VRPs, and POMO (Kwon et al., 2020) subsequently exploits multiple optima to enhance solution quality, inspiring a series of extensions and refinements (Drakulic et al., 2023; Luo et al., 2023; Berto et al., 2025a; Zhang & Cao, 2025). Recently, increasing attention has been devoted to improving generalization (Joshi et al., 2022; Zhou et al., 2023; Gao et al., 2024) and scalability (Li et al., 2021; Ouyang et al., 2025), addressing complex constraints (Bi et al., 2024; Li et al., 2025b), and handling multiple VRP variants within a single framework (Zhou et al., 2024; Berto et al., 2025b; Pan et al., 2025), though these efforts still fall short of practical deployment. In the improvement paradigm, an initial solution is iteratively refined using learned local-search (Wu et al., 2021; Ma et al., 2023) or destroy–repair strategies (Hottung & Tierney, 2022) to progressively reduce cost and enhance solution quality. 

### A.2 LLM FOR VRPS 

One line of work uses LLMs to directly generate or improve VRP solutions. For example, OPRO (Yang et al., 2024) attempts to construct solutions outright with an LLM, LEMA (Liu et al., 2024b) leverages the LLM to perform the genetic search itself, and Jiang et al. (2025a) finetune LLM to construct in the end to end manner. However, they fall short in terms of solution quality and feasibility. Another line of research applies LLMs to generate code for VRPs, which can be broadly categorized into two directions: evolving basic heuristics for conventional VRPs and developing general frameworks for complex VRPs. 

In _evolving basic heuristics_ , LLMs are employed to iteratively evolve a simple or existing heuristic within fixed templates or established solvers for conventional VRPs. Early work such as EOH (Liu et al., 2024a) adopts a population-based framework with fixed templates for heuristic evolution. ReEvo (Ye et al., 2024) further combines evolutionary search with LLM reflections to provide verbal feedback and enhance search efficiency. More recently, HSEvo (Dat et al., 2025) and MCTSAHD (Zheng et al., 2025) have advanced this line of research. Zhu et al. (2026) uses evolution framework to bridge synthetic and real routing problems. However, these approaches remain tailored to specific problems, limiting their generality across VRP variants with practical constraints. 

In _developing general frameworks_ , LLMs are leveraged as knowledgeable developers to generate function modules with distinct roles, enabling the framework to address diverse and complex VRPs. In ARS (Li et al., 2025a) and DRoC (Jiang et al., 2025b), LLMs generate specific functions to adapt frameworks to different variants, typically relying on handcrafted modules or external solvers. However, aligning LLM-generated code with these components remains challenging. In ARS, the integration between the LLM and the base algorithm is weak: the handcraft improvement operator and the constraint validation functions generated by the LLM are decoupled, and feasibility can only be verified after optimization, often leading to infeasible solutions. In DRoC, the LLM produces code that invokes OR-Tools without genuine knowledge of its internals, relying instead on external retrieval, which may undermine code reliability and reduce solution feasibility. In contrast, SGE (Iklassov et al., 2024) eliminates the need for predefined modules or solvers by directly generating code end-to-end. However, due to the inherent complexity of full code generation and the absence of effective constraint-handling mechanisms, its applicability is restricted to TSP. Moreover, it still depends on handcrafted extraction of instance information (e.g., inputs and constraints), and its overall performance remains uncompetitive. 

In this paper, we address these limitations by proposing a general framework of collaborative LLMempowered agents that can tackle complex VRPs with self-containment, full automation, and high trustworthiness in both code and solutions. 

16 

Published as a conference paper at ICLR 2026 

Table 7: Constraint composition of VRP variants. 

|_VRP Variant_|**Capacity**<br>(C)|**Open Route**<br>(O)|**Backhaul**<br>(B)|**Mixed Backhaul**<br>(MB)|**Duration Limit**<br>(L)|**Time Windows**<br>(TW)|**Multi depot**<br>(MD)|**Electric Vehicle**<br>(E)|
|---|---|---|---|---|---|---|---|---|
|CVRP|✓||||||||
|OCVRP|✓|✓|||||||
|CVRPB|✓<br>||✓||||||
|CVRPL<br>|✓<br>||||✓||||
|CVRPTW|✓|||||✓|||
|OCVRPTW|✓<br>|✓<br>||||✓|||
|OCVRPB|✓|✓|✓||||||
|OCVRPL|✓|✓|||✓||||
|CVRPBL|✓||✓||✓||||
|CVRPBTW|✓||✓|||✓|||
|CVRPLTW|✓||||✓|✓|||
|OCVRPBL<br>|✓<br>|✓<br>|✓<br>||✓||||
|OCVRPBTW|✓|✓|✓|||✓|||
|OCVRPLTW|✓|✓|||✓|✓|||
|CVRPBLTW|✓||✓||✓|✓|||
|OCVRPBLTW|✓|✓|✓||✓|✓|||
|CVRPMB|✓|||✓|||||
|OCVRPMB|✓|✓||✓|||||
|CVRPMBL|✓|||✓|✓||||
|CVRPMBTW|✓|||✓||✓|||
|OCVRPMBL|✓|✓||✓|✓||||
|OCVRPMBTW|✓|✓||✓||✓|||
|CVRPMBLTW|✓|||✓|✓|✓|||
|OCVRPMBLTW|✓|✓||✓|✓|✓|||
|MDCVRP|✓||||||✓||
|MDOCVRP|✓|✓|||||✓||
|MDCVRPB<br>|✓<br>||✓||||✓<br>||
|MDCVRPL|✓||||✓||✓||
|MDCVRPTW|✓|||||✓|✓||
|MDOCVRPB|✓|✓|✓||||✓||
|MDOCVRPL|✓|✓|||✓||✓||
|MDOCVRPTW|✓|✓||||✓|✓||
|MDOCVRPBL|✓|✓|✓||✓||✓||
|MDOCVRPBTW|✓|✓|✓|||✓|✓||
|MDOCVRPLTW|✓|✓|||✓|✓|✓||
|MDCVRPMB|✓|||✓|||✓||
|MDCVRPMBL|✓|||✓|✓||✓||
|MDCVRPMBTW|✓|||✓||✓|✓||
|MDOCVRPMB|✓|✓||✓|||✓||
|MDOCVRPMBL|✓|✓||✓|✓||✓||
|MDOCVRPMBTW|✓|✓||✓||✓|✓||
|MDCVRPMBLTW|✓|||✓|✓|✓|✓||
|MDOCVRPMBLTW|✓|✓||✓|✓|✓|✓||
|ECVRP|✓|||||||✓|
|ECVRPL|✓||||✓|||✓|
|ECVRPTW|✓|||||✓||✓|
|EOCVRP|✓|✓||||||✓|
|ECVRPLTW|✓||||✓|✓||✓|
|EOCVRPL|✓|✓|||✓|||✓|
|EOCVRPTW|✓|✓||||✓||✓|
|EOCVRPLTW|✓|✓|||✓|✓||✓|



## B PROBLEM STATEMENT 

The connections between different VRP variants and their associated constraints are illustrated in Table 7. We further provide detailed descriptions of several representative variants as follows. 

### 1. CVRP 

- **Problem Type:** CVRP. 

- **Description:** The Capacitated Vehicle Routing Problem (CVRP) involves determining optimal routes for a fleet of vehicles to deliver goods to a set of customers while minimizing total distance traveled and ensuring that vehicle capacity is not exceeded. 

- **Constraints:** _Capacity_ – the total demand on any route cannot exceed vehicle capacity. _Visit_ – each customer is visited exactly once. _Depot_ – every route starts and ends at the depot. 

- **Input:** _depot_ , _node coordinates_ , _demands_ , _capacity_ . 

- **Output:** A set of vehicle routes, each beginning and ending at the depot, visiting every customer exactly once while respecting capacity constraints. 

17 

Published as a conference paper at ICLR 2026 

- **Objective:** Minimize the total travel distance. 

### 2. CVRPL 

- **Problem Type:** CVRPL. 

- **Description:** The Capacitated Vehicle Routing Problem with a Distance Limit (CVRPL) involves optimizing routes for a fleet of vehicles with a fixed capacity, ensuring deliveries are made while adhering to a constraint on the maximum route distance, while all routes must start and end at a common depot. 

- **Constraints:** _Capacity_ – vehicles have limited capacity for carrying goods. _Distance Limit_ – the total travel distance of each route must not exceed the specified maximum. _Visit_ – each customer is visited exactly once. _Depot_ – all routes must start and end at the fixed depot. 

- **Input:** _depot_ , _node coordinates_ , _demands_ , _capacity_ , _distance_ _~~l~~ imit_ . 

- **Output:** A set of feasible vehicle routes, each beginning and ending at the depot, visiting every customer exactly once while respecting both capacity and maximum-distance constraints. 

- **Objective:** Minimize the total travel distance. 

### 3. CVRPTW 

- **Problem Type:** CVRPTW. 

- **Description:** The problem is about optimizing delivery routes for a fleet of vehicles to serve a set of customers, considering time windows and vehicle capacity constraints. Each customer must be visited within a specific time frame and vehicles have limited capacity for deliveries. 

- **Constraints:** _Capacity_ – vehicles have limited capacity for deliveries. _Time Windows_ – customers must be served within specified time intervals. _Visit_ – every customer is visited exactly once. _Depot_ – every route starts and ends at the depot. 

- **Input:** _depot_ , _node coordinates_ , _demands_ , _capacity_ , _service_ _~~t~~ imes_ , _time_ _~~w~~ indows_ . 

- **Output:** A set of vehicle routes, each beginning and ending at the depot, visiting every customer exactly once while satisfying vehicle capacity and customer time-window constraints. 

- **Objective:** Minimize the total travel distance. 

### 4. OCVRP 

- **Problem Type:** OCVRP. 

- **Description:** The Open Capacitated Vehicle Routing Problem (OCVRP) involves determining the optimal routes for a fleet of vehicles with limited capacity that start at a depot and must deliver goods to a set of customers without the obligation to return to the depot. 

- **Constraints:** _Capacity_ – vehicles have limited capacity. _Open Route_ – vehicles are not required to return to the depot after completing service. _Visit_ – each customer may only be visited once. _Depot_ – every route must start at the depot. 

- **Input:** _depot_ , _node coordinates_ , _demands_ , _capacity_ . 

- **Output:** A set of open vehicle routes, each starting at the depot and ending at a customer location, visiting every customer exactly once while satisfying the vehicle-capacity constraint. 

- **Objective:** Minimize the total travel distance. 

### 5. CVRPLTW 

- **Problem Type:** CVRPLTW. 

18 

Published as a conference paper at ICLR 2026 

- **Description:** The problem is a Capacitated Vehicle Routing Problem with a Distance Limit and Time Windows (CVRPLTW), where a fleet of vehicles is tasked with delivering goods to a set of customers, each with specific demand and time windows, while respecting the vehicles’ capacity and route limitations. 

- **Constraints:** _Capacity_ – vehicles have limited capacity. _Distance Limit_ – each route has a maximum distance. _Time Windows_ – customers must be served within specified time intervals. _Visit_ – every customer is visited exactly once. _Depot_ – every route starts and ends at the depot. 

- **Input:** _depot_ , _node_ _~~c~~ oordinates_ , _demands_ , _capacity_ , _service_ _~~t~~ imes_ , _time_ _~~w~~ indows_ , _distance_ _~~l~~ imit_ . 

- **Output:** A set of feasible vehicle routes, each beginning and ending at the depot, visiting every customer exactly once while satisfying capacity, distance-limit, and time-window constraints. 

- **Objective:** Minimize the total travel distance. 

### 6. OCVRPL 

- **Problem Type:** OCVRPL. 

- **Description:** The problem is a variant of the Open Capacitated Vehicle Routing Problem with a Distance Limit (OCVRPL), where vehicles must deliver goods to various customers while adhering to a capacity limitation and a maximum route distance, without the requirement to return to a depot. 

- **Constraints:** _Capacity_ – vehicles have limited capacity for the amount of goods they can transport. _Distance Limit_ – each route has a maximum distance that vehicles must not exceed. _Open Route_ – vehicles do not return to the depot after their delivery routes. _Visit_ – each customer is visited only once. _Depot_ – routes must start at the depot, specifically at the designated location. 

- **Input:** _depot_ , _node coordinates_ , _demands_ , _capacity_ , _distance_ _~~l~~ imit_ . 

- **Output:** A set of open vehicle routes, each starting at the depot and ending at a customer location, visiting every customer exactly once while satisfying capacity and distance-limit constraints. 

- **Objective:** Minimize the total travel distance. 

### 7. OCVRPTW 

   - **Problem Type:** OCVRPTW. 

   - **Description:** The Open Capacitated Vehicle Routing Problem with Time Windows (OCVRPTW) involves determining optimal routes for a fleet of vehicles with limited capacity that service a set of customers with specific time windows, without the requirement for vehicles to return to the depot after completing their deliveries. 

   - **Constraints:** _Capacity_ – the total demand on any route cannot exceed vehicle capacity. _Time Windows_ – customers must be served within specified time intervals. _Open Route_ – vehicles do not return to the depot. _Visit_ – each customer may only be visited once. _Depot_ – every route must start at the depot. 

   - **Input:** _depot_ , _node coordinates_ , _demands_ , _capacity_ , _service_ _~~t~~ imes_ , _time_ _~~w~~ indows_ . 

   - **Output:** A set of feasible open vehicle routes, each starting at the depot and ending at a customer location, visiting every customer exactly once while satisfying capacity, servicetime, and time-window constraints. 

   - **Objective:** Minimize the total travel distance. 

8. OCVRPLTW 

   - **Problem Type:** OCVRPLTW. 

19 

Published as a conference paper at ICLR 2026 

- **Description:** The Open Capacitated Vehicle Routing Problem with Distance Limit and Time Windows (OCVRPLTW) requires planning optimal routes for a fleet of vehicles with limited carrying capacity to serve customers within specified time windows, while each route must also satisfy a maximum travel-distance limit and vehicles are not required to return to the depot after their final delivery. 

- **Constraints:** _Capacity_ – the total demand on any route cannot exceed vehicle capacity. _Distance Limit_ – each route’s total travel distance must not exceed the specified maximum. _Time Windows_ – customers must be served within their given time intervals. _Open Route_ – vehicles do not return to the depot after completing service. _Visit_ – each customer is visited exactly once. _Depot_ – every route must start at the depot. 

- **Input:** _depot_ , _node_ _~~c~~ oordinates_ , _demands_ , _capacity_ , _service_ _~~t~~ imes_ , _time_ _~~w~~ indows_ , _distance_ _~~l~~ imit_ . 

- **Output:** A set of feasible open vehicle routes, each starting at the depot and ending at a customer location, visiting every customer exactly once while satisfying capacity, timewindow, and distance-limit constraints. 

- **Objective:** Minimize the total travel distance. 

### 9. ECVRP 

- **Problem Type:** ECVRP. 

- **Description:** Electric Capacitated Vehicle Routing Problem (ECVRP) involves determining optimal routes for a fleet of electric vehicles to serve a set of customer demands, considering vehicle load capacity and battery (fuel) constraints, where recharging is available at designated charging stations. Each route starts and ends at the depot and each customer is to be visited exactly once. 

- **Constraints:** _Electricity_ – Each vehicle has a limited battery, consumes energy proportional to distance, and may recharge only at designated charging stations, with charging time affecting feasibility. _Capacity_ – Each vehicle has a maximum load capacity. _Depot_ – Each route must start and end at the depot. _Visit_ - Each customer must be visited exactly once. 

- **Input:** _depot_ , _node_ _~~c~~ oordinates_ , _demands_ , _capacity_ , _fuel_ _~~c~~ apacity_ , _fuel_ _~~c~~ onsumption_ _~~r~~ ate_ , _refuel_ _~~r~~ ate_ , _stations_ . 

- **Output:** A set of feasible vehicle routes, each starting and ending at the depot, visiting each customer exactly once, specifying the visiting order and any charging station stops, such that vehicle capacity and battery constraints are satisfied. 

- **Objective:** Minimize the total travel distance. 

### 10. ECVRPL 

- **Problem Type:** ECVRPL. 

- **Description:** Electric Vehicle Capacitated Vehicle Routing Problem with distance limit: find the set of routes for electric vehicles, starting and ending at the depot, that serve all customers without exceeding vehicle capacity, electric fuel capacity, and an explicit route distance limit. Electricity is managed with fuel consumption, battery recharging at stations, and recharging time affects route scheduling. 

- **Constraints:** _Electricity_ – electric vehicles have limited battery, fuel consumption rate, designated charging stations, and recharging time which constrain feasible routes. _Capacity_ – vehicles have a maximum load they can carry at one time. _Distance Limit_ –each route cannot exceed a maximum distance. _Visit_ – each customer is visited exactly once. _Depot_ – all routes must start and end at the depot. 

- **Input:** _depot_ , _node_ _~~c~~ oordinates_ , _demands_ , _capacity_ , _distance_ _~~l~~ imit_ , _fuel_ _~~c~~ apacity_ , _fuel_ _~~c~~ onsumption_ _~~r~~ ate_ , _refuel_ _~~r~~ ate_ , _stations_ . 

- **Output:** a set of vehicle routes, each starting and ending at the depot, visiting every customer exactly once while satisfying capacity, distance-limit, and electric-vehicle energy constraints, including recharging stops if required. 

20 

Published as a conference paper at ICLR 2026 

- **Objective:** Minimize the total travel distance. 

### 11. ECVRPTW 

- **Problem Type:** ECVRPTW. 

- **Description:** the Electric Capacitated Vehicle Routing Problem with Time Windows (ECVRPTW) constructs least-cost routes for a fleet of electric vehicles, each starting and ending at the depot, to serve all customers exactly once within specified time windows, considering both vehicle load capacity and electric battery (fuel) constraints; vehicles may recharge at designated charging stations, and service at each customer takes a specified time. 

- **Constraints:** _Electricity_ – Electric vehicles have limited battery capacity, consume energy proportional to travel distance, may recharge at specified stations, and recharging duration depends on refuel rate. _Time Windows_ – Customers must be served within predetermined time intervals. _Capacity_ – Each vehicle has limited load capacity. _Visit_ – Each customer is visited exactly once. _Depot_ – Every route must start and end at the depot. 

- **Input:** _depot_ , _node_ _~~c~~ oordinates_ , _demands_ , _capacity_ , _service_ _~~t~~ imes_ , _time_ _~~w~~ indows_ , _fuel_ _~~c~~ apacity_ , _fuel_ _~~c~~ onsumption_ _~~r~~ ate_ , _refuel_ _~~r~~ ate_ , _stations_ . 

- **Output:** A set of feasible vehicle routes, each starting and ending at the depot, visiting every customer exactly once while satisfying capacity, time-window, and electric-vehicle energy constraints, including necessary recharging stops. 

- **Objective:** Minimize the total travel distance. 

### 12. EOCVRP 

- **Problem Type:** EOCVRP. 

- **Description:** the Electric Open Capacitated Vehicle Routing Problem plans routes for a fleet of electric vehicles, where each vehicle starts at the depot, serves customer demands, may recharge at designated charging stations, does not need to return to the depot (open route), and respects vehicle capacity and battery limits. Each customer is visited exactly once. 

- **Constraints:** _Electricity_ – vehicles have limited battery capacity, consume energy with travel, and may recharge at stations, considering recharging time. _Capacity_ – vehicle loads cannot exceed their capacity. _Open Route_ – vehicles are not required to return to the depot. _Distance Limit_ – each route has a maximum allowed travel distance. _Visit_ – each customer must be visited exactly once. _Depot_ – each route starts at the depot. 

- **Input:** _depot_ , _node_ _~~c~~ oordinates_ , _demands_ , _capacity_ , _distance_ _~~l~~ imit_ , _fuel_ _~~c~~ apacity_ , _fuel_ _~~c~~ onsumption_ _~~r~~ ate_ , _refuel_ _~~r~~ ate_ , _stations_ . 

- **Output:** a set of feasible open vehicle routes starting at the depot, each serving a subset of customers exactly once, possibly using charging stations, and ending at any node, such that all routes meet capacity, battery, and problem constraints 

- **Objective:** Minimize the total travel distance. 

### 13. ECVRPLTW 

- **Problem Type:** ECVRPLTW. 

- **Description:** Electric Capacitated Vehicle Routing Problem with Time Windows (ECVRPTW) involves designing routes for a fleet of electric vehicles to deliver goods to customers, respecting vehicle capacity limits, electric battery/range constraints, maximum route distance, and customer-specific time windows. Each customer must be visited exactly once, and all routes must start and end at the depot. Vehicles may need to recharge at designated stations as part of their routes. 

- **Constraints:** _Electricity_ – electric vehicles have limited battery (fuel) capacity, must recharge at stations as needed, and recharging consumes time. _Capacity_ – each vehicle has a limited payload capacity. _Distance Limit_ – each route has a maximum distance. _Time Windows_ – customers must be served within given time intervals. _Visit_ – each customer can be visited only once. _Depot_ – each route must start and end at the depot. 

21 

Published as a conference paper at ICLR 2026 

- **Input:** _depot_ , _node_ _~~c~~ oordinates_ , _demands_ , _capacity_ , _service_ _~~t~~ imes_ , _time_ _~~w~~ indows_ , _distance_ _~~l~~ imit_ , _fuel_ _~~c~~ apacity_ , _fuel_ _~~c~~ onsumption_ _~~r~~ ate_ , _refuel_ _~~r~~ ate_ , _stations_ . 

- **Output:** A set of feasible vehicle routes, each represented as an ordered list of nodes (customers, stations, and depot), with associated service start times and charging operations, where each route starts and ends at the depot, all customers are visited exactly once within their time windows, and all constraints on capacity, time window, fuel, route length, and recharging are satisfied. 

- **Objective:** Minimize the total travel distance. 

### 14. EOCVRPL 

- **Problem Type:** EOCVRPL. 

- **Description:** the Electric Vehicle Open Capacitated Vehicle Routing Problem involves electric vehicles with limited load and battery capacity, serving customers starting from the depot without needing to return (open route). Vehicles can recharge at charging stations, and each customer is visited at most once.”, 

- **Constraints:** _Electricity_ – Vehicles have a limited electric battery, consumed proportionally to travel; vehicles may recharge at designated stations. _Capacity_ – Vehicles have a maximum load they can carry. _Open Route_ – Vehicles do not need to return to the depot after serving customers. _Distance Limit_ – Each route has a maximum allowable distance. _Visit_ – Each customer is visited at most once. _Depot_ – Routes start at the depot.. 

- **Input:** _depot_ , _node_ _~~c~~ oordinates_ , _demands_ , _capacity_ , _distance_ _~~l~~ imit_ , _fuel_ _~~c~~ apacity_ , _fuel_ _~~c~~ onsumption_ _~~r~~ ate_ , _refuel_ _~~r~~ ate_ , _stations_ . 

- **Output:** A set of feasible open vehicle routes starting from the depot, where each route serves a subset of customers, may include recharging stops at stations as needed, and satisfies all capacity, distance, fuel, and visit constraints, ensuring each customer is visited at most once. 

- **Objective:** Minimize the total travel distance. 

### 15. EOCVRPTW 

- **Problem Type:** EOCVRPTW. 

- **Description:** Electric Open Capacitated Vehicle Routing Problem with Time Windows: The goal is to design minimum-cost routes for a fleet of electric vehicles that start from a depot, serve each customer exactly once within specified time windows, while observing vehicle capacity, electric battery limitations (with possible recharging at stations), and vehicles are not required to return to the depot. 

- **Constraints:** _Electricity_ – Vehicles have limited battery, consume energy with distance, and may recharge at designated stations. _Capacity_ – Each vehicle has a fixed carrying capacity. _Time Windows_ – Customers must be serviced within specific time intervals. _Open Route_ – Vehicles do not return to the depot after serving customers. _Visit_ – Each customer must be visited exactly once. _Depot_ – Routes start from the depot. 

- **Input:** _depot_ , _node_ _~~c~~ oordinates_ , _demands_ , _capacity_ , _service_ _~~t~~ imes_ , _time_ _~~w~~ indows_ , _fuel_ _~~c~~ apacity_ , _fuel_ _~~c~~ onsumption_ _~~r~~ ate_ , _refuel_ _~~r~~ ate_ , _stations_ . 

- **Output:** a set of feasible vehicle routes where each route starts at the depot, visits each customer exactly once within their specified time windows and service times, respects vehicle capacity and battery constraints with possible recharging at stations, and does not return to the depot. 

- **Objective:** Minimize the total travel distance. 

### 16. EOCVRPLTW 

- **Problem Type:** EOCVRPLTW. 

- **Description:** Electric Open Capacitated Vehicle Routing Problem with Distance Limit and Time Windows. In this problem, a fleet of electric vehicles with limited cargo and battery 

22 

Published as a conference paper at ICLR 2026 

capacity must serve customers, each within specified distance limit and time windows. Vehicles start at the depot but do not return (open routes), must visit each customer exactly once, can recharge only at designated charging stations, and each route has a maximum allowable distance. 

- **Constraints:** _Electricity_ – Electric vehicles have limited battery (fuel) capacity, fuel consumed proportionally to distance, can recharge at charging stations, and recharging takes time. _Capacity_ – Vehicles have limited cargo capacity. _Distance Limit_ – Each route has a maximum allowed distance. _Time Windows_ – Service at each customer must begin within its given time interval. _Open Route_ – Vehicles do not return to depot after serving customers. _Visit_ – Each customer must be visited exactly once. _Depot_ – every route must start at the depot. 

- **Input:** _depot_ , _node_ _~~c~~ oordinates_ , _demands_ , _capacity_ , _service_ _~~t~~ imes_ , _time_ _~~w~~ indows_ , _distance_ _~~l~~ imit_ , _fuel_ _~~c~~ apacity_ , _fuel_ _~~c~~ onsumption_ _~~r~~ ate_ , _refuel_ _~~r~~ ate_ , _stations_ . 

- **Output:** A set of feasible open vehicle routes, each starting at the depot, visiting every customer exactly once within their specified time windows, not exceeding vehicle cargo capacity, route distance limits, or battery constraints (with recharging at stations as needed), and ensuring vehicles do not return to the depot. 

- **Objective:** Minimize the total travel distance. 

### 17. TSP 

- **Problem Type:** TSP. 

- **Description:** The Symmetric Traveling Salesman Problem is to find the shortest possible route that visits each node (drilling location) exactly once and returns to the starting point, typically used for optimizing routes such as drilling or circuit board manufacturing. 

- **Constraints:** _Visit_ – each node (location) must be visited exactly once. 

- **Input:** _node_ _~~c~~ oordinates_ . 

- **Output:** A single closed tour that begins and ends at one node and visits every node exactly once. 

- **Objective:** Minimize the total travel distance. 

### 18. ATSP 

- **Problem Type:** ATSP. 

- **Description:** The Asymmetric Traveling Salesman Problem (ATSP) generalizes the classical TSP by allowing the travel cost from node _i_ to node _j_ to differ from the cost from _j_ to _i_ . The goal is to find the shortest Hamiltonian cycle that visits every node exactly once and returns to the starting node when edge weights are direction-dependent. 

- **Constraints:** _Visit_ – each node must be visited exactly once. _Depot_ – the tour must start and end at the same node. _Asymmetry_ – travel costs or distances are not necessarily symmetric. 

- **Input:** _edge_ _~~w~~ eight_ _~~m~~ atrix_ . 

- **Output:** A single directed Hamiltonian cycle that begins and ends at one node and visits every node exactly once while respecting the asymmetric cost structure. 

- **Objective:** Minimize the total travel cost. 

### 19. ACVRP 

- **Problem Type:** ACVRP. 

- **Description:** Asymmetric Capacitated Vehicle Routing Problem (ACVRP): a fleet of vehicles with limited carrying capacity must start and end at a central depot and serve every customer exactly once, while accounting for direction-dependent travel costs. 

- **Constraints:** _Capacity_ – the total demand on any route cannot exceed the vehicle capacity. _Asymmetry_ – travel costs between two nodes are not necessarily equal in both directions. _Visit_ – each customer is visited exactly once. _Depot_ – every route must start and end at the depot. 

23 

Published as a conference paper at ICLR 2026 

- **Input:** _depot_ , _edge_ _~~w~~ eight_ _~~m~~ atrix_ , _demands_ , _capacity_ . 

- **Output:** A set of vehicle routes, each starting and ending at the depot, visiting every customer exactly once while satisfying vehicle-capacity constraints and accounting for direction-dependent travel costs. 

- **Objective:** Minimize the total travel cost. 

### 20. SOP 

- **Problem Type:** SOP. 

- **Description:** The Sequential Ordering Problem (SOP) is to find a minimum-cost Hamiltonian path that visits each node exactly once and respects given precedence constraints (some nodes must be visited before others), subject to forbidden arcs. 

- **Constraints:** _Precedence_ – Certain nodes must be visited before others, according to the instance’s precedence relations. _Forbidden Arcs_ – Some node-to-node connections are infeasible and cannot be used. _Visit_ – each node is visited exactly once (Hamiltonian path). 

- **Input:** _edge_ _~~w~~ eight_ _~~m~~ atrix_ , _precedence_ _~~c~~ onstraints_ , _forbidden_ _~~a~~ rcs_ . 

- **Output:** A minimum-cost Hamiltonian path visiting each node exactly once that satisfies all precedence constraints and forbidden arc constraints. 

- **Objective:** Minimize the total travel cost of the path. 

## C SUPPLEMENTARY METHODOLOGY AND EXPERIMENTAL DETAILS 

### C.1 VRPLIB COMPONENT 

Table 8 summarizes the main components of a VRPLIB instance file, presenting each required or optional field along with its description and an illustrative example. The “VRPLib Field” column lists the standard sections of a vehicle-routing problem instance (e.g., NAME/COMMENT, TYPE, DIMENSION). The Description column explains the meaning of each section, while the Example column provides typical syntax drawn from a sample instance (for example, TYPE : CVRP, CAPACITY : 200), showing the exact formatting used in VRPLIB files. 

### C.2 DESTROY STRATEGY 

As the algorithm shown in Algorithm 1, Given a solution _S_ , distance matrix _Dis_ , and ratio _ρ_ , the algorithm first determines the number of nodes _nrm_ to remove. A random customer _c_ is sampled, and a candidate list _L_ is formed by sorting all customers by distance to _c_ . Iteratively, a candidate _u_ is selected, and if its route has not been destroyed, a contiguous subsequence _Q_ including _u_ is randomly chosen and removed. The subsequence _Q_ is added to the removed set _R_ , and the corresponding route is updated and marked as destroyed. This process continues until _nrm_ customers are removed, yielding the residual solution _S_<sup>_′_</sup> and the removed set _R_ . 

### C.3 SIMULATED ANNEALING CRITERION 

The _Simulated Annealing (SA) criterion_ is a stochastic acceptance rule inspired by the physical annealing process, where a material is gradually cooled to reach a low–energy crystalline state. In VRPs scenarios, it provides a mechanism to escape local minima by occasionally accepting solutions that are worse than the current one. 

Given a current solution with cost _E_ current and a candidate solution with cost _E_ new, the move is accepted if _E_ new _≤ E_ current; otherwise it is accepted with probability 



where _T_ is a temperature parameter that decreases according to a cooling schedule. In our implementation, _T_ is defined as 

where iteration denotes the total number of iterations and step is the current iteration index. 

24 

Published as a conference paper at ICLR 2026 

Table 8: Main sections of a VRPLIB instance file with descriptions and example. 

|**VRPLib Field**|**Description**|**Example**|
|---|---|---|
|NAME / COMMENT|Optional. Includes the instance name and op-<br>tional comments that can provide additional<br>context for AFL to understand the related<br>problem.|NAME : A-n32-k5<br>COMMENT : 32-node<br>Capacitated Vehicle<br>Routing Problem<br>instance.|
|TYPE|Optional.<br>Specifies the declared problem<br>type (e.g., CVRP, VRPTW, EVRP), serving<br>only as a reference for constraint extraction;<br>the actual problem characteristics must be<br>determined from the complete instance.|TYPE : CVRP|
|DIMENSION|Required. Total number of nodes including<br>both customers and depot(s).|DIMENSION : 33|
|EDGE WEIGHT TYPE|Required. Specifies how inter-node distances<br>are given: a metric (e.g., EUC 2D) or an ex-<br>plicit matrix.|EDGE WEIGHT TYPE : EUC<br>2D|
|NODE COORD SECTION|Required.<br>Lists coordinates of each node<br>(typically planar Euclidean).|NODE COORD SECTION:<br>1 45 68<br>2 37 52|
|DEMAND SECTION|Required for instances with a capacity (C)<br>constraint. Specifies the demand of each cus-<br>tomer node, typically measured in weight or<br>quantity units, where positive values denote<br>linehaul customers (delivery) and negative<br>values denote backhaul customers (pickup).|DEMAND SECTION:<br>1 0<br>2 15<br>3 -10|
|CAPACITY|Required for capacity-constrained (C) prob-<br>lems.<br>Defines the maximum load (e.g.,<br>weight or volume) each vehicle can carry.|CAPACITY : 200|
|DEPOT SECTION|Required for instances with depot constraint.<br>Identifies the depot node(s) where vehicles<br>start and optionally end their routes.|DEPOT SECTION:<br>1<br>-1|
|DISTANCE LIMIT|Required for instances with open route (O)<br>constraint. Specifies the maximum travel dis-<br>tance allowed for each route.|DISTANCE LIMIT : 500|
|TIME WINDOW SECTION|Required for instances with time window<br>(TW) constraint. Provides earliest and latest<br>allowable arrival times for each customer.|TIME WINDOW SECTION:<br>1 0 100<br>2 20 80|
|SERVICE TIME SECTION|Required for instances with time window<br>(TW) constraint.<br>Service time required at<br>each customer node; combined with travel<br>time to satisfy time-window constraints.|SERVICE TIME SECTION:<br>1 10<br>2 15|
|FUEL CAPACITY|Required for instances with electric vehicle<br>(E) constraint. Maximum energy or battery<br>capacity for each vehicle in electric-vehicle<br>routing problems.|FUEL CAPACITY : 300|
|FUEL CONSUMPTION RATE|Required for instances with electric vehicle<br>(E) constraint.<br>Energy consumed per dis-<br>tance unit.|FUEL CONSUMPTION RATE :<br>1.0|
|REFUEL RATE|Required for instances with electric vehicle<br>(E) constraint. Charging or refueling rate per<br>time unit at stations.|REFUEL RATE : 2.0|
|STATION SECTION|Required for instances with electric vehicle<br>(E) constraint. Identifies charging or refuel-<br>ing station nodes where vehicles can refuel.|STATION SECTION:<br>34<br>35|



25 

Published as a conference paper at ICLR 2026 

**Algorithm 1** Destroy Strategy 

- 1: **Input:** solution _S_ (set of routes), distance matrix _Dis_ , ratio _ρ_ 

- 2: **Output:** removed nodes _R_ , destroyed solution _S_<sup>_′_</sup> 

- 3: _R ←∅_ , _S_<sup>_′_</sup> _← S_ , _nrm ←⌊|C| · ρ⌋ ▷C_ : set of customers 4: _c ∼_ Uniform( _C_ ) _▷_ random sample center 

- 5: _L ←_ sort( _C, Dis_ ( _c, ·_ )) _▷_ sort candidate list by distance to _c_ 

- 6: **while** _|R| < nrm_ and _L̸_ = _∅_ **do** 

- 7: _u ←_ next( _L_ ); _r ←_ route( _u, S_<sup>_′_</sup> ) 

- 8: **if** _r_ already destroyed **then** 

- 9: **continue** 

- 10: **end if** 11: _Q ←_ subseq( _r, u_ ) _▷_ random select contiguous subsequence including _u_ 12: _r ← r \ Q_ , _R ← R ∪ Q ▷_ update _r_ by excluding _Q_ and extend _R_ with _Q_ 

- 13: **end while** 

- 14: **return** ( _R, S_<sup>_′_</sup> ) 

Table 9: Gap comparison across different prompting strategies. 

||CV|RP|VR|PL|VRP|TW|OV|RP|VRP|LTW|OV|RPL|OVR|PTW|OVR|PLTW|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||50|100|50|100|50|100|50|100|50|100|50|100|50|100|50|100|
|Standard Prompt|11.76%|12.42%|–|–|5.11%|8.14%|10.60%|13.77%|4.58%|7.38%|14.59%|23.56%|–|–|–|–|
|Self-Refine|5.69%|8.83%|8.13%|12.12%|–|–|–|–|–|–|4.61%|6.79%|13.99%|18.90%|2.37%|6.02%|
|Self-Debug|11.76%|12.42%|–|–|5.11%|8.14%|10.60%|13.77%|4.58%|7.38%|14.59%|23.56%|43.39%|51.39%|12.57%|14.37%|
|Self-Verification|7.61%|9.47%|–|–|6.80%|8.64%|5.71%|9.25%|–|–|–|–|3.54%|5.96%|–|–|
|COT|8.39%|12.04%|7.37%|10.51%|–|–|56.84%|93.83%|–|–|62.06%|105.86%|–|–|–|–|
|AFL|**5.01%**|**6.66%**|**7.18%**|**10.08%**|**2.87%**|**4.64%**|**4.30%**|**6.58%**|**4.34%**|**7.14%**|**4.61%**|**6.68%**|**1.24%**|**2.54%**|**2.12%**|**4.02%**|



**Note:** – indicates cases where no runnable code or feasible solution could be obtained. 

### C.4 CODE GENERATION TIME ANALYSIS 

At first, we provide the runtime breakdown during testing phrase in Table 10. These results, as noted in Lines 350–351, measure the combined runtime for Problem Description and Solution Derivation over 1,000 test instances using the already generated codes. 

A detailed runtime breakdown of solver generation phase for the three subtasks: Problem Description, Code Generation, and Solution Derivation, across eight representative VRP variants, are shown in Table 10. These results reflect the time required to generate executable solver code and obtain a feasible solution for a single instance, where the generated code can be reused in the same VRP variant. As shown in Table 10, the code can be generated within approximately 30 minutes, which is notably shorter than the time typically required for human expert design, highlighting the model’s strong efficiency in producing high-quality, executable, and feasible solver code within a short time. 

In the Figure. 4, we explore the trade-off between solution quality and different number of solution refinement iterations. 

C.5 COMPARISON ON 48 STANDARD BENCHMARK 

The results of the all 48 standard VRP variants are presented in Table 11, derived from 1,000 instances with 100 nodes each. AFL achieves results within 3% of the SOTA baseline HGS-PyVRP in most problem settings. 

C.6 DETAILS OF COMPARISON OF CODE RELIABILITY AND SOLUTION FEASIBILITY 

**Runtime Error Rate (RER).** Let _V_ err be the number of generated programs that terminate with a runtime failure. The _Runtime Error Rate_ is calculated as 



where _V_ is the total number of generated programs across all VRP variants. A high RER indicates a large proportion of solutions that fail to execute due to logical flaws, or syntax mistakes. 

26 

Published as a conference paper at ICLR 2026 

Table 10: Runtime Analysis Across Testing Phase and Solver Generation Phase. 

|**Phase**|**Component**|**CVRP**|**CVRPL**<br>|**CVRPTW**|**OCVRP**|**CVRPLTW**|**OCVRPL**|**OCVRPTW**|**OCVRPLTW**|
|---|---|---|---|---|---|---|---|---|---|
|**Testing**|Problem Description|0.10|0.12|0.11|0.10|0.15|0.17|0.15|0.20|
||Solution Derivation|2.10|6.93|9.31|2.20|8.90|5.65|11.15|17.27|
||Problem Description|0.10|0.13|0.12|0.10|0.16|0.16|0.15|0.20|
|**Solver G**|**eneration**<br>Code Generation|12.28|12.88|18.38|23.94|27.43|28.20|24.85|30.50|
||Solution Derivation|0.003|1.05|0.009|0.005|1.10|1.21|0.010|1.42|
||Gapvs. T across Different|VRP Probl|ems|||Gapvs. T|ime across Diffe|rent VRP Problem|s|
|6<br>7|||~~Problem Type~~<br>CVRP<br>~~CVRPL~~<br>CVRPTW||6<br>7||||~~Problem Type~~<br>CVRP<br>~~CVRPL~~<br>CVRPTW<br>|
|4<br>5<br>(%)|||~~OCVRP~~<br>CVRPLTW||4<br>5<br>(%)||||~~OCVRP~~<br>CVRPLTW<br>|
|1<br>2<br>3<br><br>Gap|500<br>1000<br>2000<br>4000<br>T (Number of improveme|5000<br>nt iterations|8000<br>1000<br>)<br>OCVRPL<br>OCVRPTW<br>OCVRPLTW|0<br><br>|0.0<br>1<br>2<br>3<br>Gap|2.5<br>5.0|7.5<br><br>Time of Testing D|10.0<br>12.5<br>ataset(m)|15.0<br>17.5<br>OCVRPL<br>OCVRPTW<br>OCVRPLTW|



Figure 4: Comparison of solution quality across (a) different numbers of improvement iterations _T_ and (b) different testing time, evaluated over multiple VRP variants. 

**Success Rate (SR).** Denote by _V_ succ the number of generated programs that successfully produce an feasible solution for the target VRP instance. The _Success Rate_ is given by 



This metric measures the percentage of generated programs that both execute without errors and produce a solution feasible with respect to the constraints of the input instance. 

Table 12 compares the code reliability and solution feasibility of three solvers, SGE, DRoC, and AFL, across a broad range of VRP variants. Because SGE and DRoC can generate runtime-errorfree code only for relatively simple problems where the constraints are easy to satisfy, SGE succeeds solely on TSP, while DRoC performs reliably on TSP, CVRP, and CVRPL, producing code that both compiles correctly and passes feasibility checks. In contrast, our model AFL consistently produces executable code and achieves feasibility verification across all listed variants. In this table, a ✓indicates that the solver achieves both Code Reliability and Solution Feasibility, whereas a _×_ denotes failure to meet one or both of these criteria. 

### C.7 COMPARISON ON ATSP BENCKMARK 

We evaluate our model on the ATSP benchmark (Johnson & McGeoch, 1997), which contains 18 instances with optimal solutions ranging from 17 to 443 nodes, to assess its applicability. The Asymmetric Traveling Salesman Problem (ATSP) is a variant of the classical TSP in which the distance from customer _i_ to customer _j_ may differ from the distance from customer _j_ to customer _i_ , making the problem more challenging and representative of real-world routing scenarios such as one-way street networks or asymmetric transportation costs. The results, presented in Table 13, show that our model achieves consistently favorable performance on this task. 

### C.8 COMPARISON ON ACVRP BENCKMARK 

We further evaluate our model on the ACVRP benchmark (Helsgaun, 2017), which provides 120 capacity-constrained instances with asymmetric distance matrices and customer sizes ranging from 16 to 200. The Asymmetric Capacitated Vehicle Routing Problem (ACVRP) extends the classical VRP by allowing the travel cost from location _i_ to _j_ to differ from that of the reverse direction, while also imposing vehicle-capacity constraints. This combination of asymmetric travel costs and capacity limits makes ACVRP a challenging and practical testbed, reflecting real distribution networks where one-way streets or differing traffic conditions create directional cost differences. The results, 

27 

Published as a conference paper at ICLR 2026 

Table 11: Comparison results on 48 standard 100-node benchmark instances. 

||Obj.|Gap(%)|Obj.|Gap(%)|Obj.|Gap(%)|Obj.|Gap(%)|Obj.|Gap(%)|Obj.|Gap(%)|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
||C|VRP|CV|RPL|CVR|PTW|OC|VRP|CVR|PLTW|OC|VRPL|
|HGS-PVRP|1562|–|1577|–|2542|–|973|–|2576|–|972|–|
|y<br>OR-Tools|.<br>16.28|4.18|.<br>16.47|5.30|.<br>25.81|1.51|.<br>10.00|2.73|.<br>26.26|1.90|.<br>10.00|2.79|
|RF-POMO|15.91|1.83|16.11|2.17|26.34|3.58|10.18|4.66|26.78|3.95|10.18|4.66|
|AFL (_T_=500)|16.66|6.66|17.36|10.08|26.60|4.64|10.37|6.58|27.60|7.14|10.37|6.68|
|AFL (_T_=2000)|16.22|3.84|17.03|7.99|26.02|2.36|10.11|3.91|26.96|4.66|10.15|4.42|
|AFL (_T_=10000)|**15.99**|**2.38**|16.84|6.79|**25.79**|**1.46**|**9.99**|**2.67**|26.56|3.11|**9.99**|**2.78**|
||OCV|RPTW|OCV|RPLTW|CV|RPB|CV|RPBL|CVR|PBTW|OC|VRPB|
|HGS-PyVRP|16.93|–|16.93|–|14.38|–|14.78|–|29.47|–|10.34|–|
|OR-Tools|17.03|0.58|17.02|0.73|14.93|3.85|15.43|4.34|29.95|1.60|10.58|2.32|
|RF-POMO|17.39|2.72|17.39|2.73|15.02|4.47|15.63|5.70|30.34|2.96|10.84|4.82|
|AFL (_T_=500)|1736|254|1761|402|1548|765|1618|947|3150|689|1167|1286|
|<br>AFL (_T_=2000)|.<br>17.14|.<br>1.24|.<br>17.32|.<br>2.30|.<br>15.07|.<br>4.80|.<br>15.71|.<br>6.29|.<br>30.63|.<br>3.94|.<br>11.34|.<br>9.67|
|AFL (_T_=10000)|**17.04**|**0.65**|**17.19**|**1.54**|**14.74**|**2.50**|15.41|4.26|**30.17**|**2.38**|**11.12**|**7.54**|
||CVRP|BLTW|OCV|RPBL|OCVR|PBTW|OCVR|PBLTW|MD|CVRP|MD|CVRPL|
|HGS-PyVRP|29.03|–|10.34|–|19.16|–|19.16|–|11.89|–|11.90|–|
|OR-Tools<br>RF-POMO|29.83<br>30.80|2.77<br>3.28|10.58<br>10.84|2.36<br>4.83|19.30<br>19.61|0.76<br>2.34|19.31<br>19.61|0.77<br>2.34|15.52<br>15.11|5.27<br>30.10|12.52<br>16.25|5.24<br>37.19|
|AFL (_T_=500)|31.31|7.85|10.95|5.90|19.67|2.66|19.67|2.66|12.95|8.92|12.89|8.32|
|AFL (_T_=2000)|30.64|5.55|10.72|3.68|19.41|1.30|19.41|1.30|12.56|5.63|12.54|5.38|
|AFL (_T_=10000)|30.33|4.48|**10.58**|**2.32**|**19.29**|**0.68**|**19.29**|**0.68**|12.39|4.21|12.36|3.87|
||MDC|VRPTW|MDO|CVRP|MDCV|RPLTW|MDO|CVRPL|MDO|CVRPTW|MDO|CVRPLTW|
|HGS-PyVRP|19.33|–|7.97|–|19.35|–|7.97|–|13.00|–|13.00|–|
|OR-Tools|19.62|1.55|8.16|2.33|19.66|1.58|8.16|2.33|13.09|0.74|13.09|0.70|
|RF-POMO|26.60|38.16|10.23|28.52|27.04|40.22|10.23|28.55|17.54|35.43|17.54|35.43|
|AFL (_T_=500)|20.33|5.17|8.35|4.77|20.91|8.06|8.36|4.89|**13.28**|**2.12**|**13.28**|**2.15**|
|AFL (_T_=2000)|**19.85**|**2.69**|8.21|3.01|20.52|6.05|**8.20**|**2.97**|**13.14**|**1.05**|**13.14**|**1.08**|
|AFL (_T_=10000)|**19.61**|**1.45**|**8.14**|**2.12**|20.28|4.81|**8.13**|**2.01**|**13.07**|**0.50**|**13.07**|**0.54**|
||MDC|VRPB|MDC|VRPBL|MDCV|RPBTW|MDO|CVRPB|MDCV|RPBLTW|MDO|CVRPBL|
|HGS-PyVRP|1164|–|1168|–|2203|–|869|–|2206|–|869|–|
|OR-Tools|.<br>12.22|5.01|.<br>12.22|4.62|.<br>22.40|1.69|.<br>8.87|2.33|.<br>22.43|1.70|.<br>8.87|2.13|
|RF-POMO|15.11|30.10|15.71|34.80|30.46|38.80|10.88|25.48|30.97|41.00|10.89|25.49|
|AFL (_T_=500)|12.54|7.73|12.81|9.67|23.49|6.27|9.03|3.91|23.56|6.80|9.03|3.91|
|AFL (_T_=2000)|12.25|5.24|12.47|6.76|22.59|3.54|**8.91**|**2.53**|23.12|4.81|**8.91**|**2.50**|
|AFL (_T_=10000)|12.18|4.63|12.26|4.97|**22.57**|**2.45**|**8.84**|**1.73**|22.85|3.58|**8.83**|**1.61**|
||MDOC|VRPBTW|MDOCV|RPBLTW|CVR|PMB|CVR|PMBL|CVR|PMBTW|OC|VRPMB|
|HGS-PyVRP|12.96|–|12.96|–|13.54|–|13.78|–|25.51|–|9.01|–|
|OR-Tools|14.49|11.79|14.49|11.79|14.93|10.27|15.42|11.90|29.97|17.48|10.59|17.54|
|RF-POMO|18.69|44.70|18.69|44.69|14.98|10.90|15.29|11.12|28.53|11.94|10.84|20.31|
|AFL (_T_=500)|13.40|3.40|**13.22**|**2.01**|14.81|9.38|14.62|6.09|27.38|7.33|9.38|4.11|
|AFL (_T_=2000)|**13.26**|**2.31**|**13.09**|**1.00**|14.38|6.20|**14.18**|**2.90**|26.71|4.70|**9.23**|**2.43**|
|AFL (_T_=10000)|**13.20**|**1.85**|**13.04**|**0.62**|14.17|4.65|**13.91**|**0.94**|26.40|3.49|**9.14**|**1.43**|
||CVRP|MBLTW|OCV|RPMBL|OCVR|PMBTW|OCVRP|MBLTW|MDC|VRPMB|MDC|VRPMBL|
|HGS-PyVRP|25.85|–|9.01|–|16.97|–|16.97|–|10.68|–|10.71|–|
|OR-Tools|3044|1776|1059|1754|1931|1378|1931|1378|1222|1437|1223|1423|
|RF-POMO|.<br>28.89|.<br>11.89|.<br>10.84|.<br>20.32|.<br>18.62|.<br>9.72|.<br>18.62|.<br>9.71|.<br>15.09|.<br>41.78|.<br>15.37|.<br>44.05|
|AFL (_T_=500)|27.46|6.23|9.37|4.00|**17.40**|**2.53**|**17.39**|**2.47**|11.62|8.80|11.45|6.91|
|AFL (_T_=2000)|**26.62**|**2.98**|**9.23**|**2.45**|**17.17**|**1.18**|**17.18**|**1.24**|11.29|5.71|11.17|4.30|
|AFL (_T_=10000)|**26.26**|**1.59**|**9.14**|**1.45**|**17.08**|**0.62**|**17.08**|**0.65**|11.15|4.40|**11.02**|**2.89**|
||MDCVR|PMBTW|MDOC|VRPMB|MDCV|RPLTW|MDOC|VRPMBL|MDOCV|RPMBTW|MDOCV|RPMBLTW|
|HGS-PyVRP|19.29|–|7.66|–|19.35|–|7.66|–|12.96|–|12.96|–|
|OR-Tools<br>RF-POMO|22.39<br>28.68|16.12<br>49.27|8.88<br>10.90|15.83<br>42.41|19.66<br>27.04|1.58<br>40.22|8.87<br>10.90|15.78<br>42.37|14.49<br>18.69|11.79<br>44.70|14.49<br>18.69|11.79<br>44.69|
|AFL (_T_=500)<br>AFL (_T_=2000)|20.62<br>2012|6.89<br>430|7.91<br>**780**|3.26<br>**183**|20.91<br>2052|8.06<br>605|**7.89**<br>**780**|**3.00**<br>**182**|13.40<br>**1326**|3.40<br>**231**|**13.22**<br>**1309**|**2.01**<br>**100**|
|<br>AFL (_T_=10000)|.<br>19.89|.<br>3.11|**.**<br>**7.74**|**.**<br>**1.04**|.<br>20.28|.<br>4.81|**.**<br>**7.75**|**.**<br>**1.17**|**.**<br>**13.20**|**.**<br>**1.85**|**.**<br>**13.04**|**.**<br>**0.62**|



**Note:** _Obj._ denotes the objective value, and _Gap(%)_ represents the relative gap w.r.t. HGS-PyVRP. Lower values indicate better performance. Bold numbers denote cases where the gap from SOTA is within 3%, which is considered acceptable for a fully automated and self-contained framework. 

summarized in Table 14, demonstrate that our model maintains strong code reliability and solution feasibility across all ACVRP instances. 

28 

Published as a conference paper at ICLR 2026 

Table 12: Comparison of Code Reliability and Solution Feasibility. 

|Solver|TSP|CVRP|VRPL|VRP|TW|OVR|P<br>VRPLT|W<br>OVRPL|OVRPTW|OVRPLTW|
|---|---|---|---|---|---|---|---|---|---|---|
|SGE|✓|_×_|_×_|_×_||_×_|_×_|_×_|_×_|_×_|
|DRoC|✓|✓|✓|_×_||_×_|_×_|_×_|_×_|_×_|
|AFL|✓|✓|✓|✓||✓|✓|✓|✓|✓|
|Solver|ECVRP|ECVRPL|ECVRP|TW|EOC|VRP<br>|ECVRPLTW|EOCVRPL|EOCVRPTW|EOCVRPLTW|
|SGE|_×_|_×_|_×_||_×_||_×_|_×_|_×_|_×_|
|DRoC|_×_|_×_|_×_||_×_||_×_|_×_|_×_|_×_|
|AFL|✓|✓|✓||✓||✓|✓|✓|✓|



Table 13: Comparison of AFL and Greedy on ATSP benchmark. 

|Instance|ft53|ft70|ftv33|ftv35|ftv38|ftv44|ftv47|ftv55|ftv64|
|---|---|---|---|---|---|---|---|---|---|
|Best|6905|38673|1286|1473|1530|1613|1776|1608|1839|
|Greedy Obj.|8816|43524|1637|1817|1765|1898|2353|2163|2262|
|Greedy Gap (%)|27.68|12.54|27.29|23.35|15.36|17.67|32.49|34.51|23.00|
|AFL Obj.|**7480**|**39519**|**1340**|**1500**|**1570**|**1657**|**1790**|**1630**|**1882**|
|AFL Gap (%)|**8.33**|**2.19**|**4.20**|**1.83**|**2.61**|**2.73**|**0.79**|**1.37**|**2.34**|
|Instance|ftv70<br>|ftv170<br>k|ro124p|p43<br>|rbg323|rbg358|rbg403|rbg443|ry48p|
|Best|1950|2755|36230|5620|1326|1163|2465|2720|14422|
|Greedy Obj.|2359|3887|45092|5688|1742|1794|3552|3876|16215|
|Greedy Gap (%)|20.97|41.09|24.46|1.21|31.37|54.26|44.10|42.50|12.43|
|AFL Obj.|**2031**|**2964**|**37987**|**5620**|**1358**|**1172**|**2510**|**2780**|**14958**|
|AFL Gap (%)|**4.15**|**7.59**|**4.85**|**0.00**|**2.41**|**0.77**|**1.83**|**2.21**|**3.72**|



### C.9 COMPARISON ON SOP BENCKMARK 

We also evaluate our model on the SOP benchmark (Renaud et al., 1996), which contains 39 instances with optimal solutions and sizes ranging from 9 to 380 nodes. The Sequential Ordering Problem (SOP) is a generalization of the Traveling Salesman Problem that introduces precedence constraints, requiring certain nodes to be visited before others. This added ordering requirement captures practical scenarios such as production sequencing and logistics scheduling, where tasks must follow a specified order. The results, presented in Table 15, show that our model effectively handles these precedence constraints while maintaining high solution quality. 

### C.10 AFL’S SENSITIVITY TO DIFFERENT LLMS 

We tested AFL with two additional LLMs: Claude-Sonnet-4-20250514 and GPT-4o. The results are shown in Table C.9. These experiments help us understand how different LLMs affect AFL’s performance and stability. 

**Solution Quality.** From the results, we see that the strength of the LLM does influence solution quality. More powerful models generate more accurate and complete heuristics, which leads to better objective values. In our tests, the overall performance ranking is: Claude-Sonnet-4 _>_ GPT4.1 _>_ GPT-4o. Although the final performance changes with different LLMs, AFL improves how well each model implements the required heuristics. As shown in Table 9, AFL performs better than both the standard prompt and alternative prompt strategies, showing that AFL can reliably boost a model’s ability to produce working heuristics. 

**Code Reliability.** Most importantly, code reliability stays stable across all LLMs. No matter which model we use, AFL always generates executable code and feasible solutions. This shows that the multi-agent design keeps the whole pipeline stable even when the LLM is not very strong, proving that our framework is robust and widely applicable. 

### C.11 EXPERIMENT ON DIFFERENT INPUT FORMAT 

As VRPLIB is the standard format in the VRP domain, we further evaluated AFL on JSON and CSV inputs to assess its robustness to alternative data representations commonly used in industrial 

29 

Published as a conference paper at ICLR 2026 

Table 14: Comparison of AFL and Greedy on 120 ACVRP instances. 

|Instance<br>A<br>Best Obj.<br>Greedy Gap (%)<br>AFL Gap (%)|-G-100-1<br>2139<br>68.68<br>**13.04**|A-G-100-2<br>1722<br>42.92<br>**7.0**3|A-G-100-3<br>A<br>2550<br>57.41<br>**9.41**|-G-100-4<br>A-G-100-5<br>A-G-100-6<br>1273<br>1878<br>1540<br>74.47<br>77.80<br>46.69<br>**13.98**<br>**31.36**<br>**20.78**|A-G-100-7<br>A<br>1493<br>58.07<br>**11.32**|-G-100-8<br>A-<br>1467<br><br>72.12<br><br>**11.32**<br>|G-100-9<br>A-G-100-10<br>2232<br>1631<br>55.06<br>51.07<br>**10.35**<br>**8.52**|A-G-100-11<br>1992<br>38.10<br>**13.45**|A-G-100-12<br>2057<br>28.83<br>**3.94**|
|---|---|---|---|---|---|---|---|---|---|
|Instance<br>A-|G-100-13|A-G-100-14|A-G-100-15|A-G-100-16<br>A-G-100-17<br>A-G-100-|18<br>A-G-100-19|A-G-100-20|A-G-150-1<br>A-G-150-|2<br>A-G-150|-3<br>A-G-150-4|
|Best Obj.<br>Greedy Gap (%)<br>AFL Gap (%)|2885<br>27.35<br>**3.60**|2101<br>61.78<br>**16.56**|1827<br>34.87<br>**18.28**|1208<br>928<br>2427<br>121.69<br>127.16<br>25.18<br>**26.41**<br>**28.99**<br>**0.00**|2055<br>67.40<br>**9.54**|1929<br>30.53<br>**16.69**|1308<br>913<br>100.15<br>145.89<br>**16.44**<br>**19.06**|1619<br>41.51<br>**25.63**|930<br>77.42<br>**41.51**|
|Instance<br>A<br>Best Obj.|-G-150-5<br>1203|A-G-150-6<br>A<br>1138|-G-150-7<br>A-<br>1110|G-150-8<br>A-G-150-9<br>A-G-150-10<br><br>897<br>1525<br>892|A-G-150-11<br>A-<br>1132|G-150-12<br>A-<br>1187|G-150-13<br>A-G-150-14<br>1619<br>1490|A-G-150-15<br>1095|A-G-150-16<br>749|
|<br>Greedy Gap (%)<br>AFL Gap (%)|79.88<br>**20.20**|92.71<br>**25.57**|93.51<br>1<br>**13.15**<br>|30.21<br>71.28<br>80.61<br>**36.23**<br>**24.59**<br>**15.25**|100.09<br>**23.85**|72.03<br>**27.46**|70.72<br>49.19<br>**14.76**<br>**7.85**|125.11<br>**33.88**|87.85<br>**36.98**|
|Instance<br>A<br>Best Obj.|-G-150-17<br>717|A-G-150-18<br>1610|A-G-150-19<br>1274|A-G-150-20<br>A-G-200-1<br>A-G-200<br>1177<br>1137<br>913|-2<br>A-G-200-3<br>1492|A-G-200-4<br>819|A-G-200-5<br>A-G-200-<br>1048<br>990|6<br>A-G-200-<br>1016|7<br>A-G-200-8<br>814|
|<br>Greedy Gap (%)<br>AFL Gap (%)|53.84<br>**0.00**|53.66<br>**10.19**|46.00<br>**32.10**|54.89<br>48.90<br>202.74<br>**5.01**<br>**10.99**<br>**18.73**|7.31<br>**15.55**|63.37<br>**27.59**|64.22<br>114.55<br>**17.18**<br>**17.58**|92.03<br>**28.94**|109.95<br>**0.00**|
|Instance<br>A-<br>Best Obj.|G-200-9<br><br>1438|A-G-200-10<br>A<br>816|-G-200-11<br>A-<br>1039|G-200-12<br>A-G-200-13<br>A-G-200-14<br>1082<br>1514<br>1341|A-G-200-15<br><br>949|A-G-200-16<br>A<br>662|-G-200-17<br>A-G-200-18<br>668<br>1522|A-G-200-1<br>1188|9<br>A-G-200-20<br>1035|
|Greedy Gap (%)<br>AFL Gap (%)|72.67<br>**12.52**|189.95<br>**33.95**|152.26<br>**26.56**|102.31<br>58.52<br>116.93<br>**13.31**<br>**4.89**<br>**29.23**|172.71<br>**4.11**|167.52<br>**24.62**|254.04<br>65.90<br>**37.43**<br>**0.53**|99.41<br>**10.35**|55.46<br>**13.33**|
|Instance|A-U-4-|1<br>A-U-4-2|A-U-4-3|A-U-4-4<br>A-U-4-5<br>A-U-4-6|A-U-4-7<br>|A-U-4-8<br>A|-U-4-9<br>A-U-4-10|A-U-4-11|A-U-4-12|
|Best Obj.|1671|1108|1937|994<br>1447<br>1251|1142|1043<br>|1826<br>1150|1523|1524|
|<br>Greedy Gap (%)<br>|75.10<br>|42.60<br>|54.93<br>|93.16<br>74.91<br>78.02<br><br><br>|109.81<br>|90.32<br><br><br>|35.32<br>140.35<br><br>|42.88<br>|111.15<br>|
|AFL Gap (%)|**20.35**|**10.74**|**0.00**|**5.53**<br>**19.42**<br>**42.13**|**23.82**|**41.61**<br>|**10.46**<br>**27.65**|**19.63**|**25.33**|
|Instance<br>Best Obj.|A-U-4-1<br>2096|3<br>A-U-4-14<br>1716|A-U-4-15<br>1290|A-U-4-16<br>A-U-4-17<br>A-U-4<br>995<br>825<br>1986|-18<br>A-U-4-1<br><br>1622|9<br>A-U-4-20<br>1453|A-U-6-1<br>A-U-6<br>1205<br>913|-2<br>A-U-6-<br>1492|3<br>A-U-6-4<br>819|
|<br>Greedy Gap(%)<br>|36.12<br>|82.81<br>|94.57<br>|44.12<br>87.27<br>34.4<br><br><br>|4<br>70.28<br><br>|53.68<br>|64.23<br>66.81<br><br>|57.98<br><br>|37.73<br>|
|AFL Gap(%)|**13.74**|**14.34**|**35.74**|**9.05**<br>**24.97**<br>**6.7**|**8.45**|**9.02**|**26.22**<br>**12.2**|**7.71**|**28.94**|
|Instance|A-U-6-5|A-U-6-6|A-U-6-7<br>|-U-6-8<br>A-U-6-9<br>A-U-6-10|A-U-6-11<br>|-U-6-12<br>A|-U-6-13<br>A-U-6-14|A-U-6-15|A-U-6-16|
|Best Obj.|1086|990|1016|814<br>1438<br>816|1071|1111|1544<br>1341|949|662|
|Greedy Gap (%)|90.98|133.64|92.03|215.11<br>93.88<br>262.62|101.87|92.53|64.12<br>88.22|172.71|283.38|
|<br>AFL Gap (%)|**6.72**|**19.80**|**8.17**|**36.86**<br>**13.42**<br>**32.11**|**36.13**|**29.52**|**26.04**<br>**27.96**|**12.22**|**43.35**|
|Instance<br>Bt Ob|A-U-6-<br>668|17<br>A-U-6-1<br>1563|8<br>A-U-6-1<br>1193|9<br>A-U-6-20<br>A-U-8-1<br>A-U-<br>1069<br>981<br>75|8-2<br>A-U-8-<br>3<br>1159|3<br>A-U-8-4<br>737|A-U-8-5<br>A-U-8-<br>832<br>923|6<br>A-U-8-<br>871|7<br>A-U-8-8<br>691|
|es j.<br>Greedy Gap (%)<br>AFL Gap(%)|98.05<br>**0.00**|40.24<br>**1.41**|102.51<br>**41.16**|47.52<br>121.10<br>1771<br>**18.71**<br>**36.70**<br>**29.**|.31<br>72.04<br>**22**<br>**32.18**|62.14<br>**31.89**|116.23<br>127.63<br>**26.20**<br>**17.77**|135.02<br>**52.93**|147.76<br>**27.93**|
|<br>Instance|A-U-8-9|A-U-8-10|A-U-8-11|A-U-8-12<br>A-U-8-13<br>A-U-8-14|A-U-8-15|A-U-8-16<br>|A-U-8-17<br>A-U-8-18|A-U-8-1|9<br>A-U-8-20|
|Best Obj.<br>|1295<br>|716<br>|800<br>|827<br>1091<br>1178<br><br><br>|682<br>|580<br>|591<br>1298<br><br>|1015<br>|854<br>|
|Greedy Gap (%)<br>|53.51<br>|73.46<br>|116.50<br>|187.30<br>81.58<br>125.64<br><br><br>|250.59<br>|72.41<br>|184.43<br>45.61<br><br>|93.00<br>|133.02<br>|
|AFL Gap (%)|**4.48**|**35.47**|**29.50**|**35.31**<br>**26.67**<br>**15.20**|**0.00**|**15.69**|**35.03**<br>**7.86**|**14.09**|**9.84**|
|Instance||Table<br>ESC12|15: Com<br>ESC25|parison of AFL and<br>ESC47<br>ESC63<br>ES|Greedy<br>C78<br>br1|on SOP<br>7.10<br>br|instances.<br>17.12<br>ft53.1|ft53.2|ft53.3|
|Best Ob|j.|1675|1681|1288<br>62<br>18|230<br>5|5|55<br>7531|8062|10262|
|<br>Greedy Gap|<br>(%)|21.43|99.88|198.37<br>22.58<br>10|0.00<br>43|.64<br>4|3.64<br>38.15|56.98|47.41|
|AFL Gap (|%)|**3.16**|**12.14**|**84.32**<br>**0.00**<br>**0.**|**00**<br>**5.**|**45**<br>**5**|**.45**<br>**5.11**|**1.28**|**12.45**|
|Instance|ft|53.4<br>ft7|0.1<br>ft70|.2<br>ft70.3<br>ft70.4<br>kr|o124p.1<br>|kro124p.2|kro124p.3<br>k|ro124p.4|p43.1|
|Best Obj.|1|4425<br>39|313<br>404|19<br>42535<br>53530<br>|39420|41336|49499|76103|28140|
|<br>Greedy Gap (|%)<br>2|8.59<br>17|.16<br>19.|64<br>22.41<br>100.00<br>|33.37|39.64|56.10|29.33|5.29|
|<br>AFL Gap (%|<br>)<br>**0**|**.93**<br>**4.**|**16**<br>**4.8**|**9**<br>**7.03**<br>**0.88**|**8.66**|**10.29**|**7.28**|**1.69**|**0.23**|
|Instance||43.2<br>p|43.3<br>p4|3.4<br>prob42<br>prob100|rbg048a|rbg050c|rbg109a<br>rb|g150a|rbg174a|
|Best Obj.|2|8480<br>2|8835<br>83|005<br>243<br>1163|351|467|1038<br>|1750|2033|
|<br>Greedy Gap (|%)|4.37<br>8|.69<br>2.|70<br>88.48<br>184.69|44.16|21.63|39.02<br>|23.89|20.22|
|AFL Gap (|%)|**0.02**<br>**0**|**.99**<br>**0.**|**05**<br>**30.45**<br>**94.41**|**6.55**|**0.64**|**0.77**|**0.46**|**0.00**|
|Instance||rbg253a|rbg323a|rbg341a<br>rbg358a|rbg378a|ry48p.1|ry48p.2<br>ry|48p.3|ry48p.4|
|Best Obj|.|2950|3140|2568<br>2545|2816|15805|16074<br>1|9490|31446|
|<br>Greedy Gap|<br>(%)|20.61|28.41|47.43<br>61.49|45.92|42.32|30.09<br>4|0.29|30.94|
|<br>AFL G|<br>|**000**|**121**|**308**<br>**267**|**266**|**590**|**607**<br>|**272**|**073**|
|ap (|)|**.**|**.**|**.**<br>**.**|**.**|**.**|**.**<br>|**.**|**.**|



pipelines and benchmark integrations. As shown in Table 17, the model consistently maintains strong performance and solution feasibility across different input formats. 

### C.12 EXPERIMENT ON LARGE CVRP INSTANCES 

AFL is capable of handling extremely large VRP instances. Our current approach generates a general-purpose heuristic from a small instance (e.g., a 50-node instance, which can be obtained by trimming the data of the target instance and serves as a minimal example containing all relevant information such as constraints, problem characteristics, and format specifications). The generated solver is then applied to large-scale cases. As shown in Table 18, AFL achieves competitive performance on CVRPLib-XXL (Gao et al., 2024) with more than 16,000 customers. 

30 

Published as a conference paper at ICLR 2026 

Table 16: Comparison results on different LLM. 

|||n=50|||n=100|||n=50|||n=100||
|---|---|---|---|---|---|---|---|---|---|---|---|---|
||Obj.|Gap (%)|Time (m)|Obj.|Gap (%)|Time (m)|Obj.|Gap (%)|Time (m)|Obj.|Gap (%)|Time (m)|
|HGS-PyVRP|10.37|–|10.40|15.62|–|20.80|10.59|–|10.40|15.77|–|20.80|
|GPT 4o|RP<br>10.64|2.60|2.21|16.05|2.75|4.96|RPL<br>11.01|3.97|13.06|16.64|5.52|34.25|
|Claude 4|CV<br>**10.54**|**1.65**|2.60|**15.90**|**1.79**|5.12|CV<br>**10.91**|**3.02**|6.85|**16.44**|**4.25**|**25.79**|
|GPT 4.1|10.59|2.12|2.10|15.99|2.38|4.38|11.18|5.57|6.93|16.84|6.79|25.48|
|HGS-PyVRP|W<br>16.03|–|10.40|25.42|–|20.80|P<br>6.51|–|10.40|9.73|–|20.80|
|GPT 4o|PT<br>16.45|2.62|12.62|26.88|5.74|25.44|VR<br>6.87|5.53|3.07|10.36|6.47|7.38|
|Claude 4|VR<br>16.28|1.56|8.50|26.19|3.03|33.78|OC<br>**6.60**|**1.38**|2.95|**9.94**|**2.26**|7.22|
|GPT 4.1|C<br>**16.19**|**0.99**|9.31|**25.79**|**1.46**|38.45|6.64|2.00|2.20|9.99|2.67|5.52|
|HGS-PyVRP|W<br>16.36|–|10.40|25.76|–|20.80|L<br>6.51|–|10.40|9.72|–|20.80|
|GPT 4o|PLT<br>16.79|2.63|8.54|26.81|4.08|35.48|RP<br>6.81|4.61|7.13|10.33|6.28|13.42|
|Claude 4|VR<br>**16.55**|**1.16**|7.32|**26.50**|**2.87**|30.94|CV<br>**6.59**|**1.23**|7.43|**9.91**|**1.95**|16.59|
|GPT 4.1|C<br>16.61|1.53|8.90|26.56|3.11|35.33|O<br>6.64|1.99|5.65|9.99|2.78|16.27|
|HGS-PyVRP|W<br>10.51|–|10.40|16.93|–|20.80|TW<br>10.51|–|10.40|16.93|–|20.80|
|GPT 4o|RPT<br>10.91|3.81|11.89|17.68|4.43|27.39|PL<br>10.88|3.52|11.29|17.66|4.31|58.89|
|Claude 4|CV<br>10.63|1.14|14.89|17.24|1.83|35.95|VR<br>10.64|1.24|12.23|17.26|1.95|62.24|
|GPT 4.1|O<br>**10.55**|**0.38**|11.15|**17.04**|**0.65**|49.05|OC<br>**10.58**|**0.67**|17.27|**17.19**|**1.54**|70.31|



Table 17: Combined Results on JSON and CSV Format Inputs. 

||||n=50|||n=100||||n=50|||n=100||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|||Obj.|Gap (%)|Time (m)|Obj.|Gap (%)|Time (m)||Obj.|Gap (%)|Time (m)|Obj.|Gap (%)|Time (m)|
|JSON|CVRP|10.68|2.99|2.69|16.36|3.71|4.99|CVRPL|10.86|2.55|7.37|16.42|4.12|29.20|
|CSV||10.69|3.09|2.61|16.40|4.99|5.50||10.75|1.51|4.73|16.31|3.42|20.72|
|JSON|CVRP|16.26|1.43|12.97|26.17|2.95|21.22|OCVRP|6.71|3.07|2.07|10.22|5.04|5.38|
|CSV|TW|16.19|1.00|14.87|26.07|2.56|26.11||6.68|2.61|2.80|10.14|4.21|6.17|
|JSON|CVRPL|16.63|1.65|8.02|26.52|2.95|31.64|OCVRP|6.73|3.38|6.78|10.26|5.56|16.46|
|CSV|TW|16.61|1.52|8.99|26.48|2.80|32.10|L|6.71|3.07|7.96|10.11|4.01|18.24|
|JSON|OCVRP|10.58|0.67|14.73|17.19|1.54|55.47|OCVRP|10.55|0.38|19.62|17.15|1.30|82.31|
|CSV|TW|10.60|0.86|10.26|17.25|1.89|50.99|LTW|10.56|0.48|16.65|17.16|1.36|69.19|



During code generation, we also enforce a practical constraint: during solution derivation, the algorithm must execute within 10 seconds for the given instance. If this limit is exceeded, the system triggers a timeout, then the Revision Agent (RA) and Error Analysis Agent (EAA) are trigered to refine the algorithm for improved efficiency. We will add clarifications of this mechanism in the revised manuscript. Looking ahead, we will further enhance efficiency by exploring multi-objective evolutionary strategies to evolve the generated algorithms, jointly optimizing both performance and computational efficiency. 

## D EXAMPLES OF PROMPTS AND OUTPUTS 

### D.1 SUBTASK 1: PROBLEM DESCRIPTION 

In the problem description subtask, we divide the GA’s work into two sequential phases to reduce its cognitive load and improve overall accuracy. In the first phase, the agent generates the description, constraints, and the specific problem type. In the second phase, it produces the input specification, expected output, and the optimization objective. After these two phases are completed, the JA evaluates the entire draft for consistency and correctness, and the RA subsequently refines each component as needed. 

### D.1.1 GENERATION AGENT(GA) 

### **Prompt 1** : 

We need to solve a VRP instance. I will provide you with the instance. Please analyze it carefully. First, give a concise description of the problem type in [ ], explaining what the problem is about. 

31 

Published as a conference paper at ICLR 2026 

Table 18: Performance of AFL on CVRPLib-XXL 

|**Gap(%)**|**L1(3k)**|**L2(4k)**|**A1(6k)**|**A2(7k)**|**G1(10k)**|**G2(11k)**|**B1(15k)**|**B2(16k)**|
|---|---|---|---|---|---|---|---|---|
|POMO|75.30|78.16|112.27|159.22|–|–|–|–|
|LEHD|14.04|26.30|18.90|26.40|27.23|38.45|35.94|40.76|
|Our|**8.12**|**13.34**|**8.60**|**13.62**|**8.02**|**14.85**|**7.01**|**16.56**|



Second, identify its constraints and list them clearly in numbered format (1), 2), 3), ...) within [ ]. For each constraint, write both the abbreviation (if any) and a short explanation (e.g., ‘Capacity (C): vehicles have limited capacity.’). Do not include instance-specific details like the exact number of nodes, vehicles, or capacity values. 

When analyzing, be as comprehensive as possible: consider not only the common constraints but also more general ones, such as whether each customer can be visited multiple times, whether all routes must start and end at a depot, or other structural constraints that might apply. You may refer to the following typical constraint categories as guidance, but you are not limited to them: 

- Electricity (E): electric vehicles are subject to fuel constraints. Each vehicle has a limited fuel capacity, fuel is consumed proportionally to the distance traveled related to fuel consumption rate, and vehicles must recharge at designated charging stations when necessary. Recharging consumes time related to the refuel rate and remaining fuel. 

- Capacity (C): vehicles have limited capacity. 

- Open Route (O): vehicles do not return to the depot. 

- Backhaul (B): vehicles must handle linehaul (deliveries) first, then backhaul (pickups). 

- Mixed (M): vehicles may mix deliveries and pickups in the same route. 

- Duration Limit (L): each route has a maximum distance or time limit. 

- Time Windows (TW): customers must be served within specified time intervals. 

- Multi-depot (MD): there are multiple depots. 

- Visit constraint (V): each customer may only be visited once. 

- Depot constraint (D): routes must start and end at the depot. 

Finally, write the standard problem type abbreviation (e.g., TSP, CVRP, CVRPL, VRPTW, PDP, OVRP, MDVRP, ECVRP) enclosed in ” ”. 

Check again whether the constraints fit the specific name; the Visit constraint should be present. Output exactly three lines in this order: 

1) [problem description] 

- 2) [constraints] 

3) ”specific name” 

Below is the .vrp instance content: <vrp text> 

### **Output 1:** 

1) [The Capacitated Vehicle Routing Problem (CVRP) involves determining optimal routes for a fleet of vehicles to deliver goods to a set of customers while minimizing total distance traveled and ensuring that vehicle capacity is not exceeded.] 

32 

Published as a conference paper at ICLR 2026 

2) [1) Capacity (C): the total demand on any route cannot exceed vehicle capacity. 2) Visit (V): each customer is visited exactly once. 3) Depot (D): every route starts and ends at the depot.] 

3) ”CVRP” 

### **Prompt 2:** 

We need to design an algorithm for the following VRP instance. The details of the instance are: <Output1>. 

Based on this description and the instance contents, please specify: 

First, list the essential input elements an algorithm would require from the instance. Element names must not contain spaces; use underscores _ instead. 

Second, describe precisely what the algorithm should output (e.g., a best feasible set of vehicle routes that satisfy all listed constraints). 

Third, describe clearly the optimization objective (e.g., minimize total travel distance, minimize fleet size, minimize lateness). 

Important: Each of the three answers (input, output, objective) must be enclosed in [ ] as shown. Do not include instance-specific details like the exact number of nodes, vehicles, or capacity values. Also verify that every listed input is actually provided by the instance content. 

Output exactly three lines in this order: 

4) [input] 

5) [output] 

6) [objective] 

Below is the .vrp instance content: <vrp text> 

### **Output 2:** 

4) [depot, node coordinates, demands, vehicle ~~c~~ apacity] 

5) [A set of vehicle routes, each beginning and ending at the depot, visiting every customer exactly once while respecting capacity constraints.] 

6) [Minimize the total travel distance.] 

D.1.2 JUDGMENT AGENT (JA) 

### **Prompt:** 

You are a VRP expert. I will give you: 1) The original .vrp file content 2) GPT’s first answer (problem description + constraints + specific name) 

3) GPT’s second answer (input, output, objective) 

Your task is to judge correctness: 

- For the first answer: check whether the problem description, listed constraints, and specific 

- name are consistent with .vrp file contents. Specifically, check for contradictions in the following pairs: 

- problem description vs. .vrp file 

33 

Published as a conference paper at ICLR 2026 

- constraints vs. .vrp file 

- specific name vs. .vrp file 

- problem description vs. constraints 

- problem description vs. specific name 

- constraints vs. specific name 

If any contradictions exist, treat the .vrp file as the ground truth and mark it as incorrect. If everything is consistent, mark it as correct. Check again whether the constraints fit the specific name and problem description. If correct, return ’True’ with a short explanation. If wrong, return’False’ with a short explanation. 

- For the second answer: check if input, output, and optimization objective are valid and consistent with the VRP instance and the constraints. Input must correspond only to elements explicitly defined in the instance file. Every input listed must be directly obtainable from the instance. Input element names must not contain spaces; use underscores ~~.~~ Output must clearly describe feasible vehicle routes respecting all constraints. The optimization objective must align with VRP goals. 

If any contradictions exist, treat the .vrp file as the ground truth and mark it as incorrect.If everything is consistent, mark it as correct.If correct, return ’True’ with a short explanation. If wrong, return ’False’ with a short explanation. 

Output format must be exactly 4 lines: 

1) right1: True/False 

2) jud1: explanation 

3) right2: True/False 

4) jud2: explanation Here is the VRP file: <vrp_text> Here is GPT’s first answer: <problem_description_1> Here is GPT’s second answer: <problem_description_2> 

### **Output:** 

1) right1: True 

2) jud1: The first answer accurately reflects the .vrp file, providing a clear problem description and consistent constraints (Capacity, Visit, Depot) along with the correct specific name, with no contradictions. 

3) right2: False 

4) jud2: The second answer includes input or objective elements that are not fully supported by the CVRP instance—specifically, it omits capacity from the input—so it is not fully consistent with the file’s available data and constraints. 

### D.1.3 REVISION AGENTS (RA) 

The formats of Output 1 and Output 2 are identical to those in Section D.1.1. 

### **Prompt 1:** 

34 

Published as a conference paper at ICLR 2026 

We need to solve a VRP instance. I will provide you with the instance. Please analyze it carefully. 

Step 1: Give a concise description of the problem type in [ ], explaining what the problem is about. 

Step 2: Identify its constraints and list them clearly in numbered format (1), 2), 3), ...) within [ ]. For each constraint, write both the abbreviation (if any) and a short explanation (e.g., ’Capacity (C): vehicles have limited capacity.’). Do not include instance-specific details like the exact number of nodes, vehicles, or capacity values. Consider whether customers may be visited once or multiple times, and whether all routes must start/end at a depot (unless open routes are specified). 

Reference constraint categories (not exhaustive): 

- Electricity (E): electric vehicles are subject to fuel constraints. Each vehicle has a limited fuel capacity, fuel is consumed proportionally to the distance traveled related to fuel consumption rate, and vehicles must recharge at designated charging stations when necessary. Recharging consumes time related to the refuel rate and remaining fuel. 

- Capacity (C): vehicles have limited capacity. 

- Open Route (O): vehicles do not return to the depot. 

- Backhaul (B): deliveries first, then pickups. 

- Mixed (M): deliveries and pickups can be mixed. 

- Distance Limit (L): each route has a maximum distance or time limit. 

- Time Windows (TW): customers must be served within specific time intervals. 

- Multi-depot (MD): multiple depots instead of one. 

- Visit constraint (V): whether each customer can be visited only once. 

- Depot constraint (D): routes must start and end at the depot. 

Step 3: Write the standard problem type abbreviation (e.g., TSP, CVRP, CVRPL) enclosed in “ ”. Ensure the abbreviation is consistent with the constraints. 

Check again that the constraints fit the specific name, and include the Visit constraint. 

Here is your previous answer: <ans> 

However, there were some issues identified: <jud> 

Now, please correct your answer strictly according to the rules above. 

Output format (exactly three lines): 

1) [problem description] 

- 2) [constraints] 

3) ”specific name” Below is the .vrp instance content: <vrp text> 

### **Prompt 2:** 

We need to design an algorithm for the following VRP instance. The details of the instance are: <Output 1>. 

Based on this description and the instance contents, please provide: 

35 

Published as a conference paper at ICLR 2026 

Step 1: List the essential elements an algorithm would require from the instance, and the list must include depot. 

Step 2: Describe precisely what the algorithm should output (e.g., a set of feasible vehicle routes that satisfy all listed constraints). 

Step 3: Describe clearly the optimization objective (e.g., minimize total travel distance, minimize fleet size, minimize lateness). Important rules: 

- Each of the three answers (input, output, objective) must be enclosed in [ ] exactly as shown. - Do not include instance-specific details like the exact number of nodes, vehicles, or capacity values. 

- Step 1 element names must not contain spaces; use underscores instead. Here is your previous answer: <ans> Issues identified in that answer: <jud> Now, please correct your answer strictly according to the rules above. Final output format (exactly three lines): 4) [input] 5) [output] 6) [objective] Below is the .vrp instance content: <vrp_text> 

- D.2 SUBTASK 2: CODE GENERATION 

D.2.1 GENERATION AGENT (GA) 

### **Prompt (Partly):** 

Here is the code you generated before (for reference, please improve or extend it if needed): <code> We are working on a VRP problem instance: Problem description: <problem_desc> Constraints: <constraints> Specific name: <specific_name> Input definition: <input_def> Output definition: <output_def> Optimization objective: <objective> Important rules: - You are given the raw .vrp file content for context. - Do not hardcode any instance-specific details such as the number of nodes, vehicle count, or node coordinates. 

- Any functions generated must be general-purpose and reusable for any VRP instance. Task: Generate a Python function named exactly ’read ~~v~~ rp(path: str)’: 

36 

Published as a conference paper at ICLR 2026 

- The function must read a .vrp file and parse its content strictly according to the items listed in the Input definition. 

- Every element mentioned in the Input definition must be parsed and included. No additional fields may be added, and no required fields may be omitted. 

- The function must return a dictionary where: 

- Keys exactly match the names in the Input definition, using underscores “ ” instead of 

- spaces. 

• Each value is returned as a list, even if it contains only a single element. 

- A section may end with “-1”, “EOF”, or the beginning of another section header (lines in all 

- caps ending with “ ~~S~~ ECTION”) and the function must handle all of these cases. 

- The implementation must be general-purpose; do not hardcode any instance-specific details. Output format requirement: 

Return only valid Python code inside a single code block marked as ‘‘‘python ... ‘‘‘ with no extra text, explanations, or comments outside the code block. 

If previous code is provided, include it (or an improved version) together with the newly generated function in the final output. 

Ensure that all necessary import statements required for the code to run are included at the top of the code block. 

### **Output (Partly):** 

1 **<mark>import</mark>** <mark>re</mark> 2 **<mark>import</mark>** <mark>math</mark> 3 **<mark>import</mark>** <mark>random</mark> 4 **<mark>import</mark>** <mark>copy</mark> 5 **<mark>import</mark>** <mark>argparse</mark> 6 **<mark>import</mark>** <mark>sys</mark> 7 **<mark>def</mark>** <mark>read_vrp(path:</mark> **<mark>str</mark>** <mark>):</mark> 8 **<mark>with open</mark>** <mark>(path, ’r’)</mark> **<mark>as</mark>** <mark>f:</mark> 9 <mark>lines = f.readlines()</mark> 10 <mark>node_coord_dict = {}</mark> 11 <mark>demand_dict = {}</mark> 12 <mark>depot_ids = []</mark> 13 <mark>dimension = None</mark> 14 <mark>capacity = None</mark> 15 <mark>in_node_coord_section = False</mark> 16 <mark>in_demand_section = False</mark> 17 <mark>in_depot_section = False</mark> 18 **<mark>for</mark>** <mark>line</mark> **<mark>in</mark>** <mark>lines:</mark> 19 <mark>line = line.strip()</mark> 20 **<mark>if not</mark>** <mark>line</mark> **<mark>or</mark>** <mark>line == ’EOF’:</mark> 21 **<mark>continue</mark>** 22 **<mark>if</mark>** <mark>line.startswith(’DIMENSION’):</mark> 23 <mark>dimension =</mark> **<mark>int</mark>** <mark>(re.search(r’:\s*(\d+)’, line).group(1))</mark> 24 **<mark>continue</mark>** 25 **<mark>if</mark>** <mark>line.startswith(’CAPACITY’):</mark> 26 <mark>capacity =</mark> **<mark>float</mark>** <mark>(re.search(r’:\s*([\d.]+)’, line).group(1) )</mark> 27 **<mark>continue</mark>** 28 **<mark>if</mark>** <mark>line == ’NODE_COORD_SECTION’:</mark> 29 <mark>in_node_coord_section = True</mark> 30 <mark>in_demand_section = False</mark> 31 <mark>in_depot_section = False</mark> 32 **<mark>continue</mark>** 33 **<mark>if</mark>** <mark>line == ’DEMAND_SECTION’:</mark> 

37 

Published as a conference paper at ICLR 2026 

34 <mark>in_node_coord_section = False</mark> 35 <mark>in_demand_section = True</mark> 36 <mark>in_depot_section = False</mark> 37 **<mark>continue</mark>** 38 **<mark>if</mark>** <mark>line == ’DEPOT_SECTION’:</mark> 39 <mark>in_node_coord_section = False</mark> 40 <mark>in_demand_section = False</mark> 41 <mark>in_depot_section = True</mark> 42 **<mark>continue</mark>** 43 **<mark>if</mark>** <mark>in_node_coord_section:</mark> 44 <mark>tokens = line.split()</mark> 45 <mark>idx =</mark> **<mark>int</mark>** <mark>(tokens[0])</mark> 46 <mark>x =</mark> **<mark>float</mark>** <mark>(tokens[1])</mark> 47 <mark>y =</mark> **<mark>float</mark>** <mark>(tokens[2])</mark> 48 <mark>node_coord_dict[idx] = [x, y]</mark> 49 **<mark>elif</mark>** <mark>in_demand_section:</mark> 50 <mark>tokens = line.split()</mark> 51 <mark>idx =</mark> **<mark>int</mark>** <mark>(tokens[0])</mark> 52 <mark>d =</mark> **<mark>float</mark>** <mark>(tokens[1])</mark> 53 <mark>demand_dict[idx] = d</mark> 54 **<mark>elif</mark>** <mark>in_depot_section:</mark> 55 <mark>val =</mark> **<mark>int</mark>** <mark>(line)</mark> 56 **<mark>if</mark>** <mark>val == -1:</mark> 57 **<mark>continue</mark>** 58 <mark>depot_ids.append(val)</mark> 59 **<mark>if not</mark>** <mark>depot_ids:</mark> 60 **<mark>raise</mark>** <mark>ValueError(’Depot information missing in VRP file.’)</mark> 61 **<mark>if</mark>** <mark>dimension</mark> **<mark>is</mark>** <mark>None:</mark> 62 **<mark>raise</mark>** <mark>ValueError(’DIMENSION missing in VRP file.’)</mark> 63 **<mark>if</mark>** <mark>capacity</mark> **<mark>is</mark>** <mark>None:</mark> 64 **<mark>raise</mark>** <mark>ValueError(’CAPACITY missing in VRP file.’)</mark> 65 <mark>all_ids =</mark> **<mark>sorted</mark>** <mark>(node_coord_dict.keys())</mark> 66 **<mark>if len</mark>** <mark>(all_ids) != dimension:</mark> 67 **<mark>raise</mark>** <mark>ValueError(’Parsed node_coord_dict length does not match DIMENSION.’)</mark> 68 **<mark>if len</mark>** <mark>(demand_dict) != dimension:</mark> 69 **<mark>raise</mark>** <mark>ValueError(’Parsed demand_dict length does not match DIMENSION.’)</mark> 70 <mark>depot_id = depot_ids[0]</mark> 71 **<mark>if</mark>** <mark>depot_id</mark> **<mark>not in</mark>** <mark>all_ids:</mark> 72 **<mark>raise</mark>** <mark>ValueError(’Depot id not present in node_coord_dict.’)</mark> 73 <mark>customer_ids = [nid</mark> **<mark>for</mark>** <mark>nid</mark> **<mark>in</mark>** <mark>all_ids</mark> **<mark>if</mark>** <mark>nid != depot_id]</mark> 74 <mark>node_id_list = [depot_id] +</mark> **<mark>sorted</mark>** <mark>(customer_ids)</mark> 75 <mark>node_coordinates = [node_coord_dict[nid]</mark> **<mark>for</mark>** <mark>nid</mark> **<mark>in</mark>** <mark>node_id_list]</mark> 76 <mark>demands = [demand_dict[nid]</mark> **<mark>for</mark>** <mark>nid</mark> **<mark>in</mark>** <mark>node_id_list]</mark> 77 **<mark>return</mark>** <mark>{</mark> 78 <mark>"depot": [depot_id],</mark> 79 <mark>"node_coordinates": node_coordinates,</mark> 80 <mark>"demands": demands,</mark> 81 <mark>"vehicle_capacity": [capacity]</mark> 82 <mark>}</mark> 

Listing 1: Example of route feasibility check 

D.2.2 JUDGMENT AGENT (JA) 

### **Prompt (Partly):** 

You are a strict Python code reviewer and VRP expert. Here is the generated Python code: <code> We are working on a VRP problem instance: 

38 

Published as a conference paper at ICLR 2026 

Problem description: <problem_desc> Constraints: <constraints> Specific name: <specific_name> Input definition: <input_def> Output definition: <output_def> Optimization objective: <objective> Evaluation rules: 

Only evaluate the given code snippet. Ignore any other functions or unrelated context. Check if the code has syntax errors or logical bugs that would prevent execution. For ’read ~~v~~ rp’: 

• Ensure it extracts exactly the elements listed in the Input definition. 

• No additional fields may be added, and no required fields may be omitted. 

• Verify that each extracted element is explicitly available in the provided .vrp file content. 

• Do not assume or fabricate values not present in the file. 

• A section may end with -1, EOF, or the beginning of another section header (e.g., lines in all caps ending with ~~S~~ ECTION); it must handle all of these situations. 

• Confirm that the function returns all required fields in a dictionary format, and each value must be returned as a list (array); keys must match the Input definition exactly, using underscores instead of spaces. 

• The function ’read vrp’ must be contained in the code. 

Use the provided .vrp file content as the only ground truth for evaluation. Do not invent or assume data that is not present in the instance. 

Below is the .vrp instance content: <vrp_text> 

Assume that the VRP file provides all elements in <input_def>. 

Assume that this code is only for <specific_name>, <problem_desc>. 

Assume that node IDs preserve the exact order given in the input .vrp file, are unique, and contain no duplicates. 

Your task: 

If the code is fully correct (no syntax errors, no logical bugs, all constraints satisfied, and fully consistent with the VRP rules), return right1: True and provide a brief explanation. 

If the code has any issues (syntax bugs, logical errors, constraint violations, inconsistent naming, wrong input/output handling, or deviations from the specification), return right1: False and explain why. If wrong, you must also provide clear and concrete suggestions for how to fix or improve the code. 

Important formatting rule: For easier parsing, the explanation or suggestions must be written in plain text on a single line, without using any line breaks ( _\_ n) or additional colons except the ones required in right: and jud:. 

Output format must be exactly 2 lines: right: True/False jud: explanation and suggestions 

**Output** : 

39 

Published as a conference paper at ICLR 2026 

right: False 

jud: The code is invalid because the returned dictionary key ”node ~~c~~ oordinate” does not match the required Input definition key ”node ~~c~~ oordinates”; rename the key to ”node ~~c~~ oordinates” to ensure consistency with the specified input definition. 

D.2.3 REVISION AGENT (RA) 

### **Prompt** : 

Here is the code you generated before: <prev_code> We are working on a VRP problem instance. Problem description: <problem_desc> Constraints: <constraints> Specific name: <specific_name> Input definition: <input_def> Output definition: <output_def> Optimization objective: <objective> Important rules: - You are given the raw .vrp file content below for context. - Do not hardcode any instance-specific details such as number of nodes, vehicle count, or node coordinates. - The functions you generate must be general-purpose and reusable for any VRP instance. Below is the .vrp instance content (for context only): <vrp_text> The code you generated previously has the following issues and revised suggestions: <jud> Please correct the code according to the issues above, without changing the number of functions, their names, or their signatures. Output format requirement: Return only valid Python code inside a single code block: ‘‘‘python ... ‘‘‘ with no extra text, explanations, or comments outside the code block. 

The output format is identical to that described in Sec. D.2.1. 

D.3 SUBTASK 3: SOLUTION DERIVATION 

D.3.1 ERROR ANALYSIS AGENTS (EAA) 

### **Prompt:** 

You are a strict Python code reviewer and VRP expert. We are working on a VRP problem instance. Problem description: <problem_desc> Constraints: <constraints> Specific name: <specific_name> Input definition: <input_def> 

40 

Published as a conference paper at ICLR 2026 

Output definition: <output_def> 

Optimization objective: <objective> 

The code was generated using the following rules: <all rules in generation code> Use the provided .vrp file content as the only ground truth for analysis. Do not invent or assume data that is not present in the instance. 

Below is the .vrp instance content: <vrp_text> 

The code execution failed and produced the following error message: <error_msg> 

Your task: Analyse the error message and explain why the error happened. Provide clear and concrete suggestions for how to fix or improve the code. 

Formatting rule: For easier parsing, your explanation and suggestions must be written strictly in plain text on a single line, without using any line breaks ( _\_ n) or additional colons except the required jud: prefix. 

Output format must be exactly 1 line: 

1) jud: explanation and suggestions 

### **Output:** 

jud: The error occurred because the algorithm timed out while generating routes for the CVRP instance, indicating that the current implementations of the initial and insert functions have excessively high computational complexity; to fix this, simplify the construction strategy in initial by reducing unnecessary nested loops, and in insert replace exhaustive cost evaluations with a priority queue or incremental cost update to lower overall runtime. 

The JA and RA are identical to those described in Section D.2.2 and Section D.2.3. 

## E THE USE OF LARGE LANGUAGE MODELS 

In this study, large language models (LLMs) are not merely tools for polishing text but an integral component of the proposed framework. They serve as autonomous agents within our framework, while the core ideas and the manuscript itself were conceived, prepared, and finalized by the authors. 

41 

