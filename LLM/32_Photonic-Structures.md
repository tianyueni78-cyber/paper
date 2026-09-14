# **Optimizing Photonic Structures with Large Language Model Driven Algorithm Discovery** 

Haoran Yin 

h.yin@liacs.leidenuniv.nl LIACS, Leiden University Leiden, Netherlands 

Thomas Bäck 

t.h.w.baeck@liacs.leidenuniv.nl 

LIACS, Leiden University Leiden, Netherlands 

## **Abstract** 

We study how large language models can be used in combination with evolutionary computation techniques to automatically discover optimization algorithms for the design of photonic structures. Building on the Large Language Model Evolutionary Algorithm (LLaMEA) framework, we introduce structured prompt engineering tailored to multilayer photonic problems such as Bragg mirror, ellipsometry inverse analysis, and solar cell antireflection coatings. We systematically explore multiple evolutionary strategies, including (1+1), (1+5), (2+10), and others, to balance exploration and exploitation. Our experiments show that LLM-generated algorithms, generated using small-scale problem instances, can match or surpass established methods like quasi-oppositional differential evolution on large-scale realistic real-world problem instances. Notably, LLaMEA’s self-debugging mutation loop, augmented by automatically extracted problem-specific insights, achieves strong anytime performance and reliable convergence across diverse problem scales. This work demonstrates the feasibility of domain-focused LLM prompts and evolutionary approaches in solving optical design tasks, paving the way for rapid, automated photonic inverse design. 

## **CCS Concepts** 

• **Theory of computation** → **Design and analysis of algorithms** ; **Optimization with randomized search heuristics** ; _Continuous optimization_ ; _Evolutionary algorithms_ ; • **Computing methodologies** → **Heuristic function construction** ; • **Applied computing** → _Physics_ . 

## **Keywords** 

Large Language Models, Automated Algorithm Design, Photonic Structures, Evolutionary Strategies, Inverse Design, Black-Box Optimization, Domain-Specific Prompting, Photonics Benchmarking 

Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. Copyrights for components of this work owned by others than the author(s) must be honored. Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires prior specific permission and/or a fee. Request permissions from permissions@acm.org. _Conference acronym ’XX, Woodstock, NY_ 

© 2018 Copyright held by the owner/author(s). Publication rights licensed to ACM. ACM ISBN 978-1-4503-XXXX-X/2018/06 

https://doi.org/XXXXXXX.XXXXXXX 

Anna V. Kononova 

a.kononova@liacs.leidenuniv.nl 

LIACS, Leiden University 

Leiden, Netherlands 

Niki van Stein 

n.van.stein@liacs.leidenuniv.nl LIACS, Leiden University Leiden, Netherlands 

#### **ACM Reference Format:** 

Haoran Yin, Anna V. Kononova, Thomas Bäck, and Niki van Stein. 2018. Optimizing Photonic Structures with Large Language Model Driven Algorithm Discovery. In _Proceedings of Make sure to enter the correct conference title from your rights confirmation email (Conference acronym ’XX)._ ACM, New York, NY, USA, 10 pages. https://doi.org/XXXXXXX.XXXXXXX 

## **1 Introduction** 

Optimization of photonic structures plays a key role in the advancement of technologies in various fields such as telecommunication, solar energy, and materials science [1, 16, 21, 22, 37]. However, the complexity and high dimensionality of these optimization problems pose significant challenges. Recent developments in automatic algorithm design, especially those that utilize large language models (LLMs), offer promising solutions. 

LLMs have become powerful tools in the field of algorithm discovery and optimization. Several studies have demonstrated the ability of LLMs to automatically generate and refine optimization algorithms through an iterative process [19, 33]. By combining the power of large-scale language models with automatic algorithm design, these approaches open new avenues for developing algorithms for complex problems without relevant expertise. 

In this work, we extend the capabilities of the Large Language Model Evolutionary Algorithm (LLaMEA) framework [33] to deal with real-world photonic problems by addressing two critical limitations: 

- **Generic Task Prompts** : Original LLaMEA prompts lacked domain-specific guidance, which can lead to suboptimal algorithm designs for photonic problems. 

- **Limited Evolutionary Strategy Diversity** : Previous studies focused only on simple (1,1) and (1+1) strategies, neglecting the potential of population-based exploration. 

To overcome these limitations, we introduce structured task prompts enriched with photonics-specific problem descriptions and algorithmic insights. Furthermore, we systematically evaluate five new evolutionary strategy configurations-(1,5), (1+5), (2,10), (2+10), and (5+5)-to balance exploration-exploitation trade-offs. 

The paper is organized as follows. Sec. 2 reviews the related work on LLM-driven algorithm discovery and photonic structure optimization problems. Sec. 3 describes the methodology in detail. Sec. 4 provides data related to the experimental setup. Sec. 5 shows 

Conference acronym ’XX, June 03–05, 2018, Woodstock, NY 

Yin et al. 

the experimental results. Sec. 6 summarizes the results of the work and presents future work. 

## **2 Related Work** 

The rapid development of LLMs and optimization techniques has stimulated a strong interest in combining LLM-driven algorithm discovery with domain-specific applications. This section provides an overview of related work in two key areas: algorithmic automatic generation tools using LLMs and photonic structure optimization problems. 

## **2.1 Large Language Models for Algorithm Discovery** 

Recent research has explored how LLMs can contribute to algorithmic discovery [20]. Two state-of-the-art representative frameworks in this area are Evolution of Heuristic (EoH) and LLaMEA [19, 33]. Both frameworks illustrate the potential of LLMs to automate and accelerate algorithmic discovery. 

EoH combines LLMs with evolutionary computation to iteratively generate and refine heuristics. These heuristics are small functions that are then inserted into a larger code template before the evaluation of a problem. It evolves both natural-language descriptions of heuristics and executable code representations of these heuristics, allowing for diverse exploration and efficient improvement. EoH demonstrates state-of-the-art performance in heuristic automated design on combinatorial optimization problems, outperforming existing methods such as FunSearch on bin-packing and traveling salesperson problems [19]. 

LLaMEA also uses LLMs within an evolution algorithm framework, focusing mainly on the (1,1) and (1+1) evolutionary strategies, to automatically generate, mutate and optimize complete metaheuristics [28, 33]. Unlike EoH’s emphasis on ‘thought’, LLaMEA directly optimizes the algorithm itself, using run-time performance as feedback for iterative improvement. In benchmarking continuous problems, it produces algorithms that are comparable to or better than state-of-the-art optimization methods such as the covariance matrix adaptation evolution strategy (CMA-ES) and differential evolution (DE) [33]. Furthermore, the recently proposed LLaMEAHPO framework augments LLaMEA with automated hyperparameter tuning, offloading parameter optimization from the LLM and thereby boosting algorithm quality while reducing the overall LLM query cost [34]. 

While both EoH and LLaMEA are open-source and easy to extend, we chose to base this research on LLaMEA due to it’s superior performance for discovering algorithms in the black-box optimization domain and for its ability to generate and optimize large code-bases. 

## **2.2 Earlier Methods for Automated Algorithm Discovery** 

Beyond EoH and LLaMEA, a variety of other frameworks explore how LLMs can automate algorithm discovery. One of the earliest works is _FunSearch_ [29], which applies an LLM within a distributed evolutionary search over function spaces. Starting from seed functions, FunSearch evolves them by prompting the LLM for refined or alternative code. 

(AEL) [18] and _ReEvo_ [35], similarly integrate LLMs within an iterative loop, generating small heuristic code snippets and improving them via mutation and crossover prompts. While EoH focuses on heuristics in text and code form, AEL/ReEvo explore a closely related direction by evolving coded modules. Both frameworks have shown promising results on combinatorial benchmarks such as the Traveling Salesperson Problem. 

## **2.3 Optimization of Photonic Structures** 

Optimization of photonic structures has been an important area of research, as the need for high efficiency and high precision drives the optimization of photonic structures in various applications such as communication, semiconductors, LED displays, materials analysis and solar cells [1, 16, 21, 22, 37]. The following are three real-world problems related to global optimization of multilayered photonic structures, all of which have vital applications. 

_Bragg Mirror._ A Bragg reflector mirror, or Bragg mirror, is a series of two or more semiconductors or dielectric materials stacked in a staggered pattern to achieve high reflectivity in a particular optical band [4]. It has a wide range of applications, such as the construction of acoustic wave reflectors and filters [26], the analysis of the crystal structure of materials [24], the improvement of solar cell efficiency [15], the detection of changes in physical quantities such as temperature and pressure [10], and the enhancement of the interaction between light and matter in quantum computation and quantum information [23]. 

_Ellipsometry Inverse Problem._ Ellipsometry is a nondestructive optical measurement technique that can be used to measure the thickness of the thin film, the refractive index and the absorption coefficients [30]. In chip fabrication, the properties of thin films have a critical impact on circuit performance [38]. The solution of the inverse problem of ellipsometry can help to improve the accuracy of the production process [32]. It can also be used in the new energy and chemical industry to study the properties of solar cell materials, nanostructured thin films, and chemical coatings [8]. Ellipsometry inverse problem solving can not only improve the data analysis method in materials science, but also improve the applicability of thin film technology in industrial production [9, 13, 31]. 

_Photovoltaic Problem._ This refers to the design of a sophisticated antireflection coating for solar cells - a multilayer thin film structure optimized to minimize optical reflections and maximize the absorption of the active layer of the cell. Such coatings typically consist of alternating dielectric layers with different refractive indices. By suppressing surface reflection losses, a well-designed antireflective coating can significantly improve the power conversion efficiency of a solar cell (bare silicon surfaces, for instance, reflect 30% of incident sunlight) [14]. The difficulty lies in achieving broad-band, all-encompassing antireflection: single-layer coatings can only eliminate reflections in narrow bands, so multilayer or graded index designs are needed to reduce reflectivity across the entire broad solar spectrum. Optimizing such coatings is a complex photonic inverse design problem, with many local minima in performance due to wave interference effects at multiple wavelengths [3]. 

Conference acronym ’XX, June 03–05, 2018, Woodstock, NY 

Optimizing Photonic Structures with Large Language Model Driven Algorithm Discovery 







**(a) Bragg mirror (b) ellipsometry (c) photovoltaics** 

**Figure 1: Landscape of photonic structure optimizing problems in 2D. The darker the color, the more fit the structure.** 

## **3 Optimizing Photonic Structures with LLaMEA** 

We apply LLaMEA to real-world problems published by P. Bennet et al. to automatically discover and implement photonic structure optimization algorithms [2, 33]. 

## **3.1 Real-world Problem Simulation** 

Python-based Multilayer Optics Optimization and Simulation Hub (PyMoosh) is a numerical toolkit for calculating the optical properties of multilayer structures [17]. PyMoosh is especially suited for complex problems involving multilayer optical structures (e.g. structural analysis of metallic or metalized layers) and can be extended to support advanced optimization and inverse problem design. 

Building on PyMoosh, P. Bennet et al. have developed a testbed for defining and solving photonic optimization problems [2]. Based on their work, we migrate the following problems to the IOHexperimenter platform [5]. 

- (1) Optimization of a Bragg mirror. 

## **3.3 Automatic Generation of Algorithms** 

We chose LLaMEA as the algorithm discovery method in our experiments for the following reasons: 

- (1) Targeting continuous optimization problems: Our problems are continuous optimization problems, and LLaMEA provides a solution specifically for such problems. It uses automated generation and iterative optimization based on metaheuristic algorithms suitable for dealing with the optimization of continuous variables. 

- (2) Reliable performance: LLaMEA has been shown to perform better than EoH in several complex optimization tasks [33]. 

In our work, we perform rapid validation and benchmarking of algorithms generated on small-scale problem instances, and apply them on more complex problem instances. Feedback such as convergence speed and anytime performance metrics are used as feedback for LLaMEA to iteratively improve algorithms. After many improvements, LLaMEA will provide a number of usable algorithms. The algorithms validated as the best will participate in benchmarking and comparison with other commonly used state-of-the-art optimization algorithms. 

## **4 Experimental Setup** 

The experiments are divided into two main parts: **discovery** and **benchmarking** . That is, LLaMEA is used to search for optimization algorithms, and the algorithms discovered with the best performance are benchmarked against other commonly used optimization algorithms in different instances of the problem. The following content details the experimental setup in terms of problem setup, performance metric, prompt setup for LLM, and benchmarking. 

- (2) Solving of an ellipsometry inverse problem. 

- (3) Design of a sophisticated anti-reflection coating to optimize solar absorption in a photovoltaic solar cell. 

These three problems are all optimization problems for photonic structures and are the focus of the completed benchmark work [3]. Adequate benchmark data on commonly used optimization algorithms in this area are provided for reference. The landscapes of these problems in 2D are shown in Fig. 1. This figure is intended to visualize the problem only, and since the dimensionality of the problem is directly related to the number of layers of the photonic structure, the 2D form of some problems is not of any practical interest. 

## **3.2 Enhanced Task Prompt Design** 

To improve LLaMEA’s ability to address domain-specific problems, we have added two key sections to the original task prompt: 

- Problem Description: A concise summary of the photonic structure optimization task, including key parameters (e.g., range of layer thicknesses, and dielectric constant constraints) and physical objectives (e.g., reflectivity maximization). 

- Algorithmic Insight: Domain knowledge guidance, such as ’Encourage algorithms to detect and preserve modular structures’ or ’Encourage periodicity in solutions through customized cost functions or constraints’. 

These structured suggestions could lead to more specialized algorithms that perform better for photon-specific requirements. 

## **4.1 Problem Setup** 

_4.1.1 Bragg Mirror._ For the Bragg mirror optimization problem, we set the optimization objective to find a photonic structure that has the strongest reflectance for light with a wavelength of 600 nm. The permittivity of the first material is 1 _._ 96, the permittivity of the other material is 3 _._ 24, and the maximum thickness of each layer is 218 nm. The problem instance with 10 layers of alternating materials will collectively be referred to as _mini-Bragg_ , and those with 20 layers of alternating materials will collectively be referred to as _Bragg_ . 

_4.1.2 Ellipsometry Inverse Problem._ Regarding the ellipsoidal inverse problem, the substrate material is gold. The parameters of the reflective material to be solved include thickness and permittivity. The minimum thickness is 50 nm, the maximum thickness is 150 nm, the minimum permittivity is 1 _._ 1, and the maximum permittivity is 3 _._ 0. The number of layers of material is 1. The problem instance in the latter collectively is referred to as _ellipsometry_ . 

_4.1.3 Photovoltaic Problem._ The optimization objective for the instances of the photovoltaic problem is to optimize the photonic structure to improve solar absorption, with the thickness of each material layer ranging from 30 to 250 nm. The permittivity is 2 _._ 0 for the first material and 3 _._ 0 for the other. The substrate material parameters are set as default. Similarly, we call an instance with 10 layers _photovoltaic_ , 20 layers _big-photovoltaic_ , and 32 layers _hugephotovoltaic_ . 

Conference acronym ’XX, June 03–05, 2018, Woodstock, NY 

Yin et al. 

**Table 1: Parameter settings for different problem instances. Different columns of thickness and permittivity correspond to different materials. Algorithm discovery process for different problems are based on instances with** ♠ **respectively.** 

|instances|_mini-_|_Bragg_♠|_Bra_|_gg_|_ellipsometry_♠|_phot_|_ovoltaic_♠|_big-p_|_hotovoltaic_|_huge_|_-photovoltaic_|
|---|---|---|---|---|---|---|---|---|---|---|---|
|layers||10|20||1||10||20||32|
|materials||2|2||1||2||2||2|
|min thickness(nm)|0|0|0|0|50|30|30|30|30|30|30|
|max thickness(nm)|218|218|218|218|150|250|250|250|250|250|250|
|min permittivity<br>max permittivity|1.96|3.24|1.96|3.24|1.1<br>3.0|2.0|3.0|2.0|3.0|2.0|3.0|
|evaluation budget|1|0000|200|00|1000||5000||10000||16000|



All problem instances are set as **minimization** problems. The algorithm discovery processes are based only on smaller instances, and the subsequent benchmarks on the best algorithms are based on all instances. Table 1 shows the evaluation budget and summarizes the parameter settings described above. 

## **4.2 Performance Metric** 

We use the metric suggested by LLaMEA, AOCC, as a feedback to the LLM. Eq. 1 is the definition of AOCC: 



where _𝑦𝑎,𝑓_ is a series of log-scaled current-best fitness value of _𝑓_ during the running of optimization algorithm _𝑎_ , _𝐵_ is the evaluation budget, _𝑦𝑖_ is the _𝑖_ -th element of _𝑦𝑎,𝑓_ , _𝑢𝑏_ is the upper bound of _𝑓_ , and _𝑙𝑏_ is the lower bound of _𝑓_ . In addition to the AOCC used by LLaMEA, we also add the optimal fitness value found at the end of the algorithm runs, _𝑦_<sup>∗</sup> , to the feedback. 

The algorithm discoveries are built on _mini-Bragg_ , _ellipsometry_ , and _photovoltaic_ , respectively. _𝑢𝑏_ is set to 1 _._ 0 for _mini-Bragg_ and _photovoltaic_ , and 40 _._ 0 for _ellipsometry_ . 

## **4.3 Prompt Setup** 

The high degree of freedom in prompt customization is also a feature of LLaMEA, which uses the task prompt, the mutation prompt, the feedback prompt, and the output prompt, the first three of which are modified in our experiments. 

Firstly, we state in the task prompt that the goal of the task is to find algorithms suitable for the optimization of multilayer photonic structures: 

### **Task Prompt** 

The optimization algorithm should be able to find highperformance solutions to a wide range of tasks, which include evaluation on real-world applications such as, e.g., optimization of multilayered photonic structures. _<problem description> <algorithmic insight>_ 

Your task is to write the optimization algorithm in Python code. The code should contain an ‘__init__(self, budget, dim)‘ function and the function ‘def __call__(self, func)‘, 

which should optimize the black box function ‘func‘ using ‘self.budget‘ function evaluations. 

The func() can only be called as many times as the budget allows, not more. Each of the optimization functions has a search space between func.bounds.lb (lower bound) and func.bounds.ub (upper bound). The dimensionality can be varied. 

Give an excellent and novel heuristic algorithm to solve this task and also give it a one-line description with the main idea. 

where **problem description** and **algorithmic insight** are obtained by sending the following meta-prompts to gpt-4o-2024-08-06: 

### **Meta-prompt for generating problem description** 

Please read _Illustrated tutorial on global optimization in nanophotonics_ first [3]. Then, give me summaries of bragg mirror problem, ellipsometry problem, and photovoltaics problem, respectively. The generated summaries need to be used in other chatgpt chats, so make sure they are understood by chatgpt. 

### **Meta-prompt for generating algorithmic insight** 

Please give me algorithmic insights of these three problems respectively. Similarly, these insights are used in other chatgpt chats, prompting chatgpt to generate optimization algorithms applicable to these problems, so make sure that these insights are understood by chatgpt. 

All descriptions and insights can be found in the supplementary material and the problem description and algorithmic insights for the Bragg mirror are as follows: 

### **Problem description for Bragg mirror** 

**The Bragg mirror optimization** aims to maximize reflectivity at a wavelength of 600 nm using a multilayer structure 

Conference acronym ’XX, June 03–05, 2018, Woodstock, NY 

Optimizing Photonic Structures with Large Language Model Driven Algorithm Discovery 

with alternating refractive indices (1.4 and 1.8). The structure’s thicknesses are varied to find the configuration with the highest reflectivity. The problem involves two cases: one with 10 layers (minibragg) and another with 20 layers (bragg), with the latter representing a more complex inverse design problem. The known optimal solution is a periodic Bragg mirror, which achieves the best reflectivity by leveraging constructive interference. This case exemplifies challenges such as multiple local minima in the optimization landscape. 

Finally, in the feedback prompt, we provide both AOCC and _𝑦_<sup>∗</sup> information to help LLM better establish the connection between algorithmic implementation and real-world results as a way to improve existing algorithms in a targeted manner: 

### **Feedback Prompt** 

The algorithm <name> got an average Area over the convergence curve (AOCC, 1.0 is the best) score of <aocc_score> with standard deviation <aocc_std>. And the mean value of best solutions found was <y_best> (0. is the best) with standard deviation <y_best_std>. 

### **Algorithmic insight for Bragg mirror** 

For this problem, the optimization landscape contains multiple local minima due to the wave nature of the problem. And periodic solutions are known to provide near-optimal results, suggesting the importance of leveraging constructive interference principles. Here are some suggestions for designing algorithms: 1. Use global optimization algorithms like Differential Evolution (DE) or Genetic Algorithms (GA) to explore the parameter space broadly. 2. Symmetric initialization strategies (e.g., Quasi-Oppositional DE) can improve exploration by evenly sampling the search space. 3. Algorithms should preserve modular characteristics in solutions, as multilayer designs often benefit from distinct functional blocks. 4. Combine global methods with local optimization (e.g., BFGS) to fine-tune solutions near promising regions. 5. Encourage periodicity in solutions via tailored cost functions or constraints. 

For each problem, we experiment with the task prompt without problem description and algorithmic insight, with problem description, and with both problem description and algorithmic insight. For each task prompt setting, LLaMEA runs 5 times with an evolutionary strategy (1 + 1), generating 100 algorithms per run. Each algorithm is executed 3 times to eliminate experimental randomness. 

Secondly, the dynamic mutation controlling prompt is set to control the LLaMEA mutation process, as this prompt has been validated to have better mutation control when combined with gpt-4o [36] with the fast mutation operator [6]: 

### **Dynamic Mutation Controlling Prompt** 

Refine the strategy of the selected solution to improve it. Make sure that you only change _𝑥_ % of the code, which means if the code has 100 lines, you can only change ⌊ _𝑥_ ⌋ lines, and the rest lines should remain the same. For this code, it has _𝑛_ lines, so you can only change min(⌊ _𝑛_ × _𝑥_ /100⌋ _,_ 1) lines, the rest _𝑛_ − min(⌊ _𝑛_ × _𝑥_ /100⌋ _,_ 1) lines should remain the same. This changing rate _𝑥_ % is the mandatory requirement, you cannot change more or less than this rate. 

The mutation rate _𝑥_ in the dynamic mutation control prompt is sampled from the heavy-tailed distribution known as the fast mutation operator [6]. 

## **4.4 Evolutionary Strategy Exploration** 

After confirming which task prompt setting works best, we use that task prompt setting in the following experiments. 

In addition to the initial (1,1) and (1+1) strategies, which are the default for LLaMEA, we investigate five other configurations of evolutionary strategies: 

- Comma strategy: (1,5), (2,10) 

- The plus strategy: (1+5), (2+10), (5+5) 

These configurations are often used in the black-box optimization literature, as they can balance exploration (by expanding the population of offspring) and exploitation (by retaining the elite), with _𝜆_ denoting the number of offspring and _𝜇_ denoting the number of parents, and are indicated by ( _𝜇, 𝜆_ ) [28]. 

For each of the configurations, LLaMEA runs 5 times for each problem instance, and during each run, LLaMEA generates 100 algorithms. Each algorithm is executed 3 times to eliminate experimental randomness. 

## **4.5 Benchmarking** 

After the algorithm discovery step, for each problem, we have 2500 generated algorithms. Of these, the first 3 algorithms with the best AOCC average participate in the final benchmark. The optimal algorithms discovered through _mini-Bragg_ and _photovoltaic_ are also applied to higher-dimensional problem instances. In addition, five algorithms commonly used in the field of photonic structure optimization are added to the benchmark to provide a performance comparison, including DE [7], CMA-ES [11], Broyden–Fletcher–Goldfarb–Shanno (BFGS) [12], quasi-Newton differential evolution (QNDE) [25], and quasi-oppositional differential evolution (QODE) [27]. For each problem instance, each algorithm is executed 15 times. 

## **5 Results** 

This chapter presents the results of the experiments, for which the raw data and associated code are publicly available<sup>1</sup> . 

## **5.1 Enhanced Task Prompt Design** 

The integration of domain-specific knowledge into structured prompts greatly influences the quality of the algorithms generated by LLaMEA. For the Bragg mirror designing and ellipsometry inverse problems, the detailed problem descriptions and algorithmic insights (see 

1https://doi.org/10.5281/zenodo.15073784 

Conference acronym ’XX, June 03–05, 2018, Woodstock, NY 

Yin et al. 





<!-- Start of picture text -->
(a)  mini-Bragg ♠<br>(b)  ellipsometry  ♠<br><!-- End of picture text -->

**Figure 2: Examples of task prompts that add problem descriptions and algorithm insights that improve the performance of LLaMEA. The higher the AOCC, the better. Prompts with descriptions and insights both outperform other prompt settings for** **_mini-Bragg_ and** **_ellipsometry_ instances.** 

Appendix A) guided LLM to prioritize strategies that were consistent with physical principles. For example, prompts emphasizing ’periodic solutions’ and ’constructive interference’ motivate the algorithms to use modular initialization and symmetry constraints, which are essential for Bragg reflector optimization, as shown in Fig. 2a. These prompts explicitly encourage the use of hybrid global-local search methods, e.g. combining DE and BFGS for local refinement, which improves AOCC by 10% compared to general prompts. For ellipsometry, problem description and algorithmic insight provide more significant improvements. 

However, in the photovoltaic problem, prompts without domainspecific insights outperformed the augmented variant, as shown in Fig. 3a. This counterintuitive result may be due to the the noisy fitness landscape of the photovoltaic task, where an overly detailed large prompt may prematurely limit exploration. Considering that all prompt settings in Fig. 3a start with a high AOCC, we let each 





<!-- Start of picture text -->
(a)  photovoltaic  ♠<br><!-- End of picture text -->



**(b)** **_photovoltaic_** ♠ **, all runs start with the same solution.** 

**Figure 3: Example of a task prompt that adds a problem description and algorithm insight that does not improve the effectiveness of LLaMEA. The higher the AOCC, the better. For** **_photovoltaic_ instance, task prompts without description and insight works best. Considering that the initial AOCC is high for all task prompt settings, Fig. 3b shows the results for each LLaMEA run starting from the same solution to avoid the impact of initial gaps.** 

LLaMEA run starting from the same solution to avoid the impact of initial gaps. However, the new and more reliable experimental results in Fig. 3b still show that a large prompt may pose a limitation. 

## **5.2 Evolutionary Strategy Exploration** 

The impact of the choice of evolutionary strategy on the performance of the algorithm varies according to the problem. In the Bragg mirror, as well as the ellipsometry problem, the (5+5) strategy (5 parents, 5 children) finally achieves the highest AOCC, as shown in Figs. 4a and 4b, taking full advantage of the population diversity to exploit periodic solutions while retaining elite individuals for local improvement. In contrast, the photovoltaic problem favored the (1+5) strategy, as shown in Fig. 4c. Furthermore, while 

Conference acronym ’XX, June 03–05, 2018, Woodstock, NY 

Optimizing Photonic Structures with Large Language Model Driven Algorithm Discovery 









<!-- Start of picture text -->
(a)  mini-Bragg ♠ (b)  ellipsometry  ♠ (c)  photovoltaic  ♠<br><!-- End of picture text -->

**Figure 4: Impact of different ES strategy choices. The preference for ES strategies is different for each problem and most of the time the difference is not significant.** 









<!-- Start of picture text -->
(a)  mini-Bragg ♠ (b)  Bragg (c)  ellipsometry  ♠<br>(d)  photovoltaic  ♠ (e)  big-photovoltaic (f)  huge-photovoltaic<br><!-- End of picture text -->

**Figure 5: Convergency curves of best algorithms found by LLaMEA and baselines with different problem instances, averaged over 15 runs.** _𝑦_ **-axis represents fitness, the smaller, the better.** _𝑥_ **-axis represents evaluations of problem instances. Each subfigure represents a problem instance.** 

there are differences between the performance of these strategies, they are not significant. 

## **5.3 Algorithms Benchmarking** 

Fig. 5 shows the best 3 optimal algorithms found by LLaMEA for each of the 6 instances of 3 problems, compared to the commonly used algorithms. From Figs. 5a and 5b, we find that the algorithms found by LLaMEA demonstrate a significantly more rapid convergence trend. However, the optimal algorithms found by LLaMEA 

for ellipsometry are all good at finding a local optimum at the initial stage, as shown in Fig. 5c. For the three instances of the photovoltaic problem, algorithms discovered by LLaMEA are not the best, but still show faster convergence. 

Fig. 6 shows the distribution of the fitness value of the optimal solutions found by different algorithms for different problem instances after 15 runs. We find that the optimal algorithms found by LLaMEA perform very well and are basically comparable to the best algorithms. Especially for Bragg mirror problem instances, 

Conference acronym ’XX, June 03–05, 2018, Woodstock, NY 

Yin et al. 









<!-- Start of picture text -->
(a)  mini-Bragg ♠ (b)  Bragg (c)  ellipsometry  ♠<br>(d)  photovoltaic  ♠ (e)  big-photovoltaic (f)  huge-photovoltaic<br><!-- End of picture text -->

**Figure 6: Distribution of best structure found by different algorithms.** _𝑦_ **-axis represent fitness of photonic structure.** _𝑥_ **-axis represent different algorithms. Each subfigure represents a problem instance.** 

the found algorithms not only reliably find the optimal solutions but also the distribution is concentrated, which means that the performances are unfathomably stable. For photovoltaic problem instances, the algorithms found are relatively less stable but still reliable. 

## **6 Conclusions** 

This study demonstrates the potential of making real-world problemrelated descriptions as well as algorithmic insights available to LLM and combining them with different evolutionary strategies for automatic algorithm discovery in photonic structure optimization. By embedding domain-specific knowledge into the structured task prompt, the algorithms generated by LLaMEA achieve advanced performance on real-world problems in comparison to other widely used successful algorithms in the area of photonic structure optimization. Key findings include: 

- Embedding domain-specific photonics knowledge into the LLM prompt, combined with evolutionary search strategies, enables automated discovery of optimization algorithms that achieve high performance in photonic structure design. 

- In complex photonic optimization tasks, LLM generates algorithms that can match or even surpass state-of-the-art methods (e.g., DE and CMA-ES) with performance comparable to human-designed heuristics. 

- Systematic tests using a variety of evolutionary strategies (e.g., (1 + 1), (5 + 5) and (2 + 10)) show that while different 

- strategies affect the performance of a given problem (e.g., the (5 + 5) strategy performs well in the Bragg reflector and ellipsometry tasks while the (1+5) strategy performs moderately well in the photovoltaic task), the overall difference in performance is not significant. 

- The algorithms found by LLM consistently find near-optimal solutions for each photonic design benchmark; in particular, they achieve very consistent results for Bragg mirror designs (reliably converging to the global optimum with small performance differences) and provide reliable results for challenging PV cases (with slightly larger differences, but still strong performance). 

In summary, these findings confirm that LLM-driven automatic algorithm design can effectively automate the design of optimization algorithms for realistic photonic problems, paving the way for the fast and cost-effective design of photonic structures without the need for significant human intervention. 

## **References** 

- [1] Sameh O Abdellatif and Gehad Ali Alsayed. 2019. Optimizing 1D photonic crystal structures for thin film solar cells. In _2019 IEEE Conference on Power Electronics and Renewable Energy (CPERE)_ . IEEE, 333–337. 

- [2] Pauline Bennet, Emmanuel Centeno, Jérémy Rapin, Olivier Teytaud, and Antoine Moreau. 2020. The photonics and ARCoating testbeds in Nevergrad. (May 2020). https://hal.science/hal-02613161 working paper or preprint. 

- [3] Pauline Bennet, Denis Langevin, Chaymae Essoual, Abdourahman KhairehWalieh, Olivier Teytaud, Peter Wiecha, and Antoine Moreau. 2024. Illustrated tutorial on global optimization in nanophotonics. _JOSA B_ 41, 2 (2024), A126– A145. 

Conference acronym ’XX, June 03–05, 2018, Woodstock, NY 

Optimizing Photonic Structures with Large Language Model Driven Algorithm Discovery 

- [4] WL Bragg, JJ Thomson, and Herren Friedrich. 1914. Diffraction of short electromagnetic waves. In _Proceedings of the Cambridge Philosophical Society: Mathematical and physical sciences_ , Vol. 17. 43. 

- [5] Jacob de Nobel, Furong Ye, Diederick Vermetten, Hao Wang, Carola Doerr, and Thomas Bäck. 2021. IOHexperimenter: Benchmarking Platform for Iterative Optimization Heuristics. _arXiv e-prints:2111.04077_ (nov 2021). arXiv:2111.04077 https://arxiv.org/abs/2111.04077 

- [6] Benjamin Doerr, Huu Phuoc Le, Régis Makhmara, and Ta Duy Nguyen. 2017. Fast genetic algorithms. In _Proceedings of the genetic and evolutionary computation conference_ . 777–784. 

- [7] Vitaliy Feoktistov. 2006. _Differential evolution_ . Springer. 

- [8] Hiroyuki Fujiwara and Robert W Collins. 2018. _Spectroscopic ellipsometry for photovoltaics_ . Vol. 1. Springer. 

- [9] Débora Gonçalves and Eugene A Irene. 2002. Fundamentals and applications of spectroscopic ellipsometry. _Química Nova_ 25 (2002), 794–800. 

- [10] Michal Gryga, Dalibor Ciprian, and Petr Hlubina. 2022. Distributed Bragg reflectors employed in sensors and filters based on cavity-mode spectral-domain resonances. _Sensors_ 22, 10 (2022), 3627. 

- [11] Nikolaus Hansen, Sibylle D Müller, and Petros Koumoutsakos. 2003. Reducing the time complexity of the derandomized evolution strategy with covariance matrix adaptation (CMA-ES). _Evolutionary computation_ 11, 1 (2003), 1–18. 

- [12] John D Head and Michael C Zerner. 1985. A Broyden—Fletcher—Goldfarb—Shanno optimization procedure for molecular geometries. _Chemical physics letters_ 122, 3 (1985), 264–270. 

- [13] Karsten Hinrichs and Klaus-Jochen Eichhorn. 2018. _Ellipsometry of functional organic surfaces and films_ . Vol. 52. Springer. 

- [14] Chunxue Ji, Wen Liu, Yidi Bao, Xiaoling Chen, Guiqiang Yang, Bo Wei, Fuhua Yang, and Xiaodong Wang. 2022. Recent applications of antireflection coatings in solar cells. In _Photonics_ , Vol. 9. MDPI, 906. 

      2024. Mathematical discoveries from program search with large language models. _Nature_ 625 (01 2024), 468–475. Issue 7995. 

   - [30] Alexandre Rothen. 1945. The ellipsometer, an apparatus to measure thicknesses of thin surface films. _Review of Scientific Instruments_ 16, 2 (1945), 26–30. 

   - [31] Mathias Schubert. 2004. _Infrared ellipsometry on semiconductor layer structures: phonons, plasmons, and polaritons_ . Vol. 209. Springer Science & Business Media. 

   - [32] Ryan G Toomey. 2024. Tackling the inverse problem in ellipsometry: analytic expressions for supported coatings with nonuniform refractive index profiles in the thin film and weak contrast limits. _Physica Scripta_ 99, 3 (2024), 035529. 

   - [33] Niki van Stein and Thomas Bäck. 2024. LLaMEA: A Large Language Model Evolutionary Algorithm for Automatically Generating Metaheuristics. _IEEE Transactions on Evolutionary Computation_ (2024), 1–1. doi:10.1109/TEVC.2024. 3497793 

   - [34] Niki van Stein, Diederick Vermetten, and Thomas Bäck. 2024. In-the-loop hyperparameter optimization for llm-based automated design of heuristics. _arXiv preprint arXiv:2410.16309_ (2024). 

   - [35] Haoran Ye, Jiarui Wang, Zhiguang Cao, Federico Berto, Chuanbo Hua, Haeyeon Kim, Jinkyoo Park, and Guojie Song. 2024. Reevo: Large language models as hyper-heuristics with reflective evolution. _arXiv preprint arXiv:2402.01145_ (2024). 

   - [36] Haoran Yin, Anna V Kononova, Thomas Bäck, and Niki van Stein. 2024. Controlling the Mutation in Large Language Models for the Efficient Evolution of Algorithms. _arXiv preprint arXiv:2412.03250_ (2024). 

   - [37] Yan Zhan, Chang Li, Zhigang Che, Ho Cheung Shum, Xiaotian Hu, and Huizeng Li. 2023. Light management using photonic structures towards high-index perovskite optoelectronics: fundamentals, designing, and applications. _Energy & Environmental Science_ (2023). 

   - [38] Stefan Zollner. 2013. Spectroscopic ellipsometry for inline process control in the semiconductor industry. In _Ellipsometry at the Nanoscale_ . Springer, 607–627. 

- [15] Yajie Jiang, Mark J Keevers, and Martin A Green. 2018. Design of Bragg Reflector in GaInP/GaInAs/Ge Triple-Junction Solar Cells for Spectrum Splitting Applications. In _2018 IEEE 7th World Conference on Photovoltaic Energy Conversion (WCPEC)(A Joint Conference of 45th IEEE PVSC, 28th PVSEC & 34th EU PVSEC)_ . IEEE, 0901–0904. 

- [16] Jungtaek Kim, Mingxuan Li, Oliver Hinder, and Paul Leu. 2024. Datasets and benchmarks for nanophotonic structure and parametric design simulations. _Advances in Neural Information Processing Systems_ 36 (2024). 

- [17] Denis Langevin, Pauline Bennet, Abdourahman Khaireh-Walieh, Peter Wiecha, Olivier Teytaud, and Antoine Moreau. 2024. PyMoosh: a comprehensive numerical toolkit for computing the optical properties of multilayered structures. _JOSA B_ 41, 2 (2024), A67–A78. 

- [18] Fei Liu, Xialiang Tong, Mingxuan Yuan, and Qingfu Zhang. 2023. Algorithm evolution using large language model. _arXiv preprint arXiv:2311.15249_ (2023). 

- [19] Fei Liu, Tong Xialiang, Mingxuan Yuan, Xi Lin, Fu Luo, Zhenkun Wang, Zhichao Lu, and Qingfu Zhang. 2024. Evolution of Heuristics: Towards Efficient Automatic Algorithm Design Using Large Language Model. In _Forty-first International Conference on Machine Learning_ . 

- [20] Fei Liu, Yiming Yao, Ping Guo, Zhiyuan Yang, Zhe Zhao, Xi Lin, Xialiang Tong, Mingxuan Yuan, Zhichao Lu, Zhenkun Wang, et al. 2024. A systematic survey on large language models for algorithm design. _arXiv preprint arXiv:2410.14716_ (2024). 

- [21] Qian Liu, Eric Sandgren, Miles Barnhart, Rui Zhu, and Guoliang Huang. 2015. Photonic nanostructures design and optimization for solar cell application. In _Photonics_ , Vol. 2. MDPI, 893–905. 

- [22] Dang Hoang Long, In-Kag Hwang, and Sang-Wan Ryu. 2009. Design optimization of photonic crystal structure for improved light extraction of GaN LED. _IEEE Journal of Selected Topics in Quantum Electronics_ 15, 4 (2009), 1257–1263. 

- [23] Maurine Malak. 2014. Beyond interferometers based on silicon-air bragg reflectors: Toward on-chip optical microinstruments—A review. _IEEE Journal of Selected Topics in Quantum Electronics_ 21, 4 (2014), 49–60. 

- [24] AP Mihai, M Adabi, W Liu, H Hill, N Klein, and PK Petrov. 2015. Metallic multilayers for X-band Bragg reflector applications. _arXiv preprint arXiv:1506.07702_ (2015). 

- [25] Nasimul Noman and Hitoshi Iba. 2008. Accelerating differential evolution using an adaptive local search. _IEEE Transactions on evolutionary Computation_ 12, 1 (2008), 107–125. 

- [26] Pratyasha Priyadarshini, Arnab Goswami, and Bijoy Krishna Das. 2024. Distributed Bragg reflector–based resonance filters for silicon photonics: design and demonstration. _Journal of Optical Microsystems_ 4, 4 (2024), 041403–041403. 

- [27] Shahryar Rahnamayan, Hamid R Tizhoosh, and Magdy MA Salama. 2007. Quasioppositional differential evolution. In _2007 IEEE congress on evolutionary computation_ . IEEE, 2229–2236. 

- [28] Ingo Rechenberg. 1978. Evolutionsstrategien. In _Simulationsmethoden in der Medizin und Biologie: Workshop, Hannover, 29. Sept.–1. Okt. 1977_ . Springer, 83– 114. 

- [29] Bernardino Romera-Paredes, Mohammadamin Barekatain, Alexander Novikov, Matej Balog, M Pawan Kumar, Emilien Dupont, Francisco JR Ruiz, Jordan S Ellenberg, Pengming Wang, Omar Fawzi, Pushmeet Kohli, and Alhussein Fawzi. 

Conference acronym ’XX, June 03–05, 2018, Woodstock, NY 

Yin et al. 

## **A Problem descriptions and algorithmic insights** 

### **Problem description** 

- **The Bragg mirror optimization** aims to maximize reflectivity at a wavelength of 600 nm using a multilayer structure with alternating refractive indices (1.4 and 1.8). The structure’s thicknesses are varied to find the configuration with the highest reflectivity. The problem involves two cases: one with 10 layers (minibragg) and another with 20 layers (bragg), with the latter representing a more complex inverse design problem. The known optimal solution is a periodic Bragg mirror, which achieves the best reflectivity by leveraging constructive interference. This case exemplifies challenges such as multiple local minima in the optimization landscape. 

- **The ellipsometry problem** involves retrieving the material and thickness of a reference layer by matching its reflectance properties using a known spectral response. The optimization minimizes the difference between the calculated and measured ellipsometric parameters for wavelengths between 400 and 800 nm and a fixed incidence angle of 40°. The parameters to be optimized include the thickness (30 to 250 nm) and refractive index (1.1 to 3) of the test layer. This relatively straightforward problem models a practical scenario where photonics researchers fine-tune a small number of parameters to achieve a desired spectral fit. 

- **The photovoltaics problem** optimizes the design of an antireflective multilayer coating to maximize the absorption in the active silicon layer of a solar cell. The goal is to achieve maximum short-circuit current in the 375 to 750 nm wavelength range. The structure consists of alternating materials with permittivities of 2 and 3, built upon a 30,000 nm thick silicon substrate. Three subcases with increasing complexity are explored, involving 10 layers (photovoltaics), 20 layers (bigphotovoltaics), and 32 layers (hugephotovoltaics). The optimization challenges include balancing high absorption with a low reflectance while addressing the inherent noise and irregularities in the solar spectrum. 

- can improve exploration by evenly sampling the search space. 3. Algorithms should preserve modular characteristics in solutions, as multilayer designs often benefit from distinct functional blocks. 4. Combine global methods with local optimization (e.g., BFGS) to finetune solutions near promising regions. 5. Encourage periodicity in solutions via tailored cost functions or constraints. 

- **Ellipsometry** : This problem has small parameter space with fewer variables (thickness and refractive index), and the cost function is smooth and relatively free of noise, making it amenable to local optimization methods. Here are suggestions for designing algorithms: 1. Use local optimization algorithms like BFGS or NelderMead, as they perform well in low-dimensional, smooth landscapes. 2. Uniform sampling across the parameter space ensures sufficient coverage for initial guesses. 3. Utilize fast convergence algorithms that can quickly exploit the smooth cost function landscape. 4. Iteratively adjust bounds and constraints to improve parameter estimates once initial solutions are obtained. 

- **Photovoltaics** : This problem is a challenging highdimensional optimization problem with noisy cost functions due to the realistic solar spectrum, and it requires maximizing absorption while addressing trade-offs between reflectance and interference effects. Here are the suggestions for designing algorithms: 1. Combine global methods (e.g., DE, CMA-ES) for exploration with local optimization for refinement. 2. Use consistent benchmarking and convergence analysis to allocate computational resources effectively. 3. Encourage algorithms to detect and preserve modular structures (e.g., layers with specific roles like anti-reflective or coupling layers). 4. Gradually increase the number of layers during optimization to balance problem complexity and computational cost. 5. Integrate robustness metrics into the cost function to ensure the optimized design tolerates small perturbations in layer parameters. 

### **Algorithmic insight** 

- **Bragg mirror** : For this problem, the optimization landscape contains multiple local minima due to the wave nature of the problem. And periodic solutions are known to provide near-optimal results, suggesting the importance of leveraging constructive interference principles. Here are some suggestions for designing algorithms: 1. Use global optimization algorithms like Differential Evolution (DE) or Genetic Algorithms (GA) to explore the parameter space broadly. 2. Symmetric initialization strategies (e.g., Quasi-Oppositional DE) 

