# LARGE LANGUAGE MODELS FOR COMBINATORIAL OPTIMIZATION OF DESIGN STRUCTURE MATRIX 

**Shuo Jiang**<sup>_∗_</sup> 

Department of Systems Engineering City University of Hong Kong 83 Tat Chee Ave, Kowloon Tong, Hong Kong `shuo.jiang@cityu.edu.hk` 

**Min Xie** 

Department of Systems Engineering City University of Hong Kong 83 Tat Chee Ave, Kowloon Tong, Hong Kong `xiemin@cityu.edu.hk` 

### **Jianxi Luo** 

Department of Systems Engineering City University of Hong Kong 

83 Tat Chee Ave, Kowloon Tong, Hong Kong `jianxi.luo@cityu.edu.hk` 

A Preprint, Version: Nov 19, 2024 

## **ABSTRACT** 

Combinatorial optimization (CO) is essential for improving efficiency and performance in engineering applications. As complexity increases with larger problem sizes and more intricate dependencies, identifying the optimal solution become challenging. When it comes to real-world engineering problems, algorithms based on pure mathematical reasoning are limited and incapable to capture the contextual nuances necessary for optimization. This study explores the potential of Large Language Models (LLMs) in solving engineering CO problems by leveraging their reasoning power and contextual knowledge. We propose a novel LLM-based framework that integrates network topology and domain knowledge to optimize the sequencing of Design Structure Matrix (DSM)—a common CO problem. Our experiments on various DSM cases demonstrate that the proposed method achieves faster convergence and higher solution quality than benchmark methods. Moreover, results show that incorporating contextual domain knowledge significantly improves performance despite the choice of LLMs. These findings highlight the potential of LLMs to address complex CO problems by combining semantic and mathematical reasoning. This approach paves the way for a new paradigm in real-world engineering combinatorial optimization. 

**_Keywords_** Large Language Models _·_ Combinatorial Optimization _·_ Artificial Intelligence _·_ Knowledge-based Reasoning _·_ Design Structure Matrix _·_ Systems Engineering 

## **1 Introduction** 

Combinatorial optimization (CO) problems are ubiquitous across fields, where finding an optimal solution from a finite set often drives improvements in efficiency, cost, and performance [1]. For instance, applications such as DNA barcoding and DNA assembly in synthetic biology [2], as well as job scheduling in manufacturing [3], rely heavily on effective CO solutions. However, due to their NP-hard nature, these problems present substantial challenges, especially as complexity increases with larger problem sizes and more intricate dependencies. Traditionally, CO problems in engineering are usually approached through the following process: the problem is first modelled mathematically, then solved using specific algorithms or heuristics, and finally interpreted within the context of practical engineering [4]. 

> _∗_ Comments are welcome: `shuojiangcn@gmail.com` 

LARGE LANGUAGE MODELS FOR COMBINATORIAL OPTIMIZATION OF DSM 

This separation of problem-solving and interpretation stages is limited and incapable to capture the contextual nuances necessary for optimization of real-world problems. 

Recent advancements in Large Language Models (LLMs) have demonstrated their powerful capabilities in natural language generation, semantic understanding, instruction following, and complex reasoning [5, 6]. Furthermore, pioneering studies have shown that LLMs can be used for continuous and concrete optimization [7, 8, 9]. For instance, researchers from DeepMind utilized LLMs as optimizers and evaluated their effectiveness on classic CO problems [8], such as Traveling Salesman Problems (TSP). Additionally, prior studies also highlight that LLMs possess extensive domain knowledge pretrained across a wide range of engineering-related data, which enhances their applicability in engineering fields [10, 11, 12, 13]. Therefore, the ability of LLMs to combine mathematical and semantic reasoning, along with their possession of extensive knowledge, motivated us to explore their potential for solving engineering CO problems while integrating contextual domain knowledge relevant to their network typology. Our hypotheses are: (1) LLMs can be effectively applied to solve CO problems in engineering, and (2) incorporating contextual domain knowledge can further enhance LLM performance by supporting mathematical reasoning with semantic insights. This paradigm, which leverages both semantic and mathematical reasoning, introduces a novel approach to combinatorial optimization that traditional pure mathematical methods cannot achieve for empirical problems. On this basis, we propose a novel LLM-based framework that integrates both network topology and domain context into the optimization process. 

To evaluate our proposed method, we focus on the Design Structure Matrix (DSM) sequencing task, as an example of CO problems. DSM is a modelling tool in engineering design, which represents dependency relationships among tasks or components within a system [14]. Reordering the node sequence of DSMs can significantly reduce feedback loops and improve modularization [15, 16]. The DSM sequencing is also an NP-hard problem, and traditional methods typically approach it using heuristics-based algorithms [17, 18]. Figure 1 illustrates a design activity DSM before and after sequencing [19]. In this paper, we conduct extensive experiments on various DSM cases to demonstrate that our LLM-based method achieves better convergence speed and solution quality compared to benchmark methods. Notably, results show that incorporating contextual domain knowledge significantly enhances the performance despite the choice of backbone LLMs. 



Figure 1: Illustration of a Design Activity DSM: (A) Pre-Sequencing; (B) Post-Sequencing 

## **2 Methodology** 

In this section, we introduce our proposed LLM-based framework for solving CO problems. The framework is designed to harness the generative and reasoning powers of LLMs in combination with domain knowledge and objective evaluation. The framework begins with the initialization of a solution randomly sampled in the total solution space. Each solution is evaluated based on predefined criteria by an evaluator, which quantifies the quality of a solution. Using this evaluation, the framework iteratively updates the solution base through few-shot learning and suggesting new candidates, guided by crafted prompts that include both network information in mathematical form and domain knowledge in natural language description. The newly generated solutions are appended into the solution base, together with their evaluation results. When the iteration time is reached, the solution base returns the best one as the final output. In following, we focus on DSM sequencing as a common CO problem to illustrate the pipeline. The framework is depicted in Figure 2. 

2 

LARGE LANGUAGE MODELS FOR COMBINATORIAL OPTIMIZATION OF DSM 



Figure 2: Overview of the Proposed Framework 

### **Initialization and solution sampling** 

The Solution Base serves as an essential module to (1) enable storage of explored solutions and their evaluation results, (2) provide historical solutions to the backend LLM for few-shot learning, and (3) return the top-performing solution when iteration ends. 

The initialization involves generating an initial solution that is randomly sampled from the entire solution space. In the DSM sequencing task, a solution represents a complete and non-repetitive sequence of nodes (see Figure 2). This initial solution is then evaluated and added to the Solution Base for future use. In subsequent iterations, we design a sampling rule that selects _Kp_ top-performance solutions and randomly samples _Kq_ solutions from the remaining _Kn − Kp_ solutions to form a solution set, where _Kn_ is the total number of solutions in the Solution Base. _Kp_ and _Kq_ are adjustable parameters. The obtained solution set is further refined and crafted into prompts. 

### **LLM-driven optimization using network information and domain knowledge** 

In each iteration of the optimization process, we prompt backend LLM with the following information: **(i) Typology Information** : These two elements complete the mathematical description of a DSM. It is noteworthy that there are multiple equivalent representations for describing a network mathematically, such as an edge list, a dependency relationship list according to node sequence, or an adjacency matrix. In this research, we choose the edge list as the representation of the network’s topology and shuffle all edges to avoid any possible bias. **(ii) Contextual Domain Knowledge** : This includes the name of each node and an overall description of the network, which conveys the domain knowledge underlying the DSM’s mathematical structure to the LLM. For instance, in an activity DSM, each node represents the name of an activity in the entire design process. **(iii) Meta-instructions** : We adopt some frequently used prompt engineering strategies [20], including role-playing, task specification, and output format specification. These strategies allow the LLM to follow the guidance to perform reasoning and generate solutions in a specific format. **(iv) Selected historical solutions** : As described in the last section, we obtain a set of up to _Kp_ + _Kq_ solutions through sampling from the Solution Base for the LLM to use in few-shot learning. 

Once receiving inputs described above, the backend LLM combines the network topology information with domain knowledge to infer and suggest new solutions. The generated solution must pass the checker, which verifies that all nodes are present exactly once in the sequence. Once validated, the solution is then evaluated and appended to the Solution Base. The detailed input prompts are included in Appendix 1. 

### **Evaluation of DSM sequencing solutions** 

The evaluator is used to quantify each newly generated solution. For the DSM sequencing task, the goal is to reorder the rows and columns of the DSM to minimize feedback loops. To achieve this objective, the evaluator calculates the number of backward dependencies in the corresponding sequence. 

3 

LARGE LANGUAGE MODELS FOR COMBINATORIAL OPTIMIZATION OF DSM 

We formally describe this problem as follows: Given a sequence _s_ , we can use the edge list of the network to obtain an _n × n_ asymmetric adjacency matrix _A_ , representing a directed network of _n_ nodes, where _aij_ is a typical binary entry. Specifically, _aij_ = 1 represents that node _i_ depends on node _j_ . The task is to reorder the _n_ correlated rows and columns to minimize the number of entries above the main diagonal in the corresponding adjacency matrix. On this basis, the objective function can be formally expressed as: min _s_ � _ni_ =1 � _nj_ = _i_ +1<sup>_aij_, where</sup><sup>_i < j_.</sup> 

For each sequence generated by the LLM (including the initial randomly created one), we calculate its evaluation score using the formula above. In this task, a lower score indicates a higher quality solution. 

## **3 Experiments** 

### **3.1 Data** 

We collected four DSM cases for our experiments, which can be categorized into two types [21]: (1) Activity-based DSMs, which represent the input-output relationships between different tasks or activities within a project; and (2) Parameter-based DSMs, which illustrate the relationships among design parameters of a product. 

The DSM of the Unmanned Combat Aerial Vehicle (UCAV) includes 12 conceptual design activities conducted at Boeing [22]. The DSM of the Microfilm Cartridge was derived from Kodak’s Cheetah project including 13 major tasks [23]. These two activity-based DSMs were constructed based on interviews with relevant engineers, followed by review, verification, and calibration to ensure accuracy. For the parameter-based DSMs, the Heat Exchanger [19] and the Automobile Brake System [24], researchers first identified the key components from the product and then interviewed the corresponding designers to define design parameters and establish precedence relationships. The Heat Exchanger DSM contains 17 components related to core thermal exchange elements, while the Brake System DSM includes 14 main parameters covering braking mechanisms and their dependencies. 

From the referential documents, we extracted: (1) the name of each node, (2) the edge list obtained from the adjacency matrix, and (3) the overall description of each network. All data were kept consistent with the original references. The specific data formats are shown in Appendix 1. The characteristics of four DSMs are summarized in Table 1. In general, the node count ( **N** ) of DSMs ranges from 12 to 17, and the edge count ( **E** ) varies between 32 and 47. The network diameter, representing the longest shortest path between any two nodes, spans from 2 to 7. We also present measures such as network density and clustering coefficient to highlight the complexity. For instance, the UCAV DSM has a high network density of 0.712 and a clustering coefficient of 0.773, suggesting strong interconnections, while measures of the Heat Exchanger DSM indicate a sparser network with more distinct relationships. 

Table 1: Characteristics of Four DSMs 

||**N**|**E**|**Network**<br>**Diameter**|**Network**<br>**Density**|**Average**<br>**Degree**|**Clustering**<br>**Coefficient**|**Average**<br>**Path Length**|
|---|---|---|---|---|---|---|---|
|**Activity-Based DSMs**<br>Unmanned Aerial Vehicle [22]<br>Microfilm Cartridge [23]|12<br>13|47<br>41|2<br>3|0.712<br>0.526|7.833<br>6.308|0.773<br>0.682|1.288<br>1.577|
|**Parameter-Based DSMs**<br>Heat Exchanger [19]|17|41|7|0.302|4.824|0.457|2.397|
|<br>Automobile Brake System [24]|14|32|4|0.352|4.571|0.414|1.824|



### **3.2 Experiment Setup** 

### **Experimental setting** 

In all our experiments, we ran each method 10 times with different random seeds to ensure robustness. For solution sampling, we set _Kp_ = 5 and _Kq_ = 5. For the index of each node, we use a string composed of 5 randomly generated characters (a mix of numbers and letters) to represent the node uniquely. The maximum number of iterations was set to 20. We selected _Claude-3.5-Sonnet-20241022_ as the backbone LLM and kept all other settings of the LLM as their default values [25]. 

4 

LARGE LANGUAGE MODELS FOR COMBINATORIAL OPTIMIZATION OF DSM 



Figure 3: Comparison of Convergence Speed 

### **Comparative methods for benchmarking** 

We consider two types of approaches for benchmarking. 

The first type is stochastic methods, which rely on probabilistic rules to explore the solution space. We chose the classic Genetic Algorithm (GA) for comparison, as it has been successfully applied to various optimization problems [26]. We implemented GA using the DEAP library [27]. We considered three different settings for GA: exploration-focused, exploitation-focused, and balanced setting. Specific parameter settings of three variants are detailed in Appendix 2. 

The second type is deterministic methods, which rank nodes based on a specific measure and then use this ranking for reordering. Since the calculation of each measure is deterministic, the resulting solution is consistent. We considered five deterministic methods for comparison, each reordering nodes based on different criterion: **(i) Out-In Degree** [28]: Reordering based on the difference between out-degree and in-degree of each node. **(ii) Eigenvector** [29]: Calculating the values of components in the Perron vector of the adjacency matrix and sorting nodes accordingly. **(iii) Walk-based (Exponential)** [30]: Considering in-depth connectivity patterns by involving the power of the adjacency matrix **A** . It is calculated by: _F_ ( **A** ) = exp( **A** ). **(iv) Walk-based (Resolvent)** [31]: Calculated by: _F_ ( **A** ) = ( **I** _− δ_ **A** )<sup>_−_1</sup> , where _δ_ represents the probability that a message will successfully traverse an edge. We set _δ_ = 0 _._ 025 in experiments following the original reference. **(v) Visibility** [32]: Involving the visibility matrix, showing the dependencies between all system elements for all possible path lengths up to the matrix size. It is calculated by: _F_ ( **A** ) =<sup>�</sup><sup>_n_</sup> _k_ =0<sup>**A**</sup><sup>_k_, where n represents</sup> the number of nodes. The resulting visibility matrix is then binarized. For methods **(iii)** , **(iv)** , and **(v)** , once the _F_ ( **A** ) is obtained, nodes are reordered by the sum of rows of _F_ ( **A** ). If nodes share the same value, they are then reordered based on the sum of columns of _F_ ( **A** ). 

To further investigate the effectiveness of incorporating domain knowledge, we also consider a variant of our proposed method for comparison. In this variant, all settings are kept the same as in the main method, except that the contextual knowledge about nodes and the entire network is removed. Therein, only the topological information of the network is engineered into the input prompt, guiding the LLM to search for an optimal solution solely through mathematical reasoning. 

## **4 Results and Discussion** 

We first compared the convergence speed among our LLM-based methods and the three variants of GA, as shown in Figure 3. In GA, due to different parameter settings (e.g., population size, crossover, and mutation rates), each iteration explores multiple unique solutions. In contrast, our methods suggest only one unique solution per iteration. Therefore, 

5 

LARGE LANGUAGE MODELS FOR COMBINATORIAL OPTIMIZATION OF DSM 

we standardized the iteration time (generation) for GA as the number of unique solutions explored and used this as the measure for convergence speed. Although the maximum number of generations for each GA run was set to 2,000 (refer to Appendix 2), we truncated the comparison to the first 10,000 unique solutions explored for clearer visualization. 

Compared to all three GA settings, our methods show significantly higher convergence speed, reaching lower objective values faster across all four cases. Overall, our LLM-based methods demonstrate a consistent advantage over GA, finding high-quality solutions multiple orders of magnitude faster in all cases. In each of the four cases, our methods can always identify an initial solution of good quality within the first attempt and continue optimizing the solution through subsequent iterations, approximating the optimal solution. This demonstrates that LLMs can leverage in-context learning to adapt and improve solutions efficiently. 

Moreover, in Figures 3 (A), (C), and (D), we observe that incorporating domain knowledge enhances the LLM’s performance in both convergence speed and solution quality, as indicated by the red line consistently lying below the grey line. This suggests that LLMs combining semantic reasoning with mathematical reasoning can solve CO problems more effectively and efficiently. It is noteworthy that in the cartridge development case (Figure 3 (B)), both LLM-based methods (with and without knowledge) found the best solution within the first step. Consequently, the two lines overlap, indicating identical performance in this case. 

Table 2: Comparison of Solution Quality 

|**Methods**|**Activity-Ba**|**sed DSMs**|**Parameter-**|**Based DSMs**|
|---|---|---|---|---|
||**Unmanned**<br>**Aerial Vehicle**|**Microfilm**<br>**Cartridge**|**Heat**<br>**Exchanger**|**Automobile**<br>**Brake System**|
|**Stochastic Methods**<sup>1</sup>|||||
|GA (Exploration-focused setting)|**6.0±0.0**|8.1±0.3|5.7±1.0|3.8±0.7|
|GA (Exploitation-focused setting)|7.4±1.5|9.9±1.4|7.6±1.4|6.6±1.7|
|GA (Balanced setting)|**6.0±0.0**|8.4±0.5|6.2±1.2|4.2±1.2|
|**Deterministic Methods**<sup>2</sup>|||||
|Out-In Degree [28]|10.0±0.0|12.3±0.5|10.3±0.6|5.7±0.9|
|Eigenvector [29]|15.0±0.0|13.8±0.7|13.1±1.7|11.1±1.4|
|Walk-based (Exponential) [30]|15.0±0.0|12.0±0.0|8.0±0.0|11.0±0.0|
|Walk-based (Resolvent) [31]|9.0±0.0|12.0±0.0|8.0±0.0|11.0±0.0|
|Visibility [32]|25.6±2.2|8.8±0.7|6.0±1.3|**3.0±0.0**|
|**LLM-driven Methods (Ours)**|||||
|Single-trial with knowledge|6.6±0.7|**8.0±0.0**|4.8±0.6|4.4±0.9|
|Single-trial without knowledge|11.9±3.4|8.1±0.3|5.8±1.1|5.9±1.4|
|5-trial with knowledge|6.1±0.3|**8.0±0.0**|4.0±0.4|**3.0±0.0**|
|5-trial without knowledge|7.5±0.9|**8.0±0.0**|4.9±0.5|4.0±1.0|
|20-trial with knowledge|**6.0±0.0**|**8.0±0.0**|**3.6±0.5**|**3.0±0.0**|
|20-trial without knowledge|6.4±0.7|**8.0±0.0**|4.1±0.3|3.4±0.7|



We also compared the solution quality among different methods, as presented in Table 2. We experimented with our methods over single-trial, 5-trial, and 20-trial runs to evaluate their effectiveness. Compared to stochastic methods and deterministic methods, our methods significantly outperformed the corresponding benchmarks. 

On the one hand, since all deterministic methods can be regarded as single-trial approaches (static algorithms), we first compared our single-trial results with those methods. As shown in Table 2, except for the Visibility-based method 

> 1Consistent with Figure 3, all three GA settings show optimization performance with number of unique sequences explored = 10,000. 

> 2All deterministic methods can be regarded as single-trial approaches, as they produce consistent outcomes for identical inputs across repeated executions. However, certain nodes might share the same measures. For these nodes, a random order is applied, and the final statistical evaluation results are obtained from 10 runs. 

6 

LARGE LANGUAGE MODELS FOR COMBINATORIAL OPTIMIZATION OF DSM 

finding the optimal solution directly in one case (brake system design DSM), our methods outperformed all other deterministic methods across all cases. Even in the brake system case, our 5-trial method matched the effectiveness of the Visibility-based method. 

On the other hand, when comparing with stochastic algorithms, our 20-trial method consistently found better solutions than benchmarks and achieved the optimal solution in 3 out of 4 cases. It is important to note that our experiments only tested up to 20 iterations. If we were to continue with longer iterations, the heat exchanger design case might also reach the optimal solution. Moreover, even with the 5-trial runs, our methods outperformed all three variants of GA in 3 out of 4 cases and were close in the UCAV case (6.1±0.3 vs. 6.0±0.0). This demonstrates that our LLM-based approach, leveraging contextual domain knowledge and iterative in-context learning, can effectively solve CO problems, suggesting high-quality solutions in a few attempts. 

Table 3: Ablation on the Backbone LLM 

|**# of Trial**|**Backbone LLM**|**Knowledge**|**Activity-Ba**|**sed DSMs**|**Parameter-**|**Based DSMs**|
|---|---|---|---|---|---|---|
||||**Unmanned**<br>**Aerial Vehicle**|**Microfilm**<br>**Cartridge**|**Heat**<br>**Exchanger**|**Automobile**<br>**Brake System**|
||_Mixtral-7x8B_|with|12.5±2.2|19.5±5.0|16.1±2.2|12.1±3.1|
|||without|15.8±4.6|17.7±3.3|16.8±1.9|16.0±2.3|
||_Ll370B_|with|7.6±0.8|8.3±0.5|7.9±2.0|6.1±1.1|
|**1**|_ama-_|without|12.5±3.8|10.2±1.2|10.1±1.8|7.0±2.2|
||_GPT4Tb_|with|9.6±3.2|10.0±1.6|9.2±2.1|5.0±1.2|
||_--uro_|without|13.9±4.3|11.0±1.5|12.9±3.1|7.5±2.7|
||_Claude-35-Sonnet_|with|**6.6±0.7**|**8.0±0.0**|**4.8±0.6**|**4.4±0.9**|
||_._|without|11.9±3.4|8.1±0.3|5.8±1.1|5.9±1.4|
||_Mixtral-7x8B_|with|10.6±1.4|13.1±2.7|13.0±2.1|9.7±2.5|
|||without|12.3±2.6|15.0±2.2|15.4±2.3|13.8±1.7|
||_Ll370B_|with|6.7±0.5|8.1±0.3|5.5±0.9|5.4±1.1|
|**5**|_ama-_|without|8.4±1.7|9.3±0.5|8.7±1.2|5.4±1.4|
||_GPT4Tb_|with|6.8±0.6|8.4±0.5|6.6±1.3|4.6±0.9|
||_--uro_|without|8.9±0.8|9.6±0.8|10.1±2.7|5.7±1.8|
||_Claude-35-Sonnet_|with|**6.1±0.3**|**8.0±0.0**|**4.0±0.4**|**3.0±0.0**|
||_._|without|7.5±0.9|**8.0±0.0**|4.9±0.5|4.0±1.0|
||_Mixtral-7x8B_|with|10.1±1.2|11.2±2.3|10.7±1.2|8.8±2.0|
|||without|11.3±1.7|13.0±1.2|14.0±1.3|13.1±1.7|
||_Ll370B_|with|6.7±0.5|**8.0±0.0**|4.7±0.5|5.2±1.2|
|**2**|_ama-_|without|7.4±0.8|8.8±0.6|7.7±1.3|4.6±0.9|
|**0**|_GPT4Tb_|with|6.1±0.3|8.2±0.4|5.1±0.8|4.1±0.7|
||_--uro_|without|7.3±0.6|9.1±0.3|7.7±1.8|5.0±1.5|
||_Claude-35-Sonnet_|with|**6.0±0.0**|**8.0±0.0**|**3.6±0.5**|**3.0±0.0**|
||_._|without|6.4±0.7|**8.0±0.0**|4.1±0.3|3.4±0.7|



To evaluate the effect of different backbone LLMs on our proposed method, we conducted an ablation study. In addition to _Claude-3.5-Sonnet_ [25], we repeated the experiments in Table 2 using three different backbones: two open-source LLMs ( _Mixtral-7x8B_ [33] and _Llama3-70B_ [34]) and one closed-source LLM ( _GPT-4-Turbo_ [35]), accessed via its API. We report the results for single-trial, 5-trial, and 20-trial runs, and also examine the impact of removing contextual domain knowledge from the prompts. As indicated by Table 3, _Claude-3.5-Sonnet_ , our choice, statistically outperforms the other LLMs across all four cases. _Llama3-70B_ follows as the second top performer in most cases, demonstrating that open-source LLMs can be effective alternatives. This suggests that our framework is compatible with different LLMs. We recommend users or researchers may start with _Claude-3.5-Sonnet_ for optimal performance, but may consider open-source models like _Llama_ for budget or customizability. Furthermore, in all cases, the results across all LLMs show that incorporating contextual domain knowledge consistently improves solution quality compared to the ones 

7 

LARGE LANGUAGE MODELS FOR COMBINATORIAL OPTIMIZATION OF DSM 

without knowledge. This finding aligns with our previous observation in Figure 1, highlighting the robustness of our methods and the significant role of domain knowledge in enhancing LLMs’ reasoning performance in such CO tasks with real-world contexts. 

## **5 Concluding Remarks** 

Experimental results demonstrate that our proposed method, particularly when incorporating contextual domain knowledge, offer significant advantages in both convergence speed and solution quality compared to benchmarking stochastic and deterministic approaches. Across all experiments and backbone LLMs, the inclusion of domain knowledge consistently improved performance. While _Claude-3.5-Sonnet_ is the most effective backbone LLM, opensource models such as _Llama3-70B_ also shows strong performance. Overall, these findings illustrate the capability of our proposed method to effectively address DSM sequencing tasks, leveraging both semantic and mathematical reasoning of LLMs for real-world combinatorial optimization problems. 

Despite the promising results, there are some limitations. First, the scope of the current experiments could be expanded by collecting more diverse DSM cases, including larger and more complex networks, to achieve more robust statistical results. Second, while we focused on DSM sequencing tasks, the effectiveness of our proposed method could be explored across a wider range of real-world combinatorial optimization tasks to assess its generalizability. Third, we plan to delve into the intermediate changes in LLM outputs during optimization in future work, which may provide greater interpretability and insights into the LLMs’ reasoning processes. 

In conclusion, our study highlights the potential of LLMs for combinatorial optimization of design structure matrix, showing that including domain knowledge can significantly enhance the performance of our methods. Future research can build on these findings to further refine LLM-driven methods and extend applications to more complex and diverse combinatorial optimization problems. 

## **References** 

- [1] Bernhard H. Korte and Jens Vygen. _Combinatorial optimization_ . Springer, 2011. 

- [2] Gita Naseri and Mattheos A. G. Koffas. Application of combinatorial optimization strategies in synthetic biology. _Nature Communications_ , 11:2446, 2020. 

- [3] Elias Xidias and Philip Azariadis. Energy efficient motion design and task scheduling for an autonomous vehicle. In _Proceedings of the International Conference on Engineering Design (ICED)_ , pages 2853–2862, 2019. 

- [4] Michael L. Pinedo. _Scheduling_ . Springer, New York, 2012. 

- [5] Jason Wei, Yi Tay, Rishi Bommasani, Colin Raffel, Barret Zoph, Sebastian Borgeaud, Dani Yogatama, Maarten Bosma, Denny Zhou, Donald Metzler, Ed H. Chi, Tatsunori Hashimoto, Oriol Vinyals, Percy Liang, Jeff Dean, and William Fedus. Emergent abilities of large language models. _Transactions on Machine Learning Research_ , 2022. 

- [6] Yupeng Chang, Xu Wang, Jindong Wang, Yuan Wu, Linyi Yang, Kaijie Zhu, Hao Chen, Xiaoyuan Yi, Cunxiang Wang, Yidong Wang, Wei Ye, Yue Zhang, Yi Chang, Philip S. Yu, Qiang Yang, and Xing Xie. A survey on evaluation of large language models. _ACM Transactions on Intelligent Systems and Technology_ , pages 1–45, 2024. 

- [7] Bernardino Romera-Paredes, Mohammadamin Barekatain, Alexander Novikov, Matej Balog, M. Pawan Kumar, Emilien Dupont, Francisco J. R. Ruiz, Jordan S. Ellenberg, Pengming Wang, Omar Fawzi, Pushmeet Kohli, and Alhussein Fawzi. Mathematical discoveries from program search with large language models. _Nature_ , pages 468–475, 2024. 

- [8] Chengrun Yang, Xuezhi Wang, Yifeng Lu, Hanxiao Liu, Quoc V. Le, Denny Zhou, and Xinyun Chen. Large language models as optimizers. In _The Twelfth International Conference on Learning Representations (ICLR)_ , 2024. 

- [9] Shengcai Liu, Caishun Chen, Xinghua Qu, Ke Tang, and Yew-Soon Ong. Large language models as evolutionary optimizers. In _IEEE Congress on Evolutionary Computation (CEC)_ , pages 1–8, 2024. 

- [10] Qihao Zhu and Jianxi Luo. Generative transformers for design concept generation. _Journal of Computing and Information Science in Engineering_ , page 041003, 2023. 

- [11] Liane Makatura, Michael Foshey, Bohan Wang, Felix Hähnlein, Pingchuan Ma, Bolei Deng, Megan Tjandrasuwita, Andrew Spielberg, Crystal Elaine Owens, Peter Yichen Chen, Allan Zhao, Amy Zhu, Edward Gu Wil J. Norton, Joshua Jacob, Yifei Li, Adriana Schulz, and Wojciech Matusik. Large language models for design and manufacturing. _An MIT Exploration of Generative AI_ , 2024. 

8 

LARGE LANGUAGE MODELS FOR COMBINATORIAL OPTIMIZATION OF DSM 

- [12] Shuo Jiang and Jianxi Luo. Autotriz: Artificial ideation with triz and large language models. In _International Design Engineering Technical Conferences & Computers and Information in Engineering Conference (IDETC/CIE)_ . ASME, 2024. 

- [13] Aoran Mei, Guo-Niu Zhu, Huaxiang Zhang, and Zhongxue Gan. Replanvlm: Replanning robotic tasks with visual language models. _IEEE Robotics and Automation Letters_ , 2024. 

- [14] Donald V. Steward. The design structure system: A method for managing the design of complex systems. _IEEE Transactions on Engineering Management_ , pages 71–74, 1981. 

- [15] Young Mi Choi. Effective scheduling of user input during the design process. In _Proceedings of the International Conference on Engineering Design (ICED)_ , pages 116–122, 2011. 

- [16] Steven D. Eppinger and Tyson R. Browning. _Design structure matrix methods and applications_ . MIT Press, 2012. 

- [17] Steven D. Eppinger, Daniel E. Whitney, Robert P. Smith, and David A. Gebala. A model-based method for organizing tasks in product development. _Research in Engineering Design_ , pages 1–13, 1994. 

- [18] Yanjun Qian, Jun Lin, Thong Ngee Goh, and Min Xie. A novel approach to dsm-based activity sequencing problem. _IEEE Transactions on Engineering Management_ , pages 688–705, 2011. 

- [19] Rafael Amen, Ingvar Rask, and Staffan Sunnersjö. Matching design tasks to knowledge-based software tools: When intuition does not suffice. In _International Design Engineering Technical Conferences and Computers and Information in Engineering Conference (IDETC/CIE)_ , pages 1165–1174, 1999. 

- [20] Wayne Xin Zhao, Kun Zhou, Junyi Li, Tianyi Tang, Xiaolei Wang, Yupeng Hou, Yingqian Min, Beichen Zhang, Junjie Zhang, Zican Dong, Yifan Du, Chen Yang, Yushuo Chen, Zhipeng Chen, Jinhao Jiang, Ruiyang Ren, Yifan Li, Xinyu Tang, Zikang Liu, Peiyu Liu, Jian-Yun Nie, and Ji-Rong Wen. A survey of large language models. _arXiv preprint_ , 2023. arXiv:2303.18223. 

- [21] Tyson R. Browning. Applying the design structure matrix to system decomposition and integration problems: a review and new directions. _IEEE Transactions on Engineering Management_ , pages 292–306, 2001. 

- [22] Tyson R. Browning. _Modeling and analyzing cost, schedule, and performance in complex system product development_ . PhD thesis, Massachusetts Institute of Technology, 1998. 

- [23] Karl T. Ulrich and Steven D. Eppinger. _Product Design and Development_ . McGraw-Hill, 2016. 

- [24] Thomas Andrew Black, Charles H. Fine, and Emanuel M. Sachs. A method for systems design using precedence relationships: An application to automotive brake systems. _Working Paper of Sloan School of Management,Massachusetts Institute of Technology_ , 1990. 

- [25] Anthropic. Introducing computer use, a new claude 3.5 sonnet, and claude 3.5 haiku, 2024. Accessed Oct 2024, https://www.anthropic.com/news/3-5-models-and-computer-use. 

- [26] Bushra Alhijawi and Arafat Awajan. Genetic algorithms: Theory, genetic operators, solutions, and applications. _Evolutionary Intelligence_ , pages 1245–1256, 2024. 

- [27] Felix-Antoine Fortin, Francois-Michel De Rainville, Marc-Andre Gardner, Marc Parizeau, and Christian Gagne. Deap: Evolutionary algorithms made easy. _Journal of Machine Learning Research_ , pages 2171–2175, 2012. 

- [28] Jonathan J. Crofts and Desmond J. Higham. Googling the brain: Discovering hierarchical and asymmetric network structures, with applications in neuroscience. _Internet Mathematics_ , pages 233–254, 2011. 

- [29] Erik Dietzenbacher. The measurement of interindustry linkages: Key sectors in the netherlands. _Economic Modelling_ , pages 419–437, 1992. 

- [30] Ernesto Estrada and Juan A. Rodriguez-Velazquez. Subgraph centrality in complex networks. _Physical Review E-Statistical, Nonlinear, and Soft Matter Physics_ , 56(103), 2005. 

- [31] Ernesto Estrada and Desmond J. Higham. Network properties revealed through matrix functions. _SIAM Review_ , pages 696–714, 2010. 

- [32] Alan MacCormack, Carliss Baldwin, and John Rusnak. Exploring the duality between product and organizational architectures: A test of the “mirroring” hypothesis. _Research Policy_ , pages 1309–1324, 2012. 

- [33] Albert Q. Jiang, Alexandre Sablayrolles, Antoine Roux, Arthur Mensch, Blanche Savary, Chris Bamford, and Devendra Singh Chaplot. Mixtral of experts. _arXiv preprint_ , 2024. arXiv:2401.04088. 

- [34] Meta. Introducing meta llama 3: The most capable openly available llm to date, 2024. https://ai.meta.com/blog/meta-llama-3/. 

- [35] OpenAI. Gpt-4 turbo, 2024. https://platform.openai.com/docs/models/gpt-4-and-gpt-4-turbo. 

9 

LARGE LANGUAGE MODELS FOR COMBINATORIAL OPTIMIZATION OF DSM 

## **Appendix 1. Full prompts** 

### **Prompt for our proposed method (the main method):** 

You are an expert in the domain of combinational optimization. 

Please assist me to find an optimal sequential order that minimizes feedback cycles in the dependency network described below. Your task is to propose a new order that differs from previous attempts and has fewer feedback cycles than any listed. 

```
<DescriptionoftheentireNetwork>{network_description}</Descriptionoftheentire
Network>
<NodeswithDescriptions> {node_list_with_description} </NodeswithDescriptions>
<Edges> {edge_list} </Edges>
```

Below are some previous sequential orders arranged in descending order of feedback cycles (lower is better): `{selected_historical_solutions}` 

Please suggest a new order that: - Is different from all prior orders. - Has fewer feedback cycles than any previous order. - Covers all nodes exactly once. - Starts with `<order>` and ends with `</order>` . 

- You can use the descriptions of nodes and networks to support your suggestion. 

Output Format: `<order> ...... </order>` Please provide only the order and nothing else. 

### **Prompt for our proposed method (removing contextual domain knowledge):** 

You are an expert in the domain of combinational optimization. 

Please assist me to find an optimal sequential order that minimizes feedback cycles in the dependency network described below. Your task is to propose a new order that differs from previous attempts and has fewer feedback cycles than any listed. 

```
<Nodes> {node_list} </Nodes>
<Edges> {edge_list} </Edges>
```

Below are some previous sequential orders arranged in descending order of feedback cycles (lower is better): `{selected_historical_solutions}` 

Please suggest a new order that: - Is different from all prior orders. - Has fewer feedback cycles than any previous order. - Covers all nodes exactly once. - Starts with `<order>` and ends with `</order>` . 

Output Format: `<order> ...... </order>` 

Please provide only the order and nothing else. 

10 

LARGE LANGUAGE MODELS FOR COMBINATORIAL OPTIMIZATION OF DSM 

**Example of** `{network_description}` **in the UCAV design activity DSM case:** 

```
Thisnetworkrepresentsthedependencyrelationshipsamongconceptualdesign
activitiesforUCAVdevelopmentatBoeing.Eachnodecorrespondstoaspecifictask
oranalysis,anddirectededgesindicatetheprerequisiterelationshipsbetweenthese
tasks.Nodes:Eachnodeisataskoranalysisintheconceptualdesignprocess.
Edges:Directededgesshowtheprerequisiterelationshipsbetweenthesetasksand
analyses.
```

**Example of** `{node_list_with_description}` **in the UCAV design activity DSM case:** 

```
[
{’id’:’lzOtR’,’name’:’CreateConfigurationConcepts’},
{’id’:’yLlKi’,’name’:’PrepareUCAVConceptualDR&O’},
{’id’:’Swvi2’,’name’:’Prepare3-ViewDrawing&GeometryData’},
{’id’:’CDcxF’,’name’:’PerformWeightsAnalyses&Evaluation’},
{’id’:’0KGDm’,’name’:’PerformAerodynamicsAnalyses&Evaluation’},
{’id’:’4wHtv’,’name’:’PerformMultidisciplinaryAnalyses&Evaluation’},
{’id’:’AgIBP’,’name’:’Prepare&DistributeChoiceConfig.DataSet’},
{’id’:’gRtHi’,’name’:’PerformS&CCharacteristicsAnalyses&Eval.’},
{’id’:’GV9RJ’,’name’:’MakeConceptAssessmentandVariantDecisions’},
{’id’:’I1j2m’,’name’:’PerformPerformanceAnalyses&Evaluation’},
{’id’:’Vzzm7’,’name’:’PerformPropulsionAnalyses&Evaluation’},
{’id’:’B0BFG’,’name’:’PerformMechanical&ElectricalAnalyses&Eval.’}
]
```

**Example of** `{node_list}` **in the UCAV design activity DSM case:** 

```
[’lzOtR’,’yLlKi’,’Swvi2’,’CDcxF’,’0KGDm’,’4wHtv’,’AgIBP’,’gRtHi’,’GV9RJ’,
’I1j2m’,’Vzzm7’,’B0BFG’]
```

**Example of** `{edge_list}` **in the UCAV design activity DSM case:** 

```
[
{’dependent’:’0KGDm’,’predecessor’:’Swvi2’},
{’dependent’:’AgIBP’,’predecessor’:’lzOtR’},
{’dependent’:’0KGDm’,’predecessor’:’yLlKi’},
{’dependent’:’Swvi2’,’predecessor’:’lzOtR’},
...
]
```

**Example of** `{selected_historical_solutions}` **in the UCAV design activity DSM case:** 

```
[
{’solution’:’lzOtR,yLlKi,GV9RJ,AgIBP,B0BFG,Vzzm7,Swvi2,CDcxF,0KGDm,I1j2m,
gRtHi,4wHtv’,’score’:15.0},
{’solution’:’B0BFG,yLlKi,Vzzm7,lzOtR,Swvi2,CDcxF,AgIBP,0KGDm,GV9RJ,I1j2m,
gRtHi,4wHtv’,’score’:13.0},
...
]
```

11 

LARGE LANGUAGE MODELS FOR COMBINATORIAL OPTIMIZATION OF DSM 

## **Appendix 2. Parameter settings for three variants of GA** 

In all three variants of the GA used for DSM sequencing tasks, we employed the following shared settings: the number of generations was set to 2,000, with a selection mechanism using tournament selection and mutation using shuffled indexes. The GA was implemented using the DEAP library with standard configurations for initial population generation [27]. The different configurations for each GA setting are shown in the table below. The meaning of each parameter also refers to [27]. 

||**Population**|**Individual Mutation**<br>**Probability**|**Tournament**<br>**Size**|**Crossover**<br>**Probability**|**Mutation**<br>**Probability**|
|---|---|---|---|---|---|
|**Exploration-focused**|50|0.05|5|0.6|0.4|
|**Exploitation-focused**|10|0.01|20|0.9|0.1|
|**Balanced**|20|0.02|10|0.7|0.3|



12 

