# ReflecSched: Solving Dynamic Flexible Job-Shop Scheduling via LLM-Powered Hierarchical Reflection 

Shijie Cao<sup>a</sup> , Yuan Yuan<sup>a,b,c,d,∗</sup> 

_aSchool of Computer Science and Engineering, Beihang University, Beijing 100191, China bQingdao Research Institute cHangzhou Innovation Institute dZhongguancun Laboratory_ 

## **Abstract** 

The NP-hard Dynamic Flexible Job-Shop Scheduling (DFJSP) problem involves real-time events and complex routing. While traditional rules are efficient but rigid, deep learning is opaque and requires feature engineering. Large Language Models (LLMs) promise adaptive reasoning without this engineering overhead, yet we find their direct application is suboptimal. Baseline LLMs suffer from three key pitfalls: the long-context paradox, where crucial data is underutilized; an underutilization of expert heuristics; and myopic decision-making. To address this, we propose ReflecSched, a framework that empowers the LLM beyond a direct scheduler by equipping it with a strategic analysis capability. ReflecSched tasks the LLM to analyze heuristic-driven simulations across multiple planning horizons and distill them into a concise, natural-language summary termed “Strategic Experience”. This summary is then integrated into the prompt of a final decision-making module, guiding it to produce non-myopic actions. Experiments demonstrate ReflecSched achieves superior performance, with its best variants attaining an average RPD of 6.09% and rank of 4.39 on GEN-Bench, significantly outperforming strong traditional and learning-based methods including HMPSAC and IDDQN. Extensive cross-benchmark evaluations on MK-Bench and the semiconductor-focused JMS-Bench further confirm the framework’s robustness, yielding minimum average RPDs of 6.83% and 6.18%, respectively. It also statistically and decisively surpasses direct LLM baselines, securing a 71.35% Win Rate while being, on average, 15.1% more token-efficient on Normal-scale problems. Furthermore, cumulative runtime analysis reveals that ReflecSched’s zero-shot nature eliminates the training bottleneck, providing a decisive efficiency advantage in highvariability manufacturing environments. Ablation studies attribute this performance to a robust reflection mechanism that leverages high-quality, contrastive experience. This mechanism mitigates key LLM pitfalls like myopic greed, enabling ReflecSched to outperform all evaluated heuristics. Ultimately, the framework’s performance is statistically on par with an oracle-like strategy, showcasing its effectiveness and robustness. 

_Keywords:_ Dynamic Flexible Job-Shop Scheduling, Large Language Models, Hierarchical Reflection, Deep Reinforcement Learning, LLM-based Planning 

## **1. Introduction** 

Dynamic Flexible Job-Shop Scheduling (DFJSP) is a long-standing challenge in operations research and a key component of modern smart manufacturing [1]. As an NP-hard problem, it involves the complex task of continuously allocating operations to machines in a real-time environment characterized by stochastic 

∗Corresponding author 

_Email addresses:_ cls1277@buaa.edu.cn (Shijie Cao), yuan21@buaa.edu.cn (Yuan Yuan) 

events such as new job arrivals or machine breakdowns. The ability to efficiently schedule these operations critically impacts the agility, resilience, and profitability of production systems. For decades, the field has been dominated by methods ranging from classical heuristics to meta-heuristics [2]. While foundational, these approaches often rely on handcrafted rules that can struggle to generalize across diverse and unforeseen dynamic scenarios [3]. 

In recent years, deep learning (DL), particularly reinforcement learning (RL), has emerged as a promis- 

ing paradigm for this problem [4]. By training agents on simulated data, DL-based methods can learn sophisticated, state-aware scheduling policies. However, this capability comes at a significant cost. A key limitation lies in the intricate process of state and action space engineering: translating the rich state of a dynamic workshop into a fixed-size numerical vector that a neural network can process is a complex task requiring dual expertise in scheduling and machine learning [5]. Furthermore, the resulting models are often “black boxes” with opaque decision-making logic that is difficult for engineers to interpret or trust in high-stakes environments [6]. 

The advent of Large Language Models (LLMs) offers a different approach, potentially circumventing these challenges by leveraging natural language as a more accessible interface. An LLM-based scheduler could, in principle, reason directly over a textual description of the factory state, reducing the need for complex numerical encoding [7]. This suggests the possibility of developing and adapting scheduling strategies with greater flexibility. 

However, our work finds that a direct application of LLMs to DFJSP leads to consistently suboptimal performance. We argue that the standard autoregressive generation process is not inherently well-suited for the strategic, lookahead-dependent reasoning that scheduling demands. Through a motivational analysis, we identify and empirically validate three key pitfalls of this direct approach: 

- **The Long-Context Paradox** : Foundational static information, such as machine processing times and job structures, is often underutilized by the model as the prompt length increases. 

- **Underutilization of Heuristics** : LLMs exhibit difficulty in reliably applying expert-provided procedural knowledge, such as Priority Dispatching Rules (PDRs), often allowing their generalized pre-trained behaviors to override explicit guidance. 

- **Myopic Greed** : The lack of a structured planning mechanism creates a strong tendency towards locally optimal but globally inefficient decisions, which can lead to downstream bottlenecks. 

To address these shortcomings, we introduce ReflecSched, a framework that fundamentally restructures the LLM’s role in the scheduling process. Rather than acting as a purely reactive decision-maker, the LLM also serves as a strategic analyst within a planning loop that 

decouples long-horizon reasoning from immediate execution. At its core, ReflecSched’s Hierarchical Reflection module performs multi-level, heuristic-driven simulations of future trajectories. It then tasks the LLM to reflect upon these simulations and distill them into a concise, actionable “Strategic Experience.” This experience, generated only at critical, event-driven moments, subsequently guides a lean, fast ExperienceGuided Decision-Making module to produce a highquality, non-myopic action. 

Our contributions are threefold: 

- **A rigorous empirical diagnosis of LLM-based schedulers.** We are the first to systematically identify and validate three fundamental failure modes of LLMs in the complex DFJSP domain: the longcontext paradox, heuristic underutilization, and myopic greed. This analysis provides crucial insights for the broader field of LLM-based planning. 

- **A novel LLM-based scheduling paradigm, ReflecSched.** We propose a framework that recasts the LLM from a reactive decision-maker into a strategic analyst. By decoupling long-horizon planning from immediate execution via a hierarchical reflection mechanism, ReflecSched is designed to mitigate the identified pitfalls. 

- **Multi-tiered benchmark suites and open-source ecosystem.** We introduce a comprehensive benchmarking ecosystem comprising GEN-Bench, MKBench, and JMS-Bench. These suites span from general-purpose scenarios to standardized flexible job-shop instances and high-fidelity semiconductor manufacturing environments. By opensourcing these benchmarks alongside the ReflecSched framework, we provide a rigorous, multidimensional evaluation protocol to facilitate future research in LLM-based industrial planning. 

## **2. Related Work** 

**Heuristic and Metaheuristic Approaches:** Heuristic-based methods are a foundational approach for the Dynamic Job-Shop Scheduling Problem (DJSP) due to their computational tractability. Research has advanced from simple dispatching rules to complex metaheuristics designed to handle diverse operational constraints. For instance, some works have applied greedy randomized adaptive search algorithms to manage a wide array of dynamic events [8], while others have used hybrid Particle Swarm Optimization for joint production and transportation scheduling [9]. 

2 

Further research has focused on specific uncertainties, such as variable processing times, using techniques like Artificial Bee Colony algorithms [10]. To align with the human-centric paradigm of Industry 5.0, recent research has formalized the HDDFJSP by integrating worker-related dynamic factors into a multi-objective optimization framework, leveraging a Q-learningenhanced differential evolution algorithm to balance production efficiency with operator well-being [11]. A key limitation of these metaheuristics, however, is their reliance on a pre-defined search logic that is inherently less adaptive and struggles to generalize to new, unseen problem scenarios [12]. 

**Deep Reinforcement Learning Approaches:** To address the generalization limitations of heuristics, Deep Reinforcement Learning (DRL) has emerged as an alternative that learns adaptive policies, typically by formulating the DJSP as a Markov Decision Process. Architectural innovations have been central to this area. For example, Pointer Networks have been utilized for endto-end policy learning that avoids reliance on predefined rules [13]. To enhance scalability, a multi-agent perspective has been adopted through decentralized frameworks [14]. Other approaches decompose the decisionmaking process using hierarchical structures [15]. Recently, to enhance the adaptability of dynamic jobshop scheduling, Yu et al. introduced a DRL-based framework that reformulates scheduling states as multichannel images, leveraging a Spatial Pyramid Pooling Fast module to achieve scale-independent feature extraction and a region-based dense reward function to facilitate fine-grained policy optimization [16]. Nevertheless, DRL presents its own significant challenges: performance is highly sensitive to the complex engineering of state and reward functions; the resulting policies are often opaque “black boxes” hindering trust; and they demand accurate simulation environments for training, which are often unavailable for complex real-world systems. 

**Large Language Models Paradigms:** Seeking to address the challenges of both handcrafted logic and the black-box nature of DRL, LLMs have recently introduced a new paradigm for scheduling by leveraging their vast pre-existing knowledge and reasoning capabilities. One direction explores LLMs as end-to-end solvers by fine-tuning them on large-scale datasets of problems paired with their solutions [17, 7]. Another approach employs LLMs as automated problem modelers that translate natural language into executable code for traditional solvers [18, 19]. A third direction positions the LLM as a hyper-heuristic generator that iteratively reflects upon and improves heuristic rule-code [20]. De- 

spite their potential, early works reveal critical challenges: the risk of generating infeasible solutions (“hallucinations”), high computational costs, and a primary focus on static problems, leaving their application to complex, dynamic scheduling environments largely unexploredc. 

**Hierarchical Memory and Reasoning Paradigms:** A significant body of work explores hierarchical paradigms to structure and access information beyond the fixed context window. A prominent direction involves creating hierarchical memory systems, such as MemGPT’s OS-inspired information paging [21] or the semantic-level memory structures in MemoryBank and H-MEM that enable targeted retrieval [22, 23]. A related approach, seen in HIAGENT, employs hierarchy for task decomposition to manage an agent’s working memory during long-horizon tasks [24]. Diverging from these methods, which primarily focus on organizing and retrieving an agent’s past, our proposed ReflecSched framework introduces a hierarchical reflection mechanism that functions as a dynamic, planning-time operator. Instead of retrieving historical data, it prospectively explores the future by leveraging multi-level, heuristicdriven simulations to analyze potential decision pathways. The hierarchy in ReflecSched is thus one of planning abstraction distilling numerical simulations into a transient, textual Strategic Experience to guide the next action, rather than creating a persistent memory store. 

## **3. Preliminaries** 

## _3.1. Dynamic Flexible Job-Shop Scheduling_ 

DFJSP is the problem of assigning operations from multiple jobs to a set of machines, subject to real-time stochastic events. It is characterized by two features: flexibility, which allows each operation to be processed on a subset of candidate machines, and dynamism, which refers to the occurrence of real-time stochastic events such as new job arrivals or machine breakdowns. The objective is to generate a valid schedule that minimizes the makespan, defined as the maximum completion time among all jobs [25]. Figure 1 illustrates an example of such a schedule, visualized as a Gantt chart. A valid schedule must satisfy both precedence constraints between operations of the same job and the resource constraints of the machines. 

In this work, we model a rich set of dynamic events to capture the stochastic nature of modern manufacturing environments. These include new job arrivals, machine breakdowns and subsequent repairs, job cancellations, and the introduction of high-priority emergency 

3 

jobs. This set of events is representative of the primary disruptions studied in the DFJSP literature [26, 6, 27]. More importantly, the core architecture of ReflecSched is designed to be event-agnostic and generalizable. Its strategic Hierarchical Reflection module is invoked by an event-driven trigger, which responds to any significant state change rather than to a specific event type. Consequently, the framework can be readily extended to handle other stochastic events, such as variable processing times [10] or rush order arrivals [28], without requiring modifications to its fundamental logic. 

Table 1: Notation for the DFJSP Mathematical Formulation 

|**Symbol**|**Description**|
|---|---|
|**_Sets and_**|**_Indices_**|
|_t_|Discrete decision step index,_t_=0,1,2, ...|
|τ|Continuous physical time index,τ∈[0,∞).|
|J|Set of active jobs currently in the system,<br>{1, ...,_n_}.|
|M|Set of available machines,{1, ...,_m_}.|
|O|Set of all operations to be scheduled.|
|O_i_|Set of operations for job _Ji_ ∈J.|
|M_i j_|Set of candidate machines for operation_Oi j_.|
|O_int_|Set of interrupted operations awaiting ma-<br>chine repair.|
|**_Paramete_**|**_rs and Constants_**|
|_ni_|Number of operations for job _Ji_.|
|_pi jk_|Processing time of_Oij_on machine_k_∈M_i j_.|
|_ai_|Arrival time of job _Ji_.|
|_Mbig_|A sufficiently large positive number (a “Big-<br>M” constant).|
|**_Decision_**|**_Variables_**|
|_xi jk_|Binary: 1 if_Oij_is assigned to machine_k_.|
|_yij_,_i_<sup>′</sup>_j_<sup>′</sup>_k_|Binary: 1 if operation _Oij_ precedes _Oi_<sup>′</sup>_j_<sup>′</sup><br>when both are assigned to machine_k_.|
|**_Auxiliary_**|**_and State Variables_**|
|_sij_|Start time of operation_Oij_.|
|_cij_|Completion time of operation_Oij_.|
|_rk_|Earliest time machine_k_becomes free.|
|_Cmax_|The makespan, defined asmax_Ji_∈J{_ci_,_ni_}.|



## _3.2. Mathematical Formulation of the DFJSP_ 

The notation used throughout is summarized in Table 1. 

## _3.2.1. Model Assumptions_ 

To ensure clarity and specify the applicable scope of the proposed mathematical model, we explicitly state 



<!-- Start of picture text -->
Machine<br>M3 O 1 , 1 O 1 , 2 O 3 , 2<br>M2 O 2 , 1 O 2 , 2 O 2 , 3 O 1 , 3<br>M1 O 3 , 1 O 2 , 4<br>0 1 2 3 4 5 6 7 8 Time<br>Machine<br>M3 O 1 , 2 O 3 , 2<br>M2 O 1 , 1 O 2 , 2 O 1 , 3<br>M1 O 2 , 1 O 3 , 1 O 2 , 3 O 2 , 4<br>0 1 2 3 4 5 6 7 8 Time<br><!-- End of picture text -->

Figure 1: An example of two valid schedules for the same problem instance. The Gantt charts illustrate how a locally optimal choice at an early stage can lead to a suboptimal final makespan (top, 7.51), whereas a more globally-aware decision sequence yields a better outcome (bottom, 6.51). 

the following assumptions regarding the DFJSP environment [29]. These assumptions define the boundaries of resource constraints, temporal dynamics, and event handling logic: 

To define the operational scope of the proposed mathematical model, we stipulate the following assumptions regarding the DFJSP environment [30]. These assumptions delineate the parameters of resource constraints, temporal dynamics, and the logic governing dynamic events: 

**Resource and Task Constraints:** Each job follows a predefined sequence of operations, with each operation occupying a single machine at any given time. Machines constitute the primary capacity constraints and are assumed to have infinite buffer capacity. Auxiliary resources, such as operators and tools, are considered non-constraining and remain readily available. 

**Temporal Specifications:** Setup times are assumed to be sequence-independent and are incorporated into the operation processing times. Similarly, inter-machine transfer times are considered negligible or are subsumed under the processing durations. All processing times are deterministic and remain invariant throughout the execution of an operation. 

**Dynamic Event Logic:** The scheduler operates in an online environment where the timing and characteristics of stochastic events, such as job arrivals and machine breakdowns, are unknown a priori. Operations are nonpreemptive except when interrupted by equipment failures. In such instances, we assume a preempt-resume logic: the accumulated processing progress is preserved, 

4 

and the operation resumes as soon as the machine becomes available again. 

## _3.2.2. Objective Function and Constraints_ 

The primary objective is to minimize the makespan ( _Cmax_ ), which is defined as the maximum completion time among all jobs. 



subject to: 



The schedule must satisfy the following constraints: 

**Processing Time:** The completion time of an operation is determined by its start time and the processing time on its assigned machine. 



**Assignment:** Each operation must be assigned to exactly one of its candidate machines. 



**Job Arrival:** An operation cannot start before its corresponding job has arrived. 



**Precedence:** Within each job, operations must be performed in their specified sequence. 



**Machine Capacity:** For any two distinct operations, if they are assigned to the same machine, they cannot be processed simultaneously. This is enforced by the following disjunctive constraints for any pair of operations ( _Oij_ , _Oi_<sup>′</sup> _j_<sup>′</sup> ) where _i_ � _i_<sup>′</sup> or _j_ � _j_<sup>′</sup> , and for each machine _k_ ∈ _Mij_ ∩ _Mi_<sup>′</sup> _j_<sup>′</sup> : 





_3.2.3. Formalization of Dynamic Events_ 

The state of the system at time τ is defined by the tuple _S_ τ = (Jτ, { _ai_ }, { _rk_ }, O _int_ ). A dynamic event occurring at time τ triggers an instantaneous state transition from _S_ τ to _S_ τ<sup>+</sup> , where τ<sup>+</sup> denotes the time immediately following the event execution. The specific update logic for each event type is formalized below [8]. 

**Job Arrival:** At physical time τ = τ _new_ , a new job _Jnew_ with its own set of operations O _new_ is introduced into the system [31]. The state is updated instantaneously as follows: 





The emergency status of a job is a characteristic handled by the scheduling policy via prioritization rather than being a direct modification to the model’s constraints. 

**Job Cancellation:** At physical time τ = τ _cancel_ , a job _Jcancel_ is removed from the system. This action removes the job from the set of active jobs J and all of its corresponding uncompleted operations from the set of operations to be scheduled O _cancel_ . The historical record of any completed operations of _Jcancel_ is preserved, but they are no longer relevant for future scheduling decisions. 

The state update is formalized as: 





If an operation from O _cancel_ was in process on a machine _k_ at τ, it is preempted. The machine is immediately freed, and its availability time _rk_ is updated to τ. 

**Machine Breakdown:** At physical time τ = τ _break_ , a machine _k_ ∈M fails and becomes unavailable [32]. The immediate consequence is that the machine’s earliest availability time is postponed until its projected repair time, τ _repair_ . This is formalized as: 



This update affects all subsequent scheduling decisions, as no new operations can be assigned to machine _k_ until τ _repair_ . 

If an operation _Oi j_ was being processed on machine _k_ at this time i.e., _si j_ < τ _break_ < _ci j_ , it is immediately interrupted. The operation is formally moved to a set of interrupted operations, O _int_ , to signify its special status. It retains its assignment to machine _k_ and awaits the machine’s repair to resume processing. 

**Machine Repair:** At physical time τ = τ _repair_ , machine _k_ becomes operational again. Any operation _Oi j_ ∈ O _int_ that was interrupted on this machine can now resume. Upon repair, _Oi j_ is removed from the set O _int_ . 

The resumption of its processing leads to a new, postponed completion time, _c_<sup>′</sup> _i j_<sup>. While the intrinsic process-</sup> ing time _pi jk_ remains unchanged, the new completion time is calculated based on the remaining work: 



5 

where τ _break_ − _sij_ represents the processing work completed before the interruption. This new completion time _c_<sup>′</sup> _ij_<sup>subsequentlyservesasthebasisforre-</sup> evaluating the precedence constraints for all downstream operations of job _Ji_ . The machine _k_ is also now available for scheduling other operations from time τ _repair_ onwards. 

## _3.3. Industrial Application of Semiconductor Cluster Tool Scheduling_ 

The DFJSP framework investigated in this study is motivated by the operational management of cluster tools within semiconductor wafer fabrication facilities. As illustrated in Figure 2, a cluster tool is a representative manufacturing unit comprising several heterogeneous processing chambers, denoted as PM1 through PM5, which surround a central multi-link handling robot [33]. Wafers enter the system through load lock interfaces, after which the robot executes the sequence of transport steps required to move them between specific modules. These chambers perform high-precision processes, such as chemical vapor deposition or reactive ion etching, where scheduling complexity is dictated by a set of technological constraints that transcend traditional job-shop models. 

Machine eligibility is determined by wafer recipes, as only a specific subset of process modules is configured with the gas chemistry, RF power, or thermal settings required for a given technological step [34]. Furthermore, re-entrant flow patterns are prevalent in this environment; wafers must frequently revisit modules such as PM2 or PM3 to undergo multi-layer processing at various stages of the production cycle. Yield management introduces a third critical constraint: residency time limits. These constraints mandate that the handling robot extracts wafers from a chamber immediately upon processing completion, as prolonged exposure to the chamber environment renders the wafer surface vulnerable to oxidation or chemical contamination. Consequently, the scheduler must precisely synchronize robot transport with chamber cycle times to mitigate defects induced by processing delays. 

The operational dynamism of this fabrication environment is further characterized by frequent perturbations that necessitate the real-time reconfiguration of pre-planned schedules. These disturbances encompass the stochastic arrival of high-priority “hot lots” requiring immediate prioritization to satisfy stringent delivery constraints, equipment failures resulting from parameter drifts, and job cancellations triggered by upstream quality excursions. When a processing module becomes unavailable, the system must autonomously identify alter- 

native routings through compatible modules to ensure production continuity. Addressing these challenges requires a scheduling framework capable of non-myopic reasoning to optimize throughput while adhering to the physical constraints of the equipment. Consequently, the coordination of semiconductor cluster tools provides a compelling case for the proposed hierarchical reflection mechanism, as it offers a structured paradigm for balancing transient efficiency with long-term schedule robustness [35]. 



<!-- Start of picture text -->
Process<br>Module 3<br>Process Process<br>Module 2 Module 4<br>Process Process<br>Module 1 Module 5<br>Transfer<br>Module<br>Wafer cassette<br><!-- End of picture text -->

Figure 2: Architectural schematic of a semiconductor cluster tool utilized in the JMS-Bench dataset. The system integrates five heterogeneous process modules (PM1 to PM5) with a central transfer module and dual-arm robot. Wafers are loaded from cassettes and navigate through multi-stage recipes involving re-entrant flows and strict residency time constraints. 

## _3.4. Baseline LLM-based Scheduler_ 

To evaluate our proposed method, we define a direct baseline, LLM-Direct, which employs the LLM to perform the function of classical dispatching rules. In this approach, a state-aware prompt is constructed at each decision point. The shop-floor state is encoded into the prompt, including both static specifications, such as job structures and machine data, and dynamic information, such as the set of currently available actions and current machine statuses. The action selected by the LLM is then executed in a shop-floor simulator, advancing the system state to the next decision point. Further implementation details for LLM-Direct are presented in Appendix A. 

## **4. Motivational Analysis** 

## _4.1. The Long-Context Paradox_ 

While replacing state engineering with a single LLM prompt is appealing, it creates an information utility paradox: encoding the high-dimensional shop-floor 

6 

state into a dense, verbose prompt leads to underutilization of the provided data [36]. We observe this is not merely a context-length issue but a fundamental challenge in reasoning over such textual complexity [37], as exemplified by our case study with smaller models in Appendix B. 

To validate this hypothesis, we conducted a targeted experiment by omitting the static information block from the LLM-Direct baseline’s prompt. As shown in Figure 3, this omission had a negligible impact on performance, even though the static block constitutes over 70% of the prompt. The median makespan ratio between the conditions (with vs. without static data) is nearly 1.0, providing strong evidence that the model largely ignores this information and fails to ground its decisions in the provided specifications. To test this hypothesis, we conducted experiments across a broad spectrum of model scales, ranging from the Qwen series (0.6B, 8B, and 32B) [38] to the frontier-scale DeepSeek-V3.2 (685B) [39]. Specifically, we systematically excluded the static information block from the LLM-Direct baseline’s prompt to evaluate whether increasing model capacity can compensate for the absence of explicit structural constraints. 

As shown in Figure 3, this omission had a negligible impact on performance across all tested scales, even though the static block constitutes over 70% of the prompt. The experimental results reveal that the median makespan ratio between the two conditions (with vs. without static data) approaches unity, even for the 685B parameter model. This suggests that the models, irrespective of parameter scale, exhibit a notable insensitivity to this information and demonstrate a limited capacity to ground their decisions in the provided specifications. 

The systemic neglect of context is further evidenced by the localized semantic errors analyzed in Appendix Appendix B.2. These instances reveal that the model often fails to incorporate critical state descriptors despite their explicit inclusion in the prompt. Such findings indicate that the primary obstacle is not a lack of descriptive clarity but rather a fundamental deficiency in semantic grounding when processing high-density context. Attempting to rectify these errors by further refining the prompt only serves to exacerbate the longcontext paradox. Specifically, increasing the granularity of descriptions to ensure information capture inevitably expands the total prompt volume. As demonstrated by our scaling analysis, this expansion leads to the attenuation of information saliency and ultimately reinforces the model’s reliance on parametric priors over the provided task-specific instructions. 



<!-- Start of picture text -->
Static Data Dynamic State & Task<br>1400 1.2<br>1200 1.1<br>1000 Q3: 1.043 Q3: 1.057<br>1.0 Median:  1.008 Median: 1.000<br>800 Q1: 0.952 Q1: 0.958<br>910<br>600 (72.7%) 0.9<br>400<br>0.8<br>200 (27.3%) 342 342<br>0 With Static DataWithout Static Data 0.7 Normal Small<br>(a) Prompt Composition (b) Performance Impact<br>0.986 1.003 1.024 1.003 0.996 1.012 1.011 0.971<br>1.0<br>0.8<br>0.6<br>0.4<br>0.2 Scale<br>Normal<br>Small<br>0.0<br>(c) Cross-model Scaling Analysis<br>deepseek-v3.2 qwen3-0.6b qwen3-32b qwen3-8b<br>Performance Ratio<br>Prompt Length (Number of Tokens) (Makespan without Static / with Static)<br>Makespan (No Static / Static)<br><!-- End of picture text -->

Figure 3: An empirical investigation of the Long-Context Paradox. (a) A breakdown of the prompt composition for the baseline model. (b) Box plots showing the ratio of makespans resulting from running the model with and without the static data portion of the prompt for the primary evaluation model. (c) Comparative scaling analysis of makespan ratios across the Qwen3 series and DeepSeek-v3.2. The consistent alignment of these ratios with unity across a parameter range of 0.6B to 685B indicates that the underutilization of dense static specifications is a systemic reasoning limitation that persists irrespective of model capacity. 

7 

## _4.2. Underutilization of Heuristics_ 

A key challenge in LLM-based scheduling is the effective application of PDRs. While LLMs are generally proficient at following declarative instructions, their capacity to faithfully execute complex, state-dependent procedural rules remains unreliable [40]. To quantify and isolate this competency, we introduced PDR-Bench, a diagnostic benchmark wherein each instance is systematically synthesized to possess a single, ground-truth optimal heuristic, and utilized it within a controlled experiment to evaluate the baseline LLM, the technical specifics of which are elaborated in Appendix Appendix C. 

The “optimal heuristic” for any given instance in PDR-Bench is known by design, as each problem instance is specifically constructed to ensure that one particular heuristic yields a superior outcome over all others. The results presented in Figure 4 reveal the LLM’s significant difficulty in effectively utilizing these heuristics [41]. This finding suggests the model’s limited capacity to translate the strategic guidance of the provided rules into its decision-making. Furthermore, when explicitly instructed to use the single optimal heuristic, the model still failed to match the performance of that heuristic applied in isolation, reverting instead to its generalized, pre-trained behaviors. 



<!-- Start of picture text -->
Prompt Condition<br>LLM-Direct<br>All-PDRs<br>8% 7.6% Single-Best-PDR<br>7.3% ReflecSched<br>6.3% Heuristic-Only Baseline<br>6% 5.7% 5.9%<br>4.7% 4.5%<br>4%<br>2.9%<br>2%<br>0%<br>Qwen3-14B Qwen3-8B<br>Average RPD vs. Best Heuristic<br><!-- End of picture text -->

Figure 4: Analysis of heuristic utilization on the PDR-Bench dataset, with RPD measured against the known optimal heuristic for each instance (0% baseline). The baseline LLM struggles to apply the optimal heuristic even when explicitly prompted, whereas ReflecSched substantially improves performance. 

## _4.3. The Pitfall of Myopic Greed_ 

The autoregressive, token-by-token generation process inherent in LLMs presents a structural mismatch with the strategic, non-local search required for complex scheduling problems. This mismatch predisposes them to myopic decision-making, where locally optimal choices lead to globally suboptimal outcomes. 

To quantify this myopic behavior, we introduce the **Greedy Decision Ratio (GDR)** . 

We formally define the one step greedy action at any decision point _t_ as the one that minimizes the local finish time. Let A( _S_ τ) denote the set of all currently feasible actions at state _S_ τ, where each action **a** ∈A( _S_ τ) represents a valid assignment of a ready operation to an available machine. The greedy action is defined as: 



where τ _start_ ( **a** ) is the earliest start time of an action and _p_ **a** is its processing time. The GDR is then the fraction of decision points where the agent’s chosen action matches **a** _t_ . 

We evaluated baseline LLMs using this metric on GEN-Bench, a benchmark specifically designed to be globally balanced and control for what we term rulebalance bias—a scenario where a dataset might implicitly favor a single, simple heuristic. This curation is critical: on a rule-balanced benchmark, a persistently high GDR (≈80-90%) is a strong indicator of intrinsic myopic decision-making rather than an artifact of the model correctly identifying a simple optimal heuristic for the dataset. The quantitative results presented in Figure 5 reveal that the GDR is indeed persistently high across all tested models, indicating a significant greedy bias [42]. 

A qualitative case study presented in Figure 1 further illustrates the consequences, showing how a single myopic choice can trigger a cascade of downstream inefficiencies. The complete data for this instance is provided in Appendix F. 

Specifically, consider the resource contention at _t_ = 0, where operations _O_ 2,1 and _O_ 3,1 are both available for processing. A myopic scheduling logic typically prioritizes _O_ 3,1 because it exhibits zero machine flexibility, being restricted solely to _M_ 1. This immediate allocation occupies _M_ 1 until _t_ = 1.08. Consequently, when the greedy policy subsequently evaluates _O_ 2,1, it identifies two alternatives: waiting for _M_ 1 to become available at _t_ = 2.67 or utilizing the idle _M_ 2 to complete the operation at _t_ = 2.62. The greedy policy selects _M_ 2 to achieve a marginal local gain of 0.05 time units. This decision is suboptimal as it preemptively occupies _M_ 2 for an extended duration, thereby obstructing the critical path for Job 1’s final operation, _O_ 1,3, which requires _M_ 2 until _t_ = 5.53. In contrast, the strategic policy accounts for this downstream bottleneck. By executing a global trade-off, it reverses the assignment sequence and allocates _O_ 2,1 to _M_ 1 at _t_ = 0. Although this choice introduces a slight delay for _O_ 3,1, it reserves _M_ 2 capacity for 

8 

Job 1. As a result, _O_ 1,3 can commence at _t_ = 3.88, yielding a makespan of 6.51, which is a significant improvement over the 7.51 achieved by the greedy approach. 



<!-- Start of picture text -->
LLM-Direct ReflecSched<br>Small Scale Normal Scale<br>80% 84.8% 81.6% 89.2% 79.2% 83.9% 80.4% 83.2% 75.9% 85.9% 77.4% 83.8% 80.5%<br>60%<br>40%<br>20%<br>0%<br>Qwen3-8B Qwen3-14B Qwen3-32B Qwen3-8B Qwen3-14B Qwen3-32B<br>Average Greedy Decision Ratio (GDR)<br><!-- End of picture text -->

Figure 5: Comparison of the Average Greedy Decision Ratio (GDR) between the LLM-Direct baseline and the ReflecSched framework. Results are presented for different models and are segmented by the Normal and Small problem scales. 

## **5. ReflecSched Framework** 

## _5.1. Framework Overview_ 

To address the identified limitations, we introduce ReflecSched, a novel framework that structurally decouples long-horizon, strategic reasoning from lowlatency, online decision-making via two interconnected, sequential modules (Figure 6) [43]. The first, the Hierarchical Reflection Module, serves as the framework’s strategic planning component. It leverages multi-level, heuristic-driven simulations to explore future state trajectories [44]. It then employs the LLM to analyze these simulated outcomes, distilling them into a concise, actionable Strategic Experience E. This experience then informs the second component, the Experience-Guided Decision-Making Module, which handles real-time execution. Guided by the strategic foresight in E, this module makes a strategically-informed decision based on the immediate environment state. 

This two-stage architecture is designed to address each of the identified challenges: First, by explicitly simulating future consequences, the Hierarchical Reflection Module provides the necessary foresight to counteract myopic greed, shifting the model’s focus from locally optimal choices to globally efficient strategies. Second, the framework directly addresses the underutilization of heuristics by employing PDRs to guide its exploratory rollouts [45]. This ensures that expert procedural knowledge is integrated into the reasoning process. Finally, the framework mitigates the longcontext paradox. By having the Reflection Module distill its findings into a concise Strategic Experience E, the final decision prompt supplied to the LLM contains only 

this high-level guidance and the immediate state [36]. This precludes informational overload and concentrates the model’s reasoning on the most salient data. 

ReflecSched mitigates the inherent opacity of traditional models by formalizing reasoning processes into explicit natural language representations. In contrast to DRL policies, where decision logic is implicitly encoded within high-dimensional parameter spaces, this framework generates intermediate textual artifacts designated as Strategic Experience [27, 46]. These artifacts serve as an interpretable interface between complex simulation states and final scheduling executions. By extracting discriminative features from successful and suboptimal trajectories into explicit heuristics, the framework enables human operators to verify the strategic rationale underlying each decision. Furthermore, the integration of Chain-of-Thought prompting within the decision module facilitates the generation of traceable logical sequences for each assignment [47]. This transparency allows for the identification of potential reasoning failures and enhances operational verifiability, representing a distinct functional departure from purely numerical policies that lack explanatory mechanisms. 

## _5.2. Hierarchical Reflection_ 

Central to ReflecSched is the Hierarchical Reflection module, a mechanism designed to perform strategic evaluation, which is essential for the DFJSP. From a structural perspective, the proposed hierarchy is characterized by an inverse relationship between planning granularity and temporal horizon. Rather than employing a monolithic reasoning architecture, we decompose the reflective process into distinct levels where the analytical focus transitions from long-term strategic objectives to immediate tactical execution. It implements a recursive “Simulate-Reflect-Refine” loop [48]. This iterative process first explores the future through simulation, then reflects on the outcomes to identify key strategic principles, and finally refines these principles into a concise, actionable policy directive [49]. 

The process is a top-down hierarchical simulation from _lmax_ to _l_ = 0, operating as a deterministic projection that assumes no new stochastic events during the lookahead. Central to this simulation is a randomized base policy, π _base_ , which operates by sampling a PDR from a predefined pool at each decision point to select an action. The simulation methodology differs by level to enable multi-timescale exploration. At higher levels ( _l_ > 0), the module performs sparse, long-range exploration with reduced granularity by simulating trajectories where π _base_ is applied at every step to identify global constraints such as future machine contention. In 

9 



<!-- Start of picture text -->
Legend State 𝑆 Hierarchical Reflection Module Hierarchical Reflection ModuleExample Experience-Guided Decision-Making ModuleExample<br>blockblue  (The 'Thinker')Hierarchical Reflection Module  Broad Exploration 𝐿> 0 Next Level  𝐿−1 > 0 Best Path(Makespan: 11.496) You are an expert scheduler in a dynamic factory.<br>green block Decision-Making Module (The 'Actor') (using diverse PDRs) 𝐾 RolloutsStochastic  Task: Reflect & Summarize •• Compare divergent trajectoriesIdentify high-level causal patterns Decision Path: J1O1@M3 -> J2O1@M2 -> ...Worst Path # Experience <key_insights> Prioritize operations on machines with higher contention when<br>• Distill intermediate  (Makespan:  dealing with emergency jobs,<br>orange block Prompt: Structured input for LLM interaction State Info  𝑆 strategic insights 14.41)Decision Path: J1O1@M2 -> J2O1@M1 -> ... ensuring these critical resources are freed early. </key_insights><br>Decision  # Task: Make a Decision<br>purple  Response: Structured  t = Point 𝑇 Focused Exploitation 𝐿= 0 # Output RequirementsProvide your analysis in the  ```json<br>block output for  Task: Analyze & Recommend following XML-style tags. {"job": <int>, "op": <int>,<br>LLM interactionScheduling  Machine StatesReady  ••• Evaluate immediate trade-offsDetermine the locally optimal pathFormulate the final actionable  Systematic Rollout(one per action) ```xml <key_insights> "machine": <int>}```<br>Environment StateHeuristic Rollout /  Operations Experience-Guided Decision-Making Module experience (Your NEW, REFINED, and SYNTHESIZED strategic principle. This is the key output.) </key_insights> ``` Scheduling Job 1 Operation 1 on Machine 11 sooner, optimizing future operations and minimizing would unblock Machine<br>Simulation potential delays.<br>LLM Reasoning Call State Info  𝑆 Query Task: LLM as Operator Final Decision <key_insights> Prioritize operations on  Therefore, the best decision is to schedule Job 1 Operation 1 on<br>Build Experience- • Ground reasoning in  machines with higher contention  Machine 1.<br>Augmented Prompt • Experience Select the best action from  𝐸 when dealing with emergency<br>Robust Final Action Execute & Update • Ready OpsGenerate a single, high-fidelity decision jobs, ensuring these critical resources are freed early. </key_insights> ```json{"job": 1, "op": 1, "machine": 1}```<br>𝐿−1 = 0 Next Level<br>’𝑇 Next Decision Point at t=<br>Experience  E<br><!-- End of picture text -->

Figure 6: The architecture of the ReflecSched framework, designed to decouple strategic planning from immediate execution. The main workflow is initiated at a decision point. The **Hierarchical Reflection Module** (blue) performs multi-level, heuristic-driven simulations to explore future state trajectories. It then leverages an LLM to analyze these outcomes and distill a concise Strategic Experience (E). This experience is passed to the **Experience-Guided Decision-Making Module** (green), which constructs an experience-augmented prompt to guide the LLM in selecting a final, strategically-informed action. The right-hand panels provide concrete examples of the prompts and responses for both the reflection and decision-making stages, illustrating the flow of information from simulation data to strategic guidance, and finally to a specific action. 

contrast, the base level ( _l_ = 0) performs a systematic evaluation of immediate actions to determine the highresolution impact of each candidate within a narrow temporal window. For each available action **a** ∈A( _S_ τ), a short-horizon rollout is initiated by first executing the action _a_ , and then applying π _base_ for all subsequent decisions. 

The outcome of any such rollout is a trajectory ζ<sup>(</sup><sup>_l_)</sup> and its associated cost, defined as the hypothetical partial makespan: 



where _S_ end(ζ<sup>(</sup><sup>_l_)</sup> ) denotes the terminal system state reached after simulating the trajectory ζ<sup>(</sup><sup>_l_)</sup> for a planning horizon of _Hl_ decision steps. Intuitively, _J_<sup>ˆ(</sup><sup>_l_)</sup> ( _S_ τ) represents the estimated completion time of the schedule if the current policy were to be followed for _Hl_ steps. 

Following the simulation at a given level _l_ , the reflection phase distills actionable insights from the raw trajectory data. This approach is designed to clearly delineate the attributes of successful versus unsuccessful strategies by focusing on extremal outcomes. Let Z( _S_ τ) denote the set of all such valid simulated trajectories starting from the current state _S_ τ. Specifically, the module identifies the trajectories that resulted in the minimum and maximum cost estimates from the set of sim- 

ulations performed at that level: 





Finally, in the refinement phase, these two contrasting trajectories are provided to the LLM, which acts as a higher-level policy synthesizer [50]. Its task is not merely to summarize but to identify the key distinguishing features between ζbest<sup>(</sup><sup>_l_)andζ</sup> worst<sup>(</sup><sup>_l_)anddistillthese</sup> observations into a concise, textual strategic guideline, termed the Strategic Experience E. This synthesis, represented by the function _FLLM_ , effectively transforms high-dimensional, numerical simulation data into lowdimensional, human-interpretable strategic guidance: 



To ensure operational efficiency, this computationally intensive reflection process is invoked selectively. It is triggered only upon the occurrence of a dynamic event (e.g., a new job arrival or machine breakdown), as such an event may render the existing Strategic Experience E suboptimal or obsolete. 

10 

## _5.3. Experience-Guided Decision-Making_ 

The strategic experience E distilled by the reflection module provides the long-horizon context that LLMDirect schedulers lack. This module translates this highlevel guidance into a specific, executable action by constructing a concise, experience-augmented prompt. This prompt, containing only the immediate dynamic state and the guidance from E, is then used to query the LLM for a final decision. 

Theoretically, this process connects to the principles of **Approximate Policy Iteration (API)** [51]. The validity of this connection, and the resulting performance proposition, hinges on two key working assumptions regarding the reflection process: (1) the rollout cost _J_ ˆ<sup>(</sup><sup>_l_)</sup> ( _S_ τ) serves as a reasonable approximation of the true cost-to-go function for the base policy πbase; and (2) the LLM operates as a faithful synthesizer, meaning its generated experience E correctly reflects the superiority of the best simulated trajectory over the worst (Faithful Reflection). 

The experience E generated under these conditions is then used to define the final policy πE, which makes a greedy decision with respect to the guidance [52]: 



With the policy thus defined, our framework can be understood through the lens of classical rollout algorithms [53], suggesting a conditional improvement over the base policy. 

**Proposition 1** (Conditional Policy Improvement) **.** _Let_ πE _be the policy defined above and V_<sup>π</sup> ( _S_ τ) _be the expected makespan from state S_ τ _under policy_ π _. If the assumptions of Cost Function Approximation and Faithful Reflection hold, then for all states S_ τ _, the expected performance of_ πE _is no worse than that of the base heuristic policy,_ πbase _. This relationship holds over the expectation of stochastic events in the environment and the randomness of the base policy:_ 



Proposition 1 establishes a conditional theoretical proposition, grounding ReflecSched in established reinforcement learning principles. It suggests that, under plausible assumptions, the framework’s performance is not expected to degrade below that of the underlying heuristics. It is important to note that the simulated lookahead assumes no new dynamic events occur within its finite planning horizon. While a formal proof of 

the underlying assumptions is intractable for black-box LLMs, our empirical study in Section 6 shows a consistent and significant reduction in makespan. This suggests that these assumptions hold sufficiently well in practice for performance improvements to be realized. This combination of a conditional theoretical foundation and strong empirical performance suggests that ReflecSched is an effective and well-grounded framework for dynamic scheduling. 

Proposition 1 relies on the Faithful Reflection assumption, which posits that the LLM can identify key factors that differentiate successful from unsuccessful trajectories with reasonable consistency. While formal guarantees for LLM reasoning remain limited, this assumption in ReflecSched is motivated by the contrastive design of the reflection prompt. By presenting paired trajectories with high and low rollout evaluated performance (ζ _best_<sup>(</sup><sup>_l_)andζ</sup> _worst_<sup>(</sup><sup>_l_)),theframeworkreframes</sup> scheduling into a structured comparison that can be easier for LLMs than direct generation, as suggested by our empirical observations. We nevertheless note practical limitations. The usefulness of the reflection output depends on simulation complexity, since longer planning horizons or larger machine counts can dilute informative differences across trajectories and lead to suboptimal guidance. Moreover, the Cost Function Approximation assumption requires that heuristic based rollouts provide a useful surrogate for the cost to go, which can break down when the randomized base policy π _base_ explores a narrow set of trajectories. In practice, the hierarchical refinement process is intended to partially alleviate these issues by integrating feedback across multiple temporal resolutions before the final decision is made. 

## _5.4. Illustrative Analysis of the Hierarchical Planning and Refinement Loop_ 

To illustrate the hierarchical decision process, we analyze the initial dispatching decision at _t_ = 0 for the instance in Figure 1. Operation _O_ 1,1 is ready to be dispatched, and two eligible machines are available. Option A assigns _O_ 1,1 to _M_ 3 with a processing time of 1.34 time units, but this choice can create a downstream bottleneck because _M_ 3 will later be needed by operation _O_ 3,2. Option B assigns _O_ 1,1 to _M_ 2 with a processing time of 1.90 time units, which keeps _M_ 3 available for _O_ 3,2 at a later stage. This trade off between immediate processing time and future resource contention provides a test case for whether different planning levels can select the action that yields a lower overall objective. 

**Long Horizon Reflection (** _l_ = 2 **).** At this level, the scheduler runs longer simulations to capture downstream dependencies, with a horizon that is long enough 

11 

to include the release of future operations such as _O_ 3,2. Using multiple rollouts under a randomized base policy π _base_ , we observe that assigning _O_ 1,1 to _M_ 3 based solely on immediate processing time can induce substantial downstream delay, since _O_ 3,2 later competes for _M_ 3 when the machine is still occupied. The resulting Strategic Experience E2 highlights _M_ 3 as a potential future contention point and suggests that preserving its capacity for upcoming high priority operations can outweigh the small benefit of reducing the immediate processing time. 

**Medium Horizon Refinement (** _l_ = 1 **).** In this stage, the scheduler shortens the planning horizon to focus on the interval between the current state and the downstream contention point highlighted by E2. Using an additional set of rollouts with a shorter planning horizon, the results indicate that dispatching _O_ 1, 1 to machine _M_ 2 leads to lower downstream congestion, whereas dispatching it to _M_ 3 increases contention for _M_ 3 even within this shorter window. The refined strategy E1 therefore recommends trading a small increase in immediate processing time on _M_ 2 for improved availability of _M_ 3 for the priority operations. 

**Short Horizon Execution (** _l_ = 0 **).** At _l_ = 0, the scheduler performs per action evaluation using a short planning horizon via a forced rollout procedure. For Option A, the rollout conditions on assigning _O_ 1,1 to machine _M_ 3 and computes a rollout estimated makespan, interpreted in light of the strategic guidance summarized at higher levels. While this choice reduces the immediate processing time of _O_ 1,1, the subsequent simulation captures the emergence of downstream contention on _M_ 3, leading to a higher rollout cost. For Option B, the rollout conditions on assigning _O_ 1,1 to _M_ 2, under which _M_ 3 remains available when operation _O_ 3,2 becomes relevant, yielding a lower rollout cost. The scheduler therefore selects Option B, illustrating how the hierarchical procedure can expose longer range trade offs that a single horizon planner may miss. 

To provide a step by step illustration of the cost computation in Eq. 16, we evaluate the candidate actions at _t_ = 0 using the deterministic processing times reported in Table F.1. All rollouts are simulated in a disruption free environment, meaning that no exogenous events such as new job arrivals or machine breakdowns occur during the lookahead horizon. In each rollout, the randomized base policy π _base_ samples actions from a set of 24 priority dispatching rule combinations at every decision point, which promotes exploration and reduces dependence on any single heuristic. For Option A, which fixes the assignment _O_ 1,1 → _M_ 3, if one sampled trajectory yields completion times _C_ 1 = 7.51 and 

_C_ 2 = 6.80, then the simulated makespan for that trajectory is _J_<sup>ˆ(0)</sup> = max( _C_ 1, _C_ 2) = 7.51. For Option B, the simulated makespan can be lower, for example 6.51, when preserving capacity on _M_ 3 allows the downstream operation to complete earlier. This contrast provides the numerical signal used by the Hierarchical Reflection module to refine its guidance. Although higher levels focus on bottleneck identification, the base level operates with a shorter planning horizon over the same decision process; both levels use the same deterministic simulator and the same PDR sampling scheme to produce comparable rollout based guidance. 

## _5.5. Industrial Practicality and Human-Machine Collaboration_ 

Deploying ReflecSched on the shop floor requires addressing system integration constraints and operator facing requirements. In modern wafer fabrication facilities, the framework is designed as a scheduling decision support layer that interoperates with existing Manufacturing Execution Systems (MES) and Enterprise Resource Planning (ERP) platforms [54]. Integration is implemented via a modular data pipeline. The MES supplies the latest status snapshot of process chambers and wafer batches, and this structured data is converted into a textual prompt with a fixed schema for the LLM. The resulting design is intended to support timely responses to operational events by using established interfaces to send scheduling recommendations back to the equipment control layer [55]. 

ReflecSched can offer practical advantages over common metaheuristic schedulers and DRL approaches in production settings. Metaheuristic methods typically require problem specific encodings, neighborhood operators, and parameter tuning, which can make rapid adaptation to atypical disturbances challenging. DRL based schedulers often provide limited interpretability for operators and may require additional training or fine tuning when chamber configurations or process conditions change [56]. In contrast, our framework leverages pretrained language representations to support transfer across diverse operating conditions. A key component is the synthesis of Strategic Experience, which provides a longer horizon perspective on production flows with reduced reliance on task specific feature engineering. This flexibility is relevant in semiconductor manufacturing, where product mixes, recipes, and tool configurations evolve over time. 

Furthermore, the textual form of Strategic Experience can improve transparency and support communication of decision rationale. Compared with priority score 

12 

based dispatchers that output only numerical values, ReflecSched provides textual explanations, for example by highlighting a downstream bottleneck or recommending that a critical chamber remain available for a future operation. Such explanations allow shop floor supervisors to inspect the strategic intent of the recommendation and assess its consistency with operational priorities. Improved interpretability may reduce overrides that arise primarily from limited understanding, a challenge often reported in complex manufacturing settings. In addition to makespan improvements observed in our experiments, ReflecSched can function as an interpretable decision support module that helps human schedulers understand trade offs in multi stage cluster tool operations. 

## **6. Experiments** 

We conduct a series of experiments to rigorously evaluate our proposed ReflecSched framework. In Section 6.1, we detail the experimental setup, including the benchmark datasets, evaluation metrics, and models. In Section 6.2, we present a comparative performance analysis of ReflecSched against baseline methods and traditional heuristics. In Section 6.5, we conduct ablation studies to isolate the contribution of the framework’s core components and analyze the sensitivity of its key hyperparameters. Finally, in Section 6.7, we analyze the computational cost of the framework in terms of token consumption. 

## _6.1. Experimental Setup_ 

**Benchmark Datasets.** Our evaluation is performed on two benchmark suites developed for this study: GEN-Bench, for general-purpose evaluation, and PDRBench, a diagnostic benchmark to assess heuristic utilization. Both suites contain instances at two scales: Normal and Small. Specifically, GEN-Bench consists of 20 instances for the Normal scale and 18 instances for the Small scale, while PDR-Bench includes 111 instances for the Normal scale and 12 instances for the Small scale. The detailed generation and curation methodology for these datasets is described in Appendix D. 

To evaluate cross-benchmark generalizability, we additionally report results on MK-Bench and JMS-Bench. MK-Bench is derived from the Brandimarte MK01 to MK10 instances [57], and JMS-Bench models a semiconductor cluster-tool manufacturing scenario; detailed descriptions are provided in Sections 6.3 and 6.4, respectively. 

**Metrics and Models.** To ensure a fair and scalable comparison across instances of varying difficulty, we use relative performance metrics. Our primary metrics are: 

1. **Relative Percent Deviation (RPD)** , which normalizes performance against the best-known solution for each instance, calculated as: 



where _C_ max is the makespan from the evaluated method and _C_ max<sup>⋆isthebestmakespanfoundfor</sup> that instance across all methods and runs in this study. Lower RPD is better. 

2. **Average Rank** , which measures the consistency of a method’s performance. For each instance, all competing methods are ranked based on their makespan. A method’s average rank is its mean rank across all instances. A lower average rank indicates a consistently superior method. 

To assess statistical significance, we use the nonparametric Wilcoxon signed-rank test [58]. We evaluate a range of LLMs, including GPT-4o [59], DeepSeekV3 [60], and the Qwen3 series (8B, 14B, 32B) [38]. All models are prompted in a zero-shot manner with Chainof-Thought reasoning [47]. 

**Evaluation Protocol.** For initial diagnostic analyses aimed at capturing intrinsic model behaviors, we employ a multi-sample voting scheme: actions are decided by a majority vote from 5 independent generations at a high temperature ( _T_ = 0.8) [61]. For the final comparative experiments against the LLM-Direct baseline, all LLM inferences use a low temperature ( _T_ = 0.2) for efficiency and stability. 

To ensure the reliability of our findings and mitigate the stochastic nature of LLM generation, we conduct three independent runs for each problem instance and use the resulting mean values for our primary analysis. The statistical significance of the performance improvements is assessed using the non-parametric Wilcoxon signed-rank test. It is important to note that the sample size for this statistical test is defined by the total number of problem instances in the benchmark suites instead of the number of independent runs per instance. This methodology ensures that the statistical claims are based on a diverse population of scheduling scenarios, while the repeated runs for each case provide a more stable and accurate estimate of the expected performance for each individual instance. 

13 



<!-- Start of picture text -->
ReflecSched vs LLM Direct   Segmented by Normal / Small / Average<br>25 Best Rules RPD (8.64%) Normal Small Average 100<br>Average Rules RPD (13.34%)<br>LLM Direct RPD<br>ReflecSched RPD<br>20 Win Rate (%) 80<br>15 75.0%* 70.0%* 75.0%* 75.0%** 70.0%** 12.7875.0%* 13.7573.7%** 61.1%* 72.2%* 12.9266.7%* 73.0% 69.7% 60<br>10 12.46 9.37 11.67 9.82 11.59 9.69 11.32 8.52 10.98 8.29 9.29 9.69 11.60 8.85 10.61 8.41 10.19 11.61 9.14 12.33 9.29 40<br>5 20<br>0 0<br>GPT4o DeepSeekV3 Qwen332B Qwen314B Qwen38B GPT4o DeepSeekV3 Qwen332B Qwen314B Qwen38B Avg Avg<br>Avg. RPD (%) Win Rate (%)<br><!-- End of picture text -->

Figure 7: Comparative performance of ReflecSched and the LLM-Direct baseline on the GEN-Bench dataset. Bars (left y-axis) represent the average RPD, where lower is better. The green line (right y-axis) shows the Win Rate of ReflecSched against the baseline, indicating the percentage of instances where it finds a strictly better solution. For reference, the performance of the single best-performing PDR (i.e., the heuristic with the lowest average RPD across all instances) and the average of all PDRs are shown as red and purple dashed lines, respectively. Asterisks denote statistical significance from Wilcoxon signed-rank tests (* _p_ < 0.05, ** _p_ < 0.01, *** _p_ < 0.001). 

Table 2: Statistical comparison between ReflecSched and the bestperforming heuristic on each instance across all problem cases. 

|**Instance Set**|**RPD (%)**|**_p_-value**|
|---|---|---|
|Normal|0.0620|0.8107|
|Small|0.9331|0.1240|



## _6.2. Comparative Performance Analysis_ 

In this section, we conduct a detailed quantitative analysis of ReflecSched using the GEN-Bench dataset to evaluate its general performance across varying problem scales. 

## _6.2.1. Comparison with LLM-Direct and Heuristics_ 

Our primary comparison is against the LLM-Direct baseline to investigate the effectiveness of our hierarchical reflection architecture. As shown in Figure 7, ReflecSched demonstrates a statistically significant performance improvement over LLM-Direct across all tested configurations. It achieves a 71.35% average Win Rate and an average RPD reduction of 2.755%. 

Furthermore, the framework is capable of outperforming any single heuristic. We also compared its performance to an oracle baseline constructed by selecting the best-performing heuristic for each instance individually. As shown in Table 2, a two-sided Wilcoxon signedrank test confirms no statistically significant difference between ReflecSched and this strong oracle baseline ( _p_ > 0.05), highlighting the framework’s effectiveness. 

## _6.2.2. Comparison with Baseline Methods_ 

To benchmark our ReflecSched framework, we selected and adapted five recent and competitive baselines spanning evolutionary and reinforcement learning approaches to scheduling. The baselines are taken from recent peer reviewed literature and are chosen to cover diverse modeling and optimization styles. Specifically, we include GP, an evolutionary method that uses genetic programming to evolve priority functions over a predefined feature set, reducing reliance on manually designed dispatching rules [63]. We also include DAN, an attention based model that jointly attends to operations and machines to learn instance specific representations for scheduling [64]. 

For benchmarking, we evaluate three distinct reinforcement learning baselines with diverse architectural characteristics. IDDQN is a Double DQN variant optimized for dispatching rule selection under stochastic machine breakdowns, employing a dueling network architecture and a modified experience replay scheme [65]. PPO-OC implements a Proximal Policy Optimization policy that maps production states to dispatching rules through a discrete action space [66]. HMPSAC adopts a hierarchical multi-policy Soft ActorCritic framework, where a high-level controller determines intermediate objective signals and low-level policies execute specific dispatching rules [67]. Since our problem formulation involves dynamic event types that deviate from the original assumptions of these algorithms, we adapted their state representations and action interfaces to ensure compatibility with our event-driven model. The comprehensive training protocols and hy- 

14 

Table 3: Comprehensive performance evaluation of ReflecSched variants against baseline algorithms across diverse benchmarks. Performance is quantified via Average Relative Percentage Deviation (RPD, %) and Average Rank, where lower values signify optimal outcomes. Bold values denote the best performance in each row. 

|**Metric**|||**Baseli**|(a<br>**ne Metho**|) Gener<br>**ds**|al Performan|ce Evaluati|on on GEN-B|ench|**ReflecSc**|**lhed**|||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||GP|HMPS|AC<br>|IDDQN|DAN|PPO-OC|Q3-8b|Q3-14b|Q3-32b|DS-v3|DS-v3.2|GPT-4o|GPT-5n|
|Avg. RPD (%)|54.85|11.0|0|10.45|10.74|13.47|6.94|**6.09**|6.87|7.49|7.74|7.14|8.03|
|Avg. Rank|11.42|6.6|8|6.58|6.47|8.05|5.34|**4.39**|5.45|5.58|5.21|5.34|5.32|
|**Dataset**|**Metric**|||(b) Cro<br>|ss-Benc<br>**Baseli**<br><br>|hmark Stabi<br>**ne Metho**<br>|lity on MK<br>**ds**<br><br>|-Bench and J<br>|MS-Bench<br>|**l**<br>|**ReflecSche**<br>|**ld**<br>||
||||GP|HMPS|AC<br>|IDDQN|DAN<br>|PPO-OC|Q3-8b|Q3-14b|Q3-32b|DS-v3.2|GPT-5n|
|MK-Bench|Avg. RPD|(%)|55.80|14.3|2|11.85|17.81|15.91|10.30|14.30|13.83|**6.83**|13.19|
||Avg. Ran|k|9.00|5.40||4.70|6.60|5.20|4.00|5.70|5.20|**3.90**|4.90|
|JMS-Bench|Avg. RPD|(%)|46.80|9.72||8.01|15.56|10.94|6.47|**6.18**|7.74|8.50|10.16|
||Avg. Ran|k|9.70|5.00||4.70|7.10|5.70|4.20|**4.00**|4.10|4.40|5.30|



_Note: Q3 denotes the Qwen3 series [38], DS denotes the DeepSeek series [60, 39], and GPT-5n refers to GPT-5 nano [62]. RPD values are expressed as percentages to highlight subtle performance variations between competitive models._ 

perparameter configurations for all evaluated methods are detailed in Table H.1. To ensure empirical fairness and a rigorous comparison, we strictly adhered to the canonical configurations and optimal settings recommended in the original literature for each baseline algorithm. 

The performance of ReflecSched, instantiated with seven different LLM backends, was compared against these baselines. The results, summarized in Table 3, unequivocally demonstrate the superior performance of our framework. To facilitate a more granular assessment of per-instance performance and variability, we provide a comprehensive record of raw makespan results in Appendix G. This supplement includes individual data for the LLM variants, specifically Qwen3-8B, Qwen314B, Qwen3-32B [38], DeepSeek-V3 [60], DeepSeekV3.2 [39], GPT-4o [59], and GPT-5 Nano [62], alongside the five specialized comparative algorithms. 

As detailed in Table 3a, all ReflecSched configurations demonstrate a substantial performance advantage over the traditional reinforcement learning and heuristic baselines on the GEN-Bench dataset. While the most competitive baseline method IDDQN achieves an average RPD of 10.45 percent, every variant of the ReflecSched framework maintains a significantly lower deviation with values ranging from 6.09 percent to 8.03 percent. Notably, the configuration utilizing the Qwen3 14b model delivers the most superior outcomes by attaining the minimum average RPD of 6.09 percent and the lead- 

ing average rank of 4.39. Other specialized reinforcement learning approaches such as HMPSAC and DAN exhibit higher deviations of 11.00 percent and 10.74 percent respectively, which further underscores the efficacy of the hierarchical reflection mechanism in optimizing complex scheduling trajectories. The consistency of the proposed framework is further validated by the rank metrics where the ReflecSched variants occupy the top seven positions while the GP heuristic trails significantly with an average rank of 11.42. These results indicate that ReflecSched possesses a robust capacity for high-quality solution generation that exceeds the capabilities of models relying on direct generation or conventional training paradigms. 

In summary, the ReflecSched framework not only delivers superior overall performance but also demonstrates remarkable robustness. Unlike the baseline methods, whose effectiveness varies considerably between problem scales, ReflecSched consistently delivers toptier results, proving its strong generalization and balanced performance. 

## _6.3. Evaluation on Established Benchmarks: MKBench_ 

To validate the cross-configuration generalizability of ReflecSched, the framework is benchmarked against MK-Bench, a suite derived from the established Brandimarte MK01–MK10 Flexible Job-Shop Scheduling instances [57]. The integration of these recognized bench- 

15 

marks ensures consistency with standardized scheduling research. Given that the original Brandimarte instances are inherently static, we implement a systematic transformation protocol to extend them into dynamic environments. This adaptation introduces stochastic event arrivals while preserving the intrinsic shop topology, specifically the job and machine counts, as well as the nominal processing durations. 

The adaptation protocol is structured into three sequential phases. First, the scheduling horizon for each instance is determined by deriving a theoretical workload lower bound, defined as the maximum of the longest individual job processing time and the average machine-wise workload. This bound is subsequently scaled by a factor of 1.2 to define the simulation horizon, thereby providing sufficient temporal slack for dynamic adjustments. Second, the three primary bottleneck machines are identified based on their average workload share, establishing a systematic basis for the introduction of targeted stochastic disruptions. Third, four categories of dynamic events are injected using a deterministic random seed to ensure experimental reproducibility. In these scenarios, 60% of the jobs are initialized at _t_ = 0 to simulate initial work-in-progress (WIP), while subsequent tasks follow an exponential arrival distribution restricted to the first half of the horizon. Furthermore, each resource is subject to a 50% breakdown probability, with mean time to repair sampled uniformly between 1.0 and 4.0 time units. Furthermore, the transformation incorporates stochastic job cancellations with a 30% probability and the insertion of high-priority urgent jobs, which arrive at timestamps sampled uniformly from 25% to 75% of the simulation horizon. These urgent tasks are strategically assigned to the previously identified bottleneck machines to intensify resource contention and evaluate the framework’s robustness under adversarial conditions. 

As detailed in the MK-Bench results within Table 3b, the ReflecSched framework demonstrates high stability when applied to flexible job-shop scheduling problems. While the most effective DRL baseline IDDQN achieves an average RPD of 11.85 percent, the ReflecSched variants maintain a clear performance advantage within this benchmarking suite. Specifically, the variant utilizing DeepSeek v3.2 attains the most favorable outcomes with an average RPD of 6.83 percent and a leading average rank of 3.90. This level of performance indicates that the hierarchical reflection mechanism successfully identifies fundamental coordination patterns that extend beyond the specific distributions encountered during the initial prompts. This finding validates the efficacy of the framework in addressing the intensive 

resource competition and machine flexibility constraints inherent in the standardized MK01 through MK10 instances. The overall results suggest that the strategic insights derived from the reflection module facilitate a robust approach to managing diverse workshop topologies without the necessity for specialized retraining or architecture modification. 

## _6.4. Validation on Manufacturing Scenarios: JMSBench_ 

To evaluate the industrial applicability of ReflecSched, we benchmark the framework on the JMS-Bench dataset, which is tailored to replicate the operational dynamics of a semiconductor cluster tool. In modern wafer fabrication, the cluster tool constitutes the primary production unit, comprising a central transfer robot integrated with five heterogeneous processing modules, designated as PM1 through PM5, as shown in Figure 2. Within this manufacturing context, each job represents a Front Opening Unified Pod (FOUP) carrying a batch of silicon wafers that must undergo a sequence of high-precision chemical and physical operations. The production flow is comprised of four distinct processing stages: Rough Etching, Finishing, Surface Grinding, and Metrology Inspection. 

The scheduling complexity of this system is exacerbated by the functional overlap of chamber capabilities across these processing stages. Specifically, the Rough Etching stage utilizes _PM_ 1 and _PM_ 2, while the Finishing stage is shared between _PM_ 2 and _PM_ 3. Surface Grinding is distributed across _PM_ 3 and _PM_ 4, whereas Metrology Inspection is primarily handled by _PM_ 5 with occasional overflow support from _PM_ 4. This configuration dictates that _PM_ 2, _PM_ 3, and _PM_ 4 serve as dualfunctional modules that interlink consecutive processing phases. Consequently, the scheduler must manage acute resource contention, where the completion of a finishing task in _PM_ 3 may preclude the initiation of a grinding operation for a concurrent job. Unlike traditional job shops, the central robot acts as a critical shared transport resource that must be tightly synchronized with these overlapping chamber cycles to prevent deadlocks, requiring the scheduler to incorporate lookahead reasoning regarding module availability to sustain high throughput. 

In this case study, we characterize three representative categories of dynamic disturbances inherent to semiconductor manufacturing: the insertion of highpriority “hot lots” necessitating immediate preemption of nominal production, stochastic chamber failures induced by equipment drift, and job cancellations arising from upstream yield fluctuations. These events ne- 

16 

cessitate non-myopic reasoning to re-allocate resources while preserving the integrity of the global production schedule. The Strategic Experience produced by ReflecSched is designed to encode such high level coordination patterns, for example by deciding when a shared resource such as _PM_ 4 should be kept available for metrology to reduce queue buildup at the inspection stage during high arrival periods. 

The comparative performance metrics for the semiconductor manufacturing environment are detailed in Subtable b of Table 3b. According to the recorded data, the ReflecSched variants demonstrate significant advantages in managing the complex operational constraints of cluster tools when compared to both meta-heuristic and reinforcement learning baselines. Among the baseline algorithms, IDDQN emerges as the most competitive approach with an average RPD of 8.01 percent and an average rank of 4.70. However, the ReflecSched configuration powered by the Qwen3 14b model surpasses all baselines by achieving a minimum average RPD of 6.18 percent and an optimal average rank of 4.00. Other variants such as Qwen3 8b and Qwen3 32b also maintain high solution quality with RPD values of 6.47 percent and 7.74 percent respectively. This performance trend indicates that the hierarchical reflection mechanism effectively internalizes the intricate module to stage mappings and transport synchronization requirements inherent in semiconductor fabrication. Furthermore, the proposed framework consistently outperforms specialized reinforcement learning architectures such as HMPSAC and PPO-OC which yield higher RPD values of 9.72 percent and 10.94 percent respectively. These findings suggest that the strategic insights codified within the reflection module provide a robust foundation for mitigating resource contention even under the severe stochastic disruptions characteristic of modern wafer processing units. 

## _6.5. Ablation and Sensitivity Analysis_ 

All experiments in this section were conducted using Qwen3-8B as the base model. 

## _6.5.1. Impact of Hierarchical Reflection_ 

To isolate the contribution of our core architectural design, we conducted an ablation study comparing the full ReflecSched framework ( _L_ = 6, _R_ = 24) against an ablated, single-level version ( _L_ = 0). The results in Figure 8 confirm that the strategic foresight gained from multi-level reflection is a primary driver of the framework’s effectiveness. More revealingly, simply increasing the search breadth for the single-level model fails to 

improve its performance, which plateaus and can even degrade. This suggests that a brute-force, “flat” search is ineffective without hierarchical guidance and confirms that the hierarchical reflection mechanism provides a qualitative benefit that simply increasing computation cannot replicate. 



<!-- Start of picture text -->
Ablated: Single-Level Reflection ReflecSched<br>12 (L=0) (L=6)<br>10 9.51% 8.90% 9.21% 9.04% 9.75%<br>8.38%<br>8<br>6<br>4<br>2<br>0<br>1 3 6 12 24 R=24<br>Number of Rollouts<br>Average RPD (%)<br><!-- End of picture text -->

Figure 8: Ablation study on the hierarchical reflection mechanism. The chart compares the average RPD of the full ReflecSched framework with that of a single-level version. The performance of the single-level model is shown across a range of different values for the Number of Rollouts. 

## _6.5.2. Impact of Experience Quality and Evidence Selection_ 

We conducted studies to assess the impact of experience quality and the strategy for selecting evidence. The results are presented in Figure 9. 

**Experience Quality.** We compared four configurations: our complete Full Experience; Shuffled experience, which randomizes temporal order; Generic problem-agnostic experience; and Noise, where guidance from the best and worst historical experiences is swapped. As shown on the left of Figure 9, Full Experience significantly outperforms all alternatives. The poor performance with Shuffled and Generic experience highlights the importance of temporal coherence and domain-specific learning. The severe degradation with Noise demonstrates that misleading information is highly detrimental. 

**Evidence Selection Strategy.** We investigated four strategies for selecting the trajectories that serve as the empirical basis for reflection. Our Full approach provides contrastive insights by pairing the best and worst outcomes from the simulation pool. In contrast, TopK Best focuses exclusively on successful trajectories to highlight optimal patterns, while Top-K Worst utilizes only the poorest-performing sequences to identify critical anti-patterns. The Quartile strategy employs a strat- 

17 



<!-- Start of picture text -->
Experience Quality (Left) vs Evidence Selection (Right)<br>(a) Absolute RPD Performance<br>10<br>Normal Dataset Experience Quality Full Evidence Selection<br>Small Dataset 8.49 8.33<br>7.80<br>8 7.30<br>6.79<br>6 6.80 5.10 7.01 4.89<br>4.15<br>3.61<br>4<br>4.38<br>2.13<br>2 1.15<br>0<br>Shuffled Generic Noise Full Top-K Best Top-K Worst Quartile<br>(b) Average Rank Performance<br>3.5 Normal Dataset3.05 3.00<br>Small Dataset 2.75<br>3.0 2.50 2.45<br>2.15 2.15<br>2.5 2.95 1.85<br>2.0 2.45 2.50 2.50<br>1.25<br>1.5<br>1.0 1.45<br>0.5<br>0.0<br>Shuffled Generic Noise Full Top-K Best Top-K Worst Quartile<br>Average RPD (%)<br>Average Rank<br><!-- End of picture text -->

Figure 9: Ablation studies on Experience Quality (left) and Evidence Selection (right), using Qwen3-8B. (a) shows the Absolute RPD Performance, and (b) shows the Average Rank Performance. For both metrics, lower values are better. 

ified sampling method to gather evidence from across the top, middle, and bottom performance tiers of the simulation results. The results on the right of Figure 9 show that none of the alternatives match the comprehensive guidance of the Full experience. Interestingly, on the Normal Dataset, the Top-K Worst strategy outperforms Top-K Best, suggesting that learning from failures to identify actions that should be avoided can be more valuable than learning exclusively from successes. This establishes that a comprehensive evidence base utilizing contrastive extremal outcomes provides the most robust learning signal. 

## _6.5.3. Parameter Sensitivity Analysis under Budget Constraint_ 

To understand the trade-off between search depth (Levels, L) and search width (Rollouts, R), we conducted a sensitivity analysis under a fixed computational budget where _L_ × _R_ = 24. As illustrated in Figure 10, the results reveal a clear and consistent optimal balance. 

On both datasets, the configuration of _L_ = 2, _R_ = 12 achieves the best performance. This strongly suggests that a moderate search depth combined with a substan- 



<!-- Start of picture text -->
Rollout Parameter Configuration Analysis<br>8 Normal DatasetSmall Dataset Budget Constraint: L×R = 24<br>7 6.52%<br>6 5.53% 5.69%<br>5.19%<br>5<br>4.86% 5.05%<br>4 3.27%<br>3 3.63%<br>2 2.29%<br>1<br>1.11%<br>0<br>L=1,R=24 L=2,R=12 L=3,R=8 L=4,R=6 L=6,R=4<br>Levels (L), Rollout (R)<br>Average RPD (%) - Lower is Better<br><!-- End of picture text -->

Figure 10: Analysis of Level (L) and Rollout (R) configurations under a fixed computational budget of _L_ × _R_ = 24. The graph shows the Average RPD (%) on both Normal and Small datasets for the Qwen38B model. Lower RPD indicates better performance. 

tial search width is the most effective strategy under a fixed budget. Both an extremely wide, shallow search ( _L_ = 1) and an extremely deep, narrow search ( _L_ = 6) lead to suboptimal performance. This analysis demonstrates that a balanced configuration that moderately favors search width over depth provides the most ro- 

18 



<!-- Start of picture text -->
Machine<br>PM5 O 7 , 3 O 11 , 4 O 6 , 4 O 13 , 3 O 12 , 3 O 1 , 3 O 14 , 3 O 16 , 3 O 8 , 3 O 17 , 4<br>PM4 O 11 , 3 O 17 , 3<br>PM3 O 7 , 2 O 6 , 2 O 6 , 3 O 13 , 2 O 13 , 2 O 5 , 2 O 18 , 1 O 14 , 2 O 8 , 2<br>PM2 O 6 , 1 O 11 , 1 O 11 , 2 O 4 , 1 O 17 , 1 O 1 , 1 O 12 , 2 O 1 , 2 O 16 , 2 O 17 , 2<br>PM1 O 7 , 1 O 13 , 1 O 8 , 1 O 12 , 1 O 3 , 1 O 5 , 1 O 9 , 1 O 14 , 1 O 16 , 1<br>0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 Time<br>Machine<br>PM5 O 13 , 3 O 3 , 3 O 6 , 4 O 11 , 4 O 8 , 3 O 12 , 3 O 14 , 3 O 16 , 3 O 1 , 3<br>PM4 O 6 , 3 O 7 , 3 O 4 , 3 O 5 , 3 O 17 , 3 O 17 , 4<br>PM3 O 13 , 2 O 6 , 2 O 11 , 2 O 11 , 3 O 8 , 2 O 8 , 2 O 17 , 2 O 14 , 2 O 16 , 2<br>PM2 O 6 , 1 O 3 , 1 O 3 , 2 O 7 , 2 O 4 , 2 O 5 , 2 O 9 , 1 O 12 , 1 O 12 , 2 O 16 , 1 O 1 , 2<br>PM1 O 13 , 1 O 7 , 1 O 11 , 1 O 8 , 1 O 4 , 1 O 5 , 1 O 17 , 1 O 14 , 1 O 18 , 1 O 14 , 1 O 1 , 1<br>0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 Time<br><!-- End of picture text -->

Figure 11: Comparative Gantt chart analysis of the semiconductor cluster tool scheduling instance. The top chart illustrates the schedule generated by the myopic baseline which achieves a makespan of 40.0. The bottom chart depicts the schedule produced by the ReflecSched framework yielding a superior makespan of 36.67. Red cross symbols denote the occurrence of dynamic machine breakdowns on modules PM3 and PM5. This comparison demonstrates how the proposed hierarchical reflection mechanism identifies global strategic trade-offs to mitigate the impact of stochastic disruptions. 

bust and effective performance across different problem scales. 

## _6.6. Case Study: Dynamic Scheduling under Stochastic Disruptions_ 

To provide a detailed elucidation of the decisionmaking mechanisms within ReflecSched, we conduct a comparative analysis of two distinct scheduling trajectories for a representative production instance. This scenario comprises five processing modules ( _PM_ 1 to _PM_ 5) and 15 wafer batches with heterogeneous processing requirements. The primary objective is to evaluate the framework’s resilience to stochastic machine failures and its ability to circumvent sub-optimal local states typical of reactive heuristics. As evidenced by the trajectory comparison, the ReflecSched-guided policy (Case A) yields an optimized makespan of 36.67, whereas the reactive baseline (Case B) results in an extended completion time of 40.0. 

The dynamic scenario in this case study is characterized by two discrete equipment malfunctions: _PM_ 5 undergoes a failure at _t_ = 8.78 and is restored to operational status at _t_ = 10.74, followed by a secondary failure of _PM_ 3 at _t_ = 14.80, with recovery at _t_ = 17.41. Upon the initial failure of _PM_ 5, the Strategic Experience codified by the reflection module designates Job 3 and Job 6 as critical-path tasks for the Metrology stage. Consequently, the scheduler preempts noncritical tasks, specifically Job 14 on _PM_ 1 and Job 9 on _PM_ 2, to expedite the resumption of Job 8 and Job 5 as resources become available. By tolerating localized delays for standard batches, ReflecSched prevents downstream delay propagation for Job 16 and Job 1, facilitat- 

ing the conclusion of the final metrology operation for Job 1 at _t_ = 36.67 

In contrast, Case B exemplifies the inherent limitations of a reactive, greedy baseline. While this approach maximizes chamber utilization during the initial 10 time units, it lacks sufficient look-ahead capability to mitigate long-term resource contention. When the identical disruptions affect _PM_ 3 and _PM_ 5, the baseline model fails to reconfigure the global schedule optimally. Specifically, the myopic assignment of Job 13 and Job 11 to _PM_ 3 early in the horizon induces severe congestion at the finishing stage. This inflexible allocation logic necessitates that Job 17 remains idle until the final phases of the simulation horizon before accessing its terminal processing chamber. Consequently, the absence of strategic coordination causes Job 17 to become the primary system bottleneck, yielding an extended makespan of 40.0. This comparison provides empirical evidence that the integration of hierarchical reflection enables the scheduler to anticipate downstream bottlenecks and sustain high throughput in the presence of intensive stochastic disturbances. 

## _6.7. Efficiency and Runtime Analysis_ 

To evaluate the practical utility of ReflecSched, we conduct a multi-dimensional efficiency analysis encompassing wall-clock time, hardware overhead, and token consumption. All experiments were executed on a workstation featuring an Intel Xeon Platinum 8468V CPU and an NVIDIA H100 GPU (80 GB VRAM). LLMbased models were deployed via vLLM to ensure highthroughput inference [68]. 

19 

In dynamic manufacturing environments, the selection of a scheduling framework requires a careful tradeoff between deployment readiness and per-instance execution speed. While DRL models exhibit extremely low inference latency once weights are fully trained, their high initial training overhead serves as a significant bottleneck when factory configurations or optimization objectives shift. Conversely, ReflecSched utilizes a zeroshot architecture that enables immediate deployment without any prior training phase. 

We analyze this trade-off using Cumulative Wallclock Time as defined by the following formulation: 



Figure 12: Break-even analysis of cumulative wall-clock time. Intercepts at _N_ = 0 represent initial training overhead. Solid and dashed lines denote recorded and extrapolated runtimes, respectively, with markers highlighting break-even points against the HMPSAC baseline. 



Table 4: Average total token consumption (in thousands) per instance on the GEN-Bench dataset. 

where _Ttrain_ represents the offline training time and _Tinfer_ , _i_ denotes the wall-clock time required for each scheduling instance. As illustrated in Figure 12, ReflecSched maintains a clear efficiency advantage in scenarios involving limited batch sizes or frequent environment re-configurations. Specifically, for the DeepSeekV3.2 and GPT-5-nano backends, the cumulative time remains lower than that of the DRL baseline until the number of instances reaches a break-even point of approximately 74 and 50 respectively. 

However, we must acknowledge that due to the inherent computational complexity of large language model inference and iterative reflection, the marginal time cost per instance for ReflecSched is higher than that of specialized DRL models. In static environments characterized by massive, repetitive instance batches where _N_ significantly exceeds the break-even point, the initial training investment of DRL is effectively amortized, which allows its fast inference capability to become a dominant advantage. Therefore, ReflecSched is most suitably positioned as a robust solution for highvariability manufacturing systems where the cost of repeated model retraining would be prohibitive. 

|**Model**|**Normal**|**Scale**|**Small**|**Scale**|
|---|---|---|---|---|
||LLM-Direct|ReflecSched|LLM-Direct|ReflecSched|
|GPT-4o|137.4k|115.4k|21.3k|45.2k|
|DeepSeek-V3|144.4k|126.3k|23.7k|49.7k|
|Qwen3-32B|153.3k|144.6k|23.6k|52.5k|
|Qwen3-14B|146.4k|120.9k|21.7k|46.6k|
|Qwen3-8B|148.8k|112.8k|22.8k|45.5k|
|**Average**|146.1k|**124.0k**|**22.6k**|47.9k|



The results in Table 4 reveal a trade-off dictated by problem scale. For Normal scale instances, which are longer and more complex, ReflecSched is significantly more token-efficient than the baseline. This is because the reflection module’s generated Strategic Experience allows subsequent decision-making prompts to be much leaner. Conversely, for Small scale instances, the upfront computational cost of the initial reflection outweighs these savings, resulting in higher token consumption. However, considering the significantly improved makespan ratio achieved by ReflecSched, this highlights an intentional architectural trade-off: ReflecSched allocates a greater budget to its initial reflection phase, an investment that proves effective for larger, more complex problems by improving solution quality while simultaneously reducing the total computational and financial tokens required. 

20 

## **7. Conclusion** 

This paper first provided an empirical diagnosis of applying LLMs to DFJSP, identifying three critical pitfalls: the long-context paradox, heuristic underutilization, and myopic decision-making. To address these, our proposed ReflecSched framework recasts the LLM as a strategic analyst, distilling insights from multilevel simulations into a “Strategic Experience” to guide execution. Experiments confirm that ReflecSched significantly outperforms direct LLM baselines, surpasses all traditional heuristics overall, and maintains performance on par with the instance-specific best heuristic across all problem instances. We posit that the core principle of decoupling strategic reflection from execution offers a promising template for applying LLMs to a broader class of sequential decision-making problems. 

## **Acknowledgements** 

This work was partly supported by the National Natural Science Foundation of China. The code is available on https://github.com/cls1277/ReflecSched after being accepted. 

## **Appendix A. Implementation Details of LLMDirect** 

This appendix details the implementation of the LLM-Direct baseline scheduler. The scheduler is implemented as a decision-making agent within an eventdriven simulation framework. It is invoked to make a scheduling decision at a discrete point in time, defined as a decision point. A decision point occurs whenever the processing of system events (e.g., an operation completion or machine repair) leads to a state where at least one machine is idle while one or more operations are ready for processing. 

## _Appendix A.1. Event-Driven Simulation._ 

The simulation framework is centered on an event loop that processes a series of time-stamped events (e.g., job arrivals, machine breakdowns, operation completions), which are managed in a priority queue. The simulation progresses by advancing its internal clock to the timestamp of the next event in the queue and updating the system state according to the event’s type. A decision point is reached only after the event queue has been processed up to the current simulation time and the resulting state indicates that at least one operation is ready to be scheduled. This event-driven architecture ensures 

that the LLM is invoked to make a decision only at these specific, necessary junctures, rather than on a continuous basis. 

## _Appendix A.2. State Representation and Prompt Construction_ 

At each decision point, a structured textual prompt is constructed to encode the current state of the workshop for the LLM. This prompt serves as the sole source of information for the LLM’s decision-making process. The detailed structure, components, and the logic governing its construction are provided in Appendix E. 

## _Appendix A.3. Core State Management_ 

The entire dynamic state of the simulation is encapsulated within a central state management class. This class serves as the single source of truth for the workshop’s status and is responsible for processing all dynamic events and calculating the set of currently feasible actions. Its key functional components are as follows: 

_Initialization._ The state manager is initialized with the static problem definition, including job structures and machine processing times, along with a predefined queue of initial dynamic events and the starting simulation time. 

_State Variables._ Key variables maintained by the state manager include: 

- The availability time for each machine, corresponding to the parameter _rk_ ( _t_ ) in the formal model. 

- The progress of each job, tracked by its last successfully completed operation. 

- A set containing the identifiers of machines currently in a non-operational state. 

- A set identifying jobs that have been designated with emergency status. 

- A set of operations that have been interrupted (e.g., due to a machine breakdown) and are awaiting resumption. This corresponds to the set O _int_ . 

_Event Handling._ This is the central method for state transition. It processes a single event (e.g., a Job Arrival, Machine Breakdown, or Operation Completion) based on its type and timestamp. This method is responsible for updating all relevant state variables. For instance, a Machine Breakdown event adds the machine to the set of broken machines and moves any in-process operation 

21 

to the set of interrupted operations. A Job Emergency event dynamically loads the data for the new urgent job and adds its identifier to the set of emergency jobs. 

_Feasible Action Generation._ At each decision point, this method is invoked to determine the set of all feasible scheduling actions. It iterates through all active jobs, verifies their arrival and precedence constraints, and identifies all operations that are ready to be scheduled. For each such operation, it determines the subset of its candidate machines that are currently available (i.e., not broken and not busy). The output is a set of feasible actions, which is used to generate the “Ready Operations” and “Candidate Actions” sections of the LLM prompt. 

_Action Execution._ Once the LLM selects an action, this method executes it. It updates the availability time of the selected machine, records the assignment for performance tracking (e.g., for Gantt chart generation), and updates the machine’s workload metrics. Crucially, it generates a new Operation Completion event with a calculated end time and inserts it into the simulation’s priority queue. 

## **Appendix B. Case Study: An Analysis of the Comprehension Limitations in Smaller LLMs** 

This appendix provides a qualitative analysis of the reasoning process exhibited by a smaller-scale model (Qwen3-4B) when functioning as the LLMDirect scheduler [38]. The subsequent examples, extracted directly from execution logs, are presented to illustrate specific failure modes. These examples highlight the model’s difficulties in consistently and accurately interpreting the complex, natural-language representation of the DFJSP state. These case studies serve as empirical evidence for the central claim of our main paper: that the direct application of LLMs to this scheduling problem exhibits significant limitations. This analysis, therefore, underscores the necessity for a more structured framework like ReflecSched. 

The prompt also provides other strategic metrics for this operation. 

_Model’s Reasoning and Behavior._ Across all five sampled responses, the model’s reasoning was nearly identical. A representative example is provided below, with the key reasoning statement highlighted in bold. 

### <mark>Reasoning:</mark> 

- <mark>Since there are no emergency jobs, I need to choose the next operation...</mark> 

<mark>The primary objective is to minimize the final makespan, which means</mark> **<mark>we should choose the operation that has the shortest processing time</mark>** <mark>... the operation on Machine 1 has the shortest processing time of 1.78. {"job": 1, "op": 1, "machine": 1}</mark> 

_Analysis._ This case highlights the model’s strong propensity to favor a simple, locally-optimal heuristic—the Shortest Processing Time (SPT) rule. While the model correctly identifies the action corresponding to the SPT rule, its explicit reasoning reveals that it largely disregards other strategic information provided in the prompt, such as the remaining work and number of operations for the job. The model’s decision-making process reduces to a one-dimensional analysis, which serves as a concrete example of the “myopic greed” pitfall we identify in the main paper. Although the model can parse individual data points, it fails to synthesize these multiple, potentially conflicting, pieces of information into a more robust strategic evaluation. 

## _Appendix B.2. Misinterpretation of State Descriptors_ 

_Prompt Context._ At a later decision point ( _t_ = 7.466), the model is presented with two ready operations, one of which is the final operation for its corresponding job. The two candidate actions are: 

- Job 1, Operation 3 on Machine 1 (Time 2.99, rem_work=0.0, rem_ops=0) 

- Job 5, Operation 1 on Machine 1 (Time 1.85, rem_work=5.31, rem_ops=3) 

## _Appendix B.1. Over-reliance on a Simple Heuristic_ 

_Prompt Context._ At the initial decision point in the simulation ( _t_ = 2.426), the model is presented with a scenario involving a single ready operation, _O_ 1,1, which has two candidate machines: 

_Model’s Reasoning and Behavior._ Several of the model’s responses exhibit a critical misinterpretation of the state descriptors. A representative example follows: 

<mark>Reasoning:</mark> 

- Machine 1, Processing Time: 1.78 

- Machine 3, Processing Time: 2.66 

<mark>Job 1 Operation 3 on Machine 1: This operation ...</mark> **<mark>is already completed (rem_work = 0.0, rem_ops = 0)</mark>** <mark>...</mark> 

22 

<mark>Since Job 1 Operation 3 is already completed ...the only operation that affects the makespan is Job 5 Operation 1. Therefore, we should schedule Job 5 Operation 1... {"job": 5, "op": 1, "machine": 1}</mark> 

_Model’s Reasoning and Behavior._ The five sampled responses for this single decision point show a striking lack of consistency and, in some cases, outright confusion. 

- Correct Responses (3 out of 5): Three responses correctly identified the emergency job. 

_Analysis._ This case provides a clear instance of a semantic interpretation failure. The model’s reasoning hinges on a critical error: it confuses a description of a potential future state with a historical fact. Specifically, it incorrectly interprets the metrics rem_work=0.0 and rem_ops=0—which describe the state of the job _after_ the proposed operation would be completed—as evidence that the operation is _already_ complete. This logical fallacy leads the model to erroneously discard a feasible candidate action. The example demonstrates the brittleness of the model’s ability to map state descriptors to their correct temporal context, a foundational challenge for reliable decision-making. 

While redesigning state descriptors to distinguish between current status and post-action predictions might seem like a viable solution to prevent such conflations, the failure observed here is structural rather than merely linguistic. The tendency of the model to misinterpret predicted metrics as historical facts reflects an inherent limitation in maintaining a consistent temporal context during one-step generation. ReflecSched addresses this challenge by providing Strategic Experience to serve as a top-down interpretive framework. This mechanism ensures that the model focuses on the strategic implications of a state, such as the potential to complete a critical job, instead of being misled by the semantic ambiguity of raw numerical descriptors. 

## _Appendix B.3. Inconsistent Adherence to Procedural Rules_ 

_Prompt Context._ The prompt includes an explicit, highpriority rule for handling emergency jobs. At timestamp _t_ = 11.415, the arrival of an emergency job creates a critical test of the model’s ability to reliably apply this conditional instruction, particularly when presented with competing non-emergency options. 

- The “Emergency Jobs” list now contains “[6]”. 

- The “Ready Operations” list includes “Job 6 Operation 1 [EMERGENCY]” with three machine options. 

- A non-emergency operation, “Job 3 Operation 4”, is also available. 

- Contradictory/Incorrect Responses (2 out of 5): Two responses exhibited confused reasoning. One’s rationale is presented below. 

<mark>Reasoning: First, I check for emergency jobs. Job 6 Operation 1 is marked as emergency...</mark> **<mark>However, the candidate actions list only includes non-emergency operations.</mark>** <mark>This is a contradiction...</mark> 

This assertion is factually incorrect, as the emergency job is explicitly listed in the “Candidate Actions” JSON block. The model has thus failed to correctly parse the provided context, leading it to generate a spurious contradiction. 

_Analysis._ This case demonstrates a critical failure mode: the unreliable application of explicit, highpriority rules. Even when presented with a straightforward directive, the model’s reasoning process is shown to be inconsistent across multiple generation attempts. The generation of a factually incorrect, selfcontradictory rationale reveals a significant vulnerability. While a majority voting mechanism might salvage the correct final decision in this instance, the flawed and unpredictable nature of the underlying reasoning process is exposed. This unreliability is unacceptable in operational settings where consistent adherence to critical constraints is paramount. This finding underscores that smaller-scale models cannot be reliably tasked with executing critical operational policies without a more robust, structured guiding framework. 

The ReflecSched framework systematically mitigates the inconsistent rule adherence observed in this case study through its hierarchical architecture. While smaller models in the LLM-Direct baseline may generate contradictory rationales or overlook high-priority labels, ReflecSched implements a robust fallback and validation protocol. At each decision point, the candidate actions are filtered by the environment kernel to ensure they comply with technological constraints. If the model’s output is found to be inconsistent with the set of feasible, high-priority actions, the framework utilizes a majority-voting scheme and a heuristic-driven tie-break 

23 

mechanism to restore the correct decision path. Additionally, the periodic invocation of the reflection module upon the arrival of an emergency job forces the model to re-evaluate its strategy based on the most recent evidence, thereby reinforcing the high-priority rules in the Strategic Experience prompt. 

## **Appendix C. Experimental Protocol for the PDR Application Analysis** 

This appendix provides a detailed description of the experimental protocol used to assess the LLM-Direct baseline’s ability to apply heuristics, evaluated on our diagnostic PDR-Bench dataset. 

## _Appendix C.1. Experimental Objective_ 

The primary objective of this experiment is to quantitatively assess the LLM’s ability to apply externally provided heuristics, Priority Dispatching Rules (PDRs), to its decision-making process. The PDR-Bench dataset is specifically designed for this purpose, as each instance has a single, empirically best-performing PDR. The experiment tests the hypothesis that when the model is explicitly prompted with the best-performing rule for an instance, its performance should converge towards that of the rule itself. 

## _Appendix C.2. Experimental Conditions_ 

To test this hypothesis, we evaluated the LLM-Direct baseline under three distinct prompting conditions: 

- **LLM-Direct:** In this standard condition, the prompt contains no information about any PDRs. The model must rely solely on its pre-trained knowledge and the provided state information. 

- **All-PDRs:** In this condition, the prompt is augmented with a list of all 24 PDR combinations. The model is instructed that it may use these rules for guidance but is not explicitly required to do so. 

- **Single-Best-PDR:** In this condition, for each instance in PDR-Bench, the prompt is augmented with only the single, specific PDR known to yield the best makespan. This condition provides the model with the most direct and unambiguous guidance, thereby isolating its ability to follow a single, targeted instruction. 

## _Appendix C.3. Prompt Augmentation for Heuristics_ 

The PDRs are integrated into the prompt as a distinct, clearly demarcated section. For each rule, the prompt provides its acronym (e.g., SPT), a full name, a precise selection criterion, and the strategic rationale for its use. This structure is designed to give the model all the necessary information to understand and potentially apply the heuristic. The following excerpt illustrates the format and instructional language used. 

|... (previous prompt sections: State, Ready<br>Ops, etc.) ...|
|---|
|# Priority Scheduling Rules|
|Below are the ‘‘Operations Priority Scheduling|
|Rules’’ and ‘‘Machines Priority|
|Scheduling Rules’’. You can choose to use|
|these rules for scheduling, but it is NOT<br>required.|



|## Operations|Priority Scheduling Rules|
|---|---|
|SPT (Shortest|Processing Time):|
|Criterion|: Choose the candidate with the|
|smallest|‘min_pt‘.|
|Rationale|: Selecting the operation whose|
|shortest|possible processing time is|
|minimal r|educes average flow time and|
|keeps mac<br>.|hines busy with quick tasks first|



<mark>## Machines Priority Scheduling Rules LIT (Least Idle Time): Criterion: Among candidate machines, choose the one with the smallest ‘free until time‘. Rationale: Favors machines that free up next, keeping resources continuously occupied.</mark> 

- <mark>... (subsequent prompt sections: Candidate Actions, Instructions, etc.) ...</mark> 

## **Appendix D. Benchmark Generation and Curation Methodology** 

The empirical evaluation in this study relies on two benchmark suites, GEN-Bench and PDR-Bench, which were generated for this work. These datasets were not randomly selected; rather, they were systematically curated from a large, procedurally generated pool of DFJSP instances to serve specific analytical purposes. This appendix details the formal methodology for their generation and subsequent curation. 

## _Appendix D.1. Instance Generation_ 

To create a diverse and challenging pool of problems, we developed a parameterized instance generator that 

24 

allows for fine-grained control over both the static and dynamic characteristics of the DFJSP instances. The key generation parameters are summarized in Table D.1. 

Table D.1: Parameter ranges for instance generation at Normal and Small scales. 

|**Parameter**|**Normal Scale**|**Small Scale**|
|---|---|---|
|_Static Characteristics_|||
|Number of Jobs|[15, 20]|[3, 5]|
|Operations per Job|[2, 4]|[2, 4]|
|Number of Machines|[3, 5]|[3, 5]|
|Candidate Machines per Op.|[1, 3]|[1, 3]|
|Processing Time Range|[1.0, 5.0]|[1.0, 3.0]|
|_Dynamic Event Characteristics_|||
|Emergency Jobs per Instance|1|1|
|Machine Failure Probability|0.5|0.3|
|Job Cancellation Probability|0.3|0.2|



The generation process for each instance is as follows: 

- **Static Structure** : The generator first defines the static topology of the problem by sampling the number of jobs, machines, and operations per job from the uniform integer ranges specified in Table D.1. For each operation, a set of candidate machines is randomly sampled. A base processing time is drawn from a uniform distribution, with an additional perturbation factor (±20%) applied to model machine-specific efficiency differences. 

- **Dynamic Events** : A set of dynamic events is introduced to ensure a high degree of problem dynamism. Job arrival times are sampled from the first half of the simulation horizon to ensure significant system load during the early stages. Machine breakdown events are generated stochastically for each machine based on a specified failure probability. The duration of each repair is drawn from a uniform distribution U(1.0, 4.0). Similarly, job cancellations and the arrival of new, high-priority emergency jobs are introduced based on their respective probabilities. 

- **Adaptive Horizon** : The total simulation horizon for each instance is not fixed but is calculated dynamically. It is based on a simple makespan lower bound estimate (total processing work of all initial jobs divided by the machine count), which is then multiplied by a buffer factor (1.2). This ensures that the horizon is sufficiently long to accommodate the completion of all tasks and dynamic events. 

This generator was used to create an initial pool of 200 instances for each problem scale, which subsequently served as the input for our curation processes. 

## _Appendix D.2. PDR-Bench: The Diagnostic Heuristic Benchmark_ 

_Goal._ The primary objective of PDR-Bench is to generate a diagnostic dataset of problem instances where, for each instance, a single PDR demonstrably outperforms all others. This design creates an unambiguous ground truth, enabling a clear, quantitative assessment of an LLM’s ability to apply a specific, demonstrably superior heuristic when prompted. 

_Methodology._ The curation process begins with a large, diverse set of generated DFJSP instances. For each instance _I_ , we first simulate its scheduling process using every individual PDR from a predefined set of rules R. Let _M_ ( _I_ , _r_ ) denote the final makespan achieved on instance _I_ using rule _r_ ∈R. An instance _I_ is selected for inclusion in PDR-Bench if and only if there exists a single, uniquely dominant heuristic. Formally, we first identify the best-performing rule _r_<sup>∗</sup> for the instance: 



The instance _I_ is then included in the benchmark if this minimum is unique. That is, the makespan of the bestperforming rule must be strictly better than that of any other rule in the set: 



This filtering process yields a collection of problem instances, each of which is constructed to have a single, empirically dominant heuristic. This establishes a clear and objective ground truth for our subsequent analysis of the LLM’s heuristic application capabilities. 



_Goal._ The objective of GEN-Bench is to curate a general-purpose benchmark that is demonstrably fair and unbiased. This is achieved by satisfying two competing criteria: (1) each individual instance should be challenging and capable of discriminating between the performance of different rules (high discrimination), and (2) the dataset as a whole should not exhibit a systemic bias towards any particular rule (high global balance). 

25 

_Methodology._ The curation of GEN-Bench is framed as a multi-objective optimization problem, which we address using a greedy selection algorithm. The process involves quantifying two key statistical properties: instance-level discrimination and subset-level global balance. 

_Instance-Level Discrimination._ For each candidate instance _I_ , we measure its ability to discriminate between the performances of different rules. Let P _I_ = { _M_ ( _I_ , _r_ ) | _r_ ∈R} be the set of makespan results for instance _I_ across all rules in the set R. We compute a composite Discrimination Score, _Disc_ ( _I_ ), as a weighted sum of five normalized statistical dispersion metrics. A higher _Disc_ ( _I_ ) indicates that the instance is more effective at highlighting performance differences between scheduling strategies. The components are defined as follows: 

**1. Coefficient of Variation (CV).** This metric provides a scale-invariant measure of dispersion. Let µ(P _I_ ) and σ(P _I_ ) be the mean and standard deviation of the makespans in P _I_ . 



**Final Composite Score.** The five metrics are normalized to a commensurable “[0, 1]” scale and then combined in a weighted sum to form the final discrimination score, _Disc_ ( _I_ ). We define a scaling function ϕ _c_ ( _x_ ) = min( _x_ , _c_ )/ _c_ to cap and normalize a value _x_ with a constant _c_ . The final score is calculated as: 



where the weights ( _wcv_ , _wrange_ , _wiqr_ , _wH_ , _wpair_ ) are set to (0.25, 0.20, 0.20, 0.15, 0.20). The entropy term _H_ ( _I_ ) is already normalized. 

_Subset-Level Global Balance._ For any subset of instances S, we measure its global balance to assess if the subset, as a whole, is biased towards any particular rule. Let _M_<sup>¯</sup> ( _r_ , S) be the average performance of rule _r_ across all instances in S. Let P<sup>¯</sup> S = { _M_<sup>¯</sup> ( _r_ , S) | _r_ ∈R} be the set of these average performances. The global balance is then defined as: 



**2. Relative Range.** This captures the maximum performance spread relative to the mean. 



**3. Relative Interquartile Range (IQR).** A robust measure of the spread of the central 50% of the data [69]. Let _Q_ 1(P _I_ ) and _Q_ 3(P _I_ ) be the first and third quartiles. 



**4. Entropy of Performance Ranks.** This quantifies the diversity of the performance ordering [70]. Let _pk_ be the proportion of rules achieving rank _k_ . The normalized Shannon entropy is: 



**5. Average Pairwise Relative Difference.** This assesses the average separation between all pairs of rule performances. 



A balance score close to 1 indicates that, on average, all PDRs perform similarly on the selected dataset, making it a fair and unbiased benchmark. 

_Greedy Selection Algorithm._ With these metrics defined, GEN-Bench is curated via a greedy algorithm. Starting with an empty set S0, the algorithm iteratively adds the instance _I_<sup>∗</sup> from the pool of remaining candidates that maximizes a weighted objective function. At each step _k_ , this function combines the average discrimination of the new set, its global balance, and the diversity of instance types: 



## **Appendix E. Prompt Architecture and Design** 

This appendix provides a detailed description of the architecture of the two core prompts used in this work: the **Decision Prompt** and the **Reflection Prompt** . These prompts are programmatically constructed at runtime, assembling information from the simulation environment according to a predefined structure. 

26 

## _Appendix E.1. The Decision Prompt_ 

The Decision Prompt is the primary interface for eliciting a scheduling decision from an LLM. It is engineered to provide a structured, textual representation of the current shop-floor state, enabling the model to make a single, immediate scheduling choice. This prompt’s architecture is shared by both the LLM-Direct baseline and the Experience-Guided Decision-Making (EGDM) module within ReflecSched. The key difference between the two applications is the inclusion of the “Strategic Experience” component, which is present only for the EGDM module. 

The prompt is composed of several modular information blocks, assembled hierarchically to guide the model’s reasoning. 

<mark>You are an expert scheduler in a dynamic factory. Your goal is to make smart, forward-looking decisions to keep the factory running smoothly and finish all jobs as early as possible (minimize makespan).</mark> 

- <mark># Primary Objective Choose the *single best* operation-machine pair to schedule right now. A good decision balances short-term gains with long-term risks.</mark> 

<mark># Key Information to Consider</mark> 

<mark>{Ready Operations}</mark> 

<mark># Candidate Actions (only these are allowed) ‘‘‘json {actions_json}</mark> 

<mark>‘‘‘</mark> 

- <mark># Task: Make a Decision</mark> 

- <mark>Think step-by-step. Your reasoning should balance these factors:</mark> 

<mark>1. **</mark><sup><mark>Urgency</mark></sup> <mark>**</mark><sup><mark>:Handle‘[EMERGENCY]‘jobs</mark></sup> <mark>first.</mark> 

<mark>2. **</mark><sup><mark>Constraints</mark></sup> <mark>**</mark><sup><mark>:Anoperationwithlow‘</mark></sup> <mark>flexibility‘ (e.g., 1) is a constraint. Clearing it might unlock more options.</mark> 

<mark>3. **</mark><sup><mark>Bottlenecks</mark></sup> <mark>**</mark><sup><mark>:Isthemachineyouare</mark></sup> <mark>choosing a high-‘contention‘ resource? If so, is this operation important enough to occupy it? Could a more flexible operation go to a less contended machine?</mark> 

<mark>4. **</mark><sup><mark>Flow</mark></sup> <mark>**</mark><sup><mark>:Doesschedulingalong-‘rem_work</mark></sup> <mark>‘ job now prevent it from becoming a problem later? Or is it better to clear a quick job to speed up the flow?</mark> 

- <mark>Based on your analysis, provide your final decision in JSON format.</mark> 

<mark>‘‘‘json {{"job": <int>, "op": <int>, "machine": <int >}} ‘‘‘</mark> 

<mark>1. **</mark><sup><mark>CurrentTimestamp</mark></sup> <mark>**</mark><sup><mark>:{snapshot[’</mark></sup> <mark>timestamp’]}</mark> 

<mark>2. **</mark><sup><mark>MachineStates</mark></sup> <mark>**</mark><sup><mark>:</mark></sup> 

   - <mark>‘status‘: Is the machine available or</mark> 

   - <mark>broken?</mark> 

   - <mark>‘contention‘: How many *future*</mark> 

   - <mark>operations need this machine? A high contention machine is a future bottleneck. **</mark><sup><mark>Avoidoccupyingahigh-contention</mark></sup> 

   - <mark>machine with a non-critical or flexible task.**</mark> 

<mark>3. **</mark><sup><mark>ReadyOperations</mark></sup> <mark>**</mark><sup><mark>:</mark></sup> 

   - <mark>‘est‘: When can this operation *actually</mark> 

   - <mark>*</mark><sup><mark>start?</mark></sup> <mark>- ‘rem_work‘: How much work is left for this job? High ‘rem_work‘ jobs might need to start sooner.</mark> 

   - <mark>‘flexibility‘: How many machine options</mark> 

   - <mark>does this operation have? An operation with ‘flexibility: 1‘ is a critical constraint and may need to be prioritized to avoid it getting stuck.</mark> 

   - <mark>‘[EMERGENCY]‘: These jobs MUST be</mark> 

   - <mark>scheduled before any non-emergency job.</mark> 

_Core Components of the Decision Prompt._ 

- **Role and Objective:** The prompt begins by assigning the LLM the role of an “expert scheduler” and clearly states the primary objective (e.g., minimize makespan). 

- **Glossary and Strategic Guide:** This section defines key operational metrics (e.g., machine contention, operation flexibility) to ensure consistent interpretation by the LLM and provides high-level advice on balancing competing objectives. 

- **Machine States:** A summary of each machine’s status, including its current availability (i.e., when it will be free) and a calculated contention level—a metric representing the number of future operations competing for that resource. 

<mark>{Machines States}</mark> 

<mark>{Emergency Jobs}</mark> 

<mark>{Strategic Experience}</mark> 

- **Emergency Jobs:** A list identifying any jobs currently designated with emergency status, which must be prioritized. 

27 

- **Ready Operations:** A catalog of all currently schedulable operations. For each operation, this section summarizes key attributes such as its earliest start time, shortest possible processing time, the remaining work in its parent job, and its scheduling flexibility (i.e., the number of candidate machines). 

- **Candidate Actions:** A machine-readable, JSONformatted list enumerating all feasible (job, operation, machine) scheduling actions. This serves as a strict output schema, constraining the LLM’s final output to a valid and directly executable format. 

- **Task Instructions:** A set of explicit instructions guiding the LLM’s final reasoning process, prompting the model to balance the various informational components before committing to a final decision. 

## _Conditional Component for EGDM._ 

- **Strategic Experience:** (Included only for the EGDM module) This component inserts the core strategic guidance synthesized by the Hierarchical Reflection Module. This natural-language principle, enclosed in <key_insights> tags, is the primary input for informing the LLM’s nonmyopic reasoning. 

## _Appendix E.2. The Reflection Prompt_ 

The Reflection Prompt serves a fundamentally different function from the Decision Prompt. It does not request an immediate scheduling action. Instead, it is engineered to instruct the LLM to act as a strategic analyst, tasked with synthesizing a new, more refined strategic principle based on a comparative analysis of simulated outcomes. 

- <mark>You are a master Scheduling Strategist. Your mission is to analyze different simulated futures (rollout paths) to **REFINE and UPDATE** a generalizable strategic principle.</mark> 

<mark>{The Existing Strategic Principle} {The Originating Decision-Point State} {Summarized Simulation Outcomes}</mark> 

<mark># Analysis and Synthesis Task Your task is to integrate the **New Evidence** with the **Previous Experience**.</mark> 

<mark>1. **</mark><sup><mark>AnalyzetheDecisionPaths</mark></sup> <mark>**</mark><sup><mark>:Lookat</mark></sup> <mark>the "Best Path" and "Worst/Alternative Path". What is the key difference in their *</mark><sup><mark>initialdecisions</mark></sup> <mark>*</mark><sup><mark>?Whydidstarting</mark></sup> 

<mark>with the better initial decision lead to a better overall makespan? Did it unblock a critical machine earlier? Did it</mark> 

<mark>prioritize a job with more work remaining? Look beyond just the first step and</mark> 

<mark>consider how it affected the sequence.</mark> 

<mark>2. **</mark><sup><mark>SynthesizeaNewStrategy</mark></sup> <mark>**</mark><sup><mark>:</mark></sup> <mark>* **</mark><sup><mark>EvaluateNewvs.Old</mark></sup> <mark>**</mark><sup><mark>:Howdoesthe</mark></sup> <mark>insight from your path analysis relate to the ‘Previous Experience‘? Does it **</mark> 

<mark>CONFIRM** the old strategy (e.g., "The SPT rule worked again")? Does it **CONTRADICT</mark> 

<mark>**</mark><sup><mark>it(e.g.,"SPTwasbadhere,</mark></sup> <mark>prioritizing a job with more remaining work (MWKR) was better")? Or does it **ADD NUANCE** (e.g., "SPT is good, but only if it doesn’t starve a critical machine that another job needs next").</mark> 

   - <mark>**</mark><sup><mark>FormulatetheUpdatedInsight</mark></sup> <mark>**</mark><sup><mark>:</mark></sup> 

   - <mark>Create a single, robust strategic principle for the next decision. **Do not simply list old and new rules.** Synthesize them into one superior, more general rule.</mark> 

- <mark># Output Requirements Provide your analysis in the following XMLstyle tags. Be concise and focus on the final, actionable insights.</mark> 

<mark>‘‘‘xml <comparison_summary> (Your brief analysis comparing the decision paths, explaining the "why".) </comparison_summary></mark> 

<mark><key_insights> (Your **NEW, REFINED, and SYNTHESIZED** strategic principle. This is the key output.) </key_insights> ‘‘‘</mark> 

## _Key Components of the Reflection Prompt._ 

- **Role Assignment:** The LLM is instructed to act as a “Scheduling Strategist.” Its stated task is to refine and update an existing scheduling policy, in contrast to the single-action task of the Decision Prompt. 

- **The Existing Strategic Principle:** This block presents the current natural-language strategy (the “Strategic Experience”) that was used to guide the initial heuristic-driven simulations, thereby providing the context for the refinement task. 

28 

- **The Originating Decision-Point State:** This component provides a full description of the system state at the moment the simulations were initiated. This information allows the LLM to ground its analysis of the simulation outcomes in the specific trade-offs and conditions that were present. 

- **Summarized Simulation Outcomes:** This is the primary data for analysis. It presents a concise comparison of the best- and worst-performing simulated trajectories, highlighting their final makespans and, crucially, the divergent initial decision paths that produced these outcomes. 

- **A Structured Reasoning Guide:** This section provides an explicit, two-stage set of instructions. First, it directs the LLM to analyze the causal relationship between the initial decision paths and the final outcomes. Second, it instructs the model to synthesize the insights from this analysis into a new, more robust strategic principle, potentially by refining or replacing the previous one. 

- **A Strict Output Schema:** The prompt requires the LLM to structure its response using two specific XML-style tags: <comparison_summary> for its analytical reasoning, and <key_insights> for the final, synthesized strategic principle. This structured output is essential for the framework to programmatically extract and subsequently utilize the new “Strategic Experience”. 

## **Appendix F. Data for Motivational Analysis Example** 

This appendix provides the complete problem instance data corresponding to the motivating example discussed in Section 4.3 and illustrated in Figure 1. Table F.1 details the candidate machines and corresponding processing times for each operation, derived directly from the schedule visualisations. 

## **Appendix G. Granular Performance Records for Per-Instance Comparative Analysis** 

This appendix provides the complete record of raw performance results for every problem instance across the three benchmarking suites evaluated in this study, enabling a transparent comparison between ReflecSched and all baseline algorithms. 

Table F.1: Processing time data for the illustrative example in Figure 1. The pairs ( _Mk_ , _p_ ) indicate that machine _k_ can process the operation in _p_ time units. 

|**Job**|**Operation**|**Candidate Machines & Processing Times**|
|---|---|---|
||_O_1,1|(_M_2,1.90),(_M_3,1.34)|
|Job 1|_O_1,2|(_M_3,1.98)|
||_O_1,3|(_M_2,1.98)|
||_O_2,1|(_M_1,1.59),(_M_2,2.62)|
|Job 2|_O_2,2<br>_O_2,3|(_M_2,1.71)<br>(_M_1,1.94),(_M_2,1.20)|
||_O_2,4|(_M_1,0.96)|
|Job 3|_O_3,1|(_M_1,1.08)|
||_O_3,2|(_M_3,2.22)|



## **Appendix H. Hyperparameter Settings** 

This appendix delineates the comprehensive hyperparameter configurations and architectural specifications utilized for the empirical evaluation of ReflecSched and the corresponding baselines. 

## **References** 

- [1] S. Li, W. Ouyang, Y. Ma, C. Wu, Learningguided rolling horizon optimization for longhorizon flexible job-shop scheduling, CoRR abs/2502.15791 (2025). arXiv:2502.15791, doi:10.48550/ARXIV.2502.15791. URL https://doi.org/10.48550/arXiv.2502.15791 

- [2] S. Cao, R. Li, W. Gong, C. Lu, Inverse model and adaptive neighborhood search based cooperative optimizer for energy-efficient distributed flexible job shop scheduling, Swarm and Evolutionary Computation 83 (2023) 101419. 

- [3] C. Ferreira, G. Figueira, P. Amorim, Effective and interpretable dispatching rules for dynamic job shops via guided empirical learning, Omega 111 (2022) 102643. 

- [4] M. Xu, Y. Mei, F. Zhang, M. Zhang, Learn to optimise for job shop scheduling: a survey with comparison between genetic programming and reinforcement learning, Artificial Intelligence Review 58 (6) (2025) 1–53. 

- [5] C. Zhang, W. Song, Z. Cao, J. Zhang, P. S. Tan, X. Chi, Learning to dispatch for job shop scheduling via deep reinforcement learning, Advances in neural information processing systems 33 (2020) 1621–1632. 

29 

Table G.1: Comparative results of Makespan RPD (%) across different problem scales on GEN-Bench. Relative Percentage Deviation (RPD) values are expressed as percentages. Bold values indicate the best performance for each instance across all evaluated methods. 

|**Instance**||**Base**|**line Meth**|**ods**||||**Refle**|**lcSched (P**|**l roposed)**|||
|---|---|---|---|---|---|---|---|---|---|---|---|---|
||GP|HMPSAC|IDDQN|DAN|PPO-OC|Q3-8b|Q3-14b|Q3-32b|DS-V3|DS-V3.2|GPT-4o|GPT-5n|
|Small-1|74.19|11.07|12.48|32.99|34.88|20.29|10.68|0.51|13.66|**0.00**|2.21|**0.00**|
|Small-2|23.47|28.21|28.21|7.12|15.88|2.17|7.66|9.21|7.66|**0.00**|7.66|7.66|
|Small-3|98.11|23.97|1.96|22.54|25.95|**0.00**|6.39|10.60|10.60|10.60|10.60|10.60|
|Small-4|58.65|10.15|33.63|**0.00**|9.59|5.13|4.33|1.82|4.73|21.88|1.22|10.54|
|Small-5|25.86|17.74|19.34|35.76|35.76|6.97|**0.00**|19.23|10.75|9.43|9.43|9.43|
|Small-6|43.96|7.60|19.76|8.06|11.99|9.20|**0.00**|4.59|4.33|7.59|9.20|9.20|
|Small-7|40.63|**0.00**|11.75|6.52|6.52|16.50|9.36|15.43|16.73|24.95|16.49|20.42|
|Small-8|19.90|17.63|28.28|7.80|16.76|4.23|0.15|**0.00**|4.00|0.76|3.62|0.76|
|Small-9|29.12|21.24|6.79|6.79|2.63|1.76|1.22|3.14|1.76|**0.00**|2.63|6.79|
|Small-10|13.53|**0.00**|**0.00**|**0.00**|12.63|16.04|26.22|2.81|13.80|10.95|17.48|26.22|
|Small-11|36.07|9.18|13.53|**0.00**|4.15|16.09|16.06|21.05|21.34|21.05|21.05|21.05|
|Small-12|28.70|17.47|5.31|6.21|**0.00**|4.60|0.95|7.17|3.72|12.42|3.08|3.08|
|Small-13|46.35|**0.00**|13.64|9.20|12.75|16.42|3.98|7.21|7.21|7.21|8.83|7.21|
|Small-14|1.72|3.92|6.35|**0.00**|7.72|8.57|3.93|3.93|3.93|3.93|3.93|3.93|
|Small-15|12.07|**0.00**|4.94|28.44|7.28|3.87|5.94|1.29|**0.00**|**0.00**|2.58|**0.00**|
|Small-16|59.52|**0.00**|20.07|20.07|24.93|14.38|15.43|7.24|13.59|11.03|12.72|12.84|
|Small-17|32.55|14.90|14.23|22.92|35.83|2.42|**0.00**|3.96|0.62|16.57|3.06|3.75|
|Small-18|55.27|29.09|**0.00**|23.68|42.22|4.24|4.24|4.24|5.86|9.10|4.24|4.24|
|Normal-1|51.78|15.19|26.14|8.34|11.38|4.61|**0.00**|13.97|9.11|4.79|4.45|5.48|
|Normal-2|60.73|16.79|5.13|**0.00**|6.77|4.14|7.29|4.37|3.35|4.73|1.98|16.72|
|Normal-3|73.72|8.01|**0.00**|10.39|17.73|4.70|4.83|8.01|6.58|4.62|6.57|1.97|
|Normal-4|46.75|3.89|2.36|4.63|1.38|**0.00**|5.25|7.07|7.82|6.18|8.77|6.18|
|Normal-5|46.89|9.45|**0.00**|4.28|5.15|1.21|2.29|8.59|5.30|0.15|3.70|2.48|
|Normal-6|55.35|1.26|3.14|**0.00**|5.02|0.91|0.87|4.38|1.25|14.83|3.87|16.16|
|Normal-7|94.23|19.61|6.59|6.04|9.23|6.30|5.97|6.93|7.30|**0.00**|6.37|3.68|
|Normal-8|95.64|13.98|7.58|4.58|**0.00**|3.62|3.58|4.84|0.62|2.14|4.27|8.80|
|Normal-9|50.58|5.35|0.05|0.31|6.08|2.87|**0.00**|0.06|3.76|6.72|7.30|3.52|
|Normal-10|47.94|12.83|12.28|25.88|17.60|15.53|8.13|8.67|10.69|9.80|21.38|**0.00**|
|Normal-11|46.58|17.55|15.34|3.66|7.27|11.56|12.56|9.26|6.59|8.58|7.52|**0.00**|
|Normal-12|129.32|23.97|11.08|13.41|2.78|5.84|6.90|2.09|4.79|3.67|**0.00**|4.39|
|Normal-13|75.27|**0.00**|11.70|9.71|7.92|8.57|5.45|8.14|6.55|14.86|6.71|4.00|
|Normal-14|27.44|1.62|0.42|12.29|5.27|4.45|**0.00**|9.57|13.03|0.20|12.09|26.26|
|Normal-15|74.02|7.69|2.42|9.67|11.31|4.47|6.13|4.83|2.39|9.41|8.47|**0.00**|
|Normal-16|79.02|18.33|17.61|**0.00**|23.35|2.63|7.62|4.58|14.66|1.86|1.51|7.49|
|Normal-17|52.80|**0.00**|3.62|10.13|13.36|3.90|3.95|9.30|2.52|9.40|4.64|13.15|
|Normal-18|38.77|12.95|9.25|16.26|13.87|1.56|8.10|2.59|2.64|10.65|**0.00**|3.28|
|Normal-19|110.60|9.77|7.95|**0.00**|20.28|16.14|11.82|11.04|18.47|13.95|12.24|11.08|
|Normal-20|127.35|7.62|14.05|30.47|18.68|7.85|14.18|9.17|12.87|**0.00**|9.41|12.92|
|**Average**|54.85|11.00|10.45|10.74|13.47|6.94|**6.09**|6.87|7.49|7.74|7.14|8.03|



30 

Table G.2: Makespan RPD (%) performance comparison on the established MK-Bench (Brandimarte-based). RPD values are expressed as percentages to underscore the performance variance. Bold values indicate the best performance for each instance across all evaluated methods. 

|**Instance**||**Base**|**line Meth**|**ods**|||**Reflec**|**lSched (P**|**l roposed)**||
|---|---|---|---|---|---|---|---|---|---|---|
||GP|HMPSAC|IDDQN|DAN|PPO-OC|Q3-8b|Q3-14b|Q3-32b|DS-V3.2|GPT-5n|
|MK01|27.76|2.84|2.63|18.68|**0.00**|5.05|10.68|7.32|15.95|7.39|
|MK02|16.93|12.67|9.40|9.46|28.15|17.32|30.32|34.32|**0.00**|12.67|
|MK03|45.19|12.02|27.47|26.44|21.15|8.17|40.38|44.71|**0.00**|23.56|
|MK04|123.64|3.34|10.16|4.02|3.76|1.74|7.11|0.70|**0.00**|10.16|
|MK05|25.71|25.79|7.63|9.09|3.35|11.79|**0.00**|14.14|3.47|6.25|
|MK06|147.97|22.42|17.22|28.05|29.73|12.49|15.66|9.33|**0.00**|9.33|
|MK07|64.92|17.44|19.30|23.03|45.40|39.18|**0.00**|10.90|1.28|32.31|
|MK08|7.72|6.10|6.25|23.46|7.29|**0.00**|9.74|9.43|20.13|5.96|
|MK09|21.80|21.49|13.68|11.51|17.77|4.88|29.11|**0.00**|18.70|13.68|
|MK10|76.36|19.06|4.71|24.35|2.49|2.36|**0.00**|7.46|8.80|10.61|
|**Average**|55.80|14.32|11.85|17.81|15.91|10.30|14.30|13.83|**6.83**|13.19|



Table G.3: Makespan RPD (%) performance comparison on JMS-Bench. RPD values are expressed as percentages to highlight subtle performance variations. Bold values indicate the best performance for each instance across all evaluated methods. All ReflecSched variants utilize the hierarchical reflection mechanism. 

|**Instance**||**Base**|**line Meth**|**ods**|||**Reflec**|**lSched (Pr**|**l oposed)**||
|---|---|---|---|---|---|---|---|---|---|---|
||GP|HMPSAC|IDDQN|DAN|PPO-OC|Q3-8b|Q3-14b|Q3-32b|DS-V3.2|GPT-5n|
|instance_01|25.58|**0.00**|6.47|20.51|3.67|9.30|14.88|3.67|14.88|2.55|
|instance_02|77.49|4.36|3.05|13.55|4.03|1.81|3.72|**0.00**|0.84|0.27|
|instance_03|30.69|0.70|**0.00**|3.53|7.72|11.66|5.31|9.95|18.27|10.50|
|instance_04|61.76|11.03|13.15|32.18|32.88|12.97|**0.00**|10.21|11.76|13.15|
|instance_05|62.60|19.04|5.01|20.33|11.79|**0.00**|9.35|11.79|8.88|22.90|
|instance_06|31.25|12.50|3.13|9.72|**0.00**|6.25|12.50|12.50|6.25|7.84|
|instance_07|7.20|**0.00**|1.70|18.20|15.50|9.95|2.75|3.38|3.93|0.80|
|instance_08|45.05|20.51|15.49|**0.00**|11.72|7.79|5.31|9.15|7.69|14.28|
|instance_09|78.09|10.69|13.38|18.73|12.90|4.96|**0.00**|10.63|5.29|10.36|
|instance_10|48.30|18.33|18.70|18.88|9.17|**0.00**|7.97|6.11|7.24|18.91|
|**Average**|46.80|9.72|8.01|15.56|10.94|6.47|**6.18**|7.74|8.50|10.16|



31 

Table H.1: Hyperparameter configurations for the baselines and the proposed ReflecSched. 

|**Algorithm**|**Parameter**|**Value**|
|---|---|---|
||Training Episodes|2,000|
|**IDDQN**|Learning Rate / Discount Factor (γ)<br>Batch Size (_B_) / Buffer Size<br>Exploration / PER (α, β)<br>Target Network Update Interval|0.01 / 0.9<br>_Osum_ / 10×_Osum_<br>ϵ-greedy / 0.6, 0.4<br>Every_Osum_ steps|
|**PPO-OC / DAN**|Learning Rate / Clipping Rate (ϵ)<br>Value (_cv_) / Entropy (_ce_) Loss Coef.<br>GAE (λ)<br>PPO Update Epochs (_K_)|3×10<sup>−4 </sup>/ 0.2<br>0.5 / 0.01<br>0.95 (PPO), 0.98 (DAN)<br>10 (PPO), 4 (DAN)|
||Training Episodes|1,000|
|**HMPSAC**|Learning Rate / Discount Factor (γ)<br>Value (_cv_) / Entropy (_ce_) Loss Coef.<br>Max Decision Steps per Episode|3×10<sup>−4 </sup>/ 0.99<br>0.5 / 0.01<br>10,000|
||Inference Temperature (_Tinf_) / Top-_p_<br>Top-_k_/ Max Tokens<br>Reasoning Protocol<br>Rollout Expansion Factor (_Nroll_)<br>Maximum Search Depth (_Lmax_)|0.2 / 0.8<br>20 / 8,192<br>Reflective (Non-thinking)<br>24<br>6|
|**ReflecSched**|Search Iterations (_Niter_)|3|
||Search Sampling Temperature (_Tsearch_)<br>Dynamic Gantt Information / Static Data|0.8<br>Enabled / Disabled|



- [6] C. Ngwu, Y. Liu, R. Wu, Reinforcement learning in dynamic job shop scheduling: a comprehensive review of ai-driven approaches in modern manufacturing, Journal of Intelligent Manufacturing (2025) 1–16. 

- [7] H. Abgaryan, A. Harutyunyan, T. Cazenave, Llms can schedule, CoRR abs/2408.06993 (2024). arXiv:2408.06993, doi:10.48550/ARXIV.2408.06993. URL https://doi.org/10.48550/arXiv.2408.06993 

- [8] A. Baykaso˘glu, F. S. Madeno˘glu, A. Hamzadayı, Greedy randomized adaptive search for dynamic flexible job-shop scheduling, Journal of Manufacturing Systems 56 (2020) 425–451. 

- [9] W. Ren, Y. Yan, Y. Hu, Y. Guan, Joint optimisation for dynamic flexible job-shop scheduling problem with transportation time and resource constraints, International Journal of Production Research 60 (18) (2022) 5675–5696. 

- [10] M. Shahgholi Zadeh, Y. Katebi, A. Doniavi, A heuristic model for dynamic flexible job shop scheduling problem considering variable processing times, International Journal of Production Research 57 (10) (2019) 3020–3035. 

- [11] X. Li, A. Guo, X. Yin, H. Tang, R. Wu, Q. Zhao, Y. Li, X. Wang, A q-learning improved differential evolution algorithm for human-centric dynamic distributed flexible job shop scheduling problem, Journal of Manufacturing Systems 80 (2025) 794– 823. 

- [12] X. Chen, J. Li, Z. Wang, Q. Chen, K. Gao, Q. Pan, Optimizing dynamic flexible job shop scheduling using an evolutionary multi-task optimization framework and genetic programming, IEEE Transactions on Evolutionary Computation (2025). 

- [13] S. Yang, H. Guo, J. Huang, K. Han, A deep reinforcement learning based approach for dynamic job shop scheduling considering variable processing time, in: Proceedings of the 2024 4th International Conference on Artificial Intelligence, Automation and High Performance Computing, 2024, pp. 368–374. 

- [14] R. Liu, R. Piplani, C. Toro, A deep multi-agent reinforcement learning approach to solve dynamic job shop scheduling problem, Computers & Operations Research 159 (2023) 106294. 

- [15] S. Luo, L. Zhang, Y. Fan, Real-time scheduling 

32 

for dynamic partial-no-wait multiobjective flexible job shop by deep reinforcement learning, IEEE Transactions on Automation Science and Engineering 19 (4) (2021) 3020–3038. 

- [16] H. Yu, W. Gu, N. Tang, Z. Guo, A deep reinforcement learning approach for dynamic job-shop scheduling problem considering time variable and new job arrivals, Computers & Operations Research 185 (2026) 107263. doi:https://doi.org/10.1016/j.cor.2025.107263. URL https://www.sciencedirect.com/science/ article/pii/S0305054825002928 

- [17] H. Abgaryan, T. Cazenave, A. Harutyunyan, Starjob: Dataset for llm-driven job shop scheduling, CoRR abs/2503.01877 (2025). arXiv:2503.01877, doi:10.48550/ARXIV.2503.01877. URL https://doi.org/10.48550/arXiv.2503.01877 

- [18] P. T. Amarasinghe, S. Nguyen, Y. Sun, D. Alahakoon, Ai-copilot for business optimisation: A framework and A case study in production scheduling, CoRR abs/2309.13218 (2023). arXiv:2309.13218, doi:10.48550/ARXIV.2309.13218. URL https://doi.org/10.48550/arXiv.2309.13218 

- [19] A. AhmadiTeshnizi, W. Gao, H. Brunborg, S. Talaei, M. Udell, Optimus-0.3: Using large language models to model and solve optimization problems at scale, CoRR abs/2407.19633 (2024). arXiv:2407.19633, doi:10.48550/ARXIV.2407.19633. 

   - URL https://doi.org/10.48550/arXiv.2407.19633 

- [20] J. Huang, X. Li, L. Gao, Q. Liu, Y. Teng, Automatic programming via large language models with population self-evolution for dynamic job shop scheduling problem, CoRR abs/2410.22657 (2024). arXiv:2410.22657, doi:10.48550/ARXIV.2410.22657. URL https://doi.org/10.48550/arXiv.2410.22657 

- [21] C. Packer, S. Wooders, K. Lin, V. Fang, S. G. Patil, I. Stoica, J. E. Gonzalez, Memgpt: Towards llms as operating systems (2024). arXiv:2310.08560. URL https://arxiv.org/abs/2310.08560 

- [22] W. Zhong, L. Guo, Q. Gao, H. Ye, Y. Wang, Memorybank: Enhancing large language models with long-term memory, in: Proceedings of the AAAI Conference on Artificial Intelligence, Vol. 38, 2024, pp. 19724–19731. 

- [23] H. Sun, S. Zeng, Hierarchical memory for highefficiency long-term reasoning in llm agents (2025). arXiv:2507.22925. URL https://arxiv.org/abs/2507.22925 

- [24] M. Hu, T. Chen, Q. Chen, Y. Mu, W. Shao, P. Luo, Hiagent: Hierarchical working memory management for solving long-horizon agent tasks with large language model, in: Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), 2025, pp. 32779–32798. 

- [25] S. Cao, Y. Yuan, A novel memetic algorithm for energy-efficient distributed heterogeneous flexible job shop scheduling: Case studies in uavs delivery, IEEE Internet of Things Journal (2024). 

- [26] A. Baykaso˘glu, F. S. Madeno˘glu, A. Hamzadayı, Greedy randomized adaptive search for dynamic flexible job-shop scheduling, Journal of Manufacturing Systems 56 (2020) 425–451. doi:https://doi.org/10.1016/j.jmsy.2020.06.005. URL https://www.sciencedirect.com/science/ article/pii/S0278612520300959 

- [27] H. Wang, J. Cheng, C. Liu, Y. Zhang, S. Hu, L. Chen, Multi-objective reinforcement learning framework for dynamic flexible job shop scheduling problem with uncertain events, Applied Soft Computing 131 (2022) 109717. 

- [28] F. Ren, H. Liu, Dynamic scheduling for flexible job shop based on machinerank algorithm and reinforcement learning, Scientific Reports 14 (1) (2024) 29741. 

- [29] L. Zhang, Y. Yan, C. Yang, Y. Hu, Dynamic flexible job-shop scheduling by multi-agent reinforcement learning with reward-shaping, Advanced Engineering Informatics 62 (2024) 102872. 

- [30] W. Zhang, Z. Peng, F. Zhao, B. Feng, X. Mei, A novel deep reinforcement learning framework based on digital twins for dynamic job shop scheduling problems, Expert Systems with Applications 296 (2026) 128708. 

- [31] Z. Shi, J. Si, J. Zhang, Z. Pang, H. Chen, G. Ding, A deep reinforcement learning method based on hindsight experience replay for multi-objective dynamic job-shop scheduling problem, Expert Systems with Applications 284 (2025) 127989. doi:https://doi.org/10.1016/j.eswa.2025.127989. 

33 

URL https://www.sciencedirect.com/science/ article/pii/S0957417425016100 

- [32] Y. Li, X. Liang, J. Guo, X. Li, L. Wang, B. Du, Categorized attention based hierarchical-agents reinforcement learning for multi-objective dynamic job shop scheduling problem with machine deterioration, Applied Soft Computing 175 (2025) 113032. 

- [33] C. Pan, M. Zhou, Y. Qiao, N. Wu, Scheduling cluster tools in semiconductor manufacturing: Recent advances and challenges, IEEE transactions on automation science and engineering 15 (2) (2017) 586–601. 

- [34] W. Xiong, C. Pan, Y. Qiao, N. Wu, M. Chen, P. Hsieh, Reducing wafer delay time by robot idle time regulation for single-arm cluster tools, IEEE Transactions on Automation Science and Engineering 18 (4) (2020) 1653–1667. 

- [35] J. Ahn, H.-J. Kim, A novel mixed integer programming model with precedence relation-based decision variables for non-cyclic scheduling of cluster tools, IEEE Transactions on Automation Science and Engineering 22 (2024) 2893–2908. 

- [36] H. Jiang, Q. Wu, X. Luo, D. Li, C. Lin, Y. Yang, L. Qiu, Longllmlingua: Accelerating and enhancing llms in long context scenarios via prompt compression, in: L. Ku, A. Martins, V. Srikumar (Eds.), Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), ACL 2024, Bangkok, Thailand, August 11-16, 2024, Association for Computational Linguistics, 2024, pp. 1658–1677. doi:10.18653/V1/2024.ACL-LONG.91. URL https://doi.org/10.18653/v1/2024.acllong.91 

- [37] N. F. Liu, K. Lin, J. Hewitt, A. Paranjape, M. Bevilacqua, F. Petroni, P. Liang, Lost in the middle: How language models use long contexts, Trans. Assoc. Comput. Linguistics 12 (2024) 157– 173. doi:10.1162/TACL_A_00638. URL https://doi.org/10.1162/tacl\_a\_00638 

- [38] A. Yang, A. Li, B. Yang, B. Zhang, B. Hui, B. Zheng, B. Yu, C. Gao, C. Huang, C. Lv, et al., Qwen3 technical report, arXiv preprint arXiv:2505.09388 (2025). 

- [39] DeepSeek-AI, A. Liu, A. Mei, B. Lin, B. Xue, B. Wang, B. Xu, B. Wu, B. Zhang, C. Lin, et al., 

Deepseek-v3.2: Pushing the frontier of open large language models (2025). arXiv:2512.02556. URL https://arxiv.org/abs/2512.02556 

- [40] N. Mu, S. L. Chen, Z. Wang, S. Chen, D. Karamardian, L. Aljeraisy, D. Hendrycks, D. A. Wagner, Can llms follow simple rules?, CoRR abs/2311.04235 (2023). arXiv:2311.04235, doi:10.48550/ARXIV.2311.04235. URL https://doi.org/10.48550/arXiv.2311.04235 

- [41] A. Uzunoglu, G. G. Sahin, A. Safa, PARADISE: evaluating implicit planning skills of language models with procedural warnings and tips dataset, in: L. Ku, A. Martins, V. Srikumar (Eds.), Findings of the Association for Computational Linguistics, ACL 2024, Bangkok, Thailand and virtual meeting, August 11-16, 2024, Association for Computational Linguistics, 2024, pp. 10085–10102. doi:10.18653/V1/2024.FINDINGS-ACL.599. URL https://doi.org/10.18653/v1/2024.findingsacl.599 

- [42] T. Baeumel, J. van Genabith, S. Ostermann, The lookahead limitation: Why multioperand addition is hard for llms, CoRR abs/2502.19981 (2025). arXiv:2502.19981, doi:10.48550/ARXIV.2502.19981. URL https://doi.org/10.48550/arXiv.2502.19981 

- [43] S. Yao, J. Zhao, D. Yu, N. Du, I. Shafran, K. R. Narasimhan, Y. Cao, React: Synergizing reasoning and acting in language models, in: The eleventh international conference on learning representations, 2022. 

- [44] S. Yao, D. Yu, J. Zhao, I. Shafran, T. Griffiths, Y. Cao, K. Narasimhan, Tree of thoughts: Deliberate problem solving with large language models, Advances in neural information processing systems 36 (2023) 11809–11822. 

- [45] D. Zhang, S. Zhoubian, Z. Hu, Y. Yue, Y. Dong, J. Tang, Rest-mcts*: LLM self-training via process reward guided tree search, in: A. Globersons, L. Mackey, D. Belgrave, A. Fan, U. Paquet, J. M. Tomczak, C. Zhang (Eds.), Advances in Neural Information Processing Systems 38: Annual Conference on Neural Information Processing Systems 2024, NeurIPS 2024, Vancouver, BC, Canada, December 10 - 15, 2024, 2024. URL http://papers.nips.cc/paper\_files/paper/ 2024/hash/76ec4dc30e9faaf0e4b6093eaa377218Abstract-Conference.html 

34 

- [46] Z. Liu, H. Mao, G. Sa, H. Liu, J. Tan, Dynamic job-shop scheduling using graph reinforcement learning with auxiliary strategy, Journal of Manufacturing Systems 73 (2024) 1–18. 

- [47] J. Wei, X. Wang, D. Schuurmans, M. Bosma, F. Xia, E. Chi, Q. V. Le, D. Zhou, et al., Chain-ofthought prompting elicits reasoning in large language models, Advances in neural information processing systems 35 (2022) 24824–24837. 

- [48] R. Gui, Z. Wang, J. Wang, C. Ma, H. Zhen, M. Yuan, J. Hao, D. Lian, E. Chen, F. Wu, Hypertree planning: Enhancing LLM reasoning via hierarchical thinking, in: Forty-second International Conference on Machine Learning, ICML 2025, Vancouver, BC, Canada, July 13-19, 2025, OpenReview.net, 2025. 

   - URL https://openreview.net/forum?id= 45he3Ri6JP 

- [49] N. Shinn, F. Cassano, A. Gopinath, K. Narasimhan, S. Yao, Reflexion: Language agents with verbal reinforcement learning, Advances in Neural Information Processing Systems 36 (2023) 8634–8652. 

- [50] J. Light, M. Cai, W. Chen, G. Wang, X. Chen, W. Cheng, Y. Yue, Z. Hu, Strategist: Selfimprovement of LLM decision making via bi-level tree search, in: The Thirteenth International Conference on Learning Representations, ICLR 2025, Singapore, April 24-28, 2025, OpenReview.net, 2025. 

   - URL https://openreview.net/forum?id= gfI9v7AbFg 

- [51] G. Gordon, Stable function approximation in dynamic programming, in: Proceedings of (ICML) International Conference on Machine Learning, 1995, pp. 261 – 268. 

- [52] T. Schmied, J. Bornschein, J. GrauMoya, M. Wulfmeier, R. Pascanu, Llms are greedy agents: Effects of RL finetuning on decision-making abilities, CoRR abs/2504.16078 (2025). arXiv:2504.16078, doi:10.48550/ARXIV.2504.16078. URL https://doi.org/10.48550/arXiv.2504.16078 

- [53] D. Bertsekas, Dynamic Programming and Optimal Control: Volume II; Approximate Dynamic Programming, Vol. 4, Athena Scientific, 2012. 

- [54] W. Liu, T. J. Chua, J. Larn, F. Wang, T. X. Cai, X. Yin, Aps, ERP and MES systems integration for semiconductor backend assembly, in: Seventh International Conference on Control, Automation, Robotics and Vision, ICARCV 2002, Singapore, 2-5 December 2002, Proceedings, IEEE, 2002, pp. 1403–1408. doi:10.1109/ICARCV.2002.1234978. URL https://doi.org/10.1109/ICARCV.2002. 1234978 

- [55] J. Huang, Y. Teng, Q. Liu, L. Gao, X. Li, C. Zhang, G. Xu, Leveraging large language models for efficient scheduling in human–robot collaborative flexible manufacturing systems, npj Advanced Manufacturing 2 (1) (2025) 47. 

- [56] A. Immordino, P. Stöckermann, N. Hayen, T. Altenmüller, G. A. Susto, M. Gebser, K. Schekotihin, G. Seidel, Explainable ai for reinforcement learning based dynamic scheduling solutions in semiconductor manufacturing: A. immordino et al., Journal of Intelligent Manufacturing (2025) 1– 17. 

- [57] P. Brandimarte, Routing and scheduling in a flexible job shop by tabu search, Annals of Operations research 41 (3) (1993) 157–183. 

- [58] J. Demšar, Statistical comparisons of classifiers over multiple data sets, Journal of Machine Learning Research 7 (1) (2006) 1–30. URL http://jmlr.org/papers/v7/demsar06a.html 

- [59] A. Hurst, A. Lerer, A. P. Goucher, A. Perelman, A. Ramesh, A. Clark, A. Ostrow, A. Welihinda, A. Hayes, A. Radford, et al., Gpt-4o system card, arXiv preprint arXiv:2410.21276 (2024). 

- [60] A. Liu, B. Feng, B. Xue, B. Wang, B. Wu, C. Lu, C. Zhao, C. Deng, C. Zhang, C. Ruan, et al., Deepseek-v3 technical report, arXiv preprint arXiv:2412.19437 (2024). 

- [61] X. Wang, J. Wei, D. Schuurmans, Q. V. Le, E. H. Chi, S. Narang, A. Chowdhery, D. Zhou, Selfconsistency improves chain of thought reasoning in language models, in: The Eleventh International Conference on Learning Representations, ICLR 2023, Kigali, Rwanda, May 1-5, 2023, OpenReview.net, 2023. URL https://openreview.net/forum?id= 1PL1NIMMrw 

- [62] A. Singh, A. Fry, A. Perelman, A. Tart, A. Ganesh, A. El-Kishky, A. McLaughlin, A. Low, A. Ostrow, 

35 

A. Ananthram, et al., Openai gpt-5 system card (2025). arXiv:2601.03267. 

URL https://arxiv.org/abs/2601.03267 

- [63] Y. Mei, M. Zhang, S. Nyugen, Feature selection in evolving job shop dispatching rules with genetic programming, in: Proceedings of the Genetic and Evolutionary Computation Conference 2016, 2016, pp. 365–372. 

- [64] R. Wang, G. Wang, J. Sun, F. Deng, J. Chen, Flexible job shop scheduling via dual attention network-based reinforcement learning, IEEE Transactions on Neural Networks and Learning Systems 35 (3) (2023) 3091–3102. 

- [65] R. Wu, J. Zheng, X. Li, H. Tang, X. V. Wang, Y. Li, Dynamic scheduling for flexible job shop under machine breakdown using improved double deep q-network, Expert Systems with Applications 288 (2025) 128280. 

- [66] M. Yuan, Q. Yu, L. Zhang, S. Lu, Z. Li, F. Pei, Deep reinforcement learning based proximal policy optimization algorithm for dynamic job shop scheduling, Computers & Operations Research (2025) 107149. 

- [67] L. Ding, Z. Guan, D. Luo, L. Yue, Data-driven hierarchical multi-policy deep reinforcement learning framework for multi-objective multiplicity dynamic flexible job shop scheduling, Journal of Manufacturing Systems 80 (2025) 536–562. 

- [68] W. Kwon, Z. Li, S. Zhuang, Y. Sheng, L. Zheng, C. H. Yu, J. E. Gonzalez, H. Zhang, I. Stoica, Efficient memory management for large language model serving with pagedattention, in: Proceedings of the ACM SIGOPS 29th Symposium on Operating Systems Principles, 2023. 

- [69] J. W. Tukey, et al., Exploratory data analysis, Vol. 2, Springer, 1977. 

- [70] W. Jun, T. Yue-Jin, D. Hong-Zhong, Z. Da-Zhi, Normalized entropy of rank distribution: a novel measure of heterogeneity of complex networks, Chinese Physics 16 (6) (2007) 1576. 

36 

