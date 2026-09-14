# **TEXT2ZINC: A Cross-Domain Dataset for Modeling Optimization and Satisfaction Problems in MINIZINC** 

**Akash Singirikonda**<sup>1</sup> **, Serdar Kadıo˘glu**<sup>1, 2</sup> **and Karthik Uppuluri**<sup>2</sup> 

1Department of Computer Science, Brown University, Providence, USA 

2Artificial Intelligence Center of Excellence, Fidelity Investments, Boston, USA 

_{_ serdark@cs.brown.edu _}_ 

#### **Abstract** 

There is growing interest in utilizing large language models (LLMs) as co-pilots for combinatorial optimization and constraint programming tasks across various problems. This paper aims to advance this line of research by introducing TEXT2ZINC, a cross-domain dataset for capturing optimization and satisfaction problems specified in natural language text. Our work is distinguished from previous attempts by integrating _both_ satisfaction and optimization problems within a _unified dataset_ using a _solver-agnostic_ modeling language. To achieve this, we leverage MINIZINC’s solver-andparadigm-agnostic modeling capabilities to formulate these problems. Using the TEXT2ZINC dataset, we conduct comprehensive baseline experiments to compare execution and solution accuracy across several methods, including off-theshelf prompting strategies, chain-of-thought reasoning, and a compositional approach. Additionally, we explore the effectiveness of intermediary representations, specifically knowledge graphs. Our findings indicate that LLMs are not yet a push-button technology to model combinatorial problems from text. We hope that TEXT2ZINC serves as a valuable resource for researchers and practitioners to advance the field further. 

## **Introduction** 

Generating constraint models from free-form natural language descriptions remains a significant challenge despite the groundbreaking advances in large language models (LLMs). Similarly, while constraint-solving techniques enjoy tremendous theoretical and practical advances, the cognitive barrier of translating problem descriptions into formal constraint models persists. This barrier is particularly acute, as domain experts who deeply understand their problem domain often lack the specialized knowledge required for formal modeling. The resulting dependency on modeling experts creates operational bottlenecks and can lead to misinterpretation of domain-specific requirements during the translation process. 

High-level modeling languages such as MINIZINC (Nethercote et al. 2007), CPMpy (Guns 2019), and GAMS (Bussieck and Meeraus 2004) have partially addressed these challenges by providing solver-agnostic approaches that are powerful and flexible. These modelling frameworks enable practitioners to focus on describing their problems without worrying about specific solution methods, 

making them especially useful for real-world applications, where requirements often change over time. 

In parallel, LLMs still face significant challenges in handling the mathematical and logical reasoning needed for automated modeling. While language models are powerful at interfacing with natural text, they struggle with the consistency and precision required in declarative approaches, from basic type declarations to complex constraint relations. This gap between understanding textual descriptions and turning them into problem formulations indicates that more work is needed for automated modeling assistants (akin to code copilots). 

## **Our Contributions** 

Our primary contribution is the introduction of TEXT2ZINC<sup>1</sup> , a unified, cross-domain dataset that combines both optimization and satisfaction problems expressed in natural language. The dataset contains a diverse range of problem types across multiple domains, carefully curated from excellent resources including NL4OPT<sup>2</sup> (Ramamonjison et al. 2022a), NLP4LP<sup>3</sup> (AhmadiTeshnizi et al. 2024), ComplexOR<sup>4</sup> (Xiao et al. 2023), CSPLib<sup>5</sup> (Jefferson et al. 1999), and Hakank’s collection<sup>6</sup> (Kjellerstrand 2025). We further enhance these problems through reformulation, metadata enrichment, and curation to ensure consistency and quality. This comprehensive collection provides a robust foundation for evaluating language-to-model translation. 

The remainder of this paper is organized as follows. Section 2 reviews fundamental concepts, including the distinction between optimization and satisfaction problems, an overview of MINIZINC, the role of knowledge graphs in combinatorial modelling, and relevant work utilizing LLMs for optimization. Section 3 presents a detailed description of the TEXT2ZINC dataset. Section 4 outlines our methodology, and Section 5 discusses our results and analysis. Section 6 concludes with discussing our findings and future directions. 

- 1https://huggingface.co/datasets/skadio/text2zinc 

- 2https://github.com/nl4opt/nl4opt-competition 

- 3https://nlp4lp.vercel.app/ 

- 4https://github.com/xzymustbexzy/Chain-of-Experts 

- 5https://github.com/csplib/csplib 

- 6http://www.hakank.org/ampl/ 

## **Background** 

The following section provides background information about optimization and satisfaction problems, MINIZINC as a modeling language, and knowledge graphs as a representation structure. 

### **Optimization vs. Satisfaction Problems** 

Optimization and satisfaction are two essential categories of decision-making problems commonly encountered in operations research, artificial intelligence, and mathematics. Although both require the satisfaction of constraints, their goals and approaches differ 

**Optimization:** Optimization problems aim to find the **best solution** to a given problem by maximizing or minimizing an _objective function_ under a set of constraints. For instance, consider the following problem: 

_“An oil refinery manager has several million barrels of crude oil of different types allocated for production during the coming month. These resources can be used to make multiple different products. Each product has a price at which it sells. There are multiple production processes, each that uses some amount of each type of crude oil and produces some amount of each product. Each process has a cost per barrel of product produced. The crude oil has no separate cost as they have already been allocated. How many times should each process be executed to_ **_maximize_** _the revenue for the next month?”_ 

In this example, the goal is to determine the optimal execution frequencies of the production processes to **maximize revenue** . Optimization problems have typically been solved by mathematical programming methods, which have roots in Linear Programming (LP). In this paradigm, it is common to utilize a reduction to a simpler inequalityconstrained model, such as a linear program, which can be solved with highly developed methods that exploit its special structure (Hooker and van Hoeve 2018). 

**Satisfaction:** Satisfaction problems, in contrast, focus solely on finding a **feasible solution** that satisfies a set of constraints without optimizing a specific objective. A classic example of a satisfaction problem is the following: 

_“Lecture timings need to be scheduled for courses across a limited number of periods. Each course requires a specific number of lectures and can only be assigned to certain periods due to availability constraints. Some courses have conflicts due to having common students and cannot be scheduled simultaneously. Additionally, there is a limited number of rooms that can be used and, thus, a maximum number of lectures that can occur simultaneously. How can we allocate lectures to periods while_ **_ensuring all constraints are met?_** _”_ 

Here, the task is to satisfy the constraints dictated by the requirements to create a valid schedule. Satisfaction problems have typically been solved by methods in constraint programming, which has roots in logic programming. This method is commonly used for both verification and generation. This method often processes constraints independently, using domain reduction and propagation. (Hooker and van Hoeve 2018). 

### **MINIZINC** 

MINIZINC<sup>7</sup> (Nethercote et al. 2007) is a high-level constraint modeling language that supports both discrete and continuous optimization and satisfaction problems. Its solver-agnostic design allows communication with various solver backends. This enables leveraging different problemsolving paradigms, including Constraint Programming (CP), (Mixed) Integer Programming (MIP), and Boolean Satisfiability/Lazy Clause Generation (SAT). This flexibility is achieved through compilation to FLATZINC, an intermediate language that interfaces with different solvers, allowing the same MINIZINC model to be used across multiple backends without any code modifications. This enables end users to write the modeling code once and test different backends that best suit the task at hand. 

A key feature of MINIZINC is its use of global constraints, a concept originating in CP, which significantly simplifies the modeling process. For example, the all ~~d~~ ifferent( _x_ 1 _, ..xn_ ) constraint specifies that variables _x_ 1 _, x_ 2 _, ...xn_ must take distinct values, replacing numerous pairwise inequality constraints that would be required in traditional MIP solvers. These global constraints can be specialized for particular solvers, often leading to improved performance (van Hoeve and Katriel 2006; Nethercote et al. 2007). Listing 1 shows the default expansion of the all ~~d~~ ifferent constraint from MINIZINC to FLATZINC as binary inequalities. If the solver is interfacing with Gecode, it can use Gecode’s native all ~~d~~ ifferent constraint instead. 

% pairwise binary inequalities predicate all_different(array[int] of var float:x) = 

forall(i,j in index_set(x) where i < j)( x[i] != x[j]); 

% built-in global constraint predicate all_different(array[int] of var int:x) = 

- gecode_all_different(x); % native Gecode version for ints 

Listing 1: All different constraint in MiniZinc. 

Global constraints allow end-users to leverage intuitive higher-level declarative constraints rather than focusing on low-level decomposition. 

MINIZINC’s practical utility for real-world applications is further enhanced by its clear separation of models (.mzn files) and instances (.dzn files). Models contain the problem structure, while instances provide specific input data, allowing a single model to be reused across multiple problem instances. The language structure is straightforward, consisting of four main components: decision variables, constraints, parameters, and an objective function for optimization problems or a satisfaction goal. This simple structure allows end users to create modular programs. Additionally, MINIZINC supports automated solution checking and model validation, which help evaluate model correctness during development. 

7https://www.minizinc.org/ 

Given its advanced features, we consider MINIZINC an excellent fit for bridging natural language and solver formulations. We hypothesize that higher-level language constructs, as offered by MINIZINC, serve as a good interface between LLMs and combinatorial formulations. 

### **Knowledge Graphs** 

Knowledge Graphs (KGs) are structured representations of information where entities are represented as nodes and their relationships as edges(Singhal 2012). They have become fundamental tools in various domains, from powering Google’s search engine to organizing scientific literature in academic databases((Singhal 2012), (Bizer et al. 2009), (Suchanek, Kasneci, and Weikum 2008), (Ahrabian et al. 2023)). In these graphs, real-world concepts and their relationships are captured in a format that both humans and machines can process effectively. A knowledge graph is a particularly effective tool for representing information in a structured way, especially for combinatorial problems. 

In our context, parameters, variables, constraints, and objectives are depicted as nodes, interconnected through relationships that describe their interactions. For instance, an objective node is connected to all applicable constraints, highlighting the dependencies within the problem. Generating code for less commonly known languages by large language models such as GPT-4 can be challenging when relying solely on an unstructured problem description and the input data. Instead, utilizing a structured knowledge graph as an intermediate representation can simplify this process. This graph models the problem at an atomic level, illustrating the intricate relationships between various components. This structured representation, mainly when designed to imitate the logical structure of code, facilitates a smoother transition from unstructured problem description to executable code. It is crucial that this representation is “code-inspired” to ensure it closely aligns with the final code structure, minimizing the gap between the model and this representation. We document both a knowledge graph generation prompt and an example knowledge graph in Appendix A2. 

data scarcity was addressed by data augmentation, leveraging CodeT5 to achieve higher accuracy than zero-shot LLM approaches, although still limited to linear programming problems using PuLP (Prasath and Karande 2023). Significant strides were made in training custom LLMs for optimization modeling through their OR-Instruct framework but remained constrained by single-solver dependency (Huang et al. 2024). A notable contribution to evaluation methodologies came from the MAMO benchmark, focusing on LLMs’ mathematical modeling processes rather than solution correctness. In CP, LLMs’ potential in search space optimization has been demonstrated through generating streamliners using MINIZINC (Voboril, Ramaswamy, and Szeider 2024). Natural language to constraint model translation has also been explored through a simple decomposition-based prompting approach with GPT models (Tsouros et al. 2023). Building on this, in-context learning strategies such as Retrieval Augmented Generation (RAG) have been explored to build constraint models in CPMPY (Michailidis, Tsouros, and Guns 2024). Domain-specific applications have also emerged, focusing on supply chain optimization while preserving data privacy (Li et al. 2023) and diagnosing infeasible optimization problems through interactive conversations (Chen, Constante-Flores, and Li 2023). 

Our work, TEXT2ZINC, addresses several key limitations in existing research. First, unlike previous datasets focusing on single problem types, we uniquely integrate both satisfaction and optimization problems spanning continuous and discrete domains. Second, we leverage MINIZINC’s solveragnostic modeling capabilities, moving beyond the solverspecific approaches of previous attempts. Finally, we explore the effectiveness of knowledge graphs as novel, structured, intermediate representations, an aspect unexplored in the existing literature. 

## **TEXT2ZINC** 

The TEXT2ZINC dataset<sup>8</sup> comprises of 110 carefully selected and augmented problem instances from five primary sources that blends optimization and satisfaction problems. 

- NLP4LP (AhmadiTeshnizi et al. 2024) 

## **Related Work** 

A growing interest has been in leveraging large language models for optimization and constraint programming tasks. Early efforts like (Ramamonjison et al. 2022a) focused on linear programming problems using entity recognition and logical forms, achieving promising results with ChatGPT (92.7% accuracy on NL4OPT). Additionally, Holy Grail 2.0 (Tsouros et al. 2023) proposed a blueprint for building conversation modeling assistants. Significant improvements in execution accuracy of LLM generated MINIZINC code were achieved through using in-line annotation of entities in problem descriptions. (Dakle et al. 2023; Kadıo˘glu et al. 2024) Sophisticated approaches emerged with a multiagent Chain-of-Experts framework (Xiao et al. 2023), and LLM-agent, Optimus (AhmadiTeshnizi et al. 2024), which developed a modular system for handling complex problem descriptions. However, these systems remain tied to specific solvers such as Gurobi and Cvxpy. The challenge of 

- ComplexOR (Xiao et al. 2023) 

- LPWP (Ramamonjison et al. 2022a) 

- CSPLib (Jefferson et al. 1999) 

- Hakank’s collection (Kjellerstrand 2025) 

From this larger collection, we carefully curated problems that clearly distinguish between data and parameter components. We standardize the diverse input formats (json, dzn, mzn, html, txt) to our unification format. To serve as supervised labels, we provide ground truth outputs for most problems to enable validation. Each problem instance is enriched with extensive metadata (e.g., domain) to support diverse modeling approaches and future research needs. The dataset spans 11 application domains, as shown in Figure 1. 

In the following, we detail the characteristics of each source and our specific contributions to their respective problems. 

8https://huggingface.co/datasets/skadio/text2zinc 



Figure 1: Distribution of problems across domains. 

- **NLP4LP: 65 Problems** (AhmadiTeshnizi et al. 2024) A collection of 67 LP, MILP, and MIP problems, originally represented in structured natural language. We converted the data from JSON to DZN format via a Python script and refined problem statements for clarity. Where included, we verified our generated code against the objective values provided in the dataset. We include 65 problems from this dataset. 

- **ComplexOR: 7 Problems** (Xiao et al. 2023) A diverse collection of 37 operations research problems sourced from academic papers, textbooks, and industry applications, spanning domains such as supply chain optimization, scheduling, and warehouse logistics. We sampled seven sampled representative problems from this dataset. 

- **LPWP: 5 Problems** (Ramamonjison et al. 2022a) This is a collection 1101 elementary-level linear programming (LP) problems collected from the Nl4Opt Competition (Ramamonjison et al. 2022b). For these problems, we extracted parameters from problem descriptions into data files and modified problem descriptions accordingly. 

- **CSPLib: 11 Problems** (Jefferson et al. 1999) A comprehensive library of 95 test problems for constraint solvers, featuring problems across various domains, including bin-packing, combinatorial mathematics, and scheduling. We included 11 problems from this collection and enhanced their existing MINIZINC solutions with detailed comments. 

- **Hakank’s Collection: 22 Problems** (Kjellerstrand 2025) An extensive collection of over 1000 MINIZINC models spanning combinatorial problems, puzzles, operations research, and global constraints. We extracted problem features and descriptions from the extensively documented model files to standardize 22 problems. 

### **Dataset Format** 

In our unified TEXT2ZINC format, each problem instance is divided into four components: _Input_ , _Data_ , _Model_ , and _Output_ . Detailed explanations of each component is as follows: 

**Input:** A JSON file that encapsulates a comprehensive description of a problem instance. This file is organized into several key sections: 

- **Problem Description:** A standardized natural language problem description of the problem. To maintain abstraction, we avoid including specific parameter names and values, instead incorporating them in the data file. This retains a neutral language when describing the problem. 

- **Parameters:** Additional information about the parameters that are included in the data.dzn file. Each parameter is provided with a natural language explanation of its meaning and format, an associated symbol corresponding to its name in the data.dzn file, and a specification of its shape, which can be either an n-dimensional list or a scalar, represented by an empty list. 

- **Output Specification:** A detailed explanation of the expected output format, including the name and shape of any decision variables to be output. This is required to evaluate satisfaction problems. 

- **Metadata:** Additional contextual information, such as a descriptive problem title, a domain, and subdomain that enrich the problem, an objective (one of satisfy, maximize, or minimize), and a list of automatically generated keywords that reflect the constraints used in the problem, such as all ~~d~~ ifferent and _≤_ . 

- **Unique Identifier:** A key linking the problem instance to its source. 

Figure 2 presents an example input file. 

**Model:** A MZN file containing the MINIZINC model file that formulates the problem and serves as a verifier for satisfaction problems. The model can be used as a verifier by treating the output from the LLM-generated code in DZN format as input to the model. The constraints are decomposed where possible for better clarity. 

Figure 3 shows an example model file. 



<!-- Start of picture text -->
input.json<br>1 {<br>2 "parameters": [<br>3 {<br>4 "definition": "Number of courses",<br>5 "symbol": "courses",<br>6 "shape": []<br>7 },<br>8 {<br>9 "definition": "Number of periods",<br>10 "symbol": "periods",<br>11 "shape": []<br>12 },<br>13 {<br>14 "definition": "Number of rooms available",<br>15 "symbol": "rooms",<br>16 "shape": []<br>17 },<br>18 {<br>19 "definition": "Binary matrix where A[i,j]=1 indicates lectures of course i<br>can be scheduled at period j",<br>20 "symbol": "available",<br>21 "shape": ["courses", "periods"]<br>22 },<br>23 {<br>24 "definition": "Conflict matrix where M[i,j]=1 if courses i and j have<br>common students",<br>25 "symbol": "conflict",<br>26 "shape": ["courses", "courses"]<br>27 },<br>28 {<br>29 "definition": "Array containing the number of lectures required per course<br>",<br>30 "symbol": "requirement",<br>31 "shape": ["courses"]<br>32 }<br>33 ],<br>34 "output": [<br>35 {<br>36 "definition": "Timetable grid where 1 represents a scheduled lecture and 0<br>represents an unscheduled lecture",<br>37 "symbol": "timetable",<br>38 "shape": ["courses", "periods"]<br>39 }<br>40 ],<br>41 "description": "Lecture timings need to be scheduled for courses across a<br>limited number of periods. Each course requires a specific number of<br>lectures and can only be assigned to certain periods due to availability<br>constraints. Some courses have conflicts due to having common students and<br>cannot be scheduled at the same time. Additionally, there is a limited<br>number of rooms that can be used and thus a maximum number of lectures that<br>can occur simultaneously. How can we allocate lectures to periods while<br>ensuring all constraints are met?",<br>42 "identifier": "or_lp_ip_scheduling_problem_2",<br>43 "metadata": {<br>44 "name": "Timetable Problem", "domain": "Scheduling", "objective": "satisfy",<br>"source": "hakank", "constraints": [<br>45 "forall", "<=", "+", "=", "sum"]<br>46 }<br>47 }<br><!-- End of picture text -->

Figure 2: An example input with description, parameters, metadata, and output fields. 

**model.mzn** 

1 include "globals.mzn"; 2 3 % Input parameters 4 int: courses; 5 int: periods; 6 int: rooms; 7 8 array[1..courses, 1..periods] of int: available; 9 array[1..courses, 1..courses] of int: conflict; 10 array[1..courses] of int: requirement; 11 12 % Decision variables 13 array[1..courses, 1..periods] of var 0..1: timetable; 14 15 % Solve 16 solve :: int_search( 17 [timetable[c, p] | c in 1..courses, p in 1..periods], 18 most_constrained, 19 indomain_split, 20 complete 21 ) satisfy; 22 23 % Constraints 24 constraint 25 % 1. Conflicts: Courses with common students must not be scheduled at the same time 26 forall(c1, c2 in 1..courses where c1 < c2) ( 27 if conflict[c1, c2] = 1 then 28 forall(p in 1..periods) ( 29 timetable[c1, p] + timetable[c2, p] <= 1 30 ) 31 else 32 true 33 endif 34 ) 35 % 2. Availabilities: Courses can only be scheduled in available periods 36 /\ 37 forall(c in 1..courses, p in 1..periods) ( 38 if available[c, p] = 0 then 39 timetable[c, p] = 0 40 else 41 true 42 endif 43 ) 44 % 3. Rooms: At most ‘rooms‘ lectures can be scheduled per period 45 /\ 46 forall(p in 1..periods) ( 47 sum([timetable[c, p] | c in 1..courses]) <= rooms 48 ) 49 % 4. Number of lectures per course must match the requirement 50 /\ 51 forall(c in 1..courses) ( 52 sum([timetable[c, p] | p in 1..periods]) = requirement[c] 53 ); 

Figure 3: An example MINIZINC model. 

**data.dzn** 

#### **output.json** 

- 1 int: courses = 5; 2 int: periods = 20; 3 int: rooms = 2; 4 array[1..courses, 1..periods] of int: available = array2d(1..courses, 1..periods, [ 

- 5 % 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 

- 6 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 

- 7 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 

- 8 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 

- 9 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 

- 10 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 

- 11 ]); 12 array[1..courses, 1..courses] of int: conflict = array2d(1..courses, 1.. courses, [ 



<!-- Start of picture text -->
13 % Conflict matrix<br>14 0, 1, 0, 0, 1,<br>15 1, 0, 0, 1, 0,<br>16 0, 0, 0, 0, 1,<br>17 0, 1, 0, 0, 1,<br>18 1, 0, 1, 1, 0<br>19 ]);<br>20 array[1..courses] of int: requirement<br>= [6, 10, 14, 6, 4];<br><!-- End of picture text -->

Figure 4: An example data instance. 

**Data:** A DZN file representing a concrete problem instance. This instance data is used to validate the code generated by the language model in conjunction with the ground truth output labels. Figure 4 shows an example data file. 

**Output:** A JSON file containing the assignments of variables specified in the objective values for a problem. Two essential elements of the output are the final variable configurations (serving as sample solutions for satisfaction problems) and the optimal value (for optimization problems). Figure 5 shows an example output file. 



<!-- Start of picture text -->
1 {<br>2 "timetable": [<br>3 [0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0,<br>1, 0, 1, 0, 0, 0, 0, 0, 0],<br>4 [1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0,<br>0, 1, 0, 1, 1, 1, 1, 1, 1],<br>5 [0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1,<br>1, 0, 1, 1, 1, 1, 0, 1, 1],<br>6 [0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1,<br>0, 0, 0, 0, 0, 0, 0, 0, 0],<br>7 [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,<br>0, 1, 0, 0, 0, 0, 1, 0, 0]<br>8 ]<br>9 }<br><!-- End of picture text -->

Figure 5: An example of output of model execution. 

Table 1 shows the distribution of problem instances modeled with LP, MIP, and CP across datasets. 

### **Dataset Verification** 

Input parameters are validated against DZN files through automated verification. The output files for instances with model files contain the complete MINIZINC model results in JSON format, while instances without models include only the objective value. Model files are provided for all satisfaction problems, and all included models have been verified for successful compilation. 

TEXT2ZINC dataset is actively evolving and expanding with subsequent releases. The initial version includes 45 MINIZINC model files, with plans for additional models in the following updates. All constraint satisfaction problems have been verified to produce valid solutions. 

## **Experimental Methodology** 

Given TEXT2ZINC, we present a methodology for using it to test the performance of state-of-the-art LLMs for automated modeling. Our main goal is to establish reasonable baseline performance to serve as a lower bound for emerging approaches. 

The task of MINIZINC model generation from natural language can be formally defined with the following Formulation and Evaluation. 

### **Dataset Statistics** 

TEXT2ZINC is a cross-domain dataset and the first to encompass optimization and satisfaction problems. 

||# LP|# MIP|# CP|
|---|---|---|---|
|NLP4LP|54|13|0|
|LPWP|1101|0|0|
|ComplexOR|25|12|0|
|TEXT2ZINC|64|31|15|



Table 1: Distribution of Problem Types Across Datasets 

### **Problem Formulation** 

Let _Input_ = ( _description, parameters, output, metadata, data_ ) represent the input specification where: 

- _description_ is the natural language description of the problem 

- _parameters_ = _{p_ 1 _, ..., pn}_ is the set of input parameters where each _pi_ = ( _di, si,_ **h** _i_ ) consists of: 

- _di_ : is the natural language definition of the parameter 

- **–** _si_ : parameter symbol (e.g., ’num ~~w~~ arehouses’, ’num ~~c~~ ustomers’, ’P’) 

- **h** _i_ : is the shape information of the parameter 

- _output_ = _{o_ 1 _, ..., ok}_ is the set of output variables where each _oi_ = ( _di, si,_ **h** _i_ ) consists of: 

- _di_ : is the natural language definition of the output 

- _si_ : output symbol (e.g., ’X’, ’Y’) 

- **h** _i_ : is the shape information of the output 

- _metadata_ : metadata containing problem properties (e.g., domain, objective type, constraint types) 

Let _Data_ be a concrete data instance specified in a format like a .dzn file. The objective is to learn a function _f_ : ( _Input, Data_ ) _→M_ where _M_ represents the space of valid MINIZINC models. Given the input _Input_ and data instance _data_ , the function should generate a data-compatible model and correctly implement the given specifications. 

### **Evaluation** 

Given a dataset of _N_ problems, each with a ground truth model _m_<sup>_∗_</sup> _i_<sup>and generated model</sup><sup>_mi_, we define two key met-</sup> rics: 

1. **Execution Accuracy** ( _Eacc_ ): Measures the proportion of generated models that successfully compile and execute: 



where I( _·_ ) is the indicator function. 

2. **Solution Accuracy** ( _Sacc_ ): Measures the proportion of models that achieve the same objective value as the ground truth: 



where _obj_ ( _·_ ) returns the objective value and _m_<sup>_∗_</sup> _i_<sup>isthe</sup> ground truth model for instance _i_ . 

### **Solution Approaches** 

To explore the effectiveness of different prompting approaches, we conducted experiments on the NLP4LP section of our dataset, comprising 63 optimization problems. Our investigation is organized around three main approaches, each progressively building upon the insights from previous approaches. Based on these approaches, Algorithm 1 presents a high-level architecture flow of our LLM-assisted model generation pipeline. 

**Vanilla Prompting:** Vanilla prompting involves directly providing the task description and input to the language model without any additional instructions about reasoning steps, problem decomposition, or how to approach the solution. 

1. **Basic** : Baseline approach exposing the LLM to: 

   - Problem description 

   - Expected input parameters 

2. **Basic + Data Nomenclature & Examples** : Enhances baseline approach with: 

Algorithm 1: LLM-based MINIZINC Model Generation 

- **Require:** 1: _Input ▷_ Input specification from input.json 2: _Data ▷_ Data instance from data.dzn 3: _LLM ▷_ LLM to prompt 

- 4: **Solution Approaches:** 

- 5: vanilla _←{_ 

- 6: Basic, 

- 7: + Data Nomenclature & examples, 

- 8: + Shape information, 

- 9: + Knowledge Graph information 

- 10: _}_ 11: cot _←{_ 

- 12: CoT + Data Nomenclature, 13: + Examples, 

- 14: + Shape information. 

- 15: _}_ 

- 16: compositional _←{_ 17: Multi-Call + Composition 

18: _}_ 

19: all ~~a~~ pproaches _←_ vanilla _∪_ cot _∪_ compositional 

20: **for** _approach ∈_ all ~~a~~ pproaches **do** 

- 21: prompt _←_ ConstructPrompt( _Input, approach_ ) 22: minizinc ~~c~~ ode _←_ CallLLM( _LLM_ , prompt) 23: SaveToFile(minizinc ~~c~~ ode, _approach_ ) 

24: **end for** 

- 25: **function** CONSTRUCTPROMPT( _Input, approach_ ) 26: **return** SampleRelevantInfo( _Input, approach_ ) _▷_ Sample based on strategy 

27: **end function** 

   - Parameter definitions 

   - Concrete usage examples sampled from the data instance 

3. **Basic + Shape Information** : Further augments with: 

   - Parameter dimensionality information 

4. **Basic + Knowledge Graph** : Further integrates: 

   - Intermediate knowledge representation 

**Chain-of-Thought (CoT) Approaches:** Building upon vanilla prompting, Chain-of-Thought (Wei et al. 2023) prompting adds explicit instructions for the language model to show its reasoning steps, explain its thought process, and documents how it approaches the solution. 

1. **CoT** : incorporates reasoning and data nomenclature 

   - Step-by-step reasoning 

   - Parameter definitions 

2. **CoT + Examples** : Augments with: 

   - Concrete usage examples sampled from dzn 

3. **CoT + Shape Information** : Further augments with: 

   - Parameter dimensionality information 

**Compositional Approach:** Building upon vanilla and Chain-of-Thought prompting, the compositional approach 

breaks down the task into smaller, sequential sub-tasks. These sub-tasks generate the parameters and decision variables, constraints, and an objective function. The output for each sub-task is generated independently, and the results are then combined to form the complete solution. 

1. **Multi-Call + Composition** : Implements: 

   - Decomposition into sequential sub-tasks 

   - Followed by combining results together 

Overall, each solution approach builds upon its predecessors, methodically incorporating additional information and structural elements to improve model generation accuracy. The progression from vanilla approaches to more sophisticated methods allows us to isolate the impact of different prompting elements and identify the most crucial components for successful model generation. We document all our prompts in Appendix A1 for further visibility. 

|**Prompting Method**|**Execution**<br>**Accuracy**|**Solution**<br>**Accuracy**|
|---|---|---|
|Vanilla Prompting|||
|Basic|0.1904|0.0634|
|+ Data & examples|0.3650|0.1904|
|+ Shape|0.1904|0.1269|
|+ Knowledge Graph|0.3492|0.1111|
|Chain-of-Thought (CoT)|||
|CoT with data|0.4285|0.1746|
|+ Examples|**0.5873**|**0.2539**|
|+ Shape|0.5555|0.2063|
|Compositional|||
|Multi-Call + Composition|**0.6031**|0.2222|



### **Experimental Setup** 

Using language models, our experimental setup systematically evaluates different prompting strategies for model generation. As described in the previous section, we implement three solution approaches: vanilla prompting with progressive enhancements from basic to integration with knowledge graphs), Chain-of-Thought variants with increasing contextual information and a compositional approach using multiple sequential tasks and combining their results. We use the model generation pipeline as shown in Algorithm 1. 

We use GPT 4.0 in our experiments on NLP4LP problems from our dataset, which consists of 66 problems. We excluded problems 9, 26, and 27 due to their nature and missing data, resulting in a sample of 63 problems. 

For each input specification _I_ , we generate MINIZINC models using each prompting strategy, where the prompt construction selectively samples relevant information based on the strategy’s requirements. The generated models are then evaluated on two metrics: execution accuracy 1 and solution accuracy 2. 

## **Results and Discussion** 

Table 2 presents our results which are discussed next. In addition, we release a Hugging Face Leaderboard to benchmark approaches on TEXT2ZINC<sup>9</sup> and welcome submissions on new solution approaches. 

### **Vanilla Approaches** 

Our analysis of vanilla prompting approaches reveals several important insights: 

**The current limitations of LLMs:** The basic approach achieves only 19.04% execution accuracy, highlighting that merely exposing the LLM to problem descriptions and parameters is insufficient. The even lower solution accuracy (6.34%) suggests that successfully executed models often fail to capture the underlying modeling logic correctly. 

**The value of data context:** Adding parameter definitions and examples significantly improves both metrics (36.50% 

9https://huggingface.co/spaces/skadio/text2zinc-leaderboard 

Table 2: Experimental results to compare execution and solution accuracy of TEXT2ZINC baseline approaches. 

execution, 19.04% solution), nearly doubling performance. This suggests that LLMs benefit from concrete examples to interpret parameters and their data types better. 

**The necessity of shape information:** Surprisingly, adding shape information degrades performance to baseline levels (19.04% execution). This counter-intuitive result suggests that additional structural information might overwhelm the model or lead to over-specification. 

**Knowledge graph integration:** While the KG maintains improved execution accuracy (34.92%), it leads to poorer solution accuracy (11.11%). This indicates that structured intermediate knowledge representations alone do not necessarily improve the quality of generated solutions. 

### **Chain-of-Thought Approaches** 

The Chain-of-Thought approaches demonstrate a clear progression in capability. 

**Baseline CoT:** Even the baseline CoT with data nomenclature outperforms all vanilla approaches (42.85% execution), suggesting that step-by-step reasoning is fundamental for constraint programming tasks. 

**The effect of examples:** The combination of CoT with examples produces the best solution accuracy (25.39%) and near-best execution accuracy (58.73%), indicating that stepby-step reasoning also benefits from concrete examples. 

**The necessity of shape:** Similar to vanilla approaches, adding shape information to CoT does not improve performance, suggesting an upper limit to beneficial context. 

### **Compositional Approach** 

Breaking down problems into sequential sub-tasks and stitching their outputs together reveals the value of decomposition: 

**Execution vs. Accuracy Trade-off:** Achieving the highest execution accuracy (60.31%), this approach demonstrates that breaking down model generation into sub-tasks improves the likelihood of producing syntactically valid code. Despite best-in-class execution accuracy, solution accuracy (22.22%) falls short of the best CoT approach, suggesting that component integration might introduce optimization inefficiencies, either during individual sub-task generation or via stitching. 

Graphs, reveal that the path from natural language to executable models is not straightforward. While such representations show potential, more research is needed to understand their best utilization. Future work should explore alternative intermediate representations, including named entities, semantic graphs, and agentic frameworks, which might better capture the nuances of formulating combinatorial problems. 

## **References** 

When considering general observations across all approaches, the following patterns emerge: 

**Execution-Solution gap:** Consistently lower solution accuracies (typically 30-50% of execution accuracies) across different strategies suggest how complex the problem of generating accurate code is. In many cases, we noticed that LLMs occasionally misinterpret constraint optimization problems as satisfiability problems. This fundamental misclassification suggests gaps in LLMs’ exposure to fundamental combinatorial concepts. 

**Execution issues:** In our observation, syntax errors are the primary cause of execution failures. This can be attributed to the LLM’s limited training on MINIZINC’s specialized syntax and constraints, which differ significantly from widelyused programming languages such as Python. Appendix A3 documents a detailed breakdown of these errors for reference. 

**Information sweet spot:** Both too little (basic vanilla) and too much (adding shape details) information can be detrimental to performance, suggesting a balanced approach for in-context information. 

**Reasoning vs. Structure:** The superior performance of CoT and compositional approaches can indicate that how information is processed matters more than the quantity of information provided. 

## **Conclusion** 

In this paper, we contribute TEXT2ZINC, a cross-domain Dataset for modeling optimization and satisfaction problems in MINIZINC. We go beyond the previous attempts by integrating _both_ satisfaction and optimization problems within a _unified dataset_ using a _solver-agnostic_ modeling language. Our initial findings suggest that LLMs are not yet a plug-and-play solution for combinatorial modeling despite their impressive capabilities in various domains. The consistently low solution accuracy rates across different prompting strategies highlight the inherent challenges in translating natural language specifications into executable MINIZINC models. Nevertheless, the improved performance achieved through Chain-of-Thought reasoning and compositional approaches offers promising directions. 

We emphasize that advancing modeling co-pilots heavily depends on large-scale, high-quality datasets. We are grateful to the efforts of previous work that inspired and help shape TEXT2ZINC. We encourage the research community to contribute to this and similar efforts. Our experiments with intermediate representations, particularly Knowledge 

AhmadiTeshnizi, A.; Gao, W.; Brunborg, H.; Talaei, S.; and Udell, M. 2024. OptiMUS-0.3: Using Large Language Models to Model and Solve Optimization Problems at Scale. arXiv:2407.19633. 

Ahrabian, K.; Du, X.; Myloth, R. D.; Ananthan, A. B. S.; and Pujara, J. 2023. PubGraph: A Large-Scale Scientific Knowledge Graph. arXiv:2302.02231. 

Bizer, C.; Lehmann, J.; Kobilarov, G.; Auer, S.; Becker, C.; Cyganiak, R.; and Hellmann, S. 2009. DBpedia - A crystallization point for the Web of Data. _Journal of Web Semantics_ , 7(3): 154–165. The Web of Data. 

Bussieck, M. R.; and Meeraus, A. 2004. _General Algebraic Modeling System (GAMS)_ , 137–157. Boston, MA: Springer US. ISBN 978-1-4613-0215-5. 

Chen, H.; Constante-Flores, G. E.; and Li, C. 2023. Diagnosing Infeasible Optimization Problems Using Large Language Models. arXiv:2308.12923. 

Dakle, P. P.; Kadıo˘glu, S.; Uppuluri, K.; Politi, R.; Raghavan, P.; Rallabandi, S.; and Srinivasamurthy, R. 2023. Ner4opt: Named entity recognition for optimization modelling from natural language. In _International Conference on Integration of Constraint Programming, Artificial Intelligence, and Operations Research_ , 299–319. Springer. 

Guns, T. 2019. Increasing modeling language convenience with a universal n-dimensional array, CPpy as pythonembedded example. In _Proceedings of the 18th workshop on Constraint Modelling and Reformulation at CP (Modref 2019)_ , volume 19. 

Hooker, J.; and van Hoeve, W.-J. 2018. Constraint programming and operations research. _Constraints_ , 23. 

Huang, C.; Tang, Z.; Ge, D.; Hu, S.; Jiang, R.; Wang, B.; Wang, Z.; and Zheng, X. 2024. ORLM: A Customizable Framework in Training Large Models for Automated Optimization Modeling. arXiv:2405.17743. 

Jefferson, C.; Miguel, I.; Hnich, B.; Walsh, T.; and Gent, I. P. 1999. CSPLib: A problem library for constraints. Kadıo˘glu, S.; Pravin Dakle, P.; Uppuluri, K.; Politi, R.; Raghavan, P.; Rallabandi, S.; and Srinivasamurthy, R. 2024. Ner4Opt: named entity recognition for optimization modelling from natural language. _Constraints_ , 1–39. 

Kjellerstrand, H. 2025. Hakank’s Page. https://github. com/hakank/hakank. GitHub repository, Retrieved February 13th, 2025. 

Li, B.; Mellou, K.; Zhang, B.; Pathuri, J.; and Menache, I. 2023. Large Language Models for Supply Chain Optimization. arXiv:2307.03875. 

Michailidis, K.; Tsouros, D.; and Guns, T. 2024. Constraint Modelling with LLMs Using In-Context Learning. In Shaw, P., ed., _30th International Conference on Principles and Practice of Constraint Programming (CP 2024)_ , volume 307 of _Leibniz International Proceedings in Informatics (LIPIcs)_ , 20:1–20:27. Dagstuhl, Germany: Schloss Dagstuhl – Leibniz-Zentrum f¨ur Informatik. ISBN 978-395977-336-2. 

Nethercote, N.; Stuckey, P. J.; Becket, R.; Brand, S.; Duck, G. J.; and Tack, G. 2007. MiniZinc: Towards a Standard CP Modelling Language. In Bessi`ere, C., ed., _Principles and Practice of Constraint Programming – CP 2007_ , 529–543. Berlin, Heidelberg: Springer Berlin Heidelberg. ISBN 9783-540-74970-7. 

Prasath, G.; and Karande, S. 2023. Synthesis of Mathematical programs from Natural Language Specifications. arXiv:2304.03287. 

Ramamonjison, R.; Li, H.; Yu, T. T.; He, S.; Rengan, V.; Banitalebi-Dehkordi, A.; Zhou, Z.; and Zhang, Y. 2022a. Augmenting Operations Research with Auto-Formulation of Optimization Models from Problem Descriptions. 

Ramamonjison, R.; Yu, T.; Li, R.; Li, H.; Carenini, G.; Ghaddar, B.; He, S.; Mostajabdaveh, M.; BanitalebiDehkordi, A.; Zhou, Z.; and Zhang, Y. 2022b. NL4Opt Competition: Formulating Optimization Problems Based on Their Natural Language Descriptions. In Ciccone, M.; Stolovitzky, G.; and Albrecht, J., eds., _Proceedings of the NeurIPS 2022 Competitions Track_ , volume 220 of _Proceedings of Machine Learning Research_ , 189–203. PMLR. Singhal, A. 2012. Introducing the Knowledge Graph: Things, not strings. https://www.blog.google/products/ search/introducing-knowledge-graph-things-not/. Google Blog. 

Suchanek, F. M.; Kasneci, G.; and Weikum, G. 2008. YAGO: A Large Ontology from Wikipedia and WordNet. _Journal of Web Semantics_ , 6(3): 203–217. World Wide Web Conference 2007Semantic Web Track. 

Tsouros, D.; Verhaeghe, H.; Kadioglu, S.; and Guns, T. 2023. Holy Grail 2.0: From Natural Language to Constraint Models. _arXiv preprint arXiv:2308.01589_ . 

van Hoeve, W.-J.; and Katriel, I. 2006. _Global constraints_ . ”Elsevier”. 

Voboril, F.; Ramaswamy, V. P.; and Szeider, S. 2024. Realtime Generation of Streamliners with Large Language Models. arXiv:2408.10268. 

Wei, J.; Wang, X.; Schuurmans, D.; Bosma, M.; Ichter, B.; Xia, F.; Chi, E.; Le, Q.; and Zhou, D. 2023. Chain-ofThought Prompting Elicits Reasoning in Large Language Models. arXiv:2201.11903. 

Xiao, Z.; Zhang, D.; Wu, Y.; Xu, L.; Wang, Y. J.; Han, X.; Fu, X.; Zhong, T.; Zeng, J.; Song, M.; et al. 2023. Chain-of-Experts: When LLMs Meet Complex Operations Research Problems. In _The Twelfth International Conference on Learning Representations_ . 

## **A1 Appendix - GPT-4 MiniZinc Code Generation Prompts** 

We present the details of the prompts used in our experiments below. 

### **A1.1 Vanilla Prompting Approach** 

#### **A1.1.1 PURE VANILLA** 

You are an expert MiniZinc developer. 

Generate Minizinc code from a given problem description with additional information about the parameters provided. 

The MiniZinc code should assume that the data needed, will be provided in a specific format through a .dzn file, so the generated code should assume the same names defined in the **input data nomenclature** . 

Please do not generate any other token, except the MiniZinc code. 

#### **Problem Description** : 

_{_ problem description _}_ 

**Input Data Nomenclature** : _{_ data ~~n~~ omenclature _}_ 

#### **A1.1.2 VANILLA + DATA NOMENCLATURE + EXAMPLES** 

You are an expert MiniZinc developer. 

Generate Minizinc code from a given problem description with additional information about the parameters provided. 

The MiniZinc code should assume that the data needed, will be provided in a specific format through a .dzn file, so the generated code should assume the same names/data-types defined in the **input data nomenclature and examples** . 

Please do not generate any other token, except the MiniZinc code. 

**Problem Description** : _{_ problem description _}_ 

**Input Data Nomenclature and Examples** : _{_ data ~~n~~ omenclature _}_ 

#### **A1.1.3 VANILLA + DATA NOMENCLATURE + EXAMPLES + KG GRAPH** 

You are an expert MiniZinc developer. 

Generate Minizinc code from using the following information: 

1. Problem Description: A formal description describing the optimization problem. 

2. Knowledge Graph: Detailing Parameters, Variables, Constraints and Objective. 

3. Input Data Nomenclature: The MiniZinc code should assume that the data needed, will be provided in a specific format through a .dzn file, so the generated code should assume the same names defined in the **input data nomenclature** . 

Please do not generate any other token, except the MiniZinc code. 

#### **Problem Description** : 

_{_ problem description _}_ 

**Knowledge Graph** : “‘ 

_{_ knowledge graph _}_ “‘ 

**Input Data Nomenclature** : _{_ data ~~n~~ omenclature _}_ 

### **A1.2 Chain-of-Thought (CoT) Approach** 

**A1.2.1 CHAIN-OF-THOUGHT (COT) + DATA NOMENCLATURE + EXAMPLES** 

You are an expert MiniZinc developer. 

Generate Minizinc code from a given problem description with additional information about the parameters provided. 

The MiniZinc code should assume that the data needed, will be provided in a specific format through a .dzn file, so the generated code should assume the same names, shapes and data-types defined in the **input data nomenclature and examples** . 

When generating the code, follow this format: 

“‘ 

- % Parameters 

#### % Variables 

- % Constraints 

#### % Objective 

“‘ 

Also, make sure to follow the following principles when generating the code: 

#### **General Principles** : 

1. The generated code should assume that data will be provided via a ”.dzn” file. Do not declare values directly from the input data nomenclature and examples within the MiniZinc model. 

2. Adhere to the input data nomenclature and examples precisely when declaring input parameter names and their data types. 

3. Use bounded variables whenever possible. If bounds are explicit (e.g., non-negative), include them as constraints. 

4. When defining arrays of variables, ensure bounds are integers. Apply element-wise constraints in a separate constraint block if bounds depend on array elements. 

5. When defining arrays of variables, ensure bounding constraints are applied separately rather than during initialization to avoid type mismatches. 

6. Define explicit bounds for all variables used in linear expressions, either in their declaration or through additional constraints. 

7. Separate constraints into distinct constraint blocks whenever possible. 

8. Use direct and succinct definitions for constraints in the model. 

9. Utilize global constraints as much as possible. 

10. Declare all parameters and sets before using them in other declarations to avoid circular dependencies and ordering issues. 11. When using iteration constructs like ‘forall‘, define the range or set being iterated over properly (e.g., use ‘1..M‘ instead of ‘M‘ for iteration). 

12. Ensure operands in operations are of compatible types to prevent coercion errors. 

13. Declare all identifiers (such as indices or ranges like ‘n‘) before using them in any array or parameter declarations. 

14. Ensure type consistency in expressions to avoid coercion errors. Explicitly cast types if necessary. 

15. Ensure there is only one objective, which will be a maximization, minimization, or a satisfy problem. Do not forget the ‘solve‘ keyword. 

Please do not generate any other token, except the MiniZinc code. 

#### **Problem Description** : 

_{_ problem description _}_ 

**Input Data Nomenclature and Examples** : 

_{_ data ~~n~~ omenclature _}_ 

### **A1.3 Compositional Approach** 

#### **A1.3.1 MULTI CALL PROMPT + COMPOSITION** 

#### **A1.3.2 Parameters and Variables** 

You are an expert MiniZinc developer. 

Generate MiniZinc code for the Parameters and Variables from a given problem description with additional information about input data provided. 

The MiniZinc code should assume that the data needed will be provided in a specific format through a .dzn file, so the generated code should assume the same names/data-types defined in the **input data nomenclature and examples** . 

When generating the code, follow this format: 

“‘minizinc 

% Parameters 

#### % Variables 

“‘ 

Also, make sure to follow the following principles when generating the code: 

#### **General Principles** : 

1. The generated code should assume that data will be provided via a ”.dzn” file. Do not declare values directly from the input data nomenclature and examples within the MiniZinc model. 

2. Adhere to the input data nomenclature and examples precisely when declaring input parameter names and their data types. 

3. Use bounded variables whenever possible. If bounds are explicit (e.g., non-negative), include them as constraints. 

4. When defining arrays of variables, ensure bounds are integers. Apply element-wise constraints in a separate constraint block if bounds depend on array elements. 

5. When defining arrays of variables, ensure bounding constraints are applied separately rather than during initialization to avoid type mismatches. 

6. Define explicit bounds for all variables used in linear expressions, either in their declaration or through additional constraints. 

7. Declare all parameters and sets before using them in other declarations to avoid circular dependencies and ordering issues. 

8. Declare all identifiers (such as indices or ranges like ‘n‘) before using them in any array or parameter declarations. 

9. Ensure that all indices and sets used in parameter and variable declarations are declared beforehand. 

10. When declaring variables, ensure they are appropriately typed (e.g., ‘int‘, ‘float‘). 

11. Variables should have meaningful names related to the problem description. 

12. Include comments to briefly describe each parameter and variable for clarity. 

#### **Problem Description** : 

#### _{_ problem description _}_ 

**Input Data Nomenclature and Examples** : 

_{_ data ~~n~~ omenclature _}_ 

#### **A1.3.3 Constraints** 

You are an expert MiniZinc developer. 

Generate MiniZinc code for the Constraints from a given problem description with additional information about the parameters provided. 

Given the Parameters and Variables part of the code, generate only the constraints. 

When generating the code, follow this format: 

“‘minizinc 

- % Constraints 

“‘ 

Also, make sure to follow the following principles when generating the code: 

#### **General Principles** : 

1. Separate constraints into distinct constraint blocks whenever possible. 

2. Utilize global constraints as much as possible. 

3. When using iteration constructs like ‘forall‘, define the range or set being iterated over properly (e.g., use ‘1..M‘ instead of ‘M‘ for iteration). 

4. Ensure operands in operations are of compatible types to prevent coercion errors. 

5. Ensure type consistency in expressions to avoid coercion errors. 

6. Clearly comment on the purpose of each constraint for clarity and maintenance. 

7. Avoid hardcoding values; use parameters and variables instead. 

8. Use meaningful names for all constraint blocks. 

9. Only generate constraints and do not generate objective. 

#### **Problem Description** : 

_{_ problem description _}_ 

**Input Data Nomenclature and Examples** : 

_{_ data ~~n~~ omenclature _}_ 

**Parameters and Variables** : 

“‘minizinc _{_ parameters ~~a~~ nd ~~v~~ ariables _}_ 

“‘ 

#### **A1.3.4 Objective** 

You are an expert MiniZinc developer. 

Generate MiniZinc code for the Objective from a given problem description with additional information about the parameters, variables and constraints provided. 

Given the Parameters, Variables, and Constraints sections of the code, generate only the objective. 

When generating the code, follow this format: 

“‘minizinc % Objective 

“‘ 

Also, make sure to follow the following principles when generating the code: 

#### **General Principles** : 

1. Ensure there is only one objective, which will be a maximization, minimization, or a satisfy problem. Do not forget the ‘solve‘ keyword. 

2. Ensure the objective function aligns with the problem description. 

3. Verify the correct usage of variables, parameters and constraints in the objective function. 

#### **Problem Description** : 

_{_ problem description _}_ 

**Input Data Nomenclature and Examples** : 

_{_ data ~~n~~ omenclature _}_ 

#### **Parameters and Variables** : 

“‘minizinc _{_ parameters ~~a~~ nd ~~v~~ ariables _}_ “‘ 

**Constraints** : “‘minizinc _{_ constraints _}_ 

“‘ 

#### **A1.3.5 Stitch** 

You are an expert MiniZinc developer. 

Given the Parameters, Variables, Constraints, and Objective sections of the code, stitch them into a complete solution for the optimization problem. 

When stitching the code, follow this format: 

“‘minizinc 

% Parameters 

#### % Variables 

- % Constraints 

% Objective 

“‘ 

Ensure the following principles for syntactic accuracy and logical consistency: 

#### **General Principles** : 

1. Verify that all intermediate sections (parameters, variables, constraints, objective) are consistent and correctly referenced. 

2. Confirm that the final MiniZinc code is syntactically accurate and logically coherent. 

3. Ensure that the code sections are properly integrated, maintaining the prescribed format. 

4. Check for and resolve any circular dependencies or ordering issues in declarations. 

5. Check for and resolve any coercion issues. 

5. Validate type consistency across all expressions and declarations. 

6. Utilize clear and concise comments to describe each section and its components. 

7. Make sure global constraints are utilized where applicable to enhance model efficiency. 

8. Ensure only one objective is defined, using the ‘solve‘ keyword appropriately. 

#### **Problem Description** : 

_{_ problem description _}_ 

#### **Input Data Nomenclature and Examples** : 

_{_ data ~~n~~ omenclature _}_ 

#### **Parameters and Variables** : 

“‘minizinc _{_ parameters ~~a~~ nd ~~v~~ ariables _}_ 

“‘ 

#### **Constraints** : 

“‘minizinc _{_ constraints _}_ 

“‘ 

#### **Objective** : 

“‘minizinc _{_ objective _}_ “‘ 

## **A2 KNOWLEDGE GRAPH GENERATION PROMPT** 

Given an optimization problem description and the nomenclature to be used for parameters. 

Please generate a knowledge-graph. 

**Problem Description** : 

_{_ problem description _}_ 

**Input Data Nomenclature** : 

_{_ data ~~n~~ omenclature _}_ 

**Steps to Generate a Knowledge Graph (KG)** : 

#### 1. **Identify Parameters** : 

- Extract each parameter individually, specifying its type and name. 

- Ensure that parameter names are aligned with the predefined nomenclature. 

- Record any explicit bounds for parameters, if specified. 

- Validate against the problem description to ensure that all relevant parameters are included, checking for any implicitly stated ones. 

2. **Identify Variables** : 

- Identify each variable, noting their types and names. 

- Align variable names with the nomenclature provided, ensuring consistency. 

- Determine and document any bounds (explicit or inferred) for the variables. 

- Cross-verify with the problem description to confirm all necessary variables are accounted for, including those not explicitly mentioned in the nomenclature. 

3. **Identify Constraints** : 

- Detail each constraint separately, recording its description, formula, and associated variables. 

- Classify constraints based on their nature (e.g., linear, nonlinear, global etc..). 

- Highlight if any constraints are global, impacting multiple variables or conditions across the model. 

4. **Identify Objective** : 

- Clearly define the objective function, including its description, mathematical representation, and the variables it affects. 

- Note the type of optimization (minimization, maximization, satisfy) and any relevant constraints tied to the objective. 

- Ensure the objective aligns with the overall goal of the optimization problem as described. 

5. **Generate Turtle (TTL) Representation** : 

- Construct the Turtle format representation using the gathered information on parameters, variables, constraints, and the 

- objective. 

- Sequentially organize the definitions of parameters, variables, constraints, and the objective within the Turtle file. 

- Avoid generalizing the problem statement; focus on defining each component distinctly as outlined in the steps. 

Please do not generate any other token other than the knowledge graph itself. No titles, description or markup necessary. 

### **A2.1 Example Knowledge Graph** 

#### **Unstructured Description** 

A firm produces different goods using different raw materials. The firm has a limited amount of each raw material available. Each good requires a specific amount of raw materials to be produced. Each good results in an amount of revenue produced per unit. How much of each good should the firm produce to maximize its total revenue? 

#### **Knowledge Graph** 

Listing 2: Knowledge Graph in TTL format 

1 @prefix : <\protect\vrule width0pt\protect\href{http://example.org/firm_optimization _#}{ http://example.org/firm_optimization#}> ._ 

- 2 3 _# Parameters_ 4 5 :M **a** :Parameter ; 6 :name "Number of different goods" ; 7 :type "Integer" ; 8 :description "Total number of different goods produced by the firm" . 9 

- 10 :N **a** :Parameter ; 11 :name "Number of different raw materials" ; 12 :type "Integer" ; 13 :description "Total number of different raw materials used by the firm" . 14 15 :Available **a** :Parameter ; 16 :name "Available amount of raw material i" ; 17 :type "1-D Array" ; 18 :description "Amount of each raw material available for production" . 19 20 :Requirements **a** :Parameter ; 21 :name "Requirement of raw material i to produce one unit of good j" ; 22 :type "2-D Array" ; 23 :description "Amount of each raw material required to produce one unit of each good" . 24 25 :Prices **a** :Parameter ; 26 :name "Revenue from selling one unit of good j" ; 27 :type "1-D Array" ; 28 :description "Revenue earned by selling one unit of each good" . 29 30 _# Variables_ 

- 31 32 :UnitsProduced **a** :Variable ; 33 :name "Units produced of good j" ; 34 :type "1-D Array" ; 35 :bounds "0 to infinity" ; 36 :description "Number of units of each good produced" . 

- 37 38 _# Constraints_ 39 40 :MaterialAvailability **a** :Constraint ; 41 :description "Each good’s production must not exceed available raw materials" ; 42 :formula "Sum(Requirements[i][j] * UnitsProduced[j] for j in 1..M) <= Available[i] for i in 1..N" . 

- 43 44 _# Objective_ 

45 46 :MaximizeRevenue **a** :Objective ; 47 :description "Maximize the total revenue from selling the goods" ; 48 :formula "Sum(Prices[j] * UnitsProduced[j] for j in 1..M)" ; 49 :type "Maximization" . 

## **A3 Error Analysis** 

|**Error Type**|**Commentary**|
|---|---|
|Syntax Errors|These errors indicate issues with the MiniZinc code syntax. They<br>may include unexpected tokens, missing semicolons, or incorrect use<br>of language constructs. For example: ‘Error: syntax error,<br>unexpected ’|’’.|
|Type Coercion Errors|These errors happen when there is a mismatch between expected and<br>provided data types, such as expecting an integer but receiving a<br>float. Example: ‘Error: type error: cannot determine<br>coercion from type var float to type var int’.|
|Undefined Identifiers|These errors are due to the use of variables or identifiers that have<br>not been declared or are out of scope. Example: ‘Error: type<br>error: undefined identifier ‘i’, did you mean<br>‘A’?’.|
|Array and Indexing Issues|Errors related to improper use of arrays or indexing problems.<br>This can include out-of-bounds errors or incorrect array dimen-<br>sions.<br>Example:<br>‘Error: evaluation error: Index<br>set mismatch. Declared index sets of ‘Benefit’<br>are [1..5,1..3], but is assigned to array with<br>index sets [1..5, 1..2]’.|
|Constraint Definition Errors|These errors occur when there is an issue with the constraints de-<br>fined in the model. This can include logical inconsistencies or incorrect<br>use of constraint functions. Example:‘Error: solver backend<br>cannot handle constraint: float<br>~~l~~in<br>~~n~~e’.|
|Model Instantiation Errors|Errors related to the instantiation of the model, such as problems<br>with set definitions or parameter initialization. Example: ‘Error:<br>type error: generator expression must be (par<br>or var) set of int or array, but is ‘int’.|
|Missing Data in DZN Files|These errors occur when the necessary data is not provided in the DZN<br>files. This may lead to missing parameters or sets that are required<br>by the model. Example: ‘Error: type error: variable<br>‘K’ must be defined (did you forget to specify<br>a data file?)’.|



Table 3: Categorization of MiniZinc Errors with Commentary. 

