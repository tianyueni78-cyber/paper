# **MeLA: A Metacognitive LLM-Driven Architecture for Automatic Heuristic Design** 

**Zishang Qiu**<sup>1</sup> **, Xinan Chen**<sup>1*</sup> **, Long Chen**<sup>2</sup> **, and Ruibin Bai**<sup>1</sup> 1 **School of Computer Science, University of Nottingham Ningbo China, Ningbo, China** 2 **College of Teacher Education, Zhejiang Normal University, Jinhua, China xinan.chen@nottingham.edu.com** 

#### **Abstract** 

This paper introduces MeLA, a Metacognitive LLM-Driven Architecture that presents a new paradigm for Automatic Heuristic Design (AHD). Traditional evolutionary methods operate directly on heuristic code; in contrast, MeLA evolves the instructional prompts used to guide a Large Language Model (LLM) in generating these heuristics. This process of ”prompt evolution” is driven by a novel metacognitive framework where the system analyzes performance feedback to systematically refine its generative strategy. MeLA’s architecture integrates a problem analyzer to construct an initial strategic prompt, an error diagnosis system to repair faulty code, and a metacognitive search engine that iteratively optimizes the prompt based on heuristic effectiveness. In comprehensive experiments across both benchmark and real-world problems, MeLA consistently generates more effective and robust heuristics, significantly outperforming state-of-the-art methods. Ultimately, this research demonstrates the profound potential of using cognitive science as a blueprint for AI architecture, revealing that by enabling an LLM to metacognitively regulate its problem-solving process, we unlock a more robust and interpretable path to AHD. 

#### **Code/Dataset/Result** — 

https://github.com/Qzs1335/MeLA 

## **Introduction** 

The quest for high-performance heuristics is a central and enduring challenge in computational intelligence. These specialized algorithms are the engines driving progress in complex optimization, from logistics to drug discovery. Historically, powerful metaheuristics like SCSO (Seyyedabbasi and Kiani 2023), WO (Han et al. 2024), and SOA (Givi and Hubalovska 2023) were the products of a manual, artisanal process requiring deep human expertise. While these algorithms can perform exceptionally well on the specific problems they were designed for, their performance often degrades when applied to different types of problems or even to variations of the original problem. This limitation is a direct consequence of the No Free Lunch (NFL) theorem (Wolpert and Macready 1997), which posits that no single heuristic can be universally optimal across all possible problems. Consequently, the reliance on human-driven design 

*Corresponding author. 

for specific problem instances has become a critical bottleneck, hindering the scale and speed of scientific and industrial innovation. 

To break this impasse, the field of Automatic Heuristic Design (AHD) emerged, aiming to automate the creation of heuristics. While foundational AHD paradigms like HyperHeuristics (HHs) (Pillay and Qu 2018) and Genetic Programming (GP) (Burke et al. 2007) were a conceptual leap forward, their creative potential is fundamentally capped. By design, they are tethered to human guidance, operating within search spaces defined by expert-supplied components or primitives (Mei et al. 2022). This inherent limitation prevents them from achieving true design autonomy, leaving the grand challenge of fully automated discovery unsolved. 

The advent of Large Language Models (LLMs) introduced a paradigm shift. Recognizing their potential, the latest research frontier fuses LLMs with the directed pressure of evolutionary computation (Zhang et al. 2024). Pioneering systems like FunSearch (Romera-Paredes et al. 2024), EoH (Liu et al. 2024), and ReEvo (Ye et al. 2024) have demonstrated remarkable success by evolving heuristics, discovering solutions that rival human-engineered ones. However, this paper argues that their focus on evolving _heuristics_ is a source of profound limitations. The paradigm’s core flaw is its reliance on population-level dynamics, which treats the LLM as a static generator rather than an adaptive learner. By failing to internalize the principles of what constitutes a superior heuristic, this process inherently limits both the peak performance and the generalizability of the discovered strategies. 

This work posits that the true point of leverage is not the final heuristic, but the generative _reasoning process_ that creates it. To this end, we introduce **Prompt Evolution** , a new AHD paradigm that fundamentally differs from the natural selection model used by prior work. As illustrated in **Figure 1** , instead of evolving a population of heuristic codes, our architecture evolves the problem-solving strategy itself, which is encoded in the LLM’s guiding prompt. This evolution is driven by a **metacognitive search engine** inspired by cognitive science (Martinez 2006). This engine assesses the entire causal chain—from the strategic ”thinking process” embodied in a prompt to the empirical performance of the heuristic it produces—and uses this analysis to systematically refine the prompt for the next generation of thinking. 



<!-- Start of picture text -->
Nature Evolving Driven Generate New<br>Generate<br>Heuristic LLM Heuristics LLM<br>InformationProblem GenerationPrompts Thinking Process Evaluate (Crossover, Mutate)# Reflect (ReEvo) Nature Evolving<br>Fitness<br>Metacognitive Driven<br>Refine Old<br>Generate<br>InformationProblem GenerationHeuristic Thinking LLM Heuristics Metacognitive Prompt Evolving LLM<br>Prompts Process Evaluate (Refine , Reflect)<br>Fitness<br><!-- End of picture text -->

Figure 1: Nature Evolving Driven & Metacognitive Driven Heuristic Generation Architecture 

This focus on the reasoning process inherently improves the quality and generality of the heuristics generated. However, we recognize that achieving robust performance in practice requires addressing challenges that extend beyond high-level strategy. This is particularly true for complex, illdefined real-world problems, such as Adaptive Curriculum Sequencing (ACS) (Prates et al. 2019) or Wireless Sensor Network (WSN) deployment (Chen et al. 2024). The ambiguity and situational dependencies of these problems frequently cause prior architectures to fail by generating syntactically or logically flawed code. To overcome these practical hurdles, MeLA is engineered with two novel support mechanisms: an **Automated Problem Analyzer** that formulates a rich problem description directly from source code, obviating the need for manual input, and an **Error Diagnosis System** that autonomously detects and rectifies programming flaws in the generated heuristics. These components grant MeLA a degree of autonomy and reliability essential for real-world application. 

In summary, this paper introduces MeLA, a metacognitive LLM-driven architecture that advances the state of the art in AHD. The primary contributions are: 

1. **A New AHD Paradigm:** We propose and validate _Prompt Evolution_ , which focuses on refining the LLM’s reasoning process rather than heuristics, leading to more stable and generalizable performance. 

2. **A Metacognitive Search Engine:** We introduce a novel search mechanism, inspired by metacognition, that enables the architecture to self-reflect and strategically improve its prompt-based problem-solving approach. 

3. **Robustness for Real-World Application:** We equip the architecture with automated problem analysis and error diagnosis capabilities, significantly enhancing its autonomy and making it the first LLM-based AHD framework demonstrated to be effective on complex, ill-defined realworld problems. 

## **Literature Review** 

### **Heuristic Design with Large Language Models** 

The integration of LLMs with evolutionary computation now defines the frontier of Automatic Heuristic Design (Huang et al. 2025). This approach has yielded a new 

generation of architectures capable of generating remarkably high-quality heuristics. A seminal example is FunSearch (Romera-Paredes et al. 2024), which pairs a pretrained LLM with a systematic evaluator to discover genuinely novel constructions for long-standing mathematical challenges, including the cap set and online bin packing problems. Building on this direction, the Evolution of Heuristics (EoH) (Liu et al. 2024) architecture established a paradigm for generalizable and efficient design through the dual evolution of thoughts and code, supported by multistrategy prompt engineering. The success of this approach has already inspired further development in multi-objective contexts, such as MEoH (Yao et al. 2025). Concurrently, Reflective Evolution (ReEvo) (Ye et al. 2024) introduced an innovative self-refining mechanism that substantially reduces the dependence on predefined heuristic component libraries, a traditional requirement of AHD. 

While powerful, these state-of-the-art architectures share a common paradigm rooted in natural selection: they apply evolutionary pressure directly to the generated heuristics. In this model, the LLM functions as a sophisticated evolutionary operator that produces candidate solutions, which are then evaluated and selected based on their performance. This focus on the final product, rather than the generative process that created it, represents a fundamental limitation that leaves significant potential for more intelligent and adaptive search untapped. 

### **Prompt Evolution for LLM-Driven Optimization** 

Given the limitations of evolving heuristics, the logical next step is to evolve the generative process itself. A promising paradigm for this task is **Prompt Evolution** (Sahoo et al. 2024). Research in this area has demonstrated that iteratively refining an LLM’s instructional prompt can dramatically improve the quality and specificity of its output. For instance, Li et al. (2023) designed a black-box evolutionary algorithm called SPELL that uses an LLM to iteratively improve its prompts (Li and Wu 2023). Similarly, the Promptbreeder mechanism was proposed to evolve and adapt prompts for specific domains by treating them as mutable tasks (Fernando et al. 2023). Other works have confirmed the efficacy of using evolutionary algorithms to generate prompts through dynamic interaction with the model (Martins et al. 2023). 

These methods confirm that the reasoning pathway of an LLM is a viable and potent target for optimization. However, the application of prompt evolution to the structured, high-stakes domain of AHD remains a critical and unexplored research gap. In its current form, prompt evolution is often an unguided search, lacking a higher-level intelligence to direct its path efficiently and strategically. This raises a crucial question: how can a system learn to evolve its prompts in a principled manner? 

### **Metacognition as a Framework for Self-Regulation** 

A robust answer to this question is found in the cognitive science of **metacognition** . A fundamental distinction exists between cognition and metacognition: the cognitive system executes tasks (e.g., information retrieval), 



<!-- Start of picture text -->
Automated Problem Heuristics  Heuristics<br>Best Heuristic<br>Analysis Iteration 1 Iteration 2<br>Error Diagnosing  Record<br>Problem<br>Information ...<br>Thought Processes<br>Errors Evaluate Replace ...<br>Errors<br>Error Handling<br>Correct<br>LLM ...<br>Error<br>HEUs Fitness Value<br>NP-hard  Best Heuristic<br>Analyzing<br>Fail Success<br>LLM<br>New Heuristics Evaluation<br>Analyzing Key Fitness<br>... ... Boost Prompts<br>Retaining Optimal  Meta-<br>Heuristic's Components cognitive<br>Initial Thought Processes... GenerationHeuristicsLLM New Prompt Better ComponentsSearching For  LLM<br>Prompt<br>Generation Metacognition<br><!-- End of picture text -->

Figure 2: Flowchart of MeLA. 

whereas the metacognitive system regulates these activities through higher-order processes of planning, monitoring, and evaluation (Lai 2011). Empirical studies demonstrate that individuals with well-developed metacognitive competence hold significant advantages: they can detect deficits in their own understanding and dynamically adjust their cognitive strategies based on performance outcomes (Akturk and Sahin 2011). This capacity for self-regulation, often termed learning to learn, is crucial for adaptability in complex environments (Dunlosky and Metcalfe 2008; Cox 2005). 

This concept has recently found traction in AI research, with studies exploring how to instill metacognitive capabilities in AI agents (Lin and Wei-Kocsis 2025; Wang and Zhao 2023) and LLMs specifically (Li et al. 2025). For heuristic design, metacognition offers the perfect blueprint for an architecture that does not just generate solutions, but actively analyzes its own problem-solving process to become a better problem-solver over time. However, despite its clear relevance, the strategic framework of metacognition has not yet been leveraged to guide the generative process within AHD. 

### **Summary and Identified Research Gap** 

The foregoing review reveals a compelling opportunity at the intersection of three distinct fields. Current AHD architectures are powerful yet constrained by a paradigm that evolves heuristics. Prompt evolution offers a mechanism for process refinement but lacks strategic guidance. Finally, metacognition provides the theoretical blueprint for intelligent, autonomous self-regulation. This paper bridges these 

domains by introducing MeLA, an architecture that operationalizes metacognitive principles to drive prompt evolution, thereby forging a new and more powerful path for Automatic Heuristic Design. 

## **Methodology** 

### **Main Idea & System Role** 

MeLA introduces a paradigm shift in AHD by focusing on the metacognitive process of prompt evolution. It also incorporates automatic problem analysis and error correction mechanisms to enhance the architecture’s versatility and robustness across a range of challenges, from classical benchmarks to complex real-world problems. 

Previous architectures have concentrated on the generated heuristics themselves, employing crossover and mutation based on performance. This reliance on a natural selectionbased evolutionary model can lead to instability, with inconsistent performance and significant variance among the generated heuristics. Furthermore, these approaches often lack the necessary mechanisms to effectively address the nuances of real-world problems and the errors that can arise in the generated heuristics. 

In contrast, MeLA emphasizes the ”why such heuristics are generated”. This means MeLA focuses on the thought processes that LLMs generate when creating heuristics. The quality of this thought process directly correlates with the heuristic’s performance; a sound line of reasoning leads to superior results, while flawed logic results in poor performance. By integrating metacognition, 

MeLA analyzes these LLM-generated thought processes to identify and retain the most effective reasoning patterns that contribute to improved heuristic performance. This allows the system to identify optimal heuristics and formulate new, more effective prompts to guide the LLM in subsequent heuristic generation, constituting a form of prompt evolution. The robustness of MeLA is further enhanced by its automated problem analysis and error diagnosis capabilities. 

To operationalize this approach, MeLA introduces three distinct system roles: 

- **NP-hard Problem Analysis Expert:** This role is responsible for analyzing the code-based representations of NP-hard problems. It identifies key parameter characteristics and examines the fundamental challenges inherent in these problems, providing a solid foundation for heuristic design. 

- **Elite Code Debugger:** This system component addresses errors within the generated heuristics. It analyzes execution failures, identifies the root causes of errors in the code, and applies targeted corrections while preserving the original problem-solving intent of the heuristic. 

- • **Metacognitive Reflector:** This role facilitates introspection on the thought processes and errors that occur during heuristic generation. Interpreted by the LLM as ”another version of oneself”, this component is crucial for selfregulation and strategic improvement. 

The detailed implementation of these system roles is further elaborated in the **Appendix** . A flowchart of the MeLA architecture is provided in **Figure 2** . 

**Algorithm 1** Iterative Heuristic Optimization 

- 1: **Input:** Problem _P_ , Number of Initializations _N_ , Generation Limit _L_ 

- 2: **Output:** Optimal Heuristic _Best_ ( _H_ ) 3: **procedure** OPTIMIZEHEURISTIC( _P, L_ ) 4: **for** _i ←_ 1 to _N_ **do** 5: _H, Th ←_ InitializeHeuristics(Analyze( _P_ )) 6: **end for** 7: **for** _j ← N_ + 1 to _L_ **do** 8: _f_ ( _H_ ) _, E ←_ Evaluate( _H_ ) 9: **if** _E̸_ = _∅_ **then** 

- 10: _H, Th ←_ CorrectErrors( _H, E, Th_ ) 11: _f_ ( _H_ ) _←_ Evaluate( _H_ ) 12: **end if** 13: _Meta ←_ AnalyzePerformance( _Th, f_ ( _H_ ) _,_ 14: _E, Best_ ( _H_ )) 15: _H, Th ←_ GenerateNext( _Meta_ ) 16: **end for** 17: **return** _Best_ ( _H_ ) 

- 18: **end procedure** 

### **Iteration Steps** 

The iterative optimization process of MeLA is detailed in Algorithm 1. At each iteration, MeLA maintains a population of heuristics, denoted as _H_ = _{h_ 1 _, . . . , hN }_ . Each 

heuristic _hi_ in this population is evaluated against a set of problem instances to determine its fitness value, _f_ ( _hi_ ). 

The optimization loop begins with an initial problem **Analyze** , which informs the **InitializeHeuristics** step, where the first population of heuristics _H_ and their corresponding thought processes _Th_ are generated. Subsequently, the core iterative cycle commences. First, all heuristics in the current population are subjected to **Evaluation** , which yields their fitness scores _f_ ( _H_ ) and records any execution errors _E_ . If _E_ are detected, the **CorrectErrors** procedure is invoked to repair the faulty heuristics and update the population _H_ , thought processes _Th_ and fitness _f_ ( _H_ ). Following this, the **AnalyzePerformance** stage initiates a metacognitive review _Meta_ . It assesses the recorded thought processes _Th_ , the fitness landscape of the population _f_ ( _H_ ), the errors _E_ and the characteristics of the best-performing heuristic _Best_ ( _H_ ) to generate a new set of refined prompts. These prompts are then used by the **GenerateNext** function to produce the next generation of heuristics _H_ and thoughts _Th_ . This cycle of evaluation, correction, analysis, and generation repeats, driving the continuous refinement of the underlying problem-solving strategies. 

### **Prompt Evolution** 

Prompt evolution in MeLA is a structured, reflective process driven by the metacognition phase. During this phase, MeLA leverages a comprehensive record of the iterative history—including the thought processes, execution errors, and resulting fitness values of all generated heuristics. The metacognitive analysis then evolves the guiding prompt by focusing on three key objectives: 

- **Reinforcement:** Identifying and reinforcing the reasoning patterns within the thought processes that correlated with fitness improvements. 

- **Preservation:** Isolating and preserving high-performing components from the best heuristic, such as specific search strategies. 

- **Innovation:** Hypothesizing novel components or modifications that could lead to further performance gains. 

- A concrete example illustrating this prompt evolution pro- 

- cess is detailed in the **Appendix** . 

### **Challenges in Real-World Problems** 

While architectures like EoH and ReEvo have demonstrated commendable performance on classical benchmark problems, they face significant challenges when applied to realworld optimization scenarios. These problems are often high-dimensional and richly parameterized, requiring meticulously detailed descriptions to guide the LLM toward generating feasible heuristics. Crafting such descriptions is nontrivial; it demands deep user expertise both in the problem domain and in the nuances of interacting with LLMs. This dependency on manual, expert-driven problem formulation limits their applicability and scalability for diverse real-world challenges. For a detailed guide on the modifications required to enable the execution of EoH and ReEvo on these complex problems, please refer to the **Appendix** . 

Compounding this issue, even with well-crafted problem descriptions, both EoH and ReEvo exhibit a high probability of generating non-executable heuristics. This stems from the inherent difficulty an LLM faces in translating complex, multi-parameter problem specifications into syntactically and logically correct code, leading to errors such as undefined parameters or out-of-bounds array access. While this has a lesser impact on an architecture like EoH, which does not strictly depend on a population of valid individuals, it poses a critical failure point for ReEvo. The crossover mechanism in ReEvo requires executable parent heuristics; if none can be successfully generated, the evolutionary process halts entirely. 

MeLA is specifically engineered to overcome these limitations. It utilizes an LLM’s analytical capabilities to approach problem understanding from an expert perspective, thereby enhancing the accuracy and versatility of heuristic generation. Crucially, it integrates a robust error diagnosis and correction mechanism to dramatically increase the rate of producing executable code. 

### **Predefined Prompts** 

MeLA’s operation is guided by four distinct, predefined prompts designed to steer the LLM through the heuristic design process. 

- **Problem Analysis Prompt:** The LLM first analyzes the problem’s complete Python code to produce an expert description of its key characteristics and inherent computational difficulty. This analysis grounds the entire process. 

- **Generation Prompts:** These prompts create the heuristics. The **Initial Generation** prompt uses the problem analysis to produce a diverse population of _N_ heuristics. Subsequently, the **Metacognitive Generation** prompt uses insights from the metacognition step to evolve this population, generating _N_ refined heuristics for the next iteration. 

- **Error Prompt:** If a heuristic fails during evaluation, the LLM receives the faulty code and its corresponding error message. It then attempts to generate a corrected version up to _M_ times. The best-performing valid candidate replaces the original; if all attempts fail, the heuristic’s failure is logged. 

- **Metacognition Prompt:** This core prompt drives prompt evolution by instructing the LLM to analyze the iteration’s complete history (all thought processes, errors, and fitness values). It performs a self-reflective analysis to: 1) identify reasoning patterns that led to improved fitness, 2) preserve high-performing components (e.g., a search strategy like L´evy Flight) from the best heuristic, and 3) hypothesize new strategies for further enhancement. The output of this prompt directly informs the Metacognitive Generation prompt. 

Full prompt details are provided in the **Appendix** . 

## **Experiments** 

### **Experimental Setup** 

To rigorously evaluate the performance and versatility of MeLA, we designed an experimental suite comprising three distinct categories of optimization challenges: a classical benchmark, a black-box benchmark, and two complex realworld problems. This selection allows for a comprehensive assessment of the architecture’s capabilities across various scenarios. The chosen problems are: 

- **Traveling Salesperson Problem (TSP):** A canonical NP-hard problem requiring the determination of the most efficient route that visits a set of cities exactly once before returning to the origin. In the experiment, the initial population size is 30, the evolutionary population size is 10, and a total of 100 solutions are generated. 

- **Bin Packing Problem (BPP):** A classic black-box combinatorial optimization problem that involves packing items of varying sizes into the minimum number of fixedcapacity containers (Ross et al. 2002). It serves as a benchmark for resource allocation challenges. In the experiment, the initial population size is 30, the evolutionary population size is 10, and a total of 50 solutions are generated. 

- **Adaptive Curriculum Sequencing (ACS):** A complex, real-world combinatorial optimization problem from the domain of e-learning. ACS involves generating personalized learning paths by balancing learner characteristics (e.g., knowledge level, attention span) with pedagogical constraints (e.g., concept dependencies, difficulty levels). As an NP-Hard problem, it requires optimizing multiple, often conflicting, objectives. In the experiment, the initial population size is 20, the evolutionary population size is 10, and a total of 50 solutions are generated. 

- **Wireless Sensor Network (WSN) Deployment:** A realworld optimization problem from the communications domain, abbreviated herein as WSN. The goal is to optimize the placement and power management of sensor nodes to maximize network coverage and connectivity while minimizing total energy consumption, addressing NP-hard challenges like the Minimum Power k-Coverage problem. In the experiment, the initial population size is 20, the evolutionary population size is 10, and a total of 50 solutions are generated. 

In TSP and BPP problems, we optimize the heuristic information based on Ant Colony Optimization (ACO). The core mechanism of ACO involves guiding random solution sampling through heuristic measures. This mechanism is naturally suitable for validating the value of AHD, which automatically designs these heuristic rules to guide the search process, replacing manually designed heuristic functions(Ye et al. 2024). In ACS and WSN problems, we optimize the heuristic algorithm. By evaluating the generated results of heuristic information and heuristic algorithms, we assess the excellent performance of MeLA. 

To ensure experimental fairness, EoH, ReEvo, and MeLA all use the same experimental parameters. 

|Method||TSP50||BPP500||ACS||WSN|
|---|---|---|---|---|---|---|---|---|
||SR (_↑_)|Obj. (_↓_)|SR (_↑_)|Obj. (_↓_)|SR (_↑_)|Obj. (_↓_)|SR (_↑_)|Obj. (_↓_)|
|GA|–|16_._75_±_0_._72|–|219_._60_±_0_._45|–|3927_._10_±_976_._76|–|1923_._17_±_0_._34|
|PSO|–|11_._46_±_0_._34|–|219_._30_±_0_._46|–|4067_._25_±_1095_._79|–|2674_._44_±_326_._81|
|SCSO|–|7_._87_±_0_._24|–|221_._71_±_0_._39|–|3875_._83_±_1939_._60|–|661_._00_±_199_._52|
|SOA|–|20_._48_±_0_._39|–|220_._22_±_0_._28|–|6349_._44_±_1504_._71|–|943_._69_±_80_._90|
|WO|–|20_._97_±_0_._29|–|221_._69_±_0_._37|–|6975_._08_±_7256_._24|–|1251_._25_±_670_._21|
|EoH<sup>_∗_</sup>|70.97%|5_._90_±_0_._02|88.54%|209_._08_±_4_._77|75.49%|1252_._88_±_794_._44|53.36%|177_._84_±_96_._32|
|ReEvo<sup>_∗_</sup>|89.46%|5_._89_±_0_._03|**96.73%**|208_._76_±_2_._06|40.71%|1848_._78_±_406_._90|56.52%|117_._61_±_18_._30|
|**MeLA**|**98.41%**|**5**_._**85**_±_**0**_._**01**|93.28%|**205**_._**48**_±_**0**_._**84**|**94.07%**|**589**_._**60**_±_**22**_._**79**|**99.21%**|**53**_._**89**_±_**2**_._**77**|



Table 1: Comparative Performance Analysis Across Different Problems 



Figure 3: Fitness Values of Different Architectures on Different Problems. ( MeLA, EoH, ReEvo ) 

The selection of ACS and WSN was specifically intended to test MeLA’s cross-domain execution capabilities, and all four problems are formulated as minimization tasks. We selected DeepSeek-V3-0324 as the core generative engine due to its strong metacognitive reasoning capabilities. As our preliminary tests confirmed that performance is primarily driven by the MeLA architecture itself, not the specific LLM, this work focuses on validating the framework with a single capable model. 

For our comparative analysis, we benchmarked MeLA against five traditional metaheuristics (Genetic Algorithm (GA) (Holland 1992), Particle Swarm Optimization (PSO) (Kennedy and Eberhart 1995), Sand Cat Swarm Optimization (SCSO) (Seyyedabbasi and Kiani 2023), Skill Optimization Algorithm (SOA) (Givi and Hubalovska 2023), and Walrus Optimization (WO) (Han et al. 2024)) and two state-of-the-art LLM-driven architectures (Evolution of Heuristics (EoH) (Liu et al. 2024) and Reflective Evolution (ReEvo) (Ye et al. 2024)). 

It should be emphasized that for excellent algorithms such as GA, in the TSP and BPP problems, we evaluate the ACO’s performance with heuristic information designed by these algorithms, while in the ACS and BPP problems, we evaluate the algorithms themselves. 

The details of these comprehensive definitions and constraints for all problems are documented in the **Appendix** . 

### **Results and Analysis** 

The experimental results across the four problem domains are summarized in **Figure 3** and **Table 1** . **Figure 3** illustrates a representative convergence plot from one of our independent runs. Due to the stochastic nature of LLMbased generation, an optimal heuristic may occasionally be found during initialization; presenting a run that demonstrates clear iterative improvement provides a more insightful view of an architecture’s dynamic behavior. As shown, MeLA consistently achieves superior fitness values across all four problems, with particularly significant advantages over EoH and ReEvo on the BPP and ACS problems. 

A quantitative summary of our findings over three independent runs, including heuristic success rates (SR) and final fitness values, is presented in **Table 1** . The data confirms MeLA’s superior performance on the TSP, ACS, and WSN problems in terms of both success rate and average final fitness. The advantage is most pronounced in realworld scenarios. For the ACS problem, MeLA’s success rate is 18.58% and 53.36% higher than EoH and ReEvo, respectively, while achieving a final fitness that is 52.94% and 68.11% better. Similarly, on the WSN problem, MeLA achieves a 69.70% and 54.18% higher success rate and improves the final fitness by 71.30% and 48.27%. For the BPP problem, while ReEvo records a marginally higher success rate (by 3.45%), MeLA still secures the best average fitness, indicating its overall effectiveness. Finally, when compared against traditional metaheuristics on the ACS and 



Figure 4: Performance of Optimal Heuristic Generated by Different Architectures. 

WSN problems, all modern AHD architectures demonstrate a clear advantage, affirming the power of this paradigm for complex, multi-parameter optimization. 

Beyond aggregate performance, we analyzed the generality and stability of the single best heuristic generated by each architecture, with results detailed in **Figure 4** . For the TSP and BPP, we tested generalization by evaluating the heuristics on 64 different larger-scale instances over 10 independent runs. For the complex ACS and WSN problems, we tested performance stability by re-executing the optimal heuristics 30 times with different random seeds. In all scenarios, the heuristic generated by MeLA demonstrated the most stable and superior performance. This was particularly evident for the ACS and WSN problems, where the heuristic not only exhibited minimal deviation but consistently converged to its optimal fitness value in nearly every run, confirming its exceptional quality and reliability. 

The specific parameters used for all problems and the code for the optimal heuristics generated by each architecture are available in the **Appendix** . 

### **Ablation Analysis** 

To validate the individual contributions of MeLA’s core components, we conducted a series of ablation studies. We systematically analyzed the impact of: Prompt Evolution, the Automated Problem Analysis mechanism, the Error Diagnosis mechanism, and the Metacognitive Search component. 

- **Prompt Evolution:** The superiority of Prompt Evolution over traditional natural selection is demonstrated by MeLA’s overall performance in **Table 1** and **Figure 4** . On classic benchmarks, it yields heuristics with superior fitness, an advantage particularly pronounced on the BPP. On real-world problems, it produces solutions that are not only higher-performing but also significantly more stable. This confirms that evolving the underlying reasoning process is a more effective and robust strategy than evolving the heuristic code directly. 

- **Automated Problem Analysis (PA) Mechanism:** To isolate the effect of the PA mechanism, we compared initialization performance with and without this component. 

As shown in **Table 2** , the PA mechanism provides a moderate fitness improvement across problems and, critically, yields a significant increase in the initial heuristic success rate on the black-box BPP challenge. 

- **Error Diagnosis Mechanism:** The efficacy of the Error Diagnosis mechanism is clearly evidenced by the heuristic success rates presented in **Table 1** . MeLA’s ability to achieve near-perfect execution rates, especially on complex real-world problems where baselines like EoH and ReEvo falter, is a direct result of this component’s ability to autonomously repair faulty code. 

- **Metacognitive Search Component:** The impact of the Metacognitive Search component is demonstrated by comparing the average fitness values before and after its application ( **Table 2** ). For the ACS problem, each successive metacognitive stage delivers a clear and consistent improvement in fitness. On the BPP, the first metacognitive stage provides a substantial fitness gain, with subsequent stages showing diminishing returns as the heuristics approach a strong optimum. Furthermore, this component helps maintain or improve heuristic success rates throughout the evolutionary process, as seen in the final 100% success rate for ACS after the third stage. 

|PA/Meta|BP|P|A|CS|
|---|---|---|---|---|
||Avg. (_↓_)|SR(_↑_)|Avg. (_↓_)|SR(_↑_)|
|Have PA|221_._50|70.00%|4434_._14|100.00%|
|No PA|221_._80|56.67%|4447_._32|93.33%|
|Initial|219_._61|86.67%|5335_._47|95.00%|
|Meta-1|207_._16|90.00%|4311_._72|90.00%|
|Meta-2|207_._20|90.00%|3642_._88|90.00%|
|Meta-3|–|–|3530_._78|100%|



Table 2: Ablation results. 

## **Conclusion** 

This paper introduces MeLA, a novel architecture that marks a significant advance in Automatic Heuristic Design. By 

pioneering _prompt evolution_ , MeLA shifts the focus from evolving heuristic code—the standard in natural selectionbased methods—to evolving the underlying reasoning process that generates the heursitic. Central to our approach is a metacognitive framework that enables the system to iteratively refine its generative strategy. This allows MeLA to discover high-performing thought patterns to get superior solution quality and execution success rates across a diverse range of optimization challenges. 

This shift from direct code manipulation to cognitive framework optimization allows MeLA to overcome the limitations of prior approaches. Furthermore, by making the thought process the target of optimization, MeLA yields a unique and powerful form of interpretability. Unlike evolving cryptic heuristics, MeLA produces an optimized prompt, which is human-readable. This prompt serves as a reusable, high-level strategy that can be understood, manually refined, and easily adapted by human experts, bridging the gap between automated discovery and human-centric problemsolving. Our results validate prompt evolution as a powerful and robust paradigm, offering a more stable and adaptable method for generating high-quality heuristics, particularly for complex real-world problems. 

For future work, a key direction will be to investigate the performance of MeLA with different underlying LLMs. Such experiments will not only explore the trade-offs between various models but also further validate the modelagnostic nature of the MeLA framework, enhancing its generalizability. 

## **Acknowledgments** 

This work is supported by the Ningbo Municipal Bureau of Science and Technology (Grant No. 2025Z197). 

## **References** 

Akturk, A. O.; and Sahin, I. 2011. Literature review on metacognition and its measurement. _Procedia-Social and Behavioral Sciences_ , 15: 3731–3736. 

Burke, E. K.; Hyde, M. R.; Kendall, G.; and Woodward, J. 2007. Automatic heuristic generation with genetic programming: evolving a jack-of-all-trades or a master of one. In _Proceedings of the 9th annual conference on Genetic and evolutionary computation_ , 1559–1565. 

Chen, L.; Qiu, Z.; Wu, Y.; and Tang, Z. 2024. Optimizing k-coverage in energy-saving wireless sensor networks based on the Elite Global Growth Optimizer. _Expert Systems with Applications_ , 256: 124878. 

Cox, M. T. 2005. Metacognition in computation: A selected research review. _Artificial intelligence_ , 169(2): 104–141. Dunlosky, J.; and Metcalfe, J. 2008. _Metacognition_ . Sage Publications. 

Fernando, C.; Banarse, D.; Michalewski, H.; Osindero, S.; and Rockt¨aschel, T. 2023. Promptbreeder: Self-referential self-improvement via prompt evolution. _arXiv preprint arXiv:2309.16797_ . 

Givi, H.; and Hubalovska, M. 2023. Skill Optimization Algorithm: A New Human-Based Metaheuristic Technique. _Computers, Materials & Continua_ , 74(1). 

Han, M.; Du, Z.; Yuen, K. F.; Zhu, H.; Li, Y.; and Yuan, Q. 2024. Walrus optimizer: A novel nature-inspired metaheuristic algorithm. _Expert Systems with Applications_ , 239: 122413. 

Holland, J. H. 1992. Genetic algorithms. _Scientific american_ , 267(1): 66–73. 

Huang, Z.; Wu, W.; Wu, K.; Wang, J.; and Lee, W.B. 2025. Calm: Co-evolution of algorithms and language model for automatic heuristic design. _arXiv preprint arXiv:2505.12285_ . 

Kennedy, J.; and Eberhart, R. 1995. Particle swarm optimization. In _Proceedings of ICNN’95-international conference on neural networks_ , volume 4, 1942–1948. ieee. 

Lai, E. R. 2011. Metacognition: A literature review. 

Li, W.; Li, D.; Dong, K.; Zhang, C.; Zhang, H.; Liu, W.; Wang, Y.; Tang, R.; and Liu, Y. 2025. Adaptive tool use in large language models with meta-cognition trigger. _arXiv preprint arXiv:2502.12961_ . 

Li, Y. B.; and Wu, K. 2023. Spell: Semantic prompt evolution based on a llm. _arXiv preprint arXiv:2310.01260_ . 

Lin, W.; and Wei-Kocsis, J. 2025. Think, Reflect, Create: Metacognitive Learning for Zero-Shot Robotic Planning with LLMs. _arXiv preprint arXiv:2505.14899_ . 

Liu, F.; Tong, X.; Yuan, M.; Lin, X.; Luo, F.; Wang, Z.; Lu, Z.; and Zhang, Q. 2024. Evolution of heuristics: Towards efficient automatic algorithm design using large language model. _arXiv preprint arXiv:2401.02051_ . 

Martinez, M. E. 2006. What is metacognition? _Phi delta kappan_ , 87(9): 696–699. 

Martins, T.; Cunha, J. M.; Correia, J.; and Machado, P. 2023. Towards the evolution of prompts with metaprompter. In _International Conference on Computational Intelligence in Music, Sound, Art and Design (Part of EvoStar)_ , 180–195. Springer. 

Mei, Y.; Chen, Q.; Lensen, A.; Xue, B.; and Zhang, M. 2022. Explainable artificial intelligence by genetic programming: A survey. _IEEE Transactions on Evolutionary Computation_ , 27(3): 621–641. 

Pillay, N.; and Qu, R. 2018. _Hyper-heuristics: theory and applications_ . Springer. 

Prates, M.; Avelar, P. H.; Lemos, H.; Lamb, L. C.; and Vardi, M. Y. 2019. Learning to solve np-complete problems: A graph neural network for decision tsp. In _Proceedings of the AAAI conference on artificial intelligence_ , volume 33, 4731–4738. 

Romera-Paredes, B.; Barekatain, M.; Novikov, A.; Balog, M.; Kumar, M. P.; Dupont, E.; Ruiz, F. J.; Ellenberg, J. S.; Wang, P.; Fawzi, O.; et al. 2024. Mathematical discoveries from program search with large language models. _Nature_ , 625(7995): 468–475. 

Ross, P.; Schulenburg, S.; Mar´ın-Bl¨azquez, J. G.; and Hart, E. 2002. Hyper-heuristics: learning to combine simple heuristics in bin-packing problems. In _Proceedings of the 4th annual conference on genetic and evolutionary computation_ , 942–948. 

Sahoo, P.; Singh, A. K.; Saha, S.; Jain, V.; Mondal, S.; and Chadha, A. 2024. A systematic survey of prompt engineering in large language models: Techniques and applications. _arXiv preprint arXiv:2402.07927_ . 

Seyyedabbasi, A.; and Kiani, F. 2023. Sand Cat swarm optimization: A nature-inspired algorithm to solve global optimization problems. _Engineering with computers_ , 39(4): 2627–2651. 

Wang, Y.; and Zhao, Y. 2023. Metacognitive prompting improves understanding in large language models. _arXiv preprint arXiv:2308.05342_ . 

Wolpert, D. H.; and Macready, W. G. 1997. No free lunch theorems for optimization. _IEEE transactions on evolutionary computation_ , 1(1): 67–82. 

Yao, S.; Liu, F.; Lin, X.; Lu, Z.; Wang, Z.; and Zhang, Q. 2025. Multi-objective evolution of heuristic using large language model. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 39, 27144–27152. 

Ye, H.; Wang, J.; Cao, Z.; Berto, F.; Hua, C.; Kim, H.; Park, J.; and Song, G. 2024. Reevo: Large language models as hyper-heuristics with reflective evolution. _arXiv preprint arXiv:2402.01145_ . 

Zhang, R.; Liu, F.; Lin, X.; Wang, Z.; Lu, Z.; and Zhang, Q. 2024. Understanding the importance of evolutionary search in automated heuristic design with large language models. In _International Conference on Parallel Problem Solving from Nature_ , 185–202. Springer. 

## **Appendix** 

### **A.1 Errors** 

Here are the errors that may occur during the heuristic operation of LLM generation. 

ValueError: operands could not be broadcast together with shapes (50,) (50,150) TypeError: ’numpy.float64’ object is not callable IndexError: too many indices for array: array is 1-dimensional, but 2 were indexed ValueError: operands could not be broadcast together with shapes (50,) (50,150) IndexError: invalid index to scalar variable. ValueError: operands could not be broadcast together with shapes (50,150) (50,) SyntaxError: ’[’ was never closed SyntaxError: Generator expression must be parenthesized SyntaxError: ’[’ was never closed SyntaxError: ’[’ was never closed ValueError: probabilities contain NaN SyntaxError: closing parenthesis ’]’ does not match opening parenthesis ’(’ SyntaxError: ’[’ was never closed 

Figure A1: Incomplete problem descriptions will result in no runnable heuristics for both EoH and ReEvo. 

### **A.2 Prompt Evolution** 

The process of prompt evolution based on metacognition is shown in the figure below. As illustrated in the figure, this flowchart demonstrates a systematic metacognition-driven prompt evolution framework integrating thought processes, fitness evaluation, and large language model (LLM) interaction. The left panel displays initial heuristic configurations (v1) with corresponding fitness scores (3656.5 and 1669.8125), featuring optimization components such as exploration/exploitation balance and adaptive cosine-based movement. The central metacognition module performs critical analysis, evaluating key aspects including the retention of Levy flights for global search and dynamic scaling mechanisms. This reflective process informs the LLM’s prompt generation, yielding an optimized thought process (heuristics ~~v~~ 2) on the right, which achieves significantly improved performance (fitness: 615.0625) through enhanced Levy flight implementation and fitness-aware restart mechanisms. The diagram visually captures the iterative refinement cycle where metacognitive analysis guides LLM-mediated prompt optimization, demonstrating measurable fitness improvement across generations. An example can be seen in **Figure A2** . 

### **A.3 The Problem Descriptions of EoH and ReEvo** 

The problem description for EoH and ReEvo needs to be designed as follows for proper operation. Incomplete problem descriptions will result in no runnable heuristics for both EoH and ReEvo. For EoH, with a complete problem description, it achieves a runnable heuristic generation rate of 75.49%, while ReEvo only reaches 40.41%. However, ReEvo can now run normally under these conditions. Refer to **Figure A3** for details. 

### **A.4 System Role & Full Prompt** 

For details on the specific system roles and various prompt expressions, please refer to **Figure A4** and **Figure A5** . 

### **A.5 Problems** 

All experiments were performed on a 48-core computer with an Intel Xeon Gold 6248R 3.00GHz CPU, running Windows 10 Pro and equipped with 255GB of RAM. 

The relevant parameters for the four questions are shown in Table 1. When experimenting with different problem sizes for TSP and BPP, we ensure the use of the same dataset, with its generation criteria based on ReEvo (Ye et al. 2024). This paper will not provide further explanation for these two experiments. If needed, please directly refer to the sections in ReEvo concerning TSP50, TSP100, BPP500, and BPP1000. The operating parameters for these two issues are shown in **Table A1** and **Table A2** . 

This paper will now focus on explaining the ACS and WSN problems. 

_•_ ACS: In the ACS problem, we consider real-world scenarios and utilize the Open University Learning Analytics Dataset (OULAD) for modeling and optimizing ACS solutions. It includes data from 10,000 learners, information on 7 selected courses, learner profiles, and their interactions with the virtual learning environment. To reflect realistic teaching conditions, we set the number of learners enrolled in a single course to 30, with a total of 20 concepts to be mastered in the course. The learning materials consist of 120 items, each covering at least one concept, but none covering all 20 concepts. Due to the high complexity 



Figure A2: An example of Prompt Evolution. 

#### **Initial Description** 

Implement a function that performs adaptive course material recommendation using the SCSO metaheuristic optimization algorithm. Heuristic operation success rate : EOH - 5% ReEvo - The operation rate is too low to proceed to the crossover and mutation stages. 

#### **Complete Description** 

|Implement a function that performs adaptive course material recommendation using the SCSO metaheuristic optimiza-<br>tion algorithm. The function must:|
|---|
|1. Strict Requirements for Parameter Access:|
|- All parameters must be accessed using OBJECT.ATTRIBUTE notation only<br>- NEVER use dictionary-style access like data<br>~~a~~l[’lb’] or data<br>~~a~~l[0]|
|- Required parameter accesses that must use dot notation:<br>* data<br>~~a~~l.lb - lower bounds|
|* data<br>~~a~~l.ub - upper bounds|
|* data<br>~~a~~l.dim - problem dimension|
|* data<br>~~a~~l.SearchAgents - population size|
|* data<br>~~a~~l.MaxIter - maximum iterations|
|2. Mandatory Implementation Structure:|
|# 1. Parameter initialization (MUST use dot notation)|
|lb = np.array(data<br>~~a~~l.lb)<br> <br>|
|ub = np.array(data<br>~~a~~l.ub)|
|dim = data<br>~~a~~l.dim|
|SearchAgents<br>~~n~~o = data<br>al.SearchAgents|
|# 2. Position initialization<br><br>|
|ub<br>~~a~~rray = np.array(ub)<br><br>|
|lb<br>array = np.array(lb)|
|position initialization logic<br>|
|3. Core Algorithm Requirements:<br>- Must implement both exploration and exploitation phases<br>- Must include boundary constraint handling|
|- Must use cosine-based position updates|
|- Must maintain roulette wheel selection|
|4. Input/Output Specifications:<br>|
|Input Parameters:|
|- data<br>al: Algorithm config object with dot-accessible attributes<br>- data<br>pb: Problem data object|
|- Positions: Current population positions<br>- Best<br>~~p~~os: Current best solution|
|- Best<br>~~s~~core: Current best fitness|
|- rg: Current search radius|
|Returns:|
|- Updated Positions array only|
|- NO other return values allowed|
|Heuristic operation success rate: EOH - 75.49% ReEvo - 40.71%|



Figure A3: Incomplete problem descriptions will result in no runnable heuristics for both EoH and ReEvo. 

#### **NP-hard Problem Analysis Expert** 

Act as an NP-hard problem analyst. Please analyze the characteristics and solutions of the NP-hard problem. **Elite Code Debugger** You are an elite Code Debugging. Please correct the Python code. The code generation format must strictly follow the example below: _{_ thought process: 1.xxx 2.xxx ... _}_ “‘python import numpy as np def heuristics ~~v~~ 1(data ~~a~~ l, data ~~p~~ b, Positions, Best ~~p~~ os, Best ~~s~~ core, rg): * The rest remains unchanged. * #EVOLVE-START * Your optimized code * #EVOLVE-END return Positions “‘ **Metacognition Role** You are another version of yourself, a process of thinking and a set of errors through which you come to understand yourself. Please analyze the thought process records, errors, and the optimal algorithm. 

Figure A4: System Role 

**Problem Analysis Prompt** I have an existing problem with the code as follows: _{_ problem _}_ . Please analyze the problem. Your analysis must be within 50 words. **Generation Prompt Generation 1** _{_ problem _}_ I have an initial algorithm with the code as follows: _{_ init ~~c~~ ode _}_ . And the optimization history it presents in the problem is as follows: _{_ init ~~e~~ val _}_ . Please help me create a new algorithm that has a totally different form from the given ones but can be motivated from them. 1.Analyze the history of fitness values and optimize the algorithm with the goal of surpassing the optimal value. 2.You will notice that there are #EVOLVE-START and #EVOLVE-END comments in the following code. The code within these comments is the part that you need to optimize. 3.The code: _{_ code _}_ . Analyze the algorithm, optimize the algorithm. Record your thought process in the _{}_ brackets. 4.Your thought process must be within 50 words. **Generation 2** The reflection results of metacognition are as follows: _{_ metacognition _}_ . I have a existing algorithm with their codes as follows: _{_ init ~~c~~ ode _}_ . The optimization history it presents in the optimization problem is as follows: _{_ init ~~e~~ val _}_ . Please retain the advantageous components and innovate to improve the deficient ones. 1.You will notice that there are #EVOLVE-START and #EVOLVE-END comments in the following code. The code within these comments is the part that you need to optimize. 2.The code: _{_ code _}_ . Analyze the algorithm, optimize the algorithm.Record your thought process in the _{}_ brackets. 3.Your thought process must be within 50 words. **Error Prompt** The code you generated _{_ code ~~s~~ tr _}_ has the following error _{_ str ~~e~~ rror _}_ . Please make it correct and functional. **Metacognition Prompt** The thinking process and score of each algorithm are as follows: _{_ thoughts _}_ . The errors are as follows: _{_ errors _}_ . You should avoid the errors and ensure that no new error. The optimal algorithm is as follows: _{_ code _}_ . Please conduct metacognitive reflection on your own thinking process, scores and mistakes. 1.Analyze the important considerations for optimizing fitness values. 2.The excellent components that should be retained in the optimal algorithm. 3.The components with better performance that need to be retained. 

4.Your output content must be within 80 words. 

Figure A5: Full Prompt 

of the problem, in evolutionary computation, we generally use multiple iterations of Search Agents in a single experiment to find feasible solutions. Therefore, in this problem, a heuristic evaluation method is generated by having 20 agents search for the optimal solution over 50 iterations to assess the performance of the heuristic. The relevant operating parameters are shown in **Table A3** . 

The constraints in the ACS experimental setup are carefully designed to model realistic learning constraints and priorities. The penalty factor _ε_ 1 (set to 1) applies when learners exceed the required number of concepts, while _ε_ 2 (10<sup>4</sup> ) imposes a significantly higher penalty for failing to cover essential concepts, emphasizing comprehensive learning coverage. The attention span constraint is enforced through _ε_ 3 (1000), penalizing excessive cognitive load. Weight coefficients _ω_ 1 (0.25), _ω_ 2 (1), and _ω_ 3 (0.25) balance these penalties, with _ω_ 2 giving strongest emphasis to concept coverage completeness. Priority-based material limits are implemented through _ψ_ 1 (3) for high-priority content, _ψ_ 2 (6) for medium-priority, and _ψ_ 3 (1) for challenging materials, ensuring appropriate distribution of learning resources. These parameters collectively optimize the Adaptive Course Sequencing problem using OULAD data. Its constraint parameter table is detailed in **Table A5** . 

_•_ WSN: Wireless Sensor Networks deployment problem involving 200 fixed-position Sensing Nodes (SNs) and 50 Convergence Nodes (CNs) whose positions and transmission powers need to be optimized. The system aims to achieve three primary objectives: ensuring all SNs are connected to at least one CN, maintaining connectivity among all CNs, and minimizing total power consumption while meeting technical requirements. The network operates with CNs having a 20-unit communication range and a capacity constraint of serving no more than 15 SNs each, using a path loss model that includes a 55 dB base loss, 2.5 path loss exponent, additional quadrant-based loss factors ( _βx_ , _βy_ ), and a minimum required signal strength of -85 dBm. The optimization employs a population-based metaheuristic approach with 50 search agents running for 100 iterations, where each solution represents CN configurations through three parameters (x position, y position, and power level) bounded within [0,50] for coordinates and [0,30] dBm for power. The fitness function combines multiple components including coverage penalties (10 _×_ per uncovered SN), connectivity penalties (1000 for disconnected CN networks), power uniformity penalties (100 _×_ for excessive standard deviation beyond 1 dB), and the true fitness metric of total power consumption converted from dBm to milliwatts. A feasible solution must satisfy all constraints by covering all 200 SNs, maintaining full CN connectivity, keeping power uniformity within limits, and achieving a fitness score below the 1000 penalty threshold, with the framework providing convergence tracking and visualization capabilities to monitor optimization progress throughout this complex multi-constraint problem. For details of the parameters and constraints, please refer to **Table A4** and **Table A6** . 

The parameters of each meta-heuristic algorithm are shown in **Table A7** . 

### **A.6 Optimal Heuristics for different problems** 

MeLA generated the optimal heuristics for the four issues as **Listing 1** - **Listing 4** . 

|**Parameter Category**|**TSP**|
|---|---|
|LLM architecture|DeepSeek-V3-0324|
|LLM Temperature|1|
|Population Size|30 (initial), 10 (other)|
|Independent Runs|3|
|Solutions Generated|100|



Table A1: Parameter settings for the TSP problem 

|**Parameter Category**|**BPP**|
|---|---|
|LLM architecture|DeepSeek-V3-0324|
|LLM Temperature|1|
|Population Size|30 (initial), 10 (other)|
|Independent Runs|3|
|Solutions Generated|50|



Table A2: Parameter settings for the BPP problem 

|**Parameter Category**|**ACS**|
|---|---|
|LLM architecture|DeepSeek-V3-0324|
|LLM Temperature|1|
|Population Size|20 (initial), 10 (other)|
|Independent Runs|3|
|Solutions Generated|50|
|Problem Parameter||
|Materials|120|
|Concepts|20|
|Students|30|
|Iterative Parameter||
|Search Agents|20|
|Max Iterations|50|



Table A3: Parameter settings for the ACS problem 

|**Parameter Category**|**WSNs**|
|---|---|
|LLM architecture|DeepSeek-V3-0324|
|LLM Temperature|1|
|Population Size|20 (initial), 10 (other)|
|Independent Runs|3|
|Solutions Generated|50|
|Problem Parameter||
|Number of CN|50|
|Number of SN|200|
|Capacity|15|
|Connection Distance|20|
|SN Connect Param.|-85|
|Beta (_β_)|55|
|Gamma (_γ_)|2.5|
|Iterative Parameter||
|Search Agents|50|
|Max Iterations|100|



Table A4: Parameter settings for the WSNs problem 

|Parameter|Parameter Description|Value|
|---|---|---|
|_ε_1|Penalty factor for exceeding the<br>number of concepts required for<br>learning|1<br>|
|_ε_2|Penalty factor for not covering the<br>number of learning concepts|10<sup>4</sup>|
|_ε_3|Penalty factor for exceeding the at-<br>tention span|1000|
|_ω_1|Coefficient_ε_1<br>i|0.25<br>|
|_ω_2|Coefficient_ε_2<br>i|1<br>|
|_ω_3<br>|Coefficient_ε_3<br>|0.25<br>|
|_ψ_1<br>|High priority material quantity limit<br>|3<br>|
|_ψ_2|Medium priority material quantity<br>limit|6|
|_ψ_3|Challenging material quantity limit|1|



#### Table A5: ACS Constraints 

|**Parameter**|**Value**|**Description**|
|---|---|---|
|coverage|10|Penalty per uncovered sensor node|
|connectivity|1000|Penalty for disconnected network|
|power<br>std|100|Penalty for power standard deviation|



Table A6: WSN Constraints 

|**Metaheuristic**|**Parameter**|
|---|---|
|GA|_pc_= 0_._7_, pm_= 0_._1|
|PSO|_w_ = 0_._8_, c_1 = 2_._0_, c_2 = 2_._0|
|SCSO|_rG ∈_[2_,_0]|
|SOA|–|
|WO|_r_ = 0_._4|



Table A7: Algorithm Parameters 

10 11 12 13 

1 <mark>def heuristics_v2(distance_matrix):</mark> 2 <mark>#EVOLVE-START</mark> 3 <mark>eps = 1e-8</mark> 4 <mark>neigh_mean = np.mean(np.sort(distance_matrix, axis=1)[:,1:5], axis=1)</mark> 5 <mark>norm_term = (neigh_mean[:,None] + neigh_mean)/np.maximum(distance_matrix, eps)**2</mark> 6 <mark>return np.reciprocal(distance_matrix + eps) * norm_term</mark> 7 <mark>#EVOLVE-END</mark> 8 <mark>return 1 / distance_matrix</mark> 

#### Listing 1: TSP 

- 1 <mark>def heuristics_v2(node_attr, node_constraint):</mark> 

2 <mark>#EVOLVE-START</mark> 3 <mark>n = node_attr.shape[0]</mark> 4 <mark>attr_sum = node_attr[:, None] + node_attr[None, :]</mark> 5 <mark>constraint_diff = np.maximum(1e-6, abs(node_constraint - attr_sum))</mark> 6 <mark>weights = 1 / (1 + constraint_diff * node_attr.mean())</mark> 7 <mark>#EVOLVE-END</mark> 8 <mark>return weights</mark> 

Listing 2: BPP 

1 <mark>def heuristics_v2(Positions, Best_pos, Best_score, rg):</mark> 2 <mark>SearchAgents_no = Positions.shape[0]</mark> 3 <mark>dim = Positions.shape[1]</mark> 

4 

5 <mark>lb_array = np.zeros((SearchAgents_no, dim))</mark> 6 <mark>ub_array = np.ones((SearchAgents_no, dim))</mark> 7 8 <mark>rand_adjust = lb_array + (ub_array - lb_array) * np.random.rand(*Positions.shape)</mark> 9 <mark>Positions = np.where((Positions < lb_array) | (Positions > ub_array), rand_adjust, Positions)</mark> 

<mark>#EVOLVE-START beta = 1.5</mark> 

<mark>sigma = (np.math.gamma(1+beta)*np.sin(np.pi*beta/2)/(np.math.gamma((1+beta)/2)*beta *</mark><sup><mark>(2</mark></sup> <mark>**</mark><sup><mark>((beta-1)/2))))</mark></sup> <mark>**</mark><sup><mark>(1/beta)</mark></sup> 

14 <mark>levy_step = 0.01 * np.random.randn(SearchAgents_no,1) * sigma / (np.abs(np.random.randn( SearchAgents_no,1))**beta)</mark> 15 16 <mark>learn_prob = 0.5 + 0.4*(Best_score - np.min(np.linalg.norm(Positions-Best_pos,axis=1)))/ Best_score</mark> 17 <mark>mask = np.random.rand(SearchAgents_no,dim) < learn_prob.reshape(-1,1)</mark> 18 <mark>Positions = np.where(mask,</mark> 19 <mark>Best_pos + levy_step*(Positions - Best_pos.mean(axis=0)),</mark> 20 <mark>Positions*(1 + 0.5*(np.random.rand(*Positions.shape)-0.5)))</mark> 21 <mark>#EVOLVE-END</mark> 22 <mark>return Positions</mark> 

<mark>Best_pos + levy_step*(Positions - Best_pos.mean(axis=0)), Positions*(1 + 0.5*(np.random.rand(*Positions.shape)-0.5))) #EVOLVE-END return Positions</mark> 

Listing 3: ACS 

1 <mark>def heuristics_v2(Positions, Best_pos, Best_score, rg):</mark> 2 <mark>SearchAgents_no = Positions.shape[0]</mark> 3 <mark>dim = Positions.shape[1]</mark> 4 5 <mark>lb_array = np.zeros((SearchAgents_no, dim))</mark> 6 <mark>ub_array = np.ones((SearchAgents_no, dim))</mark> 7 8 <mark>rand_adjust = lb_array + (ub_array - lb_array) * np.random.rand(*Positions.shape)</mark> 9 <mark>Positions = np.where((Positions < lb_array) | (Positions > ub_array), rand_adjust, Positions)</mark> 10 11 <mark>#EVOLVE-START</mark> 12 <mark># Levy flight component</mark> 13 <mark>beta = 1.5</mark> 14 <mark>sigma = (np.math.gamma(1+beta)*np.sin(np.pi*beta/2)/(np.math.gamma((1+beta)/2)*beta*2**(( beta-1)/2)))**(1/beta)</mark> 15 <mark>u = np.random.randn(*Positions.shape) * sigma</mark> 16 <mark>v = np.random.randn(*Positions.shape)</mark> 17 <mark>step = u/abs(v)**(1/beta)</mark> 18 19 <mark># Adaptive weights</mark> 20 <mark>w = 0.9 - 0.5*(Best_score/1000) # Scale based on fitness</mark> 21 22 <mark># Hybrid update</mark> 23 <mark>r = np.random.rand(SearchAgents_no, 1)</mark> 24 <mark>mask = r < 0.5</mark> 25 <mark>Positions = np.where(mask,</mark> 26 <mark>Best_pos + w*step*Positions,</mark> 27 <mark>w*Positions + (Best_pos - Positions)*np.random.rand(*Positions.shape) )</mark> 28 <mark>#EVOLVE-END</mark> 29 <mark>return Positions</mark> 

Listing 4: WSN 

