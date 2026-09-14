1 

# Large Language Models in Operations Research: Methods, Applications, and Challenges 

Yang Wang<sup>1</sup> , Kai Li<sup>2</sup><sup>_,_3</sup> 

> 1University of Chinese Academy of Sciences, Beijing, China 

> 2Institute of Automation, Chinese Academy of Sciences, Beijing, China 

> 3School of Artificial Intelligence, University of Chinese Academy of Sciences, Beijing, China 

**_Abstract_ —Operations research (OR) is a core methodology that supports complex system decisionmaking, with broad applications in transportation, supply chain management, and production scheduling. However, traditional approaches that rely on expertdriven modeling and manual parameter tuning often struggle with large-scale, dynamic, and multiconstraint problems, limiting scalability and real-time applicability. Large language models (LLMs), with capabilities in semantic understanding, structured generation, and reasoning control, offers new opportunities to overcome these challenges. It can translate natural language problem descriptions into mathematical models or executable code, generate heuristics, evolve algorithms, and directly solve optimization tasks. This shifts the paradigm from human-driven processes to intelligent human–AI collaboration. This paper systematically reviews progress in applying LLMs to OR, categorizing existing methods into three pathways: automatic modeling, auxiliary optimization, and direct solving. It also examines evaluation benchmarks and domain-specific applications, and highlights key challenges, including unstable semantic-to-structure mapping, fragmented research, limited generalization and interpretability, insufficient evaluation systems, and barriers to industrial deployment. Finally, it outlines potential research directions. Overall, LLMs demonstrate strong potential to reshape the OR paradigm by enhancing interpretability, adaptability, and scalability, paving the way for next-generation intelligent optimization systems.** 

**_Index Terms_ —Automatic Modeling, Auxiliary Optimization, Intelligent Optimization Systems, Large Language Models, Operations Research** 

## I. Introduction 

**A** Splexa coresystems,methodologyOR has forbeendecision-makingwidely appliedinincom-domains such as transportation, supply chain management, and production scheduling. However, with the rapid growth of data, increasing environmental dynamism, and rising demand customization, the traditional optimization paradigm—reliant on expert-based modeling and manual parameter tuning—has increasingly shown its limitations. The exponential expansion of problem scale, the growing complexity of constraint structures, and stringent realtime requirements pose formidable challenges to existing 

Emails: yangw77718@gmail.com, kai.li@ia.ac.cn 

methods, significantly hindering their applicability and adoption in complex scenarios [1], [2], [3]. 

Against this backdrop, the emergence of LLM offers a new opportunity to transform the paradigms of OR. Leveraging capabilities in semantic understanding, structured generation, and reasoning control, LLM has the potential to reshape the optimization process. Its value is primarily reflected in two aspects: First, at the modeling level, LLM can automatically translate natural language problem descriptions into formal mathematical models or executable code, thereby achieving a direct mapping from requirements to models [4], [5]. Second, at the solving level, LLM can serve as a generator of heuristic strategies and collaborate with traditional optimization algorithms to build a closed-loop perception–reasoning–feedback framework, thereby improving both efficiency and solution quality [6], [7], [8]. 

Although recent studies have made progress, most explorations remain confined to local breakthroughs on specific tasks, and a unified methodological framework has yet to emerge. When addressing complex logical reasoning, LLM still exhibits instability and uncertainty in results. The limited interpretability of its reasoning process further challenges the reliability of practical applications. Hence, a systematic review is needed to clarify the research landscape, unify methodological paradigms, and outline future development directions. As shown in Fig. 1, the literature classification map visually illustrates the distribution of research pathways and representative works. Specifically, this paper systematically introduces research on LLMdriven OR from three perspectives: 

- **Methodological Paradigm Summary:** reviewing existing work by classifying it into modeling and solving paradigms, and summarizing core technologies and implementation paths. 

- **Domain Application Analysis:** presenting case studies of LLM in typical scenarios such as supply chain optimization and urban management. 

- **Frontier Trends Outlook:** identifying key bottlenecks in current research and outlining potential breakthroughs and future directions. 

Existing surveys on LLMs for optimization provide valuable but fragmented perspectives. Da Ros et al. [1] 

2 



Fig. 1. Literature classification map of LLM-driven OR research pathways and representative works. 

emphasize methodological advances within combinatorial optimization, whereas cross-paradigm and applicationoriented perspectives remain underexplored. Liu et al. [2] highlight algorithm design, viewing LLMs mainly as generators rather than covering the full workflow. Xiao et al. [9] review the modeling stack—data, inference, and evaluation—yet give little attention to auxiliary optimization and solving. Zhang et al. [10] connect modeling and solving within evolutionary optimization but do not extend beyond this paradigm. In contrast, our review unifies automatic modeling, auxiliary optimization, and direct solving into a coherent framework, while also extending the analysis to domain problems and sector-specific applications, thereby offering a more comprehensive perspective on LLM-driven OR. The goal is to provide a systematic methodological review and structured insights, thereby promoting the deep integration of LLM with OR and supporting the development of next-generation intelligent decision-making systems. 

## II. Introduction to Basic Principles 

into mathematical representations of objectives and constraints, providing the theoretical foundation and tools for systematic analysis and exact solving. The scope of OR covers diverse problem types, including linear programming, integer programming, and combinatorial optimization [13], [14]. These models effectively capture structural characteristics and sources of uncertainty, thereby establishing the methodological basis for modeling and solving complex systems. With its rigorous mathematical framework and broad applicability, OR has been widely adopted in critical domains such as transportation, supply chain management, and production scheduling [15], [16]. However, as problem sizes expand and constraint structures become increasingly complex, traditional methods reveal clear limitations, including over-reliance on expert experience, insufficient modeling flexibility, and prohibitive computational costs for NP-hard problems. These challenges open the door for the introduction of LLM, which shows breakthrough potential in natural language–driven modeling, heuristic strategy generation, and the solving of complex problems. 

## _A. Operations Research (OR)_ 

OR is a systematic decision science centered on mathematical methods, aiming to obtain optimal or nearoptimal solutions to objective functions under multiple constraints [11], [12]. By means of formal modeling, complex real-world decision problems are abstracted 

## _B. Foundation of Competence of LLM_ 

Pre-trained on large-scale corpora, LLM acquires semantic understanding, knowledge association, and generative reasoning [17], [18]. Its relevance to OR lies in mapping natural language inputs into structured elements, 

3 

algorithmic steps, or approximate solutions. Two core applications emerge: modeling, where LLM transforms unstructured descriptions into variables, objectives, and constraints to generate mathematical models or executable code [4], [5], [19]; and solving, where reasoning decomposition and chain-of-thought (CoT) support local search, heuristic generation, and tool invocation [20], [21]. Moreover, LLM enables task generalization and interactive correction by suggesting parameters, producing heuristic operators, or reorganizing solving logic within optimization frameworks [6], [7], [22]. When modeling fails or solving degrades, it establishes a generate–validate–repair closed loop through multi-turn prompts, rewriting, or tool calls [23], enhancing stability and controllability with selfdebugging [21] and self-feedback [24]. These capabilities underpin the application of LLM in OR, particularly along two key pathways—automatic modeling and assisted solving—reviewed in the next section. 

## III. LLM-based Methods for Operations Research 

## _A. Automatic Modeling_ 

In recent years, automatic modeling has emerged as a core research direction for LLMs in OR. Ramamonjison et al. [4] first proposed a systematic modeling framework for translating natural language into optimization models, laying the research foundation for this field. Subsequently, Fan et al. [5] reviewed the multi-stage pathway for integrating artificial intelligence and OR, explicitly highlighting the unique potential of LLMs in the modeling phase. Huang et al. [19] further introduced the MAMO benchmark and proposed a “model generation + numerical validation” evaluation method, which for the first time established modeling capability as an independent research objective. As a result, automatic modeling has been increasingly recognized as a critical bridge between natural language and formal models [22]. 

To clarify the process, this paper summarizes automatic modeling into five sequential steps forming a closed loop from natural language to model execution, as illustrated in Fig. 2. The process begins with problem comprehension, where optimization objectives and resource constraints are parsed, followed by element identification to extract decision variables, constraint types, and objective functions. These elements are then organized through structure generation into a standard mathematical model, which is further transformed into solver-executable code. Finally, verification and feedback are performed by running the code in a solver and iteratively correcting errors based on the results. 

This section systematically reviews three representative research paradigms: (1) the pathway via prompting, (2) the collaborative pathway combining prompt and model fine-tuning, and (3) the external knowledge-guided mechanism. It also summarizes related evaluation benchmarks to compare their performance and applicability. 



Fig. 2. Closed-loop framework of automatic modeling from natural language input to model execution. 

TABLE I 

Representative Studies on Prompt-based LLM Automatic Modeling 

|**Framework**|**Key Modeling Traits**|**Benchmarks**|
|---|---|---|
|OptiMUS [25], [26],<br>[27]<br>Chain-of-Experts [28]|Multi-stage + Visualization<br>+ Reflection–retry prompts<br>Multi-agent chain + Expert<br>prompts + Backward<br>reflection|NL4OPT +<br>ComplexOR<br>LPWP +<br>ComplexOR|
|OptLLM [29]|Three-stage dialogue +<br>Interactive feedback|NL4OPT +<br>Optimize<br>tasks|
|NL2OR [30]|DSL generation + Structural<br>validation|30 OR inst.<br>NL4OPT +|
|Autoformulator [31]|Multi-stage + Composite<br>prompts + Structural search|IndustryOR<br>+ MAMO +<br>ComplexOR|
||Multi-agent + Hierarchical||
|MA-GTS [32]|modules + Semantic<br>decomposition|G-REAL|
||Prompt modeling + Code||
|OR-LLM-Agent [33]|validation + Self-repair<br>chain + Validation chain|83 real OR|



_1) LLM-based Automatic Modeling Paradigm via prompting:_ The prompt-driven approach has become a significant direction for automated optimization modeling due to its lightweight design and ease of implementation. This class of methods guides the LLM to generate core components such as variables, objective functions, and constraints through prompting. Representative studies are summarized in Table I. 

In this pathway, the OptiMUS series of work by AhmadiTeshnizi et al. has built the most representative prompt-driven modeling process. The initial version [25] progressively converted natural language into a solvable optimization model, covering structure generation, code generation, execution validation, and feedback correction, and developed the accompanying NLP4LP dataset to support evaluation. Subsequent research [26] introduced a connection graph mechanism to record dependencies between variables, constraints, and parameters, thereby extracting context to prompt input and adapt to complex modeling scenarios. The latest version [27] further 

4 

integrates a structure detection agent and a structure pool, combined with error correction mechanisms such as prompt retries and self-correction. It also supports calling solver subroutines in advanced optimization systems and provides an interactive modeling and visualization platform, thereby greatly improving the structural perception and engineering potential of the system. 

Within prompting-based modeling, verification has become a central theme, though different works emphasize it from distinct angles. Xiao et al. [28] strengthen controllability through the Chain-of-Experts framework, where role-specific agents handle terminology parsing, model construction, code generation, and verification, supported by a two-stage reasoning mechanism of forward construction and backward reflection. Zhang et al. [29] highlight interactive refinement, employing a three-stage workflow of parsing, structural transformation, and result generation that integrates user feedback to lower the entry barrier for non-experts. Building on structured prompts, Li et al. [30] enhance structural correctness by introducing grammar correction, variable-consistency checks, and JSON Schema validation, with automatic restarts when errors occur. Astorga et al. [31] pursue systematic exploration, combining hierarchical decomposition and Monte Carlo Tree Search (MCTS) with structured templates and a candidate generation–pruning–ranking procedure to ensure both consistency and diversity. 

Prompting has also been applied in specific scenarios. Yuan et al. [32] proposed the MA-GTS framework for graph-structured tasks, where multi-agent collaboration supports hierarchical modeling through semantic parsing, knowledge integration, and algorithmic solving, progressively reconstructing graph structures from text and invoking optimization algorithms adaptively. Zhang et al. [33] introduced the OR-LLM-Agent framework, which emphasizes reasoning-driven closed-loop modeling by using structured prompts to transform natural language into linear programming models, automatically generating executable code and performing repair and validation within a sandbox environment. 

In summary, prompting has developed across multiple dimensions, encompassing both single-prompt guidance and multi-agent collaboration, incorporating interactive parsing and structured verification mechanisms, and spanning a wide range of scenarios from general tasks to domain-specific applications. These studies not only validate the effectiveness of prompting in automatic modeling but also highlight its potential in structural perception, task decomposition, and interactive generation. 

_2) LLM-based Automatic Modeling Mechanism Driven by Prompt–Fine-tuning Synergy:_ In research on automatic modeling using LLM, the synergistic mechanism of prompting and model fine-tuning has gradually emerged as a core developmental path. By combining input optimization with parameter updating, this mechanism alleviates the instability and limited generalization of single-prompt guidance in complex tasks, while further improving the model’s accuracy and robustness in variable recognition, 

TABLE II 

Representative Studies on Prompt–Fine-tuning Synergy in Automatic Modeling 

|**Study**|**Prompt Mechanism**|**FT**|
|---|---|---|
|Amarasinghe [35]|Fixed structured prompts|SFT|
|Li [36]|Template-based prompts|SFT|
|Ma [37]|Structured prompts + Rewrite|CL +<br>InstrSFT|
|Wu [38]|Structured prompts + Validation<br>chain|LoRA +<br>Alpaca +<br>COPT|
|Jiang [39]|Structured prompts + Multi-rule<br>aug.|MI-SFT +<br>KTO|
|Lu [40]|Structured prompts +<br>Self-correction|LoRA|
|Li [41]|Structure-enhanced NL prompts|SFT + DPO|



constraint parsing, and structured representation [34]. A summary of representative studies is provided in Table II. 

In workflow and module design, researchers have explored decomposing complex tasks through structured prompts and staged fine-tuning. Amarasinghe et al. [35] proposed the AI Copilot framework, which uses supervised fine-tuning to transform natural language into modeling code and applies prompt engineering with nine submodules to overcome token limitations, ensuring completeness and executability. Li et al. [36] introduced a three-stage framework involving variable identification, constraint classification, and supplementary generation, which significantly improves the precision of variable extraction and constraint construction. Ma et al. [37] developed the LLaMoCo framework, incorporating code-tocode instruction tuning and a large-scale instruction set for diverse optimization tasks, while enhancing semantic alignment and constraint comprehension through unified structural prompts and diversified rewriting strategies. By integrating contrastive learning with instruction tuning in a two-stage process, LLaMoCo achieves stronger semantic understanding and generalization in code generation. 

In the area of data generation and consistency verification, Wu et al. [38] proposed the Evo-Step-Instruct framework, which introduces dual strategies of complexity evolution and scope evolution to guide the model in generating diverse, high-quality data. A step-by-step verification mechanism is further employed to ensure consistency among descriptions, variables, and constraints, thereby effectively preventing error propagation. This method demonstrates strong stability and accuracy on complex benchmark tasks, underscoring the critical role of data quality in the effectiveness of synergistic mechanisms. 

Meanwhile, modeling standardization and robustness enhancement have emerged as another important direction. Jiang et al. [39] proposed the LLMOPT framework, which defines a unified five-element modeling structure consisting of sets, parameters, variables, objectives, and constraints. By combining diverse samples generated through prompt templates with expert-annotated data, the framework employs supervised fine-tuning, model alignment, and self-correction mechanisms to significantly 

5 

improve modeling reliability and solution stability in complex tasks. In contrast, Lu et al. [40] introduced the OptMATH framework, which emphasizes the construction of high-quality triplet datasets encompassing natural language, mathematical expressions, and solver code, while adjusting task difficulty through a feedback mechanism. 

In the domain of structure-guided optimization algorithm generation, Li et al. [41] proposed the STRCMP framework, which integrates language modeling with graph structure learning. By extracting structural features through a constraint–variable bipartite graph, the framework generates solver-oriented algorithmic code conditioned jointly on natural language and structural embeddings. Leveraging supervised fine-tuning, preference optimization, and the generative–evolutionary capabilities of LLM, it iteratively optimizes performance across multiple rounds. Methodologically, it shares similarities with MA-GTS [32] in structural extraction and multi-module collaboration, while following the structure-guided code generation paradigm introduced by AEL [42]. 

In summary, the synergy between prompting and finetuning demonstrates multi-dimensional advantages across workflow design, data generation, modeling standardization, and structure-guided algorithm generation. At the methodological level, it advances the systematic mapping from natural language to structured models, while at the practical level, it provides a solid foundation for scalability and industrial deployment. This synergistic mechanism lays the groundwork for extending automatic modeling to more complex tasks and cross-domain applications in the future. 

_3) LLM-based Automatic Modeling Mechanism Guided by External Knowledge:_ In complex modeling tasks, external knowledge guidance provides LLM with new avenues for enhancement. Jiang et al. [43] proposed the DRoC framework, which decomposes vehicle routing problems into constraint subtasks and injects precise external knowledge through semantic retrieval and document filtering.Moreover, the Bootstrap mechanism in DRoC further validates the feasibility of dynamically expanding external knowledge bases. Extending this direction, Peng et al. [44] focused on privacy-preserving and local deployment scenarios, proposing a domain knowledge–enhanced automatic modeling framework for constructing MILPs in multi-robot task allocation and scheduling problems. By guiding variable and constraint generation through knowledge bases, and combining prompt-based guidance with supervised fine-tuning, their method enables automatic generation of solver code, demonstrating strong stability and generative capability in representative scheduling tasks. 

External knowledge guidance substantially enhances LLM’s modeling capacity for complex constraints and scheduling, improving accuracy and robustness while enabling dynamic expansion and scenario adaptation, thus supporting the development of more generalizable automatic modeling frameworks. 

_4) Benchmarks for Evaluating LLM-based Automatic Modeling:_ As the evaluation system for automatic modeling continues to mature, researchers have proposed more targeted benchmarks and frameworks from various perspectives, including industry coverage, dataset scale, structural equivalence, cross-task unification, and constraint programming adaptation. These efforts not only address the limitations of existing evaluation tools in terms of applicability and breadth but also drive the systematic assessment of automatic modeling capabilities across multiple dimensions. 

In terms of industry adaptation and large-scale sample requirements, Huang et al. [45] proposed the ORINSTRUCT framework and constructed the IndustryOR benchmark, which encompasses 1,556 natural language modeling problems across 16 industries, yielding a training set of 32,481 samples. The ORLM series models outperformed GPT-4 on the NL4OPT, MAMO, and IndustryOR tasks, demonstrating near-expert, human-level modeling capabilities under the Pass@8 setting. To address the limitations of small models in language understanding, Yang et al. [46] introduced the OptiBench and ReSocratic frameworks, constructing the ReSocratic-29K dataset. Through a reverse-generation strategy, they back-translated natural language problems and programs from structured modeling examples, significantly boosting the performance of the LLaMA series on MILP tasks. Recognizing the limited scope and insufficient domain coverage of existing benchmarks, Wang et al. [47] further extended OptiBench by proposing an evaluation tool comprising 816 problems across more than 80 domains, thereby strengthening crosstask and cross-domain coverage. 

In structural equivalence, Zhai et al. [48] introduced EquivaFormulation on the NLP4LP dataset and developed the EquivaMap framework, which uses LLM to generate variable mappings and automatically assess semantic equivalence of modeling results. This addresses the limitations of traditional accuracy metrics and WL tests in complex scenarios. For cross-task evaluation, Singirikonda et al. [49] created the TEXT2ZINC dataset, standardizing on MiniZinc and covering 110 problems across 11 domains, including both optimization and satisfiability tasks. Results show that CoT reasoning and compositional modeling outperform basic prompting in generation accuracy, offering a robust benchmark for cross-paradigm evaluation. 

In the direction of constraint programming, Michailidis et al. [50] proposed CP-Bench, which covers 101 combinatorial optimization problems and 241 types of constraints. The study systematically compared three modeling frameworks—MiniZinc, CPMpy, and OR-Tools—and introduced enhancement strategies including prompt design, in-context examples, repeated sampling, and selfverification. The results show that Python-based frameworks are more suitable for LLM-driven modeling, and that repeated sampling combined with self-verification can significantly improve solution accuracy. 

In summary, these benchmarks and frameworks have ex- 

6 



Fig. 3. Two primary approaches to LLM-assisted optimization. 

panded the evaluation dimensions of automatic modeling in terms of industry adaptation, dataset scale, structural validation, and cross-task assessment, thereby significantly advancing the systematic development of evaluation systems. Nevertheless, their limitations remain evident: task coverage is still largely confined to typical problems such as MILP and VRP, making it insufficient to capture complex constraints and heterogeneous modeling scenarios; evaluation metrics are overly centered on structural equivalence and accuracy, lacking systematic measures of efficiency, interpretability, and robustness; and some datasets rely on manual or synthetic generation, resulting in a substantial gap from real-world industrial requirements. Future research must therefore focus on developing more representative and practical benchmarks to support the evaluation of LLM’s modeling capabilities in diverse and realistic settings. 

## _B. LLM-assisted Optimization_ 

In recent years, LLM-assisted optimization has gradually become an important research direction in the field of OR. Its core objective is to enhance the practicality and controllability of models in solving optimization problems through structural design and capability coordination [22]. Figure 3 illustrates the two primary approaches to LLMassisted optimization. 

This section systematically reviews two representative research directions: (1) LLM-enabled hybrid mechanisms for integrating multiple optimization algorithms, and (2) LLM-dominated optimization solving. It also summarizes and analyzes the related evaluation benchmarks to comprehensively present the performance and limitations of such methods in optimization tasks. 

_1) LLM-enabled Hybrid Mechanisms for Integrating Multiple Optimization Algorithms:_ In recent years, LLM has demonstrated unique advantages in reasoning control and strategy generation, opening new avenues for their integration with diverse optimization algorithms. Existing studies show that LLM can contribute not only to operator design and search guidance but also to strategy adjustment and structural optimization. Huang et al. [51], through an analysis of structural mapping between LLM and evolutionary algorithms, revealed their synergistic potential in operator generation and search control; Cai et 

TABLE III 

Representative Studies on LLM-driven Heuristic Structure Evolution and Strategy Optimization 

|**Study**|**Core Mechanism**|
|---|---|
|Liu [60]|Zero-shot operator + Temperature<br>adaptation + Natural language|
|Liu [42], [61], [62]|Structured prompt modeling + Multi-round<br>evolutionary optimization|
|Liu & Li [63]|Constraint-aware heuristic construction for<br>VRP|
|Romera-<br>Paredes [64]|LLM program generation with evaluator,<br>maintain search diversity|
|Chen [65]|QUTC design, UIQ-based parent selection|
|Ye [66]|Short- and long-term reflection for evolution|
|Sun [67]|Module replacement + Candidate evaluation|
|Zhong [68]|Multi-module prompt-based heuristic<br>generation|
|Yang [69], [70]|Multi-agent strategy evolution and selection|
|Huang [71]|Reflection + Scheduling rule evolution|
|Dat [72]|Role prompts + Flash reflection + Harmony|
|Huang [73]|Reasoning path generation + Modular<br>strategies|
|Ling [74]<br>Ali [75]|“Explore” + “Modify” strategy<br>Human preference-based selection|
|Bömer [76]|Semantic structure + Context-driven<br>generation|
|Wu [77]|Key component extraction + Performance<br>prediction|
|Thach [78]|Language reduction + Parallel evolution|
|Shi [79]|Dual-loop mechanism|
|Duan [80]|Instance generator + Solver co-evolution|



al. [7] further proposed leveraging LLM as a component for structural guidance and strategy adjustment, effectively enhancing the automation and adaptability of the optimization process. Against this backdrop, this paper further reviews three representative fusion pathways: (1) heuristic structure evolution and strategy optimization; (2) collaborative mechanisms in multi-objective evolution; and (3) capability transfer in cross-paradigm integration. 

LLM has demonstrated broad potential in its integration with evolutionary algorithms. Existing studies have examined diverse embedding methods and collaborative pathways, encompassing heuristic structure generation, strategy regulation, and the optimization of evolutionary mechanisms [52], [53], while emphasizing LLM’s critical role in search guidance and strategy automation [54], [55]. This direction has further extended to the joint evolution of objective functions and control modules [56], [57], revealing the behavioral patterns and performance evolution of LLM in heuristic strategy development [58], [59]. Overall, this approach has established a systematic framework, with the core mechanisms of related studies summarized in Table III. 

On direct embedding strategies, Liu et al. [60] proposed the LMEA framework, which employs LLMs as zero-shot operators for parent selection, crossover, and mutation. This approach significantly reduces the complexity of operator design and domain adaptation. Candidate solutions are generated through natural language prompts, while a temperature-adaptive mechanism balances exploration and exploitation, yielding superior performance over tra- 

7 

ditional methods on multiple TSP instances. 

Building on this idea, Liu et al. [42] introduced the AEL framework, which regards the optimization algorithm itself as the target. By using structured prompts, LLMs generate, rewrite, and refine algorithms, enabling iterative self-improvement across evolutionary rounds. Further extensions [61] applied AEL to guided local search, where LLMs automatically produce key guiding functions that outperform manually designed schemes, demonstrating strong generalization on complex TSP tasks. 

Continuing along this trajectory, the authors developed the LLM4AD platform [62]. It leverages structured prompts and search mechanisms to generate standardized, executable algorithmic code, supported by a unified evaluation pipeline that forms a complete closed loop. In domain-specific applications, Li et al. [63] proposed the ARS framework, which uses prompt engineering to construct constraint-aware heuristics for vehicle routing problems. The framework is supported by the RoutBench benchmark, which covers 1,000 VRP variants and six realworld constraints, and achieves end-to-end optimization by performing constraint selection, detection, and scoring function generation without fine-tuning. 

On algorithm generation and evolutionary mechanisms, Romera-Paredes et al. [64] proposed the FunSearch framework, which employs LLM as a core generator to iteratively produce, evaluate, and retain high-quality solutions within the function space, while maintaining search diversity through a distributed architecture. Building on this, Chen et al. [65] introduced the QUBE framework, which incorporates a unified uncertainty-based indicator to guide parent selection and population resetting, thereby achieving a dynamic balance between structural exploration and local exploitation. Ye et al. [66] proposed the ReEvo framework, embedding a dual-layer language reflection mechanism into the heuristic evolutionary loop. After generating heuristic code, the model can suggest improvements and guide subsequent searches, enabling strategies to progressively converge toward superior solution spaces. 

On solver module optimization, Sun et al. [67] proposed the AutoSAT framework, which decomposes CDCL solvers into modular components and leverages LLM to generate candidate functions to replace specific modules. High-quality alternatives are retained through performance evaluation, thereby progressively enhancing solver performance. On structured prompting strategies, Zhong et al. [68] introduced the CRISPE prompting strategy, composed of five submodules, to guide LLM in generating heuristic pseudocode. Based on this, they developed the metaheuristic algorithm ZSO, which demonstrated strong performance and convergence stability across CEC2014, CEC2022, and several engineering optimization problems. 

Within multi-agent collaboration, Yang et al. [69] proposed the HeurAgenix framework, which constructs a heuristic optimization system composed of four agents—generation, evolution, evaluation, and selection—thereby extending the role of LLM from a single generator to a multi-role collaborator. Further research [70] 

introduced a two-stage hyper-heuristic framework that integrates solution trajectories with preference mechanisms to iteratively refine heuristic strategies, even surpassing traditional specialized optimizers. 

For dynamic scheduling and diversity maintenance, Huang et al. [71] proposed the SeEvo framework, which treats LLM-generated scheduling rules as individuals in the population and employs both individual and collective reflection mechanisms for continuous optimization, outperforming traditional methods in dynamic scheduling tasks. Dat et al. [72] introduced the HSEvo framework, which leverages role-playing prompts to generate diverse heuristic individuals and integrates Harmony Search for local refinement, effectively enhancing adaptability while maintaining diversity. 

In graph optimization and complex planning scenarios, Huang et al. [73] proposed the GraphThought framework, which leverages reasoning-path generation and template synthesis mechanisms to advance structural recognition and LLM-based strategy integration in graph optimization tasks. Ling et al. [74] introduced the AutoHD framework, which employs LLM to generate diverse heuristic functions and continuously evolve them, thereby improving solution quality and reasoning efficiency in complex planning tasks. 

In the field of preference modeling and task adaptability, Ali et al. [75] proposed the PAIR framework, which incorporates human-like preference mechanisms and leverages structured prompts to perform high-quality individual pairing and crossover and mutation, thereby equipping LLM with selection and regulation capabilities in heuristic evolution. Bömer et al. [76] introduced the CEoH framework, which integrates task context with structured prompts to generate heuristic algorithms that are more targeted and adaptive. Wu et al. [77] proposed the Hercules framework, which introduces performance prediction and confidence control mechanisms to achieve a coordinated trade-off between quality and efficiency during heuristic generation and evaluation. 

In problem reformulation and meta-optimization exploration, Thach et al. [78] proposed the RedAHD framework, which employs language-based simplification to automatically generate surrogate problems and conducts multisource evolution across multiple spaces, thereby extending the boundaries of heuristic discovery. Shi et al. [79] introduced the MoH framework, which adopts a bi-level optimization process: in the outer loop, LLM generates candidate optimizers, while in the inner loop, the optimizers generate heuristics. This approach overcomes the limitations of fixed optimizer structures and demonstrates strong generalization ability in multi-task environments. Duan et al. [80] proposed the EALG framework, which establishes an adversarial co-evolutionary system in which LLM generates problem instances and heuristic solvers separately. Driven by adversarial objectives, both evolve jointly, enhancing problem difficulty and strategy adaptability. 

In summary, LLM in heuristic structure evolution and strategy optimization has progressed from a single gen- 

8 

TABLE IV 

LLM Collaboration in Multi-objective Evolution 

|**Study**|**Key Idea**|
|---|---|
|**Phase I: Of**|**ffspring Generation and Search Collaboration**|
|Liu [81]<br>Wang [82]<br>Liu [83]|Prompted offspring + Linear operator to reduce<br>cost while preserving generalization<br>Embed LLM as search operator in CCMO +<br>Co-evolve with classic genetic operators<br>Low-cost adaptive MOEA with auxiliary evaluation<br>+ Stagnation detection + NSGA-II|
|**Phase I**|**I: Evolutionary Mechanism Construction**|
|Huang [84]<br>Yao [85]|LLM-generated executable mutation operators +<br>Performance feedback<br>Evolve non-dominated heuristic sets with<br>dominance + Code diversity + Guided parents +<br>Population update|
|Forniés-|NSGA-II guided parents + Clustering-based|
|Tabuenca[86]|reflection for heuristic evolution|
|**P**|**hase III: Unified System Framework**|
|Qian [87]|Unified framework + Homogeneous crossover +<br>Heterogeneous co-evolution + Upgrades<br>**Task-specific Applications**|
|Li [88]|Portfolio MO with NSGA-II + Non-dominated<br>sorting + Crowding distance validation|



erator to a full-process collaborator, advancing heuristic design from experience-driven patterns toward adaptive evolution. Building upon this foundation, research has further extended into multi-objective evolutionary optimization, where the collaborative role of LLM evolves from offspring generation to the construction of systematic frameworks, as outlined in Table IV. 

Early studies primarily explored the auxiliary role of LLM in offspring generation and search operators. Liu et al. [81] were the first to introduce LLM into multiobjective evolutionary optimization, where the MOEA/DLLM framework employed prompt engineering to generate offspring individuals and designed linear operators to reduce invocation costs while maintaining strong generalization performance. Wang et al. [82] embedded LLM as a novel search operator within the CCMO framework, guiding the generation of partial offspring solutions and co-evolving with traditional genetic operators, thereby accelerating convergence and improving solution quality. Subsequently, Liu et al. [83] proposed a low-cost adaptive mechanism that invokes LLM to generate candidate solutions only when evolutionary stagnation occurs, and integrates them with NSGA-II operators, thereby improving solution quality under limited computational resources. 

With the growing generative capabilities of LLM, its role has gradually expanded to the construction of evolutionary operators and heuristic structures. Huang et al. [84] proposed an automatic operator generation framework that guides LLM to produce executable mutation operators from structured task descriptions and iteratively refines them based on performance feedback, thereby enhancing algorithm adaptability and structural flexibility. Yao et al. [85] introduced the MEoH framework, which employs a combined strategy of dominance and structural diversity to guide parent selection and population updating, automatically evolving a structurally diverse set of non- 

dominated heuristics. Forniés-Tabuenca et al. [86] developed the REMoH framework, which represents individuals using LLM-generated heuristic functions and incorporates NSGA-II’s non-dominated sorting and crowding-distance mechanisms, while embedding a clustering-based reflection process to improve solution diversity and robustness. 

Building on mechanism exploration, research has further advanced toward systematic integration. Qian et al. [87] proposed the MLHH framework, which unifies the evolution of heuristic structures through three steps: homogeneous crossover evolution, heterogeneous co-evolution, and architecture function upgrading. The framework executes a “generate–standardize–evaluate–select” loop iteratively, enabling the continuous optimization of highquality multi-objective solution strategies. This stage of work highlights the shift in LLM’s role in multi-objective evolution from supporting localized operations to orchestrating holistic system-level coordination. 

For real-world tasks, Li et al. [88] embedded LLM into the NSGA-II framework and proposed the llmPCNSGA-II method for multi-objective portfolio optimization. This approach generates complete offspring populations through structured prompts and updates them using non-dominated sorting and crowding distance mechanisms. Experimental results on real financial data and standard benchmark functions demonstrate strong convergence and diversity, validating the application potential of LLM in practical OR problems. 

Overall, the collaborative mechanisms of LLM in multiobjective optimization follow a clear trajectory from initial offspring generation to unified frameworks and real-world applications, positioning LLM as a transformative force in this domain. Moving beyond the scope of multi-objective problems, recent studies have begun to emphasize crossparadigm integration, where LLM’s language understanding, structural generation, and reasoning abilities are combined with classical operators, reinforcement learning, and neuro-symbolic systems to enhance transferability and global optimization capacity. To systematically present the progress of cross-paradigm integration, Table V summarizes representative studies and their primary technical pathways. 

Some studies have focused on coupling LLM with classical optimization operators, embedding it into traditional algorithms such as large neighborhood search (LNS) and simulated annealing to enhance search efficiency and structural adaptability. Sartori et al. proposed an LLM-based heuristic redesign approach in two studies: on the one hand, structured prompts were used to extract node features and generate probabilistic signals, which were embedded into a BRKGA decoder to achieve structure-aware metaheuristic search [89]; on the other hand, the contextual understanding capabilities of LLM were incorporated into CMSA to reconstruct heuristic functions, generating variants with age bias and entropy regularization, thereby improving structural diversity and solution quality [90]. Similarly, Ye et al. [91] designed a bi-level evolutionary LNS, where the inner layer leverages LLM to generate 

9 

TABLE V 

Representative Studies on LLM Capability Transfer and Synergy in Cross-paradigm Fusion 

|**Study**|**Key Idea**|
|---|---|
||**Fusion with Classical Optimization**|
|Sartori [89]|Prompted node features + Probabilistic BRKGA<br>decoder + Structure-aware metaheuristics|
|Sartori [90]<br>Ye [91]|Heuristic context + Policy redesign + Preference<br>correction-penalty<br>Bi-level evolution + NL/Code heuristics +<br>Memory-guided evolution|
|Wang [92]|SA with heuristic reconstruction and temperature<br>adaptation|
||**Fusion with Reinforcement Learning**|
|Ma [93]|Heuristic pool + RL policy selection +<br>Feedback-driven improvement|
|Surina [94]|Program sampling + DPO-LLM optimization +<br>Preference construction|
|Huang [95]|Prompted structure + GRPO-RL optimization +<br>Collapse-restart evolution|
||**Fusion with neuro-symbolic systems**|
|Jiang [96]|Semantic encoding + RL-trained generator + Instance<br>understanding|
|Tran [97]|LLM attention bias + POMO/LEHD integration +<br>Lightweight fine-tuning|
|**S**|**earch Trajectory Control and Reasoning**|
|Deng [98]|Spatial prompting + Q-learning correction + Reverse<br>curriculum learning|
|Zheng [99]|Heuristic actions + Dual-call mechanism +<br>Thought-aligned search|
|Wang [100]|MCTS framework + Trajectory evaluation +<br>State–action–reward chain|



heuristic strategies, while the outer layer evolves prompt templates to enhance diversity. The framework also introduces differential memory and adaptive perturbation mechanisms to balance search efficiency and convergence control. Meanwhile, Wang et al. [92] integrated LLM into simulated annealing, employing three-stage prompts to guide new solution generation and combining them with a temperature control mechanism to enhance the ability to escape local optima. 

Beyond traditional operators, some studies have explored the integration of LLM with RL to support strategy optimization and adaptive evolution. Ma et al. [93] proposed the AutoDH framework, which constructs a pool of heuristic functions and employs an RL agent to select the optimal function based on solution states, thereby enabling subpath optimization and feedback-driven improvement. Surina et al. [94] introduced the Evo-Tune framework, which samples high-quality candidate construction prompts during program search to guide LLM-generated programs. After performance verification, these candidates form a preference dataset used to update the language model through direct preference optimization, gradually biasing it toward generating higher-quality structures. Building on this, Huang et al. [95] proposed the CALM framework, which incorporates prompt diversification and collapse-restart mechanisms, combined with generalized reinforcement preference optimization, to continuously enhance structural generation capabilities, thereby improving stability and robustness in complex tasks. 

At a higher level of exploration, researchers have sought to integrate LLM into neuro-symbolic systems to unify semantic representation and structural constraints. Jiang et al. [96] proposed combining LLM with Transformers to map problem instances into a unified semantic space, and employing RL to train the generator, thereby improving solution quality and diversity. Tran et al. [97] developed a neural optimizer framework in which LLM automatically generates structure-aware attention biases to guide node selection. This mechanism was integrated into multiobjective optimization and lightweight enhanced heuristic decoders, achieving cross-scale generalization under lightweight fine-tuning conditions. 

In addition, some studies have focused on search trajectory control and reasoning mechanisms. Deng et al. [98] proposed the S2RCQL model for path planning tasks, which transforms spatial prompts into entity relationships to guide LLM in constructing path representations, and integrates Q-learning with reverse curriculum learning to reduce learning difficulty, thereby improving reasoning stability and generalization. Zheng et al. [99] introduced the MCTS-AHD framework, where LLM generates heuristic functions and semantic descriptions within MCTS, and a two-stage invocation aligns function code with conceptual descriptions to enhance semantic consistency and interpretability. In contrast, Wang et al. [100] proposed the PoH framework, which employs MCTS as the dominant component while invoking LLM at the trajectory and key-node levels for evaluation and refinement, forming a “state–action–reward” closed-loop decision process that further improves global search performance. 

Overall, cross-paradigm integration has opened new directions for the application of LLM in optimization algorithms. From coupling with traditional operators, to deep collaboration with RL, and further to extensions into neuro-symbolic systems and reasoning mechanisms, the transfer and coordination of LLM capabilities is gradually forming a systematic pathway. 

_2) LLM-dominated Optimization Solving:_ In the evolution of LLM-assisted OR, research that directly leverages model generation to solve optimization problems has gradually become a frontier direction. These approaches no longer rely on traditional mathematical modeling or heuristic algorithms. Instead, they employ natural language or multimodal prompts to guide LLM in generatively addressing diverse optimization tasks [101]. To systematically review their development trajectory and application characteristics, this paper classifies related studies into two categories: single-modal generative optimization methods and multimodal structure-aware methods, which will be further analyzed through representative works in the following sections. 

Single-modal generative optimization methods leverage natural language or structured text prompts to directly guide LLM in producing optimization solutions, thereby eliminating the dependence on gradient information and explicit modeling processes. These methods demonstrate advantages such as generality, interactive flexibility, and 

10 

TABLE VI 

Representative Studies on Single-modal Generative Optimization Methods 

|**Study**|**Key Mechanism**|
|---|---|
||**Phase I: Direct Solving by LLM**|
|Yang [102]|NL prompting + Meta-prompt iteration|
|**P**|**hase II: Fusion-driven Techniques**|
|Guo [103]|CoT + Historical prompts + Interactive<br>optimization|
|Liu [104]|State prediction + Utility modeling + Preference<br>ranking|
|Huang [105]|NL-to-Python + Self-debugging and verification|
|Masoud [106]|Prompt-driven + Multi-sampling + Self-ensemble|
|Iklassov [107]|Meta-prompt + Multi-trajectory + Recursive<br>subtask optimization|
|Zhong [108]|Self-evolving prompt + Accuracy loop|
|Zhang [109]|SFT + RLF + RAG|
|Jiang [110]|Structural prompt + Multi-round opt. +<br>Knowledge integration|
|**Phase **|**III: Exploring LLM’s Solving Capacity**|
|Abgaryan[111|]<br>Constraint-aware output + Dynamic control|



ease of transfer. Related studies have undergone an evolutionary process from direct solving to technique-enhanced approaches, and further to unified solving of complex constraints. Their core mechanisms and application tasks are summarized in Table VI. 

Early studies primarily focused on direct solving, aiming to validate the black-box optimization capability of LLM under a “zero-modeling” setting. A representative example is the OPRO method proposed by Yang et al. [102], which requires neither gradients nor heuristic operators but relies solely on natural language descriptions and historical solution feedback to construct meta-prompts that guide iterative solution generation by the LLM. In both continuous and combinatorial optimization tasks, OPRO demonstrated the potential for autonomous exploration of the solution space and achieved measurable improvements in accuracy in language reasoning tasks, indicating that LLM can perform basic optimization without external tool support. However, the limited performance of such methods in complex structures and multi-round tasks has driven research toward the incorporation of enhancement mechanisms. 

Subsequent studies have progressively enhanced the solving capabilities of LLM in a gradual manner. Early improvements focused on reasoning support and trajectory interpretability, such as combining CoT reasoning with iterative prompting to accumulate the dialogue history as a traceable “optimization memory,” thereby enabling the transition from “one-shot generation” to “interactive convergence” under a unified evaluation framework [103]. On the other hand, researchers have investigated decisionmaking in uncertain environments. By incorporating state prediction, utility modeling, and preference ranking, LLM can simulate the process of expected utility maximization and adaptively balance gains and risks across multiple rounds of feedback, demonstrating greater robustness in real-world domains such as agriculture and finance [104]. In addition, the work of Huang et al. [105] achieved end-to- 

end closed-loop solving by transforming natural language descriptions into executable code and integrating selfdebugging and self-verification mechanisms in the feedback loop to ensure the feasibility and stability of generated solutions. In vehicle routing problem experiments, this method demonstrated that even without manual modeling or traditional heuristic support, LLM possesses strong zero-shot optimization capabilities. 

Beyond closed-loop design, studies have also sought to improve solution diversity and stability. Masoud et al. [106] proposed a self-ensemble strategy that mitigates local convergence through multi-round sampling and selection, enabling cross-scale generalization in tasks such as the TSP. Other work explored trajectory generation and recursive decomposition, where meta-prompts produce multiple strategies that are decomposed into subtasks and recursively optimized, extending solution scope and diversity across combinatorial, scheduling, and symbolic reasoning tasks [107]. Zhong et al. [108] further introduced a self-evolving prompt mechanism driven by accuracy feedback, in which iterative “generate–evaluate–update” cycles refine prompt design, sustaining stable performance in high-dimensional structural search and supporting crossscale generalization. 

With research progress, structured input scenarios have attracted growing attention. Zhang et al. [109] built a large-scale graph–task–code dataset and introduced a twostage training process with retrieval-augmented mechanisms, enabling LLM to map natural language graph tasks to executable code and achieve cross-task generalization. Jiang et al. [110] addressed the structural matrix ordering problem using prompts based on network topology, node descriptions, and semantic context to guide LLM in generating node sequences without gradients or operators, while applying multi-round iterative optimization to accelerate convergence and improve solution quality. These advances highlight the ability of single-modal generative approaches to handle higher-dimensional structural problems. 

Researchers have increasingly focused on unified solving under complex constraints. Abgaryan et al. [111] proposed the ACCORD framework, which embeds constraint control into the output format to ensure satisfaction during decoding. Combined with task identification and LoRA routing, ACCORD enables unified solving across multiple NP-hard problem classes. This work highlights the potential of LLM in tackling optimization tasks with complex constraints and diverse problem types, offering a new perspective for general-purpose language-based optimizers. 

In summary, single-modal methods have advanced from direct generation to reasoning- and feedback-enhanced solving, but remain limited in capturing complex structures and multi-source information. To address this gap, multimodal structure-aware approaches integrate visual and linguistic inputs to improve spatial perception and structural consistency, showing particular promise for tasks such as path planning and scheduling. The following section extends this discussion to other pathways, highlighting how external knowledge and hybrid mechanisms 

11 

further enhance the modeling and solving capabilities of LLM in OR. 

In structure-aware multimodal approaches, Huang et al. [112] proposed the MLLM-V framework, which integrates text and image prompts for solving the capacitated vehicle routing problem, simulating human cognitive processes through heuristic extraction, solution generation, and feedback refinement. This demonstrates the value of visual information in enhancing the quality and generalization of generative optimization. Building on this line, Elhenawy et al. [113] introduced a multimodal reasoning framework that combines image inputs with natural language prompts, enabling LLM to intuitively solve the traveling salesman problem (TSP) and progressively refine path structures through adaptive mechanisms, thereby highlighting the potential of multimodal inputs. Furthermore, Elhenawy et al. [114] proposed a purely visiondriven framework with both three-stage and dual-agent collaborative architectures, capable of generating solutions for TSP and multiple TSP without relying on coordinates or distance matrices, underscoring the promise of visual perception in complex structural optimization. 

Overall, multimodal structure-aware approaches enhance LLM-based optimization by integrating visual and linguistic inputs, thereby improving structural understanding, stability, and generalization. Compared with single-modal methods, they offer complementary mechanisms that drive the evolution of optimization, and are expected to extend to broader inputs such as tabular and sensor data for more versatile systems. 

_3) Benchmarks for Evaluating LLM-assisted Optimization:_ To systematically evaluate the role of LLM in solving optimization problems, researchers have proposed a series of evaluation benchmarks. Unlike traditional tests that primarily assess modeling outcomes, these benchmarks place greater emphasis on reasoning and decision-making capabilities within complex optimization processes, covering a wide range of tasks such as graph-structured reasoning, path planning, task generation, optimization interpretation, and strategy improvement. 

For graph reasoning, Wang et al. [115] proposed the NLGraph benchmark, which contains 29,370 problems spanning eight categories of graph reasoning tasks, providing an important tool for solving graph problems in natural language settings. For path planning in spatiotemporal reasoning, Aghzal et al. [116] constructed the PPNL benchmark, which simulates grid-world path planning scenarios to systematically evaluate model performance across varying prompt strategies and task complexities. Focusing on plan reasoning in asynchronous multi-step tasks, Lin et al. [117] introduced the AsyncHow benchmark, which includes 1,600 high-quality instances across multiple common domains such as education, diet, health, and household activities. 

In graph computation tasks, Tang et al. [118] proposed the GraphArena benchmark, which employs a three-stage evaluation process consisting of path extraction, feasibility verification, and optimality checking. It covers four 

classes of polynomial-time tasks and six classes of NPcomplete problems. This benchmark not only provides detailed distinctions between correct, suboptimal, hallucinatory, and missing outputs but also enhances the interpretability and diagnostic capability of the reasoning process. The authors further explored four enhancement strategies—CoT prompting, instruction fine-tuning, code generation, and reasoning augmentation—examining their applicability limits and potential utility in complex graph problems. 

For the systematic evaluation of reasoning capabilities in OR, Mostajabdaveh et al. [119] proposed the ORQA benchmark, which consists of 1,513 multiple-choice questions spanning 20 application domains in OR. To analyze the importance of interpretability in optimization processes, Zhang et al. [120] constructed the first industrialscale dataset for explainable optimization, covering 30 problem types and 300 queries, and introduced the EOR framework. This framework incorporates the concept of “decision information” and combines what-if analysis with graph-structured modeling. Through the collaboration of three agent modules—Commander, Writer, and Safeguard—it generates dual outputs of code modification explanations and result variation explanations, offering a new pathway to enhance the interpretability of LLM in optimization tasks. 

For evaluating algorithm generation and end-to-end task execution in combinatorial optimization, Sun et al. [121] proposed CO-Bench, which encompasses 36 realworld problem classes, including bin packing, cutting, location, path planning, and tree-structure optimization. The benchmark provides natural language descriptions, data-loading functions, and evaluation functions, forming a complete workflow spanning data reading, algorithm design, and performance evaluation. Building on this, Feng et al. [122] developed the FrontierCO benchmark, which systematically evaluates an LLM solver across eight combinatorial optimization tasks. Results indicate that the LLM solver is generally more robust and exhibits stronger generalization capability compared to neural approaches, and in certain tasks, it rivals or even surpasses state-ofthe-art heuristic methods. However, its performance fluctuates significantly across tasks, revealing shortcomings in algorithm selection and integration scheduling. 

To validate the intelligence of LLM in heuristic design, Chen et al. [123] proposed the HeuriGym framework, which employs an iterative mechanism of “prompt generation–code execution–error feedback–multi-round refinement.” The framework establishes a benchmark covering nine real-world tasks and introduces the Quality-Yield Index as a core metric, comprehensively evaluating the reasoning ability of the intelligent agent through success rate and relative solution quality. Focusing on long-term goaldriven structural optimization, Imajuku et al. [124] developed ALE-Bench, constructed on the AtCoder Heuristic Contest, encompassing NP-hard problems such as path planning and production scheduling. It is equipped with scorers, visualization tools, and expert evaluation systems 

12 

to assess LLM’s optimization ability under both singleround and multi-round iterations. 

For large-scale search spaces, Li et al. [125] proposed OPT-BENCH, which covers 20 real-world machine learning tasks and 10 classical NP-hard combinatorial optimization problems. Accompanying it, the OPT-Agent framework simulates the human problem-solving process of “draft–optimize–debug,” supporting the entire pipeline from initial solution generation to stepwise refinement based on feedback, thereby forming a fully automated workflow that integrates task definitions, datasets, metrics, and validation scripts. 

Overall, existing benchmarks provide essential tools for evaluating LLM in optimization, supporting their transition from modeling assistants to intelligent collaborators. Yet they remain limited in task diversity, evaluation dimensions, and realism, with most focusing on static combinatorial problems and narrow metrics. Future work should expand coverage to dynamic, multimodal, and cross-domain scenarios, while establishing unified, integrated benchmarks that capture efficiency, stability, and interpretability in real-world settings. 

## IV. Domain Problems 

With increasingly complex real-world application scenarios, the demand for optimization methods continues to grow, further exposing the limitations of traditional OR regarding modeling complexity, interactivity, and interpretability. The introduction of LLM offers new perspectives for addressing these challenges, not only enhancing problem analysis and knowledge representation but also demonstrating potential advantages in interactive processes and result presentation [126]. Therefore, this section, together with the methodological pathways, systematically discusses the practical applications and future trends of LLM in typical scenarios. 

## _A. Supply Chain_ 

In supply chain optimization, LLM enhances interpretability by bridging natural language with solver execution. OptiGuide [127], which integrates GPT-4 with an optimizer, exemplifies the prompt-driven modeling pathway: it translates user requirements into optimization expressions, forms a closed feedback loop, and achieves over 90% accuracy in Microsoft Azure practice. Complementing such applications, a theoretical framework [128] systematically mapped LLM functions across supply chain stages, highlighting roles in supplier evaluation, forecasting, routing, and sustainability. Together, these studies demonstrate how LLM extends automatic modeling toward structured decision support and foreshadow external knowledge–guided mechanisms in OR. 

## _B. Urban Planning_ 

As urban systems continue to evolve, governance processes face increasingly complex challenges. While traditional OR methods possess strong theoretical rigor, 

their practical application in smart cities characterized by multi-source data and high-frequency responsiveness remains challenging. By combining reasoning and language understanding capabilities, LLM offers a novel pathway for complex decision-making in urban contexts. The CityLEO framework [129] integrates LLM reasoning with endto-end optimization, interpreting users’ natural language requirements and leveraging historical data to generate relevant objective functions and reduce problem scale. At the same time, by combining random forests with mixedinteger programming, the framework enables interpretable mappings from features to decisions, producing solutions with higher computational efficiency and greater transparency. Experimental results show that the framework outperforms traditional methods in computational efficiency, global suboptimality control, and local satisfaction improvement, highlighting the synergistic effect of LLM and traditional optimization algorithms under a hybrid paradigm. 

## _C. Food Science_ 

In the domain of sustainable food management, traditional OR approaches are increasingly constrained by modeling complexity, high expertise requirements, and limited interpretability. Recent researcher [130] have proposed a framework that integrates the knowledge of LLM with human preference modeling capabilities, coupled with combinatorial optimization techniques, to construct a complete workflow that transforms natural language inputs into optimized decision-making outputs. Experimental evaluations demonstrate that this framework can substantially reduce greenhouse gas emissions while preserving overall user satisfaction, thereby underscoring the fusion of prompt-driven pathways with structural mapping mechanisms as a promising direction for intelligent optimization. 

## _D. Job Shop Scheduling_ 

The Job Shop Scheduling Problem (JSSP) is one of the most challenging tasks in OR, having long attracted attention due to its strong constraints and combinatorial complexity. In recent years, researchers have explored incorporating LLM into JSSP solution frameworks. One line of work constructed a large-scale dataset comprising 120,000 randomly generated natural language descriptions and feasible solutions, and employed LoRA to fine-tune the Phi-3-Mini model while introducing sampling strategies to enhance scheduling performance [131]. Subsequently, the authors introduced the Starjob dataset, extended the approach to the LLaMA model, and completed singleGPU training via Rank-Stabilized LoRA. On the Tai and DMU benchmarks, their method significantly outperformed traditional heuristic and neural network baselines [132]. Collectively, these explorations highlight the potential of integrating model fine-tuning mechanisms with structured task prompting, providing new ideas for intelligent solving of complex scheduling problems. 

13 

## _E. Communication and Networking_ 

In mobile edge computing optimization, researchers have undertaken diverse explorations across related tasks. For server allocation, researchers have proposed a natural language interaction framework that leverages multiround prompting and feedback to guide LLM in generating user–server assignment schemes that satisfy constraints while minimizing latency [133]. In the task of wireless access point deployment, the LMCO framework employs structured prompts to generate deployment schemes and incorporates ray-tracing evaluation and propagation knowledge to accelerate convergence [134]. For critical node identification, the problem has been reformulated as a score-function generation task, leading to the design of an LLM-driven evolutionary optimization framework for automatically identifying the most important nodes in communication networks [135]. At the system level, further studies have explored the potential of LLM in resource scheduling, prompt design, and heuristic strategy generation, embedding them into multiple optimization paradigms and thereby extending its application boundaries in intelligent communication systems [136]. 

## V. Conclusion and Outlook 

With the continuous advancement of LLM in natural language understanding, structural generation, and reasoning control, its role in OR is shifting from exploratory studies to paradigm reconstruction and system integration. This paper reviewed three core research pathways—automatic modeling, assisted optimization, and direct solving. LLM has demonstrated capabilities in translating natural language into structured models, generating heuristics and strategies for complex optimization tasks, and enabling end-to-end problem solving. Despite these advances, key challenges remain: unstable semantic–structure mapping; fragmented research outcomes without a unified framework; limited generalization and interpretability; insufficient evaluation tools and benchmarks; and high computational cost for large-scale deployment. Addressing these issues requires progress in robust representation and closed-loop mechanisms, standardization of task abstractions and workflows, integration of symbolic reasoning and causal analysis, development of multidimensional benchmarks, and exploration of lightweight deployment strategies. Overall, research on LLM-enabled OR is entering a stage of systematic development. By advancing methodological innovation, enhancing interpretability, and establishing comprehensive evaluation systems, LLM is expected to drive the construction of next-generation intelligent optimization systems. 

## References 

- [1] Da Ros F, Soprano M, Di Gaspero L, et al. Large Language Models for Combinatorial Optimization: A Systematic Review[J]. arXiv preprint arXiv:2507.03637, 2025. 

- [2] Liu F, Yao Y, Guo P, et al. A systematic survey on large language models for algorithm design[J]. arXiv preprint arXiv:2410.14716, 2024. 

- [3] Khalil E, Dai H, Zhang Y, et al. Learning combinatorial optimization algorithms over graphs[J]. Advances in neural information processing systems, 2017, 30. 

- [4] Ramamonjison R, Yu T, Li R, et al. Nl4opt competition: Formulating optimization problems based on their natural language descriptions[C]. NeurIPS 2022 competition track. PMLR, 2023: 189-203. 

- [5] Fan Z, Ghaddar B, Wang X, et al. Artificial intelligence for operations research: Revolutionizing the operations research process[J]. arXiv preprint arXiv:2401.03244, 2024. 

- [6] Sartori C C, Blum C. Combinatorial Optimization for All: Using LLMs to Aid Non-Experts in Improving Optimization Algorithms[J]. arXiv preprint arXiv:2503.10968, 2025. 

- [7] Cai J, Xu J, Li J, et al. Exploring the improvement of evolutionary computation via large language models[C]. Proceedings of the Genetic and Evolutionary Computation Conference Companion. 2024: 83-84. 

- [8] Song C H, Wu J, Washington C, et al. Llm-planner: Few-shot grounded planning for embodied agents with large language models[C]. Proceedings of the IEEE/CVF international conference on computer vision. 2023: 2998-3009. 

- [9] Xiao, Z., Xie, J., Xu, L., Guan, S., Zhu, J., Han, X., ... & Zhang, D. (2025). A Survey of Optimization Modeling Meets LLMs: Progress and Future Directions. arXiv preprint arXiv:2508.10047. 

- [10] Zhang, Y., Cheng, R., Yi, G., & Tan, K. C. (2025). A Systematic Survey on Large Language Models for Evolutionary Optimization: From Modeling to Solving. arXiv preprint arXiv:2509.08269. 

- [11] Kaufmann A, Faure R, Sneyd H C. Introduction to operations research[J]. 1968. 

- [12] Zieyel E R. Operations research: applications and algorithms[J]. 1988. 

- [13] Bertsimas D, Tsitsiklis J N. Introduction to linear optimization[M]. Belmont, MA: Athena scientific, 1997. 

- [14] Wolsey L A, Nemhauser G L. Integer and combinatorial optimization[M]. John Wiley & Sons, 1999. 

- [15] Papadimitriou C H, Steiglitz K. Combinatorial optimization: algorithms and complexity[M]. Courier Corporation, 1998. 

- [16] Deb K, Multi-objective optimization using evolutionary algorithms[M], John Wiley & Sons, 2001. 

- [17] Brown T, Mann B, Ryder N, et al. Language models are fewshot learners[J]. Advances in neural information processing systems, 2020, 33: 1877-1901. 

- [18] Achiam J, Adler S, Agarwal S, et al. Gpt-4 technical report[J]. arXiv preprint arXiv:2303.08774, 2023. 

- [19] Huang X, Shen Q, Hu Y, et al. Llms for mathematical modeling: Towards bridging the gap between natural and mathematical languages[J]. arXiv preprint arXiv:2405.13144, 2024. 

- [20] Wei J, Wang X, Schuurmans D, et al. Chain-of-thought prompting elicits reasoning in large language models[J]. Advances in neural information processing systems, 2022, 35: 24824-24837. 

- [21] Wang X, Wei J, Schuurmans D, et al. Self-consistency improves chain of thought reasoning in language models[J]. arXiv preprint arXiv:2203.11171, 2022. 

- [22] Li Z, Li L, Lin S, et al. Know the Ropes: A Heuristic Strategy for LLM-based Multi-Agent System Design[J]. arXiv preprint arXiv:2505.16979, 2025. 

- [23] Zhu K, Wang J, Zhou J, et al. Promptrobust: Towards evaluating the robustness of large language models on adversarial prompts[C]. Proceedings of the 1st ACM workshop on large AI systems and models with privacy and safety analysis. 2023: 57-68. 

- [24] Madaan A, Tandon N, Gupta P, et al. Self-refine: Iterative refinement with self-feedback[J]. Advances in Neural Information Processing Systems, 2023, 36: 46534-46594. 

- [25] AhmadiTeshnizi A, Gao W, Udell M. Optimus: Optimization modeling using mip solvers and large language models[J]. arXiv preprint arXiv:2310.06116, 2023. 

- [26] AhmadiTeshnizi A, Gao W, Udell M. Optimus: Scalable optimization modeling with (mi) lp solvers and large language models[J]. arXiv preprint arXiv:2402.10172, 2024. 

- [27] AhmadiTeshnizi A, Gao W, Brunborg H, et al. OptiMUS-0.3: Using large language models to model and solve optimization problems at scale[J]. arXiv preprint arXiv:2407.19633, 2024. 

14 

- [28] Xiao Z, Zhang D, Wu Y, et al. Chain-of-experts: When llms meet complex operations research problems[C]. The twelfth international conference on learning representations. 2023. 

- [29] Zhang J, Wang W, Guo S, et al. Solving general naturallanguage-description optimization problems with large language models[J]. arXiv preprint arXiv:2407.07924, 2024. 

- [30] Li J, Wickman R, Bhatnagar S, et al. Abstract Operations Research Modeling Using Natural Language Inputs[J]. Information, 2025, 16(2): 128. 

- [31] Astorga N, Liu T, Xiao Y, et al. Autoformulation of mathematical optimization models using llms[J]. arXiv preprint arXiv:2411.01679, 2024. 

- [32] Yuan Z, Liu M, Wang H, et al. MA-GTS: A Multi-Agent Framework for Solving Complex Graph Problems in RealWorld Applications[J]. arXiv preprint arXiv:2502.18540, 2025. 

- [33] Zhang B, Luo P. Or-llm-agent: Automating modeling and solving of operations research optimization problem with reasoning large language model[J]. arXiv preprint arXiv:2503.10009, 2025. 

- [34] Wasserkrug S, Boussioux L, Hertog D, et al. From large language models and optimization to decision optimization copilot: A research manifesto[J]. arXiv preprint arXiv:2402.16269, 2024. 

- [35] Amarasinghe P T, Nguyen S, Sun Y, Alahakoon D, Language Models for Business Optimisation with a Real World Case Study in Production Scheduling[C], 2023. 

- [36] Li Q, Zhang L, Mak-Hau V. Synthesizing mixed-integer linear programming models from natural language descriptions[J]. arXiv preprint arXiv:2311.15271, 2023. 

- [37] Ma Z, Guo H, Chen J, et al. Llamoco: Instruction tuning of large language models for optimization code generation[J]. arXiv preprint arXiv:2403.01131, 2024. 

- [38] Wu Y, Zhang Y, Wu Y, et al. Evo-Step: Evolutionary Generation and Stepwise Validation for Optimizing LLMs in OR[J]. 

- [39] Jiang C, Shu X, Qian H, et al. LLMOPT: Learning to Define and Solve General Optimization Problems from Scratch[J]. arXiv preprint arXiv:2410.13213, 2024. 

- [40] Lu H, Xie Z, Wu Y, et al. Optmath: A scalable bidirectional data synthesis framework for optimization modeling[J]. arXiv preprint arXiv:2502.11102, 2025. 

- [41] Li X, Yang J, Wang J, et al. STRCMP: Integrating Graph Structural Priors with Language Models for Combinatorial Optimization[J]. arXiv preprint arXiv:2506.11057, 2025. 

- [42] Liu F, Tong X, Yuan M, et al. Algorithm evolution using large language model[J]. arXiv preprint arXiv:2311.15249, 2023. 

- [43] Jiang X, Wu Y, Zhang C, et al. DRoC: Elevating large language models for complex vehicle routing via decomposed retrieval of constraints[C]. 13th international Conference on Learning Representations, ICLR 2025. OpenReview. net, 2025. 

- [44] Peng M, Chen Z, Yang J, et al. Automatic milp model construction for multi-robot task allocation and scheduling based on large language models[J]. arXiv preprint arXiv:2503.13813, 2025. 

- [45] Huang C, Tang Z, Hu S, et al. Orlm: A customizable framework in training large models for automated optimization modeling[J]. Operations Research, 2025. 

- [46] Yang Z, Wang Y, Huang Y, et al. Optibench meets resocratic: Measure and improve llms for optimization modeling[J]. arXiv preprint arXiv:2407.09887, 2024. 

- [47] Wang Z, Zhu Z, Han Y, et al. OptiBench: benchmarking large language models in optimization modeling with equivalencedetection evaluation[J]. 2024. 

- [48] Zhai H, Lawless C, Vitercik E, et al. EquivaMap: Leveraging LLMs for Automatic Equivalence Checking of Optimization Formulations[J]. arXiv preprint arXiv:2502.14760, 2025. 

- [49] Singirikonda A, Kadioglu S, Uppuluri K. Text2Zinc: A CrossDomain Dataset for Modeling Optimization and Satisfaction Problems in MiniZinc[J]. arXiv preprint arXiv:2503.10642, 2025. 

- [50] Michailidis K, Tsouros D, Guns T. CP-Bench: Evaluating Large Language Models for Constraint Modelling[J]. arXiv preprint arXiv:2506.06052, 2025. 

- [51] Huang S, Yang K, Qi S, et al. When large language model meets optimization[J]. Swarm and Evolutionary Computation, 2024, 90: 101663. 

- [52] Zhang R, Liu F, Lin X, et al. Understanding the importance of evolutionary search in automated heuristic design with large language models[C],International Conference on Parallel Problem Solving from Nature. Cham: Springer Nature Switzerland, 2024: 185-202. 

- [53] Lehman J, Gordon J, Jain S, et al. Evolution through large models[M]//Handbook of evolutionary machine learning. Singapore: Springer Nature Singapore, 2023: 331-366. 

- [54] Yu H, Liu J. Deep insights into automated optimization with large language models and evolutionary algorithms[J]. arXiv preprint arXiv:2410.20848, 2024. 

- [55] Wang C, Zhao J, Jiao L, et al. When large language models meet evolutionary algorithms: Potential enhancements and challenges[J]. Research, 2025, 8: 0646. 

- [56] Yao Y, Liu F, Cheng J, et al. Evolve cost-aware acquisition functions using large language models[C]. International Conference on Parallel Problem Solving from Nature. Cham: Springer Nature Switzerland, 2024: 374-390. 

- [57] Wu X, Wu S, Wu J, et al. Evolutionary computation in the era of large language model: Survey and roadmap[J]. IEEE Transactions on Evolutionary Computation, 2024. 

- [58] van Stein N, V. Kononova A, Kotthoff L, et al. Code evolution graphs: Understanding large language model driven design of algorithms[C]. Proceedings of the Genetic and Evolutionary Computation Conference. 2025: 943-951. 

- [59] Liu F, Zhang Q, Tong X, et al. Fitness Landscape of Large Language Model-Assisted Automated Algorithm Search[J]. arXiv preprint arXiv:2504.19636, 2025. 

- [60] Liu S, Chen C, Qu X, et al. Large language models as evolutionary optimizers[C]. 2024 IEEE Congress on Evolutionary Computation (CEC). IEEE, 2024: 1-8. 

- [61] Liu F, Tong X, Yuan M, et al. An example of evolutionary computation + large language model beating human: Design of efficient guided local search[J]. CoRR, 2024. 

- [62] Liu F, Zhang R, Xie Z, et al. Llm4ad: A platform for algorithm design with large language model[J]. arXiv preprint arXiv:2412.17287, 2024. 

- [63] Li K, Liu F, Wang Z, et al. ARS: Automatic Routing Solver with Large Language Models[J]. arXiv preprint arXiv:2502.15359, 2025. 

- [64] Romera-Paredes B, Barekatain M, Novikov A, et al. Mathematical discoveries from program search with large language models[J]. Nature, 2024, 625(7995): 468-475. 

- [65] Chen Z, Zhou Z, Lu Y, et al. Qube: Enhancing automatic heuristic design via quality-uncertainty balanced evolution[J]. arXiv preprint arXiv:2412.20694, 2024. 

- [66] Ye H, Wang J, Cao Z, et al. Reevo: Large language models as hyper-heuristics with reflective evolution[J]. Advances in neural information processing systems, 2024, 37: 43571-43608. 

- [67] Sun Y, Ye F, Zhang X, et al. Autosat: Automatically optimize sat solvers via large language models[J]. arXiv preprint arXiv:2402.10705, 2024. 

- [68] Zhong R, Xu Y, Zhang C, et al. Leveraging large language model to generate a novel metaheuristic algorithm with CRISPE framework[J]. Cluster Computing, 2024, 27(10): 13835-13869. 

- [69] Yang X, Song L, Zhang Y, et al. HeurAgenix: A Multi-Agent LLM-Based Paradigm for Adaptive Heuristic Evolution and Selection in Combinatorial Optimization[J]. 

- [70] Yang X, Zhang L, Qian H, et al. HeurAgenix: Leveraging LLMs for Solving Complex Combinatorial Optimization Challenges[J]. arXiv preprint arXiv:2506.15196, 2025. 

- [71] Huang J, Li X, Gao L, et al. Automatic programming via large language models with population self-evolution for dynamic job shop scheduling problem[J]. arXiv preprint arXiv:2410.22657, 2024. 

- [72] Dat P V T, Doan L, Binh H T T. Hsevo: Elevating automatic heuristic design with diversity-driven harmony search and genetic algorithm using llms[C]. Proceedings of the AAAI Conference on Artificial Intelligence. 2025, 39(25): 26931-26938. 

- [73] Huang Z, Guo L, Li W, et al. GraphThought: Graph Combinatorial Optimization with Thought Generation[J]. arXiv preprint arXiv:2502.11607, 2025. 

- [74] Ling H, Parashar S, Khurana S, et al. Complex LLM planning via automated heuristics discovery[J]. arXiv preprint arXiv:2502.19295, 2025. 

15 

- [75] Ali S, Ashraf M, Hegazy S, et al. PAIR: A Novel Large Language Model-Guided Selection Strategy for Evolutionary Algorithms[J]. arXiv preprint arXiv:2503.03239, 2025. 

- [76] Bömer T, Koltermann N, Disselnmeyer M, et al. Leveraging large language models to develop heuristics for emerging optimization problems[J]. arXiv preprint arXiv:2503.03350, 2025. 

- [77] Wu X, Wang D, Wu C, et al. Efficient heuristics generation for solving combinatorial optimization problems using large language models[C]. Proceedings of the 31st ACM SIGKDD Conference on Knowledge Discovery and Data Mining V. 2. 2025: 3228-3239. 

- [78] Thach N, Riahifar A, Huynh N, et al. RedAHD: ReductionBased End-to-End Automatic Heuristic Design with Large Language Models[J]. arXiv preprint arXiv:2505.20242, 2025. 

- [79] Shi Y, Zhou J, Song W, et al. Generalizable Heuristic Generation Through Large Language Models with MetaOptimization[J]. arXiv preprint arXiv:2505.20881, 2025. 

- [80] Duan R, Liu Y, Dong X, et al. EALG: Evolutionary Adversarial Generation of Language Model-Guided Generators for Combinatorial Optimization[J]. arXiv preprint arXiv:2506.02594, 2025. 

- [81] Liu F, Lin X, Yao S, et al. Large language model for multiobjective evolutionary optimization[C]. International Conference on Evolutionary Multi-Criterion Optimization. Singapore: Springer Nature Singapore, 2025: 178-191. 

- [82] Wang Z, Liu S, Chen J, et al. Large language model-aided evolutionary search for constrained multiobjective optimization[C]. International Conference on Intelligent Computing. Singapore: Springer Nature Singapore, 2024: 218-230. 

- [83] Liu W, Chen L, Tang Z. Large language model aided multiobjective evolutionary algorithm: a low-cost adaptive approach[J]. arXiv preprint arXiv:2410.02301, 2024. 

- [84] Huang Y, Wu S, Zhang W, et al. Autonomous multi-objective optimization using large language model[J]. IEEE Transactions on Evolutionary Computation, 2025. 

- [85] Yao S, Liu F, Lin X, et al. Multi-objective evolution of heuristic using large language model[C]. Proceedings of the AAAI Conference on Artificial Intelligence. 2025, 39(25): 27144-27152. 

- [86] Forniés-Tabuenca D, Uribe A, Otamendi U, et al. REMoH: A Reflective Evolution of Multi-objective Heuristics approach via Large Language Models[J]. arXiv preprint arXiv:2506.07759, 2025. 

- [87] Qian H, Dong S, Yu H, et al. Unifying All Species: LLM-based Hyper-Heuristics for Multi-objective Optimization[J]. 

- [88] Li C, Han Z, Jiang J, et al. Generative Evolution Attacks Portfolio Selection[C]. 2024 IEEE Congress on Evolutionary Computation (CEC). IEEE, 2024: 1-8. 

- [89] Sartori C C, Blum C, Bistaffa F, Rodríguez Corominas G, Metaheuristics and Large Language Models Join Forces: Toward an Integrated Optimization Approach[J], IEEE Access, 2025, 13: 2058-2079. 

- [90] Sartori C C, Blum C. Improving existing optimization algorithms with llms[J]. arXiv preprint arXiv:2502.08298, 2025. 

- [91] Ye H, Xu H, Yan A, et al. Large Language Model-driven Large Neighborhood Search for Large-Scale MILP Problems[C]. Forty-second International Conference on Machine Learning. 2025. 

- [92] Wang D, Zhang Z, Teng Y. Large Language Model Implemented Simulated Annealing Algorithm for Traveling Salesman Problem[C]. 2024 IEEE International Conference on Systems, Man, and Cybernetics (SMC). IEEE, 2024: 209-214. 

- [93] Ma L, Hao X, Yang R, et al. Automatic Algorithm Design Assisted by LLMs for Solving Vehicle Routing Problems[C]. 2024 IEEE 17th International Conference on Signal Processing (ICSP). IEEE, 2024: 247-252. 

- [94] Surina A, Mansouri A, Quaedvlieg L, et al. Algorithm discovery with llms: Evolutionary search meets reinforcement learning[J]. arXiv preprint arXiv:2504.05108, 2025. 

- [95] Huang Z, Wu W, Wu K, et al. Calm: Co-evolution of algorithms and language model for automatic heuristic design[J]. arXiv preprint arXiv:2505.12285, 2025. 

- [96] Jiang X, Wu Y, Wang Y, et al. Bridging Large Language Models and Optimization: A Unified Framework for Text-attributed Combinatorial Optimization[J]. arXiv preprint arXiv:2408.12214, 2024. 

- [97] Tran C D, Nguyen-Tri Q, Binh H T T, et al. Large language models powered neural solvers for generalized vehicle routing 

   - problems[C]. Towards Agentic AI for Science: Hypothesis Generation, Comprehension, Quantification, and Validation. 

- [98] Deng H, Zhang H, Ou J, et al. Can LLM be a good path planner based on prompt engineering? mitigating the hallucination for path planning[C]. International Conference on Intelligent Computing. Singapore: Springer Nature Singapore, 2025: 3-15. 

- [99] Zheng Z, Xie Z, Wang Z, et al. Monte carlo tree search for comprehensive exploration in llm-based automatic heuristic design[J]. arXiv preprint arXiv:2501.08603, 2025. 

- [100] Wang H, Zhang X, Mu C. Planning of Heuristics: Strategic Planning on Large Language Models with Monte Carlo Tree Search for Automating Heuristic Optimization[J]. arXiv preprint arXiv:2502.11422, 2025. 

- [101] Zhang M R, Desai N, Bae J, et al. Using large language models for hyperparameter optimization[J]. arXiv preprint arXiv:2312.04528, 2023. 

- [102] Yang C, Wang X, Lu Y, et al. Large language models as optimizers[C]. The Twelfth International Conference on Learning Representations. 2023. 

- [103] Guo P F, Chen Y H, Tsai Y D, et al. Towards optimizing with large language models[J]. arXiv preprint arXiv:2310.05204, 2023. 

- [104] Liu O, Fu D, Yogatama D, et al. Dellma: Decision making under uncertainty with large language models[J]. arXiv preprint arXiv:2402.02392, 2024. 

- [105] Huang Z, Shi G, Sukhatme G S. Can Large Language Models Solve Robot Routing?[J]. arXiv preprint arXiv:2403.10795, 2024. 

- [106] Masoud M, Abdelhay A, Elhenawy M. Exploring combinatorial problem solving with large language models: A case study on the travelling salesman problem using gpt-3.5 turbo[J]. arXiv preprint arXiv:2405.01997, 2024. 

- [107] Iklassov Z, Du Y, Akimov F, et al. Self-guiding exploration for combinatorial problems[J]. Advances in Neural Information Processing Systems, 2024, 37: 130569-130601. 

- [108] Zhong R, Cao Y, Yu J, et al. Large language model assisted adversarial robustness neural architecture search[C]. 2024 6th International Conference on Data-driven Optimization of Complex Systems (DOCS). IEEE, 2024: 433-437. 

- [109] Zhang Q, Hong X, Tang J, et al. Gcoder: Improving large language model for generalized graph problem solving[J]. arXiv preprint arXiv:2410.19084, 2024. 

- [110] Jiang S, Xie M, Luo J. Large language models for combinatorial optimization of design structure matrix[J]. arXiv preprint arXiv:2411.12571, 2024. 

- [111] Abgaryan H, Cazenave T, Harutyunyan A. ACCORD: Autoregressive Constraint-satisfying Generation for COmbinatorial Optimization with Routing and Dynamic attention[J]. arXiv preprint arXiv:2506.11052, 2025. 

- [112] Huang Y, Zhang W, Feng L, et al. How multimodal integration boost the performance of llm for optimization: Case study on capacitated vehicle routing problems[C]. 2025 IEEE Symposium for Multidisciplinary Computational Intelligence Incubators (MCII). IEEE, 2025: 1-7. 

- [113] Elhenawy M, Abdelhay A, Alhadidi T I, et al. Eyeballing combinatorial problems: A case study of using multimodal large language models to solve traveling salesman problems[C]. International Conference on Intelligent Systems, Blockchain, and Communication Technologies. Cham: Springer Nature Switzerland, 2024: 341-355. 

- [114] Elhenawy M, Abutahoun A, Alhadidi T I, et al. Visual reasoning and multi-agent approach in multimodal large language models (mllms): Solving tsp and mtsp combinatorial challenges[J]. arXiv preprint arXiv:2407.00092, 2024. 

- [115] Wang H, Feng S, He T, et al. Can language models solve graph problems in natural language?[J]. Advances in Neural Information Processing Systems, 2023, 36: 30840-30861. 

- [116] Aghzal M, Plaku E, Yao Z. Can large language models be good path planners? a benchmark and investigation on spatialtemporal reasoning[J]. arXiv preprint arXiv:2310.03249, 2023. 

- [117] Lin F, La Malfa E, Hofmann V, et al. Graph-enhanced large language models in asynchronous plan reasoning[J]. arXiv preprint arXiv:2402.02805, 2024. 

- [118] Tang J, Zhang Q, Li Y, et al. Grapharena: Evaluating and exploring large language models on graph computation[J]. arXiv preprint arXiv:2407.00379, 2024. 

16 

- [119] Mostajabdaveh M, Yu T T L, Dash S C B, et al. Evaluating LLM Reasoning in the Operations Research Domain with ORQA[C]. Proceedings of the AAAI Conference on Artificial Intelligence. 2025, 39(23): 24902-24910. 

- [120] Zhang Y, Kang Q, Yu W Y, et al. Decision information meets large language models: The future of explainable operations research[J]. arXiv preprint arXiv:2502.09994, 2025. 

- [121] Sun W, Feng S, Li S, et al. Co-bench: Benchmarking language model agents in algorithm search for combinatorial optimization[J]. arXiv preprint arXiv:2504.04310, 2025. 

- [122] Feng S, Sun W, Li S, et al. A Comprehensive Evaluation of Contemporary ML-Based Solvers for Combinatorial Optimization[J]. arXiv preprint arXiv:2505.16952, 2025. 

- [123] Chen H, Wang Y, Cai Y, et al. HeuriGym: An Agentic Benchmark for LLM-Crafted Heuristics in Combinatorial Optimization[J]. arXiv preprint arXiv:2506.07972, 2025. 

- [124] Imajuku Y, Horie K, Iwata Y, et al. ALE-Bench: A Benchmark for Long-Horizon Objective-Driven Algorithm Engineering[J]. arXiv preprint arXiv:2506.09050, 2025. 

- [125] Li X, Chen J, Fang X, et al. OPT-BENCH: Evaluating LLM Agent on Large-Scale Search Spaces Optimization Problems[J]. arXiv preprint arXiv:2506.10764, 2025. 

- [126] Wang T, Yu W Y, She R, et al. Leveraging large language models for solving rare mip challenges[J]. arXiv preprint arXiv:2409.04464, 2024. 

- [127] Li B, Mellou K, Zhang B, et al. Large language models for supply chain optimization[J]. arXiv preprint arXiv:2307.03875, 2023. 

- [128] Maryniak A, Pogorzelec-Glaser K. ChatGPT in supply chain management–a research model[J]. Zeszyty Naukowe Politechniki Śląskiej. Organizacja i Zarządzanie, 2024 (203). 

- [129] Jiao Z, Sha M, Zhang H, et al. City-LEO: Toward transparent city management using LLM with end-to-end optimization[J]. arXiv preprint arXiv:2406.10958, 2024. 

- [130] Thomas A T, Yee A, Mayne A, et al. What can large language models do for sustainable food?[J]. arXiv preprint arXiv:2503.04734, 2025. 

- [131] Abgaryan H, Harutyunyan A, Cazenave T. Llms can schedule[J]. arXiv preprint arXiv:2408.06993, 2024. 

- [132] Abgaryan H, Cazenave T, Harutyunyan A. Starjob: Dataset for llm-driven job shop scheduling[J]. arXiv preprint arXiv:2503.01877, 2025. 

- [133] Song Y, Lee W, Lee S H. Task Offloading with Large Language Models in Mobile Edge Computing[C]. 2024 15th International Conference on Information and Communication Technology Convergence (ICTC). IEEE, 2024: 917-921. 

- [134] Qiu K, Bakirtzis S, Wassell I, et al. Large language modelbased wireless network design[J]. IEEE Wireless Communications Letters, 2024. 

- [135] Mao J, Zou D, Sheng L, et al. Identify critical nodes in complex network with large language models[J]. arXiv preprint arXiv:2403.03962, 2024. 

- [136] Zhou H, Hu C, Yuan Y, et al. Large language model (llm) for telecommunications: A comprehensive survey on principles, key techniques, and opportunities[J]. IEEE Communications Surveys & Tutorials, 2024. 

This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible. 

