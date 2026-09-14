# **Evolutionary Discovery of Heuristic Policies for Traffic Signal Control** 

Ruibing Wang<sup>1</sup> , Shuhan Guo<sup>2</sup> , Zeen Li<sup>2</sup> , Zhen Wang<sup>1</sup> , and Quanming Yao<sup>2</sup> 

> 1 Northwestern Polytechnical University, Xi’an, China `wrb5261@mail.nwpu.edu.cn, w-zhen@nwpu.edu.cn` 

> 2 Tsinghua University, Beijing, China 

```
guoshuhan@tsinghua.edu.cn,lze25@mails.tsinghua.edu.cn,
```

```
qyaoaa@tsinghua.edu.cn
```

**Abstract.** Traffic Signal Control (TSC) involves a challenging tradeoff: classic heuristics are efficient but oversimplified, while Deep Reinforcement Learning (DRL) achieves high performance yet suffers from poor generalization and opaque policies. Online Large Language Models (LLMs) provide general reasoning but incur high latency and lack environment-specific optimization. To address these issues, we propose Temporal Policy Evolution for Traffic ( **TPET** ), which uses LLMs as an evolution engine to derive specialized heuristic policies. The framework introduces two key modules: (1) Structured State Abstraction (SSA), converting high-dimensional traffic data into temporal-logical facts for reasoning; and (2) Credit Assignment Feedback (CAF), tracing flawed micro-decisions to poor macro-outcomes for targeted critique. Operating entirely at the prompt level without training, TPET yields lightweight, robust policies optimized for specific traffic environments, outperforming both heuristics and online LLM actors. 

**Keywords:** Traffic signal control· Sequential decision making· LLMdriven algorithm evolution. 

## **1 Introduction** 

Traffic Signal Control (TSC) [16] is a canonical sequential decision-making problem at the heart of urban mobility. The efficient dispatching of signal phases directly impacts commuter travel time, fuel consumption, and public safety. This high-stakes domain demands policies that are not only efficient but also robust to the non-stationary, dynamic nature of traffic flows. 

In striving for effective traffic signal control, researchers have encountered a fundamental trade-off between generality and specialization. Classic transportation models, such as Fixed-Time [8] and MaxPressure [17], represent the general-purpose solution. These methods function as traditional heuristic policies: they rely on manually designed, explicit rules to map observed traffic states directly to signal actions, without the need for parameter training. While computationally trivial and fast, their reliance on simple, myopic logic makes them 

#### 2 R. Wang et al. 

fundamentally sub-optimal for any specific intersection’s unique topology and complex flow patterns. At the other end of the spectrum, Deep Reinforcement Learning (DRL) methods offer a path to deep specialization and can achieve high performance. This performance, however, comes at a significant cost: DRL agents are notorious "black boxes" with unverifiable policies, and their intensive training on specific data distributions often leads to brittle policies with poor generalization. Recently, Large Language Models (LLMs) have been proposed as a new paradigm, using a general-purpose LLM as an online actor. This approach, while intellectually appealing, suffers from critical, real-world flaws, including prohibitive inference latency incompatible with high-frequency decisions and a fundamental lack of environment-specific specialization. 

To address these limitations, We argue that the optimal role for an LLM is not as a slow, generic online actor, but as a powerful discoverer. We introduce the Temporal Policy Evolution for Traffic ( **TPET** ) framework, which leverages an LLM-driven evolutionary engine to evolve a specialized, structured, and lightweight policy from the ground up. The final output is a simple heuristic function that solves both problems of the online LLM: it runs with millisecond latency, and it is deeply specialized, having been optimized over thousands of simulated generations specifically for the target environment. 

Our scientific hypothesis is that this specialization will lead to a superior performance compared to the generic reasoning of an online LLM and the simplistic logic of classic heuristics. To achieve this, we introduce two key modules to empower the LLM in this discovery process: the Structured State Abstraction (SSA) module to bridge the numerical-to-Semantic gap, and the Credit Assignment Feedback (CAF) module to provide rich, explanatory critiques, allowing the LLM to perform targeted, intelligent mutations that adapt the policy to the environment’s unique challenges. 

Our contributions can be summarized as follows: 

- We introduce the Evolutionary Discovery paradigm for TSC, which leverages an LLM to discover specialized structured policies, offering a novel, practical alternative to fixed strategies and online LLM actors. 

- We design and implement the TPET framework with two novel modules: SSA, a state abstraction method for high-frequency time-series data, and CAF, a credit assignment mechanism that back-traces simulation logs for critique-driven evolution. 

- We demonstrate through experiments in CityFlow that our discovered policy achieves state-of-the-art performance advantage over both classic heuristics of transportation models and the general-purpose online LLM actor. 

## **2 Related Work** 

### **2.1 Traffic Signal Control (TSC) Problem** 

The pursuit of effective TSC strategies has broadly followed three paradigms. The most traditional class, classic transportation strategies, provides general- 

Evolutionary Discovery of Heuristic Policies for Traffic Signal Control 3 

purpose, computationally trivial solutions such as Fixed-Time [8] and MaxPressure series [17, 20, 10]. While fast, their simple, myopic logic is sub-optimal for complex flows. To achieve deep specialization, Reinforcement Learning (RL) based methods emerged, with a large body of work including MPLight [2], AttendLight [14], PressLight [18], and advanced methods [24, 11]. These methods achieve state-of-the-art performance in simulations but are notorious "black boxes" with unverifiable policies and poor generalization. Most recently, Online LLM-based Approaches have been proposed [5, 9, 22, 13, 1], which use a general LLM as a decision-maker. This paradigm, however, suffers from prohibitive latency and a lack of specialization. 

### **2.2 LLM for Heuristic Evolution** 

Recent advancements have established Large Language Models (LLMs) as engines for automated heuristic design, marking a shift towards "Language HyperHeuristics" where LLMs act as evolutionary operators within function space. These processes typically build on existing heuristics [4, 3, 7] and aim to refine them automatically. FunSearch [15] couples a pre-trained LLM with a systematic evaluator to discover new mathematical knowledge and algorithms. EoH [12] extends this idea by co-evolving natural language thoughts and executable codes, while ReEvo [21] introduces reflection to generate verbal gradients from past performance, improving efficiency and interpretability. NeRM [6] further addresses misalignment between task descriptions and solutions through nested refinement of prompts and algorithms, assisted by predictor-based evaluation. Collectively, these works illustrate a progression from stochastic code search to reflective and structured evolutionary frameworks. 

## **3 Methodology** 

### **3.1 Problem Formulation** 

Traffic Signal Control is a canonical sequential decision-making problem. Following LLMLight [9], we model the urban traffic network as a graph _𝐺_ = ( _𝑉, 𝐸_ ), where each intersection _𝑣_ ∈ _𝑉_ is formulated as a discrete-time Markov Decision Process (MDP). The objective is to minimize total waiting time, queue length, and travel time of vehicles. At each step _𝑡_ , the agent observes a state _𝑠𝑡_ ∈ _𝑆_ , represented by a high-dimensional vector that captures the traffic situation, including queue length (the number of waiting vehicles for each movement) and waiting time (the accumulated delays reflecting temporal pressure and fairness). The action _𝑎𝑡_ ∈ _𝐴_ is the selection of the next signal phase from a predefined set, where each phase corresponds to a group of non-conflicting traffic movements given green simultaneously. The agent’s decision must respect safety constraints such as minimum green times and clearance intervals. 

4 R. Wang et al. 



Fig. 1: Framework of TPET, depicting an LLM iteratively evolving heuristic traffic control policies by receiving actionable defect feedback from the Credit Assignment Feedback (CAF) module, which analyzes real-time traffic conditions abstracted by the Structured State Abstraction (SSA) module. 

### **3.2 Foundational Framework** 

Our framework builds upon the biologically inspired co-evolutionary paradigm introduced in NeRM [6]. The core idea is to jointly evolve task specifications and algorithmic solutions through a nested loop of two interleaved modules: Metamorphosis on Prompts (MoP), which iteratively refines natural language task descriptions, and Metamorphosis on Algorithms (MoA), which evolves code solutions conditioned on these refined prompts. While NeRM originally utilizes LLMs to evolve heuristic code for combinatorial optimization, we adapt this methodology to the domain of sequential decision-making. Specifically, the evolutionary engine in TPET targets the generation of heuristic policies for traffic control, optimizing the core decision-making logic (e.g., pressure calculation rules) encapsulated within the control loop. 

**Challenges in Adaptation** However, directly applying this general framework to Traffic Signal Control faces two distinct challenges. First, the Semantic Gap hinders reasoning, as traffic simulators output high-dimensional numerical data while LLMs rely on semantic logic. Second, since rewards in this sequential domain are sparse and delayed, the standard scalar fitness score fails to identify the specific micro-decisions causing macro-level failures. 

### **3.3 Temporal Policy Evolution for Traffic (TPET)** 

To overcome the challenges identified above, we propose the TPET framework, which equips the foundational co-evolutionary backbone with two specific mech- 

Evolutionary Discovery of Heuristic Policies for Traffic Signal Control 5 

anisms. We introduce Structured State Abstraction (SSA) to bridge the semantic gap by translating numerical states into interpretable logical facts , and Credit Assignment Feedback (CAF) to resolve the credit assignment problem by replacing sparse rewards with dense, actionable critiques derived from simulation logs. 

**Structured State Abstraction (SSA) for Context Translation** This module is developed to overcome the semantic gap. The raw state vector _𝑠𝑡_ is numerical, while the heuristic _𝜋_ we aim to discover should operate on robust, logical concepts. Furthermore, _𝑠𝑡_ is an instantaneous snapshot, lacking the crucial temporal history _𝐻𝑡_ −1 required for sequential decisions. The SSA module is designed as a formal, deterministic function _𝑓𝑆𝑆𝐴_ : ( _𝑆𝑡 , 𝐻𝑡_ −1) → Σ _𝑡_<sup>∗.Itspurposeistoact</sup> as the input interface for the policy _𝜋_ . During online validation, _𝜋_ calls SSA at each step _𝑡_ to translate the raw numerical state _𝑠𝑡_ and its history _𝐻𝑡_ −1 into a discrete, structured alphabet Σ _𝑡_<sup>∗.</sup> 

This transformation is a knowledge-driven synthesis pipeline designed to extract salient temporal-logical facts. This process involves two stages: 

- Metric Aggregation and Persistence: The module computes instantaneous aggregate metrics (such as maximum pressure). Crucially, it also maintains and updates persistent temporal metrics (such as a starvation timer for each phase), which explicitly encode the system’s history. 

- Temporal Predicate Generation: The module applies a set of logical rules to map these quantitative metrics (both instantaneous and persistent) onto a stable, qualitative vocabulary, generating structured facts (predicates). 

The resulting alphabet Σ _𝑡_<sup>∗is a structured set of facts describing the complete</sup> state. This set includes the following predicates: 

- Congestion Predicates: These describe instantaneous pressure. 

   - Examples: “Congestion: Critical”, “Congestion: High”, “Congestion: Moderate”, “Congestion: Low”, or “Dominant Flow: Phase 2”. 

- Temporal-Fairness Predicates: These capture historical context. 

   - Examples include “Starvation Risk: High” (triggered by pressure _> 𝜃𝑑𝑒𝑚𝑎𝑛𝑑_ and starvation_timer _> 𝜏𝑐𝑟𝑖𝑡𝑖𝑐𝑎𝑙_ ) or “Queue Urgency: Critical” (derived from `max_wait_time` ). 

- Balance Predicates: These describe relationships between flows. 

   - Examples: “Imbalance: EW Dominant” or “Imbalance: None”. 

It is critical to understand how this module functions within the TPET loop. During online validation, the evolved policy _𝜋𝑖_ (the Python function) calls the _𝑓𝑆𝑆𝐴_ function at every step _𝑡_ to acquire its numerical input Σ _𝑡_<sup>∗.Thelogic</sup> within _𝜋𝑖_ then operates on these inputs. During the evolution stage, the LLM is provided with the description of the structured vocabulary that _𝑓𝑆𝑆𝐴_ produces. This defined interface is the crucial information support that allows the LLM to write a new policy _𝜋𝑐ℎ𝑖𝑙𝑑_ that intelligently utilizes these pre-defined structured concepts to address the flaws of the previous policy. An example has been shown in Fig. 2a. 



<!-- Start of picture text -->
6 R. Wang et al.<br>(a) Process of SSA module.<br>(b) Process of CAF module.<br><!-- End of picture text -->

Fig. 2: Details design of key modules. 

**Credit Assignment Feedback (CAF) for Post-Hoc Defect Analysis** This module aims to address the temporal credit assignment problem. When a policy _𝜋𝑖_ completes the evaluation, its final fitness score is an intractably sparse reward. 

The CAF module is a post-hoc analysis engine designed to solve this. After the simulation is complete, it performs heuristic-driven back-tracing on the entire simulation log _𝐿_ = {(Σ0<sup>∗</sup><sup>_, 𝑎_0)</sup><sup>_,_(Σ</sup> 1<sup>∗</sup><sup>_, 𝑎_1)</sup><sup>_, ...,_(Σ</sup> _𝑇_<sup>∗</sup><sup>_, 𝑎𝑇_)}.ThecoreoftheCAFisa</sup> Defect Pattern Library containing formal definitions of common failure patterns. These patterns are expressed as temporal-logical rules that connect flawed microdecisions to negative macro-outcomes: 

- Wasted Green Time: A spatial-instantaneous failure, defined as the agent selecting a phase _𝑎𝑡_ = _𝑖_ when its corresponding structured state Σ _𝑡_<sup>∗indicated</sup> near-zero demand. 

- Phase Starvation: A severe temporal failure. This pattern is matched if the log _𝐿_ shows a phase _𝑖_ that has not been activated for a critical duration _𝜏𝑐𝑟𝑖𝑡_ (i.e., _𝑎𝑘_ ≠ _𝑖_ for _𝑘_ ∈[ _𝑡_ − _𝜏𝑐𝑟𝑖𝑡 , 𝑡_ ]) and its structured state Σ _𝑡_<sup>∗indicatedhigh</sup> demand. 

- Premature Phase Switch: A temporal inefficiency. This pattern is matched if the agent was serving a high-demand phase _𝑖_ (indicated by Σ _𝑡_<sup>∗</sup> −1<sup>)but</sup> switched to phase _𝑗_ ( _𝑎𝑡_ = _𝑗_ ), incurring the time cost of a yellow-light cycle without fully serving the demand. 

The CAF module scans the log, aggregates these defects, and generates a structured critique _𝐶𝑖_ for the entire policy _𝜋𝑖_ . This critique is the primary feedback signal for the LLM. This process replaces the simple fitness score of a standard evolutionary algorithm with a rich, actionable debug report. An example has been shown in Fig. 2b. Utilizing these two modules, the process is shown in Algorithm 1. 

Evolutionary Discovery of Heuristic Policies for Traffic Signal Control 7 

**Algorithm 1** Learning Process of TPET **Input:** Problem description; initial algorithms; LLM; **Output** : Generated optimal algorithm. 1: _ℎ_<sup>_★_</sup> ← initial algorithm 2: **while** true **do** 3: // Prompt & Algorithm Evolution with SSA & CAF 4: **for** _𝑗_ = 1 _,_ 2 _,_ · · · _,𝑇_ **do** 5: **for** _𝑘_ = 1 _,_ 2 _,_ · · · _,𝑇_ **do** 6: ... 7: Reflection & Revolution (with CAF prompt) 8: ... 9: Evaluation new policy with Real-time Analysis (with SSA module) 10: **end for** 11: **end for** 12: _ℎ_<sup>_★_</sup> ← best algorithm from current evolution 13: Deploy _ℎ_<sup>_★_</sup> in intersections 14: **end while** 

### **3.4 Comparison with Previous Works** 

While our evolutionary loop is methodologically based on NeRM’s MoP and MoA components , TPET successfully adapts this paradigm to a fully dynamic, high-frequency, sequential decision-making domain. This is a non-trivial leap, as NeRM was designed for static problems using a single fitness score, and NeRMNet addressed static batch allocation. Our adaptation is enabled exclusively by two modules: SSA serves as the structured interface for the policy, and CAF replaces the simple feedback of prior work with a sequential critique. This reframes the LLM’s task from finding a static heuristic to debugging the temporal-logical flaws in a dynamic policy. The final discovered policy is an interpretable, robust algorithm, evolved to explicitly handle the temporal defects identified by CAF. 

## **4 Experiments** 

### **4.1 Experimental Settings** 

**Datasets** Our experiments use three real-world traffic flow datasets. Specifically, we select two datasets from Jinan and one dataset from Hangzhou. 

- **Jinan-1 & Jinan-2:** These two datasets is collected from Dongfeng subdistrict, Jinan, China, featuring 12 intersections. The covered area is approximately 400 meters east-west and 800 meters north-south. 

- **Hangzhou:** This dataset is collected from Gudang sub-district, Hangzhou, China, featuring 16 intersections. The covered area spans 800 meters eastwest and 600 meters north-south. 

8 R. Wang et al. 

Table 1: Overall performance comparison of TPET against traditional transportation, reinforcement learning, and LLM-enhanced methods on the Jinan and Hangzhou datasets. The best results are bolded, the second-best results are underlined. 

|Models|ATT|Jinan-1<br>AQL|AWT|ATT|Jinan-2<br>AQL|AWT|ATT|Hangzhou<br>AQL|AWT|
|---|---|---|---|---|---|---|---|---|---|
||||**T**|**ransportatio**|**n Methods**|||||
|Random<br>FixedTime<br>Maxpressure|552_._74(12_._7) <br>450_._11(0_._00)<br>265_._75(0_._00)|529_._63(20_._05) <br>394_._34(0_._00)<br>133_._90(0_._00)|99_._33(9_._18)<br>69_._19(0_._00)<br>40_._20<br>(0_._00)|555_._23(13_._72) <br>441_._19(0_._00)<br>273_._20(0_._00)|428_._38(19_._77) <br>294_._14(0_._00)<br>106_._58(0_._00)|100_._40(5_._64)<br>66_._72(0_._00)<br>38_._25<br>(0_._00)|621_._14(20_._37) <br>616_._02(0_._00)<br>325_._33(0_._00)|295_._81(17_._08) <br>301_._33(0_._00)<br>68_._99(0_._00)|96_._06(6_._46)<br>73_._99(0_._00)<br>49_._60<br>(0_._00)|
|||||**RL Me**|**thods**|||||
|MPLight<br>AttendLight<br>PressLight<br>CoLight|291_._79(1_._25)<br>273_._02(0_._87)<br>275_._85(0_._74)<br>266_._39(0_._60)|171_._70(0_._92)<br>144_._05(0_._74)<br>148_._18(0_._81)<br>135_._08(0_._82)|89_._93(2_._40)<br>55_._93(2_._12)<br>54_._81(1_._39)<br>53_._33(2_._02)<br>**LLMLi**|304_._51(0_._88)<br>280_._94(0_._66)<br>281_._46(0_._75)<br>274_._77(0_._54)<br>**ght (with G**|142_._25(0_._74)<br>115_._52(0_._93)<br>115_._99(0_._62)<br>108_._28(0_._72)<br>**eneralist L**|90_._91(1_._93)<br>52_._46(1_._67)<br>47_._27(2_._38)<br>54_._14(1_._39)<br>**LMs)**|345_._60(0_._96)<br>322_._94(0_._78)<br>364_._13(0_._67)<br>322_._85(0_._65)|84_._70(0_._83)<br>66_._96(0_._55)<br>98_._67(0_._73)<br>66_._94(0_._61)|81_._97(2_._79)<br>55_._19(1_._41)<br>90_._33(1_._40)<br>61_._82(2_._38)|
|Qwen2-72B<br>Llama2-70B|274_._33(12_._72) <br>320_._41(12_._80)|144_._95(13_._70) <br> 210_._13(11_._78)|54_._94(3_._68)<br> 100_._90(2_._75)|277_._78(13_._74) <br>324_._52(13_._82)|112_._13(11_._71) <br> 162_._34(12_._79)|53_._12(4_._69)<br> 99_._87(4_._76)|321_._91(14_._73) <br>357_._95(10_._81)|65_._75(12_._70)<br> 93_._21(11_._77)|66_._52(5_._68)<br> 106_._63(2_._74)|
|Llama3-70B<br>ChatGPT-3.5<br>GPT-4|271_._60(7_._76) <br>501_._36(11_._90) <br>**264**_._**70**(7_._74)|142_._95(11_._73) <br> 479_._50(13_._88) <br>**132**_._**53**(9_._71)|54_._55(2_._70)<br> 154_._19(4_._85)<br>46_._16(1_._69)|277_._49(10_._78) <br>524_._81(9_._91) <br>**271**_._**34**(8_._75)<br>**Our M**|112_._86(7_._74)<br> 393_._21(12_._87) <br>**105**_._**22**(7_._72)<br>**ethod**|51_._76(2_._71)<br> 179_._34(2_._84)<br>47_._55(2_._70)|325_._85(8_._77)<br>463_._04(10_._89) <br>318_._71<br>(9_._20)|69_._42(9_._73)<br> 181_._95(11_._86) <br>62_._84<br>(7_._62)|71_._51(3_._70)<br> 191_._87(3_._83)<br>58_._09(1_._37)|
|NeRM<br>TPET|278_._45(0_._54)<br>265_._58<br>(0_._61)|149_._20(0_._42)<br>133_._43<br>(0_._47)|55_._10(0_._43)<br>**36**_._**80**(0_._49)|288_._70(0_._49)<br>271_._67<br>(0_._52)|123_._60(0_._35)<br>105_._30<br>(0_._38)|54_._80(0_._39)<br>**35**_._**08**(0_._42)|330_._25(0_._59)<br>**313**_._**64**(0_._63)|72_._10(0_._56)<br>**59**_._**13**(0_._59)|62_._35(0_._29)<br>**31**_._**41**(0_._28)|



**Evaluation Metrics** Following previous studies, we evaluate performance using three standard metrics. These are: Average Travel Time (ATT), the average time for a vehicle to travel from entry to exit; Average Queue Length (AQL), the average number of stationary vehicles across all lanes; and Average Wait Time (AWT), the average accumulated time vehicles spend in a stationary state. 

**Implementation Details** All experiments are conducted within the CityFlow [23] simulation environment. The LLM Evolution Engine is implemented using the GLM-4-Flash model as its core. Our computational environment is equipped with an NVIDIA RTX 3070Ti GPU, an Intel i7-11700K CPU, and 32GB of RAM. During each iteration of the evolutionary loop, 20 policy candidates are generated. Following the critique from the CAF module and the overall fitness evaluation, the top 3 candidates are retained for the next generation. To assess the performance and stability of the discovered policies, each experiment is run three times and has 20 iterations, with the mean and standard deviation reported in our results. 

**Compared Models** To provide a comprehensive evaluation, we consider three categories of comparison methods. First, traditional transportation strategies such as Random, FixedTime [8], and Maxpressure [17, 20, 10] are included as representative baselines. Second, we benchmark against several reinforcement learning algorithms, including MPLight [2], AttendLight [14], PressLight [18], and CoLight [19]. Finally, we instantiate LLMLight [9] with different large language model backbones, specifically GPT-4, ChatGPT-3.5, Qwen, Llama2, and Llama3. 

### **4.2 Performance Comparison** 

The experimental results in Table 1 confirm that our TPET framework delivers strong performance, validating the hypothesis that an LLM-driven evolu- 

Evolutionary Discovery of Heuristic Policies for Traffic Signal Control 9 



Fig. 3: Performance and robustness comparison on key metrics (ATT, AQL, AWT). Lower values are better for all metrics. Each point represents the mean value, and the error bar represents the standard deviation (±SD) across multiple runs. Note the Y-axis is zoomed in for each metric to highlight variance. TPET achieves top-tier performance with minimal variance, in stark contrast to the high instability (large error bars) of LLM-based actors. 

tionary process guided by SSA and CAF can discover specialized policies that outperform heuristics and rival complex models. TPET consistently surpasses traditional strategies such as FixedTime and Maxpressure, and establishes itself as highly competitive with state-of-the-art reinforcement learning methods and online LLM-Light actors. On key metrics like Average Travel Time, its performance is superior to or on par with the strongest baselines, while its exceptional results on Average Wait Time highlight the effectiveness of Attribution Feedback in addressing temporal blind spots often overlooked by other paradigms. 

A particularly important comparison is with NeRM, which evolves policies using only sparse fitness scores and lacks our feedback modules. TPET achieves substantial gains over NeRM, demonstrating that the contributions of SSA and CAF are critical for effective policy discovery. 

Beyond performance, TPET demonstrates exceptional stability and robustness. As shown in Figure 3, which reports mean performance and standard deviation, generalist LLM actors such as Qwen2-72B and GPT-4 suffer from large error bars, indicating instability. In contrast, TPET maintains consistently tight variance, often comparable to deterministic methods like Maxpressure. This stability confirms that TPET not only achieves strong performance but also delivers optimized and reliable policies, making it a practical solution for real-world traffic signal control. 

### **4.3 Ablation Study** 

To validate the effectiveness of our framework’s core components, we conduct an ablation study, with results shown in Table 2. We individually analyze the 

#### 10 R. Wang et al. 

Table 2: Ablation study. 

|**Models**||**Jinan-1**|||**Jinan-2**|||**Hangzho**|**u**|
|---|---|---|---|---|---|---|---|---|---|
||ATT|AQL|AWT|ATT|AQL|AWT|ATT|AQL|AWT|
|TPET|265_._58(0_._61)|133_._93(0_._47)|36_._80(0_._49)|271_._67(0_._52)|105_._30(0_._38)|35_._08(0_._42)|313_._64(0_._6|3) 59_._13(0_._59|) 31_._41(0_._28)|
|w/o SSA|266_._53(0_._55)|135_._04(0_._43)|43_._80(0_._48)|273_._08(0_._50)|107_._50(0_._36)|40_._43(0_._41)|322_._67(0_._6|0) 66_._70(0_._57|) 53_._01(0_._32)|
|w/o CAF|275_._70(0_._58)|146_._94(0_._46)|53_._26(0_._44)|285_._32(0_._53)|120_._18(0_._39)|52_._55(0_._40)|326_._96(0_._6|2) 69_._59(0_._61|) 60_._20(0_._30)|



contribution of our two proposed modules: (1) w/o SSA, which removes the Structured State Abstraction, forcing the policy to operate on less processed information; and (2) w/o CAF, which removes the Credit Assignment Feedback, reverting the evolution to a simpler search. 

The results demonstrate that both components are indispensable. Removing SSA causes clear performance degradation, confirming that the temporal-logical facts it synthesizes provide crucial high-level abstractions for effective reasoning. The w/o CAF variant shows an even greater drop, indicating that without its targeted critique, the LLM-driven evolution lacks guidance. Together, SSA and CAF are essential for enabling TPET to discover specialized, high-performance policies. 

### **4.4 Case Study** 



Fig. 4: Evolution of TPET for TSC. We outline the key outputs of the SSA and CAF modules. Moreover, we present the best algorithm in the final iteration and compare it with Maxpressure. 

To provide a qualitative understanding of our framework, we visualize the evolutionary discovery path of TPET against the NeRM baseline in Figure 4. This figure illustrates the progression from a simple initial policy to a specialized final heuristic, plotting the fitness improvement over generations. 

During the evaluation of a policy, the SSA module monitors the runtime statistics. Its primary role is to translate high-dimensional numerical metrics, 

Evolutionary Discovery of Heuristic Policies for Traffic Signal Control 11 

which are incomprehensible to the LLM, into a set of interpretable, structured facts, such as the high congestion levels on specific roads shown in the figure. This structured information is then passed to the CAF module. CAF aggregates these structured facts from the simulation logs to generate a high-level reflection. This reflection summarizes the policy’s defects and guides the main evolutionary direction, for instance, by shifting focus from a simple scalar fitness to a more balanced, multi-faceted one. This structured critique then informs the next code revolution, allowing the LLM to make targeted, intelligent modifications based on concrete, interpretable feedback. This iterative loop of SSA translation and CAF-guided reflection enables TPET to efficiently navigate the search space and discover a robust, multi-layered final heuristic that significantly outperforms the standard MaxPressure baseline. 

## **5 Conclusion** 

In this paper, we presented TPET framework, an approach utilizes LLM as an evolution engine. Our core contribution lies in architecting a structured feedback loop: the SSA module provides interpretable real-time traffic states, which are then analyzed by the CAF module to generate precise, actionable critiques detailing policy defects. This structured feedback loop empowers the LLM to iteratively debug and refine heuristic policy code, moving beyond opaque optimization towards transparent, explainable, and continually improving control strategies. TPET demonstrates significant advancements in policy interpretability, development efficiency, and performance over traditional methods. We believe this framework paves a robust path for future research into adaptive, LLMguided intelligent transportation systems that prioritize both effectiveness and transparency. 

## **References** 

1. Bilal, H., Rehman, A., Aslam, M.S., Ullah, I., Chang, W.J., Kumar, N., Almuhaideb, A.M.: Hybrid trafficai: A generative ai framework for real-time traffic simulation and adaptive behavior modeling. IEEE Transactions on Intelligent Transportation Systems (2025) 

2. Chen, C., Wei, H., Xu, N., Zheng, G., Yang, M., Xiong, Y., Xu, K., Li, Z.: Toward a thousand lights: Decentralized deep reinforcement learning for large-scale traffic signal control. Proceedings of the AAAI Conference on Artificial Intelligence (2020) 

3. Dorigo, M., Di Caro, G.: Ant colony optimization: a new meta-heuristic. In: Proceedings of the 1999 Congress on Evolutionary Computation-CEC99 (Cat. No. 99TH8406) (1999) 

4. Fred Glover, M.L.: Tabu Search Principles (1997) 

5. Guo, Q., Li, X., Chen, J., Guo, Z., Li, X., Zhang, L., Li, L.: A dual large language models architecture with herald guided prompts for parallel fine grained traffic signal control. arXiv (2025) 

6. Guo, S., Yin, N., Kwok, J., Yao, Q.: Nested-refinement metamorphosis: Reflective evolution for efficient optimization of networking problems. In: Findings of the Association for Computational Linguistics: ACL 2025 (2025) 

#### 12 R. Wang et al. 

7. Kennedy, J., Eberhart, R.: Particle swarm optimization. In: Proceedings of ICNN’95 - International Conference on Neural Networks (1995) 

8. Koonce, P., Rodegerdts, L.A., Lee, K., Quayle, S., Beaird, S., Braud, C., Bonneson, J.A., Tarnoff, P.J., Urbanik, T.: Traffic signal timing manual. Technical report, Federal Highway Administration, United States (2008) 

9. Lai, S., Xu, Z., Zhang, W., Liu, H., Xiong, H.: Llmlight: Large language models as traffic signal control agents. arXiv (2024) 

10. Levin, M.W.: Max-pressure traffic signal timing: A summary of methodological and experimental results. Journal of Transportation Engineering, Part A: Systems (2023) 

11. Liao, X.C., Mei, Y., Zhang, M.: Gplight+: A genetic programming method for learning symmetric traffic signal control policy. IEEE Transactions on Evolutionary Computation (2025) 

12. Liu, F., Xialiang, T., Yuan, M., Lin, X., Luo, F., Wang, Z., Lu, Z., Zhang, Q.: Evolution of heuristics: Towards efficient automatic algorithm design using large language model. In: Forty-first International Conference on Machine Learning (2024) 

13. Movahedi, M., Choi, J.: The crossroads of llm and traffic control: A study on large language models in adaptive traffic signal control. IEEE Transactions on Intelligent Transportation Systems (2025) 

14. Oroojlooy, A., Nazari, M., Hajinezhad, D., Silva, J.: Attendlight: Universal attention-based reinforcement learning model for traffic signal control. In: Advances in Neural Information Processing Systems (2020) 

15. Romera-Paredes, B., Barekatain, M., Novikov, A., Balog, M., et al: Mathematical discoveries from program search with large language models. Nature (2024) 

16. Shelby, S.G.: Single-intersection evaluation of real-time adaptive traffic signal control algorithms. Transportation Research Record **1867** (1), 183–192 (2004) 

17. Varaiya, P.: Max pressure control of a network of signalized intersections. Transportation Research Part C: Emerging Technologies (2013) 

18. Wei, H., Chen, C., Zheng, G., Wu, K., Gayah, V., Xu, K., Li, Z.: Presslight: Learning max pressure control to coordinate traffic signals in arterial network. In: Proceedings of the 25th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining (2019) 

19. Wei, H., Xu, N., Zhang, H., Zheng, G., Zang, X., Chen, C., Zhang, W., Zhu, Y., Xu, K., Li, Z.: Colight: Learning network-level cooperation for traffic signal control. In: Proceedings of the 28th ACM international conference on information and knowledge management. pp. 1913–1922 (2019) 

20. Wu, Q., Zhang, L., Shen, J., Lü, L., Du, B., Wu, J.: Efficient pressure: Improving efficiency for signalized intersections. arXiv (2021) 

21. Ye, H., Wang, J., Cao, Z., Berto, F., Hua, C., Kim, H., Park, J., Song, G.: Reevo: Large language models as hyper-heuristics with reflective evolution. In: Advances in Neural Information Processing Systems (2024) 

22. Yuan, Z., Lai, S., Liu, H.: Collmlight: Cooperative large language model agents for network-wide traffic signal control. arXiv (2025) 

23. Zhang, H., Feng, S., Liu, C., Ding, Y., Zhu, Y., Zhou, Z., Zhang, W., Yu, Y., Jin, H., Li, Z.: Cityflow: A multi-agent reinforcement learning environment for large scale city traffic scenario. In: Proceedings of The World Wide Web Conference (WWW). pp. 3620–3624. ACM (2019) 

24. Zhang, L., Wu, Q., Shen, J., Lü, L., Du, B., Wu, J.: Expression might be enough: representing pressure and demand for reinforcement learning based traffic signal control. In: Proceedings of the 39th International Conference on Machine Learning (2022) 

