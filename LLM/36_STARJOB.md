**Starjob: Dataset for LLM-Driven Job Shop Scheduling** 

**Henrik Abgaryan**<sup>1</sup> **Tristan Cazenave**<sup>* 1</sup> **Ararat Harutyunyan**<sup>* 1</sup> 

# **Abstract** 

Large Language Models (LLMs) have shown remarkable capabilities across various domains, but their potential for solving combinatorial optimization problems remains largely unexplored. In this paper, we investigate the applicability of LLMs to the Job Shop Scheduling Problem (JSSP), a classic challenge in combinatorial optimization that requires efficient job allocation to machines to minimize makespan. To this end, we introduce Starjob, the first supervised dataset for JSSP, comprising 130k instances specifically designed for training LLMs. Leveraging this dataset, we fine-tune the LLaMA 8B 4-bit quantized model with the LoRA method to develop an end-to-end scheduling approach. Our evaluation on standard benchmarks demonstrates that the proposed LLMbased method not only surpasses traditional Priority Dispatching Rules (PDRs) but also achieves notable improvements over state-of-the-art neural approaches like L2D, with an average improvement of 15.36% on DMU and 7.85% on Taillard benchmarks. These results highlight the untapped potential of LLMs in tackling combinatorial optimization problems, paving the way for future advancements in this area. ###Instruction: Directly give the 

# **1. Introduction** 

Large Language Models (LLMs), despite their powerful capabilities in natural language processing, have not traditionally been associated with solving computationally intensive problems. Specifically, their applicability to NP-hard combinatorial optimization problems is often considered limited compared to other neural approaches. This perception is reinforced by the lack of examples where LLMs have successfully outperformed methods like reinforcement learning 

> 1Department of Computer Science, Universite Paris Dauphine-´ PSL, Paris, France. Correspondence to: Henrik Abgaryan _<_ henrik.abgaryan@dauphine.eu _>_ , Tristan Cazenave _<_ tristan.cazenave@lamsade.dauphine.fr _>_ , Ararat Harutyunyan _<_ ararat.harutyunyan@lamsade.dauphine.fr _>_ . 

in such domains. Furthermore, LLMs are prone to “hallucinations,” where they not only fail to solve problem instances but also produce infeasible solutions. Consequently, LLMs have yet to be seriously explored (including fine-tuning) for tackling hard combinatorial problems. 

In this paper, we challenge this prevailing intuition by demonstrating that LLMs, when fine-tuned, can be effective for certain combinatorial optimization problems. We present the first fine-tuned LLM model for the Job Shop Scheduling Problem (JSSP)—and, to the best of our knowledge, for any NP-hard combinatorial problem. Our results show that for JSSP, LLMs not only generate feasible solutions but also surpass Priority Dispatch Rule (PDR) methods and outperform the earliest neural approaches that first exceeded PDR performance (e.g., L2D (Zhang et al., 2020)). These findings suggest LLMs, with refinement, could rival advanced neural methods for combinatorial optimization, paving the way for broader applications and a new computational paradigm. 

The job shop scheduling problem (JSSP) optimizes the allocation of _NJ_ jobs with varying processing times to _NM_ machines, targeting metrics like makespan ( _Cmax_ ) or average flow time. It has critical applications in manufacturing and services. Traditional methods, relying on mathematical programming and heuristics, often face scalability and precedence challenges. Advances in AI, such as reinforcement learning and graph neural networks, offer promising data-driven alternatives (Chaudhry & Khan, 2015)(Zhang et al., 2020)(Corsini et al., 2024). (Huang et al., 2022) examined the graph reasoning capabilities of large language models (LLMs) on tasks like connectivity, shortest paths, maximum flow, and Hamilton paths. While LLMs show promise, their performance declines on complex problems, often relying on spurious correlations. To address this, (Huang et al., 2022) introduced improved prompting strategies. (Valmeekam et al., 2022) introduce a benchmark to test for evaluating the planning/reasoning capabilities of LLMs. Recently, (Chen et al., 2024b) investigate the application of LLMs to the task of graph node classification. 

Collectively, these studies underscore the growing use of LLMs for tasks involving implicit structures, while their application to scheduling problems remains unexplored. This paper is the first to utilize LLMs for end-to-end scheduling in JSSP, leveraging their ability to process and rea- 

1 

**Starjob: Dataset for LLM-Driven Job Shop Scheduling** 

son over complex information to tackle this challenge. To this end, we introduce the first supervised dataset Starjob designed to fine-tune LLMs specifically for the task of JSSP. Instead of traditional matrix representation format, this dataset includes natural language description of the JSSP problem and its solution. On two well-known JSSP benchmarks Tai(Taillard, 1993) and DMU(Demirkol et al., 1998), we show that minimal fine-tuning through RsLoRA (Kalajdzievski, 2023) on the proposed dataset enables LLM to schedule, by finding high-quality solutions, surpassing classic PDRs and exceeding other neural approaches. 

The contributions of this work to the field of JSSP are multifaceted: 

- We introduce the first-ever supervised dataset Starjob containing 130,000 instances specifically designed for training LLMs in the context of JSSP 

- We introduce the use of fine-tuned LLMs for end-toend JSSP scheduling, showcasing their ability to reason over complex constraints with the Starjob dataset and RsLoRA method 

- We evaluate the performance of LLM-based scheduling against four traditional PDRs and the neural method L2D, demonstrating its superior generalization on large-scale JSSP graph instances having 1000 nodes 

- Our LLM-based approach enables natural language interactions with the scheduler, allowing users to inquire about specific JSSP instances and gain insights into constraints, enhancing system transparency and usability. 

# **2. Related Work** 

JSSP with more than two machines is proven to be NP-hard (Garey et al., 1976). As a result, finding exact solutions for JSSP is generally infeasible, leading to the widespread use of heuristic and approximate methods for practical efficiency (Cebi et al., 2020). Traditional approaches to solving JSSP have primarily relied on search and inference techniques developed by the constraint programming community (Beck et al., 2010). These techniques effectively leverage constraints to define the relationships and limitations between jobs and resources, enabling efficient exploration of feasible solution spaces and the identification of optimal or nearoptimal schedules (Nowicki & Smutnicki, 2005). A widely used heuristic method in real-world scheduling systems is the Priority Dispatching Rule (PDR) (Zahmani et al., 2015). PDRs are simple and effective, although designing an efficient PDR is time-consuming and requires extensive domain knowledge. 

Recently, approaches utilizing Deep Learning and Neural Networks have gained attention for finding promising solutions to the JSSP (Bonetta et al., 2023; Zhang et al., 2020; Corsini et al., 2024). These methods can be broadly categorized into supervised learning and reinforcement learning (RL). Current research in deep reinforcement learning (DRL) is actively focused on developing advanced methods to tackle JSSP. Existing DRL methods typically represent JSSP as a Markov Decision Process (MDP) and learn a policy network based on DRL techniques(Zhang et al., 2020). 

Large language models (LLMs) are now being applied to a wider range of tasks beyond language processing. In areas like robotics and planning (Huang et al., 2022). While there are currently no papers that directly address the scheduling of Job Shop Scheduling Problems (JSSP) using LLMs, some notable works explore the potential of LLMs in mathematical reasoning and programming (Chen et al., 2023; Wei et al., 2022; Ahn et al., 2024; Yang et al., 2023). Optimization using LLMs has gained significant interest in recent years, with several works exploring their capabilities across various domains (Yang et al., 2023). The ability of LLMs to understand and generate natural language has opened new possibilities for optimization tasks that were traditionally solved using derivative-based algorithms or heuristic methods(Yang et al., 2023). (Chen et al., 2023) evaluated LLMs’ performance in mathematical problem-solving and introduced ”Program of Thoughts” (PoT) prompting. Unlike Chain of Thoughts (CoT) (Wei et al., 2022), which combines reasoning and computation, PoT generates reasoning as code statements and delegates computation to an interpreter. (Ahn et al., 2024) surveys mathematical problems and datasets studied with LLMs, analyzing their strengths and weaknesses. (Frieder et al., 2024) examines LLMs’ impact on mathematicians, exploring their role in research, education, problem-solving, and proof generation, offering a balanced view of their capabilities.Recent works (Yang et al., 2023) explore LLMs as optimizers, using prompts to refine solutions iteratively. Case studies on linear reeeession and the traveling salesman problem show LLMs can produce high-quality solutions, sometimes matching heuristic algorithms in small-scale scenarios. Explorations into using LLMs for graph learning tasks have yielded notable approaches. (Huang et al., 2022) noted that LLMs exhibit some initial graph reasoning capabilities, but their performance decreases with problem complexity, (Huang et al., 2022) introduced prompting strategies to improve LLMs graph reasoning. (Valmeekam et al., 2022) developed a benchmark for assessing the planning and reasoning abilities of LLMs. More recently, (Chen et al., 2024b) examined the use of LLMs for graph node classification tasks. (Chen et al., 2024a) introduces two pipelines: LLMs-as-Enhancers, where LLMs refine textual data for Graph Neural Networks (GNNs), and LLMs-as-Predictors, where LLMs generate 

> 0https://github.com/starjob42/Starjob 

2 

**Starjob: Dataset for LLM-Driven Job Shop Scheduling** 

predictions directly from graph structures in natural language. Additionally, (Zhao et al., 2024) proposed GRAPHTEXT, translating graphs into natural language for trainingfree reasoning, often matching or exceeding GNNs. These works highlight the potential of LLMs in graph-related tasks, but their application to scheduling problems remains largely unexplored. 

# **3. Preliminary** 

JSSP is formally defined as a problem involving a set of jobs _J_ and a set of machines _M_ . The size of the JSSP problem instance is described as _NJ × NM_ , where _NJ_ represents the number of jobs and _NM_ the number of machines. For each job _Ji ∈ J_ , it must be processed through _ni_ machines (where _ni_ is the number of operations for job _Ji_ ) in a specified order _Oi_ 1 _→ . . . → Oini_ , where each _Oij_ (for 1 _≤ j ≤ ni_ ) represents an operation of _Ji_ with a processing time _pij ∈_ N. This sequence also includes a precedence constraint. Each machine can process only one job at a time, and switching jobs mid-operation is not allowed. The objective of solving a JSSP is to determine a schedule, that is, a start time _Sij_ for each operation _Oij_ , to minimize the makespan _C_ max = max _i,j{Cij_ = _Sij_ + _pij}_ while meeting all constraints. The complexity of a JSSP instance can be represented as a graph with _NJ × NM_ nodes, where each node corresponds to an operation. 

# **4. Dataset Generation** 

In order to try to solve the JSSP with LLM, we first need to represent the problem in natural language. To do that, we have to transform the matrix-based representation in standard JSSP format to a human-readable format. See the example in Listing 1. 

**Listing 1:** Job Shop Scheduling Problem instance (ft06) (Fisher and Thompson 1963) with _NJ_ = 6 and _NM_ = 6. The problem instance begins with the problem size on the first row, followed by the operations for each job. Odd columns list machines, and even columns list durations. The last row indicates the makespan (55.0). 

6 6 2 1 0 3 1 6 3 7 5 3 4 6 1 8 2 5 4 10 5 10 0 10 3 4 2 5 3 4 5 8 0 9 1 1 4 7 1 5 0 5 2 5 3 3 4 8 5 9 2 9 1 3 4 5 5 4 0 3 3 1 1 3 3 3 5 9 0 10 4 4 2 1 55 

## **4.1. Converting JSSP problem instance to Natural Language: Feature Generation** 

The approach describes the machines required for each job, providing a job-centric view of the scheduling problem. 

- **Initialization:** Begins by introducing the problem, detailing the number of jobs and machines involved. 

- **Problem Organization:** Enumerates jobs, specifying the sequence of the corresponding machines, and their respective durations. 

_Listing 1._ Natural Language description of a JSSP instance of size _NJ_ = 3 and _NM_ = 3 

- Optimize schedule f o r 3 Jobs ( denoted as J ) a c r o s s 3 Machines ( denoted as M) to minimize makespan . The makespan i s the completion time of the l a s t o p e r a t i o n in the schedule . Each 

- M can proces s only one J a t a time , and once s t a r t e d , J cannot be i n t e r r u p t e d . 

J0 : M0:105 M1:29 M2:213 J1 : M0:193 M1:18 M2:213 J3 : M0:78 M1:74 M2:221 

## **4.2. Definitions** 

- _Lp_ : Natural language representation of a problem instance _p_ . 

- _s_ : A solution in natural language, detailing operation sequences, machine assignments, and timings. 

3 

**Starjob: Dataset for LLM-Driven Job Shop Scheduling** 

- _Sp_<sup>_f_:Set of feasible solutions satisfying all JSSP con-</sup> straints. 

- _M_ ( _s_ ): Makespan of solution _s_ . 

- Objective: Minimize _M_ ( _s_ ) for feasible solutions _s ∈ S_<sup>_f_</sup> _p_<sup>.</sup> 

## **4.3. Proposed Method** 

1. **Fine-Tuning:** Train the LLM on problem-solution pairs ( _Lp, s_ ) to generate valid schedules. 

2. **Inference:** Generate _S_ candidate solutions: 



3. **Feasibility Check:** Filter feasible solutions: 



4. **Optimization:** Select the solution with the minimum makespan: 



## **4.4. Description of Rank-Stabilized LoRA Training** 

Rank-Stabilized Low-Rank Adaptation (rsLoRA) (Kalajdzievski, 2023) is a method for fine-tuning large language models with low-rank adapters that remain stable even at higher ranks. It addresses the limitation in standard LoRA (Hu et al., 2022) where the scaling factor is set as<sup>_<u>α</u>_</sup> _r_<sup>,</sup> which often leads to gradient collapse or under-utilization of higher-rank adapters. In rsLoRA, the scaling factor is modified to 



ensuring that the adapter outputs (and their gradients) remain well-conditioned across different ranks. 

## 4.4.1. LOW-RANK PARAMETER DECOMPOSITION 

Similar to LoRA, rsLoRA begins with the frozen pre-trained parameters of the LLM, _θ_ 0, and learns a low-rank update ∆ _ϕ_ : 



where _U, V ∈_ R<sup>_d×r_</sup> (or equivalently _B, A_ in some references), with a small rank _r ≪ d_ . The effective model parameters during fine-tuning become: 



where the critical _rank-stabilized_ scaling factor is 



Only _U_ and _V_ (i.e. ∆ _ϕ_ ) are trained, while _θ_ 0 remains fixed. 

## 4.4.2. RANK-STABILIZATION VIA THE SCALING FACTOR 

The main insight of rsLoRA is that setting _γr_ = _~~√~~_ _<u>αr</u>_<sup>en-</sup> sures the output variance of ∆ _ϕ_ is Θ(1) (constant order) as _r_ grows. This prevents gradient collapse and allows higher-rank adapters to _actually_ improve performance when sufficient computational resources are available. In contrast, the standard LoRA choice _γr_ =<sup>_<u>α</u>_</sup> _r_<sup>frequently under-utilizes</sup> larger ranks and leads to similar performance across different ranks. 

Mathematically, Kalajdzievski et al. (Kalajdzievski, 2023) show that for infinite-rank analysis, _γr ∈_ Θ� _r_<sup>_−_</sup><sup><u>1</u></sup> 2<sup>�</sup> is both necessary and sufficient to maintain stable updates throughout training. 

## 4.4.3. LOSS FUNCTION FOR FINE-TUNING 

Let _{_ ( _L_<sup>(</sup> _p_<sup>_i_)</sup><sup>_, s_(</sup><sup>_i_))</sup><sup>_}N_</sup> _i_ =1<sup>be a dataset of problem-solution pairs.</sup> Each solution _s_<sup>(</sup><sup>_i_)</sup> is tokenized as _{w_ 1 _, . . . , wTi}_ . Using an auto-regressive language modeling objective, the negative log-likelihood (NLL) for a single example is: 



Thus, the training loss summed over all samples is: 



## **4.5. Zero-shot inference and Label generation** 

Our choice of LLM is Meta-Llama-3.1-8B-Instruct-bnb4bit open-source model with a 128K context size. Later, we will refer to this model as Llama. The model is one of the open-source AI models developed by Meta. Llama 3.1 is an auto-regressive language model that uses an optimized transformer architecture (AI, 2024). For this study, we intentionally limited ourselves to using a single A6000 GPU and the 4-bit quantized(instead of full 32-bit) version of the model, demonstrating that our proposed dataset enables effective learning even under such constraints. 

Initially, we considered performing zero-shot inference with the Llama3.1 to solve the JSSP. However, the model consistently produced general descriptions of how to solve the problem instead of actual solutions. Promt engineering did not help. Occasionally, for very short instances (e.g 2x2, 3x2) it provided partial solutions, however, during each inference time the structure of the provided solution was different, making it hard to parse the solution. 

Because the zero-shot inference results were not satisfactory, we decided to finetune the LLM using a supervised approach. 

4 

**Starjob: Dataset for LLM-Driven Job Shop Scheduling** 

This required creating a supervised dataset, which included not only the problem formulations in natural language as described in Section 4 but also the solutions. To generate feasible solutions, we employed Google’s OR-Tools. The configuration for the Google’s OR-Tools solver was set as follows: 

- Maximum time allowed for the solver: 300 seconds. 

- Number of search workers: 42. 

- Search branching strategy: cp ~~m~~ odel.AUTOMATIC ~~S~~ EARCH. 

# **5. Training Details** 

We fine-tuned Llama 3.1, an 8 billion-parameter model from Meta, utilizing a 4-bit quantized version to minimize memory usage. We used Rank-Stabilized Low-Rank Adaptation (RSLoRA) (Kalajdzievski, 2023) with a rank of _r_ = 64 and _α_ = 64. The training required roughly 70 hours and about 30GB of GPU memory. In comparison, the dedicated Neural network such as (Zhang et al., 2020) requires 68.3 hours. We limited the context length of the model to 40k instead of the original 128k context length, to reduce memory consumption and increase the speed of fine-tuning. “Context length” refers to the maximum number of tokens (words or subwords) the model can process at once as input. 

# **6. Evaluation** 

We have generated approximately 130,000 random JSSP problems of various sizes<sup>1</sup> , ranging from 2x2 to 20x20, with the duration of each operation between 5 and 500 units. Additionally, we included several larger examples, such as 30x15, 50x20 etc., with approximately 1,000 instances, to enhance generalizability. We created problems with asymmetric sizes also, such as 3x2 and 10x5, to enhance the model’s generalization capability. Overall, the final dataset consists of around 130,000 natural language descriptions of JSSP problems along with their feasible solutions. Since we limited the maximum allowed time for Google’s OR-Tools to 300 seconds, the optimality of solutions for problems with _NJ >_ 10 and _NM >_ 10 is not guaranteed. The generated solution is converted to LLM format as described in 

4 

_Listing 2._ Natural Language description of the solution of JSSP problem instance of size _NJ_ = 3 and _NM_ = 3 S o l u t i o n : J2 −M0: 0+78 − _>_ 78 , J1 −M2: 0+193 − _>_ 193 , J0 −M0: 78+105 − _>_ 183 , J0 −M1: 183+29 − _>_ 212 , J2 −M2: 193+74 − _>_ 267 , J1 −M1: 212+18 − _>_ 230 , J1 −M0: 230+213 − _>_ 443 , J2 −M1: 267+221 − _>_ 488 , J0 −M2: 267+213 − _>_ 480 Maximum end completion time or Makespan : 488 

Representation in summation format aids LLM in performing computations effectively, enabling them to accurately calculate the makespan and produce feasible solutions with the minimum makespan; in contrast, our comparison with solutions generated without the summation operation often resulted in infeasible outputs. 

1https://github.com/starjob42/Starjob 

To ensure a fair comparison, we evaluated the fine-tuned LLM on two well-known benchmarks, Tai (Taillard, 1993) and DMU (Demirkol et al., 1998), focusing on diverse problem instances. Since this is the first time an LLM has been employed for end-to-end scheduling on the JSSP problem, we compared its performance to the first neural approach, L2D (Zhang et al., 2020), which was one of the first methods that demonstrated superiority over traditional priority dispatching rules (PDRs). The PDRs included in the comparison are Shortest Processing Time (SPT), Most Work Remaining (MWKR), Most Operations Remaining (MOPNR), and the minimum ratio of Flow Due Date to Most Work Remaining (FDD/MWKR). 

During inference, the context length is set to 40k to align with the configuration used during the fine-tuning phase. A sampling strategy is employed, using the default hyperparameters. Additionally, a sample size of _S_ = 20 is specified, meaning that at each inference step, the model generates and returns 20 different outputs for evaluation. During both training and inference time, the model was loaded in the format _float_ 4. The inference process itself consumes approximately 30GB of memory on the NVIDIA A6000 GPU. The largest instance to be tested in total contains around 23000 tokens. 

For faster inference, the fine-tuned model can be converted into the llama.cpp format (Gerganov, 2023). This conversion enables an impressive inference speed of 102.22 tokens per second, as reported in (Dai, 2024), when running on an NVIDIA RTX A6000 GPU with 48 GB of memory. Notably, the inference speed and memory usage of the LLM remain consistent across different language tasks, depending only on the token sequence length rather than the specific problem being solved. This consistency applies equally to tasks like ours (JSSP) and other tasks of similar token lengths. Consequently, the largest instance that fits within a 40,000-token context length, comprising a total of 22,224 

5 

**Starjob: Dataset for LLM-Driven Job Shop Scheduling** 

tokens, requires approximately 217.41 seconds per sample. 

## **6.1. Overview of JSSP Solution Parsing and Validation** 

Given a JSSP problem instance _Lp_ and a solution _s_ in natural language, the feasibility check ensures that _s_ satisfies all constraints and identifies feasible solutions _Sp_<sup>_f_.The</sup> objective is to minimize the makespan: 



where _M_ ( _s_ ) is the makespan of solution _s_ . 

6.1.1. VALIDATION STEPS 

1. **Parsing Inputs:** Extract jobs _Ji_ , machines _Mk_ , operations _Oij_ , start times _Sij_ , processing times _pij_ , end times _Cij_ , and declared makespan _C_ max. 

2. **Precedence Constraints:** For each job _Ji_ , ensure operations _Oij_ follow their prescribed order: 

comparison is fair because L2D was the first approach to use neural networks to outperform classic priority dispatching rule (PDR) methods, making it analogous to our work, which is the first to apply LLMs to JSSP. L2D’s method utilizes a Graph Neural Network (GNN) with Proximal Policy Optimization (PPO)(Schulman et al., 2017) and employs a size-agnostic policy network for generalization. Table 1 and Table 2 presents the performance comparison of the Llama-Finetuned model on the proposed Starjob dataset against various scheduling methods (L2D, SPT, MWKR, FDD/WKR, MOPNR) on the Tai (Taillard, 1993) and DMU (Demirkol et al., 1998) datasets, focusing on gap percentages relative to the best known solution makespan from the literature. The best solutions for Taillard’s and DMU instances can be found in<sup>2</sup> and<sup>3</sup> , respectively. 

The performance on each benchmark was evaluated using the _Percentage Gap_ (PG), defined as: 





3. **Machine Constraints:** For each machine _Mk_ , verify no overlapping operations: 



where _Oij_ and _Okl_ are operations assigned to _Mk_ . 

4. **Completeness and Validity:** Check that: 

   - All jobs _Ji_ and operations _Oij_ are represented. 

   - Machines _Mk_ process only one operation at a time. 

   - All start and end times _Sij, Cij_ are within valid bounds. 

5. **Makespan Validation:** Compute: 



and compare it with the declared makespan. If mismatched, the solution is invalid. 

If all these checks pass, the solution is deemed feasible. 

# **7. Empirical Performance Analysis** 

In this section, we provide an in-depth comparison of various job scheduling approaches. Since this is the first time an LLM is applied as an end-to-end scheduler for the JSSP, we compare our approach with the work presented in ”Learning to Dispatch for Job Shop Scheduling via Deep Reinforcement Learning” (L2D) (Zhang et al., 2020) . This 

where _M_ alg represents the makespan generated by the algorithm, and _M_ ub denotes the best-known makespan (or sometimes the optimal) for the instance. Lower PG values indicate better performance, as they correspond to solutions with objective values closer to the optimal or bestknown makespan. Figure 1, Figure 3, and Figure 2, Figure 4 presents the performance on both Tai(Taillard, 1993) and DMU (Demirkol et al., 1998) datasets across various configurations of _NJ_ and _NM_ . On Tai benchmark dataset instances with Across instances ranging from 15 jobs and 15 machines to 50 jobs and 20 machines, the fine-tuned Llama 3.1 consistently outperforms all other methods. Even on larger instances with 50 Jobs and 20 Machines (having 1000 nodes in graph representation as described in Sec. 3) Llama (24.32%) still outperformes L2D (26.40%). Average Gap: Finetuned Llama (21.69%) is significantly lower than SPT (60.57%), MWKR (55.29%), FDD/WKR (46.77%), and MOPNR (42.99%), L2D (29.54%). 

On the DMU benchmark dataset with 50 Jobs and 15 Machines finetuned Llama (22.14%) again demonstrates superior performance (over 15%) against all methods including L2D(37.50 %) (Zhang et al., 2020). Finetuned Llama (22.14%) is also notably lower average gap on DMU benchmark. The _SPT_ consistently exhibits the highest gap percentages, exceeding 60% for most problem instances. This is expected since _SPT_ , while simple, often fails to account for job-shop constraints in complex problem settings. The _MWKR_ and _FDD/WKR_ heuristics, which are more sophisticated than _SPT_ , perform moderately better, with gap per- 

> 2http://optimizizer.com/TA.php 

> 3http://jobshop.jjvh.nl/ 

6 

**Starjob: Dataset for LLM-Driven Job Shop Scheduling** 



<!-- Start of picture text -->
centages ranging between 50% and 70%. However, these 70 Gap for J=20.0, M=20.0<br>heuristics are still outclassed by the machine learning-based 60<br>approaches, likely due to their myopic decision-making, 50<br>which does not factor in longer-term scheduling impacts. 40<br>For additional detailed makspan ad gap of each instance. 30<br>20<br>Gap for J=15.0, M=15.0<br>70<br>60 Instance<br>Gap for J=30.0, M=15.0<br>50<br>70<br>40<br>30 60<br>20 50<br>40<br>Instance 30<br>Gap for J=20.0, M=15.0<br>80 20<br>70<br>60 Instance<br>50 Gap for J=30.0, M=20.0<br>90<br>40<br>30 80<br>20 70<br>10 60<br>MethodsInstance 50<br>SPT<br>MWKR 40<br>FDD/WKR<br>MOPNR 30<br>L2D<br>LLM-FT-Ours 20<br>Instance<br>Gap for J=50.0, M=15.0<br>Figure 1.  Comparison of different methods on TAI(Taillard, 1993)Taillard, 1993), 1993) 1993)) 60<br>benchmark.<br>50<br>40<br>Gap for J=20.0, M=15.0<br>80 30<br>70<br>20<br>60<br>50 10<br>40<br>30 Instance<br>20 Gap for J=50.0, M=20.0<br>70<br>Instance 60<br>Gap for J=20.0, M=20.0<br>50<br>80<br>40<br>60 30<br>40 20<br>20 Instance<br>Instance<br>Methods<br>Methods SPT<br>SPT MWKR<br>MWKR FDD/WKR<br>FDD/WKR MOPNR<br>MOPNR L2D<br>L2D LLM-FT-Ours<br>LLM-FT-Ours<br>Ta21 Ta22 Ta23 Ta24 Ta25 Ta26 Ta27 Ta28 Ta29 Ta30<br>Ta01 Ta02 Ta03 Ta04 Ta05 Ta06 Ta07 Ta08 Ta09 Ta10<br>Ta31 Ta32 Ta33 Ta34 Ta35 Ta36 Ta37 Ta38 Ta39 Ta40<br>Ta11 Ta12 Ta13 Ta14 Ta15 Ta16 Ta17 Ta18 Ta19 Ta20<br>Ta41 Ta42 Ta43 Ta44 Ta45 Ta46 Ta47 Ta48 Ta49 Ta50<br>Ta51 Ta52 Ta53 Ta54 Ta55 Ta56 Ta57 Ta58 Ta59 Ta60<br>Dmu01 Dmu02 Dmu03 Dmu04 Dmu05 Dmu41 Dmu42 Dmu43 Dmu44 Dmu45<br>Ta63 Ta64 Ta65 Ta66 Ta68<br>Dmu06 Dmu07 Dmu08 Dmu09 Dmu10 Dmu46 Dmu47 Dmu48 Dmu49 Dmu50<br>Gap Percentage (%)<br>Gap Percentage (%)<br>Gap Percentage (%)<br>Gap Percentage (%)<br>Gap Percentage (%)<br>Gap Percentage (%)<br>Gap Percentage (%)<br>Gap Percentage (%)<br>Gap Percentage (%)<br><!-- End of picture text -->

centages ranging between 50% and 70%. However, these heuristics are still outclassed by the machine learning-based approaches, likely due to their myopic decision-making, which does not factor in longer-term scheduling impacts. For additional detailed makspan ad gap of each instance. 

_Figure 1._ Comparison of different methods on TAI(Taillard, 1993)Taillard, 1993), 1993) 1993)) benchmark. 

_Figure 3._ Comparison of different methods on TAI(Taillard, 1993) benchmark. 

_Figure 2._ Comparison of different methods on DMU(Demirkol et al., 1998) benchmark. 

# **8. Conclusion** 

We introduce Starjob, the first ever supervised dataset for training LLMs on JSSP. Our goal was to demonstrate that even with a limited setup—using a single A6000 GPU, a 

compact Llama 8B model, 4-bit quantisation (insetead of 32bit full precision), and the lightweight RsLoRA fine-tuning method (which updates only a subset of parameters)—LLMs can effectively tackle complex scheduling problems like JSSP. Benchmark tests (Taillard, 1993), (Demirkol et al., 

7 

**Starjob: Dataset for LLM-Driven Job Shop Scheduling** 

_Table 1._ Comparison of different methods on the **TAI** dataset. Lower values indicate schedules closer to the optimal solution, representing better performance. 

|Method|15x15|20x15|20x20|30x15|30x20|50x15|50x20|Average|
|---|---|---|---|---|---|---|---|---|
|FDD/WKR|47.45|50.57|47.57|45.01|56.30|37.72|42.80|46.77|
|MOPNR|44.98|47.97|43.68|45.59|48.23|31.25|39.24|42.99|
|MWKR|56.74|60.65|55.60|52.61|63.93|41.90|55.62|55.29|
|SPT|54.64|65.24|64.11|61.61|66.03|51.37|61.00|60.57|
|L2D|25.95|30.03|31.60|33.02|33.62|26.15|26.40|29.54|
|LLM-FT-Ours|**19.34***|**18.00***|**21.11***|**21.44***|**30.05***|**17.57***|**24.32***|**21.69***|



_Table 2._ Comparison of different methods on the **DMU** dataset. Lower values indicate schedules closer to the optimal solution, representing better performance. 

|Method|20x15|20x20|30x15|30x20|40x15|40x20|50x15|Average|
|---|---|---|---|---|---|---|---|---|
|FDD/WKR|53.58|52.51|54.12|60.08|50.76|55.52|37.58|52.02|
|MOPNR|49.17|45.18|47.14|51.97|43.23|49.22|31.73|45.38|
|MWKR|62.14|58.16|60.96|63.15|52.40|61.09|43.23|57.30|
|SPT|64.12|64.55|62.57|65.92|55.89|62.99|47.83|60.55|
|L2D|38.95|37.74|41.86|39.48|36.68|41.18|26.60|37.50|
|LLM-FT-Ours|**19.90***|**22.26***|**22.11***|**24.82***|**18.44***|**30.61***|**16.85***|**22.14***|



1998) show that, despite these constraints, fine-tuned Llama surpasses classic and neural network methods. This work underscores the potential of LLMs in JSSP, even under resource-efficient conditions. LLMs enable interactive exploration of the JSSP, allowing users to identify constraints that hinder optimal solutions. 

# **9. Limitations and Future Work** 

By introducing the Starjob dataset and applying LLMs, we establish a foundation for future research. Advanced sampling methods like Monte Carlo, diverse LLM architectures, fine-tuning, and integration with reinforcement learning and graph neural networks could enhance performance. Our study demonstrates the potential of LLMs for JSSP, highlighting a promising direction for future research. 

# **References** 

- Ahn, J., Verma, R., Lou, R., Liu, D., Zhang, R., and Yin, W. Large language models for mathematical reasoning: Progresses and challenges. In Falk, N., Papi, S., and Zhang, M. (eds.), _Proceedings of the 18th Conference of the European Chapter of the Association for Computational Linguistics: Student Research Workshop_ , pp. 225–237, St. Julian’s, Malta, March 2024. Association for Computational Linguistics. URL https: //aclanthology.org/2024.eacl-srw.17. 

- AI, M. Llama 3 model card, 2024. URL https://github.com/meta-llama/llama3/ blob/main/MODEL_CARD.md. Accessed: 2024-0810. 

- Beck, J. C., Feng, T. K., and Watson, J.-P. Combining constraint programming and local search for job-shop scheduling. _INFORMS Journal on Computing_ , 23(1): 1–14, 2010. 

- Bonetta, G., Zago, D., Cancelliere, R., and Grosso, A. Job shop scheduling via deep reinforcement learning: a sequence to sequence approach. _Not Specified_ , Aug 2023. 

- Cebi, C., Atac, E., and Sahingoz, O. K. Job shop scheduling problem and solution algorithms: A review. In _2020 11th International Conference on Computing, Communication and Networking Technologies (ICCCNT)_ , pp. 1–7, 2020. doi: 10.1109/ICCCNT49239.2020.9225581. 

- Chaudhry, S. A. and Khan, S. Comparison of dispatching rules in job-shop scheduling problem using simulation: A case study. _ResearchGate_ , 2015. URL https: //www.researchgate.net/publication/ 283505822_Comparison_of_dispatching_ rules_in_job-shop_Schedulingproblem_ Usingsimulation_A_case_study. 

- Chen, W., Ma, X., Wang, X., and Cohen, W. W. Program of thoughts prompting: Disentangling computation 

8 

**Starjob: Dataset for LLM-Driven Job Shop Scheduling** 



<!-- Start of picture text -->
Gap for J=30.0, M=15.0<br>70<br>60<br>50<br>40<br>30<br>20<br>Instance<br>Gap for J=30.0, M=20.0<br>80<br>70<br>60<br>50<br>40<br>30<br>20<br>Instance<br>Gap for J=40.0, M=15.0<br>70<br>60<br>50<br>40<br>30<br>20<br>10<br>Instance<br>Gap for J=40.0, M=20.0<br>80<br>70<br>60<br>50<br>40<br>30<br>20<br>Instance<br>Gap for J=50.0, M=15.0<br>60<br>50<br>40<br>30<br>20<br>10<br>Instance<br>Methods<br>SPT<br>MWKR<br>FDD/WKR<br>MOPNR<br>L2D<br>LLM-FT-Ours<br>Dmu11 Dmu12 Dmu13 Dmu14 Dmu15 Dmu51 Dmu52 Dmu53 Dmu54 Dmu55<br>Dmu16 Dmu17 Dmu18 Dmu19 Dmu20 Dmu56 Dmu57 Dmu58 Dmu59 Dmu60<br>Dmu21 Dmu22 Dmu23 Dmu24 Dmu25 Dmu61 Dmu62 Dmu64 Dmu65<br>Dmu26 Dmu27 Dmu28 Dmu29 Dmu30 Dmu66 Dmu67 Dmu68 Dmu69 Dmu70<br>Dmu31 Dmu32 Dmu33 Dmu34 Dmu35 Dmu73<br>Gap Percentage (%)<br>Gap Percentage (%)<br>Gap Percentage (%)<br>Gap Percentage (%)<br>Gap Percentage (%)<br><!-- End of picture text -->

_Figure 4._ Comparison of different methods on DMU(Demirkol et al., 1998) benchmark. 

- Chen, Z., Mao, H., Li, H., Jin, W., Wen, H., Wei, X., Wang, S., Yin, D., Fan, W., Liu, H., and Tang, J. Exploring the potential of large language models (llms) in learning on graphs, 2024a. 

- Chen, Z., Mao, H., Li, H., Jin, W., Wen, H., Wei, X., Wang, S., Yin, D., Fan, W., Liu, H., and Tang, J. Exploring the potential of large language models (llms) in learning on graphs, 2024b. URL https://arxiv.org/abs/ 2307.03393. 

- Corsini, A., Porrello, A., Calderara, S., and Dell’Amico, M. Self-labeling the job shop scheduling problem. In _Self-Labeling the Job Shop Scheduling Problem_ . Arxiv, 2024. 

- Dai, X. Gpu-benchmarks-on-llm-inference. https://github.com/XiongjieDai/ GPU-Benchmarks-on-LLM-Inference, 2024. 

- Demirkol, E., Mehta, S., and Uzsoy, R. Benchmarks for shop scheduling problems. _European Journal of Operational Research_ , 109(1):137–141, 1998. 

- Frieder, S., Berner, J., Petersen, P., and Lukasiewicz, T. Large language models for mathematicians, 2024. 

- Garey, M. R., Johnson, D. S., and Sethi, R. The complexity of flowshop and jobshop scheduling. _Mathematics of Operations Research_ , 1(2):117–129, 1976. 

- Gerganov, G. llama.cpp: Llm inference in c/c++. https: //github.com/ggerganov/llama.cpp, 2023. 

- Hu, E. J., yelong shen, Wallis, P., Allen-Zhu, Z., Li, Y., Wang, S., Wang, L., and Chen, W. LoRA: Low-rank adaptation of large language models. In _International Conference on Learning Representations_ , 2022. URL https: //openreview.net/forum?id=nZeVKeeFYf9. 

- Huang, W., Abbeel, P., Pathak, D., and Mordatch, I. Language models as zero-shot planners: Extracting actionable knowledge for embodied agents. In _Proceedings of the International Conference on Machine Learning_ . PMLR, 2022. 

- Kalajdzievski, D. A rank stabilization scaling factor for fine-tuning with lora, 2023. URL https://arxiv. org/abs/2312.03732. 

- Nowicki, E. and Smutnicki, C. An advanced tabu search algorithm for the job shop problem. _Journal of Scheduling_ , 8(2):145–159, 2005. doi: 10.1007/s10951-005-6364-5. 

from reasoning for numerical reasoning tasks. _Transactions on Machine Learning Research_ , 2023. ISSN 28358856. URL https://openreview.net/forum? id=YfZ4ZPt8zd. 

- Schulman, J., Wolski, F., Dhariwal, P., Radford, A., and Klimov, O. Proximal policy optimization algorithms. arXiv preprint arXiv:1707.06347, 2017. 

9 

**Starjob: Dataset for LLM-Driven Job Shop Scheduling** 

- Taillard, E. Benchmarks for basic scheduling problems. _European Journal of Operational Research_ , 64(2):278– 285, 1993. 

- Valmeekam, K., Olmo, A., Sreedharan, S., and Kambhampati, S. Large language models still can’t plan: A benchmark for llms on planning and reasoning about change. In _NeurIPS 2022 Foundation Models for Decision Making Workshop_ , 2022. URL https://openreview. net/forum?id=wUU-7XTL5XO. 

- Wei, J., Wang, X., Schuurmans, D., Bosma, M., Ichter, B., Xia, F., Chi, E. H., Le, Q. V., and Zhou, D. Chain-ofthought prompting elicits reasoning in large language models. _Google Research, Brain Team_ , 2022. 

- Yang, C., Wang, X., Lu, Y., Liu, H., Le, Q. V., Zhou, D., and Chen, X. Large language models as optimizers. _arXiv preprint arXiv:2309.03409_ , 2023. 

- Zahmani, M. H., Atmani, B., Bekrar, A., and Aissani, N. Multiple priority dispatching rules for the job shop scheduling problem. In _3rd International Conference on Control, Engineering Information Technology (CEIT’2015)_ , Tlemcen, Algeria, 2015. doi: 10.1109/ CEIT.2015.7232991. 

- Zhang, C., Song, W., Cao, Z., Zhang, J., Tan, P. S., and Xu, C. Learning to dispatch for job shop scheduling via deep reinforcement learning. In _34th Conference on Neural Information Processing Systems (NeurIPS)_ , 2020. 

- Zhao, J., Zhuo, L., Shen, Y., Qu, M., Liu, K., Bronstein, M. M., Zhu, Z., and Tang, J. Graphtext: Graph learning in text space, 2024. URL https://openreview. net/forum?id=dbcWzalk6G. 

10 

