# **Enhancing CVRP Solver through LLM-driven Automatic Heuristic Design** 

**Zhuoliang Xie**<sup>**1**</sup> **Fei Liu**<sup>**2**</sup> **Zhenkun Wang**<sup>**1 ***</sup> **Qingfu Zhang**<sup>**2**</sup> 1 Southern University of Science and Technology 2 City University of Hong Kong 

`xiezl2025@mail.sustech.edu.cn` , `fliu36-c@my.cityu.edu.hk` , `wangzhenkun90@gmail.com` , `qingfu.zhang@cityu.edu.hk` 

## **Abstract** 

The Capacitated Vehicle Routing Problem (CVRP), a fundamental combinatorial optimization challenge, focuses on optimizing fleet operations under vehicle capacity constraints. While extensively studied in operational research, the NP-hard nature of CVRP continues to pose significant computational challenges, particularly for large-scale instances. This study presents AILS-AHD (Adaptive Iterated Local Search with Automatic Heuristic Design), a novel approach that leverages Large Language Models (LLMs) to revolutionize CVRP solving. Our methodology integrates an evolutionary search framework with LLMs to dynamically generate and optimize ruin heuristics within the AILS method. Additionally, we introduce an LLM-based acceleration mechanism to enhance computational efficiency. Comprehensive experimental evaluations against state-of-the-art solvers, including AILS-II and HGS, demonstrate the superior performance of AILS-AHD across both moderate and large-scale instances. Notably, our approach establishes new best-known solutions for 8 out of 10 instances in the CVRPLib large-scale benchmark, underscoring the potential of LLM-driven heuristic design in advancing the field of vehicle routing optimization. 

## **1 Introduction** 

The Capacitated Vehicle Routing Problem (CVRP) is a critical combinatorial optimization problem that involves managing a fleet of vehicles, each with a specified capacity, to service a set of customers with varying demands. CVRP is of significant practical importance, with applications spanning logistics, production, and transportation [1]. The complexity of real-world CVRP scenarios has escalated with the expanding scale of modern businesses and supply systems, presenting substantial challenges for existing CVRP solvers. 

Current CVRP solvers fall into three categories: exact methods, deep learning-based neural solvers, and meta-heuristics. Exact methods require extensive computational resources, rendering them impractical for large-scale instances [2, 3]. Neural solvers, while innovative, often encounter challenges related to solution quality and exhibit limitations when confronted with out-of-distribution scenarios. Meta-heuristics, on the other hand, provide satisfactory solutions within a reasonable time and are thus widely adopted in both academic research and industry applications. Notable among these is the Hybrid Genetic Search (HGS) [4], which leverages a population of solutions and a robust local search strategy. Other significant methods include Slack Induction by String Removals (SISR) [5] which uses ruin-and-recreate mechanisms, and Adaptive Iterated Local Search with Path-Relinking (AILS-PR) [6] which incorporates techniques like path-relinking and localized optimizations in each iteration. Despite their effectiveness, developing these meta-heuristic approaches often requires extensive expert knowledge and a labor-intensive trial-and-error process. 



<!-- Start of picture text -->
Heuristic Population </> </> </> …<br>Prompt </></></> Evaluation Score<br>i) Initialization ii) Iterated Local Search iii) Updating<br>Task: Design and code  Perturbation Local Search<br>a heuristic to select<br>nodes to be removed ... Inter-Route: AcceptedSolution<br>• Shift<br>{Selected Parent(s)}{Selected Operator} Ruin •• Swap*2-opt* AcceptanceSolution<br>{Output Format} Intra-Route:<br>{Code Template} • Shift 𝝎𝒌, 𝒅𝒓<br>• Swap<br>{Other Info. } • 2-opt Parameter<br>Recreate Updating<br>Depot Node Selected Node LLM </> Heuristic<br><!-- End of picture text -->

Figure 1: The AILS-AHD pipeline: (1) LLM-driven evolutionary computation generates ruin heuristics; (2) each candidate heuristic is evaluated via AILS, including initialization, iterated local search and updating; (3) the population is updated based on fitness of the heuristic. 

Recent advancements have seen Large Language Models (LLMs) being applied in fields such as code generation, mathematical reasoning, and combinatorial optimization [7, 8]. However, the integration of LLMs for enhancing CVRP solvers has yet to reach its full potential. Although recent efforts employ LLMs to enhance the automation of developing routing solvers [9], the quality of current solutions remains significantly below the requirements for practical deployment. 

In this paper, we present AILS-AHD, an effective adaptive iterated local search framework that combines automatic heuristic design powered by LLMs with an Evolutionary Computation (EC) framework. Through careful analysis of problem characteristics and the AILS framework, we identify and enhance the crucial ruin heuristic in AILS. Our comprehensive experimental evaluation on two standard benchmarks demonstrates the framework’s strong performance, achieving 8 new best-known solutions for large-scale CVRPLib instances [10] and one new best-known solution for moderate-scale instances [11], representing significant improvements over existing approaches. 

Our contributions are summarized as follows: 

- We present AILS-AHD (Adaptive Iterated Local Search with Automated Heuristic Design), an efficient framework that enhances its core ruin method through LLM-driven automatic heuristic design integrated with an evolutionary computation paradigm. 

- We further develop an LLM-based acceleration mechanism incorporating Chain-of-Thought (CoT) technique to efficiently address the computational demands during the evaluation on automated heuristic design. 

- We conduct a comprehensive evaluation against two leading algorithms HGS and AILS-II, showcasing superior solution quality and efficiency across both moderate-scale and largescale CVRPLib instances. We achieve 8 out of 10 new best-known solutions on large-scale CVRPLib instances and one new best-known solution on moderate-scale instances. 

## **2 Problem Description** 

The Capacitated Vehicle Routing Problem (CVRP) involves determining optimal routes that originate from a depot, visiting each vertex exactly once, and returning to the depot. Each vertex has a demand that must be served by a vehicle and can only be visited once. The total demand of a route cannot exceed the capacity of its assigned vehicle. 

The CVRP can be defined on a complete graph _G_ = ( _V, E_ ), where _V_ = _{_ 0 _,_ 1 _, . . . , n}_ represents the vertices (nodes), with _n ≥_ 1. The vertex 0 denotes the depot, and _Vc_ = _{_ 1 _, . . . , n}_ represents 

2 

the customer set. The demands at these vertices are given by _Q_ = _{q_ 0 _, q_ 1 _, . . . , qn}_ , and the edges _E_ = _{_ ( _i, j_ ) _|i, j ∈V, i̸_ = _j}_ connect all distinct pairs of vertices. The vehicles used are indexed by _M_ = _{m_ 1 _, . . . , ml}_ with _l >_ 1, each having the same capacity _c_ . 

The CVRP is NP-hard. Exact methods, such as branch-and-bound [12], quickly become computationally infeasible for large-scale problems. While heuristic algorithms offer a trade-off between computational efficiency and solution quality, they often struggle to maintain this balance as the problem size and complexity increase. The growing scale of real-world applications, characterized by large customer sets and diverse vehicle types, further exacerbates these challenges. 

## **3 AILS-AHD** 

### **3.1 AILS** 

The backbone Adaptive Iterated Local Search (AILS) consists of three parts: i) Initialization, ii) Iterated local search, and iii) Updating. 

**Initialization** In initialization, we generate an initial solution using the greedy insertion method followed by a local search to improve its quality. In the greedy insertion, we first randomly select _n_<sup>_r_</sup> nodes to construct _n_<sup>_r_</sup> routes, where _n_<sup>_r_</sup> is the minimum number of routes required to serve all customers: 



Then, the rest _n − n_<sup>_r_</sup> nodes are iteratively inserted into the _n_<sup>_r_</sup> routes. In each iteration, one node is selected randomly and inserted into the position that satisfies the vehicle capacity constraint while minimizing the total cost increment of the current solution. Each solution is then refined through a local search to improve its quality. 

**Iterated Local Search** We iteratively perform two steps starting from the initial solution to improve the quality. The two steps are (a) perturbation and (b) local search [13]. 

(a) _Perturbation_ : We use ruin-and-recreate [14] for the perturbation step. Ruin involves removing a set number of nodes from the current solution according to specific rules such as random selection and clustering selection. For recreation, the removed nodes are reinserted into the partial solution using the nearest insertion and the best insertion. 

This operator is specifically designed to help the solution escape local optima. To adaptively control the perturbation degree, a parameter _ωk_ is determined as the number of nodes to be removed. It is calculated and updated through Equation 2. 

After perturbation, the solution may violate constraints, such as exceeding the vehicle capacity limit. To address this and improve the solution quality, an improvement step is performed, including feasibility checking and local search. 

(b) _Local Search_ : During the improvement phase, diverse local search operators are applied iteratively to achieve both inter-route and intra-route improvements. Inter-route improvement refers to applying these operators between two different routes, while intra-route improvement applies them within a single route. 

For inter-route improvement, the operators include Shift [15], Swap* [4], and 2-opt* [16]. Similarly, for intra-route improvement, the applied operators are Shift, Swap [17], and 2-opt [18]. These operators are executed iteratively to refine the solution. 

During this process, a value representing the degree of constraint violations in the current solution is calculated. Solutions with fewer violations (i.e., fewer invalid routes) after applying an operator are accepted. This iterative process continues until a feasible solution is achieved. Once feasibility is ensured, a final local search is performed using the same operators for both inter-route and intra-route improvements. This step ensures thorough optimization and further refines the solution. In the local search phase, the solution with the lowest total cost is accepted. 

3 

**Updating** The updating phase consists of two components: parameter updating and solution acceptance, ensuring the algorithm adapts dynamically during the search process. 

(a) _Parameter Updates_ : Two key parameters, the perturbation degree _ωk_ and the reference distance _dr_ , are updated iteratively to guide the search. 

The perturbation degree _ωk_ , which determines the number of nodes removed during perturbation, is adapted based on the reference distance _dr_ and the adaptive distance _dk_ : 



where _n_ is the total number of nodes. 

The reference distance _dr_ is reduced gradually using an exponential decay formula: 



where _d_ min and _d_ max are the minimum and maximum distances manually set, and _it_ is the current iteration number. This ensures _dr_ decreases progressively, focusing the search on promising regions. 

The adaptive distance _dk_ is updated as a weighted average of its previous value and the distance between the current solution _s_ and the best solution _s_<sup>_r_</sup> : 



where _γ_ is a parameter that prevents recent updates from having too little influence. The distance _d_ ( _s, s_<sup>_r_</sup> ) is computed as _|E△E_<sup>_r_</sup> _|_ , which represents the number of different edges between the current solution _s_ and the reference solution _s_<sup>_r_</sup> . 

(b) _Solution Acceptance_ : To decide whether the solution is accepted as the reference solution, a threshold _θ_ is calculated: 



where _<u>f</u>_ and _f_<sup>¯</sup> are the minimum and average objective values observed so far, and _η_ is a dynamic parameter reflecting the quality of solutions. Only solutions with _f_ ( _s_ ) _< θ_ are accepted, allowing the algorithm to balance exploration and exploitation effectively. 

### **3.2 LLM-driven AHD** 

In the AILS framework, we identify and automatically design the perturbation step in iterated local search. Specifically, we design the heuristic for the ruin operator, i.e., the heuristic determines which nodes are removed given a current solution and features in each iteration. 

As illustrated in Figure 1, we adopt an Evolutionary Computation (EC) framework with LLMs for Automatic Heuristic Design (AHD) of the ruin heuristic. The LLM-driven AHD process maintains and evolves a population of heuristics. In each evolution population, four steps are performed: 1) prompt construction, 2) heuristic generation, 3) evaluation, and 4) population update. 

**Prompt Construction** The first step involves constructing a prompt that includes the task description, the required code template format, and other relevant details. The initial parent seed heuristic is manually designed to serve as a starting point. During subsequent iterations, parent heuristics are selected from the population based on a probability distribution defined in Equation 6. Further details about the prompt design, including specific examples and templates, can be found in Appendix. 



**Heuristic Generation** Once the prompt is constructed, it is sent to the LLM to generate offspring heuristics. The LLM employs four distinct operators to create new heuristics, each tailored to introduce specific variations or improvements. A detailed description of these operators, including their implementation and usage, is provided in Appendix. 

4 

**Evaluation** To evaluate the newly generated heuristics, each is integrated into the original evaluation method by replacing the corresponding component. The heuristic is then tested on a carefully selected set of instances, and its fitness is calculated as the average performance across all instances. This rigorous evaluation process ensures that only high-performing heuristics are retained, maintaining the quality and effectiveness of the population. 

**Population Update** After evaluation, the population is updated with the offspring heuristics. To maintain diversity and ensure robust exploration, heuristics with lower fitness are retained in the population. 

### **3.3 Feature Construction for Heuristic Design** 

To efficiently design the ruin heuristic, we construct hybrid features combining problem-specific characteristics and mechanism properties as the heuristic input and output for LLM to design. The key features include: 

- **Distance Matrix** : The Euclidean distance matrix _Dij_ between all node pairs ( _i, j_ ) serves as the spatial foundation, enabling the heuristic to evaluate proximity-based removal priorities. 

- **K-Nearest Neighbor List** : For each node _vi_ , we maintain an ordered list _NK_ ( _i_ ) of its K closest neighbors. 

- **Number of Nodes to Select** : The parameter _ωk_ determines the destruction intensity. Larger values promote exploration by removing more nodes, while smaller values favor exploitation through minor perturbations. 

- **Node Attributes** : Each node _vi_ is characterized by demand _di_ and connectivity with other nodes. For example, nodes with higher demand or critical connectivity roles may be targeted for removal, facilitating more significant improvements during the recreate phase. 

- **Average Nodes per Route** : The metric<sup>_<u>|V</u>_</sup> _R_<sup>_c|_</sup> (where _R_ is the current number of routes) prevents excessive concentration of removals on specific routes. 

- **Random Seed** : A fixed seed _s_ controls all stochastic operations (e.g., node selection probabilities) during evaluation. This reproducibility mechanism enables fair comparison between different heuristic configurations by eliminating evaluation variance. 

**Output Selected Nodes** : The heuristic outputs a set _Vr_ = _{v_ 1 _, ..., vk}_ of nodes selected for removal, where _k_ = _ωk_ . 

### **3.4 Acceleration Mechanism** 

To address the high computational demand in automatic heuristic design, we propose an LLM-driven acceleration method. Specifically, each generated heuristic is incorporated into a carefully crafted prompt that combines the Chain-of-Thought (CoT) technique [19], enabling the LLM to assess the heuristic’s potential value before actual evaluation. Furthermore, we implement an early stopping mechanism that discards heuristics showing poor performance on initial evaluation instances. The detailed prompt design is provided in Appendix. 

## **4 Experiment** 

### **4.1 AILS-AHD** 

**Settings** For the automatic heuristic design phase of the AILS-AHD, we adopt an Evolutionary Computation (EC) framework to maintain the sampled heuristics. The population size is set to 25, and the maximum generation is set to 10 (resulting in 1000 LLM calls). We use 4 EC operators to guide the LLM in heuristic sampling. The detailed operator description is shown in Appendix. For the testing phase, we directly use the top-3 LLM-designed heuristics to integrate into AILS for evaluation. 

We conduct experiments using the pre-trained LLM GPT-4o. The specific prompts employed during the experiments are provided in Appendix. To evaluate the heuristics generated through AHD 

5 



<!-- Start of picture text -->
Description:  The new algorithm performs a strategic removal of nodes by<br>first evaluating each node based on a calculated 'importance score,' which<br>considers distances to its neighboring nodes and a flexibility factor derived<br>from a random variable. Nodes with the highest scores are prioritized for<br>removal, enhancing solution diversification.<br>Code:<br>...<br>Description:  first exploration approach to select nodes from a CVRP graph. The selection process starts with a random node from the current solution, avoiding the depot node. From this starting node, the algorithm explores its K-nearest neighbors, prioritizing the ones belonging to the solution and not already selected. Each neighbor exploration increases the coverage of the solution space while promoting diverse routes. To maintain a balance, the algorithm occasionally resets to a new random starting point within the solution space, ensuring a fresh round of exploration, which could potentially uncover new optimal paths while avoiding local optimum traps. Code:  ... The algorithm opts for a modified breadth- Description: uses an expanding neighborhood strategy with a stochastic bias to select nodes from the CVRP graph. It begins at a randomly selected non-depot node and progressively explores nodes within increasing circular boundaries. The radius of these circles expands with each iteration, thereby increasing the coverage area. Code:  ...  This algorithm<br><!-- End of picture text -->

Figure 2: Convergence curve of LLM designed heuristics. 

based on LLM process, we utilized 10 problem instances. These are carefully selected taking into consideration the instance scales. For each instance, the evaluation is performed under two different random seeds, resulting in a total of 20 independent instance runs for a single evaluation. 

**Convergence Process** As shown in Figure 2, the best heuristic is identified after approximately 350 samples. To illustrate the convergence process, we list three heuristics along the convergence curve as examples, with the best heuristic highlighted in the orange box. 

**Designed Heuristics** Here we list the main idea of the top-3 heuristics. Due to the page limitation, the full code is displayed in Appendix: 

- **Expanding Neighborhood Node Selection (EN)** : This is the best-performing heuristic, which operates by first randomly selecting a seed node and then iteratively selecting the remaining nodes from the neighborhood circle of the seed node. It introduces a new dynamic parameter _λ_ to dynamically expand the neighborhood radius. The radius of the neighborhood gradually increases in steps of _λ_ during the selection process if the number of selected nodes does not meet the total requirement. 

- **Demand-Driven Node Selection with Distance Decay (DDD)** : It selects nodes based on demand, incorporating a decay factor that reduces distance influence over time. It starts from a random seed node and expands a spiral radius, prioritizing high-demand nodes while ensuring spatial coherence. This approach balances demand efficiency with effective node selection. 

- **Probabilistic Node Selection with Frequency Decay (PFD)** : This algorithm selects nodes by initializing a frequency array and iterating until the desired count is reached. It uses a luck threshold to either select nodes sequentially from a random starting point or probabilistically based on proximity and frequency, applying exponential decay to reduce selection likelihood over time. 

### **4.2 Baselines** 

We compare the designed heuristics with two state-of-the-art methods: HGS [4] and AILS-II [20]. HGS is a representative population-based memetic method that combines a genetic algorithm with local search. AILS-II is the advanced version of AILS, representing a recent single-solution-based method that utilizes an iterated local search framework. 

We also compare two hand-crafted variants of AILS-AHD: AILS-C and AILS-S to further demonstrate the superiority of our automatically designed heuristics. AILS-C uses the K-nearest heuristic, while AILS-S uses the sequence-based heuristic. 

6 

### **4.3 Benchmark** 

We use two representative CVRPLib benchmarks: 

- X Set [11]: It is the most commonly used CVRP benchmark, which includes 100 moderatescale instances with node size ranges from 100 to 1,000. 

- AGS Set [10]: It is a representative large-scale CVRP benchmark. It has 10 large-scale instances extracted from the geometrical data of real-world cities, such as Antwerp and Brussels, with sizes ranging from 3,000 to 30,000. It poses a significant challenge for existing CVRP solvers. 

All experiments are conducted on 2 Intel(R) Xeon(R) Gold 6254 CPUs. Each instance is executed for 3 _∗ n_ seconds for complete convergence according to Máximo et al. [20], where _n_ is the number of nodes in the instance. A total of 30 independent runs are performed for each instance. 

### **4.4 Result on Moderate-scale Instances** 

We first evaluate different methods on the moderate-scale instances to test their general performance. 

Table 1: Results achieved on moderate-scale instances. 

|Instance|BKS|HGS|AILS-II|AILS-C|AILS-S|Ours-PFD|Ours-DDD|Ours-EN|
|---|---|---|---|---|---|---|---|---|
|Avg. Gap(%) (+/-/=)|**0.00**|0.109 (40/38/22)|0.0702 (9/1/90)|0.0687 (3/2/95)|0.0804 (30/6/64)|0.0678 (7/3/90)|0.0686 (2/3/95)|0.0672|



As shown in Table 1, BKS represents the Best-Known Solution objectives. Avg. denotes the average objective over 30 runs. The notation “(+/-/=)” indicates the statistical significance of the results when comparing Ours-EN with the compared methods. Specifically, “+” means Ours-EN performs significantly better than the compared method, “-” indicates it performs worse, and “=” signifies no significant difference between the two methods. The results show that Ours-PFD, Ours-DDD, and Ours-EN consistently outperform HGS, AILS-II, AILS-C, and AILS-S in terms of average performance, where AILS-C and AILS-S are methods based on our AILS framework but replace the ruin heuristic with manually designed ones. Notably, Ours-EN achieves the best average gap of 0.0672%, demonstrating its superiority over other methods. Detailed results are provided in Appendix. 



Figure 3: Convergence curve on moderate-scale CVRP instances. 

As illustrated in Figure 3, we also compare the convergence curves across three different instances. The y-axis averaged over 30 independent runs and is shown in log scale. HGS usually demonstrates faster convergence at the beginning with minimal variance. However, it struggles to achieve further improvement beyond that point. In contrast, AILS-II and our designed heuristics show potential for continuous convergence, with the heuristics designed by our method achieving superior results overall. More convergence curves are shown in Appendix. 

### **4.5 Result on Large-scale Instances.** 

We further evaluate the performance of the best-designed heuristic, Ours-EN, against AILS-II on large-scale instances. The experiments are conducted over 10 independent runs to obtain the average performance, as summarized in Table 4a. The results indicate that Ours-EN achieves a lower average 

7 



<!-- Start of picture text -->
Instance BKS AILS-II Ours-EN<br>Antwerp1 477261.00 a 477536.90  ±  4.83e+01(+) 477433.90  ±  6.49e+01<br>Antwerp2 291265.00 a 291657.00  ±  1.13e+02(+) 291430.60  ±  1.29e+02<br>Brussels1 501434.00 a 501839.10  ±  3.33e+01(=) 501786.50  ±  1.02e+02<br>Brussels2 344822.00 a 345341.00  ±  1.02e+02(=) 345321.00  ±  1.41e+02<br>Flanders1 7238697.00 a 7241048.40  ±  8.90e+02(-) 7242256.90  ±  9.31e+02<br>Flanders2 4365762.00 a 4370954.10  ±  1.35e+03(-) 4375279.30  ±  1.87e+03<br>Ghent1 469482.00 a 469752.70  ±  1.13e+02(=) 469665.20  ±  1.21e+02<br>Ghent2 257563.00 257826.40  ±  1.33e+02(=) 257801.40  ±  1.13e+02<br>Leuven1 192848.00 193025.00  ±  4.96e+01(+) 192900.10  ±  5.61e+01<br>Leuven2 111355.00 a 111616.10  ±  9.74e+01(+) 111497.50  ±  1.19e+02<br>Avg. Gap(%) (+/-/=) 0.1061 (4/2/4) 0.0862<br>a Better BKS obtained by Ours-EN. (b) Convergence curve on large-<br>(a) Results achieved on the large-scale instances. scale CVRP instances.<br><!-- End of picture text -->

Figure 4: Result on large-scale CVRP instances. 

gap of 0.0862%. This demonstrates that Ours-EN consistently outperforms AILS-II in terms of average solution quality across the tested instances. 

The average convergence curve is presented in Figure 4b. The results are averaged over 10 large-scale instances across 10 independent runs. The findings indicate that Ours-EN converges at a faster rate in terms of both CPU time and iterations compared with AILS-II. 

We also conduct tests with a runtime of 10 _∗ n_ seconds to search for new best-known solutions for large-scale instances. The best-performing designed heuristic, Ours-EN, is utilized for this evaluation. As a result, we successfully generate **8 new best-known solutions** out of the 10 instances. 

Figure 5a illustrates the convergence curve of Antwerp1. Detailed results and route visualizations of all the new best-known solutions are provided in Appendix. 



<!-- Start of picture text -->
Convergence Curve on Antwerp1 Antwerp1 BKS<br>Depot<br>1.4 Convergence<br>Baseline (gap=0%)<br>1.2<br>1.0<br>0.005<br>0.8<br>0.000<br>0.6<br>0.005<br>0.4 84 86 88<br>0.2<br>0.0<br>Cost: 477277<br>0 20 40 60 80 100<br>CPU Time %<br>(b) New best-known solution found for<br>(a) Convergence curve for Antwerp1. Antwerp1.<br>Log(1+Gap%)<br><!-- End of picture text -->

Figure 5: Convergence curve and new best-known solution found for Antwerp1. 

### **4.6 LLM-Driven Acceleration Framework** 

Our analysis reveals that in automated heuristic design, most LLM-generated heuristics fail to update the population after evaluation, particularly during later search stages (see Figure 2). To address this, we conducted experiments on a fixed population comprising 375 heuristics, with results presented in Table 2. 

|The first T/F indicates whether the heuristic out-<br>performs the worst population member (warrant-|Table 2:|Results|of LL|M-driv|en acc|elerati|on (%|
|---|---|---|---|---|---|---|---|
|ing evaluation), while the second denotes LLM’s<br>judgment. TT and FF represent successful re-||TT|TF|FT|FF|U-R|C-R|
|tention of good heuristics and filtering of poor|Vote-1|49.3|19.7|17.9|11.2|60.5|98.1|
|ones, respectively. Our voting mechanism (Vote-|Vote-3|51.2|17.9|19.7|9.60|**60.8**|98.4|
|n) employs parallel LLM judgments, with U-R|Vote-5|51.2|18.9|20.5|8.80|60.0|**99.4**|



Table 2: Results of LLM-driven acceleration (%). 

8 



<!-- Start of picture text -->
1.40<br>1.20<br>1.00<br>0.80<br>0.60<br>0.40<br>0.20<br>0.00<br>2 10 100 500 1000 1500<br>Objective Gap (%)<br><!-- End of picture text -->

Figure 6: Ablation study on the neighborhood expanding factor. 

measuring acceleration efficiency and C-R showing correct judgment rates. Notably, Vote-3 achieves optimal balance with 60.8% precision. 

We further integrated the Vote-3 acceleration with early stopping mechanisms, demonstrating enhanced efficiency in automated heuristic design (detailed in Appendix). 

### **4.7 Ablation Study** 

We conduct an ablation study on the neighborhood expanding factor _λ_ to analyze its impact on Ours-EN. The factor is set to six different values: 2, 10, 100, 500, 1,000, and 1,500. For each value, we run 10 independent experiments across 10 selected instances. The results are shown in Figure 6. The setting with an expanding factor of 2 (the original setting in the LLM-designed heuristic) achieves the smallest objective gap and demonstrates the most stable performance, as indicated by the narrowest box size in the figure. The settings with expanding factors of 10 and 100 exhibit slightly worse performance. However, as the expanding factor increases to 500 and beyond, the performance shows a significant decline, with both worse median values and larger box sizes. The factor of 1,500 yields the worst results, along with the largest box size. These findings suggest that larger neighborhood expansions may lead to instability and poorer results, highlighting the importance of carefully selecting the expanding factor for optimal performance. 

## **5 Conclusion, Limitation and Future Work** 

This paper presents AILS-AHD, an efficient framework that integrates Large Language Models (LLMs) with Evolutionary Computation (EC) to automate the design of critical components in metaheuristics for the Capacitated Vehicle Routing Problem (CVRP). To address the inherent randomness in heuristic design for complex problems, we introduce a randomness-alleviation mechanism, enhancing the robustness and reproducibility of the framework. By leveraging the generative capabilities of LLMs and the optimization power of EC, AILS-AHD significantly reduces the reliance on manual heuristic design while achieving superior performance. Experimental results demonstrate the effectiveness of the proposed method, with the top three designed heuristics setting new state-of-the-art results on benchmark datasets. Notably, our approach discovers 8 out of 10 new best-known solutions for large-scale instances and one new best-known solution for moderate-scale instances. We also propose a simple yet effective LLM-driven acceleration mechanism to reduce the computation demands. These findings underscore the potential of combining LLMs with EC frameworks to enhance heuristic design in human designed solver. 

**Limitation and Future Work** While AILS-AHD achieves impressive performance on moderate and large scale CVRP instances, it currently relies on a simple AHD framework. In future work, we aim to develop a more efficient AHD framework to further improve the heuristic design efficiency. In addition, we plan to generalize our method to more vehicle routing problem variants. 

9 

## **A Related Work** 

### **A.1 Meta-heuristic for CVRP** 

CVRP is an NP-hard problem that requires an extremely large amount of time and computational resources when solved using exact methods, such as Branch and Bound [12]. While meta-heuristic approaches may not guarantee finding the global optimum, they are capable of producing high-quality approximate solutions within a relatively shorter time and with fewer computational resources. Classic meta-heuristics for solving CVRP can be broadly categorized into two types: single-solution-based methods and population-based methods. 

**Single-solution-based methods** typically maintain only one solution at a time and perform local searches to iteratively improve it. In [21], the authors introduced Iterated Local Search with Set Partitioning (ILS-SP), which hybridizes the ILS meta-heuristic with an exact algorithm based on the set partitioning (SP) formulation. The ILS-SP method operates in two stages: local search and perturbation. The local search phase considers both inter-route and intra-route neighborhood structures. The inter-route neighborhood structure employs shift and swap as local search operators, while the intra-route structure utilizes reinsertion, 2-opt, or-opt, and exchange operators. For solution perturbation, ILS applies successive shift and swap movements along with a Randomized Variable Neighborhood Descent (RVND) strategy. During the search process, the best routes generated by ILS are stored, and the exact algorithm subsequently solves the partitioning problem by selecting the optimal set of non-overlapping routes whose union covers the entire set of vertices. 

In [5], the authors proposed Slack Induction by String Removals (SISRs), which employs the ruinand-recreate (R&R) algorithm with a single ruin method and a single recreate procedure. The ruin method involves removing sequences of adjacent vertices from the same route, while the recreate method reinserts the removed vertices into the lowest-cost positions. Similarly, [22] introduced Adaptive Iterated Local Search with Path-Relinking (AILS-PR). The AILS component consists of local search and perturbation phases. The local search phase also explores inter-route and intra-route neighborhoods, while the perturbation phase employs a simplified version of the R&R algorithm with two ruin heuristics (removal by sequence or proximity) and two recreate heuristics (insertion by cost or proximity). Path-Relinking (PR) is used to construct paths between pairs of solutions to identify higher-quality intermediate solutions. However, in [20], the authors proposed AILS-II, which removes the PR component due to its high computational cost for large-scale CVRP instances. AILS-II retains most of the AILS-PR structure but introduces slight modifications to the local search operators. Notably, AILS-II incorporates the SWAP* operator proposed in [4] for inter-route local search, which improves upon the standard swap operator by identifying more suitable positions for the selected nodes. 

**Population-based methods** maintain a population of solutions throughout the search process. One of the most well-known population-based methods for solving VRP is Hybrid Genetic Search (HGS) [23, 4]. HGS is a memetic algorithm that combines Genetic Algorithms (GA) with local search (referred to as "education" in HGS). The algorithm begins by selecting parent solutions for crossover and mutation based on predefined probabilities to generate offspring. The offspring then undergo a local search process using efficient operators. HGS introduces the SWAP* operator [4], which identifies better positions for two selected nodes compared to the traditional swap operator, thus enhancing solution quality. 

### **A.2 LLM for AHD** 

Automatic Heuristic Design (AHD) is a systematic approach to creating heuristic functions for solving complex optimization problems. By leveraging computational techniques, AHD aims to automate the design process, reducing the need for manual intervention and enabling the discovery of high-performing heuristics. Recent advancements have explored the integration of Large Language Models (LLMs) into AHD, offering new possibilities for generating and refining heuristics in a scalable and adaptive manner. 

Inspired by the process of natural evolution, Evolutionary Computation (EC) serves as a versatile optimization framework [24]. EC revolves around evolving a population of candidate solutions by simulating biological mechanisms such as genetic variation and natural selection. Over successive generations, these solutions are iteratively refined to achieve optimization. The integration of LLMs 

10 

into EC has further enhanced its capabilities, enabling the generation of novel heuristics and the exploration of complex solution spaces. For example, some works propose using LLMs to simulate traditional evolutionary operators like mutation and crossover [25, 26], while others focus on utilizing LLMs to generate additional contextual or auxiliary information that supports the evolutionary process [27]. 

While existing approaches leverage the generative power of LLMs and evolutionary optimization to automate heuristic design—providing scalable and adaptive solutions—our focus is on advancing beyond current limitations. We aim not only to enhance state-of-the-art methods but also to outperform human-crafted algorithms, pushing the boundaries of automated algorithm design. 

11 

## **B AILS-AHD Settings** 

This section presents the detailed prompts used in AILS-AHD in this work. 

### **B.1 Prompts** 

**Prompt for Generate New Heuristics** The prompt for generating new heuristics consists of five key components. Figure 9 illustrates the overall structure of the prompt provided to the LLM for designing an improved heuristic. The prompt is divided into the following parts: • **Task Description** : This section provides the LLM with a detailed explanation of the objective and requirements for the strategy to be designed. 

- **Heuristic Parent** : This section includes the selected parent heuristic from the current population, chosen through a tournament selection process. It provides information about the historical elite features to guide the iteration process. 

- **Operator Selection** : This section specifies an operator to guide the LLM in generating new heuristics. The operator can either encourage diversity or focus on refining existing heuristics. 

- **Output Format** : This section instructs the LLM to output the generated heuristic along with its description and the corresponding code in a predefined format. This ensures the output can be easily parsed and utilized. 

- **Code Template** : This section provides the LLM with a code template for the designed heuristic. The template ensures that the generated code meets the required syntax and can be evaluated successfully. 

**Seed Heuristic** The process of heuristic initialization starts by adopting the ruin heuristics from the original AILS-II algorithm as the seed heuristics, as illustrated in Figure 8. These seed heuristics operate by either disrupting the solution through the selection of K-nearest nodes or by choosing successive nodes relative to a designated seed node. 

#### **EC Operators** 

**O1** : Please help me create a new heuristic that has a totally different form from the given ones. **O2** : Please help me create a new heuristic that has a totally different form from the given ones but can be motivated from them. 

**O3** : Please assist me in creating a new heuristic that has a different form but can be a modified version of the heuristic provided. 

**O4** : Please identify the main heuristic parameters and assist me in creating a new heuristic that has a different parameter settings of the score function provided. 

Figure 7: The prompt operators used in AILS-AHD. 

**Operators** Inspired by EoH [28], we employ four distinct operators to guide the LLM, as depicted in Figure 7: 

- **O1** : This operator prompts the LLM to generate entirely new strategies by introducing diversity based on the features of the parent strategies. It encourages the exploration of novel solutions that significantly differ from existing ones, promoting a broader search of the solution space. 

- **O2** : This operator directs the LLM to refine parent strategies to produce new ones. By leveraging the structure and features of the parent strategies, E2 focuses on creating enhanced versions while preserving some degree of similarity to the original designs. 

- **O3** : This operator instructs the LLM to modify a single selected parent heuristic to produce a new heuristic. The modifications are incremental, targeting specific aspects of the parent heuristic to achieve gradual improvements. 

12 

<mark>1</mark> <mark>`<Seed Heuristic Description>` 2</mark> <mark>`"` 3</mark> <mark>`The algorithm performs a local optimization by randomly selecting a starting node and then iterating through a sequence of its nearest neighboring nodes , optimizing based on their proximity and specific criteria , or alternatively , copying a sequence of nearest nodes directly for further processing.` 4</mark> <mark>`"` 5 6</mark> <mark>`<Code>` 7</mark> <mark>`package Perturbation ;` 8 9</mark> <mark>`import java . util . Random ;` 10</mark> <mark>`import Solution . newNode ;` 11 12</mark> <mark>`public class NodeSelector {` 13 14</mark> <mark>`public static int [] nodes_seq ( float [][] disMatrix , int [][] nodesKnn , int numberSelect , newNode [] solution , float average_nodes , Random rand ){` 15</mark> <mark>`int [] selectedNodes = new int [ numberSelect ];` 16</mark> <mark>`int instanceSize = nodesKnn . length ;` 17 18</mark> <mark>`int contSizeString ;` 19</mark> <mark>`int countCandidates = 0;` 20</mark> <mark>`double sizeString ;` 21</mark> <mark>`newNode initialNode ;` 22</mark> <mark>`newNode node ;` 23</mark> <mark>`double a = rand . nextDouble ();` 24 25</mark> <mark>`if ( a > 0.5){` 26</mark> <mark>`while ( countCandidates <( int ) numberSelect )` 27</mark> <mark>`{` 28</mark> <mark>`sizeString = Math . min ( Math . max (1, instanceSize - 1) ,( int ) numberSelect - countCandidates );` 29 30</mark> <mark>`node = solution [ rand . nextInt (1, instanceSize )];` 31</mark> <mark>`while (! node . nodeBelong )` 32</mark> <mark>`node = solution [ rand . nextInt (1, instanceSize )];` 33</mark> <mark>`initialNode = node ;` 34</mark> <mark>`contSizeString =0;` 35</mark> <mark>`do` 36</mark> <mark>`{` 37</mark> <mark>`contSizeString ++;` 38</mark> <mark>`node = node . next ;` 39</mark> <mark>`if ( node . name ==0)` 40</mark> <mark>`node = node . next ;` 41 42</mark> <mark>`selectedNodes [ countCandidates ++] = node . name ;` 43</mark> <mark>`node . nodeBelong = false ;` 44</mark> <mark>`}` 45</mark> <mark>`while ( initialNode . name != node . name && contSizeString < sizeString );` 46</mark> <mark>`}` 47</mark> <mark>`}` 48</mark> <mark>`else {` 49</mark> <mark>`int randomNode = rand . nextInt (1, instanceSize );` 50</mark> <mark>`System . arraycopy ( nodesKnn [ randomNode ], 0, selectedNodes , 0, numberSelect );` 51</mark> <mark>`}` 52</mark> <mark>`return selectedNodes ;` 53</mark> <mark>`}` 54</mark> <mark>`}`</mark> 

Figure 8: Seed heuristic used in AILS-AHD. 

13 

- **O4** : This operator concentrates on fine-tuning the parameters of a parent heuristic to generate a new one. It guides the LLM to optimize parameter settings while retaining the core structure of the parent heuristic, aiming to improve overall performance. 

#### **Prompt for Automatic Heuristic Design** 

Task: Design and code a heuristic to select nodes to be removed in a CVRP graph to enhance solution quality. The goal is to determine the shortest and most efficient routes from depot node 0, visiting multiple destinations. I have {number} heuristic with its code as follows. No. {number} heuristic and the corresponding code are: {Heuristic description} {Code} ... **{Select one operator} Firstly,** provide the description of your heuristic in braces “{}” outside the code block. **Next,** implement it in Java as a function implementation that follows after the description in format: package Perturbation; import Solution.newNode; import java.util.Random; //import other packages if needed; public class NodeSelector { public static int[] nodes_seq(float[][] disMatrix, int[][] nodesKnn, int numberSelect, newNode[] nodes, float average_nodes, Random rand) { // disMatrix: Distance matrix of the instance. // nodesKnn: A sorted int[instanceSize][100] where each element represents nearest nodes id for a given node. // numberSelect: The number of selected nodes. // nodes: An array of Node[instanceSize]. // Each ‘Node‘ object has the following properties: // - ‘Node.next‘: A reference to the next connected Node, or null if there is no connection. // - ‘Node.prev‘: A reference to the previous connected Node, or null if there is no previous connection. // - ‘Node.nodeBelong‘: A boolean, initially true, set to false once the node is selected. // - ‘Node.name‘: An integer representing the node’s ID within [0, instanceSize-1] // average_nodes: the average number of nodes of each route. // node 0 should not be selected. `@` Code your heuristic here return scores; } } Do not give additional explanation. 

Figure 9: Example of prompt engineering used in LLM-driven AHD. 

### **B.2 Evaluation Dataset** 

We carefully select 10 diverse instances from the moderate-scale instances of CVRPlib, as proposed by [11]. The selected instances are: “X-n251-k28”, “X-n256-k16”, “X-n275-k28”, “X-n359-k29”, 

14 

“X-n411-k19”, “X-n459-k26”, “X-n561-k42”, “X-n613-k62”, “X-n701-k44”, and “X-n783-k48”. For each instance, we employ two different random seeds as part of the randomness-alleviation mechanism. This results in a total of 20 runs for evaluating a newly designed heuristic. Each instance is allocated 3 _× n_ seconds to ensure complete convergence, where _n_ represents the number of nodes in the instance. The final evaluation result is calculated as the averaged gap across all instances, providing a robust metric for assessing the performance of the designed heuristic. 

### **B.3 Early Stopping Mechanism** 

During the AHD process, we employ the worst solution in the population as the stopping criterion. If the evaluation result of an instance is worse than this worst solution, the algorithm’s evaluation is terminated with a probability defined as: 



where _<u>p</u>_ represents the minimum probability threshold, _p_ ¯ = _<u>p</u>_ + 0 _._ 1 denotes the upper bound, and gap _≥_ _<u>p</u>_ ensures the probability remains within the specified range. 

15 

## **C Designed Heuristics** 

**Ours-PFD** The heuristic introduces a frequency-based mechanism that balances exploration and exploitation during node selection, as shown in Figure10. It utilizes a probabilistic approach to select nodes based on their relative frequency of usage and their proximity to other nodes. A key feature of this method is the dynamic adjustment of the probability threshold, which allows for greater diversity in node selection when randomness is favored. Additionally, an exponential decay mechanism is applied to the frequency component, ensuring that nodes previously selected are gradually deprioritized, promoting a more diverse solution space. 

<mark>1</mark> <mark>`<Ours-PFD Description>` 2</mark> <mark>`"` 3</mark> <mark>`This algorithm adapts node selection by incorporating a node ’s recent activity and current positional advantage. Nodes are chosen based on the length and quality of sequences they form when linked together , providing an interactive assessment of node potential. By enhancing the score function , the algorithm adopts a decaying influence mechanism , wherein the frequency importance decreases exponentially over time , distributing higher propensity to nodes with immediate route improvement capability. This is designed to provide a balanced effect between maintaining diversity through frequency moderation and focusing on sequence continuity and recent contributions for local optima evasion.` 4</mark> <mark>`"` 5 6</mark> <mark>`<Code>` 7</mark> <mark>`package Perturbation ;` 8 9</mark> <mark>`import Solution . newNode ;` 10</mark> <mark>`import java . util . Random ;` 11 12</mark> <mark>`public class NodeSelector {` 13 14</mark> <mark>`public static int [] nodes_seq ( float [][] disMatrix , int [][] nodesKnn , int numberSelect , newNode [] nodes , float average_nodes , Random rand ) {` 15</mark> <mark>`int [] selectedNodes = new int [ numberSelect ];` 16</mark> <mark>`int instanceSize = nodesKnn . length ;` 17 18</mark> <mark>`int countCandidates = 0;` 19</mark> <mark>`newNode initialNode ;` 20</mark> <mark>`newNode node ;` 21</mark> <mark>`float [] frequency = new float [ instanceSize ];` 22 23</mark> <mark>`for ( int i = 0; i < instanceSize ; i ++) {` 24</mark> <mark>`frequency [ i ] = 0.5 f ;`</mark> _<mark>`// Initializes the frequency component with a different starting point`</mark>_ <mark>25</mark> <mark>`}` 26 27</mark> <mark>`while ( countCandidates < numberSelect ) {` 28</mark> <mark>`float luck = rand . nextFloat ();` 29</mark> <mark>`if ( luck > 0.8) {`</mark> _<mark>`// Adjusted luck threshold`</mark>_ <mark>30</mark> <mark>`node = nodes [ rand . nextInt (1, instanceSize )];` 31</mark> <mark>`while (! node . nodeBelong )` 32</mark> <mark>`node = nodes [ rand . nextInt (1, instanceSize )];` 33 34</mark> <mark>`initialNode = node ;` 35</mark> <mark>`int sequenceLength = Math . min ( instanceSize , ( int )( numberSelect - countCandidates ));` 36</mark> <mark>`int contSizeString = 0;`</mark> Figure 10: Heuristic of Ours-PFD. 

16 

<mark>1</mark> <mark>`do {` 2</mark> <mark>`contSizeString ++;` 3</mark> <mark>`node = node . next ;` 4</mark> <mark>`if ( node . name == 0) {` 5</mark> <mark>`node = node . next ;` 6</mark> <mark>`}` 7</mark> <mark>`if ( countCandidates < numberSelect ) {` 8</mark> <mark>`selectedNodes [ countCandidates ++] = node . name ;` 9</mark> <mark>`node . nodeBelong = false ;` 10</mark> <mark>`}` 11</mark> <mark>`} while ( initialNode . name != node . name && contSizeString < sequenceLength );` 12</mark> <mark>`} else {` 13</mark> <mark>`int randomNode = rand . nextInt (1, instanceSize );` 14</mark> <mark>`for ( int i = 0; i < numberSelect && countCandidates < numberSelect ; i ++) {` 15</mark> <mark>`int candidateNode = nodesKnn [ randomNode ][ i ];` 16</mark> <mark>`if ( nodes [ candidateNode ]. nodeBelong ) {` 17</mark> <mark>`if ( rand . nextFloat () < 1 / ( frequency [ candidateNode ] + Math . exp (- i ))) {`</mark> _<mark>`// Modified score function`</mark>_ <mark>18</mark> <mark>`selectedNodes [ countCandidates ++] = candidateNode ;` 19</mark> <mark>`nodes [ candidateNode ]. nodeBelong = false ;` 20</mark> <mark>`frequency [ candidateNode ] *= 0.95;`</mark> _<mark>`// Exponential frequency decay`</mark>_ <mark>21</mark> <mark>`}` 22</mark> <mark>`}` 23</mark> <mark>`}` 24</mark> <mark>`}` 25</mark> <mark>`}` 26</mark> <mark>`return selectedNodes ;` 27</mark> <mark>`}` 28</mark> <mark>`}`</mark> 

Figure 11: Heuristic of Ours-PFD – continue. 

**Ours-DDD** The heuristic employs a demand-driven strategy, integrating a priority-based mechanism to select nodes, as shown in Figure12. This approach utilizes a spiral expansion model, where nodes within an expanding radius around a randomly chosen starting node are evaluated for selection. A weighted priority score is calculated for each node, combining factors such as demand, distance, and a decay factor to prioritize nodes that contribute more significantly to the solution. By leveraging a priority queue, this method ensures that the most promising nodes are selected iteratively, while also maintaining diversity in the solution by introducing randomness into the selection process. 

**Ours-EN** The heuristic adopts an expanding neighborhood node selection process, where nodes are chosen based on their proximity to a starting node within an expanding circular radius, as shown in Figure14. This method ensures that nodes closer to the starting point are prioritized, while also considering the need to explore a broader area by gradually increasing the radius. The heuristic avoids revisiting previously selected nodes and prevents the inclusion of depot nodes, ensuring a valid and efficient solution. By focusing on spatial proximity and systematic exploration, **Ours-EN** provides a balanced approach to node selection that promotes convergence while maintaining diversity. 

17 

<mark>1</mark> <mark>`<Ours-DDD Description>` 2</mark> <mark>`"` 3</mark> <mark>`This modified algorithm emphasizes demand but introduces a decay factor to the distance influence over time , providing flexibility in node selection. Initially , the distance has a reduced effect , but as the selection progresses , nodes far from the initial node are less favored. This encourages earlier inclusion of nodes that heavily contribute to balanced demand while maintaining a spatially coherent path , promoting partitions that are demand - dominant yet spatially efficient.` 4</mark> <mark>`"` 5 6</mark> <mark>`<Code>` 7</mark> <mark>`package Perturbation ;` 8 9</mark> <mark>`import Solution . newNode ;` 10</mark> <mark>`import java . util . Random ;` 11</mark> <mark>`import java . util . PriorityQueue ;` 12</mark> <mark>`import java . util . Comparator ;` 13 14</mark> <mark>`public class NodeSelector {` 15 16</mark> <mark>`public static int [] nodes_seq ( float [][] disMatrix , int [][] nodesKnn , int numberSelect , newNode [] nodes , float average_nodes , Random rand ) {` 17 18</mark> <mark>`int [] selectedNodes = new int [ numberSelect ];` 19</mark> <mark>`int instanceSize = nodes . length ;` 20</mark> <mark>`boolean [] selected = new boolean [ instanceSize ];` 21 22</mark> _<mark>`// Prevent selecting the depot`</mark>_ <mark>23</mark> <mark>`selected [0] = true ;` 24 25</mark> <mark>`int count = 0;` 26</mark> <mark>`float spiralRadius = 0.0 f ;` 27</mark> <mark>`float incrementRadius = 1.0 f ;` 28 29</mark> _<mark>`// Priority Queue to manage node selection based on weighted score`</mark>_ <mark>30</mark> <mark>`PriorityQueue < WeightedNode > priorityQueue = new PriorityQueue <>( Comparator . comparingDouble ( wn -> - wn . priority ));` 31 32</mark> _<mark>`// Start from a random initial node`</mark>_ <mark>33</mark> <mark>`newNode startNode = nodes [ rand . nextInt (1, instanceSize )];` 34</mark> <mark>`while (! startNode . nodeBelong ) {` 35</mark> <mark>`startNode = nodes [ rand . nextInt (1, instanceSize )];` 36</mark> <mark>`}`</mark> 

Figure 12: Heuristic of Ours-DDD. 

18 

<mark>1 2</mark> <mark>`while ( count < numberSelect ) {` 3</mark> <mark>`spiralRadius += incrementRadius ;` 4 5</mark> _<mark>`// Add nodes to the priority queue for the current spiral epoch`</mark>_ <mark>6</mark> <mark>`for ( newNode node : nodes ) {` 7</mark> <mark>`if ( node . nodeBelong && node . name != 0 && ! selected [ node . name ]) {` 8</mark> <mark>`float distance = disMatrix [ startNode . name ][ node . name ];` 9</mark> <mark>`if ( distance <= spiralRadius ) {` 10</mark> <mark>`float demand = node . demand ;` 11</mark> <mark>`float decayFactor = ( float ) Math . pow (0.9 , spiralRadius );`</mark> _<mark>`// Introduce a decay factor`</mark>_ <mark>12</mark> <mark>`float weightedPriority = ( demand * decayFactor ) / ( distance + 1) + rand . nextFloat ();` 13</mark> <mark>`priorityQueue . add ( new WeightedNode ( node . name , weightedPriority ));` 14</mark> <mark>`}` 15</mark> <mark>`}` 16</mark> <mark>`}` 17 18</mark> _<mark>`// Select nodes from the priority queue`</mark>_ <mark>19</mark> <mark>`while (! priorityQueue . isEmpty () && count < numberSelect ) {` 20</mark> <mark>`WeightedNode wn = priorityQueue . poll ();` 21</mark> <mark>`if (! selected [ wn . nodeIndex ]) {` 22</mark> <mark>`selectedNodes [ count ++] = wn . nodeIndex ;` 23</mark> <mark>`selected [ wn . nodeIndex ] = true ;` 24</mark> <mark>`nodes [ wn . nodeIndex ]. nodeBelong = false ;` 25</mark> <mark>`}` 26</mark> <mark>`}` 27</mark> <mark>`}` 28 29</mark> <mark>`return selectedNodes ;` 30</mark> <mark>`}` 31 32</mark> <mark>`static class WeightedNode {` 33</mark> <mark>`int nodeIndex ;` 34</mark> <mark>`double priority ;` 35 36</mark> <mark>`WeightedNode ( int index , double priority ) {` 37</mark> <mark>`this . nodeIndex = index ;` 38</mark> <mark>`this . priority = priority ;` 39</mark> <mark>`}` 40</mark> <mark>`}` 41</mark> <mark>`}`</mark> 

Figure 13: Heuristic of Ours-DDD – continue. 

19 

<mark>1</mark> <mark>`<Ours-EN Description>` 2</mark> <mark>`"` 3</mark> <mark>`This algorithm employs an expanding concentric circle strategy with a stochastic bias to select nodes from the CVRP graph. Starting from a randomly chosen non -depot node , it progressively investigates nodes within growing circular boundaries. The radius of these circles increases with every iteration , enhancing the coverage area. This approach provides a expanding strategy search to avoid local optima while effectively covering the solution space.` 4</mark> <mark>`"` 5 6</mark> <mark>`<Code>` 7</mark> <mark>`package Perturbation ;` 8 9</mark> <mark>`import Solution . newNode ;` 10</mark> <mark>`import java . util . Random ;` 11 12</mark> <mark>`public class NodeSelector {` 13 14</mark> <mark>`public static int [] nodes_seq ( float [][] disMatrix , int [][] nodesKnn , int numberSelect , newNode [] nodes , float average_nodes , Random rand ) {` 15 16</mark> <mark>`int [] selectedNodes = new int [ numberSelect ];` 17</mark> <mark>`int instanceSize = nodes . length ;` 18</mark> <mark>`boolean [] selected = new boolean [ instanceSize ];` 19 20</mark> _<mark>`// Prevent selecting the depot`</mark>_ <mark>21</mark> <mark>`selected [0] = true ;` 22 23</mark> <mark>`int count = 0;` 24</mark> <mark>`float circleRadius = 0.0 f ;` 25</mark> <mark>`float increaseFactor = 2.0 f ;` 26 27</mark> _<mark>`// Starting from a random non -depot node`</mark>_ <mark>28</mark> <mark>`newNode startNode = nodes [ rand . nextInt (1, instanceSize )];` 29</mark> <mark>`while (! startNode . nodeBelong ) {` 30</mark> <mark>`startNode = nodes [ rand . nextInt (1, instanceSize )];` 31</mark> <mark>`}` 32 33</mark> <mark>`while ( count < numberSelect ) {` 34</mark> <mark>`circleRadius += increaseFactor ;` 35 36</mark> <mark>`for ( newNode node : nodes ) {` 37</mark> <mark>`if ( node . nodeBelong && node . name != 0 && ! selected [ node . name ]) {` 38</mark> <mark>`float distance = disMatrix [ startNode . name ][ node . name ];` 39</mark> <mark>`if ( distance <= circleRadius && count < numberSelect ) {` 40</mark> <mark>`selectedNodes [ count ++] = node . name ;` 41</mark> <mark>`selected [ node . name ] = true ;` 42</mark> <mark>`nodes [ node . name ]. nodeBelong = false ;` 43</mark> <mark>`}` 44</mark> <mark>`}` 45</mark> <mark>`}` 46</mark> <mark>`}` 47 48</mark> <mark>`return selectedNodes ;` 49</mark> <mark>`}` 50</mark> <mark>`}`</mark> 

Figure 14: Heuristic of Ours-EN. 

20 



Figure 15: More convergence curves on moderate-scale instances. 

## **D More Experimental Results** 

### **D.1 More Convergence Curves** 

Due to the fact that solutions for small-scale instances are mostly proven to be optimal, in this subsection, we first present the convergence curves of the largest 12 instances within the moderatescale instances. Overall, our designed heuristics demonstrate superior convergence performance compared to the benchmark methods. 

### **D.2 Detailed Results on Moderate-scale Instances** 

In this subsection, we present detailed results for every instance within the moderate-scale dataset. Surprisingly, one of our methods, Ours-PDF, has successfully discovered a new best-known solution for the instance X-n1001-k43. 

21 

|Instance|BKS||HGS||AILS-II||Ours-EN|
|---|---|---|---|---|---|---|---|
|||Best|Avg.(%) (+/-/=)|Best|Avg.(%) (+/-/=)|Best|Avg.(%)|
|X-n101-k25<br>X-n106-k14|**27591.0000**<br>**263620000**|27591.0000<br>263760000|27591.0000_±_0.00e+00(=)<br>263760000_±_000e+00(+)|27591.0000<br>263620000|27591.0000_±_0.00e+00(=)<br>263620000_±_000e+00(=)|27591.0000<br>263620000|27591.0000_±_0.00e+00<br>263620000_±_000e+00|
|X110k13|**.**<br>**149710000**|.<br>149710000|. .<br>149710000_±_00000|.<br>149710000|. .<br>149710000_±_00000|.<br>149710000|. .<br>149710000_±_00000|
|-n-<br>X-n115-k10<br>|**.**<br>**12747.0000**<br>|.<br>12747.0000<br>|. .e+(=)<br>12747.0000_±_0.00e+00(=)<br>|.<br>12747.0000<br>|. .e+(=)<br>12747.0000_±_0.00e+00(=)<br>|.<br>12747.0000<br>|. .e+<br>12747.0000_±_0.00e+00<br>|
|X-n120-k6<br>X-n125-k30|**13332.0000**<br>**55539.0000**|13332.0000<br>55539.0000|13332.0000_±_0.00e+00(=)<br>55539.0000_±_0.00e+00(=)|13332.0000<br>55539.0000|13332.0000_±_0.00e+00(=)<br>55539.0000_±_0.00e+00(=)|13332.0000<br>55539.0000|13332.0000_±_0.00e+00<br>55539.0000_±_0.00e+00|
|X-n129-k18|**28940.0000**|28940.0000|28940.0000_±_0.00e+00(-)|28940.0000|28941.8667_±_4.06e+00(=)|28940.0000|28941.7333_±_3.21e+00|
|X-n134-k13|**10916.0000**|10916.0000|10916.0000_±_0.00e+00(=)|10916.0000|10916.0000_±_0.00e+00(=)|10916.0000|10916.0000_±_0.00e+00|
|X-n139-k10<br>X-n143-k7|**13590.0000**<br>**157000000**|13590.0000<br>157000000|<br>13590.0000_±_0.00e+00(=)<br>157000000_±_000e+00(-)|13590.0000<br>157000000|<br>13590.0000_±_0.00e+00(=)<br>157072333_±_756e+00(=)|13590.0000<br>157000000|13590.0000_±_0.00e+00<br>157070000_±_824e+00|
|X-n148-k46<br>|**.**<br>**43448.0000**<br>|.<br>43448.0000<br>|. .<br>43448.0000_±_0.00e+00(=)<br>|.<br>43448.0000<br>|. .<br>43448.0000_±_0.00e+00(=)<br>|.<br>43448.0000<br>|. .<br>43448.0000_±_0.00e+00<br>|
|X-n153-k22<br>X-n157-k13<br>|**21220.0000**<br>**16876.0000**<br>|21225.0000<br>16876.0000<br>|21225.0000_±_0.00e+00(+)<br>16876.0000_±_0.00e+00(=)<br>|21221.0000<br>16876.0000<br>|21224.8667_±_7.18e-01(+)<br>16876.0000_±_0.00e+00(=)<br>|21220.0000<br>16876.0000<br>|21223.8000_±_2.10e+00<br>16876.0000_±_0.00e+00<br>|
|X-n162-k11|**14138.0000**|14138.0000|14138.0000_±_0.00e+00(=)|14138.0000|14138.0000_±_0.00e+00(=)|14138.0000|14138.0000_±_0.00e+00|
|X-n167-k10|**20557.0000**|20557.0000|20557.0000_±_0.00e+00(=)|20557.0000|20557.0000_±_0.00e+00(=)|20557.0000|20557.0000_±_0.00e+00|
|X-n172-k51|**45607.0000**|45607.0000|45607.0000_±_0.00e+00(=)|45607.0000|45607.7000_±_2.30e+00(=)|45607.0000|45609.5333_±_7.71e+00|
|X-n176-k26|**47812.0000**|47812.0000|47812.0000_±_0.00e+00(=)|47812.0000|47812.0000_±_0.00e+00(=)|47812.0000|47812.0000_±_0.00e+00|
|X-n181-k23<br>X-n186-k15|**25569.0000**<br>**241450000**|25569.0000<br>241450000|<br>25569.0000_±_0.00e+00(-)<br>241450000_±_000e+00(-)|25569.0000<br>241450000|<br>25570.7000_±_2.62e+00(=)<br>241497333_±_369e+00(=)|25569.0000<br>241450000|25572.0000_±_5.51e+00<br>241506000_±_348e+00|
|X-n190-k8<br>|**.**<br>**16980.0000**<br>|.<br>16986.0000<br>|. .<br>16986.0000_±_0.00e+00(+)<br>|.<br>16980.0000<br>|. .<br>16981.4000_±_2.01e+00(=)<br>|.<br>16980.0000<br>|. .<br>16981.2333_±_2.11e+00<br>|
|X-n195-k51<br>X-n200-k36<br>|**44225.0000**<br>**58578.0000**<br>|44225.0000<br>58578.0000<br>|44225.0000_±_0.00e+00(-)<br>58578.0000_±_0.00e+00(-)<br>|44225.0000<br>58578.0000<br>|44257.3333_±_1.79e+01(=)<br>58588.3333_±_1.48e+01(=)<br>|44234.0000<br>58578.0000<br>|44259.7667_±_1.13e+01<br>58590.5000_±_1.69e+01<br>|
|X-n204-k19<br>X-n209-k16|**19565.0000**<br>**30656.0000**|19565.0000<br>30656.0000|19565.0000_±_0.00e+00(=)<br>30656.0000_±_0.00e+00(-)|19565.0000<br>30656.0000|19566.4333_±_4.21e+00(=)<br>30661.8667_±_6.54e+00(=)|19565.0000<br>30656.0000|19566.3000_±_4.12e+00<br>30659.2000_±_5.79e+00|
|X-n214-k11|**10856.0000**|10856.0000|10856.0000_±_0.00e+00(-)|10867.0000|10869.4667_±_2.38e+00(=)|10867.0000|10869.6333_±_4.36e+00|
|X-n219-k73|**117595.0000**|117595.0000|<br>117595.0000_±_0.00e+00(=)|117595.0000|<br>117595.0000_±_0.00e+00(=)|117595.0000|117595.0000_±_0.00e+00|
|X-n223-k34<br>X-n228-k23|**40437.0000**<br>**257420000**|40437.0000<br>257430000|<br>40437.0000_±_0.00e+00(-)<br>257430000_±_000e+00(=)|40437.0000<br>257420000|<br>40442.7000_±_1.36e+01(=)<br>257528000_±_174e+01(+)|40437.0000<br>257420000|40451.8000_±_2.31e+01<br>257432667_±_163e+00|
|X233k16|**.**<br>**192300000**|.<br>192300000|. .<br>192300000_±_00000|.<br>192300000|. .<br>192561667_±_19501|.<br>192300000|. .<br>192468333_±_25301|
|-n-<br>X-n237-k14<br>|**.**<br>**27042.0000**<br>|.<br>27042.0000<br>|. .e+(-)<br>27042.0000_±_0.00e+00(-)<br>|.<br>27042.0000<br>|. .e+(=)<br>27051.6333_±_1.60e+01(=)<br>|.<br>27042.0000<br>|. .e+<br>27047.3333_±_1.09e+01<br>|
|X-n242-k48<br>X-n247-k50|**82751.0000**<br>**37274.0000**|82789.0000<br>37274.0000|82790.5000_±_1.50e+00(-)<br>37274.0000_±_0.00e+00(=)|82751.0000<br>37274.0000|82796.6000_±_4.90e+01(=)<br>37274.0667_±_2.49e-01(=)|82751.0000<br>37274.0000|82813.1667_±_4.21e+01<br>37274.4000_±_1.23e+00|
|X-n251-k28<br>X-n256-k16|**38684.0000**<br>**18839.0000**|38699.0000<br>18839.0000|38699.0000_±_0.00e+00(-)<br>18839.0000_±_0.00e+00(-)|38684.0000<br>18839.0000|38740.6000_±_3.47e+01(=)<br>18868.3667_±_1.47e+01(=)|38684.0000<br>18839.0000|38744.9000_±_3.88e+01<br>18871.3000_±_2.03e+01|
|X-n261-k13|**26558.0000**|26558.0000|<br>26558.0000_±_0.00e+00(-)|26558.0000|<br>26572.1333_±_1.67e+01(=)|26558.0000|26581.8333_±_2.02e+01|
|X-n266-k58|**754780000**|755750000|<br>755750000_±_000e+00(+)|754780000|<br>755537333_±_463e+01(=)|754780000|<br>755466333_±_489e+01|
|X-n270-k35<br>|**.**<br>**35291.0000**<br>**2124**|.<br>35303.0000<br>|. .<br>35303.0000_±_0.00e+00(-)<br>|.<br>35303.0000<br>|. .<br>35323.3000_±_2.03e+01(=)<br>|.<br>35303.0000<br>|. .<br>35319.4333_±_1.90e+01<br>|
|X-n275-k28<br>|**5.0000**<br>|21245.0000<br>|21245.0000_±_0.00e+00(=)<br>|21245.0000<br>|21247.5333_±_1.03e+01(=)<br>|21245.0000<br>|21246.8333_±_7.14e+00<br>|
|X-n280-k17<br>|**33503.0000**<br>|33506.0000<br>|33506.0000_±_0.00e+00(-)<br>|33505.0000<br>|33565.3667_±_2.93e+01(+)<br>|33505.0000<br>|33549.5333_±_2.82e+01<br>|
|X-n284-k15|**20226.0000**<br>|20243.0000<br>|20243.0000_±_0.00e+00(-)<br>|20225.0000<br>|20257.5000_±_1.26e+01(=)<br>|20226.0000<br>|20255.6000_±_1.31e+01<br>|
|X-n289-k60|**95151.0000**|95323.0000|95323.0000_±_0.00e+00(+)|95180.0000|95252.4667_±_4.24e+01(=)|95151.0000|95248.9667_±_4.45e+01|
|X-n294-k50|**47161.0000**|47172.0000|47172.0000_±_0.00e+00(-)|47167.0000|47204.0000_±_2.93e+01(=)|47169.0000|47212.7333_±_2.78e+01|
|X-n298-k31|**34231.0000**|34231.0000|34231.0000_±_0.00e+00(-)|34231.0000|34261.0000_±_1.73e+01(=)|34231.0000|34262.5667_±_2.30e+01|
|X-n303-k21|**21736.0000**|217380000|<br>217380000_±_000e+00(-)|217380000|<br>217591667_±_301e+01(=)|217470000|217588333_±_312e+01|
|X-n308-k13|**258590000**|.<br>258620000|. .<br>258620000_±_000e+00(-)|.<br>258610000|. .<br>258808000_±_219e+01(=)|.<br>258610000|. .<br>258719000_±_201e+01|
|X313k71|**.**<br>**940430000**|.<br>940510000|. .<br>940510000_±_00000|.<br>940550000|. .<br>940969333_±_36601|.<br>940440000|. .<br>941015000_±_37601|
|-n-<br>|**.**<br>|.<br>|. .e+(-)<br>|.<br>|. .e+(=)<br>|.<br>|. .e+<br>|
|X-n317-k53<br>|**78355.0000**<br>|78368.0000<br>|78368.0000_±_0.00e+00(+)<br>|78355.0000<br>|78355.5333_±_1.36e+00(=)<br>|78355.0000<br>|78355.6667_±_1.49e+00<br>|
|X-n322-k28<br>X-n327-k20|**29834.0000**<br>**27532.0000**|29855.0000<br>27557.0000|29855.0000_±_0.00e+00(-)<br>27557.0000_±_0.00e+00(-)|29854.0000<br>27547.0000|29865.3000_±_1.66e+01(=)<br>27583.8667_±_2.01e+01(=)|29848.0000<br>27532.0000|29871.9333_±_1.58e+01<br>27588.3333_±_2.23e+01|
|X-n331-k15|**31102.0000**|31103.0000|31103.0000_±_0.00e+00(-)|31103.0000|31104.9333_±_6.76e+00(=)|31103.0000|31105.8000_±_5.46e+00|
|X-n336-k84|**139111.0000**|139272.0000|139272.0000_±_0.00e+00(=)|139139.0000|139283.5333_±_7.05e+01(=)|139197.0000|139269.6667_±_4.81e+01|
|X-n344-k43|**42050.0000**|42064.0000|<br>42064.0000_±_0.00e+00(-)|42062.0000|<br>42112.8333_±_3.06e+01(+)|42056.0000|42097.0000_±_2.53e+01|
|X-n351-k40|**258960000**|259550000|<br>259550000_±_000e+00(+)|259270000|<br>259541667_±_207e+01(=)|259250000|259480333_±_141e+01|
|X-n359-k29|**.**<br>**515050000**|.<br>515740000|. .<br>515740000_±_000e+00(+)|.<br>515050000|. .<br>515344667_±_230e+01(-)|.<br>515050000|. .<br>515563333_±_421e+01|
|X367k17|**.**<br>**228140000**|.<br>228140000|. .<br>228140000_±_00000|.<br>228140000|. .<br>228223000_±_56000|.<br>228140000|. .<br>228246667_±_52200|
|-n-<br>|**.**<br>|.<br>|. .e+(-)<br>|.<br>|. .e+(=)<br>|.<br>|. .e+<br>|
|X-n376-k94<br>X-n384-k52<br>|**147713.0000**<br>**65940.0000**<br>|147713.0000<br>66074.0000<br>|147713.0000_±_0.00e+00(-)<br>66074.0000_±_0.00e+00(+)<br>|147713.0000<br>65966.0000<br>|147714.2667_±_1.46e+00(=)<br>66024.5000_±_4.43e+01(=)<br>|147713.0000<br>65939.0000<br>|147713.9333_±_1.41e+00<br>66001.3000_±_4.58e+01<br>|
|X-n393-k38|**38260.0000**|38260.0000|38260.0000_±_0.00e+00(-)|38260.0000|38284.7667_±_2.99e+01(=)|38260.0000|38286.6333_±_3.17e+01|
|X-n401-k29|**66154.0000**|66213.0000|66213.0000_±_0.00e+00(-)|66186.0000|66216.7333_±_1.63e+01(=)|66193.0000|66219.5667_±_1.15e+01|
|X-n411-k19<br>X-n420-k130|**19712.0000**<br>**107798.0000**|19717.0000<br>107888.0000|19717.0000_±_0.00e+00(-)<br>107888.0000_±_0.00e+00(+)|19719.0000<br>107798.0000|19739.2667_±_1.51e+01(+)<br>107823.3000_±_1.70e+01(=)|19716.0000<br>107798.0000|19731.3667_±_1.03e+01<br>107822.0333_±_2.19e+01|
|X-n429-k61<br>X-n439-k37|**65449.0000**<br>**363910000**|65508.0000<br>363950000|<br>65508.0000_±_0.00e+00(-)<br>363950000_±_000e+00(-)|65468.0000<br>363950000|<br>65519.9333_±_2.62e+01(=)<br>364077667_±_118e+01(=)|65462.0000<br>363940000|<br>65525.1000_±_2.95e+01<br>364028667_±_106e+01|
|X-n449-k29<br>|**.**<br>**55233.0000**<br>|.<br>55349.0000<br>|. .<br>55349.0000_±_0.00e+00(+)<br>|.<br>55239.0000<br>|. .<br>55306.6333_±_3.62e+01(=)<br>|.<br>55237.0000<br>|. .<br>55304.7000_±_3.71e+01<br>|
|X-n459-k26<br>X-n469-k138|**24139.0000**<br>**221824.0000**|24160.0000<br>222159.0000|24160.0000_±_0.00e+00(=)<br>222159.0000_±_0.00e+00(+)|24141.0000<br>221872.0000|24162.0000_±_1.56e+01(=)<br>222025.9333_±_1.11e+02(=)|24139.0000<br>221861.0000|24162.8000_±_1.51e+01<br>222033.0667_±_8.05e+01|
|X-n480-k70<br>X-n491-k59|**89449.0000**<br>**66483.0000**|89468.0000<br>66531.0000|89468.0000_±_0.00e+00(=)<br>66531.0000_±_0.00e+00(-)|89449.0000<br>66508.0000|89461.6667_±_9.69e+00(=)<br>66570.7000_±_5.93e+01(=)|89449.0000<br>66485.0000|89469.0333_±_1.78e+01<br>66576.7000_±_6.02e+01|
|X-n502-k39|**69226.0000**|69268.0000|<br>69268.0000_±_0.00e+00(+)|69226.0000|<br>69231.3000_±_8.87e+00(=)|69226.0000|69234.9000_±_8.32e+00|
|X-n513-k21|**24201.0000**|242010000|<br>242010000_±_000e+00(-)|242010000|<br>242226000_±_282e+01(+)|242010000|242092667_±_170e+01|
|X-n524-k153|**1545930000**|.<br>1547550000|. .<br>1547550000_±_000e+00(+)|.<br>1546020000|. .<br>1546285333_±_404e+01(=)|.<br>1545990000|. .<br>1546415667_±_587e+01|
|X536k96|**.**<br>**948460000**|.<br>951010000|. .<br>951010000_±_00000|.<br>948540000|. .<br>949178000_±_32401|.<br>948450000|. .<br>949218333_±_43301|
|-n-<br>|**.**<br>|.<br>|. .e+(+)<br>|.<br>|. .e+(=)<br>|.<br>|. .e+<br>|
|X-n548-k50<br>|**86700.0000**<br>|86792.0000<br>|86792.0000_±_0.00e+00(+)<br>|86704.0000<br>|86739.2333_±_2.24e+01(=)<br>|86704.0000<br>|86728.5667_±_1.96e+01<br>|
|X-n561-k42<br>|**42717.0000**<br>|42734.0000<br>|42734.0000_±_0.00e+00(-)<br>|42719.0000<br>|42763.3333_±_2.71e+01(+)<br>|42719.0000<br>|42750.0000_±_1.87e+01<br>|
|X-n573-k30|**50673.0000**|50798.0000|50814.7000_±_1.17e+01(+)|50720.0000|50736.8333_±_1.40e+01(+)|50720.0000|50730.5000_±_9.07e+00|
|X-n586-k159|**190316.0000**|190537.0000|190537.0000_±_0.00e+00(+)|190316.0000|190393.6333_±_3.88e+01(=)|190316.0000|190393.3667_±_4.12e+01|
|X-n599-k92<br>X-n613-k62|**108451.0000**<br>**59535.0000**|108617.0000<br>59632.0000|108635.8333_±_1.91e+01(+)<br>59632.0000_±_0.00e+00(+)|108475.0000<br>59545.0000|108577.7667_±_4.99e+01(=)<br>59602.4000_±_3.65e+01(=)|108484.0000<br>59536.0000|108568.5333_±_5.41e+01<br>59610.9333_±_4.56e+01|
|X-n627-k43|**621640000**|623840000|<br>623891333_±_269e+00(+)|621700000|<br>622222000_±_335e+01(=)|621750000|<br>622100333_±_264e+01|
|X-n641-k35<br>X655k131|**.**<br>**63684.0000**<br>**1067800000**|.<br>63867.0000<br>1068180000|. .<br>63867.0000_±_0.00e+00(+)<br>1068180000_±_00000|.<br>63713.0000<br>1067800000|. .<br>63765.7667_±_2.71e+01(=)<br>1067888667_±_10101|.<br>63705.0000<br>1067800000|. .<br>63768.2333_±_3.78e+01<br>1067901000_±_98200|
|-n-<br>X-n670-k130<br>X-n685-k75|**.**<br>**146332.0000**<br>**68205.0000**|.<br>146848.0000<br>68344.0000|. .e+(+)<br>146848.1000_±_5.39e-01(=)<br>68344.0000_±_0.00e+00(+)|.<br>146441.0000<br>68227.0000|. .e+(=)<br>146787.5667_±_1.33e+02(=)<br>68299.7333_±_4.37e+01(=)|.<br>146459.0000<br>68227.0000|. .e+<br>146810.2000_±_1.46e+02<br>68290.9000_±_3.92e+01|
|X-n701-k44|**81923.0000**|82352.0000|82353.2333_±_2.06e+00(+)|81939.0000|81987.6000_±_4.40e+01(=)|81931.0000|81984.3333_±_4.78e+01|
|X-n716-k35|**43373.0000**|43489.0000|43489.0000_±_0.00e+00(+)|43371.0000|43402.8667_±_2.30e+01(=)|43371.0000|43392.8667_±_2.16e+01|



> a Better BKS obtained by Ours. 

Table 3: Results achieves on the moderate-scale instances among compared methods. 

22 

|Instance|BKS||HGS||AILS-II||Ours-EN|
|---|---|---|---|---|---|---|---|
|||Best|Avg.(%) (+/-/=)|Best|Avg.(%) (+/-/=)|Best|Avg.(%)|
|X-n733-k159|**136187.0000**|136457.0000|136457.0000_±_0.00e+00(+)|136213.0000|136286.0667_±_3.70e+01(=)|136211.0000|136281.1333_±_4.26e+01|
|X-n749-k98|**77269.0000**|77796.0000|77798.5667_±_4.65e+00(+)|77334.0000|77395.9333_±_3.78e+01(=)|77335.0000|77405.4333_±_4.56e+01|
|X-n766-k71|**114417.0000**|114754.0000|114754.0000_±_0.00e+00(+)|114427.0000|114477.9333_±_4.37e+01(=)|114426.0000|114466.9000_±_3.49e+01|
|X-n783-k48|**72386.0000**|72759.0000|72759.0000_±_0.00e+00(+)|72423.0000|72482.0667_±_4.73e+01(=)|72427.0000|72480.4667_±_3.83e+01|
|X-n801-k40|**73311.0000**|73474.0000|73474.0000_±_0.00e+00(+)|73311.0000|73364.3000_±_3.44e+01(=)|73311.0000|73369.7000_±_3.91e+01|
|X-n819-k171|**158121.0000**|158491.0000|158647.8667_±_6.74e+01(+)|158199.0000|158257.1667_±_3.26e+01(=)|158176.0000|158247.0333_±_3.18e+01|
|X-n837-k142|**193737.0000**|194141.0000|194267.8667_±_7.09e+01(+)|193739.0000|193825.0667_±_4.78e+01(=)|193764.0000|193816.5000_±_3.34e+01|
|X-n856-k95|**88965.0000**|88990.0000|88990.0000_±_0.00e+00(-)|88966.0000|89012.8333_±_3.21e+01(=)|88966.0000|89014.1333_±_2.75e+01|
|X-n876-k59|**99299.0000**|99687.0000|99705.1667_±_1.05e+01(+)|99352.0000|99426.2333_±_4.89e+01(=)|99347.0000|99442.0333_±_4.33e+01|
|X-n895-k37|**53860.0000**|54098.0000|54098.0000_±_0.00e+00(+)|53855.0000|53952.5333_±_5.62e+01(=)|53860.0000|53931.3333_±_4.13e+01|
|X-n916-k207|**329179.0000**|329909.0000|329937.0333_±_1.45e+01(+)|329225.0000|329315.3000_±_4.02e+01(=)|329230.0000|329297.4667_±_4.59e+01|
|X-n936-k151|**132715.0000**|133599.0000|133612.6333_±_2.73e+01(+)|132919.0000|132971.4667_±_3.87e+01(=)|132880.0000|132983.8333_±_4.63e+01|
|X-n957-k87|**85465.0000**|85581.0000|85581.0000_±_0.00e+00(+)|85470.0000|85508.4000_±_2.03e+01(+)|85469.0000|85495.7000_±_2.08e+01|
|X-n979-k58|**118976.0000**|119317.0000|119394.5333_±_5.84e+01(+)|118973.0000|119004.7333_±_3.03e+01(=)|118975.0000|119005.6667_±_2.12e+01|
|X-n1001-k43|**72355.0000**|72590.0000|72594.8667_±_7.44e+00(+)|72364.0000|72442.7667_±_3.90e+01(=)|72368.0000|72426.9333_±_3.94e+01|
|Average||0.1056|0.109 (40/38/22)|0.0152|0.0702 (9/1/90)|0.0135|0.0672|



> a Better BKS obtained by Ours. 

Table 4: Results achieves on the moderate-scale instances among compared methods – continue. 

|Instance|BKS||Ours-PFD||Ours-DDD||Ours-EN|
|---|---|---|---|---|---|---|---|
|||Best|Avg.(%) (+/-/=)|Best|Avg.(%) (+/-/=)|Best|Avg.(%)|
|X-n101-k25|**27591.00**|27591.00|27591.00_±_0.00e+00(=)|27591.00|27591.00_±_0.00e+00(=)|27591.00|27591.00_±_0.00e+00|
|X-n106-k14|**26362.00**|26362.00|26362.00_±_0.00e+00(=)|26362.00|26362.00_±_0.00e+00(=)|26362.00|26362.00_±_0.00e+00|
|X-n110-k13|**14971.00**|14971.00|14971.00_±_0.00e+00(=)|14971.00|14971.00_±_0.00e+00(=)|14971.00|14971.00_±_0.00e+00|
|X-n115-k10|**12747.00**|12747.00|12747.00_±_0.00e+00(=)|12747.00|12747.00_±_0.00e+00(=)|12747.00|12747.00_±_0.00e+00|
|X-n120-k6|**13332.00**|13332.00|13332.00_±_0.00e+00(=)|13332.00|13332.00_±_0.00e+00(=)|13332.00|13332.00_±_0.00e+00|
|X-n125-k30|**55539.00**|55539.00|55539.00_±_0.00e+00(=)|55539.00|55539.00_±_0.00e+00(=)|55539.00|55539.00_±_0.00e+00|
|X-n129-k18|**28940.00**|28940.00|<br>28941.13_±_3.17e+00(=)|28940.00|<br>28940.40_±_1.58e+00(-)|28940.00|28941.73_±_3.21e+00|
|X-n134-k13|**10916.00**|10916.00|10916.00_±_0.00e+00(=)|10916.00|10916.00_±_0.00e+00(=)|10916.00|10916.00_±_0.00e+00|
|X-n139-k10|**13590.00**|13590.00|13590.00_±_0.00e+00(=)|13590.00|13590.00_±_0.00e+00(=)|13590.00|13590.00_±_0.00e+00|
|X-n143-k7|**15700.00**|15700.00|15704.50_±_7.60e+00(=)|15700.00|15706.63_±_7.94e+00(=)|15700.00|15707.00_±_8.24e+00|
|X-n148-k46|**43448.00**|43448.00|43448.00_±_0.00e+00(=)|43448.00|43448.00_±_0.00e+00(=)|43448.00|43448.00_±_0.00e+00|
|X-n153-k22|**21220.00**|21220.00|21224.60_±_1.96e+00(=)|21220.00|21224.20_±_1.80e+00(=)|21220.00|21223.80_±_2.10e+00|
|X-n157-k13|**16876.00**|16876.00|16876.00_±_0.00e+00(=)|16876.00|16876.00_±_0.00e+00(=)|16876.00|16876.00_±_0.00e+00|
|X-n162-k11|**14138.00**|14138.00|14138.00_±_0.00e+00(=)|14138.00|14138.00_±_0.00e+00(=)|14138.00|14138.00_±_0.00e+00|
|X-n167-k10|**20557.00**|20557.00|20557.00_±_0.00e+00(=)|20557.00|20557.00_±_0.00e+00(=)|20557.00|20557.00_±_0.00e+00|
|X-n172-k51|**45607.00**|45607.00|45607.70_±_3.77e+00(=)|45607.00|45608.17_±_5.43e+00(=)|45607.00|45609.53_±_7.71e+00|
|X-n176-k26|**47812.00**|47812.00|<br>47812.00_±_0.00e+00(=)|47812.00|<br>47812.00_±_0.00e+00(=)|47812.00|47812.00_±_0.00e+00|
|X-n181-k23|**25569.00**|25569.00|25570.73_±_1.61e+00(=)|25569.00|25571.10_±_2.90e+00(=)|25569.00|25572.00_±_5.51e+00|
|X-n186-k15|**24145.00**|24145.00|24150.67_±_3.52e+00(=)|24145.00|24151.43_±_3.53e+00(=)|24145.00|24150.60_±_3.48e+00|
|X-n190-k8|**16980.00**|16980.00|16981.10_±_2.77e+00(=)|16980.00|16980.70_±_1.46e+00(=)|16980.00|16981.23_±_2.11e+00|
|X-n195-k51|**44225.00**|44225.00|<br>44258.97_±_1.55e+01(=)|44225.00|<br>44258.03_±_1.38e+01(=)|44234.00|44259.77_±_1.13e+01|
|X-n200-k36|**58578.00**|58578.00|58585.57_±_1.40e+01(=)|58578.00|58588.57_±_1.55e+01(=)|58578.00|58590.50_±_1.69e+01|
|X-n204-k19|**19565.00**|19565.00|19565.00_±_0.00e+00(=)|19565.00|19565.87_±_3.33e+00(=)|19565.00|19566.30_±_4.12e+00|
|X-n209-k16|**30656.00**|30656.00|30663.33_±_7.39e+00(+)|30656.00|30661.43_±_6.33e+00(=)|30656.00|30659.20_±_5.79e+00|
|X-n214-k11|**10856.00**|10863.00|10868.60_±_2.20e+00(=)|10867.00|10870.47_±_3.81e+00(=)|10867.00|10869.63_±_4.36e+00|
|X-n219-k73|**117595.00**|117595.00|<br>117595.00_±_0.00e+00(=)|117595.00|<br>117595.00_±_0.00e+00(=)|117595.00|117595.00_±_0.00e+00|
|X-n223-k34|**40437.00**|40437.00|40442.63_±_3.53e+00(-)|40437.00|40450.67_±_2.10e+01(=)|40437.00|40451.80_±_2.31e+01|
|X-n228-k23|**25742.00**|25742.00|25750.43_±_1.69e+01(+)|25742.00|25745.20_±_8.37e+00(=)|25742.00|25743.27_±_1.63e+00|
|X-n233-k16|**19230.00**|19230.00|19256.87_±_2.57e+01(=)|19230.00|19254.37_±_2.57e+01(=)|19230.00|19246.83_±_2.53e+01|
|X-n237-k14|**27042.00**|27042.00|27046.67_±_8.27e+00(=)|27042.00|27050.77_±_1.43e+01(=)|27042.00|27047.33_±_1.09e+01|
|X-n242-k48|**82751.00**|82751.00|82799.90_±_4.35e+01(=)|82751.00|82806.10_±_4.96e+01(=)|82751.00|82813.17_±_4.21e+01|
|X-n247-k50|**37274.00**|37274.00|37274.00_±_0.00e+00(=)|37274.00|37274.00_±_0.00e+00(=)|37274.00|37274.40_±_1.23e+00|
|X-n251-k28|**38684.00**|38684.00|38731.97_±_3.65e+01(=)|38684.00|38730.70_±_3.66e+01(=)|38684.00|38744.90_±_3.88e+01|
|X-n256-k16|**18839.00**|18839.00|18874.30_±_1.12e+01(=)|18839.00|18870.83_±_1.57e+01(=)|18839.00|18871.30_±_2.03e+01|
|X-n261-k13|**26558.00**|26558.00|<br>26573.10_±_1.71e+01(=)|26558.00|<br>26581.80_±_2.04e+01(=)|26558.00|26581.83_±_2.02e+01|
|X-n266-k58|**75478.00**|75478.00|<br>75540.40_±_4.59e+01(=)|75478.00|<br>75555.80_±_3.78e+01(=)|75478.00|75546.63_±_4.89e+01|
|X-n270-k35|**35291.00**|35303.00|35318.27_±_1.95e+01(=)|35303.00|35321.20_±_1.66e+01(=)|35303.00|35319.43_±_1.90e+01|
|X-n275-k28|**21245.00**|21245.00|21245.30_±_1.62e+00(=)|21245.00|21245.20_±_1.08e+00(=)|21245.00|21246.83_±_7.14e+00|
|X-n280-k17|**33503.00**|33505.00|33544.50_±_2.73e+01(=)|33505.00|33546.70_±_2.51e+01(=)|33505.00|33549.53_±_2.82e+01|
|X-n284-k15|**20226.00**|20225.00|20258.40_±_1.17e+01(=)|20241.00|20259.00_±_1.07e+01(=)|20226.00|20255.60_±_1.31e+01|
|X-n289-k60|**95151.00**|95151.00|95266.33_±_3.93e+01(=)|95175.00|95261.17_±_3.95e+01(=)|95151.00|95248.97_±_4.45e+01|



> a Better BKS obtained by Ours. 

Table 5: Comparison of results on moderate-scale instances among the top-3 designed heuristics. 

23 

|Instance|BKS||Ours-PFD||Ours-DDD||Ours-EN|
|---|---|---|---|---|---|---|---|
|||Best|Avg.(%) (+/-/=)|Best|Avg.(%) (+/-/=)|Best|Avg.(%)|
|X-n294-k50|**47161.00**|47169.00|47209.33_±_2.76e+01(=)|47167.00|47201.50_±_2.38e+01(=)|47169.00|47212.73_±_2.78e+01|
|X-n298-k31<br>X-n303-k21|**34231.00**<br>**2173600**|34231.00<br>2174800|<br>34262.40_±_2.22e+01(=)<br>2176717_±_328e+01(=)|34231.00<br>2174200|<br>34250.97_±_2.09e+01(-)<br>2176377_±_326e+01(=)|34231.00<br>2174700|34262.57_±_2.30e+01<br>2175883_±_312e+01|
|X-n308-k13|**.**<br>**25859.00**|.<br>25859.00|. .<br>25871.93_±_2.02e+01(=)|.<br>25859.00|. .<br>25873.40_±_2.42e+01(=)|.<br>25861.00|. .<br>25871.90_±_2.01e+01|
|X-n313-k71|**94043.00**|94044.00|<br>94089.33_±_4.23e+01(=)|94044.00|<br>94089.57_±_3.44e+01(=)|94044.00|94101.50_±_3.76e+01|
|X-n317-k53|**78355.00**|78355.00|<br>78356.03_±_1.72e+00(=)|78355.00|<br>78355.67_±_1.49e+00(=)|78355.00|78355.67_±_1.49e+00|
|X-n322-k28|**29834.00**|29844.00|29864.17_±_1.53e+01(=)|29844.00|29871.20_±_1.70e+01(=)|29848.00|29871.93_±_1.58e+01|
|X-n327-k20|**27532.00**|27532.00|27586.77_±_2.48e+01(=)|27532.00|27586.17_±_2.96e+01(=)|27532.00|27588.33_±_2.23e+01|
|X-n331-k15<br>|**31102.00**<br>|31103.00<br>|31104.17_±_3.18e+00(=)<br>|31103.00<br>|31103.90_±_9.78e-01(=)<br>|31103.00<br>|31105.80_±_5.46e+00<br>|
|X-n336-k84<br>X-n344-k43|**139111.00**<br>**42050.00**|139111.00<br>42056.00|139264.50_±_6.26e+01(=)<br>42104.20_±_2.81e+01(=)|139171.00<br>42056.00|139287.90_±_7.29e+01(=)<br>42094.77_±_2.45e+01(=)|139197.00<br>42056.00|139269.67_±_4.81e+01<br>42097.00_±_2.53e+01|
|X-n351-k40|**25896.00**|25925.00|25951.37_±_2.00e+01(=)|25925.00|25955.30_±_1.81e+01(=)|25925.00|25948.03_±_1.41e+01|
|X-n359-k29|**51505.00**|51505.00|<br>51558.57_±_3.96e+01(=)|51505.00|<br>51539.17_±_3.00e+01(=)|51505.00|51556.33_±_4.21e+01|
|X-n367-k17<br>|**22814.00**<br>|22814.00<br>|22824.33_±_5.01e+00(=)<br>|22814.00<br>|22825.33_±_4.37e+00(=)<br>|22814.00<br>|22824.67_±_5.22e+00<br>|
|X-n376-k94|**147713.00**|147713.00|147714.00_±_1.63e+00(=)|147713.00|147713.80_±_1.47e+00(=)|147713.00|147713.93_±_1.41e+00|
|X-n384-k52|**65940.00**|6594100|6602680_±_453e+01(+)|6593800|6600977_±_352e+01(=)|6593900|6600130_±_458e+01|
|X-n393-k38|**38260.00**|.<br>38260.00|. .<br>38278.53_±_2.56e+01(=)|.<br>38260.00|. .<br>38278.80_±_2.57e+01(=)|.<br>38260.00|. .<br>38286.63_±_3.17e+01|
|X-n401-k29<br>|**66154.00**<br>|66180.00<br>|66211.23_±_1.17e+01(-)<br>|66174.00<br>|66214.43_±_1.88e+01(=)<br>|66193.00<br>|66219.57_±_1.15e+01<br>|
|X-n411-k19|**19712.00**|19716.00|19729.60_±_1.04e+01(=)|19716.00|19733.90_±_1.48e+01(=)|19716.00|19731.37_±_1.03e+01|
|X-n420-k130|**10779800**|10779800|<br>10782270_±_192e+01(=)|10779800|<br>10782987_±_270e+01(=)|10779800|10782203_±_219e+01|
|X-n429-k61|**.**<br>**65449.00**|.<br>65457.00|. .<br>65527.70_±_4.22e+01(=)|.<br>65470.00|. .<br>65532.50_±_3.49e+01(=)|.<br>65462.00|. .<br>65525.10_±_2.95e+01|
|X-n439-k37|**36391.00**|36395.00|36403.23_±_6.63e+00(=)|36395.00|36404.03_±_9.22e+00(=)|36394.00|36402.87_±_1.06e+01|
|X-n449-k29|**55233.00**|55234.00|55293.47_±_3.75e+01(=)|55239.00|55308.43_±_3.38e+01(=)|55237.00|55304.70_±_3.71e+01|
|X-n459-k26|**24139.00**|24142.00|<br>24170.43_±_1.29e+01(+)|24142.00|<br>24171.60_±_1.42e+01(+)|24139.00|24162.80_±_1.51e+01|
|X-n469-k138|**221824.00**|221861.00|222014.73_±_9.90e+01(=)|221835.00|222023.70_±_7.35e+01(=)|221861.00|222033.07_±_8.05e+01|
|X-n480-k70|**89449.00**|89449.00|<br>89460.83_±_7.82e+00(-)|89457.00|<br>89467.83_±_1.57e+01(=)|89449.00|<br>89469.03_±_1.78e+01|
|X-n491-k59|**66483.00**|66487.00|<br>66564.93_±_5.18e+01(=)|66506.00|<br>66568.50_±_5.12e+01(=)|66485.00|66576.70_±_6.02e+01|
|X-n502-k39|**69226.00**|69226.00|<br>69236.90_±_9.02e+00(=)|69226.00|<br>69235.43_±_7.66e+00(=)|69226.00|69234.90_±_8.32e+00|
|X-n513-k21<br>|**24201.00**<br>|24201.00<br>|24227.67_±_3.01e+01(+)<br>|24201.00<br>|24218.73_±_2.55e+01(=)<br>|24201.00<br>|24209.27_±_1.70e+01<br>|
|X-n524-k153|**154593.00**|154604.00|154635.57_±_4.78e+01(=)|154598.00|154627.20_±_4.28e+01(=)|154599.00|154641.57_±_5.87e+01|
|X-n536-k96|**9484600**|9485100|<br>9492467_±_269e+01(=)|9486900|<br>9492370_±_309e+01(=)|9484500|9492183_±_433e+01|
|X-n548-k50|**.**<br>**86700.00**|.<br>86707.00|. .<br>86731.13_±_1.92e+01(=)|.<br>86704.00|. .<br>86734.13_±_2.30e+01(=)|.<br>86704.00|. .<br>86728.57_±_1.96e+01|
|X-n561-k42|**42717.00**|42719.00|<br>42762.10_±_2.94e+01(=)|42723.00|<br>42752.13_±_2.34e+01(=)|42719.00|42750.00_±_1.87e+01|
|X-n573-k30|**50673.00**|50720.00|50736.63_±_1.21e+01(+)|50719.00|50730.10_±_9.03e+00(=)|50720.00|50730.50_±_9.07e+00|
|X-n586-k159|**190316.00**|190316.00|<br>190401.73_±_4.87e+01(=)|190316.00|<br>190396.70_±_4.54e+01(=)|190316.00|190393.37_±_4.12e+01|
|X-n599-k92|**108451.00**|108482.00|108571.67_±_4.99e+01(=)|108507.00|108589.93_±_4.93e+01(=)|108484.00|108568.53_±_5.41e+01|
|X-n613-k62|**59535.00**|59536.00|<br>59592.53_±_4.41e+01(=)|59538.00|<br>59604.23_±_3.72e+01(=)|59536.00|59610.93_±_4.56e+01|
|X-n627-k43|**62164.00**|62176.00|62199.40_±_1.70e+01(=)|62179.00|62205.80_±_2.68e+01(=)|62175.00|62210.03_±_2.64e+01|
|X-n641-k35|**63684.00**|63710.00|<br>63760.53_±_2.82e+01(=)|63696.00|<br>63766.53_±_3.68e+01(=)|63705.00|<br>63768.23_±_3.78e+01|
|X-n655-k131|**106780.00**|10678000|10678940_±_842e+00(=)|10678000|10679353_±_914e+00(=)|10678000|10679010_±_982e+00|
|X-n670-k130|**146332.00**|.<br>146432.00|. .<br>146781.10_±_1.39e+02(=)|.<br>146439.00|. .<br>146806.97_±_1.88e+02(=)|.<br>146459.00|. .<br>146810.20_±_1.46e+02|
|X-n685-k75<br>X-n701-k44|**68205.00**<br>**81923.00**|68226.00<br>81941.00|68272.83_±_3.15e+01(=)<br>81983.03_±_3.65e+01(=)|68231.00<br>81942.00|68293.23_±_4.44e+01(=)<br>81985.30_±_3.38e+01(=)|68227.00<br>81931.00|68290.90_±_3.92e+01<br>81984.33_±_4.78e+01|
|X-n716-k35|**4337300**|4337200|<br>4339883_±_223e+01(=)|4337200|<br>4338433_±_107e+01(=)|4337100|4339287_±_216e+01|
|X-n733-k159|**.**<br>**136187.00**|.<br>136216.00|. .<br>136277.20_±_3.43e+01(=)|.<br>136217.00|. .<br>136274.33_±_3.59e+01(=)|.<br>136211.00|. .<br>136281.13_±_4.26e+01|
|X-n749-k98|**77269.00**|77323.00|<br>77421.07_±_4.64e+01(=)|77334.00|<br>77415.73_±_5.31e+01(=)|77335.00|77405.43_±_4.56e+01|
|X-n766-k71|**114417.00**|114419.00|114473.03_±_6.60e+01(=)|114425.00|114466.30_±_3.58e+01(=)|114426.00|114466.90_±_3.49e+01|
|X83k48|**7238600**|241100|<br>2450_±_46501|241100|<br>24430_±_43401|24200|24804_±_38301|
|-n7-<br>X-n801-k40|**.**<br>73311.00|7.<br>**73310.00**|779. .e+(=)<br>73350.60_±_3.34e+01(=)|7.<br>73310.00|79. .e+(=)<br>73361.07_±_3.46e+01(=)|77.<br>73311.00|7.7 .e+<br>73369.70_±_3.91e+01|
|X-n819-k171|**158121.00**|158215.00|<br>158262.53_±_3.79e+01(=)|158180.00|<br>158245.73_±_3.79e+01(=)|158176.00|<br>158247.03_±_3.18e+01|
|X-n837-k142<br>|**193737.00**<br>|193737.00<br>|193800.50_±_3.56e+01(=)<br>|193760.00<br>|193820.13_±_4.37e+01(=)<br>|193764.00<br>|193816.50_±_3.34e+01<br>|
|X-n856-k95<br>X-n876-k59|**88965.00**<br>**9929900**|88966.00<br>9935900|89017.53_±_3.00e+01(=)<br>9943270_±_358e+01(=)|88966.00<br>9934700|89015.40_±_2.60e+01(=)<br>9941393_±_375e+01(-)|88966.00<br>9934700|89014.13_±_2.75e+01<br>9944203_±_433e+01|
|X-n895-k37|**.**<br>**53860.00**|.<br>53871.00|. .<br>53968.13_±_6.39e+01(+)|.<br>53861.00|. .<br>53960.70_±_5.41e+01(+)|.<br>53860.00|. .<br>53931.33_±_4.13e+01|
|X-n916-k207|**32917900**|32921900|32929743_±_520e+01(=)|32921700|32928940_±_511e+01(=)|32923000|32929747_±_459e+01|
|X-n936-k151|**.**<br>**132715.00**|.<br>132809.00|. .<br>133000.43_±_5.70e+01(=)|.<br>132900.00|. .<br>132991.07_±_4.38e+01(=)|.<br>132880.00|. .<br>132983.83_±_4.63e+01|
|X-n957-k87|**8546500**|8546500|<br>8549790_±_187e+01(=)|8546700|<br>8550503_±_239e+01(=)|8546900|8549570_±_208e+01|
|X-n979-k58|**.**<br>118976.00|.<br>**118973.00**|. .<br>118999.50_±_2.00e+01(=)|.<br>118974.00|. .<br>119011.83_±_3.16e+01(=)|.<br>118975.00|. .<br>119005.67_±_2.12e+01|
|X-n1001-k43|72355.00|**72353.00**|<br>72434.37_±_4.49e+01(=)|72376.00|<br>72437.80_±_4.03e+01(=)|72368.00|72426.93_±_3.94e+01|
|Average||0.0113|0.0678 (7/3/90)|0.0145|0.0686 (2/3/95)|0.0135|0.0672|



Table 6: Comparison of Results on Moderate-Scale Instances Among the Top-3 Designed Heuristics – continue. 

24 

## **E New BKS Results** 

In this section, we present the new best-known solutions (BKS) achieved by our designed heuristics. For large-scale instances, the new BKS is obtained in 10 _∗ n_ seconds, where _n_ is the number of nodes. For moderate-scale instances, the BKS is achieved in 3 _∗ n_ seconds. First, we present the convergence curves and corresponding solution quality in section E.1. Then, we detail the routes of these solutions in section E.2. 

### **E.1 Convergence Curves and New Best-Known Solutions** 



Figure 16: Convergence curves of the new best-known solutions. The x-axis represents the CPU time percentage, while the y-axis shows log(1 + Gap%). The red dashed line indicates the baseline (gap = 0%). 

Figure 16 illustrates the convergence curves of the new BKS achieved by our designed heuristics. Specifically, we obtain **1 new BKS** for the moderate-scale instance and **8 out of 10 new BKS** for large-scale instances. 

For the moderate-scale instance X-n1001-k43, our method demonstrated consistent improvements throughout the optimization process, ultimately achieving a final result of 72353, matching the baseline but with slight refinements. 

In large-scale instances, our method consistently outperformed the baseline, achieving new BKS for Antwerp1, Antwerp2, Brussels1, Brussels2, Flanders1, Flanders2, Ghent1, and Leuven2. The convergence curves reveal a trend of rapid improvement during the early stages of optimization, followed by steady refinements in later stages. Notably, the final gaps achieved by our method were consistently close to 0.25% for Brussels2 and Flanders2, representing significant improvements over the baseline. 

For Antwerp1, Antwerp2, Flanders1, Ghent1, and Leuven2, the gap reduced sharply within the first 50% of CPU time, eventually converging to slightly better results than the baseline. A zoom-in box highlights the changes exceeding the baseline for clarity. For Brussels1, the final improvement was approximately 0.1%. 

We also provide a detailed visualization of the specific routes for each new best-known solution, as shown in Figure 17. 

25 



Figure 17: Visualization of the vehicle routes for the new best-known solutions. 

### **E.2 New BKS Routes** 

In this subsection, we provide the detailed routes for each new best-known solution. For a comprehensive overview, the complete route details can be found in the supplementary material. 

## **F License for Used Resources** 

Table 7: List of licenses for the codes and datasets we used in this work 

|Resource|Type|Link|License|
|---|---|---|---|
|HGS [4]|Code|`https://github.com/chkwon/PyHygese`|MIT License|
|AILS-II [20]|Code|`https://github.com/vinymax10/AILS-CVRP`|MIT License|
|CVRPLIB Moderate-scale [11]|Dataset|`http://vrp.galgos.inf.puc-rio.br/index.php/en/`|Available for academic research use|
|CVRPLIB Large-scale [10]|Dataset|`http://vrp.galgos.inf.puc-rio.br/index.php/en/`|Available for academic research use|



We list the used existing codes and datasets in 7, and all of them are open-sourced resources for academic usage. 

## **G Broader Impacts** 

This paper presents work whose goal is to advance the CVRP solver based on LLM. We believe the proposed AILS-AHD framework is valuable for promoting the further development of the field, such as improved efficiency in solving large-scale CVRP instances. This work can inspire follow-up 

26 

works to explore more efficient LLM-driven methods for enhancing the solvers for routing problems. The proposed method has no potential negative societal impacts that we feel must be specifically highlighted. 

27 

## **References** 

- [1] Grigorios D Konstantakopoulos, Sotiris P Gayialis, and Evripidis P Kechagias. Vehicle routing problem and related algorithms for logistics distribution: A literature review and classification. _Operational research_ , 22(3):2033–2062, 2022. 

- [2] Roberto Baldacci, Enrico Bartolini, Aristide Mingozzi, and Roberto Roberti. An exact solution framework for a broad class of vehicle routing problems. _Computational Management Science_ , 7:229–268, 2010. 

- [3] Gilbert Laporte. The vehicle routing problem: An overview of exact and approximate algorithms. _European journal of operational research_ , 59(3):345–358, 1992. 

- [4] Thibaut Vidal. Hybrid genetic search for the cvrp: Open-source implementation and swap* neighborhood. _Computers & Operations Research_ , 140:105643, 2022. 

- [5] Jan Christiaens and Greet Vanden Berghe. Slack induction by string removals for vehicle routing problems. _Transportation Science_ , 54(2):417–433, 2020. 

- [6] Luca Accorsi and Daniele Vigo. A fast and scalable heuristic for the solution of large-scale capacitated vehicle routing problems. _Transportation Science_ , 55(4):832–856, 2021. 

- [7] Shervin Minaee, Tomas Mikolov, Narjes Nikzad, Meysam Chenaghlu, Richard Socher, Xavier Amatriain, and Jianfeng Gao. Large language models: A survey. _arXiv preprint arXiv:2402.06196_ , 2024. 

- [8] Bernardino Romera-Paredes, Mohammadamin Barekatain, Alexander Novikov, Matej Balog, M Pawan Kumar, Emilien Dupont, Francisco JR Ruiz, Jordan S Ellenberg, Pengming Wang, Omar Fawzi, et al. Mathematical discoveries from program search with large language models. _Nature_ , 625(7995):468–475, 2024. 

- [9] Xia Jiang, Yaoxin Wu, Yuan Wang, and Yingqian Zhang. Unco: Towards unifying neural combinatorial optimization through large language model. _arXiv preprint arXiv:2408.12214_ , 2024. 

- [10] Florian Arnold, Michel Gendreau, and Kenneth Sörensen. Efficiently solving very large-scale routing problems. _Computers & operations research_ , 107:32–42, 2019. 

- [11] Eduardo Uchoa, Diego Pecin, Artur Pessoa, Marcus Poggi, Thibaut Vidal, and Anand Subramanian. New benchmark instances for the capacitated vehicle routing problem. _European Journal of Operational Research_ , 257(3):845–858, 2017. 

- [12] Stephen Boyd and Jacob Mattingley. Branch and bound methods. _Notes for EE364b, Stanford University_ , 2006:07, 2007. 

- [13] Vinícius R Máximo, Jean-François Cordeau, and Mariá CV Nascimento. An adaptive iterated local search heuristic for the heterogeneous fleet vehicle routing problem. _Computers & Operations Research_ , 148: 105954, 2022. 

- [14] Gerhard Schrimpf, Johannes Schneider, Hermann Stamm-Wilbrandt, and Gunter Dueck. Record breaking optimization results using the ruin and recreate principle. _Journal of Computational Physics_ , 159(2): 139–171, 2000. 

- [15] Ibrahim Hassan Osman. Metastrategy simulated annealing and tabu search algorithms for the vehicle routing problem. _Annals of operations research_ , 41:421–451, 1993. 

- [16] Jean-Yves Potvin and Jean-Marc Rousseau. An exchange heuristic for routeing problems with time windows. _Journal of the Operational Research Society_ , 46(12):1433–1446, 1995. 

- [17] Ibrahim Hassan Osman. Metastrategy simulated annealing and tabu search algorithms for the vehicle routing problem. _Annals of operations research_ , 41:421–451, 1993. 

- [18] Shen Lin. Computer solutions of the traveling salesman problem. _Bell System Technical Journal_ , 44(10): 2245–2269, 1965. 

- [19] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia, Ed Chi, Quoc V Le, Denny Zhou, et al. Chain-of-thought prompting elicits reasoning in large language models. _Advances in neural information processing systems_ , 35:24824–24837, 2022. 

- [20] Vinícius R Máximo, Jean-François Cordeau, and Mariá CV Nascimento. Ails-ii: An adaptive iterated local search heuristic for the large-scale capacitated vehicle routing problem. _INFORMS Journal on Computing_ , 36(4):974–986, 2024. 

- [21] Anand Subramanian, Eduardo Uchoa, and Luiz Satoru Ochi. A hybrid algorithm for a class of vehicle routing problems. _Computers & Operations Research_ , 40(10):2519–2531, 2013. 

- [22] Vinícius R Máximo and Mariá CV Nascimento. A hybrid adaptive iterated local search with diversification control to the capacitated vehicle routing problem. _European Journal of Operational Research_ , 294(3): 1108–1119, 2021. 

28 

- [23] Thibaut Vidal, Teodor Gabriel Crainic, Michel Gendreau, and Christian Prins. A unified solution framework for multi-attribute vehicle routing problems. _European Journal of Operational Research_ , 234(3):658–673, 2014. 

- [24] Agoston E Eiben and Jim Smith. From evolutionary computation to the evolution of things. _Nature_ , 521 (7553):476–482, 2015. 

- [25] Elliot Meyerson, Mark J Nelson, Herbie Bradley, Adam Gaier, Arash Moradi, Amy K Hoover, and Joel Lehman. Language model crossover: Variation through few-shot prompting. _ACM Transactions on Evolutionary Learning_ , 4(4):1–40, 2024. 

- [26] Joel Lehman, Jonathan Gordon, Shawn Jain, Kamal Ndousse, Cathy Yeh, and Kenneth O Stanley. Evolution through large models. In _Handbook of Evolutionary Machine Learning_ , pages 331–366. Springer, 2023. 

- [27] Haoran Ye, Jiarui Wang, Zhiguang Cao, and Guojie Song. Reevo: Large language models as hyperheuristics with reflective evolution. _arXiv preprint arXiv:2402.01145_ , 2024. 

- [28] Fei Liu, Tong Xialiang, Mingxuan Yuan, Xi Lin, Fu Luo, Zhenkun Wang, Zhichao Lu, and Qingfu Zhang. Evolution of heuristics: Towards efficient automatic algorithm design using large language model. In _Forty-first International Conference on Machine Learning_ , 2024. 

29 

