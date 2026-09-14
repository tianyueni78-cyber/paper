MIRROR: A Multi-Agent Framework with Iterative Adaptive Revision and Hierarchical Retrieval for Optimization Modeling in Operations Research 

Yifan Shi<sup>_a_,1</sup> , Jiayi Wang<sup>_a_,1</sup> , Minyi Wu<sup>_a_</sup> , Ye Fan<sup>_b_</sup> , Jialong Shi<sup>_a_,∗</sup> and Jianyong Sun<sup>_a_,∗</sup> 

_aSchool of Mathematics and Statistics, Xi’an Jiaotong University, No.28, Xianning West Road, Xi’an, Shaanxi, 710049, China bSchool of Electronics and Information, Northwestern Polytechnical University, No.1, Dongxiang Road, Xi’an, Shaanxi, 710129, China_ 

## A R T I C L E I N F O 

## A B S T R A C T 

Operations Research (OR) relies on expert-driven modeling—a slow and fragile process ill-suited to novel scenarios. While large language models (LLMs) can automatically translate natural language into optimization models, existing approaches either rely on costly post-training or employ multi-agent frameworks, yet most still lack reliable collaborative error correction and task-specific retrieval, often leading to incorrect outputs. We propose MIRROR (a Multi-agent framework with Iterative adaptive Revision and hierarchical Retrieval for optimization modeling in Operations Research), a fine-tuning-free, end-to-end multi-agent framework that directly translates natural language optimization problems into mathematical models and solver code. MIRROR integrates two core mechanisms: (1) execution-driven iterative adaptive revision for automatic error correction, and (2) hierarchical retrieval to fetch relevant modeling and coding exemplars from a carefully curated exemplar library. Experiments show that MIRROR outperforms existing methods on standard OR benchmarks, with notable results on complex industrial datasets such as “IndustryOR” and “Mamo-ComplexLP”. By combining precise external knowledge infusion with systematic error correction, MIRROR provides non-expert users with an efficient and reliable OR modeling solution, overcoming the fundamental limitations of general-purpose LLMs in expert optimization tasks. 

_Keywords_ : 

Operations Research Large Language Model Multi-Agent Iterative Adaptive Revision Hierarchical Retrieval 

# **1. Introduction** 

Operations Research (OR) serves as a foundational methodology for solving complex decision-making problems and plays an indispensable role in domains such as manufacturing, logistics, supply chain management, energy scheduling, and public services (Cannas et al., 2024). By formulating mathematical optimization models and leveraging high-performance solvers such as Gurobi(Gurobi Optimization, LLC, 2024), COPT(Ge et al., 2024). OR significantly improves resource utilization efficiency, reduces operational costs, and enables enterprises to maximize economic returns. Despite its well-established value, the practical adoption of OR faces a fundamental bottleneck: real-world problems are typically expressed in unstructured natural language, while translating them into rigorous mathematical models and executable code requires deep domain expertise and programming proficiency, making the process time-consuming, labor-intensive, and poorly scalable. This high knowledge barrier limits OR’s accessibility for small- and medium-sized 

> ∗Corresponding authors. 

> `syf123456@stu.xjtu.edu.cn` (Y. Shi); `wangjiayi21@stu.xjtu.edu.cn` (J. Wang); `3125307075@stu.xjtu.edu.cn` (M. Wu); `fanye@nwpu.edu.cn` (Y. Fan); `jialong.shi@xjtu.edu.cn` (J. Shi); `jy.sun@xjtu.edu.cn` (J. Sun) 

> 1Equal contribution. 

Page 1 of 17 

Y. Shi et al.: _Preprint submitted to Elsevier_ 

enterprises and non-technical users, and further complicates adaptation to dynamic changes in operational environments—such as demand shifts or updated constraints—that necessitate frequent, expert-driven model revisions. 

Recent advances in large language models (LLMs) have demonstrated remarkable capabilities in natural language understanding, mathematical reasoning, symbolic manipulation, and code generation—often approaching or even surpassing human expert performance. Current mainstream LLMs can be broadly categorized into two paradigms: general models and reasoning models. General models, including GPT4 (OpenAI et al., 2024a), DeepSeek-V3 (DeepSeek-AI et al., 2025), and Qwen-3 (Yang et al., 2025a), excel in semantic comprehension and broad knowledge coverage through extensive pre-training on textual corpora, enabling accurate interpretation of complex problem descriptions and the generation of preliminary modeling insights. Meanwhile, reasoning model architectures such as GPT-o1 (OpenAI et al., 2024b) and DeepSeek-R1 (Guo et al., 2025) explicitly enhance systematic thinking, multi-step reasoning chains, and self-correction mechanisms, thereby achieving superior performance in structured tasks such as mathematical derivation, constraint formalization, and code synthesis. 

Motivated by recent advances in large language models (LLMs), researchers have explored various approaches to automatically translate unstructured natural language problem statements into solvable mathematical optimization models, aiming to democratize operations research for non-experts. Recent efforts such as LLMOPT (Jiang et al., 2025), ORLM (Huang et al., 2025a), and MiniOpt (Di et al., 2026) train specialized models via supervised fine-tuning or reinforcement learning on synthetic datasets; however, they face two fundamental challenges: high-quality annotated data is scarce and expensive to construct, and the outputs inherently lack natural verifiability, making evaluation and debugging difficult—particularly for smaller-scale models. To circumvent these limitations, a growing line of work has shifted toward multi-agent frameworks that coordinate multiple LLM agents to collaboratively construct optimization models without any additional training. Systems like Chain-of-Experts (Xiao et al., 2023), OptiMUS (Ahmaditeshnizi et al., 2024), ORMind (Wang et al., 2025), and OptiTree (Liu et al., 2026) decompose complex modeling tasks into specialized roles and enable iterative interaction among agents, offering a flexible and practical alternative. Nevertheless, existing multi-agent frameworks are still constrained by closed architectures that lack extensibility; their external knowledge is often generated by the large models themselves, introducing hallucinations, biases, or misalignments with task requirements, which yields low-quality and poorly relevant contextual support. More critically, most of these frameworks lack reliable correction mechanisms, making it difficult to detect and rectify errors after code execution, thereby creating hidden risks of solution failure and diminished system credibility. 

To address these limitations, we propose MIRROR, a **M** ulti-agent framework with **I** terative adaptive **R** evision and hierarchical **R** etrieval for optimization modeling in **O** perations **R** esearch, with the following key contributions. 

- **We propose MIRROR, an end-to-end multi-agent framework.** This framework requires no finetuning and automatically transforms natural language descriptions of optimization problems into executable solver code. Its dual-memory architecture consists of local memory and shared global memory: the former records the outputs required by the revision-stage agents to ensure intra-task consistency, while the latter enables cross-task knowledge transfer. 

- **We design an Iterative Adaptive Revision (IAR) mechanism.** Whenever solver code execution fails, the mathematical modeling and code generation agents switch to their respective revision experts, diagnose errors in either the model or the solver code, and generate structured revision tips. The system then iteratively refines both the model and solver code without human intervention until a correct solution is obtained or a preset limit reached. Unlike existing methods, our approach stores the historical 

Page 2 of 17 

Y. Shi et al.: _Preprint submitted to Elsevier_ 

model, code, and associated revision tips in a local memory pool to provide contextual history for subsequent corrective iterations. 

- **We propose a Hierarchical Retrieval-Augmented Generation (HRAG) mechanism.** It is based on an exemplar library constructed via an automated synthesis and labeling pipeline. The mechanism employs a two-stage retrieval strategy—first coarse-grained filtering by overall problem semantics and metadata, then fine-grained reranking based on subproblem types and deep semantic similarity—to provide highly relevant exemplar contexts for modeling and code generation, significantly improving model rationality and solver code correctness. 

MIRROR achieves state-of-the-art performance among current multi-agent approaches on multiple operations research benchmarks. It notably outperforms existing methods on challenging datasets such as “IndustryOR” and “Mamo-ComplexLP”. The framework also demonstrates effectiveness with small open-source language models, enhancing their optimization modeling capabilities without any task-specific training. 

# **2. Related Work** 

_LLMs for Math and Code Generation_ In recent years, large language models (LLMs) have achieved remarkable advances in mathematical reasoning and code generation. On the mathematical side, specialized models such as Qwen2.5-Math (Yang et al., 2024) and DeepSeek-Prover (Ren et al., 2025) have enhanced formalized inference, while systems like AlphaEvolve (Novikov et al., 2025) and MM-Agent (Liu et al., 2025) further integrate LLMs into end-to-end mathematical problem-solving pipelines. In code generation, frameworks including CodeAct (Wang et al., 2024), KareCoder (Huang et al., 2024), SWE-bench (Jimenez et al., 2024), and Web-bench (Xu et al., 2025) demonstrate the potential of LLMs for autonomous programming and debugging. Building on these developments, the present study focuses on the intersection of mathematical modeling and programming—automated optimization modeling—and categorizes existing solutions into two paradigms: Learning-based LLM Optimization Modeling and Agent-based LLM Optimization Modeling. 

_Learning-based LLM Optimization Modeling_ Recent learning-driven studies enhance LLM-based optimization modeling via data synthesis, targeted fine-tuning, and reinforcement learning to address domain adaptation and data scarcity in operations research. ORLM (Huang et al., 2025a), OptMATH (Lu et al., 2025), Step-Opt (Wu et al., 2025), and ReSocratic (Yang et al., 2025b) are recent works on the data synthesis front. On the learning mechanism side, LLMOPT (Jiang et al., 2025), MiniOpt (Di et al., 2026), and SIRL (Chen et al., 2025) reduce modeling hallucinations and improve generalization. OR-R1 (Ding et al., 2025) achieves similar effects via verifiable learning mechanisms. Additionally, CALM (Tang et al., 2025) and StepORLM (Zhou et al., 2025) refine reasoning trajectories through corrective adaptation and process supervision. 

_Agent-based LLM Optimization Modeling_ To overcome the inherent limitations of fixed decomposition strategies, agent-based frameworks enhance modeling performance through specialized role allocation and collaborative mechanisms. Chain-of-Experts (Xiao et al., 2023) introduces a Conductor to orchestrate domain experts, whereas OptiMUS (Ahmaditeshnizi et al., 2024) utilizes a modular structure to decouple formulation, coding and evaluation modules. At the execution level, OptimAI (Thind et al., 2026) incorporates a Planner and a Code Critic to enable strategic reflection, while OR-LLM-Agent (Zhang and Luo, 2025) leverages the capabilities of reasoning LLMs to decompose the task into three sub-tasks: modeling, code generation and debugging. Furthermore, to enhance reliability, ORMind (Wang et al., 2025) draws on cognitive dual-process theory to implement counterfactual reasoning for error detection, while LEAN-LLM-OPT (Liang et al., 2026) employs a lightweight few-shot approach to reduce computational overhead without compromising modeling effectiveness. To move beyond predefined steps, OptiTree (Liu et al., 2026) introduces a hierarchical thought 

Page 3 of 17 

Y. Shi et al.: _Preprint submitted to Elsevier_ 

generation framework that employs tree search to adaptively decompose complex optimization problems into simpler subproblems based on a structured modeling tree. 

_Summary and Gaps_ Despite recent progress, existing methods face two main limitations. First, learning-based models rely on annotated datasets that are scarce and expensive to create. Their “black-box” nature also makes it difficult to diagnose errors or adapt to new constraints without costly re-training. Second, most current multi-agent frameworks often hallucinate due to a lack of external domain knowledge. Moreover, they typically struggle to effectively use solver feedback for error correction, leading to repeated execution failures. To bridge these gaps, we propose MIRROR, which integrates external knowledge retrieval with execution-based iterative revision. 

### **MIRROR: A Multi-Agent Framework for Automated Optimization Modeling** 



<!-- Start of picture text -->
Mathematical Code Execution /<br>Problem Analysis Unified Modeling Generation Validation<br>Natural- ExtractionParameter ModelingAdvisor representationsemantic 1 {"VARIABLES": "" 12 importmodel =gurobipygp.Modelas() gp success   Numericalanswer<br>optimizationlanguage 12 { "Definition""p1": {"Type": "": ""},,... } 1 2 **Category**: ...**Insight**: ... 2 3 "OBJECTIVE""CONSTRAINTS": "" }: [ ], 34 ...model.optimize()<br>problem store store failure<br>model code<br>Exemplars Exemplars Local memory  Local memory<br>(Model) (Code) pool pool<br>(Model) (Code)<br>Primary generation flow corrected code<br>Retrieval support (HRAG) Selected exemplars & model IAR:<br>Revision flow (IAR) Revision AgentModel Revision AgentCode Iterative<br>Global memory pool Cross-task knowledge and experiences HRAG: Hierarchical Exemplar library 12 34  model_tip "scenario""tip_type""error_statement"::{: "" "",, : "", 1234 "scenario" "error_statement"code_tip"tip_type":{ : "": "", , : "", AdaptiveRevision<br>5 "correct_component": "", 5 "code_error_location": "",<br>Retrieval-Augmented Generation 6 "incorrect_model": "" } 67 "correct_code_snippet" "incorrect_code_snippet": "": "", }<br><!-- End of picture text -->

**Figure 1:** MIRROR: An LLM-based multi-agent framework that automates end-to-end optimization modeling—from natural language to executable solver code—through four phases: Understanding, Modeling, Implementation, and Revision. Hierarchical Retrieval-Augmented Generation (HRAG) retrieves relevant exemplars for model and solver code synthesis; upon execution failure, the Iterative Adaptive Revision (IAR) mechanism leverages local memory to diagnose and refine outputs. Local memory stores per-task agent history for revision, while global memory accumulates cross-task knowledge for system-wide evolution. 

# **3. Methodology** 

The core of MIRROR is a synergistic multi-component methodology. MIRROR introduces a carefully curated exemplar library containing problem types and subproblem types to provide detailed exemplar references for the modeling and programming processes. A shared global memory pool stores the outputs produced by all agents throughout the workflow and allows these agents to retrieve previously generated content before producing new outputs. In addition to this shared memory, MIRROR introduces two local memory pools for the modeling and programming processes. These pools exclusively store the corresponding content and revision tips generated during the generation and revision stages, and each local pool can only be accessed and updated by its associated agents. The overall system follows a closed-loop paradigm consisting of analysis, modeling, implementation, and revision to solve optimization problems end to end. The correctness and robustness of the generated results are further supported by Iterative Adaptive Revision (IAR) and Hierarchical Retrieval-Augmented Generation (HRAG). The overall architecture of MIRROR is depicted in Figure 1. 

Page 4 of 17 

Y. Shi et al.: _Preprint submitted to Elsevier_ 

To achieve end-to-end automated modeling from natural-language problem descriptions to executable optimization programs, we design a multi-agent framework in which multiple specialized agents collaborate with one another. The complete workflow consists of a generation phase and a revision phase. 

## **3.1. Generation Phase** 

Given a natural-language optimization problem _𝑡_ , the **Parameter Extraction Agent** ( _𝑓_ param), **Modeling Advisor Agent** ( _𝑓_ adv), **Mathematical Modeling Agent** ( _𝑓_ model), and **Code Generation Agent** ( _𝑓_ code) sequentially perform their respective functions during the generation phase, ultimately producing executable solver code _𝑐_ . 

First, _𝑓_ param identifies and structures the core parameters of the problem, producing _𝑝_ , a JSON object that contains parameter symbols, data types, and semantic definitions. This output is then passed to _𝑓_ adv as contextual information. The advisor provides domain-aware semantic guidance by generating _𝑔_ , a standardized JSON list containing operational explanations of domain-specific terminology, key problem details, and a characterization of the essential structure of the problem. 

Subsequently, _𝑓_ model integrates the original problem _𝑡_ , the extracted parameters _𝑝_ , the advisory guidance _𝑔_ , and the retrieved modeling exemplar set model to construct a formal mathematical model _𝑚_ . Finally, _𝑓_ code translates _𝑚_ into an executable program, handles implementation details, and resolves potential inconsistencies between the abstract formulation and the syntax required by solvers such as Gurobi. Both the Mathematical Modeling Agent and the Code Generation Agent employ the unified HRAG mechanism described in Section 3.1.1. This mechanism dynamically retrieves and incorporates the most relevant modeling paradigms and code exemplars code from the exemplar library. 

The external executor receives the generated code _𝑐_ and attempts to run it. It returns either a numerical solution _𝑛_ or a failure flag _⊥_ accompanied by a specific error message _𝑒_ , such as a syntax error or an execution timeout. This feedback signal determines whether the revision phase should be triggered. If execution succeeds, the solving process terminates immediately; otherwise, the system enters the iterative revision phase. 

### **_3.1.1. Hierarchical Retrieval-Augmented Generation (_ HRAG** **_)_** 

High-quality exemplar libraries are a critical resource for leveraging in-context learning across diverse domains, as LLM performance is highly sensitive to the demonstrations provided in the prompt (Liu et al., 2022). Recent studies demonstrate the value of structured knowledge repositories for automated mathematical and optimization modeling. MM-Agent constructs a three-level Hierarchical Mathematical Modeling Library that organizes domains, subdomains, and modeling methods, enabling task-specific method retrieval for subtask formulation (Liu et al., 2025). Similarly, OptiTree organizes operations research problems by taxonomy and complexity in a modeling tree, stores modeling thoughts at its nodes, and retrieves relevant subproblems and thoughts to guide the decomposition of unseen complex instances (Liu et al., 2026). These designs show that reusable modeling knowledge should be explicitly organized around problem structure, rather than relying solely on the latent knowledge of an LLM. However, the retrieved knowledge in these systems primarily consists of high-level methods or modeling thoughts; it is not designed as a stage-specific library of verified end-to-end examples that jointly support mathematical formulation and solver-code generation. MIRROR addresses this gap by constructing a curated exemplar library specifically designed to support both modeling and code-generation stages. 

The HRAG mechanism follows an “exemplar construction–exemplar allocation” strategy. During exemplar construction, the system builds an exemplar library  containing 602 high-quality and distributionbalanced optimization instances. Through context augmentation, each exemplar contains a complete mathematical modeling process and its corresponding solver code, organized as a triplet ( _𝑡, 𝑚, 𝑐_ ). Each instance is additionally annotated with a high-level problem category and a fine-grained subproblem type. 

Page 5 of 17 

Y. Shi et al.: _Preprint submitted to Elsevier_ 

During exemplar allocation, the system retrieves relevant exemplars and delivers them to the corresponding agents. 

**_Exemplar Library Construction_** The exemplar library  is constructed through a multi-stage curation pipeline during the preparation phase. Figure 2 presents the construction workflow. At this stage, ground-truth verification signals are available for evaluating correctness, including both the executability of the solver code and the optimality of the resulting solution. We collect 1,127 raw optimization problems from three 



<!-- Start of picture text -->
Model-Code Completion  •  Raw OR Instances Type Annotation<br>OptiBench: 605 Problem type: LP, MILP, QP, and<br>MIRROR W/o HRAG OptMATH: 359 MIQP<br>Mamo-EasyLP: the last  Subtype:<br>Code Execution 163 network flow & transshipment...<br>Success Failure ExemplarLibrary filter ExemplarLibrary<br>Wrong Answer Correct Answer 652 602<br>the ground truth<br><!-- End of picture text -->

**Figure 2:** Construction workload of the exemplar library. 

sources: 605 instances from OptiBench (Yang et al., 2025b), 359 instances from “OptMATH”, and the final 163 instances from “Mamo-EasyLP”. 

Each instance is first processed by MIRROR without HRAG to complete its missing mathematical formulation and executable solver code. The generated model–solver-code pair is then verified by an oracle solver. This completion process is conducted for a fixed number of iterations. If the generated code fails to compile, the revision workflow is activated to correct both the model and the code. If the code compiles successfully but its final answer differs from the ground truth, the ground-truth answer is provided to the agents as a reference, and the model and code are regenerated. This procedure continues until the correct answer is obtained or the maximum number of iterations is reached. Only instances that produce the correct optimal solution are retained, yielding 652 fully specified and verified problem–solution pairs. 

We then use the large language model `qwen-plus` to annotate each verified instance with a high-level problem category, including linear programming (LP), mixed-integer linear programming (MILP), quadratic programming (QP), and mixed-integer quadratic programming (MIQP), and a fine-grained subproblem type. The subproblem taxonomy comprises blending & mixing; network flow & transshipment; multi-period production & inventory; resource allocation; sequencing & routing; location & network design; selection & knapsack; discrete scheduling & assignment; covering, packing & partitioning; risk & return balancing; error minimization & fitting; continuous optimal control; discrete risk control; non-linear layout & assignment; and constrained sparse regression. 

Instances whose categories cannot be determined reliably are removed. The remaining 602 instances form the final exemplar library and are encoded using an embedding model to support subsequent retrieval. The standard format of an individual data instance in the exemplar library is shown in Figure 3. 

Data Instance {"en_answer": 10000.0, "prompt": "A construction company is planning to allocate resources across four different tasks: ...?", "response": "## Mathematical Model: ... \"VARIABLES\": ... \"CONSTRAINTS\": ... \"OBJECTIVE\": ... ## Python Code: ...", "problem_type": "Mixed-Integer Linear Programming (MILP)", "problem_subtype": "Discrete Scheduling & Assignment"} 

**Figure 3:** Standard format of a data instance in the exemplar library. 

Page 6 of 17 

Y. Shi et al.: _Preprint submitted to Elsevier_ 

**_Hierarchical Retrieval Process_** The Mathematical Modeling Agent and the Code Generation Agent retrieve their respective reference exemplars through a two-stage process, the detailed procedure of which is illustrated in Figure 4. 



<!-- Start of picture text -->
HRAG: Hierarchical Retrieval-Augmented Generation<br>Coarse-grained filtering Fine-grained reranking<br>Exemplar MMR Problem type<br>Library algorithm subtype Exemplars<br>semantic similarity<br><!-- End of picture text -->

**Figure 4:** Hierarchical retrieval process. 

**1. Coarse-grained filtering:** The embedding model Θemb is combined with the Maximal Marginal Relevance (MMR) algorithm (Adams et al., 2022) to identify candidate exemplars that are both semantically relevant and diverse. 

**2. Fine-grained reranking:** A large language model reranks the candidate exemplars according to problem-category alignment and deeper semantic similarity, thereby selecting the exemplars most relevant to the target task. The system delivers at most two high-value exemplars to each agent. These are represented as the modeling reference _𝑅_ model and the code reference _𝑅_ code for the Mathematical Modeling Agent and the Code Generation Agent, respectively. If no suitable exemplar is identified, the system returns a null signal and activates a stable fallback mechanism. 

## **3.2. Revision Phase** 

### **_3.2.1. Iterative Adaptive Revision (_ IAR** **_)_** 

The system first performs forward generation by sequentially invoking _𝑓_ param, _𝑓_ adv, _𝑓_ model, and _𝑓_ code, thereby mapping the input task _𝑡_ to executable solver code _𝑐_ . If the executor returns a failure, the IAR mechanism is activated. The Mathematical Modeling Agent and the Code Generation Agent then switch roles and operate as the **Modeling Revision Agent** _𝛿_ model and the **Code Revision Agent** _𝛿_ code, respectively. These agents collaboratively diagnose the root cause of the failure and generate structured revision tips. The Dual Memory mechanism described in Section 3.2.2 supports error diagnosis and correction throughout this process. The detailed procedure is depicted in Figure 5. When execution fails, the Modeling Revision 



<!-- Start of picture text -->
IAR: Iterative Adaptive Revision<br>problem Model Revision Agent revised model problem Code Revision Agent revised code<br>model Local memory pool  model tip error message Local memory pool  code tip<br>Compileerror error message Stores historical model outputs for (model) code tips Stores historical code outputs for (code) Compile<br>diagnosis and refinement diagnosis and refinement<br>model tips code<br><!-- End of picture text -->

**Figure 5:** Iterative adaptive revision process. 

Agent first enters the revision process. It retrieves the most recently generated model and available revision tips from the modeling memory pool, which is empty during the initial revision round. Using the retrieved content, the original problem description, and the error message returned by the executor, the agent revises the mathematical model and stores the updated model in the modeling memory pool. It also generates a structured modeling revision tip for use in subsequent revision rounds. 

After the Modeling Revision Agent completes its work, the Code Revision Agent retrieves the latest complete code and revision tips from the programming memory pool, the most recently revised model from 

Page 7 of 17 

Y. Shi et al.: _Preprint submitted to Elsevier_ 

the modeling memory pool, and the error message provided by the executor. Based on this information and the original problem description, it revises the solver implementation and produces new code. A programmingrelated revision tip is generated simultaneously and stored in the programming memory pool. Thus, both revision agents produce structured tips that are retained in their corresponding local memory pools and reused during subsequent revision rounds. The Modeling Revision Agent produces model-level tips, whereas the Code Revision Agent produces implementation-level tips. The revision tip templates are shown in Figure 6. 



<!-- Start of picture text -->
Revision Tip (model) Revision Tip (code)<br>{{<br>{{<br>"tip_type": "code",<br>"tip_type": "modeling",<br>"scenario": "...",<br>"scenario": "...",<br>"error_statement": "...",<br>"error_statement": "...",<br>"code_error_location": "...",<br>"correct_component": "...",<br>"correct_code_snippet": "...",<br>"incorrect_model": "..."<br>"incorrect_code_snippet": "..."<br>}}<br>}}<br>(a) Modeling revision tip. (b) Code revision tip.<br><!-- End of picture text -->

**Figure 6:** Structured revision tip templates. 

The system subsequently executes the revised solver code. The model-and-code refinement process continues iteratively until a valid solution is produced or the maximum number of revision rounds is reached, forming a closed-loop correction mechanism driven by execution feedback. 

### **_3.2.2. Dual Memory_** 

Recent automated optimization-modeling systems, such as ORMind, have employed shared memory resources to coordinate specialized components by maintaining a centralized Memory Pool that is updated after each component produces an output (Wang et al., 2025). Although shared access promotes information reuse and coordination, placing heterogeneous artifacts in a single common space can blur the boundary between modeling, programming, and execution-feedback information. As the number of agents increases or their outputs become longer, the stored content becomes increasingly redundant and heterogeneous, introducing irrelevant context and retrieval noise that may interfere with error localization during subsequent revision. To address this issue, MIRROR introduces separate local memory pools for mathematical modeling and solver-code generation and revision. Each local pool stores only the historical outputs, error messages, and revision tips associated with its corresponding task, thereby providing focused context for iterative correction. Together with the global memory pool, this dual-memory design supports both cross-task knowledge reuse and task-specific error diagnosis. 

- **Local memory pools:** Each local memory pool is associated with a specific type of agent and stores the relevant historical outputs from the generation and revision stages, including previous models, solver code, error messages, and debugging or revision tips. This information provides focused contextual history for iterative revision. The modeling memory pool and the programming memory pool primarily support their corresponding agents while also enabling the necessary transfer of revised modeling information to the Code Revision Agent. 

- **Global memory pool:** The global memory pool aggregates outputs produced by all functional agents across different stages and tasks. It enables shared experience and cross-task knowledge reuse, while supporting continuous optimization at the system level. 

Page 8 of 17 

Y. Shi et al.: _Preprint submitted to Elsevier_ 

## **3.3. Illustrative Examples** 

### **_3.3.1. Revision Instance_** 

Figure 7a presents the overall structure of the revision process, while Figure 7b illustrates the detailed revision trajectory of a specific problem. In this example, the initially generated code fails to compile, but the problem is successfully solved and the correct answer is obtained after two revision rounds. 



<!-- Start of picture text -->
Revision Structure Revision Details<br>Generation Phase "problem_description": "Multi-product transportation on sparse links with capacity constraints."<br>problem: Consider a transportation problem with multiple prod- "initial_failure":<br>ucts...? # initial generated objective<br>... gp.quicksum(  ShipmentCost[i][j][p] * flow[i,j,p] Result: COMPILE ERROR<br>  for all city pairs (i,j) Error: IndexError: list index out of range<br>Result: COMPILE ERROR   for each product p<br>)<br>IAR Phase<br>-- First Revision -- "attempt_1":<br>... Modeling memory tip: iterate only over valid links in Links.<br>Result: COMPILE ERROR # after using valid-link memory tip Result: COMPILE ERROR<br>-- Second Revision -- idx = link_to_idx[(Cities[i], Cities[j])]ShipmentCost[idx][p] * flow[i,j,p] Remaining error: TypeError caused by non-scalar cost indexing<br>{{"original_incorrect_model_objective": "...",<br>"revised_correct_model_objective": "..."}, "attempt_2":<br>{"original_incorrect_code_snippet": "...", Modeling memory tip: ShipmentCost and Capacity are 3D arrays; use scalar indexing.<br>"revised_correct_code_snippet": "..."}} idx = link_to_idx[(Cities[i], Cities[j])]cost = ShipmentCost[idx][0][p] Result: ACCEPT<br>Result: ACCEPT cap  = Capacity[link_idx][0][p]<br>(a) Revision structure. (b) Revision details.<br><!-- End of picture text -->

**Figure 7:** An example of the MIRROR revision process. 

During the initial implementation, the Code Generation Agent incorrectly assumes that the transportation network is fully connected and constructs the objective function by traversing the Cartesian product of all city pairs. However, the input data contain only a specified set of sparse directed links. Consequently, the generated solver code attempts to access `ShipmentCost` entries for non-existent links and raises an `IndexError` ( `list index out of range` ). 

In response, the system initiates the first revision round (Attempt 1). The Modeling Revision Agent identifies the mismatch between the mathematical model and the sparse data structure and determines that the objective function must iterate only over the links explicitly listed in `Links` . The Code Revision Agent accordingly introduces a `link_to_idx` mapping and modifies the implementation to traverse valid links only. Although this revision resolves the out-of-range indexing problem, the revised code raises a `TypeError` at runtime. The error indicates that a sequence is being multiplied by a Gurobi variable, revealing that the code still applies an incorrect indexing depth to the three-dimensional `ShipmentCost` array and therefore fails to extract a scalar cost value. 

The system then performs a second revision round (Attempt 2) to resolve this subtler data-structure error. MIRROR analyzes the three-dimensional list structure of `ShipmentCost` , and the Modeling Revision Agent generates a critical memory tip stating that the index expression must precisely match the dimensional organization of the input data. Guided by this tip, the Code Revision Agent corrects the indexing of both the cost and capacity arrays, for example replacing `ShipmentCost[...][p]` with `ShipmentCost[...][0][p]` . 

After these two feedback-driven revision rounds, the solver code compiles and executes successfully, producing the final result `ACCEPT` . This example demonstrates that IAR can correct not only surface-level syntax errors but also deeper logical defects and data-structure alignment errors through repeated execution, diagnosis, and revision, thereby improving the correctness and robustness of the final solution. 

### **_3.3.2. Exemplar Structure_** 

The reference exemplars ultimately provided to the Mathematical Modeling Agent and the Code Generation Agent use the structures shown in Figure 8. 

Page 9 of 17 

Y. Shi et al.: _Preprint submitted to Elsevier_ 



<!-- Start of picture text -->
Modeling Exemplar Structure<br>{{<br>"Problem description": "...",<br>"Mathematical Model": {{<br>"VARIABLES": "...",<br>"CONSTRAINTS": "...",<br>"OBJECTIVE": "..."<br>}}<br>}}<br><!-- End of picture text -->



<!-- Start of picture text -->
(a) Modeling exemplar structure.<br><!-- End of picture text -->



<!-- Start of picture text -->
Solver Code Exemplar Structure<br>{{<br>"Problem description": "...",<br>"Mathematical Model": {{<br>"VARIABLES": "...",<br>"CONSTRAINTS": "...",<br>"OBJECTIVE": "..."<br>}},<br>"Code": "..."<br>}}<br><!-- End of picture text -->



<!-- Start of picture text -->
(b) Solver code exemplar structure.<br><!-- End of picture text -->

**Figure 8:** Structures of the retrieved reference exemplars. 



<!-- Start of picture text -->
are a modeling assistant specialized in the f i eld of Operations Research for<br>mathematical formulation.Your task is to formulate a precise mathematical<br>optimization model based on the problem description below.Now, formulate<br>a model for this problem:Imagine you are in charge of planning a week’ s<br>worth of meals for a small group and need to ensure everyone gets the right<br>amount of nutrients without overspending . You have four dif f erent food items<br>to choose from, each with its own nutritional content and cost.Here’ s what<br>each food item ofers f : - Food_ 1: Provides 19 grams of protein, 9 grams of<br>carbohydrates, and 83 calories for $7.- Food_ 2: Of f ers 4 grams of protein, 16<br>grams of carbohydrates, and 166 calories for $7.- Food _3: Contains 3 grams of<br>protein, 11 grams of carbohydrates, and 71 calories for $10.- Food_ 4: Delivers 8<br>grams of protein, 7 grams of carbohydrates, and 56 calories for $2. Your goal is<br>to meet the following nutritional requirements for the group: - At least 84 grams<br>of protein, - At least 132 grams of carbohydrates ,- At least 1990 calories.Your<br>challenge is to determine the most cost-ef f ective way to purchase these food<br>items to meet or exceed the nutritional requirements . What is the minimal<br>cost to meet these dietary needs?Formulate the model strictly in the following<br>JSON format: { ”V ARIABLES ”: ”A concise description about variables and<br>its shape or type” , ” CONSTRAINTS ”: ”A mathematical formula expressing<br>all constraints” , ”OBJECTIVE” : ”A mathematical formula for the objective<br>function” } Important: 1. Base your formulation primarily on the original problem<br>description2 . Output ONLY the JSON object without any additional text<br>(a) Without exemplars.<br><!-- End of picture text -->



<!-- Start of picture text -->
are a modeling assistant specialized in the f i eld of Operations Research for<br>mathematical formulation.Your task is to formulate a precise mathematical<br>optimization model based on the problem description below.Now, formulate<br>a model for this problem:Imagine you are in charge of planning a week’ s<br>worth of meals for a small group and need to ensure everyone gets the right<br>amount of nutrients without overspending . You have four dif f erent food items<br>to choose from, each with its own nutritional content and cost.Here’ s what<br>each food item of f ers: - Food_ 1: Provides 19 grams of protein, 9 grams of<br>carbohydrates, and 83 calories for $7.- Food_ 2: Of f ers 4 grams of protein, 16<br>grams of carbohydrates, and 166 calories for $7.- Food _3: Contains 3 grams of<br>protein, 11 grams of carbohydrates, and 71 calories for $10.- Food_ 4: Delivers 8<br>grams of protein, 7 grams of carbohydrates, and 56 calories for $2. Your goal is<br>to meet the following nutritional requirements for the group: - At least 84 grams<br>of protein, - At least 132 grams of carbohydrates ,- At least 1990 calories.Your<br>challenge is to determine the most cost-ef f ective way to purchase these food<br>items to meet or exceed the nutritional requirements. What is the minimal<br>cost to meet these dietary needs? Re levant modeling examples from knowledge<br>base (focus on their formulation structure and methodology only ) :example 1:<br>{” Problem description” : ”International Wool Company operates a large farm<br>on which sheep are raised. The farm manager determined that for the sheep<br>to grow in the desired fashion, they need at least minimum amounts of four<br>nutrients (the nutrients are n ontoxic so the sheep can consume more than the<br>minimum without harm) . The manager is considering three dif f erent grains to<br>feed the sheep. The table below lists the number of units of each nutrient in<br>each pound of grain, the minimum daily requirements of each nutrient for each<br>sheep, and the cost of each grain. The manager believes that as long as a sheep<br>receives the minimum daily amount of each nutrient, it will be healthy and<br>produce a standard amount of wool. The manager wants to raise the sheep at<br>minimum cost . The columns of table are nutrient name, nutrient unit in the<br>three dif f erent grains, and Minimum Daily Requirement (unit) . The rows =<br>[Nutrient A, 20, 30, 70, 110], [ Nutrient B, 10, 10, 0, 18], [ Nutrient C, 50, 30,<br>0, 90], [ Nutrient D, 6, 2.5, 10, 14]. The prices of ngrain nutrient A, B and C<br>are 41,36, 96, respectively. ”, ” Mathematica l Model” : {”V ARIABLES ”: ”x1, x2,<br>x3: non-negative real numbers representing the pounds of grain 1, grain 2, and<br>grain 3 fed to each sheep per day. ”, ” CONSTRAINTS ”: ”20x1 + 30x2 + 70x3<br>110 (Nutrient A)10x1 + 10x2 + 0x3 18 ( Nutrient B)50x1 + 30x2 + 0x3 90<br>(Nutrient C)6x1 + 2.5x2 + 10x3 14 ( Nutrient D)”, ” OBJECTIVE ”: ”minimize<br>41x1 + 36x2 + 96x 3”}}example2 : { ”Problem description” : ”Jordan is a chef.<br>He wants to design a diet consisting of Keb abs and Rice. Assume that each<br>serving of Rice costs $3 and contains 300 calories and 4.5 grams of protein.<br>Assume that each serving of Kebab costs $2 and contains 200 calories and 4<br>grams of protein. He’s interested in spending as little money as possible but<br>he wants to ensure that his meals have at least 2200 calories and at least 30<br>grams of protein per day. Formulate a linear programming problem that will<br>help minimize the cost of the diet. ”, ” Mathematica l Model” : {”V ARIABLES ”:<br>”Keb abs: integer, number of servings of Keb abs; Rice: integer, number of<br>servings of Rice” , ”CONSTRAINTS ”: ”200 * Ke babs + 300 * Rice >= 2200;<br>4 * Ke babs + 4.5 * Rice >= 30; Ke babs >= 0; Rice >= 0”, ”OBJECTIVE” :<br>”minimize 2 * Keb abs + 3 * Rice” } }Formulate the model strictly in the following<br>JSON format: { ”V ARIABLES ”: ”A concise description about variables and<br>its shape or type” , ” CONSTRAINTS ”: ”A mathematical formula expressing<br>all constraints” , ”OBJECTIVE” : ”A mathematical formula for the objective<br>function” } Important: 1. Learn formulation patterns from examples without<br>replicating their specif i c details2 . Base your formulation primarily on the original<br>problem description3 . Output ONLY the JSON object without any additional<br>text<br><!-- End of picture text -->

(b) With HRAG exemplars. 

**Figure 9:** Comparison of token-level attribution heatmaps. 

Page 10 of 17 

Y. Shi et al.: _Preprint submitted to Elsevier_ 

## **3.4. Token-Level Attribution Analysis** 

To investigate how the exemplars retrieved by HRAG influence the framework’s output, we employ Attention-aware Layer-wise Relevance Propagation (AttnLRP) (Achtibat et al., 2024) and follow the tokenlevel relevance analysis method proposed by (Huang et al., 2026). All experiments are conducted using Qwen2.5-7B-Instruct with the `lxt` library and 4-bit NormalFloat (NF4) quantization. 

We select a problem instance for which the model produces an incorrect answer without HRAG but a correct answer after HRAG is enabled. The analysis focuses on the modeling stage and examines how the retrieved exemplars affect the model’s internal relevance flow. In the heatmaps, darker colors indicate that the corresponding input tokens exert a stronger influence on the generated output. 

Because decoder-only Transformers employ causal self-attention, the first token in a sequence can accumulate a disproportionately large relevance score. Its key and value representations are attended to by all subsequent positions, and relevance is propagated back to this position from downstream tokens during the Layer-wise Relevance Propagation (LRP) backward pass. The first token consequently acts as a relevance sink and can obscure the contributions of other informative tokens. We therefore exclude it from the visualization to reveal more meaningful relevance patterns in the remainder of the prompt. 

We compare the following two prompt conditions: 

- **Condition 1 (with HRAG exemplars):** The prompt contains a role description, a task description with the complete problem text, two relevant exemplars retrieved from the exemplar library, and an output-format specification. 

- **Condition 2 (without exemplars):** The retrieval results are omitted, and the prompt contains only the role description, problem description, and output-format specification. 

As shown in Figure 9, without exemplars, generic prompt terms such as “variables”, “constraints”, “objective”, “optimization”, “formulation”, and “JSON”, which do not convey the specific semantics of the target problem, exert a relatively strong influence on the output. After the exemplars are introduced, the model captures structural information such as “linear programming” from the retrieved examples, which facilitates construction of the correct mathematical model. Compared with the zero-shot condition, the model also assigns greater relevance to domain-specific terms in the problem description, such as “calories” and “protein”. These results indicate that the retrieved exemplars guide the model toward both the appropriate optimization structure and the task-specific semantic information, providing further evidence of the effectiveness of the proposed HRAG mechanism. 

# **4. Experiments** 

In this section, we evaluate MIRROR on five diverse datasets to assess its optimization solving capabilities. 

## **4.1. Experimental Setup** 

_Benchmarks_ We evaluate our method on five standard benchmarks in the domain of optimization modeling: “NL4Opt” (Ramamonjison et al., 2023), Mamo (Huang et al., 2025b), IndustryOR (Chen et al., 2025), and “ComplexOR” (Xiao et al., 2023). From the Mamo benchmark, we specifically utilize two subsets: Mamo-EasyLP and Mamo-ComplexLP. According to the complexity analysis in (Xiao et al., 2025), which quantifies problem difficulty based on the number of variables and constraints, NL4Opt, Mamo-EasyLP, and ComplexOR are classified as simple tasks, whereas IndustryOR and Mamo-ComplexLP are categorized as complex tasks. Additionally, the last 163 instances of Mamo-EasyLP are reserved as part of the source data for the exemplar library , while the remaining 489 instances constitute the test set. 

Page 11 of 17 

Y. Shi et al.: _Preprint submitted to Elsevier_ 

_Baselines_ We compare MIRROR against three categories of methods: 

(1) **Traditional prompting** : Standard Chain-of-Thought (CoT) (Wei et al., 2022) prompting is applied on four models: the backbone model ( `qwen-plus-2025-09-11` ), `DeepSeek-v3` , `glm-5.1` (GLM-5-Team, 2026) , and `qwen3-30B` to evaluate conventional inference under different LLMs. 

(2) **Learning-based models** : MiniOpt, LLMOPT, OptMATH, ORLM, and SIRL—methods that fine-tune specialized models on large-scale optimization datasets for end-to-end modeling. 

(3) **Agent-based methods** : OptiMUS, ORMind, OptiTree and Chain-of-Experts (COE), which use multi-agent LLM frameworks with division-of-labor collaboration. All are implemented using the same backbone model as our method for fair comparison. 

Additionally, we validate MIRROR’s effectiveness on a smaller model: `qwen3-30b-a3b-instruct-2507` (abbreviated as qwen3-30B), comparing CoT prompting against the full MIRROR framework. 

_Implementation Details_ Except for the small-model ablation, all experiments use `qwen-plus-2025-09-11` as the backbone model, with temperature set to 0 for deterministic and reproducible outputs. Generated code is formatted for the Gurobi solver. 

_Evaluation Metric_ We adopt **pass@1** (Chen et al., 2021) as the primary metric, defined as the proportion of problem instances for which the model generates a correct solution in a single attempt. A prediction _̂ 𝑦_ is considered correct if it satisfies the relative error tolerance with respect to the ground-truth optimal value _𝑦_<sup>∗</sup> : 



## **4.2. Results Analysis** 

_Overall Performance_ MIRROR achieves the highest rank among all fully evaluated methods in Table 1, setting a new state of the art among multi-agent approaches for end-to-end optimization modeling. Notably, this performance is attained without any task-specific fine-tuning, relying solely on collaborative reasoning, hierarchical retrieval, and iterative adaptive revision. 

_Advancement over Agent-based Baselines_ Among existing agent-based methods, OptiTree achieves the highest macro-average accuracy (69.58%), outperforming OptiMUS (53.57%), COE (68.20%), and ORMind (61.28%). MIRROR surpasses all of them, exceeding OptiTree on four out of five benchmarks and achieving improvements of +6.0% on IndustryOR and +5.6% on ComplexOR. This consistent improvement demonstrates that the IAR and HRAG mechanisms capture complex constraints and non-standard problem structures more effectively than previous agent designs. 

Table 2 reports the token consumption of various agent-based methods on the IndustryOR and ComplexOR datasets. From the results, we can observe that: (1) MIRROR consumes fewer tokens than COE and OptiMUS on both datasets; on IndustryOR, its token usage is 70% of COE’s and 27% of OptiMUS’s; (2) Although ORMind and OptiTree consume fewer total tokens than MIRROR on both datasets, MIRROR achieves accuracy improvements over ORMind by 6 percentage points on IndustryOR and by 16.67 percentage points on ComplexOR, with the advantage on ComplexOR being particularly pronounced. Moreover, MIRROR also outperforms OptiTree by 6 percentage points on IndustryOR and by 5.55 percentage points on ComplexOR. In many practical industrial problems, accuracy is of paramount importance, as erroneous answers can lead to severe consequences. 

_Superiority to Learning-based Models_ MIRROR requires no task-specific training yet outperforms all learning-based baselines in terms of average performance: MiniOpt (14B), LLMOPT (14B), OptMATH 

Page 12 of 17 

Y. Shi et al.: _Preprint submitted to Elsevier_ 

**Table 1** 

Accuracy (pass@1, %) of different methods across benchmark datasets. 

|**Category**|**Models / Methods **|**NL4Opt **|<sup>**Mamo**</sup><br>**EasyLP**|**Mamo**<br>**ComplexLP **|<sup>**IndustryOR **</sup>|<sup>**ComplexOR **</sup>|<sup>**Macro**</sup><br>**Avg**|**Rank**|
|---|---|---|---|---|---|---|---|---|
||Backbone model|72.24|85.07|44.83|46.00|44.44|58.52|9|
|_Traditional_|Deepseek-v3|73.88|84.66|57.14|51.00|55.56|64.45|5|
|_prompting_|glm-5.1|77.96|89.16|56.16|**58.00**|50.00|66.26|4|
||qwen3-30B|68.57|85.28|30.54|41.00|33.33|51.74|12|
||MiniOpt (14B)<sup>*</sup><br>|92.17|90.80|33.65|27.00|61.11|60.95|8|
|_Learnin-based_|LLMOPT (14B)<sup>*</sup><br>|80.28|89.53|44.08|29.00|35.29|55.64|10|
|_g_<br>_methods_|OptMATH (7B)<sup>*</sup><br>|78.70|84.20|34.12|19.00|33.33|49.87|13|
||ORLM (8B)<sup>*</sup><br>|85.70|82.30|37.40|38.00|—|—|—|
||SIRL (32B)<sup>*</sup>|**98.00**|**94.60**|61.10|48.00|—|—|—|
||OptiMUS|57.96|85.28|45.81|51.00|27.78|53.57|11|
|_Atbd_|COE|84.90|87.93|57.63|55.00|55.56|68.20|3|
|_gen-ase_<br>_thd_|ORMind|77.55|81.19|52.22|51.00|44.44|61.28|7|
|_meos_|OptiTree|87.77|86.57|67.00|51.00|55.56|69.58|2|
|**_Ours_**|MIRROR<br>|86.50|87.30|**67.50**|57.00|**61.11**|**71.88**|**1**|
||MIRROR (30B)|82.40|86.90|52.70|53.00|44.44|63.89|6|



All agent-based methods use the default model. Bold denotes the current state-of-the-art (SOTA); “—” indicates unreported results; values marked with<sup>*</sup> are from other papers: SIRL and ORLM from their original works, and all other learning-based methods from MiniOpt. 

**Table 2** 

Comparison of total token consumption and accuracy across agent-based methods. 

|**Model/Variant**|**Comp**|**lexOR**|**Indust**|**ryOR**|
|---|---|---|---|---|
||**Tokens**|**Acc.**|**Tokens**|**Acc.**|
|MIRROR|209k|61.11%|1068k|57.00%|
|COE|352k|55.56%|1527k|55.00%|
|ORMind|106k|44.44%|743k|51.00%|
|OptiMUS|410k|27.78%|3953k|51.00%|
|OptiTree|124k|55.56%|732k|51.00%|



(7B), ORLM (8B), and SIRL (32B). On the challenging Mamo-ComplexLP and IndustryOR benchmarks, it achieves 67.50% and 57.00% accuracy, respectively—surpassing the strongest prior model, SIRL (32B), by 6.40 and 9.00 percentage points. This shows that structured agent collaboration can excel at complex optimization modeling without large-scale supervised fine-tuning. 

_Advantage Over Traditional Prompting Approach_ MIRROR, using the backbone model, achieves a macroaverage score of 71.88%, outperforming Chain-of-Thought (CoT) prompting on the same model (58.52%) by 13.4 points. It also exceeds CoT applied to the stronger `DeepSeek-v3` model (64.45%) and `glm-5.1` model (66.26%). 

_Effective Transfer to Small Model_ When applied to qwen3-30B, MIRROR boosts macro-average accuracy from 51.74% (achieved by CoT) to 63.89%—a 12.15-point improvement without fine-tuning, confirming its plug-and-play utility for accessible models. 

Page 13 of 17 

Y. Shi et al.: _Preprint submitted to Elsevier_ 

## **4.3. Ablation Study** 

We conduct an ablation study on the five datasets: NL4Opt, Mamo-EasyLP, Mamo-ComplexLP, IndustryOR, and ComplexOR. We evaluate four variants: the full MIRROR (with both IAR and HRAG), and three ablated versions—removing only IAR, only HRAG, or both. As shown in Table 3, the full model achieves the highest macro-average accuracy of 71.88%, outperforming the w/o HRAG variant (67.90%), w/o IAR (71.14%), and w/o Both (65.82%). This confirms that both mechanisms contribute to performance, with HRAG yielding a larger gain. 

**Table 3** 

Ablation study of MIRROR components (Accuracy (pass@1, %)). 

|**Variant**|**NL4Opt**|**Mamo EasyLP**|**Mamo ComplexLP**|**IndustryOR**|**ComplexOR**|**Macro Avg**|
|---|---|---|---|---|---|---|
|MIRROR|**86.50**|**87.30**|**67.50**|**57.00**|**61.11**|**71.88**|
|W/o IAR|85.70|86.90|67.00|55.00|61.11|71.14|
|W/o HRAG|85.30|86.70|63.50|54.00|50.00|67.90|
|W/o Both|84.10|86.50|62.05|52.00|44.44|65.82|



We further decompose errors into wrong answer rate (executable solver code that generates an incorrect numerical result) and compile error rate (syntactically invalid solver code that fails to execute), as these reflect distinct failure modes in optimization modeling: the former indicates flawed reasoning, while the latter reveals structural or grammatical mistakes in the generated solver code. Figure 10 visualizes these two error types across configurations. The light-colored regions in Figure 10a represent the compile error rate. Since the wrong answer rates are significantly higher than the compile error rates in most cases across the datasets and mechanisms, the light-colored regions for the former are omitted in Figure 10b to ensure a clearer visualization of the latter. 



<!-- Start of picture text -->
 W / o B o t h<br> W / o H R A<br> W / o I A<br> M I R R O<br>4<br>2<br>N L 4 O p a m o a m o I n d u s t r y O C o m p l e x O<br>E a s y L C o m p l e x L<br>D a t a s e<br>(a) Wrong answer rate across datasets and methods.<br>(g Ar Rt eeronnsaw<br><!-- End of picture text -->



<!-- Start of picture text -->
 W / o B o t h<br>3<br> W / o H R A<br> W / o I A<br> M I R R O<br>2<br>2<br>1<br>1<br>N L 4 O p a m o a m o I n d u s t r y O C o m p l e x O<br>E a s y L C o m p l e x L<br>D a t a s e<br>���������������������<br><!-- End of picture text -->

(b) Compile error rate across datasets and methods. 

**Figure 10:** Ablation study of MIRROR. 

_For Wrong Answer Rate_ all datasets except ComplexOR show a consistent decrease or remain stable from the w/o Both configuration to single-mechanism variants and finally to the full model, indicating that both mechanisms help produce correct solutions. Notably, removing HRAG leads to a larger increase in wrong answers than removing IAR; for example, on IndustryOR, the wrong answer rate is 3.00% higher when only 

Page 14 of 17 

Y. Shi et al.: _Preprint submitted to Elsevier_ 

HRAG is removed compared to when only IAR is removed. This suggests that HRAG enhances both problem modeling and solver code generation through its two-stage retrieval strategy, thereby improving the accuracy of the final results. 

_For Compile Error Rate_ the opposite trend is observed: on NL4Opt, Mamo-EasyLP, and IndustryOR, the w/o IAR variant incurs higher compile errors than w/o HRAG, demonstrating that the IAR mechanism’s closedloop iterative adaptive revision process effectively identifies and resolves compilation failures. Averaged across all datasets, the compile error rate decreases from 8.06% in the w/o Both setting to 2.60% with IAR only and 2.65% with HRAG only, and further declines to 1.91% when both mechanisms are used. This highlights their complementary contributions to generating valid and executable optimization models and solver code. 

_Agent Ablation Study_ We perform a more fine-grained ablation study to analyze the specific contributions of each agent. We conduct experiments on representative datasets as follows. Since the Code Generation Agent is responsible for generating the final code and the code is required for compilation, we only analyzed three agents during the generation process: the Parameter Extraction Agent (P), the Modeling Advisor Agent (A), and the Mathematical Modeling Agent (M) (abbreviated as P, A, and M respectively in the experimental table). The ablation study selects two representative test sets, IndustryOR and ComplexOR. The results are shown in Table 4. 

**Table 4** 

Ablation study on IndustryOR and ComplexOR datasets. 

|**Dataset**|**Configuration**|**Accuracy**|**Wrong Answer Rate**|**Compile Error Rate**|
|---|---|---|---|---|
|**IndustryOR**|Full|**52.00%**|44.00%|**4.00%**|
||W/o P|51.00%|42.00%|7.00%|
||W/o A|47.00%|46.00%|7.00%|
||W/o M|50.00%|42.00%|8.00%|
|**ComplexOR**|Full|**44.44%**|22.22%|**27.78%**|
||W/o P|38.89%|22.22%|38.89%|
||W/o A|38.89%|22.22%|38.89%|
||W/o M|38.89%|27.78%|33.33%|



Parameter Extraction Agent (P): After removing P, the compile error rate on ComplexOR increases from 27.78% to 38.89% (↑11.11%), and on IndustryOR from 4.00% to 7.00% (↑3.00%). Removing P leads to an increase in compile error rates on both datasets, indicating that P makes a universal contribution to reducing compilation errors. 

Modeling Advisor Agent (A): After removing A, the accuracy on IndustryOR decreases by 5% (52% → 47%), with the wrong answer rate increasing by 2% (44% →46%); on ComplexOR, accuracy decreases by 5.55% (44.44% →38.89%), while the wrong answer rate remains unchanged. Removing A leads to a decrease in accuracy on both datasets, indicating that A plays an important role in improving final solution accuracy. 

Mathematical Modeling Agent (M): After removing M, the compile error rate on ComplexOR increases from 27.78% to 33.33% (↑5.55%), with accuracy decreasing by 5.55% (44.44% →38.89%) and wrong answer rate increasing by 5.56% (22.22% →27.78%). A consistent performance degradation is also observed on the IndustryOR dataset. Removing M leads to negative impacts on either compilability or solution correctness across both datasets, indicating that M plays a key role in ensuring both code compilability and mathematical fidelity. 

In summary, removing any of the three agents P, A, or M leads to negative changes in at least one metric, verifying the necessity of all three agents within the framework. 

Page 15 of 17 

Y. Shi et al.: _Preprint submitted to Elsevier_ 

# **5. Conclusion** 

We present MIRROR, a training-free multi-agent framework for automated operations research (OR) modeling that bridges the gap between natural language problem descriptions and formal mathematical models with executable solver code. By integrating Hierarchical Retrieval-Augmented Generation (HRAG) for dynamic exemplar retrieval and an Iterative Adaptive Revision (IAR) mechanism for execution-driven selfcorrection, MIRROR effectively mitigates the hallucination and fragility of general-purpose large language models in specialized OR tasks. Experiments show that MIRROR achieves strong performance across diverse OR modeling benchmarks, attaining state-of-the-art results on complex industrial datasets and significantly boosting the capabilities of small open-source language models—without any task-specific training. This work paves the way toward accessible, reliable, and scalable AI-assisted decision-making for real-world operations research applications. 

# **CRediT authorship contribution statement** 

**Yifan Shi:** Conceptualization; Data curation; Investigation; Methodology; Software; Writing – original draft; Writing – review & editing; Validation; Visualization. **Jiayi Wang:** Writing – original draft; Visualization; Investigation; Methodology; Software; Validation; Writing – review & editing; Data curation. **Minyi Wu:** Data curation; Investigation; Software; Validation. **Ye Fan:** Data curation; Investigation; Software; Validation. **Jialong Shi:** Project administration; Supervision; Writing – review & editing; Resources. **Jianyong Sun:** Project administration; Supervision; Writing – review & editing; Resources. 

# **References** 

- Achtibat, R., Hatefi, S.M.V., Dreyer, M., Jain, A., Wiegand, T., Lapuschkin, S., Samek, W., 2024. Attnlrp: attention-aware layer-wise relevance propagation for transformers. arXiv preprint arXiv:2402.05602 . 

Adams, D., Suri, G., Chali, Y., 2022. Combining state-of-the-art models with maximal marginal relevance for few-shot and zero-shot multi-document summarization. arXiv preprint arXiv:2211.10808 . 

- Ahmaditeshnizi, A., Gao, W., Udell, M., 2024. OptiMUS: Scalable optimization modeling with (MI)LP solvers and large language models, in: International Conference on Machine Learning, PMLR. pp. 577–596. 

- Cannas, V.G., Ciano, M.P., Saltalamacchia, M., Secchi, R., 2024. Artificial intelligence in supply chain and operations management: A multiple case study research. International Journal of Production Research 62, 3333–3360. 

Chen, M., Tworek, J., Jun, H., Yuan, Q., de O. Pinto, H.P., Kaplan, J., Edwards, H., Burda, Y., Joseph, N., Brockman, G., et al., 2021. Evaluating large language models trained on code. arXiv preprint arXiv:2107.03374 . 

Chen, Y., Xia, J., Shao, S., Ge, D., Ye, Y., 2025. Solver-informed RL: Grounding large language models for authentic optimization modeling, in: The 

Thirty-ninth Annual Conference on Neural Information Processing Systems. URL: `https://openreview.net/forum?id=80L235oVBe` . 

DeepSeek-AI, Liu, A., Feng, B., Xue, B., Wang, B., Wu, B., Lu, C., Zhao, C., Deng, C., Zhang, C., Ruan, C., Dai, D., Guo, D., Yang, D., Chen, D., Ji, 

D., Li, E., Lin, F., Dai, F., ..., Pan, Z., 2025. DeepSeek-V3 technical report. arXiv preprint arXiv:2412.19437 `arXiv:2412.19437` . 

Di, Z., Zhao, K., Shu, X., Wen, Y., Shi, Q., Qian, H., Li, B., Lu, X., Wang, X., Zhou, J., Tang, K., Yu, Y., 2026. Miniopt: Reasoning to model and 

solve general optimization problems with limited resources. URL: `https://openreview.net/forum?id=nIWCUVJ6OU` . 

- Ding, Z., Tan, Z., Zhang, J., Chen, T., 2025. OR-R1: Automating modeling and solving of operations research optimization problem via test-time reinforcement learning. arXiv preprint arXiv:2511.09092 . 

- Ge, D., Huangfu, Q., Wang, Z., Wu, J., Ye, Y., 2024. Cardinal optimizer (COPT) user guide. arXiv preprint arXiv:2208.14314 . 

GLM-5-Team, 2026. Glm-5: from vibe coding to agentic engineering. URL: `https://arxiv.org/abs/2602.15763` , `arXiv:2602.15763` . 

Guo, D., Yang, D., Zhang, H., Song, J., Wang, P., Zhu, Q., Xu, R., Zhang, R., Ma, S., Bi, X., et al., 2025. DeepSeek-R1 incentivizes reasoning in LLMs through reinforcement learning. Nature 645, 633–638. 

Gurobi Optimization, LLC, 2024. Gurobi optimizer reference manual. URL: `https://www.gurobi.com` . reference Manual. 

- Huang, C., Tang, Z., Hu, S., Jiang, R., Zheng, X., Ge, D., Wang, B., Wang, Z., 2025a. ORLM: A customizable framework in training large models for automated optimization modeling. Operations Research . 

- Huang, Q., Ye, F., Shahane, A., Bäck, T., van Stein, N., 2026. From heuristic selection to automated algorithm design: Llms benefit from strong priors. arXiv preprint arXiv:2603.02792 . 

- Huang, T., Sun, Z., Jin, Z., Li, G., Lyu, C., 2024. Knowledge-aware code generation with large language models, in: 2024 IEEE/ACM 32nd International Conference on Program Comprehension (ICPC), IEEE Computer Society. pp. 52–63. 

- Huang, X., Shen, Q., Hu, Y., Gao, A., Wang, B., 2025b. Large language models for mathematical modeling: Towards bridging the gap between natural and mathematical languages. arXiv preprint arXiv:2405.13144 . 

- Jiang, C., Shu, X., Qian, H., Lu, X., Zhou, J., Zhou, A., Yu, Y., 2025. LLMOPT: Learning to define and solve general optimization problems from scratch, in: International Conference on Learning Representations, pp. 101580–101606. 

Page 16 of 17 

Y. Shi et al.: _Preprint submitted to Elsevier_ 

Jimenez, C.E., Yang, J., Wettig, A., Yao, S., Pei, K., Press, O., Narasimhan, K., 2024. SWE-bench: Can language models resolve real-world GitHub issues?, in: International Conference on Learning Representations. 

Liang, K., Lu, Y., Mao, J., Sun, S., Yang, C., Zeng, C., Jin, X., Qin, H., Zhu, R., Teo, C.P., 2026. LLM for large-scale optimization model auto-formulation: Bridging flexibility and standardization via agentic workflow. arXiv preprint arXiv:2601.09635 . 

- Liu, F., Yang, Z.R., Liu, C., Song, T., Gao, X., Liu, H., 2025. MM-agent: LLM as agents for real-world mathematical modeling problem, in: 2nd AI for Math Workshop @ ICML 2025. URL: `https://openreview.net/forum?id=QyKBf7X98d` . 

- Liu, H., Wang, J., Cai, Y., Han, X., Kuang, Y., Hao, J., 2026. OptiTree: Hierarchical thoughts generation with tree search for LLM optimization modeling, in: The Thirty-ninth Annual Conference on Neural Information Processing Systems. URL: `https://openreview.net/forum?id= Ej20yjWMCj` . 

- Liu, J., Shen, D., Zhang, Y., Dolan, B., Carin, L., Chen, W., 2022. What makes good in-context examples for GPT-3?, in: Proceedings of the 3rd Workshop on Knowledge Extraction and Integration for Deep Learning Architectures, pp. 100–114. URL: `https://aclanthology.org/2022. deelio-1.10/` . 

- Lu, H., Xie, Z., Wu, Y., Ren, C., Chen, Y., Wen, Z., 2025. OptMATH: A scalable bidirectional data synthesis framework for optimization modeling. arXiv preprint arXiv:2502.11102 . 

- Novikov, A., Vu, N., Eisenberger, M., Dupont, E., Huang, P.S., Wagner, A.Z., Shirobokov, S., Kozlovskii, B., Ruiz, F.J.R., Mehrabian, A., et al., 2025.˜ AlphaEvolve: A coding agent for scientific and algorithmic discovery. arXiv preprint arXiv:2506.13131 . 

- OpenAI, Achiam, J., Adler, S., Agarwal, S., Ahmad, L., Akkaya, I., et al., 2024a. GPT-4 technical report. arXiv preprint arXiv:2303.08774 . 

OpenAI, Jaech, A., Kalai, A., Lerer, A., Richardson, A., El-Kishky, A., et al., 2024b. OpenAI o1 system card. arXiv preprint arXiv:2412.16720 . 

- Ramamonjison, R., Yu, T., Li, R., Li, H., Carenini, G., Ghaddar, B., He, S., Mostajabdaveh, M., Banitalebi-Dehkordi, A., Zhou, Z., et al., 2023. NL4Opt competition: Formulating optimization problems based on their natural language descriptions, in: NeurIPS 2022 Competition Track, PMLR. pp. 189–203. 

- Ren, Z.Z., Shao, Z., Song, J., Xin, H., Wang, H., Zhao, W., Zhang, L., Fu, Z., Zhu, Q., Yang, D., et al., 2025. DeepSeek-Prover-V2: Advancing formal mathematical reasoning via reinforcement learning for subgoal decomposition. arXiv preprint arXiv:2504.21801 . 

- Tang, Z., Ye, Z., Huang, C., Huang, X., Li, C., Li, S., Chen, G., Yan, M., Wang, Z., Zha, H., et al., 2025. CALM before the STORM: Unlocking native reasoning for optimization modeling. arXiv preprint arXiv:2510.04204 . 

- Thind, R., Sun, Y., Liang, L., Yang, H., 2026. OptimAI: Optimization from natural language using LLM-powered AI agents. URL: `https: //openreview.net/forum?id=JtgZkVdAIP` . 

Wang, X., Chen, Y., Yuan, L., Zhang, Y., Li, Y., Peng, H., Ji, H., 2024. Executable code actions elicit better LLM agents, in: Proceedings of the 41st International Conference on Machine Learning, PMLR. pp. 50208–50232. 

- Wang, Z., Chen, B., Huang, Y., Cao, Q., He, M., Fan, J., Liang, X., 2025. ORMind: A cognitive-inspired end-to-end reasoning framework for operations research. arXiv preprint arXiv:2506.01326 . 

- Wei, J., Wang, X., Schuurmans, D., Bosma, M., Xia, F., Chi, E., Le, Q.V., Zhou, D., et al., 2022. Chain-of-thought prompting elicits reasoning in large language models. Advances in Neural Information Processing Systems 35, 24824–24837. 

- Wu, Y., Zhang, Y., Wu, Y., Wang, Y., Zhang, J., Cheng, J., 2025. Step-Opt: Boosting optimization modeling in LLMs through iterative data synthesis and structured validation. arXiv preprint arXiv:2506.17637 . 

- Xiao, Z., Xie, J., Xu, L., Guan, S., Zhu, J., Han, X., Fu, X., Yu, W., Wu, H., Shi, W., Kang, Q., Duan, J., Zhong, T., Yuan, M., Zeng, J., Wang, Y., Chen, G., Zhang, D., 2025. A survey of optimization modeling meets LLMs: Progress and future directions, in: Proceedings of the Thirty-Fourth International Joint Conference on Artificial Intelligence (IJCAI-25), pp. 10742–10750. doi: `10.24963/ijcai.2025/1192` . 

- Xiao, Z., Zhang, D., Wu, Y., Xu, L., Wang, Y.J., Han, X., Fu, X., Zhong, T., Zeng, J., Song, M., et al., 2023. Chain-of-experts: When LLMs meet complex operations research problems, in: The Twelfth International Conference on Learning Representations. 

- Xu, K., Mao, Y., Guan, X., Feng, Z., 2025. Web-Bench: A LLM code benchmark based on web standards and frameworks. arXiv preprint arXiv:2505.07473 . 

- Yang, A., Li, A., Yang, B., Zhang, B., Hui, B., Zheng, B., Yu, B., Gao, C., Huang, C., Lv, C., et al., 2025a. Qwen3 technical report. arXiv preprint arXiv:2505.09388 . 

- Yang, A., Zhang, B., Hui, B., Gao, B., Yu, B., Li, C., Liu, D., Tu, J., Zhou, J., Lin, J., et al., 2024. Qwen2.5-Math technical report: Toward mathematical expert model via self-improvement. arXiv preprint arXiv:2409.12122 . 

- Yang, Z., Wang, Y., Huang, Y., Guo, Z., Shi, S., Han, X., Feng, L., Song, L., Liang, X., Tang, J., 2025b. Optibench meets resocratic: Measure and improve llms for optimization modeling, in: International Conference on Learning Representations, pp. 24726–24759. 

- Zhang, B., Luo, P., 2025. OR-LLM-Agent: Automating modeling and solving of operations research optimization problem with reasoning large language model. arXiv preprint arXiv:2503.10009 . 

- Zhou, C., Xu, T., Lin, J., Ge, D., 2025. StepORLM: A self-evolving framework with generative process supervision for operations research language models. arXiv preprint arXiv:2509.22558 . 

Page 17 of 17 

Y. Shi et al.: _Preprint submitted to Elsevier_ 

