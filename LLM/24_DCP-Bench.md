# **DCP-Bench-Open: Evaluating LLMs for Constraint Modelling of Discrete Combinatorial Problems** 

KOSTIS MICHAILIDIS<sup>∗</sup> , KU Leuven, Belgium DIMOS TSOUROS, University of Western Macedonia, Greece TIAS GUNS, KU Leuven, Belgium 

Discrete Combinatorial Problems (DCPs) are prevalent in industrial decision-making and optimisation. However, while constraint solving technologies for DCPs have advanced significantly, the core process of formalising them—namely constraint modelling—requires significant expertise and remains a bottleneck for wider adoption. Aiming to alleviate this bottleneck, recent studies have explored using Large Language Models (LLMs) to transform combinatorial problem descriptions into executable constraint models. However, the existing evaluation datasets for discrete constraint modelling are often limited to small, homogeneous, or domain-specific problems, which do not capture the diversity of real-world scenarios. This work addresses this gap by introducing **DCP-Bench-Open** , a novel benchmark that includes a diverse set of well-known discrete combinatorial problems sourced from the Constraint Programming (CP) and Operations Research (OR) communities, structured explicitly for evaluating LLM-driven constraint modelling. With this dataset, and given the variety of modelling frameworks, we compare and evaluate the modelling capabilities of LLMs for three distinct constraint modelling systems, which vary in abstraction level and underlying syntax. Notably, the results show higher performance when modelling with a high-level Python-based framework. Additionally, we systematically evaluate the use of prompt-based and inference-time compute methods across different LLMs, which further increase accuracy, reaching up to 91% on this highly challenging benchmark. DCP-Bench-Open is publicly available in https://github.com/DCP-Bench/DCP-Bench-Open. 

## **1 Introduction** 

Discrete combinatorial problems exist in numerous real-world applications, where optimal decision-making is essential, including logistics, scheduling, and network design (Paschos 2014). Solving these problems requires finding the best combination of elements under specific constraints, which is computationally intensive; many such problems are NP-hard, meaning that their solving time can increase exponentially with problem size in the worst case. This challenge has led to the development of various industrial solvers and solving paradigms, including Constraint Programming (CP), Integer Linear Programming (ILP) and Boolean Satisfiability (SAT), among others (Paschos 2014; Simonis 1999; Wallace 1996). 

Common to most solving paradigms is the need for an input formal model: a declarative specification in which users specify _what_ constraints the solution must satisfy, rather than detailing _how_ to find it. Despite the effectiveness of such solving approaches, the complex process of modelling—translating a problem description into a formal specification—remains a significant bottleneck. Specifically for CP, modelling involves identifying and formally defining the problem’s decision variables with their domains, constraints on the variables, and, where applicable, an objective function. This process demands a deep understanding of the application domain and proficiency in the chosen modelling framework, both syntactically and semantically. This modelling complexity 

∗Corresponding Author. 

Authors’ Contact Information: Kostis Michailidis, orcid: 0009-0000-2139-0106, kostis.michailidis@kuleuven.be, KU Leuven, Belgium; Dimos Tsouros, orcid: 0000-0002-3040-0959, dtsouros@uowm.gr, University of Western Macedonia, Greece; Tias Guns, orcid: 0000-0002-2156-2155, tias.guns@kuleuven.be, KU Leuven, Belgium. 

This work is licensed under a Creative Commons Attribution International 4.0 License. 

6:2 • Michailidis, Tsouros & Guns 



<!-- Start of picture text -->
Find the shortest tour that Paris → Amsterdam<br>visits each of these cities: … → … → New York<br>Combinatorial Modelling Constraint<br>Solution<br>Problem Assistant Model<br>Solver<br><!-- End of picture text -->

Fig. 1. LLM-driven constraint modelling: users state a combinatorial problem in natural language, which the system transforms into a formal constraint representation, and delegates the latter to a constraint solver. 

is recognised as one of the most important limitations for the wider use of combinatorial optimisation techniques, restricting accessibility for non-experts (Freuder 2018; Freuder and O’Sullivan 2014). 

This raises a central question: Can we lower the modelling barrier to make CP and related technologies for Discrete Combinatorial Problems accessible to a broader audience? Prior works in this direction include constraint acquisition methods that aim to learn the constraints from data (Bessiere, Carbonnel, et al. 2023; Bessiere, Coletta, et al. 2007; Mechqrane et al. 2024) and constraint detection methods from natural language (Kiziltan et al. 2016). More recently, advances in large language models (LLMs) offer the opportunity of creating _modelling assistants_ (Cappart et al. 2025) that could initiate or (semi-)automate the modelling process (as illustrated in Figure 1), in analogy to how coding assistants are widely being used for a variety of coding tasks (M. Chen et al. 2021; Fan et al. 2023; Jiang et al. 2024). 

Nevertheless, LLM-driven constraint modelling presents different challenges compared to general code generation. First, while imperative code specifies step-by-step sequential instructions, declarative modelling requires that all constraints must hold true simultaneously. Second, formalizing the extracted conceptual constraints is hard due to the combinatorial nature of modelling choices themselves. Specifically, modelling requires selecting a _viewpoint_ —a specific way to represent variables and structure constraints based on the problem domain—from potentially many alternatives (Frisch et al. 2005). Third, verifying the correctness of a generated constraint model is different from imperative code generation, in which correctness can often be tested using example inputs and expected outputs (e.g., unit tests). In contrast, constraint modelling lacks such verifications, as a “test” would require knowing the correct model or solution in advance. 

Recent works have explored the potential of LLMs in this direction by generating solvable representations of numerical reasoning problems in formal declarative modelling frameworks (Tsouros et al. 2023; X. Ye, Q. Chen, et al. 2023). Ishay et al. (2023) frame Logic Grid Puzzles (LGPs) as Answer Set Programming (ASP) programs, Prasath and Karande (2023) focus on linear optimization problems, and X. Ye, Q. Chen, et al. (2023) propose translating inputs into satisfiability problems. Although promising results have been achieved for simple domain-specific problems, such as small-scale linear optimization problems (Prasath and Karande 2023; Ramamonjison, Yu, et al. 2023) and LGPs (Ishay et al. 2023), scaling to more complex and diverse problems remains a significant challenge (Michailidis et al. 2024). 

Existing limitations can be summarized as follows. (a) Current NL-to-CP and other benchmarks lack the diversity and complexity necessary to represent a wide range of realistic discrete combinatorial problems. This constitutes a prerequisite for assessing LLM capabilities on this task. (b) Given the wide variety of constraint modelling frameworks available, ranging in abstraction levels and interface types, there is a need for systematic evaluation across them to explore their impact on LLM-driven model generation. (c) Applying recent LLM advances to combinatorial modelling remains underexplored, even though test-time scaling methods have shown success for complex programming tasks (X. Chen et al. 2023). 

To address the lack of representative benchmarks, we developed DCP-Bench-Open (extending the previous CPBench (Michailidis et al. 2025b)), a novel dataset of discrete combinatorial problems gathered from distinct sources 

DCP-Bench-Open: Evaluating LLMs for Constraint Modelling of Discrete Combinatorial Problems • 6:3 

within the research community. While existing repositories (e.g., PyCSP3 examples (Lecoutre and Szczepanski 2020), CSPLib (Gent and Walsh 1999), and others) contain constraint models, they are not suitable for automated evaluation of LLM-generated models, as they are not structured for this purpose. We designed DCP-Bench-Open for this task based on solution-level evaluation, which is non-trivial since more than one (optimal) solution may exist for a combinatorial problem (detailed in Section 5.2). 

Using this benchmark, we systematically evaluate the capabilities of state-of-the-art LLMs when prompted to generate models using different modeling frameworks, varying by abstraction level (low vs. high) and interface type (domain-specific vs. Python-based). We select the following as representatives: OR-Tools (Perron and Didier 2024; Perron and Furnon 2024) offers a low-level, direct solver Python API; CPMpy (Guns 2019) provides a highlevel, Python-based modelling interface; and MiniZinc (Nethercote et al. 2007) is a well-established high-level, domain-specific modelling language. Across these frameworks, we compare different system prompts, starting from basic minimal instructions and progressing to detailed, classroom-level, modeling guidelines and including documentation specific to the framework used. 

With inference-time computation showing high success rates across various LLM tasks (Snell et al. 2024), we adapt and evaluate such methods in order to further enhance the quality of the generated constraint models. Firstly, we use Retrieval-Augmented In-Context Learning (RAICL) to enrich the prompt context with representative examples (Michailidis et al. 2024; X. Ye, Iyer, et al. 2023). Secondly, we investigate reasoning LLMs (J. Sun et al. 2025) that utilize internal chain-of-thought processes to decompose the modelling procedure. Thidly, we exploit the probabilistic nature of LLMs, by repeatedly sampling multiple CP models and employing solution majority voting to select the most reliable model based on the observed outputs (M. Chen et al. 2021; Olausson et al. 2023). Finally, to address detectable errors, such as runtime or solution printing ones, and trigger self-correction of modelling errors, we investigate the effect of self-verification prompting on LLMs for iterative model refinement. The primary contributions of this work are the following: 

- A novel benchmark structured specifically for evaluating LLM-driven constraint modelling of discrete combinatorial multi-instance problems. The dataset consists of 164 diverse combinatorial problem descriptions along with their runnable constraint models, 23 of which contain more than one data instance. 

- Systematic evaluation of state-of-the-art LLMs across three commonly used modelling frameworks, showing the impact of interface type on accuracy, with Python-based frameworks achieving up to 75% accuracy compared to a maximum of 57.3% for the domain-specific language in zero-shot settings. 

- Adaptation of prompt-based and inference-time compute methods for enhancing LLM-driven constraint modelling, reaching up to 91% accuracy. 

_Publication History._ This version extends the work presented in Michailidis et al. (2025b) in three central directions. Firstly, we expand the benchmark from 101 to 164 problems, also incorporating problems from the ComplexOR dataset and facilitating the inclusion of multiple data instances per problem. Importantly, as some of the original problem instances contained underspecified descriptions or overconstrained ground-truth models (e.g. due to symmetry-breaking constraints), we also manually verified and corrected them<sup>1</sup> in this new version. Secondly, we introduce a Multi-Instance evaluation framework to test model generalization across hidden data instances, with additional experiments showing significantly lower accuracy on the new strictest metric. Thirdly, we evaluate a new generation of LLMs with a final inference-time compute experiment across all three modelling frameworks, showing large improvements in accuracy of all frameworks. Furthermore, more minor changes in the experiments include: a) adding self-verification in the error types experiment (Q2), and b) the addition of "reasoning" as an additional inference-time compute method in Q3. Finally, we added a dedicated section discussing the Related Work. 

1More details on the affected instances can be found in the CP-Bench repository. 

6:4 • Michailidis, Tsouros & Guns 

## **2 Background** 

## **2.1 Constraint Programming** 

We use CP as a formal intermediate representation for the given combinatorial problems. A _Constraint Optimization Problem_ (COP) is a type of combinatorial problem that involves finding an optimal assignment of values to decision variables, subject to a set of constraints and an objective function. Formally, a COP is defined as a tuple (X _,_ D _,_ C _, 𝑓_ ) where: 

- X = { _𝑥_ 1 _,𝑥_ 2 _, . . . ,𝑥𝑛_ } is a set of _𝑛_ decision variables. 

- D = { _𝐷_ 1 _, 𝐷_ 2 _, . . . , 𝐷𝑛_ } is a set of _𝑛_ domains, where each _𝐷𝑖_ is a finite set of allowable values for _𝑥𝑖_ . 

- C = { _𝐶_ 1 _,𝐶_ 2 _, . . . ,𝐶𝑚_ } is a set of _𝑚_ constraints, with each _𝐶 𝑗_ specifying allowed combinations of values for a subset of variables. Formally, _𝐶 𝑗_ ⊆ _𝐷 𝑗_ 1 × _𝐷 𝑗_ 2 × _. . ._ × _𝐷 𝑗𝑘_ for some subset { _𝑥 𝑗_ 1 _,𝑥 𝑗_ 2 _, . . . ,𝑥 𝑗𝑘_ } ⊆ X. 

- _𝑓_ :<sup>�</sup><sup>_𝑛_</sup> _𝑖_ =1<sup>_𝐷𝑖_→R is the objective function to be optimized (either maximized or minimized).</sup> 

The goal is to find an assignment a = { _𝑥_ 1 = _𝑣_ 1 _,𝑥_ 2 = _𝑣_ 2 _, . . . ,𝑥𝑛_ = _𝑣𝑛_ } that satisfies all constraints in C and optimizes the objective function _𝑓_ . Formally, an assignment a is feasible if _𝑣𝑖_ ∈ _𝐷𝑖_ for all _𝑖_ and if ( _𝑣 𝑗_ 1 _, 𝑣 𝑗_ 2 _, . . . , 𝑣 𝑗𝑘_ ) ∈ _𝐶 𝑗_ for each constraint _𝐶 𝑗_ . An optimal solution a<sup>∗</sup> is a feasible assignment that optimizes _𝑓_ . If no objective function _𝑓_ is defined, the problem reduces to a _Constraint Satisfaction Problem_ (CSP), where the goal is to find any feasible assignment. When no feasible assignment exists, the problem is considered unsatisfiable. For brevity, we will use a<sup>∗</sup> to represent either an optimal solution in COPs or a feasible solution in CSPs, and we will commonly refer to it as the _optimal solution_ . 

Notably, CP systems are not restricted to linear constraints but also support a variety of global constraints that capture common patterns in combinatorial problems. These include min/max aggregators, element constraints (for array access), count/nr-values (for aggregation over arrays), cumulative constraints (for scheduling-type problems), and many others that facilitate more expressive modelling of complex problems (Beldiceanu et al. 2007). 

## **2.2 Large Language Models** 

Based on the Transformer architecture (Vaswani et al. 2017), LLMs are deep learning systems, typically with billions of parameters, capable of learning and generating complex language patterns (J. Li et al. 2021). In this work, we use them as black-box text generators, configured only by an input text (or prompt) and a randomness parameter (temperature). Formally: 



Here, _𝑥_ ≤ _𝑡_ denotes the sequence of tokens generated up to time step _𝑡_ , with _𝑥_ ≤0 as the empty sequence and _𝑥_ 1 as the first generated token. At each step, the next token _𝑥𝑡_ +1 is sampled from the temperature-adjusted probability distribution _𝑃𝜏_ ( _𝑥𝑡_ +1 | _𝑝,𝑥_ ≤ _𝑡_ ), which is typically computed by applying the softmax function to the model’s logits—raw unnormalized scores over the vocabulary. The temperature _𝜏_ scales the logits before softmax, with higher values increasing randomness and diversity, while lower values favour the most likely tokens. The generation process continues until a predefined stop token is encountered or the maximum context length is reached. We assume tokenization and detokenization into text are handled internally by the LLM. 

## **3 Problem Formulation** 

As illustrated in Figure 1, we conceptualize a system capable of assisting users in modelling combinatorial problems, transforming their textual descriptions into executable models that a constraint solver can solve. In this paper, we focus on this transformation, which requires a mechanism that can process and accurately represent 

DCP-Bench-Open: Evaluating LLMs for Constraint Modelling of Discrete Combinatorial Problems • 6:5 

the problem’s constraints, variables, and objectives—tasks that demand expert knowledge in both the application domain and CP modelling. We consider LLMs such versatile tools, because of their powerful natural language processing and coding capabilities (M. Chen et al. 2021). 

Formally, we define the process as follows: Let V<sup>∗</sup> represent the set of all possible text sequences composed of tokens from the LLM’s vocabulary V. Let S be the space of all possible valid assignments (solutions) to the decision variables of a discrete combinatorial problem. We utilize the previously defined function _𝐿𝐿𝑀_ , which maps an input prompt<sup>2</sup> _𝑝_ ∈V<sup>∗</sup> and a temperature parameter _𝜏_ ∈ R to an output sequence _𝜋_ ∈V<sup>∗</sup> . Here, _𝜋_ represents an _executable program_ (e.g., a Python script) that encodes the constraint model. Next, we define an execution function _𝑒𝑥𝑒𝑐_ : V<sup>∗</sup> →S ∪{∅ _,𝑒𝑟𝑟𝑜𝑟_ }, which acts as a runtime environment that interprets the program _𝜋_ . The function yields an output a<sup>+</sup> , which represents either an optimal solution a<sup>∗</sup> ∈S, an unsatisfiable result ∅, or some kind of error (e.g., syntax, runtime, solver timeout etc.). The overall system can be represented as follows: 



## **4 Methodology** 

The task for LLMs in this context is to translate problem descriptions into a declarative specification of variables and constraints over them, including expressing them correctly in a specific modelling framework and generating code for printing the computed solution in a structured way. These latter requirements demand coding skills; thus, we take inspiration from successful test-time scaling techniques used for generating imperative code. 

## **4.1 System Prompt** 

Given the complexity of translating natural language descriptions into constraint models, we explore different levels of system prompts to guide LLMs more effectively in a 0-shot setting. Without examples in the prompt (hence 0-shot), providing a comprehensive description of the task is important to help the LLM process and correctly model the problem declaratively. Formally, if _𝑠𝑦𝑠_ ∈V<sup>∗</sup> is the system prompt describing the task, and _𝑐_ ∈V<sup>∗</sup> is the combinatorial problem description, then the LLM input prompt is _𝑝_ = _𝑠𝑦𝑠_ ⊕ _𝑐_ , concatenating the system prompt and the problem description. We examine three levels of system prompts, each progressively providing more detailed information (the prompts are available in the supplementary material): 

- (1) **Basic prompt.** The basic prompt provides essential instructions to the LLM, only describing the task of producing a constraint model using a specific framework and how the solution should be formatted. This prompt simulates a scenario where a user gives minimal guidance, e.g. as one would do in a chat interface. 

- (2) **Guidelines prompt.** Expanding on the basic prompt, this level adds specific guidelines related to the modelling process. These guidelines include code generation steps, generic classroom-style advice on constraint modelling, and a template on how to format the response model in the modelling framework used. It mirrors a situation where a user provides more elaborate but still generic instructions. 

- (3) **Documentation prompt.** The most detailed prompt builds on top of the guidelines prompt, appending single-line API documentation of the available classes and functions of the CP modelling framework. This prompt offers (limited) access to documentation, enabling direct reference to available methods and functionalities. 

The Basic prompt that we used for the CPMpy framework is shown in Listing 1. All system prompts for each level and framework are available in detail in Appendix C. 

> 2We assume that input _𝑝_ includes bothP instructions for a modelling framework and a problem description (which includes a default instance of parameter values for parameterized problems). 

6:6 • Michailidis, Tsouros & Guns 

**Listing 1** Basic System Prompt (Level 1) for the CPMpy framework 

You are an expert in Python, constraint programming, and modelling combinatorial problems. Your task is to model the given problem using the CPMpy library. Specifically, you should generate Python code that uses CPMpy to define and solve the problem. Only the standard Python libraries, CPMpy, and numpy should be used. **# Output Formatting** Here is an example for printing; assume the problem description contains: "Print the number of apples and oranges (apples, oranges), the cost per round (cost), and the total cost (total_cost)." In this case, the output of the solution as JSON should be done as follows: ````` python if model.solve(): # assuming 'apples', 'oranges', 'cost' are variables solution = { 'apples': int(apples.value()), 'oranges': int(oranges.value()), 'cost': cost.value().tolist(), 'total_cost': int(model.objective_value()) } print(json.dumps(solution)) else: print("No solution found.") ````` 

## **4.2 In-Context Learning** 

Few-shot prompting is a widely used method that includes task-relevant examples in the input prompt, improving LLM responses without requiring retraining (Brown et al. 2020). However, selecting effective examples is critical, as a static or random set of examples may not align well with diverse inputs (J. Liu et al. 2021; J. Ye et al. 2023). To address this, recent studies have examined dynamically inserting examples in the prompt context based on the current input (X. Ye, Iyer, et al. 2023). In the context of constraint modelling, adding examples of semantically similar problems and their corresponding models has previously improved the accuracy of generated models (Michailidis et al. 2024). 

Formally, this method retrieves from a prebuilt database an ordered set _𝐸_ of _𝑒_ input-output pairs, _𝐸_ = �( _𝑖 𝑗,𝑜 𝑗_ )� _𝑒𝑗_ =1<sup>,basedontheirrelationtothegivenproblem</sup><sup>_𝑐_.Givenadatabaseofproblem-modelpairs,the</sup> retrieval process involves comparing the token embeddings of _𝑐_ with each problem in the database and selecting the _𝑒_ most similar ones using a predefined metric, such as semantic similarity (Chandrasekaran and Mago 2022). The prompt then becomes _𝑝_ = _𝑠𝑦𝑠_ ⊕ _𝐸_ ⊕ _𝑐_ , where the retrieved examples _𝐸_ are placed between the system prompt and the current problem description, as shown in Figure 2. 

## **4.3 Repeated Sampling** 

While enriching the prompt with instructions and examples can enhance the guidance provided to LLMs, it does not fully address the challenge of synthesizing CP models from textual descriptions. By generating a broad distribution of potential solutions, we can increase the probability that at least one candidate is correct. In this direction, we aim to benefit from the probabilistic nature of LLMs through repeated sampling (or self-consistency) (M. Chen et al. 2021). Instead of relying on the single “most probable” output, we increase the temperature 

DCP-Bench-Open: Evaluating LLMs for Constraint Modelling of Discrete Combinatorial Problems • 6:7 



<!-- Start of picture text -->
System Prompt<br>Problem Description Examples Step 1: Retrieve Relevant Examples<br>Constraint Model Database<br>Problem Description<br>Constraint Model<br>LLM Constraint Model<br>Problem Description<br>Step 2: Generate Model<br><!-- End of picture text -->

Fig. 2. Retrieval-augmented few-shot prompting: on-the-fly example retrieval to provide more relevant patterns to the LLM. 

parameter value _𝜏_ , generating multiple candidate models for the same problem description. This strategy exploits the variability in LLM outputs to identify the most consistent model across multiple runs. 

Specifically, we apply _Solution Majority Voting_ for the final selection of the generated model (Olausson et al. 2023). By repeatedly querying the LLM and solving each generated constraint model, we observe and save the solutions they produce; then, the first model yielding the most frequently observed solution is selected. If none of the models produces a solution, we default to the first generated model. The process is outlined in Algorithm 1. 

**Algorithm 1** Sampling with Solution Majority Voting 

**Require:** ( _𝑝,𝑘,𝜏_ ) // Prompt, #Samples, Temperature 1: C _,_ S ←∅ _,_ ∅ // Candidate CP models & solutions 2: **for** _𝑖_ = 1 to _𝑘_ **do** 3: _𝑚𝑖_ ← _𝐿𝐿𝑀_ ( _𝑝,𝜏_ ) // Generate CP model 4: _𝑠𝑖_ ← _𝑆𝑜𝑙𝑣𝑒𝑟_ ( _𝑚𝑖_ ) // Extract the solution 5: C _,_ S ←C ∪{ _𝑚𝑖_ } _,_ S ∪{ _𝑠𝑖_ } 6: **end for** 7: _𝑠_ maj ← most_freq(S) // Find most frequent solution 8: **if** _𝑠_ maj exists **then** 9: **return** C[first_index_of( _𝑠_ maj _,_ S)] 10: **end if** 11: **return** C[1] // Fallback to first candidate model 

## **4.4 Self-Verification** 

Writing semantically and syntactically correct code in a single pass, without the ability to revise previous steps, is a complex task even for experienced programmers. This challenge holds even more for CP modelling, where variables need to be declared before constraints, and constraints should not contradict earlier ones. We expect that the generated models may occasionally contain runtime, modelling or formatting errors. This motivates us to define three criteria that assert the validity of the generated constraint model: 

- **Runtime Integrity:** The generated code executes without errors and correctly utilizes library components. 

- **Model Accuracy:** The decision variables, constraints, and objective function are correctly defined and aligned with the problem description; when the model is executed, the produced solution is valid and optimal. 

- **Solution Output:** The solution is printed in the correct structured format as per the user’s provided instructions. 

6:8 • Michailidis, Tsouros & Guns 

A promising approach to improve the reliability of code generation is to allow LLMs to review, verify, and refine their previous output, effectively mimicking the human debugging process (X. Chen et al. 2023; Weng et al. 2023). 

We composed a _Self-Verification_ base prompt _𝑣_ (Listing 2) that guides the LLM through an evaluation and correction process, instructing it to iteratively assess the model based on the aforementioned criteria. Appended to this prompt are: (a) the system prompt _𝑠𝑦𝑠_ , (b) the problem description _𝑐_ , (c) the model _𝑚_ generated by the LLM in the previous attempt, and (d) its resulting output a<sup>+</sup> when executed, which may be either a solution of the model or a runtime error traceback message. Formally, the full self-verification prompt at iteration _𝑡_ is denoted as _𝑣_ ⊕ _𝑠𝑦𝑠_ ⊕ _𝑐_ ⊕ _𝑚𝑡_ −1 ⊕ a _𝑡_<sup>+</sup> −1<sup>. This process continues until either the LLM determines that the most recent constraint</sup> model _𝑚𝑡_ −1 is correct according to the specified criteria, or a predefined number of iterations is reached; at that point, the latest model is selected. The process is depicted in Figure 3. 

**Listing 2** Base Self-Debug Prompt 

You are an expert in combinatorial optimization and you are asked to verify (or debug) a code snippet that models a combinatorial problem. You will be given a combinatorial problem description with instructions on how to model it, its code formulation according to these instructions, and the code output. Explain the given code, especially elaborating on the decision variables, constraints, and the objective function (if applicable). 

Then, evaluate the code’s correctness in three aspects: 

- (1) **Runtime:** Does the code run successfully without syntax errors, and does it correctly utilize the required libraries? 

- (2) **Model:** Are the decision variables, constraints, and objective function (if applicable) correctly defined? Does the generated solution satisfy the constraints and objective of the given problem description? 

- (3) **Solution Printing:** Does the code print the solution in the required JSON format, with the correct keys and values according to the given instructions? 

If the code is correct, end your response with [[OK]]. If the code is incorrect, provide a corrected version of the code between triple backticks, ensuring the fixed code is self-contained and runnable. End your response with [[FIXED]]. 

Note: Use [[OK]] and [[FIXED]] only once at the end of your response, and only one of them. 

## **5 DCP-Bench-Open** 

The evaluation of LLMs on translating textual problem descriptions into formal CP specifications has so far been limited by the scope and diversity of available datasets. Existing benchmarks, such as NL4Opt (Ramamonjison, H. Li, et al. 2022)–part of a competition at NeurIPS<sup>3</sup> – and _Logic Grid Puzzles_ (LGPs) (Jabrayilzade and Tekir 2020), primarily feature small, domain-specific problems, such as simple linear programming (LP) problems or homogeneous puzzles, as summarized in Table 1. More recently, Singirikonda et al. (2025) presented a crossdomain dataset with MiniZinc models, focusing on CP, LP and Mixed-Integer Programming (MIP) problems as well. 

To address the gap in discrete CP-modelling LLM benchmarks (Michailidis et al. 2024), we introduce **DCPBench-Open**<sup>4</sup> (Michailidis et al. 2025a), whose first version (v0.1.0) contains a collection of 164 discrete combinatorial problems drawn from well-established sources in the research community, as detailed in Table 2. To 

> 3https://neurips.cc/virtual/2022/competition/50079 

> 4https://github.com/DCP-Bench/DCP-Bench-Open. 

DCP-Bench-Open: Evaluating LLMs for Constraint Modelling of Discrete Combinatorial Problems • 6:9 



<!-- Start of picture text -->
Correct Model/Limit Reached<br>Wrong Model Verifier<br>Problem LLM<br>Last Model<br>Description<br>LLM Constraint Model Solution<br>Step 2: Iterative Verification<br>Step 1: Generate Model<br><!-- End of picture text -->

Fig. 3. Iterative Self-Verification: the generated CP model is verified iteratively; both the original problem description and produced solution are also provided back to the LLM. In this work, we use a single LLM for both model generation and verification (thus, self-verification). 

Table 1. Comparison of DCP-Bench-Open v0.1.0 with existing datasets for evaluating LLM-generated constraint models of combinatorial problems. Unique constraints count distinct constraint operators and their argument structures (arity and type, e.g., variable/constant/expression). The number of problems reflects the test subset of each dataset. The drop in some average values is due to the changes and removal of symmtery-breaking constraints during the verification and correction of the original (CP-Bench) ground-truth models towards this new version. 

|**Benchmark**|**#**|**Constraints**||**Decision Varia**|**bles**|**# Unique**|**# Opt.**|
|---|---|---|---|---|---|---|---|
|||**Mean (Median, IQR)**|**Min/Max**|**Mean (Median, IQR)**|**Min/Max**|**Constr.**|**Probs.**|
|**NL4Opt**|289|2.90 (3.0, 1.0)|2/5|2.02 (2.0, 0.0)|2/3|27|All|
|**LGPs**|100|38.47 (38.0, 29.0)|7/69|12.00 (12.0, 0.0)|12/12|8|None|
|**CP-Bench**_[old]_|101|84.76 (13.5, 45.0)|1/2017|51.69 (13.0, 17.3)|3/962|241|30|
|**DCP-Bench-Open**_[new]_|164|69.48 (12.0, 33.5)|1/2463|40.33 (13.0, 25.5)|2/716|349|54|



achieve high quality and diversity, we selected problems from: a) the popular “benchmark library for constraints” CSPLib (Gent and Walsh 1999), b) the examples repository of the CPMpy modelling framework (Guns 2019), c) the extensive repository of Håkan Kjellerstrand (Kjellerstrand 2024), d) a modelling course-based set of problems (Michailidis et al. 2024), and e) a dataset of complex operations research problems (ComplexOR) (Xiao et al. 2024). Notably, we also gathered and integrated multiple data instances for 23 CSPLib problems (in total 167 different instances) to accommodate more robust model evaluation. 

Table 1 highlights the diversity and complexity of DCP-Bench-Open compared to existing benchmarks. It spans optimization and satisfaction problems, with a wide range of decision variables, constraints, and 349 distinct constraint relations. In particular, the number of constraints per problem ranges from 1 to 2463, and the number of variables from 2 to 716, offering a significantly broader scope than NL4Opt and LGPs (Table 1). 

## **5.1 Problem Structure** 

Each dataset problem can be viewed as a self-contained Python file containing all the necessary components for evaluating the modelling capabilities of LLMs, with the following structure: 

- (1) **Metadata:** The source(s) of the problem along with any additional relevant information. 

- (2) **Problem Description:** The original problem statement as provided by the source, with an additional print instruction that specifies the required output structure. 

- (3) **Input Data (optional):** 

6:10 • Michailidis, Tsouros & Guns 

Table 2. Sources for DCP-Bench-Open v0.1.0 which contains 164 problems in total. Selection was based on CPMpy model availability to facilitate evaluation (the ground-truth model is necessary). 

|**Source**|**#**|**Selected Problems**|
|---|---|---|
|CSPLib|39|IDs: 1–3, 5–16, 18–19, 21–24, 26, 28, 32–34, 39, 41, 44, 49–50, 53–54, 56–57, 67,<br>74, 76, 84.|
|CPMpy Examples|16|_bus_scheduling, minesweeper, packing_rectangles, jobshop, knapsack, mario,_<br>_n_puzzle, RCPS, room, send, set_game, sudoku, tsp, agatha, wolf, zebra_.|
|Håkan K.|80|From_3_coins_until_knights_tour_circuit_ (alphabetically), excluding test files.|
|Course|18|All problems from the repository.|
|ComplexOR|11|All discrete problems from the repository.|



   - _Default Instance (Prompt):_ One valid data instance is provided in plain Python syntax (using only built-in types) to the LLM to showcase the input format. 

   - _Test Instances (Hidden):_ A set of diverse hidden data instances (e.g., varying sizes, graph structures, or numerical ranges) may exist for each problem to evaluate model correctness and robustness under different parameters. 

- (4) **Model:** The decision variables, constraints, and objectives (if any) that make up a runnable CP model of the problem, using the CPMpy modelling framework. 

- (5) **Solution Printing:** Solution printing code, following the requirements in the problem description. 

Importantly, only the **Problem Description** and (optionally) the **Default Instance** are provided to the LLM, the remaining components are used exclusively for evaluation. 

## **5.2 Evaluation Metrics** 

As the focus lies on problems that may have more than one optimal solution, it is mandatory to adopt an appropriate metric to evaluate the generated constraint models. Related works have used constraint-level, modellevel, and solution-level accuracy (Michailidis et al. 2024; Ramamonjison, H. Li, et al. 2022). The first two metrics require mapping the decision variables of the generated model with those from the ground-truth model. However, when modelling complex problems, multiple possible viewpoints and formulations of the decision variables are possible, thus making it highly challenging to map variables between the generated and ground-truth models in a correct but generic way. This leads us to opt for **solution-level accuracy** , which measures the correctness of the solution obtained by executing the generated code; correctness is evaluated with respect to the ground-truth model, considering both feasibility and optimality. Additionally, this metric allows for evaluating LLMs on **any** modelling framework desired, as long as a final solution can be printed. 

Formally, let P be the set of _𝑁_ problems in the benchmark. For each problem _𝑝_ ∈P, we utilize a set of test data instances D _𝑝_ = { _𝑑_ 1 _, . . . ,𝑑𝑘_ }, where _𝑑_ 1 represents the default instance provided in the prompt. Let ˆa _𝑝,𝑑_ be the solution produced by executing the LLM-generated model for problem _𝑝_ on data instance _𝑑_ , and let C _𝑝,𝑑_ be the ground-truth constraint model instantiated with _𝑑_ . We define an indicator function I _𝑐𝑜𝑟𝑟𝑒𝑐𝑡_ ( _𝑝,𝑑_ ) which evaluates to 1 if the generated solution satisfies all constraints and (only for optimization problems) achieves the optimal objective value _𝑓_<sup>∗</sup> (·): 

I _𝑐𝑜𝑟𝑟𝑒𝑐𝑡_ ( _𝑝,𝑑_ ) = I<sup>�</sup> aˆ _𝑝,𝑑_ ∈ Sol(C _𝑝,𝑑_ ) ∧ _𝑓_ (aˆ _𝑝,𝑑_ ) = _𝑓_<sup>∗</sup> (C _𝑝,𝑑_ )<sup>�</sup> (3) 

DCP-Bench-Open: Evaluating LLMs for Constraint Modelling of Discrete Combinatorial Problems • 6:11 

To account for the potential imbalance in the number of available data instances across problems, we define three solution-based metrics: 

_1. Single Instance Accuracy (SIA)._ Measures whether the generated constraint model correctly solves the default data instance provided in the context. This serves as an optimistic upper bound on performance. 



_2. Multiple Instance Accuracy (MIA)._ A strict metric requiring the generated model to correctly solve **all** test instances for a given problem. This penalizes generated models that overfit to the prompt’s default example instance. 



_3. Averaged Instance Accuracy (AIA)._ Calculates the accuracy per problem first (for all problem’s instances), then averages across problems. This ensures that problems with large instance sets available do not dominate the metric. 



In our experiments, we use SIA and evaluate the default instance, unless stated otherwise. 

## **6 Experiments** 

In our experiments, we focus on the following questions: 

- **Q1:** How do LLMs perform in generating constraint models across different modelling frameworks? 

- **Q2:** What types of errors appear in the generated constraint models, and how do different system prompts address them? How does self-verification affect runtime errors? 

- **Q3:** What is the impact of inference-time computation methods, such as reasoning, retrieval-augmented in-context learning, repeated sampling, and self-verification, individually and in combination? 

- **Q4:** How robust are the generated models when evaluating over multiple hidden data instances per problem? 

- **Q5:** How do LLMs perform in generating constraint models across different modelling frameworks when using inference-time compute methods? 

## **Experimental Setup** 

Table 3 lists the LLMs used throughout the experiments. We considered covering a range of properties (coding, rank, mixture of experts, number of parameters, open weights/proprietary, context window size, etc.). Specifically, we selected 7 models from the LMSys Chatbot Arena leaderboard based on their size<sup>5</sup> and ranking on coding tasks (Chiang et al. 2024).<sup>6</sup> We used<sup>7</sup> the _OpenAI_<sup>8</sup> , _Together AI_<sup>9</sup> , _Anthropic_<sup>10</sup> , and _DeepSeek_<sup>11</sup> APIs via their Python 

5For instance, Mistral-Small-24B-Instruct-2501 reached only up to 20% accuracy 

> 6As accessed on 28 November 2025, https://lmarena.ai/leaderboard 

> 7The code is available here: https://github.com/kostis-init/CP-Bench 

> 8https://platform.openai.com/docs/api-reference 

> 9https://docs.together.ai/reference 

> 10https://docs.anthropic.com/en/api 

> 11https://platform.deepseek.com/docs 

##### 6:12 • Michailidis, Tsouros & Guns 

client libraries, using Python 3.12. We set the reproducibility seed to 42 for all API calls, and the temperature parameter _𝜏_ to 0 for deterministic outputs, except when applying repeated sampling techniques, where we increased it to _𝜏_ = 0 _._ 8 for variability, following existing works (Olausson et al. 2023). Notably, some LLMs do not support setting the temperature parameter (e.g. gpt-5.1), thus relying on their internal variability for sampling. Additionally, we set output token limit per answer to 12k. 

For executing the generated constraint models, we used a 10-second timeout due to the small instance sizes of the problems. Specifically, all data instances selected for the multiple instance experiments (Q4 and Q5) are solved under 5 seconds using the ground-truth model. For the final experiment, we increased the generated model time limit to 30 minutes, to account for instances that were slower to solve with some frameworks. Finally, all experiments were conducted on an Ubuntu 24.04.3 system with 32GB RAM and an Intel Core Ultra 7 165Hx22 processor. 

Table 3. LLMs used in the experiments. Parameter counts and context sizes are approximate, active parameters for Mixtureof-Experts models are denoted in parentheses, and N/A means we found no public information about it. 

|**LLM**|**Organization**|**# Parameters(Active)**|**Context Size**|**API Provider**|
|---|---|---|---|---|
|gpt-5.1-2025-11-13|OpenAI|N/A|400k|OpenAI|
|gpt-oss-120B|OpenAI|117B (5.1B)|200k|Together AI|
|DeepSeek-V3.2|DeepSeek|685B (37B)|128k|DeepSeek|
|Qwen3-Coder-480B-A35B|Alibaba|480B (35B)|256k|Together AI|
|Qwen3 235B A22B Instruct 2507|Alibaba|235B (22B)|262k|Together AI|
|Kimi K2 Instruct|Moonshot AI|1T (32B)|256k|Together AI|
|Cogito v2.1 671B|Deep Cogito|671B (37B)|128k|Together AI|



## **Q1: Modelling Frameworks** 

Figure 4 presents the detailed accuracy breakdown, while Figure 5 illustrates the aggregated results across all LLMs for each modelling framework (MiniZinc, CPMpy, and OR-Tools CP-SAT) under different system prompt levels. 

The aggregated results indicate that the choice of modelling framework significantly influences LLM success rates. When instructed to utilise CPMpy, LLMs exhibit consistently higher performance compared to MiniZinc and (slightly) OR-Tools, particularly when supplied with detailed system prompts (Levels 2 and 3). This gap is likely attributable to two factors. First, contemporary LLMs are trained on vast corpora of Python code (M. Chen et al. 2021); this familiarity with Python syntax facilitates the generation of syntax error-free constraint models in Python-based frameworks (CPMpy and OR-Tools). Second, CPMpy offers higher-level modelling abstractions—such as nested expressions, double reification, and a large set of built-in global constraints and global functions, which simplify the translation from natural language specifications to code. 

Analyzing the individual LLM performance across frameworks (Figure 4) reveals distinct patterns for each framework: 

**MiniZinc:** The code-specialized Qwen3-Coder significantly outperforms other models, achieving a peak accuracy of 57.3%. Notably, Qwen3-Coder and Kimi-K2-I are the only models that gain substantial benefit from the inclusion of documentation (Level 3). For other LLMs, added documentation fails to increase accuracy. This suggests that for domain-specific languages like MiniZinc, which also have limited presence in pre-training data, code-specialized LLMs with explicit syntax documentation yield higher accuracies. 

DCP-Bench-Open: Evaluating LLMs for Constraint Modelling of Discrete Combinatorial Problems • 6:13 



Fig. 4. Percentages of successfully generated models (Single Instance Accuracy). From top to bottom: MiniZinc, CPMpy, OR-Tools. 

**CPMpy:** In contrast, results for CPMpy show higher consistency. Performance is evenly distributed, with a narrow variance between the lowest performing models (Kimi and Cogito at 66.5%) and the top performers 

6:14 • Michailidis, Tsouros & Guns 



Fig. 5. Average Single Instance Accuracy by Framework and System Prompt Level (Aggregated across LLMs). 

(gpt-5.1 and DeepSeek-V3.2 at roughly 70.1%). This consistency is present only under the documentation prompt (Level 3), at which LLM choice seems to become a less critical factor than in other frameworks. 

**OR-Tools:** OpenAI’s LLMs are leading with gpt-oss-120b achieving the highest overall accuracy (75.0%), closely surpassing gpt-5.1 (71.3%). Conversely, Qwen3-Coder, despite its dominance in MiniZinc, struggles significantly with OR-Tools (max ∼55.5%). Interestingly, this also comes in contrast with gpt-oss-120b, which excels at OR-Tools but vastly underperforms in MiniZinc. 

In summary: a) generating constraint models using Python libraries tends to yield higher accuracy than the domain-specific MiniZinc language, and b) the documented high-level framework (CPMpy with documentation prompt) show the highest consistency in accuracy over all LLMs tested (>60%). 

## **Q2: System Prompt & Error Types** 

Figures 4 and 5 also demonstrate the impact of varying system prompt levels across frameworks and LLMs. A key observation across all configurations is that providing at least some specific guidance — either classroom-level guidelines (Level 2) or framework documentation (Level 3) — consistently yields higher accuracy than the basic prompt (Level 1). However, the addition of detailed documentation on top of the guidelines showed some variations. For the Python-based frameworks (CPMpy, OR-Tools), API documentation in the system prompts is beneficial to produce valid constraint models, as it led to an increase in accuracy for 5 and 4 (respectively) out of the 7 LLMs tested. Similarly, Interestingly, for MiniZinc, while adding guidelines (Level 2) improved performance over the baseline (Level 1) for all LLMs, further adding detailed documentation (Level 3) did not consistently improve upon Level 2. In fact, average performance slightly decreased, with only 2 out of 7 LLMs showing any benefit from the extra documentation on MiniZinc. 

To understand _why_ models fail, we categorize failures into two distinct types: **Detectable Errors** (syntax errors, invalid API usage, or running into timeouts) and **Modelling Errors** (the code executes but yields incorrect solutions or unsatisfiable models). For CPMpy, depicted in Figure 6, as the prompt level increases, detectable errors decrease while modelling errors rise. A similar trend was observed for MiniZinc and OR-Tools (figures are available in Appendix B). The reduction in detectable errors with more detailed prompts suggests that LLMs generate more syntactically correct and executable code as they receive more information. This partly leads to more successes, but at times also to an increase in logical modelling errors (bottom subfigure), where the code is syntactically correct but the solution is either incorrect or not found. 

DCP-Bench-Open: Evaluating LLMs for Constraint Modelling of Discrete Combinatorial Problems • 6:15 



Fig. 6. Detectable and modelling errors with CPMpy. 3+SV stands for Self-Verification of a single repetition along with a system prompt level 3 (documentation). Importantly, the (green) bars for level 3 represent the same experimental runs as 3+SV (red), but report the errors prior to the self-verification iteration, for reproducibility. 

_Self-Verification._ To further reduce the number of detectable errors, we also report a comparison with SelfVerification (SV) being used on top of the documentation prompt (Figure 6, label 3+SV). Results show the positive effect of Self-Verification, even on only 1 single repetition. Across nearly all LLMs, SV significantly reduces detectable errors compared to a pure documentation-rich prompt. For instance, gpt-5.1 reduces detectable errors from 19 to 5, and Qwen3-Coder from 30 to 16. This indicates that LLMs are capable of interpreting error tracebacks to fix their own syntax and API misuse. However, the impact on modelling errors is mixed. For stronger models like gpt-5.1 and Qwen3-Coder, SV reduces both error types, suggesting full improvement, but for models like Kimi-K2-I, SV reduces detectable errors (from 37 to 16) but nearly doubles modelling errors (from 17 to 31). These results indicate a correlation between the reduction in detectable errors and the increase in modelling errors, where the initial runtime error may be corrected but nonetheless result in a logical modelling error. 

## **Q3: Inference-Time Compute Methods** 

We assess the impact of various inference-time compute strategies introduced in Section 4, with the following configurations: 

- (1) **Baseline** (Section 4.1): The input consists of the system prompt and problem description. The first generated model is directly evaluated without further processing, as in Q1. 

- (2) **RAICL** (Section 4.2): The input contains the system prompt and _𝑒_ = 8 examples based on reverse semantic similarity, following existing work (Michailidis et al. 2024). We use a leave-one-out strategy for evaluation, testing each problem individually while utilizing the 100 remaining ones as the retrieval database. 

- (3) **Reasoning** : We investigate internal "reasoning" as a test-time method for improving model generation. Depending on the model, this involves either prompting for "Low Reasoning Effort" (gpt-5.1, gpt-oss, Qwen3-Coder) or utilizing a reasoning-specialized variant (e.g., DeepSeek-Reasoner, Kimi-Thinking). 

6:16 • Michailidis, Tsouros & Guns 

- (4) **Sampling** (Section 4.3): Generation of _𝑘_ = 10 responses in parallel, with the final model selected via solution majority voting. The input consists of the system prompt and problem description. 

- (5) **Self-Verification** (Section 4.4): Iterative refinement of the Baseline generation through the self-verification loop, with a maximum of 10 iterations. 

- (6) **Sampling & Self-Verification** : A hybrid approach where the output selected by Sampling is subsequently refined via Self-Verification. Again, we use 10 samples and maximum 10 iterations. 

We included five LLMs (those that benefit from the Level 3 Documentation prompt): _gpt-5.1_ , _gpt-oss_ , _DeepSeek-V3.2_ , _Qwen3-Coder_ , _Kimi-K2_ , and we used CPMpy due to its higher accuracy on average (Q1). Based on the Q2 results, we used the documentation system prompt (Level 3). The results are summarized in Figure 7. 



Fig. 7. Performance (Single Instance Accuracy) across different inference-time compute methods for each LLM using CPMpy. 

_Baseline & RAICL._ Surprisingly, the RAICL strategy was shown ineffective for most LLMs or occasionally slightly effective. For most models, including DeepSeek-V3.2, Qwen3-Coder, and Kimi-K2, performance degraded when retrieval-augmented in-context examples were provided compared to the zero-shot Baseline. Based on these results and compared to the results from Michailidis et al. (2024), it seems that for formal constraint modelling, LLMs may utilize the structured framework documentation in the system prompt more effectively than they generalize from retrieved, problem-specific specific model examples provided in context. This finding also can simplify practical deployment by removing the need for custom example databases and dynamic retrieval methods. As such, investigating more modelling tools or frameworks could start on merely adapting their documentation for the system prompt. 

_Reasoning._ The "Low Reasoning" strategy showed high variance accross LLMs. While _gpt-5.1_ showed substantial gains, suggesting its internal reasoning chain benefits constraint formulation, other models such as _gpt-oss_ and _Kimi-K2_ saw roughly 5-10% performance drops. As such, "reasoning" LLMs on their own are not yet an absolute enhancement for formal modelling. 

_Sampling & Self-Verification._ These methods boosted performance across all LLMs (more than 10% increase in accuracy), with the most significant gains observed by Kimi-K2, which increased accuracy by roughly 20% compared to the Baseline. Notably, with repeated sampling, open-source LLMs managed to slightly outperform OpenAI’s larger LLM (gpt-5.1). Self-verification also improved accuracy significantly compared to the Baseline, 

DCP-Bench-Open: Evaluating LLMs for Constraint Modelling of Discrete Combinatorial Problems • 6:17 

yielding results comparable to repeated sampling, although Kimi-K2 performed slightly better with sampling than with self-verification alone. As RAICL and Reasoning failed to improve accuracy consistently across all LLMs, we experimented with the combination of the two best-performing methods: repeated sampling & selfverification. This combined approach further increased accuracy, with all LLMs tested demonstrating their highest performance in this setting, reaching up to 91% accuracy (gpt-5.1); only 2 instances resulted in detectable errors (1 runtime error, 1 wrong solution format generation), and 13 instances resulted in modelling errors (unsatisfiable or wrong solution). 

## **Q4: Multiple Data Instances** 



Fig. 8. Comparison of model reliability metrics when all instances per problem are evaluated (only using problems that have more than 1 data instance). **Single Instance Accuracy** (optimistic) measures success on the prompt’s default example. **Multiple Instance Accuracy** (strict) requires success on all hidden instances. 

To evaluate model generalization and robustness, we compared the performance of generated models on the default instance provided in the prompt versus a set of hidden test instances. In this experiment, the input prompt explicitly defines the expected data structure and parameter types by including the default instance. Crucially, the prompt instructs the LLM to generate a model that assumes these parameter values are pre-loaded into the namespace, thereby allowing to use the same generated model for all the hidden instances of the problem. We restricted this evaluation to only problems containing multiple data instances, resulting in a subset of 23 problems with 167 total instances. Figure 8 shows the gap between Single Instance Accuracy (SIA), Averaged Instance Accuracy (AIA), and Multiple Instance Accuracy (MIA). 

Across all evaluated LLMs, we observe a consistent performance decline when moving from the single default instance to the full instance set. While gpt-5.1 and Kimi-K2-I achieve the highest performance across all metrics (SIA: 78.3%, MIA: 60.9%), they both still show a 17.4% drop in strict robustness. Notably, despite gpt-oss-120b and Qwen3-Coder achieving an SIA of 69.6%, their MIA drops to 47.8%, a relative decrease of over 30%. The smallest decline was observed with DeepSeek-V3.2, which dropped by only 8.7%. These results suggest that LLMs frequently overfit to the specific values or structure of the default data instance provided in the prompt (e.g., 

6:18 • Michailidis, Tsouros & Guns 

Table 4. Impact of inference-time compute on Single-Instance Accuracy across frameworks. The Baseline uses the Level 3 documentation prompt with problem data included directly in the prompt context. The Inference-Time Compute (ITC) method employs Repeated Sampling ( _𝑘_ = 10) combined with Self-Verification (max 10 iterations)-as in the combined method in Q3-and loads problem data externally. 

|||**gpt-5.1-2025-11-13**||**Kimi K2 Instruct**|
|---|---|---|---|---|
|**Framework**|Baseline|Sampling & Self-Verification|Baseline|Sampling & Self-Verification|
|MiniZinc|37.8%|**73.2%**|49.4%|**72.0%**|
|CPMpy|70.1%|**90.2%**|66.5%|**89.0%**|
|OR-Tools|68.9%|**88.4%**|64.0%|**82.3%**|





Fig. 9. Comparison of accuracy for all frameworks and all multi-instance problems (23) when all instances per problem are evaluated using the combined Sampling & Self-Verification method with the Documentation Prompt. For this experiment, a timeout of 30 minutes was set for executing each generated model. From left to right: MiniZinc, CPMpy, OR-Tools. 

hardcoding array sizes or assuming specific domain ranges) rather than modelling the abstract constraints of the problem. Multiple Instance Accuracy can indeed serve as a stricter correctness metric in this domain. 

## **Q5: Multi-Instance Evaluation with Inference-Time Compute** 

Finally, we integrate our findings by evaluating the strongest configuration—Sampling ( _𝑘_ = 10) combined with Self-Verification ( _𝑖_ = 10) using the Documentation Prompt—on the full dataset across all modelling frameworks. As in the previous experiment (Q4), problem data is loaded externally rather than being hardcoded in the prompt. 

As shown in Table 4, **applying inference-time compute yields impressive improvements over the baseline across all frameworks** . For CPMpy, Single Instance Accuracy increases from 70.1% to 90.2% for gpt-5.1, and from 66.5% to 89.0% for Kimi-K2. Similar gains are observed for OR-Tools (∼20% increase) and MiniZinc (∼35% increase for gpt-5.1). 

Regarding multi-instance robustness, Figure 9 shows a similar trend to Q4, where there are still several occurrences of models that correctly solve the default instance but fail on all hidden ones. As in Q4, in this experiment we again only included the 23 problems that contain more than one instance in the dataset, and we set the timeout limit to 30 minutes. Notably, both the highest MIA and the smallest relative decline is observed when modelling with CPMpy, closely followed by OR-Tools with gpt-5.1, and MiniZinc with Kimi-K2. After close 

DCP-Bench-Open: Evaluating LLMs for Constraint Modelling of Discrete Combinatorial Problems • 6:19 

inspection upon the specific error types in hidden instances when the default one is solved correctly, we found that the majority of them for CPMpy and OR-Tools were that either the generated solution was incorrect or the model unsatisfiable. In contrast, for MiniZinc, code execution errors and wrong solutions were more common, followed by model timeouts (the detailed numbers are shown in Appendix A). 

## **7 Related Work** 

_Inference-Time Compute and Scaling._ Recent LLM literature has shifted from scaling model parameters during pre-training to scaling computational resources at inference time. Snell et al. (2024) demonstrated that optimally scaling test-time compute can allow smaller models to outperform significantly larger ones. Muennighoff et al. (2025) categorizes test-time scaling into two dimensions: parallel and sequential scaling. Parallel scaling involves generating independent candidate solutions and selecting the most likely correct answer through methods like Majority Voting (or Self-Consistency decoding) (X. Wang et al. 2022), including also massive parallel sampling for solving competitive programming tasks (AlphaCode) (Y. Li et al. 2022). Sequential scaling, by contrast, allocates compute to iterative refinement, enabling LLMs to self-correct syntax and logical errors when provided with execution feedback from an interpreter or unit test results (X. Chen et al. 2023; Madaan et al. 2023). More recently, hybrid frameworks have emerged to combine these two dimensions, such as S*, which incorporates a self-debugging chain in each unique sample (D. Li et al. 2025). Furthermore, reasoning-native models such as DeepSeek-R1 have internalized these processes through large-scale reinforcement learning, enabling backtracking and "thinking" tokens before producing a final response (Guo et al. 2025). 

_LLMs for Formal Modelling and Optimization._ Early works on transforming natural language inputs into formal optimization models were motivated by the NL4Opt competition (Ramamonjison, Yu, et al. 2023), with various succesfull approaches on both entity recognition (Dakle et al. 2023) and model generation (Prasath and Karande 2023). More recent neuro-symbolic methods utilize LLMs to translate textual problem descriptions into various declarative representations for symbolic solvers, spanning Satisfiability (SAT) formulas (X. Ye, Q. Chen, et al. 2023), First-Order Logic (Olausson et al. 2023), Answer Set Programming (Ishay et al. 2023), Mixed-Integer Programming (MIP) (AhmadiTeshnizi et al. 2023), and PDDL for planning (B. Liu et al. 2023). Specifically for CP modelling, we have explored decomposition-based pipelines (Tsouros et al. 2023) and retrieval-augmented in-context learning with intermediate blueprint model representations (Michailidis et al. 2024). Additionally, Shi et al. (2025) present a modelling approach based on supervised fine-tuned LLMs, while Szeider (2025) and Cai et al. (2025) investigate agentic-based frameworks for CP modelling. Finally, distinct from pure modelling, Voboril et al. (2025) introduce an LLM-based method to generate streamlining constraints that accelerate the solving process. 

_Existing Formal Modelling Benchmarks._ The evaluation of LLMs for optimization has primarily focused on Linear Programming (LP) and Mixed-Integer Programming (MIP). Early works like NL4Opt (Ramamonjison, Yu, et al. 2023) targeted entity extraction and formulation for small and homogeneous linear problems. More recent benchmarks such as NLP4LP (AhmadiTeshnizi et al. 2023), MAMO (Huang et al. 2024), IndustryOR (Tang et al. 2024), BWOR (B. Zhang and Luo 2025), ComplexOR (Xiao et al. 2024), and CO-Bench (W. Sun et al. 2025) expanded this scope to textbook and industrial operations research problems. To the best of our knowledge, in the domain of Constraint Programming, benchmarks remain limited. Parallel efforts include: CPEval (Y. Song and Cohen 2025) and IndusCP (Shi et al. 2025) which offer datasets of classic problems derived from various well-established sources, and Text2Zinc (Singirikonda et al. 2025) which introduces a cross-domain dataset containing CP, LP, and MIP problems with MiniZinc ground-truth models. Our DCP-Bench-Open complements these efforts by focusing specifically on discrete combinatorial problems, allowing for _modelling framework-independent_ multi-instance and multi-solution evaluation. 

6:20 • Michailidis, Tsouros & Guns 

## **8 Conclusion** 

In this work, we collected a diverse dataset of discrete combinatorial problems and systematically evaluated various state-of-the-art LLMs on transforming textual problem descriptions into executable constraint models. We explored the use of different modelling frameworks, with varying abstraction and interface types. We also explored the use of prompt-based and inference-time compute methods for enhancing the performance of LLMs in constraint modelling. 

Our evaluation indicated an advantage of Python-based frameworks (CPMpy, OR-Tools) compared to the domain-specific MiniZinc language, with further improvements when appending detailed guidelines and documentation in system prompts. Inference-time methods were shown to provide a significant improvement in general, with repeated sampling and self-verification showing up to a 35% increase in accuracy (MiniZinc). Notably, retrieval-augmented in-context learning was not consistently effective when combined with increased documentation in the prompts, and considering also its requirement for constructing example databases and selection strategies, suggests practical challenges for it in this domain. The strongest performance came from combining repeated sampling and self-verification with the documentation prompt, achieving up to 90% accuracy on CPMpy modelling, suggesting that LLMs can indeed assist in the modelling process. Our multi-instance evaluation does show that LLMs can over-encode the example instance given in the prompt, leading to incorrect results on other instances of the same problem type. Further work on multi-instance aware prompting, for example, multi-instance inference time computation could remedy this. 

The existence of DCP-Bench-Open allows for systematically evaluating additional design choices, including newer LLMs, additional modeling or solving frameworks (e.g., different CP solvers, or directly modeling for integer linear programming solvers or SAT solvers), more coding LLM techniques (e.g. retrieval-augmented documentation), or supervised fine-tuning of LLMs. The latter would require a training dataset of constraint models and problem descriptions, in addition to the use of DCP-Bench-Open as evaluation dataset. While our benchmark contains diverse and realistic combinatorial problems, they often originate from textbooks. Large-scale industrial problems typically involve more data, many constraints and objectives, and elaborate descriptions, though these are rarely publicly available. Future work could also explore multi-turn interactions for modelling with LLMs, where a user and system iteratively refine the model through conversation and trial-and-error. Finally, while this paper focused on evaluating model correctness, adding more instances in DCP-Bench-Open is straightforward. This opens the door to also evaluating modeling efficiency across multiple instances, allowing in turn to connect to LLM-driven multiple model generation, model selection based on efficiency as well as solver selection and algorithm configuration. 

## **Acknowledgments** 

This project has received funding from the European Research Council (ERC) under the European Union’s Horizon 2020 research and innovation program (Grant No. 101002802, CHAT-Opt), and from the Flemish Government under “Onderzoeksprogramma Artificiële Intelligentie (AI) Vlaanderen”. 

## **References** 

> A. AhmadiTeshnizi, W. Gao, and M. Udell. 2023. “Optimus: Optimization modeling using mip solvers and large language models.” _arXiv preprint arXiv:2310.06116_ . 

> N. Beldiceanu, M. Carlsson, S. Demassey, and T. Petit. 2007. “Global constraint catalogue: Past, present and future.” _Constraints_ , 12, 21–62. 

> C. Bessiere, C. Carbonnel, et al.. 2023. “Learning constraints through partial queries.” _Artif. Intell._ , 319, 103896. doi:10.1016/j.artint.2023.103896. 

> C. Bessiere, R. Coletta, B. O’Sullivan, M. Paulin, et al.. 2007. “Query-Driven Constraint Acquisition.” In: _IJCAI_ . Vol. 7, 50–55. 

> T. Brown et al.. 2020. “Language models are few-shot learners.” _Advances in neural information processing systems_ , 33, 1877–1901. 

> J. Cai, S. Kadioglu, and B. Dilkina. 2025. “Gala: Global LLM Agents for Text-to-Model Translation.” _arXiv preprint arXiv:2509.08970_ . 

> Q. Cappart, T. Guns, M. Lombardi, G. Pesant, and D. Tsouros. 2025. “Combining Constraint Programming and Machine Learning: From Current Progress to Future Opportunities.” _Journal of Artificial Intelligence Research_ , 84. 

DCP-Bench-Open: Evaluating LLMs for Constraint Modelling of Discrete Combinatorial Problems • 6:21 

- D. Chandrasekaran and V. Mago. Feb. 2022. “Evolution of Semantic Similarity - A Survey.” _ACM Comput. Surv._ , 54, 2, Article 41, (Feb. 2022), 41:1–41:37. doi:10.1145/3440755. 

- M. Chen et al.. 2021. “Evaluating large language models trained on code.” _arXiv preprint arXiv:2107.03374_ . 

- X. Chen, M. Lin, N. Schaerli, and D. Zhou. 2023. “Teaching Large Language Models to Self-Debug.” In: _The 61st Annual Meeting Of The Association For Computational Linguistics_ . 

- W.-L. Chiang et al.. 2024. _Chatbot Arena: An Open Platform for Evaluating LLMs by Human Preference_ . (2024). arXiv: 2403.04132 (cs.AI). 

- P. P. Dakle, S. Kadioglu, K. Uppuluri, R. Politi, P. Raghavan, S. Rallabandi, and R. Srinivasamurthy. 2023. “Ner4Opt: Named Entity Recognition for Optimization Modelling from Natural Language.” In: _Integration of Constraint Programming, Artificial Intelligence, and Operations Research - 20th International Conference, CPAIOR 2023, Nice, France, May 29 - June 1, 2023, Proceedings_ (Lecture Notes in Computer Science). Ed. by A. A. Ciré. Vol. 13884. Springer, Cham, 299–319. isbn: 978-3-031-33271-5. doi:10.1007/978-3-031-33271-5_20. 

- Z. Fan, X. Gao, M. Mirchev, A. Roychoudhury, and S. H. Tan. 2023. “Automated repair of programs from large language models.” In: _2023 IEEE/ACM 45th International Conference on Software Engineering (ICSE)_ . IEEE, 1469–1481. 

- E. C. Freuder. 2018. “Progress towards the Holy Grail.” _Constraints An Int. J._ , 23, 2, 158–171. doi:10.1007/s10601-017-9275-0. 

- E. C. Freuder and B. O’Sullivan. 2014. “Grand challenges for constraint programming.” _Constraints An Int. J._ , 19, 2, 150–162. doi:10.1007/s10601 -013-9155-1. 

- A. M. Frisch, C. Jefferson, B. M. Hernández, and I. Miguel. 2005. “The rules of constraint modelling.” In: _IJCAI_ , 109–116. 

- I. P. Gent and T. Walsh. 1999. “CSPlib: A Benchmark Library for Constraints.” In: _Principles and Practice of Constraint Programming – CP’99_ . Ed. by J. Jaffar. Springer Berlin Heidelberg, Berlin, Heidelberg, 480–481. isbn: 978-3-540-48085-3. 

- T. Guns. 2019. “Increasing modeling language convenience with a universal n-dimensional array, CPpy as python-embedded example.” In: _Proceedings of the 18th workshop on Constraint Modelling and Reformulation at CP (Modref 2019)_ . Vol. 19. 

- D. Guo et al.. 2025. “Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning.” _arXiv preprint arXiv:2501.12948_ . 

- X. Huang, Q. Shen, Y. Hu, A. Gao, and B. Wang. 2024. _Mamo: a Mathematical Modeling Benchmark with Solvers_ . (2024). arXiv: 2405.13144 (cs.AI). 

- A. Ishay, Z. Yang, and J. Lee. 2023. “Leveraging Large Language Models to Generate Answer Set Programs.” In: _Proceedings of the International Conference on Principles of Knowledge Representation and Reasoning_ . Vol. 19, 374–383. 

- E. Jabrayilzade and S. Tekir. 2020. “Lgpsolver-solving logic grid puzzles automatically.” In: _Findings of the Association for Computational Linguistics: EMNLP 2020_ , 1118–1123. 

- J. Jiang, F. Wang, J. Shen, S. Kim, and S. Kim. 2024. “A survey on large language models for code generation.” _arXiv preprint arXiv:2406.00515_ . 

- Z. Kiziltan, M. Lippi, P. Torroni, et al.. 2016. “Constraint detection in natural language problem descriptions.” In: _IJCAI_ . Vol. 2016. International Joint Conferences on Artificial Intelligence, 744–750. 

- H. Kjellerstrand. 2024. _Håkan’s CPMpy Examples Repository_ . Accessed: 2024-12-24. (2024). http://www.hakank.org/cpmpy/. 

- C. Lecoutre and N. Szczepanski. 2020. “PYCSP3: modeling combinatorial constrained problems in python.” _arXiv preprint arXiv:2009.00326_ . 

- D. Li, S. Cao, C. Cao, X. Li, S. Tan, K. Keutzer, J. Xing, J. E. Gonzalez, and I. Stoica. Nov. 2025. “S*: Test Time Scaling for Code Generation.” In: _Findings of the Association for Computational Linguistics: EMNLP 2025_ . Ed. by C. Christodoulopoulos, T. Chakraborty, C. Rose, and V. Peng. Association for Computational Linguistics, Suzhou, China, (Nov. 2025), 15964–15978. isbn: 979-8-89176-335-7. doi:10.18653/v1/2025.findin gs-emnlp.865. 

- J. Li, T. Tang, W. X. Zhao, and J. Wen. 2021. “Pretrained Language Model for Text Generation: A Survey.” In: _Proceedings of the Thirtieth International Joint Conference on Artificial Intelligence, IJCAI 2021, Virtual Event / Montreal, Canada, 19-27 August 2021_ . Ed. by Z. Zhou. ijcai.org, 4492–4499. doi:10.24963/ijcai.2021/612. 

- Y. Li et al.. 2022. “Competition-level code generation with alphacode.” _Science_ , 378, 6624, 1092–1097. 

- B. Liu, Y. Jiang, X. Zhang, Q. Liu, S. Zhang, J. Biswas, and P. Stone. 2023. “Llm+ p: Empowering large language models with optimal planning proficiency.” _arXiv preprint arXiv:2304.11477_ . 

- J. Liu, D. Shen, Y. Zhang, B. Dolan, L. Carin, and W. Chen. 2021. “What Makes Good In-Context Examples for GPT-3?” _arXiv preprint arXiv:2101.06804_ . 

- A. Madaan et al.. 2023. “Self-refine: Iterative refinement with self-feedback.” _Advances in Neural Information Processing Systems_ , 36, 46534– 46594. 

- Y. Mechqrane, C. Bessiere, and I. Elabbassi. 2024. “Using large language models to improve query-based constraint acquisition.” In: _IJCAI 2024-33rd International Joint Conference on Artificial Intelligence_ , 1916–1925. 

- K. Michailidis, D. Tsouros, and T. Guns. 2025a. _DCP-Bench-Open_ . Zenodo. doi:10.5281/zenodo.17800138. 

- K. Michailidis, D. Tsouros, and T. Guns. 2024. “Constraint modelling with LLMs using in-context learning.” In: _30th International conference on principles and practice of constraint programming_ . 

- K. Michailidis, D. Tsouros, and T. Guns. 2025b. “CP-Bench: Evaluating Large Language Models for Constraint Modelling.” _arXiv preprint arXiv:2506.06052_ . Full version of this paper. 

- N. Muennighoff et al.. 2025. “s1: Simple test-time scaling.” In: _Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing_ , 20286–20332. 

6:22 • Michailidis, Tsouros & Guns 

- N. Nethercote, P. J. Stuckey, R. Becket, S. Brand, G. J. Duck, and G. Tack. 2007. “MiniZinc: Towards a standard CP modelling language.” In: _International conference on principles and practice of constraint programming_ . Springer, 529–543. 

- T. Olausson, A. Gu, B. Lipkin, C. Zhang, A. Solar-Lezama, J. Tenenbaum, and R. Levy. 2023. “LINC: A Neurosymbolic Approach for Logical Reasoning by Combining Language Models with First-Order Logic Provers.” In: _Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing_ , 5153–5176. 

- V. T. Paschos. 2014. _Applications of combinatorial optimization_ . John Wiley & Sons. 

- L. Perron and F. Didier. 2024. _CP-SAT_ . Version v9.10. Accessed: 2025-5-5. Google, (2024). https://developers.google.com/optimization/cp/cp_so lver. 

- L. Perron and V. Furnon. 2024. _OR-Tools_ . Version v9.10. Accessed: 2025-5-5. Google, (2024). https://developers.google.com/optimization/. 

- G. Prasath and S. Karande. Mar. 30, 2023. “Synthesis of Mathematical programs from Natural Language Specifications.” _CoRR_ , abs/2304.03287, arXiv:2304.03287, (Mar. 30, 2023). arXiv: 2304.03287. doi:10.48550/arXiv.2304.03287. 

- R. Ramamonjison, H. Li, T. T. L. Yu, S. He, V. Rengan, A. Banitalebi-Dehkordi, Z. Zhou, and Y. Zhang. Oct. 11, 2022. “Augmenting Operations Research with Auto-Formulation of Optimization Models from Problem Descriptions.” _CoRR_ , abs/2209.15565, arXiv:2209.15565, (Oct. 11, 2022). arXiv: 2209.15565. doi:10.48550/arXiv.2209.15565. 

- R. Ramamonjison, T. Yu, et al.. 2023. “Nl4opt competition: Formulating optimization problems based on their natural language descriptions.” In: _NeurIPS 2022 Competition Track_ . PMLR, 189–203. 

- W. Shi, M. Liu, W. Zhang, L. Shi, F. Jia, F. Ma, and J. Zhang. Nov. 2025. “ConstraintLLM: A Neuro-Symbolic Framework for IndustrialLevel Constraint Programming.” In: _Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing_ . Ed. by C. Christodoulopoulos, T. Chakraborty, C. Rose, and V. Peng. Association for Computational Linguistics, Suzhou, China, (Nov. 2025), 16010–16030. isbn: 979-8-89176-332-6. doi:10.18653/v1/2025.emnlp-main.809. 

- H. Simonis. 1999. “Building Industrial Applications with Constraint Programming.” In: _Constraints in Computational Logics: Theory and Applications, International Summer School, CCL’99 Gif-sur-Yvette, France, September 5-8, 1999, Revised Lectures_ (Lecture Notes in Computer Science). Vol. 2002. Springer, 271–309. doi:10.1007/3-540-45406-3_6. 

- A. Singirikonda, S. Kadioglu, and K. Uppuluri. 2025. “TEXT2ZINC: A Cross-Domain Dataset for Modeling Optimization and Satisfaction Problems in MINIZINC.” _arXiv preprint arXiv:2503.10642_ . 

- C. Snell, J. Lee, K. Xu, and A. Kumar. 2024. “Scaling llm test-time compute optimally can be more effective than scaling model parameters.” _arXiv preprint arXiv:2408.03314_ . 

- Y. Song and E. Cohen. 2025. “Do LLMs Understand Constraint Programming? Zero-Shot Constraint Programming Model Generation Using LLMs.” In: _Proceedings of the 19th Learning and Intelligent Optimization Conference (LION-25)_ , In press. https://openreview.net/forum?id=6 zlpzSKzqj. 

- J. Sun et al.. June 2025. “A Survey of Reasoning with Foundation Models: Concepts, Methodologies, and Outlook.” _ACM Comput. Surv._ , 57, 11, Article 278, (June 2025), 43 pages. doi:10.1145/3729218. 

- W. Sun, S. Feng, S. Li, and Y. Yang. 2025. “CO-Bench: Benchmarking Language Model Agents in Algorithm Search for Combinatorial Optimization.” _ArXiv_ , abs/2504.04310. https://arxiv.org/abs/2504.04310. 

- S. Szeider. 2025. “Cp-agent: Agentic constraint programming.” _arXiv preprint arXiv:2508.07468_ . 

- Z. Tang, C. Huang, X. Zheng, S. Hu, Z. Wang, D. Ge, and B. Wang. 2024. “ORLM: Training Large Language Models for Optimization Modeling.” _arXiv preprint arXiv:2405.17743_ . 

- D. C. Tsouros, H. Verhaeghe, S. Kadioglu, and T. Guns. Aug. 3, 2023. “Holy Grail 2.0: From Natural Language to Constraint Models.” _CoRR_ , abs/2308.01589, arXiv:2308.01589, (Aug. 3, 2023). arXiv: 2308.01589. doi:10.48550/arXiv.2308.01589. 

- A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, Ł. Kaiser, and I. Polosukhin. 2017. “Attention is all you need.” _Advances in neural information processing systems_ , 30. 

- F. Voboril, V. P. Ramaswamy, and S. Szeider. 2025. “Generating streamlining constraints with large language models.” _Journal of Artificial Intelligence Research_ , 84. 

- M. Wallace. 1996. “Practical Applications of Constraint Programming.” _Constraints An Int. J._ , 1, 1/2, 139–168. doi:10.1007/BF00143881. 

- X. Wang, J. Wei, D. Schuurmans, Q. Le, E. Chi, S. Narang, A. Chowdhery, and D. Zhou. 2022. “Self-consistency improves chain of thought reasoning in language models.” _arXiv preprint arXiv:2203.11171_ . 

- Y. Weng, M. Zhu, F. Xia, B. Li, S. He, S. Liu, B. Sun, K. Liu, and J. Zhao. 2023. “Large Language Models are Better Reasoners with Self-Verification.” In: _Findings of the Association for Computational Linguistics: EMNLP 2023_ . Singapore, 2550–2575. doi:10.18653/v1/2023.findings-emnlp.167. 

- Z. Xiao et al.. 2024. “Chain-of-Experts: When LLMs Meet Complex Operations Research Problems.” In: _The Twelfth International Conference on Learning Representations_ . https://openreview.net/forum?id=HobyL1B9CZ. 

- J. Ye, Z. Wu, J. Feng, T. Yu, and L. Kong. 2023. “Compositional exemplars for in-context learning.” In: _International Conference on Machine Learning_ . PMLR, 39818–39833. 

- X. Ye, Q. Chen, I. Dillig, and G. Durrett. 2023. “Satlm: Satisfiability-aided language models using declarative prompting.” _Advances in Neural Information Processing Systems_ , 36, 45548–45580. 

DCP-Bench-Open: Evaluating LLMs for Constraint Modelling of Discrete Combinatorial Problems • 6:23 

- X. Ye, S. Iyer, A. Celikyilmaz, V. Stoyanov, G. Durrett, and R. Pasunuru. July 2023. “Complementary Explanations for Effective In-Context Learning.” In: _Findings of the Association for Computational Linguistics: ACL 2023_ . Ed. by A. Rogers, J. Boyd-Graber, and N. Okazaki. Association for Computational Linguistics, Toronto, Canada, (July 2023), 4469–4484. doi:10.18653/v1/2023.findings-acl.273. 

- B. Zhang and P. Luo. 2025. “Or-llm-agent: Automating modeling and solving of operations research optimization problem with reasoning large language model.” _arXiv preprint arXiv:2503.10009_ . 

## **A Error Analysis for Q5** 

Table 5 shows the absolute error numbers by LLM and Framework in the multi-instance inference-time compute experiment. Specifically, in this table we count the errors only when the default instance is solved correctly. 

Table 5. Detailed count of errors by LLM and Framework for the multi-instance ITC experiment (Q5) when the default instance is solved correctly. 

|**Error Type**|**CPMpy**|**gpt-5.1**<br>**MiniZinc**|**OR-Tools**|**CPMpy**|**Kimi-K2-I**<br>**MiniZinc**|**OR-Tools**|
|---|---|---|---|---|---|---|
|Wrong Solution|4|7|4|5|3|15|
|Unsatisfiable|6|-|6|6|-|1|
|Runtime Error|1|6|1|-|5|-|
|Gen. Model Timeout|-|-|-|-|5|4|



## **B Detailed Errors for MiniZinc & OR-Tools** 

Figures 10 and 11 show the detailed number of detectable and modelling errors per system prompt level and LLM for MiniZinc and OR-Tools respectively, for Q1 (zero-shot). 

## **C System Prompts** 

We used the official documentation platform of each framework to compose the system prompts for our experiments. All system prompts that we created separately for each framework are visible as follows: 

- CPMpy<sup>12</sup> : Listings 3, 4, 6 

- MiniZinc<sup>13</sup> : Listings 9, 10, 11 

- OR-Tools<sup>14</sup> : Listings 14, 15, 17 

## **D An Example Dataset Instance** 

A dataset instance is shown in Listing 20. 

## **E An Example LLM Response** 

Listing 21 shows the input composed for an example from our dataset. Listing 22 shows the successful initial response from deepseek-coder to this input. Then, the model is given to a solver which gives a solution; the 

12Last accessed at December 2, 2025: https://cpmpy.readthedocs.io/en/latest/index.html 13Last accessed at December 2, 2025: https://docs.minizinc.dev/en/stable/lib-globals.html 14Last accessed at December 2, 2025: https://developers.google.com/optimization/cp 

6:24 • Michailidis, Tsouros & Guns 



Fig. 10. Detectable and modelling errors when LLMs produce MiniZinc code through all system prompt levels. 



Fig. 11. Detectable and modelling errors when LLMs produce OR-Tools code through all system prompt levels. 

self-debug prompt is given as in Listing 23, and the final response of the LLM is given in Listing 24, agreeing to its correctness. 

DCP-Bench-Open: Evaluating LLMs for Constraint Modelling of Discrete Combinatorial Problems • 6:25 

### **Listing 3** Basic Prompt (Level 1) for CPMpy. 

You are an expert in Python, constraint programming, and modelling combinatorial problems. Your task is to model the given problem using the CPMpy library. Specifically, you should generate Python code that uses CPMpy to define and solve the problem. Only the standard Python libraries, CPMpy, and numpy should be used. # Output Formatting Here is an example for printing; assume the problem description contains: "Print the number of apples and oranges (apples, oranges), the cost per round (cost), and the total cost (total_cost)." In this case, the output of the solution as JSON should be done as follows: ````` python if model.solve(): # assuming 'model' is the CPMpy model, and 'apples', 'oranges', 'cost' are the # decision variables, and the objective has been set to minimize or maximize the total cost solution = { 'apples': int(apples.value()), 'oranges': int(oranges.value()), 'cost': cost.value().tolist(), 'total_cost': int(model.objective_value()) } print(json.dumps(solution)) else: print("No solution found.") ````` 

6:26 • Michailidis, Tsouros & Guns 

### **Listing 4** Guidelines Prompt (Level 2) for CPMpy (Part A). 

- [[Basic Prompt]] # Guidelines 

- ## Code Generation Steps 

   - (1) Import only the necessary libraries (cpmpy, json, numpy, etc.). Avoid the use of other libraries except for standard Python libraries, CPMpy, and numpy. 

   - (2) Further process the input data if needed. For example, if there is an array, convert it to a numpy array for easier manipulation (e.g. ‘arr = cp.cpm_array(input_arr)‘) and potential indexing with decision variables. 

   - (3) Define decision variables. 

   - (4) Construct a model with appropriate constraints; always use ‘model = cp.Model()‘ to initialize your model, no other variable names are allowed for the model. 

   - (5) Set the objective, if applicable. 

   - (6) Solve the model. 

   - (7) Print the solution in JSON format according to the print request. The print request is the last part of the given problem description. The JSON output must strictly use the keys provided in the problem description’s print request. Do not add extra keys. Do not change the casing. The values should be integers or lists of integers, or lists of lists of integers, etc. 

- ## Mandatory guidelines: 

   - Do not write ‘from cpmpy import *‘, the implicit overloading of any/all and sum may break or slow down other libraries, so always use ‘import cpmpy as cp‘. 

   - • For maintainability, use logical code organization and comments to explain your constraints. 

   - • Use .value().tolist() method to get solution values from array variables (of any dimension). 

   - When printing integer values (e.g objective values, integer variable values, sums, etc.), always wrap them with int() to avoid JSON serialization issues. 

   - Stick to integer constants (and in general); floats and fractional numbers are not supported. 

   - Explicitly use CPMpy versions of built-in functions sum, max, min, all, and any to avoid confusion with Python built-in functions. E.g. use cp.sum instead of sum, etc. 

- Consider edge cases and possible errors that may occur during the execution of the code. 

- [[continued at Listing 5]] 

DCP-Bench-Open: Evaluating LLMs for Constraint Modelling of Discrete Combinatorial Problems • 6:27 

### **Listing 5** Guidelines Prompt (Level 2) for CPMpy (Part B). 

[[continuing from Listing 4]] ## Response Format Feel free to think step-by-step about the problem before writing the code, but the final answer MUST be the model code as instructed, between triple backticks (python), with the following structure: ````` python import cpmpy as cp import json # Data (optional) ... # End of data # Model definition model = cp.Model() # Decision Variables ... # Constraints model += ... # Objective (optional) model.minimize(objective) # or model.maximize(objective) # Solve and print if model.solve(): solution = {...} print(json.dumps(solution, indent=4)) else: print("No solution found.") ````` ## Important Notes for Printing Solutions The generated code should always print the solution in JSON format using as keys the decision variables as given in the parentheses in the problem description’s print request. The only values allowed are integers and lists of (lists of ...) integers. If booleans are requested, use 0 for False and 1 for True. This is really important for the evaluation of your response, because these values will be directly assigned to the variables of the ground-truth model and check if the constraints (and objective) are satisfied, so follow these guidelines carefully. Finally, always use ‘solution = ...‘ to create the solution dictionary, and print it using ‘print(json.dumps(solution))‘. 

6:28 • Michailidis, Tsouros & Guns 

**Listing 6** Documentation Prompt (Level 3) for CPMpy (Part A). 

[[Guidelines Prompt]] # CPMpy Documentation CPMpy is a Constraint Programming and Modeling library in Python, based on numpy, with direct solver access. An example of a CPMpy model: ````` python import cpmpy as cp import json model = cp.Model() # Variables b = cp.boolvar(name="b") x1 , x2 , x3 = x = cp.intvar (1,10, shape=3, name="x") # unpacking # Constraints model += (x[0] == 1) # fixed value , can also be written as x1 == 1 model += cp.AllDifferent(x) # all values of the decision variables in x are different model += cp.Count(x, 9) == 1 # exactly one of the x's is equal to 9 model += b.implies(x[1] + x[2] > 5) # if b is true , then x2 + x3 > 5 # Objective (optional) model.maximize(cp.sum(x) + 100*b) # maximize the sum of x plus 100 if b is true if model.solve(): solution = {'b': int(b.value ()), 'x': x.value ().tolist ()} # convert boolean to int and list to Python list print(json.dumps(solution , indent =4)) else: print ("No solution found .") ````` ## Short API Documentation: ### Model * ``` model = cp.Model() ``` : Create a model. Use 'model ' as the variable name. * ``` model += constraint ``` : Add a constraint. * ``` model.maximize(obj) ``` or ``` model.minimize(obj) ``` : Set objective (one only). * ``` model.solve () ``` : Solve the model. Returns True if solved. * ``` model.objective_value () ``` : Get objective value after ``` solve () ``` . Wrap with ``` int() ``` to avoid serialization issues. [[continued at Listing 7]] 

DCP-Bench-Open: Evaluating LLMs for Constraint Modelling of Discrete Combinatorial Problems • 6:29 

### **Listing 7** Documentation Prompt (Level 3) for CPMpy (Part B). 

[[continuing from Listing 6]] ### Decision Variables 

- ``` x = cp.boolvar () ``` : Create a boolean variable (True/False). 

- ``` x = cp.intvar(lb, ub) ``` : Create an integer variable with lower bound ``` lb ``` and upper bound ``` ub ``` . 

- ``` xs = cp.intvar(lb , ub, shape=(dim1 , dim2 , ...)) ``` : Create a multi -dimensional array of integer variables. 

- ``` x.value () ``` : Get the value of a variable after ``` model.solve () ``` . 

- ``` x.value ().tolist () ``` : Get the value of an array variable as a Python list. 

##### ### Global Constraints 

- ``` cp.AllDifferent (*args) ``` : All arguments have different values. 

- ``` cp.AllDifferentExcept0 (*args) ``` : All nonzero arguments have different values. 

- ``` cp.AllDifferentExceptN(args , n) ``` : All arguments except those equal to a value in 'n' have a distinct value. 

- ``` cp.AllEqual (*args) ``` : All arguments have the same value. 

- ``` cp.AllEqualExceptN(args , n) ``` : All arguments except those equal to a value in 'n' have the same value. 

- ``` cp.Circuit (*args) ``` : Variables form a circuit (e.g., for routing), where x[i] = j means that j is the successor of i. 

- ``` cp.Inverse(array1 , array2) ``` : Inverse (aka channeling / assignment) constraint. The value of array1[i] is the index of the value in array2. 

- ``` cp.Table(array , table) ``` : Variables in array must match a row in table. 

- ``` cp.ShortTable(array , table) ``` : Extension of the ``` Table ``` constraint where the ``` table ``` matrix may contain wildcards , meaning there are no restrictions for the corresponding variable in that tuple. 

- ``` cp.NegativeTable(array , table) ``` : The values of the variables in 'array ' do not correspond to any row in 'table '. 

- ``` cp.IfThenElse(cond , if_true , if_false) ``` : If cond is true , then if_true else if_false. All arguments must be boolean expressions. 

- ``` cp.InDomain(expr , domain) ``` : Defines non -interval domains for an expression. 

- ``` cp.Xor(arg_list) ``` : Exclusive -or constraint for the arguments. 

- ``` cp.Cumulative(start , duration , end , demand , capacity) ``` : Ensures no task overlaps and respects resource capacity. 

- ``` cp.Precedence(vars , p) ``` : Constraint enforcing some values have precedence over others . If vars[i] = p[j+1], then there exists a vars[i'] = p[j] with i' < i 

- ``` cp.NoOverlap(start , dur , end) ``` : Ensures that the intervals defined by start , dur , and end do not overlap. 

- ``` cp.GlobalCardinalityCount(vars , vals , occ) ``` : Specifies the number of occurrences of values in a variable list. 

[[continued at Listing 8]] 

6:30 • Michailidis, Tsouros & Guns 

### **Listing 8** Documentation Prompt (Level 3) for CPMpy (Part C). 

#### [[continuing from Listing 7]] 

- ``` cp.Increasing(array) ``` : The elements of array are in non -decreasing order. 

- * ``` cp.IncreasingStrict(array) ``` : Same as Increasing , but strictly increasing. * ``` cp.Decreasing(array) ``` : The elements of array are in non -increasing order. * ``` cp.DecreasingStrict(array) ``` : Same as Decreasing , but strictly decreasing. * ``` cp.LexLess(l1, l2) ``` : List l1 is lexicographically less than list l2. * ``` cp.LexLessEq(l1, l2) ``` : List l1 is lexicographically less than or equal to list l2. * ``` cp.LexChainLess(X) ``` : All rows of matrix X are lexicographically ordered. * ``` cp.LexChainLessEq(X) ``` : Same as LexChainLess , but with less than or equal. ### Global Functions 

- ``` cp.Minimum(arg_list) ``` : Computes the minimum value of the arguments. 

- * ``` cp.Maximum(arg_list) ``` : Computes the maximum value of the arguments. * ``` cp.Abs(expr) ``` : Computes the absolute value of an expression. 

- ``` cp.Element(arr , idx) ``` : Enforces arr[idx] to match a specific result. It is generally better to use ``` arr[idx] ``` directly. 

- ``` cp.Count(arr , val) ``` : Counts occurrences of val in arr. 

- ``` cp.Among(arr , vals) ``` : Counts variables taking values in vals. 

- * ``` cp.NValue(arr) ``` : Counts distinct values in arr. * ``` cp.NValueExcept(arr , n) ``` : Counts distinct values in arr excluding n. ### Core expressions: * Python built -in overwrites: ``` sum ``` , ``` max ``` , ``` min ``` , ``` all ``` , ``` any ``` , ``` abs ``` * Comparisons: ``` == ``` , ``` != ``` , ``` < ``` , ``` <= ``` , ``` > ``` , ``` >= ``` (e.g., ``` x == y ``` ) * Math: ``` + ``` , ``` - ``` , ``` * ``` , ``` // ``` (integer division only; never use float division), ``` % ``` ( modulo) (e.g., ``` -x ``` , ``` x + y ``` , ``` x * 2 ``` ) 

- * Logical: ``` & ``` (and), ``` | ``` (or), ``` ~ ``` (not), ``` ^ ``` (xor) (e.g., ``` x & y ``` , ``` ~b ``` ) * Sum: ``` cp.sum([x, y, z]) ``` (sum of variables) * Weighted Sum: ``` cp.sum([c1*x, c2*y, c3*z]) ``` (sum with coefficients) * Implication: ``` x.implies(y) ``` (if x then y) 

DCP-Bench-Open: Evaluating LLMs for Constraint Modelling of Discrete Combinatorial Problems • 6:31 

**Listing 9** Basic Prompt (Level 1) for MiniZinc. 

You are an expert in Minizinc, constraint programming, and modelling combinatorial problems. Your task is to model the given problem using Minizinc. Specifically, you should generate Minizinc code to define and solve the problem. Only the standard Minizinc library and global constraints should be used (e.g., globals.mzn). # Output Formatting Here is an example for printing; assume the problem description contains: "Print the number of apples and oranges (apples, oranges), the cost per round (cost), and the total cost (total_cost)." In this case, the output of the solution as JSON should be done as follows: ````` minizinc output [ "{", join(",", [ "\"" ++ "apples" ++ "\": " ++ show(apples), "\"" ++ "oranges" ++ "\": " ++ show(oranges), "\"" ++ "cost" ++ "\": [" ++ join(",", [show(apple_cost[r]) | r in 1.. num_rounds ]) ++ "]", "\"" ++ "total_cost" ++ "\": " ++ show(total_cost) ]), "}" ]; ````` 

6:32 • Michailidis, Tsouros & Guns 

### **Listing 10** Guidelines Prompt (Level 2) for MiniZinc. 

[[Basic Prompt]] # Guidelines ## Code Generation Steps (1) Import necessary libraries (globals, etc.). (2) Extract and process the provided data. (3) Define decision variables. (4) Construct a model with appropriate constraints. (5) Solve the model (satisfy, minimize, maximize). (6) Print the solution in JSON format according to the print request. The print request is the last part of the given problem description. The JSON output must strictly use the keys provided in the problem description’s print request. Do not add extra keys. Do not change the casing. The values should be integers or lists of integers, or lists of lists of integers, etc. ## Mandatory guidelines: • Be clear, logically organized, and include comments explaining each step. • Use ‘show‘ function to get solution values from variables. • Avoid deprecated functions. • Keep your code simple and maintainable to prevent syntax errors. • Consider edge cases and possible errors that may occur during the execution of the code. ## Response Format Feel free to think step-by-step about the problem before writing the code, but the final answer MUST be the model code as instructed, between triple backticks (minizinc), with the following structure: ````` minizinc % Include libraries if needed include ... % Data (Input Processing) % Extract the data from the problem description and assign it to parameters here. ... % End of data % Decision Variables ... % Constraints ... solve satisfy; % or solve minimize or solve maximize output ["{{...}}"]; ````` 

## Important Notes for Printing Solutions 

The generated code should always print the solution in JSON format using as keys the decision variables as given in the parentheses in the problem description’s print request. The only values allowed are integers and lists of (lists of ...) integers. If booleans are requested, use 0 for False and 1 for True. This is really important for the evaluation of your response, because these values will be directly assigned to the variables of the ground-truth model and check if the constraints (and objective) are satisfied, so follow these guidelines carefully. 

DCP-Bench-Open: Evaluating LLMs for Constraint Modelling of Discrete Combinatorial Problems • 6:33 

**Listing 11** Documentation Prompt (Level 3) for MiniZinc (Part A). 

[[Guidelines Prompt]] # MiniZinc Documentation Minizinc is a high-level constraint modeling language that allows you to define and solve constraint satisfaction and optimization problems. An example of a Minizinc model: ````` minizinc include "globals.mzn"; % Variables var bool: b; array [1..3] of var 1..10: x; % Constraints constraint x[1] = 1; constraint alldifferent(x); constraint b -> (x[2] + x[3] > 5); % Objective function (optional) solve maximize sum(x) + 100 * bool2int(b); % maximize the sum of x plus 100 if b is true output [ "{\n", " \"b\": ", show(bool2int(b)), ",\n", " \"x\": ", show(x), "\n", "}" ]; ````` ## Short API Documentation ### Global Constraints , Predicates and Standard Library Functions 

- predicate all_different(array [$X] of var int: x): Constrain the elements in the array x to be pairwise different. 

- predicate all_different_except_0(array [$X] of var int: vs): Constrain the elements of the array of integers vs to be pairwise different except for those elements that 

- are assigned the value 0. 

- predicate all_equal(array [$X] of var int: x): Constrain the elements of the array x to be all equal. 

- predicate all_disjoint(array [$X] of var set of int: S): Constrain the array of sets of integers S to be pairwise disjoint. 

- predicate circuit(array [$$E] of var $$E: x): Constrains the elements of x to define a circuit where x[i] = j means that j is the successor of i. 

- [[continued at Listing 12]] 

6:34 • Michailidis, Tsouros & Guns 

### **Listing 12** Documentation Prompt (Level 3) for MiniZinc (Part B). 

|[[continuing <br>- predicate <br>of var <br>duratio<br>bound|from Listing 11]]<br> cumulative(array <br> int: r, var int: <br>ns d, and resource <br>b at any one time.|[int] of var int: s, array [int] of var int: d, array [int]<br> b): Requires that a set of tasks given by start times s,<br> requirements r, never require more than a global resource<br> Assumptions: forall i, d[i] >= 0 and r[i] >= 0.|
|---|---|---|
|- predicate <br>[$Y] o<br>is cou|global_cardinalit<br>f var int: counts)<br>nts[i].|y(array [$X] of var $$E: x, array [$Y] of $$E: cover , array<br>: Requires that the number of occurrences of cover[i] in x|
|- predicate <br>Condit<br>else ex<br>corresp|if_then_else(arra<br>ional constraint. <br>pressions. The las<br>onding to the else|y [int] of var bool: c, array [int] of int: x, var int: y):<br> This constraint is generated by the compiler for if -then -<br>t entry in the c array is always the constant true ,<br> case.|
|- predicate <br>the con<br>of tupl|table(array [$$E] <br>straint x in t whe<br>es.|of var bool: x, array [int ,$$E] of bool: t): Represents<br>re we consider each row in t to be a tuple and t as a set|
|- predicate <br>y|'xor '(var bool: x|, var bool: y): Return truth value of x xor y. Usage: x xor|
|- predicate <br>minimum|minimum(var float<br> of the values in|: m, array [int] of var float: x): Constrains m to be the<br> x. Assumptions: |x| > 0.|
|- predicate <br>maximum|maximum(var $$E: <br> of the values in|m, array [int] of var $$E: x): Constrains m to be the<br> x. Assumptions: |x| > 0.|
|- function i|nt: abs(int: x):|Computes the absolute value of the expression.|
|- predicate <br>to be t|element(var $$E: <br>he index of the el|i, array [$$E] of var bool: x, var bool: y): Constrains i<br>ement y in the array x.|
|- predicate <br>the arr|member(array [int<br>ay x.|] of var bool: x, var bool: y): Requires that y occurs in|
|- predicate <br>be the|count(array [$X] <br> number of occurre|of var opt $$E: x, var $$E: y, var int: c): Constrains c to<br>nces of y in x.|
|- predicate <br>n vari|among(var int: n, <br>ables in x to take|array [$X] of var $$E: x, set of $$E: v): Requires exactly<br> one of the values in v.|
|- predicate <br>distinc|nvalue(var int: n<br>t values in x is n|, array [$X] of var int: x): Requires that the number of<br>.|
|- predicate <br>increas|increasing(array <br>ing order (duplica|[$X] of var bool: x): Requires that the array x is in<br>tes are allowed).|



- predicate inverse(array [$$X] of var $$Y: f, array [$$Y] of var $$X: invf): Constrains two arrays of int variables , f and invf , to represent inverse functions. All the 

- values in each array must be within the index set of the other array. 

- - predicate at_least(int: n, array [$X] of var set of $$E: x, set of $$E: v): Requires at least n variables in x to take the value v. 

- predicate exactly(int: n, array [$X] of var set of $$E: x, set of $$E: v): Requires exactly n variables in x to take the value v. 

- predicate disjoint(var set of $$E: s1 , var set of $$E: s2): Requires that sets s1 and s2 do not intersect. 

- [[continued at Listing 13]] 

DCP-Bench-Open: Evaluating LLMs for Constraint Modelling of Discrete Combinatorial Problems • 6:35 

**Listing 13** Documentation Prompt (Level 3) for MiniZinc (Part C). 

[[continuing from Listing 12]] - function var $$E: arg_max(array [$$E] of var int: x): Returns the index of the maximum value in the array x. When breaking ties the least index is returned. - predicate range(array [$$X] of var $$Y: x, var set of $$X: s, var set of $$Y: t): Requires that the image of function x (represented as an array) on set of values s is t. ub(s) must be a subset of index_set(x) otherwise an assertion failure will occur. - predicate subcircuit(array [$$E] of var $$E: x): Constrains the elements of x to define a subcircuit where x[i] = j means that j is the successor of i and x[i] = i means that i is not in the circuit. - predicate sum_set(array [$$X] of $$Y: vs , array [$$X] of int: ws , var set of $$Y: x, var int: s): Requires that the sum of the weights ws[i1]..ws[iN] equals s, where vs [i1]..vs[iN] are the elements appearing in set x. ### Core Expressions - Comparisons: - ``` x == y ``` - ``` x != y ``` - ``` x < y ``` - ``` x <= y ``` - ``` x > y ``` - ``` x >= y ``` - Mathematical operators: - ``` -x ``` - ``` x + y ``` - ``` sum([x, y, z]) ``` - ``` sum([c0 * x, c1 * y, c2 * z]) ``` - ``` x - y ``` - ``` x * y ``` - ``` x / y ``` - ``` x mod y ``` - Logical operators: - ``` x /\ y ``` (and) - ``` x \/ y ``` (or) - ``` not x ``` (not) - ``` x xor y ``` (exclusive or) - ``` x -> y ``` (implication) ### Solving - solve satisfy: Find any solution that satisfies all constraints. - solve minimize expr: Find a solution that minimizes the value of ``` expr ``` . - solve maximize expr: Find a solution that maximizes the value of ``` expr ``` . 

6:36 • Michailidis, Tsouros & Guns 

### **Listing 14** Basic Prompt (Level 1) for OR-Tools. 

You are an expert in Python, constraint programming, and modelling combinatorial problems. Your task is to model the given problem using the OR-Tools library. Specifically, you should generate Python code that uses OR-Tools CP-SAT to define and solve the problem. Only the standard Python libraries and OR-tools should be used. # Output Formatting Here is an example for printing; assume the problem description contains: "Print the number of apples and oranges (apples, oranges), the cost per round (cost), and the total cost (total_cost)." In this case, the output of the solution as JSON should be done as follows: ````` python if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE: solution = { 'apples ': solver.Value(apples), 'oranges ': solver.Value(oranges), 'cost ': [solver.Value(c) for c in cost], 'total_cost ': solver.ObjectiveValue () } print(json.dumps(solution)) else: print("No solution found .") ````` 

DCP-Bench-Open: Evaluating LLMs for Constraint Modelling of Discrete Combinatorial Problems • 6:37 

### **Listing 15** Guidelines Prompt (Level 2) for OR-Tools (Part A). 

- [[Basic Prompt]] # Guidelines ## Code Generation Steps 

   - (1) Import necessary libraries (ortools.sat.python.cp_model, json, etc.). 

   - (2) Extract and process the provided data. 

   - (3) Define decision variables. 

   - (4) Construct a model with appropriate constraints; always use ‘model = cp_model.CpModel()‘ to initialize your model, no other variable names are allowed for the model. 

   - (5) Set the objective, if applicable. 

   - (6) Solve the model. 

   - (7) Print the solution in JSON format according to the print request. The print request is the last part of the given problem description. The JSON output must strictly use the keys provided in the problem description’s print request. Do not add extra keys. Do not change the casing. The values should be integers or lists of integers, or lists of lists of integers, etc. 

#### ## Mandatory guidelines: 

   - For maintainability, use logical code organization and comments to explain your constraints. 

   - • Use .Value() method to get solution values from variables. 

   - Avoid deprecated functions. 

- Consider edge cases and possible errors that may occur during the execution of the code. 

- [[continued at Listing 16]] 

6:38 • Michailidis, Tsouros & Guns 

**Listing 16** Guidelines Prompt (Level 2) for OR-Tools (Part B). 

[[continuing from Listing 15]] ## Response Format Feel free to think step-by-step about the problem before writing the code, but the final answer MUST be the model code as instructed, between triple backticks (python), with the following structure: ````` python from ortools.sat.python import cp_model import json # Data (optional) ... # End of data # Model definition model = cp_model.CpModel () # Decision Variables ... # Constraints ... # Objective function (if any) model.Minimize(objective) # or model.Maximize(objective) # Solve the model solver = cp_model.CpSolver () status = solver.Solve(model) if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE: solution = {...} print(json.dumps(solution)) else: print ("No solution found .") ````` ## Important Notes for Printing Solutions The generated code should always print the solution in JSON format using as keys the decision variables as given in the parentheses in the problem description’s print request. The only values allowed are integers and lists of (lists of ...) integers. If booleans are requested, use 0 for False and 1 for True. This is really important for the evaluation of your response, because these values will be directly assigned to the variables of the ground-truth model and check if the constraints (and objective) are satisfied, so follow these guidelines carefully. Finally, always use ‘solution = ...‘ to create the solution dictionary, and print it using ‘print(json.dumps(solution))‘. 

DCP-Bench-Open: Evaluating LLMs for Constraint Modelling of Discrete Combinatorial Problems • 6:39 

**Listing 17** Documentation Prompt (Level 3) for OR-Tools (Part A). 

[[Guidelines Prompt]] # OR-tools Documentation OR-tools is an open-source software suite for optimization, including constraint programming, linear programming, and mixed-integer programming. We are focusing here on the CP-SAT solver for constraint programming. An example of an OR-tools CP-SAT model: ````` python from ortools.sat.python import cp_model import json # Model definition model = cp_model.CpModel () # Variables b = model.NewBoolVar('b') x = [model.NewIntVar (1, 10, f'x{i}') for i in range (3)] # Constraints model.Add(x[0] == 1) model.AddAllDifferent(x) model.Add(x[1] + x[2] > 5).OnlyEnforceIf(b) # Objective (optional) model.Maximize(sum(x) + 100 * b) # Solve the model solver = cp_model.CpSolver () status = solver.Solve(model) if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE: solution = {'b': solver.Value(b), 'x': [solver.Value(var) for var in x]} print(json.dumps(solution , indent =4)) else: print ("No solution found .") ````` [[continued at Listing 18]] 

6:40 • Michailidis, Tsouros & Guns 

### **Listing 18** Documentation Prompt (Level 3) for OR-Tools (Part B). 

- [[continuing from Listing 17]] ## Short API Documentation ### Model - ``` model = cp_model.CpModel () ``` : Create a new model. - ``` model.Add(expr) ``` : Add a constraint to the model. - ``` model.Maximize(expr) ``` or ``` model.Minimize(expr) ``` : Set objective (one only). ### Solver - ``` solver = cp_model.CpSolver () ``` : Create a solver. - ``` solver.Solve(model) ``` : Solve the model. - ``` solver.Value(var) ``` : Get the value of the variable ``` var ``` in the solution. - ``` solver.ObjectiveValue () ``` : Get the value of the objective function. ### Variables - ``` model.NewIntVar(lb, ub , 'name ') ``` : Create a new integer variable with lower bound ``` lb ``` and upper bound ``` ub ``` . 

- - ``` model.NewBoolVar('name ') ``` : Create a new boolean variable. - ``` model.NewIntervalVar(start , size , end , 'name ') ``` : Create a new interval variable with start , size , and end. An interval variable is a constraint , that is itself used in other constraints like NoOverlap. Internally , it ensures that ``` start + size == end ``` . 

- [[continued at Listing 19]] 

DCP-Bench-Open: Evaluating LLMs for Constraint Modelling of Discrete Combinatorial Problems • 6:41 

### **Listing 19** Documentation Prompt (Level 3) for OR-Tools (Part C). 

|[[continu<br>### Cons|ing from Listing 18]]<br>traints|
|---|---|
|- ```model<br>diff|.AddAllDifferent (* expressions)```: This constraint forces all expressions to have<br>erent values.|
|- ```model<br>enco|.AddCircuit(arcs)```: Adds a circuit constraint from a sparse list of arcs that<br>de the graph.|
|- ```model<br>inte<br>- ```model<br>- ```model<br>- ```model<br>is <br>are <br>- ```model<br>- ```model<br>- ```model<br>- ```model<br>- ```model<br>- ```model<br>- ```model<br>- ```model<br>- ```model<br>- ```model<br>- ```model<br>if ```<br>a va|.AddCumulative(interval_vars , demands , capacity)```: Each interval in ```<br>rval_vars``` requires ```demands[i]``` resources and the capacity is ```capacity```.<br>.AddElement(index , variables , target)```: Enforces ```variables[index] == target```.<br>.AddImplication(a, b)```: Adds the implication constraint ```a -> b```.<br>.AddAllowedAssignments(variables , tuple_list)```: An AllowedAssignments constraint<br> a constraint on an array of variables , which requires that when all variables<br> assigned values , the resulting array equals one of the tuples in ```tuple_list```.<br>.AddAbsEquality(target , expr)```: Adds ```target == Abs(expr)```.<br>.AddModuloEquality(target , expr , mod)```: Adds ```target = expr % mod```.<br>.AddBoolXOr(literals)```: Adds ```XOr(literals) == true```.<br>.AddBoolOr(literals)```: Adds ```Or(literals) == true```.<br>.AddBoolAnd(literals)```: Adds ```And(literals) == true```.<br>.AddAtLeastOne(literals)```: Same as ```add_bool_or```: ```sum(literals) >= 1```.<br>.AddAtMostOne(literals)```: Adds ```AtMostOne(literals)```: ```sum(literals) <= 1```.<br>.AddExactlyOne(literals)```: Adds ```ExactlyOne(literals)```: ```sum(literals) == 1```.<br>.AddNoOverlap2D(x_intervals , y_intervals)```: Adds a 2D no -overlap constraint.<br>.AddNoOverlap(intervals)```: Adds a no -overlap constraint.<br>.AddInverse(variables , inverse_variables)```: An inverse constraint enforces that<br>variables[i]``` is assigned a value ```j```, then ```inverse_variables[j]``` is assigned<br>lue ```i```. And vice versa.|
|- ```model<br>- ```model<br>### Reif|.AddMinEquality(target , exprs)```: Adds ```target == Min(exprs)```.<br>.AddMaxEquality(target , exprs)```: Adds ```target == Max(exprs)```.<br>ication|



- ``` constraint.OnlyEnforceIf(boolvar) ``` : Adds an enforcement literal to the constraint. The constraint is only enforced if the enforcement literal is true. 

6:42 • Michailidis, Tsouros & Guns 

**Listing 20** An example instance from the dataset: Clock Triplets Problem 

#!/usr/bin/python3 # Category: hakan_examples # Source: http ://www.hakank.org/cpmpy/clock_triplets.py # Source description: http ://www.f1compiler.com/samples/Dean %20 Clark %27s%20 Problem.f1. html """ Rearrange the numbers on the face of a clock (1 to 12) so no triplet of adjacent numbers has a sum higher than 21. This is the smallest value that the highest sum of a triplet can have. Print the arrangement of the numbers on the clock (x) as a list of 12 integers - ranging from 1 to 12. """ # Import libraries **from** cpmpy **import** * **import** json # Parameters n = 12 # variables x = intvar(1, n, shape=n, name="x") # The numbers on the clock triplet_sum = intvar(0, 21, name="triplet_sum") # constraints model = Model ([ AllDifferent(x), # <SYMMETRY_BREAKING_CONSTRAINT_START > # x[1] > x[11], # <SYMMETRY_BREAKING_CONSTRAINT_END > [(x[i % 12] + x[(i % 12) - 1] + x[(i % 12) - 2]) <= triplet_sum **for** i **in range** (n)], ]) # Solve model.solve () # Print the solution solution = {"x": x.value().tolist ()} **print** (json.dumps(solution)) 

DCP-Bench-Open: Evaluating LLMs for Constraint Modelling of Discrete Combinatorial Problems • 6:43 

**Listing 21** An example input prompt for the problem _autoref_ from DCP-Bench-Open v0.1.0. 

[[System Prompt]] The problem that you have to model is the following: Given an integer n > 0 and an integer m >= 0, find a non -empty finite series S=(s0 , s1 , ..., sn, sn+1) such that (1) there are si occurrences of i in S for each integer i ranging from 0 to n, and (2) sn+1=m. Print the series S (s). ### Input data: n = 27 m = 5 ### End of input data 

6:44 • Michailidis, Tsouros & Guns 

**Listing 22** The initial response from deepseek-coder to the input of Listing 21. 

````` python import cpmpy as cp import json # Input data n = 27 m = 5 # Model definition model = cp.Model () # Decision Variables s = cp.intvar(0,n+1,shape=n+2,name="s") # Constraints # Constraint (1): there are si occurrences of i in S for each integer i ranging from 0 to n for i in range(n+1): model += [cp.sum([s[j] == i for j in range(n+2)]) == s[i]] # Constraint (2): sn+1=m model += [s[n+1] == m] # Solve and print if model.solve (): solution = {'s': s.value().tolist ()} print(json.dumps(solution , indent =4)) else: print("No solution found .") ````` 

DCP-Bench-Open: Evaluating LLMs for Constraint Modelling of Discrete Combinatorial Problems • 6:45 

**Listing 23** The self-debug <u>prompt given to the LLM, after its response shown in Listing 22.</u> 

You are an expert in combinatorial optimization and you are asked to verify (or debug) a code snippet that models a combinatorial problem. You will be given a combinatorial problem description with instructions on how to model it, its code formulation according to these instructions, and the code output. Explain the given code, especially elaborating on the decision variables, constraints, and the objective function (if applicable). Then, evaluate the code’s correctness in three aspects: 

- (1) **Runtime:** Does the code run successfully without syntax errors, and does it correctly utilize the required libraries? 

- (2) **Model:** Are the decision variables, constraints, and objective function (if applicable) correctly defined? Does the generated solution satisfy the constraints and objective of the given problem description? 

(3) **Solution Printing:** Does the code print the solution in the required JSON format, with the correct keys and values according to the given instructions? If the code is correct, end your response with [[OK]]. If the code is incorrect, provide a corrected version of the code between triple backticks, ensuring the fixed code is self-contained and runnable. End your response with [[FIXED]]. Note: Use [[OK]] and [[FIXED]] only once at the end of your response, and only one of them. Here are the instructions of the user: ````` instr [[System Prompt]] ````` Here is the given problem description: ````` desc [[Problem Description]] ````` Here is the generated code: ````` python [[Initial Model]] ````` Here is the output of the generated code: ````` out {"s": [23,2,2,...,5]} ````` Here is the error description, if any: ````` error No syntax error detected. ````` 

6:46 • Michailidis, Tsouros & Guns 

**Listing 24** The self-debug verification response from the LLM, after the prompt shown in Listing 23 (Part A). 

Let 's analyze the given code line by line , focusing on the decision variables , constraints , and the objective function (if applicable). ````` python import cpmpy as cp import json # Input data n = 27 m = 5 # Model definition model = cp.Model() # Decision Variables s = cp.intvar(0,n+1,shape=n+2,name="s") ````` - ** Decision Variables **: ``` s ``` is defined as an array of ``` n+2 ``` integer variables , each ranging from ``` 0 ``` to ``` n+1 ``` . This array represents the series ``` S ``` with ``` n+2 ``` elements . ````` python # Constraints # Constraint (1): there are si occurrences of i in S for each integer i ranging from 0 to n for i in range(n+1): model += [cp.sum([s[j] == i for j in range(n+2)]) == s[i]] ````` - ** Constraint (1) **: This loop ensures that for each integer ``` i ``` from ``` 0 ``` to ``` n ``` , the number of occurrences of ``` i ``` in the series ``` S ``` (i.e., the number of ``` j ``` such that ``` s[j] == i ``` ) is equal to ``` s[i] ``` . ````` python # Constraint (2): sn+1=m model += [s[n+1] == m] ````` - ** Constraint (2) **: This ensures that the last element of the series ``` S ``` , ``` s[n+1] ``` , is equal to ``` m ``` . [[continued at Listing 25]] 

DCP-Bench-Open: Evaluating LLMs for Constraint Modelling of Discrete Combinatorial Problems • 6:47 

**Listing 25** The self-debug verification response from the LLM, after the prompt as in Listing 23 (Part B). 

[[continuing from Listing 24]] ````` python # Solve and print if model.solve(): solution = {'s': s.value ().tolist ()} print(json.dumps(solution , indent =4)) else: print ("No solution found .") ````` - ** Solve and Print **: The model is solved , and if a solution is found , it is printed in JSON format with the key 's' and the value being the list of integers representing the series S. ### Evaluation of Code Correctness a) **Code Correctness **: - The code runs successfully without syntax errors. - It correctly utilizes the required libraries ( ``` cpmpy ``` , ``` json ``` ). b) ** Model Correctness **: - ** Decision Variables **: Correctly defined as an array of integers. - ** Constraints **: - Constraint (1) correctly ensures the number of occurrences of each integer ``` i ``` in the series ``` S ``` . - Constraint (2) correctly ensures the last element of the series ``` S ``` is equal to ``` m ``` . - ** Objective Function **: Not applicable in this problem. - The generated solution satisfies the constraints of the given problem description. c) ** Solution Printing **: - The code prints the solution in the required JSON format with the correct key ``` 's' ``` and the values are integers. Given the analysis , the code is correct in all aspects. [[OK]] 

