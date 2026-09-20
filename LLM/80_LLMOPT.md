# Autonomous Multi-Objective Optimization Using Large Language Model

**Authors:** Yuxiao Huang, Shenghao Wu, Wenjie Zhang, Jibin Wu, Liang Feng, and Kay Chen Tan  

**Source:** arXiv:2406.08987v2 [cs.NE], 26 Jul 2024  

**Note:** Markdown converted from the uploaded PDF. Text, equations, tables, and references are preserved as faithfully as possible; complex PDF layout may not map perfectly to Markdown.

---


<!-- Page 1 -->

Autonomous Multi-Objective Optimization Using Large Language Model Yuxiao Huang, Shenghao Wu, Wenjie Zhang, Jibin Wu, Liang Feng, and Kay Chen Tan,

Abstract—Multi-objective optimization problems (MOPs) are

ubiquitous in real-world applications, presenting a complex challenge of balancing multiple conflicting objectives. Traditional evolutionary algorithms (EAs), though effective, often rely on domain-specific expertise and iterative fine-tuning, hindering adaptability to unseen MOPs. In recent years, the advent of Large Language Models (LLMs) has revolutionized software engineering by enabling the autonomous generation and refinement of programs. Leveraging this breakthrough, we propose a new LLM-based framework that autonomously designs EA operators for solving MOPs. The proposed framework includes a robust testing module to refine the generated EA operator through error-driven dialogue with LLMs, a dynamic selection strategy along with informative prompting-based crossover and mutation to fit textual optimization pipeline. Our approach facilitates the design of EA operators without the extensive demands for expert intervention, thereby speeding up the innovation of EA operators. Empirical studies across various MOP categories validate the robustness and superior performance of our proposed framework.

Index Terms—Multi-objective Optimization, Automatic Algo-

rithm Design, Large Language Model


## I. INTRODUCTION

MULTI-OBJECTIVE optimization is a crucial field of research that tackles the challenge of simultaneously optimizing two or more conflicting objectives in real-world scenarios [1]. The primary goal of multi-objective optimization is to find a set of solutions, often known as the Pareto Optimal Set [2], where no other solutions outperform all objectives. To solve the multi-objective optimization problems (MOPs), a lot of well-known evolutionary algorithms (EAs) have been developed in the literature, including non-dominated-sortingbased methods [3]–[5] and decomposition-based techniques

[6]–[8]. With the growing demand of multi-objective opti-

mization in real-world applications [9], extensive efforts have been conducted to improve the search performance of EAs

[10]–[12], with the goal of tackling the new multi-objective

optimization challenges encountered. However, such handcrafting pipeline for algorithm design necessitates a substantial Corresponding author: Liang Feng Yuxiao Huang, Shenghao Wu are with the Department of Computing, The Hong Kong Polytechnic University, Hong Kong SAR. E-mail: {yuxiao.huang, shenghao.wu}@polyu.edu.hk. Wenjie Zhang is with Department of Electrical and Elctronics Engineering, The Hong Kong Polytechnic University, Hong Kong SAR. E-mail: wenjie zhang@u.nus.edu Jibin Wu and Kay Chen Tan are with the Department of Data Science and Artificial Intelligence, The Hong Kong Polytechnic University, Hong Kong SAR. E-mail: {jibin.wu, kctan}@polyu.edu.hk. Liang Feng is with College of Computer Science, Chongqing University, Chongqing 400044, China. E-mail: {liangf}@cqu.edu.cn. amount of expert knowledge and numerous trials, which could constrain the innovation of EA in solving complex optimization problems. Nowadays, owing to the impressive language processing capabilities, Large Language Models (LLMs) have made significant strides in software engineering tasks. Modern society increasingly leverages these powerful LLMs to address the demands of daily programming tasks [13]–[15]. Particularly, Chen et al. enabled LLMs to refine their programs autonomously [16], while Shypula et al. proposed to enhance the efficiency of programs via few-shot prompting and chain-ofthought [17]. Furthermore, efforts to create powerful programs using LLMs have explored iterative evolution, leading to new mathematical discoveries [18], autonomous programming [19], enhanced vehicle routing [20], [21], hybrid swarm intelligence

[22], and dynamic heuristic adaptation [23]. As these works

demonstrate, LLMs are revolutionizing the field of software engineering through iterative program evolution, marking a new era in algorithmic design for optimization. While the existing methods of program evolution have showcased notable successes across various domains, it is worth noting that, they often adopt succinct prompts and traditional evolutionary strategies. Such design effectively develops pivotal task-specific functions with locked power of LLMs [21]–[23]. However, when employed to construct intricate problem-solving systems for handling complex problems, such as MOPs, these methods often result in catastrophic outcomes—such as program crashes or endless loop—mainly due to inadequate error-handling mechanisms. Furthermore, they may encounter bottlenecks in program design arising from the absence of informative task descriptions and mismatched evolutionary strategies. Although these strategies perform well in numerical optimization tasks, they do not seamlessly align with the prompting-based textual optimization paradigm, which often lead to early stagnation of the search. With the above in mind, to further exploit the power of LLM, we propose a new framework of EA operator design that utilizes LLMs to discover and refine EA operators tailored for diverse MOPs. Recognizing the susceptibility to errors and the prevalence of execution anomalies in sophisticated programs produced by LLMs, our framework incorporates a robust testing module, which is seamlessly integrated into the evolutionary progress. This module treats compilation and runtime errors as indicators, and then guides the refinement of designed operator through dialogues with LLMs using the collected errors. To safeguard against the risk of infinite execution loops—a known hazard in LLM-generated code—


<!-- Page 2 -->

we launch this module as an independent process, governed by a strict execution time limit. Furthermore, we introduce a dynamic selection module, along with informative crossover and mutation that align with the prompting-based textual optimization paradigm, aims to enlarge the exploration capabilities of LLMs. Particularly, our proposed framework initiates with a diverse population of EA operators generated through LLMs. Throughout the evolutionary process, our proposed textual crossover and mutation techniques guide the LLM to craft advanced EA operators for various MOPs. These EA operators generated via LLMs may encompass various search strategies to effectively address MOPs. The contributions of this work can be outlined as follows: • To handle the challenges posed by autonomous multiobjective optimization, a new EA operator evolution framework is devised, which facilitates the autonomous ideation and crafting of cutting-edge EA operators, thereby amplifying the search efficacy for solving MOPs. • In light of the intrinsic vulnerabilities and the frequently occurred errors in programs conceived by LLMs, a robust testing module is established, which can seamlessly refine the generated operator by leveraging the errors as a dialogue-based feedback with LLMs. • To enhance the performance of EA operator evolution, we introduce a dynamic selection strategy, along with informative crossover and mutation specifically tailored to the LLM-based textual optimization paradigm. • To validate the performance of our proposed framework, we have conducted extensive empirical studies, employing both continuous and combinatorial MOPs, against state-of-the-art human-engineered multi-objective optimization algorithms. The obtained results demonstrate the efficacy of EA operators generated via the proposed framework. The remainder of this paper is structured as follows. Section II first provides a literature review of existing works on LLM-assisted program evolution for solving diverse problems, followed by the introduction of three distinct MOPs that serves as our case studies. Our proposed operator evolution framework by using LLM is presented in Section III. Furthermore, to assess the performance of the proposed framework, comprehensive empirical studies are conducted in Section IV. Lastly, Section V summarizes this work and discusses the directions to be explored in the future.


## II. BACKGROUND

This section begins with a literature review of the LLMassisted program evolution methods. Subsequently, the mathematical definitions of continuous MOPs and combinatorial MOPs are given, which serve as the focal points of investigation in our study. Notably, the rationale behind the selection of these MOPs is to investigate the capability of LLM in devising innovative EA operators across varied gene encoding modes.


### A. Review of LLM-assisted Program Evolution

The emergence of LLMs have marked a transformative phase in optimization [14], [24], [25]. Within the context of textual optimization, such as program evolution, LLMs empower the generation of code that addresses a wide range of programming requirements [13]. Early study of Lehman et al. explored the potential of LLM trained to generate code in the context of genetic programming, which reveals that LLMs can significantly enhance the effectiveness of the programs [26]. Subsequently, Romera-Paredes et al. utilized LLMs to make new mathematical discoveries via search novel programs iteratively, indicating the potential software engineering capability by the integration of LLMs and evolutionary computation [18]. Liventsev et al. showcased the performance of fully autonomous programming using LLMs, suggesting a future where programs evolve without human guidance [19]. Liu et al. proposed a LLM-based algorithm evolution framework to design novel programs for solving traveling salesman problems (TSPs) [20]. Furthermore, they extended their work to develop superior guided local search for combinatorial optimization [21]. Pluhacek et al. leveraged LLMs in metaheuristic optimization to generate hybrid swarm intelligence, potentially outperforming traditional methods [22]. Ye et al. introduced LLMs as hyper-heuristics within a reflective evolution framework, allowing for dynamic adaptation [23]. These advancements underscore the transformative role of LLMs in the algorithmic design for optimization tasks. Despite the promising advancements, the exploration of LLM-assisted program evolution in optimization remains embryonic. To date, no effort has been made to develop innovative EA operators using LLMs for MOPs. Our proposed methodology aims to bridge this gap, overcoming the intrinsic constraints of LLMs and crafting EA operators that deliver superior search performance across different MOPs.


### B. Continuous Multi-objective Optimization Problems

Continuous Multi-objective Optimization Problems (CMOPs) constitute a pivotal category of optimization problems. These problems, characterized by continuous real numbers as decision variables, entail the optimization of multiple conflicting objectives. Considering a minimization CMOP, the mathematical definition can be given by:

Minimize

f(x) = [f1 (x), f2 (x), . . . , fk (x)]

Subject to

x ∈ X (1) where k represents the number of objectives, x denotes the decision variables and X specifies the feasible search space. Generally, the goal of CMOP is to find a set of Paretooptimal solutions, P = {x1, x2, . . .}, x ∈ X, which cannot be improved in any objective without degrading another. The research value of CMOPs lies in their applicability to realworld scenarios, such as engineering design [27], finance [28], and environmental management [29].


### C. Combinatorial Multi-objective Optimization Problems

In contrast to the continuous MOPs which involve realvalued decision variables, combinatorial MOPs focus on discrete decision variables, which present challenges due to their


<!-- Page 3 -->

discontinuity and lack of smoothness. In what follows, we introduce two distinct combinatorial MOPs, each characterized by unique gene encoding.


#### 1) Multi-objective Knapsack Problems: MOKPs are combi-

natorial optimization problems that involve selecting a subset of items from a given set, subject to a capacity constraint [30]. Each item has multiple associated objectives (e.g., different types of profits). The goal is to find a Pareto-optimal set of items that maximizes the profits while respecting the capacity constraint. The mathematical definition of MOKPs can be expressed as follows. Given n items with associated weights wi, k types of profits pi j (i = 1, 2, · · · , k), and a knapsack capacity C, the goal is to find a binary vector x = [x1, x2, . . .] to maximize the profits given by:

Maximize

f(x) = [f1 (x), f2 (x), . . . , fk (x)]

Where

fi (x) = n

X

j=1 pi j · xj

Subject to

n

X

j=1 wj · xj ≤ C, xj ∈ {0, 1}, j = 1, 2, ..., n (2) MOKPs find applications in many real-world optimization problems, such as food order optimization [31], engineering and operational research [32], cargo loading and project selection [33]. The versatility of MOKPs in addressing these diverse challenges underscores their significance in strategic planning and optimization across various industries.


#### 2) Multi-objective Traveling Salesman Problems: MOTSPs

extend the traditional Traveling Salesman Problem (TSP) by incorporating several minimization objectives [34]. In a MOTSP, a salesman is tasked with visiting each city in a set exactly once, while optimizing not just for the total travel distance, but also for additional objectives such as time, cost, or environmental impact. Mathematically, consider a set of n cities and distinct k types of pairwise distances di (u, v), where the u and the v specifies two different vertexes. The goal is to find a permutation π of the n cities that minimizes the k traveling distances simultaneously, which can be given by:

Minimize

f(π) = [f1 (π), f2 (π), . . . , fk (π)]

Where

fi (π) = n−1

X

i=1 di (π(i), π(i + 1))

Subject to

π ∈ permutations(1, 2, . . . , n) (3) Multi-objective Traveling Salesman Problems (MOTSPs) have practical implications in logistics, transportation, and network design. Particularly, MOTSPs streamline complex decisionmaking processes in areas such as efficient routing for delivery services [35], sustainable urban development [36], and resource management in healthcare systems [37]. The adaptability of MOTSPs to cater to multiple objectives simultaneously is what makes them invaluable in the pursuit of operational excellence and sustainability across diverse sectors.


## III. PROPOSED METHOD

In this section, the proposed method for evolving EA operators via LLM is introduced. The workflow of our proposed paradigm has been depicted in Fig. 1. In contrast to existing program evolution pipelines [18], [20], [26], our proposed method integrates an LLM-assisted debugging process, encompassing Pilot Run & Repair, into the core operator generation stages: “Operator Initialization”, “Operator Crossover”, and “Operator Mutation”. Additionally, the “Dynamic Operator Selection” is tailored to complement the LLM-based crossover mechanism, facilitating the handling of textual data. As illustrated in Fig. 1 and outlined in Alg. 1, the paradigm begins with the phase of “Operator Initialization”, where an initial population of EA operators is generated from a meticulously crafted ‘Initial Prompts’ (line 1 of Alg. 1). These operators undergo “Parallel Operator Evaluation”, receiving scores based on their efficacy across MOPs. These scores inform the “Dynamic Operator Selection” (lines 4-5), bringing diversity in “Crossover Prompts” by altering the number of selected parent operators, thus fostering the creation of innovative operators during “Operator Crossover” (line 6) and “Operator Mutation” (line 7). The newly generated operator obtained


### Algorithm 1: Pseudocode of the operator evolution.

Input:

Gev: Number of generations to evolve operators. Nev: Number of operators in each population. PBs: Multi-objective problems.

Output:

Pev: The best evolutionary operators. 1 Obtain the initial operator population Pev and the scores on PBs via ‘Operator Initialization’ (Alg. 2). 2 for gen ← 1 to Gev do 3 for i ← 1 to Nev do 4 Obtain selection probabilities of operators in Pev based on their scores. 5 Generate a random integer Ns, 1 < Ns ≤ Nmax 6 Obtain a new operator RC leveraging LLM and Ns selected operators through ‘Operator Crossover’ (Alg. 3). 7 Obtain a new operator ˆ RC leveraging LLM and the generated operator RC through ‘Operator Mutation’ (Alg. 4). 8 Obtain score of ˆ RC via parallel evaluation on PBs. 9 Pev = Pev ∪ { ˆ

RC}.

10 end 11 Update Pev based on scores. 12 end


<!-- Page 4 -->

Initial Prompts Parallel Operator Evaluation Dynamic Operator Selection via Scores End? Best Operator

LLM

Pilot Run Operators Repair Prompts Opt. 1 Opt. 2 Opt. Nev ... Pro. 1 Pro. 2 Pro. Np ... Opt. 1 Opt. 1 Opt. Nev ... Pro. 1 Pro. Np Pro. Np ... + + ... ... + Multi-thread Evaluation Score 1 Score 2 Score Nev ... Score 1 Score 2 Score Nev ... Probability 1 Probability Nev ... Preprocessing Opt. 1 Opt. 2 Opt. Nev ... Selection Probability Probability 2 Rand Ns, 1<Ns < Nmax Opt. 1 Opt. 2 Opt. Ns ... Opt. 1 Opt. 2 Opt. Ns ... Crossover Prompts LLM Pilot Run Repair Prompts Opt.

TC

Opt. IC Mutation Prompts LLM Opt. TC Pilot Run Repair Prompts Yes No Parallel Operator Evaluation Operator Initialization

LLM

Operator Crossover

LLM

Operator Mutation

LLM


*Fig. 1: Illustration of the proposed multi-objective algorithm evolution via LLM.*

through mutation (i.e., ˆ RC) is evaluated in parallel to obtain its score, which is then integrated into the population, followed by an elitist strategy-based update of the population (lines 8- 11). The evolution of operators persists, driven by enhanced optimization performance, until the termination criteria are met. The paradigm’s iterative design guarantees ongoing refinement, cycling through operator deployment and assessment until an established endpoint is reached. With this framework, the most effective EA operators—demonstrating consistent superiority in solution generation—is identified. This LLMaided strategy infuses program evolution with human-like deductive processes, bolstering the adaptability and resilience of multi-objective optimization methods. In what follows, the details of each component are introduced.


### A. Operator Initialization

This section introduces the initialization of operators by prompting LLM. It is commonly acknowledged that wellcrafted prompts are pivotal for the effective initialization of operators, which can significantly speed up the evolution of operators. In light of this, we advocate for the utilization of detailed task descriptions and stringent requirements to prompt the LLM, with the aim of engendering superior EA operators. The prompts for initialization are presented in the Fig. 2, titled by “INITIALIZATION”. As depicted, the prompts can be briefly divided into three parts, i.e., ‘System’, ‘Description of Task’ and ‘Requirements’, respectively. The ‘System’ gives the initial prompts for LLM with a brief description for


### Algorithm 2: Pseudocode of the operator initialization.

Input:

Nev: Number of operators in each population. PBs: Multi-objective problems.

Output:

Pev: The initialization population of operators. // Operator Initialization 1 Pev ← {} 2 for i ← 1 to Nev do 3 RC ← None 4 while RC is None do 5 Obtain an operator TC via prompting LLM. 6 Obtain new RC via Alg. 5. 7 end 8 Obtain score of RC via parallel evaluation on PBs. 9 Pev = Pev ∪ {RC} 10 end the task. The ‘Description of Task’ outlines the details of the task for the LLM, while the ‘Requirements’ provides the specific requirements on the task. Within these prompts, the placeholder #PROBLEM# is a user-defined descriptor for MOPs; the #PROBLEM DESC# presents an informative introduction to the MOP with optimization objectives, which aids crafting bespoke search operator for specific MOPs; and the #FORMAT# delineates the operator’s specifics, encompassing the function name, input parameters, output and their


<!-- Page 5 -->

annotations. Details of these placeholders have been given in the Supplementary Materials. Employing these comprehensive prompts enables the LLM to generate EA operators that may achieve higher score across MOPs, as delineated in Alg. 2. To further validate the operator produced by the LLM engine, it will undergo Pilot Run & Repair as discussed in Section III-E, specifically lines 3-7 of Alg. 2. The generation process continues until an operator successfully passes the validation tests or a rectified operator is produced through the repair process outlined in Alg. 5.

INITIALIZATION

System:

You are an expert in designing intelligent evolutionary search strategies that can solve #PROBLEM# efficiently and effectively. #PROBLEM DESC#

Description of Task:

Your task is to evolve a superior evolutionary operator with Python for tackling #PROBLEM#, with the goal of achieving top search performance across #PROBLEM#. You have to provide me the Python code with a single function namely ‘next generation’ following the format and the requirements given below, which are matched with their functionalities:

#FORMAT#

Requirements:

You have to return me a single function namely ‘next generation’, keep the format of input and the format of output unchanged, and provide concise descriptions in the annotation. Please return me an XML text using the following format: <next generation> ... </next generation> where ‘...’ gives only the entire code without any additional information. To enable direct compilation for the code given in ‘...’, please don’t provide any other text except the single Python function namely ‘next generation’ with its annotation. No Explanation Needed!!


*Fig. 2: Prompt design for ‘Operator Initialization’*


### B. Dynamic Operator Selection via Scores

This section introduces the proposed selection strategy tailored for LLM-assisted operator evolution. In traditional evolutionary algorithms [38]–[40], this component is typically responsible for selecting a predetermined number of parents (commonly two) for subsequent operations such as crossover. In contrast, generative pre-trained transformer (GPT) models

[41], [42] may yield similar responses (i.e., programs) when

provided with a detailed and specific prompt—effectively replicating the same operator. This can lead to a stagnation in the operator evolution progress, as the newly generated operator, when underperforming compared to the existing operators within the operator population, may cause the process to become ensnared in local optima. Considering the aforementioned issue, this study introduces a dynamic selection mechanism to facilitate the generation of novel operators during operator crossover. Specifically, as illustrated in lines 4-5 of Alg. 1, the selection probabilities for the individual operators within Pev are determined based on their performance scores on MOPs. A higher score signifies enhanced search capability and, consequently, an increased likelihood of selection. The selection probability for each operator is computed as follows: Ps(i) = exp(scorei) PNev k=1 exp(scorek) (4) where Nev denotes the number of operators within the population. Additionally, a random integer Ns, where 1 < Ns ≤ Nmax, is generated to designate the count of parent operators chosen for the operator crossover.


### C. Operator Crossover

Utilizing the dynamically selected parent operators, this study performs informative operator crossovers by engaging a LLM with these operators. The LLM, serving as an intelligent engine, is anticipated to synthesize innovative operators that surpass the parent operators in terms of scores. The prompts for the LLM are structured as Fig. 3, named by

“CROSSOVER”:

CROSSOVER

Description of Task:

I will showcase several evaluated ‘next generation’ functions in XML format, with their scores obtained on the #PROBLEM#. Your task is to conceive an advanced function with the same input/output formats, termed ‘next generation’, that is inspired by the evaluated cases.

#FORMAT#

Below, you will find the #Ns# evaluated ‘next generation’ functions in XML texts, each accompanied by its corresponding score.

#SELECTED OPERATORS#

Requirements:

Kindly devise an innovative ‘next generation’ method with XML that retains the identical input/output structure. This method should be crafted through a meticulous analysis of the shared characteristics among high-performing algorithms. No Explanation Needed!!


*Fig. 3: Prompt design for ‘Operator Crossover’*

The placeholders #PROBLEM#, #FORMAT#, #Ns#, and #SELECTED OPERATORS# denote the MOP name, the coding format of the operator, the quantity of parent operators selected, and the XML code snippets of the parent operators with their scores, respectively. The dynamic nature of these prompts is likely to facilitate the generation of varied operators


<!-- Page 6 -->


### Algorithm 3: Pseudocode of the operator crossover.

Input:

P̂ev: Selected operators via dynamic operator selection.

Output:

RC: Validated or repaired operator. // Operator Crossover 1 RC ← None 2 while RC is None do 3 Obtain a new operator TC via prompting LLM with P̂ev. 4 Obtain new RC via Alg. 5. 5 end


### Algorithm 4: Pseudocode of the operator mutation.

Input:

IC: Input operator gained via operator crossover.

Output:

Pev: The best evolutionary operators. // Operator Mutation 1 if rand < 1 Nev then 2 RC ← None 3 while RC is None do 4 Obtain a new operator TC via prompting LLM with IC. 5 Obtain new RC via Alg. 5. 6 end 7 end 8 else

9 RC ← IC

10 end by the LLM, as outlined in line 3 of Alg. 3. However, as outlined in line 4 of Alg. 1, the resultant operator TC requires additional validation or refinement to obtain RC, akin to the proposed operator initialization.


### D. Operator Mutation

This section introduces the process of operator mutation, facilitated through the utilization of a LLM. The fundamental goal of this mutation component is to implement strategic modifications to the operators derived from the crossover phase. As illustrated in lines 1-7 of Alg. 4, these alterations occur with a predefined probability, i.e., 1/Nev, where Nev denotes the total number of operators within the population


### P. Given an input operator, i.e., IC, we intend to alter the

code slightly with the prompts given by Fig. 4, where the placeholder #OPERATOR# represents the textual data of IC. Once gained a modified operator by leveraging the LLM, the operator (i.e., TC) will be validated or repaired through Alg. 5 akin to ‘Operator Crossover’ (line 5 of Alg. 4). The mutation mechanism is designed to be adaptive, allowing for the fine-tuning of operators based on the evolving demands of the MOPs at hand. Such component mitigates the risk of premature convergence and maintains a healthy diversity among operators, which is crucial for navigating complex problem landscapes.

MUTATION

Description of Task:

I will introduce an evolutionary search function titled ‘next generation’ in XML format. Your task is to meticulously refine this function and propose a novel one that may obtain superior search performance on #PROBLEM#, ensuring the input/output formats, function name, and core functionality remain unaltered.

#FORMAT#

The original function is given by: <next generation>#OPERATOR#</next generation>

Requirements:

Please return me an innovative ‘next generation’ operator with the same XML format. No Explanation Needed!!


*Fig. 4: Prompt design for ‘Operator Mutation’*


### E. Pilot Run & Repair

Since the operators generated via LLMs may encounter various errors during compilation and execution, which can lead to disastrous outcomes in operator evolution, it is of great significance to design a component that ensures the quality of operator produced by LLMs. With this goal in mind, we introduce a Pilot Run & Repair component in this section, seamlessly integrated into the program’s evolution process. This component treats compilation and runtime errors as indicators and engages in dialogues with LLMs to guide operator quality improvement.

REPAIR

Description of Task:

The code you provided for me cannot pass my demo test on #PROBLEM#. The error is given by: #ERROR#. Can you correct the code according to the errors?

Requirements:

Please return me a refined ‘next generation’ with the same XML format, i.e., <next generation>...</next generation> , where the ‘...’ represents the code snippet. No Explanation Needed!!


*Fig. 5: Prompt design for repairing operators*

Alg. 5 outlines the workflow of the proposed component. It assesses the quality of the tested operator (referred to as TC) on the toy problems (given by PBs) within a specified budgeted running time (MaxT). If necessary, it proceeds to repair the operator by identifying errors and engaging in dialogues with LLMs. The procedure initiates a while loop with a maximum repair time (Ntrail). Within the loop, as observed in lines 3-4, an independent process is launched to execute RC on PBs, adhering to the time budget of MaxT. The


<!-- Page 7 -->


### Algorithm 5: Pseudocode of Pilot Run & Repair.

Input:

Ntrail: Number of trails for code repair. TC: The tested operator. PBs: The testing multi-objective problems. MaxT: The maximum running time.

Output:

RC: Repaired operator. 1 iter ← 0 2 while iter < Ntrail do

3 RC ← TC

4 Start an independent process to run RC on PBs under a limited running time MaxT. 5 Obtain the running state and error occurred during the testing run. 6 if state is True then 7 Return RC 8 end 9 else if state is False and error is not empty then 10 Obtain new TC based on communication with LLM using the informative error collected. 11 end 12 else 13 Return None 14 end 15 iter ← iter + 1 16 end 17 Return None process provides its running state and any encountered errors during execution (line 5). Notably, the error may be empty due to unknown issues (such as an endless loop). Subsequently, if state = True, it signifies that the tested operator successfully passed the pilot run and does not require further repair through LLM dialogues (lines 6-8). Conversely, when state = False and error is not empty, it indicates that errors occurred during testing and can be leveraged for code repair using LLMs (lines 9-11). The code repair prompts are illustrated in Fig. 5, termed as ‘REPAIR’, where #PROBLEM# denotes the name of the test MOPs, and #ERROR# encapsulates the descriptions collected by the error handler. Otherwise, if no specific issues are identified, None is returned to denote default testing failure (lines 12-14). The repair process continues until the specified maximum repair time (Ntrail) is met, ultimately returning None.


### F. Parallel Operator Evaluation

Upon successful completion of the ‘Pilot Run’ by the operators generated through LLM, a parallel evaluation is conducted to measure their efficacy on the MOPs in terms of a normalized score. As depicted in Fig. 1, each operator, denoted as ‘Opt. ∗’, is systematically paired with a validation problem, referred to ‘Pro. ∗’). Following this, the pairs are independently processed in multiple threads, each yielding an operator’s performance score for a specific MOP. It is worth noting that, the normalized score for the i-th operator, aggregated across the MOPs, is calculated as follows: scorei = MEAN(PS) − STD(PS) (5) Here, ‘MEAN’ and ‘STD’ denote the mean and standard deviation of the collected scores, respective. PS specifies the scores obtained on the MOPs. By maximizing the normalized score through LLM-assisted operator evolution, we aim to derive an operator that not only excels consistently across MOPs but also demonstrates robust competitiveness across diverse MOPs.


## IV. EXPERIMENTAL STUDY

In this section, we conduct comprehensive empirical studies to rigorously assess the efficacy of our proposed LLM-assisted operator evolution framework within the domain of multiobjective optimization. This section begins by delineating the experimental settings of validation and testing MOPs, the performance metrics across different MOP categories, and the setup of compared multi-objective algorithms. Subsequently, the results obtained on COMPs, MOKPs and MOTSPs are presented and discussed to validate the search performance of the proposed automatic operator evolution paradigm, which is denoted by LLMOPT.


### A. Experimental Settings

We select one continuous MOP and two combinatorial MOPs with very different gene encoding modes to validate the performance of our proposed framework: the CMOP with continuous variables, the MOKP with binary variables, and the MOTSP with permutation-based variables. Each MOP category is further subdivided into two distinct sets: a validation group and a testing group. The validation group consists of smaller-scale problem instances that are utilized during the evolutionary progression of operators in LLMOPT. On the other hand, the testing group comprises larger-scale problem instances that serve to assess the performance of the best operator optimized through our proposed LLMOPT. For the CMOPs, we select ‘ZDT1’ to ‘ZDT6’ (two objectives) and ‘DTLZ1’ to ‘DTLZ7’ (three objectives) [43] with default configurations (with decision variables ranging from 10 to 30) in [44] as the validation group, while their counterparts with 50 decision variables serve as the testing group. The performance score for each CMOP instance, denoted by PSi, is calculated via PSi = 1 − IGDi, where IGDi denotes the Inverted Generational Distance (IGD) value [45] obtained for the i-th problem instance. A lower IGD value signifies a higher score and indicates a more effective search performance by the operator. In the case of the MOKP, we have randomly generated 10 problem instances with item counts ranging from 50 to 200 for the validation group, and 10 problem instances with item counts ranging from 100 to 200 for the testing group. The score for each MOKP instance is given by: PSi = 1 − HVi, where HVi denotes the Hypervolume (normalized between 0 and 1) [46] achieved on the i-th problem instance. Since the MOKP is a maximization problem, a lower Hypervolume implies a higher score and more favorable


<!-- Page 8 -->


### TABLE I: Configurations of MOEAD, CTAEA, RVEA, NSGA2, AGEMOEA and SMSEMOA for solving different categories

of MOPs. Decomposition-based Non-dominated Sorting-based

MOEAD CTAEA RVEA NSGA2 AGEMOEA SMSEMOA

Population Size 100 100 100 100 100 100 Generation 200 200 200 200 200 200 Crossover

CMOP SBX SBX SBX SBX SBX SBX

MOKP — TwoPointCrossover TwoPointCrossover TwoPointCrossover TwoPointCrossover TwoPointCrossover MOTSP OrderCrossover OrderCrossover OrderCrossover OrderCrossover OrderCrossover OrderCrossover Mutation

CMOP PM PM PM PM PM PM

MOKP — BitflipMutation BitflipMutation BitflipMutation BitflipMutation BitflipMutation MOTSP InversionMutation InversionMutation InversionMutation InversionMutation InversionMutation InversionMutation Repair MOKP RandWeightRepair RandWeightRepair RandWeightRepair RandWeightRepair RandWeightRepair RandWeightRepair 2 4 6 8 10 Generation −3 −2 −1 0 Scores on CMOPs

LLMOPT

MOEAD

CTAEA

RVEA

NSGA2

AGEMOEA

SMSEMOA

(a) Validation CMOPs (b) Validation MOKPs 2 4 6 8 10 Generation 0.72 0.74 0.76 0.78 0.80 0.82 Scores on MOTSPs

LLMOPT

MOEAD

CTAEA

RVEA

NSGA2

AGEMOEA

SMSEMOA

(c) Validation MOTSPs


*Fig. 6: The convergence curves of the proposed operator evolution framework on different types of MOPs.*

outcomes. Furthermore, for the MOTSP, we have generated 20 problem instances with 30 vertices for the validation group, and 10 problem instances with vertices ranging from 100 to 200 for the testing group. The score for each MOTSP instance is determined by: PSi = HVi. As the MOTSP is a minimization problem, a higher normalized Hypervolume indicates a higher score and a more proficient search capability. To demonstrate the search performance of the EA operator optimized via the proposed LLMOPT, we adopt six multiobjective optimization algorithms with suitable evolutionary operators for handling the three MOP categories based on

[44], namely MOEAD [6], CTAEA [47], RVEA [48], NSGA2

[3], AGEMOEA [49], SMSEMOA [50]. The configurations

of these methods are detailed in Table I, ensuring a fair comparison by maintaining the same population size and the maximum number of generations across all algorithms (also configured in the operator obtained through LLMOPT). As can be observed, for CMOPs, we employ the ‘Simulated Binary Crossover (SBX)’ [51] and ‘Polynomial Mutation (PM)’ [52] operators; MOKPs are addressed using ‘Two-Point Crossover’

[53] and ‘Bit-Flip Mutation’ [54]; while MOTSPs are opti-

mized with ‘Order Crossover’ [55] and ‘Inversion Mutation’

[56]. Notably, the MOEAD is not applied to MOKPs due to its

incompatibility with the knapsack capacity constraints. Additionally, for the efficient resolution of MOKPs, the commonly adopted ‘RandWeightRepair’ strategy is employed, wherein items are randomly removed to meet the capacity constraints. Each multi-objective algorithm under comparison, as well as the optimized operator, is subjected to 10 independent runs for every MOP instance to ensure robust statistical analysis. The hyper-parameters specific to the evolution of the operator within our framework are as follows: • Population size for the proposed framework: Nev = 10. • Maximum generations for the proposed framework: Gev = 10. • Maximum number of selected parents: Nmax = Nev/2. • Language model employed: gpt-4-1106-preview. • Temperature setting for the language model: 0.5. • Maximum running time for Pilot Run: MaxT = 2000s. • Number of trials for code repair: Ntrial = 2. The temperature is set at 0.5 to strike an optimal balance between exploitation and exploration within the operator evolution framework. Other configuration of the temperature can also be applied accordingly. The maximum running time MaxT and the number of trials Ntrial = 2 for code repair are configured empirically.


### B. Results and Discussions

In this section, we first evaluate the efficacy of the proposed operator evolution framework, i.e., LLMOPT, on the previously discussed validation MOPs. Figure 6 depicts the convergence trajectories of the proposed LLMOPT across


<!-- Page 9 -->


### TABLE II: Averaged IGD values obtained by MOEAD, CTAEA, RVEA, NSGA2, AGEMOEA, SMSEMOA, and the best

operator optimized via the proposed LLMOPT on testing CMOP instances over 10 independent runs. Superior averaged results on each instance are highlighted in bold font. Problem LLMOPT MOEAD CTAEA RVEA NSGA2 AGEMOEA SMSEMOA zdt1 1.133e-02 2.575e-02 2.313e-02 7.249e-02 9.998e-03 1.098e-02 6.569e-03 zdt2 3.996e-02 1.979e-01 6.199e-02 1.079e-01 1.320e-02 2.779e-02 5.899e-02 zdt3 1.947e-02 3.069e-02 3.211e-02 1.120e-01 8.365e-03 7.526e-03 6.567e-03 zdt4 3.180e+01 1.093e+01 3.199e+01 5.346e+01 3.673e+01 3.140e+01 3.521e+01 zdt5 1.587e-01 2.055e-01 1.836e-01 1.749e-01 1.266e-01 1.424e-01 1.462e-01 zdt6 1.984e-02 3.116e-01 2.445e+00 1.870e+00 1.321e+00 1.052e+00 1.487e+00 dtlz1 6.519e+01 1.011e+02 1.179e+02 8.428e+01 2.503e+02 1.861e+02 1.676e+02 dtlz2 7.758e-02 7.506e-02 6.032e-02 5.857e-02 8.110e-02 6.666e-02 6.662e-02 dtlz3 2.054e+02 3.129e+02 4.434e+02 3.113e+02 5.438e+02 4.360e+02 5.571e+02 dtlz4 3.982e-01 6.064e-01 5.819e-02 6.359e-02 8.066e-02 4.409e-01 2.536e-01 dtlz5 1.564e-02 3.028e-02 1.065e-01 1.264e-01 1.111e-02 1.443e-02 6.789e-03 dtlz6 2.318e-01 3.055e+01 2.506e+01 2.327e+01 2.658e+01 2.801e+01 1.850e+01 dtlz7 1.169e-01 2.041e-01 1.440e-01 3.143e-01 1.238e-01 1.272e-01 9.400e-02 Averaged IGD 2.335e+01 3.516e+01 4.780e+01 3.655e+01 6.609e+01 5.257e+01 6.004e+01 these MOPs. The X-axis represents the evolutionary progress of the operators, while the Y-axis indicates the scores achieved by the best-performing operator in the current population. As shown in Fig. 6 (a), the performance of EA operator generated at the early stage is relatively low compared to other multiobjective algorithms due to the black-box nature of CMOPs, which provide limited problem information. Despite initial trials, the generated operators for CMOPs were unsatisfactory. However, the proposed LLMOPT allows the LLM to iteratively refine EA operators through feedback, showcasing the advantage of our approach over one-off code generation techniques. At last, the optimized EA operator obtained the best performance in terms of the scores on validation CMOPs. Sub-figure (b) reveals that the EA operator generated through LLMOPT outperforms competing algorithms from the start in the MOKP domain, which leverages on the rich problemspecific properties within the informative prompts. Notably, the optimization capabilities of these EA operators continue to improve as the evolution progresses. Similarly, sub-figure (c) shows that LLMOPT starts with a high initial score against CTAEA, RVEA, NSGA2, AGEMOEA and SMSEMOA. By iteratively improving the performance via the proposed LL- MOPT, the optimized EA operator ultimately achieved competitive performance against MOEAD, which obtained the best performance on validation MOTSPs. Despite this, MOEAD shows weaker results in CMOPs, underscoring the competitive edge of operators optimized via our proposed method across diverse MOP categories. To delve deeper into the search capabilities of the best operator optimized via the proposed LLMOPT, we present a detailed analysis of the results obtained on the testing CMOPs, MOKPs and MOTSPs.


#### 1) Evaluation on CMOPs: Table II presents the averaged

IGD values achieved by MOEAD, CTAEA, RVEA, NSGA- II, AGEMOEA, SMSEMOA, and the best operator evolved by LLMOPT across testing CMOP instances, based on 10 independent runs. The ‘Average IGD’ row reflects the mean IGD value across all evaluated problems. It is evident that the best EA operator generated by LLMOPT secures competitive standings when juxtaposed with existing hand-crafted multiobjective optimization methods. Notably, it excels in more challenging scenarios (from dtlz1 to dtlz7), outperforming all compared methods in three instances. This success can be attributed to the scoring mechanism defined in Eq. 5, which compels the LLM-assisted search engine to harmonize search efficacy across all problems, thereby significantly diminishing large IGD values in complex problems like ‘DTLZ-1’ and ‘DTLZ-3’. This feedback loop culminates in the lowest average IGD for the testing CMOPs. Additionally, Fig.7 illustrates the convergence curves for each algorithm on representative CMOP cases. The operator optimized by LLMOPT demonstrates rapid convergence—or at least competitive convergence rates—in most instances, such as ‘ZDT-6’, ‘DTLZ1’, ‘DTLZ- 3’, and ‘DTLZ-6’. The marked reduction in IGD value for ‘DTLZ-6’ further underscores the performance of the operator obtained by LLMOPT in contrast to other methods.


#### 2) Evaluation on MOKPs: In assessing the search per-

formance on MOKPs, Table III enumerates the average HV values achieved by CTAEA, RVEA, NSGA-II, AGEMOEA, SMSEMOA, and the optimal operator developed through the proposed LLMOPT. This evaluation encompasses 10 testing MOKP instances, each subjected to 10 independent runs. As can be observed, the ‘Average HV’ row aggregates the HV metrics, providing a summarized view of the algorithms’ overall performance across all testing instances. Examination of Table III reveals that the EA operator gained by LLMOPT consistently outperforms the competing methods across all testing cases. This underscores the LLM’s capacity to construct a potent evolutionary operator when provided with clearly defined problem attributes in the prompts. A closer look at


<!-- Page 10 -->

0 25 50 75 100 125 150 175 200 Generation 0 1 2 3 4 5 6 7

IGD

zdt6

LLMOPT

MOEAD

CTAEA

RVEA

NSGA2

AGEMOEA

SMSEMOA

(a) ZDT-6 0 25 50 75 100 125 150 175 200 Generation 200 400 600 800 1000 1200

IGD

dtlz1

LLMOPT

MOEAD

CTAEA

RVEA

NSGA2

AGEMOEA

SMSEMOA

(b) DTLZ-1 0 25 50 75 100 125 150 175 200 Generation 500 1000 1500 2000 2500 3000 3500 4000

IGD

dtlz3

LLMOPT

MOEAD

CTAEA

RVEA

NSGA2

AGEMOEA

SMSEMOA

(c) DTLZ-3 0 25 50 75 100 125 150 175 200 Generation 0 20 30 40

IGD

dtlz6

LLMOPT

MOEAD

CTAEA

RVEA

NSGA2

AGEMOEA

SMSEMOA

(d) DTLZ-6


*Fig. 7: Convergence curves obtained by MOEAD, CTAEA, RVEA, NSGA2, AGEMOEA, SMSEMOA, and the best EA operator*

generated by the proposed LLMOPT on the representative CMOPs.


### TABLE III: Averaged HV values obtained by CTAEA, RVEA, NSGA2, AGEMOEA, SMSEMOA, and the best operator

generated by the proposed LLMOPT on 10 MOKPs over 10 independent runs. Superior averaged results (Lower HV values) on each instance are highlighted in bold font. Problem LLMOPT CTAEA RVEA NSGA2 AGEMOEA SMSEMOA MOKP1 9.191e-03 1.771e-02 2.103e-02 1.895e-02 1.599e-02 1.705e-02 MOKP2 5.268e-03 1.054e-02 1.241e-02 9.356e-03 8.762e-03 9.007e-03 MOKP3 4.346e-03 1.215e-02 1.504e-02 1.170e-02 8.730e-03 1.039e-02 MOKP4 8.762e-03 1.807e-02 2.224e-02 1.668e-02 1.462e-02 1.553e-02 MOKP5 9.029e-03 2.167e-02 2.873e-02 1.916e-02 1.832e-02 1.861e-02 MOKP6 6.690e-03 1.450e-02 1.810e-02 1.444e-02 1.286e-02 1.334e-02 MOKP7 1.244e-02 2.265e-02 3.193e-02 2.183e-02 1.927e-02 1.981e-02 MOKP8 3.490e-03 9.116e-03 1.285e-02 8.393e-03 7.468e-03 7.569e-03 MOKP9 8.272e-03 1.523e-02 1.770e-02 1.405e-02 1.331e-02 1.329e-02 MOKP10 4.780e-03 1.296e-02 1.644e-02 1.165e-02 1.114e-02 1.078e-02 Averaged HV 7.227e-03 1.546e-02 1.965e-02 1.462e-02 1.305e-02 1.354e-02 0 25 50 75 100 125 150 175 200 Generation 0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7

HV

MOKP3

LLMOPT

CTAEA

RVEA

NSGA2

AGEMOEA

SMSEMOA

(a) MOKP-3 0 25 50 75 100 125 150 175 200 Generation 0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7

HV

MOKP5

LLMOPT

CTAEA

RVEA

NSGA2

AGEMOEA

SMSEMOA

(b) MOKP-5 0 25 50 75 100 125 150 175 200 Generation 0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8

HV

MOKP6

LLMOPT

CTAEA

RVEA

NSGA2

AGEMOEA

SMSEMOA

(c) MOKP-6 0 25 50 75 100 125 150 175 200 Generation 0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7

HV

MOKP8

LLMOPT

CTAEA

RVEA

NSGA2

AGEMOEA

SMSEMOA

(d) MOKP-8


*Fig. 8: Convergence curves obtained by CTAEA, RVEA, NSGA2, AGEMOEA, SMSEMOA, and the best operator generated*

by the proposed LLMOPT on the representative MOKPs. the best operator generated by LLMOPT in the Supplementary Materials reveals an effective repair function crafted by the LLM, which strategically removes the heaviest item from the knapsack, thereby obtaining peak performance on the MOKPs. Complementing the tabulated results, Fig.8 visually charts the convergence paths of the algorithms under comparison. The EA operator evolved by LLMOPT distinguishes itself by attaining the fastest convergence speed across all representative instances. The significant reduction in HV values not only validates the effectiveness of LLMOPT but also its robustness when face diverse multi-objective optimization challenges.


#### 3) Evaluation on MOTSPs: Here we showcase the com-

parative performance analysis of the compared algorithms, including the best operator developed via our proposed LL- MOPT, on the testing MOTSPs. Table IV tabulates the average Hypervolume (HV) values achieved by MOEAD, CTAEA, RVEA, NSGA-II, AGEMOEA, SMSEMOA, and the operator developed via LLMOPT on testing MOTSP instances. The tabulated results demonstrate the efficacy of LLMOPT, particularly in its ability to generate effective EA operators for MOTSP. LLMOPT’s operator outperforms the other algorithms in most instances, achieving the highest averaged HV values in MOTSP3 through MOTSP9. This is indicative of its


<!-- Page 11 -->


### TABLE IV: Averaged HV values obtained by MOEAD, CTAEA, RVEA, NSGA2, AGEMOEA, SMSEMOA, and the best

operator generated by the proposed LLMOPT on 10 MOKPs over 10 independent runs. Superior averaged results (larger HV values) are highlighted in bold font. Problem LLMOPT MOEAD CTAEA RVEA NSGA2 AGEMOEA SMSEMOA MOTSP1 4.784e-01 4.844e-01 3.485e-01 3.583e-01 3.844e-01 3.954e-01 3.750e-01 MOTSP2 5.030e-01 5.050e-01 3.669e-01 3.721e-01 3.983e-01 4.084e-01 3.991e-01 MOTSP3 5.262e-01 5.198e-01 3.824e-01 3.961e-01 4.241e-01 4.322e-01 4.129e-01 MOTSP4 6.082e-01 5.804e-01 4.462e-01 4.479e-01 4.980e-01 5.035e-01 4.847e-01 MOTSP5 5.416e-01 5.303e-01 3.866e-01 4.012e-01 4.358e-01 4.420e-01 4.248e-01 MOTSP6 5.211e-01 5.142e-01 3.736e-01 3.866e-01 4.132e-01 4.234e-01 4.090e-01 MOTSP7 5.346e-01 5.175e-01 3.810e-01 3.846e-01 4.235e-01 4.358e-01 4.120e-01 MOTSP8 5.256e-01 5.177e-01 3.753e-01 3.944e-01 4.174e-01 4.360e-01 4.113e-01 MOTSP9 5.620e-01 5.393e-01 4.022e-01 4.207e-01 4.419e-01 4.502e-01 4.308e-01 MOTSP10 5.160e-01 5.099e-01 3.722e-01 3.759e-01 4.115e-01 4.161e-01 3.956e-01 Averaged HV 5.317e-01 5.218e-01 3.835e-01 3.938e-01 4.248e-01 4.343e-01 4.155e-01 0 25 50 75 100 125 150 175 200 Generation 0.15 0.20 0.25 0.30 0.35 0.40 0.45 0.50

HV

MOTSP1

LLMOPT

MOEAD

CTAEA

RVEA

NSGA2

AGEMOEA

SMSEMOA

(a) MOTSP-1 0 25 50 75 100 125 150 175 200 Generation 0.15 0.20 0.25 0.30 0.35 0.40 0.45 0.50 0.55

HV

MOTSP5

LLMOPT

MOEAD

CTAEA

RVEA

NSGA2

AGEMOEA

SMSEMOA

(b) MOTSP-5 0 25 50 75 100 125 150 175 200 Generation 0.15 0.20 0.25 0.30 0.35 0.40 0.45 0.50

HV

MOTSP6

LLMOPT

MOEAD

CTAEA

RVEA

NSGA2

AGEMOEA

SMSEMOA

(c) MOTSP-6 0 25 50 75 100 125 150 175 200 Generation 0.15 0.20 0.25 0.30 0.35 0.40 0.45 0.50 0.55

HV

MOTSP9

LLMOPT

MOEAD

CTAEA

RVEA

NSGA2

AGEMOEA

SMSEMOA

(d) MOTSP-9


*Fig. 9: Convergence curves obtained by MOEAD, CTAEA, RVEA, NSGA2, AGEMOEA, SMSEMOA, and the best operator*

gained by LLMOPT on the representative MOTSPs. superior capability to navigate the complex search space of MOTSPs effectively. While MOEAD exhibits slightly higher averaged HV values in MOTSP1 and MOTSP2, the operator’s consistent performance across the majority of test cases suggests a more reliable and versatile approach to solving MOTSPs, which is also demonstrated by the bolded ‘Averaged HV’ in the table. Moreover, Fig. 9 illustrates the convergence trajectories for the compared algorithms on representative MOTSP instances. The X-axis represents the evolutionary progress through generations, while the Y-axis shows the average HV values from 10 independent runs. The visual data reveals that LLMOPT’s best operator consistently achieves faster convergence, further demonstrating its capability to effectively solve a range of MOTSPs. This performance is attributed to the proposed LLMOPT, which automatically refine EA operators by leveraging problem-specific knowledge at hand. Delving into the Supplementary Materials for a more detailed examination of the optimal operator devised by LLMOPT, the LLMOPT utilizes a proficient crossover mechanism, specifically the edge recombination crossover (ERX) [57], to adeptly address the intricacies of MOTSPs.


#### 4) Efficiency of Algorithms: To evaluate the search effi-

ciency of the EA operator generated via our proposed method, we focus on the execution time (wall clock time) as a primary metric, which is measured in seconds for a fair comparison across the algorithms MOEAD, CTAEA, RVEA, NSGA2, AGEMOEA, SMSEMOA. The investigation was conducted using testing groups of CMOP, MOKP, and MOTSP.


### TABLE V: Running time (wall clock time measured in

seconds) obtained by MOEAD, CTAEA, RVEA, NSGA2, AGEMOEA, SMSEMOA, and the best operator optimized through LLMOPT on CMOP, MOKP and MOTSP. Smaller running time on each category is highlighted in bold font.

CMOP MOKP MOTSP

LLMOPT 32 21 373

MOEAD 202 — 135

CTAEA 114 79 94

RVEA 37 54 64

NSGA2 23 45 53

AGEMOEA 50 52 60

SMSEMOA 1491 48 56

The empirical evaluation of the search efficiency, as presented in Table V, indicates a significant variance in execution time across the competing algorithms. While the best operator generated via LLMOPT excels in MOKP, achieving the lowest


<!-- Page 12 -->

running time of 21 seconds, it falls behind in MOTSP, with a longer running time of 373 seconds, indicating the worst efficiency among the compared multi-objective algorithms. Despite this, the operator’s efficacy in terms of solution quality for MOTSPs is superior, suggesting that its strategic approach, while time-intensive, results in high-quality solutions. In the domain of CMOPs, the operator’s execution time is commendably efficient at 32 seconds, narrowly trailing behind NSGA2’s 23 seconds. This demonstrates the robustness of the proposed LLMOPT when handling different MOP categories.


### C. Investigation on Different LLMs

In this section, we rigorously validate the performance of our proposed LLMOPT framework using various LLMs. For brevity, we denote them as GPT4, GPT4O, GEMINI, and CLAUDE, respectively. Moreover, the same temperature (0.5) is adopted for each LLM. Fig. 10 has illustrated the convergence curves obtained on CMOP validation dataset using these LLMs. As can be observed, different LLMs exhibit distinct behaviors within the proposed LLMOPT paradigm. Particularly, GPT4 and GPT4O initially struggle to produce a competent EA operator at the start of the search. However, through iterative optimization using LLMOPT, the effectiveness of operators generated by GPT4 and GPT4O improves significantly, highlighting the advantages of LLMOPT over traditional one-off program generation approaches. In contrast, CLAUDE consistently achieves the best EA operator performance from the outset until the end of the search. While GEMINI does yield a qualified EA operator initially, it fails to further enhance operator effectiveness over subsequent iterations. Based on these observations, the CLAUDE may have a superior performance in generating innovative EA operators against other LLMs. 2 4 6 8 10 Generation −3 −2 −1 0 1 Scores on

MOP

Convergence Curve Obtained by LLMs

GPT4

GPT4O

GEMINI

CLAUDE


*Fig. 10: Convergence curves gained by the proposed LLMOPT*

using different LLMs.


### D. Ablation Study

In this section, the ablation studies are conducted to demonstrate the efficacy of the proposed Pilot Run & Repair component and dynamic selection strategy for LLM-based crossover.


### TABLE VI: Quality of operator generated with different LLMs

LLM Tests Success Failed Repaired (%)

GPT4 20 9 + 9 2 81.8%

GPT4O 20 16 + 2 2 50.0%

GEMINI 20 16 + 3 1 75.0%

CLAUDE 20 10 + 7 3 70.0%


#### 1) In-depth Analysis of Code Quality Among LLMs: As

we discussed in the introduction, a common challenge of using LLMs in program design is the occurrence of execution errors in the generated code, which can halt the iterative refinement process. To validate the efficacy of the proposed Pilot Run & Repair component, we tested the code quality generated by GPT4, GPT4O, GEMINI and CLAUDE, using the initialization prompts. Particularly, each LLM was tasked to generate 20 EA operators, which were then assessed for their operational viability. During the testing phase, any errors encountered triggered a repair protocol, which is designed to systematically address and resolve coding errors. The results have been summarized in Table VI, which presents a comparative analysis of the initial operator generation and subsequent repair success rates. As can be observed from, the ‘Tests’ column records the number of attempts made to generate functional EA operators. The “A + B” within the ‘Success’ column represents the total number of successfully generated EA operators, where “A” quantifies the instances without further interaction while “B” counts the successfully repaired instances via the proposed method. Moreover, ‘Failed’ tallies the number of unrepaired operators after one trial, while ‘Repaired’ reflects the proportion of successfully corrected operators through the repair process. The data presented in Table VI clearly demonstrates the superior initial success rates of GPT4O and GEMINI, with an impressive 80% of their generated operators being immediately deployable. Conversely, GPT4 shows a lower initial success but an outstanding repair success rate of 81.8%, underscoring the ‘Pilot Run & Repair’ component’s capability to effectively rectify errors. CLAUDE presents a balanced profile, showcasing a consistent performance in both initial operator generation and subsequent repairability.


#### 2) Investigation on Dynamic Selection Strategy: The se-

lectiopn strategy plays an important role in evolutionary progresses. To validate the performance of the developed dynamic selection strategy, tailored for LLM-based textual optimization tasks, we present the convergence curves of the proposed LLMOPT (denoted by ‘GPT4’) and its counterpart lacking this strategy (denoted by ‘GPT4-no-dc’). As can be observed in Fig. 11, the ‘GPT4’ model, equipped with the dynamic selection strategy, shows a significant improvement in terms of scores gained on CMOPs, indicating an effective adaptation and optimization capability brought by the developed dynamic selection strategy. In contrast, despite a good initialization for the operators, the ‘GPT4-no-dc’ model’s performance remains stagnant, again underscoring the necessity and impact of a dynamic selection strategy in the proposed LLMOPT.


<!-- Page 13 -->


## V. CONCLUSION

In this work, we have embarked on a journey to harness the capabilities of LLMs for the evolution of evolutionary operators, specifically targeting the nuanced domain of multiobjective optimization problems. Our proposed framework, LLMOPT, represents a paradigm shift in EA operator design, moving towards an autonomous methodology that minimizes the need for expert intervention. The ’Pilot Run & Repair’ mechanism embedded within LLMOPT has been instrumental in refining the evolution process of EA operators, enhancing the robustness of the generated operator and setting the stage for fully autonomous programming. The empirical studies showcases the superiority of LLM-evolved operators, demonstrating their advantage over traditional human-crafted approaches. The future of this field is promising, with the potential for LLMs to further revolutionize the optimization landscape. Our results point to an emerging era of self-evolving, self-adapting, and self-improving programs, autonomously driven by the challenges they are engineered to conquer. The application of our framework to a broader spectrum of MOPs, particularly those of greater complexity and scale, stands as a significant next step.

REFERENCES

[1] N. Gunantara, “A review of multi-objective optimization: Methods and

its applications,” Cogent Engineering, vol. 5, no. 1, p. 1502242, 2018.

[2] D. A. Van Veldhuizen, G. B. Lamont et al., “Evolutionary computation

and convergence to a pareto front,” in Late breaking papers at the genetic programming 1998 conference. Citeseer, 1998, pp. 221–228.

[3] K. Deb, A. Pratap, S. Agarwal, and T. Meyarivan, “A fast and elitist

multiobjective genetic algorithm: Nsga-ii,” IEEE transactions on evolutionary computation, vol. 6, no. 2, pp. 182–197, 2002.

[4] Y. Zhou, W. Zhang, J. Kang, X. Zhang, and X. Wang, “A problem-

specific non-dominated sorting genetic algorithm for supervised feature selection,” Information Sciences, vol. 547, pp. 841–859, 2021.

[5] W. Deng, X. Zhang, Y. Zhou, Y. Liu, X. Zhou, H. Chen, and H. Zhao,

“An enhanced fast non-dominated solution sorting genetic algorithm for multi-objective problems,” Information Sciences, vol. 585, pp. 441–453, 2022.

[6] Q. Zhang and H. Li, “Moea/d: A multiobjective evolutionary algorithm

based on decomposition,” IEEE Transactions on evolutionary computation, vol. 11, no. 6, pp. 712–731, 2007. 2 4 6 8 10 Generation −3 −2 −1 0 Scores on

MOP

Convergence Curve Obtained b LLMs

GPT4

GPT4-no-dc


*Fig. 11: Convergence curves gained by the proposed LLMOPT*

(denoted by ‘GPT4’) and its counterpart without dynamic selection strategy (denoted by GPT4-no-dc).

[7] M. Asafuddoula, T. Ray, and R. Sarker, “A decomposition-based evolu-

tionary algorithm for many objective optimization,” IEEE Transactions on Evolutionary Computation, vol. 19, no. 3, pp. 445–460, 2014.

[8] C. Dai, Y. Wang, and M. Ye, “A new multi-objective particle swarm

optimization algorithm based on decomposition,” Information Sciences, vol. 325, pp. 541–557, 2015.

[9] R. Tanabe and H. Ishibuchi, “An easy-to-use real-world multi-objective

optimization problem suite,” Applied Soft Computing, vol. 89, p. 106078, 2020.

[10] Y. Huang, W. Zhou, Y. Wang, M. Li, L. Feng, and K. C. Tan, “Evolu-

tionary multitasking with centralized learning for large-scale combinatorial multi-objective optimization,” IEEE Transactions on Evolutionary Computation, pp. 1–1, 2023.

[11] X. Xue, C. Yang, L. Feng, K. Zhang, L. Song, and K. C. Tan, “Solution

transfer in evolutionary optimization: An empirical study on sequential transfer,” IEEE Transactions on Evolutionary Computation, pp. 1–1, 2023.

[12] Y. Feng, L. Feng, S. Kwong, and K. C. Tan, “A multi-form evolutionary

search paradigm for bi-level multi-objective optimization,” IEEE Transactions on Evolutionary Computation, pp. 1–1, 2023.

[13] L. Belzner, T. Gabor, and M. Wirsing, “Large language model assisted

software engineering: prospects, challenges, and a case study,” in International Conference on Bridging the Gap between AI and Reality. Springer, 2023, pp. 355–374.

[14] X. Wu, S.-h. Wu, J. Wu, L. Feng, and K. C. Tan, “Evolutionary

computation in the era of large language model: Survey and roadmap,” arXiv preprint arXiv:2401.10034, 2024.

[15] V. Alto, Modern Generative AI with ChatGPT and OpenAI Models:

Leverage the capabilities of OpenAI’s LLM for productivity and innovation with GPT3 and GPT4. Packt Publishing Ltd, 2023.

[16] X. Chen, M. Lin, N. Schärli, and D. Zhou, “Teaching large language

models to self-debug,” arXiv preprint arXiv:2304.05128, 2023.

[17] A. Shypula, A. Madaan, Y. Zeng, U. Alon, J. Gardner, M. Hashemi,


### G. Neubig, P. Ranganathan, O. Bastani, and A. Yazdanbakhsh, “Learning

performance-improving code edits,” arXiv preprint arXiv:2302.07867, 2023.

[18] B. Romera-Paredes, M. Barekatain, A. Novikov, M. Balog, M. P. Kumar,


### E. Dupont, F. J. Ruiz, J. S. Ellenberg, P. Wang, O. Fawzi et al.,

“Mathematical discoveries from program search with large language models,” Nature, vol. 625, no. 7995, pp. 468–475, 2024.

[19] V. Liventsev, A. Grishina, A. Härmä, and L. Moonen, “Fully autonomous

programming with large language models,” in Proceedings of the Genetic and Evolutionary Computation Conference, 2023, pp. 1146–1155.

[20] F. Liu, X. Tong, M. Yuan, and Q. Zhang, “Algorithm evolution using

large language model,” arXiv preprint arXiv:2311.15249, 2023.

[21] F. Liu, X. Tong, M. Yuan, X. Lin, F. Luo, Z. Wang, Z. Lu, and


### Q. Zhang, “An example of evolutionary computation+ large language

model beating human: Design of efficient guided local search,” arXiv preprint arXiv:2401.02051, 2024.

[22] M. Pluhacek, A. Kazikova, T. Kadavy, A. Viktorin, and R. Senkerik,

“Leveraging large language models for the generation of novel metaheuristic optimization algorithms,” in Proceedings of the Companion Conference on Genetic and Evolutionary Computation, 2023, pp. 1812– 1820.

[23] H. Ye, J. Wang, Z. Cao, and G. Song, “Reevo: Large language

models as hyper-heuristics with reflective evolution,” arXiv preprint arXiv:2402.01145, 2024.

[24] B. Huang, X. Wu, Y. Zhou, J. Wu, L. Feng, R. Cheng, and K. C.

Tan, “Exploring the true potential: Evaluating the black-box optimization capability of large language models,” arXiv preprint arXiv:2404.06290, 2024.

[25] Y. Huang, W. Zhang, L. Feng, X. Wu, and K. C. Tan, “How multimodal

integration boost the performance of llm for optimization: Case study on capacitated vehicle routing problems,” arXiv preprint arXiv:2403.01757, 2024.

[26] J. Lehman, J. Gordon, S. Jain, K. Ndousse, C. Yeh, and K. O.

Stanley, “Evolution through large models,” in Handbook of Evolutionary Machine Learning. Springer, 2023, pp. 331–366.

[27] M. Janga Reddy and D. Nagesh Kumar, “An efficient multi-objective

optimization algorithm based on swarm intelligence for engineering design,” Engineering Optimization, vol. 39, no. 1, pp. 49–68, 2007.

[28] S. C. Chiam, K. C. Tan, and A. Al Mamum, “Evolutionary multi-

objective portfolio optimization in practical context,” International Journal of Automation and Computing, vol. 5, pp. 67–80, 2008.

[29] Y. Wang, C. Chen, Y. Tao, Z. Wen, B. Chen, and H. Zhang, “A many-

objective optimization of industrial environmental management using


<!-- Page 14 -->

nsga-iii: A case of china’s iron and steel industry,” Applied energy, vol. 242, pp. 46–56, 2019.

[30] C. Bazgan, H. Hugot, and D. Vanderpooten, “Solving efficiently the 0–1

multi-objective knapsack problem,” Computers & Operations Research, vol. 36, no. 1, pp. 260–279, 2009.

[31] A. P. Khandekar and A. Nargundkar, “Dynamic programming approach

to solve real-world application of multi-objective unbounded knapsack problem,” in Intelligent Systems and Applications: Select Proceedings of ICISA 2022. Springer, 2023, pp. 417–422.

[32] Y. Du, Z. Feng, and Y. Shen, “A mixed-factor evolutionary algorithm

for multi-objective knapsack problem,” in International Conference on Intelligent Computing. Springer, 2022, pp. 51–67.

[33] Z. Song, W. Luo, X. Lin, Z. She, and Q. Zhang, “On multiobjective

knapsack problems with multiple decision makers,” in 2022 IEEE Symposium Series on Computational Intelligence (SSCI). IEEE, 2022, pp. 156–163.

[34] W. Peng, Q. Zhang, and H. Li, “Comparison between moea/d and nsga-ii

on the multi-objective travelling salesman problem,” in Multi-objective memetic algorithms. Springer, 2009, pp. 309–324.

[35] I. Khan, M. K. Maiti, and K. Basuli, “Multi-objective traveling salesman

problem: an abc approach,” Applied Intelligence, vol. 50, pp. 3942–3960, 2020.

[36] W. Li, “Solving multi-objective traveling salesman problem,” in The

Traveling Salesman Problem: Optimization with the Attractor-Based Search System. Springer, 2023, pp. 83–95.

[37] Y. Shuai, S. Yunfeng, and Z. Kai, “An effective method for solving

multiple travelling salesman problem based on nsga-ii,” Systems Science & Control Engineering, vol. 7, no. 2, pp. 108–116, 2019.

[38] T. Bäck and H.-P. Schwefel, “An overview of evolutionary algorithms

for parameter optimization,” Evolutionary computation, vol. 1, no. 1, pp. 1–23, 1993.

[39] T. Bartz-Beielstein, J. Branke, J. Mehnen, and O. Mersmann, “Evolu-

tionary algorithms,” Wiley Interdisciplinary Reviews: Data Mining and Knowledge Discovery, vol. 4, no. 3, pp. 178–195, 2014.

[40] Z. He and G. G. Yen, “Many-objective evolutionary algorithms based

on coordinated selection strategy,” IEEE Transactions on Evolutionary Computation, vol. 21, no. 2, pp. 220–233, 2016.

[41] Q. Zhu and J. Luo, “Generative pre-trained transformer for design

concept generation: an exploration,” Proceedings of the design society, vol. 2, pp. 1825–1834, 2022.

[42] R. Luo, L. Sun, Y. Xia, T. Qin, S. Zhang, H. Poon, and T.-Y. Liu,

“Biogpt: generative pre-trained transformer for biomedical text generation and mining,” Briefings in bioinformatics, vol. 23, no. 6, p. bbac409, 2022.

[43] Y. Tian, X. Xiang, X. Zhang, R. Cheng, and Y. Jin, “Sampling reference

points on the pareto fronts of benchmark multi-objective optimization problems,” in 2018 IEEE congress on evolutionary computation (CEC). IEEE, 2018, pp. 1–6.

[44] J. Blank and K. Deb, “Pymoo: Multi-objective optimization in python,”

Ieee access, vol. 8, pp. 89 497–89 509, 2020.

[45] Y. Sun, G. G. Yen, and Z. Yi, “Igd indicator-based evolutionary algo-

rithm for many-objective optimization problems,” IEEE Transactions on Evolutionary Computation, vol. 23, no. 2, pp. 173–187, 2018.

[46] L. Bradstreet, The hypervolume indicator for multi-objective optimisa-

tion: calculation and use. University of Western Australia Perth, 2011.

[47] K. Li, R. Chen, G. Fu, and X. Yao, “Two-archive evolutionary algorithm

for constrained multiobjective optimization,” IEEE Transactions on Evolutionary Computation, vol. 23, no. 2, pp. 303–315, 2018.

[48] R. Cheng, Y. Jin, M. Olhofer, and B. Sendhoff, “A reference vector

guided evolutionary algorithm for many-objective optimization,” IEEE Transactions on Evolutionary Computation, vol. 20, no. 5, pp. 773–791, 2016.

[49] A. Panichella, “An adaptive evolutionary algorithm based on non-

euclidean geometry for many-objective optimization,” in Proceedings of the genetic and evolutionary computation conference, 2019, pp. 595– 603.

[50] N. Beume, B. Naujoks, and M. Emmerich, “Sms-emoa: Multiobjective

selection based on dominated hypervolume,” European Journal of Operational Research, vol. 181, no. 3, pp. 1653–1669, 2007.

[51] K. Deb, R. B. Agrawal et al., “Simulated binary crossover for continuous

search space,” Complex systems, vol. 9, no. 2, pp. 115–148, 1995.

[52] K. Deb, K. Sindhya, and T. Okabe, “Self-adaptive simulated binary

crossover for real-parameter optimization,” in Proceedings of the 9th annual conference on genetic and evolutionary computation, 2007, pp. 1187–1194.

[53] H. Ouerfelli and A. Dammak, “The genetic algorithm with two point

crossover to solve the resource-constrained project scheduling problems,” in 2013 5th International Conference on Modeling, Simulation and Applied Optimization (ICMSAO). IEEE, 2013, pp. 1–4.

[54] J. Garnier, L. Kallel, and M. Schoenauer, “Rigorous hitting times for

binary mutations,” Evolutionary Computation, vol. 7, no. 2, pp. 173– 203, 1999.

[55] I. Ono, M. Yamamura, and S. Kobayashi, “A genetic algorithm for job-

shop scheduling problems using job-based order crossover,” in Proceedings of IEEE International Conference on evolutionary computation. IEEE, 1996, pp. 547–552.

[56] M. B. Schmid and J. R. Roth, “Genetic methods for analysis and

manipulation of inversion mutations in bacteria,” Genetics, vol. 105, no. 3, pp. 517–537, 1983.

[57] Z. H. Ahmed, “Genetic algorithm for the traveling salesman problem

using sequential constructive crossover operator,” International Journal of Biometrics & Bioinformatics (IJBB), vol. 3, no. 6, p. 96, 2010.
