**A Systematic Survey on Large Language Models for Algorithm Design** 

FEI LIU, City University of Hong Kong, China YIMING YAO, City University of Hong Kong, China PING GUO, City University of Hong Kong, China ZHIYUAN YANG, Huawei Noah’s Ark Lab, China XI LIN, Xi’an Jiaotong University, China 

ZHE ZHAO, City University of Hong Kong, China 

XIALIANG TONG, Huawei Noah’s Ark Lab, China 

KUN MAO, Huawei Cloud EI Service Product Dept., China 

ZHICHAO LU, City University of Hong Kong, China ZHENKUN WANG, Southern University of Science and Technology, China MINGXUAN YUAN, Huawei Noah’s Ark Lab, China QINGFU ZHANG<sup>∗</sup> , City University of Hong Kong, China 

Algorithm design is crucial for effective problem-solving across various domains. The advent of Large Language Models (LLMs) has notably enhanced the automation and innovation within this field, offering new perspectives and promising solutions. In just a few years, this integration has yielded remarkable progress in areas ranging from combinatorial optimization to scientific discovery. Despite this rapid expansion, a holistic understanding of the field is hindered by the lack of a systematic review, as existing surveys either remain limited to narrow sub-fields or with different objectives. This paper seeks to provide a systematic review of algorithm design with LLMs. We introduce a taxonomy that categorises the roles of LLMs as optimizers, predictors, extractors and designers, analyzing the progress, advantages, and limitations within each category. We further synthesize literature across the three phases of the algorithm design pipeline and across diverse algorithmic applications that define the current landscape. Finally, we outline key open challenges and opportunities to guide future research. To support future research and collaboration, we provide an accompanying repository at: https://github.com/FeiLiu36/LLM4AlgorithmDesign. 

CCS Concepts: • Computing methodologies _→_ Search methodologies; _Heuristic function construction_ ; • Theory of computation _→_ Design and analysis of algorithms; Algorithm design techniques; 

Additional Key Words and Phrases: Algorithm design, Large language model, LLM4AD, Optimization, Heuristic, Evolutionary algorithm. 

> ∗the corresponding author 

Authors’ Contact Information: Fei Liu, fliu36-c@my.cityu.edu.hk, City University of Hong Kong, Hong Kong, China; Yiming Yao, yimingyao3-c@my.cityu.edu.hk, City University of Hong Kong, Hong Kong, China; Ping Guo, pingguo5-c@my.cityu.edu.hk, City University of Hong Kong, Hong Kong, China; Zhiyuan Yang, zhiyuan.yang@my.cityu.edu.hk, Huawei Noah’s Ark Lab, Hong Kong, China; Xi Lin, xi.lin@my.cityu. edu.hk, Xi’an Jiaotong University, Xi’an, China; Zhe Zhao, zzhao26-c@my.cityu.edu.hk, City University of Hong Kong, Hong Kong, China; Xialiang Tong, tongxialiang@huawei.com, Huawei Noah’s Ark Lab, Shenzhen, China; Kun Mao, maokun@huawei.com, Huawei Cloud EI Service Product Dept., Shenzhen, China; Zhichao Lu, luzhichaocn@gmail.com, City University of Hong Kong, Hong Kong, China; Zhenkun Wang, wangzk3@sustech.edu.cn, Southern University of Science and Technology, Shenzhen, China; Mingxuan Yuan, yuan.mingxuan@huawei.com, Huawei Noah’s Ark Lab, Hong Kong, China; Qingfu Zhang, qingfu. zhang@cityu.edu.hk, City University of Hong Kong, Hong Kong, China. 

2025. ACM XXXX-XXXX/2025/1-ART https://doi.org/XXXXXXX.XXXXXXX 

, Vol. 1, No. 1, Article . Publication date: January 2025. 

Liu et al. 

2 

# **1 Introduction** 

Algorithms, which are a sequence of computational steps for solving a well-specified computational problem [24], play a crucial role in addressing various problems across various domains such as industry, economics, healthcare, and technology [24, 75]. Traditionally, designing algorithm has been a labor-intensive process that demands deep expertise. Recently, there has been a surge in interest towards employing learning and computational intelligence methods techniques to enhance and automate the algorithm development process [7, 142]. 

Over the past few years, the application of Large Language Models for Algorithm Design (LLM4AD) has merged as a promising research area with the potential to fundamentally transform the ways in which algorithms are designed, implemented, and optimized. The remarkable capability and flexibility of LLMs have demonstrated potential in enhancing the algorithm design process from algorithm ideation [46] to implementation [91]. This approach not only reduces the human effort required in the design phase but also enhances the creativity and efficiency of the produced solutions [94, 116, 124]. 

Despite this surge of interest, the field lacks a systematic survey with a clear organizational structure. While several recent surveys have reviewed the interaction of LLM and algorithms, they either focus on narrow sub-fields or adjacent but different domains. For example, code generation surveys [71, 152, 154, 193] emphasize translating specifications into executable code, focusing on implementation rather than the upstream ideation and strategic design of algorithms. Reviews on optimization and evolutionary computation [37, 64, 163, 189] target specific problem classes (e.g., combinatorial optimization), offering limited breadth beyond the target sub-fields. Surveys on LLM agents and planning [41, 52, 117, 154] center on system architecture, tool use, and reasoning pipelines rather than the creation and refinement of core algorithmic logic. As summarized in Table 1, these surveys cover partial stages of algorithm design or specific algorithm types. 

This paper aims to fill this gap by providing a systematic survey dedicated to the emerging field of LLM4AD. To ensure conceptual clarity, we first establish a precise definition for “algorithm design” and the scope of this survey, distinguishing it from general-purpose programming. We then introduce a role-based taxonomy that organizes the literature according to the four fundamental ways LLMs are being employed in the algorithm design process. By synthesizing insights from over 180 recent papers, we analyze the using of LLM in different algorithm design stages and application domains. Finally, we critically assess the field’s current challenges and identify promising opportunities for future research. We intend for this survey to serve as an essential resource for both newcomers seeking a structured overview and experts looking for a consolidated analysis of the latest advancements. 

Fig. 1 provides an overview of this survey’s structure. The remainder of the paper is organized as follows. Section 2 outlines our survey methodology, including scope and literature collection and screening pipeline. Section 3 introduces a taxonomy for organizing LLM4AD research, categorizing works based on the primary role of the LLM in the algorithm design process: as optimizer (LLMaO), predictor (LLMaP), extractor (LLMaE), or designer (LLMaD). Subsequently, Section 4 reviews works across different algorithm development stages, while Section 5 summarizes key application domains. Section 6 discusses current open challenges and promising future research directions. Finally, Section 7 presents the conclusions. 

, Vol. 1, No. 1, Article . Publication date: January 2025. 

A Systematic Survey on Large Language Models for Algorithm Design 

3 

Table 1. A Comparison of Different Survey Papers Across Algorithmic Design Stages and Algorithm Types. 

||||Algo|rithmic Design S|tages|Algo|rithm Types||
|---|---|---|---|---|---|---|---|---|
|Year|Survey|LLM|||||||
||||Algorithm<br>Ideation|Algorithm<br>Implementation|Algorithm<br>Evaluation|Non-heuristic|Heuristic and<br>Metaheuristic|Hybrid|
||Wang et al. [152]|Yes|No|Yes|Partial|No|No|No|
|2023|Zhao et al. [191]|Yes|Yes|Yes|Partial|No|Yes|Partial|
||Zheng et al. [193]|Yes|No|Yes|Partial|Partial|Partial|Partial|
||Ahn et al. [4]|Yes|Partial|No|No|Yes|No|No|
||Guo et al. [52]|Yes|No|Partial|Partial|Partial|Partial|Partial|
|2024|Jiang et al. [71]|Yes|No|Yes|Partial|No|No|No|
||Joel et al. [74]|Yes|No|Yes|Partial|No|No|No|
||Wu et al. [163]|Yes|Partial|Partial|Partial|No|Partial|Partial|
||Fan et al. [37]|Partial|No|Yes|Yes|Yes|Yes|Yes|
||Ferrag et al. [41]|Yes|No|Partial|Partial|Partial|Partial|Partial|
||Zhang et al. [189]|Yes|Partial|Partial|Partial|No|Partial|Partial|
|2025|Ma et al. [106]|Partial|Partial|Yes|Yes|No|Partial|Partial|
||Da Ros et al. [26]|Yes|Partial|Yes|Yes|No|Partial|Partial|
|Ours||Yes|Yes|Yes|Yes|Yes|Yes|Yes|





<!-- Start of picture text -->
Definition and Scope<br>Scope<br>&Paper Collection Paper Collection and Scanning<br>LLM as Optimizer (LLMaO)<br>LLM as Predictor (LLMaP)<br>Taxonomy<br>LLM as Extractor (LLMaE)<br>LLM as Designer (LLMaD)<br>Algorithm Ideation<br>Stages Algorithm Implementation<br>Algorithm Evaluation<br>Optimization Algorithms<br>Applications Machine Learning Systems and Data Science<br>Scientific and Symbolic Domains<br>Scalability<br>Generalization<br>Challenges<br>Interpretability<br>&Future Directions<br>Efficiency<br>Benchmarking<br>Algorithm Design with LLMs<br><!-- End of picture text -->

Fig. 1. Overview of the Survey Structure: Scope, Taxonomy of LLM Roles, Stages of Algorithm Design, Applications, Open Challenges and Future Directions. 

, Vol. 1, No. 1, Article . Publication date: January 2025. 

Liu et al. 

4 

# **2 Methodology** 

# **2.1 Definition and Scope** 

This paper focuses on studies where LLMs substantively contribute to the conception, synthesis, or refinement of algorithms. This section defines our core concepts and delineates the scope of this survey to clarify its boundaries with respect to related research works. 

_Algorithm._ We adopt the definition of an “algorithm” as a well-defined computational procedure that transforms a set of inputs into a set of outputs in a finite amount of time [24]. This includes deterministic and stochastic procedures, exact methods and approximations [75], as well as heuristics and metaheuristics [47]. Examples include a procedure that sorts a set of integers, a method that finds a shortest path on a graph, or a heuristic for a scheduling problem. This scope covers both classic textbook algorithms and practically motivated strategies that trade optimality for speed or simplicity. 

_Algorithm Design._ We cover three stages of algorithm design: i) generation of algorithmic ideas or pseudocodes [133]; ii) algorithm implementation, which concerns the production of executable code from specifications [147]; and iii) algorithm evaluation, where LLMs are used for assessing the performance and analyzing the behavior of the designed algorithms [94]. A crucial distinction is made between algorithm design and general-purpose code generation [71]. Studies that merely translate algorithms or procedures into code are excluded. 

_Large Language Models._ Our focus is on large-scale language models, typically with billions of parameters, capable of sophisticated text and code processing [192]. This includes both text-only and multi-modal LLMs where language is a core component. We exclude smallerscale models and traditional machine learning approaches for algorithm generation, which have been discussed by other survey papers [7, 106]. 

# **2.2 Paper Collection and Scanning** 

We introduce the detailed pipeline for paper collection and scanning, which consists of three stages: 

- Stage I Data Extraction and Collection: We collect the related papers through Google Scholar, Web of Science, and Scopus. The logic of our search is the title must include any combinations of at least one of the following two groups of words “LLM”, “LLMs”, “Large Language Model”, “Large Language Models” and “Algorithm”, “Heuristic”, “Search”, “Optimization”, “Optimizer”, “Design”, “Function” (e.g., LLM and optimization, LLMs and algorithm). After removing duplicate papers, we ended up with around 3,000 papers as of October 1, 2025. 

- Stage II: Paper Screening This stage involved a two-step screening process to identify the most relevant papers. First, we screened the titles and abstracts of the 3,000 papers against predefined exclusion criteria: i) The paper is _not_ written in English. ii) The paper’s primary focus is _not_ on algorithm design (e.g., it focuses only on general code generation without any algorithmic component). iii) The paper does _not_ utilize large language models as defined in our scope. This initial screening narrowed the corpus down to about 500 papers. Subsequently, we conducted a full-text review of these manuscripts, applying the same exclusion criteria more rigorously to filter out papers that, upon closer inspection, lacked substantive content on LLM-aided algorithm design. This thorough review resulted in a refined set of 150 high-quality, relevant papers. 

, Vol. 1, No. 1, Article . Publication date: January 2025. 

A Systematic Survey on Large Language Models for Algorithm Design 

5 



<!-- Start of picture text -->
Stage I: Data extraction and  Stage II: Paper Screening Stage III: Snowballing and<br>collection Cross-checking<br>• Key Words:  Title = (LLM OR  • Screen the titles and abstracts  • Examine the reference lists to<br>Large Language Model) AND  first and then check the full text  identify additional relevant<br>(Algorithm OR Heuristic OR  for these related manuscripts studies, particularly those using<br>Search OR Optimization OR  different terminology<br>• Exclusion criteria:  not English,<br>Optimizer OR Design OR  not algorithm design, not using  • Add additional papers manually<br>Function)<br>large language models based on domain expertise<br>• Database:  Google scholar,  • Remaining Results:                    • Final Results:<br>Web of Science, Scopus<br>About 150 papers About 180 papers<br>• Results (remove duplication):<br>About 3000 papers<br><!-- End of picture text -->

Fig. 2. A Three-stage Pipeline for Paper Collection and Screening. 



<!-- Start of picture text -->
80<br>10.7% 6.7%<br>60<br>40 22.8% Research ParadigmsLLM as Predictor<br>LLM as Optimizer<br>LLM as Designer<br>LLM as Extractor<br>20<br>59.7%<br>0<br>Year<br>(a) Annual Publication Volume of Sur- (b) Distribution on Research Paradigms<br>veyed Papers (until Sep. 2025).<br>2022 2023 2024 2025<br>Number of Publications<br><!-- End of picture text -->

Fig. 3. Publication Trends and Paradigm Distribution in the Surveyed Literature. 

- Stage III: Snowballing and Cross-checking To ensure comprehensive coverage and mitigate the limitations of keyword-based searches, we performed a backward snowballing procedure on the 150 papers. This involved manually examining the reference lists of these papers to identify relevant studies that our initial search may have missed (for instance, papers using terminology like “code generation” instead of “algorithm design” but still involving some algorithm design tasks). Additionally, we manually appended a small number of works based on the authors’ domain knowledge to avoid omitting any important contributions. After integrating these additional papers identified through snowballing and expert knowledge, our final corpus contained over 180 papers. 

We acknowledge that, given the vast domains of algorithm design and the volume of literature, it is impossible to guarantee an exhaustive coverage of all relevant papers. Instead, our objective is to systematically survey the landscape, focusing on a representative body 

, Vol. 1, No. 1, Article . Publication date: January 2025. 

Liu et al. 

6 



<!-- Start of picture text -->
Problem Algorithm Solution<br>Solution Solution<br>LLM<br>(a) LLM as Optimizer (LLMaO)<br><!-- End of picture text -->

`You are tasked with a Traveling Salesman Problem. Given the following coordinate points:` A (0,0), B (2,2), C (5,1), D (4,4) 



`and known tours with their total lengths:` Tour 1: A → B → C → D → A (length: 14.81) Tour 2: A → C → B → D → A (length: 16.75) `Please generate a better tour with shorter total length.` Directly output the optimized tour (format: A → X → Y → Z → A). No additional text. 



<!-- Start of picture text -->
A → B → D → C → A<br><!-- End of picture text -->



## (b) An example for LLMaO in a Traveling Salesman Problem 

Fig. 4. (a) Large Language Models as Optimizers (LLMaO). LLMs Serve as Optimizers within the Algorithm to Generate New Solutions. (b) An Example for LLMaO on Traveling Salesman Problem. 

of work that allows us to organize and discuss the field. Fig. 3a illustrates the number of publications per year surveyed in this paper. The graph shows a marked rise in research activity related to LLM4AD, and most of the related studies have been conducted in the last two years. 

# **3 Taxonomy of LLM Roles in Algorithm Design** 

According to the roles of LLM in algorithm design, existing works can be categorized into four paradigms: LLM as Optimizer (LLMaO), LLM as Predictor (LLMaP), LLM as Extractor (LLMaE), and LLM as Designer (LLMaD). Fig. 3b displays the distribution of publications across these four paradigms. This section discusses the progress, advantages, and limitations of each category. 

# **3.1 LLM as Optimizer (LLMaO)** 

In LLMaO (Fig. 4), LLMs are employed as a black-box optimizer within an algorithmic framework to generate and refine solutions. Fig. 4 (b) illustrates an example applied to the Traveling Salesman Problem (TSP), which involves optimizing a tour that visits each city (node) exactly once and returns to the starting city, with the goal of minimizing the total route length. In this example, we are given four nodes (A, B, C, and D) with their coordinates, and the algorithm has two existing tours (tour 1 and tour 2) each with a different sequence and route length. The LLM is used to generate a potentially better tour with a shorter length. The LLM directly outputs the optimized tour sequence, which is commonly the role of hard-coded optimizers within traditional algorithmic approaches. 

One of the initial efforts to utilize LLM as Optimizer in algorithm design is by Yang et al. [170]. They leverage the in-context learning capabilities of LLMs to generate new solutions for specific problems based on previously evaluated solutions. This method is applied iteratively 

, Vol. 1, No. 1, Article . Publication date: January 2025. 

A Systematic Survey on Large Language Models for Algorithm Design 

7 

to refine solutions further. Yang et al. [170] have successfully demonstrated this technique across various domains, including continuous and combinatorial optimization, as well as machine learning tasks. 

From an evolutionary algorithm perspective, using LLMs to generate solutions from existing data can be seen as analogous to search operators in EA. For instance, Liu et al. [88] introduce the use of LLMs as evolutionary operators to tackle multi-objective problems. This method involves breaking down a multi-objective problem into simpler single-objective tasks, with LLMs acting as black-box search operators for each sub-problem to suggest new solutions. In a related study, Liu et al. [98] explore the integration of LLMs within EAs, not just for generating solutions but also for guiding selection, crossover, and mutation processes. Meanwhile, Brahmachary et al. [11] propose a new population-based evolutionary framework that includes both exploration and exploitation pools, with solutions being exchanged during the optimization process and LLMs generating solutions for both pools. 

Differing from direct solution generation, Lange et al. [77] investigate the use of LLMs in designing evolution strategies, introducing a new prompting strategy to enhance the mean statistic in their EvoLLM method, which shows superior performance over baseline algorithms in synthetic black-box optimization functions and neuroevolution tasks. They also demonstrate that fine-tuning LLMs with data from teacher algorithms can further improve the performance of EvoLLM. Custode et al. [25] present a preliminary study that uses LLMs to automate hyperparameter selection by analyzing optimization logs and providing real-time recommendations. Moreover, Xu et al. [169] adopt LLMs to adaptively adjust the hyperparameter for metaheuristic algorithms. 

Beyond traditional optimization tasks, LLMaO has been widely adopted in prompt engineering for LLMs, a process often referred to as “automatic prompt optimization” [196]. These methods primarily involve iterative refinement of prompts by LLMs to improve their effectiveness for specific models (typically LLMs). Techniques include resampling-based strategies, where LLMs generate variations of original prompts while maintaining semantic similarity [156], and reflection-based strategies, where LLMs optimize by analyzing and learning from previous prompt iterations or errors [51], have been explored. Ma et al. [103] note that LLM optimizers often struggle to accurately identify the root causes of errors during the reflection process, influenced by their pre-existing knowledge rather than an objective analysis of mistakes. To address these issues, they propose a new approach termed “automatic behavior optimization”, aimed at directly and more effectively controlling the behavior of target models. Liu et al. [97] introduce RSBench, a benchmark set specifically for the task of evaluating LLM-based evolutionary algorithms in optimizing recommendation prompts in recommender systems. 

_Discussion:_ Traditional optimizers rely on numerical or symbolic update rules. LLMaO introduces a language-conditioned optimization process, where LLMs propose and refine candidate solutions by reasoning over problem descriptions, instance context, and past trajectories rather than following fixed mathematical updates. 

- Advantages: 1) Leverages pre-trained domain knowledge and natural-language context. For example, in the TSP, conventional operators (e.g., 2-opt [78]) improve routes based on hard-coded heuristics that do not exploit textual instance information. In contrast, LLM-based optimizers can condition on problem descriptions, constraints, previously evaluated tours and history information to produce informed improvements. Liu et al. [98] integrate LLMs as evolutionary optimizers; given task descriptions, existing solutions, and stepwise traces, the LLM performs multi-step search and generates new 

, Vol. 1, No. 1, Article . Publication date: January 2025. 

Liu et al. 

8 

candidates. 2) Enables adaptive refinement without handcrafted rules. Yang et al. [170] show that LLMs can infer optimization directions from prompt-supplied trajectories on small-scale problems, and Nie et al. [115] demonstrate that natural-language feedback during search further enhances LLM-driven optimization. 

- Limitations: 1) Limited interpretability and theoretical guarantees due to the blackbox nature. Early efforts approximate LLM behavior with linear operators [88] and analyze convergence under restricted settings [79], but general frameworks remain open. 2) Sensitivity to prompts and domain priors. Competitive results often require careful prompt design and alignment with the LLM’s training distribution [170]. 3) Computational and token cost at scale. Most evaluations focus on small instances [98, 170]; scaling to large problems is challenging due to long inputs/outputs, inference latency, and costs [88]. 

# **3.2 LLM as Predictor (LLMaP)** 

LLMaP utilizes LLMs as surrogate models (Fig. 5) to predict the outcomes or responses of solutions, operating in either a classification or regression context [56]. Fig. 5 (b) provides an example on a simple TSP instance, where the LLM is given the task description and a set of existing evaluated tours along with their corresponding lengths. The LLM is then instructed to evaluate a new tour, predicting its length and performance (whether it improves upon the existing tours). Note that while the length of a TSP tour is easily calculated and serves here as a straightforward illustration, LLMaP is designed for tasks where evaluations are typically expensive or difficult to obtain. 



<!-- Start of picture text -->
Problem Algorithm Solution<br>Fitness /<br>Solution<br>Category<br>LLM<br>(a) LLM as Predictor (LLMaP)<br>You are tasked with a Traveling Salesman Problem. Given the following coordinate points:<br>A (0,0), B (2,2), C (5,1), D (4,4)<br>and known tours with / without their total lengths:<br>Tour 1: A → B → C → D → A (length: 14.81)<br>Tour 2: A → C → B → D → A (length: 16.75)<br>Tour 3:  A → B → D → C → A  (length: ?)<br>Please evaluate the unlabeled tour based on the numerical attributes and determine its<br>category as ‘better’ or ‘worse’ in terms of total length. No additional text.<br><!-- End of picture text -->



<!-- Start of picture text -->
length: 13.92 (better)<br><!-- End of picture text -->



(b) An example for LLMaP in a Traveling Salesman Problem 

Fig. 5. (a) Large Language Models as Predictors (LLMaP). LLMs are Utilized Iteratively in Algorithms to Predict a Solution’s Outcomes or Responses. (b) An Example for LLMaP on Traveling Salesman Problem. 

The majority of LLMaP works use LLMs as pre-trained models as a regression model to predict solution scores. For instance, LLMs have been used as performance predictors for deep 

, Vol. 1, No. 1, Article . Publication date: January 2025. 

A Systematic Survey on Large Language Models for Algorithm Design 

9 

neural network architectures by Jawahar et al. [69]. It offers a cost-effective alternative for performance estimation in neural architecture search. Zhang et al. [188] introduce LINVIT, an algorithm that incorporates guidance from LLMs as a regularization factor in value-based RL to improve sample efficiency. Science discovery is another domain that LLMaP has commonly investigated. For example, Li et al. [83] introduce CodonBERT for sequence optimization of mRNA-based vaccines and therapeutics. CodonBERT uses codons as inputs and is trained on over 10 million mRNA sequences from various organisms. Soares et al. [136] demonstrate the use of LLMs in predicting the performance of battery electrolytes. Other applications include employing LLMs to determine the fame score of celebrities to predict the box office performance of projects in the motion pictures industry [5] and adopting LLMs to score the video question answering by using detailed video captions as content proxies [184]. 

For classification, Hao et al. [56] introduce LAEA, which employs LLMs as surrogate models within evolutionary algorithms for both regression and classification, eliminating the need for costly model training. In another study, Chen et al. [20] develope a label-free node classification method that leverages LLMs to annotate nodes. These annotations are subsequently used to train graph neural networks, resulting in enhanced performance. Moving beyond binary classification, Bhambri et al. [8] utilize LLMs to predict discrete actions for constructing reward shaping functions in Reinforcement Learning (RL). Their method demonstrate effectiveness within the BabyAI environment, showcasing the versatility of LLMs in various settings. Wang et al. [155] explore the use of LLMs in federated search, applying them in a zero-shot setting to effectively select resources. This approach highlights the potential of LLMs in improving resource selection without prior explicit training on specific tasks. 

_Discussion:_ Conventional surrogate models (e.g., Gaussian processes (GPs) or neural regressors [73]) rely on structured features and explicit training. In contrast, LLMaP leverages pre-trained LLMs as semantic surrogates that can interpret textual and multimodal context when predicting outcomes. 

- Advantages: 1) Effective in data-scarce or concept-driven tasks due to embedded general knowledge [35]. For example, Wong et al. [162] employ a multimodal LLM to score car shapes, accelerating early-stage design by filtering out poor candidates before costly simulation signals that conventional surrogates built on numeric features struggle to capture. Ge et al. [44] adopt LLMs to extract deeper interest preferences from the user’s behaviour and interaction history to dynamically adjust the prediction of user’s rating of items in the recommendation algorithm. 2) Requires little or no retraining, reducing computational cost. As discussed by Hao et al. [56], conventional surrogates often require repeated rebuilding or fine-tuning as new solutions are sampled, which is expensive for large-scale cases. LLMs can be used zero-shot or with lightweight in-context examples and can use flexible descriptors (text, code, images), thereby avoiding tedious feature engineering. 

- Limitations: 1) Quantitative precision is often inferior to specialized regression models. In the evaluation by Hao et al. [56], LLMs, though flexible, often achieve lower accuracy compared to GP models trained directly on the target data. Xie et al. [166] propose hybrid schemes that combine LLMs with conventional surrogates: instead of predicting scores directly, the LLM selects which specialized surrogate to use, offering a pragmatic compromise between performance and efficiency. 2) Outputs are sensitive to prompt design and phrasing. For example, Taboada et al. [141] use LLMs for ontology alignment 

, Vol. 1, No. 1, Article . Publication date: January 2025. 

Liu et al. 

10 

and find that simple prompts limit performance, whereas incorporating contextual ontology information improves matching accuracy. This sensitively introduces additional costs for prompt refinement, which relies on domain knowledge. 

# **3.3 LLM as Extractor (LLMaE)** 

LLMaE leverages LLMs to mine and extract embedded features or specific knowledge from target problems and/or algorithms, which are then used to enhance algorithm-based problem solving (Fig. 6). As shown in Fig. 6 (b), when provided with the task description and tours for a TSP instance, LLMs can be instructed to extract key features, such as node count, which can then be utilized in algorithm design. These features are typically defined by experts or learned implicitly using conventional machine learning models. 



<!-- Start of picture text -->
Problem Algorithm Solution<br>Solution Embedding<br>LLM<br><!-- End of picture text -->



<!-- Start of picture text -->
(a) LLM as Extractor  (LLMaE)<br><!-- End of picture text -->



`You are tasked with a Traveling Salesman Problem. Given the following coordinate points: A (0,0), B (2,2), C (5,1), D (4,4) and known tours with their total lengths:` Tour 1: A → B → C → D → A (length: 14.81) Tour 2: A → C → B → D → A (length: 16.75) `Extract and output the features of the problem in JSON format. No additional text. {"node_count": 4, "coordinate_range": {"x": [0, 5], "y": [0, 4]}, "centroid": [2.75, 1.75], "distance_matrix": {"A": {"B": 2.83, "C": 5.10, "D": 5.66}, "B": {"C": 3.16, "D": 2.83}, "C": {"D": 3.16}}, "closest_pair": ["A", "B"], ["B", "D"], "farthest_pair": ["A", "D"], "best_known_length": 14.81, "optimization_goal": "minimize_tour_length"}` 



(b) An example for LLMaE in a Traveling Salesman Problem 

Fig. 6. (a) Large Language Models as Extractors (LLMaE). LLMs are Employed to Extract Features or Specific Knowledge from Target Problem and/or Algorithms. (b) An Example for LLMaE on Traveling Salesman Problem. 

Beyond embedding-based feature extraction, LLMs excel in text comprehension and knowledge extraction, allowing them to discern subtle patterns and relationships within the data that might not be evident through conventional feature extraction methods. For example, Wu et al. [164] utilize LLMs to extract high-dimensional algorithm representations by comprehending code text. These representations are combined with problem representations to determine the most suitable algorithm for a specific problem. Du et al. [31] propose a mixture-of-experts framework augmented with LLMs to optimize various wireless user tasks. The LLM is used to analyze user objectives and constraints, thus selecting specialized experts, and weighing decisions from the experts, reducing the need for training new models for each unique optimization problem. Additionally, Memduhoğlu et al. [108] use LLM to enhance the classification of urban building functions by interpreting OpenStreetMap tags and integrating them with physical and spatial metrics. Traditional techniques, which have previously struggled with semantic ambiguities, are outperformed by LLMs due to their 

, Vol. 1, No. 1, Article . Publication date: January 2025. 

A Systematic Survey on Large Language Models for Algorithm Design 

11 

superior ability to capture broader language contexts. Beyond extracting problem features, LLMs are employed to mine relevant knowledge to inform and enhance algorithm design. In HiFo-Prompt [16], for example, knowledge is distilled into reusable design principles that guide the design process. 

Typical feature extraction relies on statistical learning or dimensionality reduction from structured data. LLMaE instead is able to perform semantic extraction, deriving contextual features and domain knowledge from unstructured sources such as text, code, or documentation. 

- Advantages: 1) It generates concept-aware embeddings that integrate both linguistic and symbolic meaning. For instance, Xu et al. [168] use LLMs to analyze existing heuristic structures and extract underlying design principles and domain-relevant insights, thereby providing a warm start to enhance the quality of designed heuristics. 2) It combines textual, spatial, and numeric features into a unified representation. For example, [164] use LLMs to extract algorithm features for algorithm selection. Unlike traditional approaches, such as machine learning prediction models, both text descriptions and code implementations can be leveraged. 

- Limitations: 1) There is a risk of hallucinated or misinterpreted features in specialized domains. For instance, [60] report information loss and misinterpretation when using multi-modal LLMs for designing algorithms for agents. 2) The validation and interpretability of embeddings remain challenging. Jiang et al. [72] use LLM embeddings to solve the vehicle routing problem. While the extracted information proves beneficial in ablation studies, providing a clear interpretation and analysis of the embedding remains difficult. 

# **3.4 LLM as Designer (LLMaD)** 

LLMaD directly creates algorithms or specific components (Fig. 7). LLMs can generate heuristics [91], write code snippets [57], and formulate functions [124] that integrate seamlessly into algorithmic systems, or even design the entire algorithms [116, 146]. Fig. 7 demonstrates this process using a TSP instance. Unlike other paradigms, LLMaD directly produces new algorithms or algorithm components based on a task description and an existing algorithm implementation. 

Function design is among the early applications of LLMaD. Eureka [104] leverages the capabilities of LLMs in code-writing, and in-context learning to evolve and optimize reward functions for RL. It can generate reward functions without specific prompts or predefined templates, achieving better performance than rewards designed by human experts. Similarly, Auto MC-Reward [80] utilizes LLMs to automatically design dense reward functions for RL agents in environments with sparse rewards. The three key components of Auto MCReward work together to iteratively refine the reward function based on feedback from the agent’s interactions with the environment. Through this iterative process, the agent is able to learn complex tasks more efficiently, as demonstrated in experiments in Minecraft. Moreover, FunSearch [124] adopts LLMs for function generation in an evolutionary framework with a multi-island population management. It demonstrates promising results on both mathematical problems and combinatorial optimization problems. 

EoH [90, 91] presents an early attempt to adopt the LLM as a designer for Automated Heuristic Design (AHD). It uses both heuristic ideas and code implementations to represent heuristics and adopts LLM in an evolutionary framework to create, combine, and revise the heuristics. While it is original proposed for heuristic design, it has been applied on different 

, Vol. 1, No. 1, Article . Publication date: January 2025. 

Liu et al. 

12 



<!-- Start of picture text -->
Problem Algorithm Solution<br>Algorithm<br>LLM<br>(a) LLM as Designer (LLMaD)<br>You are tasked with a Traveling Salesman Problem. Given the  # Improved TSP algorithm using nearest neighbor<br>following coordinate points:  heuristic<br>A (0,0), B (2,2), C (5,1), D (4,4)<br>import itertools<br>and the existing algorithm for solving this problem: import math<br>importimport itertools math def    start =     tour = [start]tsp_nearest_neighborlist(points.keys())[0](points):<br>def tsp(points):     unvisited = set(points.keys()) - {start}<br>    tour = None<br>    min_distance = float('inf') while unvisited:<br>for perm in itertools.permutations(points.keys()):         last = tour[-1]<br>        dist = total_distance(perm + (perm[0],))         next_city = min(unvisited, key=lambda city:<br>if dist < min_distance:         distance(points[last], points[city]))<br>            min_distance = dist         tour.append(next_city)<br>            tour = perm         unvisited.remove(next_city)<br>return tour<br>Please generate a better algorithm following the above format.     tour.append(start)  return tour # Return to start<br>Directly output the improved algorithm. No additional text.<br>(b) An example for LLMaD in a Traveling Salesman Problem<br><!-- End of picture text -->

Fig. 7. (a) Large Language Models as Designers (LLMaD). LLMs are Used to Directly Create the Entire Algorithms or Specific Components. (b) An Example for LLMaD on Traveling Salesman Problem. 

algorithm design tasks including combinatorial optimization problems [89, 91, 172], Bayesian optimization [174], image adversary attack [50], and edge server task scheduling [157], among others. Moreover, LLaMEA [146, 149] develops an iterative framework to generate, mutate, and select algorithms based on performance metrics and runtime evaluations. The automatically designed algorithms outperform state-of-the-art optimization algorithms on some benchmark instances. ReEvo [178] introduces an evolutionary framework with both short and long-term reflections, which provides a search direction to explore the heuristic space. HSEvo [28] and PartEvo [61] integrate different diversity control strategies in evolutionary search framework to enhance the search. In addition to evolutionary search framework, recent attempts also adopt other frameworks such as large neighborhood search [167] and Monte Carlo Tree Search (MCTS) [194] for effective explore the algorithm space. Unlike previous studies that focus on optimizing a single performance criterion, MEoH [172] considers multiple performance metrics, including optimality and efficiency, and seeks a set of trade-off algorithms in a single run in a multi-objective evolutionary framework. A dominance-dissimilarity score is designed for effectively searching the complex algorithm space. 

LLM-based agent design has also gained much attention. For example, ADAS [62] proposes an automated design of agentic systems, which aims to automatically generate powerful agentic system designs by using meta agents that program new agents. They present a novel algorithm, meta agent search, which iteratively creates new agents from an archive of previous designs, demonstrating through experiments that these agents can outperform state-of-the-art hand-designed agents across various domains. Further studies on LLM-based agent systems are discussed in [137] and [100]. 

, Vol. 1, No. 1, Article . Publication date: January 2025. 

13 

A Systematic Survey on Large Language Models for Algorithm Design 



<!-- Start of picture text -->
1. Algorithm  2. Algorithm  3. Algorithm<br>Ideation Implementation Evaluation<br>Problem  Code Performance<br>Formulation Generation Testing<br>Algorithm  Algorithm  Algorithm<br>Concept Design Optimization Analysis<br><!-- End of picture text -->

Fig. 8. The using of LLMs in Different Stages of Algorithm Design: 1) Algorithm Ideation, 2) Algorithm Implementation, and 3) Algorithm Evaluation. 

_Discussion:_ Different from existing approaches, such as human-crafted heuristics, AutoML, and genetic programming, search within explicit procedural representations. LLMaD advances this by using LLMs for language-based algorithm synthesis, generating algorithms or components via natural-language reasoning and code generation. 

- Advantages: 1) Accelerates algorithm design by reducing human intervention and implementation effort. LLMaD often operates zero-shot or with lightweight iterative prompting; the outputs are executable text/code that can be inspected, profiled, and reused, while achieving competitive efficiency [91]. 2) Supports iterative self-improvement when embedded in feedback or evolutionary loops, expanding the creativity and diversity of algorithmic solutions [147, 182]. For instance, Zhang et al. [182] propose a treebased search framework that uses LLMs to design diverse, high-quality agents in an open-ended manner. 

- Limitations: 1) LLMs struggle with synthesizing complete, state-of-the-art algorithms for complex tasks; most studies target specific components (e.g., heuristics, reward functions, code snippets) rather than the complete solvers [116]. Challenges around correctness, robustness, and runtime guarantees persist. 2) Algorithm design is domainspecific, and standalone LLMs typically lack sufficient task-specific knowledge, leading to subpar performance [185]. Effective LLMaD systems therefore depend on search frameworks that iteratively test, execute, and refine designs while interacting with the environment and tools [148, 185]. 

# **4 Stages of LLM-Assisted Algorithm Design** 

Algorithm design is a multi-stage process where LLMs can provide targeted assistance at distinct phases. We identify three key stages in this process: 1) algorithm ideation, 2) algorithm implementation, and 3) algorithm evaluation. This section organizes the existing literature along these three stages, summarizing the typical artifacts, recent progresses and challenges. 

, Vol. 1, No. 1, Article . Publication date: January 2025. 

Liu et al. 

14 

# **4.1 Stage I: Algorithm Ideation** 

The ideation stage encompasses both problem formulation and the generation of novel algorithmic concepts. 

_Problem Formulation._ While not a direct step in creating an algorithm, modeling the target problem is a crucial precursor to its design, and LLMs are increasingly used to automate this process. Early systems, such as OptiMUS, guide users from natural language descriptions to formal linear programs, producing executable solver [2]. To mitigate the privacy and controllability concerns associated with proprietary APIs, ORLM combines an instructionfollowing recipe (OR-Instruct) with open-source backbone models, reporting strong results on benchmarks like NL4Opt and the new IndustryOR benchmark [63, 121]. Complementary fine-tuning strategies, such as those in LM4OPT, demonstrate that even modest-sized models can be specialized to reliably map domain-specific text to optimization modeling [3]. In the context of interactive decision support, DOCP integrates user feedback to progressively assemble problem-specific models before invoking solvers [160]. For a comprehensive overview, Xiao et al. [165] provide an in-depth survey of LLMs for optimization modeling. 

_Algorithm Concept Design._ LLMs have shown promise in generating new algorithmic ideas across various domains [133]. For instance, Pluhacek et al. [119] use LLMs to analyze and decompose well-performing algorithms to propose hybrid algorithms that combine their complementary strengths. While this work demonstrated that novel algorithmic ideas could be designed, it did not implement them for specific algorithm design tasks. EoH presents an early attempt to co-design algorithm concepts in natural language alongside their executable code implementations [91]. Different strategies have been explored to enhance this co-design search process, including reasoning over algorithmic ideas during design [10, 87] and controlling the diversity to foster innovation [173]. 

However, how to effectively measure the quality and novelty of an algorithmic idea remains an open question [92]. Moreover, the concept descriptions are often highly abstract, which lacks a strict mapping to a detailed implementation, therefore making it hard to effectively guide algorithm implementation [54]. 

# **4.2 Stage II: Algorithm Implementation** 

The implementation stage spans from initial code synthesis to subsequent performance optimization. 

_Code Generation._ Given an algorithmic idea or a natural language description, LLMs can be instructed to generate the corresponding code implementation [91, 174, 194]. Some works bypass the explicit ideation stage and directly use code as the primary representation of an algorithm [124, 178]. Instead of generating code from structure, ADAS employs meta-agents to program new agents from an archive of prior designs, thereby automating the construction of multi-component pipelines [62]. Initially, code generation focused on individual algorithmic components, reflecting the limited capabilities of early LLMs and simpler design pipelines [91, 124]. More recently, this has been extended to generating entire algorithms [146]. To handle large-scale code, Novikov et al. [116] use “diff blocks” to highlight specific sections, enabling the model to generate or revise partial code instead of regenerating the entire program. To improve reliability at scale, LLaMoCo introduces instruction tuning tailored to code generation for optimization tasks, reducing the reliance on expert-crafted prompts [105]. 

, Vol. 1, No. 1, Article . Publication date: January 2025. 

A Systematic Survey on Large Language Models for Algorithm Design 

15 

Despite these advances, the generation of entire, complex algorithms remains a significant challenge. First, the reliable generation of long programs is a difficult problem in itself [71]. Second, it is challenging to ensure that a complicated implementation correctly instantiates the intended algorithmic idea and is effective for the target task. Addressing this requires not only powerful LLMs but also sophisticated frameworks, such as multi-agent systems [67], to manage the complexity. 

_Algorithm Optimization._ A common pattern for algorithmic code optimization is closedloop refinement, where execution feedback informs subsequent code edits and integration choices [185]. Evolutionary search is the most prevalent framework for this purpose, maintaining a population of algorithms that are progressively refined by an LLM [185]. Variants of this simple evolutionary approach have emerged. For instance, ReEvo [178] combines shortand long-term reflection with information on history evaluated results to guide algorithm optimization, while HSEvo [28] adopts diversity control strategies with two population diversity measurements to enhance the optimization process. Recently, non-evolutionary search frameworks, such as large neighborhood search and Monte Carlo tree search [194], have also been demonstrated to be effective. Moreover, instead of prompting LLMs to optimize algorithm implementations, recent attempts have explored fine-tuning LLMs, in both offline [93] and online manners [66], to learn a preference for generating better-performing algorithms during algorithm optimization for specific design tasks. 

A significant open challenge is ensuring that the optimized algorithms generalize robustly. An algorithm may be overfitted to the specific benchmarks or problem instances used during the optimization loop, failing to perform well on unseen instances [134] or under different conditions [130]. 

# **4.3 Stage III: Algorithm Evaluation** 

The final stage, algorithm evaluation, involves assessing the performance and analyzing the behavior of the designed algorithms. 

_Performance Testing._ To ensure comparability and robustness in LLM-driven algorithm design, recent efforts have focused on establishing standardized benchmarks. Notable examples include CO-Bench and HeuriGym, which are tailored for structured combinatorial optimization tasks [17, 138]. In addition to combinatorial optimization, LLM4AD [94] provides a unified evaluation platform that spans a broader range of domains, including optimization, machine learning, and scientific discovery [94]. Beyond static benchmarks for testing, some approaches leverage LLMs to dynamically refine the evaluation process itself. For instance, Li et al. [81] propose a method to co-evolve algorithms and their test instances, aiming to generate more effective test cases that better guide the algorithm design process. Similarly, Duan et al. [34] introduce a mutation-based adversarial approach that dynamically evolves instance generation procedures to create increasingly difficult problems, thereby enhancing the generalization performance of the designed algorithms. 

Moving beyond a single performance score, a deeper evaluation should analyze the algorithm’s behavior, including its search trajectory, robustness across different problem distributions, convergence properties, and computational efficiency [172]. LLMs are uniquely positioned to automate this in-depth analysis. Just as a human expert would, they can interpret search patterns, identify failure modes, and diagnose the root causes of poor performance to provide actionable, human-like insights to directly enhance the design process [179]. 

, Vol. 1, No. 1, Article . Publication date: January 2025. 

Liu et al. 

16 

_Algorithm Analysis._ In addition to generation, LLMs are also being employed to analyze algorithmic outcomes and explain their behavior. d’Aloisio et al. [27] empirically analyze and compare the quality of explanations provided by three different LLMs for seven state-of-theart quantum algorithms. Their findings indicate that while the explanations were consistent across multiple iterations, there remains a significant gap for improvement in quality, and the results were highly sensitive to the specific prompts used. In a different application, Chacón Sartori et al. [14] integrate LLMs into STNWeb, an algorithm analysis tool. The LLM generates extensive written reports, complemented by automatically generated plots, which enhances the user experience and lowers the barrier to adoption for the broader research community. 

The central challenge for LLM-based algorithm analysis is the gap between descriptive summarization and causal, principled understanding. Current methods can generate consistent and well-written reports, but these often remain surface-level descriptions of behavior rather than deep explanations rooted in algorithmic theory [14]. The analysis quality is also highly sensitive to prompt engineering, making it unreliable and not yet a trustworthy source of foundational insight. For the field to advance, LLMs must move beyond post-hoc commentary to providing causal reasoning about why an algorithm performs as it does. For instance, by explain its convergence properties, time complexity, or failure modes based on its structural components [75, 92, 147]. 

# **5 Applications** 

# **5.1 Optimization Algorithms** 

In this subsection, we delve into the applications of LLMs in designing optimization algorithms. We categorize the existing literature into combinatorial optimization and continuous optimization. Then we proceed to compare the various roles played by LLMs, and the specific problems or tasks to which they are applied. The comparative analysis is summarized in Table 2, where we list the names of the frameworks or methods proposed by the authors. For studies that do not explicitly name their methods, we assign appropriate designations in our article and denote them with asterisks for easy reference (e.g., MH-LLM* for [126]). 

_5.1.1 Combinatorial Optimization._ In the domain of Combinatorial Optimization (CO), automated algorithm heuristics design has been a significant area of interest for a long time. The Traveling Salesman Problem (TSP) stands out as one of the most renowned CO problems, involving the quest for the shortest route to visit all specified locations exactly once and return to the starting point. Some recent work leverages LLMs to evolve algorithms within evolutionary computation framework, such as EoH [91] and ReEvo [178]. Differently, OPRO [170] employs LLMs as optimizers with a proposed meta-prompt, in which the solution-score pairs with task descriptions are added in each optimization step. Additionally, LMEA [98] investigates the utilization of LLMs as evolutionary combinatorial optimizers for generating offspring solutions, wherein a self-adaptation mechanism is introduced to balance exploration and exploitation. The Capacitated Vehicle Routing Problem (CVRP) extends the TSP by introducing constraints related to vehicle capacity. To address this challenge, MLLM [65] devises a multi-modal LLM-based framework with textual and visual inputs to enhance optimization performance. In addition to routing problems, other combinatorial optimization problems that have also been investigated include cap set [124], bin packing [91], flow shop scheduling [91], hybrid job shop scheduling [82] and social networks problems [126]. 

, Vol. 1, No. 1, Article . Publication date: January 2025. 

A Systematic Survey on Large Language Models for Algorithm Design 

17 

_5.1.2 Continuous Optimization._ For single-objective optimization problems with continuous variables, LLaMEA [146] utilizes LLMs to automate the evolution of algorithm design. It demonstrates the effectiveness in generating new metaphor-based optimization algorithms on BBOB benchmark [55] within IOHexperimenter benchmarking tool [29], which supports evaluating the quality of the generated algorithms and also provides feedback to the LLM during evolution. Instead of creating new algorithms, EvolLLM [77] introduces a prompt strategy that enables LLM-based optimization to act as an Evolution Strategy (ES) and showcases robust performance on synthetic BBOB functions and neuroevolution tasks. OPRO [170] illustrates that LLMs can effectively capture optimization directions for linear regression problems by leveraging the past optimization trajectory from the meta-prompt. Additionally, LEO [11] devises an explore-exploit policy using LLMs for solution generation, the method has been tested in both benchmark functions as well as industrial engineering problems. Different with directly employing LLMs for generating solutions, LAEA [56] introduces LLM-based surrogate models for both regression and classification tasks and has been validated on 2D test functions using nine mainstream LLMs. 

Beyond a single objective, there are multiple competing objectives that need to be optimized simultaneously in many scenarios, forming the multi-objective optimization problems (MOPs). The goal is to identify a set of optimal solutions, referred to as Pareto optimal solution set. An initial exploration of utilizing LLMs to tackle MOPs is introduced in MOEA/D-LMO [88]. Benefiting from the decomposition-based framework, the in-context learning process of LLMs is easily incorporated to generate candidate solutions for each subproblem derived from the original MOP. In the realm of large-scale MOPs, LLM-MOEA* [135] showcases the inferential capabilities of LLMs in multi-objective sustainable infrastructure planning problem. The study highlights the LLM’s proficiency in filtering crucial decision variables, automatically analyzing the Pareto front, and providing customized inferences based on varying levels of expertise. Additionally, CMOEA-LLM [159] leverages LLMs with evolutionary search operators to address the challenges of constrained MOPs and exhibits robust competitiveness in DAS-CMOP test suite [38]. 

In various real-world applications, the cost of evaluating the objective functions can be very expensive, which greatly limits the evaluation budget in the optimization process [42]. Bayesian optimization (BO) stands out as a sample-efficient method, it typically employs a surrogate model to approximate the expensive function and well-designed Acquisition Functions (AFs) to carefully select potential solutions. To facilitate the direct generation of solutions using LLMs, HPO-LLM* [183] provides LLMs with an initial set of instructions that outlines the specific dataset, model, and hyperparameters to propose recommended hyperparameters for evaluation in Hyperparameter Optimization (HPO) tasks. Furthermore, LLAMBO [99] incorporates LLM capabilities to enhance BO efficiency, in which three specific enhancements throughout the BO pipeline have been systematically investigated on tasks selected from HPOBench [36]. Instead of utilizing LLMs for direct solution generation, BO-LIFT* [122] utilizes predictions with uncertainties provided by a Language-Interfaced Fine-Tuning (LIFT) framework [30] with LLMs to perform BO for catalyst optimization using natural language. EvolCAF [174] introduces a novel paradigm to design AFs automatically for cost-aware BO. The approach showcases remarkable efficiency and discovers novel ideas not previously explored in existing literature on AF design. Similarly, FunBO [1] found novel and well-performing AFs for BO by extending FunSearch [124]. The discovered AFs are evaluated on various synthetic and HPO benchmarks in and out of the training distribution. 

, Vol. 1, No. 1, Article . Publication date: January 2025. 

Liu et al. 

18 

Table 2. An Overview of Optimization Applications Utilizing Language Models Across Various Domains and Task. 

|Application|Method|Role of LLM|Specific Problems or Tasks|
|---|---|---|---|
||EoH [90, 91]|LLMaD|TSP, Online BPP, FSSP|
||ReEvo [178]|LLMaD|TSP, CVRP, OP, MKP, BPP, DPP|
||OPRO [170]|LLMaO|TSP|
||LMEA [98]|Mixed|TSP|
|Combinatorial Optimization|MLLM [65]|Mixed|CVRP|
||FunSearch [124]|LLMaD|Cap Set Problem, Online BPP|
||MH-LLM* [126]|LLMaD|Social Networks Problem|
||SolSearch [129]|LLMaD|Satisfiability Problem|
||LMPSO [131]|LLMaO|TSP|
||LLM-NSGA [151]|LLMaD|Surgery Scheduling Problem|
||STRCMP [84]|LLMaD|MILP, SAT|
||EvoCut [175]|LLMaD|MILP|
||LLaMEA [146]|LLMaD|BBOB|
||EvoLLM [77]|LLMaO|BBOB, Neuroevolution|
||OPRO [170]|LLMaO|Linear Regression|
||LEO [11]|LLMaO|Numerical Benchmarks, Industrial Engineering Problems|
||LAEA [56]|LLMaP|Ellipsoid, Rosenbrock, Ackley, Griewank|
||MOEA/D-LMO [88]|LLMaO|Mulit-objective Synthetic Functions|
|Continuous Optimization|LLM-MOEA* [135]|LLMaE|Multi-objective Sustainable Infrastructure Planning Problem|
||CMOEA-LLM [159]|LLMaO|DAS-CMOP|
||HPO-LLM* [183]|LLMaO|HPOBench|
||LLAMBO [99]|Mixed|Bayesmark, HPOBench|
||BO-LIFT* [122]|LLMaD|Catalyst Optimization|
||EvolCAF [174]|LLMaD|Synthetic Functions, HPO|
||FunBO [1]|LLMaD|Synthetic Functions, HPO|
||LLM-SAEA [166]|LLMaP|Synthetic Functions|
||AwesomeDE [171]|LLMaO|Synthetic Functions|
||BBNM [79]|LLMaO|Wireless Networks|
||LLM4CMO [21]|LLMaO|Constrained Multiobjective Optimization|



# **5.2 Machine Learning Systems and Data Science** 

In this subsection, we investigate the applications of LLMs in the machine learning domain, focusing on their contribution to algorithmic design. These applications are summarized in Table 3. 

_5.2.1 Reinforcement Learning._ Reinforcement Learning (RL) has been the de facto standard for sequential decision-making tasks, and recently, the synergy between RL and LLMs has emerged as a novel trend in the domain. This convergence mirrors the dynamics of task planning, yet places RL at the core of its methodology. Many of the LLM4AD papers on RL is for automatically designing the reward functions [8, 104, 112]. In addition, Shah et al. [127] investigate the employment of LLMs for heuristic planning to steer the search process within RL frameworks. Zhang et al. [188] integrate LLMs into RL by introducing a Kullback-Leibler divergence regularization term that aligns LLM-driven policies with RL-derived policies. LLMs have also extended their reach to multi-agent RL scenarios, as shown by Du et al. [31], who illustrates their application within a Mixture-of-Experts system to direct RL models in the realm of intelligent network solutions. 

_5.2.2 Neural Architecture Search._ Neural Architecture Search (NAS), which is a significant focus within the AutoML community, has been investigated in many LLM4AD papers. For 

, Vol. 1, No. 1, Article . Publication date: January 2025. 

A Systematic Survey on Large Language Models for Algorithm Design 

19 

example, Chen et al. [15] have integrated LLMs with evolutionary search to successfully generate NAS code for diverse tasks. Nasir et al. [113] introduce a quality-diversity algorithm tailored to NAS, producing architectures for CIFAR-10 and NAS-bench-201 benchmarks. Moreover, Morris et al. [110] introduce guided evolution for the development of neural architectures and suggest the concept of the evolution of thought in algorithm design. Except for using LLM for design, Jawahar et al. [69] employ LLMs in predicting NAS performance, combining this approach with evolutionary search to effectively create novel network architectures. In contrast to the LLM-based architecture design and performance prediction, Zhou et al. [195] explore the adoption of LLMs for transferring design principles to narrow and guide the search space. 

_5.2.3 Prompt Tuning._ Prompt tuning aims to identify the most effective task prompt to enhance the performance of the LLM on a specific task dataset. Despite of requiring specialized training for each specific task, traditional discrete or continuous approaches [85] typically necessitate access to the logits or internal states of LLMs, which may not be applicable when the LLM can only be accessed through an API. To address these issues, recent works propose to model the optimization problem in natural language with LLMs as prompts. APE [196] utilizes the LLM as an inference model to generate instruction candidates directly based on a small set of demonstrations in the form of input-output pairs. This approach has demonstrated human-level performance on various tasks, including Instruction Induction [58] and Big-Bench Hard (BBH) [140]. OPRO [170] enables the LLM as an optimizer to gradually generate new prompts based on the full optimization trajectory, the optimizer prompt showcases significant improvement compared with human-designed prompts on BBH and GSM8K [23]. Inspired by the numerical gradient descent method, APO [120] conducts textual “gradient descent” by identifying the current prompts’ flaws and adjusting the prompt in the opposite semantic direction of the gradient. Similar practices are also found in the gradient-inspired LLM-based prompt optimizer named GPO [143], as well as the collaborative optimization approach [53] integrating a gradient-based optimizer and an LLMbased optimizer. Differently, Guo et al. [51] introduce a discrete prompt tuning framework named EvoPrompt that prompts LLM to act like evolutionary operators in generating new candidate prompts, harnessing the benefits of evolutionary algorithms that strike a good balance between exploration and exploitation. StrategyLLM [43] integrates four LLM-based agents—strategy generator, executor, optimizer, and evaluator—to collaboratively induce and deduce reasoning. This method generates more generalizable and consistent few-shot prompts than CoT prompting techniques. 

_5.2.4 Graph Learning._ Graph learning is another application with the advancing capabilities of LLMs in symbolic reasoning and graph processing. For example, Chen et al. [20] apply LLMs to the task of labeling in Text-Attributed Graphs (TAGs), capitalizing on the language task proficiency of LLMs. Both Mao et al. [107] and Chen et al. [18] adopt LLMs in an evolutionary framework for designing functions. The former evolves heuristic code functions to identify critical nodes in a graph while the latter identifies meta-structures within heterogeneous information networks to enhance their interpretability. Moreover, knowledge graphs have also seen substantial benefits from the application of LLMs. Zhang et al. [186] introduce AutoAlign, a method that employs LLMs to semantically align entities across different knowledge graphs, and Feng et al. [39] develop the knowledge search language to effectively conduct searches within knowledge graphs. 

, Vol. 1, No. 1, Article . Publication date: January 2025. 

Liu et al. 

20 

_5.2.5 Dataset Labeling._ LLMs have been used for mining semantic and multi-modal information from datasets. LLMs are employed to train interpretable classifiers to extract attributes from images [22] and to generate label functions for weakly supervised learning [48]. 

Table 3. An Overview of Machine Learning Applications Utilizing Language Models Across Various Domains and Tasks. 

|Application|Method|Role of LLM|Specific Problems or Tasks|
|---|---|---|---|
||LFG [127]|LLMaP|ObjectNav Tasks, Real-world Tasks|
||SLINVIT [188]|LLMaP|ALFWorld Tasks, InterCode Tasks, BlocksWorld Tasks|
|Reinforcement Learning|MEDIC [8]|LLMaP|BabyAI Tasks|
||Eureka [104]|LLMaD|IsaacGym Tasks, Bidexterous Manipulation Tasks|
||EROM [112]|LLMaD|IsaacGym Tasks|
||LLM-MOE [31]|LLMaP|Intelligent Networks|
||EvoPrompting [15]|LLMaD|MNIST Dataset, CLRS Algorithmic Reasoning|
|Neural Architecture Search|HS-NAS [69]|LLMaP|Machine Translation Tasks|
||LLMatic [113]|LLMaD|CIFAR-10 Dataset, NAS-bench-201 Benchmarks|
||LAPT [195]|LLMaD|NAS201, Trans101, DARTs|
||LLM-GE [110]|LLMaD|CIFAR-10 Dataset|
||APE [196]|LLMaO|Instruction Induction, BBH|
||OPRO [170]|LLMaO|GSM8K, BBH|
|Prompt Tuning|APO [120]|LLMaO|NLP Benchmark Classification Tasks|
||GPO [143]|LLMaO|Reasoning, Knowledge-intensive, NLP Tasks|
||MaaO [53]|LLMaO|NLU Tasks, Image Classification Tasks|
||EvoPrompt [51]|LLMaO|Language Understanding and Generation Tasks, BBH|
||StrategyLLM [43]|Mixed|Reasoning Tasks|
||LLM-Critical [107]|LLMaD|Critical Node Identification|
|GraphLearning|LLM-GNN [20]|LLMaP|Label-free Node Classification|
||ReStruct [18]|LLMaE|Meta-structure Discovery|
||AutoAlign [186]|LLMaE|Entity Type Inference|
||KSL [39]|LLMaP|Knowledge Search|
||AutoSGNN [109]|LLMaD|GNNs|
|DatasetLabeling|Inter-Classier [22]|LLMaO|iNaturalist Datasets, KikiBouba datasets|
||DataSculpt [48]|LLMaP|Label Function Design|
||LLM2FEA [161]|LLMaP|Objective-oriented Generation|
|Other Applications|tnGPS [180]|LLMaD|Tensor Network Structure Search|
||L-AutoDA [50]|LLMaD|Adversarial Attack|
||L-SFE [158]|LLMaD|Causal Structure Learning|



_5.2.6 Other Applications._ Other applications of LLMs extend to a myriad of machine learning tasks. Notably, Wong et al. [161] capitalize on multi-task learning and the iterative refinement of prompts to foster innovative design approaches. Zeng et al. [180] integrate LLMs with evolutionary search to develop a heuristic function aimed at efficiently sifting through candidate tensor sets representing the primal tensor network. Furthermore, Guo et al. [50] have blazed a trail in employing LLMs to generate novel decision-based adversarial attack algorithms, thus opening up a new diagram for the automatic assessment of model robustness. 

# **5.3 Scientific and Symbolic Domains** 

This subsection is dedicated to exploring LLM-based scientific discoveries. Rather than focusing on classic algorithm design, the works discussed here demonstrate how LLMs 

, Vol. 1, No. 1, Article . Publication date: January 2025. 

A Systematic Survey on Large Language Models for Algorithm Design 

21 

function as algorithmic engines to create search strategies, predict performance, and generate symbolic expressions to solve complex scientific problems. Table. 4 lists the related works in this domain. 

_5.3.1 Symbolic Regression._ In the realm of scientific discovery, LLMs are usually adopted for equation or functioin search. Notably, Du et al. [33] introduce LLM4ED, a framework that employs iterative strategies, including a black-box optimizer and evolutionary operators, to generate and optimize equations. This approach has shown significant advancements in stability and usability for uncovering physical laws from nonlinear dynamic systems. Similarly, Shojaee et al. [132] present LLM-SR, which combines LLMs’ extensive scientific knowledge and code generation capabilities with evolutionary search. This framework excels in proposing and refining initial equation structures based on physical understanding, outperforming traditional symbolic regression methods in discovering physically accurate equations across multiple scientific domains. A bilevel optimization framework, named SGA, is introduce by Ma et al. [102]. It merges the abstract reasoning capabilities of LLMs with the computational power of simulations. This integration facilitates hypothesis generation and discrete reasoning with simulations for experimental feedback and optimization of continuous variables, leading to improved performance. 

_5.3.2 Chemistry, Biology & Physics._ In the field of chemistry, LLMs can be applied not only to conventional molecular generation and design [9, 68], but also to specialized areas such as drug molecule design [176], chemical reaction prediction and optimization [123], and catalyst design [153], providing customized solutions. Furthermore, LLMs have also shown promising application prospects in materials discovery [70, 181], synthesis route planning [95], green chemistry [125], and other areas. These studies demonstrate the advantages of LLMs in molecular representation and optimization. 

In biology, LLMs are increasingly being used for tasks such as protein engineering [128], enzyme design [111], and biological sequence analysis [40]. By combining LLMs with vast amounts of biological data, they can more accurately predict interactions between biological molecules and significantly improve the efficiency of bioinformatics workflows. This has important implications for drug discovery and therapeutic protein design. The unique sequence generation and optimization capabilities of LLMs offer new possibilities for tackling combinatorial optimization challenges in biomacromolecular design. 

Although applications in physics are relatively fewer, some emerging work has demonstrated the broad prospects of LLMs. Pan et al. [118] use multi-step prompt templates to prove that LLMs can perform complex analytical calculations in theoretical physics. Quantum computing algorithm design, physics simulation optimization, and computational methods in condensed matter. 

_5.3.3 Mechanics._ MechAgents [114] introduces a class of physics-inspired generative machine learning platforms that utilize multiple LLMs to solve mechanics problems, such as elasticity, by autonomously collaborating to write, execute, and self-correct code using finite element methods. Moreover, Du et al. [32] adopt LLMs in automatically discovering governing equations from data, utilizing the models’ generation and reasoning capabilities to iteratively refine candidate equations. This approach, tested on various nonlinear systems including the Burgers, Chafee–Infante, and Navier–Stokes equations, demonstrates a superior ability to uncover correct physical laws and shows better generalization on unseen data compared to other models. AutoTurb [190], on the other hand, adopts LLMs in an evolutionary framework to automatically design and search for turbulence model in computational fluid dynamics. 

, Vol. 1, No. 1, Article . Publication date: January 2025. 

Liu et al. 

22 

Furthermore, Buehler [13] study LLM-based methods for forward and inverse mechanics problems, including bio-inspired hierarchical honeycomb design, carbon nanotube mechanics, and protein unfolding. 

Table 4. An Overview of Science Discovery Applications Utilizing Language Models Across Various Domains and Tasks. 

|Application|Method|Role of LLM|Specific Problems or Tasks|
|---|---|---|---|
|i|Bilevel [102]|LLMaD|Physical Scientific Discovery|
|General Scientific Equation Discovery|LLM-SR [132]|LLMaD|Scientific Equation Discovery|
||LLM4ED [33]|LLMaD|Equation Discovery|
||ChatChemTS [68]|LLMaD|Molecule Design|
||Debjyoti Bhattacharya, et al. [9]|LLMaO|Molecule Design|
|Chemical|Agustinus Kristiadi, et al. [76]|LLMaE|Molecule Design|
||BoChemian [123]|LLMaE|Chemical Reaction|
||Multi-modal MoLFormer [136]|LLMaP|Battery Electrolytes Formulation Design|
||CataLM [153]|LLMaP|Catalyst Design|
||Gavin Ye [176]|LLMaD|Drug Design|
||DrugAssist [177]|LLMaO|Drug Design|
||MLDE [144]|LLMaP|Protein Design|
|Biology|Prollama [101]|Mixed|Protein Design|
||X-LoRA [12]|LLMaP|Protein Design|
||CodonBERT [83]|LLMaP|mRNA Design and Optimization|
||Revisiting-PLMs [59]|LLMaP|Protein Function Prediction|
||MechAgents [114]|LLMaD|Mechanics Design|
|Mechanics|MeLM [13]|LLMaP, LLMaD|Carbon Nanotubes and Proteins Design|
||Mengge Du, et al. [32]|LLMaD|Nonlinear Dynamics Equation Discovery|
||AutoTurb [190]|LLMaD|Computational Fliud Dynamics|



# **6 Challenges and Future Directions** 

# **6.1 Scalability** 

A primary limitation of LLMs in algorithm design is their scalability. LLMs operate within a fixed context window, which restricts the amount of information they can process simultaneously. This constraint is particularly problematic for complex algorithmic tasks that involve detailed specifications or large inputs. Furthermore, even with an adequate context window, LLMs often struggle to accurately comprehend and reason over long sequences of information and generate a long solution [19]. 

While the growing capabilities of LLMs and advancements in reasoning models [49] have improved performance on tasks that can be mapped to their prior knowledge, this strength offers little advantage for novel algorithm design problems [96]. For instance, when used as optimizers, LLMs tend to perform well only on low-dimensional problems [170]. Similarly, in the LLMaD paradigm, LLMs are often limited to generating individual components or heuristic functions rather than a complete algorithm framework [91]. 

To mitigate these scalability challenges, some researchers have proposed hybrid methods. For example, Novikov et al. [116] introduce an approach that combines targeted code modifications using diff blocks with complete code regeneration, allowing for the evolution of more complex programs. Although related research has explored long-code generation [67], these efforts typically prioritize code correctness and general software engineering over the specific challenge of algorithmic scalability. 

, Vol. 1, No. 1, Article . Publication date: January 2025. 

A Systematic Survey on Large Language Models for Algorithm Design 

23 

# **6.2 Generalization** 

Another major challenge lies in generalization across different distributions and problem types. Existing methods often exhibit strong performance within their training distribution but fail to generalize to unseen instances [134]. Designing a single heuristic that performs optimally across diverse instance distributions is inherently difficult [130, 134]. For example, Sim et al. [134] reveal that algorithms designed on synthetic bin packing instances perform poorly on bin packing instances with real-world distributions. Similarly, Shi et al. [130] show that an algorithm designed for TSP instances with a fixed size can hardly generalize to TSP instances with other sizes. 

Several approaches aim to enhance cross-distribution generalization. Shi et al. [130] adopt a meta-learning framework that promotes adaptation across distributions. Zhang et al. [187] partition the overall problem class into subclasses based on instance features, enabling differentiated and automated heuristic design for each subclass. In contrast to designing a single optimal algorithm, EoH-S [89] proposes the concept of heuristic set design, which creates a portfolio of complementary algorithms to improve overall robustness across heterogeneous distributions. 

Beyond distribution generalization, cross-problem generalization presents an even greater challenge, particularly for LLM-driven algorithm design. The majority of existing works focus on developing algorithms for a specific target task, and the resulting algorithm can rarely be applied to solve other problems [91]. On the one hand, the algorithmic code implementation can not be used for solving other problems. On the other hand, the designed algorithm idea is either too high-level or problem-specific and thus lack cross-problem generalization. This contrasts with commonly used algorithmic frameworks, such as metaheuristic pipelines, which are often applicable to various problems despite differences in specific code implementations, as the core algorithmic idea remains the same [45]. While there has been some discussion on designing general metaheuristics [119], this work has remained at a high level without comprehensive evaluation. Consequently, cross-problem algorithm design is a promising and challenging direction for future research. 

# **6.3 Interpretability** 

Due to the black-box nature of LLMs, it is often difficult to trace how specific inputs influence the generated outputs. Moreover, we lack a deep understanding of the iterative algorithm design process itself [6, 88]. 

Recent studies have begun to address this challenge by analyzing the algorithmic landscape of LLM-driven design. For instance, Liu et al. [88] employ a simpler, interpretable model to approximate the behavior of LLMs when used as optimizers for multi-objective problems. To visualize the design process, van Stein et al. [147] propose Code Evolution Graphs (CEGs), which map the evolution of code using Abstract Syntax Tree (AST) features. Liu et al. [92] introduce a graph-based representation where nodes signify algorithms and edges denote their evolutionary relationships, enabling a structural analysis of the design space. A related and crucial research direction involves developing appropriate similarity metrics to quantify the relationships between generated algorithms, which remains an active area of investigation [92, 172]. 

Other work has focused on establishing a theoretical basis for these methods. Lee et al. [79] propose to interpret the LLMaO procedure as a finite-state Markov chain, providing a potential avenue for formal analysis. 

, Vol. 1, No. 1, Article . Publication date: January 2025. 

Liu et al. 

24 

# **6.4 Efficiency** 

Efficiency is another major challenge in applying LLMs to algorithm design, encompassing both efficient iterative algorithm search and evaluation reduction. 

While early methods relied on simple evolutionary search [91], more sophisticated strategies have been introduced to improve search efficiency. These include reflective reasoning [178], Monte Carlo Tree Search [194], and ensemble methods [116]. Recent attempts have also explored fine-tuning LLMs specifically for algorithm design, using both offline [93] and online [66, 139] approaches. For instance, Liu et al. [93] constructed diverse algorithm pairs and employed Direct Preference Optimization (DPO) to offline fine-tune a smaller model. This specialized model demonstrated higher inference speeds and achieved results competitive with much larger models. In an online setting, Huang et al. [66] utilized reinforcement learning to dynamically update the model during the algorithm search, leading to faster convergence and superior final algorithms within a fixed computational budget. However, these fine-tuned models are typically specialized for code generation on a single task. A key open question is how to accelerate the entire algorithm design process in a way that generalizes across diverse problem domains. 

Furthermore, real-world algorithm design often requires computationally expensive evaluations. This expense arises from two factors: the large number of test instances required for robust assessment and the time-consuming nature of each individual evaluation, which may involve complex simulations or searches. Recent work has attempted to reduce this evaluation cost by enabling the LLM to predict an algorithm’s quality and terminate unpromising evaluations early [69]. Despite these efforts, there remains a need for principled approaches that can effectively balance the trade-off between exploration efficiency and performance reliability. 

# **6.5 Benchmarking** 

Benchmarking is essential for ensuring fairness, reproducibility, and standardization across studies, facilitating both qualitative and quantitative comparisons. Despite rapid progress in LLM4AD, the field currently lacks standardized benchmarks for either algorithm design tasks or evaluation pipelines assessing LLM capabilities in this context. 

While related benchmarks have been developed for mathematical reasoning [86], planning [145], and classical algorithmic tasks [150], they do not fully capture the nuances of LLM-driven design. Recently, efforts have begun to develop benchmarks specifically for LLM-driven algorithm design. For example, Sun et al. [138] and Chen et al. [17] introduce benchmark suites focused on combinatorial optimization. van Stein et al. [148] developed a benchmark for designing metaheuristics for black-box optimization. Broadening the scope, Liu et al. [94] proposed a collection of tasks spanning diverse domains, from optimization and machine learning to scientific discovery. 

Despite this progress, establishing rigorous and widely accepted benchmarks with standard settings remains a significant challenge. The development of datasets, unified evaluation protocols, and transparent reporting practices is crucial. Such standards will not only enhance reproducibility but also catalyze innovation in this emerging research area. 

# **7 Conclusion** 

In this survey, we have provided a systematic review of the emerging field of algorithm design with large language models (LLM4AD). We categorized existing works into four paradigms based on the LLM’s primary role: LLM as Optimizer (LLMaO), LLM as Predictor (LLMaP), 

, Vol. 1, No. 1, Article . Publication date: January 2025. 

A Systematic Survey on Large Language Models for Algorithm Design 

25 

LLM as Extractor (LLMaE), and LLM as Designer (LLMaD). The LLMaO paradigm employs the LLM as a black-box optimizer to generate solutions, while LLMaP uses it as a surrogate model for prediction. LLMaE leverages the LLM to derive semantic features from unstructured data to inform an algorithm, and LLMaD directly generates algorithmic components or designs the entire algorithm. Furthermore, we have mapped works to the three core stages of the algorithm design, i.e., ideation, implementation, and evaluation, highlighting both progress and limitations. Finally, we summarized key application domains and identified critical open challenges, including scalability, generalization, interpretability, efficiency, and benchmarking, to help guide future research in this area. 

# **References** 

- [1] Virginia Aglietti, Ira Ktena, Jessica Schrouff, Eleni Sgouritsa, Francisco Ruiz, Alan Malek, Alexis Bellot, and Silvia Chiappa. 2025. FunBO: Discovering Acquisition Functions for Bayesian Optimization with FunSearch. In _Forty-second International Conference on Machine Learning_ . 

- [2] Ali AhmadiTeshnizi, Wenzhi Gao, and Madeleine Udell. 2024. OptiMUS: scalable optimization modeling with (MI) LP solvers and large language models. In _Proceedings of the 41st International Conference on Machine Learning_ . 577–596. 

- [3] Tasnim Ahmed and Salimur Choudhury. 2024. LM4OPT: Unveiling the potential of Large Language Models in formulating mathematical optimization problems. _INFOR: Information Systems and Operational Research_ (2024), 1–14. 

- [4] Janice Ahn, Rishu Verma, Renze Lou, Di Liu, Rui Zhang, and Wenpeng Yin. 2024. Large Language Models for Mathematical Reasoning: Progresses and Challenges. In _Proceedings of the 18th Conference of the European Chapter of the Association for Computational Linguistics: Student Research Workshop_ . 225–237. 

- [5] Mohammad Alipour-Vaezi and Kwok-Leung Tsui. 2024. Data-Driven Portfolio Management for Motion Pictures Industry: A New Data-Driven Optimization Methodology Using a Large Language Model as the Expert. _arXiv preprint arXiv:2404.07434_ (2024). 

- [6] Zeyuan Allen-Zhu and Yuanzhi Li. 2023. Physics of language models: Part 3.1, knowledge storage and extraction. _arXiv preprint arXiv:2309.14316_ (2023). 

- [7] Yoshua Bengio, Andrea Lodi, and Antoine Prouvost. 2021. Machine learning for combinatorial optimization: a methodological tour d’horizon. _European Journal of Operational Research_ 290, 2 (2021), 405–421. 

- [8] Siddhant Bhambri, Amrita Bhattacharjee, Subbarao Kambhampati, et al. 2024. Efficient reinforcement learning via large language model-based search. In _NeurIPS 2024 Workshop on Open-World Agents_ . 

- [9] Debjyoti Bhattacharya, Harrison J Cassady, Michael A Hickner, and Wesley F Reinhart. 2024. Large Language Models as Molecular Design Engines. _Journal of Chemical Information and Modeling_ (2024). 

- [10] Thomas Bömer, Nico Koltermann, Max Disselnmeyer, Laura Dörr, and Anne Meyer. 2025. Leveraging large language models to develop heuristics for emerging optimization problems. _arXiv preprint arXiv:2503.03350_ (2025). 

- [11] Shuvayan Brahmachary, Subodh M Joshi, Aniruddha Panda, Kaushik Koneripalli, Arun Kumar Sagotra, Harshil Patel, Ankush Sharma, Ameya D Jagtap, and Kaushic Kalyanaraman. 2025. Large language model-based evolutionary optimizer: Reasoning with elitism. _Neurocomputing_ 622 (2025), 129272. 

- [12] Eric L Buehler and Markus J Buehler. 2024. X-LoRA: Mixture of low-rank adapter experts, a flexible framework for large language models with applications in protein mechanics and molecular design. _APL Machine Learning_ 2, 2 (2024). 

- [13] Markus J Buehler. 2023. MeLM, a generative pretrained language modeling framework that solves forward and inverse mechanics problems. _Journal of the Mechanics and Physics of Solids_ 181 (2023), 105454. 

- [14] Camilo Chacón Sartori, Christian Blum, and Gabriela Ochoa. 2024. Large Language Models for the Automated Analysis of Optimization Algorithms. In _Proceedings of the Genetic and Evolutionary Computation Conference_ . 160–168. 

- [15] Angelica Chen, David Dohan, and David So. 2024. EvoPrompting: language models for code-level neural architecture search. _Advances in Neural Information Processing Systems_ 36 (2024). 

, Vol. 1, No. 1, Article . Publication date: January 2025. 

Liu et al. 

26 

- [16] Chentong Chen, Mengyuan Zhong, Jianyong Sun, Ye Fan, and Jialong Shi. 2025. HiFo-Prompt: Prompting with Hindsight and Foresight for LLM-based Automatic Heuristic Design. _arXiv preprint arXiv:2508.13333_ (2025). 

- [17] Hongzheng Chen, Yingheng Wang, Yaohui Cai, Hins Hu, Jiajie Li, Shirley Huang, Chenhui Deng, Rongjian Liang, Shufeng Kong, Haoxing Ren, et al. 2025. HeuriGym: An Agentic Benchmark for LLM-Crafted Heuristics in Combinatorial Optimization. _arXiv preprint arXiv:2506.07972_ (2025). 

- [18] Lin Chen, Fengli Xu, Nian Li, Zhenyu Han, Meng Wang, Yong Li, and Pan Hui. 2024. Large Language Model-driven Meta-structure Discovery in Heterogeneous Information Network. In _Proceedings of the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining, KDD_ . ACM. 

- [19] Yanxi Chen, Yaliang Li, Bolin Ding, and Jingren Zhou. 2024. On the design and analysis of llm-based algorithms. _arXiv preprint arXiv:2407.14788_ (2024). 

- [20] Zhikai Chen, Haitao Mao, Hongzhi Wen, Haoyu Han, Wei Jin, Haiyang Zhang, Hui Liu, and Jiliang Tang. 2024. Label-free Node Classification on Graphs with Large Language Models (LLMs). In _The Twelfth International Conference on Learning Representations_ . 

- [21] Zhen-Song Chen, Hong-Wei Ding, Xian-Jia Wang, and Witold Pedrycz. 2025. LLM4CMO: Large Language Model-aided Algorithm Design for Constrained Multiobjective Optimization. _arXiv preprint arXiv:2508.11871_ (2025). 

- [22] Mia Chiquier, Utkarsh Mall, and Carl Vondrick. 2024. Evolving interpretable visual classifiers with large language models. In _European Conference on Computer Vision_ . Springer, 183–201. 

- [23] Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias Plappert, Jerry Tworek, Jacob Hilton, Reiichiro Nakano, et al. 2021. Training verifiers to solve math word problems. _arXiv preprint arXiv:2110.14168_ (2021). 

- [24] Thomas H Cormen, Charles E Leiserson, Ronald L Rivest, and Clifford Stein. 2022. _Introduction to algorithms_ . MIT press. 

- [25] Leonardo Lucio Custode, Fabio Caraffini, Anil Yaman, and Giovanni Iacca. 2024. An investigation on the use of Large Language Models for hyperparameter tuning in Evolutionary Algorithms. In _Proceedings of the Genetic and Evolutionary Computation Conference Companion_ . 1838–1845. 

- [26] Francesca Da Ros, Michael Soprano, Luca Di Gaspero, and Kevin Roitero. 2025. Large language models for combinatorial optimization: A systematic review. _arXiv preprint arXiv:2507.03637_ (2025). 

- [27] Giordano d’Aloisio, Sophie Fortz, Carol Hanna, Daniel Fortunato, Avner Bensoussan, Eñaut Mendiluze Usandizaga, and Federica Sarro. 2024. Exploring LLM-driven explanations for quantum algorithms. In _Proceedings of the 18th ACM/IEEE International Symposium on Empirical Software Engineering and Measurement_ . 475–481. 

- [28] Pham Vu Tuan Dat, Long Doan, and Huynh Thi Thanh Binh. 2025. Hsevo: Elevating automatic heuristic design with diversity-driven harmony search and genetic algorithm using llms. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , Vol. 39. 26931–26938. 

- [29] Jacob de Nobel, Furong Ye, Diederick Vermetten, Hao Wang, Carola Doerr, and Thomas Bäck. 2024. Iohexperimenter: Benchmarking platform for iterative optimization heuristics. _Evolutionary Computation_ (2024), 1–6. 

- [30] Tuan Dinh, Yuchen Zeng, Ruisu Zhang, Ziqian Lin, Michael Gira, Shashank Rajput, Jy-yong Sohn, Dimitris Papailiopoulos, and Kangwook Lee. 2022. Lift: Language-interfaced fine-tuning for nonlanguage machine learning tasks. _Advances in Neural Information Processing Systems_ 35 (2022), 11763–11784. 

- [31] Hongyang Du, Guangyuan Liu, Yijing Lin, Dusit Niyato, Jiawen Kang, Zehui Xiong, and Dong In Kim. 2024. Mixture of Experts for Network Optimization: A Large Language Model-enabled Approach. _arXiv preprint arXiv:2402.09756_ (2024). 

- [32] Mengge Du, Yuntian Chen, Zhongzheng Wang, Longfeng Nie, and Dongxiao Zhang. 2024. Large language models for automatic equation discovery of nonlinear dynamics. _Physics of Fluids_ 36, 9 (2024). 

- [33] Mengge Du, Yuntian Chen, Zhongzheng Wang, Longfeng Nie, and Dongxiao Zhang. 2024. LLM4ED: Large Language Models for Automatic Equation Discovery. _arXiv preprint arXiv:2405.07761_ (2024). 

- [34] Ruibo Duan, Yuxin Liu, Xinyao Dong, and Chenglin Fan. 2025. EALG: Evolutionary Adversarial Generation of Language Model-Guided Generators for Combinatorial Optimization. _arXiv preprint arXiv:2506.02594_ (2025). 

- [35] Naoki Egami, Musashi Hinck, Brandon Stewart, and Hanying Wei. 2024. Using imperfect surrogates for downstream inference: Design-based supervised learning for social science applications of large language models. _Advances in Neural Information Processing Systems_ 36 (2024). 

, Vol. 1, No. 1, Article . Publication date: January 2025. 

A Systematic Survey on Large Language Models for Algorithm Design 

27 

- [36] Katharina Eggensperger, Philipp Müller, Neeratyoy Mallik, Matthias Feurer, Rene Sass, Aaron Klein, Noor Awad, Marius Lindauer, and Frank Hutter. 2021. HPOBench: A Collection of Reproducible Multi-Fidelity Benchmark Problems for HPO. In _Thirty-fifth Conference on Neural Information Processing Systems Datasets and Benchmarks Track (Round 2)_ . 

- [37] Zhenan Fan, Bissan Ghaddar, Xinglu Wang, Linzi Xing, Yong Zhang, and Zirui Zhou. 2024. Artificial intelligence for operations research: Revolutionizing the operations research process. _arXiv preprint arXiv:2401.03244_ (2024). 

- [38] Zhun Fan, Wenji Li, Xinye Cai, Hui Li, Caimin Wei, Qingfu Zhang, Kalyanmoy Deb, and Erik Goodman. 2020. Difficulty adjustable and scalable constrained multiobjective test problem toolkit. _Evolutionary computation_ 28, 3 (2020), 339–378. 

- [39] Chao Feng, Xinyu Zhang, and Zichu Fei. 2023. Knowledge solver: Teaching llms to search for domain knowledge from knowledge graphs. _arXiv preprint arXiv:2309.03118_ (2023). 

- [40] Ruijun Feng, Chi Zhang, and Yang Zhang. 2024. Large language models for biomolecular analysis: From methods to applications. _TrAC Trends in Analytical Chemistry_ (2024), 117540. 

- [41] Mohamed Amine Ferrag, Norbert Tihanyi, and Merouane Debbah. 2025. From llm reasoning to autonomous ai agents: A comprehensive review. _arXiv preprint arXiv:2504.19678_ (2025). 

- [42] Peter I Frazier and Jialei Wang. 2016. Bayesian optimization for materials design. _Information science for materials discovery and design_ (2016), 45–75. 

- [43] Chang Gao, Haiyun Jiang, Deng Cai, Shuming Shi, and Wai Lam. 2024. Strategyllm: Large language models as strategy generators, executors, optimizers, and evaluators for problem solving. _Advances in Neural Information Processing Systems_ 37 (2024), 96797–96846. 

- [44] Yuanyuan Ge, Likang Wu, Haipeng Yang, Fan Cheng, Hongke Zhao, and Lei Zhang. 2025. MORA-LLM: Enhancing Multi-Objective Optimization Recommendation Algorithm by Integrating Large Language Models. _IEEE Transactions on Evolutionary Computation_ (2025). 

- [45] Michel Gendreau, Jean-Yves Potvin, et al. 2010. _Handbook of metaheuristics_ . Vol. 2. Springer. 

- [46] Karan Girotra, Lennart Meincke, Christian Terwiesch, and Karl T Ulrich. 2023. Ideas are dimes a dozen: Large language models for idea generation in innovation. _Available at SSRN 4526071_ (2023). 

- [47] Fred W Glover and Gary A Kochenberger. 2006. _Handbook of metaheuristics_ . Vol. 57. Springer Science & Business Media. 

- [48] Naiqing Guan, Kaiwen Chen, and Nick Koudas. 2023. Can large language models design accurate label functions? _arXiv preprint arXiv:2311.00739_ (2023). 

- [49] Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Ruoyu Zhang, Runxin Xu, Qihao Zhu, Shirong Ma, Peiyi Wang, Xiao Bi, et al. 2025. Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning. _arXiv preprint arXiv:2501.12948_ (2025). 

- [50] Ping Guo, Fei Liu, Xi Lin, Qingchuan Zhao, and Qingfu Zhang. 2024. L-autoda: Large language models for automatically evolving decision-based adversarial attacks. In _Proceedings of the Genetic and Evolutionary Computation Conference Companion_ . 1846–1854. 

- [51] Qingyan Guo, Rui Wang, Junliang Guo, Bei Li, Kaitao Song, Xu Tan, Guoqing Liu, Jiang Bian, and Yujiu Yang. 2024. Connecting Large Language Models with Evolutionary Algorithms Yields Powerful Prompt Optimizers. In _The Twelfth International Conference on Learning Representations_ . 

- [52] Taicheng Guo, Xiuying Chen, Yaqi Wang, Ruidi Chang, Shichao Pei, Nitesh V Chawla, Olaf Wiest, and Xiangliang Zhang. 2024. Large language model based multi-agents: a survey of progress and challenges. In _Proceedings of the Thirty-Third International Joint Conference on Artificial Intelligence_ . 8048–8057. 

- [53] Zixian Guo, Ming Liu, Zhilong Ji, Jinfeng Bai, Yiwen Guo, and Wangmeng Zuo. 2024. Two Optimizers Are Better Than One: LLM Catalyst for Enhancing Gradient-Based Optimization. _arXiv preprint arXiv:2405.19732_ (2024). 

- [54] Can Gurkan, Narasimha Karthik Jwalapuram, Kevin Wang, Rudy Danda, Leif Rasmussen, John Chen, and Uri Wilensky. 2025. LEAR: LLM-Driven Evolution of Agent-Based Rules. In _Proceedings of the Genetic and Evolutionary Computation Conference Companion_ . 2309–2326. 

- [55] Nikolaus Hansen and Raymond Ros. 2010. Black-box optimization benchmarking of NEWUOA compared to BIPOP-CMA-ES: on the BBOB noiseless testbed. In _Proceedings of the 12th annual conference companion on Genetic and evolutionary computation_ . 1519–1526. 

- [56] Hao Hao, Xiaoqun Zhang, and Aimin Zhou. 2024. Large language models as surrogate models in evolutionary algorithms: A preliminary study. _Swarm and Evolutionary Computation_ 91 (2024), 101741. 

, Vol. 1, No. 1, Article . Publication date: January 2025. 

Liu et al. 

28 

- [57] Erik Hemberg, Stephen Moskal, and Una-May O’Reilly. 2024. Evolving code with a large language model. _Genetic Programming and Evolvable Machines_ 25, 2 (2024), 21. 

- [58] Or Honovich, Uri Shaham, Samuel Bowman, and Omer Levy. 2023. Instruction Induction: From Few Examples to Natural Language Task Descriptions. In _Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_ . 1935–1952. 

- [59] Mingyang Hu, Fajie Yuan, Kevin Yang, Fusong Ju, Jin Su, Hui Wang, Fei Yang, and Qiuyang Ding. 2022. Exploring evolution-aware &-free protein language models as protein function predictors. _Advances in Neural Information Processing Systems_ 35 (2022), 38873–38884. 

- [60] Qinglong Hu, Xialiang Tong, Mingxuan Yuan, Fei Liu, Zhichao Lu, and Qingfu Zhang. 2025. Discovering Interpretable Programmatic Policies via Multimodal LLM-assisted Evolutionary Search. _arXiv preprint arXiv:2508.05433_ (2025). 

- [61] Qinglong Hu and Qingfu Zhang. 2025. Partition to Evolve: Niching-enhanced Evolution with LLMs for Automated Algorithm Discovery. In _The Thirty-ninth Annual Conference on Neural Information Processing Systems_ . 

- [62] Shengran Hu, Cong Lu, and Jeff Clune. 2025. Automated Design of Agentic Systems. In _The Thirteenth International Conference on Learning Representations_ . 

- [63] Chenyu Huang, Zhengyang Tang, Shixi Hu, Ruoqing Jiang, Xin Zheng, Dongdong Ge, Benyou Wang, and Zizhuo Wang. 2025. Orlm: A customizable framework in training large models for automated optimization modeling. _Operations Research_ (2025). 

- [64] Sen Huang, Kaixiang Yang, Sheng Qi, and Rui Wang. 2024. When large language model meets optimization. _Swarm and Evolutionary Computation_ 90 (2024), 101663. 

- [65] Yuxiao Huang, Wenjie Zhang, Liang Feng, Xingyu Wu, and Kay Chen Tan. 2025. How multimodal integration boost the performance of llm for optimization: Case study on capacitated vehicle routing problems. In _2025 IEEE Symposium for Multidisciplinary Computational Intelligence Incubators (MCII)_ . IEEE, 1–7. 

- [66] Ziyao Huang, Weiwei Wu, Kui Wu, Jianping Wang, and Wei-Bin Lee. 2025. Calm: Co-evolution of algorithms and language model for automatic heuristic design. _arXiv preprint arXiv:2505.12285_ (2025). 

- [67] Yoichi Ishibashi and Yoshimasa Nishimura. 2024. Self-Organized Agents: A LLM Multi-Agent Framework toward Ultra Large-Scale Code Generation and Optimization. _CoRR_ (2024). 

- [68] Shoichi Ishida, Tomohiro Sato, Teruki Honma, and Kei Terayama. 2025. Large language models open new way of AI-assisted molecule design for chemists. _Journal of Cheminformatics_ 17, 1 (2025), 36. 

- [69] Ganesh Jawahar, Muhammad Abdul-Mageed, Laks VS Lakshmanan, and Dujian Ding. 2024. LLM Performance Predictors are good initializers for Architecture Search. In _ACL (Findings)_ . 

- [70] Shuyi Jia, Chao Zhang, and Victor Fung. 2024. LLMatDesign: Autonomous Materials Discovery with Large Language Models. _arXiv preprint arXiv:2406.13163_ (2024). 

- [71] Juyong Jiang, Fan Wang, Jiasi Shen, Sungju Kim, and Sunghun Kim. 2024. A Survey on Large Language Models for Code Generation. _arXiv preprint arXiv:2406.00515_ (2024). 

- [72] Xia Jiang, Yaoxin Wu, Yuan Wang, and Yingqian Zhang. 2024. Bridging Large Language Models and Optimization: A Unified Framework for Text-attributed Combinatorial Optimization. _arXiv preprint arXiv:2408.12214_ (2024). 

- [73] Yaochu Jin, Handing Wang, Tinkle Chugh, Dan Guo, and Kaisa Miettinen. 2018. Data-driven evolutionary optimization: An overview and case studies. _IEEE Transactions on Evolutionary Computation_ 23, 3 (2018), 442–458. 

- [74] Sathvik Joel, Jie Wu, and Fatemeh Fard. 2024. A survey on llm-based code generation for lowresource and domain-specific programming languages. _ACM Transactions on Software Engineering and Methodology_ (2024). 

- [75] J Kleinberg. 2006. _Algorithm Design_ . Vol. 92. Pearson Education. 

- [76] Agustinus Kristiadi, Felix Strieth-Kalthoff, Marta Skreta, Pascal Poupart, Alan Aspuru-Guzik, and Geoff Pleiss. 2024. A Sober Look at LLMs for Material Discovery: Are They Actually Good for Bayesian Optimization Over Molecules?. In _Forty-first International Conference on Machine Learning_ . 

- [77] Robert Lange, Yingtao Tian, and Yujin Tang. 2024. Large language models as evolution strategies. In _Proceedings of the Genetic and Evolutionary Computation Conference Companion_ . 579–582. 

- [78] Gilbert Laporte. 1992. The traveling salesman problem: An overview of exact and approximate algorithms. _European Journal of Operational Research_ 59, 2 (1992), 231–247. 

- [79] Hoon Lee, Wentao Zhou, Merouane Debbah, and Inkyu Lee. 2025. On the Convergence of Large Language Model Optimizer for Black-Box Network Management. _arXiv preprint arXiv:2507.02689_ 

, Vol. 1, No. 1, Article . Publication date: January 2025. 

A Systematic Survey on Large Language Models for Algorithm Design 

29 

(2025). 

- [80] Hao Li, Xue Yang, Zhaokai Wang, Xizhou Zhu, Jie Zhou, Yu Qiao, Xiaogang Wang, Hongsheng Li, Lewei Lu, and Jifeng Dai. 2024. Auto mc-reward: Automated dense reward design with large language models for minecraft. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ . 16426–16435. 

- [81] Kefan Li, Yuan Yuan, Hongyue Yu, Tingyu Guo, and Shijie Cao. 2025. CoCoEvo: Co-Evolution of Programs and Test Cases to Enhance Code Generation. _IEEE Transactions on Evolutionary Computation_ (2025). 

- [82] Rui Li, Ling Wang, Hongyan Sang, Lizhong Yao, and Lijun Pan. 2025. LLM-Assisted Automatic Memetic Algorithm for Lot-Streaming Hybrid Job Shop Scheduling With Variable Sublots. _IEEE Transactions on Evolutionary Computation_ (2025). 

- [83] Sizhen Li, Saeed Moayedpour, Ruijiang Li, Michael Bailey, Saleh Riahi, Milad Miladi, Jacob Miner, Dinghai Zheng, Jun Wang, Akshay Balsubramani, Khang Tran, Minnie, Monica Wu, Xiaobo Gu, Ryan Clinton, Carla Asquith, Joseph Skaleski, Lianne Boeglin, Sudha Chivukula, Anusha Dias, Fernando Ulloa Montoya, Vikram Agarwal, Ziv Bar-Joseph, and Sven Jager. 2023. CodonBERT: Large Language Models for mRNA design and optimization. In _NeurIPS 2023 Generative AI and Biology (GenBio) Workshop_ . 

- [84] Xijun Li, Jiexiang Yang, Jinghao Wang, Bo Peng, Jianguo Yao, and Haibing Guan. 2025. STRCMP: Integrating Graph Structural Priors with Language Models for Combinatorial Optimization. _arXiv preprint arXiv:2506.11057_ (2025). 

- [85] Xiang Lisa Li and Percy Liang. 2021. Prefix-Tuning: Optimizing Continuous Prompts for Generation. In _Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing (Volume 1: Long Papers)_ . 4582–4597. 

- [86] Xiaohan Lin, Qingxing Cao, Yinya Huang, Zhicheng Yang, Zhengying Liu, Zhenguo Li, and Xiaodan Liang. 2024. ATG: Benchmarking Automated Theorem Generation for Generative Language Models. In _Findings of the Association for Computational Linguistics: NAACL 2024_ . 4465–4480. 

- [87] Hongyi Ling, Shubham Parashar, Sambhav Khurana, Blake Olson, Anwesha Basu, Gaurangi Sinha, Zhengzhong Tu, James Caverlee, and Shuiwang Ji. 2025. Complex LLM planning via automated heuristics discovery. _arXiv preprint arXiv:2502.19295_ (2025). 

- [88] Fei Liu, Xi Lin, Shunyu Yao, Zhenkun Wang, Xialiang Tong, Mingxuan Yuan, and Qingfu Zhang. 2025. Large language model for multiobjective evolutionary optimization. In _International Conference on Evolutionary Multi-Criterion Optimization_ . Springer, 178–191. 

- [89] Fei Liu, Yilu Liu, Qingfu Zhang, Xialiang Tong, and Mingxuan Yuan. 2026. EoH-S: Evolution of heuristic set using llms for automated heuristic design. _Proceedings of the AAAI Conference on Artificial Intelligence_ (2026). 

- [90] Fei Liu, Xialiang Tong, Mingxuan Yuan, and Qingfu Zhang. 2023. Algorithm evolution using large language model. _arXiv preprint arXiv:2311.15249_ (2023). 

- [91] Fei Liu, Tong Xialiang, Mingxuan Yuan, Xi Lin, Fu Luo, Zhenkun Wang, Zhichao Lu, and Qingfu Zhang. 2024. Evolution of Heuristics: Towards Efficient Automatic Algorithm Design Using Large Language Model. In _Forty-first International Conference on Machine Learning_ . 

- [92] Fei Liu, Qingfu Zhang, Jialong Shi, Xialiang Tong, Kun Mao, and Mingxuan Yuan. 2025. Fitness landscape of large language model-assisted automated algorithm search. _arXiv preprint arXiv:2504.19636_ (2025). 

- [93] Fei Liu, Rui Zhang, Xi Lin, Zhichao Lu, and Qingfu Zhang. 2025. Fine-tuning large language model for automated algorithm design. _arXiv preprint arXiv:2507.10614_ (2025). 

- [94] Fei Liu, Rui Zhang, Zhuoliang Xie, Rui Sun, Kai Li, Xi Lin, Zhenkun Wang, Zhichao Lu, and Qingfu Zhang. 2024. Llm4ad: A platform for algorithm design with large language model. _arXiv preprint arXiv:2412.17287_ (2024). 

- [95] Gang Liu, Michael Sun, Wojciech Matusik, Meng Jiang, and Jie Chen. 2025. Multimodal Large Language Models for Inverse Molecular Design with Retrosynthetic Planning. In _The Thirteenth International Conference on Learning Representations_ . 

- [96] Jiayuan Liu, Mingyu Guo, and Vincent Conitzer. 2025. An Interpretable Automated Mechanism Design Framework with Large Language Models. _arXiv preprint arXiv:2502.12203_ (2025). 

- [97] Jiao Liu, Zhu Sun, Shanshan Feng, Caishun Chen, and Yew-Soon Ong. 2025. Language model evolutionary algorithms for recommender systems: Benchmarks and algorithm comparisons. _IEEE Transactions on Evolutionary Computation_ (2025). 

, Vol. 1, No. 1, Article . Publication date: January 2025. 

Liu et al. 

30 

- [98] Shengcai Liu, Caishun Chen, Xinghua Qu, Ke Tang, and Yew-Soon Ong. 2024. Large language models as evolutionary optimizers. In _2024 IEEE Congress on Evolutionary Computation (CEC)_ . IEEE, 1–8. 

- [99] Tennison Liu, Nicolás Astorga, Nabeel Seedat, and Mihaela van der Schaar. 2024. Large Language Models to Enhance Bayesian Optimization. In _The Twelfth International Conference on Learning Representations_ . 

- [100] Zhiwei Liu, Weiran Yao, Jianguo Zhang, Liangwei Yang, Zuxin Liu, Juntao Tan, Prafulla K Choubey, Tian Lan, Jason Wu, Huan Wang, et al. 2024. AgentLite: A Lightweight Library for Building and Advancing Task-Oriented LLM Agent System. _arXiv preprint arXiv:2402.15538_ (2024). 

- [101] Liuzhenghao Lv, Zongying Lin, Hao Li, Yuyang Liu, Jiaxi Cui, Calvin Yu-Chian Chen, Li Yuan, and Yonghong Tian. 2025. Prollama: A protein large language model for multi-task protein language processing. _IEEE Transactions on Artificial Intelligence_ (2025). 

- [102] Pingchuan Ma, Tsun-Hsuan Wang, Minghao Guo, Zhiqing Sun, Joshua B. Tenenbaum, Daniela Rus, Chuang Gan, and Wojciech Matusik. 2024. LLM and Simulation as Bilevel Optimizers: A New Paradigm to Advance Physical Scientific Discovery. In _Forty-first International Conference on Machine Learning_ . 

- [103] Ruotian Ma, Xiaolei Wang, Xin Zhou, Jian Li, Nan Du, Tao Gui, Qi Zhang, and Xuanjing Huang. 2024. Are Large Language Models Good Prompt Optimizers? _arXiv preprint arXiv:2402.02101_ (2024). 

- [104] Yecheng Jason Ma, William Liang, Guanzhi Wang, De-An Huang, Osbert Bastani, Dinesh Jayaraman, Yuke Zhu, Linxi Fan, and Anima Anandkumar. 2024. Eureka: Human-Level Reward Design via Coding Large Language Models. In _The Twelfth International Conference on Learning Representations_ . 

- [105] Zeyuan Ma, Hongshu Guo, Jiacheng Chen, Guojun Peng, Zhiguang Cao, Yining Ma, and Yue-Jiao Gong. 2024. LLaMoCo: Instruction Tuning of Large Language Models for Optimization Code Generation. _arXiv preprint arXiv:2403.01131_ (2024). 

- [106] Zeyuan Ma, Hongshu Guo, Yue-Jiao Gong, Jun Zhang, and Kay Chen Tan. 2025. Toward automated algorithm design: A survey and practical guide to meta-black-box-optimization. _IEEE Transactions on Evolutionary Computation_ (2025). 

- [107] Jinzhu Mao, Dongyun Zou, Li Sheng, Siyi Liu, Chen Gao, Yue Wang, and Yong Li. 2024. Identify Critical Nodes in Complex Network with Large Language Models. (2024). 

- [108] Abdulkadir Memduhoğlu, Nir Fulman, and Alexander Zipf. 2024. Enriching building function classification using Large Language Model embeddings of OpenStreetMap Tags. _Earth Science Informatics_ (2024), 1–16. 

- [109] Shibing Mo, Kai Wu, Qixuan Gao, Xiangyi Teng, and Jing Liu. 2025. AutoSGNN: automatic propagation mechanism discovery for spectral graph neural networks. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , Vol. 39. 19493–19502. 

- [110] Clint Morris, Michael Jurado, and Jason Zutty. 2024. Llm guided evolution-the automation of models advancing models. In _Proceedings of the Genetic and Evolutionary Computation Conference_ . 377–384. 

- [111] Yves Gaetan Nana Teukam, Federico Zipoli, Teodoro Laino, Emanuele Criscuolo, Francesca Grisoni, and Matteo Manica. 2025. Integrating genetic algorithms and language models for enhanced enzyme design. _Briefings in bioinformatics_ 26, 1 (2025), bbae675. 

- [112] Ali Narin. 2024. Evolutionary Reward Design and Optimization with Multimodal Large Language Models. In _Proceedings of the 3rd Workshop on Advances in Language and Vision Research (ALVR)_ . 202–208. 

- [113] Muhammad Umair Nasir, Sam Earle, Julian Togelius, Steven James, and Christopher Cleghorn. 2024. Llmatic: neural architecture search via large language models and quality diversity optimization. In _proceedings of the Genetic and Evolutionary Computation Conference_ . 1110–1118. 

- [114] Bo Ni and Markus J Buehler. 2024. MechAgents: Large language model multi-agent collaborations can solve mechanics problems, generate new data, and integrate knowledge. _Extreme Mechanics Letters_ 67 (2024), 102131. 

- [115] Allen Nie, Ching-An Cheng, Andrey Kolobov, and Adith Swaminathan. 2024. The importance of directional feedback for llm-based optimizers. _arXiv preprint arXiv:2405.16434_ (2024). 

- [116] Alexander Novikov, Ngân V˜u, Marvin Eisenberger, Emilien Dupont, Po-Sen Huang, Adam Zsolt Wagner, Sergey Shirobokov, Borislav Kozlovskii, Francisco JR Ruiz, Abbas Mehrabian, et al. 2025. AlphaEvolve: A coding agent for scientific and algorithmic discovery. _arXiv preprint arXiv:2506.13131_ (2025). 

- [117] Vishal Pallagani, Bharath Chandra Muppasani, Kaushik Roy, Francesco Fabiano, Andrea Loreggia, Keerthiram Murugesan, Biplav Srivastava, Francesca Rossi, Lior Horesh, and Amit Sheth. 2024. On the prospects of incorporating large language models (llms) in automated planning and scheduling 

, Vol. 1, No. 1, Article . Publication date: January 2025. 

A Systematic Survey on Large Language Models for Algorithm Design 

31 

- (aps). In _Proceedings of the International Conference on Automated Planning and Scheduling_ , Vol. 34. 432–444. 

- [118] Haining Pan, Nayantara Mudur, William Taranto, Maria Tikhanovskaya, Subhashini Venugopalan, Yasaman Bahri, Michael P Brenner, and Eun-Ah Kim. 2025. Quantum many-body physics calculations with large language models. _Communications Physics_ 8, 1 (2025), 49. 

- [119] Michal Pluhacek, Anezka Kazikova, Tomas Kadavy, Adam Viktorin, and Roman Senkerik. 2023. Leveraging Large Language Models for the Generation of Novel Metaheuristic Optimization Algorithms. In _Proceedings of the Companion Conference on Genetic and Evolutionary Computation_ . 1812–1820. 

- [120] Reid Pryzant, Dan Iter, Jerry Li, Yin Tat Lee, Chenguang Zhu, and Michael Zeng. 2023. Automatic Prompt Optimization with ”Gradient Descent” and Beam Search. In _The 2023 Conference on Empirical Methods in Natural Language Processing_ . 

- [121] Rindranirina Ramamonjison, Timothy Yu, Raymond Li, Haley Li, Giuseppe Carenini, Bissan Ghaddar, Shiqi He, Mahdi Mostajabdaveh, Amin Banitalebi-Dehkordi, Zirui Zhou, et al. 2023. Nl4opt competition: Formulating optimization problems based on their natural language descriptions. In _NeurIPS 2022 Competition Track_ . PMLR, 189–203. 

- [122] Mayk Caldas Ramos, Shane S Michtavy, Marc D Porosoff, and Andrew D White. 2023. Bayesian optimization of catalysts with in-context learning. _arXiv preprint arXiv:2304.05341_ (2023). 

- [123] Bojana Ranković and Philippe Schwaller. 2023. BoChemian: Large language model embeddings for Bayesian optimization of chemical reactions. In _NeurIPS 2023 Workshop on Adaptive Experimental Design and Active Learning in the Real World_ . 

- [124] Bernardino Romera-Paredes, Mohammadamin Barekatain, Alexander Novikov, Matej Balog, M Pawan Kumar, Emilien Dupont, Francisco JR Ruiz, Jordan S Ellenberg, Pengming Wang, Omar Fawzi, et al. 2024. Mathematical discoveries from program search with large language models. _Nature_ 625, 7995 (2024), 468–475. 

- [125] Emily F Ruff, Jeanne L Franz, and Joseph K West. 2024. Using ChatGPT for Method Development and Green Chemistry Education in Upper-Level Laboratory Courses. _Journal of Chemical Education_ 101, 8 (2024), 3224–3232. 

- [126] Camilo Chacón Sartori, Christian Blum, Filippo Bistaffa, and Guillem Rodríguez Corominas. 2024. Metaheuristics and large language models join forces: Towards an integrated optimization approach. _IEEE Access_ (2024). 

- [127] Dhruv Shah, Michael Robert Equi, Błażej Osiński, Fei Xia, Brian Ichter, and Sergey Levine. 2023. Navigation with large language models: Semantic guesswork as a heuristic for planning. In _Conference on Robot Learning_ . PMLR, 2683–2699. 

- [128] Yiqing Shen, Zan Chen, Michail Mamalakis, Yungeng Liu, Tianbin Li, Yanzhou Su, Junjun He, Pietro Liò, and Yu Guang Wang. 2024. Toursynbio: A multi-modal large model and agent framework to bridge text and protein sequences for protein engineering. In _2024 IEEE International Conference on Bioinformatics and Biomedicine (BIBM)_ . IEEE, 2382–2389. 

- [129] Junjie Sheng, Yanqiu Lin, Jiehao Wu, Yanhong Huang, Jianqi Shi, Min Zhang, and Xiangfeng Wang. 2025. SolSearch: An LLM-Driven Framework for Efficient SAT-Solving Code Generation. In _2025 IEEE/ACM 47th International Conference on Software Engineering: New Ideas and Emerging Results (ICSE-NIER)_ . IEEE, 6–10. 

- [130] Yiding Shi, Jianan Zhou, Wen Song, Jieyi Bi, Yaoxin Wu, and Jie Zhang. 2025. Generalizable heuristic generation through large language models with meta-optimization. _arXiv preprint arXiv:2505.20881_ (2025). 

- [131] Yamato Shinohara, Jinglue Xu, Tianshui Li, and Hitoshi Iba. 2025. Large language models as particle swarm optimizers. _arXiv preprint arXiv:2504.09247_ (2025). 

- [132] Parshin Shojaee, Kazem Meidani, Shashank Gupta, Amir Barati Farimani, and Chandan K. Reddy. 2025. LLM-SR: Scientific Equation Discovery via Programming with Large Language Models. In _The Thirteenth International Conference on Learning Representations_ . 

- [133] Chenglei Si, Diyi Yang, and Tatsunori Hashimoto. 2025. Can LLMs Generate Novel Research Ideas? A Large-Scale Human Study with 100+ NLP Researchers. In _The Thirteenth International Conference on Learning Representations_ . 

- [134] Kevin Sim, Quentin Renau, and Emma Hart. 2025. Beyond the hype: Benchmarking llm-evolved heuristics for bin packing. In _International Conference on the Applications of Evolutionary Computation (Part of EvoStar)_ . Springer, 386–402. 

- [135] Gaurav Singh and Kavitesh Kumar Bali. 2024. Enhancing decision-making in optimization through llm-assisted inference: A neural networks perspective. In _2024 International Joint Conference on_ 

, Vol. 1, No. 1, Article . Publication date: January 2025. 

Liu et al. 

32 

_Neural Networks (IJCNN)_ . IEEE, 1–7. 

- [136] Eduardo Soares, Vidushi Sharma, Emilio Vital Brazil, Renato Cerqueira, and Young-Hye Na. 2023. Capturing formulation design of battery electrolytes with chemical large language model. In _AI for Accelerated Materials Design-NeurIPS 2023 Workshop_ . 

- [137] Chuanneng Sun, Songjun Huang, and Dario Pompili. 2024. LLM-based Multi-Agent Reinforcement Learning: Current and Future Directions. _arXiv preprint arXiv:2405.11106_ (2024). 

- [138] Weiwei Sun, Shengyu Feng, Shanda Li, and Yiming Yang. 2025. Co-bench: Benchmarking language model agents in algorithm search for combinatorial optimization. _arXiv preprint arXiv:2504.04310_ (2025). 

- [139] Anja Surina, Amin Mansouri, Lars Quaedvlieg, Amal Seddas, Maryna Viazovska, Emmanuel Abbe, and Caglar Gulcehre. 2025. Algorithm discovery with llms: Evolutionary search meets reinforcement learning. _arXiv preprint arXiv:2504.05108_ (2025). 

- [140] Mirac Suzgun, Nathan Scales, Nathanael Schärli, Sebastian Gehrmann, Yi Tay, Hyung Won Chung, Aakanksha Chowdhery, Quoc V Le, Ed H Chi, Denny Zhou, et al. 2022. Challenging big-bench tasks and whether chain-of-thought can solve them. _arXiv preprint arXiv:2210.09261_ (2022). 

- [141] Maria Taboada, Diego Martinez, Mohammed Arideh, and Rosa Mosquera. 2025. Ontology matching with large language models and prioritized depth-first search. _Information Fusion_ (2025), 103254. 

- [142] Ke Tang and Xin Yao. 2024. Learn to Optimize-A Brief Overview. _National Science Review_ (2024), nwae132. 

- [143] Xinyu Tang, Xiaolei Wang, Wayne Xin Zhao, Siyuan Lu, Yaliang Li, and Ji-Rong Wen. 2025. Unleashing the potential of large language models as prompt optimizers: Analogical analysis with gradient-based model optimizers. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , Vol. 39. 25264– 25272. 

- [144] Thanh VT Tran and Truong Son Hy. 2024. Protein design by directed evolution guided by large language models. _IEEE Transactions on Evolutionary Computation_ (2024). 

- [145] Karthik Valmeekam, Matthew Marquez, Alberto Olmo, Sarath Sreedharan, and Subbarao Kambhampati. 2024. Planbench: An extensible benchmark for evaluating large language models on planning and reasoning about change. _Advances in Neural Information Processing Systems_ 36 (2024). 

- [146] Niki van Stein and Thomas Bäck. 2024. Llamea: A large language model evolutionary algorithm for automatically generating metaheuristics. _IEEE Transactions on Evolutionary Computation_ (2024). 

- [147] Niki van Stein, Anna V. Kononova, Lars Kotthoff, and Thomas Bäck. 2025. Code evolution graphs: Understanding large language model driven design of algorithms. In _Proceedings of the Genetic and Evolutionary Computation Conference_ . 943–951. 

- [148] Niki van Stein, Anna V. Kononova, Haoran Yin, and Thomas Bäck. 2025. BLADE: Benchmark suite for LLM-driven Automated Design and Evolution of iterative optimisation heuristics. In _Proceedings of the Genetic and Evolutionary Computation Conference Companion_ . 2336–2344. 

- [149] Niki van Stein, Diederick Vermetten, and Thomas Bäck. 2024. In-the-loop hyper-parameter optimization for llm-based automated design of heuristics. _ACM Transactions on Evolutionary Learning_ (2024). 

- [150] Petar Veličković, Adrià Puigdomènech Badia, David Budden, Razvan Pascanu, Andrea Banino, Misha Dashevskiy, Raia Hadsell, and Charles Blundell. 2022. The CLRS algorithmic reasoning benchmark. In _International Conference on Machine Learning_ . PMLR, 22084–22102. 

- [151] Fang Wan, Tao Wang, Kezhi Wang, Yuanhang Si, Julien Fondrevelle, Shuimiao Du, and Antoine Duclos. 2025. Surgery scheduling based on large language models. _Artificial Intelligence in Medicine_ (2025), 103151. 

- [152] Jianxun Wang and Yixiang Chen. 2023. A review on code generation with llms: Application and evaluation. In _2023 IEEE International Conference on Medical Artificial Intelligence (MedAI)_ . IEEE, 284–289. 

- [153] Ludi Wang, Xueqing Chen, Yi Du, Yuanchun Zhou, Yang Gao, and Wenjuan Cui. 2025. CataLM: empowering catalyst design through large language models. _International Journal of Machine Learning and Cybernetics_ (2025), 1–11. 

- [154] Lei Wang, Chen Ma, Xueyang Feng, Zeyu Zhang, Hao Yang, Jingsen Zhang, Zhiyuan Chen, Jiakai Tang, Xu Chen, Yankai Lin, et al. 2024. A survey on large language model based autonomous agents. _Frontiers of Computer Science_ 18, 6 (2024), 186345. 

- [155] Shuai Wang, Shengyao Zhuang, Bevan Koopman, and Guido Zuccon. 2025. Resllm: Large language models are strong resource selectors for federated search. In _Companion Proceedings of the ACM on Web Conference 2025_ . 1360–1364. 

, Vol. 1, No. 1, Article . Publication date: January 2025. 

A Systematic Survey on Large Language Models for Algorithm Design 

33 

- [156] Xinyuan Wang, Chenxi Li, Zhen Wang, Fan Bai, Haotian Luo, Jiayou Zhang, Nebojsa Jojic, Eric Xing, and Zhiting Hu. 2024. PromptAgent: Strategic Planning with Language Models Enables Expert-level Prompt Optimization. In _The Twelfth International Conference on Learning Representations_ . 

- [157] Yatong Wang, Yuchen Pei, and Yuqi Zhao. 2024. TS-EoH: An Edge Server Task Scheduling Algorithm Based on Evolution of Heuristic. In _2024 IEEE International Symposium on Parallel and Distributed Processing with Applications (ISPA)_ . IEEE, 693–700. 

- [158] Zidong Wang, Fei Liu, Qi Feng, Qingfu Zhang, and Xiaoguang Gao. 2025. LLM-enhanced score function evolution for causal structure learning. In _Proceedings of the Thirty-Fourth International Joint Conference on Artificial Intelligence_ . 9086–9094. 

- [159] Zeyi Wang, Songbai Liu, Jianyong Chen, and Kay Chen Tan. 2024. Large Language Model-Aided Evolutionary Search for Constrained Multiobjective Optimization. In _International Conference on Intelligent Computing_ . Springer, 218–230. 

- [160] Segev Wasserkrug, Leonard Boussioux, Dick den Hertog, Farzaneh Mirzazadeh, Ilker Birbil, Jannis Kurtz, and Donato Maragno. 2024. From Large Language Models and Optimization to Decision Optimization CoPilot: A Research Manifesto. _arXiv preprint arXiv:2402.16269_ (2024). 

- [161] Melvin Wong, Jiao Liu, Thiago Rios, Stefan Menzel, and Yew Soon Ong. 2024. LLM2FEA: Discover Novel Designs with Generative Evolutionary Multitasking. _arXiv preprint arXiv:2406.14917_ (2024). 

- [162] Melvin Wong, Thiago Rios, Stefan Menzel, and Yew Soon Ong. 2024. Generative AI-based Prompt Evolution Engineering Design Optimization With Vision-Language Model. _arXiv preprint arXiv:2406.09143_ (2024). 

- [163] Xingyu Wu, Sheng-hao Wu, Jibin Wu, Liang Feng, and Kay Chen Tan. 2024. Evolutionary computation in the era of large language model: Survey and roadmap. _IEEE Transactions on Evolutionary Computation_ (2024). 

- [164] Xingyu Wu, Yan Zhong, Jibin Wu, Bingbing Jiang, and Kay Chen Tan. 2024. Large Language ModelEnhanced Algorithm Selection: Towards Comprehensive Algorithm Representation. In _Proceedings of the 33rd International Joint Conference on Artificial Intelligence, IJCAI 2024_ . 5235–5244. 

- [165] Ziyang Xiao, Jingrong Xie, Lilin Xu, Shisi Guan, Jingyan Zhu, Xiongwei Han, Xiaojin Fu, WingYin Yu, Han Wu, Wei Shi, et al. 2025. A survey of optimization modeling meets llms: Progress and future directions. _arXiv preprint arXiv:2508.10047_ (2025). 

- [166] Lindong Xie, Genghui Li, Zhenkun Wang, Edward Chung, and Maoguo Gong. 2025. Large language model-driven surrogate-assisted evolutionary algorithm for expensive optimization. _arXiv preprint arXiv:2507.02892_ (2025). 

- [167] Zhuoliang Xie, Fei Liu, Zhenkun Wang, and Qingfu Zhang. 2025. LLM-Driven Neighborhood Search for Efficient Heuristic Design. In _2025 IEEE Congress on Evolutionary Computation (CEC)_ . IEEE, 1–8. 

- [168] Meng Xu, Jiao Liu, and Yew Soon Ong. 2025. EvoSpeak: Large Language Models for Interpretable Genetic Programming-Evolved Heuristics. _arXiv preprint arXiv:2510.02686_ (2025). 

- [169] Zhenxing Xu, Yizhe Zhang, Weidong Bao, Hao Wang, Ming Chen, Haoran Ye, Wenzheng Jiang, Hui Yan, and Ji Wang. 2025. AutoEP: LLMs-Driven Automation of Hyperparameter Evolution for Metaheuristic Algorithms. _arXiv preprint arXiv:2509.23189_ (2025). 

- [170] Chengrun Yang, Xuezhi Wang, Yifeng Lu, Hanxiao Liu, Quoc V Le, Denny Zhou, and Xinyun Chen. 2024. Large Language Models as Optimizers. In _The Twelfth International Conference on Learning Representations_ . 

- [171] Xu Yang, Rui Wang, Kaiwen Li, Wenhua Li, and Weixiong Huang. 2025. Large Language Modelassisted Meta-optimizer for Automated Design of Constrained Evolutionary Algorithm. _arXiv preprint arXiv:2509.13251_ (2025). 

- [172] Shunyu Yao, Fei Liu, Xi Lin, Zhichao Lu, Zhenkun Wang, and Qingfu Zhang. 2025. Multi-objective evolution of heuristic using large language model. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , Vol. 39. 27144–27152. 

- [173] Xufeng Yao, Jiaxi Jiang, Yuxuan Zhao, Peiyu Liao, Yibo Lin, and Bei Yu. 2025. Evolution of Optimization Algorithms for Global Placement via Large Language Models. _arXiv preprint arXiv:2504.17801_ (2025). 

- [174] Yiming Yao, Fei Liu, Ji Cheng, and Qingfu Zhang. 2024. Evolve cost-aware acquisition functions using large language models. In _International Conference on Parallel Problem Solving from Nature_ . Springer, 374–390. 

- [175] Milad Yazdani, Mahdi Mostajabdaveh, Samin Aref, and Zirui Zhou. 2025. EvoCut: Strengthening Integer Programs via Evolution-Guided Language Models. _arXiv preprint arXiv:2508.11850_ (2025). 

, Vol. 1, No. 1, Article . Publication date: January 2025. 

Liu et al. 

34 

- [176] Gavin Ye. 2024. De novo drug design as GPT language modeling: large chemistry models with supervised and reinforcement learning. _Journal of Computer-Aided Molecular Design_ 38, 1 (2024), 20. 

- [177] Geyan Ye, Xibao Cai, Houtim Lai, Xing Wang, Junhong Huang, Longyue Wang, Wei Liu, and Xiangxiang Zeng. 2025. Drugassist: A large language model for molecule optimization. _Briefings in Bioinformatics_ 26, 1 (2025), bbae693. 

- [178] Haoran Ye, Jiarui Wang, Zhiguang Cao, Federico Berto, Chuanbo Hua, Haeyeon Kim, Jinkyoo Park, and Guojie Song. 2024. ReEvo: large language models as hyper-heuristics with reflective evolution. In _Proceedings of the 38th International Conference on Neural Information Processing Systems_ . 43571–43608. 

- [179] He Yu and Jing Liu. 2024. Deep insights into automated optimization with large language models and evolutionary algorithms. _arXiv preprint arXiv:2410.20848_ (2024). 

- [180] Junhua Zeng, Chao Li, Zhun Sun, Qibin Zhao, and Guoxu Zhou. 2024. tnGPS: Discovering Unknown Tensor Network Structure Search Algorithms via Large Language Models (LLMs). In _Forty-first International Conference on Machine Learning, ICML_ . 

- [181] Huan Zhang, Yu Song, Ziyu Hou, Santiago Miret, and Bang Liu. 2024. HoneyComb: A Flexible LLM-Based Agent System for Materials Science. In _Findings of the Association for Computational Linguistics: EMNLP 2024_ . 3369–3382. 

- [182] Jenny Zhang, Shengran Hu, Cong Lu, Robert Lange, and Jeff Clune. 2025. Darwin Godel Machine: Open-Ended Evolution of Self-Improving Agents. _arXiv preprint arXiv:2505.22954_ (2025). 

- [183] Michael R Zhang, Nishkrit Desai, Juhan Bae, Jonathan Lorraine, and Jimmy Ba. 2023. Using large language models for hyperparameter optimization. In _NeurIPS 2023 Foundation Models for Decision Making Workshop_ . 

- [184] Ruohong Zhang, Liangke Gui, Zhiqing Sun, Yihao Feng, Keyang Xu, Yuanhan Zhang, Di Fu, Chunyuan Li, Alexander G Hauptmann, Yonatan Bisk, et al. 2025. Direct Preference Optimization of Video Large Multimodal Models from Language Model Reward. In _Proceedings of the 2025 Conference of the Nations of the Americas Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers)_ . 694–717. 

- [185] Rui Zhang, Fei Liu, Xi Lin, Zhenkun Wang, Zhichao Lu, and Qingfu Zhang. 2024. Understanding the Importance of Evolutionary Search in Automated Heuristic Design with Large Language Models. In _International Conference on Parallel Problem Solving from Nature_ . Springer, 185–202. 

- [186] Rui Zhang, Yixin Su, Bayu Distiawan Trisedya, Xiaoyan Zhao, Min Yang, Hong Cheng, and Jianzhong Qi. 2024. AutoAlign: Fully Automatic and Effective Knowledge Graph Alignment Enabled by Large Language Models. _IEEE Trans. Knowl. Data Eng._ (2024). 

- [187] Shaofeng Zhang, Shengcai Liu, Ning Lu, Jiahao Wu, Ji Liu, Yew-Soon Ong, and Ke Tang. 2025. Llm-driven instance-specific heuristic generation and selection. _arXiv preprint arXiv:2506.00490_ (2025). 

- [188] Shenao Zhang, Sirui Zheng, Shuqi Ke, Zhihan Liu, Wanxin Jin, Jianbo Yuan, Yingxiang Yang, Hongxia Yang, and Zhaoran Wang. 2024. How Can LLM Guide RL? A Value-Based Approach. _arXiv preprint arXiv:2402.16181_ (2024). 

- [189] Yisong Zhang, Ran Cheng, Guoxing Yi, and Kay Chen Tan. 2025. A Systematic Survey on Large Language Models for Evolutionary Optimization: From Modeling to Solving. _arXiv preprint arXiv:2509.08269_ (2025). 

- [190] Yu Zhang, Kefeng Zheng, Fei Liu, Qingfu Zhang, and Zhenkun Wang. 2025. AutoTurb: Using large language models for automatic algebraic turbulence model discovery. _Physics of Fluids_ 37, 1 (2025). 

- [191] Qi Zhao, Qiqi Duan, Bai Yan, Shi Cheng, and Yuhui Shi. 2024. Automated Design of Metaheuristic Algorithms: A Survey. _Transactions on Machine Learning Research_ (2024). 

- [192] Wayne Xin Zhao, Kun Zhou, Junyi Li, Tianyi Tang, Xiaolei Wang, Yupeng Hou, Yingqian Min, Beichen Zhang, Junjie Zhang, Zican Dong, et al. 2023. A survey of large language models. _arXiv preprint arXiv:2303.18223_ (2023). 

- [193] Zibin Zheng, Kaiwen Ning, Yanlin Wang, Jingwen Zhang, Dewu Zheng, Mingxi Ye, and Jiachi Chen. 2023. A survey of large language models for code: Evolution, benchmarking, and future trends. _arXiv preprint arXiv:2311.10372_ (2023). 

- [194] Zhi Zheng, Zhuoliang Xie, Zhenkun Wang, and Bryan Hooi. 2025. Monte Carlo Tree Search for Comprehensive Exploration in LLM-Based Automatic Heuristic Design. In _Forty-second International Conference on Machine Learning_ . 

- [195] Xun Zhou, Xingyu Wu, Liang Feng, Zhichao Lu, and Kay Chen Tan. 2025. Design principle transfer in neural architecture search via large language models. In _Proceedings of the AAAI Conference on_ 

, Vol. 1, No. 1, Article . Publication date: January 2025. 

- A Systematic Survey on Large Language Models for Algorithm Design 35 _Artificial Intelligence_ , Vol. 39. 23000–23008. 

- [196] Yongchao Zhou, Andrei Ioan Muresanu, Ziwen Han, Keiran Paster, Silviu Pitis, Harris Chan, and Jimmy Ba. 2022. Large language models are human-level prompt engineers. In _The eleventh international conference on learning representations_ . 

Received 20 February 2007; revised 12 March 2009; accepted 5 June 2009 

, Vol. 1, No. 1, Article . Publication date: January 2025. 

