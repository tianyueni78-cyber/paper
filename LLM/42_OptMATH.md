# OptMATH: A Scalable Bidirectional Data Synthesis Framework for Optimization Modeling 

Hongliang Lu<sup>1</sup><sup>_,∗_</sup> , Zhonglin Xie<sup>2</sup><sup>_,∗_</sup> , Yaoyu Wu<sup>1</sup> , Can Ren<sup>3</sup> , Yuxuan Chen<sup>3</sup> , Zaiwen Wen<sup>2</sup><sup>_,†_</sup> 

> 1College of Engineering, Peking University 

> 2Beijing International Center for Mathematical Research, Peking University 

> 3School of Mathematics Science, Peking University 

> _∗_ Equal contribution 

> _†_ Corresponding author: wenzw@pku.edu.cn 

### **Abstract** 

proach. Our dataset is publicly available at `https://github.com/AuroraLHL/OptMATH` . 

Despite the rapid development of large language models (LLMs), a fundamental challenge persists: the lack of high-quality optimization modeling datasets hampers LLMs’ robust modeling of practical optimization problems from natural language descriptions (NL). This data scarcity also contributes to the generalization difficulties experienced by learning-based methods. To address these challenges, we propose a scalable framework for synthesizing a high-quality dataset, named OptMATH. Starting from curated seed data with mathematical formulations (MF), this framework automatically generates problem data (PD) with controllable complexity. Then, a back-translation step is employed to obtain NL. To verify the correspondence between the NL and the PD, a forward modeling step followed by rejection sampling is used. The accepted pairs constitute the training part of OptMATH. Then a collection of rejected pairs is identified and further filtered. This collection serves as a new benchmark for optimization modeling, containing difficult instances whose lengths are much longer than these of NL4OPT and MAMO. Through extensive experiments, we demonstrate that models of various sizes (0.5B-32B parameters) trained on OptMATH achieve superior results on multiple modeling benchmarks, thereby validating the effectiveness and scalability of our ap- 

### **1 Introduction** 

Automatic translation of natural language descriptions of optimization problems into solverready formats is a critical step in democratizing access to optimization techniques. This capability would enable individuals without expertise in optimization to leverage the power of optimization for solving real-world problems across various domains, including logistics [32], finance [18], and engineering [64]. Known as optimization modeling, this task has long been challenging due to the inherent ambiguity of natural language and the need for a deep understanding of optimization modeling principles. The manual process of formulating an optimization problem typically involves iterative refinement and demands significant mastery of the relevant techniques, making it time-consuming and inaccessible to many practitioners. 

Recent advances in Large Language Models (LLMs), such as ChatGPT [14], GPT4 [59], and OpenAI’s o1 [58], have demonstrated remarkable capabilities in understanding natural language and performing complex reasoning tasks. Notably, the introduction of o1 has significantly enhanced the performance of LLMs in mathematical reasoning, achieving state-of-the-art results on challeng- 

1 

ing datasets including AIME (2024), GPQA, and CodeForces. However, optimization modeling presents unique challenges. Unlike gradeschool mathematics, where problems typically have a single correct solution, optimization problems can often be approached using multiple valid models, making the task semi-openended. Furthermore, optimization frequently relies on a vast body of empirical knowledge that is less formally structured than purely mathematical concepts. As a result, research has shown that directly applying LLMs to optimization modeling tasks yields suboptimal outcomes [63]. 

**LLMs for Optimization Modeling.** To address this issue, recent efforts have explored various strategies. Research on leveraging LLMs for optimization modeling typically follows two main approaches. The first uses prompt engineering techniques to guide LLMs in generating or refining optimization models, without modifying the underlying model parameters. Examples include the NL4Opt competition [63], which aims to extract optimization formulations from natural language descriptions, and OptiMUS [3], which proposes an agent-based prompt engineering method. More recently, Autoformulation [6] combines Monte Carlo tree search with LLMs to address optimization modeling. While these methods rely heavily on the base capabilities of generalpurpose LLMs, they do not yield fundamental advancements beyond refined prompting. 

The second approach centers on fine-tuning, wherein model parameters are adapted using specially curated or synthesized optimization datasets. ORLM [71] introduces OR-Instruct, a data augmentation framework for optimization problems, and demonstrates performance gains via Supervised Fine-Tuning on a foundation model. LLMOPT [44] likewise applies a multi-instruction fine-tuning strategy and self-correction mechanisms. However, most of these methods generate small amounts of synthetic training data—often of inconsistent quality and insufficient complexity. Consequently, their ability to generalize to more sophisticated optimization tasks is limited. 

**LLM-Based Data Synthesis for Op-** 

**timization.** Data synthesis methods have become essential for addressing data scarcity and enhancing the performance of LLMs. According to [75], these methods can be broadly categorized into two main approaches: data augmentation and data synthesis. ORInstruct [71, 76] exemplifies a data augmentation approach, following the self-instruct framework to expand existing datasets. On the other hand, MILP-Evolve [49] introduces an evolutionary framework designed to generate diverse mixed-integer linear programming (MILP) problems using LLMs. While MILPEvolve represents a significant step forward in synthetic data generation, it does not address the critical challenge of translating natural language descriptions into mathematical optimization models. 

**Instance Generation for Optimization.** Recent research in MILP instance generation has evolved along two primary axes: learning-based structural synthesis and rulebased distribution expansion. The learningbased paradigm addresses data scarcity by developing generative models that preserve instance hardness and constraints. Examples include the bipartite graph variational autoencoder framework proposed by [31], the block decomposition operators for constraint matrices introduced in [52], the duality-driven feasibility guarantees established by [74], and the adaptive constraint modification mechanisms developed in [36]. The rule-based approach leverages instance space analysis techniques [4, 70, 5] to guide the generation of more diverse instance distributions [67, 9]. Alternatively, it may rely on manually selected features to control the characteristics of the generated instances [10]. 

**Our Contributions.** We propose a scalable bidirectional synthesis framework that addresses the critical challenge of data scarcity in optimization modeling through _triplet-aligned (NL, MF, PD) data generation_ and rigorous validation. Our framework uniquely integrates a closed-loop workflow with _optimal value matching_ , ensuring semantic equivalence between NL, MF, and PD. This approach demonstrates exceptional scalability. The frame- 

2 

work’s domain adaptability is evidenced by coverage of 10+ real-world applications (e.g., logistics, energy, finance) through 53 seed generators, with manual analysis confirming 99.6% equivalence accuracy across all triplets. 

We introduce _OptMATH-Train_ , a large scale verified optimization modeling dataset containing rigorously validated (NL, MF, PD) triplets. Each triplet undergoes three-stage quality control: mathematical consistency checks (MF-to-PD compilation), semantic fidelity validation (PD-to-NL backtranslation), and solution equivalence verification through solver-based rejection sampling. From rejected instances, we curate _OptMATH-Bench_ , a challenging benchmark comprising “hard instances” characterized by extended natural language contexts (2.9 _×_ longer than MAMO EasyLP) and complex constraints. We further span it using various problems including LP, MILP, IP, NLP, SOCP. This benchmark provides the standardized evaluation for longcontext optimization modeling. 

Finally, extensive experiments demonstrate the efficacy of our framework. Models trained on the OptMATH-Train dataset achieve stateof-the-art performance on multiple established modeling benchmarks, including NL4OPT and MAMO. These results definitively validate the effectiveness and scalability of our framework for generating high-quality optimization modeling datasets. 

### **2 Backgrounds & Overview** 

In mathematical optimization theory, a canonical optimization problem can be formulated as: 



where **x** _∈_ R<sup>_n_</sup> denotes the decision vector. The objective function _g_ : R<sup>_n_</sup> _→_ R assigns a scalar value to each candidate solution, which we seek to minimize. The constraint functions _ci_ : R<sup>_n_</sup> _→_ R define the feasible region through equality constraints indexed by _E_ and inequality constraints indexed by _I_ . 

To formalize the optimization modeling problem, we define several key concepts and illustrate them using a concrete example in Appendix D.1. For a specific optimization problem, we define NL as the _natural language description_ , which corresponds to the “Input-Natural Language Description” in the example. We represent the LP/MPS file, the concrete mathematical expression (corresponding to the “Output-Instance Formulation”), and any other solver-ready formats, such as executable Python code with Gurobi shown in Appendix D.1, as _problem data_ (PD). A common characteristic of these representations is that they allow us to obtain the optimal value of the problem by invoking a solver based on the PD. _Mathematical formulation_ (MF) refers to formulation where concrete numbers are not yet specified, corresponding to the “Output-General Formulation” in the example. We emphasize that, in subsequent sections, we may use different forms of PD. However, these forms essentially carry the same information about the problem and can be inferred from the context without ambiguity. We use different forms of PD to facilitate their integration into the workflow and to enhance clarity in various contexts. 

Modern solvers such as Gurobi and Mosek [38, 56] can efficiently solve problems stored with PDs using algorithms like interior-point methods [45]. However, practical challenges remain. In real-world applications, one of the main difficulties lies in converting informal NLs of problems into precise MFs. Moreover, extracting the PDs from NLs poses an additional significant challenge. Traditionally, this process has required deep optimization expertise [11], but recent advances in LLMs offer promising opportunities to automate this transformation. 

Let _Aθ_ represent an LLM parameterized by _θ_ . The formulation for increasing the modeling capability of the LLM can be expressed as: 





3 

where `prompt` M is a modeling prompt template mapping NL to MF<sup>_′_</sup> and PD<sup>_′_</sup> . The quality metric _Q_ evaluates the generated (MF<sup>_′_</sup> _,_ PD<sup>_′_</sup> ) pairs based on the verified (NL _,_ MF _,_ PD) triplet. Constraint (2.3) formalizes the automated formulation process (Autoformulation), as depicted in the example in Appendix D.1. Optimizing _θ_ relies on having a large corpus of high-quality triplets (NL _,_ MF _,_ PD). To address this requirement, we propose a systematic framework for generating synthetic training data that maintains mathematical rigor. 

**An Overview of Our Pipeline.** The pipeline of our framework is presented in Figure 1. In the reverse data generation phase, we collect optimization problems from two sources: (1) LP/MPS files from challenging benchmarks such as MIPLIB 2017 [34] and netlib [57, 29], and (2) over 50 expert-curated seed problem generators covering diverse optimization scenarios. Through our carefully designed backtranslation pipeline, we leverage both the LP files and their MFs to generate high-quality NLs of optimization problems. Notably, using an LLM-based feedback workflow with evaluation, our collected generators can produce tremendous PDs with controllable varying difficulty levels. This enables us to effectively address the data scarcity challenge in training learning-based optimization methods. 

In the forward modeling and evaluation process, we utilize our trained AutoFormulator to translate the generated NLs back into PDs. Specifically, in this phase, all PDs are represented as solver code, which can then be exported as LP files. We then implement a rigorous rejection sampling strategy, where only instances whose optimal objective values match between the original and generated LP files are retained. This equivalence-based filtering mechanism ensures the high quality of our OptMATH-Train dataset by guaranteeing the semantic consistency of each instance. 

Building upon the high-quality instances obtained through rejection sampling, we employ various data augmentation strategies to further enhance the diversity and coverage of our 

dataset. This enriched collection of training pairs is then utilized to fine-tune a foundation model, leading to AutoFormulator, a specialized model specifically designed for automated mathematical optimization modeling. 

### **3 Feedback-Driven PD Generation** 

The mature development of the optimization community has provided us with access to many high-quality optimization PDs. These PDs are typically stored in standardized formats like MPS or LP files. To effectively leverage these resources, we began by curating over 50 seed problem classes sourced from a variety of optimization journals and websites (see Appendix A.2 for details). For each _i_ -th problem class, we developed a corresponding instance generator _Gi_ . This generator takes a problem-specific configuration as input and outputs a probability distribution over PDs. The distribution is designed to produce PDs with varying scales and complexities, which are controllable through adjustable configurations. Before delving into the controlled generation process for the PDs, we first explain how the complexity of PDs can be measured. 

**Measuring the Modeling Complexity.** The complexity of formulating and solving a MIP problem depends on modeling choices such as the types of variables, the forms of constraints, and auxiliary modeling techniques employed. We introduce a scoring function _S_ defined as: 



where _N_ bin _, N_ int _, N_ cont are the number of binary, integer, and continuous variables, respectively. Similarly, _N_ lin _, N_ indic _, N_ quad _, N_ gen represent the number of linear, indicator, quadratic, and general nonlinear constraints. The term _f_ BigM is a factor reflecting the frequency of Big-M formulations, and _L_ expr is the average number of terms per constraint and the objective function, which captures the structural information of the expressions. 

4 



<!-- Start of picture text -->
Step1: Reverse Data Generation Step2: Forward Modeling and Evaluation<br>Quality Filtering<br>Rejection Samping<br>Benchmark Generator  Generated LP Files  LP Files<br>(Hard LP Files)<br>Reject<br>min  � � � Backtranslation<br>LLM/Expert s.t.  푨�≤� Pipeline<br>Math Formula Natural Language  AutoFormulator<br>Description<br>Step3: Fine-Tuning<br>Augmentation Fine Tuning<br>OptMATH-Train Filter Augmented Data Base Model<br><!-- End of picture text -->

Figure 1: An overview of our scalable, bidirectional data synthesizing pipeline. 

Lastly, the weights _α·, β·, γ_ BigM _, δ_ expr are tunable parameters reflecting the contribution of each component to the overall complexity. To illustrate it, we provide an example in Appendix B.1 that considers a MIP problem incorporating multiple constraint types to optimize production costs for two products under resource constraints. 

**Selecting Parameters to Control the Complexity.** We now present the workflow in Algorithm 1 for selecting parameter configurations for instance generator _Gi_ to generate PDs fitting the complexity, feasibility, and solving time requirements. The prompt templates are illustrated in Appendix E.4. As formalized in Algorithm 1, the process begins by specifying target bounds. Then a template `prompt` IC for initializing the configuration are incorporated. After obtaining the configuration, we generate _N_ PDs using it. We then evaluate the generated PDs through the complexity score, solving time, and feasibility satisfactory. Then, a feedback `prompt` RC is created based on the statistics of these metrics over the _N_ generated PDs. The LLM iteratively adjusts parameters based on feedback from solved instances, ultimately converging to a configuration that satisfy predefined criteria. 

This ensures generated PDs remain both expressive and tractable by adhering to runtime thresholds. 

### **4 The Data Synthesis Framework** 

This section presents our bidirectional scalable data synthesis framework. In this section, all of the PDs are in solver code form (see subsection 4.2 for more details). Let _L_ represents the LLM employed on the reverse data generation phase, and _Aθ_ for our fine-tuned AutoFormulator with weights _θ_ . We define `prompt` I, `prompt` C, `prompt` R as the prompt templates that accept certain inputs for the initial generation, self-critism, and self-refinement stages. The algorithm is formalized in Algorithm 2, with an illustrative example of the backtranslation process shown in Figure 13. 

The final OptMATH dataset _D_ is constructed by collecting all valid quadruples (NL _i,j,_ MF<sup>_′_</sup> _i,j_<sup>_,_PD</sup><sup>_′_</sup> _i,j_<sup>_,_OV</sup><sup>_i,j_)thatpasstheval-</sup> idation process, where MF<sup>_′_</sup> _i,j_<sup>andPD</sup><sup>_′_</sup> _i,j_<sup>rep-</sup> resent the generated mathematical formulation and problem data using _Aθ_ , OV _i,j_ is the optimal value obtained by solving the problem specified by PD _i,j_ . By leveraging our instance generators and the iterative refine- 

5 

**Algorithm 1** Feedback-Driven Problem Data <u>Generation</u> 

- **Require:** Target complexity range [ _S_ min _, S_ max], time limits [ _T_ min _, T_ max], instance generator _G_ , feasibility threshold _F_ target, max iterations _T_ 

- **Ensure:** Configuration Θ such that for PD _i ∼ G_ (Θ): 

- 1: _S_ (PD _i_ ) _∈_ [ _S_ min _, S_ max] (complexity), _τi ≤ T_ max (solving time), 

- 2: Pr( _fi_ = feasible) _≥F_ target 

- 3: **Initialize parameters via LLM:** 

- 4: Θ0 _←L_ ( `prompt` IC( _S_ min _, S_ max _, T_ min _, T_ max)) 

- 5: **for** _t_ = 1 **to** _T_ **do** 

- 6: Generate _N_ PDs: _{_ PD _i}_<sup>_N_</sup> _i_ =1 _← G_ (Θ _t−_ 1) 

- 7: Compute metrics: _S_ (PD _i_ ) (Eq. 3.1), _τi_ (solving time), _fi_ (feasibility) 

- 8: Aggregate statistics: 

- 9: _S_ ¯ _t_ = _N_<sup><u>1</u></sup> � _S_ (PD _i_ ) 

- 10: _τ_ ¯ _t_ = _N_<sup><u>1</u></sup> <u>�</u> _τi_ 11: _Ft_ = _N_<sup><u>1</u></sup> � I( _fi_ = feasible) 12: **if** _S_<sup>¯</sup> _t ∈_ [ _S_ min _, S_ max] **and** _τ_ ¯ _t ≤ T_ max **and** _Ft ≥F_ target **then** 

- 13: **return** Θ _t−_ 1 

- 14: **else** 

- 15: **Refine parameters via feed-** 

**back:** 

**Algorithm 2** Bidirectional Data Synthesis Algorithm 

- **Require:** Instance pair (MF _i,_ PD _i,j_ ), Max Iteration _T_ 

- **Ensure:** (NL _i,j,_ MF<sup>_′_</sup> _i,j_<sup>_,_PD</sup> _i,j_<sup>_′,_OV</sup><sup>_i,j_)</sup> 1: Initial generation: NL _← L_ ( `prompt` I(MF _i,_ PD _i,j_ )) 

- 2: Initialize: SC = SR = Null 

- 3: **for** _k_ = 1 _, . . . , T −_ 1 **do** 

- 4: Self-Criticize: 

- 5: SC _←L_ ( `prompt` C(MF _i,_ PD _i,j,_ NL)) 6: Self-Refine: 7: SR _← L_ ( `prompt` R(MF _i,_ PD _i,j,_ NL _,_ SC _,_ SR)) 

- 8: **if** SR is good enough **then** 

- 9: **break** 

- 10: **end if** 

- 11: **end for** 

- 12: NL _i,j ←_ SR 

- 13: AutoFormulation: 

- 14: (MF<sup>_′_</sup> _i,j_<sup>_,_PD</sup><sup>_′_</sup> _i,j_<sup>)</sup><sup>_←Aθ_(</sup><sup>`prompt`</sup> M<sup>(NL</sup><sup>_i,j_))</sup> 15: OV _i,j ←_ Solve PD _i,j_ by Gurobi 16: OV<sup>_′_</sup> _i,j_<sup>_←_SolvePD</sup><sup>_i,j_byGurobi</sup> 17: **if** OV _i,j_ = OV<sup>_′_</sup> _i,j_<sup>**then**</sup> 18: **return** (NL _i,j,_ MF<sup>_′_</sup> _i,j_<sup>_,_PD</sup><sup>_′_</sup> _i,j_<sup>_,_OV</sup><sup>_i,j_)</sup> 

19: **else** 

   - 20: **return** Null 21: **end if** 

- 16: Θ _t ← L_ ( `prompt` RC( _S_<sup>¯</sup> _t,_ ¯ _τt, Ft_ ; Θ _t−_ 1)) 

- 17: **end if** 

18: **end for** 

19: **return** _∅_ (no valid Θ found) 

ment process, this algorithm enables scalable generation of high-quality data pairs. The mathematical equivalence between the generated formulations and the original instances is rigorously validated through rejection sampling, ensuring the reliability of our dataset. A comprehensive discussion of our quality control and rejection sampling can be found in Section 4.3. 

#### **4.1 Backtranslation Pipeline** 

To generate high-quality NLs of optimization problems at scale, we leverage a specific LLM as the foundation of our pipeline. Recent re- 

search has demonstrated that complex tasks often benefit from iterative refinement approaches rather than direct generation [53]. This observation aligns with human problemsolving processes in mathematics, which typically requires multiple attempts and refinements. Building upon this insight, we design a three-phase backtranslation pipeline that systematically improves the quality of generated descriptions through iterative refinement. All prompt templates used in this pipeline can be found in E.1. 

**Initial Generation.** Given the mathematical formulation MF _i_ and the corresponding problem data PD _i,j_ of a problem _j_ in _i_ -class, the LLM generates an initial natural language description NL using the prompt template `prompt` I. This stage requires the model to comprehend both the mathematical seman- 

6 

tics and the instance parameters to produce a preliminary human-readable description. 

**Self-Criticism.** Using prompt template `prompt` C, the LLM evaluates the current description by examining the mathematical equivalence with MF _i_ , completeness of the constraints and objective functions, clarity and comprehensibility, and consistency of the parameters with PD _i,j_ . The criticism SC in iteration _k_ incorporates feedback from all previous iterations to guide improvements. 

**Self-Refinement.** Based on the criticism, the model generates refined descriptions SR with the prompt template `prompt` R. The refinement process focuses on improving the mathematical accuracy, completeness of the constraints, and clarity of the descriptions. 

This process iterates for _T_ rounds until a satisfactory description NL _i,j_ is obtained, with each iteration potentially improving the quality of the generated description. Based on our empirical analysis (see Appendix C.2), we set _T_ = 1 in the final implementation. 

#### **4.2 Forward modeling** 

Building upon the NLs generated in subsection 4.1, we leverage AutoFormulator to transform them back into MFs and PDs in solver code form, enabling rejection sampling for quality validation. Given a NL as input, AutoFormulator produces two key outputs: a MF and corresponding PD in solver code form. While previous works [71, 44] adopted fixed output formats, our approach is not constrained to any particular format, as our primary goal is to obtain correct solver code, with the formulation serving as an intermediate reasoning step. To facilitate genuine mathematical modeling capabilities rather than superficial format mapping, we design diverse Chainof-Thought (CoT) prompting strategies [78]. This approach generates multiple valid reasoning paths and formulation variants for the same problem, enriching our training data with diverse modeling perspectives and enhancing the model’s mathematical reasoning capabilities. Detailed implementation of these CoT strategies is described in Appendix D.1. 

#### **4.3 Rejection Sampling** 

To ensure the quality and mathematical soundness of our generated optimization problem descriptions, we employ a rejection sampling strategy [83, 51] to filter and select highquality samples from the generated candidates. 

As illustrated in Algorithm 2, our rejection sampling mechanism relies on solution-based comparison to validate the generated samples. Specifically, for each generated natural language description NL _i,j_ , we use AutoFormulator to transform it into a mathematical formulation MF<sup>_′_</sup> _i,j_<sup>andsolvercodePD</sup><sup>_′_</sup> _i,j_<sup>,ob-</sup> taining solution OV<sup>_′_</sup> _i,j_<sup>.Thissolutionisthen</sup> compared with OV _i,j_ , obtained by directly solving the original instance PD _i,j_ . A sample is accepted into our dataset _D_ as a validated quadruple (NL _i,j,_ MF<sup>_′_</sup> _i,j_<sup>_,_PD</sup><sup>_′_</sup> _i,j_<sup>_,_OV</sup><sup>_i,j_)ifand</sup> only if OV _i,j_ = OV<sup>_′_</sup> _i,j_<sup>.</sup> 

While this solution-based validation approach may not guarantee perfect equivalence (as problems with identical optimal values may represent different optimization problems), our manual analysis of randomly sampled instances (1% of the total dataset) reveals a remarkable 99.6% accuracy rate. We acknowledge that determining the exact equivalence between two mathematical formulations remains an open research question worthy of further investigation. Nevertheless, our current approach provides a practical and highly effective mechanism for ensuring dataset quality. 

### **5 Fine-Tuning** 

#### **5.1 Data Augmentation** 

To improve the diversity of our dataset, we use data augmentation to augment the training data. This method generates more nonstandard problems compared to a data generator, enhancing the model’s generalization performance. We create rules for problem rewriting, semantic substitution, constraint expansion, and numerical augmentation. For each instance, a randomly selected rule is used to prompt the LLMs to generate the corre- 

7 

sponding augmented data. The detailed augmentation rules and prompt templates can be found in Appendix E.7. 

For quality control, we employ a specific LLM _L_ to sample each augmented description twice independently, followed by the rejection sampling strategy described in Section 4.3. This process yields approximately 10 qualified augmented datasets for each problem, and this method was applied to augment 50 thousand instances to complement our original dataset. 

#### **5.2 Training the AutoFormulator** 

We adopt a supervised fine-tuning (SFT) approach to enhance the AutoFormulator’s modeling capabilities. Specifically, we employ the LoRA algorithm [42] for efficient parameter-efficient fine-tuning, which significantly reduces memory requirements while maintaining model performance by updating only a small set of adapter parameters. Using the OptMATH-Train dataset _D_ SFT = _{_ (NL _i,_ MF _i,_ PD _i_ ) _}_<sup>_N_</sup> _i_ =1<sup>Train</sup> , we train the model to generate both mathematical formulations and solver code given problem descriptions. For each training sample, the input consists of the problem description NL _i_ , while the target output is the concatenation of the formulation and solver code: _yi_ = [MF _i_ ; PD _i_ ], where [; ] denotes sequence concatenation. The training objective follows the standard sequence-tosequence loss: 



where _yt_ represents the token at position _t_ in the target sequence, and _y<t_ denotes all preceding tokens. This approach allows the model to learn the mapping from natural language problem descriptions to both mathematical formulations and solver code within a unified sequence-to-sequence framework. 

### **6 Experiments** 

#### **6.1 Statistics of the OptMATH Dataset** 

First, using our generators, we generated a quality-filtered dataset containing over 600,000 LP files, which span 53 distinct problem types and are distributed across five hardness levels. For more details on the seed data class, please refer to Appendix A.2. To ensure computational feasibility, we impose a solving time threshold and employ a feedback pipeline that leverages an LLM to regulate both the complexity and feasibility of the generated instances. Further details on this process are provided in Appendix B. The distribution of file lengths across these LP files is visualized in Figure 2. As shown, the lengths range widely from 1,000 to 25,000 characters, capturing a rich variety of problem complexities. The proportions of different lengths are well-balanced, with a concentration on medium difficulty levels (which are already quite challenging compared to other benchmarks) and a gradual decline as the problems become harder. Additionally, the distribution confirms the effectiveness of our complexity control mechanism. 



<!-- Start of picture text -->
5<br>Easy<br>Medium Easy<br>4 Medium<br>Medium Hard<br>3 Hard<br>2<br>1<br>0<br>5,000 10,000 15,000 20,000 25,000<br>Number of Characters<br>Percentage (%)<br><!-- End of picture text -->

Figure 2: Distribution of LP file lengths. 

We further conducted a comparative analysis of problem lengths between OptMATH and other benchmark datasets, with their average lengths shown in Figure 3. The analysis reveals that OptMATH presents significantly more complex problem descriptions compared to existing benchmarks. This increased complexity, manifested through longer problem descriptions, poses greater challenges for LLMs, 

8 

Table 1: Performance Comparison of Models on Different Benchmarks 

|Types|Models||Accura|cy(pass@1)||Macro<br>AVG|Micro<br>AVG|
|---|---|---|---|---|---|---|---|
|||NL4OPT|MAMO<br>EasyLP|MAMO<br>ComplexLP|OptMATH<br>Bench|||
|**Baseline**|GPT-3.5-turbo<br>GPT-4|78.0%<br>89.0%|79.3%<br>87.3%|33.2%<br>49.3%|15.0%<br>16.6%|51.4%<br>60.6%|61.0%<br>70.9%|
||Deepseek-V3|95.9%|88.3%|51.1%|32.6%|67.0%|75.3%|
|**Prompt-based**|Chain-of-Experts<br>Optimus|64.2%<sup>_†_</sup><br>78.8%<sup>_†_</sup>|–<br>–|–<br>–|–<br>–|–<br>–|–<br>–|
|**Fii**|ORLM-LLaMA-3-8B|85.7%<sup>_†_</sup>|82.3%<sup>_†_</sup>|37.4%<sup>_†_</sup>|0.0%|51.4%|64.8%|
|**ne-tunng**|**OptMATH-Qwen2.5-7B**|94.7%|86.5%|51.2%|24.4%|64.2%|73.5%|
||**OptMATH-Qwen2.5-32B**|**95.9%**|**89.9%**|**54.1%**|**34.7%**|**68.7%**|**76.5%**|



_†_ : Results reported in their original papers. 

as longer descriptions typically demand enhanced comprehension and reasoning capabilities. 



<!-- Start of picture text -->
4000 OptMATH-Train MAMO EasyLP<br>OptMATH-Bench NL4OPT<br>3500 3,315 MAMO ComplexLP<br>2,974<br>3000<br>2500<br>2000 1,724<br>1500<br>1,045<br>1000<br>541<br>500<br>0<br>Average Question Length (character)<br><!-- End of picture text -->

Figure 3: Question length analysis 

As shown in Figure 4, OptMATH-Bench has selected a number of representative mathematical optimization problems covering a wide range of application scenarios, including LP, MILP, IP, NLP, SOCP and other optimization problems. For details, please refer to Appendix A.1. 

form distinct clusters, suggesting that OptMATH effectively captures the diversity of different problem families. It can be observed that OptMATH surrounds the area of other benchmarks. This explains the improvement on various benchmarks obtained by training on OptMATH-Train. 



<!-- Start of picture text -->
40<br>20<br>0<br>−20<br>−40<br>−40 −20 0 20 40<br>NL4OPT MAMO ComplexLP OptMATH-Train<br>MAMO EasyLP OptMATH-Bench<br><!-- End of picture text -->

Figure 5: Visualization of OptMATH and other benchmarks. 



Figure 4: The proportion of problems in different datasets. 

To visualize the distribution of different benchmarks and OptMATH dataset, we project their high-dimensional embeddings onto a 2D space using t-SNE. As shown in Figure 5, the instances from different sources 

#### **6.2 Autoformulation** 

**Evaluation Benchmarks and Metrics.** We evaluate our fine-tuned model on three benchmarks: NL4OPT[63], MAMO[43], and our newly constructed OptMATH-Bench. Detailed descriptions of these benchmarks can be found in Appendix A.1. We use pass@1 accuracy as the evaluation metric, which specifically measures whether the optimal value obtained by the generated code matches the 

9 



<!-- Start of picture text -->
100<br>Baseline Model<br>80 Finetuned Model 73.6%11.5% 76.0% 8.0% 76.9% 9.6%<br>11.8%<br>59.9%<br>60 48.0%<br>49.3%<br>40<br>23.2% 62.0% 68.0% 67.3%<br>23.3% 48.0%<br>20<br>0.1% 1.2%<br>0<br>0.5B 1.5B 3B 7B 14B 32B<br>Model Size<br>Micro Accuracy (%)<br><!-- End of picture text -->

Figure 6: Scaling behavior of Qwen2.5 models (0.5B-32B). 

ground truth provided in the benchmark. The detailed matching criteria are described in Appendix A.1. Notably, since prompt design can significantly impact model performance, we maintain consistency by using the same prompt template across all model evaluations (see Appendix E.2 for details).Additionally, comprehensive details about our fine-tuning procedure are provided in Appendix D.3. 

**Main Results.** The primary results are presented in Table 1. First, our bestperforming model, OptMATH-Qwen2.5-32B, achieves superior performance across all benchmarks, surpassing proprietary large language models such as GPT-3.5-Turbo[13], GPT4[59], and Deepseek-V3[50], despite these models having tens of times more parameters. Furthermore, our OptMATH-Qwen2.5-7B outperforms ORLM-LLaMA-3-8B, a model of comparable size, on all benchmarks and demonstrates performance only marginally inferior to Deepseek-V3. Collectively, these results demonstrate that training with OptMATHTrain significantly enhances the model’s optimization modeling capabilities. 

**Ablation Study on Model Size.** To investigate the effectiveness of OptMATH training across different model scales, we conducted experiments using Qwen2.5 models ranging from 0.5B to 32B parameters. Due to computational constraints, we used a randomly sampled subset of 100,000 training examples. As shown in Figure 6, all models exhibit substantial performance improvements after OptMATH-Train fine-tuning. Notably, we 



<!-- Start of picture text -->
80<br>70<br>60<br>50<br>40<br>30<br>20<br>NL4OPT<br>10 MAMO EasyLP<br>MAMO ComplexLP<br>OptMATH-Bench<br>0 Micro Accuracy<br>0.0 0.2 0.4 0.6 0.8 1.0<br>Proportion<br>Accuracy (%)<br><!-- End of picture text -->

Figure 7: Accuracy of Qwen2.5-1.5B within one training epoch. 

observe that while larger models generally achieve better absolute performance, the relative performance gains from OptMATH-Train training demonstrate diminishing returns as model size increases. 

**Ablation Study on Data Size.** Figure 7 presents our comprehensive analysis of how varying amounts of training data influence the performance of Qwen2.5-1.5B model on OptMATH-Train. We observed significant improvements in the model’s optimization modeling capabilities even with only a small fraction of the OptMATH-Train dataset. As we gradually increased the size of the training data, the performance gains became less pronounced, exhibiting a typical pattern of diminishing returns. Larger models exhibit smoother learning curves, while smaller models demonstrate greater sensitivity to additional training data, indicating higher potential for improvement through data scaling (detailed results across model sizes can be found in the Appendix D.4). 

### **7 Conclusion** 

In this paper, we introduce a bidirectional data synthesis framework for optimization modeling. It utilizes a two-step process: reverse data generation, where LLMs refine themselves in a loop to create diverse datasets, and autoformulation, where a specialized model translates natural language into mathematical representations. Our evaluation on NL4OPT, MAMO 

10 

and OptMATH-Benchmarks demonstrated AutoFormulator’s superior performance in generating accurate and well-formed optimization models compared to baseline approaches. 

### **Impact Statements** 

This study introduces OptMATH, a dataset for optimization modeling, comprising a largescale training set (OptMATH-Train) and a challenging benchmark (OptMATH-Bench). OptMATH has the potential to democratize optimization by enabling those without expertise to translate real-world problems into mathematical formulations. The OptMATHTrain dataset will significantly improve LLMs’ ability to understand and model optimization problems. Furthermore, OptMATH’s structured data facilitates the integration of optimization with advanced AI techniques like reinforcement learning, Monte Carlo Tree Search. Additionally, OptMATH-Bench provides a standardized benchmark for evaluating optimization modeling systems, pushing the boundaries of LLM capabilities. Ultimately, OptMATH can improve efficiency and decision-making across industries. 

### **References** 

- [1] Jeph Abara. Applying integer linear programming to the fleet assignment problem. _Interfaces_ , 19(4):20–28, 1989. 

- [2] Joseph Adams, Egon Balas, and Daniel Zawack. The shifting bottleneck procedure for job shop scheduling. _Management Science_ , 34(3):391–401, 1988. 

- [3] Ali AhmadiTeshnizi, Wenzhi Gao, and Madeleine Udell. OptiMUS: Optimization modeling using MIP solvers and large language models, 2023. 

- [4] H. Alipour, M. A. Mu˜noz, and K. SmithMiles. Enhanced instance space analysis for the maximum flow problem. _European Journal of Operational Research_ , 2022. 

- [5] H. Alipour and K. Smith-Miles. Instance space analysis for 2d bin packing mathematical models. _Discrete Optimization_ , 2023. 

- [6] Nicol´as Astorga, Tennison Liu, Yuanzhang Xiao, and Mihaela van der Schaar. Autoformulation of mathematical optimization models using LLMs, 2024. 

- [7] J. E. Beasley, M. Krishnamoorthy, Y. M. Sharaiha, and D. Abramson. Scheduling aircraft landings—the static case. _Transportation Science_ , 34(2):180–197, 2000. 

- [8] Dimitri Bertsekas. _Network optimization: continuous and discrete models_ , volume 8. Athena Scientific, 1998. 

- [9] Simon Bowly. _Stress testing mixed integer programming solvers through new test instance generation methods._ PhD thesis, University of Melbourne, Parkville, Victoria, Australia, 2019. 

- [10] Simon Bowly, Kate Smith-Miles, Davaatseren Baatar, and Hans Mittelmann. Generation techniques for linear programming instances with controllable properties. _Math. Program. Comput._ , 12(3):389–415, 2020. 

- [11] Stephen Boyd. Convex optimization. _Cambridge UP_ , 2004. 

- [12] Gerald G. Brown, Robert F. Dell, and Alexandra M. Newman. Optimizing military capital planning. _Interfaces_ , 34(6):415–425, 2004. 

- [13] Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, et al. Language models are few-shot learners. _Advances in neural information processing systems_ , 33:1877–1901, 2020. 

- [14] Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, Sandhini Agarwal, Ariel Herbert-Voss, Gretchen Krueger, Tom Henighan, Rewon Child, Aditya Ramesh, Daniel M. Ziegler, Jeffrey Wu, Clemens Winter, Christopher Hesse, Mark Chen, Eric Sigler, Mateusz Litwin, Scott Gray, Benjamin Chess, Jack Clark, Christopher Berner, Sam McCandlish, Alec Radford, Ilya Sutskever, and Dario Amodei. Language models are few-shot learners, 2020. 

- [15] Rainer Burkard, Mauro Dell’Amico, and Silvano Martello. _Assignment Problems_ . Society for Industrial and Applied Mathematics, 2012. 

11 

- [16] Alberto Caprara, Paolo Toth, and Matteo Fischetti. Algorithms for the set covering problem. _Annals of Operations Research_ , 98(1):353–371, 2000. [Online; accessed 19January-2025]. 

- [17] Guanglin Chen, Xin Li, and Yinyu Ye. An improved analysis of lp-based control for revenue management. _arXiv preprint_ , 2022. [Online; accessed 19-January-2025]. 

- [18] Giorgio Consigli. Optimization methods in finance. _Quantitative Finance_ , 19:717 – 719, 2019. 

- [19] Lee G. Cooper. Market-share models. In _Handbooks in Operations Research and Management Science_ , volume 5, pages 259–314. Elsevier Science Publishers, 1993. [Online; accessed 19-January-2025]. 

- [20] JF. Cordeau, F. Pasin, and M.M. Solomon. An integrated model for logistics network design. _Annals of Operations Research_ , 144:59– 82, 2006. 

- [21] G. Dantzig, R. Fulkerson, and S. Johnson. Solution of a large-scale traveling-salesman problem. _Journal of the Operations Research Society of America_ , 2(4):393–410, 1954. 

- [22] Mark S. Daskin. _Network and Discrete Location: Models, Algorithms, and Applications_ . Wiley, 1995. [Online; accessed 19-January2025]. 

- [23] A. Drexl and A. Kimms. Lot sizing and scheduling — survey and extensions. _European Journal of Operational Research_ , 99(2):221–235, 1997. 

- [24] Bernhard Fleischmann. The discrete lotsizing and scheduling problem. _European Journal of Operational Research_ , 44(3):337– 348, 1990. 

- [25] Michael Florian and Morton Klein. Deterministic production planning with concave costs and capacity constraints. _Management Science_ , 18(1):12–20, 1971. 

- [26] L. R. Ford and D. R. Fulkerson. Maximal flow through a network. _Canadian Journal of Mathematics_ , 8:399–404, 1956. 

- [27] Michael R Garey and David S Johnson. Approximation algorithms for bin packing problems: A survey. In _Analysis and design of algorithms in combinatorial optimization_ , pages 147–172. Springer, 1981. 

- [28] Susan Garner Garille and Saul I. Gass. Stigler’s diet problem revisited. _Operations Research_ , 49(1):1–13, 2001. 

- [29] David M Gay. Electronic mail distribution of linear programming test problems. _Mathematical Programming Society COAL Newsletter_ , 13:10–12, 1985. 

- [30] Bernard Gendron, Teodor Gabriel Crainic, and Antonio Frangioni. Multicommodity capacitated network design. In _Telecommunications network planning_ , pages 1–19. Springer, 1999. 

- [31] Zijie Geng, Xijun Li, Jie Wang, Xiao Li, Yongdong Zhang, and Feng Wu. A deep instance generative framework for MILP solvers under limited data availability. In Alice Oh, Tristan Naumann, Amir Globerson, Kate Saenko, Moritz Hardt, and Sergey Levine, editors, _Advances in Neural Information Processing Systems 36: Annual Conference on Neural Information Processing Systems 2023, NeurIPS 2023, New Orleans, LA, USA, December 10 - 16, 2023_ , 2023. 

- [32] Gianpaolo Ghiani, Gilbert Laporte, and Roberto Musmanno. _Introduction to Logistics Systems Management: With Microsoft Excel and Python Examples_ . John Wiley & Sons, 2022. 

- [33] P. C. Gilmore and R. E. Gomory. A linear programming approach to the cutting-stock problem. _Operations Research_ , 9(6):849–859, 1961. 

- [34] Ambros Gleixner, Gregor Hendel, Gerald Gamrath, Tobias Achterberg, Michael Bastubbe, Timo Berthold, Philipp M. Christophel, Kati Jarck, Thorsten Koch, Jeff Linderoth, Marco L¨ubbecke, Hans D. Mittelmann, Derya Ozyurt, Ted K. Ralphs, Domenico Salvagnin, and Yuji Shinano. MIPLIB 2017: Data-Driven Compilation of the 6th Mixed-Integer Programming Library. _Mathematical Programming Computation_ , 2021. 

- [35] Bruce Golden, S. Raghavan, and Edward Wasil, editors. _The Vehicle Routing Problem: Latest Advances and New Challenges_ . Operations Research/Computer Science Interfaces Series. Springer New York, NY, 1 edition, 2008. 

- [36] Ziao Guo, Yang Li, Chang Liu, Wenli Ouyang, and Junchi Yan. Acm-milp: Adaptive constraint modification via grouping and selection for hardness-preserving milp instance 

12 

generation. In _International Conference on Machine Learning (ICML)_ , 2024. 

- [37] LLC Gurobi Optimization. Optimization modeling, 2025. [Online; accessed 19-January2025]. 

- [38] Gurobi Optimization, LLC. Gurobi Optimizer Reference Manual, 2024. 

- [39] Peter B. R. Hazell and Roger D. Norton. _Mathematical Programming for Economic Analysis in Agriculture_ . Macmillan Publishing Co., 1986. [Online; accessed 19-January2025]. 

- [40] Jeffrey W. Herrmann, editor. _Handbook of Production Scheduling_ . International Series in Operations Research & Management Science. Springer New York, NY, 1 edition, 2006. 

- [41] Frederick S. Hillier and Gerald J. Lieberman. _Introduction to Operations Research_ . McGraw-Hill Education, 10th edition, 2014. [Online; accessed 19-January-2025]. 

- [42] Edward J Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, and Weizhu Chen. Lora: Low-rank adaptation of large language models. _arXiv preprint arXiv:2106.09685_ , 2021. 

- [43] Xuhan Huang, Qingning Shen, Yan Hu, Anningzhe Gao, and Benyou Wang. Mamo: a mathematical modeling benchmark with solvers. _CoRR_ , abs/2405.13144, 2024. 

- [44] Caigao Jiang, Xiang Shu, Hong Qian, Xingyu Lu, Jun Zhou, Aimin Zhou, and Yang Yu. LLMOPT: Learning to define and solve general optimization problems from scratch, 2024. 

- [45] Narendra Karmarkar. A new polynomial-time algorithm for linear programming. In _Proceedings of the sixteenth annual ACM symposium on Theory of computing_ , pages 302–311, 1984. 

- [46] Morton Klein. A primal method for minimal cost flows with applications to the assignment and transportation problems. _Management Science_ , 14(3):205–220, 1967. 

- [47] Michael J. Kuby. Programming models for facility dispersion: the p-dispersion and maxisum dispersion problems. _Mathematical and Computer Modelling_ , 10(10):792, 1988. 

- [48] H. W. Kuhn. The hungarian method for the assignment problem. _Naval Research Logistics Quarterly_ , 2(1-2):83–97, 1955. 

- [49] Sirui Li, Janardhan Kulkarni, Ishai Menache, Cathy Wu, and Beibin Li. Towards foundation models for mixed integer linear programming. _arXiv preprint arXiv:2410.08288_ , 2024. 

- [50] Aixin Liu, Bei Feng, Bing Xue, Bingxuan Wang, Bochao Wu, Chengda Lu, Chenggang Zhao, Chengqi Deng, Chenyu Zhang, Chong Ruan, et al. Deepseek-v3 technical report. _arXiv preprint arXiv:2412.19437_ , 2024. 

- [51] Haoxiong Liu, Yifan Zhang, Yifan Luo, and Andrew Chi-Chih Yao. Augmenting math word problems via iterative question composing. _ArXiv_ , abs/2401.09003, 2024. 

- [52] Haoyang Liu, Jie Wang, Wanbo Zhang, Zijie Geng, Yufei Kuang, Xijun Li, Bin Li, Yongdong Zhang, and Feng Wu. Milp-studio: MILP instance generation via block structure decomposition. _CoRR_ , abs/2410.22806, 2024. 

- [53] Aman Madaan, Niket Tandon, Prakhar Gupta, Skyler Hallinan, Luyu Gao, Sarah Wiegreffe, Uri Alon, Nouha Dziri, Shrimai Prabhumoye, Yiming Yang, et al. Self-refine: Iterative refinement with self-feedback. _Advances in Neural Information Processing Systems_ , 36, 2024. 

- [54] Harry Markowitz. Portfolio selection. _The Journal of Finance_ , 7(1):77–91, 1952. 

- [55] Silvano Martello and Paolo Toth. _Knapsack problems: algorithms and computer implementations_ . John Wiley & Sons, Inc., USA, 1990. 

- [56] MOSEK ApS. _MOSEK Optimization Software_ , 2025. Version 11.0.3. 

- [57] Netlib. Netlib: A collection of mathematical software, papers, and databases. `http: //netlib.org` , 1990. Available at `http: //netlib.org` . 

- [58] OpenAI. Learning to reason with llms: Introducing openai o1. `https://openai.com/ index/learning-to-reason-with-llms/` , 2024. Accessed: 2024-12-21. 

- [59] OpenAI, Josh Achiam, and Steven et al. Adler. GPT-4 Technical Report, 2023. 

- [60] N.P. Padhy. Unit commitment-a bibliographical survey. _IEEE Transactions on Power Systems_ , 19(2):1196–1205, 2004. 

- [61] Michael L. Pinedo. _Scheduling: Theory, Algorithms, and Systems_ . Springer Cham, 6 edition, 2022. 

13 

- [62] Chandrasekharan Rajendran. Heuristics for scheduling in flowshop with multiple objectives. _European Journal of Operational Research_ , 82(3):540–555, 1995. 

- [63] Rindranirina Ramamonjison, Timothy T. L. Yu, Raymond Li, Haley Li, Giuseppe Carenini, Bissan Ghaddar, Shiqi He, Mahdi Mostajabdaveh, Amin Banitalebi-Dehkordi, Zirui Zhou, and Yong Zhang. Nl4opt competition: Formulating optimization problems based on their natural language descriptions. In Marco Ciccone, Gustavo Stolovitzky, and Jacob Albrecht, editors, _NeurIPS 2022 Competition Track, November 28 - December 9, 2022, Online_ , volume 220 of _Proceedings of Machine Learning Research_ , pages 189–203. PMLR, 2021. 

- [64] Singiresu S Rao. _Engineering optimization: theory and practice_ . John Wiley & Sons, 2019. 

- [65] A. Sch¨obel. Line planning in public transportation: models and methods. _OR Spectrum_ , 34:491–510, 2012. 

- [66] D. Smith. Network flows: Theory, algorithms, and applications. _J Oper Res Soc_ , 45:1340, 1994. 

- [67] Kate Smith-Miles and Simon Bowly. Generating new test instances by evolving in instance space. _Comput. Oper. Res._ , 63:102–113, 2015. 

- [68] Marius M. Solomon. Algorithms for the vehicle routing and scheduling problems with time window constraints. _Oper. Res._ , 35:254–265, 1987. 

- [69] M. SteadieSeifi, N.P. Dellaert, W. Nuijten, T. Van Woensel, and R. Raoufi. Multimodal freight transportation planning: A literature review. _European Journal of Operational Research_ , 233(1):1–15, 2014. 

- [70] S. Strassl and N. Musliu. Instance space analysis and algorithm selection for the job shop scheduling problem. _European Journal of Operational Research_ , 2022. 

- [71] Zhengyang Tang, Chenyu Huang, Xin Zheng, Shixi Hu, Zizhuo Wang, Dongdong Ge, and Benyou Wang. ORLM: Training large language models for optimization modeling, 2024. 

- [72] Constantine Toregas, Ralph Swain, Charles ReVelle, and Lawrence Bergman. The location of emergency service facilities. _Operations Research_ , 19(6):1363–1373, 1971. 

- [73] P Toth. The vehicle routing problem. _SIAM Monographs on Discrete Mathematics and Applications_ , 2002. 

- [74] Haoyu Wang, Jialin Liu, Xiaohan Chen, Xinshang Wang, Pan Li, and Wotao Yin. Dig-milp: A deep instance generator for mixed-integer linear programming with feasibility guarantee. _arXiv preprint_ , 2023. Code: `https://github.com/Graph-COM/ DIG_MILP` . 

- [75] Ke Wang, Jiahui Zhu, Minjie Ren, Zeming Liu, Shiwei Li, Zongye Zhang, Chenkai Zhang, Xiaoyu Wu, Qiqi Zhan, Qingjie Liu, et al. A survey on data synthesis and augmentation for large language models. _arXiv preprint arXiv:2410.12896_ , 2024. 

- [76] Yizhong Wang, Yeganeh Kordi, Swaroop Mishra, Alisa Liu, Noah A Smith, Daniel Khashabi, and Hannaneh Hajishirzi. Selfinstruct: Aligning language models with self-generated instructions. _arXiv preprint arXiv:2212.10560_ , 2022. 

- [77] Larry R. Weatherford and Samuel E. Bodily. Forecasting and control of passenger bookings. _Journal of Revenue and Pricing Management_ , 1(1):37–45, 1997. [Online; accessed 19-January-2025]. 

- [78] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Ed H. Chi, F. Xia, Quoc Le, and Denny Zhou. Chain of thought prompting elicits reasoning in large language models. _ArXiv_ , abs/2201.11903, 2022. 

- [79] Wikipedia. Supply chain management — Wikipedia, the free encyclopedia. `http://en.wikipedia.org/w/index.php? title=Supply%20chain%20management& oldid=1261250036` , 2025. [Online; accessed 19-January-2025]. 

- [80] Wayne L. Winston. _Operations Research: Applications and Algorithms_ . Duxbury Press, 4th edition, 2004. [Online; accessed 19January-2025]. 

- [81] Ziyang Xiao, Dongxiang Zhang, Yangjun Wu, Lilin Xu, Yuan Jessica Wang, Xiongwei Han, Xiaojin Fu, Tao Zhong, Jia Zeng, Mingli Song, and Gang Chen. Chain-of-experts: When llms meet complex operations research problems. In _The Twelfth International Conference on Learning Representations, ICLR 2024, Vienna, Austria, May 7-11, 2024_ . OpenReview.net, 2024. 

14 

- [82] An Yang, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chengyuan Li, Dayiheng Liu, Fei Huang, Haoran Wei, et al. Qwen2. 5 technical report. _arXiv preprint arXiv:2412.15115_ , 2024. 

- [83] Zheng Yuan, Hongyi Yuan, Cheng Li, Guanting Dong, Chuanqi Tan, and Chang Zhou. Scaling relationship on learning mathematical reasoning with large language models. _ArXiv_ , abs/2308.01825, 2023. 

- [84] Yaowei Zheng, Richong Zhang, Junhao Zhang, Yanhan Ye, Zheyan Luo, Zhangchi Feng, and Yongqiang Ma. Llamafactory: Unified efficient fine-tuning of 100+ language models. In _Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 3: System Demonstrations)_ , Bangkok, Thailand, 2024. Association for Computational Linguistics. 

- [85] Eric R. Zieyel. Operations research : applications and algorithms. _Technometrics_ , 30:361– 362, 1988. 

15 

### **A Dataset** 

#### **A.1 An Introduction of Different Benchmarks** 

We evaluated the modeling capabilities of our trained model on NL4OPT, MAMO, and our self-constructed dataset, OptMATH-Bench. Both MAMO and OptMATH-Bench have ground truth annotations, while the original NL4OPT dataset lacks ground truth. To address this, we utilized a LLM to generate initial ground truth for NL4OPT, followed by expert validation and correction for each data. As a result, we obtained the ground truth for the NL4OPT dataset. In addition, we have also analyzed these datasets in terms of problem scenarios and problem model types, and the distribution of scenarios for each dataset is shown in Figure 8, the distribution of problem types for each dataset is shown in Figure 4. 



Figure 8: Scenarios distribution of the datasets. 

**NL4OPT** [63] is a curated dataset derived from the NL4OPT Competition, where participants were tasked with developing automated methods to convert natural language problem descriptions into solver-ready code. This dataset primarily focuses on LP (Linear Programming) problems across various contexts, though the underlying mathematical models are relatively uniform, with more complex MIPS (Mixed Integer Programming and Scheduling) problems notably absent. For our experiments, we selected the test set from this dataset, filtered out low-quality examples, and retained a total of 245 high-quality instances. 

**MAMO** [43] introduces a novel optimization dataset to assess the modeling capabilities of LLMs. The dataset is divided into two main components, _Easy LP_ and _Complex LP_ , containing 652 and 211 instances, respectively. These components cover both LP and MILP problems, capturing a wide range of real-life scenarios. However, the dataset does not include any nonlinear programming (NLP) problems. 

**OptMATH-Bench.** As shown in Table 1, while our fine-tuned model achieves remarkable performance on NL4OPT and _MAMO EasyLP_ , these datasets alone are insufficient to compre- 

16 

hensively evaluate the model’s optimization modeling capabilities. Moreover, both NL4OPT and MAMO datasets are limited to linear programming problems, making them less representative of the broader optimization landscape. To address this limitation, we constructed a more challenging dataset for large models, while also expanding the diversity of problem types— **OptMATH-Bench** . This dataset includes a carefully curated selection of representative mathematical optimization problems that span a broad range of application scenarios, covering LP, MILP, IP, NLP, SOCP, and other common optimization problems. Additionally, the problems in OptMATH-Bench are inherently challenging, making them effective in distinguishing the modeling capabilities of the model. 

During evaluation, we observed that certain ambiguities in problem statements could cause the LLM to struggle in determining whether a variable is integer or continuous. To address this, we applied a rule-based substitution approach: as long as the optimal solution derived under either assumption (integer or continuous variable) matches the ground truth, we consider it a pass. To determine whether the optimal values are equivalent, we use the following formula: 



where _ϵ_ is set to 1e-6. 

#### **A.2 Seed Classes** 

Our seed problem classes were curated by drawing from MIPLIB instances and integrating insights from both Chain-of-Experts[81] and peer-reviewed literature. For each instance, we conducted an in-depth analysis of its structure, starting from the problem description to identify its broader optimization category and further refining it into specific subclasses. To ensure theoretical accuracy, we consulted literature that provided detailed descriptions of these optimization subclasses. Based on these references, we formulated the mathematical representation of each subclass, systematically outlining sets (where applicable), parameters, decision variables, objective functions, and constraints. This step aimed to establish an abstract mathematical framework rather than focusing on specific instances. 

We organized comprehensive metadata for each problem class in a structured `metadata.json` file, encompassing subclass names, references, reference links, and LaTeX-formulated mathematical expressions. An example of this metadata structure is provided in Appendix E.5. This systematic documentation not only ensures clarity but also facilitates dataset utilization and future extensions. 

Next, we focused on generating new problem instances. We implemented a custom Python class, `Generator()` , in `generator.py` , which contained a step-by-step algorithm to create instances of the identified subclasses (an example is provided in Appendix E.6). The input parameters and outputs were explicitly defined, with detailed specifications for each parameter’s type and valid range documented in `README.txt` . We validated the generator by running `test generator()` with default parameters to ensure the produced instances were both mathematically valid and practically meaningful. 

Through this systematic and meticulous approach, we constructed a high-quality dataset of Problem Description (PD) generators that lays a solid foundation for generating natural language descriptions of optimization problems through Backtranslation Pipeline. This dataset is designed to be versatile and scalable, making it suitable for a wide range of applications in optimization research and practice. 

17 

|**Main Class**|**Problem Class**|**Nu**|**m**<br>**Reference**|
|---|---|---|---|
|Assignment and Resource Alloca-<br>tion Optimization|Car Selection Problem<br>Contract Allocation Problem<br>Assignment Problem<br>Structure-Based Assignment<br>Problem<br>Team Formation Problem<br>Military<br>Personnel<br>Deploy-<br>ment Problem|1<br>1<br>2<br>1<br>1<br>1|[15]<br>[79]<br>[48]<br>[15]<br>[37]<br>[12]|
|Combinatorial Optimization|Knapsack Problem<br>Market Share Optimization<br>Problem<br>Set Multi-Cover Problem<br>Set Cover Problem|1<br>1<br>1<br>1|[55]<br>[19]<br>[80]<br>[16]|
|Cutting and Packing Optimiza-<br>tion|Bin Packing Problem<br>Blending Problem<br>Cutting Stock Problem|1<br>1<br>1|[27]<br>[85]<br>[33]|
|Domain-Specific Optimization|Diet Problem<br>Unit Commitment Problem<br>Farm Planning Problem|3<br>1<br>1|[28]<br>[60]<br>[39]|
|Facility Location Optimization|Facility Location Problem<br>Capacitated Facility Location<br>Problem<br>Transportation Problem, Air-<br>line Industry Resource Alloca-<br>tion<br>Facility Dispersion Problem|2<br>2<br>1<br>2|[72]<br>[22]<br>[73]<br>[47]|
|Financial and Revenue Optimiza-<br>tion|Portfolio Optimization Prob-<br>lem<br>Profit Maximization Problem<br>Revenue Management Prob-<br>lem<br>Revenue Maximization Prob-<br>lem|1<br>1<br>1<br>1|[54]<br>[41]<br>[17]<br>[77]|
|Network Flow Optimization|Multi-Commodity<br>Capac-<br>itated<br>Network<br>Design<br>Problem<br>Multi-Commodity Transporta-<br>tion Problem<br>Minimum Cost Flow Problem<br>Multi-Commodity<br>Network<br>Flow Problem<br>Network Flow Problem<br>Static Line Planning Problem<br>Supply Chain Optimization<br>Network Optimization|1<br>1<br>1<br>1<br>1<br>1<br>1<br>1|[30]<br>[66]<br>[46]<br>[66]<br>[26]<br>[65]<br>[20]<br>[8]|



18 

|**Main Class**|**Problem Class**|**Num**|**Reference**|
|---|---|---|---|
|Production<br>Planning<br>and<br>Scheduling Optimization|Capacitated Lot-Sizing Prob-<br>lem<br>Factory Planning Problem<br>Flow Shop Scheduling Prob-<br>lem<br>Job Shop Scheduling Problem<br>Discrete<br>Lot-Sizing<br>and<br>Scheduling Problem<br>Production Planning Problem<br>Lot-Sizing Problem|1<br>1<br>1<br>1<br>1<br>3<br>1|[25]<br>[61]<br>[62]<br>[2]<br>[24]<br>[40]<br>[23]|
|Transportation and Routing Op-<br>timization|Aircraft Assignment Problem<br>Aircraft Landing Problem<br>Transportation Problem<br>Traveling Salesman Problem<br>Operations Optimization<br>Capacitated Vehicle Routing<br>Problem with Time Windows|1<br>1<br>2<br>1<br>1<br>3|[1]<br>[7]<br>[69]<br>[21]<br>[35]<br>[68]|



#### **A.3 OptMATH-Train** 

The OptMATH-Train dataset consists of over 150k reverse-generated samples and 50k augmented instances, forming a comprehensive collection of optimization problems. The dataset encompasses a rich variety of real-world application scenarios. As illustrated in Figure 9, the dataset covers over 10 major application domains spanning across both core business sectors and specialized industries, demonstrating extensive coverage of real-world optimization scenarios. The substantial proportions in logistics, supply chain, and manufacturing ensure robust representation of primary industrial applications, while the balanced inclusion of sectors like transportation, energy, and finance provides comprehensive coverage of specialized use cases. This thoughtful allocation of problems across different domains not only prevents data concentration but also maintains sufficient samples for each sector, enabling effective model training and evaluation. 

The sequence length distribution of OptMATH-Train, as shown in Figure 10, exhibits a wellbalanced profile for both input and output sequences. The distribution approximates a normal distribution with mild right-skewness, centered around 5,000 characters, demonstrating a natural variation in problem complexity. This balanced distribution pattern is particularly advantageous for model training, as it ensures sufficient context length for complex problem representation while maintaining computational efficiency. Furthermore, the moderate right-skewness encompasses challenging cases with extended sequences, which is essential for developing robust models capable of handling sophisticated optimization problems that require comprehensive reasoning and detailed solution steps. 

### **B Details of Instance Generation** 

#### **B.1 An Example for Measuring the Complexity** 

Let binary variables _y_ 1 _, y_ 2 _∈{_ 0 _,_ 1 _}_ indicate whether products 1 and 2 are produced, integer variables _x_ 1 _, x_ 2 _∈_ Z<sup>+</sup> represent production quantities, and a continuous variable _z ≥_ 0 denote total cost. The objective function minimizes total operational costs: min _z_ + 10 _y_ 1 + 8 _y_ 2. 

19 



Figure 9: Distribution of Application Scenarios across OptMATH-Train 



<!-- Start of picture text -->
Input<br>5000 Output<br>4000<br>3000<br>2000<br>1000<br>0<br>0 5000 10000<br>Sequence Length<br>Frequency<br><!-- End of picture text -->

Figure 10: Sequence Length Distribution of OptMATH-Train 

The constraints span four categories: First, linear constraints include the resource limitation 2 _x_ 1 + 3 _x_ 2 _≤_ 100 and market demand bounds _x_ 1 _≤_ 50, _x_ 2 _≤_ 30. Second, indicator constraints using the Big-M method (with _M_ = 100) enforce minimum production levels when activated: _y_ 1 = 1 = _⇒ x_ 1 _≥_ 5 is reformulated as _x_ 1 _≥_ 5 _−_ 100(1 _−y_ 1), and analogously for _y_ 2 = 1 = _⇒ x_ 2 _≥_ 3. Third, a quadratic constraint _z ≥_ 0 _._ 5 _x_<sup>2</sup> 1<sup>+ 0</sup><sup>_._3</sup><sup>_x_2</sup> 2<sup>integratesinventorycostsintotheobjective.</sup> Finally, a general nonlinear constraint _x_ 1 _e_<sup>_x_2</sup> _≤_ 100 captures efficiency coupling between products. To compute the complexity score _S_ (PD), we identify: 2 binary variables, 2 integer variables, and 1 continuous variable; 3 linear constraints, 2 indicator constraints, 1 quadratic constraint, and 1 nonlinear constraint. The Big-M factor frequency is _f_ BigM = 2, while the average number of terms per expression _L_ expr _≈_ 2 _._ 71 is derived from structural analysis of constraints and the objective. With all weights set to 1, the total complexity score becomes _S_ = 16 _._ 71. This example demonstrates how modeling choices (e.g., introducing nonlinear terms, Big-M parameterization) directly influence the score, providing a quantitative framework for assessing model complexity. 

#### **B.2 An Overview of the Generated LP Files** 

The average lengths of LP files for different difficulty levels are illustrated in Figure 11. We define the complexity thresholds for the five difficulty levels—easy, medium ~~e~~ asy, medium, medium ~~h~~ ard, and hard—as [25, 75], [50, 100], [75, 125], [100, 150], and [125, 175], respectively. The results demonstrate that our feedback-driven problem data generation approach is effective. The average length of the generated LP files across the five difficulty levels is presented in Figure 12, categorized by seed data name. All generated LP files are feasible and possess optimal solutions. 

### **C Details of Backtranslation** 

#### **C.1 Backtranslation Pipeline** 

In our reverse generation pipeline, we employ Deepseek-V3[50] as our foundation model and configure its temperature parameter to 0.8 to enhance the diversity of generated problems. Furthermore, to achieve rich contextual diversity, we implement a random scenario assignment mechanism during the Initial Generate phase. This mechanism directs the LLM to synthesize problems that optimally integrate the mathematical characteristics with the designated scenario 

20 



<!-- Start of picture text -->
25000 24,329<br>20000<br>16,098<br>15000<br>11,919<br>10000<br>8,430<br>5000 4,092<br>0<br>Difficulty Level<br>Easy Medium Easy Medium Medium Hard Hard<br>Average Number of Characters<br><!-- End of picture text -->

Figure 11: Distribution of LP file lengths across generated instances by difficulty levels. 

context. The detailed prompt is elaborated in Section E.1. 

Through this backtranslation process, we initially generated approximately 120,000 easy optimization problems. As shown in Figure 15, the length distribution of problem descriptions exhibits a right-skewed pattern, with most problems containing 2,000 to 5,000 characters. After applying rejection sampling, around 40% of the generated problems were filtered out while maintaining a similar distribution pattern. This consistency in distribution before and after filtering suggests that our quality control process effectively removes low-quality samples without introducing length-related biases, ensuring the retained problems maintain natural and appropriate descriptive lengths. After multi-stage refinement including semantic verification and difficulty calibration, the pipeline ultimately produced 150,000 rigorously validated optimization problems. Together with 50,000 augmented instances, this curated collection forms our OptMATH-Train dataset, where each instance demonstrates: (1) Contextual alignment between mathematical formulations and real-world scenarios, (2) Controllable complexity levels matching specified difficulty tiers, and (3) Natural language expressions adhering to authentic problem-solving discourse patterns. The hierarchical quality assurance framework ensures the dataset’s applicability for both educational interventions and benchmarking mathematical reasoning systems. 

#### **C.2 Ablation Study on the Impact of Self-Refine Iterations** 

To validate the effectiveness of each step in our backtranslation pipeline, we conducted comprehensive ablation studies. We first compared the accuracy between using only the Generate step versus implementing the complete pipeline with Generate, Self-criticize, and Self-refine steps. To investigate the impact of parameter _T_ on the acceptance rate of rejection sampling, we randomly selected 500 instances for evaluation, with results shown in Figure 14. The results demonstrate that our Self-Refine loop ( _T ≥_ 1) consistently outperforms direct generation ( _T_ = 0) in terms of acceptance rate. While there are some fluctuations in performance across different _T_ values, possibly due to the inherent hallucination tendencies of large language models, we observe that setting _T_ = 1 achieves a satisfactory acceptance rate of 61.56%. Considering the trade-off between performance and computational efficiency (token usage), we adopt _T_ = 1 in our final data synthesis process. 

21 



Figure 12: Distribution of LP file lengths across generated instances by problem types. 

### **D Details of AutoFormulation** 

#### **D.1 CoT Instructions of AutoFormulation** 

To support comprehensive mathematical modeling capabilities, we developed a diverse set of CoT instructions, which are detailed in Section E.3. These instructions vary in their decomposition approaches, intermediate reasoning steps, and presentation formats, providing multiple pathways for problem formulation. In Figure 16, we present one representative formulation pattern from our instruction set. This format includes three key components: a general mathematical formulation with standard notation, a detailed instance-specific formulation with complete parameter specifications, and the corresponding Python implementation using Gurobi. However, this represents just one of many possible formulation styles. Other formats in our instruction set may use different ordering of steps, alternative notation systems, or various levels of mathematical abstraction. The diversity in formulation patterns ensures that our dataset captures a wide range of valid mathematical modeling approaches while maintaining logical coherence and mathematical correctness. 

#### **D.2 Ablation Study on Augmentation** 

As mentioned in the previous section, the purpose of data augmentation is to increase the diversity of the dataset and generate more non-standard problems, which can help the fine-tuned model to solve more difficult problems. We use 50k raw data, augmented data and mixed data (50% raw data and 50% augmented data) for fine-tuning training on the Qwen2.5-7B model, respectively, and the results show in Table 3 that the model fine-tuned with raw data performs better in solving relatively simple problems, augmented data performs better in solving difficult 

22 

#### An Example of Backtranslation 



<!-- Start of picture text -->
Input-General Formulation Input-LP File<br>Minimize<br>  80000 Selected[1] + 40000 Selected[2] + 20000<br>Selected[3] + 10000Selected[4]<br>   + 80000 Selected[5] + 90000 Selected[6]<br>Subject To<br>Generator  MultiCover_e1: Selected[1] + Selected[3] + Selected[5] +<br>Selected[6] >= 4<br> represents the cost coefficient for each set ………… MultiCover_e10: Selected[1] + Selected[4] + Selected[5] +<br>is a binary decision variable indicating whether set Selected[6]<br>i is selected    >= 4<br> represents the set of all sets containing element j Bounds<br>Binaries<br> represents the minimum number of times element j<br> Selected[1] Selected[2] Selected[3] Selected[4] Selected[5]<br>needs to be covered<br>Selected[6]<br>End<br>Backtranslation<br>Output-Natural Language Description<br>A city is planning the layout of emergency medical stations. There are 6 candidate locations for building medical stations, each<br>with different construction costs:<br>Location 1: Construction cost $80,000 ;    Location 2: Construction cost $40,000    ……<br>The city is divided into 10 districts, each requiring different numbers of medical stations for coverage due to population density and<br>emergency medical needs:<br>Districts 1 and 2: require coverage by at least 4 stations ；     District 3: requires coverage by at least 2 stations      ……<br>Each candidate location can cover specific districts:<br>Location 1 covers districts: 1, 2, 6, 10 ；    Location 2 covers districts: 3, 5, 6, 9     ……<br>The objective is to decide which locations should be selected for building medical stations, minimizing the total construction cost<br>while meeting the coverage requirements for each district. Each location can only be selected or not selected (binary decision).<br><!-- End of picture text -->

Figure 13: An example of backtranslation: transforming mathematical formulations and LP files into natural language descriptions of optimization problems. The process transforms formal mathematical notation and concrete data into human-readable problem descriptions. 

problems, and mixed data combines the advantages of the above two very well, being the best in terms of average accuracy across the four types of test sets. 

#### **D.3 SFT** 

We employ the LlamaFactory framework for fine-tuning [84]. We select the Qwen2.5 series (0.5B _∼_ 32B) as our base models [82], and the hyperparameters are generally set as follows: initial learning rate of 1e-4, 1 _∼_ 3 epochs, LoRA rank of 32, LoRA alpha of 32, and LoRA dropout of 0.1. While there are minor variations in hyperparameters across different experiments, the overall settings remain similar and we omit these details for brevity. Notably, as illustrated in our framework diagram 1, the entire AutoFormulator training process is an iterative cycle. The Rejection Sampling in Step 2 relies on AutoFormulator’s modeling capabilities - stronger modeling abilities lead to higher pass rates and better data quality. Similarly, the data augmentation phase depends on AutoFormulator’s modeling competence. Higher quality data, in turn, results in a more capable Formulator through training.Through this systematic model fine-tuning and data augmentation approach, we have developed a dynamically evolving fine-tuning framework. This framework not only accurately transforms natural language descriptions into mathematical formulations and solver code but, more importantly, establishes a self-improving data flywheel 

23 



<!-- Start of picture text -->
66 65.77<br>65<br>64.37 64.26<br>64<br>63.06<br>63<br>62 61.56 61.67<br>60.86<br>61<br>60<br>0 1 3 5 7 9 10<br>Max Iteration of the self-refine loop<br>Acceptance Rate (%)<br><!-- End of picture text -->

Figure 14: Acceptance Rate vs. Maximum Iteration of Self-Refine Loop. The bar chart illustrates the acceptance rate achieved at different maximum iteration limits. 



<!-- Start of picture text -->
Original<br>5000 After Rejection<br>4000<br>3000<br>2000<br>1000<br>0<br>0 5000 10000<br>Problem Description Length<br>Frequency<br><!-- End of picture text -->

Figure 15: Distribution of Natural Language Description Lengths for Easy Problems in OptMATH-Train Dataset. The histogram compares the length distribution before and after rejection sampling, showing the quality filtering process. 

Table 3: Comparison of Original Data and Augmentation Data in Training Models. 

|Types|NL4OPT|MAMO<br>EasyLP|MAMO<br>ComplexLP|OptMATH<br>Bench|Micro<br>Avg|Macro<br>Avg|
|---|---|---|---|---|---|---|
|Without Augmentation|86.9%|**88.0%**|44.5%|31.1%|72.1%|62.3%|
|Without Original|82.9%|85.5%|44.7%|23.6%|69.2%|59.2%|
|Mixture of Augmentation and Original|**87.3**%|87.7%|**48.1%**|**33.3%**|**73.1%**|**64.1%**|



mechanism. This positive feedback loop enables the AutoFormulator system to continuously enhance its capability in handling complex optimization problems through ongoing learning and self-optimization, forming a virtuous growth cycle. 

#### **D.4 Detailed Ablation Studies on Model Size and Data Size** 

To investigate the impact of model capacity and training data volume on optimization modeling performance, we conducted two sets of experiments using OptMATH-Train. For the model size study in Figure 6 and Figure 17, we compare the performance of baseline and finetuned Qwen2.5 models ranging from 0.5B to 32B parameters. For the data scaling analysis in Figure 7 and Figure 18, we track the accuracy progression within the first training epoch across different model sizes, using varying proportions of the training data. 

The model size experiments reveal distinct scaling patterns across benchmarks. On NL4OPT, the performance improves from 12.7% (0.5B) to 96.7% (32B), showing particularly rapid gains in the 0.5B-3B range. For MAMO EasyLP, we observe similar but more moderate improvements, with accuracy increasing from 31.9% to 90.5%. However, on more challenging benchmarks like MAMO ComplexLP and OptMATH-Bench, even the largest models achieve relatively modest gains, reaching 52.6% and 30.6% respectively at 32B parameters. 

The comparison between baseline and OptMATH-Train finetuned models reveals interesting 

24 

#### An Example of AutoFormulation 

##### **Input-Natural Language Description** 

A city is planning the layout of emergency medical stations. There are 6 candidate locations for building medical stations, each with different construction costs: 

Location 1: Construction cost $80,000 ;    Location 2: Construction cost $40,000    …… 

The city is divided into 10 districts, each requiring different numbers of medical stations for coverage due to population density and emergency medical needs: 

Districts 1 and 2: require coverage by at least 4 stations ； District 3: requires coverage by at least 2 stations      …… Each candidate location can cover specific districts: 

Location 1 covers districts: 1, 2, 6, 10 ； Location 2 covers districts: 3, 5, 6, 9     …… 

The objective is to decide which locations should be selected for building medical stations, minimizing the total construction cost while meeting the coverage requirements for each district. Each location can only be selected or not selected (binary decision). 

## **AutoFormulation** 

##### **Output-General Formulation** 

##### **Output-Python Code with Gurobi** 



<!-- Start of picture text -->
from gurobipy import *<br># Create a new model<br>m = Model("Medical Station Location")<br># Parameters<br>costs = {<br>1: 8, # $80,000<br>2: 4,<br> represents the cost coefficient for each set …………<br>is a binary decision variable indicating whether set i is }<br>selected<br># Coverage requirements for each district<br> represents the set of all sets containing element j coverage_req = {<br> represents the minimum number of times element j 1: 4,<br>needs to be covered 2: 4,<br>3: 2,<br>…………<br>}<br># Coverage matrix<br>coverage = {<br>Output-Instance Formulation 1: [1, 2, 6, 10],<br>2: [3, 5, 6, 9],<br>1.Sets …………<br>L = {1,...,6}: set of potential locations }<br>D = {1,...,10}: set of districts # Decision Variables<br>selected = m.addVars(costs.keys(),<br>2. Parameters<br>vtype=GRB.BINARY, name="Selected")<br>c[i]: construction cost for location i ∈ L<br>c[1] = 8, c[2] = 4, c[3] = 2, c[4] = 1, c[5] = 8, c[6] = 9 # Objective Function<br>r[j]: coverage requirement for district j ∈ D m.setObjective(quicksum(costs[i] * selected[i] for<br>r[1] = 4, r[2] = 4, r[3] = 2, r[4] = 4, r[5] = 5 i in costs.keys()), GRB.MINIMIZE)<br>r[6] = 1, r[7] = 2, r[8] = 3, r[9] = 4, r[10] = 4 # Constraints<br>a[i,j]: coverage matrix, 1 if location i can cover district j, 0 for district in coverage_req.keys():<br>otherwise. # Sum up all locations<br>3. Variables m.addConstr(quicksum(selected[loc]<br>for loc in coverage.keys() if district in<br>x[i] ∈ {0,1}: binary decision variable coverage[loc])>=coverage_req[district],<br>f"MultiCover_e{district}")<br>x[i] = 1 if location i is selected<br>x[i] = 0 otherwise # Optimize model<br>m.optimize()<br>4. Objective Function<br>Minimize: ∑(i∈L) c[i]×x[i] (total construction cost) # Print results<br>5. Constraints if m.status == GRB.OPTIMAL:<br>    print("\nOptimal solution found:")<br>Coverage requirements: ∑(i∈L) a[i,j]×x[i] ≥ r[j], ∀j∈D<br>Binary constraints: x[i] ∈ {0,1}, ∀i∈L else:<br>    print("No solution found")<br><!-- End of picture text -->

Figure 16: An Example of AutoFormulation 

25 

Table 4: Performance comparison of Qwen2.5 models of varying sizes on mathematical optimization tasks. The percentages in parentheses indicate improvements after fine-tuning. 

|Models|NL4OPT|MAMO EasyLP|MAMO ComplexLP|OptMATH-Bench|Micro AVG|
|---|---|---|---|---|---|
|Qwen2.5-0.5B|0.00%|0.15%|0.00%|0.00%|0.08%|
|Qwen2.5-0.5B(Finetuned)|12.65% (↑12.65%)|31.90% (↑31.75%)|16.59% (↑16.59%)|15.03% (↑15.03%)|23.29% (↑23.21%)|
|Qwen2.5-1.5B|0.00%|2.15%|0.95%|0.00%|1.23%|
|Qwen2.5-1.5B(Finetuned)|46.12% (↑46.12%)|68.10% (↑65.95%)|22.75% (↑21.80%)|18.65% (↑18.65%)|49.27% (↑48.04%)|
|Qwen2.5-3B|67.35%|65.18%|16.11%|0.52%|48.04%|
|Qwen2.5-3B(Finetuned)|68.57% (↑1.22%)|80.98% (↑15.80%)|25.59% (↑9.48%)|15.03% (↑14.51%)|59.88% (↑11.84%)|
|Qwen2.5-7B|86.94%|83.59%|21.80%|1.55%|62.03%|
|Qwen2.5-7B(Finetuned)|86.94%|89.42% (↑5.83%)|48.82% (↑27.02%)|30.05% (↑28.50%)|73.56% (↑11.53%)|
|Qwen2.5-14B|93.47%|82.52%|42.65%|14.51%|68.02%|
|Qwen2.5-14B(Finetuned)|95.51% (↑2.04%)|90.49% (↑7.97%)|51.18% (↑8.53%)|29.53% (↑15.02%)|76.02% (↑8.00%)|
|Qwen2.5-32B|92.65%|82.21%|44.55%|9.33%|67.26%|
|Qwen2.5-32B(Finetuned)|96.73% (↑4.08%)|88.04% (↑5.83%)|56.4% (↑11.85%)|36.27% (↑26.94%)|76.86% (↑9.60%)|



patterns across different model scales. For simpler benchmarks like NL4OPT and MAMO EasyLP, while the performance gap narrows with increased model size, OptMATH-Train finetuning still provides consistent improvements even for the largest models. More notably, on complex benchmarks such as MAMO ComplexLP and OptMATH-Bench, models finetuned on OptMATH-Train demonstrate substantial performance gains across all model sizes, highlighting the effectiveness of our training dataset in enhancing models’ capabilities for challenging optimization problems. 

The data scaling analysis reveals distinct learning dynamics across model sizes. Smaller models (0.5B, 1.5B, 3B) exhibit higher initial performance variance during training, while larger models (7B, 14B) demonstrate more stable learning curves from the outset. Notably, all model sizes achieve relative performance stability after utilizing approximately 40% of the training data, though the absolute performance levels differ significantly. The 3B model, for instance, maintains consistently higher performance across all benchmarks while requiring a similar proportion of training data to reach stability. 

This efficient data utilization pattern holds true across all benchmarks, regardless of their complexity levels. Whether for the relatively straightforward tasks in NL4OPT or the more challenging problems in OptMATH-Bench, models typically converge to their peak performance using around 40% of the available training data. The remaining 60% of the data contributes primarily to fine-tuning and minor performance adjustments rather than substantial improvements. 

26 



<!-- Start of picture text -->
100 Baseline Model 86.9% 95.5% 2.0% 96.7% 4.1% 100 Baseline ModelFinetuned Model81.0%15.8% 89.4%5.8% 90.5% 8.0% 88.0%5.8%<br>Finetuned Model 80<br>80 65.9%<br>1.2% 68.1%<br>68.6%<br>60<br>60<br>46.1%<br>40 46.1% 86.9% 93.5% 92.7% 40 31.8% 83.6% 82.5% 82.2%<br>67.3% 31.9% 65.2%<br>20 12.7% 20<br>12.7%<br>0.0% 0.0% 0.1% 2.1%<br>0 0<br>0.5B 1.5B 3B 7B 14B 32B 0.5B 1.5B 3B 7B 14B 32B<br>Model Size Model Size<br>(a) NL4OPT (b) MAMO EasyLP<br>100 100<br>Baseline Model Baseline Model<br>Finetuned Model Finetuned Model<br>80 80<br>11.9%<br>60 48.8%27.0% 51.2% 8.5% 56.4% 60<br>26.9%<br>40 40 28.5% 15.0% 36.3%<br>20 16.6% 16.6% 22.8%21.8% 25.6%9.5% 42.6% 44.5% 20 15.0% 15.0% 18.6%18.6% 15.0% 14.5% 30.1% 29.5%<br>21.8%<br>16.1% 14.5%<br>0.0% 0.9% 0.0% 0.0% 0.5% 1.6% 9.3%<br>0 0<br>0.5B 1.5B 3B 7B 14B 32B 0.5B 1.5B 3B 7B 14B 32B<br>Model Size Model Size<br>(c) MAMO ComplexLP (d) OptMATH-Bench<br>Accuracy (%) Accuracy (%)<br>Accuracy (%) Accuracy (%)<br><!-- End of picture text -->

Figure 17: Scaling behavior of Qwen2.5 models (0.5B-32B) on various benchmarks. 

27 



<!-- Start of picture text -->
40 NL4OPT<br>35 MAMO EasyLP MAMO ComplexLP 80<br>OptMATH-Bench<br>30 Micro Accuracy<br>60<br>25<br>20<br>40<br>15<br>10 20 NL4OPT<br>5 MAMO EasyLPMAMO ComplexLP<br>0 0 OptMATHMicro Accuracy-Bench<br>0.0 0.2 0.4 0.6 0.8 1.0 0.0 0.2 0.4 0.6 0.8 1.0<br>Proportion Proportion<br>(a) Qwen2.5-0.5B (b) Qwen2.5-3B<br>100<br>80 80<br>60 60<br>40 40<br>20 NL4OPT 20 NL4OPT<br>MAMO EasyLP MAMO EasyLP<br>MAMO ComplexLP MAMO ComplexLP<br>0 OMicro AccuracyptMATH-Bench 0 OptMATH-Bench Micro Accuracy<br>0.0 0.2 0.4 0.6 0.8 1.0 0.0 0.2 0.4 0.6 0.8 1.0<br>Proportion Proportion<br>(c) Qwen2.5-7B (d) Qwen2.5-14B<br>Accuracy (%) Accuracy (%)<br>Accuracy (%) Accuracy (%)<br><!-- End of picture text -->

Figure 18: Scaling behavior of Qwen2.5-0.5B, Qwen2.5-3B, Qwen2.5-7B and Qwen2.5-14B Accuracy Within One Training Epoch. 

### **E Prompt Templates** 

In this section, we present all the important prompt templates. Due to space constraints, certain parts are omitted, and only the prompt frameworks are shown. 

#### **E.1 Reverse Data Generate Prompt** 

#### Generate Prompt 

```
AsanOperationsResearchExpert,analyzethegivenmathematicaloptimizationexpression
andLPdata.
```

```
......
InputMathematicalExpression:
{{mathematical_expression}}
InputLPData:
{{lp_data}}
ReferenceExamples:
{{examples}}
##RequiredOutput:
ProvideONLYaclear,detailednaturallanguagedescriptionoftheoptimizationproblem
that:
```

28 

- `Describes the complete scenario` 

- `States all decisions to be made` 

- `Specifies the objective clearly` 

- `Incorporates all constraints and conditions naturally` 

- `Includes all numerical parameters within narrative` 

- `Uses appropriate domain terminology` 

- `Maintains mathematical accuracy without showing formulation` 

#### Self-Criticism Prompt 

```
AsanOperationsResearchExpert,evaluateifthegeneratedproblemdescriptionmatches
themathematicaloptimizationproblem...
```

```
InputLPData:
{{lp_data}}
```

```
GeneratedProblemDescription:
{{problem_description}}
AnalysisSteps...
##RequiredOutput:
Ifperfectmatch:
"CompleteInstance"
Ifinconsistenciesexist:
"IncompleteInstance:
[Listspecificdiscrepancies...]"
```

29 

#### Self-Refinement Prompt 

```
AsanOperationsResearchExpert,analyzethecriticismandrefinetheproblem
descriptionifneeded.
```

```
First,checkthecriticismresult:
{{criticism}}
Ifthecriticismshows"CompleteInstance":
Output"Nothingneedtorefine"
```

```
Otherwise,followthesestepstogenerateanimproveddescription:
```

```
1.ReviewInputMaterials:
MathematicalExpression:
{{mathematical_expression}}
LPData:
{{lp_data}}
InitialDescription:
{{initial_description}}
2.Task:
```

```
Basedonthecriticismfeedback,LPdatainformation,andinitialdescription,generatea
completeandaccurateproblemdescription.
```

```
RequiredOutput:
Ifcriticismis"CompleteInstance":
Output"Nothingneedtorefine"
```

###### `Otherwise:` 

```
[Directnaturallanguagedescriptionoftheoptimizationproblem]
```

- `No introductory phrases or meta-commentary` 

- `No section headers or separators` 

- `Just the complete problem description in clear natural language` 

- `Ensure exact match with all LP data parameters` 

- `Include all constraints and objectives naturally` 

- `Avoid mathematical notation` 

```
Note:TheoutputshouldbeONLYthecompletenaturallanguagedescriptionitself,withno
additionaltextorformatting.
```

30 

#### **E.2 Baseline Prompt** 

#### Baseline Prompt Template for optimization modeling 

```
Belowisanoperationsresearchquestion.Buildamathematicalmodelandcorresponding
pythoncodeusing‘gurobipy‘thatappropriatelyaddressesthequestion.
#Question:
```

```
{}
```

```
#Notes:
```

- `Please output Python code starting with the following lines:‘‘‘python\n\nimport gurobipy as gp\nfrom gurobipy import GRB\n‘‘‘` 

- `Make sure the model variable is named ‘model‘.` 

- `Avoid using "<" and ">" in Gurobi constraints; instead, use "<=" or ">=" as appropriate .` 

- `Carefully determine whether the variable is an integer or a continuous variable.` 

```
#Response:
```

```
(Provideyourresponsehere,keepthenotesaboveinmind)
```

#### **E.3 AutoFormulation Instructions** 

#### CoT Instructions 

```
instructions=[
```

- `# Total instructions: 15 entries` 

- `# Showing 5 representative examples below...` 

- `"Below is an operations research question. Build a mathematical model and corresponding Python code using ‘gurobipy‘ to solve it.",` 

```
"Createacompletesolutionthatincludes:1)Mathematicalformulation2)Pythoncode
usinggurobipy3)Resultsinterpretation.Ensureallvariablesandconstraintsare
properlydefined.",
```

```
"Transformthisoperationsresearchproblemintoamathematicalmodelandimplement
itinPythonwithgurobipy.Includeclearvariabledefinitionsandconstraint
explanations.",
```

- `"The following is an operations research problem. Let’s solve it step by step: 1) Identify the decision variables, objective function, and constraints 2) Formulate the mathematical model 3) Implement the solution using Gurobi in Python 4) Verify and` 

- `interpret the results.",` 

```
"Thisisanoperationsresearchproblem.Followthisstructuredapproach:Beginwith
understandingtheproblem->Identifythekeyvariables->Analyzetheconstraints->
Developthemathematicalmodel->SolveitprogrammaticallyusingGurobiinPython.
Provideclearreasoningandexplanationsateachstage."
```

```
]
```

31 

#### **E.4 Prompts for Configuration Selecting** 

#### Initializing the Parameters 

```
Youareanoptimizationexperthelpingtotunetheparametersin:
```

```
\begin{verbatim}
{generator_code}
\end{verbatim}
```

```
CRITICALREQUIREMENT:
GeneratedinstancesMUSTbesolvabletoOPTIMALITYbyGurobi...
```

```
ModelComplexityScoreCalculation:
```

`1. Variable Score:` 

```
-Binaryvariables:weight={weights[’alpha\_bin’]}
-Integervariables:weight={weights[’alpha\_int’]}
-Continuousvariables:weight={weights[’alpha\_cont’]}
```

`2. Constraint Score...` 

`3. Additional Complexity Factors...` 

```
TotalScore=VariableScore+ConstraintScore+Big-MScore+ExpressionScore
```

```
SecondaryRequirements:
```

`1. Model Complexity: {complexity\_score\_min} to {complexity\_score\_max}` 

`2. Solve Time: {min\_solve\_time} to {max\_solve\_time} seconds` 

- `Return parameter values in JSON format matching ’default\_parameters’ structure: - Keep exact same keys` 

- `Preserve data types` 

- `Use lists for tuples` 

- `Format with proper indentation` 

#### Feedback Prompt 

```
Basedontesting{total_instances}instanceswithyoursuggestedparameters:
{last_suggested_parameters}
```

```
Herearethedetailedresults:
```

`1. Solution Status Analysis:` 

   - `Total Instances: {total_instances}` 

   - `Solvable Instances: {solvable_instances}` 

   - `OPTIMAL Solutions: {optimal_instances} ({optimal_rate:.1f}%)` 

   - `Solution Status Distribution:` 

   - `Status Percentages:` 

`2. Overall Performance (Only OPTIMAL Solutions):` 

   - `Success Rate: {success_rate:.1f}% ({results["requirements_met"]["all_requirements"]} out of {total_instances} instances met all requirements)` 

   - `Note: Only OPTIMAL solutions are considered successful` 

`3. Requirements Satisfaction (Only OPTIMAL Solutions): Complexity Score Distribution:{analyze_distribution("complexity")}` 

   - `Required range: {requirements}` 

   - `Success rate: {num_satisfying_requirements/total_instances}` 

32 

```
SolveTimeDistribution:{analyze_distribution("solvetime")}
```

   - `Required range: {requirements}` 

   - `Success rate: {num_satisfying_requirements/total_instances}` 

`4. Model Structure Analysis (Only OPTIMAL Solutions): Variable Distributions:` 

   - `Binary Variables: ...` 

```
ConstraintDistributions:
```

```
LinearConstraints:...
IndicatorConstraints:...
QuadraticConstraints:...
GeneralConstraints:...
```

```
ComplexityScoreComponents:...
```

`5. Distribution Analysis Insights:` 

   - `{throughout analysis of the instances generated by the parameters by calling statistics package in Python}` 

- `Based on these results and distribution analysis, please suggest parameter values that would:` 

`1. MAXIMIZE the proportion of instances that reach OPTIMAL status` 

`2. Adjust the model complexity to meet the target score range (for OPTIMAL instances)` 

`3. Maintain solve times within the required range (for OPTIMAL instances)` 

`4. Reduce variability in key metrics where high variance was detected` 

`5. Increase the overall success rate` 

- `Return your response in JSON format, strictly following the structure of the previous suggestions dictionary. Ensure that:` 

`1. All keys remain exactly the same as in the previous suggestions` 

`2. The data types for each value are preserved` 

`3. The JSON should be properly formatted with indentation for readability` 

`4. Do not add any new keys or remove any existing keys` 

33 

#### **E.5 An Example of Metadata** 

Metadata 

```
Subclass:BinPacking
```

```
Reference:Garey,M.R.andJohnson,D.S."ApproximationAlgorithmsfor
BinPackingProblems:ASurvey."AnalysisandDesignofAlgorithmsin
CombinatorialOptimization(1981)
```

```
ReferenceURL:https://doi.org/10.1007/978-3-7091-2748-38
MathematicalFormula:
```

_`Consider` n_ _`items, where each item` i_ _`has:`_ 

- `Weight` _si_ `: The weight of item` _i_ 

```
Theproblemincludes:
```

- `Bin Capacity` _c_ `: The uniform capacity of each bin` 

- `Bin Usage Variable` _yj_ `: A binary variable indicating whether bin` _j_ `is used` 

- `Assignment Variable` _xi,j_ `: A binary variable indicating whether item` _i_ `is assigned to bin` _j_ 



34 

#### **E.6 An Example of Generator** 

#### Python Code for Bin Packing Generator 

1 <mark>`import gurobipy as gp`</mark> 2 <mark>`from gurobipy import GRB`</mark> 3 <mark>`import random`</mark> 4 5 <mark>`class Generator:`</mark> 6 <mark>`def __init__(self, parameters=None, seed=None):`</mark> 7 <mark>`self.problem_type = "binpacking"`</mark> 8 <mark>`default_parameters = {`</mark> 9 <mark>`"n_items": (3, 10),`</mark> 10 <mark>`"weight_range": (1, 50),`</mark> 11 <mark>`"bin_capacity": 100`</mark> 12 <mark>`}`</mark> 13 <mark>`if parameters is None:`</mark> 14 <mark>`parameters = default_parameters`</mark> 15 <mark>`for key, value in parameters.items():`</mark> 16 <mark>`setattr(self, key, value)`</mark> 17 <mark>`self.seed = seed`</mark> 18 <mark>`if self.seed:`</mark> 19 <mark>`random.seed(seed)`</mark> 20 21 <mark>`def generate_instance(self):`</mark> 22 <mark>`self.n_items = random.randint(*self.n_items)`</mark> 23 <mark>`items = list(range(self.n_items))`</mark> 24 <mark>`item_weights = {i: random.randint(*self.weight_range) for i in items}`</mark> 25 26 <mark>`model = gp.Model("BinPacking")`</mark> 27 <mark>`model.Params.OutputFlag = 0 # Suppress Gurobi output`</mark> 28 <mark>`x = model.addVars(items, items, vtype=GRB.BINARY, name="x")`</mark> 29 <mark>`y = model.addVars(items, vtype=GRB.BINARY, name="y")`</mark> 30 31 <mark>`# Objective: Minimize the number of bins used`</mark> 32 <mark>`model.setObjective(gp.quicksum(y[j] for j in items), GRB.MINIMIZE)`</mark> 33 <mark>`for j in items:`</mark> 34 <mark>`model.addConstr(`</mark> 35 <mark>`gp.quicksum(item_weights[i] * x[i,j] for i in items) <= self. bin_capacity * y[j],`</mark> 36 <mark>`name=f"Capacity_{j}"`</mark> 37 <mark>`)`</mark> 38 <mark>`for i in items:`</mark> 39 <mark>`model.addConstr(`</mark> 40 <mark>`gp.quicksum(x[i,j] for j in items) == 1,`</mark> 41 <mark>`name=f"Assignment_{i}"`</mark> 42 <mark>`)`</mark> 43 <mark>`return model`</mark> 

35 

#### **E.7 Augmentation Prompt** 

#### Generate Augmentation Problem Prompt 

```
AUGMENTATION_RULES=[
```

```
#SemanticEnhancement
"Rephrasetheproblemdescriptionwhilemaintainingthesamemathematicalstructure
...",
```

- `"Rewrite the problem using different expressions and terminology...", # Change the scenario` 

```
"Transformtheproblemintoadifferentapplicationscenariowhilepreservingthe
samestructure...",
"Conceiveavariantonanotherscenarioforthemathematicalmodel...",
#Numericalenhancement
```

```
"Changethenumericalparameterswhilemaintainingthesameproblemstructure...",
"Scaleupordowntheproblemsizebyadjustingparametersproportionally...",
#Problemvariantgeneration
```

```
"Generateavariantbyadding/removing/modifyingconstraints...",
```

```
"Createavariationbycombiningdifferenttypesofconstraints...",
#Complicatingtheproblem
```

```
##VariableExpansion
```

```
"Increasethenumberofdecisionvariableswhilemaintainingsimilarstructure...",
"Addboundsforadjustmentvariables...",
```

```
##ConstraintsExpansion
```

```
"Addrealisticconstraintslikecapacitylimitations,budgetrestrictions...",
"Introducecross-variableconstraintsbetweencomponents...",
```

```
##DataComplexity
```

```
"Convertparametersintotabularformwithmorecomplexdatastructures...",
```

```
##ProblemTypes
```

```
"Generatenon-linearproblemsbyreplacinglinearrelations...",
```

```
"Combinewithotherproblemtypestogeneratehybridproblems...",
```

```
#Multi-objective
```

```
"Addnewobjectivefunctionstogeneratemulti-objectiveproblems...",
```

```
"Modifyobjectivefunctiontoincludeadditionalterms...",
```

- `# Problem symmetry` 

```
"Generatevariantsbyintroducingsymmetries...",
```

```
"Generatedualproblemswhilemodifyingparametersandconstraints..."
```

```
]
```

```
AUGMENTATION_TEMPLATE="""Belowisanoptimizationproblem,pleasegenerateanew
optimizationproblembyfollowingtheaugmentationruleprovided.
```

```
#OriginalProblem
Theoriginaloptimizationproblemisasfollows:
’’’
{original_problem}
’’’
#AugmentationRule
```

```
{rule}
```

```
#AugmentedProblem
```

```
Pleaseconstructanewoptimizationproblemaccordingtotheaboverequirementsandthe
providedquestioninthefollowingformat:
```

```
[Writeyournewproblemhere]
```

```
Note:Thegeneratedproblemshouldmaintainmathematicalvalidityandpractical
feasibility.Andjustprovidetheproblemdescriptionwithoutanyadditional
information.
```

```
"""
```

36 

