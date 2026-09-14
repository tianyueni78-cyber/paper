# **Abstract Operations Research Modeling Using Natural Language Inputs** 

Junxuan Li<sup>1</sup><sup>_⋆_</sup> , Ryan Wickman<sup>1</sup> , Sahil Bhatnagar<sup>1</sup> , Raj Kumar Maity<sup>1</sup> , and Arko Mukherjee<sup>1</sup> 

Microsoft, Redmond, WA 98052 USA _{_ `junxuanli,sabhatn,ramaity,ryanwickman, arko.mukherjee` _}_ `@microsoft.com` 

**Abstract.** Operations research (OR) uses mathematical models to enhance decision-making, but developing these models requires expert knowledge and can be time-consuming. Automated mathematical programming (AMP) has emerged to simplify this process, but existing systems have limitations. This paper introduces a novel methodology that uses recent advances in Large Language Model (LLM) to create and edit OR solutions from non-expert user queries expressed using Natural Language. This reduces the need for domain expertise and the time to formulate a problem. The paper presents an end-to-end pipeline, named NL2OR, that generates solutions to OR problems from natural language input, and shares experimental results on several important OR problems. 

**Keywords:** Operations Research · Automated Mathematical Programming · Large Language Model. 

## **1 Introduction** 

Operations research (OR) is a field that has been widely used to enhance decisionmaking by creating and using mathematical models of real-world situations to find solutions [11]. A major stream of OR solution is to use mathematical programs (MP) which consist mathematical representations of decision variables, optimization objectives, and decision constraints. For instance, in the area of e-commerce order fulfillment, a resource allocation MP aims to minimize total fulfillment cost, utilizing limited inventories located across the merchant’s warehouse/retailing network. The feasible fulfillment decisions are required to satisfy operational constraints, e.g. channel restrictions, region restrictions, logistic restrictions, and etc.. Another OR problem example, in the area of resource scheduling optimization, a scheduling planner aims to optimize the utilization of human agent resources to accomplish tasks with skill set specifications. The feasible scheduling decisions are required to satisfy operational constraints, e.g. staffing requirements, shift scheduling, skill matching and etc.. For physical tasks, the scheduling planner will also need to minimize agent traveling, and making sure agent traveling schedules satisfy time windows for both task reservations 

> _⋆_ Corresponding author 

2 Li, Wickman, Bhatnagar, Maity and Mukherjee 

and agent shifts. In both examples, the MP aims to optimize a certain objective function, subject to a set of operational constraints. 

However, in the related industries, modeling an OR problem and developing an MP solution will require specialized knowledge set (e.g. mathematical modeling and operations research algorithm design training). For instance, in the e-commerce order fulfillment example, one needs to have knowledge in inventory optimization, transportation optimization, and logistics optimization. Therefore, the development of MP solutions is often left to a small group of domain experts. Moreover, developing and deploying a computer-based solution may take months. This long development cycle can be a barrier to OR solution adoption, especially in the context of small and medium-sized enterprises. 

To overcome this barrier, the field of automated mathematical programming (AMP) has emerged, aiming to automate the process of developing MP solutions. AMP aims to enable non-experts to develop and deploy MP solutions with little or no human intervention. AMP systems can be divided into two categories: _closed-box_ and _open-box_ systems. 

_Closed-box_ AMP systems use machine learning techniques to learn the mapping between the input data and the optimal solution [31,13]. These systems require no prior knowledge of the mathematical structures. However, the solutions produced by black-box systems are often sub-optimal and cannot be guaranteed to satisfy operational constraints. 

_Open-box_ AMP systems, on the other hand, are based on mathematical programming techniques and require the user to specify the mathematical model of the problem [12,15,28]. These systems start from detailed business logic and a problem data set, and generate a solver-specific script (also known as a concrete model) for user to review. After the generated model being reviewed and validated, it is able to guarantee that the solution satisfies the operational constraints, and can _often_ produce optimal solutions. However, the user needs to have a good understanding of the mathematical programming problem and how to interface with a variety of solvers/libraries (e.g. Gurobi, CPLEX, ORtools, AMPL). 

To mitigate the limitations these drawbacks of existing closed- and open-box AMP systems, we propose a novel methodology that create new OR solutions and edit existing OR solutions using natural language (NL) queries. Recent advances in natural language processing (NLP) have led to the development of large language models (LLMs) that can be used for human language text generation. These models have been used for various tasks, such as language translation, question answering, and text summarization [8,33,7,6,2,20]. We propose to use LLMs to generate markup language passages for OR problems, which can then be converted into programming language passages. This technique entails obtaining user input for an OR problem, formulating an NL prompt grounded in the user input, generating a domain-specific language (DSL) that captures the OR problem, transforming the DSL into an executable script (with a suitable solver triaging), and producing a solution by executing the script. Our proposed method can significantly reduce the time and effort required to model and solve 

NL2OR 3 

complex OR problems, which 1) reduces the time required to formulate a problem in a solver-specific format, and 2) provides a framework for the development of an interactive OR problem-solving tool that can be used by non-experts. 

We would like to emphasize that instead of providing any specific OR solution, we present a system that can create an abstract model from a user query and generate a concrete model together with the user data and subsequently, solve the OR problem. For example in a real life scenario, a non-expert user can open a data file ( for example an Excel sheet or google sheet) and invoke(call) the system with query to solve OR problems and do ”what-if” analysis. In our solution methodology, we focus on creating an abstract model grounded on a problem class instead of concrete model based on a problem instance (the problem class together with the data for a problem instance). In our methodology, the creation of an ‘abstract model’ allows users to (1) perform ‘what-if’ analysis using natural language queries, (2) deploy a problem class to support a wide spectrum of tenants with different data instances. Users can later input data to generate a ‘concrete model’ that any solver can handle. Initially, users only need access to a simple data file to create an abstract model, which they can modify to better fit different scenarios. Hence this system can be used to build out of box systems that can work with a non-technical user who wants to bring the power of AI and OR solvers to their data. 

### **1.1 Contributions and Organization** 

Our paper distinguishes itself from existing work on the intersection of natural language processing and automated mathematical programming in the following ways: 

1. We are, to the best of our knowledge, the first to propose a out of the box multi-turn chat system that can generate abstract OR models from user query and then combine that with user data to generate and solve concrete OR models. Further our solution is not tied to any particular OR solver. Our approach empowers LLMs to create and edit an abstraction of a class of OR models, such as order fulfillment models. This abstraction is particularly important for industrial solution providers, as it enables them to work with the model abstraction class instead of having to work with each individual concrete OR models. 

2. We are also the first to handle automatic solver triage. In an OR problemsolving cycle, selecting a proper solver is as important as building a mathematical program. All existing MP interfaces require developers to manually decide which solver to choose, while our approach handles solver triage through a solver interface unification. This innovation streamlines the problemsolving process and saves time for developers. 

We have implemented the proposed methodology as an end-to-end pipeline, named Natural Language to Operations Research _NL2OR_ , that can 1) take natural language input and generate an abstract OR model; 2) resolve data 

4 Li, Wickman, Bhatnagar, Maity and Mukherjee 

mapping and triage solvers to provide a solution to the generated OR problem; 3) edit the generated OR model for what-if analysis. 

In this paper, we describe the details of our proposed method, implementation details and present experimental results on several OR problems. The rest of this paper is organized as follows. Section 2 provides an overview of related work. Section 3 describes our proposed method in detail. Section 4 presents experimental results on several OR problems. Finally, Section 5 concludes the paper and provides directions for future work. 

## **2 Related Works** 

### **2.1 Large Language Models** 

A large language model (LLM) [34] is a sequence-to-sequence model designed for predicting sequences of text-based tokens. This model has undergone training on a substantial volume of text data to enhance its ability to generate accurate predictions for sequences of tokens in a given context. In recent years, the Transformer architecture [22] has revolutionized the field by encouraging efficient parallelization of training and scalability. There have been many foundational LLM models such as BERT [8], OPT [33], PaLM [7], GPT-3 [6], GPT-4 [2], LLaMA [20], Gemini [19], and many more. 

_Prompt engineering_ is a vital step in generating quality responses from a language model. A popular approach is to perform _in-context learning_ [6,25,5], which is an emergent ability of LLMs where it can perform complex tasks by conditioning it on a description of the problem and few-shot examples. There are many approaches that have been shown to dramatically increase the model inference accuracy such as Chain of Thought (CoT) [26], Self-consistency with CoT (CoT-SC) [23], Tree of Thoughts (ToT) [29], Self-consistency [24], ReAct [30] , Progressive Hint Prompting [35] and Graph of Thoughts (GoT) [4]. 

### **2.2 Automated Mathematical Programming** 

An automated mathematical programming (AMP) system aims to automate the process of developing MP solutions with little of no human intervention. The first research stream of AMP focuses on developing an inference system to derive solutions based on historical data. [31] surveys ML-enhanced approaches that solve mix-integer programming and combinatorial optimizations. For example, researchers have found a close-box system using neural network approximations significantly improves the efficiency of modeling and solving the class of SCIP problems in the OR space. The other stream of AMP research considers the formulation of the MP problem to be articulated in natural language and subsequently translated into MP solutions utilizing LLMs [12,15,28]. Recent studies have demonstrated the efficacy of leveraging pretrained LLMs for AMP tasks [12,15,28,14]. Due to their capacity to obviate the need for custom model training or fine-tuning, pretrained LLMs emerge as an appealing solution for 

NL2OR 5 

AMP endeavors. Our work differentiates from existing research, as we focus on creating and editing abstract OR models, and our approach is solver-agnostic. 

There have been a surge of works in the field of the optimization modelling and synthetic data generation for OR tasks [3,27,18,21,15,32] following the Natural Language for Optimization (NL4Opt) NeurIPS 2022 competition. In [3], the authors proposed _OptiMUS_ a modular end to end solution taking natural language description of the problem as input and then process and solves the problem using a multi-agent framework. In [32], researchers from Alibaba introduced a chat based model framework named _OptLLM_ for the similar purpose. In _Chain-of-Experts_ [27], the model employed task specific expert agents powered by external knowledge base. A _Conductor_ co-ordinates the agents effectively to create a ”forward thought chain” for execution and take the feedback signals from the execution environment to trigger a ”backward reflection” in order for better collaboration among the experts. 

## **3 Comparison with current work:** 

|Feature|**OptiGuide [12]**|**OptiMUS [3]**|**Chain of**<br>**Experts [27]**|**NL2OR**<br>**(this paper)**|
|---|---|---|---|---|
|“What-if”<br>analysis|✓|✗|✗|✓|
|End-to-end<br>pipeline|✗|✓|✓|✓|
|Optimizer|Gurobi|Gurobi|Gurobi|OR solver<br>agnostic|
|External<br>Knowledge|✗|✗|✓|✗|
|Validation,|SfGd|Evaluator|Reviewer|JSON Schema|
|Error Correction|aeuar|LLM Agent|LLM Agent|LLM Agent|
|Complexity|Low|Medium|High|Low|
|Modeling type|Concrete|Concrete|Concrete|Abstract|



**Table 1.** Table comparing the functionalities of OptiGuide [12], OptiMUS [3], Chain of Experts [27] with NL2OR(this paper). 

In the table 1, we compare the methods and algorithms of [3,27,12] and in the following, we provide a detailed discussion on each point. 

_What-if analysis:_ By “what-if” analysis, we mean that the constraints and the variables of the problem can change and the algorithm or the end-to-end setup should be able adopt the change. The main purpose of _OptiGuide:_ is “what-if” analysis. In our methodology, NL2OR can create and modify its output based 

6 Li, Wickman, Bhatnagar, Maity and Mukherjee 

on the natural language “what-if” input. OptiMUS [3] and Chain-of-Experts[27] do not support “what-if” analysis. 

_End-to-end pipeline:_ NL2OR provides “end-to-end” architecture where the input is natural language describing the OR problem and it outputs solution alongside a report. OptiMUS [3] and Chain-of-Experts[27] have build this capabilities but NL2OR is the only end-to-end pipeline that also supports the above mentioned ”what-if” analysis. 

_Optimizer:_ The choice of _optimizer_ is important part of the end-to-end architecture for optimization based modelling. In this paper, NL2OR generates abstract model from the natural language then triaged with the appropriate solver. This is an unique capability. 

_External Knowledge:_ In Chain-of-Experts [27]. each experts are equipped with external knowledge base such as supply chain management scenario, Gurobi manual etc. and facilitate In-context learning. NL2OR depends on the knowledge of the LLM. 

_Validation, Error Correction:_ All optimization model has the capability to handle error while formulating the linear program for the OR problem and generating optimization code. OptiMUS[3] uses an “Evaluator” that generates the error code which later being use for debugging and fixing formulation. Chainof-Experts[27] uses a “Code reviewer” in the similar manner. In this work, we employ a custom JSON schema defining permissible properties and valid formats. 

_Complexity:_ In terms of complexity, we employ a simple methodology and architecture in comparison the agent based pipeline of OptiMUS [3] with a “Manager” and Chain-of-Experts[27] with “Conductor”. In addition to the ”Conductor”, Chain-of-Experts[27] employees 11 experts (LLM) with external knowledge and reasoning with the use of Chain-of thought style prompting, summarization and comments. The methodology entails “forward thought construction” for choosing the experts and ”backward reflection” for better collaboration among the experts. This makes the process and the system “highly” complex. With the use of the “Manager” and the contextual choice of agents in any step deems OptiMUS [3] as “medium” complexity. 

_Modeling type:_ An abstract model is a simplified representation of a system or problem, emphasizing essential elements and relationships without delving into details. It enables users to explore various scenarios and perform ‘what-if’ analyses without needing to rebuild the model. Conversely, a concrete model is a detailed and specific version of the abstract model, incorporating all necessary data and parameters, making it ready for solvers to find solutions. Our approach is novel in its focus on abstract modeling, whereas other research has primarily concentrated on concrete modeling 

NL2OR 

7 



<!-- Start of picture text -->
User Query<br>Has original<br>yes Retrieve original yaml<br>model yaml?<br>no<br>NL2OR DSL Generator FORA Builder NL2OR Report Generator<br>Build DSL generation  Build reporting<br>Transpile executables<br>prompts prompts<br>Call LLMs Triage solvers Call LLMs<br>Generate abstract<br>Post processing DSLs model Summarize a report<br>FORA Executor<br>execution?Need  Yes Instantiate concrete model Send report to User<br>No Execute solver<br>Store generated artifacts<br><!-- End of picture text -->

**Fig. 1.** Overview of the NL2OR architecture. There are 4 major blocks in the methodology depicted in the figure. Each performs one important task. 1) With user query as input, the system first decides to create if this is a new problem or edit if it is an old problem to be updated. Then natural language input is transformed to DSL (domain specific language) which is built using prompt engineering and processed to check for error. 2) In the next step, we take the DSL and then convert it into an executable form which we call an abstract model. 3) Then with the user provided data we instantiate the concrete model and solve the problem. 4) Then, with the user query, the variable information and solution the system designs a prompt that generates a database where the solution of the problem is stored, and report is generated. 

## **4 Methodology** 

The main objective is of NL2OR is to convert a natural language description of an OR problem into an OR model, and then generate executable artifacts. These executables are known as abstract models, which have data input contracts. By 

8 Li, Wickman, Bhatnagar, Maity and Mukherjee 

providing data following an input contract, a concrete model instance can be solved by a selected solver. By solving the concrete model, the NL2OR pipeline can generate problem solutions with reports. This takes considerable engineering efforts to develop various parts of the pipeline. In this section, we will go through the architecture of our system in-depth. An overview of the architecture is given in Figure 1. 

The NL2OR pipeline is composed of four major components: Domain Specific Language (DSL) Generator, Framework for OR Analytics (FORA) Builder, FORA Executor and Report Generator. The pipeline starts by admitting a user query to identify the user intention, whether the query is asking to generate a new OR model or edit an existing OR model. The DSL Generator is responsible for converting the natural language query into a formal representation of the optimization problem. The FORA Builder takes the formal representation and generates a FORA model that can be executed by the FORA Executor. The FORA Executor takes the FORA model and user specified parameter data sets, and executes it, returning an optimal solution if the concrete model is feasible. Finally, the Report Generator takes the executor’s output and generates a report that can be easily understood by the user. To illustrate the pipeline, we use the example of optimizing a food purchasing plan to satisfy nutrition constraints while minimizing food purchasing cost. 

### **4.1 DSL Generator** 

The input construct of the DSL generator variates based on a job type, i.e. creation or edition. A creation job only requires a user query, while a edition job also requires providing an original model YAML file. 

Given a user input, the first step in the DSL generator is to construct a DSL generation prompt. Prompt engineering is directly interlinked with the quality of the LLM output. We streamline this process by automating prompt construction within our system. A _prompt builder_ module is designed to automatically generate a prompt for the LLM by amalgamating various components, including instructions, syntax overview for the (OR) model YAML, few-shot learning instances, and the user’s specific problem statement. Subsequently, this constructed prompt is inputted into the LLM to facilitate the generation of the DSL, for a new OR model or an updated model. 

An illustrative example of a model generation prompt is depicted in Figure 2. From the user’s perspective, the complexities involved in OR model YAML and LLM prompts are abstracted away. Users must only provide a query elucidating the OR problem they aim to address. By concealing these technical intricacies, we empower users to focus solely on articulating and engaging with solutions to their OR problems without being burdened by the internal mechanics of the system. See Figure 2 for an illustration of building a food purchasing planning optimization problem. 

**Post-processing and Error Handling:** Following the generation of the OR model YAML, i.e. the DSL, it undergoes a series of validation, correction, and 

NL2OR 9 



<!-- Start of picture text -->
System:<br>You are an assistant working to generate a YAML file for an optimization process which<br>specifies the following parameters of the process:<br>(Description of the YAML schema)<br>Refer to the examples provided with each query to determine how to generate the solution for<br>the optimization processes. Only output these exact outputs in the YAML file.<br>User:<br>Create a YAML file for an optimization process. Here is an example for the following problem:<br>Problem:<br>(Createion query example)<br>YAML file:<br>(Model YAML file example<br>(Additional examples...)<br>Problem:<br>InputData: food costs (vector), food nutritions (matrix), nutrition levels (vectors).<br>Variable: Decide buying quantities for each food, with different cost.<br>Objective: Minimize food purchase cost, which is a sum of production of food cost and food<br>buying quantities.<br>Constraint: Each food contains multiple nutritions. Make sure for each category, the sum of<br>nutrition quantities in all food bought to be no less than the minimum nutrition level, and no<br>more than the maximum level.<br>YAML file:<br><!-- End of picture text -->

**Fig. 2.** An overview of the LLM prompt for model creation. 

processing steps facilitated by error detection mechanisms to ensure its integrity as a valid OR model. In the following, we describe the steps 

_Syntax Error:_ Initially, the YAML is subjected to **syntax error rectification** , which involves _automatically correcting property names, validating correctly labeled constraints, and rectifying various Python expression errors_ . These corrections aim to preempt the need for YAML regeneration if syntax errors are the only remaining issues. 

_Early Detection:_ Subsequently, beyond syntax correction, **early error detection mechanisms** are deployed to identify _irreparable errors_ . These mechanisms include _schema validation, detection of redefined variable declarations_ , and _identification of undefined variables_ . Upon detection of any of these errors, the system throws an error and logs it; as such, errors cannot be rectified programmatically. 

_JSON based validation:_ Validation of the YAML involves employing a custom JSON schema and defining permissible properties and valid formats for each property. For detecting redefined variable declarations, the input and decision variables are scanned to identify any duplicated names. Upon the absence of duplicates, these variables are cached as the defined set of variables, which aids 

10 Li, Wickman, Bhatnagar, Maity and Mukherjee 

in detecting undefined variables. Detection of undefined variables involves transforming Python expressions into abstract syntax trees (ASTs), enabling the extraction of non-control loop variables and subsequent verification of their prior definition as input or decision variables. 

_Runtime Error and Restart:_ After completing these post-processing steps and confirming the absence of detectable errors, the system may still contend with the possibility of _runtime errors_ . Such errors may stem from either a _malformed OR model_ or _mismatches between user data and the OR model specifications_ . In cases where the OR model is malformed, regeneration of the model is necessary, necessitating a restart of the entire process. An output of the food purchase planning optimization model creation is depicted in Figure 3. 

A model edition prompt has the same structure with the creation prompt, with additional Original YAML file sections in few shots examples and user prompt guides. An illustrative example is depicted in Figure 4. An edition of OR model YAML file output, after DSL post processing, is illustrated in Figure 5. The model YAML file editions are highlighted. 

### **4.2 FORA Builder and Executor** 

After the LLM post-processing step, assuming successful completion, a model YAML file is transpiled into an FORA model. This transpile step primarily involves the instantiation of entities within the internal FORA library, with metadata declared in the InputData property of the YAML. The InputData property is a contractual agreement between the user and the OR model, delineating the requisite data for the solver to optimize the OR model. Consequently, it falls upon the user to furnish the specified data accordingly. Notably, the method of providing data to our system is agnostic to application specifics and, therefore, lies outside the primary scope of this work. 

An illustration of this process is provided in Figure 6 for the objective. Upon loading the YAML, the objective of the OR model is instantiated by extracting the construction definition that delineates the objective. Subsequently, the associated Python expression is executed, incorporating the specified sense parameter, following which the objective is incorporated into the OR model. This procedural pattern remains consistent for the remaining properties in the OR model YAML. 

The generated YAML file also indicates solver specific properties, so that a generated abstract model is triaged with a proper solver during the DSL generation phase. The generated artifacts from the FORA builder is an abstract model program. 

If the user furnishes input data sets, the FORA executor is then able to instantiate a concrete model. By executing the optimize method of a concrete model with the triaged solver, the FORA executor then either generates an optimal solution for feasible concrete models or returns a status flag with logs indicating infeasibility, early stop or sub-optimality. 

NL2OR 11 

InputData : max nutr : desc : Dictionary of max n u t r i t i o n values key : − n u t r i t i o n : s t r value : − max level : f l o a t min nutr : desc : Dictionary of min n u t r i t i o n values key : − n u t r i t i o n : s t r value : − m i n l e v e l : f l o a t n u t r v a l s : desc : Dictionary of n u t r i t i o n values key : − food : s t r − n u t r i t i o n : s t r value : − n u t r i t i o n v a l u e : f l o a t c o s t s : desc : Dictionary of food c o s t s key : − food : s t r value : − c o s t : f l o a t VariableBatch : − desc : Quantities of each food bought name : buy key : − food : s t r value : − quantity : i n t e g e r i n d i c e s : l i s t ( s e l f . c o s t s . keys ( ) ) vtype : I lower bound : 0 upper bound : i n f Objective : desc : Minimize the food purchase c o s t c o n s t r u c t o r : sum( s e l f . c o s t s [ i ] ∗ s e l f . buy [ i ] _\_ f o r i in s e l f . c o s t s ) sense : min ConstraintBatch : − desc : Constraint on the t o t a l minimum n u t r i t i o n name : min nutr generator : (sum( s e l f . n u t r v a l s [ i , j ] ∗ s e l f . buy [ i ] _\_ f o r i in s e l f . c o s t s ) _>_ = s e l f . min nutr [ j ] _\_ f o r j in s e l f . min nutr ) − desc : Constraint on the t o t a l maximum n u t r i t i o n name : max nutr generator : (sum( s e l f . n u t r v a l s [ i , j ] ∗ s e l f . buy [ i ] _\_ f o r i in s e l f . c o s t s ) _<_ = s e l f . max nutr [ j ] _\_ f o r j in s e l f . max nutr ) 

**Fig. 3.** Created OR model YAML for the food purchasing planning optimization problem. 

12 Li, Wickman, Bhatnagar, Maity and Mukherjee 

**System:** You are an assistant working to edit a YAML file for an optimization process which specifies the following parameters of the process: (Description of the YAML schema) Refer to the examples provided with each query to determine how to revise the given YAML file. Only output these exact outputs in the YAML file. **User:** Based on a given query, update the original YAML, and output the updated YAML. Here are a few examples. Problem: (An edit query example) Original YAML: (Original model YAML file example) Updated YAML: (Edited model YAML file example) (Additional examples...) Problem: _Double the maximum nutrition levels in the model_ . Original YAML: InputData : max nutr : desc : Dictionary of max n u t r i t i o n values key : − n u t r i t i o n : s t r value : − max level : f l o a t min nutr : desc : Dictionary of min n u t r i t i o n values key : − n u t r i t i o n : s t r value : − m i n l e v e l : f l o a t ... Updated YAML: 

**Fig. 4.** An overview of the LLM prompt for model edition. 

### **4.3 Report Generator** 

Once FORA is employed to execute a concrete model, yielding a solution or status log, the Report Generator facilitate further analysis of the results, storing this solution in a database may be necessary. The responsibility of constructing the database schema for the solution falls under the purview of the report summarization step. The _report prompt builder_ plays a vital role in this process by assimilating details about the OR problem and its solution, abstracting any information related to sensitive user data, and generating a report prompt tailored 

NL2OR 13 



<!-- Start of picture text -->
InputData :<br>max nutr :<br>desc : Dictionary of max n u t r i t i o n values<br>key :<br>− n u t r i t i o n : s t r<br>value :<br>− max level : f l o a t<br>. . .<br>ConstraintBatch :<br>− desc : Constraint on the t o t a l minimum n u t r i t i o n<br>name : min nutr<br>generator : (sum( s e l f . n u t r v a l s [ i , j ] ∗ s e l f . buy [ i ] \<br>f o r i in s e l f . c o s t s ) > = s e l f . min nutr [ j ] \<br>f o r j in s e l f . min nutr )<br>− desc : Constraint on the t o t a l maximum n u t r i t i o n<br>name : max nutr<br>generator : (sum( s e l f . n u t r v a l s [ i , j ] ∗ s e l f . buy [ i ] \<br>f o r i in s e l f . c o s t s ) < = 2∗ s e l f . max nutr [ j ] \<br>f o r j in s e l f . max nutr )<br><!-- End of picture text -->

**Fig. 5.** Edited OR model YAML for the food purchasing planning optimization problem. 

obj = Objective ( c o n s t r u c t o r=exec ( or yaml [ ” c o n s t r u c t o r ” ] ) , sense=or yaml [ ” sense ” ] ) model . add obj ( obj ) 

**Fig. 6.** Example of adding the objective to an OR model. 

for the LLM. The report prompt builder is generated using 1) the user prompt 2) variable description that is generated in the OR model and 3) the solution of the concrete model. Using the power of the LLMs, the schema is easily generated from the variable description and the column of the tables is updated with the solution values. Utilizing this prompt, the LLM generates a database schema designed explicitly for the solution to the OR model. An illustrative example of the resulting database schema is presented in Figure 7. 

After establishing this database schema, the report YAML undergoes processing, and the OR solution is transformed into an intermediate data format conducive to being seamlessly written as rows to a database. This trans-formative step prepares the OR solution data for efficient storage and retrieval in a structured database environment. 

14 Li, Wickman, Bhatnagar, Maity and Mukherjee 

Database Schema : t a b l e s : − name : Diet Solution desc : The s o l u t i o n r e p o r t f o r the d i e t problem . v a r i a b l e : buy columns : − name : Food type : s t r desc : The name of the food . primary key : true value : food − name : Buy type : i n t desc : Quantity of each food bought . value : quantity 

**Fig. 7.** Example of a solution database schema for the diet problem. 

## **5 Experiments** 

### **5.1 OR Model Creation** 

For initial experimentation aimed at assessing the capabilities of NL2OR, we evaluate its proficiency in generating a valid OR model that can be executed from a specified user query. The experimentation involved assessing NL2OR across a spectrum of 30 distinct OR problem instances, spanning various scenarios encountered in practical applications. A comprehensive overview of these problem instances is presented in Table 2. Additionally, we explored the performance of NL2OR using two different LLM models, gpt-35-turbo-16k and gpt-4-32k, each subjected to varied temperature values. The models were evaluated based on two key metrics: _Valid@k_ and _Latency_ . Valid@k is the average number of successes generating a valid OR model when given k attempts. At the same time, Latency is the amount of time, in seconds, required for NL2OR to generate and execute the OR model. The results are given in Table 3. 

As one might expect, gpt-4-32k has a higher latency compared to gpt-35turbo-16k due to it having a more significant number of parameters. Additionally, we see that gpt-4-32k outperforms gpt-35-turbo-16k w.r.t. the Valid@k metric across all temperature values, showcasing its superior performance. 

Both models performed similarly in producing valid YAML outputs of the OR model for well explained real world scenarios such as inventory assignment, network flow optimization or resource scheduling. One of the major differences between the gpt-35-turbo-16k and gpt-4-32k models was in the handling of more ambiguous mathematical optimization such as optimizing the Knapsack problem or graph based algorithm solving with linear programming, where the gpt-35turbo-16k consistently failed to produce a YAML describing a valid OR solution. 

NL2OR 15 

|**Problem**|**Description**|**# problems**|
|---|---|---|
|Minimum vertex<br>covering|A vertex cover having the smallest possible<br>number of vertices for a given graph. [9]|3|
|Knapsack optimization|Given a set of items, each with a weight and<br>a value, determine which items to include in<br>the collection so that the total weight is less than<br>or equal to a given limit and the total value is as<br>large as possible.[9]|3|
|Simple linear<br>programming|Achieve the best outcome in a mathematical<br>model whose requirements and objective are<br>represented by linear relationships.[11]|3|
|Inventory assignment<br>optimization|Minimize operational costs by optimizing inventory<br>assignments in a two echelon warehouse-store network.[36]|3|
|Multi echelon inventory<br>optimization|Minimize supply chain costs by optimizing inventory<br>plan in a multi echelon supply chain network.[10]|3|
|Bill-of-material<br>optimization|Maximize material utilization and product fulfillment<br>with limited raw materials in a manufacturing facility.[11]|3|
|Network flow<br>optimization|Minimize flow costs while satisfying node constraints.[11]|3|
|Logistic<br>optimization|Minimize logistic cost in a supply chain network. [17]|3|
|Resource scheduling<br>optimization|Minimize agent resource cost and maximize resource<br>utilization, while respecting agent shift and skill<br>requirements.[36]|6|



**Table 2.** Brief description of different optimization problems in the test dataset 

|**Model**|**Temp**|**Valid**<br>|**Valid**<br>|**Valid**<br>||**Lat**<br>|**ency **<br>|**(s)**<br>||
|---|---|---|---|---|---|---|---|---|---|
|||**@1**|**@3**|**@5**|Ave.|Std.|P50|P75|P90|
|gpt-35-turbo-16k|0.1|0.6|0.66|0.7|4.58|2.09|4.12|5.46|6.93|
|gpt-35-turbo-16k|0.2|0.7|0.73|0.73|4.44|1.69|4.18|4.84|6.67|
|gpt-35-turbo-16k|0.4|0.63|0.66|0.73|4.59|1.77|4.33|5.73|6.88|
|gpt-35-turbo-16k|0.6|0.6|0.63|0.7|4.69|2.17|4.23|5.99|6.85|
|gpt-35-turbo-16k|0.8|0.63|0.66|0.73|4.82|1.91|4.59|6.24|7.25|
|gpt-4-32k|0.1|0.73|0.7|0.8|35.49|15.79|34.17|45.22|59.34|
|gpt-4-32k|0.2|0.83|0.86|0.9|35.49|16.17|31.24|40.69|58.04|
|gpt-4-32k|0.4|0.63|0.8|0.9|36.94|20.40|32.38|42.53|55.31|
|gpt-4-32k|0.6|0.73|0.8|0.9|35.32|17.70|32.63|42.53|61.80|
|gpt-4-32k|0.8|0.7|0.73|0.86|36.77|15.50|32.99|39.45|61.59|



**Table 3.** Experiments conducted on a set of 30 different OR problem creation statements 

### **5.2 OR Model Edit** 

An essential practical application of NL2OR is editing existing OR models. We characterize OR model edits as introducing alterations or augmentations to the properties outlined in the OR model YAML. Such refinement proves invaluable when addressing minor adjustments necessary to accommodate evolving 

- 16 Li, Wickman, Bhatnagar, Maity and Mukherjee 



<!-- Start of picture text -->
k = 1 k = 3 k = 5<br>1.0<br>0.8<br>0.6<br>0.4<br>0.2<br>0.0<br>0.1 0.2 0.4 0.6 0.8 0.1 0.2 0.4 0.6 0.8 0.1 0.2 0.4 0.6 0.8<br>Temperature Temperature Temperature<br>gpt-35-turbo-16k gpt-4-32k<br>Valid@k<br><!-- End of picture text -->

**Fig. 8.** Bar plot of NL2OR edit experiments over various k values for Valid@k and temperature values used for the LLMs. 

|**Model**|**Tem**|**Valid**|**Valid**|**Valid**||**La**|**tency**|**(s)**||
|---|---|---|---|---|---|---|---|---|---|
||**p**|**@1**|**@3**|**@5**|Ave.|Std.|P50|P75|P90|
|gpt-35-turbo-16k|0.1|0.97|0.97|0.97|4.37|1.75|3.97|4.42|8.13|
|gpt-35-turbo-16k|0.2|0.93|0.93|0.97|4.37|1.76|4.02|4.39|8.08|
|gpt-35-turbo-16k|0.4|0.92|0.92|0.92|4.37|1.75|3.94|4.40|8.09|
|gpt-35-turbo-16k|0.6|0.93|0.93|0.93|4.38|1.78|4.03|4.49|8.09|
|gpt-35-turbo-16k|0.8|0.92|0.93|0.93|4.37|1.77|3.99|4.49|8.12|
|gpt-4-32k|0.1|0.98|1.00|1.00|15.00|7.38|14.19|15.63|29.46|
|gpt-4-32k|0.2|0.98|1.00|1.00|15.27|6.66|13.76|15.54|28.86|
|gpt-4-32k|0.4|0.97|1.00|1.00|15.46|6.72|14.04|15.61|28.47|
|gpt-4-32k|0.6|0.98|0.98|0.98|15.36|6.82|13.95|16.07|28.69|
|gpt-4-32k|0.8|0.98|0.97|0.97|15.24|6.77|13.76|15.55|28.77|



**Table 4.** Experiments conducted on a set of 60 different OR problem edition statements 

customer or business demands or validating prospective alterations to the foundational system upon which the model relies. This is also known as What-if analysis. For instance, this functionality proves invaluable when integrating a new product into a resource allocation problem or assessing the impact of updated material constraints on the resultant outcomes. 

The test data is constructed as follows. We select 15 validated OR model YAML as original YAMLs, and we use GPT-4 to create possible model update queries. For each YAML file, four edition queries are generated, and thus 60 different edit scenarios are prepared. The test over 60 different edit scenarios where the results are given in Table 4 

Like the generation experiments, gpt-4-32k exhibits superior performance over gpt-35-turbo-16k concerning the Valid@k metric across all temperature settings, albeit with an associated increase in Latency. Across the entire spectrum 



<!-- Start of picture text -->
NL2OR 17<br>k = 1 k = 3 k = 5<br>1.0<br>0.8<br>0.6<br>0.4<br>0.2<br>0.0<br>0.1 0.2 0.4 0.6 0.8 0.1 0.2 0.4 0.6 0.8 0.1 0.2 0.4 0.6 0.8<br>Temperature Temperature Temperature<br>gpt-35-turbo-16k gpt-4-32k<br>Valid@k<br><!-- End of picture text -->

**Fig. 9.** Bar plot of NL2OR creation experiments over various k values for Valid@k and temperature values used for the LLMs. 

of temperature values, NL2OR consistently demonstrates its capability to incorporate user-specified modifications into the OR model accurately. A comparative analysis with the creation experiments underscores the relative simplicity of modifying an existing OR model compared to generating a novel one. Intuitively, this makes sense, as translating user intentions into components of an OR model is much easier when the prior underlying system is given. 

### **5.3 OR Model Creation for LPWP Data:** 

We evaluate the OR Model creation problem with the LPWP dataset [16] that is collected from the NL4Opt competition in NeurIPS 2022. We evaluate NL2OR Model creation on 287 test samples data with three different LLM models, gpt35-turbo-16k, gpt-4-32k and the latest model gpt-4o. We choose the temperature to be 0 _._ 1 for all the experiments. In the table 5, we show the accuracy ( _Valid_ @1 _)_ , average number of prompt tokens for each LLMs, the total cost to run the experiments and latency. Accuracy is the number of successful generation of the OR models out of 287 problems. We compute the prompt tokens from the _usage_ of the chat completion api of each LLM models. We calculate the cost in the following way, 

Total Cost = (Prompt Tokens _/_ 1000000) _∗_ Cost per 1M input tokens) + (Completion Tokens _/_ 1000000) _∗_ Cost per 1M output tokens) 

The pricing for all the models can be found [1]. All the models performed really well. As expected, gpt-4o performed the best in terms of accuracy (94 _._ 4%) and the cost is lowest for gpt-35-turbo-16k. For the gpt-4 the accuracy is close to the gpt-4o but the cost higher than that of gpt-4o model. This is due to the fact that gpt-4o is designed to be more cost effective than gpt-4 which is a very 

18 Li, Wickman, Bhatnagar, Maity and Mukherjee 

large model. In terms of latency, gpt-35-turbo-16k has the lowest latency and gpt-4-32k being a large model has the highest latency. gpt-4o performed the best in terms of accuracy, latency and cost overall. 

|**Mdl**|**Accuracy**|**Prompt Token**|**Total Cost**|**Lat**|**ency (s)**||
|---|---|---|---|---|---|---|
|**oe**|**(Valid@1)**|**(Mean** _±_ **std)**|**(USD)**<br>Ave.|Std.|P50 P75|P90|
|gpt-4o|94_._4%|2230_._76_±_22_._12|2_._84<br>5.01|2.01|4.49 5.47|6.93|
|gpt-4-32k|91_._6%|2852_._61_±_22_._34|30_._45<br>7.22|1.48|7.08 8.0|9.08|
|gpt-35<br>-turbo-16k|77_._3%|2852_._61_±_22_._34|0_._57<br>3.93|0.93|3.8<br>4.43|4.968|



**Table 5.** Experimental result on LPWP Dataset. 

## **6 Conclusion and Future Work** 

In this paper, we propose a novel methodology that creates new OR solutions and edits existing OR solutions using natural language (NL) queries. Our proposed method can significantly reduce the time and effort required to model and solve complex OR problems, which reduces the time required to formulate a problem in a solver-specific format and provides a framework for the development of an interactive OR problem-solving tool that can be used by non-experts. We have implemented the proposed methodology as an end-to-end pipeline, named _NL2OR_ , that can 1) take natural language input and generate an abstract OR model; 2) resolve data mapping and triage solvers to provide a solution to the generated OR problem; 3) edit the generated OR model for what-if analysis. To demonstrate experimentally, first, we evaluate NL2OR across a spectrum of more than 30 distinct OR problem instances, spanning various scenarios encountered in practical applications where NL2OR shown to have high accuracy and low latency. Additionally, we show how NL2OR is capable of effectively editing existing OR models. Finally, we choose the LPWP dataset [16] and show the effectiveness of NL2OR in terms of accuracy and cost across ( _≈_ )300 test problems. It is always beneficial to use smaller models as they are faster and cheaper. In our experiment, we show the cost and accuracy for different LLMs. A comprehensive study into the use and effectiveness of SLM is an important future work. Moreover, a study on the use of reinforcement learning to improve the performance of the NL2OR is an exciting direction. 

## **References** 

> 1. https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openaiservice, `https://azure.microsoft.com/en-us/pricing/details/ cognitive-services/openai-service` 

NL2OR 19 

2. Achiam, J., Adler, S., Agarwal, S., Ahmad, L., Akkaya, I., Aleman, F.L., Almeida, D., Altenschmidt, J., Altman, S., Anadkat, S., et al.: Gpt-4 technical report. arXiv preprint arXiv:2303.08774 (2023) 

3. AhmadiTeshnizi, A., Gao, W., Udell, M.: Optimus: Scalable optimization modeling with (mi) lp solvers and large language models. arXiv preprint arXiv:2402.10172 (2024) 

4. Besta, M., Blach, N., Kubicek, A., Gerstenberger, R., Gianinazzi, L., Gajda, J., Lehmann, T., Podstawski, M., Niewiadomski, H., Nyczyk, P., et al.: Graph of thoughts: Solving elaborate problems with large language models. arXiv preprint arXiv:2308.09687 (2023) 

5. Brown, T., Mann, B., Ryder, N., Subbiah, M., Kaplan, J.D., Dhariwal, P., Neelakantan, A., Shyam, P., Sastry, G., Askell, A., Agarwal, S., Herbert-Voss, A., Krueger, G., Henighan, T., Child, R., Ramesh, A., Ziegler, D., Wu, J., Winter, C., Hesse, C., Chen, M., Sigler, E., Litwin, M., Gray, S., Chess, B., Clark, J., Berner, C., McCandlish, S., Radford, A., Sutskever, I., Amodei, D.: Language models are few-shot learners. In: Larochelle, H., Ranzato, M., Hadsell, R., Balcan, M., Lin, H. (eds.) Advances in Neural Information Processing Systems. vol. 33, pp. 1877–1901. Curran Associates, Inc. (2020) 

6. Brown, T., Mann, B., Ryder, N., Subbiah, M., Kaplan, J.D., Dhariwal, P., Neelakantan, A., Shyam, P., Sastry, G., Askell, A., et al.: Language models are few-shot learners. Advances in neural information processing systems **33** , 1877–1901 (2020) 

7. Chowdhery, A., Narang, S., Devlin, J., Bosma, M., Mishra, G., Roberts, A., Barham, P., Chung, H.W., Sutton, C., Gehrmann, S., et al.: Palm: Scaling language modeling with pathways. Journal of Machine Learning Research **24** (240), 1–113 (2023) 

8. Devlin, J., Chang, M.W., Lee, K., Toutanova, K.: Bert: Pre-training of deep bidirectional transformers for language understanding. arXiv preprint arXiv:1810.04805 (2018) 

9. Du, D., Pardalos, P.M.: Handbook of combinatorial optimization, vol. 4. Springer Science & Business Media (1998) 

10. Eruguz, A.S., Sahin, E., Jemai, Z., Dallery, Y.: A comprehensive survey of guaranteed-service models for multi-echelon inventory optimization. International Journal of Production Economics **172** , 110– 125 (2016). https://doi.org/https://doi.org/10.1016/j.ijpe.2015.11.017, `https://www.sciencedirect.com/science/article/pii/S0925527315005162` 

11. Hillier, F.S., Lieberman, G.J.: Introduction to Operations Research. McGraw-Hill, New York, NY, USA, seventh edn. (2001) 

12. Li, B., Mellou, K., Zhang, B., Pathuri, J., Menache, I.: Large language models for supply chain optimization. arXiv (2023), `https://doi.org/10.48550/arXiv. 2307.03875` 

13. Nair, V., Bartunov, S., Gimeno, F., von Glehn, I., Lichocki, P., Lobov, I., O’Donoghue, B., Sonnerat, N., Tjandraatmadja, C., Wang, P., Addanki, R., Hapuarachchi, T., Keck, T., Keeling, J., Kohli, P., Ktena, I., Li, Y., Vinyals, O., Zwols, Y.: Solving mixed integer programs using neural networks. arXiv (2021), `https://doi.org/10.48550/arXiv.2012.13349` 

14. Prasath, G., Karande, S.: Synthesis of mathematical programs from natural language specifications. arXiv preprint arXiv:2304.03287 (2023) 

15. Ramamonjison, R., Li, H., Yu, T., He, S., Rengan, V., Banitalebi-dehkordi, A., Zhou, Z., Zhang, Y.: Augmenting operations research with auto-formulation of optimization models from problem descriptions. In: Empirical Methods in Natural 

20 Li, Wickman, Bhatnagar, Maity and Mukherjee 

Language Processing: Industry Track. pp. 29–62. Association for Computational Linguistics (2022). https://doi.org/10.18653/v1/2022.emnlp-industry.4, `https:// aclanthology.org/2022.emnlp-industry.4` 

16. Ramamonjison, R., Li, H., Yu, T.T., He, S., Rengan, V., Banitalebi-Dehkordi, A., Zhou, Z., Zhang, Y.: Augmenting operations research with auto-formulation of optimization models from problem descriptions. arXiv preprint arXiv:2209.15565 (2022) 

17. Rushton, A., Croucher, P., Baker, P.: The handbook of logistics and distribution management: Understanding the supply chain. Kogan Page Publishers (2022) 

18. Tang, Z., Huang, C., Zheng, X., Hu, S., Wang, Z., Ge, D., Wang, B.: Orlm: Training large language models for optimization modeling. arXiv preprint arXiv:2405.17743 (2024) 

19. Team, G., Anil, R., Borgeaud, S., Wu, Y., Alayrac, J.B., Yu, J., Soricut, R., Schalkwyk, J., Dai, A.M., Hauth, A., et al.: Gemini: a family of highly capable multimodal models. arXiv preprint arXiv:2312.11805 (2023) 

20. Touvron, H., Lavril, T., Izacard, G., Martinet, X., Lachaux, M.A., Lacroix, T., Rozi`ere, B., Goyal, N., Hambro, E., Azhar, F., et al.: Llama: Open and efficient foundation language models. arXiv preprint arXiv:2302.13971 (2023) 

21. Tsouros, D., Verhaeghe, H., Kadıo˘glu, S., Guns, T.: Holy grail 2.0: From natural language to constraint models. arXiv preprint arXiv:2308.01589 (2023) 

22. Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A.N., Kaiser, �L., Polosukhin, I.: Attention is all you need. Advances in neural information processing systems **30** (2017) 

23. Wang, X., Wei, J., Schuurmans, D., Le, Q., Chi, E., Narang, S., Chowdhery, A., Zhou, D.: Self-consistency improves chain of thought reasoning in language models. arXiv preprint arXiv:2203.11171 (2022) 

24. Wang, X., Wei, J., Schuurmans, D., Le, Q., Chi, E., Narang, S., Chowdhery, A., Zhou, D.: Self-consistency improves chain of thought reasoning in language models. arXiv preprint arXiv:2203.11171 (2022) 

25. Wei, J., Tay, Y., Bommasani, R., Raffel, C., Zoph, B., Borgeaud, S., Yogatama, D., Bosma, M., Zhou, D., Metzler, D., et al.: Emergent abilities of large language models. arXiv preprint arXiv:2206.07682 (2022) 

26. Wei, J., Wang, X., Schuurmans, D., Bosma, M., Xia, F., Chi, E., Le, Q.V., Zhou, D., et al.: Chain-of-thought prompting elicits reasoning in large language models. Advances in neural information processing systems **35** , 24824–24837 (2022) 

27. Xiao, Z., Zhang, D., Wu, Y., Xu, L., Wang, Y.J., Han, X., Fu, X., Zhong, T., Zeng, J., Song, M., et al.: Chain-of-experts: When llms meet complex operations research problems. In: The Twelfth International Conference on Learning Representations (2023) 

28. Yang, C., Wang, X., Lu, Y., Liu, H., Le, Q.V., Zhou, D., Chen, X.: Large language models as optimizers. arXiv (2023), `https://doi.org/10.48550/arXiv. 2309.03409` 

29. Yao, S., Yu, D., Zhao, J., Shafran, I., Griffiths, T., Cao, Y., Narasimhan, K.: Tree of thoughts: Deliberate problem solving with large language models. Advances in Neural Information Processing Systems **36** (2024) 

30. Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., Cao, Y.: React: Synergizing reasoning and acting in language models. arXiv preprint arXiv:2210.03629 (2022) 

31. Zhang, J., Liu, C., Li, X., Zhen, H.L., Yuan, M., Li, Y., Yan, J.: A survey for solving mixed integer programming via machine learning. Neurocomputing **519** , 205– 

NL2OR 21 

217 (2023). https://doi.org/https://doi.org/10.1016/j.neucom.2022.11.024, `https: //www.sciencedirect.com/science/article/pii/S0925231222014035` 

32. Zhang, J., Wang, W., Guo, S., Wang, L., Lin, F., Yang, C., Yin, W.: Solving general natural-language-description optimization problems with large language models. arXiv preprint arXiv:2407.07924 (2024) 

33. Zhang, S., Roller, S., Goyal, N., Artetxe, M., Chen, M., Chen, S., Dewan, C., Diab, M., Li, X., Lin, X.V., et al.: Opt: Open pre-trained transformer language models. arXiv preprint arXiv:2205.01068 (2022) 

34. Zhao, W.X., Zhou, K., Li, J., Tang, T., Wang, X., Hou, Y., Min, Y., Zhang, B., Zhang, J., Dong, Z., et al.: A survey of large language models. arXiv preprint arXiv:2303.18223 (2023) 

35. Zheng, C., Liu, Z., Xie, E., Li, Z., Li, Y.: Progressive-hint prompting improves reasoning in large language models. arXiv preprint arXiv:2304.09797 (2023) 

36. Oncan,<sup>¨</sup> T.: A survey of the generalized assignment problem and its applications. INFOR: Information Systems and Operational Research **45** (3), 123– 141 (2007). https://doi.org/10.3138/infor.45.3.123, `https://doi.org/10.3138/ infor.45.3.123` 

