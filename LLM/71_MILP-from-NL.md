# Synthesizing mixed-integer linear programming models from natural language descriptions 

Qingyang Li<sup>a,b</sup> , Lele Zhang<sup>a,b</sup> , Vicky Mak-Hau<sup>c</sup> 

> _aThe University of Melbourne, Melbourne, 3010, Victoria, Australia_ 

> _bARC Training Centre in Optimisation Technologies, Integrated Methodologies, and Applications (OPTIMA), Australia_ 

> _cDeakin University, Burwood, 3125, Victoria, Australia_ 

## **Abstract** 

Numerous real-life problems arising in various domains such as production planning, resource allocation, scheduling, and transportation planning and management, can be effectively formulated and solved using Mixed-Integer Linear Programming (MILP) models. However, the transformation of realworld decision-making problems into MILP models heavily relies on expertise in operations research and mathematical optimization, which restricts non-experts’ accessibility to MILP. To address this challenge, we propose a framework for automatically formulating MILP models from unstructured natural language descriptions of decision problems, which integrates Large Language Models (LLMs) and mathematical modeling techniques. This framework consists of three phases: i) identification of decision variables, ii) classification of objective and constraints, and iii) finally, generation of MILP models. 

In this study, we propose a knowledge representation structure that includes relational knowledge, inheritable knowledge, and so on. Specifically, we present a constraint classification scheme and a set of constraint templates that can guide the LLMs in synthesizing a complete MILP model from a given natural language description of a decision-making problem. After _fine-tuning_ LLMs based on numerous examples of constraint and objective descriptions, our approach can, from the natural language description, identify and synthesize logic constraints in addition to classic demand and resource constraints. The logic constraints have not been studied in existing work. 

To evaluate the performance of the proposed framework, we extend the NL4Opt dataset with more problem descriptions and constraint types, in particular logic constraints and binary variables, and with the newly created dataset, we compare our method with one-step model generation methods offered by LLMs like ChatGPT and Google Bard. The experimental results reveal that with respect to the accuracies of generating the correct model, objective, and constraints, our method which integrates knowledge representation with LLMs significantly outperforms the others. Taking ChatGPT for example, our framework accurately formulates 86.67% problems and 99.32% constraints compared to ChatGPT’s 26.67% and 82.99% respectively. The three-phase framework that we developed is a prototype system for synthesizing MILP models from natural language descriptions and has a great potential to capture more constraints for more complex MILPs. Our framework opens up opportunities for developing training tools for operations research practitioners and has the potential to be a powerful tool for automatic decision problem modeling and solving in practice. 

_Keywords:_ 

Mixed-integer linear programming, Large language model, Automatic formulation, 

_Email addresses:_ `ql5@student.unimelb.edu.au` (Qingyang Li), `lele.zhang@unimelb.edu.au` (Lele Zhang), `vicky.mak@deakin.edu.au` (Vicky Mak-Hau) 

_Preprint submitted to Elsevier_ 

_November 28, 2023_ 

## **1. Introduction** 

In the last few decades, mathematicians and computer scientists have collectively improved the way business decisions are made, through understanding the requirements of the end-users and creating computerized systems to optimize their decisions. Many real-life decision-making problems are combinatorial optimization problems that can typically be formulated as Integer Programming (IP)-family of problems (such as Pure Binary Integer Programming (BIP), Mixed-Integer Linear Programming (MILP) problems). CO problems are about making the best decisions given a large number of (and sometimes exponentially many) options. For example, to make decisions on “yes/no” questions such as whether to build a facility at a location, to allocate a machine to a job, or if a customer is to be visited immediately before another customer on a trip. Or, to make decisions on a quantity, for example, how many tables to make, how many acres of land to be used to grow apples, or how much money to invest in a stock. These decisions are often made with the objective to maximize profit or minimize cost, subject to business requirements or needs, such as limitations due to resource availability, quantities to be balanced, demands to be supplied, quality to be conformed to, or business logic to be observed. 

Optimizing business decisions through formulating mathematical programming models and developing solution methodologies to solve them has brought huge social and economic benefits. For instance, Ford Motor developed an Integer Programming (IP) model to shorten the planning process, which optimized global procedures and saved USD 250M (Chen et al., 2009). Baosteel applied IP for production planning, and just their main Shanghai plant alone, reduced annual carbon monoxide emissions by over 500,000 tons (INFORMS, 2013). As of 2020, (M)ILP was the technique used in one out of five Franz Edelman Award Finalists (Gorman et al., 2020). In fact, businesses of all sizes can benefit from optimized decision making. 

In the last six decades or so, the focus of research amongst the Operation Research community has been on the theories, solution methodologies, and applications of IP-family of problems, see, e.g., (J¨unger et al., 2010). Countless MILPs have been formulated for different combinatorial optimization problems in the past, and no doubt many more to come. An MILP comprises decision variables (binary, integer, and/or continuous), an objective function (a linear combination of parameters and decision variables), and constraints of different classes. Even though an MILP can have exponentially many constraints, the number of types of MILP constraints is limited. With recent advances in Natural Language Processing (NLP), in particular Large Language Models (LLMs), the idea of automating the formulation of MILPs has inspired much new research. 

Our research is motivated by the desire to find out how LLMs can be utilized to “translate” a natural language description of a combinatorial optimization problem into a mathematical model, in particular, through constraint recognition and model synthesis. 

## _1.1. Literature review_ 

Surprisingly, research on the automatic synthesis of mathematical programming models from natural language descriptions has only become active in recent years. There has been a lot of research thus far on methods that synthesise mathematical programming models from data (observations). They made use of different techniques that allow the synthesis of different types of Mathematical Programming (MP) models, such as utilizing MILP formulation for the linear and nonlinear constraint synthesis problems (Pawlak and Krawiec, 2017), local search for MILP model synthesis (Sroka and Pawlak, 2018), inductive logic programming for integer nonlinear programming (Kumar et al., 2019), Grammatical Evolution for MILP constraint synthesis (Pawlak and O’Neill, 2021). These data-driven constraint learning methods do not focus on the context of the problem represented by the model, and hence, they are more applicable to the constraints that are difficult to formulate directly. However, one concern is that the interpretability of constraints learned from the data may be poor and not easily understood by humans (Fajemisin et al., 2023). Another limitation of these approaches is the availability of data, i.e., whether a sufficient number of solution examples can be collected for good 

2 

performance. Notice that the only guarantee of a correct MILP being “learned” from data is when all “positive samples” (feasible solutions) are present in the system. However, in most real-life combinatorial optimization problems, even finding one feasible solution is hard. If all feasible solutions are known, then one can just evaluate the objective function value for all the solutions to find the optimal solution. 

Research on automatically solving natural language mathematical word problems has been conducted since the 1960s. An intelligent system capable of solving mathematical word problems should be able to process the natural language description of the problem, allow different users to describe the problem in different ways, and minimize control over the user’s input (Mukherjee and Garain, 2008). Many approaches have been proposed for transforming natural language descriptions of mathematical word problems into sets of equations, which are mostly based on semantic parsing, text similarity, predefined templates for sets of equations, or deep learning (Zhang et al., 2019). 

The rise of LLMs opens up more possibilities for equation synthesis of mathematical word problems. LLMs can perform new tasks with only instruction and no training examples (zero-shot learning), or with a few training examples (few-shot learning) (Kojima et al., 2023). Zong and Krishnamachari (2023) evaluated the performance of Generative Pre-trained Transformer 3 (GPT-3, Brown et al., 2020) in three types of tests: classifying mathematical word problems that can be expressed as two linear equations; extracting equations from word problems; and generating word problems. The accuracy of extracting equations increases with the number of examples provided in the prompt, and the accuracy of the fine-tuned GPT-3 is higher than that of the few-shot learning and zero-shot learning. GPT-3 with zero-shot learning performs well on classifying word problems for most classes, and their experiment results provide some evidence that supplying examples of the same class in the prompt for few-shot learning for extracting equations can be helpful. However, in contrast to our approach, they do not incorporate classification as a prior step to equation extraction in their framework. Notice that problem classification is not always helpful in equation extraction. Compared to our approach, these authors fine-tuned GPT-3 used for equation extraction rather than for the classification task with a limited number of valid responses. 

In contrast to their study, we classify constraints rather than problems since constraint classification is more helpful for extracting MILP models. In integer programming for combinatorial optimization (CO) problems, sometimes different problems can share the same constraints. For example, many of the scheduling problems have similar requirements to routing problems. Sometimes, a CO problem can have characteristics of two or more well-known problem classes. With different combinations of constraints, there are infinitely many possibilities of CO problems that can be formulated as MILPs, hence classifying problems may not be a practical solution. On the other hand, the number of constraint types is limited, and therefore classifying the type of a constraint is much easier. 

Recent technological advancements within the field of natural language processing have opened up more possibilities on the topic of automatic synthesis of mathematical programming models from natural language descriptions. Extracting mathematical models from text descriptions can be regarded as a semantic parsing task, i.e., extracting machine-interpretable meaning representations from a natural language text (Ramamonjison et al., 2023). Ofoghi and Yearwood (2023) presented an “ontology” for MILP, however some elements are unclear. For example, coefficients were said to be parametric, but there is no mention that the decision variables are parametric as well. The paper also states that “order is of importance for indices that represent parametric coefficients, so the correct sequence is preserved”. As MILP practitioners, our understanding is that the order of appearance of the set of decision variables and their associated coefficients is usually arbitrary. Further, if the purpose of the proposed ontology is for automatic model generation, then without seeing the framework, it is hard to ascertain if the ontology is useful. If the purpose is only to demonstrate a possible machine representation of MILPs, then this work may not be new, as there are so many open source and commercial MILP solvers, each of them may have developed an ontology at some point. 

One of the earliest works in this area is by Islam et al. (2021), incorporating both the fields of natural 

3 

language processing and linear programming. Given a structured problem description, their method first classifies the objective as maximizing or minimizing using Support Vector Machine (SVM). It then tokenizes sentences using the Python NLTK package and extracts the numbers using NLTK POS-tagger. However, there are obvious limitations to their method, namely the structured problem description and the requirement that all sentences included must be simple. Information about model components (e.g., number of variables, number of constraints) and parameter values (e.g., coefficients of variables) must appear in the textual description in a specified order. Moreover, the method can only handle constraints that represent upper bounds. 

With the popularity of LLMs growing, a number of recently developed automated modeling frameworks have utilized LLMs in the methodology architecture for converting natural language descriptions into mathematical models. To formulate and solve the MILP problem from a structured natural language description, AhmadiTeshnizi et al. (2023) developed an LLM-based agent called OptiMUS. The method uses LLM to build the mathematical formulation in one step by using a prompt containing user input that contains additional “hints” far beyond the natural language description of the problem. OptiMUS is also able to exploit the LLM to transform the mathematical model into solver code, debug it, and check the validity of the solution. The study shows the potential to automate multiple stages of solving optimization problems by integrating LLMs and solvers. However, it requires users to use as input a representation called SNOP (Structured Natural Language Optimization Problem) that explicitly specifies the decision variables, the objective function, and all the parameters used to compose the objective and constraints. Whilst this greatly reduces the challenge of automatic modeling, writing an accurate input is difficult for users without mathematical programming-related expertise. Typically, a domain expert does not describe his/her decision problem in such an ideally structured language style. The fact is that different people are likely to describe the same problem in different ways. In contrast to their work, our paper is concerned with automatic formulation from unstructured text descriptions of MILP problems. 

In 2022, the NL4Opt competition (Ramamonjison et al., 2023) for extracting linear programming formulations from natural language has attracted wider attention to this research topic and has led to significant progress in this field. Ramamonjison et al. (2022) proposed an automatic formulation method, OptGen, that is capable of handling unstructured LP problem descriptions with different types of constraints, and developed and tested it on a dataset containing 1101 problem instances. In the first stage (entity identification), the fine-tuned transformer acts as an entity tagger that tags the keywords denoting variables, objective function, and constraints from the problem description. In the second stage, a set of intermediate representation declarations of the objective and constraints are generated from the recognized entities, creating a bridge from contextual descriptions to contextindependent mathematical formulations. An intermediate representation declaration is a sequence of tokens derived from the problem description to preserve the contextual information of the problem, indicating the objective or constraint (and its type) in a structured way. This transformation is based on predefined templates for different types of objectives and constraints. Finally, the transformation of intermediate representation declarations to mathematical expressions is performed by a parser. The authors created a modeling platform that allows user interaction using the OptGen architecture described above as the underlying framework. In addition, they developed the first dataset of linear programming word problems (NL4Opt) that comprises instances in a number of application domains. Since then, a number of research groups utilize ensemble learning to improve the first-stage outcomes (He et al., 2022, Doan, 2022, Wang, Chen and Zheng, 2023, Ning et al., 2023). Data pre-processing and augmentation are used to improve the second-stage outcomes (Gangwar and Kani, 2023, Jang, 2022, Ning et al., 2023). Prasath and Karande (2023) used GPT-3 to generate new instances by making parameter changes and context changes to the original problems in order to increase the size of the training dataset. The authors reported that in most cases, the new problem descriptions generated were not semantically correct. Despite this, the models were trained on the augmented data but evaluated using only the original NL4Opt dataset, and it reportedly led to improved performance. 

These studies are the first steps toward the goal of automatic linear programming modeling from natural language descriptions. The average number of decision variables in the NL4Opt instances 

4 

is 2.08 and the average number of constraints is 2.83. The constraints are confined to a number of basic constraint types, and neither logic constraints nor binary variables are accounted for. Whilst the problem descriptions covered a wide range of domains, the difficulty of the mathematical models is limited to simple linear programming (even though the decision variables in most problem instances should in fact be integers). These are typically simple LP problems taught in the first week of a tertiary optimization subject, or even in some secondary school mathematics textbooks. 

To transform any combination of Boolean logic operations (such as `AND` , `OR` and `Implication` ) into MILP constraints, Wang, Gupta and Wang (2023) developed a syntax-guided synthesis method based on Domain Specification Language (DSL). The input specification is a logical condition consisting of propositions representing linear expressions connected by Boolean logic operators, e.g., ( _X_ 8 = 0 _→ X_ 11 = 0) _∧_ ( _X_ 8 = 0 _→ X_ 17 = 0), which means `if` _X_ 8 = 0 `, then` _X_ 11 `and` _X_ 17 `must be` 0. This type of specification can be seen as an intermediate representation between natural language descriptions to mathematical expressions. 

Advances in LLMs make it possible to develop a new workflow for automated modeling. Inspired by the NL4Opt competition, Tsouros et al. (2023) developed a framework called Holy Grail 2.0, consisting of similar steps, i.e., extracting the semantic entities of the optimization problem (as proposed in (Dakle et al., 2023)), identifying the relationships between the entities, formulating the problem, and generating runnable code, but the framework heavily utilizes LLMs in all steps involved. To assess the ability of the method to formulate problems, they presented four levels of abstraction for natural language problem descriptions, (from all model components being stated explicitly to the closest way that someone not familiar with optimization modeling would describe a problem.) For developing a diverse instance set of MILP word problems in the future, the abstraction level of a problem description can be considered as a characteristic of the instance, providing guidance for creating new instances that are more challenging in terms of translating natural language descriptions into mathematical models. 

Li et al. (2023) developed another LLM-based framework called OptiGuide for several application scenarios in supply chain optimization, with textual queries as input and interpretations of optimization solutions as output. In this system, LLMs are used to transform the user’s questions described in natural language (e.g., can we use caf´e S1 for roastery D1?) into new constraints added to the MIP model (e.g., `m.addConstr(x["S1", "D1"]==1)` ) or updates to the parameters in the MIP model in code form. In this approach, a prompt consists of simple instructions and examples, i.e., pairs of questions and code answers, in addition to the question asked by the user. The approach requires developing, for each scenario, a repository of question-code pairs, some of which form a set for the selection of examples in the prompt, and the others serve as a test set. The performance of few-shot learning is highly affected by the appropriateness of the example selection in the prompt. In contrast, our approach uses classification plus fine-tuning to avoid the shortcomings of few-shot learning and to shorten the length of the input to LLMs by avoiding providing a large number of examples in the prompt. 

In all studies discussed above, LLMs are employed as translators in the transformation from natural language to mathematical models. However, the OPRO (optimization by prompting) method developed by Yang et al. (2023) uses LLMs as optimizers to improve optimization solutions. They describe optimization problems in natural language but do not formally formulate them. Instead of using solvers to obtain solutions, the method guides the LLM to iteratively generate new solutions by providing previously generated solutions and their evaluations as examples in the prompt, since LLMs are capable of identifying patterns from examples. This method is only suitable for small-scale optimization problems. 

In contrast to the aim of transforming a given problem description into a mathematical model, some research focuses on the generation of models that satisfy the specifications required by users. It provides us with another approach for building instance sets of MILP word problems, namely, generating problem descriptions from diverse models. Almonacid (2023) tentatively demonstrated the ability of 

5 

GPT-3.5 to generate optimization models (represented in the Minizinc modeling language) that satisfy the required features of the model as specified by the user via prompts, such as whether the domains of the variables are open or bounded, and whether constraints are imposed. 

## _1.2. Contributions and outline of the paper_ 

The main contributions of this paper include: 

- proposing a framework to automatically build MILP models from unstructured natural language descriptions of optimization problems, which integrates LLMs and mathematical modeling techniques. This framework consists of three stages as shown in Figure 1: i) identification of decision variables, ii) classification of the objective and constraints, and iii) constraint generation and supplementation. In contrast to previous work, this approach is able to handle binary variables and logic constraints. It has a great potential to capture more constraints for more complex MILPs. This framework has been shown to outperform LLMs when they are asked to directly generate the MILP models, with the former generating correct models in 50% to 60% more problem instances. Our framework provides opportunities for the development of training tools for operations research practitioners. It also has the potential to become a powerful tool for automatic decision problem modeling and solving in practice, making optimal decision making more accessible to non-experts. 

- developing an instance set of MILP word problems, comprising 30 problem descriptions and their MILP models. In contrast to the first LP word problem instance set, NL4Opt, our instance set involves binary variables and includes four types of logic constraints. 

- proposing a constraint recognition method by fine-tuning LLMs as constraint classifiers. We extend the constraint descriptions in the NL4Opt dataset (the dev set) by adding descriptions for logic constraints, annotating their classes, and fine-tuning LLMs on this modified dataset. 

- creating templates for constraints to guide LLMs in generating the mathematical formulation of the MILPs. 

The rest of the paper is organized as follows. Section 2 describes the types of constraints we currently consider and compares them with the constraint classification of the NL4Opt competition. Section 3 illustrates the methodology of the framework for automatically converting natural language descriptions into mathematical models. Section 4 presents the numerical experiment, including dataset creation and results comparing the performance of two variants of our framework and two chatbots in automatically synthesizing models. Finally, Section 5 summarizes the paper and proposes some future work. 

## **2. Constraint Classification** 

Even though the types of constraints are limited, it is non-trivial to consider all constraint types for automatic modeling. This work, as a proof-of-concept, focuses on the categories of constraints: _basic constraints_ included in the NL4Opt dataset and some _logic constraints_ . 

The NL4Opt competition classified the constraints in their problem instances into 7 types, e.g., upper bound, ratio control and sum constraints, and here we refine them into 9 types. See Table 1. We deconstructed the 99 problem descriptions from the NL4Opt (development) dataset, and obtained 292 descriptions of constraints. These constraints can be covered by the types 1 to 9 in Table 1. 

However, the problems in the NL4Opt dataset only involve continuous or integer variables and the nine types of constraints, and no binary variables or logic constraints are included. In this study, we consider 4 types of logic constraints, each involving two binary variables. To extend the NL4Opt dataset, we 

6 

- **Type Constraint type defined in this work Mathematical Constraint type defined Type No. inequality in NL4Opt competition No.** 1 Upper bound on single variable _xi ≤ b_ Upper bound 2 2 Upper bound on sum of variables � _i_<sup>_xi≤b_</sup> Sum constraint 1 3 Upper bound on weighted sum of variables � _i_<sup>_aixi≤b_</sup> Linear constraint 4 4 Upper bound on proportion _xj ≤ c_<sup>�</sup> _i_<sup>_xi_</sup> Ratio control constraint 5 5 Lower bound on single variable _xi ≥ b_ Lower bound 3 6 Lower bound on sum of variables � _i_<sup>_xi≥b_</sup> Sum constraint 1 7 Lower bound on weighted sum of variables � _i_<sup>_aixi≥b_</sup> Linear constraint 4 8 Lower bound on proportion _xj ≥ c_<sup>�</sup> _i_<sup>_xi_</sup> Ratio control constraint 5 9 Comparison constraints _dxi ≤ xj_ Balance constraint Type-1 (if 6/7 _d̸_ = 1) or Type-2 (if _d_ = 1) 

- 10 If A then B/ if not B then not A/ B if A _yA ≤ yB_ 11 Exactly one of A and B/ either A or B but _yA_ + _yB_ = 1 not both (or neither) 

- 12 At least one of A and B/ if not A then B/ _yA_ + _yB ≥_ 1 either A or B or both 

- 13 At most one of A and B/ if A then not B/ _yA_ + _yB ≤_ 1 either A or B or neither <u>(but</u> not both) 

Table 1: Constraint types defined in this work and those in the NL4Opt competition. _xi_ and _xj_ , _i, j ∈{_ 1 _,_ 2 _, . . . , n}_ , denote decision variables, _ai_ , _b_ and _d_ are non-negative constants, and _c_ is a constant _∈_ (0 _,_ 1]. We use a binary decision variable _y ∈{_ 0 _,_ 1 _}_ to represent the true/false value of a statement (e.g., if an event will take place), with, e.g., _yA_ = 1 indicating Statement A is true (Event A does take place), and _yA_ = 0 otherwise. 

create descriptions of logic constraints belonging to the types 10 to 13 in Table 1 and problem instances involving these types of constraints. Due to limited existing datasets for MILP modeling, this study relies on the NL4Opt dataset, which does not contain equality constraints. Therefore this study does not consider equality constraints except for the logic constraint type 11 that we have added. 

In what follows, we simplify our notation and use _ax_ to represent **_a_** _·_ **_x_** , where **_a_** and **_x_** are vectors of coefficients and decision variables respectively. We also use<sup>�</sup> _j_<sup>torepresent�</sup> _∀j_<sup>.</sup> 

## _2.1. Constraints for resource, demand, proportions and comparison_ 

Constraints that capture resource restrictions (static upper limit) and minimum demand requirements (static lower limit) are commonly used in MILP. They are expressed in the form of _ax ≤ b_ (e.g., types 1-3 in Table 1) and _ax ≥ b_ (e.g., types 5-7) respectively. If the requirement is to equate amounts, we should use _ax_ = _b_ . However, this equality constraint type is not addressed in the NL4Opt dataset, and hence, this study focuses on the inequality constraints. 

In some cases, upper or lower bounds on proportions are required, e.g., types 4 and 8 in Table 1. For example, the proportion of product _j_ must not be more than _c_ of the total (mathematically, _xj ≤ c_<sup>�</sup> _j_<sup>_xj_with0</sup><sup>_<c≤_1).Or,thesumofaproductset</sup><sup>_N_1mustbeatleast</sup><sup>_c_ofthesumof</sup> another set _N_ 2 (<sup>�</sup> _j∈N_ 1<sup>_xj≥c_�</sup> _j∈N_ 2<sup>_xj_).</sup> 

A comparison between two quantities can be given as _dxi ≤ xj_ for _d ∈_ R+. If _d >_ 1, it implies that the amount of _j_ must be at least _d_ times the amount of _i_ (e.g., _d_ = 3 _,_ 3 _xi ≤ xj_ ), or that the amount of _i_ cannot exceed 1 _/d_ of the amount of _j_ (e.g., _d_ = 3 _, xi ≤_ (1 _/_ 3) _xj_ ). If _d <_ 1, it implies that the amount of _j_ must be at least _d_ of the amount of _i_ (e.g., _d_ = 1 _/_ 3 _,_ (1 _/_ 3) _xi ≤ xj_ ), or that the amount of _i_ cannot exceed 1 _/d_ times the amount of _j_ (e.g., _d_ = 1 _/_ 3 _, xi ≤_ 3 _xj_ ). In the NL4Opt competition dataset, the constraint descriptions of type 9 involve only the first and third expression styles. Therefore, we do not need to specifically define another type of comparison constraints represented by _xi ≤ dxj_ . Nevertheless, in terms of using LLMs to formulate comparison constraints, there is no impact since LLMs have the flexibility to use the data mentioned in the constraint descriptions as the coefficients of variables. 

7 

## _2.2. Set packing/partitioning/covering constraints_ 

Set packing/partitioning/covering constraints are sub-types of resource/conservation/demand constraints respectively. These constraints require at most/exactly/at least one of _n_ options to be selected. Constraints of type 11/12/13 in Table 1) are special cases of set partitioning/covering/packing constraints. These options are represented by a set of _n_ binary variables **_y_** _∈{_ 0 _,_ 1 _}_<sup>_n_</sup> . Then set packing/partitioning/covering constraints are denoted as **_a_** _·_ **_y_** _{≤,_ = _, ≥}_ 1 respectively for **_a_** _∈{_ 0 _,_ 1 _}_<sup>_n_</sup> . If the right-hand side (RHS) of the constraint is an integer constant _b >_ 1, it is the weighted set packing/partitioning/covering constraint. Set packing and set covering constraints as well as weighted versions of them are also included in type 2 (<sup>�</sup> _i_<sup>_xi≤b_)andtype6(�</sup> _i_<sup>_xi≥b_)inTable1ifthe</sup> variables _xi_ ’s are all binary. 

## _2.3. Logic constraints_ 

In real-life applications, sometimes just capturing quantities (using continuous or general integer variables) is not enough, we need to capture logic requirements as well. Binary variables are commonly used to convert logical relations in a combinatorial optimization problem into linear constraints, known as logic constraints. Consider an example from the dataset we created; `if Haus Toys makes trucks, then they will not make trains` , can be represented as the nonlinear constraint `trucks` _∗_ `trains` = 0, where the integer variables `trucks` _,_ `trains` _∈_ Z _≥_ 0 refer to the number of trucks and trains they plan to produce, respectively. To capture the same business requirement as a linear programming model, one can introduce binary variables `bi` ~~`t`~~ `rucks` _,_ `bi` ~~`t`~~ `rains` _∈{_ 0 _,_ 1 _}_ indicating whether Haus Toys makes trucks and trains respectively. The binary variable takes the value of 1 if they make trucks/trains, and 0 otherwise. Then the logic constraint can be represented as the linear inequality `bi` ~~`t`~~ `rucks` + `bi trains` _≤_ 1. 

In general, one can use a binary variable _yA ∈{_ 0 _,_ 1 _}_ to capture if _xA_ = 0 or _xA >_ 0 for a continuous or integer variable _xA_ . To establish the link between the binary variable and its corresponding continuous or integer variable, we impose two _linking constraints_ as follows. 





Inequality (1), for a sufficiently large value _M_ , enforces _yA_ = 1 if _xA >_ 0. Inequality (2) ensures _yA_ = 0 if _xA_ = 0 (here, _M_ is needed only if _xA_ may take values less than 1). 

Consider two statements, A and B, with truth values represented by binary variables _yA, yB ∈{_ 0 _,_ 1 _}_ respectively; for example, _yA_ = 1 means statement A is true and 0 otherwise. This study considers the following logic conditions. 

- The _If-then_ condition: “If A then B” (type 10), equivalent to “If not B then not A”, is given by _yA ≤ yB_ . Since “not A” can be represented by 1 _− yA_ , “If not A then B” (type 12), equivalent to “At least one of A and B”, is satisfied by 1 _− yA ≤ yB_ . “If A then not B” (type 13), equivalent to “At most one of A and B”, is satisfied by 1 _− yB ≥ yA_ . 

- The _Exclusive or_ condition (type 11): “Either A or B (but not both)” is given by _yA_ + _yB_ = 1, which is equivalent to “Exactly one of A and B”. 

- The _Inclusive or_ condition (type 12): “Either A or B or both” is given by _yA_ + _yB ≥_ 1, which is equivalent to “At least one of A and B”. 

## **3. Methodology** 

The automatic modeling approach proposed in this paper consists of three stages and two preparation modules. The three stages are 1) variable identification, 2) constraint classification, and 3) constraint 

8 

generation and supplementation. See Figure 1. We assume that a full problem description is provided as input by the user and it is presented in the form of paragraphs, each representing an objective or a constraint. See an example in Figure 2. Given the problem description, the approach first determines all decision variables, then for each paragraph, classifies the objective function or constraint and generates a mathematical formula using the corresponding template, and finally for logic constraint(s) if any, supplements linking constraints, to the final model as the output. The first preparation module fine-tunes an LLM to be the classifier of Stage 2, and the second preparation module, empowered by the knowledge representation, creates a set of constraint templates for generating mathematical constraints in Stage 3. Both modules are completed before executing the automatic modeling procedure. The main flow of the proposed approach is depicted in Figure 1, whereas an example of the problem description input, the modeling process, and the model output is shown in Figure 2. 

## _3.1. Stage 1: Variable identification_ 

The first stage of the modeling approach is to determine the decision variables and is composed of two steps. The first step is to identify all continuous and/or integer variables from the full problem description by an LLM. If the problem does not involve any types of these variables, the LLM is asked to recognize all binary variables. In that case, the problem is considered to involve only binary variables and will be formulated as a pure binary linear programming model. The answer of the LLM should consist only of the variable names. We instruct the LLM that a continuous or integer variable needs to be called with the name of the quantity that it represents. For example, the integer variable representing `the quantity of vanilla cakes to be made by a bakery` is named `vanilla` ~~`c`~~ `akes` . The name of a binary variable must start with `bi` and be linked to the name of the entity it represents, for example, `bi` ~~`v`~~ `anilla` ~~`c`~~ `akes` . The benefit of this naming convention is that it facilitates comparison of the model formulated with the true model, eliminating the effects of the order in which the variables appear. 

The second step of Stage 1 is to generate a corresponding binary indicator variable for each of the continuous or integer variables; if its value is greater than 0 then the binary variable is 1, otherwise 0. This step is the basis for constructing the logic constraints later in the automatic modeling approach. It is important to note that the binary variables generated in this step are associated with the corresponding continuous or integer variables, and so in Stage 3, for those of them that are used in the formulation, we need to add linking constraints to the model in order to associate each of them with the corresponding continuous or integer variable. Note that all variables in the dataset used in this paper are non-negative. 

9 



Figure 1: Main steps of the automatic modeling approach with GPT 

10 



11 

## _3.2. Stage 2: Constraint classification_ 

For each paragraph of the given problem description, which is an objective function description or a constraint description, the second stage classifies the constraint type from the type set in Table 1 for each description using a fine-tuned LLM. 

LLMs are pre-trained on large amounts of data, which allows them to respond to a given prompt containing only a few examples or no examples. However, for the constraint classification in this framework, we allow LLMs to rely on more than just prompts and to learn more examples. Thus, we fine-tune LLMs as the classifier of Stage 2 to recognize constraints, so that there is no need to provide examples in the prompts. Fine-tuning trains an already trained model by using a specific dataset to adapt it to a customized application scenario. It can improve the accuracy and response speed of LLMs to specific tasks. More details about the dataset and hyperparameters used for fine-tuning can be found in Section 4. Once the dataset and hyperparameters are set up, the LLM fine-tuning, such as for GPT models and PaLM, can often be done automatically. 

For the classification by LLMs, if the name of each class (i.e., type) contains more than one token, OpenAI suggests that it may affect the output quality of the trained model. Therefore, in the dataset for fine-tuning, we use the type numbers rather than type names in Table 1 to annotate the objective function and the 13 constraint types in each prompt-completion pair. This allows us to use a single objective description or a single constraint description as the prompt to a fine-tuned LLM, and the fine-tuned LLM responds with its corresponding type number as the completion. 

## _3.3. Stage 3: Constraint generation and supplementation_ 

## _3.3.1. Constraint generation_ 

The third stage is to generate mathematical formulas for the objective function and constraints under the guidance of the templates. In Stage 2, we have identified whether a paragraph in the given problem description described an objective function or a type of constraint. For each paragraph, Stage 3 uses the predefined template corresponding to the type label classified in Stage 2 as part of the prompt to guide the LLM for _template matching_ , and further generates the mathematical expression using the variables defined in Stage 1. Here, template matching refers to matching the variables identified to the variable placeholders in the template and then substituting the identified variables into the placeholders for variables in the formula templates. In order to standardize the form of the answers generated by LLMs, we also use some instructions in combination with the template to form the prompt. Examples of the prompts for generating the objective function and some types of constraints can be found in Appendix A.2. 

A template for a constraint type explains the meaning of such constraint and the form of the corresponding mathematical formula. For logic constraint types, the templates also include the usual expression of the constraint in natural language to facilitate correct template matching by LLMs. For example, given binary variables _yA_ and _yB_ each taking the value of 1 are denoted as statements A and B each being true, the logic constraint belonging to type 10 is described in natural language as “If A (is true) then B (is true)”, which corresponds to the mathematical expression _yA ≤ yB_ . Given a description, for example, `if Product A is produced then Product B is produced` , the template for type 10 constraints allows LLMs to learn how to substitute the variables into the formula template. In this example, if the expression uses the “ _≤_ ” sign, then the binary variable representing the state of the proposition following “if” (whether Product A is produced) should be placed to the left-hand-side of the inequality sign, and the binary variable indicating the state of the proposition following “then” (whether Product B is produced) should be placed to the right-hand-side of the inequality sign. 

The main contents of the templates are shown in Table 2. Since LLMs are better at handling text prompts, we tend to use natural language in templates to describe the meaning and form of the formula, rather than using complex mathematical symbols directly as prompts. 

12 

Table 2: Templates for the objective function and 13 types of constraints. Consider Statements A and B with truth value represented binary variables _yA_ and _yB_ respectively - with 1 representing the statement is true and 0 otherwise. 

|**No.**|**Meaning**|**Formula template**|
|---|---|---|
|0|The objective function should specify a direction of op-<br>timization, either to maximize or minimize. Therefore,<br>the answer should only include the words “Maximize”<br>or “Minimize” and a linear expression.|sum of terms consisting of a variable<br>multiplied by one or more constant<br>coefficients|
|1|This constraint represents an upper bound on a single<br>decision variable.|variable _<_= constant|
|2|This constraint represents an upper bound on the sum<br>of decision variables.|sum of variables _<_= constant|
|3|This constraint represents an upper bound on the<br>weighted sum of decision variables.|sum of variables multiplied by their<br>weight _<_= constant|
|4|This constraint indicates that the upper bound on a<br>single variable is a constant proportion of the sum of<br>all variables.|one variable _<_= proportion * sum<br>of all variables|
|5|This constraint represents a lower bound on a single<br>decision variable.|variable _>_= constant|
|6|This constraint represents a lower bound on the sum of<br>decision variables.|sum of variables _>_= constant|
|7|This constraint represents a lower bound on the<br>weighted sum of decision variables.|sum of variables multiplied by their<br>weight _>_= constant|
|8|This constraint indicates that the lower bound on a<br>single variable is a proportion of the sum of all variables.|one variable _>_= proportion * sum<br>of all variables|
|9|This constraint is a comparison constraint between two<br>variables.|c * x _<_= y, where x and y are vari-<br>ables and c is a positive constant.|
|10|In natural language descriptions, this type of constraint<br>often contains a format like “If A then B” or “If not B<br>then not A”.|_yA <_=_yB_|
|11|In natural language descriptions, this type of constraint<br>often contains a format like “(Exactly) one of A and B”<br>or “Either A or B (but not both)”.|_yA_+_yB_ = 1|
|12|In natural language descriptions, this type of constraint<br>often contains a format like “At least one of A and B”<br>or “If not A then B” or “Either A or B or both”.|_yA_+_yB >_= 1|
|13|In natural language descriptions, this type of constraint<br>often contains a format like “At most one of A and B”<br>or “If A then not B” or “Either A or B or neither (but<br>not both)”.|_yA_+_yB <_= 1|



## _3.3.2. Constraint supplementation_ 

After each constraint or objective function in the problem description has been formulated, if the problem is not a pure binary problem (one that involves binary variables only), the final task of Stage 3 is to introduce two additional constraints for each binary indicator variable used in the generated mathematical model. Specifically, if any of the binary variables automatically generated in the second step of Stage 1 are used in the formulation, then the model needs to add two constraints for each used binary variable to link it to the corresponding continuous or integer variable. Even if the following two types of linking constraints are not explicitly mentioned in the problem description, they capture some business rules. 

For example, `if an investor decides not to invest in a particular stock, then the amount invested in this stock cannot be greater than 0` . To ensure that if the binary variable is equal 

13 

to 0, then its corresponding continuous or integer variable should be at most 0, we need to add the following constraint to the model, 



where _M_ is a constant representing a sufficiently large value. The binary variable is required to be equal to 1 if its corresponding continuous or integer variable is greater than 0. However, if this continuous or integer variable has an upper bound, _M_ will be replaced by this upper bound, and the upper bound constraint on this variable generated earlier in Stage 3 can be replaced by inequality (3). 

In addition, the binary variable should be 0 if its corresponding continuous or integer variable is equal to 0. In other words, if the binary variable is equal to 1 then its corresponding continuous or integer variable should be greater than 0. To enforce this, the following constraint should be added to the model, 



where again, _M_ is a sufficiently large constant. Taking an example in the investment context, the above constraint implies that `if an investor decides to invest in a particular stock, then this means that he needs to invest at least some amount that is greater than 0` . 

The objective function and constraints translated from the problem description plus automatically supplemented linking constraints (if needed) constitute the final MILP model as the output shown in Figure 2. 

## **4. Numerical Experiment** 

The proposed multi-stage framework requires the assistance of LLMs for variable identification in the first stage, constraint classification (with fine-tuned LLMs) in the second stage, and constraint generation in the third stage. In this numerical experiment, we employ two well-known LLMs: GPT and PaLM 2. The first variant, which we refer to as the multi-stage approach with GPT, fine-tunes GPT-3 to classify constraints and uses GPT-3.5 to identify variables and generate constraints. The second variant, which we refer to as the multi-stage approach with PaLM, adopts PaLM 2 in all the stages. 

We compare two variants of our approach with two baseline models that utilize zero-shot prompting to directly instruct the following chatbots in directly converting problem descriptions to mathematical models. 

- ChatGPT: AI-powered chatbot, powered by GPT-3.5 and developed by OpenAI. 

- Bard: chat-based AI tool, powered by PaLM 2 and developed by Google. 

## _4.1. Dataset and configuration for fine-tuning_ 

In our experiments, we fine-tuned two LLMs, GPT-3 and PaLM 2, to implement the classification prediction for a given segment description of an objective or a constraint. They were later used in Stage 2 when testing the entire framework. The first dataset on which we conduct the numerical experiment is for fine-tuning LLMs, namely training and validating classifiers. It consists of instances of objective descriptions and constraint descriptions as well as their annotated type labels. 

Each instance of NL4Opt dataset has a paragraph describing an LP problem. We deconstructed the 99 problem descriptions from the NL4Opt (development) dataset, and obtained 391 descriptions of objectives and constraints. Each problem description has only one objective function. These 292 constraints can be covered by nine types, i.e., types 1 to 9 in Table 1 and Table 3. However, the problems in the original NL4Opt dataset do not involve logic constraints. To extend the decomposed 

14 

NL4Opt dataset, we create a total of 183 descriptions of logic constraints involving two binary variables belonging to four types, i.e. types 10 to 13 in Table 1 and Table 3. The numbers of descriptions contained in these types are shown in Table 3. 

The dataset used for fine-tuning thus contains 574 pairs of descriptions and manually annotated type numbers, which are then divided into the training and validation sets automatically by the data preparation tool of OpenAI. Due to the relatively small size of the current dataset, the number of descriptions for some classes is small. There are only 7 descriptions for type 6, and they were all split into the training set, resulting in missing classes in the validation set which is not ideal. We therefore manually moved one description of type 6 from the training set to the validation set. As a result, the training set contains 464 descriptions, and the validation set contains 110 descriptions. For the purpose of a fair comparison, we use the same training set and validation set to fine-tune PaLM. 

Table 3: The dataset used in fine-tuning LLMs for constraint classification 

|**Type**<br>**No.**|**Type name**|**No.**<br>**of descriptions**<br>**from NL4Opt**|**No.**<br>**of descriptions**<br>**we create for tuning**|
|---|---|---|---|
|0|Objective function|99|-|
|1|Upper bound on single variable|20|-|
|2|Upper bound on sum of variables|12|-|
|3|Upper bound on weighted sum of variables|93|-|
|4|Upper bound on proportion|8|-|
|5|Lower bound on single variable|36|-|
|6|Lower bound on sum of variables|7|-|
|7|Lower bound on weighted sum of variables|59|-|
|8|Lower bound on proportion|14|-|
|9|Comparison constraints<br>|43|-|
|10|If A then B/ if not B then not A/ B if A<br>|-|46|
|11|Exactly one of A and B/ either A or B but<br>not both (or neither)|-|40|
|12|At least one of A and B/ if not A then B/<br>either A or B or both<br>|-|49|
|13|At most one of A and B/ if A then not B/<br>either A or B or neither (but not both)|-|48|



After preparing the dataset, we need to select the base model and the hyperparameters to start the automatic fine-tuning. GPT-3 series has four base models, which were the only models of OpenAI that could be fine-tuned at the time we conducted our experiments. For proof-of-concept purposes, we fine-tuned the base model called _ada_ for this specific text classification task, which is suitable for simple classification and is the fastest and least expensive. We also tuned the base model _text-bison001_ , which is the only base model of the PaLM API that can be tuned so far. Hyperparameters used for fine-tuning GPT-3 and PaLM, such as the number of epochs and batch size, can be found in Table A.5. Finding better classifiers using different configurations of the hyperparameters, namely hyperparameter tuning, can be left as further research for future work, which is not the focus of this paper for proof-of-concept purposes. 

## _4.2. Test set for evaluating the framework_ 

The second dataset on which we conduct numerical experiments is for evaluating the whole framework of automatic modeling. In contrast to NL4Opt dataset, we develop a new test set, comprising 30 MILP word problems to introduce the four types of logic constraints mentioned in Section 2. Each problem consists of its natural language description and a mathematical model (for evaluating the accuracy). For each problem, the model has a single objective function and several constraints. In the problem description, each paragraph describes either an objective function or a constraint. The dataset includes a total of 30 objective descriptions and 147 constraint descriptions. In terms of both natural language contexts and mathematical formulations, the problems within the new dataset showcase diversity. The descriptions of these problems span different domains, including production 

15 

planning, resource allocation, and transport. These problems include different combinations of more constraint types. 

Readers may find examples of the prompts given to ChatGPT and Bard as well as those used in the multi-stage framework in Appendix A.2. All data used in this paper is available as a GitHub repository ( `https://github.com/yangyangyang777/Datasets-for-automatic-modeling.git` ). 

## _4.3. Evaluation metrics_ 

We evaluate the performance of the framework using two instance-level and expression-level formulation accuracy metrics, ACC1 and ACC3. For evaluating the classification performance of Stage 2, we also consider another expression-level classification accuracy, ACC2. The formulas for the three metrics are given below. 







Here, the number of problem instances in the test set is denoted by _N_ . The total number of the objective descriptions and constraint descriptions contained in the problem description of instance _i_ is denoted as _Di_ . For a given instance _i_ , _Ti_ takes the value of 1 if the generated model is completely accurate (including linking constraints if any) and 0 otherwise. For the expression-level metrics, _TCi_ is the number of objective and constraint descriptions in instance _i_ that are correctly classified, and _TEi_ is the number of objective and constraint descriptions that are correctly formulated. 

We do not specifically investigate the accuracy of variable identification in this section. If the decision variables of instance _i_ are incorrectly identified (variables are missing and/or unneeded variables are defined), it would be reflected by _Ti_ . Specifically, if some decision variable(s) of instance _i_ is missing, then the model is incorrect, at least partially wrong, and hence _Ti_ = 0. If some redundant variable(s) is defined, the model is incorrect and _Ti_ = 0 unless the redundant variable does not appear in any of the objective and constraint expressions but only in the variable list. 

## _4.4. Fine-tuning results_ 

We use classification accuracy to initially evaluate the performance of the fine-tuned GPT-3 and PaLM on the validation set, before integrating them with the framework and evaluating the whole framework on the test set. Similar to the ACC2 metric, classification accuracy here refers to the number of objective and constraint descriptions that are correctly classified divided by the total number of descriptions in the fine-tuning validation set. 

The accuracy of the fine-tuned GPT-3 reached 99.09%. Only one instance in the validation set containing 110 instances was misclassified. The description CD1 was classified as class 4 (Upper bound on proportion), but the actual class is class 2 (Upper bound on the sum of decision variables). In the training set, both types 2 and 4 have less than 10 constraints. The small number of samples available for learning may have led to this misclassification. OpenAI hypothesized that the model would perform better with at least 100 examples per class in theory. Expanding the dataset for constraint classification should be a future task, especially for those classes with few instances, so that LLMs can learn patterns from more instances. 

Constraint description 1 (CD1) `Bold Tycoon decides to invest his money in GICs and index ETF. Bold Tycoon wants to invest` $10 _,_ 000 `in total.` 

16 

Constraint description 2 (CD2) `A waste treatment company must remove waste using a large container or a medium container. There must be at most 65 total containers.` 

The tuned PaLM obtained an accuracy of 98.18%. Two instances in the validation set were misclassified. But by analyzing the results it appears to be more reliable than the fine-tuned GPT-3 on constraint classification. The description CD1 was classified as type 3 (Upper bound on weighted sum of variables), which makes sense somehow since the actual class (upper bound on sum of decision variables) is a special case of type 3. The misclassification of CD2 was the same as that of CD1. Type 3 contains far more constraints than any other constraint type since it is very common in practice, and this imbalanced fine-tuning dataset may have an impact on strict constraint classification. However, fuzzy (not uniquely correct) classifications similar to the above is acceptable in terms of modeling. 

## _4.5. Modeling results_ 

We assessed the two variants of the multi-stage framework on the new instance set consisting of 30 problems and compared them with two baselines. The experimental results in Table 4 reveal that the multi-stage approaches which integrate knowledge representation with the two LLMs significantly outperform the one-step model-generation methods by ChatGPT and Bard with respect to the accuracies at both the model and expression levels. Between the two LLMs, the two methods powered by the GPT models outperform those powered by PaLM. 

Table 4: Results of the multi-stage framework (utilizing GPT models or PaLM) proposed in this paper and two baseline models, ChatGPT and Bard. 

||**Multi-stage**<br>**approach with**<br>**GPT**|**Multi-stage**<br>**approach**<br>**with PaLM**|**ChatGPT**|**Bard**|
|---|---|---|---|---|
|ACC1<br>ACC2|0.8667<br>0.9944|0.7<br>0.9887|0.2667<br>-|0.1667<br>-|
|ACC3|0.9774|0.9435|0.8475|0.7627|
|No. of incorrect models|4|9|22|25|
|No. of incorrect objectives|3|4|2|3|
|No. of incorrect constraints|1|6|25|40|
|No. of models missing linking<br>constraints|1|0|17|17|



## _Cases missed by the multiple-stage approach_ 

The multi-stage approach using GPT did not formulate the correct models for four problem instances in the test dataset. Among them, three models were incorrect because the coefficients of the variables in the generated objective functions were wrong. Taking one of the three models as an example, the objective is to maximize the total profit. The coefficients for computing the profits should be expressed as the differences between selling prices and costs, yet the generated objective function used selling prices directly as coefficients. The multi-stage approach with PaLM and the one-step approach with Bard made the same mistake. Surprisingly, ChatGPT correctly formulated the objective function for the profit maximization. The errors in the other two objective functions were due to the failure to perform unit conversions on the coefficients. Taking one of these two problems as an example, the variables are in minutes. The data referring to the variable coefficients in the objective function description are in minutes per kilometer. They cannot be used as coefficients directly since their inverse (in kilometers per minute) should be used. The multi-stage approach with PaLM, ChatGPT and Bard all failed to notice the inconsistency in the units and derived incorrect models for the two problems. In the future, to improve the multi-stage approach, we may consider including an additional calculation phase for unit conversion. 

17 

Our framework with GPT misclassified one logic constraint as a non-logic constraint, giving this classification model an accuracy ACC2 of 99.44% on the test dataset. As a result, the constraint was incorrectly formulated. We took a closer look at the problem instance, which is to determine the number of orders from three manufacturers. The description of the misclassified constraint is given below. 

Constraint description 3 (CD3): `If the store decides to order chairs from manufacturer A, they must also order at least 10 chairs from manufacturer B.` 

CD3 belongs to the logic constraint of the type “if A then B” (i.e., type 10 in Table 1). However, the second half of the sentence is close to the description of the basic lower bound constraint (i.e., type 5 in Table 1). The chance of accurately classifying it would be improved if the method makes use of the information from other constraint descriptions of this problem. From the whole problem description, it can be noticed that one type of decisions to be made is to determine the number of orders from different manufacturers (integer variables). Specifically, another constraint description is “ `Each order from manufacturer A will include 15 chairs, while each order from B and C will include 10 chairs.` ”. With that, CD3 is equivalent to “ `If the store decides to order chairs from manufacturer A, they must also order chairs from manufacturer B.` ”. Classifying and modeling this equivalent description is less challenging. This example suggests that it requires global information as well as logical reasoning for modeling challenging constraint descriptions. Similarly, our framework with PaLM misclassified CD3 as another type of logic constraint thus failing to formulate it correctly. Google Bard and ChatGPT also failed to model it correctly. 

Since the multi-stage approach with GPT formulated CD3 as a non-logic constraint, its mathematical expression did not use binary variables. As a result, the linking constraint attached to the binary variables for the logic constraint was missed in the final model of the problem, which explains the missing linking constraint in Table 4 (second column, last row). On the other hand, the approach with PaLM classified CD3 as a logic constraint using two binary variables therefore the corresponding linking constraints were added. For this problem, ChatGPT and Bard did not correctly formulate any of the logic constraints and did not add the linking constraints. 

In addition to the above mentioned, more mistakes were made by the multi-stage approach using PaLM and these were mainly due to missing coefficients of variables, and incorrect direction of the inequality (ignoring the specification of upper or lower bounds in the template). 

## _Cases missed by ChatGPT and Bard_ 

ChatGPT’s mistakes are mainly in the formulation of constraints; in particular, failing to formulate 20 logic constraints, often due to its failures in identifying the binary variables. These constraints were formulated as logic constraints in terms of integer and continuous variables. But even for those problems where it correctly generated expressions for logic constraints, ChatGPT missed the linking constraints, leading to incorrect final models. For other types of constraints, common mistakes include having the wrong coefficients for the variables and missing variables. 

Furthermore, ChatGPT missed three constraints in three problem descriptions. For another problem instance, ChatGPT generated a constraint that is not mentioned in the given problem description. Both of the errors were impossible to occur within our framework. 

In comparison, Bard’s performance was worse than that of ChatGPT. Bard only generated correct models for five of the thirty instances. Bard was more prone to miss constraints than ChatGPT, missing 7 constraints in total. Bard failed more times than ChatGPT on the formulation of both the basic constraints and the logic constraints. ChatGPT made 4 mistakes for basic constraints, and Bard made 14 due to using wrong variables, coefficients, the direction of inequality in the constraints, etc. There is also a special class of errors that Bard made, using unexpected variables outside of the given problem description to formulate a constraint. For one problem instance with seven continuous 

18 

variables, Bard correctly identified and defined the seven continuous variables, but used an eighth continuous variable in a constraint whilst this variable was not defined by Bard and not included in the problem description. 

Bard was less reliable in formulating logic constraints. One important finding is that Bard could only correctly formulate logic constraints for pure binary programming models. For MILP problems, it did not once identify binary variables thus failing to correctly formulate logic constraints, not to mention the linking constraints. In contrast, ChatGPT successfully identified binary variables for a few MILP problems. 

## _Variable identification_ 

For every instance in the test dataset, the variable identification procedure of our framework successfully defined all the variables needed to build its mathematical model, especially the binary variables, which facilitates high accuracy in the subsequent formulation phase. LLMs by themselves are often unaware of binary variables involved in the problem description and have less knowledge about logic constraints. 

## **5. Conclusion** 

In this paper, we propose a three-stage framework to automatically synthesize MILP models from unstructured natural language descriptions of decision problems. This framework can employ LLMs to perform tasks in all stages, namely the identification of decision variables, the classification of objective and constraints, and the generation of the MILP model. We propose a constraint recognition method for Stage 2 by using the modified NL4Opt dataset to fine-tune LLMs as constraint classifiers. We build constraint templates to instruct LLMs to generate formulas for Stage 3. 

The framework can be adapted to make it capable of handling more types of constraints for more complex MILP problems. For the purpose of proof-of-concept, we first extended the application of the framework to four types of logic constraints, in contrast to previous studies that can only handle classic demand and resource constraints. To fill this gap, we developed a dataset of the MILP word problems with logic constraints. The results of testing the framework on this dataset show that our method which integrates knowledge representation significantly outperforms one that uses LLMs alone. The accuracy of generating the correct model can be improved by about 50% to 60%. 

Some directions can be explored as future work. For the framework presented in this paper, we assume that a full problem description has been provided as input. In the next step, we will adjust the framework to another scenario, assuming that we elicit from the user information sufficient to construct an optimization model through a question-and-answer dialogue system. In this context, the two modules of eliciting the problem description and mathematical formulation will not be separated, but may be more interactive. Such a problem elicitation approach may facilitate automatic partitioning between constraint descriptions, which is done manually in this paper. This paper focuses on the translation of natural language problem descriptions to mathematical models, and further translation to modeling languages for integration with solvers is future work. The performance of the LLMs integrated in this framework can potentially be improved by adding appropriate few-shot examples to the prompts. The dataset needs to be expanded to include not only more contexts but also more constraint types and optimization problem types. Testing the capability of LLMs to generate new MILP word problems can facilitate exploring systematic generation of instances. 

## **Acknowledgment** 

This work was partially funded by the Australian Research Council, Australia through the Discovery Project 2022 (grant number DP220101925). It was partially funded by the Australian Government 

19 

through the Australian Research Council Industrial Transformation Training Centre in Optimisation Technologies, Integrated Methodologies, and Applications (OPTIMA), Project ID IC200100009. 

## **References** 

- AhmadiTeshnizi, A., Gao, W. and Udell, M. (2023), ‘OptiMUS: Optimization Modeling Using mip Solvers and large language models’. **URL:** _http://arxiv.org/abs/2310.06116_ 

- Almonacid, B. (2023), ‘Towards an Automatic Optimisation Model Generator Assisted with Generative Pre-trained Transformer’. 

   - **URL:** _http://arxiv.org/abs/2305.05811_ 

- Brown, T. B., Mann, B., Ryder, N., Subbiah, M., Kaplan, J., Dhariwal, P., Neelakantan, A., Shyam, P., Sastry, G., Askell, A., Agarwal, S., Herbert-Voss, A., Krueger, G., Henighan, T., Child, R., Ramesh, A., Ziegler, D. M., Wu, J., Winter, C., Hesse, C., Chen, M., Sigler, E., Litwin, M., Gray, S., Chess, B., Clark, J., Berner, C., McCandlish, S., Radford, A., Sutskever, I. and Amodei, D. (2020), ‘Language Models are Few-Shot Learners’. 

   - **URL:** _http://arxiv.org/abs/2005.14165_ 

- Chen, D.-S., Batson, R. G. and Dang, Y. (2009), _Applied Integer Programming_ , Wiley. **URL:** _https://doi.org/10.1002/9781118166000_ 

- Dakle, P. P., Kadıo˘glu, S., Uppuluri, K., Politi, R., Raghavan, P., Rallabandi, S. and Srinivasamurthy, R. (2023), Ner4Opt: Named Entity Recognition for Optimization Modelling from Natural Language, _in_ A. A. Cire, ed., ‘Integration of Constraint Programming, Artificial Intelligence, and Operations Research’, Springer Nature Switzerland, pp. 299–319. 

- Doan, X.-D. (2022), ‘VTCC-NLP at NL4Opt competition subtask 1: An Ensemble Pre-trained language models for Named Entity Recognition’. **URL:** _http://arxiv.org/abs/2212.07219_ 

- Fajemisin, A. O., Maragno, D. and den Hertog, D. (2023), ‘Optimization with constraint learning: A framework and survey’. **URL:** _https://www.sciencedirect.com/science/article/pii/S0377221723003405_ 

- Gangwar, N. and Kani, N. (2023), ‘Highlighting Named Entities in Input for Auto-Formulation of Optimization Problems’. **URL:** _http://arxiv.org/abs/2212.13201_ 

- Gorman, M. F., Nittala, L. and Alden, J. M. (2020), ‘Anatomy of the edelman: Measuring the world’s best analytics projects’, _INFORMS Journal on Applied Analytics_ **50** (6), 373–386. **URL:** _https://doi.org/10.1287/inte.2020.1052_ 

- He, J., N, M., Vignesh, S., Kumar, D. and Uppal, A. (2022), ‘Linear programming word problems formulation using EnsembleCRF NER labeler and T5 text generator with data augmentations’. **URL:** _http://arxiv.org/abs/2212.14657_ 

- INFORMS (2013), ‘2013 franz edelman finalists’, `https://www.informs.org/content/download/ 279469/2673366/file/2013edelman_finalWEB.pdf` . 

- Islam, M. S., Mamud, F., Haque, R. U., Saber, A. Y. and Saha, A. K. (2021), Automatic formulation and optimization of linear problems from a structured paragraph, _in_ ‘2021 International Conference on Science & Contemporary Technologies (ICSCT)’, pp. 1–6. 

- Jang, S. (2022), ‘Tag Embedding and Well-defined Intermediate Representation improve AutoFormulation of Problem Description’. **URL:** _http://arxiv.org/abs/2212.03575_ 

20 

- J¨unger, M., Liebling, T. M., Naddef, D., Nemhauser, G. L., Pulleyblank, W. R., Reinelt, G., Rinaldi, G. and Wolsey, L. A., eds (2010), _50 Years of Integer Programming 1958-2008 - From the Early Years to the State-of-the-Art_ , Springer. 

   - **URL:** _https://doi.org/10.1007/978-3-540-68279-0_ 

- Kojima, T., Gu, S. S., Reid, M., Matsuo, Y. and Iwasawa, Y. (2023), ‘Large Language Models are Zero-Shot Reasoners’. **URL:** _http://arxiv.org/abs/2205.11916_ 

- Kumar, M., Teso, S. and De Raedt, L. (2019), _Acquiring Integer Programs from Data_ . 

- Li, B., Mellou, K., Zhang, B., Pathuri, J. and Menache, I. (2023), ‘Large Language Models for Supply Chain Optimization’. **URL:** _http://arxiv.org/abs/2307.03875_ 

- Mukherjee, A. and Garain, U. (2008), ‘A review of methods for automatic understanding of natural language mathematical problems’, **29** (2), 93–122. **URL:** _https://doi.org/10.1007/s10462-009-9110-0_ 

- Ning, Y., Liu, J., Qin, L., Xiao, T., Xue, S., Huang, Z., Liu, Q., Chen, E. and Wu, J. (2023), ‘A Novel Approach for Auto-Formulation of Optimization Problems’. **URL:** _http://arxiv.org/abs/2302.04643_ 

- Ofoghi, B. and Yearwood, J. (2023), ‘Knowledge representation of mathematical optimization problems and constructs for modeling’, _Knowledge-Based Systems_ **280** , 110980. **URL:** _https://www.sciencedirect.com/science/article/pii/S095070512300730X_ 

- OpenAI (2023), ‘Fine-tuning for GPT-3’. 

   - **URL:** _https://platform.openai.com/docs/guides/legacy-fine-tuning_ 

- Pawlak, T. P. and Krawiec, K. (2017), ‘Automatic synthesis of constraints from examples using mixed integer linear programming’, **261** (3), 1141–1157. **URL:** _https://www.sciencedirect.com/science/article/pii/S037722171730156X_ 

- Pawlak, T. P. and O’Neill, M. (2021), ‘Grammatical evolution for constraint synthesis for mixedinteger linear programming’, **64** , 100896. 

**URL:** _https://www.sciencedirect.com/science/article/pii/S2210650221000572_ 

- Prasath, G. and Karande, S. (2023), ‘Synthesis of Mathematical programs from Natural Language Specifications’. **URL:** _http://arxiv.org/abs/2304.03287_ 

- Ramamonjison, R., Li, H., Yu, T. T., He, S., Rengan, V., Banitalebi-Dehkordi, A., Zhou, Z. and Zhang, Y. (2022), ‘Augmenting Operations Research with Auto-Formulation of Optimization Models from Problem Descriptions’. 

   - **URL:** _http://arxiv.org/abs/2209.15565_ 

- Ramamonjison, R., Yu, T. T., Li, R., Li, H., Carenini, G., Ghaddar, B., He, S., Mostajabdaveh, M., Banitalebi-Dehkordi, A., Zhou, Z. and Zhang, Y. (2023), ‘NL4Opt Competition: Formulating Optimization Problems Based on Their Natural Language Descriptions’. **URL:** _http://arxiv.org/abs/2303.08233_ 

- Sroka, D. and Pawlak, T. P. (2018), One-class constraint acquisition with local search, _in_ ‘Proceedings of the Genetic and Evolutionary Computation Conference’, GECCO ’18, Association for Computing Machinery, pp. 363–370. 

**URL:** _https://dl.acm.org/doi/10.1145/3205455.3205480_ 

- Tsouros, D., Verhaeghe, H., Kadıo˘glu, S. and Guns, T. (2023), _Holy Grail 2.0: From Natural Language to Constraint Models_ . 

21 

- Wang, J., Gupta, A. and Wang, C. (2023), ‘Synthesizing MILP Constraints for Efficient and Robust Optimization’, **7** , 184:1896–184:1919. 

   - **URL:** _https://dl.acm.org/doi/10.1145/3591298_ 

- Wang, K., Chen, Z. and Zheng, J. (2023), ‘OPD@NL4Opt: An ensemble approach for the NER task of the optimization problem’. **URL:** _http://arxiv.org/abs/2301.02459_ 

- Yang, C., Wang, X., Lu, Y., Liu, H., Le, Q. V., Zhou, D. and Chen, X. (2023), ‘Large Language Models as Optimizers’. 

   - **URL:** _http://arxiv.org/abs/2309.03409_ 

- Zhang, D., Wang, L., Zhang, L., Dai, B. T. and Shen, H. (2019), ‘The Gap of Semantic Parsing: A Survey on Automatic Math Word Problem Solvers’, **PP** , 1–1. 

- Zong, M. and Krishnamachari, B. (2023), ‘Solving Math Word Problems concerning Systems of Equations with GPT-3’, **37** (13), 15972–15979. 

   - **URL:** _https://ojs.aaai.org/index.php/AAAI/article/view/26896_ 

22 

## **Appendix A. Appendix** 

## _Appendix A.1. Hyperparameters for fine-tuning_ 

Hyperparameters used for fine-tuning GPT-3 and PaLM are shown in Table A.5. OpenAI (2023) suggests that the default values of the hyperparameters they have picked work well in various use cases. The recommended batch size is about 0.2% of the number of instances in the training set, which we set to 1. 

Table A.5: Hyperparameters used for fine-tuning GPT-3 and PaLM 

|**Hyperparameter**<br>**for**|**Value**|**Hyperparameter**<br>**for**|**Value**|
|---|---|---|---|
|**fine-tuning GPT-3**||**fine-tuning PaLM**||
|Epochs|4 (default)|Epochs|20|
|Batch size|1|Batch size|24|
|Learning rate multiplier|default|Learning rate|0.02|



## _Appendix A.2. Prompt examples_ 

Taking the problem in Figure 2 as an example, a few prompt examples are depicted in Table A.6 - Table A.12. Problem-specific texts have been <mark>shaded.</mark> The prompt examples for constraint generation (Table A.9 - Table A.12) are displayed in the order in which these constraints appear in the problem description. 

Table A.6: An example of the prompts to ChatGPT and Bard 

Assuming you are an expert in the field of mixed-integer programming, please formulate the following problem as a mixed-integer linear programming model and ensure that the model is presented in LaTeX syntax. 

<mark>Haus Toys can make and sell toy trucks, toy aeroplanes, toy ships, and toy trains. The prof</mark> i <mark>t for each truck sold</mark> is <mark>$5, each aeroplane sold</mark> is <mark>$10, each ship sold</mark> is <mark>$8, and each train sold</mark> is <mark>$7. How many</mark> of <mark>each type</mark> of <mark>toys should Haus Toys make</mark> to <mark>maximise the prof</mark> i <mark>t?</mark> 

<mark>There are 890 units</mark> of <mark>timber available. The amount</mark> of <mark>timber</mark> r <mark>equired</mark> is 12 <mark>units for each truck,</mark> 20 <mark>units for each aeroplane,</mark> 15 <mark>units for each ship, and</mark> 10 <mark>units for each train.</mark> 

<mark>The are 500 units</mark> of <mark>steel available. The amount</mark> of <mark>steel</mark> r <mark>equired</mark> is 3 <mark>units for each aeroplane,</mark> 5 <mark>units for each ship,</mark> 4 <mark>units for each train, and</mark> 6 <mark>units for each truck.</mark> If <mark>Haus Toys makes trucks, then they will not make trains.</mark> If <mark>they make ships, however, they will also make aeroplanes. The number</mark> of <mark>toy ships made cannot</mark> e <mark>xceed the number</mark> of <mark>trains made. Haus Toys must also make</mark> at <mark>least twice</mark> as <mark>many ships</mark> as <mark>aeroplanes.</mark> 

23 

Table A.7: An example of the prompt for variable identification 

You need to formulate the following given problem as a mixed integer programming (MIP) model. But now you just need to define the decision variables. 

MIP Problem Description: <mark>Haus Toys can make and sell toy trucks, toy aeroplanes, toy ships, and toy trains. The prof</mark> i <mark>t for each truck sold</mark> is <mark>$5, each aeroplane sold</mark> is <mark>$10, each ship sold</mark> is <mark>$8, and each train sold</mark> is <mark>$7. How many</mark> of <mark>each type</mark> of <mark>toys should Haus Toys make</mark> to <mark>maximise the prof</mark> i <mark>t? There are 890 units</mark> of <mark>timber available. The amount</mark> of <mark>timber</mark> r <mark>equired</mark> is 12 <mark>units for each truck,</mark> 20 <mark>units for each aeroplane,</mark> 15 <mark>units for each ship, and</mark> 10 <mark>units for each train. There are 500 units</mark> of <mark>steel available. The amount</mark> of <mark>steel</mark> r <mark>equired</mark> is 3 <mark>units for each aeroplane,</mark> 5 <mark>units for each ship,</mark> 4 <mark>units for each train, and</mark> 6 <mark>units for each truck.</mark> If <mark>Haus Toys makes trucks, then they will not make trains.</mark> If <mark>they make ships, however, they will also make aeroplanes. The number</mark> of <mark>toy ships made cannot</mark> e <mark>xceed the number</mark> of <mark>trains made. Haus Toys must also make</mark> at <mark>least twice</mark> as <mark>many ships</mark> as <mark>aeroplanes.</mark> 

Please first identify the continuous variables and/or non-binary integer variables in the mixed-integer linear programming problem and provide them as a Python list. If you can find either of these two types of variables, there is no need to find binary variables and include binary variables as part of your answer. If you do not think there are any continuous or integer variables involved in the problem description, then give as an answer a Python list consisting only of the binary variables that you identified as the decision variables for the problem. 

A binary variable usually represents a decision about whether a single activity is carried out or not, such as whether a person does something or not, or whether a class of products is produced or not. Binary variables must be named by starting with “bi ” and linking “bi ” to the name of the entity it represents. 

An integer variable or continuous variable should describe the decision to be made, usually the quantity to be determined. An integer variable or continuous variable often corresponds to some parameters that represent attributes such as profit, cost, resource consumption per unit, etc. Your answer should only include one list of variable names. Your answer does not need to specify the type of variable and provide any explanation. The variable needs to be named with the name of the quantity it represents and stored in a list. For example, the integer variable representing the quantity of vanilla cakes to be made is named vanilla ~~c~~ akes. 

Note that your answer must contain only a list consisting entirely of non-binary integer variables and continuous variables, or a list consisting entirely of binary variables, not a mixed list. 

You need to be aware that the (weighted) sums of some quantities, such as total amount of products, total space, total production time, total amount of resources used, and total cost, are not directly considered as a decision variable if they can be expressed as a (weighted) sum of the variables representing those quantities. 

24 

Table A.8: An example of the prompt for objective function generation 

You need to formulate the following given problem as a mixed integer programming (MIP) model. But now you just need to define the objective function. 

Full problem description to give you context: <mark>Haus Toys can make and sell toy trucks, toy aeroplanes, toy ships, and toy trains. The prof</mark> i <mark>t for each truck sold</mark> is <mark>$5, each aeroplane sold</mark> is <mark>$10, each ship sold</mark> is <mark>$8, and each train sold</mark> is <mark>$7. How many</mark> of <mark>each type</mark> of <mark>toys should Haus Toys make</mark> to <mark>maximise the prof</mark> i <mark>t? There are 890 units</mark> of <mark>timber available. The amount</mark> of <mark>timber</mark> r <mark>equired</mark> is 12 <mark>units for each truck,</mark> 20 <mark>units for each aeroplane,</mark> 15 <mark>units for each ship, and</mark> 10 <mark>units for each train. The are 500 units</mark> of <mark>steel available. The amount</mark> of <mark>steel</mark> r <mark>equired</mark> is 3 <mark>units for each aeroplane,</mark> 5 <mark>units for each ship,</mark> 4 <mark>units for each train, and</mark> 6 <mark>units for each truck.</mark> If <mark>Haus Toys makes trucks, then they will not make trains.</mark> If <mark>they make ships, however, they will also make aeroplanes. The number</mark> of <mark>toy ships made cannot</mark> e <mark>xceed the number</mark> of <mark>trains made. Haus Toys must also make</mark> at <mark>least twice</mark> as <mark>many ships</mark> as <mark>aeroplanes.</mark> 

Description of Objective Function: <mark>Haus Toys can make and sell toy trucks, toy aeroplanes, toy ships, and toy trains. The prof</mark> i <mark>t for each truck sold</mark> is <mark>$5, each aeroplane sold</mark> is <mark>$10, each ship sold</mark> is <mark>$8, and each train sold</mark> is <mark>$7. How many</mark> of <mark>each type</mark> of <mark>toys should Haus Toys make</mark> to <mark>maximise the prof</mark> i <mark>t?</mark> 

Please select the relevant variables from the continuous (or integer) variables <mark>[‘trucks’, ‘aeroplanes’, ‘ships’, ‘trains’]</mark> to build the objective function. Do not change the names of the variables in the list when generating expressions. You must only use the relevant constants from the description of the objective function as the parameters or coefficients of the resulting expression. The parameters or coefficients may involve additional calculations or conversions of units. The resulting expression will not necessarily involve all the variables in the variable list provided. You do not need to model other constraints in the problem. 

Your answer needs to indicate whether the objective function should be maximized or minimized. Therefore, your answer should only include the words “Maximize” or “Minimize” and an expression. 

Please provide the requested information without any extra or unnecessary details and explanations beyond what is explicitly asked. 

If the objective function is about profit and the value of the product’s profit is given directly, then there is no need to use the difference between the selling price and the cost of the product to calculate the profit value. In this case, the total profit is the sum of the individual profits, independent of costs. If the profit value of a product is not explicitly given, the difference between the selling price and the cost of the product should be used to calculate the profit value. 

25 

Table A.9: An example of the prompt for type 3 constraint generation 

You need to formulate the following given problem as a mixed integer programming (MIP) model. But now you just need to define a single constraint of the model. Full problem description to give you context: <mark>Haus Toys can make and sell toy trucks, toy aeroplanes, toy ships, and toy trains. The prof</mark> i <mark>t for each truck sold</mark> is <mark>$5, each aeroplane sold</mark> is <mark>$10, each ship sold</mark> is <mark>$8, and each train sold</mark> is <mark>$7. How many</mark> of <mark>each type</mark> of <mark>toys should Haus Toys make</mark> to <mark>maximise the prof</mark> i <mark>t? There are 890 units</mark> of <mark>timber available. The amount</mark> of <mark>timber</mark> r <mark>equired</mark> is 12 <mark>units for each truck,</mark> 20 <mark>units for each aeroplane,</mark> 15 <mark>units for each ship, and</mark> 10 <mark>units for each train. The are 500 units</mark> of <mark>steel available. The amount</mark> of <mark>steel</mark> r <mark>equired</mark> is 3 <mark>units for each aeroplane,</mark> 5 <mark>units for each ship,</mark> 4 <mark>units for each train, and</mark> 6 <mark>units for each truck.</mark> If <mark>Haus Toys makes trucks, then they will not make trains.</mark> If <mark>they make ships, however, they will also make aeroplanes. The number</mark> of <mark>toy ships made cannot</mark> e <mark>xceed the number</mark> of <mark>trains made. Haus Toys must also make</mark> at <mark>least twice</mark> as <mark>many ships</mark> as <mark>aeroplanes.</mark> 

Constraint Description: <mark>There are 890 units</mark> of <mark>timber available. The amount</mark> of <mark>timber</mark> r <mark>equired</mark> is 12 <mark>units for each truck,</mark> 20 <mark>units for each aeroplane,</mark> 15 <mark>units for each ship, and</mark> 10 <mark>units for each train.</mark> 

This constraint represents an upper bound on the weighted sum of decision variables. The expression for the constraint has the format “weighted sum of variables _<_ = constant representing the upper bound”. Each variable in the constraint inequality will be multiplied by a parameter (weight). This parameter must be a constant mentioned in the constraint description above. Please find the correct parameter in the description that corresponds to each variable to substitute into the inequality based on the variable name. 

Please use the variables <mark>[‘trucks’, ‘aeroplanes’, ‘ships’, ‘trains’]</mark> to model this constraint without making any alterations to the variable names. You do not need to model other constraints or the objective function in the problem. The resulting expression will not necessarily involve all the variables in the variable list provided. Ensure that the variables in the generated expression completely retain their original names from the list. 

Use the symbols “ _>_ =”, “ _<_ =”, and “=” to denote greater than or equal to, less than or equal to, and equal to, respectively. 

Your answer must only be a mathematical expression and do not provide any explanation. 

26 

Table A.10: An example of the prompt for type 13 logic constraint generation 

You need to formulate the following given problem as a mixed integer programming (MIP) model. But now you just need to define a single logic constraint of the model. Full problem description to give you context: <mark>Haus Toys can make and sell toy trucks, toy aeroplanes, toy ships, and toy trains. The prof</mark> i <mark>t for each truck sold</mark> is <mark>$5, each aeroplane sold</mark> is <mark>$10, each ship sold</mark> is <mark>$8, and each train sold</mark> is <mark>$7. How many</mark> of <mark>each type</mark> of <mark>toys should Haus Toys make</mark> to <mark>maximise the prof</mark> i <mark>t? There are 890 units</mark> of <mark>timber available. The amount</mark> of <mark>timber</mark> r <mark>equired</mark> is 12 <mark>units for each truck,</mark> 20 <mark>units for each aeroplane,</mark> 15 <mark>units for each ship, and</mark> 10 <mark>units for each train. The are 500 units</mark> of <mark>steel available. The amount</mark> of <mark>steel</mark> r <mark>equired</mark> is 3 <mark>units for each aeroplane,</mark> 5 <mark>units for each ship,</mark> 4 <mark>units for each train, and</mark> 6 <mark>units for each truck.</mark> If <mark>Haus Toys makes trucks, then they will not make trains.</mark> If <mark>they make ships, however, they will also make aeroplanes. The number</mark> of <mark>toy ships made cannot</mark> e <mark>xceed the number</mark> of <mark>trains made. Haus Toys must also make</mark> at <mark>least twice</mark> as <mark>many ships</mark> as <mark>aeroplanes.</mark> Constraint Description: If <mark>Haus Toys makes trucks, then they will not make trains.</mark> 

This constraint belongs to a subtype of logic constraints. Please use the binary variables <mark>[‘bi</mark> ~~<mark>t</mark>~~ <mark>rucks’, ‘bi</mark> ~~<mark>a</mark>~~ <mark>eroplanes’, ‘bi</mark> ~~<mark>s</mark>~~ <mark>hips’, ‘bi trains’]</mark> to model this logic constraint according to the following guidance. Do not change the names of the variables in the list when generating expressions. You do not need to model other constraints or the objective function in the problem. The resulting expression will not necessarily involve all the variables in the list. 

Use the symbols “ _>_ =”, “ _<_ =”, and “=” to denote greater than or equal to, less than or equal to, and equal to, respectively. 

Template: Consider Statements A and B with truth value represented binary variables a, b respectively - with 1 representing a statement is true and 0 otherwise. In natural language descriptions, this type of constraint often contains a format like “At most one of A and B” or “If A then not B” or “Either A or B or neither (but not both)”, which corresponds to the mathematical formula a + b _<_ = 1. Please match the variables in the given constraint description with the variables in the template to generate the correct mathematical expression. 

Your answer can only be a mathematical expression and do not provide any explanation. 

27 

Table A.11: An example of the prompt for type 10 logic constraint generation 

You need to formulate the following given problem as a mixed integer programming (MIP) model. But now you just need to define a single logic constraint of the model. Full problem description to give you context: <mark>Haus Toys can make and sell toy trucks, toy aeroplanes, toy ships, and toy trains. The prof</mark> i <mark>t for each truck sold</mark> is <mark>$5, each aeroplane sold</mark> is <mark>$10, each ship sold</mark> is <mark>$8, and each train sold</mark> is <mark>$7. How many</mark> of <mark>each type</mark> of <mark>toys should Haus Toys make</mark> to <mark>maximise the prof</mark> i <mark>t? There are 890 units</mark> of <mark>timber available. The amount</mark> of <mark>timber</mark> r <mark>equired</mark> is 12 <mark>units for each truck,</mark> 20 <mark>units for each aeroplane,</mark> 15 <mark>units for each ship, and</mark> 10 <mark>units for each train. The are 500 units</mark> of <mark>steel available. The amount</mark> of <mark>steel</mark> r <mark>equired</mark> is 3 <mark>units for each aeroplane,</mark> 5 <mark>units for each ship,</mark> 4 <mark>units for each train, and</mark> 6 <mark>units for each truck.</mark> If <mark>Haus Toys makes trucks, then they will not make trains.</mark> If <mark>they make ships, however, they will also make aeroplanes. The number</mark> of <mark>toy ships made cannot</mark> e <mark>xceed the number</mark> of <mark>trains made. Haus Toys must also make</mark> at <mark>least twice</mark> as <mark>many ships</mark> as <mark>aeroplanes.</mark> Constraint Description: If <mark>they make ships, however, they will also make aeroplanes.</mark> This constraint belongs to a subtype of logic constraints. Please use the binary variables <mark>[‘bi</mark> ~~<mark>t</mark>~~ <mark>rucks’, ‘bi</mark> ~~<mark>a</mark>~~ <mark>eroplanes’, ‘bi</mark> ~~<mark>s</mark>~~ <mark>hips’, ‘bi trains’]</mark> to model this logic constraint according to the following guidance. Do not change the names of the variables in the list when generating expressions. You do not need to model other constraints or the objective function in the problem. The resulting expression will not necessarily involve all the variables in the list. Use the symbols “ _>_ =”, “ _<_ =”, and “=” to denote greater than or equal to, less than or equal to, and equal to, respectively. 

Template: Consider Statements A and B with truth value represented binary variables a, b respectively - with 1 representing a statement is true and 0 otherwise. In natural language descriptions, this type of constraint often contains a format like “If A then B” or “If not B then not A”, which corresponds to the mathematical formula a _<_ = b. Please match the variables in the given constraint description with the variables in the template to generate the correct mathematical expression. 

Your answer can only be a mathematical expression and do not provide any explanation. 

28 

Table A.12: An example of the prompt for type 9 constraint generation 

You need to formulate the following given problem as a mixed integer programming (MIP) model. But now you just need to define a single constraint of the model. 

Full problem description to give you context: <mark>Haus Toys can make and sell toy trucks, toy aeroplanes, toy ships, and toy trains. The prof</mark> i <mark>t for each truck sold</mark> is <mark>$5, each aeroplane sold</mark> is <mark>$10, each ship sold</mark> is <mark>$8, and each train sold</mark> is <mark>$7. How many</mark> of <mark>each type</mark> of <mark>toys should Haus Toys make</mark> to <mark>maximise the prof</mark> i <mark>t? There are 890 units</mark> of <mark>timber available. The amount</mark> of <mark>timber</mark> r <mark>equired</mark> is 12 <mark>units for each truck,</mark> 20 <mark>units for each aeroplane,</mark> 15 <mark>units for each ship, and</mark> 10 <mark>units for each train. The are 500 units</mark> of <mark>steel available. The amount</mark> of <mark>steel</mark> r <mark>equired</mark> is 3 <mark>units for each aeroplane,</mark> 5 <mark>units for each ship,</mark> 4 <mark>units for each train, and</mark> 6 <mark>units for each truck.</mark> If <mark>Haus Toys makes trucks, then they will not make trains.</mark> If <mark>they make ships, however, they will also make aeroplanes. The number</mark> of <mark>toy ships made cannot</mark> e <mark>xceed the number</mark> of <mark>trains made. Haus Toys must also make</mark> at <mark>least twice</mark> as <mark>many ships</mark> as <mark>aeroplanes.</mark> 

Constraint Description: <mark>The number</mark> of <mark>toy ships made cannot</mark> e <mark>xceed the number</mark> of <mark>trains made.</mark> 

This constraint is a comparison constraint between two variables, expressed in a mathematical formula similar to x _<_ = b*y, where x and y are variables and b is a positive constant. 

Please use the variables <mark>[‘trucks’, ‘aeroplanes’, ‘ships’, ‘trains’]</mark> to model this constraint without making any alterations to the variable names. You do not need to model other constraints or the objective function in the problem. The resulting expression will not necessarily involve all the variables in the variable list provided. Ensure that the variables in the generated expression completely retain their original names from the list. 

Use the symbols “ _>_ =”, “ _<_ =”, and “=” to denote greater than or equal to, less than or equal to, and equal to, respectively. 

Your answer must only be a mathematical expression and do not provide any explanation. 

29 

