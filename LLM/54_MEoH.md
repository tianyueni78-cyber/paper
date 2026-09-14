**Multi-objective Evolution of Heuristic Using Large Language Model** 

# **Shunyu Yao**<sup>1,*</sup> **Fei Liu**<sup>1,*</sup> **Xi Lin**<sup>1</sup> **, Zhichao Lu**<sup>1</sup> **, Zhenkun Wang**<sup>2,†</sup> **, Qingfu Zhang**<sup>1,†</sup> 

1Department of Computer Science, City University of Hong Kong, Hong Kong, China 

2School of System Design and Intelligent Manufacturing, Southern University of Science and Technology, Shen Zhen, China 

_{_ shunyuyao8, fliu36 _}_ -c@my.cityu.edu.hk, _{_ xilin4, zhichao.lu _}_ @cityu.edu.hk, wangzhenkun90@gmail.com, qingfu.zhang@cityu.edu.hk 

### **Abstract** 

Heuristics are commonly used to tackle various search and optimization problems. Design heuristics usually require tedious manual crafting with domain knowledge. Recent works have incorporated Large Language Models (LLMs) into automatic heuristic search, leveraging their powerful language and coding capacity. However, existing research focuses on the optimal performance on the target problem as the sole objective, neglecting other criteria such as efficiency and scalability, which are vital in practice. To tackle this challenge, we propose to model the heuristic search as a multiobjective optimization problem and consider introducing additional practical criteria beyond optimal performance. Due to the complexity of the search space, conventional multiobjective optimization methods struggle to effectively handle LLM-based multi-objective heuristic search. We propose the first LLM-based multi-objective heuristic search framework, Multi-objective Evolution of <u>Heuristic (MEoH), which</u> integrates LLMs in a zero-shot manner to generate a nondominated set of heuristics to meet multiple design criteria. We design a new dominance-dissimilarity mechanism for effective population management and selection, which incorporates both code dissimilarity in the search space and dominance in the objective space. MEoH is demonstrated in two well-known combinatorial optimization problems: the online Bin Packing Problem (BPP) and the Traveling Salesman Problem (TSP). The results indicate that a variety of elite heuristics are automatically generated in a single run, offering more trade-off options than the existing methods. It successfully achieves competitive or superior performance while improving efficiency up to 10 times. Moreover, we also observe that the multi-objective search introduces novel insights into heuristic design and leads to the discovery of diverse heuristics. 

**Code** — https://github.com/Optima-CityU/LLM4AD 

# **1 Introduction** 

Heuristics are commonly used in solving optimization and decision-making problems in a variety of fields, including engineering (Bozorg-Haddad, Solgi, and Lo´aiciga 2017), 

*Equal contribution. 

> †Corresponding authors. 

Copyright © 2025, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved. 

industry (Silver 2004), and economics (Vasant 2012). Unlike exact methods, heuristics offer practical alternatives for finding sub-optimal solutions within a reasonable time cost (Pearl 1984) and are particularly adept at handling complex problems with diverse attributes and constraints. However, developing effective heuristics typically requires expert knowledge and involves laborious trial-and-error manual crafting, presenting a significant challenge for real-world applications. 

To address this challenge, much effort has been devoted to automating the design of heuristics (Pillay and Qu 2021). These efforts can be broadly classified into three categories: heuristic configuration (Ramos et al. 2005; Visheratin, Melnik, and Nasonov 2016), heuristic selection (Tang et al. 2014; Xu, Hoos, and Leyton-Brown 2010), and heuristic composition (Burke et al. 2010; Drake et al. 2020; Pillay and Qu 2018). Despite the successful creation of novel heuristics, the effectiveness of these heuristics still heavily relies on algorithmic components crafted by human experts (Drake et al. 2020). 

In recent years, Large Language Models (LLMs) have demonstrated remarkable capabilities in algorithm design (Liu et al. 2024b). The integration of LLMs with Evolutionary Computation (EC) has enabled the automatic generation and refinement of heuristics along with their corresponding code implementations (Liu et al. 2024a; RomeraParedes et al. 2024; Ye et al. 2024). The designed heuristics achieved competitive performance with minimized human design and model training. However, all existing LLMbased evolutionary heuristic search methods focus on a single objective regarding the optimized performance of the target problem (Ma et al. 2023; Nasir et al. 2024; Liu et al. 2024a; Romera-Paredes et al. 2024; Zhang et al. 2024; Yao et al. 2024; van Stein and B¨ack 2024; Li et al. 2024; Zeng et al. 2024; Mao et al. 2024; Ma et al. 2024). Other important heuristic design criteria, such as heuristic complexity (Ausiello et al. 2012) and code readability (Buse and Weimer 2009), which could be vital in practice, are often neglected. Although some studies have attempted to optimize multiple objectives by combining them into a single objective function, resulting in a single heuristic, the conflicting nature of diverse objectives often makes it challenging to find a single heuristic that satisfies all simultaneously. The exploration of effective methods for searching a set of non- 

dominated heuristics in a single run remains unexplored. 

In this study, we model the automatic heuristic design as a multi-objective optimization problem (Dr´eo 2009) and propose the first LLM-based multi-objective heuristic search framework, termed <u>Multi-objective Evolution of Heuristic</u> (MEoH), to effectively search for a set of non-dominated heuristics in a single run. The contributions of this paper are as follows: 

- We propose an LLM-based automated heuristic design framework to consider the heuristic design from a multiobjective optimization perspective. 

- We propose a dominance-dissimilarity mechanism to enhance diversity and improve search efficiency by considering both the dominance relationships in the objective space and the dissimilarity of heuristics in the search space. 

- We demonstrate the superiority compared with the counterpart of single-objective LLM-based automated heuristic design on two classical optimization problems: the Traveling Salesman Problem (TSP) and the online Bin Packing Problem (BPP). 

function design (Ma et al. 2023), molecular design (Wang et al. 2024), network design (Mao et al. 2024), and Bayesian optimization (Yao et al. 2024). While effective heuristics are developed, they often focus solely on performance for specific target instances, overlooking other crucial objectives like efficiency and complexity. 

## **2.3 Multi-objective Heuristic Design** 

Heuristic design can be modeled as a multi-objective optimization problem. Dr´eo (2009) consider automated heuristic design as a multi-objective problem to design a set of nondominated heuristics to balance optimality and efficiency. S- Race (Zhang, Georgiopoulos, and Anagnostopoulos 2013) employs a racing algorithm to automatically choose machine learning models based on multiple objectives. Furthermore, MO-ParamILS (Blot et al. 2016) extends the singleobjective heuristic configuration framework ParamILS to handle multiple objectives. Multi-objective genetic programming has also been utilized in heuristic search (Schmidt and Lipson 2009; Vladislavleva, Smits, and Den Hertog 2008; Fan et al. 2024). However, they still demand existing hand-crafted primitives for defining and generating heuristics. 

# **2 Related Works** 

## **2.1 Automated Heuristic Design** 

Automated heuristic design methods can be broadly classified into automated heuristic configuration, automated heuristic selection, and automated heuristic composition (Pillay and Qu 2021). The first category involves using optimization methods and machine learning techniques (Ramos et al. 2005; Visheratin, Melnik, and Nasonov 2016) to automatically adjust the parameters within a given algorithm framework (Agasiev and Karpenko 2017). The second category focuses on automatically choosing a suitable heuristic for each specific instance from a pool of existing heuristics (Tang et al. 2014; Xu, Hoos, and LeytonBrown 2010). The third category combines various algorithmic elements to create novel heuristics (Burke et al. 2010; Drake et al. 2020; Pillay and Qu 2018). While these methods have shown promise in enhancing the automation of heuristic design and improving performance, they still heavily rely on human-designed algorithmic components. 

## **2.2 LLM-based Automated Heuristic Design** 

Large language models have shown remarkable performance across a variety of tasks and exhibit promising zeroshot capabilities in linguistic processing and code generation. The use of LLMs in automated heuristic design is still in its early stages (Liu et al. 2024b). For example, FunSearch (Romera-Paredes et al. 2024) leverages LLMs to generate and improve code implementations of heuristics based on EC frameworks, achieving state-of-the-art results in mathematical and combinatorial optimization problems. EoH (Liu et al. 2024a) evolves both idea descriptions and code implementations of heuristics simultaneously, leading to competitive performance in a more efficient manner. This EC+LLM approach has been successfully applied in heuristic and function design across various tasks such as reward 

# **3 Preliminaries** 

## **3.1 Multi-objective Optimization** 

A Multi-objective Optimization Problem (MOP) can be defined as 



where _X_ represents the search space, **_x_** is a decision vector, and **_f_** ( **_x_** ) is an _M_ -objective vector to optimize. A non-trivial MOP cannot be solved by a single decision vector, and we have the following definitions for multi-objective optimization: 

**Pareto Dominance** : Let **_x_** _a,_ **_x_** _b ∈X_ , **_x_** _a_ is said to dominate **_x_** _b_ ( **_x_** _a ≺_ **_x_** _b_ ) if and only if _fi_ ( **_x_** _a_ ) _≤ fi_ ( **_x_** _b_ ) _, ∀i ∈ {_ 1 _,_ 2 _, . . . , M }_ and _fj_ ( **_x_** _a_ ) _< fj_ ( **_x_** _b_ ) _, ∃j ∈{_ 1 _,_ 2 _, . . . , M }_ . 

**Pareto Optimality** : A decision vector **_x_**<sup>_∗_</sup> _∈X_ is Paretooptimal if there does not exist **_x_**<sup>_′_</sup> _∈X_ dominates **_x_**<sup>_∗_</sup> , i.e., ∄ **_x_**<sup>_′_</sup> _∈X_ such that **_x_**<sup>_′_</sup> _≺_ **_x_**<sup>_∗_</sup> . 

**Pareto Set/Front** : The set of all Pareto-optimal decision vectors is called the Pareto Set (PS), and its mapping in the objective space is called the Pareto Front (PF). 

In this paper, we investigate multi-objective heuristic design. The decision vector **_x_** indicates the heuristic and the _M_ -objective vector represents different criteria measuring different aspects of the performance of heuristics (e.g., optimal performance and complexity). 

## **3.2 Multi-objective Evolutionary Algorithms** 

Multi-objective Evolutionary Algorithms (MOEAs) are among the most commonly used methods to solve MOPs. MOEAs work by maintaining a population of _N_ candidate individuals that evolve iteratively through genetic operators like crossover and mutation. There are three main paradigms for MOEAs: the dominance-based approach (Deb et al. 



<!-- Start of picture text -->
Optimal Gap Optimal Gap<br>Designer LLM LLM<br>Objective Objective Optimal Gap<br>Objectives<br>… … … …<br>Thought Code Thoughts Codes Thoughts Codes<br>(a) Manual Heuristic Design (b) Single-objective LLM-based (c) Multi-objective LLM-based<br>Heuristic Design  Heuristic Design, MEoH (Ours)<br>Complexity<br><!-- End of picture text -->

Figure 1: Comparison to human design and existing LLM-based heuristic design (a) manual heuristic design by human experts, (b) single-objective LLM-based heuristic design (e.g., FunSearch and EoH), and (c) our proposed multi-objective heuristic design (MEoH). 

2002), the decomposition-based approach (Zhang and Li 2007), and the indicator-based approach (Zitzler and K¨unzli 2004). 

# **4 Methodology** 

## **4.1 Framework** 

Multi-objective Evolution of Heuristic (MEoH) is a fusion of LLMs and multi-objective evolutionary optimization for effective multi-objective heuristic design. As illustrated in Algorithm 1, MEoH begins with population initialization, where the population comprises heuristics, and progressively improves the population using MOEA until the termination condition is satisfied, to obtain a set of non-dominated heuristics that represent trade-offs among multiple objectives. Throughout each iteration, MEoH generates offspring using search operators. These operators are implemented through LLMs and predefined prompts to create offspring based on the selected parents from the population. New offspring are added to the population and population management is utilized to update the population to keep its size, with a focus on maintaining diversity and convergence. The dominance-dissimilarity mechanism is utilized in both parent selection and population management. Detailed explanations of each of these components will be provided in the subsequent sections. 

MEoH advances existing LLM-based heuristic design by extending the single-objective approach (Romera-Paredes et al. 2024; Liu et al. 2024a) to the multi-objective scenarios and designing a set of non-dominated heuristics in a single run. Moreover, unlike directly combining MOEA and LLM-based heuristic search, MEoH introduces a unique dominance-dissimilarity measure to navigate the complex and discrete heuristic search space, overcoming challenges faced by conventional MOEAs like NSGA-II (Deb et al. 2002) and MOEA/D (Zhang and Li 2007). 

## **4.2 Dominance-dissimilarity Mechanism** 

Traditional MOEAs (Deb et al. 2002; Zhang and Li 2007) and single-objective LLM-based heuristic design meth- 

Algorithm 1: MEoH 

- 1: **Input:** Population size _N_ ; Maximum number of iterations _T_ , Parent selection size _d_ ; Initial population **_P_** 0; Pre-trained LLM _L_ . 

- 2: **Output:** Approximate Pareto-set **_P_**<sup>_∗_</sup> . 

- 3: **if** **_P_** 0 = _∅_ **then** 

- 4: **for** _i_ = 1 _, . . . , N_ **do** 5: _o ←_ Generation( _L_ ); 6: **_P_** 0 _←_ **_P_** 0 _∪ o_ 7: **end for** 8: **end if** 9: **for** _t_ = 1 _, . . . , T_ **do** 

- 10: **for** _i_ = 1 _, . . . , N_ **do** 11: **_P_** _parent ←_ ParentSelection( **_P_** _t−_ 1, _d_ ); 12: _o ←_ Search( _L,_ **_P_** _parent_ ); 13: **_P_** _t−_ 1 _←_ **_P_** _t−_ 1 _∪ o_ 14: **end for** 15: **_P_** _t ←_ PopulationManagement( **_P_** _t−_ 1 _, N_ ) 

- 16: **end for** 

- 17: **_P_**<sup>_∗_</sup> _←_ **_P_** _T_ 

ods (Romera-Paredes et al. 2024; Liu et al. 2024a) lack effective diversity maintenance strategies for multi-objective automated heuristic design. To address this, we propose a novel dominance-dissimilarity mechanism that considers both objective space dominance and heuristic search space dissimilarity. 

**Dominance Measure in Objective Space:** In the objective space, the Pareto dominance relationship between each pair of heuristics is evaluated, which is widely used in MOEAs (Zitzler and Thiele 1998; Deb et al. 2002). 

**Dissimilarity Measure in Search Space:** In the search space, the heuristics are represented through natural language descriptions and implemented in Python code. We evaluate the dissimilarity between code segments. Notably, there are various techniques available for this purpose, and we choose to utilize the widely adopted Abstract Syntax Tree (AST) (Neamtiu, Foster, and Hicks 2005). The AST 

converts the code segment to an abstract syntactic structure (Baxter et al. 1998). And the similarity of code _a_ and code _b_ can be calculated based on the tree structures following Ren et al. (2020): 

SimAST( _a, b_ ) = Countclip(Tree _a_ ) _/_ Count(Tree _b_ ) _,_ (2) 

where Count(Tree _b_ ) is the number of subtrees of Tree _b_ , and Countclip(Tree _a_ ) is the number of subtrees of Tree _a_ that are matched the Tree _b_ . The AST similarity value ranges from 0 to 1, with 0 indicating complete dissimilarity between the two code segments and 1 signifying identical code segments. This quantitative approach enables the assessment of structural similarity between code segments, facilitating the comparison and evaluation of heuristics based on their code implementations. 

**Dominance-dissimilarity Score:** As illustrated in Figure 2, to determine the dominance-dissimilarity of each heuristic in the population, the dissimilarity, i.e., the negative AST similarity, between each pair of heuristics is calculated and stored in a matrix. Concurrently, in the objective space, the dominance relationship between each pair of heuristics is captured and represented as a mask with the same size as the dissimilarity matrix. Specifically, only the dominance relationship is considered, while all other relationships are masked. Subsequently, the masked dissimilarity matrix is aggregated column-wise. The resulting dominance-dissimilarity score vector encapsulates both dominance and diversity aspects to guide parent selection and population management in the subsequent steps. The details can be found in Appendix A. 

## **4.3 Heuristic Representation** 

Similar to Liu et al. (2024a), each heuristic in MEoH is composed of three elements: a description in plain language, a code snippet in a specific format, and a fitness score. 

The description is a brief linguistic explanation generated by LLMs that conveys the main idea. The code snippet is the actual implementation of the heuristic. In the experiments, we opted to use Python functions for implementation. The code snippet must include the 1) function name, 2) input variables, and 3) output variables for clarity. The fitness is evaluated on a set of instances for the specific target problem. Example heuristics can be found in Appendix H. 

## **4.4 Heuristic Generation** 

**Initial Heuristic Generation** The initial population of MEoH is comprised of heuristics. These heuristics can be generated by leveraging a LLM with a predefined generation prompt or by using human-designed existing heuristics. In order to fully demonstrate the capability of MEoH in designing competitive heuristics, we let LLM generate all the heuristics in both the initiation and evolution processes. 

**Offspring Heuristic Generation** The parent selection is the first step of generating offspring, in which a set of parent heuristics **_P_** _parent_ are selected from the current population. To consider both convergence and diversity in the heuristic search process, the dominance-dissimilarity score is utilized to guide the probability of parent selection. A higher 

dominance-dissimilarity score indicates a lower likelihood of being dominated or a more diverse code segment, making it preferable. The parents are selected with probability proportional to their dominance-dissimilarity scores. The details can be found in Appendix A. 

The selected parent heuristics serve as samples in the prompt to instruct LLM in generating offspring heuristics. We employ five different search operators with diverse prompt strategies adapted from EoH (Liu et al. 2024a) to produce offspring heuristics. The details of these prompts can be found in Appendix G. 

## **4.5 Population Management** 

As the offspring generated through search operations are incorporated into the population, the size of the population gradually increases. In order to ensure a consistent population size and update the population effectively, a population management strategy is proposed. The dominancedissimilarity score is utilized for this purpose. Specifically, the heuristics in the population are sorted based on their dominance-dissimilarity score and the worst heuristics are removed to ensure that only the most promising individuals are retained within the population, as detailed in Appendix A. By employing this strategy, the population is continually refined to maintain a high-quality and diverse set of individuals, enhancing the overall efficiency and effectiveness of the evolutionary process. 

# **5 Experiments** 

## **5.1 Experimental Settings** 

**Problems & Implementation Details** We demonstrate MEoH on two representative combinatorial optimization problems: 

1) _Online Bin Packing Problem:_ In online Bin Packing Problem (BPP) (Seiden 2002), a set of items, each with its own weight, needs to be packed into bins with a predetermined capacity. The objective of the BPP is to minimize the total number of bins required to accommodate all the items. In an online scenario, items are packed as they are received without prior knowledge. The generated heuristics are evaluated on 5 Weibull instances with 5 _,_ 000 items (referred to as 5k), and the capacity of bins is 100. 

We inherit the settings from Romera-Paredes et al. (2024) to design constructive heuristics for aligning the arriving items to the appropriate bins. The designed heuristics involve a function scoring the bins, where the input includes the arriving item size and the remaining capacities of the bins. The item will be assigned to the bin with the highest score. 

2) _Travelling Salesman Problem:_ In Traveling Salesman Problem (TSP) (Reinelt 2003), the objective is to find the shortest route that visits all given nodes exactly once and returns to the starting node. In this work, we evaluate the fitness of designed heuristics during evolution on 64 instances with 100 nodes. The coordinate of each node is randomly sampled from [0 _,_ 1] (Kool, van Hoof, and Welling 2018). 

The Guided Local Search (GLS) framework is employed (Voudouris, Tsang, and Alsheddy 2010) to iteratively 



<!-- Start of picture text -->
Dissimilarity Dominance<br>Search Space Objective Space<br>≺ 1 2 3 4 5<br>Code1 Code2 1 0 -0.5 -0.4 -0.9 -0.2<br>Code3 2 -0.4 0 -0.3 -0.6 -0.6<br>Code5 3 -0.5 -0.2 0 -0.7 -0.1<br>Code4 4 -0.7 -0.7 -0.6 0 -0.4<br>0.3 Probability 5 -0.3 -0.5 -0.2 -0.5 0 New Population𝑓𝑓1<br>0.25<br>0.2 � 0 0 -0.3 0 -0.8 1 2 4 3 5<br>0.15<br>0.1 0 0 0 -0.3 -0.8<br>0.05 Parent Selection Population Management<br>0<br>Code1 Code2 Code4<br>𝑓𝑓2<br><!-- End of picture text -->

Figure 2: An illustration of parent selection and population management with dominance-dissimilarity mechanism. By incorporating code dissimilarity in the search space and dominance relationships in the objective space, the parent selection and population management are enhanced to promote diversity and improve search efficiency. 

improve the solution quality following (Liu et al. 2024a). GLS iteratively performs two steps: 1) local search and 2) perturbation. Until the stop criterion is satisfied, the best solution obtained throughout the iterations is considered the final solution. We aim to design a heuristic to update the distance matrix in the perturbation step. 

The experimental parameter settings are as follows: the number of generations is 20, and the population size is 20 and 10 for online BPP and TSP, respectively. Each crossover operator selects 5 parent heuristics to reproduce the offspring heuristics. The number of iterations and running time in the GLS for TSP is limited to 1 _,_ 000 and 60 seconds, respectively. 

**Environments** To ensure fairness and consistency, all experiments in this study were conducted on a computer equipped with an Intel Core i7-11700 processor and 32GB of memory. GPT3.5-turbo is employed as the per-trained LLM, with each experiment repeated three times to ensure the robustness and reliability of the results. 

### **Performance Metric** 

**Objectives** 1) _Optimal Gap:_ We use the optimal gap to baseline as the first objective (e.g., the gap between the number of bins used in designed heuristics to the lower bound of bin number). 2) _Efficiency:_ The running time of heuristics is used as the second objective to reflect the efficiency of heuristics. 

**Metric** 1) _Hypervolume:_ The Hypervolume(HV) is a commonly used metric in multi-objective optimization. It provides a comprehensive assessment of convergence and diversity of the approximate Pareto front without the ground truth Pareto front (Audet et al. 2021). A larger HV value indicates a better performance. 2) _IGD:_ The Inverted Generational Distance(IGD) measures the quality of the generated approximate Pareto front in relation to the reference set. Here the reference set is the nondominated set derived from the union of all generated heuristics. A lower IGD value is preferred, which indicates better convergence and diversity, 

implying that the generated population is closer to the reference set. The detailed formulation of the two metrics can be found in Appendix D. 

**Baseline Methods** In this study, our primary focus lies in exploring LLM-based automated heuristic design approaches. Consequently, we compare the two closest related works, namely FunSearch (Romera-Paredes et al. 2024) and EoH (Liu et al. 2024a). The details can be found in Appendix C. 

## **5.2 Experimental Results** 

**Convergence Analysis** The curve of HV and IGD for the heuristic populations generated in each iteration on BPP are displayed in Figure 3(b) and (c), respectively. As EoH only pursues optimal gaps without considering diversity, the HV and IGD become worse as the evolution progresses. In contrast, MEoH systematically takes into account both the optimal gap and running time. As a result, MEoH achieves notably higher HV and lower IGD, indicating significantly better multi-objective trade-off results. Figure 4(b) and (c) provide more evidence on TSP. MEoH converges faster and clearly outperforms EoH in terms of HV and IGD. Additionally, the average dominance-dissimilarity score is shown in Figure 3 (d) and Figure 4 (d). Results demonstrate the superiority of MEoH and the efficiency of our dominancedissimilarity mechanism in maintaining population diversity. The details can be found in Appendix F. 

**Pareto Fronts** Figure 3(a) and Figure 4(a) compare the non-dominated heuristics of the final population obtained by MEoH and EoH. Results show that 1) MEoH generates a diverse set of heuristics with different trade-offs over the two objectives. In contrast, EoH only finds similar heuristics that cover a much smaller region in the objective space. 2) The heuristics obtained from MEoH can significantly reduce the running time (up to 10 times) when achieving a similar optimal gap. 

**Performance Measurement** 1) _BPP:_ To comprehensively evaluate the performance of our MEoH in more gen- 



<!-- Start of picture text -->
Pareto Front HV IGD Dominance-dissimilarity<br>1.5 0.8 0<br>MEoH 1.0 MEoH<br>1.0 EoH 0.6 EoH 25<br>0.5 0.4 50<br>0.5 MEoH ME o H<br>EoH 0.2 75 EoH<br>0.0<br>2 4 5 10 15 20 5 10 15 20 5 10 15<br>Gap Iterations Iterations Iterations<br>(a) Pareto Front (b) HV (c) IGD (d) Score<br>Figure 3: Comparations of EoH and MEoH on BPP5k.<br>Pareto Front HV IGD Dominance-dissimilarity<br>20 MEoH 1.0 7.5 0<br>EoH 20<br>MEoH 5.0<br>10 0.5 EoH 40<br>2.5 MEoH MEoH<br>EoH 60 EoH<br>0.0<br>0 0.0<br>7.8 7.9 8.0 5 10 15 20 5 10 15 20 5 10 15<br>Gap Iterations Iterations Iterations<br>(a) Pareto Front (b) HV (c) IGD (d) Score<br>Running Time/s<br>Running Time/s<br><!-- End of picture text -->

Figure 4: Comparations of EoH and MEoH on TSP100. 

eral cases, we test FunSearch, EoH, and MEoH on various problem instances with different sizes and capacities. The problem sizes in our test include 5k, 10k, and 100k, and the capacities of the bins are set at 100 and 500. Each test set consists of five instances sampled from Weibull distribution (Romera-Paredes et al. 2024). The average gap with reference to the relaxation lower bound _lb_ and the running time are shown in Table 1. For the in-distribution instances, i.e., the bin capacity is 100, all of these three frameworks exhibit promising performance in terms of the optimal gap, and the running time of MEoH heuristics are significantly less than the counterparts of FunSearch and EoH, especially in largesize instances, i.e., BPP100k. MEoH heuristics achieve competitive performance compared to EoH but do so in significantly less running time (up to 10 times faster). In contrast, for out-distribution instances, i.e., the bin capacity is 500, the performance of FunSearch heuristics drastically deteriorates in terms of the optimal gap. On the other hand, both EoH and MEoH heuristics exhibit promising performances in such scenarios. Notably, MEoH demonstrates a balanced tradeoff between the optimal gap and running time, showcasing its effectiveness in handling out-distribution instances efficiently. 

2) _TSP:_ We evaluate these three methods on randomly generated TSP instances comprising 100, 500, and 1 _,_ 000 nodes and a variety of TSP instances with up to 1 _,_ 002 nodes from TSPLIB (Reinelt 1991). Table 2 and Table 3 display the gap compared to the best-known solution (for the randomly generated instances, the best-known solutions are obtained using the Concorde solver (Applegate et al. 2006)) 

|Weibull|FunSe<br>|arch<br>|Eo<br>|H<br>|ME<br>|oH<br>|
|---|---|---|---|---|---|---|
||Gap|Time/s|Gap|Time/s|Gap|Time/s|
|5k C100|0.802%|0.728|0.753%|1.362|1.387%|0.191|
|10k C100|2.595%|2.128|0.537%|5.128|0.651%|0.650|
|100k C100|3.319%|195.734|0.391%|502.938|0.080%|59.078|
|Avg.|2.239%|66.197|0.560%|169.809|0.706%|19.973|
|5k C500|29.494%|0.750|0.100%|1.672|0.351%|0.100|
|10k C500|47.734%|2.459|0.125%|6.337|0.473%|0.306|
|100k C500|53.640%|259.094|0.099%|646.828|0.410%|22.078|
|Avg.|43.623%|87.434|0.108%|218.279|0.411%|7.495|



Table 1: Results of in- and out-of-distribution BPP. 

and the corresponding running times. As shown in Table 2, FunSearch and MEoH (Best) heuristics exhibit promising performance on TSP100 and TSP500 instances. In general, MEoH provides a set of heuristics that enable trade-offs between optimality and efficiency. As shown in Table 3, for smaller instances (up to 200 nodes), the MEoH heuristics demonstrate superior performance in terms of both the optimal gap and running time. For larger instances (201 to 1 _,_ 002 nodes), MEoH still outperforms in running time, although slightly lagging behind EoH in terms of the optimal gap. The details can be found in Appendix E. 

## **5.3 Comparison to Conventional MOEAs** 

In this section, we evaluate the impact of our proposed dominance-dissimilarity mechanism on the optimization process and compare to two representative MOEAs: NSGAII (Deb et al. 2002) and MOEA/D (Zhang and Li 2007). 

||TSP|100|TSP|500|TSP|1000|
|---|---|---|---|---|---|---|
||Gap|Time/s|Gap|Time/s|Gap|Time/s|
|FunSearch|0.100%|1.452|1.525%|27.598|2.344%|161.124|
|EoH|0.113%|22.434|1.750%|43.541|2.524%|262.603|
|MEoH(Best)|0.109%|1.373|1.733%|30.945|4.208%|26.844|
|MEoH(Fast)|3.690%|0.175|4.402%|3.306|4.536%|21.900|



Table 2: Results of in- and out-of-distribution randomly generated TSP. 

|TSPLIB|FunS|earch|E|oH|ME|oH|
|---|---|---|---|---|---|---|
||Gap|Time/s|Gap|Time/s|Gap|Time/s|
|Avg. (0-200)|0.050%|3.418|0.093%|25.917|0.018%|2.354|
|Avg. (201-1002)|1.535%|419.613|1.376%|1515.992|1.50%|355.754|



Table 3: Results of small and large TSPLIB instances. 

||TSP|LIB|BPP|C100|
|---|---|---|---|---|
||Gap|Time/s|Gap|Time/s|
|FunSearch|0.050%|3.418|2.239%|66.197|
|EoH|0.093%|25.917|0.560%|169.809|
|MEoH (Best)|0.018%|2.354|0.706%|19.973|
|MEoH (Fast)|3.563%|0.138|4.326%|6.533|



Table 4: Two top heuristics designed by MEoH. 



<!-- Start of picture text -->
HV IGD<br>0.6 MOEA/D 3 MOEA/D<br>NSGA-II NSGA-II<br>0.4 2<br>MEoH MEoH<br>0.2 1<br>0.0 0<br>5 10 15 20 5 10 15 20<br>Iterations Iterations<br>(a) HV (b) IGD<br><!-- End of picture text -->

Figure 5: Comparison to conventional MOEAs on BPP. 



<!-- Start of picture text -->
HV IGD<br>0.8 MOEA/D<br>0.4 NSGA-II<br>0.6<br>MOEA/D MEoH<br>0.4 NSGA-II 0.2<br>MEoH<br>0.2 0.0<br>5 10 15 20 5 10 15 20<br>Iterations Iterations<br>(a) HV (b) IGD<br><!-- End of picture text -->

Figure 6: Comparison to conventional MOEAs on TSP. 

Figure 5 and Figure 6 depict the results on BPP and TSP, respectively. MEoH can obtain the best HV and IGD. Our findings highlight the effectiveness of our dominancedissimilarity mechanism, which integrates considerations 

from both the search and objective spaces, in improving the optimization process. 



<!-- Start of picture text -->
Pareto Front<br>2000<br>40 MEoH<br>1 500 EoH *<br>1 000<br>20<br>5 00<br>100<br>0<br>7.8 7.9 8.0<br>Gap<br>Running Time/s<br><!-- End of picture text -->

Figure 7: Comparations of the non-dominated heuristics generated by MEoH and the any-time performance of the best heuristic generated by EoH (termed as EoH<sup>_∗_</sup> ) on TSP. 

## **5.4 Comparison to Any-time Performance** 

The performance of a single heuristic at any given time can provide a set of heuristics that offer different trade-offs between optimal gap and running time. For instance, reducing the number of iterations in GLS from 1 _,_ 000 to 100 results in a decrease in running time but a deterioration in the optimal gap. By comparing the heuristics generated by MEoH to the best heuristic produced by EoH, we can further illustrate the benefits of multi-objective heuristic design. We evaluate the performance of the best EoH heuristic with varying numbers of iterations. Figure 7 demonstrates that the heuristics generated by MEoH outperform those of EoH. Even the best EoH heuristic with 100 iterations falls short in terms of running time and optimal gap compared to all MEoH heuristics. Additionally, while the best EoH heuristic with 2 _,_ 000 iterations can achieve competitive optimality, it lags behind in running time by approximately 20 times. 

# **6 Conclusion, Limitation, and Future Work** 

**Conclusion** This paper develops a novel framework, termed MEoH, for LLM-based multi-objective automatic heuristic design. We propose a dominance-dissimilarity mechanism for effective search in the discrete and complex heuristic space. We demonstrate MEoH on two widelystudied combinatorial optimization problems to optimize both heuristics’ optimal gap and running time. Results show that MEoH significantly outperforms existing LLM-based heuristic design methods including FunSearch and EoH in producing trade-off heuristics over multiple objectives. The efficiency can be increased dramatically up to 10 times with a close optimal gap. Moreover, additional ablation studies and visualization of the evolution process validate the superiority of MEoH over conventional MOEAs and the effectiveness of the proposed dominance-dissimilarity mechanism in multi-objective automatic heuristic design. 

**Limitation and Future Work** Although we have demonstrated the effectiveness of MEoH primarily on two objectives, and three objectives in Appendix I, we aim to investigate the performance of MEoH on many-objective cases and a broader range of heuristic design tasks. 

# **Acknowledgments** 

This work was supported by the Research Grants Council of the Hong Kong Special Administrative Region, China (GRF Project No. CityU 11215622), the National Natural Science Foundation of China (Grant No. 62106096 and Grant No. 62476118), the Natural Science Foundation of Guangdong Province (Grant No. 2024A1515011759), the National Natural Science Foundation of Shenzhen (Grant No. JCYJ20220530113013031). 

# **References** 

Agasiev, T.; and Karpenko, A. 2017. The program system for automated parameter tuning of optimization algorithms. _Procedia Computer Science_ , 103: 347–354. 

Applegate, D.; Bixby, R.; Chvatal, V.; and Cook, W. 2006. Concorde TSP solver. 

Audet, C.; Bigeon, J.; Cartier, D.; Le Digabel, S.; and Salomon, L. 2021. Performance indicators in multiobjective optimization. _European journal of operational research_ , 292(2): 397–422. 

Ausiello, G.; Crescenzi, P.; Gambosi, G.; Kann, V.; Marchetti-Spaccamela, A.; and Protasi, M. 2012. _Complexity and approximation: Combinatorial optimization problems and their approximability properties_ . Springer Science & Business Media. 

Baxter, I. D.; Yahin, A.; Moura, L.; Sant’Anna, M.; and Bier, L. 1998. Clone detection using abstract syntax trees. In _Proceedings. International Conference on Software Maintenance (Cat. No. 98CB36272)_ , 368–377. IEEE. 

Blot, A.; Hoos, H. H.; Jourdan, L.; Kessaci-Marmion, M.-E.;<sup>´</sup> and Trautmann, H. 2016. MO-ParamILS: A multi-objective automatic algorithm configuration framework. In _Learning and Intelligent Optimization: 10th International Conference, LION 10, Ischia, Italy, May 29–June 1, 2016, Revised Selected Papers 10_ , 32–47. Springer. 

Bozorg-Haddad, O.; Solgi, M.; and Lo´aiciga, H. A. 2017. _Meta-heuristic and evolutionary algorithms for engineering optimization_ . John Wiley & Sons. 

Burke, E. K.; Hyde, M.; Kendall, G.; Ochoa, G.; Ozcan,<sup>¨</sup> E.; and Woodward, J. R. 2010. A classification of hyperheuristic approaches. _Handbook of metaheuristics_ , 449– 468. 

Buse, R. P.; and Weimer, W. R. 2009. Learning a metric for code readability. _IEEE Transactions on software engineering_ , 36(4): 546–558. 

Deb, K.; Pratap, A.; Agarwal, S.; and Meyarivan, T. 2002. A fast and elitist multiobjective genetic algorithm: NSGAII. _IEEE transactions on evolutionary computation_ , 6(2): 182–197. 

Drake, J. H.; Kheiri, A.; Ozcan, E.; and Burke, E. K. 2020.<sup>¨</sup> Recent advances in selection hyper-heuristics. _European Journal of Operational Research_ , 285(2): 405–428. 

Dr´eo, J. 2009. Using performance fronts for parameter setting of stochastic metaheuristics. In _Proceedings of the 11th Annual Conference Companion on Genetic and Evolutionary Computation Conference: Late Breaking Papers_ , 2197– 2200. 

Fan, L.; Su, Z.; Liu, X.; and Wang, Y. 2024. Decomposition based cross-parallel multiobjective genetic programming for symbolic regression. _Applied Soft Computing_ , 112239. 

Kool, W.; van Hoof, H.; and Welling, M. 2018. Attention, Learn to Solve Routing Problems! In _International Conference on Learning Representations_ . 

Li, H.; Yang, X.; Wang, Z.; Zhu, X.; Zhou, J.; Qiao, Y.; Wang, X.; Li, H.; Lu, L.; and Dai, J. 2024. Auto mc-reward: Automated dense reward design with large language models for minecraft. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 16426–16435. 

Liu, F.; Xialiang, T.; Yuan, M.; Lin, X.; Luo, F.; Wang, Z.; Lu, Z.; and Zhang, Q. 2024a. Evolution of Heuristics: Towards Efficient Automatic Algorithm Design Using Large Language Model. In _Forty-first International Conference on Machine Learning_ . 

Liu, F.; Yao, Y.; Guo, P.; Yang, Z.; Lin, X.; Tong, X.; Yuan, M.; Lu, Z.; Wang, Z.; and Zhang, Q. 2024b. A Systematic Survey on Large Language Models for Algorithm Design. _arXiv preprint arXiv:2410.14716_ . 

Ma, P.; Wang, T.-H.; Guo, M.; Sun, Z.; Tenenbaum, J. B.; Rus, D.; Gan, C.; and Matusik, W. 2024. LLM and Simulation as Bilevel Optimizers: A New Paradigm to Advance Physical Scientific Discovery. _arXiv preprint arXiv:2405.09783_ . 

Ma, Y. J.; Liang, W.; Wang, G.; Huang, D.-A.; Bastani, O.; Jayaraman, D.; Zhu, Y.; Fan, L.; and Anandkumar, A. 2023. Eureka: Human-level reward design via coding large language models. _arXiv preprint arXiv:2310.12931_ . 

Mao, J.; Zou, D.; Sheng, L.; Liu, S.; Gao, C.; Wang, Y.; and Li, Y. 2024. Identify Critical Nodes in Complex Network with Large Language Models. _arXiv preprint arXiv:2403.03962_ . 

Nasir, M. U.; Earle, S.; Togelius, J.; James, S.; and Cleghorn, C. 2024. LLMatic: neural architecture search via large language models and quality diversity optimization. In _Proceedings of the Genetic and Evolutionary Computation Conference_ , 1110–1118. 

Neamtiu, I.; Foster, J. S.; and Hicks, M. 2005. Understanding source code evolution using abstract syntax tree matching. In _Proceedings of the 2005 international workshop on Mining software repositories_ , 1–5. 

Pearl, J. 1984. _Heuristics: intelligent search strategies for computer problem solving_ . Addison-Wesley Longman Publishing Co., Inc. 

Pillay, N.; and Qu, R. 2018. _Hyper-heuristics: theory and applications_ . Springer. 

Pillay, N.; and Qu, R. 2021. _Automated Design of Machine Learning and Search Algorithms_ . Springer. 

Ramos, I. C.; Goldbarg, M. C.; Goldbarg, E. G.; and Neto, A. D. D. 2005. Logistic regression for parameter tuning on an evolutionary algorithm. In _2005 IEEE congress on evolutionary computation_ , volume 2, 1061–1068. IEEE. 

Reinelt, G. 1991. TSPLIB–A Traveling Salesman Problem Library. _ORSA Journal on Computing_ , 3(4): 376–384. 

Reinelt, G. 2003. _The traveling salesman: computational solutions for TSP applications_ , volume 840. Springer. 

Ren, S.; Guo, D.; Lu, S.; Zhou, L.; Liu, S.; Tang, D.; Sundaresan, N.; Zhou, M.; Blanco, A.; and Ma, S. 2020. Codebleu: a method for automatic evaluation of code synthesis. _arXiv preprint arXiv:2009.10297_ . 

Romera-Paredes, B.; Barekatain, M.; Novikov, A.; Balog, M.; Kumar, M. P.; Dupont, E.; Ruiz, F. J.; Ellenberg, J. S.; Wang, P.; Fawzi, O.; et al. 2024. Mathematical discoveries from program search with large language models. _Nature_ , 625(7995): 468–475. 

Schmidt, M.; and Lipson, H. 2009. Distilling free-form natural laws from experimental data. _science_ , 324(5923): 81–85. Seiden, S. S. 2002. On the online bin packing problem. _Journal of the ACM (JACM)_ , 49(5): 640–671. 

Silver, E. A. 2004. An overview of heuristic solution methods. _Journal of the operational research society_ , 55: 936– 956. 

Tang, K.; Peng, F.; Chen, G.; and Yao, X. 2014. Populationbased algorithm portfolios with automated constituent algorithms selection. _Information Sciences_ , 279: 94–104. 

Zeng, J.; Li, C.; Sun, Z.; Zhao, Q.; and Zhou, G. 2024. tnGPS: Discovering Unknown Tensor Network Structure Search Algorithms via Large Language Models (LLMs). In _Forty-first International Conference on Machine Learning_ . Zhang, Q.; and Li, H. 2007. MOEA/D: A multiobjective evolutionary algorithm based on decomposition. _IEEE Transactions on evolutionary computation_ , 11(6): 712–731. 

Zhang, R.; Liu, F.; Lin, X.; Wang, Z.; Lu, Z.; and Zhang, Q. 2024. Understanding the Importance of Evolutionary Search in Automated Heuristic Design with Large Language Models. In _International Conference on Parallel Problem Solving from Nature_ , 185–202. Springer. 

Zhang, T.; Georgiopoulos, M.; and Anagnostopoulos, G. C. 2013. S-Race: A multi-objective racing algorithm. In _Proceedings of the 15th annual conference on Genetic and evolutionary computation_ , 1565–1572. 

Zitzler, E.; and K¨unzli, S. 2004. Indicator-based selection in multiobjective search. In _International conference on parallel problem solving from nature_ , 832–842. Springer. 

Zitzler, E.; and Thiele, L. 1998. An evolutionary algorithm for multiobjective optimization: The strength pareto approach. _TIK report_ , 43. 

van Stein, N.; and B¨ack, T. 2024. LLaMEA: A Large Language Model Evolutionary Algorithm for Automatically Generating Metaheuristics. _arXiv preprint arXiv:2405.20132_ . 

Vasant, P. M. 2012. _Meta-heuristics optimization algorithms in engineering, business, economics, and finance_ . IGI Global. 

Visheratin, A. A.; Melnik, M.; and Nasonov, D. 2016. Automatic workflow scheduling tuning for distributed processing systems. _Procedia Computer Science_ , 101: 388–397. 

Vladislavleva, E. J.; Smits, G. F.; and Den Hertog, D. 2008. Order of nonlinearity as a complexity measure for models generated by symbolic regression via pareto genetic programming. _IEEE Transactions on Evolutionary Computation_ , 13(2): 333–349. 

Voudouris, C.; Tsang, E. P.; and Alsheddy, A. 2010. Guided local search. In _Handbook of metaheuristics_ , 321–361. Springer. 

Wang, H.; Skreta, M.; Ser, C.-T.; Gao, W.; Kong, L.; Streith-Kalthoff, F.; Duan, C.; Zhuang, Y.; Yu, Y.; Zhu, Y.; et al. 2024. Efficient Evolutionary Search over Chemical Space with Large Language Models. _arXiv preprint arXiv:2406.16976_ . 

Xu, L.; Hoos, H.; and Leyton-Brown, K. 2010. Hydra: Automatically configuring algorithms for portfolio-based selection. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 24, 210–216. 

Yao, Y.; Liu, F.; Cheng, J.; and Zhang, Q. 2024. Evolve Cost-aware Acquisition Functions Using Large Language Models. In _International Conference on Parallel Problem Solving from Nature_ , 374–390. Springer. 

Ye, H.; Wang, J.; Cao, Z.; and Song, G. 2024. ReEvo: Large Language Models as Hyper-Heuristics with Reflective Evolution. _arXiv preprint arXiv:2402.01145_ . 

# **A Algorithm Details** 

In this part, we elaborate on the details of parent selection and population management used in our proposed MEoH, as shown in Algorithm 1 and Algorithm 2, respectively. 

**Calculation of Dominance-dissimilarity Score** The lines 3-16 in Algorithm 1 and the lines 4-17 in Algorithm 2 are almost identical, illustrating the computation of the dominance-dissimilarity score. Specifically, two square matrices, namely the dissimilarity score matrix **_S_** and the dominance mask matrix **_D_** , are initialized to be zeros. Each heuristic within the population is compared in pairs, with their dissimilarity (negative AST similarity) and dominance relationships recorded in the corresponding matrices. Subsequently, these matrices are element-wise multiplied to yield the dominance-dissimilarity score matrix **_S_**<sup>_′_</sup> . The dominance-dissimilarity vector **_v_** is then derived by summing the columns of **_S_**<sup>_′_</sup> . This vector encapsulates a blend of dominance and dissimilarity considerations, guiding the following parent selection and population management. 

**Parent Selection** For parent selection, as delineated in Algorithm 1, the dominance-dissimilarity vector **_v_** is leveraged to construct a probability distribution **_π_** using the softmax function. The parents are subsequently sampled based on this distribution to strike a balance between exploration and exploitation. 

**Population Management** For population management, as shown in Algorithm 2, the dominance-dissimilarity vector **_v_** is descending sorted, and the resulting indices **_k_** are utilized to truncate the population, and the first _N_ individuals consists the new population **_P_**<sup>_′_</sup> . 

Algorithm 1: ParentSelection 

1: **Input:** Population **_P_** ; Population size _N_ ; Parent selection size _d_ . 2: **Output:** Selected parents **_P_** _parent_ . 3: Initialize the dissimilarity score matrix **_S_** as an _N × N_ matrix filled with zeros; 4: Initialize the dominance mask matrix **_D_** as an _N × N_ matrix filled with zeros; 5: **for** _i_ = 1 _, . . . , N_ **do** 6: **for** _j_ = 1 _, . . . , N_ **do** 7: **if** _i̸_ = _j_ **then** 8: **_S_** [ _i, j_ ] _←−_ AST( **_P_** [ _i_ ] _,_ **_P_** [ _j_ ]); 9: **if** **_P_** [ _i_ ] _≺_ **_P_** [ _j_ ] **then** 10: **_D_** [ _i, j_ ] _←_ 1; 11: **end if** 12: **end if** 13: **end for** 14: **end for** 15: **_S_**<sup>_′_</sup> _←_ **_S_** _⊙_ **_D_** 16: **_v_** _←_ ColumnwiseSum( **_S_**<sup>_′_</sup> ) 17: **_π_** _←_ Softmax( **_v_** ) 18: **_P_** _parent ←_ Sample( **_P_** _,_ **_π_** _, d_ ) 

Algorithm 2: PopulationManagement 

1: **Input:** Population **_P_** ; Population size _N_ . 2: **Output:** New population **_P_**<sup>_′_</sup> . 3: Current population size _N_<sup>_′_</sup> _←_ size( **_P_** ) 4: Initialize the dissimilarity score matrix **_S_** as an _N_<sup>_′_</sup> _× N_<sup>_′_</sup> matrix filled with zeros; 5: Initialize the dominance mask matrix **_D_** as an _N_<sup>_′_</sup> _× N_<sup>_′_</sup> matrix filled with zeros; 6: **for** _i_ = 1 _, . . . , N_ **do** 7: **for** _j_ = 1 _, . . . , N_ **do** 8: **if** _i̸_ = _j_ **then** 9: **_S_** [ _i, j_ ] _←−_ AST( **_P_** [ _i_ ] _,_ **_P_** [ _j_ ]); 10: **if** **_P_** [ _i_ ] _≺_ **_P_** [ _j_ ] **then** 11: **_D_** [ _i, j_ ] _←_ 1; 12: **end if** 13: **end if** 14: **end for** 15: **end for** 16: **_S_**<sup>_′_</sup> _←_ **_S_** _⊙_ **_D_** 17: **_v_** _←_ ColumnwiseSum( **_S_**<sup>_′_</sup> ) 18: **_k_** _←_ DescendingSortedIndexes( **_v_** ) 19: Initialize a new population **_P_**<sup>_′_</sup> _←∅_ 20: **for** _i_ = 1 _, . . . , N_ **do** 21: **_P_**<sup>_′_</sup> _←_ **_P_**<sup>_′_</sup> _∪_ **_P_** [ **_k_** [ _i_ ]] 22: **end for** 

# **B Heuristic Design Task Details** 

We demonstrate the proposed method on two heuristic design tasks: 1) heuristics design for online Bin Packing Problem (BPP) and 2) heuristic design for guided local search for Traveling Salesman Problem (TSP). We introduce the detailed heuristic design settings for each task. 

## **B.1 BPP** 

In online Bin Packing Problem (BPP) (Seiden 2002), a set of items, each with its own weight, needs to be packed into bins with a predetermined capacity. The objective of the BPP is to minimize the total number of bins required to accommodate all the items. In an online scenario, items are packed as they are received without prior knowledge. 

The heuristic operates by loading items sequentially in an online fashion, requiring only the selection of the best bin at each iteration. This designed function scores bins based on their remaining capacities and the size of the arriving item, with the highest scoring bin chosen for each iteration. The function takes two inputs - the size of the arriving item and the remaining capacities of the bins - and outputs a vector that ranks the bins accordingly. A task description used in the prompt and the Python code snippet template are illustrated as follows: 

**~~'~~ Task Description:** Implement a function that returns the priority with which we want to add an item to each bin. **$ Template Program: import numpy as np def** priority(item: float, bins: np.ndarray) -> np.ndarray: _"""Returns priority with which we want to add item to each bin. Args: item: Size of item to be added to the bin. bins: Array of capacities for each bin. Return: Array of same size as bins with priority score of each bin. """_ **return** item - bins **~~&~~ %** 

Figure 1: BPP heuristic design description and template program. 

## **B.2 TSP** 

For TSP, one of the widely used metaheuristics, Guided Local Search (GLS), is used (Voudouris, Tsang, and Alsheddy 2010). The pipeline of GLS is as follows: 

**Step 1:** Create an initial solution using nearest neighbor constructive heuristics. 

**Step 2:** Local Search Stage: Perform a local search (swap and relocate) to improve the current solution and generate a local optimal solution. 

**Step 3:** Perturbation Stage: Update the distance matrix. Perform another local search based on the updated distance matrix to perturb the local optimal solution to escape from local optimality. 

**Steps 2** and **3** are iteratively repeated until the stopping criterion (maximum number of iterations set to 1 _,_ 000 in the experiments) is satisfied. The best solution obtained throughout the iterations is considered the final solution. 

Our goal is to develop a heuristic to update the distance matrix in the perturbation step. The task description provided in the prompt and the template of the Python code snippet is outlined below. The inputs include the original distance matrix, the local optimal solution, and the frequency of edge usage in perturbation. The output should be the updated distance matrix. 

**~~'~~ Task Description:** Given an edge distance matrix and a local optimal route, please help me design a strategy to update the distance matrix to avoid being trapped in the local optimum with the final goal of finding a tour with minimized distance. You should create a heuristic for me to update the edge distance matrix. 

**Template Program: import numpy as np def** update_edge_distance(edge_distance: np.ndarray, local_opt_tour: _�→_ np.ndarray, edge_n_used: np.ndarray) -> np.ndarray: _""" Design a novel algorithm to update the distance matrix. Args: edge_distance: A matrix of the distance. local_opt_tour: An array of the local optimal tour of IDs. edge_n_used: A matrix of the number of each edge used during �→ permutation. Return: updated_edge_distance: A matrix of the updated distance. """_ updated_edge_distance = np.copy(edge_distance) _# Calculate combined importance and frequency factor_ updated_edge_distance = edge_distance **return** updated_edge_distance **~~&~~** 

**$** 

**%** 

Figure 2: TSP heuristic design task description and template program. 

# **C Baseline Settings** 

In this work, we employ FunSearch (Romera-Paredes et al. 2024) and EoH (Liu et al. 2024a) as baseline. For EoH, we inherit the default settings, including the number of iterations _T_ = 20, the parent selection size _d_ = 5, and the population size _N_ = 10 for the TSP and _N_ = 20 for the BPP. Our MEoH also follows these settings. In summary, 1 _,_ 000 heuristics are generated for solving TSP, and 2 _,_ 000 heuristics for BPP. For FunSearch, we also adopt the default settings, the number of islands is 10 and the number of samples for each prompt is 4. FunSearch generates 10 _,_ 000 heuristics for solving BPP and TSP. 

# **D Metric Definition** 

## **D.1 HV** 

Hypervolume (HV) is calculated as follows: 



where _P_ represents the approximate Pareto front obtained by an automated heuristic design approach, **_v_** = ( _v_ 1 _, . . . , vm_ )<sup>⊺</sup> denotes the corresponding objective vector, VOL( _·_ ) represents the Lebesgue measure, and **_r_**<sup>_∗_</sup> = ( _r_ 1<sup>_∗, . . . , r_</sup> _m_<sup>_∗_)⊺is a reference</sup> objective vector. 

To account for variations in HV values across different objective domains, i.e., the scalar of intrinsic objective value and the running time, we normalized each objective value for each instance. Specifically, the generated heuristic **_x_** can be normalized in the objective space using the approximated ideal point **_z_**<sup>ideal</sup> = ( _z_ 1<sup>ideal</sup> _, . . . , zM_<sup>ideal)⊺and the approximated nadir point</sup><sup>**_z_**nadir=</sup> ( _z_ 1<sup>nadir</sup> _, . . . , zM_<sup>nadir)⊺derived from the union of all approximated Pareto-front</sup><sup>_P_as</sup> 



where _zi_<sup>ideal</sup> = min _{vi|_ **_v_** _∈P}_ and _zi_<sup>nadir</sup> = max _{vi|_ **_v_** _∈P}_ , _∀i ∈{_ 1 _, . . . , M }_ . Consequently, the value of each objective is normalized to [0 _,_ 1]. Based on that, the reference point **_r_**<sup>_∗_</sup> = (1 _._ 1 _, . . . ,_ 1 _._ 1)<sup>⊺</sup> . 

## **D.2 IGD** 

Inverted Generational Distance (IGD) measures the convergence and diversity of the obtained Pareto front approximation concerning the true Pareto front. It is calculated as follows: 



where _P_ is the set of decision vectors, i.e, the approximated Pareto front. _P_<sup>_∗_</sup> is the true Pareto front, _|P_<sup>_∗_</sup> _|_ is the number of points in the true Pareto front _d_ ( _p, q_ ) is the Euclidean distance between the points _p_ and _q_ in the objective space. 

The IGD calculates the average distance from the true Pareto front points to their nearest neighbor in the approximated Pareto front. A lower IGD value indicates a better approximation of the true Pareto front. 

It’s important to note that the true Pareto front is required for calculating the IGD metric, which may not always be available in many cases. So, a reference set of well-distributed Pareto-optimal heuristics is often used as an approximation of the true Pareto front, here the reference set is the nondominated set derived from the union of all generated heuristics. 

# **E TSPLIB Results** 

Table 5: Results of small and large TSPLIB instances. 

|TSPLIB|FunS|earch|E|oH|ME|oH|
|---|---|---|---|---|---|---|
||Gap|Time/s|Gap|Time/s|Gap|Time/s|
|berlin52|0.000%<br>|0.484|0.000%|8.500|0.000%|0.344|
|ch130|0.156%|2.031|0.233%|42.360|0.233%|1.016|
|ch150|0.306%|2.500|0.502%|56.062|0.000%|1.250|
|eil101<br>|0.000%|28.391<br>|0.373%|56.031|0.000%|22.297|
|eil51|0.000%|0.515|0.000%|7.109|0.000%|0.312|
|eil76|0.183%|0.938|0.107%|14.844|0.000%|0.531|
|kroA100|0.000%|1.407|0.000%|24.437|0.000%|0.734|
|kroC100<br>|0.000%|1.500<br>|0.000%|24.781<br>|0.000%|0.703|
|kroD100|0.000%|1.578|0.000%|24.563|0.000%|0.734|
|lin105|0.000%|1.812|0.000%|26.703|0.000%|0.890|
|pr76|0.000%|0.969|0.000%|14.469|0.000%|0.546|
|rd100|0.000%|1.453|0.000%|24.266|0.000%|0.750|
|st70|0.000%|0.859|0.000%|12.797|0.000%|0.500|
|Avg.|0.050%|3.418|0.093%|25.917|0.018%|2.354|
|a280|0.195%|378.656|0.059%|640.453|1.245%|356.468|
|pcb442|1.389%|932.093|1.714%|1694.547|1.284%|916.219|
|pr1002|2.878%|354.813|2.487%|3592.891|3.272%|142.000|
|tsp225|1.679%|12.891|1.243%|136.078|0.197%|8.328|
|Avg.|1.535%|419.613|1.376%|1515.992|1.50%|355.754|



# **F Visualization of Dominance-dissimilarity Scores** 

We visualize the evolution of Dominance-dissimilarity Scores in Figure 3. The x-axis is the heuristic index, and the y-axis is the iteration index. It is important to note that the presence of blank blocks in the early iterations indicates cases where the population is not filled, due to the generation of illegal code segments by LLM. As shown in Figure 3, MEoH heuristics can maintain diversity during the evolutionary process, while the diversity of EoH drastically deteriorates. 



<!-- Start of picture text -->
0.0 0.0 0.0 0.0 -1.4 0 0.0 0.0 0.0-0.4-0.4-0.4-1.1-1.2-1.6-1.9-2.3-2.4-2.9-3.0-3.2-3.6-3.7-4.3-4.5-6.2 0<br>0.0 0.0 0.0 0.0-0.5-0.9-1.0-1.5-1.7-3.6-3.8-4.0-4.1-4.2-4.3-4.9-6.2-6.9-7.5-9.2<br>0.0 0.0 -0.6-0.7-1.1-1.5-1.5-1.5-1.6-2.8<br>0.0 0.0 0.0 0.0-0.5-0.5-0.6-0.7-0.9-1.1-1.2-1.4-1.6-2.9-3.4-3.7-4.3-6.8-7.8-7.8<br>0.0 0.0 0.0 -0.6-0.7-1.4-1.5-1.5-1.5-2.1-2.1-3.0-3.1-3.3-4.1<br>0.0 0.0 0.0 0.0-0.6-1.2-1.3-1.8-2.0-2.0-2.3-2.5-3.1-3.3-4.2-4.4-5.2-6.3-6.4-6.6<br>0.0 0.0 0.0 -0.6-0.7-0.7-1.5-1.5-1.5-1.7-2.0-2.1-2.5-2.6-2.7-2.8-3.1-3.2-3.2-3.5 0.0 0.0 0.0-0.7-0.7-0.8-0.8-1.8-1.8-1.9-1.9-2.7-3.1-3.1-3.3-6.4-6.4-8.4-9.1-9.9<br>0.0 0.0 0.0 -0.6-0.7-0.7-1.4-1.5-1.5-1.5-1.7-2.0-2.1-2.2-2.2-2.4-2.5-3.2-3.4-3.4 0.0 0.0 0.0-0.5-0.6-0.6-0.6-0.8-0.8-1.1-1.3-1.4-2.5-2.5-4.1-5.0-5.8-6.5-6.6-8.4<br>0.0 0.0 0.0 -0.6-0.7-0.7-1.4-1.5-1.5-1.5-1.7-2.0-2.1-2.2-2.2-2.4-2.5-3.2-3.4-3.4 0.0 0.0 0.0 0.0 0.0-0.6-0.6-1.2-1.3-1.3-1.3-1.5-1.8-2.6-3.2-5.0-6.1-6.4-8.4-8.6<br>0.0 0.0 0.0 -0.5-0.5-0.6-0.7-0.7-1.5-1.5-1.5-1.7-2.0-2.1-2.7-2.8-2.8-2.8-2.9-3.1 0.0 0.0 0.0 0.0 0.0 0.0-0.5-0.6-1.2-1.3-1.9-2.3-2.3-2.5-3.1-3.2-3.8-4.6-8.4-9.1<br>0.0 0.0 0.0 -0.5-0.6-0.6-0.7-0.8-1.2-1.3-1.6-2.5-2.5-2.5-2.6-3.0-3.0-3.1-3.2-3.8 0.0 0.0 0.0 0.0 0.0 0.0 0.0-0.5-0.5-0.6-1.2-1.3-1.5-1.8-2.3-2.5-2.8-3.7-4.5-5.2<br>0.0 0.0 0.0 0.0 0.0 -0.5-0.6-0.6-0.7-0.7-0.8-1.6-1.9-2.0-2.5-2.5-2.6-2.6-2.8-3.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0-0.5-0.5-0.5-0.7-0.9-1.8-2.3-2.5-3.3-3.3-5.1-5.3<br>0.0 0.0 0.0 0.0 0.0 0.0 -0.6-0.6-0.7-0.8-1.0-1.2-1.4-1.6-1.7-2.0-2.5-2.5-2.6-2.8 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0-0.4-0.5-0.5-0.5-0.7-0.9-1.4-1.8-3.3-3.4-4.3-5.3 5<br>0.0 0.0 0.0 0.0 0.0 0.0 -0.5-0.6-0.6-0.7-0.8-1.0-1.1-1.2-1.4-1.6-1.7-2.0-2.5-2.5 2 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0-0.4-0.5-0.5-0.5-0.6-0.7-3.4-3.9-5.0-5.2-6.5<br>0.0 0.0 0.0 0.0 0.0 0.0 -0.3-0.3-0.5-0.6-0.7-0.8-1.0-1.0-1.2-1.3-1.6-1.7-2.0-2.0 0.0 0.0 0.0 0.0 0.0 0.0-0.4-0.5-0.7-1.2-1.2-1.2-1.3-1.5-1.5-1.7-3.8-7.6-8.4-8.8<br>0.0 0.0 0.0 0.0 0.0 0.0 -0.3-0.3-0.3-0.6-0.7-0.8-0.9-1.0-1.0-1.2-1.3-1.4-1.6-1.7 0.0 0.0 0.0 0.0 0.0-0.4-0.5-0.5-0.7-0.9-0.9-1.1-1.8-2.5-3.4-4.2-5.8-7.8-7.8-10.5<br>0.0 0.0 0.0 0.0 0.0 0.0 -0.3-0.5-0.6-0.7-0.8-0.9-1.0-1.0-1.0-1.0-1.1-1.2-1.5-1.6 0.0 0.0 0.0 0.0-0.4-0.5-0.5-0.5-0.6-0.7-1.2-1.5-2.5-3.5-3.6-3.8-4.3-6.8-7.7-9.5<br>0.0 0.0 0.0 0.0 0.0 0.0 -0.4-0.4-0.5-0.5-0.6-0.6-0.7-0.7-0.8-1.0-1.0-1.1-1.3-1.4 0.0 0.0 0.0 0.0-0.4-0.4-0.5-0.5-0.7-1.1-1.1-1.2-1.9-2.1-3.0-3.6-3.8-5.8-7.2-8.1<br>0.0 0.0 0.0 0.0 0.0 0.0 -0.4-0.4-0.5-0.5-0.6-0.6-0.7-1.0-1.0-1.0-1.0-1.1-1.3-1.4 0.0 0.0 0.0-0.4-0.5-0.5-0.5-0.7-1.1-1.6-1.9-2.6-2.7-3.0-3.2-4.1-4.5-6.4-7.8-8.2<br>0.0 0.0 0.0 0.0 0.0 0.0 -0.4-0.5-0.5-0.6-0.7-0.8-1.0-1.0-1.0-1.1-1.3-1.4-1.4-1.5 0.0 0.0 0.0 0.0-0.4-0.4-0.5-0.7-1.1-1.1-1.4-1.9-2.5-3.0-3.0-4.1-4.3-4.4-6.2-6.3<br>0.0 0.0 0.0 0.0 0.0 0.0 0.0 -0.4-0.4-0.5-0.5-0.6-0.6-0.7-0.7-0.8-1.0-1.0-1.1-1.3 0.0 0.0 0.0-0.4-0.5-0.6-0.6-0.6-0.7-1.0-1.3-2.8-2.8-3.2-3.3-3.7-3.7-3.8-3.9-6.0<br>0.0 0.0 0.0 0.0 0.0 0.0 0.0 -0.4-0.4-0.5-0.5-0.6-0.6-0.7-0.7-0.8-1.0-1.0-1.1-1.1 0.0 0.0 0.0 0.0 0.0 0.0-0.6-0.6-1.6-2.2-2.3-2.5-2.8-3.9-4.4-4.5-4.5-5.6-6.1-6.3<br>0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 -0.4-0.4-0.5-0.5-0.5-0.6-0.7-0.9-1.0-1.0-1.0 4 0.0 0.0 0.0 0.0 0.0-0.4-0.5-0.5-1.3-1.8-2.2-2.8-3.0-3.3-3.9-4.1-4.4-4.4-4.8-6.6 10<br>0 2 4 6 8 10 12 14 16 18 0 2 4 6 8 10 12 14 16 18<br>Individuals Individuals<br>(a) BPP, MEoH (b) BPP, EoH<br>0.0 0.0 -0.6 -0.6 -2.0 0 0.0 0.0 0.0 0.0 -0.5 -0.6 -1.4 -3.8 -4.3 -5.4 0<br>0.0 0.0 0.0 0.0 0.0 0.0 -0.5 -0.7 -0.7 -1.2<br>0.0 0.0 0.0 -0.7 -0.7 -0.8 -2.3 -2.3 -4.6 -4.9<br>0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 -0.3<br>0.0 0.0 0.0 -0.5 -0.7 -0.7 -0.8 -1.9 -4.1 -5.3<br>0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0<br>0.0 0.0 0.0 0.0 -0.7 -1.3 -2.2 -2.9 -3.6 -3.7<br>0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 -0.8 -0.8 -0.8 -1.6 -2.3 -2.3 -7.1<br>0.00.0 0.00.0 0.00.0 0.00.0 0.00.0 0.00.0 0.00.0 0.00.0 0.00.0 -0.40.0 0.00.0 0.00.0 0.00.0 -0.80.0 -0.8-0.8 -0.8-0.8 -2.3-0.8 -2.5-0.8 -2.6-4.5 -3.0-5.8 2<br>0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 -0.9 -2.2 -2.6 -4.3 -6.9<br>0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 -0.8 -0.8 -1.0 -1.8 -2.4 -4.8 -4.9 -5.7<br>0.00.0 0.00.0 0.00.0 0.00.0 0.00.0 0.00.0 0.00.0 0.00.0 0.00.0 0.00.0 1 0.00.0 -0.80.0 -0.80.0 -0.8-0.8 -0.8-2.8 -1.6-3.9 -2.1-4.1 -2.5-5.4 -3.2-5.6 -3.8-6.4<br>0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 -0.8 -1.6 -1.7 -3.7 -3.9 -5.8 -6.4 4<br>0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 -0.8 -1.0 -1.6 -1.7 -3.4 -3.4 -4.7 -5.4<br>0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 -0.8 -0.9 -1.6 -2.5 -2.5 -6.8 -6.9<br>0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 -0.8 -0.8 -1.6 -1.6 -3.2 -4.1 -6.7<br>0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 -0.8 -0.8 -1.8 -1.8 -2.9 -4.4 -4.4 -4.4<br>0.00.0 0.00.0 0.00.0 0.00.0 0.00.0 0.00.0 0.00.0 0.00.0 0.00.0 0.00.0 0.00.0 0.00.0 0.00.0 -0.80.0 -1.6-0.8 -1.6-0.9 -1.6-2.2 -1.6-2.8 -2.3-3.1 -5.1-3.7 6<br>0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 -0.8 -1.7 -3.5 -4.3 -5.2 -5.3<br>0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 2 0.0 0.0 -0.8 -1.6 -1.6 -1.6 -3.3 -4.2 -4.5 -5.8<br>0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9<br>Individuals Individuals<br>(c) TSP, MEoH (d) TSP, EoH<br>0<br>0<br>2<br>2<br>4<br>4<br>6<br>6<br>8<br>8<br>10<br>10<br>12<br>Iterations 12 Iterations<br>14<br>14<br>16<br>16<br>18<br>18<br>20<br>0<br>0<br>2<br>2<br>4 4<br>6 6<br>8 8<br>10 10<br>Iterations 12 Iterations 12<br>14 14<br>16 16<br>18 18<br><!-- End of picture text -->

Figure 3: Visualization of the evolution of dominance-dissimilarity score. 

# **G Search Operators** 

MEoH inherits 5 search operators from EoH (Liu et al. 2024a). These operators are all implemented based on LLMs. In this part, the corresponding prompts will be elaborated. Generally, the prompt consists of operator-specific guidance, task description, and program template. For brevity, the task description and the program template are denoted as **<u>$Task Description</u>** and **<u>$Program Template</u>** <u>, respectively.</u> 

## **G.1 E1 Operator** 

As shown in Figure 4, the E1 operator is used to explore a new heuristic different from the 5 selected heuristics. For simplicity, the heuristics including corresponding heuristic description and code are omitted. 

**~~<u>'</u>~~** **<u>$Task Description</u>** 

**$** 

I have 5 existing algorithms with their codes as follows: _<_ Algorithm description _>_ : ... _<_ Code _>_ : ... 

Please help me create a new algorithm that has a totally different form from the given ones. 

1. First, describe your new algorithm and main steps in one sentence. The description must be inside within boxed _{}_ . 

2. Next, implement the following Python function: **<u>$Program Template</u>** **~~&~~** Do not give additional explanations. 

**%** 

Figure 4: An example of E1 prompt for TSP 

## **G.2 E2 Operator** 

As shown in Figure 5, the E2 operator is used to generate a new heuristic based on the common idea of the 5 selected heuristics. 

**~~<u>'</u>~~** **<u>$Task Description</u>** 

**$** 

I have 5 existing algorithms with their codes as follows: 

_<_ Algorithm description _>_ : ... 

_<_ Code _>_ : ... 

Please help me create a new algorithm that has a totally different form from the given ones but can be motivated from them. 

1. Firstly, identify the common backbone idea in the provided algorithms. 

2. Secondly, based on the backbone idea describe your new algorithm in one sentence. The description must be inside within boxed _{}_ . 

3. Thirdly, implement the following Python function: **<u>$Program Template</u>** 

**~~&~~** Do not give additional explanations. 

**%** 

Figure 5: An example of E2 prompt for TSP 

## **G.3 M1 Operator** 

As shown in Figure 6, the M1 operator is desired to generate a new heuristic based on a given heuristics to improve the performance. 

### **~~<u>'</u>~~** **<u>$Task Description</u>** 

**$** 

I have one algorithm with its code as follows: _<_ Algorithm description _>_ : ... _<_ Code _>_ : ... 

Please assist me in creating a new algorithm that has a different form but can be a modified version of the algorithm provided. 

1. First, describe your new algorithm and main steps in one sentence. The description must be inside within boxed _{}_ . 2. Next, implement the following Python function: **<u>$Program Template</u>** **~~&~~** Do not give additional explanations. 

**%** 

Figure 6: An example of M1 prompt for TSP 

## **G.4 M2 Operator** 

As shown in Figure 7, the goal of the M2 operator is to modify the parameters of a given heuristic. 

**~~<u>'</u>~~** **<u>$Task Description</u>** 

**$** 

I have one algorithm with its code as follows: _<_ Algorithm description _>_ : ... _<_ Code _>_ : ... 

Please identify the main algorithm parameters and assist me in creating a new algorithm that has a different parameter settings of the score function provided. 

1. First, describe your new algorithm and main steps in one sentence. The description must be inside within boxed _{}_ . 

2. Next, implement the following Python function: **<u>$Program Template</u>** **~~&~~** Do not give additional explanations. 

**%** 

Figure 7: An example of M2 prompt for TSP 

## **G.5 M3 Operator** 

In Figure 8, the M3 operator is used to simplify a given heuristic by eliminating redundant components. In this context, the task description and code requirements are not required. 

- **~~'~~** 1. First, you need to identify the main components in the function below. 2. Next, analyze whether any of these components can be overfit to the in-distribution instances. 3. Then, based on your analysis, simplify the components to enhance the generalization to potential out-ofdistribution instances. 

4. Finally, provide the revised code, keeping the function, inputs, and outputs unchanged. _<_ Code _>_ : ... 

**~~&~~** Do not give additional explanations. 

**$** 

**%** 

Figure 8: An example of M3 prompt for TSP 

# **H Designed Heuristics** 

In this section, we present a variety of representative heuristics designed by LLM-based automated heuristic design frameworks, encompassing FunSearch (Romera-Paredes et al. 2024), EoH (Liu et al. 2024a), and our own MEoH. 

## **H.1 BPP** 

**EoH Heuristics** The heuristic developed by EoH with the best performance in terms of the optimal gap, as shown in Figure 9, utilizes sophisticated mathematical operators such as logarithm, square root, and exponential. The complexity of this scoring function renders it challenging to construct manually due to its intricate nature and reliance on advanced mathematical operations. 

**~~'~~ Algorithm Description:** My new algorithm calculates the score for each bin as the sum of the bin’s current capacity divided by the product of the logarithm of the difference between the bin’s capacity and the item size and the square root of the difference between the bin’s capacity and the item size, raised to the power of the bin’s current capacity, and multiplied by the exponential function raised to the power of the item size multiplied by the difference between the bin’s capacity and the item size. Additionally, the score is multiplied by the reciprocal of the bin’s current capacity to prioritize bins with lower capacities. **import numpy as np def** score(item, bins): scores = (bins / ((np.log(bins - item) * np.sqrt(bins - item)) ** _�→_ bins)) * np.exp(item * (bins - item)) * (1/bins) **return** scores **~~&~~** 

**$** 

**%** 

Figure 9: The EoH heuristic with the best optimal gap on BPP. 

**FunSearch Heuristics** The heuristic devised by FunSearch, illustrated in Figure 10, it incorporates numerous sophisticated parameters and introduces a random noise. Unlike the EoH approach, the FunSearch heuristic relies on intricate parameter settings and stochastic perturbations for optimization. 

**~~'~~ def** priority(item: float, bins: np.ndarray) -> np.ndarray: eps = 1e-7 _# Calculate scores based on available space and current capacity_ scores = (bins - item) / (bins + eps) _# Adjust the penalty if necessary_ penalty = np.power(np.min(bins), 0.5) * np.arange(len(bins)) * 0.01 scores -= penalty _# Scale the scores and add a weight_ weight = 0.8 scores = (scores - np.min(scores)) / (np.max(scores) - np.min(scores)) _�→_ *<sup>(1-weight)+weight</sup> _# Favor bins where the item fits perfectly_ scores += 0.5 * (bins == item) _# Favor bins with relatively higher remaining capacity_ scores += 0.02 * (bins - item) / np.max(bins) _# Normalize the priority values_ priority = scores / np.sum(scores) _# Add a small randomness to the priorities for exploration_ priority += np.random.uniform(0, 1e-5, bins.shape) _# Handle the case where the sum of priorities is not equal to 1_ **if** np.abs(np.sum(priority) - 1) > 1e-6: remaining_capacity = bins - np.sum(priority * bins) priority += remaining_capacity / (np.sum(remaining_capacity) * _�→_ len(bins)) 

**$** 

**return** priority 

**~~&~~** 

**%** 

Figure 10: The FunSearch heuristic with the best optimal gap on BPP. 



Figure 11: An illustration of MEoH heuristics on BPP. 

**MEoH Heuristics** In this section, Figure 11 showcases the heuristics developed by MEoH, featuring heuristic descriptions, corresponding code segments, and images in the objective space. Specifically, these heuristics are designed to assign scores to bins based on the arriving items, subsequently arranging the items in bins with the highest scores. 

Among these heuristics highlighted in Figure 11, three exhibit superior performance in terms of the optimal gap, leveraging advanced mathematical operators like absolute value and square root. Furthermore, in the case of the fast heuristic, the score is consistently set to a fixed value of 1, which deviates from the intended description. 

Given the integration of these heuristics into a greedy algorithm, the running time demonstrates low variance. Nevertheless, these MEoH-generated heuristics effectively balance the optimal gap and running time, enabling adaptability to diverse scenarios. 

**H.2 TSP** 

**EoH Heuristics** The heuristic crafted by EoH, as illustrated in Figure 12, intricately incorporates advanced mathematical functions such as tanh alongside sophisticated parameters. It is noteworthy that this complex operation is executed within two nested for-loops, resulting in a computational complexity of _O_ ( _n_<sup>2</sup> ). 

**~~'~~ Algorithm Description:** Update the edge distances in the edge distance matrix by applying a genetic algorithminspired method, where the update is determined by a combination of edge count, distance, usage, and a customized genetic function to promote global exploration and improved convergence. 

**$** 

### **import numpy as np** 

**def** update_edge_distance(edge_distance, local_opt_tour, edge_n_used): updated_edge_distance = np.copy(edge_distance) edge_count = np.zeros_like(edge_distance) **for** i **in** range(len(local_opt_tour) - 1): start = local_opt_tour[i] end = local_opt_tour[i + 1] edge_count[start][end] += 1 edge_count[end][start] += 1 

edge_n_used_max = np.max(edge_n_used) mean_edge_distance = np.mean(edge_distance) **for** i **in** range(edge_distance.shape[0]): **for** j **in** range(edge_distance.shape[1]): **if** edge_count[i][j] > 0: score_factor = (np.tanh(edge_count[i][j]) / _�→_ edge_count[i][j]) + (edge_distance[i][j] / _�→_ mean_edge_distance) - (0.6 / edge_n_used_max) * _�→_ edge_n_used[i][j] updated_edge_distance[i][j] += score_factor * (1 + _�→_ edge_count[i][j]) 

**return** updated_edge_distance **~~&~~** 

**%** 

Figure 12: The EoH heuristic with the best optimal gap on TSP. 

**FunSearch Heuristics** The heuristic formulated by FunSearch, as depicted in Figure 13, incorporates a logarithm operation base 2, Gaussian-distributed noise sampling, and intricate parameter configurations. It is worth noting that this heuristic only includes a single for-loop, indicating a computational efficiency that surpasses the aforementioned EoH heuristic. 



Figure 14: An illustration of MEoH heuristics on TSP. 



<!-- Start of picture text -->
' def update_edge_distance(edge_distance: np.ndarray, local_opt_tour: $<br>�→ np.ndarray, edge_n_used: np.ndarray) -> np.ndarray:<br>num_nodes = edge_distance.shape[0]<br>updated_edge_distance = np.copy(edge_distance)<br>decay_factor = 0.99<br>for i in range(num_nodes - 1):<br>node_i, node_j = local_opt_tour[i], local_opt_tour[i + 1]<br>edge_score = edge_distance[node_i, node_j] * np.log2((num_nodes -<br>�→ edge_n_used[node_i, node_j]) + 1)<br>edge_score *= decay_factor ** edge_n_used[node_i, node_j] #<br>�→ Multiply by decay factor<br>edge_score += np.random.normal(0, 0.1) # Add small noise<br>updated_edge_distance[node_i, node_j] = edge_score<br>updated_edge_distance[node_j, node_i] = edge_score<br>return updated_edge_distance<br>& %<br><!-- End of picture text -->

Figure 13: The FunSearch heuristic with the best optimal gap on TSP. 

**MEoH Heuristics** In this section, the heuristics designed by MEoH are shown in Figure 14, showcasing 5 representative heuristic descriptions along with corresponding code segments, and visual representations of all the heuristics in the objective space. 

In this work, GLS is employed to solve TSP, and the heuristics are designed to update the edge distance to facilitate the perturbation in each iteration. 

As shown in Figure 14, the designed heuristics leverage advanced mathematical operators including logarithm, square root, and exponential functions. Furthermore, for the fast heuristic, the edge distances remain unchanged, deviating from the original description due to the complexity of implementing Q-Learning. 

These heuristics underscore the capability of our MEoH to strike a balance between the optimal gap and running time, allowing for effective adaptation to various scenarios. 

# **I MEoH on 3-objective tasks** 

In this section, MEoH is utilized to develop heuristics while taking into account 3 objectives. In addition to performance and efficiency, we also consider code readability, which is crucial for user comprehension and maintenance of the programming code (Buse et al., 2009). The readability is assessed using the Halstead difficulty metric (Curtis et al., 1979). As illustrated in Figure 15 and 16, MEoH continues to perform well, particularly in the TSP task. Despite the promising outcomes achieved with three objectives, future research will be essential to address the challenges associated with handling more objectives. 



<!-- Start of picture text -->
HV IGD<br>0.6 MEoH<br>2<br>EoH<br>0.4<br>0.2 MEoH 1<br>EoH<br>0.0<br>5 10 15 20 5 10 15 20<br>Iterations Iterations<br>(a) HV (b) IGD<br><!-- End of picture text -->

Figure 15: Comparations of EoH and MEoH on BPP5k. 



<!-- Start of picture text -->
HV IGD<br>10<br>1.0<br>MEoH<br>5<br>0.5 EoH<br>MEoH<br>EoH<br>0.0 0<br>5 10 15 20 5 10 15 20<br>Iterations Iterations<br>(a) HV (b) IGD<br><!-- End of picture text -->

Figure 16: Comparations of EoH and MEoH on TSP100. 

