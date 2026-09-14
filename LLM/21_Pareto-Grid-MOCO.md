# **Pareto-Grid-Guided Large Language Models for Fast and High-Quality Heuristics Design in Multi-Objective Combinatorial Optimization** 

**Minh Hieu Ha**<sup>1*</sup> **, Hung Phan**<sup>1*</sup> **, Tung Duy Doan**<sup>1</sup> **, Tung Dao**<sup>1</sup> **, Dao Tran**<sup>2</sup> **, Huynh Thi Thanh Binh**<sup>1</sup> 

1Hanoi University of Science and Technology, Vietnam 

2FPT Software AI Center, Vietnam 

_{_ hieu.hm220026, hung.pd214903, tung.dd224906, tung.dv242050M _}_ @sis.hust.edu.vn, daotc2@fpt.com, binhht@soict.hust.edu.vn 

#### **Abstract** 

Multi-objective combinatorial optimization problems (MOCOP) frequently arise in practical applications that require the simultaneous optimization of conflicting objectives. Although traditional evolutionary algorithms can be effective, they typically depend on domain knowledge and repeated parameter tuning, limiting flexibility when applied to unseen MOCOP instances. Recently, integration of Large Language Models (LLMs) into evolutionary computation has opened new avenues for automatic heuristic generation, using their advanced language understanding and code synthesis capabilities. Nevertheless, most existing approaches predominantly focus on single-objective tasks, often neglecting key considerations such as runtime efficiency and heuristic diversity in multi-objective settings. To bridge this gap, we introduce **<u>M</u>** <u>ulti-heuristics for MOCOP via</u> **<u>Pa</u>** <u>reto-</u> **<u>G</u>** rid-guided **<u>E</u>** <u>volution</u> of LLMs (MPaGE), a novel enhancement of the Simple Evolutionary Multiobjective Optimization (SEMO) framework that leverages LLMs and Pareto Front Grid (PFG) technique. By partitioning the objective space into grids and retaining top-performing candidates to guide heuristic generation, MPaGE utilizes LLMs to prioritize heuristics with semantically distinct logical structures during variation, thus promoting diversity and mitigating redundancy within the population. Through extensive evaluations, MPaGE demonstrates superior performance over existing LLM-based frameworks, and achieves competitive results to traditional Multiobjective evolutionary algorithms (MOEAs), with significantly faster runtime. Our code is available at https://github. com/langkhachhoha/MPaGE. 

## **1 Introduction** 

Multi-objective combinatorial optimization problems (MOCOP) commonly arise in real-world applications such as vehicle routing, production planning, where multiple conflicting objectives must be optimized simultaneously over a large, discrete solution space (T¨urkyılmaz et al. 2020; Liu et al. 2020; Phan Duc et al. 2025). Unlike single-objective optimization, MOCOP aims to approximate the Pareto front, which captures trade-offs among non-dominated solutions. 

Due to the NP-hard nature of these problems, exact algorithms are often impractical, resulting in the widespread 

*Equal contribution. Copyright © 2026. All rights reserved. 

use of heuristic and metaheuristic methods such as NSGAII, MOEA/D, and MOEA/D-DE (Deb et al. 2002; Zhang and Li 2007a; Li and Zhang 2008). Despite their success, these methods typically rely on domain-specific knowledge and extensive iterative search. Several neural approaches have been proposed for MOCOP, aiming to automatically learn heuristics and improve adaptability (Zhang et al. 2022; Hieu et al. 2024; Fan et al. 2024). However, these methods often require retraining for different problem sizes, demand substantial computational resources, and struggle to generalize to problems with unseen input formats. 

Recently, Large Language Models (LLMs) have shown strong capabilities in automatic heuristic design, offering a new paradigm for optimization algorithm development (Wu et al. 2024; Liu et al. 2025; Novikov et al. 2025). By leveraging their language understanding and code generation abilities, LLMs can produce heuristics and the corresponding implementations with minimal human intervention. Recent approaches integrate LLMs with evolutionary strategies to iteratively evolve effective problem-solving programs (Liu et al. 2024; Ye et al. 2024; Romera-Paredes et al. 2024a; van Stein and B¨ack 2024). While achieving competitive performance and often surpassing traditional methods, most existing LLM-based evolution frameworks primarily target single-objective problems, with limited exploration of their applicability to multi-objective settings. The inherent complexity and trade-off structure of MOCOP introduce significant challenges that require tailored and robust design strategies. To address this, Huang et al. (Huang, Zhang, and Liu 2025) propose an LLM-based framework for discovering and refining evolutionary operators suited to diverse MOCOP. However, runtime efficiency, which is crucial for the real-world deployment of MOCOP solvers, remains an underexplored aspect of LLM-driven heuristic design. MEoH (Yao, Chen, and Wang 2025) considers both optimality and efficiency within a multi-objective evolutionary framework. Additionally, prior LLM-based methods tend to produce populations of algorithms with similar operational logic and slight representation difference, limiting both population diversity and the creativity of LLMs. 

To address the aforementioned issues, we propose MPaGE, a novel framework designed to solve MOCOP while simultaneously discovering a pareto front of LLMgenerated heuristics that jointly optimize solution quality 

and runtime efficiency, with an explicit emphasis on promoting heuristic diversity. Our approach curates heuristic algorithms for the Simple Evolutionary Multiobjective Optimization (SEMO) paradigm, leveraging Pareto Front Grid (PFG) to guide the design of LLM-based variation heuristics by partitioning the objective space into grids, retaining leading individuals from promising regions, and enhancing both solution quality and search efficiency. From these regions, MPaGE builds a pool of elitist candidates and employs LLMs to assess their semantic structures, clustering them into groups of similar logic. Variation is then performed with respect to these clusters, promoting semantic diversity and mitigating redundancy within the heuristic population. To the best of our knowledge, this is the first comprehensive evaluation of LLM-generated heuristics on standard MOCOP, addressing both solution quality, computational efficiency and semantic diversity. Our main contributions are as follows: 

- We introduce MPaGE, the first framework to systematically combine LLMs with the SEMO paradigm and PFG, aiming to solve MOCOP by jointly optimizing runtime, solution quality, and maintaining semantic diversity. 

- We leverage LLMs to verify the logical structure of heuristics and perform cross-cluster recombination, thereby enhancing diversity and reducing redundancy through logically dissimilar variations. 

- We conduct extensive experiments on standard MOCOP benchmarks, demonstrating consistent improvements in runtime efficiency, solution quality, and semantic diversity over LLM-based baselines and traditional MOEAs. 

## **2 Related Works** 

### **2.1 Multi-objective Optimization Algorithms** 

Solving MOCOP often involves extending metaheuristics to handle multiple objectives in discrete domains. NSGA-II (Deb et al. 2002) and MOEA/D (Zhang and Li 2007a) remain popular for effectively maintaining Pareto front diversity. Local search techniques like Pareto Local Search (PLS) (Paquete and St¨utzle 2004), SEMO (Laumanns, Thiele, and Zitzler 2004) improve exploitation by iteratively exploring non-dominated neighbors. More recent neural approaches aim to learn the entire Pareto set, as in PMOCO (Lin, Yang, and Zhang 2022), or boost diversity through dual mechanisms, as in NHDE (Chen et al. 2023b). Despite their success in solving MOCOP, these methods still rely on handcrafted components, struggle to generalize across diverse problem settings, and incur substantial computational costs. 

### **2.2 LLMs for Heuristic Design** 

LLMs are increasingly used to automate heuristic design in combinatorial optimization. Core approaches like EoH, AEL, and FunSearch employ evolutionary frameworks to generate, combine, and refine heuristics in natural language or code, outperforming traditional methods on TSP, bin packing, and scheduling tasks (Liu et al. 2024, 2023; Romera-Paredes et al. 2024b). Similarly, HSEvo incorporates harmony search principles into the LLM-driven generation process to promote diversity and adaptability in solutions (Dat, Doan, and Binh 2025). Other work combines 

LLMs with synthesis techniques like MCTS for guided search (Zheng et al. 2025). While promising, most of these methods primarily focus on single-objective tasks, with limited attention to MOCOP, neglects other practical criteria like efficiency and complexity (Gutjahr 2012). 

### **2.3 Multi-Objective Optimization with LLMs** 

Recent LLM-based heuristics have been applied to metaheuristic design. Huang et al. (Huang, Zhang, and Liu 2025) used LLMs to generate crossover and mutation operators for multi-objective optimization, later extending this to evolutionary multitasking with LLM-designed knowledge transfer models (Huang et al. 2024). Nevertheless, these methods overlook the computational cost of generating and evaluating heuristics, a key challenge in MOEAs. MEoH, REMoH (Yao, Chen, and Wang 2025; Forni´es-Tabuenca et al. 2025) present a multi-objective evolutionary framework that optimizes multiple performance metrics, such as optimality and efficiency, to discover trade-off algorithms in a single run. However, they struggle to distinguish heuristics with similar logic but different implementations, reducing diversity on the pareto front and hindering multi-objective exploration. 

## **3 Preliminary** 

### **3.1 Multi-Objective Combinatorial Optimization** 

Generally, we consider MOCOP defined as: = min _x∈X f_ ( _x_ ) ( _f_ 1( _x_ ) _, . . . , fM_ ( _x_ )) _,_ where _X_ is a finite or discrete feasible set, and _f_ : _X →_ R<sup>_M_</sup> maps each solution to _M_ objectives to be minimized. Trade-offs among objectives are characterized by Pareto optimality, as defined below, and solution quality is commonly assessed using the hypervolume (HV) indicator (Zitzler and Thiele 1999). **Definition 1 (Pareto dominance).** For solutions _x_<sup>_a_</sup> _, x_<sup>_b_</sup> _∈ X_ , _x_<sup>_a_</sup> dominates _x_<sup>_b_</sup> , denoted _x_<sup>_a_</sup> _≺ x_<sup>_b_</sup> , if _fi_ ( _x_<sup>_a_</sup> ) _≤ fi_ ( _x_<sup>_b_</sup> ) for all _i ∈{_ 1 _, . . . , M }_ , and there exists some _j_ such that _fj_ ( _x_<sup>_a_</sup> ) _< fj_ ( _x_<sup>_b_</sup> ). 

**Definition 2 (Pareto optimality).** A solution _x_<sup>_∗_</sup> _∈X_ is Pareto optimal if no _x ∈X_ satisfies _x ≺ x_<sup>_∗_</sup> . The set of all such solutions forms the Pareto set (PS), and Pareto front PF = _{f_ ( _x_ ) _| x ∈_ PS _}_ . 

### **3.2 Simple Evolutionary Multiobjective Optimization** 

Simple Evolutionary Multiobjective Optimization (SEMO) is a minimalist yet effective MOEAs, widely used in theoretical analyses of runtime performance (Laumanns, Thiele, and Zitzler 2004). Similar to Pareto Local Search (PLS) (Paquete and St¨utzle 2004), SEMO maintains an archive of nondominated solutions. As shown in Algorithm 1, each iteration selects a random solution from the archive, explores one of its neighbors, and updates the archive if a new nondominated solution is discovered. Unlike PLS, which evaluates all neighbors, SEMO samples only one neighbor per iteration, which may limit its anytime performance. See appendix B for detailed insights compared to other frameworks. 

## **4 Methodology** 

### **4.1 Problem Formulation** 

We formalize heuristics design for MOCOP as a Language Multi-Criteria Heuristic Design (LMHD) problem, aiming 



<!-- Start of picture text -->
Iteration<br>Selection SelectionReflection < / > ...<br>Population Management<br>Heuristics Heuristics code<br>...<br>< / > ... < / > 💡 < / > ...<br>... Offsprings<br>< / > ... Effectiveness PopulationHeuristics<br>< / > ... Review Crossover and Mutation < / > ...<br>Decomposition ... LLM<br>...<br>< / > ... 💡 < / > ... < / > 💡<br>... ... < / > ... < / > ... < / > ... ... Feedback<br>< / > ... 💡 < / > ... ... ... ... ... < / ><br>< / > < / > < / ><br>Flow direction<br>Complexity<br><!-- End of picture text -->

Figure 1: Overview of the proposed method. The heuristics are first represented in a feature space, and then partitioned into grid cells based on their objective values. Potential parent heuristics are then chosen with the assistance of LLM-based review from grids. Crossover and mutation operations are applied, guided by informative feedback from LLM-based reflection to enhance population diversity. Finally, nondominated individuals are retained to form the next generation for the subsequent iteration. 

|**Algorithm 1:**Simple Evolutionary Multiobjective Opti-<br>mization|
|---|
|_s ←rand_<br>_~~g~~eneration_();<br>// Initialize randomly a<br>solution<br>_A ←{s}_;<br>**repeat**|
|_s ←_**_selection_**(_A_);<br>// Random _s_ from _A_|
|_s_<sup>_′ _</sup>_←_**_neighborhood_**<br>**_~~e~~xploration_**(_s_);<br>// Select a<br>neighbor of _s_ randomly|
|**if**∄_a ∈A_:_a ≺s_<sup>_′_</sup> **then**<br>// Check dominance<br>_A ←A ∪{s_<sup>_′_</sup>_} \ {a ∈A | s_<sup>_′ _</sup>_≺a}_;|
|**until**_stop_<br>_~~c~~ondition_();<br>**return**_A_;|



cally, we define: 



where _e_ 1 is the average negative hypervolume across a set of instances, measuring solution quality, and _e_ 2 is the total running time. These two criteria reflect critical trade-offs in real-world applications, where high performance must be balanced with efficiency. Each heuristic _h ∈H_ is a complete algorithm that, given the current population _A_ , returns a new candidate solution _s_<sup>_′_</sup> by internally performing both selection and neighborhood generation, as in Algorithm 1: 



where _S_ denotes the space of feasible solutions. 

to discover heuristics that balance evaluation criteria reflecting various aspects of heuristic behavior, such as effectiveness, efficiency, or generalization across problems. The key components are introduced as follows: 

**Multi-Criteria Evaluation Function.** We define _E_ : _H →_ R<sup>_M_</sup> to evaluate each heuristic _h ∈H_ over _M_ criteria, capturing its expected performance and key behavioral aspects on a given MOCOP. 

**Language Multi-Criteria Heuristic Design.** Language Multi-Criteria Heuristic Design (LMHD) is a variant of hyper-heuristic that leverages LLMs to generate a diverse set of heuristics. The goal is to discover heuristics that balance multiple criteria simultaneously. Given the heuristic space _H_ , the evaluation function _E_ ( _h_ ) = ( _e_ 1( _h_ ) _, e_ 2( _h_ ) _, . . . , eM_ ( _h_ )) assigns to each heuristic _h_ a vector of _M_ criteria to be minimized. The aim is to approximate the Pareto front of nondominated heuristics in _H_ . 

Our goal is to design MOCOP-specific heuristics for the selection and neighborhood exploration steps, corresponding to lines 4 and 5 in Algorithm 1. The proposed LMHD takes problem specifications as input and generates heuristics optimized over two practical and complementary criteria: solution quality and computational efficiency. Specifi- 

### **4.2 Overview** 

MPaGE integrates LLMs into a multi-phase evolutionary framework to design diverse and effective heuristics, as illustrated in Figure 1. The process begins by initializing a population of heuristics tailored for SEMO paradigm. Each heuristic is represented in a feature space defined by solution quality and running time, and the population is progressively refined until the stopping criterion is met, yielding a set of non-dominated heuristics. At each iteration, PFG generates grids that partition the objective space, thereby grouping heuristics into distinct regions (Section 4.3). A pool of elitism heuristics is selected from these grids, and an LLM-based review analyzes the logical semantics of candidate heuristics to cluster them into behaviorally similar groups (Section 4.4). Subsequently, search operators such as crossover and mutation are applied to these clusters, guided by informative feedback from LLM-based reflection, to generate new offspring. These offspring are added to the population, and non-dominated individuals are selected to form the next generation for the subsequent iteration (Section 4.5). 

### **4.3 Pareto Front Grid mechanism** 

Dominance-based approaches like NSGA-II (Deb et al. 2002) and decomposition-based methods such as MOEA/D 

(Zhang and Li 2007b) often struggle to balance convergence and diversity in tracking the true Pareto Fronts, particularly in heuristic design scenarios where objectives like runtime and solution quality exhibit irregular or non-uniform distributions. To address these limitations, we adopt the Pareto Front Grid (PFG) approach (Xu et al. 2023a) to achieve a better balance between convergence and diversity. Guiding the search using leading solutions in PFG helps focus on promising regions, improving solution quality and efficiency while reducing redundancy. 

**PFG Generation:** Motivated by (Xu et al. 2023a), let the objective space be denoted by _Z ⊂_ R<sup>2</sup> . At generation _t_ , let _P_<sup>(</sup><sup>_t_)</sup> = _{E_ ( _hi_ ) _∈_ R<sup>2</sup> _| hi ∈H_<sup>(</sup><sup>_t_)</sup> _}_ be the set of objective vectors of the current population, where each _hi_ is a heuristic algorithm and _H_<sup>(</sup><sup>_t_)</sup> denotes the heuristic space. We define the _ideal_ and _nadir_ points for each objective _j ∈{_ 1 _,_ 2 _}_ as _zj_<sup>_∗_=min</sup> _h∈P_<sup>(</sup><sup>_t_)</sup><sup>_ej_(</sup><sup>_h_)and</sup><sup>_z_</sup> _j_<sup>_n_=max</sup> _h∈P_<sup>(</sup><sup>_t_)</sup><sup>_ej_(</sup><sup>_h_),where</sup> _ej_ ( _h_ ) denotes the _j_ -th objective value of heuristic _h_ . The objective space is scaled via min-max normalization: 



To structure the population in the normalized objective space, we partition [0 _,_ 1]<sup>2</sup> into a grid of cells of side length _δ_ 1 _>_ 0, _δ_ 2 _>_ 0 along each objective axis, respectively, depending on the number of segments along each dimension. For each solution _hi_ , assign its objective vector _E_<sup>˜</sup> ( _hi_ ) to a grid cell _G_ ( _hi_ ) _∈_ N<sup>2</sup> , and define the PFG mapping as: 



This discretization forms a structured grid over the objective space, grouping solutions into distinct regions. We define the following mapping: 



where each cell _g_ contains all solutions whose objective vectors fall within that grid region. For each non-empty cell _g ∈_ dom( _G_ ), retain a representative subset _Rg ⊂G_ ( _g_ ), selected using non-dominated sorting within the cell. The union of all representatives yields the elite set: 



**PFG Selection:** To facilitate reproduction, the population is organized into a grid, where heuristics exhibiting similar running time or solution quality are placed in neighboring cells. This spatial organization encourages crossover between heuristics with related characteristics, promoting the inheritance and refinement of useful traits. 

Selection for mating is performed over a pool _P_ formed using the grid structure of the objective space. With probability _ϵ_ , a group of elitism candidates is selected from a set of adjacent grid cells. Specifically, a grid cell _g_ is randomly sampled, and the pool is formed as the union of _G_ ( _g_ ) and its neighboring cells _G_ ( _g_<sup>_′_</sup> ), where _g_<sup>_′_</sup> denotes the cells adjacent 

to _g_ along both objective axes, as shown in Figure 2. Otherwise, the parents are selected from entire _E_<sup>(</sup><sup>_t_)</sup> . Formally: 



This hybrid strategy balances local exploitation and global exploration, promoting diversity while guiding search toward the Pareto front. See Appendix C for details. 

### **4.4 Semantic clustering** 

Previous methods struggle to maintain effective diversity in multi-objective heuristic design, especially for complex MOCOP. The standard MOEAs relies on Pareto dominance in the objective space _f_ ( _x_ ), which is unreliable due to the stochastic nature of the heuristic performance. MEoH addresses this by introducing a dominance-dissimilarity measure based on Abstract Syntax Trees (ASTs) (Yao, Chen, and Wang 2025; Neamtiu, Foster, and Hicks 2005). However, ASTs fail to capture semantic similarity between heuristics with similar logic but different implementations, resulting in redundant individuals and reduced diversity. To address 



<!-- Start of picture text -->
Review<br>Crossover Probability<br>Searching Semantic cluster 1 2 3 4 5 6<br>< / > 1 - 0.33 0.00 0.33 0.33 0.00<br>Heuristic 6 Heuristic 1 < / > Heuristic 3 < / > 23 0.250.00 0.33- 0.25- 0.000.33 0.250.33 0.250.00<br>Heuristic 2 < / > 4 0.25 0.00 0.25 - 0.25 0.25<br>< / > < / > 5 0.20 0.20 0.20 0.20 - 0.20<br>Heuristic 4 Heuristic 5 6 0.00 0.33 0.00 0.33 0.33 -<br><!-- End of picture text -->

Figure 2: LLM-based review clustering applies elitism heuristics based on semantic similarity and employs a probability matrix to guide variation among clusters. 

these challenges, instead of relying solely on syntactic features, we query LLMs to assess the semantic and behavioral similarity among elite heuristics _P_ = _{h_ 1 _, h_ 2 _, . . . , hn}_ , and group them into coherent clusters as depicted in Figure 2: 



Each cluster _Ci_ contains heuristics whose code segments implement similar underlying logic, despite syntactic or structural differences. This semantic clustering mitigates redundancy and enhances behavioral diversity at a higher abstraction level. During variation, we apply mutation within clusters to explore local variations, and perform crossover across clusters to combine diverse behaviors. Specifically, given a randomly selected cluster _Ci_ and a heuristic _h ∈ Ci_ , the offspring heuristic _o_ is generated as follows: 



More detailed insights can be found in Appendix F. 

### **4.5 Automatic Heuristic generation** 

In this section, we propose the MPaGE framework for automatic heuristic design. Examples of the prompts used at each stage are provided in the Appendix E. 

**Individual Representation.** Following previous works (Liu et al. 2024; Ye et al. 2024), MPaGE encodes each individual as a natural language description and its corresponding code implementation in Python, both generated by LLMs, together with an associated fitness score. The fitness is evaluated over a set of problem-specific instances by measuring both performance and running time. 

**Population initialization.** MPaGE initializes the heuristic population by querying LLMs with prompts that describe the problem and specify the signature of the heuristic function to be discovered. Specifically, each heuristic is tailored for selection mechanisms and neighborhood exploration within the SEMO paradigm, then evaluated on benchmark instances and assigned a fitness score. 

**Selection.** MPaGE partitions the objective space into grid cells to construct an elitism pool (Section 4.3), then clusters the candidates and selects parent pairs based on dissimilarity as detailed in Section 4.4, or sample from the entire population as Equation 7. 

**Feedback reflection.** Feedback reflection enhances heuristic design by providing LLMs with clear, interpretable signals that guide improvement. For each pair of heuristic parents, an LLM-based reflection module analyzes their respective strengths and weaknesses, returning a textual suggestion on how to improve or effectively combine them. 

**Crossover and Mutation.** MPaGE prompts the generator LLM to create an offspring heuristic by recombining or modifying parent elements, guided by reflective feedback. The prompt includes: (i) task specifications, (ii) parent heuristics in code and natural language, (iii) reflection guidance, and (iv) instructions to generate the new heuristic. 

**Population Management.** Offspring are merged into the population, with non-dominated individuals forming the next generation, as defined by Equation 6. The process repeats until the maximum number of iterations is reached. 

## **5 Experiments** 

### **5.1 Experimental Setup** 

**Benchmarks.** We evaluate the proposed MPaGE framework on four widely recognized MOCOP that are extensively investigated in the literature: Bi-TSP, Tri-TSP, BiCVRP, and Bi-KP. Comprehensive descriptions of these problems are provided in Appendix A. 

**Experiment settings.** The generated heuristics are evaluated on 10 instances for each problem, with sizes of 20, 20, 50, and 50 for Bi-TSP, Tri-TSP, Bi-CVRP and Bi-KP, following the setup in (Chen et al. 2023a). The experimental parameters are configured as follows: the number of generations is set to 20, and the population size is 10 for all problems. Each crossover operator selects 2 parent heuristics to generate offspring heuristics. All heuristics are designed and evaluated under the SEMO search paradigm, with a runtime constraint of 2000 iterations and a time limit of 60 seconds. The probabilities _ϵ_ = 0 _._ 9, _γ_ = 0 _._ 3, and the number of 

PFG segments is set to 4. Experiments were conducted on a Mac with an Apple M1 chip and 8 GB RAM. GPT-4o-mini (temperature 0.7) was used as the pre-trained LLM, while GPT-4o was used for assessing and clustering task. 

#### **Performance Metric.** 

**Objectives** To evaluate a heuristic, we consider two objectives, both averaged across instances and minimized simultaneously: 1) _Negative Hypervolume (NHV)_ : Minimizing the negative hypervolume guides the search toward high-quality solutions. 2) _Running Time_ : Measures the execution time of the heuristic to encourage efficiency. 

**Metrics** Solution quality is evaluated using the hypervolume (HV) and Inverted Generational Distance (IGD). HV indicates how well the Pareto front is approximated (higher is better), while IGD measures proximity and distribution relative to a reference front. Specifically, when comparing LLM-based methods, HV captures overall performance, as each heuristic is evaluated by NHV and execution time; for MOEAs, it reflects final solution quality. In term of diversity measurement, we use the Shannon-Wiener Diversity Index (SWDI) and Cumulative Diversity Index (CDI) (Dat, Doan, and Binh 2025). Details are provided in Appendix D. 

**Baseline Methods** For LLM-based automated heuristic design, we compare our method against representative approaches: EoH, MEoH, ReEvo and HSEvo (Liu et al. 2024; Yao, Chen, and Wang 2025; Ye et al. 2024; Dat, Doan, and Binh 2025) and additionally against widely adopted MOEAs, including NSGA-II, MOEA/D, SEMO and PFGMOEA (Deb et al. 2002; Li and Zhang 2008; Xu et al. 2023b; Laumanns, Thiele, and Zitzler 2004). See Appendix B for the full experimental setup and descriptions. 

### **5.2 Experimental Results** 

**Pareto Fronts and Convergence Analysis** As illustrated in Table 1, MPaGE consistently outperforms other LLMbased baselines in both convergence and Pareto front quality across all benchmarks. On Bi-TSP20 and Tri-TSP20, MPaGE achieves the highest HV scores of 0.911 and 0.936, and the lowest IGD scores of 0.010 and 0.050, respectively, indicating faster convergence and superior solution quality. Similar trends are observed on Bi-KP50 and Bi-CVRP50, where MPaGE maintains strong performance. 

Table 1: Results of MPaGE compared to other baselines regarding HV and IGD on four benchmark problems. The best values are highlighted in bold. 

|Method|Bi-T|SP20|Tri-T|SP20|Bi-C|VRP50|Bi-|KP50|
|---|---|---|---|---|---|---|---|---|
||HV↑|IGD↓|HV↑|IGD↓|HV↑|IGD↓|HV↑|IGD↓|
|EoH|0.756|0.117|0.755|0.148|0.957|0.538|0.602|0.363|
|ReEvo|0.541|0.435|0.694|0.547|0.658|0.462|**0.996**|0.138|
|HSEvo|0.557|0.329|0.715|0.308|0.626|0.450|0.730|0.182|
|MEoH|0.724|0.067|0.884|0.114|0.322|0.286|0.748|0.248|
|MPaGE (Ours)|**0.911**|**0.010**|**0.936**|**0.050**|**0.980**|**0.007**|0.932|**0.035**|



In Figures 3a – 3d, the non-dominated heuristics in the final population, along with the corresponding convergence curves of HV and IGD per iteration, illustrate clear differences among methods on Bi-TSP20 and Tri-TSP20, respectively. MPaGE consistently yields a broader and more diverse set of Pareto-optimal solutions, spanning wider regions of the objective space, converges faster and clearly 



<!-- Start of picture text -->
Pareto Front 1.0 HV  0.4 IGD<br>0.5 EoHMEoHMPaGE 0.8 EoHMEoHMPaGE<br>0.4 0.3<br>0.3 0.6<br>0.2<br>0.2 0.4<br>0.1<br>0.1 0.2 EoH<br>MEoH<br>0.0 0.0 MPaGE 0.0<br>0.0 0.2 Negative hypervolume0.4 0.6 0.8 1.0 1 5 Iterations10 15 20 1 5 Iterations10 15 20<br>Figure 3a: Pareto Front of heuristics on Bi-TSP20 Figure 3b: HV and IGD comparison on Bi-TSP20<br>Pareto Front HV  IGD<br>EoH 1.0 EoH<br>0.35 MEoHMPaGE MEoHMPaGE<br>0.30 0.8<br>0.25<br>0.6 0.4<br>0.20<br>0.3<br>0.15 0.4<br>0.2<br>0.10<br>0.05 0.2 EoH MEoH 0.1<br>0.00 0.0 MPaGE 0.0<br>0.0 0.1 Negative hypervolume0.2 0.3 0.4 0.5 1 5 Iterations10 15 20 1 5 Iterations10 15 20<br>Figure 3c: Pareto Front of heuristics on Tri-TSP20 Figure 3d: HV and IGD comparison on Tri-TSP20<br>Pareto Front B i- TSP20 Bi- TS P50<br>0.5 EoHMEoHMPaGE w/o FeedbackMPaGE 109 NSGA-II (HV: 0.6327)MOEA/D (HV: 0.6321)PFG-MOEA (HV: 0.6466)MPaGE (HV: 0.6505) 2220 NSGA-II (HV: 0.5778)MOEA/D (HV: 0.5512)PFG-MOEA (HV: 0.5914)MPaGE (HV: 0.6032)<br>0.4<br>8 18<br>0.3 7 16<br>14<br>0.2 6<br>12<br>0.1 5<br>10<br>4<br>0.0 8<br>0.0 0.2 Negative hypervolume0.4 0.6 0.8 1.0 3 4 5 6 f1 7 8 9 8 10 12 14f1 16 1 8 20<br>Figure 3e: The non-dominated heuristics on Bi-TSP20 Figure 3f: Pareto fronts of benchmark instances, Bi-TSP 20/50<br>Time HV IGD<br>Time HV IGD<br>Time f2 f2<br><!-- End of picture text -->

outperforms other baselines in terms of HV and IGD. In contrast, EoH shows slower HV growth and higher IGD due to its narrow focus on minimizing performance gaps alone. MEoH, while enhancing diversity over EoH, still trails MPaGE in convergence and final quality, likely due to the complexity of MOCOP tasks and the limited impact of its diversity mechanism. 

Table 2: Two top heuristics designed by MEoH and MPaGE. 

|Method|Bi-T|SP20|Tri-T|SP20|Bi-C|VRP50|Bi-|KP50|
|---|---|---|---|---|---|---|---|---|
||HV↑|Time↓|HV↑|Time↓|HV↑|Time↓|HV↑|Time↓|
|MEoH (best)|0.603|3.265|0.410|5.790|0.241|3.383|0.344|4.139|
|MEoH (fast)|0.345|**0.177**|0.403|**5.228**|0.141|0.081|0.349|2.246|
|MPaGE (best)|**0.629**|4.429|**0.478**|8.112|**0.454**|0.191|**0.359**|2.647|
|MPaGE (fast)|0.451|1.304|0.411|7.590|0.151|**0.063**|0.354|**1.367**|



We evaluate the two best-so-far heuristics across multiple benchmark problems (Table 2), each in two configurations: “best” (highest hypervolume) and “fast” (lowest runtime), measured at the final population. Notably, MPaGE discovers heuristics that outperform MEoH in HV. In several cases, its fast variant is quicker and more effective, highlighting MPaGE’s strength in balancing quality and efficiency. 

**In and out-of-distribution size generalization analysis** We evaluate the generalization capability of MPaGE on both in-distribution and out-of-distribution larger instances of BiTSP (20, 50, 100, 150, 200), Tri-TSP (20, 50, 100), and BiKP instances (50, 100, 200), each comprising 10 instances. 

All hyperparameter settings are elaborated in Appendix D. As evidenced in Table 5, MPaGE consistently outperforms baseline methods across various problem settings. While competing approaches suffer significant performance degradation as problem size increases, our method maintains remarkable stability and robustness. For instance, in Bi-TSP 200, MPaGE achieves an IGD of just 0.017, substantially lower than MEoH (0.186) and EoH (0.181), indicating a much closer approximation to the true Pareto front. Similarly, in the more complex Tri-TSP 100, MPaGE attains an IGD of 0.000, whereas MEoH and EoH produce 0.101 and 0.409, respectively, further demonstrating MPaGE’s exceptional solution quality and scalability. 

**Impact of Reflection and Heuristic Diversity** We conducted experiments on the Bi-TSP20 benchmark to assess the effectiveness of our LLM Reflection approach. The results, summarized in Figure 3e and Table 4a, demonstrate the superior performance of MPaGE over baseline methods (EoH and MEoH) in both HV and IGD metrics. Remarkably, even without the reflection-based feedback, MPaGE outperforms all baselines, indicating that it inherently benefits from capturing the correlation among objectives within each grid. When enhanced with the reflection feedbacks, MPaGE exhibits further improvements, achieving the highest HV and the lowest IGD. These findings underscore the 

Table 3: Comparison results across all benchmarks against baselines. The HV and time are averaged over 50 instances. 

|||Bi-TSP2|0||Bi-TSP5|0||Bi-TSP1|00||Tri-TSP2|0||Tri-TSP50|||Tri-TSP1|00|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Method|HV_↑_|Speedup|Time_↓_|HV_↑_|Speedup|Time_↓_|HV_↑_|Speedup|Time_↓_|HV_↑_|Speedup|Time_↓_|HV_↑↑_|Speedup|Time_↓_|HV_↑_|Speedup|Time_↓_|
|NSGA-II|0.603|1.0x|731.2|0.495|1.0x|875.5|0.419|1.0x|932.5|0.451|3.9x|252.446|0.279|1.7x|669.9|0.195|1.5x|830.3|
|MOEA/D|0.597|5.8x|126.644|0.473|5.5x|157.796|0.414|4.0x|240.680|0.365|4.5x|216.485|0.189|3.6x|310.583|0.123|3.1x|398.387|
|PFG-MOEA|0.624|1.2x|617.734|0.532|1.0x|844.914|0.457|1.0x|952.186|0.465|1.0x|984.180|0.289|1.0x|1127.46|0.222|1.0x|1229.857|
|SEMO|0.543|149.4x|4.894|0.284|80.5x|10.878|0.178|56.5x|16.846|0.295|143.0x|6.881|0.108|**84.8x**|13.290|0.065|33.2x|36.994|
|EoH|0.584|52.2x|14.004|0.510|18.5x|47.233|0.503|6.0x|159.156|0.420|108.7x|9.050|0.208|39.7x|28.368|0.107|29.3x|42.038|
|ReEvo|0.623|107.3x|6.812|0.516|86.2x|10.151|0.413|51.0x|18.653|0.427|95.0x|10.361|0.205|41.1x|27.416|0.103|14.8x|83.213|
|HSEvo|0.620|112.3x|6.513|0.519|95.3x|9.182|0.422|54.1x|17.590|0.420|115.6x|8.515|0.218|55.2x|20.435|0.115|20.3x|60.659|
|MEoH (best)|0.603|**224.0x**|3.265|0.480|**126.2x**|6.937|0.395|**79.2x**|12.024|0.410|**170.0x**|5.790|0.205|79.4x|14.197|0.111|**48.8x**|25.213|
|MPaGE (best)|0.629|165.1x|4.429|0.542|126.0x|6.950|0.442|74.9x|12.719|0.478|121.3x|8.112|0.220|76.5x|14.747|0.109|46.6x|26.394|
|Method|HV_↑_|Bi-KP50<br>Speedup|Time_↓_|HV_↑_|Bi-KP10<br>Speedup|0<br>Time_↓_|HV_↑_|Bi-KP20<br>Speedup|0<br>Time_↓_|HV_↑_|Bi-CVRP<br>Speedup|20<br>Time_↓_|HV_↑_|Bi-CVRP5<br>Speedup|0<br>Time_↓_|HV_↑_|Bi-CVRP<br>Speedup|100<br>Time_↓_|
|NSGA-II|0.357|1.0_×_|926.406|0.483|1.0_×_|995.178|0.293|1.0_×_|1176.915|0.573|1.0_×_|1051.192|0.416|1.0_×_|1945.667|0.357|1.0_×_|3433.284|
|MOEA/D|0.358|10.7_×_|86.247|0.484|13.9_×_|71.674|0.286|13.4_×_|87.621|0.568|16.2x|64.698|0.420|23.5x|82.801|0.353|35.7x|96.200|
|PFG-MOEA|0.358|1.9x|488.617|0.484|1.7x|596.989|0.330|2.1x|570.174|0.598|6.6x|159.867|0.435|7.0x|277.464|0.318|9.6x|359.108|
|SEMO|0.195|136.9x|6.766|0.144|529.4x|1.880|0.188|115.0x|10.234|0.518|8342.8x|0.126|0.205|1616.0x|1.204|0.135|944.8x|3.634|
|EoH|0.343|4.9x|187.455|0.463|5.1x|195.414|0.320|18.5x|63.555|0.539|6332.5x|0.166|0.443|6176.7x|0.315|0.369|5731.7x|0.599|
|ReEvo|0.357|**368.1x**|2.517|0.452|432.1x|2.303|0.202|550.2x|2.139|0.511|3822.5x|0.275|0.354|2231.3x|0.872|0.249|2257.3x|1.521|
|HSEvo|0.357|330.5x|2.803|0.450|318.3x|3.127|0.205|456.5x|2.578|0.515|3185.4x|0.330|0.405|1781.7x|1.092|0.305|916.0x|3.748|
|MEoH (best)|0.344|223.8x|4.139|0.464|219.1x|4.543|0.321|275.3x|4.275|0.503|2280.2x|0.461|0.241|575.1x|3.383|0.126|279.3x|12.291|
|MPaGE (best)|0.359|350.0x|2.647|0.486|**535.3x**|1.859|0.197|**555.7x**|2.118|0.568|**14599.9x**|0.072|0.454|**10186.7x**|0.191|0.422|**9563.5x**|0.359|



strength of our approach in promoting both convergence and diversity. To investigate the impact of our approach on population diversity, we evaluate all frameworks using the SWDI and CDI metrics, as depicted in Table 4b. Notably, MPaGE demonstrates significantly better performance compared to the other baselines. Higher SWDI and CDI values indicate more uniform heuristic distribution and greater population diversity, promoting effective exploration. Further analysis is provided in Appendix F. 

**Comparison to Conventional MOEAs** We evaluate the impact of PFG on the optimization process and compare its performance with two well-established MOEAs: NSGA-II (Deb et al. 2002) and MOEA/D (Zhang and Li 2007a). As shown in Table 6, based on experiments conducted on BiTSP problems, MPaGE consistently outperforms the baselines in HV and IGD. These results highlight the effectiveness of the PFG mechanism. By directing the search toward the most promising regions of the objective space, the method enhances both the solution quality and the overall efficiency of the optimization process. 

Table 4: (a) Effects of LLM Reflection Bi-TSP20; (b) Comparison in Shannon–Wiener diversity index (SWDI) and cumulative diversity index (CDI). 

|**Method**|**HV**_↑_|**IGD**_↓_|**Problems**|**Bi T**|**SP**|**Bi CV**|**RP**|
|---|---|---|---|---|---|---|---|
|||||SWDI_↑_|CDI_↑_|SWDI_↑_|CDI_↑_|
|EoH<br>MEoH|0.688<br>0.659|0.141<br>0.122|EoH<br>ReEvo|0.897<br>0.647|1.944<br>2.133|1.168<br>0.943|2.173<br>1.908|
|MPaGE w/o Feedback|0.829|0.077|HSEvo|0.757|1.915|1.102|1.964|
|**MPaGE**|**0.941**|**0.023**|MEoH|0.639<br>|2.086<br>|0.143<br>|2.181<br>|
|(a)|||MPaGE|**1.029**|**2.152**<br>(b)|**1.172**|**2.213**|



**Evaluation Against Baselines** We evaluate the best heuristics generated by MPaGE based on hypervolume performance, against baselines on standard MOCOP benchmarks. As shown in Table 6 and Figure 3f, MPaGE consistently outperforms existing LLM-based heuristics, achieving the highest HV on 9 out of 12 test suites and up to 100 _×_ 

Table 5: Performance comparison in terms of HV and IGD on inand out-of-distribution instances. 

|Problems|E|oH|M|EoH|MP|aGE|
|---|---|---|---|---|---|---|
||HV↑|IGD↓|HV↑|IGD↓|HV↑|IGD↓|
|Bi-TSP 20|0.843|0.100|0.786|**0.045**|**0.918**|0.063|
|Bi-TSP 50|0.293|0.154|0.450|0.113|**0.972**|**0.020**|
|Bi-TSP 100|0.361|0.169|0.364|0.134|**0.937**|**0.026**|
|Bi-TSP 150|0.351|0.216|0.364|0.159|**0.985**|**0.026**|
|Bi-TSP 200|0.341|0.181|0.349|0.186|**0.990**|**0.017**|
|Tri-TSP 20|0.755|0.148|0.884|0.114|**0.936**|**0.050**|
|Tri-TSP 50|0.483|0.379|0.881|0.093|**0.916**|**0.000**|
|Tri-TSP 100|0.447|0.409|0.810|0.101|**0.897**|**0.000**|
|Bi-KP 50|0.695|0.470|0.862|0.061|**0.907**|**0.008**|
|Bi-KP 100|0.751|0.390|0.828|0.243|**0.923**|**0.063**|
|Bi-KP 200|0.316|0.704|0.472|0.192|**0.855**|**0.080**|
|Tab|le 6:Efi<br>|ficiency <br>|of our Pa<br>|reto Fro<br>|nt Grid<br>||
||Bi-T|SP 20|Bi-T|SP 50|Bi-TS|P 100|
|Backbone|||||||
||HV↑|IGD↓|HV↑|IGD↓|HV↑|IGD↓|
|NSGA-II|0.860|0.052|0.801|0.120|0.757|**0.095**|
|MOEA/D|0.819|0.119|0.768|0.108|0.560|0.157|
|PFG (Ours)|**0.913**|**0.024**|**0.836**|**0.075**|**0.844**|0.099|



speedup. Compared to traditional MOEAs, it delivers comparable or better HV on over half of the problems while being up to 14,599 _×_ faster. Although MEoH also offers strong runtime, MPaGE achieves a more balanced trade-off, maintaining high HV even on large instances. For example, on Bi-TSP100 and Bi-CVRP100, it reaches HV of 0.442 and 0.422 while being 46.6 _×_ and 9563.5 _×_ faster than NSGAII. Overall, MPaGE offers a robust set of heuristics balancing optimality and efficiency, making it highly suitable for large-scale combinatorial optimization. 

## **6 Conclusion** 

In this paper, we propose MPaGE, a novel LLM-guided framework for solving MOCOP that simultaneously discov- 

ers a Pareto front of heuristics balancing solution quality, runtime efficiency, and semantic diversity. Integrating LLMs with the SEMO paradigm and introducing the Pareto Front Grid, our approach efficiently partitions the objective space and steers heuristic evolution toward promising regions. By clustering heuristics based on semantic logic and promoting inter-group diversity, the framework ensures meaningful variation within the heuristic population. Empirical results show that MPaGE consistently outperforms prior LLMbased approaches in achieving superior trade-offs across objectives, enhancing heuristic diversity, and reducing computational cost. Furthermore, it outperforms traditional algorithms in efficiency while maintaining comparable solution quality, demonstrating its potential as a scalable and generalizable approach for automated heuristic discovery. 

## **References** 

Chen, J.; Wang, J.; Zhang, Z.; Cao, Z.; Ye, T.; and Chen, S. 2023a. Efficient meta neural heuristic for multi-objective combinatorial optimization. _Advances in Neural Information Processing Systems_ , 36: 56825–56837. 

Chen, J.; Zhang, Z.; Cao, Z.; Wu, Y.; Ma, Y.; Ye, T.; and Wang, J. 2023b. Neural Multi-Objective Combinatorial Optimization with Diversity Enhancement. In _Thirty-seventh Conference on Neural Information Processing Systems_ . 

Coello Coello, C. A.; and Reyes Sierra, M. 2004. A study of the parallelization of a coevolutionary multi-objective evolutionary algorithm. In _MICAI 2004: Advances in Artificial Intelligence: Third Mexican International Conference on Artificial Intelligence, Mexico City, Mexico, April 26-30, 2004. Proceedings 3_ , 688–697. Springer. 

Dat, P. V. T.; Doan, L.; and Binh, H. T. T. 2025. HSEvo: Elevating Automatic Heuristic Design with Diversity-Driven Harmony Search and Genetic Algorithm Using LLMs. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 39, 26931–26938. AAAI Press. 

Deb, K.; Pratap, A.; Agarwal, S.; and Meyarivan, T. 2002. A fast and elitist multiobjective genetic algorithm: NSGAII. _IEEE transactions on evolutionary computation_ , 6(2): 182–197. 

Dubois-Lacoste, J.; L´opez-Ib´a˜nez, M.; and St¨utzle, T. 2015. Anytime Pareto local search. _European journal of operational research_ , 243(2): 369–385. 

Fan, M.; Wu, Y.; Cao, Z.; Song, W.; Sartoretti, G.; Liu, H.; and Wu, G. 2024. Conditional Neural Heuristic for Multiobjective Vehicle Routing Problems. _IEEE transactions on neural networks and learning systems_ , PP. 

Forni´es-Tabuenca, D.; Uribe, A.; Otamendi, U.; Artetxe, A.; Rivera, J. C.; and de Lacalle, O. L. 2025. REMoH: A Reflective Evolution of Multi-objective Heuristics approach via Large Language Models. _arXiv preprint arXiv:2506.07759_ . Gutjahr, W. J. 2012. Runtime analysis of an evolutionary algorithm for stochastic multi-objective combinatorial optimization. _Evolutionary computation_ , 20(3): 395–421. 

Hieu, H. M.; Phan, H.; Tran, D. C.; Van, D. C.; Tung, D. V.; and Binh, H. T. T. 2024. Alimentation Deep Multiple Optimal Ant Colony Optimization to solve Vehicle 

Routing Problem with Time Windows. In _Proceedings of the Genetic and Evolutionary Computation Conference Companion_ , GECCO ’24 Companion, 17–18. New York, NY, USA: Association for Computing Machinery. ISBN 9798400704956. 

Huang, L.; Zhang, M.; and Liu, K. 2025. Autonomous Design of Evolutionary Operators for Multi-Objective Optimization Using Large Language Models. _Artificial Intelligence Journal_ , 300: 50–65. 

Huang, Y.; Lv, X.; Wu, S.; Wu, J.; Feng, L.; and Tan, K. C. 2024. Advancing automated knowledge transfer in evolutionary multitasking via large language models. _arXiv preprint arXiv:2409.04270_ . 

Laumanns, M.; Thiele, L.; and Zitzler, E. 2004. Running time analysis of multiobjective evolutionary algorithms on pseudo-boolean functions. _IEEE Transactions on Evolutionary Computation_ , 8(2): 170–182. 

Li, H.; and Zhang, Q. 2008. Multiobjective optimization problems with complicated Pareto sets, MOEA/D and NSGA-II. _IEEE transactions on evolutionary computation_ , 13(2): 284–302. 

Li, M.; Han, X.; Chu, X.; and Liang, Z. 2024. Empirical Comparison between MOEAs and Local Search on MultiObjective Combinatorial Optimisation Problems. In _Proceedings of the Genetic and Evolutionary Computation Conference_ , GECCO ’24, 547–556. New York, NY, USA: Association for Computing Machinery. ISBN 9798400704949. 

Lin, X.; Yang, Z.; and Zhang, Q. 2022. Pareto Set Learning for Neural Multi-Objective Combinatorial Optimization. In _International Conference on Learning Representations_ . 

Liu, F.; Lin, X.; Yao, S.; Wang, Z.; Tong, X.; Yuan, M.; and Zhang, Q. 2025. Large language model for multiobjective evolutionary optimization. In _International Conference on Evolutionary Multi-Criterion Optimization_ , 178– 191. Springer. 

Liu, F.; Tong, X.; Yuan, M.; Lin, X.; Luo, F.; Wang, Z.; Lu, Z.; and Zhang, Q. 2024. Evolution of Heuristics: Towards Efficient Automatic Algorithm Design Using Large Language Model. _arXiv preprint arXiv:2401.02051_ . 

Liu, F.; Tong, X.; Yuan, M.; and Zhang, Q. 2023. Algorithm evolution using large language model. _arXiv preprint arXiv:2311.15249_ . 

Liu, Q.; Li, X.; Liu, H.; and Guo, Z. 2020. Multi-objective metaheuristics for discrete optimization problems: A review of the state-of-the-art. _Applied Soft Computing_ , 93: 106382. 

Neamtiu, I.; Foster, J. S.; and Hicks, M. 2005. Understanding source code evolution using abstract syntax tree matching. In _Proceedings of the 2005 international workshop on Mining software repositories_ , 1–5. 

Novikov, A.; V˜u, N.; Eisenberger, M.; Dupont, E.; Huang, P.-S.; Wagner, A. Z.; Shirobokov, S.; Kozlovskii, B.; Ruiz, F. J.; Mehrabian, A.; et al. 2025. AlphaEvolve: A coding agent for scientific and algorithmic discovery. _arXiv preprint arXiv:2506.13131_ . 

Paquete, L.; and St¨utzle, T. 2004. Pareto local optimum sets in the biobjective traveling salesman problem: An experimental study. In _Metaheuristics for multiobjective optimisation_ , 177–199. Springer. 

Phan Duc, H.; Bui Trong, D.; Nguyen Thi, T.; and Huynh Thi Thanh, B. 2025. Pareto Front Grid Guided Multiobjective Optimization In Dynamic Pickup And Delivery Problem Considering Two-Sided Fairness. In _Proceedings of the Genetic and Evolutionary Computation Conference_ , GECCO ’25, 277–285. New York, NY, USA: Association for Computing Machinery. ISBN 9798400714658. 

Zheng, Z.; Xie, Z.; Wang, Z.; and Hooi, B. 2025. Monte Carlo Tree Search for Comprehensive Exploration in LLM-Based Automatic Heuristic Design. _arXiv preprint arXiv:2501.08603_ . 

Zitzler, E.; and Thiele, L. 1999. Multiobjective evolutionary algorithms: a comparative case study and the strength Pareto approach. _IEEE transactions on Evolutionary Computation_ , 3(4): 257–271. 

Romera-Paredes, B.; Barekatain, M.; Novikov, A.; Balog, M.; Kumar, M. P.; Dupont, E.; Ruiz, F. J.; Ellenberg, J. S.; Wang, P.; Fawzi, O.; et al. 2024a. Mathematical discoveries from program search with large language models. _Nature_ , 625(7995): 468–475. 

Romera-Paredes, B.; Barekatain, M.; Novikov, A.; Balog, M.; et al. 2024b. Mathematical discoveries from program search with large language models. _Nature_ . 

T¨urkyılmaz, A.; S¸envar, O.;<sup>¨</sup> Unal, I.; and Bulkan, S. 2020. A<sup>¨</sup> research survey: heuristic approaches for solving multi objective flexible job shop problems. _Journal of Intelligent Manufacturing_ , 31(8): 1949–1983. 

van Stein, N.; and B¨ack, T. 2024. Llamea: A large language model evolutionary algorithm for automatically generating metaheuristics. _IEEE Transactions on Evolutionary Computation_ . 

Wu, X.; Wu, S.-h.; Wu, J.; Feng, L.; and Tan, K. C. 2024. Evolutionary computation in the era of large language model: Survey and roadmap. _IEEE Transactions on Evolutionary Computation_ . 

Xu, Y.; Zhang, H.; Huang, L.; Qu, R.; and Nojima, Y. 2023a. A Pareto Front grid guided multi-objective evolutionary algorithm. _Applied Soft Computing_ , 136: 110095. 

Xu, Y.; Zhang, H.; Huang, L.; Qu, R.; and Nojima, Y. 2023b. A Pareto Front grid guided multi-objective evolutionary algorithm. _Applied Soft Computing_ , 136: 110095. 

Yao, M.; Chen, Y.; and Wang, L. 2025. MEoH: Multiobjective Evolution of Heuristics with Large Language Models. In _Proceedings of the 39th AAAI Conference on Artificial Intelligence_ , 1300–1307. AAAI Press. Ye, H.; Wang, J.; Cao, Z.; Berto, F.; Hua, C.; Kim, H.; Park, J.; and Song, G. 2024. Reevo: Large language models as hyper-heuristics with reflective evolution. _arXiv preprint arXiv:2402.01145_ . 

Zhang, Q.; and Li, H. 2007a. MOEA/D: A multiobjective evolutionary algorithm based on decomposition. _IEEE Transactions on evolutionary computation_ , 11(6): 712–731. Zhang, Q.; and Li, H. 2007b. MOEA/D: A multiobjective evolutionary algorithm based on decomposition. _IEEE Transactions on Evolutionary Computation_ , 11(6): 712– 731. 

Zhang, Z.; Wu, Z.; Zhang, H.; and Wang, J. 2022. Metalearning-based deep reinforcement learning for multiobjective optimization problems. _IEEE Transactions on Neural Networks and Learning Systems_ , 34(10): 7978–7991. 

## **Appendix: Table of Contents** 

This is Appendix for “Pareto-Grid-Guided Large Language Models for Fast and High-Quality Heuristics Design in MultiObjective Combinatorial Optimization”. 

|**A**<br>|**Detailed of MOCOP benchmarks** . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 11|
|---|---|
|A.1|Multi-objective traveling salesman problem (MOTSP) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 11|
|A.2|Multi-objective capacitated vehicle routing problem (MOCVRP) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 11|
|A.3|Multi-objective knapsack problem (MOKP) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 11|
|**B**<br>|**Baseline Descriptions** . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 11|
|B.1|LLM-based Baselines . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 11|
|B.2|MOEAs Baselines . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 12|
|B.3|Motivation for Using SEMO as the Underlying Framework . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 13|
|**C**<br>|**Algorithm details** . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 14|
|**D**<br>|**Metric descriptions** . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 16|
|D.1|Hypervolume . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 16|
|D.2|Inverted Generational Distance . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 16|
|D.3|Shannon-Wiener diversity index . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 17|
|D.4|Cummmulative diversity index . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 17|
|**E**<br>|**MPaGE prompt details** . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 18|
|E.1|Task description prompt . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 18|
|E.2|Initialization prompt . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 21|
|E.3|Semantic clustering prompt . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 22|
|E.4|Feedback reflection prompt . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 23|
|E.5|Crossover prompt . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 24|
|**F**<br>|**Clustering variations analysis** . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 26|
|**G**<br>|**Designed Heuristics** . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 30|
|**H**<br>|**Comparison to Neural Combinatorial Optimization** . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 36|



## **A Detailed of MOCOP benchmarks** 

### **A.1 Multi-objective traveling salesman problem (MOTSP)** 

In the multi-objective traveling salesman problem (MOTSP) involving _n_ nodes and _M_ objectives, each node _i ∈{_ 1 _, . . . , n}_ is represented by _M_ sets of 2-dimensional coordinates, one for each objective. For a given objective _m_ , the Euclidean distance _c_<sup>_m_</sup> _ij_ between two nodes _i_ and _j_ is calculated based on their corresponding coordinates. The goal is to construct a tour _π_ that visits every node exactly once and simultaneously minimizes the total travel distance across all _M_ objectives. Formally, the objective vector to minimize is defined as: 



with each component given by: 



Problem instances are synthetically generated by sampling all coordinates independently and uniformly from the [0 _,_ 1]<sup>2</sup><sup>_M_</sup> hypercube. 

### **A.2 Multi-objective capacitated vehicle routing problem (MOCVRP)** 

We focus on the bi-objective capacitated vehicle routing problem (Bi-CVRP), which considers a set of _n_ customer nodes and a single depot. Each node, including the depot, is assigned a location in 2D space, and every customer has a specific demand. A fleet of identical vehicles with uniform capacity is stationed at the depot and must complete routes that collectively serve all customers, returning to the depot afterward. Each vehicle must have sufficient remaining capacity to fulfill the demand of any customer it visits. The problem simultaneously optimizes two conflicting objectives: minimizing the total traveled distance and minimizing the makespan, defined as the length of the longest route. In our Bi-CVRP instances, node coordinates are randomly sampled from the [0 _,_ 1]<sup>2</sup> space, and customer demands are randomly selected from the set _{_ 1 _, . . . ,_ 9 _}_ . The vehicle capacity is set to 30, 40, and 50 for problem sizes where 20 _≤ n <_ 40, 40 _≤ n <_ 70, and 70 _≤ n ≤_ 100, respectively. To standardize inputs, all demand values are normalized with respect to vehicle capacity. 

### **A.3 Multi-objective knapsack problem (MOKP)** 

In the multi-objective knapsack problem (MOKP) with _M_ objectives and _n_ items, each item is characterized by a weight and _M_ distinct profit values, one for each objective. These items can be visualized as nodes within an instance graph. The goal is to select a subset of items such that the total profit across all _M_ objectives is maximized, while the combined weight of the selected items does not exceed a predefined capacity. Formally, let _x ∈{_ 0 _,_ 1 _}_<sup>_n_</sup> be a binary decision vector, where _xi_ = 1 indicates that item _i_ is selected. The problem can be stated as: 



subject to: 



where _wi_ is the weight of item _i_ , and _fm_ ( _x_ ) =<sup>�</sup><sup>_n_</sup> _i_ =1<sup>_p_</sup> _i_<sup>_mxi_represents the total profit for objective</sup><sup>_m_, with</sup><sup>_pm_</sup> _i_<sup>being the profit</sup> of item _i_ under objective _m_ . The instances are generated by independently sampling all weights _wi_ and profits _p_<sup>_m_</sup> _i_ from the uniform distribution over [0 _,_ 1]. The knapsack capacity _C_ is set to 12.5 for 50 _≤ n <_ 100 and 25 for 100 _≤ n ≤_ 200, respectively. 

## **B Baseline Descriptions** 

### **B.1 LLM-based Baselines** 

We compare the Pareto fronts of heuristics generated by MPaGE with those of the following methods: 

- **EoH (Liu et al. 2024)** is a framework that combines large language models and evolutionary computation to automatically design heuristics. It simulates expert reasoning by evolving both code and thought via five tailored prompt strategies. 

- **ReEvo (Ye et al. 2024)** is an evolutionary framework that integrates LLMs with reflective feedback to enhance heuristic generation. 

- **HSEvo (Dat, Doan, and Binh 2025)** is a framework built on harmony search principles, introducing new components and enhancing evolutionary operators to jointly optimize objective performance and solution diversity. 

- **MEoH (Yao, Chen, and Wang 2025)** is an LLM-based framework that formulates heuristic design as a multi-objective optimization problem to generate diverse, non-dominated heuristics in a single run. 

To ensure fairness, experimental parameters follow MPaGE: 20 generations and a population size of 10 across all problems. Each crossover operator selects two parent heuristics to generate offspring. 

### **B.2 MOEAs Baselines** 

For all algorithms, we assume a minimisation problem as: 



where _F_ : _X →_ R<sup>_M_</sup> is vector-valued with mutually conflicting objectives, and Pareto-dominance _⪯_ is defined in the usual way. To benchmark the effectiveness of LLM-generated heuristics in solving multi-objective combinatorial optimization problems, we compare them against three well-established MOEAs and SEMO. These algorithms are representative of different design philosophies in evolutionary multi-objective optimization and are widely used in the literature. 

**NSGA-II (Deb et al. 2002)** NSGA-II maintains a population _Pt_ of fixed size _N_ . It contains components: 

- **Fast non-dominated sorting.** Each solution _x_ is assigned a _rank_ 



where _Fk_ is the _k_ -th non-dominated front. Fronts are constructed iteratively: _F_ 0 contains all non-dominated individuals, _F_ 1 those dominated only by members of _F_ 0, and so on. The total sorting cost is _O_ ( _MN_<sup>2</sup> ) (or _O_ ( _MN_ log _N_ ) with incremental approaches). 

- **Crowding distance.** Within each front _Fr_ , crowding distance is calculated as 



where _x_<sup>prev</sup> and _x_<sup>next</sup> are the nearest neighbours in front _Fr_ along each objective _fm_ , and missing values at boundaries are treated as zero. 

- **Selection and variation.** Binary tournament based on the lexicographic key ( _r_ ( _x_ ) _, −d_ ( _x_ )) chooses parents; simulated binary crossover (SBX) and polynomial mutation create _N_ offspring. 

- **Elitist replacement.** Parents and offspring are merged and the best _N_ solutions under ( _r, −d_ ) are kept, guaranteeing _O_ (1) elitism per generation. The algorithm explicitly balances _convergence_ (via rank) and _diversity_ (via distance) while preserving the worst-case _O_ ( _N_ ) memory footprint. 

**MOEA/D (Zhang and Li 2007b)** MOEA/D decomposes the multi-objective problem into _K_ single-objective _sub-problems_ using a set of weight vectors _{_ **_λ_**<sup>(</sup><sup>_k_)</sup> _}_<sup>_K_</sup> _k_ =1<sup>with</sup><sup>**_λ_**(</sup><sup>_k_)</sup><sup>_∈_∆</sup><sup>_M−_1, where ∆</sup><sup>_M−_1 is the unit simplex.</sup> 

- **Scalarisation.** Typical aggregation functions include: 



where **z**<sup>_∗_</sup> = (min _f_ 1 _, . . . ,_ min _fM_ ) is the _ideal_ point. 

- **Neighbourhood collaboration.** Each sub-problem _k_ is allotted a neighbourhood _Nk_ comprising the _T_ closest weight vectors in Euclidean distance. Variation operators are restricted to parents drawn from _Nk_ , and offspring _x_<sup>_′_</sup> may update the solutions of all neighbours _j ∈Nk_ if _g_ ( _x_<sup>_′_</sup> _|_ **_λ_**<sup>(</sup><sup>_j_)</sup> ) _< g_ ( _x_<sup>(</sup><sup>_j_)</sup> _|_ **_λ_**<sup>(</sup><sup>_j_)</sup> ). 

- The decomposition transforms the _M_ -objective search into parallelised scalar searches of complexity _O_ ( _KT_ ) per generation while implicitly promoting solution diversity through the geometry of _{_ **_λ_**<sup>(</sup><sup>_k_)</sup> _}_ . 

**PFG-MOEA (Xu et al. 2023a)** PFG-MOEA is a recent grid-guided extension of MOEA/D that introduces PFG. 



- **Grid construction.** Given a grid size _G ∈_ N, the _cell index_ of _x_ is 



Only the _leading_ (knee) solution in each occupied cell is retained in an external _PFG archive_ , drastically lowering memory and update costs to _O_ ( _|_ PFG _|_ ), with _|_ PFG _| ≪ N_ for moderate _G_ . 

- **Environmental selection.** At every generation PFG-MOEA: 

- (i) updates **z**<sup>nad</sup> via a statistical estimator using a random sample of the population, and 

- (ii) performs a _grid-based knee-point selection_ : within each **_g_** the solution maximising _κ_ ( _x_ ) =<sup>�</sup> _m_ �� _fm ′_<sup>(</sup><sup>_x_)</sup><sup>_−_</sup> 2<sup><u>1</u></sup> �� is chosen to preserve extreme trade-offs. 

The algorithm then follows MOEA/D-style neighbourhood variation and update, but the decisions are guided by the sparsified PFG archive, yielding superior convergence/diversity on irregular fronts with an empirical time complexity close to _O_ ( _KT_ + _|_ PFG _|_ ) per generation. 

**SEMO (Li et al. 2024)** is a minimalistic (1 + 1) MOEA widely used in theoretical studies. At each step, it selects a random solution from the current archive and applies a simple mutation to generate one neighbor. The new solution is added to the archive if it is not dominated, while any dominated solutions are removed. Its key strength lies in its simplicity and efficiency in exploring the Pareto front through fast, randomized local search, making it especially effective on discrete and combinatorial problems. 

To ensure a fair and controlled comparison, all algorithms are configured with a population size of 300 and are evolved for 300 generations across all benchmark instances. This uniform experimental setup allows performance differences to be attributed primarily to the algorithmic design, rather than variations in computational budget or search effort. For the SEMO algorithm and the LLM-generated heuristics applied to SEMO, we run 20,000 iterations for Bi-TSP and Tri-TSP, and 10,000 iterations for Bi-KP and Bi-CVRP. 

Combinatorial optimization problems are encoded appropriately based on their structure. For permutation-based problems such as Bi-TSP, Tri-TSP, and Bi-CVRP, we adopt standard permutation representations and apply combinatorial variation operators including Swap Mutation and Partially Mapped Crossover. For binary-encoded problems such as Bi-KP, we use bitstring representations and apply bit-flip mutation along with standard uniform crossover to maintain diversity and introduce variation during evolution. 

### **B.3 Motivation for Using SEMO as the Underlying Framework** 

In this work, we adopt the Simple Evolutionary Multi-objective Optimization (SEMO) framework as the basis for evaluating LLM-generated heuristics, motivated by both practical efficiency and algorithmic effectiveness: 

- **Lightweight and Computationally Efficient:** Evaluating LLM-generated heuristics involves running optimization routines repeatedly, often hundreds or thousands of times over combinatorial problems. Embedding each heuristic within full-fledged MOEAs such as NSGA-II or MOEA/D results in significant computational overhead. In contrast, SEMO follows a (1 + 1) design that evaluates only one solution per iteration, which greatly reduces runtime and makes large-scale heuristic search tractable. 

- **Surprisingly Effective Search Performance:** Despite its simplicity, SEMO has demonstrated competitive, and in some cases superior, performance compared to both traditional MOEAs and local search heuristics (Li et al. 2024). One key factor is its unbounded archive, which enables the generation of new solutions from the entire set of non-dominated individuals, in contrast to the fixed-size populations used in most MOEAs. This promotes greater diversity and adaptability in the search. Additionally, SEMO’s inherent stochasticity in selection and mutation introduces a less greedy search behavior, which helps the algorithm escape local optima more effectively than deterministic local search methods such as PLS or Anytime PLS (Dubois-Lacoste, L´opez-Ib´a˜nez, and St¨utzle 2015; Paquete and St¨utzle 2004). 

Building on these advantages, we employ LLMs to design the _selection_ and _neighborhood exploration_ components within the SEMO framework, resulting in heuristics that combine speed with strong search performance for MOCOP. 

**C Algorithm details** 

In this section, we provide a detailed explanation of the PFG generation process and the proposed MPaGE Framework, as illustrated in Algorithm 2 and Algorithm 3, respectively. 

|**Algorithm 2:**PFG Generation|
|---|
|**Input:** Population_H_of heuristics;|
|Objective values_ej_(_h_)for_j_ = 1_,_2;|
|Number of grid segments_K_1_, K_2;|
|Small positive value_σ_|
|**Output:**Grid mapping_G_ :N<sup>2</sup> _→_2<sup>_|H|_</sup>; Elite set_E_|
|**1 for**_j ←_1**to**2**do**|
|**2**<br>_z_<sup>_∗_</sup><br>_j _<sup>_←_min</sup><sup>_h∈H_</sup> <sup>_ej_(</sup><sup>_h_) ;</sup><br>// Ideal point of objective _j_|
|**3**<br>_z_<sup>_n_</sup><br>_j _<sup>_←_max</sup><sup>_h∈H_</sup> <sup>_ej_(</sup><sup>_h_) ;</sup><br>// Nadir point of objective _j_<br><br><br>|
|**4**<br>_δj ←_<br>_z_<sup>_n_</sup><br>_j _<sup>_−z∗_</sup><br>_j_ <sup>+2</sup><sup>_σ_</sup><br>_Kj_<br>;<br>// Cell width with margin|
|**5 foreach**_h ∈H_**do**|
|**6**<br>**for**_j ←_1**to**2**do**<br>_∗_<br><br>|
|**7**<br>_gj ←_<br>�_ej_(_h_)_−z_<br>_j_ <sup>+</sup><sup>_σ_</sup><br>_δj_<br>�<br>;<br>// Grid index|
|**8**<br>_G_(_h_)_←_(_g_1_, g_2);<br>// Grid cell index for _h_|
|**9**<br>_G_(_G_(_h_))_←G_(_G_(_h_))_∪{h}_;<br>// Assign _h_ to cell|
|**10** _E ←∅_;|
|**11 foreach**_cell g in G_ **do**|
|**12**<br>_C ←G_(_g_);<br>// Current set of solutions in cell|
|**13**<br>_G_(_g_)_←∅_;<br>// Reset cell content|
|**14**<br>**foreach**_h ∈C_ **do**<br><sup>_̸_</sup>|
|**15**<br>**if**∄_h_<sup>_′ _</sup>_∈C, h_<sup>_′̸_ </sup>=_h ∧e_(_h_<sup>_′_</sup>)_≺e_(_h_)**then**|
|**16**<br>_G_(_g_)_←G_(_g_)_∪{h}_;<br>// Keep non-dominated _h_|
|**17** _E ←_<sup>�</sup><br>_g∈_dom(_G_) <sup>_G_(</sup><sup>_g_) ;</sup><br>// Collect elite set from all non-empty cells<br>**18 return**_G, E_;|



|**Algorithm 3:**MPaGE Framework||
|---|---|
|**Input:** Population size_N_; Iteration count_T_;<br>Problem descriptionΠ; Pretrained LLM_L_;<br>Grid size(_K_1_, K_2); Margin_σ_;<br>Probabilities_ϵ_(local selection),_γ_ (mutation)<br>**Output:**Final heuristic population_P _<sup>_∗_</sup>||
|**1** _P_0 _←∅_;||
|**2 for**_i ←_1**to**_N_ **do**||
|**3**<br>_o ←_LLMGenerate(_L,_Π);||
|**4**<br>_P_0 _←P_0_∪{o}_;||
|**5 for**_t ←_1**to**_T_ **do**||
|**6**<br>_G, E ←_**PFGGeneration**(_Pt−_1_, e_1_, e_2_, K_1_, K_2_, σ_);||
|**7**<br>**for**_i ←_1**to**_N_ **do**<br>||
|**8**<br>_u ∼U_(0_,_1);||
|**9**<br>**if**_u < ϵ_**then**||
|**10**<br>_g ∼U_(1_, |G|_);_N_(_g_)_←_Neighbors(_g_);_P ←_<sup>�</sup><br>_g_<sup>_′_</sup>_∈{g}∪N_(_g_) <sup>_G_(</sup><sup>_g′_) ;</sup>|// Exploration|
|<br>**11**<br>_{C_1_, . . . , Cm} ←_SemClust(_P_;_L_);||
|**12**<br>_i ∼U_(1_, m_);<br>_h ∼Ci_;||
|**13**<br>_v ∼U_(0_,_1);||
|**14**<br>**if**_v < γ_ **then**||
|**15**<br>_P_parent _←{h}_;|// Mutation|
|**16**<br>**else**||
|**17**<br>_h_<sup>_′ _</sup>_∼_<sup>�</sup><br>_k̸_=_i _<sup>_Ck_;</sup>||
|**18**<br>_P_parent _←{h, h_<sup>_′_</sup>_}_;|// Crossover|
|**19**<br>**else**||
|**20**<br>_P_parent _∼_Sample(_E,_2);|// Exploitation|
|**21**<br>_ϕ ←_ReflectiveFeedback(_L, P_parent);||
|**22**<br>_o ←_SearchOffspring(_L, ϕ_);||
|**23**<br>_Pt−_1 _←Pt−_1_∪{o}_;||
|**24** _P _<sup>_∗_</sup>_←_NonDominatedSet(_PT_);<br>**25 return**_P _<sup>_∗_</sup>||



## **D Metric descriptions** 

### **D.1 Hypervolume** 

The hypervolume (HV) metric is a prevalent indicator used to assess the quality of solutions generated by multi-objective combinatorial optimization (MOCO) algorithms. It evaluates both convergence toward the Pareto front and the diversity of solutions, without relying on a known ground truth. Given a reference point **r** _∈_ R<sup>_M_</sup> , the hypervolume of a Pareto front _F_ is denoted as HV **r** ( _F_ ) and defined by: 



where _µ_ is the Lebesgue measure, and [ **f** ( _π_ ) _,_ **r** ] represents the axis-aligned hyperrectangle spanning from the point **f** ( _π_ ) to the reference point **r** in _M_ dimensions, i.e., [ _f_ ( _π_ ) _, r_ ] = [ _f_ 1( _π_ ) _, r_ 1] _× · · · ×_ [ _fM_ ( _π_ ) _, rM_ ]. 

To ensure fair comparison of HV values across different objectives, we normalize each objective value based on global approximations. Specifically, to compare the quality of the Pareto fronts produced by LLM-based method, we compute the ideal point **z**<sup>ideal</sup> = ( _z_ 1<sup>ideal</sup> _, . . . , zM_<sup>ideal)</sup><sup>_⊤_and nadir point</sup><sup>**z**nadir=(</sup><sup>_z_</sup> 1<sup>nadir</sup> _, . . . , zM_<sup>nadir)</sup><sup>_⊤_from the union of all approximated Pareto</sup> fronts _P_ obtained by all heuristics: 



where _zi_<sup>ideal</sup> = min _{vi |_ **v** _∈P}, zi_<sup>nadir</sup> = max _{vi |_ **v** _∈P}, ∀i ∈{_ 1 _, . . . , M }._ This normalization maps all objective values to [0 _,_ 1]. The HV reference point is set to **r**<sup>_∗_</sup> = (1 _._ 1 _, . . . ,_ 1 _._ 1)<sup>_⊤_</sup> . To evaluate HV of a heuristic for given MOCOP, The HV is normalized as HV<sup>_′_</sup> **r**<sup>(</sup><sup>_F_) = HV</sup><sup>**r**(</sup><sup>_F_)</sup><sup>_/_�</sup><sup>_M_</sup> _i_ =1<sup>_|ri −zi|_, where</sup><sup>**z**is</sup> an ideal point such that _zi <_ min _{fi_ ( _π_ ) _| f_ ( _π_ ) _∈F}_ (or _zi >_ max _{fi_ ( _π_ ) _| f_ ( _π_ ) _∈F}_ for maximization), _∀i ∈{_ 1 _, . . . , M }_ . The **r** and **z** are used across all methods for a given MOCOP, as summarized in Table 7. 

Table 7: Reference points and ideal points for the MOCO problems. 

|**Problem**|**Size**|**r**|**z**|
|---|---|---|---|
||20|(20, 20)|(0, 0)|
||50|(35, 35)|(0, 0)|
|Bi-TSP|100|(65, 65)|(0, 0)|
||150|(85, 85)|(0, 0)|
||200|(115, 115)|(0, 0)|
||20|(30, 8)|(0, 0)|
|Bi-CVRP|50|(45, 8)|(0, 0)|
||100|(80, 8)|(0, 0)|
||50|(5, 5)|(30, 30)|
|Bi-KP|100|(20, 20)|(50, 50)|
||200|(30, 30)|(75, 75)|
||20|(20, 20, 20)|(0, 0)|
|Tri-TSP|50|(35, 35, 35)|(0, 0)|
||100|(65, 65, 65)|(0, 0)|



### **D.2 Inverted Generational Distance** 

The Inverted Generational Distance (IGD) is a commonly used metric to assess the quality of solutions generated by multiobjective optimization methods. It captures both convergence to the Pareto front and diversity among solutions by averaging the shortest distances from each point in a reference set of Pareto-optimal solutions to the closest solution in the approximated front. Given a reference front _Q_ and a non-dominated set _P_ obtained by the algorithm, IGD is computed as: 



where _∥· ∥_ 2 denotes the Euclidean norm. Lower IGD values indicate that the solution set _P_ is closer to the true Pareto front _Q_ in terms of both convergence and diversity. In this study, the reference set _Q_ is constructed as the non-dominated front derived from the union of all heuristics (Coello Coello and Reyes Sierra 2004). 

### **D.3 Shannon-Wiener diversity index** 

The Shannon–Wiener Diversity Index (SWDI) provides a quantitative measure of population diversity at a given time step, based on the distribution of individuals into clusters (Dat, Doan, and Binh 2025). In the context of heuristic search algorithms, this index reflects how evenly the population is spread across the search space. Given a set of encoded individuals _V_ = _{_ **v** 1 _, . . . ,_ **v** _n}_ , each individual is assigned to a cluster using cosine similarity. Let _Ci_ denote the _i_ -th cluster, and let _M_ be the total number of individuals in all clusters. The proportion of individuals in cluster _Ci_ is defined as: 



The diversity score is then computed using the Shannon entropy: 



where _N_ is the total number of clusters. A higher value of _H_ ( _X_ ) indicates a more uniform distribution of individuals across clusters, suggesting better exploration of the search space. In contrast, a lower value implies that individuals are concentrated in fewer clusters, which may facilitate exploitation of promising regions but also increases the risk of premature convergence. In this study, the clustering procedure and associated hyper-parameters follow the configuration described in (Dat, Doan, and Binh 2025). 

### **D.4 Cummmulative diversity index** 

In the context of heuristic search, the Cumulative Diversity Index (CDI) quantifies how well the diversity, or system energy, is distributed from a centralized state to a more dispersed configuration.(Dat, Doan, and Binh 2025). 

Let _A_ = _{_ **v** 1 _, . . . ,_ **v** _n}_ be the set of all individuals in the archive, where each individual is represented by an embedding vector in a continuous space. To assess the diversity within _A_ , a Minimum Spanning Tree (MST) is constructed over the set using Euclidean distances between individual vectors. The MST connects all individuals with a subset of _|A| −_ 1 edges such that the total edge length is minimized and no cycles are formed. Let _di_ denote the length of the _i_ -th edge in the MST. The probability associated with each edge is computed as: 



and the cumulative diversity is then defined using Shannon entropy: 



where _|A|_ is the archive size. Higher CDI values indicate a more distributed and diverse population, which is essential for maintaining a robust search process. 

**E MPaGE prompt details** 

### **E.1 Task description prompt** 

Our goal is to design a heuristic function for generating high-quality neighbor solutions in specific MOCOP. The task description provided in the prompt and the template of the Python code snippet is outlined below. The inputs include a solution archive and relevant problem-specific data, and the output should be a feasible neighbor solution. 

#### **Bi-TSP heuristic design task description and template program.** 

**Task Description:** You are solving a Bi-objective Travelling Salesman Problem (bi-TSP), where each node has two different 2D coordinates: ( _x_ 1 _, y_ 1) and ( _x_ 2 _, y_ 2), representing its position in two objective spaces. The goal is to find a tour visiting each node exactly once and returning to the starting node, while minimizing two objectives simultaneously: the total tour length in each coordinate space. 

Given an archive of solutions, where each solution is a numpy array representing a TSP tour, and its corresponding objective is a tuple of two values (cost in each space), design a heuristic function named select ~~n~~ eighbor that selects one solution from the archive and applies a novel or hybrid local search operator to generate a neighbor solution from it. 

Please perform an intelligent random selection from among the solutions that show promising potential for further local improvement. Using a creative local search strategy that you design yourself, go beyond standard approaches to design a method that yields higher-quality solutions across multiple objectives. The function should return the new neighbor solution. 

#### **Template Program:** 

1 **<mark>import</mark>** <mark>numpy as np</mark> 2 **<mark>from</mark>** <mark>typing</mark> **<mark>import</mark>** <mark>List , Tuple</mark> 3 **<mark>import</mark>** <mark>random</mark> 4 5 **<mark>def</mark>** <mark>select_neighbor(</mark> 6 <mark>archive: List[Tuple[np.ndarray , Tuple[</mark> **<mark>float</mark>** <mark>,</mark> **<mark>float</mark>** <mark>]]],</mark> 7 <mark>instance: np.ndarray ,</mark> 8 <mark>distance_matrix_1: np.ndarray ,</mark> 9 <mark>distance_matrix_2: np.ndarray</mark> 10 <mark>) -> np.ndarray:</mark> 11 <mark>"""</mark> 12 <mark>Select a promising solution from the archive and generate a neighbor solution from it.</mark> 13 14 <mark>Args:</mark> 15 <mark>archive: List of (solution , objective) pairs. Each solution is a numpy array of node IDs.</mark> 16 <mark>Each objective is a tuple of two float values (cost in each space).</mark> 17 <mark>instance: Numpy array of shape (N, 4). Each row contains coordinates in 2D spaces: (x1 , y1 , x2 , y2).</mark> 18 <mark>distance_matrix_1: Distance matrix in the first objective space.</mark> 19 <mark>distance_matrix_2: Distance matrix in the second objective space.</mark> 20 21 <mark>Returns:</mark> 22 <mark>A new neighbor solution (numpy array).</mark> 23 <mark>"""</mark> 24 <mark>base_solution = archive [0][0]. copy()</mark> 25 <mark>new_solution = base_solution.copy()</mark> 26 <mark>new_solution [0], new_solution [1] = new_solution [1], new_solution [0]</mark> 27 28 **<mark>return</mark>** <mark>new_solution</mark> 

#### **Tri-TSP heuristic design task description and template program.** 

**Task Description:** You are solving a Tri-objective Travelling Salesman Problem (tri-TSP), where each node has three different 2D coordinates: ( _x_ 1 _, y_ 1), ( _x_ 2 _, y_ 2), and ( _x_ 3 _, y_ 3), representing its position in three objective spaces. The goal is to find a tour visiting each node exactly once and returning to the starting node, while minimizing three objectives simultaneously: the total tour length in each coordinate space. 

Given an archive of non-dominated solutions, where each solution is a numpy array representing a TSP tour, and its corresponding objective is a tuple of three values (cost in each space), design a heuristic function named select ~~n~~ eighbor that selects one solution from the archive and applies a novel or hybrid local search operator to generate a neighbor solution from it. Please perform an intelligent random selection from among the solutions that show promising potential for further local improvement. Using a creative local search strategy of your own design, specifically tailored to effectively optimize across three objectives, go beyond standard approaches to design a method that yields higher-quality solutions across multiple objectives. The function should return the new neighbor solution. 

#### **Template Program:** 

- 1 **<mark>import</mark>** <mark>numpy as np</mark> 

- 2 **<mark>from</mark>** <mark>typing</mark> **<mark>import</mark>** <mark>List , Tuple</mark> 

- 3 **<mark>import</mark>** <mark>random</mark> 4 5 **<mark>def</mark>** <mark>select_neighbor(</mark> 6 <mark>archive: List[Tuple[np.ndarray , Tuple[</mark> **<mark>float</mark>** <mark>,</mark> **<mark>float</mark>** <mark>,</mark> **<mark>float</mark>** <mark>]]],</mark> 7 <mark>instance: np.ndarray ,</mark> 8 <mark>distance_matrix_1: np.ndarray ,</mark> 9 <mark>distance_matrix_2: np.ndarray ,</mark> 

- 10 <mark>distance_matrix_3: np.ndarray</mark> 11 <mark>) -> np.ndarray:</mark> 12 <mark>"""</mark> 

- 13 <mark>Select a promising solution from the archive and generate a neighbor solution from it.</mark> 14 15 <mark>Args:</mark> 16 <mark>archive: List of (solution , objective) pairs. Each solution is a numpy array of node IDs.</mark> 17 <mark>Each objective is a tuple of three float values (costs in each space).</mark> 18 <mark>instance: Numpy array of shape (N, 6). Each row contains coordinates: (x1 , y1 , x2 , y2 , x3 , y3).</mark> 19 <mark>distance_matrix_1: Distance matrix in the first objective space.</mark> 20 <mark>distance_matrix_2: Distance matrix in the second objective space.</mark> 21 <mark>distance_matrix_3: Distance matrix in the third objective space.</mark> 22 

- 23 <mark>Returns:</mark> 

- 24 <mark>A new neighbor solution (numpy array).</mark> 25 <mark>"""</mark> 

26 <mark>base_solution = archive [0][0]. copy()</mark> 27 <mark>new_solution = base_solution.copy()</mark> 28 <mark>new_solution [0], new_solution [1] = new_solution [1], new_solution [0]</mark> 29 30 **<mark>return</mark>** <mark>new_solution</mark> 

#### **Bi-KP heuristic design task description and template program.** 

**Task Description:** You are solving a Bi-objective Knapsack Problem (BI-KP), where each item has a weight and two profit values: value1 and value2. The goal is to select a subset of items such that the total weight does not exceed a given capacity, while simultaneously maximizing the total value in both objective spaces. 

Given an archive of non-dominated solutions, where each solution is a binary numpy array indicating item inclusion (1) or exclusion (0), and its corresponding objective is a tuple of two values (total value1, total value2), design a heuristic function named select ~~n~~ eighbor that selects one solution from the archive and applies a novel or hybrid local search operator to generate a neighbor solution from it. 

You must ensure that the generated neighbor solution remains feasible. Please perform an intelligent random selection from among the solutions that show promising potential for further local improvement. Using a creative local search strategy that you design yourself, go beyond standard approaches to develop a method that yields higher-quality solutions across multiple objectives. The function should return the new neighbor solution. 

#### **Template Program:** 

- 1 **<mark>import</mark>** <mark>numpy as np</mark> 

- 2 **<mark>from</mark>** <mark>typing</mark> **<mark>import</mark>** <mark>List , Tuple</mark> 

- 3 **<mark>import</mark>** <mark>random</mark> 

- 4 

- 5 **<mark>def</mark>** <mark>select_neighbor(</mark> 

- 6 <mark>archive: List[Tuple[np.ndarray , Tuple[</mark> **<mark>float</mark>** <mark>,</mark> **<mark>float</mark>** <mark>]]],</mark> 

- 7 <mark>weight_lst: np.ndarray ,</mark> 8 <mark>value1_lst: np.ndarray ,</mark> 9 <mark>value2_lst: np.ndarray ,</mark> 

- 10 <mark>capacity:</mark> **<mark>float</mark>** 11 <mark>) -> np.ndarray:</mark> 12 <mark>"""</mark> 13 <mark>Select a promising solution from the archive and generate a neighbor solution from it.</mark> 14 15 <mark>Args:</mark> 16 <mark>archive: List of (solution , objective) pairs. Each solution is a binary numpy array (0/1) of item selections.</mark> 17 <mark>Each objective is a tuple of two float values (total value1 , total value2).</mark> 18 <mark>weight_lst: Numpy array of shape (N,), item weights.</mark> 19 <mark>value1_lst: Numpy array of shape (N,), item values for objective 1.</mark> 20 <mark>value2_lst: Numpy array of shape (N,), item values for objective 2.</mark> 21 <mark>capacity: Maximum allowed total weight.</mark> 22 23 <mark>Returns:</mark> 24 <mark>A new neighbor solution (numpy array).</mark> 25 <mark>"""</mark> 26 <mark>base_solution = archive [0][0]. copy()</mark> 27 <mark>new_solution = base_solution.copy()</mark> 28 <mark>new_solution [0], new_solution [1] = new_solution [1], new_solution [0]</mark> 29 

- 30 **<mark>return</mark>** <mark>new_solution</mark> 

#### **Bi-CVRP heuristic design task description and template program.** 

**Task Description:** You are solving a Bi-objective Capacitated Vehicle Routing Problem (Bi-CVRP), where a single depot and multiple customers are located in 2D space. Each customer has a positive demand, and all vehicles in the fleet have identical capacity limits. The objective is to construct a set of routes, each starting and ending at the depot, such that: 

- all customers are served, 

- vehicle capacities are not exceeded on any route, 

- two conflicting objectives are minimized: 

- total travel distance across all routes, 

- makespan (the length of the longest individual route). 

Each solution in the archive is represented as a list of NumPy arrays, where each array denotes a single route (starting and ending at depot index 0), and is paired with a tuple of two objective values (total ~~d~~ istance, makespan). Your task is to implement a function named select ~~n~~ eighbor that selects one promising solution from the archive and applies a novel or hybrid local search operator to generate a feasible neighbor solution. You must ensure that vehicle capacity constraints are respected. 

Please perform an intelligent random selection among solutions that show potential for local improvement. Go beyond standard approaches to develop a method that yields higher-quality solutions across both objectives. The function should return the new neighbor solution. 

#### **Template Program:** 

1 **<mark>import</mark>** <mark>numpy as np</mark> 2 **<mark>from</mark>** <mark>typing</mark> **<mark>import</mark>** <mark>List , Tuple</mark> 3 **<mark>import</mark>** <mark>random</mark> 4 5 **<mark>def</mark>** <mark>select_neighbor(</mark> 6 <mark>archive: List[Tuple[np.ndarray , Tuple[</mark> **<mark>float</mark>** <mark>,</mark> **<mark>float</mark>** <mark>]]],</mark> 7 <mark>coords: np.ndarray ,</mark> 8 <mark>demand: np.ndarray ,</mark> 9 <mark>distance_matrix: np.ndarray ,</mark> 10 <mark>capacity:</mark> **<mark>float</mark>** 11 <mark>) -> np.ndarray:</mark> 12 <mark>"""</mark> 13 <mark>Select a promising solution from the archive and generate a neighbor solution from it.</mark> 14 <mark>Args:</mark> 15 <mark>archive: A list of tuples , where each tuple contains:</mark> 16 <mark>- solution: A list of numpy arrays , each representing a vehicle route.</mark> 17 <mark>Each route starts and ends at the depot (node index 0), e.g., [0, 3, 5, 0].</mark> 18 <mark>- objective: A tuple of two float values (total_distance , makespan),</mark> 19 <mark>representing the two objective values of the solution.</mark> 20 21 <mark>coords: A numpy array of shape (n_nodes , 2), representing (x, y) coordinates of each node (depot + customers).</mark> 22 <mark>demand: A numpy array of shape (n_nodes ,), where demand[i] is the demand of node i. The depot has demand 0.</mark> 23 <mark>distance_matrix: A numpy array of shape (n_nodes , n_nodes), where [i][j] is the Euclidean distance between node i and j.</mark> 24 <mark>capacity: A float representing the maximum capacity of each vehicle.</mark> 25 26 <mark>Returns:</mark> 27 <mark>A new neighbor solution.</mark> 28 <mark>"""</mark> 29 <mark>base_solution = archive [0][0]. copy()</mark> 30 <mark>new_solution = base_solution.copy()</mark> 31 32 **<mark>return</mark>** <mark>new_solution</mark> 

### **E.2 Initialization prompt** 

In our experiments, all initial heuristics are generated by LLMs without requiring any expert-crafted designs. The LLMs are prompted with the heuristic design task and instructed to produce new heuristics by first providing a textual description, followed by a corresponding Python implementation. This process is repeated _N_ times to obtain _N_ distinct initial heuristics. 

#### **Prompt for population initialization.** 

You are an expert in the domain of optimization heuristics helping to design heuristics that can effectively solve optimization problems. 

_{_ Task Description _}_ 

1. First, describe your new algorithm and main steps in one long, detail sentence. The description must be inside within boxed _{{}_ . 

2. Next, implement the following Python function: _{_ Template Program _}_ 

Check syntax, code carefully before returning the final function. Do not give additional explanations. 

Here, Task Description and Template Program are defined in **E.1** . 

### **E.3 Semantic clustering prompt** 

We employ the following prompt to instruct the LLM to analyze and cluster a list of heuristic code snippets based on their semantic logic. Each snippet corresponds to a heuristic generated in earlier stages and is represented as a Python function. The LLM is asked to group these snippets such that heuristics with similar behavior or design principles fall into the same cluster. This enables automated semantic analysis and categorization without manual labeling. The expected output is a JSON object, where each key corresponds to a cluster ID (as a string), and each value is a list of indices indicating the heuristics belonging to that cluster. 

To improve efficiency and avoid redundant computation, we cache the clustering results for each grid cell along with its neighboring cells. These cached results can be reused in subsequent runs, substantially reducing overall processing time. 

#### **Prompt for Grouping Code Snippets** 

You are an expert in the domain of optimization heuristics helping to design heuristics that can effectively solve optimization problems. 

I have _{_ len(codes) _}_ code snippets as follows: <Code>: ... ... 

Analyze the logic of all the given code snippets carefully. Then group the snippets into clusters where each group contains codes with similar logic. Return the result as a JSON object where the keys are the group indices and the values are lists of code indices that belong to each group. 

For example: { "1": [0, 2, 4], "2": [1, 3], "3": [5] } 

### **E.4 Feedback reflection prompt** 

We use this prompt to guide the LLM in synthesizing a new heuristic by reflecting on a set of existing candidate heuristics. Each candidate is provided in code form, and the LLM is instructed to analyze common patterns, identify shared strengths and recurring weaknesses, and ultimately propose a single hybrid or improved strategy. 

#### **Prompt for heuristic synthesis.** 

You are an expert in the domain of optimization heuristics helping to design heuristics that can effectively solve optimization problems. 

_{_ Task Description _}_ I have _{_ len(indivs) _}_ existing algorithms with their codes as follows: <Code>: ... 

Please carefully analyze all of the above algorithms. Your task is to synthesize their ideas, identify recurring patterns, and point out opportunities for improvement. 

Your output should be a **Suggestions** section, where you: 

- Summarize key strengths shared across the implementations. 

- Identify limitations or blind spots that appear in multiple codes. 

- Propose hybrid or improved strategies that integrate strengths and overcome shortcomings, in a feasible running time. 

- **Output format:** 

Suggestions: Write only one proposed hybrid or improved strategy that integrates strengths and overcomes shortcomings here. 

Do not include any explanations, summaries, or new algorithms outside of this section. 

Here, len(indivs) is the number of selected heuristics and <Code> are their corresponding Python implementations and descripions, respectively. 

### **E.5 Crossover prompt** 

MPaGE adopts search operators from EoH (Liu et al. 2024), each implemented via LLMs. Beyond this standard structure, we optionally include a reflective feedback segment, highlighted in red, which is derived from the synthesis output of **E.4** . This feedback provides suggestions for improvement based on analysis of previously generated heuristics. Importantly, not all operators incorporate this component: mutation operators are generated without feedback, while crossover operators may include it with a certain probability _ρ_ . This probabilistic inclusion aims to balance solution quality with computational efficiency, by reducing the frequency of costly LLM inference. 

#### **E1 Operator.** 

I have _{_ len(indivs) _}_ existing algorithms with their codes as follows: <Code>: ... 

Analyze the logic of all the given code snippets carefully. Then identify the two code snippets whose logic is most different from each other and create a new algorithm that is totally different in both logic and form from both of them. Here are some suggestions you can refer to: 

— Suggestions: + _{_ suggestions _}_ + — 

1. First, describe your new algorithm and main steps in one long, detailed sentence. The description must be inside within boxed _{{}_ . 

2. Next, implement the following Python function: 

   - _{_ Template Program _}_ 

Check syntax, code carefully before returning the final function. Do not give additional explanations. 

#### **E2 Operator.** 

I have _{_ len(indivs) _}_ existing algorithms with their codes as follows: <Code>: ... 

... Here are some suggestions you can refer to: — Suggestions: + _{_ suggestions _}_ + — 

Please help me create a new algorithm that has a totally different form from the given ones but can be motivated from them. 

1. Firstly, identify the common backbone idea in the provided algorithms. 

2. Secondly, based on the backbone idea, describe your new algorithm. The description must be inside within boxed _{{}_ . 

3. Thirdly, implement the following Python function: 

   - _{_ Template Program _}_ 

Check syntax, code carefully before returning the final function. Do not give additional explanations. 

#### **M1 Operator.** 

I have one algorithm with its code as follows. 

<Code>: ... 

Please assist me in creating a new algorithm that has a different form but can be a modified version of the algorithm provided. You may focus on refining either the _selection phase_ or the _neighborhood search phase_ . 

1. First, describe your new algorithm and main steps in one long, detailed sentence. The description must be inside within boxed _{{}_ . 

2. Next, implement the following Python function: 

   - _{_ Template Program _}_ 

Check syntax, code carefully before returning the final function. Do not give additional explanations. 

#### **M2 Operator.** 

I have one algorithm with its code as follows. 

<Code>: ... 

Please identify the main algorithm parameters and assist me in creating a new algorithm that has a different parameter setting of the score function provided. You may focus on refining either the _selection phase_ or the _neighborhood search phase_ . 

1. First, describe your new algorithm and main steps in one long, detailed sentence. The description must be inside within boxed _{{}_ . 

2. Next, implement the following Python function: 

   - _{_ Template Program _}_ 

Check syntax, code carefully before returning the final function. Do not give additional explanations. 

## **F Clustering variations analysis** 

We analyze the effectiveness of different clustering methods in grouping heuristics according to their underlying logic rather than superficial code characteristics. To this end, we construct a controlled code space consisting of three ground-truth clusters, where each cluster contains multiple heuristics that implement the same functional behavior. Although all heuristics within a cluster share identical logic, they differ in implementation details such as programming constructs (e.g., use of loops vs. vectorized operations), random sampling techniques, copying mechanisms, or library functions. This design introduces syntactic and stylistic variations that challenge clustering algorithms to look beyond surface-level code differences. Illustrative examples of these heuristic groups are shown in Figures 4–6, where each group demonstrates the same operational intent expressed through distinct code structures. This setup allows us to evaluate whether clustering methods can correctly recover the latent functional groupings, rather than being misled by low-level syntactic variations. 

We evaluate four clustering strategies: 

1. **Ours (MPaGE)** : Leverages LLMs to semantically interpret the code and group heuristics based on inferred logical behavior. 

2. **SWDI-based clustering** : Converts code snippets into vector representations using a code embedding model and performs clustering based on similarity, following the setting in Dat, Doan, and Binh (2025). 

3. **K-Means** : Clusters heuristics solely based on their performance across optimization objectives, without incorporating any code-level information. The number of clusters is fixed at 3 to align with the semantic clustering setting. 

4. **AST Similarity** : Computes pairwise structural similarity between the Abstract Syntax Trees (ASTs) of the heuristics, as described in Yao, Chen, and Wang (2025). The AST similarity score ranges from 0 to 1, where 0 indicates complete structural dissimilarity and 1 signifies syntactically identical structures. 



Figure 4: **Group Heuristics 1** : Three heuristics implementing the same logic: selecting a solution and generating a neighbor by randomly swapping two elements. 

Based on Figure 7 and Figure 8, it is evident that the MPaGE method yields clustering results that most closely align with the ground-truth functional grouping. This demonstrates that LLMs, when properly utilized, are capable of understanding the semantics and intended logic of code in ways that surpass purely quantitative approaches. In contrast, the K-Means clustering method, which groups heuristics based on objective performance metrics, produces significantly less coherent clusters. This is because quantitative values, such as execution time or solution quality, do not reliably capture the underlying logic of code. Such values are often affected by stochastic behavior, system-dependent conditions, or implementation-level optimizations, leading to misleading assessments of similarity. Two heuristics implementing the same logic may yield different numerical results for reasons entirely unrelated to their semantic behavior. 

The SWDI approach, which relies on embedding representations, partially captures structural similarity (e.g., correctly grouping the last three heuristics), but overall lacks consistency. Code embeddings are heavily influenced by surface-level patterns and often fail to account for the high degree of syntactic variability introduced by LLMs. As a result, heuristics with equivalent functionality may be represented as distant points in the embedding space. The AST similarity also matrix exhibits limited discriminative power. Although ASTs reflect syntactic structure, they remain sensitive to superficial differences in code, particularly in LLM-generated heuristics, where identical logic can manifest in diverse syntactic forms. As observed in Figure 7e, the pairwise similarity scores between heuristic pairs fail to highlight or emphasize any significant structural grouping. Similarity values tend to be uniformly distributed and do not correspond well to the functional relationships among heuristics. 



Figure 5: **Group Heuristics 2** : Three heuristics implementing the same logic: selecting a solution and reversing a randomly chosen segment [ _i_ : _j_ + 1]. 



Figure 6: **Group Heuristics 3** : Four heuristics implementing the same logic: Sequentially select unvisited nodes such that the next node in the closet with the smallest sum of total distance. 







<!-- Start of picture text -->
(a) Ground Truth (b) MPaGE<br><!-- End of picture text -->





<!-- Start of picture text -->
(c) SWDI Approach<br><!-- End of picture text -->







<!-- Start of picture text -->
(d) K-Means (e) AST Similarity<br><!-- End of picture text -->

Figure 7: Clustering consistency and similarity matrices across various methods. Each heatmap represents pairwise relationships between code heuristics. In subfigures (a)–(d), a value of 1 indicates that two heuristics are assigned to the same cluster, while 0 indicates they are assigned to different clusters. (a) Ground-truth grouping by functional logic. (b) Clustering result from our method (MPaGE). (c) Clustering based on SWDI. (d) K-Means clustering based on objective performance. (e) Pairwise AST similarity scores between heuristics, where higher values indicate greater syntactic similarity between the corresponding Abstract Syntax Trees. 

Table 8: Performance comparison on Bi-TSP20 and Tri-TSP20 instances. 

|**Method**|**Bi-T**|**SP20**|**Tri-T**|**SP20**|
|---|---|---|---|---|
||HV_↑_|IGD_↓_|HV_↑_|IGD_↓_|
|SWDI Cluster|0.911|0.024|0.888|0.098|
|K-Means|0.876|0.030|0.815|0.184|
|AST Similarity|0.745|0.184|0.757|0.203|
|**MPaGE (Ours)**|0.921|0.013|0.892|0.102|



To evaluate the effectiveness of different strategies in guiding parent selection for heuristic synthesis, we conduct experiments on two benchmark problems: Bi-TSP20 and Tri-TSP20, as shown in Table 8. For the SWDI Clustering and K-Means baselines, parent selection is performed based on cluster membership, similar to MPaGE. In contrast, the AST Similarity method samples parent pairs based on their pairwise structural similarity scores. 

As shown in Table 8, MPaGE consistently outperforms all baselines across both benchmark instances. On Bi-TSP20, MPaGE achieves the highest HV (0.921) and the lowest IGD (0.013), indicating superior convergence and solution diversity. A similar pattern is observed on Tri-TSP20, where MPaGE attains the best HV (0.892) and a competitive IGD (0.102), closely approaching the best IGD achieved by SWDI Clustering (0.098). These results suggest that relying solely on AST similarity offers 

limited utility for parent selection, particularly when dealing with heuristics that involve complex or subtle logic structures. 







<!-- Start of picture text -->
(a) Ground Truth Clusters (b) MPaGE Clusters<br><!-- End of picture text -->







<!-- Start of picture text -->
(c) SWDI Clusters (d) K-Means<br><!-- End of picture text -->

Figure 8: Visualization of heuristic clustering results produced by different methods. **(a)** Ground truth clusters based on manual semantic annotation. **(b)** MPaGE clusters, which are generated using LLM-driven semantic interpretation of code logic. **(c)** SWDI clusters, derived from code embeddings using an embedding model. **(d)** K-Means clusters, obtained by grouping heuristics based solely on performance metrics. MPaGE most closely approximates the ground truth structure, while other methods exhibit greater semantic drift, especially in cases with subtle logic differences. 

## **G Designed Heuristics** 

This section presents the best-performing heuristics generated by MPaGE in terms of hypervolume and runtime across all benchmark instances. 

### **Bi-TSP** 

**# Best hypervolume** # score = [0.584, 0.505] 1 **<mark>def</mark>** <mark>select_neighbor ( archive : List [ Tuple [ np . ndarray , Tuple [</mark> **<mark>float</mark>** <mark>,</mark> **<mark>float</mark>** <mark>]]],</mark> 2 <mark>instance : np . ndarray ,</mark> 3 <mark>distance_matrix_1 : np . ndarray ,</mark> 4 <mark>distance_matrix_2 : np . ndarray ) -> np . ndarray :</mark> 5 <mark># Compute selection probabilities based on inverse objective values</mark> 6 <mark>total_objective_value =</mark> **<mark>sum</mark>** <mark>(1 / ( obj [0] + 1e -9) + 1 / ( obj [1] + 1e -9)</mark> 7 **<mark>for</mark>** <mark>_ , obj</mark> **<mark>in</mark>** <mark>archive )</mark> 8 <mark>probabilities = [(1 / ( obj [0] + 1e -9) + 1 / ( obj [1] + 1e -9)) / total_objective_value</mark> 9 **<mark>for</mark>** <mark>_ , obj</mark> **<mark>in</mark>** <mark>archive ]</mark> 

10 

11 <mark># Select a solution from the archive based on computed probabilities</mark> 12 <mark>selected_index = np . random . choice (</mark> **<mark>len</mark>** <mark>( archive ), p= probabilities )</mark> 13 <mark>selected_solution = archive [ selected_index ][0]. copy ()</mark> 14 15 <mark># Generate neighbor using segment reversal</mark> 16 <mark>n =</mark> **<mark>len</mark>** <mark>( selected_solution )</mark> 17 <mark>i , j =</mark> **<mark>sorted</mark>** <mark>( random . sample (</mark> **<mark>range</mark>** <mark>(n), 2)) # Choose two distinct indices</mark> 18 <mark>new_solution = np . concatenate (( selected_solution [: i],</mark> 19 <mark>selected_solution [i:j +1][:: -1] ,</mark> 20 <mark>selected_solution [j +1:]))</mark> 

21 

22 **<mark>return</mark>** <mark>new_solution</mark> 

**# Best runningtime** 

# score = [0.395, 0.121] 1 **<mark>def</mark>** <mark>select_neighbor ( archive : List [ Tuple [ np . ndarray , Tuple [</mark> **<mark>float</mark>** <mark>,</mark> **<mark>float</mark>** <mark>]]],</mark> 2 <mark>instance : np . ndarray ,</mark> 3 <mark>distance_matrix_1 : np . ndarray ,</mark> 4 <mark>distance_matrix_2 : np . ndarray ) -> np . ndarray :</mark> 5 <mark># Compute selection probabilities based on inverse objective values</mark> 6 <mark>total_score =</mark> **<mark>sum</mark>** <mark>(1 / ( obj [0] + 1e -9) + 1 / ( obj [1] + 1e -9)</mark> 7 **<mark>for</mark>** <mark>_ , obj</mark> **<mark>in</mark>** <mark>archive )</mark> 8 <mark>probabilities = [(1 / ( obj [0] + 1e -9) + 1 / ( obj [1] + 1e -9)) / total_score</mark> 9 **<mark>for</mark>** <mark>_ , obj</mark> **<mark>in</mark>** <mark>archive ]</mark> 10 11 <mark># Select a solution from the archive based on computed probabilities</mark> 12 <mark>selected_index = np . random . choice (</mark> **<mark>len</mark>** <mark>( archive ), p= probabilities )</mark> 13 <mark>selected_solution = archive [ selected_index ][0]. copy ()</mark> 14 15 <mark># Generate neighbor using node repositioning</mark> 16 <mark>n =</mark> **<mark>len</mark>** <mark>( selected_solution )</mark> 17 <mark>neighbor_solution = selected_solution . copy ()</mark> 18 19 <mark># Select two distinct nodes</mark> 20 <mark>idx1 , idx2 = random . sample (</mark> **<mark>range</mark>** <mark>(n), 2)</mark> 21 22 <mark># Heuristic: move node1 right after , node2 right before</mark> 23 <mark>new_position1 = ( idx1 + 1) % n</mark> 24 <mark>new_position2 = ( idx2 - 1) % n</mark> 25 26 <mark># Apply the swap</mark> 27 <mark>neighbor_solution [ new_position1 ], neighbor_solution [ new_position2 ] = neighbor_solution [ idx1 ], neighbor_solution [ idx2 ]</mark> 

28 

29 **<mark>return</mark>** <mark>neighbor_solution</mark> 

### **Tri-TSP** 

**# Best hypervolume** # score = [0.359, 0.893] 1 **<mark>def</mark>** <mark>select_neighbor ( archive : List [ Tuple [ np . ndarray , Tuple [</mark> **<mark>float</mark>** <mark>,</mark> **<mark>float</mark>** <mark>,</mark> **<mark>float</mark>** <mark>]]],</mark> 2 <mark>instance : np . ndarray ,</mark> 3 <mark>distance_matrix_1 : np . ndarray ,</mark> 4 <mark>distance_matrix_2 : np . ndarray ,</mark> 5 <mark>distance_matrix_3 : np . ndarray ) -> np . ndarray :</mark> 6 <mark># Select a promising solution based on multi -objective performance</mark> 7 <mark>archive_weights = [1 / (1 +</mark> **<mark>sum</mark>** <mark>( obj ))</mark> **<mark>for</mark>** <mark>_ , obj</mark> **<mark>in</mark>** <mark>archive ]</mark> 8 <mark>weighted_archive = random . choices ( archive , weights = archive_weights , k =1) [0]</mark> 9 <mark>base_solution = weighted_archive [0]. copy ()</mark> 10 11 <mark>new_solution = base_solution . copy ()</mark> 12 <mark>N =</mark> **<mark>len</mark>** <mark>( new_solution )</mark> 13 14 <mark># Compute performance score and set perturbation factor</mark> 15 <mark>first_objective , second_objective , third_objective = weighted_archive [1]</mark> 

16 <mark>avg_objective = ( first_objective + second_objective + third_objective ) / 3</mark> 17 <mark>perturbation_factor =</mark> **<mark>max</mark>** <mark>(0.1, 0.5 + (0.5 - avg_objective ))</mark> 18 19 <mark># Diversify neighborhood: Swap , Reverse , or Shift</mark> 20 <mark>mutation_type = random . choices ([ 'swap' , 'reverse ' , 'shift '],</mark> 21 <mark>weights =[0.5 * perturbation_factor ,</mark> 22 <mark>0.3 * (1 - perturbation_factor ),</mark> 23 <mark>0.2],</mark> 24 <mark>k =1) [0]</mark> 25 

26 **<mark>if</mark>** <mark>mutation_type == 'swap':</mark> 27 <mark>idx1 , idx2 = random . sample (</mark> **<mark>range</mark>** <mark>(1, N - 1), 2)</mark> 28 <mark>new_solution [ idx1 ], new_solution [ idx2 ] = new_solution [ idx2 ], new_solution [ idx1 ]</mark> 29 **<mark>elif</mark>** <mark>mutation_type == 'reverse ':</mark> 30 <mark>start_idx = random . randint (1, N - 2)</mark> 31 <mark>end_idx = random . randint ( start_idx + 1, N - 1)</mark> 32 <mark>new_solution [ start_idx : end_idx + 1] = new_solution [ start_idx : end_idx + 1][:: -1]</mark> 33 **<mark>elif</mark>** <mark>mutation_type == 'shift ':</mark> 34 <mark>shift_idx = random . randint (1, N - 2)</mark> 35 <mark>new_solution [ shift_idx ], new_solution [ shift_idx + 1] = new_solution [ shift_idx + 1], new_solution [ shift_idx ]</mark> 

36 

37 <mark># Adaptive large perturbation for good solutions</mark> 38 **<mark>if</mark>** <mark>avg_objective < 0.5:</mark> 39 <mark>perturb_indices = random . sample (</mark> **<mark>range</mark>** <mark>(1, N - 1), k=</mark> **<mark>min</mark>** <mark>(3, N - 2))</mark> 40 <mark>random . shuffle ( perturb_indices )</mark> 41 **<mark>for</mark>** <mark>i</mark> **<mark>in range</mark>** <mark>(</mark> **<mark>len</mark>** <mark>( perturb_indices ) - 1):</mark> 42 <mark>new_solution [ perturb_indices [i ]], new_solution [ perturb_indices [i + 1]] = (</mark> 43 <mark>new_solution [ perturb_indices [i + 1]], new_solution [ perturb_indices [ i ]]</mark> 44 <mark>)</mark> 

45 

46 <mark># Additional large shuffle with some probability</mark> 47 **<mark>if</mark>** <mark>random . random () < 0.3:</mark> 48 <mark>additional_indices = random . sample (</mark> **<mark>range</mark>** <mark>(1, N - 1), k =3)</mark> 49 <mark>random . shuffle ( additional_indices )</mark> 50 <mark>new_solution [ additional_indices [0]], new_solution [ additional_indices [1]], new_solution [ additional_indices [2]] = (</mark> 51 <mark>new_solution [ additional_indices [1]], new_solution [ additional_indices [2]], new_solution [ additional_indices [0]]</mark> 52 <mark>)</mark> 

53 

- 54 **<mark>return</mark>** <mark>new_solution</mark> 

**# Best running time** # score = [0.335, 0.476] 1 **<mark>def</mark>** <mark>select_neighbor ( archive : List [ Tuple [ np . ndarray , Tuple [</mark> **<mark>float</mark>** <mark>,</mark> **<mark>float</mark>** <mark>,</mark> **<mark>float</mark>** <mark>]]],</mark> 2 <mark>instance : np . ndarray ,</mark> 3 <mark>distance_matrix_1 : np . ndarray ,</mark> 4 <mark>distance_matrix_2 : np . ndarray ,</mark> 5 <mark>distance_matrix_3 : np . ndarray ) -> np . ndarray :</mark> 6 <mark># Select a solution with good objective sum</mark> 7 <mark>selected_solution , _ = random . choices (</mark> 8 <mark>archive ,</mark> 9 <mark>weights =[1 / ( obj [0] + obj [1] + obj [2])</mark> **<mark>for</mark>** <mark>_ , obj</mark> **<mark>in</mark>** <mark>archive ],</mark> 10 <mark>k =1</mark> 11 <mark>)[0]</mark> 12 13 <mark># Apply a simple swap</mark> 14 <mark>neighbor_solution = selected_solution . copy ()</mark> 15 <mark>n =</mark> **<mark>len</mark>** <mark>( neighbor_solution )</mark> 16 <mark>i , j = random . sample (</mark> **<mark>range</mark>** <mark>(n), 2)</mark> 17 <mark>neighbor_solution [i], neighbor_solution [j] = neighbor_solution [j], neighbor_solution [ i ]</mark> 

18 

- 19 **<mark>return</mark>** <mark>neighbor_solution</mark> 

### **Bi-KP** 

**# Best hypervolume** # score = [0.348, 0.130] 1 **<mark>def</mark>** <mark>select_neighbor ( archive : List [ Tuple [ np . ndarray , Tuple [</mark> **<mark>float</mark>** <mark>,</mark> **<mark>float</mark>** <mark>]]],</mark> 2 <mark>weight_lst : np . ndarray ,</mark> 3 <mark>value1_lst : np . ndarray ,</mark> 4 <mark>value2_lst : np . ndarray ,</mark> 5 <mark>capacity :</mark> **<mark>float</mark>** <mark>) -> np . ndarray :</mark> 6 <mark># Select a solution with high objective sum</mark> 7 <mark>selected_pair = random . choices (</mark> 8 <mark>archive ,</mark> 9 <mark>weights =[ sol [1][0] + sol [1][1]</mark> **<mark>for</mark>** <mark>sol</mark> **<mark>in</mark>** <mark>archive ],</mark> 10 <mark>k =1</mark> 11 <mark>)[0]</mark> 12 13 <mark>base_solution = selected_pair [0]. copy ()</mark> 14 <mark>new_solution = base_solution . copy ()</mark> 15 <mark>current_weight = np . dot ( new_solution , weight_lst )</mark> 16 17 <mark>selected_indices = np . where ( new_solution == 1)[0]</mark> 18 <mark>unselected_indices = np . where ( new_solution == 0)[0]</mark> 19 20 <mark># Prioritize swapping items with high profit -to -weight ratio</mark> 21 **<mark>if</mark>** <mark>selected_indices . size > 0 and unselected_indices . size > 0:</mark> 22 <mark>profit_to_weight = ( value1_lst [ selected_indices ] + value2_lst [ selected_indices ]) / weight_lst [ selected_indices ]</mark> 23 <mark>sorted_selected_indices = selected_indices [ np . argsort ( profit_to_weight )[:: -1]]</mark> 24 25 **<mark>for</mark>** <mark>_</mark> **<mark>in range</mark>** <mark>(5): # Try multiple swaps for improvement</mark> 26 <mark>selected_idx = random . choice ( sorted_selected_indices )</mark> 27 <mark>unselected_idx = random . choice ( unselected_indices )</mark> 28 29 <mark>new_solution [ selected_idx ] = 0</mark> 30 <mark>new_solution [ unselected_idx ] = 1</mark> 31 32 **<mark>if</mark>** <mark>np . dot ( new_solution , weight_lst ) <= capacity :</mark> 33 **<mark>return</mark>** <mark>new_solution # Accept valid neighbor</mark> 34 35 <mark># Revert swap if constraint violated</mark> 36 <mark>new_solution [ selected_idx ] = 1</mark> 37 <mark>new_solution [ unselected_idx ] = 0</mark> 38 39 <mark># Fallback: perturb multiple items</mark> 40 <mark>num_toggles = random . randint (2, 4)</mark> 41 **<mark>for</mark>** <mark>_</mark> **<mark>in range</mark>** <mark>( num_toggles ):</mark> 42 <mark>idx = random . randint (0,</mark> **<mark>len</mark>** <mark>( base_solution ) - 1)</mark> 43 **<mark>if</mark>** <mark>new_solution [ idx ] == 1:</mark> 44 <mark>new_solution [ idx ] = 0</mark> 45 **<mark>else</mark>** <mark>:</mark> 46 **<mark>if</mark>** <mark>current_weight + weight_lst [ idx ] <= capacity :</mark> 47 <mark>new_solution [ idx ] = 1</mark> 48 <mark>current_weight += weight_lst [ idx ]</mark> 49 50 <mark># Final validation: enforce capacity</mark> 51 <mark>while np . dot ( new_solution , weight_lst ) > capacity :</mark> 52 <mark>deselect_idx = random . choice ( np . where ( new_solution == 1)[0])</mark> 53 <mark>new_solution [ deselect_idx ] = 0</mark> 54 55 **<mark>return</mark>** <mark>new_solution</mark> **# Best running time** # score = [0.319, 0.074] 1 **<mark>def</mark>** <mark>select_neighbor ( archive : List [ Tuple [ np . ndarray , Tuple [</mark> **<mark>float</mark>** <mark>,</mark> **<mark>float</mark>** <mark>]]],</mark> 2 <mark>weight_lst : np . ndarray ,</mark> 

3 <mark>value1_lst : np . ndarray ,</mark> 4 <mark>value2_lst : np . ndarray ,</mark> 5 <mark>capacity :</mark> **<mark>float</mark>** <mark>) -> np . ndarray :</mark> 6 <mark># Randomly sample a base solution</mark> 7 <mark>selected_solution , _ = random . choice ( archive )</mark> 8 <mark>neighbor_solution = selected_solution . copy ()</mark> 9 <mark>num_items =</mark> **<mark>len</mark>** <mark>( weight_lst )</mark> 10 11 <mark># Flip 1 to 3 random items with feasibility check</mark> 12 **<mark>for</mark>** <mark>_</mark> **<mark>in range</mark>** <mark>( random . randint (1, 3)):</mark> 13 <mark>item_index = random . randint (0, num_items - 1)</mark> 14 <mark>neighbor_solution [ item_index ] = 1 - neighbor_solution [ item_index ]</mark> 15 16 <mark># Undo flip if capacity exceeded</mark> 17 <mark>while np . dot ( neighbor_solution , weight_lst ) > capacity :</mark> 18 <mark>neighbor_solution [ item_index ] = 1 - neighbor_solution [ item_index ]</mark> 19 <mark>item_index = random . randint (0, num_items - 1)</mark> 20 <mark>neighbor_solution [ item_index ] = 1 - neighbor_solution [ item_index ]</mark> 21 22 **<mark>return</mark>** <mark>neighbor_solution</mark> 

### **Bi-CVRP** 

**# Best hypervolume** # score = [0.417, 0.158] 1 **<mark>def</mark>** <mark>select_neighbor ( archive : List [ Tuple [ np . ndarray , Tuple [</mark> **<mark>float</mark>** <mark>,</mark> **<mark>float</mark>** <mark>]]],</mark> 2 <mark>coords : np . ndarray ,</mark> 3 <mark>demand : np . ndarray ,</mark> 4 <mark>distance_matrix : np . ndarray ,</mark> 5 <mark>capacity :</mark> **<mark>float</mark>** <mark>) -> np . ndarray :</mark> 6 <mark># Select a solution with best makespan (2nd objective)</mark> 7 <mark>best_solution , _ =</mark> **<mark>min</mark>** <mark>( archive , key = lambda x: x [1][1])</mark> 8 <mark>neighbor_solution = [ np . copy ( route )</mark> **<mark>for</mark>** <mark>route</mark> **<mark>in</mark>** <mark>best_solution ]</mark> 9 10 <mark># Choose two distinct routes</mark> 11 <mark>route_from_index = np . random . choice (</mark> **<mark>len</mark>** <mark>( neighbor_solution ))</mark> 12 <mark>route_to_index = np . random . choice ([ i</mark> **<mark>for</mark>** <mark>i</mark> **<mark>in range</mark>** <mark>(</mark> **<mark>len</mark>** <mark>( neighbor_solution ))</mark> **<mark>if</mark>** <mark>i != route_from_index ])</mark> 13 14 **<mark>if len</mark>** <mark>( neighbor_solution [ route_from_index ]) > 2 and</mark> **<mark>len</mark>** <mark>( neighbor_solution [ route_to_index ]) > 2:</mark> 15 <mark># Select customers (excluding depot)</mark> 16 <mark>customer_from_index = np . random . randint (1,</mark> **<mark>len</mark>** <mark>( neighbor_solution [ route_from_index ]) - 1)</mark> 17 <mark>customer_to_index = np . random . randint (1,</mark> **<mark>len</mark>** <mark>( neighbor_solution [ route_to_index ]) - 1)</mark> 18 19 <mark>customer_from = neighbor_solution [ route_from_index ][ customer_from_index ]</mark> 20 <mark>customer_to = neighbor_solution [ route_to_index ][ customer_to_index ]</mark> 21 22 <mark># Swap the customers</mark> 23 <mark>neighbor_solution [ route_from_index ][ customer_from_index ] = customer_to</mark> 24 <mark>neighbor_solution [ route_to_index ][ customer_to_index ] = customer_from</mark> 25 26 <mark># Validate route demands</mark> 27 <mark>demand_from = np .</mark> **<mark>sum</mark>** <mark>( demand [ neighbor_solution [ route_from_index ]])</mark> 28 <mark>demand_to = np .</mark> **<mark>sum</mark>** <mark>( demand [ neighbor_solution [ route_to_index ]])</mark> 29 30 **<mark>if</mark>** <mark>demand_from > capacity or demand_to > capacity :</mark> 31 <mark># Revert if infeasible</mark> 32 <mark>neighbor_solution [ route_from_index ][ customer_from_index ] = customer_from</mark> 33 <mark>neighbor_solution [ route_to_index ][ customer_to_index ] = customer_to</mark> 

34 

35 **<mark>return</mark>** <mark>neighbor_solution</mark> 

**# Best running time** 

# score = [0.146, 0.033] 

1 **<mark>def</mark>** <mark>select_neighbor ( archive : List [ Tuple [ np . ndarray , Tuple [</mark> **<mark>float</mark>** <mark>,</mark> **<mark>float</mark>** <mark>]]],</mark> 2 <mark>coords : np . ndarray ,</mark> 3 <mark>demand : np . ndarray ,</mark> 4 <mark>distance_matrix : np . ndarray ,</mark> 5 <mark>capacity :</mark> **<mark>float</mark>** <mark>) -> np . ndarray :</mark> 6 <mark># Select route with smallest makespan</mark> 7 <mark>min_makespan_solution =</mark> **<mark>min</mark>** <mark>( archive , key = lambda x: x [1][1])</mark> 8 <mark>routes = min_makespan_solution [0]</mark> 9 10 <mark># Choose two distinct routes</mark> 11 <mark>route1_index , route2_index = np . random . choice (</mark> **<mark>len</mark>** <mark>( routes ), 2, replace =</mark> **<mark>False</mark>** <mark>)</mark> 12 <mark>route1 = routes [ route1_index ]</mark> 13 <mark>route2 = routes [ route2_index ]</mark> 14 15 **<mark>if len</mark>** <mark>( route1 ) > 2 and</mark> **<mark>len</mark>** <mark>( route2 ) > 2:</mark> 16 <mark># Choose customers (excluding depot)</mark> 17 <mark>customer1_index = np . random . randint (1,</mark> **<mark>len</mark>** <mark>( route1 ) - 1)</mark> 18 <mark>customer2_index = np . random . randint (1,</mark> **<mark>len</mark>** <mark>( route2 ) - 1)</mark> 19 20 <mark>customer1 = route1 [ customer1_index ]</mark> 21 <mark>customer2 = route2 [ customer2_index ]</mark> 22 23 <mark># Attempt to swap</mark> 24 <mark>new_route1 = route1 . copy ()</mark> 25 <mark>new_route2 = route2 . copy ()</mark> 26 <mark>new_route1 [ customer1_index ], new_route2 [ customer2_index ] = customer2 , customer1</mark> 27 28 <mark># Check if feasible</mark> 29 <mark>demand1 = np .</mark> **<mark>sum</mark>** <mark>( demand [ new_route1 [1: -1]])</mark> 30 <mark>demand2 = np .</mark> **<mark>sum</mark>** <mark>( demand [ new_route2 [1: -1]])</mark> 31 32 **<mark>if</mark>** <mark>demand1 <= capacity and demand2 <= capacity :</mark> 33 <mark>routes [ route1_index ] = new_route1</mark> 34 <mark>routes [ route2_index ] = new_route2</mark> 35 **<mark>else</mark>** <mark>:</mark> 36 <mark># Fallback: remove and insert</mark> 37 <mark>idx_remove = np . random . randint (1,</mark> **<mark>len</mark>** <mark>( route1 ) - 1)</mark> 38 <mark>customer = route1 [ idx_remove ]</mark> 39 <mark>new_route1 = np . delete ( route1 , idx_remove )</mark> 40 41 **<mark>if</mark>** <mark>np .</mark> **<mark>sum</mark>** <mark>( demand [ new_route1 [1: -1]]) + demand [ customer ] <= capacity :</mark> 42 <mark>routes [ route1_index ] = new_route1</mark> 43 <mark>routes [ route2_index ] = np . insert ( route2 , -1, customer )</mark> 44 45 **<mark>return</mark>** <mark>routes</mark> 

## **H Comparison to Neural Combinatorial Optimization** 

Table 9: Performance comparison across all benchmarks against Neural Combinatorial Optimization methods. 

|Method|B<br>|i-TSP<br>|20<br>||Bi-TSP<br>|50<br>||Bi-TSP<br>|100<br>||Tri-TS<br>|P20<br>||Tri-TSP<br>|50<br>||Tri-TSP<br>|100<br>|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||HV_↑_|Gap|Time_↓_|HV_↑_|Gap|Time_↓_|HV_↑_|Gap|Time_↓_|HV_↑_|Gap|Time_↓_|HV_↑_|Gap|Time_↓_|HV_↑_|Gap|Time_↓_|
|PMOCO|0.632|0.31|3.739|0.637|0.93|5.405|0.699|1.82|7.952|0.470|1.67|4.448|0.436|30.68|5.596|0.490|4.10|9.296|
|NHDE-P|0.630|0.63|3.373|0.510|20.68|9.250|0.703|1.26|11.907|0.474|0.83|14.580|0.629|**0.00**|25.123|0.506|0.97|65.506|
|NHDE-M|0.634|**0.00**|93.421|0.643|**0.00**|157.843|0.712|**0.00**|328.562|0.476|0.41|1195.237|0.447|28.93|1498.893|0.511|**0.00**|3612.458|
|MPaGE (best)|0.629|0.78|4.429|0.542|15.70|6.950|0.442|37.92|12.719|0.478|0.00|8.112|0.220|65.02|14.747|0.109|78.66|26.394|
|Method|HV_↑_|Bi-KP<br>Gap|50<br>Time_↓_|HV_↑_|Bi-KP1<br>Gap|00<br>Time_↓_|HV_↑_|Bi-KP2<br>Gap|00<br>Time_↓_|HV_↑_|Bi-CVR<br>Gap|P20<br>Time_↓_|HV_↑_|Bi-CVR<br>Gap|P50<br>Time_↓_|B<br>HV_↑_|i-CVR<br>Gap|P100<br>Time_↓_|
|PMOCO|0.378|0.00|5.415|0.441|9.25|8.597|0.350|5.14|11.060|0.407|28.34|5.221|0.413|9.03|9.684|0.329|22.03|14.759|
|NHDE-P|0.371|1.85|4.681|0.431|11.31|8.224|0.359|2.71|14.092|0.411|27.64|3.509|0.432|4.84|5.981|0.380|9.95|10.747|
|NHDE-M|0.353|6.61|283.514|0.453|6.79|502.367|0.369|**0.00**|897.214|0.421|25.88|213.678|0.441|2.86|299.112|0.396|6.16|655.309|
|MPaGE (best)|0.359|5.02|2.647|0.486|**0.00**|1.859|0.197|46.61|2.118|0.568|**0.00**|0.072|0.454|**0.00**|0.191|0.422|**0.00**|0.359|



In this section, we compare our proposed MPaGE method against three representative NCO-based baselines: PMOCO, NHDE-P, and NHDE-M (Chen et al. 2023b; Lin, Yang, and Zhang 2022). As shown in Table 9, MPaGE achieves the best solution quality, measured by hypervolume (HV), in 5 out of 12 benchmarks, while consistently offering substantial runtime advantages. For instance, it is over 100 _×_ faster than NHDE-M on Tri-TSP50 (14.75s and 1498.89s) and achieves a 137 _×_ speedup on Tri-TSP100. Notably, MPaGE outperforms all NCO baselines in both hypervolume and runtime across all BiCVRP instances, demonstrating its strength not only in efficiency but also in solution quality on challenging vehicle routing problems. Although NCO methods can achieve strong results when carefully trained, a critical limitation is their reliance on retraining from scratch whenever the instance size changes to obtain better result, which incurs significant overhead and restricts scalability. In contrast, MPaGE generalizes seamlessly across problem sizes without any retraining. These results suggest that MPaGE offers a compelling trade-off between quality and efficiency, combining competitive hypervolume performance with strong adaptability and fast inference, making it more suitable for practical deployment. 

