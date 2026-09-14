# **Self-Guiding Exploration for Combinatorial Problems** 

**Zangir Iklassov Yali Du Farkhad Akimov Martin Takáˇc** MBZUAI King’s College London MBZUAI MBZUAI 

## **Abstract** 

Large Language Models (LLMs) have become pivotal in addressing reasoning tasks across diverse domains, including arithmetic, commonsense, and symbolic reasoning. They utilize prompting techniques such as Exploration-of-Thought, Decomposition, and Refinement to effectively navigate and solve intricate tasks. Despite these advancements, the application of LLMs to Combinatorial Problems (CPs), known for their NP-hardness and critical roles in logistics and resource management remains underexplored. To address this gap, we introduce a novel prompting strategy: Self-Guiding Exploration (SGE), designed to enhance the performance of solving CPs. SGE operates autonomously, generating multiple thought trajectories for each CP task. It then breaks these trajectories down into actionable subtasks, executes them sequentially, and refines the results to ensure optimal outcomes. We present our research as the first to apply LLMs to a broad range of CPs and demonstrate that SGE outperforms existing prompting strategies by over 27.84% in CP optimization performance. Additionally, SGE achieves a 2.46% higher accuracy over the best existing results in other reasoning tasks (arithmetic, commonsense, and symbolic). Our implementation is available online.<sup>1</sup> 

## **1 Introduction** 

Large Language Models (LLMs) have emerged as powerful tools capable of executing reasoning tasks across various domains, including arithmetic, commonsense, and symbolic reasoning Brown et al. [2020], Thoppilan et al. [2022], Chowdhery et al. [2023], Ouyang et al. [2022]. These models may leverage prompting techniques such as Exploration-of-Thought Wei et al. [2022b], Kojima et al. [2022], Yao et al. [2023], Decomposition Zhou et al. [2023], Khot et al. [2022], and Refinement Madaan et al. [2023] to break down and solve various tasks in a step-by-step manner. Recent research has been directed towards extending these techniques to tackle more sophisticated optimization challenges Yang et al. [2024]. Combinatorial problems (CPs) may represent a category of these complex optimization tasks, associated with intricate computational challenges. 

Combinatorial Problems are characterized by their NP-hardness and inherent complexity, which result in an exponential growth in the number of potential solutions. This complexity presents substantial challenges in the research Oroojlooyjadid et al. [2020], Nazari et al. [2018], Iklassov et al. [2023b,a]. CPs are especially crucial in sectors that require efficient logistics, planning, and scheduling. Currently, the dominant approach in these industries involves metaheuristic methods. These methods combine various simple but fast heuristics to effectively tackle CPs within specific constraints. Nonetheless, the effectiveness of these heuristics can vary significantly depending on the CP task and its associated constraints, necessitating a customized selection of heuristics to achieve optimal performance. In the meantime, research on exploring LLMs to solve CPs reveals substantial gaps. While recent advancements indicate the effectiveness of LLMs in various reasoning tasks Wei et al. [2022a], Zhang et al. [2023], Suzgun et al. [2023], Zhou et al. [2023], their application to CPs 

> 1 `https://github.com/Zangir/LLM-for-CP` 

Preprint. Under review. 

has been minimal. Research such as that conducted in Liu et al. [2024], Masoud et al. [2024], Yang et al. [2024] suggests that current generative models can address smaller instances of the Traveling Salesman Problem (TSP). However, as problem sizes increase, existing prompting strategies begin to yield inadequate responses, underscoring the need for more sophisticated prompting methods. Moreover, there is a notable scarcity of research addressing other complex CPs, particularly the Vehicle Routing and Job Scheduling Problems, which pose significant challenges in logistics, planning industries, and operations research. 

In this work, we introduce a novel prompting strategy: self-guiding exploration (SGE), designed to enhance the problem-solving process for CPs. This algorithm works as a combination of explorationof-thought, decomposition, and refinement prompting methods. The SGE approach autonomously generates multiple thought trajectories for a given CP, each trajectory representing a specific heuristic to tackle the given task. Each trajectory is then decomposed into subtasks, which are executed one by one, and their outputs are refined and combined into a final solution. Unlike the task-specific prompts utilized in other methods, SGE employs general-purpose prompts, allowing for the adaptive use of specific heuristic solutions tailored to various CPs, such as the Hungarian heuristic for the assignment problem and the Nearest Neighbor heuristic for the vehicle routing problem. Essentially, SGE acts as a versatile metaheuristic capable of identifying, combining, and refining task-specific heuristics for individual CP tasks. 

**Our work makes following contributions.** Firstly, we present a novel investigation into the application of large language models for solving combinatorial problems. Secondly, we introduce a new prompting strategy, SGE, that autonomosly generates thought trajectories, splits them into subtasks and refines the answers. Thirdly, we demonstrate that SGE outperforms existing prompting strategies such as Chain-of-Thought, Decomposition, and Self-Refinement, improving CP optimization performance by 27 _._ 84%. Lastly, we validate the applicability of SGE across other reasoning tasks, including arithmetic, commonsense, and symbolic tasks, where our method achieves a 2 _._ 46% higher accuracy than the best existing results. 

## **2 Related Work** 

**CP via Classical Approach.** In classical research, combinatorial problems are predominantly tackled using heuristic and metaheuristic methods specifically crafted for particular tasks. Notable examples include the Ant-Colony Optimization and Tabu Search methods for addressing the Vehicle Routing Problem Pichpibul and Kawtummachai [2013], Goel et al. [2019], Li and Li [2020], the Shortest Processing Time and Most Work Remaining Heuristics for Job Scheduling Problems Sels et al. [2012], and the Hungarian Algorithm for the Assignment Problem Amponsah et al. [2016]. These approaches are favored in industrial settings due to their simplicity and speed. However, they need to be individually tailored to each task and its constraints’ setting. In contrast, exact solvers such as Google-OR-Tools Google [2023] offer general and precise solutions, but their applicability is often limited to smaller-scale problems due to the inherent NP-hardness of combinatorial problems. **CP via Learning-Based Approach.** In AI literature, Reinforcement Learning (RL) has been a prominent approach for tackling combinatorial problems since the 1990s Mahadevan et al. [1997], Mahadevan and Theocharous [1998], Zhang and Dietterich [1995], Gabel and Riedmiller [2008], Aydin and Öztemel [2000]. The integration of deep learning, particularly through innovations like Pointer Networks, has significantly enhanced RL’s capability to handle more complex combinatorial tasks Vinyals et al. [2015], Bello et al. [2016]. Further advancements involve the use of Transformer networks Deudon et al. [2018], Vaswani et al. [2017], Kool et al. [2018], with notable applications in solving the Vehicle Routing Problem Nazari et al. [2018], Iklassov et al. [2023b]. Despite these advances, RL-based methods often still do not exceed the performance of traditional heuristics, especially when scalability and accurate state representation are required Wang et al. [2021], Mao et al. [2019], Zhang et al. [2020], Sun et al. [2021]. 

**CP with LLMs.** To date, Liu et al. [2024], Masoud et al. [2024], Yang et al. [2024] are the only studies investigating the use of LLMs (GPT-3.5 and GPT-4) models on the Traveling Salesman Problem through iterative prompting, requesting the model to refine a candidate solution repeatedly. There remains a significant research gap in applying more advanced prompting strategies and exploring LLMs for other combinatorial problems such as vehicle routing and job scheduling. 

**Prompting Strategies.** The expressive capabilities of direct prompting in Large Language Models are theoretically limited to the complexity class TC<sup>0</sup> Merrill and Sabharwal [2023]. To effectively address combinatorial problems with LLMs, sophisticated prompting strategies are required. One 

2 

basic approach is the Chain-of-Thought (CoT) prompting, introduced in Wei et al. [2022c], which encourages LLMs to articulate intermediate "thoughts" that inform the generation of the final output. This technique has given rise to advanced variations, including Self-consistency with CoT (CoT-SC), Tree-of-Thoughts (ToT), and Graph-of-Thought methods Wang et al. [2022], Yao et al. [2023], Zhang et al. [2024]. Additionally, decomposition prompting strategies can be employed Zhou et al. [2022], Khot et al. [2022], since they simplify complex tasks into smaller, manageable subtasks via symbolic programs or structured algorithms, thus improving the performance of LLMs. In our experiments, we found these techniques to be insufficient, leading us to propose the Self-Guiding Exploration method as a more effective solution for tackling combinatorial problem tasks. 

## **3 Preliminaries** 

We provide an overview of combinatorial problems, highlighting their inherent complexity with the classic example of the Traveling Salesman Problem (TSP) and an example of a combinatorial problem formulation in a prompt for use by a Large Language Model (LLM). **Combinatorial Problems.** Combinatorial problems involve decision-making processes where the goal is to assign binary decision variables _x ∈_ 0 _,_ 1 in order to optimize a cost function _g_ ( _x_ 1 _, ..., xn_ ), subject to task-specific constraints. A classic example of such a problem is the TSP. In the TSP, given a list of _n_ cities and the distances _dij_ between cities _i, j_ , the objective is to determine the shortest possible route that visits each city exactly once and returns to the starting city. _xij_ is used as the action variable, indicating whether the route progresses from city _i_ to city _j_ . The cost function to minimize in TSP is _g_ ( _x_ ) =<sup>�</sup><sup>_n_</sup> _i_ =1 � _nj_ =1<sup>_dijxij_,under the condition that all cities visited exactly</sup> once<sup>�</sup><sup>_n_</sup> _i_ =1<sup>_xij_= 1 and �</sup><sup>_n_</sup> _j_ =1<sup>_xij_= 1 for all</sup><sup>_i, j_.Combinatorial problems are generally categorized</sup> as NP-hard due to their inherent computational complexity. For instance, a TSP with _n_ cities presents ( _n −_ 1)! possible routes, rendering the evaluation of all potential solutions impractical and exceedingly time-consuming as _n_ increases. 

**Prompting Combinatorial Problems in LLMs.** To use LLM for solving CP tasks, we define _f_ as the interface function of a generative LLM model, which accepts high-dimensional discrete input tokens and generates outputs within the same token space ( _f_ : _W �→ W_ ). For each combinatorial problem task, the input _Q_ to the LLM can be explicitly defined in a textual format. This description delineates the specific goal alongside a list of variables tailored to the task at hand. For instance, the objective of the Traveling Salesman Problem (TSP) can be textually articulated as "Find a route that minimizes the total travel distance, visits each city exactly once, and starts and ends in the same city." Subsequently, the variables, such as the distances between cities _dij_ , are provided in a format such as "The distance between city _i_ and city _j_ is [number]", laying out all necessary parameters for the model to process and generate solutions. The model will then process this structured input _Q_ to produce the corresponding solution answer _A_ , where both _Q_ and _A_ are within token space _W_ ; formally, _A_ = _f_ ( _Q_ ). Given the inherent complexity of combinatorial problems, direct zero-shot prompting _f_ ( _Q_ ) is insufficient. Consequently, we propose a self-guiding exploration algorithm that employs metaheuristic-like strategies to effectively solve CP tasks. 

## **4 Method** 

In this section, we introduce Self-Guiding Exploration (SGE) method and provide a detailed explanation of its algorithm designed to tackle combinatorial problems. The method (Fig 1), inspired by metaheuristic approaches, synthesizes multiple heuristic methods. It generates various thought trajectories, with each trajectory representing a specific heuristic approach. These trajectories are then integrated to form the final solution. To overcome the challenges of executing complex heuristics through LLMs in one step, our algorithm utilizes a decomposition strategy. This approach breaks down each trajectory into smaller, more manageable subtasks, enabling the solution to progress through sequential, simpler steps. This general-purpose algorithm is tailored to adapt to a wide range of combinatorial problems without the constraints of task-specific exemplars for few-shot solution generation. 

3 



Figure 1: **Self-Guiding Exploration** . The generative model autonomously addresses a combinatorial problem task _Q_ through a five-phase process: (1) Exploration of _N_ solution trajectories, where each trajectory offers potential solutions; (2) Decomposition of these trajectories into _K_ subtasks, outlining specific steps for each method; (3) Resolution of each subtask, executing the outlined steps; (4) Feedback and Refinement, where feedback is gathered and used to refine each subtask; (5) Integration of all trajectories into a consolidated final solution _A_ . Distinct from traditional exploration/decomposition techniques, SGE(Q) functions entirely autonomously, eliminating the reliance on task-specific queries or manually created thought exemplars. This independence makes it universally applicable to all CP tasks without necessitating modifications. 



<!-- Start of picture text -->
Algorithm 1  Self-Guiding Exploration algorithm -  SGE ( · )<br>Require: query  Q , model  f , meta-prompts  Z , maximum recursion depth  D<br>1: Q N =  f ( Q, Zexplore ) ▷ Explore method trajectories<br>2: for  iteration n  ∈ 1 ,  2 , . . . , N do<br>3: Q n K =  f ( Q, Qn, Zdecomp ) ▷ Decompose trajectory subtasks<br>4: for  iteration k  ∈ 1 ,  2 , . . . , K do<br>5: if  f ( Q n k , Zcheck )  then ▷ Check if subtask is simple<br>6: Tk n =  f ( Q, T k  n − 1 , Qn k ) ▷ Execute subtask and get thought<br>7: else<br>8: Tk n =  SGE ( T n k− 1 ||Qn k , f, Z ) ▷ Recursive call of subtask<br>9: end if<br>10: Q n kfeedback =  f ( Q, Q k n, T k  n, Zfeedback ) ▷ Get feedback query<br>11: Tk n =  f ( Q, T k  n, Qn kfeedback ) ▷ Refine thought<br>12: end for<br>13: end for<br>14: A  =  f ( Q, TK 1 , ..., T K  N , Zintegrate ) ▷ Get answer<br><!-- End of picture text -->

### **4.1 Algorithm** 

The proposed method’s algorithm is segmented into five distinct phases, as outlined in Algorithm 1. These phases include exploring thought trajectories, decomposing each trajectory into subtasks, resolving each subtask to generate thoughts, obtaining feedback and refining the thoughts, and finally integrating all thoughts to formulate the answer. Each thought here represents one completed subtask. **Exploration.** During the exploration stage, the model tackles the overarching problem _Q_ by engaging with exploration meta-prompt. This prompt _Zexplore_ is structured as: "List all possible methods to solve this problem. Return them separated by new lines." This prompt stimulates the model to enumerate potential methodologies pertinent to _Q_ . The sequence is then divided into task-specific trajectories of queries _Q_<sup>_n_</sup> each incorporating a method to address _Q_ : 



**Decomposition.** Following exploration, each trajectory query _Q_<sup>_n_</sup> is processed through the model to break down the trajectory into actionable steps. The decomposition meta-prompt _Zdecomp_ is formulated as: "List all steps to use the method. Return them separated by new lines." This leads to 

4 

the generation of subtask queries that operationalize the trajectory method: 

### _Q_<sup>_n_</sup> K<sup>=</sup><sup>_f_(</sup><sup>_Q, Qn, Zdecomp_)</sup><sup>_._</sup> 

**Subtask Resolution.** Post-decomposition, the subtask queries _Q_<sup>_n_</sup> K<sup>are each split into</sup><sup>_K_individual</sup> queries and processed by the model to generate thoughts. The model initially evaluates if the task is easily solvable using the meta-prompt _Zcheck_ : "Is this problem easily solvable? Return yes or no": _f_ ( _Q_<sup>_n_</sup> _k_<sup>_, Zcheck_).If the response is affirmative, the model executes the subtask query</sup><sup>_Qn_</sup> _k_<sup>to generate a</sup> new thought: 



Otherwise, the model engages a recursive instance of the self-guiding exploration algorithm on _Q_<sup>_n_</sup> _k_ instead of the main task _Q_ to navigate and decompose the complex subtask, producing: 



**Feedback and Refinement.** In this stage, the model utilizes an additional meta-prompt _Zfeedback_ - "Give feedback to the proposed solution" - to generate feedback queries _Q_<sup>_n_</sup> _kfeedback_<sup>=</sup> _f_ ( _Q, Q_<sup>_n_</sup> _k_<sup>_, T_</sup> _k_<sup>_n, Zfeedback_).This guides the model in refining the initial responses through reevaluation</sup> and enhancement of the thoughts: 



**Integration.** Upon completion of all trajectories and their associated subtasks, the model employs a final meta-prompt _Zintegrate_ - "Integrate all previous findings and provide the final answer" - to amalgamate the last thoughts into a definitive solution answer: 



SGE draws inspiration from metaheuristic methods used to solve combinatorial problem tasks. Yet, due to its general-purpose nature and meta-prompts, it is also suitable for other tasks, beyond CPs. Essentially, it integrates elements of exploration-of-thought, decomposition, and refinement prompting strategies, but it does so without relying on task-specific prompts or solution exemplars. For additional information on these prompting strategies, see Section A.1 

## **5 Experiments** 

This section details the experimental setup and presents the results of our proposed method applied to combinatorial problem tasks, as well as its performance on other reasoning tasks commonly explored in LLM research. 

### **5.1 Setup** 

**CP tasks.** The experiments were conducted on six combinatorial tasks: Assignment Problem, Knapsack Problem, Bin Packing Problem, Traveling Salesman Problem, Vehicle Routing Problem, and Job Scheduling Problem. The Assignment Problem, classified as P-complete, can be optimally solved using the Hungarian Algorithm. In contrast, the other tasks are NP-hard and ordered by increasing complexity. For a more detailed discussion of these CP tasks, refer to Section A.2. We included five distinct problem sizes, involving 5, 10, 15, 20, and 30 elements (nodes) such as cities in the TSP/VRP. To facilitate these experiments, a dataset was created, comprising 100 randomly generated instances for each problem size. These instances were characterized by uniformly distributed variables, such as the positioning of cities in TSP/VRP or bin volume in the Bin Packing Problem, over an interval from 0 to 100. The experiments utilized an NVIDIA A100 SXM 40GB GPU, paired with two AMD EPYC 7742 CPUs (8 cores each) and 256GB RAM. On average, solving a problem instance with SGE takes between 1 and 3 minutes, depending on the LLM utilized. 

**Baselines.** We utilized four baseline prompting methods: Input-Output (IO) Direct Prompting, Chain-of-Thought Prompting, Self-Refine (Refine) Prompting, and Decomposition Prompting. The Input-Output (IO) approach involves a single prompt where the model is asked to provide a solution directly, without complex prompting. In this approach, we generate _N_ sample candidates by repeatedly prompting the model with the same query _Q_ , _N_ times. The responses are then aggregated through majority voting to identify the most common solution among the _N_ outputs. We employ the Self-Refine (Refine) method Madaan et al. [2023], which includes a feedback-refinement procedure 

5 

Table 1: **Percentage performance improvement compared to IO** on CP tasks using GPT-4 and Gemini-1.5 models. CoT uses majority voting, with the number of candidates equal to the number of thoughts produced by SGE. The metrics is quantified as percentage improvement in cost with respect to IO solution (the bigger it is the better). 

|||GP|T-4||Gem|ini-1.5|
|---|---|---|---|---|---|---|
|Task|CoT|Refine|Decomp|Ours<br>CoT|Refine|Decomp Ours|
|Assignment|11.46|14.47|33.80|**41.33** 11.66|13.98|31.94 **40.46**|
|Knapsack|15.37|17.16|51.95|**70.39** 13.85|16.85|48.62 **65.87**|
|Bin Packing|14.06|17.12|39.57|**74.72** 11.89|15.43|35.74 **67.63**|
|Travelling Salesman|13.64|15.75|38.49|**72.10** 14.34|15.90|36.36 **68.09**|
|Vehicle Routing|14.27|16.94|36.73|**71.92** 11.88|15.13|33.59 **68.02**|
|Job Scheduling|13.84|16.37|38.20|**75.33** 13.41|15.75|36.36 **67.89**|



that aligns closely with phase four of SGE. Additionally, we use the zero-shot Chain-of-Thought method Kojima et al. [2022], which is the basic technique among Exploration-of-Thought methods. Lastly, we implemented the Decomposition method as described in Zhou et al. [2023]. In our experiments, these baseline methods were tested across a range of five LLM models including GPT-4, GPT-3.5 by OpenAI, Gemini-1.5 by Google, and the Llama-2 series from Meta, which includes models with 70 billion and 7 billion parameters. We did not include prompting methods previously used in Liu et al. [2024], Masoud et al. [2024], Yang et al. [2024], as their prompting strategies showed inferior results compared to the zero-shot Chain-of-Thought approach when tested with our data. 

**Metrics.** In our study, each method’s performance is evaluated relative to IO (Input-Output) prompting. To quantify the improvement, we first measure the solution cost _gio_ for each combinatorial problem task using IO prompting (e.g., for the TSP, _gio_ =<sup>�</sup><sup>_n_</sup> _i_ =1 � _nj_ =1<sup>_dijxij_).Wethencal-</sup> culate the cost _gmethod_ using alternative methods. The percentage improvement is computed as 100 _×_<sup>_<u>gio−g</u>_</sup> _g_<sup>_<u>method</u>_</sup> _io_ . For problems of smaller sizes, we are able to obtain optimal solutions using the Google-OR-Tools solver through a brute force approach. In such instances, we measure the cost of the optimal solution _gopt_ and determine the optimality gap as 100 _×_<sup>_<u>gmethod</u>_</sup> _gopt_<sup>_−gopt_</sup> . 

### **5.2 Results on CP Tasks** 

To evaluate the general performance of SGE on combinatorial problems, we conducted experiments comparing performance improvement to IO of SGE and CoT, Decomposition, and Refinement baselines using GPT-4 and Gemini-1.5 LLM models. Table 1 gives the results on six combinatorial problem tasks. The results analysis shows that the SGE method consistently outperforms CoT, Refine, and Decomposition methods across all tasks. Notably, the magnitude of improvement escalates with the increasing complexity of the problems, from polynomial to exponential. The margin with the second-best method, Decomposition, ranges from 7 _._ 53% for the Assignment Problem to 37 _._ 13% for the JSP. This trend suggests that the IO method may struggle with the computational demands of NP-hard problems, where more sophisticated strategies like SGE provide significant advantages. For a comprehensive view of all experimental results, see Section A.6. 

To qualitatively evaluate the performance of the Exploration, Decomposition, and Refinement phases of SGE method, we assessed the LLM outputs for each phase across five random instances of each combinatorial problem task. Figure 2 illustrates an example of how our method addresses the TSP, showcasing outputs during each of the three phases of SGE. In the Exploration phase, the first box of Figure 2 displays how LLM _f_ generates a list of potential algorithms suitable for solving the TSP, such as heuristic approaches like Nearest Neighbor, metaheuristic techniques like Ant Colony, and Mixed Integer Linear Programming (MILP) method. This phase adapts to different combinatorial problems by suggesting tailored algorithms, like the Hungarian algorithm for the Assignment problem, Greedy algorithms for the Knapsack problem, and Clustering methods for the Vehicle Routing Problem (VRP). Each list of algorithms forms the foundation for generating diverse candidate solutions tailored to each specific problem. The Decomposition phase, depicted in the second box of Figure 2, breaks down each identified algorithm into specific subtasks. This example shows the decomposition of the Nearest Neighbor algorithm for the TSP, where the initial 

6 



<!-- Start of picture text -->
Example of Exploration of TSP<br>• Prompt : You are given a list of points with coordinates: (1): (0, 49); (2): (26, 41);<br>(3): (2, 29); (4): (49, 15); (5): (0, 23); We need to find the route that has a minimum<br>total length. List all possible methods to solve this problem. [Return conditions].<br>• Exploration Output :<br>– Nearest Neighbor Algorithm<br>– Christofides’ Algorithm<br>– Ant Colony Optimization<br>– Integer Linear Programming<br>Example of Decomposition of TSP<br>• Prompt : [Problem definition]. Nearest Neighbor Algorithm. List all steps to use the<br>method. [Return conditions].<br>• Decomposition Output :<br>– Select a Starting Point<br>– Find the Nearest Neighbor<br>– Update the Tour<br>– Repeat<br>– Return to the Starting Point<br>Example of Refinement of TSP<br>• Prompt : [Problem definition]. [Nearest Neighbor candidate solution]. Give feed-<br>back to the proposed solution.<br>• Refinement Output :<br>– Choose two edges<br>– Remove these edges and reconnect the two paths that were created in such a<br>way that the new connections do not cross over each other.<br>– Check if the new tour has a shorter distance than the previous tour. If it does,<br>keep the change. Otherwise, revert to the previous tour.<br>– Repeat this process until no improvements can be made.<br><!-- End of picture text -->

Figure 2: **Example of SGE inference** across the Exploration, Decomposition, and Refinement phases for the Traveling Salesman Problem. The figure displays three boxes, each illustrating the prompt structure and corresponding example output for each phase. 



Figure 3: **Effect of Problem Size on Performance Improvement** relative to the IO solution using `gpt-4` w/ code interpreter. The analysis spans problem instances of varying sizes, systematically presented from the smallest to the largest, specifically ranging from _n_ = 5 to _n_ = 20 nodes. Results are organized to highlight the impact of increasing problem complexity on the effectiveness of the solution. 

subtasks are simple enough for direct processing by model _f_ . However, more complex tasks, such as loops, undergo further decomposition using SGE in a recursive manner, with computational or programming tasks being handled using Python within models like GPT-4 and Gemini-1.5 equipped with a Code Interpreter. Finally, the Refinement phase, illustrated in the third box of Figure 2, focuses on enhancing the candidate solutions developed in the previous stage. This example pertains to refining a solution derived from the Nearest Neighbor algorithm for the TSP by implementing the 2-opt algorithm. Renowned for its effectiveness in TSP and VRP contexts, the 2-opt algorithm optimizes the initial solution to find locally optimal solutions within a specific neighborhood, thus improving the overall quality of the candidate solutions. This example shows that SGE method adapts its approach to suit different combinatorial problems, finding a special set of heuristics for each task. 

7 

Table 2: **Optimality gap** of prompting methods using `gpt-4` w/ code interpreter. The results are represented as performance percentage difference compared to optimal solutions (the smaller it is, the better). 

|**Size**|**Method**|**Assignment **|**Knapsack **|**Bin Packing**|**TSP**|**VRP**|**JSP**|
|---|---|---|---|---|---|---|---|
|S|IO|45.45|90.10|108.2|100.3|102.0|105.3|
|DE|CoT|39.33|66.88|78.24|81.15|78.17|79.41|
|O|Refine|36.42|61.98|77.40|71.62|72.49|71.72|
|5 N|Decomp|14.66|21.56|40.00|43.62|40.65|44.15|
||Ours|**2.500**|**8.050**|**9.060**|**8.27**|**11.92 **|**9.300**|
|S|IO|46.84|103.5|112.8|116.9|116.3|108.2|
|DE|CoT|39.70|73.84|85.08|89.01|89.48|85.21|
|O|Refine|37.32|72.62|86.25|85.59|83.31|78.43|
|8 N|Decomp|18.49|26.43|52.73|53.48|54.43|49.81|
||Ours|**8.290**|**14.88**|**20.95**|**15.19 **|**19.65 **|**21.26**|
|S|IO|49.11|101.5|120.7|121.6|118.5|117.6|
|DE|CoT|41.70|79.33|93.84|86.84|90.05|89.29|
|NO|Refine|40.35|77.09|82.23|88.57|88.40|87.02|
|2|Decomp|21.12|35.82|55.40|57.51|59.19|56.01|
|1|Ours|**11.26**|**16.82**|**22.38**|**16.12 **|**24.00 **|**22.86**|





Figure 4: **Effect of Model Choice on Performance Improvement** relative to the IO solution. 

**Effect of Problem Size on SGE Performance.** To evaluate the effect of problem size on SGE performance, we conducted experiments on all six tasks with input sizes of 5, 8, 12, 15, and 20 nodes using the GPT-4 model. Figure 3 gives the results of these experiments. The results analysis shows that generally, an increase in problem complexity, as determined by the size of the problem input, negatively influences performance improvement; larger problem sizes result in diminished performance improvement of the SGE method compared to IO. Specifically, tasks with 20 input nodes consistently exhibit lower performance improvements relative to the IO method than tasks with 5 input nodes. However, when comparing less disparate sizes, such as 8 and 12 nodes, the differential impact on performance is less pronounced and can occasionally be positive. 

**Gap Between SGE Performance and the Global Optimum.** To evaluate the gap between SGE solutions and global optimum solutions, we conducted experiments on small problem sizes involving 5, 8, and 12 nodes, utilizing the brute force method via Google-OR-Tools to determine the global optimum. Figure 2 provides the results of these experiments in terms of the percentage gap between the performance of SGE and optimal solutions. The results analysis shows that generally, the SGE method exhibits a smaller optimality gap across all tasks when compared to baseline methods. This advantage is particularly pronounced for more complex problems such as Bin Packing, TSP, VRP, and JSP. For instance, SGE achieves a 12.16% smaller optimality gap on the Assignment task than the next best Decomposition method and a 34.85% smaller gap on the JSP. 

**Effect of LLM Selection on SGE Performance.** To evaluate the impact of model selection on SGE performance, we conducted experiments comparing different models, including GPT-4, Gemini-1.5, GPT-3.5, Llama-2-70b, and Llama-2-7b models. Figure 4 provides the results of these experiments. The results analysis shows that GPT-4 and Gemini-1.5 demonstrate significantly better performance compared to other models across all tasks. A notable feature of both models is the integration of a Code Interpreter (CI) tool, which appears crucial for combinatorial problem tasks as it enables the 

8 

Table 3: **Results for reasoning tasks** using `gpt-4` with a code interpreter are presented as accuracies on benchmark test sets. 

|**Method**||**Arith**|**metic**||**Comm**|**onsens**|**e**|**Symbolic **|**Avg.**|
|---|---|---|---|---|---|---|---|---|---|
||AQUA|GSM8K|SVAMP|ASDiv|StrategyQA|CSQA|ARC|LastLetter||
|IO Prompting|67.30|87.04|88.34|90.10|78.40|81.14|87.52|81.98|82.73|
|CoT Prompting|69.57|89.76|91.58|93.32|81.16|84.15|90.80|85.18|85.69|
|Refine Prompting|69.68|89.80|91.00|93.10|81.26|83.50|91.09|84.82|85.53|
|Decomp Prompting|69.99|91.85|92.16|94.08|82.08|84.88|91.76|85.64|86.43|
|Ours|**74.63**|**97.35**|**98.16**|**97.24**|**83.49**|**85.68 **|**93.28**|**86.96**|**89.60**|



Table 4: **Performance vs Efficiency** of prompting methods using `gpt-4` w/ code interpreter. The results are represented as performance percentage improvement compared to IO solution and number of model _f_ calls. 

|Method|Performance Improvement|Function Calls|
|---|---|---|
|CoT|13.77|58.32|
|Refine|16.30|58.32|
|Decomp|39.79|31.04|
|Ours|67.63|58.32|



models to execute generated code and evaluate solution performance directly. In contrast, models lacking a CI tool, such as GPT-3.5, Llama-2-70b, and Llama-2-7b, exhibit poorer outcomes, with GPT-3.5 slightly outperforming the Llama models. The comparison between Llama models indicates that the size of the model with 70 billion versus 7 billion parameters does not significantly influence performance. This suggests that model size alone does not guarantee substantial performance improvements in combinatorial tasks. 

**Trade-off Between Performance and Cost in SGE.** To evaluate the cost-effectiveness of different methods, we conducted experiments to compare the average performance improvement per method against the average number of LLM calls utilized to solve each combinatorial problem instance. Table 4 gives the results of these experiments, where the number of function calls in CoT and Refine methods was explicitly controlled to make them equal to SGE function calls. The results analysis shows that the SGE method achieves a 27.84% better performance compared to the Decomposition method but requires 87.89% more function calls. Thus, while SGE offers superior performance, it does so at a marginally higher operational cost. Therefore, the application of this method is particularly justified in scenarios where performance gains are prioritized over cost efficiency. 

### **5.3 Results on Reasoning Tasks** 

To evaluate the versatility of SGE in handling different types of tasks, we conducted experiments across eight datasets commonly referenced in LLM research, categorized into three distinct task types: arithmetic, commonsense reasoning, and symbolic reasoning. Table 3 gives the results of these experiments, with each dataset comprising train and test splits where SGE and baseline methods were applied to the test splits. The results analysis shows that the SGE method demonstrates incremental but consistently superior performance across all task categories. Notably, the method shows particular strength in arithmetic tasks, where it achieves an average improvement of 4.83%, compared to 1.24% in commonsense reasoning tasks and 1.32% in symbolic reasoning tasks. This demonstrates the method’s applicability and effectiveness across a diverse range of tasks, extending beyond combinatorial problems. 

## **6 Conclusion** 

This study has explored the application of Large Language Models to Combinatorial Problems, a category of tasks known for their NP-hardness. Our research introduced a ’Self-Guiding Exploration’ prompting strategy that effectively utilizes the inherent strengths of LLMs. By generating multiple 

9 

thought trajectories tailored to various CPs and autonomously decomposing them into manageable subtasks. Our findings confirm that SGE outperforms existing strategies, improving optimization performance by 27.84% and achieving a 2.46% higher accuracy in reasoning tasks. Notably, SGE shows a 34.85% smaller gap with the global optimum on complex tasks like the Job Sheduling Problem compared to baseline methods. These results underline the potential of advanced LLM strategies in complex problem-solving scenarios, suggesting that the right techniques can enhance the utility of LLMs in critical logistics and resource management applications. 

Despite the performance improvements demonstrated by the SGE, several limitations have emerged that merit attention. Firstly, SGE performance depends on the choice of language model. Secondly, the operational costs associated with SGE are notably higher; it requires 87.89% more function calls than the Decomposition method. These issues present clear avenues for future research. Enhancing SGE’s computational efficiency while maintaining its high performance could broaden its applicability and make it a more practical choice for a wider range of problems. 

10 

## **References** 

- Samuel Kwame Amponsah, Dominic Otoo, Said Salhi, and Ebenezer Quayson. Proposed heuristic method for solving assignment problems. _American Journal of Operations Research_ , 06:436–441, 01 2016. doi: 10.4236/ajor.2016.66040. 

- M Emin Aydin and Ercan Öztemel. Dynamic job-shop scheduling using reinforcement learning agents. _Robotics and Autonomous Systems_ , 33(2-3):169–178, 2000. 

- Irwan Bello, Hieu Pham, Quoc V Le, Mohammad Norouzi, and Samy Bengio. Neural combinatorial optimization with reinforcement learning. _arXiv preprint arXiv:1611.09940_ , 2016. 

- Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, Sandhini Agarwal, Ariel Herbert-Voss, Gretchen Krueger, Tom Henighan, Rewon Child, Aditya Ramesh, Daniel M. Ziegler, Jeffrey Wu, Clemens Winter, Christopher Hesse, Mark Chen, Eric Sigler, Mateusz Litwin, Scott Gray, Benjamin Chess, Jack Clark, Christopher Berner, Sam McCandlish, Alec Radford, Ilya Sutskever, and Dario Amodei. Language models are few-shot learners. In Hugo Larochelle, Marc’Aurelio Ranzato, Raia Hadsell, Maria-Florina Balcan, and Hsuan-Tien Lin, editors, _Advances in Neural Information Processing Systems 33: Annual Conference on Neural Information Processing Systems 2020, NeurIPS 2020, December 6-12, 2020, virtual_ , 2020. URL `https://proceedings.neurips.cc/paper/2020/hash/ 1457c0d6bfcb4967418bfb8ac142f64a-Abstract.html` . 

- Aakanksha Chowdhery, Sharan Narang, Jacob Devlin, Maarten Bosma, Gaurav Mishra, Adam Roberts, Paul Barham, Hyung Won Chung, Charles Sutton, Sebastian Gehrmann, Parker Schuh, Kensen Shi, Sasha Tsvyashchenko, Joshua Maynez, Abhishek Rao, Parker Barnes, Yi Tay, Noam Shazeer, Vinodkumar Prabhakaran, Emily Reif, Nan Du, Ben Hutchinson, Reiner Pope, James Bradbury, Jacob Austin, Michael Isard, Guy Gur-Ari, Pengcheng Yin, Toju Duke, Anselm Levskaya, Sanjay Ghemawat, Sunipa Dev, Henryk Michalewski, Xavier Garcia, Vedant Misra, Kevin Robinson, Liam Fedus, Denny Zhou, Daphne Ippolito, David Luan, Hyeontaek Lim, Barret Zoph, Alexander Spiridonov, Ryan Sepassi, David Dohan, Shivani Agrawal, Mark Omernick, Andrew M. Dai, Thanumalayan Sankaranarayana Pillai, Marie Pellat, Aitor Lewkowycz, Erica Moreira, Rewon Child, Oleksandr Polozov, Katherine Lee, Zongwei Zhou, Xuezhi Wang, Brennan Saeta, Mark Diaz, Orhan Firat, Michele Catasta, Jason Wei, Kathy Meier-Hellstern, Douglas Eck, Jeff Dean, Slav Petrov, and Noah Fiedel. Palm: Scaling language modeling with pathways. _Journal of Machine Learning Research_ , 24(240):1–113, 2023. URL `http://jmlr.org/papers/v24/22-1144.html` . 

- Michel Deudon, Pierre Cournut, Alexandre Lacoste, Yossiri Adulyasak, and Louis-Martin Rousseau. Learning heuristics for the tsp by policy gradient. In _International conference on the integration of constraint programming, artificial intelligence, and operations research_ , pages 170–181. Springer, 2018. 

- Thomas Gabel and Martin Riedmiller. Adaptive reactive job-shop scheduling with reinforcement learning agents. _International Journal of Information Technology and Intelligent Computing_ , 24 (4):14–18, 2008. 

- Rajeev Kumar Goel, Raman Maini, and Sandhya Bansal. Vehicle routing problem with time windows having stochastic customers demands and stochastic service times: Modelling and solution. _J. Comput. Sci._ , 34:1–10, 2019. 

Google. Or-tools, 2023. URL `https://developers.google.com/optimization` . 

- Zangir Iklassov, Dmitrii Medvedev, Ruben Solozabal Ochoa de Retana, and Martin Takác. On the study of curriculum learning for inferring dispatching policies on the job shop scheduling. In _Proceedings of the Thirty-Second International Joint Conference on Artificial Intelligence, IJCAI 2023, 19th-25th August 2023, Macao, SAR, China_ , pages 5350–5358. ijcai.org, 2023a. doi: 10.24963/IJCAI.2023/594. URL `https://doi.org/10.24963/ijcai.2023/594` . 

- Zangir Iklassov, Ikboljon Sobirov, Ruben Solozabal, and Martin Takác. Reinforcement learning approach to stochastic vehicle routing problem with correlated demands. _IEEE Access_ , 11: 87958–87969, 2023b. doi: 10.1109/ACCESS.2023.3306076. URL `https://doi.org/10. 1109/ACCESS.2023.3306076` . 

11 

- Tushar Khot, Harsh Trivedi, Matthew Finlayson, Yao Fu, Kyle Richardson, Peter Clark, and Ashish Sabharwal. Decomposed prompting: A modular approach for solving complex tasks. _arXiv preprint arXiv:2210.02406_ , 2022. 

- Takeshi Kojima, Shixiang Shane Gu, Machel Reid, Yutaka Matsuo, and Yusuke Iwasawa. Large language models are zero-shot reasoners. In _NeurIPS_ , 2022. URL `http://papers.nips.cc/paper_files/paper/2022/hash/ 8bb0d291acd4acf06ef112099c16f326-Abstract-Conference.html` . 

- Wouter Kool, Herke Van Hoof, and Max Welling. Attention, learn to solve routing problems! _arXiv preprint arXiv:1803.08475_ , 2018. 

- Guoming Li and Junhua Li. An improved tabu search algorithm for the stochastic vehicle routing problem with soft time windows. _IEEE Access_ , 8:158115–158124, 2020. 

- Fei Liu, Xialiang Tong, Mingxuan Yuan, Xi Lin, Fu Luo, Zhenkun Wang, Zhichao Lu, and Qingfu Zhang. Evolution of heuristics: Towards efficient automatic algorithm design using large language mode, 2024. 

- Aman Madaan, Niket Tandon, Prakhar Gupta, Skyler Hallinan, Luyu Gao, Sarah Wiegreffe, Uri Alon, Nouha Dziri, Shrimai Prabhumoye, Yiming Yang, Sean Welleck, Bodhisattwa Prasad Majumder, Shashank Gupta, Amir Yazdanbakhsh, and Peter Clark. Self-refine: Iterative refinement with selffeedback. _ArXiv preprint_ , abs/2303.17651, 2023. URL `https://arxiv.org/abs/2303.17651` . 

- Sridhar Mahadevan and Georgios Theocharous. Optimizing production manufacturing using reinforcement learning. In _FLAIRS conference_ , volume 372, page 377, 1998. 

- Sridhar Mahadevan, Nicholas Marchalleck, Tapas K Das, and Abhijit Gosavi. Self-improving factory simulation using continuous-time average-reward reinforcement learning. In _Machine Learning Interantional Workshop_ , pages 202–210, 1997. 

- Hongzi Mao, Malte Schwarzkopf, Shaileshh Bojja Venkatakrishnan, Zili Meng, and Mohammad Alizadeh. Learning scheduling algorithms for data processing clusters. In _Proceedings of the ACM special interest group on data communication_ , pages 270–288. 2019. 

- Mahmoud Masoud, Ahmed Abdelhay, and Mohammed Elhenawy. Exploring combinatorial problem solving with large language models: A case study on the travelling salesman problem using gpt-3.5 turbo, 2024. 

- William Merrill and Ashish Sabharwal. The parallelism tradeoff: Limitations of log-precision transformers. _Transactions of the Association for Computational Linguistics_ , 11:531–545, 2023. doi: 10.1162/tacl_a_00562. URL `https://aclanthology.org/2023.tacl-1.31` . 

- Mohammadreza Nazari, Afshin Oroojlooy, Lawrence V Snyder, and Martin Takáˇc. Reinforcement learning for solving the vehicle routing problem. In _Conference on Neural Information Processing Systems, NeurIPS 2018_ , 2018. 

- Afshin Oroojlooyjadid, Lawrence V Snyder, and Martin Takáˇc. Applying deep learning to the newsvendor problem. _IISE Transactions_ , 52(4):444–463, 2020. 

- Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida, Carroll L. Wainwright, Pamela Mishkin, Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, John Schulman, Jacob Hilton, Fraser Kelton, Luke Miller, Maddie Simens, Amanda Askell, Peter Welinder, Paul F. Christiano, Jan Leike, and Ryan Lowe. Training language models to follow instructions with human feedback. In _NeurIPS_ , 2022. URL `http://papers.nips.cc/paper_files/paper/2022/hash/ b1efde53be364a73914f58805a001731-Abstract-Conference.html` . 

- Tantikorn Pichpibul and Ruengsak Kawtummachai. A heuristic approach based on clarke-wright algorithm for open vehicle routing problem. _The Scientific World Journal_ , 2013, 2013. 

- Veronique Sels, Nele Gheysen, and Mario Vanhoucke. A comparison of priority rules for the job shop scheduling problem under different flow time-and tardiness-related objective functions. _International Journal of Production Research_ , 50(15):4255–4270, 2012. 

12 

- Penghao Sun, Zehua Guo, Junchao Wang, Junfei Li, Julong Lan, and Yuxiang Hu. Deepweave: Accelerating job completion time with deep reinforcement learning-based coflow scheduling. In _Proceedings of the Twenty-Ninth International Conference on International Joint Conferences on Artificial Intelligence_ , pages 3314–3320, 2021. 

- Mirac Suzgun, Nathan Scales, Nathanael Schärli, Sebastian Gehrmann, Yi Tay, Hyung Won Chung, Aakanksha Chowdhery, Quoc V. Le, Ed Chi, Denny Zhou, and Jason Wei. Challenging big-bench tasks and whether chain-of-thought can solve them. In Anna Rogers, Jordan L. Boyd-Graber, and Naoaki Okazaki, editors, _Findings of the Association for Computational Linguistics: ACL 2023, Toronto, Canada, July 9-14, 2023_ , pages 13003–13051. Association for Computational Linguistics, 2023. doi: 10.18653/v1/2023.findings-acl.824. URL `https://doi.org/10.18653/v1/2023. findings-acl.824` . 

- Romal Thoppilan, Daniel De Freitas, Jamie Hall, Noam M. Shazeer, Apoorv Kulshreshtha, Heng-Tze Cheng, Alicia Jin, Taylor Bos, Leslie Baker, Yu Du, Yaguang Li, Hongrae Lee, Huaixiu Zheng, Amin Ghafouri, Marcelo Menegali, Yanping Huang, Maxim Krikun, Dmitry Lepikhin, James Qin, Dehao Chen, Yuanzhong Xu, Zhifeng Chen, Adam Roberts, Maarten Bosma, Yanqi Zhou, Chung-Ching Chang, I. A. Krivokon, Willard James Rusch, Marc Pickett, Kathleen S. MeierHellstern, Meredith Ringel Morris, Tulsee Doshi, Renelito Delos Santos, Toju Duke, Johnny Hartz Søraker, Ben Zevenbergen, Vinodkumar Prabhakaran, Mark Díaz, Ben Hutchinson, Kristen Olson, Alejandra Molina, Erin Hoffman-John, Josh Lee, Lora Aroyo, Ravindran Rajakumar, Alena Butryna, Matthew Lamm, V. O. Kuzmina, Joseph Fenton, Aaron Cohen, Rachel Bernstein, Ray Kurzweil, Blaise Aguera-Arcas, Claire Cui, Marian Croak, Ed Huai hsin Chi, and Quoc Le. Lamda: Language models for dialog applications. _ArXiv preprint_ , abs/2201.08239, 2022. URL `https://arxiv.org/abs/2201.08239` . 

- Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez, Łukasz Kaiser, and Illia Polosukhin. Attention is all you need. In _NeurIPS_ , pages 5998–6008, 2017. 

- Oriol Vinyals, Meire Fortunato, and Navdeep Jaitly. Pointer networks. _Advances in neural information processing systems_ , 28, 2015. 

- Libing Wang, Xin Hu, Yin Wang, Sujie Xu, Shijun Ma, Kexin Yang, Zhijun Liu, and Weidong Wang. Dynamic job-shop scheduling in smart manufacturing using deep reinforcement learning. _Computer Networks_ , 190:107969, 2021. 

- Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc Le, Ed Chi, Sharan Narang, Aakanksha Chowdhery, and Denny Zhou. Self-consistency improves chain of thought reasoning in language models. _arXiv preprint arXiv:2203.11171_ , 2022. 

- Jason Wei, Yi Tay, Rishi Bommasani, Colin Raffel, Barret Zoph, Sebastian Borgeaud, Dani Yogatama, Maarten Bosma, Denny Zhou, Donald Metzler, Ed H. Chi, Tatsunori Hashimoto, Oriol Vinyals, Percy Liang, Jeff Dean, and William Fedus. Emergent abilities of large language models. _Transactions on Machine Learning Research_ , 2022a. ISSN 2835-8856. URL `https://openreview.net/forum?id=yzkSU5zdwD` . Survey Certification. 

- Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, brian ichter, Fei Xia, Ed Chi, Quoc V Le, and Denny Zhou. Chain-of-thought prompting elicits reasoning in large language models. In S. Koyejo, S. Mohamed, A. Agarwal, D. Belgrave, K. Cho, and A. Oh, editors, _Advances in Neural Information Processing Systems_ , volume 35, pages 24824–24837. Curran Associates, Inc., 2022b. URL `https://proceedings.neurips.cc/paper_files/paper/2022/file/ 9d5609613524ecf4f15af0f7b31abca4-Paper-Conference.pdf` . 

- Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia, Ed Chi, Quoc V Le, Denny Zhou, et al. Chain-of-thought prompting elicits reasoning in large language models. _Advances in Neural Information Processing Systems_ , 35:24824–24837, 2022c. 

- Chengrun Yang, Xuezhi Wang, Yifeng Lu, Hanxiao Liu, Quoc V. Le, Denny Zhou, and Xinyun Chen. Large language models as optimizers, 2024. 

- Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran, Thomas L Griffiths, Yuan Cao, and Karthik Narasimhan. Tree of thoughts: Deliberate problem solving with large language models. _arXiv preprint arXiv:2305.10601_ , 2023. 

13 

- Di Zhang, Dong Dai, Youbiao He, Forrest Sheng Bao, and Bing Xie. Rlscheduler: an automated hpc batch job scheduler using reinforcement learning. In _SC20: International Conference for High Performance Computing, Networking, Storage and Analysis_ , pages 1–15. IEEE, 2020. 

- Wei Zhang and Thomas G Dietterich. A reinforcement learning approach to job-shop scheduling. In _IJCAI_ , volume 95, pages 1114–1120. Citeseer, 1995. 

- Yizhou Zhang, Lun Du, Defu Cao, Qiang Fu, and Yan Liu. Prompting with divide-and-conquer program makes large language models discerning to hallucination and deception, 2024. 

- Zhuosheng Zhang, Aston Zhang, Mu Li, and Alex Smola. Automatic chain of thought prompting in large language models. In _The Eleventh International Conference on Learning Representations, ICLR 2023, Kigali, Rwanda, May 1-5, 2023_ . OpenReview.net, 2023. URL `https://openreview. net/pdf?id=5NTt8GFjUHkr` . 

- Denny Zhou, Nathanael Schärli, Le Hou, Jason Wei, Nathan Scales, Xuezhi Wang, Dale Schuurmans, Claire Cui, Olivier Bousquet, Quoc Le, et al. Least-to-most prompting enables complex reasoning in large language models. _arXiv preprint arXiv:2205.10625_ , 2022. 

- Denny Zhou, Nathanael Schärli, Le Hou, Jason Wei, Nathan Scales, Xuezhi Wang, Dale Schuurmans, Claire Cui, Olivier Bousquet, Quoc V. Le, and Ed H. Chi. Least-to-most prompting enables complex reasoning in large language models. In _The Eleventh International Conference on Learning Representations, ICLR 2023, Kigali, Rwanda, May 1-5, 2023_ . OpenReview.net, 2023. URL `https://openreview.net/pdf?id=WZH7099tgfM` . 

14 

## **A Appendix** 

### **A.1 Baseline Prompting Techniques** 

Combinatorial problems are too complex for solving using direct approach. To solve in several shots, different methods can be used such as few-shot prompting, chain-of-thought, exploration-of-thought, decomposition, and self-refine advanced prompting techniques. Traditional few-shot prompting involves teaching an LLM to derive an answer _A_ to a query _Q_ using a limited set of contextual examples _D_ = _{E_ 1 _, ..., E|D|}_ , where _A_ = _f_ ( _Q, D_ ). In the simplest few-shot setup, examples are formatted as _Ej_ = ( _Qj, Aj_ ), where each _Qj, Aj_ are corresponding prompt and solution of example problem _j_ . For Chain of Thought (CoT) prompting, the objective shifts to generating a sequence of intermediate reasoning steps, or "thoughts" _T_ , and subsequently deriving the final answer from _T_ . These in-context examples are structured as _Ej_ = ( _Qj,_ ( _Tj,_ 1 _, . . . , Tj,k_ ) _, Aj_ ). Exploration-ofThought techniques, such as those described in Wang et al. [2022], Yao et al. [2023], focus on dividing the problem _Q_ into _K_ subproblems and auto-generating thoughts _Tk_ through subproblem queries _Qk_ with _Tk_ = _f_ ( _Qk, Tk−_ 1).The ultimate answer is then computed as _A_ = _f_ ( _Q, TK_ ). In addition to that, in Tree-of-Thought (ToT) and Graph-of-Thought (GoT) prompting strategies, the problem is split into _N_ thought trajectories _Tk_<sup>_n_, using pre-determined subqueries</sup><sup>_Qn_</sup> _k_<sup>, with the final answer determined by</sup> _A_ = _f_ ( _Q, TK_<sup>1</sup><sup>_, ..., T_</sup> _K_<sup>_N_).These strategies necessitate manually identifying effective subqueries</sup><sup>_Qn_</sup> _k_<sup>for</sup> each specific task (e.g., arithmetic, commonsense, symbolic). Decomposition prompting strategies, as referenced in Zhou et al. [2022], Khot et al. [2022] get _Q_<sup>_n_</sup> _k_<sup>subqueries through in-context examples</sup> formatted similarly to CoT exemplars: _Ej_ = �( _Qj,_ � _Qj,_ 1 _, Tj,_ 1) _, ...,_ ( _Qj,kj , Tj,kj_ )� _Aj_ �. Another prompting method called self-refinement Madaan et al. [2023] uses feedback and refine procedures to generate feedback queries _Q_<sup>_n_</sup> _kfeedback_<sup>andsubsequentlyrefinethoughts</sup><sup>_T n_</sup> _k_<sup>.Inourresearch</sup> we combined these advanced techniques and updated them into new method called self-guiding exploration to enhance performance of LLMs for CPs. 

### **A.2 Combinatorial Problems** 

Combinatorial problems are decision problems where solver needs to assign binary decision variable _x ∈{_ 0 _,_ 1 _}_ to minimize some cost function or maximize reward function given input _C_ . 

**Assignment Problem.** Despite not being classified as NP-hard and solvable in polynomial time using the Hungarian algorithm, the Assignment Problem remains a fundamental combinatorial challenge. This problem entails optimally assigning _n_ tasks to _n_ workers, aiming to minimize the total cost or maximize the total efficiency of the assignments. The input array _C_ is represented as _n × n_ cost matrix, where the element at the _i_<sup>_th_</sup> row and _j_<sup>_th_</sup> column represents the cost of assigning the _j_<sup>_th_</sup> task to the _i_<sup>_th_</sup> worker. The goal is essentially about finding a one-to-one matching between workers and tasks with the objective of minimizing the total cost, i.e. 





**Knapsack Problem.** The knapsack problem is a classic combinatorial problem, focusing on resource allocation. It is a decision problem in which the goal is to pack items from a set of items with given weights _w_ and values _v_ into a container with a maximum capacity _W_ . The input array _C_ is represented as _n ×_ 2 matrix with volume and value information of every item _i_ . The goal is to maximize total value of packed items without exceeding container capacity, i.e. 



15 

**Bin Packing Problem.** The bin packing problem is a combinatorial problem that involves efficiently packing _n_ objects of different sizes _w_ into a finite number of _k_ bin containers of fixed capacity _W_ in a way that minimizes the number of bins used. The input array _C_ is represented as _n ×_ 1 vector with size information of every item _i_ , 



**Travelling Salesman Problem.** In the travelling salesman problem, given a list of _n_ cities and the distances _d_ between each pair of cities, what is the shortest possible route that visits each city exactly once and returns to the origin city. The input array _C_ is represented as _n × n_ cost matrix, where the element at the _i_<sup>_th_</sup> row and _j_<sup>_th_</sup> column represents the cost _dij_ of travelling between these two cities, 



**Vehicle Routing Problem.** The vehicle routing problem generalizes the TSP by incorporating multiple vehicles into the route planning. The VRP seeks to determine the optimal set of routes for a fleet of _K_ vehicles with maximum capacity _P_ to deliver goods to _n_ customers, typically from a central depot, with the objective of minimizing the total travel cost. In addition to TSP, the input _C_ also includes the demand of each customer, i.e. 



In cases when the capacity _P_ is less than the customer’s demand, the vehicle will go between the depot and the customer until the demand is satisfied. 

**Job Scheduling Problem.** The job scheduling problem focuses on scheduling _n_ jobs on _m_ machines, where each job _i_ consists of a sequence of _m_ operations that need to be processed in a specified order. Each operation requires a specific machine for a certain period of time, and each machine can handle only one operation at a time. The input array _C_ is represented as _n × m ×_ 2 cost matrix, which stores machine id and completion time for every operation _j_ of every job _i_ . The primary objective is to minimize the makespan, which is the total time required to complete all jobs, effectively reducing the time from the start of the first operation to the completion of the last operation across all jobs. 

**Challenges in Solving Combinatorial Problems.** The difficulty of the combinatorial problems like TSP, VRP, JSP, and Knapsack problem stems from several intrinsic and mathematical characteristics common among them. These problems are typically classified as NP-hard, which fundamentally contributes to their computational complexity. As the number of elements (cities, jobs, items, etc.) increases, the number of possible combinations or permutations explodes exponentially. For instance, the TSP with _n_ cities has ( _n −_ 1)! possible routes to evaluate. This exponential growth means that the time required to examine all possible solutions becomes impractically long even for relatively small _n_ . In addition to that combinatorial problems involve decisions that are interdependent, where the choice for one element affects the options and costs for others. For example, in the JSP, the order in which jobs are processed on one machine can affect the scheduling for other machines. 

16 

**Applicability of SGE to Combinatorial Problems.** For combinatorial problems, obtaining exact solutions is generally computationally prohibitive. Consequently, approximation algorithms and heuristic methods are frequently employed to tackle these challenges. Typically, these problems are broken down into more manageable subproblems. Initial solutions are then generated using heuristic functions, which are subsequently refined through additional heuristic techniques to enhance solution quality. The SGE approach is particularly well-suited for combinatorial problems as it embodies this multi-stage process: it systematically decomposes the problem, explores potential solving methods, and iteratively refines the solutions. 

### **A.3 Effect of Problem Size on SGE Performance** 

Table 5: **Effect of problem size** on _SGE_ performance using `gpt-4` w/ code interpreter. The results are represented as performance percentage improvement compared to IO solution (the bigger it is the better). 

|**Size**|**Assignment **|**Knapsack **|**Bin Packing**|**TSP**|**VRP**|**JSP**|
|---|---|---|---|---|---|---|
|5|44.05|75.94|90.92|76.77|80.47|87.81|
|8|42.03|77.14|75.92|80.12|80.78|71.68|
|12|42.65|72.50|80.36|79.93|76.18|77.08|
|15|41.78|71.70|71.61|73.24|78.41|79.73|
|20|40.24|67.21|69.78|67.14|65.19|76.29|
|25|39.83|67.07|66.35|60.17|60.87|69.52|
|30|38.75|61.15|68.13|67.32|61.55|65.20|



### **A.4 Effect of Model Selection on SGE Performance** 

Table 6: **Effect of model selection** on _SGE_ performance using `gpt-4` w/ code interpreter. The results are represented as performance percentage improvement compared to IO solution (the bigger it is the better). 

|Task|GPT-3.5|GPT-4|Gemini-1.5|Llama-2-7b|Llama-2-70b|
|---|---|---|---|---|---|
|Assignment|25.35|41.33|40.46|23.19|24.01|
|Knapsack|34.43|70.39|65.87|28.37|32.82|
|Bin Packing|35.83|74.72|67.63|29.78|33.76|
|Travelling Salesman|35.26|72.10|68.09|30.65|33.77|
|Vehicle Routing|36.28|71.92|68.02|30.55|33.65|
|Job Scheduling|35.02|75.33|67.89|30.39|34.42|



### **A.5 Results on Reasoning Tasks** 

Table 7: **Results for reasoning tasks** using `gpt-3.5` with a code interpreter are presented as accuracies on benchmark test sets. 

|**Method**||**Arith**|**metic**||**Comm**|**onsens**|**e**|**Symbolic**|**Avg.**|
|---|---|---|---|---|---|---|---|---|---|
||AQUA|GSM8K|SVAMP|ASDiv|StrategyQA|CSQA|ARC|LastLetter||
|IO Prompting|44.16|57.05|60.02|65.43|54.70|55.68|64.35|56.21|57.20|
|CoT Prompting|58.35|75.84|80.30|87.39|72.97|74.36|85.48|74.63|76.17|
|Refine Prompting|58.81|76.10|80.44|87.35|73.38|74.13|85.71|74.78|76.34|
|Decomp Prompting|71.64|82.11|84.34|89.83|76.16|78.84|87.48|77.89|81.11|
|Ours|**72.84**|**86.18**|**86.44**|**90.17**|**77.44**|**79.09 **|**87.83**|**78.78**|**82.27**|



17 

### **A.6 Complete Results of Combinatorial Problem Experiments** 

Table 8: Comparison of various combinatorial problems based on their average cost per problem size, using `gpt-3.5` . The Knapsack problem aims to maximize returns, while other problems focus on minimizing costs. 

|**Size**|**Method**|**Assignment **|**Knapsack **|**Bin Packing**|**TSP**|**VRP**|**JSP**|
|---|---|---|---|---|---|---|---|
||Avg.|102.23|710.53|13.480|679.26|809.67|3873.98|
|ES|IO|119.25|604.83|15.220|784.98|951.89|4499.38|
|D|CoT|111.61|637.73|14.040|701.50|853.91|4032.66|
|NO|Refine|96.350|750.91|14.150|711.28|828.42|4048.06|
|5|Decomp|94.350|738.32|12.920|643.25|746.36|3628.41|
||Ours|**89.610**|**820.85**|**11.080**|**555.29**|**667.76**|**3161.4**|
||Avg.|144.99|1053.98|23.080|1261.02|1436.94|8714.13|
|ES|IO|166.38|870.54|26.850|1425.48|1634.52|9896.3|
|D|CoT|157.67|937.96|23.910|1341.56|1527.66|9202.0|
|NO|Refine|137.22|1118.63|23.500|1293.09|1504.8|9068.51|
|8|Decomp|137.40|1122.79|21.670|1195.11|1327.99|8088.35|
||Ours|**126.27**|**1220.0**|**19.450**|**1049.85**|**1189.73**|**7315.47**|
||Avg.|218.82|1705.26|32.940|1695.44|2149.65|22142.9|
|ES|IO|257.33|1462.01|37.420|1914.84|2424.01|24954.7|
|OD|CoT|239.36|1553.15|34.380|1758.64|2305.24|23697.5|
|N|Refine|204.69|1798.81|34.020|1775.3|2219.27|22721.6|
|12|Decomp|205.31|1790.05|30.880|1589.09|1992.09|20553.1|
||Ours|**187.44**|**1922.26**|**27.970**|**1439.32**|**1807.66**|**18787.4**|
||Avg.|254.60|2412.26|37.230|2536.35|2704.09|38224.9|
|ES|IO|294.53|2010.03|42.810|2855.74|3070.15|42092.4|
|OD|CoT|281.95|2208.41|38.840|2743.79|2817.55|40660.3|
|N|Refine|242.95|2537.45|38.710|2625.05|2807.14|40123.6|
|15|i<br>Decomp|235.55|2606.89|34.770|2354.43|2584.13|36515.9|
||Ours|**218.01**|**2698.54**|**31.040**|**2102.76**|**2241.5**|**31732.2**|
||Avg.|323.14|2799.89|47.160|3122.83|3317.71|58569.7|
|ES|IO|377.67|2433.27|53.060|3490.25|3798.23|66151.8|
|OD|CoT|350.43|2523.88|50.330|3342.51|3504.49|62343.8|
|N|Refine|311.98|2867.08|48.550|3202.12|3356.6|61383.3|
|20|i<br>Decomp|298.35|2988.4|43.690|2924.58|3120.93|54426.8|
||Ours|**277.27**|**3186.8**|**40.180**|**2654.7**|**2808.3**|**48542.6**|
||Avg.|411.80|3732.26|14.640|3787.11|3991.53|103789.0|
|ES|IO|467.70|3208.8|16.740|4246.8|4470.97|117662.0|
|OD|CoT|449.08|3310.65|15.670|4023.17|4152.43|111329.0|
|N|Refine|387.31|3854.93|15.150|3943.46|4101.81|105411.0|
|25|Decomp|394.03|3988.58|13.560|3590.42|3832.48|97377.8|
||Ours|**360.87**|**4298.35**|**12.060**|**3131.7**|**3399.95**|**87164.7**|
||Avg.|512.38|4653.31|83.860|4995.58|5725.6|144036.0|
|ES|IO|595.35|3957.27|92.660|5605.85|6501.08|162140.0|
|OD|CoT|568.30|4162.98|88.780|5308.59|6051.78|147656.0|
|N|Refine|481.16|4796.2|88.280|5108.91|5853.66|152181.0|
|30|Decomp|476.20|5028.73|79.800|4762.89|5449.52|134230.0|
||Ours|**440.87**|**5321.36**|**69.790**|**4191.68**|**4771.98**|**123974.0**|



18 

Table 9: Comparison of various combinatorial problems based on their average cost per problem size, using `gpt-4` . The Knapsack problem aims to maximize returns, while other problems focus on minimizing costs. 

|**Size**|**Method**|**Assignment **|**Knapsack **|**Bin Packing**|**TSP**|**VRP**|**JSP**|
|---|---|---|---|---|---|---|---|
||Avg.|198.69|370.00|7.4800|372.00|442.95|2131.42|
|ES|IO|267.83|267.03|9.5800|459.92|555.57|2701.22|
|OD|CoT|234.43|300.42|8.2000|415.99|490.05|2360.95|
|N|Refine|174.66|400.32|8.1600|394.11|474.43|2259.75|
|5|Decomp|166.67|412.43|6.4400|329.82|386.85|1896.89|
||Ours|**149.84**|**469.81**|**5.0200**|**260.18**|**307.84**|**1438.3**|
||Avg.|278.35|571.94|13.030|710.49|821.54|4878.37|
|ES|IO|365.34|415.19|16.160|890.27|1029.37|6024.32|
|D|CoT|324.71|456.91|14.050|775.93|901.69|5359.79|
|NO|Refine|249.70|623.87|14.140|761.91|872.33|5163.49|
|8|Decomp|240.23|628.28|11.600|630.08|734.92|4335.16|
||Ours|**211.78**|**735.45**|**9.1800**|**494.25**|**569.41**|**3509.08**|
|S|Avg.|405.56|944.25|18.730|962.85|1238.87|12501.5|
|E|IO|534.81|680.40|23.640|1215.49|1537.63|15581.6|
|OD|CoT|475.38|791.10|20.760|1024.87|1337.63|13557.7|
|N|Refine|359.52|1031.5|19.520|1034.36|1325.99|13395.1|
|12|Decomp|351.35|1044.55|16.640|864.00|1120.36|11173.7|
||Ours|**306.72**|**1173.71**|**13.110**|**675.53**|**872.74**|**8799.38**|
||Avg.|478.16|1349.74|21.780|1469.81|1555.83|21885.7|
|ES|IO|634.70|996.41|27.150|1822.75|1958.65|27565.6|
|OD|CoT|561.76|1133.85|23.670|1608.72|1670.3|23247.9|
|N|Refine|415.50|1460.7|22.820|1567.79|1639.87|23778.5|
|15|Decomp|409.32|1446.91|19.420|1297.62|1412.5|19499.5|
||Ours|**369.55**|**1710.83**|**15.820**|**1052.15**|**1097.85**|**15336.9**|
|S|Avg.|587.33|1581.38|27.780|1822.89|1918.24|34243.4|
|E|IO|754.98|1189.83|34.320|2262.86|2356.68|42589.9|
|OD|CoT|669.13|1326.23|30.270|1981.0|2065.07|36955.8|
|N|Refine|536.41|1678.17|29.380|1902.42|1998.58|36585.5|
|20|Decomp|525.00|1723.18|24.700|1614.36|1744.24|30926.3|
||Ours|**451.14**|**1989.48**|**20.220**|**1353.84**|**1426.64**|**24159.4**|
||Avg.|743.93|2148.32|8.6300|2249.6|2381.92|61530.6|
|ES|IO|959.89|1622.78|10.430|2690.03|2872.54|75770.1|
|OD|CoT|843.97|1827.16|9.3000|2430.33|2563.55|67624.2|
|N|Refine|678.44|2238.86|9.3300|2445.45|2510.81|64490.3|
|25|i<br>Decomp|659.79|2341.61|7.8200|2002.71|2177.05|55070.7|
||Ours|**577.56**|**2711.18**|**6.2700**|**1679.49**|**1785.68**|**44697.5**|
||Avg.|912.48|2707.35|50.790|3070.36|3388.03|87633.7|
|ES|IO|1166.32|2079.35|62.520|3735.78|4104.37|104798.0|
|OD|CoT|1049.36|2254.12|55.550|3296.34|3602.09|95887.8|
|N|Refine|844.18|2932.01|52.290|3278.37|3546.61|93372.0|
|30|Decomp|788.12|2920.33|46.390|2808.58|3146.44|80674.5|
||Ours|**714.42**|**3350.95**|**37.180**|**2232.74**|**2540.65**|**63435.8**|



19 

Table 10: Comparison of various combinatorial problems based on their average cost per problem size, using `gemini-1.5` . The Knapsack problem aims to maximize returns, while other problems focus on minimizing costs. 

|**Size**|**Method**|**Assignment **|**Knapsack **|**Bin Packing**|**TSP**|**VRP**|**JSP**|
|---|---|---|---|---|---|---|---|
||Avg.|185.01|395.98|7.8900|392.96|475.25|2247.28|
|ES|IO|249.50|293.42|9.7400|488.09|581.55|2781.78|
|OD|CoT|212.33|325.58|8.6400|432.11|530.63|2460.15|
|N|Refine|161.90|424.53|8.4800|414.98|500.49|2410.6|
|5|Decomp|161.13|433.07|7.0600|346.36|432.60|2007.1|
||Ours|**140.19**|**503.30**|**5.5400**|**283.29**|**330.98**|**1576.76**|
||Avg.|262.29|596.51|13.650|739.72|853.62|5263.2|
|ES|IO|348.38|450.87|17.040|917.04|1055.48|6532.72|
|D|CoT|296.24|489.46|14.860|803.14|938.79|5783.3|
|NO|Refine|238.56|637.94|14.520|781.85|903.12|5646.28|
|8|Decomp|230.29|653.73|12.050|672.67|769.21|4636.82|
||Ours|**197.98**|**750.57**|**9.7700**|**523.89**|**601.50**|**3716.89**|
|S|Avg.|382.15|1005.24|19.690|1012.68|1291.47|13134.0|
|E|IO|490.19|729.67|24.330|1249.43|1583.87|15971.6|
|OD|CoT|437.93|848.80|21.730|1080.36|1396.44|14301.9|
|N|Refine|346.04|1068.12|20.700|1077.78|1360.73|14185.8|
|12|Decomp|339.04|1129.44|17.490|927.75|1194.11|11726.4|
||Ours|**297.53**|**1250.18**|**14.200**|**728.06**|**922.21**|**9484.31**|
||Avg.|444.10|1449.26|23.150|1564.27|1653.6|23061.3|
|ES|IO|585.87|1090.76|27.950|1940.9|2036.78|28629.8|
|OD|CoT|509.47|1216.37|25.330|1658.02|1801.66|25246.4|
|N|Refine|399.71|1541.78|24.940|1687.24|1715.89|23949.6|
|15|Decomp|385.44|1585.02|20.670|1416.65|1510.22|20343.8|
||Ours|**340.02**|**1812.35**|**16.830**|**1118.55**|**1203.46**|**17137.1**|
|S|Avg.|548.21|1678.75|29.180|1945.87|2009.98|35753.1|
|E|IO|701.27|1280.46|35.360|2396.6|2438.29|44349.1|
|OD|CoT|620.99|1428.82|31.960|2111.46|2166.27|38059.4|
|N|Refine|497.49|1810.0|30.120|2025.49|2142.69|37385.7|
|20|Decomp|480.97|1800.23|26.790|1740.08|1806.83|32493.8|
||Ours|**440.31**|**2074.24**|**21.690**|**1455.74**|**1495.83**|**26477.4**|
||Avg.|708.54|2233.73|9.2200|2352.5|2496.48|64955.1|
|ES|IO|911.14|1694.31|11.280|2890.44|2978.91|77142.4|
|OD|CoT|791.74|1878.46|9.9700|2504.54|2720.89|70181.8|
|N|Refine|642.79|2401.42|9.7100|2478.42|2670.85|69104.9|
|25|i<br>Decomp|634.67|2434.54|8.4200|2126.79|2266.56|60013.5|
||Ours|**562.34**|**2759.92**|**6.7300**|**1762.3**|**1845.18**|**48333.0**|
||Avg.|863.39|2855.59|52.430|3200.01|3534.72|91402.1|
|ES|IO|1108.6|2189.92|62.270|3807.69|4232.51|111716.0|
|OD|CoT|1002.04|2442.99|56.720|3411.03|3757.36|96055.7|
|N|Refine|784.26|2991.77|55.310|3447.36|3764.56|95672.6|
|30|Decomp|751.20|3134.08|47.690|2886.03|3265.4|83939.4|
||Ours|**670.85**|**3519.17**|**40.140**|**2447.95**|**2653.76**|**69626.6**|



20 

Table 11: Comparison of various combinatorial problems based on their average cost per problem size, using `llama-2-7b` . The Knapsack problem aims to maximize returns, while other problems focus on minimizing costs. 

|**Size**|**Method**|**Assignment **|**Knapsack **|**Bin Packing**|**TSP**|**VRP**|**JSP**|
|---|---|---|---|---|---|---|---|
||Avg.|89.950|802.42|15.550|775.06|926.24|4397.27|
|ES|IO|104.24|698.34|17.110|853.58|1041.09|4958.95|
|OD|CoT|98.820|734.35|16.520|821.09|979.18|4575.45|
|N|Refine|84.600|845.41|15.890|787.03|939.69|4634.51|
|5|Decomp|82.460|839.18|14.810|745.98|873.03|4156.86|
||Ours|**79.630**|**894.84**|**13.410**|**667.62**|**798.20**|**3660.59**|
||Avg.|126.29|1197.13|26.320|1418.23|1645.42|9991.67|
|ES|IO|147.10|1013.08|28.850|1566.87|1832.76|11162.0|
|D|CoT|136.66|1092.28|27.860|1498.77|1709.73|10389.7|
|NO|Refine|119.83|1252.94|27.120|1499.56|1710.88|10509.7|
|8|Decomp|118.10|1274.02|25.100|1343.11|1572.56|9305.07|
||Ours|**109.75**|**1353.31**|**22.700**|**1182.83**|**1401.16**|**8591.86**|
|S|Avg.|191.22|1966.31|37.090|1921.87|2465.52|24978.0|
|E|IO|220.40|1731.58|40.930|2146.2|2697.85|27795.8|
|OD|CoT|204.53|1810.85|39.550|1984.84|2596.84|25572.4|
|N|Refine|181.54|2045.48|38.930|1992.89|2594.67|26383.4|
|12|i<br>Decomp|178.63|2063.66|34.910|1834.9|2338.43|24007.4|
||Ours|**170.98**|**2179.96**|**31.130**|**1650.52**|**2099.78**|**21131.3**|
|S|Avg.|228.48<br>|2739.37<br>|42.610|2889.57|3017.02|43004.7|
|E|IO|256.26|2351.63|48.170|3212.82|3331.89|47876.6|
|OD|CoT|250.10|2553.18|44.260|3025.74|3113.82|45938.3|
|N|Refine|220.66|2843.52|44.470|3039.47|3077.27|43884.0|
|15|Decomp|216.12|2896.08|40.350|2695.41|2901.24|41025.1|
||Ours|**199.24**|**3052.45**|**35.790**|**2474.42**|**2660.9**|**36299.3**|
||Avg.|287.07|3209.13|52.710|3548.1|3703.92|65481.9|
|ES|IO|329.28|2836.21|58.190|3983.11|4240.29|72279.5|
|OD|CoT|307.87|2933.81|54.780|3746.41|3837.66|69172.2|
|N|Refine|277.27|3249.57|55.810|3667.07|3743.99|69032.1|
|20|Decomp<br>|268.09<br>|3413.37<br>|50.130<br>|3373.55<br>|3477.77<br>|61580.1<br>|
||Ours|**252.84**|**3612.7**|**44.640**|**2970.35**|**3219.91**|**55345.8**|
|S|Avg.|368.58|4255.19|16.310|4292.01|4503.47|116702.0|
|E|IO|425.08|3693.28|18.060|4674.8|5083.89|127229.0|
|OD|CoT|395.84|3938.03|16.780|4529.96|4718.81|121452.0|
|N|Refine|356.35|4438.0|17.280|4418.16|4667.3|123046.0|
|25|Decomp|344.61|4534.51|15.410|4140.85|4267.0|110197.0|
||Ours|**321.02**|**4672.15**|**14.030**|**3696.27**|**3780.34**|**101586.0**|
||Avg.|452.94|5279.99|93.580|5711.01|6309.75|160913.0|
|ES|IO|504.64|4594.52|103.15|6409.08|7164.38|177461.0|
|OD|CoT|502.24|4891.09|98.630|5995.11|6626.95|166083.0|
|N|Refine|431.79|5446.81|96.390|5957.74|6419.75|169324.0|
|30|Decomp|426.99|5619.47|89.550|5402.13|5940.75|153129.0|
||Ours|**399.05**|**5848.08**|**80.200**|**4791.01**|**5396.94**|**138570.0**|



21 

Table 12: Comparison of various combinatorial problems based on their average cost per problem size, using `llama-2-70b` . The Knapsack problem aims to maximize returns, while other problems focus on minimizing costs. 

|**Size**|**Method**|**Assignment **|**Knapsack **|**Bin Packing**|**TSP**|**VRP**|**JSP**|
|---|---|---|---|---|---|---|---|
||Avg.|96.760|757.12|14.650|719.93|864.61|4130.53|
|ES|IO|111.85|632.09|16.800|831.07|980.70|4706.85|
|OD|CoT|105.51|700.25|15.590|744.12|917.25|4290.67|
|N|Refine|92.620|788.01|15.130|740.45|897.79|4297.34|
|5|Decomp|89.850|815.64|13.340|689.33|807.57|3915.78|
||Ours|**83.980**|**849.63**|**12.410**|**594.70**|**719.74**|**3442.0**|
||Avg.|134.41|1140.45|24.710|1321.35|1538.71|9429.18|
|ES|IO|155.54|967.89|28.290|1477.89|1768.47|10645.8|
|D|CoT|145.07|1035.49|25.540|1399.97|1602.0|9988.41|
|NO|Refine|128.91|1186.02|26.100|1355.37|1601.33|9835.02|
|8|Decomp|126.39|1209.13|23.090|1263.55|1424.77|8794.53|
||Ours|**116.14**|**1303.73**|**20.560**|**1109.98**|**1296.99**|**7882.13**|
|S|Avg.|201.99|1834.2|35.110|1805.11|2315.91|23294.2|
|E|IO|231.77|1562.82|40.340|2081.41|2610.96|26535.8|
|OD|CoT|220.85|1690.42|36.560|1922.4|2462.96|24542.6|
|N|Refine|190.52|1865.06|36.340|1831.0|2363.75|23820.7|
|12|Decomp|192.52|1937.35|32.570|1666.65|2169.12|21807.0|
||Ours|**174.27**|**2115.36**|**29.750**|**1524.11**|**1972.79**|**19764.7**|
|S|Avg.|239.40|2575.28|40.140<br>|2728.94<br>|2902.12|40452.0<br>|
|E|IO|271.97|2237.81|45.310|3091.61|3270.84|46491.8|
|OD|CoT|255.93|2296.4|41.940|2852.78|3034.48|42731.8|
|N|Refine|234.52|2625.13|41.180|2850.11|2987.35|42280.3|
|15|Decomp|226.70|2761.56|37.990|2533.08|2736.93|37362.8|
||Ours|**207.87**|**2955.51**|**34.280**|**2317.12**|**2480.98**|**33393.3**|
||Avg.|301.13|2972.25|50.240|3334.42|3499.69|61957.2|
|ES|IO|341.58|2565.48|56.260|3758.49|4025.37|69824.9|
|OD|CoT|330.69|2705.18|51.940|3462.22|3620.96|63469.1|
|N|Refine|282.33|3031.65|52.210|3438.04|3567.26|64022.3|
|20|Decomp<br>|287.94<br>|3116.33<br>|47.640<br>|3167.42<br>|3297.34<br>|58800.7<br>|
||Ours|**263.10**|**3442.61**|**43.130**|**2845.92**|**2987.54**|**53669.1**|
|S|Avg.|389.69|4024.08|15.510|4029.51|4184.99|110414.0|
|E|IO|443.99|3518.82|17.390|4600.6|4735.73|126686.0|
|OD|CoT|418.18|3677.69|15.880|4148.72|4358.13|115617.0|
|N|Refine|373.97|4197.63|16.380|4136.03|4306.45|111541.0|
|25|Decomp|369.43|4170.69|14.700|3822.3|3975.41|104862.0|
||Ours|**342.89**|**4555.58**|**13.180**|**3439.89**|**3549.23**|**93361.4**|
||Avg.|490.92|5026.68|88.930|5310.47|5986.86|154018.0|
|ES|IO|562.14|4332.75|99.580|5902.09|6848.47|171767.0|
|OD|CoT|535.73|4629.8|92.530|5670.09|6113.72|158276.0|
|N|Refine|472.51|5217.75|92.730|5409.26|6165.51|160831.0|
|30|Decomp|455.30|5339.41|85.010|4948.58|5562.01|146910.0|
||Ours|**428.95**|**5613.7**|**74.780**|**4622.34**|**5244.57**|**132308.0**|



22 

