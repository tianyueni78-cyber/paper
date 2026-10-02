LARGE LANGUAGE MODELS FOR COMBINATORIAL OPTIMIZATION: A SYSTEMATIC REVIEW 

## **Francesca Da Ros University of Udine, Italy** 

## **Michael Soprano University of Udine, Italy** 

```
francesca.daros@uniud.itmichael.soprano@uniud.it
```

**Luca Di Gaspero University of Udine, Italy** `luca.digaspero@uniud.it` 

**Kevin Roitero University of Udine, Italy** 

```
kevin.roitero@uniud.it
```

# **ABSTRACT** 

This systematic review explores the application of Large Language Models (LLMs) in Combinatorial Optimization (CO). We report our findings using the Preferred Reporting Items for Systematic Reviews and Meta-Analyses (PRISMA) guidelines. We conduct a literature search via Scopus and Google Scholar, examining over 2,000 publications. We assess publications against four inclusion and four exclusion criteria related to their language, research focus, publication year, and type. Eventually, we select 103 studies. We classify these studies into semantic categories and topics to provide a comprehensive overview of the field, including the tasks performed by LLMs, the architectures of LLMs, the existing datasets specifically designed for evaluating LLMs in CO, and the field of application. Finally, we identify future directions for leveraging LLMs in this field. 

**_K_ eywords** Systematic Review _·_ Large Language Models _·_ Combinatorial Optimization 

# **1 Introduction** 

Combinatorial Optimization Problems (COPs) are a class of optimization problems characterized by discrete variable domains and finite search space. Combinatorial Optimization (CO) plays a crucial role in identifying promising solutions in many areas requiring complex decision-making capabilities, such as industrial [219] and employee scheduling [25, 102], facility location [27, 64], and timetabling [199, 254]. Traditionally, such problems are modeled with techniques like Linear Programming (LP), Integer Linear Programming (ILP), Mixed Integer Linear Programming (MILP), and Constraint Programming (CP), further solved through commercial solvers such as IBM ILOG CPLEX [88] or Gurobi [70] and through heuristic and Metaheuristic (MH) algorithms [194]. 

While many successful CO applications have been developed, the design and engineering of optimization tasks remain primarily human-driven. Users must convert the problem into an optimization model by defining a set of variables, constraints, and one or more objective functions, then coding and running a software solver or algorithm to find solutions. These activities are not trivial and require a certain extent of expertise. 

Inspired by the recent advancements in the usage of Large Language Models (LLMs) to perform a wide array of complex tasks, there is growing interest in integrating LLMs into CO to mitigate the human-intensive aspects of optimization [53, 84, 145, 236]. The abilities of LLMs to process, interpret, and generate human language make them particularly suited for tackling activities within CO, including the translation of natural language descriptions to formalisms such as mathematical models [74, 89] and code generation [111, 214]. 

The rapid advancement in Artificial Intelligence (AI) and in particular in Natural Language Processing (NLP) has led to a rapid increase in the capabilities and applications of LLMs, resulting in a proliferation of scholarly works and models being developed. While highlighting the increasing activity in the field, this multitude of studies has created a complex body of knowledge that is challenging to navigate. Looking specifically at the application of LLMs to CO, the academic literature is limited and fragmented, with existing works characterized by diverse methodologies, areas of applications, and findings. 

LLMS FOR COMBINATORIAL OPTIMIZATION 

DA ROS ET AL. 

Therefore, this systematic review aims to consolidate the current state-of-the-art in LLMs applied to CO. We identify, screen, analyze, and systematically organize the literature to clarify the topic and identify strategic directions for ongoing and future research efforts. The process is reported following the Preferred Reporting Items for Systematic Reviews and Meta-Analyses (PRISMA) guidelines. Through this examination, we seek to understand the capabilities of LLMs in addressing complex optimization tasks and to explore the evolving trends and directions in this field. By systematically synthesizing and analyzing existing research, this review aims to provide a structured understanding of how LLMs are employed in CO and offer insights that can inform future research in the field. 

The remainder of this review is structured as follows. In Section 2, we discuss the aims and motivations that drove our work. We then explore the relationships and differences with related work in Section 3. In Section 4, we present the background necessary to understand the interconnections between LLMs and CO. We provide a detailed account of the methodology we followed in Section 5. In Section 6, we classify and discuss the studies included in our review. Next, we outline future research directions in Section 7 and discuss the limitations of our approach in Section 8. Finally, we draw some conclusions and propose future work in Section 9. 

# **2 Aims and Motivations** 

The main objective of this systematic review is to critically evaluate the current state of LLMs application in CO. To this end, we aim to answer the following questions: 

- _(i)_ How are LLMs currently being applied to COPs? 

- _(ii)_ Which tasks of the optimization process are aided with LLMs? 

- _(iii)_ Which LLM architectures and training paradigms are most effective for CO? 

- _(iv)_ Which application fields are employing LLMs within CO? 

- _(v)_ What are the main trends in the application of LLMs within CO? 

- _(vi)_ What are possible research directions in the application of LLMs to CO? 

Two primary motivations drive this systematic review. Firstly, traditional optimization approaches primarily rely on human expertise (e.g., application domain knowledge, coding capabilities, etc.), thus limiting their applicability, scalability, and efficiency. Leveraging LLMs offers a promising direction, as their success in tasks like entity recognition, domain knowledge, and coding suggests their potential for CO. For instance, LLMs could be used for translating high-level descriptions of solution algorithms to executable code [125]. 

Secondly, the rapid evolution of NLP (in particular of LLMs) and their application in optimization techniques (specifically CO), highlights the urgency of a comprehensive systematic review. Existing literature and reviews are scattered, lacking a cohesive framework that provides researchers and practitioners with clear guidance in the domain of LLMs applied to CO. 

While exploring the reverse relationship between LLMs and CO (i.e., applying CO techniques to enhance LLMs) is also a valid research direction, we deliberately chose not to include it in this survey. This is primarily because such applications essentially use well-established CO methods in a new, albeit challenging, domain. Instead, we focus on the novel and emerging contributions of LLMs to the practice of CO, as this also aligns more closely with the primary research interests of some of the authors, particularly in exploring the potential for LLMs to enhance CO techniques. For the same reason, our review emphasizes CO rather than other paradigms, such as continuous optimization. This decision is also motivated by the inherent differences between the two paradigms: continuous optimization typically relies on mathematical models or black-box ones, whereas CO encompasses a broader and more diverse set of problem domains (e.g., scheduling, assignment, routing, permutation-based problems) characterized by intricate substructures and complex constraints. This diversity makes the application of LLMs to CO potentially more impactful, given the richness and complexity of the CO landscape. 

# **3 Related Work** 

A limited number of surveys have addressed the intersection of LLM and CO along with related topics. It is important to remark that none of these works are systematic reviews. In this section, we overview their main characteristics and highlight the differences with respect to our work. 

Fan et al. [53] presented a review of AI applications in Operations Research (OR), with a focus on three specific aspects of the optimization process: conversion of data into modeling parameters, model formulations, and model optimization. 

2 

LLMS FOR COMBINATORIAL OPTIMIZATION 

DA ROS ET AL. 

Although they extensively covered various AI techniques, such as Reinforcement Learning (RL) and Neural Networks (NNs), the usage of LLMs was investigated only in the context of model formulation [53, Section 4]. Huang et al. [84] explored the topic by including not only CO, but also continuous optimization and the use of optimization for LLMs. However, when discussing LLMs for optimization, they examined a set of 20 papers and focused on a narrow range of optimization aspects, specifically algorithm generation and the usage of LLMs as search operators. Lai et al. [109] reviewed the literature on LLMs concerning their mathematical capabilities and briefly discussed their applications in CO along with math word problems, geometry problems, and theorem proving. Liu et al. [128] described the application of LLMs to algorithm design in various fields, like optimization, Machine Learning (ML), mathematical reasoning, and scientific discovery. Wu et al. [236] provided a review on the intersection of Evolutionary Computation (EC) and LLMs. As done by Huang et al. [84], they also covered aspects like continuous optimization and the use of optimization for LLMs enhancement. However, their focus on EC represented only a partial view of the CO landscape and, more generally, of optimization techniques. Similarly, Yu and Liu [246] and Cai et al. [23] described the evolution of Evolutionary Algorithms (EAs) to solve optimization problems from heuristic approaches to LLMs. 

Our systematic review differ from the aforementioned surveys in the following ways: 

- _(i)_ We systematically reviewed the topic using a rigorous methodology to identify, screen, include, and analyze relevant literature works. We reported the process following the PRISMA 2020 guidelines. 

- _(ii)_ We limited our focus to the usage of LLMs within CO, thus excluding optimization areas outside discrete combinatorial optimization, as well as the use of optimization within LLMs, nor, more generally, the use of LLMs for mathematical problem-solving. 

- _(iii)_ We addressed the entire optimization process, not focusing solely on specific parts. 

- _(iv)_ We considered a broader set of optimization techniques and algorithms, not just evolutionary techniques. 

- _(v)_ We described datasets, frameworks, tools, and metrics that could enhance applications of LLMs within CO. 

# **4 Background** 

## **4.1 Large Language Models** 

LLMs have fundamentally transformed the landscape of NLP and related fields. At the core of this transformation is the Transformer architecture introduced by Vaswani et al. [220], which revolutionized the NLP field with the introduction of an improved self-attention mechanism built on top of the one proposed by Bahdanau et al. [12]. This mechanism allows models to weigh the importance of different words in a sentence, irrespective of their distance, leading to more contextually aware representations. 

The Transformer architecture operates with an arrangement of two specified modules, an encoder and a decoder, designed to transform the input data into more abstract and general-purpose representations. Each encoder and decoder in the architecture is built from layers that perform specific functions. First, positional encoding is introduced to inject information about the order of input words into the model, which is crucial for processing sequences where the arrangement of elements carries meaning, as is common in NLP. Following positional encoding, the embedding layer converts the input tokens (i.e., individual pieces of text, typically words or sub-words) into vectors of continuous numbers. This transformation turns linguistic information into a mathematical form that neural networks can process. Once the input has been encoded and embedded, it passes through the Transformer’s core mechanisms, i.e., the attention layers. The encoder relies on a self-attention mechanism to independently assess and emphasize different parts of the input data. This allows the model to understand each input segment in relation to the rest of the input, thus enhancing the context awareness of the system. In parallel, the decoder also employs a self-attention layer but focuses on generating the next output token in the sequence conditioned on the tokens generated so far. This ensures that each generated element is contextually aligned with the previous (i.e., already generated) text. Additionally, cross-attention layers in the decoder access the encoder’s output to guide the generation process. These layers allow the decoder to reference the full context provided by the encoder, ensuring that each output token is a contextually appropriate continuation or response to the specific provided input sequence. This comprehensive mechanism of encoding, self-attention, and cross-attention within the Transformer allows for highly effective processing and generation of text, making it a robust model for various complex language understanding and generation tasks. 

Building on the innovative self-attention mechanism of the Transformer, subsequent models have been developed with specialized architectures tailored for different tasks. `ELMo` [170] defined the usage on contextual embeddings. Encoder-only models, like `BERT` [44], specialize in tasks that require a deep understanding of language context, making them ideal for applications like sentiment analysis and named entity recognition. On the other hand, decoder-only 

3 

LLMS FOR COMBINATORIAL OPTIMIZATION 

DA ROS ET AL. 

models, such as `GPT-3` [21] and `GPT-4` [22, 160], excel in generating coherent and contextually appropriate text, powering applications in creative writing and dialogue systems. 

After encoder and decoder-only models, the introduction of instruction-based models marks a significant evolution in LLMs. These models are trained to follow user-provided instructions [34, 162], making them versatile tools across various tasks without needing task-specific fine-tuning. Instruction-based training involves exposing the model to various tasks during training, along with corresponding instructions, thereby enabling the model to generalize from instructions at inference time. This approach has started the development of emerging abilities in LLMs, such as zero-shot learning capabilities [104], complex reasoning strategies [15, 230], and the discovery of latent abilities that emerge as models sled [229]. 

Following the introduction of instruction-based models in LLMs, several state-of-the-art models have epitomized this approach, showcasing remarkable capabilities in handling a wide array of tasks directly based on user instructions. Some notable models in this field include `PaLM` [33], which represents a significant advancement in scaling up transformerbased architectures designed to perform well across diverse linguistic tasks. Its successor, `PaLM-2` [66], builds upon this foundation with improved training techniques and larger model capacities, further enhancing its ability to understand and generate nuanced text based on instructions. `PaLM-E` [49] further extends the `PaLM` series by emphasizing efficiency in energy usage and processing speed, making it a more sustainable option for deploying sophisticated NLP tasks at scale. 

Another architecture is `LLaMA` [212] and its successors, `LLaMa 2` [62] and `LLaMa 3` [132], which focus on achieving high cross-task effectiveness with relatively smaller model sizes, facilitating easier deployment and lower operational costs without compromising on capability. These architectures have demonstrated significant prowess in tasks requiring deep contextual understanding. `Mistral 7B` [90] and `Mixtral 8x7B` [91] introduce a unique approach to model training called Mixture of Experts (MoE) that involves dynamic adjustments of model parameters based on task complexity, which enhances the model’s adaptability and performance across different NLP tasks. `Gemini 1.5` [206] is another innovative model that integrates dual mechanisms of understanding and generation to improve interaction dynamics in conversational AI applications. `Bard` [141] focuses on incorporating broad, encyclopedic knowledge and the ability to update its understanding in real-time, making it exceptionally useful for applications that require up-to-date information. Finally, `Claude` [11] distinguishes itself by its ethical training framework, prioritizing safety and fairness, setting a new standard in responsible AI development. 

These models exemplify the most advanced and state-of-the-art instruction-based learning, where each has been tailored to excel in standard benchmarks and improve specific aspects such as versatility, efficiency, and ethical considerations. 

## **4.2 Combinatorial Optimization** 

COPs are a class of optimization problems defined by discrete decision variables and the objective of finding one or more optimal solutions within a finite search space of solutions [97]. Many of these problems are classified as NP-hard, meaning that, based on current knowledge, they require exponential time to be optimally solved. Besides the prominent Boolean Satisfiability Problem (SAT), prototypical COPs include the Permutation Flowshop Scheduling Problem (PFSP) [165], the Knapsack Problem (KP), the Graph Coloring Problem (GCP), and the Traveling Salesperson Problem (TSP) [174]. CO is also widely applied to tackle real-world problems across various domains. Examples include employee scheduling [101, 247], machine scheduling [107, 150], educational timetabling [26], and automotive production [232], to name a few. 

Figure 1 outlines the steps practitioners and researchers undertake to address an optimization problem [14, 214]. In the following, we detail the process specifically for the case of CO. 

The first step regards the description in Natural Language (NL) of the decision-making process or real-world issue to be tackled. Its specifications must be outlined to identify the decisions to be made, the rules that must be followed, and the goals to be achieved. 

After framing the decision-making process, the practitioner must create a formal representation to enable a software solver or a custom algorithm to tackle it. A given NL description can correspond to multiple representations, called _models_ or _problem formulations_ . Models are articulated in terms of _(i) variables_ (or decision variables), which represent the decisions to be made; _(ii) constraints_ , which are restrictions on the possible values of the variables and capture problem substructures and/or business rules; and _(iii)_ at least one _objective_ (or fitness) _function_ , which assesses the quality of a solution. When the problem tackles more than one objective function, it is the case of multi-objective optimization. The development of an effective problem formulation is known as _modeling_ . How we define variables, objectives, and constraints determines the model type. E.g., if variables assume integer values and constraints are linear, 

4 

LLMS FOR COMBINATORIAL OPTIMIZATION 

DA ROS ET AL. 



<!-- Start of picture text -->
Problem model i ng Solut i on method<br>Model Algor i thm/solver Solut i on(s) Ob j ect i ve value(s)<br>Var i ables<br>Descr i pt i on  i n natural  Constra i nts Algor i thm/solver Solut i on(s) Ob j ect i ve value(s)<br>language<br>Real - world  Dec i s i ons Ob j ect i ve(s) Algor i thm/solver Solut i on(s) Ob j ect i ve value(s)<br>problem Rules Model<br>Goal(s) Var i ables (Automated)<br>Data Constra i nts Algor i thm<br>conf i gurat i on<br>Ob j ect i ve(s)<br>Instance<br> Val i dat i on<br>No Free Lunch Theorem (benchmark i ng)<br><!-- End of picture text -->

Figure 1: Overview of the steps for addressing an optimization problem. 

the model is an ILP. Other model types, such as MILP and LP, handle both discrete and continuous variables, while structured constraints can be represented using CP. 

While a problem formulation provides an abstract formal description of a decision process, an _instance_ (or problem instance) represents a specific case of the problem defined by concrete data. A _solution_ to a problem instance is an assignment of values to all the decision variables. As mentioned before, the solution quality is evaluated through an objective function, which provides one or more objective values, also referred to as scores or costs (typically numerical values). The search space of an instance encompasses all possible assignments of the variables; the subset of solutions that satisfy all constraints is called the set of _feasible_ solutions. A solution which violates at least one constraint is called _infeasible_ . When no feasible solution exists for an instance, resulting in a logically inconsistent instantiation of the problem model, the model instance is also called infeasible. 

The search space is explored using _solution methods_ , which are algorithms or software solvers. Solution methods for COPs can be classified based on the completeness of their search (i.e., complete or incomplete methods) and how solutions are constructed (i.e., perturbative or constructive methods). Note that models and solution methods are strictly coupled together. 

Complete methods exhaustively explore the search space, ensuring that _(i)_ If a solution exists, the complete method will eventually find it; _(ii)_ When the search terminates, the best solution found is guaranteed to be optimal (for this reason, complete methods are also called exact methods). Examples of these methods include LP, MILP, and CP [186]. For such methods, numerous widely accepted software tools exist, including IBM ILOG CPLEX and IBM CP Optimizer [88], Gurobi Optimizer [70], OR-Tools [169], Gecode [60], and the solvers included in the MiniZinc distribution [155] together with interfaces and APIs available in common programming languages. 

However, given that most COPs are NP-hard [59, 106], exhaustive exploration can result in an exponential increase in runtime w.r.t. the size of the problem instance. Additionally, in many real-world applications, it is not necessary to certify the optimality of a solution. Instead, obtaining a good, feasible solution in a reasonable amount of time is sufficient. Incomplete methods address such necessities by exploring the search space non-exhaustively, often using stochastic approaches. When these methods are tailored to the problem, they are called heuristics; when they employ problem-independent strategies, they are referred to as MHs [144]. Examples of MHs include Tabu Search (TS) [65], Simulated Annealing (SA) [55, 100], Greedy Randomized Adaptive Search Procedure (GRASP) [108], Large Neighborhood Search (LNS) [191] and its adaptive version [231], Genetic Algorithm (GA) [76], Biased Random-key Genetic Algorithm (BRKGA) [133], and Ant Colony Optimization (ACO) [48]. Differently from complete methods, widely accepted tools have not been available for incomplete methods, where researchers still rely on customized coding solutions [203, 204, 205] and on a sprout of possible frameworks and libraries [135, 168]. 

Constructive methods build solutions from scratch and iteratively set all variables according to specific policies. Examples include CP and ACO. Conversely, perturbative methods start from an existing complete solution and generate new solutions by modifying some variables. Examples include methods based on the concept of neighborhood, such as TS and SA. 

Algorithmic choices in solvers and algorithms can be addressed through _automated algorithm configuration_ , as advocated by the Programming by Optimization (PbO) manifesto [77]. Such a paradigm calls for a shift of perspective 

5 

LLMS FOR COMBINATORIAL OPTIMIZATION 

DA ROS ET AL. 

in software development, where the design of components is approached through optimization. This involves a systematic exploration of design alternatives to select a configuration for the different components via automated tools (e.g., irace [138]). 

The process undergoes various types of _validation_ . First, a practitioner must ensure that the models adhere as closely as possible to the real-world scenario, even though some assumptions are necessary to generalize the concepts (i.e., validation of specifications). Secondly, model and technical validation should be applied to check the correctness of the code, ensure it adheres to the model, and evaluate its performance efficiency. Furthermore, to efficiently solve a problem, evaluating and comparing different algorithms, solvers, and models is essential. This comparison is necessary because of the _No Free Lunch Theorem_ [233], which states that no single algorithm is best suited for all instances of an optimization problem. Therefore, rigorous tests are conducted to determine the most effective approach for the specific problem, ensuring that the chosen solution method is robust and efficient (in other fields, this type of validation is addressed as a _benchmarking_ process). 

# **5 Methodology** 

## **5.1 PRISMA** 

The Preferred Reporting Items for Systematic Reviews and Meta-Analyses (PRISMA) guidelines are a well-known framework for reporting systematic reviews. The current version was proposed in 2020 [163] and builds upon the PRISMA 2009 formulation [149]. This methodology evolved from the earlier Quality of Reporting of Meta-analyses (QUOROM) guidelines [148], which were firstly introduced in 1999. This evolution over time has broadened the scope of the guidelines. While QUOROM primarily focused on improving reports of meta-analyses in clinical trials, PRISMA addresses systematic reviews that evaluate the effects of health interventions more broadly. These guidelines are sufficiently general to apply to reports of systematic reviews that evaluate other types of interventions [121, 234], systematic reviews with objectives beyond evaluating interventions [75, 185], and systematic reviews not related with the medical field [154, 193, 217]. PRISMA can be used to report systematic reviews that involve result synthesis, such as meta-analyses and other statistical methods. It is also helpful for reviews identifying only a single eligible study and for mixed-methods approaches. 

At its core, PRISMA is composed of four main elements: the statement [163], the explanation and elaboration document [164], the checklist,<sup>1</sup> and the flow diagram.<sup>2</sup> The statement introduces the purpose of the methodology. The checklist consists of 27 items across 7 sections, providing guidelines for writing a systematic review report. It should be used alongside the explanation and elaboration document, which offers additional reporting guidance for each item. The diagram shows the flow of information through the review phases. 

In this work, we adopt, use, rely on, and refer to the PRISMA 2020 guidelines [163, 164]. 

## **5.2 Terminology** 

Most of the terminology used within PRISMA resources [163, 164] derives from its original field of application – systematic reviews of health-related interventions – which may be confusing for researchers from other disciplines. We particularly refer to the following definitions [163]: 

- _(i) Study_ : an experiment including a defined group of participants and one or more interventions and outcomes. 

- _(ii) Report_ : a paper providing information about a particular study. Multiple reports may refer to the same study. 

- _(iii) Record_ : the title or abstract (or both) of a report indexed in a database or website. 

- _(iv) Outcome_ : a measurement event for participants in a study. 

- _(v) Result_ : the combination of a point estimate and precision measurement for an outcome. 

Since our systematic review covers a broader scope than health-related interventions, where we expect to find only individual eligible studies rather than multiple studies referring to a given experimental design, we will join the definitions of _study_ and _report_ , using _study_ to refer to papers in general. This approach will also apply to the definitions of _result_ and _outcome_ . We consider the term _record_ to encompass titles and abstracts of papers. For example, the PRISMA flow diagram explicitly distinguishes between records screened and reports sought for retrieval. We will adjust this to refer only to records as we define them. 

> 1 `https://www.prisma-statement.org/prisma-2020-checklist` 

> 2 `https://www.prisma-statement.org/prisma-2020-flow-diagram` 

6 

LLMS FOR COMBINATORIAL OPTIMIZATION 

DA ROS ET AL. 

## **5.3 Literature Collection** 

## **5.3.1 Process** 

Our systematic review includes studies up to the end of 2024. The literature collection process, conducted according to PRISMA, involves three main activities: identification, screening, and inclusion (Figure 2). To provide a comprehensive overview of our application of the PRISMA guidelines, we have included the checklists in Appendix A. 

While the inclusion activity simply involves reporting the number of studies included in the systematic review, the task of identifying and screening records is more complex. Figure 3 reports a Business Process Model and Notation (BPMN) diagram [158] describing how we conducted these activities. Initially, all authors worked together to define the keywords for searching records, establish eligibility criteria for study inclusion/exclusion, and select the databases for record identification. Subsequently, one author sent queries to the selected databases to retrieve records and performed data cleaning to remove duplicates and records without authors. Then, the author screened the remaining records by reviewing titles, abstracts, and publication years in order to apply an initial filter. The resulting list was then augmented through citation tracking [36]. After this phase, three authors independently read the full text of one-third of the studies each. They then decided whether to include each study based on the eligibility criteria. Subsequently, we collectively cross-checked the studies read by the other authors. The author not initially involved in full-text reading performed the final screening and resolved conflicts. 



<!-- Start of picture text -->
Ident i f i cat i on of stud i es v i a databases and reg i sters Ident i f i cat i on of stud i es v i a other methods<br>Scopus Google Scholar Records removed  before<br>(n  =  1396) (n  =  648) screening (n  =  572) : Records  i dent i f i ed through c i tat i on  Records removed<br>Records  i dent i f i ed through database  Dupl i cated removed  (n  =  488) track i ng on January 13, 2025     before screening (n  =  101) :<br>search i ng on January 7, 2025  No author  (n  =  84) (n  =  420)  Dupl i cated removed  (n  =  101)<br>(n  =  2044)<br>Records screened on  Records  excluded Records screened on  Records  excluded<br>t i tle + abstract + publ i cat i on year (n  =  1349) t i tle + abstract (n  =  268)<br>(n  =  1472) (n  =  319)<br>Records sought for  retr i eval Records  not retrieved Records sought for  retr i eval Records  not retrieved<br>(n  =  123) (n  =  2) (n  =  51) (n  =  0)<br>Records assessed on  Records  excluded Records assessed on  Records  excluded<br>t i tle + abstract + full paper (n  =  51) t i tle + abstract + full paper (n  =  18)<br>(n  =  121) (n  =  51)<br>Stud i es  i ncluded  i n the  rev i ew<br>(n  =  103)<br><!-- End of picture text -->

Figure 2: Literature identification, screening, and inclusion activities conducted following the PRISMA guidelines. 



<!-- Start of picture text -->
i dentElcr i g ii terf ii bcat ii la  i ty  i on i dentDBs  i f i cat i on IdentKeywords  i f i cat i on checkCross  i ng<br>(January 7,  DB record collection  2025) cleaning records of DB Data  title + abstract Screening on + publication year of DB records record collection (January 13,  Cit. tracking  2025) of cit. tracking Data cleaning records cit. tracking recordsScreening on title + publication year of abstract +  Screening 1/3 of the studies on full text<br>Screening 1/3<br>of the studies<br>on full text<br>Screening 1/3<br>of the studies<br>on full text<br>F i nal screen i ng<br>and confl i ct<br>resolut i on<br><!-- End of picture text -->

Figure 3: BPMN diagram describing the identification and selection activities of records in the literature collection process. 

7 

LLMS FOR COMBINATORIAL OPTIMIZATION 

DA ROS ET AL. 

## **5.3.2 Identification** 

On January 7, 2025, we searched two popular databases to identify records: Scopus and Google Scholar. Scopus is an extensive, multidisciplinary database of peer-reviewed literature, while Google Scholar allows for broader searches, including pre-prints and other types of studies. 

To identify studies addressing the usage of LLMs within CO, we used the following set of keywords: “large language models”, “generative artificial intelligence”, “GPT”, “optimization”, “combinatorial optimization”, “mathematical formulations”, “metaheuristics”, “constraint programming”, “integer programming”, “integer linear programming”, “NL4Opt”, “Ner4Opt” . These keywords were combined into 14 search queries, reported in Table 1 along with the number of matches found for each query. Besides the self-explanatory queries (i.e., those including the relevant LLM and CO terms like “combinatorial optimization”), we also include the keywords “NL4Opt” and “Ner4Opt” in our Google Scholar search. These terms relate to a recent competition focused on extracting the meaning and formulation of an optimization problem from its textual description. Note that Google Scholar only provides an estimated number of matches and that we used the advanced query functionality on Scopus to restrict the search to study titles, abstracts, and keywords using the `TITLE-ABS-KEY(...)` construct. Using these queries, we retrieved approximately 648 records from Google Scholar and 1,396 from Scopus, for a total of 2,044 records. This list required further processing because both databases contain duplicates. We found 269 duplicate records from Google Scholar, 196 from Scopus, and 23 shared records, totaling to 488 duplicates. Another case to consider is a small subset of records that lack an author string and should, therefore, be removed from the list of 2,044 records. Specifically, we identified 4 records without an author string on Google Scholar and 84 records on Scopus. When combining the two lists, the number of distinct records without an author string is 84, as all four records found on Google Scholar are also present on Scopus. The final number of distinct records from Google Scholar and Scopus is 1 _,_ 472. 

Table 1: <u>Queries used to retrieve records from Scopus and Google Scholar.</u> 

|**Scopus**||**Google Scholar**||
|---|---|---|---|
|Query|Count|Query|Count|
|"large language models" and "optimization"|944|"large language models" and "combinatorial opti-<br>mization"|334|
|"GPT" and "optimization"|394|"large language models" and "constraint program-<br>ming"|104|
|"large language models" and "constraint programming"|10|"large language models" and "mathematical formu-<br>lations"|106|
|"large language models" and "integer programming"|14|"large language models" and "metaheuristics"|88|
|"large language models" and "integer linear programming"|15|"NL4Opt"|11|
|"generative artificial intelligence" and "combinatorial opti-<br>mization"|0|"Ner4Opt"|5|
|"large language models" and "combinatorial optimization"|14|||
|"GPT" and "combinatorial optimization"|5|||



## **5.3.3 Screening** 

We define 8 eligibility criteria to screen the list of studies referred by the 1,472 records retrieved. Specifically, we define 4 inclusion (INCL) criteria and derive 4 exclusion (EXCL) criteria: 

- INCL1 The study is written in English. 

- INCL2 The study focuses primarily on the usage of LLMs in the field of CO. 

- INCL3 The study has been published in 2016 or later. 

- INCL4 The study is in the form of a research article, a case report, a technical note, a narrative review, a systematic review, a position paper, a pictorial essay, or a PhD Dissertation. 

- EXCL1 The study is written in languages other than English. 

- EXCL2 The study focuses primarily on optimization in the context of LLMs, solely on CO, solely on LLMs, or solely on optimization different from CO, such as Continuous Optimization. 

- EXCL3 The study has been published in 2015 or earlier. 

8 

LLMS FOR COMBINATORIAL OPTIMIZATION 

DA ROS ET AL. 

- EXCL4 The study is not in the form of a research article, a case report, a technical report, a narrative review, a systematic review, a position paper, a pictorial essay, or a PhD Dissertation. 

In summary, we focus on how LLMs are used in optimization, specifically targeting studies that address the subfield of CO (INCL2); consequently, we exclude those taking the opposite perspective (EXCL2). Note that some of the exclusion criteria may appear redundant w.r.t. the inclusion ones; this is due to a rigorous application of the PRISMA guidelines in reporting on our activity of review. 

The formulation of these criteria is based on the concept of “primary focus” on the use of LLMs in the field of CO. According to our criteria, a study focusing on the use of LLMs in COPs should either: 

- _(i)_ Describe the usage of LLMs within one of the tasks of the overall optimization process. 

- _(ii)_ Address specific aspects of a COP. 

- _(iii)_ Propose improvements or new approaches for a given optimization paradigm. 

- _(iv)_ Outline use cases, perspectives, and/or potential future applications. 

- _(v)_ Involve specific LLMs and, if applicable, provide metrics and/or reference datasets. 

We believe that this notion of “primary focus” allows us to consider not only research papers but also reviews and surveys, which are equally important as they may provide general directions and perspectives (INCL2 and INCL4). This also helps clarify the rationale behind EXCL2 and EXCL4; if any of the components described above is missing, we exclude the study from consideration. For example, let us hypothesize a study on how an LLM could enhance an evolutionary procedure for solving a COP; this study would align with our inclusion criteria. Conversely, consider a study proposing the use of a MH to generate prompts for LLMs; such a study would not meet our criteria and would be excluded. Concerning the criteria for the publication year (INCL3/EXCL3), we selected 2016 as the earliest publication year to ensure comprehensive coverage for our systematic review. This choice aligns with key developments in LLMs, particularly following the “Attention Is All You Need” paper [220], which introduced the Transformer architecture in 2017 (Section 4.1) 

Regarding the types of publications considered, we have identified a subset that aligns with our objectives (INCL4). We therefore exclude all other publication types not specified therein (EXCL4). 

We screened the identified records (1,472) according to our eligibility criteria. We removed 68 records because they were published earlier than 2016 (INCL3/EXCL3). A total of 1227 records tackled solely LLMs, solely optimization, or a type of optimization different from CO. Additionally, we excluded 47 records that addressed optimization in the context of LLMs (INCL2/EXCL2). We also removed 7 records because they referred to studies of the wrong type (EXCL4). In total, we removed 1,349 records, resulting in a final count of 123 records. 

On January 13, 2025, we performed citation tracking [36] on the 123 records that remained after the initial screening. Specifically, we traced all the citations received by the collected studies referred to in the records, identifying a total of 420 records. We then checked for duplicates in this set, identifying 101 duplicates. Thus, we ended up with 319 distinct records from citation tracking. 

We manually addressed each record, evaluating them according to our criteria as we did previously. Among the 319 distinct records, we found that 251 tackled solely LLMs, solely optimization, or a type of optimization different from CO (EXCL2). Additionally, 11 records referred to studies that tackled optimization in the context of LLMs. We excluded 5 records because they referred to studies of the wrong type (EXCL4) and 1 study because it was not written in English (EXCL1). In total, we removed a total of 268 records, leaving us with 51 records. By examining these citations, we uncovered additional highly related or complementary sources w.r.t. the initial set of records, thereby broadening and enriching our literature review. 

In summary, combining the records retrieved through databases (123) and those obtained through citation tracking (51), we had a total of 174 records. 

## **5.3.4 Inclusion** 

We read the full text of each of the 174 studies referred to by the records obtained after the screening activity to decide which ones to include in our systematic review. This involved a more thorough evaluation of each study concerning our eligibility criteria. Below are a few examples: 

- Amarasinghe et al. [8] proposed to automate the formulation of optimization problems from NL descriptions, using fine-tuned LLMs to generate modular code for complex real-world business optimization scenarios. In this study, LLMs are used to enhance the formulation of a COP, thereby satisfying all our inclusion criteria. 

9 

LLMS FOR COMBINATORIAL OPTIMIZATION 

DA ROS ET AL. 

- Pluhacek et al. [171] used an LLM to identify and decompose six well-performing swarm algorithms for continuous optimization. Despite the involvement of LLMs, we exclude this study because it focuses exclusively on continuous optimization problems (EXCL2). 

- Wang et al. [227] proposed a survey on the usage of Deep Generative Models (DGMs) for COPs. We exclude this study since DGMs are not LLMs (EXCL2). 

Thus, the final number of studies included in this systematic review is 103 (i.e., 2 studies were not retrieved and 69 were not included as per inclusion/exclusion criteria, thus 174 = 103 + 2 + 69). 

Table 2 summarizes the characteristics of the included studies. Please note that when feasible, the characteristics reported are those of the peer-reviewed version of the studies, i.e., if a study was previously published in a pre-print form and later in a peer-reviewed version, we consider the latter here. The majority (82 studies, 80%) were published in 2024. The remaining studies were published in 2023 (17 studies, 16%) and in 2022 (4 studies, 4%). Considering their identification approach, 70 (68%) were retrieved from databases; additionally, we included 33 (32%) studies referred to by records found through citation tracking. Regarding the publication venues, approximately 50 studies (49%) were disseminated through pre-print distribution services such as arXiv. The remaining studies were peer-reviewed, with 25 (24%) published in journals and 28 (27%) in conference proceedings. Focusing on the type of each study, as specified in our inclusion criteria (INCL4), 84 of them (approximately 82%) are research studies addressing specific research questions and/or experimental settings. Additionally, we included 11 (10%) literature reviews, one (1%) technical report, and 7 (7%) position papers, as these provide perspectives, guidelines, or future directions. 

Table 2: Overview of the 103 studies included in our review. 

|**Year**|**Total**|**Idei**|**ntification**||**Venue**|||**Publicati**|**on Type**||
|---|---|---|---|---|---|---|---|---|---|---|
|||DB|Citation<br>Tracking|Journal|Confer-<br>ence|Pre-print|Research|Review|Report|Position|
|2022|4|3|1|0|1|3|4|0|0|0|
|2023|17|16|1|3|4|10|15|0|1|1|
|2024|82|51|31|22|23|37|65|11|0|6|
|**Total**|103|70|33|25|28|50|84|11|1|7|



# **6 Analysis** 

In this section, we classify and discuss the 103 studies. The analysis is conducted in terms of optimization process, LLMs, benchmark datasets, and application domain. Each selected study is described in Appendix B. 

## **6.1 Optimization Process** 

In this section, we report the analysis of the included studies w.r.t. the optimization process, both considering the general task (e.g., problem modeling) and the related activities (e.g., domain knowledge). A detailed tabular overview is available in Appendix C. 

This analysis accounts for 86 out of the 103 studies (83%). The omitted studies provide perspective and general direction on the topic (Section 6.5). In the counts related to the number of studies per step or task, a study addressing multiple tasks within the same step is counted only once for that step. For instance, Li et al. [116] addresses both entity recognition and model creation within the problem modeling step. Therefore, it is counted as 1 in the problem modeling step. If a study addresses multiple steps, it is counted as 1 in each step. For instance, Tsouros et al. [214] addresses activities both in the problem modeling and solution method steps, thus it is counted as 1 in each of them. Most of the studies (64 out of 103) focus on activities related to the solution method, representing 63% of the total. The problem modeling task follows closely, with 38 studies, accounting for 37%. A limited number of studies are related to benchmarking (7, 7%) and validation (9, 9%). In the following sections, we outline how LLMs are used within each step of the process. 

The optimization process could benefit from the application of LLMs in several ways, as advocated by Wasserkrug et al. [228], who argues for their integration throughout the entire process. While such a holistic approach is possible, only 24 studies (23%) address multiple steps across the pipeline. 

10 

LLMS FOR COMBINATORIAL OPTIMIZATION 

DA ROS ET AL. 

## **6.1.1 Problem Modeling** 

Problem modeling aims to translate problems, expressed in NL, into mathematical and computational models. This step is foundational, as the quality of the models influence the success of optimization. 

A specialized understanding of the domain in which the COP is located is crucial for effective modeling and for ensuring realistic and applicable solutions. Traditionally, human experts are necessary in this phase as they bring deep knowledge of industry-specific rules, regulations, etc. In such context, LLM can help by extracting implicit knowledge from the real-world data and integrating it into solution processes [40, 131, 188, 253] and to generate solutions [37, 39, 95]. Li et al. [119] integrates the domain knowledge, with both entity recognition and the generation of solution code. 

In the given problem context, it is crucial to identify the key entities and their interrelations to properly model variables, constraints, and objectives. LLMs can be particularly useful for recognizing and labeling these elements within a NL description of the problem [47, 224]. This capability can enhance the accessibility and usability of the models, enabling non-domain experts to solve significant problems across various industries. Such activity is frequently paired with the extraction of domain knowledge [6, 216], the creation of the model [4, 45, 74, 89, 116, 156, 157, 179], and toward code generation [87, 119]. Note that Obata et al. [157] also addresses solution generation. As mentioned, LLMs can produce optimization models [58, 181] and assist users in doing so, as evidenced, for instance, by the conversational agents developed by Abdullin et al. [1]. The generation of an optimization model is often accompanied by the production of the related code [82, 94, 111, 238]. Several studies have jointly addressed entity recognition, model creation, and code generation [2, 3, 71, 92, 96, 152, 214, 240, 248], with Michailidis et al. [146] also addressing solution generation. 

A total of 38 studies focused on problem modeling, encompassing the identification of domain knowledge (11 studies), entity recognition (25 studies), and model creation (25 studies). 

## **6.1.2 Solution Methods** 

Solution methods refer to strategies and algorithms used to find (near) optimal solutions to COPs. The choice of the solution method is linked to the problem model and is deemed critical, as it determines the efficiency, scalability, and accuracy of the results. Thus, optimization researchers’ expertise is essential to select the right solving strategy and to design algorithms and their components. LLMs have been adopted in the design of solution methods, especially through code generation; there exists one case where LLMs have been used for algorithm selection [237]. Complete algorithms have been designed starting from NL description of solution methods for CP [8, 222] and MILP [7, 114, 118]. Liu et al. [127] and van Stein et al. [198] used LLMs to generate heuristic algorithms within an evolutionary framework, with the latter also including in the loop parameter tuning using an automated tool (SMAC [122]). On the contrary, a few studies implemented a LLM-based parameter tuning [63, 110, 143, 218]. Ye et al. [243] and Liu et al. [125] developed heuristics for a hyper-heuristic framework. Romera-Paredes et al. [184] introduced FunSearch, a method for discovering new heuristics for the online bin packing problem, achieving improvements over widely used baselines. Following, many other studies tackled the topic of generating code for heuristics [30, 127, 129, 201, 241, 242, 245, 250]. Mao et al. [142] integrated LLMs into mutation and crossover operators for GAs. Most of the generated code is written in Python (30, note that overall 35 studies use Python). 

Generating solutions that satisfy the constraints and are diverse enough is complex and sometimes even unfeasible [221]. LLMs have been asked to directly produce solutions [19, 32, 52, 63, 69, 80, 81, 86, 93, 115, 124, 130, 147, 153, 182, 183, 187, 213, 226, 239, 244]. Such an approach is useful, for instance,in MHs, where complete solutions are required as a starting point or to be mutated during the evolutionary process, and in population-based optimization algorithms, where a large number of (possibly diverse) solutions are required at each iteration. Finally, code generation and solution generation have been tackled together by 2 works [20, 98]. 

A total of 64 studies focused on solution methods, encompassing code generation (36 studies), solution generation (28 studies), parameter tuning (4), and algorithm selection (1). 

## **6.1.3 Validation** 

The validation step ensures that the model, the code, and the produced solutions align with the problem requirements and meet end-users’ needs. This process often requires substantial human input, as domain experts are typically involved in an iterative feedback loop to critically review the models and solutions to verify that all specifications have been adequately addressed. As LLMs have been proven to perform fairly well in such tasks [189], they have also been applied to optimization. Huang et al. [87] employed an LLM to validate solutions in an end-to-end framework (spanning from problem modeling to technical validation). Conversely, Hao Chen and Li [72] acted at the model level, employing a LLM agent to validate the (MI)LP models. Specifically, they integrated LLMs in diagnosing inconsistent (i.e., over-constrained) MILP optimization models, trying to isolate the minimal subset of linear constraints (including 

11 

LLMS FOR COMBINATORIAL OPTIMIZATION 

DA ROS ET AL. 

variable bounds) that makes the model instance infeasible. Validation has also been addressed by other studies, reported also in other steps of the optimization process [52, 71, 115, 152, 238, 248]. Note that we do not address bug checks in LLM-generated code as proper technical validation (e.g., during code generation for the solution method step) since we assume such checks are inherently part of that activity (if not state otherwise). A total of 9 study focused on validation (5 on solution validation and 6 on model validation). 

## **6.1.4 Models and Algorithm Types** 

Since the optimization process can be clearly outlined in terms of tasks and steps, it is crucial to recognize that modeling choices, solution methods, and validation procedures are closely interconnected. This section presents an overview of the algorithms and solvers considered in the studies. Please refer to the sections related to the single steps. 

Considering the underlying model and algorithm type, the majority of studies (19) focus on LP and MILP (18). Other exact methods involve CP (7) and ILP (2). (Meta-)Heuristic algorithms account for 20 studies; among them, 9 focus on heuristics, 3 focuses on hyper-heuristics, 3 on GAs, and 3 on EAs. Furthermore, 3 study explores the capabilities of LLM w.r.t. multi-objective CO [124]. One study deals with SAT – even though LLMs are used to generate heuristics for their solution [201]. 

One reason for the prominence of LP in these studies is the Natural Language for Optimization Modeling (NL4Opt) competition. The primary objective of this competition was to assess whether models could generalize to unseen problem domains, with an emphasis on two sub-tasks: named entity recognition for LP components and LP model generation. For more detailed information on the competition, readers are forwarded to the report by Ramamonjison et al. [180], while a description of the related dataset is provided in Section 6.3. 

## **6.1.5 Benchmarking** 

In CO, benchmarking involves evaluating and comparing the performance of algorithms and techniques. The objective is to determine how effective a solution method is and, potentially, understand the reasons behind its performance. Conventional comparison methods involve gathering numerical data from algorithm runs and reporting them in the form of tables and boxplots, alongside considerations of computational times and statistical tests (such as the Friedman test) to account for stochasticity. For decades, researchers have emphasized the need for additional tools to better understand the behavior of optimization algorithms [18]. One such tool is related to Search Trajectory Networks (STNs), a graph-based tool for the visualization of MH behavior [159]. While these visualizations are very informative, they require prior knowledge to be produced (e.g., parameters for search space partitioning) and interpreted (e.g., which algorithm is superior). To bridge this gap, Chacón Sartori et al. [28] enriched STNs with LLM-generated explanations and suggestions. 

The visual investigation of solutions is enabled by Da et al. [37], who also allows solution validation. The visual capabilities of LLM are also explored by Elhenawy et al. [52], who directly employ them to solve problems, presenting instances in visual form. 

An increasingly relevant topic in CO is explainability of results [204] as a way for enhancing confidence and trust in the solutions. Interesting questions include identifying which solution components most significantly influence the final result and understanding the characteristics of high-quality solutions, among others. Providing informative answers to these questions requires in-depth knowledge of the application domain, the solution method, and the specific instance being addressed. To reduce this human-intensive task, Kikuta et al. [99] proposed a post hoc LLM-based explanation framework aimed at clarifying the decision-making process of Vehicle Routing Problems (VRPs). Similarly, also other study included an explainability level [80, 183]. 

A total of 7 studies focused on benchmarking (3 on visual analysis and 4 on explainability). 

## **6.2 Large Language Models** 

The LLMs available today exhibit different capabilities: some are designed for processing instruction-like prompts, others specialize in generating programming code, etc. Understanding the role of each LLM in the reviewed studies is valuable for developing future approaches to solving COPs, complementing the findings in Section 6.1. 

The 70 LLMs used in the 103 studies are based on 22 different architectures. Despite the diverse capabilities of the architectures employed, most LLMs have been used in CO to enhance problem modeling and solution methods. In the following, we provide a description of how LLMs are used within the included studies, considering their architectures, general tasks, and related activities. Note that the numbers for activities may not sum to those at the main task level, as 

12 

LLMS FOR COMBINATORIAL OPTIMIZATION 

DA ROS ET AL. 

a given LLM can be used for multiple purposes. For a tabular overview of the LLMs, we refer the interested reader to Appendix D. 

## **6.2.1 LLM Architectures** 

13 out of the 22 architectures focus on generative approaches. Introduced in 2022, `GPT-3.5` [21] is particularly effective for tasks requiring fluent text generation. `GLM` [51] emerged as a balanced approach to generative tasks, leveraging both bidirectional and autoregressive capabilities. During 2023, several architectures were released: `LLaMa 2` [62], optimized for efficiency and suitable for tasks involving scalability and quick inference times; `PaLM 2` [66], which performs strongly in scenarios requiring comprehension and contextual text generation; `Mistral` [90], designed for efficient inference and competitive performance in text generation, making it suitable for resource-constrained deployments; and `Qwen` [175], focusing on general-purpose text generation with multilingual support and fine-tuned reasoning capabilities. In the same year, `GPT-4` [160] appeared as a particularly strong model for fluent text generation, alongside `LLaMa 3` [132], which is optimized for instruction-following and structured text understanding. `DeepSeek` [41] also adopts generative approaches with a particular focus on the Chinese language, while `Claude 3.5` [10] excels in dialogue-based applications and knowledge-intensive tasks. `Qwen2` [176] extends its predecessor with multilingual capabilities and refined reasoning. `Cohere` ’s `Command-R+` [5] is optimized for Retrieval-Augmented Generation (RAG), improving factual accuracy and knowledge recall. Finally, `Yi` [210] is tailored for diverse text generation tasks, integrating efficient training strategies for improved performance. A total of 62 studies rely on these architectures, namely 24 on `GPT-3.5` (2022), 2 on `GLM` (2022), 9 on `LLaMa 2` (2023), 3 on `PaLM 2` (2023), 2 on `Mistral` (2023), 3 on `Qwen` (2023), 43 on `GPT-4` (2023), 7 on `LLaMa 3` (2024), 6 on `DeepSeek` (2024), 7 on `Claude 3.5` (2024), 1 on `Qwen2` (2024), 1 on `Cohere` (2024), and 1 on `Yi` (2024). 

A total of 5 architectures are designed to handle textual input. `T5` [178] (2019) treats all text-based tasks as text-to-text problems, offering significant flexibility across a range of natural language processing applications. `BART` [113] (2019) is particularly effective at transforming textual input into structured outputs, making it suitable for complex textual tasks. `UnixCoder` [68] (2022) is an architecture specialized in programming-related tasks, such as code generation, code summarization, and code translation. Additionally, `LLaMa 2` [62] (2023) and its successor, `LLaMa 3` [132] (2024) provide LLMs optimized for instruction-following (e.g., `LLaMa 3-70B-Instruct` ) and are fine-tuned for tasks requiring structured text understanding. A total of 9 studies rely on these architectures: 3 on `T5` (2019), 3 on `BART` (2019), 1 on `UnixCoder` (2022), 1 on `LLaMa 2` (2023), and 1 on `LLaMa 3` (2024). 

Additionally, 4 architectures focus on multimodal data. All these architectures (or their multimodal models) were introduced in 2024. `Gemini` emphasizes both multimodal capabilities and generative approaches, making it ideal for tasks that require integrating and generating text, images, and possibly other forms of data. `GPT-4-Vision-Preview` extends the `GPT-4` [160] architecture by incorporating visual input processing, allowing it to handle tasks involving image understanding and text-image reasoning. `Mixtral` [91] leverages an ensemble of models designed to handle multimodal tasks, such as text-to-image and image-to-text conversions. `OpenCoder` [83] is optimized for code-related tasks and supports multimodal inputs, particularly focusing on enhancing software development workflows with a combination of textual and structural data processing. A total of 9 studies rely on these architectures: 5 on `Gemini` , 2 on `Mixtral` , 1 on `GPT-4` , and 1 on `OpenCoder` . 

At the time of writing, several LLMs analyzed in this study have been deprecated or replaced by newer versions. OpenAI’s `Text-Davinci-003` and `Text-Davinci-Edit-001` , based on `GPT-3.5` , have been phased out in favor of `GPT-4-Turbo` and `GPT-4o` . Google rebranded `Bard` as `Gemini` , transitioning from `PaLM 2` to the `Gemini 1.x` and `2.x` series. Meta’s `LLaMa 2-13B` has been largely replaced by `LLaMa 3` , while OpenAI’s `GPT-4` evolved into `GPT-4o` , incorporating multimodal capabilities. Similarly, `Mixtral-8x7B-Instruct-v0.1` , `Qwen` , and `DeepSeek` have advanced to `Mixtral` , `Qwen2` , and `DeepSeek-V2` , respectively. Anthropic’s `Claude 3.5` is also expected to be succeeded by newer iterations. Given the rapid evolution of LLMs, readers should consider the latest available models when interpreting our findings. 

Given the varying performance of LLMs across architectures, access to their source code remains a key issue to be analyzed. Most high-performing models, including OpenAI’s `GPT-3.5` and `GPT-4` , Google’s `PaLM 2` and `Gemini` , as well as Anthropic’s `Claude 3.5` and Cohere’s `Command-R+` , are closed source and require paid access. `Mixtral` , while open-weight, is commercialized via paid APIs, and `DeepSeek V2` adopts a more restrictive licensing model. In contrast, Meta’s `LLaMa 2` and `LLaMa 3` are open source under specific licenses, while Mistral AI offers both open-weight and commercial models. `Qwen` and `Qwen2` provide open-source variants alongside proprietary versions. Fully open-source models include `BART` , `T5` , and certain versions of `LLaMa` , `Mistral` , `StarCoder` , and `OpenCoder` (the latter two specialized for code generation). Given the evolving nature of access policies and licensing conditions, these constraints may influence model selection in research. 

13 

LLMS FOR COMBINATORIAL OPTIMIZATION 

DA ROS ET AL. 

We count separately both specific implementations designed for conversational purposes and versions of the same model updated to a specific timestamp, such as `GPT-4-0613` (referring to a version of `GPT-4` released or fine-tuned on June 13, 2023). This approach aims to enhance clarity and improve reproducibility. However, there is no guarantee of consistent responses even when using different versions of the same models [56, 103], especially since chat completions are not deterministic by default [161]. 

When using LLMs in a research setting, several key aspects must be addressed to ensure both reliable and reproducible results. Documenting the exact prompts used is crucial, as LLMs are highly sensitive to prompt variations, which can lead to significantly different outcomes [9, 16]. Additionally, detailed reporting on the model version, configuration, and any fine-tuning is essential for accuracy and replicability. Notably, a limited number of studies (7) that conducted experiments in this area did not provide any details about the LLM employed [45, 131, 146, 153, 157, 181, 218]. Understanding the training data used in an LLM can help identify potential data leakage, biases, or knowledge gaps that might affect results [13]. Moreover, documenting any additional steps, such as data preprocessing or post-processing of model outputs, is critical for ensuring that findings can be replicated across different studies and datasets. By addressing these factors, research involving LLMs remains transparent, reproducible, and robust. 

Finally, when evaluating LLMs in the context of COPs, no universally shared metrics emerge. Accuracy is the most commonly used metric, but its interpretation varies by task. Researchers sometimes define a problem-specific “score”, while other metrics remain domain-specific. Indeed, many studies evaluate LLMs based on the objective values of the solutions they produce. As discussed in Section 4.2, this evaluation is problem-specific, as each problem has distinct objective functions. For instance, in TSP, the goal is to minimize travel distance, whereas in PFSP, it is typically to minimize tardiness or completion time. Since the optimal solution may not always be available, evaluations often compare the obtained solutions to the best-known ones. A common metric for this comparison is the optimality gap (or relative deviation), calculated as: gap = 100 _×_ ( _Z_ llm _− Z_ best) _/Z_ best where _Z_ llm represents the objective value of the LLM solution, and _Z_ best denotes the best-known objective value. 

## **6.2.2 Problem Modeling** 

A total of 40 LLMs out of 70 (57%) have been used for problem modeling. Among them, 19 LLMs have focused on enhancing _model creation_ . A common approach involves creating models from unstructured NL. Some of these approaches address optimization problems more broadly, utilizing LLMs such as `GPT-3.5-Turbo` (an optimized variant of `GPT-3.5` for faster performance and lower cost [238]), `GPT-3.5-turbo-0613` (a June 2023 release of `GPT-3.5-Turbo` ), `GPT-4-0613` (a June 2023 release of `GPT-4` ), and `GPT-4` itself [94], as well as `LLaMa 2-7b` , a version of `LLaMa 2` with 7 billion parameters [4], and `T5-Base` , the base model built on the `T5` architecture [74]. Additional optimized or specialized variants, including `GPT-4o` , an improved multimodal version of `GPT-4` [2], `Qwen1.5-14B` , `DeepSeek-V2` [240], `Mistral-7B` , `DeepSeek-Math-7B` , `LLaMa 3-8B` , and `Qwen2.5-7B` [82], have also been used for broad optimization tasks, leveraging improved reasoning capabilities and efficiency. Moreover, instruction-tuned models such as `Code Llama-Instruct` and `Zephyr-7b-beta` , a `7B` -parameter model designed for instruction-following, have been used for structured task execution [152]. Furthermore, both `GPT-4o` and `Claude 3.5 Sonnet` have been employed in a zero-shot fashion to generate problem formulations directly from user input, thus reducing the need for extensive prompts or examples [71]. Other approaches focus on specific formulations. For instance, LLMs have been used to automate the generation of LP models with `ChatGPT-3.5` [116], `GPT-4` [1], and the `BART` architecture, including both `BART-Base` [58, 179] and `BART-Large` variants [58, 89]. Furthermore, `ChatGPT-3.5` has also been employed in MILP problems [8], as have `Bard` , a conversational model built on the `PaLM-2` architecture [116], and `LLaMa 3-70B` [96]. Instruction-tuned `Code Llama-Instruct` and `Zephyr-7b-beta` have likewise been applied to Quadratic Programming (QP) tasks by translating user directives into valid constraints and objective functions. 

Concerning _entity recognition_ , 22 LLMs have been used to identify and extract specific elements from model representations. Specifically, `GPT-4` and `Text-Davinci-003` , based on `GPT-3.5` and optimized for a wide range of tasks, have been used to translate user input into constraints that the underlying CP model can process [111]. This approach has also been applied to LP and MILP problems using `GPT-3.5` [3, 248], `GPT-4` [248], `ChatGPT-4` [6], `LLaMa 3-70B` [2, 96, 152], `ChatGPT-4o` [2, 71, 92], and `Claude 3.5 Sonnet` [71]. Meanwhile, `CodeLlama-Instruct` and `Zephyr-7b-beta` have also been used for QP problems. Additionally, `ChatGPT-3.5` and `Bard` have been used exclusively for MILP [116], while `T5-Base` has been employed for LP [74]. Furthermore, several LLMs have been applied to general optimization problems, including `GPT-3.5-Turbo-0163` , `GPT-4` , `LLaMa 2-7b` , `LLaMa 2-13b` , and `LLaMa 3-70B` [4, 37], as well as `GPT-4o-mini` [119], `BART-Base` , `BART-Large` [89, 179], and `Gemini 1.0 Pro` [87]. 

Additionally, there are 12 applications of LLMs for extracting _domain-specific knowledge_ . For instance, `GPT-4` and `GPT-4-0163` have been used to extract general domain knowledge in household financial planning [40, 96]. `GPT-4o` , 

14 

LLMS FOR COMBINATORIAL OPTIMIZATION 

DA ROS ET AL. 

`Claude 3.5 Opus` , `Command-R+` , and `Mixtral-8x2B` have been applied to a social network problem [188], and `GPT-4o` has also been used in robotics [147]. `LLaMa2-7B` , `LLaMa2-13B` , `GPT-3.5` , and `GPT-4` have been employed to model knowledge for the VRP problem [37]. Moreover, a single LLM, `ChatGPT-4` , has been used to model domain knowledge in the form of knowledge graphs [216]. 

## **6.2.3 Solution Methods** 

LLMs has been employed in 60 out of 70 (85%) works for what concerns the solution method task. Specifically, 23 LLMs have been used for _solution generation_ . One approach involves creating candidate solutions for well-known COPs, such as a specific class of the VRP, by leveraging both GPT-based models like `GPT-4` [3], `GPT-4-Turbo` , and `GPT-4o` [98], and LLaMa-based or T5-based models, including `LLaMa 2` and `T5-Base` [32]. Another approach uses LLMs to combine problem descriptions and previously generated solutions within a meta-prompt processed by `ChatGPT-3.5-Turbo` , `PaLM 2-L` , `PaLM 2-L-IT` , and `text-bison` [239]. The multimodal capabilities of `GPT-4-Vision-Preview` and `ChatGPT-4o` have also been employed to generate solutions through visual prompts [52, 86]. Moreover, `ChatGPT-4` has been adopted for finance-related solutions [183] or automated sequence planning in robot-based assembly [244]. Other LLMs used for domain-specific problems include `GPT-4` for travel planning [39], program scheduling [95], and traffic simulation [37]. `LLaMa 2-7b` and `LLaMa 2-13b` have also been applied to traffic simulation. `Claude 3.5 Sonnet` has been used in molecular biology [182], and `ChatGPT-4-Turbo` together with `ChatGPT-4o-mini` has been used to coordinate computation in a graph reasoning scenario [80]. `GPT-3.5-Turbo` has found utility in industry-related problems [238], while `GPT-4-Turbo` , `GPT-4o` , `Gemini 1.5` (Pro and Flash), and `Gemma 2 27B` have been employed in planning tasks [19, 147]. Furthermore, in the context of GAs, `GPT-3.5-Turbo-0613` has been used to select parent solutions from the current population and perform crossover and mutation [130], as well as to perform mutation and crossover only [142]. 

Additionally, 35 LLMs leverage approaches for _code generation_ . `GPT-3.5` , `GPT-4` , `GPT-4o` , and `Qwen (LoRA Fine-Tuned)` , which is a version of the `Qwen` family fine-tuned using LoRA [79], have been used to generate code specifically for LP, Mixed Integer Programming (MIP), and MILP approaches to COPs [3, 94, 118, 248], whereas `CodeLlama-Instruct` and `Zephyr-7b-beta` have been applied to both MILP and QP [152]. Various methods for automating the generation of heuristic algorithms rely on a range of LLMs, each optimized for different aspects of code generation. For example, `CodeLlama` , a code-oriented variant of `LLaMa 2` [250], and `StarCoder` , trained on extensive code-related datasets, are fine-tuned for specific programming tasks, while `DeepSeek-LLM-7B-Base` , `GPT-3.5-Turbo` , and `GPT-4-Turbo` are optimized for speed and efficiency [96, 124, 125, 127, 129, 184, 241, 243, 245]. `GPT-3.5-Turbo-0613` has likewise been employed for generating crossover and mutation implementations in Python [142] within EA contexts. Multimodal models, such as `GPT-4o` , and advanced reasoning models like `Claude 3.5 Opus` and `Claude 3.5 Haiku` , have also been utilized in heuristic generation tasks, and `DeepSeek-Coder` along with its updated `DeepSeek-Coder-V2` focus on high-performance code synthesis. Similarly, `GLM-3-Turbo` , `OpenCoder-8B-Instruct` , and `Yi-34b-Chat` provide structured, optimized code generation [129, 242]. For large-scale problem-solving, models such as `Gemini 1.0 Pro` and `Codey` , both built on `PaLM 2` , have shown strong performance in complex coding scenarios, while the latest iterations of foundation models (e.g., `LLaMa 3-70B` , `LLaMa3-70B-Instruct` , `LLaMa 3.1-8B` , `GPT-3.5-Turbo` , `GPT-4o-Mini` , and `Qwen-Turbo` ) have been refined for specialized programming applications [129, 242, 250]. Other approaches harness a self-reflection mechanism to directly generate executable Python code from natural language, exemplified by `GPT-4` and `Gemini 1.0 Pro` [87]. A comprehensive code-generating framework for business optimization has also been developed using `CodeT5-finetuned_CodeRL` [112], a model that employs reinforcement learning on top of `CodeT5` [8]. Additionally, `Text-Davinci-Edit-001` has been employed to generate MiniZinc-specific representations [7], while `Text-Davinci-003` and `GPT-4` have produced Gurobi-based code for supply chain optimization [114]. `GPT-3.5-Turbo` , `Mistral-7B` , `DeepSeek-Math-7B` , `LLaMA 3-8B` , and `Qwen2.5-7B` have been broadly used for industry-related problems [82, 238], and a specialized version called `GPT-4o-2024-08-06` has been introduced to optimize code for SAT solvers [201]. Moreover, `GPT-4o` and `Claude 3.5 Sonnet` have addressed supply chain and robot logistics tasks [71], and `ChatGPT-4o-mini` has been applied to multi-agent solution design [119]. 

Moving to _parameter tuning_ , we identified 5 applications of LLMs. `ChatGPT-4o` has been adopted to model user preferences by adjusting an optimizer’s weights [63], whereas `GPT-3.5` , `GPT-4` , `Gemini` , and `Le Chat` (the chatbot interface for Mistral models) have been used to set MHs parameters [143]. 

A single application aimed at enhancing _algorithm selection_ : `UnixCoder` , a code representation model designed for programming tasks, has been used to extract features linked to the underlying optimization algorithms [237]. 

15 

LLMS FOR COMBINATORIAL OPTIMIZATION 

DA ROS ET AL. 

## **6.2.4 Validation** 

We found 10 applications of LLMs out of 70 (14%), in the context of validation for optimization models. In particular, 7 LLMs have been involved in _solution validation_ . `GPT-4` and `Gemini 1.0 Pro` have been used to validate solutions generated for the VRP [87], while `GPT-3.5` , `LLaMa 2-7b` , `LLaMa 2-13b` , and `ChatGPT-4o` have been applied to broader validation tasks [37, 52]. Additionally, `Qwen (LoRA Fine-Tuned)` has been leveraged for solution validation [248]. 

As for _model validation_ , 9 LLMs have played a role. `GPT-4` has been employed to diagnose infeasible MILP models through interactive sessions [72], while `GPT-3.5-Turbo` has been used to validate models built from natural language [238]. Similarly, `GPT-3.5` , `GPT-4` , and `Qwen (LoRA Fine-Tuned)` have also been applied in this context [72, 248], with `GPT-4o` and `Claude 3.5 Sonnet` reported for model validation tasks [71]. In addition, code-focused models have been utilized to ensure correctness: `CodeLlama-Instruct` and `Zephyr-7b-beta` have been adopted to verify that the generated code remains consistent with the original model formulations [152]. 

## **6.2.5 Benchmarking** 

As for benchmarking, 9 out of 70 (14%) LLMs have been used to enhance it. Specifically, 8 LLMs use _visual analysis_ , as they are integrated, for instance, with a tool designed to visualize the behavior of various algorithms applied to specific instances of a COP [28]. The models used by Chacón Sartori et al. [28] include `Mixtral-8x7B-Instruct-v0.1` , which is optimized for instructional and guided tasks, `GPT-4-Turbo` , and `Tulu-v2-dpo-7b` , a fine-tuned version of `LLaMa 2` that was trained on a mix of publicly available, synthetic, and human-generated datasets using a parametrization of the RLHF algorithm known as Direct Preference Optimization [177]. Furthermore, `GPT-3.5` , `GPT-4` , `LLaMa 2-7b` , and `LLaMa 2-13b` have been employed to visualize solutions for a domain-specific problem [37], while `ChatGPT-4o` has been used to interpret visual inputs in lieu of purely numerical data [52]. 

We also identified 5 applications aimed at improving _explainability_ . `ChatGPT-4` has been employed to describe the decision-making process for the VRP [99], while `ChatGPT-4-Turbo` , `ChatGPT-4o` , `ChatGPT-4o-mini` , and `Claude 3.5 Sonnet` have been used for instances of both the TSP and mTSP [37, 63, 80, 182]. 

## **6.2.6 Platforms for Supporting LLMs-Based Approaches** 

While reviewing the studies considered for inclusion, we came across two platforms used by Chacón Sartori et al. [28] to support the design of their approach. Although these platforms are general-purpose and facilitate the use of LLMs broadly rather than specifically in the context of CO, we believe it is beneficial to describe them briefly. 

Chatbot Arena [31] is an open platform for evaluating LLMs based on human preferences. It offers access to over twenty LLMs, including both proprietary and open-source options, and provides a leaderboard to compare results. Chat2Vis [139], on the other hand, focuses on generating visualizations directly from natural language text. It uses various LLMs and shows that a set of proposed prompts offers a reliable approach to rendering visualizations from natural language queries, even when they are highly misspecified or underspecified. 

## **6.3 Benchmark Datasets** 

The methodologies proposed in the studies have been evaluated using well-known CO instances, related problem suits (e.g., MIPLIB<sup>3</sup> and ASLIB),<sup>4</sup> or datasets specifically developed for the case of LLMs. Considering this latter point, 29 studies assess the efficacy and efficiency of leveraging LLM within CO with specific benchmark datasets developed for this purpose. We now describe these datasets and report a tabular overview in Appendix E. 

The most frequently used benchmark dataset is the LPWP, also referred to as the NL4Opt dataset, which has been employed in 16 studies [1, 3, 4, 47, 58, 74, 82, 89, 92, 116, 146, 156, 179, 224, 238, 248]. Initially introduced by Ramamonjison et al. [179] and later expanded by Li et al. [116], this dataset has been used in the NL4Opt competition. The original dataset includes 4,216 NL problem declarations derived from 1,101 LP problems across six different domains. The extension enhances the dataset by introducing new problem descriptions and constraint types, such as logic constraints and binary variables. The second most used benchmark dataset is the ComplexOR dataset [238], which has been employed in 3 studies [3, 92, 238] and has been introduced to complement the NL4Opt dataset. The dataset consists of NL descriptions of 37 problems across different domains, sourced from academic studies and real-world scenarios, encompassing 25 LP formulations and 12 MILP formulations. As ComplexOR also the NLP4LP dataset [2, 3] has been used in 3 studies [2, 3, 92]. It encompasses NL descriptions of 67 problems across various domains 

> 3 `https://miplib.zib.de/` 

> 4 `https://www.coseal.net/aslib/` 

16 

LLMS FOR COMBINATORIAL OPTIMIZATION 

DA ROS ET AL. 

and including both LP (54) and MILP (13) formulations. This same dataset has been enriched to up to more than 200 optimization problems by AhmadiTeshnizi et al. [2]. Huang et al. [82] proposed OR-Instruct, a pipeline for creating synthetic data for optimization data. To test the capabilities of such a pipeline, they created IndustryOR, which has been used in 2 studies [82, 92]. As the name suggests, it focuses on industrial problems (a total of 100 real-world problems from eight industries) covering LP, ILP, MILP, and non-linear programming. Huang et al. [85] introduced Mamo, a dataset for LP modeling. It includes 652 easy and 211 complex LP problems, each paired with its corresponding optimal solution, sourced from various academic materials. Mamo has been used in 2 studies [82, 92]. Luo et al. [137] introduced GraphInstruct, a dataset comprising 21 reasoning problems on the topic of graphs and networks, including COPs. GraphInstruct has been used in 2 studies [80, 119] . Similar to this dataset, there is Talk Like A Graph [54], LLM4DyG [252], GraphViz [29], NLGraph [223], and GNN-AutoGL [119] (note that these datasets have been used only by one study [119]). 

The remaining datasets have been used exclusively in one out of the retrieved studies – many times this being the study proposing the dataset on the first place. Amarasinghe et al. [8] introduced the AI-copilot-data dataset, which includes 100 NL descriptions of problems within the production scheduling domain. Huang et al. [87] introduced the homonym dataset,<sup>5</sup> which comprises 80 NL descriptions of routing problems, including variants for single-robot and multi-robot routing. Almonacid [7] introduced a homonym dataset, which comprises 10 NL instructions for the creation of MiniZinc models involving discrete variables and arrays of discrete variables, thus ILP problems. Hao Chen and Li [72] introduced the OptiChat dataset, which comprises 63 infeasible (i.e., inconsistent) MILP model formulations across various domains. This dataset was derived from feasible models expressed through the Python library Pyomo [73] and sourced from a collection of libraries and textbooks. The formulations were created by modifying one or more model parameters (e.g., minimum inventory, demand, maximum capacity) or adding constraints (e.g., maximum cost, minimum demand for a particular product) so to make the instances infeasible (i.e., their set of feasible solutions is empty). Lawless et al. [111] introduced two datasets, Safeguard and Code Generation. They both are strictly connected to the framework the authors proposed. The Safeguard dataset is a binary classification dataset designed to evaluate whether the system at hand (i.e., a system that integrates CP and LLMs to schedule meetings in a company) has sufficient data sources (e.g., information related to the meeting attendees) to handle given NL constraints. The Code Generation dataset contains a collection of NL constraints that can be translated into Python code using the data structures available in the system. An example of such constraints is “The team has a no-meeting policy on {WEEKDAY}”. This dataset aims to test the capability of generating executable Python code that satisfies the specified constraints. While employing NL4Opt and other existing dataset from the ML community, Michailidis et al. [146] also introduced a homonym CP-based benchmark. The dataset was built using 18 CP problems from a university-level CP modelling course. Yang et al. [240] introduced OptiBench and ReSocratic-29k. OptiBench includes 816 real-world optimization problems spanning multiple domains, focusing on linear and mixed-integer programming and introducing a graph-based evaluation method to assess model correctness. ReSocratic-29k consists of 29,000 optimization problem demonstrations, generated through a reverse synthesis approach that first constructs step-by-step formulations before back-translating them into NL questions. These datasets provide a targeted benchmark for assessing and improving LLMs in formulating and solving optimization tasks. Borazjanizadeh et al. [20] introduced SearchBench, a dataset encompassing five problem categories and 1,107 instances, primarily focused on puzzles and general combinatorics. Each problem type corresponds to a well-known COP, but the constraints have been slightly modified to reduce the likelihood that LLMs encountered identical problems during their training phase. Mostajabdaveh et al. [152] presented a new dataset to complement the existing NL4Opt and ComplexOR benchmarks, aiming to provide less structured input and more complex optimization scenarios. This benchmark includes problems related to LP, MILP, and QP. Unlike NL4Opt, which expects a formal model as output, and ComplexOR, which requires Python code, this dataset outputs solutions in Zimple code. Similarly, Zhang et al. [248] enriched the NL4Opt dataset with English and Chinese problem descriptions. Ju et al. [96] introduced a dataset of 173,700 training and 21,800 test samples related to travel planning. 

Finally, a different dataset is ORQUA [151]. It is designed to evaluate the extent of CO knowledge in LLMs. Given a problem description, the dataset assesses the model’s ability to understand and identify, for example, the appropriate type of mathematical modeling the problem corresponds to. 

Similar to the platforms discussed in Section 6.2.6, we also identified general-purpose datasets in the reviewed studies. These datasets are valuable for developing LLMs-based approaches to optimization, particularly by providing math-related problems expressed in unstructured natural language which are useful especially for problem modeling (e.g., handling addition, multiplication, and data structures like sets). These resources can support researchers and practitioners in designing new applications of LLMs in CO. We briefly outline their characteristics and report some examples in Table 3. Notably, all of these resources were used by Ahmed and Choudhury [4], while GSM8K was also employed by Yang et al. [239]. 

> 5We use the term “homonym” when the authors did not provide a specific name for the dataset. 

17 

LLMS FOR COMBINATORIAL OPTIMIZATION 

DA ROS ET AL. 

Table 3: Examples of mathematical reasoning tasks from various benchmark datasets. 

|**Dataset**|**Task**|**Example**|
|---|---|---|
|GSM8K [35]|Arithmetic Word Prob-<br>lem|_Natalia sold clips to 48 of her friends in April, and then she sold half as many clips_<br>_in May. How many clips did Natalia sell altogether in April and May?_|
|MultiArith [78]|Multi-Step Arithmetic|_John has 3 apples. He buys 5 more apples and then eats 2. How many apples does_<br>_he have left?_|
|AquA [123]|Probability|_From a pack of 52 cards, two cards are drawn together at random. What is the_<br>_probability of both the cards being kings?_|
|BIG-Bench [195]|Logical Reasoning|_If a snail climbs a 10-meter pole at a rate of 2 meters per day but slides back 1_<br>_meter each night, how many days will it take to reach the top?_|
|BIG-Bench<br>Hard [202]|Combinatorial Reason-<br>ing|_A school has 6 different clubs. Each student must join exactly 2 clubs. How many_<br>_unique pairs of clubs can be formed?_|



GSM8K [35] consists of 8,500 linguistically diverse grade-school human-generated math word problems. Unlike simpler arithmetic datasets like AddSub [78] (395 problems) and SingleOp [105] (562 problems), GSM8K requires multi-step reasoning. Its emphasis on stepwise numerical reasoning aligns with CO, where problems often require sequential computations and recursive decision-making. 

MultiArith [78] consists of around 600 multi-step arithmetic problems that require sequential operations (e.g., addition, subtraction, and multiplication). It was partially generated from existing math problems and structured for ML applications. Its focus on structured numerical reasoning makes it relevant to CO techniques such as branch-and-bound and constraint satisfaction, which rely on constructive decision-making. 

AquA [123] presents 100,000 human- and machine-generated algebraic word problems in a multiple-choice format along with rationales explaining each answer. It requires the computation of correct answers and their selection from distractors. Many COPs involve symbolic reasoning and equation solving, making AquA useful for assessing a model’s ability to handle algebraic structures and optimization constraints. 

BIG-Bench [195] is a large-scale benchmark evaluating language models across more than 200 tasks, covering mathematics, reasoning, linguistics, commonsense understanding, and code generation. The dataset was created through a combination of human-designed tasks and algorithmically generated problem sets, allowing for a broad evaluation of logical reasoning and heuristic problem-solving. This makes it valuable for studying how models approach optimizationbased decision-making. A more challenging subset, BIG-Bench Hard [202], focuses on 23 particularly difficult tasks from BIG-Bench that remain unsolved or challenging for state-of-the-art models. Many of these challenges relate to CO, where finding optimal solutions in complex search spaces is a key difficulty. 

## **6.4 Application Domains** 

CO has been applied to a wide range of problems across various domains, and over the years, these problems have been formalized into well-known prototypical models, such as the TSP, the VRP, and the Capacited Vehicle Routing Problem (CVRP) in the field of routing. Among the 103 studies, 64 explicitly address problems within specific domains or problem formulations – which we overview in this section. In this analysis, literature reviews that provide information on the use of LLM without offering actual implementations are excluded, such as those by Fan et al. [53], Wu et al. [236], and Zhao et al. [253]. Exceptions apply to reviews like the one by Saka et al. [187] that also verified the application of LLMs in CO within the construction domain. 

The majority of these studies (26) focus on routing problems, particularly within the contexts of the TSP [30, 52, 81, 98, 124, 125, 127, 129, 131, 143, 198, 200, 239, 241, 243, 250], VRP [32, 37, 63, 86, 87, 98, 99, 129, 235, 243], orienteering [243] , and traveling [39, 96, 115] . While the first three COPs are well-known in the CO field, the latter refers to the modeling of the traveling activity (i.e., visiting a new city) as a COP. It cannot be considered as a TSP variant in all cases, as it is not given that the goal is to find a Hamiltonian path. Two other domains that have garnered significant attention are scheduling/planning (14 studies) and networks and graphs (10). In the first domain, studies have focused on variants of well-known benchmark problems, like the PFSP [8, 125] and planning [19, 45, 71, 93, 147, 157, 166, 226, 244], as well as specific scheduling problems, like server [242] and meeting/conference [95, 111] scheduling. Also for what concerns the Network and Graph domains, studies focused on general network design [80, 119, 134, 216, 245], but also on classical problems like coloring [143], social networks Sartori et al. [188], critical node identification [142], and path finding [20, 98]. 

18 

LLMS FOR COMBINATORIAL OPTIMIZATION 

DA ROS ET AL. 

The remaining studies focused on packing (9), combinatorics (4), engineering (3), finance (3), bioinformatics (3), supply chain (1), and strings (1). For a breakdown of specific COPs, we refer the interested reader to Appendix F. 

A limited number of studies (9) explore multiple problem domains and formulations to demonstrate the capabilities of LLMs across various contexts [20, 30, 125, 143, 184, 198, 241, 243, 250]. Additionally, Khan and Hamad [98] tackled a diverse set of problems, which however can all be reduced to graph-based ones, while studies like the one by Lawless et al. [110] inherently address multiple problem domains as they are based on library of problems (initially not thought for applications in the field of LLMs), like the MIPLIB dataset. 

## **6.5 Positions from Non-experimental Literature** 

Among the 103 selected studies, 11 are literature reviews, 7 are position papers, and 1 is a technical report. 

Fan et al. [53], Wu et al. [236], Huang et al. [84], Lai et al. [109], Cai et al. [23], and Liu et al. [128] presented literature reviews on the topic of LLM and optimization or on strictly related fields, such as algorithm design (Section 3). Saka et al. [187], Zhao et al. [253], Wu et al. [235], Pallagani et al. [166], Sui et al. [200], and Long et al. [134] presented literature reviews that deal with CO in specific application domains (i.e., engineering, planning, VRP, planning and scheduling, TSP, and network optimization, respectively) and in some cases involve (preliminary) studies and experiments with LLM. 

Wasserkrug et al. [228] put forward a position paper advocating for the usage of an LLM within optimization considering all the optimization steps. Similarly, Tsouros et al. [214] proposed a LLM-aided optimization pipeline in the context of CP modeling. Freuder [57] highlighted the potential of LLMs in facilitating the discussion between optimization and domain experts. Srivastava and Pallagani [196], Yu and Liu [246], and Ustyugov [218] presented insights on the usage of LLMs within EAs, planning-like tasks, and automated MILP configuration. 

The only technical report identified is by Ramamonjison et al. [179]. The report includes insights and comparisons related to the NL4Opt challenge (Sections 6.1 and 6.3). 

# **7 Future Research Directions** 

While various aspects of the optimization process have been addressed in the existing literature (Section 6), certain areas still call for further exploration. We have identified several future research directions: 

- _Metaheuristics_ : The adoption of LLMs in MH frameworks has been limited and scattered. Future research could investigate how LLMs can be used to dynamically adjust MH strategies, optimizing parameters (as anticipated in some studies [63, 110, 143]) or switching strategies based on the current state of the search. This could enhance the flexibility and effectiveness of MHs. Future studies could explore how LLMs might expand local search neighborhoods by suggesting structures or transition operators. 

- _Algorithm Selection_ : Utilizing LLMs to explore the search space of algorithm selection might be winning (as anticipated by Wu et al. [237]) and LLMs could help pinpoint scenarios where current solvers are less effective. Additionally, LLMs could be used to generate instances specifically designed to test the strengths and weaknesses of these solvers, leading to improved performance insights. 

- _Synthetic Instance Generation_ : LLMs could be leveraged to create synthetic instances that replicate the complexities of real-world problems or that are specifically crafted to challenge existing algorithms. This approach has been anticipated in the IndustryOR dataset [82]. 

- _LLMs behavior w.r.t. NLP problem description_ : While LLM capabilities w.r.t. visual representations in CO has been addressed [52], it remains unclear to what extent LLMs adjust their responses depending on the input style thus representing a promising research area. 

- _Evaluation Protocol_ : Evaluating the performance of LLMs on COPs remains challenging due to several factors: problems can have multiple representations, various encoding methods, and often lack known optimal solutions. While some efforts exist, a promising research direction involves developing standardized evaluation protocols and identifying suitable metrics. 

- _Agent-based System and COPs_ : Recent studies have explored how LLMs can function as autonomous agents [225]. While some of the studies already use an ensemble of LLMs, a promising research direction would be to investigate thoroughly how these autonomous agents can be effectively utilized within CO. 

Additional more general considerations for future research include ethical and bias considerations. As LLMs are integrated into optimization frameworks, research should also focus on ensuring that these technologies are used 

19 

LLMS FOR COMBINATORIAL OPTIMIZATION 

DA ROS ET AL. 

responsibly. This includes considering the environmental impact of the resources required by LLMs and developing more sustainable approaches to large-scale optimization. Future research should examine the potential biases in LLM-generated optimization solutions. More generally, strategies for ensuring fairness as well as incorporating ethical considerations into the optimization process could be explored. 

# **8 Limitations** 

While our systematic review offers valuable insights into the use of LLMs in CO, it has some limitations. First, research on LLMs and their application to optimization is advancing rapidly, with new studies emerging continuously. Consequently, while this systematic review attempts to be as comprehensive as possible, it inevitably cannot cover all existing studies. Also, systematic reviews depend on data gathered from other studies, meaning the quality and bias level of the evidence in a systematic review are directly tied to those of the data sources [50]. Therefore, we acknowledge that following PRISMA guidelines might have led to the inclusion of too many studies that report positive outcomes or successful applications of LLM over those that do not, potentially overstating the effectiveness or applicability of LLM in this field due to inherent selection bias. 

Then, our review focuses solely on how LLMs can be applied to CO. An equally significant aspect not covered in this study is how CO techniques can be employed to enhance LLMs, which is dual to our main focus. By not addressing this aspect, which can be pursued in future work, our review may miss relationships and interdependencies between the two research fields. Examples of such works include Pan et al. [167], who experiment with using MHs to engineer LLM prompts. More specifically, they use – among other methods – Hill Climbing (HC) and SA, to discover and learn new efficient prompts. Another example is the work by Singla et al. [192], who model the trade-off between response quality and inference cost of LLM as a bi-objective combinatorial optimization problem. Additionally, this study focuses on CO, disregarding other types of optimizations, such as Continuous Optimization. Examples of such works are those by Pluhacek et al. [171, 172]. 

We intentionally included a significant number of pre-prints alongside peer-reviewed publications (Section 5). Such a decision is driven by the fast-paced nature of research in the field of LLMs, where discoveries and advancements are rapidly shared through pre-prints before formal publication (see, for example, Devlin et al. [44]). Pre-prints allow for timely access to the latest research, innovations, and discussions and are widely used within the NLP community. We take no position on the content of pre-prints found on platforms like arXiv; instead, we include these documents to maximize the recall of our systematic review. 

Eventually, our systematic review includes studies based on closed-source LLMs, like ChatGPT. The proprietary nature of these systems often restricts access to their full methodologies and inner workings, which creates significant challenges for understanding and replicating the reported findings. Despite these downsides, we include works dealing both with open- and closed-source LLMs to maximize the recall of our systematic review. 

# **9 Conclusions and Future Work** 

In this systematic review, we examined the application of LLMs to CO. Our study summarizes the literature leveraging the PRISMA 2020 guidelines. To our knowledge, this is the first attempt to comprehensively study the application of LLMs to CO and COP. Out of over 2,000 collected publications, we included 103 studies in our analysis. These studies were classified based on the task LLMs performed within the optimization process, the implementation details of the LLMs, the most commonly used datasets, and the application domains where LLMs have been employed in CO thus far. Additionally, we highlighted the caveats associated with using LLMs in the field of optimization, outlined future research directions, and exposed the limitations of the present review. 

The research on LLMs is rapidly evolving, thus continuously identifying areas for further research is crucial. We plan to periodically update our systematic review (as advocated by the PRISMA guidelines [163]). This process ensures that our review remains relevant in this fast-moving field and allows us to update those studies initially polished as pre-prints (thus solving one of the limitations of our work, Section 8). Future research will also account for the aspects neglected by this paper, such as the integration of LLMs into optimization paradigms other than CO and for the dual aspect of optimization used for enhancing LLMs. 

With much of the state-of-the-art work being conducted relying on proprietary models such as ChatGPT, future studies will also focus on developing methods for assessing and reporting on such models to improve the transparency and replicability of the presented studies. This could involve creating frameworks for sharing results that do not compromise proprietary data but still provide sufficient detail for academic reproducibility/replicability (as also advocated by many researchers in the optimization field [203, 204]). 

20 

LLMS FOR COMBINATORIAL OPTIMIZATION 

DA ROS ET AL. 

As LLMs are deployed in critical areas, their ethical implications, particularly in sensitive optimization tasks, require closer examination especially under the ethical point of view. Finally, addressing biases in LLM outputs remains a significant concern and is essential for ensuring fair and responsible applications of LLMs in CO. 

# **Declaration of Competing Interest** 

The authors declare that they have no known competing interests. 

# **Data Availability** 

The data supporting the findings of this study are available within the paper and its appendices. 

# **Acknowledgments** 

This research is partially supported by the PRIN 2022 Project – “MoT—The Measure of Truth: An Evaluation-Centered Machine-Human Hybrid Framework for Assessing Information Truthfulness” – Code No. 20227F2ZN3, CUP No. G53D23002800006 Funded by the European Union – Next Generation EU – PNRR M4 C2 I1.1., by the Strategic Plan of the University of Udine–Interdepartment Project on Artificial Intelligence (2020-2025), and by the Strategic Plan of the University of Udine (2022-2025). 

# **References** 

- [1] Abdullin, Y., Molla, D., Ofoghi, B., Yearwood, J., Li, Q.: Synthetic Dialogue Dataset Generation using LLM Agents. In: Proceedings of the Third Workshop on Natural Language Generation, Evaluation, and Metrics (GEM), pp. 181–191, ACL, Singapore (12 2023), URL `https://aclanthology.org/2023.gem-1.16` 

- [2] AhmadiTeshnizi, A., Gao, W., Brunborg, H., Talaei, S., Udell, M.: OptiMUS-0.3: Using Large Language Models to Model and Solve Optimization Problems at Scale. arXiv (2024), doi:10.48550/arXiv.2407.19633 

- [3] AhmadiTeshnizi, A., Gao, W., Udell, M.: OptiMUS: Scalable Optimization Modeling with (MI)LP Solvers and Large Language Models. In: Proceedings of the 41st International Conference on Machine Learning, pp. 1234–1245, ICML ’24, JMLR.org, Vienna, Austria (2024), doi:10.5555/3692070.3692094 

- [4] Ahmed, T., Choudhury, S.: LM4OPT: Unveiling the potential of Large Language Models in formulating mathematical optimization problems. INFOR: Information Systems and Operational Research **62** (4), 559–572 (2024), doi:10.1080/03155986.2024.2388452 

- [5] AI, C.: Command R+: A Large Language Model for Enterprise AI (2024), URL `https://docs.cohere.com/ v2/docs/command-r-plus` 

- [6] Alipour-Vaezi, M., Tsui, K.L.: Data-driven portfolio management for motion pictures industry: A new datadriven optimization methodology using a large language model as the expert. Computers & Industrial Engineering **197** , 110574 (2024), doi:10.1016/j.cie.2024.110574 

- [7] Almonacid, B.: Towards an Automatic Optimisation Model Generator Assisted with Generative Pre-trained Transformer. arXiv (2023), doi:10.48550/arXiv.2305.05811 

- [8] Amarasinghe, P.T., Nguyen, S., Sun, Y., Alahakoon, D.: AI-Copilot for Business Optimisation: A Framework and A Case Study in Production Scheduling. arXiv (2023), doi:10.48550/arXiv.2309.13218 

- [9] Anagnostidis, S., Bulian, J.: How Susceptible are LLMs to Influence in Prompts? arXiv (2024), doi:10.48550/ arXiv.2408.11865 

- [10] Anthropic: Claude 3.5 Sonnet Model Card Addendum (2024), URL `https://www.anthropic.com/news/ claude-3-5-sonnet` 

- [11] Anthropic Team: Introducing the next generation of Claude (March 2024), URL `https://www.anthropic. com/news/claude-3-family` , accessed: 2024-06-18 

- [12] Bahdanau, D., Cho, K., Bengio, Y.: Neural Machine Translation by Jointly Learning to Align and Translate. arXiv (2016), doi:10.48550/arXiv.1409.0473 

- [13] Balloccu, S., Schmidtová, P., Lango, M., Dusek, O.: Leak, Cheat, Repeat: Data Contamination and Evaluation Malpractices in Closed-Source LLMs. In: Proceedings of the 18th Conference of the European Chapter of the ACL (Volume 1: Long Papers), pp. 67–93, ACL, St. Julian’s, Malta (3 2024), URL `https://aclanthology. org/2024.eacl-long.5` 

21 

LLMS FOR COMBINATORIAL OPTIMIZATION 

DA ROS ET AL. 

- [14] Bengio, Y., Lodi, A., Prouvost, A.: Machine learning for combinatorial optimization: A methodological tour d’horizon. European Journal of Operational Research **290** (2), 405–421 (2021), ISSN 0377-2217, doi: 10.1016/j.ejor.2020.07.063 

- [15] Besta, M., Blach, N., Kubicek, A., Gerstenberger, R., Podstawski, M., Gianinazzi, L., Gajda, J., Lehmann, T., Niewiadomski, H., Nyczyk, P., Hoefler, T.: Graph of thoughts: Solving elaborate problems with large language models. Proceedings of the AAAI Conference on Artificial Intelligence **38** (16), 17682–17690 (3 2024), doi:10.1609/aaai.v38i16.29720 

- [16] Bifulco, R., Errica, F., Sanvito, D., Siracusano, G.: What Did I Do Wrong? Quantifying LLMs’ Sensitivity and Consistency to Prompt Engineering. arXiv (2024), doi:10.48550/arXiv.2406.12334, URL `https://arxiv. org/abs/2406.12334` 

- [17] Blank, J., Deb, K.: Pymoo: Multi-Objective Optimization in Python. IEEE Access **8** , 89497–89509 (2020), doi:10.1109/ACCESS.2020.2990567 

- [18] Blum, C., Roli, A.: Metaheuristics in combinatorial optimization: Overview and conceptual comparison. ACM Computing Surveys **35** (3), 268–308 (9 2003), ISSN 0360-0300, doi:10.1145/937503.937505 

- [19] Bohnet, B., Nova, A., Parisi, A.T., Swersky, K., Goshvadi, K., Dai, H., Schuurmans, D., Fiedel, N., Sedghi, H.: Exploring and Benchmarking the Planning Capabilities of Large Language Models. arXiv (2024), doi: 10.48550/arXiv.2406.13094 

- [20] Borazjanizadeh, N., Herzig, R., Darrell, T., Feris, R., Karlinsky, L.: Navigating the Labyrinth: Evaluating and Enhancing LLMs’ Ability to Reason About Search Problems. arXiv (2024), doi:10.48550/arXiv.2406.12172 

- [21] Brown, T., Mann, B., Ryder, N., Subbiah, M., Kaplan, J.D., Dhariwal, P., Neelakantan, A., Shyam, P., Sastry, G., Askell, A., et al.: Language Models are Few-Shot Learners. In: Advances in Neural Information Processing Systems, vol. 33, pp. 1877–1901, Curran Associates, Inc., Virtual Conference (2020), URL `https://proceedings. neurips.cc/paper_files/paper/2020/file/1457c0d6bfcb4967418bfb8ac142f64a-Paper.pdf` 

- [22] Bubeck, S., Chandrasekaran, V., Eldan, R., Gehrke, J., Horvitz, E., Kamar, E., Lee, P., Lee, Y.T., Li, Y., Lundberg, S., Nori, H., Palangi, H., Ribeiro, M.T., Zhang, Y.: Sparks of Artificial General Intelligence: Early experiments with GPT-4. arXiv (2023), doi:10.48550/arXiv.2303.12712 

- [23] Cai, J., Xu, J., Li, J., Yamauchi, T., Iba, H., Tei, K.: Exploring the Improvement of Evolutionary Computation via Large Language Models. In: Proceedings of the Genetic and Evolutionary Computation Conference Companion, p. 83–84, GECCO ’24 Companion, ACM, New York, NY, USA (2024), ISBN 9798400704956, doi:10.1145/ 3638530.3664086 

- [24] Cai, Z., Cao, M., Chen, H., Chen, K., Chen, K., Chen, X., Chen, X., Chen, Z., Chen, Z., Chu, P., et al.: InternLM2 Technical Report. arXiv (2024), doi:10.48550/arXiv.2403.17297 

- [25] Ceschia, S., Di Gaspero, L., Mazzaracchio, V., Policante, G., Schaerf, A.: Solving a real-world nurse rostering problem by simulated annealing. Operations Research for Health Care **36** , 100379 (2023), ISSN 2211-6923, doi:10.1016/j.orhc.2023.100379 

- [26] Ceschia, S., Di Gaspero, L., Schaerf, A.: Educational timetabling: Problems, benchmarks, and state-of-the-art results. European Journal of Operational Research **308** (1), 1–18 (2023), ISSN 0377-2217, doi:10.1016/j.ejor. 2022.07.011 

- [27] Ceschia, S., Schaerf, A.: Multi-neighborhood simulated annealing for the capacitated facility location problem with customer incompatibilities. Computers & Industrial Engineering **188** , 109858 (2024), ISSN 0360-8352, doi:10.1016/j.cie.2023.109858 

- [28] Chacón Sartori, C., Blum, C., Ochoa, G.: Large Language Models for the Automated Analysis of Optimization Algorithms. In: Proceedings of the Genetic and Evolutionary Computation Conference, pp. 160–168, GECCO ’24, ACM, New York, NY, USA (2024), doi:10.1145/3638529.3654086 

- [29] Chen, N., Li, Y., Tang, J., Li, J.: GraphWiz: An Instruction-Following Language Model for Graph Problems. arXiv (2024), doi:10.48550/arXiv.2402.16029 

- [30] Chen, Z., Zhou, Z., Lu, Y., Xu, R., Pan, L., Lan, Z.: UBER: Uncertainty-Based Evolution with Large Language Models for Automatic Heuristic Design. arXiv (2024), doi:10.48550/arXiv.2412.20694 

- [31] Chiang, W.L., Zheng, L., Sheng, Y., Angelopoulos, A.N., Li, T., Li, D., Zhang, H., Zhu, B., Jordan, M., Gonzalez, J.E., Stoica, I., et al.: Chatbot Arena: An Open Platform for Evaluating LLMs by Human Preference. arXiv (2024), doi:10.48550/arXiv.2403.04132 

- [32] Chin, S.J.K., Winkenbach, M., Srivastava, A.: Learning to Deliver: a Foundation Model for the Montreal Capacitated Vehicle Routing Problem. arXiv (2024), doi:10.48550/arXiv.2403.00026 

22 

LLMS FOR COMBINATORIAL OPTIMIZATION 

DA ROS ET AL. 

- [33] Chowdhery, A., Narang, S., Devlin, J., Bosma, M., Mishra, G., Roberts, A., Barham, P., Chung, H.W., Sutton, C., Gehrmann, S., et al.: PaLM: scaling language modeling with pathways. Journal of Machine Learning Research **24** (1) (3 2024), ISSN 1532-4435, URL `http://jmlr.org/papers/v24/22-1144.html` 

- [34] Chung, H.W., Hou, L., Longpre, S., Zoph, B., Tay, Y., Fedus, W., Li, Y., Wang, X., Dehghani, M., Brahma, S., , et al.: Scaling instruction-finetuned language models. Journal of Machine Learning Research **25** (70), 1–53 (2024), URL `http://jmlr.org/papers/v25/23-0870.html` 

- [35] Cobbe, K., Kosaraju, V., Bavarian, M., Chen, M., Jun, H., Kaiser, L., Plappert, M., Tworek, J., Hilton, J., Nakano, R., Hesse, C., Schulman, J.: Training Verifiers to Solve Math Word Problems. arXiv (2021), doi: 10.48550/arXiv.2110.14168 

- [36] Cooper, C., Booth, A., Britten, N., Garside, R.: A comparison of results of empirical studies of supplementary search techniques and recommendations in review methodology handbooks: a methodological review. Systematic Reviews **6** (1), 234 (Nov 2017), ISSN 2046-4053, doi:10.1186/s13643-017-0625-1 

- [37] Da, L., Liou, K., Chen, T., Zhou, X., Luo, X., Yang, Y., Wei, H.: Open-ti: open traffic intelligence with augmented language model. International Journal of Machine Learning and Cybernetics **15** (10), 4761–4786 (Oct 2024), ISSN 1868-808X, doi:10.1007/s13042-024-02190-8 

- [38] Dakle, P.P., Kadıo˘glu, S., Uppuluri, K., Politi, R., Raghavan, P., Rallabandi, S., Srinivasamurthy, R.: Ner4Opt: Named Entity Recognition for Optimization Modelling from Natural Language. In: Integration of Constraint Programming, Artificial Intelligence, and Operations Research, pp. 299–319, Springer Nature Switzerland, Cham (2023), ISBN 978-3-031-33271-5, doi:10.1007/978-3-031-33271-5_20 

- [39] De La Rosa, T., Gopalakrishnan, S., Pozanco, A., Zeng, Z., Borrajo, D.: TRIP-PAL: Travel Planning with Guarantees by Combining Large Language Models and Automated Planners. arXiv (2024), doi:10.48550/arXiv. 2406.10196 

- [40] De Zarzà, I., De Curtò, J., Roig, G., Calafate, C.T.: Optimized Financial Planning: Integrating Individual and Cooperative Budgeting Models with LLM Recommendations. AI **5** (1), 91–114 (2024), ISSN 2673-2688, doi:10.3390/ai5010006 

- [41] DeepSeek-AI, Bi, X., Chen, D., Chen, G., Chen, S., Dai, D., Deng, C., Ding, H., Dong, K., Du, Q.: DeepSeek LLM: Scaling Open-Source Language Models with Longtermism. arXiv (2024), doi:10.48550/arXiv.2401.02954 

- [42] DeepSeek-AI, Liu, A., Feng, B., Wang, B., Wang, B., Liu, B., Zhao, C., Deng, C., Ruan, C., Dai, D.: DeepSeekV2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model. arXiv (2024), doi:10.48550/ arXiv.2405.04434 

- [43] DeepSeek-AI, Zhu, Q., Guo, D., Shao, Z., Yang, D., Wang, P., Xu, R., Wu, Y., Li, Y., Gao, H.: DeepSeek-CoderV2: Breaking the Barrier of Closed-Source Models in Code Intelligence. arXiv (2024), doi:10.48550/arXiv.2406. 11931 

- [44] Devlin, J., Chang, M.W., Lee, K., Toutanova, K.: BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding. In: Proceedings of the 2019 Conference of the North American Chapter of the ACL: Human Language Technologies, Volume 1 (Long and Short Papers), pp. 4171–4186, ACL, Minneapolis, Minnesota (6 2019), doi:10.18653/v1/N19-1423 

- [45] Dhanaraj, N., Jeon, M., Kang, J.H., Nikolaidis, S., Gupta, S.K.: Preference Elicitation and Incorporation for Human-Robot Task Scheduling. In: 2024 IEEE 20th International Conference on Automation Science and Engineering (CASE), pp. 3103–3110, IEEE, Bari, Italy (2024), doi:10.1109/CASE59546.2024.10711695 

- [46] Diamond, S., Boyd, S.: CVXPY: a python-embedded modeling language for convex optimization. The Journal of Machine Learning Research **17** (1), 2909–2913 (1 2016), ISSN 1532-4435, doi:10.5555/2946645.3007036 

- [47] Doan, X.D.: VTCC-NLP at NL4Opt competition subtask 1: An Ensemble Pre-trained language models for Named Entity Recognition. arXiv (2022), doi:10.48550/arXiv.2212.07219 

- [48] Dorigo, M., Birattari, M., Stutzle, T.: Ant colony optimization. IEEE Computational Intelligence Magazine **1** (4), 28–39 (2006), doi:10.1109/MCI.2006.329691 

- [49] Driess, D., Xia, F., Sajjadi, M.S.M., Lynch, C., Chowdhery, A., Ichter, B., Wahid, A., Tompson, J., Vuong, Q., Yu, T., et al.: PaLM-E: an embodied multimodal language model. In: Proceedings of the 40th International Conference on Machine Learning, ICML’23, JMLR.org, Honolulu, Hawaii, USA (2023), doi:10.5555/3618408.3618748 

- [50] Drucker, A.M., Fleming, P., Chan, A.W.: Research Techniques Made Simple: Assessing Risk of Bias in Systematic Reviews. Journal of Investigative Dermatology **136** (11), e109–e114 (2016), ISSN 0022-202X, doi:10.1016/j.jid.2016.08.021 

23 

LLMS FOR COMBINATORIAL OPTIMIZATION 

DA ROS ET AL. 

- [51] Du, Z., Qian, Y., Liu, X., Ding, M., Qiu, J., Yang, Z., Tang, J.: GLM: General Language Model Pretraining with Autoregressive Blank Infilling. In: Proceedings of the 60th Annual Meeting of the ACL (Volume 1: Long Papers), pp. 320–335, ACL, Dublin, Ireland (2022), doi:10.18653/v1/2022.acl-long.26 

- [52] Elhenawy, M., Abutahoun, A., Alhadidi, T.I., Jaber, A., Ashqar, H.I., Jaradat, S., Abdelhay, A., Glaser, S., Rakotonirainy, A.: Visual Reasoning and Multi-Agent Approach in Multimodal Large Language Models (MLLMs): Solving TSP and mTSP Combinatorial Challenges. Machine Learning and Knowledge Extraction **6** (3), 1894–1920 (2024), doi:10.3390/make6030093 

- [53] Fan, Z., Ghaddar, B., Wang, X., Xing, L., Zhang, Y., Zhou, Z.: Artificial Intelligence for Operations Research: Revolutionizing the Operations Research Process. arXiv (2024), doi:10.48550/arXiv.2401.03244 

- [54] Fatemi, B., Halcrow, J., Perozzi, B.: Talk like a Graph: Encoding Graphs for Large Language Models. arXiv (2023), doi:10.48550/arXiv.2310.04560 

- [55] Franzin, A., Stützle, T.: Revisiting simulated annealing: A component-based analysis. Computers & Operations Research **104** , 191–206 (2019), ISSN 0305-0548, doi:10.1016/j.cor.2018.12.015 

- [56] Freire, Y., Santamaría Laorden, A., Orejas Pérez, J., Gómez Sánchez, M., Díaz-Flores García, V., Suárez, A.: ChatGPT performance in prosthodontics: Assessment of accuracy and repeatability in answer generation. The Journal of Prosthetic Dentistry **131** (4), 659.e1–659.e6 (2024), ISSN 0022-3913, doi:10.1016/j.prosdent.2024.01. 018 

- [57] Freuder, E.C.: Conversational Modeling for Constraint Satisfaction. Proceedings of the AAAI Conference on Artificial Intelligence **38** (20), 22592–22597 (Mar 2024), doi:10.1609/aaai.v38i20.30268 

- [58] Gangwar, N., Kani, N.: Highlighting Named Entities in Input for Auto-formulation of Optimization Problems. In: Intelligent Computer Mathematics, pp. 130–141, Springer Nature Switzerland, Cham (2023), ISBN 978-3031-42753-4, doi:10.1007/978-3-031-42753-4_9 

- [59] Garey, M.R., Johnson, D.S., Sethi, R.: The Complexity of Flowshop and Jobshop Scheduling. Mathematics of Operations Research **1** (2), 117–129 (1976), ISSN 0364-765X, 1526-5471, URL `http://www.jstor.org/ stable/3689278` 

- [60] Gecode Team: Gecode: Generic Constraint Development Environment (2006), URL `http://www.gecode.org` , accessed: 27-06-2024 

- [61] GenAI, M.: Camels in a Changing Climate: Enhancing LM Adaptation with Tulu 2. arXiv (2023), doi: 10.48550/arXiv.2311.10702 

- [62] GenAI, M.: Llama 2: Open Foundation and Fine-Tuned Chat Models. arXiv (2023), doi:10.48550/arXiv.2307. 09288 

- [63] Ghiani, G., Solazzo, G., Elia, G.: Integrating Large Language Models and Optimization in Semi-Structured Decision Making: Methodology and a Case Study. Algorithms **17** (12) (2024), doi:10.3390/a17120582 

- [64] Gjergji, I., Musliu, N.: Large Neighborhood Search for the Capacitated P-Median Problem. In: Metaheuristics, pp. 158–173, Springer Nature Switzerland, Cham (2024), ISBN 978-3-031-62922-8, doi:10.1007/ 978-3-031-62922-8_11 

- [65] Glover, F.: Tabu Search. Springer, New York, NY (1997), ISBN 978-0-7923-9965-0, doi:10.1007/ 978-1-4615-6089-0 

- [66] Google: PaLM 2 Technical Report. arXiv (2023), doi:10.48550/arXiv.2305.10403 

- [67] Guns, T.: Increasing Modeling Language Convenience with a Universal N-Dimensional Array: CPpy as a PythonEmbedded Example. In: Proceedings of the 18th Workshop on Constraint Modelling and Reformulation at CP (ModRef 2019), ACP, Stamford, CT, USA (2019), URL `https://modref.github.io/ModRef2019.html` 

- [68] Guo, D., Lu, S., Duan, N., Wang, Y., Zhou, M., Yin, J.: UniXcoder: Unified Cross-Modal Pre-training for Code Representation. In: Proceedings of the 60th Annual Meeting of the ACL (Volume 1: Long Papers), pp. 7212–7225, ACL, Dublin, Ireland (may 2022), doi:10.18653/v1/2022.acl-long.499 

- [69] Guo, P.F., Chen, Y.H., Tsai, Y.D., Lin, S.D.: Towards Optimizing with Large Language Models. arXiv (2024), doi:10.48550/arXiv.2310.05204 

- [70] Gurobi Optimization, LLC: Gurobi Optimizer Reference Manual (2023), URL `https://www.gurobi.com` 

- [71] Hao, Y., Zhang, Y., Fan, C.: Planning Anything with Rigor: General-Purpose Zero-Shot Planning with LLMbased Formalized Programming. arXiv (2024), doi:10.48550/arXiv.2410.12112 

- [72] Hao Chen, G.E.C.F., Li, C.: Diagnosing infeasible optimization problems using large language models. INFOR: Information Systems and Operational Research **62** (4), 573–587 (2024), doi:10.1080/03155986.2024.2385189 

24 

LLMS FOR COMBINATORIAL OPTIMIZATION 

DA ROS ET AL. 

- [73] Hart, W.E., Watson, J.P., Woodruff, D.L.: Pyomo: modeling and solving mathematical programs in python. Mathematical Programming Computation **3** (3), 219–260 (Sep 2011), ISSN 1867-2957, doi:10.1007/s12532-011-0026-8 

- [74] He, J., N, M., Vignesh, S., Kumar, D., Uppal, A.: Linear programming word problems formulation using EnsembleCRF NER labeler and text generator with data augmentations. arXiv (2022), doi:10.48550/arXiv.2212. 14657 

- [75] Heinrich, M., Hofmann, L., Baurecht, H., Kreuzer, P.M., Knüttel, H., Leitzmann, M.F., Seliger, C.: Suicide risk and mortality among patients with cancer. Nature Medicine **28** (4), 852–859 (Apr 2022), ISSN 1546-170X, doi:10.1038/s41591-022-01745-y 

- [76] Holland, J.H.: Genetic Algorithms. Scientific American **267** (1), 66–73 (1992), ISSN 00368733, 19467087, URL `http://www.jstor.org/stable/24939139` 

- [77] Hoos, H.H.: Programming by optimization. Communications of the ACM **55** (2), 70–80 (feb 2012), ISSN 0001-0782, doi:10.1145/2076450.2076469 

- [78] Hosseini, M.J., Hajishirzi, H., Etzioni, O., Kushman, N.: Learning to Solve Arithmetic Word Problems with Verb Categorization. In: Proceedings of the 2014 Conference on Empirical Methods in Natural Language Processing (EMNLP), pp. 523–533, ACL, Doha, Qatar (Oct 2014), doi:10.3115/v1/D14-1058 

- [79] Hu, E.J., Shen, Y., Wallis, P., Allen-Zhu, Z., Li, Y., Wang, S., Wang, L., Chen, W.: LoRA: Low-Rank Adaptation of Large Language Models. arXiv (2021), doi:10.48550/arXiv.2106.09685 

- [80] Hu, Y., Lei, R., Huang, X., Wei, Z., Liu, Y.: Scalable and Accurate Graph Reasoning with LLM-based MultiAgents. arXiv (2024), doi:10.48550/arXiv.2410.05130 

- [81] Huang, B., Wu, X., Zhou, Y., Wu, J., Feng, L., Cheng, R., Tan, K.C.: Exploring the True Potential: Evaluating the Black-box Optimization Capability of Large Language Models. arXiv (2024), doi:10.48550/arXiv.2404.06290 

- [82] Huang, C., Tang, Z., Hu, S., Jiang, R., Zheng, X., Ge, D., Wang, B., Wang, Z.: ORLM: A Customizable Framework in Training Large Models for Automated Optimization Modeling. arXiv (2024), doi:10.48550/arXiv. 2405.17743 

- [83] Huang, H., et al.: The Open Cookbook for Top-Tier Code Large Language Models. arXiv (2024), doi:10.48550/ arXiv.2411.04905 

- [84] Huang, S., Yang, K., Qi, S., Wang, R.: When large language model meets optimization. Swarm and Evolutionary Computation **90** , 101663 (2024), doi:10.1016/j.swevo.2024.101663 

- [85] Huang, X., Shen, Q., Hu, Y., Gao, A., Wang, B.: LLMs for Mathematical Modeling: Towards Bridging the Gap between Natural and Mathematical Languages. arXiv (2025), doi:10.48550/arXiv.2405.13144 

- [86] Huang, Y., Zhang, W., Feng, L., Wu, X., Tan, K.C.: How Multimodal Integration Boost the Performance of LLM for Optimization: Case Study on Capacitated Vehicle Routing Problems. arXiv (2024), doi:10.48550/arXiv.2403. 01757 

- [87] Huang, Z., Shi, G., Sukhatme, G.S.: From Words to Routes: Applying Large Language Models to Vehicle Routing. arXiv (2024), doi:10.48550/arXiv.2403.10795 

- [88] IBM: IBM ILOG CPLEX Optimization Studio, Getting Started with Scheduling in CPLEX Studio. IBM (2017), URL `https://www.ibm.com/docs/en/icos/20.1.0?topic= kit-getting-started-scheduling-in-cplex-studio` , accessed: 27-06-2024 

- [89] Jang, S.: Tag Embedding and Well-defined Intermediate Representation improve Auto-Formulation of Problem Description. arXiv (2022), doi:10.48550/arXiv.2212.03575 

- [90] Jiang, A.Q., Sablayrolles, A., Mensch, A., Bamford, C., Chaplot, D.S., de las Casas, D., Bressand, F., Lengyel, G., Lample, G., Saulnier, L., Renard Lavaud, L., Lachaux, M.A., Stock, P., Le Scao, T., Lavril, T., Wang, T., Lacroix, T., El Sayed, W.: Mistral 7B. arXiv (2023), doi:10.48550/arXiv.2310.06825 

- [91] Jiang, A.Q., Sablayrolles, A., Roux, A., Mensch, A., Savary, B., Bamford, C., Chaplot, D.S., de las Casas, D., Bou Hanna, E., Bressand, F., Lengyel, G., Bour, G., Lample, G., Renard Lavaud, L., Saulnier, L., Lachaux, M.A., Stock, P., Subramanian, S., Yang, S., Antoniak, S., Le Scao, T., Gervet, T., Lavril, T., Wang, T., Lacroix, T., El Sayed, W.: Mixtral of Experts. arXiv (2024), doi:10.48550/arXiv.2401.04088 

- [92] Jiang, C., Shu, X., Qian, H., Lu, X., Zhou, J., Zhou, A., Yu, Y.: LLMOPT: Learning to Define and Solve General Optimization Problems from Scratch. In: Proceedings of the Thirteenth International Conference on Learning Representations, pp. 3160–3172, Conference Organizers, Singapore (2025), URL `https://openreview.net/ forum?id=9OMvtboTJg` 

- [93] Jiang, S., Xie, M., Luo, J.: Large Language Models for Combinatorial Optimization of Design Structure Matrix. arXiv (2024), doi:10.48550/arXiv.2411.12571 

25 

LLMS FOR COMBINATORIAL OPTIMIZATION 

DA ROS ET AL. 

- [94] Jin, M., Sel, B., Hardeep, F., Yin, W.: Democratizing Energy Management with LLM-Assisted Optimization Autoformalism. In: 2024 IEEE International Conference on Communications, Control, and Computing Technologies for Smart Grids (SmartGridComm), pp. 258–263, IEEE Communications Society, Oslo, Norway (2024), doi:10.1109/SmartGridComm60555.2024.10738100 

- [95] Jobson, D., Li, Y.: Investigating the Potential of Using Large Language Models for Scheduling. In: Proceedings of the 1st ACM International Conference on AI-Powered Software, p. 170–171, AIware 2024, ACM, New York, NY, USA (2024), ISBN 9798400706851, doi:10.1145/3664646.3665084 

- [96] Ju, D., Jiang, S., Cohen, A., Foss, A., Mitts, S., Zharmagambetov, A., Amos, B., Li, X., Kao, J.T., Fazel-Zarandi, M., Tian, Y.: To the Globe (TTG): Towards Language-Driven Guaranteed Travel Planning. In: Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing: System Demonstrations, pp. 240–249, ACL, Miami, Florida, USA (Nov 2024), doi:10.18653/v1/2024.emnlp-demo.25 

- [97] Karimi-Mamaghan, M., Mohammadi, M., Meyer, P., Karimi-Mamaghan, A.M., Talbi, E.G.: Machine learning at the service of meta-heuristics for solving combinatorial optimization problems: A state-of-the-art. European Journal of Operational Research **296** (2), 393–422 (2022), ISSN 0377-2217, doi:10.1016/j.ejor.2021.04.032 

- [98] Khan, M.A., Hamad, L.: On the Capability of LLMs in Combinatorial Optimization. TechRxiv (November 2024), doi:10.36227/techrxiv.173092026.60478567/v1 

- [99] Kikuta, D., Ikeuchi, H., Tajiri, K., Nakano, Y.: RouteExplainer: An Explanation Framework for Vehicle Routing Problem. In: Advances in Knowledge Discovery and Data Mining, pp. 30–42, Springer Nature Singapore, Singapore (2024), ISBN 978-981-97-2259-4, doi:10.1007/978-981-97-2259-4_3 

- [100] Kirkpatrick, S., Gelatt, C.D., Vecchi, M.P.: Optimization by Simulated Annealing. Science **220** (4598), 671–680 (1983), doi:10.1126/science.220.4598.671 

- [101] Kletzander, L., Musliu, N.: Solving the general employee scheduling problem. Computers & Operations Research **113** , 104794 (2020), ISSN 0305-0548, doi:10.1016/j.cor.2019.104794 

- [102] Kletzander, L., Musliu, N.: Hyper-heuristics for personnel scheduling domains. Artificial Intelligence **334** , 104172 (2024), ISSN 0004-3702, doi:10.1016/j.artint.2024.104172 

- [103] Kochanek, K., Skarzynski, H., Jedrzejczak, W.W.: Accuracy and Repeatability of ChatGPT Based on a Set of Multiple-Choice Questions on Objective Tests of Hearing. Cureus **16** (5) (5 2024), doi:10.7759/cureus.59857 

- [104] Kojima, T., Gu, S.S., Reid, M., Matsuo, Y., Iwasawa, Y.: Large Language Models are Zero-Shot Reasoners. arXiv (2023), doi:10.48550/arXiv.2205.11916 

- [105] Koncel-Kedziorski, R., Roy, S., Amini, A., Kushman, N., Hajishirzi, H.: Parsing Algebraic Word Problems into Equations. Transactions of the ACL **3** , 585–597 (2015), doi:10.1162/tacl_a_00153 

- [106] Kubiak, W.: On a conjecture for the university timetabling problem. Discrete Applied Mathematics **299** , 26–49 (2021), ISSN 0166-218X, doi:10.1016/j.dam.2021.04.010 

- [107] Lackner, M.L., Mrkvicka, C., Musliu, N., Walkiewicz, D., Winter, F.: Exact methods for the Oven Scheduling Problem. Constraints **28** (2), 320–361 (Jun 2023), ISSN 1572-9354, doi:10.1007/s10601-023-09347-2 

- [108] Laguna, M., Martí, R., Martinez-Gavara, A., Perez-Peló, S., Resende, M.G.C.: 20 years of Greedy Randomized Adaptive Search Procedures with Path Relinking. arXiv (2023), doi:10.48550/arXiv.2312.12663 

- [109] Lai, H., Wang, B., Liu, J., He, F., Zhang, C., Liu, H., Chen, H.: Solving Mathematical Problems Using Large Language Models: A Survey. SSRN (2024), doi:10.2139/ssrn.5002356 

- [110] Lawless, C., Li, Y., Wikum, A., Udell, M., Vitercik, E.: LLMs for Cold-Start Cutting Plane Separator Configuration. arXiv (2024), doi:10.48550/arXiv.2412.12038 

- [111] Lawless, C., Schoeffer, J., Le, L., Rowan, K., Sen, S., St. Hill, C., Suh, J., Sarrafzadeh, B.: “I Want It That Way”: Enabling Interactive Decision Support Using Large Language Models and Constraint Programming. ACM Transactions on Interactive Intelligent Systems **14** (3), 8432–8448 (Sep 2024), doi:10.1145/3685053 

- [112] Le, H., Wang, Y., Gotmare, A.D., Savarese, S., Hoi, S.C.: CodeRL: mastering code generation through pretrained models and deep reinforcement learning (2022), doi:10.5555/3600270.3601819 

- [113] Lewis, M., Liu, Y., Goyal, N., Ghazvininejad, M., Mohamed, A., Levy, O., Stoyanov, V., Zettlemoyer, L.: BART: Denoising Sequence-to-Sequence Pre-training for Natural Language Generation, Translation, and Comprehension. arXiv (2019), URL `https://arxiv.org/abs/1910.13461` 

- [114] Li, B., Mellou, K., Zhang, B., Pathuri, J., Menache, I.: Large Language Models for Supply Chain Optimization. arXiv (2023), doi:10.48550/arXiv.2307.03875 

26 

LLMS FOR COMBINATORIAL OPTIMIZATION 

DA ROS ET AL. 

- [115] Li, B., Zhang, K., Sun, Y., Zou, J.: Research on Travel Route Planning Optimization based on Large Language Model. In: 2024 6th International Conference on Data-driven Optimization of Complex Systems (DOCS), pp. 352–357, IEEE, Hangzhou, China (2024), doi:10.1109/DOCS63458.2024.10704489 

- [116] Li, Q., Zhang, L., Mak-Hau, V.: Synthesizing mixed-integer linear programming models from natural language descriptions. arXiv (2023), doi:10.48550/arXiv.2311.15271 

- [117] Li, R., Allal, L.B., Zi, Y., Muennighoff, N., Kocetkov, D., Mou, C., Marone, M., Akiki, C., Li, J., Chim, J., et al.: StarCoder: May the Source Be with You! arXiv (2023), doi:10.48550/arXiv.2305.06161 

- [118] Li, S., Kulkarni, J., Menache, I., Wu, C., Li, B.: Towards Foundation Models for Mixed Integer Linear Programming. arXiv (2024), doi:10.48550/arXiv.2410.08288 

- [119] Li, X., Chu, Q., Chen, Y., Liu, Y., Liu, Y., Yu, Z., Chen, W., Qian, C., Shi, C., Yang, C.: Facilitating Large Language Model-based Graph Analysis via Multi-Agent Collaboration. arXiv (2024), doi:10.48550/arXiv.2410. 18032 

- [120] Lin, C.Y.: ROUGE: A Package for Automatic Evaluation of Summaries. In: Text Summarization Branches Out, pp. 74–81, ACL, Barcelona, Spain (Jul 2004), URL `https://aclanthology.org/W04-1013` 

- [121] Lin, H., Zhang, L., Zheng, R., Zheng, Y.: The prevalence, metabolic risk and effects of lifestyle intervention for metabolically healthy obesity: a systematic review and meta-analysis: A PRISMA-compliant article. Medicine **96** (47) (2017), doi:10.1097/MD.0000000000008838 

- [122] Lindauer, M., Eggensperger, K., Feurer, M., Biedenkapp, A., Deng, D., Benjamins, C., Ruhkopf, T., Sass, R., Hutter, F.: SMAC3: A Versatile Bayesian Optimization Package for Hyperparameter Optimization. Journal of Machine Learning Research **23** (54), 1–9 (2022), URL `http://jmlr.org/papers/v23/21-0888.html` 

- [123] Ling, W., Yogatama, D., Dyer, C., Blunsom, P.: Program Induction by Rationale Generation: Learning to Solve and Explain Algebraic Word Problems. In: Proceedings of the 55th Annual Meeting of the ACL (Volume 1: Long Papers), pp. 158–167, ACL, Vancouver, Canada (Jul 2017), doi:10.18653/v1/P17-1015 

- [124] Liu, F., Lin, X., Wang, Z., Yao, S., Tong, X., Yuan, M., Zhang, Q.: Large Language Model for Multi-objective Evolutionary Optimization. arXiv (2024), doi:10.48550/arXiv.2310.12541 

- [125] Liu, F., Tong, X., Yuan, M., Lin, X., Luo, F., Wang, Z., Lu, Z., Zhang, Q.: Evolution of Heuristics: Towards Efficient Automatic Algorithm Design Using Large Language Model. arXiv (2024), doi:10.48550/arXiv.2401. 02051 

- [126] Liu, F., Tong, X., Yuan, M., Lin, X., Luo, F., Wang, Z., Lu, Z., Zhang, Q.: Evolution of Heuristics: Towards Efficient Automatic Algorithm Design Using Large Language Model. In: Proceedings of the 41st International Conference on Machine Learning, ICML’24, JMLR.org, Vienna, Austria (2024), URL `https://openreview. net/forum?id=BwAkaxqiLB` 

- [127] Liu, F., Tong, X., Yuan, M., Zhang, Q.: Algorithm Evolution Using Large Language Model. arXiv (2023), doi:10.48550/arXiv.2311.15249 

- [128] Liu, F., Yao, Y., Guo, P., Yang, Z., Zhao, Z., Lin, X., Tong, X., Yuan, M., Lu, Z., Wang, Z., Zhang, Q.: A Systematic Survey on Large Language Models for Algorithm Design. arXiv (2024), doi:10.48550/arXiv.2410. 14716 

- [129] Liu, F., Zhang, R., Xie, Z., Sun, R., Li, K., Lin, X., Wang, Z., Lu, Z., Zhang, Q.: LLM4AD: A Platform for Algorithm Design with Large Language Model. arXiv (2024), doi:10.48550/arXiv.2412.17287 

- [130] Liu, S., Chen, C., Qu, X., Tang, K., Ong, Y.S.: Large Language Models as Evolutionary Optimizers. arXiv (2024), doi:10.48550/arXiv.2310.19046 

- [131] Liu, Y., Wu, F., Liu, Z., Wang, K., Wang, F., Qu, X.: Can language models be used for real-world urban-delivery route optimization? The Innovation **4** (6), 100520 (2023), ISSN 2666-6758, doi:10.1016/j.xinn.2023.100520 

- [132] Llama Team, A.a.M.: The Llama 3 Herd of Models. arXiv (2024), doi:10.48550/arXiv.2407.21783 

- [133] Londe, M.A., Pessoa, L.S., Andrade, C.E., Resende, M.G.: Biased random-key genetic algorithms: A review. European Journal of Operational Research **318** (2) (2024), ISSN 0377-2217, doi:10.1016/j.ejor.2024.03.030 

- [134] Long, S., Tan, J., Mao, B., Tang, F., Li, Y., Zhao, M., Kato, N.: A Survey on Intelligent Network Operations and Performance Optimization Based on Large Language Models. IEEE Communications Surveys & Tutorials pp. 1–1 (2025), doi:10.1109/COMST.2025.3526606 

- [135] Lopes Silva, M.A., de Souza, S.R., Freitas Souza, M.J., de França Filho, M.F.: Hybrid metaheuristics and multi-agent systems for solving optimization problems: A review of frameworks and a comparative analysis. Applied Soft Computing **71** , 433–459 (2018), ISSN 1568-4946, doi:10.1016/j.asoc.2018.06.050 

27 

LLMS FOR COMBINATORIAL OPTIMIZATION 

DA ROS ET AL. 

- [136] Lozhkov, A., Li, R., Allal, L.B., Cassano, F., Lamy-Poirier, J., Tazi, N., Tang, A., Pykhtar, D., Liu, J., Wei, Y., et al.: StarCoder 2 and The Stack v2: The Next Generation. arXiv (2024), doi:10.48550/arXiv.2402.19173 

- [137] Luo, Z., Song, X., Huang, H., Lian, J., Zhang, C., Jiang, J., Xie, X.: GraphInstruct: Empowering Large Language Models with Graph Understanding and Reasoning Capability. arXiv (2024), URL `https://arxiv.org/abs/ 2403.04483` 

- [138] López-Ibáñez, M., Dubois-Lacoste, J., Pérez Cáceres, L., Birattari, M., Stützle, T.: The irace package: Iterated racing for automatic algorithm configuration. Operations Research Perspectives **3** , 43–58 (2016), ISSN 22147160, doi:10.1016/j.orp.2016.09.002 

- [139] Maddigan, P., Susnjak, T.: Chat2VIS: Generating Data Visualizations via Natural Language Using ChatGPT, Codex and GPT-3 Large Language Models. IEEE Access **11** , 45181–45193 (2023), doi:10.1109/ACCESS.2023. 3274199 

- [140] Manica, M., Born, J., Cadow, J., Christofidellis, D., Dave, A., Clarke, D., Teukam, Y.G.N., Giannone, G., Hoffman, S.C., Buchan, M., Chenthamarakshan, V., Donovan, T., Hsu, H.H., Zipoli, F., Schilter, O., Kishimoto, A., Hamada, L., Padhi, I., Wehden, K., McHugh, L., Khrabrov, A., Das, P., Takeda, S., Smith, J.R.: Accelerating material design with the generative toolkit for scientific discovery. npj Computational Materials **9** (1), 69 (5 2023), ISSN 2057-3960, doi:10.1038/s41524-023-01028-1 

- [141] Manyika, J., Hsiao, S.: An overview of Bard: an early experiment with generative AI. AI. Google Static Documents (2023), URL `https://ai.google/static/documents/google-about-bard.pdf` , accessed: 2024-06-27 

- [142] Mao, J., Zou, D., Sheng, L., Liu, S., Gao, C., Wang, Y., Li, Y.: Identify Critical Nodes in Complex Network with Large Language Models. arXiv (2024), doi:10.48550/arXiv.2403.03962 

- [143] Martinek, A., Łukasik, S., Gandomi, A.H.: Large Language Models as Tuning Agents of Metaheuristics. In: 32nd European Symposium on Artificial Neural Networks, Computational Intelligence and Machine Learning (ESANN 2024), pp. 631–636, i6doc.com, Bruges, Belgium (2024), doi:10.14428/ESANN/2024.ES2024-209 

- [144] Martí, R., Sevaux, M., Sörensen, K.: Fifty years of metaheuristics. European Journal of Operational Research **318** (2) (2024), ISSN 0377-2217, doi:10.1016/j.ejor.2024.04.004 

- [145] Meadows, J., Freitas, A.: A Survey in Mathematical Language Processing. arXiv (2024), doi:10.48550/arXiv. 2205.15231 

- [146] Michailidis, K., Tsouros, D., Guns, T.: Constraint Modelling with LLMs Using In-Context Learning. In: 30th International Conference on Principles and Practice of Constraint Programming (CP 2024), Leibniz International Proceedings in Informatics (LIPIcs), vol. 307, pp. 20:1–20:27, Schloss Dagstuhl – Leibniz-Zentrum für Informatik, Dagstuhl, Germany (2024), doi:10.4230/LIPIcs.CP.2024.20 

- [147] Mo, K., Liu, W., Shen, F., Xu, X., Xu, L., Su, X., Zhang, Y.: Precision Kinematic Path Optimization for High-DoF Robotic Manipulators Utilizing Advanced Natural Language Processing Models. In: 2024 5th International Conference on Electronic Communication and Artificial Intelligence (ICECAI), pp. 649–654, IEEE, Shenzhen, China (2024), doi:10.1109/ICECAI62591.2024.10675146 

- [148] Moher, D., Cook, D.J., Eastwood, S., Olkinm, I., Rennie, D., Stroup, D.F.: Improving The Quality of Reports of Meta-analyses of Randomised Controlled Trials: The QUOROM Statement. The Lancet **354** (9193), 1896–1900 (1999), ISSN 0140-6736, doi:10.1016/S0140-6736(99)04149-5 

- [149] Moher, D., Liberati, A., Tetzlaff, J., Altman, D.G., Group, T.P.: Preferred Reporting Items for Systematic Reviews and Meta-Analyses: The PRISMA Statement. PLOS Medicine **6** (7), 1–6 (07 2009), doi:10.1371/journal. pmed.1000097 

- [150] Moser, M., Musliu, N., Schaerf, A., Winter, F.: Exact and metaheuristic approaches for unrelated parallel machine scheduling. Journal of Scheduling **25** (5), 507–534 (2022), doi:10.1007/s10951-021-00714-6 

- [151] Mostajabdaveh, M., Yu, T.T., Dash, S.C.B., Ramamonjison, R., Byusa, J.S., Carenini, G., Zhou, Z., Zhang, Y.: Evaluating LLM Reasoning in the Operations Research Domain with ORQA. arXiv (2024), doi:10.48550/arXiv. 2412.17874 

- [152] Mostajabdaveh, M., Yu, T.T., Ramamonjison, R., Carenini, G., Zhou, Z., Zhang, Y.: Optimization modeling and verification from problem specifications using a multi-agent multi-stage LLM framework. INFOR: Information Systems and Operational Research **62** (4), 599–617 (2024), doi:10.1080/03155986.2024.2381306 

- [153] Nana Teukam, Y.G., Zipoli, F., Laino, T., Criscuolo, E., Grisoni, F., Manica, M.: Integrating Genetic Algorithms and Language Models for Enhanced Enzyme Design. Briefings in Bioinformatics **26** (1), bbae675 (Nov 2024), doi:10.1093/bib/bbae675 

28 

LLMS FOR COMBINATORIAL OPTIMIZATION 

DA ROS ET AL. 

- [154] Nassen, L.M., Vandebosch, H., Poels, K., Karsay, K.: Opt-out, abstain, unplug. A systematic review of the voluntary digital disconnection literature. Telematics and Informatics **81** , 101980 (2023), ISSN 0736-5853, doi:https://doi.org/10.1016/j.tele.2023.101980 

- [155] Nethercote, N., Stuckey, P.J., Becket, R., Brand, S., Duck, G.J., Tack, G.: MiniZinc: Towards a Standard CP Modelling Language. In: Principles and Practice of Constraint Programming – CP 2007, pp. 529–543, Springer Berlin Heidelberg, Berlin, Heidelberg (2007), ISBN 978-3-540-74970-7, doi:10.1007/978-3-540-74970-7_38 

- [156] Ning, Y., Liu, J., Qin, L., Xiao, T., Xue, S., Huang, Z., Liu, Q., Chen, E., Wu, J.: A Novel Approach for Auto-Formulation of Optimization Problems. arXiv (2023), doi:10.48550/arXiv.2302.04643 

- [157] Obata, K., Aoki, T., Horii, T., Taniguchi, T., Nagai, T.: LiP-LLM: Integrating Linear Programming and Dependency Graph With Large Language Models for Multi-Robot Task Planning. IEEE Robotics and Automation Letters **10** (2), 1122–1129 (2025), doi:10.1109/LRA.2024.3518105 

- [158] Object Management Group: Business Process Model and Notation (BPMN), Version 2.0 (January 2011), URL `https://www.omg.org/spec/BPMN/2.0/PDF` , retrieved from the Object Management Group website 

- [159] Ochoa, G., Malan, K.M., Blum, C.: Search trajectory networks: A tool for analysing and visualising the behaviour of metaheuristics. Applied Soft Computing **109** , 107492 (2021), ISSN 1568-4946, doi:10.1016/j.asoc. 2021.107492 

- [160] OpenAI: GPT-4 Technical Report. arXiv (2024), doi:10.48550/arXiv.2303.08774 

- [161] OpenAI Team: Reproducible outputs (2024), URL `https://platform.openai.com/docs/ advanced-usage/reproducible-outputs` , accessed: 2024-08-26 

- [162] Ouyang, L., Wu, J., Jiang, X., Almeida, D., Wainwright, C., Mishkin, P., Zhang, C., Agarwal, S., Slama, K., Ray, A., et al.: Training language models to follow instructions with human feedback. Advances in Neural Information Processing Systems **35** , 27730–27744 (2022), URL `https://proceedings.neurips.cc/paper_files/ paper/2022/file/b1efde53be364a73914f58805a001731-Paper-Conference.pdf` 

- [163] Page, M.J., McKenzie, J.E., Bossuyt, P.M., Boutron, I., Hoffmann, T.C., Mulrow, C.D., Shamseer, L., Tetzlaff, J.M., Akl, E.A., Brennan, S.E., Chou, R., Glanville, J., Grimshaw, J.M., Hróbjartsson, A., Lalu, M.M., Li, T., Loder, E.W., Mayo-Wilson, E., McDonald, S., McGuinness, L.A., Stewart, L.A., Thomas, J., Tricco, A.C., Welch, V.A., Whiting, P., Moher, D.: The PRISMA 2020 Statement: An Updated Guideline For Reporting Systematic Reviews. BMJ **372** (2021), doi:10.1136/bmj.n71 

- [164] Page, M.J., Moher, D., Bossuyt, P.M., Boutron, I., Hoffmann, T.C., Mulrow, C.D., Shamseer, L., Tetzlaff, J.M., Akl, E.A., Brennan, S.E., Chou, R., Glanville, J., Grimshaw, J.M., Hróbjartsson, A., Lalu, M.M., Li, T., Loder, E.W., Mayo-Wilson, E., McDonald, S., McGuinness, L.A., Stewart, L.A., Thomas, J., Tricco, A.C., Welch, V.A., Whiting, P., McKenzie, J.E.: PRISMA 2020 Explanation and Elaboration: Updated Guidance And Exemplars For Reporting Systematic Reviews. BMJ **372** (2021), doi:10.1136/bmj.n160 

- [165] Pagnozzi, F., Stützle, T.: Automatic design of hybrid stochastic local search algorithms for permutation flowshop problems with additional constraints. Operations Research Perspectives **8** , 100180 (2021), ISSN 2214-7160, doi:https://doi.org/10.1016/j.orp.2021.100180 

- [166] Pallagani, V., Muppasani, B.C., Roy, K., Fabiano, F., Loreggia, A., Murugesan, K., Srivastava, B., Rossi, F., Horesh, L., Sheth, A.: On the prospects of incorporating large language models (LLMs) in automated planning and scheduling (APS). In: Proceedings of the Thirty-Fourth International Conference on Automated Planning and Scheduling, ICAPS ’24, AAAI Press, Alberta, Canada (2025), ISBN 1-57735-889-9, doi:10.1609/icaps. v34i1.31503 

- [167] Pan, R., Xing, S., Diao, S., Sun, W., Liu, X., Shum, K., Zhang, J., Pi, R., Zhang, T.: Plum: Prompt learning using metaheuristics. In: Findings of the ACL: ACL 2024, pp. 2177–2197, ACL, Bangkok, Thailand (Aug 2024), doi:10.18653/v1/2024.findings-acl.129 

- [168] Parejo, J.A., Ruiz-Cortés, A., Lozano, S., Fernandez, P.: Metaheuristic optimization frameworks: a survey and benchmarking. Soft Computing **16** (3), 527–561 (mar 2012), ISSN 1432-7643, doi:10.1007/s00500-011-0754-8 

- [169] Perron, L., Furnon, V.: OR-Tools (2024), URL `https://developers.google.com/optimization/` , software 

- [170] Peters, M.E., Neumann, M., Iyyer, M., Gardner, M., Clark, C., Lee, K., Zettlemoyer, L.: Deep Contextualized Word Representations. In: Proceedings of the 2018 Conference of the North American Chapter of the ACL: Human Language Technologies, Volume 1 (Long Papers), pp. 2227–2237, ACL, New Orleans, Louisiana (Jun 2018), doi:10.18653/v1/N18-1202 

29 

LLMS FOR COMBINATORIAL OPTIMIZATION 

DA ROS ET AL. 

- [171] Pluhacek, M., Kazikova, A., Kadavy, T., Viktorin, A., Senkerik, R.: Leveraging large language models for the generation of novel metaheuristic optimization algorithms. In: Proceedings of the Companion Conference on Genetic and Evolutionary Computation, pp. 1812–1820, GECCO ’23 Companion, ACM, New York, NY, USA (2023), ISBN 9798400701207, doi:10.1145/3583133.3596401 

- [172] Pluhacek, M., Kazikova, A., Viktorin, A., Kadavy, T., Senkerik, R.: Investigating the Potential of AI-Driven Innovations for Enhancing Differential Evolution in Optimization Tasks. In: 2023 IEEE International Conference on Systems, Man, and Cybernetics (SMC), pp. 1070–1075, IEEE, Honolulu, Oahu, HI, USA (2023), doi: 10.1109/SMC53992.2023.10394233 

- [173] Pluhacek, M., Kovac, J., Viktorin, A., Janku, P., Kadavy, T., Senkerik, R.: Using LLM for Automatic Evolvement of Metaheuristics from Swarm Algorithm SOMA. In: Proceedings of the Genetic and Evolutionary Computation Conference Companion, p. 2018–2022, GECCO ’24 Companion, ACM, New York, NY, USA (2024), ISBN 9798400704956, doi:10.1145/3638530.3664181 

- [174] Pop, P.C., Cosma, O., Sabo, C., Pop Sitar, C.: A comprehensive survey on the generalized traveling salesman problem. European Journal of Operational Research **314** (3), 819–835 (2024), ISSN 0377-2217, doi:10.1016/j. ejor.2023.07.022 

- [175] Qwen Team, A.G.: Qwen Technical Report. arXiv (2023), doi:10.48550/arXiv.2309.16609 

- [176] Qwen Team, A.G.: Qwen2 Technical Report. arXiv (2024), doi:10.48550/arXiv.2407.10671 

- [177] Rafailov, R., Sharma, A., Mitchell, E., Ermon, S., Manning, C.D., Finn, C.: Direct Preference Optimization: Your Language Model is Secretly a Reward Model. arXiv (2024), doi:10.48550/arXiv.2305.18290) 

- [178] Raffel, C., Shazeer, N., Roberts, A., Lee, K., Narang, S., Matena, M., Zhou, Y., Li, W., Liu, P.J., et al.: Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer. arXiv (2023), doi:10.48550/arXiv.1910. 10683 

- [179] Ramamonjison, R., Li, H., Yu, T., He, S., Rengan, V., Banitalebi-dehkordi, A., Zhou, Z., Zhang, Y.: Augmenting Operations Research with Auto-Formulation of Optimization Models From Problem Descriptions. In: Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing: Industry Track, pp. 29–62, ACL, Abu Dhabi, UAE (Dec 2022), doi:10.18653/v1/2022.emnlp-industry.4 

- [180] Ramamonjison, R., Yu, T.T., Li, R., Li, H., Carenini, G., Ghaddar, B., He, S., Mostajabdaveh, M., BanitalebiDehkordi, A., Zhou, Z., Zhang, Y.: NL4Opt Competition: Formulating Optimization Problems Based on Their Natural Language Descriptions. arXiv (2023), doi:10.48550/arXiv.2303.08233 

- [181] Régin, F., De Maria, E., Bonlarron, A.: Combining Constraint Programming Reasoning with Large Language Model Predictions. In: 30th International Conference on Principles and Practice of Constraint Programming (CP 2024), Leibniz International Proceedings in Informatics (LIPIcs), vol. 307, pp. 25:1–25:18, Schloss Dagstuhl – Leibniz-Zentrum für Informatik, Dagstuhl, Germany (2024), doi:10.4230/LIPIcs.CP.2024.25 

- [182] Reinhart, W.F., Statt, A.: Large language models design sequence-defined macromolecules via evolutionary optimization. NPJ Computational Materials **10** (1), 262 (2024), doi:10.1038/s41524-024-01449-6 

- [183] Romanko, O., Narayan, A., Kwon, R.H.: ChatGPT-Based Investment Portfolio Selection. SN Operations Research Forum **4** (4), 1–27 (December 2023), doi:10.1007/s43069-023-00277-6 

- [184] Romera-Paredes, B., Barekatain, M., Novikov, A., Balog, M., Kumar, M.P., Dupont, E., Ruiz, F.J.R., Ellenberg, J.S., Wang, P., Fawzi, O., Kohli, P., Fawzi, A.: Mathematical discoveries from program search with large language models. Nature **625** (7995), 468–475 (1 2024), ISSN 1476-4687, doi:10.1038/s41586-023-06924-6 

- [185] Ross, J., Stevenson, F., Lau, R., Murray, E.: Factors that influence the implementation of e-health: a systematic review of systematic reviews (an update). Implementation Science **11** (1), 146 (Oct 2016), ISSN 1748-5908, doi:10.1186/s13012-016-0510-7 

- [186] Rossi, F., Van Beek, P., Walsh, T.: Handbook of constraint programming. Elsevier, Amsterdam (2006), ISBN 9780444527264, URL `https://www.dcs.gla.ac.uk/~pat/cpM/papers/CP_ Handbook-20060315-final.pdf` 

- [187] Saka, A., Taiwo, R., Saka, N., Salami, B.A., Ajayi, S., Akande, K., Kazemi, H.: GPT models in construction industry: Opportunities, limitations, and a use case validation. Developments in the Built Environment **17** , 100300 (2024), ISSN 2666-1659, doi:https://doi.org/10.1016/j.dibe.2023.100300 

- [188] Sartori, C.C., Blum, C., Bistaffa, F., Rodríguez Corominas, G.: Metaheuristics and Large Language Models Join Forces: Toward an Integrated Optimization Approach. IEEE Access **13** , 2058–2079 (2025), doi:10.1109/ ACCESS.2024.3524176 

30 

LLMS FOR COMBINATORIAL OPTIMIZATION 

DA ROS ET AL. 

- [189] Schäfer, M., Nadi, S., Eghbali, A., Tip, F.: An Empirical Evaluation of Using Large Language Models for Automated Unit Test Generation. IEEE Transactions on Software Engineering **50** (1), 85–105 (2024), doi: 10.1109/TSE.2023.3334955 

- [190] Shao, Z., Wang, P., Zhu, Q., Xu, R., Song, J., Bi, X., Zhang, H., Zhang, M., Li, Y.K., Wu, Y., Guo, D.: DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models. arXiv (2024), doi:10.48550/arXiv.2402.03300 

- [191] Shaw, P.: Principles and Practice of Constraint Programming — CP98. In: 4th International Conference, CP98, Pisa, Italy, October 26-30, 1998: Proceedings, Lecture Notes in Computer Science, vol. 1520, Springer, Berlin (1998), ISBN 978-3540659290, doi:10.1007/3-540-49481-2 

- [192] Singla, A., Singh, A., Kukreja, K.: A bi-objective _ϵ_ -constrained framework for quality-cost optimization in language model ensembles. arXiv (2023), doi:10.48550/arXiv.2312.16119 

- [193] Soprano, M., Roitero, K., La Barbera, D., Ceolin, D., Spina, D., Demartini, G., Mizzaro, S.: Cognitive Biases in Fact-Checking and Their Countermeasures: A Review. Information Processing & Management **61** (3), 103672 (2024), ISSN 0306-4573, doi:10.1016/j.ipm.2024.103672 

- [194] Sörensen, K., Sevaux, M., Glover, F.: A History of Metaheuristics, pp. 791–808. Springer International Publishing, Cham (2018), ISBN 978-3-319-07124-4, doi:10.1007/978-3-319-07124-4_4 

- [195] Srivastava, A., Rastogi, A., Rao, A., Shoeb, A.A.M., Abid, A., Fisch, A., Brown, A.R., Santoro, A., Gupta, A., Garriga-Alonso, A., et al.: Beyond the Imitation Game: Quantifying and Extrapolating the Capabilities of Language Models. arXiv (2022), doi:10.48550/arXiv.2206.04615 

- [196] Srivastava, B., Pallagani, V.: The Case for Developing a Foundation Model for Planning-like Tasks from Scratch (2024), doi:10.48550/arXiv.2404.04540 

- [197] van Stein, N., Bäck, T.: LLaMEA: A Large Language Model Evolutionary Algorithm for Automatically Generating Metaheuristics. IEEE Transactions on Evolutionary Computation pp. 1–1 (2024), doi:10.1109/TEVC. 2024.3497793 

- [198] van Stein, N., Vermetten, D., Bäck, T.: In-the-loop Hyper-Parameter Optimization for LLM-Based Automated Design of Heuristics. arXiv (2024), doi:10.48550/arXiv.2410.16309 

- [199] Steiner, E., Pferschy, U., Schaerf, A.: Curriculum-based university course timetabling considering individual course of studies. Central European Journal of Operations Research **32** (6 2024), ISSN 1613-9178, doi:10.1007/ s10100-024-00923-2 

- [200] Sui, J., Ding, S., Huang, X., Yu, Y., Liu, R., Xia, B., Ding, Z., Xu, L., Zhang, H., Yu, C., Bu, D.: A survey on deep learning-based algorithms for the traveling salesman problem. Frontiers of Computer Science **19** (6), 196322 (2024), doi:10.1007/s11704-024-40490-y 

- [201] Sun, Y., Ye, F., Zhang, X., Huang, S., Zhang, B., Wei, K., Cai, S.: AutoSAT: Automatically Optimize SAT Solvers via Large Language Models. arXiv (2024), doi:10.48550/arXiv.2402.10705 

- [202] Suzgun, M., Scales, N., Schärli, N., Gehrmann, S., Tay, Y., Chung, H.W., Chowdhery, A., Le, Q.V., Chi, E.H., Zhou, D., Wei, J.: Challenging BIG-Bench Tasks and Whether Chain-of-Thought Can Solve Them. arXiv (2022), doi:10.48550/arXiv.2210.09261 

- [203] Swan, J., Adriaensen, S., Bishr, M., Burke, E.K., Clark, J.A., De Causmaecker, P., Durillo, J., Hammond, K., Hart, E., Johnson, C.G., Kocsis, Z.A., Kovitz, B., Krawiec, K., Martin, S., Merelo, J.J., Minku, L.L., Özcan, E., Pappa, G.L., Pesch, E., Garcia-Sánchez, P., Schaerf, A., Sim, K., Smith, J., Stützle, T., Vo, S., Wagner, S., Yao, X.: A Research Agenda for Metaheuristic Standardization. In: Proceedings of the XI Metaheuristics International Conference (MIC 2015), pp. 1–3, University of Nottingham, Agadir, Morocco (June 2015), doi:10.1007/978-3-031-62912-9 

- [204] Swan, J., Adriaensen, S., Brownlee, A.E., Hammond, K., Johnson, C.G., Kheiri, A., Krawiec, F., Merelo, J., Minku, L.L., Özcan, E., Pappa, G.L., García-Sánchez, P., Sörensen, K., Voß, S., Wagner, M., White, D.R.: Metaheuristics “In the Large”. European Journal of Operational Research **297** (2), 393–406 (2022), ISSN 0377-2217, doi:10.1016/j.ejor.2021.05.042 

- [205] Swan, J., Adriænsen, S., Barwell, A.D., Hammond, K., White, D.R.: Extending the “Open-Closed Principle” to Automated Algorithm Configuration. Evolutionary Computation **27** (1), 173–193 (03 2019), ISSN 1063-6560, doi:10.1162/evco_a_00245 

- [206] Team, G.: Gemini 1.5: Unlocking multimodal understanding across millions of tokens of context. arXiv (2024), doi:10.48550/arXiv.2403.05530 

31 

LLMS FOR COMBINATORIAL OPTIMIZATION 

DA ROS ET AL. 

- [207] Team, G.: Gemini: A Family of Highly Capable Multimodal Models. arXiv (2024), doi:10.48550/arXiv.2312. 11805 

- [208] Team, G.: Gemma 2: Improving Open Language Models at a Practical Size. arXiv (2024), doi:10.48550/arXiv. 2408.00118 

- [209] Team, M.A.: Code Llama: Open Foundation Models for Code. arXiv (2024), doi:10.48550/arXiv.2308.12950 

- [210] Team, Y.: Yi: Open Foundation Models by 01.AI. arXiv (2024), doi:10.48550/arXiv.2403.04652 

- [211] Thieu, N.V., Mirjalili, S.: MEALPY: An Open-Source Library for Latest Meta-Heuristic Algorithms in Python. Journal of Systems Architecture **139** , 102871 (2023), doi:10.1016/j.sysarc.2023.102871 

- [212] Touvron, H., Lavril, T., Izacard, G., Martinet, X., Lachaux, M.A., Lacroix, T., Rozière, B., Goyal, N., Hambro, E., Azhar, F., Rodriguez, A., Joulin, A., Grave, E., Lample, G.: LLaMA: Open and Efficient Foundation Language Models. arXiv (2023), doi:10.48550/arXiv.2302.13971 

- [213] Tran, T.V.T., Hy, T.S.: Protein Design by Directed Evolution Guided by Large Language Models. IEEE Transactions on Evolutionary Computation pp. 1–1 (2024), doi:10.1109/TEVC.2024.3439690 

- [214] Tsouros, D., Verhaeghe, H., Kadıo˘glu, S., Guns, T.: Holy Grail 2.0: From Natural Language to Constraint Models. arXiv (2023), doi:10.48550/arXiv.2308.01589 

- [215] Tunstall, L., Beeching, E., Lambert, N., Rajani, N., Rasul, K., Belkada, Y., Huang, S., von Werra, L., Fourrier, C., Habib, N., Sarrazin, N., Sanseviero, O., Rush, A.M., Wolf, T.: Zephyr: Direct Distillation of LM Alignment. arXiv (2023), doi:10.48550/arXiv.2310.16944 

- [216] Tupayachi, J., Xu, H., Omitaomu, O.A., Camur, M.C., Sharmin, A., Li, X.: Towards Next-Generation Urban Decision Support Systems through AI-Powered Construction of Scientific Ontology Using Large Language Models—A Case in Optimizing Intermodal Freight Transportation. Smart Cities **7** (5), 2392–2421 (2024), doi:10.3390/smartcities7050094 

- [217] Urdaneta-Ponte, M.C., Mendez-Zorrilla, A., Oleagordia-Ruiz, I.: Recommendation Systems for Education: Systematic Review. Electronics **10** (14) (2021), ISSN 2079-9292, doi:10.3390/electronics10141611 

- [218] Ustyugov, V.: On Different Methods For Automated MILP Solver Configuration. In: 2024 20th International Asian School-Seminar on Optimization Problems of Complex Systems (OPCS), pp. 24–27, IEEE, Issyk-Kul Lake, Kyrgyzstan (2024), doi:10.1109/OPCS63516.2024.10720437 

- [219] Vass, J., Lackner, M.L., Mrkvicka, C., Musliu, N., Winter, F.: Exact and meta-heuristic approaches for the production leveling problem. Journal of Scheduling **25** (3), 339–370 (Jun 2022), ISSN 1099-1425, doi:10.1007/ s10951-022-00721-1 

- [220] Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A.N., Kaiser, Ł., Polosukhin, I.: Attention is All You Need. In: Advances in Neural Information Processing Systems, vol. 30, pp. 5998–6008, Curran Associates, Inc., Long Beach, CA, USA (2017), URL `https://proceedings.neurips.cc/paper_files/ paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf` 

- [221] Verduin, K., Weise, T., van den Berg, D.: Why is the traveling tournament problem not solved with genetic algorithms? In: Evo* 2023 – Late-Breaking Abstracts Volume, pp. 13–18, Species, Brno, Czech Republic (04 2023), URL `https://arxiv.org/pdf/2403.13950` 

- [222] Voboril, F., Ramaswamy, V.P., Szeider, S.: Generating Streamlining Constraints with Large Language Models. arXiv (2024), doi:10.48550/arXiv.2408.10268 

- [223] Wang, H., Feng, S., He, T., Tan, Z., Han, X., Tsvetkov, Y.: Can Language Models Solve Graph Problems in Natural Language? arXiv (2024), doi:10.48550/arXiv.2305.10037 

- [224] Wang, K., Chen, Z., Zheng, J.: OPD@NL4Opt: An ensemble approach for the NER task of the optimization problem. arXiv (2023), doi:10.48550/arXiv.2301.02459 

- [225] Wang, L., Ma, C., Feng, X., Zhang, Z., Yang, H., Zhang, J., Chen, Z., Tang, J., Chen, X., Lin, Y., Zhao, W.X., Wei, Z., Wen, J.: A Survey on Large Language Model Based Autonomous Agents. Frontiers of Computer Science **18** (6) (March 2024), ISSN 2095-2236, doi:10.1007/s11704-024-40231-1 

- [226] Wang, Y., Farooq, J., Ghazzai, H., Setti, G.: Multi-UAV Placement for Integrated Access and Backhauling Using LLM-Driven Optimization. TechRxive (2024), doi:10.36227/techrxiv.172833400.07230719/v1 

- [227] Wang, Y., Sambasivan, L.K., Fu, M., Mehrotra, P.: Pivoting Retail Supply Chain with Deep Generative Techniques: Taxonomy, Survey and Insights. arXiv (2024), doi:10.48550/arXiv.2403.00861 

32 

LLMS FOR COMBINATORIAL OPTIMIZATION 

DA ROS ET AL. 

- [228] Wasserkrug, S., Boussioux, L., Hertog, D.d., Mirzazadeh, F., Birbil, I., Kurtz, J., Maragno, D.: From Large Language Models and Optimization to Decision Optimization CoPilot: A Research Manifesto. arXiv (2024), doi:10.48550/arXiv.2402.16269 

- [229] Wei, J., Tay, Y., Bommasani, R., Raffel, C., Zoph, B., Borgeaud, S., Yogatama, D., Bosma, M., Zhou, D., Metzler, D., Chi, E.H., Hashimoto, T., Vinyals, O., Liang, P., Dean, J., Fedus, W.: Emergent Abilities of Large Language Models. arXiv (2022), doi:10.48550/arXiv.2206.07682 

- [230] Wei, J., Wang, X., Schuurmans, D., Bosma, M., Richter, B., Xia, F., Chi, E., Le, Q.V., Zhou, D.: Chain-of-thought prompting elicits reasoning in large language models. In: Advances in Neural Information Processing Systems, vol. 35, pp. 24824–24837, Curran Associates, Inc., Virtual Conference (2022), URL `https://proceedings.neurips.cc/paper_files/paper/2022/file/ 9d5609613524ecf4f15af0f7b31abca4-Paper-Conference.pdf` 

- [231] Windras Mara, S.T., Norcahyo, R., Jodiawan, P., Lusiantoro, L., Rifai, A.P.: A survey of adaptive large neighborhood search algorithms and applications. Computers & Operations Research **146** , 105903 (2022), ISSN 0305-0548, doi:https://doi.org/10.1016/j.cor.2022.105903 

- [232] Winter, F., Musliu, N., Demirovi´c, E., Mrkvicka, C.: Solution approaches for an automotive paint shop scheduling problem. In: Proceedings of the International Conference on Automated Planning and Scheduling, vol. 29, pp. 573–581, AAAI Press, Virtual Conference (2019), doi:10.1609/icaps.v29i1.3524 

- [233] Wolpert, D., Macready, W.: No free lunch theorems for optimization. IEEE Transactions on Evolutionary Computation **1** (1), 67–82 (1997), doi:10.1109/4235.585893 

- [234] Wu, C., Ge, Y., Zhang, X., Du, Y., He, S., Ji, Z., Lang, H.: The combined effects of Lamaze breathing training and nursing intervention on the delivery in primipara: A PRISMA systematic review meta-analysis. Medicine **100** (4) (2021), doi:10.1097/MD.0000000000023920 

- [235] Wu, X., Wang, D., Wen, L., Xiao, Y., Wu, C., Wu, Y., Yu, C., Maskell, D.L., Zhou, Y.: Neural Combinatorial Optimization Algorithms for Solving Vehicle Routing Problems: A Comprehensive Survey with Perspectives. arXiv (2024), doi:10.48550/arXiv.2406.00415 

- [236] Wu, X., Wu, S.h., Wu, J., Feng, L., Tan, K.C.: Evolutionary Computation in the Era of Large Language Model: Survey and Roadmap. arXiv (2024), doi:10.48550/arXiv.2401.10034 

- [237] Wu, X., Zhong, Y., Wu, J., Jiang, B., Tan, K.C.: Large Language Model-Enhanced Algorithm Selection: Towards Comprehensive Algorithm Representation. In: Proceedings of the Thirty-Third International Joint Conference on Artificial Intelligence, IJCAI ’24, International Joint Conferences on Artificial Intelligence, Jeju Island, South Korea (2024), doi:10.24963/ijcai.2024/579 

- [238] Xiao, Z., Zhang, D., Wu, Y., Xu, L., Wang, Y.J., Han, X., Fu, X., Zhong, T., Zeng, J., Song, M., Chen, G.: Chain-of-Experts: When LLMs Meet Complex Operations Research Problems. In: The Twelfth International Conference on Learning Representations (ICLR 2024), OpenReview, Virtual Conference (2024), URL `https: //openreview.net/forum?id=HobyL1B9CZ` 

- [239] Yang, C., Wang, X., Lu, Y., Liu, H., Le, Q.V., Zhou, D., Chen, X.: Large Language Models as Optimizers. arXiv (2024), doi:10.48550/arXiv.2309.03409 

- [240] Yang, Z., Wang, Y., Huang, Y., Guo, Z., Shi, W., Han, X., Feng, L., Song, L., Liang, X., Tang, J.: OptiBench Meets ReSocratic: Measure and Improve LLMs for Optimization Modeling (2024), doi:10.48550/arXiv.2407.09887 

- [241] Yao, S., Liu, F., Lin, X., Lu, Z., Wang, Z., Zhang, Q.: Multi-objective Evolution of Heuristic Using Large Language Model. arXiv (2024), doi:10.48550/arXiv.2409.16867 

- [242] Yatong, W., Yuchen, P., Yuqi, Z.: TS-EoH: An Edge Server Task Scheduling Algorithm Based on Evolution of Heuristic. arXiv (2024), doi:10.48550/arXiv.2409.09063 

- [243] Ye, H., Wang, J., Cao, Z., Berto, F., Hua, C., Kim, H., Park, J., Song, G.: ReEvo: Large Language Models as Hyper-Heuristics with Reflective Evolution. In: Proceedings of the Thirty-Eighth Annual Conference on Neural Information Processing Systems (NeurIPS 2024), pp. 1–32, Neural Information Processing Systems Foundation, Vancouver, Canada (2024), URL `https://openreview.net/forum?id=483IPG0HWL` 

- [244] You, H., Ye, Y., Zhou, T., Zhu, Q., Du, J.: Robot-Enabled Construction Assembly with Automated Sequence Planning Based on ChatGPT: RoboGPT. Buildings **13** (7) (2023), ISSN 2075-5309, doi:10.3390/buildings13071772 

- [245] Yu, H., Liu, J.: AutoRNet: Automatically Optimizing Heuristics for Robust Network Design via Large Language Models. arXiv (2024), doi:10.48550/arXiv.2410.17656 

- [246] Yu, H., Liu, J.: Deep Insights into Automated Optimization with Large Language Models and Evolutionary Algorithms. arXiv (2024), doi:10.48550/arXiv.2410.20848 

33 

LLMS FOR COMBINATORIAL OPTIMIZATION 

DA ROS ET AL. 

- [247] Zanazzo, E., Ceschia, S., Schaerf, A.: Solving the Integrated Patient-to-Room and Nurse-to-Patient Assignment by Simulated Annealing. In: Metaheuristics: 15th International Conference, MIC 2024, Lorient, France, June 4–7, 2024, Proceedings, Part I, p. 158–163, Springer-Verlag, Berlin, Heidelberg (2024), ISBN 978-3-031-62911-2, doi:10.1007/978-3-031-62912-9_15 

- [248] Zhang, J., Wang, W., Guo, S., Wang, L., Lin, F., Yang, C., Yin, W.: Solving General Natural-LanguageDescription Optimization Problems with Large Language Models. In: Proceedings of the 2024 Conference of the North American Chapter of the ACL: Human Language Technologies (Volume 6: Industry Track), pp. 483–490, ACL, Mexico City, Mexico (Jun 2024), doi:10.18653/v1/2024.naacl-industry.42 

- [249] Zhang, M., Yin, W., Wang, M., Shen, Y., Xiang, P., Wu, Y., Zhao, L., Pan, J., Jiang, H., Huang, K.: MindOpt Tuner: Boost the Performance of Numerical Software by Automatic Parameter Tuning (2023), doi:10.48550/ arXiv.2307.08085 

- [250] Zhang, R., Liu, F., Lin, X., Wang, Z., Lu, Z., Zhang, Q.: Understanding the Importance of Evolutionary Search in Automated Heuristic Design with Large Language Models. In: Parallel Problem Solving from Nature – PPSN XVIII, pp. 185–202, Springer Nature Switzerland, Cham (2024), doi:10.1007/978-3-031-70068-2_12 

- [251] Zhang, T., Kishore, V., Wu, F., Weinberger, K.Q., Artzi, Y.: BERTScore: Evaluating Text Generation with BERT. arXiv (2020), doi:10.48550/arXiv.1904.09675 

- [252] Zhang, Z., Wang, X., Zhang, Z., Li, H., Qin, Y., Zhu, W.: LLM4DyG: Can Large Language Models Solve Spatial-Temporal Problems on Dynamic Graphs? arXiv (2024), doi:10.48550/arXiv.2310.17110 

- [253] Zhao, Z., Cheng, S., Ding, Y., Zhou, Z., Zhang, S., Xu, D., Zhao, Y.: A Survey of Optimization-Based Task and Motion Planning: From Classical to Learning Approaches. IEEE/ASME Transactions on Mechatronics **29** (5), 1–27 (2024), doi:10.1109/TMECH.2024.3452509 

- [254] Çalık, H., Wauters, T., Vanden Berghe, G.: The exam location problem: Mathematical formulations and variants. Computers & Operations Research **161** , 106438 (2024), ISSN 0305-0548, doi:10.1016/j.cor.2023.106438 

34 

LLMS FOR COMBINATORIAL OPTIMIZATION 

DA ROS ET AL. 

# **A PRISMA Checklists** 

This appendix provides the “PRISMA 2020 for Abstracts Checklist” and the “PRISMA 2020 Checklist” [163, 164], which were used to guide our systematic review on the applications of LLMs in the field of Combinatorial Optimization (Section 5). 



### PRISMA 2020 for Abstracts Checklist 

|**Section and Topic**|**Item**<br>**#**|**Checklist item**|**Reported (Yes/No)**|
|---|---|---|---|
|**TITLE**||||
|Title|1|Identifythe report as a systematic review.|Yes|
|**BACKGROUND**||||
|Objectives|2|Provide an explicit statement of the main objective(s)orquestion(s)the review addresses.|Yes|
|**METHODS**||||
|Eligibilitycriteria|3|Specifythe inclusion and exclusion criteria for the review.|Yes|
|Information sources|4|Specify the information sources (e.g. databases, registers) used to identify studies and the<br>date when each was last searched.|Yes|
|Risk of bias|5|Specifythe methods used to assess risk of bias in the included studies.|No|
|Synthesis of results|6|Specifythe methods used topresent and synthesise results.|Yes|
|**RESULTS**||||
|Included studies|7|Give the total number of included studies and participants and summarise relevant<br>characteristics of studies.|Yes|
|Synthesis of results|8|Present results for main outcomes, preferably indicating the number of included studies and<br>participants for each. If meta-analysis was done, report the summary estimate and<br>confidence/credible interval. If comparing groups, indicate the direction of the effect (i.e.<br>whichgroupis favoured).|Yes|
|**DISCUSSION**||||
|Limitations of evidence|9|Provide a brief summary of the limitations of the evidence included in the review (e.g. study<br>risk of bias,inconsistencyand imprecision).|No|
|Interpretation|10|Provide ageneral interpretation of the results and important implications.|Yes|
|**OTHER**||||
|Funding|11|Specifytheprimarysource of fundingfor the review.|Withinpaper body|
|Registration|12|Provide the register name and registration number.|Not relevant|



_From:_ Page MJ, McKenzie JE, Bossuyt PM, Boutron I, Hoffmann TC, Mulrow CD, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. BMJ 2021;372:n71. doi: 10.1136/bmj.n71 

For more information, visit: http://www.prisma-statement.org/ 

35 

LLMS FOR COMBINATORIAL OPTIMIZATION 

DA ROS ET AL. 



### PRISMA 2020 Checklist 

|**Section and Topic**|**Item**<br>**#**|**Checklist item**|**Location where item is reported**|
|---|---|---|---|
|**TITLE**||||
|Title|1|Identify the report as a systematic review.|Title|
|**ABSTRACT**||||
|Abstract|2|See the PRISMA 2020 for Abstracts checklist.|Abstract, see PRISMA for Abstracts<br>checklist|
|**INTRODUCTION**||||
|Rationale|3|Describe the rationale for the review in the context of existing knowledge.|Section 1|
|Objectives|4|Provide an explicit statement of the objective(s)orquestion(s)the review addresses.|Section 2|
|**METHODS**||||
|Eligibilitycriteria|5|Specifythe inclusion and exclusion criteria for the review and how studies weregrouped for the syntheses.|Section 5.3.3|
|Information sources|6|Specify all databases, registers, websites, organisations, reference lists and other sources searched or consulted to identify studies. Specify<br>the date when each source was last searched or consulted.|Section 5.3.2|
|Search strategy|7|Present the full search strategies for all databases, registers and websites, includinganyfilters and limits used.|Section 5.3.2|
|Selection process|8|Specify the methods used to decide whether a study met the inclusion criteria of the review, including how many reviewers screened each<br>record and each report retrieved, whether they worked independently, and if applicable, details of automation tools used in the process.|Section 5.3.3|
|Data collection<br>process|9|Specify the methods used to collect data from reports, including how many reviewers collected data from each report, whether they worked<br>independently, any processes for obtaining or confirming data from study investigators, and if applicable, details of automation tools used in<br>the process.|Section 5.3.4|
|Data items|10a|List and define all outcomes for which data were sought. Specify whether all results that were compatible with each outcome domain in each<br>studywere sought(e.g. for all measures, timepoints, analyses), and if not, the methods used to decide which results to collect.|Section 6 and Appendix B|
||10b|List and define all other variables for which data were sought (e.g. participant and intervention characteristics, funding sources). Describe<br>anyassumptions made about anymissingor unclear information.|Section 6 and Appendix B|
|Study risk of bias<br>assessment|11|Specify the methods used to assess risk of bias in the included studies, including details of the tool(s) used, how many reviewers assessed<br>each studyand whether theyworked independently, and if applicable, details of automation tools used in theprocess.|Section 5.3|
|Effect measures|12|Specifyfor each outcome the effect measure(s) (e.g. risk ratio, mean difference)used in the synthesis orpresentation of results.|Not relevant|
|Synthesis methods|13a|Describe the processes used to decide which studies were eligible for each synthesis (e.g. tabulating the study intervention characteristics<br>and comparing against the planned groups for each synthesis (item #5)).|Section 5.3.3|
||13b|Describe any methods required to prepare the data for presentation or synthesis, such as handling of missing summary statistics, or data<br>conversions.|Not relevant|
||13c|Describe any methods used to tabulate or visually display results of individual studies and syntheses.|Section 6|
||13d|Describe any methods used to synthesize results and provide a rationale for the choice(s). If meta-analysis was performed, describe the<br>model(s), method(s) to identify the presence and extent of statistical heterogeneity, and software package(s) used.|Section 6|
||13e|Describe any methods used to explore possible causes of heterogeneity among study results (e.g. subgroup analysis, meta-regression).|Not relevant|
||13f|Describe any sensitivity analyses conducted to assess robustness of the synthesized results.|Not relevant|
|Reporting bias<br>assessment|14|Describe any methods used to assess risk of bias due to missing results in a synthesis (arising from reporting biases).|Section 8|
|Certainty<br>assessment|15|Describe any methods used to assess certainty (or confidence) in the body of evidence for an outcome.|Not relevant|
|**RESULTS**||||
|Study selection|16a|Describe the results of the search and selection process, from the number of records identified in the search to the number of studies<br>included in the review, ideallyusinga flow diagram.|Figure 2|



36 

LLMS FOR COMBINATORIAL OPTIMIZATION 

DA ROS ET AL. 



### PRISMA 2020 Checklist 

|**Section and Topic**|**Item**<br>**#**|**Checklist item**|**Location where item is reported**|
|---|---|---|---|
||16b|Cite studies that might appear to meet the inclusion criteria, but which were excluded, and explain whytheywere excluded.|Section 5.3.4|
|Study<br>characteristics|17|Cite each included study and present its characteristics.|Appendix B|
|Risk of bias in<br>studies|18|Present assessments of risk of bias for each included study.|Not relevant|
|Results of individual<br>studies|19|For all outcomes, present, for each study: (a) summary statistics for each group (where appropriate) and (b) an effect estimate and its<br>precision (e.g. confidence/credible interval), ideally using structured tables or plots.|Not relevant|
|Results of<br>|20a|For each synthesis, briefly summarise the characteristics and risk of bias among contributing studies.|Section 6|
|syntheses|20b|Present results of all statistical syntheses conducted. If meta-analysis was done, present for each the summary estimate and its precision<br>(e.g. confidence/credible interval) and measures of statistical heterogeneity. If comparing groups, describe the direction of the effect.|Not relevant|
||20c|Present results of all investigations of possible causes of heterogeneity among study results.|Section 6|
||20d|Present results of all sensitivity analyses conducted to assess the robustness of the synthesized results.|Not relevant|
|Reporting biases|21|Present assessments of risk of bias due to missing results (arising from reporting biases) for each synthesis assessed.|Section 8|
|Certainty of<br>evidence|22|Present assessments of certainty (or confidence) in the body of evidence for each outcome assessed.|Not relevant|
|**DISCUSSION**||||
|Discussion|23a|Provide a general interpretation of the results in the context of other evidence.|Section 6|
||23b|Discuss any limitations of the evidence included in the review.|Section 8|
||23c|Discuss any limitations of the review processes used.|Section 8|
||23d|Discuss implications of the results for practice, policy, and future research.|Section 7 and Section 9|
|**OTHER INFORMATIO**|**N**|||
|Registration and<br>|24a|Provide registration information for the review, including register name and registration number, or state that the review was not registered.|Not relevant|
|protocol|24b|Indicate where the review protocol can be accessed, or state that a protocol was not prepared.|Not relevant|
||24c|Describe and explain anyamendments to informationprovided at registration or in theprotocol.|Not relevant|
|Support|25|Describe sources of financial or non-financial support for the review, and the role of the funders or sponsors in the review.|End of thepaper, before references|
|Competinginterests|26|Declare anycompetinginterests of review authors.|End of thepaper, before references|
|Availability of data,<br>code and other<br>materials|27|Report which of the following are publicly available and where they can be found: template data collection forms; data extracted from<br>included studies; data used for all analyses; analytic code; any other materials used in the review.|The paper is self contained and all<br>the material is included either in the<br>paper or in the appendix.|



_From:_ Page MJ, McKenzie JE, Bossuyt PM, Boutron I, Hoffmann TC, Mulrow CD, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. BMJ 2021;372:n71. doi: 10.1136/bmj.n71 For more information, visit: http://www.prisma-statement.org/ 

37 

LLMS FOR COMBINATORIAL OPTIMIZATION 

DA ROS ET AL. 

# **B Description of Included Studies** 

This appendix provides the full list of the 103 studies found in the literature using the methodology described in Section 5 and analyzed in Section 6. For each study, we report its type (INCL4-EXCL4) and provide a brief description of the application of LLMs in the field of CO. When applicable, we also mention the specific COP involved. 

- Abdullin et al. [1] published a research study introducing a goal-oriented conversational agent to assist users in constructing accurate LP models. The LLM is used in the dialogue generation phase to automate the interaction between a conversational agent and a simulated user, effectively extracting necessary information to formulate LP models. 

- AhmadiTeshnizi et al. [3] published a research study investigating the usage of LLM to formulate and solve LP and MILP problems from NL descriptions. The LLM is employed to develop an agent that recognizes entities and translates NL descriptions into code. This code is subsequently used by a solver to find solutions and potentially debug them. The work has been extended by AhmadiTeshnizi et al. [2]. 

- Ahmed and Choudhury [4] published a research study to investigate the usage of LLMs for recognizing entities and translating NL descriptions in optimization problem formulations. A LLM is used for this task in both zero-shot and one-shot settings. 

- Alipour-Vaezi and Tsui [6] proposed a research study on using LLMs to extract domain knowledge in the context of the motion picture industry for portfolio optimization. 

- Almonacid [7] published a research study investigating LLM capabilities of generating optimization code. The LLM is used to generate the model and its code using MiniZinc, eventually debugging it. 

- Amarasinghe et al. [8] published a research study introducing a framework based on Copilot, designed to automate the generation of code from NL descriptions. The LLM is used to automate the generation of Python code employing the CPMpy library starting from business descriptions. 

- Bohnet et al. [19] published a research study on using LLMs in generating solutions for planning problems. 

- Borazjanizadeh et al. [20] published a research study on solving search problems using LLMs. The framework involves generating solution code and producing the solution in a specific format. The results were evaluated in terms of feasibility, correctness, and optimality. The study also introduces a new benchmark called SearchBench. 

- Cai et al. [23] published a position paper on the possible advantages LLMs can bring to evolutionary computation, including evolutionary-based optimization. 

- Chacón Sartori et al. [28] published a research study integrating LLMs into a web-based tool for visualizing the behavior of optimization algorithms. The LLM generates prompts for the tool, enabling users to comprehend how multiple algorithms behave when applied to specific instances of a COP. 

- Chen et al. [30] published a research study related to FunSearch [184]; specifically, it introduces the concept of uncertainty to maintain diversity in the population of codes while ensuring a balance between exploration and intensification during the search. The results are compared to FunSearch and Evolution of Heuristic [126]. 

- Chin et al. [32] published a research study addressing the resolution of a particular CO, the Montreal Capacitated Vehicle Routing Problem (FM-MCVRP). The LLM is used to train a model in a supervised manner on computationally inexpensive, sub-optimal solutions obtained algorithmically. 

- Da et al. [37] published a research study on integrating LLMs into traffic and routing contexts. Specifically, the framework enables user–LLM conversations, generates solutions based on domain knowledge, and allows for solution visualization and validation. 

- De La Rosa et al. [39] published a research study on using LLMs for travel planning. The LLM retrieves information about a given city and generates a route to visit specified landmarks. 

- De Zarzà et al. [40] published a research study addressing the resolution of problems in a specific CO domain (financial and budget optimization). The LLM is used to provide domain-specific advice to the user. 

- Dhanaraj et al. [45] published a research study on integrating human preferences into task scheduling for humanrobot teams using CP and LLMs. 

- Doan [47] published a research study on the topic of recognizing optimization entities. The LLM is used to recognize such entities from problem descriptions expressed in NL. 

- Elhenawy et al. [52] proposed a research study on solving the TSP using LLMs. Differently from other studies, this one uses the visual capabilities of LLMs. 

38 

LLMS FOR COMBINATORIAL OPTIMIZATION 

DA ROS ET AL. 

– Fan et al. [53] published a literature review exploring the integration of AI within the OR process, focusing on enhancing various stages such as parameter generation and model formulation. 

– Freuder [57] published a position paper discussing the role of LLMs in constraint satisfaction problems, where traditionally a crucial component is the dialogue between an optimization expert and a domain expert. The LLM is used to replace the optimization expert. 

- Gangwar and Kani [58] published a research study describing a method to translate NL descriptions into LP problem formulations. 

- Ghiani et al. [63] proposed a research study on using LLMs to integrate stakeholders’ preferences in decisionmaking processes. The methodology is applied to a last-mile delivery problem, and the LLM is used in two ways: to act as a construction heuristic and to set the weights of the optimizer (i.e., parameter tuning). 

- Guo et al. [69] published a research study on using LLMs to generate solutions. Specifically, the LLM is asked to mimic the behavior of well-known algorithms, such as HC. 

- Hao et al. [71] published a research study on using LLMs in planning. Specifically, LLMs are used to recognize entities, formulate the model, generate code, and catch errors. 

– Hao Chen and Li [72] published a research study on the usage of LLM in detecting model infeasibility. The LLM is used to provide NL descriptions of the optimization model itself, identify potential sources of infeasibility, and offer suggestions to make the model feasible. 

– He et al. [74] published a research study describing a method to generate LP problem formulations from NL descriptions. The LLM automates the transformation of text-based LP problem descriptions into structured formats, including entity recognition tasks. 

– Hu et al. [80] published a research study on finding solutions for graph-related problems. Additionally, an explainability layer is included to outline the reasoning process. 

- Huang et al. [81] published a research study on using LLMs to generate solutions for COPs. The experiments are conducted on the TSP. 

- Huang et al. [82] published a research study proposing a tool called OR-Instruct, used to create synthetic data tailored to optimization modeling. They test the approach by developing the IndustryOR dataset. 

– Huang et al. [84] published a literature review exploring the integration of LLM and optimization, considering both the perspective of LLM for optimization and optimization for LLM. The LLM is used as a black-box optimization search model or to generate optimization algorithms. 

– Huang et al. [86] published a research study proposing an optimization framework based on LLMs in the context of CVRP. The LLM is used to generate solutions using textual and visual prompts. 

- Huang et al. [87] published a research study addressing a specific class of COPs, the VRPs. The LLM is used to generate Python code from NL descriptions. 

- Jang [89] published a research study introducing a method to generate LP problem formulations. The LLM is used to translate NL description into LP formulation with entity recognition. 

- Jiang et al. [92] published a research study on using LLMs in an end-to-end approach: the LLM generates solution code directly from NL problem descriptions. 

- Jiang et al. [93] published a research study on using LLMs as optimizers, i.e., generating solutions in the context of planning. 

- Jin et al. [94] proposed a research study on using LLMs for problem formulation and code generation in the context of energy management. 

- Jobson and Li [95] published a research study on using LLMs to create feasible schedules for conferences. The LLM either groups presentation titles or generates solutions. 

- Ju et al. [96] published a research study on using LLMs for travel planning. LLMs recognize entities, create a corresponding MILP model, and solve the code. 

- Khan and Hamad [98] published a research study investigating LLMs’s capabilities in solving COPs. Specifically, LLMs either generate code or produce solutions. The study considers the TSP, the assignment problem, the transportation problem, and the shortest path problem. 

- Kikuta et al. [99] published a research study introducing a framework designed to explain the decision-making process for a certain class of problems. The LLM is used to explain the influence of each route edge and integrate counterfactual explanations. The COP addressed is the VRP. 

39 

LLMS FOR COMBINATORIAL OPTIMIZATION 

DA ROS ET AL. 

- Lai et al. [109] reviewed the literature on LLMs regarding their mathematical capabilities and briefly discussed their applications in CO, along with math word problems, geometry problems, and theorem proving. 

- Lawless et al. [110] published a research study on using LLMs to decide which cutting-plane strategy to use, thus assisting the MILP solver in choosing the appropriate parameters. 

- Lawless et al. [111] published a research study introducing a hybrid framework that integrates LLMs with CP to enable interactive decision support. The LLM is used in the preference elicitation phase to translate user input into structured constraint functions that the CP model can understand. The COP addressed is the Meeting Scheduling Problem, a specific Constraint Satisfaction Problem (CSP). 

- Li et al. [114] published a research study investigating the usage of LLM for reasoning about supply chain optimization. The LLM translates human queries into code, which is then utilized by an optimization solver. The final answer is returned via the LLM. 

- Li et al. [115] published a research study on using LLMs to generate solutions for a travel planning problem. The solutions are evaluated and validated with user feedback. 

- Li et al. [116] published a research study describing a method for synthesizing MILP models directly from NL descriptions. The LLM is used in the initial modeling phase to identify and classify decision variables and constraints. 

- Li et al. [118] published a research study on generating MILP codes (and instances) with LLMs to train learningbased methods. The pipeline is called MILP-Evolve. 

- Li et al. [119] published a research study on reasoning with graphs and networks. LLMs are used for knowledge extraction, entity recognition, and code generation in Python. 

- Liu et al. [124] published a research study on automating the design of search operators within multi-objective evolutionary procedures. The LLM is used to generate new individuals for each subproblem within the decomposition approach. 

- Liu et al. [125] published a research study on the usage of LLM in automatic heuristic design. The LLM is used to generate and evolve heuristic algorithm components, tested on TSPs, PFSP, and online Bin Packing Problem (BPP). 

- Liu et al. [127] published a research study on automatically generating optimization algorithms through an evolutionary framework. The LLM creates the initial solutions—each individual represents an algorithm—and applies mutation and crossover. The COP addressed is the TSP. 

- Liu et al. [128] published a literature review on using LLMs for algorithm design, including optimization algorithms. 

- Liu et al. [129] published a research study on algorithm design (heuristic code generation in Python), comparing results with other approaches such as FunSearch [184]. 

- Liu et al. [130] published a research study investigating LLMs as evolutionary combinatorial optimizers. A LLM selects parent solutions from a given population, performing crossover and mutation to generate offspring. The COP addressed is the TSP. 

- Liu et al. [131] published a research study investigating the integration of LLM in a delivery route optimization problem (a variation of the TSP). The LLM is used to gather knowledge regarding delivery patterns. 

- Long et al. [134] published a literature review on Network Operations and Performance Optimization, discussing potential roles for LLMs. 

- Mao et al. [142] published a research study investigating the usage of LLM to enhance evolutionary procedures for identifying critical nodes in a graph. The LLM crosses and mutates given functions to generate new code snippets. 

- Martinek et al. [143] proposed a research study in which LLMs are used to set MHs parameters, tested on the TSP and the Graph Coloring Problem. 

- Michailidis et al. [146] proposed a research study examining LLMs from entity recognition to solution generation. In the context of entity recognition, the authors used Ner4Opt [38]. 

- Mo et al. [147] published a research study on generating solutions using LLMs in the context of planning. 

- Mostajabdaveh et al. [151] published a research study analyzing the capabilities of LLMs in CO compared to human experts. A benchmark dataset called ORQUA is introduced, evaluating LLMs by asking them to answer questions based on NL problem descriptions. 

- Mostajabdaveh et al. [152] published a research study on using LLMs in an end-to-end optimization process, where the LLM generates solution code from NL problem descriptions. 

40 

LLMS FOR COMBINATORIAL OPTIMIZATION 

DA ROS ET AL. 

– Nana Teukam et al. [153] published a research study introducing a framework for optimizing enzymes. The LLM learns relationships between amino acid residues linked to structure and function, which are then used as input for an evolutionary search procedure aimed at improved catalytic performance. 

- Ning et al. [156] published a research study on recognizing optimization entities and providing LP problem formulations. The LLM is used to identify these entities from NL problem descriptions and to generate the LP model. 

- Obata et al. [157] proposed a research study on integrating LP and Dependency Graph approaches with LLMs for robot planning tasks. 

- Pallagani et al. [166] proposed a review on the applications of LLMs in planning, including language translation, plan generation, model construction, multi-agent planning, interactive planning, heuristic optimization, tool integration, and brain-inspired planning. 

- Ramamonjison et al. [179] published a research study to recognize entities and generate LP formulations from NL descriptions of LP problems. 

- Ramamonjison et al. [180] published a technical report on the NL4Opt competition, describing tasks, datasets, metrics for evaluation, and competition statistics. 

- Régin et al. [181] proposed a research study introducing GenCP, a framework combining CP with LLMs to handle structural constraints, including the semantic meaning in text generation. 

- Reinhart and Statt [182] proposed a research study on using LLMs to generate solutions for macromolecule design. The LLM was also used to explain or justify the proposed solution. 

- Romanko et al. [183] published a research study evaluating LLM stock-picking capability. The LLM is used to generate financial assets (solutions) for which a Mean-Variance Cardinality-Constrained Portfolio Optimization Model is computed. 

- Romera-Paredes et al. [184] published a research study proposing a new evolutionary procedure. The LLM is integrated to find new solutions and heuristics for COPs by evolving the code of an initial program skeleton at each step. The COPs addressed are the Cap Set problem and online bin packing. 

- Saka et al. [187] published a literature review investigating the usage of Generative Pre-trained Transformer (GPT) models in the Architecture, Engineering, and Construction Industry (AEC) industry. The review identifies opportunities, evaluates limitations, and validates a LLM use case for solution generation in AEC. 

- Sartori et al. [188] published a research study proposing a tool called OptiPattern. The LLM extracts knowledge from instances and integrates it into the MH (GA) process. The methodology is applied to a network problem. 

- Srivastava and Pallagani [196] published a position paper on the application of LLMs to planning and scheduling. 

- Sui et al. [200] published a literature review addressing deep learning methods for the TSP, which also mentions the role of LLMs. 

- Sun et al. [201] presented a research study on leveraging LLMs to solve SAT problems through a framework called AutoSAT. The framework automatically selects and optimizes heuristics within a predefined search space, building on conflict-driven clause learning solvers. 

- Tran and Hy [213] published a research study on using LLMs in protein design. The LLM generates feasible solutions from incomplete ones, acting similarly to a repair operator in local neighborhood search (LNS). 

- Tsouros et al. [214] published a research study introducing a framework for translating NL descriptions into CP. The LLM is used to produce executable code that can be run and debugged. 

- Tupayachi et al. [216] published a research study on applying LLMs to domain knowledge and entity recognition. Specifically, the LLM builds knowledge graphs on the problem at hand (e.g., transportation networks). 

- Ustyugov [218] published a research study on using LLMs for parameter tuning. Their methodology leverages BERT-based embeddings to predict solver parameters for MILP problems, aiming to automate and improve efficiency in Gurobi. 

- van Stein et al. [198] published a research study on integrating LLM-generated code with parameter tuning. The code is generated via LLaMEA [197], and the tuning is performed using SMAC [122]. While LLaMEA was originally designed for black-box optimization, this study also addresses CO (TSP and online bin packing). 

- Voboril et al. [222] proposed a research study introducing StreamLLM. The LLM enriches existing CP code in Python with additional constraints, aiming to reduce the search space. 

- Wang et al. [224] published a research study on the topic of recognizing optimization entities. The LLM identifies such entities from NL problem descriptions. 

41 

LLMS FOR COMBINATORIAL OPTIMIZATION 

DA ROS ET AL. 

– Wang et al. [226] published a research study on using LLMs as optimizers, i.e., generating solutions for drone placement. 

- Wasserkrug et al. [228] published a position paper advocating for introducing LLMs into CO to democratize optimization practices, helping non-experts across different sectors. 

- Wu et al. [235] published a literature review on vehicle routing, noting LLMs among other deep learning methods for TSP. 

- Wu et al. [236] published a literature review on the intersection between LLM and evolutionary computation, offering insights on possible research directions. 

- Wu et al. [237] published a research study on using LLMs for algorithm selection. More specifically, the LLM extracts features related to the underlying optimization algorithms. 

- Xiao et al. [238] published a research study introducing a multi-agent framework that automates the translation of problem descriptions into mathematical formulations and executable code. The LLM formulates models from NL descriptions and generates runnable code. 

- Yang et al. [239] published a research study on LLMs as optimizers. The LLM generates candidate solutions based on the problem description and previously evaluated solutions in the meta-prompt. The COP addressed is the TSP. 

- Yang et al. [240] proposed a research study on using LLMs for entity recognition and Python code generation. The final LLM output also includes the solution, though not directly computed by the LLM. Two datasets, Optibench and ReSocratic-29k, are introduced. 

- Yao et al. [241] published a research study on generating code that balances two objectives: efficiency of the code and the quality of solutions generated by it, tested on TSP and online bin packing. 

- Yatong et al. [242] published a research study on generating heuristic code for task scheduling in edge servers. 

- Ye et al. [243] published a research study on integrating LLM into hyper-heuristics generation. The LLM is used to generate heuristic algorithms in Python, tested on well-known COPs like TSP, CVRP, Orienteering Problem (OP), Decap Placement Problem (DPP), Multiple Knapsack Problem (MKP), and BPP. 

- You et al. [244] published a research study on a domain-specific COP (robot task sequencing). The LLM is used as a black-box optimizer. 

- Yu and Liu [245] published a research study on the usage of LLMs for robust network design. The LLM generates heuristic code. 

- Yu and Liu [246] published a position paper on the evolution of optimization toward automation, mentioning the integration of LLMs. 

- Zhang et al. [248] published a research study proposing OptLLM, a system that accepts user queries in natural language, converts them into mathematical formulations and programming code, and calls solvers for decisionmaking. OptLLM supports multi-round dialogues to iteratively refine modeling and solving. 

- Zhang et al. [250] published a research study on automated heuristic design (code generation). Results are compared with ReEvo [243] and FunSearch [184]. 

- Zhao et al. [253] published a literature review on optimization-based task and motion planning within a domainspecific CO. The review discusses how LLMs might generate domain knowledge and goal descriptions for planning methods. 

42 

LLMS FOR COMBINATORIAL OPTIMIZATION 

DA ROS ET AL. 

# **C Classification of Studies by Optimization Process Step** 

This appendix provides a breakdown of the identified studies with respect to the optimization process (Table 4). Columns display the general tasks (e.g., problem modeling), further divided into activities (e.g., domain knowledge). Furthermore, we report the optimization paradigm (e.g., CP) and technical details on the implementation (i.e., programming languages and commercial solvers). Each row groups together studies that share the same characteristics. The checkmark symbol (✓) identifies whether a study performs/is related to the column item. 

Table 4: Classification of the studies by Combinatorial Optimization task within the optimization process. 

|**Studies**|**Prob. **|**Mod.**<br>|**Sol. Meth.**|**Ben.**<br>|**Valid.**|**Models/Algorithms Types**|**Prog.**<br>**Lang.**|**Lib./**<br>**Solv.**|
|---|---|---|---|---|---|---|---|---|
||Domain Know.<br>Entity Rec.|<br>Model Creation|Code Gen.<br>Solution Gen.<br>Param. Tuning<br>Alg. Selection|Explain.<br>Visual Analysis|Sol. Valid.<br>Model Val.|CP<br>LP<br>ILP<br>MILP<br>Heuristic<br>HH<br>EA<br>GA<br>QAP<br>MOO<br>Non Linear<br>MH (general)<br>SAT|||
|[40,<br>131,<br>253]|✓||||||||
|[188]|✓|||||✓|||
|[39]|✓||✓||||||
|[95]|✓||✓|||✓|||
|[6,<br>216]|✓<br>✓||||||||
|[37]|✓<br>✓||✓|✓|✓||||
|[45]|✓<br>✓|✓||||✓|CP-<br>SAT||
|[119]|✓<br>✓||✓||||Python||
|[47,<br>224]|✓|||||✓|||
|[87]|✓||✓||✓||Python||
|[116]|✓|✓||||✓|||
|[4, 74,<br>89|✓|✓||||✓|||
|,<br>156,|||||||||
|179]|||||||||
|[157]|✓|✓|✓|||✓|||
|[214]|✓|✓|✓|||✓|Python|CMPy<br>[67]|
|[96]|✓|✓|✓|||✓|||
|[152]|✓|✓|✓||✓|✓<br>✓<br>✓||Zimpl|
|[71]|✓|✓|✓||✓|✓<br>✓|Python|MST,<br>Gurobi|
|[2,<br>3,<br>92,<br>240]|✓|✓|✓|||✓<br>✓|Python|Pyomo [73],<br>pyscipopt,<br>Gurobi [70]<br>(guro-<br>bipy)|
|[248]|✓|✓|✓||✓<br>✓|✓<br>✓<br>✓|MAPL<br>code|MindOpt<br>[249]|
|[146]|✓|✓|✓<br>✓|||✓|Python|CMPy<br>[67]|
|[181]||✓||||✓|||
|[82]||✓|✓|||✓<br>✓<br>✓<br>✓<br>✓|Python|coptpy|



_Continued on next page_ 

43 

LLMS FOR COMBINATORIAL OPTIMIZATION 

DA ROS ET AL. 

Table 4: Classification of the studies by Combinatorial Optimization task within the optimization process (continued). 

|**Studies**|**Prob. Mod.**|**Sol. Meth.**|**Ben.**|**Valid.**|**Models/Algorithms Types**|**Prog.**<br>**Lang.**|**Lib./**<br>**Solv.**|
|---|---|---|---|---|---|---|---|
||Domain Know.<br>Entity Rec.<br>Model Creation|Code Gen.<br>Solution Gen.<br>Param. Tuning<br>Alg. Selection|Explain.<br>Visual Analysis|Sol. Valid.<br>Model Val.|CP<br>LP<br>ILP<br>MILP<br>Heuristic<br>HH<br>EA<br>GA<br>QAP<br>MOO<br>Non Linear<br>MH (general)<br>SAT|||
|[94]|✓|✓|||✓|Python|CVXPY [46]|
|[98]<br>||✓<br>✓<br><br>||||Python||
|[63]<br>||✓<br>✓<br>|✓<br>||✓|||
|[80,<br>182]||✓|✓|||||
|[52]||✓|✓|✓<br>✓||||
|[218]<br>[115]<br>||✓<br>✓<br>||✓|✓|||
|[19,<br>32||✓||||||
|,<br>69, 81,<br>86, 93,<br>147,<br>187,<br>213,<br>226,<br>239,||||||||
|244]||||||||
|[143]||✓|||✓<br>✓|Python|Mealpy<br>[211]|
|[110]||✓|||✓|||
|[30,<br>129,<br>241||✓|||✓|Python||
|,<br>242,<br>245,||||||||
|250]||||||||
|[201]||✓|||✓|Cpp||
|[118]||✓|||✓|Python||
|[198]||✓|||✓|Python||
|[20]||✓<br>✓||||Python||
|[237]||✓||||||
|[1,58]|✓||||✓|||
|[238]|✓|✓||✓|✓<br>✓|Python|Gurobi [70]<br>(guro-<br>bipy)|
|[111]|✓|✓|||✓|Python||
|[127,<br>||✓|||✓|Python||
|184]||||||||
|[243]||✓|||✓|Python||
|[114]||✓|||✓|Python|Gurobi [70]<br>|
||||||||(guro-|
||||||||bipy)|
|[142]||✓|||✓|Python||
|[7]||✓|||✓|MiniZin|c|
|[125]||✓|||✓|Python||



_Continued on next page_ 

44 

LLMS FOR COMBINATORIAL OPTIMIZATION 

DA ROS ET AL. 

Table 4: Classification of the studies by Combinatorial Optimization task within the optimization process (continued). 

|**Studies**|**Prob. Mod.**<br>|**Sol. **|**Meth.**|**Ben.**<br>s|**Valid.**|**Models/Algorithms Types**|**Prog.**<br>**Lang.**|**Lib./**<br>**Solv.**|
|---|---|---|---|---|---|---|---|---|
||Domain Know.<br>Entity Rec.<br>Model Creation|Code Gen.<br>Solution Gen.|Param. Tuning<br>Alg. Selection|Explain.<br>Visual Analysi|Sol. Valid.<br>Model Val.|CP<br>LP<br>ILP<br>MILP<br>Heuristic<br>HH<br>EA<br>GA<br>QAP<br>MOO<br>Non Linear<br>MH (general)<br>SAT|||
|[8]||✓||||✓|Python|CMPy<br>[67]|
|[222]||✓||||✓|Python|MiniZinc|
|[183]||✓||||✓|Python|CPLEX [88]<br>(CVXPY [46])|
|[130]||✓||||✓|||
|[124]||✓||||✓<br>✓|Python|PyMoo [17]|
|[153]||✓||||✓|Python|GT4SD [140]|
|[99]||||✓|||||
|[28]||||✓|||R/Web<br>Int.||
|[72]|||||✓|✓|Python|Gurobi [70]<br>(Py-<br>omo [73])|



45 

LLMS FOR COMBINATORIAL OPTIMIZATION 

DA ROS ET AL. 

# **D Classification of Studies by LLM Architecture** 

This appendix provides the analysis of the retrieved studies in terms of LLMs (Table 5). We categorize each LLM by its architecture, the tasks researchers employed it for during optimization, its release date, evaluation metrics, and corresponding studies. The table also highlights the access type ( `F/P` , indicating free or paid) and source availability ( `O/C` , indicating open or closed). Overlapping naming conventions often create confusion, as the same term can refer to both a general architecture and specific models. Additionally, it is sometimes unclear whether researchers fine-tuned a model directly or used a version adapted for conversational purposes. When researchers did not specify the exact model in their studies, we refer to the base architecture and denote it with the keyword `Family` , as is commonly done with `GPT-4` . 

Table 5: Classification of studies by the role of 70 LLMs in combinatorial optimization tasks. The `F/P` column indicates free or paid access type, while `O/C` denotes open or closed source availability. 

|**Architecture**|**LLM**|**Date**|**Task**|**F/P**|**O/C**|**Metrics**|**Studies**|
|---|---|---|---|---|---|---|---|
|`T5`[178]|`T5-Base`|10/2019|<sup>Problem Modeling, So-</sup><br>lution Method|F|O|/|[32,74]|
||`CodeT5-fine-`<br>`tuned_CodeRL`[112]|07/2022|<sup>Problem Modeling, So-</sup><br>lution Method|F|O|Training Loss, Success<br>Rate, Correctness|[8]|
|`BART`[113]|`BART-Base`|10/2019|Problem Modeling|F|O|Accuracy|[58,<br>179]|
||`BART-Large`|10/2019|Problem Modeling|F|O|Accuracy|[58,89]|
|`UnixCoder`[68]|`UnixCoder`|03/2022|Solution Method|F|O|PAR10|[237]|
||`Text-Davinci-Edit-`<br>`001`|07/2022|Solution Method|P|C|/|[7]|
||`Text-Davinci-003`|11/2022|<sup>Problem Modeling, So-</sup><br>lution Method|P|C|Accuracy|[7, 111,<br>114]|
|`GPT-3.5`[21]|`GPT-3.5 (Family)`|11/2022|Problem Modeling, So-<br>lution Method, Bench-<br>marking, Validation|P|C|# API Call Rate, API<br>Mismatching Rate, Error<br>Raise Rate, Throughput,<br>Average<br>Travel<br>Time,<br>GAP|[3,<br>20,<br>37,248,<br>250]|
||`ChatGPT 3.5`|11/2022|Problem Modeling|F|C|Accuracy|[116]|
||`ChatGPT 3.5-Turbo`|11/2022|<sup>Problem Modeling, So-</sup><br>lution Method|P|C|/|[124,<br>127,<br>239]|
||`GPT-3.5-turbo`|11/2022|Problem Modeling, So-<br>lution Method, Valida-<br>tion|P|C|Accuracy, Hypervolume,<br>Inverted<br>Generational<br>Distance, Compile Error<br>Rate,<br>Runtime<br>Error<br>Rate|[125,<br>129,<br>238,<br>240,<br>241,<br>242,<br>243]|
||`GPT-3.5-turbo-0613`|06/2023|<sup>Problem Modeling, So-</sup><br>lution Method|P|C|F1-Score, ANC, Rank,<br>Uncertainty, Policy Met-<br>ric, Goal Metric|[4,<br>69,<br>130,<br>142]|
||`GPT-3.5-Turbo-1106`|11/2023|Solution Method|P|C|Correctness, Output For-<br>mat Consistency|[81]|



_Continued on next page_ 

46 

LLMS FOR COMBINATORIAL OPTIMIZATION 

DA ROS ET AL. 

Table 5: Classification of studies by the role of 70 LLMs in combinatorial optimization tasks. The `F/P` column indicates free or paid access type, while `O/C` denotes open or closed source availability (continued). 

|**Architecture**|**LLM**|**Date**|**Task**|**F/P**|**O/C**|**Metrics**|**Studies**|
|---|---|---|---|---|---|---|---|
||`GPT-4 (Family)`|03/2023|Problem Modeling, So-<br>lution Method, Bench-<br>marking, Validation|P|C|Accuracy,<br>Feasibility,<br>Optimality,<br>Effi-<br>ciency, ROUGE [120],<br>BERTScore<br>[251],<br>Completeness<br>Score,<br>Homogeneity<br>Score,<br>No API Call Rate, API<br>Mismatching Rate, Error<br>Raise Rate, Throughput,<br>Average<br>Travel<br>Time,<br>Code<br>Compilation<br>Success,<br>Debugging<br>Success Rate, and Code<br>Generation Efficiency|[1,<br>3,<br>20, 37,<br>39, 72,<br>87, 94,<br>95,111,<br>114,<br>216,<br>239,<br>240,<br>248,<br>250]|
||`ChatGPT 4`|03/2023|Problem Modeling, So-<br>lution Method, Bench-<br>marking|P|C|Macro-F1 Score, Time|[6,<br>99,<br>183,<br>244]|
|`GPT-4`[160]|`GPT-4-0613`|06/2023|<sup>Problem Modeling, So-</sup><br>lution Method|P|C|F1-Score,<br>Correctness,<br>Output Format Consis-<br>tency|[4,<br>40,<br>81]|
||`GPT-4-Turbo`|11/2023|Problem Modeling, So-<br>lution Method, Bench-<br>marking|P|C|Score|[28, 98,<br>127,<br>173,<br>226,<br>243,|
||||||||245]|
||`GPT-4-Vision-`<br>`Preview`|12/2023|Solution Method|P|C|/|[86]|
||`GPT-4o`|05/2024|Problem Modeling, So-<br>lution Method, Valida-<br>tion|P|C|Execution Rate, Solving<br>Accuracy, Average Solv-<br>ing Times|[2,<br>71,<br>92, 98,<br>118,<br>147,<br>188,|
||||||||222]|
||`ChatGPT-4o`|05/2024|Problem Modeling, So-<br>lution Method, Bench-<br>marking, Validation|P|C|Accuracy, Consistency,<br>Stability, Solution Con-<br>sistency, Constraints Ro-<br>bustness, Runtime Effi-<br>ciency|[52,63]|
||`GPT-4o-2024-05-13`|05/2024|Solution Method|P|C|/|[198]|
||`ChatGPT-4-Turbo`|07/2024|<sup>Problem Modeling, So-</sup><br>lution Method|P|C|/|[80]|



_Continued on next page_ 

47 

LLMS FOR COMBINATORIAL OPTIMIZATION 

DA ROS ET AL. 

Table 5: Classification of studies by the role of 70 LLMs in combinatorial optimization tasks. The `F/P` column indicates free or paid access type, while `O/C` denotes open or closed source availability (continued). 

|**Architecture**|**LLM**|**Date**|**Task**|**F/P**|**O/C**|**Metrics**|**Studies**|
|---|---|---|---|---|---|---|---|
||`GPT-4o-mini`|07/2024|Solution Method|P|C|/|[80,<br>119,<br>129,<br>226]|
||`ChatGPT-4o-mini`|07/2024|<sup>Problem Modeling, So-</sup><br>lution Method|P|C|/|[80]|
||`GPT-4o-2024-08-06`|08/2024|Solution Method|P|C|Solved Instances, Penal-<br>ized Average Runtime|[201]|
||`Bard`|05/2023|Problem Modeling|F|C|Accuracy|[116]|
||`Codey`|05/2023|Solution Method|P|C|/|[184]|
|`PaLM 2`[66]|`PaLM 2-L`|05/2023|Solution Method|P|C|Accuracy|[239]|
||`PaLM 2-L-IT`|05/2023|Solution Method|P|C|Accuracy|[239]|
||`Text-Bison`|05/2023|Solution Method|P|C|Accuracy|[239]|
||`LLaMa 2 (Family)`|07/2023|Solution Method|F|O|Accuracy|[32]|
||`LLaMa 2-7b`|07/2023|Problem Modeling, So-<br>lution Method, Bench-<br>marking, Validation|F|O|F1-Score,<br>Throughput,<br>Average Travel Time, No<br>API Call Rate, API Mis-<br>matching Rate,<br>Error<br>Raise Rate|[4,37]|
|`LLaMa 2`[62]|`LLaMa 2-13b`|07/2023|Problem Modeling, So-<br>lution Method, Bench-<br>marking, Validation|F|O|Throughput,<br>Average<br>Travel Time, No API<br>Call<br>Rate,<br>API<br>Mis-<br>matching Rate,<br>Error<br>Raise Rate|[37]|
||`LLaMa 2-13b-Chat`|07/2023|Solution Method|F|O|Correctness, Output For-<br>mat Consistency|[201]|
||`CodeLlama`[209]|08/2023|Solution Method|F|O|/|[20,<br>125,<br>250]|
||`CodeLlama-Instruct`<br>[209]|08/2023|Problem Modeling, So-<br>lution Method, Valida-<br>tion|F|O|Accuracy, Feasibility, Ef-<br>ficiency|[20,<br>152]|
||`Tulu-v2-dpo-7b`[61]|11/2023|Benchmarking|F|O|Score|[28]|
||`Mistral-7B`|09/2023|<sup>Problem Modeling, So-</sup><br>lution Method|F|O|Accuracy, Pass@K|[82]|
|`Mistral`[90]|`Zephyr-7B-beta`[215]|10/2023|Problem Modeling, So-<br>lution Method, Valida-<br>tion|F|O|/|[152]|



_Continued on next page_ 

48 

LLMS FOR COMBINATORIAL OPTIMIZATION 

DA ROS ET AL. 

Table 5: Classification of studies by the role of 70 LLMs in combinatorial optimization tasks. The `F/P` column indicates free or paid access type, while `O/C` denotes open or closed source availability (continued). 

|**Architecture**|**LLM**|**Date**|**Task**|**F/P**|**O/C**|**Metrics**|**Studies**|
|---|---|---|---|---|---|---|---|
||`Le Chat`|07/2024|Problem Modeling|P|C|/|[143]|
|175|`Qwen1.5-14B`|10/2023|<sup>Problem Modeling, So-</sup><br>lution Method|F|O|Execution Rate, Solving<br>Accuracy, Average Solv-<br>ing Times|[92]|
|`Qwen`[]|`Qwen-Turbo`|08/2024|Solution Method|F|O|/|[129]|
||`Qwen (LoRA Fine-`<br>`Tuned)`|08/2024|<sup>Problem Modeling, So-</sup><br>lution Method|P|C|/|[248]|
||`Gemini 1.0 Pro`|12/2023|Problem Modeling, So-<br>lution Method, Valida-<br>tion|P|C|Feasibility,<br>Optimality,<br>Efficiency, F1-Score|[87,<br>125]|
|`Gemini`[207]|`Gemini 1.5 Pro`|02/2024|Problem Modeling|P|C|/|[19]|
||`Gemini 1.5 Flash`|02/2024|Problem Modeling|P|C|/|[19]|
||`Gemini 2.0 Flash`|08/2024|Problem Modeling|P|C|/|[143]|
||`Gemini 2.0 Pro`|08/2024|Solution Method|P|C|/|[81]|
|`Mixtral [91]`|`Mixtral-8x7b-`<br>`instruct-v0.1`|01/2024|Benchmarking|P|C|Score|[28]|
||`Mixtral-8x22B`|07/2024|<sup>Problem Modeling, So-</sup><br>lution Method|P|C|/|[188]|
||`DeepSeek-LLM-7B-`<br>`Base`|01/2024|Solution Method|P|C|/|[125]|
||`DeepSeek-Math-7B`<br>[190]|06/2024|<sup>Problem Modeling, So-</sup><br>lution Method|P|C|Accuracy, Pass@K|[82]|
|`DeepSeek`[41]|`DeepSeek-Coder-33B`|07/2024|Solution Method|P|C|/|[30,<br>250]|
||`DeepSeek-V2`[42]|08/2024|<sup>Problem Modeling, So-</sup><br>lution Method|P|C|/|[240]|
||`DeepSeek-Coder-V2`<br>[43]|08/2024|Solution Method|P|C|/|[242]|
|`Claude 3.5`[10|] `Claude 3.5 Sonnet`|06/2024|Problem Modeling, So-<br>lution Method, Bench-<br>marking, Validation|P|C|Accuracy,<br>Solution<br>Quality, # Good Solu-<br>tions, Convergence Rate,<br>Instruction<br>Adherence,<br>Consistency,<br>Stability,<br>Prompt<br>Sensitivity,<br>Stochastic<br>Variability,<br>Constraints Robustness,<br>Runtime Efficiency|[71,<br>182,<br>222]|



_Continued on next page_ 

49 

LLMS FOR COMBINATORIAL OPTIMIZATION 

DA ROS ET AL. 

Table 5: Classification of studies by the role of 70 LLMs in combinatorial optimization tasks. The `F/P` column indicates free or paid access type, while `O/C` denotes open or closed source availability (continued). 

|**Architecture**|**LLM**|**Date**|**Task**|**F/P**|**O/C**|**Metrics**|**Studies**|
|---|---|---|---|---|---|---|---|
||`Claude 3.5 Opus`|06/2024|<sup>Problem Modeling, So-</sup><br>lution Method|P|C|/|[188,<br>250]|
||`Claude 3.5 Haiku`|06/2024|Solution Method|P|C|/|[129,<br>129]|
||`Claude-3.5-Sonnet-`<br>`20241022`|10/2024|Solution Method|P|C|/|[93]|
|`Cohere`[5]|`Command-R+`|06/2024|<sup>Problem Modeling, So-</sup><br>lution Method|P|C|/|[188]|
||`LLaMa 3-70B`|07/2024|<sup>Problem Modeling, So-</sup><br>lution Method|F|O|/|[2,<br>96,<br>240,<br>243]|
|`LLaMa 3`[132]|`LLaMa 3-8B`|08/2024|<sup>Problem Modeling, So-</sup><br>lution Method|F|O|Accuracy, Compilation<br>Error Rate, Runtime Er-<br>ror Rate|[82]|
||`LLaMa 3-70B-`<br>`Instruct`|08/2024|Solution Method|F|O|Accuracy, Pass@K|[242]|
||`LLaMa 3.1-8B`|08/2024|Solution Method|F|O|/|[129]|
|`Qwen2`[176]|`Qwen2.5-7B`|07/2024|<sup>Problem Modeling, So-</sup><br>lution Method|F|O|Accuracy, Pass@K|[82]|
|`StarCoder`<br>[117]|`StarCoder2`[136]|07/2024|Solution Method|P|C|/|[250]|
|`GLM`[51]|`GLM-3-Turbo`|07/2024|Solution Method|P|C|/|[129,<br>242]|
|`OpenCoder`<br>[83]|`OpenCoder-8B-`<br>`Instruct`|07/2024|Solution Method|P|C|/|[30]|
|`Yi`[210]|`Yi-34B-Chat`|07/2024|Solution Method|P|C|/|[129]|
|`Gemma`[208]|`Gemma 2 27B`|07/2024|Problem Modeling|P|O|/|[19]|
|`InternLM2`<br>[24]|`InternLM2-20B-Chat`|08/2024|Solution Method|P|C|Correctness, Output For-<br>mat Consistency|[81]|



50 

LLMS FOR COMBINATORIAL OPTIMIZATION 

DA ROS ET AL. 

# **E Classification of Studies by Benchmark Dataset** 

This appendix provides the tabular analysis related to the classification of studies by dataset (Table 6). Please refer to Section 6.3 for further context. 

Table 6: Classification of studies by benchmark dataset. 

|**Name**|**Source**|**Studies**|**#**|
|---|---|---|---|
|LPWP or NL4Opt|Ramamonjison et al. [179]|[1,3,4,47,58,74,82,89,92,116,146,156,179,224,<br>238,248]|16|
|ComplexOR|Xiao et al. [238]|[3,92,238]|3|
|NLP4LP|AhmadiTeshnizi et al.[2,3]|[2,3,92]|3|
|IndustryOR|Huang et al. [82]|[82,92]|2|
|Mamo|Huang et al. [85]|[82,92]|2|
|GraphInstruct|Luo et al. [137]|[80,119]|2|
|AI-copilot-data|Amarasinghe et al. [8]|[8]|1|
|Almonacid|Almonacid [7]|[7]|1|
|Safeguard, Code Genera-<br>tion|Lawless et al. [111]|[111]|1|
|Huang et al.|Huang et al. [87]|[87]|1|
|OptiChat|Hao Chen and Li [72]|[72]|1|
|Michailidis et al.|Michailidis et al. [146]|[146]|1|
|Optibench, ReScratic-29k|Yang et al. [240]|[240]|1|
|Mostajabdaveh et al.|Mostajabdaveh et al. [152]|[152]|1|
|Zhang et al.|Zhang et al. [248]|[248]|1|
|SearchBench|Borazjanizadeh et al. [20]|[20]|1|
|Ju et al.|Ju et al. [96]|[96]|1|
|Talk Like A Graph|Fatemi et al. [54]|[119]|1|
|LLM4DyG|Zhang et al. [252]|[119]|1|
|GraphViz|Chen et al. [29]|[119]|1|
|NLGraph|Wang et al. [223]|[119]|1|
|GNN-AutoGL|Li et al. [119]|[119]|1|
|ORQUA|Mostajabdaveh et al. [151]|[151]|1|



51 

LLMS FOR COMBINATORIAL OPTIMIZATION 

DA ROS ET AL. 

# **F Classification of Studies by Application Domain** 

This appendix provides the tabular analysis related to the classification of studies by application domain (Table 7). Please refer to Section 6.4 for further context. 

Table 7: Classification of studies by application domain. 

|**Domain**|**COP/Detail**|**Studies**|**#**|
|---|---|---|---|
||Traveling Salesperson|[30,52,81,98,124,125,127,129,<br>131, 143, 198, 200, 239, 241, 243,||
|Routing||250]|26|
||Vehicle Routing|[32,37,63,86,87,98,99,129,235,<br>243]||
||Orienteering|[243]||
||Travel|[39,96,115]||
||Permutation Flowshop Scheduling|[8,125]||
|Schedulin and Plannin|Meeting and Conferece Scheduling|[95,111]|14|
|g  g|Server Scheduling|[242]||
||Planning|[19,45,71,93,147,157,166,226,<br>244]||
||Network Design|[80,119,134,216,245]||
||Critical Node Identification|[142]||
|Network and Grahs|Coloring|[143]|10|
|p|Social Network|[188]||
||Shortest Path, Assignement|[98]||
||Path Finding|[20]||
|Packing|Bin Packing|[30, 125, 129, 184, 198, 241, 243,<br>250]|8|
||Multiple Knapsack|[243]||
||Cap Set|[184]||
|Cbiti|Admissible Set|[250]|4|
|omnaorcs|Puzzles|[20,146]||
||Subset Sum, Sorting, Under-determined Sys-<br>tems|[20]||
||Construction|[187]||
|Engineering|Circuit Design|[243]|3|
||Energy Management|[94]||
|Finance|Portfolio Optimization|[6,40,183]|3|
|Bioinformatics|Enzyme Design|[153,182,213]|3|
|Supply Chain|Warehousing|[114]|1|
|Strings|Text Generation|[181]|1|



52 

